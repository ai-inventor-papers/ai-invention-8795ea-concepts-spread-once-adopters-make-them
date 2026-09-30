#!/usr/bin/env python3
"""iter-5 STEP 2 (Part C.2): the sealed Exp11 Sun-Abraham event study, run from the SEALED event_study.run_es /
fe_stats.sun_abraham code with the thread-explosion fix (OPENBLAS/OMP/MKL/NUMBA threads = 1, <= 4 workers).

Differences from event_study.main (logged as deviations): draw counts are set per cell by a timing gate; every
(body, variant) cell is checkpointed into results/event_study.json and skipped on resume; figures are drawn.
H-M4 is evaluated exactly as sealed. Usage: python run_event_study.py --timing-only | --workers 4 [--subsample]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, FIGS, RES, RES_IN, add_deviation, jdump, setup_logger

SEED = 20260929
PLAN = {  # draws requested by the plan (before the timing gate)
    ("DEV", "primary_never"): 1000, ("DEV", "not_yet_treated_last_cohort"): 500,
    ("DEV", "outcome_entries_t"): 300, ("DEV", "mechanical_home_volume"): 300,
    ("OLD_HELDOUT", "primary_never"): 300, ("OLD_HELDOUT", "not_yet_treated_last_cohort"): 300,
    ("COHORT", "primary_never"): 300, ("COHORT", "not_yet_treated_last_cohort"): 300,
}
N_PERM = 1000


def cell_args(variant: str) -> tuple[str, list[str], str]:
    from event_study import ES_CONTROLS
    return {"primary_never": ("y_next", ES_CONTROLS, "never"),
            "not_yet_treated_last_cohort": ("y_next", ES_CONTROLS, "last"),
            "outcome_entries_t": ("entries", ES_CONTROLS, "never"),
            "mechanical_home_volume": ("log1p_home", ["log1p_all", "log_at_risk"], "never")}[variant]


def stratified_half(d: pd.DataFrame) -> pd.DataFrame:
    c = d.drop_duplicates("ci")[["ci", "group", "g"]].copy()
    c["tr"] = c.g.notna().astype(int)
    rng = np.random.default_rng(SEED)
    keep = []
    for _, s in c.groupby(["group", "tr"]):
        ids = s.ci.to_numpy()
        keep += list(rng.choice(ids, int(np.ceil(len(ids) / 2)), replace=False))
    return d[d.ci.isin(set(keep))].copy()


def timing(d: pd.DataFrame, logger) -> float:
    from event_study import ES_CONTROLS
    from fe_stats import cluster_index, cluster_resample, sun_abraham
    idx = cluster_index(d.ci.to_numpy())
    ts = []
    for s in range(3):
        dd = cluster_resample(d, idx, np.random.default_rng(s))
        t = time.time()
        sun_abraham(dd, "y_next", ES_CONTROLS, "g", "never")
        ts.append(time.time() - t)
    logger.info(f"timing gate: sun_abraham on DEV never-treated resamples {ts}")
    return float(np.mean(ts))


def perm_placebo(d: pd.DataFrame, obs: float, n_perm: int, workers: int) -> tuple[dict, np.ndarray]:
    import event_study as ES
    seeds = [SEED + 104729 * i for i in range(n_perm)]
    chunks = [seeds[i::workers * 4] for i in range(workers * 4)]
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=ES._winit,
                             initargs=(d,)) as ex:
        perm = np.array([v for part in ex.map(ES._perm, ["y_next"] * len(chunks), [ES.ES_CONTROLS] * len(chunks),
                                              chunks) for v in part])
    pv = perm[np.isfinite(perm)]
    return {"n": int(len(pv)), "mean": float(pv.mean()), "sd": float(pv.std(ddof=1)),
            "q025_q975": [float(np.percentile(pv, 2.5)), float(np.percentile(pv, 97.5))],
            "p_one_sided_le_obs": float((1 + (pv <= obs).sum()) / (1 + len(pv))),
            "p_two_sided": float((1 + (np.abs(pv - pv.mean()) >= abs(obs - pv.mean())).sum()) / (1 + len(pv))),
            "observed": obs}, perm


def plot_cell(r: dict, body: str, variant: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ks = [-3, -2, -1, 0, 1, 2, 3, 4]
    att = [0.0 if k == -1 else r["att"][str(k)] for k in ks]
    ci = [[0.0, 0.0] if k == -1 else (r.get("ci", {}).get(str(k)) or [np.nan, np.nan]) for k in ks]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.axhline(0, color="grey", lw=0.8)
    ax.axvline(-0.5, color="grey", ls=":", lw=0.8)
    ax.errorbar(ks, att, yerr=[np.array(att) - np.array([c[0] for c in ci]), np.array([c[1] for c in ci]) - np.array(att)],
                fmt="o", capsize=3, color="#1f77b4")
    for k in ks:
        n = r.get("treated_rows_by_e", {}).get(str(k))
        if n:
            ax.annotate(f"n={n}", (k, ax.get_ylim()[0]), fontsize=7, ha="center", va="bottom", color="dimgrey")
    ax.set_xlabel("years relative to first home-only closure jump (e=-1 reference)")
    ax.set_ylabel(f"ATT on {r['outcome']}")
    ax.set_title(f"{body} - {variant} (Sun-Abraham IW, {r.get('n_boot_ok', 0)} boots)", fontsize=9)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"es_{body}_{variant}.{ext}", dpi=150)
    plt.close(fig)


def plot_placebo(perm: np.ndarray, obs: float) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(5, 3.4))
    ax.hist(perm[np.isfinite(perm)], bins=40, color="#9ecae1", edgecolor="white")
    ax.axvline(obs, color="#d62728", lw=2, label=f"observed mean lag 0..2 = {obs:.3f}")
    ax.set_xlabel("mean lag 0..2 under randomised event dates")
    ax.legend(fontsize=8)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(FIGS / f"es_placebo_DEV.{ext}", dpi=150)
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--timing-only", action="store_true")
    ap.add_argument("--budget-min", type=float, default=100.0)
    ap.add_argument("--scale", type=float, default=1.0, help="multiply all draw counts (mini runs)")
    ap.add_argument("--out", default="event_study.json")
    args = ap.parse_args()
    logger = setup_logger("run_event_study")
    import event_study as ES
    from seal_m import check_seal
    check_seal()
    t0 = time.time()
    p = pd.read_parquet(DATA_IN / "yearly_panel.parquet")
    cj = pd.read_parquet(DATA_IN / "closure_jumps.parquet")
    dev = ES.es_panel(p, cj, "DEV")
    spf = timing(dev, logger)
    draws = {k: max(2, int(round(v * args.scale))) for k, v in PLAN.items()}
    n_perm = max(2, int(round(N_PERM * args.scale)))
    fits = sum(draws.values()) + n_perm
    projected = spf * fits / args.workers / 60
    gate = {"sec_per_fit_DEV": spf, "fits_planned": fits, "workers": args.workers, "projected_min_full": projected,
            "subsample_50pct": False, "steps": []}
    if projected > args.budget_min:
        gate["subsample_50pct"] = True
        gate["steps"].append("50% stratified concept subsample for bootstrap and permutation draws")
        projected = projected * 0.5
        if projected > args.budget_min:
            for k in [("DEV", "outcome_entries_t"), ("DEV", "mechanical_home_volume"),
                      ("DEV", "not_yet_treated_last_cohort")]:
                draws[k] = min(draws[k], 200)
            gate["steps"].append("DEV secondary variants at 200 draws")
            projected = spf * 0.5 * (sum(draws.values()) + n_perm) / args.workers / 60
        if projected > args.budget_min:
            for b in ("OLD_HELDOUT", "COHORT"):
                draws[(b, "not_yet_treated_last_cohort")] = 0
            gate["steps"].append("not-yet-treated control of OLD_HELDOUT/COHORT point-only")
            projected = spf * 0.5 * (sum(draws.values()) + n_perm) / args.workers / 60
    gate["projected_min_after_gate"] = projected
    gate["draws"] = {f"{b}|{v}": n for (b, v), n in draws.items()}
    gate["n_perm"] = n_perm
    logger.info(f"timing gate: {gate}")
    outp = RES / args.out
    out = json.loads(outp.read_text()) if outp.exists() else {}
    out["timing_gate"] = gate
    out["k_sd"] = json.loads((RES_IN / "frozen_spec.json").read_text())["estimators"]["closure_jump"]
    jdump(out, outp)
    if args.timing_only:
        return
    for body in ("DEV", "OLD_HELDOUT", "COHORT"):
        d = dev if body == "DEV" else ES.es_panel(p, cj, body)
        rb = out.get(body, {})
        rb.update({"n_eligible": int(d.ci.nunique()), "n_treated": int(d.loc[d.g.notna(), "ci"].nunique()),
                   "cohorts": {str(int(k)): int(v) for k, v in d.drop_duplicates("ci").g.value_counts().sort_index().items()}})
        variants = ["primary_never", "not_yet_treated_last_cohort"] + (
            ["outcome_entries_t", "mechanical_home_volume"] if body == "DEV" else [])
        for v in variants:
            if v in rb and rb[v].get("done"):
                logger.info(f"{body}/{v}: done (checkpoint)")
                continue
            y, ctr, control = cell_args(v)
            nb = draws[(body, v)]
            dfull = d
            try:
                r = ES.run_es(dfull, y, ctr, "g", control, 0, args.workers, "", crosscheck=(body == "DEV" and v == "primary_never"))
                if nb:
                    dsub = stratified_half(dfull) if gate["subsample_50pct"] else dfull
                    rs = ES.run_es(dsub, y, ctr, "g", control, nb, args.workers, f"{body}_{v}")
                    for k in ("n_boot_ok", "se", "ci", "lag02_se", "lag02_ci", "pretrend_wald",
                              "roth_detectable_slope_80pct"):
                        r[k] = rs[k]
                    if gate["subsample_50pct"]:   # subsample SEs are for half the concepts: rescale by sqrt(n_half/n)
                        f = np.sqrt(dsub.ci.nunique() / dfull.ci.nunique())
                        r["se_rescaled_to_full_n"] = {k: s * f for k, s in rs["se"].items()}
                        r["note_subsample"] = "bootstrap on a 50% stratified concept subsample; point estimates on full data"
                    leads = np.array([r["att"]["-3"], r["att"]["-2"]])
                    B = pd.read_parquet(DATA / f"es_boot_{body}_{v}.parquet")
                    ok = B.drop(columns=[c for c in B.columns if c == "error"]).dropna()
                    V = np.cov(ok[["e-3", "e-2"]].to_numpy().T)
                    from fe_stats import roth_power_slope, wald
                    W, pw = wald(leads, V)
                    r["pretrend_wald"] = {"W": W, "p": pw, "df": 2, "note": "full-data leads, bootstrap covariance"}
                    r["roth_detectable_slope_80pct"] = roth_power_slope(V, [-3, -2])
                    r["max_abs_lead"] = float(np.max(np.abs(leads)))
                    r["lead_small_vs_lag"] = bool(r["max_abs_lead"] < 0.5 * abs(r["mean_lag_0_2"]))
                    r["n_boot_requested"] = nb
                r["done"] = True
            except (np.linalg.LinAlgError, ValueError, KeyError) as e:
                logger.error(f"{body}/{v} failed: {e!r}")
                r = {"error": repr(e)[:300], "done": True}
            rb[v] = r
            out[body] = rb
            jdump(out, outp)
            if "att" in r:
                plot_cell(r, body, v)
                logger.info(f"{body}/{v}: lag02={r['mean_lag_0_2']:.4f} CI={r.get('lag02_ci')} "
                            f"pre={r.get('pretrend_wald', {}).get('p')} ({r['seconds']:.0f}s)")
        if body == "DEV" and not rb.get("placebo_event_date"):
            dsub = stratified_half(d) if gate["subsample_50pct"] else d
            obs = rb["primary_never"]["mean_lag_0_2"]
            pl, perm = perm_placebo(dsub, obs, n_perm, args.workers)
            if gate["subsample_50pct"]:
                pl["note"] = "permutation on the 50% stratified subsample; observed = full-data point estimate"
            rb["placebo_event_date"] = pl
            np.save(DATA / "es_placebo_perm_DEV.npy", perm)
            plot_placebo(perm, obs)
            logger.info(f"placebo: {pl}")
        out[body] = rb
        jdump(out, outp)
    pn = out["DEV"]["primary_never"]
    h = {"mean_lag_0_2": pn["mean_lag_0_2"], "ci": pn.get("lag02_ci"),
         "lag_negative_ci_below_0": bool(pn.get("lag02_ci") and pn["lag02_ci"][1] < 0),
         "pretrend_p": pn.get("pretrend_wald", {}).get("p"), "lead_small_vs_lag": pn.get("lead_small_vs_lag"),
         "roth_detectable_slope_80pct": pn.get("roth_detectable_slope_80pct"),
         "placebo_p_one_sided": out["DEV"]["placebo_event_date"]["p_one_sided_le_obs"]}
    h["holds"] = bool(h["lag_negative_ci_below_0"] and (h["pretrend_p"] or 0) > 0.10 and h["lead_small_vs_lag"]
                      and h["placebo_p_one_sided"] < 0.05)
    out["H_M4"] = h
    out["seconds"] = time.time() - t0
    jdump(out, outp)
    if gate["subsample_50pct"]:
        add_deviation("es_subsample", "event-study bootstrap/permutation on a 50% stratified concept subsample "
                      "(timing gate); point estimates on full data")
    add_deviation("es_draws", f"event-study draws per cell after the timing gate: {gate['draws']}, perm {n_perm}")
    logger.info(f"event study done: H-M4 {h} ({(time.time()-t0)/60:.1f} min)")


if __name__ == "__main__":
    main()
