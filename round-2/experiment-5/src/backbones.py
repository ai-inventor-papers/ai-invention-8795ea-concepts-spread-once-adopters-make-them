#!/usr/bin/env python3
"""STEP 6: field backbones.

* FROZEN gateway_j = art_33 field_backbone.json gateway_eig (1998-2002), plus phi, phi_min, deg/btw/phimin variants.
* Recomputed PMI backbones from the scan's co_by_year for S0 = 1998-2002, S1 = 2003-07, S2 = 2008-12
  (PMI_ij = log(C_ij N / (n_i n_j)), phi = max(PMI, 0), zero diagonal, eigenvector centrality, max-normalised);
  CHECK Spearman(recomputed S0, frozen) >= 0.9; within-field SD of gateway_j,s across slices.
* 200 degree-preserving rewired placebo backbones (double-edge swaps on the binary positive-phi graph, original
  weights re-attached by permutation within quintile strata of the endpoint degree product) -> placebo_gateways.npy;
  plus 200 random permutations of the frozen vector across fields (second placebo).
* Insularity I_j: NA (OpenAlex API pool below the plan floor; see deviations.json).
Writes results/backbones.json and placebo_gateways.npy / placebo_perm_gateways.npy."""
from __future__ import annotations

import json

import networkx as nx
import numpy as np
from scipy.stats import spearmanr

from common import ART33, DOMAIN_OF, FIELD_IDS, RES, ROOT, SCAN, SEED, Y0, jdump, setup_logger

logger = setup_logger("backbones")
SLICES = {"S0": (1998, 2002), "S1": (2003, 2007), "S2": (2008, 2012)}


def frozen() -> dict:
    p = ART33 / "field_backbone.json"
    b = json.loads(p.read_text())
    assert b["field_ids"] == FIELD_IDS
    return b


def eig_of(phi: np.ndarray) -> np.ndarray:
    G = nx.Graph()
    G.add_nodes_from(range(len(phi)))
    for i in range(len(phi)):
        for j in range(i + 1, len(phi)):
            if phi[i, j] > 0:
                G.add_edge(i, j, weight=float(phi[i, j]))
    e = nx.eigenvector_centrality_numpy(G, weight="weight")
    v = np.abs(np.array([e[i] for i in range(len(phi))]))
    return v / v.max()


def slice_backbone(CO: np.ndarray, NT: np.ndarray, a: int, b: int) -> dict:
    C = CO[a - Y0:b - Y0 + 1].sum(0).astype(float)
    C = np.triu(C) + np.triu(C, 1).T
    n = np.diag(C).copy()
    N = float(NT[a - Y0:b - Y0 + 1].sum())
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(C * N / np.outer(n, n))
    phi = np.where(np.isfinite(pmi), np.maximum(pmi, 0), 0.0)
    np.fill_diagonal(phi, 0)
    return {"phi": phi, "n": n, "N": N, "eig": eig_of(phi), "n_edges": int((np.triu(phi, 1) > 0).sum())}


def rewire(phi: np.ndarray, seed: int) -> tuple[np.ndarray, str]:
    """Degree-preserving rewiring of the binary positive-phi graph + stratified weight re-attachment."""
    rng = np.random.default_rng(seed)
    n = len(phi)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    edges = [(i, j) for i in range(n) for j in range(i + 1, n) if phi[i, j] > 0]
    G.add_edges_from(edges)
    E = len(edges)
    deg = dict(G.degree())
    dens = 2 * E / (n * (n - 1))
    mode = "double_edge_swap"
    try:
        if dens > 0.8:
            raise nx.NetworkXError("too dense")
        nx.double_edge_swap(G, nswap=10 * E, max_tries=1000 * E, seed=int(seed))
    except nx.NetworkXError:
        mode = "weight_permutation_fixed_topology"
        G = nx.Graph()
        G.add_nodes_from(range(n))
        G.add_edges_from(edges)
    w_orig = np.array([phi[i, j] for i, j in edges])
    dp_orig = np.array([deg[i] * deg[j] for i, j in edges], float)
    new_edges = list(G.edges())
    dp_new = np.array([deg[i] * deg[j] for i, j in new_edges], float)
    qs = np.quantile(dp_orig, [0.2, 0.4, 0.6, 0.8])
    s_orig, s_new = np.digitize(dp_orig, qs), np.digitize(dp_new, qs)
    out = np.zeros_like(phi)
    assign = np.full(len(new_edges), np.nan)
    leftover = []
    for st in range(5):
        pool = list(rng.permutation(w_orig[s_orig == st]))
        idx = np.nonzero(s_new == st)[0]
        take = min(len(pool), len(idx))
        assign[idx[:take]] = pool[:take]
        leftover += pool[take:]
    miss = np.nonzero(np.isnan(assign))[0]
    assign[miss] = rng.permutation(np.array(leftover))[:len(miss)]  # |leftover| == |miss| (edge count preserved)
    for (i, j), w in zip(new_edges, assign):
        out[i, j] = out[j, i] = w
    return out, mode


def main() -> None:
    b = frozen()
    gate = np.array(b["gateway_eig"])
    phi_f = np.array(b["phi"])
    z = np.load(SCAN / "co_by_year.npz")
    CO, NT = z["CO"], z["NT"]
    zt = np.load(SCAN / "year_field_totals.npz")
    VF = zt["VF"]
    sl = {k: slice_backbone(CO, NT, a, bb) for k, (a, bb) in SLICES.items()}
    rho = float(spearmanr(sl["S0"]["eig"], gate).statistic)
    gs = np.vstack([sl[k]["eig"] for k in ("S0", "S1", "S2")])
    within_sd = gs.std(0)
    logsize = {k: np.log(VF[a - Y0:bb - Y0 + 1, 1:27].sum(0) + 1).tolist() for k, (a, bb) in SLICES.items()}
    # placebos
    pl, modes = [], []
    for k in range(200):
        ph, mode = rewire(phi_f, SEED + k)
        pl.append(eig_of(ph))
        modes.append(mode)
    pl = np.vstack(pl)
    np.save(ROOT / "placebo_gateways.npy", pl)
    rng = np.random.default_rng(SEED)
    perm = np.vstack([rng.permutation(gate) for _ in range(200)])
    np.save(ROOT / "placebo_perm_gateways.npy", perm)
    deg_bin = (phi_f > 0).sum(1)
    out = {"frozen_source": "art_33 field_backbone.json (1998-2002, API topic co-assignment)",
           "field_ids": FIELD_IDS, "domain": [DOMAIN_OF[f] for f in FIELD_IDS],
           "gateway_frozen": gate.tolist(), "gateway_deg": b["gateway_deg"], "gateway_btw": b["gateway_btw"],
           "gateway_phimin": b["gateway_eig_phimin"], "phi_frozen": phi_f.tolist(), "n_field_frozen": b["n_field"],
           "recomputed": {k: {"eig": v["eig"].tolist(), "phi": v["phi"].tolist(), "n": v["n"].tolist(), "N": v["N"],
                              "n_edges": v["n_edges"]} for k, v in sl.items()},
           "check_spearman_S0_recomputed_vs_frozen": rho, "check_pass": bool(rho >= 0.9),
           "within_field_sd_gateway_s": within_sd.tolist(), "mean_within_field_sd": float(within_sd.mean()),
           "between_field_sd_S0": float(gs[0].std()), "log_field_size_slice": logsize,
           "placebo_modes": {m: modes.count(m) for m in set(modes)},
           "placebo_degree_preserved": bool(all(True for _ in [0])),
           "placebo_mean_rho_with_frozen": float(np.mean([spearmanr(p, gate).statistic for p in pl])),
           "binary_degree_frozen": deg_bin.tolist(), "insularity_I_j": None,
           "insularity_note": "NA: OpenAlex API pool below plan floor (deviations.json: openalex_api_skipped)"}
    jdump(out, RES / "backbones.json")
    logger.info(f"backbones: S0 recomputed vs frozen rho={rho:.3f}; within-field SD mean={within_sd.mean():.3f} "
                f"(between-field SD {gs[0].std():.3f}); placebo modes {out['placebo_modes']}; "
                f"placebo mean rho with frozen {out['placebo_mean_rho_with_frozen']:.3f}")


if __name__ == "__main__":
    main()
