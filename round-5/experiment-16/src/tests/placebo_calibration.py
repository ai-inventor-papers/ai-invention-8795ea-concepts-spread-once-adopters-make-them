#!/usr/bin/env python3
"""Post-seal diagnostic (exploratory): calibration of the psp CIs under the exact null. 500 permutations of the
planted-x (PC3 construction) per body at R2; share of |psp| > 1.96 x (the placebos' mean bootstrap SE from PC3) and
the ratio sd(permutation psp) / bootstrap SE. -> results/placebo_calibration.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import numpy as np
from scipy import stats
from common import RES, jdump
from fastpsp import complete, psp_fast
from tables import design, load_tables
T = load_tables()
V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
out = {"label": "exploratory, post-seal diagnostic"}
for body in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED"):
    df = T[body]
    Bm, Cm = design(df, "R2", body == "POOLED")
    y = df.O2r_m50.to_numpy(float)
    rr = df.O2r_resid.to_numpy(float)
    rng = np.random.default_rng(99)
    ok = np.isfinite(rr)
    rk = np.full(len(rr), np.nan); rk[ok] = stats.rankdata(rr[ok])
    x = rk + rng.normal(0, 3 * np.nanstd(rk), len(rk))
    m = complete(x, y, Bm, Cm)
    se = float(np.mean([p["se"] for p in V["cells"]["planted_PC3"][body]["placebos"]]))
    rh = []
    for _ in range(500):
        xs = x.copy(); xs[ok] = rng.permutation(x[ok])
        mm = complete(xs, y, Bm, Cm)
        rh.append(psp_fast(xs[mm], y[mm], Bm[mm], Cm[mm]))
    rh = np.asarray(rh)
    out[body] = {"n": int(m.sum()), "boot_se": se, "perm_sd": float(rh.std()), "ratio_sd_se": float(rh.std() / se),
                 "share_abs_gt_1.96se": float(np.mean(np.abs(rh) > 1.96 * se))}
    print(body, out[body], flush=True)
jdump(out, RES / "placebo_calibration.json")
