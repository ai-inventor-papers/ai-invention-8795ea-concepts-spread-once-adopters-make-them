"""S3 (test A, Cheng replication panel) and S5 (test C, within-panel reach vs depth).

Test A: EXP5 concept-years t0+1 <= t <= min(t0+10, 2021) with finite CONS_b(t) (b = HOME / ALL).
  A1    fepois V(t+1) ~ zCONS + zEMB + zSOC | age + year          (Cheng's spec; CRV1 by concept)
  A1c   fepois V(t+1) ~ zCONS | age + year                        (CONS-only variant, all CONS rows)
  A1-NB statsmodels NB2 with age + year dummies (cluster-robust by concept)
  A2    A1 + log1p V(t);  A3  A2 | ci + year
  RATIO b_A2 / b_A1 on CONS, 500-draw concept-cluster bootstrap, same draws for A1 and A2 (numpy Poisson IRLS with
        age/year dummies, validated against pyfixest on the point estimate)
Test C: Exp11 yearly_panel estimation sample (at_risk_next > 0, deg >= 2), finite CONS_home(t).
  C1 fepois entries(t+1) ~ zCONS_home(t) + log1p_home + log1p_all + log1p_deg + log_at_risk | ci + year
  C2 feols dHomeShare(t+1) ~ same | ci + year
  500-draw concept-cluster bootstrap (duplicated concepts relabelled as new FE units)."""
from __future__ import annotations

import math
import multiprocessing as mp
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy import stats

from common import (DATA, EXP5, EXP11, GROUP5, GROUPS5, N_BOOT_PANEL, RES, SEED, SELECTION_LABEL, add_deviation,
                    body_of_split, home_codes, jdump, n_workers)
from rq1stats import dersimonian_laird

XS_JOINT = ["zCONS", "zEMB", "zSOC"]


# ----------------------------------------------------------------------------- data
def panel_A(build: str) -> pd.DataFrame:
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "t0", "group", "split"])
    fr["body"] = fr.split.map(body_of_split)
    fr["group5"] = fr.group.map(GROUP5)
    f = pd.read_parquet(DATA / "cheng_features.parquet")
    f = f[(f.body_src == "EXP5") & (f.build == build)][["ci", "year", "CONS", "EMB", "SOC", "n_papers", "n_topics"]]
    V = pd.read_parquet(DATA / "V_exp5.parquet", columns=["ci", "year", "V"])
    d = f.merge(fr, on="ci")
    d = d[(d.year >= d.t0 + 1) & (d.year <= np.minimum(d.t0 + 10, 2021))]
    d = d.merge(V, on=["ci", "year"], how="left").merge(
        V.assign(year=V.year - 1).rename(columns={"V": "V_next"}), on=["ci", "year"], how="left")
    d = d[np.isfinite(d.CONS)].copy()
    d["age"] = d.year - d.t0
    d["logV"] = np.log1p(d.V)
    return d.reset_index(drop=True)


def zcols(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    d = d.copy()
    for c in cols:
        v = d[c].to_numpy(float)
        d["z" + c] = (v - np.nanmean(v)) / np.nanstd(v)
    return d


# ----------------------------------------------------------------------------- numpy Poisson IRLS (dummies FE)
def dummy_design(d: pd.DataFrame, xs: list[str], fe: list[str]) -> tuple[np.ndarray, list[str]]:
    cols = [np.ones(len(d))]
    names = ["_const"]
    for c in xs:
        cols.append(d[c].to_numpy(float))
        names.append(c)
    for f in fe:
        v = d[f].to_numpy()
        for u in np.unique(v)[1:]:
            cols.append((v == u).astype(float))
            names.append(f"{f}={u}")
    return np.column_stack(cols), names


def poisson_irls(X: np.ndarray, y: np.ndarray, iters: int = 100, tol: float = 1e-10) -> np.ndarray:
    mu = y.mean() + 0.1
    b = np.zeros(X.shape[1])
    b[0] = math.log(mu)
    eta = X @ b
    for _ in range(iters):
        mu = np.exp(np.clip(eta, -30, 30))
        z = eta + (y - mu) / mu
        XtW = X.T * mu
        H = XtW @ X
        try:
            bn = np.linalg.solve(H, XtW @ z)
        except np.linalg.LinAlgError:
            bn = np.linalg.lstsq(H, XtW @ z, rcond=None)[0]
        if np.max(np.abs(bn - b)) < tol:
            b = bn
            break
        b = bn
        eta = X @ b
    return b


def _boot_ratio_worker(args) -> list[tuple[float, float]]:
    X1, X2, y, cl_idx, seeds = args
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        pick = rng.integers(0, len(cl_idx), len(cl_idx))
        rows = np.concatenate([cl_idx[p] for p in pick])
        b1 = poisson_irls(X1[rows], y[rows])[1]
        b2 = poisson_irls(X2[rows], y[rows])[1]
        out.append((b1, b2))
    return out


def cluster_index(ci: np.ndarray) -> list[np.ndarray]:
    order = np.argsort(ci, kind="stable")
    u, start = np.unique(ci[order], return_index=True)
    return np.split(order, start[1:])


def boot_ratio(d: pd.DataFrame, xs: list[str], n_boot: int, seed: int, workers: int) -> dict:
    """Cluster bootstrap of b_A1 and b_A2 on the first regressor (zCONS), same draws."""
    X1, _ = dummy_design(d, xs, ["age", "year"])
    X2, _ = dummy_design(d, xs + ["logV"], ["age", "year"])
    y = d.V_next.to_numpy(float)
    cl = cluster_index(d.ci.to_numpy())
    b1p, b2p = poisson_irls(X1, y)[1], poisson_irls(X2, y)[1]
    seeds = [seed + k for k in range(n_boot)]
    parts = [seeds[i::workers] for i in range(workers)]
    res = []
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
            for r in ex.map(_boot_ratio_worker, [(X1, X2, y, cl, p) for p in parts]):
                res.extend(r)
    else:
        res = _boot_ratio_worker((X1, X2, y, cl, seeds))
    B = np.array(res)
    ratio = B[:, 1] / B[:, 0]
    pr = b2p / b1p
    return {"b_A1_irls": b1p, "b_A2_irls": b2p, "ratio": pr,
            "ratio_ci": np.percentile(ratio, [2.5, 97.5]).tolist(), "ratio_boot_median": float(np.median(ratio)),
            "b_A1_ci_boot": np.percentile(B[:, 0], [2.5, 97.5]).tolist(),
            "b_A2_ci_boot": np.percentile(B[:, 1], [2.5, 97.5]).tolist(),
            "p_one_ratio_lt_0.5": float((np.sum(ratio >= 0.5) + 1) / (len(ratio) + 1)),
            "p_one_A1_gt_0": float((np.sum(B[:, 0] <= 0) + 1) / (len(B) + 1)),
            "n_boot": int(len(B)), "resampling_unit": "concept (cluster bootstrap)", "boot_b": B}


# ----------------------------------------------------------------------------- pyfixest wrappers
def fepois(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:
    import pyfixest as pf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = pf.fepois(f"{y} ~ {' + '.join(xs)} | {fe}", data=d, vcov={"CRV1": "ci"})
    return summarize(fit, xs, d)


def feols(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:
    import pyfixest as pf
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fit = pf.feols(f"{y} ~ {' + '.join(xs)} | {fe}", data=d, vcov={"CRV1": "ci"})
    return summarize(fit, xs, d)


def summarize(fit, xs: list[str], d: pd.DataFrame) -> dict:
    co, se, pv = fit.coef(), fit.se(), fit.pvalue()
    ci = fit.confint()
    out = {"n_rows": int(fit._N), "n_concepts": int(d.ci.nunique()), "coef": {}}
    for x in xs:
        if x not in co.index:
            continue
        b = float(co[x])
        out["coef"][x] = {"b": b, "se": float(se[x]), "ci": [float(ci.loc[x].iloc[0]), float(ci.loc[x].iloc[1])],
                          "p": float(pv[x]), "pct_per_sd": math.exp(b) - 1,
                          "pct_ci": [math.exp(float(ci.loc[x].iloc[0])) - 1, math.exp(float(ci.loc[x].iloc[1])) - 1]}
    return out


def nb_fit(d: pd.DataFrame, xs: list[str]) -> dict:
    import statsmodels.api as sm
    X, names = dummy_design(d, xs, ["age", "year"])
    y = d.V_next.to_numpy(float)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        m = sm.NegativeBinomial(y, X, loglike_method="nb2")
        try:
            r = m.fit(disp=0, maxiter=300, method="bfgs", cov_type="cluster", cov_kwds={"groups": d.ci.to_numpy()})
            how = "bfgs"
        except np.linalg.LinAlgError:
            # retry: Newton from the Poisson IRLS solution and alpha = 0.5
            sp0 = np.r_[poisson_irls(X, y), 0.5]
            r = m.fit(start_params=sp0, disp=0, maxiter=100, method="newton", cov_type="cluster",
                      cov_kwds={"groups": d.ci.to_numpy()})
            how = "newton (retry after singular bfgs)"
    out = {"n_rows": int(len(y)), "alpha": float(r.params[-1]), "converged": bool(r.mle_retvals.get("converged", True)),
           "optimizer": how, "coef": {}}
    for i, nm in enumerate(names):
        if nm in xs:
            b, s = float(r.params[i]), float(r.bse[i])
            out["coef"][nm] = {"b": b, "se": s, "ci": [b - 1.96 * s, b + 1.96 * s], "pct_per_sd": math.exp(b) - 1,
                               "p": float(2 * stats.norm.sf(abs(b / s)))}
    return out


# ----------------------------------------------------------------------------- test A
def fit_A_set(d: pd.DataFrame, xs: list[str], with_A3: bool = True, with_nb: bool = False) -> dict:
    out = {"A1": fepois(d, "V_next", xs, "age + year"),
           "A2": fepois(d, "V_next", xs + ["logV"], "age + year")}
    if with_A3:
        out["A3"] = fepois(d, "V_next", xs + ["logV"], "ci + year")
    if with_nb:
        try:
            out["A1_NB"] = nb_fit(d, xs)
        except (ValueError, np.linalg.LinAlgError) as e:
            out["A1_NB"] = {"error": repr(e)[:300]}
    b1 = out["A1"]["coef"].get("zCONS", {}).get("b", np.nan)
    b2 = out["A2"]["coef"].get("zCONS", {}).get("b", np.nan)
    out["ratio_point"] = b2 / b1 if b1 else float("nan")
    return out


def run_A(logger, quick: bool = False, workers: int = 0) -> dict:
    W = workers or n_workers()
    nb = 60 if quick else N_BOOT_PANEL
    res = {"label": SELECTION_LABEL, "resampling_unit": "concept", "n_boot": nb,
           "spec": "PPML (pyfixest fepois); CRV1 by concept; X standardised over the rows of each model",
           "EMB_note": "EMB is an ANALOGUE of Cheng's word2vec embeddedness (backbone PMI), not the same measure",
           "builds": {}}
    for build in ["HOME", "ALL"]:
        t = time.time()
        d0 = panel_A(build)
        if quick:
            keep = d0.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)
            d0 = d0[d0.ci.isin(keep)]
        d0 = d0[np.isfinite(d0.V_next)]
        dj = zcols(d0.dropna(subset=["EMB", "SOC"]), ["CONS", "EMB", "SOC"])
        dc = zcols(d0, ["CONS"])
        B = {"n_rows_CONS": int(len(dc)), "n_rows_joint": int(len(dj)), "n_concepts_joint": int(dj.ci.nunique()),
             "share_rows_dropped_for_EMB_SOC": 1 - len(dj) / max(len(dc), 1),
             "CONS_mean": float(d0.CONS.mean()), "CONS_sd": float(d0.CONS.std())}
        B["joint"] = fit_A_set(dj, XS_JOINT, with_A3=True, with_nb=(build == "HOME"))
        B["cons_only"] = fit_A_set(dc, ["zCONS"], with_A3=True, with_nb=(build == "HOME"))
        logger.info(f"A {build}: joint A1 {B['joint']['A1']['coef']['zCONS']} A2 {B['joint']['A2']['coef']['zCONS']}")
        # bootstrap ratio (headline = HOME joint), plus CONS-only
        br = boot_ratio(dj, XS_JOINT, nb, SEED, W)
        pf1 = B["joint"]["A1"]["coef"]["zCONS"]["b"]
        br["irls_vs_pyfixest_abs_diff_A1"] = abs(br["b_A1_irls"] - pf1)
        np.save(DATA / f"boot_ratio_{build}_joint.npy", br.pop("boot_b"))
        B["joint"]["ratio_boot"] = br
        brc = boot_ratio(dc, ["zCONS"], nb, SEED + 7, W)
        brc.pop("boot_b")
        B["cons_only"]["ratio_boot"] = brc
        logger.info(f"A {build}: ratio {br['ratio']:.3f} CI {br['ratio_ci']} (irls-pf diff "
                    f"{br['irls_vs_pyfixest_abs_diff_A1']:.2e}); cons-only {brc['ratio']:.3f} {brc['ratio_ci']}")
        # per body / per group (joint, A1 and A2, CRV1) + DL across groups
        B["by_body"] = {}
        for bd in sorted(d0.body.unique()):
            g = zcols(d0[d0.body == bd].dropna(subset=["EMB", "SOC"]), ["CONS", "EMB", "SOC"])
            B["by_body"][bd] = fit_A_set(g, XS_JOINT, with_A3=False)
        B["by_group"] = {}
        for gname in GROUPS5 + ["MATHDEC"]:
            g = zcols(d0[d0.group5 == gname].dropna(subset=["EMB", "SOC"]), ["CONS", "EMB", "SOC"])
            if g.ci.nunique() < 30:
                continue
            B["by_group"][gname] = fit_A_set(g, XS_JOINT, with_A3=False)
        for m in ["A1", "A2"]:
            bs = [B["by_group"][g][m]["coef"]["zCONS"]["b"] for g in GROUPS5 if g in B["by_group"]]
            ss = [B["by_group"][g][m]["coef"]["zCONS"]["se"] for g in GROUPS5 if g in B["by_group"]]
            B[f"DL_{m}_groups"] = dersimonian_laird(bs, ss)
        res["builds"][build] = B
        logger.info(f"A {build} done in {(time.time() - t) / 60:.1f} min")
    jdump(res, RES / ("cheng_panel_models_quick.json" if quick else "cheng_panel_models.json"))
    return res


def refit_nb(logger) -> None:
    """Re-fit A1-NB for both HOME specs and patch results/cheng_panel_models.json (used when the joint NB fit hit a
    singular Hessian in the main S3 run)."""
    from common import jload
    res = jload(RES / "cheng_panel_models.json")
    d0 = panel_A("HOME")
    d0 = d0[np.isfinite(d0.V_next)]
    dj = zcols(d0.dropna(subset=["EMB", "SOC"]), ["CONS", "EMB", "SOC"])
    dc = zcols(d0, ["CONS"])
    for spec, d, xs in (("joint", dj, XS_JOINT), ("cons_only", dc, ["zCONS"])):
        try:
            res["builds"]["HOME"][spec]["A1_NB"] = nb_fit(d, xs)
        except (ValueError, np.linalg.LinAlgError) as e:
            res["builds"]["HOME"][spec]["A1_NB"] = {"error": repr(e)[:300]}
        logger.info(f"A1-NB {spec}: {res['builds']['HOME'][spec]['A1_NB']}")
    jdump(res, RES / "cheng_panel_models.json")


# ----------------------------------------------------------------------------- test C
def panel_C() -> pd.DataFrame:
    yp = pd.read_parquet(EXP11 / "data/yearly_panel.parquet",
                         columns=["ci", "year", "t0", "h_end", "body", "group", "y_next", "at_risk_next", "deg",
                                  "log1p_home", "log1p_all", "log1p_deg", "log_at_risk"])
    yp = yp[(yp.at_risk_next > 0) & (yp.deg >= 2) & yp.y_next.notna()]
    f = pd.read_parquet(DATA / "cheng_features.parquet")
    f = f[(f.body_src == "EXP5") & (f.build == "HOME")][["ci", "year", "CONS"]]
    d = yp.merge(f, on=["ci", "year"], how="left")
    d = d[np.isfinite(d.CONS)].copy()
    # home share from Exp11 counts_m (grounded counts per ci x year x vfield)
    fr = pd.read_csv(EXP5 / "frame_concepts.csv", usecols=["ci", "home"])
    hm = {int(r.ci): home_codes(r.home) for r in fr.itertuples()}
    cm = pd.read_parquet(EXP11 / "data/counts_m.parquet")
    cm = cm[cm.ci.isin(set(d.ci))]
    cm["is_home"] = [v in hm.get(c, ()) for c, v in zip(cm.ci.to_numpy(), cm.vfield.to_numpy())]
    tot = cm.groupby(["ci", "year"]).n.sum().rename("tot")
    hom = cm[cm.is_home].groupby(["ci", "year"]).n.sum().rename("hom")
    hs = pd.concat([tot, hom], axis=1).fillna(0).reset_index()
    hs["hshare"] = np.where(hs.tot > 0, hs.hom / hs.tot.clip(lower=1), np.nan)
    d = d.merge(hs[["ci", "year", "hshare"]], on=["ci", "year"], how="left").merge(
        hs[["ci", "year", "hshare"]].assign(year=hs.year - 1).rename(columns={"hshare": "hshare_next"}),
        on=["ci", "year"], how="left")
    d["dHomeShare_next"] = d.hshare_next - d.hshare
    d["group5"] = d.group.map(GROUP5)
    return zcols(d, ["CONS"]).reset_index(drop=True)


CTRL = ["log1p_home", "log1p_all", "log1p_deg", "log_at_risk"]


def _boot_C_worker(args) -> list[tuple[float, float]]:
    d, cl, seeds = args
    import pyfixest as pf
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        pick = rng.integers(0, len(cl), len(cl))
        rows = np.concatenate([cl[p] for p in pick])
        newid = np.concatenate([np.full(len(cl[p]), j) for j, p in enumerate(pick)])
        b = d.iloc[rows].copy()
        b["ci"] = newid
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                b1 = float(pf.fepois(f"y_next ~ zCONS + {' + '.join(CTRL)} | ci + year", data=b,
                                     vcov="iid").coef()["zCONS"])
            except (ValueError, RuntimeError, np.linalg.LinAlgError):
                b1 = float("nan")
            bb = b.dropna(subset=["dHomeShare_next"])
            try:
                b2 = float(pf.feols(f"dHomeShare_next ~ zCONS + {' + '.join(CTRL)} | ci + year", data=bb,
                                    vcov="iid").coef()["zCONS"])
            except (ValueError, RuntimeError, np.linalg.LinAlgError):
                b2 = float("nan")
        out.append((b1, b2))
    return out


def run_C(logger, quick: bool = False, workers: int = 0) -> dict:
    W = workers or n_workers()
    nb = 40 if quick else N_BOOT_PANEL
    t = time.time()
    d = panel_C()
    if quick:
        keep = d.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)
        d = d[d.ci.isin(keep)].reset_index(drop=True)
    res = {"label": SELECTION_LABEL, "resampling_unit": "concept", "n_rows": int(len(d)),
           "n_concepts": int(d.ci.nunique()),
           "C1": fepois(d, "y_next", ["zCONS"] + CTRL, "ci + year"),
           "C2": feols(d.dropna(subset=["dHomeShare_next"]), "dHomeShare_next", ["zCONS"] + CTRL, "ci + year"),
           "C1_by_body": {}, "C2_by_body": {}}
    for bd in sorted(d.body.unique()):
        g = d[d.body == bd]
        res["C1_by_body"][bd] = fepois(g, "y_next", ["zCONS"] + CTRL, "ci + year")
        res["C2_by_body"][bd] = feols(g.dropna(subset=["dHomeShare_next"]), "dHomeShare_next", ["zCONS"] + CTRL,
                                      "ci + year")
    logger.info(f"C1 {res['C1']['coef']['zCONS']}  C2 {res['C2']['coef']['zCONS']}  ({time.time() - t:.0f}s)")
    cl = cluster_index(d.ci.to_numpy())
    seeds = [SEED + 500 + k for k in range(nb)]
    parts = [seeds[i::W] for i in range(W)]
    out = []
    t = time.time()
    with ProcessPoolExecutor(max_workers=W, mp_context=mp.get_context("spawn")) as ex:
        for r in ex.map(_boot_C_worker, [(d, cl, p) for p in parts]):
            out.extend(r)
    B = np.array(out)
    for j, k in enumerate(["C1", "C2"]):
        v = B[:, j]
        v = v[np.isfinite(v)]
        res[k]["boot"] = {"n_boot": int(len(v)), "ci": np.percentile(v, [2.5, 97.5]).tolist(),
                          "p_one_lt_0": float((np.sum(v >= 0) + 1) / (len(v) + 1))}
    logger.info(f"C bootstrap {nb} draws in {(time.time() - t) / 60:.1f} min: C1 {res['C1']['boot']} "
                f"C2 {res['C2']['boot']}")
    jdump(res, RES / ("panel_C_quick.json" if quick else "panel_C.json"))
    return res
