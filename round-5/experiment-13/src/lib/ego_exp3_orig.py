#!/usr/bin/env python3
"""Ego-network features for every dev concept.

Ego network of concept c in window W (PRE=t0-3..t0-1, W1=t0..t0+1, W2=t0+2, W3=t0+3..t0+4): topic tag counts
n_ck(W) over c's title-matched base works; PMI_ck(W) = log(n_ck(W) N_W / (n_c(W) nbg_k(W))) with the exact
full-corpus background (nbg_k(W) = base works tagged k in W, N_W = base works with >= 1 topic in W).
NB(W) = {k : n_ck(W) >= 2, PMI > 0} minus SELF topics.  NEW = NB(W1)|NB(W2)|NB(W3) minus topics seen in PRE.

PRIMARY D  (D_z): distinct backbone communities reached by NEW (community of each topic in the slice of its first
                  appearance year), z-scored against a frequency-matched null (M topics drawn without replacement
                  with p ~ background frequency in t0..t0+4, from the non-PRE, non-SELF pool; 1,000 draws).
PRIMARY F  (F_res): growth S(W3) - S(W1) of the mean PMI of the top-20 neighbours (by n_ck), minus its mean under a
                  size-matched, concept-preserving multinomial null (T_W tags from the concept's pooled W1-W3 mix).
Secondaries / rivals are documented inline. Writes results/features.csv, results/field_features.csv,
results/reliability_splits.csv."""
from __future__ import annotations

import math
import multiprocessing as mp
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

import igraph as ig
import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr

from common import group_windows, lemmas, load_matches, load_scan_aggregates, slice_of, topic_lemma_df
from config import LOGS, N_NULL, PANEL, RES, ROOT, SEED, SLICES

BB = ROOT / "backbone"
SELF_DF_MAX = 100      # a concept lemma is "content" if it occurs in <= 100 of the 4,516 topic names
SELF_SHARE = 0.20
TOPN_F = 20
R_RARE = 10
N_SPLITS = 50
N_NULL_REL = 200

C: dict = {}  # per-process context


# ----------------------------------------------------------------------------- context
def build_context() -> dict:
    tids, G, Gt, bg, _pairs, nt, years = load_scan_aggregates()
    tm = pd.read_csv(RES / "topic_meta.csv").set_index("topic").loc[tids]
    sl = [np.load(BB / f"slice{s}.npz") for s in range(len(SLICES))]
    comm = [z["comm"] for z in sl]
    comm_q = [z["comm_q"] for z in sl]
    deg = [z["deg"] for z in sl]
    knn = [(z["ka"], z["kb"]) for z in sl]
    full_edges = [(z["a"], z["b"]) for z in sl]
    names = tm.name.tolist()
    ldf = topic_lemma_df(names)
    tlem = [lemmas(n) for n in names]
    return dict(tids=tids, nt=nt, years=years, Gt=Gt, bg=bg, comm=comm, comm_q=comm_q, deg=deg, knn=knn,
                full_edges=full_edges, subfield=tm.subfield.to_numpy(), field=tm.field.to_numpy(), names=names,
                ldf=ldf, tlem=tlem)


def _init(ctx_or_none=None) -> None:
    if not C:
        C.update(build_context())
        C["graphs"] = {}


def knn_graph(s: int) -> ig.Graph:
    if s not in C["graphs"]:
        ka, kb = C["knn"][s]
        C["graphs"][s] = ig.Graph(n=C["nt"], edges=list(zip(ka.tolist(), kb.tolist())), directed=False)
    return C["graphs"][s]


def bg_window(years: list[int]) -> tuple[np.ndarray, float]:
    yi = [C["years"].index(y) for y in years if y in C["years"]]
    return C["bg"][yi].sum(axis=0).astype(float), float(sum(C["Gt"].get(y, 0) for y in years))


# ----------------------------------------------------------------------------- ego statistics
def window_counts(works: list[tuple[int, tuple]], years: list[int]) -> tuple[np.ndarray, int]:
    nck = np.zeros(C["nt"], dtype=float)
    ncw = 0
    ys = set(years)
    for y, tp in works:
        if y in ys and tp:
            ncw += 1
            for k in tp:
                nck[k] += 1
    return nck, ncw


def pmi(nck: np.ndarray, nc: int, nbg: np.ndarray, N: float) -> np.ndarray:
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.log(nck * N / (nc * nbg))
    v[~np.isfinite(v)] = np.nan
    return v


def neighbours(nck, nc, nbg, N, excl: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    p = pmi(nck, nc, nbg, N) if nc > 0 else np.full(C["nt"], np.nan)
    nb = (nck >= 2) & (np.nan_to_num(p, nan=-1) > 0) & ~excl
    return nb, p


def topS(nck: np.ndarray, p: np.ndarray, nb: np.ndarray, top: int = TOPN_F) -> tuple[float, int]:
    idx = np.nonzero(nb)[0]
    if len(idx) == 0:
        return float("nan"), 0
    order = idx[np.lexsort((-p[idx], -nck[idx]))][:top]
    return float(np.mean(p[order])), len(order)


def self_topics(ci: int, n_early: np.ndarray, nc_early: int) -> np.ndarray:
    name, aliases, _ = PANEL[ci]
    # lexical SELF: the topic name contains ALL content lemmas of at least one of the concept's phrases
    sets = []
    for ph in [name] + aliases:
        cl = {l for l in lemmas(ph) if C["ldf"].get(l, 0) <= SELF_DF_MAX}
        if cl:
            sets.append(cl)
    lex = np.array([any(cl <= tl for cl in sets) for tl in C["tlem"]])
    share = n_early / nc_early if nc_early else np.zeros(C["nt"])
    return lex | (share >= SELF_SHARE)


def distinct_null(pool_idx: np.ndarray, w: np.ndarray, M: int, labels: np.ndarray, rng, n: int) -> np.ndarray:
    """# distinct labels among M topics drawn without replacement with p ~ w (Gumbel top-M), n draws."""
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


def f_null(p_mix: np.ndarray, pool: np.ndarray, T1: int, T3: int, nc1: int, nc3: int, nbg1, N1, nbg3, N3,
           rng, n: int) -> np.ndarray:
    """Null growth S*(W3)-S*(W1) under multinomial tag draws with probabilities p_mix over `pool`."""
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
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return S(T3, nc3, nbg3, N3) - S(T1, nc1, nbg1, N1)


def concept_core(ci: int, t0: int, works: list[tuple[int, tuple]], n_null: int, seed: int,
                 full: bool = True) -> dict:
    """All ego features for one concept (full=False: only D_z and F_res, for reliability splits)."""
    rng = np.random.default_rng(seed)
    win = group_windows(t0)
    early_years = list(range(t0, t0 + 5))
    n_early, nc_early = window_counts(works, early_years)
    SELF = self_topics(ci, n_early, nc_early)
    noself = np.zeros(C["nt"], dtype=bool)
    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}
    for w, ys in win.items():
        cnt[w], nc[w] = window_counts(works, ys)
        bgw[w], NW[w] = bg_window(ys)
    nbg_early, N_early = bg_window(early_years)
    for w in ("W1", "W2", "W3"):
        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF)
    pre_set = cnt["PRE"] >= 1
    new = (NB["W1"] | NB["W2"] | NB["W3"]) & ~pre_set
    new_idx = np.nonzero(new)[0]
    M = len(new_idx)
    # first appearance year of each NEW topic
    first_year = {}
    for y in early_years:
        cy, _ = window_counts(works, [y])
        for k in new_idx:
            if k not in first_year and cy[k] >= 1:
                first_year[k] = y
    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]
    s_mid = slice_of(t0 + 2)
    r: dict = {"M": M, "n_self_topics": int(SELF.sum()), "has_self_topic": int(SELF.any()),
               "nc_PRE": nc["PRE"], "nc_W1": nc["W1"], "nc_W2": nc["W2"], "nc_W3": nc["W3"]}

    def dz(labels_by_slice, pool_idx, new_list, lag=False):
        if M < 3:
            return float("nan"), float("nan"), float("nan"), None
        labs = []
        for k in new_list:
            s = slice_of(first_year.get(k, t0))
            if lag:
                s = max(0, s - 1)
            labs.append(labels_by_slice[s][k])
        obs = len(set(labs))
        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[max(0, s_mid - 1) if lag else s_mid],
                           rng, n_null)
        mu, sd = nl.mean(), nl.std()
        return (obs - mu) / sd if sd > 0 else 0.0, obs / mu if mu > 0 else float("nan"), obs, labs

    r["D_z"], r["D_ratio"], r["D_obs"], labs = dz(C["comm"], pool, new_idx)
    # ---- F
    S1, k1 = topS(cnt["W1"], P["W1"], NB["W1"])
    S3, k3 = topS(cnt["W3"], P["W3"], NB["W3"])
    obs_g = S3 - S1
    pooled = cnt["W1"] + cnt["W2"] + cnt["W3"]
    mixpool = np.nonzero((pooled > 0) & ~SELF)[0]
    T1 = int(cnt["W1"][~SELF].sum())
    T3 = int(cnt["W3"][~SELF].sum())
    ng = f_null(pooled, mixpool, T1, T3, nc["W1"], nc["W3"], bgw["W1"], NW["W1"], bgw["W3"], NW["W3"], rng, n_null)
    ok = np.isfinite(ng)
    if np.isfinite(obs_g) and ok.sum() >= 20:
        r["F_res"] = obs_g - ng[ok].mean()
        sdn = ng[ok].std()
        r["F_z"] = r["F_res"] / sdn if sdn > 0 else 0.0
    else:
        r["F_res"] = r["F_z"] = float("nan")
    r["F_obs_growth"] = obs_g
    r["k_used_W1"], r["k_used_W3"] = k1, k3
    if not full:
        return r
    # ---- D secondaries
    if M >= R_RARE and labs is not None:
        cc = np.array(list(Counter(labs).values()), dtype=float)
        from common import lgC
        r["D_rare"] = float(sum(1 - math.exp(lgC(M - m, R_RARE) - lgC(M, R_RARE)) if M - m >= R_RARE else 1.0
                                for m in cc))
    else:
        r["D_rare"] = float("nan")
    sub3 = [C["subfield"]] * len(SLICES)
    r["D_sub"], _, r["D_sub_obs"], _ = dz(sub3, pool, new_idx)
    r["D_lag"], _, _, _ = dz(C["comm"], pool, new_idx, lag=True)
    r["D_q"], _, r["D_q_obs"], _ = dz(C["comm_q"], pool, new_idx)
    # with self topics kept
    NBs = {w: neighbours(cnt[w], nc[w], bgw[w], NW[w], noself)[0] for w in ("W1", "W2", "W3")}
    new_s = np.nonzero((NBs["W1"] | NBs["W2"] | NBs["W3"]) & ~pre_set)[0]
    pool_s = np.nonzero((nbg_early > 0) & ~pre_set)[0]
    if len(new_s) >= 3:
        for k in new_s:
            if k not in first_year:
                for y in early_years:
                    if window_counts(works, [y])[0][k] >= 1:
                        first_year[k] = y
                        break
        labs_s = [C["comm"][slice_of(first_year.get(k, t0))][k] for k in new_s]
        nl = distinct_null(pool_s, nbg_early, len(new_s), C["comm"][s_mid], rng, n_null)
        r["D_withself"] = (len(set(labs_s)) - nl.mean()) / nl.std() if nl.std() > 0 else 0.0
    else:
        r["D_withself"] = float("nan")
    # F with the literal background-frequency null
    allpool = np.nonzero((bgw["W1"] > 0) & (bgw["W3"] > 0) & ~SELF)[0]
    nb_bg = f_null(nbg_early, allpool, T1, T3, nc["W1"], nc["W3"], bgw["W1"], NW["W1"], bgw["W3"], NW["W3"], rng,
                   n_null)
    okb = np.isfinite(nb_bg)
    r["F_bg"] = obs_g - nb_bg[okb].mean() if (np.isfinite(obs_g) and okb.sum() >= 20) else float("nan")
    # ---- novelty vs degree-preserving expectation
    s0 = slice_of(t0)
    comm0 = C["comm"][s0]
    w1 = cnt["W1"]
    if w1.sum() > 0:
        cs = Counter()
        for k in np.nonzero(w1)[0]:
            cs[comm0[k]] += w1[k]
        C0 = cs.most_common(1)[0][0]
        r["C0"] = int(C0)
        if M > 0:
            r["NOV"] = float(np.mean([C["comm"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))
            dg = C["deg"][s0][pool].astype(float)
            E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float("nan")
            r["NOV_res"] = r["NOV"] - E
        else:
            r["NOV"] = r["NOV_res"] = float("nan")
    else:
        r["C0"], r["NOV"], r["NOV_res"] = -1, float("nan"), float("nan")
    # ---- classic rivals on the same ego network
    n1, n2, n3 = NB["W1"].sum(), NB["W2"].sum(), NB["W3"].sum()
    r["deg_W1"], r["deg_W3"] = int(n1), int(n3)
    r["deg_growth"] = math.log(n3 + 1) - math.log(n1 + 1)
    sp1 = np.nansum(P["W1"][NB["W1"]])
    sp3 = np.nansum(P["W3"][NB["W3"]])
    r["str_growth"] = math.log(sp3 + 1) - math.log(sp1 + 1)
    r["new_edge_rate"] = (M / 5.0) / (n1 + 1)

    def jac(a, b):
        u = (a | b).sum()
        return (a & b).sum() / u if u else float("nan")
    r["edge_persistence"] = float(np.nanmean([jac(NB["W1"], NB["W2"]), jac(NB["W2"], NB["W3"])]))
    r["turnover"] = float((NB["W1"] & ~NB["W3"]).sum() / n1) if n1 else float("nan")
    s4 = slice_of(t0 + 4)
    if n3 > 0:
        ws = Counter()
        for k in np.nonzero(NB["W3"])[0]:
            ws[C["comm"][s4][k]] += cnt["W3"][k]
        tot = sum(ws.values())
        r["participation"] = 1 - sum((v / tot) ** 2 for v in ws.values())
        r["n_comm_W3"] = len(ws)
    else:
        r["participation"], r["n_comm_W3"] = float("nan"), 0
    dom = []
    for w in ("W1", "W2", "W3"):
        s = slice_of(win[w][0])
        if cnt[w].sum() > 0:
            cs = Counter()
            for k in np.nonzero(cnt[w])[0]:
                cs[C["comm"][s][k]] += cnt[w][k]
            dom.append(cs.most_common(1)[0][0])
    r["comm_transitions"] = sum(1 for a, b in zip(dom, dom[1:]) if a != b)
    # ego density in the backbone (local clustering of the neighbourhood) and its change
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
    # betweenness / k-core of the concept inserted in the kNN backbone
    for tag, w, s in (("t0", "W1", s0), ("t4", "W3", s4)):
        idx = np.nonzero(NB[w])[0]
        if len(idx) == 0:
            r[f"btw_{tag}"] = 0.0
            r[f"kcore_{tag}"] = 0
            continue
        g = knn_graph(s).copy()
        g.add_vertices(1)
        v = g.vcount() - 1
        g.add_edges([(v, int(k)) for k in idx])
        n = g.vcount()
        b = g.betweenness(vertices=[v], directed=False)[0]
        r[f"btw_{tag}"] = b / ((n - 1) * (n - 2) / 2)
        r[f"kcore_{tag}"] = int(g.coreness()[v])
        r[f"constraint_{tag}"] = float(g.constraint(vertices=[v])[0])
    r["btw_change"] = r["btw_t4"] - r["btw_t0"]
    r["constraint_change"] = r.get("constraint_t4", np.nan) - r.get("constraint_t0", np.nan)
    # ---- field-level features (for R_j): Dj and Fj per field j
    fl = {}
    for j in np.unique(C["field"]):
        mj = C["field"] == j
        dj = int((new & mj).sum())
        s1, _ = topS(cnt["W1"], P["W1"], NB["W1"] & mj, top=5)
        s3, _ = topS(cnt["W3"], P["W3"], NB["W3"] & mj, top=5)
        fl[int(j)] = {"Dj": math.log1p(dj), "Fj": (s3 - s1) if np.isfinite(s3) and np.isfinite(s1) else 0.0,
                      "Fj_missing": int(not (np.isfinite(s3) and np.isfinite(s1)))}
    r["_field"] = fl
    # neighbour audit (top-10 PMI neighbours in W3, for sanity/case studies)
    idx = np.nonzero(NB["W3"])[0]
    top = idx[np.argsort(-P["W3"][idx])][:10]
    r["_top_nb_W3"] = [(C["names"][k], round(float(P["W3"][k]), 2), int(cnt["W3"][k])) for k in top]
    r["_self_names"] = [C["names"][k] for k in np.nonzero(SELF)[0]][:8]
    return r


# ----------------------------------------------------------------------------- job wrappers (process pool)
def job_full(args):
    ci, t0, works, seed = args
    _init()
    return ci, concept_core(ci, t0, works, N_NULL, seed, full=True)


def job_split(args):
    ci, t0, works, seed = args
    _init()
    rng = np.random.default_rng(seed)
    out = []
    for sp in range(N_SPLITS):
        mask = rng.random(len(works)) < 0.5
        A = [w for w, m in zip(works, mask) if m]
        B = [w for w, m in zip(works, mask) if not m]
        ra = concept_core(ci, t0, A, N_NULL_REL, seed + 1000 + sp, full=False)
        rb = concept_core(ci, t0, B, N_NULL_REL, seed + 5000 + sp, full=False)
        out.append({"split": sp, "D_z_A": ra["D_z"], "D_z_B": rb["D_z"], "F_res_A": ra["F_res"],
                    "F_res_B": rb["F_res"], "D_ratio_A": ra["D_ratio"], "D_ratio_B": rb["D_ratio"]})
    return ci, out


def concept_works(matches: pd.DataFrame, ci: int, t0: int) -> list[tuple[int, tuple]]:
    d = matches[(matches.ci == ci) & (matches.year >= t0 - 3) & (matches.year <= t0 + 4)]
    return list(zip(d.year.astype(int).tolist(), d.topics.tolist()))


@logger.catch(reraise=True)
def main(n_workers: int = 4, do_reliability: bool = True, only: list[str] | None = None) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "features.log", rotation="30 MB", level="DEBUG")
    out = pd.read_csv(RES / "outcomes.csv")
    dev = out[out.dropped_reason.isna() | (out.dropped_reason == "")].copy()
    if only:
        dev = dev[dev.concept.isin(only)]
    matches = load_matches()
    name2ci = {p[0]: i for i, p in enumerate(PANEL)}
    jobs = []
    for _, row in dev.iterrows():
        ci = name2ci[row.concept]
        jobs.append((ci, int(row.t0), concept_works(matches, ci, int(row.t0)), SEED + ci))
    del matches
    logger.info(f"features for {len(jobs)} dev concepts, {n_workers} workers")
    feats, ffeats, audits = [], [], []
    with ProcessPoolExecutor(n_workers, mp_context=mp.get_context("spawn")) as ex:
        for ci, r in ex.map(job_full, jobs):
            name = PANEL[ci][0]
            for j, v in r.pop("_field").items():
                ffeats.append({"concept": name, "field": j, **v})
            audits.append({"concept": name, "top_nb_W3": r.pop("_top_nb_W3"), "self_topics": r.pop("_self_names")})
            feats.append({"concept": name, **r})
            logger.info(f"{name:45s} M={r['M']:4d} D_z={r['D_z']:.2f} F_res={r['F_res']:.3f} "
                        f"NOV_res={r['NOV_res']:.2f} k1={r['k_used_W1']} k3={r['k_used_W3']}")
    fdf = pd.DataFrame(feats)
    fdf.to_csv(RES / "features_ego.csv", index=False)
    pd.DataFrame(ffeats).to_csv(RES / "field_features.csv", index=False)
    import json
    (RES / "neighbour_audit.json").write_text(json.dumps(audits, indent=1))
    if do_reliability:
        rel = []
        with ProcessPoolExecutor(n_workers, mp_context=mp.get_context("spawn")) as ex:
            for ci, rows in ex.map(job_split, jobs):
                for rr in rows:
                    rel.append({"concept": PANEL[ci][0], **rr})
        pd.DataFrame(rel).to_csv(RES / "reliability_splits.csv", index=False)
        logger.info(f"reliability splits written: {len(rel)} rows")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--no_rel", action="store_true")
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args()
    main(a.workers, not a.no_rel, a.only)
