"""Core statistics for the gateway stress test. Worker-safe (imported by spawn workers): no logging side effects.

The LOGO logistic model, training-fold median imputation and AUC come from iteration-1 exp4's screen.py, imported
read-only (never rewritten). The only extension is fold-dependent columns (field propensity P, O1_base) that must be
recomputed inside each training fold to stay leakage-free.
"""
from __future__ import annotations

import math
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# Parent folder holding the three iteration-1 dependency artifacts as sub-folders gen_art_experiment_1
# (art_xp8BGBJZsxeI), gen_art_experiment_3 (art_yrradSC27HtQ) and gen_art_experiment_4 (art_33_KKk_G8Gw5).
ITER1 = Path(os.environ.get("AII_ITER1", Path(__file__).resolve().parent.parent.parent.parent / "round-1" / "."))
EXP4 = ITER1 / "experiment-4/src"
if str(EXP4) not in sys.path:
    sys.path.insert(0, str(EXP4))
import screen as S4  # noqa: E402  exp4's own screen.py (logo_predict, _prep, _auc, dersimonian_laird)

GROUPS = S4.GROUPS  # ["CS", "Eng", "BGM", "Med"]
_ORIG_PREP, _ORIG_AUC = S4._prep, S4._auc


def fast_prep(X: pd.DataFrame, train: np.ndarray) -> np.ndarray:
    """Numerically identical numpy version of screen._prep (training-fold median imputation per column)."""
    A = X.to_numpy(dtype=float, copy=True)
    if np.isnan(A).any():
        with np.errstate(all="ignore"):
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                med = np.nanmedian(A[train], axis=0)
        med = np.where(np.isfinite(med), med, 0.0)
        r, c = np.nonzero(np.isnan(A))
        A[r, c] = med[c]
    return A


def fast_auc(y, p) -> float:
    """Rank (Mann-Whitney) AUC with screen._auc's conventions (finite rows, >= 4 rows, both classes)."""
    from scipy.stats import rankdata
    y = np.asarray(y, float)
    p = np.asarray(p, float)
    ok = np.isfinite(p) & np.isfinite(y)
    if ok.sum() < 4:
        return math.nan
    y, p = y[ok], p[ok]
    n1 = y.sum()
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return math.nan
    r = rankdata(p)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


# Speed: exp4's logo_predict looks up _prep at call time; the numpy version gives identical matrices (verified in
# eval.py against the original on every dataset before use).
S4._prep = fast_prep


# ----------------------------------------------------------------------------- fold-dependent features
def propensity(key: np.ndarray, cl: np.ndarray, y: np.ndarray, grp: np.ndarray, test_g: str, a: float,
               pool: pd.DataFrame | None = None, concept: np.ndarray | None = None) -> np.ndarray:
    """Shrunken leave-concept-out field retention propensity for one LOGO fold.

    Within-dataset (pool None): statistics from training-fold rows (group != test_g) of the same field key;
    test rows use all training rows of the key, training rows exclude rows of their own cluster (concept copy).
    Pooled: statistics from the external pool (rows of all three files) with group != test_g and concept != own
    concept, for both test and training rows. P = (sum R + a*pbar) / (n + a); pbar = training mean; n=0,a=0 -> pbar.
    """
    n = len(y)
    out = np.empty(n)
    if pool is None:
        tr = grp != test_g
        pbar = float(y[tr].mean())
        d = pd.DataFrame({"k": key[tr], "c": cl[tr], "y": y[tr]})
        tot = d.groupby("k")["y"].agg(["sum", "count"])
        byc = d.groupby(["k", "c"])["y"].agg(["sum", "count"])
        ks = tot.reindex(key)
        s_all = np.nan_to_num(ks["sum"].to_numpy(float))
        n_all = np.nan_to_num(ks["count"].to_numpy(float))
        own = byc.reindex(pd.MultiIndex.from_arrays([key, cl]))
        s_own = np.nan_to_num(own["sum"].to_numpy(float))
        n_own = np.nan_to_num(own["count"].to_numpy(float))
        s = np.where(tr, s_all - s_own, s_all)
        c = np.where(tr, n_all - n_own, n_all)
    else:
        pp = pool[pool["group"].to_numpy() != test_g]
        pbar = float(pp["R"].mean())
        tot = pp.groupby("key")["R"].agg(["sum", "count"])
        byc = pp.groupby(["key", "concept"])["R"].agg(["sum", "count"])
        ks = tot.reindex(key)
        own = byc.reindex(pd.MultiIndex.from_arrays([key, concept]))
        s = np.nan_to_num(ks["sum"].to_numpy(float)) - np.nan_to_num(own["sum"].to_numpy(float))
        c = np.nan_to_num(ks["count"].to_numpy(float)) - np.nan_to_num(own["count"].to_numpy(float))
    den = c + a
    out[:] = np.where(den > 0, (s + a * pbar) / np.where(den > 0, den, 1.0), pbar)
    return out


def logo_ext(df: pd.DataFrame, cols: list[str], y: str = "R", a: float = 2.0, pool: pd.DataFrame | None = None,
             cl_col: str = "cl") -> np.ndarray:
    """exp4 screen.logo_predict(kind='logit') plus fold-computed P columns ('P_within', 'P_pooled')."""
    dyn = [c for c in cols if c in ("P_within", "P_pooled")]
    if not dyn:
        return S4.logo_predict(df, cols, y, "logit")
    oof = np.full(len(df), np.nan)
    g = df["group"].to_numpy()
    Y = df[y].to_numpy(float)
    key = df["key"].to_numpy()
    cl = df[cl_col].to_numpy()
    con = df["concept"].to_numpy()
    for lg in GROUPS:
        te = g == lg
        tr = ~te
        if te.sum() == 0 or tr.sum() < 5:
            continue
        X = df[[c for c in cols if c not in dyn]].copy()
        if "P_within" in dyn:
            X["P_within"] = propensity(key, cl, Y, g, lg, a)
        if "P_pooled" in dyn:
            X["P_pooled"] = propensity(key, cl, Y, g, lg, a, pool=pool, concept=con)
        X = X[cols]
        Xall = S4._prep(X, tr)
        yt = Y[tr]
        if len(np.unique(yt)) < 2:
            oof[te] = yt.mean()
            continue
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000))
        m.fit(Xall[tr], yt.astype(int))
        oof[te] = m.predict_proba(Xall[te])[:, 1]
    return oof


def pooled_auc(y: np.ndarray, p: np.ndarray, g: np.ndarray) -> tuple[float, int]:
    """Pooled OOF AUC after dropping rows of test groups that contain a single class. Returns (auc, n_dropped_groups)."""
    keep = np.ones(len(y), bool)
    nd = 0
    for lg in GROUPS:
        m = g == lg
        if m.sum() and len(np.unique(y[m])) < 2:
            keep &= ~m
            nd += 1
    return fast_auc(y[keep], p[keep]), nd


def group_aucs(y: np.ndarray, p: np.ndarray, g: np.ndarray) -> dict:
    return {lg: fast_auc(y[g == lg], p[g == lg]) for lg in GROUPS}


def eval_specs(df: pd.DataFrame, specs: list[tuple[str, list[str], list[str]]], a: float = 2.0,
               pool: pd.DataFrame | None = None, keep_oof: bool = False) -> dict:
    """Fit every distinct model once; return pooled/per-group delta-AUC per spec."""
    cache: dict[tuple, np.ndarray] = {}
    Y = df["R"].to_numpy(float)
    g = df["group"].to_numpy()

    def get(cols):
        k = tuple(cols)
        if k not in cache:
            cache[k] = logo_ext(df, list(cols), "R", a, pool)
        return cache[k]
    out = {}
    for name, base, cand in specs:
        ob, oc = get(base), get(cand)
        ab, nd = pooled_auc(Y, ob, g)
        ac, _ = pooled_auc(Y, oc, g)
        gb, gc = group_aucs(Y, ob, g), group_aucs(Y, oc, g)
        r = {"auc_base": ab, "auc_cand": ac, "delta": ac - ab, "n_groups_dropped": nd,
             "per_group": {lg: {"base": gb[lg], "cand": gc[lg],
                                "delta": (gc[lg] - gb[lg]) if np.isfinite(gb[lg]) and np.isfinite(gc[lg]) else math.nan}
                           for lg in GROUPS},
             "brier_base": float(np.nanmean((ob - Y) ** 2)), "brier_cand": float(np.nanmean((oc - Y) ** 2))}
        if keep_oof:
            r["oof_base"], r["oof_cand"] = ob, oc
        out[name] = r
    return out


def resample(df: pd.DataFrame, rng: np.random.Generator, stratified: bool = False) -> pd.DataFrame:
    """Concept-clustered resample; every duplicated concept gets a fresh cluster id ('cl')."""
    cons = df["concept"].unique()
    rows = {c: np.flatnonzero(df["concept"].to_numpy() == c) for c in cons}
    if stratified:
        cg = df.groupby("concept")["group"].first()
        pick = np.concatenate([rng.choice(cg.index[cg == lg].to_numpy(), (cg == lg).sum())
                               for lg in GROUPS if (cg == lg).sum()])
    else:
        pick = rng.choice(cons, len(cons))
    idx, cid = [], []
    for k, c in enumerate(pick):
        idx.append(rows[c])
        cid.append(np.full(len(rows[c]), k))
    d = df.iloc[np.concatenate(idx)].reset_index(drop=True)
    d["cl"] = np.concatenate(cid)
    return d


def boot_worker(args: tuple) -> list[dict]:
    """One chunk of refit bootstrap draws. args = (df, specs, seeds, a, pool, stratified)."""
    df, specs, seeds, a, pool, stratified = args
    res = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        d = resample(df, rng, stratified)
        r = eval_specs(d, specs, a, pool)
        res.append({k: {"delta": v["delta"], "nd": v["n_groups_dropped"],
                        "pg": {lg: v["per_group"][lg]["delta"] for lg in GROUPS}} for k, v in r.items()})
    return res


def perm_worker(args: tuple) -> list[dict]:
    """Placebo gateway vectors: args = (df, W, base_cols, gvecs, a). Returns point delta-AUC per vector for each base."""
    df, W, bases, gvecs = args
    Y = df["R"].to_numpy(float)
    g = df["group"].to_numpy()
    base_auc = {nm: pooled_auc(Y, S4.logo_predict(df, cols, "R", "logit"), g)[0] for nm, cols in bases.items()}
    out = []
    for gv in gvecs:
        d = df.copy()
        d["g_plac"] = W @ gv
        r = {}
        for nm, cols in bases.items():
            r[nm] = pooled_auc(Y, S4.logo_predict(d, cols + ["g_plac"], "R", "logit"), g)[0] - base_auc[nm]
        out.append(r)
    return out


# ----------------------------------------------------------------------------- concept-level O1 (Block D)
def o1_base(home: np.ndarray, cl: np.ndarray, y: np.ndarray, grp: np.ndarray, test_g: str) -> np.ndarray:
    """Training-fold mean O1 of concepts sharing the home field (leave-own-concept-out for training rows),
    falling back to the training-fold global mean."""
    tr = grp != test_g
    out = np.empty(len(y))
    gm = y[tr].mean()
    for i in range(len(y)):
        m = tr & (home == home[i]) & (cl != cl[i])
        out[i] = y[m].mean() if m.sum() else (y[tr & (cl != cl[i])].mean() if tr[i] else gm)
    return out


def logo_concept(df: pd.DataFrame, cols: list[str], y: str) -> np.ndarray:
    dyn = "O1_base" in cols
    if not dyn:
        return S4.logo_predict(df, cols, y, "logit")
    oof = np.full(len(df), np.nan)
    g = df["group"].to_numpy()
    Y = df[y].to_numpy(float)
    for lg in GROUPS:
        te = g == lg
        tr = ~te
        if te.sum() == 0 or tr.sum() < 5:
            continue
        X = df[[c for c in cols if c != "O1_base"]].copy()
        X["O1_base"] = o1_base(df["home"].to_numpy(), df["cl"].to_numpy(), Y, g, lg)
        X = X[cols]
        Xa = S4._prep(X, tr)
        yt = Y[tr]
        if len(np.unique(yt)) < 2:
            oof[te] = yt.mean()
            continue
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000))
        m.fit(Xa[tr], yt.astype(int))
        oof[te] = m.predict_proba(Xa[te])[:, 1]
    return oof


def concept_specs_eval(df: pd.DataFrame, specs: list[tuple[str, list[str], list[str]]], y: str = "O1") -> dict:
    cache = {}
    Y = df[y].to_numpy(float)
    g = df["group"].to_numpy()

    def get(cols):
        k = tuple(cols)
        if k not in cache:
            cache[k] = logo_concept(df, list(cols), y)
        return cache[k]
    out = {}
    for nm, b, c in specs:
        ob, oc = get(b), get(c)
        ab, ac = fast_auc(Y, ob), fast_auc(Y, oc)
        pg = {}
        for lg in GROUPS:
            m = g == lg
            x1, x2 = fast_auc(Y[m], ob[m]), fast_auc(Y[m], oc[m])
            pg[lg] = x2 - x1 if np.isfinite(x1) and np.isfinite(x2) else math.nan
        out[nm] = {"base": ab, "cand": ac, "delta": ac - ab, "per_group": pg}
    return out


def concept_boot_worker(args: tuple) -> list[dict]:
    df, specs, seeds = args
    res = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        idx = rng.integers(0, len(df), len(df))
        d = df.iloc[idx].reset_index(drop=True)
        d["cl"] = np.arange(len(d))
        r = concept_specs_eval(d, specs)
        res.append({k: v["delta"] for k, v in r.items()})
    return res


# ----------------------------------------------------------------------------- Block E simulation
def sim_worker(args: tuple) -> list[float]:
    """Simulate clustered episodes from the fitted M2+gateway model and return sampling draws of 4-fold grouped-CV
    delta-AUC. args = (Xpool, beta0, beta, gcol, sigma_c, N, m, seeds)."""
    from sklearn.model_selection import GroupKFold
    Xpool, b0, beta, gcol, sig, N, m, seeds = args[:8]
    keyc, tau_f = (args[8], args[9]) if len(args) > 8 else (None, 0.0)
    out = []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        nc = int(math.ceil(N / m))
        idx = rng.integers(0, len(Xpool), nc * m)
        X = Xpool[idx]
        conc = np.repeat(np.arange(nc), m)
        u = rng.normal(0, sig, nc)[conc]
        eta = b0 + X @ beta + u
        if keyc is not None and tau_f > 0:  # field random intercept: arbitrary field constants can absorb it
            eta = eta + rng.normal(0, tau_f, int(keyc.max()) + 1)[keyc[idx]]
        y = rng.random(len(eta)) < 1 / (1 + np.exp(-eta))
        if y.all() or (~y).all():
            continue
        pb = np.full(len(y), np.nan)
        pc = np.full(len(y), np.nan)
        base_cols = [i for i in range(X.shape[1]) if i != gcol]
        for tr, te in GroupKFold(4).split(X, y, conc):
            if len(np.unique(y[tr])) < 2:
                continue
            for cols, dest in ((base_cols, pb), (list(range(X.shape[1])), pc)):
                mdl = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=1000))
                mdl.fit(X[tr][:, cols], y[tr])
                dest[te] = mdl.predict_proba(X[te][:, cols])[:, 1]
        out.append(fast_auc(y.astype(float), pc) - fast_auc(y.astype(float), pb))
    return out
