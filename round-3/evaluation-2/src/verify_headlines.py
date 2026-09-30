#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers from RAW inputs through code paths that differ from the pipeline
(sklearn/scipy/hand-written estimators instead of common.py helpers), each paired with a shuffled/placebo control that must
fail. Writes results/verify_headlines.json."""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import optimize, stats
from sklearn.metrics import cohen_kappa_score

WS = Path(__file__).resolve().parent
ROOT = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[2]))).resolve()
E5, E6 = ROOT / "iter_2/gen_art/gen_art_experiment_5", ROOT / "iter_2/gen_art/gen_art_experiment_6"
rng = np.random.default_rng(7)
out = {}


def cid(x) -> str:
    return "C" + str(x).rsplit("/", 1)[-1].lstrip("C")


# 1. frame agreement (retention kappa, onset, home) from the raw CSVs with sklearn
f5 = pd.read_csv(E5 / "frame_concepts.csv"); f6 = pd.read_csv(E6 / "results/frame_concepts.csv")
f5["k"] = f5.concept_id.map(cid); f6["k"] = f6.concept_id.map(cid)
m = f5.merge(f6, on="k", suffixes=("5", "6"))
e5 = pd.read_csv(E5 / "episodes.csv").merge(f5[["ci", "k"]], on="ci")
e6 = pd.read_csv(E6 / "results/episodes.csv").merge(f6[["cidx", "k"]], on="cidx")
pr = e5.merge(e6, on=["k", "field"]).dropna(subset=["R", "R_cj"])
kap = cohen_kappa_score(pr.R.astype(int), pr.R_cj.astype(int))
kap2 = cohen_kappa_score(pr.R_abs2.astype(int), pr.R_cj.astype(int))
kap_shuf = cohen_kappa_score(pr.R_abs2.astype(int), rng.permutation(pr.R_cj.astype(int)))
h5 = m.home5.astype(str).str.replace("|", ";").str.split(";").str[0].astype(float).astype(int)
out["frames"] = {"n_both": len(m), "onset_exact": float((m.t05 == m.t06).mean()), "onset_pm1": float(((m.t05 - m.t06).abs() <= 1).mean()),
                 "home_kappa_sklearn": float(cohen_kappa_score(h5, m.home_primary.astype(int))),
                 "home_kappa_shuffled": float(cohen_kappa_score(h5, rng.permutation(m.home_primary.astype(int)))),
                 "n_pairs": len(pr), "retention_kappa_sklearn": float(kap), "retention_kappa_R_abs2": float(kap2),
                 "retention_kappa_R_abs2_shuffled": float(kap_shuf)}

# 2. O5_main from the joined events with an independent qualification rule; per-group Spearman, Fisher-z pooling
ev = [json.loads(l) for l in open(WS / "results/o5_joined.jsonl")]
t0 = dict(zip(f5.k, f5.t0))
LISTS = {"gartner_hype_cycle", "mit_tr10", "nature_methods_moty", "science_boty", "physics_world_boty", "research_fronts"}
OK_T = {("mesh", "mesh_descriptor_introduced"), ("wikipedia_en", "wikipedia_article_created"), ("wikipedia_en", "wikipedia_page_created_estimated"),
        ("wikidata", "wikidata_inception"), ("wikidata", "wikidata_discovery_or_invention"), ("acm_ccs", "taxonomy_added_between"),
        ("msc", "taxonomy_added_between"), ("pacs_physh", "taxonomy_added_between")}
o5, pre = {}, 0
for r in ev:
    T = t0[r["openalex_id"]]
    q = [e["year"] for e in r["events"] if e["year_usable"] and e["relation"] == "same" and e["year"] is not None
         and ((e["source"], e["event_type"]) in OK_T or e["source"] in LISTS)
         and not (e["source"] == "mesh" and (e.get("mesh_baseline") or e["year"] <= 1966))]
    o5[r["openalex_id"]] = int(any(T < y <= T + 8 for y in q))
    pre += int(bool(q) and min(q) <= T)
oc = pd.read_csv(E5 / "concept_outcomes.csv").drop(columns=["split"]).merge(f5[["ci", "k", "group", "split"]], on="ci")
oc["o5"] = oc.k.map(o5)
zs, ws, rhos, shuf = [], [], {}, []
for g in ["PHYS", "LIFEENV", "SOC", "MATHDEC"]:
    d = oc[(oc.split == f"HELDOUT_{g}") & oc.O2r_m50.notna()]
    r = stats.spearmanr(d.o5, d.O2r_m50).statistic
    rhos[g] = float(r)
    zs.append(np.arctanh(r)); ws.append(len(d) - 3)
    shuf.append(stats.spearmanr(rng.permutation(d.o5.to_numpy()), d.O2r_m50).statistic)
zp = np.average(zs, weights=ws); se = 1 / np.sqrt(sum(ws))
ho = oc[oc.split.str.startswith("HELDOUT")]
lN = stats.spearmanr(ho.o5, np.log(ho.N_outcome.clip(lower=1))).statistic
out["o5"] = {"base_rate_heldout": float(ho.o5.mean()), "share_recognised_le_t0": pre / len(f5),
             "rho_O2r_m50_per_group": rhos, "fisher_pooled_rho": float(np.tanh(zp)),
             "fisher_pooled_ci95": [float(np.tanh(zp - 1.96 * se)), float(np.tanh(zp + 1.96 * se))],
             "shuffled_o5_rho_per_group": [float(x) for x in shuf], "rho_logN_heldout_pooled_concepts": float(lN),
             "rho_logN_shuffled": float(stats.spearmanr(rng.permutation(ho.o5.to_numpy()), np.log(ho.N_outcome.clip(lower=1))).statistic)}

# 3. next-field LR M1 vs M0 (Breslow) with a fresh per-stratum loop estimator; placebo: d0_ret_rel permuted within strata
spec = json.loads((E6 / "results/frozen_spec.json").read_text())
df = pd.read_parquet(E6 / "results/entry_risk_sets_heldout.parquet")
df = df[df.n_ret > 0].copy()
for c, s in spec["standardisation"].items():
    df[c] = (df[c] - s["mean"]) / s["sd"]
g = df.groupby("stratum").entered.agg(["sum", "size"])
df = df[df.stratum.isin(g[(g["sum"] > 0) & (g["sum"] < g["size"])].index)]
groups = [x for _, x in df.groupby("stratum")]
M0 = ["a_phi_home", "b_log_size", "c_density", "e_gate_own"]


def breslow_ll(cols, data):
    Xs = [d[cols].to_numpy(float) for d in data]
    ys = [d.entered.to_numpy(float) for d in data]

    def nll(b):
        tot = 0.0
        for X, y in zip(Xs, ys):
            eta = X @ b
            tot += (y @ eta) - y.sum() * np.logaddexp.reduce(eta)
        return -tot
    r = optimize.minimize(nll, np.zeros(len(cols)), method="L-BFGS-B")
    return -r.fun, r.x


ll0, _ = breslow_ll(M0, groups)
ll1, b1 = breslow_ll(M0 + ["d0_ret_rel"], groups)
perm = []
for d in groups:
    d = d.copy(); d["d0_ret_rel"] = rng.permutation(d.d0_ret_rel.to_numpy()); perm.append(d)
llp, _ = breslow_ll(M0 + ["d0_ret_rel"], perm)
out["next_field"] = {"n_strata": len(groups), "LR_M1_vs_M0_breslow": float(2 * (ll1 - ll0)), "d0_ret_rel": float(b1[-1]),
                     "LR_placebo_within_stratum_permuted": float(2 * (llp - ll0))}

# 4. ordering denominators from the raw ordering CSV
O = pd.read_csv(E6 / "results/ordering_heldout.csv")
T = O[O.top_o2r & O.tau.notna() & O.gamma.notna()]
out["ordering"] = {"before": int((T.gamma < T.tau).sum()), "after": int((T.gamma > T.tau).sum()), "ties": int((T.gamma == T.tau).sum()),
                   "n_top": int(O.top_o2r.sum())}

# 5. exp4 G delta-rho O2r_m30 with a hand-written closed-form ridge (no sklearn); placebo: G shuffled 200x
f4 = pd.read_csv(ROOT / "iter_1/gen_art/gen_art_experiment_4/features.csv").dropna(subset=["O2r_m30"]).reset_index(drop=True)
B5 = ["log_count_W5", "growth_W5_B5", "offhome_share_W3", "entropy_W3", "reach_W3"]


def logo_rho(d, cols):
    pred = np.full(len(d), np.nan)
    for grp in ["CS", "Eng", "BGM", "Med"]:
        te = (d.group == grp).to_numpy(); tr = ~te
        X = d[cols].copy()
        X = X.fillna(X[tr].median())
        Xtr, Xte = X[tr].to_numpy(float), X[te].to_numpy(float)
        mu, sd = Xtr.mean(0), Xtr.std(0); sd[sd == 0] = 1
        Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
        y = d.O2r_m30.to_numpy(float)[tr]
        w = np.linalg.solve(Ztr.T @ Ztr + np.eye(Ztr.shape[1]), Ztr.T @ (y - y.mean()))
        pred[te] = y.mean() + Zte @ w
    return stats.spearmanr(pred, d.O2r_m30).statistic


base = logo_rho(f4, B5)
dl = logo_rho(f4, B5 + ["G", "G_missing"]) - base
pl = []
for _ in range(200):
    d = f4.copy(); d["G"] = rng.permutation(d.G.to_numpy()); pl.append(logo_rho(d, B5 + ["G", "G_missing"]) - base)
out["t3_exp4_G"] = {"delta_rho_O2r_m30": float(dl), "placebo_mean": float(np.mean(pl)), "placebo_share_ge_real": float(np.mean(np.array(pl) >= dl))}

# 6. hand-check precision from the final items table
it = pd.read_csv(WS / "record_tables/o5_handcheck_items_final.csv")
pos, neg = it[it.kind == "positive"], it[it.kind == "negative"]
out["hand_check"] = {"precision_strict": float((pos.final_same == "yes").mean()), "fn_rate": float((neg.final_fn == "yes").mean())}
(WS / "results/verify_headlines.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
