"""Estimation layer: a Newton conditional logit (Breslow ties, the EXP6 likelihood) with stratum weights (exact
concept-clustered refit bootstrap = multinomial concept weights), row offsets (crossed field bootstrap),
cluster / two-way-cluster sandwich SEs; rung definitions; LR tests; bootstraps; LPM; DL pooling.
Validated against lib/stats_core.CLogit (EXP6, verbatim copy) in tests/test_units.py."""
from __future__ import annotations

import math
import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np
import pandas as pd
from scipy import stats

import h2_exp6 as H2
from stats_core import dersimonian_laird, fe_ols

N_THREADS = int(os.environ.get("AII_THREADS", 8))


def tmap(fn, items) -> list:
    """deterministic thread map (numpy releases the GIL in the heavy kernels); order of results = order of items."""
    items = list(items)
    if N_THREADS <= 1 or len(items) < 4:
        return [fn(x) for x in items]
    with ThreadPoolExecutor(N_THREADS) as ex:
        return list(ex.map(fn, items))


BASE = ["a_phi_home", "b_log_size", "c_density", "e_gate_own"]
RIVALS_STRICT = ["D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3"]
RUNGS = {
    "R0_M0": BASE,
    "R1_rca": BASE + ["D_rca_1y"],
    "R2_vol": BASE + ["D_rca_1y", "D_vol"],
    "R3_ret": BASE + ["D_rca_1y", "D_vol", "d0_ret_rel"],
    "R4_lost": BASE + ["D_rca_1y", "D_vol", "d0_ret_rel", "d_lost"],
    "S_strict0": BASE + RIVALS_STRICT,
    "S_strict": BASE + RIVALS_STRICT + ["d0_ret_rel"],
    "S_pca0": BASE + ["RCA_PC1", "D_vol", "D_vol_w3"],
    "S_pca": BASE + ["RCA_PC1", "D_vol", "D_vol_w3", "d0_ret_rel"],
    "A1_lost": BASE + ["d_lost"],
    "EXP6_M1": BASE + ["d0_ret_rel"],
    "EXP6_M2lost": BASE + ["d_lost_gate"],
}
LADDER = [("R1_rca", "R0_M0"), ("R2_vol", "R1_rca"), ("R3_ret", "R2_vol"), ("R4_lost", "R3_ret"),
          ("S_strict", "S_strict0"), ("S_pca", "S_pca0"), ("A1_lost", "R0_M0"), ("EXP6_M1", "R0_M0"), ("EXP6_M2lost", "R0_M0")]
STD_COLS = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate", "d_lost_gate", "d_lost",
            "D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3", "D_cum", "d_lost_short", "d_lost_long"]
D0_SCALE_COLS = ["d_ret_a2", "d_ret_a3", "d_ret_a4p", "d_R_m", "d_N_m", "d_R_mf", "d_N_mf"]  # common scale = SD of d0_ret_rel


class FastCLogit:
    """ll = sum_s w_s [ sum_{e in s} eta_e - nev_s log sum_{i in s} exp(eta_i) ],  eta = X b + offset.
    Only informative strata (>= 1 event and >= 1 non-event) are kept."""

    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, offset: np.ndarray | None = None,
                 clusters: dict[str, np.ndarray] | None = None):
        o = np.argsort(strata, kind="stable")
        s = strata[o]
        _, starts, counts = np.unique(s, return_index=True, return_counts=True)
        yy = y[o].astype(np.float64)
        nev = np.add.reduceat(yy, starts)
        keep_s = (nev > 0) & (nev < counts)
        rows = np.repeat(keep_s, counts)
        self.idx = o[rows]                      # original row index of every internal row
        self.X = np.ascontiguousarray(X[self.idx], dtype=np.float64)
        self.y = yy[rows]
        self.off = None if offset is None else offset[self.idx].astype(np.float64)
        s = s[rows]
        self.sid, self.starts, self.counts = np.unique(s, return_index=True, return_counts=True)
        self.nev = np.add.reduceat(self.y, self.starts) if len(self.starts) else np.zeros(0)
        self.row_s = np.repeat(np.arange(len(self.starts)), self.counts)
        self.clusters = {k: v[self.idx] for k, v in (clusters or {}).items()}
        self.w = np.ones(len(self.starts))

    @property
    def n_strata(self) -> int:
        return int(len(self.starts))

    def set_col(self, j: int, values: np.ndarray) -> None:
        self.X[:, j] = values[self.idx]

    def _parts(self, b: np.ndarray, w: np.ndarray):
        eta = self.X @ b
        if self.off is not None:
            eta = eta + self.off
        m = np.maximum.reduceat(eta, self.starts)
        e = np.exp(eta - m[self.row_s])
        S = np.add.reduceat(e, self.starts)
        p = e / S[self.row_s]
        lse = np.log(S) + m
        ll = float((w[self.row_s] * self.y * eta).sum() - (w * self.nev * lse).sum())
        return eta, p, ll

    def fit(self, b0: np.ndarray | None = None, w: np.ndarray | None = None, ridge: float = 0.0, tol: float = 1e-9,
            maxit: int = 60, want_cov: bool = True) -> dict:
        k = self.X.shape[1]
        if self.n_strata == 0:
            return {"coef": np.full(k, np.nan), "se": np.full(k, np.nan), "ll": np.nan, "converged": False,
                    "n_strata": 0, "n_events": 0, "n_rows": 0, "max_grad": np.nan}
        w = self.w if w is None else w
        b = np.zeros(k) if b0 is None else np.array(b0, float)
        _, p, ll = self._parts(b, w)
        ll -= 0.5 * ridge * b @ b
        conv = False
        for it in range(maxit):
            wr = w[self.row_s]
            Ex = np.add.reduceat(p[:, None] * self.X, self.starts)
            g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b
            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]
            B = Ex * np.sqrt(w * self.nev)[:, None]
            H = A.T @ A - B.T @ B + ridge * np.eye(k)
            try:
                step = np.linalg.solve(H, g)
            except np.linalg.LinAlgError:
                step = np.linalg.lstsq(H, g, rcond=None)[0]
            t = 1.0
            for _ in range(30):
                bn = b + t * step
                _, pn, lln = self._parts(bn, w)
                lln -= 0.5 * ridge * bn @ bn
                if lln >= ll - 1e-10:
                    break
                t *= 0.5
            b, p, dll = bn, pn, lln - ll
            ll = lln
            if np.abs(t * step).max() < tol or abs(dll) < 1e-12:
                conv = True
                break
        wr = w[self.row_s]
        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)
        g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b
        out = {"coef": b, "ll": ll, "converged": bool(conv and np.abs(g).max() < 1e-4), "max_grad": float(np.abs(g).max()),
               "n_strata": self.n_strata, "n_events": int(self.y.sum()), "n_rows": int(len(self.y)), "iters": it + 1}
        if want_cov:
            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]
            B = Ex * np.sqrt(w * self.nev)[:, None]
            H = A.T @ A - B.T @ B + ridge * np.eye(k)
            try:
                Hi = np.linalg.inv(H)
                out["se"] = np.sqrt(np.clip(np.diag(Hi), 0, None))
            except np.linalg.LinAlgError:
                Hi = np.linalg.pinv(H)
                out["se"] = np.full(k, np.nan)
            out["_Hi"] = Hi
            out["_p"] = p
        return out

    def row_scores(self, res: dict) -> np.ndarray:
        """per-row score contributions u_i = (y_i - nev_s p_i) x_i (sum within stratum = stratum score)."""
        return (self.y - self.nev[self.row_s] * res["_p"])[:, None] * self.X

    def cluster_se(self, res: dict, by: str | list[str]) -> np.ndarray:
        """CRV1 sandwich; `by` a cluster name, or two names for Cameron-Gelbach-Miller two-way clustering."""
        U = self.row_scores(res)
        Hi = res["_Hi"]

        def meat(key: np.ndarray) -> tuple[np.ndarray, int]:
            _, inv = np.unique(key, return_inverse=True)
            G = inv.max() + 1
            sc = np.zeros((G, U.shape[1]))
            np.add.at(sc, inv, U)
            return (G / max(G - 1, 1)) * (sc.T @ sc), G
        if isinstance(by, str):
            M, _ = meat(self.clusters[by])
        else:
            a, b = (self.clusters[x] for x in by)
            Ma, _ = meat(a); Mb, _ = meat(b)
            Mab, _ = meat(a.astype(np.int64) * 1000 + b.astype(np.int64))
            M = Ma + Mb - Mab
        V = Hi @ M @ Hi
        return np.sqrt(np.clip(np.diag(V), 0, None))


# ----------------------------------------------------------------------------- helpers
def standardise(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    out = df.copy()
    for c, v in spec.items():
        if c in out and "mean" in v:
            out[c] = (df[c] - v["mean"]) / (v["sd"] if v["sd"] > 0 else 1.0)
    if "RCA_PC1" in spec and all(c in out for c in spec["RCA_PC1"]["cols"]):
        p = spec["RCA_PC1"]
        out["RCA_PC1"] = (out[p["cols"]].to_numpy() @ np.array(p["loadings"]) - p["pc_mean"]) / p["pc_sd"]
    return out


def make_spec(df: pd.DataFrame, cols: list[str] = STD_COLS, base: dict | None = None) -> dict:
    """mean/SD per column; the dose and matched-contrast columns use mean 0 and the SD of d0_ret_rel (common scale)."""
    spec = dict(base or {})
    for c in cols:
        if c not in spec and c in df:
            sd = float(df[c].std())
            spec[c] = {"mean": float(df[c].mean()), "sd": sd if sd > 0 else 1.0}
    for c in D0_SCALE_COLS:
        if c in df:
            spec[c] = {"mean": 0.0, "sd": spec["d0_ret_rel"]["sd"]}
    # PCA-combined RCA factor (fallback F6 for collinear RCA variants): first PC of the four standardised D_rca
    rc = ["D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers"]
    if "RCA_PC1" not in spec and all(c in df for c in rc):
        Z = np.column_stack([(df[c] - spec[c]["mean"]) / spec[c]["sd"] for c in rc])
        w, V = np.linalg.eigh(np.cov(Z, rowvar=False))
        v = V[:, -1] * np.sign(V[:, -1].sum())
        pc = Z @ v
        spec["RCA_PC1"] = {"loadings": v.tolist(), "cols": rc, "explained": float(w[-1] / w.sum()),
                           "pc_mean": float(pc.mean()), "pc_sd": float(pc.std())}
    return spec


def model(df: pd.DataFrame, cols: list[str], offset: np.ndarray | None = None) -> FastCLogit:
    return FastCLogit(df[cols].to_numpy(np.float64), df.entered.to_numpy(), df.stratum.to_numpy(), offset=offset,
                      clusters={"concept": df.cidx.to_numpy(), "field": df.field.to_numpy()})


def summarise(m: FastCLogit, r: dict, cols: list[str], cluster: bool = True) -> dict:
    out = {"coef": dict(zip(cols, map(float, r["coef"]))), "se_model": dict(zip(cols, map(float, r["se"]))),
           "ll": float(r["ll"]), "n_strata": r["n_strata"], "n_events": r["n_events"], "n_rows": r["n_rows"],
           "converged": r["converged"], "max_grad": r["max_grad"]}
    if cluster and r["n_strata"] > 0:
        out["se_concept"] = dict(zip(cols, map(float, m.cluster_se(r, "concept"))))
    return out


def lr(big: dict, small: dict, df_: int = 1) -> dict:
    x = 2 * (big["ll"] - small["ll"])
    return {"LR": float(x), "df": df_, "p": float(stats.chi2.sf(max(x, 0), df_))}


def fit_ladder(df: pd.DataFrame, rungs: list[str] | None = None, auc: bool = True, two_way: list[str] | None = None) -> dict:
    """fit every rung on the same rows; LR along LADDER; within-stratum AUC of each linear predictor."""
    rungs = rungs or list(RUNGS)
    fits, res = {}, {"models": {}, "LR": {}, "auc_within": {}}
    for rn in rungs:
        cols = RUNGS[rn]
        m = model(df, cols)
        r = m.fit()
        fits[rn] = r
        res["models"][rn] = summarise(m, r, cols)
        if two_way and rn in two_way:
            res["models"][rn]["se_two_way_concept_field"] = dict(zip(cols, map(float, m.cluster_se(r, ["concept", "field"]))))
        if auc:
            sc = df[cols].to_numpy() @ r["coef"]
            res["auc_within"][rn] = float(H2.within_auc(df, sc).mean())
    for big, small in LADDER:
        if big in fits and small in fits:
            res["LR"][f"{big}_vs_{small}"] = lr(fits[big], fits[small], len(RUNGS[big]) - len(RUNGS[small]))
    res["n"] = {"rows": int(len(df)), "strata": int(df.stratum.nunique()), "concepts": int(df.cidx.nunique()),
                "events": int(df.entered.sum()), "informative_strata": fits[rungs[0]]["n_strata"],
                "informative_rows": fits[rungs[0]]["n_rows"]}
    res["_fits"] = fits
    return res


def concept_weights(cid_of_stratum: np.ndarray, rng, n_boot: int) -> np.ndarray:
    """multinomial concept-resampling counts mapped to strata -> [n_boot, n_strata]. A concept drawn m times
    contributes m identical independent copies of its strata, i.e. weight m (exact equivalence with the
    duplicate-and-relabel refit bootstrap of h2_exp6.boot_coef)."""
    u, inv = np.unique(cid_of_stratum, return_inverse=True)
    W = np.empty((n_boot, len(cid_of_stratum)))
    for b in range(n_boot):
        cnt = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)
        W[b] = cnt[inv]
    return W


def boot_refit(df: pd.DataFrame, cols: list[str], targets: list[str], n_boot: int, rng, small_cols: list[str] | None = None,
               W: np.ndarray | None = None) -> dict:
    """concept-clustered refit bootstrap (weights), warm-started at the full-sample estimate."""
    m = model(df, cols)
    r0 = m.fit(want_cov=False)
    ms = model(df, small_cols) if small_cols else None
    rs0 = ms.fit(want_cov=False) if ms else None
    if W is None:
        W = concept_weights(m.sid // 100, rng, n_boot)
    def one(w):
        r = m.fit(b0=r0["coef"], w=w, want_cov=False)
        lrv = 2 * (r["ll"] - ms.fit(b0=rs0["coef"], w=w, want_cov=False)["ll"]) if ms is not None else None
        return r["coef"], lrv
    got = tmap(one, W)
    B = np.array([g[0] for g in got])
    L = [g[1] for g in got if g[1] is not None]
    out = {"resampling_unit": "concept", "n_boot": int(len(W))}
    for tg in targets:
        j = cols.index(tg)
        out[tg] = {"est": float(r0["coef"][j]), "ci": [float(np.nanpercentile(B[:, j], 2.5)), float(np.nanpercentile(B[:, j], 97.5))],
                   "se_boot": float(np.nanstd(B[:, j])), "p_one_sided_le0": float((1 + (B[:, j] <= 0).sum()) / (1 + len(B)))}
    if L:
        L = np.array(L)
        out["LR_boot_q"] = [float(x) for x in np.percentile(L, [5, 25, 50, 75, 95])]
    out["_B"] = B
    return out


def contrast_boot(df: pd.DataFrame, cols: list[str], a: str, b: str, n_boot: int, rng, sign: int = 1) -> dict:
    """bootstrap CI of coef[a] - coef[b] (concept refit)."""
    bt = boot_refit(df, cols, [a, b], n_boot, rng)
    d = bt["_B"][:, cols.index(a)] - bt["_B"][:, cols.index(b)]
    est = bt[a]["est"] - bt[b]["est"]
    return {"resampling_unit": "concept", "n_boot": n_boot, "est": float(est),
            "ci": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "p_one_sided": float((1 + (sign * d <= 0).sum()) / (1 + len(d))), a: bt[a], b: bt[b]}


def crossed_boot(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng) -> dict:
    """Owen pigeonhole: concept weights u_c ~ Poisson(1) on stratum log-lik; target-field weights v_k ~ Poisson(1) as
    offset log(v_k) on each alternative (v_k = 0 removes the alternative; strata left uninformative drop out)."""
    m0 = model(df, cols)
    b0 = m0.fit(want_cov=False)["coef"]
    fk = df.field.to_numpy() - 11
    cid = df.cidx.to_numpy()
    uc, cinv = np.unique(cid, return_inverse=True)
    draws = [(rng.poisson(1.0, 26).astype(float), rng.poisson(1.0, len(uc)).astype(float)) for _ in range(n_boot)]
    Xall, yall, sall = df[cols].to_numpy(np.float64), df.entered.to_numpy(), df.stratum.to_numpy()

    def one(vu):
        v, u = vu
        keep = (v[fk] > 0) & (u[cinv] > 0)
        m = FastCLogit(Xall[keep], yall[keep], sall[keep], offset=np.log(v[fk][keep]))
        if m.n_strata == 0:
            return np.nan
        ws = u[np.searchsorted(uc, m.sid // 100)]
        return m.fit(b0=b0, w=ws, want_cov=False)["coef"][cols.index(target)]
    B = np.array(tmap(one, draws))
    B = B[np.isfinite(B)]
    return {"resampling_unit": "concept x target field (Owen pigeonhole, Poisson(1) weights)", "n_boot": int(len(B)),
            "ci": [float(np.percentile(B, 2.5)), float(np.percentile(B, 97.5))], "se_boot": float(B.std())}


def lpm(df: pd.DataFrame, cols: list[str]) -> dict:
    """linear probability model with concept-year (stratum) FE, concept-clustered CRV1 SEs (econ-geo comparability)."""
    r = fe_ols(df.entered.to_numpy(float), df[cols].to_numpy(float), [df.stratum.to_numpy()], df.cidx.to_numpy(), cols)
    r.pop("V", None); r.pop("_b", None)
    r["resampling_unit"] = "concept (CRV1 clusters)"
    r["base_rate"] = float(df.entered.mean())
    return r


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = float(run)
    return out


def dl(b: list[float], se: list[float]) -> dict:
    return dersimonian_laird(np.array(b), np.array(se))


def informative(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("stratum").entered.agg(["sum", "size"])
    ok = g.index[(g["sum"] > 0) & (g["sum"] < g["size"])]
    return df[df.stratum.isin(ok)]
