#!/usr/bin/env python3
"""Secondary: the frozen EXP8 learned models (no refit) applied to the cohort.

Builds the 58-column EXP8 indicator matrix for the cohort with ported code (lib/featport.py for families E/F/G/FR/S,
s7_ego.py 'full' build = EXP8 family-A settings) and validates the port on EXP5 concepts against EXP8
results/indicator_matrix.parquet. Models: linear_all_O2r_m50 / linear_all_O2r_resid (ElasticNet) and
linear_all_O3 (L1-logit) with their frozen B5 comparators; EBM_O4 is not evaluable (no O4).
Imputation at the frozen DEV medians (lib/design.py). A model is reported 'not evaluable' if > 20% of its
|standardised coefficient| mass sits on fully imputed features.
Usage: python s_learned.py features|validate|score"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP5, EXP8, RES, jdump, load_frame, read_parquet_parts, setup_logger
from featport import exp5_concept_level, exp8_basic

logger = setup_logger("s_learned")
Y0, NY = 1995, 28


def arrays(fr: pd.DataFrame, cap: bool):
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(fr.ci))]
    pos = pd.Series(np.arange(len(fr)), index=fr.ci.to_numpy())
    f = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    n = ag.n.to_numpy(float)
    vf = ag.vfield.to_numpy(np.int64)
    N = np.bincount(f * NY + y, weights=n, minlength=len(fr) * NY).reshape(len(fr), NY)
    V = np.bincount((f * NY + y) * 27 + vf, weights=n, minlength=len(fr) * NY * 27).reshape(len(fr), NY, 27)
    if cap:
        for i, t0 in enumerate(fr.t0.to_numpy()):
            N[i, t0 + 3 - Y0:] = 0
            V[i, t0 + 3 - Y0:] = 0
    return N, V


def build(fr: pd.DataFrame, early: pd.DataFrame, cap: bool) -> pd.DataFrame:
    N, V = arrays(fr, cap)
    G = np.load(EXP5 / "scan/year_field_totals.npz")["G"].astype(float)
    GF = np.load(EXP5 / "scan/year_field_totals.npz")["VF"][:, 1:].astype(float)
    a = exp5_concept_level(fr, N, V, G)
    b = exp8_basic(fr, V, GF, early)
    return a.merge(b, on="ci")


def cmd_validate() -> None:
    fr = load_frame().sample(150, random_state=9)
    em = read_parquet_parts(EXP8 / "data/frame_matches_early", columns=["ci", "year", "vfield", "authors"])
    em = em[em.ci.isin(set(fr.ci))]
    mine = build(fr, em, cap=False)
    ref = pd.read_parquet(EXP8 / "results/indicator_matrix.parquet")
    m = mine.merge(ref, on="ci", suffixes=("", "_ref"))
    out = {c: float(np.nanmax(np.abs(m[c].astype(float) - m[f"{c}_ref"].astype(float))))
           for c in mine.columns if c != "ci" and f"{c}_ref" in m.columns}
    jdump({"n": len(m), "max_abs_diff": out}, RES / "learned_port_validation.json")
    logger.info(f"port validation: {out}")


def cmd_features() -> None:
    fr = pd.read_parquet(DATA / "features_cohort.parquet")
    em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "vfield", "tagstate", "authors"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(fr.ci))]
    f = build(fr[["ci", "t0", "home"]].reset_index(drop=True), em, cap=True)
    eg = pd.read_parquet(DATA / "ego_open_cohort_full.parquet")
    eg = eg[["ci"] + [c for c in eg.columns if c.endswith("__full")]].rename(columns=lambda c: c.replace("__full", ""))
    f = f.merge(eg, on="ci", how="left")
    f.to_parquet(DATA / "learned_features_cohort.parquet", index=False)
    logger.info(f"cohort learned-model features {f.shape}")


def cmd_score() -> None:
    import joblib
    from scipy.stats import spearmanr
    from design import apply_design, design_names
    from rq1stats import auc, logit_pred
    lm = json.loads((EXP8 / "results/learned_model.json").read_text())
    spec8 = json.loads((EXP8 / "results/frozen_spec.json").read_text())
    A = pd.read_parquet(DATA / "analysis_cohort.parquet")
    lf = pd.read_parquet(DATA / "learned_features_cohort.parquet")
    keep = [c for c in A.columns if c not in lf.columns or c == "ci"]
    d = A[keep].merge(lf, on="ci", how="left")
    X = apply_design(d, spec8["design_spec"])
    Xb = apply_design(d, spec8["b5_spec"])
    names = design_names(spec8["design_spec"])
    fully_imputed = [c for c in spec8["design_spec"]["cols"] if c not in d.columns or d[c].isna().all()]
    rng = np.random.default_rng(20260929)
    res = {"fully_imputed_features": fully_imputed}
    for o in ("O2r_m50", "O2r_resid", "O3"):
        m = spec8["learned"][o]
        is_bin = o == "O3"
        extra = np.zeros((len(d), 0))
        if m.get("t0_std"):
            extra = ((d.t0.to_numpy(float) - m["t0_std"][0]) / m["t0_std"][1])[:, None]
        lin = joblib.load(EXP8 / f"models/linear_all_{o}.joblib")
        coef = np.ravel(lin.coef_)[:len(names)]
        mass = np.abs(coef)
        imp_mass = float(mass[[names.index(c) for c in fully_imputed if c in names]].sum() / mass.sum()) if mass.sum() else 0.0
        b_all = np.c_[Xb, extra]
        c = np.array(m["B5_coef"])
        pb = logit_pred(c, b_all) if is_bin else c[0] + b_all @ c[1:]
        pl = lin.predict_proba(np.c_[X, extra])[:, 1] if is_bin else lin.predict(X)
        y = d[o].to_numpy(float)
        ok = np.isfinite(y)
        f = (lambda yy, p: auc(yy, p)) if is_bin else (lambda yy, p: spearmanr(p, yy)[0])
        est0, est1 = f(y[ok], pb[ok]), f(y[ok], pl[ok])
        bs = []
        idx = np.nonzero(ok)[0]
        for _ in range(2000):
            i = rng.choice(idx, len(idx))
            bs.append(f(y[i], pl[i]) - f(y[i], pb[i]))
        res[o] = {"n": int(ok.sum()), "metric": "AUC" if is_bin else "Spearman", "B5": float(est0),
                  "linear_all": float(est1), "diff": float(est1 - est0),
                  "diff_ci": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))],
                  "imputed_coef_mass": imp_mass, "evaluable": imp_mass <= 0.20,
                  "note": "t0 standardised with DEV constants: cohort onset years lie outside the DEV range" if m.get("t0_std") else ""}
        logger.info(f"learned {o}: {res[o]}")
    res["O4_EBM"] = "not evaluable: O4 not computed (no citation pass; declared drop)"
    jdump(res, RES / "learned_models_cohort.json")


if __name__ == "__main__":
    {"features": cmd_features, "validate": cmd_validate, "score": cmd_score}[sys.argv[1]]()
