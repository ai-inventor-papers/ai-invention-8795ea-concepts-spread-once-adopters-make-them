"""S1/S0 primitives copied from iteration 1 (gen_art_experiment_4 features.py / s0_ground.py / s0_labels.py),
adapted to integer field ids and numpy yearly arrays."""
from __future__ import annotations

import math

import numpy as np
from scipy.special import gammaln


def rarefied_richness(counts, m: int) -> float:
    """Exact hypergeometric rarefaction E[S_m] = sum_j 1 - C(N-n_j, m)/C(N, m)  (verbatim logic)."""
    n = np.asarray([c for c in counts if c > 0], dtype=float)
    N = n.sum()
    if N < m:
        return math.nan
    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)  # noqa: E731
    out = 0.0
    for nj in n:
        out += 1.0 if N - nj < m else 1.0 - math.exp(lc(N - nj, m) - lc(N, m))
    return out


def shannon(v) -> float:
    v = np.asarray([x for x in v if x > 0], dtype=float)
    if v.sum() == 0:
        return math.nan
    p = v / v.sum()
    return float(-(p * np.log(p)).sum())


def onset(yc: dict[int, float]) -> tuple[float, bool | None]:
    """t0 = first year 2000..2014 with >= 20 works; newborn = each of t0-3..t0-1 < 0.25 * n(t0+2)."""
    ts = [y for y in range(2000, 2015) if yc.get(y, 0) >= 20]
    if not ts:
        return math.nan, None
    t0 = ts[0]
    newborn = all(yc.get(t0 - k, 0) < 0.25 * yc.get(t0 + 2, 0) for k in (1, 2, 3))
    return float(t0), newborn


def home_of(fc: dict[int, float]) -> tuple[list[int], bool]:
    """home = fields with >= 40% share, else the top field (flagged weak)."""
    tot = sum(fc.values())
    if not tot:
        return [], True
    h = [f for f, n in fc.items() if n / tot >= 0.40]
    if h:
        return sorted(h, key=lambda f: -fc[f]), False
    return [max(fc, key=fc.get)], True


def outcomes(yc: dict, gtot: dict, t0: int, fcD) -> dict:
    """O1 sustained share uptake, O3 transience, O2r rarefied venue-field richness in t0+6..t0+8 (verbatim logic)."""
    sh = lambda y: yc.get(y, 0) / gtot[y]  # noqa: E731
    o1 = int(np.mean([sh(y) for y in range(t0 + 6, t0 + 9)]) >= sh(t0 + 5))
    seq = [yc.get(y, 0) for y in range(t0, t0 + 9)]
    peak_y = t0 + int(np.argmax(seq))
    late = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])
    o3 = int(t0 + 3 <= peak_y <= t0 + 8 and max(seq) / max(late, 1e-9) >= 2)
    counts = [int(round(x)) for x in fcD]
    N = int(sum(counts))
    return {"O1": o1, "O3": o3, "peak_year": peak_y, "N_outcome": N, "O2r_m30": rarefied_richness(counts, 30),
            "O2r_m50": rarefied_richness(counts, 50), "O2_raw": int(sum(1 for c in counts if c >= 15))}
