"""Exact log-additive decomposition of the breadth gap between top and bottom O2r_resid terciles.

Per concept (H = 8): E2 = off-home fields entered by age 2, EH = entered by age 8, Bn = |RETAINED at age 8|,
M = EH / E2 (frontier advance), rho = Bn / EH (retention); log Bn = log E2 + log M + log rho when E2, Bn >= 1.
GROUP LEVEL (exact with zeros): Ebar = mean E2, M_g = sum EH / sum E2, rho_g = sum Bn / sum EH, so
Bbar = mean Bn = Ebar * M_g * rho_g. D_k = log f_k(top) - log f_k(bottom); share_k = D_k / sum_k D_k (for a
log-additive identity the Shapley value of each factor is exactly D_k). Stratified variants average stratum D_k with
weights n_s (top + bottom concepts of the stratum); strata where a factor is undefined are merged with the adjacent
stratum (logged)."""
from __future__ import annotations

import math

import numpy as np

FACTORS = ["E2", "M", "rho"]
MIN_PER_TERCILE_CI = 30          # fallback 8: fewer concepts per tercile -> no CI, excluded from DL


def terciles(y: np.ndarray, by: np.ndarray | None) -> tuple[np.ndarray, np.ndarray]:
    """top / bottom tercile masks of y, computed within each level of `by` (or the whole sample)."""
    top = np.zeros(len(y), bool)
    bot = np.zeros(len(y), bool)
    levels = [None] if by is None else np.unique(by)
    for g in levels:
        m = np.ones(len(y), bool) if g is None else by == g
        if m.sum() < 3:
            continue
        lo, hi = np.quantile(y[m], [1 / 3, 2 / 3])
        top |= m & (y > hi)
        bot |= m & (y <= lo)
    return top, bot


def quantile_bins(v: np.ndarray, q: int) -> np.ndarray:
    edges = np.quantile(v, np.linspace(0, 1, q + 1)[1:-1])
    return np.searchsorted(edges, v, side="right")


def _factors(E2, EH, Bn) -> tuple[float, float, float]:
    se2, seh, sbn = E2.sum(), EH.sum(), Bn.sum()
    if len(E2) == 0 or se2 <= 0 or seh <= 0 or sbn <= 0:
        return (math.nan,) * 3
    return float(E2.mean()), float(seh / se2), float(sbn / seh)


def _stratum_ok(E2, EH, Bn, t, b) -> bool:
    return t.sum() > 0 and b.sum() > 0 and all(np.isfinite(_factors(E2[m], EH[m], Bn[m])).all() for m in (t, b))


def merge_strata(strata: np.ndarray, E2, EH, Bn, top, bot, family: np.ndarray | None = None) -> tuple[np.ndarray, int]:
    """merge adjacent (ordered) strata until each has valid factors in both terciles; within `family` levels."""
    out = strata.copy()
    merges = 0
    fams = [None] if family is None else np.unique(family)
    for f in fams:
        fm = np.ones(len(strata), bool) if f is None else family == f
        levels = sorted(np.unique(strata[fm]))
        buckets, cur = [], []
        for s in levels:
            cur.append(s)
            m = fm & np.isin(strata, cur)
            if _stratum_ok(E2, EH, Bn, top & m, bot & m):
                buckets.append(cur)
                cur = []
        if cur:
            if buckets:
                buckets[-1] = buckets[-1] + cur
            else:
                buckets.append(cur)
        merges += len(levels) - len(buckets)
        for bk in buckets:
            out[fm & np.isin(strata, bk)] = bk[0]
    return out, merges


def gap(E2, EH, Bn, top, bot, strata: np.ndarray | None = None, family: np.ndarray | None = None) -> dict:
    """D_k (n-weighted over strata), shares, and the unstratified factor levels."""
    if strata is None:
        strata = np.zeros(len(E2), int)
    st, merges = merge_strata(strata, E2, EH, Bn, top, bot, family)
    keys = st * 1000 + (0 if family is None else family)
    Dw = np.zeros(3)
    W = 0.0
    n_str = 0
    for s in np.unique(keys):
        m = keys == s
        t, b = top & m, bot & m
        ft, fb = _factors(E2[t], EH[t], Bn[t]), _factors(E2[b], EH[b], Bn[b])
        if not (np.isfinite(ft).all() and np.isfinite(fb).all()):
            continue
        w = float(t.sum() + b.sum())
        Dw += w * (np.log(ft) - np.log(fb))
        W += w
        n_str += 1
    D = Dw / W if W > 0 else np.full(3, np.nan)
    tot = D.sum()
    sh = D / tot if np.isfinite(tot) and abs(tot) > 1e-12 else np.full(3, np.nan)
    ft, fb = _factors(E2[top], EH[top], Bn[top]), _factors(E2[bot], EH[bot], Bn[bot])
    return {"D_E2": D[0], "D_M": D[1], "D_rho": D[2], "D_total": tot, "s_E2": sh[0], "s_M": sh[1], "s_rho": sh[2],
            "s_explore": sh[0] + sh[1], "s_contact": sh[0], "s_ret": sh[2],
            "diff_explore_ret": (sh[0] + sh[1]) - sh[2], "diff_contact_ret": sh[0] - sh[2],
            "top_Ebar": ft[0], "top_M": ft[1], "top_rho": ft[2], "bot_Ebar": fb[0], "bot_M": fb[1], "bot_rho": fb[2],
            "top_Bbar": float(Bn[top].mean()) if top.any() else math.nan,
            "bot_Bbar": float(Bn[bot].mean()) if bot.any() else math.nan,
            "n_top": int(top.sum()), "n_bot": int(bot.sum()), "n_strata": n_str, "merges": merges}


def das_gupta(E2, EH, Bn, top, bot) -> dict:
    """additive 3-factor Das Gupta decomposition of Bbar(top) - Bbar(bottom) (pooled)."""
    a1, b1, c1 = _factors(E2[top], EH[top], Bn[top])
    a2, b2, c2 = _factors(E2[bot], EH[bot], Bn[bot])

    def eff(x1, x2, y1, y2, z1, z2):
        return (x1 - x2) * ((y1 * z1 + y2 * z2) / 3 + (y1 * z2 + y2 * z1) / 6)
    eA = eff(a1, a2, b1, b2, c1, c2)
    eB = eff(b1, b2, a1, a2, c1, c2)
    eC = eff(c1, c2, a1, a2, b1, b2)
    g = a1 * b1 * c1 - a2 * b2 * c2
    return {"effect_E2": eA, "effect_M": eB, "effect_rho": eC, "gap_Bbar": g, "sum_effects": eA + eB + eC,
            "share_E2": eA / g, "share_M": eB / g, "share_rho": eC / g}


def concept_cov(E2, EH, Bn) -> dict:
    """exact covariance decomposition var(log Bn) = sum_k cov(log Bn, log f_k) among Bn >= 1."""
    m = (Bn >= 1) & (E2 >= 1)
    lb = np.log(Bn[m])
    le, lm, lr = np.log(E2[m]), np.log(EH[m] / E2[m]), np.log(Bn[m] / EH[m])
    v = lb.var()
    cs = [float(np.cov(lb, x, bias=True)[0, 1]) for x in (le, lm, lr)]
    return {"n": int(m.sum()), "var_logBn": float(v), "cov_E2": cs[0], "cov_M": cs[1], "cov_rho": cs[2],
            "share_E2": cs[0] / v, "share_M": cs[1] / v, "share_rho": cs[2] / v,
            "identity_max_abs_err": float(np.max(np.abs(lb - (le + lm + lr)))) if m.any() else 0.0}


def run_variant(d: dict, spec: dict, rng: np.random.Generator | None, n_boot: int) -> dict:
    """d: arrays E2, EH, Bn, y (tercile outcome), logvol_early, med, tby (tercile-within levels or None),
    rs (resampling strata, e.g. unit). spec: strata in {none, vol, vol_med}."""
    def once(idx: np.ndarray | None) -> dict:
        g = (lambda a: a) if idx is None else (lambda a: None if a is None else a[idx])  # noqa: E731
        E2, EH, Bn, y = g(d["E2"]), g(d["EH"]), g(d["Bn"]), g(d["y"])
        top, bot = terciles(y, g(d.get("tby")))
        strata = family = None
        if spec["strata"] in ("vol", "vol_med"):
            lv = g(d["logvol_early"])
            tb = g(d.get("tby"))
            if tb is None:
                strata = quantile_bins(lv, 5)
            else:  # quintiles within each tercile-level (unit) so strata never mix units
                strata = np.zeros(len(lv), int)
                for u in np.unique(tb):
                    m = tb == u
                    strata[m] = quantile_bins(lv[m], 5)
                family = np.unique(tb, return_inverse=True)[1]
        if spec["strata"] == "vol_med":
            med = g(d["med"]).astype(int)
            family = med if family is None else family * 2 + med
        return gap(E2, EH, Bn, top, bot, strata, family)
    point = once(None)
    out = {"point": point, "n": int(len(d["E2"]))}
    if rng is None or n_boot <= 0:
        return out
    n = len(d["E2"])
    rs = d.get("rs")
    groups = [np.arange(n)] if rs is None else [np.nonzero(rs == u)[0] for u in np.unique(rs)]
    keys = ["D_E2", "D_M", "D_rho", "D_total", "s_E2", "s_M", "s_rho", "s_explore", "s_contact", "s_ret",
            "diff_explore_ret", "diff_contact_ret"]
    B = {k: np.empty(n_boot) for k in keys}
    for b in range(n_boot):
        idx = np.concatenate([gi[rng.integers(0, len(gi), len(gi))] for gi in groups])
        r = once(idx)
        for k in keys:
            B[k][b] = r[k]
    out["ci"] = {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in B.items()}
    out["se"] = {k: float(np.nanstd(v, ddof=1)) for k, v in B.items()}
    out["p_two_sided"] = {k: float(min(1.0, 2 * min(np.nanmean(v <= 0), np.nanmean(v >= 0)))) for k, v in B.items()}
    out["boot_nan_share"] = float(np.mean(~np.isfinite(B["s_ret"])))
    out["_boot"] = B
    return out


def verdict(ci: list[float]) -> str:
    lo, hi = ci
    if not (np.isfinite(lo) and np.isfinite(hi)):
        return "NOT EVALUABLE"
    if lo > 0:
        return "SUPPORTED"
    if hi < 0:
        return "REVERSED"
    return "NOT SUPPORTED"
