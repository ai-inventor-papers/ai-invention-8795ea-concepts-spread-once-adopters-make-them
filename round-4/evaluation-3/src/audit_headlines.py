#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers through a DIFFERENT code path (no lib/, no vendor/ imports).

- partial Spearman: pandas ranks + statsmodels OLS residuals (instead of scipy rankdata + numpy lstsq in rq1stats)
- OPEN rebuilt from raw Exp8 analysis_table.parquet + the sealed DEV constants (instead of lib/data.py)
- D_vol_post rebuilt from raw frame_arrays.npz with a vectorised window sum (instead of the states() loop)
- DerSimonian-Laird written inline with analytic Fisher-z variances 1/(n-k-3)
- placebo: indicator shuffled within unit (20 draws) must NOT give a pooled CI excluding 0 more than ~5% of the time
Writes results/audit_headlines.json. Usage: python audit_headlines.py"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

WS = Path(__file__).resolve().parent
RUN = Path(_os.environ.get("AII_RUN_LOOP", str(WS.parents[2])))
E8 = RUN / "round-3/experiment-8/src"
RES = WS / "results"
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
UNITS6 = HELD4 + ["COH_DEVHOME", "COH_OTHER"]
COMP = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1, "edge_persistence": -1}


def psp(d: pd.DataFrame, x: str, y: str, unit: str, xvals=None):
    d = d[[x, y, "t0", "group"] + B5].copy()
    if xvals is not None:
        d[x] = xvals
    d = d.dropna()
    n = len(d)
    Z = pd.concat([d[B5].rank(), pd.get_dummies(d.t0.astype(int).astype(str), prefix="t", drop_first=True, dtype=float)], axis=1)
    if unit.startswith("COH"):
        Z = pd.concat([Z, pd.get_dummies(d.group.astype(str), prefix="g", drop_first=True, dtype=float)], axis=1)
    Z = sm.add_constant(Z, has_constant="add").astype(float)
    k = np.linalg.matrix_rank(Z.to_numpy())
    ex = sm.OLS(d[x].rank().to_numpy(), Z).fit().resid
    ey = sm.OLS(d[y].rank().to_numpy(), Z).fit().resid
    return float(np.corrcoef(ex, ey)[0, 1]), n, k


def dl(rs, ns, ks):
    z = np.arctanh(np.array(rs)); v = 1 / (np.array(ns) - np.array(ks) - 3)
    w = 1 / v; zf = (w * z).sum() / w.sum(); Q = (w * (z - zf) ** 2).sum(); c = w.sum() - (w ** 2).sum() / w.sum()
    t2 = max(0.0, (Q - (len(z) - 1)) / c); ws = 1 / (v + t2); m = (ws * z).sum() / ws.sum(); se = math.sqrt(1 / ws.sum())
    return {"est": math.tanh(m), "ci": [math.tanh(m - 1.96 * se), math.tanh(m + 1.96 * se)],
            "I2": max(0.0, (Q - (len(z) - 1)) / Q) if Q > 0 else 0.0}


def main() -> None:
    A = pd.read_parquet(E8 / "data/analysis_table.parquet")
    spec = json.loads((RES / "boundary_spec.json").read_text())["open_definition"]["dev_constants"]
    Zc = np.column_stack([COMP[c] * (A[c].to_numpy(float) - spec["mu"][c]) / spec["sd"][c] for c in COMP])
    cnt = np.isfinite(Zc).sum(1)
    with np.errstate(all="ignore"):
        A["OPEN_audit"] = np.where(cnt >= 4, np.nanmean(Zc, 1), np.nan)
    Bt = pd.read_parquet(RES / "b_table.parquet", columns=["ci", "OPEN", "D_vol_post", "D_vol_end"])
    M = A[["ci", "OPEN_audit", "home", "t0"]].merge(Bt, on="ci")
    out = {"OPEN_rebuild_max_abs_diff": float(np.nanmax(np.abs(M.OPEN_audit - M.OPEN))),
           "OPEN_rebuild_nan_pattern_equal": bool((M.OPEN_audit.isna() == M.OPEN.isna()).all())}
    # D_vol_post from raw arrays: off-home fields with >= 2 grounded papers summed over t0..t0+2
    z = np.load(E8 / "data/frame_arrays.npz")
    V, ci = z["V"], z["ci"]
    pos = {int(c): i for i, c in enumerate(ci)}
    dvp = []
    for r in M.itertuples(index=False):
        g = V[pos[int(r.ci)]][:, 1:]
        s = g[int(r.t0) - 1995:int(r.t0) - 1995 + 3].sum(0)
        home = [int(float(h)) - 11 for h in str(r.home).split(";") if h and h != "nan"]
        off = np.ones(26, bool); off[home] = False
        dvp.append(int(((s >= 2) & off).sum()))
    M["D_vol_post_audit"] = dvp
    out["D_vol_post_rebuild_share_equal"] = float((M.D_vol_post_audit == M.D_vol_post).mean())
    A = A.merge(M[["ci", "D_vol_post_audit"]], on="ci")
    # headline psp re-derivations
    port = pd.read_csv(E8 / "results/portability_table.csv")
    pg = pd.read_csv(RES / "per_group_table.csv")
    rows = {}
    for ind, o, x, units in (("M0_density_end", "O2r_m50", "M0_density_end", HELD4), ("D_vol_end", "O2r_m50", "D_vol_end", HELD4),
                             ("OPEN", "O2r_m50", "OPEN_audit", HELD4), ("OPEN", "O2r_m50", "OPEN_audit", UNITS6),
                             ("OPEN", "O2r_resid", "OPEN_audit", HELD4)):
        rs, ns, ks, du = [], [], [], []
        for u in units:
            r, n, k = psp(A[A.unit == u], x, o, u)
            rs.append(r); ns.append(n); ks.append(k)
            ref = port if ind != "OPEN" else pg
            rec = ref[(ref.indicator == ind) & (ref.outcome == o) & (ref.unit == u)].rho.iloc[0]
            du.append(abs(r - rec))
        rows[f"{ind}|{o}|DL{len(units)}"] = {"per_unit": dict(zip(units, np.round(rs, 4))), "max_unit_diff_vs_record": float(max(du)),
                                              "pooled_analytic": dl(rs, ns, ks)}
    out["psp"] = rows
    # B1 post-onset M0/D_vol: D_vol_post (audit build) pooled over units where defined
    rs, ns, ks = [], [], []
    for u in ["PHYS", "LIFEENV", "SOC"]:
        r, n, k = psp(A[A.unit == u], "D_vol_post_audit", "O2r_m50", u); rs.append(r); ns.append(n); ks.append(k)
    out["D_vol_post_O2r_m50_DL3_analytic"] = dl(rs, ns, ks)
    # placebo: shuffle OPEN within unit
    rng = np.random.default_rng(20260929)
    hits, ests = 0, []
    for _ in range(20):
        rs, ns, ks = [], [], []
        for u in HELD4:
            d = A[A.unit == u]
            r, n, k = psp(d, "OPEN_audit", "O2r_m50", u, xvals=rng.permutation(d.OPEN_audit.to_numpy()))
            rs.append(r); ns.append(n); ks.append(k)
        P = dl(rs, ns, ks); ests.append(P["est"]); hits += int(P["ci"][0] > 0 or P["ci"][1] < 0)
    out["placebo_shuffled_OPEN"] = {"n_draws": 20, "share_ci_excludes_0": hits / 20, "mean_est": float(np.mean(ests)),
                                    "max_abs_est": float(np.max(np.abs(ests)))}
    # spec-curve share and ledger re-count straight from the raw rows
    S = pd.read_csv(RES / "spec_curve_specs.csv")
    out["spec_share_ci_gt0_from_rows"] = float((S.DL4_lo > 0).mean())
    out["spec_median_from_rows"] = float(S.DL4_est.median())
    nd = pd.read_csv(RES / "spec_curve_null_DL4.csv")
    col = [c for c in nd.columns if "share" in c and "ci" in c][0]
    out["spec_null_share_col"] = col
    out["spec_p_from_null_rows"] = float((1 + (nd[col] >= out["spec_share_ci_gt0_from_rows"]).sum()) / (1 + len(nd)))
    L = pd.read_csv(RES / "claims_ledger_v3.csv")
    out["ledger_status_from_rows"] = L.status.value_counts().to_dict()
    (RES / "audit_headlines.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps(out, indent=1, default=float)[:4000])


if __name__ == "__main__":
    main()
