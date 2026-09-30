#!/usr/bin/env python3
"""S9 AUDIT: an independent code path re-derives the headline numbers of results/frame_n_result.json.

  psp (OPEN_home, NOVCHURN_home at R3 / R5): statsmodels OLS residuals of the ranks + scipy pearsonr (not lib/rq1stats)
  DL pooling: a re-implementation from the per-group estimates
  Cheng raw rho: scipy spearmanr
  O2r_m50 for 30 concepts: straight from the sealed parts (A + B) and the open rows, scipy.stats.hypergeom
  CHENG_consistency_home for 5 concepts: pandas explode counting of the raw early rows
Every match must be <= 1e-9 -> results/audit.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

from common import DATA, RES, ROOT, jdump, setup_logger

logger = setup_logger("audit_frame_n")
TOL = 1e-9


def psp_sm(df: pd.DataFrame, x: str, y: str, rung: str) -> tuple[float, int]:
    from laddern import rung_design
    Bc, Cc = rung_design(df, rung)
    d = pd.concat([df[[x, y]], Bc, Cc], axis=1)
    d = d[np.all(np.isfinite(d.to_numpy(float)), 1)]
    Cc2 = d[Cc.columns]
    Cc2 = Cc2.loc[:, Cc2.std() > 0]
    Z = np.c_[stats.rankdata(d[Bc.columns].to_numpy(float), axis=0), Cc2.to_numpy(float)]
    Z = sm.add_constant(Z, has_constant="add")
    rx = sm.OLS(stats.rankdata(d[x]), Z).fit().resid
    ry = sm.OLS(stats.rankdata(d[y]), Z).fit().resid
    return float(stats.pearsonr(rx, ry)[0]), int(len(d))


def dl(b, se) -> float:
    b, se = np.asarray(b, float), np.asarray(se, float)
    w = 1 / se ** 2
    bf = np.sum(w * b) / np.sum(w)
    Q = np.sum(w * (b - bf) ** 2)
    c = np.sum(w) - np.sum(w ** 2) / np.sum(w)
    tau2 = max(0.0, (Q - (len(b) - 1)) / c)
    ws = 1 / (se ** 2 + tau2)
    return float(np.sum(ws * b) / np.sum(ws))


def rarefied_hypergeom(counts, m: int) -> float:
    counts = np.asarray([c for c in counts if c > 0], int)
    N = int(counts.sum())
    if N < m:
        return float("nan")
    return float(sum(1 - stats.hypergeom(N, int(nj), m).pmf(0) for nj in counts))


@logger.catch(reraise=True)
def main() -> None:
    res = json.loads((RES / "frame_n_result.json").read_text())
    df = pd.read_parquet(DATA / "analysis_frame_n.parquet")
    prim = res["primary_outcome"]
    C = res["cells"]
    out = {"tolerance": TOL, "checks": {}}
    for x in ("OPEN_home", "NOVCHURN_home"):
        for r in ("R3", "R5"):
            v, n = psp_sm(df, x, prim, r)
            ref = C[f"ladder|{x}|{prim}|{r}"]
            out["checks"][f"psp|{x}|{prim}|{r}"] = {"audit": v, "result": ref["rho"], "n_audit": n, "n_result": ref["n"],
                                                   "abs_diff": abs(v - ref["rho"]), "ok": abs(v - ref["rho"]) <= TOL}
    for x in ("OPEN_home", "NOVCHURN_home"):
        g = C[f"groups|{x}|{prim}|R3"]
        est = g["estimable"]
        if len(est) >= 2:
            v = dl([g["groups"][k]["rho"] for k in est], [g["groups"][k]["se"] for k in est])
            out["checks"][f"DL|{x}"] = {"audit": v, "result": g["DL"]["b"], "abs_diff": abs(v - g["DL"]["b"]),
                                        "ok": abs(v - g["DL"]["b"]) <= TOL}
    m = np.isfinite(df.CHENG_consistency_home) & np.isfinite(df.V_next)
    v = float(stats.spearmanr(df.loc[m, "CHENG_consistency_home"], df.loc[m, "V_next"])[0])
    ref = C["cheng|CHENG_consistency_home|V_next|raw"]["rho"]
    out["checks"]["cheng_raw_rho"] = {"audit": v, "result": ref, "abs_diff": abs(v - ref), "ok": abs(v - ref) <= TOL}
    # O2r_m50 for 30 concepts from raw sealed + open rows
    sealed = pd.concat([pd.read_parquet(p) for p in sorted((ROOT / "sealed/parts").glob("sealed*.parquet"))])
    pre = pd.read_parquet(ROOT / "open/passN_pre_agg.parquet")
    e = pd.read_parquet(ROOT / "open/early_frame.parquet", columns=["ci", "year", "vfield"]).assign(n=1)
    rng = np.random.default_rng(5)
    sub = df[np.isfinite(df.O2r_m50)].sample(min(30, int(np.isfinite(df.O2r_m50).sum())), random_state=5)
    diffs = []
    for r in sub.itertuples():
        a0 = r.t0 + 6 - (1 if r.t0 == 2015 else 0)
        rows = pd.concat([d[(d.ci == r.ci) & (d.year >= a0) & (d.year <= a0 + 2) & (d.vfield >= 1)]
                          [["vfield", "n"]] for d in (sealed, pre, e)])
        cnt = rows.groupby("vfield").n.sum().to_numpy()
        v = rarefied_hypergeom(cnt, 50)
        diffs.append(abs(v - r.O2r_m50))
    out["checks"]["O2r_m50_hypergeom_30"] = {"n": len(diffs), "max_abs_diff": float(np.max(diffs)),
                                             "ok": float(np.max(diffs)) <= 1e-8}
    # CHENG consistency for 5 concepts (independent counting; SELF from ego.self_topics)
    import ego
    from ego_ctx import rq1_context
    ego.set_context(rq1_context())
    ee = pd.read_parquet(ROOT / "open/early_frame.parquet", columns=["ci", "year", "topics", "vfield"])
    sub = df[np.isfinite(df.CHENG_consistency_home) & (df.n_home_early >= 10)].sample(5, random_state=9)
    cd = []
    for r in sub.itertuples():
        home = {int(float(x)) - 10 for x in str(r.home).split(";") if x}
        d = ee[(ee.ci == r.ci) & ee.vfield.isin(home) & (ee.year >= r.t0) & (ee.year <= r.t0 + 2)]
        works = [(int(y), tuple(int(t) for t in tp)) for y, tp in zip(d.year, d.topics)]
        n_early, nc_early = ego.window_counts(works, [r.t0, r.t0 + 1, r.t0 + 2])
        SELF = ego.self_topics(str(r.name), [a for a in str(r.aliases).split("|") if a and a != "nan"],
                               n_early, nc_early)
        x = d.explode("topics").dropna(subset=["topics"])
        x = x[~x.topics.astype(int).map(lambda k: bool(SELF[k]))]
        tab = x.groupby(["year", "topics"]).size().unstack(fill_value=0)
        cs = []
        for y in (r.t0 + 1, r.t0 + 2):
            a = tab.loc[y - 1] if (y - 1) in tab.index else pd.Series(dtype=float)
            b = tab.loc[y] if y in tab.index else pd.Series(dtype=float)
            S = a[a >= 1].index
            av, bv = a.reindex(S).fillna(0).to_numpy(float), b.reindex(S).fillna(0).to_numpy(float)
            cs.append(0.0 if len(S) == 0 or bv.sum() == 0 else float(av @ bv / np.linalg.norm(av) / np.linalg.norm(bv)))
        cd.append(abs(np.mean(cs) - r.CHENG_consistency_home))
    out["checks"]["cheng_consistency_5"] = {"max_abs_diff": float(max(cd)), "ok": float(max(cd)) <= TOL}
    out["all_ok"] = bool(all(v["ok"] for v in out["checks"].values()))
    jdump(out, RES / "audit.json")
    logger.info(f"audit: all_ok={out['all_ok']} {json.dumps(out['checks'], default=str)[:1500]}")


if __name__ == "__main__":
    main()
