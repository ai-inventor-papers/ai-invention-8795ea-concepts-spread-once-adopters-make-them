#!/usr/bin/env python3
"""Short INDEPENDENT re-derivation of the headline numbers (TODO 5), separate from the pipeline code path.

Reads the raw per-concept tables only (data/features_cohort.parquet components, data/outcomes_cohort.parquet,
results/frozen_spec.json constants, data/cohort_predictions.parquet) -- NOT results/cohort_result.json fields -- and
(1) rebuilds OPEN_home / OPEN_all from the six raw components with the frozen constants (pandas, own loop);
(2) recomputes the partial Spearman at R2 with its own design matrix (pandas ranks + numpy QR residuals, no
    lib/ladder.rung_design, no rq1stats); a 400-draw bootstrap CI;
(3) the B5 vs B5+OPEN_home prediction Spearman gain (scipy on the stored frozen predictions);
(4) the same R2 statistic on shuffled outcomes (200 permutations) and on a random OPEN, which must NOT look significant.
Writes results/rederive.json."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
spec = json.loads((ROOT / "results/frozen_spec.json").read_text())
F = pd.read_parquet(ROOT / "data/features_cohort.parquet")
O = pd.read_parquet(ROOT / "data/outcomes_cohort.parquet")[["ci", "O2r_m50"]]
D = F.merge(O, on="ci")
SIGN = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
        "edge_persistence": -1}


def open_score(build):
    c = spec["open_constants"][build]
    zs = []
    for k, s in SIGN.items():
        v = D[f"{k}__{build}"].clip(c[k]["lo"], c[k]["hi"])
        zs.append(s * (v - c[k]["mu"]) / c[k]["sd"])
    Z = pd.concat(zs, axis=1)
    o = Z.mean(axis=1, skipna=True).where(Z.notna().sum(axis=1) >= 4)
    if build != "all":
        o = o.where(D.n_home_early >= 10)
    return o


def design(d):
    cont = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH"]
    X = [np.ones(len(d))] + [d[c].rank().to_numpy() for c in cont]
    for y in (2016, 2017):
        X.append((d.t0 == y).to_numpy(float))
    for t in ("method", "object", "property"):
        X.append((d["type"] == t).to_numpy(float))
    X.append(d["generic"].to_numpy(float))
    for lv in (3, 4, 5):
        X.append((d.level == lv).to_numpy(float))
    return np.column_stack(X)


def psp(x, y, X):
    keep = np.abs(np.linalg.qr(X)[1].diagonal()) > 1e-9      # drop collinear / empty dummy columns
    Q, _ = np.linalg.qr(X[:, keep])
    rx = pd.Series(x).rank().to_numpy(); ry = pd.Series(y).rank().to_numpy()
    rx = rx - Q @ (Q.T @ rx); ry = ry - Q @ (Q.T @ ry)
    return float(np.corrcoef(rx, ry)[0, 1])


out = {}
for b in ("home", "all"):
    o = open_score(b)
    out[f"OPEN_{b}_max_abs_diff_vs_frozen_table"] = float(np.nanmax(np.abs(o - F[f"OPEN_{b}"])))
    d = D.assign(o=o).dropna(subset=["o", "O2r_m50", "logvol", "growth_c", "offhome_share", "entropy", "reach"])
    d = d.reset_index(drop=True)
    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))
    rng = np.random.default_rng(1)
    bs = []
    for _ in range(400):
        i = rng.integers(0, len(d), len(d))
        di = d.iloc[i].reset_index(drop=True)
        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))
    out[f"OPEN_{b}_psp_R2"] = {"n": len(d), "est": est, "ci95_400boot": [float(np.percentile(bs, 2.5)),
                                                                          float(np.percentile(bs, 97.5))]}
    if b == "home":
        # placebo 1: within-group shuffled outcome; placebo 2: random OPEN
        perm = []
        for _ in range(200):
            y = d.O2r_m50.to_numpy().copy()
            for g in d.agroup.unique():
                m = (d.agroup == g).to_numpy()
                y[m] = rng.permutation(y[m])
            perm.append(psp(d.o.to_numpy(), y, design(d)))
        perm = np.abs(perm)
        out["placebo_shuffled_outcome"] = {"q95_abs": float(np.percentile(perm, 95)),
                                           "share_ge_observed": float((perm >= abs(est)).mean())}
        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))
        out["placebo_random_open_psp"] = rnd
P = pd.read_parquet(ROOT / "data/cohort_predictions.parquet").merge(O, on="ci").dropna()
s0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]
out["prediction_spearman"] = {"n": len(P), "B5": float(s0), "B5_plus_OPEN_home": float(s1), "diff": float(s1 - s0)}
(ROOT / "results/rederive.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
