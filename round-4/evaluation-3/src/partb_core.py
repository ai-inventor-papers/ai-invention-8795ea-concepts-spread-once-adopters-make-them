#!/usr/bin/env python3
"""Part B core: GATE T0 (reproduce the Exp8 record), B1 post-onset re-score, B2 per-group table.

Usage: python partb_core.py [--stage t0|b1|b2|all] [--workers 12] [--mini]"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"          # 4-CPU box: one BLAS thread per process (the previous attempt died on thread exhaustion)

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger

from common import (B5, DEV_UNITS, E8, HELD4, LOGS, RES, SEED, UNITS6, assert_sealed, cat_for, dl, holm, jdump,
                    rel)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "partb_core.log", rotation="30 MB", level="DEBUG")

E8_SEED = 20260928
ALL10 = DEV_UNITS + UNITS6
G: dict = {}


def _init(extra_cols: list[str]) -> None:
    import warnings
    warnings.filterwarnings("ignore")
    sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
    A = pd.read_parquet(RES / "b_table.parquet") if (RES / "b_table.parquet").exists() else None
    if A is None:
        A = pd.read_parquet(E8 / "data/analysis_table.parquet")
    G["A"] = A


def unit_frame(A: pd.DataFrame, unit: str) -> pd.DataFrame:
    return A[A.unit == unit]


def job_boot(args):
    """Exp8 psp_boot on one (indicator, outcome, unit), optional extra ranked controls."""
    from rq1stats import psp_boot, spearman_raw
    ind, outcome, unit, nboot, seed, covs = args
    d = unit_frame(G["A"], unit)
    x = d[ind].to_numpy(float)
    y = d[outcome].to_numpy(float)
    r = psp_boot(x, y, d[B5 + list(covs)].to_numpy(float), cat_for(d.t0.to_numpy(), d.group.to_numpy(), unit),
                 nboot, seed)
    raw, _ = spearman_raw(x, y)
    return {"indicator": ind, "outcome": outcome, "unit": unit, "covs": "+".join(covs), "n": r["n"], "rho": r["rho"],
            "ci_lo": r["ci"][0], "ci_hi": r["ci"][1], "z": r.get("z"), "se_z": r.get("se_z"), "p": r["p"],
            "raw_rho": raw}


def job_paired(args):
    """Paired concept bootstrap of psp(full) and psp(post) with the same resample in every draw (B1 (c))."""
    from rq1stats import psp_point
    full, post, outcome, unit, nboot, seed = args
    d = unit_frame(G["A"], unit)
    cols = [full, post, outcome] + B5
    ok = np.all(np.isfinite(d[cols].to_numpy(float)), 1)
    cat = cat_for(d.t0.to_numpy(), d.group.to_numpy(), unit)[ok]
    d = d[ok]
    xf, xp, y, B = d[full].to_numpy(float), d[post].to_numpy(float), d[outcome].to_numpy(float), d[B5].to_numpy(float)
    n = len(y)
    kz = 1 + len(B5) + np.linalg.matrix_rank(cat) if cat.shape[1] else 1 + len(B5)
    ef, ep = psp_point(xf, y, B, cat), psp_point(xp, y, B, cat)
    rng = np.random.default_rng(seed)
    bf, bp = np.empty(nboot), np.empty(nboot)
    for b in range(nboot):
        i = rng.integers(0, n, n)
        bf[b] = psp_point(xf[i], y[i], B[i], cat[i])
        bp[b] = psp_point(xp[i], y[i], B[i], cat[i])
    return {"full": full, "post": post, "outcome": outcome, "unit": unit, "n": n, "k": int(kz), "est_full": ef,
            "est_post": ep, "boot_full": bf, "boot_post": bp}


def run_pool(fn, jobs, workers, label):
    t = time.time()
    out = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init, initargs=([],)) as ex:
        for i, r in enumerate(ex.map(fn, jobs, chunksize=1)):
            out.append(r)
            if (i + 1) % 20 == 0 or i + 1 == len(jobs):
                logger.info(f"{label}: {i+1}/{len(jobs)} ({time.time()-t:.0f}s)")
    return out


# ============================================================================= T0
def stage_t0(workers: int) -> dict:
    sys.path.insert(0, str(E8 / "lib"))
    from indicators import INDICATORS  # read-only import from Exp8 for the seed order of the portability table
    spec8 = json.loads((E8 / "results/frozen_spec.json").read_text())
    summ = json.loads((E8 / "results/heldout_summary.json").read_text())
    port = pd.read_csv(E8 / "results/portability_table.csv")
    targets = [("M0_density_end", "O2r_resid", "heldout_summary"), ("M0_density_end", "O2r_m50", "heldout_summary"),
               ("D_vol_end", "O2r_m50", "heldout_summary"), ("n_comm_W3", "O2r_m50", "heldout_summary"),
               ("ego_density_W3", "O2r_m50", "heldout_summary"), ("new_edge_rate", "O2r_m50", "portability_table")]
    jobs, meta = [], []
    for ind, o, src in targets:
        if src == "heldout_summary":
            inds = list(dict.fromkeys([d["indicator"] for d in spec8["top10"][o]] + spec8["union_top10"]))
            seed, nb = E8_SEED + 31 * inds.index(ind), 1000
        else:
            feats = INDICATORS + B5
            seed, nb = E8_SEED + 7 * feats.index(ind), 500
        for u in HELD4:
            jobs.append((ind, o, u, nb, seed, ()))
        meta.append((ind, o, src))
    res = pd.DataFrame(run_pool(job_boot, jobs, workers, "T0"))
    out = {"tolerance": 1e-3, "rows": []}
    rec_units = pd.read_csv(E8 / "results/heldout_unit_results.csv")
    for ind, o, src in meta:
        t = res[(res.indicator == ind) & (res.outcome == o)].set_index("unit").loc[HELD4]
        pl = dl(t.z.to_numpy(float), t.se_z.to_numpy(float) ** 2)
        if src == "heldout_summary":
            rec = [r for r in summ[o] if r["indicator"] == ind][0]
            rec_val, rec_key = rec["pooled"], f"{o}[indicator={ind}].pooled"
            ru = rec_units[(rec_units.indicator == ind) & (rec_units.outcome == o)].set_index("unit")
        else:
            ru = port[(port.indicator == ind) & (port.outcome == o)].set_index("unit")
            p2 = dl(ru.loc[HELD4].z.to_numpy(float), ru.loc[HELD4].se_z.to_numpy(float) ** 2)
            rec_val, rec_key = p2["est"], f"portability_table DL4 of z/se_z (= prereg P3 new_edge_rate pooled_psp)"
        unit_diff = float(np.max(np.abs(t.rho.to_numpy() - ru.loc[HELD4].rho.to_numpy())))
        out["rows"].append({"indicator": ind, "outcome": o, "record_source": src, "record_key": rec_key,
                            "record_pooled": rec_val, "rederived_pooled": pl["est"], "abs_diff": abs(pl["est"] - rec_val),
                            "rederived_ci": pl["ci"], "I2": pl["I2"], "max_unit_point_diff": unit_diff,
                            "pass": bool(abs(pl["est"] - rec_val) < 1e-3)})
        logger.info(f"T0 {ind}|{o}: record {rec_val:.4f} rederived {pl['est']:.4f} unit max diff {unit_diff:.2e}")
    out["readme_note"] = ("README table shows M0_density_end +0.375 (O2r_m50, 0.3745) while portability/heldout_summary "
                          "headline +0.377 is O2r_resid; both are reproduced here")
    out["gate_T0_pass"] = bool(all(r["pass"] for r in out["rows"]))
    jdump(out, RES / "gate_T0.json")
    return out


# ============================================================================= B1
def states(g: np.ndarray, home: list[int], min_n: int = 2):
    x = g[:, 1:]
    cum = np.cumsum(x, 0)
    entered = cum >= min_n
    offhome = np.ones(26, bool)
    for h in home:
        offhome[h - 11] = False
    return entered, offhome


def home_list(h) -> list[int]:
    return [int(float(x)) for x in str(h).split(";") if x and x != "nan"]


def build_b_table() -> pd.DataFrame:
    """Recompute D_vol_end / M0_density_end on full history (must equal Exp8) and on t0..t0+2 only; footprint."""
    A = pd.read_parquet(E8 / "data/analysis_table.parquet")
    z = np.load(E8 / "data/frame_arrays.npz")
    N, V, ci = z["N"].astype(float), z["V"].astype(float), z["ci"]
    pos = {int(c): i for i, c in enumerate(ci)}
    phi = np.asarray(json.loads((E8 / "inputs/field_backbone.json").read_text())["phi"], float)
    colsum = phi.sum(0)
    den = np.where(colsum > 0, colsum, 1)
    yi = lambda y: y - 1995
    rows = []
    for r in A[["ci", "t0", "home"]].itertuples(index=False):
        f = pos[int(r.ci)]
        t0 = int(r.t0)
        g = V[f]
        home = home_list(r.home)
        Ef, off = states(g, home)
        E_end = Ef[yi(t0 + 2)]
        cand = ~E_end & off
        m0 = float((phi[E_end].sum(0) / den)[cand].mean()) if cand.any() else np.nan
        gw = np.zeros_like(g)
        gw[yi(t0):yi(t0 + 2) + 1] = g[yi(t0):yi(t0 + 2) + 1]
        Ew, _ = states(gw, home)
        Ep = Ew[yi(t0 + 2)]
        candp = ~Ep & off
        m0p = float((phi[Ep].sum(0) / den)[candp].mean()) if candp.any() else np.nan
        dpre = int((Ef[yi(t0 - 1)] & off).sum())
        dend = int((E_end & off).sum())
        rows.append({"ci": int(r.ci), "D_vol_end_re": dend, "M0_density_end_re": m0, "D_vol_post": int((Ep & off).sum()),
                     "M0_density_post": m0p, "D_vol_pre": dpre, "footprint_share": dpre / max(dend, 1),
                     "log_pre_papers": float(np.log1p(N[f, yi(t0 - 3):yi(t0 - 1) + 1].sum()))})
    R = pd.DataFrame(rows)
    B = A.merge(R, on="ci", how="left")
    return B


def stage_b1(workers: int, nboot: int = 1000) -> dict:
    from scipy.stats import spearmanr
    spec = assert_sealed()
    from data import add_open
    t = time.time()
    B = build_b_table()
    B = add_open(B, spec)
    B.to_parquet(RES / "b_table.parquet", index=False)
    chk = {}
    for a, b in (("D_vol_end", "D_vol_end_re"), ("M0_density_end", "M0_density_end_re")):
        x, y = B[a].to_numpy(float), B[b].to_numpy(float)
        both_nan = np.isnan(x) & np.isnan(y)
        d = np.abs(x - y)
        chk[a] = {"max_abs_diff": float(np.nanmax(d)), "nan_pattern_equal": bool((np.isnan(x) == np.isnan(y)).all()),
                  "n": int(len(x)), "exact_lt_1e9": bool(np.nanmax(d) < 1e-9 and (np.isnan(x) == np.isnan(y)).all())}
    chk["share_post_differs"] = {
        "D_vol": float((B.D_vol_post != B.D_vol_end).mean()),
        "M0_density": float((~np.isclose(B.M0_density_post.fillna(-9), B.M0_density_end.fillna(-9))).mean())}
    logger.info(f"B1 recompute check {chk} ({time.time()-t:.0f}s)")
    assert chk["D_vol_end"]["exact_lt_1e9"] and chk["M0_density_end"]["exact_lt_1e9"], "B1 full-history recompute != Exp8"
    # --- jobs
    pairs = [("M0_density_end", "M0_density_post"), ("D_vol_end", "D_vol_post")]
    outs = ("O2r_m50", "O2r_resid")
    jobs = [(f, p, o, u, nboot, SEED + 11 * i + 101 * j) for i, (f, p) in enumerate(pairs) for j, o in enumerate(outs)
            for u in UNITS6]
    paired = run_pool(job_paired, jobs, workers, "B1 paired")
    jobs2 = [(ind, o, u, nboot, SEED + 7, ("D_vol_pre", "log_pre_papers")) for ind in ("M0_density_end", "D_vol_end")
             for o in outs for u in UNITS6]
    foot = pd.DataFrame(run_pool(job_boot, jobs2, workers, "B1 footprint-controlled"))
    res = {"recompute_check": chk, "verdict_rule": spec["B1"]["verdict_rule"], "cells": [], "pooled": {},
           "footprint_controlled": [], "spearman": {}}
    for r in paired:
        bf, bp = r["boot_full"], r["boot_post"]
        okb = np.isfinite(bf) & np.isfinite(bp)       # draws where psp is undefined (x rank-collinear with B5) dropped
        if okb.sum() < 2:
            bf = bp = np.array([np.nan, np.nan])
        else:
            bf, bp = bf[okb], bp[okb]
        res["cells"].append({k: r[k] for k in ("full", "post", "outcome", "unit", "n", "k", "est_full", "est_post")} |
                            {"ci_full": np.percentile(bf, [2.5, 97.5]).tolist(),
                             "ci_post": np.percentile(bp, [2.5, 97.5]).tolist(),
                             "diff": r["est_full"] - r["est_post"],
                             "ci_diff": np.percentile(bf - bp, [2.5, 97.5]).tolist(),
                             "atten": 1 - r["est_post"] / r["est_full"] if r["est_full"] else np.nan,
                             "ci_atten": np.percentile(1 - bp / bf, [2.5, 97.5]).tolist(),
                             "n_boot_valid": int(okb.sum())})
    for units, tag in ((HELD4, "DL4"), (UNITS6, "DL6")):
        for f, p in pairs:
            for o in outs:
                cs0 = [r for r in paired if r["full"] == f and r["outcome"] == o and r["unit"] in units]
                # a unit whose post-onset psp is undefined in >= 50% of draws (post indicator rank-collinear with the
                # B5 'reach' column) is excluded from BOTH the full and post pools, so the pair stays comparable
                cs = [c for c in cs0 if np.mean(np.isfinite(c["boot_post"]) & np.isfinite(c["boot_full"])) >= 0.5]
                excluded = [c["unit"] for c in cs0 if c not in cs]
                v = np.array([1 / (c["n"] - c["k"] - 3) for c in cs])
                zf = np.arctanh([c["est_full"] for c in cs]); zp = np.arctanh([c["est_post"] for c in cs])
                Pf, Pp = dl(zf, v), dl(zp, v)
                Bf = np.arctanh(np.clip(np.column_stack([c["boot_full"] for c in cs]), -.999999, .999999))
                Bp = np.arctanh(np.clip(np.column_stack([c["boot_post"] for c in cs]), -.999999, .999999))
                okd = np.all(np.isfinite(Bf), 1) & np.all(np.isfinite(Bp), 1)   # keep draws defined in every unit
                Bf, Bp = Bf[okd], Bp[okd]
                pf = np.array([dl(Bf[b], v)["est"] for b in range(len(Bf))])
                pp = np.array([dl(Bp[b], v)["est"] for b in range(len(Bp))])
                ci_post = np.percentile(pp, [2.5, 97.5]).tolist()
                ci_diff = np.percentile(pf - pp, [2.5, 97.5]).tolist()
                if ci_post[1] < 0.5 * Pf["est"]:
                    verdict = "MOST"
                elif ci_diff[0] <= 0 <= ci_diff[1]:
                    verdict = "LITTLE"
                else:
                    verdict = "PARTIAL"
                res["pooled"][f"{tag}|{f}|{o}"] = {
                    "psp_full": Pf["est"], "psp_full_ci_boot": np.percentile(pf, [2.5, 97.5]).tolist(),
                    "psp_full_ci_analytic": Pf["ci"], "psp_post": Pp["est"], "psp_post_ci_boot": ci_post,
                    "psp_post_ci_analytic": Pp["ci"], "I2_full": Pf["I2"], "I2_post": Pp["I2"],
                    "diff": Pf["est"] - Pp["est"], "diff_ci": ci_diff,
                    "attenuation": 1 - Pp["est"] / Pf["est"], "attenuation_ci": np.percentile(1 - pp / pf, [2.5, 97.5]).tolist(),
                    "n_pos_post": Pp["n_pos"], "k": Pp["k"], "verdict": verdict,
                    "n_boot_draws_valid_all_units": int(okd.sum()), "units_pooled": [c["unit"] for c in cs],
                    "units_excluded_undefined_post": excluded}
    for (ind, o), t in foot.groupby(["indicator", "outcome"]):
        for units, tag in ((HELD4, "DL4"), (UNITS6, "DL6")):
            tt = t.set_index("unit").loc[units]
            P = dl(tt.z.to_numpy(float), tt.se_z.to_numpy(float) ** 2)
            res["footprint_controlled"].append({"indicator": ind, "outcome": o, "pool": tag, "controls": "B5+D_vol_pre+log_pre_papers",
                                                "pooled": P["est"], "ci": P["ci"], "I2": P["I2"],
                                                "per_unit": dict(zip(tt.index, tt.rho.round(4)))})
    H = B[B.unit.isin(UNITS6)]
    res["collinearity_post_vs_B5_reach"] = {
        "note": "D_vol_post counts off-home fields entered from t0..t0+2 papers only; B5 'reach' is built from the same "
                "window, so the two are near rank-identical and psp(D_vol_post | B5) rests on the few discordant ranks",
        "spearman_D_vol_post_reach_by_unit": {u: float(spearmanr(g.D_vol_post, g.reach, nan_policy="omit")[0])
                                              for u, g in B.groupby("unit")},
        "spearman_D_vol_end_reach_by_unit": {u: float(spearmanr(g.D_vol_end, g.reach, nan_policy="omit")[0])
                                             for u, g in B.groupby("unit")},
        "spearman_M0_post_reach_by_unit": {u: float(spearmanr(g.M0_density_post, g.reach, nan_policy="omit")[0])
                                           for u, g in B.groupby("unit")}}
    res["spearman"] = {
        "D_vol_post_vs_D_vol_end_heldout6": float(spearmanr(H.D_vol_post, H.D_vol_end, nan_policy="omit")[0]),
        "M0_post_vs_M0_end_heldout6": float(spearmanr(H.M0_density_post, H.M0_density_end, nan_policy="omit")[0]),
        "footprint_share_vs_O2r_m50_heldout6": float(spearmanr(H.footprint_share, H.O2r_m50, nan_policy="omit")[0]),
        "per_unit_footprint_share_vs_O2r_m50": {u: float(spearmanr(g.footprint_share, g.O2r_m50, nan_policy="omit")[0])
                                                 for u, g in H.groupby("unit")},
        "median_footprint_share_heldout6": float(H.footprint_share.median()),
        "share_with_any_pre_onset_entry": float((H.D_vol_pre > 0).mean())}
    jdump(res, RES / "post_onset_rescore.json")
    logger.info("B1 pooled: " + "; ".join(f"{k}: full {v['psp_full']:.3f} post {v['psp_post']:.3f} att {v['attenuation']:.2f} {v['verdict']}"
                                          for k, v in res["pooled"].items()))
    return res


# ============================================================================= B2
B2_ROWS = ["M0_density_end", "D_vol_end", "CONTACT_REACH", "n_comm_W3", "NOV", "RETENTION_RATIO_early", "ego_density_W3",
           "log_offhome_volume", "D_ratio", "D_rare", "participation", "NOV_res", "entropy", "edge_persistence",
           "new_edge_rate"]
NEW_ROWS = ["M0_density_post", "D_vol_post", "OPEN", "OPEN_PC1"]


def stage_b2(workers: int, nboot: int = 1000) -> None:
    assert_sealed()
    from rq1stats import psp_point
    port = pd.read_csv(E8 / "results/portability_table.csv")
    outs = ("O2r_m50", "O2r_resid")
    jobs = [(ind, o, u, nboot, SEED + 13 * i, ()) for i, ind in enumerate(NEW_ROWS) for o in outs for u in ALL10]
    cache = RES / "b2_new_rows.csv"
    if cache.exists():
        new = pd.read_csv(cache)
        logger.info(f"B2 new rows reused from {cache.name}")
    else:
        new = pd.DataFrame(run_pool(job_boot, jobs, workers, "B2 new rows"))
        new["source"] = f"computed_here_B{nboot}"
        new.to_csv(cache, index=False)
    old = port[port.indicator.isin(B2_ROWS) & port.outcome.isin(outs)][
        ["indicator", "unit", "outcome", "n", "rho", "ci_lo", "ci_hi", "raw_rho", "z", "se_z", "p"]].copy()
    old["source"] = "Exp8 portability_table.csv (B=500)"
    tab = pd.concat([old, new[old.columns]], ignore_index=True)
    tab["ci_includes_0"] = (tab.ci_lo <= 0) & (tab.ci_hi >= 0)
    tab["unit_type"] = tab.unit.map(lambda u: "SELECTION_DATA(DEV)" if u in DEV_UNITS else
                                    ("HELDOUT" if u in HELD4 else "COHORT"))
    # 10% cross-check of existing cells (point estimates are deterministic)
    B = pd.read_parquet(RES / "b_table.parquet")
    rng = np.random.default_rng(SEED)
    sel = old.sample(frac=0.10, random_state=SEED)
    diffs = []
    for r in sel.itertuples():
        d = B[B.unit == r.unit]
        x, y, Bm = d[r.indicator].to_numpy(float), d[r.outcome].to_numpy(float), d[B5].to_numpy(float)
        cat = cat_for(d.t0.to_numpy(), d.group.to_numpy(), r.unit)
        ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(Bm), 1)
        if ok.sum() < 20 or np.unique(x[ok]).size < 3:
            continue
        diffs.append(abs(psp_point(x[ok], y[ok], Bm[ok], cat[ok]) - r.rho))
    pooled = []
    for (ind, o), t in tab.groupby(["indicator", "outcome"]):
        t = t.set_index("unit")
        for units, tag in ((HELD4, "DL4"), (UNITS6, "DL6")):
            tt = t.reindex(units).dropna(subset=["z"])
            P = dl(tt.z.to_numpy(float), tt.se_z.to_numpy(float) ** 2)
            if not P["k"]:          # entropy is a B5 member: psp | B5 undefined, raw Spearman only
                P = {"est": np.nan, "ci": [np.nan, np.nan], "I2": np.nan, "tau2": np.nan, "Q": np.nan, "Q_p": np.nan,
                     "pi": [np.nan, np.nan], "k": 0}
            pooled.append({"indicator": ind, "outcome": o, "pool": tag, "pooled": P.get("est"), "ci_lo": P["ci"][0],
                           "ci_hi": P["ci"][1], "I2": P["I2"], "tau2": P["tau2"], "Q": P["Q"], "Q_p": P["Q_p"],
                           "pi_lo": P["pi"][0], "pi_hi": P["pi"][1], "k": P["k"],
                           "sign_pos_6": int((t.reindex(UNITS6).rho > 0).sum()),
                           "n_ci_includes_0_6": int(t.reindex(UNITS6).ci_includes_0.fillna(True).astype(bool).sum())})
    pooled = pd.DataFrame(pooled)
    for tag in ("DL4", "DL6"):
        for o in outs:
            m = (pooled.pool == tag) & (pooled.outcome == o)
            pp = [2 * __import__("scipy").stats.norm.sf(abs(np.arctanh(r.pooled) / ((np.arctanh(r.ci_hi) - np.arctanh(r.ci_lo)) / 3.92)))
                  if np.isfinite(r.pooled) else np.nan for r in pooled[m].itertuples()]
            pooled.loc[m, "holm_p"] = holm(pp)
    tab.to_csv(RES / "per_group_table.csv", index=False)
    pooled.to_csv(RES / "per_group_pooled.csv", index=False)
    # robustness block: sensitivities_pooled.json rows + CONTACT_REACH without intersection-born
    sens = json.loads((E8 / "results/sensitivities_pooled.json").read_text())
    sh = pd.read_csv(E8 / "results/sensitivities_heldout.csv")
    ni = sh[(sh.indicator == "CONTACT_REACH") & sh.sensitivity.astype(str).str.contains("intersect", case=False)] \
        if "sensitivity" in sh.columns else sh.iloc[0:0]
    jdump({"cross_check_10pct": {"n_cells": len(diffs), "max_abs_diff": float(max(diffs)) if diffs else None},
           "sensitivities_pooled_verbatim": sens,
           "contact_reach_no_intersection_rows": ni.to_dict("records"),
           "unit_order": ALL10}, RES / "per_group_extra.json")
    logger.info(f"B2 table {tab.shape}; cross-check max diff {max(diffs) if diffs else None}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--nboot", type=int, default=1000)
    a = ap.parse_args()
    assert_sealed()
    if a.stage in ("t0", "all"):
        r = stage_t0(a.workers)
        if not r["gate_T0_pass"]:
            logger.error("GATE T0 FAILED - Part B stopped")
            sys.exit(2)
    if a.stage in ("b1", "all"):
        stage_b1(a.workers, a.nboot)
    if a.stage in ("b2", "all"):
        stage_b2(a.workers, a.nboot)


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
