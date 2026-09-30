#!/usr/bin/env python3
"""S8: selection on the EXP5 frame (selection data only), cohort feature table, power + extension decision, FREEZE.

  (a) winsor bounds + z constants per build on the 12,499 EXP5 concepts -> OPEN_all / OPEN_home / OPEN_sizematch
  (b) selection-data ladder (EXP8 EXP5-frame outcomes): every build x {O2r_m50, O2r_resid} x R0..R5; components alone;
      per group (DL) at R2/R3; within type; RETENTION_RATIO_early; HOME min-paper sensitivity 5 / 20
  (c) coupling diagnostic: Spearman of each OPEN build with early off-home share and log early volume
  (d) power for the cohort (true effect = half the EXP5 estimate) and the declared 2017 extension rule
  (e) cohort feature table (frozen constants applied) + SMD check, frozen B5 / B5+OPEN_home prediction models
  (f) freeze: results/frozen_spec.json (hash-chained into logs/seal.log), pre-unseal checklist
Usage: python s8_select.py [--nboot 500] [--no-freeze]"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, EXP8, RES, ROOT, add_deviation, jdump, load_frame, setup_logger, sha256_file
from ladder import (ANALYSIS_GROUP, B5, BUILDS, COMPONENTS, POOL_GROUPS, RUNGS, fit_open_constants, open_score,
                    per_group, psp_df, rung_design, strip)
from rq1stats import psp_point

logger = setup_logger("s8_select")
SEED = 20260929
OUTC = ["O2r_m50", "O2r_resid"]


def load_types() -> pd.DataFrame:
    t = pd.read_csv(DATA / "concept_types.csv")
    t["type_agree"] = t.type_agree.fillna(False).astype(bool)
    return t[["ci", "frame", "type", "generic", "type_agree"]]


def exp5_table() -> pd.DataFrame:
    fr = load_frame()[["ci", "concept_id", "name", "t0", "group", "split", "home", "intersect40"]]
    eg = pd.read_parquet(DATA / "ego_open_exp5.parquet")
    cv = pd.read_parquet(DATA / "covariates_exp5.parquet")
    ty = load_types()
    ty = ty[ty.frame == "exp5"].drop(columns="frame")
    oc = pd.read_parquet(EXP8 / "data/outcomes.parquet", columns=["ci", "O1c", "O1b", "O2r_m50", "O2r_resid", "O3"])
    df = fr.merge(eg, on="ci", how="left").merge(cv, on="ci", how="left").merge(ty, on="ci", how="left") \
        .merge(oc, on="ci", how="left")
    mv = DATA / "exp5_o2r_match_vs_tag.parquet"
    if mv.exists():
        df = df.merge(pd.read_parquet(mv)[["ci", "O2r_m50_MATCH"]], on="ci", how="left")
    df["agroup"] = df.group.map(ANALYSIS_GROUP)
    df["home_coverage_early"] = df.n_home_early / df.n_all_early.replace(0, np.nan)
    df["generic"] = df.generic.fillna(0)
    df["type_agree"] = df.type_agree.fillna(False).astype(bool)
    return df


def selection(df: pd.DataFrame, nboot: int) -> dict:
    out: dict = {"ladder": {}, "components": {}, "groups": {}, "within_type": {}, "retention": {}, "min_home": {}}
    for b in BUILDS:
        for y in OUTC:
            for r in RUNGS:
                out["ladder"][f"OPEN_{b}|{y}|{r}"] = strip(psp_df(df, f"OPEN_{b}", y, r, nboot, SEED))
        logger.info(f"selection ladder {b} done: R2 O2r_m50 = {out['ladder'][f'OPEN_{b}|O2r_m50|R2']['rho']:.3f}")
    for b in BUILDS:
        for k in COMPONENTS:
            for r in ("R0", "R2", "R3"):
                out["components"][f"{k}__{b}|O2r_m50|{r}"] = strip(psp_df(df, f"{k}__{b}", "O2r_m50", r, nboot // 2, SEED))
    for b in BUILDS:
        for r in ("R2", "R3"):
            out["groups"][f"OPEN_{b}|O2r_m50|{r}"] = strip(per_group(df, f"OPEN_{b}", "O2r_m50", r, nboot // 2, SEED))
    for t in ("method", "object", "property", "topic"):
        d = df[(df.type == t) & (df.type_agree if t in ("method", "object") else True)]   # M1 = M2 (gate fallback)
        for b in BUILDS:
            out["within_type"][f"OPEN_{b}|{t}|R3"] = strip(psp_df(d, f"OPEN_{b}", "O2r_m50", "R3", nboot // 2, SEED,
                                                                  drop_type=True))
    for y in OUTC:
        for r in ("R0", "R2", "R3"):
            out["retention"][f"RETENTION_RATIO_early|{y}|{r}"] = strip(
                psp_df(df, "RETENTION_RATIO_early", y, r, nboot, SEED, direction=-1))
    for mh in (5, 20):
        o, _ = open_score(df, "home", CONST["home"], min_home=mh)
        d = df.assign(OPEN_home_mh=o)
        out["min_home"][f"OPEN_home_min{mh}|O2r_m50|R2"] = strip(psp_df(d, "OPEN_home_mh", "O2r_m50", "R2", nboot // 2,
                                                                         SEED))
    return out


def power_calc(df: pd.DataFrame, cohort: pd.DataFrame, ycol: str, n_draw: int = 1000) -> dict:
    """P(95% CI > 0 at R2) for pooled OPEN_home psp at the cohort's expected analysis n and group mix, with the true
    effect = half the EXP5 selection estimate (subsample distribution shifted by -est/2; Fisher-z SE)."""
    Bc, Cc = rung_design(df, "R2")
    x, y = df.OPEN_home.to_numpy(float), df[ycol].to_numpy(float)
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(Bc.to_numpy(float)), 1)
    d = df[ok].reset_index(drop=True)
    B, C = Bc.to_numpy(float)[ok], Cc.to_numpy(float)[ok]
    est = psp_point(d.OPEN_home.to_numpy(float), d[ycol].to_numpy(float), B, C)
    # expected analysis n: cohort concepts with finite OPEN_home x EXP5 availability of the outcome among those
    avail = float(np.isfinite(df.loc[np.isfinite(x), ycol]).mean())
    n_open = int(np.isfinite(cohort.OPEN_home).sum())
    n_eff = int(round(n_open * avail))
    mix = cohort.loc[np.isfinite(cohort.OPEN_home), "agroup"].value_counts(normalize=True)
    rng = np.random.default_rng(SEED)
    k = B.shape[1] + C.shape[1]
    se_z = 1 / math.sqrt(max(n_eff - k - 3, 1))
    ests = []
    idx_by = {g: np.nonzero(d.agroup.to_numpy() == g)[0] for g in mix.index}
    for _ in range(n_draw):
        take = np.concatenate([rng.choice(idx_by[g], size=max(1, int(round(n_eff * p))), replace=True)
                               for g, p in mix.items() if len(idx_by[g])])
        Ci = C[take]
        keep = Ci.std(0) > 0
        ests.append(psp_point(d.OPEN_home.to_numpy(float)[take], d[ycol].to_numpy(float)[take], B[take], Ci[:, keep]))
    ests = np.asarray(ests)
    shifted = ests - est / 2
    power = float(np.mean(np.arctanh(np.clip(shifted, -0.999, 0.999)) - 1.96 * se_z > 0))
    sd_sub = float(np.std(ests))
    by_type = {}
    for t in ("method", "object"):
        nt = int(round(n_eff * float((cohort.loc[np.isfinite(cohort.OPEN_home), "type"] == t).mean())))
        by_type[t] = {"n_expected": nt, "MDE_2.8SE": 2.8 / math.sqrt(max(nt - k - 3, 1))}
    return {"exp5_estimate_R2": est, "assumed_true_effect": est / 2, "n_expected": n_eff, "n_open_finite": n_open,
            "outcome_availability_exp5": avail, "group_mix": mix.to_dict(), "power_ci_gt0": power,
            "MDE_2.8SE_analytic": 2.8 * se_z, "MDE_2.8SE_subsample_sd": 2.8 * sd_sub, "within_type": by_type,
            "n_draws": n_draw}


def cohort_table(extension: bool) -> pd.DataFrame:
    g = pd.read_csv(DATA / "cohort_candidates_gated.csv")
    g = g[g.pass_gate & ((g.t0 <= 2016) | extension)].copy()
    eg = pd.read_parquet(DATA / "ego_open_cohort.parquet")
    cv = pd.read_parquet(DATA / "covariates_cohort.parquet")
    ty = load_types()
    ty = ty[ty.frame == "cohort"].drop(columns="frame")
    g = g.drop(columns=["level", "label_coverage_early"])      # recomputed identically in covariates_cohort
    df = g.rename(columns={"openalex_id": "concept_id", "label": "name"}).merge(eg, on="ci", how="left") \
        .merge(cv.drop(columns=["newborn"]), on="ci", how="left").merge(ty, on="ci", how="left")
    assert not [c for c in df.columns if c.endswith("_x") or c.endswith("_y")], "column clash in cohort table"
    df["agroup"] = df.group.map(ANALYSIS_GROUP)
    df["home_coverage_early"] = df.n_home_early / df.n_all_early.replace(0, np.nan)
    df["generic"] = df.generic.fillna(0)
    df["type_agree"] = df.type_agree.fillna(False).astype(bool)
    df["window_flag"] = (df.t0 == 2017).astype(int)
    df["newborn"] = df.newborn.astype(int)
    for b in BUILDS:
        df[f"OPEN_{b}"], _ = open_score(df, b, CONST[b])
    return df


def smd(a: pd.Series, b: pd.Series) -> float:
    a, b = a.dropna().astype(float), b.dropna().astype(float)
    s = math.sqrt((a.var() + b.var()) / 2)
    return float((a.mean() - b.mean()) / s) if s > 0 else float("nan")


CONST: dict = {}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nboot", type=int, default=500)
    ap.add_argument("--no-freeze", action="store_true")
    a = ap.parse_args()
    s3 = json.loads((RES / "s3_decision.json").read_text())
    grounding = s3["OUTCOME_GROUNDING"]
    primary = s3["PRIMARY"]
    df = exp5_table()
    for b in BUILDS:
        CONST[b] = fit_open_constants(df, b)
        df[f"OPEN_{b}"], _ = open_score(df, b, CONST[b])
    logger.info(f"EXP5 OPEN finite: " + ", ".join(f"{b} {np.isfinite(df[f'OPEN_{b}']).mean():.3f}" for b in BUILDS))
    # EXP8 ALL-build reproduction on the full frame (U2 extension)
    e8 = pd.read_parquet(EXP8 / "data/ego_features.parquet", columns=["ci"] + COMPONENTS)
    m = df[["ci"] + [f"{k}__all" for k in COMPONENTS]].merge(e8, on="ci")
    repro = {k: float(np.nanmax(np.abs(m[f"{k}__all"] - m[k]))) for k in COMPONENTS}
    # outcome used for power: the grounding S3 chose (MATCH -> EXP5 MATCH O2r_m50)
    ycol_power = "O2r_m50_MATCH" if primary.startswith("MATCH") else "O2r_m50"
    sel = selection(df, a.nboot)
    sel["coupling"] = {f"OPEN_{b}": {"rho_offhome_share": float(stats.spearmanr(df[f"OPEN_{b}"], df.offhome_share,
                                                                                  nan_policy="omit")[0]),
                                     "rho_logvol": float(stats.spearmanr(df[f"OPEN_{b}"], df.logvol,
                                                                         nan_policy="omit")[0])} for b in BUILDS}
    sel["sign_check_R0_all_build"] = {
        k: {"psp": sel["components"][f"{k}__all|O2r_m50|R0"]["rho"],
            "expected_sign": {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1,
                              "ego_density_W3": -1, "edge_persistence": -1}[k]} for k in COMPONENTS}
    for k, v in sel["sign_check_R0_all_build"].items():
        v["match"] = bool(np.sign(v["psp"]) == v["expected_sign"])
    sel["exp8_all_build_reproduction_max_abs_diff"] = repro
    sel["n_exp5"] = int(len(df))
    sel["open_finite_share"] = {b: float(np.isfinite(df[f"OPEN_{b}"]).mean()) for b in BUILDS}
    # ---- cohort (outcome-free) + power / extension
    coh = cohort_table(extension=False)
    pw = power_calc(df, coh, ycol_power)
    n_gate = int(len(coh))
    extension = bool(n_gate < 800 or pw["power_ci_gt0"] < 0.80)
    if primary.startswith("TAG 2015-onset"):
        extension = False
        add_deviation("extension_not_applicable", "S3 fallback primary (2015 onsets, <= 2022) makes the 2017 extension "
                                                  "impossible (no <= 2022 outcome window)")
    coh = cohort_table(extension)
    pw_ext = power_calc(df, coh, ycol_power) if extension else None
    sel["power"] = {"base_2015_2016": pw, "with_2017": pw_ext, "n_gate_2015_2016": n_gate, "extension": extension,
                    "rule": "extend iff n_gate < 800 OR power < 0.80 (declared S0)"}
    logger.info(f"power {pw['power_ci_gt0']:.3f} (n_exp {pw['n_expected']}, MDE {pw['MDE_2.8SE_analytic']:.3f}); "
                f"n_gate {n_gate}; extension={extension}")
    # SMD check cohort vs EXP5
    cols = B5 + ["CONTACT_REACH", "RETENTION_RATIO_early", "n_authors_early", "OPEN_home", "OPEN_all",
                 "OPEN_sizematch", "fp_logN", "fp_nfields", "label_coverage_early", "home_coverage_early"] + \
        [f"{k}__home" for k in COMPONENTS]
    sel["smd_cohort_vs_exp5"] = {c: smd(coh[c], df[c]) for c in cols}
    sel["open_finite_share_cohort"] = {b: float(np.isfinite(coh[f"OPEN_{b}"]).mean()) for b in BUILDS}
    # frozen prediction models for method_out (fit on EXP5, applied unchanged): OLS of O2r_m50 on standardised B5
    fitd = df[np.isfinite(df.O2r_m50) & np.all(np.isfinite(df[B5]), 1) & np.isfinite(df.OPEN_home)]
    mu, sd = fitd[B5].mean(), fitd[B5].std()
    X0 = np.c_[np.ones(len(fitd)), ((fitd[B5] - mu) / sd).to_numpy()]
    w0 = np.linalg.lstsq(X0, fitd.O2r_m50.to_numpy(), rcond=None)[0]
    X1 = np.c_[X0, fitd.OPEN_home.to_numpy()]
    w1 = np.linalg.lstsq(X1, fitd.O2r_m50.to_numpy(), rcond=None)[0]
    pred_models = {"B5": {"coef": w0.tolist(), "mu": mu.to_dict(), "sd": sd.to_dict()},
                   "B5_plus_OPEN_home": {"coef": w1.tolist()}, "n_fit": int(len(fitd)),
                   "note": "OLS on EXP5 concepts with finite O2r_m50 (TAG), B5 standardised with EXP5 constants"}
    coh.to_parquet(DATA / "features_cohort.parquet", index=False)
    df.drop(columns=[c for c in ("O1c", "O1b", "O3") if c in df.columns]).to_parquet(
        DATA / "features_exp5_open.parquet", index=False)
    jdump(sel, RES / "exp5_selection_result.json")
    # outcome-free checklist: no outcome column in any cohort table
    bad = [c for c in coh.columns if c.startswith("O1") or c.startswith("O2") or c.startswith("O3")]
    from seal2 import check_sealed_untouched
    chk = check_sealed_untouched()
    s3m = s3.get("match_validation", {}).get("O2r_resid_match_fit_dev", {})
    spec = {
        "prereg_sha256": sha256_file(ROOT / "prereg.md"), "spec_v0_sha256": sha256_file(RES / "frozen_spec_v0.json"),
        "open_constants": CONST, "open_min_home_papers": 10, "open_min_components": 4,
        "outcome_grounding": grounding, "primary": primary,
        "O2r_resid": ({"a": s3m.get("a"), "b": s3m.get("b"), "source": "MATCH refit on EXP5 DEV"} if grounding == "MATCH"
                      else {"a": 2.7410366547641205, "b": 0.3966308230599589, "source": "EXP8 o2r_resid_fit.json"}),
        "extension_2017": extension, "power": sel["power"],
        "type_labels_sha256": sha256_file(DATA / "concept_types.csv"),
        "type_benchmark": json.loads((RES / "type_benchmark_final.json").read_text()) if (RES / "type_benchmark_final.json").exists() else None,
        "rungs": {r: {"cont": list(rung_design(coh, r)[0].columns), "cat": list(rung_design(coh, r)[1].columns)}
                  for r in RUNGS},
        "groups": POOL_GROUPS, "holm_family": [f"{x}|{y}" for x in ["OPEN_home", "OPEN_all", "OPEN_sizematch",
                                                                    "RETENTION_RATIO_early"] for y in OUTC],
        "directions": {"OPEN_home": 1, "OPEN_all": 1, "OPEN_sizematch": 1, "RETENTION_RATIO_early": -1},
        "bootstrap": {"B": 2000, "seed": SEED, "unit": "concept"},
        "prediction_models": pred_models,
        "cohort_n": int(len(coh)), "cohort_n_by_t0": coh.t0.value_counts().sort_index().to_dict(),
        "sha256": {p: sha256_file(ROOT / p) for p in ["data/features_cohort.parquet", "data/cohort_candidates_gated.csv",
                                                      "data/concept_types.csv", "data/covariates_cohort.parquet",
                                                      "data/ego_open_cohort.parquet", "data/features_exp5_open.parquet"]},
        "code_sha256": {p.relative_to(ROOT).as_posix(): sha256_file(p)
                        for p in sorted(list(ROOT.glob("*.py")) + list(ROOT.glob("lib/*.py")))},
        "pre_unseal_checklist": {"outcome_columns_in_cohort_table": bad, "sealed_parts": chk},
    }
    if bad or not chk["ok"]:
        raise RuntimeError(f"pre-unseal checklist failed: {bad} {chk}")
    if not a.no_freeze:
        from seal2 import freeze
        h = freeze(spec)
        logger.info(f"FROZEN spec sha256 {h}")
    else:
        jdump(spec, RES / "frozen_spec_draft.json")


if __name__ == "__main__":
    main()
