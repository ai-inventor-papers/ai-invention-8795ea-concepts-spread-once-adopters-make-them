#!/usr/bin/env python3
"""STEP 3: Exp7's D_rca_pers vs Research 2's D_rca_persist_k (DEV only).

D_rca_pers (Exp7 frozen_spec): U_j = RCA(t-3..t-1) > 1 AND RCA(t-6..t-4) > 1   (two 3-year window-aggregated RCAs)
D_rca_persist_k (Research 2 R1): U_j = entered or RCA > 1 in EACH of the k years before the risk year
Both are Hidalgo densities omega_k = sum_j U_j phi_jk / sum_j phi_jk over the frozen 26-field backbone.

Recipe check: rebuilding D_rca_1y (U = RCA_1y(t-1) > 1) from state_panel_dev.parquet must reproduce Exp7's risk-set
column (Spearman ~ 1) before the persist_k variants are trusted. Usage: python step3_drca.py"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr

from common import E7, E8, LOGS, RES, jdump, rel

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "step3_drca.log", rotation="30 MB", level="DEBUG")


def main() -> None:
    spec7 = json.loads((E7 / "results/frozen_spec.json").read_text())
    defs = spec7.get("covariates", {})
    phi = np.asarray(json.loads((E8 / "inputs/field_backbone.json").read_text())["phi"], float)
    cs = phi.sum(0)
    den = np.where(cs > 0, cs, 1)
    sp = pd.read_parquet(E7 / "results/state_panel_dev.parquet", columns=["ci", "field", "year", "rca_1y", "state"])
    cis = np.sort(sp.ci.unique())
    ci_pos = {c: i for i, c in enumerate(cis)}
    Y0, Y1 = int(sp.year.min()), int(sp.year.max())
    ny = Y1 - Y0 + 1
    R = np.zeros((len(cis), ny, 26), np.float32)
    S = np.zeros((len(cis), ny, 26), np.int8)
    ii = sp.ci.map(ci_pos).to_numpy()
    yy = (sp.year - Y0).to_numpy()
    ff = (sp.field - 11).to_numpy()
    R[ii, yy, ff] = sp.rca_1y.to_numpy()
    S[ii, yy, ff] = sp.state.to_numpy()
    del sp
    rs = pd.read_parquet(E7 / "results/risk_sets_exp5_minus_exp6_dev.parquet",
                         columns=["cidx", "t", "field", "D_rca_1y", "D_rca_w3", "D_rca_pers", "D_rca_cum", "entered"])
    rs = rs[rs.cidx.isin(ci_pos)].reset_index(drop=True)
    logger.info(f"risk-set rows (DEV): {len(rs):,}; concepts {rs.cidx.nunique():,}; panel years {Y0}-{Y1}")
    rows_i = rs.cidx.map(ci_pos).to_numpy()
    t_i = rs.t.to_numpy() - Y0
    f_i = rs.field.to_numpy() - 11

    def density(U: np.ndarray) -> np.ndarray:          # U [n_rows, 26] bool -> omega at the target field
        return (U.astype(np.float64) @ phi)[np.arange(len(U)), f_i] / den[f_i]

    def U_years(ks: range, kind: str) -> np.ndarray:
        out = np.ones((len(rs), 26), bool)
        for k in ks:
            y = t_i - k
            ok = y >= 0
            yc = np.clip(y, 0, ny - 1)
            if kind == "rca":
                u = R[rows_i, yc] > 1
            else:
                u = (R[rows_i, yc] > 1) | (S[rows_i, yc] > 0)
            u[~ok] = False
            out &= u
        return out

    res = {"definitions": {"D_rca_pers (Exp7 frozen_spec.covariates.D_rca_pers)": defs.get("D_rca_pers"),
                           "D_rca_persist_k (Research 2, research_report.md R1)":
                               "entered or RCA > 1 in each of t-k..t (predictor-side twin of Pinheiro 2022's Delta rule)",
                           "operationalisation_here": "k yearly checks over years t-k..t-1 before risk year t "
                                                      "(information set of the Exp7 predictors); 'entered' = state > 0 "
                                                      "in Exp7's state panel; RCA-only variant also reported"},
           "source": {"state_panel": rel(E7 / "results/state_panel_dev.parquet"),
                      "risk_sets": rel(E7 / "results/risk_sets_exp5_minus_exp6_dev.parquet"),
                      "phi": rel(E8 / "inputs/field_backbone.json")},
           "n_rows": int(len(rs)), "n_concepts": int(rs.cidx.nunique())}
    d1 = density(U_years(range(1, 2), "rca"))
    res["recipe_check_D_rca_1y_spearman"] = float(spearmanr(d1, rs.D_rca_1y)[0])
    logger.info(f"recipe check D_rca_1y rebuilt vs Exp7: rho={res['recipe_check_D_rca_1y_spearman']:.4f}")
    out = {}
    for k in (2, 3):
        for kind in ("entered_or_rca", "rca"):
            v = density(U_years(range(1, k + 1), kind))
            key = f"D_rca_persist_{k}_{kind}"
            out[key] = {"spearman_vs_D_rca_pers": float(spearmanr(v, rs.D_rca_pers)[0]),
                        "spearman_vs_D_rca_1y": float(spearmanr(v, rs.D_rca_1y)[0]),
                        "share_rows_nonzero": float((v > 0).mean()),
                        "share_rows_both_zero_with_pers": float(((v > 0) == (rs.D_rca_pers.to_numpy() > rs.D_rca_pers.min())).mean()),
                        "mean_entered": float(v[rs.entered.to_numpy() == 1].mean()), "mean_not_entered": float(v[rs.entered.to_numpy() == 0].mean())}
            rs[key] = v
    res["comparisons"] = out
    res["spearman_D_rca_pers_vs_D_rca_1y"] = float(spearmanr(rs.D_rca_pers, rs.D_rca_1y)[0])
    rmax = max(o["spearman_vs_D_rca_pers"] for o in out.values())
    res["verdict"] = "DIFFERENT" if rmax < 0.9 else "NESTED"
    res["verdict_reason"] = (
        "D_rca_pers requires RCA>1 in two window-aggregated 3-year blocks (t-3..t-1 and t-6..t-4), i.e. a 6-year "
        "horizon that tolerates single bad years; D_rca_persist_k requires the state in EACH single year t-k..t-1 and "
        "admits 'entered' presences below RCA 1. Neither set contains the other, so the constructs are not equivalent; "
        f"the maximum rank correlation on DEV candidate rows is {rmax:.3f}.")
    jdump(res, RES / "drca_persist_comparison.json")
    logger.info(f"STEP 3 verdict {res['verdict']}: {json.dumps(out)[:600]}")


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
