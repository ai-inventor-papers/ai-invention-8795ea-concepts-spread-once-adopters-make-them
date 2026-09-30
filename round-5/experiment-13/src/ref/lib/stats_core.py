"""Estimators: vectorised conditional logit (Breslow form for multiple events per stratum), within-FE OLS with
cluster-robust (CRV1) SEs, Poisson with concept FE, DerSimonian-Laird random-effects pooling, sign test."""
from __future__ import annotations

import math

import numpy as np
from scipy import optimize, stats


class CLogit:
    """Each event row e in stratum s contributes x_e.b - log sum_{i in s} exp(x_i.b).
    Rows must be sorted by stratum; `starts` are the first row index of each stratum."""

    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, ridge: float = 0.0):
        o = np.argsort(strata, kind="stable")
        self.X, self.y, self.s = X[o].astype(float), y[o].astype(float), strata[o]
        self.order = o
        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)
        self.nev = np.add.reduceat(self.y, self.starts)
        keep_s = (self.nev > 0) & (self.nev < self.counts)  # informative strata only
        rows = np.repeat(keep_s, self.counts)
        self.X, self.y, self.s = self.X[rows], self.y[rows], self.s[rows]
        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)
        self.nev = np.add.reduceat(self.y, self.starts)
        self.ridge = ridge

    def nll(self, b: np.ndarray) -> tuple[float, np.ndarray]:
        eta = self.X @ b
        m = np.maximum.reduceat(eta, self.starts)
        mm = np.repeat(m, self.counts)
        w = np.exp(eta - mm)
        S = np.add.reduceat(w, self.starts)
        lse = np.log(S) + m
        ll = float((self.y * eta).sum() - (self.nev * lse).sum())
        p = w / np.repeat(S, self.counts)
        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)  # per stratum expectation
        g = (self.y[:, None] * self.X).sum(0) - (self.nev[:, None] * Ex).sum(0)
        ll -= 0.5 * self.ridge * float(b @ b)
        g = g - self.ridge * b
        return -ll, -g

    def hessian(self, b: np.ndarray) -> np.ndarray:
        eta = self.X @ b
        m = np.maximum.reduceat(eta, self.starts)
        w = np.exp(eta - np.repeat(m, self.counts))
        S = np.add.reduceat(w, self.starts)
        p = w / np.repeat(S, self.counts)
        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)
        Exx = np.add.reduceat(p[:, None, None] * (self.X[:, :, None] * self.X[:, None, :]), self.starts)
        cov = Exx - Ex[:, :, None] * Ex[:, None, :]
        return (self.nev[:, None, None] * cov).sum(0) + self.ridge * np.eye(len(b))

    def fit(self) -> dict:
        k = self.X.shape[1]
        if len(self.starts) == 0:
            return {"coef": np.full(k, np.nan), "se": np.full(k, np.nan), "ll": np.nan, "n_strata": 0, "converged": False}
        r = optimize.minimize(self.nll, np.zeros(k), jac=True, method="L-BFGS-B", options={"maxiter": 500, "gtol": 1e-8})
        H = self.hessian(r.x)
        try:
            se = np.sqrt(np.diag(np.linalg.inv(H)))
        except np.linalg.LinAlgError:
            se = np.full(k, np.nan)
        return {"coef": r.x, "se": se, "ll": -r.fun, "n_strata": int(len(self.starts)), "n_events": int(self.y.sum()),
                "n_rows": int(len(self.y)), "converged": bool(r.success)}


def ll_null_clogit(y: np.ndarray, strata: np.ndarray) -> float:
    """log-likelihood at b = 0 on informative strata."""
    _, inv, cnt = np.unique(strata, return_inverse=True, return_counts=True)
    nev = np.bincount(inv, weights=y)
    keep = (nev > 0) & (nev < cnt)
    return float(-(nev[keep] * np.log(cnt[keep])).sum())


def demean(A: np.ndarray, groups: list[np.ndarray], iters: int = 50, tol: float = 1e-10) -> np.ndarray:
    """Alternating projections to sweep out several sets of fixed effects."""
    A = A.astype(float).copy()
    if A.ndim == 1:
        A = A[:, None]
    for _ in range(iters if len(groups) > 1 else 1):
        prev = A.copy()
        for g in groups:
            _, inv = np.unique(g, return_inverse=True)
            cnt = np.bincount(inv)
            for j in range(A.shape[1]):
                A[:, j] -= (np.bincount(inv, weights=A[:, j]) / cnt)[inv]
        if len(groups) > 1 and np.abs(A - prev).max() < tol:
            break
    return A


def fe_ols(y: np.ndarray, X: np.ndarray, fe: list[np.ndarray], cluster: np.ndarray, names: list[str]) -> dict:
    """OLS of y on X after sweeping out fixed effects `fe`; CRV1 SEs clustered on `cluster` (small-sample corrected)."""
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X, cluster = y[ok], X[ok], cluster[ok]
    fe = [g[ok] for g in fe]
    Z = demean(np.column_stack([y, X]), fe) if fe else np.column_stack([y - y.mean(), X - X.mean(0)])
    yd, Xd = Z[:, 0], Z[:, 1:]
    XtX = Xd.T @ Xd
    try:
        XtXi = np.linalg.pinv(XtX)
    except np.linalg.LinAlgError:
        return {"error": "singular"}
    b = XtXi @ Xd.T @ yd
    e = yd - Xd @ b
    _, cinv = np.unique(cluster, return_inverse=True)
    G = cinv.max() + 1
    sc = np.zeros((G, Xd.shape[1]))
    np.add.at(sc, cinv, Xd * e[:, None])
    n, k = Xd.shape
    corr = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)
    V = corr * XtXi @ (sc.T @ sc) @ XtXi
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    tcrit = stats.t.ppf(0.975, max(G - 1, 1))
    out = {"n": int(n), "n_clusters": int(G), "coef": {}, "V": V.tolist()}
    for i, nm in enumerate(names):
        out["coef"][nm] = {"b": float(b[i]), "se": float(se[i]), "ci": [float(b[i] - tcrit * se[i]), float(b[i] + tcrit * se[i])],
                           "p": float(2 * stats.t.sf(abs(b[i] / se[i]), max(G - 1, 1))) if se[i] > 0 else float("nan")}
    out["_b"] = b
    return out


def fe_poisson(y: np.ndarray, X: np.ndarray, group: np.ndarray, names: list[str], offset: np.ndarray | None = None,
               iters: int = 100) -> dict:
    """Poisson with group fixed effects (concentrated out: exp(alpha_g) = sum y / sum exp(xb+off) within g),
    Newton on b; CRV1 sandwich SEs clustered by group."""
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X, group = y[ok].astype(float), X[ok].astype(float), group[ok]
    off = np.zeros(len(y)) if offset is None else offset[ok]
    _, gi = np.unique(group, return_inverse=True)
    sy = np.bincount(gi, weights=y)
    keep = sy[gi] > 0  # groups with all-zero outcomes carry no information
    y, X, off, gi = y[keep], X[keep], off[keep], gi[keep]
    _, gi = np.unique(gi, return_inverse=True)
    sy = np.bincount(gi, weights=y)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        eta = X @ b + off
        w = np.exp(eta - eta.max())
        sw = np.bincount(gi, weights=w)
        mu = w * (sy / sw)[gi]
        # concentrated score / hessian: X demeaned by mu-weighted group means
        xm = np.column_stack([np.bincount(gi, weights=mu * X[:, j]) / np.bincount(gi, weights=mu) for j in range(X.shape[1])])[gi]
        Xc = X - xm
        g = Xc.T @ (y - mu)
        H = (Xc * mu[:, None]).T @ Xc
        step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), g)
        b = b + step
        if np.abs(step).max() < 1e-9:
            break
    Hi = np.linalg.pinv(H)
    sc = np.zeros((gi.max() + 1, X.shape[1]))
    np.add.at(sc, gi, Xc * (y - mu)[:, None])
    G = gi.max() + 1
    V = G / max(G - 1, 1) * Hi @ (sc.T @ sc) @ Hi
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    out = {"n": int(len(y)), "n_clusters": int(G), "coef": {}}
    for i, nm in enumerate(names):
        out["coef"][nm] = {"b": float(b[i]), "se": float(se[i]), "ci": [float(b[i] - 1.96 * se[i]), float(b[i] + 1.96 * se[i])],
                           "p": float(2 * stats.norm.sf(abs(b[i] / se[i]))) if se[i] > 0 else float("nan")}
    return out


def dersimonian_laird(b: np.ndarray, se: np.ndarray) -> dict:
    b, se = np.asarray(b, float), np.asarray(se, float)
    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)
    b, se = b[ok], se[ok]
    k = len(b)
    if k == 0:
        return {"k": 0}
    w = 1 / se**2
    bf = (w * b).sum() / w.sum()
    Q = float((w * (b - bf) ** 2).sum())
    C = w.sum() - (w**2).sum() / w.sum()
    tau2 = max(0.0, (Q - (k - 1)) / C) if k > 1 and C > 0 else 0.0
    ws = 1 / (se**2 + tau2)
    bre = (ws * b).sum() / ws.sum()
    sre = math.sqrt(1 / ws.sum())
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0
    return {"k": k, "b": float(bre), "se": sre, "ci": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],
            "p": float(2 * stats.norm.sf(abs(bre / sre))), "tau2": float(tau2), "Q": Q, "I2": float(I2)}


def sign_test(k_pos: int, n: int) -> float:
    """one-sided binomial P(X >= k_pos | p = 0.5)."""
    return float(stats.binom.sf(k_pos - 1, n, 0.5)) if n > 0 else float("nan")
