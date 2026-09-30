#!/usr/bin/env python3
"""Knowledge-network backbone: OpenAlex topics (4,516 nodes) linked by full-corpus co-occurrence PMI.

For each slice (2000-04, 2005-09, 2010-14): c_kl = # base works carrying topics k and l, c_k = # base works
with k, W = # base works with >= 1 topic; PMI_kl = log(c_kl W / (c_k c_l)); keep c_kl >= 3 and PMI > 0.
Leiden (RBConfiguration, PMI weights): resolution gamma chosen on 2000-04 from {0.25..3} x 10 seeds by the
median standard modularity, then FROZEN; best-Q partition of 10 seeds per slice. Communities of size < 3
inherit the plurality community of their OpenAlex subfield. Slices are aligned one-to-one by greedy Jaccard
matching (>= 0.3, else a new id). A kNN-sparsified copy (top-10 PMI edges per node) is kept for centrality.
Writes backbone/*.npz, results/topic_communities.csv, results/backbone_summary.json."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

import igraph as ig
import leidenalg as la
import numpy as np
import pandas as pd
from loguru import logger

from common import load_scan_aggregates
from config import LOGS, RES, ROOT, SEED, SLICES

BB = ROOT / "backbone"
BB.mkdir(exist_ok=True)
GAMMAS = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]
MIN_COMM = 20  # deviation (fixed before any outcome was seen): primary gamma needs >= 20 non-trivial communities
N_SEEDS = 10
KNN = 10


def slice_edges(s: int, bg, pairs, Gt, years, nt):
    ya, yb = SLICES[s]
    yi = [years.index(y) for y in range(ya, yb + 1)]
    ck = bg[yi].sum(axis=0).astype(float)
    W = float(sum(Gt[y] for y in range(ya, yb + 1)))
    keys, cnt = pairs[s]
    a, b = keys // nt, keys % nt
    c = cnt.astype(float)
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(c * W / (ck[a] * ck[b]))
    keep = (c >= 3) & (pmi > 0) & np.isfinite(pmi)
    return a[keep].astype(np.int32), b[keep].astype(np.int32), pmi[keep].astype(np.float32), c[keep].astype(
        np.int32), ck, W


def leiden_runs(g: ig.Graph, gamma: float, seeds) -> list[tuple[float, list[int]]]:
    out = []
    for sd in seeds:
        p = la.find_partition(g, la.RBConfigurationVertexPartition, weights="weight", resolution_parameter=gamma,
                              seed=int(sd), n_iterations=-1)
        memb = list(p.membership)
        q = g.modularity(memb, weights="weight")
        out.append((q, memb))
    return out


def fix_small(memb: list[int], subfield: np.ndarray, present: np.ndarray) -> np.ndarray:
    """Topics isolated/absent or in communities of size < 3 -> plurality community of their subfield."""
    memb = np.asarray(memb)
    size = Counter(memb[present].tolist())
    ok = present & np.array([size.get(m, 0) >= 3 for m in memb])
    out = memb.copy()
    by_sf = defaultdict(Counter)
    for k in np.nonzero(ok)[0]:
        by_sf[subfield[k]][memb[k]] += 1
    nxt = memb.max() + 1
    n_inh = n_single = 0
    for k in np.nonzero(~ok)[0]:
        if by_sf[subfield[k]]:
            out[k] = by_sf[subfield[k]].most_common(1)[0][0]
            n_inh += 1
        else:
            out[k] = nxt
            nxt += 1
            n_single += 1
    return out, n_inh, n_single


def align(prev: np.ndarray, cur: np.ndarray, next_id: int) -> tuple[np.ndarray, list[float], int]:
    """Greedy one-to-one Jaccard matching of cur communities onto prev ids (>= 0.3), else new ids."""
    P = defaultdict(set)
    C = defaultdict(set)
    for k, (p, c) in enumerate(zip(prev, cur)):
        P[p].add(k)
        C[c].add(k)
    cand = []
    for c, sc in C.items():
        overlap = Counter(prev[list(sc)].tolist())
        for p, inter in overlap.items():
            j = inter / len(sc | P[p])
            if j >= 0.3:
                cand.append((j, c, p))
    cand.sort(reverse=True)
    mc, mp = {}, set()
    jac = []
    for j, c, p in cand:
        if c in mc or p in mp:
            continue
        mc[c] = p
        mp.add(p)
        jac.append(j)
    out = np.empty_like(cur)
    for c in C:
        if c not in mc:
            mc[c] = next_id
            next_id += 1
    for k, c in enumerate(cur):
        out[k] = mc[c]
    return out, jac, next_id


def knn_sparsify(nt: int, a, b, w, k: int = KNN):
    """Union of each node's top-k PMI edges."""
    src = np.concatenate([a, b])
    dst = np.concatenate([b, a])
    ww = np.concatenate([w, w])
    order = np.lexsort((-ww, src))
    src, dst, ww = src[order], dst[order], ww[order]
    first = np.searchsorted(src, np.arange(nt))
    rank = np.arange(len(src)) - first[src]
    sel = rank < k
    ea, eb = np.minimum(src[sel], dst[sel]), np.maximum(src[sel], dst[sel])
    key = np.unique(ea.astype(np.int64) * nt + eb)
    return (key // nt).astype(np.int32), (key % nt).astype(np.int32)


@logger.catch(reraise=True)
def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "backbone.log", rotation="30 MB", level="DEBUG")
    tids, G, Gt, bg, pairs, nt, years = load_scan_aggregates()
    tm = pd.read_csv(RES / "topic_meta.csv").set_index("topic").loc[tids]
    subfield = tm.subfield.to_numpy()
    rng = np.random.default_rng(SEED)
    summary = {"n_topics": nt, "slices": []}
    gamma = None
    comms, comms_q = [], []
    next_id = next_q = 0
    gamma_q = None
    for s in range(len(SLICES)):
        a, b, w, c, ck, W = slice_edges(s, bg, pairs, Gt, years, nt)
        g = ig.Graph(n=nt, edges=list(zip(a.tolist(), b.tolist())), directed=False)
        g.es["weight"] = w.astype(float).tolist()
        present = np.array(g.degree()) > 0
        comp = g.connected_components()
        giant = max(comp.sizes()) if len(comp) else 0
        info = {"slice": SLICES[s], "W_works_with_topics": W, "n_edges": int(len(a)), "n_nodes_with_edges": int(present.sum()),
                "giant_component_share": giant / nt, "median_pmi": float(np.median(w)) if len(w) else None,
                "mean_degree": float(2 * len(a) / max(present.sum(), 1))}
        seeds = rng.integers(0, 2**31 - 1, N_SEEDS)
        if gamma is None:
            grid = {}
            for gm in GAMMAS:
                runs = leiden_runs(g, gm, seeds)
                qs = [q for q, _ in runs]
                ntriv = [sum(1 for v in Counter(m).values() if v >= 3) for _, m in runs]
                grid[gm] = {"median_Q": float(np.median(qs)), "n_comm_median": float(np.median([len(set(m)) for _, m in runs])),
                            "n_comm_ge3_median": float(np.median(ntriv))}
                logger.info(f"slice {SLICES[s]} gamma={gm}: median Q={grid[gm]['median_Q']:.4f} "
                            f"#comm={grid[gm]['n_comm_median']}")
            gamma_q = max(grid, key=lambda k: grid[k]["median_Q"])  # plan rule (reported variant D_q)
            elig = [k for k in grid if grid[k]["n_comm_ge3_median"] >= MIN_COMM]
            gamma = max(elig, key=lambda k: grid[k]["median_Q"]) if elig else gamma_q
            summary["gamma_grid"] = grid
            summary["gamma"] = gamma
            summary["gamma_plan_rule"] = gamma_q
        # primary partition
        runs = leiden_runs(g, gamma, seeds)
        q, memb = max(runs, key=lambda t: t[0])
        fixed, n_inh, n_single = fix_small(memb, subfield, present)
        # plan-rule partition (coarse variant)
        runs_q = runs if gamma_q == gamma else leiden_runs(g, gamma_q, seeds)
        fixed_q, _, _ = fix_small(max(runs_q, key=lambda t: t[0])[1], subfield, present)
        if s == 0:
            aligned = np.unique(fixed, return_inverse=True)[1]
            next_id = int(aligned.max()) + 1
            aligned_q = np.unique(fixed_q, return_inverse=True)[1]
            next_q = int(aligned_q.max()) + 1
            jac = []
        else:
            aligned, jac, next_id = align(comms[-1], fixed, next_id)
            aligned_q, _, next_q = align(comms_q[-1], fixed_q, next_q)
        comms.append(aligned)
        comms_q.append(aligned_q)
        sizes = Counter(aligned.tolist())
        info.update(Q=q, n_comm=len(sizes), n_comm_plan_rule=len(set(aligned_q.tolist())), n_comm_ge3=sum(1 for v in sizes.values() if v >= 3),
                    n_inherited=n_inh, n_singleton=n_single,
                    align_jaccard_median=float(np.median(jac)) if jac else None,
                    align_n_matched=len(jac), comm_size_median=float(np.median(list(sizes.values()))))
        ka, kb = knn_sparsify(nt, a, b, w)
        deg = np.bincount(np.concatenate([a, b]), minlength=nt)
        np.savez_compressed(BB / f"slice{s}.npz", a=a, b=b, w=w, c=c, ck=ck, W=np.array(W), ka=ka, kb=kb, deg=deg,
                            comm=aligned, comm_q=aligned_q)
        info["knn_edges"] = int(len(ka))
        summary["slices"].append(info)
        logger.info(f"slice {SLICES[s]}: {info}")
    df = pd.DataFrame({"topic": tids, "name": tm.name.values, "subfield": subfield, "field": tm.field.values,
                       "comm_s0": comms[0], "comm_s1": comms[1], "comm_s2": comms[2],
                       "commq_s0": comms_q[0], "commq_s1": comms_q[1], "commq_s2": comms_q[2]})
    df.to_csv(RES / "topic_communities.csv", index=False)
    (RES / "backbone_summary.json").write_text(json.dumps(summary, indent=1, default=float))
    logger.info(f"gamma frozen at {gamma}")


if __name__ == "__main__":
    main()
