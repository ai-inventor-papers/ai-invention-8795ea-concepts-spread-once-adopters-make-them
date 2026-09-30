#!/usr/bin/env python3
"""S3 SIZE-DEPENDENCE DIAGNOSTICS (no outcomes): Spearman of every raw / clean variant with log n_home_early,
log(n_home_early / 3), growth_c and log n_all_early per body and pooled; OLS R2 of raw persistence / NOV_res / density
on log n and on [log n, 1/min_year_n, 1/mean_year_n]; Spearman of the degree-normalised z with log deg_W3;
binned raw vs V2-null-mean persistence (the key picture) and the 'thin-sample share' = R2 of raw persistence on its
own V2 null mean. -> results/size_dependence.json, figures/persistence_vs_n.png"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, DATA_IN, FIGS, RES, jdump, setup_logger

logger = setup_logger("s5_size")
VARS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
        "participation__raw", "NOVCHURN_raw", "OPEN_home",
        "NOV_res_rare5", "NOV_res_rare10", "NOV_res_rare20", "edge_persistence_rare5", "edge_persistence_rare10",
        "edge_persistence_rare20", "ego_density_W3_rare10", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_rare20",
        "NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "NOV_res_zperm", "edge_persistence_zperm",
        "NOVCHURN_exc", "NOVCHURN_zperm", "EP_chao", "NOVCHURN_chao", "z_dens_cfg", "z_dens_cfg_W1", "z_dens_k",
        "z_pers_cfg", "excess_pers_cfg", "z_pers_k", "NOVCHURN_cfg", "OPEN_home_clean", "OPEN_home_exc",
        "edge_persistence_nullmean", "NOV_res_nullmean", "ego_density_W3_nullmean"]
BINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]


def sp(x, y) -> dict:
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 20:
        return {"rho": None, "n": int(ok.sum())}
    r, p = stats.spearmanr(x[ok], y[ok])
    return {"rho": float(r), "p": float(p), "n": int(ok.sum())}


def ols_r2(y, X) -> dict:
    ok = np.isfinite(y) & np.all(np.isfinite(X), 1)
    if ok.sum() < 20:
        return {"R2": None, "n": int(ok.sum())}
    Z = np.c_[np.ones(ok.sum()), X[ok]]
    b = np.linalg.lstsq(Z, y[ok], rcond=None)[0]
    res = y[ok] - Z @ b
    return {"R2": float(1 - res.var() / y[ok].var()), "n": int(ok.sum()), "coef": b.tolist()}


def main() -> None:
    d = pd.read_parquet(DATA / "clean_variants.parquet")
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci", "growth_c", "n_all_early"])
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci", "growth_c", "n_all_early"])
    fe["frame"], ac["frame"] = "exp5", "cohort"
    d = d.merge(pd.concat([fe, ac]), on=["frame", "ci"], how="left", validate="1:1")
    ln = np.log(d.n_home_early.to_numpy(float))
    d["mean_year_n"] = (d.n_W1 + d.n_W2 + d.n_W3) / 3
    out: dict = {"n_concepts": int(len(d)), "note": "log(n/3) is a monotone transform of n, so its Spearman equals "
                                                    "that of log n (reported for completeness)", "spearman": {}}
    groups = {"POOLED": np.ones(len(d), bool), **{b: (d.body == b).to_numpy() for b in
                                                   ("DEV", "OLDHO", "COH1014", "COH1517")}}
    for v in VARS:
        if v not in d:
            continue
        x = d[v].to_numpy(float)
        out["spearman"][v] = {g: {"log_n_home_early": sp(x[m], ln[m]),
                                  "log_n_home_early_over_3": sp(x[m], np.log(d.n_home_early.to_numpy(float)[m] / 3)),
                                  "growth_c": sp(x[m], d.growth_c.to_numpy(float)[m]),
                                  "log_n_all_early": sp(x[m], np.log1p(d.n_all_early.to_numpy(float)[m]))}
                              for g, m in groups.items()}
    X1 = ln[:, None]
    with np.errstate(divide="ignore"):
        X3 = np.c_[ln, 1 / d.min_year_n.replace(0, np.nan).to_numpy(float), 1 / d.mean_year_n.to_numpy(float)]
    out["ols_r2"] = {}
    for v in ("edge_persistence__raw", "NOV_res__raw", "ego_density_W3__raw", "NOVCHURN_raw", "edge_persistence_exc",
              "NOVCHURN_exc", "z_pers_cfg", "edge_persistence_rare10"):
        y = d[v].to_numpy(float)
        out["ols_r2"][v] = {"log_n": ols_r2(y, X1), "log_n_inv_min_inv_mean": ols_r2(y, X3)}
    lg = np.log(d.deg_W3__raw.to_numpy(float))
    out["degree_dependence"] = {v: {g: sp(d[v].to_numpy(float)[m], lg[m]) for g, m in groups.items()}
                                for v in ("ego_density_W3__raw", "z_dens_cfg", "z_dens_k", "edge_persistence__raw",
                                          "z_pers_cfg", "z_pers_k")}
    # key picture: binned raw vs null-mean persistence
    tab = []
    for lo, hi in BINS:
        m = (d.n_home_early >= lo) & (d.n_home_early <= hi)
        s = d[m]
        tab.append({"bin": f"{lo}-{hi if hi < 10**9 else 'inf'}", "n": int(m.sum()),
                    "raw_mean": float(s.edge_persistence__raw.mean()),
                    "v2_null_mean": float(s.edge_persistence_nullmean.mean()),
                    "excess_mean": float(s.edge_persistence_exc.mean()),
                    "rare10_mean": float(s.edge_persistence_rare10.mean()),
                    "curveball_null_mean": float(s.pers_cfg_mean.mean()),
                    "raw_NOV_res_mean": float(s.NOV_res__raw.mean()),
                    "null_NOV_res_mean": float(s.NOV_res_nullmean.mean())})
    out["binned_persistence"] = tab
    y = d.edge_persistence__raw.to_numpy(float)
    out["thin_sample_share"] = {
        "definition": "R2 of raw edge_persistence on its own V2 (year-label permutation) null mean",
        "POOLED": ols_r2(y, d.edge_persistence_nullmean.to_numpy(float)[:, None]),
        **{b: ols_r2(y[m], d.edge_persistence_nullmean.to_numpy(float)[m][:, None]) for b, m in groups.items()
           if b != "POOLED"}}
    yN = d.NOV_res__raw.to_numpy(float)
    out["thin_sample_share_NOV_res"] = {"POOLED": ols_r2(yN, d.NOV_res_nullmean.to_numpy(float)[:, None])}
    jdump(out, RES / "size_dependence.json")
    logger.info(f"thin-sample share (R2 raw EP ~ V2 null mean) pooled: {out['thin_sample_share']['POOLED']['R2']:.3f}")
    for r in tab:
        logger.info(r)
    # figure
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    xs = np.arange(len(tab))
    lab = [r["bin"] for r in tab]
    ax[0].plot(xs, [r["raw_mean"] for r in tab], "o-", label="raw edge persistence")
    ax[0].plot(xs, [r["v2_null_mean"] for r in tab], "s--", label="V2 null mean (year labels permuted)")
    ax[0].plot(xs, [r["rare10_mean"] for r in tab], "^-", label="V1 rarefied (n = 10 / year)")
    ax[0].plot(xs, [r["curveball_null_mean"] for r in tab], "d:", label="V3c curveball null mean")
    ax[0].set_xticks(xs, lab)
    ax[0].set_xlabel("home papers t0..t0+2 (n_home_early bin)")
    ax[0].set_ylabel("mean Jaccard persistence")
    ax[0].legend(fontsize=8)
    ax[0].set_title("Persistence and its sampling null by sample size")
    ok = np.isfinite(y) & np.isfinite(d.edge_persistence_nullmean)
    ax[1].scatter(d.edge_persistence_nullmean[ok], y[ok], s=3, alpha=0.25)
    lim = [0, max(0.8, float(np.nanmax(y)))]
    ax[1].plot(lim, lim, "k--", lw=0.8)
    ax[1].set_xlabel("V2 null mean persistence (same papers, years shuffled)")
    ax[1].set_ylabel("observed raw persistence")
    ax[1].set_title(f"thin-sample share R2 = {out['thin_sample_share']['POOLED']['R2']:.2f} (n = {int(ok.sum())})")
    fig.tight_layout()
    fig.savefig(FIGS / "persistence_vs_n.png", dpi=150)
    logger.info("wrote figures/persistence_vs_n.png")


if __name__ == "__main__":
    main()
