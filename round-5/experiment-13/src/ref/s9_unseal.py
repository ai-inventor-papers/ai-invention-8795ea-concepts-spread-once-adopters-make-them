#!/usr/bin/env python3
"""S9: the SINGLE unseal and the frozen scoring of the fresh 2015-2016(-2017) cohort.

1. lib/seal2.unseal() (refuses without the matching frozen-spec hash, if the sealed parts changed, or on a 2nd call)
2. cohort outcomes (lib/outc.outcomes, frozen windows; grounding from the frozen S3 decision) -> data/outcomes_cohort.parquet
   (sha256 hash-chained into logs/seal.log)
3. frozen ladder, groups (DL), within type, components, RETENTION_RATIO_early, paired build contrasts, Holm, VERDICT
4. secondary (frozen, no refit): n_authors_early, CONTACT_REACH, frozen B5 vs B5+OPEN_home predictions
5. placebos: 200 within-group outcome permutations; planted psp = 0.10 recovery
Writes results/cohort_result.json."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import rankdata

from common import DATA, EXP5, RES, ROOT, jdump, setup_logger, sha256_file
from ladder import (BUILDS, COMPONENTS, POOL_GROUPS, RUNGS, holm, open_score, paired_diff, per_group, psp_df,
                    rung_design, strip)
from outc import outcomes
from rq1stats import psp_point
from seal2 import SPEC, record, unseal

logger = setup_logger("s9_unseal")
Y0, Y1 = 1995, 2024
NY = Y1 - Y0 + 1


def build_outcomes(coh: pd.DataFrame, spec: dict, sealed: pd.DataFrame) -> pd.DataFrame:
    pre = pd.read_parquet(DATA / "passC_pre_agg.parquet")
    pre = pre[pre.ci.isin(set(coh.ci))]
    agg = pd.concat([pre, sealed[sealed.ci.isin(set(coh.ci))]], ignore_index=True)
    G = np.load(DATA / "passC_totals.npz")["G"].sum(1).astype(float)
    a, b = spec["O2r_resid"]["a"], spec["O2r_resid"]["b"]
    use_match = spec["outcome_grounding"] == "MATCH"
    rows = []
    for r in coh.itertuples():
        d = agg[agg.ci == r.ci]
        rec = {"ci": int(r.ci)}
        for nm, m in (("TAG", d.tagstate == 1), ("MATCH", np.ones(len(d), bool))):
            dd = d[m]
            N = np.zeros(NY)
            V = np.zeros((NY, 27))
            np.add.at(N, dd.year.to_numpy() - Y0, dd.n.to_numpy(float))
            np.add.at(V, (dd.year.to_numpy() - Y0, dd.vfield.to_numpy()), dd.n.to_numpy(float))
            shift = 1 if r.t0 == 2017 else 0
            o = outcomes(N, V, G, int(r.t0), Y0, shift=shift)
            rec.update({f"{k}_{nm}": v for k, v in o.items()})
            if r.t0 == 2015:   # <= 2022 window for 2015 onsets (t0+5..t0+7), always reported
                o22 = outcomes(N, V, G, int(r.t0), Y0, shift=1)
                rec.update({f"{k}_{nm}_le2022": v for k, v in o22.items()})
        g = "MATCH" if use_match else "TAG"
        for k in ("O1b", "O3", "O2r_m50", "O2r_m30", "O1c", "N_outcome"):
            rec[k] = rec[f"{k}_{g}"]
        rec["O2r_resid"] = rec["O2r_m50"] - (a + b * r.logvol) if np.isfinite(rec["O2r_m50"]) else math.nan
        rec["O2r_m50_le2022_TAG"] = rec.get("O2r_m50_TAG_le2022", math.nan)
        rec["O2r_resid_le2022_TAG"] = (rec["O2r_m50_le2022_TAG"] - (2.7410366547641205 + 0.3966308230599589 * r.logvol)
                                       if np.isfinite(rec["O2r_m50_le2022_TAG"]) else math.nan)
        rows.append(rec)
    return pd.DataFrame(rows)


def verdict(res: dict) -> dict:
    L = res["primary"]
    h2, h3 = L["OPEN_home|O2r_m50|R2"], L["OPEN_home|O2r_m50|R3"]
    c = {}
    c["1_open_home_R2_R3_ci_gt0"] = bool(h2["rho"] > 0 and h2["ci"][0] > 0 and h3["rho"] > 0 and h3["ci"][0] > 0)
    c["2_o2r_resid_same_sign_R2"] = bool(L["OPEN_home|O2r_resid|R2"]["rho"] > 0)
    c["3_positive_in_ge4_of_5_groups_R2"] = bool(res["groups"]["OPEN_home|O2r_m50|R2"]["n_positive_of_5"] >= 4)
    wm, wo = res["within_type"]["OPEN_home|method|R3"]["rho"], res["within_type"]["OPEN_home|object|R3"]["rho"]
    c["4_within_method_and_object_gt0"] = bool(np.isfinite(wm) and np.isfinite(wo) and wm > 0 and wo > 0)
    c["5_retention_ratio_lt0_R0"] = bool(res["retention"]["RETENTION_RATIO_early|O2r_m50|R0"]["rho"] < 0)
    disc = bool(h2["ci"][0] <= 0 <= h2["ci"][1])
    if all(c.values()):
        v = "CONFIRMED"
    elif disc:
        v = "DISCONFIRMED"
    else:
        v = "PARTIAL"
    r1 = L["OPEN_home|O2r_m50|R1"]
    a_all = L["OPEN_all|O2r_m50|R2"]
    readings = {
        "a_type_absorbs_OPEN": bool(r1["ci"][0] > 0 and h2["ci"][0] <= 0),
        "b_mechanical": bool(h2["ci"][0] <= 0 and a_all["ci"][0] > 0),
    }
    if readings["b_mechanical"]:
        s2 = L["OPEN_sizematch|O2r_m50|R2"]
        readings["b_sizematch_reading"] = ("paper count (SIZEMATCH also null)" if s2["ci"][0] <= 0
                                           else "home restriction (SIZEMATCH still positive)")
    return {"verdict": v, "clauses": c, "failing_clauses": [k for k, x in c.items() if not x],
            "named_readings": readings}


def synthetic_sealed(coh: pd.DataFrame) -> pd.DataFrame:
    """DRY RUN ONLY: random outcome-window counts (no real sealed data is read) to exercise every code path."""
    rng = np.random.default_rng(0)
    rows = []
    for r in coh.itertuples():
        for y in range(int(r.t0) + 3, 2025):
            for vf in rng.choice(np.arange(1, 27), size=4, replace=False):
                rows.append((r.ci, y, vf, int(rng.choice([1, 1, 2])), 0, int(rng.integers(0, 12))))
    return pd.DataFrame(rows, columns=["ci", "year", "vfield", "tagstate", "mt", "n"])


def load_or_unseal(coh: pd.DataFrame, spec: dict, dry: bool) -> pd.DataFrame:
    """Single unseal; a scoring crash AFTER the unseal resumes from the hashed outcomes file (never re-unseals)."""
    from seal2 import MARK, _lines
    if dry:
        return build_outcomes(coh, spec, synthetic_sealed(coh))
    rec = [json.loads(l) for l in _lines() if json.loads(l)["stage"] == "S9_outcomes"]
    if MARK.exists() and rec and (DATA / "outcomes_cohort.parquet").exists():
        if sha256_file(DATA / "outcomes_cohort.parquet") != rec[-1]["outcomes_cohort_sha256"]:
            raise RuntimeError("outcomes_cohort.parquet does not match its seal-log hash")
        logger.info("resuming scoring from the hashed outcomes_cohort.parquet (unseal already done)")
        return pd.read_parquet(DATA / "outcomes_cohort.parquet")
    sealed = unseal()
    logger.info(f"UNSEALED {len(sealed)} sealed agg rows for {sealed.ci.nunique()} concepts")
    oc = build_outcomes(coh, spec, sealed)
    oc.to_parquet(DATA / "outcomes_cohort.parquet", index=False)
    record("S9_outcomes", outcomes_cohort_sha256=sha256_file(DATA / "outcomes_cohort.parquet"), rows=len(oc))
    return oc


@logger.catch(reraise=True)
def main() -> None:
    dry = "--dryrun" in sys.argv
    spec = json.loads(SPEC.read_text())
    for p, h in spec["sha256"].items():
        if sha256_file(ROOT / p) != h:
            raise RuntimeError(f"frozen input changed: {p}")
    B = spec["bootstrap"]["B"] if not dry else 30
    SEED = spec["bootstrap"]["seed"]
    coh = pd.read_parquet(DATA / "features_cohort.parquet")
    oc = load_or_unseal(coh, spec, dry)
    df = coh.merge(oc, on="ci", how="left")
    tag = "_dryrun" if dry else ""
    df.to_parquet(DATA / f"analysis_cohort{tag}.parquet", index=False)
    res: dict = {"n_cohort": int(len(df)), "n_by_t0": df.t0.value_counts().sort_index().to_dict(),
                 "outcome_availability": {k: int(np.isfinite(df[k]).sum()) for k in ("O2r_m50", "O2r_resid", "O1c")},
                 "resampling_unit": "concept", "B": B, "grounding": spec["outcome_grounding"],
                 "primary_definition": spec["primary"], "primary": {}, "groups": {}, "within_type": {},
                 "components": {}, "retention": {}, "contrasts": {}, "holm": {}, "secondary": {}, "sensitivity": {},
                 "placebos": {}}
    for b in BUILDS:
        for y in ("O2r_m50", "O2r_resid"):
            for r in RUNGS:
                res["primary"][f"OPEN_{b}|{y}|{r}"] = strip(psp_df(df, f"OPEN_{b}", y, r, B, SEED))
        logger.info(f"{b}: R2 O2r_m50 {res['primary'][f'OPEN_{b}|O2r_m50|R2']['rho']:.3f} "
                    f"CI {res['primary'][f'OPEN_{b}|O2r_m50|R2']['ci']}")
    for b in BUILDS:
        for r in ("R2", "R3"):
            for y in ("O2r_m50", "O2r_resid"):
                res["groups"][f"OPEN_{b}|{y}|{r}"] = strip(per_group(df, f"OPEN_{b}", y, r, min(1000, B), SEED))
    for t in ("method", "object", "property", "topic"):
        d = df[(df.type == t) & (df.type_agree if t in ("method", "object") else True)]   # M1 = M2 (gate fallback)
        for b in BUILDS:
            res["within_type"][f"OPEN_{b}|{t}|R3"] = strip(psp_df(d, f"OPEN_{b}", "O2r_m50", "R3", B, SEED,
                                                                  drop_type=True))
    for b in BUILDS:
        for k in COMPONENTS:
            for r in ("R2", "R3"):
                res["components"][f"{k}__{b}|O2r_m50|{r}"] = strip(psp_df(df, f"{k}__{b}", "O2r_m50", r, min(1000, B), SEED))
    for y in ("O2r_m50", "O2r_resid"):
        for r in ("R0", "R2", "R3"):
            res["retention"][f"RETENTION_RATIO_early|{y}|{r}"] = strip(
                psp_df(df, "RETENTION_RATIO_early", y, r, B, SEED, direction=-1))
    res["contrasts"]["all_minus_home|R3"] = paired_diff(df, "OPEN_all", "OPEN_home", "O2r_m50", "R3", B, SEED)
    res["contrasts"]["sizematch_minus_home|R3"] = paired_diff(df, "OPEN_sizematch", "OPEN_home", "O2r_m50", "R3", B,
                                                              SEED)
    # Holm (8 tests, one-sided bootstrap p in the frozen direction, R2)
    fam = spec["holm_family"]
    ps = []
    for key in fam:
        x, y = key.split("|")
        if x == "RETENTION_RATIO_early":
            ps.append(res["retention"][f"{x}|{y}|R2"]["p_one"])
        else:
            ps.append(res["primary"][f"{x}|{y}|R2"]["p_one"])
    res["holm"] = {k: {"p_one": p, "p_holm": ph} for k, p, ph in zip(fam, ps, holm(ps))}
    res["verdict"] = verdict(res)
    logger.info(f"VERDICT: {res['verdict']}")
    # ---------------- secondary (frozen, no refit)
    for y in ("O3", "O1b", "O1c"):
        res["secondary"][f"n_authors_early|{y}|R0"] = strip(psp_df(df, "n_authors_early", y, "R0", min(1000, B), SEED))
    for y in ("O2r_m50", "O2r_resid"):
        res["secondary"][f"CONTACT_REACH|{y}|R0"] = strip(psp_df(df, "CONTACT_REACH", y, "R0", min(1000, B), SEED))
        res["secondary"][f"CONTACT_REACH|{y}|R0|excl_intersection_born"] = strip(
            psp_df(df[df.intersection_born == 0], "CONTACT_REACH", y, "R0", min(1000, B), SEED))
    pm = spec["prediction_models"]
    mu, sd = pd.Series(pm["B5"]["mu"]), pd.Series(pm["B5"]["sd"])
    Z = ((df[list(mu.index)] - mu) / sd).to_numpy(float)
    X0 = np.c_[np.ones(len(df)), Z]
    df["pred_b5"] = X0 @ np.asarray(pm["B5"]["coef"])
    df["pred_b5_open"] = np.c_[X0, df.OPEN_home.to_numpy(float)] @ np.asarray(pm["B5_plus_OPEN_home"]["coef"])
    ok = np.isfinite(df.O2r_m50) & np.isfinite(df.pred_b5) & np.isfinite(df.pred_b5_open)
    y_, p0, p1 = df.O2r_m50[ok].to_numpy(), df.pred_b5[ok].to_numpy(), df.pred_b5_open[ok].to_numpy()
    rng = np.random.default_rng(SEED)
    bs = []
    for _ in range(B):
        i = rng.integers(0, len(y_), len(y_))
        bs.append(stats.spearmanr(p1[i], y_[i])[0] - stats.spearmanr(p0[i], y_[i])[0])
    res["secondary"]["frozen_prediction_O2r_m50"] = {
        "n": int(ok.sum()), "spearman_B5": float(stats.spearmanr(p0, y_)[0]),
        "spearman_B5_plus_OPEN_home": float(stats.spearmanr(p1, y_)[0]),
        "diff": float(stats.spearmanr(p1, y_)[0] - stats.spearmanr(p0, y_)[0]),
        "diff_ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "resampling_unit": "concept"}
    df[["ci", "pred_b5", "pred_b5_open"]].to_parquet(DATA / f"cohort_predictions{tag}.parquet", index=False)
    # ---------------- sensitivities (declared)
    common = df[np.isfinite(df.OPEN_home)]
    res["sensitivity"]["OPEN_all_on_home_sample|O2r_m50|R2"] = strip(psp_df(common, "OPEN_all", "O2r_m50", "R2", 1000,
                                                                            SEED))
    d15 = df[df.t0 == 2015]
    for b in BUILDS:
        res["sensitivity"][f"OPEN_{b}|O2r_m50_le2022_TAG|2015onsets|R2"] = strip(
            psp_df(d15, f"OPEN_{b}", "O2r_m50_le2022_TAG", "R2", min(1000, B), SEED))
        res["sensitivity"][f"OPEN_{b}|O2r_m50_TAG|R2"] = strip(psp_df(df, f"OPEN_{b}", "O2r_m50_TAG", "R2", min(1000, B), SEED))
        res["sensitivity"][f"OPEN_{b}|O2r_m50_MATCH|R2"] = strip(psp_df(df, f"OPEN_{b}", "O2r_m50_MATCH", "R2", 1000,
                                                                        SEED))
    for mh in (5, 20):
        o, _ = open_score(df, "home", spec["open_constants"]["home"], min_home=mh)
        res["sensitivity"][f"OPEN_home_min{mh}|O2r_m50|R2"] = strip(psp_df(df.assign(OH=o), "OH", "O2r_m50", "R2",
                                                                            1000, SEED))
    if (df.t0 == 2017).any():
        res["sensitivity"]["OPEN_home|O2r_m50|R2|2015_2016_only"] = strip(
            psp_df(df[df.t0 <= 2016], "OPEN_home", "O2r_m50", "R2", min(1000, B), SEED))
    # included vs excluded (finite OPEN_home) B5 profile (F7)
    inc = np.isfinite(df.OPEN_home)
    res["sensitivity"]["open_home_finite_share"] = float(inc.mean())
    res["sensitivity"]["b5_profile_included_vs_excluded"] = {
        c: [float(df.loc[inc, c].mean()), float(df.loc[~inc, c].mean())] for c in
        ["logvol", "growth_c", "offhome_share", "entropy", "reach", "O2r_m50"]}
    # ---------------- placebos
    Bc, Cc = rung_design(df, "R2")
    x = df.OPEN_home.to_numpy(float)
    y = df.O2r_m50.to_numpy(float)
    okp = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(Bc.to_numpy(float)), 1)
    xs, ys, Bs, Cs, gs = x[okp], y[okp], Bc.to_numpy(float)[okp], Cc.to_numpy(float)[okp], df.agroup.to_numpy()[okp]
    rngp = np.random.default_rng(SEED + 7)
    perm = []
    for _ in range(200 if not dry else 5):
        yp = ys.copy()
        for g in np.unique(gs):
            m = gs == g
            yp[m] = rngp.permutation(yp[m])
        perm.append(psp_point(xs, yp, Bs, Cs))
    perm = np.asarray(perm)
    res["placebos"]["within_group_permutation"] = {"n_perm": 200, "mean": float(perm.mean()),
                                                   "q95_abs": float(np.percentile(np.abs(perm), 95)),
                                                   "share_abs_lt_0.05": float((np.abs(perm) < 0.05).mean()),
                                                   "observed_R2": res["primary"]["OPEN_home|O2r_m50|R2"]["rho"]}
    # planted: y' = z(rank(permuted y)) + delta * z(OPEN_home residual) with delta giving psp ~ 0.10
    yp = ys.copy()
    for g in np.unique(gs):
        m = gs == g
        yp[m] = rngp.permutation(yp[m])
    Z = np.c_[np.ones(len(xs)), rankdata(Bs, axis=0), Cs]
    rx = rankdata(xs) - Z @ np.linalg.lstsq(Z, rankdata(xs), rcond=None)[0]
    zr = (rankdata(yp) - rankdata(yp).mean()) / rankdata(yp).std()
    delta = 0.10 / math.sqrt(1 - 0.10 ** 2)
    yplant = zr + delta * rx / rx.std()
    pl = psp_df(pd.DataFrame({"x": xs, "y": yplant}).join(df[okp].reset_index(drop=True)[
        [c for c in df.columns if c not in ("x", "y")]]), "x", "y", "R2", min(1000, B), SEED)
    res["placebos"]["planted_0.10"] = strip(pl)
    res["placebos"]["planted_0.10"]["recovered_ci_gt0"] = bool(pl["ci"][0] > 0)
    jdump(res, RES / f"cohort_result{tag}.json")
    if not dry:
        record("S9_scored", cohort_result_sha256=sha256_file(RES / "cohort_result.json"),
               verdict=res["verdict"]["verdict"])
    logger.info("S9 done")


if __name__ == "__main__":
    main()
