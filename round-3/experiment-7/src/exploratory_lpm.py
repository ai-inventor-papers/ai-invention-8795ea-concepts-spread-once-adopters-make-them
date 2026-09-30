#!/usr/bin/env python3
"""EXPLORATORY (post-unseal; never changes a verdict): why the econ-geo LPM row gives d0 a different sign than the
conditional logit on the held-out pooled-4 sample. Variants: (i) the frozen LPM; (ii) informative strata only;
(iii) + log-size decile dummies (non-linear size); (iv) (iii) on informative strata; (v) the same on DEV.
Writes results/exploratory_lpm.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
import analysis as AN  # noqa: E402,F401
import models as M  # noqa: E402

spec = json.loads((ROOT / "results" / "frozen_spec.json").read_text())["standardisation_DEV"]
out = {"label": "EXPLORATORY (post-unseal diagnostic; verdicts unchanged)"}
for tag, f, sel in (("heldout_pooled4", "risk_sets_exp5_minus_exp6_heldout.parquet", ["PHYS", "LIFEENV", "SOC", "MATHDEC"]),
                    ("dev", "risk_sets_exp5_minus_exp6_dev.parquet", None)):
    df = pd.read_parquet(ROOT / "results" / f)
    if sel:
        df = df[df.unit.isin(sel)]
    p = M.standardise(df[df.n_ret > 0], spec)
    cols = M.RUNGS["R3_ret"]
    dec = pd.qcut(p.b_log_size, 10, labels=False, duplicates="drop")
    for q in range(1, int(dec.max()) + 1):
        p[f"sz{q}"] = (dec == q).astype(float)
    szc = [c for c in p.columns if c.startswith("sz")]
    inf = M.informative(p)
    r = {}
    for nm, d, cc in (("frozen_lpm", p, cols), ("informative_strata", inf, cols), ("size_deciles", p, cols + szc),
                      ("size_deciles_informative", inf, cols + szc)):
        x = M.lpm(d, cc)["coef"]["d0_ret_rel"]
        r[nm] = {"b": x["b"], "ci": x["ci"], "p": x["p"]}
    r["clogit_R3_d0"] = M.summarise(*(lambda m: (m, m.fit()))(M.model(p, cols)), cols)["coef"]["d0_ret_rel"]
    r["corr_d0_logsize_within_stratum"] = float(np.corrcoef(
        p.d0_ret_rel - p.groupby("stratum").d0_ret_rel.transform("mean"),
        p.b_log_size - p.groupby("stratum").b_log_size.transform("mean"))[0, 1])
    out[tag] = r
    print(tag, json.dumps(r, indent=0))
(ROOT / "results" / "exploratory_lpm.json").write_text(json.dumps(out, indent=1))
