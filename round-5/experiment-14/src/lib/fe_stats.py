"""Panel statistics for the within-concept mechanism test.

  * demean2 / feols_np: fast OLS with several high-dimensional FE (sparse group means, alternating projections) and
    CRV1 concept-clustered SEs -- used inside bootstraps and as the independent code path of the event study.
  * ppml: pyfixest.fepois wrapper (concept + year FE, CRV1 by concept).
  * cluster_resample: concept-cluster bootstrap resample with duplicated concepts relabelled as new FE units.
  * sun_abraham: interaction-weighted event-study estimator (Sun & Abraham 2021) with never-treated or last-treated
    controls, implemented directly on top of feols_np.
  * roth_power_slope: the linear pre-trend slope the joint lead test detects with 80% power (Roth 2022 style).
  * within_sd: SD of a variable after sweeping out concept and year FE."""
from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy import stats


# ----------------------------------------------------------------------------- FE OLS
def _group_ops(groups: list[np.ndarray]) -> list[tuple[sp.csr_matrix, np.ndarray]]:
    ops = []
    for g in groups:
        _, inv = np.unique(g, return_inverse=True)
        n, G = len(inv), inv.max() + 1
        S = sp.csr_matrix((np.ones(n), (np.arange(n), inv)), shape=(n, G))
        ops.append((S, np.asarray(S.sum(0)).ravel()))
    return ops


def demean2(A: np.ndarray, groups: list[np.ndarray], iters: int = 500, tol: float = 1e-11) -> np.ndarray:
    A = np.asarray(A, float).copy()
    if A.ndim == 1:
        A = A[:, None]
    ops = _group_ops(groups)
    for _ in range(iters if len(ops) > 1 else 1):
        prev = A.copy()
        for S, cnt in ops:
            A -= S @ ((S.T @ A) / cnt[:, None])
        if len(ops) > 1 and np.abs(A - prev).max() < tol:
            break
    return A


def feols_np(y: np.ndarray, X: np.ndarray, fe: list[np.ndarray], cluster: np.ndarray, names: list[str],
             want_V: bool = False) -> dict:
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X, cluster = y[ok], X[ok], cluster[ok]
    fe = [g[ok] for g in fe]
    Z = demean2(np.column_stack([y, X]), fe)
    yd, Xd = Z[:, 0], Z[:, 1:]
    keep = np.abs(Xd).max(0) > 1e-10                       # drop columns swept out by the FE
    Xk = Xd[:, keep]
    XtXi = np.linalg.pinv(Xk.T @ Xk)
    bk = XtXi @ Xk.T @ yd
    e = yd - Xk @ bk
    _, cinv = np.unique(cluster, return_inverse=True)
    G = cinv.max() + 1
    sc = np.zeros((G, Xk.shape[1]))
    np.add.at(sc, cinv, Xk * e[:, None])
    n, k = Xk.shape
    corr = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)
    Vk = corr * XtXi @ (sc.T @ sc) @ XtXi
    b = np.full(X.shape[1], np.nan)
    se = np.full(X.shape[1], np.nan)
    b[keep] = bk
    se[keep] = np.sqrt(np.clip(np.diag(Vk), 0, None))
    out = {"n": int(n), "n_clusters": int(G), "b": dict(zip(names, b)), "se": dict(zip(names, se))}
    if want_V:
        V = np.full((X.shape[1], X.shape[1]), np.nan)
        idx = np.nonzero(keep)[0]
        V[np.ix_(idx, idx)] = Vk
        out["V"] = V
    return out


def within_sd(v: np.ndarray, ci: np.ndarray, year: np.ndarray) -> float:
    ok = np.isfinite(v)
    return float(np.std(demean2(v[ok], [ci[ok], year[ok]])[:, 0], ddof=1))


# ----------------------------------------------------------------------------- PPML (pyfixest)
def ppml(df: pd.DataFrame, y: str, xs: list[str], fe: str = "ci + year", vcov="CRV1", offset: str | None = None):
    import pyfixest as pf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fml = f"{y} ~ {' + '.join(xs)} | {fe}"
        kw = {"offset": offset} if offset else {}
        return pf.fepois(fml, data=df, vcov={"CRV1": "ci"} if vcov == "CRV1" else vcov, **kw)


def ppml_summary(fit, x: str) -> dict:
    co, se = float(fit.coef()[x]), float(fit.se()[x])
    ci = fit.confint().loc[x].to_numpy(float)
    return {"b": co, "se": se, "ci": [float(ci[0]), float(ci[1])], "p": float(fit.pvalue()[x]), "n": int(fit._N),
            "n_concepts": int(fit._data["ci"].nunique()) if hasattr(fit, "_data") else None}


def feols_pf(df: pd.DataFrame, y: str, xs: list[str], fe: str = "ci + year"):
    import pyfixest as pf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return pf.feols(f"{y} ~ {' + '.join(xs)} | {fe}", data=df, vcov={"CRV1": "ci"})


# ----------------------------------------------------------------------------- bootstrap
def cluster_index(ci: np.ndarray) -> list[np.ndarray]:
    order = np.argsort(ci, kind="stable")
    u, start = np.unique(ci[order], return_index=True)
    return np.split(order, start[1:])


def cluster_resample(df: pd.DataFrame, idx: list[np.ndarray], rng: np.random.Generator) -> pd.DataFrame:
    pick = rng.integers(0, len(idx), len(idx))
    rows = np.concatenate([idx[p] for p in pick])
    newid = np.concatenate([np.full(len(idx[p]), j) for j, p in enumerate(pick)])
    d = df.iloc[rows].copy()
    d["ci_orig"] = d["ci"].to_numpy()
    d["ci"] = newid
    return d


# ----------------------------------------------------------------------------- Sun & Abraham
def sa_design(df: pd.DataFrame, g_col: str, leads: int = 3, lags: int = 4, control: str = "never"
              ) -> tuple[pd.DataFrame, list[str], dict]:
    """Fully saturated cohort x relative-time dummies (e = -1 omitted); only -leads..lags are reported.
    control='never': never-treated concepts (g NaN) are the control group.
    control='last': never-treated dropped, the last-treated cohort is the control, rows at t >= g_last dropped."""
    d = df.copy()
    if control == "last":
        d = d[d[g_col].notna()]
        g_last = d[g_col].max()
        d = d[d.year < g_last]
        d.loc[d[g_col] == g_last, g_col] = np.nan
    e = d.year - d[g_col]
    rel = [k for k in range(-leads, lags + 1) if k != -1]
    cols, meta = [], {}
    for g in sorted(d[g_col].dropna().unique()):
        isg = (d[g_col] == g).to_numpy()
        for k in rel:
            m = isg & (e == k).to_numpy()
            if m.sum() == 0:
                continue
            c = f"D_{int(g)}_{'m' if k < 0 else 'p'}{abs(k)}"
            d[c] = m.astype(float)
            cols.append(c)
            meta[c] = (int(g), k, int(m.sum()))
        # relative times outside the reported window get their OWN cohort-specific dummies (full saturation):
        # binning them into one dummy per side forces a constant effect and biases the reported lags
        eg = e[isg].dropna().astype(int).unique()
        for k in sorted(int(x) for x in eg if (x < -leads or x > lags)):
            m = isg & (e == k).to_numpy()
            c = f"O_{int(g)}_{'m' if k < 0 else 'p'}{abs(k)}"
            d[c] = m.astype(float)
            cols.append(c)
            meta[c] = (int(g), "out", int(m.sum()))
    return d, cols, meta


def sa_aggregate(b: dict, meta: dict, leads: int = 3, lags: int = 4) -> dict[int, float]:
    """IW: ATT(e) = sum_g w_{g,e} CATT(g,e), w = cohort share of treated rows at e (among cohorts with a finite CATT)."""
    out = {}
    for k in [k for k in range(-leads, lags + 1) if k != -1]:
        num = den = 0.0
        for c, (g, kk, n) in meta.items():
            if kk == k and np.isfinite(b.get(c, np.nan)):
                num += n * b[c]
                den += n
        out[k] = num / den if den > 0 else float("nan")
    return out


def sun_abraham(df: pd.DataFrame, y: str, controls: list[str], g_col: str = "g", control: str = "never",
                leads: int = 3, lags: int = 4) -> dict:
    d, cols, meta = sa_design(df, g_col, leads, lags, control)
    X = d[cols + controls].to_numpy(float)
    r = feols_np(d[y].to_numpy(float), X, [d.ci.to_numpy(), d.year.to_numpy()], d.ci.to_numpy(), cols + controls)
    att = sa_aggregate(r["b"], meta, leads, lags)
    lag_mean = float(np.nanmean([att[k] for k in (0, 1, 2)]))
    return {"att": att, "mean_lag_0_2": lag_mean, "n": r["n"], "n_concepts": r["n_clusters"],
            "n_treated": int(d.loc[d[g_col].notna(), "ci"].nunique()), "n_cells": len(cols), "b": r["b"],
            "meta": meta}


def roth_power_slope(V_leads: np.ndarray, rel: list[int], alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest slope delta of a linear pre-trend beta_e = delta * (e + 1) that the joint Wald test on the leads
    rejects with probability `power`."""
    v = np.array([k + 1 for k in rel], float)
    Vi = np.linalg.pinv(V_leads)
    q = float(v @ Vi @ v)
    df_ = len(rel)
    crit = stats.chi2.ppf(1 - alpha, df_)
    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        if stats.ncx2.sf(crit, df_, mid) < power:
            lo = mid
        else:
            hi = mid
    return float(np.sqrt(hi / q)) if q > 0 else float("nan")


def wald(b: np.ndarray, V: np.ndarray) -> tuple[float, float]:
    W = float(b @ np.linalg.pinv(V) @ b)
    return W, float(stats.chi2.sf(W, len(b)))
