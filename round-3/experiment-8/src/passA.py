#!/usr/bin/env python3
"""PASS A: one zero-credit pass over all 2,040 OpenAlex works parquet files (HTTP range reads).

Adapted from EXP5 scan_full.process_file: SAME base filter (article|review, not paratext, not xpac), SAME venue-field
lookup, SAME Aho-Corasick automaton built from the FULL frozen lexicon_v1 and SAME stemmed verification, SAME TAG rule
(legacy concept tag score >= 0.3 -> tagstate 1). Differences: titles are matched only for publication years
2000..2016 (all frame feature windows t0-3..t0+2 lie there), and only hits of the 12,499 frame concepts are kept.

Per file (passA/parts/, resumable):
  BG[year, topic]  base works per topic per year (1995-2022, 4,516 topics of EXP3 topic_ids.json); GT[year] = base
                   works with >= 1 known topic
  CNT              grounded (tagstate 1) frame hits keyed (ci, year, vfield) for years 2000-2016 -> check A1
  EARLY rows       grounded frame hits with t0-3 <= year <= t0+2: (ci, year, work_id, vfield, topic idx list,
                   author ids [only year >= t0], cited_by_count)
  RSAMPLE          base works 2003-2016 with splitmix64(fi<<32 | row) % 400 == 0: (work_id, year, vfield,
                   cited_by_count) -- the reference set that field/year-normalises O4

Usage: python passA.py [--files i,j] [--limit N] [--workers W] [--merge]"""
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

from common import (DATA, INPUTS, MATCH_Y0, MATCH_Y1, NY, PASSA, TAG_MIN, Y0, Y1, add_deviation, load_frame, mix64,
                    setup_logger, source_field_lut, works_files, write_parquet_parts)

COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
        "topics.list.element.field.id", "primary_topic.field.id", "concepts.list.element.id",
        "concepts.list.element.score",
        "id", "topics.list.element.id", "authorships.list.element.author.id", "cited_by_count"]
RS_MOD = 400
_W: dict = {}


def _init() -> None:
    from matcher import build_automaton
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "forms", "mtypes"])
    entries = [(f, ci, m) for ci, (fs, ms) in enumerate(zip(lex.forms, lex.mtypes)) for f, m in zip(fs, ms)]
    A, specs = build_automaton(entries)
    sid, code = source_field_lut()
    fr = load_frame()
    t0_of = np.full(len(lex), -1, np.int64)
    t0_of[fr.ci.to_numpy()] = fr.t0.to_numpy()
    tids = np.asarray(json.loads((INPUTS / "topic_ids.json").read_text()), np.int64)
    order = np.argsort(tids)
    _W.update(A=A, specs=specs, cid=lex.concept_id.to_numpy(np.int64), sid=sid, code=code, t0_of=t0_of,
              tids_sorted=tids[order], tids_pos=order.astype(np.int64), nt=len(tids))
    pa.set_cpu_count(1)


def _oa_int(arr, prefix_len: int = 22, null: str = "https://openalex.org/X0") -> np.ndarray:
    """'https://openalex.org/W123' -> 123 (int64); null -> 0."""
    s = pc.utf8_slice_codeunits(pc.fill_null(arr, null), prefix_len)
    return pc.cast(s, pa.int64()).to_numpy(zero_copy_only=False)


def _field_code(arr) -> np.ndarray:
    s = pc.utf8_slice_codeunits(pc.fill_null(arr, "https://openalex.org/fields/10"), 28)
    v = pc.cast(s, pa.int64()).to_numpy(zero_copy_only=False) - 10
    return np.clip(v, 0, 26).astype(np.int64)


def _list_offsets(col) -> tuple[pa.Array, np.ndarray]:
    """(flattened values, offsets[n+1]) of a list column; nulls count as empty lists."""
    arr = col.combine_chunks() if isinstance(col, pa.ChunkedArray) else col
    ln = pc.fill_null(pc.list_value_length(arr), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    off = np.zeros(len(ln) + 1, np.int64)
    off[1:] = np.cumsum(ln)
    return pc.list_flatten(arr), off


def process_file(fi: int, key: str, size: int) -> dict:
    from common5 import surf_arrow
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
    # venue field (EXP5 rule)
    pl = tb.column("primary_location").combine_chunks()
    src = pl.field("source").field("id")
    sidn = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(src, "https://openalex.org/S0"), 22), pa.int64()).to_numpy(
        zero_copy_only=False)
    pos = np.clip(np.searchsorted(_W["sid"], sidn), 0, len(_W["sid"]) - 1)
    vfield = np.where(_W["sid"][pos] == sidn, _W["code"][pos], 0).astype(np.int64)
    wid = _oa_int(tb.column("id"))
    cbc = pc.fill_null(tb.column("cited_by_count"), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    # topics -> topic index (EXP3 order)
    tflat, toff = _list_offsets(tb.column("topics"))
    tnum = _oa_int(tflat.field("id"), 22, "https://openalex.org/T0")
    tp = np.clip(np.searchsorted(_W["tids_sorted"], tnum), 0, _W["nt"] - 1)
    known = _W["tids_sorted"][tp] == tnum
    tix = np.where(known, _W["tids_pos"][tp], -1)
    row_of_t = np.repeat(np.arange(n), np.diff(toff))
    okt = known & base[row_of_t]
    BG = np.bincount(yi[row_of_t[okt]] * _W["nt"] + tix[okt], minlength=NY * _W["nt"]).reshape(NY, _W["nt"])
    has_t = np.zeros(n, bool)
    has_t[row_of_t[okt]] = True
    GT = np.bincount(yi[base & has_t], minlength=NY)
    n_unknown_topic = int((~known & base[row_of_t]).sum())
    # RSAMPLE
    h = mix64(np.int64(fi) * (1 << 32) + np.arange(n, dtype=np.int64))
    rs = base & (year >= 2003) & (year <= 2016) & (h % np.uint64(RS_MOD) == 0) if h.dtype == np.uint64 else \
        base & (year >= 2003) & (year <= 2016) & (h % RS_MOD == 0)
    rsdf = pd.DataFrame({"work_id": wid[rs], "year": year[rs].astype(np.int16), "vfield": vfield[rs].astype(np.int8),
                         "cited_by_count": cbc[rs].astype(np.int32)})
    # title matching on base rows in the match window
    inwin = base & (year >= MATCH_Y0) & (year <= MATCH_Y1)
    bidx = np.nonzero(inwin & pc.is_valid(tb.column("title")).to_numpy(zero_copy_only=False))[0]
    tsub = tb.column("title").take(pa.array(bidx))
    stitles = surf_arrow(tsub).to_pylist()
    titles = tsub.to_pylist()
    A, specs, t0_of = _W["A"], _W["specs"], _W["t0_of"]
    h_row, h_ci = [], []
    for k, (st, t) in enumerate(zip(stitles, titles)):
        m = match(st, t, A, specs)
        if not m:
            continue
        for ci in m:
            if t0_of[ci] >= 0:
                h_row.append(bidx[k])
                h_ci.append(ci)
    del stitles, titles
    h_row = np.asarray(h_row, np.int64)
    h_ci = np.asarray(h_ci, np.int64)
    # tagstate (EXP5 rule) for frame hits only
    tag1 = np.zeros(len(h_row), bool)
    if len(h_row):
        cflat, coff = _list_offsets(tb.column("concepts"))
        cids = _oa_int(cflat.field("id"), 22, "https://openalex.org/C0")
        csc = pc.fill_null(cflat.field("score"), 0.0).to_numpy(zero_copy_only=False)
        want = _W["cid"][h_ci]
        for k in range(len(h_row)):
            r = h_row[k]
            a, b = coff[r], coff[r + 1]
            if b == a:
                continue
            w = np.nonzero(cids[a:b] == want[k])[0]
            tag1[k] = bool(len(w) and csc[a + w[0]] >= TAG_MIN)
    g_row, g_ci = h_row[tag1], h_ci[tag1]
    gy = year[g_row]
    cnt_key = (g_ci * 32 + (gy - Y0)) * 32 + vfield[g_row]
    uK, cK = np.unique(cnt_key, return_counts=True)
    # early rows
    t0c = t0_of[g_ci]
    early = (gy >= t0c - 3) & (gy <= t0c + 2)
    e_row, e_ci = g_row[early], g_ci[early]
    tops, auths = [], []
    if len(e_row):
        aflat, aoff = _list_offsets(tb.column("authorships"))
        aid = _oa_int(aflat.field("author").field("id"), 22, "https://openalex.org/A0")
        for r, c in zip(e_row.tolist(), e_ci.tolist()):
            tt = tix[toff[r]:toff[r + 1]]
            tops.append(tt[tt >= 0].astype(np.int16).tolist())
            if year[r] >= t0_of[c]:
                aa = aid[aoff[r]:aoff[r + 1]]
                auths.append(aa[aa > 0].tolist())
            else:
                auths.append([])
    edf = pd.DataFrame({"ci": e_ci.astype(np.int32), "year": year[e_row].astype(np.int16), "work_id": wid[e_row],
                        "vfield": vfield[e_row].astype(np.int8), "topics": tops, "authors": auths,
                        "cited_by_count": cbc[e_row].astype(np.int32)})
    out = {"fi": fi, "n": n, "n_base": int(base.sum()), "n_win_titles": int(len(bidx)),
           "n_frame_hits": int(len(h_row)), "n_grounded": int(len(g_row)), "n_early": int(len(e_row)),
           "n_rsample": int(len(rsdf)), "n_unknown_topic": n_unknown_topic, "t_io": t_io}
    np.savez_compressed(PASSA / f"agg_{fi:04d}.npz", BG=BG.astype(np.int32), GT=GT, uK=uK, cK=cK)
    edf.to_parquet(PASSA / f"early_{fi:04d}.parquet", index=False)
    rsdf.to_parquet(PASSA / f"rs_{fi:04d}.parquet", index=False)
    out["t_all"] = time.time() - t_start
    (PASSA / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb
    gc.collect()
    return out


def merge(logger) -> None:
    done = sorted(PASSA.glob("done_*.json"))
    fis = [int(p.stem.split("_")[1]) for p in done]
    logger.info(f"merging {len(fis)} Pass A parts")
    BG = None
    GT = np.zeros(NY, np.int64)
    keys, cnts, early, rs = [], [], [], []
    for fi in fis:
        z = np.load(PASSA / f"agg_{fi:04d}.npz")
        BG = z["BG"].astype(np.int64) if BG is None else BG + z["BG"]
        GT += z["GT"]
        keys.append(z["uK"]); cnts.append(z["cK"])
        early.append(pd.read_parquet(PASSA / f"early_{fi:04d}.parquet"))
        rs.append(pd.read_parquet(PASSA / f"rs_{fi:04d}.parquet"))
    k = np.concatenate(keys); c = np.concatenate(cnts)
    u, inv = np.unique(k, return_inverse=True)
    c = np.bincount(inv, weights=c).astype(np.int64)
    vf = u % 32; r = u // 32; yy = r % 32; ci = r // 32
    pd.DataFrame({"ci": ci.astype(np.int32), "year": (yy + Y0).astype(np.int16), "vfield": vf.astype(np.int8),
                  "n": c}).to_parquet(DATA / "counts_check.parquet", index=False)
    np.savez_compressed(DATA / "bg_topics.npz", BG=BG, GT=GT, years=np.arange(Y0, Y1 + 1))
    edf = pd.concat(early, ignore_index=True).sort_values(["ci", "year", "work_id"]).reset_index(drop=True)
    write_parquet_parts(edf, DATA / "frame_matches_early")
    pd.concat(rs, ignore_index=True).to_parquet(DATA / "ref_sample.parquet", index=False)
    meta = [json.loads(p.read_text()) for p in done]
    info = {"files_done": len(fis), **{k_: int(sum(m[k_] for m in meta)) for k_ in
                                       ("n", "n_base", "n_win_titles", "n_frame_hits", "n_grounded", "n_early",
                                        "n_rsample", "n_unknown_topic")},
            "early_rows": int(len(edf))}
    (DATA / "passA_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"Pass A merged: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    logger = setup_logger("passA")
    if args.merge:
        merge(logger)
        return
    files = works_files()
    done = {int(p.stem.split("_")[1]) for p in PASSA.glob("done_*.json")}
    if args.files:
        want = {int(x) for x in args.files.split(",")}
        todo = [f for f in files if f[0] in want and f[0] not in done]
    else:
        todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"files done={len(done)} todo={len(todo)} workers={args.workers}")
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
        for _ in range(args.workers + 2):
            submit_next()
        while pending:
            fin, _ = wait(pending, return_when=FIRST_COMPLETED)
            for fut in fin:
                pending.discard(fut)
                try:
                    r = fut.result()
                except Exception as e:  # noqa: BLE001 -- keep scanning; failed files are retried on resume
                    logger.error(f"file {fut.fi} failed: {e!r}"[:600])
                    failures.append(fut.fi)
                    submit_next()
                    continue
                n_new += 1
                done_bytes += sizes[r["fi"]]
                el = time.time() - t0
                if n_new % 10 == 0 or n_new == len(todo) or n_new <= 6:
                    eta = el / max(done_bytes, 1) * (tot_bytes - done_bytes) / 60
                    logger.info(f"{n_new}/{len(todo)} files {el/60:.1f} min eta~{eta:.1f} min | fi={r['fi']} "
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s base={r['n_base']} "
                                f"grounded={r['n_grounded']} early={r['n_early']}")
                submit_next()
    logger.info(f"Pass A finished in {(time.time()-t0)/60:.1f} min; failures={failures}")
    if failures:
        add_deviation("passA_failures", f"files failed in this run (retried on resume): {failures}")


if __name__ == "__main__":
    main()
