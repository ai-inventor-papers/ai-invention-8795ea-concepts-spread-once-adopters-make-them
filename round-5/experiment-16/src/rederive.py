#!/usr/bin/env python3
"""Independent re-derivation (separate code path: own design matrices, scipy rankdata + numpy lstsq residualisation,
own z-scoring and Spearman) of (a) the P1-P3 psp point estimates and (b) the pooled split-half SB of NOVCHURN_raw.
Tolerances: psp <= 1e-9, SB <= 1e-6. -> results/rederive.json"""
from __future__ import annotations

import json
import math
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from common import DATA, DATA_IN, RES, jdump, setup_logger

logger = setup_logger("rederive")


def my_design(df: pd.DataFrame, pooled: bool) -> tuple[np.ndarray, np.ndarray]:
    """Rung R2 rebuilt from scratch: continuous B5 + CONTACT_REACH; dummies t0 (drop first), window_flag (if
    varying), type (method/object/property/unlabelled), generic, level 3/4/5, body (pooled, drop first)."""
    cont = df[["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH"]].to_numpy(float)
    cols = []
    for y in sorted(df.t0.unique())[1:]:
        cols.append((df.t0 == y).to_numpy(float))
    if df.window_flag.nunique() > 1:
        cols.append(df.window_flag.to_numpy(float))
    t = df["type"].fillna("unlabelled")
    for c in ("method", "object", "property", "unlabelled"):
        cols.append((t == c).to_numpy(float))
    cols.append(df.generic.to_numpy(float))
    for l in (3, 4, 5):
        cols.append((df.level == l).to_numpy(float))
    if pooled:
        for b in sorted(df.body.unique())[1:]:
            cols.append((df.body == b).to_numpy(float))
    C = np.column_stack(cols)
    C = C[:, C.std(0) > 0]
    return cont, C


def my_psp(x, y, cont, C) -> tuple[float, int]:
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(cont), 1) & np.all(np.isfinite(C), 1)
    x, y, cont, C = x[ok], y[ok], cont[ok], C[ok]
    Z = np.column_stack([np.ones(len(x))] + [rankdata(cont[:, j]) for j in range(cont.shape[1])] + [C])
    res = []
    for v in (rankdata(x), rankdata(y)):
        beta = np.linalg.lstsq(Z, v, rcond=None)[0]
        res.append(v - Z @ beta)
    return float(np.corrcoef(res[0], res[1])[0, 1]), int(ok.sum())


def main() -> None:
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet")
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet")
    keep = ["ci", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "t0", "type", "generic",
            "level", "O2r_m50"]
    e = cv[cv.frame == "exp5"].drop(columns=["t0"]).merge(fe[keep], on="ci")
    e["window_flag"] = 0
    c = cv[cv.frame == "cohort"].drop(columns=["t0"]).merge(ac[keep + ["window_flag"]], on="ci")
    P = pd.concat([e, c], ignore_index=True)
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    cells, pairs = V["cells"]["psp"], V["cells"]["paired"]
    out = {"psp": {}, "tolerance_psp": 1e-9, "tolerance_SB": 1e-6}
    checks = [("COH1517", "NOVCHURN_exc"), ("COH1517", "NOVCHURN_raw"), ("OLDHO", "NOVCHURN_exc"),
              ("OLDHO", "NOVCHURN_raw"), ("POOLED", "z_pers_cfg"), ("POOLED", "edge_persistence__raw"),
              ("POOLED", "NOVCHURN_raw"), ("POOLED", "NOVCHURN_exc")]
    worst = 0.0
    for body, x in checks:
        d = P if body == "POOLED" else P[P.body == body]
        cont, C = my_design(d, body == "POOLED")
        r, n = my_psp(d[x].to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        ref = cells[f"{body}|{x}|O2r_m50|R2"]
        dd = abs(r - ref["rho"])
        worst = max(worst, dd)
        out["psp"][f"{body}|{x}|R2"] = {"rederived": r, "pipeline": ref["rho"], "abs_diff": dd, "n": n,
                                        "n_pipeline": ref["n"]}
    for body in ("COH1517", "OLDHO"):
        d = P[P.body == body]
        m = np.isfinite(d.NOVCHURN_exc) & np.isfinite(d.NOVCHURN_raw)
        d = d[m]
        cont, C = my_design(d, False)
        a, n = my_psp(d.NOVCHURN_exc.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        b, _ = my_psp(d.NOVCHURN_raw.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        ref = pairs[f"{body}|NOVCHURN_exc|NOVCHURN_raw|O2r_m50|R2"]
        dd = max(abs(a - ref["a"]), abs(b - ref["b"]))
        worst = max(worst, dd)
        out["psp"][f"{body}|P1_same_sample_ratio"] = {"rederived_ratio": a / b, "pipeline_ratio": ref["ratio"],
                                                      "abs_diff_components": dd, "n": n}
    x = cv.NOVCHURN_exc.to_numpy(float)
    ok = np.isfinite(x)
    r3 = float(spearmanr(x[ok], np.log(cv.n_home_early.to_numpy(float))[ok])[0])
    out["P3"] = {"rederived": r3, "pipeline": V["predictions"]["P3"]["spearman_NOVCHURN_exc_log_n_all"],
                 "abs_diff": abs(r3 - V["predictions"]["P3"]["spearman_NOVCHURN_exc_log_n_all"])}
    worst = max(worst, out["P3"]["abs_diff"])
    # pooled SB of NOVCHURN_raw from the S2 half arrays (own z-scoring)
    spec = json.loads((RES / "frozen_spec.json").read_text())
    K = spec["exp10_open_constants_home"]
    pos = {(f, int(ci)): i for i, (f, ci) in enumerate(zip(cv.frame, cv.ci))}
    A = np.full((100, len(cv)), np.nan)
    Bh = np.full((100, len(cv)), np.nan)
    for p in sorted((DATA / "s2_parts_full").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, ex in zip(z["rows"], z["extras"]):
            if not ex:
                continue
            i = pos[(r["frame"], int(r["ci"]))]
            for h, M in (("A", A), ("B", Bh)):
                nov = ex["half_raw"][h][:, 3].astype(float)
                ep = ex["half_raw"][h][:, 5].astype(float)
                zn = (np.clip(nov, K["NOV_res"]["lo"], K["NOV_res"]["hi"]) - K["NOV_res"]["mu"]) / K["NOV_res"]["sd"]
                ze = -(np.clip(ep, K["edge_persistence"]["lo"], K["edge_persistence"]["hi"]) -
                       K["edge_persistence"]["mu"]) / K["edge_persistence"]["sd"]
                M[:, i] = np.where(np.isfinite(zn) & np.isfinite(ze), (zn + ze) / 2, np.nan)
    rs = []
    for s in range(100):
        ok = np.isfinite(A[s]) & np.isfinite(Bh[s])
        rs.append(spearmanr(A[s, ok], Bh[s, ok])[0])
    rr = math.tanh(np.mean(np.arctanh(rs)))
    sb = 2 * rr / (1 + rr)
    rel = json.loads((RES / "reliability.json").read_text())
    ref = rel["variants"]["NOVCHURN_raw"]["pooled"]["SB"]
    out["SB_NOVCHURN_raw_pooled"] = {"rederived": sb, "pipeline": ref, "abs_diff": abs(sb - ref)}
    out["pass"] = bool(worst <= 1e-9 and abs(sb - ref) <= 1e-6)
    jdump(out, RES / "rederive.json")
    logger.info(f"rederive pass {out['pass']}; worst psp diff {worst:.2e}; SB diff {abs(sb-ref):.2e}")


if __name__ == "__main__":
    main()
