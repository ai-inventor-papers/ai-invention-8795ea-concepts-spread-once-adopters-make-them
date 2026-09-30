"""S4 (test B: static early trait vs reach / depth), S6 (test D: Palla size x turnover), S7 (test E: coupling).

psp = partial Spearman = Pearson(resid(rank x | Z), resid(rank y | Z)), Z = [1, rank(B5), dummies]; ranks and the
residualisation are recomputed inside every concept-bootstrap draw (EXP8 rq1stats.psp_point logic). Several x / y
columns share one draw (same resampled concepts), so paired differences use the SAME draws on a common complete-case
set. Covariates: B5 + onset-year dummies; + 8-group dummies when groups are pooled; + body dummies when bodies are
pooled; + window_flag for the 2015-17 cohort (EXP10 R0). All tables: selection data, not confirmation."""
from __future__ import annotations

import math
import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import rankdata

from common import (B5, BODY_COHORT, DATA, DEPTH, EXP8, EXP10, GROUP5, GROUPS5, N_BOOT_STATIC, REACH, RES, SEED,
                    SELECTION_LABEL, body_of_split, jdump, n_workers)
from rq1stats import dersimonian_laird

OUTS = REACH + DEPTH
TRAITS2 = ["EMB_early_home", "SOC_early_home", "CONS_early_all", "CONS_r_early_home", "EMB_cos_early_home"]
PRIMARY = "EXP5_pooled"


# ----------------------------------------------------------------------------- data
def static_frame() -> pd.DataFrame:
    st = pd.read_parquet(DATA / "cheng_static.parquet")
    a5 = pd.read_parquet(EXP8 / "data/analysis_table.parquet",
                         columns=["ci", "t0", "group", "split", "name"] + B5 + OUTS)
    a5["body"] = a5.split.map(body_of_split)
    a5["window_flag"] = 0
    V = pd.read_parquet(DATA / "V_exp5.parquet", columns=["ci", "year", "V"])
    a5 = a5.merge(V.rename(columns={"year": "y2", "V": "V_t0p2"}).assign(y2=lambda x: x.y2), how="left",
                  left_on=["ci", a5.t0 + 2], right_on=["ci", "y2"]).drop(columns=["y2"])
    a5 = a5.merge(V.rename(columns={"year": "y3", "V": "V_t0p3"}), how="left",
                  left_on=["ci", a5.t0 + 3], right_on=["ci", "y3"]).drop(columns=["y3"])
    a5 = a5.drop(columns=[c for c in a5.columns if c.startswith("key_")])
    ac = pd.read_parquet(EXP10 / "data/analysis_cohort.parquet")
    ac["body"] = BODY_COHORT
    ac["split"] = "COHORT_2015_17"
    vc = pd.read_parquet(DATA / "V_cohort.parquet", columns=["ci", "V_t0p2", "V_t0p3"])
    ac = ac.merge(vc, on="ci", how="left")
    keep = ["ci", "t0", "group", "split", "name", "body", "window_flag", "V_t0p2", "V_t0p3"] + B5 + OUTS
    extra = ["CONTACT_REACH", "type", "generic", "level", "fp_logN", "fp_nfields", "fp_reemerge", "fp_wiki_pre",
             "newborn", "label_coverage_early", "home_coverage_early", "agroup"]
    df = pd.concat([a5[keep], ac[keep + extra]], ignore_index=True)
    s = st.drop(columns=["body", "t0", "group"])
    df = df.merge(s, on="ci", how="left", suffixes=("", "_st"))
    df["group5"] = df.group.map(GROUP5)
    df["logV_t0p2"] = np.log1p(df.V_t0p2)
    return df


def body_frames(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    out = {PRIMARY: df[df.body != BODY_COHORT]}
    for b in ["DEV", "OLD_HELDOUT", "COHORT_2010_14", BODY_COHORT]:
        out[b] = df[df.body == b]
    return out


def dummies(v: np.ndarray) -> np.ndarray:
    u = np.unique(v)
    if len(u) <= 1:
        return np.zeros((len(v), 0))
    return (v[:, None] == u[None, 1:]).astype(float)


def design(d: pd.DataFrame, cont: list[str] | None = None, groups: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """(continuous covariates to be ranked, raw dummy matrix)."""
    cont = B5 if cont is None else cont
    cat = [dummies(d.t0.to_numpy())]
    if groups:
        cat.append(dummies(d.group.astype(str).to_numpy()))
    cat.append(dummies(d.body.astype(str).to_numpy()))
    if d.window_flag.nunique() > 1:
        cat.append(d[["window_flag"]].to_numpy(float))
    return d[cont].to_numpy(float), np.hstack(cat)


# ----------------------------------------------------------------------------- multi-psp bootstrap engine
def _resid_corr(xr: np.ndarray, yr: np.ndarray, Br: np.ndarray, C: np.ndarray) -> np.ndarray:
    Z = np.hstack([np.ones((len(xr), 1)), Br, C])
    Yall = np.hstack([xr, yr])
    beta, *_ = np.linalg.lstsq(Z, Yall, rcond=None)
    R = Yall - Z @ beta
    R -= R.mean(0)
    s = R.std(0)
    s[s < 1e-12] = np.nan
    R /= s
    nx = xr.shape[1]
    return (R[:, :nx].T @ R[:, nx:]) / len(R)                      # [nx, ny] Pearson of residuals


def psp_multi(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:
    Br = rankdata(B, axis=0) if B.shape[1] else np.zeros((len(X), 0))
    return _resid_corr(rankdata(X, axis=0), rankdata(Y, axis=0), Br, C)


def unique_ids(M: np.ndarray) -> list[tuple[np.ndarray, int]]:
    """Per column: ids of the value-sorted unique values (so ranks of any resample follow from bincounts)."""
    out = []
    for j in range(M.shape[1]):
        _, inv = np.unique(M[:, j], return_inverse=True)
        out.append((inv.astype(np.int64), int(inv.max()) + 1))
    return out


def resample_ranks(uids: list[tuple[np.ndarray, int]], idx: np.ndarray) -> np.ndarray:
    """Average ranks (identical to scipy rankdata 'average') of every column within the resample idx, scaled by
    1/n. For unique value k with c_k copies: rank = cumsum(c)_k - (c_k - 1)/2. No sort needed."""
    n = len(idx)
    R = np.empty((n, len(uids)))
    for j, (u, U) in enumerate(uids):
        ui = u[idx]
        c = np.bincount(ui, minlength=U)
        avg = np.cumsum(c) - (c - 1) / 2.0
        R[:, j] = avg[ui] / n
    return R


def fast_corr(RX: np.ndarray, RY: np.ndarray, RB: np.ndarray, C: np.ndarray) -> np.ndarray:
    """Residual-correlation matrix via the pseudo-inverse of Z'Z (min-norm LS; exact projection even when the
    dummy block is rank deficient)."""
    Z = np.hstack([np.ones((len(RX), 1)), RB, C])
    V = np.hstack([RX, RY])
    ZtZ = Z.T @ Z
    beta = np.linalg.pinv(ZtZ, rcond=1e-12, hermitian=True) @ (Z.T @ V)
    R = V - Z @ beta
    R -= R.mean(0)
    s = R.std(0)
    s[s < 1e-12] = np.nan
    R /= s
    nx = RX.shape[1]
    return (R[:, :nx].T @ R[:, nx:]) / len(R)


def multi_boot(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray, n_boot: int, seed: int,
               check: bool = True) -> dict:
    ok = np.all(np.isfinite(X), 1) & np.all(np.isfinite(Y), 1) & np.all(np.isfinite(B), 1)
    X, Y, B, C = X[ok], Y[ok], B[ok], C[ok]
    n = len(X)
    if n < 30:
        return {"n": n, "est": np.full((X.shape[1], Y.shape[1]), np.nan), "boot": np.zeros((0, X.shape[1], Y.shape[1]))}
    keep = C.std(0) > 0
    est = psp_multi(X, Y, B, C[:, keep])                           # exact path (lstsq, scipy rankdata)
    ux, uy, ub = unique_ids(X), unique_ids(Y), unique_ids(B)
    rng = np.random.default_rng(seed)
    bs = np.empty((n_boot, X.shape[1], Y.shape[1]))
    max_dev = 0.0
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        bs[b] = fast_corr(resample_ranks(ux, i), resample_ranks(uy, i), resample_ranks(ub, i), C[i])
        if check and b < 2:                                         # fast path == exact path on the first draws
            Ci = C[i]
            ex = psp_multi(X[i], Y[i], B[i], Ci[:, Ci.std(0) > 0])
            max_dev = max(max_dev, float(np.nanmax(np.abs(ex - bs[b]))))
    if max_dev > 1e-8:
        raise ValueError(f"fast bootstrap path deviates from exact psp by {max_dev:.2e}")
    return {"n": n, "est": est, "boot": bs, "fast_path_max_dev": max_dev}


def summ(est: float, bs: np.ndarray, direction: int = -1) -> dict:
    bs = bs[np.isfinite(bs)]
    if not len(bs) or not np.isfinite(est):
        return {"rho": None, "ci": [None, None], "se": None}
    lo, hi = np.percentile(bs, [2.5, 97.5])
    return {"rho": float(est), "ci": [float(lo), float(hi)], "se": float(np.std(bs, ddof=1)),
            "p_one_pred": float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1)),
            "p_two": float(min(1.0, 2 * min((np.sum(bs <= 0) + 1) / (len(bs) + 1), (np.sum(bs >= 0) + 1) / (len(bs) + 1)))),
            "n_boot": int(len(bs))}


def task_trait(args) -> dict:
    """One trait x one body: depth set (O1c, O1b, O3 own complete cases) and reach set (O2r_* complete cases, with
    the depth outcomes on the SAME rows for the paired differences)."""
    name, d, x, n_boot, seed, groups = args
    out = {"task": name, "x": x, "n_body": int(len(d))}
    B, C = design(d, groups=groups)
    xv = d[[x]].to_numpy(float)
    r1 = multi_boot(xv, d[DEPTH].to_numpy(float), B, C, n_boot, seed)
    r2 = multi_boot(xv, d[REACH + DEPTH].to_numpy(float), B, C, n_boot, seed + 1)
    res = {}
    for j, y in enumerate(DEPTH):
        res[y] = summ(r1["est"][0, j], r1["boot"][:, 0, j], direction=-1 if y == "O3" else 1)
        res[y]["n"] = r1["n"]
    for j, y in enumerate(REACH):
        res[y] = summ(r2["est"][0, j], r2["boot"][:, 0, j], direction=-1)
        res[y]["n"] = r2["n"]
    diffs = {}
    for a, b in [("O1c", "O2r_m50"), ("O1b", "O2r_m50"), ("O1c", "O2r_resid"), ("O3", "O2r_m50")]:
        ia, ib = (REACH + DEPTH).index(a), (REACH + DEPTH).index(b)
        e = r2["est"][0, ia] - r2["est"][0, ib]
        bs = r2["boot"][:, 0, ia] - r2["boot"][:, 0, ib]
        diffs[f"{a}-{b}"] = summ(e, bs, direction=1)
        diffs[f"{a}-{b}"]["n_common"] = r2["n"]
        diffs[f"{a}-{b}"]["psp_a_common"] = float(r2["est"][0, ia])
        diffs[f"{a}-{b}"]["psp_b_common"] = float(r2["est"][0, ib])
    out.update({"psp": res, "paired_diff": diffs})
    return out


def task_volume(args) -> dict:
    name, d, x, n_boot, seed = args
    xv, v3, v2 = d[x].to_numpy(float), d.V_t0p3.to_numpy(float), d.logV_t0p2.to_numpy(float)
    ok = np.isfinite(xv) & np.isfinite(v3) & np.isfinite(v2)
    xv, v3, v2 = xv[ok], v3[ok], v2[ok]
    n = len(xv)
    out = {"task": name, "x": x, "n": int(n)}
    if n < 30:
        return out
    rng = np.random.default_rng(seed)
    body_c = dummies(d.body.astype(str).to_numpy()[ok])
    Zc = np.hstack([v2[:, None], body_c])
    raw = float(stats.spearmanr(xv, v3)[0])
    ps = float(_resid_corr(rankdata(xv)[:, None], rankdata(v3)[:, None], rankdata(v2)[:, None], body_c)[0, 0])
    Bb, Cb = design(d[ok])
    ok5 = np.all(np.isfinite(Bb), 1)                               # B5 variant: complete B5 rows only
    x5, y5, Bb, Cb = xv[ok5], v3[ok5], Bb[ok5], Cb[ok5]
    n5 = len(x5)
    ps5 = float(psp_multi(x5[:, None], y5[:, None], Bb, Cb[:, Cb.std(0) > 0])[0, 0])
    br, bp, bp5 = np.empty(n_boot), np.empty(n_boot), np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        br[b] = stats.spearmanr(xv[i], v3[i])[0]
        k = body_c[i].std(0) > 0
        bp[b] = _resid_corr(rankdata(xv[i])[:, None], rankdata(v3[i])[:, None], rankdata(v2[i])[:, None],
                            body_c[i][:, k])[0, 0]
        j = rng.integers(0, n5, n5)
        Ci = Cb[j]
        bp5[b] = psp_multi(x5[j][:, None], y5[j][:, None], Bb[j], Ci[:, Ci.std(0) > 0])[0, 0]
    out["n_B5_variant"] = int(n5)
    out["B_raw_spearman_V_t0p3"] = summ(raw, br, direction=1)
    out["B_size_psp_V_t0p3_given_logV_t0p2"] = summ(ps, bp, direction=1)
    out["B_size_psp_V_t0p3_given_B5_dummies"] = summ(ps5, bp5, direction=1)
    return out


def run_tasks(tasks: list, fn, workers: int) -> list[dict]:
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex:
        return list(ex.map(fn, tasks))


def mde(se: float | None) -> float | None:
    return 2.8 * se if se else None


# ----------------------------------------------------------------------------- test B
def run_B(logger, quick: bool = False) -> dict:
    t = time.time()
    W = n_workers()
    nb = 100 if quick else N_BOOT_STATIC
    nb2 = 60 if quick else 500
    nbg = 100 if quick else 1000
    df = static_frame()
    df.to_parquet(DATA / "static_analysis_table.parquet", index=False)
    bodies = body_frames(df)
    tasks_t, tasks_v = [], []
    for bi, (bn, d) in enumerate(bodies.items()):
        tasks_t.append((f"{bn}|CONS_early_home", d, "CONS_early_home", nb, SEED + 10 * bi, True))
        tasks_v.append((f"{bn}|volume", d, "CONS_early_home", nb, SEED + 10 * bi + 5))
        for k, x in enumerate(TRAITS2):
            tasks_t.append((f"{bn}|{x}", d, x, nb2, SEED + 1000 + 10 * bi + k, True))
        tasks_v.append((f"{bn}|volume_all", d, "CONS_early_all", nb2, SEED + 2000 + 10 * bi))
    # per group within PRIMARY and within the 2015-17 cohort
    for bn in [PRIMARY, BODY_COHORT]:
        d = bodies[bn]
        for gi, g in enumerate(GROUPS5 + ["MATHDEC"]):
            dg = d[d.group5 == g]
            if len(dg) >= 40:
                tasks_t.append((f"{bn}|group={g}|CONS_early_home", dg, "CONS_early_home", nbg, SEED + 3000 + gi,
                                True))
    logger.info(f"B: {len(tasks_t)} trait tasks + {len(tasks_v)} volume tasks on {W} workers")
    rt = run_tasks(tasks_t, task_trait, W)
    rv = run_tasks(tasks_v, task_volume, W)
    res = {"label": SELECTION_LABEL, "resampling_unit": "concept", "n_boot_primary": nb, "n_boot_secondary": nb2,
           "n_boot_group": nbg, "covariates": "rank(B5) + onset-year dummies + 8-group dummies + body dummies "
           "(pooled) + window_flag (2015-17 cohort)", "primary_body": PRIMARY, "replication_body": BODY_COHORT,
           "EMB_note": "EMB_* = analogue (backbone PMI), not Cheng's word2vec measure",
           "trait": {r["task"]: r for r in rt}, "volume": {r["task"]: r for r in rv}}
    # DL over groups (primary trait) for each outcome and the paired diffs
    res["DL"] = {}
    for bn in [PRIMARY, BODY_COHORT]:
        res["DL"][bn] = {}
        keys = OUTS + ["O1c-O2r_m50", "O1c-O2r_resid"]
        for y in keys:
            bs, ss, per = [], [], {}
            for g in GROUPS5:
                r = res["trait"].get(f"{bn}|group={g}|CONS_early_home")
                if r is None:
                    continue
                v = r["psp"][y] if y in r["psp"] else r["paired_diff"][y]
                per[g] = {"rho": v["rho"], "ci": v["ci"], "n": v.get("n", v.get("n_common"))}
                bs.append(v["rho"] if v["rho"] is not None else np.nan)
                ss.append(v["se"] if v["se"] is not None else np.nan)
            dl = dersimonian_laird(bs, ss)
            dl["n_negative"] = int(sum(1 for b in bs if np.isfinite(b) and b < 0))
            dl["n_positive"] = int(sum(1 for b in bs if np.isfinite(b) and b > 0))
            dl["per_group"] = per
            m = res["trait"].get(f"{bn}|group=MATHDEC|CONS_early_home")
            if m is not None:
                dl["MATHDEC_report_only"] = (m["psp"][y] if y in m["psp"] else m["paired_diff"][y])["rho"]
            res["DL"][bn][y] = dl
    # cohort rungs R2 / R3 (EXP10 ladder)
    try:
        import ladder
        dc = bodies[BODY_COHORT].copy()
        res["cohort_rungs"] = {}
        for rung in ["R2", "R3"]:
            for y in ["O2r_m50", "O2r_resid", "O1c", "O3"]:
                r = ladder.psp_df(dc, "CONS_early_home", y, rung, 200 if quick else 1000, SEED + 4000,
                                  direction=1 if y == "O1c" else -1)
                r.pop("boot", None)
                res["cohort_rungs"][f"{rung}|{y}"] = r
    except (ImportError, KeyError, ValueError) as e:
        res["cohort_rungs"] = {"error": repr(e)[:300]}
    # cohort MDE for the P3 test
    c = res["trait"][f"{BODY_COHORT}|CONS_early_home"]["psp"]["O2r_m50"]
    res["cohort_MDE_O2r_m50"] = {"n": c.get("n"), "se": c.get("se"), "MDE_2.8SE": mde(c.get("se"))}
    jdump(res, RES / ("cheng_static_quick.json" if quick else "cheng_static.json"))
    p = res["trait"][f"{PRIMARY}|CONS_early_home"]
    logger.info(f"B primary: " + ", ".join(f"{y} {p['psp'][y]['rho']:+.3f} {np.round(p['psp'][y]['ci'], 3)}"
                                          for y in OUTS))
    logger.info(f"B primary diff O1c-O2r_m50 {p['paired_diff']['O1c-O2r_m50']}")
    logger.info(f"B volume primary {res['volume'][f'{PRIMARY}|volume']}")
    logger.info(f"S4 done in {(time.time() - t) / 60:.1f} min")
    return res


# ----------------------------------------------------------------------------- test D (Palla)
def cr(v: np.ndarray) -> np.ndarray:
    r = rankdata(v) / len(v)
    return r - r.mean()


def palla_fit(d: pd.DataFrame, y: str, i: np.ndarray | None = None) -> float:
    x, s, yy = d.CONS_early_home.to_numpy(float), d.logvol.to_numpy(float), d[y].to_numpy(float)
    other = d[["growth_c", "offhome_share", "entropy", "reach"]].to_numpy(float)
    _, C = design(d)
    if i is not None:
        x, s, yy, other, C = x[i], s[i], yy[i], other[i], C[i]
    C = C[:, C.std(0) > 0]
    rx, rs = cr(x), cr(s)
    Z = np.column_stack([np.ones(len(x)), rx, rs, rx * rs, rankdata(other, axis=0) / len(x), C])
    beta, *_ = np.linalg.lstsq(Z, cr(yy), rcond=None)
    return float(beta[3]), float(beta[1])


def task_palla(args) -> dict:
    name, d, y, n_boot, seed = args
    d = d[np.isfinite(d.CONS_early_home) & np.isfinite(d[y]) & d[B5].notna().all(1)].reset_index(drop=True)
    n = len(d)
    est, main = palla_fit(d, y)
    rng = np.random.default_rng(seed)
    bs = np.array([palla_fit(d, y, rng.integers(0, n, n)) for _ in range(n_boot)])
    out = {"task": name, "y": y, "n": n, "interaction": summ(est, bs[:, 0], direction=1),
           "main_rank_CONS": summ(main, bs[:, 1], direction=-1)}
    # psp by early-size tercile
    q = np.quantile(d.logvol, [1 / 3, 2 / 3])
    terc = np.digitize(d.logvol, q)
    out["by_size_tercile"] = {}
    for k, lab in enumerate(["small", "medium", "large"]):
        dk = d[terc == k]
        B, C = design(dk)
        r = multi_boot(dk[["CONS_early_home"]].to_numpy(float), dk[[y]].to_numpy(float), B, C, n_boot, seed + 7 + k)
        out["by_size_tercile"][lab] = {**summ(r["est"][0, 0], r["boot"][:, 0, 0]), "n": r["n"],
                                       "logvol_range": [float(dk.logvol.min()), float(dk.logvol.max())]}
    return out


def run_D(logger, quick: bool = False) -> dict:
    df = pd.read_parquet(DATA / "static_analysis_table.parquet")
    bodies = body_frames(df)
    nb = 100 if quick else 1000
    tasks = [(f"{bn}|{y}", bodies[bn], y, nb, SEED + 5000 + 10 * k + j)
             for k, bn in enumerate([PRIMARY, BODY_COHORT]) for j, y in enumerate(["O3", "O2r_m50", "O1c"])]
    rs = run_tasks(tasks, task_palla, n_workers())
    res = {"label": SELECTION_LABEL, "model": "OLS on centred ranks/n: rank O ~ rank CONS_early + rank logvol + "
           "product + rank(other B5) + onset-year/group/body dummies; concept bootstrap",
           "palla_prediction": "interaction on O3 (transience) > 0: stability helps small concepts survive, turnover "
           "helps large ones", "results": {r["task"]: r for r in rs}}
    jdump(res, RES / ("palla_quick.json" if quick else "palla.json"))
    for r in rs:
        logger.info(f"D {r['task']}: interaction {r['interaction']['rho']:+.4f} {r['interaction']['ci']}")
    return res


# ----------------------------------------------------------------------------- test E (coupling)
def task_coupling(args) -> dict:
    name, d, n_boot, seed = args
    B, C = design(d)
    X = d[["CONS_early_all", "CONS_early_home"]].to_numpy(float)
    out = {"task": name}
    for tag, ys in (("reach_set", ["O2r_m50", "O1c"]), ("full_set", ["O1c"])):
        r = multi_boot(X, d[ys].to_numpy(float), B, C, n_boot, seed)
        for j, y in enumerate(ys):
            e = r["est"][0, j] - r["est"][1, j]
            bs = r["boot"][:, 0, j] - r["boot"][:, 1, j]
            out[f"{tag}|{y}"] = {"n_common": r["n"], "psp_all": float(r["est"][0, j]),
                                 "psp_home": float(r["est"][1, j]), "diff_all_minus_home": summ(e, bs, direction=1)}
    return out


def run_E(logger, quick: bool = False) -> dict:
    df = pd.read_parquet(DATA / "static_analysis_table.parquet")
    bodies = body_frames(df)
    nb = 100 if quick else N_BOOT_STATIC
    tasks = [(bn, bodies[bn], nb, SEED + 6000 + k) for k, bn in enumerate([PRIMARY, BODY_COHORT, "DEV",
                                                                          "OLD_HELDOUT", "COHORT_2010_14"])]
    rs = run_tasks(tasks, task_coupling, n_workers())
    res = {"label": SELECTION_LABEL, "test": "paired concept bootstrap psp(CONS_early_all) - psp(CONS_early_home), "
           "common complete-case set", "results": {r["task"]: r for r in rs}}
    jdump(res, RES / ("coupling_quick.json" if quick else "coupling.json"))
    for r in rs:
        logger.info(f"E {r['task']}: " + "; ".join(f"{k} {v['diff_all_minus_home']['rho']:+.3f} "
                                                  f"{np.round(v['diff_all_minus_home']['ci'], 3)}"
                                                  for k, v in r.items() if k != "task"))
    return res
