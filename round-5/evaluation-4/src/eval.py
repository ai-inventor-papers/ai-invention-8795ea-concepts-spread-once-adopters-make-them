#!/usr/bin/env python3
"""Iteration-5 evaluation 4 driver: record repair (10 MUST-FIX items), Eval3 corrections applied, ledger
re-verification, and a descriptive OPEN_home / NOVCHURN_home evidence synthesis. Zero new data, $0 LLM.

Steps (each a script in src/, run in order unless --assemble-only):
  P0/P2 src/synthesis.py          gates G1/G2 (reproduce Exp10 psp) + item 11 cells and pools
  P1    src/build_corrections.py  items 1-4, 6-11 -> corrections_iter5/*.md + results/claims_ledger_v4.csv
  P3    src/apply_corrections.py  item 5: Eval3 pack + iteration-5 blocks -> report_corrected.md
        src/refs.py               item 10 references -> references_master.json|md (+ in-text renumbering)
        src/figures.py            figures/evidence_forest.png|pdf
  P4    src/checks.py             G3 + ledger v3/v4 verification, text presence, stale strings, verbatim diffs
then assembles eval_out.json (exp_eval_sol_out) with mini / preview variants.
Usage: uv run eval.py [--assemble-only] [--nboot 2000]"""
from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS / "src"))

from loguru import logger

from paths import RES, jdump, rel, sha256  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WS / "logs/eval.log", rotation="30 MB", level="DEBUG")


def run(script: str, *args: str) -> None:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1")
    logger.info(f"running {script} {' '.join(args)}")
    r = subprocess.run([sys.executable, str(WS / script), *args], env=env, capture_output=True, text=True)
    (WS / "logs" / f"{Path(script).stem}_stdout.log").write_text(r.stdout + r.stderr)
    if r.returncode:
        raise RuntimeError(f"{script} failed:\n{r.stderr[-1500:]}")


def inputs_manifest() -> dict:
    from paths import (DS2, E8, E10, E11, E12, EVAL3, EXP5, EXP7, R1, R2, R3, REPORT4, REPORT5)
    files = [REPORT5, REPORT4, EVAL3 / "verify_ledger.py", EVAL3 / "results/claims_ledger_v3.csv",
             EVAL3 / "results/boundary_spec.json", EVAL3 / "results/drca_persist_comparison.json",
             EVAL3 / "results/heterogeneity.json", EVAL3 / "results/spec_curve.json",
             E12 / "results/case_pairs.json", E12 / "results/preregistration_R2.json",
             E12 / "results/decomposition_dev.json", E12 / "results/decomposition_heldout.json",
             E12 / "results/sequence_light_dev.json", E12 / "results/sequence_light_heldout.json",
             E12 / "results/trajectories_dev.json", E12 / "results/trajectories_heldout.json",
             E12 / "ai_atlas/atlas.json", E10 / "README.md", E10 / "results/cohort_report.json",
             E10 / "results/cohort_result.json", E10 / "results/learned_models_cohort.json",
             E10 / "results/exp5_selection_result.json", E10 / "results/frozen_spec.json", E10 / "prereg.md",
             E10 / "data/ego_open_exp5.parquet", E10 / "data/covariates_exp5.parquet",
             E10 / "data/concept_types.csv", E10 / "data/analysis_cohort.parquet", E10 / "lib/ladder.py",
             E10 / "lib/rq1stats.py", E11 / "prereg.md", E11 / "results/fe_results.json",
             E11 / "results/deviations.json", E11 / "logs/analysis_fe.log", E11 / "logs/event_study.out",
             E11 / "logs/event_study.log", E11 / "logs/partners.log", E8 / "results/heldout_unit_results.csv",
             E8 / "results/rq1_heldout.json", E8 / "results/heldout_summary.json", E8 / "data/outcomes.parquet",
             EXP7 / "results/step2_heldout.json", EXP7 / "results/step2_dev.json", EXP5 / "frame_concepts.csv",
             R1 / "research_out.json", R2 / "references_new.json", R3 / "research_out.json",
             R3 / "raw/verify.json"]
    out = []
    for f in files:
        out.append({"path": rel(f), "exists": f.exists(), "bytes": f.stat().st_size if f.exists() else None,
                    "sha256": sha256(f) if f.exists() else None,
                    "mtime": f.stat().st_mtime if f.exists() else None})
    return {"n": len(out), "all_exist": all(o["exists"] for o in out), "files": out}


def fmt_ci(c):
    return f"[{c[0]:+.3f}, {c[1]:+.3f}]"


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assemble-only", action="store_true")
    ap.add_argument("--nboot", default="2000")
    a = ap.parse_args()
    man = inputs_manifest()
    jdump(RES / "inputs_manifest.json", man)
    if not man["all_exist"]:
        raise FileNotFoundError([f["path"] for f in man["files"] if not f["exists"]])
    if not a.assemble_only:
        run("src/synthesis.py", "--nboot", a.nboot, "--nperm", "200", "--workers", "3")
        run("src/build_corrections.py")
        run("src/apply_corrections.py")
        run("src/refs.py")
        run("src/figures.py")
        run("src/checks.py")
    syn = json.loads((RES / "evidence_synthesis.json").read_text())
    chk = json.loads((RES / "ledger_rerun.json").read_text())
    app = list(csv.DictReader(open(RES / "corrections_applied.csv")))
    refs = json.loads((RES / "refs_summary.json").read_text())
    g1, g2 = syn["gates"]["G1"], syn["gates"]["G2"]
    v3, v4 = chk["a_v3_reverify"], chk["b_v4"]
    g3 = (v3["n_rows"] == 1290 and v3["n_mismatch_recomputed"] == 0 and v3["n_not_found_recomputed"] == 0
          and v3["n_orphan_numeric_tokens"] == 9)
    gates = {"G0_inputs_exist": man["all_exist"], "G1_R0": g1["pass_R0"], "G1_R2": g1["pass_R2"], "G2": g2["pass"],
             "G3": g3}
    jdump(RES / "gates.json", {"gates": gates, "G1": g1, "G2": {k: v for k, v in g2.items()},
                               "G3": {k: v3[k] for k in ("n_rows", "recomputed_status_counts", "n_mismatch_recomputed",
                                                         "n_not_found_recomputed", "n_orphan_numeric_tokens")}})
    st = {}
    for r in app:
        st[r["status"]] = st.get(r["status"], 0) + 1
    by = {(r["source_file"], r["block_id"]): r["status"] for r in app}

    def ok(fn, *bids):
        return all(by.get((fn, b)) == "APPLIED" for b in bids)

    verb = chk["e_verbatim"]
    stale = chk["d_stale"]
    eval3_missing = sum(1 for r in app if r["status"] == "NOT_APPLIED_TARGET_MISSING")
    mustfix = {
        "1_case_studies_26_4": ok("01_case_studies_26_4.md", "26.4_rebuilt", "26.5_atlas") and stale["n_stale_hits"] == 0,
        "2_exp11_25a": ok("02_exp11_25a.md", "25a_exp11", "29_deadend_exp11", "28.1_c4", "24_counts", "31_counts")
        and verb["Exp11_HM1_HP1_lines_24_32_verbatim"],
        "3_exp10_rewrite": ok("03_exp10_rewrite.md", "25.1", "25.2", "25.4", "25.7", "25.8", "31.1"),
        "4_exp12_rewrite": ok("04_exp12_rewrite.md", "26.1", "26.3", "26.2_pc", "31.3_caveat")
        and all(verb[f"{k}_verbatim"] for k in ("PR1", "PR1b", "PR2", "PR3")),
        "5_eval3_application": eval3_missing == 0 and ok("05_eval3_application.md", "27.6_list"),
        "6_section23_restore": ok("06_section23_restore.md", "23_restore", "16.2_tag") and verb["section23_byte_identical"],
        "7_section28_evidence": ok("07_section28_evidence.md", "28.1_evidence", "28.2_survives", "31.2_retention"),
        "8_secondary": ok("08_exp8_exp10_secondary.md", "25.5_leads", "25.6", "19.5b_tag", "19.7_tag", "19.2_pergroup")
        and verb["Exp10_leads_block_lines_48_53_verbatim"],
        "9_coverage_table_30": ok("09_coverage_table_30.md", "30_table"),
        "10_minor_and_refs": ok("10_minor_and_refs.md", "fcr", "27.3_I2", "27.2_label") and stale["n_stale_hits"] == 0
        and refs["n_master"] > 0}
    rows = {(r["body"], r["feature"]): r for r in syn["rows"]}
    m = {"n_mustfix_cleared": sum(mustfix.values()), "n_mustfix_total": len(mustfix),
         "ledger_v3_rows": v3["n_rows"], "ledger_v3_mismatch": v3["n_mismatch_recomputed"],
         "ledger_v3_not_found": v3["n_not_found_recomputed"], "ledger_v3_orphans": v3["n_orphan_numeric_tokens"],
         "ledger_v4_rows": v4["n_rows"], "ledger_v4_mismatch": v4["n_mismatch_recomputed"],
         "ledger_v4_not_found": v4["n_not_found_recomputed"], "ledger_v4_orphans": v4["n_orphan_numeric_tokens"],
         "ledger_v4_disagreements": v4["n_disagreements"],
         "text_present_v3": chk["c_text_presence"]["v3"]["counts"].get("TEXT_PRESENT", 0),
         "text_present_elsewhere_v3": chk["c_text_presence"]["v3"]["counts"].get("TEXT_PRESENT_ELSEWHERE", 0),
         "text_absent_v3": chk["c_text_presence"]["v3"]["counts"].get("TEXT_ABSENT", 0),
         "text_present_v4": chk["c_text_presence"]["v4"]["counts"].get("TEXT_PRESENT", 0),
         "text_absent_v4": chk["c_text_presence"]["v4"]["counts"].get("TEXT_ABSENT", 0)
         + chk["c_text_presence"]["v4"]["counts"].get("TEXT_PRESENT_ELSEWHERE", 0),
         "stale_hits": stale["n_stale_hits"], "stale_correction_note_mentions": stale["n_correction_note_mentions"],
         "verbatim_checks_passed": sum(verb.values()), "verbatim_checks_total": len(verb),
         "gate_G0_pass": int(gates["G0_inputs_exist"]), "gate_G1_R0_pass": int(gates["G1_R0"]),
         "gate_G1_R2_pass": int(gates["G1_R2"]), "gate_G2_pass": int(gates["G2"]), "gate_G3_pass": int(gates["G3"]),
         "G1_open_home_R0_recomputed": g1["OPEN_home|O2r_m50|R0"]["recomputed"],
         "G1_open_home_R2_recomputed": g1["OPEN_home|O2r_m50|R2"]["recomputed"],
         "G2_cohort_open_home_R2": g2["R2"]["rho"], "G2_cohort_open_home_R3": g2["R3"]["rho"],
         "corrections_applied": st.get("APPLIED", 0), "corrections_already_present": st.get("ALREADY_PRESENT", 0),
         "corrections_not_applied_target_missing": st.get("NOT_APPLIED_TARGET_MISSING", 0),
         "corrections_not_applied_superseded": st.get("NOT_APPLIED_SUPERSEDED", 0),
         "references_master_n": refs["n_master"], "references_cited_n": refs["n_cited"],
         "references_excluded_unverified_n": refs["n_excluded"]}
    short = {"B1_DEV": "B1_dev", "B2_HELDOUT_pooled": "B2_heldout_pooled", "B3_EXP5_COHORT_2010_14": "B3_cohort1014",
             "B4_COHORT_2015_17": "B4_cohort1517", "B2_PHYS": "B2_phys", "B2_LIFEENV": "B2_lifeenv", "B2_SOC": "B2_soc",
             "B2_MATHDEC": "B2_mathdec"}
    for (b, f), r in rows.items():
        if b in short and r["R2"]["psp"] is not None:
            m[f"psp_R2_{f}_{short[b]}"] = r["R2"]["psp"]
    for f in ("OPEN_home", "NOVCHURN_home"):
        for rung in ("R0", "R2", "R3"):
            p = syn["pools"][f"{f}|{rung}"]
            n = p["nonselection"]
            tag = f"{f}_{rung}"
            m[f"pooled_nonselection_{tag}"] = n["est"]
            m[f"pooled_nonselection_{tag}_dl_lo"], m[f"pooled_nonselection_{tag}_dl_hi"] = n["dl_ci"]
            m[f"pooled_nonselection_{tag}_hksj_lo"], m[f"pooled_nonselection_{tag}_hksj_hi"] = n["hksj_ci"]
            m[f"pooled_nonselection_{tag}_I2"] = n["I2"]
            m[f"pooled_nonselection_{tag}_tau2_z"] = n["tau2_z"]
            m[f"pooled_nonselection_{tag}_k"] = n["k"]
            m[f"pooled_all_bodies_{tag}"] = p["all_bodies_includes_selection_data"]["est"]
            m[f"shrinkage_selection_over_nonselection_{tag}"] = p["shrinkage_ratio_selection_over_nonselection"]
            k_pos, k_all = p["sign_agreement_nonselection"].split("/")
            m[f"sign_agreement_nonselection_{tag}_pos"] = int(k_pos)
            m[f"sign_agreement_nonselection_{tag}_k"] = int(k_all)
    # ---------------- datasets
    ds_syn = []
    for r in syn["rows"]:
        for rung in ("R0", "R2", "R3"):
            if rung not in r:
                continue
            c = r[rung]
            ds_syn.append({"input": f"body={r['body']} | feature={r['feature']} | outcome=O2r_m50 | rung={rung} | "
                                    f"status={r['status']}",
                           "output": ("pending iteration-5 artifact" if c["psp"] is None else
                                      f"psp {c['psp']:+.3f} {fmt_ci(c['ci'])} n={c['n']}"),
                           "metadata_body": r["body"], "metadata_feature": r["feature"], "metadata_rung": rung,
                           "metadata_status": r["status"], "metadata_n": c.get("n"),
                           **({"eval_psp": c["psp"], "eval_ci_lo": c["ci"][0], "eval_ci_hi": c["ci"][1]}
                              if c["psp"] is not None else {}),
                           **({"eval_placebo_p95_abs_psp": r["placebo"]["p95_abs_psp"]}
                              if "placebo" in r and rung == "R2" else {})})
    pg = list(csv.DictReader(open(RES / "per_group_table.csv")))
    ds_pg = [{"input": f"indicator={r['indicator']} | unit={r['unit']} | outcome=O2r_m50 (EXP8 held-out)",
              "output": f"psp {float(r['psp']):+.3f} [{float(r['ci_lo']):+.3f}, {float(r['ci_hi']):+.3f}] "
                        f"n={r['n']}{' (CI includes 0)' if r['ci_includes_0'] == 'True' else ''}",
              "metadata_indicator": r["indicator"], "metadata_unit": r["unit"],
              "eval_psp": float(r["psp"]), "eval_ci_lo": float(r["ci_lo"]), "eval_ci_hi": float(r["ci_hi"]),
              "eval_n": int(r["n"]), "eval_ci_includes_0": int(r["ci_includes_0"] == "True")} for r in pg]
    ds_app = [{"input": f"{r['source_file']} :: {r['block_id']} -> {r['target_section']} ({r['action']})",
               "output": f"{r['status']}: {r['reason']}", "metadata_source_file": r["source_file"],
               "metadata_status": r["status"],
               "eval_applied": int(r["status"] == "APPLIED"),
               "eval_line_in_corrected": int(r["line_in_corrected_final"])} for r in app]
    out = {"metadata": {
        "evaluation_name": "Fix the record and pool the openness evidence (iteration 5, evaluation 4)",
        "plan": "3_invention_loop/iter_5/gen_plan/gen_plan_evaluation_1",
        "llm_spend_usd": 0.0, "openalex_credit": 0, "new_data": False, "unseal": False,
        "mustfix": mustfix, "gates": gates,
        "estimator": syn["design"]["estimator"], "synthesis_design": syn["design"],
        "status_labels": {"selection": "data on which the index / constants were chosen",
                          "already-unsealed": "held-out data whose outcomes earlier artifacts had read",
                          "confirmatory": "never used before the test",
                          "pending iteration-5 artifact": "Frame N slot, empty"},
        "not_claimed": ["no new confirmation: the pooled estimate is descriptive and uses already-unsealed bodies",
                        "NOVCHURN_home on the 2015-17 cohort is a selection estimate",
                        "the ledger checks numbers against files, not the reasoning around them"],
        "not_found_notes": json.loads((RES / "not_found_notes.json").read_text()),
        "deviations": [
            "bootstrap seed = Exp10's frozen 20260929 (plan said 0) so every CI is comparable with the record; G2 was "
            "also run with seed 0 (CI within +-0.005, reported in results/gates_g1_g2.json)",
            "DL pooling on Fisher z (plan) whereas Exp10 pooled raw psp; reported values are back-transformed",
            "the 37-concept AI atlas is atlas.json -> concepts (ai_atlas/table.csv is the per-measure median table)",
            "the OPEN~PC1/PC2 table is read from trajectories_dev/heldout.json (open_diagnostics.json has no PC table)",
            "reference de-duplication uses first-author surname + year + first 5 words of the title head (before "
            "':' or '?') and a prefix pass, because the end-of-report list abbreviates titles",
            "Eval3 blocks already present with >= 90% of their numbers are marked ALREADY_PRESENT; partial ones are "
            "appended in full with a note",
            "the review's 'Exp8 raw sign flip +0.143 / -0.126' is not in any file (NOT_FOUND) and is not used"],
        "artifact_counts": json.loads((RES / "artifact_counts.json").read_text()),
        "references": refs},
        "metrics_agg": {k: float(v) for k, v in m.items() if v is not None},
        "datasets": [{"dataset": "evidence_synthesis", "examples": ds_syn},
                     {"dataset": "per_group_table_exp8_O2r_m50", "examples": ds_pg},
                     {"dataset": "corrections_applied", "examples": ds_app}]}
    jdump(WS / "eval_out.json", out)
    jdump(WS / "full_eval_out.json", out)
    mini = dict(out, datasets=[dict(d, examples=d["examples"][:3]) for d in out["datasets"]])
    jdump(WS / "mini_eval_out.json", mini)

    def trunc(o):
        if isinstance(o, str):
            return o[:200]
        if isinstance(o, list):
            return [trunc(x) for x in o]
        if isinstance(o, dict):
            return {k: trunc(v) for k, v in o.items()}
        return o
    jdump(WS / "preview_eval_out.json", trunc(mini))
    logger.info(f"must-fix cleared {m['n_mustfix_cleared']}/10: {mustfix}")
    logger.info(f"gates {gates}; metrics {len(m)}")


if __name__ == "__main__":
    main()
