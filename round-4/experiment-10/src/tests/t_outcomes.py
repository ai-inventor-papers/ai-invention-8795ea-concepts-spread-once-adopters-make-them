#!/usr/bin/env python3
"""U5: lib/outc.outcomes reproduces EXP8 data/outcomes.parquet (O1c, O1b, O3, O2r_m50, O2r_m30) on 200 EXP5 concepts,
and O2r_resid with the frozen a/b reproduces EXP8's O2r_resid."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import numpy as np
import pandas as pd

from common import EXP5, EXP8, RES, load_frame
from outc import outcomes

fr = load_frame()
o8 = pd.read_parquet(EXP8 / "data/outcomes.parquet")
s = fr.sample(200, random_state=5)
ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet")
ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(s.ci))]
G = np.load(EXP5 / "scan/year_field_totals.npz")["G"].astype(float)
lv = pd.read_csv(EXP5 / "concept_features_basic.csv", usecols=["ci", "logvol"]).set_index("ci").logvol
rows = []
for r in s.itertuples():
    d = ag[ag.ci == r.ci]
    N = np.zeros(28); V = np.zeros((28, 27))
    np.add.at(N, d.year - 1995, d.n); np.add.at(V, (d.year - 1995, d.vfield), d.n)
    o = outcomes(N, V, G, r.t0, 1995)
    o["O2r_resid"] = o["O2r_m50"] - (2.7410366547641205 + 0.3966308230599589 * lv[r.ci])
    rows.append({"ci": r.ci, **o})
m = pd.DataFrame(rows).merge(o8, on="ci", suffixes=("", "_8"))
out = {}
for c in ["O1c", "O1b", "O3", "O2r_m50", "O2r_m30", "O2r_resid"]:
    a, b = m[c].astype(float), m[c + "_8"].astype(float)
    out[c] = {"max_abs_diff": float(np.nanmax(np.abs(a - b))), "nan_equal": bool((a.isna() == b.isna()).all())}
out["pass"] = all(v["max_abs_diff"] < 1e-9 and v["nan_equal"] for v in out.values())
(RES / "u5_outcomes.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
sys.exit(0 if out["pass"] else 1)
