#!/usr/bin/env python3
"""S10 PIPELINE COUNTS AND OUTPUTS: pipeline_counts.json (every number read from files), method_out.json
(exp_gen_sol_out; datasets rq2_concepts + case_pairs; headline metadata), summary figures (PNG + PDF)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import typology as TY  # noqa: E402
import viz  # noqa: E402
from common import (ATLAS, B5, DATA, DISCLOSURE, E5, E7, E8_DATA, FIGS, RES, ROOT, jdump, jload, load_outcomes,  # noqa: E402
                    network_guard, setup_logger, validate_out)

network_guard()
logger = setup_logger("s10_outputs")
plt = viz.plt


def nrows(p: Path) -> int:
    return int(pq.ParquetFile(p).metadata.num_rows)


def pipeline_counts() -> dict:
    J = pd.read_parquet(DATA / "joined.parquet")
    si = jload(E5 / "scan/scan_info.json")
    od = jload(RES / "open_diagnostics.json")
    cp = jload(RES / "case_pairs.json")
    at = jload(ATLAS / "atlas.json")
    tr = jload(RES / "trajectories_dev.json")
    with (E5 / "episodes.csv").open() as f:
        n_ep = sum(1 for _ in f) - 1
    c = {
        "EXP5_scan": {k: si[k] for k in si},
        "EXP5_lexicon_rows": nrows(E5 / "lexicon_v1.parquet"),
        "EXP5_episodes_rows": n_ep,
        "frame_by_split": J.split.value_counts().to_dict(),
        "frame_by_split_group": J.groupby(["split", "group"]).size().rename("n").reset_index().to_dict("records"),
        "EXP8_passA": jload(E8_DATA / "passA_info.json"),
        "EXP8_passB": jload(E8_DATA / "passB_info.json"),
        "EXP8_frame_matches_early_rows": nrows(E8_DATA / "frame_matches_early/part_001.parquet"),
        "EXP7_risk_set_rows": {p.name: nrows(p) for p in sorted((E7 / "results").glob("risk_sets_*.parquet"))},
        "EXP7_state_panel_rows": {p.name: nrows(p) for p in sorted((E7 / "results").glob("state_panel_*.parquet"))},
        "this_artifact": {
            "state_sequence_rows": nrows(ROOT / "state_sequences.parquet"),
            "concept_ages_panel_rows": nrows(ROOT / "panel.parquet"),
            "states_verification": {k: v for k, v in jload(RES / "states_verification.json").items() if k != "note"},
            "dtw_n_dev": tr["n"], "dtw_pairs_dev": tr["n"] * (tr["n"] - 1) // 2,
            "open_coverage": {b: od["coverage"][b]["overall"] for b in ("all", "home", "size")},
            "n_case_pairs": len(cp["pairs"]), "atlas_n": len(at["concepts"]),
            "decomposition_n_dev": jload(RES / "decomposition_dev.json")["n_concepts_with_outcome"]},
    }
    jdump(c, RES / "pipeline_counts.json")
    return c


# ----------------------------------------------------------------------------- figures
def fig_waterfall(d4: dict, d4h: dict) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4), sharey=True)
    panels = [("DEV (CS/Eng/BGM/Med)", d4["variants"]), ("Held-out pooled (PHYS/LIFEENV/SOC/MATHDEC)",
                                                         d4h["pooled_heldout4"]["variants"]),
              ("Cohort 2010-14 pooled", d4h["pooled_cohort"]["variants"])]
    for ax, (title, V) in zip(axes, panels):
        for j, (var, lab) in enumerate((("ii_vol_PRIMARY", "all homes"), ("iv_vol_noMed_PR1", "Medicine excluded"))):
            p, ci = V[var]["point"], V[var].get("ci", {})
            cum = 0.0
            for i, (k, name, col) in enumerate((("D_E2", "early contact E2", viz.OI["blue"]),
                                                ("D_M", "frontier advance M", viz.OI["green"]),
                                                ("D_rho", "retention rho", viz.OI["vermillion"]))):
                x = i + 0.38 * j - 0.19
                ax.bar(x, p[k], bottom=cum, width=0.34, color=col, alpha=1 if j == 0 else 0.55,
                       edgecolor="black", lw=0.3)
                if k in ci:
                    ax.errorbar(x, cum + p[k], yerr=[[p[k] - ci[k][0]], [ci[k][1] - p[k]]], color="black", lw=0.6,
                                capsize=1.5)
                cum += p[k]
            ax.bar(3 + 0.38 * j - 0.19, cum, width=0.34, color=viz.OI["grey"], alpha=1 if j == 0 else 0.55,
                   edgecolor="black", lw=0.3, label=lab)
        ax.set_xticks(range(4))
        ax.set_xticklabels(["E2\n(contact)", "M\n(frontier)", "rho\n(retention)", "total\nlog gap"], fontsize=7)
        ax.axhline(0, color="black", lw=0.5)
        ax.set_title(title, loc="left", fontsize=8)
    axes[0].set_ylabel("log(top / bottom O2r_resid tercile)\n(volume-stratified, n-weighted)")
    h, l = axes[0].get_legend_handles_labels()
    fig.legend(h, l, frameon=False, fontsize=7.5, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.06))
    fig.suptitle("Breadth gap decomposition: log mean retained fields = log E2 + log M + log rho (bars cumulate; "
                 "whiskers = 95% concept-bootstrap CI of each factor)", fontsize=8.5, x=0.01, ha="left")
    viz.save(fig, FIGS / "fig_decomposition_waterfall")


def fig_forest(d4: dict, d4h: dict) -> None:
    rows = []
    for g, r in d4["dev_groups"].items():
        v = r["variants"]["ii_vol_PRIMARY"]
        rows.append((f"DEV {g} (all homes; n={v['n']})", v["point"]["diff_explore_ret"],
                     v.get("ci", {}).get("diff_explore_ret"), "dev"))
    v = d4["variants"]["iv_vol_noMed_PR1"]
    rows.append(("DEV pooled, no Med (PR1)", v["point"]["diff_explore_ret"], v["ci"]["diff_explore_ret"], "pool"))
    for u, r in d4h["units"].items():
        v = r["variants"]["iv_vol_noMed_PR1"]
        rows.append((f"{u} (no Med; n={r['n_with_outcome']})", v["point"]["diff_explore_ret"],
                     v.get("ci", {}).get("diff_explore_ret") if v["ci_reported"] else None, "held"))
    v = d4h["pooled_heldout4"]["variants"]["iv_vol_noMed_PR1"]
    rows.append(("Held-out pooled, no Med (PR1)", v["point"]["diff_explore_ret"], v["ci"]["diff_explore_ret"], "pool"))
    dl = d4h["DL_heldout_groups"]["diff_explore_ret"]
    rows.append((f"DL held-out groups (I2={dl['I2']:.2f})", dl["b"], dl["ci"], "pool"))
    fig, ax = plt.subplots(figsize=(6.2, 0.35 * len(rows) + 0.8))
    for i, (lab, b, ci, kind) in enumerate(rows):
        y = len(rows) - 1 - i
        col = {"dev": viz.OI["blue"], "held": viz.OI["orange"], "pool": viz.OI["black"]}[kind]
        if b is None or not np.isfinite(b):
            continue
        ax.plot(b, y, marker="D" if kind == "pool" else "o", color=col, ms=5)
        if ci and None not in ci:
            ax.plot(ci, [y, y], color=col, lw=1.2)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows[::-1]], fontsize=7)
    ax.axvline(0, color="black", lw=0.6)
    ax.set_xlabel("s_explore - s_ret (share of the breadth gap from exploration minus retention)")
    ax.set_title("PR1: exploration vs retention share, by unit (95% concept-bootstrap CI)", loc="left", fontsize=8.5)
    viz.save(fig, FIGS / "fig_forest_explore_vs_retention")


def fig_loadings(tr: dict) -> None:
    L = tr["pca"]["loadings"]
    k = len(L)
    fig, axes = plt.subplots(1, k, figsize=(4.2 * k, 3.4))
    axes = np.atleast_1d(axes)
    for ax, (pcn, ld) in zip(axes, L.items()):
        M = np.array([ld[v] for v in TY.VARS])
        m = np.abs(M).max()
        im = ax.imshow(M, cmap="RdBu_r", vmin=-m, vmax=m, aspect="auto")
        ax.set_yticks(range(len(TY.VARS)))
        ax.set_yticklabels(TY.VARS, fontsize=7)
        ax.set_xticks(range(9))
        ax.set_xlabel("age")
        j = int(pcn[2:]) - 1
        ax.set_title(f"{pcn} ({tr['pca']['explained'][j]:.1%} of variance)", loc="left", fontsize=8.5)
        fig.colorbar(im, ax=ax, shrink=0.8)
    fig.suptitle("PCA continuum of DEV trajectories: loadings (variable x age; z-scored, asinh counts)", fontsize=8.5,
                 x=0.01, ha="left")
    viz.save(fig, FIGS / "fig_pca_loadings")


def fig_agreement() -> None:
    A = pd.read_parquet(RES / "typology_dev_assign.parquet")
    tr = jload(RES / "trajectories_dev.json")
    ct = pd.crosstab(A.dtw_class, A.hmm_class)
    fig, ax = plt.subplots(figsize=(3.8, 3.2))
    im = ax.imshow(ct.to_numpy(), cmap="Blues")
    for i in range(ct.shape[0]):
        for j in range(ct.shape[1]):
            ax.text(j, i, int(ct.iloc[i, j]), ha="center", va="center", fontsize=7)
    ax.set_xlabel("HMM-partition class")
    ax.set_ylabel("DTW k-medoids class")
    ax.set_xticks(range(ct.shape[1]))
    ax.set_yticks(range(ct.shape[0]))
    ax.set_title(f"DTW vs HMM agreement (DEV, k={tr['choose_k']['k']}): ARI {tr['hmm']['ari_dtw_hmm']:.3f}",
                 loc="left", fontsize=8)
    fig.colorbar(im, ax=ax, shrink=0.8)
    viz.save(fig, FIGS / "fig_dtw_hmm_agreement")


def fig_hexbin() -> None:
    of = pd.read_parquet(ROOT / "open_features.parquet", columns=["ci", "OPEN_all", "OPEN_home"])
    A = pd.concat([pd.read_parquet(RES / "typology_dev_assign.parquet")[["ci", "PC1"]],
                   pd.read_parquet(RES / "typology_heldout_assign.parquet")[["ci", "PC1"]]]).merge(of, on="ci")
    J = pd.read_parquet(DATA / "joined.parquet")[["ci", "split"]]
    A = A.merge(J, on="ci")
    trd, trh = jload(RES / "trajectories_dev.json"), jload(RES / "trajectories_heldout.json")
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6), sharey=True)
    for ax, b in zip(axes, ("all", "home")):
        m = A[f"OPEN_{b}"].notna()
        hb = ax.hexbin(A[f"OPEN_{b}"][m], A.PC1[m], gridsize=45, cmap="viridis", mincnt=1, bins="log")
        rd = trd["open_on_axis"]["pooled"]["PC1"][b]
        rh = trh["DL_heldout_groups_PC1"][b]
        ax.set_xlabel(f"OPEN_{b} (early ego-network openness, t0..t0+2)")
        ax.set_title(f"DEV rho {rd['spearman']['rho']:.2f} (partial {rd['partial_given_B5_labelcov']['rho']:.2f}); "
                     f"held-out DL {rh['spearman']['b']:.2f} (partial {rh['partial_given_B5_labelcov']['b']:.2f})",
                     fontsize=7, loc="left")
        fig.colorbar(hb, ax=ax, shrink=0.8, label="concepts (log)")
    axes[0].set_ylabel("PC1 (trajectory axis: breadth of off-home spread)")
    fig.suptitle("OPEN vs the trajectory continuum (all 12,499 concepts; partial = given B5 + label coverage)", fontsize=8.5,
                 x=0.01, ha="left")
    viz.save(fig, FIGS / "fig_open_vs_pc1_hexbin")


def fig_km(sq: dict, sqh: dict) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.2), sharey=True)
    for ax, (lab, r) in zip(axes, (("DEV", sq["DEV"]), ("Held-out", sqh["HELDOUT"]), ("Cohort", sqh["COHORT"]))):
        for f, col, name in (("0", viz.OI["blue"], "single-home"), ("1", viz.OI["orange"], "intersection-born")):
            S = r["km"][f]["S"]
            ax.step(range(len(S)), S, where="post", color=col, label=f"{name} (n={r['km'][f]['n']})")
        hz = r["cloglog_hazard"]
        ax.set_title(f"{lab}: HR {hz.get('HR', float('nan')):.2f} [{hz.get('HR_ci', [np.nan] * 2)[0]:.2f}, "
                     f"{hz.get('HR_ci', [np.nan] * 2)[1]:.2f}] -> {r['verdict']}", fontsize=7.5, loc="left")
        ax.set_xlabel("age")
        ax.legend(frameon=False, fontsize=6.5)
    axes[0].set_ylabel("share not yet taken off off-home")
    fig.suptitle("Off-home take-off (first age with >= 2 new off-home fields or >= 1 retained): Kaplan-Meier by "
                 "intersection-born flag", fontsize=8.5, x=0.01, ha="left")
    viz.save(fig, FIGS / "fig_km_takeoff")


# ----------------------------------------------------------------------------- method_out.json
def method_out(c: dict) -> dict:
    J = pd.read_parquet(DATA / "joined.parquet")
    OF = pd.read_parquet(ROOT / "open_features.parquet")[["ci", "OPEN_all", "OPEN_home", "OPEN_size"]]
    Dd = pd.read_parquet(DATA / "decomp_inputs.parquet")[["ci", "E2", "EH", "Bn"]]
    O = load_outcomes().all()
    A = pd.concat([pd.read_parquet(RES / "typology_dev_assign.parquet").rename(columns={"dtw_class": "cls"}),
                   pd.read_parquet(RES / "typology_heldout_assign.parquet").rename(columns={"dtw_class_nearest": "cls"})])
    T = J.merge(OF, on="ci").merge(Dd, on="ci").merge(O.drop(columns=["split"]), on="ci").merge(A, on="ci", how="left")
    T["terc"] = np.nan
    for s, g in T.groupby("split"):
        m = g.O2r_resid.notna()
        if m.any():
            T.loc[g.index[m], "terc"] = pd.qcut(g.O2r_resid[m], 3, labels=False).astype(float)
    pcs = [c_ for c_ in ("PC1", "PC2", "PC3") if c_ in T]
    f = lambda v: None if v is None or (isinstance(v, float) and not np.isfinite(v)) else (  # noqa: E731
        round(float(v), 6) if isinstance(v, (float, np.floating)) else v)
    ex = []
    for r in T.itertuples():
        lg = {"log_E2": f(np.log(r.E2)) if r.E2 > 0 else None,
              "log_M": f(np.log(r.EH / r.E2)) if r.E2 > 0 and r.EH > 0 else None,
              "log_rho": f(np.log(r.Bn / r.EH)) if r.EH > 0 and r.Bn > 0 else None}
        ex.append({
            "input": json.dumps({"name": r.name, "group": r.rgroup, "split": r.split, "t0": int(r.t0),
                                 "B5": {b: f(getattr(r, b)) for b in B5}, "OPEN_all": f(r.OPEN_all),
                                 "OPEN_home": f(r.OPEN_home), "OPEN_size": f(r.OPEN_size),
                                 "RETENTION_RATIO_early": f(r.RETENTION_RATIO_early)}),
            "output": json.dumps({"O2r_resid_tercile": None if not np.isfinite(r.terc) else ["bottom", "middle", "top"][int(r.terc)],
                                  "O2r_resid": f(r.O2r_resid), "E2": int(r.E2), "EH": int(r.EH), "Bn": int(r.Bn),
                                  "dtw_class": None if pd.isna(r.cls) else int(r.cls),
                                  **{p: f(getattr(r, p)) for p in pcs}}),
            "predict_open_axis": str(f(r.PC1)),
            "predict_decomposition": json.dumps(lg),
            "metadata_ci": int(r.ci), "metadata_concept_id": int(r.concept_id), "metadata_split": r.split,
            "metadata_group": r.group, "metadata_rgroup": r.rgroup, "metadata_unit": r.unit,
            "metadata_med_home": int(r.med_home), "metadata_in_exp6": int(r.in_exp6),
            "metadata_intersection_born": int(r.intersection_born)})
    cp = jload(RES / "case_pairs.json")
    ex2 = [{"input": json.dumps({"rgroup": p["rgroup"], "high_open": p["high"], "low_open": p["low"],
                                 "OPEN_all": p["OPEN_all"], "logvol": p["logvol"]}),
            "output": json.dumps({"O2r_resid": p["O2r_resid"], "Bn": p["Bn"], "E2": p["E2"], "rho": p["rho"]}),
            "predict_high_open_higher_breadth": str(p["high_open_higher_O2r_resid"]),
            "metadata_pair": p["pair"], "metadata_open_home_order_disagrees": p["open_home_order_disagrees"]}
           for p in cp["pairs"]]
    d4, d4h = jload(RES / "decomposition_dev.json"), jload(RES / "decomposition_heldout.json")
    trd, trh = jload(RES / "trajectories_dev.json"), jload(RES / "trajectories_heldout.json")
    sq, sqh = jload(RES / "sequence_light_dev.json"), jload(RES / "sequence_light_heldout.json")
    prev = jload(ROOT / "method_out.json").get("metadata", {})
    meta = {
        "artifact": "rq2_trajectories_rerun", "status": "complete", "stages_done": prev.get("stages_done", []) + ["S10_outputs"],
        "method_name": "RQ2 contact-vs-retention decomposition + trajectory typology/continuum (cache-only re-run)",
        "description": "Per concept: D3 field-state sequences t0..t0+10, exact log-additive decomposition of retained "
                       "breadth (E2 x M x rho), trajectory continuum (PCA; DTW/HMM typology failed or passed the "
                       "naming rule), OPEN ego-network openness in 3 builds. predict_open_axis = PC1 score; "
                       "predict_decomposition = log factors.",
        "disclosure": DISCLOSURE,
        "headline": {
            "PR_verdicts_DEV": {k: d4["verdicts"][k]["verdict"] for k in ("PR1", "PR1b", "PR2")},
            "PR_verdicts_heldout_pooled4": {k: d4h["pooled_heldout4"]["verdicts"][k]["verdict"] for k in ("PR1", "PR1b", "PR2")},
            "PR_verdicts_cohort": {k: d4h["pooled_cohort"]["verdicts"][k]["verdict"] for k in ("PR1", "PR1b", "PR2")},
            "shares_DEV_primary": {k: d4["variants"]["ii_vol_PRIMARY"]["point"][k] for k in ("s_E2", "s_M", "s_rho")},
            "shares_DEV_PR1_variant": {k: d4["variants"]["iv_vol_noMed_PR1"]["point"][k] for k in ("s_E2", "s_M", "s_rho")},
            "PR1_DEV": d4["verdicts"]["PR1"], "PR1_heldout_pooled4": d4h["pooled_heldout4"]["verdicts"]["PR1"],
            "PR2_DEV": d4["verdicts"]["PR2"], "PR2_heldout_pooled4": d4h["pooled_heldout4"]["verdicts"]["PR2"],
            "D_rho_sign_DEV": d4["verdicts"]["PR3_descriptive"],
            "typology_outcome": trh["outcome"], "ari_dtw_hmm": trd["hmm"]["ari_dtw_hmm"], "k": trd["choose_k"]["k"],
            "hennig_jaccard": trd["stability"]["hennig"]["mean_jaccard"],
            "open_pc1_DEV": {b: trd["open_on_axis"]["pooled"]["PC1"][b] for b in ("all", "home", "size")},
            "open_pc1_heldout_DL": trh["DL_heldout_groups_PC1"],
            "sequence_verdicts": {"DEV": sq["DEV"]["verdict"], "HELDOUT": sqh["HELDOUT"]["verdict"],
                                  "COHORT": sqh["COHORT"]["verdict"]},
            "case_pairs": cp["descriptive_summary"]},
        "pipeline_counts": c,
    }
    out = {"metadata": meta, "datasets": [{"dataset": "rq2_concepts", "examples": ex},
                                          {"dataset": "case_pairs", "examples": ex2}]}
    p = ROOT / "method_out.json"
    tmp = ROOT / "method_out.tmp.json"
    tmp.write_text(json.dumps(out, indent=1, default=float))
    validate_out("S10", tmp, logger)
    tmp.replace(p)
    logger.info(f"method_out.json: {len(ex)} concepts + {len(ex2)} pairs; {p.stat().st_size/1e6:.1f} MB")
    return meta


@logger.catch(reraise=True)
def main() -> None:
    c = pipeline_counts()
    d4, d4h = jload(RES / "decomposition_dev.json"), jload(RES / "decomposition_heldout.json")
    fig_waterfall(d4, d4h)
    fig_forest(d4, d4h)
    tr = jload(RES / "trajectories_dev.json")
    fig_loadings(tr)
    fig_agreement()
    fig_hexbin()
    fig_km(jload(RES / "sequence_light_dev.json"), jload(RES / "sequence_light_heldout.json"))
    method_out(c)


if __name__ == "__main__":
    main()
