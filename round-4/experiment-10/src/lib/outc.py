"""Concept outcomes from grounded yearly counts (EXP5 frame.concept_outcomes / EXP8 outcomes.py definitions).

N[y] grounded works (all venues), V[y, 27] grounded works by venue-field code (0 = unlabelled), G[y] base works
(all venues), all indexed by year - Y0. `shift` moves every post-onset window earlier by `shift` years (the 2017
extension and the <= 2022 TAG sensitivity use shift = 1: t0+5..t0+7 instead of t0+6..t0+8)."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import gammaln


def rarefied_richness(counts, m: int) -> float:
    """EXP5 frame.rarefied_richness (exact hypergeometric; verbatim)."""
    n = np.asarray([c for c in counts if c > 0], dtype=float)
    N = n.sum()
    if N < m:
        return math.nan
    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)  # noqa: E731
    out = 0.0
    for nj in n:
        if N - nj < m:
            out += 1.0
        else:
            out += 1.0 - math.exp(lc(N - nj, m) - lc(N, m))
    return out


def outcomes(N: np.ndarray, V: np.ndarray, G: np.ndarray, t0: int, Y0: int, shift: int = 0) -> dict:
    yi = lambda y: y - Y0  # noqa: E731
    a, b = 6 - shift, 8 - shift          # outcome window t0+a..t0+b
    sh = lambda y: N[yi(y)] / G[yi(y)]  # noqa: E731
    o1 = int(np.mean([sh(y) for y in range(t0 + a, t0 + b + 1)]) >= sh(t0 + a - 1))
    seq = [N[yi(y)] for y in range(t0, t0 + b + 1)]
    peak_y = t0 + int(np.argmax(seq))
    late = np.mean([N[yi(t0 + b - 1)], N[yi(t0 + b)]])
    o3 = int(t0 + 3 <= peak_y <= t0 + b and max(seq) / max(late, 1e-9) >= 2)
    counts = V[yi(t0 + a):yi(t0 + b) + 1, 1:27].sum(0)
    rc = [int(round(c)) for c in counts]
    early = N[yi(t0):yi(t0 + 2) + 1].sum()
    lateN = N[yi(t0 + a):yi(t0 + b) + 1].sum()
    return {"O1b": o1, "O3": o3, "peak_year": peak_y, "N_outcome": float(counts.sum()),
            "O2r_m50": rarefied_richness(rc, 50), "O2r_m30": rarefied_richness(rc, 30),
            "O1c": float(np.log1p(lateN) - np.log1p(early)), "N_late_all": float(lateN)}
