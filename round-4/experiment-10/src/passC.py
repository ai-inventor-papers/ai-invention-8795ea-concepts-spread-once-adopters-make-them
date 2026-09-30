#!/usr/bin/env python3
"""S2 PASS C: one zero-credit pass over all 2,040 OpenAlex works parquet files (public S3, HTTP range reads).

Adapted from EXP8 passA.py / EXP5 scan_full.process_file: SAME base filter (article|review, not paratext, not xpac),
SAME venue-field lookup (EXP5 source->field map), SAME Aho-Corasick automaton built from the FULL frozen lexicon_v1,
SAME stemmed verification, SAME tagstate rule (1 = legacy tag of the concept with score >= 0.3; 2 = work has legacy
concepts but not this one at >= 0.3; 3 = work has no legacy concept). Differences: the base-year cap moves
2022 -> 2024, titles are matched for publication years 2012..2024 only, and hits are kept only for the cohort
candidates (t0 2015-2017) and the 300 EXP5 control concepts. referenced_works is NOT read (O4 dropped up front,
plan drop order; see results/deviations.json).

Per file (passC/parts/, resumable via done_XXXX.json):
  tot_XXXX.npz  G[year, vfield] base works 1995..2024 x 27 venue codes; TAGANY[year, vfield] base works with >= 1
                legacy concept; TAG03[year, vfield] base works with >= 1 legacy concept of score >= 0.3;
                BG[year 2012..2018, topic] base works per topic (EXP3 topic order)
  pre_XXXX.parquet     AGG counts (ci, year, vfield, tagstate, mt, n) for controls (all years 2012..2024) and for
                       candidates with year <= t0+2
  early_XXXX.parquet   candidate hits with t0-3 <= year <= t0+2 (all tagstates): ci, year, work_id, vfield, tagstate,
                       mt, topic idx list, author ids (years >= t0, as EXP8), title
  data/sealed/parts/sealed_XXXX.parquet  AGG counts for candidates with year >= t0+3 (NOT read before the seal)

Usage: python passC.py [--files i,j] [--limit N] [--workers W] [--merge]"""
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

from common import DATA, INPUTS, LOGS, ROOT, add_deviation, setup_logger, sha256_file, source_field_lut, works_files

Y0, Y1 = 1995, 2024
NY = Y1 - Y0 + 1
MATCH_Y0, MATCH_Y1 = 2012, 2024
BG_Y0, BG_Y1 = 2012, 2018
TAG_MIN = 0.3
PARTS = ROOT / "passC" / "parts"
SEALED_PARTS = DATA / "sealed" / "parts"
COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
        "concepts.list.element.id", "concepts.list.element.score", "id", "topics.list.element.id",
        "authorships.list.element.author.id"]
_W: dict = {}


def _init() -> None:
    from matcher import build_automaton
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "forms", "mtypes"])
    entries = [(f, ci, m) for ci, (fs, ms) in enumerate(zip(lex.forms, lex.mtypes)) for f, m in zip(fs, ms)]
    A, specs = build_automaton(entries)
    sid, code = source_field_lut()
    cc = pd.read_csv(DATA / "cohort_candidates.csv")
    ct = pd.read_csv(DATA / "controls.csv")
    role = np.zeros(len(lex), np.int8)            # 0 = not wanted, 1 = candidate, 2 = control
    role[ct.ci.to_numpy()] = 2
    role[cc.ci.to_numpy()] = 1
    t0_of = np.full(len(lex), 9999, np.int64)
    t0_of[cc.ci.to_numpy()] = cc.t0.to_numpy()
    tids = np.asarray(json.loads((INPUTS / "topic_ids.json").read_text()), np.int64)
    order = np.argsort(tids)
    _W.update(A=A, specs=specs, cid=lex.concept_id.to_numpy(np.int64), sid=sid, code=code, role=role, t0_of=t0_of,
              tids_sorted=tids[order], tids_pos=order.astype(np.int64), nt=len(tids))
    pa.set_cpu_count(1)


def _oa_int(arr, prefix_len: int = 22, null: str = "https://openalex.org/X0") -> np.ndarray:
    s = pc.utf8_slice_codeunits(pc.fill_null(arr, null), prefix_len)
    return pc.cast(s, pa.int64()).to_numpy(zero_copy_only=False)


def _list_offsets(col) -> tuple[pa.Array, np.ndarray]:
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
    pl = tb.column("primary_location").combine_chunks()
    src = pl.field("source").field("id")
    sidn = pc.cast(pc.utf8_slice_codeunits(pc.fill_null(src, "https://openalex.org/S0"), 22), pa.int64()).to_numpy(
        zero_copy_only=False)
    pos = np.clip(np.searchsorted(_W["sid"], sidn), 0, len(_W["sid"]) - 1)
    vfield = np.where(_W["sid"][pos] == sidn, _W["code"][pos], 0).astype(np.int64)
    G = np.bincount(yi[base] * 27 + vfield[base], minlength=NY * 27).reshape(NY, 27)
    # legacy concept coverage (outcome-blind audit)
    cflat, coff = _list_offsets(tb.column("concepts"))
    csc = pc.fill_null(cflat.field("score"), 0.0).to_numpy(zero_copy_only=False)
    nconc = np.diff(coff)
    row_of_c = np.repeat(np.arange(n), nconc)
    has03 = np.zeros(n, bool)
    has03[row_of_c[csc >= TAG_MIN]] = True
    hasany = nconc > 0
    TAGANY = np.bincount(yi[base & hasany] * 27 + vfield[base & hasany], minlength=NY * 27).reshape(NY, 27)
    TAG03 = np.bincount(yi[base & has03] * 27 + vfield[base & has03], minlength=NY * 27).reshape(NY, 27)
    # topic background 2012..2018
    tflat, toff = _list_offsets(tb.column("topics"))
    tnum = _oa_int(tflat.field("id"), 22, "https://openalex.org/T0")
    tp = np.clip(np.searchsorted(_W["tids_sorted"], tnum), 0, _W["nt"] - 1)
    known = _W["tids_sorted"][tp] == tnum
    tix = np.where(known, _W["tids_pos"][tp], -1)
    row_of_t = np.repeat(np.arange(n), np.diff(toff))
    nbg = BG_Y1 - BG_Y0 + 1
    okt = known & base[row_of_t] & (year[row_of_t] >= BG_Y0) & (year[row_of_t] <= BG_Y1)
    BG = np.bincount((year[row_of_t[okt]] - BG_Y0) * _W["nt"] + tix[okt], minlength=nbg * _W["nt"]).reshape(
        nbg, _W["nt"])
    wid = _oa_int(tb.column("id"))
    # title matching on base rows in the match window
    inwin = base & (year >= MATCH_Y0) & (year <= MATCH_Y1)
    bidx = np.nonzero(inwin & pc.is_valid(tb.column("title")).to_numpy(zero_copy_only=False))[0]
    tsub = tb.column("title").take(pa.array(bidx))
    stitles = surf_arrow(tsub).to_pylist()
    titles = tsub.to_pylist()
    A, specs, role = _W["A"], _W["specs"], _W["role"]
    h_row, h_ci, h_mt, h_k = [], [], [], []
    for k, (st, t) in enumerate(zip(stitles, titles)):
        m = match(st, t, A, specs)
        if not m:
            continue
        for ci, mt in m.items():
            if role[ci]:
                h_row.append(bidx[k]); h_ci.append(ci); h_mt.append(mt); h_k.append(k)
    del stitles
    h_row = np.asarray(h_row, np.int64)
    h_ci = np.asarray(h_ci, np.int64)
    h_mt = np.asarray(h_mt, np.int64)
    tagstate = np.full(len(h_row), 3, np.int64)
    if len(h_row):
        cids = _oa_int(cflat.field("id"), 22, "https://openalex.org/C0")
        want = _W["cid"][h_ci]
        for k in range(len(h_row)):
            r = h_row[k]
            a, b = coff[r], coff[r + 1]
            if b == a:
                continue
            w = np.nonzero(cids[a:b] == want[k])[0]
            tagstate[k] = 1 if (len(w) and csc[a + w[0]] >= TAG_MIN) else 2
    hy = year[h_row]
    hv = vfield[h_row]
    t0c = _W["t0_of"][h_ci]
    is_cand = role[h_ci] == 1
    sealed = is_cand & (hy >= t0c + 3)
    agg = pd.DataFrame({"ci": h_ci.astype(np.int32), "year": hy.astype(np.int16), "vfield": hv.astype(np.int8),
                        "tagstate": tagstate.astype(np.int8), "mt": h_mt.astype(np.int8)})
    agg_pre = agg[~sealed].value_counts().rename("n").reset_index()
    agg_sealed = agg[sealed].value_counts().rename("n").reset_index()
    early = is_cand & (hy >= t0c - 3) & (hy <= t0c + 2)
    tops, auths, etit = [], [], []
    e_idx = np.nonzero(early)[0]
    if len(e_idx):
        aflat, aoff = _list_offsets(tb.column("authorships"))
        aid = _oa_int(aflat.field("author").field("id"), 22, "https://openalex.org/A0")
        for j in e_idx.tolist():
            r = h_row[j]
            tt = tix[toff[r]:toff[r + 1]]
            tops.append(tt[tt >= 0].astype(np.int16).tolist())
            if year[r] >= t0c[j]:
                aa = aid[aoff[r]:aoff[r + 1]]
                auths.append(aa[aa > 0].tolist())
            else:
                auths.append([])
            etit.append((titles[h_k[j]] or "")[:300])
    edf = pd.DataFrame({"ci": h_ci[e_idx].astype(np.int32), "year": hy[e_idx].astype(np.int16),
                        "work_id": wid[h_row[e_idx]], "vfield": hv[e_idx].astype(np.int8),
                        "tagstate": tagstate[e_idx].astype(np.int8), "mt": h_mt[e_idx].astype(np.int8),
                        "topics": tops, "authors": auths, "title": etit})
    np.savez_compressed(PARTS / f"tot_{fi:04d}.npz", G=G, TAGANY=TAGANY, TAG03=TAG03, BG=BG.astype(np.int32))
    agg_pre.to_parquet(PARTS / f"pre_{fi:04d}.parquet", index=False)
    edf.to_parquet(PARTS / f"early_{fi:04d}.parquet", index=False)
    agg_sealed.to_parquet(SEALED_PARTS / f"sealed_{fi:04d}.parquet", index=False)
    out = {"fi": fi, "n": n, "n_base": int(base.sum()), "n_win_titles": int(len(bidx)), "n_hits": int(len(h_row)),
           "n_sealed_hits": int(sealed.sum()), "n_early": int(len(edf)), "t_io": t_io,
           "year_min": int(year[base].min()) if base.any() else None,
           "year_max": int(year[base].max()) if base.any() else None, "t_all": time.time() - t_start}
    (PARTS / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb, titles
    gc.collect()
    return out


def merge(logger) -> None:
    done = sorted(PARTS.glob("done_*.json"))
    fis = [int(p.stem.split("_")[1]) for p in done]
    logger.info(f"merging {len(fis)} Pass C parts")
    G = TAGANY = TAG03 = BG = None
    pre, early = [], []
    for fi in fis:
        z = np.load(PARTS / f"tot_{fi:04d}.npz")
        if G is None:
            G, TAGANY, TAG03, BG = (z[k].astype(np.int64) for k in ("G", "TAGANY", "TAG03", "BG"))
        else:
            G += z["G"]; TAGANY += z["TAGANY"]; TAG03 += z["TAG03"]; BG += z["BG"]
        pre.append(pd.read_parquet(PARTS / f"pre_{fi:04d}.parquet"))
        early.append(pd.read_parquet(PARTS / f"early_{fi:04d}.parquet"))
    np.savez_compressed(DATA / "passC_totals.npz", G=G, TAGANY=TAGANY, TAG03=TAG03, years=np.arange(Y0, Y1 + 1))
    np.savez_compressed(DATA / "passC_bg.npz", BG=BG, years=np.arange(BG_Y0, BG_Y1 + 1))
    pre = pd.concat(pre, ignore_index=True)
    pre = pre.groupby(["ci", "year", "vfield", "tagstate", "mt"], as_index=False)["n"].sum()
    pre.to_parquet(DATA / "passC_pre_agg.parquet", index=False)
    edf = pd.concat(early, ignore_index=True).sort_values(["ci", "year", "work_id"]).reset_index(drop=True)
    edf.to_parquet(DATA / "passC_early.parquet", index=False)
    # hash every sealed part (never read here); the seal gate re-checks these hashes before and at the unseal
    sealed = sorted(SEALED_PARTS.glob("sealed_*.parquet"))
    with (LOGS / "sealed_files.log").open("w") as f:
        for p in sealed:
            f.write(f"{p.name}\t{sha256_file(p)}\n")
    meta = [json.loads(p.read_text()) for p in done]
    info = {"files_done": len(fis), **{k: int(sum(m[k] for m in meta)) for k in
                                       ("n", "n_base", "n_win_titles", "n_hits", "n_sealed_hits", "n_early")},
            "year_min": min(m["year_min"] for m in meta if m["year_min"] is not None),
            "year_max": max(m["year_max"] for m in meta if m["year_max"] is not None),
            "early_rows": int(len(edf)), "pre_agg_rows": int(len(pre)), "sealed_parts": len(sealed)}
    (DATA / "passC_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"Pass C merged: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    PARTS.mkdir(parents=True, exist_ok=True)
    SEALED_PARTS.mkdir(parents=True, exist_ok=True)
    logger = setup_logger("passC")
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
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s base={r['n_base']} hits={r['n_hits']} "
                                f"early={r['n_early']} yrs={r['year_min']}-{r['year_max']}")
                submit_next()
    logger.info(f"Pass C finished in {(time.time()-t0)/60:.1f} min; failures={failures}")
    if failures:
        add_deviation("passC_failures", f"files failed in this run (retried on resume): {failures}")


if __name__ == "__main__":
    main()
