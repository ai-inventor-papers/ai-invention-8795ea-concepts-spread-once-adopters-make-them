#!/usr/bin/env python3
"""T7 independent audit: re-derive the held-out pooled dAUC, the per-group signs and the H3 partial rho from the
output tables (episode_features.csv + episodes.csv + concept tables + frozen_spec.json) with SEPARATE code
(own leave-concept-out propensity, sklearn lbfgs L2 logistic instead of the pipeline's Newton-IRLS, own Mann-Whitney AUC, own rank residualisation),
and compare with results/h1_heldout.json and results/h3_results.json (tolerance 1e-6).
Writes audit.json (with results/checks.json merged in)."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import RES, ROOT, jdump


def auc_mw(y: np.ndarray, s: np.ndarray) -> float:
    r = rankdata(s)
    n1 = y.sum()
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def lbfgs_l2(X: np.ndarray, y: np.ndarray, C: float) -> np.ndarray:
    """sklearn lbfgs (tol 1e-10) -- a different optimiser from the pipeline's Newton-IRLS; returns [b0, w]."""
    from sklearn.linear_model import LogisticRegression
    m = LogisticRegression(C=C, solver="lbfgs", tol=1e-10, max_iter=20000).fit(X, y)
    return np.concatenate([m.intercept_, m.coef_[0]])


def pj(df: pd.DataFrame, m: float, win: int) -> np.ndarray:
    ss = np.where(df.split.str.startswith("HELDOUT"), "HELDOUT", df.split)
    out = np.zeros(len(df))
    R = df.R.to_numpy(float)
    for i in range(len(df)):
        same = (ss == ss[i]) & (df.field.to_numpy() == df.field.iat[i])
        mu = np.nanmean(R[ss == ss[i]])
        k = same & (np.abs(df.t0.to_numpy() - df.t0.iat[i]) <= win) & (df.ci.to_numpy() != df.ci.iat[i]) & ~np.isnan(R)
        out[i] = (R[k].sum() + m * mu) / (k.sum() + m)
    return out


def design(df, cols, sc):
    return np.nan_to_num(np.column_stack([(df[c].to_numpy(float) - sc[c][0]) / (sc[c][1] or 1.0) for c in cols]))


def partial_rho(x, y, Zc):
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Zc).all(1)
    rx, ry = rankdata(x[ok]), rankdata(y[ok])
    RZ = np.column_stack([np.ones(ok.sum())] + [rankdata(c) for c in Zc[ok].T])
    bx = np.linalg.solve(RZ.T @ RZ, RZ.T @ rx)
    by = np.linalg.solve(RZ.T @ RZ, RZ.T @ ry)
    ex, ey = rx - RZ @ bx, ry - RZ @ by
    return float((ex * ey).sum() / math.sqrt((ex ** 2).sum() * (ey ** 2).sum()))


def main() -> None:
    spec = json.loads((ROOT / "frozen_spec.json").read_text())
    sc, X0, X1, C = spec["standardisation"], spec["X0"], spec["X1"], spec["C"]
    F = pd.read_csv(ROOT / "episode_features.csv")
    ep = pd.read_csv(ROOT / "episodes.csv")
    F = F.drop(columns=[c for c in ("R",) if c in F]).merge(ep[["ci", "field", "R"]], on=["ci", "field"])
    F["P_j"] = pj(F, spec["P_j"]["pseudo_count"], spec["P_j"]["window"])
    dev = F[F.split == "DEV"]
    ho = F[F.split.str.startswith("HELDOUT")]
    yd, yh = dev.R.to_numpy(float), ho.R.to_numpy(float)
    w0 = lbfgs_l2(design(dev, X0, sc), yd, C)
    w1 = lbfgs_l2(design(dev, X1, sc), yd, C)
    s0 = np.column_stack([np.ones(len(ho)), design(ho, X0, sc)]) @ w0
    s1 = np.column_stack([np.ones(len(ho)), design(ho, X1, sc)]) @ w1
    d_pooled = auc_mw(yh, s1) - auc_mw(yh, s0)
    per = {}
    for g in sorted(ho.group.unique()):
        m = (ho.group == g).to_numpy()
        per[g] = auc_mw(yh[m], s1[m]) - auc_mw(yh[m], s0[m]) if 0 < yh[m].sum() < m.sum() else math.nan
    h1 = json.loads((RES / "h1_heldout.json").read_text())
    rep_pooled = h1["primary"]["dauc"]
    rep_per = {g: v["dauc"] for g, v in h1["primary"]["per_group"].items()}
    # H3
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    co = pd.read_csv(ROOT / "concept_outcomes.csv")
    cf = pd.read_csv(ROOT / "concept_features_basic.csv")
    d = fc[fc.split.str.startswith("HELDOUT")][["ci"]].merge(co, on="ci").merge(cf, on="ci", suffixes=("", "_cf"))
    a, b = spec["O2r_resid"]["a"], spec["O2r_resid"]["b"]
    d["res"] = d.O2r_m30 - (a + b * np.log(d.N_outcome.clip(lower=1)))
    d = d.dropna(subset=["res"])
    Zc = d[["logvol", "growth_c", "offhome_share", "entropy", "reach"]].to_numpy(float)
    h3 = json.loads((RES / "h3_results.json").read_text())
    h3a = {v: partial_rho(d[v].to_numpy(float), d.res.to_numpy(float), Zc) for v in ("G", "G_A", "G_btw")}
    h3r = {v: h3[v]["partial_rho"] for v in ("G", "G_A", "G_btw")}
    tol = 1e-6
    res = {"heldout_pooled_dauc": {"audit": d_pooled, "reported": rep_pooled, "match": abs(d_pooled - rep_pooled) < tol},
           "heldout_per_group": {g: {"audit": per.get(g), "reported": rep_per.get(g),
                                     "sign_match": bool(np.sign(per.get(g, np.nan)) == np.sign(rep_per.get(g, np.nan))),
                                     "match": bool(abs(per.get(g, np.nan) - rep_per.get(g, np.nan)) < tol)}
                                 for g in rep_per if rep_per[g] is not None},
           "H3_partial_rho": {v: {"audit": h3a[v], "reported": h3r[v], "match": abs(h3a[v] - h3r[v]) < tol} for v in h3a},
           "tolerance": tol, "method": "separate sklearn-lbfgs L2 logistic + Mann-Whitney AUC + own P_j(-c) + own rank "
                                       "residualisation"}
    res["all_match"] = bool(res["heldout_pooled_dauc"]["match"] and all(v["match"] for v in res["H3_partial_rho"].values())
                            and all(v["sign_match"] for v in res["heldout_per_group"].values()))
    out = {"T7_independent_audit": res}
    ck = RES / "checks.json"
    if ck.exists():
        out.update(json.loads(ck.read_text()))
    bb = json.loads((RES / "backbones.json").read_text())
    out["backbone_recompute_check"] = {"spearman_S0_vs_frozen": bb["check_spearman_S0_recomputed_vs_frozen"],
                                       "pass_ge_0.9": bb["check_pass"]}
    out["api_audit"] = "NOT DONE: OpenAlex API pool below plan floor (results/deviations.json: openalex_api_skipped)"
    jdump(out, ROOT / "audit.json")
    print(json.dumps(res, indent=1)[:3000])


if __name__ == "__main__":
    main()
