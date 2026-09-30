"""Concept features (G family, secondaries, simple reference indicators, B5) and S0 outcomes. No API cost."""
from __future__ import annotations

import math
from collections import Counter

import numpy as np
from scipy.special import gammaln
from scipy.stats import spearmanr

HOME_DEV = {"CS": "Computer Science", "Eng": "Engineering",
            "BGM": "Biochemistry, Genetics and Molecular Biology", "Med": "Medicine"}


# ------------------------------------------------------------------ primitives
def rarefied_richness(counts: list[int] | np.ndarray, m: int) -> float:
    """Exact hypergeometric rarefaction E[S_m] = sum_j 1 - C(N-n_j, m)/C(N, m)."""
    n = np.asarray([c for c in counts if c > 0], dtype=float)
    N = n.sum()
    if N < m:
        return math.nan
    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)
    out = 0.0
    for nj in n:
        if N - nj < m:
            out += 1.0
        else:
            out += 1.0 - math.exp(lc(N - nj, m) - lc(N, m))
    return out


def shannon(c: dict) -> float:
    v = np.array([x for x in c.values() if x > 0], dtype=float)
    if v.sum() == 0:
        return math.nan
    p = v / v.sum()
    return float(-(p * np.log(p)).sum())


def kleinberg_batched(r: list[int], d: list[int], s: float = 2.0, gamma: float = 1.0) -> tuple[list[int], float]:
    """Kleinberg (2002) 2-state batched burst detection (own Viterbi). Returns states and burst weight."""
    r = np.asarray(r, float)
    d = np.asarray(d, float)
    n = len(r)
    p0 = r.sum() / d.sum()
    p1 = min(s * p0, 0.9999)

    def cost(p):
        return -(r * math.log(p) + (d - r) * math.log(1 - p))
    c = np.vstack([cost(p0), cost(p1)])
    trans = gamma * math.log(n)
    V = np.zeros((2, n))
    back = np.zeros((2, n), int)
    V[0, 0], V[1, 0] = c[0, 0], c[1, 0] + trans
    for t in range(1, n):
        for q in (0, 1):
            cand = [V[0, t - 1] + (trans if q == 1 else 0), V[1, t - 1]]
            back[q, t] = int(np.argmin(cand))
            V[q, t] = min(cand) + c[q, t]
    st = [int(np.argmin(V[:, -1]))]
    for t in range(n - 1, 0, -1):
        st.append(back[st[-1], t])
    st = st[::-1]
    weight = float(sum(c[0, t] - c[1, t] for t in range(n) if st[t] == 1))
    return st, weight


def cohort_split_half(mats: list[list[str]], fn, n_splits: int = 50, seed: int = 0) -> dict:
    """Split-half reliability across concepts: split each concept's paper-label list into random halves,
    compute fn(labels) per half, Spearman across concepts, Spearman-Brown corrected."""
    rng = np.random.default_rng(seed)
    rs = []
    for _ in range(n_splits):
        a, b = [], []
        for labels in mats:
            idx = rng.permutation(len(labels))
            h = len(labels) // 2
            a.append(fn([labels[i] for i in idx[:h]]))
            b.append(fn([labels[i] for i in idx[h:2 * h]]))
        a, b = np.array(a, float), np.array(b, float)
        ok = np.isfinite(a) & np.isfinite(b)
        if ok.sum() >= 5:
            r = spearmanr(a[ok], b[ok]).statistic
            if np.isfinite(r):
                rs.append(2 * r / (1 + r) if r > -1 else np.nan)
    rs = np.array(rs, float)
    if len(rs) == 0:
        return {"r_sb_median": math.nan, "p05": math.nan, "p95": math.nan, "n_splits": 0}
    return {"r_sb_median": float(np.nanmedian(rs)), "p05": float(np.nanpercentile(rs, 5)),
            "p95": float(np.nanpercentile(rs, 95)), "n_splits": int(len(rs))}


# ------------------------------------------------------------------ feature builders
class Backbone:
    def __init__(self, b: dict):
        self.fields = b["fields"]
        self.idx = {f: i for i, f in enumerate(self.fields)}
        self.phi = np.array(b["phi"])
        self.phi_min = np.array(b["phi_min"])
        self.gate = {k: np.array(b[k]) for k in ("gateway_eig", "gateway_deg", "gateway_btw", "gateway_eig_phimin")}
        self.domain = b["domain"]
        self.logsize = np.log(np.array(b["n_field"]))

    def g(self, f: str, kind: str = "gateway_eig") -> float:
        return float(self.gate[kind][self.idx[f]])


def g_family(fc: dict, home: list[str], bb: Backbone) -> dict:
    """G and secondaries from a field-count dict (labelled papers)."""
    tot = sum(fc.values())
    out = {}
    off = {f: n for f, n in fc.items() if f not in home and n > 0}
    offt = sum(off.values())
    for kind, nm in (("gateway_eig", "G"), ("gateway_deg", "G_deg"), ("gateway_btw", "G_btw"),
                     ("gateway_eig_phimin", "G_phimin")):
        out[nm] = sum(n * bb.g(f, kind) for f, n in off.items()) / offt if offt else math.nan
    out["G_all"] = sum(n * bb.g(f) for f, n in fc.items()) / tot if tot else math.nan
    hi = [bb.idx[h] for h in home if h in bb.idx]
    out["REL_home"] = (sum(n * np.mean([bb.phi[i, bb.idx[f]] for i in hi]) for f, n in off.items()) / offt
                       if offt and hi else math.nan)
    if tot:
        p = np.zeros(26)
        for f, n in fc.items():
            p[bb.idx[f]] = n / tot
        D = 1 - bb.phi_min
        np.fill_diagonal(D, 0)
        out["RS"] = float(p @ D @ p)
        for dom in ("Physical", "Life", "Health", "Social"):
            out[f"DOM_{dom}"] = float(sum(p[i] for i in range(26) if bb.domain[i] == dom))
    else:
        out["RS"] = math.nan
        for dom in ("Physical", "Life", "Health", "Social"):
            out[f"DOM_{dom}"] = math.nan
    top5 = set(np.argsort(bb.gate["gateway_eig"])[::-1][:5])
    out["GATEWAY_REACH"] = sum(1 for f, n in fc.items() if n >= 2 and bb.idx[f] in top5)
    return out


def g_from_labels(labels: list[str], home: list[str], bb: Backbone) -> float:
    return g_family(Counter(labels), home, bb)["G"]


def label_indicators(fc: dict, home: list[str], total: int) -> dict:
    lab = sum(fc.values())
    off = sum(n for f, n in fc.items() if f not in home)
    return {"entropy": shannon(fc) if lab else math.nan,
            "reach": sum(1 for n in fc.values() if n >= 2),
            "offhome_share": off / lab if lab else math.nan,
            "log_offhome_volume": math.log1p(off),
            "label_coverage": lab / total if total else math.nan}


def count_indicators(yc: dict, gtot: dict, t0: int, end: int) -> dict:
    ys = list(range(t0, end + 1))
    n = np.array([yc.get(y, 0) for y in ys], float)
    out = {"log_count": math.log1p(n.sum()), "share": n.sum() / sum(gtot[y] for y in ys) * 1e6,
           "growth": math.log((yc.get(end, 0) + 1) / (yc.get(t0 + 1, 0) + 1))}
    x = np.array(ys, float) - t0
    out["accel"] = float(np.polyfit(x, np.log1p(n), 2)[0]) if len(ys) >= 3 else math.nan
    yrs = list(range(t0 - 3, end + 1))
    _, w = kleinberg_batched([yc.get(y, 0) for y in yrs], [gtot[y] for y in yrs])
    out["burst"] = w
    return out


def outcomes(yc: dict, gtot: dict, t0: int, fcD: dict | None) -> dict:
    sh = lambda y: yc.get(y, 0) / gtot[y]
    o1 = int(np.mean([sh(y) for y in range(t0 + 6, t0 + 9)]) >= sh(t0 + 5))
    seq = [yc.get(y, 0) for y in range(t0, t0 + 9)]
    peak_y = t0 + int(np.argmax(seq))
    late = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])
    o3 = int(t0 + 3 <= peak_y <= t0 + 8 and max(seq) / max(late, 1e-9) >= 2)
    res = {"O1": o1, "O3": o3, "peak_year": peak_y}
    if fcD is not None:
        counts = list(fcD.values())
        N = int(sum(counts))
        res.update({"N_outcome": N, "O2r_m30": rarefied_richness(counts, 30),
                    "O2r_m50": rarefied_richness(counts, 50),
                    "O2_raw": int(sum(1 for c in counts if c >= 15))})
    else:
        res.update({"N_outcome": math.nan, "O2r_m30": math.nan, "O2r_m50": math.nan, "O2_raw": math.nan})
    return res
