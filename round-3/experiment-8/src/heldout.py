#!/usr/bin/env python3
"""STEP 6: unseal ONCE (lib/seal.load_heldout) and score the frozen spec on the held-out groups and cohort parts.

  * frozen top10 per outcome (+ union_top10) in every unit: psp | B5 (+ t0 dummies; + group dummies in cohort parts)
    with 1,000 concept-bootstrap resamples (continuous); dAUC with the FROZEN DEV coefficients and a joint refit
    bootstrap (resample DEV -> refit -> resample unit -> score) (binary)
  * DL pooling over PHYS/LIFEENV/SOC/MATHDEC, sign agreement over 6 units, Holm within each outcome family
  * learned (ElasticNet/L1-logit, EBM) vs B5 vs B5 + best single on the same units
  * portability table (every indicator x 10 units x {O2r_m50, O2r_resid, O1c} + raw Spearman with O2r_m50)
  * pre-registered predictions P1-P5; labelled post-seal sensitivities
Usage: python heldout.py [--stage unseal|score|all] [--workers 5]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP6, HELD_GROUPS, MODELS, RES, SEED, UNITS, jdump, setup_logger
from indicators import B5, BIN_OUTCOMES, CONT_OUTCOMES, FAMILY_OF, INDICATORS, OUTCOMES, PREVIOUSLY_SCORED

B_HELD = 1000
B_PORT = 500
B_SENS = 300
MIN_POS = 20
DEV_UNITS = ["CS", "Eng", "BGM", "Med"]
ALL_UNITS = DEV_UNITS + UNITS
G: dict = {}


def _init() -> None:
    warnings.filterwarnings("ignore")
    G["A"] = pd.read_parquet(DATA / "analysis_table.parquet")
    G["spec"] = json.loads((RES / "frozen_spec.json").read_text())


def cat_for(d: pd.DataFrame, unit: str) -> np.ndarray:
    from rq1stats import dummies
    parts = [dummies(d.t0.to_numpy())]
    if unit in ("COH_DEVHOME", "COH_OTHER", "ALL_DEV"):
        parts.append(dummies(d.group.to_numpy()))
    return np.hstack(parts)


def std_b(d: pd.DataFrame, outcome: str, spec: dict) -> np.ndarray:
    bs = spec["b5_spec"]
    from design import apply_design
    Xb = apply_design(d, bs)
    t0s = spec["learned"].get(outcome, {}).get("t0_std")
    if outcome in ("O5", "O5_WW") and t0s:
        Xb = np.c_[Xb, (d.t0.to_numpy(float) - t0s[0]) / t0s[1]]
    return Xb


def job(args):
    """kind: cont | bin | port. Returns a dict row."""
    kind, ind, outcome, unit, nboot, seed, extra = args
    from rq1stats import auc, logit_fit, logit_pred, psp_boot, spearman_raw
    A = G["A"]
    spec = G["spec"]
    d = A[A.unit == unit] if unit != "ALL_DEV" else A[A.split == "DEV"]
    if extra and extra.get("subset") == "no_exp6":
        d = d[~d.in_exp6]
    if extra and extra.get("subset") == "no_intersection":
        d = d[d.intersect40 == 0]
    y = d[outcome].to_numpy(float)
    x = d[ind].to_numpy(float)
    row = {"indicator": ind, "outcome": outcome, "unit": unit, "kind": kind}
    if kind in ("cont", "port"):
        cov = B5 + (extra.get("covs", []) if extra else [])
        if extra and extra.get("drop_reach"):
            cov = [c for c in cov if c != "reach"]
        r = psp_boot(x, y, d[cov].to_numpy(float), cat_for(d, unit), nboot, seed)
        raw, nraw = spearman_raw(x, y)
        row.update(n=r["n"], rho=r["rho"], ci_lo=r["ci"][0], ci_hi=r["ci"][1], se=r["se"], z=r.get("z"),
                   se_z=r.get("se_z"), p=r["p"], raw_rho=raw)
        # raw Spearman CI (percentile bootstrap) for P1/P2
        if kind == "cont" or (kind == "port" and outcome == "O2r_m50"):
            ok = np.isfinite(x) & np.isfinite(y)
            xs, ys = x[ok], y[ok]
            rng = np.random.default_rng(seed + 1)
            bs = []
            if ok.sum() >= 20:
                from scipy.stats import rankdata
                for _ in range(min(nboot, 500)):
                    i = rng.integers(0, len(xs), len(xs))
                    bs.append(np.corrcoef(rankdata(xs[i]), rankdata(ys[i]))[0, 1])
            row.update(raw_ci_lo=float(np.nanpercentile(bs, 2.5)) if bs else np.nan,
                       raw_ci_hi=float(np.nanpercentile(bs, 97.5)) if bs else np.nan)
        return row
    # binary, frozen DEV coefficients + joint refit bootstrap
    D = A[A.split == "DEV"]
    yD = D[outcome].to_numpy(float)
    okD = np.isfinite(yD) & np.isfinite(D[ind].to_numpy(float))
    ok = np.isfinite(y) & np.isfinite(x)
    npos = int(np.nansum(y[ok]))
    row.update(n=int(ok.sum()), n_pos=npos)
    if npos < MIN_POS or ok.sum() - npos < MIN_POS:
        row.update(dauc=np.nan, status=f"dropped (< {MIN_POS} positives or negatives)")
        return row
    XbD = std_b(D, outcome, spec)[okD]
    xD = D[ind].to_numpy(float)[okD]
    mu, sd = float(xD.mean()), float(xD.std() or 1.0)
    yD = yD[okD]
    Xb = std_b(d, outcome, spec)[ok]
    xs = (x[ok] - mu) / sd
    yy = y[ok]
    w0 = logit_fit(XbD, yD)
    w1 = logit_fit(np.c_[XbD, (xD - mu) / sd], yD)
    a0 = auc(yy, logit_pred(w0, Xb))
    a1 = auc(yy, logit_pred(w1, np.c_[Xb, xs]))
    rng = np.random.default_rng(seed)
    grpD = D.group.to_numpy()[okD]
    idxD = [np.nonzero(grpD == g)[0] for g in np.unique(grpD)]
    bs = []
    for _ in range(nboot):
        i = np.concatenate([rng.choice(v, len(v)) for v in idxD])
        ww0 = logit_fit(XbD[i], yD[i])
        ww1 = logit_fit(np.c_[XbD[i], (xD[i] - mu) / sd], yD[i])
        j = rng.integers(0, len(yy), len(yy))
        bs.append(auc(yy[j], logit_pred(ww1, np.c_[Xb[j], xs[j]])) - auc(yy[j], logit_pred(ww0, Xb[j])))
    bs = np.array([b for b in bs if np.isfinite(b)])
    se = float(np.std(bs, ddof=1))
    from scipy import stats
    row.update(dauc=a1 - a0, auc_base=a0, auc_full=a1, ci_lo=float(np.percentile(bs, 2.5)),
               ci_hi=float(np.percentile(bs, 97.5)), se=se,
               p=float(2 * stats.norm.sf(abs((a1 - a0) / se))) if se > 0 else np.nan, status="scored")
    return row


def run(jobs, workers, logger, label):
    t = time.time()
    out = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        for i, r in enumerate(ex.map(job, jobs, chunksize=2)):
            out.append(r)
            if (i + 1) % 100 == 0 or i + 1 == len(jobs):
                logger.info(f"{label}: {i+1}/{len(jobs)} ({(time.time()-t)/60:.1f} min)")
    return pd.DataFrame(out)


def stage_unseal(logger) -> None:
    import seal
    held = seal.load_heldout()
    X = pd.read_parquet(RES / "indicator_matrix.parquet")
    dev = pd.read_parquet(DATA / "outcomes_dev.parquet")
    Y = pd.concat([dev, held], ignore_index=True)
    Y.to_parquet(DATA / "outcomes.parquet", index=False)
    A = X.merge(Y[["ci"] + OUTCOMES + ["O5_sens", "O5_WW_sens", "O2r_m30", "O2r_resid_N"]], on="ci", how="left")
    e6 = pd.read_csv(EXP6 / "results/frame_concepts.csv")
    idcol = "concept_id" if "concept_id" in e6.columns else e6.columns[0]
    ids = set(pd.to_numeric(e6[idcol].astype(str).str.extract(r"C?(\d+)$")[0], errors="coerce").dropna()
              .astype(np.int64))
    A["in_exp6"] = A.concept_id.astype(np.int64).isin(ids)
    A.to_parquet(DATA / "analysis_table.parquet", index=False)
    logger.info(f"UNSEALED: {len(held)} held-out/cohort rows; analysis table {A.shape}; in_exp6 {int(A.in_exp6.sum())}")


def pool_block(tab: pd.DataFrame, value: str, se: str) -> dict:
    from rq1stats import dersimonian_laird
    t = tab[tab.unit.isin(HELD_GROUPS)]
    return dersimonian_laird(t[value].to_numpy(float), t[se].to_numpy(float))


def stage_score(logger, workers: int) -> None:
    from rq1stats import holm, sign_test_two_sided
    spec = json.loads((RES / "frozen_spec.json").read_text())
    top = spec["top10"]
    union = spec["union_top10"]
    jobs = []
    for o in OUTCOMES:
        if o not in top:
            continue
        inds = list(dict.fromkeys([d["indicator"] for d in top[o]] + union))
        kind = "cont" if o in CONT_OUTCOMES else "bin"
        for i, ind in enumerate(inds):
            for u in UNITS:
                jobs.append((kind, ind, o, u, B_HELD, SEED + 31 * i, None))
    t = time.time()
    tab = run(jobs, workers, logger, "held-out frozen scoring")
    tab.to_csv(RES / "heldout_unit_results.csv", index=False)
    # --------------- pooling, signs, Holm
    summary = {}
    for o in top:
        is_c = o in CONT_OUTCOMES
        members = [d["indicator"] for d in top[o]]
        inds = list(dict.fromkeys(members + union))
        rows = []
        for ind in inds:
            tt = tab[(tab.outcome == o) & (tab.indicator == ind)]
            sgn = spec["signs"][o].get(ind, 1)
            if is_c:
                pl = pool_block(tt, "z", "se_z")
                est = float(np.tanh(pl["b"])) if pl["k"] else np.nan
                ci = [float(np.tanh(pl["ci"][0])), float(np.tanh(pl["ci"][1]))] if pl["k"] else [np.nan] * 2
                vals = tt.set_index("unit").rho
            else:
                pl = pool_block(tt[tt.status == "scored"], "dauc", "se")
                est, ci = pl["b"], pl["ci"]
                vals = tt.set_index("unit").dauc
            signs = [int(np.sign(v)) == sgn for v in vals.reindex(UNITS).to_numpy() if np.isfinite(v)]
            k_agree = int(sum(signs))
            rows.append({"indicator": ind, "family": FAMILY_OF[ind], "in_top10": ind in members,
                         "in_union": ind in union, "frozen_sign": sgn, "pooled": est, "pooled_ci": ci,
                         "pooled_p": pl.get("p"), "tau2": pl.get("tau2"), "I2": pl.get("I2"), "k": pl.get("k"),
                         "sign_agree": k_agree, "n_units": len(signs),
                         "sign_test_p": sign_test_two_sided(k_agree, len(signs)),
                         "previously_scored": ind in PREVIOUSLY_SCORED,
                         "per_unit": {u: (None if not np.isfinite(v) else float(v))
                                      for u, v in vals.reindex(UNITS).items()},
                         "per_unit_ci": {r.unit: [r.ci_lo, r.ci_hi] for r in tt.itertuples()
                                         if np.isfinite(getattr(r, "ci_lo", np.nan))},
                         "per_unit_n": {r.unit: int(r.n) for r in tt.itertuples()}})
        hp = holm([r["pooled_p"] for r in rows if r["in_top10"]])
        k = 0
        for r in rows:
            if r["in_top10"]:
                r["holm_p"] = hp[k]; k += 1
                r["confirmed"] = bool(np.isfinite(r["holm_p"]) and r["holm_p"] < 0.05
                                      and np.sign(r["pooled"]) == r["frozen_sign"])
        summary[o] = rows
    jdump(summary, RES / "heldout_summary.json")
    logger.info(f"held-out scoring done in {(time.time()-t)/60:.1f} min")


def stage_portability(logger, workers: int) -> None:
    feats = INDICATORS + B5
    jobs = []
    for o in ("O2r_m50", "O2r_resid", "O1c"):
        for i, ind in enumerate(feats):
            for u in ALL_UNITS:
                jobs.append(("port", ind, o, u, B_PORT, SEED + 7 * i, None))
    tab = run(jobs, workers, logger, "portability")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    frozen = {(o, d["indicator"]) for o, lst in spec["top10"].items() for d in lst}
    tab["family"] = tab.indicator.map(lambda c: FAMILY_OF.get(c, "B5"))
    tab["status"] = [("FROZEN" if (o, i) in frozen else "EXPLORATORY") for o, i in zip(tab.outcome, tab.indicator)]
    tab["previously_scored"] = tab.indicator.isin(PREVIOUSLY_SCORED)
    tab["unit_type"] = tab.unit.map(lambda u: "DEV" if u in DEV_UNITS else ("HELDOUT" if u in HELD_GROUPS else "COHORT"))
    cols = ["indicator", "family", "unit", "unit_type", "outcome", "n", "rho", "ci_lo", "ci_hi", "raw_rho",
            "raw_ci_lo", "raw_ci_hi", "status", "previously_scored", "se_z", "z", "p"]
    tab[[c for c in cols if c in tab.columns]].to_csv(RES / "portability_table.csv", index=False)
    logger.info(f"portability table: {len(tab)} rows")


def stage_learned(logger) -> None:
    """Learned vs single vs B5 on the SAME held-out units (frozen models), paired concept bootstrap vs B5."""
    import joblib
    from scipy.stats import spearmanr
    from design import apply_design
    from rq1stats import auc, logit_pred
    spec = json.loads((RES / "frozen_spec.json").read_text())
    A = pd.read_parquet(DATA / "analysis_table.parquet")
    lm = json.loads((RES / "learned_model.json").read_text())
    rng = np.random.default_rng(SEED)
    res = {}
    preds_all = []
    for o, m in spec["learned"].items():
        is_bin = o in BIN_OUTCOMES
        d = A[A.split != "DEV"].copy()
        X = apply_design(d, spec["design_spec"])
        Xb = apply_design(d, spec["b5_spec"])
        extra = np.zeros((len(d), 0))
        if m.get("t0_std"):
            extra = ((d.t0.to_numpy(float) - m["t0_std"][0]) / m["t0_std"][1])[:, None]
        b_all = np.c_[Xb, extra]
        P = {}
        if is_bin:
            P["B5"] = logit_pred(np.array(m["B5_coef"]), b_all)
        else:
            c = np.array(m["B5_coef"]); P["B5"] = c[0] + b_all @ c[1:]
        if m.get("best_single"):
            mu, sd, med = m["best_single_std"]
            t1 = d[m["best_single"]].to_numpy(float)
            t1 = (np.where(np.isfinite(t1), t1, med) - mu) / sd
            c = np.array(m["B5_best_single_coef"])
            P["B5_best_single"] = logit_pred(c, np.c_[b_all, t1]) if is_bin else c[0] + np.c_[b_all, t1] @ c[1:]
        lin = joblib.load(MODELS / f"linear_all_{o}.joblib")
        P["linear_all"] = lin.predict_proba(np.c_[X, extra])[:, 1] if is_bin else lin.predict(X)
        if (MODELS / f"ebm_{o}.joblib").exists():
            e = joblib.load(MODELS / f"ebm_{o}.joblib")
            P["EBM"] = e.predict_proba(np.c_[X, extra])[:, 1] if is_bin else e.predict(X)
        pr = pd.DataFrame({"ci": d.ci.to_numpy(), **{f"{o}__{k}": v for k, v in P.items()}})
        preds_all.append(pr.set_index("ci"))
        y = d[o].to_numpy(float)
        res[o] = {}
        for u in UNITS + ["POOLED_HELDOUT"]:
            mk = (d.unit.isin(HELD_GROUPS) if u == "POOLED_HELDOUT" else (d.unit == u)).to_numpy() & np.isfinite(y)
            if mk.sum() < 30 or (is_bin and (y[mk].sum() < MIN_POS or (1 - y[mk]).sum() < MIN_POS)):
                res[o][u] = {"n": int(mk.sum()), "status": "dropped"}
                continue
            yy = y[mk]

            def metric(p, yv):
                if is_bin:
                    return auc(yv, p)
                return float(spearmanr(p, yv)[0])
            r = {"n": int(mk.sum())}
            for k, p in P.items():
                pp = p[mk]
                r[k] = {"metric": metric(pp, yy)}
                if is_bin:
                    r[k]["brier"] = float(np.mean((pp - yy) ** 2))
                    lo = np.log(np.clip(pp, 1e-6, 1 - 1e-6) / (1 - np.clip(pp, 1e-6, 1 - 1e-6)))
                    from rq1stats import logit_fit
                    w = logit_fit(lo[:, None], yy, lam=1e-6)
                    r[k]["calibration_slope"] = float(w[1])
                else:
                    r[k]["r2"] = float(1 - np.sum((yy - pp) ** 2) / np.sum((yy - yy.mean()) ** 2))
            bs = {k: [] for k in P if k != "B5"}
            for _ in range(500):
                j = rng.integers(0, len(yy), len(yy))
                b0 = metric(P["B5"][mk][j], yy[j])
                for k in bs:
                    bs[k].append(metric(P[k][mk][j], yy[j]) - b0)
            for k, v in bs.items():
                v = np.array(v)
                r[k]["delta_vs_B5"] = r[k]["metric"] - r["B5"]["metric"]
                r[k]["delta_ci"] = [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]
            res[o][u] = r
    jdump(res, RES / "learned_vs_single_heldout.json")
    pd.concat(preds_all, axis=1).reset_index().to_parquet(RES / "heldout_predictions.parquet", index=False)
    logger.info("learned vs single scored")


def stage_prereg(logger, workers: int) -> None:
    """P1-P5 verdicts from the portability table (+ B5-minus-reach runs for P4/P5)."""
    from rq1stats import dersimonian_laird
    port = pd.read_csv(RES / "portability_table.csv")
    jobs = [("cont", ind, o, u, B_HELD, SEED + 99, {"drop_reach": True})
            for ind in ("RETENTION_RATIO_early", "FRONTIER_POTENTIAL", "CONTACT_REACH")
            for o in ("O2r_resid", "O1c") for u in HELD_GROUPS]
    nr = run(jobs, workers, logger, "P4/P5 given B5-minus-reach")
    nr.to_csv(RES / "prereg_b5_minus_reach.csv", index=False)

    def pooled(tab, ind, o):
        t = tab[(tab.indicator == ind) & (tab.outcome == o) & tab.unit.isin(HELD_GROUPS)]
        pl = dersimonian_laird(t.z.to_numpy(float), t.se_z.to_numpy(float))
        if not pl["k"]:
            return np.nan, [np.nan, np.nan], t
        return float(np.tanh(pl["b"])), [float(np.tanh(pl["ci"][0])), float(np.tanh(pl["ci"][1]))], t

    def raw_groups(ind):
        t = port[(port.indicator == ind) & (port.outcome == "O2r_m50") & port.unit.isin(HELD_GROUPS)]
        return int((t.raw_ci_lo > 0).sum()), t
    V = {}
    # P1
    det = {}
    ok_raw = True
    for ind in ("entropy", "D_rare", "D_ratio", "participation", "NOV_res"):
        k, t = raw_groups(ind)
        det[ind] = {"n_groups_raw_CI_gt0": k, "raw_rho": dict(zip(t.unit, t.raw_rho))}
        ok_raw &= k >= 3
    ok_small = True
    for ind in ("D_rare", "D_ratio", "participation", "NOV_res"):
        est, ci, _ = pooled(port, ind, "O2r_m50")
        det[ind].update(pooled_psp=est, pooled_ci=ci)
        ok_small &= bool(np.isfinite(ci[1]) and ci[1] < 0.10)
    V["P1"] = {"verdict": "HOLDS" if (ok_raw and ok_small) else "FAILS", "raw_part_holds": bool(ok_raw),
               "adds_little_part_holds": bool(ok_small), "detail": det}
    # P2
    est, ci, _ = pooled(port, "edge_persistence", "O2r_m50")
    t = port[(port.indicator == "edge_persistence") & (port.outcome == "O2r_m50") & port.unit.isin(HELD_GROUPS)]
    raw_mean = float(t.raw_rho.mean())
    V["P2"] = {"verdict": "HOLDS" if (raw_mean < 0 and est < 0) else "FAILS", "pooled_psp": est, "pooled_ci": ci,
               "mean_raw_rho_4_groups": raw_mean, "raw_rho": dict(zip(t.unit, t.raw_rho))}
    # P3
    det = {}
    allfail = True
    for ind in ("deg_growth", "str_growth", "new_edge_rate"):
        est, ci, t = pooled(port, ind, "O2r_m50")
        s = np.sign(t.rho.to_numpy(float))
        flips = int(min((s > 0).sum(), (s < 0).sum()))
        fails = bool((ci[0] <= 0 <= ci[1]) or flips >= 2)
        dev_cs = port[(port.indicator == ind) & (port.outcome == "O2r_m50") & (port.unit == "CS")]
        det[ind] = {"pooled_psp": est, "pooled_ci": ci, "sign_flips": flips, "fails_heldout": fails,
                    "dev_CS_psp": float(dev_cs.rho.iloc[0]) if len(dev_cs) else None}
        allfail &= fails
    V["P3"] = {"verdict": "HOLDS" if allfail else "FAILS", "detail": det}
    # P4
    det = {}
    ok4 = True
    for ind in ("RETENTION_RATIO_early", "FRONTIER_POTENTIAL"):
        for o in ("O2r_resid", "O1c"):
            est, ci, _ = pooled(port, ind, o)
            est2, ci2, _ = pooled(nr, ind, o)
            det[f"{ind}|{o}"] = {"pooled_psp": est, "pooled_ci": ci, "given_B5_minus_reach": est2,
                                 "ci_B5_minus_reach": ci2}
            ok4 &= bool(np.isfinite(ci[0]) and ci[0] > 0)
    V["P4"] = {"verdict": "HOLDS" if ok4 else "FAILS", "detail": det}
    est, ci, _ = pooled(port, "CONTACT_REACH", "O2r_m50")
    est2, ci2, _ = pooled(nr, "CONTACT_REACH", "O2r_resid")
    V["P5"] = {"verdict": "HOLDS" if (ci[0] <= 0 <= ci[1]) else "FAILS", "pooled_psp_O2r_m50": est, "pooled_ci": ci,
               "given_B5_minus_reach_O2r_resid": est2, "ci_B5_minus_reach": ci2}
    jdump(V, RES / "prereg_verdicts.json")
    logger.info("prereg verdicts: " + ", ".join(f"{k}={v['verdict']}" for k, v in V.items()))


def stage_sens(logger, workers: int) -> None:
    spec = json.loads((RES / "frozen_spec.json").read_text())
    jobs = []
    for o in ("O2r_resid", "O1c"):
        for d_ in spec["top10"].get(o, []):
            ind = d_["indicator"]
            for u in HELD_GROUPS:
                jobs.append(("cont", ind, o, u, B_SENS, SEED + 5, {"subset": "no_exp6", "tag": "excl_in_exp6"}))
                jobs.append(("cont", ind, o, u, B_SENS, SEED + 5, {"subset": "no_intersection", "tag": "excl_intersection"}))
                jobs.append(("cont", ind, o, u, B_SENS, SEED + 5, {"covs": ["label_coverage_early", "tag_coverage",
                                                                             "precision_c"], "tag": "coverage_covs"}))
    for d_ in spec["top10"].get("O2r_resid", []):
        for u in HELD_GROUPS:
            jobs.append(("cont", d_["indicator"], "O2r_resid_N", u, B_SENS, SEED + 5, {"tag": "O2r_resid_N_exp5_definition"}))
    for d_ in spec["top10"].get("O2r_m50", []):
        for u in HELD_GROUPS:
            jobs.append(("cont", d_["indicator"], "O2r_m30", u, B_SENS, SEED + 5, {"tag": "O2r_m30"}))
    for o, o2 in (("O5", "O5_sens"), ("O5_WW", "O5_WW_sens")):
        for d_ in spec["top10"].get(o, []):
            for u in UNITS:
                jobs.append(("bin", d_["indicator"], o2, u, B_SENS, SEED + 5, {"tag": "relation_same_or_narrower"}))
    tags = [j[6]["tag"] for j in jobs]
    tab = run(jobs, workers, logger, "sensitivities")
    tab["sensitivity"] = tags
    tab.to_csv(RES / "sensitivities_heldout.csv", index=False)
    from rq1stats import dersimonian_laird
    summ = []
    for (s, o, ind), t in tab[tab.unit.isin(HELD_GROUPS)].groupby(["sensitivity", "outcome", "indicator"]):
        if "z" in t and t.z.notna().any():
            pl = dersimonian_laird(t.z.to_numpy(float), t.se_z.to_numpy(float))
            summ.append({"sensitivity": s, "outcome": o, "indicator": ind, "pooled": float(np.tanh(pl["b"])) if pl["k"] else None,
                         "ci": [float(np.tanh(c)) for c in pl["ci"]] if pl["k"] else None, "I2": pl.get("I2")})
        elif "dauc" in t:
            tt = t[t.get("status", pd.Series("")).eq("scored")] if "status" in t else t
            pl = dersimonian_laird(tt.dauc.to_numpy(float), tt.se.to_numpy(float)) if len(tt) else {"k": 0}
            summ.append({"sensitivity": s, "outcome": o, "indicator": ind, "pooled": pl.get("b"), "ci": pl.get("ci"),
                         "I2": pl.get("I2")})
    jdump(summ, RES / "sensitivities_pooled.json")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    logger = setup_logger("heldout")
    st = a.stage
    if st in ("all", "unseal"):
        stage_unseal(logger)
    if st in ("all", "score"):
        stage_score(logger, a.workers)
    if st in ("all", "learned"):
        stage_learned(logger)
    if st in ("all", "port"):
        stage_portability(logger, a.workers)
    if st in ("all", "prereg"):
        stage_prereg(logger, a.workers)
    if st in ("all", "sens"):
        stage_sens(logger, a.workers)


if __name__ == "__main__":
    main()
