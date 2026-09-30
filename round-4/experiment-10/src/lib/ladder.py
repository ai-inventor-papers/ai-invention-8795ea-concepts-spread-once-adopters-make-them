"""Ladder machinery: OPEN construction from frozen constants, rung design matrices, partial Spearman with a refit
concept bootstrap (EXP8 rq1stats.psp_point), DL pooling over groups, one-sided bootstrap p, Holm.

psp = Pearson(resid(rank x | ranks of continuous covariates + dummies), resid(rank y | same)); the residualisation is
refitted in every bootstrap draw (ranks recomputed within the draw). Resampling unit: concept."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

from rq1stats import dersimonian_laird, holm, psp_point

COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
SIGNS = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
         "edge_persistence": -1}
BUILDS = ["home", "all", "sizematch"]
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
FOOTPRINT = ["fp_logN", "fp_nfields"]
FOOTPRINT_BIN = ["fp_reemerge", "fp_wiki_pre", "newborn"]
COVERAGE = ["label_coverage_early", "home_coverage_early"]
ANALYSIS_GROUP = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med", "PHYS": "PHYS",
                  "LIFEENV": "LIFEENV", "SOC": "SOC", "MATHDEC": "MATHDEC"}
POOL_GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]
RUNGS = ["R0", "R1", "R2", "R3", "R4", "R5"]
MIN_HOME_PAPERS = 10


# ----------------------------------------------------------------------------- OPEN
def fit_open_constants(df: pd.DataFrame, build: str) -> dict:
    """Winsor bounds (0.5 / 99.5 pct) and mean / sd of the winsorised component, on the frame given (EXP5)."""
    out = {}
    for k in COMPONENTS:
        v = df[f"{k}__{build}"].to_numpy(float)
        v = v[np.isfinite(v)]
        lo, hi = np.percentile(v, [0.5, 99.5])
        w = np.clip(v, lo, hi)
        out[k] = {"lo": float(lo), "hi": float(hi), "mu": float(w.mean()), "sd": float(w.std()) or 1.0,
                  "sign": SIGNS[k], "n": int(len(v))}
    return out


def open_score(df: pd.DataFrame, build: str, const: dict, min_home: int = MIN_HOME_PAPERS,
               min_comp: int = 4) -> tuple[np.ndarray, pd.DataFrame]:
    """OPEN_b (NaN unless >= min_comp of 6 z-scores finite; HOME/SIZEMATCH NaN if < min_home home papers t0..t0+2)."""
    Z = pd.DataFrame(index=df.index)
    for k in COMPONENTS:
        c = const[k]
        v = df[f"{k}__{build}"].to_numpy(float)
        Z[k] = c["sign"] * (np.clip(v, c["lo"], c["hi"]) - c["mu"]) / c["sd"]
    nfin = np.isfinite(Z.to_numpy()).sum(1)
    with np.errstate(invalid="ignore"):
        o = np.nanmean(np.where(np.isfinite(Z.to_numpy()), Z.to_numpy(), np.nan), axis=1)
    o[nfin < min_comp] = np.nan
    if build in ("home", "sizematch"):
        o[df["n_home_early"].to_numpy() < min_home] = np.nan
    return o, Z


# ----------------------------------------------------------------------------- rungs
def type_dummies(df: pd.DataFrame) -> pd.DataFrame:
    t = df["type"].fillna("unlabelled")
    return pd.DataFrame({f"type_{c}": (t == c).astype(float) for c in ("method", "object", "property", "unlabelled")},
                        index=df.index)


def level_dummies(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({f"level_{l}": (df.level == l).astype(float) for l in (3, 4, 5)}, index=df.index)


def year_dummies(df: pd.DataFrame) -> pd.DataFrame:
    ys = sorted(df.t0.unique())[1:]
    return pd.DataFrame({f"t0_{y}": (df.t0 == y).astype(float) for y in ys}, index=df.index)


def group_dummies(df: pd.DataFrame) -> pd.DataFrame:
    gs = sorted(df.agroup.unique())[1:]
    return pd.DataFrame({f"g_{g}": (df.agroup == g).astype(float) for g in gs}, index=df.index)


def rung_design(df: pd.DataFrame, rung: str, drop_type: bool = False, drop_group: bool = False
                ) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(continuous covariates -> ranked, categorical dummies -> raw) for rung R0..R5."""
    r = RUNGS.index(rung)
    cont = list(B5)
    cat = [year_dummies(df)]
    if "window_flag" in df.columns and df.window_flag.nunique() > 1:
        cat.append(df[["window_flag"]].astype(float))
    if r >= 1:
        cont.append("CONTACT_REACH")
    if r >= 2:
        if not drop_type:
            cat.append(type_dummies(df))
        cat.append(df[["generic"]].astype(float))
        cat.append(level_dummies(df))
    if r >= 3:
        cont += FOOTPRINT
        cat.append(df[FOOTPRINT_BIN].astype(float))
    if r >= 4:
        cont += COVERAGE
    if r >= 5 and not drop_group:
        cat.append(group_dummies(df))
    C = pd.concat(cat, axis=1) if cat else pd.DataFrame(index=df.index)
    C = C.loc[:, C.std() > 0] if len(C) > 1 else C
    return df[cont], C


def rung_columns() -> list[str]:
    return B5 + ["CONTACT_REACH", "generic", "level", "type"] + FOOTPRINT + FOOTPRINT_BIN + COVERAGE + ["agroup", "t0"]


# ----------------------------------------------------------------------------- estimation
def psp_boot2(x: np.ndarray, y: np.ndarray, B: np.ndarray, C: np.ndarray, n_boot: int, seed: int,
              direction: int = 1, idx_boot: np.ndarray | None = None) -> dict:
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
    x, y, B, C = x[ok], y[ok], B[ok], C[ok]
    n = len(x)
    if n < 30 or np.unique(x).size < 3:
        return {"n": int(n), "rho": math.nan, "ci": [math.nan, math.nan], "se": math.nan, "p_one": math.nan,
                "p_two": math.nan, "boot": np.array([])}
    est = psp_point(x, y, B, C)
    rng = np.random.default_rng(seed)
    bs = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0 if Ci.shape[1] else np.zeros(0, bool)
        bs[b] = psp_point(x[i], y[i], B[i], Ci[:, keep])
    bs = bs[np.isfinite(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    p_one = float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1))
    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))
    se_z = float(np.std(z, ddof=1))
    ze = math.atanh(max(min(est, 0.999999), -0.999999))
    return {"n": int(n), "rho": float(est), "ci": [float(lo), float(hi)], "se": float(np.std(bs, ddof=1)),
            "p_one": p_one, "p_two": float(2 * stats.norm.sf(abs(ze / se_z))) if se_z > 0 else math.nan,
            "boot": bs}


def psp_df(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1,
           drop_type: bool = False, drop_group: bool = False) -> dict:
    Bc, Cc = rung_design(df, rung, drop_type, drop_group)
    r = psp_boot2(df[xcol].to_numpy(float), df[ycol].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float),
                  n_boot, seed, direction)
    r.update({"x": xcol, "y": ycol, "rung": rung, "resampling_unit": "concept", "n_boot": n_boot})
    return r


def paired_diff(df: pd.DataFrame, xa: str, xb: str, ycol: str, rung: str, n_boot: int, seed: int) -> dict:
    """Paired concept bootstrap of psp(xa) - psp(xb) on the common sample."""
    Bc, Cc = rung_design(df, rung)
    B, C = Bc.to_numpy(float), Cc.to_numpy(float)
    xa_, xb_, y = df[xa].to_numpy(float), df[xb].to_numpy(float), df[ycol].to_numpy(float)
    ok = np.isfinite(xa_) & np.isfinite(xb_) & np.isfinite(y) & np.all(np.isfinite(B), 1)
    xa_, xb_, y, B, C = xa_[ok], xb_[ok], y[ok], B[ok], C[ok]
    n = len(y)
    if n < 30:
        return {"n": int(n), "diff": math.nan, "ci": [math.nan, math.nan]}
    est = psp_point(xa_, y, B, C) - psp_point(xb_, y, B, C)
    rng = np.random.default_rng(seed)
    bs = []
    for _ in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0
        bs.append(psp_point(xa_[i], y[i], B[i], Ci[:, keep]) - psp_point(xb_[i], y[i], B[i], Ci[:, keep]))
    bs = np.asarray(bs)
    bs = bs[np.isfinite(bs)]
    return {"n": int(n), "a": xa, "b": xb, "y": ycol, "rung": rung, "diff": float(est),
            "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], "resampling_unit": "concept"}


def per_group(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1) -> dict:
    rows = {}
    for gi, g in enumerate(POOL_GROUPS + ["MATHDEC"]):
        d = df[df.agroup == g]
        r = psp_df(d, xcol, ycol, rung, n_boot, seed + 101 * gi, direction, drop_group=True)
        r.pop("boot", None)
        rows[g] = r
    b = [rows[g]["rho"] for g in POOL_GROUPS]
    se = [rows[g]["se"] for g in POOL_GROUPS]
    dl = dersimonian_laird(b, se)
    pos = int(sum(1 for v in b if np.isfinite(v) and v > 0))
    return {"groups": rows, "DL": dl, "n_positive_of_5": pos, "x": xcol, "y": ycol, "rung": rung}


def strip(d):
    if isinstance(d, dict):
        return {k: strip(v) for k, v in d.items() if k != "boot"}
    if isinstance(d, list):
        return [strip(v) for v in d]
    return d


__all__ = ["COMPONENTS", "SIGNS", "BUILDS", "RUNGS", "B5", "ANALYSIS_GROUP", "POOL_GROUPS", "fit_open_constants",
           "open_score", "rung_design", "psp_boot2", "psp_df", "paired_diff", "per_group", "holm", "strip",
           "dersimonian_laird"]
