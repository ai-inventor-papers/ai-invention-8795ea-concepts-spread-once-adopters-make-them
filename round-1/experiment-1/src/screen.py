"""Screen statistics: leave-one-dev-group-out (LOGO) prediction of B5 vs B5+candidate, bootstrap CIs, per-group
signs, AUC deltas, the field-level test and reliability helpers."""
from __future__ import annotations

import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler

SEED = 20260928


def _impute(Xtr: np.ndarray, Xte: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    med = np.nanmedian(Xtr, axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    return np.where(np.isfinite(Xtr), Xtr, med), np.where(np.isfinite(Xte), Xte, med)


def logo_oof(X: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str = "ridge") -> np.ndarray:
    """Out-of-fold predictions; training-fold median imputation + standardisation inside each fold."""
    oof = np.full(len(y), np.nan)
    for g in np.unique(groups):
        te = groups == g
        tr = ~te
        if tr.sum() < 3:
            continue
        Xtr, Xte = _impute(X[tr], X[te])
        sc = StandardScaler().fit(Xtr)
        Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)
        Xtr, Xte = np.nan_to_num(Xtr), np.nan_to_num(Xte)
        if kind == "ridge":
            oof[te] = Ridge(alpha=1.0).fit(Xtr, y[tr]).predict(Xte)
        else:
            if len(np.unique(y[tr])) < 2:
                oof[te] = y[tr].mean()
                continue
            oof[te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr, y[tr]).predict_proba(Xte)[:, 1]
    return oof


def rho(a: np.ndarray, b: np.ndarray) -> float:
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 4 or np.std(a[m]) == 0 or np.std(b[m]) == 0:
        return float("nan")
    return float(spearmanr(a[m], b[m])[0])


def auc(y: np.ndarray, p: np.ndarray) -> float:
    m = np.isfinite(p) & np.isfinite(y)
    if len(np.unique(y[m])) < 2:
        return float("nan")
    return float(roc_auc_score(y[m], p[m]))


def compare(XB: np.ndarray, Xc: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str = "ridge",
            n_boot: int = 2000, n_refit: int = 0, clusters: np.ndarray | None = None) -> dict:
    """B vs B+cand under LOGO. Metric: Spearman (ridge) or AUC (logistic). Bootstrap over concepts (or clusters)
    on the fixed OOF pairs, plus an optional refit bootstrap. Per-group deltas and signs."""
    XBC = np.hstack([XB, Xc])
    oB = logo_oof(XB, y, groups, kind)
    oBC = logo_oof(XBC, y, groups, kind)
    met = rho if kind == "ridge" else (lambda p, yy: auc(yy, p))
    mB, mBC = met(oB, y), met(oBC, y)
    rng = np.random.default_rng(SEED)
    units = clusters if clusters is not None else np.arange(len(y))
    uu = np.unique(units)
    rows_of = {u: np.where(units == u)[0] for u in uu}
    deltas = []
    for _ in range(n_boot):
        pick = rng.choice(uu, len(uu))
        ii = np.concatenate([rows_of[u] for u in pick])
        deltas.append(met(oBC[ii], y[ii]) - met(oB[ii], y[ii]))
    deltas = np.array(deltas)
    ci = [float(np.nanpercentile(deltas, 5)), float(np.nanpercentile(deltas, 95))] if np.isfinite(deltas).any() else [np.nan, np.nan]
    refit = None
    if n_refit:
        rd = []
        for _ in range(n_refit):
            pick = rng.choice(uu, len(uu))
            ii = np.concatenate([rows_of[u] for u in pick])
            if len(np.unique(groups[ii])) < 2:
                continue
            a = logo_oof(XB[ii], y[ii], groups[ii], kind)
            b = logo_oof(XBC[ii], y[ii], groups[ii], kind)
            rd.append(met(b, y[ii]) - met(a, y[ii]))
        rd = np.array(rd)
        refit = {"n": int(np.isfinite(rd).sum()), "ci90": [float(np.nanpercentile(rd, 5)), float(np.nanpercentile(rd, 95))],
                 "mean": float(np.nanmean(rd))} if np.isfinite(rd).any() else None
    per = {}
    for g in np.unique(groups):
        m = groups == g
        n = int(m.sum()) if clusters is None else int(len(np.unique(clusters[m])))
        d = met(oBC[m], y[m]) - met(oB[m], y[m])
        per[str(g)] = {"n": n, "metric_B": met(oB[m], y[m]), "metric_BC": met(oBC[m], y[m]), "delta": d,
                       "sign": ("insufficient" if n < 5 or not np.isfinite(d) else ("+" if d > 1e-12 else ("-" if d < -1e-12 else "0")))}
    return {"metric_B": mB, "metric_BC": mBC, "delta": mBC - mB, "ci90": ci, "refit_bootstrap": refit,
            "per_group": per, "n_pos_groups": sum(1 for v in per.values() if v["sign"] == "+"),
            "n": int(np.isfinite(y).sum()), "oof_B": oB, "oof_BC": oBC}


def spearman_brown(r: float) -> float:
    return 2 * r / (1 + r) if np.isfinite(r) and r > -1 else float("nan")
