"""Figures and method_out.json (exp_gen_sol_out schema) from the dev / held-out results."""
from __future__ import annotations

import json
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
from config import FIGS, RES, SCAN, Y0  # noqa: E402
import h2 as H2  # noqa: E402
from stats_core import demean  # noqa: E402

plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})
FNAMES = None


def fsave(fig, name: str) -> None:
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight"); fig.savefig(FIGS / f"{name}.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


def softmax_by(strata: np.ndarray, eta: np.ndarray) -> np.ndarray:
    s = pd.Series(eta).groupby(strata)
    m = s.transform("max").to_numpy()
    w = np.exp(eta - m)
    return w / pd.Series(w).groupby(strata).transform("sum").to_numpy()


def entry_examples(df: pd.DataFrame, dev: dict, spec: dict, names: dict, split: str) -> list[dict]:
    d = df[df.n_ret > 0].copy()
    ds, _ = H2.standardise(d, spec["standardisation"], list(spec["standardisation"]))
    preds = {}
    for m in ("M0", "M2"):
        b = np.array([dev["H2"]["models"][m]["coef"][c] for c in H2.MODELS[m]])
        preds[m] = softmax_by(ds.stratum.to_numpy(), ds[H2.MODELS[m]].to_numpy() @ b)
    ex = []
    for i, r in enumerate(d.itertuples()):
        inp = {"concept": names.get(r.cidx, str(r.cidx)), "year": int(r.t), "age": int(r.age), "candidate_field": int(r.field),
               "field_name": FNAMES[int(r.field) - 11], "phi_home": round(r.a_phi_home, 4), "log_size": round(r.b_log_size, 3),
               "density": round(r.c_density, 4), "gateway_own": round(r.e_gate_own, 4),
               "ret_relatedness_d0": round(r.d0_ret_rel, 4), "ret_gateway_relatedness_d": round(r.d_ret_gate, 4),
               "n_retaining_fields": int(r.n_ret)}
        ex.append({"input": json.dumps(inp), "output": str(int(r.entered)),
                   "predict_M0_size_density_home_owngateway": f"{preds['M0'][i]:.5f}",
                   "predict_M2_plus_retaining_gateway_relatedness": f"{preds['M2'][i]:.5f}",
                   "metadata_split": split, "metadata_group": str(r.group), "metadata_stratum": int(r.stratum),
                   "metadata_cidx": int(r.cidx)})
    return ex


def retention_examples(R: pd.DataFrame, names: dict, split: str) -> list[dict]:
    d = R[R.P_generic.notna()].copy()
    d["log_n_early_j"] = np.log(d.n_early_j)
    base = ["gateway_j", "log_size_j", "phi_home_j", "P_generic", "log_n_early_j"]
    full = base + ["S_hanski"]
    out = {}
    for nm, cols in (("base", base), ("conn", full)):
        Z = demean(np.column_stack([d.R_cj.to_numpy(float), d[cols].to_numpy(float)]), [d.cidx.to_numpy()])
        b = np.linalg.lstsq(Z[:, 1:], Z[:, 0], rcond=None)[0]
        cm = d.groupby("cidx").R_cj.transform("mean").to_numpy()
        xm = d.groupby("cidx")[cols].transform("mean").to_numpy()
        out[nm] = np.clip(cm + (d[cols].to_numpy(float) - xm) @ b, 0, 1)
    ex = []
    for i, r in enumerate(d.itertuples()):
        inp = {"concept": names.get(r.cidx, str(r.cidx)), "field": int(r.field), "field_name": FNAMES[int(r.field) - 11],
               "t0": int(r.t0), "entry_year": int(r.entry_year), "n_early_j": float(r.n_early_j),
               "gateway_j": round(r.gateway_j, 4), "S_hanski": round(r.S_hanski, 4),
               "resc_logodds_bg_adjusted": None if pd.isna(r.resc) else round(r.resc, 4)}
        ex.append({"input": json.dumps(inp), "output": str(int(r.R_cj)), "predict_base": f"{out['base'][i]:.4f}",
                   "predict_with_connectivity": f"{out['conn'][i]:.4f}", "metadata_split": split, "metadata_group": str(r.group)})
    return ex


def figures(dev: dict, held: dict | None, names: dict) -> None:
    # 1. AUC forest by block (dev pooled, held-out pooled)
    fig, ax = plt.subplots(figsize=(6, 3.2))
    blocks = ["b_log_size", "c_density", "a_phi_home", "e_gate_own", "d0_ret_rel", "d_ret_gate", "M0", "M2"]
    for off, (lab, res, col) in enumerate([("dev", dev["H2"], "#1f77b4")] + ([("held-out", held["H2_pooled"], "#d62728")] if held else [])):
        for i, b in enumerate(blocks):
            a = res["auc_within_stratum"][b]
            ax.errorbar(a["mean"], i + 0.2 * off, xerr=[[a["mean"] - a["ci"][0]], [a["ci"][1] - a["mean"]]], fmt="o", color=col,
                        label=lab if i == 0 else None, ms=4)
    ax.set_yticks(range(len(blocks))); ax.set_yticklabels(blocks); ax.axvline(0.5, color="grey", lw=0.8, ls="--")
    ax.set_xlabel("mean within-stratum AUC (concept-bootstrap 95% CI)"); ax.legend(frameon=False)
    ax.set_title("Next-field entry: which block ranks the entered field first?")
    fsave(fig, "fig_entry_auc_forest")
    # 2. per-group d coefficients (held-out)
    if held:
        per = held["H2_per_group"]
        gs = [g for g in per if per[g].get("d") is not None]
        fig, ax = plt.subplots(figsize=(5, 2.6))
        for i, g in enumerate(gs):
            ax.errorbar(per[g]["d"], i, xerr=[[per[g]["d"] - per[g]["boot_ci"][0]], [per[g]["boot_ci"][1] - per[g]["d"]]], fmt="o", color="k")
        dl = held["H2_DL_pooled"]
        if dl.get("k"):
            ax.errorbar(dl["b"], len(gs), xerr=[[dl["b"] - dl["ci"][0]], [dl["ci"][1] - dl["b"]]], fmt="D", color="#d62728")
        ax.set_yticks(range(len(gs) + 1)); ax.set_yticklabels(gs + [f"DL pooled (I2={dl.get('I2', 0):.2f})"])
        ax.axvline(0, color="grey", lw=0.8, ls="--"); ax.set_xlabel("standardised d coefficient (clogit, M2)")
        fsave(fig, "fig_heldout_group_forest")
    # 3. incidence-function curve
    rr = dev.get("rescue_relay", {})
    if "R3_incidence" in rr:
        fig, ax = plt.subplots(figsize=(4, 3))
        for ter, col in (("top", "#d62728"), ("mid", "#7f7f7f"), ("bottom", "#1f77b4")):
            d = pd.DataFrame(rr["R3_incidence"][ter])
            if len(d):
                ax.plot(d.S_bin, d["mean"], "o-", color=col, label=f"{ter} gateway tercile")
        ax.set_xlabel("Hanski connectivity S_cj (quintile)"); ax.set_ylabel("P(retained at t0+6..t0+8)")
        ax.legend(frameon=False); fsave(fig, "fig_incidence_function")
    # 4. cluster mean series
    for lab, res in (("dev", dev), ("heldout", held)):
        if not res:
            continue
        cms = res["trajectories"]["cluster_mean_series"]
        vars_ = ["n_entered_offhome", "n_retaining", "H", "G_share", "log_volume"]
        fig, axs = plt.subplots(1, len(vars_), figsize=(12, 2.4))
        for c, s in cms.items():
            for ax, v in zip(axs, vars_):
                ax.plot(range(len(s[v])), s[v], "o-", ms=3, label=f"cluster {c} (n={res['trajectories']['cluster_sizes'][int(c)]})")
                ax.set_title(v); ax.set_xlabel("years since t0")
        axs[0].legend(frameon=False, fontsize=7)
        fsave(fig, f"fig_trajectory_clusters_{lab}")
    # 5. event study
    for lab, res in (("dev", dev), ("heldout", held)):
        if not res:
            continue
        es = res["ordering"]["lead_lag"]["event_study_H"]["coef"]
        ks = [-3, -2, -1, 0, 1, 2, 3]
        b = [es[f"ev{k:+d}"]["b"] if k != -1 else 0 for k in ks]
        lo = [es[f"ev{k:+d}"]["ci"][0] if k != -1 else 0 for k in ks]
        hi = [es[f"ev{k:+d}"]["ci"][1] if k != -1 else 0 for k in ks]
        fig, ax = plt.subplots(figsize=(4, 2.8))
        ax.errorbar(ks, b, yerr=[np.array(b) - lo, np.array(hi) - b], fmt="o-", color="k")
        ax.axhline(0, color="grey", lw=0.8); ax.axvline(-0.5, color="grey", ls="--", lw=0.8)
        ax.set_xlabel("years relative to first retained gateway field"); ax.set_ylabel("venue-field entropy H (FE-adjusted)")
        fsave(fig, f"fig_event_study_{lab}")


def case_flow(names: dict) -> list[dict]:
    """field-flow plots for the dev cluster medoids (cases chosen from the quantitative results, not by hand)."""
    from frame_io import load_backbone, load_g
    spec = json.loads((RES / "frozen_spec.json").read_text()) if (RES / "frozen_spec.json").exists() else None
    if not spec:
        return []
    bb = load_backbone(); gate = bb["g"]
    order = np.argsort(gate)
    fc = pd.read_csv(RES / "frame_concepts.csv").set_index("cidx")
    G = load_g("dev")
    cases = []
    relay = pd.read_csv(RES / "relay_dev.csv") if (RES / "relay_dev.csv").exists() else None
    ids = list(spec["medoid_cidx"])
    if relay is not None and len(relay):
        ids += relay.sort_values("relay_excess").cidx.tail(2).tolist()
    for c in dict.fromkeys(ids):
        if c not in G:
            continue
        r = fc.loc[c]; t0 = int(r.t0); home = [int(h) for h in str(r.home).split("|")]
        S = H2.states(G[c], home)
        yrs = list(range(t0 - 2, min(t0 + 9, 2023)))
        fig, ax = plt.subplots(figsize=(6, 4.2))
        for yi, y in enumerate(yrs):
            ti = y - Y0
            for rank, k in enumerate(order):
                n = G[c][ti, k + 1]
                if n <= 0:
                    continue
                col = ("#2ca02c" if (k + 11) in home else "#d62728" if S["retaining"][ti, k] else
                       "#7f7f7f" if S["lost"][ti, k] else "#1f77b4" if S["entered"][ti, k] else "#c7c7c7")
                ax.scatter(y, rank, s=8 + 6 * np.sqrt(n), color=col, alpha=0.8, lw=0)
        ax.set_yticks(range(26)); ax.set_yticklabels([FNAMES[k][:28] for k in order], fontsize=6)
        ax.set_title(f"{r['name']} (t0={t0}; green=home, red=retaining, blue=entered, grey=lost)", fontsize=8)
        ax.set_xlabel("year"); ax.set_ylabel("field (sorted by gateway centrality)")
        fn = f"fig_case_{c}"
        fsave(fig, fn)
        cases.append({"cidx": int(c), "name": r["name"], "figure": f"figures/{fn}.png"})
    return cases


def main() -> None:
    global FNAMES
    bb = json.loads((ROOT / "inputs" / "field_backbone.json").read_text())
    FNAMES = bb["fields"]
    dev = json.loads((RES / "dev_result.json").read_text())
    held = json.loads((RES / "heldout_result.json").read_text()) if (RES / "heldout_result.json").exists() else None
    spec = json.loads((RES / "frozen_spec.json").read_text())
    lex = pd.read_parquet(RES / "lexicon.parquet")
    names = dict(zip(lex.concept_idx, lex.name))
    figures(dev, held, names)
    cases = case_flow(names)
    datasets = []
    ddf = pd.read_parquet(RES / "entry_risk_sets_dev.parquet")
    datasets.append({"dataset": "entry_events_dev", "examples": entry_examples(ddf, dev, spec, names, "dev")})
    if (RES / "entry_risk_sets_heldout.parquet").exists():
        hdf = pd.read_parquet(RES / "entry_risk_sets_heldout.parquet")
        datasets.append({"dataset": "entry_events_heldout", "examples": entry_examples(hdf, dev, spec, names, "heldout")})
    for sp in ("dev", "heldout"):
        p = RES / f"rescue_{sp}.csv"
        if p.exists():
            R = pd.read_csv(p)
            if len(R):
                datasets.append({"dataset": f"retention_episodes_{sp}", "examples": retention_examples(R, names, sp)})
    fs = json.loads((RES / "frame_summary.json").read_text())
    gr = json.loads((RES / "grounding_report.json").read_text())
    meta = {"method_name": "Gateway-weighted relatedness to retaining fields (H2 next-field entry) + rescue, relay, trajectories",
            "baselines": "M0 = relatedness-to-home + log field size + Hidalgo relatedness density + target field's own gateway centrality",
            "frame": fs, "grounding": {k: gr[k] for k in gr if k in ("rules_test", "kappa_llm1_llm2", "agreement_llm1_hand",
                                                                        "filter_test_auc", "n_concepts_below_gate_0.8")},
            "dev_headline": {"LR_M2_vs_M0": dev["H2"]["LR"]["M2_vs_M0"], "d_coef": dev["H2"]["models"]["M2"]["coef"]["d_ret_gate"],
                             "d_boot_ci": dev["H2"]["boot_d"]["ci"], "perm_p": dev["H2"]["perm_null"]["p"],
                             "rewired": dev["H2"]["rewired_null"], "auc": {k: dev["H2"]["auc_within_stratum"][k]["mean"]
                                                                          for k in ("M0", "M2", "b_log_size", "c_density", "d_ret_gate")}},
            "heldout_decisions": held.get("decisions") if held else "NOT RUN",
            "case_studies": cases}
    out = {"metadata": meta, "datasets": datasets}
    (ROOT / "method_out.json").write_text(json.dumps(out, default=lambda o: None if isinstance(o, float) and not np.isfinite(o) else str(o)))
    logger.info(f"method_out.json: {[(d['dataset'], len(d['examples'])) for d in datasets]}")
