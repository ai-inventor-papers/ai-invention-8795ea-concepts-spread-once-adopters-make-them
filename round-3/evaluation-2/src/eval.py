#!/usr/bin/env python3
"""Checking the record before the paper: orchestrates the five work packages and assembles eval_out.json
(exp_eval_sol_out schema).

  uv run eval.py --stages all        # WP2-T3, WP2-T4, WP3, WP4 (extract, validation, hand check finalize), WP1, assemble
  uv run eval.py                     # assemble only (from the files the stages wrote)

The hand-check sampling/LLM/Wikipedia step (wp4_handcheck.py without --finalize) is run separately because the executor
reads the items and writes results/executor_verdicts.json between that step and --finalize."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys

import numpy as np
import pandas as pd
from loguru import logger

import common as C

STAGES = [["wp2_t3_refit.py"], ["wp2_t4_nextfield.py"], ["wp3_frames.py"], ["wp4_extract.py"], ["wp4_o5.py"],
          ["wp4_handcheck.py", "--finalize"], ["wp1_ledger.py"]]


def s(x) -> str:
    if isinstance(x, float) and not math.isfinite(x):
        return "NaN"
    return x if isinstance(x, str) else json.dumps(C.jsonable(x))


def num(x) -> float | None:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return None
    return v if math.isfinite(v) else None


def assemble() -> dict:
    led = pd.read_csv(C.WS / "claims_ledger.csv")
    fa = json.loads((C.WS / "frame_agreement.json").read_text())
    core = json.loads((C.RES / "o5_validation_core.json").read_text())
    hc = json.loads((C.RES / "o5_handcheck_summary.json").read_text())
    t3 = json.loads((C.RES / "t3_refit_bootstrap.json").read_text())
    tr = json.loads((C.TAB / "next_field_trace.json").read_text())
    wp1 = json.loads((C.RES / "wp1_summary.json").read_text())
    defs = json.loads((C.WS / "o5_definitions.json").read_text())
    o5v = {"definitions_file": "o5_definitions.json", **core, "hand_check": hc}
    C.dump(o5v, C.WS / "o5_validation.json")
    ag = fa["agreement"]
    main = core["associations_pooled_heldout_DL"]["O5_main"]
    st = led.status.value_counts().to_dict()
    blocking_rows = led[led.severity == "blocking"]
    ma = {"n_ledger_rows": len(led), "n_match": st.get("MATCH", 0), "n_rounding": st.get("ROUNDING", 0), "n_mismatch": st.get("MISMATCH", 0),
          "n_missing": st.get("MISSING", 0) + st.get("MISSING_SOURCE", 0), "n_mislabelled": st.get("MISLABELLED", 0),
          "n_file_flag_overridden": st.get("FILE_FLAG_OVERRIDDEN", 0),
          "n_blocking_rows": len(blocking_rows),
          "n_blocking_fixed": int(blocking_rows.correction_text.fillna("").str.len().gt(0).sum() + blocking_rows.text_change_note.fillna("").str.len().gt(0).sum()
                                  - (blocking_rows.correction_text.fillna("").str.len().gt(0) & blocking_rows.text_change_note.fillna("").str.len().gt(0)).sum()),
          "n_draft_numbers_harvested": sum(wp1["harvest"].values()), "n_draft_numbers_auto_matched": wp1["harvest"].get("AUTO_MATCH", 0),
          "t1_n_portability_indicators": wp1["T1_n_indicators"], "n_partial_association_candidates": wp1["n_partial_candidates"],
          "frame_n_exp5": fa["n_exp5"], "frame_n_exp6": fa["n_exp6"], "frame_n_both": fa["n_both"],
          "onset_exact_agree": ag["onset_exact"]["value"], "onset_pm1_agree": ag["onset_pm1"]["value"],
          "home_kappa": ag["home_kappa_26"]["value"], "o1_kappa": ag["O1_kappa"]["value"], "o3_kappa": ag["O3_kappa"]["value"],
          "o2r_spearman": ag["O2r_m50"]["spearman"], "o2r_m50_lin_ccc": ag["O2r_m50"]["lin_ccc"],
          "early_volume_log_spearman": ag["early_volume_log"]["spearman"], "episode_jaccard_median": ag["episode_jaccard"]["median"],
          "episode_jaccard_pooled": ag["episode_jaccard"]["pooled"], "retention_kappa": ag["retention"]["kappa_R_vs_Rcj"],
          "retention_kappa_R_abs2_matched_definition": ag["retention"]["kappa_R_abs2_vs_Rcj"],
          "pooling_criteria_met": fa["pooling"]["n_met"],
          "o5_main_base_rate_heldout": core["base_rate_heldout"], "o5_main_base_rate_all": next(r["O5_main_rate"] for r in core["coverage_by_group"] if r["group"] == "ALL"),
          "o5_rho_O2r_pooled": main["rho_O2r_m50"]["pooled"], "o5_rho_O2r_pooled_ci_lo": main["rho_O2r_m50"]["ci95"][0],
          "o5_rho_O2r_pooled_ci_hi": main["rho_O2r_m50"]["ci95"][1], "o5_rho_O1_pooled": main["rho_O1"]["pooled"],
          "o5_rho_O1_pooled_ci_lo": main["rho_O1"]["ci95"][0], "o5_rho_O1_pooled_ci_hi": main["rho_O1"]["ci95"][1],
          "o5_rho_O2r_resid_pooled": main["rho_O2r_resid"]["pooled"], "o5_rho_logN_pooled": main["rho_log_N_outcome"]["pooled"],
          "o5_tax_rho_O2r_pooled": core["associations_pooled_heldout_DL"]["O5_tax"]["rho_O2r_m50"]["pooled"],
          "o5_share_recognised_at_or_before_t0": core["lag"]["_all_main_sources"]["n_excluded_recognised_at_or_before_t0"] / core["n_frame"],
          "o5_pos_precision": hc["positive_precision_strict"], "o5_pos_precision_lenient": hc["positive_precision_lenient_partial_counts"],
          "o5_neg_fn_rate": hc["negatives_false_negative_rate"], "o5_date_error_le1_share": hc["date_error_le_1y_share_all_checked"],
          "o5_executor_llm_kappa": hc["executor_vs_llm_kappa_same_concept"], "o5_fit_for_use": int(hc["FIT_FOR_USE"]),
          "llm_cost_usd": hc["llm"]["llm_cost_usd"],
          "next_field_LR_M1_vs_M0_reproduced": tr["trace"]["LR_M1_vs_M0_breslow"]["recomputed"],
          "next_field_LR_M2_vs_M0_reproduced": tr["trace"]["LR_M2_vs_M0_breslow"]["recomputed"],
          "next_field_LR_M2_vs_M0_exact": tr["trace"]["LR_M2_vs_M0_exact"]["recomputed"],
          "next_field_trace_matches": tr["n_trace_match"], "next_field_trace_checked": tr["n_trace_checked"]}
    for r in t3:
        k = r["row"].replace(".", "_")
        ma[f"t3_{k}_point"] = r["point_reproduced"]
        ma[f"t3_{k}_ci95_lo"] = r["ci95_refit"][0]
        ma[f"t3_{k}_ci95_hi"] = r["ci95_refit"][1]
    ma = {k.replace("-", "_").replace(".", "_"): float(v) for k, v in ma.items() if num(v) is not None}
    # ---------------- datasets
    ds = []
    ex = []
    for r in led.itertuples():
        e = {"input": s({"claim_id": r.claim_id, "draft_section": r.draft_section, "claim_text": r.claim_text, "quantity": r.quantity,
                         "reported_value": r.reported_value}),
             "output": s(r.source_value), "predict_status": str(r.status),
             "metadata_source_file": s(r.source_file), "metadata_key_path": s(r.key_path), "metadata_severity": r.severity,
             "metadata_artifact_id": r.artifact_id, "metadata_in_draft": bool(r.in_draft),
             "metadata_correction": s(r.correction_text) if isinstance(r.correction_text, str) else "",
             "eval_match": 1.0 if r.status in ("MATCH", "ROUNDING") else 0.0}
        if num(r.abs_diff) is not None:
            e["eval_abs_diff"] = float(r.abs_diff)
        ex.append(e)
    ds.append({"dataset": "claims_ledger", "examples": ex})
    ex = []
    for r in t3:
        ex.append({"input": s({"row": r["row"], "experiment": r["experiment"], "outcome": r["outcome"], "base": r["base_cols"], "cand": r["cand_cols"]}),
                   "output": s({"point_reported": r["point_reported"], "fixed_prediction_ci90": r["fixed_prediction_ci90"]}),
                   "predict_refit_bootstrap": s({"point": r["point_reproduced"], "ci90": r["ci90_refit"], "ci95": r["ci95_refit"], "B": r["B"]}),
                   "metadata_source_file": r["source_file"], "metadata_key_path": r["key_path"],
                   "eval_point_abs_diff": float(r["abs_diff"]), "eval_ci95_width": float(r["ci95_refit"][1] - r["ci95_refit"][0]),
                   **({"eval_ci_widening_ratio_90": float(r["ci_widening_ratio_90"])} if num(r["ci_widening_ratio_90"]) is not None else {})})
    ds.append({"dataset": "refit_bootstrap_iter1", "examples": ex})
    ex = []
    for k, v in tr["trace"].items():
        e = {"input": s({"quantity": k, "how": v.get("how")}), "output": s(v.get("reported")), "predict_recomputed": s(v.get("recomputed")),
             "metadata_source_file": s(v.get("source_file")), "metadata_key_path": s(v.get("key_path"))}
        if v.get("match") is not None:
            e["eval_match"] = 1.0 if v["match"] else 0.0
        ex.append(e)
    ds.append({"dataset": "next_field_trace", "examples": ex})
    # frame agreement per shared concept
    f5 = C.read_csv(C.E5 / "frame_concepts.csv")
    f6 = C.read_csv(C.E6 / "results/frame_concepts.csv")
    f5["id"] = f5.concept_id.map(C.norm_id)
    f6["id"] = f6.concept_id.map(C.norm_id)
    m = f5.merge(f6, on="id", suffixes=("_5", "_6"))
    ex = []
    for r in m.itertuples():
        h5 = int(float(str(r.home_5).replace("|", ";").split(";")[0]))
        ex.append({"input": s({"concept": r.id, "name": r.name_5, "exp5_split": r.split_5, "exp6_split": r.split_6}),
                   "output": s({"t0": r.t0_6, "home_primary": int(r.home_primary), "O2r_m50": r.O2r_m50}),
                   "predict_exp5_frame": s({"t0": r.t0_5, "home_primary": h5, "early_volume": r.early_volume}),
                   "metadata_group_exp5": r.group_5, "metadata_group_exp6": r.group_6,
                   "eval_onset_exact": float(r.t0_5 == r.t0_6), "eval_onset_abs_diff": float(abs(r.t0_5 - r.t0_6)),
                   "eval_home_agree": float(h5 == int(r.home_primary))})
    ds.append({"dataset": "frame_agreement_shared_concepts", "examples": ex})
    # O5 per concept (Exp5 frame)
    pan = C.read_csv(C.TAB / "o5_concept_panel.csv")
    ex = []
    for r in pan.itertuples():
        e = {"input": s({"concept": r.id, "name": r.name, "t0": int(r.t0), "group": r.gkey}),
             "output": s({"O1": r.O1, "O2r_m50": r.O2r_m50, "O3": r.O3}),
             "predict_O5_main": str(int(r.O5_main)), "predict_O5_wiki": str(int(r.O5_wiki)), "predict_O5_tax": str(int(r.O5_tax)),
             "metadata_split": r.split, "eval_O5_main": float(r.O5_main)}
        if num(r.O5_lag) is not None:
            e["eval_O5_lag"] = float(r.O5_lag)
        ex.append(e)
    ds.append({"dataset": "o5_exp5_frame", "examples": ex})
    it = C.read_csv(C.TAB / "o5_handcheck_items_final.csv")
    ex = []
    for r in it.itertuples():
        e = {"input": s({"item": r.item, "kind": r.kind, "concept": r.id, "name": r.name, "t0": r.t0, "source": r.source,
                         "entry_title": r.entry_title, "year": r.year}),
             "output": s({"final_same": getattr(r, "final_same", None), "final_fn": getattr(r, "final_fn", None)}),
             "predict_llm_same_concept": s(r.llm_same_concept), "predict_executor_same_concept": s(r.exec_same),
             "metadata_wiki_first_rev_year": s(r.wiki_first_rev_year), "metadata_bucket": r.bucket}
        if r.kind == "positive" and isinstance(getattr(r, "final_same", None), str):
            e["eval_positive_correct"] = 1.0 if r.final_same == "yes" else 0.0
        if r.kind == "negative" and isinstance(getattr(r, "final_fn", None), str):
            e["eval_false_negative"] = 1.0 if r.final_fn == "yes" else 0.0
        ex.append(e)
    ds.append({"dataset": "o5_hand_check", "examples": ex})
    meta = {"evaluation_name": "Checking the record before the paper (iteration-3 record audit)",
            "plan_id": "gen_plan_evaluation_1_idx4", "resampling_unit": "concept", "bootstrap": {"B": 2000, "seed": C.SEED},
            "path_convention": "source paths are relative to the run's 3_invention_loop directory; workspace outputs relative to this workspace",
            "dependencies": ["art_wxWssKSUR45f", "art_N-mpomDZZ1ln", "art_O7Dq4L02QnDN"],
            "read_by_path": ["art_lwI2DuRtQRZX", "iter_1 exp1/exp3/exp4", "iter_2 paper_draft.md", "iter_2 review_report"],
            "ledger_status_counts": st, "frame_agreement": {k: fa[k] for k in ("n_exp5", "n_exp6", "n_both", "pooling", "disagreement_attribution")},
            "exp5_minus_exp6": fa["exp5_minus_exp6"], "o5_readings": {v: p["reading"] for v, p in core["associations_pooled_heldout_DL"].items()},
            "o5_hand_check": {k: v for k, v in hc.items() if not isinstance(v, list)}, "o5_definitions": defs,
            "next_field_clashes": {k: tr[k] for k in ("strata_clash_resolution", "LR_clash_resolution", "d_clash_resolution")},
            "t3_refit": t3, "record_tables": sorted(p.name for p in C.TAB.iterdir()),
            "files": ["claims_ledger.csv", "frame_agreement.json", "o5_validation.json", "o5_definitions.json", "text_corrections.md",
                      "inputs_manifest.json", "record_tables/"]}
    out = {"metadata": C.jsonable(meta), "metrics_agg": ma, "datasets": ds}
    (C.WS / "eval_out.json").write_text(json.dumps(C.jsonable(out), indent=1))
    # combined inputs manifest
    man = {}
    for p in sorted(C.RES.glob("inputs_manifest_*.json")):
        man.update(json.loads(p.read_text()))
    (C.WS / "inputs_manifest.json").write_text(json.dumps(dict(sorted(man.items())), indent=1))
    logger.info(f"eval_out.json: {len(ma)} metrics, datasets {[ (d['dataset'], len(d['examples'])) for d in ds]}")
    return out


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stages", default="", help="'all' to rerun every work package before assembling")
    a = ap.parse_args()
    C.setup_logging("eval")
    if a.stages == "all":
        for st in STAGES:
            logger.info(f"running {st}")
            subprocess.run([sys.executable, *st], check=True, cwd=C.WS)
    assemble()


if __name__ == "__main__":
    main()
