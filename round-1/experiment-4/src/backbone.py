"""Leakage-free 26-field relatedness backbone (SLICE_A = 1998-2002, whole-corpus topic co-assignment) and gateway
centrality. Reads only cached group_by responses (26 + 1 calls)."""
from __future__ import annotations

import json
from pathlib import Path

import networkx as nx
import numpy as np
from loguru import logger

import oa_client as oa

ROOT = Path(__file__).resolve().parent
FIELD_IDS = list(range(11, 37))
SLICE_A = "1998-2002"
DOMAIN_OF = {11: "Life", 13: "Life", 24: "Life", 28: "Life", 30: "Life",
             12: "Social", 14: "Social", 18: "Social", 20: "Social", 32: "Social", 33: "Social",
             15: "Physical", 16: "Physical", 17: "Physical", 19: "Physical", 21: "Physical", 22: "Physical",
             23: "Physical", 25: "Physical", 26: "Physical", 31: "Physical",
             27: "Health", 29: "Health", 34: "Health", 35: "Health", 36: "Health"}


def build() -> dict:
    names: dict[int, str] = {}
    C = np.zeros((26, 26))
    for i, f in enumerate(FIELD_IDS):
        d = oa.get("/works", {"filter": f"topics.field.id:{f},publication_year:{SLICE_A},type:article|review",
                              "group_by": "topics.field.id", "per_page": 200}, f"backbone:A:{f}")
        for g in d["group_by"]:
            fid = int(str(g["key"]).split("/")[-1])
            names[fid] = g["key_display_name"]
            C[i, FIELD_IDS.index(fid)] = g["count"]
    dN = oa.get("/works", {"filter": f"publication_year:{SLICE_A},type:article|review",
                           "group_by": "primary_topic.field.id", "per_page": 200}, "backbone:A:N")
    N = float(sum(g["count"] for g in dN["group_by"]))
    Cs = (C + C.T) / 2  # co-assignment is symmetric up to count drift between calls
    n = np.diag(C).copy()
    with np.errstate(divide="ignore", invalid="ignore"):
        pmi = np.log(Cs * N / np.outer(n, n))
    pmi[~np.isfinite(pmi)] = np.nan
    phi = np.where(np.isnan(pmi), 0.0, np.maximum(pmi, 0.0))
    np.fill_diagonal(phi, 0.0)
    phi_min = Cs / np.maximum.outer(n, n)
    np.fill_diagonal(phi_min, 1.0)
    fields = [names.get(f, str(f)) for f in FIELD_IDS]
    Gr = nx.Graph()
    Gr.add_nodes_from(range(26))
    for i in range(26):
        for j in range(i + 1, 26):
            if phi[i, j] > 0:
                Gr.add_edge(i, j, weight=phi[i, j], dist=1.0 / phi[i, j])
    eig = nx.eigenvector_centrality_numpy(Gr, weight="weight")
    deg = dict(Gr.degree(weight="weight"))
    btw = nx.betweenness_centrality(Gr, weight="dist")
    Gm = nx.Graph()
    for i in range(26):
        for j in range(i + 1, 26):
            Gm.add_edge(i, j, weight=phi_min[i, j])
    eig_min = nx.eigenvector_centrality_numpy(Gm, weight="weight")
    gate = np.array([eig[i] for i in range(26)])
    gate = gate / gate.max()
    cv = float(np.std(gate) / np.mean(gate))
    out = {"slice": SLICE_A, "fields": fields, "field_ids": FIELD_IDS,
           "domain": [DOMAIN_OF[f] for f in FIELD_IDS], "N_works_with_primary_topic": N,
           "n_field": n.tolist(), "cooc": Cs.tolist(), "pmi": np.nan_to_num(pmi, nan=-99).tolist(),
           "phi": phi.tolist(), "phi_min": phi_min.tolist(),
           "gateway_eig": gate.tolist(), "gateway_eig_cv": cv,
           "gateway_deg": (np.array([deg[i] for i in range(26)]) / max(deg.values())).tolist(),
           "gateway_btw": [btw[i] for i in range(26)],
           "gateway_eig_phimin": (np.array([eig_min[i] for i in range(26)]) /
                                  max(eig_min.values())).tolist(),
           "n_positive_edges": Gr.number_of_edges(),
           "not_computed": {"SLICE_B": "skipped (degrade ladder step 5; shared key below floor)",
                            "insularity_I_j": "not computed: shared OpenAlex key fell below the 1,000-credit floor "
                                              "before the insularity stage; INS features are absent",
                            "phi_cit": "not computed (by-product of insularity)"}}
    logger.info(f"backbone: N={N:.0f}, positive edges={Gr.number_of_edges()}, gateway CV={cv:.3f}")
    return out


if __name__ == "__main__":
    b = build()
    order = np.argsort(b["gateway_eig"])[::-1]
    for i in order:
        print(f"{b['fields'][i]:45s} eig={b['gateway_eig'][i]:.3f} deg={b['gateway_deg'][i]:.3f} n={b['n_field'][i]:.0f}")
