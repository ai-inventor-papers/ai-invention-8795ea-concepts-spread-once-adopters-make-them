#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers (does NOT import src/ or vendor/).

Reads the raw inputs (Exp10 parquet/csv, EXP5 frame, EXP8 outcomes, frozen constants) and recomputes, by its own code:
  1. OPEN_home and NOVCHURN_home from the frozen winsor/z constants;
  2. psp (rank-residual partial Spearman) at R2 for the 2015-17 cohort and the EXP5 bodies, with its own design
     matrix, ranking (pandas average ranks) and least squares (numpy.linalg.lstsq);
  3. the non-selection DL + HKSJ pool at R2, using its own concept bootstrap SEs (B = 500, different seed);
  4. placebos: the same psp with the feature shuffled within body (200 draws) must be null, and the pool of shuffled
     psps must not exclude 0.
Writes results/audit.json. Usage: python audit.py"""
from __future__ import annotations

import json
import math
import os
from pathlib import Path

import numpy as np
import pandas as pd

WS = Path(__file__).resolve().parent
RUN = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[3])))
LOOP = RUN / "."
E10 = LOOP / "round-4/experiment-10/src"
E8 = LOOP / "round-3/experiment-8/src"
EXP5 = LOOP / "round-2/experiment-5/src"
COMP = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
GROUP = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med"}


def zscores(df, const):
    out = {}
    for k in COMP:
        c = const[k]
        v = df[f"{k}__home"].astype(float).clip(c["lo"], c["hi"])
        out[k] = c["sign"] * (v - c["mu"]) / c["sd"]
    return pd.DataFrame(out, index=df.index)


def indices(df, const):
    z = zscores(df, const)
    nfin = z.notna().sum(axis=1)
    open_home = z.mean(axis=1, skipna=True).where(nfin >= 4)
    nov = z[["NOV_res", "edge_persistence"]].mean(axis=1).where(z[["NOV_res", "edge_persistence"]].notna().all(axis=1))
    small = df["n_home_early"] < 10
    return open_home.mask(small), nov.mask(small)


def design_r2(df):
    """R2 = ranks(B5 + CONTACT_REACH) + onset-year, window, type, generic and level dummies (own construction)."""
    cont = df[["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH"]]
    parts = [pd.get_dummies(df["t0"].astype(str), prefix="y", drop_first=True, dtype=float),
             pd.get_dummies(df["type"].fillna("unlabelled"), prefix="t", dtype=float),
             df[["generic"]].astype(float), pd.get_dummies(df["level"].astype(str), prefix="l", dtype=float)]
    if "window_flag" in df and df["window_flag"].nunique() > 1:
        parts.append(df[["window_flag"]].astype(float))
    return cont, pd.concat(parts, axis=1)


def psp(x, y, cont, cat):
    X = np.column_stack([np.ones(len(x)), cont.rank().to_numpy(), cat.to_numpy()])
    X = X[:, np.r_[True, X[:, 1:].std(0) > 0]]
    r = []
    for v in (x.rank().to_numpy(), y.rank().to_numpy()):
        b = np.linalg.lstsq(X, v, rcond=None)[0]
        r.append(v - X @ b)
    return float(np.corrcoef(r[0], r[1])[0, 1])


def cell(df, feat, B, rng):
    d = df.dropna(subset=[feat, "O2r_m50", "logvol", "growth_c", "offhome_share", "entropy", "reach",
                          "CONTACT_REACH"]).reset_index(drop=True)
    cont, cat = design_r2(d)
    est = psp(d[feat], d["O2r_m50"], cont, cat)
    zs = []
    for _ in range(B):
        i = rng.integers(0, len(d), len(d))
        zs.append(math.atanh(psp(d[feat].iloc[i].reset_index(drop=True), d["O2r_m50"].iloc[i].reset_index(drop=True),
                                 cont.iloc[i].reset_index(drop=True), cat.iloc[i].reset_index(drop=True))))
    return {"n": len(d), "psp": est, "se_z": float(np.std(zs, ddof=1))}, d, cont, cat


def pool(rows):
    z = np.array([math.atanh(r["psp"]) for r in rows])
    v = np.array([r["se_z"] ** 2 for r in rows])
    w = 1 / v
    q = float(np.sum(w * (z - np.sum(w * z) / w.sum()) ** 2))
    k = len(z)
    t2 = max(0.0, (q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum()))
    ws = 1 / (v + t2)
    mu = float(np.sum(ws * z) / ws.sum())
    se_hk = math.sqrt(np.sum(ws * (z - mu) ** 2) / (k - 1) / ws.sum())
    from scipy.stats import t as tdist
    tc = float(tdist.ppf(0.975, k - 1))
    return {"k": k, "est": math.tanh(mu), "dl_ci": [math.tanh(mu - 1.96 / math.sqrt(ws.sum())),
                                                   math.tanh(mu + 1.96 / math.sqrt(ws.sum()))],
            "hksj_ci": [math.tanh(mu - tc * se_hk), math.tanh(mu + tc * se_hk)], "I2": max(0.0, (q - k + 1) / q) if q else 0}


def main():
    const = json.loads((E10 / "results/frozen_spec.json").read_text())["open_constants"]["home"]
    rng = np.random.default_rng(12345)
    # ---- cohort
    coh = pd.read_parquet(E10 / "data/analysis_cohort.parquet")
    oh, nc = indices(coh, const)
    out = {"open_home_cohort_maxabs_vs_stored": float(np.nanmax(np.abs(oh - coh["OPEN_home"])))}
    coh = coh.assign(OPEN_A=oh, NOV_A=nc)
    # ---- EXP5 bodies (own joins)
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "t0", "group", "split", "level"])
    e5 = (fr.merge(pd.read_parquet(E10 / "data/ego_open_exp5.parquet"), on="ci", how="left")
          .merge(pd.read_parquet(E10 / "data/covariates_exp5.parquet").drop(columns=["level"]), on="ci", how="left")
          .merge(pd.read_csv(E10 / "data/concept_types.csv").query("frame == 'exp5'")[["ci", "type", "generic"]],
                 on="ci", how="left")
          .merge(pd.read_parquet(E8 / "data/outcomes.parquet", columns=["ci", "O2r_m50"]), on="ci", how="left"))
    e5["generic"] = e5["generic"].fillna(0)
    oh5, nc5 = indices(e5, const)
    e5 = e5.assign(OPEN_A=oh5, NOV_A=nc5)
    bodies = {"B1_DEV": e5[e5.split == "DEV"], "B3_EXP5_COHORT_2010_14": e5[e5.split == "COHORT"],
              "B4_COHORT_2015_17": coh}
    for g in ("PHYS", "LIFEENV", "SOC", "MATHDEC"):
        bodies[f"B2_{g}"] = e5[e5.split == f"HELDOUT_{g}"]
    syn = json.loads((WS / "results/evidence_synthesis.json").read_text())
    rec = {(r["body"], r["feature"]): r for r in syn["rows"]}
    cells, placebo = {}, {}
    for b, d in bodies.items():
        for f, fa in (("OPEN_home", "OPEN_A"), ("NOVCHURN_home", "NOV_A")):
            c, dd, cont, cat = cell(d, fa, 500, rng)
            c["pipeline_psp"] = rec[(b, f)]["R2"]["psp"]
            c["pipeline_n"] = rec[(b, f)]["R2"]["n"]
            c["abs_diff"] = abs(c["psp"] - c["pipeline_psp"])
            cells[f"{b}|{f}"] = c
            sh = [psp(pd.Series(rng.permutation(dd[fa].to_numpy())), dd["O2r_m50"], cont, cat) for _ in range(200)]
            placebo[f"{b}|{f}"] = {"mean": float(np.mean(sh)), "se_mean": float(np.std(sh, ddof=1) / math.sqrt(len(sh))), "p95_abs": float(np.percentile(np.abs(sh), 95)),
                                   "share_ge_observed": float(np.mean(np.abs(sh) >= abs(c["psp"]))),
                                   "one_draw": sh[0]}
    ns_open = [cells[f"{b}|OPEN_home"] for b in ("B2_PHYS", "B2_LIFEENV", "B2_SOC", "B2_MATHDEC",
                                                 "B3_EXP5_COHORT_2010_14", "B4_COHORT_2015_17")]
    ns_nov = [cells[f"{b}|NOVCHURN_home"] for b in ("B2_PHYS", "B2_LIFEENV", "B2_SOC", "B2_MATHDEC",
                                                    "B3_EXP5_COHORT_2010_14")]
    p_open, p_nov = pool(ns_open), pool(ns_nov)
    # placebo pool: shuffled feature in every body, own bootstrap SEs reused
    sh_rows = [{"psp": placebo[f"{b}|OPEN_home"]["one_draw"], "se_z": cells[f"{b}|OPEN_home"]["se_z"]}
               for b in ("B2_PHYS", "B2_LIFEENV", "B2_SOC", "B2_MATHDEC", "B3_EXP5_COHORT_2010_14", "B4_COHORT_2015_17")]
    p_sh = pool(sh_rows)
    res = {"cells": cells, "placebo": placebo, "pool_OPEN_home_R2": p_open, "pool_NOVCHURN_home_R2": p_nov,
           "pipeline_pool_OPEN_home_R2": syn["pools"]["OPEN_home|R2"]["nonselection"]["est"],
           "pipeline_pool_NOVCHURN_home_R2": syn["pools"]["NOVCHURN_home|R2"]["nonselection"]["est"],
           "placebo_pool_OPEN_home_shuffled": p_sh,
           "max_abs_diff_psp": max(c["abs_diff"] for c in cells.values()),
           "n_mismatch_n": sum(c["n"] != c["pipeline_n"] for c in cells.values()), **out}
    res["verdict"] = {
        "psp_reproduced_1e-9": res["max_abs_diff_psp"] < 1e-9 and res["n_mismatch_n"] == 0,
        "pool_reproduced_within_0.01": abs(p_open["est"] - res["pipeline_pool_OPEN_home_R2"]) < 0.01,
        "placebo_pool_ci_includes_0": p_sh["dl_ci"][0] <= 0 <= p_sh["dl_ci"][1],
        "placebo_cells_null_mean_within_3se": all(abs(p["mean"]) < 3 * p["se_mean"] for p in placebo.values())}
    (WS / "results/audit.json").write_text(json.dumps(res, indent=1))
    print(json.dumps({k: res[k] for k in ("max_abs_diff_psp", "n_mismatch_n", "open_home_cohort_maxabs_vs_stored")},
                     indent=0))
    print("pool OPEN", p_open, "\npool NOV", p_nov, "\nplacebo pool", p_sh, "\nverdict", res["verdict"])


if __name__ == "__main__":
    main()
