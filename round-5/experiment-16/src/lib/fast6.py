"""Vectorised re-implementation of the six OPEN components of lib/ego.concept_core (EXP10 version), batched over
D resamples of ONE concept's HOME papers.

A resample is a label vector over the concept's home papers: -1 = dropped, 0 = PRE (t0-3..t0-1), 1 = W1 (t0),
2 = W2 (t0+1), 3 = W3 (t0+2). The raw build is the label vector implied by the paper years. The SELF set (the
concept's own name topics) is computed ONCE on the full home build (ego.self_topics) and held fixed in every
resample (declared in results/frozen_spec.json). Every other step is copied from ego.concept_core:
  window counts -> neighbours (count >= 2 & PMI > 0 & ~SELF) -> pre_set (PRE count >= 1) -> new = union(NB) & ~pre
  -> first year -> NOV / degree-matched expectation over the pool -> Jaccards -> participation / n_comm over comm[s4]
  -> ego density over full_edges[s4].
Validated against ego.concept_core with the SELF override to <= 1e-12 (tests/u_tests.py, U1)."""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp

import ego

OUT6 = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def base_labels(years: np.ndarray, t0: int) -> np.ndarray:
    lab = np.full(len(years), -1, np.int8)
    lab[(years >= t0 - 3) & (years <= t0 - 1)] = 0
    for j in range(3):
        lab[years == t0 + j] = j + 1
    return lab


def prep(name: str, aliases: list, t0: int, works: list) -> dict:
    """Per-concept precomputation (needs ego.set_context to have been called)."""
    C = ego.C
    years = np.array([y for y, _ in works], np.int64)
    tps = [np.asarray(tp, np.int64) for _, tp in works]
    lab = base_labels(years, t0)
    allt = np.concatenate(tps) if tps else np.zeros(0, np.int64)
    U = np.unique(allt)                                  # ascending global ids -> local order == global order
    nU = len(U)
    loc = {int(g): i for i, g in enumerate(U)}
    rows, cols = [], []
    for p, tp in enumerate(tps):
        for k in tp.tolist():
            rows.append(p)
            cols.append(loc[k])
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(works), nU))   # duplicates summed
    nonempty = np.array([len(tp) > 0 for tp in tps], float)
    # SELF on the FULL home build (ego.self_topics inputs = early-window counts)
    early = [t0, t0 + 1, t0 + 2]
    n_early, nc_early = ego.window_counts(works, early)
    SELF = ego.self_topics(name, aliases, n_early, nc_early)
    selfU = SELF[U]
    # candidate neighbour topics: non-SELF, total W1..W3 count >= 2
    wmask = (lab >= 1).astype(float)
    totW = np.asarray(A.T @ wmask).ravel()
    cand = np.nonzero((~selfU) & (totW >= 2))[0]
    cg = U[cand]
    win = ego.rq1_windows(t0)
    bgw, NW = {}, {}
    for w, ys in win.items():
        b, n = ego.bg_window(ys)
        bgw[w], NW[w] = b, n
    nbg_early, _ = ego.bg_window(early)
    s0 = ego.slice_of(t0)
    s4 = ego.slice_of(win["W3"][-1])
    comm0 = C["comm"][s0]
    dg = C["deg"][s0].astype(float)
    pool0 = (nbg_early > 0) & ~SELF
    Tpool = float(dg[pool0].sum())
    ncomm_g = int(max(c.max() for c in C["comm"])) + 1
    Dc = np.bincount(comm0[pool0], weights=dg[pool0], minlength=ncomm_g)
    # dense W3 adjacency among candidates (full_edges[s4], each listed edge counted once, a < b)
    a, b = C["full_edges"][s4]
    pos = np.full(C["nt"], -1, np.int64)
    pos[cg] = np.arange(len(cg))
    m = (pos[a] >= 0) & (pos[b] >= 0)
    adj = np.zeros((len(cg), len(cg)), float)
    np.add.at(adj, (pos[a[m]], pos[b[m]]), 1.0)
    adj = adj + adj.T
    return dict(t0=t0, U=U, A=A, AT=A.T.tocsr(), nonempty=nonempty, lab=lab, years=years, selfU=selfU, cand=cand,
                cg=cg, SELF=SELF, s0=s0, s4=s4,
                bg_c={w: bgw[w][cg] for w in ("W1", "W2", "W3")}, NW=NW,
                comm0U=comm0[U], comm4c=C["comm"][s4][cg],
                commfy=np.stack([C["comm"][ego.slice_of(t0 + j)][cg] for j in range(3)]),
                dgU=dg[U], pool0U=pool0[U], Tpool=Tpool, Dc=Dc, ncomm_g=ncomm_g, adj=adj)


def window_counts_batch(P: dict, L: np.ndarray, w: int) -> tuple[np.ndarray, np.ndarray]:
    """counts (D x nU) and n papers with >= 1 topic (D) for label w."""
    Mw = (L == w).astype(float)                          # D x P
    cnt = np.asarray((P["AT"] @ Mw.T)).T if P["A"].shape[1] else np.zeros((L.shape[0], 0))
    return cnt, Mw @ P["nonempty"]


def fast6(P: dict, L: np.ndarray, return_sets: bool = False, return_counts: bool = False) -> dict:
    """L: D x P int8 labels. Returns dict of (D,) arrays for OUT6 (+ M, deg_W1, deg_W3, nc_W*) and optionally the
    neighbour sets NB_W1..3 as D x n_cand bool (candidate order P['cg'])."""
    L = np.atleast_2d(L)
    D = L.shape[0]
    cnt, nc = {}, {}
    for w in range(4):
        cnt[w], nc[w] = window_counts_batch(P, L, w)
    cand = P["cand"]
    NB = {}
    for w in (1, 2, 3):
        c = cnt[w][:, cand]
        key = f"W{w}"
        ncw = nc[w][:, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            v = np.log(c * P["NW"][key] / (ncw * P["bg_c"][key][None, :]))
        v[~np.isfinite(v)] = np.nan
        NB[w] = (c >= 2) & (np.nan_to_num(v, nan=-1) > 0) & (ncw > 0)
    pre = cnt[0] >= 1                                     # D x nU
    new = (NB[1] | NB[2] | NB[3]) & ~pre[:, cand]
    M = new.sum(1)
    # first year of each new topic (first early year with count >= 1)
    c1, c2 = cnt[1][:, cand], cnt[2][:, cand]
    fy = np.where(c1 >= 1, 0, np.where(c2 >= 1, 1, 2))
    commfy = P["commfy"][fy, np.arange(len(cand))[None, :]] if len(cand) else np.zeros((D, 0), np.int64)
    # C0: dominant W1 community over ALL topics (Counter insertion order == ascending topic id -> ties go to the
    # community whose first contributing topic has the smallest id)
    w1 = cnt[1]
    has1 = w1.sum(1) > 0
    nU = len(P["U"])
    comm0U = P["comm0U"]
    cw = np.zeros((D, P["ncomm_g"]))
    first = np.full((D, P["ncomm_g"]), nU + 1, np.int64)
    rr, kk = np.nonzero(w1 > 0)
    np.add.at(cw, (rr, comm0U[kk]), w1[rr, kk])
    np.minimum.at(first, (rr, comm0U[kk]), kk)
    cmax = cw.max(1, keepdims=True)
    key = np.where((cw == cmax) & (cw > 0), -first, -(10 ** 9))
    C0 = key.argmax(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        nov = ((commfy != C0[:, None]) & new).sum(1) / M
    preP = pre & P["pool0U"][None, :]
    corrT = preP.astype(float) @ P["dgU"]
    corrC = (preP & (comm0U[None, :] == C0[:, None])).astype(float) @ P["dgU"]
    den = P["Tpool"] - corrT
    num = den - (P["Dc"][C0] - corrC)
    with np.errstate(invalid="ignore", divide="ignore"):
        E = np.where(den > 0, num / np.where(den > 0, den, 1), np.nan)
    nov_res = np.where(has1 & (M > 0), nov - E, np.nan)
    n1, n3 = NB[1].sum(1), NB[3].sum(1)
    ner = (M / 3.0) / (n1 + 1)

    def jac(a, b):
        u = (a | b).sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(u > 0, (a & b).sum(1) / np.where(u > 0, u, 1), np.nan)
    j12, j23 = jac(NB[1], NB[2]), jac(NB[2], NB[3])
    with np.errstate(invalid="ignore"):
        ep = np.where(np.isfinite(j12) & np.isfinite(j23), (j12 + j23) / 2,
                      np.where(np.isfinite(j12), j12, np.where(np.isfinite(j23), j23, np.nan)))
    # participation / n_comm over comm[s4] of NB_W3 weighted by W3 counts
    c3 = cnt[3][:, cand] * NB[3]
    ncm = int(P["comm4c"].max()) + 1 if len(cand) else 1
    ws = np.zeros((D, ncm))
    if len(cand):
        rr, kk = np.nonzero(c3 > 0)
        np.add.at(ws, (rr, P["comm4c"][kk]), c3[rr, kk])
    tot = ws.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pw = ws / tot[:, None]
    part = np.where(n3 > 0, 1 - (pw ** 2).sum(1), np.nan)
    ncomm = np.where(n3 > 0, (ws > 0).sum(1), 0).astype(float)
    nb3f = NB[3].astype(float)
    e = ((nb3f @ P["adj"]) * nb3f).sum(1) / 2
    with np.errstate(invalid="ignore", divide="ignore"):
        dens = np.where(n3 >= 2, e / (n3 * (n3 - 1) / 2), np.nan)
    out = {"new_edge_rate": ner.astype(float), "n_comm_W3": ncomm, "participation": part, "NOV_res": nov_res,
           "ego_density_W3": dens, "edge_persistence": ep, "M": M.astype(float), "deg_W1": n1.astype(float),
           "deg_W3": n3.astype(float), "e_W3": e, "nc_W1": nc[1], "nc_W2": nc[2], "nc_W3": nc[3]}
    if return_sets:
        out["NB"] = NB
    if return_counts:
        out["cnt"] = cnt
    return out


# ----------------------------------------------------------------------------- resampling label generators
def rarefy_labels(lab: np.ndarray, n: int, D: int, rng: np.random.Generator) -> np.ndarray:
    """Exactly n papers per W-year (without replacement) and min(|PRE|, 3n) PRE papers; others dropped."""
    P = len(lab)
    key = rng.random((D, P))
    L = np.full((D, P), -1, np.int8)
    for w in range(4):
        idx = np.nonzero(lab == w)[0]
        if not len(idx):
            continue
        q = min(len(idx), 3 * n) if w == 0 else n
        r = np.argsort(key[:, idx], axis=1)[:, :q]
        rows = np.repeat(np.arange(D), q)
        L[rows, idx[r.ravel()]] = w
    return L


def permute_labels(lab: np.ndarray, D: int, rng: np.random.Generator) -> np.ndarray:
    """Permute the W1..W3 labels among the W papers (yearly counts preserved); PRE fixed; dropped stay dropped."""
    idx = np.nonzero(lab >= 1)[0]
    L = np.broadcast_to(lab, (D, len(lab))).copy()
    if len(idx) > 1:
        perm = np.argsort(rng.random((D, len(idx))), axis=1)
        L[:, idx] = lab[idx][perm]
    return L


def half_split(lab: np.ndarray, S: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """S random split-halves within each window (PRE, W1, W2, W3); odd windows give the extra paper at random.
    Returns (LA, LB): S x P label arrays (papers of the other half dropped)."""
    P = len(lab)
    LA = np.full((S, P), -1, np.int8)
    LB = np.full((S, P), -1, np.int8)
    for w in range(4):
        idx = np.nonzero(lab == w)[0]
        n = len(idx)
        if not n:
            continue
        r = np.argsort(rng.random((S, n)), axis=1)
        na = n // 2 + (rng.random(S) < 0.5).astype(int) * (n % 2)
        inA = np.arange(n)[None, :] < na[:, None]
        rows = np.repeat(np.arange(S), n)
        cols = idx[r.ravel()]
        a = inA.ravel()
        LA[rows[a], cols[a]] = w
        LB[rows[~a], cols[~a]] = w
    return LA, LB


# ----------------------------------------------------------------------------- Chao et al. 2005 abundance Jaccard
def chao_jaccard(x: np.ndarray, y: np.ndarray) -> float:
    """Chao, Chazdon, Colwell & Shen (2005, Ecol Lett 8:148) abundance-based Jaccard with the unseen-shared-species
    correction; bias-corrected f2 = 0 form. x, y: count vectors on a common support."""
    n1, n2 = float(x.sum()), float(y.sum())
    if n1 <= 0 or n2 <= 0:
        return float("nan")
    Dm = (x > 0) & (y > 0)
    if not Dm.any():
        return 0.0
    f_p1 = float(((y == 1) & Dm).sum())   # shared species seen once in sample 2
    f_p2 = float(((y == 2) & Dm).sum())
    f_1p = float(((x == 1) & Dm).sum())
    f_2p = float(((x == 2) & Dm).sum())
    r2 = f_p1 / (2 * f_p2) if f_p2 > 0 else f_p1 * (f_p1 - 1) / 2 / max(f_p1, 1.0) if f_p1 > 0 else 0.0
    r1 = f_1p / (2 * f_2p) if f_2p > 0 else f_1p * (f_1p - 1) / 2 / max(f_1p, 1.0) if f_1p > 0 else 0.0
    # r = f1^2 / (2 f2) -> f1 / (2 f2) multiplies f1-weighted sum below; bias-corrected: f1 (f1 - 1) / 2 over f1
    U = x[Dm].sum() / n1 + ((n2 - 1) / n2) * r2 * x[Dm & (y == 1)].sum() / n1
    V = y[Dm].sum() / n2 + ((n1 - 1) / n1) * r1 * y[Dm & (x == 1)].sum() / n2
    U, V = min(U, 1.0), min(V, 1.0)
    den = U + V - U * V
    return float(U * V / den) if den > 0 else float("nan")
