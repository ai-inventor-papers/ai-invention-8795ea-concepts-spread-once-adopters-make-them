#!/usr/bin/env python3
"""WP2-T3: concept-clustered REFIT bootstrap CIs for the iteration-1 concept-level deltas.

Each row re-implements the source experiment's own LOGO pipeline (exp1 screen.compare, exp3 screen.eval_concept,
exp4 screen.paired_delta), first reproduces the reported point estimate (gate: |diff| <= 0.002), then resamples
concepts WITHIN home group and refits the whole LOGO pipeline on each resample (B = 2000, seed 20260928)."""
from __future__ import annotations

import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import math
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import common as C


# ------------------------------------------------------------------ exp1 pipeline (screen.compare)
def _x1_impute(Xtr, Xte):
    med = np.nanmedian(Xtr, axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    return np.where(np.isfinite(Xtr), Xtr, med), np.where(np.isfinite(Xte), Xte, med)


def x1_logo(X, y, groups, kind="ridge"):
    oof = np.full(len(y), np.nan)
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if tr.sum() < 3:
            continue
        Xtr, Xte = _x1_impute(X[tr], X[te])
        sc = StandardScaler().fit(Xtr)
        Xtr, Xte = np.nan_to_num(sc.transform(Xtr)), np.nan_to_num(sc.transform(Xte))
        if kind == "ridge":
            oof[te] = Ridge(alpha=1.0).fit(Xtr, y[tr]).predict(Xte)
        else:
            if len(np.unique(y[tr])) < 2:
                oof[te] = y[tr].mean()
                continue
            oof[te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr, y[tr]).predict_proba(Xte)[:, 1]
    return oof


def _rho(a, b):
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 4 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return math.nan
    return float(spearmanr(a[m], b[m]).statistic)


def _auc(y, p):
    m = np.isfinite(p) & np.isfinite(y)
    if m.sum() < 4 or len(np.unique(y[m])) < 2:
        return math.nan
    return float(roc_auc_score(y[m].astype(int), p[m]))


# ------------------------------------------------------------------ exp3 pipeline (screen.eval_concept)
def _x3_prep(Xtr, Xte):
    Xtr = Xtr.astype(float).copy()
    Xte = Xte.astype(float).copy()
    ftr, fte = [], []
    for j in range(Xtr.shape[1]):
        mtr, mte = np.isnan(Xtr[:, j]), np.isnan(Xte[:, j])
        if mtr.any() or mte.any():
            med = np.nanmedian(Xtr[:, j]) if (~mtr).any() else 0.0
            Xtr[mtr, j] = med
            Xte[mte, j] = med
            if mtr.any() and (~mtr).any():
                ftr.append(mtr.astype(float))
                fte.append(mte.astype(float))
    if ftr:
        Xtr = np.column_stack([Xtr] + ftr)
        Xte = np.column_stack([Xte] + fte)
    mu = Xtr.mean(0)
    sd = Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd


def x3_logo(X, y, groups):
    oof = np.full(len(y), np.nan)
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if tr.sum() < 5:
            continue
        Xtr, Xte = _x3_prep(X[tr], X[te])
        ym = y[tr].mean()
        beta = np.linalg.solve(Xtr.T @ Xtr + np.eye(Xtr.shape[1]), Xtr.T @ (y[tr] - ym))
        oof[te] = ym + Xte @ beta
    return oof


# ------------------------------------------------------------------ exp4 pipeline (screen.paired_delta)
def x4_logo(df: pd.DataFrame, cols: list[str], y: str, kind: str) -> np.ndarray:
    oof = np.full(len(df), np.nan)
    g = df["group"].to_numpy()
    for lg in ["CS", "Eng", "BGM", "Med"]:
        te = g == lg
        tr = ~te
        if te.sum() == 0 or tr.sum() < 5:
            continue
        X = df[cols].copy()
        for c in X.columns:
            med = X.loc[tr, c].median()
            X[c] = X[c].fillna(med if np.isfinite(med) else 0.0)
        X = X.to_numpy(float)
        yt = df.loc[tr, y].to_numpy(float)
        if kind == "ridge":
            oof[te] = make_pipeline(StandardScaler(), Ridge(alpha=1.0)).fit(X[tr], yt).predict(X[te])
        else:
            if len(np.unique(yt)) < 2:
                oof[te] = yt.mean()
                continue
            m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000)).fit(X[tr], yt.astype(int))
            oof[te] = m.predict_proba(X[te])[:, 1]
    return oof


# ------------------------------------------------------------------ row definitions
def load_rows() -> list[dict]:
    rows = []
    # exp1 A*_h on O2r (primary)
    out = C.read_csv(C.X1 / "results/outcomes.csv")
    feat = C.read_csv(C.X1 / "results/features.csv")
    D = out.merge(feat, on=["concept", "dev_group"], how="left")
    D = D[np.isfinite(D["O2r"])].reset_index(drop=True)
    B5 = ["B_logvol", "B_growth", "B_offhome", "B_entropy", "B_nfields"]
    rows.append({"row": "exp1_Astar_h_delta_rho_O2r", "exp": "exp1", "df": D, "group": "dev_group",
                 "base": B5 + ["A_h_missing"], "cand": B5 + ["A_h_missing", "A_h"], "y": "O2r", "kind": "ridge",
                 "point_reported": -0.005644811115935844,
                 "reported_src": ("round-1/experiment-1/src/results/screen_result.json", "delta_rho"),
                 "fixed_ci90_src": ("round-1/experiment-1/src/results/screen_result.json", "ci90"),
                 "old_refit_src": ("round-1/experiment-1/src/results/screen_result.json", "refit_bootstrap.ci90")})
    # exp3 D_ratio and F_res on O2r
    f3 = C.read_csv(C.X3 / "results/features.csv")
    o3 = C.read_csv(C.X3 / "results/outcomes.csv")
    d3 = f3.merge(o3[["concept", "O2r"]], on="concept", how="left")
    d3 = d3[d3["O2r"].notna()].reset_index(drop=True)
    B5_3 = ["logvol", "growth", "offhome_share", "entropy", "nfields2"]
    for key, feat_ in (("D", "D_ratio"), ("F", "F_res")):
        rows.append({"row": f"exp3_{feat_}_delta_rho_O2r", "exp": "exp3", "df": d3, "group": "group", "base": B5_3,
                     "cand": B5_3 + [feat_], "y": "O2r", "kind": "x3ridge",
                     "reported_src": ("round-1/experiment-3/src/results/screen_result.json", f"candidates.{key}.delta_rho"),
                     "fixed_ci90_src": None,
                     "old_refit_src": ("round-1/experiment-3/src/results/screen_result.json", f"candidates.{key}.CI95")})
    # exp4 G rows
    f4 = C.read_csv(C.X4 / "features.csv")
    B5_4 = ["log_count_W5", "growth_W5_B5", "offhome_share_W3", "entropy_W3", "reach_W3"]
    CAND = B5_4 + ["G", "G_missing"]
    d2 = f4.dropna(subset=["O2r_m30"]).reset_index(drop=True)
    src4 = "round-1/experiment-4/src/screen_result.json"
    rows.append({"row": "exp4_G_delta_rho_O2r_m30", "exp": "exp4", "df": d2, "group": "group", "base": B5_4, "cand": CAND,
                 "y": "O2r_m30", "kind": "ridge", "reported_src": (src4, "delta_rho_O2r_m30.delta"),
                 "fixed_ci90_src": (src4, "delta_rho_O2r_m30.ci90"), "fixed_ci95_src": (src4, "delta_rho_O2r_m30.ci95"),
                 "old_refit_src": (src4, "delta_rho_O2r_m30.refit_boot.ci90")})
    rows.append({"row": "exp4_G_delta_rho_O2r_resid", "exp": "exp4", "df": d2, "group": "group", "base": B5_4, "cand": CAND,
                 "y": "O2r_resid", "kind": "ridge", "reported_src": (src4, "delta_rho_O2r_resid.delta"),
                 "fixed_ci90_src": (src4, "delta_rho_O2r_resid.ci90"), "old_refit_src": None})
    rows.append({"row": "exp4_G_delta_auc_O1", "exp": "exp4", "df": f4.reset_index(drop=True), "group": "group",
                 "base": B5_4, "cand": CAND, "y": "O1", "kind": "logit", "reported_src": (src4, "delta_auc_O1.delta"),
                 "fixed_ci90_src": (src4, "delta_auc_O1.ci90"), "fixed_ci95_src": (src4, "delta_auc_O1.ci95"),
                 "old_refit_src": None})
    rows.append({"row": "exp4_G_delta_auc_O1_label_coverage_adjusted", "exp": "exp4", "df": f4.reset_index(drop=True),
                 "group": "group", "base": B5_4 + ["label_coverage_early"],
                 "cand": B5_4 + ["label_coverage_early", "G", "G_missing"], "y": "O1", "kind": "logit",
                 "reported_src": ("round-2/evaluation-1/src/eval_out.json", "metadata.D_O1_artefact.G.B5+cov.delta"),
                 "fixed_ci90_src": None,
                 "old_refit_src": ("round-2/evaluation-1/src/eval_out.json", "metadata.D_O1_artefact.G.B5+cov.ci95")})
    return rows


def stat_row(r: dict, df: pd.DataFrame) -> float:
    g = df[r["group"]].to_numpy()
    y = df[r["y"]].to_numpy(float)
    ok = np.isfinite(y)
    if r["kind"] == "ridge" and r["exp"] == "exp1":
        a = x1_logo(df[r["base"]].to_numpy(float), y, g, "ridge")
        b = x1_logo(df[r["cand"]].to_numpy(float), y, g, "ridge")
        return _rho(b, y) - _rho(a, y)
    if r["kind"] == "x3ridge":
        a = x3_logo(df[r["base"]].to_numpy(float), y, g)
        b = x3_logo(df[r["cand"]].to_numpy(float), y, g)
        return _rho(b, y) - _rho(a, y)
    d = df[ok].reset_index(drop=True)
    a = x4_logo(d, r["base"], r["y"], r["kind"])
    b = x4_logo(d, r["cand"], r["y"], r["kind"])
    yy = d[r["y"]].to_numpy(float)
    if r["kind"] == "ridge":
        return _rho(b, yy) - _rho(a, yy)
    return _auc(yy, b) - _auc(yy, a)


def _worker(args):
    r, seeds = args
    df = r["df"]
    gidx = [np.where(df[r["group"]].to_numpy() == g)[0] for g in pd.unique(df[r["group"]])]
    out = []
    for sd in seeds:
        rng = np.random.default_rng(int(sd))
        idx = np.concatenate([rng.choice(ix, len(ix)) for ix in gidx if len(ix)])
        try:
            out.append(stat_row(r, df.iloc[idx].reset_index(drop=True)))
        except (ValueError, np.linalg.LinAlgError):
            out.append(math.nan)
    return out


def src_val(src):
    if not src:
        return None
    path, key = src
    try:
        return C.get_path(C.read_json(C.ROOT / path), key)
    except (KeyError, FileNotFoundError, IndexError):
        return None


def main(B: int, workers: int) -> None:
    C.setup_logging("wp2_t3")
    rows = load_rows()
    master = np.random.default_rng(C.SEED)
    results = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        for r in rows:
            t = time.time()
            rep = src_val(r["reported_src"])
            if rep is None:
                rep = r.get("point_reported")
            pt = stat_row(r, r["df"])
            reproduces = rep is not None and abs(pt - rep) <= 0.002
            seeds = master.integers(0, 2**31 - 1, B)
            chunks = np.array_split(seeds, workers * 2)
            boots = []
            for part in ex.map(_worker, [(r, ch) for ch in chunks]):
                boots.extend(part)
            boots = np.asarray(boots, float)
            fin = boots[np.isfinite(boots)]
            ci95 = C.pct_ci(fin)
            ci90 = C.pct_ci(fin, 5, 95)
            fixed90 = src_val(r.get("fixed_ci90_src"))
            fixed95 = src_val(r.get("fixed_ci95_src"))
            old_refit = src_val(r.get("old_refit_src"))
            wid_fixed = (fixed90[1] - fixed90[0]) if isinstance(fixed90, list) else math.nan
            ratio = (ci90[1] - ci90[0]) / wid_fixed if np.isfinite(wid_fixed) and wid_fixed > 0 else math.nan
            res = {"row": r["row"], "experiment": r["exp"], "outcome": r["y"], "base_cols": "|".join(r["base"]),
                   "cand_cols": "|".join(r["cand"]), "point_reported": rep, "point_reproduced": pt,
                   "abs_diff": abs(pt - rep) if rep is not None else math.nan,
                   "reproduction_status": "MATCH" if reproduces else "MISMATCH",
                   "ci90_refit": ci90, "ci95_refit": ci95, "B": int(len(fin)), "B_requested": B,
                   "n_concepts": int(r["df"][r["y"]].notna().sum()), "fixed_prediction_ci90": fixed90,
                   "fixed_prediction_ci95": fixed95, "earlier_refit_or_source_ci": old_refit,
                   "ci_widening_ratio_90": ratio, "ci95_excludes_0": bool(ci95[0] > 0 or ci95[1] < 0),
                   "source_file": r["reported_src"][0], "key_path": r["reported_src"][1],
                   "runtime_s": round(time.time() - t, 1)}
            logger.info(f"{r['row']}: rep={rep} pt={pt:.4f} ci95={np.round(ci95, 3)} ratio={ratio:.2f} ({res['runtime_s']}s)")
            results.append(res)
    C.dump(results, C.RES / "t3_refit_bootstrap.json")
    C.save_manifest("wp2_t3")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=C.B_MAIN)
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()
    main(a.B, a.workers)
