#!/usr/bin/env python3
"""S10: figures (PNG + PDF) and the exp_gen_sol_out method output (one example per cohort concept).

fig_ladder          psp by rung, three builds, O2r_m50 / O2r_resid panels; cohort (solid, 95% CI) vs EXP5 (dashed)
fig_forest_groups   per-group psp of OPEN_home at R2 with the DL diamond, cohort and EXP5 side by side
fig_components      the six components alone at R2 (HOME / ALL builds), cohort vs EXP5
fig_within_type     OPEN builds within method / object / property / topic concepts (R3 minus type dummies)
fig_coverage_audit  legacy-tag rate, control TAG/MATCH ratio and venue-label coverage by year (S3 audit)"""
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

from common import DATA, FIGS, RES, ROOT, jdump, setup_logger
from ladder import BUILDS, COMPONENTS, POOL_GROUPS, RUNGS
from outjson import make_method_out

logger = setup_logger("make_outputs")
plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
                     "axes.spines.right": False})
COL = {"home": "#1b6ca8", "all": "#c0392b", "sizematch": "#7d8a2e"}
LAB = {"home": "HOME-ONLY", "all": "ALL-PAPERS", "sizematch": "SIZE-MATCHED"}


def save(fig, name: str) -> None:
    fig.savefig(FIGS / f"{name}.png", dpi=200, bbox_inches="tight")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_ladder(res: dict, sel: dict) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
    xs = np.arange(len(RUNGS))
    for ax, y in zip(axs, ("O2r_m50", "O2r_resid")):
        for j, b in enumerate(BUILDS):
            est = [res["primary"][f"OPEN_{b}|{y}|{r}"]["rho"] for r in RUNGS]
            lo = [res["primary"][f"OPEN_{b}|{y}|{r}"]["ci"][0] for r in RUNGS]
            hi = [res["primary"][f"OPEN_{b}|{y}|{r}"]["ci"][1] for r in RUNGS]
            off = (j - 1) * 0.12
            ax.errorbar(xs + off, est, yerr=[np.subtract(est, lo), np.subtract(hi, est)], fmt="o-", color=COL[b],
                        ms=4, lw=1.2, capsize=2, label=f"{LAB[b]} cohort")
            se = [sel["ladder"][f"OPEN_{b}|{y}|{r}"]["rho"] for r in RUNGS]
            ax.plot(xs + off, se, ls="--", marker="x", color=COL[b], alpha=0.6, lw=1, label=f"{LAB[b]} EXP5 (selection)")
        ax.axhline(0, color="k", lw=0.6)
        ax.set_xticks(xs, ["R0\nB5\n+year", "R1\n+reach", "R2\n+type", "R3\n+foot-\nprint", "R4\n+cover-\nage",
                           "R5\n+group\nFE"], fontsize=7)
        ax.set_title(f"{y}", fontsize=9)
    axs[0].set_ylabel("partial Spearman with OPEN (95% CI)")
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=7, frameon=False, loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.12))
    save(fig, "fig_ladder")


def fig_forest(res: dict, sel: dict) -> None:
    fig, ax = plt.subplots(figsize=(5.2, 3.6))
    rows = POOL_GROUPS + ["MATHDEC"]
    for k, (src, lab, dy, c) in enumerate(((res["groups"]["OPEN_home|O2r_m50|R2"], "cohort 2015-17", -0.15, "#1b6ca8"),
                                           (sel["groups"]["OPEN_home|O2r_m50|R2"], "EXP5 2003-14 (selection)", 0.15,
                                            "#888888"))):
        for i, g in enumerate(rows):
            r = src["groups"][g]
            if not np.isfinite(r["rho"]):
                ax.text(0, i + dy, f"  not estimable (n={r['n']} < 30)", fontsize=6, color=c, va="center")
                continue
            ax.errorbar(r["rho"], i + dy, xerr=[[r["rho"] - r["ci"][0]], [r["ci"][1] - r["rho"]]], fmt="o", color=c,
                        ms=4, capsize=2, label=lab if i == 0 else None)
            ax.text(1.02, i + dy, f"n={r['n']}", transform=ax.get_yaxis_transform(), fontsize=6, color=c, va="center")
        dl = src["DL"]
        yv = len(rows) + dy
        ax.fill([dl["ci"][0], dl["b"], dl["ci"][1], dl["b"]], [yv, yv + 0.12, yv, yv - 0.12], color=c, alpha=0.8)
    ax.set_yticks(list(range(len(rows))) + [len(rows)], rows + [f"DL pooled (5 groups)"])
    ax.axvline(0, color="k", lw=0.6)
    ax.invert_yaxis()
    ax.set_xlabel("partial Spearman OPEN_home ~ O2r_m50 | R2 (95% CI)")
    ax.legend(fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(0.0, -0.13), ncol=2)
    save(fig, "fig_forest_groups")


def fig_components(res: dict, sel: dict) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)
    for ax, b in zip(axs, ("home", "all")):
        xs = np.arange(len(COMPONENTS))
        c = [res["components"][f"{k}__{b}|O2r_m50|R2"] for k in COMPONENTS]
        s = [sel["components"][f"{k}__{b}|O2r_m50|R2"] for k in COMPONENTS]
        ax.errorbar(xs - 0.1, [r["rho"] for r in c], yerr=[[r["rho"] - r["ci"][0] for r in c],
                                                            [r["ci"][1] - r["rho"] for r in c]],
                    fmt="o", color=COL[b], capsize=2, ms=4, label="cohort")
        ax.errorbar(xs + 0.1, [r["rho"] for r in s], yerr=[[r["rho"] - r["ci"][0] for r in s],
                                                            [r["ci"][1] - r["rho"] for r in s]],
                    fmt="s", color="#888888", capsize=2, ms=3, label="EXP5 (selection)")
        ax.axhline(0, color="k", lw=0.6)
        short = {"new_edge_rate": "new edge\nrate (+)", "n_comm_W3": "n comm\nW3 (+)", "participation": "partici-\npation (+)",
                 "NOV_res": "NOV_res\n(+)", "ego_density_W3": "ego dens.\nW3 (-)", "edge_persistence": "edge pers-\nistence (-)"}
        ax.set_xticks(xs, [short[k] for k in COMPONENTS], fontsize=7)
        ax.set_title(f"{LAB[b]} build, O2r_m50 | R2", fontsize=9)
    axs[0].set_ylabel("partial Spearman (95% CI)")
    axs[0].legend(fontsize=7, frameon=False)
    save(fig, "fig_components")


def fig_within_type(res: dict, sel: dict) -> None:
    fig, ax = plt.subplots(figsize=(6, 3.2))
    types = ["method", "object", "property", "topic"]
    for j, b in enumerate(BUILDS):
        xs = np.arange(len(types)) + (j - 1) * 0.22
        r = [res["within_type"][f"OPEN_{b}|{t}|R3"] for t in types]
        est = np.array([v["rho"] for v in r], float)
        ax.errorbar(xs, est, yerr=[est - np.array([v["ci"][0] for v in r]), np.array([v["ci"][1] for v in r]) - est],
                    fmt="o", color=COL[b], capsize=2, ms=4, label=f"{LAB[b]} cohort")
        s = [sel["within_type"][f"OPEN_{b}|{t}|R3"]["rho"] for t in types]
        ax.plot(xs, s, "x", color=COL[b], alpha=0.6)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xticks(np.arange(4), [f"{t}\n(n={res['within_type'][f'OPEN_home|{t}|R3']['n']})" for t in types])
    ax.set_ylabel("partial Spearman | R3 - type (95% CI)")
    ax.set_title("OPEN within concept type (x = EXP5 selection estimate)", fontsize=9)
    ax.legend(fontsize=7, frameon=False)
    save(fig, "fig_within_type")


def fig_coverage() -> None:
    cov = pd.read_csv(RES / "coverage_by_year.csv")
    cov = cov[cov.year >= 2008]
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.plot(cov.year, cov.tag03_rate, "o-", ms=3, label="base works with a legacy tag >= 0.3")
    ax.plot(cov.year, cov.tagany_rate, "s-", ms=3, label="base works with any legacy tag")
    ax.plot(cov.year, cov.control_tag_over_match, "^-", ms=3, label="controls: TAG / title-match hits")
    ax.plot(cov.year, cov.venue_label_coverage, "d-", ms=3, label="venue-field label coverage")
    ax.axvspan(2020.5, 2024.5, color="0.9", zorder=0)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(range(2008, 2025, 2))
    ax.set_xlabel("publication year")
    ax.set_ylabel("share")
    ax.set_title("Outcome-window measurement audit (shaded: cohort outcome years)", fontsize=9)
    ax.legend(fontsize=7, frameon=False, loc="lower left")
    save(fig, "fig_coverage_audit")


def method_out(res: dict) -> None:
    A = pd.read_parquet(DATA / "analysis_cohort.parquet")
    P = pd.read_parquet(DATA / "cohort_predictions.parquet")
    A = A.merge(P, on="ci", how="left")
    rows = []
    for r in A.itertuples():
        d = {"label": r.name, "openalex_id": r.concept_id, "t0": r.t0, "group": r.agroup, "O2r_m50": r.O2r_m50,
             "pred_b5": r.pred_b5, "pred_b5_open": r.pred_b5_open}
        for c in ("OPEN_home", "OPEN_all", "OPEN_sizematch", "type", "generic", "level", "fp_logN", "fp_nfields",
                  "fp_reemerge", "fp_wiki_pre", "newborn", "O2r_resid", "O1c", "O1b", "O3", "O2r_m50_TAG",
                  "O2r_m50_MATCH", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH",
                  "RETENTION_RATIO_early", "n_authors_early", "n_home_early", "n_all_early", "precision_c",
                  "home", "window_flag"):
            v = getattr(r, c)
            d[f"meta_{c}"] = v.item() if hasattr(v, "item") else v
        rows.append(d)
    meta = {"method_name": "OPEN (open-neighbourhood composite) vs B5 baseline, fresh 2015-2017 onset cohort (2017 = declared power extension)",
            "verdict": res["verdict"]["verdict"], "primary_outcome": "O2r_m50",
            "predict_B5": "frozen OLS of O2r_m50 on standardised B5 fitted on the EXP5 frame",
            "predict_B5_plus_OPEN_home": "frozen OLS on B5 + OPEN_home fitted on the EXP5 frame",
            "outcome_grounding": res["grounding"], "n": len(rows)}
    out = make_method_out(rows, meta)
    (ROOT / "full_method_out.json").write_text(json.dumps(out, indent=1))
    logger.info(f"method_out: {len(rows)} examples")


def nan_none(o):
    """JSON null (NaN written by jdump) -> float NaN, recursively."""
    if isinstance(o, dict):
        return {k: nan_none(v) for k, v in o.items()}
    if isinstance(o, list):
        return [nan_none(v) for v in o]
    return float("nan") if o is None else o


def main() -> None:
    res = nan_none(json.loads((RES / "cohort_result.json").read_text()))
    sel = nan_none(json.loads((RES / "exp5_selection_result.json").read_text()))
    fig_ladder(res, sel)
    fig_forest(res, sel)
    fig_components(res, sel)
    fig_within_type(res, sel)
    fig_coverage()
    method_out(res)


if __name__ == "__main__":
    main()
