"""U1: make_method_out() on 3 stub rows validates as exp_gen_sol_out (aii-json schema, checked with jsonschema)."""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

from outputs import make_method_out  # noqa: E402

# optional: the pipeline's aii-json skill folder (validator script); the schema itself is vendored in tests/
SKILL = Path(os.environ["AII_JSON_SKILL_DIR"]) if os.environ.get("AII_JSON_SKILL_DIR") else None


def stub() -> pd.DataFrame:
    return pd.DataFrame({
        "ci": [1, 2, 3], "t0": [2005, 2011, 2016], "name": ["A", "B", "C"], "group": ["CS", "Med", "SOC"],
        "group5": ["CS+Eng", "BGM+Med", "SOC"], "body": ["DEV", "COHORT_2010_14", "COHORT_2015_17"],
        "CONS_early_home": [0.4, np.nan, 0.2], "CONS_early_all": [0.5, 0.3, 0.1], "CONS_r_early_home": [0.5, np.nan, 0.3],
        "EMB_early_home": [0.9, 1.1, np.nan], "SOC_early_home": [0.1, 0.0, 0.3], "V_t0p2": [30.0, 40.0, 50.0],
        "V_t0p3": [35.0, 41.0, np.nan], "O2r_m50": [4.2, np.nan, 5.0], "O2r_resid": [0.1, np.nan, 0.3],
        "O1c": [0.2, 0.1, -0.3], "O1b": [1.0, 0.0, 1.0], "O3": [0.0, 0.0, 1.0]})


def test_u1_stub_validates(tmp_path: Path) -> None:
    out = make_method_out(stub(), np.array([4.0, 4.5, np.nan]), np.array([4.1, 4.4, np.nan]))
    p = tmp_path / "method_out.json"
    p.write_text(json.dumps(out, allow_nan=False))
    schema = json.loads((Path(__file__).parent / "exp_gen_sol_out.schema.json").read_text())
    import jsonschema
    jsonschema.validate(out, schema)
    py = SKILL.parent / ".ability_client_venv/bin/python" if SKILL else None
    if py is not None and py.exists():
        r = subprocess.run([str(py), str(SKILL / "scripts/aii_json_validate_schema.py"), "--format", "exp_gen_sol_out",
                            "--file", str(p)], capture_output=True, text=True, timeout=120)
        assert "PASSED" in r.stdout, r.stdout + r.stderr
