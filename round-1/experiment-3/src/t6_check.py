#!/usr/bin/env python3
"""T6: compare bootstrap CIs of two screen runs with different bootstrap seeds (results/screen_result.json vs
results/screen_result_seed2.json). Writes results/t6_bootstrap_stability.json."""
import json
from pathlib import Path

RES = Path(__file__).resolve().parent / "results"
a = json.loads((RES / "screen_result.json").read_text())
b = json.loads((RES / "screen_result_seed2.json").read_text())
out = {}
for k in a["candidates"]:
    for m in ["CI90", "CI95", "delta_AUC_O1_CI90", "delta_AUC_O2r_top_CI90"]:
        x, y = a["candidates"][k].get(m), b["candidates"][k].get(m)
        if x and y and None not in x and None not in y:
            out[f"{k}.{m}"] = {"seed1": x, "seed2": y, "max_abs_diff": max(abs(x[0] - y[0]), abs(x[1] - y[1]))}
mx = max(v["max_abs_diff"] for v in out.values())
res = {"check": "T6 bootstrap-seed stability (2,000 draws each; seeds 20260928 vs 20260929)",
       "max_abs_CI_endpoint_diff": mx, "pass": mx < 0.02, "details": out}
(RES / "t6_bootstrap_stability.json").write_text(json.dumps(res, indent=1))
print(f"T6 max |CI endpoint diff| = {mx:.4f}  pass={mx < 0.02}")
