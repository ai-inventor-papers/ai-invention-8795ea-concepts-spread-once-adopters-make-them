#!/usr/bin/env python3
"""Outcome reliability (rel_y) for O2r_m50, run AFTER the S1b seal.

Outcome-window (t0+6..t0+8; COH1517 t0 = 2017: t0+5..t0+7) venue-field counts of TAG-grounded papers:
  EXP5 bodies  EXP5 scan/agg_counts.parquet (tagstate == 1)
  COH1517      EXP10 passC_pre_agg + sealed parts (tagstate == 1), the EXP10 build_outcomes inputs
Check: rarefied richness at m = 50 recomputed from these counts == the stored O2r_m50.
Split-half: 100 multivariate-hypergeometric halves of the outcome papers; exact rarefied richness at m = 25 on each
half (concepts with >= 50 outcome papers); Spearman across concepts; Fisher-mean; Spearman-Brown.
'conservative, m = 25 halves'. Adds results/reliability.json = reliability_x.json + outcome block."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import DATA, DATA_IN, EXP5, RES, jdump, setup_logger
from outc import rarefied_richness

logger = setup_logger("s4b_outcome_rel")
Y0 = 1995


def counts_exp5(fr: pd.DataFrame) -> dict:
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(fr.ci)) & (ag.vfield >= 1)]
    t0 = fr.set_index("ci").t0
    ag = ag.assign(t0=t0.loc[ag.ci].to_numpy())
    ag = ag[(ag.year >= ag.t0 + 6) & (ag.year <= ag.t0 + 8)]
    out = {}
    for ci, g in ag.groupby("ci"):
        v = np.zeros(27)
        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))
        out[int(ci)] = v[1:27]
    return out


def counts_cohort(coh: pd.DataFrame) -> dict:
    pre = pd.read_parquet(DATA_IN / "passC_pre_agg.parquet")
    sealed = pd.concat([pd.read_parquet(p) for p in sorted((DATA_IN / "sealed/parts").glob("sealed_*.parquet"))],
                       ignore_index=True)
    agg = pd.concat([pre, sealed], ignore_index=True)
    agg = agg[(agg.tagstate == 1) & agg.ci.isin(set(coh.ci)) & (agg.vfield >= 1)]
    t0 = coh.set_index("ci").t0
    agg = agg.assign(t0=t0.loc[agg.ci].to_numpy())
    a = np.where(agg.t0 == 2017, 5, 6)
    agg = agg[(agg.year >= agg.t0 + a) & (agg.year <= agg.t0 + a + 2)]
    out = {}
    for ci, g in agg.groupby("ci"):
        v = np.zeros(27)
        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))
        out[int(ci)] = v[1:27]
    return out


def main() -> None:
    cv = pd.read_parquet(DATA / "clean_variants.parquet", columns=["frame", "ci", "body", "n_home_early"])
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci", "t0", "O2r_m50"])
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci", "t0", "O2r_m50"])
    ce = counts_exp5(fe[fe.ci.isin(cv[cv.frame == "exp5"].ci)])
    cc = counts_cohort(ac[ac.ci.isin(cv[cv.frame == "cohort"].ci)])
    rows = []
    for frame, tab, cnt in (("exp5", fe, ce), ("cohort", ac, cc)):
        tab = tab.set_index("ci")
        for ci in cv[cv.frame == frame].ci:
            v = cnt.get(int(ci), np.zeros(26))
            rows.append({"frame": frame, "ci": int(ci), "N_out": float(v.sum()),
                         "O2r_m50_recomputed": rarefied_richness([int(round(c)) for c in v], 50),
                         "O2r_m50": float(tab.at[ci, "O2r_m50"]), "vec": np.rint(v).astype(np.int64)})
    df = pd.DataFrame(rows).merge(cv, on=["frame", "ci"])
    both = df.O2r_m50.notna() & df.O2r_m50_recomputed.notna()
    md = float(np.max(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]))) if both.any() else math.nan
    agree = float(np.mean(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]) < 1e-9)) if both.any() else math.nan
    nan_mism = int((df.O2r_m50.isna() ^ df.O2r_m50_recomputed.isna()).sum())
    logger.info(f"O2r_m50 recomputation: max diff {md:.3g}; share exact {agree:.4f}; NaN mismatch {nan_mism}")
    rng = np.random.default_rng(20260937)
    elig = df[(df.N_out >= 50) & df.O2r_m50.notna()].reset_index(drop=True)
    S = 100
    A = np.full((S, len(elig)), np.nan)
    B = np.full((S, len(elig)), np.nan)
    for i, v in enumerate(elig.vec):
        v = v[v > 0]
        n = int(v.sum())
        for s in range(S):
            a = rng.multivariate_hypergeometric(v, n // 2)
            A[s, i] = rarefied_richness(a, 25)
            B[s, i] = rarefied_richness(v - a, 25)

    def sb(mask):
        rs = []
        for s in range(S):
            ok = mask & np.isfinite(A[s]) & np.isfinite(B[s])
            if ok.sum() < 20:
                continue
            rs.append(np.corrcoef(rankdata(A[s, ok]), rankdata(B[s, ok]))[0, 1])
        if not rs:
            return {"r_half": None, "SB": None, "n": int(mask.sum())}
        r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))
        return {"r_half": r, "SB": 2 * r / (1 + r), "n": int(mask.sum())}
    out = {"variable": "O2r_m50", "flag": "conservative, m = 25 halves (rarefied richness at 25 on each half of the "
                                          "outcome-window papers; multivariate hypergeometric thinning; 100 splits)",
           "recompute_check": {"max_abs_diff": md, "share_exact": agree, "nan_mismatch": nan_mism,
                               "n_compared": int(both.sum())},
           "eligible_min_outcome_papers": 50, "pooled": sb(np.ones(len(elig), bool))}
    for bd in ("DEV", "OLDHO", "COH1014", "COH1517"):
        out[bd] = sb((elig.body == bd).to_numpy())
    # bootstrap CI (concepts)
    bs = []
    for _ in range(200):
        idx = rng.integers(0, len(elig), len(elig))
        rs = [np.corrcoef(rankdata(A[s, idx]), rankdata(B[s, idx]))[0, 1] for s in range(10)
              if np.all(np.isfinite(A[s, idx])) and np.all(np.isfinite(B[s, idx]))]
        if rs:
            r = math.tanh(np.mean(np.arctanh(rs)))
            bs.append(2 * r / (1 + r))
    out["pooled"]["SB_ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else None
    out["pooled"]["SB_boot_sd"] = float(np.std(bs)) if bs else None
    logger.info(f"outcome reliability: {out['pooled']}")
    relx = json.loads((RES / "reliability_x.json").read_text())
    relx["outcome"] = {"O2r_m50": out, "O2r_resid": "O2r_resid = O2r_m50 - (a + b logvol): logvol is an early-window "
                                                    "covariate, so its reliability equals that of O2r_m50 up to the "
                                                    "shared variance; the O2r_m50 value is used for both"}
    jdump(relx, RES / "reliability.json")


if __name__ == "__main__":
    main()
