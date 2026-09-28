#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv
"""Stage `outputs`: results/frontier_result.json (everything in one place), figures/ (PNG + PDF), method_out.json
(exp_gen_sol_out schema; one example per held-out candidate row in an informative primary-sample stratum, with
within-stratum probabilities from the frozen DEV coefficients of R2 (RCA>1 + volume baseline) and R3 (+ retained frontier))."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
import models as M  # noqa: E402
import analysis as AN  # noqa: E402,F401  (registers the extra rungs)

RES, FIGS = ROOT / "results", ROOT / "figures"
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 200, "savefig.bbox": "tight"})
C = {"exp6": "#0072B2", "dev": "#999999", "held": "#D55E00", "dl": "#000000", "cohort": "#009E73", "null": "#56B4E9"}
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
PART_LIMIT = 85_000_000


def load(name: str) -> dict:
    p = RES / name
    return json.loads(p.read_text()) if p.exists() else {}


def save(fig, name: str) -> None:
    fig.savefig(FIGS / f"{name}.png"); fig.savefig(FIGS / f"{name}.pdf")
    plt.close(fig)


def _ci(d: dict, key: str) -> tuple[float, float, float]:
    x = d[key]
    lo, hi = x.get("boot_ci", [x["coef"] - 1.96 * x["se_concept"], x["coef"] + 1.96 * x["se_concept"]])
    return x["coef"], lo, hi


def forest(s1: dict, dev: dict, ho: dict, key: str, dl_key: str, title: str, name: str) -> None:
    rows = []
    for u in ("Physical", "LifeEnv", "Social", "Cohort"):
        if key in s1.get("heldout_units", {}).get(u, {}):
            rows.append((f"EXP6 {u}", *_ci(s1["heldout_units"][u], key), C["exp6"], "o"))
    if s1:
        d = s1["heldout_DL"][dl_key]
        rows.append(("EXP6 DL pooled", d["b"], d["ci"][0], d["ci"][1], C["exp6"], "D"))
    for g in ("CS", "Eng", "BGM", "Med"):
        if key in dev.get("dev_groups", {}).get(g, {}):
            rows.append((f"DEV {g}", *_ci(dev["dev_groups"][g], key), C["dev"], "o"))
    for u in HELD4 + ["COHORT_DEVHOME", "COHORT_NONDEVHOME"]:
        if key in ho.get("units", {}).get(u, {}):
            rows.append((f"HELD {u}", *_ci(ho["units"][u], key), C["cohort"] if u.startswith("COHORT") else C["held"], "o"))
    if ho:
        d = ho["DL_4groups"][dl_key]
        rows.append(("HELD DL (4 groups)", d["b"], d["ci"][0], d["ci"][1], C["dl"], "D"))
        bkey = "d0_R3" if key == "d0_R3" else "d_lost_A1"
        tg = "d0_ret_rel" if key == "d0_R3" else "d_lost"
        b = ho["pooled4"]["boot"][bkey][tg]
        rows.append(("HELD pooled-4 (refit boot)", b["est"], b["ci"][0], b["ci"][1], C["dl"], "s"))
    fig, ax = plt.subplots(figsize=(5.2, 0.28 * len(rows) + 1.0))
    for i, (lab, b, lo, hi, col, mk) in enumerate(rows[::-1]):
        ax.plot([lo, hi], [i, i], color=col, lw=1.4)
        ax.plot(b, i, marker=mk, color=col, ms=5 if mk != "D" else 6)
    ax.axvline(0, color="k", lw=0.6, ls="--")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.set_xlabel("coefficient per DEV-SD (conditional logit, concept-year strata); 95% CI, resampling unit = concept")
    ax.set_title(title, fontsize=9)
    save(fig, name)


def ladder_fig(panels: list[tuple[str, dict]]) -> None:
    steps = [("R1_rca_vs_R0_M0", "R1_rca", "+RCA>1 dens."), ("R2_vol_vs_R1_rca", "R2_vol", "+share dens."),
             ("R3_ret_vs_R2_vol", "R3_ret", "+RETAINED"), ("R4_lost_vs_R3_ret", "R4_lost", "+lost"), ("S_strict_vs_S_strict0", "S_strict", "strict: +RET.")]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.3 * len(panels), 3.3))
    axes = np.atleast_1d(axes)
    for ax, (lab, lad) in zip(axes, panels):
        lr = [lad["LR"][k]["LR"] for k, _, _ in steps]
        cols = [C["held"] if "RET" in s else C["dev"] for _, _, s in steps]
        ax.bar(range(len(steps)), lr, color=cols)
        ax.axhline(6.63, color="k", lw=0.6, ls=":")
        ax.set_xticks(range(len(steps))); ax.set_xticklabels([s for _, _, s in steps], fontsize=7, rotation=35, ha="right")
        ax.set_title(f"{lab}\n(R0 within-AUC {lad['auc_within']['R0_M0']:.3f})", fontsize=8)
        ax.set_ylabel("LR of the added block (dotted: p = 0.01)", fontsize=7)
        ax2 = ax.twinx()
        ax2.plot(range(len(steps)), [lad["auc_within"][r] for _, r, _ in steps], "k.-", lw=0.8)
        ax2.set_ylabel("within-stratum AUC of the rung", fontsize=7)
        ax2.tick_params(labelsize=7)
    fig.tight_layout()
    save(fig, "ladder")


def dose_fig(panels: list[tuple[str, dict]]) -> None:
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    for j, (lab, d, col) in enumerate(panels):
        f = d["fit"]
        xs = np.arange(3) + (j - 1) * 0.12
        b = [f[c]["coef"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
        se = [f[c]["se_concept"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
        ax.errorbar(xs, b, yerr=1.96 * np.array(se), fmt="o-", color=col, label=lab, capsize=2, lw=1)
    ax.axhline(0, color="k", lw=0.6, ls="--")
    ax.set_xticks(range(3)); ax.set_xticklabels(["2", "3", ">=4"])
    ax.set_xlabel("years the retaining field has held the concept (persistence age)")
    ax.set_ylabel("coefficient (per SD of d0)")
    ax.legend(fontsize=7, frameon=False)
    save(fig, "dose_response")


def null_fig(tags: list[tuple[str, str]]) -> None:
    fig, axes = plt.subplots(len(tags), 3, figsize=(9, 2.3 * len(tags)), squeeze=False)
    for i, (lab, tag) in enumerate(tags):
        p = RES / f"nulls_{tag}.npz"
        if not p.exists():
            continue
        z = np.load(p)
        obs = float(z["LR_obs"])
        for j, (k, t) in enumerate((("perm", "retained-label permutation"), ("rewire", "degree-preserving rewiring"), ("label_perm", "node-label permutation"))):
            ax = axes[i, j]
            ax.hist(z[k], bins=40, color=C["null"])
            ax.axvline(obs, color=C["held"], lw=1.5)
            ax.set_title(f"{lab}: {t}\n(obs LR = {obs:.1f}; p = {(1 + (z[k] >= obs).sum()) / (1 + len(z[k])):.4f})", fontsize=7)
            ax.set_xlabel("LR(R3 vs R2) under the null")
    fig.tight_layout()
    save(fig, "null_hist")


def vm_fig(panels: list[tuple[str, dict]]) -> None:
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    labs, i = [], 0
    for lab, sp in panels:
        for key, tag, rk, nk in (("b_volume_matched", "coarse", "d_R_m", "d_N_m"), ("b2_volume_matched_fine", "fine", "d_R_mf", "d_N_mf")):
            c = sp.get(key, {}).get("contrast_R_minus_N")
            if not c:
                continue
            for off, kk, col in ((-0.15, rk, C["held"]), (0.15, nk, C["dev"])):
                ax.errorbar(i + off, c[kk]["est"], yerr=[[c[kk]["est"] - c[kk]["ci"][0]], [c[kk]["ci"][1] - c[kk]["est"]]],
                            fmt="o", color=col, capsize=2)
            labs.append(f"{lab}\n{tag}\nR-N={c['est']:.2f}\n[{c['ci'][0]:.2f},{c['ci'][1]:.2f}]")
            i += 1
    ax.axhline(0, color="k", lw=0.6, ls="--")
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, fontsize=6)
    ax.set_ylabel("coefficient per SD of d0\n(orange: retained R; grey: entered-not-retained N)")
    save(fig, "vol_matched")


def method_out(ho: dict, spec: dict) -> dict:
    df = pd.read_parquet(RES / "risk_sets_exp5_minus_exp6_heldout.parquet")
    dev = load("step2_dev.json")
    fr = pd.read_csv(Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv"),
                     usecols=["ci", "concept_id", "qid", "name"]).set_index("ci")
    std = spec["standardisation_DEV"]
    prim = M.standardise(df[df.n_ret > 0], std)
    raw = df[df.n_ret > 0]
    inf = M.informative(prim)
    raw = raw.loc[inf.index]
    coef = dev["battery"]["ladder"]["frontier_primary_sample"]["models"]
    preds = {}
    for rn, nm in (("R2_vol", "predict_R2_rca_vol_baseline"), ("R3_ret", "predict_R3_retained_frontier")):
        cols = M.RUNGS[rn]
        eta = inf[cols].to_numpy() @ np.array([coef[rn]["coef"][c] for c in cols])
        e = np.exp(eta - inf.assign(_e=eta).groupby("stratum")._e.transform("max").to_numpy())
        preds[nm] = e / pd.Series(e, index=inf.index).groupby(inf.stratum).transform("sum").to_numpy()
    covs = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol", "d0_ret_rel", "d_lost", "n_ret", "n_lost"]
    datasets = {}
    cid = fr.concept_id.to_dict(); qid = fr.qid.to_dict()
    vals = raw[covs].to_numpy()
    for i, r in enumerate(raw[["cidx", "t", "field", "entered", "unit", "stratum"]].itertuples(index=False)):
        c = int(r.cidx)
        inp = "|".join([f"C{int(cid[c])}", str(qid[c]), str(int(r.t)), str(int(r.field))] + [f"{v:.4g}" for v in vals[i]])
        ex = {"input": inp, "output": str(int(r.entered)),
              "predict_R2_rca_vol_baseline": f"{preds['predict_R2_rca_vol_baseline'][i]:.4g}",
              "predict_R3_retained_frontier": f"{preds['predict_R3_retained_frontier'][i]:.4g}",
              "metadata_unit": r.unit, "metadata_stratum": int(r.stratum)}
        ds = "entry_events_heldout_pooled4" if r.unit in HELD4 else "entry_events_heldout_cohort"
        datasets.setdefault(ds, []).append(ex)
    meta = {"method_name": "Retained frontier (d0_ret_rel = mean relatedness of target field to off-home fields that RETAIN the concept)",
            "baseline": "R2 = relatedness-to-home + log field size + Hidalgo density of entered fields + own gateway + RCA>1 density (annual, "
                        "Hidalgo current portfolio) + share-weighted density",
            "prediction": "within-stratum (concept-year) choice probability from the FROZEN DEV coefficients; output = 1 if the field was entered",
            "rows": "held-out candidate rows in informative strata of the primary sample (non-empty retained set)",
            "input_format": "concept_id|qid|year|target_field|" + "|".join(["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol", "d0_ret_rel", "d_lost", "n_ret", "n_lost"]) + " (raw, unstandardised covariates at t-1; stratum = concept-year)",
            "verdicts": ho.get("verdicts", {}).get("FRONTIER"), "abandonment": ho.get("verdicts", {}).get("ABANDONMENT")}
    return {"metadata": meta, "datasets": [{"dataset": k, "examples": v} for k, v in datasets.items()]}


def trunc(o):
    if isinstance(o, str):
        return o[:200]
    if isinstance(o, dict):
        return {k: trunc(v) for k, v in o.items()}
    if isinstance(o, list):
        return [trunc(v) for v in o]
    return o


def write_method_out(mo: dict) -> list[str]:
    """method_out.json == full_method_out.json (complete; compact rows keep it under the size limit), plus mini/preview."""
    s = json.dumps(mo, separators=(",", ":"))
    if len(s) > PART_LIMIT:
        raise RuntimeError(f"method_out would be {len(s)/1e6:.1f} MB > {PART_LIMIT/1e6:.0f} MB limit")
    for nm in ("method_out.json", "full_method_out.json"):
        (ROOT / nm).write_text(s)
    mini = {"metadata": mo["metadata"], "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in mo["datasets"]]}
    (ROOT / "mini_method_out.json").write_text(json.dumps(mini, indent=1))
    (ROOT / "preview_method_out.json").write_text(json.dumps(trunc(mini), indent=1))
    return ["method_out.json", "full_method_out.json", "mini_method_out.json", "preview_method_out.json"]


@logger.catch(reraise=True)
def main() -> None:
    s1, dev, ho = load("step1_exp6_robustness.json"), load("step2_dev.json"), load("step2_heldout.json")
    spec = load("frozen_spec.json")
    forest(s1, dev, ho, "d0_R3", "d0", "Retained frontier d0 in R3 (beyond RCA>1 and share-weighted density)", "forest_d0_by_unit")
    forest(s1, dev, ho, "d_lost_A1", "d_lost", "Abandonment penalty d_lost in A1 (given ever-entered density)", "forest_dlost_by_unit")
    panels = [("EXP6 dev", s1.get("dev")), ("EXP6 held-out", s1.get("heldout")), ("EXP5-EXP6 DEV", dev.get("battery")),
              ("EXP5-EXP6 held-out pooled-4", ho.get("pooled4"))]
    panels = [(a, b["ladder"]["frontier_primary_sample"]) for a, b in panels if b]
    ladder_fig(panels)
    dp = [("EXP6 held-out", s1.get("heldout"), C["exp6"]), ("DEV", dev.get("battery"), C["dev"]), ("held-out pooled-4", ho.get("pooled4"), C["held"])]
    dose_fig([(a, b["specificity"]["c_dose"], c) for a, b, c in dp if b and "specificity" in b])
    null_fig([(a, t) for a, t in (("EXP6 held-out", "exp6_heldout"), ("DEV", "exp5_dev"), ("held-out pooled-4", "exp5_heldout_pooled4"))
              if (RES / f"nulls_{t}.npz").exists()])
    vm_fig([(a, b["specificity"]) for a, b, _ in dp if b and "specificity" in b])
    fr = {"title": "Do concepts spread from fields that keep them?",
          "step1_robustness_exp6": s1, "step2_dev": dev, "power_table": dev.get("power"), "step2_heldout": ho,
          "verdicts": ho.get("verdicts"), "overlap": load("overlap_report.json"), "deviations": load("deviations.json"),
          "unit_tests_T0": load("unit_tests_T0.json"), "audit": load("audit.json"),
          "exploratory_lpm_EXPLORATORY": load("exploratory_lpm.json"),
          "guevara_comparison": {"ours_exp5_heldout_pooled4": ho.get("pooled4", {}).get("guevara_comparable_auc"),
                                 "ours_exp6_heldout": s1.get("heldout", {}).get("guevara_comparable_auc"),
                                 "guevara_2016": {"individuals": 0.896, "organisations": 0.715, "countries": 0.682},
                                 "flag": "different unit (concept vs scholar/org/country), event (D3 count entry vs RCA transition) and proximity (26-field PMI vs author-sharing over subfields): not a head-to-head"},
          "resampling_unit_note": "every CI resamples concepts unless labelled 'concept x target field' (crossed bootstrap)",
          "provenance_note": "EXP5 held-out concepts' counts and retention outcomes (t0+6..8) were unsealed in iteration 2 for H1/H3; no entry or "
                             "frontier analysis had touched them. The replication is independent of EXP6's concepts and of any d0 analysis, but "
                             "the frame is not never-seen data."}
    (RES / "frontier_result.json").write_text(json.dumps(fr, indent=1, default=float))
    if ho and spec:
        mo = method_out(ho, spec)
        names = write_method_out(mo)
        logger.info(f"method_out: {sum(len(d['examples']) for d in mo['datasets']):,} examples -> {names}")
    logger.info("outputs done")


if __name__ == "__main__":
    main()
