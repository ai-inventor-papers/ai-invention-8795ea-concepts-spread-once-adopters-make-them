#!/usr/bin/env python3
"""Consolidated deliverable results/cohort_report.json: verdict + clause table, primary ladder, groups, within type,
power / MDE, secondary, placebos, audits (S2 T1-T3, S3, U-tests, post-unseal audit), type benchmark, LLM spend.
results/cohort_result.json itself is left untouched (its sha256 is in logs/seal.log)."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import RES, jdump

L = lambda n: json.loads((RES / n).read_text())  # noqa: E731
res, spec = L("cohort_result.json"), L("frozen_spec.json")
with (RES / "llm_cost_log.csv").open() as f:
    rows = list(csv.DictReader(f))
spend = {}
for r in rows:
    tag = r["tag"].split(":")[0]
    spend[tag] = spend.get(tag, 0.0) + float(r["cost"] or 0)
pw = spec["power"]
rep = {
    "question": "Does an open early ego-neighbourhood (OPEN, t0..t0+2) anticipate later disciplinary breadth "
                "(O2r_m50, t0+6..t0+8) beyond size/growth/breadth, concept type, pre-onset footprint, coverage and field, "
                "on a fresh 2015-2017 onset cohort scored once from a sealed spec?",
    "verdict": res["verdict"],
    "headline": {k: res["primary"][k] for k in ("OPEN_home|O2r_m50|R2", "OPEN_home|O2r_m50|R3", "OPEN_home|O2r_resid|R2",
                                                "OPEN_all|O2r_m50|R2", "OPEN_sizematch|O2r_m50|R2")},
    "n_cohort": res["n_cohort"], "n_by_t0": res["n_by_t0"], "outcome_availability": res["outcome_availability"],
    "resampling_unit": "concept", "bootstrap_B": res["B"],
    "power_pre_seal": {"base_2015_2016": {k: pw["base_2015_2016"][k] for k in ("power_ci_gt0", "n_expected",
                                                                                "MDE_2.8SE_analytic", "within_type")},
                       "with_2017": {k: pw["with_2017"][k] for k in ("power_ci_gt0", "n_expected", "MDE_2.8SE_analytic",
                                                                     "within_type")} if pw["with_2017"] else None,
                       "extension_applied": pw["extension"]},
    "primary_ladder": res["primary"], "groups": res["groups"], "within_type": res["within_type"],
    "components": res["components"], "retention_ratio": res["retention"], "build_contrasts": res["contrasts"],
    "holm": res["holm"], "secondary": res["secondary"], "sensitivity": res["sensitivity"], "placebos": res["placebos"],
    "learned_models_frozen_exp8": L("learned_models_cohort.json"),
    "audits": {"S2_checks": L("s2_checks.json"), "S3_decision": L("s3_decision.json"), "post_unseal_audit": L("audit.json"),
               "unit_tests": L("unit_tests.json"), "U2_ego_flags": L("u2_ego_flags.json"),
               "U5_outcomes": L("u5_outcomes.json"), "U8_prompt_identity": L("u8_prompt_identity.json"),
               "learned_port_validation": L("learned_port_validation.json")},
    "type_benchmark": L("type_benchmark_final.json"),
    "precision_gate": L("s4_gate_summary.json"),
    "llm_spend_usd": {"total": sum(spend.values()), "by_stage": spend,
                      "note": "OpenRouter usage.cost ledger (results/llm_cost_log.csv); OpenAlex credits: 0"},
    "exp5_selection_summary": {k: v for k, v in L("exp5_selection_result.json").items()
                               if k in ("coupling", "sign_check_R0_all_build", "open_finite_share",
                                        "open_finite_share_cohort", "smd_cohort_vs_exp5")},
    "seal": {"frozen_spec_sha256": json.loads(Path("logs/unsealed.json").read_text())["frozen_spec_sha256"],
             "seal_log": "logs/seal.log (hash-chained JSON lines: S0_prereg, S8_freeze, S9_unseal, S9_outcomes, S9_scored)"},
    "deviations": L("deviations.json"),
}
jdump(rep, RES / "cohort_report.json")
print("total LLM spend", round(sum(spend.values()), 3), spend)
