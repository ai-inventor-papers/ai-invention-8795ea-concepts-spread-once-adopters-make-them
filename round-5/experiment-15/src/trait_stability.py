#!/usr/bin/env python3
"""iter-5 STEP 8 (Part B): is HOME openness a stable concept trait?

Yearly: Exp11 yearly_features (HOME-ONLY, 1-year windows), rows t0..h_end with deg >= 2.
  OPEN_home_y  = panel_m.open_home with the Exp11 frozen yearly z constants (>= 4 of 6 signed z-scores)
  NOVCHURN_y   = mean(z nov_res, -z persistence), same constants, both finite
  log1p_home_works = positive control (a known stable size trait)
Per body (DEV, OLD_HELDOUT, COHORT_2010_14) and per group:
  ICC(1): one-way random-effects ANOVA estimator on x residualised on year + age dummies,
          k0 = (N - sum n_i^2 / N) / (g - 1); concept bootstrap (500); MixedLM REML cross-check (point)
  ICC size-adjusted: residualised also on log1p_deg, log1p_home_works, log1p_all_works
  test-retest: Spearman(mean x over t0..t0+2, mean x over t0+3..t0+5), >= 2 defined years each; partial given early
          log volume and mean log degree (early and later); bootstrap CI (500)
  lag-1 within-concept autocorrelation of demeaned residuals (Nickell-biased; first-difference correlation beside it)
  reliability: Spearman-Brown odd/even-year means; ICC-implied reliability of a 3-year mean; disattenuated retest
  FE power link: within-SD / total-SD and the H-M2 MDE implied by the within SD
  sensitivity: deg >= 5 rows
Static: Exp10 early HOME build (t0..t0+2) vs the same build on t0+3..t0+5 (partners_home.py --frame retest).
Verdict (hashed prediction P-B1): TRAIT SUPPORTED iff ICC >= 0.40 and early-later rho >= 0.40 for OPEN_home on DEV
AND OLD_HELDOUT. Writes results/trait_stability.json, figures/trait_scatter.png."""
from __future__ import annotations

import argparse
import json
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib_iter5"))

import numpy as np
import pandas as pd
from scipy import stats

from common_iter5 import DATA, E5, E10, E11, FIGS, HELD, RES, SEED, jdump, setup_logger

warnings.filterwarnings("ignore")
VARS = ["OPEN_home", "NOVCHURN", "log1p_home_works"]


def resid(x: np.ndarray, Z: np.ndarray) -> np.ndarray:
    b, *_ = np.linalg.lstsq(Z, x, rcond=None)
    return x - Z @ b


def dummies(v: np.ndarray) -> np.ndarray:
    u = np.unique(v)
    return (v[:, None] == u[1:][None, :]).astype(float)


def icc1(x: np.ndarray, g: np.ndarray) -> float:
    """One-way random-effects ICC(1), ANOVA estimator for unbalanced groups (groups with >= 2 rows)."""
    _, inv, cnt = np.unique(g, return_inverse=True, return_counts=True)
    keep = cnt[inv] >= 2
    x, g = x[keep], g[keep]
    _, inv, n = np.unique(g, return_inverse=True, return_counts=True)
    G, N = len(n), len(x)
    if G < 3:
        return float("nan")
    m = np.bincount(inv, weights=x) / n
    gm = x.mean()
    msb = (n * (m - gm) ** 2).sum() / (G - 1)
    msw = ((x - m[inv]) ** 2).sum() / (N - G)
    k0 = (N - (n ** 2).sum() / N) / (G - 1)
    return float((msb - msw) / (msb + (k0 - 1) * msw))


def design_Z(d: pd.DataFrame, size_adj: bool) -> np.ndarray:
    parts = [np.ones((len(d), 1)), dummies(d.year.to_numpy()), dummies(d.age.to_numpy())]
    if size_adj:
        parts.append(d[["log1p_deg", "log1p_home_works", "log1p_all_works"]].to_numpy(float))
    return np.hstack(parts)


def icc_block(d: pd.DataFrame, v: str, size_adj: bool, n_boot: int, seed: int) -> dict:
    d = d[np.isfinite(d[v])]
    x = resid(d[v].to_numpy(float), design_Z(d, size_adj))
    g = d.ci.to_numpy()
    est = icc1(x, g)
    ids, inv = np.unique(g, return_inverse=True)
    order = np.argsort(inv, kind="stable")
    starts = np.r_[0, np.cumsum(np.bincount(inv))]
    rng = np.random.default_rng(seed)
    Zfull = design_Z(d, size_adj)
    bs = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(ids), len(ids))
        rows = np.concatenate([order[starts[p]:starts[p + 1]] for p in pick])
        newg = np.repeat(np.arange(len(pick)), [starts[p + 1] - starts[p] for p in pick])
        xr = resid(d[v].to_numpy(float)[rows], Zfull[rows])
        bs.append(icc1(xr, newg))
    bs = np.array(bs)
    bs = bs[np.isfinite(bs)]
    return {"icc": est, "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) > 10 else None,
            "n_rows": int(len(d)), "n_concepts": int(len(ids)),
            "mean_rows_per_concept": float(len(d) / max(len(ids), 1)), "n_boot": int(len(bs))}


def mixedlm_icc(d: pd.DataFrame, v: str) -> dict:
    import statsmodels.formula.api as smf
    d = d[np.isfinite(d[v])].copy()
    # year + age dummies are swept out by OLS first (the joint dummy design is singular for MixedLM's Hessian);
    # the REML variance components are then estimated on the residuals with a random concept intercept
    d["x"] = resid(d[v].to_numpy(float), design_Z(d, False))
    d = d[["ci", "x"]]
    try:
        m = smf.mixedlm("x ~ 1", d, groups=d["ci"]).fit(reml=True, method="bfgs", maxiter=500)
        tau2, s2 = float(m.cov_re.iloc[0, 0]), float(m.scale)
        return {"icc_reml": tau2 / (tau2 + s2), "tau2": tau2, "sigma2": s2, "converged": bool(m.converged)}
    except (np.linalg.LinAlgError, ValueError) as e:
        return {"error": repr(e)[:200]}


def window_means(d: pd.DataFrame, v: str) -> pd.DataFrame:
    e = d[(d.year >= d.t0) & (d.year <= d.t0 + 2) & np.isfinite(d[v])]
    l_ = d[(d.year >= d.t0 + 3) & (d.year <= d.t0 + 5) & np.isfinite(d[v])]
    ge, gl = e.groupby("ci"), l_.groupby("ci")
    out = pd.DataFrame({"early": ge[v].mean(), "n_e": ge[v].size(), "late": gl[v].mean(), "n_l": gl[v].size(),
                        "logvol_e": ge.log1p_home_works.mean(), "logdeg_e": ge.log1p_deg.mean(),
                        "logdeg_l": gl.log1p_deg.mean()}).dropna()
    return out[(out.n_e >= 2) & (out.n_l >= 2)]


def retest(d: pd.DataFrame, v: str, n_boot: int, seed: int) -> dict:
    from rq1stats import psp_point
    w = window_means(d, v)
    if len(w) < 30:
        return {"n": int(len(w)), "note": "too few"}
    a, b = w.early.to_numpy(), w.late.to_numpy()
    Bm = w[["logvol_e", "logdeg_e", "logdeg_l"]].to_numpy(float)
    rho = float(stats.spearmanr(a, b)[0])
    prho = psp_point(a, b, Bm, None)
    rng = np.random.default_rng(seed)
    bs, bp = [], []
    for _ in range(n_boot):
        i = rng.integers(0, len(a), len(a))
        bs.append(stats.spearmanr(a[i], b[i])[0])
        bp.append(psp_point(a[i], b[i], Bm[i], None))
    return {"n": int(len(w)), "rho": rho, "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "partial_rho_given_size": prho, "partial_ci": [float(np.percentile(bp, 2.5)), float(np.percentile(bp, 97.5))],
            "mean_years_early": float(w.n_e.mean()), "mean_years_later": float(w.n_l.mean())}


def autocorr(d: pd.DataFrame, v: str) -> dict:
    d = d[np.isfinite(d[v])].sort_values(["ci", "year"]).copy()
    d["r"] = resid(d[v].to_numpy(float), design_Z(d, False))
    d["dm"] = d.r - d.groupby("ci").r.transform("mean")
    d["lag_dm"] = d.groupby("ci").dm.shift(1)
    d["lag_year"] = d.groupby("ci").year.shift(1)
    c = d[(d.year - d.lag_year) == 1]
    d["dx"] = d.groupby("ci").r.diff()
    d["lag_dx"] = d.groupby("ci").dx.shift(1)
    d["lag2_year"] = d.groupby("ci").year.shift(2)
    f = d[((d.year - d.lag2_year) == 2) & d.dx.notna() & d.lag_dx.notna()]
    Tbar = d.groupby("ci").size().mean()
    return {"lag1_within_demeaned": float(np.corrcoef(c.dm, c.lag_dm)[0, 1]) if len(c) > 30 else None,
            "n_pairs": int(len(c)), "nickell_bias_approx": float(-1 / (Tbar - 1)) if Tbar > 1 else None,
            "first_difference_corr": float(np.corrcoef(f.dx, f.lag_dx)[0, 1]) if len(f) > 30 else None,
            "note": "first-difference corr = -0.5 under pure year-to-year noise around a stable level"}


def odd_even(d: pd.DataFrame, v: str) -> dict:
    d = d[np.isfinite(d[v])].copy()
    d["r"] = resid(d[v].to_numpy(float), design_Z(d, False))
    d["odd"] = (d.year - d.t0) % 2
    p = d.pivot_table(index="ci", columns="odd", values="r", aggfunc="mean").dropna()
    if len(p) < 30:
        return {"n": int(len(p))}
    r = float(stats.spearmanr(p[0], p[1])[0])
    return {"n": int(len(p)), "r_odd_even": r, "spearman_brown": 2 * r / (1 + r)}


def build_yearly(logger) -> tuple[pd.DataFrame, dict]:
    sys.path.insert(0, str(Path(__file__).resolve().parent / "exp11_code" / "lib"))
    from panel_m import frame_plus, open_home
    spec = json.loads((E11 / "results/frozen_spec.json").read_text())
    zc = spec["features"]["z_constants"]
    fr = frame_plus(pd.read_csv(E5 / "frame_concepts.csv").assign(
        split=lambda f: np.where(f.split.str.startswith("HELDOUT"), "HELDOUT", f.split)))
    fr["body"] = fr.split.map({"DEV": "DEV", "COHORT": "COHORT_2010_14"}).fillna("OLD_HELDOUT")
    yf = pd.read_parquet(E11 / "data/yearly_features.parquet")
    d = yf.merge(fr[["ci", "t0", "h_end", "body", "group"]], on="ci")
    d = d[(d.year >= d.t0) & (d.year <= d.h_end) & (d.deg >= 2)].copy()
    d["OPEN_home"] = open_home(d, zc)
    zn = (d.nov_res - zc["nov_res"]["mean"]) / zc["nov_res"]["sd"]
    zp = -(d.persistence - zc["persistence"]["mean"]) / zc["persistence"]["sd"]
    d["NOVCHURN"] = np.where(np.isfinite(zn) & np.isfinite(zp), (zn + zp) / 2, np.nan)
    d["log1p_home_works"] = np.log1p(d.n_home_works)
    d["log1p_all_works"] = np.log1p(d.n_all_works)
    d["log1p_deg"] = np.log1p(d.deg)
    logger.info(f"yearly panel {d.shape}; concepts {d.ci.nunique()}")
    return d, zc


def static_retest(logger) -> dict:
    from ladder import open_score
    from rq1stats import psp_point
    e10 = json.loads((E10 / "results/frozen_spec.json").read_text())
    hc = e10["open_constants"]["home"]
    early = pd.read_parquet(E10 / "data/features_exp5_open.parquet")
    late = pd.read_parquet(DATA / "partner_home_components_retest.parquet")
    L = late.rename(columns={c: c.replace("__later", "__home") for c in late.columns})
    L["n_home_early"] = L.n_home_later
    L["OPEN_home_later"], _ = open_score(L, "home", hc)
    k = {"NOV_res": hc["NOV_res"], "edge_persistence": hc["edge_persistence"]}

    def nc(df: pd.DataFrame, nh: str) -> np.ndarray:
        a, b = k["NOV_res"], k["edge_persistence"]
        zn = a["sign"] * (np.clip(df.NOV_res__home, a["lo"], a["hi"]) - a["mu"]) / a["sd"]
        ze = b["sign"] * (np.clip(df.edge_persistence__home, b["lo"], b["hi"]) - b["mu"]) / b["sd"]
        o = ((zn + ze) / 2).to_numpy(float)
        o[df[nh].to_numpy() < 10] = np.nan
        return o
    early["NOVCHURN_early"] = nc(early, "n_home_early")
    L["NOVCHURN_later"] = nc(L, "n_home_later")
    D = early[["ci", "split", "group", "OPEN_home", "NOVCHURN_early", "n_home_early"]].merge(
        L[["ci", "OPEN_home_later", "NOVCHURN_later", "n_home_later"]], on="ci")
    D["body"] = np.where(D.split == "DEV", "DEV", np.where(D.split == "COHORT", "COHORT_2010_14", "OLD_HELDOUT"))
    out = {"n_concepts": int(len(D))}
    rng = np.random.default_rng(SEED)
    for b in ("DEV", "OLD_HELDOUT", "COHORT_2010_14", "ALL"):
        dd = D if b == "ALL" else D[D.body == b]
        out[b] = {}
        for nm, a_, b_ in (("OPEN_home", "OPEN_home", "OPEN_home_later"), ("NOVCHURN", "NOVCHURN_early", "NOVCHURN_later")):
            s = dd[[a_, b_, "n_home_early", "n_home_later"]].dropna()
            if len(s) < 30:
                out[b][nm] = {"n": int(len(s))}
                continue
            x, y = s[a_].to_numpy(float), s[b_].to_numpy(float)
            Bm = np.log1p(s[["n_home_early", "n_home_later"]].to_numpy(float))
            bs = []
            for _ in range(500):
                i = rng.integers(0, len(x), len(x))
                bs.append(stats.spearmanr(x[i], y[i])[0])
            out[b][nm] = {"n": int(len(s)), "rho": float(stats.spearmanr(x, y)[0]),
                          "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                          "partial_rho_given_log_home_volumes": psp_point(x, y, Bm, None)}
    logger.info(f"static retest: { {b: {k_: v.get('rho') for k_, v in out[b].items()} for b in ('DEV', 'OLD_HELDOUT')} }")
    return out, D


def scatter(d: pd.DataFrame, D: pd.DataFrame) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(1, 3, figsize=(13, 4))
    for a, v in zip(axs[:2], ("OPEN_home", "NOVCHURN")):
        w = window_means(d[d.body.isin(["DEV", "OLD_HELDOUT"])], v)
        a.scatter(w.early, w.late, s=3, alpha=0.3)
        a.set_xlabel(f"{v}: mean of yearly values t0..t0+2")
        a.set_ylabel("mean of yearly values t0+3..t0+5")
        a.set_title(f"yearly windows, rho={stats.spearmanr(w.early, w.late)[0]:.2f} (n={len(w)})", fontsize=9)
    s = D[["OPEN_home", "OPEN_home_later"]].dropna()
    axs[2].scatter(s.OPEN_home, s.OPEN_home_later, s=3, alpha=0.3, color="#ff7f0e")
    axs[2].set_xlabel("static OPEN_home t0..t0+2")
    axs[2].set_ylabel("static OPEN_home t0+3..t0+5")
    axs[2].set_title(f"static 3-year build, rho={stats.spearmanr(s.iloc[:, 0], s.iloc[:, 1])[0]:.2f} (n={len(s)})", fontsize=9)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"trait_scatter.{ext}", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-boot", type=int, default=500)
    ap.add_argument("--no-mixedlm", action="store_true")
    args = ap.parse_args()
    logger = setup_logger("trait_stability")
    t0 = time.time()
    from seal_iter5 import check
    seal = check()
    d, zc = build_yearly(logger)
    fe_path = Path(__file__).resolve().parent / "exp11_code/results/fe_results_completed.json"
    fe = json.loads(fe_path.read_text()) if fe_path.exists() else None
    if fe and "COHORT" in fe:
        fe["COHORT_2010_14"] = fe["COHORT"]
    out: dict = {"seal": seal, "status": "trait-stability test of the prediction P-B1/P-B2 hashed in frozen_spec_iter5",
                 "yearly_constants": "Exp11 frozen_spec features.z_constants", "bodies": {}}
    units = [("DEV", d[d.body == "DEV"]), ("OLD_HELDOUT", d[d.body == "OLD_HELDOUT"]),
             ("COHORT_2010_14", d[d.body == "COHORT_2010_14"])]
    units += [(f"group_{g}", d[d.group == g]) for g in ["CS", "Eng", "BGM", "Med"] + HELD]
    for ui, (u, du) in enumerate(units):
        r = {}
        main_body = not u.startswith("group_")
        for vi, v in enumerate(VARS):
            nb = args.n_boot if main_body else 100
            e = {"icc_raw": icc_block(du, v, False, nb, SEED + 10 * ui + vi),
                 "icc_size_adj": icc_block(du, v, True, nb, SEED + 10 * ui + vi + 5)}
            if main_body:
                e["icc_raw_deg_ge5"] = icc_block(du[du.deg >= 5], v, False, 200, SEED + 3)
                e["test_retest"] = retest(du, v, nb, SEED + 11)
                e["test_retest_deg_ge5"] = retest(du[du.deg >= 5], v, 200, SEED + 12)
                e["autocorr"] = autocorr(du, v)
                e["odd_even"] = odd_even(du, v)
                x = du[v].to_numpy(float)
                ok = np.isfinite(x)
                wsd = float(np.std(x[ok] - du[ok].groupby("ci")[v].transform("mean").to_numpy(), ddof=1))
                e["within_sd"], e["total_sd"] = wsd, float(np.std(x[ok], ddof=1))
                e["within_over_total_sd"] = wsd / e["total_sd"]
                icc_ = e["icc_raw"]["icc"]
                kk = e["test_retest"].get("mean_years_early", 3.0) if isinstance(e["test_retest"], dict) else 3.0
                rel = kk * icc_ / (1 + (kk - 1) * icc_) if np.isfinite(icc_) and icc_ > 0 else float("nan")
                e["reliability_3yr_mean_from_icc"] = rel
                tr = e["test_retest"].get("rho") if isinstance(e["test_retest"], dict) else None
                e["disattenuated_retest"] = float(tr / rel) if tr is not None and np.isfinite(rel) and rel > 0 else None
                if not args.no_mixedlm and v != "log1p_home_works":
                    e["mixedlm_reml"] = mixedlm_icc(du, v)
            r[v] = e
        if main_body and fe and u in fe and "H_M2_open" in fe[u]:
            h = fe[u]["H_M2_open"]
            r["fe_power_link"] = {"H_M2_se_per_unit_OPEN": h["se"], "sd_within_x_panel": h["sd_within_x"],
                                  "MDE_80pct_per_within_sd": 2.8 * h["se"] * h["sd_within_x"],
                                  "MDE_pct_change_entries_per_within_sd": 100 * (np.exp(2.8 * h["se"] * h["sd_within_x"]) - 1)}
        out["bodies"][u] = r
        logger.info(f"{u}: ICC OPEN {r['OPEN_home']['icc_raw']['icc']:.3f} NOVCHURN {r['NOVCHURN']['icc_raw']['icc']:.3f} "
                    f"size {r['log1p_home_works']['icc_raw']['icc']:.3f}")
        jdump(out, RES / "trait_stability.json")
    st, D = static_retest(logger)
    out["static_retest"] = st
    B = out["bodies"]
    ver = {}
    for v in ("OPEN_home", "NOVCHURN"):
        cond = {b: {"icc": B[b][v]["icc_raw"]["icc"], "retest_rho": B[b][v]["test_retest"].get("rho"),
                    "icc_size_adj": B[b][v]["icc_size_adj"]["icc"],
                    "static_retest_rho": st[b][v].get("rho"),
                    "disattenuated_retest": B[b][v].get("disattenuated_retest")} for b in ("DEV", "OLD_HELDOUT")}
        holds = all((c["icc"] or 0) >= 0.40 and (c["retest_rho"] or 0) >= 0.40 for c in cond.values())
        ver[v] = {"conditions": cond, "TRAIT_SUPPORTED": bool(holds)}
    out["verdict"] = {"P-B1_OPEN_home": ver["OPEN_home"], "P-B2_NOVCHURN": ver["NOVCHURN"],
                      "positive_control_icc_log1p_home_works": {b: B[b]["log1p_home_works"]["icc_raw"]["icc"]
                                                                for b in ("DEV", "OLD_HELDOUT", "COHORT_2010_14")},
                      "rule": "TRAIT SUPPORTED iff ICC >= 0.40 and yearly-window early-later Spearman >= 0.40 on DEV AND "
                              "OLD_HELDOUT"}
    out["seconds"] = time.time() - t0
    jdump(out, RES / "trait_stability.json")
    scatter(d, D)
    logger.info(f"trait stability done in {(time.time()-t0)/60:.1f} min: {out['verdict']}")


if __name__ == "__main__":
    main()
