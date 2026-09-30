#!/usr/bin/env python3
"""S9 outputs: figures (PNG + PDF) and method_out.json (exp_gen_sol_out; one example per Frame-N concept).

fig_ladder            4 indices x R0..R5 (95% CI) on the primary outcome; EXP10 cohort OPEN_home overlaid in grey
fig_forest_groups     per-group psp at R3 (OPEN_home, NOVCHURN_home) with the DL diamond
fig_components        the six components alone at R3 (HOME vs ALL builds)
fig_cheng_reversal    Cheng consistency: raw rho with V_next vs size-controlled vs psp with breadth / other outcomes
fig_coupling          OPEN_home / OPEN_sizematch / OPEN_all at R3 + paired differences
fig_pipeline_counts   candidates -> exclusions -> onset -> gated -> OPEN_home -> primary outcome
fig_survivorship      Frame N vs legacy (raw and reweighted) base rates
Usage: python make_outputs_n.py [--dryrun]"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from common import DATA, FIGS, INPUTS, RES, ROOT, jdump, setup_logger

logger = setup_logger("make_outputs_n")
plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
                     "axes.spines.right": False})
RUNGS = ["R0", "R1", "R2", "R3", "R4", "R5"]
IDX = ["OPEN_home", "NOVCHURN_home", "OPEN_sizematch", "OPEN_all"]
COL = {"OPEN_home": "#1b6ca8", "NOVCHURN_home": "#8e44ad", "OPEN_sizematch": "#7d8a2e", "OPEN_all": "#c0392b"}
GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]


def save(fig, name: str, tag: str) -> None:
    fig.savefig(FIGS / f"{name}{tag}.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIGS / f"{name}{tag}.pdf", bbox_inches="tight")
    plt.close(fig)


def err(ax, x, c, **kw):
    ax.errorbar(x, c["rho"], yerr=[[c["rho"] - c["ci"][0]], [c["ci"][1] - c["rho"]]], fmt="o", capsize=2, ms=4, **kw)


def fig_ladder(res: dict, prim: str, tag: str) -> None:
    C = res["cells"]
    ex10 = json.loads((INPUTS / "cohort_result.json").read_text())["primary"]
    fig, axs = plt.subplots(1, 2, figsize=(9.5, 3.5), sharey=True)
    xs = np.arange(len(RUNGS))
    for ax, y in zip(axs, (prim, "O2r_resid")):
        for j, x in enumerate(IDX):
            est = [C[f"ladder|{x}|{y}|{r}"]["rho"] for r in RUNGS]
            lo = [C[f"ladder|{x}|{y}|{r}"]["ci"][0] for r in RUNGS]
            hi = [C[f"ladder|{x}|{y}|{r}"]["ci"][1] for r in RUNGS]
            off = (j - 1.5) * 0.1
            ax.errorbar(xs + off, est, yerr=[np.subtract(est, lo), np.subtract(hi, est)], fmt="o-", color=COL[x],
                        ms=3.5, lw=1.1, capsize=2, label=f"{x} (Frame N)")
        e10 = [ex10[f"OPEN_home|{'O2r_m50' if y != 'O2r_resid' else 'O2r_resid'}|{r}"]["rho"] for r in RUNGS]
        ax.plot(xs, e10, color="grey", ls="--", marker="x", lw=1, label="OPEN_home, EXP10 legacy cohort (n=573)")
        ax.axhline(0, color="k", lw=0.6)
        ax.set_xticks(xs, ["R0\nB5+year", "R1\n+reach", "R2\n+type", "R3\n+foot-\nprint", "R4\n+cover-\nage",
                           "R5\n+group\nFE"], fontsize=7)
        ax.set_title(y, fontsize=9)
    axs[0].set_ylabel("partial Spearman (95% concept-bootstrap CI)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, frameon=False, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.14))
    save(fig, "fig_ladder", tag)


def fig_forest(res: dict, prim: str, tag: str) -> None:
    C = res["cells"]
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2), sharex=True)
    for ax, x in zip(axs, ("OPEN_home", "NOVCHURN_home")):
        g = C[f"groups|{x}|{prim}|R3"]
        ys = []
        for i, k in enumerate(GROUPS):
            c = g["groups"][k]
            if c["rho"] is not None:
                ax.errorbar(c["rho"], i, xerr=[[c["rho"] - c["ci"][0]], [c["ci"][1] - c["rho"]]], fmt="s",
                            color=COL[x], capsize=2, ms=4)
            ys.append(f"{k} (n={c['n']})")
        if g["DL"]:
            d = g["DL"]
            ax.errorbar(d["b"], len(GROUPS), xerr=[[d["b"] - d["ci"][0]], [d["ci"][1] - d["b"]]], fmt="D",
                        color="k", capsize=2, ms=5)
            ys.append(f"DL pooled (I2={d['I2']:.2f})")
        ax.set_yticks(range(len(ys)), ys, fontsize=7)
        ax.axvline(0, color="k", lw=0.6)
        ax.set_title(f"{x} | {prim} | R3", fontsize=9)
        ax.invert_yaxis()
    axs[0].set_xlabel("partial Spearman")
    axs[1].set_xlabel("partial Spearman")
    save(fig, "fig_forest_groups", tag)


def fig_components(res: dict, prim: str, tag: str) -> None:
    C = res["cells"]
    comps = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
    fig, ax = plt.subplots(figsize=(6.5, 3.2))
    for j, (b, col) in enumerate((("home", "#1b6ca8"), ("all", "#c0392b"))):
        for i, k in enumerate(comps):
            c = C[f"comp|{k}__{b}|{prim}|R3"]
            err(ax, i + (j - 0.5) * 0.25, c, color=col, label=f"{b.upper()} build" if i == 0 else None)
    ax.set_xticks(range(len(comps)), comps, rotation=20, fontsize=7)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel(f"psp with {prim} | R3")
    ax.legend(fontsize=7, frameon=False)
    save(fig, "fig_components", tag)


def fig_cheng(res: dict, prim: str, tag: str) -> None:
    C = res["cells"]
    keys = [("cheng|CHENG_consistency_home|V_next|raw", "V_next raw rho\n(Cheng's DV)"),
            ("cheng|CHENG_consistency_home|V_next|logN2", "V_next | log N(t0+2)"),
            ("cheng|CHENG_consistency_home|V_next|R0", "V_next | R0"),
            (f"cheng|CHENG_consistency_home|{prim}|R0", f"{prim} | R0"),
            ("cheng|CHENG_consistency_home|O2r_resid|R0", "O2r_resid | R0"),
            ("cheng|CHENG_consistency_home|O3|R0", "O3 | R0"), ("cheng|CHENG_consistency_home|O1b|R0", "O1b | R0"),
            ("cheng|CHENG_consistency_home|O1c|R0", "O1c | R0")]
    fig, ax = plt.subplots(figsize=(7, 3.2))
    for i, (k, lab) in enumerate(keys):
        err(ax, i, C[k], color="#d35400" if i < 3 else "#2c3e50")
    ax.set_xticks(range(len(keys)), [l for _, l in keys], fontsize=7, rotation=15)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_ylabel("Spearman / partial Spearman (95% CI)")
    ax.set_title("Cheng et al. 2023 ideational consistency (home papers, topics as terms)", fontsize=9)
    save(fig, "fig_cheng_reversal", tag)


def fig_coupling(res: dict, prim: str, tag: str) -> None:
    C = res["cells"]
    fig, axs = plt.subplots(1, 2, figsize=(8, 3), gridspec_kw={"width_ratios": [3, 2]})
    for i, x in enumerate(("OPEN_home", "OPEN_sizematch", "OPEN_all")):
        err(axs[0], i, C[f"ladder|{x}|{prim}|R3"], color=COL[x])
    axs[0].set_xticks(range(3), ["HOME only", "SIZE-matched", "ALL papers"])
    axs[0].axhline(0, color="k", lw=0.6)
    axs[0].set_ylabel(f"psp with {prim} | R3")
    for i, k in enumerate(("all_minus_home", "sizematch_minus_home")):
        c = C[f"coupling|{k}|R3"]
        axs[1].errorbar(i, c["diff"], yerr=[[c["diff"] - c["ci"][0]], [c["ci"][1] - c["diff"]]], fmt="o", capsize=2,
                        color="k")
    axs[1].set_xticks(range(2), ["ALL - HOME", "SIZEMATCH - HOME"])
    axs[1].axhline(0, color="k", lw=0.6)
    axs[1].set_ylabel("paired psp difference")
    save(fig, "fig_coupling", tag)


def fig_pipeline(counts: list[tuple[str, int]], tag: str) -> None:
    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    labs = [l for l, _ in counts]
    vals = [v for _, v in counts]
    ax.barh(range(len(vals)), vals, color="#1b6ca8")
    for i, v in enumerate(vals):
        ax.text(v, i, f" {v:,}", va="center", fontsize=7)
    ax.set_yticks(range(len(vals)), labs, fontsize=7)
    ax.set_xscale("log")
    ax.invert_yaxis()
    ax.set_xlabel("phrases (log scale)")
    save(fig, "fig_pipeline_counts", tag)


def fig_surv(surv: dict, tag: str) -> None:
    ms = surv["measures"]
    fig, axs = plt.subplots(1, len(ms), figsize=(10, 2.8))
    for ax, (k, v) in zip(axs, ms.items()):
        ax.bar([0, 1, 2], [v["frame_n_mean"], v["legacy_raw_mean"], v["legacy_reweighted_mean"]],
               color=["#1b6ca8", "#95a5a6", "#7f8c8d"])
        ax.set_xticks([0, 1, 2], ["Frame N", "legacy\nraw", "legacy\nreweighted"], fontsize=7)
        ax.set_title(k.replace("_vs_legacy_", " vs ") + f"\nrel diff {v['rel_diff_vs_reweighted']:+.0%}", fontsize=7)
    save(fig, "fig_survivorship", tag)


def pipeline_counts() -> list[tuple[str, int]]:
    """All counts include the t0 = 2015 extension onsets (fallback E was triggered, so they are in the frame)."""
    s3 = json.loads((RES / "s3_summary.json").read_text())
    s5 = json.loads((RES / "s5_onset.json").read_text())
    fr = pd.read_csv(DATA / "frame_n_concepts.csv")
    an = pd.read_parquet(DATA / "analysis_frame_n.parquet")
    g = pd.read_csv(DATA / "gate_m1.csv")
    res = json.loads((RES / "frame_n_result.json").read_text())
    prim = res["primary_outcome"]
    return [("mined title n-gram keys (20% sample, k=3 superset)", s3["U_superset"]),
            ("candidate rule, k_t = 4", s3["after_k_t"]), ("after legacy / generic / place exclusions", s3["after_lexical"]),
            ("after POS filter (Pass-N candidates)", s3["retained"]),
            ("full-corpus onset 2003-2015 + selection clause", s5["onset_2003_2014"] + s5["extension_2015"]),
            ("after containment dedup + home", s5["after_s5a"]), ("LLM-gated (M1)", int(g.gated.sum())),
            ("kept: M1 sense rule AND G2 concept", int(len(fr))),
            ("finite OPEN_home", int(np.isfinite(an.OPEN_home).sum())),
            (f"finite OPEN_home & {prim} (primary set)", int((np.isfinite(an.OPEN_home) & np.isfinite(an[prim])).sum())),
            ("finite OPEN_home & O2r_m50", int((np.isfinite(an.OPEN_home) & np.isfinite(an.O2r_m50)).sum()))]


def method_out(df: pd.DataFrame, prim: str, res: dict) -> dict:
    def s(v):
        if v is None or (isinstance(v, float) and not np.isfinite(v)):
            return "NA"
        return f"{float(v):.6g}"
    ex = []
    for r in df.itertuples():
        ex.append({"input": json.dumps({"phrase": r.name, "t0": int(r.t0), "home_fields": str(r.home),
                                        "home_group": r.agroup, "logvol": round(float(r.logvol), 4),
                                        "growth_c": round(float(r.growth_c), 4),
                                        "offhome_share": None if not np.isfinite(r.offhome_share) else round(float(r.offhome_share), 4),
                                        "entropy": None if not np.isfinite(r.entropy) else round(float(r.entropy), 4),
                                        "reach": int(r.reach)}, ensure_ascii=False),
                   "output": s(getattr(r, prim)),
                   "predict_B5": s(r.pred_b5), "predict_B5_plus_OPEN_home": s(r.pred_b5_open),
                   "predict_B5_plus_NOVCHURN": s(r.pred_b5_novchurn_cv),
                   "metadata_ci": int(r.ci), "metadata_gloss": str(r.gloss), "metadata_type": str(r.type),
                   "metadata_OPEN_home": None if not np.isfinite(r.OPEN_home) else float(r.OPEN_home),
                   "metadata_NOVCHURN_home": None if not np.isfinite(r.NOVCHURN_home) else float(r.NOVCHURN_home),
                   "metadata_CHENG_consistency_home": None if not np.isfinite(r.CHENG_consistency_home) else float(r.CHENG_consistency_home),
                   "metadata_O2r_resid": None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid),
                   "metadata_O2r_m50": None if not np.isfinite(r.O2r_m50) else float(r.O2r_m50),
                   "metadata_O2r_m30": None if not np.isfinite(r.O2r_m30) else float(r.O2r_m30),
                   "metadata_t0_extension_2015": int(r.extension),
                   "metadata_O3": None if not np.isfinite(r.O3) else int(r.O3),
                   "metadata_O1b": None if not np.isfinite(r.O1b) else int(r.O1b),
                   "metadata_V_next": None if not np.isfinite(r.V_next) else float(r.V_next)})
    v = res["verdicts"]
    meta = {"method_name": "Frame-N confirmation of the home-neighbourhood churn signal (OPEN_home / NOVCHURN_home)",
            "description": "Vocabulary-free newborn title phrases (2003-2014 onsets, not in the legacy OpenAlex/MAG "
                           "vocabulary); early (t0-3..t0+2) ego-network indices vs later venue-field breadth "
                           f"({prim}, t0+6..t0+8). output = observed {prim}; predict_B5 / predict_B5_plus_OPEN_home = "
                           "frozen EXP5-fitted OLS (fitted on the O2r_m50 scale; compare by rank); predict_B5_plus_NOVCHURN = 5-fold CV OLS "
                           f"on Frame N ({prim} scale). The primary outcome is {prim} because declared fallback A "
                           "triggered (< 800 concepts with finite O2r_m50 and OPEN_home).",
            "primary_outcome": prim, "verdict": v["verdict"], "n": int(len(df))}
    return {"metadata": meta, "datasets": [{"dataset": "frame_n_newborn_title_phrases_2003_2014", "examples": ex}]}


def main() -> None:
    tag = "_dryrun" if "--dryrun" in sys.argv else ""
    res = json.loads((RES / f"frame_n_result{tag}.json").read_text())
    prim = res["primary_outcome"]
    fig_ladder(res, prim, tag)
    fig_forest(res, prim, tag)
    fig_components(res, prim, tag)
    fig_cheng(res, prim, tag)
    fig_coupling(res, prim, tag)
    fig_surv(res["survivorship"], tag)
    if not tag:
        pc = pipeline_counts()
        jdump(dict(pc), RES / "pipeline_counts.json")
        fig_pipeline(pc, tag)
        df = pd.read_parquet(DATA / "analysis_frame_n.parquet")
        out = method_out(df, prim, res)
        (ROOT / "method_out.json").write_text(json.dumps(out, indent=1))
        logger.info(f"method_out.json: {len(out['datasets'][0]['examples'])} examples")
    logger.info("figures written")


if __name__ == "__main__":
    main()
