#!/usr/bin/env python3
"""STEPS 8-9 (analysis): H1 episode-level gateway-retention models and H3 concept-level partial Spearman.

  python models.py dev       dev-only analysis, then FREEZE (frozen_spec.json, sha256 -> logs/seal.log, git commit)
  python models.py heldout   score the frozen models ONCE on the unsealed held-out groups and the 2010-14 cohort

Primary: L2 logistic (C=1, lbfgs) of R on X0 vs X1 = X0 + gateway_j. Dev: leave-one-home-group-out OOF dAUC with a
2,000-draw concept-clustered REFIT bootstrap. Held-out: fit on all dev, predict held-out, bootstrap resampling dev
concepts (refit) and held-out concepts (evaluate). Secondary: conditional logit (concept FE), LPM with field FE and
time-varying gateway_j,s (concept- and two-way clustered SEs), boundary interaction, relatedness head-to-head,
200 rewired-backbone placebos (+ permutation placebo), leave-one-adopting-field-out, crossed concept x field
bootstrap, power simulation."""
from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
import time
import warnings

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
from scipy import stats
from sklearn.metrics import roc_auc_score

from common import DEV_GROUPS, HELD_GROUPS, LOGS, RES, ROOT, SEED, jdump, setup_logger

warnings.filterwarnings("ignore")
logger = setup_logger("models")
N_JOBS = 4
X0 = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "log_field_size", "phi_home", "density", "P_j",
      "label_coverage_early", "precision_c", "tag_coverage", "log_n_early", "share_early", "growth_j"]
GATE = "gateway_j"
X1 = X0 + [GATE]
FE_VARY = ["log_field_size", "phi_home", "density", "P_j", "log_n_early", "share_early", "growth_j"]
C_REG = 1.0
PJ_M = 5.0      # shrinkage pseudo-count of the leave-concept-out propensity towards the split-set mean
PJ_WIN = 2      # |t0' - t0| <= 2
import os
SMOKE = os.environ.get("SMOKE") == "1"   # smoke test: small B, no freeze, separate output file
B_MAIN = 60 if SMOKE else 2000
B_SMALL = 20 if SMOKE else 500
SPEC = ROOT / "frozen_spec.json"


# ----------------------------------------------------------------------------- helpers
def split_set(s: str) -> str:
    return "HELDOUT" if s.startswith("HELDOUT") else s


def add_pj(df: pd.DataFrame, rcol: str = "R", out: str = "P_j") -> pd.DataFrame:
    """Leave-concept-out retention propensity of field j among OTHER concepts' episodes in the same split set
    with |t0' - t0| <= 2, shrunk towards the split-set mean with pseudo-count PJ_M."""
    df = df.copy()
    df["_ss"] = df.split.map(split_set)
    vals = np.full(len(df), np.nan)
    for (ss, f), g in df.groupby(["_ss", "field"]):
        mu = df.loc[(df._ss == ss) & df[rcol].notna(), rcol].mean()
        gv = g[g[rcol].notna()]
        t0 = gv.t0.to_numpy()
        r = gv[rcol].to_numpy(float)
        ci = gv.ci.to_numpy()
        for idx, row in zip(g.index, g.itertuples()):
            m = (np.abs(t0 - row.t0) <= PJ_WIN) & (ci != row.ci)
            vals[df.index.get_loc(idx)] = (r[m].sum() + PJ_M * mu) / (m.sum() + PJ_M)
    df[out] = vals
    return df.drop(columns="_ss")


def add_pj_train(df: pd.DataFrame, rcol: str = "R", out: str = "P_j_trainset") -> pd.DataFrame:
    """Variant P_j_train: dev-only retention propensity of field j (any t0, other concepts), shrunk to the dev mean."""
    df = df.copy()
    dv = df[(df.split == "DEV") & df[rcol].notna()]
    mu = dv[rcol].mean()
    s = dv.groupby("field")[rcol].sum()
    n = dv.groupby("field")[rcol].size()
    own = dv.groupby(["ci", "field"])[rcol].agg(["sum", "size"])
    vals = []
    for r in df.itertuples():
        a, b = float(s.get(r.field, 0.0)), float(n.get(r.field, 0))
        if r.split == "DEV" and (r.ci, r.field) in own.index:
            a -= float(own.at[(r.ci, r.field), "sum"])
            b -= float(own.at[(r.ci, r.field), "size"])
        vals.append((a + PJ_M * mu) / (b + PJ_M))
    df[out] = vals
    return df


def std_consts(df: pd.DataFrame, cols: list[str]) -> dict:
    return {c: [float(df[c].mean()), float(df[c].std() or 1.0)] for c in cols}


def Z(df: pd.DataFrame, cols: list[str], sc: dict) -> np.ndarray:
    X = np.column_stack([(df[c].to_numpy(float) - sc[c][0]) / (sc[c][1] if sc[c][1] > 0 else 1.0) for c in cols])
    return np.nan_to_num(X, nan=0.0)  # NaN -> dev mean (0 after standardisation)


class L2Logit:
    """Exact Newton-IRLS for sklearn's L2 objective 0.5*||w||^2 + C * sum_i s_i * logloss_i (intercept unpenalised).
    Fast for the ~16 standardised covariates used here; converges to the same optimum as lbfgs."""

    def __init__(self, C: float = C_REG):
        self.C = C

    def fit(self, X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> "L2Logit":
        Xa = np.column_stack([np.ones(len(X)), X])
        s = np.ones(len(X)) if w is None else np.asarray(w, float)
        y = np.asarray(y, float)
        P = np.eye(Xa.shape[1])
        P[0, 0] = 0.0
        b = np.zeros(Xa.shape[1])
        for _ in range(100):
            eta = np.clip(Xa @ b, -35, 35)
            p = 1 / (1 + np.exp(-eta))
            g = self.C * Xa.T @ (s * (p - y)) + P @ b
            H = self.C * (Xa * (s * p * (1 - p))[:, None]).T @ Xa + P
            step = np.linalg.solve(H, g)
            b -= step
            if np.abs(step).max() < 1e-10:
                break
        self.coef_, self.intercept_ = b[1:][None, :], np.array([b[0]])
        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        return X @ self.coef_[0] + self.intercept_[0]

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        p = 1 / (1 + np.exp(-np.clip(self.decision_function(X), -35, 35)))
        return np.column_stack([1 - p, p])


def fit(X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> L2Logit:
    return L2Logit(C_REG).fit(X, y, w)


def auc(y, p, w=None) -> float:
    y = np.asarray(y)
    if len(np.unique(y)) < 2:
        return math.nan
    return float(roc_auc_score(y, p, sample_weight=w))


def logo_oof(df: pd.DataFrame, cols: list[str], sc: dict, y: np.ndarray, groups: np.ndarray,
             w: np.ndarray | None = None) -> np.ndarray:
    X = Z(df, cols, sc)
    oof = np.full(len(df), np.nan)
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if len(np.unique(y[tr])) < 2:
            continue
        m = fit(X[tr], y[tr], None if w is None else w[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]
    return oof


def dl_pool(est: list[float], se: list[float]) -> dict:
    y = np.array(est, float)
    v = np.array(se, float) ** 2
    ok = np.isfinite(y) & np.isfinite(v) & (v > 0)
    y, v = y[ok], v[ok]
    k = len(y)
    if k == 0:
        return {"k": 0}
    w = 1 / v
    ybar = (w * y).sum() / w.sum()
    Q = float((w * (y - ybar) ** 2).sum())
    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0
    ws = 1 / (v + tau2)
    mu = float((ws * y).sum() / ws.sum())
    se_mu = float(math.sqrt(1 / ws.sum()))
    I2 = float(max(0.0, (Q - (k - 1)) / Q)) if Q > 0 and k > 1 else 0.0
    return {"k": k, "pooled": mu, "se": se_mu, "ci95": [mu - 1.96 * se_mu, mu + 1.96 * se_mu], "tau2": tau2,
            "I2": I2, "Q": Q}


def sign_test(vals: list[float]) -> dict:
    v = [x for x in vals if np.isfinite(x)]
    k = sum(1 for x in v if x > 0)
    return {"n": len(v), "n_positive": k, "p_one_sided": float(stats.binomtest(k, len(v), 0.5,
                                                                                alternative="greater").pvalue) if v else math.nan}


def concept_index(df: pd.DataFrame) -> dict:
    return {c: np.nonzero(df.ci.to_numpy() == c)[0] for c in np.unique(df.ci)}


# ----------------------------------------------------------------------------- dev: LOGO + refit bootstrap
def _boot_logo(seed: int, df: pd.DataFrame, specs: dict, sc: dict, y: np.ndarray, grp: np.ndarray,
               cidx: dict, cgrp: dict) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    for g in DEV_GROUPS:
        cs = cgrp[g]
        pick = rng.choice(cs, size=len(cs), replace=True)
        rows.append(np.concatenate([cidx[c] for c in pick]))
    idx = np.concatenate(rows)
    d = df.iloc[idx]
    yy, gg = y[idx], grp[idx]
    out = {}
    for name, cols in specs.items():
        out[name] = logo_oof(d, cols, sc, yy, gg)
    res = {name: auc(yy, p) for name, p in out.items()}
    res["per_group"] = {g: {name: auc(yy[gg == g], out[name][gg == g]) for name in specs} for g in DEV_GROUPS}
    return res


def boot_logo(df, specs, sc, y, grp, B, seed0):
    cidx = concept_index(df)
    cg = df.groupby("ci").group.first()
    cgrp = {g: cg.index[cg == g].to_numpy() for g in DEV_GROUPS}
    return Parallel(n_jobs=N_JOBS, batch_size=8)(delayed(_boot_logo)(seed0 + b, df, specs, sc, y, grp, cidx, cgrp)
                                                 for b in range(B))


def ci95(a) -> list[float]:
    a = np.asarray([x for x in a if np.isfinite(x)])
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else [math.nan, math.nan]


# ----------------------------------------------------------------------------- secondary models
def cond_logit(df: pd.DataFrame, y: np.ndarray, sc: dict, gate: str = GATE) -> dict:
    from statsmodels.discrete.conditional_models import ConditionalLogit
    g = df.ci.to_numpy()
    mix = pd.Series(y).groupby(g).transform(lambda s: 0 < s.mean() < 1).to_numpy(bool)
    d, yy = df[mix], y[mix]
    cols0 = FE_VARY
    X0_ = Z(d, cols0, sc)
    X1_ = np.column_stack([X0_, Z(d, [gate], sc)])
    out = {"n_episodes_informative": int(mix.sum()), "n_concepts_informative": int(d.ci.nunique())}
    try:
        m0 = ConditionalLogit(yy, X0_, groups=d.ci.to_numpy()).fit(disp=0, maxiter=200)
        m1 = ConditionalLogit(yy, X1_, groups=d.ci.to_numpy()).fit(disp=0, maxiter=200)
        b, se = float(m1.params[-1]), float(m1.bse[-1])
        lr = 2 * (m1.llf - m0.llf)
        out.update({"beta_gateway_std": b, "se": se, "z": b / se, "p_two_sided": float(2 * stats.norm.sf(abs(b / se))),
                    "LR": float(lr), "LR_p": float(stats.chi2.sf(lr, 1)), "method": "ConditionalLogit"})
    except (np.linalg.LinAlgError, ValueError) as e:
        out.update({"error": repr(e)[:200]})
        out.update(mixed_logit_fallback(d, yy, sc, gate))
    return out


def mixed_logit_fallback(d, yy, sc, gate) -> dict:
    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM
    X = np.column_stack([np.ones(len(d)), Z(d, FE_VARY + [gate], sc)])
    codes = pd.factorize(d.ci)[0]
    exog_vc = np.zeros((len(d), codes.max() + 1))
    exog_vc[np.arange(len(d)), codes] = 1
    m = BinomialBayesMixedGLM(yy, X, exog_vc, np.zeros(codes.max() + 1, int)).fit_vb()
    b, se = float(m.fe_mean[-1]), float(m.fe_sd[-1])
    return {"method": "BinomialBayesMixedGLM (fallback)", "beta_gateway_std": b, "se": se, "z": b / se}


def lpm_fe(df: pd.DataFrame, y: np.ndarray, sc: dict, gcol: str = "gateway_js") -> dict:
    import statsmodels.api as sm
    cols = [c for c in X0 if c != "log_field_size"]
    X = pd.DataFrame(Z(df, cols, sc), columns=cols, index=df.index)
    X[gcol] = (df[gcol] - df[gcol].mean()) / (df[gcol].std() or 1)
    fe = pd.get_dummies(df.field.astype(str), prefix="f", drop_first=True, dtype=float)
    te = pd.get_dummies(df.t0.astype(str), prefix="t", drop_first=True, dtype=float)
    X = sm.add_constant(pd.concat([X, fe, te], axis=1))
    out = {"n": int(len(df)), "within_field_sd_of_regressor": float(df.groupby("field")[gcol].std().mean())}
    try:
        m1 = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(df.ci)[0]})
        m2 = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": np.column_stack(
            [pd.factorize(df.ci)[0], pd.factorize(df.field)[0]])})
        b = float(m1.params[gcol])
        out.update({"beta_within_per_sd": b, "se_concept": float(m1.bse[gcol]), "p_concept": float(m1.pvalues[gcol]),
                    "se_twoway": float(m2.bse[gcol]), "p_twoway": float(m2.pvalues[gcol])})
    except (np.linalg.LinAlgError, ValueError) as e:
        out["error"] = repr(e)[:200]
    return out


def boundary(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:
    import statsmodels.api as sm
    X = pd.DataFrame(Z(df, X1, sc), columns=X1, index=df.index)
    X["gw_x_toptercile"] = X[GATE] * df.top_tercile_home.to_numpy()
    X["top_tercile_home"] = df.top_tercile_home.to_numpy()
    X = sm.add_constant(X)
    try:
        m = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type="cluster",
                               cov_kwds={"groups": pd.factorize(df.ci)[0]})
        return {"beta_interaction": float(m.params["gw_x_toptercile"]), "se": float(m.bse["gw_x_toptercile"]),
                "p": float(m.pvalues["gw_x_toptercile"]), "beta_gateway_main": float(m.params[GATE]),
                "n_top_tercile_home_episodes": int(df.top_tercile_home.sum()),
                "prediction": "negative interaction", "consistent": bool(m.params["gw_x_toptercile"] < 0)}
    except (np.linalg.LinAlgError, ValueError, Exception) as e:  # noqa: BLE001 -- perfect separation etc.
        return {"error": repr(e)[:200]}


def logit_twoway(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:
    import statsmodels.api as sm
    X = sm.add_constant(pd.DataFrame(Z(df, X1, sc), columns=X1, index=df.index))
    out = {}
    for nm, grp in (("concept", pd.factorize(df.ci)[0]),
                    ("twoway", np.column_stack([pd.factorize(df.ci)[0], pd.factorize(df.field)[0]])),
                    ("field", pd.factorize(df.field)[0])):
        try:
            m = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type="cluster", cov_kwds={"groups": grp})
            out[nm] = {"beta_gateway_std": float(m.params[GATE]), "se": float(m.bse[GATE]),
                       "p": float(m.pvalues[GATE])}
        except Exception as e:  # noqa: BLE001
            out[nm] = {"error": repr(e)[:200]}
    return out


# ----------------------------------------------------------------------------- DEV phase
def load_dev() -> tuple[pd.DataFrame, pd.DataFrame]:
    F = pd.read_csv(ROOT / "episode_features.csv")
    co = pd.read_csv(ROOT / "concept_outcomes.csv")
    dev = F[F.split == "DEV"].copy()
    assert dev.R.notna().all(), "dev outcomes missing"
    dev = add_pj(dev)
    dev = dev.reset_index(drop=True)
    return dev, co


def logo_dauc(df, sc, y, grp, gate_col=GATE, base=None) -> dict:
    base = base if base is not None else logo_oof(df, X0, sc, y, grp)
    p1 = logo_oof(df, X0 + [gate_col], sc, y, grp)
    return {"auc0": auc(y, base), "auc1": auc(y, p1), "dauc": auc(y, p1) - auc(y, base), "p0": base, "p1": p1}


def placebo_dauc(df, sc, y, grp, vecs: np.ndarray, base) -> list[float]:
    fidx = df.field.to_numpy() - 11

    def one(v):
        d = df.copy()
        d["gw_pl"] = v[fidx]
        sc2 = dict(sc)
        sc2["gw_pl"] = [float(d.gw_pl.mean()), float(d.gw_pl.std() or 1)]
        p1 = logo_oof(d, X0 + ["gw_pl"], sc2, y, grp)
        return auc(y, p1) - auc(y, base)
    return Parallel(n_jobs=N_JOBS)(delayed(one)(v) for v in vecs)


def leave_field_out(df, sc, y, grp) -> dict:
    def one(f):
        m = df.field.to_numpy() != f
        d = df[m].reset_index(drop=True)
        r = logo_dauc(d, sc, y[m], grp[m])
        return f, r["dauc"]
    res = dict(Parallel(n_jobs=N_JOBS)(delayed(one)(f) for f in sorted(df.field.unique())))
    vals = np.array(list(res.values()))
    full = logo_dauc(df, sc, y, grp)["dauc"]
    infl = max(res, key=lambda f: abs(res[f] - full))
    return {"by_field": {str(k): v for k, v in res.items()}, "min": float(np.nanmin(vals)), "max": float(np.nanmax(vals)),
            "most_influential_field": int(infl), "dauc_without_it": res[infl], "full": full}


def pigeonhole(df, sc, y, grp, B: int, seed0: int, heldout=None) -> list[float]:
    """Crossed concept x field bootstrap (Owen 2007): row weight = multiplicity(concept) * multiplicity(field)."""
    cs = np.unique(df.ci)
    fs = np.unique(df.field)

    def one(b):
        rng = np.random.default_rng(seed0 + b)
        mc = pd.Series(rng.multinomial(len(cs), np.ones(len(cs)) / len(cs)), index=cs)
        mf = pd.Series(rng.multinomial(len(fs), np.ones(len(fs)) / len(fs)), index=fs)
        w = df.ci.map(mc).to_numpy(float) * df.field.map(mf).to_numpy(float)
        keep = w > 0
        d, yy, gg, ww = df[keep].reset_index(drop=True), y[keep], grp[keep], w[keep]
        if heldout is None:
            p0 = logo_oof(d, X0, sc, yy, gg, ww)
            p1 = logo_oof(d, X1, sc, yy, gg, ww)
            ok = np.isfinite(p0) & np.isfinite(p1)
            return auc(yy[ok], p1[ok], ww[ok]) - auc(yy[ok], p0[ok], ww[ok])
        hd, hy = heldout
        wh = hd.ci.map(mc).fillna(0).to_numpy(float) * hd.field.map(mf).fillna(0).to_numpy(float)
        return math.nan if wh.sum() == 0 else _fit_eval(d, yy, ww, hd, hy, wh, sc)
    return Parallel(n_jobs=N_JOBS)(delayed(one)(b) for b in range(B))


def pigeonhole_heldout(dev: pd.DataFrame, ho: pd.DataFrame, sc: dict, B: int, seed0: int) -> list[float]:
    """Crossed bootstrap for the held-out statistic: adopting FIELDS are resampled once per draw and shared by the
    dev refit and the held-out evaluation; dev concepts (refit) and held-out concepts (evaluation) are resampled
    independently. Row weight = multiplicity(concept) * multiplicity(field)."""
    fs = np.union1d(dev.field.unique(), ho.field.unique())
    cd, ch = dev.ci.unique(), ho.ci.unique()
    yd, yh = dev.R.to_numpy(int), ho.R.to_numpy(int)

    def one(b):
        rng = np.random.default_rng(seed0 + b)
        mf = pd.Series(rng.multinomial(len(fs), np.ones(len(fs)) / len(fs)), index=fs)
        md = pd.Series(rng.multinomial(len(cd), np.ones(len(cd)) / len(cd)), index=cd)
        mh = pd.Series(rng.multinomial(len(ch), np.ones(len(ch)) / len(ch)), index=ch)
        wd = dev.ci.map(md).to_numpy(float) * dev.field.map(mf).to_numpy(float)
        wh = ho.ci.map(mh).to_numpy(float) * ho.field.map(mf).to_numpy(float)
        kd = wd > 0
        if wh.sum() == 0 or len(np.unique(yh[wh > 0])) < 2:
            return math.nan
        return _fit_eval(dev[kd], yd[kd], wd[kd], ho, yh, wh, sc)
    return Parallel(n_jobs=N_JOBS)(delayed(one)(b) for b in range(B))


def _fit_eval(d, yy, ww, hd, hy, wh, sc):
    m0 = fit(Z(d, X0, sc), yy, ww)
    m1 = fit(Z(d, X1, sc), yy, ww)
    keep = wh > 0
    p0 = m0.predict_proba(Z(hd, X0, sc))[:, 1]
    p1 = m1.predict_proba(Z(hd, X1, sc))[:, 1]
    return auc(hy[keep], p1[keep], wh[keep]) - auc(hy[keep], p0[keep], wh[keep])


def power_sim(df, sc, y, n_heldout: int, seed: int = SEED) -> dict:
    X0m = Z(df, X0, sc)
    eta = fit(X0m, y).decision_function(X0m)
    gz = Z(df, [GATE], sc)[:, 0]
    cs = np.unique(df.ci)
    out = {}

    def sim(b, k):
        rng = np.random.default_rng(seed + 1000 * int(b * 10) + k)
        ys = rng.random(len(df)) < 1 / (1 + np.exp(-(eta + b * gz)))
        tr_c = set(rng.choice(cs, size=len(cs) // 2, replace=False))
        tr = df.ci.isin(tr_c).to_numpy()
        te_idx = np.nonzero(~tr)[0]
        te_idx = rng.choice(te_idx, size=n_heldout, replace=True)
        m0 = fit(X0m[tr], ys[tr])
        m1 = fit(np.column_stack([X0m, gz])[tr], ys[tr])
        p0 = m0.predict_proba(X0m[te_idx])[:, 1]
        p1 = m1.predict_proba(np.column_stack([X0m, gz])[te_idx])[:, 1]
        yt = ys[te_idx]
        d = auc(yt, p1) - auc(yt, p0)
        bs = []
        for _ in range(150):
            ii = rng.integers(0, len(te_idx), len(te_idx))
            bs.append(auc(yt[ii], p1[ii]) - auc(yt[ii], p0[ii]))
        return d, np.percentile(bs, 2.5) > 0
    for b in (0.0, 0.1, 0.2, 0.3):
        r = Parallel(n_jobs=N_JOBS)(delayed(sim)(b, k) for k in range(4 if SMOKE else 40))
        out[str(b)] = {"mean_dauc": float(np.mean([x[0] for x in r])), "power_ci_gt0": float(np.mean([x[1] for x in r]))}
    det = [float(v["mean_dauc"]) for k, v in out.items() if v["power_ci_gt0"] >= 0.8]
    out["min_detectable_dauc_80pct"] = min(det) if det else None
    out["n_heldout_episodes_assumed"] = n_heldout
    out["note"] = "planted effect b in SD log-odds of standardised gateway_j on the dev covariate structure; 40 sims x 150 boot"
    return out


def partial_spearman(x, y, Zc: np.ndarray) -> float:
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Zc).all(1)
    if ok.sum() < 8:
        return math.nan
    rx, ry = stats.rankdata(x[ok]), stats.rankdata(y[ok])
    RZ = np.column_stack([np.ones(ok.sum())] + [stats.rankdata(c) for c in Zc[ok].T])
    ex = rx - RZ @ np.linalg.lstsq(RZ, rx, rcond=None)[0]
    ey = ry - RZ @ np.linalg.lstsq(RZ, ry, rcond=None)[0]
    return float(np.corrcoef(ex, ey)[0, 1])


B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
# pre-registered explanatory ladder (reported next to the primary, never used for the verdict): where does the
# gateway increment disappear as the baseline grows from the iteration-1 base to the full X0?
LADDER = {"L1_iter1_base": B5 + ["log_n_early", "share_early", "growth_j", "log_field_size"]}
LADDER["L2_plus_relatedness"] = LADDER["L1_iter1_base"] + ["phi_home", "density"]
LADDER["L3_plus_Pj"] = LADDER["L2_plus_relatedness"] + ["P_j"]
LADDER["L4_full_X0"] = X0
LADDER["L0_size_only"] = ["log_n_early", "share_early", "log_field_size"]
H3_VARS = ["G", "G_A", "G_btw"]


def h3_table(fc: pd.DataFrame, co: pd.DataFrame, cf: pd.DataFrame, split_mask, resid_ab) -> pd.DataFrame:
    d = fc[split_mask][["ci", "group", "split"]].merge(co.drop(columns=["split"], errors="ignore"), on="ci") \
        .merge(cf, on=["ci"], suffixes=("", "_cf"))
    a, b = resid_ab
    d["O2r_resid"] = d.O2r_m30 - (a + b * np.log(d.N_outcome.clip(lower=1)))
    return d


def cmd_dev() -> None:
    t_start = time.time()
    dev, co = load_dev()
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    cf = pd.read_csv(ROOT / "concept_features_basic.csv")
    y = dev.R.to_numpy(int)
    grp = dev.group.to_numpy()
    sc = std_consts(dev, X1 + ["gateway_js", "gateway_deg", "gateway_btw", "gateway_phimin", "gateway_S0rec",
                               "log_field_size_s"])
    res = {"n_episodes": len(dev), "n_concepts": int(dev.ci.nunique()), "R_rate": float(y.mean()),
           "by_group": dev.groupby("group").agg(n=("R", "size"), R=("R", "mean"), concepts=("ci", "nunique")).to_dict("index")}
    logger.info(f"DEV: {res['n_episodes']} episodes / {res['n_concepts']} concepts, R rate {y.mean():.3f}")
    base = logo_oof(dev, X0, sc, y, grp)
    prim = logo_dauc(dev, sc, y, grp, base=base)
    res["primary"] = {"auc_X0": prim["auc0"], "auc_X1": prim["auc1"], "dauc": prim["dauc"],
                      "per_group": {g: {"auc_X0": auc(y[grp == g], prim["p0"][grp == g]),
                                        "auc_X1": auc(y[grp == g], prim["p1"][grp == g]),
                                        "dauc": auc(y[grp == g], prim["p1"][grp == g]) - auc(y[grp == g], prim["p0"][grp == g]),
                                        "n": int((grp == g).sum())} for g in DEV_GROUPS}}
    dev["oof_X0"], dev["oof_X1"] = prim["p0"], prim["p1"]
    logger.info(f"DEV primary dAUC={prim['dauc']:+.4f} (AUC0 {prim['auc0']:.3f})")
    # refit bootstrap (2,000) -- also carries the rival head-to-head models (paired)
    Xr = [c for c in X0 if c not in ("phi_home", "density")]
    t = time.time()
    bs = boot_logo(dev, {"X0": X0, "X1": X1}, sc, y, grp, B_MAIN, SEED)
    d_boot = [b["X1"] - b["X0"] for b in bs]
    res["primary"]["boot_ci95"] = ci95(d_boot)
    res["primary"]["boot_sd"] = float(np.nanstd(d_boot))
    res["primary"]["boot_p_le0"] = float(np.mean(np.array(d_boot) <= 0))
    for g in DEV_GROUPS:
        gd = [b["per_group"][g]["X1"] - b["per_group"][g]["X0"] for b in bs]
        res["primary"]["per_group"][g]["boot_se"] = float(np.nanstd(gd))
    res["primary"]["dl_pool_groups"] = dl_pool([res["primary"]["per_group"][g]["dauc"] for g in DEV_GROUPS],
                                               [res["primary"]["per_group"][g]["boot_se"] for g in DEV_GROUPS])
    # T5 stability: second seed on 500 draws vs first 500
    bs2 = boot_logo(dev, {"X0": X0, "X1": X1}, sc, y, grp, B_SMALL, SEED + 1_000_000)  # disjoint seed range
    c1 = ci95(d_boot[:B_SMALL])
    c2 = ci95([b["X1"] - b["X0"] for b in bs2])
    res["T5_seed_stability"] = {"ci_seed1_500": c1, "ci_seed2_500": c2, "max_abs_diff": float(np.max(np.abs(np.subtract(c1, c2))))}
    logger.info(f"bootstrap done in {time.time()-t:.0f}s; CI {res['primary']['boot_ci95']}")
    bsr = boot_logo(dev, {"Xr": Xr, "Xr_rel": Xr + ["phi_home", "density"], "Xr_gw": Xr + [GATE]}, sc, y, grp,
                    B_SMALL, SEED + 3)
    rel = [b["Xr_rel"] - b["Xr"] for b in bsr]
    gw = [b["Xr_gw"] - b["Xr"] for b in bsr]
    base_r = logo_oof(dev, Xr, sc, y, grp)
    p_rel = logo_oof(dev, Xr + ["phi_home", "density"], sc, y, grp)
    p_gw = logo_oof(dev, Xr + [GATE], sc, y, grp)
    res["rival_head_to_head"] = {"dauc_relatedness_pair": auc(y, p_rel) - auc(y, base_r),
                                 "dauc_gateway": auc(y, p_gw) - auc(y, base_r),
                                 "diff_gateway_minus_relatedness": (auc(y, p_gw) - auc(y, p_rel)),
                                 "diff_boot_ci95": ci95(np.subtract(gw, rel)),
                                 "relatedness_boot_ci95": ci95(rel), "gateway_boot_ci95": ci95(gw)}
    # explanatory ladder (dev, LOGO, 500-draw refit bootstrap each)
    res["ladder"] = {}
    for nm, cols in LADDER.items():
        b0 = logo_oof(dev, cols, sc, y, grp)
        b1 = logo_oof(dev, cols + [GATE], sc, y, grp)
        bl = boot_logo(dev, {"a": cols, "b": cols + [GATE]}, sc, y, grp, B_SMALL, SEED + 5)
        res["ladder"][nm] = {"cols": cols, "auc_base": auc(y, b0), "dauc": auc(y, b1) - auc(y, b0),
                             "ci95": ci95([x["b"] - x["a"] for x in bl])}
    res["gateway_alone_auc"] = auc(y, dev[GATE].to_numpy())
    # secondary
    res["cond_logit"] = cond_logit(dev, y, sc)
    res["lpm_field_fe"] = lpm_fe(dev, y, sc)
    res["boundary"] = boundary(dev, y, sc)
    res["logit_clustered_se"] = logit_twoway(dev, y, sc)
    # placebo
    pl = np.load(ROOT / "placebo_gateways.npy")
    pp = np.load(ROOT / "placebo_perm_gateways.npy")
    pld = placebo_dauc(dev, sc, y, grp, pl, base)
    ppd = placebo_dauc(dev, sc, y, grp, pp, base)
    res["placebo_rewired"] = {"n": len(pld), "p95": float(np.nanpercentile(pld, 95)), "mean": float(np.nanmean(pld)),
                              "real": prim["dauc"], "share_ge_real": float(np.mean(np.array(pld) >= prim["dauc"])),
                              "real_exceeds_p95": bool(prim["dauc"] > np.nanpercentile(pld, 95)), "values": pld}
    res["placebo_permutation"] = {"n": len(ppd), "p95": float(np.nanpercentile(ppd, 95)),
                                  "share_ge_real": float(np.mean(np.array(ppd) >= prim["dauc"])), "values": ppd}
    # field-level robustness
    res["leave_one_field_out"] = leave_field_out(dev, sc, y, grp)
    ph = pigeonhole(dev, sc, y, grp, B_SMALL, SEED + 7)
    res["pigeonhole_crossed_bootstrap"] = {"B": B_SMALL, "ci95": ci95(ph), "sd": float(np.nanstd(ph))}
    # power (held-out n known outcome-blind from the frame)
    ep_all = pd.read_csv(ROOT / "episodes.csv", usecols=["split"])
    n_ho = int(ep_all.split.str.startswith("HELDOUT").sum())
    res["power"] = power_sim(dev, sc, y, max(n_ho, 50))
    # H3 on dev
    dco = co[co.split == "DEV"].dropna(subset=["O2r_m30", "N_outcome"])
    bfit = np.polyfit(np.log(dco.N_outcome.clip(lower=1)), dco.O2r_m30, 1)
    resid_ab = [float(bfit[1]), float(bfit[0])]
    h = h3_table(fc, co, cf, (fc.split == "DEV").to_numpy(), resid_ab)
    Zc = h[B5].to_numpy(float)
    res["H3_dev"] = {v: partial_spearman(h[v].to_numpy(float), h.O2r_resid.to_numpy(float), Zc) for v in H3_VARS + ["REL_home"]}
    res["H3_dev"]["n"] = int(h.O2r_resid.notna().sum())
    res["runtime_s"] = time.time() - t_start
    if SMOKE:
        jdump(res, RES / "h1_dev_smoke.json")
        logger.info(f"SMOKE done in {time.time()-t_start:.0f}s (no freeze)")
        return
    dev.to_csv(ROOT / "dev_episodes_with_oof.csv", index=False)
    jdump(res, RES / "h1_dev.json")
    # --------------------------------------------------------------- FREEZE
    ep = pd.read_csv(ROOT / "episodes.csv", usecols=["ci", "split"])
    lexh = (ROOT / "frozen_lexicon.sha256").read_text().strip().splitlines()[-1].split()[-1]
    sfh = hashlib.sha256((ROOT / "sense_filter.joblib").read_bytes()).hexdigest()
    spec = {"created": time.strftime("%Y-%m-%d %H:%M:%S"), "X0": X0, "X1": X1, "gateway": GATE,
            "standardisation": sc, "C": C_REG, "solver": "Newton-IRLS (exact L2 optimum; sklearn objective)", "P_j": {"pseudo_count": PJ_M, "window": PJ_WIN,
                                                                                      "split_sets": ["DEV", "HELDOUT", "COHORT"]},
            "R_primary": "share_out >= 0.5*share_early AND n_out >= 9 (t0+6..t0+8)",
            "R_sensitivities": ["R_abs1", "R_abs2", "R_abs3"], "episode_rule": "n_early >= 2 grounded labelled, j not home",
            "group_map": "common.GROUP_OF_FIELD", "dev_groups": DEV_GROUPS, "heldout_groups": HELD_GROUPS,
            "O2r_resid": {"a": resid_ab[0], "b": resid_ab[1]}, "bootstrap": {"B": B_MAIN, "seed": SEED},
            "placebo_seeds": f"{SEED}+k, k=0..199", "verdict_rules": {
                "pooled_dauc_min": 0.05, "ci_gt0": True, "sign_groups_min": 3, "cohort_same_sign": True,
                "lpm_beta_within_gt0_p": 0.05, "placebo_real_gt_p95": True},
            "lexicon_v1_sha256": lexh, "sense_filter_sha256": sfh,
            "heldout_concept_ids": sorted(int(c) for c in fc.loc[fc.split.str.startswith("HELDOUT"), "concept_id"]),
            "cohort_concept_ids": sorted(int(c) for c in fc.loc[fc.split == "COHORT", "concept_id"]),
            "insularity": "dropped (NA; API pool below floor)", "dev_primary_dauc": prim["dauc"],
            "ladder": LADDER, "sensitivities": ["R_abs1", "R_abs2", "R_abs3", "n_early_ge5", "newborn_only",
                                                "excl_intersection_born", "P_j_train", "gateway_deg/btw/phimin/S0rec",
                                                "log_field_size_slice", "without_P_j", "alt_ptopic", "alt_match",
                                                "alt_b5_t0p4"],
            "H3": {"vars": H3_VARS, "rival": "REL_home", "outcome": "O2r_resid", "controls": B5,
                   "permutations": 2000, "holm": True}}
    try:
        subprocess.run(["git", "init", "-q"], cwd=ROOT, check=False)
        subprocess.run(["git", "add", "-A", "--", "*.py", "tests", "pyproject.toml", "frozen_lexicon.sha256",
                        "results", "frame_concepts.csv", "episodes.csv", "concept_outcomes.csv", ".gitignore"],
                       cwd=ROOT, check=False, capture_output=True)
        subprocess.run(["git", "-c", "user.name=AMGrobelnik", "-c", "user.email=noreply@anthropic.com", "commit", "-q",
                        "-m", "Freeze dev specification before unsealing held-out outcomes\n\n"
                        "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], cwd=ROOT, check=False,
                       capture_output=True)
        gh = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    except OSError:
        gh = "unavailable"
    spec["git_hash_code"] = gh
    SPEC.write_text(json.dumps(spec, indent=1))
    h = hashlib.sha256(SPEC.read_bytes()).hexdigest()
    # T6 pre-unseal checklist
    held_rows = pd.read_csv(ROOT / "episodes.csv")
    hmask = held_rows.split != "DEV"
    t6 = {"frozen_spec_complete": all(k in spec for k in ("X0", "X1", "standardisation", "heldout_concept_ids")),
          "heldout_outcomes_absent_episodes": bool(held_rows.loc[hmask, "R"].isna().all()),
          "heldout_outcomes_absent_concepts": bool(pd.read_csv(ROOT / "concept_outcomes.csv").query("split != 'DEV'")
                                                   .get("O2r_m30", pd.Series(dtype=float)).isna().all()),
          "git_commit": gh}
    with (LOGS / "seal.log").open("a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} FREEZE sha256(frozen_spec.json)={h}\n")
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} T6 {json.dumps(t6)}\n")
    logger.info(f"FROZEN: sha256={h[:16]} T6={t6} runtime {time.time()-t_start:.0f}s")


# ----------------------------------------------------------------------------- HELD-OUT phase
def _boot_ho(seed, dev, ydev, cidx_dev, dev_cg, ho, yho, cidx_ho, ho_cg, sc, cols_pair):
    rng = np.random.default_rng(seed)
    di = np.concatenate([cidx_dev[c] for g in dev_cg for c in rng.choice(dev_cg[g], len(dev_cg[g]), replace=True)])
    hi_by_g = {g: np.concatenate([cidx_ho[c] for c in rng.choice(ho_cg[g], len(ho_cg[g]), replace=True)])
               for g in ho_cg if len(ho_cg[g])}
    d = dev.iloc[di]
    m0 = fit(Z(d, cols_pair[0], sc), ydev[di])
    m1 = fit(Z(d, cols_pair[1], sc), ydev[di])
    out = {}
    allidx = np.concatenate(list(hi_by_g.values()))
    for key, idx in list(hi_by_g.items()) + [("pooled", allidx)]:
        h = ho.iloc[idx]
        p0 = m0.predict_proba(Z(h, cols_pair[0], sc))[:, 1]
        p1 = m1.predict_proba(Z(h, cols_pair[1], sc))[:, 1]
        out[key] = auc(yho[idx], p1) - auc(yho[idx], p0)
    return out


def score_heldout(dev, ho, sc, cols0=X0, cols1=X1, rcol="R", B=B_MAIN, seed=SEED, groups=HELD_GROUPS):
    """Fit on all dev, evaluate on `ho`. Returns point estimates per group + pooled and bootstrap CIs."""
    ydev = dev[rcol].to_numpy(int)
    yho = ho[rcol].to_numpy(int)
    m0 = fit(Z(dev, cols0, sc), ydev)
    m1 = fit(Z(dev, cols1, sc), ydev)
    p0 = m0.predict_proba(Z(ho, cols0, sc))[:, 1]
    p1 = m1.predict_proba(Z(ho, cols1, sc))[:, 1]
    g = ho.group.to_numpy()
    out = {"n": int(len(ho)), "n_concepts": int(ho.ci.nunique()), "R_rate": float(yho.mean()),
           "auc_X0": auc(yho, p0), "auc_X1": auc(yho, p1), "dauc": auc(yho, p1) - auc(yho, p0), "per_group": {}}
    for gg in groups:
        m = g == gg
        out["per_group"][gg] = {"n": int(m.sum()), "n_concepts": int(ho[m].ci.nunique()),
                                "auc_X0": auc(yho[m], p0[m]), "auc_X1": auc(yho[m], p1[m]),
                                "dauc": auc(yho[m], p1[m]) - auc(yho[m], p0[m]) if m.sum() else math.nan}
    if B:
        cidx_dev = concept_index(dev)
        dcg = dev.groupby("ci").group.first()
        dev_cg = {k: dcg.index[dcg == k].to_numpy() for k in dcg.unique()}
        cidx_ho = concept_index(ho)
        hcg = ho.groupby("ci").group.first()
        ho_cg = {k: hcg.index[hcg == k].to_numpy() for k in groups}
        bs = Parallel(n_jobs=N_JOBS, batch_size=16)(delayed(_boot_ho)(seed + b, dev, ydev, cidx_dev, dev_cg, ho, yho,
                                                                       cidx_ho, ho_cg, sc, (cols0, cols1)) for b in range(B))
        out["boot_ci95"] = ci95([b["pooled"] for b in bs])
        out["boot_p_le0"] = float(np.mean(np.array([b["pooled"] for b in bs]) <= 0))
        for gg in groups:
            vals = [b.get(gg, math.nan) for b in bs]
            out["per_group"][gg]["boot_se"] = float(np.nanstd(vals))
            out["per_group"][gg]["boot_ci95"] = ci95(vals)
    return out, p0, p1


def cmd_heldout() -> None:
    import seal
    seal.assert_unsealed()
    spec = json.loads(SPEC.read_text())
    sc = spec["standardisation"]
    F = pd.read_csv(ROOT / "episode_features.csv")
    ep = pd.read_csv(ROOT / "episodes.csv")
    F = F.drop(columns=[c for c in ("n_out", "share_out", "R", "R_abs1", "R_abs2", "R_abs3", "lab_out") if c in F]) \
        .merge(ep[["ci", "field", "n_out", "share_out", "R", "R_abs1", "R_abs2", "R_abs3", "lab_out"]], on=["ci", "field"])
    F = add_pj(F)
    F = add_pj_train(F)
    res = analyze_heldout(F, sc, seal.spec_sha(), HELD_GROUPS)
    jdump(res, RES / "h1_heldout.json")
    h3_heldout(spec)


def smoke_heldout() -> None:
    """Pre-unseal smoke test of the held-out code path on DEV data only: CS + Eng act as 'dev', BGM and Med as two
    pseudo held-out groups (relabelled), a random half of dev concepts as a pseudo cohort. Nothing sealed is read."""
    F = pd.read_csv(ROOT / "episode_features.csv")
    F = F[F.split == "DEV"].copy()
    rng = np.random.default_rng(0)
    coh_c = set(rng.choice(F[F.group.isin(["CS", "Eng"])].ci.unique(), 300, replace=False))
    F.loc[F.group == "BGM", "split"] = "HELDOUT_PSEUDO_A"
    F.loc[F.group == "Med", "split"] = "HELDOUT_PSEUDO_B"
    F.loc[F.ci.isin(coh_c), "split"] = "COHORT"
    F.loc[F.split == "HELDOUT_PSEUDO_A", "group"] = "PSA"
    F.loc[F.split == "HELDOUT_PSEUDO_B", "group"] = "PSB"
    F = add_pj(F)
    F = add_pj_train(F)
    sc = std_consts(F[F.split == "DEV"], X1 + ["gateway_js", "gateway_deg", "gateway_btw", "gateway_phimin",
                                               "gateway_S0rec", "log_field_size_s"])
    res = analyze_heldout(F, sc, "smoke", ["PSA", "PSB"], dev_groups_for_logo=["CS", "Eng"])
    jdump(res, RES / "h1_heldout_smoke.json")
    logger.info(f"smoke held-out: dAUC {res['primary']['dauc']:+.4f} verdict {res['verdict_H1']}")


def analyze_heldout(F: pd.DataFrame, sc: dict, sha: str, groups: list[str], dev_groups_for_logo=None) -> dict:
    n_undef = F[F.R.isna()].groupby("split").size().to_dict()
    F = F[F.R.notna()].copy()  # R undefined when no labelled outcome work exists (share_out = 0/0); excluded as in dev
    dev = F[F.split == "DEV"].reset_index(drop=True)
    ho = F[F.split.str.startswith("HELDOUT")].reset_index(drop=True)
    coh = F[F.split == "COHORT"].reset_index(drop=True)
    res = {"spec_sha256": sha, "n_dev": len(dev), "n_heldout": len(ho), "n_cohort": len(coh),
           "n_R_undefined_excluded": n_undef}
    prim, p0, p1 = score_heldout(dev, ho, sc, groups=groups)
    ho["pred_X0"], ho["pred_X1"] = p0, p1
    res["primary"] = prim
    evaluable = [g for g in groups if prim["per_group"][g]["n_concepts"] >= 15]
    res["dl_pool"] = dl_pool([prim["per_group"][g]["dauc"] for g in evaluable],
                             [prim["per_group"][g]["boot_se"] for g in evaluable])
    res["evaluable_groups"] = evaluable
    res["sign_test_groups"] = sign_test([prim["per_group"][g]["dauc"] for g in evaluable])
    coh_groups = sorted(coh.group.unique())
    coh_s, c0, c1 = score_heldout(dev, coh, sc, groups=coh_groups)
    coh["pred_X0"], coh["pred_X1"] = c0, c1
    res["cohort"] = coh_s
    logger.info(f"HELD-OUT dAUC={prim['dauc']:+.4f} CI {prim.get('boot_ci95')}; cohort {coh_s['dauc']:+.4f}")
    yho = ho.R.to_numpy(int)
    res["cond_logit"] = cond_logit(ho, yho, sc)
    res["lpm_field_fe"] = lpm_fe(ho, yho, sc)
    res["lpm_field_fe_all_splits"] = lpm_fe(F.dropna(subset=["R"]).reset_index(drop=True),
                                            F.dropna(subset=["R"]).R.to_numpy(int), sc)
    res["boundary"] = boundary(ho, yho, sc)
    res["logit_clustered_se"] = logit_twoway(ho, yho, sc)
    # relatedness head-to-head on held-out (fit on dev)
    Xr = [c for c in X0 if c not in ("phi_home", "density")]
    rel, _, _ = score_heldout(dev, ho, sc, Xr, Xr + ["phi_home", "density"], B=B_SMALL, seed=SEED + 11, groups=groups)
    gw, _, _ = score_heldout(dev, ho, sc, Xr, Xr + [GATE], B=B_SMALL, seed=SEED + 11, groups=groups)
    res["rival_head_to_head"] = {"dauc_relatedness_pair": rel["dauc"], "relatedness_ci95": rel.get("boot_ci95"),
                                 "dauc_gateway": gw["dauc"], "gateway_ci95": gw.get("boot_ci95"),
                                 "diff_gateway_minus_relatedness": gw["dauc"] - rel["dauc"]}
    res["ladder"] = {}
    for nm, cols in LADDER.items():
        r_, _, _ = score_heldout(dev, ho, sc, cols, cols + [GATE], B=B_SMALL, seed=SEED + 5, groups=groups)
        res["ladder"][nm] = {"auc_base": r_["auc_X0"], "dauc": r_["dauc"], "ci95": r_.get("boot_ci95"),
                             "per_group": {g: v["dauc"] for g, v in r_["per_group"].items()}}
    res["gateway_alone_auc"] = auc(yho, ho[GATE].to_numpy())
    # placebo on held-out: dev-fit with placebo vector, evaluate on held-out
    pl = np.load(ROOT / "placebo_gateways.npy")
    pp = np.load(ROOT / "placebo_perm_gateways.npy")

    def pl_one(v):
        d, h = dev.copy(), ho.copy()
        d["gw_pl"] = v[d.field.to_numpy() - 11]
        h["gw_pl"] = v[h.field.to_numpy() - 11]
        sc2 = dict(sc)
        sc2["gw_pl"] = [float(d.gw_pl.mean()), float(d.gw_pl.std() or 1)]
        r, _, _ = score_heldout(d, h, sc2, X0, X0 + ["gw_pl"], B=0, groups=groups)
        return r["dauc"]
    pld = Parallel(n_jobs=N_JOBS)(delayed(pl_one)(v) for v in pl)
    ppd = Parallel(n_jobs=N_JOBS)(delayed(pl_one)(v) for v in pp)
    res["placebo_rewired"] = {"p95": float(np.nanpercentile(pld, 95)), "mean": float(np.nanmean(pld)),
                              "share_ge_real": float(np.mean(np.array(pld) >= prim["dauc"])),
                              "real_exceeds_p95": bool(prim["dauc"] > np.nanpercentile(pld, 95)), "values": pld}
    res["placebo_permutation"] = {"p95": float(np.nanpercentile(ppd, 95)),
                                  "share_ge_real": float(np.mean(np.array(ppd) >= prim["dauc"])), "values": ppd}
    # field-level robustness on held-out
    lofo = {}
    for f in sorted(ho.field.unique()):
        r, _, _ = score_heldout(dev[dev.field != f].reset_index(drop=True), ho[ho.field != f].reset_index(drop=True),
                                sc, B=0, groups=groups)
        lofo[str(f)] = r["dauc"]
    vals = np.array(list(lofo.values()))
    infl = max(lofo, key=lambda k: abs(lofo[k] - prim["dauc"]))
    res["leave_one_field_out"] = {"by_field": lofo, "min": float(np.nanmin(vals)), "max": float(np.nanmax(vals)),
                                  "most_influential_field": int(infl), "dauc_without_it": lofo[infl]}
    ph = pigeonhole_heldout(dev, ho, sc, B_SMALL, SEED + 17)
    res["pigeonhole_crossed_bootstrap"] = {"B": B_SMALL, "ci95": ci95(ph), "sd": float(np.nanstd(ph))}
    # verdict
    signs_ok = sum(1 for g in evaluable if prim["per_group"][g]["dauc"] > 0)
    lpm = res["lpm_field_fe"]
    crit = {"pooled_dauc_ge_0.05": bool(prim["dauc"] >= 0.05),
            "refit_ci_gt0": bool(prim["boot_ci95"][0] > 0),
            "sign_ge3_of_4_evaluable": bool(signs_ok >= 3), "n_groups_positive": signs_ok,
            "cohort_same_sign": bool(np.sign(coh_s["dauc"]) == np.sign(prim["dauc"])),
            "lpm_beta_within_gt0_p05": bool(lpm.get("beta_within_per_sd", -1) > 0 and lpm.get("p_concept", 1) < 0.05),
            "placebo_null": res["placebo_rewired"]["real_exceeds_p95"]}
    core = ["pooled_dauc_ge_0.05", "refit_ci_gt0", "sign_ge3_of_4_evaluable", "cohort_same_sign",
            "lpm_beta_within_gt0_p05", "placebo_null"]
    if all(crit[k] for k in core):
        verdict = "CONFIRMED"
    elif prim["dauc"] > 0 and prim["boot_ci95"][0] > 0:
        verdict = "PARTIAL"
    elif prim["dauc"] > 0 and signs_ok >= 3:
        verdict = "PARTIAL"
    else:
        verdict = "DISCONFIRMED"
    res["verdict_H1"] = {"verdict": verdict, "criteria": crit}
    res["sensitivities"] = sensitivities(F, dev, ho, sc, groups)
    if sha != "smoke":
        ho.to_csv(ROOT / "heldout_episodes_with_pred.csv", index=False)
        coh.to_csv(ROOT / "cohort_episodes_with_pred.csv", index=False)
    logger.info(f"H1 verdict {verdict}: {crit}")
    return res


def sensitivities(F, dev, ho, sc, groups=HELD_GROUPS) -> dict:
    out = {}

    def run(name, d, h, cols0=X0, cols1=X1, rcol="R"):
        try:
            r, _, _ = score_heldout(d.dropna(subset=[rcol]).reset_index(drop=True),
                                    h.dropna(subset=[rcol]).reset_index(drop=True), sc, cols0, cols1, rcol=rcol,
                                    B=200, seed=SEED + 99, groups=groups)
            out[name] = {"dauc": r["dauc"], "ci95": r.get("boot_ci95"), "n": r["n"],
                         "per_group": {g: v["dauc"] for g, v in r["per_group"].items()}}
        except (ValueError, KeyError) as e:
            out[name] = {"error": repr(e)[:200]}
    for rc in ("R_abs1", "R_abs2", "R_abs3"):
        run(rc, dev, ho, rcol=rc)
    run("n_early_ge5", dev[dev.n_early >= 5], ho[ho.n_early >= 5])
    run("newborn_only", dev[dev.newborn.astype(bool)], ho[ho.newborn.astype(bool)])
    run("excl_intersection_born", dev[dev.intersect40 == 0], ho[ho.intersect40 == 0])
    d2, h2 = dev.copy(), ho.copy()
    d2["P_j"], h2["P_j"] = d2.P_j_trainset, h2.P_j_trainset
    run("P_j_train_instead_of_Pj", d2, h2)
    for gv in ("gateway_deg", "gateway_btw", "gateway_phimin", "gateway_S0rec"):
        run(f"gateway_variant_{gv}", dev, ho, X0, X0 + [gv])
    run("log_field_size_slice", dev, ho, [c if c != "log_field_size" else "log_field_size_s" for c in X0],
        [c if c != "log_field_size" else "log_field_size_s" for c in X1])
    run("without_P_j", dev, ho, [c for c in X0 if c != "P_j"], [c for c in X1 if c != "P_j"])
    for alt in ("ptopic", "match", "b5_t0p4"):
        p = ROOT / f"sens_episodes_{alt}.csv"
        if p.exists():
            A = pd.read_csv(p)
            A = add_pj(A)
            run(f"alt_{alt}", A[A.split == "DEV"], A[A.split.str.startswith("HELDOUT")])
    return out


def h3_heldout(spec) -> None:
    import seal  # noqa: F401
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    co = pd.read_csv(ROOT / "concept_outcomes.csv")
    cf = pd.read_csv(ROOT / "concept_features_basic.csv")
    ab = (spec["O2r_resid"]["a"], spec["O2r_resid"]["b"])
    h = h3_table(fc, co, cf, fc.split.str.startswith("HELDOUT").to_numpy(), ab).dropna(subset=["O2r_resid"])
    Zc = h[B5].to_numpy(float)
    rng = np.random.default_rng(SEED)
    res = {"n": int(len(h))}
    pvals = {}
    for v in H3_VARS + ["REL_home"]:
        x = h[v].to_numpy(float)
        yv = h.O2r_resid.to_numpy(float)
        rho = partial_spearman(x, yv, Zc)
        perm = []
        g = h.group.to_numpy()
        for _ in range(2000):
            xp = x.copy()
            for gg in np.unique(g):
                m = g == gg
                xp[m] = rng.permutation(xp[m])
            perm.append(partial_spearman(xp, yv, Zc))
        p = float((1 + np.sum(np.array(perm) >= rho)) / (1 + len(perm)))
        bs = []
        for _ in range(1000):
            ii = rng.integers(0, len(h), len(h))
            bs.append(partial_spearman(x[ii], yv[ii], Zc[ii]))
        per = {}
        for gg in HELD_GROUPS:
            m = g == gg
            r_g = partial_spearman(x[m], yv[m], Zc[m]) if m.sum() >= 10 else math.nan
            bsg = [partial_spearman(x[m][ii], yv[m][ii], Zc[m][ii])
                   for ii in (rng.integers(0, m.sum(), m.sum()) for _ in range(300))] if m.sum() >= 10 else []
            per[gg] = {"rho": r_g, "n": int(m.sum()), "se": float(np.nanstd(bsg)) if bsg else math.nan}
        res[v] = {"partial_rho": rho, "p_perm_one_sided": p, "ci95": ci95(bs), "per_group": per,
                  "dl_pool": dl_pool([per[k]["rho"] for k in HELD_GROUPS], [per[k]["se"] for k in HELD_GROUPS])}
        if v in H3_VARS:
            pvals[v] = p
    order = sorted(pvals, key=pvals.get)
    holm = {}
    run_max = 0.0
    for i, v in enumerate(order):
        adj = min(1.0, (len(order) - i) * pvals[v])
        run_max = max(run_max, adj)
        holm[v] = run_max
    res["holm_adjusted_p"] = holm
    res["verdict_H3"] = "CONFIRMED" if any(holm[v] < 0.05 and res[v]["partial_rho"] > 0 for v in H3_VARS) else "NOT CONFIRMED"
    jdump(res, RES / "h3_results.json")
    logger.info(f"H3 held-out: { {v: round(res[v]['partial_rho'], 3) for v in H3_VARS} } holm={holm}")


if __name__ == "__main__":
    {"dev": cmd_dev, "heldout": cmd_heldout, "smoke_heldout": smoke_heldout}[sys.argv[1]]()
