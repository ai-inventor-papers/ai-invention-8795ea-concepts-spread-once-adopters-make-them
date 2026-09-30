#!/usr/bin/env python3
"""U1: make_method_out() on 3 stub rows writes a file that validates as exp_gen_sol_out (aii-json validator)."""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
from outjson import make_method_out  # noqa: E402

rows = [{"label": "Stub concept A", "openalex_id": 123, "t0": 2015, "group": "SOC", "O2r_m50": 3.2, "pred_b5": 2.9,
         "pred_b5_open": 3.0, "meta_type": "method", "meta_OPEN_home": 0.1, "meta_O1c": float("nan")},
        {"label": "Stub B", "openalex_id": 456, "t0": 2016, "group": "PHYS", "O2r_m50": float("nan"), "pred_b5": 1.0,
         "pred_b5_open": None, "meta_type": None},
        {"label": "Stub C", "openalex_id": 789, "t0": 2016, "group": "BGM+Med", "O2r_m50": 5.0, "pred_b5": 4.0,
         "pred_b5_open": 4.5}]
out = ROOT / "tests" / "stub_method_out.json"
out.write_text(json.dumps(make_method_out(rows, {"method_name": "stub"}), indent=1))
import os  # noqa: E402

skill = Path(os.environ.get("AII_JSON_SKILL_DIR", "")) if os.environ.get("AII_JSON_SKILL_DIR") else None
if skill and (skill / "scripts/aii_json_validate_schema.py").exists():   # AI Inventor validator, when available
    r = subprocess.run([str(skill.parent / ".ability_client_venv/bin/python"), str(skill / "scripts/aii_json_validate_schema.py"),
                        "--format", "exp_gen_sol_out", "--file", str(out)], capture_output=True, text=True)
    print(r.stdout[-400:], r.stderr[-400:])
    sys.exit(0 if "PASSED" in r.stdout else 1)
# portable fallback: structural check of the exp_gen_sol_out schema
d = json.loads(out.read_text())
ok = isinstance(d.get("datasets"), list) and d["datasets"] and all(
    set(ds) <= {"dataset", "examples"} and ds["examples"] and all(
        isinstance(e["input"], str) and isinstance(e["output"], str) and all(
            k in ("input", "output") or k.startswith("metadata_") or (k.startswith("predict_") and isinstance(v, str))
            for k, v in e.items()) for e in ds["examples"]) for ds in d["datasets"])
print("structural exp_gen_sol_out check:", "PASSED" if ok else "FAILED")
sys.exit(0 if ok else 1)
