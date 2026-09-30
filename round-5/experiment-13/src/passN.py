#!/usr/bin/env python3
"""S4 PASS N: one zero-credit pass over all 2,040 OpenAlex works files, counting the Frame-N candidate phrases.

Adapted from EXP10 passC.py: SAME base filter (article|review, not paratext, not xpac), SAME venue-field LUT, SAME
HTTP-range reader, SAME Aho-Corasick + stemmed verification (lib/matcher.py). Differences: the automaton holds the
Frame-N candidate names/aliases (data/frame_n_candidates.csv, ci >= 0), titles are matched for 1995..2022, there is no
legacy-concept tagstate, and hits are ROUTED AT WRITE TIME by the candidate's detection year t_det:
  year >  t_det+4           -> sealed/parts/sealedA_XXXX.parquet  AGG (ci, year, vfield, n)   [never opened pre-unseal]
  t_det-5 <= year <= t_det+4 -> open/parts/early_XXXX.parquet    detail (ci, year, work_id, vfield, topics, authors,
                                                                  title[:300] for years >= t_det-2)
  year <  t_det-5           -> open/parts/pre_XXXX.parquet       AGG (ci, year, vfield, n)
Per file also: open/parts/tot_XXXX.npz base totals G[1995..2024, 27] (T1 check vs EXP10 tot_XXXX).

--legacy-test runs the EXP10 configuration instead (full lexicon_v1 automaton, EXP10 cohort roles, t_det := t0,
match window 2012..2024) into tests/t1_parts/, for unit test T1.
Usage: python passN.py [--files i,j] [--limit N] [--workers W] [--merge] [--legacy-test]"""
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
OPEN_HI = 4          # v2: open window t_det-5..t_det+4 (v1: +2), so onsets t0 in [t_det-2, t_det+2] are findable
NY = Y1 - Y0 + 1
COLS = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id", "id",
        "topics.list.element.id", "authorships.list.element.author.id"]
_W: dict = {}


def dirs(legacy: bool) -> tuple[Path, Path]:
    if legacy:
        return ROOT / "tests" / "t1_parts", ROOT / "tests" / "t1_parts"
    return ROOT / "open" / "parts", ROOT / "sealed" / "parts"


def _init(legacy: bool) -> None:
    from common5 import surf
    from matcher import build_automaton
    if legacy:
        lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "forms", "mtypes"])
        entries = [(f, ci, m) for ci, (fs, ms) in enumerate(zip(lex.forms, lex.mtypes)) for f, m in zip(fs, ms)]
        cc = pd.read_csv(INPUTS / "cohort_candidates.csv")
        want = np.zeros(len(lex), bool)
        want[cc.ci.to_numpy()] = True
        tdet = np.full(len(lex), 9999, np.int64)
        tdet[cc.ci.to_numpy()] = cc.t0.to_numpy()
        my0, my1 = 2012, 2024
    else:
        cand = pd.read_csv(DATA / "frame_n_candidates.csv")
        cand = cand[cand.ci >= 0].sort_values("ci")
        entries = []
        for r in cand.itertuples():
            entries.append((surf(r.name), int(r.ci), "name_exact"))
            for a in str(r.aliases).split("|"):
                if a and a != "nan":
                    entries.append((surf(a), int(r.ci), "name_variant"))
        n = int(cand.ci.max()) + 1
        want = np.ones(n, bool)
        tdet = np.zeros(n, np.int64)
        tdet[cand.ci.to_numpy()] = cand.t_det.to_numpy()
        my0, my1 = 1995, 2022
    A, specs = build_automaton(entries)
    sid, code = source_field_lut()
    tids = np.asarray(json.loads((INPUTS / "topic_ids.json").read_text()), np.int64)
    order = np.argsort(tids)
    _W.update(A=A, specs=specs, sid=sid, code=code, want=want, tdet=tdet, my0=my0, my1=my1, legacy=legacy,
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
    OPEN, SEALED = dirs(_W["legacy"])
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
    wid = _oa_int(tb.column("id"))
    inwin = base & (year >= _W["my0"]) & (year <= _W["my1"])
    bidx = np.nonzero(inwin & pc.is_valid(tb.column("title")).to_numpy(zero_copy_only=False))[0]
    tsub = tb.column("title").take(pa.array(bidx))
    stitles = surf_arrow(tsub).to_pylist()
    titles = tsub.to_pylist()
    A, specs, want = _W["A"], _W["specs"], _W["want"]
    h_row, h_ci, h_mt, h_k = [], [], [], []
    for k, (st, t) in enumerate(zip(stitles, titles)):
        m = match(st, t, A, specs)
        if not m:
            continue
        for ci, mt in m.items():
            if want[ci]:
                h_row.append(bidx[k]); h_ci.append(ci); h_mt.append(mt); h_k.append(k)
    del stitles
    h_row = np.asarray(h_row, np.int64)
    h_ci = np.asarray(h_ci, np.int64)
    h_mt = np.asarray(h_mt, np.int64)
    hy = year[h_row]
    hv = vfield[h_row]
    td = _W["tdet"][h_ci]
    sealed = hy > td + (2 if _W["legacy"] else OPEN_HI)
    early = (hy >= td - 5) & ~sealed
    pre = hy < td - 5
    agg = pd.DataFrame({"ci": h_ci.astype(np.int32), "year": hy.astype(np.int16), "vfield": hv.astype(np.int8),
                        "mt": h_mt.astype(np.int8)})
    agg_sealed = agg[sealed].value_counts().rename("n").reset_index()
    agg_pre = agg[pre].value_counts().rename("n").reset_index()
    tops, auths, etit = [], [], []
    e_idx = np.nonzero(early)[0]
    if len(e_idx):
        tflat, toff = _list_offsets(tb.column("topics"))
        tnum = _oa_int(tflat.field("id"), 22, "https://openalex.org/T0")
        tp = np.clip(np.searchsorted(_W["tids_sorted"], tnum), 0, _W["nt"] - 1)
        tix = np.where(_W["tids_sorted"][tp] == tnum, _W["tids_pos"][tp], -1)
        aflat, aoff = _list_offsets(tb.column("authorships"))
        aid = _oa_int(aflat.field("author").field("id"), 22, "https://openalex.org/A0")
        for j in e_idx.tolist():
            r = h_row[j]
            tt = tix[toff[r]:toff[r + 1]]
            tops.append(tt[tt >= 0].astype(np.int16).tolist())
            if year[r] >= td[j] - 2:
                aa = aid[aoff[r]:aoff[r + 1]]
                auths.append(aa[aa > 0].tolist())
                etit.append((titles[h_k[j]] or "")[:300])
            else:
                auths.append([])
                etit.append("")
    edf = pd.DataFrame({"ci": h_ci[e_idx].astype(np.int32), "year": hy[e_idx].astype(np.int16),
                        "work_id": wid[h_row[e_idx]], "vfield": hv[e_idx].astype(np.int8),
                        "mt": h_mt[e_idx].astype(np.int8), "topics": tops, "authors": auths, "title": etit})
    np.savez_compressed(OPEN / f"tot_{fi:04d}.npz", G=G)
    agg_pre.to_parquet(OPEN / f"pre_{fi:04d}.parquet", index=False)
    edf.to_parquet(OPEN / f"early_{fi:04d}.parquet", index=False)
    agg_sealed.to_parquet(SEALED / f"sealedA_{fi:04d}.parquet", index=False)
    out = {"fi": fi, "n": n, "n_base": int(base.sum()), "n_win_titles": int(len(bidx)), "n_hits": int(len(h_row)),
           "n_sealed_hits": int(sealed.sum()), "n_early": int(len(edf)), "n_pre_hits": int(pre.sum()), "t_io": t_io,
           "t_all": time.time() - t_start}
    (OPEN / f"done_{fi:04d}.json").write_text(json.dumps(out))
    del tb, titles
    gc.collect()
    return out


def merge(logger) -> None:
    OPEN, SEALED = dirs(False)
    done = sorted(OPEN.glob("done_*.json"))
    fis = [int(p.stem.split("_")[1]) for p in done]
    logger.info(f"merging {len(fis)} Pass N parts")
    G = None
    pre, early = [], []
    for fi in fis:
        z = np.load(OPEN / f"tot_{fi:04d}.npz")
        G = z["G"].astype(np.int64) if G is None else G + z["G"]
        pre.append(pd.read_parquet(OPEN / f"pre_{fi:04d}.parquet"))
        e = pd.read_parquet(OPEN / f"early_{fi:04d}.parquet", columns=["ci"])
        if len(e):
            early.append(e)
    np.savez_compressed(DATA / "passN_totals.npz", G=G, years=np.arange(Y0, Y1 + 1))
    pre = pd.concat(pre, ignore_index=True).groupby(["ci", "year", "vfield", "mt"], as_index=False)["n"].sum()
    pre.to_parquet(ROOT / "open" / "passN_pre_agg.parquet", index=False)
    # v2: the detail rows stay in the per-file parts (too large to merge in pandas); S5 reads them with pyarrow
    n_early_rows = int(sum(len(e) for e in early))
    edf = pd.DataFrame({"n": [n_early_rows]})
    from sealn import log_sealed_parts
    n_sealed = log_sealed_parts()
    meta = [json.loads(p.read_text()) for p in done]
    info = {"files_done": len(fis), **{k: int(sum(m[k] for m in meta)) for k in
                                       ("n", "n_base", "n_win_titles", "n_hits", "n_sealed_hits", "n_early",
                                        "n_pre_hits")},
            "early_rows": int(edf.n.iat[0]), "open_hi": OPEN_HI, "pre_agg_rows": int(len(pre)), "sealed_parts": n_sealed}
    (DATA / "passN_info.json").write_text(json.dumps(info, indent=1))
    logger.info(f"Pass N merged: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--files", type=str, default="")
    ap.add_argument("--merge", action="store_true")
    ap.add_argument("--legacy-test", action="store_true")
    args = ap.parse_args()
    OPEN, SEALED = dirs(args.legacy_test)
    OPEN.mkdir(parents=True, exist_ok=True)
    SEALED.mkdir(parents=True, exist_ok=True)
    logger = setup_logger("passN" + ("_t1" if args.legacy_test else ""))
    if args.merge:
        merge(logger)
        return
    files = works_files()
    done = {int(p.stem.split("_")[1]) for p in OPEN.glob("done_*.json")}
    if args.files:
        want = {int(x) for x in args.files.split(",")}
        todo = [f for f in files if f[0] in want and f[0] not in done]
    else:
        todo = sorted([f for f in files if f[0] not in done], key=lambda f: -f[2])
    if args.limit:
        todo = todo[:args.limit]
    logger.info(f"files done={len(done)} todo={len(todo)} workers={args.workers} legacy_test={args.legacy_test}")
    t0 = time.time()
    tot_bytes = sum(f[2] for f in todo)
    sizes = {f[0]: f[2] for f in todo}
    done_bytes, n_new, failures = 0, 0, []
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"), initializer=_init,
                             initargs=(args.legacy_test,)) as ex:
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
                if n_new % 10 == 0 or n_new == len(todo) or n_new <= 6:
                    eta = el / max(done_bytes, 1) * (tot_bytes - done_bytes) / 60
                    logger.info(f"{n_new}/{len(todo)} files {el/60:.1f} min eta~{eta:.1f} min | fi={r['fi']} "
                                f"io={r['t_io']:.1f}s all={r['t_all']:.1f}s base={r['n_base']} hits={r['n_hits']} "
                                f"early={r['n_early']} sealed={r['n_sealed_hits']}")
                submit_next()
    logger.info(f"Pass N finished in {(time.time()-t0)/60:.1f} min; failures={failures}")
    if failures and not args.legacy_test:
        add_deviation("passN_failures", f"files failed in this run (retried on resume): {failures}")


if __name__ == "__main__":
    main()
