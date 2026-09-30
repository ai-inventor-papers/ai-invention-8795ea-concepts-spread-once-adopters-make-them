#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers (different code paths from method.py / screen.py):
closed-form numpy ridge, manual rank-Spearman, IRLS logistic + Mann-Whitney AUC, math.lgamma rarefaction recomputed
from the raw S2 late-window records, lstsq OLS for M1. Placebo (shuffled A*_h) and positive control (leaky feature)
check that the Delta-rho test is neither vacuous nor powerless. Writes audit/rederive_out.json."""
from __future__ import annotations

import gzip
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
B5 = ["B_logvol", "B_growth", "B_offhome", "B_entropy", "B_nfields"]


def ranks(x):
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x))
    xs = x[order]
    i = 0
    while i < len(x):  # average ranks for ties
        j = i
        while j + 1 < len(x) and xs[j + 1] == xs[i]:
            j += 1
        r[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    return r


def spear(a, b):
    ra, rb = ranks(np.asarray(a, float)), ranks(np.asarray(b, float))
    ra, rb = ra - ra.mean(), rb - rb.mean()
    return float((ra * rb).sum() / math.sqrt((ra ** 2).sum() * (rb ** 2).sum()))


def prep(Xtr, Xte):
    med = np.array([np.median(c[np.isfinite(c)]) if np.isfinite(c).any() else 0 for c in Xtr.T])
    Xtr = np.where(np.isfinite(Xtr), Xtr, med); Xte = np.where(np.isfinite(Xte), Xte, med)
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd = np.where(sd > 0, sd, 1.0)
    return (Xtr - mu) / sd, (Xte - mu) / sd


def ridge_oof(X, y, g, alpha=1.0):
    oof = np.zeros(len(y))
    for gg in np.unique(g):
        te = g == gg
        A, B = prep(X[~te], X[te])
        ytr = y[~te]
        ym = ytr.mean()
        w = np.linalg.solve(A.T @ A + alpha * np.eye(A.shape[1]), A.T @ (ytr - ym))
        oof[te] = ym + B @ w
    return oof


def logit_oof(X, y, g, C=1.0):
    oof = np.zeros(len(y))
    for gg in np.unique(g):
        te = g == gg
        A, B = prep(X[~te], X[te])
        A1 = np.hstack([np.ones((len(A), 1)), A]); B1 = np.hstack([np.ones((len(B), 1)), B])
        w = np.zeros(A1.shape[1]); ytr = y[~te]
        pen = np.eye(A1.shape[1]) / C; pen[0, 0] = 0
        for _ in range(100):  # IRLS / Newton on the L2-penalised log-likelihood
            p = 1 / (1 + np.exp(-A1 @ w))
            grad = A1.T @ (ytr - p) - pen @ w
            H = A1.T @ (A1 * (p * (1 - p))[:, None]) + pen
            step = np.linalg.solve(H, grad); w += step
            if np.abs(step).max() < 1e-10:
                break
        oof[te] = 1 / (1 + np.exp(-B1 @ w))
    return oof


def auc(y, p):
    pos, neg = p[y == 1], p[y == 0]
    return float(((pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()) / (len(pos) * len(neg)))


def membership(fos):
    fos = fos or []
    cats = sorted({f["category"] for f in fos if f.get("source") == "s2-fos-model"}) or sorted({f["category"] for f in fos})
    return {c: 1 / len(cats) for c in cats} if cats else None


def rarefy(counts, m):
    N = sum(counts)
    if N < m:
        return float("nan")
    lc = lambda n, k: math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return sum(1 - (math.exp(lc(N - n, m) - lc(N, m)) if N - n >= m else 0) for n in counts if n > 0)


def main():
    D = pd.read_csv(RES / "screen_table.csv")
    sr = json.loads((RES / "screen_result.json").read_text())
    out = {}
    # 1. O2r recomputed from raw S2 late-window records
    diffs = []
    for _, r in D.iterrows():
        raw = json.loads(gzip.decompress((RES / "concepts" / "".join(ch if ch.isalnum() else "_" for ch in r["concept"].lower()).strip("_") / "s2_raw.json.gz").read_bytes()))
        mass = {}
        for p in raw["late"]:
            m = membership(p.get("s2FieldsOfStudy"))
            for k, v in (m or {}).items():
                mass[k] = mass.get(k, 0) + v
        thin = (raw.get("total_late") or len(raw["late"])) / max(len(raw["late"]), 1)
        diffs.append(rarefy([v * thin for v in mass.values()], 30) - r["O2r"])
    out["O2r_max_abs_diff_vs_raw"] = float(np.nanmax(np.abs(diffs)))
    # 2. headline Delta-rho (LOGO ridge B5 vs B5 + A*_h)
    X = np.column_stack([D[B5].values, D["A_h_missing"].values]).astype(float)
    y = D["O2r"].values.astype(float); g = D["dev_group"].values
    oB = ridge_oof(X, y, g); oBC = ridge_oof(np.column_stack([X, D["A_h"].values]), y, g)
    rB, rBC = spear(oB, y), spear(oBC, y)
    rng = np.random.default_rng(1)
    bs = [spear(oBC[i], y[i]) - spear(oB[i], y[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(2000))]
    out["delta_rho"] = {"rederived": rBC - rB, "rho_B": rB, "rho_BC": rBC, "ci90": [float(np.percentile(bs, 5)), float(np.percentile(bs, 95))],
                        "reported": sr["delta_rho"], "reported_rho_B": sr["rho_B"], "reported_ci90": sr["ci90"]}
    # 3. placebo: shuffled A*_h (the test must fail) and positive control (leaky feature must pass)
    plc = []
    for s in range(200):
        perm = np.random.default_rng(100 + s).permutation(len(y))
        plc.append(spear(ridge_oof(np.column_stack([X, D["A_h"].values[perm]]), y, g), y) - rB)
    plc = np.array(plc)
    leak = y + np.random.default_rng(7).normal(0, 0.5 * y.std(), len(y))
    oL = ridge_oof(np.column_stack([X, leak]), y, g)
    bsl = [spear(oL[i], y[i]) - spear(oB[i], y[i]) for i in (rng.integers(0, len(y), len(y)) for _ in range(2000))]
    ladder = {}
    for k in (0.1, 0.25, 0.5, 1.0):  # power ladder: how strong must a feature be to pass the delta clause?
        lk = y + np.random.default_rng(7).normal(0, k * y.std(), len(y))
        ok_ = ridge_oof(np.column_stack([X, lk]), y, g)
        bb = [spear(ok_[i], y[i]) - spear(oB[i], y[i]) for i in (np.random.default_rng(3).integers(0, len(y), len(y)) for _ in range(1000))]
        ladder[f"noise_sd_{k}"] = {"spearman_feature_O2r": spear(lk, y), "delta": spear(ok_, y) - rB,
                                   "ci90_low": float(np.percentile(bb, 5))}
    out["positive_control_ladder"] = ladder
    out["placebo_shuffled_A_h"] = {"mean_delta": float(plc.mean()), "share_passing_rule_delta_ge_0.10": float((plc >= 0.10).mean())}
    out["positive_control_leaky"] = {"delta": spear(oL, y) - rB, "ci90_low": float(np.percentile(bsl, 5)),
                                     "passes_delta_clause": bool(spear(oL, y) - rB >= 0.10 and np.percentile(bsl, 5) > 0)}
    # 4. size correlations
    out["size_corr"] = {"vol": spear(D["A_h"].values, D["B_logvol"].values), "growth": spear(D["A_h"].values, D["B_growth"].values),
                        "reported": sr["size_corr"]}
    # 5. O1 Delta-AUC (IRLS logistic)
    o1 = D["O1"].values.astype(int)
    out["delta_auc_O1"] = {"rederived": auc(o1, logit_oof(np.column_stack([X, D["A_h"].values]), o1, g)) - auc(o1, logit_oof(X, o1, g)),
                           "reported": sr["delta_auc_O1"]["delta"]}
    # 6. M1 via lstsq
    F = pd.read_csv(RES / "features.csv")
    m = F["raw_LOR_sampled"].notna() & F["bg_LOR"].notna()
    a, b = F.loc[m, "raw_LOR_sampled"].values, F.loc[m, "bg_LOR"].values
    A = np.column_stack([np.ones(len(b)), b]); coef, *_ = np.linalg.lstsq(A, a, rcond=None)
    res = a - A @ coef
    out["M1"] = {"R2": float(1 - (res ** 2).sum() / ((a - a.mean()) ** 2).sum()), "reported": sr["M1"]["R2"],
                 "bg_positive_share": float((b > 0).mean())}
    # 7. field-level Delta-AUC (IRLS logistic, pooled OOF)
    FL = pd.read_csv(RES / "field_outcomes.csv").merge(pd.read_csv(RES / "field_features.csv"), on=["concept", "field"], how="left")
    bgj = FL["bg_LOR_j"].values.astype(float)
    XB = np.column_stack([FL[["log_n_j_early", "growth_j", "share_j"]].values, bgj, (~np.isfinite(bgj)).astype(float)])
    XC = np.column_stack([XB, FL[["rho_star", "has_data"]].values.astype(float)])
    yf = FL["R_j"].values.astype(int); gf = FL["dev_group"].values
    out["field_level"] = {"rederived_delta_auc": auc(yf, logit_oof(XC, yf, gf)) - auc(yf, logit_oof(XB, yf, gf)),
                          "n_units": int(len(FL)), "reported": sr["field_level"]["delta"]}
    (ROOT / "audit" / "rederive_out.json").write_text(json.dumps(out, indent=1, default=float))
    print(json.dumps(out, indent=1, default=float))


if __name__ == "__main__":
    main()
