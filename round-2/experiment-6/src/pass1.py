#!/usr/bin/env python3
"""Pass 1 (zero credits): stream the full OpenAlex works snapshot (2,040 parquet files) over HTTP range reads and,
per file, write scan/pass1/f{idx:04d}.npz with
  * hit records for every lexicon title match: row, cidx, year, venue field vf, primary-topic field pf,
    tag (1 = concept tag with score >= 0.3, 0 = tagged work but not with c, -1 = work has no concept tags),
    tag score, variant flag, base flag;
  * tag-only counter: (cidx, year, vf) counts of base works tagged c (score >= 0.3) without a title hit;
  * base totals G[y] and venue-field totals GF[y, f];
  * per-row vf (int8) and year (int16) for ALL rows (the global id -> field map is completed in pass 2).
Resumable: a file whose npz exists is skipped.  Usage: python pass1.py [--limit N] [--workers W] [--sample FRAC]"""
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
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import INP, LOGS, NY, P1, RES, SEED, TAG_SCORE, Y0, Y1  # noqa: E402

COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
        "primary_topic.field.id", "concepts.list.element.id", "concepts.list.element.score"]
_W: dict = {}


def _init_worker() -> None:
    import pandas as pd
    from matcher import build_automaton
    lex = pd.read_parquet(RES / "lexicon.parquet")
    forms = {int(i): [f] for i, f in zip(lex.concept_idx, lex.form)}
    _W["A"] = build_automaton(forms)
    _W["lex_ids"] = lex.oa_int.to_numpy(np.int64)  # sorted, index == concept_idx
    sf = pd.read_parquet(INP / "source_field.parquet")
    sf = sf.sort_values("source")
    _W["src_ids"] = sf.source.to_numpy(np.int64)
    _W["src_f"] = sf.field.fillna(-1).astype("int64").to_numpy().astype(np.int8)
    _W["NC"] = len(lex)
    pa.set_cpu_count(1)


def _int_ids(arr: pa.Array, prefix_len: int) -> np.ndarray:
    """'https://openalex.org/S123' -> 123 ; null -> -1."""
    a = pc.utf8_slice_codeunits(arr, prefix_len)
    a = pc.if_else(pc.equal(pc.utf8_length(pc.fill_null(a, "")), 0), None, a)
    return pc.fill_null(pc.cast(a, pa.int64()), -1).to_numpy(zero_copy_only=False)


def process_file(fi: int, key: str, size: int) -> dict:
    from matcher import match, norm_arrow
    from rangefile import read_columns
    t_start = time.time()
    tb = read_columns(key, size, COLS, n_threads=10)
    t_io = time.time() - t_start
    n = tb.num_rows
    year = pc.fill_null(tb.column("publication_year"), -1).to_numpy(zero_copy_only=False).astype(np.int64)
    typ = tb.column("type")
    btype = pc.fill_null(pc.is_in(typ, value_set=pa.array(["article", "review"])), False).to_numpy(zero_copy_only=False)
    para = pc.fill_null(tb.column("is_paratext"), False).to_numpy(zero_copy_only=False)
    xpac = pc.fill_null(tb.column("is_xpac"), False).to_numpy(zero_copy_only=False)
    inyr = (year >= Y0) & (year <= Y1)
    base = btype & ~para & ~xpac & inyr
    # venue field
    sid = _int_ids(pc.struct_field(pc.struct_field(tb.column("primary_location"), [0]), [0]).combine_chunks(), 22)
    pos = np.clip(np.searchsorted(_W["src_ids"], sid), 0, len(_W["src_ids"]) - 1)
    vf = np.where((sid >= 0) & (_W["src_ids"][pos] == sid), _W["src_f"][pos], -1).astype(np.int8)
    pfa = pc.struct_field(pc.struct_field(tb.column("primary_topic"), [0]), [0]).combine_chunks()
    pf = _int_ids(pfa, 28)  # https://openalex.org/fields/17
    pf = np.where((pf >= 11) & (pf <= 36), pf, -1).astype(np.int8)
    yb = year[base] - Y0
    G = np.bincount(yb, minlength=NY)
    vb = vf[base].astype(np.int64)
    okf = vb >= 11
    GF = np.bincount(yb[okf] * 26 + (vb[okf] - 11), minlength=NY * 26).reshape(NY, 26)
    # concepts
    cl = tb.column("concepts").combine_chunks()
    lens = pc.fill_null(pc.list_value_length(cl), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    flat = pc.list_flatten(cl)
    cid = _int_ids(pc.struct_field(flat, [0]), 22)
    csc = pc.fill_null(pc.struct_field(flat, [1]), 0).to_numpy(zero_copy_only=False).astype(np.float32)
    crow = np.repeat(np.arange(n, dtype=np.int64), lens)
    lp = np.clip(np.searchsorted(_W["lex_ids"], cid), 0, len(_W["lex_ids"]) - 1)
    inlex = (_W["lex_ids"][lp] == cid) & base[crow]
    NC = _W["NC"]
    tag_keys = crow[inlex] * NC + lp[inlex]
    tag_sc = csc[inlex]
    o = np.argsort(tag_keys, kind="stable")
    tag_keys, tag_sc = tag_keys[o], tag_sc[o]
    # titles (base rows only)
    brow = np.nonzero(base)[0]
    titles = norm_arrow(tb.column("title").take(pa.array(brow)).combine_chunks()).to_pylist()
    del tb, cl, flat
    A = _W["A"]
    hr, hc, hv = [], [], []
    for r, t in zip(brow.tolist(), titles):
        if len(t) < 4:
            continue
        m = match(A, t)
        for c, v in m.items():
            hr.append(r); hc.append(c); hv.append(v)
    del titles
    hr = np.asarray(hr, np.int64); hc = np.asarray(hc, np.int64); hv = np.asarray(hv, np.int8)
    hk = hr * NC + hc
    p = np.clip(np.searchsorted(tag_keys, hk), 0, max(len(tag_keys) - 1, 0))
    has = (len(tag_keys) > 0) & (tag_keys[p] == hk) if len(tag_keys) else np.zeros(len(hk), bool)
    hscore = np.where(has, tag_sc[p] if len(tag_keys) else 0, 0).astype(np.float16)
    tag = np.where(lens[hr] == 0, -1, np.where(has & (hscore >= TAG_SCORE), 1, 0)).astype(np.int8)
    # tag-only counter (tagged >= 0.3, no title hit)
    hk_sorted = np.sort(hk)
    strong = tag_sc >= TAG_SCORE
    tk = tag_keys[strong]
    q = np.clip(np.searchsorted(hk_sorted, tk), 0, max(len(hk_sorted) - 1, 0))
    nohit = ~((len(hk_sorted) > 0) & (hk_sorted[q] == tk)) if len(hk_sorted) else np.ones(len(tk), bool)
    tk = tk[nohit]
    trow, tcon = tk // NC, tk % NC
    tokey = tcon * 10000 + (year[trow] - Y0) * 100 + (vf[trow].astype(np.int64) + 1)
    tu, tcnt = np.unique(tokey, return_counts=True)
    out = dict(row=hr.astype(np.int32), cidx=hc.astype(np.int32), year=year[hr].astype(np.int16), vf=vf[hr], pf=pf[hr],
               tag=tag, score=hscore, variant=hv, to_key=tu.astype(np.int64), to_cnt=tcnt.astype(np.int32),
               G=G.astype(np.int64), GF=GF.astype(np.int64), vf_all=vf, year_all=np.clip(year, -1, 32000).astype(np.int16),
               base_all=base, n=np.array(n))
    tmp = P1 / f"f{fi:04d}.tmp.npz"
    np.savez_compressed(tmp, **out)
    tmp.replace(P1 / f"f{fi:04d}.npz")
    gc.collect()
    return {"fi": fi, "n": n, "nhit": len(hr), "t_io": t_io, "t_all": time.time() - t_start}


def file_list() -> list[tuple[int, str, int]]:
    man = json.loads((INP / "works_manifest.json").read_text())
    return [(i, f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"]) for i, f in enumerate(man["files"])]


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--order", default="size", choices=["size", "random"])
    args = ap.parse_args()
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "pass1.log", rotation="30 MB", level="DEBUG")
    resource.setrlimit(resource.RLIMIT_AS, (28 * 1024**3, 28 * 1024**3))
    P1.mkdir(parents=True, exist_ok=True)
    files = file_list()
    todo = [f for f in files if not (P1 / f"f{f[0]:04d}.npz").exists()]
    if args.order == "random":
        rng = np.random.default_rng(SEED)
        todo = [todo[i] for i in rng.permutation(len(todo))]
    else:
        todo.sort(key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    tot_bytes = sum(f[2] for f in todo)
    logger.info(f"files total={len(files)} todo={len(todo)} ({tot_bytes/1e9:.1f} GB) workers={args.workers}")
    t0 = time.time(); done_b = 0; nd = 0; fails = []
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"), initializer=_init_worker) as ex:
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
                    r = fut.result()
                    done_b += f[2]; nd += 1
                    el = time.time() - t0
                    if nd % 10 == 0 or nd == len(todo) or nd <= 3:
                        logger.info(f"{nd}/{len(todo)} {el/60:.1f} min, eta {(tot_bytes-done_b)*el/max(done_b,1)/60:.1f} min | "
                                    f"file {r['fi']} rows={r['n']} hits={r['nhit']} io={r['t_io']:.1f}s all={r['t_all']:.1f}s")
                except Exception as e:  # noqa: BLE001 -- keep scanning; failures are retried on the next run
                    logger.error(f"file {f[0]} failed: {e!r}"[:500]); fails.append(f[0])
                submit()
    logger.info(f"pass1 finished in {(time.time()-t0)/60:.1f} min; failures={fails}")


if __name__ == "__main__":
    main()
