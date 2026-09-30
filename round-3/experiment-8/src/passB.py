#!/usr/bin/env python3
"""PASS B: citations received by the frame's early works (outcome O4) and by the reference sample.

targets = work ids of grounded frame hits in t0..t0+2 (data/frame_matches_early) UNION data/ref_sample.parquet ids.
Per file: citing works = base works (article|review, not paratext, not xpac) with publication year 2003..2022;
referenced_works flattened -> int64; kept if the id is a target; counted by (target index, citing year).
Output: data/cites_early.parquet (work_id, citing_year, n).  Usage: python passB.py [--files ..] [--merge]"""
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

from common import DATA, PASSB, add_deviation, load_frame, read_parquet_parts, setup_logger, works_files

COLS = ["publication_year", "type", "is_paratext", "is_xpac", "referenced_works.list.element"]
CY0, CY1 = 2003, 2022
NCY = CY1 - CY0 + 1
TARGETS = DATA / "passB_targets.npy"
_W: dict = {}


def build_targets(logger) -> np.ndarray:
    fr = load_frame()[["ci", "t0"]]
    e = read_parquet_parts(DATA / "frame_matches_early", columns=["ci", "year", "work_id"]).merge(fr, on="ci")
    e = e[(e.year >= e.t0) & (e.year <= e.t0 + 2)]
    rs = pd.read_parquet(DATA / "ref_sample.parquet", columns=["work_id"])
    t = np.unique(np.concatenate([e.work_id.to_numpy(np.int64), rs.work_id.to_numpy(np.int64)]))
    np.save(TARGETS, t)
    logger.info(f"targets: {len(t):,} ids ({e.work_id.nunique():,} early works, {len(rs):,} ref-sample works)")
    return t


def _init() -> None:
    _W["t"] = np.load(TARGETS)
    pa.set_cpu_count(1)


def process_file(fi: int, key: str, size: int) -> dict:
    from rangefile import read_columns
    t_start = time.time()
    tb = read_columns(key, size, COLS, n_threads=8)
    t_io = time.time() - t_start
    year = pc.fill_null(tb.column("publication_year"), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    base = pc.fill_null(pc.is_in(tb.column("type"), value_set=pa.array(["article", "review"])), False).to_numpy(
        zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_paratext"), False).to_numpy(zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_xpac"), False).to_numpy(zero_copy_only=False)
    base &= (year >= CY0) & (year <= CY1)
    rw = tb.column("referenced_works").combine_chunks()
    ln = pc.fill_null(pc.list_value_length(rw), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    rows = np.repeat(np.arange(len(ln)), ln)
    flat = pc.list_flatten(rw)
    keep = base[rows]
    n_links = int(keep.sum())
    out = {"fi": fi, "n_base_citing": int(base.sum()), "n_links": n_links, "t_io": t_io}
    if n_links:
        ids = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(flat.filter(pa.array(keep)), "https://openalex.org/W0"),
                                              22), pa.int64()).to_numpy(zero_copy_only=False)
        cy = year[rows[keep]]
        t = _W["t"]
        p = np.clip(np.searchsorted(t, ids), 0, len(t) - 1)
        hit = t[p] == ids
        key_ = p[hit].astype(np.int64) * NCY + (cy[hit] - CY0)
        u, c = np.unique(key_, return_counts=True)
    else:
        u = np.zeros(0, np.int64); c = np.zeros(0, np.int64)
    np.savez_compressed(PASSB / f"cit_{fi:04d}.npz", u=u, c=c)
    out["n_hits"] = int(c.sum())
    out["t_all"] = time.time() - t_start
    (PASSB / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb, rw, flat
    gc.collect()
    return out


def merge(logger) -> None:
    t = np.load(TARGETS)
    done = sorted(PASSB.glob("done_*.json"))
    keys, cnts = [], []
    for p in done:
        fi = int(p.stem.split("_")[1])
        z = np.load(PASSB / f"cit_{fi:04d}.npz")
        keys.append(z["u"]); cnts.append(z["c"])
        if len(keys) >= 200:
            k = np.concatenate(keys); c = np.concatenate(cnts)
            u, inv = np.unique(k, return_inverse=True)
            keys, cnts = [u], [np.bincount(inv, weights=c).astype(np.int64)]
    k = np.concatenate(keys); c = np.concatenate(cnts)
    u, inv = np.unique(k, return_inverse=True)
    c = np.bincount(inv, weights=c).astype(np.int64)
    df = pd.DataFrame({"work_id": t[u // NCY], "citing_year": (u % NCY + CY0).astype(np.int16), "n": c.astype(np.int32)})
    df.to_parquet(DATA / "cites_early.parquet", index=False, compression="zstd")
    meta = [json.loads(p.read_text()) for p in done]
    info = {"files_done": len(done), "n_targets": int(len(t)), "links_scanned": int(sum(m["n_links"] for m in meta)),
            "hits": int(sum(m["n_hits"] for m in meta)), "rows": int(len(df)),
            "targets_cited": int(df.work_id.nunique())}
    (DATA / "passB_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"Pass B merged: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--targets", action="store_true")
    args = ap.parse_args()
    logger = setup_logger("passB")
    if args.targets or not TARGETS.exists():
        build_targets(logger)
    if args.merge:
        merge(logger)
        return
    files = works_files()
    done = {int(p.stem.split("_")[1]) for p in PASSB.glob("done_*.json")}
    if args.files:
        want = {int(x) for x in args.files.split(",")}
        todo = [f for f in files if f[0] in want and f[0] not in done]
    else:
        todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"files done={len(done)} todo={len(todo)}")
    t0 = time.time()
    sizes = {f[0]: f[2] for f in todo}
    tot_bytes = sum(sizes.values())
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
        for _ in range(args.workers + 2):
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
                if n_new % 20 == 0 or n_new == len(todo) or n_new <= 5:
                    eta = el / max(done_bytes, 1) * (tot_bytes - done_bytes) / 60
                    logger.info(f"{n_new}/{len(todo)} files {el/60:.1f} min eta~{eta:.1f} min | fi={r['fi']} "
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s links={r['n_links']} hits={r['n_hits']}")
                submit_next()
    logger.info(f"Pass B finished in {(time.time()-t0)/60:.1f} min; failures={failures}")
    if failures:
        add_deviation("passB_failures", f"files failed (retried on resume): {failures}")


if __name__ == "__main__":
    main()
