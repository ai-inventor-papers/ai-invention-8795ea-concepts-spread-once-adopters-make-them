#!/usr/bin/env python3
"""Screen statistics under the shared protocol S0 (h)-(i) and the pre-registered selection rule.

Leave-one-home-field-group-out (LOGO) prediction: train on 3 dev groups, predict the 4th; standardised ridge
(alpha=1) for O2r, L2 logistic (C=1) for binary outcomes; B5 vs B5+candidate under identical folds.
Missing candidate values are imputed with the training-fold median plus a missing-indicator column.
Bootstrap: 2,000 resamples of CONCEPTS stratified by home group (each group keeps its n); the whole LOGO is
refitted in every resample. Field-level R_j: concept-clustered bootstrap (resample concepts, keep all rows)."""
from __future__ import annotations

import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")  # tiny models: avoid BLAS thread oversubscription across bootstrap workers

import json
import math
import multiprocessing as mp
import sys
import warnings
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from config import GROUP_SHORT, LOGS, N_BOOT, RES, SEED

warnings.filterwarnings("ignore")
B5 = ["logvol", "growth", "offhome_share", "entropy", "nfields2"]
BF = ["logn_j_early", "growth_j", "share_j"]
# D: the plan's literal primary D_z failed the T3 STOP-AND-FIX size diagnostic (70% of D_z < -5,
# Spearman(D_z, M) = -0.69, with log volume -0.63; computed before any outcome was inspected), so the pre-declared
# fallback (the one of D_ratio / D_rare with the smaller |Spearman| with M) is primary: D_ratio (0.23 vs 0.29).
# D_z is still screened and reported as 'D_z_literal'.
PRIMARY = {"D": "D_ratio", "F": "F_res", "D_z_literal": "D_z"}
SCREENED = ("D", "F")


# ----------------------------------------------------------------------------- models
def _prep(Xtr: np.ndarray, Xte: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Median-impute (train medians) + missing flags for columns with NaN, then standardise on train."""
    Xtr = Xtr.astype(float).copy()
    Xte = Xte.astype(float).copy()
    flags_tr, flags_te = [], []
    for j in range(Xtr.shape[1]):
        mtr, mte = np.isnan(Xtr[:, j]), np.isnan(Xte[:, j])
        if mtr.any() or mte.any():
            med = np.nanmedian(Xtr[:, j]) if (~mtr).any() else 0.0
            Xtr[mtr, j] = med
            Xte[mte, j] = med
            if mtr.any() and (~mtr).any():
                flags_tr.append(mtr.astype(float))
                flags_te.append(mte.astype(float))
    if flags_tr:
        Xtr = np.column_stack([Xtr] + flags_tr)
        Xte = np.column_stack([Xte] + flags_te)
    mu = Xtr.mean(0)
    sd = Xtr.std(0)
    sd[sd == 0] = 1.0
    return (Xtr - mu) / sd, (Xte - mu) / sd


def ridge_fit_predict(Xtr, ytr, Xte, alpha: float = 1.0) -> np.ndarray:
    Xtr, Xte = _prep(Xtr, Xte)
    ym = ytr.mean()
    A = Xtr.T @ Xtr + alpha * np.eye(Xtr.shape[1])
    beta = np.linalg.solve(A, Xtr.T @ (ytr - ym))
    return ym + Xte @ beta


def logit_newton(X: np.ndarray, y: np.ndarray, C: float = 1.0, iters: int = 100, tol: float = 1e-10) -> np.ndarray:
    """Exact minimiser of 0.5*||w||^2 + C*sum(logloss) with an unpenalised intercept (the sklearn
    LogisticRegression(C=1) objective), by Newton-Raphson; returns [b, w]."""
    n, p = X.shape
    Z = np.column_stack([np.ones(n), X])
    beta = np.zeros(p + 1)
    R = np.eye(p + 1) / C
    R[0, 0] = 0.0
    for _ in range(iters):
        eta = Z @ beta
        mu = 1.0 / (1.0 + np.exp(-eta))
        g = Z.T @ (mu - y) + R @ beta
        H = (Z * (mu * (1 - mu))[:, None]).T @ Z + R + 1e-12 * np.eye(p + 1)
        step = np.linalg.solve(H, g)
        beta -= step
        if np.abs(step).max() < tol:
            break
    return beta


def logit_fit_predict(Xtr, ytr, Xte) -> np.ndarray:
    if len(np.unique(ytr)) < 2:
        return np.full(len(Xte), ytr.mean())
    Xtr, Xte = _prep(Xtr, Xte)
    beta = logit_newton(Xtr, ytr.astype(float))
    return 1.0 / (1.0 + np.exp(-(beta[0] + Xte @ beta[1:])))


def logit_fit_predict_sklearn(Xtr, ytr, Xte) -> np.ndarray:
    """Reference implementation (used only in the equivalence check)."""
    Xtr, Xte = _prep(Xtr, Xte)
    m = LogisticRegression(C=1.0, max_iter=5000, tol=1e-10)
    m.fit(Xtr, ytr)
    return m.predict_proba(Xte)[:, 1]


def logo(X: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str) -> np.ndarray:
    oof = np.full(len(y), np.nan)
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if tr.sum() < 5:
            continue
        f = ridge_fit_predict if kind == "ridge" else logit_fit_predict
        oof[te] = f(X[tr], y[tr], X[te])
    return oof


def srho(a, b) -> float:
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 3 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(spearmanr(a[m], b[m]).statistic)


def auc(y, p) -> float:
    m = np.isfinite(p) & np.isfinite(y)
    if m.sum() < 3 or len(np.unique(y[m])) < 2:
        return float("nan")
    return float(roc_auc_score(y[m], p[m]))


# ----------------------------------------------------------------------------- one evaluation (point or bootstrap)
def eval_concept(df: pd.DataFrame, cands: list[str], base_cols: list[str], outcomes: dict[str, str],
                 per_group: bool = False) -> dict:
    """Returns {outcome: {'base': metric, cand: delta, ...}} (+ per-group deltas for continuous outcomes)."""
    res = {}
    g = df["group"].to_numpy()
    for oname, kind in outcomes.items():
        d = df[np.isfinite(df[oname].to_numpy(dtype=float))]
        if len(d) < 8:
            continue
        y = d[oname].to_numpy(dtype=float)
        gg = d["group"].to_numpy()
        Xb = d[base_cols].to_numpy(dtype=float)
        pb = logo(Xb, y, gg, "ridge" if kind == "cont" else "logit")
        metric = srho if kind == "cont" else auc
        mb = metric(pb, y) if kind == "cont" else metric(y, pb)
        r = {"base": mb}
        for c in cands:
            Xc = d[base_cols + [c]].to_numpy(dtype=float)
            pc_ = logo(Xc, y, gg, "ridge" if kind == "cont" else "logit")
            mc = metric(pc_, y) if kind == "cont" else metric(y, pc_)
            r[c] = mc - mb
            if per_group:
                pg = {}
                for grp in np.unique(gg):
                    m = gg == grp
                    if kind == "cont":
                        pg[grp] = srho(pc_[m], y[m]) - srho(pb[m], y[m])
                    else:
                        pg[grp] = auc(y[m], pc_[m]) - auc(y[m], pb[m])
                r[c + "__per_group"] = pg
                r[c + "__oof"] = pc_.tolist()
        if per_group:
            r["base__oof"] = pb.tolist()
            r["index"] = d["concept"].tolist()
        res[oname] = r
    del g
    return res


def eval_field(fdf: pd.DataFrame, cands: list[list[str]]) -> dict:
    y = fdf["R_j"].to_numpy(dtype=float)
    gg = fdf["group"].to_numpy()
    pb = logo(fdf[BF].to_numpy(dtype=float), y, gg, "logit")
    r = {"base": auc(y, pb)}
    for cc in cands:
        pc_ = logo(fdf[BF + cc].to_numpy(dtype=float), y, gg, "logit")
        r["+".join(cc)] = auc(y, pc_) - r["base"]
    return r


def strat_resample(df: pd.DataFrame, rng) -> pd.DataFrame:
    parts = []
    for _, d in df.groupby("group"):
        idx = rng.integers(0, len(d), len(d))
        parts.append(d.iloc[idx])
    return pd.concat(parts, ignore_index=True)


def _boot_worker(args):
    df, fdf, cands, base_cols, outcomes, field_cands, seeds = args
    out = []
    for sd in seeds:
        rng = np.random.default_rng(int(sd))
        bdf = strat_resample(df, rng)
        r = {"concept": eval_concept(bdf, cands, base_cols, outcomes)}
        if fdf is not None:
            # concept-clustered: resample concepts within group, take all their field rows
            parts = []
            for c in bdf["concept"]:
                parts.append(fdf[fdf.concept == c])
            bf = pd.concat(parts, ignore_index=True) if parts else fdf.iloc[:0]
            r["field"] = eval_field(bf, field_cands) if len(bf) > 10 else {}
        out.append(r)
    return out


def bootstrap(df, fdf, cands, base_cols, outcomes, field_cands, n_boot, seed, n_workers=4):
    seeds = np.random.default_rng(seed).integers(0, 2**31 - 1, n_boot)
    chunks = np.array_split(seeds, n_workers * 4)
    res = []
    with ProcessPoolExecutor(n_workers, mp_context=mp.get_context("spawn")) as ex:
        for part in ex.map(_boot_worker, [(df, fdf, cands, base_cols, outcomes, field_cands, ch) for ch in chunks]):
            res.extend(part)
    return res


def ci(vals, lo, hi):
    v = np.asarray([x for x in vals if x is not None and np.isfinite(x)])
    if len(v) < 20:
        return [float("nan"), float("nan")]
    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]


# ----------------------------------------------------------------------------- reliability & diagnostics
def reliability(rel: pd.DataFrame, col: str, concepts: list[str]) -> dict:
    rs = []
    rel = rel[rel.concept.isin(concepts)]
    for _, d in rel.groupby("split"):
        a, b = d[f"{col}_A"].to_numpy(float), d[f"{col}_B"].to_numpy(float)
        r = srho(a, b)
        if np.isfinite(r):
            rs.append(r)
    if not rs:
        return {"SB_median": float("nan")}
    rs = np.array(rs)
    sb = 2 * rs / (1 + rs)
    return {"r_half_median": float(np.median(rs)), "SB_median": float(np.median(sb)),
            "SB_IQR": [float(np.percentile(sb, 25)), float(np.percentile(sb, 75))], "n_splits": int(len(rs)),
            "method": "paper-level random halves of each concept's title-matched works (t0-3..t0+4), 200 null draws"}


def kendall_w(mat: np.ndarray) -> float:
    """mat: raters x items (scores); W over rankings of items, raters = groups."""
    mat = mat[:, np.all(np.isfinite(mat), axis=0)]
    m, n = mat.shape
    if n < 3 or m < 2:
        return float("nan")
    ranks = np.array([pd.Series(row).rank().to_numpy() for row in mat])
    R = ranks.sum(0)
    S = ((R - R.mean()) ** 2).sum()
    return float(12 * S / (m ** 2 * (n ** 3 - n)))


# ----------------------------------------------------------------------------- main
INDICATORS = ["D_z", "D_ratio", "D_rare", "D_sub", "D_lag", "D_withself", "D_q", "M", "F_res", "F_z", "F_bg",
              "F_obs_growth", "NOV", "NOV_res", "deg_growth", "str_growth", "new_edge_rate", "edge_persistence",
              "turnover", "participation", "n_comm_W3", "comm_transitions", "ego_density_change", "btw_t0", "btw_t4",
              "btw_change", "kcore_t4", "constraint_t4", "constraint_change"] + B5


def estimable(df: pd.DataFrame, o: str) -> bool:
    """A binary outcome is LOGO-estimable only if positives and negatives occur in >= 2 home groups each."""
    d = df[df[o].notna()]
    pos = d[d[o] == 1].group.nunique()
    neg = d[d[o] == 0].group.nunique()
    return pos >= 2 and neg >= 2


def selection(c: dict) -> dict:
    crit = {"delta_rho>=0.10": c["delta_rho"] >= 0.10,
            "CI90_low>0": c["CI90"][0] > 0,
            ">=3/4 groups positive": c["n_groups_positive"] >= 3,
            "SB>=0.6": (c["reliability"].get("SB_median", float("nan")) or 0) >= 0.6,
            "|rho_logvol|<=0.6": abs(c["rho_logvol"]) <= 0.6,
            "|rho_growth|<=0.6": abs(c["rho_growth"]) <= 0.6}
    crit = {k: bool(v) if v == v else False for k, v in crit.items()}
    return {"criteria": crit, "survives": all(crit.values())}


@logger.catch(reraise=True)
def main(n_boot: int = N_BOOT, seed: int = SEED, n_workers: int = 4, tag: str = "") -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "screen.log", rotation="30 MB", level="DEBUG")
    out = pd.read_csv(RES / "outcomes.csv")
    fe = pd.read_csv(RES / "features_ego.csv")
    dev = out[out.dropped_reason.isna() | (out.dropped_reason == "")].merge(fe, on="concept", how="left")
    dev["group"] = dev["group_id"].map(GROUP_SHORT)
    feats_cols = ["concept", "t0", "newborn", "group"] + B5 + [c for c in fe.columns if c != "concept"]
    dev[feats_cols].to_csv(RES / "features.csv", index=False)
    # field-level table
    fo = pd.read_csv(RES / "field_outcomes_base.csv")
    ff = pd.read_csv(RES / "field_features.csv")
    fdf = fo.merge(ff, on=["concept", "field"], how="left")
    fdf["group"] = fdf["group"].map({v: GROUP_SHORT[k] for k, v in __import__("config").DEV_FIELDS.items()})
    fdf = fdf.merge(dev[["concept", "D_z", "D_ratio", "F_res"]], on="concept", how="left")
    fdf.to_csv(RES / "field_outcomes.csv", index=False)
    # O2r top tercile (within the dev set with O2r)
    q = dev["O2r"].quantile(2 / 3)
    dev["O2r_top"] = np.where(dev["O2r"].notna(), (dev["O2r"] >= q).astype(float), np.nan)
    main_df = dev[dev["O2r"].notna()].reset_index(drop=True)
    for c in ("O1", "O3", "reach30"):
        dev[c] = dev[c].astype(float)
    n_main = len(main_df)
    logger.info(f"dev concepts: {len(dev)}  with O2r: {n_main}  groups: {main_df.group.value_counts().to_dict()}  "
                f"field rows: {len(fdf)}")
    outcomes = {"O2r": "cont", "O1": "bin", "O3": "bin", "O2r_top": "bin"}
    cands = list(PRIMARY.values())
    fc = [["Dj"], ["Fj", "Fj_missing"], ["D_ratio"], ["D_z"], ["F_res"]]
    point = eval_concept(main_df, cands, B5, outcomes, per_group=True)
    hurdle_pt = eval_concept(dev, cands, B5, {"reach30": "bin"})
    field_pt = eval_field(fdf, fc)
    logger.info(f"point: O2r base rho={point['O2r']['base']:.3f} dD={point['O2r']['D_ratio']:.3f} "
                f"dF={point['O2r']['F_res']:.3f}  field: {field_pt}")
    boots = bootstrap(main_df, fdf, cands, B5, outcomes, fc, n_boot, seed, n_workers)
    hb = bootstrap(dev, None, cands, B5, {"reach30": "bin"}, [], min(n_boot, 1000), seed + 1, n_workers)
    rel = pd.read_csv(RES / "reliability_splits.csv") if (RES / "reliability_splits.csv").exists() else None
    result = {"n_dev_concepts": int(len(dev)), "n_used_O2r": n_main,
              "n_per_group": main_df.group.value_counts().to_dict(),
              "O2r_top_threshold": float(q), "n_boot": n_boot, "boot_seed": seed,
              "base_metrics": {o: point[o]["base"] for o in point},
              "candidates": {}}
    for key, c in PRIMARY.items():
        pg = point["O2r"][c + "__per_group"]
        dvals = [b["concept"].get("O2r", {}).get(c) for b in boots]
        cr = {"feature": c,
              "delta_rho": point["O2r"][c], "CI90": ci(dvals, 5, 95), "CI95": ci(dvals, 2.5, 97.5),
              "per_group_delta_rho": pg, "n_groups_positive": int(sum(1 for v in pg.values() if v == v and v > 0)),
              "n_groups": len(pg),
              "rho_logvol": srho(main_df[c].to_numpy(float), main_df["logvol"].to_numpy(float)),
              "rho_growth": srho(main_df[c].to_numpy(float), main_df["growth"].to_numpy(float)),
              "n_missing": int(main_df[c].isna().sum()),
              "reliability": reliability(rel, c, main_df.concept.tolist()) if rel is not None else {}}
        for o in ("O1", "O3", "O2r_top"):
            if o in point:
                vals = [b["concept"].get(o, {}).get(c) for b in boots]
                cr[f"delta_AUC_{o}"] = point[o][c]
                cr[f"delta_AUC_{o}_CI90"] = ci(vals, 5, 95)
                cr[f"delta_AUC_{o}_per_group"] = point[o][c + "__per_group"]
        for o in ("O1", "O3", "O2r_top"):
            if not estimable(main_df, o):
                cr[f"delta_AUC_{o}"] = None
                cr[f"delta_AUC_{o}_CI90"] = [None, None]
                cr[f"delta_AUC_{o}_note"] = ("not estimable under leave-one-group-out: all positives (or all "
                                             "negatives) lie in one home group")
        cr["delta_AUC_reach30"] = hurdle_pt.get("reach30", {}).get(c)
        if not estimable(dev, "reach30"):
            cr["delta_AUC_reach30_note"] = "not estimable: every dev concept reaches N>=30 labelled papers in t0+6..t0+8"
        cr["delta_AUC_reach30_CI90"] = ci([b["concept"].get("reach30", {}).get(c) for b in hb], 5, 95)
        # dissociation: Delta_AUC(O2r_top) - Delta_AUC(O1), paired
        diff_pt = point["O2r_top"][c] - point["O1"][c]
        dv = [b["concept"].get("O2r_top", {}).get(c, np.nan) - b["concept"].get("O1", {}).get(c, np.nan)
              for b in boots]
        dci = ci(dv, 5, 95)
        if key.startswith("D"):
            verdict = "supported" if dci[0] > 0 else ("contradicted" if dci[1] < 0 else "inconclusive")
            pred = "D's gain concentrates on breadth: CI90 of [dAUC(O2r_top) - dAUC(O1)] > 0"
        else:
            eq = dci[0] >= -0.05 and dci[1] <= 0.05
            pos = point["O1"][c] > 0 and point["O2r_top"][c] > 0
            verdict = "supported" if (eq and pos) else ("contradicted" if (dci[0] > 0.05 or dci[1] < -0.05) else
                                                         "inconclusive")
            pred = "F's gain equal for uptake and breadth: CI90 within [-0.05,0.05] and both dAUC > 0"
        cr["dissociation"] = {"diff_point": diff_pt, "CI90": dci, "prediction": pred, "verdict": verdict}
        fk = "Dj" if key.startswith("D") else "Fj+Fj_missing"
        cr["field_level"] = {"base_AUC": field_pt["base"], "delta_AUC": field_pt[fk],
                             "CI90": ci([b.get("field", {}).get(fk) for b in boots], 5, 95),
                             "concept_level_variant_delta_AUC": field_pt[c],
                             "concept_level_variant_CI90": ci([b.get("field", {}).get(c) for b in boots], 5, 95),
                             "n_rows": int(len(fdf)), "base_rate": float(fdf.R_j.mean())}
        cr.update(selection(cr))
        cr["role"] = {"D": "primary D (pre-declared T3 fallback for D_z)", "F": "primary F",
                      "D_z_literal": "plan's literal primary D; superseded (fails size diagnostic); not ranked"}[key]
        result["candidates"][key] = cr
        logger.info(f"{key}: drho={cr['delta_rho']:.3f} CI90={cr['CI90']} groups+={cr['n_groups_positive']} "
                    f"SB={cr['reliability'].get('SB_median')} survives={cr['survives']}")
    # ranking
    ranked = sorted(SCREENED, key=lambda k: -result["candidates"][k]["delta_rho"])
    surv = [k for k in ranked if result["candidates"][k]["survives"]]
    result["ranking_by_delta_rho"] = ranked
    result["survivors"] = surv
    result["carried_forward"] = (surv[:1] + [k for k in surv[1:2] if result["candidates"][surv[0]]["delta_rho"] -
                                             result["candidates"][k]["delta_rho"] <= 0.05]) if surv else ranked[:1]
    result["screen_label"] = "screen" if n_main >= 32 else "underpowered screen"
    # ---- portability of every indicator
    port = {}
    groups = sorted(main_df.group.unique())
    rho_mat = []
    for ind in INDICATORS:
        if ind not in main_df.columns:
            continue
        x = main_df[ind].to_numpy(float)
        e = {"pooled_rho_O2r": srho(x, main_df.O2r.to_numpy(float)),
             "pooled_rho_O1": srho(x, main_df.O1.to_numpy(float)),
             "rho_logvol": srho(x, main_df.logvol.to_numpy(float)),
             "within_group_rho_O2r": {}, "within_group_rho_O1": {}, "n_missing": int(np.isnan(x).sum())}
        for grp in groups:
            m = (main_df.group == grp).to_numpy()
            e["within_group_rho_O2r"][grp] = srho(x[m], main_df.O2r.to_numpy(float)[m])
            e["within_group_rho_O1"][grp] = srho(x[m], main_df.O1.to_numpy(float)[m])
        yy = main_df.O2r.to_numpy(float)
        e["logo_single_rho_O2r"] = srho(logo(main_df[[ind]].to_numpy(float), yy, main_df.group.to_numpy(), "ridge"), yy)
        e["rho_entropy"] = srho(x, main_df.entropy.to_numpy(float))
        e["rho_offhome_share"] = srho(x, main_df.offhome_share.to_numpy(float))
        e["rho_growth"] = srho(x, main_df.growth.to_numpy(float))
        if ind not in B5:
            pr = eval_concept(main_df, [ind], B5, {"O2r": "cont"}, per_group=True)["O2r"]
            e["logo_delta_rho_O2r"] = pr[ind]
            e["logo_delta_rho_per_group"] = pr[ind + "__per_group"]
        wg = e["within_group_rho_O2r"]
        others = [wg[g] for g in groups if g != "CS"]
        e["negative_result_CS_only"] = bool(wg.get("CS", np.nan) > 0.3 and sum(1 for v in others if v <= 0) >= 2)
        e["n_groups_same_sign_as_pooled"] = int(sum(1 for v in wg.values()
                                                    if v == v and np.sign(v) == np.sign(e["pooled_rho_O2r"])))
        port[ind] = e
        rho_mat.append([wg[g] for g in groups])
    rm = np.array(rho_mat).T  # groups x indicators
    result["portability"] = {"groups": groups, "indicators": port, "kendall_W_indicator_ranks_O2r": kendall_w(rm)}
    # ---- sensitivities (point estimates + 1,000-draw CIs for the two primaries)
    sens = {}

    def run_s(name, df_, cands_, base_=B5, outcome="O2r"):
        pt = eval_concept(df_, cands_, base_, {outcome: "cont"}, per_group=True)[outcome]
        bs = bootstrap(df_, None, cands_, base_, {outcome: "cont"}, [], min(1000, n_boot), seed + 7, n_workers)
        sens[name] = {c: {"delta_rho": pt[c], "CI90": ci([b["concept"].get(outcome, {}).get(c) for b in bs], 5, 95),
                          "per_group": pt[c + "__per_group"], "n": int(len(df_))} for c in cands_}
    nb = main_df[main_df.newborn.astype(str).str.lower() == "true"]
    if len(nb) >= 16 and nb.group.nunique() >= 3:
        run_s("newborn_only", nb, cands)
    m50 = dev[dev.O2r_m50.notna()].reset_index(drop=True)
    if len(m50) >= 16:
        run_s("O2r_m50", m50, cands, outcome="O2r_m50")
    run_s("baseline_plus_label_coverage", main_df, cands, B5 + ["cov_early"])
    run_s("baseline_plus_has_self_topic", main_df, cands, B5 + ["has_self_topic"])
    run_s("secondary_D_and_F_variants", main_df, ["D_lag", "D_sub", "D_withself", "D_q", "D_rare",
                                                  "F_bg", "F_z", "NOV_res"])
    result["sensitivities"] = sens
    # ---- sanity (T5)
    result["outcome_estimability"] = {o: estimable(dev if o == "reach30" else main_df, o)
                                      for o in ("O1", "O3", "O2r_top", "reach30")}
    result["O3_positives_by_group"] = dev[dev.O3 == 1].group.value_counts().to_dict()
    result["sanity"] = {"rho_O2r_entropy": srho(main_df.entropy.to_numpy(float), main_df.O2r.to_numpy(float)),
                        "O1_base_rate": float(dev.O1.mean()), "O3_base_rate": float(dev.O3.mean()),
                        "reach30_rate": float(dev.reach30.mean()),
                        "rho_Dz_M": srho(main_df.D_z.to_numpy(float), main_df.M.to_numpy(float)),
                        "rho_Dratio_M": srho(main_df.D_ratio.to_numpy(float), main_df.M.to_numpy(float)),
                        "rho_Drare_M": srho(main_df.D_rare.to_numpy(float), main_df.M.to_numpy(float)),
                        "share_M_below_3": float((main_df.M < 3).mean()),
                        "share_kused_W1_below_5": float((main_df.k_used_W1 < 5).mean()),
                        "share_Dz_below_-5": float((main_df.D_z < -5).mean()),
                        "rho_title_vs_api_early_volume": srho(np.log1p(main_df.n_title_early.to_numpy(float)),
                                                              main_df.logvol.to_numpy(float)),
                        "median_title_share_of_api_early": float(np.nanmedian(main_df.n_title_early /
                                                                              main_df.n_api_early))}
    # OOF predictions for method_out.json
    result["_oof"] = {"index": point["O2r"]["index"], "base": point["O2r"]["base__oof"],
                      "D_ratio": point["O2r"]["D_ratio__oof"], "D_z": point["O2r"]["D_z__oof"],
                      "F_res": point["O2r"]["F_res__oof"]}
    result["_oof_O1"] = {"index": point["O1"]["index"], "base": point["O1"]["base__oof"],
                         "D_ratio": point["O1"]["D_ratio__oof"], "F_res": point["O1"]["F_res__oof"]}
    (RES / f"screen_result{tag}.json").write_text(json.dumps(result, indent=1, default=lambda o: None
                                                             if isinstance(o, float) and not math.isfinite(o) else o))
    logger.info(f"screen written ({tag or 'main'}); survivors={surv}")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_boot", type=int, default=N_BOOT)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    main(a.n_boot, a.seed, a.workers, a.tag)
