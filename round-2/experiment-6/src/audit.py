#!/usr/bin/env python3
"""T7 independent audit: recompute the held-out H2 LR (statsmodels ConditionalLogit, exact conditional likelihood),
the R1 retained x top-gateway interaction (statsmodels OLS with concept dummies, cluster SE) and p_gw (pandas) from the
saved tables, and compare with results/heldout_result.json. Writes results/audit.json."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.discrete.conditional_models import ConditionalLogit

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
held = json.loads((RES / "heldout_result.json").read_text())
spec = json.loads((RES / "frozen_spec.json").read_text())
out = {}
# 1. H2 LR
df = pd.read_parquet(RES / "entry_risk_sets_heldout.parquet")
df = df[df.n_ret > 0].copy()
for c, s in spec["standardisation"].items():
    df[c] = (df[c] - s["mean"]) / s["sd"]
g = df.groupby("stratum").entered.agg(["sum", "size"])
keep = g[(g["sum"] > 0) & (g["sum"] < g["size"])].index
d = df[df.stratum.isin(keep)]
m0c = ["a_phi_home", "b_log_size", "c_density", "e_gate_own"]
f0 = ConditionalLogit(d.entered.to_numpy(), d[m0c].to_numpy(), groups=d.stratum.to_numpy()).fit(disp=0)
f2 = ConditionalLogit(d.entered.to_numpy(), d[m0c + ["d_ret_gate"]].to_numpy(), groups=d.stratum.to_numpy()).fit(disp=0)
lr_sm = 2 * (f2.llf - f0.llf)
lr_own = held["H2_pooled"]["LR"]["M2_vs_M0"]["LR"]
multi = float((g.loc[keep, "sum"] > 1).mean())
out["H2_LR"] = {"statsmodels_exact": float(lr_sm), "own_breslow": lr_own, "rel_diff": float(abs(lr_sm - lr_own) / lr_own),
                "d_statsmodels": float(f2.params[-1]), "d_own": held["H2_pooled"]["models"]["M2"]["coef"]["d_ret_gate"],
                "share_strata_multi_event": multi,
                "note": "own estimator uses the Breslow form for strata with >1 event; statsmodels uses the exact conditional likelihood"}
# 2. R1 interaction (held-out rescue table)
R = pd.read_csv(RES / "rescue_heldout.csv")
R = R[R.resc.notna()].copy()
lo, hi = spec["gate_terciles"]
R["top"] = (R.gateway_j >= hi).astype(float); R["mid"] = ((R.gateway_j >= lo) & (R.gateway_j < hi)).astype(float)
R["ret_x_top"] = R.R_cj * R.top; R["ret_x_mid"] = R.R_cj * R.mid; R["log_n_early_j"] = np.log(R.n_early_j)
X = pd.concat([R[["R_cj", "top", "mid", "ret_x_top", "ret_x_mid", "log_n_early_j", "log_size_j"]],
               pd.get_dummies(R.cidx, prefix="c", drop_first=True, dtype=float)], axis=1)
ols = sm.OLS(R.resc.to_numpy(), sm.add_constant(X).to_numpy()).fit(cov_type="cluster", cov_kwds={"groups": R.cidx.to_numpy()})
b_sm = float(ols.params[4])
b_own = held["rescue_relay"]["R1_resc"]["coef"]["ret_x_top"]["b"]
out["R1_interaction"] = {"statsmodels": b_sm, "own": b_own, "abs_diff": abs(b_sm - b_own), "agree_1e-3": abs(b_sm - b_own) < 1e-3}
# 3. p_gw
O = pd.read_csv(RES / "ordering_heldout.csv")
T = O[O.top_o2r & O.tau.notna() & O.gamma.notna()]
before, after = int((T.gamma < T.tau).sum()), int((T.gamma > T.tau).sum())
p = before / (before + after)
out["p_gw"] = {"pandas": p, "own": held["ordering"]["gateway"]["share_before_excl_ties"],
               "agree_1e-3": abs(p - held["ordering"]["gateway"]["share_before_excl_ties"]) < 1e-3}
(RES / "audit.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
