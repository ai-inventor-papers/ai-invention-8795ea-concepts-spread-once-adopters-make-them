#!/usr/bin/env python3
"""Step 5b (post-seal): within-concept FE estimation.

Attaches the D3 outcomes through the seal gate, builds the panel (lib/panel_m.build_panel) and estimates per body:
  * H-M1 / H-M2: PPML entries(t+1) ~ density(t) [OPEN_home(t)] + controls | concept + year FE (CRV1 by concept),
    plus 2,000 (DEV) concept-cluster bootstrap refits; LPM twin on any_entry(t+1); joint model
  * H-M3: forward entries(t+1) ~ density(t) vs reverse density(t+1) ~ entries(t), both FE-OLS, standardised by
    FE-demeaned SDs, paired concept bootstrap of |std fwd| - |std rev| (same resamples as H-M1/H-M2)
  * per group within body -> DL pooling with I2
  * pre-declared robustness list on DEV
  * out-of-fold predictions (5 concept folds on DEV; DEV-trained slopes transferred to the other bodies) of three
    PPML models (density, OPEN_home, controls only) for method_out.json
Writes data/yearly_panel.parquet, results/fe_results.json, data/predictions.parquet."""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, LOGS_IN, RES, RES_IN, jdump, load_frame, setup_logger
from panel_m import BODIES, CONTROLS, build_panel, estimation_sample, frame_plus

warnings.filterwarnings("ignore")
SEED = 20260929
_G: dict = {}


def _winit(dfs: dict) -> None:
    os.environ.setdefault("NUMBA_NUM_THREADS", "2")
    warnings.filterwarnings("ignore")
    from fe_stats import cluster_index
    _G["dfs"] = dfs
    _G["idx"] = {k: cluster_index(v.ci.to_numpy()) for k, v in dfs.items()}


def hm3_stat(fw: pd.DataFrame, rv: pd.DataFrame) -> dict:
    from fe_stats import feols_np, within_sd
    c, t = fw.ci.to_numpy(), fw.year.to_numpy()
    f = feols_np(fw.y_next.to_numpy(float), fw[["density"] + CONTROLS].to_numpy(float), [c, t], c,
                 ["density"] + CONTROLS)["b"]["density"]
    sf = f * within_sd(fw.density.to_numpy(float), c, t) / within_sd(fw.y_next.to_numpy(float), c, t)
    c2, t2 = rv.ci.to_numpy(), rv.year.to_numpy()
    rc = ["log1p_home_next", "log1p_all_next", "log1p_deg_next", "log_at_risk_next"]
    r = feols_np(rv.density_next.to_numpy(float), rv[["entries"] + rc].to_numpy(float), [c2, t2], c2,
                 ["entries"] + rc)["b"]["entries"]
    sr = r * within_sd(rv.entries.to_numpy(float), c2, t2) / within_sd(rv.density_next.to_numpy(float), c2, t2)
    return {"b_fwd": f, "b_rev": r, "std_fwd": sf, "std_rev": sr, "diff": abs(sf) - abs(sr)}


def boot_task(body: str, seeds: list[int]) -> list[dict]:
    from fe_stats import cluster_resample, ppml
    fw, rv = _G["dfs"][f"{body}_fw"], _G["dfs"][f"{body}_rv"]
    ifw, irv = _G["idx"][f"{body}_fw"], _G["idx"][f"{body}_rv"]
    # paired: the SAME resampled concept ids for forward and reverse samples
    ids_fw = np.array(sorted(fw.ci.unique()))
    pos_rv = {c: i for i, c in enumerate(sorted(rv.ci.unique()))}
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        pick = rng.integers(0, len(ids_fw), len(ids_fw))
        rows = np.concatenate([ifw[p] for p in pick])
        newid = np.concatenate([np.full(len(ifw[p]), j) for j, p in enumerate(pick)])
        d = fw.iloc[rows].copy(); d["ci"] = newid
        rr = [(irv[pos_rv[ids_fw[p]]], j) for j, p in enumerate(pick) if ids_fw[p] in pos_rv]
        r = rv.iloc[np.concatenate([a for a, _ in rr])].copy()
        r["ci"] = np.concatenate([np.full(len(a), j) for a, j in rr])
        rec = {"seed": s}
        try:
            rec["b_density"] = float(ppml(d, "y_next", ["density"] + CONTROLS, vcov="iid").coef()["density"])
            dO = d[np.isfinite(d.OPEN_home)]
            rec["b_open"] = float(ppml(dO, "y_next", ["OPEN_home"] + CONTROLS, vcov="iid").coef()["OPEN_home"])
            rec.update(hm3_stat(d, r))
        except Exception as e:  # noqa: BLE001 -- a failed resample is recorded, not fatal
            rec["error"] = repr(e)[:200]
        out.append(rec)
    return out


def summ(fit, x) -> dict:
    from fe_stats import ppml_summary
    return ppml_summary(fit, x)


def lpm_summ(fit, x) -> dict:
    ci = fit.confint().loc[x].to_numpy(float)
    return {"b": float(fit.coef()[x]), "se": float(fit.se()[x]), "ci": [float(ci[0]), float(ci[1])],
            "p": float(fit.pvalue()[x]), "n": int(fit._N)}


def safe(fn, *a, **k) -> dict:
    try:
        return fn(*a, **k)
    except Exception as e:  # noqa: BLE001 -- robustness cells must not abort the run
        return {"error": repr(e)[:300]}


def ppml_x(df: pd.DataFrame, x: str, controls=CONTROLS, fe: str = "ci + year", offset: str | None = None,
           y: str = "y_next") -> dict:
    from fe_stats import ppml
    d = df[np.isfinite(df[x])]
    f = ppml(d, y, [x] + list(controls), fe=fe, offset=offset)
    r = summ(f, x)
    r["n_concepts_used"] = int(d.ci.nunique())
    r["sd_within_x"] = float(np.std(d[x] - d.groupby("ci")[x].transform("mean"), ddof=1))
    r["pct_per_within_sd"] = float(100 * (np.exp(r["b"] * r["sd_within_x"]) - 1))
    return r


def reverse_sample(p: pd.DataFrame) -> pd.DataFrame:
    return p[(p.deg_next >= 2) & p.density_next.notna() & (p.at_risk > 0) & p.entries.notna()].copy()


def body_results(p: pd.DataFrame, body: str, n_boot: int, workers: int, logger) -> dict:
    from fe_stats import feols_pf
    from rq1stats import dersimonian_laird
    t = time.time()
    fw = estimation_sample(p[p.body == body])
    rv = reverse_sample(p[p.body == body])
    res: dict = {"n_rows": int(len(fw)), "n_concepts": int(fw.ci.nunique()),
                 "share_rows_all_zero_concepts": float((fw.groupby("ci").y_next.transform("sum") == 0).mean()),
                 "mean_y_next": float(fw.y_next.mean()), "share_any_next": float(fw.any_next.mean())}
    res["H_M1_density"] = ppml_x(fw, "density")
    res["H_M2_open"] = ppml_x(fw, "OPEN_home")
    res["joint"] = safe(lambda: {x: summ(f, x) for f in [__import__("fe_stats").ppml(
        fw[np.isfinite(fw.OPEN_home)], "y_next", ["density", "OPEN_home"] + CONTROLS)] for x in ("density", "OPEN_home")})
    res["lpm_density"] = safe(lambda: lpm_summ(feols_pf(fw, "any_next", ["density"] + CONTROLS), "density"))
    res["lpm_open"] = safe(lambda: lpm_summ(feols_pf(fw[np.isfinite(fw.OPEN_home)], "any_next",
                                                     ["OPEN_home"] + CONTROLS), "OPEN_home"))
    res["H_M3_point"] = hm3_stat(fw, rv)
    res["H_M3_point"]["n_fwd"], res["H_M3_point"]["n_rev"] = int(len(fw)), int(len(rv))
    # per group -> DL pooling
    grp = {}
    for g, d in fw.groupby("group"):
        if d.ci.nunique() < 30:
            continue
        grp[g] = {"density": safe(ppml_x, d, "density"), "OPEN_home": safe(ppml_x, d, "OPEN_home"),
                  "n_concepts": int(d.ci.nunique())}
    res["by_group"] = grp
    for x in ("density", "OPEN_home"):
        bs = [(v[x]["b"], v[x]["se"]) for v in grp.values() if "b" in v[x]]
        res[f"DL_{x}"] = dersimonian_laird(np.array([b for b, _ in bs]), np.array([s for _, s in bs])) if bs else {}
    # bootstrap
    if n_boot:
        seeds = [SEED * 10 + i for i in range(n_boot)]
        chunks = [seeds[i::workers * 3] for i in range(workers * 3)]
        dfs = {f"{body}_fw": fw, f"{body}_rv": rv}
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_winit,
                                 initargs=(dfs,)) as ex:
            bl = [r for part in ex.map(boot_task, [body] * len(chunks), chunks) for r in part]
        B = pd.DataFrame(bl)
        res["bootstrap"] = {"n_boot": n_boot, "n_failed": int(B["error"].notna().sum()) if "error" in B else 0}
        for k in ("b_density", "b_open", "std_fwd", "std_rev", "diff"):
            v = B[k].dropna().to_numpy(float) if k in B else np.array([])
            res["bootstrap"][k] = {"mean": float(v.mean()) if len(v) else None, "sd": float(v.std(ddof=1)) if len(v) > 1 else None,
                                   "ci": [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else None,
                                   "p_two_sided_sign": float(2 * min((v <= 0).mean(), (v >= 0).mean())) if len(v) else None,
                                   "n": int(len(v))}
        B.to_parquet(DATA / f"boot_fe_{body}.parquet", index=False)
    logger.info(f"{body}: {res['n_rows']} rows / {res['n_concepts']} concepts; density b={res['H_M1_density'].get('b'):.4f} "
                f"OPEN b={res['H_M2_open'].get('b'):.4f} H-M3 diff={res['H_M3_point']['diff']:.4f} ({time.time()-t:.0f}s)")
    return res


def robustness(p: pd.DataFrame, logger) -> dict:
    fw = estimation_sample(p[p.body == "DEV"])
    R = {}
    R["dens_adj"] = safe(ppml_x, fw, "dens_adj")
    for nm, d in {"excl_Med": fw[fw.group != "Med"], "excl_intersection_born": fw[fw.multi_home == 0],
                  "drop_year_ge_2015": fw[fw.year < 2015], "home_cov_ge_0.5": fw[fw.home_cov >= 0.5]}.items():
        R[nm] = {"density": safe(ppml_x, d, "density"), "OPEN_home": safe(ppml_x, d, "OPEN_home")}
    fa = estimation_sample(p[p.body == "DEV"].assign(deg=p.loc[p.body == "DEV", "deg_all"]))
    fa = fa.assign(log1p_deg=np.log1p(fa.deg_all))
    R["ALL_PAPERS_density_contrast"] = safe(ppml_x, fa, "density_all")
    R["offset_log_at_risk"] = {x: safe(ppml_x, fw, x, controls=CONTROLS[:3], offset="log_at_risk")
                               for x in ("density", "OPEN_home")}
    R["S1_age_FE"] = {x: safe(ppml_x, fw.assign(agefe=fw.age), x, fe="ci + agefe") for x in ("density", "OPEN_home")}
    R["S2_add_cum_entries"] = {x: safe(ppml_x, fw, x, controls=CONTROLS + ["cum_entries_t"])
                               for x in ("density", "OPEN_home")}
    R["S3_home_field_x_year_FE"] = {x: safe(ppml_x, fw, x, fe="ci + home_year") for x in ("density", "OPEN_home")}
    R["no_log_deg_control"] = {x: safe(ppml_x, fw, x, controls=[c for c in CONTROLS if c != "log1p_deg"])
                               for x in ("density", "OPEN_home")}
    R["components"] = {c: safe(ppml_x, fw, c) for c in ("new_rate", "n_comm", "participation", "nov_res",
                                                          "persistence", "kcore")}
    logger.info("robustness done")
    return R


def oof_predictions(p: pd.DataFrame, logger) -> pd.DataFrame:
    """Slopes + year FE from training folds (PPML); concept FE by the Poisson closed form on the concept's own rows."""
    from fe_stats import ppml
    models = {"fe_density": ["density"] + CONTROLS, "fe_open": ["OPEN_home"] + CONTROLS, "controls_only": CONTROLS}
    allrows = estimation_sample(p)
    allrows = allrows[np.isfinite(allrows.OPEN_home)].copy()
    dev = allrows[allrows.body == "DEV"]
    ids = np.array(sorted(dev.ci.unique()))
    rng = np.random.default_rng(SEED)
    fold = dict(zip(ids, rng.integers(0, 5, len(ids))))
    allrows["fold"] = allrows.ci.map(fold).fillna(-1).astype(int)

    def predict(train: pd.DataFrame, test: pd.DataFrame, xs: list[str]) -> np.ndarray:
        f = ppml(train, "y_next", xs, vcov="iid")
        b = f.coef()[xs].to_numpy(float)
        fx = f.fixef()
        yfe = {int(float(k)): v for k, v in fx["C(year)"].items()}
        dt = test.year.map(lambda y: yfe.get(int(y), np.nan)).to_numpy(float)
        dt = np.where(np.isfinite(dt), dt, np.nanmean(list(yfe.values())))
        eta = test[xs].to_numpy(float) @ b + dt
        e = np.exp(eta)
        s_y = test.groupby("ci").y_next.transform("sum").to_numpy(float)
        s_e = pd.Series(e, index=test.index).groupby(test.ci).transform("sum").to_numpy(float)
        return np.where(s_y > 0, e * s_y / s_e, 0.0)
    out = allrows[["ci", "year", "body", "group", "age", "y_next", "density", "OPEN_home"] + CONTROLS + ["fold"]].copy()
    for m, xs in models.items():
        pred = np.full(len(allrows), np.nan)
        for k in range(5):
            te = (allrows.fold == k).to_numpy()
            pred[te] = predict(dev[dev.ci.map(fold) != k], allrows[te], xs)
        te = (allrows.fold == -1).to_numpy()
        pred[te] = predict(dev, allrows[te], xs)
        out[f"pred_{m}"] = pred
    logger.info(f"predictions for {len(out)} rows")
    return out


def deviance(y: np.ndarray, mu: np.ndarray) -> float:
    mu = np.clip(mu, 1e-12, None)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = np.where(y > 0, y * np.log(y / mu), 0.0) - (y - mu)
    return float(2 * np.mean(t))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot-dev", type=int, default=2000)
    ap.add_argument("--boot-other", type=int, default=500)
    ap.add_argument("--workers", type=int, default=20)
    args = ap.parse_args()
    logger = setup_logger("analysis_fe")
    t = time.time()
    from seal_m import attach_outcomes
    spec = json.loads((RES_IN / "frozen_spec.json").read_text())
    zc = spec["features"]["z_constants"]
    fr = frame_plus(load_frame())
    yf = pd.read_parquet(DATA_IN / "yearly_features.parquet")
    yo = attach_outcomes(yf, reason="analysis_fe primary run")
    p = build_panel(yo, fr, zc)
    p.drop(columns=["home_list"]).to_parquet(DATA / "yearly_panel.parquet", index=False)
    logger.info(f"panel {p.shape}; estimation rows {len(estimation_sample(p))}")
    res = {"spec_sha": json.loads((LOGS_IN / "seal.log").read_text())["frozen_spec_sha256"]}
    counts = {}
    for b in BODIES:
        pb = p[p.body == b]
        counts[b] = {"concept_years_t0_to_hend_minus1": int(len(pb)), "concepts": int(pb.ci.nunique()),
                     "rows_at_risk": int((pb.at_risk_next > 0).sum()),
                     "rows_deg_ge2_at_risk": int(((pb.at_risk_next > 0) & (pb.deg >= 2)).sum()),
                     "dropped_share_deg_lt2": float(((pb.at_risk_next > 0) & (pb.deg < 2)).sum() / max((pb.at_risk_next > 0).sum(), 1))}
    res["sample_counts"] = counts
    for b in BODIES:
        res[b] = body_results(p, b, args.boot_dev if b == "DEV" else args.boot_other, args.workers, logger)
        jdump(res, RES / "fe_results.json")
    res["robustness_DEV"] = robustness(p, logger)
    jdump(res, RES / "fe_results.json")
    pr = oof_predictions(p, logger)
    pr.to_parquet(DATA / "predictions.parquet", index=False)
    res["prediction_deviance"] = {b: {m: deviance(d.y_next.to_numpy(float), d[f"pred_{m}"].to_numpy(float))
                                      for m in ("fe_density", "fe_open", "controls_only")}
                                  for b, d in pr.groupby("body")}
    jdump(res, RES / "fe_results.json")
    logger.info(f"analysis_fe done in {(time.time()-t)/60:.1f} min")


if __name__ == "__main__":
    main()
