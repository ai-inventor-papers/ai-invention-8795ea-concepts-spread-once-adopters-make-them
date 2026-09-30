#!/usr/bin/env python3
"""Post-unseal audit with INDEPENDENT code (statsmodels OLS residuals, scipy ranks/hypergeometric, hand DL).

A1  primary OPEN_home psp (O2r_m50) at R2 and R3 re-derived with statsmodels (target |diff| < 1e-8)
A2  DL pooled estimate re-derived by hand from the per-group estimates / SEs in cohort_result.json
A3  O2r_m50 re-computed for 30 random cohort concepts straight from the sealed parts with scipy.stats.hypergeom
A4  within-group shuffled-outcome control (200 draws; 95th percentile of |psp|) with the independent psp
A5  planted-signal recovery (psp = 0.10) with the independent psp and a 1,000-draw bootstrap
Writes results/audit.json."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import hypergeom, rankdata

from common import DATA, RES, jdump, setup_logger
from ladder import rung_design

logger = setup_logger("audit")


def psp_sm(x, y, B, C) -> float:
    Z = sm.add_constant(np.c_[np.column_stack([rankdata(B[:, j]) for j in range(B.shape[1])]), C], has_constant="add")
    rx = sm.OLS(rankdata(x), Z).fit().resid
    ry = sm.OLS(rankdata(y), Z).fit().resid
    return float(np.corrcoef(rx, ry)[0, 1])


def design(df, rung, xcol, ycol):
    Bc, Cc = rung_design(df, rung)
    x, y = df[xcol].to_numpy(float), df[ycol].to_numpy(float)
    B, C = Bc.to_numpy(float), Cc.to_numpy(float)
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
    return x[ok], y[ok], B[ok], C[ok], df[ok]


def rarefy_indep(counts, m=50) -> float:
    counts = np.asarray([int(c) for c in counts if c > 0])
    N = counts.sum()
    if N < m:
        return math.nan
    return float(sum(1 - hypergeom(N, int(c), m).pmf(0) for c in counts))


@logger.catch(reraise=True)
def main() -> None:
    res = json.loads((RES / "cohort_result.json").read_text())
    spec = json.loads((RES / "frozen_spec.json").read_text())
    df = pd.read_parquet(DATA / "analysis_cohort.parquet")
    out: dict = {}
    a1 = {}
    for r in ("R2", "R3"):
        x, y, B, C, _ = design(df, r, "OPEN_home", "O2r_m50")
        v = psp_sm(x, y, B, C)
        ref = res["primary"][f"OPEN_home|O2r_m50|{r}"]["rho"]
        a1[r] = {"statsmodels": v, "pipeline": ref, "abs_diff": abs(v - ref), "pass": abs(v - ref) < 1e-8}
    out["A1_psp_rederivation"] = a1
    a2 = {}
    for key, g in res["groups"].items():
        b = np.array([g["groups"][k]["rho"] for k in ("CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC")], float)
        se = np.array([g["groups"][k]["se"] for k in ("CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC")], float)
        ok = np.isfinite(b) & np.isfinite(se) & (se > 0)
        b, se = b[ok], se[ok]
        w = 1 / se ** 2
        mf = np.sum(w * b) / np.sum(w)
        Q = np.sum(w * (b - mf) ** 2)
        k = len(b)
        tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w))) if k > 1 else 0.0
        ws = 1 / (se ** 2 + tau2)
        est = float(np.sum(ws * b) / np.sum(ws))
        a2[key] = {"hand": est, "pipeline": g["DL"]["b"], "abs_diff": abs(est - g["DL"]["b"])}
    out["A2_DL_rederivation"] = {"max_abs_diff": max(v["abs_diff"] for v in a2.values()), "items": a2}
    # A3 O2r_m50 from the sealed parts (independent code; grounding as frozen)
    sealed = pd.concat([pd.read_parquet(p) for p in sorted((DATA / "sealed/parts").glob("sealed_*.parquet"))])
    use_match = spec["outcome_grounding"] == "MATCH"
    rng = np.random.default_rng(3)
    pick = rng.choice(df.ci[np.isfinite(df.O2r_m50)].to_numpy(), size=min(30, int(np.isfinite(df.O2r_m50).sum())),
                      replace=False)
    diffs = []
    for ci in pick:
        t0 = int(df.t0[df.ci == ci].iat[0])
        sh = 1 if t0 == 2017 else 0
        d = sealed[(sealed.ci == ci) & (sealed.year >= t0 + 6 - sh) & (sealed.year <= t0 + 8 - sh) & (sealed.vfield > 0)]
        if not use_match:
            d = d[d.tagstate == 1]
        cnt = d.groupby("vfield").n.sum()
        v = rarefy_indep(cnt.to_numpy())
        diffs.append(abs(v - float(df.O2r_m50[df.ci == ci].iat[0])))
    out["A3_O2r_from_sealed"] = {"n": len(diffs), "max_abs_diff": float(np.nanmax(diffs)), "pass": float(np.nanmax(diffs)) < 1e-8}
    # A4 shuffled control
    x, y, B, C, d = design(df, "R2", "OPEN_home", "O2r_m50")
    g = d.agroup.to_numpy()
    r4 = np.random.default_rng(11)
    vals = []
    for _ in range(200):
        yp = y.copy()
        for gg in np.unique(g):
            m = g == gg
            yp[m] = r4.permutation(yp[m])
        vals.append(psp_sm(x, yp, B, C))
    vals = np.abs(vals)
    out["A4_shuffled"] = {"q95_abs_psp": float(np.percentile(vals, 95)), "mean_abs": float(vals.mean()),
                          "share_lt_0.05": float((vals < 0.05).mean())}
    # A5 planted
    Z = sm.add_constant(np.c_[np.column_stack([rankdata(B[:, j]) for j in range(B.shape[1])]), C], has_constant="add")
    rx = sm.OLS(rankdata(x), Z).fit().resid
    yp = y.copy()
    for gg in np.unique(g):
        m = g == gg
        yp[m] = r4.permutation(yp[m])
    zr = (rankdata(yp) - rankdata(yp).mean()) / rankdata(yp).std()
    yplant = zr + 0.10 / math.sqrt(1 - 0.01) * rx / rx.std()
    est = psp_sm(x, yplant, B, C)
    bs = []
    for _ in range(1000):
        i = r4.integers(0, len(x), len(x))
        Ci = C[i]
        bs.append(psp_sm(x[i], yplant[i], B[i], Ci[:, Ci.std(0) > 0]))
    out["A5_planted"] = {"target": 0.10, "estimate": est, "ci": [float(np.percentile(bs, 2.5)),
                                                                 float(np.percentile(bs, 97.5))],
                         "recovered_ci_gt0": bool(np.percentile(bs, 2.5) > 0)}
    out["all_rederivations_pass"] = bool(all(v["pass"] for v in a1.values()) and out["A3_O2r_from_sealed"]["pass"]
                                         and out["A2_DL_rederivation"]["max_abs_diff"] < 1e-10)
    jdump(out, RES / "audit.json")
    logger.info(f"audit: {json.dumps({k: v for k, v in out.items() if k != 'A2_DL_rederivation'})[:1500]}")


if __name__ == "__main__":
    main()
