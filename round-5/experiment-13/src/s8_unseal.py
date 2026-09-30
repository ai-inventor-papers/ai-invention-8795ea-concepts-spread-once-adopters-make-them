#!/usr/bin/env python3
"""S8: the SINGLE unseal and the frozen scoring of Frame N.

1. verify every frozen hash; lib/sealn.unseal() (refuses without the S7 freeze record, on a changed spec or sealed part,
   or on a second call); a crash AFTER the unseal resumes from the hashed data/outcomes_frame_n.parquet (never
   re-unseals)
2. outcomes (lib/outc.outcomes, MATCH grounding, shift 0; shift 1 for the 2015 extension): O2r_m50, O2r_m30, O1b, O1c,
   O3, O2r_resid (EXP8 frozen a/b), V_next = N(t0+3); fallback A applied mechanically from counts only
3. all pre-declared tables (lib/scoring.py), Holm, verdict code, forecasting, placebo / planted, survivorship, case
   pairs -> results/frame_n_result.json, results/survivorship.json, results/case_pairs_frame_n.json
--dryrun: synthetic outcomes (permuted EXP5 outcomes attached to Frame-N ids); no sealed file is read; output *_dryrun."""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, EXP5, INPUTS, RES, ROOT, jdump, setup_logger, sha256_file
from outc import outcomes
from scoring import (cells_for, cv_forecast, frozen_prediction, holm_table, placebo_planted, run_cells, verdict)
from sealn import MARK, SPEC, record, stages, unseal

logger = setup_logger("s8_unseal")
Y0, Y1 = 1995, 2024
NY = Y1 - Y0 + 1
FIELD_NAMES = {11: "Agri&Bio", 12: "Arts&Hum", 13: "BGM", 14: "Business", 15: "ChemEng", 16: "Chemistry", 17: "CS",
               18: "Decision", 19: "Earth", 20: "Economics", 21: "Energy", 22: "Engineering", 23: "EnvSci",
               24: "Immunol", 25: "MatSci", 26: "Math", 27: "Medicine", 28: "Neuro", 29: "Nursing", 30: "Pharma",
               31: "Physics", 32: "Psychology", 33: "SocSci", 34: "Veterinary", 35: "Dentistry", 36: "HealthProf"}


def counts_tables(ids: set, sealed: pd.DataFrame | None) -> pd.DataFrame:
    pre = pd.read_parquet(ROOT / "open/passN_pre_agg.parquet")
    pre = pre[pre.ci.isin(ids)][["ci", "year", "vfield", "n"]]
    e = pd.read_parquet(ROOT / "open/early_frame.parquet", columns=["ci", "year", "vfield"])
    e = e[e.ci.isin(ids)].groupby(["ci", "year", "vfield"]).size().rename("n").reset_index()
    parts = [pre, e]
    if sealed is not None:
        parts.append(sealed[sealed.ci.isin(ids)][["ci", "year", "vfield", "n"]])
    return pd.concat(parts, ignore_index=True).groupby(["ci", "year", "vfield"], as_index=False)["n"].sum()


def build_outcomes(fr: pd.DataFrame, agg: pd.DataFrame, spec: dict) -> pd.DataFrame:
    G = np.load(INPUTS / "passC_totals.npz")["G"].sum(1).astype(float)
    a, b = spec["O2r_resid"]["a"], spec["O2r_resid"]["b"]
    rows = []
    by = {ci: d for ci, d in agg.groupby("ci")}
    for r in fr.itertuples():
        d = by.get(r.ci)
        N = np.zeros(NY)
        V = np.zeros((NY, 27))
        if d is not None:
            np.add.at(N, d.year.to_numpy() - Y0, d.n.to_numpy(float))
            np.add.at(V, (d.year.to_numpy() - Y0, d.vfield.to_numpy()), d.n.to_numpy(float))
        shift = 1 if int(r.t0) == 2015 else 0
        o = outcomes(N, V, G, int(r.t0), Y0, shift=shift)
        rec = {"ci": int(r.ci), **o, "V_next": float(N[int(r.t0) + 3 - Y0]),
               "N_t0p2_check": float(N[int(r.t0) + 2 - Y0])}
        rec["O2r_resid"] = rec["O2r_m50"] - (a + b * r.logvol) if np.isfinite(rec["O2r_m50"]) else math.nan
        a0, a1 = int(r.t0) + 6 - shift, int(r.t0) + 8 - shift
        late = V[a0 - Y0:a1 - Y0 + 1, 1:27].sum(0)
        early = V[int(r.t0) - Y0:int(r.t0) + 3 - Y0, 1:27].sum(0)
        rec["fields_entered_by_t0p8"] = ";".join(FIELD_NAMES[k + 11] for k in range(26) if late[k] >= 2 and early[k] == 0)
        rows.append(rec)
    return pd.DataFrame(rows)


def synthetic_outcomes(fr: pd.DataFrame) -> pd.DataFrame:
    """DRY RUN ONLY: permuted EXP5 outcomes attached to Frame-N ids (no sealed data is read)."""
    rng = np.random.default_rng(0)
    f5 = pd.read_parquet(INPUTS / "features_exp5_open.parquet", columns=["ci", "O2r_m50", "O2r_resid"])
    co = pd.read_csv(EXP5 / "concept_outcomes.csv", usecols=["ci", "O1", "O3", "O2r_m30"])
    f5 = f5.merge(co, on="ci")
    i = rng.integers(0, len(f5), len(fr))
    s = f5.iloc[i].reset_index(drop=True)
    return pd.DataFrame({"ci": fr.ci.to_numpy(), "O2r_m50": s.O2r_m50.to_numpy(), "O2r_m30": s.O2r_m30.to_numpy(),
                         "O2r_resid": s.O2r_resid.to_numpy(), "O1b": s.O1.to_numpy(), "O3": s.O3.to_numpy(),
                         "O1c": rng.normal(0, 1, len(fr)),
                         "V_next": np.round(fr.N_t0p2.to_numpy() * rng.lognormal(0, 0.5, len(fr))),
                         "fields_entered_by_t0p8": ""})


def load_or_unseal(fr: pd.DataFrame, spec: dict, dry: bool) -> pd.DataFrame:
    if dry:
        return synthetic_outcomes(fr)
    rec = [r for r in stages() if r["stage"] == "S8_outcomes"]
    p = DATA / "outcomes_frame_n.parquet"
    if MARK.exists() and rec and p.exists():
        if sha256_file(p) != rec[-1]["outcomes_sha256"]:
            raise RuntimeError("outcomes_frame_n.parquet does not match its seal-log hash")
        logger.info("resuming scoring from the hashed outcomes_frame_n.parquet (unseal already done)")
        return pd.read_parquet(p)
    sealed = unseal()
    logger.info(f"UNSEALED {len(sealed)} sealed agg rows for {sealed.ci.nunique()} concepts")
    agg = counts_tables(set(fr.ci), sealed)
    oc = build_outcomes(fr, agg, spec)
    oc.to_parquet(p, index=False)
    record("S8_outcomes", outcomes_sha256=sha256_file(p), rows=len(oc))
    return oc


def survivorship(df: pd.DataFrame, B: int, seed: int) -> dict:
    co = pd.read_csv(EXP5 / "concept_outcomes.csv", usecols=["ci", "O1", "O3", "O2r_m50"])
    f5 = pd.read_parquet(INPUTS / "features_exp5_open.parquet", columns=["ci", "t0", "logvol", "O2r_m50_MATCH"])
    leg = co.merge(f5, on="ci")
    leg = leg[(leg.t0 >= 2003) & (leg.t0 <= 2014)].rename(columns={"O1": "O1b"})
    fn = df[df.t0 <= 2014]
    edges = np.quantile(fn.logvol, np.linspace(0, 1, 11))
    edges[0], edges[-1] = -np.inf, np.inf
    fn_cell = fn.t0.astype(str) + "_" + pd.cut(fn.logvol, edges, labels=False).astype(str)
    lg_cell = leg.t0.astype(str) + "_" + pd.cut(leg.logvol, edges, labels=False).astype(str)
    target = fn_cell.value_counts(normalize=True)
    out = {"n_frame_n": int(len(fn)), "n_legacy": int(len(leg)),
           "legacy_source": "EXP5 concept_outcomes (TAG grounding), t0 2003-2014; O2r_m50_MATCH from EXP10 features",
           "reweighting": "legacy reweighted to Frame N's (onset year x Frame-N logvol decile) distribution",
           "caveat": "Frame N is MATCH-grounded (verified title phrases); legacy base rates are TAG-grounded",
           "measures": {}}
    rng = np.random.default_rng(seed)
    for m_fn, m_lg in (("O2r_m50", "O2r_m50"), ("O2r_m50", "O2r_m50_MATCH"), ("O3", "O3"), ("O1b", "O1b")):
        a = fn[m_fn].to_numpy(float)
        bvals = leg[m_lg].to_numpy(float)
        cell_lg = lg_cell.to_numpy()

        def stat(ai, bi, ci_):
            okb = np.isfinite(bi)
            s = pd.DataFrame({"c": ci_[okb], "v": bi[okb]}).groupby("c").v.mean()
            w = target.reindex(s.index).fillna(0)
            rw = float((s * w).sum() / w.sum()) if w.sum() > 0 else math.nan
            return float(np.nanmean(ai)), float(np.nanmean(bi)), rw
        fa, lraw, lrw = stat(a, bvals, cell_lg)
        bs = []
        for _ in range(B):
            i = rng.integers(0, len(a), len(a))
            j = rng.integers(0, len(bvals), len(bvals))
            x1, _, x3 = stat(a[i], bvals[j], cell_lg[j])
            bs.append((x1 - x3) / x3 if x3 else math.nan)
        bs = np.asarray(bs, float)
        rel = (fa - lrw) / lrw if lrw else math.nan
        out["measures"][f"{m_fn}_vs_legacy_{m_lg}"] = {
            "frame_n_mean": fa, "legacy_raw_mean": lraw, "legacy_reweighted_mean": lrw,
            "rel_diff_vs_reweighted": rel, "rel_diff_ci": [float(np.nanpercentile(bs, 2.5)),
                                                          float(np.nanpercentile(bs, 97.5))],
            "FLAG_gt_25pct": bool(abs(rel) > 0.25), "n_frame_n_finite": int(np.isfinite(a).sum()),
            "n_legacy_finite": int(np.isfinite(bvals).sum())}
    out["mining_recall"] = json.loads((RES / "mining_recall.json").read_text())
    return out


def case_pairs(df: pd.DataFrame, prim: str) -> dict:
    import warnings

    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    d = df[np.isfinite(df.NOVCHURN_home) & np.isfinite(df[prim]) & np.isfinite(df.pred_b5)].copy()
    q = d.NOVCHURN_home.quantile([0.2, 0.8]).to_numpy()
    b5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
    Z = (d[b5] - d[b5].mean()) / d[b5].std()
    sdp = d.pred_b5.std()
    cand = []
    for g, dg in d.groupby("agroup"):
        hi, lo = dg[dg.NOVCHURN_home >= q[1]], dg[dg.NOVCHURN_home <= q[0]]
        for i in hi.index:
            for j in lo.index:
                if abs(d.at[i, "pred_b5"] - d.at[j, "pred_b5"]) <= 0.25 * sdp and abs(d.at[i, "reach"] - d.at[j, "reach"]) <= 1:
                    cand.append((float(np.linalg.norm(Z.loc[i] - Z.loc[j])), g, i, j))
    cand.sort()
    used, per_g, pairs = set(), {}, []
    for dist, g, i, j in cand:
        if len(pairs) >= 8:
            break
        if i in used or j in used or per_g.get(g, 0) >= 2:
            continue
        used |= {i, j}
        per_g[g] = per_g.get(g, 0) + 1
        pairs.append((dist, g, i, j))
    ego.set_context(rq1_context())
    e = pd.read_parquet(ROOT / "open/early_frame.parquet", columns=["ci", "year", "topics", "vfield"])

    def desc(i):
        r = d.loc[i]
        home = {int(float(x)) - 10 for x in str(r.home).split(";") if x}
        ee = e[(e.ci == r.ci) & (e.year >= r.t0 - 3) & (e.year <= r.t0 + 2)]
        works = [(int(y), tuple(int(t) for t in tp)) for y, tp, v in zip(ee.year, ee.topics, ee.vfield) if v in home]
        top = []
        try:
            cc = ego.concept_core(str(r["name"]), [a for a in str(r.aliases).split("|") if a and a != "nan"],
                                  int(r.t0), works, 0, 0, compute_btw=False)
            top = [t[0] for t in cc["_top_nb_W3"][:5]]
        except (ValueError, IndexError, ZeroDivisionError):
            pass
        return {"ci": int(r.ci), "name": r["name"], "gloss": r.get("gloss"), "t0": int(r.t0),
                "home": ";".join(FIELD_NAMES.get(int(float(x)), x) for x in str(r.home).split(";") if x),
                "early_N": float(r.early_volume), "reach": int(r.reach), "OPEN_home": float(r.OPEN_home),
                "NOVCHURN_home": float(r.NOVCHURN_home), "CHENG_consistency_home": float(r.CHENG_consistency_home),
                "top5_home_neighbour_topics_W3": top, prim: float(r[prim]), "O2r_resid": float(r.O2r_resid),
                "fields_entered_by_t0p8": r.get("fields_entered_by_t0p8", "")}
    return {"label": "illustration, not inference",
            "rule": "same group; |pred_B5 diff| <= 0.25 SD; |reach diff| <= 1; one concept in NOVCHURN_home Q5, one in "
                    "Q1; 8 closest pairs by standardized-B5 distance, <= 2 pairs per group",
            "pairs": [{"group": g, "b5_distance": dist, "high_churn": desc(i), "low_churn": desc(j),
                       "label": "illustration, not inference"} for dist, g, i, j in pairs]}


@logger.catch(reraise=True)
def main() -> None:
    dry = "--dryrun" in sys.argv
    workers = 9
    if dry and not SPEC.exists():   # pre-freeze dry run (code test only): v0 spec, no hashes, no power
        spec = json.loads((RES / "frozen_spec_v0.json").read_text()) | {"sha256": {}, "power": {}}
    else:
        spec = json.loads(SPEC.read_text())
    for p, h in spec["sha256"].items():
        if sha256_file(ROOT / p) != h:
            raise RuntimeError(f"frozen input changed: {p}")
    B = spec["bootstrap"]["B"] if not dry else 60
    SEED = spec["bootstrap"]["seed"]
    fr = pd.read_parquet(DATA / "analysis_features_frame_n.parquet")
    oc = load_or_unseal(fr, spec, dry)
    df = fr.merge(oc, on="ci", how="left")
    df["has_open_home"] = np.isfinite(df.OPEN_home)
    tag = "_dryrun" if dry else ""
    # ---------------- fallback A (counts only, before any psp)
    n_prim = int((np.isfinite(df.O2r_m50) & np.isfinite(df.OPEN_home)).sum())
    prim = "O2r_m50" if n_prim >= 800 else "O2r_m30"
    fallbackA = {"n_finite_O2r_m50_and_OPEN_home": n_prim, "threshold": 800, "primary_outcome": prim,
                 "applied": prim != "O2r_m50",
                 "n_finite_O2r_m30_and_OPEN_home": int((np.isfinite(df.O2r_m30) & np.isfinite(df.OPEN_home)).sum())}
    logger.info(f"fallback A: {fallbackA}")
    path = DATA / f"analysis_frame_n{tag}.parquet"
    df.to_parquet(path, index=False)
    t = time.time()
    cells = run_cells(str(path), cells_for(prim, B, SEED, have_type_agree=bool(df.type_agree.notna().any()
                                                                                  and df.type_agree.any())),
                      workers, log=logger.info)
    logger.info(f"cells done in {(time.time()-t)/60:.1f} min")
    res = {"dry_run": dry, "n_frame": int(len(df)), "n_by_t0": df.t0.value_counts().sort_index().to_dict(),
           "n_by_group": df.agroup.value_counts().to_dict(), "fallback_A": fallbackA, "primary_outcome": prim,
           "B": B, "seed": SEED, "resampling_unit": "concept",
           "outcome_availability": {k: int(np.isfinite(df[k]).sum()) for k in ("O2r_m50", "O2r_m30", "O2r_resid",
                                                                              "O1c", "O1b", "O3", "V_next")},
           "index_availability": {k: int(np.isfinite(df[k]).sum()) for k in
                                  ("OPEN_home", "OPEN_all", "OPEN_sizematch", "NOVCHURN_home",
                                   "CHENG_consistency_home")},
           "cells": cells}
    res["holm"] = holm_table(cells, prim)
    # EXPLORATORY (declared before the freeze): inverse-variance pooling with the independent EXP10 legacy cohort
    ex10 = json.loads((INPUTS / "cohort_result.json").read_text())["primary"]
    pooled = {}
    for r in ("R2", "R3", "R5"):
        a = cells[f"ladder|OPEN_home|{prim}|{r}"]
        b = ex10[f"OPEN_home|O2r_m50|{r}"]
        se_b = (b["ci"][1] - b["ci"][0]) / (2 * 1.96)
        if np.isfinite(a["rho"]) and np.isfinite(a["se"]) and a["se"] > 0:
            w = np.array([1 / a["se"] ** 2, 1 / se_b ** 2])
            est = float((w * np.array([a["rho"], b["rho"]])).sum() / w.sum())
            se = float(1 / math.sqrt(w.sum()))
            pooled[r] = {"frame_n": a["rho"], "frame_n_se": a["se"], "exp10_cohort": b["rho"], "exp10_se": se_b,
                         "pooled_fixed": est, "pooled_ci": [est - 1.96 * se, est + 1.96 * se],
                         "note": "EXPLORATORY; rungs are not identical (legacy level/footprint dummies in EXP10)"}
    res["exploratory_pooled_with_exp10"] = pooled
    res["verdicts"] = verdict(res, prim, spec.get("power", {}).get("OPEN_home", {}).get("power_joint_R3_R5"))
    logger.info(f"VERDICT: {res['verdicts']['verdict']} | {res['verdicts']['clauses']}")
    fc = cv_forecast(df, prim, min(1000, B), SEED)
    pred_nov = fc.pop("_pred_novchurn", {})
    res["forecast_cv"] = fc
    res["forecast_frozen_exp5"], preds = frozen_prediction(df, spec["prediction_models"], prim, min(1000, B), SEED)
    df = df.merge(preds, on="ci", how="left")
    df["pred_b5_novchurn_cv"] = df.ci.map(pred_nov)
    res["placebo_planted"] = placebo_planted(df, prim, SEED + 7, workers, n_perm=200 if not dry else 20,
                                             n_plant=100 if not dry else 9, n_boot_plant=400 if not dry else 30)
    surv = survivorship(df, min(1000, B), SEED)
    res["survivorship"] = surv
    try:
        cp = case_pairs(df, prim)
    except (KeyError, ValueError) as e:
        cp = {"error": repr(e)}
    df.to_parquet(path, index=False)
    jdump(surv, RES / f"survivorship{tag}.json")
    jdump(cp, RES / f"case_pairs_frame_n{tag}.json")
    jdump(res, RES / f"frame_n_result{tag}.json")
    if not dry:
        record("S8_scored", result_sha256=sha256_file(RES / "frame_n_result.json"),
               verdict=res["verdicts"]["verdict"])
    logger.info("S8 done")


if __name__ == "__main__":
    main()
