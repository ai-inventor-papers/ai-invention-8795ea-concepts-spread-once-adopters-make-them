#!/usr/bin/env python3
"""Figures and the executor-contract output method_out.json (exp_gen_sol_out schema)."""
from __future__ import annotations

import json
import math
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

from config import FIGS, LOGS, RES, ROOT  # noqa: E402

GCOL = {"CS": "#1f77b4", "ENG": "#ff7f0e", "BIO": "#2ca02c", "MED": "#d62728"}


def _clean(o):
    if isinstance(o, float) and not math.isfinite(o):
        return None
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return _clean(float(o))
    if isinstance(o, (np.integer,)):
        return int(o)
    return o


def _load(name: str):
    fp = RES / name
    return json.loads(fp.read_text()) if fp.exists() else None


def figures(sr: dict, feats: pd.DataFrame) -> None:
    d = feats[feats.O2r.notna()]
    fig, ax = plt.subplots(1, 2, figsize=(10, 4.2))
    for a, c, lab in ((ax[0], "D_ratio", "D_ratio (distinct communities of new neighbours / null mean)"),
                      (ax[1], "F_res", "F_res (selectivity growth minus size-matched null)")):
        for g, dd in d.groupby("group"):
            a.scatter(dd[c], dd.O2r, s=22, alpha=0.8, color=GCOL.get(g, "k"), label=g)
        a.set_xlabel(lab, fontsize=8)
        a.set_ylabel("O2r (rarefied venue-field richness, m=30)")
    ax[0].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "D_F_vs_O2r.png", dpi=150)
    fig.savefig(FIGS / "D_F_vs_O2r.pdf")
    plt.close(fig)
    # forest plot of per-group delta rho
    fig, ax = plt.subplots(figsize=(6.5, 3.8))
    yk = 0
    labels = []
    for key, c in sr["candidates"].items():
        pg = c["per_group_delta_rho"]
        for g in ["CS", "ENG", "BIO", "MED"]:
            v = pg.get(g)
            if v is not None:
                ax.plot(v, yk, "o", color=GCOL[g])
            labels.append(f"{key}: {g}")
            yk += 1
        lo, hi = c["CI90"]
        ax.errorbar(c["delta_rho"], yk, xerr=[[c["delta_rho"] - (lo if lo is not None else c['delta_rho'])],
                                               [(hi if hi is not None else c['delta_rho']) - c["delta_rho"]]],
                    fmt="s", color="k", capsize=3)
        labels.append(f"{key} [{c['feature']}]: pooled (90% CI)")
        yk += 1
        labels.append("")
        yk += 1
    ax.axvline(0, color="grey", lw=0.8)
    ax.axvline(0.10, color="grey", lw=0.8, ls="--")
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("Delta Spearman (B5 + candidate vs B5), leave-one-group-out, O2r")
    fig.tight_layout()
    fig.savefig(FIGS / "delta_rho_forest.png", dpi=150)
    fig.savefig(FIGS / "delta_rho_forest.pdf")
    plt.close(fig)
    # portability heatmap of within-group rho with O2r
    port = sr["portability"]["indicators"]
    inds = list(port)
    mat = np.array([[port[i]["within_group_rho_O2r"].get(g, np.nan) or np.nan for g in sr["portability"]["groups"]]
                    for i in inds], dtype=float)
    fig, ax = plt.subplots(figsize=(4.6, 0.26 * len(inds) + 1))
    im = ax.imshow(mat, cmap="RdBu_r", vmin=-0.8, vmax=0.8, aspect="auto")
    ax.set_yticks(range(len(inds)))
    ax.set_yticklabels(inds, fontsize=7)
    ax.set_xticks(range(len(sr["portability"]["groups"])))
    ax.set_xticklabels(sr["portability"]["groups"])
    plt.colorbar(im, ax=ax, label="within-group Spearman with O2r")
    fig.tight_layout()
    fig.savefig(FIGS / "portability_heatmap.png", dpi=150)
    fig.savefig(FIGS / "portability_heatmap.pdf")
    plt.close(fig)


def method_out(sr: dict, feats: pd.DataFrame, out: pd.DataFrame, fo: pd.DataFrame) -> dict:
    oof = sr["_oof"]
    oofmap = {c: (b, dz, fr) for c, b, dz, fr in zip(oof["index"], oof["base"], oof["D_ratio"], oof["F_res"])}
    o1 = sr["_oof_O1"]
    o1map = {c: (b, dz, fr) for c, b, dz, fr in zip(o1["index"], o1["base"], o1["D_ratio"], o1["F_res"])}
    ex_main, ex_o1 = [], []
    for _, r in feats.iterrows():
        inp = {"concept": r.concept, "t0": int(r.t0), "home_group": r.group, "newborn": bool(r.newborn),
               "B5": {k: (None if pd.isna(r[k]) else round(float(r[k]), 4)) for k in
                      ["logvol", "growth", "offhome_share", "entropy", "nfields2"]},
               "D_ratio": None if pd.isna(r.D_ratio) else round(float(r.D_ratio), 4),
               "D_z": None if pd.isna(r.D_z) else round(float(r.D_z), 4),
               "F_res": None if pd.isna(r.F_res) else round(float(r.F_res), 4), "M_new_neighbours": int(r.M)}
        if r.concept in oofmap:
            b, dz, fr = oofmap[r.concept]
            ex_main.append({"input": json.dumps(inp), "output": f"{r.O2r:.4f}",
                            "predict_baseline_B5": f"{b:.4f}", "predict_B5_plus_D_ratio": f"{dz:.4f}",
                            "predict_B5_plus_F_res": f"{fr:.4f}",
                            "metadata_group": r.group, "metadata_fold": f"left-out group {r.group}",
                            "metadata_outcome": "O2r (rarefied venue-field richness at m=30, t0+6..t0+8)",
                            "metadata_N_WO": int(r.N_WO), "metadata_t0": int(r.t0)})
        if r.concept in o1map:
            b, dz, fr = o1map[r.concept]
            ex_o1.append({"input": json.dumps(inp), "output": str(int(r.O1)),
                          "predict_baseline_B5": f"{b:.4f}", "predict_B5_plus_D_ratio": f"{dz:.4f}",
                          "predict_B5_plus_F_res": f"{fr:.4f}", "metadata_group": r.group,
                          "metadata_outcome": "O1 sustained uptake (P(O1=1) from LOGO logistic)"})
    from screen import BF, logo
    yf = fo.R_j.to_numpy(float)
    gf = fo.group.to_numpy()
    pf = {"base": logo(fo[BF].to_numpy(float), yf, gf, "logit"),
          "Dj": logo(fo[BF + ["Dj"]].to_numpy(float), yf, gf, "logit"),
          "Fj": logo(fo[BF + ["Fj", "Fj_missing"]].to_numpy(float), yf, gf, "logit")}
    ex_field = []
    for i, (_, r) in enumerate(fo.iterrows()):
        ex_field.append({"input": json.dumps({"concept": r.concept, "field": int(r.field), "n_j_early": int(r.n_j_early),
                                              "share_j_early": round(float(r.share_j), 4),
                                              "growth_j": round(float(r.growth_j), 4),
                                              "Dj": None if pd.isna(r.Dj) else round(float(r.Dj), 4),
                                              "Fj": None if pd.isna(r.Fj) else round(float(r.Fj), 4)}),
                         "output": str(int(r.R_j)), "metadata_group": str(r.group),
                         "predict_baseline_B_field": f"{pf['base'][i]:.4f}",
                         "predict_B_field_plus_Dj": f"{pf['Dj'][i]:.4f}",
                         "predict_B_field_plus_Fj": f"{pf['Fj'][i]:.4f}",
                         "metadata_outcome": "R_j field-level retention"})
    drops = out[out.dropped_reason.notna() & (out.dropped_reason != "")]
    meta = {"method_name": "Co-occurrence screen: structural diversity D and frequency-free selectivity F vs B5",
            "artifact": "gen_art_experiment_3 (iteration 1 wide screen)",
            "screen_label": sr["screen_label"],
            "summary": {k: {kk: v[kk] for kk in ["delta_rho", "CI90", "CI95", "per_group_delta_rho",
                                                 "n_groups_positive", "rho_logvol", "rho_growth", "reliability",
                                                 "criteria", "survives", "dissociation", "field_level", "role",
                                                 "delta_AUC_O1", "delta_AUC_O1_CI90", "delta_AUC_O3",
                                                 "delta_AUC_O3_CI90", "delta_AUC_O2r_top", "delta_AUC_O2r_top_CI90",
                                                 "delta_AUC_reach30", "delta_AUC_reach30_CI90"] if kk in v}
                        for k, v in sr["candidates"].items()},
            "survivors": sr["survivors"], "carried_forward": sr["carried_forward"],
            "ranking_by_delta_rho": sr["ranking_by_delta_rho"],
            "base_metrics": sr["base_metrics"], "n_dev_concepts": sr["n_dev_concepts"], "n_used_O2r": sr["n_used_O2r"],
            "n_per_group": sr["n_per_group"],
            "n_dropped_by_reason": drops.dropped_reason.str.split(":").str[0].value_counts().to_dict(),
            "sanity": sr["sanity"], "sensitivities": sr["sensitivities"],
            "portability_kendall_W": sr["portability"]["kendall_W_indicator_ranks_O2r"],
            "indicator_matrix": sr["portability"]["indicators"],
            "credits": json.loads((RES / "credit_ledger.json").read_text()),
            "backbone": json.loads((RES / "backbone_summary.json").read_text()),
            "deviations": json.loads((RES / "deviations.json").read_text()) if (RES / "deviations.json").exists() else [],
            "outcome_estimability": sr.get("outcome_estimability"), "O3_positives_by_group": sr.get("O3_positives_by_group"),
            "exploratory_partial_association": _load("exploratory_partial_association.json"),
            "T6_bootstrap_seed_stability": _load("t6_bootstrap_stability.json"),
            "T0_unit_tests": _load("unit_tests_T0.json")}
    return _clean({"metadata": meta, "datasets": [
        {"dataset": "P78_dev_concepts_O2r_LOGO", "examples": ex_main},
        {"dataset": "P78_dev_concepts_O1_LOGO", "examples": ex_o1},
        {"dataset": "P78_dev_concept_x_field_R_j", "examples": ex_field}]})


@logger.catch(reraise=True)
def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "make_outputs.log", rotation="30 MB", level="DEBUG")
    sr = json.loads((RES / "screen_result.json").read_text())
    feats = pd.read_csv(RES / "features.csv")
    out = pd.read_csv(RES / "outcomes.csv")
    feats = feats.merge(out[["concept", "O1", "O2r", "O3", "N_WO"]], on="concept", how="left")
    fo = pd.read_csv(RES / "field_outcomes.csv")
    figures(sr, feats)
    mo = method_out(sr, feats, out, fo)
    (ROOT / "method_out.json").write_text(json.dumps(mo, indent=1))
    logger.info(f"method_out.json: {[len(d['examples']) for d in mo['datasets']]} examples")


if __name__ == "__main__":
    main()
