#!/usr/bin/env python3
"""Screen of candidate G (gateway landing) on the frozen P78 dev panel under protocol S0 + authoritative outcome
tables. Runs fully offline from the frozen cache (cache/raw) and the public sources snapshot; 0 API credits.

Usage: .venv/bin/python method.py            (writes all outputs into this directory)
"""
from __future__ import annotations

import json
import math
import resource
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
(ROOT / "logs").mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")
resource.setrlimit(resource.RLIMIT_AS, (12 * 1024 ** 3, 12 * 1024 ** 3))

import oa_client as oa  # noqa: E402
from assemble import assemble  # noqa: E402
from backbone import build as build_backbone  # noqa: E402
from features import (Backbone, cohort_split_half, count_indicators, g_family, g_from_labels,  # noqa: E402
                      label_indicators, outcomes, rarefied_richness, shannon)
from next_field import analyse as nf_analyse, build_rows as nf_rows  # noqa: E402
from screen import (GROUPS, field_level, loco_delta, paired_delta, single_indicator)  # noqa: E402

N_BOOT = 2000
REFIT_BOOT = 200
TRUNC_THR = 0.15


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not np.isfinite(o) else float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def concept_features(r: dict, bb: Backbone, gtot: dict) -> dict:
    t0 = int(r["t0"])
    w = r["windows"]
    A, B, D = w["A"], w["B"], w.get("D")
    fW3 = Counter(A["fields"]) + Counter(B["fields"])
    totW3 = A["total"] + B["total"]
    home = r["home"]
    f = {"concept": r["concept"]}
    gf = g_family(dict(fW3), home, bb)
    f.update({k: v for k, v in gf.items()})
    f["G_missing"] = int(not np.isfinite(gf["G"]))
    gA = g_family(dict(A["fields"]), home, bb)
    f["G_A"] = gA["G"]  # G on t0..t0+1 only (earlier landing)
    for k, v in label_indicators(dict(fW3), home, totW3).items():
        f[f"{k}_W3"] = v
    nA = sum(1 for n in A["fields"].values() if n >= 1)
    nBnew = sum(1 for fl, n in B["fields"].items() if n >= 1 and A["fields"].get(fl, 0) == 0)
    f["fields_gained_per_year_W3"] = (nA + nBnew) / 3
    for wn, end in (("W3", t0 + 2), ("W5", t0 + 4)):
        for k, v in count_indicators(r["yc"], gtot, t0, end).items():
            f[f"{k}_{wn}"] = v
    f["growth_W5_B5"] = math.log((r["yc"].get(t0 + 4, 0) + 1) / (r["yc"].get(t0 + 1, 0) + 1))
    f["label_coverage_early"] = f["label_coverage_W3"]
    f["label_coverage_outcome"] = (D["labelled"] / D["total"]) if D and D["total"] else math.nan
    f["trunc_share_outcome"] = D["truncated_share"] if D else math.nan
    f["trunc"] = int(D is not None and D["truncated_share"] > TRUNC_THR)
    return f


def field_rows(r: dict, bb: Backbone) -> list[dict]:
    w = r["windows"]
    A, B, D = w["A"], w["B"], w.get("D")
    if not D:
        return []
    fW3 = Counter(A["fields"]) + Counter(B["fields"])
    labW3, labD = sum(fW3.values()), sum(D["fields"].values())
    K = {bb.idx[x] for x, n in fW3.items() if n >= 2}
    home_idx = [bb.idx[h] for h in r["home"] if h in bb.idx]
    rows = []
    for j, n in fW3.items():
        if j in r["home"] or n < 5:
            continue
        k = bb.idx[j]
        Kj = K - {k}
        den = bb.phi[:, k].sum()
        dens = bb.phi[list(Kj), k].sum() / den if Kj and den > 0 else 0.0
        sW3 = n / labW3
        nD = D["fields"].get(j, 0)
        sD = nD / labD if labD else math.nan
        rows.append({"concept": r["concept"], "group": r["group"], "field": j, "n_W3": n, "n_A": A["fields"].get(j, 0),
                     "n_B": B["fields"].get(j, 0), "share_W3": sW3, "n_outcome": nD, "share_outcome": sD,
                     "R": int(sD >= 0.5 * sW3 and nD >= 9) if np.isfinite(sD) else math.nan,
                     "log_n_W3": math.log1p(n),
                     "growth_j": math.log((B["fields"].get(j, 0) + 1) / (A["fields"].get(j, 0) / 2 + 1)),
                     "gateway_j": bb.g(j), "phi_home_j": float(np.mean([bb.phi[h, k] for h in home_idx])),
                     "density_j": dens, "log_field_size": bb.logsize[k]})
    return rows


@logger.catch(reraise=True)
def main() -> None:
    t_start = time.time()
    logger.info("assembling cached data")
    data = assemble()
    C = data["concepts"]
    gtot = data["meta"]["global_totals"]
    bdict = build_backbone()
    bb = Backbone(bdict)
    (ROOT / "field_backbone.json").write_text(json.dumps(clean(bdict), indent=1))

    dev = {k: v for k, v in C.items() if v["status"] == "dev" and v.get("windows")}
    logger.info(f"dev concepts: {len(dev)}")
    feats = pd.DataFrame([concept_features(r, bb, gtot) for r in dev.values()])
    meta_cols = pd.DataFrame([{"concept": r["concept"], "group": r["group"], "t0": int(r["t0"]),
                               "newborn": bool(r["newborn"]), "thin_home": bool(r.get("thin_home")),
                               "home": ";".join(r["home"])} for r in dev.values()])
    feats = meta_cols.merge(feats, on="concept")

    # ---------------------------------------------------------------- outcomes (authoritative, all 78 rows)
    orows = []
    for nm, r in C.items():
        base = {"concept": nm, "panel_entry": r["panel_entry"], "aliases_used": "|".join(r["aliases_used"]),
                "intended_group": r["intended_group"], "t0": r["t0"], "newborn": r["newborn"], "status": r["status"],
                "dev": int(nm in dev), "home": ";".join(r.get("home", []) or []), "group": r.get("group")}
        if nm in dev:
            D = r["windows"].get("D")
            o = outcomes(r["yc"], gtot, int(r["t0"]), D["fields"] if D else None)
            f = feats.set_index("concept").loc[nm]
            base.update({"thin_home": r.get("thin_home"), "label_coverage_early": f["label_coverage_early"],
                         "label_coverage_outcome": f["label_coverage_outcome"],
                         "outcome_window_pulled": int(D is not None), "trunc_share_outcome": f["trunc_share_outcome"],
                         "trunc": int(f["trunc"]) if D else None, **o})
        orows.append(base)
    out_df = pd.DataFrame(orows)
    dmask = out_df["dev"] == 1
    ok = dmask & out_df["O2r_m30"].notna()
    X = np.log(out_df.loc[ok, "N_outcome"].astype(float).values)
    yv = out_df.loc[ok, "O2r_m30"].astype(float).values
    beta = np.polyfit(X, yv, 1)
    out_df["O2r_resid"] = np.nan
    out_df.loc[ok, "O2r_resid"] = yv - np.polyval(beta, X)
    col_order = ["concept", "panel_entry", "aliases_used", "intended_group", "t0", "newborn", "status", "dev", "home",
                 "group", "thin_home", "label_coverage_early", "label_coverage_outcome", "outcome_window_pulled",
                 "trunc", "trunc_share_outcome", "N_outcome", "O1", "O2r_m30", "O2r_m50", "O2r_resid", "O2_raw",
                 "O3", "peak_year"]
    out_df = out_df[col_order]
    out_df.to_csv(ROOT / "outcomes.csv", index=False)
    logger.info(f"outcomes.csv rows={len(out_df)}; dev={int(dmask.sum())}; with O2r={int(ok.sum())}")

    df = feats.merge(out_df[["concept", "O1", "O2r_m30", "O2r_m50", "O2r_resid", "O2_raw", "O3", "N_outcome"]],
                     on="concept")
    df.to_csv(ROOT / "features.csv", index=False)

    # ---------------------------------------------------------------- field-level rows
    fr = pd.DataFrame([row for r in dev.values() for row in field_rows(r, bb)])
    fr.to_csv(ROOT / "field_outcomes.csv", index=False)

    # ---------------------------------------------------------------- validations
    val = {}
    mc = {}
    rng = np.random.default_rng(0)
    for nm in list(df.dropna(subset=["O2r_m30"])["concept"])[:3]:
        counts = np.array([v for v in dev[nm]["windows"]["D"]["fields"].values() if v > 0])
        labels = np.repeat(np.arange(len(counts)), counts)
        sims = [len(np.unique(rng.choice(labels, 30, replace=False))) for _ in range(100_000)]
        mc[nm] = {"exact": rarefied_richness(counts, 30), "monte_carlo_1e5": float(np.mean(sims))}
    val["rarefaction_vs_mc"] = mc
    val["O2r_range_ok"] = bool(df["O2r_m30"].dropna().between(1, 26).all())
    val["label_coverage_early_range"] = [float(df["label_coverage_early"].min()), float(df["label_coverage_early"].max())]
    val["api_snapshot_label_agreement"] = data["meta"]["api_snapshot_label_agreement"]

    # ---------------------------------------------------------------- screen
    B5 = ["log_count_W5", "growth_W5_B5", "offhome_share_W3", "entropy_W3", "reach_W3"]
    CAND = B5 + ["G", "G_missing"]
    d2 = df.dropna(subset=["O2r_m30"]).reset_index(drop=True)
    n_per_group = d2["group"].value_counts().to_dict()
    logger.info(f"screen n={len(d2)} per group {n_per_group}")
    scr = {}
    for y in ("O2r_m30", "O2r_m50", "O2r_resid"):
        scr[y] = paired_delta(d2, B5, CAND, y, "ridge", N_BOOT, refit_boot=REFIT_BOOT if y == "O2r_m30" else 0)
        logger.info(f"{y}: base={scr[y]['base']:.3f} cand={scr[y]['cand']:.3f} delta={scr[y]['delta']:.3f} "
                    f"ci90={scr[y]['ci90']}")
    for y in ("O1", "O3"):
        scr[y] = paired_delta(df, B5, CAND, y, "logit", N_BOOT)
        pos = int(df[y].sum())
        grp_pos = df.groupby("group")[y].sum()
        scr[y]["n_positive"] = pos
        scr[y]["n_negative"] = int(len(df) - pos)
        scr[y]["positives_per_group"] = grp_pos.astype(int).to_dict()
        scr[y]["evaluable"] = bool(min(pos, len(df) - pos) >= 5 and (grp_pos > 0).sum() >= 2)
        if not scr[y]["evaluable"]:
            scr[y]["note"] = (f"not evaluable: only {min(pos, len(df) - pos)} concepts in the minority class "
                              f"(positives per group {grp_pos.astype(int).to_dict()}); LOGO training folds lack one "
                              "class, so AUCs are artefacts and are not interpreted")
        logger.info(f"{y}: base AUC={scr[y]['base']:.3f} cand={scr[y]['cand']:.3f} delta={scr[y]['delta']:.3f} "
                    f"evaluable={scr[y]['evaluable']}")
    scr["LOCO_O2r_m30"] = loco_delta(d2, B5, CAND, "O2r_m30")

    # reliability & size
    home_of = {nm: dev[nm]["home"] for nm in d2["concept"]}
    mats = [[fl for fl, n in (Counter(dev[nm]["windows"]["A"]["fields"]) +
                              Counter(dev[nm]["windows"]["B"]["fields"])).items() for _ in range(n)]
            for nm in df["concept"]]
    homes_all = [dev[nm]["home"] for nm in df["concept"]]
    rel = {}
    for fname, fn in (("G", lambda labs, h: g_from_labels(labs, h, bb)),
                      ("G_all", lambda labs, h: g_family(Counter(labs), h, bb)["G_all"]),
                      ("RS", lambda labs, h: g_family(Counter(labs), h, bb)["RS"]),
                      ("REL_home", lambda labs, h: g_family(Counter(labs), h, bb)["REL_home"]),
                      ("entropy_W3", lambda labs, h: shannon(Counter(labs))),
                      ("offhome_share_W3", lambda labs, h: (sum(1 for x in labs if x not in h) / len(labs))
                       if labs else math.nan)):
        # pair each concept's labels with its home via closure over index
        vals = []
        rng2 = np.random.default_rng(11)
        rs = []
        for _ in range(50):
            a, b = [], []
            for labs, h in zip(mats, homes_all):
                idx = rng2.permutation(len(labs))
                hh = len(labs) // 2
                a.append(fn([labs[i] for i in idx[:hh]], h))
                b.append(fn([labs[i] for i in idx[hh:2 * hh]], h))
            a, b = np.array(a, float), np.array(b, float)
            okk = np.isfinite(a) & np.isfinite(b)
            r_ = spearmanr(a[okk], b[okk]).statistic
            rs.append(2 * r_ / (1 + r_))
        rel[fname] = {"r_sb_median": float(np.median(rs)), "p05": float(np.percentile(rs, 5)),
                      "p95": float(np.percentile(rs, 95)), "n_splits": 50}
    # count-only reliability via binomial thinning
    rng3 = np.random.default_rng(12)
    rsb = []
    for _ in range(50):
        a, b = [], []
        for nm in df["concept"]:
            r = dev[nm]
            t0 = int(r["t0"])
            ys = range(t0, t0 + 5)
            n = np.array([r["yc"][y] for y in ys])
            ha = rng3.binomial(n, 0.5)
            a.append(math.log1p(ha.sum()))
            b.append(math.log1p((n - ha).sum()))
        r_ = spearmanr(a, b).statistic
        rsb.append(2 * r_ / (1 + r_))
    rel["log_count_W5"] = {"r_sb_median": float(np.median(rsb)), "method": "binomial thinning"}
    size = {"G_vs_log_count_W5": float(spearmanr(df["G"], df["log_count_W5"], nan_policy="omit").statistic),
            "G_vs_growth_W5": float(spearmanr(df["G"], df["growth_W5_B5"], nan_policy="omit").statistic),
            "G_vs_label_coverage": float(spearmanr(df["G"], df["label_coverage_early"], nan_policy="omit").statistic)}
    size["max_abs"] = max(abs(size["G_vs_log_count_W5"]), abs(size["G_vs_growth_W5"]))

    prim = scr["O2r_m30"]
    few = len(d2) < 25 or min(n_per_group.get(g, 0) for g in GROUPS) < 5
    clauses = {"i_delta_ge_0.10_and_ci90_low_gt_0": bool(prim["delta"] >= 0.10 and prim["ci90"][0] > 0),
               "ii_positive_in_ge_3_of_4_groups": ("not evaluable" if few else bool(prim["n_groups_positive"] >= 3)),
               "iii_split_half_r_sb_ge_0.6": bool(rel["G"]["r_sb_median"] >= 0.6),
               "iv_max_abs_size_rho_le_0.6": bool(size["max_abs"] <= 0.6)}
    survives = all(v is True for v in clauses.values())

    # sensitivities
    sens = {}
    subsets = {"newborn_only": d2["newborn"], "exclude_trunc": d2["trunc"] == 0, "exclude_thin_home": ~d2["thin_home"],
               "exclude_low_coverage_lt_0.3": d2["label_coverage_early"] >= 0.3}
    for nm, m in subsets.items():
        dd = d2[m.values].reset_index(drop=True)
        if len(dd) >= 12 and dd["group"].nunique() >= 3:
            s = paired_delta(dd, B5, CAND, "O2r_m30", "ridge", N_BOOT)
            sens[nm] = {k: s[k] for k in ("n", "base", "cand", "delta", "ci90", "n_groups_positive")}
        else:
            sens[nm] = {"n": int(len(dd)), "note": "too few concepts for LOGO"}
    for alt in ("G_deg", "G_phimin", "G_btw", "G_A"):
        dd = d2.copy()
        dd["G_alt_missing"] = dd[alt].isna().astype(int)
        s = paired_delta(dd, B5, B5 + [alt, "G_alt_missing"], "O2r_m30", "ridge", N_BOOT)
        sens[f"gateway_variant_{alt}"] = {k: s[k] for k in ("n", "base", "cand", "delta", "ci90", "n_groups_positive")}
    sens["m50"] = {k: scr["O2r_m50"][k] for k in ("n", "base", "cand", "delta", "ci90", "n_groups_positive")}
    hurdle = df[df["N_outcome"].notna() & (df["N_outcome"] < 30)]
    sens["hurdle_N_lt_30"] = {"n": int(len(hurdle)), "O1_rate": float(hurdle["O1"].mean()) if len(hurdle) else None,
                              "O3_rate": float(hurdle["O3"].mean()) if len(hurdle) else None}

    # secondaries one at a time (exploratory)
    secondaries = ["G_all", "G_deg", "G_btw", "G_phimin", "G_A", "REL_home", "RS", "DOM_Physical", "DOM_Life",
                   "DOM_Health", "DOM_Social", "GATEWAY_REACH"]
    sec = {}
    for s_ in secondaries:
        dd = d2.copy()
        dd["_miss"] = dd[s_].isna().astype(int)
        cols = B5 + [s_] + (["_miss"] if dd["_miss"].any() else [])
        r2 = paired_delta(dd, B5, cols, "O2r_m30", "ridge", N_BOOT)
        r1 = paired_delta(df.assign(_miss=df[s_].isna().astype(int)), B5, cols, "O1", "logit", N_BOOT)
        r3 = paired_delta(df.assign(_miss=df[s_].isna().astype(int)), B5, cols, "O3", "logit", N_BOOT)
        sec[s_] = {"label": "exploratory; not the pre-registered primary",
                   "O2r_m30": {k: r2[k] for k in ("delta", "ci90", "n_groups_positive")},
                   "O1": {k: r1[k] for k in ("delta", "ci90", "n_groups_positive")},
                   "O3": {k: r3[k] for k in ("delta", "ci90", "n_groups_positive")}}
    joint = B5 + ["G", "G_missing", "REL_home", "RS", "G_all"]
    jd = d2.copy()
    rj = paired_delta(jd, B5, joint, "O2r_m30", "ridge", N_BOOT)
    sec["joint_B5+G+REL_home+RS+G_all"] = {"label": "exploratory joint composition model (insularity unavailable)",
                                           **{k: rj[k] for k in ("base", "cand", "delta", "ci90", "n_groups_positive")}}

    # field level
    B_field = ["log_n_W3", "growth_j", "share_W3"]
    fl = {"all_four_available": field_level(fr, B_field, B_field + ["gateway_j", "phi_home_j", "density_j"], N_BOOT)}
    for c_ in ("gateway_j", "phi_home_j", "density_j"):
        fl[c_] = field_level(fr, B_field, B_field + [c_], N_BOOT)
    fl["size_controlled_gateway_j"] = field_level(fr, B_field + ["log_field_size"],
                                                   B_field + ["log_field_size", "gateway_j"], N_BOOT)
    fl["size_controlled_all_three"] = field_level(fr, B_field + ["log_field_size"],
                                                  B_field + ["log_field_size", "gateway_j", "phi_home_j", "density_j"],
                                                  N_BOOT)
    fl["log_field_size_alone_added"] = field_level(fr, B_field, B_field + ["log_field_size"], N_BOOT)
    fl["note"] = "I_j (insularity) unavailable: shared key below floor before the insularity stage"

    # single-indicator table
    indicators = ["log_count_W3", "share_W3", "growth_W3", "accel_W3", "burst_W3", "log_count_W5", "share_W5",
                  "growth_W5", "accel_W5", "burst_W5", "growth_W5_B5", "fields_gained_per_year_W3", "entropy_W3",
                  "reach_W3", "offhome_share_W3", "log_offhome_volume_W3", "label_coverage_W3",
                  "G", "G_A", "G_all", "G_deg", "G_btw", "G_phimin", "REL_home", "RS", "GATEWAY_REACH",
                  "DOM_Physical", "DOM_Life", "DOM_Health", "DOM_Social"]
    si_rows = []
    si_full = []
    for ind in indicators:
        for y, binary in (("O2r_m30", False), ("O1", True), ("O3", True)):
            base_df = d2 if y == "O2r_m30" else df
            r = single_indicator(base_df, ind, y, binary)
            si_full.append(r)
            row = {"indicator": ind, "family": "reference" if not ind.startswith(("G", "REL", "RS", "DOM"))
                   else "G-family", "outcome": y, "n": r["n"]}
            if binary:
                row.update({"pooled_raw_auc": r["pooled_raw"], "meta_oriented_auc": r["meta_pooled_oriented"],
                            "meta_ci95_low": r["meta_ci95"][0], "meta_ci95_high": r["meta_ci95"][1], "I2": r["I2"],
                            "sign_consistency_k_of_4": r["sign_consistency"],
                            **{f"raw_{g}": r["per_group_raw"][g] for g in GROUPS},
                            **{f"oriented_{g}": r["per_group_oriented"][g] for g in GROUPS}})
            else:
                row.update({"pooled_spearman": r["pooled"], "meta_spearman": r["meta_pooled"],
                            "meta_ci95_low": r["meta_ci95"][0], "meta_ci95_high": r["meta_ci95"][1], "I2": r["I2"],
                            "sign_consistency_k_of_4": r["sign_consistency"],
                            **{f"raw_{g}": r["per_group"][g] for g in GROUPS}})
            si_rows.append(row)
    si = pd.DataFrame(si_rows)
    si.to_csv(ROOT / "single_indicators.csv", index=False)

    # next-field entry
    nfr = nf_rows(dev, bb)
    nfr.to_csv(ROOT / "next_field_entry.csv", index=False)
    nf = nf_analyse(nfr, bb)
    logger.info(f"next-field: all AUC density={nf['all']['auc_density_mean']:.3f} "
                f"size={nf['all']['auc_size_mean']:.3f} perm p={nf['all'].get('perm_null', {}).get('p_value')}")

    # confirmation signals
    conf = {"B5_alone_oof_spearman_O2r_positive": bool(prim["base"] > 0),
            "entropy_W3_positive_with_O2r": float(si[(si.indicator == "entropy_W3") & (si.outcome == "O2r_m30")]
                                                  ["pooled_spearman"].iloc[0]),
            "reach_W3_positive_with_O2r": float(si[(si.indicator == "reach_W3") & (si.outcome == "O2r_m30")]
                                                ["pooled_spearman"].iloc[0])}

    deviations = [
        "Shared OpenAlex key had ~2,180 credits left at start (five artifacts; reset ~11.7 h later). It fell below the "
        "1,000-credit floor at 12:26 after 286 credits used by this artifact; per plan all pulling stopped there.",
        "Per-year label pulls pooled into windows A=t0..t0+1, B=t0+2, C=t0+3..t0+4, D=t0+6..t0+8 (4 group_by calls "
        "per concept); only the top-200 sources per window were pulled (max_pages=1, degrade-ladder steps 3-4).",
        "Window C (t0+3..t0+4) was never pulled (floor reached): the label-based B5 components (off-home share, "
        "entropy, reach) use W3=t0..t0+2 instead of W5; log_count_W5 and growth_W5=log(n[t0+4]/n[t0+1]) use the free "
        "yearly counts as specified. Field-retention rows use W3 (>=5 labelled papers in t0..t0+2) and share_j(W3).",
        "Outcome window D pulled for 34 of 46 dev concepts (the first ones in the seeded order: an unbiased subset); "
        "O1 and O3 need only yearly counts and use all 46 dev concepts.",
        "Sources in D not looked up via the API before the floor were labelled with the same >=40% topic-profile rule "
        "from the free OpenAlex S3 sources snapshot (2026-09-23); API-vs-snapshot label agreement on the overlap: "
        f"{data['meta']['api_snapshot_label_agreement']:.4f}.",
        "Insularity I_j, phi_cit, SLICE_B, and the P5 primary_topic look were not computed (floor reached). INS "
        "features and the B5+G+INS joint model are absent; gateway sensitivities use weighted degree, betweenness "
        "and a phi_min (Hidalgo proximity) eigenvector instead of SLICE_B/phi_cit.",
        "Alias hygiene: 'NOTES' dropped, 'natural orifice translumenal endoscopic surgery' added (grounding_log.json).",
        "Probe anchors differ from the probe snapshot because S0 adds type:article|review,is_paratext:false "
        "(compressed sensing 2007: 37 vs 120 in the probe's unfiltered query); t0 shifts accordingly.",
        "Field retention '>=3 papers/year' operationalised as >=9 labelled papers pooled over t0+6..t0+8.",
        "Rao-Stirling uses d = 1 - phi_min (co-assignment proximity), not citation cosine.",
    ]

    screen_result = {
        "candidate": "G_gateway_landing", "primary_feature": "G = off-home share-weighted eigenvector gateway "
        "centrality (SLICE_A positive-PMI topic co-assignment backbone) of venue fields adopting in t0..t0+2",
        "baseline": "B5 = [log_count_W5, growth log(n[t0+4]/n[t0+1]), offhome_share_W3, entropy_W3, reach_W3]",
        "n_used_O2r": int(len(d2)), "n_used_per_group_O2r": n_per_group,
        "n_used_O1_O3": int(len(df)), "n_used_per_group_O1_O3": df["group"].value_counts().to_dict(),
        "delta_rho_O2r_m30": {k: prim[k] for k in ("base", "cand", "delta", "ci90", "ci95", "p_boot_le0",
                                                   "per_group", "n_groups_positive", "n_groups_evaluable",
                                                   "refit_boot")},
        "per_group_signs": {g: (None if not np.isfinite(prim["per_group"][g]["delta"])
                                else int(np.sign(prim["per_group"][g]["delta"]))) for g in GROUPS},
        "reliability_split_half": rel, "size_correlations": size,
        "delta_auc_O1": {k: scr["O1"][k] for k in ("base", "cand", "delta", "ci90", "ci95", "per_group",
                                                   "n_groups_positive", "n_positive", "positives_per_group",
                                                   "evaluable")},
        "delta_auc_O3": {k: scr["O3"].get(k) for k in ("base", "cand", "delta", "ci90", "ci95", "per_group",
                                                       "n_groups_positive", "n_positive", "positives_per_group",
                                                       "evaluable", "note")},
        "delta_rho_O2r_m50": {k: scr["O2r_m50"][k] for k in ("base", "cand", "delta", "ci90", "n_groups_positive")},
        "delta_rho_O2r_resid": {k: scr["O2r_resid"][k] for k in ("base", "cand", "delta", "ci90",
                                                                 "n_groups_positive")},
        "loco_supplementary": scr["LOCO_O2r_m30"],
        "survival_clauses": clauses, "survives": survives,
        "verdict": "SURVIVES" if survives else "DOES NOT SURVIVE the pre-registered S0 rule",
        "sensitivities": sens, "field_level": fl, "secondary_screens": sec,
        "confirmation_signals": conf, "status": "partial_data (credit floor); analysis complete on cached subset",
    }
    (ROOT / "screen_result.json").write_text(json.dumps(clean(screen_result), indent=1))

    # ---------------------------------------------------------------- figures
    try:
        import report
        report.make_figures(bdict, screen_result, si, nf, ROOT / "figures")
    except (ImportError, ValueError, KeyError) as e:
        logger.error(f"figures failed: {e}")

    # ---------------------------------------------------------------- method_out.json (exp_gen_sol_out)
    def examples_for(y: str, res: dict, frame: pd.DataFrame) -> list[dict]:
        ob = dict(zip(res["concepts"], res["oof_base"]))
        oc = dict(zip(res["concepts"], res["oof_cand"]))
        ex = []
        for _, row in frame.iterrows():
            if row["concept"] not in ob:
                continue
            inp = {"concept": row["concept"], "t0": int(row["t0"]), "home": row["home"], "group": row["group"],
                   **{c: (None if pd.isna(row[c]) else float(row[c])) for c in B5 + ["G", "G_missing"]}}
            ex.append({"input": json.dumps(inp), "output": str(row[y]),
                       "predict_baseline": f"{ob[row['concept']]:.6f}", "predict_our_method": f"{oc[row['concept']]:.6f}",
                       "metadata_group": row["group"], "metadata_fold": f"leave-out-{row['group']}",
                       "metadata_outcome": y, "metadata_newborn": bool(row["newborn"]),
                       "metadata_trunc": int(row["trunc"]) if not pd.isna(row["trunc"]) else None})
        return ex
    datasets = [{"dataset": "P78_dev_O2r_m30_rarefied_venue_breadth", "examples": examples_for("O2r_m30", prim, d2)},
                {"dataset": "P78_dev_O1_sustained_uptake", "examples": examples_for("O1", scr["O1"], df)},
                {"dataset": "P78_dev_O3_transience", "examples": examples_for("O3", scr["O3"], df)}]
    method_out = {"metadata": clean({
        "method_name": "G gateway-landing screen (S0) with authoritative outcome tables",
        "description": "Leave-one-home-group-out ridge/logistic of B5 vs B5+G on the P78 dev panel; 2,000 concept "
                       "bootstrap resamples; next-field relatedness-density entry test; single-indicator table.",
        "screen_result": {k: v for k, v in screen_result.items()},
        "next_field_entry": {k: ({kk: vv for kk, vv in v.items() if kk != "perm_null"} | (
            {"perm_null": {kk: vv for kk, vv in v["perm_null"].items() if kk != "values"}} if "perm_null" in v else {}))
            if isinstance(v, dict) else v for k, v in nf.items()},
        "single_indicator_table": si_rows,
        "backbone_summary": {"fields": bdict["fields"], "gateway_eig": bdict["gateway_eig"],
                             "gateway_eig_cv": bdict["gateway_eig_cv"], "n_positive_edges": bdict["n_positive_edges"],
                             "not_computed": bdict["not_computed"]},
        "p5_primary_topic_look": "not computed (shared key below the 1,000-credit floor)",
        "validations": val, "credits": oa.credits_summary(), "deviations": deviations,
        "runtime_s": round(time.time() - t_start, 1)}), "datasets": clean(datasets)}
    (ROOT / "method_out.json").write_text(json.dumps(method_out, indent=1))
    logger.info(f"done in {time.time() - t_start:.0f}s; verdict: {screen_result['verdict']}")


if __name__ == "__main__":
    main()
