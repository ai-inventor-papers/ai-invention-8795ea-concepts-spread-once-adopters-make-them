#!/usr/bin/env python3
"""Zero-credit full scan of the OpenAlex works snapshot (s3://openalex/data/parquet/works, 2,040 files,
476M works) reading only 7 leaf columns (title, publication_year, type, is_paratext, is_xpac,
primary_location.source.id, topics.id) through HTTP range requests.

Per file it produces
  * title matches for every P78 phrase (OpenAlex-like English analysis: lowercase, possessive strip,
    stop-word removal with position gaps, Porter stemming, positional phrase match),
  * background topic tag counts per year (1995-2025) over base works (article|review, not paratext, not xpac),
  * base-work counts per year (with / without a topic),
  * full-corpus topic-pair co-occurrence counts for the three backbone slices (2000-04, 2005-09, 2010-14).
Aggregates are checkpointed in scan/ so the scan resumes where it stopped.

Usage: python scan_snapshot.py [--limit N] [--workers W]"""
from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import re
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from functools import lru_cache
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
from loguru import logger

from config import LOGS, PANEL, ROOT, SLICES, SNAP

SCAN = ROOT / "scan"
SCAN.mkdir(exist_ok=True)
Y0, Y1 = 1995, 2025
NY = Y1 - Y0 + 1
COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
        "topics.list.element.id"]
ES_STOP = set("a an and are as at be but by for if in into is it no not of on or such that the their then there "
              "these they this to was will with".split())
TOKEN_RE = re.compile(r"[^\W_]+(?:\.[^\W_]+)*", re.UNICODE)


# ----------------------------------------------------------------------------- text analysis
_STEMMER = None


def _stem(w: str) -> str:
    global _STEMMER
    if _STEMMER is None:
        import snowballstemmer
        _STEMMER = snowballstemmer.stemmer("porter")
    return _cached_stem(w)


@lru_cache(maxsize=500_000)
def _cached_stem(w: str) -> str:
    return _STEMMER.stemWord(w)


def normalise(text: str) -> str:
    t = text.lower().replace("’", "'")
    t = re.sub(r"'s\b", "", t)
    return re.sub(r"[\-‐‑‒–—/]", " ", t)


def analyse(text: str) -> list[tuple[int, str]]:
    """(position, stem) for non-stop tokens; stop words keep their position slot (ES semantics)."""
    out = []
    for p, tok in enumerate(TOKEN_RE.findall(normalise(text))):
        if tok in ES_STOP:
            continue
        out.append((p, _stem(tok)))
    return out


def phrase_spec(phrase: str) -> tuple[tuple[int, str], ...]:
    a = analyse(phrase)
    p0 = a[0][0]
    return tuple((p - p0, s) for p, s in a)


def anchor(phrase: str) -> str:
    """Longest common prefix of a phrase token and its stem (a superset prefilter anchor)."""
    best = ""
    for tok in TOKEN_RE.findall(normalise(phrase)):
        if tok in ES_STOP:
            continue
        s = _stem(tok)
        k = 0
        while k < min(len(s), len(tok)) and s[k] == tok[k]:
            k += 1
        cand = tok[:k]
        if len(cand) > len(best):
            best = cand
    return best


def build_specs() -> tuple[list[tuple[int, tuple]], str]:
    specs = []
    anchors = set()
    for ci, (name, aliases, _) in enumerate(PANEL):
        for ph in [name] + aliases:
            specs.append((ci, phrase_spec(ph)))
            anchors.add(re.escape(anchor(ph)))
    regex = r"\b(?:" + "|".join(sorted(anchors, key=len, reverse=True)) + ")"
    return specs, regex


def match_title(title: str, specs) -> set[int]:
    a = analyse(title)
    if not a:
        return set()
    pos = {}
    for p, s in a:
        pos.setdefault(s, []).append(p)
    hit = set()
    for ci, spec in specs:
        if ci in hit:
            continue
        first = spec[0][1]
        if first not in pos:
            continue
        for p0 in pos[first]:
            if all(p0 + off in pos.get(s, ()) for off, s in spec[1:]):
                hit.add(ci)
                break
    return hit


# ----------------------------------------------------------------------------- worker
_W: dict = {}


def _init_worker(topic_ids: list[int]) -> None:
    lut = np.full(20000, -1, dtype=np.int32)
    for i, t in enumerate(topic_ids):
        lut[t] = i
    specs, regex = build_specs()
    _W.update(lut=lut, nt=len(topic_ids), specs=specs, regex=regex)
    pa.set_cpu_count(1)


def process_file(fi: int, key: str, size: int) -> dict:
    from rangefile import read_columns
    t_start = time.time()
    tb = read_columns(key, size, COLS, n_threads=8)
    t_io = time.time() - t_start
    n = tb.num_rows
    lut, nt = _W["lut"], _W["nt"]
    year = tb.column("publication_year").to_numpy(zero_copy_only=False).astype(np.int64)
    year = np.where(np.isnan(year.astype(float)), -1, year) if year.dtype.kind == "f" else year
    typ = tb.column("type")
    is_base_type = pc.fill_null(pc.is_in(typ, value_set=pa.array(["article", "review"])), False).to_numpy(
        zero_copy_only=False)
    para = pc.fill_null(tb.column("is_paratext"), False).to_numpy(zero_copy_only=False)
    xpac = pc.fill_null(tb.column("is_xpac"), False).to_numpy(zero_copy_only=False)
    base = is_base_type & ~para & ~xpac
    base_incl_xpac = is_base_type & ~para
    # topics -> index arrays
    tl = tb.column("topics").combine_chunks()
    lens = pc.fill_null(pc.list_value_length(tl), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    flat = pc.list_flatten(tl)
    tid_str = pc.struct_field(flat, [0])
    tid = pc.cast(pc.utf8_slice_codeunits(tid_str, 22), pa.int64()).to_numpy(zero_copy_only=False)
    tidx = lut[np.clip(tid, 0, 19999)]
    offs = np.zeros(n + 1, dtype=np.int64)
    offs[1:] = np.cumsum(lens)
    inyr = (year >= Y0) & (year <= Y1)
    # base counts per year
    G = np.bincount(year[base & inyr] - Y0, minlength=NY)
    Gx = np.bincount(year[base_incl_xpac & inyr] - Y0, minlength=NY)
    Gt = np.bincount(year[base & inyr & (lens > 0)] - Y0, minlength=NY)
    # background topic tags per year
    row_of_tag = np.repeat(np.arange(n), lens)
    ok = base[row_of_tag] & inyr[row_of_tag] & (tidx >= 0)
    bg = np.bincount((year[row_of_tag[ok]] - Y0) * nt + tidx[ok], minlength=NY * nt).reshape(NY, nt)
    # topic pairs per slice (first 3 topics)
    L = np.minimum(lens, 3)

    def tpos(j):
        v = np.full(n, -1, dtype=np.int64)
        m = L > j
        v[m] = tidx[offs[:-1][m] + j]
        return v
    t0, t1, t2 = tpos(0), tpos(1), tpos(2)
    pairs = []
    for (a, b) in ((t0, t1), (t0, t2), (t1, t2)):
        m = (a >= 0) & (b >= 0) & (a != b)
        pairs.append((np.minimum(a[m], b[m]), np.maximum(a[m], b[m]), np.nonzero(m)[0]))
    pair_out = []
    for (ya, yb) in SLICES:
        ks, cs = [], []
        keys = []
        for a, b, rows in pairs:
            sel = base[rows] & (year[rows] >= ya) & (year[rows] <= yb)
            keys.append(a[sel] * nt + b[sel])
        kk = np.concatenate(keys) if keys else np.zeros(0, dtype=np.int64)
        u, c = np.unique(kk, return_counts=True)
        pair_out.append((u.astype(np.int64), c.astype(np.int32)))
    # title matching (all rows; flags stored)
    titles = tb.column("title")
    low = pc.utf8_lower(pc.fill_null(titles, ""))
    cand = pc.match_substring_regex(low, _W["regex"]).to_numpy(zero_copy_only=False)
    cidx = np.nonzero(cand)[0]
    src_col = pc.struct_field(pc.struct_field(tb.column("primary_location"), [0]), [0])
    matches = []
    if len(cidx):
        tsub = titles.take(pa.array(cidx)).to_pylist()
        ssub = src_col.take(pa.array(cidx)).to_pylist()
        for r, t, s in zip(cidx, tsub, ssub):
            if not t:
                continue
            hit = match_title(t, _W["specs"])
            if hit:
                matches.append({"f": fi, "c": sorted(hit), "y": int(year[r]), "b": bool(base[r]),
                                "x": bool(xpac[r]), "s": int(s[22:]) if s else None,
                                "t": [int(x) for x in tidx[offs[r]:offs[r + 1]] if x >= 0],
                                "ti": t[:300]})
    del tb, low, titles
    gc.collect()
    return {"fi": fi, "n": n, "G": G, "Gx": Gx, "Gt": Gt, "bg": bg, "pairs": pair_out, "matches": matches,
            "n_cand": int(len(cidx)), "t_io": t_io, "t_all": time.time() - t_start}


# ----------------------------------------------------------------------------- driver
def topic_ids() -> list[int]:
    import pyarrow.parquet as pq
    ids = set()
    for f in sorted((SNAP / "topics").rglob("*.parquet")):
        for x in pq.read_table(f, columns=["id"]).column("id").to_pylist():
            ids.add(int(x.split("/T")[-1]))
    return sorted(ids)


def load_ckpt(nt: int):
    ck = SCAN / "ckpt.npz"
    done = json.loads((SCAN / "done.json").read_text()) if (SCAN / "done.json").exists() else []
    if ck.exists() and done:
        z = np.load(ck)
        pairs = []
        for s in range(len(SLICES)):
            m = np.zeros(nt * nt, dtype=np.int32)
            m[z[f"pk{s}"]] = z[f"pc{s}"]
            pairs.append(m)
        return set(done), z["G"], z["Gx"], z["Gt"], z["bg"], pairs, int(z["n"])
    return set(), np.zeros(NY, np.int64), np.zeros(NY, np.int64), np.zeros(NY, np.int64), \
        np.zeros((NY, nt), np.int64), [np.zeros(nt * nt, dtype=np.int32) for _ in SLICES], 0


def save_ckpt(done, G, Gx, Gt, bg, pairs, n) -> None:
    d = {"G": G, "Gx": Gx, "Gt": Gt, "bg": bg, "n": np.array(n)}
    for s, m in enumerate(pairs):
        nz = np.nonzero(m)[0]
        d[f"pk{s}"] = nz
        d[f"pc{s}"] = m[nz]
    tmp = SCAN / "ckpt_tmp.npz"
    np.savez(tmp, **d)
    tmp.replace(SCAN / "ckpt.npz")
    (SCAN / "done.json").write_text(json.dumps(sorted(done)))


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--ckpt_every", type=int, default=100)
    args = ap.parse_args()
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "scan.log", rotation="30 MB", level="DEBUG")
    man = json.loads((SNAP / "works_manifest.json").read_text())
    files = [(i, f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"]) for i, f in
             enumerate(man["files"])]
    tids = topic_ids()
    nt = len(tids)
    (SCAN / "topic_ids.json").write_text(json.dumps(tids))
    specs, regex = build_specs()
    (SCAN / "match_spec.json").write_text(json.dumps({"regex": regex, "specs": specs}, indent=0))
    done, G, Gx, Gt, bg, pairs, nrows = load_ckpt(nt)
    # drop match lines from files not in the checkpoint (they will be redone)
    mfile = SCAN / "matches.jsonl"
    if mfile.exists():
        keep = [ln for ln in mfile.read_text().splitlines() if ln and json.loads(ln)["f"] in done]
        mfile.write_text("\n".join(keep) + ("\n" if keep else ""))
    todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])  # largest first
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"topics={nt}  files done={len(done)}  todo={len(todo)}  regex_len={len(regex)}")
    t0 = time.time()
    n_new = 0
    since = 0
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"),
                             initializer=_init_worker, initargs=(tids,)) as ex, mfile.open("a") as mf:
        pending = set()
        it = iter(todo)
        failures = []

        def submit_next() -> bool:
            try:
                fi, key, size = next(it)
            except StopIteration:
                return False
            fut = ex.submit(process_file, fi, key, size)
            fut.fi = fi
            pending.add(fut)
            return True
        for _ in range(args.workers * 2):
            submit_next()
        while pending:
            fin, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in fin:
                pending.discard(fut)
                try:
                    r = fut.result()
                except Exception as e:  # noqa: BLE001 -- keep scanning; failed files are retried on resume
                    logger.error(f"file {fut.fi} failed: {e!r}"[:400])
                    failures.append(fut.fi)
                    submit_next()
                    continue
                G += r["G"]; Gx += r["Gx"]; Gt += r["Gt"]; bg += r["bg"]
                for s, (u, c) in enumerate(r["pairs"]):
                    np.add.at(pairs[s], u, c)
                nrows += r["n"]
                for m in r["matches"]:
                    mf.write(json.dumps(m) + "\n")
                done.add(r["fi"])
                n_new += 1
                since += 1
                el = time.time() - t0
                if n_new % 20 == 0 or n_new == len(todo):
                    logger.info(f"{n_new}/{len(todo)} files  {el/60:.1f} min  eta {(len(todo)-n_new)*el/n_new/60:.1f} min"
                                f"  last io={r['t_io']:.1f}s all={r['t_all']:.1f}s cand={r['n_cand']} "
                                f"matches={len(r['matches'])} rows={nrows}")
                if since >= args.ckpt_every:
                    mf.flush()
                    save_ckpt(done, G, Gx, Gt, bg, pairs, nrows)
                    since = 0
                submit_next()
        mf.flush()
    save_ckpt(done, G, Gx, Gt, bg, pairs, nrows)
    logger.info(f"scan finished: files done={len(done)}/{len(files)} rows={nrows} failures={failures}")


if __name__ == "__main__":
    main()
