#!/usr/bin/env python3
"""T7 post-scoring audit on an INDEPENDENT code path (own average ranks via argsort, own OLS via normal equations,
sklearn roc_auc_score, sklearn LogisticRegression for the frozen binary models).

  (a) per-unit psp of the top-3 O2r_resid indicators == heldout_unit_results.csv (to 1e-6)
  (b) held-out AUCs of the frozen B5 and B5 + x logistic models (top-1 of each binary outcome) re-derived with sklearn
  (c) shuffled-outcome control: 20 within-unit permutations of O2r_resid -> mean pooled |psp| < 0.03
  (d) planted positive control: x* = z(O2r_resid residual) + noise at rho ~ 0.1 is detected (pooled CI > 0)
Writes results/audit.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from common import DATA, HELD_GROUPS, RES, SEED, jdump
from indicators import B5


def avg_rank(v: np.ndarray) -> np.ndarray:
    o = np.argsort(v, kind="mergesort")
    r = np.empty(len(v))
    sv = v[o]
    i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and sv[j + 1] == sv[i]:
            j += 1
        r[o[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return r


def own_psp(x, y, B, t0) -> float:
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1)
    x, y, B, t0 = x[ok], y[ok], B[ok], t0[ok]
    cols = [np.ones(len(x))] + [avg_rank(B[:, j]) for j in range(B.shape[1])]
    for u in np.unique(t0)[1:]:
        cols.append((t0 == u).astype(float))
    Z = np.column_stack(cols)
    ZtZ = Z.T @ Z

    def res(v):
        return v - Z @ np.linalg.solve(ZtZ + 1e-12 * np.eye(len(ZtZ)), Z.T @ v)
    a, b = res(avg_rank(x)), res(avg_rank(y))
    return float((a @ b) / np.sqrt((a @ a) * (b @ b)))


def main() -> None:
    A = pd.read_parquet(DATA / "analysis_table.parquet")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    ur = pd.read_csv(RES / "heldout_unit_results.csv")
    out = {}
    # (a)
    diffs = []
    top3 = [d["indicator"] for d in spec["top10"]["O2r_resid"][:3]]
    for ind in top3:
        for u in HELD_GROUPS:
            d = A[A.unit == u]
            mine = own_psp(d[ind].to_numpy(float), d.O2r_resid.to_numpy(float), d[B5].to_numpy(float), d.t0.to_numpy())
            ref = ur[(ur.indicator == ind) & (ur.outcome == "O2r_resid") & (ur.unit == u)].rho.iloc[0]
            diffs.append({"indicator": ind, "unit": u, "audit": mine, "pipeline": float(ref), "absdiff": abs(mine - ref)})
    out["a_psp_top3_O2r_resid"] = {"max_abs_diff": max(r["absdiff"] for r in diffs), "rows": diffs,
                                   "pass": bool(max(r["absdiff"] for r in diffs) < 1e-6)}
    # (b)
    D = A[A.split == "DEV"]
    rows = []
    for o in ("O1b", "O3", "O5", "O5_WW"):
        if o not in spec["top10"] or not spec["top10"][o]:
            continue
        ind = spec["top10"][o][0]["indicator"]
        bs = spec["b5_spec"]
        from design import apply_design
        t0s = spec["learned"].get(o, {}).get("t0_std")

        def base(d):
            X = apply_design(d, bs)
            return np.c_[X, (d.t0.to_numpy(float) - t0s[0]) / t0s[1]] if (o in ("O5", "O5_WW") and t0s) else X
        okD = D[o].notna() & D[ind].notna()
        xD = D.loc[okD, ind].to_numpy(float)
        mu, sd = xD.mean(), xD.std() or 1.0
        yD = D.loc[okD, o].to_numpy(float)
        # sklearn C=1 L2 == our lam=1 objective (intercept unpenalised in liblinear? use lbfgs, which penalises no intercept)
        m0 = LogisticRegression(C=1.0, max_iter=20000, tol=1e-12).fit(base(D[okD]), yD)
        m1 = LogisticRegression(C=1.0, max_iter=20000, tol=1e-12).fit(np.c_[base(D[okD]), (xD - mu) / sd], yD)
        for u in HELD_GROUPS + ["COH_DEVHOME", "COH_OTHER"]:
            d = A[(A.unit == u) & A[o].notna() & A[ind].notna()]
            y = d[o].to_numpy(float)
            if y.sum() < 20 or (1 - y).sum() < 20:
                continue
            a0 = roc_auc_score(y, m0.predict_proba(base(d))[:, 1])
            a1 = roc_auc_score(y, m1.predict_proba(np.c_[base(d), (d[ind].to_numpy(float) - mu) / sd])[:, 1])
            ref = ur[(ur.indicator == ind) & (ur.outcome == o) & (ur.unit == u)]
            rows.append({"outcome": o, "indicator": ind, "unit": u, "audit_dauc": a1 - a0,
                         "pipeline_dauc": float(ref.dauc.iloc[0]) if len(ref) else None,
                         "audit_auc_base": a0, "pipeline_auc_base": float(ref.auc_base.iloc[0]) if len(ref) else None})
    md = [abs(r["audit_dauc"] - r["pipeline_dauc"]) for r in rows if r["pipeline_dauc"] is not None]
    out["b_heldout_auc_sklearn"] = {"rows": rows, "max_abs_diff_dauc": max(md) if md else None,
                                    "pass": bool(md and max(md) < 1e-4)}
    # (c) shuffled-outcome control and (d) planted positive control
    from rq1stats import dersimonian_laird, psp_boot
    rng = np.random.default_rng(SEED)
    ind = top3[0]
    pooled_abs = []
    for p in range(20):
        zs, ses = [], []
        for u in HELD_GROUPS:
            d = A[A.unit == u]
            y = rng.permutation(d.O2r_resid.to_numpy(float))
            r = psp_boot(d[ind].to_numpy(float), y, d[B5].to_numpy(float), None, 100, SEED + p)
            zs.append(r["z"]); ses.append(r["se_z"])
        pooled_abs.append(abs(np.tanh(dersimonian_laird(zs, ses)["b"])))
    out["c_shuffled_outcome"] = {"indicator": ind, "mean_pooled_abs_psp": float(np.mean(pooled_abs)),
                                 "pass": bool(np.mean(pooled_abs) < 0.03)}
    zs, ses = [], []
    for u in HELD_GROUPS:
        d = A[A.unit == u]
        y = d.O2r_resid.to_numpy(float)
        ok = np.isfinite(y)
        # plant on the part of rank(y) not explained by rank(B5) (what psp | B5 measures): true psp ~ 0.10
        Bd = d[B5].to_numpy(float)
        okb = ok & np.all(np.isfinite(Bd), 1)
        e = np.zeros(len(y))
        Z = np.c_[np.ones(okb.sum()), np.apply_along_axis(avg_rank, 0, Bd[okb])]
        ry = avg_rank(y[okb])
        res = ry - Z @ np.linalg.lstsq(Z, ry, rcond=None)[0]
        e[okb] = res / res.std()
        x = 0.1 * e + np.sqrt(1 - 0.01) * rng.normal(size=len(y))
        r = psp_boot(x, y, d[B5].to_numpy(float), None, 200, SEED)
        zs.append(r["z"]); ses.append(r["se_z"])
    pl = dersimonian_laird(zs, ses)
    out["d_planted_positive"] = {"pooled": float(np.tanh(pl["b"])), "ci": [float(np.tanh(c)) for c in pl["ci"]],
                                 "pass": bool(pl["ci"][0] > 0)}
    out["all_pass"] = bool(all(v.get("pass", True) for v in out.values() if isinstance(v, dict)))
    jdump(out, RES / "audit.json")
    print(json.dumps({k: (v.get("pass") if isinstance(v, dict) else v) for k, v in out.items()}, indent=1))


if __name__ == "__main__":
    main()
