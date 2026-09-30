#!/usr/bin/env python3
"""B4: heterogeneity of OPEN on finer home-field x period sub-units (REML meta-regression, Knapp-Hartung,
permutation p, Holm), leave-one-unit-out pooling, and the LIFEENV diagnosis (variance restriction vs label
coverage vs domain boundary). Outcome O2r_m50, control set C1 (Exp8 default). EXPLORATORY.

Usage: python heterogeneity.py [--nperm 1000] [--nboot 1000]"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"          # 4-CPU box: one BLAS thread per process (the previous attempt died on thread exhaustion)

import argparse
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger
from scipy import optimize, stats
from scipy.stats import rankdata

from common import B5, COMPONENTS, HELD4, LOGS, RES, SEED, UNITS6, assert_sealed, cat_for, dl, holm, jdump

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "heterogeneity.log", rotation="30 MB", level="DEBUG")

Y = "O2r_m50"
IND = ["OPEN"] + COMPONENTS
TRAITS = ["median_label_coverage", "median_log_early_volume", "share_multi_home", "share_generic", "median_O2r_m50",
          "sd_OPEN", "mean_t0"]


# ----------------------------------------------------------------------------- GENERIC rule (frozen in spec)
def generic_flag(label: str, rule: dict) -> int:
    from wordfreq import zipf_frequency
    s = re.sub(r"\(.*?\)", " ", str(label).lower())
    toks = re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*", s)
    if not toks:
        return 0
    if len(toks) == 1 and zipf_frequency(toks[0], rule["wordfreq_lang"]) >= rule["single_token_zipf_ge"]:
        return 1
    return int(toks[-1] in set(rule["head_nouns"]))


# ----------------------------------------------------------------------------- psp with analytic variance
def psp_an(x, y, Bm, cat, w=None):
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(Bm), 1)
    x, y, Bm, cat = x[ok], y[ok], Bm[ok], cat[ok]
    n = len(x)
    if n < 20 or np.unique(x).size < 3:
        return np.nan, n, np.nan
    Z = np.hstack([np.ones((n, 1)), rankdata(Bm, axis=0), cat])
    k = np.linalg.matrix_rank(Z)
    R = np.c_[rankdata(x), rankdata(y)]
    if w is None:
        beta, *_ = np.linalg.lstsq(Z, R, rcond=None)
        E = R - Z @ beta
        r = float(np.corrcoef(E[:, 0], E[:, 1])[0, 1])
    else:
        w = w[ok]
        sw = np.sqrt(w)[:, None]
        beta, *_ = np.linalg.lstsq(Z * sw, R * sw, rcond=None)
        E = R - Z @ beta
        m = (w[:, None] * E).sum(0) / w.sum()
        E = E - m
        r = float((w * E[:, 0] * E[:, 1]).sum() / math.sqrt((w * E[:, 0] ** 2).sum() * (w * E[:, 1] ** 2).sum()))
    return r, n, 1.0 / (n - k - 3) if n - k - 3 > 0 else np.nan


# ----------------------------------------------------------------------------- REML meta-regression + KH
def reml(y, v, X):
    k, p = X.shape

    def nll(t2):
        w = 1 / (v + t2)
        XtWX = X.T @ (X * w[:, None])
        b = np.linalg.solve(XtWX, X.T @ (w * y))
        r = y - X @ b
        return 0.5 * (np.sum(np.log(v + t2)) + np.linalg.slogdet(XtWX)[1] + np.sum(w * r ** 2))
    hi = max(10 * np.var(y), 1e-4)
    res = optimize.minimize_scalar(nll, bounds=(0, hi), method="bounded", options={"xatol": 1e-10})
    t2 = float(res.x) if nll(res.x) < nll(0.0) else 0.0
    w = 1 / (v + t2)
    XtWX = X.T @ (X * w[:, None])
    Vb = np.linalg.inv(XtWX)
    b = Vb @ (X.T @ (w * y))
    r = y - X @ b
    s2 = float(np.sum(w * r ** 2) / (k - p)) if k > p else float("nan")
    Vkh = max(s2, 1e-12) * Vb      # Knapp-Hartung (untruncated s2 floored only for numerical safety)
    se = np.sqrt(np.diag(Vkh))
    tq = stats.t.ppf(0.975, k - p)
    tstat = b / se
    return {"b": b, "se": se, "ci": np.c_[b - tq * se, b + tq * se], "t": tstat,
            "p": 2 * stats.t.sf(np.abs(tstat), k - p), "tau2": t2, "resid": r, "df": k - p}


def build_subunits(H: pd.DataFrame, min_n: int) -> pd.Series:
    H = H.copy()
    H["home1"] = H.home.astype(str).str.split(";").str[0].astype(float).astype(int)
    H["period"] = np.where(H.t0 <= 2009, "2003-09", "2010-14")
    H["cell"] = H.unit + "|F" + H.home1.astype(str) + "|" + H.period
    usable = H[Y].notna() & H.OPEN.notna() & H[B5].notna().all(axis=1)
    cnt = H[usable].groupby("cell").size()
    big = set(cnt[cnt >= min_n].index)
    sub = np.where(H.cell.isin(big), H.cell, H.unit + "_other")
    s = pd.Series(sub, index=H.index)
    cnt2 = s[usable].value_counts()
    s[s.isin(cnt2[cnt2 < min_n].index)] = None
    return s


def ebal(c: np.ndarray, target_m: float, target_v: float) -> np.ndarray:
    """Entropy balancing on the first two moments of one covariate (Hainmueller 2012)."""
    X = np.c_[c - target_m, (c - target_m) ** 2 - target_v]
    sc = X.std(0)
    sc[sc == 0] = 1
    X = X / sc

    def f(l):
        e = np.exp(np.clip(X @ l, -50, 50))
        return np.log(e.sum()), X.T @ e / e.sum()
    r = optimize.minimize(lambda l: f(l)[0], np.zeros(2), jac=lambda l: f(l)[1], method="BFGS")
    w = np.exp(np.clip(X @ r.x, -50, 50))
    return w / w.sum() * len(w)


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nperm", type=int, default=1000)
    ap.add_argument("--nboot", type=int, default=1000)
    a = ap.parse_args()
    spec = assert_sealed()
    rule = spec["B4"]["generic_rule"]
    B = pd.read_parquet(RES / "b_table.parquet")
    H = B[B.unit.isin(UNITS6)].copy()
    H["GENERIC"] = [generic_flag(n, rule) for n in H.name]
    H["log_early_volume"] = np.log1p(H.early_volume.astype(float))
    rng = np.random.default_rng(SEED + 41)
    audit = H.sample(100, random_state=SEED)[["name", "GENERIC"]].to_dict("records")
    min_n = spec["B4"]["min_n"]
    H["subunit"] = build_subunits(H, min_n)
    k_sub = H.subunit.nunique()
    if k_sub < 20:
        min_n = spec["B4"]["fallback_min_n"]
        H["subunit"] = build_subunits(H, min_n)
        logger.warning(f"fewer than 20 sub-units at n>=60 -> threshold {min_n}")
    logger.info(f"sub-units: {H.subunit.nunique()} (min_n {min_n}); GENERIC share {H.GENERIC.mean():.3f}")
    # ---------------- per sub-unit psp
    rows = []
    for su, d in H[H.subunit.notna()].groupby("subunit"):
        unit = d.unit.iloc[0]
        cat = cat_for(d.t0.to_numpy(), d.group.to_numpy(), unit)
        usable = d[Y].notna() & d.OPEN.notna() & d[B5].notna().all(axis=1)
        du = d[usable]
        r = {"subunit": su, "unit": unit, "n_usable": int(usable.sum()),
             "median_label_coverage": float(du.label_coverage_early.median()),
             "median_log_early_volume": float(du.log_early_volume.median()),
             "share_multi_home": float((du.intersect40 > 0).mean()), "share_generic": float(du.GENERIC.mean()),
             "median_O2r_m50": float(du[Y].median()), "sd_OPEN": float(du.OPEN.std()), "mean_t0": float(du.t0.mean())}
        for ind in IND:
            rho, n, v = psp_an(d[ind].to_numpy(float), d[Y].to_numpy(float), d[B5].to_numpy(float), cat)
            r[f"psp_{ind}"], r[f"n_{ind}"], r[f"v_{ind}"] = rho, n, v
        rows.append(r)
    SU = pd.DataFrame(rows)
    SU.to_csv(RES / "subunit_table.csv", index=False)
    ok = SU.psp_OPEN.notna() & SU.v_OPEN.notna()
    SU = SU[ok].reset_index(drop=True)
    y = np.arctanh(SU.psp_OPEN.to_numpy())
    v = SU.v_OPEN.to_numpy()
    k = len(y)
    P_sub = dl(y, v)
    # unit-level OPEN (analytic)
    unit_rows = {}
    for u in UNITS6:
        d = H[H.unit == u]
        rho, n, vv = psp_an(d.OPEN.to_numpy(float), d[Y].to_numpy(float), d[B5].to_numpy(float),
                            cat_for(d.t0.to_numpy(), d.group.to_numpy(), u))
        unit_rows[u] = {"rho": rho, "n": n, "v": vv}
    P_u6 = dl(np.arctanh([unit_rows[u]["rho"] for u in UNITS6]), [unit_rows[u]["v"] for u in UNITS6])
    P_u4 = dl(np.arctanh([unit_rows[u]["rho"] for u in HELD4]), [unit_rows[u]["v"] for u in HELD4])
    logo = {}
    for drop in UNITS6:
        us = [u for u in UNITS6 if u != drop]
        q = dl(np.arctanh([unit_rows[u]["rho"] for u in us]), [unit_rows[u]["v"] for u in us])
        logo[drop] = {"est": q["est"], "ci": q["ci"], "I2": q["I2"]}
    # component I2 at sub-unit level
    comp_sub = {}
    for ind in IND:
        m = SU[f"psp_{ind}"].notna() & SU[f"v_{ind}"].notna()
        q = dl(np.arctanh(SU.loc[m, f"psp_{ind}"]), SU.loc[m, f"v_{ind}"])
        comp_sub[ind] = {"est": q["est"], "ci": q["ci"], "I2": q["I2"], "tau2": q["tau2"], "k": q["k"], "pi": q["pi"]}
    # ---------------- meta-regression
    X0 = np.ones((k, 1))
    m0 = reml(y, v, X0)
    tau2_0 = m0["tau2"]
    mr = {}
    for tr in TRAITS:
        x = SU[tr].to_numpy(float)
        xs = (x - x.mean()) / (x.std() if x.std() > 0 else 1)
        X = np.c_[np.ones(k), xs]
        m = reml(y, v, X)
        tobs = abs(m["t"][1])
        cnt = 0
        for _ in range(a.nperm):
            mp_ = reml(y, v, np.c_[np.ones(k), rng.permutation(xs)])
            cnt += abs(mp_["t"][1]) >= tobs
        mr[tr] = {"slope_per_sd": float(m["b"][1]), "ci": m["ci"][1].tolist(), "p_kh": float(m["p"][1]),
                  "p_perm": (cnt + 1) / (a.nperm + 1), "tau2": m["tau2"],
                  "R2_analog": max(0.0, (tau2_0 - m["tau2"]) / tau2_0) if tau2_0 > 0 else float("nan"),
                  "trait_sd": float(x.std()), "trait_mean": float(x.mean())}
    hp = holm([mr[t]["p_perm"] for t in TRAITS])
    for t, h in zip(TRAITS, hp):
        mr[t]["p_perm_holm"] = h
    top2 = sorted(TRAITS, key=lambda t: mr[t]["p_perm"])[:2]
    Xj = np.c_[np.ones(k)] 
    for t in top2:
        x = SU[t].to_numpy(float)
        Xj = np.c_[Xj, (x - x.mean()) / x.std()]
    mj = reml(y, v, Xj)
    joint = {"traits": top2, "slopes_per_sd": mj["b"][1:].tolist(), "ci": mj["ci"][1:].tolist(),
             "p_kh": mj["p"][1:].tolist(), "tau2": mj["tau2"],
             "R2_analog": max(0.0, (tau2_0 - mj["tau2"]) / tau2_0) if tau2_0 > 0 else float("nan")}
    # ---------------- LIFEENV diagnosis
    usable = H[Y].notna() & H.OPEN.notna() & H[B5].notna().all(axis=1)
    L = H[usable & (H.unit == "LIFEENV")]
    O = H[usable & (H.unit != "LIFEENV")]
    others = [u for u in UNITS6 if u != "LIFEENV"]
    P_oth = dl(np.arctanh([unit_rows[u]["rho"] for u in others]), [unit_rows[u]["v"] for u in others])
    P_oth_h3 = dl(np.arctanh([unit_rows[u]["rho"] for u in HELD4 if u != "LIFEENV"]),
                  [unit_rows[u]["v"] for u in HELD4 if u != "LIFEENV"])
    sdr = {}
    for ind in IND:
        a1, a2 = L[ind].dropna().to_numpy(), O[ind].dropna().to_numpy()
        ratio = a1.std(ddof=1) / a2.std(ddof=1)
        bs = [rng.choice(a1, len(a1)).std(ddof=1) / rng.choice(a2, len(a2)).std(ddof=1) for _ in range(a.nboot)]
        bf = stats.levene(a1, a2, center="median")
        sdr[ind] = {"sd_LIFEENV": float(a1.std(ddof=1)), "sd_others": float(a2.std(ddof=1)), "ratio": float(ratio),
                    "ci": np.percentile(bs, [2.5, 97.5]).tolist(), "brown_forsythe_W": float(bf.statistic),
                    "brown_forsythe_p": float(bf.pvalue)}
    r_L = unit_rows["LIFEENV"]["rho"]
    U = 1 / sdr["OPEN"]["ratio"]
    r_c = r_L * U / math.sqrt(1 + r_L ** 2 * (U ** 2 - 1))
    # coverage terciles (DEV cutpoints)
    D = B[B.split == "DEV"]
    cuts = np.percentile(D.label_coverage_early.dropna(), [100 / 3, 200 / 3]).tolist()
    Lall = H[H.unit == "LIFEENV"]
    terc = {}
    from rq1stats import psp_boot
    for ti, (lo, hi) in enumerate([(-np.inf, cuts[0]), (cuts[0], cuts[1]), (cuts[1], np.inf)]):
        d = Lall[(Lall.label_coverage_early > lo) & (Lall.label_coverage_early <= hi)]
        r = psp_boot(d.OPEN.to_numpy(float), d[Y].to_numpy(float), d[B5].to_numpy(float),
                     cat_for(d.t0.to_numpy(), d.group.to_numpy(), "LIFEENV"), a.nboot, SEED + 50 + ti)
        terc[f"T{ti+1}"] = {"range": [lo, hi], "n": r["n"], "rho": r["rho"], "ci": r["ci"]}
    cov_share = {"LIFEENV_by_DEV_tercile": {f"T{i+1}": float(((L.label_coverage_early > lo) & (L.label_coverage_early <= hi)).mean())
                                            for i, (lo, hi) in enumerate([(-np.inf, cuts[0]), (cuts[0], cuts[1]), (cuts[1], np.inf)])},
                 "others_by_DEV_tercile": {f"T{i+1}": float(((O.label_coverage_early > lo) & (O.label_coverage_early <= hi)).mean())
                                           for i, (lo, hi) in enumerate([(-np.inf, cuts[0]), (cuts[0], cuts[1]), (cuts[1], np.inf)])},
                 "median_LIFEENV": float(L.label_coverage_early.median()), "median_others": float(O.label_coverage_early.median())}
    # entropy balancing of LIFEENV to the others' coverage distribution
    tm, tv = float(O.label_coverage_early.mean()), float(O.label_coverage_early.var())
    catL = cat_for(L.t0.to_numpy(), L.group.to_numpy(), "LIFEENV")
    w = ebal(L.label_coverage_early.to_numpy(float), tm, tv)
    rw, _, _ = psp_an(L.OPEN.to_numpy(float), L[Y].to_numpy(float), L[B5].to_numpy(float), catL, w=w)
    bs = []
    n = len(L)
    for _ in range(a.nboot):
        i = rng.integers(0, n, n)
        Li = L.iloc[i]
        wi = ebal(Li.label_coverage_early.to_numpy(float), tm, tv)
        bs.append(psp_an(Li.OPEN.to_numpy(float), Li[Y].to_numpy(float), Li[B5].to_numpy(float), catL[i], w=wi)[0])
    bs = np.array(bs)
    eb = {"psp_reweighted": rw, "ci": np.nanpercentile(bs, [2.5, 97.5]).tolist(), "ess": float(w.sum() ** 2 / (w ** 2).sum()),
          "weighted_mean_cov": float((w * L.label_coverage_early).sum() / w.sum()), "target_mean_cov": tm,
          "psp_unweighted": r_L}
    # LIFEENV residual after the best trait
    best = top2[0]
    x = SU[best].to_numpy(float)
    mb = reml(y, v, np.c_[np.ones(k), (x - x.mean()) / x.std()])
    lm = (SU.unit == "LIFEENV").to_numpy()
    wl = 1 / (v[lm] + mb["tau2"])
    lres = {"best_trait": best, "mean_resid_z": float((wl * mb["resid"][lm]).sum() / wl.sum()),
            "se": float(math.sqrt(1 / wl.sum())), "n_subunits": int(lm.sum())}
    lres["ci"] = [lres["mean_resid_z"] - 1.96 * lres["se"], lres["mean_resid_z"] + 1.96 * lres["se"]]
    # frozen verdict
    cov_slope_ci = mr["median_label_coverage"]["ci"]
    oth_ci = P_oth["ci"]
    overlap = eb["ci"][1] >= oth_ci[0] and eb["ci"][0] <= oth_ci[1]
    cov_ok = cov_slope_ci[0] > 0 and overlap
    var_ok = sdr["OPEN"]["ci"][1] < 1 and (oth_ci[0] <= r_c <= oth_ci[1])
    verdict = "COVERAGE" if cov_ok else ("VARIANCE" if var_ok else "UNEXPLAINED")
    code = {"COVERAGE": 1, "VARIANCE": 2, "UNEXPLAINED": 3}[verdict]
    out = {"status": "EXPLORATORY (old held-out, already unsealed); ecological traits (sub-unit medians)",
           "outcome": Y, "control": "C1", "min_n": min_n, "k_subunits": k, "subunits": SU.to_dict("records"),
           "pooled_subunit": P_sub, "pooled_unit6": P_u6, "pooled_unit4": P_u4,
           "I2_unit6": P_u6["I2"], "I2_unit4": P_u4["I2"], "I2_subunit": P_sub["I2"],
           "unit_psp": unit_rows, "logo_unit6": logo, "components_subunit": comp_sub,
           "meta_regression": {"tau2_intercept_only": tau2_0, "univariate": mr, "joint_top2": joint,
                               "method": "REML + Knapp-Hartung; permutation p over trait shuffles; Holm over 7"},
           "lifeenv": {"sd_ratio": sdr, "thorndike_U": U, "psp_LIFEENV": r_L, "psp_thorndike_corrected": r_c,
                       "others_pooled_6minusL": P_oth, "others_pooled_held3": P_oth_h3,
                       "coverage_terciles_DEV_cuts": cuts, "tercile_psp": terc, "coverage_shares": cov_share,
                       "entropy_balanced": eb, "residual_after_best_trait": lres,
                       "verdict_inputs": {"coverage_slope_ci": cov_slope_ci, "reweighted_ci_overlaps_others": overlap,
                                          "sd_ratio_ci": sdr["OPEN"]["ci"], "corrected_in_others_ci": bool(oth_ci[0] <= r_c <= oth_ci[1])},
                       "verdict": verdict, "verdict_code": code},
           "generic": {"share_heldout6": float(H.GENERIC.mean()), "audit_100": audit,
                       "top_generic_examples": H[H.GENERIC == 1].name.head(30).tolist()}}
    jdump(out, RES / "heterogeneity.json")
    logger.info(f"B4: k={k}, I2 unit6 {P_u6['I2']:.2f} sub {P_sub['I2']:.2f}; top traits {top2}; LIFEENV verdict {verdict}")


if __name__ == "__main__":
    main()
