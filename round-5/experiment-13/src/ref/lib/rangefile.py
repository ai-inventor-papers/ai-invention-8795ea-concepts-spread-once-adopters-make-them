"""Column-pruned remote parquet reading over plain HTTP range requests.

pyarrow's own S3 reader issues many small serial requests (measured ~10 s per 1 GB works file for 36 MB of
needed column chunks). Here we fetch the footer, work out the byte ranges of the needed column chunks, fetch
them concurrently, and serve them to pyarrow from memory through a file-like object (the workspace filesystem
does not support sparse files, so a local sparse copy is not an option)."""
from __future__ import annotations

import bisect
import io
import struct
import time
from concurrent.futures import ThreadPoolExecutor

import pyarrow as pa
import pyarrow.parquet as pq
import requests

S3_HTTP = "https://openalex.s3.amazonaws.com/"
_session = requests.Session()
_adapter = requests.adapters.HTTPAdapter(pool_connections=32, pool_maxsize=32)
_session.mount("https://", _adapter)


def _get_range(url: str, start: int, end: int) -> bytes:
    """Inclusive byte range with retries."""
    err = None
    for k in range(6):
        if k:
            time.sleep(2 * k)
        try:
            r = _session.get(url, headers={"Range": f"bytes={start}-{end}"}, timeout=120)
            if r.status_code in (200, 206) and len(r.content) == end - start + 1:
                return r.content
            err = f"HTTP {r.status_code} len={len(r.content)}"
        except requests.RequestException as e:
            err = repr(e)
    raise RuntimeError(f"range fetch failed {url} {start}-{end}: {err}")


class RangeFile(io.RawIOBase):
    """Read-only file object that serves bytes only from pre-fetched ranges."""

    def __init__(self, size: int, chunks: dict[int, bytes]):
        super().__init__()
        self._size = size
        # merge overlapping / touching buffers so every request falls inside one buffer
        merged: list[tuple[int, bytes]] = []
        for s in sorted(chunks):
            b = chunks[s]
            if merged and s <= merged[-1][0] + len(merged[-1][1]):
                ps, pb = merged[-1]
                end = s + len(b)
                if end > ps + len(pb):
                    pb = pb + b[ps + len(pb) - s:]
                merged[-1] = (ps, pb)
            else:
                merged.append((s, b))
        self._chunks = dict(merged)
        self._starts = [s for s, _ in merged]
        self._pos = 0

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self._pos

    def seek(self, pos: int, whence: int = 0) -> int:
        if whence == 0:
            self._pos = pos
        elif whence == 1:
            self._pos += pos
        else:
            self._pos = self._size + pos
        return self._pos

    def size(self) -> int:
        return self._size

    def read(self, n: int = -1) -> bytes:
        if n is None or n < 0:
            n = self._size - self._pos
        n = min(n, self._size - self._pos)
        i = bisect.bisect_right(self._starts, self._pos) - 1
        if i < 0:
            raise OSError(f"offset {self._pos} not fetched")
        s = self._starts[i]
        buf = self._chunks[s]
        off = self._pos - s
        if off + n > len(buf):
            raise OSError(f"range {self._pos}+{n} not fully fetched (chunk {s}+{len(buf)})")
        self._pos += n
        return buf[off:off + n]

    def readinto(self, b) -> int:
        data = self.read(len(b))
        b[:len(data)] = data
        return len(data)


def read_columns(key: str, size: int, columns: list[str], n_threads: int = 12,
                 merge_gap: int = 1 << 20) -> pa.Table:
    """Read `columns` (parquet leaf paths, e.g. 'topics.list.element.id') of the snapshot file `key`."""
    url = S3_HTTP + key
    tail_len = min(size, 2 << 20)
    tail = _get_range(url, size - tail_len, size - 1)
    assert tail[-4:] == b"PAR1", "not a parquet file"
    flen = struct.unpack("<I", tail[-8:-4])[0]
    if flen + 8 > tail_len:
        tail_len = flen + 8
        tail = _get_range(url, size - tail_len, size - 1)
    chunks = {size - tail_len: tail}
    meta = pq.ParquetFile(pa.PythonFile(RangeFile(size, dict(chunks)), mode="r")).metadata
    want = set(columns)
    ranges = []
    for rg in range(meta.num_row_groups):
        r = meta.row_group(rg)
        for c in range(r.num_columns):
            col = r.column(c)
            if col.path_in_schema in want:
                start = col.data_page_offset
                if col.has_dictionary_page and col.dictionary_page_offset and col.dictionary_page_offset > 0:
                    start = min(start, col.dictionary_page_offset)
                ranges.append((start, start + col.total_compressed_size - 1))
    ranges.sort()
    merged: list[list[int]] = []
    for a, b in ranges:
        if merged and a - merged[-1][1] <= merge_gap:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    with ThreadPoolExecutor(n_threads) as ex:
        datas = list(ex.map(lambda ab: _get_range(url, ab[0], ab[1]), merged))
    for (a, _), d in zip(merged, datas):
        chunks[a] = d
    # collapse overlap with the tail chunk (tail is last; data ranges end before the footer)
    pf = pq.ParquetFile(pa.PythonFile(RangeFile(size, chunks), mode="r"))
    return pf.read(columns=columns, use_threads=False)
