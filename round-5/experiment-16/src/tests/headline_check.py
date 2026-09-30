#!/usr/bin/env python3
"""Headline audit (different code path from the pipeline): reads data/clean_variants.parquet and the EXP10 covariate
tables directly and recomputes (a) the thin-sample share (squared Pearson of raw persistence with its V2 null mean),
(b) binned raw vs null-mean persistence, (c) pooled R2 psp of NOVCHURN_raw, NOVCHURN_exc, NOVCHURN_rare10,
edge_persistence_nullmean with rederive.my_design/my_psp, and (d) the same psp with the outcome SHUFFLED within body
(must be ~0: |psp| < 2/sqrt(n)). -> results/headline_check.json"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "lib"))
import numpy as np, pandas as pd
from common import DATA, DATA_IN, RES, jdump
from rederive import my_design, my_psp
cv = pd.read_parquet(DATA / "clean_variants.parquet")
y, x = cv.edge_persistence__raw.to_numpy(float), cv.edge_persistence_nullmean.to_numpy(float)
ok = np.isfinite(x) & np.isfinite(y)
out = {"thin_sample_share_R2": float(np.corrcoef(x[ok], y[ok])[0, 1] ** 2), "n": int(ok.sum())}
n = cv.n_home_early.to_numpy()
out["binned"] = {f"{lo}-{hi}": [float(np.nanmean(y[(n >= lo) & (n <= hi)])), float(np.nanmean(x[(n >= lo) & (n <= hi)]))]
                 for lo, hi in ((10, 19), (20, 49), (50, 99), (100, 10**9))}
keep = ["ci", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "t0", "type", "generic", "level", "O2r_m50"]
fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=keep)
ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=keep + ["window_flag"])
e = cv[cv.frame == "exp5"].drop(columns=["t0"]).merge(fe, on="ci"); e["window_flag"] = 0
c = cv[cv.frame == "cohort"].drop(columns=["t0"]).merge(ac, on="ci")
P = pd.concat([e, c], ignore_index=True)
cont, C = my_design(P, True)
rng = np.random.default_rng(123)
ysh = P.O2r_m50.to_numpy(float).copy()
for b in P.body.unique():
    m = np.nonzero((P.body == b).to_numpy())[0]
    ysh[m] = rng.permutation(ysh[m])
V = json.loads((RES / "clean_vs_raw_psp.json").read_text())["cells"]["psp"]
out["psp_R2_pooled"] = {}
for v in ("NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_rare10", "edge_persistence_nullmean", "OPEN_home_clean"):
    r, nn = my_psp(P[v].to_numpy(float), P.O2r_m50.to_numpy(float), cont, C)
    rs, _ = my_psp(P[v].to_numpy(float), ysh, cont, C)
    out["psp_R2_pooled"][v] = {"rederived": r, "pipeline": V[f"POOLED|{v}|O2r_m50|R2"]["rho"], "n": nn,
                               "shuffled_outcome": rs, "shuffled_fails": bool(abs(rs) < 2 / np.sqrt(nn))}
jdump(out, RES / "headline_check.json")
print(json.dumps(out, indent=1))
