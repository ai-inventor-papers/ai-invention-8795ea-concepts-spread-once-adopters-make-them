#!/usr/bin/env python3
"""U7b: psp_fast == rq1stats.psp_point on bootstrap resamples of the EXP5 and cohort tables at R0/R2/R3/R5
(max |diff| <= 1e-9) + timing -> results/unit_tests_fastpsp.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import numpy as np, pandas as pd
from common import DATA_IN, RES, jdump
from fastpsp import psp_fast
from ladder import rung_design
from rq1stats import psp_point
out = {}
worst = 0.0
for nm, f, x in (("exp5", "features_exp5_open.parquet", "OPEN_home"), ("cohort", "analysis_cohort.parquet", "OPEN_home")):
    d = pd.read_parquet(DATA_IN / f)
    for r in ("R0", "R2", "R3", "R5"):
        Bc, Cc = rung_design(d, r)
        xv, yv = d[x].to_numpy(float), d.O2r_m50.to_numpy(float)
        B, C = Bc.to_numpy(float), Cc.to_numpy(float)
        ok = np.isfinite(xv) & np.isfinite(yv) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
        xv, yv, B, C = xv[ok], yv[ok], B[ok], C[ok]
        rng = np.random.default_rng(0)
        t1 = t2 = 0.0
        for _ in range(20):
            i = rng.integers(0, len(xv), len(xv)); Ci = C[i]; keep = Ci.std(0) > 0
            t = time.time(); a = psp_point(xv[i], yv[i], B[i], Ci[:, keep]); t1 += time.time() - t
            t = time.time(); b = psp_fast(xv[i], yv[i], B[i], Ci[:, keep]); t2 += time.time() - t
            worst = max(worst, abs(a - b))
        out[f"{nm}_{r}"] = {"n": int(len(xv)), "orig_ms": t1 / 20 * 1e3, "fast_ms": t2 / 20 * 1e3}
        print(nm, r, out[f"{nm}_{r}"], worst, flush=True)
out["max_abs_diff"] = worst
out["pass"] = bool(worst <= 1e-9)
jdump(out, RES / "unit_tests_fastpsp.json")
print("pass", out["pass"], worst)
