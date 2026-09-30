#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers through a DIFFERENT code path than eval.py.

- Own L2 logistic regression (scipy L-BFGS on the explicit objective C*sum(logloss) + 0.5*||w||^2, unpenalised
  intercept), own z-scoring and training-fold median imputation, own LOGO loop, own rank-based (Mann-Whitney) AUC.
- Reads raw inputs: iteration-1 exp4 field_outcomes.csv / features.csv and this workspace's results/union_episodes.csv
  (never the aggregated metrics), then compares with eval_out.json.
- Placebo checks: permuted R labels (delta-AUC must sit at 0 and the 'CI>0' criterion must fail), and a node-label
  permutation null for the union panel recomputed with the own solver.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
ITER1 = Path(os.environ.get("AII_ITER1", HERE.parent.parent.parent / "round-1" / "."))
E4 = ITER1 / "experiment-4/src"
GROUPS = ["CS", "Eng", "BGM", "Med"]


def auc_mw(y: np.ndarray, p: np.ndarray) -> float:
    r = rankdata(p)
    n1 = y.sum()
    n0 = len(y) - n1
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def fit_l2(X: np.ndarray, y: np.ndarray, C: float = 1.0) -> np.ndarray:
    Xa = np.hstack([np.ones((len(X), 1)), X])

    def f(w):
        z = Xa @ w
        ll = np.sum(np.logaddexp(0, z) - y * z)
        g = Xa.T @ (1 / (1 + np.exp(-z)) - y)
        return C * ll + 0.5 * w[1:] @ w[1:], C * g + np.r_[0, w[1:]]
    return minimize(f, np.zeros(Xa.shape[1]), jac=True, method="L-BFGS-B",
                    options={"gtol": 1e-10, "ftol": 1e-14, "maxiter": 5000}).x


def logo(df: pd.DataFrame, cols: list[str], y: np.ndarray) -> np.ndarray:
    out = np.full(len(df), np.nan)
    g = df["group"].to_numpy()
    for lg in GROUPS:
        te = g == lg
        tr = ~te
        if not te.any():
            continue
        X = df[cols].to_numpy(float).copy()
        med = np.nanmedian(X[tr], axis=0)
        med = np.where(np.isfinite(med), med, 0.0)
        X = np.where(np.isnan(X), med, X)
        mu, sd = X[tr].mean(0), X[tr].std(0)
        sd[sd == 0] = 1.0
        Z = (X - mu) / sd
        w = fit_l2(Z[tr], y[tr])
        out[te] = 1 / (1 + np.exp(-(w[0] + Z[te] @ w[1:])))
    return out


def delta(df, base, y, g="gateway_j"):
    return auc_mw(y, logo(df, base + [g], y)) - auc_mw(y, logo(df, base, y))


def main() -> None:
    ev = json.loads((HERE / "eval_out.json").read_text())
    ma, meta = ev["metrics_agg"], ev["metadata"]
    out = {}
    # 1. exp4 reproduction from the raw iteration-1 file
    fr = pd.read_csv(E4 / "field_outcomes.csv")
    y4 = fr["R"].to_numpy(float)
    BF = ["log_n_W3", "growth_j", "share_W3"]
    out["exp4_gateway_delta"] = {"audit": delta(fr, BF, y4), "reported_iter1": 0.10254}
    out["exp4_size_controlled_delta"] = {"audit": delta(fr, BF + ["log_field_size"], y4), "reported_iter1": 0.10222}
    # 2. union / new-episodes M2 delta from the harmonised panel written by eval.py
    u = pd.read_csv(HERE / "results" / "union_episodes.csv")
    M2 = ["b_logn", "b_growth", "b_share", "src_exp1", "src_exp3", "b5_logvol", "b5_growth", "b5_offhome",
          "b5_entropy", "b5_reach", "log_field_size", "phi_home_j", "density_j"]
    yu = u["R"].to_numpy(float)
    out["union_M2_delta"] = {"audit": delta(u, M2, yu), "eval": ma.get("A_union_M2_delta_auc")}
    ne = u[u["source"] != "exp4"].reset_index(drop=True)
    out["new_eps_M2_delta"] = {"audit": delta(ne, M2, ne["R"].to_numpy(float)), "eval": ma.get("A_new_eps_M2_delta_auc")}
    M0 = ["b_logn", "b_growth", "b_share", "src_exp1", "src_exp3"]
    out["union_M0_delta"] = {"audit": delta(u, M0, yu), "eval": ma.get("A_union_M0_delta_auc")}
    e4 = u[u["source"] == "exp4"].reset_index(drop=True)
    M2e4 = [c for c in M2 if not c.startswith("src_")]
    out["exp4_M2_delta"] = {"audit": delta(e4, M2e4, e4["R"].to_numpy(float)), "eval": ma.get("A_exp4_M2_delta_auc")}
    # 3. pooled AUC recomputed from the per-episode OOF predictions stored in eval_out.json (rank AUC)
    exs = ev["datasets"][0]["examples"]
    yy = np.array([float(e["output"]) for e in exs])
    pb = np.array([float(e["predict_M2"]) for e in exs])
    pc = np.array([float(e["predict_M2_plus_gateway"]) for e in exs])
    out["union_from_stored_oof"] = {"auc_M2": auc_mw(yy, pb), "auc_M2_g": auc_mw(yy, pc),
                                    "delta": auc_mw(yy, pc) - auc_mw(yy, pb),
                                    "eval_auc_base": ma.get("A_union_M2_auc_base")}
    # 4. placebo: permuted R labels -> delta must centre on 0; the CI>0 criterion must fail
    rng = np.random.default_rng(99)
    sh = []
    for _ in range(int(os.environ.get("AUDIT_N_SHUF", 60))):
        ys = rng.permutation(yu)
        sh.append(delta(u, M2, ys))
    sh = np.array(sh)
    out["placebo_shuffled_R_union"] = {"n": len(sh), "mean": float(sh.mean()), "p2.5": float(np.percentile(sh, 2.5)),
                                       "p97.5": float(np.percentile(sh, 97.5)),
                                       "ci95_excludes_0_(should_be_false)": bool(np.percentile(sh, 2.5) > 0)}
    # exp4 lead on shuffled labels
    sh4 = np.array([delta(fr, BF, rng.permutation(y4)) for _ in range(60)])
    out["placebo_shuffled_R_exp4_M0"] = {"mean": float(sh4.mean()), "p95": float(np.percentile(sh4, 95)),
                                         "real_0.10254_above_p95": bool(0.10254 > np.percentile(sh4, 95))}
    # 5. node-label permutation null (own solver) on the union panel, M2
    bb = json.loads((E4 / "field_backbone.json").read_text())
    idx = {f: i for i, f in enumerate(bb["fields"])}
    gate = np.array(bb["gateway_eig"])
    one = u["key"].isin(idx).to_numpy()
    uu = u[one].reset_index(drop=True)
    kk = uu["key"].map(idx).to_numpy()
    real = delta(uu, M2, uu["R"].to_numpy(float))
    base_auc = auc_mw(uu["R"].to_numpy(float), logo(uu, M2, uu["R"].to_numpy(float)))
    nl = []
    for _ in range(int(os.environ.get("AUDIT_N_PERM", 100))):
        d = uu.copy()
        d["g_p"] = rng.permutation(gate)[kk]
        nl.append(auc_mw(d["R"].to_numpy(float), logo(d, M2 + ["g_p"], d["R"].to_numpy(float))) - base_auc)
    nl = np.array(nl)
    out["C2_union_one_to_one_rows"] = {"n_rows": int(len(uu)), "real": real, "null_p95": float(np.percentile(nl, 95)),
                                       "real_percentile": float(np.mean(nl < real) * 100),
                                       "eval_real_percentile_all_rows": ma.get("C2_label_perm_union_M2_real_percentile")}
    out["verdict_eval"] = meta["verdict"]
    (HERE / "results" / "audit_out.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    sys.exit(main())
