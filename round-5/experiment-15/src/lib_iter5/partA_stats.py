"""Part A statistics: a vectorised partial Spearman that reproduces EXP8 rq1stats.psp_point column by column, with the
SAME concept-bootstrap indices for every component (paired differences are valid), exact Shapley values of a psp game,
DerSimonian-Laird on Fisher z, Holm.

psp(x, y | B, cat) = Pearson(resid(rank x ~ 1 + rank B + cat), resid(rank y ~ same)) on the rows where x, y and B are
finite; ranks (average ties) are recomputed inside every resample, exactly as psp_point does."""
from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.stats import rankdata

from rq1stats import dersimonian_laird, holm, psp_point  # noqa: F401  (re-exported)


def _psp_block(X: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> np.ndarray:
    Zc = [np.ones((len(y), 1))]
    if B is not None and B.shape[1]:
        Zc.append(rankdata(B, axis=0))
    if cat is not None and cat.shape[1]:
        Zc.append(cat)
    Z = np.hstack(Zc)
    Y = np.c_[rankdata(X, axis=0), rankdata(y)]
    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)
    R = Y - Z @ beta
    Rx, Ry = R[:, :-1], R[:, -1]
    sx, sy = Rx.std(0), Ry.std()
    Rxc, Ryc = Rx - Rx.mean(0), Ry - Ry.mean()
    with np.errstate(invalid="ignore", divide="ignore"):
        r = (Rxc * Ryc[:, None]).mean(0) / (sx * sy)
    r[(sx <= 1e-12) | (sy <= 1e-12)] = np.nan
    # a constant column has rank residuals that are pure lstsq round-off (ranks ~ n/2): psp undefined
    r[np.ptp(X, axis=0) == 0] = np.nan
    if np.ptp(y) == 0:
        r[:] = np.nan
    return r


class Scorer:
    """All columns of X against one outcome y given B (+cat), point and bootstrap, shared resample indices."""

    def __init__(self, X: np.ndarray, names: list[str], y: np.ndarray, B: np.ndarray, cat: np.ndarray | None,
                 min_n: int = 30):
        self.names = list(names)
        base = np.isfinite(y) & np.all(np.isfinite(B), 1)
        if cat is not None and cat.shape[1]:
            base &= np.all(np.isfinite(cat), 1)
        self.base_idx = np.nonzero(base)[0]
        self.X, self.y, self.B, self.cat = X, y, B, cat
        fin = np.isfinite(X) & base[:, None]
        groups: dict[bytes, list[int]] = {}
        for j in range(X.shape[1]):
            groups.setdefault(np.packbits(fin[:, j]).tobytes(), []).append(j)
        self.groups = [(fin[:, cols[0]], np.array(cols)) for cols in groups.values()]
        self.min_n = min_n
        self.n = {names[j]: int(fin[:, j].sum()) for j in range(X.shape[1])}

    def eval(self, idx: np.ndarray | None = None) -> np.ndarray:
        """psp of every column on the rows idx (a resample of base_idx; None = the observed sample)."""
        idx = self.base_idx if idx is None else idx
        out = np.full(self.X.shape[1], np.nan)
        for m, cols in self.groups:
            j = idx[m[idx]]
            if len(j) < self.min_n:
                continue
            Xj = self.X[np.ix_(j, cols)]
            cat = self.cat[j] if self.cat is not None and self.cat.shape[1] else None
            out[cols] = _psp_block(Xj, self.y[j], self.B[j], cat)
        return out

    def boot(self, n_boot: int, seed: int) -> np.ndarray:
        rng = np.random.default_rng(seed)
        nb = len(self.base_idx)
        return np.vstack([self.eval(self.base_idx[rng.integers(0, nb, nb)]) for _ in range(n_boot)])


def summarize(point: float, bs: np.ndarray) -> dict:
    v = bs[np.isfinite(bs)]
    if not np.isfinite(point) or len(v) < 10:
        return {"rho": point if np.isfinite(point) else None, "ci": None, "se": None, "z": None, "se_z": None,
                "p_two": None, "n_boot_ok": int(len(v))}
    z = np.arctanh(np.clip(v, -0.999999, 0.999999))
    se_z = float(np.std(z, ddof=1))
    ze = math.atanh(max(min(point, 0.999999), -0.999999))
    return {"rho": float(point), "ci": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))],
            "se": float(np.std(v, ddof=1)), "z": ze, "se_z": se_z,
            "p_two": float(min(1.0, 2 * min((v <= 0).mean(), (v >= 0).mean()) + 1 / len(v))),
            "n_boot_ok": int(len(v))}


def summarize_diff(pa: float, pb: float, ba: np.ndarray, bb: np.ndarray) -> dict:
    d = ba - bb
    d = d[np.isfinite(d)]
    est = pa - pb
    if not np.isfinite(est) or len(d) < 10:
        return {"diff": est if np.isfinite(est) else None, "ci": None, "se": None, "p_two": None}
    return {"diff": float(est), "ci": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "se": float(np.std(d, ddof=1)),
            "p_two": float(min(1.0, 2 * min((d <= 0).mean(), (d >= 0).mean()) + 1 / len(d))), "n_boot_ok": int(len(d))}


# ----------------------------------------------------------------------------- Shapley
def subsets(players: list[str]) -> list[frozenset]:
    return [frozenset(c) for r in range(len(players) + 1) for c in itertools.combinations(players, r)]


def shapley(players: list[str], v: dict[frozenset, float]) -> dict[str, float]:
    """Exact Shapley value: phi_i = sum_S |S|!(n-|S|-1)!/n! (v(S+i) - v(S))."""
    n = len(players)
    phi = {}
    for p in players:
        others = [q for q in players if q != p]
        s = 0.0
        for r in range(n):
            w = math.factorial(r) * math.factorial(n - r - 1) / math.factorial(n)
            for c in itertools.combinations(others, r):
                S = frozenset(c)
                s += w * (v[S | {p}] - v[S])
        phi[p] = s
    return phi


def dl_fisher(rhos: list, se_zs: list) -> dict:
    z = [math.atanh(max(min(r, 0.999999), -0.999999)) if r is not None and np.isfinite(r) else np.nan for r in rhos]
    pl = dersimonian_laird(np.array(z, float), np.array([s if s is not None else np.nan for s in se_zs], float))
    if not np.isfinite(pl["b"]):
        return {"psp": None, "ci": None, "I2": None, "k": pl["k"]}
    return {"psp": float(np.tanh(pl["b"])), "ci": [float(np.tanh(pl["ci"][0])), float(np.tanh(pl["ci"][1]))],
            "p": pl["p"], "I2": pl["I2"], "tau2": pl["tau2"], "k": pl["k"]}
