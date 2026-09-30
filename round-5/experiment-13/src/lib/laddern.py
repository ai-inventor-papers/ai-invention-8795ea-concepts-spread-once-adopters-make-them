"""Frame-N ladder: EXP10 lib/ladder.py machinery (OPEN from frozen constants, psp with refit concept bootstrap, DL,
Holm) with the declared Frame-N rung substitutions:
  R0 = B5 (ranked) + onset-year dummies (reference 2008) [+ window_flag if the 2015 extension is present]
  R1 = R0 + CONTACT_REACH
  R2 = R1 + type_method / type_object / type_property (+ unlabelled) + generic   (no legacy level dummies)
  R3 = R2 + fp_logN, fp_nfields + fp_reemerge (not constant in Frame N)     (newborn/fp_wiki_pre dropped)
  R4 = R3 + label_coverage_early, home_coverage_early
  R5 = R4 + home-group FE (reference BGM+Med)
Constant columns are dropped (and reported by rung_columns_realised)."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd

from ladder import COMPONENTS, SIGNS, open_score, psp_boot2, strip  # noqa: F401  (EXP10 code, unchanged)
from rq1stats import dersimonian_laird, holm, psp_point  # noqa: F401

B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
RUNGS = ["R0", "R1", "R2", "R3", "R4", "R5"]
POOL_GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]
REF_YEAR = 2008


def year_dummies(df: pd.DataFrame) -> pd.DataFrame:
    ys = [y for y in sorted(df.t0.unique()) if y != REF_YEAR]
    return pd.DataFrame({f"t0_{y}": (df.t0 == y).astype(float) for y in ys}, index=df.index)


def type_dummies(df: pd.DataFrame) -> pd.DataFrame:
    t = df["type"].fillna("unlabelled")
    return pd.DataFrame({f"type_{c}": (t == c).astype(float) for c in ("method", "object", "property", "unlabelled")},
                        index=df.index)


def group_dummies(df: pd.DataFrame) -> pd.DataFrame:
    gs = [g for g in sorted(df.agroup.dropna().unique()) if g != "BGM+Med"]
    return pd.DataFrame({f"g_{g}": (df.agroup == g).astype(float) for g in gs}, index=df.index)


def rung_design(df: pd.DataFrame, rung: str, drop_type: bool = False, drop_group: bool = False,
                type_generic_only: bool = False) -> tuple[pd.DataFrame, pd.DataFrame]:
    r = RUNGS.index(rung)
    cont = list(B5)
    cat = [year_dummies(df)]
    if "window_flag" in df.columns and df.window_flag.nunique() > 1:
        cat.append(df[["window_flag"]].astype(float))
    if r >= 1:
        cont.append("CONTACT_REACH")
    if r >= 2:
        if not drop_type and not type_generic_only:
            cat.append(type_dummies(df))
        cat.append(df[["generic"]].astype(float))
    if r >= 3:
        cont += ["fp_logN", "fp_nfields"]
        if "fp_reemerge" in df.columns:          # D_fp_reemerge: not constant in Frame N (EXP10 R3 column)
            cat.append(df[["fp_reemerge"]].astype(float))
    if r >= 4:
        cont += ["label_coverage_early", "home_coverage_early"]
    if r >= 5 and not drop_group:
        cat.append(group_dummies(df))
    C = pd.concat(cat, axis=1) if cat else pd.DataFrame(index=df.index)
    C = C.loc[:, C.std() > 0] if len(C) > 1 else C
    Bc = df[cont]
    Bc = Bc.loc[:, Bc.std() > 0] if len(Bc) > 1 else Bc
    return Bc, C


def rung_columns_realised(df: pd.DataFrame, **kw) -> dict:
    out = {}
    for r in RUNGS:
        Bc, C = rung_design(df, r, **kw)
        out[r] = {"cont": list(Bc.columns), "cat": list(C.columns)}
    return out


def psp_df(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1,
           keep_boot: bool = False, **kw) -> dict:
    Bc, Cc = rung_design(df, rung, **kw)
    r = psp_boot2(df[xcol].to_numpy(float), df[ycol].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float),
                  n_boot, seed, direction)
    r.update({"x": xcol, "y": ycol, "rung": rung, "resampling_unit": "concept", "n_boot": n_boot})
    if not keep_boot:
        r.pop("boot", None)
    return r


def paired_diff(df: pd.DataFrame, xa: str, xb: str, ycol: str, rung: str, n_boot: int, seed: int) -> dict:
    """Paired concept bootstrap of psp(xa) - psp(xb) on the common sample (one-sided p for > 0)."""
    Bc, Cc = rung_design(df, rung)
    B, C = Bc.to_numpy(float), Cc.to_numpy(float)
    xa_, xb_, y = df[xa].to_numpy(float), df[xb].to_numpy(float), df[ycol].to_numpy(float)
    ok = np.isfinite(xa_) & np.isfinite(xb_) & np.isfinite(y) & np.all(np.isfinite(B), 1)
    xa_, xb_, y, B, C = xa_[ok], xb_[ok], y[ok], B[ok], C[ok]
    n = len(y)
    if n < 30:
        return {"n": int(n), "diff": math.nan, "ci": [math.nan, math.nan], "p_one": math.nan}
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
            "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
            "p_one": float((np.sum(bs <= 0) + 1) / (len(bs) + 1)), "resampling_unit": "concept", "n_boot": n_boot}


def per_group(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1) -> dict:
    rows = {}
    for gi, g in enumerate(POOL_GROUPS + ["MATHDEC"]):
        d = df[df.agroup == g]
        rows[g] = psp_df(d, xcol, ycol, rung, n_boot, seed + 101 * gi, direction, drop_group=True)
    est = [g for g in POOL_GROUPS if rows[g]["n"] >= 30 and np.isfinite(rows[g]["rho"])]
    b = [rows[g]["rho"] for g in est]
    se = [rows[g]["se"] for g in est]
    dl = dersimonian_laird(b, se) if len(est) >= 2 else {}
    logo = {}
    for g in est:
        o = [h for h in est if h != g]
        if len(o) >= 2:
            logo[g] = dersimonian_laird([rows[h]["rho"] for h in o], [rows[h]["se"] for h in o])
    pos = int(sum(1 for v in b if v > 0))
    return {"groups": rows, "estimable": est, "n_estimable": len(est), "DL": dl, "n_positive": pos,
            "leave_one_group_out": logo, "x": xcol, "y": ycol, "rung": rung}
