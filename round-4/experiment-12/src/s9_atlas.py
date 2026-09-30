#!/usr/bin/env python3
"""S9 AI/CS ATLAS -- RETROSPECTIVE, DESCRIPTIVE, OUTCOME-SELECTED BY DESIGN (the request's stage-1 inspection).
40 AI concepts (CS home, AI topic share >= 0.3) in 5 outcome types x 8. Topic-level ego structure for ages -3..2 (the
only window EXP8 Pass A kept) and field-level D3 structure for ages 0..10. A 'looked meaningful' column is filled by
the frozen written rule (results/frozen_spec.json: atlas.looked_meaningful)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import kruskal, spearmanr  # noqa: E402

import cases_spec as CS  # noqa: E402
import viz  # noqa: E402
from common import (ATLAS, DATA, DISCLOSURE, E8_DATA, E8_INPUTS, ROOT, add_deviation, jdump, load_outcomes,  # noqa: E402
                    network_guard, setup_logger, update_status)

network_guard()
logger = setup_logger("s9_atlas")
TYPES = ["RAPID", "GRADUAL", "LOCAL", "DIFFUSING", "TRANSIENT"]
FIELD_MEAS = ["n_c", "H", "n_ent_off", "n_ret", "n_lost", "home_share", "comm_span", "ret_share", "frontier"]
TOPIC_MEAS = ["degree_W3", "new_nb_W3", "n_comm_W3", "ego_density_W3"]
OPEN_MEAS = ["new_edge_rate_all", "n_comm_W3_all", "participation_all", "NOV_res_all", "ego_density_W3_all",
             "edge_persistence_all", "OPEN_all", "OPEN_home"]


def ai_share(em: pd.DataFrame) -> pd.Series:
    tids = json.loads((E8_INPUTS / "topic_ids.json").read_text())
    tm = pd.read_csv(E8_INPUTS / "topic_meta.csv").set_index("topic").loc[tids].reset_index()
    rx = re.compile(CS.AI_TOPIC_REGEX)
    is_ai = (tm.subfield.isin(CS.AI_SUBFIELDS) | tm.name.map(lambda s: bool(rx.search(str(s))))).to_numpy()
    e = em.explode("topics").dropna(subset=["topics"])
    e["ai"] = is_ai[e.topics.astype(int).to_numpy()]
    return e.groupby("ci").ai.mean()


def pick(T: pd.DataFrame) -> tuple[dict, dict, dict]:
    """per type, the highest AI-share tier (0.3 -> 0.2 -> 0.1) that yields 8 concepts; type order as listed; a
    concept is used at most once; outcome terciles/growth quantiles are computed over the CS-home, non-generic pool."""
    g90 = T[T.ai_share >= 0.1].growth_c.quantile(0.9)
    g50 = T[T.ai_share >= 0.1].growth_c.median()
    rules = {"RAPID": T.growth_c >= g90, "GRADUAL": (T.growth_c <= g50) & (T.O1b == 1),
             "LOCAL": (T.O1b == 1) & (T.o2r_terc == 0), "DIFFUSING": T.o2r_terc == 2, "TRANSIENT": T.O3 == 1}
    used, out, avail, tiers = set(), {}, {}, {}
    for t in TYPES:
        for thr in (0.3, 0.2, 0.1):
            c = T[rules[t] & (T.ai_share >= thr) & ~T.ci.isin(used)].sort_values("early_volume", ascending=False)
            if len(c) >= 8 or thr == 0.1:
                break
        avail[t] = int(len(c))
        tiers[t] = thr
        out[t] = c.ci.head(8).tolist()
        used.update(out[t])
    return out, avail, tiers


@logger.catch(reraise=True)
def main() -> None:
    import ego_open
    from ego_ctx import rq1_context
    O = load_outcomes().all()
    J = pd.read_parquet(DATA / "joined.parquet")
    OF = pd.read_parquet(ROOT / "open_features.parquet")
    pre = pd.read_parquet(DATA / "pre_onset.parquet")
    T = J.merge(O.drop(columns=["split"]), on="ci").merge(pre, on="ci").merge(
        OF[["ci", "OPEN_all", "OPEN_home"] + [f"{k}_all" for k in ("new_edge_rate", "n_comm_W3", "participation", "NOV_res",
                                                                  "ego_density_W3", "edge_persistence")]]
        .rename(columns=lambda c: c), on="ci", suffixes=("", "_of"))
    T["o2r_terc"] = pd.qcut(T.O2r_resid, 3, labels=False)
    em = pd.read_parquet(E8_DATA / "frame_matches_early/part_001.parquet", columns=["ci", "year", "topics"])
    em = em.merge(J[["ci", "t0"]], on="ci")
    early = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)]
    cs = J[J.home_list.map(lambda h: "17" in h.split(";"))].ci
    share = ai_share(early[early.ci.isin(cs)])
    T = T[T.ci.isin(cs)].copy()
    T["ai_share"] = T.ci.map(share).fillna(0.0)
    T["generic"], T["generic_why"] = CS.generic_flags(T.name, T.pre_onset_papers, T.early_volume)
    T = T[~T.generic]
    sel, avail, tiers = pick(T)
    tier = tiers
    relaxed = {t: v for t, v in tiers.items() if v < 0.3}
    if relaxed:
        add_deviation("atlas_relax", f"types with < 8 eligible AI concepts at AI share >= 0.3 were relaxed per type: "
                      f"{relaxed}; available: {avail}", "those atlas rows include lower-AI-share CS concepts (tier "
                      "recorded per type); types still short of 8 show all eligible concepts")
    rows = []
    for t in TYPES:
        for ci in sel[t]:
            rows.append({"ci": ci, "type": t, "ai_tier": tiers[t]})
    A = pd.DataFrame(rows).merge(T, on="ci")
    logger.info(f"atlas: tier {tier}; per type {A.type.value_counts().to_dict()}; eligible avail {avail}")
    # ---- topic-level (ages -3..2) and field-level (ages 0..10) panels
    ctx = rq1_context()
    ego_open.set_context(ctx)
    P = pd.read_parquet(ROOT / "panel.parquet")
    emA = em[em.ci.isin(A.ci)]
    topic_rows, ego_snaps = [], {}
    for r in A.itertuples():
        d = emA[emA.ci == r.ci]
        works = list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))
        s = ego_open.concept_open(str(r.name), [], int(r.t0), works, keep_nb=True)
        pre = set(s["_pre"])
        rec = {"ci": r.ci}
        for a in range(-3, 3):
            rec[f"nc_age{a}"] = int((d.year == r.t0 + a).sum())
        for w in ("W1", "W2", "W3"):
            nb = s["_nb"][w]
            rec[f"degree_{w}"] = len(nb)
            rec[f"new_nb_{w}"] = len([v for v in nb if v not in pre])
            sl = __import__("ego").slice_of(int(r.t0) + int(w[1]) - 1)
            rec[f"n_comm_{w}"] = len({int(ctx["comm"][sl][v]) for v in nb})
            ins = np.zeros(ctx["nt"], bool)
            ins[nb] = True
            a_, b_ = ctx["full_edges"][sl]
            rec[f"ego_density_{w}"] = (int((ins[a_] & ins[b_]).sum()) / (len(nb) * (len(nb) - 1) / 2)
                                       if len(nb) >= 2 else np.nan)
        topic_rows.append(rec)
        ego_snaps[r.ci] = s
    TP = pd.DataFrame(topic_rows)
    A = A.merge(TP, on="ci")
    FP = P[P.ci.isin(A.ci)].copy()
    # ---- table: medians per type at ages 2, 5, 8 + KW + looked-meaningful rule
    dev = J[J.split == "DEV"][["ci"]].merge(O[["ci", "O2r_resid"]], on="ci")
    Pdev = P[(P.age == 2) & P.ci.isin(dev.ci)].merge(dev, on="ci")
    frame_rho = {m: float(spearmanr(Pdev[m], Pdev.O2r_resid, nan_policy="omit").statistic) for m in FIELD_MEAS}
    D2 = dev.merge(OF[["ci", "OPEN_all", "OPEN_home"] + [f"{k}_all" for k in ("new_edge_rate", "n_comm_W3", "participation",
                                                                              "NOV_res", "ego_density_W3", "edge_persistence")]],
                   on="ci")
    frame_rho.update({m: float(spearmanr(D2[m], D2.O2r_resid, nan_policy="omit").statistic) for m in OPEN_MEAS})
    table = []
    wide = {}
    for age in (2, 5, 8):
        Fa = FP[FP.age == age].set_index("ci")
        for m in FIELD_MEAS:
            wide[(m, age)] = A.ci.map(Fa[m])
    for m in TOPIC_MEAS:
        wide[(m, 2)] = A[m.replace("_W3", "_W3")] if m in A else A[m]
    for m in OPEN_MEAS:
        wide[(m, 2)] = A[m]
    for (m, age), v in wide.items():
        v = pd.to_numeric(v, errors="coerce")
        row = {"measure": m, "age": age}
        groups = []
        for t in TYPES:
            vv = v[A.type == t]
            row[f"median_{t}"] = float(vv.median()) if vv.notna().any() else None
            if vv.notna().sum() >= 2:
                groups.append(vv.dropna().to_numpy())
        try:
            row["kruskal_H"] = float(kruskal(*groups).statistic) if len(groups) >= 2 else None
            row["kruskal_p_descriptive"] = float(kruskal(*groups).pvalue) if len(groups) >= 2 else None
        except ValueError:
            row["kruskal_H"] = row["kruskal_p_descriptive"] = None
        if age == 2:
            dv, lv = v[A.type == "DIFFUSING"].dropna(), v[A.type == "LOCAL"].dropna()
            psd = np.sqrt((dv.var(ddof=1) + lv.var(ddof=1)) / 2) if len(dv) > 1 and len(lv) > 1 else np.nan
            dz = (dv.mean() - lv.mean()) / psd if psd and np.isfinite(psd) and psd > 0 else np.nan
            fr = frame_rho.get(m)
            row["diff_minus_local_pooled_sd"] = float(dz) if np.isfinite(dz) else None
            row["frame_dev_spearman_O2r_resid"] = fr
            row["looked_meaningful"] = bool(np.isfinite(dz) and abs(dz) >= 0.5 and fr is not None
                                            and np.sign(dz) == np.sign(fr))
        table.append(row)
    TB = pd.DataFrame(table)
    TB.to_csv(ATLAS / "table.csv", index=False)
    # ---- figures
    plt = __import__("matplotlib.pyplot").pyplot
    fig, axes = plt.subplots(5, 8, figsize=(16, 9.5), sharex=True)
    for i, t in enumerate(TYPES):
        cis = sel[t]
        for j in range(8):
            ax = axes[i, j]
            if j >= len(cis):
                ax.set_axis_off()
                continue
            d = FP[FP.ci == cis[j]].sort_values("age")
            ax.plot(d.age, d.n_ent_off, color=viz.OI["sky"], lw=1.2, label="entered off-home")
            ax.plot(d.age, d.n_ret, color=viz.OI["blue"], lw=1.2, label="retained")
            ax2 = ax.twinx()
            ax2.plot(d.age, d.H, color=viz.OI["vermillion"], lw=0.9, ls="--", label="field entropy H")
            ax2.set_ylim(0, 3)
            ax2.tick_params(labelsize=5)
            if j < 7:
                ax2.set_yticklabels([])
            ax.tick_params(labelsize=5)
            nm = A.set_index("ci").name[cis[j]]
            ax.set_title(f"{nm[:24]} ({int(A.set_index('ci').t0[cis[j]])})", fontsize=6, loc="left")
            if j == 0:
                ax.set_ylabel(t, fontsize=8, fontweight="bold")
            if i == 0 and j == 0:
                h1, l1 = ax.get_legend_handles_labels()
                h2, l2 = ax2.get_legend_handles_labels()
                fig.legend(h1 + h2, l1 + l2, loc="upper right", ncol=3, frameon=False, fontsize=7)
    fig.subplots_adjust(wspace=0.32, hspace=0.45)
    fig.suptitle("AI/CS atlas (RETROSPECTIVE, outcome-selected by design): off-home fields entered / retained (left "
                 "axis) and field entropy H (dashed, right axis 0-3) by age since onset", fontsize=10, x=0.01, ha="left")
    viz.save(fig, ATLAS / "small_multiples")
    fig, axes = plt.subplots(5, 8, figsize=(16, 10))
    for i, t in enumerate(TYPES):
        for j in range(8):
            ax = axes[i, j]
            if j >= len(sel[t]):
                ax.set_axis_off()
                continue
            ci = sel[t][j]
            s = ego_snaps[ci]
            t0 = int(A.set_index("ci").t0[ci])
            sl = __import__("ego").slice_of(t0 + 2)
            viz.ego_snapshot(ax, s["_nb"]["W3"], s["_cnt"]["W3"], s["_pmi"]["W3"], ctx["full_edges"][sl],
                             ctx["comm"][sl], ctx["names"], f"{t}: {A.set_index('ci').name[ci][:22]}")
    fig.suptitle("AI/CS atlas: W3 (t0+2) topic ego networks, colour = EXP3 Leiden community (retrospective)", fontsize=10,
                 x=0.01, ha="left")
    viz.save(fig, ATLAS / "ego_W3_grid")
    atlas = {"label": CS.ATLAS_RULE["label"], "rule": CS.ATLAS_RULE, "ai_share_tier": tier, "available_per_type": avail,
             "concepts": A[["ci", "concept_id", "name", "type", "ai_tier", "t0", "ai_share", "early_volume", "growth_c", "O1b", "O3",
                            "O2r_resid", "OPEN_all", "OPEN_home"]].to_dict("records"),
             "topic_level": TP.to_dict("records"),
             "table": TB.to_dict("records"),
             "looked_meaningful": TB[TB.get("looked_meaningful", pd.Series(dtype=bool)).fillna(False).astype(bool)]
             .measure.tolist() if "looked_meaningful" in TB else [],
             "data_limit": "topic-level ego structure exists only for t0-3..t0+2 (EXP8 Pass A kept only those hits; no "
                           "snapshot pass is allowed here), so topic-neighbour change after t0+2 cannot be shown",
             "disclosure": DISCLOSURE, "Source": "s9_atlas.py"}
    jdump(atlas, ATLAS / "atlas.json")
    logger.info(f"atlas looked-meaningful: {atlas['looked_meaningful']}")
    update_status("S9_atlas", {"atlas_n": int(len(A)), "atlas_ai_share_tier_per_type": tier})


if __name__ == "__main__":
    main()
