#!/usr/bin/env python3
"""STEP 6: assemble eval_out.json (exp_eval_sol_out schema) from the Part A / Part B result files.

Nothing is re-estimated here: every metric is read from results/*.json|csv written by partb_core.py (T0, B1, B2),
spec_curve.py (B3), heterogeneity.py (B4), step3_drca.py, build_corrections.py and verify_ledger.py.

Datasets:
  open_heldout_concepts - one example per held-out concept (6 units): OPEN (all-papers build) and OPEN_PC1 as
                          predictions of O2r_m50, with within-unit rank agreement and B1 footprint flags
  spec_curve            - one example per specification (1,920): pooled psp over held-out groups
  claims_ledger_v3      - one example per ledger row: reported value vs file value, eval_match 0/1

Usage: python eval.py"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger

from common import LOGS, RES, SEED, UNITS6, WS, sha256

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "eval.log", rotation="30 MB", level="DEBUG")

VERDICT_B1 = {"MOST": 1, "PARTIAL": 2, "LITTLE": 3}
VERDICT_LIFE = {"COVERAGE": 1, "VARIANCE": 2, "UNEXPLAINED": 3}
VERDICT_DRCA = {"EQUIVALENT": 1, "NESTED": 2, "DIFFERENT": 3}


def fin(x) -> bool:
    return x is not None and isinstance(x, (int, float, np.integer, np.floating)) and math.isfinite(float(x))


def rj(name: str) -> dict:
    return json.loads((RES / name).read_text())


def metrics() -> tuple[dict, dict]:
    T0, B1, SC, H = rj("gate_T0.json"), rj("post_onset_rescore.json"), rj("spec_curve.json"), rj("heterogeneity.json")
    DC, LV = rj("drca_persist_comparison.json"), rj("ledger_verification.json")
    PG = pd.read_csv(RES / "per_group_pooled.csv")
    LG = pd.read_csv(RES / "claims_ledger_v3.csv")
    m: dict = {"gate_T0_pass": int(T0["gate_T0_pass"]),
               "gate_T0_max_abs_diff": max(r["abs_diff"] for r in T0["rows"])}
    for f, tag in (("M0_density_end", "M0"), ("D_vol_end", "Dvol")):
        for o in ("O2r_m50", "O2r_resid"):
            p = B1["pooled"][f"DL4|{f}|{o}"]
            s = f"B1_{tag}_{o}"
            m[f"{s}_psp_full"] = p["psp_full"]
            m[f"{s}_psp_post"] = p["psp_post"]
            m[f"{s}_psp_post_ci_lo"], m[f"{s}_psp_post_ci_hi"] = p["psp_post_ci_boot"]
            m[f"{s}_attenuation"] = p["attenuation"]
            m[f"{s}_attenuation_ci_lo"], m[f"{s}_attenuation_ci_hi"] = p["attenuation_ci"]
            m[f"{s}_verdict_code"] = VERDICT_B1[p["verdict"]]
    m["B1_share_heldout_any_preonset_entry"] = B1["spearman"]["share_with_any_pre_onset_entry"]
    m["B1_spearman_Dvol_post_reach_MATHDEC"] = B1["collinearity_post_vs_B5_reach"]["spearman_D_vol_post_reach_by_unit"]["MATHDEC"]
    for o in ("O2r_m50", "O2r_resid"):
        for pool in ("DL4", "DL6"):
            r = PG[(PG.indicator == "OPEN") & (PG.outcome == o) & (PG.pool == pool)].iloc[0]
            s = f"OPEN_{o}_{pool}"
            m[f"{s}_psp"], m[f"{s}_ci_lo"], m[f"{s}_ci_hi"] = r.pooled, r.ci_lo, r.ci_hi
            m[f"{s}_I2"], m[f"{s}_pi_lo"], m[f"{s}_pi_hi"] = r.I2, r.pi_lo, r.pi_hi
            m[f"{s}_sign_pos_of6"] = int(r.sign_pos_6)
    for pool in ("DL4", "DL6"):
        s, n = SC["summary"][pool], SC["null"][pool]
        m[f"spec_{pool}_share_ci_gt0"] = s["share_ci_gt0"]
        m[f"spec_{pool}_share_est_gt0"] = s["share_est_gt0"]
        m[f"spec_{pool}_median_psp"] = s["median"]
        m[f"spec_{pool}_p_share_ci_gt0"] = n["p_share_ci_gt0"]
        m[f"spec_{pool}_p_median"] = n["p_median"]
        m[f"spec_{pool}_null_median_mean"] = n["null_median_mean"]
        m[f"spec_{pool}_headline_psp"] = SC["headline"][pool]["est"]
    m["spec_n_specs"] = SC["n_specs"]
    m["spec_null_draws"] = SC["null"]["DL4"]["n_draws"]
    m["spec_calibration_median_ratio_boot_over_analytic"] = SC["calibration"]["median_ratio_boot_over_analytic"]
    m["spec_DL4_median_C1"] = SC["marginals"]["DL4"]["control"]["C1"]["median"]
    m["spec_DL4_median_C3_contact_reach"] = SC["marginals"]["DL4"]["control"]["C3"]["median"]
    m["I2_unit6"], m["I2_unit4"], m["I2_subunit"] = H["I2_unit6"], H["I2_unit4"], H["I2_subunit"]
    m["k_subunits"] = H["k_subunits"]
    m["meta_regression_min_perm_p"] = min(v["p_perm"] for v in H["meta_regression"]["univariate"].values())
    m["LIFEENV_psp_OPEN"] = H["lifeenv"]["psp_LIFEENV"]
    m["LIFEENV_psp_reweighted_coverage"] = H["lifeenv"]["entropy_balanced"]["psp_reweighted"]
    m["LIFEENV_sd_ratio_OPEN"] = H["lifeenv"]["sd_ratio"]["OPEN"]["ratio"]
    m["LIFEENV_verdict_code"] = VERDICT_LIFE[H["lifeenv"]["verdict"]]
    m["drca_verdict_code"] = VERDICT_DRCA[DC["verdict"]]
    m["drca_max_spearman_persist_k_vs_pers"] = max(v["spearman_vs_D_rca_pers"] for v in DC["comparisons"].values())
    st = LG.status.value_counts().to_dict()
    for k in ("MATCH", "ROUNDING_ONLY", "MISMATCH", "NOT_FOUND"):
        m[f"ledger_{k}"] = int(st.get(k, 0))
    m["ledger_rows"] = int(len(LG))
    m["ledger_verify_disagreements"] = LV["n_disagreements"]
    m["ledger_orphan_numeric_tokens"] = LV["n_orphan_numeric_tokens"]
    ev2 = pd.read_csv(WS.parents[2] / "round-3/evaluation-2/src/claims_ledger.csv")
    m["eval2_open_rows_resolved"] = int(ev2.status.isin(["MISMATCH", "MISLABELLED"]).sum())
    m = {k: (float(v) if isinstance(v, (float, np.floating)) else int(v)) for k, v in m.items() if fin(v)}
    info = {"B1_verdicts": {k: v["verdict"] for k, v in B1["pooled"].items()},
            "B1_units_excluded": {k: v["units_excluded_undefined_post"] for k, v in B1["pooled"].items()},
            "LIFEENV_verdict": H["lifeenv"]["verdict"], "drca_verdict": DC["verdict"]}
    return m, info


def ds_concepts() -> dict:
    B = pd.read_parquet(RES / "b_table.parquet", columns=["ci", "name", "unit", "t0", "O2r_m50", "O2r_resid", "OPEN", "OPEN_PC1",
                                                          "OPEN_n_components", "M0_density_end", "M0_density_post",
                                                          "D_vol_end", "D_vol_post", "footprint_share", "D_vol_pre"])
    B = B[B.unit.isin(UNITS6)].reset_index(drop=True)
    for c in ("OPEN", "OPEN_PC1", "O2r_m50"):
        B[f"pct_{c}"] = B.groupby("unit")[c].rank(pct=True)
    ex = []
    for r in B.itertuples(index=False):
        e = {"input": f"{r.name}|{r.unit}|{int(r.t0)}",
             "output": f"{r.O2r_m50:.4f}" if fin(r.O2r_m50) else "NA",
             "predict_OPEN_all": f"{r.OPEN:.4f}" if fin(r.OPEN) else "NA",
             "predict_OPEN_pc1": f"{r.OPEN_PC1:.4f}" if fin(r.OPEN_PC1) else "NA",
             "predict_M0_density_post": f"{r.M0_density_post:.4f}" if fin(r.M0_density_post) else "NA",
             "metadata_concept_index": int(r.ci), "metadata_unit": r.unit, "metadata_t0": int(r.t0),
             "eval_open_defined": int(fin(r.OPEN)), "eval_open_n_components": int(r.OPEN_n_components),
             "eval_post_differs_D_vol": int(r.D_vol_post != r.D_vol_end),
             "eval_D_vol_pre": int(r.D_vol_pre)}
        for k, v in (("eval_rank_pct_OPEN", r.pct_OPEN), ("eval_rank_pct_OPEN_pc1", r.pct_OPEN_PC1),
                     ("eval_rank_pct_O2r_m50", r.pct_O2r_m50), ("eval_footprint_share", r.footprint_share)):
            if fin(v):
                e[k] = float(round(v, 6))
        if fin(r.pct_OPEN) and fin(r.pct_O2r_m50):
            e["eval_abs_rank_gap_OPEN"] = float(round(abs(r.pct_OPEN - r.pct_O2r_m50), 6))
        ex.append(e)
    logger.info(f"open_heldout_concepts: {len(ex):,} examples")
    return {"dataset": "open_heldout_concepts", "examples": ex}


def ds_specs() -> dict:
    S = pd.read_csv(RES / "spec_curve_specs.csv")
    ex = []
    for r in S.itertuples(index=False):
        e = {"input": f"{r.composite}|{r.outcome}|{r.control}", "output": f"{r.DL4_est:.4f}",
             "predict_DL4_pooled_psp": f"{r.DL4_est:.4f} [{r.DL4_lo:.4f}, {r.DL4_hi:.4f}]",
             "predict_DL6_pooled_psp": f"{r.DL6_est:.4f} [{r.DL6_lo:.4f}, {r.DL6_hi:.4f}]",
             "metadata_weights": r.weights, "metadata_size": int(r.size), "metadata_spec_id": int(r.spec_id),
             "eval_DL4_est": float(r.DL4_est), "eval_DL4_ci_gt0": int(r.DL4_lo > 0), "eval_DL4_I2": float(r.DL4_I2),
             "eval_DL4_npos": int(r.DL4_npos), "eval_DL6_est": float(r.DL6_est), "eval_DL6_ci_gt0": int(r.DL6_lo > 0)}
        ex.append(e)
    return {"dataset": "spec_curve", "examples": ex}


def ds_ledger() -> dict:
    L = pd.read_csv(RES / "claims_ledger_v3.csv", dtype={"reported_value": str, "file_value": str})
    ex = []
    for r in L.itertuples(index=False):
        e = {"input": f"{r.target_file} | {r.target_section} | {r.text_snippet}", "output": str(r.reported_value),
             "predict_file_value": str(r.file_value), "metadata_claim_id": r.claim_id, "metadata_source_file": r.source_file,
             "metadata_key_path": r.key_path, "metadata_status": r.status, "metadata_kind": r.kind,
             "eval_match": int(r.status in ("MATCH", "ROUNDING_ONLY"))}
        try:
            d = float(r.abs_diff)
            if math.isfinite(d):
                e["eval_abs_diff"] = d
        except (TypeError, ValueError):
            pass
        ex.append(e)
    return {"dataset": "claims_ledger_v3", "examples": ex}


def main() -> None:
    m, info = metrics()
    spec = rj("boundary_spec.json")
    out = {"metadata": {
        "evaluation_name": "Fix the record and test how far openness holds (iteration 4, evaluation 3)",
        "status_part_B": "EXPLORATORY: old held-out groups already unsealed (Exp5, Exp8); nothing here confirms OPEN",
        "seal": {"boundary_spec_sha256": sha256(RES / "boundary_spec.json"), "seal_log": "logs/seal.log"},
        "seed": SEED, "estimator": spec.get("estimator"), "pooling": spec.get("pooling"),
        "verdicts": info,
        "code_maps": {"B1_verdict": VERDICT_B1, "LIFEENV_verdict": VERDICT_LIFE, "drca_verdict": VERDICT_DRCA},
        "skipped": {"optional_GENERIC_LLM_check": "SKIPPED_BY_DEFAULT (plan: optional, $0 default; no LLM spend)"},
        "deviations": [
            "B1 implementation fix after the seal: bootstrap draws in which psp is undefined (post-onset D_vol rank-collinear "
            "with B5 reach) are dropped; a unit with < 50% defined draws (MATHDEC for D_vol) is excluded from BOTH the full "
            "and post pools. The verdict rule is unchanged.",
            "B4: 21 sub-units reach n >= 60 (plan expected about 30-50); >= 20, so the frozen n >= 60 rule is kept.",
            "The previous attempt of this artifact crashed the worker container (OpenBLAS thread exhaustion: 48 threads x "
            "~36 processes); all scripts now pin BLAS to 1 thread and use <= 3 workers. Results from before the crash that "
            "had completed (seal, T0, B1, spec curve) were verified; B1, B2 and B4 were re-run."],
        "files": {"corrections": "corrections/00..11 *.md", "ledger": "results/claims_ledger_v3.csv",
                  "ledger_verification": "results/ledger_verification.json", "figures": "figures/*.png|pdf"}},
        "metrics_agg": m,
        "datasets": [ds_concepts(), ds_specs(), ds_ledger()]}
    (WS / "eval_out.json").write_text(json.dumps(out, indent=1))
    logger.info(f"eval_out.json: {len(m)} metrics; datasets {[ (d['dataset'], len(d['examples'])) for d in out['datasets']]}")


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
