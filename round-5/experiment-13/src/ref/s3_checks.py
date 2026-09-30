#!/usr/bin/env python3
"""S2 checks T1-T3 and the S3 outcome-grounding decision (all outcome-blind: no cohort year >= t0+3 is read).

T1  controls: yearly TAG counts 2012..2022 (Pass C) == EXP5 agg_counts; candidates: years 2012..t0+2 only.
    Rule: >= 99% of (concept, year) cells exact and median |rel diff| < 1% -> proceed.
T2  BG[year, topic] 2012-2018 == EXP8 bg_topics.npz.
T3  base totals by (year, venue field) 1995-2022 == EXP5 year_field_totals VF.
S3  tag_rate[y] = share of base works with >= 1 legacy tag of score >= 0.3; control ratio[y] = TAG / all verified
    title-match hits of the 300 controls. TAG iff min_{2021..2024} x[y] / mean(x[2017..2019]) >= 0.90 for BOTH;
    else MATCH (validated on the EXP5 frame: Spearman(O2r_m50_MATCH, O2r_m50_TAG) >= 0.90; O2r_resid a/b refit on
    EXP5 DEV for MATCH), else the 2015-onset TAG window t0+5..t0+7 becomes primary.
Writes results/s2_checks.json, results/s3_decision.json, results/coverage_by_year.csv."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, EXP5, EXP8, RES, add_deviation, jdump, load_frame, setup_logger
from outc import outcomes

logger = setup_logger("s3_checks")


@logger.catch(reraise=True)
def main() -> None:
    cc = pd.read_csv(DATA / "cohort_candidates.csv")
    ct = pd.read_csv(DATA / "controls.csv")
    pre = pd.read_parquet(DATA / "passC_pre_agg.parquet")
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "mt", "n"])
    want = set(ct.ci) | set(cc.ci)
    ag = ag[ag.ci.isin(want) & (ag.year >= 2012)]
    t0m = cc.set_index("ci").t0
    # ---------------- T1
    def yearly(df):
        return df[df.tagstate == 1].groupby(["ci", "year"]).n.sum()
    a = yearly(pre)
    b = yearly(ag[ag.year <= 2022])
    idx = a.index.union(b.index)
    cmp_ = pd.DataFrame({"passC": a.reindex(idx, fill_value=0), "exp5": b.reindex(idx, fill_value=0)}).reset_index()
    cmp_ = cmp_[cmp_.year <= 2022]
    is_c = cmp_.ci.isin(set(cc.ci))
    cmp_ = cmp_[~is_c | (cmp_.year <= cmp_.ci.map(t0m).fillna(0) + 2)]
    cmp_["exact"] = cmp_.passC == cmp_.exp5
    cmp_["rel"] = (cmp_.passC - cmp_.exp5).abs() / cmp_.exp5.clip(lower=1)
    t1 = {}
    for nm, m in (("controls", ~cmp_.ci.isin(set(cc.ci))), ("candidates", cmp_.ci.isin(set(cc.ci)))):
        d = cmp_[m]
        t1[nm] = {"cells": int(len(d)), "exact_share": float(d.exact.mean()), "median_rel_diff": float(d.rel.median()),
                  "max_abs_diff": int((d.passC - d.exp5).abs().max()), "pass": bool(d.exact.mean() >= 0.99
                                                                                     and d.rel.median() < 0.01)}
    # also the full (vfield, tagstate, mt) cells for controls
    key = ["ci", "year", "vfield", "tagstate", "mt"]
    pc_ = pre[pre.ci.isin(set(ct.ci)) & (pre.year <= 2022)].set_index(key).n
    ec_ = ag[ag.ci.isin(set(ct.ci))].groupby(key).n.sum()
    ii = pc_.index.union(ec_.index)
    t1["controls_full_cells_exact_share"] = float((pc_.reindex(ii, fill_value=0) == ec_.reindex(ii, fill_value=0)).mean())
    # ---------------- T2
    bg = np.load(DATA / "passC_bg.npz")
    bg8 = np.load(EXP8 / "data/bg_topics.npz")
    yrs8 = bg8["years"].tolist()
    B8 = bg8["BG"][[yrs8.index(y) for y in range(2012, 2019)]]
    t2 = {"equal": bool(np.array_equal(bg["BG"], B8)), "max_abs_diff": int(np.abs(bg["BG"] - B8).max())}
    # ---------------- T3
    tot = np.load(DATA / "passC_totals.npz")
    G = tot["G"]                                   # [1995..2024, 27]
    VF5 = np.load(EXP5 / "scan/year_field_totals.npz")["VF"]
    t3 = {"equal_1995_2022": bool(np.array_equal(G[:28], VF5)), "max_abs_diff": int(np.abs(G[:28] - VF5).max())}
    checks = {"T1": t1, "T2": t2, "T3": t3}
    jdump(checks, RES / "s2_checks.json")
    logger.info(f"checks: {checks}")
    # ---------------- S3
    years = np.arange(1995, 2025)
    Gy = G.sum(1).astype(float)
    tag03 = tot["TAG03"].sum(1) / Gy
    tagany = tot["TAGANY"].sum(1) / Gy
    lab = G[:, 1:].sum(1) / Gy
    ctl = pre[pre.ci.isin(set(ct.ci))]
    tag_hits = ctl[ctl.tagstate == 1].groupby("year").n.sum()
    all_hits = ctl.groupby("year").n.sum()
    ratio = (tag_hits / all_hits).reindex(range(2012, 2025))
    cov = pd.DataFrame({"year": years, "base_works": Gy, "tag03_rate": tag03, "tagany_rate": tagany,
                        "venue_label_coverage": lab})
    cov = cov.merge(pd.DataFrame({"year": ratio.index, "control_tag_over_match": ratio.values,
                                  "control_match_hits": all_hits.reindex(range(2012, 2025)).values}), on="year",
                    how="left")
    cov.to_csv(RES / "coverage_by_year.csv", index=False)
    cy = cov.set_index("year")

    def rule(col):
        ref = cy.loc[2017:2019, col].mean()
        r = {y: float(cy.at[y, col] / ref) for y in range(2020, 2025)}
        return min(r[y] for y in range(2021, 2025)), r
    m_tag, r_tag = rule("tag03_rate")
    m_ctl, r_ctl = rule("control_tag_over_match")
    use_tag = m_tag >= 0.90 and m_ctl >= 0.90
    dec = {"tag_rate_min_ratio_2021_2024": m_tag, "tag_rate_ratios": r_tag, "control_ratio_min_2021_2024": m_ctl,
           "control_ratios": r_ctl, "OUTCOME_GROUNDING": "TAG" if use_tag else "MATCH"}
    # MATCH validation on the EXP5 frame (selection data; EXP5 outcomes <= 2022)
    fr = load_frame()
    agx = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    agx = agx[agx.ci.isin(set(fr.ci))]
    Gt = np.load(EXP5 / "scan/year_field_totals.npz")["G"].astype(float)
    NYx = 28
    ci_ = agx.ci.to_numpy(); yy = agx.year.to_numpy() - 1995; vf = agx.vfield.to_numpy(); n = agx.n.to_numpy(float)
    ts = agx.tagstate.to_numpy()
    pos = pd.Series(np.arange(len(fr)), index=fr.ci.to_numpy())
    f = pos.loc[ci_].to_numpy()
    res = {}
    for nm, m in (("TAG", ts == 1), ("MATCH", np.ones(len(ts), bool))):
        N = np.bincount(f[m] * NYx + yy[m], weights=n[m], minlength=len(fr) * NYx).reshape(len(fr), NYx)
        V = np.bincount((f[m] * NYx + yy[m]) * 27 + vf[m], weights=n[m], minlength=len(fr) * NYx * 27).reshape(
            len(fr), NYx, 27)
        res[nm] = np.array([outcomes(N[i], V[i], Gt, int(t0), 1995)["O2r_m50"] for i, t0 in enumerate(fr.t0)])
    ok = np.isfinite(res["TAG"]) & np.isfinite(res["MATCH"])
    rho = float(stats.spearmanr(res["TAG"][ok], res["MATCH"][ok])[0])
    basic = pd.read_csv(EXP5 / "concept_features_basic.csv", usecols=["ci", "logvol"]).set_index("ci").logvol
    lv = fr.ci.map(basic).to_numpy(float)
    dev = (fr.split == "DEV").to_numpy() & np.isfinite(res["MATCH"]) & np.isfinite(lv)
    a, b = np.linalg.lstsq(np.c_[np.ones(dev.sum()), lv[dev]], res["MATCH"][dev], rcond=None)[0]
    dec["match_validation"] = {"spearman_O2r_m50_match_vs_tag": rho, "n": int(ok.sum()),
                               "n_finite_TAG": int(np.isfinite(res["TAG"]).sum()),
                               "n_finite_MATCH": int(np.isfinite(res["MATCH"]).sum()),
                               "pass": rho >= 0.90, "O2r_resid_match_fit_dev": {"a": float(a), "b": float(b),
                                                                                  "n": int(dev.sum())}}
    pd.DataFrame({"ci": fr.ci, "O2r_m50_TAG": res["TAG"], "O2r_m50_MATCH": res["MATCH"]}).to_parquet(
        DATA / "exp5_o2r_match_vs_tag.parquet", index=False)
    if use_tag:
        dec["PRIMARY"] = "TAG t0+6..t0+8"
    elif rho >= 0.90:
        dec["PRIMARY"] = "MATCH t0+6..t0+8"
    else:
        dec["PRIMARY"] = "TAG 2015-onset t0+5..t0+7 (<= 2022); full cohort secondary"
    dec["venue_label_coverage_by_year"] = {int(y): float(v) for y, v in zip(years, lab) if y >= 2012}
    jdump(dec, RES / "s3_decision.json")
    add_deviation("S3_outcome_grounding", f"outcome-blind S3 rule -> {dec['OUTCOME_GROUNDING']} "
                                          f"(tag-rate min ratio {m_tag:.3f}, control ratio {m_ctl:.3f}; MATCH "
                                          f"validation rho {rho:.3f}); primary = {dec['PRIMARY']}")
    logger.info(f"S3: {dec}")


if __name__ == "__main__":
    main()
