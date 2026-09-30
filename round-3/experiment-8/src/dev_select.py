#!/usr/bin/env python3
"""STEP 5: DEV-ONLY selection, learned models, power, FREEZE + SEAL.

Reads results/indicator_matrix.parquet and data/outcomes_dev.parquet (never the sealed file).
  continuous outcomes {O1c, O2r_m50, O2r_resid, O4}: partial Spearman psp(x, y | B5 + group + t0 dummies),
      1,000 concept-bootstrap resamples with the rank residualisation refitted in each resample
  binary outcomes {O1b, O3, O5, O5_WW}: dAUC = AUC(B5 + x) - AUC(B5), L2 logistic, leave-one-DEV-group-out OOF;
      concept bootstrap (stratified by group) refitting both models (O5*: + linear onset year)
  frozen ranking rule -> top10 per outcome (+ sign), union_top10; sensitivity rankings; shuffled-outcome placebo;
  learned models (ElasticNetCV / L1-logistic CV / EBM) vs B5-only, LOGO on DEV; power; freeze -> seal.log.
Usage: python dev_select.py [--stage all|rank|models|freeze] [--workers 5]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import subprocess
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, FIGS, LIB, LOGS, MODELS, RES, ROOT, SEED, add_deviation, jdump, setup_logger, sha256_file
from indicators import (B5, BIN_OUTCOMES, CONT_OUTCOMES, FAMILY_OF, FORMULA_OF, INDICATORS, OUTCOMES, PREREG,
                        PREREG_INDICATORS, PREVIOUSLY_SCORED, T0_BASELINE_OUTCOMES)

N_BOOT_CONT = 1000
N_BOOT_BIN = 500
N_BOOT_SENS = 200
MAX_MISSING = 0.30
DEDUP_RHO = 0.85
COVERAGE = ["label_coverage_early", "tag_coverage", "precision_c"]
G: dict = {}


def load_dev() -> pd.DataFrame:
    X = pd.read_parquet(RES / "indicator_matrix.parquet")
    Y = pd.read_parquet(DATA / "outcomes_dev.parquet")
    assert set(Y.split) == {"DEV"}
    D = X[X.split == "DEV"].merge(Y[["ci"] + OUTCOMES], on="ci", how="inner")
    return D.reset_index(drop=True)


def _init() -> None:
    warnings.filterwarnings("ignore")
    G["D"] = load_dev()


def cat_matrix(D: pd.DataFrame, with_group: bool = True) -> np.ndarray:
    from rq1stats import dummies
    parts = [dummies(D.t0.to_numpy())]
    if with_group:
        parts.append(dummies(D.group.to_numpy()))
    return np.hstack(parts)


def base_matrix(D: pd.DataFrame, outcome: str, extra: list[str] | None = None) -> np.ndarray:
    cols = B5 + (extra or [])
    Xb = D[cols].to_numpy(float)
    if outcome in T0_BASELINE_OUTCOMES:
        Xb = np.c_[Xb, D.t0.to_numpy(float)]
    return Xb


def job(args):
    kind, ind, outcome, seed, nboot, extra, perm = args
    from rq1stats import dauc_boot, psp_boot, spearman_raw
    D = G["D"]
    y = D[outcome].to_numpy(float)
    if perm is not None:
        rng = np.random.default_rng(perm)
        y = y.copy()
        for g_ in D.group.unique():
            m = (D.group == g_).to_numpy()
            y[m] = rng.permutation(y[m])
    x = D[ind].to_numpy(float)
    if kind == "cont":
        B = D[B5 + (extra or [])].to_numpy(float)
        r = psp_boot(x, y, B, cat_matrix(D), nboot, seed)
        raw, _ = spearman_raw(x, y)
        out = {"est": r["rho"], "ci": r["ci"], "n": r["n"], "p": r["p"], "se": r["se"], "raw_rho": raw}
    else:
        Xb = base_matrix(D, outcome, extra)
        r = dauc_boot(Xb, x, y, D.group.to_numpy(), nboot, seed)
        out = {"est": r["dauc"], "ci": r["ci"], "n": r["n"], "p": r["p"], "se": r.get("se"),
               "auc_base": r.get("auc_base"), "auc_full": r.get("auc_full"), "n_pos": r.get("n_pos")}
    return kind, ind, outcome, perm, out


def run_jobs(jobs, workers, logger, label):
    t = time.time()
    res = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        for i, r in enumerate(ex.map(job, jobs, chunksize=1)):
            res.append(r)
            if (i + 1) % 50 == 0 or i + 1 == len(jobs):
                logger.info(f"{label}: {i+1}/{len(jobs)} jobs, {(time.time()-t)/60:.1f} min")
    return res


def select_top(tab: pd.DataFrame, D: pd.DataFrame, k: int = 10) -> list[dict]:
    """Frozen rule: eligible = CI excludes 0 and missing <= 30%; order by |est|; greedy |Spearman| > 0.85 dedup."""
    t = tab.copy()
    t["eligible"] = (t.ci_lo > 0) | (t.ci_hi < 0)
    t["eligible"] &= t.missing <= MAX_MISSING
    t = t[np.isfinite(t.est)].assign(a=lambda d: d.est.abs()).sort_values("a", ascending=False)
    corr = D[INDICATORS].rank().corr().abs()
    sel = []
    for pool, flag in ((t[t.eligible], "eligible"), (t[~t.eligible & (t.missing <= MAX_MISSING)], "filled")):
        for r in pool.itertuples():
            if len(sel) >= k:
                break
            if any(corr.loc[r.indicator, s["indicator"]] > DEDUP_RHO for s in sel):
                continue
            sel.append({"indicator": r.indicator, "sign": int(np.sign(r.est)), "est": float(r.est),
                        "ci": [float(r.ci_lo), float(r.ci_hi)], "status": flag, "family": FAMILY_OF[r.indicator]})
    return sel


def stage_rank(logger, workers: int) -> None:
    D = load_dev()
    logger.info(f"DEV rows {len(D)}; groups {D.group.value_counts().to_dict()}")
    miss = D[INDICATORS].isna().mean()
    # ---------------- diagnostics
    from scipy.stats import spearmanr
    diag = []
    for c in INDICATORS:
        ok = D[c].notna()
        r_lv = spearmanr(D.loc[ok, c], D.loc[ok, "logvol"])[0] if ok.sum() > 10 else np.nan
        r_gr = spearmanr(D.loc[ok, c], D.loc[ok, "growth_c"])[0] if ok.sum() > 10 else np.nan
        diag.append({"indicator": c, "family": FAMILY_OF[c], "missing": float(miss[c]), "rho_logvol": r_lv,
                     "rho_growth_c": r_gr, "size_flag": bool(abs(r_lv) > 0.6 or abs(r_gr) > 0.6)})
    pd.DataFrame(diag).to_csv(RES / "size_diagnostic_dev.csv", index=False)
    corr = D[INDICATORS + B5].rank().corr()
    corr.to_csv(RES / "indicator_corr_dev.csv")
    _cluster_fig(corr.loc[INDICATORS, INDICATORS], logger)
    # ---------------- rankings
    jobs = []
    for o in CONT_OUTCOMES:
        if D[o].notna().sum() < 100:
            logger.warning(f"{o}: too few DEV values; skipped")
            continue
        jobs += [("cont", c, o, SEED + 17 * i, N_BOOT_CONT, None, None) for i, c in enumerate(INDICATORS)]
    for o in BIN_OUTCOMES:
        if D[o].notna().sum() < 100:
            logger.warning(f"{o}: too few DEV values; skipped")
            continue
        jobs += [("bin", c, o, SEED + 17 * i, N_BOOT_BIN, None, None) for i, c in enumerate(INDICATORS)]
    res = run_jobs(jobs, workers, logger, "DEV ranking")
    rows = [{"indicator": ind, "family": FAMILY_OF[ind], "outcome": o, "kind": k, "missing": float(miss[ind]),
             "est": r["est"], "ci_lo": r["ci"][0], "ci_hi": r["ci"][1], "p": r["p"], "n": r["n"], "se": r["se"],
             **{kk: r.get(kk) for kk in ("raw_rho", "auc_base", "auc_full", "n_pos")}}
            for k, ind, o, _, r in res]
    tab = pd.DataFrame(rows)
    tab.to_csv(RES / "dev_ranking.csv", index=False)
    # ---------------- selection
    top = {o: select_top(tab[tab.outcome == o], D) for o in tab.outcome.unique()}
    rk = tab.assign(a=tab.est.abs()).copy()
    rk["rank"] = rk.groupby("outcome").a.rank(ascending=False, na_option="bottom")
    mean_rank = rk[rk.missing <= MAX_MISSING].groupby("indicator")["rank"].mean().sort_values()
    corr_i = D[INDICATORS].rank().corr().abs()
    union = []
    for ind in mean_rank.index:
        if len(union) >= 10:
            break
        if any(corr_i.loc[ind, u] > DEDUP_RHO for u in union):
            continue
        union.append(ind)
    signs = {o: {r.indicator: int(np.sign(r.est)) for r in tab[tab.outcome == o].itertuples() if np.isfinite(r.est)}
             for o in tab.outcome.unique()}
    # ---------------- sensitivity rankings (reported, not used for the freeze)
    sjobs = [("cont", c, o, SEED + 5 + i, N_BOOT_SENS, COVERAGE, None) for o in ("O2r_m50", "O2r_resid", "O1c")
             for i, c in enumerate(INDICATORS)]
    sres = run_jobs(sjobs, workers, logger, "coverage-sensitivity ranking")
    sens = pd.DataFrame([{"indicator": ind, "outcome": o, "est_cov": r["est"], "ci_lo_cov": r["ci"][0],
                          "ci_hi_cov": r["ci"][1]} for _, ind, o, _, r in sres])
    terc = []
    from rq1stats import auc
    for o in CONT_OUTCOMES:
        for c in INDICATORS:
            vals = []
            for g_, d in D.groupby("group"):
                d = d[[c, o]].dropna()
                if len(d) < 30:
                    continue
                q1, q2 = d[o].quantile([1 / 3, 2 / 3])
                dd = d[(d[o] <= q1) | (d[o] >= q2)]
                vals.append(auc((dd[o] >= q2).to_numpy(), dd[c].to_numpy()))
            terc.append({"indicator": c, "outcome": o, "tercile_auc_mean": float(np.nanmean(vals)) if vals else np.nan})
    sens = sens.merge(pd.DataFrame(terc), on=["indicator", "outcome"], how="outer")
    sens.to_csv(RES / "dev_ranking_sensitivity.csv", index=False)
    # ---------------- T5 shuffled-outcome placebo (O2r_resid within group, 20 permutations)
    pjobs = [("cont", c, "O2r_resid", SEED + 3 + i, N_BOOT_SENS, None, 1000 + p) for p in range(20)
             for i, c in enumerate(INDICATORS)]
    pres = run_jobs(pjobs, workers, logger, "placebo")
    pl = pd.DataFrame([{"perm": perm, "indicator": ind, "est": r["est"], "lo": r["ci"][0], "hi": r["ci"][1]}
                       for _, ind, _, perm, r in pres])
    pl["excl0"] = (pl.lo > 0) | (pl.hi < 0)
    per = pl.groupby("perm").excl0.sum()
    placebo = {"n_perm": 20, "n_indicators": len(INDICATORS), "mean_excluding_0": float(per.mean()),
               "expected_at_5pct": 0.05 * len(INDICATORS), "per_perm": per.tolist(),
               "mean_abs_psp": float(pl.est.abs().mean()), "pass": bool(per.mean() <= 6)}
    out = {"n_dev": len(D), "top10": top, "union_top10": union, "union_mean_rank": mean_rank.loc[union].to_dict(),
           "signs": signs, "placebo_T5": placebo, "missing": miss.to_dict(),
           "n_boot": {"cont": N_BOOT_CONT, "bin": N_BOOT_BIN, "sens": N_BOOT_SENS}}
    jdump(out, RES / "rq1_dev_selection.json")
    logger.info(f"placebo: mean # CI excluding 0 = {placebo['mean_excluding_0']:.2f} of {len(INDICATORS)}")
    for o, s in top.items():
        logger.info(f"TOP10 {o}: " + ", ".join(f"{d['indicator']}({d['est']:+.3f},{d['status'][0]})" for d in s))
    logger.info(f"UNION: {union}")


def _cluster_fig(corr: pd.DataFrame, logger) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
    from scipy.spatial.distance import squareform
    Dm = 1 - corr.abs().fillna(0).to_numpy()
    np.fill_diagonal(Dm, 0)
    Z = linkage(squareform(np.clip((Dm + Dm.T) / 2, 0, None), checks=False), "average")
    cl = fcluster(Z, t=0.3, criterion="distance")   # clusters at |rho| < 0.7
    jdump({"n_clusters_at_abs_rho_0.7": int(len(set(cl))), "membership": dict(zip(corr.index, cl.tolist()))},
          RES / "indicator_clusters_dev.json")
    fig, ax = plt.subplots(figsize=(13, 5.5))
    dendrogram(Z, labels=[f"{c} [{FAMILY_OF.get(c, 'B5')}]" for c in corr.index], leaf_rotation=90, ax=ax,
               color_threshold=0.3)
    ax.axhline(0.3, ls="--", c="grey", lw=0.8)
    ax.set_ylabel("1 - |Spearman| (average linkage)")
    ax.set_title(f"DEV indicator clusters ({len(set(cl))} clusters at |rho| < 0.7)")
    fig.tight_layout()
    fig.savefig(FIGS / "indicator_clusters.png", dpi=150)
    fig.savefig(FIGS / "indicator_clusters.pdf")
    plt.close(fig)
    logger.info(f"indicator clusters at |rho|<0.7: {len(set(cl))}")


# ----------------------------------------------------------------------------- learned models
def learned_models(logger) -> None:
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=UserWarning)
    import joblib
    from sklearn.linear_model import ElasticNetCV, LinearRegression, LogisticRegression, LogisticRegressionCV
    from sklearn.model_selection import LeaveOneGroupOut
    from design import apply_design, design_names, fit_design
    from rq1stats import auc, logit_fit, logit_pred
    try:
        from interpret.glassbox import ExplainableBoostingClassifier, ExplainableBoostingRegressor
        HAS_EBM = True
    except ImportError:
        HAS_EBM = False
        add_deviation("F7_ebm", "interpret unavailable -> HistGradientBoosting substitute")
    D = load_dev()
    sel = json.loads((RES / "rq1_dev_selection.json").read_text())
    feats = INDICATORS + B5
    dspec = fit_design(D, feats)
    b5spec = fit_design(D, B5)
    names = design_names(dspec)
    X = apply_design(D, dspec)
    XB = apply_design(D, b5spec)
    grp = D.group.to_numpy()
    logo = LeaveOneGroupOut()
    out = {"design_spec": dspec, "b5_spec": b5spec, "models": {}}
    preds = pd.DataFrame({"ci": D.ci})
    for o in OUTCOMES:
        y = D[o].to_numpy(float)
        ok = np.isfinite(y)
        if ok.sum() < 100:
            continue
        top1 = sel["top10"].get(o, [{}])[0].get("indicator") if sel["top10"].get(o) else None
        Xo, XBo, yo, go = X[ok], XB[ok], y[ok], grp[ok]
        t1 = D[top1].astype(float).to_numpy()[ok] if top1 else None
        t1_med = float(np.nanmedian(D[top1])) if top1 else 0.0
        if top1 is not None:
            t1 = np.where(np.isfinite(t1), t1, t1_med)
            t1_mu, t1_sd = float(t1.mean()), float(t1.std() or 1.0)
            t1 = (t1 - t1_mu) / t1_sd
        extra = D.t0.to_numpy(float)[ok][:, None] if o in T0_BASELINE_OUTCOMES else np.zeros((ok.sum(), 0))
        t0mu, t0sd = (float(extra.mean()), float(extra.std() or 1.0)) if extra.shape[1] else (0.0, 1.0)
        extra_s = (extra - t0mu) / t0sd
        oof = {k: np.full(len(yo), np.nan) for k in ("B5", "B5_best_single", "linear_all", "EBM")}
        rec: dict = {"n": int(ok.sum()), "best_single": top1, "best_single_std": [t1_mu, t1_sd, t1_med] if top1 else None,
                     "t0_std": [t0mu, t0sd] if extra.shape[1] else None}
        t = time.time()
        is_bin = o in BIN_OUTCOMES
        for tr, te in logo.split(Xo, yo, go):
            b_tr = np.c_[XBo[tr], extra_s[tr]]
            b_te = np.c_[XBo[te], extra_s[te]]
            if is_bin:
                w = logit_fit(b_tr, yo[tr]); oof["B5"][te] = logit_pred(w, b_te)
                if top1:
                    w = logit_fit(np.c_[b_tr, t1[tr]], yo[tr]); oof["B5_best_single"][te] = logit_pred(w, np.c_[b_te, t1[te]])
                m = LogisticRegressionCV(Cs=20, penalty="l1", solver="saga", max_iter=1000, tol=1e-3, cv=3, scoring="roc_auc",
                                         n_jobs=5, random_state=SEED).fit(np.c_[Xo[tr], extra_s[tr]], yo[tr])
                oof["linear_all"][te] = m.predict_proba(np.c_[Xo[te], extra_s[te]])[:, 1]
                if HAS_EBM:
                    e = ExplainableBoostingClassifier(interactions=10, outer_bags=8, random_state=SEED, n_jobs=5)
                    e.fit(np.c_[Xo[tr], extra_s[tr]], yo[tr])
                    oof["EBM"][te] = e.predict_proba(np.c_[Xo[te], extra_s[te]])[:, 1]
            else:
                oof["B5"][te] = LinearRegression().fit(b_tr, yo[tr]).predict(b_te)
                if top1:
                    oof["B5_best_single"][te] = LinearRegression().fit(np.c_[b_tr, t1[tr]], yo[tr]).predict(
                        np.c_[b_te, t1[te]])
                m = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9, 1.0], cv=3, n_jobs=5, random_state=SEED, max_iter=5000)
                oof["linear_all"][te] = m.fit(Xo[tr], yo[tr]).predict(Xo[te])
                if HAS_EBM:
                    e = ExplainableBoostingRegressor(interactions=10, outer_bags=8, random_state=SEED, n_jobs=5)
                    oof["EBM"][te] = e.fit(Xo[tr], yo[tr]).predict(Xo[te])
        from scipy.stats import spearmanr
        met = {}
        for k, p in oof.items():
            okp = np.isfinite(p)
            if okp.sum() < 50:
                continue
            if is_bin:
                met[k] = {"auc": auc(yo[okp], p[okp]), "brier": float(np.mean((p[okp] - yo[okp]) ** 2))}
            else:
                met[k] = {"spearman": float(spearmanr(p[okp], yo[okp])[0]),
                          "r2": float(1 - np.sum((yo[okp] - p[okp]) ** 2) / np.sum((yo[okp] - yo[okp].mean()) ** 2))}
        rec["dev_logo"] = met
        # final fits on all DEV
        b_all = np.c_[XBo, extra_s]
        if is_bin:
            rec["B5_coef"] = logit_fit(b_all, yo).tolist()
            if top1:
                rec["B5_best_single_coef"] = logit_fit(np.c_[b_all, t1], yo).tolist()
            m = LogisticRegressionCV(Cs=20, penalty="l1", solver="saga", max_iter=1000, tol=1e-3, cv=list(logo.split(Xo, yo, go)),
                                     scoring="roc_auc", n_jobs=5, random_state=SEED).fit(np.c_[Xo, extra_s], yo)
            rec["linear_all"] = {"C": float(m.C_[0]), "coef": dict(zip(names + (["t0"] if extra.shape[1] else []),
                                                                        m.coef_[0].tolist())),
                                 "intercept": float(m.intercept_[0]),
                                 "l1_path_nonzero": [int((c != 0).sum()) for c in
                                                     m.coefs_paths_[1.0].mean(0)[:, :-1]]}
        else:
            lr = LinearRegression().fit(b_all, yo)
            rec["B5_coef"] = [float(lr.intercept_)] + lr.coef_.tolist()
            if top1:
                lr2 = LinearRegression().fit(np.c_[b_all, t1], yo)
                rec["B5_best_single_coef"] = [float(lr2.intercept_)] + lr2.coef_.tolist()
            m = ElasticNetCV(l1_ratio=[0.1, 0.5, 0.9, 1.0], cv=list(logo.split(Xo, yo, go)), n_jobs=5,
                             random_state=SEED, max_iter=5000).fit(Xo, yo)
            rec["linear_all"] = {"alpha": float(m.alpha_), "l1_ratio": float(m.l1_ratio_),
                                 "coef": dict(zip(names, m.coef_.tolist())), "intercept": float(m.intercept_)}
        joblib.dump(m, MODELS / f"linear_all_{o}.joblib")
        if HAS_EBM:
            e = (ExplainableBoostingClassifier if is_bin else ExplainableBoostingRegressor)(
                interactions=10, outer_bags=8, random_state=SEED, n_jobs=5)
            e.fit(np.c_[Xo, extra_s] if is_bin else Xo, yo)
            joblib.dump(e, MODELS / f"ebm_{o}.joblib")
            fn = names + (["t0"] if (is_bin and extra.shape[1]) else [])
            imp = e.term_importances()
            terms = [" x ".join(fn[i] for i in t) for t in e.term_features_]
            order = np.argsort(-imp)
            rec["ebm"] = {"term_importance": {terms[i]: float(imp[i]) for i in order[:25]},
                          "pairwise_terms": [terms[i] for i in range(len(terms)) if len(e.term_features_[i]) == 2],
                          "shapes": {}}
            for i in order[:8]:
                if len(e.term_features_[i]) == 1:
                    cuts = e.bins_[e.term_features_[i][0]][0]
                    cuts = [float(b) for b in np.asarray(cuts).ravel()] if isinstance(cuts, np.ndarray) else None
                    rec["ebm"]["shapes"][terms[i]] = {"cuts": cuts,
                                                      "scores": np.asarray(e.term_scores_[i]).ravel().tolist()}
        for k in oof:
            full = np.full(len(D), np.nan)
            full[np.nonzero(ok)[0]] = oof[k]
            preds[f"{o}__{k}"] = full
        out["models"][o] = rec
        logger.info(f"learned {o}: {json.dumps(met)} ({time.time()-t:.0f}s)")
    preds.to_parquet(RES / "dev_oof_predictions.parquet", index=False)
    jdump(out, RES / "learned_model.json")


def power(logger) -> dict:
    """Simulated SD of psp at the held-out unit sizes (x independent draw with planted rho on the y residual)."""
    from rq1stats import psp_point
    D = load_dev()
    B = D[B5].dropna().to_numpy(float)
    rng = np.random.default_rng(SEED)
    sizes = {"PHYS": 742, "LIFEENV": 1113, "SOC": 1352, "MATHDEC": 165, "COH_DEVHOME": 2484, "COH_OTHER": 1872}
    res = {}
    for u, n in sizes.items():
        sims = {0.0: [], 0.05: [], 0.10: []}
        for rho in sims:
            for _ in range(300):
                i = rng.integers(0, len(B), n)
                Bs = B[i]
                lin = (Bs - Bs.mean(0)) / (Bs.std(0) + 1e-9) @ np.array([0.6, 0.2, 0.1, 0.2, 0.3])
                e = rng.normal(size=n)
                x = rho * e + np.sqrt(1 - rho ** 2) * rng.normal(size=n)
                sims[rho].append(psp_point(x, lin + e, Bs, None))
        sd = float(np.std(sims[0.0]))
        res[u] = {"n": n, "sd_psp_null": sd, "MDE_2.8SE": 2.8 * sd,
                  "power_rho_0.05": float(np.mean(np.array(sims[0.05]) - 1.96 * sd > 0)),
                  "power_rho_0.10": float(np.mean(np.array(sims[0.10]) - 1.96 * sd > 0))}
    se_pool = 1 / np.sqrt(sum(1 / (res[u]["sd_psp_null"] ** 2) for u in ("PHYS", "LIFEENV", "SOC", "MATHDEC")))
    res["pooled_4_groups"] = {"se_fixed": float(se_pool), "MDE_2.8SE": float(2.8 * se_pool)}
    jdump(res, RES / "power_dev.json")
    logger.info(f"power: {json.dumps({k: round(v.get('MDE_2.8SE', 0), 3) for k, v in res.items()})}")
    return res


def freeze(logger) -> None:
    import seal
    sel = json.loads((RES / "rq1_dev_selection.json").read_text())
    lm = json.loads((RES / "learned_model.json").read_text())
    pw = json.loads((RES / "power_dev.json").read_text())
    o2 = json.loads((RES / "o2r_resid_fit.json").read_text())
    feats = json.loads((RES / "features_config.json").read_text()) if (RES / "features_config.json").exists() else {}
    libs = {p.name: sha256_file(p) for p in sorted(LIB.glob("*.py"))}
    scripts = {p.name: sha256_file(p) for p in sorted(ROOT.glob("*.py"))}
    spec = {
        "indicators": {c: {"family": FAMILY_OF[c], "formula": FORMULA_OF[c],
                           "previously_scored_heldout": c in PREVIOUSLY_SCORED} for c in INDICATORS},
        "windows": {"features": "t0..t0+2", "ego": "PRE t0-3..t0-1, W1 t0, W2 t0+1, W3 t0+2",
                    "O1c/O2r/O3": "t0+6..t0+8", "O4": "citing years t0..t0+2 vs t0+3..t0+8", "O5": "t0..t0+8"},
        "features_config": feats, "B5": B5, "baseline_extra": {"O5": "linear onset year", "O5_WW": "linear onset year"},
        "psp_covariates": {"DEV": "rank(B5) + group dummies + t0 dummies",
                           "held-out group": "rank(B5) + t0 dummies",
                           "cohort part": "rank(B5) + group dummies + t0 dummies"},
        "sensitivity_covariates": COVERAGE, "O2r_resid": {"a": o2["a_dev"], "b": o2["b_dev"]},
        "O5_rules": "year_usable & relation == same; MeSH (non-baseline), Wikipedia creation, Wikidata P571/P575, "
                    "taxonomy_added_between (ACM CCS, MSC, PACS/PhySH), curated lists except Research Fronts; at risk "
                    "= no qualifying event before t0; MeSH & taxonomy need year > t0; O5_WW = Wikipedia+Wikidata only; "
                    "groups with < 20 positives dropped",
        "top10": sel["top10"], "union_top10": sel["union_top10"], "signs": sel["signs"],
        "learned": {o: {k: v for k, v in m.items() if k in ("B5_coef", "B5_best_single_coef", "best_single",
                                                            "best_single_std", "t0_std", "linear_all")}
                    for o, m in lm["models"].items()},
        "design_spec": lm["design_spec"], "b5_spec": lm["b5_spec"],
        "bootstrap": {"B_heldout": 1000, "seed": SEED, "unit": "concept"},
        "holm_families": "per outcome: the 10 pooled tests of that outcome's frozen top 10",
        "pooling": "DerSimonian-Laird over PHYS, LIFEENV, SOC, MATHDEC (Fisher z of psp with bootstrap SE; dAUC with "
                   "bootstrap SE)",
        "power": pw, "preregistered_predictions": PREREG,
        "sha256": {"lib": libs, "scripts": scripts,
                   "indicator_matrix.parquet": sha256_file(RES / "indicator_matrix.parquet"),
                   "outcomes_dev.parquet": sha256_file(DATA / "outcomes_dev.parquet"),
                   "outcomes_sealed.parquet": sha256_file(DATA / "outcomes_sealed.parquet")},
    }
    # T6: pre-unseal checklist -- no held-out/cohort outcome values in any object written before the freeze
    Xm = pd.read_parquet(RES / "indicator_matrix.parquet")
    leak = [o for o in OUTCOMES if o in Xm.columns]
    dev_only = set(pd.read_parquet(DATA / "outcomes_dev.parquet").split) == {"DEV"}
    oof = pd.read_parquet(RES / "dev_oof_predictions.parquet")
    oof_dev_only = set(oof.ci).issubset(set(Xm[Xm.split == "DEV"].ci))
    subprocess.run(["git", "add", "-A", "--", "*.py", "lib", "tests", "pyproject.toml"], cwd=ROOT, check=False,
                   capture_output=True)
    subprocess.run(["git", "-c", "user.email=aii@local", "-c", "user.name=aii", "commit", "-q", "-m",
                    "RQ1 freeze: code + DEV selection before unseal"], cwd=ROOT, check=False, capture_output=True)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    check = {"outcome_columns_in_indicator_matrix": leak, "outcomes_dev_only_DEV_rows": dev_only,
             "dev_oof_predictions_only_DEV": oof_dev_only, "git_commit": commit,
             "unsealed_marker_absent": not (LOGS / "unsealed.json").exists()}
    if leak or not dev_only or not oof_dev_only or (LOGS / "unsealed.json").exists():
        raise RuntimeError(f"T6 pre-unseal checklist failed: {check}")
    h = seal.freeze(spec, extra={"T6_checklist": check})
    logger.info(f"FROZEN: frozen_spec sha256 {h[:16]}; commit {commit[:10]}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    logger = setup_logger("dev_select")
    if a.stage in ("all", "rank"):
        stage_rank(logger, a.workers)
    if a.stage in ("all", "models"):
        learned_models(logger)
    if a.stage in ("all", "models", "power"):
        power(logger)
    if a.stage in ("all", "freeze"):
        freeze(logger)


if __name__ == "__main__":
    main()
