#!/usr/bin/env python3
"""S2 PASS M: mining sample over every 5th works file (fi % 5 == 0; titles only; publication years 2000..2017).

Same base filter as EXP10 passC (article|review, not paratext, not xpac) and the same venue-field LUT. Per file:
  passM/parts/ng_XXXX.npz      (year, key hash, n-gram length, title count) rows, sorted by the top-4-bit bucket
  passM/parts/titles_XXXX.parquet  sample titles (work id, year, vfield, source id, title[:300]) for string
                               recovery / POS / the source-diversity burst filter (v2)
  passM/parts/bal_XXXX.npy     base works per (year 2000..2017, vfield) for the balance check
Merge (--merge): per bucket, aggregate over files -> passM/merged/bucket_XX.npz with keys and S[key, year 2000..2017]
for keys whose max count in 2003..2017 is >= 3 (the k_t floor).

Usage: python passM.py [--files i,j] [--limit N] [--workers W] [--mod 5 --rem 0] [--merge]"""
from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc

from common import LOGS, ROOT, setup_logger, source_field_lut, works_files

Y0, Y1 = 2000, 2017
NY = Y1 - Y0 + 1
PARTS = ROOT / "passM" / "parts"
MERGED = ROOT / "passM" / "merged"
COLS = ["id", "title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id"]
NBUCKET = 16
_W: dict = {}


def _init() -> None:
    sid, code = source_field_lut()
    _W.update(sid=sid, code=code)
    pa.set_cpu_count(1)


def bucket_of(h: np.ndarray) -> np.ndarray:
    return (h >> np.uint64(59)).astype(np.int64)


def process_file(fi: int, key: str, size: int) -> dict:
    from common5 import surf_arrow
    from nrules import ngram_table
    from rangefile import read_columns
    t_start = time.time()
    tb = read_columns(key, size, COLS, n_threads=8)
    t_io = time.time() - t_start
    year = pc.fill_null(tb.column("publication_year"), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    base = pc.fill_null(pc.is_in(tb.column("type"), value_set=pa.array(["article", "review"])), False).to_numpy(
        zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_paratext"), False).to_numpy(zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_xpac"), False).to_numpy(zero_copy_only=False)
    base &= (year >= Y0) & (year <= Y1)
    pl = tb.column("primary_location").combine_chunks()
    src = pl.field("source").field("id")
    sidn = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(src, "https://openalex.org/S0"), 22), pa.int64()).to_numpy(
        zero_copy_only=False)
    pos = np.clip(np.searchsorted(_W["sid"], sidn), 0, len(_W["sid"]) - 1)
    vfield = np.where(_W["sid"][pos] == sidn, _W["code"][pos], 0).astype(np.int64)
    bal = np.bincount((year[base] - Y0) * 27 + vfield[base], minlength=NY * 27).reshape(NY, 27)
    valid_t = pc.is_valid(tb.column("title")).to_numpy(zero_copy_only=False)
    bidx = np.nonzero(base & valid_t)[0]
    tsub = tb.column("title").take(pa.array(bidx))
    st = pc.utf8_trim_whitespace(surf_arrow(tsub))
    ng = ngram_table(st)
    yr = year[bidx]
    df = pd.DataFrame({"row": ng["row"], "h": ng["h"], "n": ng["n"]}).drop_duplicates(["row", "h"])
    df["year"] = yr[df.row.to_numpy()].astype(np.int16)
    agg = df.groupby(["h", "year", "n"], sort=False).size().rename("c").reset_index()
    b = bucket_of(agg.h.to_numpy(np.uint64))
    o = np.argsort(b, kind="stable")
    agg = agg.iloc[o]
    boff = np.searchsorted(b[o], np.arange(NBUCKET + 1))
    np.savez(PARTS / f"ng_{fi:04d}.npz", h=agg.h.to_numpy(np.uint64), year=agg.year.to_numpy(np.int16),
             n=agg.n.to_numpy(np.int8), c=agg.c.to_numpy(np.int32), boff=boff)
    wid = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(tb.column("id").take(pa.array(bidx)), "https://openalex.org/W0"),
                                          22), pa.int64()).to_numpy(zero_copy_only=False)
    pd.DataFrame({"work_id": wid, "year": yr.astype(np.int16), "vfield": vfield[bidx].astype(np.int8),
                  "source": sidn[bidx].astype(np.int64),
                  "title": pc.utf8_slice_codeunits(tsub, 0, 300).to_pylist()}).to_parquet(
        PARTS / f"titles_{fi:04d}.parquet", index=False, compression="zstd")
    np.save(PARTS / f"bal_{fi:04d}.npy", bal)
    out = {"fi": fi, "n": tb.num_rows, "n_base": int(base.sum()), "n_titles": int(len(bidx)),
           "n_ngram_rows": int(len(agg)), "t_io": t_io, "t_all": time.time() - t_start}
    (PARTS / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb, df, agg, ng
    gc.collect()
    return out


def merge_bucket(bk: int, fis: list[int]) -> dict:
    hs, ys, ns, cs = [], [], [], []
    for fi in fis:
        z = np.load(PARTS / f"ng_{fi:04d}.npz")
        a, b = z["boff"][bk], z["boff"][bk + 1]
        hs.append(z["h"][a:b]); ys.append(z["year"][a:b]); ns.append(z["n"][a:b]); cs.append(z["c"][a:b])
    h = np.concatenate(hs); y = np.concatenate(ys).astype(np.int64); n = np.concatenate(ns); c = np.concatenate(cs)
    del hs, ys, ns, cs
    keys, inv = np.unique(h, return_inverse=True)
    S = np.zeros((len(keys), NY), np.int32)
    np.add.at(S, (inv, y - Y0), c)
    nlen = np.zeros(len(keys), np.int8)
    nlen[inv] = n
    keep = S[:, 3:].max(1) >= 3
    np.savez(MERGED / f"bucket_{bk:02d}.npz", keys=keys[keep], S=S[keep], nlen=nlen[keep])
    return {"bucket": bk, "keys_all": int(len(keys)), "keys_kept": int(keep.sum())}


def merge(logger, workers: int) -> None:
    MERGED.mkdir(parents=True, exist_ok=True)
    fis = sorted(int(p.stem.split("_")[1]) for p in PARTS.glob("done_*.json"))
    logger.info(f"merging {len(fis)} Pass M parts into {NBUCKET} buckets")
    bal = sum(np.load(PARTS / f"bal_{fi:04d}.npy").astype(np.int64) for fi in fis)
    np.save(ROOT / "passM" / "sample_bal.npy", bal)
    res = []
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        for r in ex.map(merge_bucket, range(NBUCKET), [fis] * NBUCKET):
            logger.info(f"bucket {r}")
            res.append(r)
    meta = [json.loads((PARTS / f"done_{fi:04d}.json").read_text()) for fi in fis]
    info = {"files": fis, "n_files": len(fis), "n_base": int(sum(m["n_base"] for m in meta)),
            "n_titles": int(sum(m["n_titles"] for m in meta)),
            "keys_all": int(sum(r["keys_all"] for r in res)), "keys_kept_max_ge3": int(sum(r["keys_kept"] for r in res))}
    (ROOT / "passM" / "passM_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"Pass M merged: { {k: v for k, v in info.items() if k != 'files'} }")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--mod", type=int, default=5)
    ap.add_argument("--rem", type=str, default="0")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    PARTS.mkdir(parents=True, exist_ok=True)
    logger = setup_logger("passM")
    if args.merge:
        merge(logger, args.workers)
        return
    rems = {int(x) for x in args.rem.split(",")}
    files = [f for f in works_files() if f[0] % args.mod in rems]
    done = {int(p.stem.split("_")[1]) for p in PARTS.glob("done_*.json")}
    if args.files:
        want = {int(x) for x in args.files.split(",")}
        todo = [f for f in files if f[0] in want and f[0] not in done]
    else:
        todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"Pass M: sample files {len(files)} done={len(done)} todo={len(todo)} workers={args.workers}")
    t0 = time.time()
    tot_bytes = sum(f[2] for f in todo)
    sizes = {f[0]: f[2] for f in todo}
    done_bytes, n_new, failures = 0, 0, []
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        pending = set()
        it = iter(todo)

        def submit_next() -> None:
            try:
                fi, key, size, _ = next(it)
            except StopIteration:
                return
            fut = ex.submit(process_file, fi, key, size)
            fut.fi = fi
            pending.add(fut)
        for _ in range(args.workers + 1):
            submit_next()
        while pending:
            fin, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in fin:
                pending.discard(fut)
                try:
                    r = fut.result()
                except Exception as e:  # noqa: BLE001 -- failed files are retried on resume
                    logger.error(f"file {fut.fi} failed: {e!r}"[:600])
                    failures.append(fut.fi)
                    submit_next()
                    continue
                n_new += 1
                done_bytes += sizes[r["fi"]]
                el = time.time() - t0
                if n_new % 10 == 0 or n_new == len(todo) or n_new <= 5:
                    eta = el / max(done_bytes, 1) * (tot_bytes - done_bytes) / 60
                    logger.info(f"{n_new}/{len(todo)} files {el/60:.1f} min eta~{eta:.1f} min | fi={r['fi']} "
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s titles={r['n_titles']} "
                                f"ngr={r['n_ngram_rows']}")
                submit_next()
    logger.info(f"Pass M finished in {(time.time()-t0)/60:.1f} min; failures={failures}")
    (LOGS / "passM_failures.json").write_text(json.dumps(failures))


if __name__ == "__main__":
    main()
