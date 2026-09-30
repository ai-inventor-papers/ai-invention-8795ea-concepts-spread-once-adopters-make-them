"""Co-occurrence ego-network indicators (family A), ported from art_yrradSC27HtQ features.concept_core.

Port changes (all logged in results/deviations.json):
  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)
    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).
  * the background comes from the context (Pass A BG/GT for RQ1; EXP3's ckpt for the port-validation test T0-8).
  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.
  * dropped near-duplicate variants: D_lag, D_q, D_withself, F_bg; the per-field block is not needed.
  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.
Everything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,
NOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code."""
from __future__ import annotations

import math
import warnings
from collections import Counter

import igraph as ig
import numpy as np

SELF_DF_MAX = 100
SELF_SHARE = 0.20
TOPN_F = 20
R_RARE = 10
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]

C: dict = {}


def slice_of(y: int) -> int:
    for i, (a, b) in enumerate(SLICES):
        if a <= y <= b:
            return i
    return 0 if y < SLICES[0][0] else len(SLICES) - 1


def rq1_windows(t0: int) -> dict[str, list[int]]:
    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0], "W2": [t0 + 1], "W3": [t0 + 2]}


def exp3_windows(t0: int) -> dict[str, list[int]]:
    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0, t0 + 1], "W2": [t0 + 2], "W3": [t0 + 3, t0 + 4]}


def lgC(n: float, k: float) -> float:
    from scipy.special import gammaln
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def set_context(ctx: dict) -> None:
    """ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,
    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable)."""
    C.clear()
    C.update(ctx)
    C["graphs"] = {}
    C["yidx"] = {y: i for i, y in enumerate(ctx["years"])}


def knn_graph(s: int) -> ig.Graph:
    if s not in C["graphs"]:
        ka, kb = C["knn"][s]
        C["graphs"][s] = ig.Graph(n=C["nt"], edges=list(zip(ka.tolist(), kb.tolist())), directed=False)
    return C["graphs"][s]


def bg_window(years: list[int]) -> tuple[np.ndarray, float]:
    yi = [C["yidx"][y] for y in years if y in C["yidx"]]
    return C["bg"][yi].sum(axis=0).astype(float), float(sum(C["Gt"].get(y, 0) for y in years))


def window_counts(works, years) -> tuple[np.ndarray, int]:
    nck = np.zeros(C["nt"], dtype=float)
    ncw = 0
    ys = set(years)
    for y, tp in works:
        if y in ys and len(tp):
            ncw += 1
            for k in tp:
                nck[k] += 1
    return nck, ncw


def pmi(nck, nc, nbg, N):
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.log(nck * N / (nc * nbg))
    v[~np.isfinite(v)] = np.nan
    return v


def neighbours(nck, nc, nbg, N, excl, min_n: int = 2):
    p = pmi(nck, nc, nbg, N) if nc > 0 else np.full(C["nt"], np.nan)
    nb = (nck >= min_n) & (np.nan_to_num(p, nan=-1) > 0) & ~excl
    return nb, p


def topS(nck, p, nb, top: int = TOPN_F):
    idx = np.nonzero(nb)[0]
    if len(idx) == 0:
        return float("nan"), 0
    order = idx[np.lexsort((-p[idx], -nck[idx]))][:top]
    return float(np.mean(p[order])), len(order)


def self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:
    lem = C["lemmas"]
    sets = []
    for ph in [name] + aliases:
        cl = {l for l in lem(ph) if C["ldf"].get(l, 0) <= SELF_DF_MAX}
        if cl:
            sets.append(cl)
    lex = np.array([any(cl <= tl for cl in sets) for tl in C["tlem"]])
    share = n_early / nc_early if nc_early else np.zeros(C["nt"])
    return lex | (share >= SELF_SHARE)


def distinct_null(pool_idx, w, M, labels, rng, n):
    if M <= 0 or len(pool_idx) == 0:
        return np.zeros(n)
    M = min(M, len(pool_idx))
    lw = np.log(w[pool_idx])
    out = np.empty(n)
    lab = labels[pool_idx]
    chunk = max(1, 2_000_000 // len(pool_idx))
    for s in range(0, n, chunk):
        m = min(chunk, n - s)
        g = lw[None, :] + rng.gumbel(size=(m, len(pool_idx)))
        top = np.argpartition(-g, M - 1, axis=1)[:, :M]
        L = np.sort(lab[top], axis=1)
        out[s:s + m] = 1 + (np.diff(L, axis=1) != 0).sum(axis=1)
    return out


def f_null(p_mix, pool, T1, T3, nc1, nc3, nbg1, N1, nbg3, N3, rng, n):
    if len(pool) == 0 or T1 == 0 or T3 == 0 or nc1 == 0 or nc3 == 0:
        return np.full(n, np.nan)
    pr = p_mix[pool] / p_mix[pool].sum()

    def S(T, nc, nbg, N):
        X = rng.multinomial(T, pr, size=n).astype(float)
        with np.errstate(divide="ignore", invalid="ignore"):
            P = np.log(X * N / (nc * nbg[pool][None, :]))
        elig = (X >= 2) & np.isfinite(P) & (P > 0)
        key = np.where(elig, X + 1e-6 * np.nan_to_num(P, nan=0, posinf=0, neginf=0), -np.inf)
        order = np.argsort(-key, axis=1)[:, :TOPN_F]
        Ps = np.take_along_axis(np.where(elig, P, np.nan), order, axis=1)
        with np.errstate(invalid="ignore"):
            return np.nanmean(np.where(np.isfinite(Ps), Ps, np.nan), axis=1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return S(T3, nc3, nbg3, N3) - S(T1, nc1, nbg1, N1)


def _centrality(idx: np.ndarray, s: int, cutoff: int | None) -> tuple[float, int, float]:
    if len(idx) == 0:
        return 0.0, 0, float("nan")
    g = knn_graph(s).copy()
    g.add_vertices(1)
    v = g.vcount() - 1
    g.add_edges([(v, int(k)) for k in idx])
    n = g.vcount()
    b = g.betweenness(vertices=[v], directed=False, cutoff=cutoff)[0]
    return b / ((n - 1) * (n - 2) / 2), int(g.coreness()[v]), float(g.constraint(vertices=[v])[0])


def concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,
                 btw_cutoff: int | None = 4, nb_min_w: int = 2) -> dict:
    """All family-A indicators for one concept. works = [(year, tuple of topic indices)]."""
    rng = np.random.default_rng(seed)
    win = windows(t0)
    early_years = sorted(set(win["W1"] + win["W2"] + win["W3"]))
    n_early, nc_early = window_counts(works, early_years)
    SELF = self_topics(name, aliases, n_early, nc_early)
    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}
    for w, ys in win.items():
        cnt[w], nc[w] = window_counts(works, ys)
        bgw[w], NW[w] = bg_window(ys)
    nbg_early, _ = bg_window(early_years)
    for w in ("W1", "W2", "W3"):
        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, nb_min_w)
    pre_set = cnt["PRE"] >= 1
    new = (NB["W1"] | NB["W2"] | NB["W3"]) & ~pre_set
    new_idx = np.nonzero(new)[0]
    M = len(new_idx)
    first_year = {}
    for y in early_years:
        cy, _ = window_counts(works, [y])
        for k in new_idx:
            if k not in first_year and cy[k] >= 1:
                first_year[k] = y
    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]
    s_mid = slice_of(early_years[len(early_years) // 2])
    r: dict = {"M": M, "n_self_topics": int(SELF.sum()), "nc_PRE": nc["PRE"], "nc_W1": nc["W1"], "nc_W2": nc["W2"],
               "nc_W3": nc["W3"]}

    def dz(labels_by_slice, pool_idx, new_list):
        if M < 3:
            return float("nan"), float("nan"), float("nan"), None
        labs = [labels_by_slice[slice_of(first_year.get(k, t0))][k] for k in new_list]
        obs = len(set(labs))
        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[s_mid], rng, n_null)
        mu, sd = nl.mean(), nl.std()
        return (obs - mu) / sd if sd > 0 else 0.0, obs / mu if mu > 0 else float("nan"), obs, labs

    r["D_z"], r["D_ratio"], r["D_obs"], labs = dz(C["comm"], pool, new_idx)
    S1, k1 = topS(cnt["W1"], P["W1"], NB["W1"])
    S3, k3 = topS(cnt["W3"], P["W3"], NB["W3"])
    obs_g = S3 - S1
    pooled = cnt["W1"] + cnt["W2"] + cnt["W3"]
    mixpool = np.nonzero((pooled > 0) & ~SELF)[0]
    T1 = int(cnt["W1"][~SELF].sum())
    T3 = int(cnt["W3"][~SELF].sum())
    ng = f_null(pooled, mixpool, T1, T3, nc["W1"], nc["W3"], bgw["W1"], NW["W1"], bgw["W3"], NW["W3"], rng,
                n_null)
    ok = np.isfinite(ng)
    if np.isfinite(obs_g) and ok.sum() >= 20:
        r["F_res"] = obs_g - ng[ok].mean()
        sdn = ng[ok].std()
        r["F_z"] = r["F_res"] / sdn if sdn > 0 else 0.0
    else:
        r["F_res"] = r["F_z"] = float("nan")
    if M >= R_RARE and labs is not None:
        cc = np.array(list(Counter(labs).values()), dtype=float)
        r["D_rare"] = float(sum(1 - math.exp(lgC(M - m, R_RARE) - lgC(M, R_RARE)) if M - m >= R_RARE else 1.0
                                for m in cc))
    else:
        r["D_rare"] = float("nan")
    sub3 = [C["subfield"]] * len(SLICES)
    r["D_sub"], _, _, _ = dz(sub3, pool, new_idx)
    # novelty vs degree-preserving expectation
    s0 = slice_of(t0)
    comm0 = C["comm"][s0]
    w1 = cnt["W1"]
    if w1.sum() > 0:
        cs = Counter()
        for k in np.nonzero(w1)[0]:
            cs[comm0[k]] += w1[k]
        C0 = cs.most_common(1)[0][0]
        if M > 0:
            r["NOV"] = float(np.mean([C["comm"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))
            dg = C["deg"][s0][pool].astype(float)
            E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float("nan")
            r["NOV_res"] = r["NOV"] - E
        else:
            r["NOV"] = r["NOV_res"] = float("nan")
    else:
        r["NOV"] = r["NOV_res"] = float("nan")
    n1, n3 = NB["W1"].sum(), NB["W3"].sum()
    r["deg_W1"], r["deg_W3"] = int(n1), int(n3)
    r["deg_growth"] = math.log(n3 + 1) - math.log(n1 + 1)
    sp1 = np.nansum(P["W1"][NB["W1"]])
    sp3 = np.nansum(P["W3"][NB["W3"]])
    r["str_growth"] = math.log(sp3 + 1) - math.log(sp1 + 1)
    n_years = len(early_years)
    r["new_edge_rate"] = (M / float(n_years)) / (n1 + 1)

    def jac(a, b):
        u = (a | b).sum()
        return (a & b).sum() / u if u else float("nan")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        r["edge_persistence"] = float(np.nanmean([jac(NB["W1"], NB["W2"]), jac(NB["W2"], NB["W3"])]))
    r["turnover"] = float((NB["W1"] & ~NB["W3"]).sum() / n1) if n1 else float("nan")
    s4 = slice_of(win["W3"][-1])
    if n3 > 0:
        ws = Counter()
        for k in np.nonzero(NB["W3"])[0]:
            ws[C["comm"][s4][k]] += cnt["W3"][k]
        tot = sum(ws.values())
        pw = np.array([v / tot for v in ws.values()])
        r["participation"] = float(1 - (pw ** 2).sum())
        r["n_comm_W3"] = len(ws)
        r["comm_entropy"] = float(-(pw * np.log(pw)).sum())
    else:
        r["participation"], r["n_comm_W3"], r["comm_entropy"] = float("nan"), 0, float("nan")
    dom = []
    for w in ("W1", "W2", "W3"):
        s = slice_of(win[w][0])
        if cnt[w].sum() > 0:
            cs = Counter()
            for k in np.nonzero(cnt[w])[0]:
                cs[C["comm"][s][k]] += cnt[w][k]
            dom.append(cs.most_common(1)[0][0])
    r["comm_transitions"] = sum(1 for a, b in zip(dom, dom[1:]) if a != b)
    for w, s in (("W1", s0), ("W3", s4)):
        idx = np.nonzero(NB[w])[0]
        if len(idx) >= 2:
            a, b = C["full_edges"][s]
            ins = np.zeros(C["nt"], dtype=bool)
            ins[idx] = True
            e = int((ins[a] & ins[b]).sum())
            r[f"ego_density_{w}"] = e / (len(idx) * (len(idx) - 1) / 2)
        else:
            r[f"ego_density_{w}"] = float("nan")
    r["ego_density_change"] = r["ego_density_W3"] - r["ego_density_W1"]
    b0, _, c0 = _centrality(np.nonzero(NB["W1"])[0], s0, btw_cutoff)
    b4, k4, c4 = _centrality(np.nonzero(NB["W3"])[0], s4, btw_cutoff)
    r["btw_start"], r["btw_end"], r["kcore_end"] = b0, b4, k4
    r["btw_change"] = b4 - b0
    r["constraint_end"] = c4
    r["constraint_change"] = c4 - c0
    idx = np.nonzero(NB["W3"])[0]
    top = idx[np.argsort(-P["W3"][idx])][:10]
    r["_top_nb_W3"] = [(C["names"][k], round(float(P["W3"][k]), 2), int(cnt["W3"][k])) for k in top]
    return r


EGO_OUT = ["D_z", "D_ratio", "D_rare", "D_sub", "D_obs", "NOV", "NOV_res", "F_res", "F_z", "deg_W1", "deg_W3",
           "deg_growth", "str_growth", "new_edge_rate", "edge_persistence", "turnover", "participation", "n_comm_W3",
           "comm_entropy", "comm_transitions", "ego_density_W3", "ego_density_change", "btw_end", "btw_change",
           "kcore_end", "constraint_end", "constraint_change"]
