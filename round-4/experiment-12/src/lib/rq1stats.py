"""Statistics for RQ1: partial Spearman given a baseline (rank residualisation, refitted in every bootstrap
resample), L2-logistic delta-AUC (leave-one-group-out, out-of-fold), DerSimonian-Laird pooling, Holm, sign tests."""
from __future__ import annotations

import math

import numpy as np
from scipy import stats
from scipy.stats import rankdata


# ----------------------------------------------------------------------------- partial Spearman
def dummies(v: np.ndarray, drop_first: bool = True) -> np.ndarray:
    u = np.unique(v)
    if len(u) <= 1:
        return np.zeros((len(v), 0))
    cols = u[1:] if drop_first else u
    return (v[:, None] == cols[None, :]).astype(float)


def _resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:
    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    return Y - Z @ beta


def psp_point(x: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> float:
    """Pearson(resid(rank x ~ rank B + cat dummies), resid(rank y ~ same)). Rows must be complete."""
    Zc = [np.ones((len(x), 1))]
    if B is not None and B.shape[1]:
        Zc.append(rankdata(B, axis=0))
    if cat is not None and cat.shape[1]:
        Zc.append(cat)
    Z = np.hstack(Zc)
    R = _resid(Z, np.c_[rankdata(x), rankdata(y)])
    sx, sy = R[:, 0].std(), R[:, 1].std()
    if sx <= 1e-12 or sy <= 1e-12:
        return float("nan")
    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])


def psp_boot(x, y, B, cat, n_boot: int, seed: int) -> dict:
    """Point + concept bootstrap (resample rows; ranks and residualisation recomputed in each resample)."""
    ok = np.isfinite(x) & np.isfinite(y)
    if B is not None:
        ok &= np.all(np.isfinite(B), axis=1)
    x, y = x[ok], y[ok]
    Bs = B[ok] if B is not None else None
    cs = cat[ok] if cat is not None else None
    n = len(x)
    if n < 20 or np.unique(x).size < 3:
        return {"n": int(n), "rho": float("nan"), "ci": [float("nan")] * 2, "se": float("nan"), "p": float("nan"),
                "boot": np.array([])}
    est = psp_point(x, y, Bs, cs)
    rng = np.random.default_rng(seed)
    bs = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        bs[b] = psp_point(x[i], y[i], Bs[i] if Bs is not None else None, cs[i] if cs is not None else None)
    bs = bs[np.isfinite(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5]) if len(bs) else (np.nan, np.nan)
    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))
    se_z = float(np.std(z, ddof=1)) if len(z) > 2 else float("nan")
    ze = math.atanh(max(min(est, 0.999999), -0.999999)) if np.isfinite(est) else float("nan")
    p = float(2 * stats.norm.sf(abs(ze / se_z))) if se_z and np.isfinite(se_z) and se_z > 0 else float("nan")
    return {"n": int(n), "rho": est, "ci": [float(lo), float(hi)], "se": float(np.std(bs, ddof=1)),
            "z": ze, "se_z": se_z, "p": p, "boot": bs}


def spearman_raw(x, y) -> tuple[float, int]:
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 10 or np.unique(x[ok]).size < 3:
        return float("nan"), int(ok.sum())
    return float(stats.spearmanr(x[ok], y[ok])[0]), int(ok.sum())


# ----------------------------------------------------------------------------- L2 logistic (sklearn C=1 objective)
def logit_fit(X: np.ndarray, y: np.ndarray, lam: float = 1.0, iters: int = 50) -> np.ndarray:
    """Newton-IRLS for  sum log-loss + lam/2 ||w||^2 (intercept unpenalised). X excludes the intercept."""
    n, d = X.shape
    A = np.c_[np.ones(n), X]
    w = np.zeros(d + 1)
    pen = np.full(d + 1, lam)
    pen[0] = 0.0
    for _ in range(iters):
        eta = A @ w
        p = 1 / (1 + np.exp(-np.clip(eta, -30, 30)))
        g = A.T @ (p - y) + pen * w
        W = p * (1 - p)
        H = (A * W[:, None]).T @ A + np.diag(pen)
        try:
            step = np.linalg.solve(H, g)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, g, rcond=None)[0]
        w -= step
        if np.max(np.abs(step)) < 1e-8:
            break
    return w


def logit_pred(w: np.ndarray, X: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-np.clip(w[0] + X @ w[1:], -30, 30)))


def auc(y: np.ndarray, s: np.ndarray) -> float:
    y = np.asarray(y).astype(bool)
    n1, n0 = y.sum(), (~y).sum()
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def _std_fit(X):
    mu = X.mean(0)
    sd = X.std(0)
    sd[sd < 1e-12] = 1.0
    return mu, sd


def logo_oof(X: np.ndarray, y: np.ndarray, grp: np.ndarray) -> np.ndarray:
    """Out-of-fold predictions, leave-one-group-out, standardisation fitted on the training folds."""
    pred = np.full(len(y), np.nan)
    for g in np.unique(grp):
        te = grp == g
        tr = ~te
        if y[tr].min() == y[tr].max():
            continue
        mu, sd = _std_fit(X[tr])
        w = logit_fit((X[tr] - mu) / sd, y[tr])
        pred[te] = logit_pred(w, (X[te] - mu) / sd)
    return pred


def dauc_logo(Xb: np.ndarray, x: np.ndarray, y: np.ndarray, grp: np.ndarray) -> tuple[float, float, float]:
    p0 = logo_oof(Xb, y, grp)
    p1 = logo_oof(np.c_[Xb, x], y, grp)
    ok = np.isfinite(p0) & np.isfinite(p1)
    a0, a1 = auc(y[ok], p0[ok]), auc(y[ok], p1[ok])
    return a1 - a0, a0, a1


def dauc_boot(Xb, x, y, grp, n_boot: int, seed: int) -> dict:
    ok = np.all(np.isfinite(Xb), 1) & np.isfinite(x) & np.isfinite(y)
    Xb, x, y, grp = Xb[ok], x[ok], y[ok].astype(float), grp[ok]
    n = len(y)
    if n < 50 or y.sum() < 10 or (n - y.sum()) < 10 or np.unique(x).size < 3:
        return {"n": int(n), "dauc": float("nan"), "ci": [float("nan")] * 2, "p": float("nan"), "boot": np.array([])}
    est, a0, a1 = dauc_logo(Xb, x, y, grp)
    rng = np.random.default_rng(seed)
    idx_by = {g: np.nonzero(grp == g)[0] for g in np.unique(grp)}
    bs = []
    for _ in range(n_boot):
        i = np.concatenate([rng.choice(v, len(v)) for v in idx_by.values()])
        bs.append(dauc_logo(Xb[i], x[i], y[i], grp[i])[0])
    bs = np.array([b for b in bs if np.isfinite(b)])
    se = float(np.std(bs, ddof=1)) if len(bs) > 2 else float("nan")
    return {"n": int(n), "n_pos": int(y.sum()), "dauc": est, "auc_base": a0, "auc_full": a1,
            "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) else [np.nan] * 2,
            "se": se, "p": float(2 * stats.norm.sf(abs(est / se))) if se and se > 0 else float("nan"), "boot": bs}


# ----------------------------------------------------------------------------- pooling / multiplicity
def dersimonian_laird(b, se) -> dict:
    """EXP6 lib/stats_core.dersimonian_laird (verbatim logic)."""
    b, se = np.asarray(b, float), np.asarray(se, float)
    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)
    b, se = b[ok], se[ok]
    k = len(b)
    if k == 0:
        return {"k": 0, "b": float("nan"), "se": float("nan"), "ci": [float("nan")] * 2, "p": float("nan"),
                "tau2": float("nan"), "I2": float("nan"), "Q": float("nan")}
    w = 1 / se**2
    bf = (w * b).sum() / w.sum()
    Q = float((w * (b - bf) ** 2).sum())
    Cc = w.sum() - (w**2).sum() / w.sum()
    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 and Cc > 0 else 0.0
    ws = 1 / (se**2 + tau2)
    bre = (ws * b).sum() / ws.sum()
    sre = math.sqrt(1 / ws.sum())
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0
    return {"k": k, "b": float(bre), "se": sre, "ci": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],
            "p": float(2 * stats.norm.sf(abs(bre / sre))), "tau2": float(tau2), "Q": Q, "I2": float(I2)}


def holm(p: list[float]) -> list[float]:
    p = np.asarray(p, float)
    out = np.full(len(p), np.nan)
    ok = np.isfinite(p)
    idx = np.nonzero(ok)[0]
    m = len(idx)
    order = idx[np.argsort(p[idx])]
    run = 0.0
    for r, i in enumerate(order):
        run = max(run, min(1.0, (m - r) * p[i]))
        out[i] = run
    return out.tolist()


def sign_test_two_sided(k_pos: int, n: int) -> float:
    return float(stats.binomtest(k_pos, n, 0.5).pvalue) if n > 0 else float("nan")
