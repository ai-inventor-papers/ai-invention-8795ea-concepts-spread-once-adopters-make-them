"""Pre-registered S0 screen statistics: LOGO ridge/logistic, paired bootstrap deltas, per-group signs,
DerSimonian-Laird pooling, field-level clustered bootstrap."""
from __future__ import annotations

import math
import warnings

import numpy as np
import pandas as pd
from scipy.stats import norm, rankdata, spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore", category=RuntimeWarning)
GROUPS = ["CS", "Eng", "BGM", "Med"]


def _prep(X: pd.DataFrame, train: np.ndarray) -> np.ndarray:
    """Median-impute each column with the TRAINING-fold median (G's missing indicator is a separate column)."""
    X = X.copy()
    for c in X.columns:
        med = X.loc[train, c].median()
        X[c] = X[c].fillna(med if np.isfinite(med) else 0.0)
    return X.values.astype(float)


def logo_predict(df: pd.DataFrame, cols: list[str], y: str, kind: str = "ridge") -> np.ndarray:
    """Leave-one-home-group-out out-of-fold predictions."""
    oof = np.full(len(df), np.nan)
    g = df["group"].values
    for lg in GROUPS:
        te = g == lg
        tr = ~te
        if te.sum() == 0 or tr.sum() < 5:
            continue
        Xall = _prep(df[cols], tr)
        yt = df.loc[tr, y].values
        if kind == "ridge":
            m = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
            m.fit(Xall[tr], yt)
            oof[te] = m.predict(Xall[te])
        else:
            if len(np.unique(yt)) < 2:
                oof[te] = yt.mean()
                continue
            m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000))
            m.fit(Xall[tr], yt.astype(int))
            oof[te] = m.predict_proba(Xall[te])[:, 1]
    return oof


def _sp(a, b) -> float:
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 4 or np.std(a[ok]) == 0 or np.std(b[ok]) == 0:
        return math.nan
    return float(spearmanr(a[ok], b[ok]).statistic)


def _auc(y, p) -> float:
    ok = np.isfinite(p) & np.isfinite(y)
    if ok.sum() < 4 or len(np.unique(y[ok])) < 2:
        return math.nan
    return float(roc_auc_score(y[ok].astype(int), p[ok]))


def paired_delta(df: pd.DataFrame, base: list[str], cand: list[str], y: str, kind: str = "ridge",
                 n_boot: int = 2000, seed: int = 20260928, refit_boot: int = 0) -> dict:
    d = df[np.isfinite(df[y].values.astype(float))].reset_index(drop=True)
    ob = logo_predict(d, base, y, kind)
    oc = logo_predict(d, cand, y, kind)
    Y = d[y].values.astype(float)
    stat = _sp if kind == "ridge" else (lambda p, yy: _auc(yy, p))
    sb, sc = stat(ob, Y), stat(oc, Y)
    rng = np.random.default_rng(seed)
    n = len(d)
    boots = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        a, b = stat(ob[i], Y[i]), stat(oc[i], Y[i])
        if np.isfinite(a) and np.isfinite(b):
            boots.append(b - a)
    boots = np.array(boots)
    per = {}
    for g in GROUPS:
        m = d["group"].values == g
        pb, pc = stat(ob[m], Y[m]), stat(oc[m], Y[m])
        per[g] = {"n": int(m.sum()), "base": pb, "cand": pc,
                  "delta": (pc - pb) if np.isfinite(pb) and np.isfinite(pc) else math.nan}
    out = {"n": n, "metric": "spearman" if kind == "ridge" else "auc", "base": sb, "cand": sc, "delta": sc - sb,
           "ci90": [float(np.percentile(boots, 5)), float(np.percentile(boots, 95))] if len(boots) else [math.nan] * 2,
           "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))] if len(boots) else [math.nan] * 2,
           "p_boot_le0": float(np.mean(boots <= 0)) if len(boots) else math.nan,
           "per_group": per,
           "n_groups_positive": int(sum(1 for v in per.values() if np.isfinite(v["delta"]) and v["delta"] > 0)),
           "n_groups_evaluable": int(sum(1 for v in per.values() if np.isfinite(v["delta"]))),
           "oof_base": ob.tolist(), "oof_cand": oc.tolist(), "concepts": d["concept"].tolist()}
    if refit_boot:
        rr = []
        for _ in range(refit_boot):
            idx = np.concatenate([rng.choice(np.where(d["group"].values == g)[0], (d["group"].values == g).sum())
                                  for g in GROUPS if (d["group"].values == g).sum()])
            dd = d.iloc[idx].reset_index(drop=True)
            a = stat(logo_predict(dd, base, y, kind), dd[y].values.astype(float))
            b = stat(logo_predict(dd, cand, y, kind), dd[y].values.astype(float))
            if np.isfinite(a) and np.isfinite(b):
                rr.append(b - a)
        rr = np.array(rr)
        out["refit_boot"] = {"n": int(len(rr)), "ci90": [float(np.percentile(rr, 5)), float(np.percentile(rr, 95))]
                             if len(rr) else [math.nan] * 2, "mean": float(rr.mean()) if len(rr) else math.nan}
    return out


def loco_delta(df: pd.DataFrame, base: list[str], cand: list[str], y: str) -> dict:
    """Supplementary leave-one-concept-out ridge Delta-rho."""
    d = df[np.isfinite(df[y].values.astype(float))].reset_index(drop=True)
    res = {}
    for nm, cols in (("base", base), ("cand", cand)):
        oof = np.full(len(d), np.nan)
        for i in range(len(d)):
            tr = np.ones(len(d), bool)
            tr[i] = False
            X = _prep(d[cols], tr)
            m = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X[tr], d.loc[tr, y].values)
            oof[i] = m.predict(X[~tr])[0]
        res[nm] = _sp(oof, d[y].values.astype(float))
    return {"base": res["base"], "cand": res["cand"], "delta": res["cand"] - res["base"], "n": len(d)}


# ------------------------------------------------------------------ meta-analysis
def dersimonian_laird(est: list[float], var: list[float]) -> dict:
    e = np.array(est, float)
    v = np.array(var, float)
    ok = np.isfinite(e) & np.isfinite(v) & (v > 0)
    e, v = e[ok], v[ok]
    k = len(e)
    if k < 2:
        return {"k": k, "pooled": float(e[0]) if k else math.nan, "se": math.nan, "tau2": math.nan, "I2": math.nan}
    w = 1 / v
    fe = (w * e).sum() / w.sum()
    Q = (w * (e - fe) ** 2).sum()
    C = w.sum() - (w ** 2).sum() / w.sum()
    tau2 = max(0.0, (Q - (k - 1)) / C) if C > 0 else 0.0
    ws = 1 / (v + tau2)
    re = (ws * e).sum() / ws.sum()
    se = math.sqrt(1 / ws.sum())
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
    return {"k": k, "pooled": float(re), "se": float(se), "tau2": float(tau2), "I2": float(I2), "Q": float(Q)}


def hanley_mcneil_var(auc: float, n1: int, n0: int) -> float:
    q1, q2 = auc / (2 - auc), 2 * auc ** 2 / (1 + auc)
    return (auc * (1 - auc) + (n1 - 1) * (q1 - auc ** 2) + (n0 - 1) * (q2 - auc ** 2)) / (n1 * n0)


def single_indicator(df: pd.DataFrame, feat: str, y: str, binary: bool) -> dict:
    d = df[np.isfinite(df[y].values.astype(float)) & np.isfinite(df[feat].values.astype(float))]
    x, Y = d[feat].values.astype(float), d[y].values.astype(float)
    res = {"feature": feat, "outcome": y, "n": len(d)}
    if not binary:
        res["pooled"] = _sp(x, Y)
        ests, vars_, per = [], [], {}
        for g in GROUPS:
            m = d["group"].values == g
            r = _sp(x[m], Y[m])
            per[g] = r
            if np.isfinite(r) and m.sum() > 3:
                ests.append(math.atanh(max(min(r, 0.999), -0.999)))
                vars_.append(1.06 / (m.sum() - 3))
        dl = dersimonian_laird(ests, vars_)
        res.update({"per_group": per, "meta_pooled": math.tanh(dl["pooled"]) if np.isfinite(dl["pooled"]) else math.nan,
                    "meta_ci95": [math.tanh(dl["pooled"] - 1.96 * dl["se"]), math.tanh(dl["pooled"] + 1.96 * dl["se"])]
                    if np.isfinite(dl["se"]) else [math.nan] * 2, "I2": dl["I2"], "k": dl["k"],
                    "sign_consistency": int(sum(1 for v in per.values() if np.isfinite(v) and np.sign(v) ==
                                                np.sign(res["pooled"])))})
    else:
        res["pooled_raw"] = _auc(Y, x)
        per_raw, per_or, ests, vars_ = {}, {}, [], []
        for g in GROUPS:
            m = d["group"].values == g
            a = _auc(Y[m], x[m])
            per_raw[g] = a
            atr = _auc(Y[~m], x[~m])  # orientation chosen on training groups only
            sgn = 1 if (not np.isfinite(atr) or atr >= 0.5) else -1
            ao = a if sgn == 1 else (1 - a if np.isfinite(a) else a)
            per_or[g] = ao
            n1, n0 = int(Y[m].sum()), int((1 - Y[m]).sum())
            if np.isfinite(ao) and n1 and n0:
                aa = min(max(ao, 0.01), 0.99)
                ests.append(math.log(aa / (1 - aa)))
                vars_.append(hanley_mcneil_var(aa, n1, n0) / (aa * (1 - aa)) ** 2)
        dl = dersimonian_laird(ests, vars_)
        inv = lambda z: 1 / (1 + math.exp(-z))
        res.update({"per_group_raw": per_raw, "per_group_oriented": per_or,
                    "meta_pooled_oriented": inv(dl["pooled"]) if np.isfinite(dl["pooled"]) else math.nan,
                    "meta_ci95": [inv(dl["pooled"] - 1.96 * dl["se"]), inv(dl["pooled"] + 1.96 * dl["se"])]
                    if np.isfinite(dl["se"]) else [math.nan] * 2, "I2": dl["I2"], "k": dl["k"],
                    "sign_consistency": int(sum(1 for v in per_or.values() if np.isfinite(v) and v > 0.5))})
    return res


# ------------------------------------------------------------------ field level
def field_level(fr: pd.DataFrame, base: list[str], cand: list[str], n_boot: int = 2000, seed: int = 1) -> dict:
    d = fr.dropna(subset=["R"]).reset_index(drop=True)
    ob = logo_predict(d, base, "R", "logit")
    oc = logo_predict(d, cand, "R", "logit")
    Y = d["R"].values.astype(float)
    ab, ac = _auc(Y, ob), _auc(Y, oc)
    rng = np.random.default_rng(seed)
    cons = d["concept"].unique()
    rows = {c: np.where(d["concept"].values == c)[0] for c in cons}
    boots = []
    for _ in range(n_boot):
        pick = rng.choice(cons, len(cons))
        i = np.concatenate([rows[c] for c in pick])
        a, b = _auc(Y[i], ob[i]), _auc(Y[i], oc[i])
        if np.isfinite(a) and np.isfinite(b):
            boots.append(b - a)
    boots = np.array(boots)
    per = {}
    for g in GROUPS:
        m = d["group"].values == g
        per[g] = {"n_rows": int(m.sum()), "base": _auc(Y[m], ob[m]), "cand": _auc(Y[m], oc[m])}
    return {"n_rows": len(d), "n_concepts": len(cons), "prevalence": float(Y.mean()), "auc_base": ab, "auc_cand": ac,
            "delta_auc": ac - ab, "ci90": [float(np.percentile(boots, 5)), float(np.percentile(boots, 95))],
            "ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))], "per_group": per}
