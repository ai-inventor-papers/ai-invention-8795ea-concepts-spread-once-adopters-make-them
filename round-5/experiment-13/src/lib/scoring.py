"""Frame-N scoring tables (frozen at S7; used by s8_unseal.py, the S7 dry run and the power simulation).

Every psp cell: partial Spearman given the rung covariates, 95% percentile CI from a refit concept bootstrap, n,
one-sided bootstrap p in the frozen direction. Cells run in a spawn process pool (one DataFrame per worker)."""
from __future__ import annotations

import math
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import rankdata

from laddern import POOL_GROUPS, RUNGS, holm, paired_diff, per_group, psp_boot2, psp_df, psp_point, rung_design

INDICES = ["OPEN_home", "OPEN_all", "OPEN_sizematch", "NOVCHURN_home"]
COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
_DF: dict = {}


def _load(path: str) -> pd.DataFrame:
    if path not in _DF:
        _DF.clear()
        _DF[path] = pd.read_parquet(path)
    return _DF[path]


def psp_custom(df: pd.DataFrame, x: str, y: str, cont: list[str], n_boot: int, seed: int, direction: int = 1) -> dict:
    B = df[cont].to_numpy(float) if cont else np.zeros((len(df), 0))
    r = psp_boot2(df[x].to_numpy(float), df[y].to_numpy(float), B, np.zeros((len(df), 0)), n_boot, seed, direction)
    r.pop("boot", None)
    r.update({"x": x, "y": y, "covariates": cont, "resampling_unit": "concept", "n_boot": n_boot})
    return r


def spearman_boot(df: pd.DataFrame, x: str, y: str, n_boot: int, seed: int) -> dict:
    a, b = df[x].to_numpy(float), df[y].to_numpy(float)
    ok = np.isfinite(a) & np.isfinite(b)
    a, b = a[ok], b[ok]
    n = len(a)
    if n < 30:
        return {"n": n, "rho": math.nan, "ci": [math.nan, math.nan]}
    rho = float(stats.spearmanr(a, b)[0])
    rng = np.random.default_rng(seed)
    ra, rb = a, b
    bs = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        bs.append(stats.spearmanr(ra[i], rb[i])[0])
    bs = np.asarray(bs, float)
    bs = bs[np.isfinite(bs)]
    return {"n": int(n), "rho": rho, "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "p_one_gt0": float((np.sum(bs <= 0) + 1) / (len(bs) + 1)), "x": x, "y": y, "n_boot": n_boot,
            "resampling_unit": "concept"}


def _logit(X: np.ndarray, y: np.ndarray, iters: int = 60) -> np.ndarray:
    A = np.c_[np.ones(len(y)), X]
    w = np.zeros(A.shape[1])
    lam = 1e-4
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(A @ w, -30, 30)))
        g = A.T @ (p - y) + lam * np.r_[0, w[1:]]
        H = (A * (p * (1 - p))[:, None]).T @ A + lam * np.diag(np.r_[0, np.ones(len(w) - 1)])
        step = np.linalg.solve(H + 1e-9 * np.eye(len(w)), g)
        w -= step
        if np.abs(step).max() < 1e-8:
            break
    return w


def palla(df: pd.DataFrame, y: str, n_boot: int, seed: int, binary: bool) -> dict:
    Bc, Cc = rung_design(df, "R3")
    z = lambda v: (v - np.nanmean(v)) / np.nanstd(v)  # noqa: E731
    lv, ep = z(df.logvol.to_numpy(float)), z(df.edge_persistence__home.to_numpy(float))
    X = np.c_[rankdata(Bc.to_numpy(float), axis=0) / len(df), Cc.to_numpy(float), lv, ep, lv * ep]
    yy = df[y].to_numpy(float)
    ok = np.isfinite(yy) & np.all(np.isfinite(X), 1)
    X, yy = X[ok], yy[ok]
    n = len(yy)
    if n < 50 or (binary and (yy.sum() < 10 or (1 - yy).sum() < 10)):
        return {"n": int(n), "coef": math.nan, "ci": [math.nan, math.nan]}
    if not binary:
        yy = rankdata(yy) / n

    def fit(Xs, ys):
        keep = Xs.std(0) > 0
        keep[-3:] = True
        Xs = Xs[:, keep]
        if binary:
            return _logit(Xs, ys)[-1]
        A = np.c_[np.ones(len(ys)), Xs]
        return np.linalg.lstsq(A, ys, rcond=None)[0][-1]
    est = float(fit(X, yy))
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        try:
            bs.append(fit(X[i], yy[i]))
        except np.linalg.LinAlgError:
            continue
    bs = np.asarray(bs, float)
    bs = bs[np.isfinite(bs)]
    return {"n": int(n), "outcome": y, "model": "logit" if binary else "OLS on rank(y)/n",
            "term": "z(logvol) x z(edge_persistence_home)", "coef": est,
            "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "n_boot": int(len(bs)),
            "covariates": "R3 (ranked continuous + dummies) + z(logvol) + z(edge_persistence_home)"}


def run_cell(path: str, kind: str, key: str, kw: dict) -> tuple[str, str, dict]:
    df = _load(path)
    if "subset" in kw:
        col, val = kw.pop("subset")
        df = df[df[col] == val] if not isinstance(val, list) else df[df[col].isin(val)]
    if "mask" in kw:
        df = df[df[kw.pop("mask")].astype(bool)]
    if kind == "psp":
        return kind, key, psp_df(df, **kw)
    if kind == "group":
        return kind, key, per_group(df, **kw)
    if kind == "pair":
        return kind, key, paired_diff(df, **kw)
    if kind == "custom":
        return kind, key, psp_custom(df, **kw)
    if kind == "spear":
        return kind, key, spearman_boot(df, **kw)
    if kind == "palla":
        return kind, key, palla(df, **kw)
    raise ValueError(kind)


def run_cells(path: str, cells: list[tuple[str, str, dict]], workers: int, log=None) -> dict:
    out: dict = {}
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        futs = [ex.submit(run_cell, path, k, key, dict(kw)) for k, key, kw in cells]
        for i, f in enumerate(futs):
            kind, key, r = f.result()
            out[key] = r
            if log and (i % 25 == 0 or i == len(futs) - 1):
                log(f"cells {i+1}/{len(futs)}")
    return out


def cells_for(prim: str, B: int, seed: int, have_type_agree: bool) -> list:
    Bm = min(1000, B)
    cells = []
    for x in INDICES:
        for y in (prim, "O2r_resid", "O2r_m30" if prim != "O2r_m30" else "O2r_m50"):
            for r in RUNGS:
                cells.append(("psp", f"ladder|{x}|{y}|{r}", dict(xcol=x, ycol=y, rung=r, n_boot=B, seed=seed)))
    for x in INDICES:
        for r in ("R3",):
            cells.append(("group", f"groups|{x}|{prim}|{r}", dict(xcol=x, ycol=prim, rung=r, n_boot=Bm, seed=seed)))
    for t in ("method", "object"):
        for x in INDICES:
            kw = dict(xcol=x, ycol=prim, rung="R3", n_boot=Bm, seed=seed, drop_type=True, subset=("type", t))
            if have_type_agree:
                kw["mask"] = "type_agree"
            cells.append(("psp", f"type|{x}|{t}|R3", kw))
    for b in ("home", "all"):
        for k in COMPONENTS:
            for r in ("R2", "R3"):
                cells.append(("psp", f"comp|{k}__{b}|{prim}|{r}", dict(xcol=f"{k}__{b}", ycol=prim, rung=r,
                                                                       n_boot=Bm, seed=seed)))
    cells.append(("pair", "coupling|all_minus_home|R3", dict(xa="OPEN_all", xb="OPEN_home", ycol=prim, rung="R3",
                                                            n_boot=B, seed=seed)))
    cells.append(("pair", "coupling|sizematch_minus_home|R3", dict(xa="OPEN_sizematch", xb="OPEN_home", ycol=prim,
                                                                  rung="R3", n_boot=B, seed=seed)))
    cells.append(("psp", "coupling|OPEN_all_on_home_sample|R3", dict(xcol="OPEN_all", ycol=prim, rung="R3",
                                                                    n_boot=Bm, seed=seed, mask="has_open_home")))
    for c in ("CHENG_consistency_home", "CHENG_consistency_all", "CHENG_embeddedness_home", "CHENG_prominence_home"):
        cells.append(("spear", f"cheng|{c}|V_next|raw", dict(x=c, y="V_next", n_boot=B, seed=seed)))
        cells.append(("custom", f"cheng|{c}|V_next|logN2", dict(x=c, y="V_next", cont=["logN2"], n_boot=B,
                                                                 seed=seed)))
        for y in (prim, "O2r_resid", "O1c", "O1b", "O3", "V_next"):
            cells.append(("psp", f"cheng|{c}|{y}|R0", dict(xcol=c, ycol=y, rung="R0", n_boot=B if y == prim else Bm,
                                                            seed=seed, direction=-1)))
    cells.append(("spear", "cheng|consistency_vs_persistence", dict(x="CHENG_consistency_home",
                                                                    y="edge_persistence__home", n_boot=Bm, seed=seed)))
    cells.append(("spear", "cheng|consistency_vs_logvol", dict(x="CHENG_consistency_home", y="logvol", n_boot=Bm,
                                                               seed=seed)))
    cells.append(("psp", "palla_psp|edge_persistence__home|O3|R3", dict(xcol="edge_persistence__home", ycol="O3",
                                                                         rung="R3", n_boot=Bm, seed=seed)))
    for y, binary in ((prim, False), ("O3", True), ("O1b", True)):
        cells.append(("palla", f"palla|{y}", dict(y=y, n_boot=Bm, seed=seed, binary=binary)))
    for x, d in (("ego_density_W3_cz", -1), ("edge_persistence_sz", -1), ("NOVCHURN_home_rare", 1),
                 ("edge_persistence_excess", -1), ("NOVCHURN_clean", 1), ("CONTACT_REACH", 1),
                 ("RETENTION_RATIO_early", -1), ("n_authors_early", 1)):
        r = "R3" if x not in ("CONTACT_REACH", "RETENTION_RATIO_early") else "R0"
        cells.append(("psp", f"clean|{x}|{prim}|{r}", dict(xcol=x, ycol=prim, rung=r, n_boot=Bm, seed=seed,
                                                            direction=d)))
    cells.append(("psp", f"clean|n_comm_W3__home|{prim}|R3", dict(xcol="n_comm_W3__home", ycol=prim, rung="R3",
                                                                  n_boot=B, seed=seed)))
    for y in ("O3", "O1b", "O1c"):
        cells.append(("psp", f"secondary|NOVCHURN_home|{y}|R3", dict(xcol="NOVCHURN_home", ycol=y, rung="R3",
                                                                      n_boot=Bm, seed=seed)))
        cells.append(("psp", f"secondary|OPEN_home|{y}|R3", dict(xcol="OPEN_home", ycol=y, rung="R3", n_boot=Bm,
                                                                  seed=seed)))
    return cells


# ----------------------------------------------------------------------------- forecasting
def cv_forecast(df: pd.DataFrame, prim: str, B: int, seed: int) -> dict:
    """5-fold CV (folds stratified by group, seed 0) OLS: B5 vs B5+OPEN_home vs B5+NOVCHURN_home."""
    feats = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
    d = df[np.isfinite(df[prim]) & np.isfinite(df.OPEN_home) & np.isfinite(df.NOVCHURN_home)].copy()
    d = d[np.all(np.isfinite(d[feats].to_numpy(float)), 1)].reset_index(drop=True)
    n = len(d)
    if n < 100:
        return {"n": n}
    rng = np.random.default_rng(0)
    fold = np.zeros(n, int)
    for g, idx in d.groupby("agroup").groups.items():
        idx = rng.permutation(np.asarray(idx))
        fold[idx] = np.arange(len(idx)) % 5
    preds = {}
    for name, extra in (("B5", []), ("B5_plus_OPEN_home", ["OPEN_home"]), ("B5_plus_NOVCHURN_home", ["NOVCHURN_home"])):
        X = d[feats + extra].to_numpy(float)
        p = np.zeros(n)
        for k in range(5):
            tr, te = fold != k, fold == k
            mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
            A = np.c_[np.ones(tr.sum()), (X[tr] - mu) / sd]
            beta = np.linalg.lstsq(A, d[prim].to_numpy(float)[tr], rcond=None)[0]
            p[te] = np.c_[np.ones(te.sum()), (X[te] - mu) / sd] @ beta
        preds[name] = p
    y = d[prim].to_numpy(float)
    top = (y >= np.quantile(y, 2 / 3)).astype(int)

    def auc(lab, s):
        r = rankdata(s)
        n1 = lab.sum()
        n0 = len(lab) - n1
        return float((r[lab == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
    res = {"n": n, "folds": "5, stratified by group, seed 0", "models": {}}
    for k, p in preds.items():
        res["models"][k] = {"spearman": float(stats.spearmanr(p, y)[0]), "auc_top_tercile": auc(top, p)}
    rngb = np.random.default_rng(seed)
    for k in ("B5_plus_OPEN_home", "B5_plus_NOVCHURN_home"):
        ds, da = [], []
        for _ in range(B):
            i = rngb.integers(0, n, n)
            ds.append(stats.spearmanr(preds[k][i], y[i])[0] - stats.spearmanr(preds["B5"][i], y[i])[0])
            if 0 < top[i].sum() < n:
                da.append(auc(top[i], preds[k][i]) - auc(top[i], preds["B5"][i]))
        res["models"][k]["d_spearman_vs_B5"] = res["models"][k]["spearman"] - res["models"]["B5"]["spearman"]
        res["models"][k]["d_spearman_ci"] = [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))]
        res["models"][k]["d_auc_vs_B5"] = res["models"][k]["auc_top_tercile"] - res["models"]["B5"]["auc_top_tercile"]
        res["models"][k]["d_auc_ci"] = [float(np.percentile(da, 2.5)), float(np.percentile(da, 97.5))]
    d["pred_cv_b5_novchurn"] = preds["B5_plus_NOVCHURN_home"]
    res["_pred_novchurn"] = dict(zip(d.ci.astype(int), preds["B5_plus_NOVCHURN_home"]))
    return res


def frozen_prediction(df: pd.DataFrame, pm: dict, prim: str, B: int, seed: int) -> tuple[dict, pd.DataFrame]:
    mu, sd = pd.Series(pm["B5"]["mu"]), pd.Series(pm["B5"]["sd"])
    Z = ((df[list(mu.index)] - mu) / sd).to_numpy(float)
    X0 = np.c_[np.ones(len(df)), Z]
    df = df.copy()
    df["pred_b5"] = X0 @ np.asarray(pm["B5"]["coef"])
    df["pred_b5_open"] = np.c_[X0, df.OPEN_home.to_numpy(float)] @ np.asarray(pm["B5_plus_OPEN_home"]["coef"])
    ok = np.isfinite(df[prim]) & np.isfinite(df.pred_b5) & np.isfinite(df.pred_b5_open)
    y_, p0, p1 = df[prim][ok].to_numpy(), df.pred_b5[ok].to_numpy(), df.pred_b5_open[ok].to_numpy()
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(B):
        i = rng.integers(0, len(y_), len(y_))
        bs.append(stats.spearmanr(p1[i], y_[i])[0] - stats.spearmanr(p0[i], y_[i])[0])
    return ({"n": int(ok.sum()), "spearman_B5": float(stats.spearmanr(p0, y_)[0]),
             "spearman_B5_plus_OPEN_home": float(stats.spearmanr(p1, y_)[0]),
             "diff": float(stats.spearmanr(p1, y_)[0] - stats.spearmanr(p0, y_)[0]),
             "diff_ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
             "note": "EXP5-fitted frozen OLS (TAG-grounded B5); Frame-N features are MATCH-grounded (scale shift)"},
            df[["ci", "pred_b5", "pred_b5_open"]])


# ----------------------------------------------------------------------------- placebo / planted
def _perm_within(y: np.ndarray, g: np.ndarray, rng) -> np.ndarray:
    yp = y.copy()
    for k in np.unique(g):
        m = g == k
        yp[m] = rng.permutation(yp[m])
    return yp


def placebo_task(args) -> list[float]:
    x, y, B_, C_, g, seed, n = args
    rng = np.random.default_rng(seed)
    return [psp_point(_perm_within(x, g, rng), y, B_, C_) for _ in range(n)]


def planted_task(args) -> list[tuple[float, float]]:
    x, y, B_, C_, g, seed, n, n_boot, target = args
    rng = np.random.default_rng(seed)
    Z = np.c_[np.ones(len(x)), rankdata(B_, axis=0), C_]
    rx = rankdata(x) - Z @ np.linalg.lstsq(Z, rankdata(x), rcond=None)[0]
    out = []
    for _ in range(n):
        yp = _perm_within(y, g, rng)
        zr = (rankdata(yp) - rankdata(yp).mean()) / rankdata(yp).std()
        delta = target / math.sqrt(1 - target ** 2)
        yplant = zr + delta * rx / rx.std()
        r = psp_boot2(x, yplant, B_, C_, n_boot, int(rng.integers(1 << 30)), 1)
        out.append((r["rho"], r["ci"][0]))
    return out


def placebo_planted(df: pd.DataFrame, prim: str, seed: int, workers: int, n_perm: int = 200, n_plant: int = 100,
                    n_boot_plant: int = 400, rung: str = "R3") -> dict:
    Bc, Cc = rung_design(df, rung)
    x, y = df.OPEN_home.to_numpy(float), df[prim].to_numpy(float)
    B_, C_ = Bc.to_numpy(float), Cc.to_numpy(float)
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B_), 1)
    x, y, B_, C_, g = x[ok], y[ok], B_[ok], C_[ok], df.agroup.to_numpy()[ok]
    keep = C_.std(0) > 0
    C_ = C_[:, keep]
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        per = max(1, n_perm // workers)
        tasks = [(x, y, B_, C_, g, seed + 11 * k, per) for k in range(math.ceil(n_perm / per))]
        perm = np.asarray([v for r in ex.map(placebo_task, tasks) for v in r])[:n_perm]
        per2 = max(1, n_plant // workers)
        tasks = [(x, y, B_, C_, g, seed + 7 * k + 1, per2, n_boot_plant, 0.10) for k in range(math.ceil(n_plant / per2))]
        pl = [v for r in ex.map(planted_task, tasks) for v in r][:n_plant]
    pl = np.asarray(pl, float)
    return {"placebo_within_group_shuffle_OPEN_home": {"n_perm": int(len(perm)), "rung": rung,
                                                        "mean": float(perm.mean()),
                                                        "q95_abs": float(np.percentile(np.abs(perm), 95))},
            "planted_0.10": {"n_draws": int(len(pl)), "rung": rung, "mean_estimate": float(pl[:, 0].mean()),
                             "recovery_rate_ci_low_gt0": float((pl[:, 1] > 0).mean()),
                             "n_boot_per_draw": n_boot_plant,
                             "note": "y' = z(rank(within-group permuted y)) + delta*z(resid OPEN_home), psp target 0.10"}}


# ----------------------------------------------------------------------------- verdicts
def verdict(res: dict, prim: str, power_joint: float | None) -> dict:
    L = res["cells"]
    o3, o5 = L[f"ladder|OPEN_home|{prim}|R3"], L[f"ladder|OPEN_home|{prim}|R5"]
    nv3 = L[f"ladder|NOVCHURN_home|{prim}|R3"]
    grp = L[f"groups|OPEN_home|{prim}|R3"]
    ne, npos = grp["n_estimable"], grp["n_positive"]
    if ne >= 5:
        gclause, geval = npos >= 4, True
    elif ne == 4:
        gclause, geval = npos == 4, True
    else:
        gclause, geval = False, False
    c = {"open_home_R3_ci_gt0": bool(o3["ci"][0] > 0), "open_home_R5_ci_gt0": bool(o5["ci"][0] > 0),
         "group_clause": bool(gclause), "group_clause_evaluable": geval,
         "novchurn_R3_ci_gt0": bool(nv3["ci"][0] > 0)}
    if c["open_home_R3_ci_gt0"] and c["open_home_R5_ci_gt0"] and gclause and c["novchurn_R3_ci_gt0"]:
        v = "CONFIRMED"
    elif c["open_home_R3_ci_gt0"] or c["novchurn_R3_ci_gt0"]:
        v = "PARTIAL"
    else:
        v = "NOT CONFIRMED"
    caps = []
    if v == "CONFIRMED" and not geval:
        v, _ = "PARTIAL", caps.append("group clause not evaluable (<= 3 estimable groups)")
    if v == "CONFIRMED" and power_joint is not None and power_joint < 0.5:
        v, _ = "PARTIAL", caps.append(f"pre-unseal power {power_joint:.2f} < 0.5")
    hp = res["holm"]
    fam = list(hp.keys())
    confirmed_holm = all(hp[k]["p_holm"] < 0.05 for k in fam[:3])
    ch_raw = L["cheng|CHENG_consistency_home|V_next|raw"]
    ch_o2 = L[f"cheng|CHENG_consistency_home|{prim}|R0"]
    ch_sz = L["cheng|CHENG_consistency_home|V_next|logN2"]
    reversal = bool(ch_raw["ci"][0] > 0 and ch_o2["ci"][1] < 0)
    fails_as_size = bool(ch_sz["ci"][0] <= 0 <= ch_sz["ci"][1])
    cp = L["coupling|all_minus_home|R3"]
    nc = L[f"clean|n_comm_W3__home|{prim}|R3"]
    coupling = bool(cp["ci"][0] > 0 and nc["ci"][0] <= 0 <= nc["ci"][1])
    return {"verdict": v, "clauses": c, "caps": caps, "n_estimable_groups": ne, "n_positive_groups": npos,
            "CONFIRMED_HOLM": bool(confirmed_holm),
            "reversal": {"REVERSAL_CONFIRMED": reversal, "raw_rho_V_next": ch_raw["rho"], "raw_ci": ch_raw["ci"],
                         f"psp_{prim}_R0": ch_o2["rho"], f"psp_{prim}_R0_ci": ch_o2["ci"],
                         "REVERSAL_FAILS_AS_SIZE": fails_as_size, "psp_V_next_given_logN2": ch_sz["rho"],
                         "psp_V_next_given_logN2_ci": ch_sz["ci"],
                         "statement": ("Cheng consistency effect is a size effect" if fails_as_size else
                                       "Cheng consistency effect on V_next survives the size control")},
            "coupling": {"COUPLING_WARNING_CONFIRMED": coupling, "all_minus_home": cp["diff"],
                         "all_minus_home_ci": cp["ci"], "n_comm_W3_home_psp": nc["rho"], "n_comm_W3_home_ci": nc["ci"]}}


def holm_table(cells: dict, prim: str) -> dict:
    fam = [(f"OPEN_home|{prim}|R3", cells[f"ladder|OPEN_home|{prim}|R3"]["p_one"]),
           (f"OPEN_home|{prim}|R5", cells[f"ladder|OPEN_home|{prim}|R5"]["p_one"]),
           (f"NOVCHURN_home|{prim}|R3", cells[f"ladder|NOVCHURN_home|{prim}|R3"]["p_one"]),
           (f"CHENG_consistency_home|{prim}|R0 (<0)", cells[f"cheng|CHENG_consistency_home|{prim}|R0"]["p_one"]),
           (f"OPEN_all-OPEN_home|{prim}|R3 paired", cells["coupling|all_minus_home|R3"]["p_one"])]
    ph = holm([p for _, p in fam])
    return {k: {"p_one": p, "p_holm": h} for (k, p), h in zip(fam, ph)}
