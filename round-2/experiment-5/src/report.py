#!/usr/bin/env python3
"""STEP 10: figures (PNG + PDF) and method_out.json (exp_gen_sol_out schema).

One example per episode (dev: OOF LOGO predictions; held-out / cohort: frozen dev-fitted model predictions);
metadata = headline numbers and verdicts."""
from __future__ import annotations

import json
import math

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from common import FIELD_NAMES, FIGS, GROUP_OF_FIELD, RES, ROOT, jdump, setup_logger  # noqa: E402
from models import X0, X1  # noqa: E402

logger = setup_logger("report")
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "pdf.fonttype": 42,
                     "ps.fonttype": 42, "savefig.dpi": 200})
C_DEV, C_HO, C_POOL, C_GREY = "#3b6ea8", "#c0504d", "#222222", "#9a9a9a"


def save(fig, name: str) -> None:
    fig.savefig(FIGS / f"{name}.png", bbox_inches="tight")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_forest(dev: dict, ho: dict) -> None:
    rows = []
    for g, v in dev["primary"]["per_group"].items():
        se = v.get("boot_se", math.nan)
        rows.append((f"DEV {g} (LOGO, n={v['n']})", v["dauc"], v["dauc"] - 1.96 * se, v["dauc"] + 1.96 * se, C_DEV))
    rows.append((f"DEV pooled OOF (n={dev['n_episodes']})", dev["primary"]["dauc"], *dev["primary"]["boot_ci95"], C_DEV))
    for g, v in ho["primary"]["per_group"].items():
        lo, hi = v.get("boot_ci95", [math.nan, math.nan])
        rows.append((f"HELD-OUT {g} (n={v['n']}, {v['n_concepts']} c.)", v["dauc"], lo, hi, C_HO))
    c = ho["cohort"]
    rows.append((f"COHORT 2010-14 (n={c['n']})", c["dauc"], *c.get("boot_ci95", [math.nan, math.nan]), C_HO))
    dl = ho["dl_pool"]
    if dl.get("k"):
        rows.append((f"HELD-OUT DL pooled (k={dl['k']}, I²={dl['I2']:.2f})", dl["pooled"], *dl["ci95"], C_POOL))
    rows.append((f"HELD-OUT pooled episodes (n={ho['primary']['n']})", ho["primary"]["dauc"],
                 *ho["primary"]["boot_ci95"], C_POOL))
    fig, ax = plt.subplots(figsize=(7.2, 0.36 * len(rows) + 1.2))
    for i, (lab, e, lo, hi, col) in enumerate(rows[::-1]):
        ax.plot([lo, hi], [i, i], color=col, lw=1.6)
        ax.plot(e, i, "o" if "pooled" not in lab else "D", color=col, ms=6)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.axvline(0, color=C_GREY, lw=0.8, ls="--")
    ax.axvline(0.05, color=C_GREY, lw=0.8, ls=":")
    ax.set_xlabel("ΔAUC of adding gateway_j to X0 (95% CI)")
    ax.set_title("Gateway centrality and retention of adopted concepts")
    save(fig, "forest_dauc")


def fig_placebo(dev: dict, ho: dict) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2))
    for ax, d, nm in ((axs[0], dev, "DEV (LOGO)"), (axs[1], ho, "HELD-OUT")):
        v = np.array(d["placebo_rewired"]["values"], float)
        real = d["primary"]["dauc"]
        ax.hist(v, bins=30, color=C_GREY, alpha=0.8, label="200 rewired backbones")
        pv = np.array(d["placebo_permutation"]["values"], float)
        ax.hist(pv, bins=30, histtype="step", color=C_DEV, label="200 field permutations")
        ax.axvline(real, color=C_HO, lw=2, label=f"real ΔAUC {real:+.3f}")
        ax.axvline(np.nanpercentile(v, 95), color="k", ls=":", lw=1, label="rewired 95th pct")
        ax.set_title(nm)
        ax.set_xlabel("ΔAUC")
    axs[0].legend(fontsize=7, frameon=False)
    save(fig, "placebo_hist")


def fig_coef(dev: dict, ho: dict) -> None:
    rows = []
    for nm, d, col in (("DEV", dev, C_DEV), ("HELD-OUT", ho, C_HO)):
        cl = d["cond_logit"]
        if "beta_gateway_std" in cl:
            rows.append((f"{nm} conditional logit (concept FE)", cl["beta_gateway_std"], cl["se"], col))
        lp = d["lpm_field_fe"]
        if "beta_within_per_sd" in lp:
            rows.append((f"{nm} LPM field FE, gateway_j,s (x10)", 10 * lp["beta_within_per_sd"], 10 * lp["se_concept"], col))
        for k in ("concept", "twoway", "field"):
            v = d["logit_clustered_se"].get(k, {})
            if "beta_gateway_std" in v:
                rows.append((f"{nm} logit X1, {k}-clustered SE", v["beta_gateway_std"], v["se"], col))
        b = d["boundary"]
        if "beta_interaction" in b:
            rows.append((f"{nm} gateway x top-tercile home", b["beta_interaction"], b["se"], col))
    fig, ax = plt.subplots(figsize=(7.2, 0.33 * len(rows) + 1.0))
    for i, (lab, e, se, col) in enumerate(rows[::-1]):
        ax.plot([e - 1.96 * se, e + 1.96 * se], [i, i], color=col, lw=1.6)
        ax.plot(e, i, "o", color=col)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.axvline(0, color=C_GREY, ls="--", lw=0.8)
    ax.set_xlabel("standardised coefficient of gateway (95% CI)")
    save(fig, "coef_secondary")


def fig_lofo(ho: dict, dev: dict) -> None:
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.2), sharey=False)
    for ax, d, nm, ref in ((axs[0], dev, "DEV", dev["leave_one_field_out"]["full"]), (axs[1], ho, "HELD-OUT", ho["primary"]["dauc"])):
        bf = d["leave_one_field_out"]["by_field"]
        ks = sorted(bf, key=lambda k: bf[k])
        ax.barh(range(len(ks)), [bf[k] for k in ks], color=[C_DEV if nm == "DEV" else C_HO] * len(ks))
        ax.set_yticks(range(len(ks)))
        ax.set_yticklabels([FIELD_NAMES[int(k)][:28] for k in ks], fontsize=6.5)
        ax.axvline(ref, color="k", lw=1, ls=":")
        ax.axvline(0, color=C_GREY, lw=0.8)
        ax.set_title(f"{nm}: ΔAUC leaving one adopting field out")
    save(fig, "leave_one_field_out")


def fig_ladder(dev: dict, ho: dict) -> None:
    order = ["L0_size_only", "L1_iter1_base", "L2_plus_relatedness", "L3_plus_Pj", "L4_full_X0"]
    labels = ["size only", "iteration-1 base\n(B5 + size)", "+ phi_home,\ndensity", "+ P_j(-c)", "full X0\n(+ coverage)"]
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    for d, col, off, nm in ((dev, C_DEV, -0.1, "DEV (LOGO OOF)"), (ho, C_HO, 0.1, "HELD-OUT (frozen dev fit)")):
        e = [d["ladder"][k]["dauc"] for k in order]
        lo = [d["ladder"][k]["ci95"][0] for k in order]
        hi = [d["ladder"][k]["ci95"][1] for k in order]
        x = np.arange(len(order)) + off
        ax.errorbar(x, e, yerr=[np.subtract(e, lo), np.subtract(hi, e)], fmt="o", color=col, capsize=3, label=nm)
    ax.axhline(0, color=C_GREY, ls="--", lw=0.8)
    ax.set_xticks(range(len(order)))
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("ΔAUC of adding gateway_j (95% CI)")
    ax.set_title(f"Gateway alone: AUC {dev['gateway_alone_auc']:.3f} (dev) vs {ho['gateway_alone_auc']:.3f} (held-out)", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    save(fig, "ladder_dauc")


def fig_gateway_map() -> None:
    b = json.loads((RES / "backbones.json").read_text())
    g = np.array(b["gateway_frozen"])
    rec = np.array(b["recomputed"]["S0"]["eig"])
    order = np.argsort(g)
    cmap = {"CS": "#1f77b4", "Eng": "#17becf", "BGM": "#2ca02c", "Med": "#d62728", "PHYS": "#9467bd",
            "LIFEENV": "#8c564b", "SOC": "#e377c2", "MATHDEC": "#7f7f7f"}
    fids = b["field_ids"]
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.barh(range(26), g[order], color=[cmap[GROUP_OF_FIELD[fids[i]]] for i in order])
    ax.plot(rec[order], range(26), "k|", ms=10, label=f"recomputed S0 (ρ={b['check_spearman_S0_recomputed_vs_frozen']:.2f})")
    ax.set_yticks(range(26))
    ax.set_yticklabels([FIELD_NAMES[fids[i]] for i in order], fontsize=7)
    ax.set_xlabel("frozen 1998-2002 eigenvector gateway centrality (max = 1)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=v, label=k) for k, v in cmap.items()] +
              [plt.Line2D([], [], color="k", marker="|", ls="", label="recomputed S0")], fontsize=7, frameon=False,
              loc="lower right")
    save(fig, "gateway_map")


def method_out(dev: dict, ho: dict, h3: dict) -> None:
    D = pd.read_csv(ROOT / "dev_episodes_with_oof.csv")
    H = pd.read_csv(ROOT / "heldout_episodes_with_pred.csv")
    Cc = pd.read_csv(ROOT / "cohort_episodes_with_pred.csv")

    def ex(r, p0, p1, split):
        cov = {c: (None if pd.isna(getattr(r, c)) else round(float(getattr(r, c)), 5)) for c in X1}
        inp = {"concept_id": int(r.concept_id), "concept": r.name, "adopting_field": int(r.field),
               "adopting_field_name": FIELD_NAMES[int(r.field)], "home": str(r.home), "t0": int(r.t0),
               "group": r.group, "split": split, "covariates": cov}
        return {"input": json.dumps(inp, ensure_ascii=False), "output": str(int(r.R)),
                "predict_baseline": f"{p0:.6f}", "predict_gateway": f"{p1:.6f}",
                "metadata_split": split, "metadata_group": r.group, "metadata_concept_id": int(r.concept_id),
                "metadata_field": int(r.field), "metadata_n_early": float(r.n_early),
                "metadata_n_out": float(r.n_out), "metadata_gateway_j": float(r.gateway_j)}
    ds = [{"dataset": "episodes_dev_LOGO_oof", "examples": [ex(r, r.oof_X0, r.oof_X1, "DEV") for r in D.itertuples()]},
          {"dataset": "episodes_heldout_frozen_model", "examples": [ex(r, r.pred_X0, r.pred_X1, r.split) for r in H.itertuples()]},
          {"dataset": "episodes_cohort_2010_2014_frozen_model",
           "examples": [ex(r, r.pred_X0, r.pred_X1, "COHORT") for r in Cc.itertuples()]}]
    fs = json.loads((RES / "frame_summary.json").read_text())
    gr = json.loads((ROOT / "grounding_report.json").read_text())
    meta = {"method_name": "Held-out test of adopting-field gateway centrality for concept retention (H1) and "
                           "concept-level gateway landing vs size-adjusted breadth (H3)",
            "description": "One zero-credit scan of the full OpenAlex works snapshot (2,040 parquet files); legacy "
                           "concept lexicon (levels 2-5) + Wikidata aliases; Aho-Corasick title matching with stemmed "
                           "verification; grounding by legacy concept tags validated on an LLM-labelled benchmark and a "
                           "per-concept LLM precision gate; frozen dev specification (hashed) scored once on sealed "
                           "held-out home groups and the 2010-2014 cohort.",
            "baseline": "X0 = B5 + log field size + phi(home,j) + relatedness density + P_j(-c) + coverage + episode size",
            "method": "X1 = X0 + frozen 1998-2002 eigenvector gateway centrality of the adopting field",
            "frame": fs, "grounding": {k: gr.get(k) for k in ("frozen_grounding_rule", "kappa_l1_l2", "rules_test",
                                                               "handcheck", "filter")},
            "H1_dev": {k: dev[k] for k in ("n_episodes", "n_concepts", "R_rate")} | {
                "dauc": dev["primary"]["dauc"], "ci95": dev["primary"]["boot_ci95"],
                "per_group": {g: v["dauc"] for g, v in dev["primary"]["per_group"].items()},
                "placebo_real_exceeds_p95": dev["placebo_rewired"]["real_exceeds_p95"],
                "cond_logit": dev["cond_logit"], "lpm": dev["lpm_field_fe"]},
            "H1_heldout": {"dauc": ho["primary"]["dauc"], "ci95": ho["primary"]["boot_ci95"],
                           "auc_X0": ho["primary"]["auc_X0"], "auc_X1": ho["primary"]["auc_X1"],
                           "per_group": {g: v["dauc"] for g, v in ho["primary"]["per_group"].items()},
                           "dl_pool": ho["dl_pool"], "cohort_dauc": ho["cohort"]["dauc"],
                           "cohort_ci95": ho["cohort"].get("boot_ci95"), "verdict": ho["verdict_H1"],
                           "placebo_p95": ho["placebo_rewired"]["p95"], "cond_logit": ho["cond_logit"],
                           "lpm": ho["lpm_field_fe"], "rival_head_to_head": ho["rival_head_to_head"],
                           "pigeonhole_ci95": ho["pigeonhole_crossed_bootstrap"]["ci95"]},
            "ladder_dev": {k: v["dauc"] for k, v in dev["ladder"].items()},
            "ladder_heldout": {k: v["dauc"] for k, v in ho["ladder"].items()},
            "gateway_alone_auc": {"dev": dev["gateway_alone_auc"], "heldout": ho["gateway_alone_auc"]},
            "H3_heldout": {v: {"partial_rho": h3[v]["partial_rho"], "p": h3[v]["p_perm_one_sided"],
                               "ci95": h3[v]["ci95"]} for v in ("G", "G_A", "G_btw", "REL_home")}
                          | {"holm": h3["holm_adjusted_p"], "verdict": h3["verdict_H3"],
                             "verdict_qualified": h3.get("verdict_H3_qualified"),
                             "dl_pool_G": h3["G"]["dl_pool"]},
            "files": {"h1_dev": "results/h1_dev.json", "h1_heldout": "results/h1_heldout.json",
                      "h3": "results/h3_results.json", "frozen_spec": "frozen_spec.json", "seal_log": "logs/seal.log",
                      "deviations": "results/deviations.json"}}
    out = {"metadata": meta, "datasets": ds}
    jdump(out, ROOT / "method_out.json")
    logger.info(f"method_out.json: {sum(len(d['examples']) for d in ds)} examples")


def main() -> None:
    dev = json.loads((RES / "h1_dev.json").read_text())
    ho = json.loads((RES / "h1_heldout.json").read_text())
    h3 = json.loads((RES / "h3_results.json").read_text())
    fig_forest(dev, ho)
    fig_placebo(dev, ho)
    fig_coef(dev, ho)
    fig_lofo(ho, dev)
    fig_gateway_map()
    fig_ladder(dev, ho)
    method_out(dev, ho, h3)


if __name__ == "__main__":
    main()
