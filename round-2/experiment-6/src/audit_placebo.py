#!/usr/bin/env python3
"""Second independent re-derivation (different code path: statsmodels exact ConditionalLogit, sklearn AUC, inline DL)
from the raw held-out risk-set table, plus placebo runs that must FAIL: labels shuffled within strata, and the ordering
share with the gateway-retention year replaced by a random year. Writes results/audit_placebo.json."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import roc_auc_score
from statsmodels.discrete.conditional_models import ConditionalLogit

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
rng = np.random.default_rng(20261001)
spec = json.loads((RES / "frozen_spec.json").read_text())
dev = json.loads((RES / "dev_result.json").read_text())
held = json.loads((RES / "heldout_result.json").read_text())
M0 = ["a_phi_home", "b_log_size", "c_density", "e_gate_own"]
df = pd.read_parquet(RES / "entry_risk_sets_heldout.parquet")
df = df[df.n_ret > 0].copy()
for c, s in spec["standardisation"].items():
    df[c] = (df[c] - s["mean"]) / s["sd"]


def informative(d):
    g = d.groupby("stratum").entered.agg(["sum", "size"])
    return d[d.stratum.isin(g[(g["sum"] > 0) & (g["sum"] < g["size"])].index)]


def lr(d, y):
    f0 = ConditionalLogit(y, d[M0].to_numpy(), groups=d.stratum.to_numpy()).fit(disp=0)
    f2 = ConditionalLogit(y, d[M0 + ["d_ret_gate"]].to_numpy(), groups=d.stratum.to_numpy()).fit(disp=0)
    return 2 * (f2.llf - f0.llf), f2.params[-1], f2.bse[-1]


out = {}
d = informative(df)
L, b, se = lr(d, d.entered.to_numpy())
out["real"] = {"LR_exact": float(L), "p": float(stats.chi2.sf(L, 1)), "d": float(b)}
# placebo 1: shuffle the entered label within each stratum (keeps the number of events per stratum)
ps = []
for _ in range(20):
    y = d.groupby("stratum").entered.transform(lambda s: rng.permutation(s.to_numpy())).to_numpy()
    ps.append(stats.chi2.sf(lr(d, y)[0], 1))
out["placebo_shuffled_labels"] = {"n": 20, "reject_rate_p<0.01": float(np.mean(np.array(ps) < 0.01)),
                                  "median_p": float(np.median(ps))}
# per-group d and DerSimonian-Laird, written inline
grp = {}
for gname in ("Physical", "LifeEnv", "Social", "Cohort"):
    g = informative(df[df.hgroup == gname])
    _, bg, sg = lr(g, g.entered.to_numpy())
    grp[gname] = (float(bg), float(sg))
bb = np.array([v[0] for v in grp.values()]); ss = np.array([v[1] for v in grp.values()])
w = 1 / ss**2; bf = (w * bb).sum() / w.sum(); Q = (w * (bb - bf) ** 2).sum(); k = len(bb)
tau2 = max(0, (Q - (k - 1)) / (w.sum() - (w**2).sum() / w.sum())); ws = 1 / (ss**2 + tau2)
dl = (ws * bb).sum() / ws.sum(); dlse = (1 / ws.sum()) ** 0.5
out["per_group_exact"] = grp
out["DL_exact"] = {"b": float(dl), "ci": [float(dl - 1.96 * dlse), float(dl + 1.96 * dlse)],
                   "I2": float(max(0, (Q - (k - 1)) / Q)) if Q > 0 else 0.0,
                   "pipeline_DL_breslow": held["H2_DL_pooled"]["b"], "positive_groups": int((bb > 0).sum())}
# within-stratum AUC of the frozen dev linear predictors, sklearn per stratum
aucs = {}
for m, cols in (("M0", M0), ("M2", M0 + ["d_ret_gate"])):
    beta = np.array([dev["H2"]["models"][m]["coef"][c] for c in cols])
    s = d[cols].to_numpy() @ beta
    vals = [roc_auc_score(g.entered, s[g.index.map(d.index.get_loc)]) for _, g in d.groupby("stratum")]
    aucs[m] = float(np.mean(vals))
out["frozen_coef_auc_sklearn"] = aucs
out["frozen_coef_auc_pipeline"] = {k: v["mean"] for k, v in held["frozen_dev_coef_auc"].items()}
# ordering: real share vs a placebo where the gateway year is a random year in t0..t0+8
O = pd.read_csv(RES / "ordering_heldout.csv")
fc = pd.read_csv(RES / "frame_concepts.csv").set_index("cidx")
T = O[O.top_o2r & O.tau.notna() & O.gamma.notna()]
real = (T.gamma < T.tau).sum() / ((T.gamma < T.tau).sum() + (T.gamma > T.tau).sum())
sh = []
for _ in range(200):
    t0 = T.cidx.map(fc.t0).to_numpy()
    gam = t0 + rng.integers(0, 9, len(T))
    bef, aft = (gam < T.tau).sum(), (gam > T.tau).sum()
    sh.append(bef / (bef + aft))
out["ordering"] = {"p_gw_real": float(real), "placebo_random_year_mean": float(np.mean(sh)),
                   "placebo_share_ge_real": float(np.mean(np.array(sh) >= real))}
(RES / "audit_placebo.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
