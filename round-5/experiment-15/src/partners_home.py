#!/usr/bin/env python3
"""iter-5 STEP 6 (Part A build): HOME-ONLY t0..t0+2 new / dropped / added partner sets with the EXACT EXP8 ego
primitives Exp10 used for NOV_res__home, new_edge_rate__home and edge_persistence__home (lib_iter5/ego.py is Exp10's
lib/ego.py verbatim), each partner classified on four axes, and an EXACT additive decomposition of the three totals.

Axes (class of a partner topic k):
  type     METHOD | DOMAIN                    Exp11 results/topic_types.csv (LLM-typed, kappa 0.84)
  comm     new | old | unk                    backbone community of k in the slice of its (first) year != / == the
                                              concept's t0 modal community C0 (unk if C0 undefined)
  deg      low | high                         key (deg_s0(k), k) below / above the degree-weighted median key of the
                                              NOV null pool (P_null(low) = 0.5 by construction)
  carrier  mixed | pure                       some home paper of the partner's (first) year that contains k also carries
                                              a non-SELF topic from a field outside the concept's home fields -> mixed
Components (identities asserted per concept, |err| < 1e-12):
  NOV_res        = sum_X nov_X,  nov_X = (1/M) sum_{k in NEW & X} (1[comm_k != C0] - E)      (type, deg, carrier)
  novnull_X      = NOV_X - E_X  (E_X = degree-weighted share outside C0 within pool & X; carrier: E_X = E)
  new_edge_rate  = sum_X ner_X, ner_X = (|NEW & X| / 3) / (n1 + 1)                            (all four axes)
  churn          = 1 - edge_persistence = sum_X (chd_X + cha_X),
                   chd_X = (1/T) sum_t |DROP_t & X| / |U_t|,  cha_X = (1/T) sum_t |ADD_t & X| / |U_t|
                   (t over the defined transitions W1->W2, W2->W3; T = # defined)
Also: bridging papers (early home papers that introduce >= 1 new-community new partner in its first year) and the
static later-window build (t0+3..t0+5 with PRE = t0..t0+2) for the Part B test-retest.

Usage: python partners_home.py --frame exp5|cohort|retest [--limit N] [--workers 4]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
import warnings
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib_iter5"))

import numpy as np
import pandas as pd

from common_iter5 import DATA, E8, E10, E11, read_parts, setup_logger

AXES = {"type": ["METHOD", "DOMAIN", "OTHER"], "comm": ["new", "old", "unk"], "deg": ["low", "high"],
        "carrier": ["mixed", "pure"]}
NOV_AXES = ["type", "deg", "carrier"]
_T: dict = {}


# ----------------------------------------------------------------------------- worker context
def _init() -> None:
    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    tids = json.loads((E11 / "inputs/topic_ids.json").read_text())
    tm = pd.read_csv(E11 / "inputs/topic_meta.csv").set_index("topic").loc[tids]
    tt = pd.read_csv(E11 / "results/topic_types.csv").set_index("topic_idx")
    cls = tt.reindex(np.arange(len(tids)))["class"].fillna("OTHER").to_numpy()
    _T["type"] = np.where(np.isin(cls, ["METHOD", "DOMAIN"]), cls, "OTHER")
    _T["fcode"] = tm.field.to_numpy(int) - 10          # same code space as the frame's vfield / home codes


def home_codes_of(h) -> set[int]:
    """Exp10 s7_ego.home_codes_of (verbatim)."""
    return {int(float(x)) - 10 for x in str(h).split(";") if x and x != "nan"}


# ----------------------------------------------------------------------------- the build
def home_partners(ci: int, name: str, aliases: list[str], t0: int, rows: list, hcodes: set[int]) -> tuple[dict, list, list]:
    """rows = [(year, topics tuple, vfield, work_id)] grounded early papers t0-3..t0+2 (all venues)."""
    import ego
    C = ego.C
    works = [(y, tp) for y, tp, v, _ in rows if v in hcodes]           # = s7 works_home
    papers = [(y, tp, w) for y, tp, v, w in rows if v in hcodes]
    out: dict = {"ci": ci, "n_home_early": int(sum(1 for y, *_ in papers if t0 <= y <= t0 + 2))}
    # ------- verbatim concept_core preamble (same calls, same order)
    win = ego.rq1_windows(t0)
    early_years = sorted(set(win["W1"] + win["W2"] + win["W3"]))
    n_early, nc_early = ego.window_counts(works, early_years)
    SELF = ego.self_topics(name, aliases, n_early, nc_early)
    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}
    for w, ys in win.items():
        cnt[w], nc[w] = ego.window_counts(works, ys)
        bgw[w], NW[w] = ego.bg_window(ys)
    nbg_early, _ = ego.bg_window(early_years)
    for w in ("W1", "W2", "W3"):
        NB[w], P[w] = ego.neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, 2)
    pre_set = cnt["PRE"] >= 1
    new = (NB["W1"] | NB["W2"] | NB["W3"]) & ~pre_set
    new_idx = np.nonzero(new)[0]
    M = len(new_idx)
    first_year = {}
    for y in early_years:
        cy, _ = ego.window_counts(works, [y])
        for k in new_idx:
            if k not in first_year and cy[k] >= 1:
                first_year[k] = y
    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]
    s0 = ego.slice_of(t0)
    comm0 = C["comm"][s0]
    w1 = cnt["W1"]
    C0 = None
    if w1.sum() > 0:
        cs = Counter()
        for k in np.nonzero(w1)[0]:
            cs[comm0[k]] += w1[k]
        C0 = cs.most_common(1)[0][0]
    n1 = int(NB["W1"].sum())
    deg0 = C["deg"][s0].astype(float)
    # ------- class maps
    # degree cut: lexicographic key (deg, topic index); cut at the degree-weighted median of the pool
    if len(pool) and deg0[pool].sum() > 0:
        o = pool[np.lexsort((pool, deg0[pool]))]
        cw = np.cumsum(deg0[o]) / deg0[o].sum()
        j = int(np.searchsorted(cw, 0.5))
        kcut = (deg0[o[j]], o[j])
        out["null_low_share"] = float(cw[j - 1]) if j > 0 else 0.0
    else:
        kcut = None
        out["null_low_share"] = np.nan

    def is_low(k: int) -> bool:
        return bool(kcut is not None and (deg0[k], k) < kcut)

    fcode = _T["fcode"]
    by_year: dict[int, list] = {}
    for y, tp, w in papers:
        by_year.setdefault(y, []).append((tp, w))

    def carrier(k: int, y: int) -> str:
        for tp, _ in by_year.get(y, []):
            if k in tp and any((kk != k) and (not SELF[kk]) and (fcode[kk] not in hcodes) for kk in tp):
                return "mixed"
        return "pure"

    def comm_of(k: int, y: int) -> str:
        if C0 is None:
            return "unk"
        return "new" if C["comm"][ego.slice_of(y)][k] != C0 else "old"

    prow = []
    for k in new_idx:
        y = first_year.get(k, t0)
        prow.append({"ci": ci, "topic": int(k), "role": "new", "trans": -1, "year": int(y), "type": _T["type"][k],
                     "comm": comm_of(int(k), y), "deg": "low" if is_low(int(k)) else "high",
                     "carrier": carrier(int(k), y), "deg_s0": float(deg0[k])})
    # ------- totals (the concept_core formulas)
    if C0 is not None and M > 0:
        isnew = np.array([C["comm"][ego.slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx], bool)
        NOV = float(np.mean(isnew))
        dg = deg0[pool]
        E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float("nan")
        NOV_res = NOV - E
    else:
        isnew = np.zeros(M, bool)
        NOV = E = NOV_res = float("nan")
    out.update({"M": M, "n1": n1, "NOV": NOV, "E": E, "NOV_res": NOV_res, "C0_defined": int(C0 is not None),
                "new_edge_rate": (M / float(len(early_years))) / (n1 + 1)})
    for r, inw in zip(prow, isnew):   # per-partner weights: parts = sums of weights over the class's rows
        r["w_ner"] = 1.0 / (len(early_years) * (n1 + 1))
        r["w_nov"] = float((inw - E) / M) if np.isfinite(NOV_res) else float("nan")
        r["w_ch"] = 0.0
    trans = []
    for a, b in (("W1", "W2"), ("W2", "W3")):
        u = int((NB[a] | NB[b]).sum())
        trans.append((a, b, u))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        jac = [(NB[a] & NB[b]).sum() / u if u else float("nan") for a, b, u in trans]
        out["edge_persistence"] = float(np.nanmean(jac))
    out["churn"] = 1 - out["edge_persistence"]
    # ------- parts
    for ax, cl in AXES.items():
        lab = np.array([r[ax] for r in prow], dtype=object) if prow else np.array([], dtype=object)
        for X in cl:
            m = lab == X
            mx = int(m.sum())
            out[f"m_{ax}_{X}"] = mx
            out[f"ner_{ax}_{X}"] = (mx / float(len(early_years))) / (n1 + 1)
            if ax in NOV_AXES:
                if np.isfinite(NOV_res):
                    out[f"nov_{ax}_{X}"] = float(np.sum(isnew[m] - E) / M)
                    out[f"NOVX_{ax}_{X}"] = float(isnew[m].mean()) if mx else float("nan")
                else:
                    out[f"nov_{ax}_{X}"] = out[f"NOVX_{ax}_{X}"] = float("nan")
    # class-specific nulls E_X on the pool (type, deg) and null shares
    if C0 is not None and len(pool) and deg0[pool].sum() > 0:
        pt = _T["type"][pool]
        pl = np.array([is_low(int(k)) for k in pool])
        dg = deg0[pool]
        outside = comm0[pool] != C0
        for ax, masks in (("type", {X: pt == X for X in AXES["type"]}),
                          ("deg", {"low": pl, "high": ~pl})):
            for X, mk in masks.items():
                w = dg[mk].sum()
                EX = dg[mk & outside].sum() / w if w > 0 else float("nan")
                out[f"Enull_{ax}_{X}"] = EX
                out[f"poolshare_{ax}_{X}"] = float(w / dg.sum())
                out[f"novnull_{ax}_{X}"] = out[f"NOVX_{ax}_{X}"] - EX if np.isfinite(EX) else float("nan")
        for X in AXES["carrier"]:
            out[f"novnull_carrier_{X}"] = out[f"NOVX_carrier_{X}"] - E
    else:
        for ax in ("type", "deg"):
            for X in AXES[ax]:
                out[f"Enull_{ax}_{X}"] = out[f"poolshare_{ax}_{X}"] = out[f"novnull_{ax}_{X}"] = float("nan")
        for X in AXES["carrier"]:
            out[f"novnull_carrier_{X}"] = float("nan")
    # churn parts
    T = sum(1 for _, _, u in trans if u)
    acc = {f"{r}_{ax}_{X}": 0.0 for r in ("chd", "cha") for ax, cl in AXES.items() for X in cl}
    acc["chd_all"] = acc["cha_all"] = 0.0
    wy = {"W1": t0, "W2": t0 + 1, "W3": t0 + 2}
    for ti, (a, b, u) in enumerate(trans):
        if not u:
            continue
        for role, S, wsrc in (("drop", NB[a] & ~NB[b], a), ("add", NB[b] & ~NB[a], b)):
            key = "chd" if role == "drop" else "cha"
            y = wy[wsrc]
            for k in np.nonzero(S)[0]:
                k = int(k)
                r = {"ci": ci, "topic": k, "role": role, "trans": ti, "year": y, "type": _T["type"][k],
                     "comm": comm_of(k, y), "deg": "low" if is_low(k) else "high", "carrier": carrier(k, y),
                     "deg_s0": float(deg0[k]), "w_ner": 0.0, "w_nov": 0.0, "w_ch": 1.0 / (u * T)}
                prow.append(r)
                for ax in AXES:
                    acc[f"{key}_{ax}_{r[ax]}"] += 1.0 / (u * T)
                acc[f"{key}_all"] += 1.0 / (u * T)
    if T == 0:
        acc = {k: float("nan") for k in acc}
    out.update(acc)
    # ------- bridging papers (early home papers introducing >= 1 new-community new partner in its first year)
    newc = {(r["topic"], r["year"]) for r in prow if r["role"] == "new" and r["comm"] == "new"}
    brows = []
    for y, tp, w in papers:
        if t0 <= y <= t0 + 2:
            br = any((k, y) in newc for k in tp)
            brows.append({"ci": ci, "year": int(y), "work_id": int(w), "bridging": bool(br), "n_topics": len(tp),
                          "has_offhome_topic": bool(any((not SELF[k]) and fcode[k] not in hcodes for k in tp))})
    out["bridging_share_home"] = float(np.mean([b["bridging"] for b in brows])) if brows else float("nan")
    out["n_bridging"] = int(sum(b["bridging"] for b in brows))
    return out, prow, brows


def retest_core(ci: int, name: str, aliases: list[str], t0: int, rows: list, hcodes: set[int]) -> dict:
    """Static later-window HOME build: the same concept_core with t0' = t0+3 (PRE = t0..t0+2, W1..W3 = t0+3..t0+5)."""
    import ego
    works = [(y, tp) for y, tp, v, _ in rows if v in hcodes]
    out = {"ci": ci, "n_home_later": int(sum(1 for y, _ in works if t0 + 3 <= y <= t0 + 5))}
    try:
        r = ego.concept_core(name, aliases, t0 + 3, works, 0, 0, compute_btw=False)
        for k in ("new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence", "M"):
            out[f"{k}__later"] = float(r[k])
    except (ValueError, IndexError, ZeroDivisionError) as e:
        out["error"] = repr(e)[:200]
    return out


def run_chunk(k: int, jobs: list, mode: str) -> tuple[int, list, list, list, float]:
    t = time.time()
    C, P, B = [], [], []
    for j in jobs:
        try:
            if mode == "retest":
                C.append(retest_core(*j))
            else:
                c, p, b = home_partners(*j)
                C.append(c); P += p; B += b
        except (ValueError, IndexError, ZeroDivisionError, KeyError) as e:
            C.append({"ci": j[0], "error": repr(e)[:200]})
    return k, C, P, B, time.time() - t


# ----------------------------------------------------------------------------- jobs (Exp10 s7_ego.jobs_*, + work_id)
def load_frame():
    fr = pd.read_csv(E11.parents[2] / "round-2/experiment-5/src/frame_concepts.csv")
    return fr


def jobs_exp5(source: str = "early") -> list:
    fr = load_frame()
    if source == "early":   # EXP8 frame_matches_early (t0-3..t0+2): the Exp10 source
        em = read_parts(E8 / "data/frame_matches_early", columns=["ci", "year", "topics", "vfield", "work_id"])
    else:                   # Exp11 frame_matches_long (t0-3..t0+10): for the later-window retest
        em = read_parts(E11 / "data/frame_matches_long", columns=["ci", "year", "topics", "vfield", "work_id"])
    em = em[em.ci.isin(set(fr.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist(),
                       d.work_id.astype(np.int64).tolist())) for ci, d in em.groupby("ci")}
    jobs = []
    for r in fr.itertuples():
        al = [a for a in str(r.aliases_used).split("|") if a and a != "nan"]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def jobs_cohort() -> list:
    cf = pd.read_csv(E10 / "data/cohort_candidates.csv")
    lex = pd.read_parquet(E10 / "inputs/lexicon_v1.parquet", columns=["aliases_used"])
    em = pd.read_parquet(E10 / "data/passC_early.parquet", columns=["ci", "year", "topics", "vfield", "tagstate", "work_id"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist(),
                       d.work_id.astype(np.int64).tolist())) for ci, d in em.groupby("ci")}
    jobs = []
    for r in cf.itertuples():
        al = [a for a in str(lex.aliases_used.iat[r.ci]).split("|") if a and a not in ("nan", "None")]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True, choices=["exp5", "cohort", "retest"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    logger = setup_logger(f"partners_home_{a.frame}{a.tag}")
    t0 = time.time()
    jobs = jobs_cohort() if a.frame == "cohort" else jobs_exp5("long" if a.frame == "retest" else "early")
    if a.limit:
        jobs = jobs[:a.limit]
    chunks = [jobs[i:i + a.chunk] for i in range(0, len(jobs), a.chunk)]
    logger.info(f"{a.frame}: {len(jobs)} concepts in {len(chunks)} chunks, workers {a.workers} "
                f"(jobs built in {time.time()-t0:.0f}s)")
    C, P, B = [None] * len(chunks), [None] * len(chunks), [None] * len(chunks)
    done = 0
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_chunk, k, ch, a.frame) for k, ch in enumerate(chunks)]
        for i, fu in enumerate(as_completed(futs)):
            k, c, p, b, dt = fu.result()
            C[k], P[k], B[k] = c, p, b
            done += len(c)
            if (i + 1) % 10 == 0 or i + 1 == len(futs):
                el = time.time() - t0
                logger.info(f"chunk {i+1}/{len(futs)} ({done}) {el/60:.1f} min; {dt/len(c):.3f} s/concept/worker")
    comp = pd.DataFrame([r for c in C for r in c])
    tag = f"{a.frame}{a.tag}"
    comp.to_parquet(DATA / f"partner_home_components_{tag}.parquet", index=False)
    if a.frame != "retest":
        rows = pd.DataFrame([r for p in P for r in p])
        outd = DATA / f"partner_home_rows_{tag}"
        outd.mkdir(exist_ok=True)
        for old in outd.glob("part_*.parquet"):
            old.unlink()
        for j, s in enumerate(range(0, max(len(rows), 1), 1_000_000)):
            rows.iloc[s:s + 1_000_000].to_parquet(outd / f"part_{j+1:03d}.parquet", index=False)
        pd.DataFrame([r for b in B for r in b]).to_parquet(DATA / f"bridging_home_papers_{tag}.parquet", index=False)
        logger.info(f"{tag}: {len(comp)} concepts, {len(rows)} partner rows, errors {int(comp.get('error', pd.Series(dtype=str)).notna().sum())}")
    logger.info(f"done in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
