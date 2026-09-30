"""RQ2 trajectories (DTW k-medoids + Gaussian HMM, k by silhouette and bootstrap ARI) and the ordering test
(calibrated change-point for entropy take-off vs first retained gateway field; lead-lag panels)."""
from __future__ import annotations

import math
import warnings

import numpy as np
import pandas as pd
from scipy import stats

from config import Y0
from h2 import states
from lib_outcomes import rarefied_richness, shannon
from stats_core import fe_ols

VARS = ["n_entered_offhome", "n_retaining", "n_lost", "R20", "H", "G_share", "log_volume"]


def concept_series(g: np.ndarray, t0: int, home: list[int], gate: np.ndarray, top: np.ndarray, bot: np.ndarray) -> pd.DataFrame:
    S = states(g, home)
    rows = []
    for t in range(t0, t0 + 9):
        ti = t - Y0
        win = g[max(ti - 2, 0):ti + 1, 1:].sum(0)
        off = S["offhome"]
        tot = win.sum()
        rows.append({"t": t, "age": t - t0, "n_entered_offhome": int((S["entered"][ti] & off).sum()),
                     "n_retaining": int(S["retaining"][ti].sum()), "n_lost": int((S["lost"][ti] & off).sum()),
                     "R20": rarefied_richness(np.round(win).astype(int), 20), "H": shannon(win),
                     "G_share": float((win * off * gate).sum() / tot) if tot else np.nan,
                     "log_volume": math.log1p(g[ti].sum()),
                     "ret_gw": int((S["retaining"][ti] & top).sum()), "ret_per": int((S["retaining"][ti] & bot).sum())})
    df = pd.DataFrame(rows)
    for v in ("R20", "H", "G_share"):
        df[v] = df[v].ffill().bfill().fillna(0 if v != "R20" else 1.0)
    return df


def panel(frame: pd.DataFrame, G: dict, gate: np.ndarray, top: np.ndarray, bot: np.ndarray) -> pd.DataFrame:
    out = []
    for r in frame.itertuples():
        home = [int(h) for h in str(r.home).split("|")]
        s = concept_series(G[int(r.cidx)], int(r.t0), home, gate, top, bot)
        s.insert(0, "cidx", int(r.cidx))
        out.append(s)
    return pd.concat(out, ignore_index=True)


def to_array(P: pd.DataFrame, zspec: dict) -> tuple[np.ndarray, np.ndarray]:
    ids = P.cidx.unique()
    Z = np.stack([((P[P.cidx == c][VARS] - pd.Series({v: zspec[v][0] for v in VARS})) /
                   pd.Series({v: zspec[v][1] for v in VARS})).to_numpy() for c in ids])
    return ids, Z


def dtw_matrix(Z: np.ndarray) -> np.ndarray:
    from tslearn.metrics import cdist_dtw
    return cdist_dtw(Z, global_constraint="sakoe_chiba", sakoe_chiba_radius=2, n_jobs=4)


def kmed(D: np.ndarray, k: int, seed: int) -> tuple[np.ndarray, np.ndarray]:
    import kmedoids
    r = kmedoids.fasterpam(D, k, random_state=seed, max_iter=300, init="build")
    return np.asarray(r.labels), np.asarray(r.medoids)


def choose_k(D: np.ndarray, seed: int, ks=range(2, 9), n_boot: int = 100) -> dict:
    from sklearn.metrics import adjusted_rand_score, silhouette_score
    rng = np.random.default_rng(seed)
    n = len(D)
    res = {}
    for k in ks:
        if k >= n:
            break
        lab, med = kmed(D, k, seed)
        sil = float(silhouette_score(D, lab, metric="precomputed")) if len(set(lab)) > 1 else float("nan")
        aris = []
        for b in range(n_boot):
            idx = np.sort(rng.choice(n, int(0.8 * n), replace=False))
            lb, _ = kmed(D[np.ix_(idx, idx)], k, seed + b + 1)
            aris.append(adjusted_rand_score(lab[idx], lb))
        res[k] = {"silhouette": sil, "ari_median": float(np.median(aris)), "ari_p10": float(np.percentile(aris, 10)),
                  "sizes": np.bincount(lab).tolist()}
    ok = [k for k, v in res.items() if v["ari_median"] >= 0.6]
    if ok:
        kbest = max(ok, key=lambda k: res[k]["silhouette"]); flag = "stable"
    else:
        kbest = 2; flag = "unstable"
    return {"grid": res, "k": kbest, "flag": flag}


def hmm_fit(Z: np.ndarray, seed: int, n_states=range(2, 7)) -> dict:
    from hmmlearn.hmm import GaussianHMM
    X = Z.reshape(-1, Z.shape[2]); L = [Z.shape[1]] * Z.shape[0]
    best = None; grid = {}
    for s in n_states:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            m = GaussianHMM(n_components=s, covariance_type="diag", n_iter=200, random_state=seed).fit(X, L)
        ll = m.score(X, L)
        p = s * (s - 1) + (s - 1) + 2 * s * Z.shape[2]
        bic = -2 * ll + p * math.log(len(X))
        grid[s] = {"ll": float(ll), "bic": float(bic)}
        if best is None or bic < best[1]:
            best = (s, bic, m)
    s, _, m = best
    paths = np.stack([m.predict(z) for z in Z])
    return {"grid": grid, "n_states": s, "paths": paths, "model": m,
            "means": m.means_.tolist(), "transmat": m.transmat_.tolist()}


def collapse(path: np.ndarray) -> str:
    out = [int(path[0])]
    for x in path[1:]:
        if int(x) != out[-1]:
            out.append(int(x))
    return "-".join(map(str, out))


# ------------------------------------------------------------------ ordering
def first_upward_change(h: np.ndarray, pen: float) -> int | None:
    import ruptures as rpt
    x = np.asarray(h, float)
    sd = x.std()
    if sd == 0 or len(x) < 4:
        return None
    x = (x - x.mean()) / sd
    bps = rpt.Pelt(model="l2", min_size=2, jump=1).fit(x.reshape(-1, 1)).predict(pen=pen)
    prev = 0
    for b in bps[:-1]:
        nxt = bps[bps.index(b) + 1]
        if x[b:nxt].mean() > x[prev:b].mean():
            return b
        prev = b
    return None


def calibrate_pen(series: list[np.ndarray], seed: int, target: float = 0.05, n_shuf: int = 200) -> dict:
    rng = np.random.default_rng(seed)
    shuf = []
    for _ in range(n_shuf):
        s = series[rng.integers(len(series))]
        shuf.append(rng.permutation(s))
    grid = np.round(np.concatenate([np.linspace(0.5, 6, 23), np.linspace(6.5, 20, 10)]), 3)
    far = {float(p): float(np.mean([first_upward_change(s, p) is not None for s in shuf])) for p in grid}
    ok = [p for p, f in far.items() if f <= target]
    pen = min(ok) if ok else max(far)
    # fresh shuffles to check the achieved rate
    fresh = [rng.permutation(series[rng.integers(len(series))]) for _ in range(n_shuf)]
    far_fresh = float(np.mean([first_upward_change(s, pen) is not None for s in fresh]))
    return {"pen": float(pen), "far_grid": far, "far_fresh": far_fresh}


def ordering(P: pd.DataFrame, frame: pd.DataFrame, pen: float, top_o2r: set[int]) -> dict:
    rows = []
    for c, d in P.groupby("cidx"):
        d = d.sort_values("t")
        b = first_upward_change(d.H.to_numpy(), pen)
        tau = int(d.t.iloc[b]) if b is not None else None
        gw = d[d.ret_gw > 0].t; pe = d[d.ret_per > 0].t
        rows.append({"cidx": c, "tau": tau, "gamma": int(gw.iloc[0]) if len(gw) else None,
                     "pi": int(pe.iloc[0]) if len(pe) else None, "top_o2r": c in top_o2r})
    O = pd.DataFrame(rows)
    T = O[O.top_o2r]

    def share(col: str) -> dict:
        d = T[T.tau.notna() & T[col].notna()]
        before = int((d[col] < d.tau).sum()); ties = int((d[col] == d.tau).sum()); after = int((d[col] > d.tau).sum())
        n = before + after
        return {"n_evaluable": int(len(d)), "before": before, "ties": ties, "after": after,
                "share_before_excl_ties": before / n if n else float("nan"),
                "sign_test_p_one_sided": float(stats.binom.sf(before - 1, n, 0.5)) if n else float("nan")}
    res = {"n_top_o2r": int(len(T)), "n_tau_detected": int(T.tau.notna().sum()),
           "share_tau_detected": float(T.tau.notna().mean()) if len(T) else float("nan"),
           "gateway": share("gamma"), "peripheral": share("pi")}
    # paired McNemar on concepts with both gamma and pi evaluable
    d = T[T.tau.notna() & T.gamma.notna() & T.pi.notna()]
    a = (d.gamma < d.tau).astype(int); b = (d.pi < d.tau).astype(int)
    n01 = int(((a == 0) & (b == 1)).sum()); n10 = int(((a == 1) & (b == 0)).sum())
    res["mcnemar"] = {"n": int(len(d)), "gw_only": n10, "per_only": n01,
                      "p_exact_two_sided": float(stats.binomtest(n10, n10 + n01, 0.5).pvalue) if n10 + n01 else float("nan")}
    return res, O


def lead_lag(P: pd.DataFrame) -> dict:
    P = P.sort_values(["cidx", "t"]).copy()
    P["dH_next"] = P.groupby("cidx").H.shift(-1) - P.H
    P["dret_gw_next"] = P.groupby("cidx").ret_gw.shift(-1) - P.ret_gw
    P["ret_gw_i"] = (P.ret_gw > 0).astype(float); P["ret_per_i"] = (P.ret_per > 0).astype(float)
    ok = P.dH_next.notna()
    d = P[ok]
    fwd = fe_ols(d.dH_next.to_numpy(), d[["ret_gw_i", "ret_per_i", "log_volume"]].to_numpy(),
                 [d.cidx.to_numpy(), d.age.to_numpy()], d.cidx.to_numpy(), ["ret_gw", "ret_per", "log_volume"])
    rev = fe_ols(d.dret_gw_next.to_numpy(), d[["H", "log_volume"]].to_numpy(), [d.cidx.to_numpy(), d.age.to_numpy()],
                 d.cidx.to_numpy(), ["H", "log_volume"])
    # event study on H(t) around the first retained gateway year (never-treated concepts are controls)
    first = P[P.ret_gw > 0].groupby("cidx").t.min()
    P["ev"] = P.t - P.cidx.map(first)
    names, cols = [], []
    for k in (-3, -2, 0, 1, 2, 3):
        nm = f"ev{k:+d}"
        if k == -3:
            P[nm] = (P.ev <= -3).astype(float)
        elif k == 3:
            P[nm] = (P.ev >= 3).astype(float)
        else:
            P[nm] = (P.ev == k).astype(float)
        P[nm] = P[nm].fillna(0.0)
        names.append(nm); cols.append(nm)
    es = fe_ols(P.H.to_numpy(), P[cols + ["log_volume"]].to_numpy(), [P.cidx.to_numpy(), P.age.to_numpy()],
                P.cidx.to_numpy(), names + ["log_volume"])
    for r in (fwd, rev, es):
        r.pop("_b", None); r.pop("V", None)
    return {"forward_dH_on_ret": fwd, "reverse_dret_on_H": rev, "event_study_H": es,
            "n_treated": int(first.notna().sum()), "n_concepts": int(P.cidx.nunique())}
