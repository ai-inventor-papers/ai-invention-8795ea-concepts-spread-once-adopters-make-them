"""Fast partial Spearman for bootstrap draws (same estimand as rq1stats.psp_point).

psp = Pearson(resid(rank x ~ 1 + rank B + C), resid(rank y ~ same)). The projection is computed from the normal
equations of the column-scaled design (ranks / n) solved by lstsq on the small p x p Gram matrix -- the projection is
unique even when the design is rank-deficient, so residuals equal those of rq1stats.psp_point up to rounding
(validated to <= 1e-9 in tests/u_fastpsp.py). Point estimates in every result use the ORIGINAL rq1stats.psp_point;
only bootstrap draws use this function. psp_boot2_fast consumes the RNG exactly like ladder.psp_boot2."""
from __future__ import annotations

import math

import numpy as np
from scipy import stats
from scipy.stats import rankdata

from rq1stats import psp_point


def psp_fast(x: np.ndarray, y: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
    n = len(x)
    cols = [np.ones((n, 1))]
    if B is not None and B.shape[1]:
        cols.append(rankdata(B, axis=0) / n)
    if C is not None and C.shape[1]:
        cols.append(C)
    Z = np.hstack(cols)
    Y = np.c_[rankdata(x), rankdata(y)] / n
    G = Z.T @ Z
    beta = np.linalg.lstsq(G, Z.T @ Y, rcond=1e-13)[0]
    R = Y - Z @ beta
    sx, sy = R[:, 0].std(), R[:, 1].std()
    if sx <= 1e-12 / n or sy <= 1e-12 / n:
        return float("nan")
    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])


def boot_indices(n: int, n_boot: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.stack([rng.integers(0, n, n) for _ in range(n_boot)]) if n_boot else np.zeros((0, n), np.int64)


def complete(x, y, B, C):
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
    return ok


def psp_boot2_fast(x, y, B, C, n_boot: int, seed: int, direction: int = 1, min_n: int = 30) -> dict:
    """== ladder.psp_boot2 (point by the original psp_point; draws by psp_fast with identical resample indices)."""
    ok = complete(x, y, B, C)
    x, y, B, C = x[ok], y[ok], B[ok], C[ok]
    n = len(x)
    if n < min_n or np.unique(x).size < 3:
        return {"n": int(n), "rho": math.nan, "ci": [math.nan, math.nan], "se": math.nan, "p_one": math.nan,
                "p_two": math.nan, "boot": np.array([])}
    est = psp_point(x, y, B, C)
    rng = np.random.default_rng(seed)
    bs = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0 if Ci.shape[1] else np.zeros(0, bool)
        bs[b] = psp_fast(x[i], y[i], B[i], Ci[:, keep])
    bs = bs[np.isfinite(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    p_one = float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1))
    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))
    se_z = float(np.std(z, ddof=1))
    ze = math.atanh(max(min(est, 0.999999), -0.999999))
    return {"n": int(n), "rho": float(est), "ci": [float(lo), float(hi)], "se": float(np.std(bs, ddof=1)),
            "se_z": se_z, "p_one": p_one,
            "p_two": float(2 * stats.norm.sf(abs(ze / se_z))) if se_z > 0 else math.nan, "boot": bs}


def paired_fast(xa, xb, y, B, C, n_boot: int, seed: int, min_n: int = 30) -> dict:
    """Paired concept bootstrap of psp(xa) and psp(xb) on the common sample: diff and ratio (xa / xb) with shared
    resample indices (== ladder.paired_diff resampling)."""
    ok = np.isfinite(xa) & np.isfinite(xb) & complete(xa, y, B, C)
    xa, xb, y, B, C = xa[ok], xb[ok], y[ok], B[ok], C[ok]
    n = len(y)
    if n < min_n or np.unique(xa).size < 3 or np.unique(xb).size < 3:
        return {"n": int(n), "a": math.nan, "b": math.nan, "diff": math.nan, "diff_ci": [math.nan] * 2,
                "ratio": math.nan, "ratio_ci": [math.nan] * 2}
    pa, pb = psp_point(xa, y, B, C), psp_point(xb, y, B, C)
    rng = np.random.default_rng(seed)
    A_, B_ = np.empty(n_boot), np.empty(n_boot)
    for k in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0
        A_[k] = psp_fast(xa[i], y[i], B[i], Ci[:, keep])
        B_[k] = psp_fast(xb[i], y[i], B[i], Ci[:, keep])
    f = np.isfinite(A_) & np.isfinite(B_)
    d = A_[f] - B_[f]
    with np.errstate(divide="ignore", invalid="ignore"):
        r = A_[f] / B_[f]
    return {"n": int(n), "a": float(pa), "b": float(pb), "diff": float(pa - pb),
            "diff_ci": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "ratio": float(pa / pb) if pb != 0 else math.nan,
            "ratio_ci": [float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))],
            "a_ci": [float(np.percentile(A_[f], 2.5)), float(np.percentile(A_[f], 97.5))],
            "b_ci": [float(np.percentile(B_[f], 2.5)), float(np.percentile(B_[f], 97.5))],
            "p_diff_le0": float((np.sum(d <= 0) + 1) / (len(d) + 1)), "resampling_unit": "concept"}
