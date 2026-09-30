#!/usr/bin/env python3
"""Independent re-derivation of the HEADLINE numbers from raw inputs through different code paths
(results/rederive.json), plus placebo versions of each test that must FAIL.

Raw inputs: data/cheng_features.parquet (per concept-year measures; the static early trait is re-averaged here, not
read from cheng_static), EXP5 scan/agg_counts.parquet (V(t) re-aggregated here, not read from V_exp5), EXP8
analysis_table / EXP10 analysis_cohort (B5 + outcomes), EXP10 sealed parts (cohort V(t0+3)).
Code paths: statsmodels GLM (Poisson / NB with fixed alpha) with pandas dummies for the panel; pandas average ranks
+ numpy QR residualisation for partial Spearman (the pipeline uses pyfixest / numpy IRLS and scipy rankdata + lstsq).
Usage: uv run rederive.py"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
import statsmodels.api as sm

from common import B5, DATA, EXP5, EXP8, EXP10, RES, jdump, jload, setup_logger

logger = setup_logger("rederive")
rng = np.random.default_rng(777)


def early_trait(feat: pd.DataFrame, t0: pd.Series, build: str = "HOME") -> pd.Series:
    f = feat[feat.build == build].merge(t0.rename("t0"), left_on="ci", right_index=True)
    f = f[(f.year - f.t0).isin([1, 2])]
    return f.groupby("ci").CONS.mean()


def resid_qr(Z: np.ndarray, y: np.ndarray) -> np.ndarray:
    Q, R = np.linalg.qr(Z)
    keep = np.abs(np.diag(R)) > 1e-9 * np.abs(np.diag(R)).max()
    Q = Q[:, keep]
    return y - Q @ (Q.T @ y)


def psp_qr(d: pd.DataFrame, x: str, y: str, cats: list[str]) -> float:
    d = d.dropna(subset=[x, y] + B5)
    Z = [np.ones(len(d))] + [d[c].rank(method="average").to_numpy() for c in B5]
    for c in cats:
        Z.append(pd.get_dummies(d[c].astype(str), drop_first=True, dtype=float).to_numpy())
    Z = np.column_stack(Z)
    rx = resid_qr(Z, d[x].rank(method="average").to_numpy())
    ry = resid_qr(Z, d[y].rank(method="average").to_numpy())
    return float(np.corrcoef(rx, ry)[0, 1]), len(d)


def glm_panel(p: pd.DataFrame, xs: list[str], family) -> float:
    X = pd.concat([p[xs], pd.get_dummies(p.age, prefix="a", drop_first=True, dtype=float),
                   pd.get_dummies(p.year, prefix="y", drop_first=True, dtype=float)], axis=1)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = sm.GLM(p.Vn.to_numpy(float), sm.add_constant(X), family=family).fit()
    return float(r.params[xs[0]]), float(r.bse[xs[0]])


@logger.catch(reraise=True)
def main() -> None:
    A = jload(RES / "cheng_panel_models.json")
    S = jload(RES / "cheng_static.json")
    C = jload(RES / "panel_C.json")
    out = {"label": "independent re-derivation from raw inputs + placebo checks"}
    feat = pd.read_parquet(DATA / "cheng_features.parquet")
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "t0", "split"])
    # ---------- V(t) straight from EXP5 agg_counts (TAG = tagstate 1)
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "tagstate", "n"])
    V = ag[ag.tagstate == 1].groupby(["ci", "year"]).n.sum()
    del ag
    # ---------- static trait + raw Spearman with V(t0+3), EXP5 pooled
    f5 = feat[feat.body_src == "EXP5"]
    ce = early_trait(f5, fr.set_index("ci").t0)
    s = fr.set_index("ci").assign(CONS=ce)
    s["V3"] = V.reindex(pd.MultiIndex.from_arrays([s.index, s.t0 + 3])).fillna(0).to_numpy()
    ok = s.CONS.notna()
    raw = float(s.loc[ok, "CONS"].rank().corr(s.loc[ok, "V3"].rank()))
    raw_perm = [float(s.loc[ok, "CONS"].rank().corr(pd.Series(rng.permutation(s.loc[ok, "V3"].to_numpy())).rank()
                                                   .set_axis(s.index[ok]))) for _ in range(200)]
    out["B_raw_spearman_primary"] = {
        "rederived": raw, "pipeline": S["volume"]["EXP5_pooled|volume"]["B_raw_spearman_V_t0p3"]["rho"],
        "n": int(ok.sum()), "placebo_shuffled_V_p95_abs": float(np.percentile(np.abs(raw_perm), 95))}
    # ---------- psp primary (EXP8 table + re-averaged CONS), and cohort
    at = pd.read_parquet(EXP8 / "data/analysis_table.parquet", columns=["ci", "t0", "group", "split"] + B5 +
                         ["O2r_m50", "O1c"])
    at["body"] = at.split
    at = at.merge(ce.rename("CONS"), left_on="ci", right_index=True, how="left")
    cats = ["t0", "group", "body"]
    p_reach, n_reach = psp_qr(at, "CONS", "O2r_m50", cats)
    common = at.dropna(subset=["CONS", "O2r_m50", "O1c"] + B5)
    p_o1c_c, _ = psp_qr(common, "CONS", "O1c", cats)
    placebo = []
    for _ in range(200):
        a2 = at.copy()
        a2["CONS"] = rng.permutation(a2.CONS.to_numpy())
        placebo.append(psp_qr(a2, "CONS", "O2r_m50", cats)[0])
    pr = S["trait"]["EXP5_pooled|CONS_early_home"]
    out["P3_psp_O2r_m50_primary"] = {"rederived": p_reach, "pipeline": pr["psp"]["O2r_m50"]["rho"], "n": n_reach,
                                     "placebo_global_shuffle_p95_abs": float(np.percentile(np.abs(placebo), 95)),
                                     "placebo_share_as_extreme": float(np.mean(np.abs(placebo) >= abs(p_reach)))}
    out["P5_paired_diff_point"] = {"rederived": p_o1c_c - p_reach, "pipeline": pr["paired_diff"]["O1c-O2r_m50"]["rho"]}
    fc = feat[feat.body_src == "COHORT_2015_17"]
    ac = pd.read_parquet(EXP10 / "data/analysis_cohort.parquet", columns=["ci", "t0", "group", "window_flag"] + B5 +
                         ["O2r_m50"])
    ac = ac.merge(early_trait(fc, ac.set_index("ci").t0).rename("CONS"), left_on="ci", right_index=True, how="left")
    pc, nc = psp_qr(ac, "CONS", "O2r_m50", ["t0", "group", "window_flag"])
    out["P3_psp_O2r_m50_cohort_2015_17"] = {"rederived": pc, "n": nc,
                                            "pipeline": S["trait"]["COHORT_2015_17|CONS_early_home"]["psp"]["O2r_m50"]["rho"]}
    # ---------- test A on the FULL HOME panel with statsmodels GLM
    h = f5[f5.build == "HOME"].merge(fr[["ci", "t0"]], on="ci")
    h = h[(h.year >= h.t0 + 1) & (h.year <= np.minimum(h.t0 + 10, 2021))].dropna(subset=["CONS", "EMB", "SOC"])
    h["Vn"] = V.reindex(pd.MultiIndex.from_arrays([h.ci, h.year + 1])).fillna(0).to_numpy()
    h["Vt"] = V.reindex(pd.MultiIndex.from_arrays([h.ci, h.year])).fillna(0).to_numpy()
    h["age"] = h.year - h.t0
    h["logV"] = np.log1p(h.Vt)
    for c in ["CONS", "EMB", "SOC"]:
        h["z" + c] = (h[c] - h[c].mean()) / h[c].std(ddof=0)
    xs = ["zCONS", "zEMB", "zSOC"]
    b1, se1 = glm_panel(h, xs, sm.families.Poisson())
    b2, _ = glm_panel(h, xs + ["logV"], sm.families.Poisson())
    alpha = A["builds"]["HOME"]["joint"]["A1_NB"]["alpha"]
    bnb, _ = glm_panel(h, xs, sm.families.NegativeBinomial(alpha=alpha))
    hj = A["builds"]["HOME"]["joint"]
    out["A_full_panel_statsmodels"] = {
        "n_rows": int(len(h)), "n_rows_pipeline": hj["A1"]["n_rows"],
        "A1_b": {"rederived": b1, "pipeline": hj["A1"]["coef"]["zCONS"]["b"]},
        "A2_b": {"rederived": b2, "pipeline": hj["A2"]["coef"]["zCONS"]["b"]},
        "ratio": {"rederived": b2 / b1, "pipeline": hj["ratio_boot"]["ratio"]},
        "A1_NB_b_GLM_fixed_alpha": {"rederived": bnb, "pipeline": hj["A1_NB"]["coef"]["zCONS"]["b"], "alpha": alpha}}
    # placebo: CONS permuted across concept-years -> A1 coefficient must vanish
    pl = []
    for _ in range(5):
        hp = h.copy()
        hp["zCONS"] = rng.permutation(hp.zCONS.to_numpy())
        bp, sep = glm_panel(hp, xs, sm.families.Poisson())
        pl.append({"b": bp, "z_naive": bp / sep})
    out["A_full_panel_statsmodels"]["placebo_permuted_CONS_A1"] = pl
    out["C1_note"] = {"pipeline_b": C["C1"]["coef"]["zCONS"]["b"], "rederived": None,
                      "why": "concept + year FE PPML with 11,761 concepts is not re-fitted through a second library "
                             "here (dense statsmodels dummies do not fit in memory); C1 has CRV1 and 500-draw bootstrap"}
    tol = {"B_raw_spearman_primary": 1e-9, "P3_psp_O2r_m50_primary": 1e-9, "P5_paired_diff_point": 1e-9,
           "P3_psp_O2r_m50_cohort_2015_17": 1e-9}
    chk = {k: abs(out[k]["rederived"] - out[k]["pipeline"]) < t for k, t in tol.items()}
    a = out["A_full_panel_statsmodels"]
    chk.update({"A1_b": abs(a["A1_b"]["rederived"] - a["A1_b"]["pipeline"]) < 1e-6,
                "A2_b": abs(a["A2_b"]["rederived"] - a["A2_b"]["pipeline"]) < 1e-6,
                "ratio": abs(a["ratio"]["rederived"] - a["ratio"]["pipeline"]) < 1e-5,
                "A1_NB_b": abs(a["A1_NB_b_GLM_fixed_alpha"]["rederived"] - a["A1_NB_b_GLM_fixed_alpha"]["pipeline"]) < 5e-3,
                "placebo_raw_fails": out["B_raw_spearman_primary"]["placebo_shuffled_V_p95_abs"] < abs(raw),
                "placebo_psp_fails": out["P3_psp_O2r_m50_primary"]["placebo_global_shuffle_p95_abs"] < abs(p_reach),
                "placebo_A1_fails": all(abs(x["b"]) < 0.1 * abs(b1) for x in pl)})
    out["checks"] = chk
    out["all_pass"] = bool(all(chk.values()))
    jdump(out, RES / "rederive.json")
    logger.info(f"rederive checks: {chk}")


if __name__ == "__main__":
    main()
