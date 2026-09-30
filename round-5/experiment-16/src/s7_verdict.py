#!/usr/bin/env python3
"""S4 post-processing: DL over groups, disattenuated effects, P1-P3, Holm and the mechanical VERDICT from the frozen
rules; headline table; figures forest_raw_vs_clean.png and reliability_bars.png.
-> results/clean_vs_raw_psp.json (label: selection data, outcomes previously unsealed)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, FIGS, RES, jdump, setup_logger
from rq1stats import dersimonian_laird, holm

logger = setup_logger("s7_verdict")
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517", "POOLED"]
POOL_GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]


def relkey(x: str) -> str | None:
    if x.startswith("NOVCHURN_rare"):
        return "NOVCHURN_rare5"
    for base in ("NOV_res", "edge_persistence", "ego_density_W3"):
        if x.startswith(f"{base}_rare"):
            return f"{base}_rare5"
    if x in ("EP_chao", "NOVCHURN_chao", "excess_pers_cfg"):
        return None
    return x


def main() -> None:
    cells = json.loads((RES / "clean_vs_raw_psp_cells.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    boots = dict(np.load(DATA / "psp_boot.npz"))
    psp, pair = cells["psp"], cells["paired"]
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    out: dict = {"label": cells["label"], "B": cells["B"], "seed": cells["seed"], "resampling_unit": "concept"}

    def P(body, x, y="O2r_m50", rung="R2"):
        return psp.get(f"{body}|{x}|{y}|{rung}", {})

    def PR(body, a, b, rung="R2"):
        return pair.get(f"{body}|{a}|{b}|O2r_m50|{rung}", {})
    # ------------------------------------------------------------- DL over groups (POOLED, R2)
    groups = {}
    for key, g in cells["groups_raw"].items():
        b = [g.get(k, {}).get("rho", math.nan) for k in POOL_GROUPS]
        se = [g.get(k, {}).get("se", math.nan) for k in POOL_GROUPS]
        dl = dersimonian_laird(b, se)
        groups[key] = {"groups": g, "DL": dl, "n_positive_of_5": int(sum(1 for v in b if v is not None and
                                                                          np.isfinite(v) and v > 0))}
    out["groups"] = groups
    # ------------------------------------------------------------- disattenuation
    rel_y = rel["outcome"]["O2r_m50"]
    rng = np.random.default_rng(20260938)
    dis = {}
    n_pool = rel["variants"]["NOVCHURN_raw"]["pooled"]["n_concepts_mean"]
    for key, r in psp.items():
        body, x, y, rung = key.split("|")
        if y != "O2r_m50" or rung not in ("R2", "R3") or not np.isfinite(r.get("rho") or math.nan):
            continue
        rk = relkey(x)
        bk = "pooled" if body == "POOLED" else body
        if rk is None or rk not in rel["variants"]:
            dis[key] = {"psp": r["rho"], "psp_dis": None, "note": "no split-half reliability for this variant"}
            continue
        sbx = rel["variants"][rk][bk]["SB"]
        ry = (rel_y["pooled"] if body == "POOLED" else rel_y.get(body, rel_y["pooled"]))["SB"]
        if sbx is None or not np.isfinite(sbx) or sbx < 0.10 or ry is None:
            dis[key] = {"psp": r["rho"], "SB_x": sbx, "rel_y": ry, "psp_dis": None,
                        "note": "SB_x < 0.10: not disattenuated (variant essentially unreliable)"}
            continue
        sd_x = rel["variants"][rk]["pooled"].get("SB_boot_sd") or 0.01
        nb = rel["variants"][rk][bk].get("n_concepts_mean", n_pool) or n_pool
        sd_x = sd_x * math.sqrt(n_pool / max(nb, 1))
        sd_y = rel_y["pooled"].get("SB_boot_sd") or 0.005
        bs = boots.get(key.replace("|", "__"))
        est = r["rho"] / math.sqrt(sbx * ry)
        ci = [None, None]
        if bs is not None and len(bs):
            sx = np.clip(rng.normal(sbx, sd_x, len(bs)), 0.05, 1.0)
            syy = np.clip(rng.normal(ry, sd_y, len(bs)), 0.05, 1.0)
            dd = bs / np.sqrt(sx * syy)
            ci = [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]
        dis[key] = {"psp": r["rho"], "SB_x": sbx, "SB_x_key": rk, "rel_y": ry, "psp_dis": est, "ci": ci,
                    "flag": "approximate for partial Spearman (Spearman 1904 correction applied to a rank partial "
                            "correlation); rel_y conservative (m = 25 halves)"}
    out["disattenuated"] = dis
    # ------------------------------------------------------------- F6 contingency
    n_r10 = P("COH1517", "NOVCHURN_rare10").get("n", 0)
    n_r5 = P("COH1517", "NOVCHURN_rare5").get("n", 0)
    rare_primary_coh = "NOVCHURN_rare10" if n_r10 >= 150 else ("NOVCHURN_rare5" if n_r5 >= 100 else None)
    out["F6_contingency"] = {"COH1517_n_rare10": n_r10, "COH1517_n_rare5": n_r5,
                             "COH1517_rare_primary": rare_primary_coh}
    rare_primary = {"COH1517": rare_primary_coh, "OLDHO": "NOVCHURN_rare10"}
    # ------------------------------------------------------------- P1-P3
    ratios = {}
    for b in ("COH1517", "OLDHO"):
        pe = PR(b, "NOVCHURN_exc", "NOVCHURN_raw")
        rp = rare_primary[b]
        pv = PR(b, rp, "NOVCHURN_raw") if rp else {}
        ratios[b] = {"exc": pe, "rare_primary": rp, "rare": pv, "raw_full_sample": P(b, "NOVCHURN_raw")}
    p1_each = {b: bool(np.isfinite(ratios[b]["exc"].get("ratio", math.nan)) and ratios[b]["exc"]["ratio"] >= 0.70)
               for b in ratios}
    P1 = all(p1_each.values())
    zc = P("POOLED", "z_pers_cfg")
    P2 = bool(zc and np.isfinite(zc["rho"]) and zc["ci"][1] < 0)
    x = cv.NOVCHURN_exc.to_numpy(float)
    ln = np.log(cv.n_home_early.to_numpy(float))
    ok = np.isfinite(x)
    rho3 = float(stats.spearmanr(x[ok], ln[ok])[0])
    bsr = []
    idx = np.nonzero(ok)[0]
    for _ in range(500):
        i = rng.choice(idx, len(idx))
        bsr.append(stats.spearmanr(x[i], ln[i])[0])
    bsr = np.asarray(bsr)
    P3 = abs(rho3) < 0.20
    # same test on the analysis sample (finite O2r_m50)
    from tables import load_tables
    T = load_tables()["POOLED"]
    oka = np.isfinite(T.NOVCHURN_exc) & np.isfinite(T.O2r_m50)
    rho3a = float(stats.spearmanr(T.NOVCHURN_exc[oka], np.log(T.n_home_early[oka]))[0])
    out["predictions"] = {
        "P1": {"holds": P1, "per_body": p1_each, "rule": "psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, "
                                                        "COH1517 AND OLDHO",
               "detail": {b: {"ratio": ratios[b]["exc"].get("ratio"), "ratio_ci": ratios[b]["exc"].get("ratio_ci"),
                              "psp_exc": ratios[b]["exc"].get("a"), "psp_raw_same_sample": ratios[b]["exc"].get("b"),
                              "n": ratios[b]["exc"].get("n")} for b in ratios}},
        "P2": {"holds": P2, "psp": zc.get("rho"), "ci": zc.get("ci"), "n": zc.get("n")},
        "P3": {"holds": P3, "spearman_NOVCHURN_exc_log_n_all": rho3,
               "ci": [float(np.percentile(bsr, 2.5)), float(np.percentile(bsr, 97.5))], "n": int(ok.sum()),
               "spearman_on_analysis_sample": rho3a, "n_analysis": int(oka.sum())}}
    # ------------------------------------------------------------- verdict
    keep = {}
    for b in ("COH1517", "OLDHO"):
        rv = ratios[b]["rare"]
        keep[b] = rv.get("ratio") if rv else None
    v1_keep = any(v is not None and np.isfinite(v) and v >= 0.5 for v in keep.values())
    raw_ci_excl0 = {b: bool(ratios[b]["raw_full_sample"] and (ratios[b]["raw_full_sample"]["ci"][0] > 0 or
                                                             ratios[b]["raw_full_sample"]["ci"][1] < 0))
                    for b in ratios}
    thin_each = {b: bool(np.isfinite(ratios[b]["exc"].get("ratio", math.nan)) and ratios[b]["exc"]["ratio"] < 0.30 and
                         (keep[b] is None or not np.isfinite(keep[b]) or keep[b] < 0.30)) for b in ratios}
    if P1 and P3 and v1_keep:
        verdict = "CHURN_NOT_THIN"
    elif any(raw_ci_excl0.values()) and all(thin_each.values()):
        verdict = "CHURN_THIN"
    else:
        verdict = "PARTLY_THIN"
    ep_raw = P("POOLED", "edge_persistence__raw")
    flag = bool((not P2) and ep_raw and ep_raw["ci"][1] < 0)
    out["verdict"] = {"verdict": verdict, "DEGREE_ARTEFACT_PERSISTENCE": flag,
                      "clauses": {"P1": P1, "P3": P3, "V1_keeps_ge_50pct_in_COH1517_or_OLDHO": v1_keep,
                                  "V1_retention": keep, "raw_NOVCHURN_ci_excludes_0": raw_ci_excl0,
                                  "exc_and_rare_keep_lt_30pct": thin_each, "P2": P2,
                                  "raw_edge_persistence_pooled_ci_lt0": bool(ep_raw and ep_raw["ci"][1] < 0)},
                      "label": "selection data, outcomes previously unsealed: robustness evidence, not confirmation"}
    # Holm (reported only)
    p1p = max(P("COH1517", "NOVCHURN_exc").get("p_one", math.nan), P("OLDHO", "NOVCHURN_exc").get("p_one", math.nan))
    p2p = zc.get("p_one", math.nan)
    p3p = float((np.sum(np.abs(bsr) >= 0.20) + 1) / (len(bsr) + 1))
    ph = holm([p1p, p2p, p3p])
    out["holm"] = {"family": ["P1: NOVCHURN_exc psp > 0 in COH1517 and OLDHO (max one-sided p)",
                              "P2: z_pers_cfg psp < 0 POOLED", "P3: |Spearman(NOVCHURN_exc, log n)| >= 0.20 (boot)"],
                   "p": [p1p, p2p, p3p], "p_holm": ph}
    # ------------------------------------------------------------- headline table
    head = []
    for x in ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_zperm", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_cfg",
              "NOVCHURN_chao", "NOV_res__raw", "NOV_res_exc", "NOV_res_rare10", "edge_persistence__raw",
              "edge_persistence_exc", "edge_persistence_rare10", "z_pers_cfg", "excess_pers_cfg", "EP_chao",
              "edge_persistence_nullmean", "ego_density_W3__raw", "z_dens_cfg", "z_dens_k", "OPEN_home",
              "OPEN_home_clean", "OPEN_home_exc"]:
        row = {"variant": x}
        for b in BODIES:
            r = P(b, x)
            row[b] = {"psp": r.get("rho"), "ci": r.get("ci"), "n": r.get("n")}
            raw = {"NOVCHURN": "NOVCHURN_raw", "NOV_res": "NOV_res__raw", "edge_persistence": "edge_persistence__raw",
                   "z_pers": "edge_persistence__raw", "excess_pers": "edge_persistence__raw",
                   "EP_chao": "edge_persistence__raw", "ego_density": "ego_density_W3__raw", "z_dens": "ego_density_W3__raw",
                   "OPEN_home": "OPEN_home"}
            rr = next((v for k, v in raw.items() if x.startswith(k)), None)
            if rr and rr != x:
                pr = PR(b, x, rr)
                if pr:
                    row[b]["same_sample_raw"] = pr.get("b")
                    row[b]["retention_ratio"] = pr.get("ratio")
                    row[b]["retention_ratio_ci"] = pr.get("ratio_ci")
                    row[b]["diff_ci"] = pr.get("diff_ci")
        head.append(row)
    out["headline_R2_O2r_m50"] = head
    out["cells"] = {"psp": psp, "paired": pair, "planted_PC3": cells["planted_PC3"]}
    out["confounds_removed"] = {
        "V1_rare": "removes the dependence of persistence/NOV_res on the number of home papers per year (fixed n); "
                   "does NOT remove concept-level topic heterogeneity; restricts the sample to concepts with >= n per "
                   "W-year (same-sample raw reported)",
        "V2_exc": "removes what the concept's own pooled papers would produce under a stationary partner distribution "
                  "(sampling noise given n and the concept's topic mix); conservative -- PC2 shows it also absorbs "
                  "most planted true churn at these sample sizes",
        "V2b_chao": "abundance-based undersampling correction of Jaccard; does not remove the count>=2/PMI "
                    "neighbour-rule sensitivity",
        "V3a_z_dens_cfg": "removes the part of ego density explained by partner degrees (configuration backbone); "
                          "does not remove true modular structure",
        "V3b_z_dens_k": "removes dependence of density on |S| and partner popularity",
        "V3c_z_pers_cfg": "degree normalisation of Jaccard given neighbour-set sizes and topic popularity per year; "
                          "null expected Jaccard ~0 so z ~ obs / sd; NaN when the null sd is 0 (small sets)"}
    jdump(out, RES / "clean_vs_raw_psp.json")
    logger.info(f"VERDICT {verdict}; P1 {P1} {p1_each}; P2 {P2}; P3 {P3} (rho {rho3:.3f}); V1 keep {keep}; "
                f"degree flag {flag}")
    # ------------------------------------------------------------- figures
    fvars = ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_rare10", "NOVCHURN_cfg", "NOVCHURN_chao", "OPEN_home",
             "OPEN_home_clean", "NOV_res__raw", "NOV_res_exc", "edge_persistence__raw", "edge_persistence_exc",
             "edge_persistence_rare10", "z_pers_cfg"]
    fig, axes = plt.subplots(1, len(BODIES), figsize=(17, 6), sharey=True)
    for ax, b in zip(axes, BODIES):
        for i, x in enumerate(fvars):
            r = P(b, x)
            if not r or r.get("rho") is None or not np.isfinite(r["rho"]):
                continue
            col = "C3" if ("raw" in x or x == "OPEN_home") else "C0"
            ax.errorbar(r["rho"], i, xerr=[[r["rho"] - r["ci"][0]], [r["ci"][1] - r["rho"]]], fmt="o", color=col,
                        ms=4, capsize=2)
        ax.axvline(0, color="k", lw=0.7)
        ax.set_title(f"{b}", fontsize=10)
        ax.set_yticks(range(len(fvars)), fvars, fontsize=8)
        ax.set_xlabel("partial Spearman | R2 (O2r_m50)", fontsize=8)
    axes[0].invert_yaxis()
    fig.suptitle("Raw (red) vs noise-controlled (blue) churn / openness variants; 95% concept-bootstrap CI; "
                 "selection data, outcomes previously unsealed", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "forest_raw_vs_clean.png", dpi=150)
    rv = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "NOVCHURN_raw", "OPEN_home",
          "edge_persistence_nullmean", "NOV_res_exc", "edge_persistence_exc", "NOVCHURN_exc", "NOV_res_rare5",
          "edge_persistence_rare5", "NOVCHURN_rare5", "z_pers_cfg", "z_dens_cfg", "z_dens_k", "NOVCHURN_cfg",
          "OPEN_home_clean", "OPEN_home_exc"]
    bins = ["n10-19", "n20-49", "n50-99", "n100-inf"]
    fig, ax = plt.subplots(figsize=(13, 4.5))
    w = 0.2
    for j, bn in enumerate(bins):
        vals = [rel["variants"][v][bn]["SB"] if v in rel["variants"] and rel["variants"][v][bn]["SB"] is not None
                else np.nan for v in rv]
        ax.bar(np.arange(len(rv)) + (j - 1.5) * w, vals, w, label=bn)
    pooled = [rel["variants"][v]["pooled"]["SB"] for v in rv]
    ax.plot(np.arange(len(rv)), pooled, "k_", ms=14, mew=2, label="pooled")
    ax.axhline(0.6, color="grey", ls="--", lw=0.8)
    ax.set_xticks(np.arange(len(rv)), rv, rotation=60, ha="right", fontsize=8)
    ax.set_ylabel("split-half reliability (Spearman-Brown)")
    ax.legend(fontsize=8, ncol=5)
    ax.set_title(f"Reliability by n_home_early bin; outcome O2r_m50 SB = {rel_y['pooled']['SB']:.2f} (m = 25 halves)")
    fig.tight_layout()
    fig.savefig(FIGS / "reliability_bars.png", dpi=150)
    logger.info("figures written")


if __name__ == "__main__":
    main()
