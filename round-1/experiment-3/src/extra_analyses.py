#!/usr/bin/env python3
"""EXPLORATORY (not pre-registered; never used for selection).

Why the screen's Delta-rho can miss a real incremental signal: with B5 already at Spearman ~0.77 against O2r,
the Spearman of fitted values is near its ceiling. This script reports an out-of-group PARTIAL association:
in each leave-one-group-out fold, O2r and the candidate are both residualised on B5 with coefficients fitted on
the training groups only; the pooled Spearman of the held-out residual pairs is the statistic, with the same
2,000-draw group-stratified concept bootstrap. Also the in-sample partial Spearman given B5 and a
rank-feature / alpha=10 robustness check of Delta-rho. Writes results/exploratory_partial_association.json."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
from concurrent.futures import ProcessPoolExecutor

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402
from scipy.stats import rankdata, spearmanr  # noqa: E402

from config import LOGS, RES, SEED  # noqa: E402
from screen import B5, _prep, ci, logo, ridge_fit_predict, strat_resample  # noqa: E402

CANDS = ["D_ratio", "D_rare", "D_z", "D_sub", "NOV_res", "participation", "n_comm_W3", "F_res", "F_z", "F_bg",
         "deg_growth", "btw_change"]


def _ols_resid(Xtr, ytr, Xte, yte):
    Xtr, Xte = _prep(Xtr, Xte)
    Z = np.column_stack([np.ones(len(Xtr)), Xtr])
    b = np.linalg.lstsq(Z, ytr, rcond=None)[0]
    return yte - np.column_stack([np.ones(len(Xte)), Xte]) @ b


def logo_partial(df: pd.DataFrame, cand: str) -> tuple[float, dict]:
    d = df[df[cand].notna()]
    g = d.group.to_numpy()
    XB = d[B5].to_numpy(float)
    y = d.O2r.to_numpy(float)
    x = d[cand].to_numpy(float)
    ry, rx, gg = [], [], []
    for grp in np.unique(g):
        te = g == grp
        if (~te).sum() < 8 or te.sum() < 3:
            continue
        ry.append(_ols_resid(XB[~te], y[~te], XB[te], y[te]))
        rx.append(_ols_resid(XB[~te], x[~te], XB[te], x[te]))
        gg += [grp] * te.sum()
    ry, rx, gg = np.concatenate(ry), np.concatenate(rx), np.array(gg)
    pooled = float(spearmanr(rx, ry).statistic)
    per = {grp: float(spearmanr(rx[gg == grp], ry[gg == grp]).statistic) for grp in np.unique(gg)}
    return pooled, per


def _worker(args):
    df, seeds = args
    out = []
    for sd in seeds:
        b = strat_resample(df, np.random.default_rng(int(sd)))
        out.append({c: logo_partial(b, c)[0] for c in CANDS})
    return out


def in_sample_partial(df: pd.DataFrame, cand: str) -> float:
    d = df[df[cand].notna()]
    Z = np.column_stack([np.ones(len(d))] + [rankdata(d[c]) for c in B5])

    def res(v):
        return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]
    return float(spearmanr(res(rankdata(d[cand])), res(rankdata(d.O2r))).statistic)


def delta_rho_robustness(df: pd.DataFrame, cand: str) -> dict:
    """Delta-rho of B5+cand vs B5: in-sample, LOGO on rank-transformed features, LOGO with ridge alpha=10."""
    d = df[df[cand].notna()]
    y = d.O2r.to_numpy(float)
    g = d.group.to_numpy()
    X = d[B5 + [cand]].to_numpy(float)

    def sp(p):
        return float(spearmanr(p, y).statistic)

    def logo_a(Xm, alpha):
        oof = np.full(len(y), np.nan)
        for grp in np.unique(g):
            te = g == grp
            oof[te] = ridge_fit_predict(Xm[~te], y[~te], Xm[te], alpha=alpha)
        return oof
    R = d[B5 + [cand]].rank().to_numpy(float)
    return {"in_sample_delta_rho": sp(ridge_fit_predict(X, y, X)) - sp(ridge_fit_predict(X[:, :5], y, X[:, :5])),
            "logo_delta_rho_rank_features": sp(logo(R, y, g, "ridge")) - sp(logo(R[:, :5], y, g, "ridge")),
            "logo_delta_rho_alpha10": sp(logo_a(X, 10)) - sp(logo_a(X[:, :5], 10))}


@logger.catch(reraise=True)
def main(n_boot: int = 2000, workers: int = 4) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "extra_analyses.log", rotation="30 MB", level="DEBUG")
    f = pd.read_csv(RES / "features.csv")
    o = pd.read_csv(RES / "outcomes.csv")[["concept", "O2r"]]
    df = f.merge(o, on="concept")
    df = df[df.O2r.notna()].reset_index(drop=True)
    seeds = np.random.default_rng(SEED + 11).integers(0, 2**31 - 1, n_boot)
    boots = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        for part in ex.map(_worker, [(df, ch) for ch in np.array_split(seeds, workers * 4)]):
            boots += part
    res = {"label": "EXPLORATORY, not pre-registered; not used for selection",
           "statistic": "LOGO out-of-group partial Spearman (candidate and O2r residualised on B5, train-fold OLS)",
           "n": int(len(df)), "n_boot": n_boot, "candidates": {}}
    for c in CANDS:
        pooled, per = logo_partial(df, c)
        res["candidates"][c] = {"logo_partial_rho": pooled, "CI90": ci([b[c] for b in boots], 5, 95),
                                "CI95": ci([b[c] for b in boots], 2.5, 97.5), "per_group": per,
                                "n_groups_positive": int(sum(v > 0 for v in per.values())),
                                "in_sample_partial_rho_given_B5": in_sample_partial(df, c),
                                "delta_rho_robustness": delta_rho_robustness(df, c)}
        logger.info(f"{c:14s} LOGO partial rho={pooled:+.3f} CI90={res['candidates'][c]['CI90']} per-group={per}")
    (RES / "exploratory_partial_association.json").write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
