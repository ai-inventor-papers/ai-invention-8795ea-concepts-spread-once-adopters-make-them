#!/usr/bin/env python3
"""Pass 2 (zero credits): for every works file, read id, title, referenced_works and authorships.author.id and
  * keep the rows that pass 1 matched to a CANDIDATE frame concept (scan/cand_concepts.json): work id, year, venue
    field, primary-topic field, title, referenced work ids, author ids -> scan/pass2/w{idx}.parquet, plus the
    per-(work, concept) hit rows -> scan/pass2/h{idx}.parquet;
  * write the global id -> (venue field, year) map for every work with a venue field (1990-2022) ->
    scan/pass2/m{idx}.npz (used to classify the fields of background references).
Resumable per file.  Usage: python pass2.py [--limit N] [--workers W] [--idmap-only]"""
from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import resource
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from pathlib import Path

import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import LOGS, P1, P2, SCAN, SEED  # noqa: E402
from pass1 import file_list  # noqa: E402

COLS = ["id", "title", "referenced_works.list.element", "authorships.list.element.author.id"]
_W: dict = {}


def _init_worker(cand: list[int], idmap_only: bool) -> None:
    _W["cand"] = np.asarray(sorted(cand), np.int32)
    _W["idmap_only"] = idmap_only
    pa.set_cpu_count(1)


def _ids(arr, plen: int = 22) -> np.ndarray:
    a = pc.utf8_slice_codeunits(pc.fill_null(arr, "https://openalex.org/W0"), plen)
    return pc.cast(a, pa.int64()).to_numpy(zero_copy_only=False)


def _list_ids(listarr: pa.ListArray, plen: int = 22) -> pa.ListArray:
    listarr = listarr.combine_chunks() if hasattr(listarr, "combine_chunks") else listarr
    flat = pc.list_flatten(listarr)
    if pa.types.is_struct(flat.type):
        flat = pc.struct_field(pc.struct_field(flat, [0]), [0])
    vals = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(flat, "https://openalex.org/A0"), plen), pa.int64())
    lens = pc.fill_null(pc.list_value_length(listarr), 0).to_numpy(zero_copy_only=False)
    offs = np.zeros(len(lens) + 1, np.int32); offs[1:] = np.cumsum(lens)
    return pa.ListArray.from_arrays(pa.array(offs), vals)


def process_file(fi: int, key: str, size: int) -> dict:
    from rangefile import read_columns
    t = time.time()
    z = np.load(P1 / f"f{fi:04d}.npz")
    vf_all, yr_all = z["vf_all"], z["year_all"]
    cols = ["id"] if _W["idmap_only"] else COLS
    tb = read_columns(key, size, cols, n_threads=10)
    t_io = time.time() - t
    wid = _ids(tb.column("id").combine_chunks())
    m = (vf_all >= 11) & (yr_all >= 1990) & (yr_all <= 2022)
    o = np.argsort(wid[m])
    np.savez(P2 / f"m{fi:04d}.npz", id=wid[m][o], vf=vf_all[m][o], year=yr_all[m][o])
    nk = 0
    if not _W["idmap_only"]:
        keep = np.isin(z["cidx"], _W["cand"])
        rows = z["row"][keep]
        if len(rows):
            ur = np.unique(rows)
            take = pa.array(ur)
            sub = tb.take(take)
            works = pa.table({"work_id": pa.array(wid[ur]), "file": pa.array(np.full(len(ur), fi, np.int16)),
                              "row": pa.array(ur.astype(np.int32)), "year": pa.array(yr_all[ur]), "vf": pa.array(vf_all[ur]),
                              "title": sub.column("title").combine_chunks(),
                              "refs": _list_ids(sub.column("referenced_works").combine_chunks()),
                              "authors": _list_ids(sub.column("authorships").combine_chunks(), 22)})
            pq.write_table(works, P2 / f"w{fi:04d}.parquet")
            hits = pa.table({"work_id": pa.array(wid[rows]), "cidx": pa.array(z["cidx"][keep]), "tag": pa.array(z["tag"][keep]),
                             "score": pa.array(z["score"][keep].astype(np.float32)), "variant": pa.array(z["variant"][keep]),
                             "year": pa.array(z["year"][keep]), "vf": pa.array(z["vf"][keep]), "pf": pa.array(z["pf"][keep])})
            pq.write_table(hits, P2 / f"h{fi:04d}.parquet")
            nk = len(ur)
        (P2 / f"done{fi:04d}").write_text("1")
    del tb
    gc.collect()
    return {"fi": fi, "kept": nk, "t_io": t_io, "t_all": time.time() - t}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--idmap-only", action="store_true")
    args = ap.parse_args()
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "pass2.log", rotation="30 MB", level="DEBUG")
    resource.setrlimit(resource.RLIMIT_AS, (28 * 1024**3, 28 * 1024**3))
    P2.mkdir(parents=True, exist_ok=True)
    cand = [] if args.idmap_only else json.loads((SCAN / "cand_concepts.json").read_text())["cidx"]
    files = file_list()
    marker = (lambda i: P2 / f"m{i:04d}.npz") if args.idmap_only else (lambda i: P2 / f"done{i:04d}")
    todo = [f for f in files if not marker(f[0]).exists()]
    rng = np.random.default_rng(SEED)
    todo = [todo[i] for i in rng.permutation(len(todo))]  # random order: any prefix is a random file sample
    if args.limit:
        todo = todo[:args.limit]
    tot = sum(f[2] for f in todo)
    logger.info(f"candidates={len(cand)} todo={len(todo)} files ({tot/1e9:.1f} GB)")
    t0 = time.time(); db = 0; nd = 0; fails = []
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"), initializer=_init_worker,
                             initargs=(cand, args.idmap_only)) as ex:
        it = iter(todo); pending = {}

        def submit() -> None:
            try:
                f = next(it)
            except StopIteration:
                return
            pending[ex.submit(process_file, *f)] = f
        for _ in range(args.workers + 2):
            submit()
        while pending:
            fin, _ = wait(list(pending), return_when=FIRST_COMPLETED)
            for fut in fin:
                f = pending.pop(fut)
                try:
                    r = fut.result(); db += f[2]; nd += 1
                    if nd % 20 == 0 or nd <= 3 or nd == len(todo):
                        el = time.time() - t0
                        logger.info(f"{nd}/{len(todo)} {el/60:.1f} min eta {(tot-db)*el/max(db,1)/60:.1f} min | "
                                    f"file {r['fi']} kept={r['kept']} io={r['t_io']:.1f}s all={r['t_all']:.1f}s")
                except Exception as e:  # noqa: BLE001 -- retried on next run
                    logger.error(f"file {f[0]} failed: {e!r}"[:500]); fails.append(f[0])
                submit()
    logger.info(f"pass2 finished {(time.time()-t0)/60:.1f} min failures={fails}")


if __name__ == "__main__":
    main()
