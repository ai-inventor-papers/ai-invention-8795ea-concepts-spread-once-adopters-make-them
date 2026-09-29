"""S8: Holm over the declared family, the mechanical verdict (results/cheng_verdict.json), figures, method_out.json
(exp_gen_sol_out), and reconciling_cheng.md. Every number written here is read from a results JSON; its key path
is recorded next to it."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import rankdata

from common import (B5, BODY_COHORT, DATA, FIGS, GROUPS5, RES, ROOT, SELECTION_LABEL, jdump, jload)
from rq1stats import holm

PRIMARY = "EXP5_pooled"


def g(d: dict, path: str):
    """Get a value by a dotted key path; list indices allowed as [i]; keys may contain '|' and '-'."""
    cur = d
    for part in path.split("."):
        if "[" in part:
            k, i = part[:-1].split("[")
            cur = cur[k][int(i)]
        else:
            cur = cur[part]
    return cur


# ----------------------------------------------------------------------------- verdict
def verdict() -> dict:
    A = jload(RES / "cheng_panel_models.json")
    S = jload(RES / "cheng_static.json")
    C = jload(RES / "panel_C.json")
    K = {}

    def put(name, file, path, obj):
        K[name] = {"value": g(obj, path), "source": f"{file}:{path}"}
        return K[name]["value"]

    a1 = put("A1_HOME_joint_zCONS", "cheng_panel_models.json", "builds.HOME.joint.A1.coef.zCONS", A)
    a2 = put("A2_HOME_joint_zCONS", "cheng_panel_models.json", "builds.HOME.joint.A2.coef.zCONS", A)
    rb = put("RATIO_HOME_joint", "cheng_panel_models.json", "builds.HOME.joint.ratio_boot", A)
    raw = put("B_raw_primary", "cheng_static.json", f"volume.{PRIMARY}|volume.B_raw_spearman_V_t0p3", S)
    p3 = put("P3_primary", "cheng_static.json", f"trait.{PRIMARY}|CONS_early_home.psp.O2r_m50", S)
    p4 = put("P4_primary", "cheng_static.json", f"trait.{PRIMARY}|CONS_early_home.psp.O3", S)
    p5 = put("P5_primary", "cheng_static.json", f"trait.{PRIMARY}|CONS_early_home.paired_diff.O1c-O2r_m50", S)
    rawc = put("B_raw_cohort", "cheng_static.json", f"volume.{BODY_COHORT}|volume.B_raw_spearman_V_t0p3", S)
    p3c = put("P3_cohort", "cheng_static.json", f"trait.{BODY_COHORT}|CONS_early_home.psp.O2r_m50", S)
    c1 = put("C1", "panel_C.json", "C1", C)
    # one-sided p-values in the predicted direction
    p_a1 = float(stats.norm.sf(a1["b"] / a1["se"]))
    fam = {"P1-A1": p_a1, "P2": rb["p_one_ratio_lt_0.5"], "P3": p3["p_one_pred"], "P4": p4["p_one_pred"],
           "P5": p5["p_one_pred"]}
    hp = dict(zip(fam, holm(list(fam.values()))))
    pred = {
        "P1": {"holds": bool(raw["rho"] > 0 and raw["ci"][0] > 0 and a1["b"] > 0 and a1["ci"][0] > 0),
               "raw_rho": raw["rho"], "raw_ci": raw["ci"], "A1_b": a1["b"], "A1_ci": a1["ci"]},
        "P2": {"holds": bool(rb["ratio_ci"][1] < 0.5), "ratio": rb["ratio"], "ratio_ci": rb["ratio_ci"]},
        "P3": {"holds": bool(p3["rho"] < 0 and p3["ci"][1] < 0), "psp": p3["rho"], "ci": p3["ci"]},
        "P4": {"holds": bool(p4["rho"] <= 0 and p4["ci"][1] <= 0), "psp": p4["rho"], "ci": p4["ci"],
               "point_holds": bool(p4["rho"] <= 0)},
        "P5": {"holds": bool(p5["rho"] > 0 and p5["ci"][0] > 0), "diff": p5["rho"], "ci": p5["ci"]},
        "P6": {"holds": bool(c1["coef"]["zCONS"]["b"] < 0 and c1["boot"]["ci"][1] < 0),
               "b": c1["coef"]["zCONS"]["b"], "boot_ci": c1["boot"]["ci"], "crv1_ci": c1["coef"]["zCONS"]["ci"]},
    }
    confirmed = bool(raw["rho"] > 0 and raw["ci"][0] > 0 and p3["rho"] < 0 and p3["ci"][1] < 0)
    n_c = p3c.get("n") or 0
    rep = bool(rawc["rho"] is not None and rawc["rho"] > 0 and rawc["ci"][0] > 0 and p3c["rho"] is not None
               and p3c["rho"] < 0 and (n_c < 600 or p3c["ci"][1] < 0))
    labels = []
    if confirmed:
        labels.append("REVERSAL CONFIRMED (on selection data)")
    if rep:
        labels.append("REVERSAL REPLICATED")
    if pred["P2"]["holds"]:
        labels.append("SIZE-DOMINATED")
    if pred["P5"]["holds"]:
        labels.append("DEPTH-REACH SPLIT")
    null_rev = bool(p3["ci"][0] <= 0 <= p3["ci"][1])
    if null_rev:
        labels.append("NULL-REVERSAL")
    out = {"label": SELECTION_LABEL, "verdicts": labels, "predictions": pred,
           "holm_family_one_sided": {k: {"p": fam[k], "p_holm": hp[k]} for k in fam},
           "replication": {"body": BODY_COHORT, "n": n_c, "raw": rawc, "psp_O2r_m50": p3c,
                           "MDE_2.8SE": S["cohort_MDE_O2r_m50"]["MDE_2.8SE"],
                           "CI_required": n_c >= 600, "replicated": rep},
           "null_reversal_note": "consistency predicts volume but carries no breadth information net of size"
           if null_rev else None,
           "sources": {k: v["source"] for k, v in K.items()},
           "rules": jload(RES / "frozen_spec.json")["verdict_rules"]}
    jdump(out, RES / "cheng_verdict.json")
    return out


# ----------------------------------------------------------------------------- figures
def figures() -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "ps.fonttype": 42, "axes.spines.top": False,
                         "axes.spines.right": False})
    A = jload(RES / "cheng_panel_models.json")
    S = jload(RES / "cheng_static.json")
    P = jload(RES / "palla.json")
    col = {"HOME": "#1f5fa8", "ALL": "#d9822b"}
    # ---- fig_cheng_ladder
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    models = [("A1", "A1 (Cheng spec)"), ("A2", "A2 (+ log V(t))"), ("A3", "A3 (+ concept FE)")]
    for k, b in enumerate(["HOME", "ALL"]):
        for j, (m, lab) in enumerate(models):
            c = A["builds"][b]["joint"][m]["coef"]["zCONS"]
            x = j + (k - 0.5) * 0.25
            ax.errorbar(x, 100 * c["pct_per_sd"], yerr=[[100 * (c["pct_per_sd"] - c["pct_ci"][0])],
                                                        [100 * (c["pct_ci"][1] - c["pct_per_sd"])]],
                        fmt="o", color=col[b], capsize=3, label=b if j == 0 else None)
            ax.annotate(f"{100 * c['pct_per_sd']:+.1f}%", (x + 0.05, 100 * c["pct_per_sd"]), fontsize=7)
    ax.axhline(53, ls=":", color="grey")
    ax.text(2.35, 55, "Cheng et al. 2023: +53%", fontsize=7, color="grey", ha="right")
    ax.axhline(0, color="black", lw=0.6)
    ax.set_xticks(range(3), [lab for _, lab in models])
    ax.set_ylabel("% change in V(t+1) per SD of consistency")
    ax.set_title("Test A: Cheng's volume effect of consistency, with and without current size", fontsize=9)
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"fig_cheng_ladder.{ext}", dpi=200)
    plt.close(fig)
    # ---- fig_reach_depth_forest
    outs = ["O2r_m50", "O2r_resid", "O1c", "O1b", "O3"]
    olab = {"O2r_m50": "O2r_m50 (reach)", "O2r_resid": "O2r_resid (reach)", "O1c": "O1c (sustained uptake)",
            "O1b": "O1b (retention)", "O3": "O3 (transience)"}
    bodies = [PRIMARY, "DEV", "OLD_HELDOUT", "COHORT_2010_14", BODY_COHORT]
    bcol = dict(zip(bodies, ["black", "#1f5fa8", "#2a9d8f", "#8a5cc2", "#d9822b"]))
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    yk = 0
    yt, yl = [], []
    for o in outs:
        for bi, bd in enumerate(bodies):
            r = S["trait"][f"{bd}|CONS_early_home"]["psp"][o]
            if r["rho"] is None:
                continue
            y = yk + bi * 0.14
            ax.errorbar(r["rho"], y, xerr=[[r["rho"] - r["ci"][0]], [r["ci"][1] - r["rho"]]], fmt="o", ms=3,
                        color=bcol[bd], capsize=2, label=bd if o == outs[0] else None)
        dl = S["DL"][PRIMARY][o]
        y = yk + len(bodies) * 0.14
        ax.plot([dl["ci"][0], dl["b"], dl["ci"][1], dl["b"], dl["ci"][0]], [y, y + 0.06, y, y - 0.06, y],
                color="crimson", lw=1)
        yt.append(yk + 0.35)
        yl.append(olab[o])
        yk += 1.2
    ax.plot([], [], color="crimson", label="DL over 5 groups (primary)")
    ax.axvline(0, color="black", lw=0.6)
    ax.set_yticks(yt, yl)
    ax.invert_yaxis()
    ax.set_xlabel("psp(CONS_early_home, outcome | B5 + dummies), 95% concept-bootstrap CI")
    ax.set_title("Test B: early consistency vs reach and depth outcomes (selection data)", fontsize=9)
    ax.legend(frameon=False, fontsize=7, loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=3)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"fig_reach_depth_forest.{ext}", dpi=200)
    plt.close(fig)
    # ---- fig_palla
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    for ax, o in zip(axs, ["O3", "O2r_m50", "O1c"]):
        r = P["results"][f"{PRIMARY}|{o}"]
        for k, lab in enumerate(["small", "medium", "large"]):
            t = r["by_size_tercile"][lab]
            ax.errorbar(k, t["rho"], yerr=[[t["rho"] - t["ci"][0]], [t["ci"][1] - t["rho"]]], fmt="o",
                        color="#1f5fa8", capsize=3)
        ax.axhline(0, color="black", lw=0.6)
        ax.set_xticks(range(3), ["small", "medium", "large"])
        it = r["interaction"]
        ax.set_title(f"{o}\ninteraction {it['rho']:+.3f} [{it['ci'][0]:+.3f}, {it['ci'][1]:+.3f}]", fontsize=8)
        ax.set_xlabel("early-size tercile")
    axs[0].set_ylabel("psp(CONS_early_home)")
    fig.suptitle("Test D (Palla): consistency effect by early size, EXP5 pooled", fontsize=9)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"fig_palla.{ext}", dpi=200)
    plt.close(fig)


# ----------------------------------------------------------------------------- method_out.json
class RankOLS:
    """Frozen rank-OLS fitted on DEV: target = normal-score rank of O2r_m50; features = DEV empirical-CDF ranks.
    Prediction mapped back to the O2r_m50 scale through the DEV quantile function."""

    def __init__(self, dev: pd.DataFrame, feats: list[str], y: str = "O2r_m50"):
        d = dev.dropna(subset=feats + [y])
        self.feats, self.y = feats, y
        self.ref = {f: np.sort(d[f].to_numpy(float)) for f in feats}
        self.yref = np.sort(d[y].to_numpy(float))
        X = self._X(d)
        yr = (rankdata(d[y]) - 0.5) / len(d)
        self.beta, *_ = np.linalg.lstsq(X, yr, rcond=None)
        self.n = len(d)

    def _X(self, d: pd.DataFrame) -> np.ndarray:
        cols = [np.ones(len(d))]
        for f in self.feats:
            v = d[f].to_numpy(float)
            r = np.searchsorted(self.ref[f], v, side="left") + np.searchsorted(self.ref[f], v, side="right")
            cols.append(r / (2.0 * len(self.ref[f])))
        return np.column_stack(cols)

    def predict(self, d: pd.DataFrame) -> np.ndarray:
        q = np.clip(self._X(d) @ self.beta, 0.0, 1.0)
        return np.quantile(self.yref, q)


def make_method_out(df: pd.DataFrame, pred0: np.ndarray, pred1: np.ndarray) -> dict:
    def fmt(v):
        return "NA" if v is None or (isinstance(v, float) and not math.isfinite(v)) else f"{float(v):.4f}"

    def num(v):
        return None if v is None or (isinstance(v, float) and not math.isfinite(v)) else float(v)

    ds = {}
    for i, r in enumerate(df.itertuples()):
        src = "COHORT_2015_17" if r.body == BODY_COHORT else "EXP5_frame"
        ex = {"input": f"{r.name} | ci={int(r.ci)} | t0={int(r.t0)} | group={r.group} | body={r.body}",
              "output": fmt(r.O2r_m50),
              "predict_B5": fmt(pred0[i]), "predict_B5_plus_CONS": fmt(pred1[i]),
              "metadata_ci": int(r.ci), "metadata_t0": int(r.t0), "metadata_group": str(r.group),
              "metadata_group5": str(r.group5), "metadata_body": str(r.body),
              "metadata_CONS_early_home": num(r.CONS_early_home), "metadata_CONS_early_all": num(r.CONS_early_all),
              "metadata_CONS_r_early_home": num(r.CONS_r_early_home),
              "metadata_EMB_early_home_analogue": num(r.EMB_early_home), "metadata_SOC_early_home": num(r.SOC_early_home),
              "metadata_V_t0p2": num(r.V_t0p2), "metadata_V_t0p3": num(r.V_t0p3),
              "metadata_CONS_imputed_dev_median": bool(not np.isfinite(r.CONS_early_home)),
              "metadata_label": SELECTION_LABEL}
        for o in ["O2r_m50", "O2r_resid", "O1c", "O1b", "O3"]:
            ex[f"metadata_{o}"] = num(getattr(r, o))
        ds.setdefault(src, []).append(ex)
    return {"metadata": {"method_name": "Cheng ideational consistency (count-weighted topic co-usage cosine) added "
                         "to the B5 baseline", "baseline": "predict_B5 = rank-OLS on B5 fitted on DEV",
                         "method": "predict_B5_plus_CONS = same + CONS_early_home, fitted on DEV, applied frozen",
                         "output": "O2r_m50 (rarefied venue-field richness at t0+6..t0+8); 'NA' where undefined",
                         "label": SELECTION_LABEL},
            "datasets": [{"dataset": k, "examples": v} for k, v in ds.items()]}


def method_out() -> dict:
    df = pd.read_parquet(DATA / "static_analysis_table.parquet")
    dev = df[df.body == "DEV"]
    med = float(np.nanmedian(dev.CONS_early_home))
    df = df.copy()
    df["CONS_imp"] = df.CONS_early_home.fillna(med)
    dev = df[df.body == "DEV"]
    m0 = RankOLS(dev, B5)
    m1 = RankOLS(dev.assign(CONS_imp=dev.CONS_imp), B5 + ["CONS_imp"])
    p0 = m0.predict(df)
    p1 = m1.predict(df)
    ok_b5 = df[B5].notna().all(1).to_numpy()
    p0[~ok_b5] = np.nan
    p1[~ok_b5] = np.nan
    # held-out comparison (never fitted on these bodies)
    comp = {}
    for bd in ["OLD_HELDOUT", "COHORT_2010_14", BODY_COHORT, "DEV (in-sample)"]:
        m = (df.body == bd.split(" ")[0]).to_numpy() & np.isfinite(df.O2r_m50.to_numpy()) & ok_b5
        if m.sum() < 30:
            continue
        y = df.O2r_m50.to_numpy()[m]
        r0 = float(stats.spearmanr(p0[m], y)[0])
        r1 = float(stats.spearmanr(p1[m], y)[0])
        rng = np.random.default_rng(20260929)
        idx = np.nonzero(m)[0]
        bs = []
        for _ in range(1000):
            i = rng.choice(idx, len(idx))
            bs.append(stats.spearmanr(p1[i], df.O2r_m50.to_numpy()[i])[0] - stats.spearmanr(p0[i], df.O2r_m50.to_numpy()[i])[0])
        comp[bd] = {"n": int(m.sum()), "spearman_B5": r0, "spearman_B5_plus_CONS": r1, "delta": r1 - r0,
                    "delta_ci": np.percentile(bs, [2.5, 97.5]).tolist()}
    beta = {"B5": dict(zip(["const"] + B5, m0.beta.tolist())),
            "B5_plus_CONS": dict(zip(["const"] + B5 + ["CONS_early_home"], m1.beta.tolist())), "n_dev": m1.n,
            "CONS_dev_median_imputation": med}
    jdump({"label": SELECTION_LABEL, "models": beta, "heldout_comparison": comp},
          RES / "predictive_comparison.json")
    out = make_method_out(df, p0, p1)
    (ROOT / "method_out.json").write_text(json.dumps(out, indent=1, allow_nan=False))
    return comp


def run(logger) -> None:
    v = verdict()
    logger.info(f"VERDICT: {v['verdicts']}")
    logger.info(f"Holm: {v['holm_family_one_sided']}")
    figures()
    comp = method_out()
    logger.info(f"predictive comparison: {comp}")
    write_report()
    logger.info("reconciling_cheng.md written")


# ----------------------------------------------------------------------------- write-up
def write_report() -> dict:
    """reconciling_cheng.md: one paragraph for the paper; every number carries its JSON key path."""
    J = {f: jload(RES / f) for f in ["cheng_panel_models.json", "cheng_static.json", "cheng_verdict.json",
                                      "identity_check.json", "panel_C.json", "palla.json", "coupling.json",
                                      "audit.json", "predictive_comparison.json"] if (RES / f).exists()}
    H = {}

    def v(file: str, path: str, fmt: str = "{:+.3f}", scale: float = 1.0) -> str:
        x = g(J[file], path)
        H[f"{file}:{path}"] = x
        s = fmt.format(x if scale == 1.0 else x * scale) if isinstance(x, (int, float)) else str(x)
        return f"{s} `[{file}:{path}]`"

    def ci(file: str, path: str, fmt: str = "{:+.3f}", scale: float = 1.0) -> str:
        x = g(J[file], path)
        H[f"{file}:{path}"] = x
        return f"[{fmt.format(x[0] * scale)}, {fmt.format(x[1] * scale)}] `[{file}:{path}]`"

    P, S, Vd = "cheng_panel_models.json", "cheng_static.json", "cheng_verdict.json"
    hj = "builds.HOME.joint"
    pr = f"trait.{PRIMARY}|CONS_early_home"
    co = f"trait.{BODY_COHORT}|CONS_early_home"
    para = (
        f"**Reconciling Cheng et al. (2023).** We rebuilt Cheng et al.'s ideational consistency (cosine of a concept's "
        f"neighbour co-usage vector from t-1 to t) on OpenAlex topic co-usage for "
        f"{v(P, f'{hj}.A1.n_concepts', '{:,}')} concepts ({v(P, f'{hj}.A1.n_rows', '{:,}')} concept-years). In "
        f"their design (next-year volume, age and year controls, no current-size control) the negative-binomial "
        f"twin reproduces their estimate almost exactly: b = {v(P, f'{hj}.A1_NB.coef.zCONS.b', '{:.3f}')}, i.e. "
        f"{v(P, f'{hj}.A1_NB.coef.zCONS.pct_per_sd', '{:+.1f}%', 100)} articles per SD (Cheng: b = .43, +53%); PPML "
        f"gives {v(P, f'{hj}.A1.coef.zCONS.pct_per_sd', '{:+.1f}%', 100)} "
        f"{ci(P, f'{hj}.A1.coef.zCONS.pct_ci', '{:+.1f}%', 100)}. Adding the current volume log V(t) removes almost "
        f"all of it: {v(P, f'{hj}.A2.coef.zCONS.pct_per_sd', '{:+.1f}%', 100)} "
        f"{ci(P, f'{hj}.A2.coef.zCONS.pct_ci', '{:+.1f}%', 100)}, an A2/A1 ratio of "
        f"{v(P, f'{hj}.ratio_boot.ratio', '{:.3f}')} (500-draw concept-cluster bootstrap "
        f"{ci(P, f'{hj}.ratio_boot.ratio_ci', '{:.3f}')}), and concept fixed effects leave "
        f"{v(P, f'{hj}.A3.coef.zCONS.pct_per_sd', '{:+.1f}%', 100)}. The same pattern holds on the all-papers build "
        f"(ratio {v(P, 'builds.ALL.joint.ratio_boot.ratio', '{:.3f}')}). So in this corpus consistency's volume "
        f"effect is mostly a proxy for current size. As an early trait (t0+1..t0+2), consistency still correlates "
        f"with volume at t0+3 (Spearman {v(S, f'volume.{PRIMARY}|volume.B_raw_spearman_V_t0p3.rho')} "
        f"{ci(S, f'volume.{PRIMARY}|volume.B_raw_spearman_V_t0p3.ci')}). But net of the B5 size/growth/breadth "
        f"baseline it predicts LESS later cross-field reach: partial Spearman with rarefied venue-field richness "
        f"O2r_m50 = {v(S, f'{pr}.psp.O2r_m50.rho')} {ci(S, f'{pr}.psp.O2r_m50.ci')} on the pooled EXP5 bodies "
        f"(DerSimonian-Laird over five field groups {v(S, f'DL.{PRIMARY}.O2r_m50.b')}, I2 = "
        f"{v(S, f'DL.{PRIMARY}.O2r_m50.I2', '{:.2f}')}, {v(S, f'DL.{PRIMARY}.O2r_m50.n_negative', '{:d}')}/5 groups "
        f"negative). This replicates on the 2015-17 cohort ({v(S, f'{co}.psp.O2r_m50.rho')} "
        f"{ci(S, f'{co}.psp.O2r_m50.ci')}, n = {v(S, f'{co}.psp.O2r_m50.n', '{:d}')}). It carries no depth "
        f"information: sustained uptake O1c {v(S, f'{pr}.psp.O1c.rho')} {ci(S, f'{pr}.psp.O1c.ci')} and "
        f"transience O3 {v(S, f'{pr}.psp.O3.rho')} {ci(S, f'{pr}.psp.O3.ci')}. The paired depth-minus-reach gap is "
        f"{v(S, f'{pr}.paired_diff.O1c-O2r_m50.rho')} {ci(S, f'{pr}.paired_diff.O1c-O2r_m50.ci')}, but its "
        f"group-pooled DL CI includes 0 ({ci(S, f'DL.{PRIMARY}.O1c-O2r_m50.ci')}). The measure is close to, but not "
        f"identical with, unweighted edge persistence (Spearman with Exp11 Jaccard persistence "
        f"{v('identity_check.json', 'by_body.EXP5_pooled.jaccard_exp11_early.rho', '{:.2f}')}). Within concepts "
        f"(concept and year fixed effects), a more consistent year is followed by slightly MORE new off-home field "
        f"entries, not fewer ({v('panel_C.json', 'C1.coef.zCONS.pct_per_sd', '{:+.1f}%', 100)} per SD, "
        f"concept-cluster bootstrap CI of b {ci('panel_C.json', 'C1.boot.ci')}). So the negative reach association is "
        f"a between-concept trait of early consistency, not a within-concept dynamic. No Palla-type size x "
        f"consistency interaction appears on transience (rank-OLS interaction "
        f"{v('palla.json', 'results.EXP5_pooled|O3.interaction.rho')} "
        f"{ci('palla.json', 'results.EXP5_pooled|O3.interaction.ci')}). The reversal is "
        f"therefore one of sign across outcome families: consistency goes with more volume and less reach, and with "
        f"no extra depth. All bodies are selection data whose outcomes were read before (not confirmation).")
    verdict_line = ", ".join(J[Vd]["verdicts"]) if Vd in J else "n/a"
    txt = ("# Reconciling Cheng et al. (2023) with the reach results\n\n"
           f"Frozen verdict (`results/cheng_verdict.json:verdicts`): **{verdict_line}** "
           "(selection data, not confirmation).\n\n" + para + "\n")
    (ROOT / "reconciling_cheng.md").write_text(txt)
    jdump({"label": SELECTION_LABEL, "numbers": H}, RES / "headline_numbers.json")
    return H
