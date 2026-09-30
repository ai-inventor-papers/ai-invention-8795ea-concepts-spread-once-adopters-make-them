"""Stage 2: partial pooling of the concept x field contrasts rho_hat_cj.

Model: y_k = x_k beta + u_c(k) + w_k + e_k, u ~ N(0, tau_c^2), w ~ N(0, tau_cj^2), e ~ N(0, v_k) (v_k known from the
stage-1 child bootstrap). Engine: REML over (log tau_c, log tau_cj) (L-BFGS-B, 3 starts), then Henderson's
mixed-model equations for beta, BLUPs and the full prediction-error covariance. Fallback (F4): DerSimonian-Laird
one-level empirical Bayes. Headline check: the same model in PyMC (non-centred, NUTS).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from loguru import logger
from scipy.optimize import minimize


@dataclass
class PoolFit:
    beta: np.ndarray
    tau_c: float
    tau_cj: float
    u: np.ndarray            # (n_concepts,)
    w: np.ndarray            # (K,)
    Cinv: np.ndarray         # PEV of [beta, u, w]
    X: np.ndarray
    fields_x: list[str]      # column meaning of X (intercept + dummies)
    engine: str
    converged: bool


def design(field_of_k: list[str], min_cells: int = 5) -> tuple[np.ndarray, list[str]]:
    vals, cnt = np.unique(field_of_k, return_counts=True)
    keep = [v for v, n in zip(vals, cnt) if n >= min_cells]
    if len(keep) == len(vals) and keep:  # every field frequent: the most common one becomes the reference
        keep.remove(vals[np.argmax(cnt)])
    cols = ["intercept"] + keep
    X = np.zeros((len(field_of_k), len(cols)))
    X[:, 0] = 1
    for k, f in enumerate(field_of_k):
        if f in keep:
            X[k, cols.index(f)] = 1
    return X, cols


def x_row(field: str, cols: list[str]) -> np.ndarray:
    x = np.zeros(len(cols))
    x[0] = 1
    if field in cols[1:]:
        x[cols.index(field)] = 1
    return x


def _reml_nll(theta: np.ndarray, y: np.ndarray, X: np.ndarray, Zc: np.ndarray, v: np.ndarray) -> float:
    tc2, tcj2 = np.exp(2 * theta)
    S = tc2 * Zc @ Zc.T + np.diag(tcj2 + v)
    try:
        L = np.linalg.cholesky(S)
    except np.linalg.LinAlgError:
        return 1e10
    Si = np.linalg.inv(S)
    XtSiX = X.T @ Si @ X
    sgn, ld2 = np.linalg.slogdet(XtSiX)
    if sgn <= 0:
        return 1e10
    P = Si - Si @ X @ np.linalg.solve(XtSiX, X.T @ Si)
    return 0.5 * (2 * np.log(np.diag(L)).sum() + ld2 + y @ P @ y)


def mme(y: np.ndarray, X: np.ndarray, Zc: np.ndarray, v: np.ndarray, tc2: float, tcj2: float):
    K, p = X.shape
    nc = Zc.shape[1]
    Z = np.hstack([Zc, np.eye(K)])
    Ri = np.diag(1.0 / v)
    Gi = np.diag(np.r_[np.full(nc, 1 / max(tc2, 1e-6)), np.full(K, 1 / max(tcj2, 1e-6))])
    C = np.block([[X.T @ Ri @ X, X.T @ Ri @ Z], [Z.T @ Ri @ X, Z.T @ Ri @ Z + Gi]])
    rhs = np.r_[X.T @ Ri @ y, Z.T @ Ri @ y]
    Cinv = np.linalg.pinv(C)
    sol = Cinv @ rhs
    return sol[:p], sol[p:p + nc], sol[p + nc:], Cinv


def fit_reml(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str]) -> PoolFit:
    X, cols = design(fields)
    Zc = np.zeros((len(y), n_concepts))
    Zc[np.arange(len(y)), cidx] = 1
    best = None
    for start in ([np.log(0.3), np.log(0.3)], [np.log(1.0), np.log(0.1)], [np.log(0.1), np.log(1.0)]):
        r = minimize(_reml_nll, np.array(start), args=(y, X, Zc, v), method="L-BFGS-B",
                     bounds=[(np.log(1e-3), np.log(10))] * 2)
        if best is None or r.fun < best.fun:
            best = r
    tc, tcj = np.exp(best.x)
    boundary = min(tc, tcj) <= 1.01e-3
    if not best.success:
        logger.warning(f"REML not converged: {best.message}; using DerSimonian-Laird fallback")
        return fit_dl(y, v, cidx, n_concepts, fields)
    beta, u, w, Cinv = mme(y, X, Zc, v, tc ** 2, tcj ** 2)
    logger.info(f"REML: tau_c={tc:.3f} tau_cj={tcj:.3f} beta={np.round(beta, 3)} boundary={boundary}")
    return PoolFit(beta=beta, tau_c=float(tc), tau_cj=float(tcj), u=u, w=w, Cinv=Cinv, X=X, fields_x=cols,
                   engine="REML" + ("(tau at boundary)" if boundary else ""), converged=True)


def fit_dl(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str]) -> PoolFit:
    """F4 fallback: DerSimonian-Laird tau_c^2 (tau_cj^2 = 0) and one-level empirical-Bayes shrinkage."""
    X, cols = design(fields)
    w0 = 1 / v
    mu = (w0 * y).sum() / w0.sum()
    Q = (w0 * (y - mu) ** 2).sum()
    tau2 = max(0.0, (Q - (len(y) - 1)) / (w0.sum() - (w0 ** 2).sum() / w0.sum()))
    Zc = np.zeros((len(y), n_concepts))
    Zc[np.arange(len(y)), cidx] = 1
    beta, u, w, Cinv = mme(y, X, Zc, v, max(tau2, 1e-6), 1e-6)
    return PoolFit(beta=beta, tau_c=float(np.sqrt(tau2)), tau_cj=0.0, u=u, w=w, Cinv=Cinv, X=X, fields_x=cols,
                   engine="DerSimonian-Laird", converged=True)


def predict(fit: PoolFit, concept: int, field: str, k: int | None) -> tuple[float, np.ndarray]:
    """rho*_cj point prediction and its l-vector over [beta, u, w] (w part only when the unit has data)."""
    p = len(fit.beta)
    nc = len(fit.u)
    K = len(fit.w)
    l = np.zeros(p + nc + K)
    l[:p] = x_row(field, fit.fields_x)
    l[p + concept] = 1
    if k is not None:
        l[p + nc + k] = 1
    val = l[:p] @ fit.beta + fit.u[concept] + (fit.w[k] if k is not None else 0.0)
    return float(val), l


def var_of(fit: PoolFit, l: np.ndarray, extra: float = 0.0) -> float:
    return float(l @ fit.Cinv @ l + extra)


def fit_pymc(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str],
             draws: int = 1000, chains: int = 4, seed: int = 20260928):
    """Headline check: same crossed random-effects model, non-centred, NUTS. Returns (idata, X, cols)."""
    import pymc as pm
    X, cols = design(fields)
    with pm.Model() as m:
        beta = pm.Normal("beta", 0, 2, shape=X.shape[1])
        tau_c = pm.HalfNormal("tau_c", 1)
        tau_cj = pm.HalfNormal("tau_cj", 1)
        zc = pm.Normal("zc", 0, 1, shape=n_concepts)
        zk = pm.Normal("zk", 0, 1, shape=len(y))
        u = pm.Deterministic("u", tau_c * zc)
        w = pm.Deterministic("w", tau_cj * zk)
        mu = pm.math.dot(X, beta) + u[cidx] + w
        pm.Normal("y", mu, pm.math.sqrt(v), observed=y)
        try:
            idata = pm.sample(draws=draws, tune=1000, chains=chains, random_seed=seed, target_accept=0.95,
                              nuts_sampler="nutpie", progressbar=False)
        except (ImportError, ValueError, RuntimeError) as e:
            logger.warning(f"nutpie unavailable ({e!r:.100}); using the PyMC NUTS sampler")
            idata = pm.sample(draws=draws, tune=1000, chains=min(chains, 4), cores=min(chains, 4),
                              random_seed=seed, target_accept=0.95, progressbar=False)
    return idata, X, cols
