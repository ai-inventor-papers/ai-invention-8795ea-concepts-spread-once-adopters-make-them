"""STEP 0: schema probe + timing of column reads on the works snapshot."""
import json, sys, time, struct
from pathlib import Path
import pyarrow as pa, pyarrow.parquet as pq
from rangefile import _get_range, RangeFile, read_columns
ROOT = Path(__file__).resolve().parent
man = json.loads((ROOT/"snapshot/works_manifest.json").read_text())
files = [(f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"]) for f in man["files"]]
print(len(files), sum(s for _, s in files)/1e12, "TB")
key, size = max(files, key=lambda f: f[1])
url = "https://openalex.s3.amazonaws.com/" + key
tail = _get_range(url, size - min(size, 8 << 20), size - 1)
flen = struct.unpack("<I", tail[-8:-4])[0]
meta = pq.ParquetFile(pa.PythonFile(RangeFile(size, {size - len(tail): tail}), mode="r")).metadata
paths = sorted({meta.row_group(0).column(c).path_in_schema for c in range(meta.row_group(0).num_columns)})
print("rows", meta.num_rows, "rgs", meta.num_row_groups)
# column sizes
sz = {}
for rg in range(meta.num_row_groups):
    r = meta.row_group(rg)
    for c in range(r.num_columns):
        col = r.column(c); sz[col.path_in_schema] = sz.get(col.path_in_schema, 0) + col.total_compressed_size
Path(ROOT/"logs/schema_leaf_paths.json").write_text(json.dumps({p: sz[p] for p in paths}, indent=0))
for p in paths:
    if any(k in p for k in ["concept", "title", "topic", "primary_location.source.id", "year", "type", "paratext", "xpac", "keywords"]):
        print(p, round(sz[p]/1e6, 2), "MB")
