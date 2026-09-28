#!/usr/bin/env python3
"""STEP 3: the single zero-credit pass over all 2,040 OpenAlex works parquet files (HTTP range reads of 10 leaf
columns). Per file (written to scan/parts/, so the scan resumes file by file):

  A  G[year], VF[year, vfield 0..26] over base works (article|review, not paratext, not xpac, 1995-2022)
  B  CO[year, i, j]: base works whose topic-field SET contains fields i and j (diagonal = contains i), NT[year]
  C  verified title matches of lexicon_v1 -> sparse counts keyed (concept, year, vfield, ptfield, tagstate, mtype)
     tagstate: 1 legacy tag present with score >= 0.3; 2 work has tags but not this one; 3 work has no tags
  R  reservoir: per (concept, era) the 12 hits with the smallest hash(file, row), with title (scan/reservoir/part_*)
  U  untagged hits (tagstate 3): all rows as ints; titles for the 20% hash sample (h % 5 == 0)

Usage: python scan_full.py [--limit N] [--workers W] [--files i,j,k] [--merge]"""
from __future__ import annotations

import argparse
import gc
import json
import multiprocessing as mp
import time
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from common import (NY, RESERVOIR_DIR, ROOT, SCAN, Y0, Y1, setup_logger, source_field_lut, surf_arrow, works_files,
                    write_parquet_parts)

PARTS = SCAN / "parts"
PARTS.mkdir(parents=True, exist_ok=True)
COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
        "topics.list.element.field.id", "primary_topic.field.id", "concepts.list.element.id",
        "concepts.list.element.score"]
TAG_MIN = 0.3
RES_K = 12
ERAS = [(Y0, 2002), (2003, 2014), (2015, Y1)]


def mix64(x: np.ndarray) -> np.ndarray:
    """splitmix64 finaliser: deterministic pseudo-random hash of (file, row)."""
    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)


_W: dict = {}


def _init() -> None:
    from matcher import build_automaton
    lex = pd.read_parquet(ROOT / "lexicon_v1.parquet", columns=["concept_id", "forms", "mtypes"])
    entries = [(f, ci, m) for ci, (fs, ms) in enumerate(zip(lex.forms, lex.mtypes)) for f, m in zip(fs, ms)]
    A, specs = build_automaton(entries)
    sid, code = source_field_lut()
    _W.update(A=A, specs=specs, cid=lex.concept_id.to_numpy(np.int64), sid=sid, code=code)
    pa.set_cpu_count(1)


def _field_code(arr) -> np.ndarray:
    """'https://openalex.org/fields/17' -> 7 (fid - 10); null -> 0."""
    s = pc.utf8_slice_codeunits(pc.fill_null(arr, "https://openalex.org/fields/10"), 28)
    v = pc.cast(s, pa.int64()).to_numpy(zero_copy_only=False) - 10
    return np.clip(v, 0, 26).astype(np.int64)


def process_file(fi: int, key: str, size: int) -> dict:
    from matcher import match
    from rangefile import read_columns
    t_start = time.time()
    tb = read_columns(key, size, COLS, n_threads=8)
    t_io = time.time() - t_start
    n = tb.num_rows
    year = pc.fill_null(tb.column("publication_year"), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    base = pc.fill_null(pc.is_in(tb.column("type"), value_set=pa.array(["article", "review"])), False).to_numpy(
        zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_paratext"), False).to_numpy(zero_copy_only=False)
    base &= ~pc.fill_null(tb.column("is_xpac"), False).to_numpy(zero_copy_only=False)
    base &= (year >= Y0) & (year <= Y1)
    yi = np.clip(year - Y0, 0, NY - 1)
    # venue field
    src = pc.struct_field(pc.struct_field(tb.column("primary_location"), [0]), [0])
    sidn = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(src, "https://openalex.org/S0"), 22), pa.int64()).to_numpy(
        zero_copy_only=False)
    pos = np.searchsorted(_W["sid"], sidn)
    pos = np.clip(pos, 0, len(_W["sid"]) - 1)
    vfield = np.where(_W["sid"][pos] == sidn, _W["code"][pos], 0).astype(np.int64)
    ptfield = _field_code(pc.struct_field(tb.column("primary_topic"), [0]).combine_chunks().field(0)
                          if False else pc.struct_field(pc.struct_field(tb.column("primary_topic"), [0]), [0]))
    # A
    G = np.bincount(yi[base], minlength=NY)
    VF = np.bincount(yi[base] * 27 + vfield[base], minlength=NY * 27).reshape(NY, 27)
    # B: topic-field sets
    tl = tb.column("topics").combine_chunks()
    tlen = pc.fill_null(pc.list_value_length(tl), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    tf = _field_code(pc.struct_field(pc.struct_field(pc.list_flatten(tl), [0]), [0]))
    bits = np.where(tf > 0, np.left_shift(np.int64(1), np.maximum(tf - 1, 0)), 0).astype(np.int64)
    row_of = np.repeat(np.arange(n), tlen)
    mask = np.zeros(n, np.int64)
    np.bitwise_or.at(mask, row_of, bits)
    okb = base & (mask > 0)
    NT = np.bincount(yi[okb], minlength=NY)
    u, c = np.unique(yi[okb] * (1 << 26) + mask[okb], return_counts=True)
    CO = np.zeros((NY, 26, 26), np.int64)
    for key_, cnt in zip(u.tolist(), c.tolist()):
        y, m = divmod(key_, 1 << 26)
        fs = [k for k in range(26) if m >> k & 1]
        for a in range(len(fs)):
            for b in range(a, len(fs)):
                CO[y, fs[a], fs[b]] += cnt
    # C: title matching on base rows
    bidx = np.nonzero(base & pc.is_valid(tb.column("title")).to_numpy(zero_copy_only=False))[0]
    tsub = tb.column("title").take(pa.array(bidx))
    stitles = surf_arrow(tsub).to_pylist()
    titles = tsub.to_pylist()
    A, specs = _W["A"], _W["specs"]
    h_row, h_ci, h_mt = [], [], []
    for k, (st, t) in enumerate(zip(stitles, titles)):
        for ci, mt in match(st, t, A, specs).items():
            h_row.append(bidx[k])
            h_ci.append(ci)
            h_mt.append(mt)
    del stitles
    h_row = np.asarray(h_row, np.int64)
    h_ci = np.asarray(h_ci, np.int64)
    h_mt = np.asarray(h_mt, np.int64)
    # tagstate
    cl = tb.column("concepts").combine_chunks()
    clen = pc.fill_null(pc.list_value_length(cl), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    coff = np.zeros(n + 1, np.int64)
    coff[1:] = np.cumsum(clen)
    tagstate = np.full(len(h_row), 3, np.int64)
    if len(h_row):
        flat = pc.list_flatten(cl)
        cids = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(pc.struct_field(flat, [0]), "https://openalex.org/C0"), 22),
                       pa.int64()).to_numpy(zero_copy_only=False)
        csc = pc.fill_null(pc.struct_field(flat, [1]), 0.0).to_numpy(zero_copy_only=False)
        want = _W["cid"][h_ci]
        for k in range(len(h_row)):
            r = h_row[k]
            a, b = coff[r], coff[r + 1]
            if b == a:
                continue
            seg = cids[a:b]
            w = np.nonzero(seg == want[k])[0]
            tagstate[k] = 1 if (len(w) and csc[a + w[0]] >= TAG_MIN) else 2
    hy = yi[h_row]
    hv = vfield[h_row]
    hp = ptfield[h_row]
    keyC = ((((h_ci * 32 + hy) * 32 + hv) * 32 + hp) * 4 + tagstate) * 4 + h_mt
    uC, cC = np.unique(keyC, return_counts=True)
    hsh = mix64(np.int64(fi) * (1 << 32) + h_row)
    era = np.digitize(year[h_row], [2003, 2015])
    rows = pd.DataFrame({"ci": h_ci, "era": era, "h": hsh.astype(np.int64), "year": year[h_row], "vfield": hv,
                         "ptfield": hp, "tagstate": tagstate, "mt": h_mt, "file": fi, "row": h_row})
    resv = rows.sort_values(["ci", "era", "h"]).groupby(["ci", "era"], sort=False).head(RES_K)
    unt = rows[rows.tagstate == 3].drop(columns=["era", "file", "row"])
    local = {int(r): t for r, t in zip(bidx, titles)} if len(h_row) else {}
    resv = resv.assign(title=[local[int(r)][:300] for r in resv.row])
    samp = rows[(rows.tagstate == 3) & (rows.h % 5 == 0)]
    samp = samp.assign(title=[local[int(r)][:300] for r in samp.row])
    out = {"fi": fi, "n": n, "n_base": int(base.sum()), "n_hits": int(len(h_row)), "t_io": t_io}
    np.savez_compressed(PARTS / f"agg_{fi:04d}.npz", G=G, VF=VF, NT=NT, CO=CO, uC=uC, cC=cC)
    resv.to_parquet(PARTS / f"resv_{fi:04d}.parquet", index=False)
    unt.to_parquet(PARTS / f"unt_{fi:04d}.parquet", index=False)
    samp.to_parquet(PARTS / f"untsamp_{fi:04d}.parquet", index=False)
    (PARTS / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb, titles, local, rows
    gc.collect()
    out["t_all"] = time.time() - t_start
    return out


RESV_RUN = SCAN / "reservoir_running.parquet"


def reduce_reservoir() -> int:
    """Fold every per-file reservoir part into the running reservoir (12 smallest hashes per concept x era) and
    delete the folded parts, so disk use stays bounded. Atomic: the running file is replaced, then parts removed."""
    parts = [q for q in sorted(PARTS.glob("resv_*.parquet"))
             if (PARTS / f"done_{q.stem.split('_')[1]}.json").exists()]  # only parts whose file finished writing
    if not parts:
        return 0
    dfs = [pd.read_parquet(RESV_RUN)] if RESV_RUN.exists() else []
    dfs += [pd.read_parquet(p) for p in parts]
    rs = pd.concat(dfs, ignore_index=True).sort_values(["ci", "era", "h"]).groupby(["ci", "era"], sort=False).head(RES_K)
    tmp = SCAN / "reservoir_running.tmp.parquet"
    rs.to_parquet(tmp, index=False)
    tmp.replace(RESV_RUN)
    for p in parts:
        p.unlink()
    return len(parts)


def merge(logger) -> None:
    """Reduce per-file parts into scan/agg_counts.parquet, reservoir/part_*.parquet, untagged_*.parquet, *.npz."""
    done = sorted(PARTS.glob("done_*.json"))
    fis = [int(p.stem.split("_")[1]) for p in done]
    logger.info(f"merging {len(fis)} parts")
    G = np.zeros(NY, np.int64); VF = np.zeros((NY, 27), np.int64); NT = np.zeros(NY, np.int64)
    CO = np.zeros((NY, 26, 26), np.int64)
    keys, cnts = [], []
    for i, fi in enumerate(fis):
        z = np.load(PARTS / f"agg_{fi:04d}.npz")
        G += z["G"]; VF += z["VF"]; NT += z["NT"]; CO += z["CO"]
        keys.append(z["uC"]); cnts.append(z["cC"])
        if len(keys) >= 200:
            k = np.concatenate(keys); c = np.concatenate(cnts)
            u, inv = np.unique(k, return_inverse=True)
            keys, cnts = [u], [np.bincount(inv, weights=c).astype(np.int64)]
    k = np.concatenate(keys) if keys else np.zeros(0, np.int64)
    c = np.concatenate(cnts) if cnts else np.zeros(0, np.int64)
    u, inv = np.unique(k, return_inverse=True)
    c = np.bincount(inv, weights=c).astype(np.int64)
    mt = u % 4; r = u // 4; ts = r % 4; r //= 4; pt = r % 32; r //= 32; vf = r % 32; r //= 32; yy = r % 32; ci = r // 32
    pd.DataFrame({"ci": ci.astype(np.int32), "year": (yy + Y0).astype(np.int16), "vfield": vf.astype(np.int8),
                  "ptfield": pt.astype(np.int8), "tagstate": ts.astype(np.int8), "mt": mt.astype(np.int8),
                  "n": c}).to_parquet(SCAN / "agg_counts.parquet", index=False)
    np.savez(SCAN / "year_field_totals.npz", G=G, VF=VF, NT=NT, years=np.arange(Y0, Y1 + 1))
    np.savez(SCAN / "co_by_year.npz", CO=CO, NT=NT, years=np.arange(Y0, Y1 + 1))
    reduce_reservoir()
    if RESV_RUN.exists():
        rs = pd.read_parquet(RESV_RUN)
        write_parquet_parts(rs, RESERVOIR_DIR)  # scan/reservoir/part_*.parquet, each < 100 MB
        RESV_RUN.unlink()  # the running copy is only needed while the scan is in progress
    elif not any(RESERVOIR_DIR.glob("part_*.parquet")):
        raise FileNotFoundError("no running reservoir and no reservoir parts: rerun the scan")
    else:
        logger.info("reservoir already merged into scan/reservoir/ (kept)")
    ut = [pd.read_parquet(PARTS / f"unt_{fi:04d}.parquet") for fi in fis]
    pd.concat(ut, ignore_index=True).to_parquet(SCAN / "untagged_rows.parquet", index=False)
    us = [pd.read_parquet(PARTS / f"untsamp_{fi:04d}.parquet") for fi in fis]
    pd.concat(us, ignore_index=True).to_parquet(SCAN / "untagged_sample_titles.parquet", index=False)
    meta = [json.loads(p.read_text()) for p in done]
    info = {"files_done": len(fis), "rows": int(sum(m["n"] for m in meta)), "base_rows": int(sum(m["n_base"] for m in meta)),
            "verified_hits": int(sum(m["n_hits"] for m in meta)), "agg_rows": int(len(u))}
    (SCAN / "scan_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"merged: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    logger = setup_logger("scan")
    if args.merge:
        merge(logger)
        return
    files = works_files()
    done = {int(p.stem.split("_")[1]) for p in PARTS.glob("done_*.json")}
    if args.files:
        want = {int(x) for x in args.files.split(",")}
        todo = [f for f in files if f[0] in want and f[0] not in done]
    else:
        todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"files done={len(done)} todo={len(todo)}")
    t0 = time.time()
    n_new, failures = 0, []
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
        tot_bytes = sum(f[2] for f in todo)
        done_bytes = 0
        sizes = {f[0]: f[2] for f in todo}
        while pending:
            fin, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in fin:
                pending.discard(fut)
                try:
                    r = fut.result()
                except Exception as e:  # noqa: BLE001 -- keep scanning; failed files retried on resume
                    logger.error(f"file {fut.fi} failed: {e!r}"[:500])
                    failures.append(fut.fi)
                    submit_next()
                    continue
                n_new += 1
                if n_new % 40 == 0:
                    k = reduce_reservoir()
                    logger.info(f"reservoir: folded {k} parts")
                done_bytes += sizes[r["fi"]]
                el = time.time() - t0
                if n_new % 10 == 0 or n_new == len(todo) or n_new <= 5:
                    eta = el / max(done_bytes, 1) * (tot_bytes - done_bytes) / 60
                    logger.info(f"{n_new}/{len(todo)} files {el/60:.1f} min eta~{eta:.1f} min | fi={r['fi']} "
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s base={r['n_base']} hits={r['n_hits']}")
                submit_next()
    logger.info(f"scan pass finished in {(time.time()-t0)/60:.1f} min; failures={failures}")


if __name__ == "__main__":
    main()
