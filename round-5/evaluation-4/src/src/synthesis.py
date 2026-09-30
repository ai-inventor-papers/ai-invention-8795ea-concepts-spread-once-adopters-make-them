#!/usr/bin/env python3
"""P0 gates G1/G2 + item 11: descriptive evidence synthesis of OPEN_home and NOVCHURN_home across every body already
scored (EXP5 DEV / old held-out groups / 2010-14 cohort, and the 2015-17 cohort), with design-status labels.

Estimator = Exp10 (art_NMe386dX9GLF) lib/ladder.py + lib/rq1stats.py, copied verbatim into vendor/: rank-residual
partial Spearman (psp), rungs R0/R2/R3, concept bootstrap with refit in every draw. OPEN_home and NOVCHURN_home use
the FROZEN EXP5 winsor bounds / z constants in Exp10 results/frozen_spec.json -> open_constants.home.
Pooling: DerSimonian-Laird on Fisher-z psp with the bootstrap SE of z, plus Hartung-Knapp-Sidik-Jonkman (HKSJ).
Usage: python src/synthesis.py [--nboot 2000] [--workers 3]"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
sys.dont_write_bytecode = True
WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "vendor"))
sys.path.insert(0, str(WS / "src"))

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

from ladder import ANALYSIS_GROUP, open_score, psp_boot2, rung_design  # noqa: E402
from paths import E10, E8, EXP5, RES, FIG, LOGS, jdump  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "synthesis.log", rotation="30 MB", level="DEBUG")

SEED_E10 = 20260929          # Exp10 frozen_spec.bootstrap.seed (used for the gates so CIs are comparable)
SEED_PLAN = 0                # plan's seed; reported alongside for G2
FEATS = ["OPEN_home", "NOVCHURN_home"]
RUNGS = ["R0", "R2", "R3"]
HELD = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


# ----------------------------------------------------------------------------- data
def frozen_const() -> dict:
    return json.loads((E10 / "results/frozen_spec.json").read_text())["open_constants"]


def add_indices(df: pd.DataFrame, const: dict) -> pd.DataFrame:
    o, Z = open_score(df, "home", const["home"])
    df = df.copy()
    df["OPEN_home_re"] = o
    nc = Z[["NOV_res", "edge_persistence"]].to_numpy()          # signs already applied (+NOV_res, -edge_persistence)
    v = np.where(np.isfinite(nc).all(1), nc.mean(1), np.nan)
    v[df["n_home_early"].to_numpy() < 10] = np.nan                  # same HOME min-paper rule as OPEN_home
    df["NOVCHURN_home"] = v
    return df


def exp5_table(const: dict) -> tuple[pd.DataFrame, dict]:
    """Identical joins to Exp10 s8_select.exp5_table (frame + ego + covariates + types + EXP8 outcomes)."""
    fr = pd.read_csv(EXP5 / "frame_concepts.csv")
    fr["split_raw"] = fr["split"]
    fr["split"] = np.where(fr.split_raw.str.startswith("HELDOUT"), "HELDOUT", fr.split_raw)
    fr = fr[["ci", "concept_id", "name", "t0", "group", "split", "split_raw", "home", "intersect40"]]
    eg = pd.read_parquet(E10 / "data/ego_open_exp5.parquet")
    cv = pd.read_parquet(E10 / "data/covariates_exp5.parquet")
    ty = pd.read_csv(E10 / "data/concept_types.csv")
    ty["type_agree"] = ty.type_agree.fillna(False).astype(bool)
    ty = ty[ty.frame == "exp5"][["ci", "type", "generic", "type_agree"]]
    oc = pd.read_parquet(E8 / "data/outcomes.parquet", columns=["ci", "O2r_m50", "O2r_resid"])
    joins = {"frame": len(fr)}
    df = fr.merge(eg, on="ci", how="left")
    joins["after_ego_nonnull"] = int(df.n_home_early.notna().sum())
    df = df.merge(cv, on="ci", how="left")
    joins["after_cov_nonnull"] = int(df.logvol.notna().sum())
    df = df.merge(ty, on="ci", how="left")
    joins["type_nonnull"] = int(df.type.notna().sum())
    df = df.merge(oc, on="ci", how="left")
    joins["O2r_m50_finite"] = int(np.isfinite(df.O2r_m50).sum())
    df["agroup"] = df.group.map(ANALYSIS_GROUP)
    df["home_coverage_early"] = df.n_home_early / df.n_all_early.replace(0, np.nan)
    df["generic"] = df.generic.fillna(0)
    df = add_indices(df, const)
    df["OPEN_home"] = df["OPEN_home_re"]
    return df, joins


def cohort_table(const: dict) -> pd.DataFrame:
    df = pd.read_parquet(E10 / "data/analysis_cohort.parquet")
    df = add_indices(df, const)
    return df


# ----------------------------------------------------------------------------- estimation
def _cell(args):
    key, df, x, y, rung, nboot, seed = args
    Bc, Cc = rung_design(df, rung)
    r = psp_boot2(df[x].to_numpy(float), df[y].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float), nboot, seed)
    bs = r.pop("boot")
    z = np.arctanh(np.clip(bs, -0.999999, 0.999999)) if len(bs) else np.array([])
    r["se_z"] = float(np.std(z, ddof=1)) if len(z) > 1 else math.nan
    r.update({"x": x, "y": y, "rung": rung, "n_boot": nboot, "seed": seed})
    return key, r


def _placebo(args):
    key, df, x, y, nperm, seed = args
    from rq1stats import psp_point
    Bc, Cc = rung_design(df, "R2")
    xx, yy, B, C = df[x].to_numpy(float), df[y].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float)
    ok = np.isfinite(xx) & np.isfinite(yy) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
    xx, yy, B, C = xx[ok], yy[ok], B[ok], C[ok]
    rng = np.random.default_rng(seed)
    v = np.array([psp_point(xx, rng.permutation(yy), B, C) for _ in range(nperm)])
    return key, {"n": int(ok.sum()), "nperm": nperm, "p95_abs_psp": float(np.nanpercentile(np.abs(v), 95)),
                 "mean_psp": float(np.nanmean(v))}


def dl_hksj(rows: list[dict]) -> dict:
    """DL random effects on Fisher z (se_z from the bootstrap) + HKSJ interval; back-transformed to r."""
    z = np.array([math.atanh(r["rho"]) for r in rows])
    se = np.array([r["se_z"] for r in rows])
    k = len(z)
    w = 1 / se**2
    zf = (w * z).sum() / w.sum()
    Q = float((w * (z - zf) ** 2).sum())
    Cc = w.sum() - (w**2).sum() / w.sum()
    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 else 0.0
    ws = 1 / (se**2 + tau2)
    mu = float((ws * z).sum() / ws.sum())
    se_dl = math.sqrt(1 / ws.sum())
    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0
    q = float((ws * (z - mu) ** 2).sum() / (k - 1)) if k > 1 else math.nan
    se_hk = math.sqrt(q / ws.sum()) if k > 1 else math.nan
    t = stats.t.ppf(0.975, k - 1) if k > 1 else math.nan
    th = math.tanh
    return {"k": k, "est": th(mu), "dl_ci": [th(mu - 1.96 * se_dl), th(mu + 1.96 * se_dl)],
            "hksj_ci": [th(mu - t * se_hk), th(mu + t * se_hk)] if k > 1 else [math.nan, math.nan],
            "Q": Q, "I2": float(I2), "tau2_z": float(tau2), "z": mu, "se_z_dl": se_dl, "se_z_hksj": se_hk,
            "I2_note": "imprecise at small k (k <= 6)"}


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nboot", type=int, default=2000)
    ap.add_argument("--nperm", type=int, default=200)
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    const = frozen_const()
    e5, joins = exp5_table(const)
    coh = cohort_table(const)
    logger.info(f"EXP5 rows {len(e5)}; joins {joins}; cohort rows {len(coh)}")

    # ---------------- G1: OPEN_home recomputation vs Exp10 frozen constants; pooled EXP5 psp at R0/R2
    sel = json.loads((E10 / "results/exp5_selection_result.json").read_text())
    from rq1stats import psp_point

    def point(df, x, y, rung):
        Bc, Cc = rung_design(df, rung)
        xx, yy, B, C = df[x].to_numpy(float), df[y].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float)
        ok = np.isfinite(xx) & np.isfinite(yy) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
        return psp_point(xx[ok], yy[ok], B[ok], C[ok]), int(ok.sum())

    g1 = {"open_home_source": "recomputed from ego_open_exp5.parquet components with frozen_spec.open_constants.home "
                              "(no OPEN_home column exists in ego_open_exp5 / covariates_exp5)"}
    for r in ("R0", "R2"):
        v, n = point(e5, "OPEN_home", "O2r_m50", r)
        pub = sel["ladder"][f"OPEN_home|O2r_m50|{r}"]["rho"]
        g1[f"OPEN_home|O2r_m50|{r}"] = {"recomputed": v, "n": n, "published": pub, "published_n":
                                        sel["ladder"][f"OPEN_home|O2r_m50|{r}"]["n"], "abs_diff": abs(v - pub),
                                        "pass_3dp": round(v, 3) == round(pub, 3)}
    for k in ("NOV_res", "edge_persistence"):
        v, n = point(e5, f"{k}__home", "O2r_m50", "R2")
        pub = sel["components"][f"{k}__home|O2r_m50|R2"]["rho"]
        g1[f"{k}__home|O2r_m50|R2"] = {"recomputed": v, "n": n, "published": pub, "abs_diff": abs(v - pub),
                                       "pass_3dp": round(v, 3) == round(pub, 3)}
    g1["pass_R0"] = g1["OPEN_home|O2r_m50|R0"]["pass_3dp"]
    g1["pass_R2"] = g1["OPEN_home|O2r_m50|R2"]["pass_3dp"] and all(
        g1[f"{k}__home|O2r_m50|R2"]["pass_3dp"] for k in ("NOV_res", "edge_persistence"))
    logger.info(f"G1 R0 {g1['OPEN_home|O2r_m50|R0']['recomputed']:.4f} vs {g1['OPEN_home|O2r_m50|R0']['published']:.4f}; "
                f"R2 {g1['OPEN_home|O2r_m50|R2']['recomputed']:.4f} vs {g1['OPEN_home|O2r_m50|R2']['published']:.4f}")

    # ---------------- G2: cohort OPEN_home (stored column) and recomputation
    cr = json.loads((E10 / "results/cohort_result.json").read_text())
    g2 = {"OPEN_home_stored_vs_recomputed_maxabs": float(np.nanmax(np.abs(coh.OPEN_home - coh.OPEN_home_re))),
          "nan_pattern_equal": bool((coh.OPEN_home.isna() == coh.OPEN_home_re.isna()).all())}
    jobs = [("G2|R2|e10seed", coh, "OPEN_home", "O2r_m50", "R2", a.nboot, SEED_E10),
            ("G2|R2|seed0", coh, "OPEN_home", "O2r_m50", "R2", a.nboot, SEED_PLAN),
            ("G2|R3|e10seed", coh, "OPEN_home", "O2r_m50", "R3", a.nboot, SEED_E10)]

    # ---------------- item 11 cells
    bodies = {"B1_DEV": ("selection", "selection", e5[e5.split == "DEV"]),
              "B2_HELDOUT_pooled": ("already-unsealed", "already-unsealed", e5[e5.split == "HELDOUT"]),
              "B3_EXP5_COHORT_2010_14": ("already-unsealed", "already-unsealed", e5[e5.split == "COHORT"]),
              "B4_COHORT_2015_17": ("confirmatory", "selection (index chosen here)", coh)}
    for g in HELD:
        bodies[f"B2_{g}"] = ("already-unsealed", "already-unsealed", e5[(e5.split == "HELDOUT") & (e5.group == g)])
    for bk, (_, _, d) in bodies.items():
        for f in FEATS:
            for r in RUNGS:
                jobs.append((f"{bk}|{f}|{r}", d, f, "O2r_m50", r, a.nboot, SEED_E10))
    pjobs = [(f"{bk}|{f}", d, f, "O2r_m50", a.nperm, SEED_E10 + 7) for bk, (_, _, d) in bodies.items() for f in FEATS]
    res, plc = {}, {}
    with ProcessPoolExecutor(a.workers) as ex:
        for k, r in ex.map(_cell, jobs):
            res[k] = r
            logger.info(f"{k}: {r['rho']:+.3f} [{r['ci'][0]:+.3f}, {r['ci'][1]:+.3f}] n={r['n']}")
        for k, r in ex.map(_placebo, pjobs):
            plc[k] = r
    pub_ci = cr["primary"]["OPEN_home|O2r_m50|R2"]["ci"]
    pub_r2 = cr["primary"]["OPEN_home|O2r_m50|R2"]["rho"]
    pub_r3 = cr["primary"]["OPEN_home|O2r_m50|R3"]["rho"]
    g2.update({"R2": res["G2|R2|e10seed"], "R2_seed0": res["G2|R2|seed0"], "R3": res["G2|R3|e10seed"],
               "published_R2": pub_r2, "published_R2_ci": pub_ci, "published_R3": pub_r3})
    g2["pass_point_R2"] = round(res["G2|R2|e10seed"]["rho"], 3) == round(pub_r2, 3)
    g2["pass_point_R3"] = round(res["G2|R3|e10seed"]["rho"], 3) == round(pub_r3, 3)
    g2["pass_ci_e10seed"] = all(abs(a_ - b_) <= 0.005 for a_, b_ in zip(res["G2|R2|e10seed"]["ci"], pub_ci))
    g2["pass_ci_seed0"] = all(abs(a_ - b_) <= 0.005 for a_, b_ in zip(res["G2|R2|seed0"]["ci"], pub_ci))
    g2["pass"] = g2["pass_point_R2"] and g2["pass_point_R3"] and (g2["pass_ci_e10seed"] or g2["pass_ci_seed0"])
    for k in [k for k in res if k.startswith("G2|")]:
        res.pop(k)

    # ---------------- rows, pools
    rows = []
    for bk, (st_open, st_nc, d) in bodies.items():
        for f in FEATS:
            st = st_open if f == "OPEN_home" else st_nc
            row = {"body": bk, "feature": f, "status": st, "outcome": "O2r_m50",
                   "onsets": {"B1": "2003-09", "B2": "2003-09", "B3": "2010-14", "B4": "2015-17"}[bk[:2]],
                   "n_body_rows": int(len(d)), "placebo": plc[f"{bk}|{f}"]}
            for r in RUNGS:
                c = res[f"{bk}|{f}|{r}"]
                row[r] = {"psp": c["rho"], "ci": c["ci"], "n": c["n"], "se_z": c["se_z"], "p_two": c["p_two"]}
            rows.append(row)
    rows.append({"body": "B5_FRAME_N", "feature": "OPEN_home", "status": "pending iteration-5 artifact",
                 "R2": {"psp": None, "ci": [None, None], "n": None}})
    rows.append({"body": "B5_FRAME_N", "feature": "NOVCHURN_home", "status": "pending iteration-5 artifact",
                 "R2": {"psp": None, "ci": [None, None], "n": None}})

    def cells(feature, keys, rung):
        return [dict(res[f"{k}|{feature}|{rung}"], body=k) for k in keys]

    heldg = [f"B2_{g}" for g in HELD]
    pools = {}
    for rung in RUNGS:
        for f in FEATS:
            nonsel = heldg + ["B3_EXP5_COHORT_2010_14"] + (["B4_COHORT_2015_17"] if f == "OPEN_home" else [])
            alls = ["B1_DEV"] + heldg + ["B3_EXP5_COHORT_2010_14", "B4_COHORT_2015_17"]
            cs = [c for c in cells(f, nonsel, rung) if np.isfinite(c["rho"]) and np.isfinite(c["se_z"])]
            ca = [c for c in cells(f, alls, rung) if np.isfinite(c["rho"]) and np.isfinite(c["se_z"])]
            p = {"nonselection": dl_hksj(cs), "nonselection_bodies": [c["body"] for c in cs],
                 "all_bodies_includes_selection_data": dl_hksj(ca), "all_bodies": [c["body"] for c in ca]}
            p["sign_agreement_nonselection"] = f"{sum(c['rho'] > 0 for c in cs)}/{len(cs)}"
            p["sign_agreement_all"] = f"{sum(c['rho'] > 0 for c in ca)}/{len(ca)}"
            p["leave_one_body_out"] = {c["body"]: dl_hksj([x for x in cs if x["body"] != c["body"]])["est"]
                                       for c in cs}
            sel_est = res[f"B1_DEV|{f}|{rung}"]["rho"]
            p["selection_body_estimate"] = sel_est
            p["shrinkage_ratio_selection_over_nonselection"] = sel_est / p["nonselection"]["est"] \
                if p["nonselection"]["est"] else math.nan
            pools[f"{f}|{rung}"] = p
    for f in FEATS:
        pn = pools[f"{f}|R2"]["nonselection"]
        logger.info(f"POOL {f} R2 non-selection: {pn['est']:+.3f} DL [{pn['dl_ci'][0]:+.3f}, {pn['dl_ci'][1]:+.3f}] "
                    f"HKSJ [{pn['hksj_ci'][0]:+.3f}, {pn['hksj_ci'][1]:+.3f}] I2 {pn['I2']:.2f} k={pn['k']}")
    out = {"gates": {"G1": g1, "G2": g2}, "joins_exp5": joins,
           "n_cohort_rows": int(len(coh)), "rows": rows, "pools": pools,
           "design": {"estimator": "Exp10 ladder.psp_boot2 (vendor/ladder.py, vendor/rq1stats.py verbatim)",
                      "n_boot": a.nboot, "seed": SEED_E10, "rungs": RUNGS, "primary_rung": "R2",
                      "outcome": "O2r_m50 (EXP5 bodies: EXP8 outcomes.parquet; cohort: Exp10 analysis_cohort TAG)",
                      "NOVCHURN_home": "mean(z_NOV_res, -z_edge_persistence), HOME build, frozen EXP5 constants; "
                                       "NaN unless both finite and n_home_early >= 10",
                      "pooling": "DL on Fisher z with bootstrap se_z; HKSJ interval with t_{k-1}; back-transformed",
                      "headline_pool": "non-selection bodies only: B2 groups + B3 (+ B4 for OPEN_home)",
                      "placebo": f"within-body outcome permutation at R2, {a.nperm} draws, 95th pct of |psp|",
                      "deviation_seed": "bootstrap seed = Exp10's 20260929 (not 0) so CIs are comparable to the record; "
                                        "the G2 check is also run with seed 0 and reported"}}
    jdump(RES / "evidence_synthesis.json", out)
    jdump(RES / "gates_g1_g2.json", {"G1": g1, "G2": g2})
    logger.info(f"G1 pass R0={g1['pass_R0']} R2={g1['pass_R2']}; G2 pass={g2['pass']}")


if __name__ == "__main__":
    main()
