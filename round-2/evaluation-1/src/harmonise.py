"""Step 0: input harmonisation of the three iteration-1 field-retention files onto exp4's 26-field backbone."""
from __future__ import annotations

import json
import math
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from lib import ITER1

E1 = ITER1 / "experiment-1/src" / "results"
E3 = ITER1 / "experiment-3/src" / "results"
E4 = ITER1 / "experiment-4/src"
HERE = Path(__file__).resolve().parent
XW = json.loads((HERE / "prereg" / "crosswalk.json").read_text())
G1 = XW["group_harmonisation"]["exp1_dev_group"]
G3 = XW["group_harmonisation"]["exp3"]
M0 = ["b_logn", "b_growth", "b_share"]
B5 = ["b5_logvol", "b5_growth", "b5_offhome", "b5_entropy", "b5_reach"]
REL = ["log_field_size", "phi_home_j", "density_j"]
RIVALS = ["r_strength", "r_degree", "r_betweenness", "r_pagerank", "r_closeness", "r_kcore", "r_eig_phimin",
          "log_field_size"]


class Backbone:
    def __init__(self) -> None:
        b = json.loads((E4 / "field_backbone.json").read_text())
        self.raw = b
        self.fields = b["fields"]
        self.idx = {f: i for i, f in enumerate(self.fields)}
        self.phi = np.array(b["phi"])
        self.phi_min = np.array(b["phi_min"])
        self.n = np.array(b["n_field"], float)
        self.logn = np.log(self.n)
        self.gate = np.array(b["gateway_eig"])
        self.domain = b["domain"]
        self.rivals = self._rivals()

    def graph(self) -> nx.Graph:
        G = nx.Graph()
        G.add_nodes_from(range(26))
        for i in range(26):
            for j in range(i + 1, 26):
                if self.phi[i, j] > 0:
                    G.add_edge(i, j, weight=self.phi[i, j], dist=1.0 / self.phi[i, j])
        return G

    def _rivals(self) -> dict[str, np.ndarray]:
        G = self.graph()
        v = lambda d: np.array([d[i] for i in range(26)], float)  # noqa: E731
        return {"gateway_j": self.gate,
                "r_strength": v(dict(G.degree(weight="weight"))),
                "r_degree": v(dict(G.degree())),
                "r_betweenness": v(nx.betweenness_centrality(G, weight="dist")),
                "r_pagerank": v(nx.pagerank(G, alpha=0.85, weight="weight")),
                "r_closeness": v(nx.closeness_centrality(G, distance="dist")),
                "r_kcore": v(nx.core_number(G)),
                "r_eig_phimin": np.array(self.raw["gateway_eig_phimin"]),
                "log_field_size": self.logn}


def _w_row(bb: Backbone, names: list[str]) -> np.ndarray:
    w = np.zeros(26)
    ii = [bb.idx[n] for n in names]
    w[ii] = bb.n[ii] / bb.n[ii].sum()
    return w


def _attach(df: pd.DataFrame, W: np.ndarray, homes: list[list[int]], bb: Backbone, K: list[set[int]] | None) -> None:
    """gateway, rivals, log_field_size, phi_home_j and (if K given) density_j from weight rows W."""
    for nm, vec in bb.rivals.items():
        df[nm] = W @ vec
    df["phi_home_j"] = [float(np.mean([bb.phi[h] @ w for h in hs])) if hs else 0.0 for w, hs in zip(W, homes)]
    if K is not None:
        dens = []
        colsum = bb.phi.sum(0)
        for w, Kc in zip(W, K):
            val = 0.0
            for k in np.flatnonzero(w):
                Kj = list(Kc - {k})
                val += w[k] * (bb.phi[Kj, k].sum() / colsum[k] if Kj and colsum[k] > 0 else 0.0)
            dens.append(val)
        df["density_j"] = dens


def _K_from_rows(df: pd.DataFrame, W: np.ndarray, homes: list[list[int]]) -> list[set[int]]:
    """Early-window field presence approximated by the concept's home field(s) plus every field with a retention row
    (rows require >= 5 early papers; exp4's own rule is >= 2 labelled papers, which the exp1/exp3 files do not hold)."""
    pres: dict[str, set[int]] = {}
    for c, w, hs in zip(df["concept"], W, homes):
        pres.setdefault(c, set(hs)).update(np.flatnonzero(w).tolist())
    return [pres[c] for c in df["concept"]]


def load_exp4(bb: Backbone) -> tuple[pd.DataFrame, np.ndarray, dict]:
    fr = pd.read_csv(E4 / "field_outcomes.csv")
    ft = pd.read_csv(E4 / "features.csv")
    ft = ft[["concept", "t0", "home", "log_count_W5", "growth_W5_B5", "offhome_share_W3", "entropy_W3", "reach_W3"]]
    d = fr.merge(ft, on="concept", how="left", validate="many_to_one")
    W = np.vstack([_w_row(bb, [f]) for f in d["field"]])
    homes = [[bb.idx[h] for h in str(hs).split(";") if h in bb.idx] for hs in d["home"]]
    orig = d[["gateway_j", "phi_home_j", "log_field_size", "density_j"]].copy()
    out = pd.DataFrame({"concept": d["concept"], "group": d["group"], "key": d["field"], "dkey": d["field"],
                        "source": "exp4", "R": d["R"].astype(float), "t0": d["t0"].astype(float),
                        "b_logn": d["log_n_W3"], "b_growth": d["growth_j"], "b_share": d["share_W3"],
                        "b5_logvol": d["log_count_W5"], "b5_growth": d["growth_W5_B5"],
                        "b5_offhome": d["offhome_share_W3"], "b5_entropy": d["entropy_W3"], "b5_reach": d["reach_W3"],
                        "n_early": d["n_W3"].astype(float), "one_to_many": 0, "many_to_one": 0,
                        "field_s2": ""})
    _attach(out, W, homes, bb, None)
    Kapprox = _K_from_rows(out, W, homes)
    tmp = out.copy()
    _attach(tmp, W, homes, bb, Kapprox)
    chk = {"gateway_j_maxabs": float(np.abs(out["gateway_j"] - orig["gateway_j"]).max()),
           "phi_home_j_maxabs": float(np.abs(out["phi_home_j"] - orig["phi_home_j"]).max()),
           "log_field_size_maxabs": float(np.abs(out["log_field_size"] - orig["log_field_size"]).max()),
           "density_j_rows_approx_vs_exp4": {"spearman": float(pd.Series(tmp["density_j"]).corr(orig["density_j"],
                                                                                                method="spearman")),
                                             "maxabs": float(np.abs(tmp["density_j"] - orig["density_j"]).max())}}
    out["density_j"] = orig["density_j"].to_numpy()  # exp4's own K (>=2 labelled papers in t0..t0+2) is authoritative
    return out, W, chk


def load_exp1(bb: Backbone) -> tuple[pd.DataFrame, np.ndarray, dict]:
    fr = pd.read_csv(E1 / "field_outcomes.csv")
    oc = pd.read_csv(E1 / "outcomes.csv")
    ff = pd.read_csv(E1 / "field_features.csv")[["concept", "field", "bg_LOR_j"]]
    d = fr.merge(oc[["concept", "t0", "home_s2", "B_logvol", "B_growth", "B_offhome", "B_entropy", "B_nfields"]],
                 on="concept", how="left", validate="many_to_one")
    d = d.merge(ff, on=["concept", "field"], how="left", validate="one_to_one")
    xmap = XW["map"]
    n0 = len(d)
    unmapped = d[~d["field"].isin(xmap)]
    d = d[d["field"].isin(xmap)].reset_index(drop=True)
    tgt_count: dict[str, int] = {}
    for s2, tg in xmap.items():
        for t in tg:
            tgt_count[t] = tgt_count.get(t, 0) + 1
    W = np.vstack([_w_row(bb, xmap[f]) for f in d["field"]])
    hm = XW["home_map_exp1"]
    homes = [[bb.idx[hm[h]] for h in str(hs).split("|") if h in hm] for hs in d["home_s2"]]
    keys = [xmap[f][0] if len(xmap[f]) == 1 else f"S2:{f}" for f in d["field"]]
    out = pd.DataFrame({"concept": d["concept"], "group": d["dev_group"].map(G1), "key": keys,
                        "dkey": [xmap[f][0] for f in d["field"]], "source": "exp1", "R": d["R_j"].astype(float),
                        "t0": d["t0"].astype(float), "b_logn": d["log_n_j_early"], "b_growth": d["growth_j"],
                        "b_share": d["share_j"], "b5_logvol": d["B_logvol"], "b5_growth": d["B_growth"],
                        "b5_offhome": d["B_offhome"], "b5_entropy": d["B_entropy"], "b5_reach": d["B_nfields"],
                        "n_early": d["n_j_early"].astype(float),
                        "one_to_many": [int(len(xmap[f]) > 1) for f in d["field"]],
                        "many_to_one": [int(any(tgt_count[t] > 1 for t in xmap[f])) for f in d["field"]],
                        "field_s2": d["field"], "bg_LOR_j": d["bg_LOR_j"]})
    _attach(out, W, homes, bb, _K_from_rows(out, W, homes))
    return out, W, {"n_in": n0, "n_unmapped_dropped": int(len(unmapped)),
                    "unmapped_fields": sorted(unmapped["field"].unique().tolist()),
                    "n_missing_group": int(out["group"].isna().sum())}


def load_exp3(bb: Backbone) -> tuple[pd.DataFrame, np.ndarray, dict]:
    fr = pd.read_csv(E3 / "field_outcomes.csv")
    oc = pd.read_csv(E3 / "outcomes.csv")
    names = pd.read_csv(E3 / "field_names.csv").set_index("field")["field_name"].to_dict()
    d = fr.merge(oc[["concept", "t0", "home", "logvol", "growth", "offhome_share", "entropy", "nfields2"]],
                 on="concept", how="left", validate="many_to_one", suffixes=("", "_c"))
    d["fname"] = d["field"].map(names)
    bad = d["fname"].isna() | ~d["fname"].isin(bb.idx)
    d = d[~bad].reset_index(drop=True)
    W = np.vstack([_w_row(bb, [f]) for f in d["fname"]])
    homes = [[bb.idx[names[int(float(h))]] for h in str(hs).split(";") if h not in ("", "nan")] for hs in d["home"]]
    out = pd.DataFrame({"concept": d["concept"], "group": d["group"].map(G3), "key": d["fname"], "dkey": d["fname"],
                        "source": "exp3", "R": d["R_j"].astype(float), "t0": d["t0"].astype(float),
                        "b_logn": d["logn_j_early"], "b_growth": d["growth_j_x"] if "growth_j_x" in d else d["growth_j"],
                        "b_share": d["share_j"], "b5_logvol": d["logvol"], "b5_growth": d["growth_c"]
                        if "growth_c" in d else d["growth"], "b5_offhome": d["offhome_share"],
                        "b5_entropy": d["entropy"], "b5_reach": d["nfields2"], "n_early": d["n_j_early"].astype(float),
                        "one_to_many": 0, "many_to_one": 0, "field_s2": ""})
    _attach(out, W, homes, bb, _K_from_rows(out, W, homes))
    return out, W, {"n_unmapped_dropped": int(bad.sum()), "n_missing_group": int(out["group"].isna().sum())}


def kappa(a: np.ndarray, b: np.ndarray) -> dict:
    a, b = a.astype(int), b.astype(int)
    t = pd.crosstab(pd.Series(a, name="a"), pd.Series(b, name="b")).reindex(index=[0, 1], columns=[0, 1],
                                                                            fill_value=0)
    n = t.values.sum()
    po = np.trace(t.values) / n if n else math.nan
    pe = (t.values.sum(0) * t.values.sum(1)).sum() / n ** 2 if n else math.nan
    k = (po - pe) / (1 - pe) if n and pe < 1 else math.nan
    return {"n": int(n), "agreement": float(po), "kappa": float(k), "table_rows_a_cols_b": t.values.tolist()}


def build_all() -> dict:
    bb = Backbone()
    d4, W4, c4 = load_exp4(bb)
    d1, W1, c1 = load_exp1(bb)
    d3, W3, c3 = load_exp3(bb)
    for d in (d4, d1, d3):
        d["cl"] = d["concept"]
    # overlap report
    cs = {s: set(d["concept"]) for s, d in (("exp4", d4), ("exp1", d1), ("exp3", d3))}
    ov = {"concepts": {"exp4": len(cs["exp4"]), "exp1": len(cs["exp1"]), "exp3": len(cs["exp3"]),
                       "exp4&exp1": len(cs["exp4"] & cs["exp1"]), "exp4&exp3": len(cs["exp4"] & cs["exp3"]),
                       "exp1&exp3": len(cs["exp1"] & cs["exp3"]), "all_three": len(cs["exp4"] & cs["exp1"] & cs["exp3"])}}
    e1u = d1.sort_values("n_early", ascending=False).drop_duplicates(["concept", "dkey"])
    eps = {"exp4": d4.set_index(["concept", "dkey"])["R"], "exp3": d3.set_index(["concept", "dkey"])["R"],
           "exp1": e1u.set_index(["concept", "dkey"])["R"]}
    ov["episodes"] = {"exp1_within_file_duplicates_after_crosswalk": int(len(d1) - len(e1u))}
    for a, b in (("exp4", "exp1"), ("exp4", "exp3"), ("exp1", "exp3")):
        sh = eps[a].index.intersection(eps[b].index)
        ov["episodes"][f"{a}&{b}"] = int(len(sh))
        ov["episodes"][f"R_agreement_{a}_vs_{b}"] = kappa(eps[a].loc[sh].to_numpy(), eps[b].loc[sh].to_numpy()) \
            if len(sh) else None
    ov["episodes"]["all_three"] = int(len(eps["exp4"].index.intersection(eps["exp1"].index)
                                          .intersection(eps["exp3"].index)))
    # union panel: priority exp4 > exp3 > exp1
    allrows = pd.concat([d4.assign(_p=0), d3.assign(_p=1), e1u.assign(_p=2)], ignore_index=True)
    Wall = {"exp4": W4, "exp3": W3, "exp1": W1}
    allrows["_w"] = list(np.vstack([W4, W3, W1[e1u.index.to_numpy()]]))
    u = allrows.sort_values(["_p"], kind="stable").drop_duplicates(["concept", "dkey"]).copy()
    # concept group consistency: group of the highest-priority source that holds the concept
    cg = allrows.sort_values("_p", kind="stable").drop_duplicates("concept").set_index("concept")["group"]
    n_regroup = int((u["group"] != u["concept"].map(cg)).sum())
    u["group"] = u["concept"].map(cg)
    # agreement across files for the agree-only sensitivity
    agree = []
    for c, k in zip(u["concept"], u["dkey"]):
        vals = [eps[s].loc[(c, k)] for s in eps if (c, k) in eps[s].index]
        agree.append(int(len(set(vals)) == 1))
    u["R_agrees_all_files"] = agree
    u["n_files"] = [sum((c, k) in eps[s].index for s in eps) for c, k in zip(u["concept"], u["dkey"])]
    u = u.sort_values(["_p", "concept", "dkey"]).reset_index(drop=True)
    Wu = np.vstack(u["_w"].to_numpy())
    u = u.drop(columns=["_w", "_p"])
    u["src_exp1"] = (u["source"] == "exp1").astype(int)
    u["src_exp3"] = (u["source"] == "exp3").astype(int)
    ov["union"] = {"n_rows": int(len(u)), "by_source": u["source"].value_counts().to_dict(),
                   "n_concepts": int(u["concept"].nunique()), "n_rows_regrouped_for_concept_consistency": n_regroup,
                   "n_rows_R_disagree_across_files": int((u["R_agrees_all_files"] == 0).sum()),
                   "n_new_episode_rows": int((u["source"] != "exp4").sum())}
    # pooled pool for P_pooled: every row of all three files (exp1 all 367 rows)
    pool = pd.concat([d4, d3, d1], ignore_index=True)[["key", "concept", "group", "R"]]
    return {"bb": bb, "exp4": (d4, W4), "exp1": (d1, W1), "exp3": (d3, W3), "union": (u, Wu), "pool": pool,
            "checks": {"exp4_recompute": c4, "exp1": c1, "exp3": c3}, "overlap": ov, "Wall": Wall}
