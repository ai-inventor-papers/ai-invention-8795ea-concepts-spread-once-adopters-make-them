"""Yearly (1-year window) co-occurrence ego-network statistics, built from the EXP8 lib/ego.py primitives
(neighbours, pmi, bg_window, self_topics, slice_of) on the EXP3 Leiden-gamma-3 backbone. NO betweenness.

For concept c and calendar year t (t0 <= t <= h_end) and a paper set P (HOME = grounded works in the concept's home
venue fields; ALL = all grounded works):
  NB(t)      = ego.neighbours(counts_P[t], n_P[t], bg[t], GT[t], SELF, min_n)        (PMI > 0 and count >= min_n)
  SEEN(t)    = topics with >= 1 count in P over t0-3..t-1
  NEW(t)     = NB(t) & ~SEEN(t)
  new_rate   = |NEW(t)| / (|NB(t-1)| + 1)
  n_comm     = # distinct comm[s(t)] labels among NB(t)
  participation = 1 - sum_c w_c^2, w_c = count-weighted share of NB(t) in community c (comm[s(t)])
  nov_res    = share of NEW(t) outside C0_s (the modal comm[s(t)] community of the concept's t0 papers) minus the
               backbone-degree-weighted share of the pool (bg[t] > 0, ~SEEN, ~SELF) outside C0_s
  density    = # full backbone edges of slice s(t) among NB(t) / C(|NB(t)|, 2)            (NA if |NB(t)| < 2)
  dens_null  = mean density of N_NULL topic sets of size |NB(t)| drawn without replacement with bg[t]-proportional
               weights from the non-SELF pool (Gumbel top-k, as ego.distinct_null); dens_adj = density - dens_null
  persistence= Jaccard(NB(t-1), NB(t))
  deg        = |NB(t)|;  kcore = coreness of the concept node inserted into the kNN graph of slice s(t)
SELF is frozen once per concept exactly as EXP8 (ego.self_topics on ALL papers over t0..t0+2).
Years >= 2015 use slice 2 (2010-14) -- `clamped` flags them.

The same pass also returns the EXP8 static (t0..t0+2, ALL papers) port quantities and the static new-partner list
for the partner-source decomposition (step 6)."""
from __future__ import annotations

import math
import warnings
from collections import Counter

import igraph as ig
import numpy as np
import scipy.sparse as sp

import ego

N_NULL = 100
_ADJ: dict = {}


def adjacency(s: int) -> sp.csr_matrix:
    if s not in _ADJ:
        a, b = ego.C["full_edges"][s]
        nt = ego.C["nt"]
        A = sp.coo_matrix((np.ones(len(a) * 2), (np.r_[a, b], np.r_[b, a])), shape=(nt, nt)).tocsr()
        A.data[:] = 1.0
        A.sum_duplicates()
        A.data = np.minimum(A.data, 1.0)
        _ADJ[s] = A
    return _ADJ[s]


def density_of(idx: np.ndarray, s: int) -> float:
    m = len(idx)
    if m < 2:
        return float("nan")
    A = adjacency(s)
    e = A[idx][:, idx].sum() / 2.0
    return float(e / (m * (m - 1) / 2.0))


def density_null(M: int, pool: np.ndarray, w: np.ndarray, s: int, rng: np.random.Generator,
                 n: int = N_NULL) -> float:
    """Mean density of n bg-weighted random topic sets of size M from `pool` (Gumbel top-k, no replacement)."""
    if M < 2 or len(pool) < M:
        return float("nan")
    lw = np.log(w[pool])
    g = lw[None, :] + rng.gumbel(size=(n, len(pool)))
    top = np.argpartition(-g, M - 1, axis=1)[:, :M]
    idx = pool[top]                                            # [n, M]
    rows = np.repeat(np.arange(n), M)
    X = sp.csr_matrix((np.ones(n * M), (rows, idx.ravel())), shape=(n, ego.C["nt"]))
    E = np.asarray((X @ adjacency(s)).multiply(X).sum(1)).ravel() / 2.0
    return float(np.mean(E / (M * (M - 1) / 2.0)))


def kcore_of(idx: np.ndarray, s: int) -> int:
    if len(idx) == 0:
        return 0
    g = ego.knn_graph(s).copy()
    g.add_vertices(1)
    v = g.vcount() - 1
    g.add_edges([(v, int(k)) for k in idx])
    return int(g.coreness()[v])


def _counts(years: np.ndarray, t_off: np.ndarray, tflat: np.ndarray, mask: np.ndarray, Y: np.ndarray,
            nt: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """counts [len(Y), nt], works-with-topics per year [len(Y)], all works per year [len(Y)] for rows in mask."""
    ny = len(Y)
    yi = years - Y[0]
    ok = mask & (yi >= 0) & (yi < ny)
    ln = np.diff(t_off)
    rows = np.repeat(np.arange(len(years)), ln)
    sel = ok[rows]
    cnt = np.bincount(yi[rows[sel]] * nt + tflat[sel], minlength=ny * nt).reshape(ny, nt).astype(float)
    ncw = np.bincount(yi[ok & (ln > 0)], minlength=ny).astype(float)
    nall = np.bincount(yi[ok], minlength=ny).astype(float)
    return cnt, ncw, nall


def _modal(counts: np.ndarray, labels: np.ndarray):
    nz = np.nonzero(counts)[0]
    if len(nz) == 0:
        return None
    cs = Counter()
    for k in nz:
        cs[labels[k]] += counts[k]
    return cs.most_common(1)[0][0]


def _jac(a: np.ndarray, b: np.ndarray) -> float:
    u = (a | b).sum()
    return float((a & b).sum() / u) if u else float("nan")


def _part(nb: np.ndarray, cnt: np.ndarray, labels: np.ndarray) -> tuple[float, int]:
    idx = np.nonzero(nb)[0]
    if len(idx) == 0:
        return float("nan"), 0
    ws = Counter()
    for k in idx:
        ws[labels[k]] += cnt[k]
    tot = sum(ws.values())
    pw = np.array([v / tot for v in ws.values()])
    return float(1 - (pw ** 2).sum()), len(ws)


def concept_yearly(*, ci: int, name: str, aliases: list[str], t0: int, h_end: int, years: np.ndarray,
                   vfield: np.ndarray, t_off: np.ndarray, tflat: np.ndarray, home_codes: set[int], min_n: int,
                   seed: int, do_null: bool = True, do_kcore: bool = True) -> tuple[list[dict], dict, list[dict]]:
    """Returns (yearly rows, static port/partner record, static new-partner rows)."""
    C = ego.C
    nt = C["nt"]
    rng = np.random.default_rng(seed)
    Y = np.arange(t0 - 3, h_end + 1)
    is_home = np.isin(vfield, list(home_codes))
    allm = np.ones(len(years), bool)
    cH, ncH, nH = _counts(years, t_off, tflat, is_home, Y, nt)
    cA, ncA, nA = _counts(years, t_off, tflat, allm, Y, nt)
    iy = {int(y): i for i, y in enumerate(Y)}
    early = [t0, t0 + 1, t0 + 2]
    e_idx = [iy[y] for y in early if y in iy]
    SELF = ego.self_topics(name, aliases, cA[e_idx].sum(0), float(ncA[e_idx].sum()))
    NB_H, NB_A, P_A = {}, {}, {}
    for y in range(t0 - 1, h_end + 1):
        i = iy[y]
        bgw, N = ego.bg_window([y])
        NB_H[y], _ = ego.neighbours(cH[i], ncH[i], bgw, N, SELF, min_n)
        NB_A[y], P_A[y] = ego.neighbours(cA[i], ncA[i], bgw, N, SELF, 2)
    seenH = np.cumsum(cH, 0)
    seenA = np.cumsum(cA, 0)
    c0H = cH[iy[t0]] if cH[iy[t0]].sum() > 0 else cA[iy[t0]]
    C0 = [_modal(c0H, C["comm"][s]) for s in range(3)]
    rows = []
    for t in range(t0, h_end + 1):
        i = iy[t]
        s = ego.slice_of(t)
        comm = C["comm"][s]
        nb, nbp = NB_H[t], NB_H[t - 1]
        seen = seenH[i - 1] >= 1
        new = nb & ~seen
        deg = int(nb.sum())
        idx = np.nonzero(nb)[0]
        r = {"ci": ci, "year": t, "age": t - t0, "slice": s, "clamped": int(t >= 2015),
             "n_home_works": float(nH[i]), "n_all_works": float(nA[i]), "n_home_topic_works": float(ncH[i]),
             "home_cov": float(nH[i] / nA[i]) if nA[i] > 0 else float("nan"),
             "deg": deg, "n_new": int(new.sum()), "new_rate": float(new.sum() / (nbp.sum() + 1))}
        r["participation"], r["n_comm"] = _part(nb, cH[i], comm)
        bgw, _ = ego.bg_window([t])
        new_idx = np.nonzero(new)[0]
        if len(new_idx) and C0[s] is not None:
            pool = np.nonzero((bgw > 0) & ~seen & ~SELF)[0]
            dg = C["deg"][s][pool].astype(float)
            E = dg[comm[pool] != C0[s]].sum() / dg.sum() if dg.sum() > 0 else float("nan")
            r["nov_res"] = float(np.mean(comm[new_idx] != C0[s]) - E)
        else:
            r["nov_res"] = float("nan")
        r["density"] = density_of(idx, s)
        if do_null and deg >= 2:
            pool = np.nonzero((bgw > 0) & ~SELF)[0]
            r["dens_null"] = density_null(deg, pool, bgw, s, rng)
        else:
            r["dens_null"] = float("nan")
        r["dens_adj"] = r["density"] - r["dens_null"]
        r["persistence"] = _jac(nbp, nb)
        r["kcore"] = kcore_of(idx, s) if do_kcore else -1
        # ALL-PAPERS comparison build
        nbA = NB_A[t]
        r["deg_all"] = int(nbA.sum())
        r["density_all"] = density_of(np.nonzero(nbA)[0], s)
        r["new_rate_all"] = float((nbA & ~(seenA[i - 1] >= 1)).sum() / (NB_A[t - 1].sum() + 1))
        rows.append(r)
    # ---------------- EXP8 static port (ALL papers, windows PRE = t0-3..t0-1, W1..W3 = t0, t0+1, t0+2)
    pre = seenA[iy[t0] - 1] >= 1
    W = [NB_A[y] for y in early if y <= h_end]
    port = {"ci": ci}
    if len(W) == 3:
        newS = (W[0] | W[1] | W[2]) & ~pre
        n1 = W[0].sum()
        port["p_new_edge_rate"] = float((newS.sum() / 3.0) / (n1 + 1))
        s4 = ego.slice_of(t0 + 2)
        port["p_participation"], port["p_n_comm_W3"] = _part(W[2], cA[iy[t0 + 2]], C["comm"][s4])
        if W[2].sum() == 0:
            port["p_n_comm_W3"] = 0
        port["p_ego_density_W3"] = density_of(np.nonzero(W[2])[0], s4)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            port["p_edge_persistence"] = float(np.nanmean([_jac(W[0], W[1]), _jac(W[1], W[2])]))
        # static new partners (EXP8 definition) for the partner-source decomposition
        new_idx = np.nonzero(newS)[0]
        s0 = ego.slice_of(t0)
        C0s = _modal(cA[iy[t0]], C["comm"][s0])
        prt = []
        for k in new_idx:
            fy = next((y for y in early if cA[iy[y]][k] >= 1), t0)
            prt.append({"ci": ci, "topic": int(k), "first_year": int(fy),
                        "comm_new": int(C0s is not None and C["comm"][ego.slice_of(fy)][k] != C0s),
                        "in_W3": int(W[2][k]), "cnt_W3": float(cA[iy[t0 + 2]][k])})
        port["C0_static"] = -1 if C0s is None else int(C0s)
        port["n1_static"] = int(n1)
        port["w3_comms"] = {int(k): int(C["comm"][s4][k]) for k in np.nonzero(W[2])[0]}
    else:
        prt = []
    return rows, port, prt
