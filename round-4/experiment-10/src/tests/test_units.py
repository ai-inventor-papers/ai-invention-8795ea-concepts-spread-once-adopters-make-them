#!/usr/bin/env python3
"""Unit tests U3, U4, U6, U7 (U1 = tests/test_output.py, U2 = tests/t_ego_flags.py, U5 / U8 logged by s4_gate.py u8
and results/u5_outcomes.json). Writes results/unit_tests.json."""
from __future__ import annotations

import json
import sys
import tempfile
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "lib"))
warnings.simplefilter("ignore", RuntimeWarning)

import numpy as np
import pandas as pd

from common import EXP5, EXP8, RES

out = {}

# ---------------- U3 / U4: home filter and SIZEMATCH identity
import ego
from ego_ctx import rq1_context
import s7_ego

ego.set_context(rq1_context())
jobs = s7_ego.jobs_exp5(subset=None)
rng = np.random.default_rng(0)
picked = [jobs[i] for i in rng.choice(len(jobs), 5, replace=False)]
u3 = []
for ci, name, al, t0, rows, hc in picked:
    r = s7_ego.concept_builds(ci, name, al, t0, rows, hc, builds=("home",))
    works_home = [(y, tp) for y, tp, v in rows if v in hc]
    direct = s7_ego.core6(name, al, t0, works_home)
    same = all((np.isnan(r[f"{k}__home"]) and np.isnan(direct[k])) or r[f"{k}__home"] == direct[k]
               for k in s7_ego.COMPONENTS)
    pre_filtered = all(v in hc for y, tp, v in rows if y < t0 and v in hc)
    u3.append(bool(same and pre_filtered))
# synthetic: off-home papers carry all the new topics -> new_edge_rate(HOME) < new_edge_rate(ALL)
ci, name, al, t0, rows, hc = picked[0]
home_code = next(iter(hc))
rs = np.random.default_rng(1)
base_topics = tuple(int(x) for x in rs.choice(4516, 3, replace=False))
syn = [(t0 - 1, base_topics, home_code)] * 5
for y in (t0, t0 + 1, t0 + 2):
    syn += [(y, base_topics, home_code)] * 6
    syn += [(y, tuple(int(x) for x in rs.choice(4516, 3, replace=False)), (home_code % 26) + 1)] * 3
rsyn = s7_ego.concept_builds(-1, "zzqx synthetic", [], t0, syn, {home_code}, builds=("all", "home"))
u3_syn = bool(rsyn["new_edge_rate__home"] < rsyn["new_edge_rate__all"])
out["U3_home_filter"] = {"concepts_exact": u3, "synthetic_home_lt_all": u3_syn,
                         "values": [rsyn["new_edge_rate__home"], rsyn["new_edge_rate__all"]],
                         "pass": bool(all(u3) and u3_syn)}
ci, name, al, t0, rows, hc = picked[1]
allcodes = set(range(0, 27))
r1 = s7_ego.concept_builds(ci, name, al, t0, rows, allcodes, builds=("all", "sizematch"))
r2 = s7_ego.concept_builds(ci, name, al, t0, rows, hc, builds=("sizematch",))
r3 = s7_ego.concept_builds(ci, name, al, t0, rows, hc, builds=("sizematch",))
ident = all((np.isnan(r1[f"{k}__all"]) and np.isnan(r1[f"{k}__sizematch"])) or
            abs(r1[f"{k}__all"] - r1[f"{k}__sizematch"]) < 1e-12 for k in s7_ego.COMPONENTS)
det = all((np.isnan(r2[f"{k}__sizematch"]) and np.isnan(r3[f"{k}__sizematch"])) or
          r2[f"{k}__sizematch"] == r3[f"{k}__sizematch"] for k in s7_ego.COMPONENTS)
out["U4_sizematch"] = {"full_size_equals_all": bool(ident), "seed_deterministic": bool(det), "pass": bool(ident and det)}

# ---------------- U6: psp equals EXP8 rq1stats on the EXP8 analysis table; planted recovery
from ladder import psp_df
from rq1stats import dummies, psp_point
A = pd.read_parquet(EXP8 / "data/analysis_table.parquet")
A = A[A.split == "DEV"]
diffs = []
for ind in ("CONTACT_REACH", "n_comm_W3", "RETENTION_RATIO_early"):
    d = A[np.isfinite(A[ind]) & np.isfinite(A.O2r_m50) & np.all(np.isfinite(A[["logvol", "growth_c", "offhome_share",
                                                                                "entropy", "reach"]]), 1)]
    ref = psp_point(d[ind].to_numpy(float), d.O2r_m50.to_numpy(float),
                    d[["logvol", "growth_c", "offhome_share", "entropy", "reach"]].to_numpy(float),
                    dummies(d.t0.to_numpy()))
    mine = psp_df(d, ind, "O2r_m50", "R0", 2, 0)["rho"]
    diffs.append(abs(ref - mine))
rs = np.random.default_rng(5)
n = 1000
Bs = rs.normal(size=(n, 3))
x = Bs @ [0.5, 0.2, 0] + rs.normal(size=n)
y = Bs @ [0.3, 0, 0.4] + rs.normal(size=n)
from scipy.stats import rankdata
Z = np.c_[np.ones(n), rankdata(Bs, axis=0)]
rx = rankdata(x) - Z @ np.linalg.lstsq(Z, rankdata(x), rcond=None)[0]
ry = rankdata(y) - Z @ np.linalg.lstsq(Z, rankdata(y), rcond=None)[0]
ry = ry / ry.std() + 0.10 / np.sqrt(0.99) * rx / rx.std()
syn = pd.DataFrame({"x": x, "y": ry, "logvol": Bs[:, 0], "growth_c": Bs[:, 1], "offhome_share": Bs[:, 2],
                    "entropy": 0.0, "reach": 0.0, "t0": 2010})
pl = psp_df(syn, "x", "y", "R0", 300, 1)
out["U6_psp"] = {"max_abs_diff_vs_exp8_rq1stats": float(max(diffs)), "planted_estimate": pl["rho"], "planted_ci": pl["ci"],
                 "planted_ci_gt0": bool(pl["ci"][0] > 0),
                 "criterion": "exact equality with EXP8 rq1stats AND the 95% CI covers the planted 0.10 (n = 1000, "
                              "SE ~ 0.03, so CI > 0 alone has only ~85% power)",
                 "pass": bool(max(diffs) < 1e-10 and pl["ci"][0] <= 0.10 <= pl["ci"][1])}

# ---------------- U7: seal gate refuses before freeze and refuses a second unseal
import seal2
with tempfile.TemporaryDirectory() as td:
    td = Path(td)
    seal2.SPEC, seal2.SEAL, seal2.MARK = td / "frozen_spec.json", td / "seal.log", td / "unsealed.json"
    try:
        seal2.unseal()
        refused_before = False
    except seal2.SealError:
        refused_before = True
    seal2.SPEC.write_text("{}")
    seal2.record("S8_freeze", frozen_spec_sha256=seal2.sha256_file(seal2.SPEC))
    seal2.MARK.write_text("{}")
    try:
        seal2.unseal()
        refused_second = False
    except seal2.SealError:
        refused_second = True
    seal2.MARK.unlink()
    seal2.SPEC.write_text('{"changed": 1}')
    try:
        seal2.unseal()
        refused_changed = False
    except seal2.SealError:
        refused_changed = True
out["U7_seal"] = {"refuses_before_freeze": refused_before, "refuses_second_unseal": refused_second,
                  "refuses_changed_spec": refused_changed,
                  "pass": bool(refused_before and refused_second and refused_changed)}
out["all_pass"] = bool(all(v["pass"] for v in out.values()))
(RES / "unit_tests.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
sys.exit(0 if out["all_pass"] else 1)
