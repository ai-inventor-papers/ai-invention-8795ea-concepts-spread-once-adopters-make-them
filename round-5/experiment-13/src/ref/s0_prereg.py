#!/usr/bin/env python3
"""S0: machine-readable pre-registration (results/frozen_spec_v0.json) + hash record in logs/seal.log."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import RES, ROOT, jdump, sha256_file
from ladder import B5, BUILDS, COMPONENTS, COVERAGE, FOOTPRINT, FOOTPRINT_BIN, MIN_HOME_PAPERS, POOL_GROUPS, SIGNS
from seal2 import record

spec = {
    "OPEN": {"components": COMPONENTS, "signs": SIGNS, "winsor_pct": [0.5, 99.5], "min_components": 4,
             "z_constants": "per build, on the 12,499 EXP5 concepts (finite values)", "builds": BUILDS,
             "home_min_papers_t0_t0p2": MIN_HOME_PAPERS, "home_min_sensitivity": [5, 20],
             "sizematch": {"draws": 20, "seed": "1000 + ci", "windows": ["PRE", "W1", "W2", "W3"]},
             "ego_flags": {"n_null": 0, "compute_btw": False}},
    "outcomes": {"primary": "O2r_m50", "co": "O2r_resid", "window": "t0+6..t0+8",
                 "O2r_resid_exp8_frozen": {"a": 2.7410366547641205, "b": 0.3966308230599589},
                 "secondary": ["O1c", "O1b", "O3"], "O4": "not computed (no citation pass)"},
    "S3_rule": {"tag_rate_ratio_min": 0.90, "years": [2021, 2022, 2023, 2024], "ref_years": [2017, 2018, 2019],
                "match_validation_min_spearman": 0.90},
    "rungs": {"R0": {"cont": B5, "cat": ["onset-year dummies", "window flag"]}, "R1": "+CONTACT_REACH",
              "R2": "+type dummies (method/object/property/unlabelled; topic ref) + generic + level dummies",
              "R3": {"cont": FOOTPRINT, "cat": FOOTPRINT_BIN}, "R4": {"cont": COVERAGE}, "R5": "+home-group dummies"},
    "groups": POOL_GROUPS, "report_only": ["MATHDEC"],
    "bootstrap": {"B": 2000, "seed": 20260929, "unit": "concept"},
    "holm_family": [f"{x}|{y}" for x in ["OPEN_home", "OPEN_all", "OPEN_sizematch", "RETENTION_RATIO_early"]
                    for y in ["O2r_m50", "O2r_resid"]],
    "verdict": "see prereg.md",
    "extension_rule": {"n_min": 800, "power_min": 0.80, "effect_assumed": "half of EXP5 selection estimate"},
    "type_gate": {"min_precision_method_object": 0.85, "gold_n": 60, "bench_n": 300},
}
jdump(spec, RES / "frozen_spec_v0.json")
code = {p.relative_to(ROOT).as_posix(): sha256_file(p) for p in sorted(list(ROOT.glob("*.py")) + list(ROOT.glob("lib/*.py")))}
rec = record("S0_prereg", prereg_sha256=sha256_file(ROOT / "prereg.md"),
             spec_v0_sha256=sha256_file(RES / "frozen_spec_v0.json"), code_sha256=code)
print(rec["stage"], rec["prereg_sha256"][:16], rec["spec_v0_sha256"][:16])
