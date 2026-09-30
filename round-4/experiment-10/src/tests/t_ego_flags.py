#!/usr/bin/env python3
"""U2: with n_null = 0 and compute_btw = False the six OPEN components (ALL build) equal EXP8 data/ego_features.parquet
to 1e-12 on 100 EXP5 concepts (data/ego_open_exp5_u2.parquet, produced by s7_ego.py --tag _u2)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
from common import EXP8, RES  # noqa: E402

COMP = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
mine = pd.read_parquet(ROOT / "data/ego_open_exp5_u2.parquet")
ref = pd.read_parquet(EXP8 / "data/ego_features.parquet", columns=["ci"] + COMP)
m = mine.merge(ref, on="ci")
out = {"n": len(m)}
ok = True
for k in COMP:
    a, b = m[f"{k}__all"].to_numpy(float), m[k].to_numpy(float)
    same_nan = bool(np.array_equal(np.isnan(a), np.isnan(b)))
    d = float(np.nanmax(np.abs(a - b))) if np.isfinite(a).any() else 0.0
    out[k] = {"max_abs_diff": d, "nan_pattern_equal": same_nan}
    ok &= same_nan and d <= 1e-12
out["pass"] = bool(ok)
(RES / "u2_ego_flags.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
sys.exit(0 if ok else 1)
