"""Cheng et al. (2023, ASR 88:522-561) resonance measures rebuilt on OpenAlex topic co-usage (frozen in S0).

For concept c, paper set P (HOME = grounded papers whose venue field is in the frozen home set; ALL = every grounded
paper) and calendar year t:
  v_t[k]   = # year-t papers of c in P tagged with topic k, k not in SELF(c)       (neighbour co-usage vector)
  CONS(t)  = cosine(v_{t-1}, v_t)                                  defined iff both years have >= 3 papers (with
                                                                   >= 1 topic) and >= 2 non-self topics; else NaN
  CONS_r(t)= Cheng-verbatim variant: cosine over the t-1 neighbour support only,
             dot(v_{t-1}, v_t) / (|v_{t-1}| |v_t restricted to supp(v_{t-1})|), 0 if that restriction is empty
  EMB(t)   = ANALOGUE of ideational embeddedness: co-usage-weighted mean positive PMI over pairs of the top-20
             year-t neighbour topics on the EXP3 backbone slice s(t); weight(k,l) = v_t[k] v_t[l]; a pair with no
             backbone edge has PMI+ = 0 (the backbone keeps only PMI > 0, c >= 3)
  EMB_cos(t) (exploratory) = unweighted mean pairwise cosine of the neighbours' backbone PMI rows (a second-order
             'embedding' similarity, closer in spirit to Cheng's word2vec cosine)
  SOC(t)   = density of the prior-tie graph among year-t authors of c in P (papers with <= 15 authors, as Cheng);
             nodes capped at 200 (random, seeded by (ci, year)); an edge iff the two co-authored any paper of c
             (any field, <= 15 authors) in years t-10..t-1. NaN if < 3 authors.
SELF(c) = Exp11/EXP8 ego.self_topics on ALL papers over t0..t0+2 (name/alias lemma rule + share >= 0.20)."""
from __future__ import annotations

import math
from functools import lru_cache

import numpy as np
import scipy.sparse as sp

import ego
from common import (EMB_TOPN, MIN_PAPERS, MIN_TOPICS, SOC_CAP, SOC_LOOKBACK, SOC_MAX_AUTHORS_PER_PAPER,
                    SOC_MIN_AUTHORS)

_PMI: dict = {}
_ROWN: dict = {}


def init_context() -> None:
    """Backbone-only ego context (no background counts are needed: CONS uses raw co-usage, not PMI neighbours)."""
    from ego_ctx import backbone_context
    ctx = backbone_context()
    ctx.update(years=[], bg=np.zeros((0, ctx["nt"])), Gt={})
    ego.set_context(ctx)
    from common import INPUTS
    for s in range(3):
        z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
        a, b, w = z["a"].astype(np.int64), z["b"].astype(np.int64), z["w"].astype(float)
        nt = ctx["nt"]
        W = sp.coo_matrix((np.r_[w, w], (np.r_[a, b], np.r_[b, a])), shape=(nt, nt)).tocsr()
        W.sum_duplicates()
        _PMI[s] = W
        nrm = np.sqrt(np.asarray(W.multiply(W).sum(1)).ravel())
        nrm[nrm == 0] = 1.0
        _ROWN[s] = sp.diags(1.0 / nrm) @ W


def set_pmi_for_tests(mats: dict) -> None:
    _PMI.clear()
    _ROWN.clear()
    for s, W in mats.items():
        W = sp.csr_matrix(W, dtype=float)
        _PMI[s] = W
        nrm = np.sqrt(np.asarray(W.multiply(W).sum(1)).ravel())
        nrm[nrm == 0] = 1.0
        _ROWN[s] = sp.diags(1.0 / nrm) @ W


# ----------------------------------------------------------------------------- measures
def cosine(u: np.ndarray, v: np.ndarray) -> float:
    nu, nv = float(np.sqrt(u @ u)), float(np.sqrt(v @ v))
    if nu == 0 or nv == 0:
        return 0.0
    return float(u @ v / (nu * nv))


def cons(v_prev: np.ndarray, v_cur: np.ndarray, n_prev: int, n_cur: int) -> tuple[float, float]:
    """(CONS, CONS_r). NaN unless both years have >= MIN_PAPERS papers and >= MIN_TOPICS non-self topics."""
    if n_prev < MIN_PAPERS or n_cur < MIN_PAPERS:
        return float("nan"), float("nan")
    if (v_prev > 0).sum() < MIN_TOPICS or (v_cur > 0).sum() < MIN_TOPICS:
        return float("nan"), float("nan")
    c = cosine(v_prev, v_cur)
    supp = v_prev > 0
    vr = np.where(supp, v_cur, 0.0)
    cr = cosine(v_prev, vr)
    return c, cr


def top_neighbours(v: np.ndarray, topn: int = EMB_TOPN) -> np.ndarray:
    idx = np.nonzero(v > 0)[0]
    if len(idx) <= topn:
        return idx
    order = np.lexsort((idx, -v[idx]))           # count desc, ties by topic index
    return idx[order[:topn]]


def emb(v: np.ndarray, n_cur: int, s: int) -> tuple[float, float]:
    """(EMB weighted mean positive PMI, EMB_cos mean pairwise second-order cosine) over the top-20 neighbours."""
    if n_cur < MIN_PAPERS:
        return float("nan"), float("nan")
    idx = top_neighbours(v)
    m = len(idx)
    if m < MIN_TOPICS:
        return float("nan"), float("nan")
    P = _PMI[s][idx][:, idx].toarray()
    P = np.maximum(P, 0.0)
    w = np.outer(v[idx], v[idx])
    iu = np.triu_indices(m, 1)
    e = float((w[iu] * P[iu]).sum() / w[iu].sum())
    X = _ROWN[s][idx]
    G = (X @ X.T).toarray()
    ec = float(G[iu].mean())
    return e, ec


def soc_density(nodes: list[int], adj_years: list[dict]) -> float:
    """Share of node pairs linked by a prior tie (union of the per-year co-author adjacency dicts)."""
    m = len(nodes)
    if m < SOC_MIN_AUTHORS:
        return float("nan")
    S = set(nodes)
    e2 = 0
    for u in nodes:
        nb = set()
        for adj in adj_years:
            x = adj.get(u)
            if x:
                nb |= x
        if nb:
            e2 += len(nb & S)
    return float(e2 / 2.0 / (m * (m - 1) / 2.0))


# ----------------------------------------------------------------------------- per-concept driver
def _year_vectors(years: np.ndarray, t_off: np.ndarray, tflat: np.ndarray, mask: np.ndarray, Y: np.ndarray,
                  nt: int) -> tuple[np.ndarray, np.ndarray]:
    """counts [len(Y), nt] and # papers with >= 1 topic per year, for rows in mask."""
    ny = len(Y)
    yi = years - Y[0]
    ok = mask & (yi >= 0) & (yi < ny)
    ln = np.diff(t_off)
    rows = np.repeat(np.arange(len(years)), ln)
    sel = ok[rows]
    cnt = np.bincount(yi[rows[sel]] * nt + tflat[sel], minlength=ny * nt).reshape(ny, nt).astype(float)
    ncw = np.bincount(yi[ok & (ln > 0)], minlength=ny).astype(float)
    return cnt, ncw


def concept_measures(*, ci: int, name: str, aliases: list[str], t0: int, y_lo: int, y_hi: int, years: np.ndarray,
                     vfield: np.ndarray, t_off: np.ndarray, tflat: np.ndarray, a_off: np.ndarray,
                     aflat: np.ndarray, home: set[int], want_self: np.ndarray | None = None) -> list[dict]:
    """Rows (ci, year, build, CONS, CONS_r, EMB, EMB_cos, SOC, n_papers, n_topics, n_authors) for y_lo <= t <= y_hi
    and build in {HOME, ALL}. The input rows are the concept's grounded papers over t0-3..y_hi."""
    C = ego.C
    nt = C["nt"]
    Y = np.arange(t0 - 3, y_hi + 1)
    iy = {int(y): i for i, y in enumerate(Y)}
    is_home = np.isin(vfield, list(home)) if home else np.zeros(len(years), bool)
    allm = np.ones(len(years), bool)
    cA, ncA = _year_vectors(years, t_off, tflat, allm, Y, nt)
    cH, ncH = _year_vectors(years, t_off, tflat, is_home, Y, nt)
    if want_self is None:
        e_idx = [iy[y] for y in (t0, t0 + 1, t0 + 2) if y in iy]
        SELF = ego.self_topics(name, aliases, cA[e_idx].sum(0), float(ncA[e_idx].sum()))
    else:
        SELF = want_self
    keep = ~SELF
    # author lists per paper (papers with <= 15 authors only, as Cheng)
    alen = np.diff(a_off)
    small = (alen > 0) & (alen <= SOC_MAX_AUTHORS_PER_PAPER)
    if not len(alen):
        small = np.zeros(0, bool)
    adj_by_year: dict[int, dict] = {}
    auth_by_year: dict[tuple[str, int], list[int]] = {}
    for j in np.nonzero(small)[0]:
        y = int(years[j])
        au = aflat[a_off[j]:a_off[j + 1]]
        au = au[au > 0].tolist()                  # null author ids were filled with -1 upstream
        adj = adj_by_year.setdefault(y, {})
        su = set(au)
        for u in su:
            adj.setdefault(u, set()).update(su - {u})
        auth_by_year.setdefault(("ALL", y), []).extend(au)
        if is_home[j]:
            auth_by_year.setdefault(("HOME", y), []).extend(au)
    rows = []
    for build, cnt, ncw in (("HOME", cH, ncH), ("ALL", cA, ncA)):
        for t in range(y_lo, y_hi + 1):
            if t not in iy:
                continue
            i = iy[t]
            v = cnt[i] * keep
            n_cur = int(ncw[i])
            r = {"ci": ci, "year": t, "build": build, "n_papers": n_cur, "n_topics": int((v > 0).sum())}
            if t - 1 in iy:
                vp = cnt[i - 1] * keep
                r["CONS"], r["CONS_r"] = cons(vp, v, int(ncw[i - 1]), n_cur)
            else:
                r["CONS"], r["CONS_r"] = float("nan"), float("nan")
            r["EMB"], r["EMB_cos"] = emb(v, n_cur, ego.slice_of(t))
            au = sorted(set(auth_by_year.get((build, t), [])))
            r["n_authors"] = len(au)
            if len(au) > SOC_CAP:
                rng = np.random.default_rng([int(ci), int(t)])
                au = sorted(rng.choice(au, SOC_CAP, replace=False).tolist())
            window = [adj_by_year[y] for y in range(t - SOC_LOOKBACK, t) if y in adj_by_year]
            r["SOC"] = soc_density(au, window)
            rows.append(r)
    return rows


def pack(df_rows) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(years, vfield, t_off, tflat, a_off, aflat) from a per-concept DataFrame with list columns."""
    t_len = df_rows.topics.map(len).to_numpy()
    t_off = np.zeros(len(df_rows) + 1, np.int64)
    t_off[1:] = np.cumsum(t_len)
    tflat = (np.concatenate([np.asarray(t, np.int64) for t in df_rows.topics]) if t_off[-1]
             else np.zeros(0, np.int64))
    a_len = df_rows.authors.map(len).to_numpy()
    a_off = np.zeros(len(df_rows) + 1, np.int64)
    a_off[1:] = np.cumsum(a_len)
    aflat = (np.concatenate([np.asarray(a, np.int64) for a in df_rows.authors]) if a_off[-1]
             else np.zeros(0, np.int64))
    return (df_rows.year.to_numpy(np.int64), df_rows.vfield.to_numpy(np.int64), t_off, tflat, a_off, aflat)


def nan_or(x) -> float:
    return float(x) if x is not None and math.isfinite(x) else float("nan")
