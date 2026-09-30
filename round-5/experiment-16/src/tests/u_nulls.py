#!/usr/bin/env python3
"""U3 curveball uniformity on an enumerable toy + margin preservation; U4 rewire null calibration:
z of edge counts inside random topic sets, where the 'observed' graph is itself one degree-preserving rewire of
slice 0 and the null is formed by further independent rewires of the original -> mean z ~ 0 (|mean| < 0.15).
-> results/unit_tests_nulls.json"""
from __future__ import annotations

import itertools
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np
from scipy import stats

from common import INPUTS, RES, jdump, setup_logger
from nullkern import _trade


def toy_curveball(n_samples: int = 30000) -> dict:
    # 3 rows x 4 columns, row sums (2, 2, 1), column sums (2, 1, 1, 1)
    rows = [np.array([0, 1], np.int32), np.array([0, 2], np.int32), np.array([3], np.int32)]
    r_s, c_s = [2, 2, 1], [2, 1, 1, 1]
    states = []
    for bits in itertools.product([0, 1], repeat=12):
        M = np.array(bits).reshape(3, 4)
        if list(M.sum(1)) == r_s and list(M.sum(0)) == c_s:
            states.append(tuple(bits))
    sidx = {s: i for i, s in enumerate(states)}
    data = np.concatenate(rows).astype(np.int32)
    off = np.array([0, 2, 4, 5], np.int64)
    mark = np.zeros(5, np.int64)
    pool = np.empty(8, np.int32)
    np.random.seed(3)
    from numba import njit

    @njit
    def seed(s):
        np.random.seed(s)
    seed(3)
    stamp = 1
    rng = np.random.default_rng(4)
    counts = np.zeros(len(states))
    for t in range(n_samples * 3):
        i, j = rng.choice(3, 2, replace=False)
        _trade(data, off, i, j, mark, stamp, pool)
        stamp += 2
        if t % 3 == 2:
            M = np.zeros((3, 4), int)
            for r in range(3):
                M[r, data[off[r]:off[r + 1]]] = 1
            assert list(M.sum(1)) == r_s and list(M.sum(0)) == c_s
            counts[sidx[tuple(M.ravel())]] += 1
    chi = stats.chisquare(counts)
    return {"n_states": len(states), "freq": counts.tolist(), "chi2_p": float(chi.pvalue),
            "pass": bool(chi.pvalue > 0.01)}


def rewire_calibration(n_obs: int = 10, n_null: int = 40, n_sets: int = 20, k: int = 12) -> dict:
    """n_obs independent 'observed' rewires (each exchangeable with the null draws) x n_sets random topic sets;
    z against n_null further rewires of the original; mean z over all (graph-clustered SE reported)."""
    import igraph as ig
    z = np.load(INPUTS / "backbone" / "slice0.npz")
    nt = 4516
    G0 = ig.Graph(n=nt, edges=np.c_[z["a"], z["b"]].tolist())
    deg0 = np.array(G0.degree())

    def rewired(seed):
        random.seed(seed)
        ig.set_random_number_generator(random)
        g = G0.copy()
        g.rewire(n=10 * g.ecount(), allowed_edge_types="simple")
        el = np.array(g.get_edgelist())
        A = np.zeros((nt, nt), bool)
        A[el[:, 0], el[:, 1]] = True
        A[el[:, 1], el[:, 0]] = True
        return A, g
    rng = np.random.default_rng(7)
    sets = [[rng.choice(nt, k, replace=False) for _ in range(n_sets)] for _ in range(n_obs)]
    iu, ju = np.triu_indices(k, 1)
    obs = np.zeros((n_obs, n_sets))
    simple, degok = True, True
    for o in range(n_obs):
        A, g = rewired(999 + o)
        simple &= bool(g.is_simple())
        degok &= bool(np.array_equal(np.array(g.degree()), deg0))
        obs[o] = [A[s[iu], s[ju]].sum() for s in sets[o]]
    null = np.zeros((n_null, n_obs, n_sets))
    for d in range(n_null):
        A, _ = rewired(5000 + d)
        for o in range(n_obs):
            null[d, o] = [A[s[iu], s[ju]].sum() for s in sets[o]]
    sd = null.std(0)
    zz = np.where(sd > 0, (obs - null.mean(0)) / np.where(sd > 0, sd, 1), np.nan)
    gm = np.nanmean(zz, 1)
    return {"mean_z": float(np.nanmean(zz)), "sd_z": float(np.nanstd(zz)), "graph_means": gm.tolist(),
            "se_mean_graph_clustered": float(np.std(gm, ddof=1) / np.sqrt(n_obs)), "n_obs_graphs": n_obs,
            "n_sets_per_graph": n_sets, "n_null": n_null, "degree_preserved": degok, "simple": simple,
            "pass": bool(abs(np.nanmean(zz)) < 0.15),
            "note": "v1 of this test (one observed rewire x 50 sets, 30 nulls) gave mean z -0.236 (sets share one "
                    "observed graph, so their z are correlated); replaced by this clustered design"}


def main() -> None:
    logger = setup_logger("u_nulls")
    prev = RES / "unit_tests_nulls.json"
    out = json.loads(prev.read_text()) if prev.exists() else {"U3_toy": toy_curveball()}
    if "U3_toy" not in out:
        out["U3_toy"] = toy_curveball()
    logger.info(f"U3 toy: {out['U3_toy']}")
    if "U4_rewire_calibration" in out and "U4_v1_single_graph" not in out:
        out["U4_v1_single_graph"] = out["U4_rewire_calibration"]     # kept: the first (failed) design
    out["U4_rewire_calibration"] = rewire_calibration()
    logger.info(f"U4: {out['U4_rewire_calibration']}")
    jdump(out, RES / "unit_tests_nulls.json")


if __name__ == "__main__":
    main()
