#!/usr/bin/env python3
"""iter-5 GEN_ART experiment: why churning concepts spread (Part A), trait stability (Part B), and the completion
of the sealed Exp11 within-concept closure test (Part C). Entry point that runs every stage in order (skipping stages
whose outputs already exist unless --force) and assembles the deliverables:

  STEP 0  setup_exp11.py                 copy + path-only patch of the sealed Exp11 code, seal verification (G0)
  STEP 1  exp11_code/run_completion.py   OLD_HELDOUT / COHORT body models, G1, robustness, OOF predictions, H-M5
  STEP 2  exp11_code/run_event_study.py  Sun-Abraham event study (timing gate, placebo) -> H-M4
  STEP 3  exp11_code/sequence.py         H-S1 share test, survival, event studies around peak / take-off
  STEP 4  exp11_code/run_partners.py     H-P1 as preregistered (ALL-papers static partner set)
  STEP 6  partners_home.py               HOME partner build (G2) for EXP5, the 2015-17 cohort, and the later retest
  STEP 5  seal_iter5.py freeze/seal      Part A/B spec + feature hashes (before any outcome join)
  T0      tests/test_iter5.py            identities, Shapley, planted signal, ICC recovery, degree cut, G2
  STEP 7  score_partA.py                 class psp, DL, Shapley, Holm, placebos, bridging (EXPLORATORY)
  STEP 8  trait_stability.py             ICC / test-retest (P-B1, P-B2)
  STEP 9  this file                      exp11_completion.json, method_out.json (baseline B5 vs B5 + NOVCHURN)

Usage: python method.py [--stages all|assemble] [--workers 4] [--force]"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS / "lib_iter5"))

import numpy as np
import pandas as pd

from common_iter5 import B5, DATA, E8, RES, SEED, add_deviation, jdump, setup_logger

X11 = WS / "exp11_code"
PY = sys.executable
STAGES = [
    ("setup", ["setup_exp11.py"], RES / "seal_verification.json"),
    ("completion", ["exp11_code/run_completion.py", "--workers", "{w}"], X11 / "results/fe_results_completed.json"),
    ("event_study", ["exp11_code/run_event_study.py", "--workers", "{w}"], X11 / "results/event_study.json"),
    ("sequence", ["exp11_code/sequence.py", "--boot", "300", "--workers", "{w}"], X11 / "results/sequence_tests.json"),
    ("partners_c4", ["exp11_code/run_partners.py"], X11 / "results/H_P1.json"),
    ("home_exp5", ["partners_home.py", "--frame", "exp5", "--workers", "{w}"], DATA / "partner_home_components_exp5.parquet"),
    ("home_cohort", ["partners_home.py", "--frame", "cohort", "--workers", "{w}"], DATA / "partner_home_components_cohort.parquet"),
    ("home_retest", ["partners_home.py", "--frame", "retest", "--workers", "{w}"], DATA / "partner_home_components_retest.parquet"),
    ("freeze", ["seal_iter5.py", "freeze"], RES / "frozen_spec_iter5.json"),
    ("seal", ["seal_iter5.py", "seal"], WS / "logs/seal_iter5.log"),
    ("tests", ["tests/test_iter5.py"], RES / "unit_tests_iter5.json"),
    ("score_partA", ["score_partA.py", "--workers", "{w}"], RES / "partner_classes.json"),
    ("trait", ["trait_stability.py"], RES / "trait_stability.json"),
]


def run_stages(workers: int, force: bool, logger) -> None:
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMBA_NUM_THREADS="1")
    for name, cmd, out in STAGES:
        if out.exists() and not force:
            logger.info(f"stage {name}: output exists, skipped")
            continue
        c = [PY] + [x.format(w=workers) for x in cmd]
        logger.info(f"stage {name}: {' '.join(c[1:])}")
        t = time.time()
        r = subprocess.run(c, cwd=WS, env=env)
        if r.returncode != 0:
            raise RuntimeError(f"stage {name} failed with exit code {r.returncode}")
        logger.info(f"stage {name} done in {(time.time()-t)/60:.1f} min")


# ----------------------------------------------------------------------------- exp11 completion
def exp11_completion(logger) -> dict:
    j = lambda p: json.loads(p.read_text()) if p.exists() else None  # noqa: E731
    seal = j(RES / "seal_verification.json")
    fe = j(X11 / "results/fe_results_completed.json")
    es = j(X11 / "results/event_study.json")
    sq = j(X11 / "results/sequence_tests.json")
    hp = j(X11 / "results/H_P1.json")
    ut = j(X11 / "results/unit_tests.json")
    dv = j(X11 / "results/deviations.json") or {}
    out: dict = {"dev_verdict": "DEV verdict unchanged: NOT SUPPORTED",
                 "seal_verification": {k: seal[k] for k in ("frozen_spec_ok", "n_files", "n_ok", "G0_pass", "mismatches")}
                 if seal else None}
    if fe:
        out["panel_rebuild_equal_to_cache"] = fe["panel_rebuild_check"]["equal"]
        out["G1_dev_reproduction"] = fe["G1_dev_reproduction"]["pass"]
        bm = {}
        for b in ("DEV", "OLD_HELDOUT", "COHORT"):
            r = fe[b]
            bs = r.get("bootstrap", {})
            bm[b] = {"n_rows": r["n_rows"], "n_concepts": r["n_concepts"],
                     "H_M1_density": {"b": r["H_M1_density"]["b"], "ci_crv1": r["H_M1_density"]["ci"],
                                      "ci_boot": bs.get("b_density", {}).get("ci"),
                                      "pct_per_within_sd": r["H_M1_density"]["pct_per_within_sd"]},
                     "H_M2_OPEN_home": {"b": r["H_M2_open"]["b"], "ci_crv1": r["H_M2_open"]["ci"],
                                        "ci_boot": bs.get("b_open", {}).get("ci"),
                                        "pct_per_within_sd": r["H_M2_open"]["pct_per_within_sd"]},
                     "joint": r.get("joint"), "lpm_density": r.get("lpm_density"), "lpm_open": r.get("lpm_open"),
                     "DL_density": r.get("DL_density"), "DL_OPEN_home": r.get("DL_OPEN_home"),
                     "n_boot": bs.get("n_boot")}
        out["body_models"] = bm
        out["H_M3"] = fe.get("H_M3")
        out["H_M5"] = fe.get("H_M5")
        out["robustness_DEV"] = fe.get("robustness_DEV")
        out["prediction_deviance"] = fe.get("prediction_deviance")
    if es:
        E = {}
        for b in ("DEV", "OLD_HELDOUT", "COHORT"):
            if b not in es:
                continue
            E[b] = {"n_eligible": es[b].get("n_eligible"), "n_treated": es[b].get("n_treated")}
            for v, r in es[b].items():
                if isinstance(r, dict) and "att" in r:
                    E[b][v] = {k: r.get(k) for k in ("att", "ci", "mean_lag_0_2", "lag02_ci", "pretrend_wald",
                                                     "roth_detectable_slope_80pct", "max_abs_lead", "lead_small_vs_lag",
                                                     "n_treated", "n", "n_boot_ok", "treated_rows_by_e",
                                                     "crosscheck_pyfixest_max_abs_diff")}
            if "placebo_event_date" in es[b]:
                E[b]["placebo_event_date"] = es[b]["placebo_event_date"]
        out["event_study"] = E
        out["H_M4"] = es.get("H_M4")
        out["event_study_timing_gate"] = es.get("timing_gate")
    if sq:
        out["H_S1"] = {b: sq[b]["share_test"] for b in ("DEV", "OLD_HELDOUT", "COHORT", "ALL") if b in sq}
        out["H_S1_excl_Med"] = {b: sq[b]["share_test_excl_Med"] for b in ("DEV", "OLD_HELDOUT", "COHORT", "ALL") if b in sq}
        out["sequence_survival"] = {b: {"logrank": sq[b]["survival"]["logrank"], "cox": sq[b]["survival"]["cox"],
                                        "km_median": {k: v["median"] for k, v in sq[b]["survival"]["km"].items()}}
                                    for b in ("DEV", "OLD_HELDOUT", "COHORT", "ALL") if b in sq}
        out["sequence_event_studies"] = {k: {kk: v.get(kk) for kk in ("att", "ci", "mean_lag_0_2", "lag02_ci",
                                                                      "pretrend_wald", "n_treated")}
                                         for k, v in sq.items() if k.startswith("es_")}
        out["H_S1_prior_estimate_Exp12"] = {"HR": 0.47, "note": "Exp12 independent prior estimate, cited, not recomputed"}
    if hp:
        out["H_P1"] = hp
    out["exp11_unit_tests_rerun"] = {k: v.get("pass") for k, v in ut.items() if isinstance(v, dict)} if ut else None
    out["deviations_exp11_code"] = dv
    return out


# ----------------------------------------------------------------------------- method_out
def cv_ridge(d: pd.DataFrame, feats: list[str], y: str, folds: np.ndarray, cats: list[str]) -> np.ndarray:
    from sklearn.linear_model import Ridge
    pred = np.full(len(d), np.nan)
    Xn = d[feats].to_numpy(float)
    C = pd.get_dummies(d[cats].astype(str), drop_first=True).to_numpy(float) if cats else np.zeros((len(d), 0))
    yv = d[y].to_numpy(float)
    for k in np.unique(folds):
        tr, te = folds != k, folds == k
        med = np.nanmedian(Xn[tr], axis=0)
        miss = ~np.isfinite(Xn)
        Xi = np.where(miss, med, Xn)
        mu, sd = Xi[tr].mean(0), Xi[tr].std(0)
        sd[sd < 1e-12] = 1
        Z = np.c_[(Xi - mu) / sd, miss[:, [j for j in range(Xn.shape[1]) if miss[:, j].any()]].astype(float), C]
        m = Ridge(alpha=1.0).fit(Z[tr], yv[tr])
        pred[te] = m.predict(Z[te])
    return pred


def method_out(logger) -> dict:
    from scipy import stats
    D5 = pd.read_parquet(DATA / "partA_features_exp5.parquet")
    Dc = pd.read_parquet(DATA / "partA_features_cohort.parquet")
    D5["label"], D5["body_name"] = D5.ci.astype(str), D5.body
    A = pd.read_parquet(E8 / "data/analysis_table.parquet", columns=["ci", "name"])
    D5 = D5.merge(A, on="ci", how="left")
    Dc["body_name"] = "COHORT_2015_17"
    parts = ["nov_type_METHOD", "nov_type_DOMAIN", "ch_type_METHOD", "ch_type_DOMAIN", "ner_comm_new", "ner_comm_old",
             "nov_deg_low", "nov_deg_high", "ner_carrier_mixed", "ner_carrier_pure", "chd_all", "cha_all"]
    meta_cols = ["NOVCHURN_home", "NOV_res", "edge_persistence", "new_edge_rate", "churn", "bridging_share_home",
                 "OPEN_home", "M", "n1", "n_home_early"] + parts
    rows, metrics = [], {}
    for body, d in list(D5.groupby("body_name")) + [("COHORT_2015_17", Dc)]:
        d = d[np.isfinite(d.O2r_m50) & d[B5].notna().all(1)].reset_index(drop=True)
        folds = np.random.default_rng(SEED).integers(0, 5, len(d))
        cats = ["t0"] + (["group"] if "group" in d and d.group.nunique() > 1 else [])
        p0 = cv_ridge(d, B5, "O2r_m50", folds, cats)
        p1 = cv_ridge(d, B5 + ["NOVCHURN_home"], "O2r_m50", folds, cats)
        p2 = cv_ridge(d, B5 + parts, "O2r_m50", folds, cats)
        p3 = cv_ridge(d, B5 + ["OPEN_home"], "O2r_m50", folds, cats)
        y = d.O2r_m50.to_numpy(float)
        metrics[body] = {"n": int(len(d))}
        for nm, p in (("B5", p0), ("B5_plus_NOVCHURN", p1), ("B5_plus_partner_classes", p2), ("B5_plus_OPEN_home", p3)):
            metrics[body][nm] = {"spearman_oof": float(stats.spearmanr(p, y)[0]),
                                 "rmse_oof": float(np.sqrt(np.mean((p - y) ** 2)))}
        # paired concept bootstrap of the OOF Spearman gain (NOVCHURN vs baseline)
        rng = np.random.default_rng(SEED)
        g = []
        for _ in range(1000):
            i = rng.integers(0, len(y), len(y))
            g.append(stats.spearmanr(p1[i], y[i])[0] - stats.spearmanr(p0[i], y[i])[0])
        metrics[body]["gain_NOVCHURN_spearman"] = {"est": metrics[body]["B5_plus_NOVCHURN"]["spearman_oof"] -
                                                   metrics[body]["B5"]["spearman_oof"],
                                                   "ci": [float(np.percentile(g, 2.5)), float(np.percentile(g, 97.5))]}
        for i, r in d.iterrows():
            inp = {"concept": str(r.get("name", "")), "ci": int(r.ci), "body": body, "t0": int(r.t0),
                   "group": str(r.get("group", r.get("agroup", "")))}
            ex = {"input": json.dumps(inp), "output": f"{r.O2r_m50:.6f}",
                  "predict_B5": f"{p0[i]:.6f}", "predict_B5_plus_NOVCHURN": f"{p1[i]:.6f}",
                  "predict_B5_plus_partner_classes": f"{p2[i]:.6f}", "predict_B5_plus_OPEN_home": f"{p3[i]:.6f}",
                  "metadata_body": body, "metadata_fold": int(folds[i]), "metadata_O2r_resid": None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)}
            for c in meta_cols:
                v = r.get(c, np.nan)
                ex[f"metadata_{c}"] = None if v is None or not np.isfinite(v) else float(round(v, 6))
            rows.append(ex)
        logger.info(f"{body}: {metrics[body]}")
    ds = [{"dataset": "partner_home_concepts", "examples": rows}]
    pr = X11 / "data/predictions.parquet"
    if pr.exists():
        P = pd.read_parquet(pr)
        P = pd.concat([g.sample(min(len(g), 2000), random_state=SEED) for _, g in P.groupby("body")])
        ex2 = []
        for r in P.itertuples():
            ex2.append({"input": json.dumps({"ci": int(r.ci), "year": int(r.year), "body": r.body, "age": int(r.age),
                                             "density": float(r.density), "OPEN_home": float(r.OPEN_home),
                                             "log1p_home": float(r.log1p_home), "log1p_all": float(r.log1p_all),
                                             "log1p_deg": float(r.log1p_deg), "log_at_risk": float(r.log_at_risk)}),
                        "output": f"{r.y_next:.0f}", "predict_fe_density": f"{r.pred_fe_density:.6f}",
                        "predict_fe_open": f"{r.pred_fe_open:.6f}", "predict_controls_only": f"{r.pred_controls_only:.6f}",
                        "metadata_body": r.body, "metadata_fold": int(r.fold)})
        ds.append({"dataset": "exp11_panel_predictions", "examples": ex2})
    return {"metadata": {"method_name": "HOME partner-class decomposition of NOVCHURN (Part A) + Exp11 completion",
                         "description": "One example per concept with a finite O2r_m50: output = O2r_m50; predictions "
                                        "are 5-fold concept-CV ridge within body: B5 baseline vs B5 + NOVCHURN_home, "
                                        "B5 + 12 partner-class parts, B5 + OPEN_home. Second dataset: Exp11 out-of-fold "
                                        "PPML predictions of off-home field entries (sample of 2,000 rows per body).",
                         "status": "EXPLORATORY (selection data) for Part A",
                         "cv_metrics": metrics}, "datasets": ds}


@__import__("loguru").logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="all", choices=["all", "assemble"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    logger = setup_logger("method")
    t = time.time()
    if a.stages == "all":
        run_stages(a.workers, a.force, logger)
    comp = exp11_completion(logger)
    comp["runtime_assemble_s"] = time.time() - t
    jdump(comp, RES / "exp11_completion.json")
    mo = method_out(logger)
    jdump(mo, WS / "method_out.json")
    logger.info(f"method_out.json: {[ (d['dataset'], len(d['examples'])) for d in mo['datasets']]}")


if __name__ == "__main__":
    main()
