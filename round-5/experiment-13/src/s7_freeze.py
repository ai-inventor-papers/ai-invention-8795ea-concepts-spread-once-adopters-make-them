#!/usr/bin/env python3
"""S7: indices from the frozen EXP5 constants, pre-seal diagnostics (no outcome), expected primary n, fallback E, POWER
simulation, and the FREEZE (results/frozen_spec.json hash-chained as S7_freeze).

  OPEN_b      = lib/ladder.open_score with the frozen EXP10 constants (>= 10 home papers, >= 4 finite components)
  NOVCHURN_home = mean(zw(NOV_res_home), -zw(edge_persistence_home)), frozen home constants, both finite, >= 10 home
  NOVCHURN_home_rare = the same on the rarefied components; NOVCHURN_clean = mean(zw(NOV_res_home), -z(edge_persistence_sz))
  (edge_persistence_sz standardised with its Frame-N mean / sd: no EXP5 constant exists; declared in prereg)
Usage: python s7_freeze.py prepare|power|freeze"""
from __future__ import annotations

import json
import math
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import rankdata

from common import DATA, INPUTS, RES, ROOT, jdump, setup_logger, sha256_file

logger = setup_logger("s7_freeze")
COMP = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]


def zw(v: np.ndarray, c: dict) -> np.ndarray:
    return c["sign"] * (np.clip(v, c["lo"], c["hi"]) - c["mu"]) / c["sd"]


def indices(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    from ladder import open_score
    oc = spec["open_constants"]
    for b in ("home", "all", "sizematch"):
        df[f"OPEN_{b}"], _ = open_score(df, b, oc[b], min_home=spec["open_min_home_papers"],
                                        min_comp=spec["open_min_components"])
    h = oc["home"]
    ok_home = df.n_home_early.to_numpy() >= spec["open_min_home_papers"]

    def nov(nr, ep):
        a, b = zw(df[nr].to_numpy(float), h["NOV_res"]), zw(df[ep].to_numpy(float), h["edge_persistence"])
        v = (a + b) / 2
        v[~(np.isfinite(a) & np.isfinite(b) & ok_home)] = np.nan
        return v
    df["NOVCHURN_home"] = nov("NOV_res__home", "edge_persistence__home")
    df["NOVCHURN_home_rare"] = nov("NOV_res_rare", "edge_persistence_rare")
    sz = df.edge_persistence_sz.to_numpy(float)
    zsz = -(sz - np.nanmean(sz)) / np.nanstd(sz)
    a = zw(df.NOV_res__home.to_numpy(float), h["NOV_res"])
    v = (a + zsz) / 2
    v[~(np.isfinite(a) & np.isfinite(zsz) & ok_home)] = np.nan
    df["NOVCHURN_clean"] = v
    # Cheng measures share OPEN_home's eligibility (>= 10 home papers in t0..t0+2; >= 10 papers for the _all variant)
    for c in ("CHENG_consistency_home", "CHENG_embeddedness_home", "CHENG_prominence_home"):
        df.loc[~ok_home, c] = np.nan
    df.loc[df.n_all_early.to_numpy() < spec["open_min_home_papers"], "CHENG_consistency_all"] = np.nan
    df["window_flag"] = df.extension.astype(float)
    return df


def prepare() -> None:
    """Indices, fallback-E decision, pre-seal diagnostics -> data/analysis_features_frame_n.parquet."""
    spec = json.loads((RES / "frozen_spec_v0.json").read_text())
    df = pd.read_parquet(DATA / "features_frame_n.parquet")
    if "N_t0p2_x" in df.columns:   # S5 onset table and S6 covariates both carry N(t0+2); identical (asserted)
        assert (df.N_t0p2_x - df.N_t0p2_y).abs().max() == 0
        df = df.rename(columns={"N_t0p2_x": "N_t0p2"}).drop(columns=["N_t0p2_y"])
    df = indices(df, spec)
    gb = json.loads((RES / "gate_benchmark.json").read_text())
    f7 = gb.get("m1_m2", {}).get("kappa_type", 1.0)
    if not (f7 >= 0.4):
        df["type"] = None
        logger.info(f"F7: kappa_type {f7} < 0.4 -> type dummies dropped from R2")
    # expected primary n: logistic model of [O2r_m50 defined] on B5 + label_coverage_early fitted on EXP5
    f5 = pd.read_parquet(INPUTS / "features_exp5_open.parquet")
    X5 = f5[B5 + ["label_coverage_early"]].to_numpy(float)
    y5 = np.isfinite(f5.O2r_m50.to_numpy(float)).astype(float)
    ok = np.all(np.isfinite(X5), 1)
    from sklearn.linear_model import LogisticRegression
    mu, sd = X5[ok].mean(0), X5[ok].std(0)
    lr = LogisticRegression(C=1e4, max_iter=2000).fit((X5[ok] - mu) / sd, y5[ok])
    Xn = df[B5 + ["label_coverage_early"]].to_numpy(float)
    okn = np.all(np.isfinite(Xn), 1)
    p = np.full(len(df), np.nan)
    p[okn] = lr.predict_proba((Xn[okn] - mu) / sd)[:, 1]
    df["p_O2r_defined"] = p
    main = df.extension == 0
    fin = np.isfinite(df.OPEN_home) & np.isfinite(df.p_O2r_defined)
    n_exp_main = float(df.loc[main & fin, "p_O2r_defined"].sum())
    n_exp_all = float(df.loc[fin, "p_O2r_defined"].sum())
    use_ext = n_exp_main < 800 and (df.extension == 1).any()
    decision = {"n_gated_main": int(main.sum()), "n_gated_ext": int((~main).sum()),
                "n_open_home_finite_main": int((main & np.isfinite(df.OPEN_home)).sum()),
                "n_expected_primary_main": n_exp_main, "n_expected_primary_with_ext": n_exp_all,
                "fallback_E_triggered": bool(n_exp_main < 800), "extension_used": bool(use_ext),
                "model": "logistic [O2r_m50 defined] ~ B5 + label_coverage_early, fitted on EXP5 (TAG)"}
    if not use_ext:
        df = df[main].copy()
    logger.info(f"expected n / fallback E: {decision}")
    # ---------------- pre-seal diagnostics (outcome-free)
    diag = {"fallback_E": decision}
    smd = {}
    for c in [f"{k}__home" for k in COMP] + [f"{k}__all" for k in COMP] + B5:
        a, b = df[c].to_numpy(float), f5[c].to_numpy(float)
        a, b = a[np.isfinite(a)], b[np.isfinite(b)]
        s = math.sqrt((a.var() + b.var()) / 2) if len(a) and len(b) else math.nan
        smd[c] = {"frame_n_mean": float(a.mean()), "exp5_mean": float(b.mean()),
                  "smd": float((a.mean() - b.mean()) / s) if s else math.nan}
    diag["smd_vs_exp5"] = smd
    diag["smd_flags_gt_0.5"] = [k for k, v in smd.items() if abs(v["smd"]) > 0.5]

    def sp(x, y):
        m = np.isfinite(df[x]) & np.isfinite(df[y])
        return float(stats.spearmanr(df.loc[m, x], df.loc[m, y])[0]) if m.sum() > 10 else math.nan
    diag["coupling_check"] = {f"{x}~{y}": sp(x, y) for x in ("OPEN_home", "OPEN_all", "NOVCHURN_home")
                              for y in ("offhome_share", "logvol")}
    diag["cheng_vs_persistence_spearman"] = sp("CHENG_consistency_home", "edge_persistence__home")
    m = np.isfinite(df.ego_edges_W3_rewire_mean) & np.isfinite(df.ego_edges_W3_chunglu)
    diag["chunglu_vs_rewiring_mean_pearson"] = float(np.corrcoef(df.loc[m, "ego_edges_W3_rewire_mean"],
                                                                 df.loc[m, "ego_edges_W3_chunglu"])[0, 1])
    diag["missingness"] = {c: float(np.isnan(df[c].to_numpy(float)).mean()) for c in
                           [f"{k}__home" for k in COMP] + ["OPEN_home", "OPEN_all", "OPEN_sizematch", "NOVCHURN_home",
                                                           "CHENG_consistency_home", "CHENG_embeddedness_home",
                                                           "ego_density_W3_cz", "edge_persistence_sz",
                                                           "NOVCHURN_home_rare", "edge_persistence_excess"]}
    diag["open_home_coverage"] = float(np.isfinite(df.OPEN_home).mean())
    diag["n_analysis_frame"] = int(len(df))
    diag["by_group"] = df.agroup.value_counts().to_dict()
    diag["by_t0"] = df.t0.value_counts().sort_index().to_dict()
    jdump(diag, RES / "s7_preseal_diagnostics.json")
    out_cols = [c for c in df.columns if c.startswith(("O1", "O2", "O3", "V_next"))]
    assert not out_cols, out_cols
    df.to_parquet(DATA / "analysis_features_frame_n.parquet", index=False)
    logger.info(f"prepared analysis features: {df.shape}; OPEN_home finite {int(np.isfinite(df.OPEN_home).sum())}")


# ----------------------------------------------------------------------------- power
def _power_task(args) -> list[dict]:
    from laddern import psp_boot2
    X_R3, C_R3, X_R5, C_R5, x, yhat, sig, gamma_r, seed, n, n_boot = args
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        y = yhat + gamma_r + rng.normal(0, sig, len(yhat))
        r3 = psp_boot2(x, y, X_R3, C_R3, n_boot, int(rng.integers(1 << 30)), 1)
        r5 = psp_boot2(x, y, X_R5, C_R5, n_boot, int(rng.integers(1 << 30)), 1)
        out.append({"r3": r3["rho"], "lo3": r3["ci"][0], "se3": r3["se"], "r5": r5["rho"], "lo5": r5["ci"][0],
                    "se5": r5["se"]})
    return out


def power(n_draws: int = 300, n_boot: int = 500, target: float = 0.08, workers: int = 9) -> None:
    from laddern import rung_design
    df = pd.read_parquet(DATA / "analysis_features_frame_n.parquet")
    f5 = pd.read_parquet(INPUTS / "features_exp5_open.parquet")
    res = {"target_psp": target, "n_draws": n_draws, "n_boot": n_boot,
           "model": "y = X*beta_EXP5 + gamma*resid(rank x | Z) + eps; beta, sd(eps) from OLS of O2r_m50 on the "
                    "standardised R4 continuous covariates in EXP5; realised Frame-N design matrices; the sample is the "
                    "concepts with finite index and p(O2r_m50 defined) >= 0.5 (expected primary set)"}
    cont = B5 + ["CONTACT_REACH", "fp_logN", "fp_nfields", "label_coverage_early", "home_coverage_early"]
    ok5 = np.isfinite(f5.O2r_m50) & np.all(np.isfinite(f5[cont].to_numpy(float)), 1)
    X5 = f5.loc[ok5, cont].to_numpy(float)
    mu5, sd5 = X5.mean(0), X5.std(0)
    A5 = np.c_[np.ones(ok5.sum()), (X5 - mu5) / sd5]
    beta, *_ = np.linalg.lstsq(A5, f5.loc[ok5, "O2r_m50"].to_numpy(float), rcond=None)
    sig = float(np.std(f5.loc[ok5, "O2r_m50"].to_numpy(float) - A5 @ beta))
    for x in ("OPEN_home", "NOVCHURN_home"):
        d = df[np.isfinite(df[x]) & (df.p_O2r_defined >= 0.5)].copy()
        B3, C3 = rung_design(d, "R3")
        B5_, C5 = rung_design(d, "R5")
        okd = np.all(np.isfinite(B5_.to_numpy(float)), 1) & np.all(np.isfinite(d[cont].to_numpy(float)), 1)
        d, B3, C3, B5_, C5 = d[okd], B3[okd], C3[okd], B5_[okd], C5[okd]
        Xn = (d[cont].to_numpy(float) - mu5) / sd5
        yhat = np.c_[np.ones(len(d)), Xn] @ beta
        xv = d[x].to_numpy(float)
        Z = np.c_[np.ones(len(d)), rankdata(B5_.to_numpy(float), axis=0), C5.to_numpy(float)]
        rx = rankdata(xv) - Z @ np.linalg.lstsq(Z, rankdata(xv), rcond=None)[0]
        # residual SD of yhat's rank-unexplained part is ~ sig; gamma on the rank-residual scale
        gamma = target * sig / (rx.std() * math.sqrt(1 - target ** 2))
        per = math.ceil(n_draws / workers)
        tasks = [(B3.to_numpy(float), C3.to_numpy(float), B5_.to_numpy(float), C5.to_numpy(float), xv, yhat, sig,
                  gamma * rx, 900 + 17 * k + (0 if x == "OPEN_home" else 5000), per, n_boot) for k in range(workers)]
        with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
            rows = [r for lst in ex.map(_power_task, tasks) for r in lst][:n_draws]
        R = pd.DataFrame(rows)
        res[x] = {"n_sim_sample": int(len(d)), "mean_est_R3": float(R.r3.mean()), "mean_est_R5": float(R.r5.mean()),
                  "power_R3": float((R.lo3 > 0).mean()), "power_R5": float((R.lo5 > 0).mean()),
                  "power_joint_R3_R5": float(((R.lo3 > 0) & (R.lo5 > 0)).mean()),
                  "SE_R3": float(R.se3.mean()), "SE_R5": float(R.se5.mean()),
                  "MDE_R3_2.8SE": float(2.8 * R.se3.mean()), "MDE_R5_2.8SE": float(2.8 * R.se5.mean())}
        logger.info(f"power {x}: {res[x]}")
    jdump(res, RES / "power.json")


def freeze() -> None:
    from laddern import rung_columns_realised
    from sealn import check_sealed_untouched, freeze as do_freeze, record
    spec = json.loads((RES / "frozen_spec_v0.json").read_text())
    df = pd.read_parquet(DATA / "analysis_features_frame_n.parquet")
    pw = json.loads((RES / "power.json").read_text())
    diag = json.loads((RES / "s7_preseal_diagnostics.json").read_text())
    gb = json.loads((RES / "gate_benchmark.json").read_text())
    spec.update({
        "prereg_sha256": sha256_file(ROOT / "prereg.md"),
        "spec_v0_sha256": sha256_file(RES / "frozen_spec_v0.json"),
        "rungs_realised": rung_columns_realised(df),
        "power": pw, "fallback_E": diag["fallback_E"], "gate_benchmark": gb,
        "analysis_n": int(len(df)), "analysis_n_by_t0": df.t0.value_counts().sort_index().to_dict(),
        "sha256": {p: sha256_file(ROOT / p) for p in
                   ["data/analysis_features_frame_n.parquet", "data/features_frame_n.parquet",
                    "data/frame_n_concepts.csv", "data/frame_n_candidates.csv", "data/frame_n_onset.csv",
                    "open/early_frame.parquet", "open/passN_pre_agg.parquet", "logs/sealed_files.log"]},
        "code_sha256": {str(p.relative_to(ROOT)): sha256_file(p) for p in
                        sorted(list((ROOT / "lib").glob("*.py")) + list(ROOT.glob("s*.py")) + [ROOT / "passN.py",
                                                                                                ROOT / "passM.py"])},
        "pre_unseal_checklist": {"sealed_parts": check_sealed_untouched(),
                                 "outcome_columns_in_feature_table": [c for c in df.columns if c.startswith(
                                     ("O1", "O2", "O3", "V_next"))]},
    })
    h = do_freeze(spec)
    record("S7_power", power_OPEN_home=pw["OPEN_home"], power_NOVCHURN=pw["NOVCHURN_home"])
    logger.info(f"FROZEN: {h}")


def main() -> None:
    cmd = sys.argv[1]
    if cmd == "prepare":
        prepare()
    elif cmd == "power":
        power()
    elif cmd == "freeze":
        freeze()


if __name__ == "__main__":
    main()
