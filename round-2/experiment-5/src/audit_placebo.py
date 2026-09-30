#!/usr/bin/env python3
"""Headline re-derivation (different code path) + shuffled-input controls -> results/audit_placebo.json.

  1. H3 per-group partial rho of G (held-out) via statsmodels-free numpy code and pandas ranks, and our own
     DerSimonian-Laird on concept-bootstrap SEs -> compare with results/h3_results.json (pooled 0.068).
  2. The pre-registered H3 test (within-group permutation, one-sided) run on SHUFFLED outcomes must fail.
  3. Held-out dAUC with SHUFFLED R (dev fit with sklearn, independent of models.py) must be ~0, and the gateway
     increment computed on a planted-signal copy must be detected (sanity of the metric)."""
import json

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from common import RES, ROOT, jdump

rng = np.random.default_rng(7)
spec = json.loads((ROOT / "frozen_spec.json").read_text())
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]


def prho(df, x, y):
    d = df[[x, y] + B5].dropna()
    R = d.rank()
    Zm = np.column_stack([np.ones(len(d)), R[B5].to_numpy()])
    rx = R[x].to_numpy() - Zm @ np.linalg.lstsq(Zm, R[x].to_numpy(), rcond=None)[0]
    ry = R[y].to_numpy() - Zm @ np.linalg.lstsq(Zm, R[y].to_numpy(), rcond=None)[0]
    return float(np.dot(rx, ry) / np.sqrt(np.dot(rx, rx) * np.dot(ry, ry)))


fc = pd.read_csv(ROOT / "frame_concepts.csv")
co = pd.read_csv(ROOT / "concept_outcomes.csv")
cf = pd.read_csv(ROOT / "concept_features_basic.csv")
h = fc[fc.split.str.startswith("HELDOUT")][["ci", "group"]].merge(co[["ci", "O2r_m30", "N_outcome"]], on="ci") \
    .merge(cf[["ci", "G"] + B5], on="ci")
a, b = spec["O2r_resid"]["a"], spec["O2r_resid"]["b"]
h["res"] = h.O2r_m30 - (a + b * np.log(h.N_outcome.clip(lower=1)))
h = h.dropna(subset=["res", "G"])
est, var = [], []
per = {}
for g, d in h.groupby("group"):
    r = prho(d, "G", "res")
    bs = [prho(d.sample(len(d), replace=True, random_state=int(rng.integers(1e9))), "G", "res") for _ in range(300)]
    per[g] = r
    est.append(r); var.append(np.var(bs))
est, var = np.array(est), np.array(var)
w = 1 / var
mu_f = (w * est).sum() / w.sum()
Q = (w * (est - mu_f) ** 2).sum()
tau2 = max(0, (Q - (len(est) - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
ws = 1 / (var + tau2)
dl = float((ws * est).sum() / ws.sum())
rep = json.loads((RES / "h3_results.json").read_text())
out = {"H3_G_per_group": {"audit": per, "reported": {k: v["rho"] for k, v in rep["G"]["per_group"].items()}},
       "H3_G_DL_pooled": {"audit": dl, "reported": rep["G"]["dl_pool"]["pooled"],
                          "note": "SEs from an independent 300-draw bootstrap, so agreement is approximate"}}


def within_perm_p(d, ycol, n=1000):
    obs = prho(d, "G", ycol)
    cnt = 0
    for _ in range(n):
        dd = d.copy()
        dd["G"] = dd.groupby("group").G.transform(lambda s: s.sample(frac=1, random_state=int(rng.integers(1e9))).to_numpy())
        cnt += prho(dd, "G", ycol) >= obs
    return obs, (1 + cnt) / (1 + n)


real = within_perm_p(h, "res", 500)
hs = h.copy()
hs["res_shuf"] = hs.groupby("group").res.transform(lambda s: s.sample(frac=1, random_state=3).to_numpy())
shuf = within_perm_p(hs, "res_shuf", 500)
out["H3_test_real_vs_shuffled_outcome"] = {"real_rho_p": real, "shuffled_rho_p": shuf,
                                           "shuffled_fails_at_0.05": bool(shuf[1] > 0.05)}
# held-out dAUC with shuffled R (independent sklearn code); planted signal control
F = pd.read_csv(ROOT / "heldout_episodes_with_pred.csv")
D = pd.read_csv(ROOT / "dev_episodes_with_oof.csv")
sc = spec["standardisation"]
Xz = lambda d, cols: np.nan_to_num(np.column_stack([(d[c] - sc[c][0]) / sc[c][1] for c in cols]))  # noqa: E731


def dauc(dev, ho, ycol):
    m0 = LogisticRegression(C=1, max_iter=5000).fit(Xz(dev, spec["X0"]), dev[ycol])
    m1 = LogisticRegression(C=1, max_iter=5000).fit(Xz(dev, spec["X1"]), dev[ycol])
    return float(roc_auc_score(ho[ycol], m1.predict_proba(Xz(ho, spec["X1"]))[:, 1])
                 - roc_auc_score(ho[ycol], m0.predict_proba(Xz(ho, spec["X0"]))[:, 1]))


out["heldout_dauc_real"] = dauc(D, F, "R")
shuf_d = []
for k in range(20):
    D2, F2 = D.copy(), F.copy()
    D2["Rs"] = rng.permutation(D2.R.to_numpy()); F2["Rs"] = rng.permutation(F2.R.to_numpy())
    shuf_d.append(dauc(D2, F2, "Rs"))
out["heldout_dauc_shuffled_R"] = {"mean": float(np.mean(shuf_d)), "sd": float(np.std(shuf_d))}
D3, F3 = D.copy(), F.copy()
for d in (D3, F3):
    z = (d.gateway_j - sc["gateway_j"][0]) / sc["gateway_j"][1]
    lp = np.log(d.pred_X0 / (1 - d.pred_X0)) if "pred_X0" in d else np.log(d.oof_X0 / (1 - d.oof_X0))
    d["Rp"] = (rng.random(len(d)) < 1 / (1 + np.exp(-(lp + 1.0 * z)))).astype(int)
out["heldout_dauc_planted_gateway_effect_1SD"] = dauc(D3, F3, "Rp")
jdump(out, RES / "audit_placebo.json")
print(json.dumps(out, indent=1, default=str))


# 4. calibrated alternative: size-weighted mean of WITHIN-group partial rhos, null by within-group permutation of G.
def within_stat(d, ycol):
    tot, n = 0.0, 0
    for g, dg in d.groupby("group"):
        k = dg[["G", ycol]].dropna().shape[0]
        tot += k * prho(dg, "G", ycol); n += k
    return tot / n


def within_test(d, ycol, n=300):
    obs = within_stat(d, ycol)
    cnt = 0
    for _ in range(n):
        dd = d.copy()
        dd["G"] = dd.groupby("group").G.transform(lambda s: s.sample(frac=1, random_state=int(rng.integers(1e9))).to_numpy())
        cnt += within_stat(dd, ycol) >= obs
    return obs, (1 + cnt) / (1 + n)


out["H3_calibrated_within_group_stat"] = {"real": within_test(h, "res"),
                                          "shuffled_outcome": within_test(hs, "res_shuf"),
                                          "note": "size-weighted mean of within-group partial rho; one-sided within-group permutation p"}
out["H3_preregistered_test_valid"] = bool(out["H3_test_real_vs_shuffled_outcome"]["shuffled_fails_at_0.05"])
jdump(out, RES / "audit_placebo.json")
print(out["H3_calibrated_within_group_stat"])


# 5. calibration: false-positive rate of both tests over 40 independent outcome shuffles (alpha = 0.05)
fp_pre, fp_cal = [], []
for k in range(40):
    hk = h.copy()
    hk["ys"] = hk.groupby("group").res.transform(lambda s: s.sample(frac=1, random_state=1000 + k).to_numpy())
    fp_pre.append(within_perm_p(hk, "ys", 200)[1] < 0.05)
    fp_cal.append(within_test(hk, "ys", 200)[1] < 0.05)
out["H3_calibration_40_shuffles"] = {"false_positive_rate_preregistered_pooled_test": float(np.mean(fp_pre)),
                                     "false_positive_rate_within_group_stat": float(np.mean(fp_cal)),
                                     "nominal_alpha": 0.05}
out["H3_preregistered_test_valid"] = bool(np.mean(fp_pre) <= 0.10)
jdump(out, RES / "audit_placebo.json")
print(out["H3_calibration_40_shuffles"])
