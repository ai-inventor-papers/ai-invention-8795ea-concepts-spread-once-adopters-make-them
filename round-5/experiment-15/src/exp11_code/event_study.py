#!/usr/bin/env python3
"""Step 5c (post-seal): Sun-Abraham interaction-weighted event study around the FIRST home-only closure jump
(data/closure_jumps.parquet, frozen before the seal).

Per body: outcome entries(t+1) (primary) and entries(t); never-treated controls (primary) and last-treated cohort
(not-yet-treated) variant; 1,000 concept-cluster bootstrap draws (DEV; 300 elsewhere) -> SEs, CIs, lead Wald test with
the bootstrap covariance, Roth-style detectable pre-trend slope; event-date permutation placebo (1,000 draws, DEV);
home-volume mechanical check (outcome log1p home works(t)); pyfixest cross-check of the CATT cells (1e-6).
Writes results/event_study.json and data/es_boot_*.parquet. Also exposes run_es() for the sequence tests."""
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

from common import DATA, DATA_IN, RES, RES_IN, jdump, setup_logger

warnings.filterwarnings("ignore")
SEED = 20260929
ES_CONTROLS = ["log1p_home", "log1p_all", "log_at_risk"]
REL = [-3, -2, 0, 1, 2, 3, 4]
_G: dict = {}


def _winit(df: pd.DataFrame) -> None:
    os.environ.setdefault("NUMBA_NUM_THREADS", "1")
    warnings.filterwarnings("ignore")
    from fe_stats import cluster_index
    _G["df"] = df
    _G["idx"] = cluster_index(df.ci.to_numpy())


def _boot(y: str, controls: list[str], g_col: str, control: str, seeds: list[int]) -> list[dict]:
    from fe_stats import cluster_resample, sun_abraham
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        d = cluster_resample(_G["df"], _G["idx"], rng)
        try:
            r = sun_abraham(d, y, controls, g_col, control)
            out.append({**{f"e{k}": r["att"][k] for k in REL}, "lag02": r["mean_lag_0_2"]})
        except (np.linalg.LinAlgError, ValueError, KeyError) as e:
            out.append({"error": repr(e)[:200]})
    return out


def _perm(y: str, controls: list[str], seeds: list[int]) -> list[float]:
    """Event-date permutation: each treated concept's jump year is redrawn uniformly among its eligible years."""
    from fe_stats import sun_abraham
    df = _G["df"]
    tr = df.drop_duplicates("ci")
    tr = tr[tr.g.notna()][["ci", "eligible_years"]]
    el = {c: [int(v) for v in s.split(",") if v] for c, s in zip(tr.ci, tr.eligible_years)}
    out = []
    for s in seeds:
        rng = np.random.default_rng(s)
        newg = {c: (rng.choice(v) if len(v) else np.nan) for c, v in el.items()}
        d = df.copy()
        d["g"] = d.ci.map(newg)
        try:
            out.append(float(sun_abraham(d, y, controls, "g", "never")["mean_lag_0_2"]))
        except (np.linalg.LinAlgError, ValueError, KeyError):
            out.append(float("nan"))
    return out


def run_es(df: pd.DataFrame, y: str, controls: list[str], g_col: str = "g", control: str = "never",
           n_boot: int = 1000, workers: int = 20, tag: str = "", crosscheck: bool = False) -> dict:
    from fe_stats import roth_power_slope, sun_abraham, wald
    t = time.time()
    df = df[np.isfinite(df[y])].copy()
    for c in controls:
        df = df[np.isfinite(df[c])]
    pt = sun_abraham(df, y, controls, g_col, control)
    res = {"att": {str(k): pt["att"][k] for k in REL}, "mean_lag_0_2": pt["mean_lag_0_2"], "n": pt["n"],
           "n_concepts": pt["n_concepts"], "n_treated": pt["n_treated"], "n_cells": pt["n_cells"],
           "control": control, "outcome": y}
    cohort_n = {}
    for c, (g, k, n) in pt["meta"].items():
        if k in REL:
            cohort_n.setdefault(str(k), 0)
            cohort_n[str(k)] += n
    res["treated_rows_by_e"] = cohort_n
    if n_boot:
        seeds = [SEED + 7919 * i for i in range(n_boot)]
        chunks = [seeds[i::workers * 2] for i in range(workers * 2)]
        dd = df.rename(columns={g_col: "g"}) if g_col != "g" else df
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_winit,
                                 initargs=(dd,)) as ex:
            B = pd.DataFrame([r for part in ex.map(_boot, [y] * len(chunks), [controls] * len(chunks),
                                                    ["g"] * len(chunks), [control] * len(chunks), chunks)
                              for r in part])
        if tag:
            B.to_parquet(DATA / f"es_boot_{tag}.parquet", index=False)
        ok = B.drop(columns=[c for c in B.columns if c == "error"]).dropna()
        res["n_boot_ok"] = int(len(ok))
        res["se"] = {str(k): float(ok[f"e{k}"].std(ddof=1)) for k in REL}
        res["ci"] = {str(k): [float(np.percentile(ok[f"e{k}"], 2.5)), float(np.percentile(ok[f"e{k}"], 97.5))]
                     for k in REL}
        res["lag02_se"] = float(ok.lag02.std(ddof=1))
        res["lag02_ci"] = [float(np.percentile(ok.lag02, 2.5)), float(np.percentile(ok.lag02, 97.5))]
        leads = np.array([pt["att"][-3], pt["att"][-2]])
        V = np.cov(ok[["e-3", "e-2"]].to_numpy().T)
        W, pw = wald(leads, V)
        res["pretrend_wald"] = {"W": W, "p": pw, "df": 2}
        res["roth_detectable_slope_80pct"] = roth_power_slope(V, [-3, -2])
        res["max_abs_lead"] = float(np.max(np.abs(leads)))
        res["lead_small_vs_lag"] = bool(res["max_abs_lead"] < 0.5 * abs(pt["mean_lag_0_2"]))
    if crosscheck:
        from fe_stats import feols_pf, sa_design
        d, cols, meta = sa_design(df, g_col, 3, 4, control)
        f = feols_pf(d, y, cols + controls)
        co = f.coef()
        diffs = [abs(co[c] - pt["b"][c]) for c in cols if c in co.index and np.isfinite(pt["b"][c])]
        res["crosscheck_pyfixest_max_abs_diff"] = float(max(diffs)) if diffs else None
        res["crosscheck_n_cells"] = len(diffs)
    res["seconds"] = time.time() - t
    return res


def es_panel(p: pd.DataFrame, cj: pd.DataFrame, body: str) -> pd.DataFrame:
    d = p[(p.body == body) & (p.at_risk_next > 0) & p.y_next.notna()]
    d = d.merge(cj[["ci", "t_jump", "es_eligible", "eligible_years"]], on="ci", how="left")
    d = d[d.es_eligible == 1].copy()
    d["g"] = d.t_jump
    d["log1p_entries_t"] = np.log1p(d.entries)
    return d


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=1000)
    ap.add_argument("--boot-other", type=int, default=300)
    ap.add_argument("--perm", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=20)
    args = ap.parse_args()
    logger = setup_logger("event_study")
    from seal_m import check_seal
    check_seal()
    t = time.time()
    p = pd.read_parquet(DATA_IN / "yearly_panel.parquet")
    cj = pd.read_parquet(DATA_IN / "closure_jumps.parquet")
    out: dict = {"k_sd": json.loads((RES_IN / "frozen_spec.json").read_text())["estimators"]["closure_jump"]}
    for body in ("DEV", "OLD_HELDOUT", "COHORT"):
        d = es_panel(p, cj, body)
        nb = args.boot if body == "DEV" else args.boot_other
        rb = {"n_eligible": int(d.ci.nunique()), "n_treated": int(d.loc[d.g.notna(), "ci"].nunique()),
              "cohorts": {str(int(k)): int(v) for k, v in d.drop_duplicates("ci").g.value_counts().sort_index().items()}}
        rb["primary_never"] = run_es(d, "y_next", ES_CONTROLS, "g", "never", nb, args.workers, f"{body}_never",
                                     crosscheck=(body == "DEV"))
        logger.info(f"{body} never-treated: lag02={rb['primary_never']['mean_lag_0_2']:.4f} "
                    f"CI={rb['primary_never'].get('lag02_ci')} pre p={rb['primary_never'].get('pretrend_wald')}")
        rb["not_yet_treated_last_cohort"] = run_es(d, "y_next", ES_CONTROLS, "g", "last", nb, args.workers,
                                                   f"{body}_last")
        if body == "DEV":
            rb["outcome_entries_t"] = run_es(d, "entries", ES_CONTROLS, "g", "never", nb, args.workers, "DEV_entries_t")
            rb["mechanical_home_volume"] = run_es(d, "log1p_home", ["log1p_all", "log_at_risk"], "g", "never", nb,
                                                  args.workers, "DEV_homevol")
            seeds = [SEED + 104729 * i for i in range(args.perm)]
            chunks = [seeds[i::args.workers * 2] for i in range(args.workers * 2)]
            with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"), initializer=_winit,
                                     initargs=(d,)) as ex:
                perm = np.array([v for part in ex.map(_perm, ["y_next"] * len(chunks), [ES_CONTROLS] * len(chunks),
                                                      chunks) for v in part])
            obs = rb["primary_never"]["mean_lag_0_2"]
            pv = perm[np.isfinite(perm)]
            rb["placebo_event_date"] = {"n": int(len(pv)), "mean": float(pv.mean()), "sd": float(pv.std(ddof=1)),
                                        "q025_q975": [float(np.percentile(pv, 2.5)), float(np.percentile(pv, 97.5))],
                                        "p_one_sided_le_obs": float((1 + (pv <= obs).sum()) / (1 + len(pv))),
                                        "p_two_sided": float((1 + (np.abs(pv - pv.mean()) >= abs(obs - pv.mean())).sum())
                                                             / (1 + len(pv)))}
            np.save(DATA / "es_placebo_perm_DEV.npy", perm)
            logger.info(f"placebo: {rb['placebo_event_date']}")
        out[body] = rb
        jdump(out, RES / "event_study.json")
    pn = out["DEV"]["primary_never"]
    out["H_M4"] = {"mean_lag_0_2": pn["mean_lag_0_2"], "ci": pn.get("lag02_ci"),
                   "lag_negative_ci_below_0": bool(pn.get("lag02_ci") and pn["lag02_ci"][1] < 0),
                   "pretrend_p": pn.get("pretrend_wald", {}).get("p"), "lead_small_vs_lag": pn.get("lead_small_vs_lag"),
                   "placebo_p_one_sided": out["DEV"]["placebo_event_date"]["p_one_sided_le_obs"]}
    out["H_M4"]["holds"] = bool(out["H_M4"]["lag_negative_ci_below_0"] and (out["H_M4"]["pretrend_p"] or 0) > 0.10
                                and out["H_M4"]["lead_small_vs_lag"] and out["H_M4"]["placebo_p_one_sided"] < 0.05)
    out["seconds"] = time.time() - t
    jdump(out, RES / "event_study.json")
    logger.info(f"event study done: H-M4 {out['H_M4']} ({(time.time()-t)/60:.1f} min)")


if __name__ == "__main__":
    main()
