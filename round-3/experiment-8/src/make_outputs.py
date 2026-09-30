#!/usr/bin/env python3
"""STEP 7: rq1_heldout.json (headline deliverable), figures, case exemplars and method_out.json (exp_gen_sol_out)."""
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

from common import DATA, FIGS, HELD_GROUPS, RES, ROOT, UNITS, jdump, setup_logger
from indicators import B5, BIN_OUTCOMES, CONT_OUTCOMES, FAMILIES, FAMILY_OF, INDICATORS, OUTCOMES, PREREG

DEV_UNITS = ["CS", "Eng", "BGM", "Med"]


def _save(fig, name):
    fig.savefig(FIGS / f"{name}.png", dpi=150, bbox_inches="tight")
    fig.savefig(FIGS / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def fig_heatmap(port: pd.DataFrame, spec: dict) -> None:
    t = port[port.outcome == "O2r_m50"]
    order = [c for f in FAMILIES for c, _ in FAMILIES[f]] + B5
    units = DEV_UNITS + HELD_GROUPS + ["COH_DEVHOME", "COH_OTHER"]
    M = t.pivot_table(index="indicator", columns="unit", values="rho").reindex(index=order, columns=units)
    lo = t.pivot_table(index="indicator", columns="unit", values="ci_lo").reindex(index=order, columns=units)
    hi = t.pivot_table(index="indicator", columns="unit", values="ci_hi").reindex(index=order, columns=units)
    frozen = {d["indicator"] for d in spec["top10"].get("O2r_m50", [])}
    fig, ax = plt.subplots(figsize=(8.5, 15))
    v = np.nanmax(np.abs(M.to_numpy())) if np.isfinite(M.to_numpy()).any() else 0.3
    im = ax.imshow(M.to_numpy(), cmap="RdBu_r", vmin=-v, vmax=v, aspect="auto")
    for i in range(len(order)):
        for j in range(len(units)):
            if np.isfinite(lo.iloc[i, j]) and (lo.iloc[i, j] > 0 or hi.iloc[i, j] < 0):
                ax.plot(j, i, "k.", ms=4)
    ax.set_xticks(range(len(units)))
    ax.set_xticklabels(units, rotation=45, ha="right")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{c} [{FAMILY_OF.get(c, 'B5')}]" for c in order], fontsize=7)
    for lab in ax.get_yticklabels():
        if lab.get_text().split(" [")[0] in frozen:
            lab.set_fontweight("bold")
    ax.axvline(3.5, c="k", lw=1)
    ax.axvline(7.5, c="k", lw=1)
    ax.set_title("Partial Spearman with O2r_m50 given B5, per unit\n(dot: 95% CI excludes 0; bold: frozen top 10)")
    fig.colorbar(im, ax=ax, shrink=0.4, label="psp | B5")
    _save(fig, "portability_heatmap")


def fig_forest(summary: dict, outcome: str) -> None:
    rows = [r for r in summary.get(outcome, []) if r["in_top10"]]
    if not rows:
        return
    fig, ax = plt.subplots(figsize=(8, 0.55 * len(rows) * 1.0 + 1.5))
    cols = dict(zip(UNITS, plt.cm.tab10(np.arange(len(UNITS)))))
    for i, r in enumerate(rows):
        yb = len(rows) - i
        for k, u in enumerate(UNITS):
            v = r["per_unit"].get(u)
            ci = r["per_unit_ci"].get(u)
            if v is None:
                continue
            yy = yb + 0.3 - 0.1 * k
            ax.plot(v, yy, "o", color=cols[u], ms=3, label=u if i == 0 else None)
            if ci:
                ax.plot(ci, [yy, yy], "-", color=cols[u], lw=0.8)
        ax.plot(r["pooled"], yb - 0.35, "D", color="k", ms=5, label="DL pooled (4 groups)" if i == 0 else None)
        ax.plot(r["pooled_ci"], [yb - 0.35] * 2, "k-", lw=1.5)
    ax.axvline(0, c="grey", lw=0.8)
    ax.set_yticks([len(rows) - i for i in range(len(rows))])
    ax.set_yticklabels([f"{r['indicator']} ({'+' if r['frozen_sign'] > 0 else '-'})" for r in rows], fontsize=8)
    ax.set_xlabel("psp | B5" if outcome in CONT_OUTCOMES else "dAUC over B5 (frozen DEV coefficients)")
    ax.set_title(f"Held-out scoring of the frozen top 10: {outcome}")
    ax.legend(fontsize=7, loc="best")
    _save(fig, f"heldout_forest_{outcome}")


def fig_learned(lv: dict) -> None:
    outs = [o for o in OUTCOMES if o in lv and "POOLED_HELDOUT" in lv[o] and lv[o]["POOLED_HELDOUT"].get("n")]
    if not outs:
        return
    fig, axes = plt.subplots(2, 4, figsize=(15, 6.5))
    for ax, o in zip(axes.ravel(), outs):
        r = lv[o]["POOLED_HELDOUT"]
        ks = [k for k in ("B5", "B5_best_single", "linear_all", "EBM") if k in r and r[k].get("metric") is not None]
        if "linear_all" in r and r["linear_all"].get("metric") is None:
            ax.text(0.02, 0.95, "linear_all: all coefficients 0 (constant prediction)", transform=ax.transAxes,
                    fontsize=6, va="top")
        vals = [r[k]["metric"] for k in ks]

        def _e(k, j):
            ci = r[k].get("delta_ci") or [None, None]
            if k == "B5" or ci[j] is None:
                return 0.0
            return abs(r[k]["metric"] - (r["B5"]["metric"] + ci[j]))
        err = [[_e(k, 0) for k in ks], [_e(k, 1) for k in ks]]
        ax.bar(range(len(ks)), vals, yerr=np.abs(err), color=[{"B5": "grey", "B5_best_single": "tab:blue", "linear_all": "tab:orange", "EBM": "tab:green"}[k] for k in ks],
               capsize=3)
        ax.set_xticks(range(len(ks)))
        ax.set_xticklabels([k.replace("_", "\n") for k in ks], fontsize=7)
        lo = min(vals) - 0.05
        ax.set_ylim(max(0, lo) if o in BIN_OUTCOMES else min(0, lo), max(vals) + 0.05)
        ax.set_title(f"{o} ({'AUC' if o in BIN_OUTCOMES else 'Spearman'}; n={r['n']})", fontsize=9)
    for ax in axes.ravel()[len(outs):]:
        ax.axis("off")
    fig.suptitle("Held-out (4 groups pooled): B5 vs B5 + best single vs learned models (95% CI of the paired "
                 "difference vs B5)")
    fig.tight_layout()
    _save(fig, "learned_vs_single")


def fig_ebm(lm: dict) -> None:
    items = []
    for o in ("O2r_resid", "O5_WW"):
        sh = lm["models"].get(o, {}).get("ebm", {}).get("shapes", {})
        for name, d in list(sh.items())[:6]:
            items.append((o, name, d))
    if not items:
        return
    fig, axes = plt.subplots(2, 6, figsize=(18, 6))
    for ax, (o, name, d) in zip(axes.ravel(), items):
        sc = np.asarray(d["scores"], float)
        cuts = d.get("cuts")
        if cuts and len(sc) >= len(cuts) + 2:
            xs = np.r_[cuts[0], cuts]            # left edge of each bin (first bin: below the first cut)
            ax.step(xs, sc[1:len(cuts) + 2], where="post")
        else:
            ax.plot(sc[1:-1], ".-")
        ax.set_title(f"{o}: {name}", fontsize=8)
        ax.axhline(0, c="grey", lw=0.6)
        ax.set_xlabel("standardised value", fontsize=7)
    for ax in axes.ravel()[len(items):]:
        ax.axis("off")
    fig.suptitle("EBM shape functions (top terms by importance; DEV fit)")
    fig.tight_layout()
    _save(fig, "ebm_shapes")


def fig_o5(br: dict) -> None:
    t = pd.DataFrame(br["O5_by_t0"])
    if t.empty:
        return
    fig, ax = plt.subplots(figsize=(7, 3.5))
    ax.plot(t.t0, t.pos / t.n, "o-", label="O5 (all sources)")
    ax.plot(t.t0, t.pos_ww / t.n_ww, "s-", label="O5_WW (Wikipedia/Wikidata)")
    ax.set_xlabel("onset year t0")
    ax.set_ylabel("positive rate among at-risk")
    ax.legend()
    ax.set_title("External-recognition base rates by onset year")
    _save(fig, "o5_base_rates")


def precision_top_decile(A: pd.DataFrame, preds: pd.DataFrame, spec: dict) -> dict:
    out = {}
    d = A[A.unit.isin(HELD_GROUPS)].merge(preds, on="ci", how="left")
    for o in ("O2r_m50", "O5_WW"):
        res = {}
        top1 = spec["top10"].get(o, [{}])[0].get("indicator") if spec["top10"].get(o) else None
        sign = spec["top10"][o][0]["sign"] if top1 else 1
        scorers = {f"best_single:{top1}": d[top1] * sign if top1 else None}
        for k in ("B5", "B5_best_single", "linear_all", "EBM"):
            c = f"{o}__{k}"
            if c in d:
                scorers[k] = d[c]
        for u in HELD_GROUPS + ["POOLED"]:
            dd = d if u == "POOLED" else d[d.unit == u]
            y = dd[o]
            ok = y.notna()
            if ok.sum() < 30:
                continue
            truth = (y[ok] >= y[ok].quantile(0.9)) if o in CONT_OUTCOMES else (y[ok] == 1)
            rr = {"n": int(ok.sum()), "base_rate": float(truth.mean())}
            for k, s in scorers.items():
                if s is None:
                    continue
                ss = s.loc[ok[ok].index].to_numpy(float)
                okk = np.isfinite(ss)
                if okk.sum() < 30:
                    continue
                if u == "POOLED":
                    # top decile within each group, pooled
                    sel = np.zeros(ok.sum(), bool)
                    units = dd.unit[ok].to_numpy()
                    for g in np.unique(units):
                        m = (units == g) & okk
                        if m.sum() >= 10:
                            thr = np.quantile(ss[m], 0.9)
                            sel |= m & (ss >= thr)
                else:
                    thr = np.nanquantile(ss, 0.9)
                    sel = okk & (ss >= thr)
                rr[k] = float(truth.to_numpy()[sel].mean()) if sel.sum() else None
            res[u] = rr
        out[o] = res
    return out


def exemplars(A: pd.DataFrame, spec: dict) -> dict:
    """Best portable indicator for O2r_resid: 3 held-out concepts with the highest / lowest values + W3 neighbours."""
    summ = json.loads((RES / "heldout_summary.json").read_text())
    rows = [r for r in summ.get("O2r_resid", []) if r["in_top10"] and r["pooled"] is not None]
    if not rows:
        return {}
    best = max(rows, key=lambda r: (r.get("confirmed", False), abs(r["pooled"]) if r["pooled"] is not None else 0))
    ind = best["indicator"]
    eg = pd.read_parquet(DATA / "ego_features.parquet", columns=["ci", "_top_nb_W3"]) \
        if "_top_nb_W3" in pd.read_parquet(DATA / "ego_features.parquet").columns else None
    d = A[A.unit.isin(HELD_GROUPS) & A[ind].notna() & A.O2r_resid.notna()].copy()
    d["score"] = d[ind] * best["frozen_sign"]
    out = {"indicator": ind, "frozen_sign": best["frozen_sign"], "pooled_psp": best["pooled"], "high": [], "low": []}
    for tag, dd in (("high", d.nlargest(3, "score")), ("low", d.nsmallest(3, "score"))):
        for r in dd.itertuples():
            nb = None
            if eg is not None:
                m = eg[eg.ci == r.ci]
                nb = json.loads(m._top_nb_W3.iloc[0]) if len(m) and isinstance(m._top_nb_W3.iloc[0], str) else None
            out[tag].append({"ci": int(r.ci), "name": r.name, "group": r.group, "t0": int(r.t0),
                             ind: float(getattr(r, ind)), "O2r_resid": float(r.O2r_resid), "O2r_m50": float(r.O2r_m50),
                             "logvol": float(r.logvol), "top10_W3_neighbours": nb})
    return out


def method_out(A: pd.DataFrame, logger) -> None:
    dev_oof = pd.read_parquet(RES / "dev_oof_predictions.parquet")
    hp = pd.read_parquet(RES / "heldout_predictions.parquet")
    P = pd.concat([dev_oof, hp], ignore_index=True).drop_duplicates("ci").set_index("ci")
    feats = INDICATORS + B5
    ds = {}
    for r in A.itertuples(index=False):
        rd = r._asdict()
        inp = {"concept": rd["name"], "concept_id": f"C{int(rd['concept_id'])}", "t0": int(rd["t0"]),
               "home_group": rd["group"], "indicators_t0_t0p2": {c: (None if pd.isna(rd.get(c)) else
                                                                    round(float(rd[c]), 6)) for c in feats}}
        outp = {o: (None if pd.isna(rd.get(o)) else round(float(rd[o]), 6)) for o in OUTCOMES}
        ex = {"input": json.dumps(inp), "output": json.dumps(outp),
              "metadata_split": rd["split"], "metadata_unit": rd["unit"], "metadata_ci": int(rd["ci"]),
              "metadata_prediction_type": "DEV out-of-fold (leave-one-DEV-group-out)" if rd["split"] == "DEV"
              else "frozen DEV model applied once after the unseal"}
        if rd["ci"] in P.index:
            pr = P.loc[rd["ci"]]
            for o in OUTCOMES:
                for k, nm in (("B5", "B5"), ("B5_best_single", "best_single"), ("EBM", "EBM"),
                              ("linear_all", "linear_all")):
                    c = f"{o}__{k}"
                    if c in pr.index and pd.notna(pr[c]):
                        ex[f"predict_{nm}_{o}"] = f"{float(pr[c]):.6f}"
        key = {"DEV": "rq1_dev_concepts", "HELDOUT": "rq1_heldout_concepts", "COHORT": "rq1_cohort_2010_14_concepts"}[
            rd["split"]]
        ds.setdefault(key, []).append(ex)
    meta = {"method_name": "RQ1 held-out indicator portability (DEV freeze -> sealed held-out scoring)",
            "description": "One example per frame concept: input = the ~53 candidate indicators + B5 over t0..t0+2; "
                           "output = the 8 outcomes; predict_* = B5-only, B5 + best single indicator (frozen DEV #1), "
                           "ElasticNet/L1-logistic on all indicators, and EBM, per outcome.",
            "outcomes": OUTCOMES, "indicators": INDICATORS, "baseline": B5}
    doc = {"metadata": meta, "datasets": [{"dataset": k, "examples": v} for k, v in ds.items()]}
    (ROOT / "method_out.json").write_text(json.dumps(doc))
    logger.info(f"method_out.json: {sum(len(v) for v in ds.values())} examples")


def main() -> None:
    logger = setup_logger("outputs")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    A = pd.read_parquet(DATA / "analysis_table.parquet")
    summ = json.loads((RES / "heldout_summary.json").read_text())
    port = pd.read_csv(RES / "portability_table.csv")
    lv = json.loads((RES / "learned_vs_single_heldout.json").read_text())
    lm = json.loads((RES / "learned_model.json").read_text())
    pv = json.loads((RES / "prereg_verdicts.json").read_text()) if (RES / "prereg_verdicts.json").exists() else {}
    br = json.loads((RES / "outcome_base_rates.json").read_text())
    sel = json.loads((RES / "rq1_dev_selection.json").read_text())
    audit = json.loads((RES / "audit.json").read_text()) if (RES / "audit.json").exists() else {}
    sens = json.loads((RES / "sensitivities_pooled.json").read_text()) if (RES / "sensitivities_pooled.json").exists() else []
    preds = pd.read_parquet(RES / "heldout_predictions.parquet")
    fig_heatmap(port, spec)
    for o in OUTCOMES:
        fig_forest(summ, o)
    fig_learned(lv)
    fig_ebm(lm)
    fig_o5(br)
    ex = exemplars(A, spec)
    jdump(ex, RES / "case_exemplars.json")
    ptd = precision_top_decile(A, preds, spec)
    # portability summary: per indicator, held-out groups with CI>0 / <0 for O2r_m50
    ph = port[(port.outcome == "O2r_m50") & port.unit.isin(HELD_GROUPS)]
    pt_sum = ph.groupby("indicator").apply(lambda t: pd.Series({
        "n_groups_ci_pos": int((t.ci_lo > 0).sum()), "n_groups_ci_neg": int((t.ci_hi < 0).sum()),
        "mean_psp": float(t.rho.mean())}), include_groups=False).reset_index()
    headline = {}
    for o, rows in summ.items():
        headline[o] = {"n_top10": sum(r["in_top10"] for r in rows),
                       "n_confirmed_holm": sum(bool(r.get("confirmed")) for r in rows if r["in_top10"]),
                       "confirmed": [r["indicator"] for r in rows if r.get("confirmed")],
                       "pooled": {r["indicator"]: {"pooled": r["pooled"], "ci": r["pooled_ci"], "I2": r["I2"],
                                                   "holm_p": r.get("holm_p"), "sign_agree": f"{r['sign_agree']}/{r['n_units']}",
                                                   "cohort": {u: r["per_unit"].get(u) for u in ("COH_DEVHOME", "COH_OTHER")}}
                                  for r in rows if r["in_top10"]}}
    out = {
        "title": "RQ1 held-out portability of early network indicators of concept emergence",
        "frame": {"n_concepts": int(len(A)), "units": A.unit.value_counts().to_dict()},
        "second_use_disclosure": "EXP5 already unsealed O1/O3/O2r for these held-out concepts to test its H1/H3. "
                                 "The ~50 other indicators were never scored on them and no selection here touched "
                                 "held-out rows; the G family (G, G_A, G_btw) was scored once before on O2r_resid "
                                 "and its held-out rows are flagged previously_scored (not confirmatory).",
        "headline_by_outcome": headline, "heldout_summary": summ, "learned_vs_single": lv,
        "precision_at_top_decile": ptd, "prereg_verdicts": pv, "dev_selection": {k: sel[k] for k in (
            "top10", "union_top10", "placebo_T5")}, "portability_O2r_m50_heldout_counts": pt_sum.to_dict(orient="records"),
        "sensitivities": sens, "audit": {k: (v.get("pass") if isinstance(v, dict) else v) for k, v in audit.items()},
        "outcome_base_rates": br["base_rates_by_unit"], "case_exemplars": ex,
    }
    jdump(out, RES / "rq1_heldout.json")
    method_out(A, logger)
    logger.info("outputs written")


if __name__ == "__main__":
    main()
