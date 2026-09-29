#!/usr/bin/env python3
"""Post-run audit with independent code paths (statsmodels, pandas dummies, hand-computed DL), writes
results/audit.json:
  1. A1 / A2 HOME joint betas re-derived with statsmodels GLM Poisson + age/year dummies on a 2,000-concept random
     subset, compared with pyfixest fepois on the SAME subset (same sign, |diff| < 0.02) and with the full-panel sign.
  2. The primary psp(CONS_early_home, O2r_m50 | B5 + dummies) re-derived with statsmodels OLS on ranks (|diff| < 1e-8).
  3. The DL pooled estimate (primary, O2r_m50 and O1c-O2r_m50) re-derived by hand from the per-group values.
  4. Shuffled-CONS placebo: CONS_early_home permuted within group (200 draws); 95th percentile of |psp| with O2r_m50.
Usage: uv run audit.py"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import rankdata

from common import B5, DATA, EXP5, RES, SEED, body_of_split, jdump, jload, setup_logger

logger = setup_logger("audit")


def panel_home() -> pd.DataFrame:
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "t0"])
    f = pd.read_parquet(DATA / "cheng_features.parquet")
    f = f[(f.body_src == "EXP5") & (f.build == "HOME")]
    V = pd.read_parquet(DATA / "V_exp5.parquet", columns=["ci", "year", "V"]).set_index(["ci", "year"]).V
    d = f.merge(fr, on="ci")
    d = d[(d.year >= d.t0 + 1) & (d.year <= np.minimum(d.t0 + 10, 2021))].dropna(subset=["CONS", "EMB", "SOC"])
    d["Vt"] = V.reindex(pd.MultiIndex.from_arrays([d.ci, d.year])).to_numpy()
    d["Vn"] = V.reindex(pd.MultiIndex.from_arrays([d.ci, d.year + 1])).to_numpy()
    d = d.dropna(subset=["Vn"]).copy()
    d["age"] = d.year - d.t0
    for c in ["CONS", "EMB", "SOC"]:
        d["z" + c] = (d[c] - d[c].mean()) / d[c].std(ddof=0)
    d["logV"] = np.log1p(d.Vt)
    return d


def audit_panel(full: dict) -> dict:
    import pyfixest as pf
    d = panel_home()
    rng = np.random.default_rng(SEED)
    pick = rng.choice(d.ci.unique(), 2000, replace=False)
    s = d[d.ci.isin(pick)].copy()
    out = {"n_rows_subset": int(len(s)), "n_concepts_subset": 2000}
    for m, xs in (("A1", ["zCONS", "zEMB", "zSOC"]), ("A2", ["zCONS", "zEMB", "zSOC", "logV"])):
        X = pd.concat([s[xs], pd.get_dummies(s.age, prefix="age", drop_first=True, dtype=float),
                       pd.get_dummies(s.year, prefix="yr", drop_first=True, dtype=float)], axis=1)
        X = sm.add_constant(X)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            glm = sm.GLM(s.Vn.to_numpy(float), X, family=sm.families.Poisson()).fit()
            pfb = float(pf.fepois(f"Vn ~ {' + '.join(xs)} | age + year", data=s).coef()["zCONS"])
        b_sm = float(glm.params["zCONS"])
        fb = full["builds"]["HOME"]["joint"][m]["coef"]["zCONS"]["b"]
        out[m] = {"statsmodels_glm_subset": b_sm, "pyfixest_subset": pfb, "abs_diff": abs(b_sm - pfb),
                  "full_panel_pyfixest": fb, "same_sign_as_full": bool(np.sign(b_sm) == np.sign(fb)),
                  "pass": bool(abs(b_sm - pfb) < 0.02 and np.sign(b_sm) == np.sign(fb))}
    return out


def audit_psp(S: dict) -> dict:
    df = pd.read_parquet(DATA / "static_analysis_table.parquet")
    d = df[df.body != "COHORT_2015_17"]
    d = d.dropna(subset=["CONS_early_home", "O2r_m50"] + B5)
    Z = pd.concat([pd.DataFrame(rankdata(d[B5], axis=0), index=d.index, columns=B5),
                   pd.get_dummies(d.t0, prefix="t0", drop_first=True, dtype=float),
                   pd.get_dummies(d.group, prefix="g", drop_first=True, dtype=float),
                   pd.get_dummies(d.body, prefix="b", drop_first=True, dtype=float)], axis=1)
    Z = sm.add_constant(Z)
    rx = sm.OLS(rankdata(d.CONS_early_home), Z).fit().resid
    ry = sm.OLS(rankdata(d.O2r_m50), Z).fit().resid
    r = float(np.corrcoef(rx, ry)[0, 1])
    pub = S["trait"]["EXP5_pooled|CONS_early_home"]["psp"]["O2r_m50"]["rho"]
    return {"statsmodels": r, "pipeline": pub, "abs_diff": abs(r - pub), "n": int(len(d)),
            "pass": bool(abs(r - pub) < 1e-8)}


def audit_dl(S: dict) -> dict:
    out = {}
    for y in ["O2r_m50", "O1c-O2r_m50"]:
        dl = S["DL"]["EXP5_pooled"][y]
        b, se = [], []
        for g in ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]:
            r = S["trait"][f"EXP5_pooled|group={g}|CONS_early_home"]
            v = r["psp"][y] if y in r["psp"] else r["paired_diff"][y]
            b.append(v["rho"])
            se.append(v["se"])
        b, se = np.array(b), np.array(se)
        w = 1 / se**2
        fixed = (w * b).sum() / w.sum()
        Q = (w * (b - fixed) ** 2).sum()
        k = len(b)
        tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w**2).sum() / w.sum()))
        ws = 1 / (se**2 + tau2)
        est = (ws * b).sum() / ws.sum()
        I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 else 0.0
        out[y] = {"hand": est, "pipeline": dl["b"], "abs_diff": abs(est - dl["b"]), "I2_hand": I2,
                  "I2_pipeline": dl["I2"], "pass": bool(abs(est - dl["b"]) < 1e-10)}
    return out


def audit_placebo(S: dict, n: int = 200) -> dict:
    from static_cheng import design, psp_multi
    df = pd.read_parquet(DATA / "static_analysis_table.parquet")
    d = df[df.body != "COHORT_2015_17"].dropna(subset=["CONS_early_home", "O2r_m50"] + B5).reset_index(drop=True)
    B, C = design(d)
    C = C[:, C.std(0) > 0]
    y = d[["O2r_m50"]].to_numpy(float)
    rng = np.random.default_rng(SEED + 99)
    grp = d.group5.to_numpy()
    vals = []
    for _ in range(n):
        x = d.CONS_early_home.to_numpy(float).copy()
        for gname in np.unique(grp):
            m = np.nonzero(grp == gname)[0]
            x[m] = x[rng.permutation(m)]
        vals.append(psp_multi(x[:, None], y, B, C)[0, 0])
    vals = np.abs(np.array(vals))
    obs = S["trait"]["EXP5_pooled|CONS_early_home"]["psp"]["O2r_m50"]["rho"]
    return {"n_draws": n, "p95_abs_psp": float(np.percentile(vals, 95)), "max_abs_psp": float(vals.max()),
            "observed_psp": obs, "observed_exceeds_p95": bool(abs(obs) > np.percentile(vals, 95))}


@logger.catch(reraise=True)
def main() -> None:
    A = jload(RES / "cheng_panel_models.json")
    S = jload(RES / "cheng_static.json")
    res = {"panel_rederivation": audit_panel(A), "psp_rederivation": audit_psp(S), "DL_by_hand": audit_dl(S),
           "placebo_shuffled_CONS_within_group": audit_placebo(S)}
    res["all_rederivations_pass"] = bool(res["panel_rederivation"]["A1"]["pass"] and
                                         res["panel_rederivation"]["A2"]["pass"] and
                                         res["psp_rederivation"]["pass"] and
                                         all(v["pass"] for v in res["DL_by_hand"].values()))
    jdump(res, RES / "audit.json")
    logger.info(f"audit: {res}")


if __name__ == "__main__":
    main()
