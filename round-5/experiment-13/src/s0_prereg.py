#!/usr/bin/env python3
"""S0: write results/frozen_spec_v0.json (EXP10 frozen constants copied verbatim + Frame-N rules) and hash-chain
prereg.md, the spec, the mining code and every copied input into logs/seal.log (record S0_prereg)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import INPUTS, LOGS, RES, ROOT, jdump, setup_logger, sha256_file
from nrules import FILLER, GENERIC
from sealn import record

logger = setup_logger("s0_prereg")


def main() -> None:
    ex = json.loads((INPUTS / "exp10_frozen_spec.json").read_text())
    spec = {
        "source": "EXP10 results/frozen_spec.json (constants copied verbatim)",
        "open_constants": ex["open_constants"], "open_min_home_papers": ex["open_min_home_papers"],
        "open_min_components": ex["open_min_components"], "O2r_resid": ex["O2r_resid"],
        "groups": ex["groups"], "bootstrap": ex["bootstrap"], "prediction_models": ex["prediction_models"],
        "exp10_rungs": ex["rungs"],
        "mining": {"file_sample": "fi % 5 == 0", "years": [2000, 2017], "ngram_n": [2, 3],
                   "token_valid": "^(?=.*[a-z])[a-z0-9]{2,}$", "filler": FILLER, "generic": GENERIC,
                   "candidate_rule": "s_t >= k_t and max(s_{t-3..t-1}) <= floor(0.25 s_t)",
                   "k_t": "max(3, smallest k with |cand_t after exclusions| <= 4500)",
                   "pos_rule": "(ADJ|NOUN|PROPN)* (NOUN|PROPN) in >= 60% of <= 5 contexts; trigram middle ADP/CCONJ/DET ok"},
        "onset": {"years": [2003, 2014], "min_N": 20, "newborn_ratio": 0.25, "selection_clause": "t_det <= t0+2",
                  "extension": {"t0": 2015, "shift": 1}},
        "gate": {"model": "google/gemini-2.5-flash-lite", "m2": "openai/gpt-4.1-mini", "titles": 20,
                 "seed": "7919+ci", "keep": "specific and sense_share >= 0.8 and not generic", "cap_usd": 1.35},
        "home_rule": {"share": 0.4, "first_n": 30},
        "rungs": {
            "R0": {"cont": ["logvol", "growth_c", "offhome_share", "entropy", "reach"], "cat": ["t0 dummies ref 2008"]},
            "R1": {"add_cont": ["CONTACT_REACH"]},
            "R2": {"add_cat": ["type_method", "type_object", "type_property", "generic"]},
            "R3": {"add_cont": ["fp_logN", "fp_nfields"]},
            "R4": {"add_cont": ["label_coverage_early", "home_coverage_early"]},
            "R5": {"add_cat": ["home-group FE ref BGM+Med"]}},
        "primary": "OPEN_home | O2r_m50 (MATCH, t0+6..t0+8)",
        "holm_family": ["OPEN_home|O2r_m50|R3", "OPEN_home|O2r_m50|R5", "NOVCHURN_home|O2r_m50|R3",
                        "CHENG_consistency_home|O2r_m50|R0", "OPEN_all-OPEN_home|O2r_m50|R3"],
        "directions": {"OPEN_home|O2r_m50|R3": 1, "OPEN_home|O2r_m50|R5": 1, "NOVCHURN_home|O2r_m50|R3": 1,
                       "CHENG_consistency_home|O2r_m50|R0": -1, "OPEN_all-OPEN_home|O2r_m50|R3": 1},
        "fallbacks": {"A": "n(finite O2r_m50 & OPEN_home) < 800 -> O2r_m30", "E": "expected n < 800 -> add t0=2015",
                      "power_cap": "power < 0.5 -> verdict capped at PARTIAL"},
    }
    jdump(spec, RES / "frozen_spec_v0.json")
    # input hashes
    lines = []
    for p in sorted(list(INPUTS.rglob("*")) + list((ROOT / "lib").glob("*.py")) + list((ROOT / "ref").rglob("*.py"))):
        if p.is_file():
            lines.append(f"{sha256_file(p)}  {p.relative_to(ROOT)}")
    (LOGS / "inputs.sha256").write_text("\n".join(lines) + "\n")
    rec = record("S0_prereg", prereg_sha256=sha256_file(ROOT / "prereg.md"),
                 spec_v0_sha256=sha256_file(RES / "frozen_spec_v0.json"),
                 nrules_sha256=sha256_file(ROOT / "lib/nrules.py"), passM_sha256=sha256_file(ROOT / "passM.py"),
                 inputs_sha256_file=sha256_file(LOGS / "inputs.sha256"))
    logger.info(f"S0 recorded: {rec}")


if __name__ == "__main__":
    main()
