"""S2: construct-identity check -- is Cheng's count-weighted consistency 'the same as' this run's older measures?

Spearman of CONS_early_home (per body) with
  * Exp11 unweighted Jaccard persistence (HOME PMI neighbours), mean over t0+1..t0+2        [EXP5 bodies only]
  * EXP10 edge_persistence__home (static t0..t0+2 Jaccard)                                  [all bodies]
  * -NOVCHURN_home, NOVCHURN_home = mean(z NOV_res_home, -z edge_persistence_home) with the EXP10 frozen
    open_constants['home'] (winsorised at the frozen lo/hi, both components required)       [all bodies]
  * log early volume (B5 logvol) and home degree (mean # non-self HOME topics over t0+1..t0+2)
CIs: Fisher-z 95% (n - 3). This step reads NO outcome."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

from common import BODY_COHORT, DATA, EXP8, EXP10, EXP11, RES, jdump, jload


def spear(a: np.ndarray, b: np.ndarray) -> dict:
    ok = np.isfinite(a) & np.isfinite(b)
    n = int(ok.sum())
    if n < 20:
        return {"rho": None, "n": n, "ci": [None, None]}
    r = float(stats.spearmanr(a[ok], b[ok])[0])
    z, se = math.atanh(max(min(r, 0.999999), -0.999999)), 1 / math.sqrt(n - 3)
    return {"rho": r, "n": n, "ci": [math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)]}


def novchurn(df: pd.DataFrame) -> np.ndarray:
    k = jload(EXP10 / "results/frozen_spec.json")["open_constants"]["home"]
    zn = (np.clip(df.NOV_res__home.to_numpy(float), k["NOV_res"]["lo"], k["NOV_res"]["hi"]) - k["NOV_res"]["mu"]) \
        / k["NOV_res"]["sd"]
    ep = k["edge_persistence"]
    ze = (np.clip(df.edge_persistence__home.to_numpy(float), ep["lo"], ep["hi"]) - ep["mu"]) / ep["sd"]
    return (zn - ze) / 2.0


def load_static_covars() -> pd.DataFrame:
    """ci, logvol (B5) for both frames; EXP10 ego_open (edge persistence, NOV_res) for both frames."""
    a5 = pd.read_parquet(EXP8 / "data/analysis_table.parquet", columns=["ci", "logvol"])
    ac = pd.read_parquet(EXP10 / "data/analysis_cohort.parquet", columns=["ci", "logvol"])
    eo = pd.concat([pd.read_parquet(EXP10 / "data/ego_open_exp5.parquet",
                                    columns=["ci", "edge_persistence__home", "NOV_res__home"]).assign(src="EXP5"),
                    pd.read_parquet(EXP10 / "data/ego_open_cohort.parquet",
                                    columns=["ci", "edge_persistence__home", "NOV_res__home"]).assign(src="COH")])
    return pd.concat([a5, ac]), eo


def run(logger) -> dict:
    st = pd.read_parquet(DATA / "cheng_static.parquet")
    lv, eo = load_static_covars()
    st5 = st[st.body != BODY_COHORT].merge(lv, on="ci", how="left").merge(
        eo[eo.src == "EXP5"].drop(columns="src"), on="ci", how="left")
    stc = st[st.body == BODY_COHORT].merge(lv, on="ci", how="left").merge(
        eo[eo.src == "COH"].drop(columns="src"), on="ci", how="left")
    yp = pd.read_parquet(EXP11 / "data/yearly_panel.parquet", columns=["ci", "year", "t0", "persistence"])
    yp = yp[(yp.year >= yp.t0 + 1) & (yp.year <= yp.t0 + 2)].groupby("ci").persistence.mean().rename(
        "jaccard_exp11_early").reset_index()
    st5 = st5.merge(yp, on="ci", how="left")
    d = pd.concat([st5, stc], ignore_index=True)
    d["NEG_NOVCHURN_home"] = -novchurn(d)
    d.to_parquet(DATA / "identity_table.parquet", index=False)
    comps = {"jaccard_exp11_early": "Exp11 unweighted Jaccard persistence (yearly HOME PMI neighbours, mean t0+1..t0+2)",
             "edge_persistence__home": "EXP10 static Jaccard edge persistence (HOME, t0..t0+2)",
             "NEG_NOVCHURN_home": "-NOVCHURN_home (EXP10 frozen z constants)",
             "logvol": "log early volume (B5)", "deg_early_home": "HOME degree (mean # non-self topics t0+1..t0+2)",
             "CONS_early_all": "ALL-papers build of the same measure", "CONS_r_early_home": "Cheng-verbatim support-"
             "restricted cosine", "EMB_early_home": "EMB analogue", "SOC_early_home": "SOC"}
    out = {"label": "construct-identity check (reads no outcome)", "definitions": comps, "by_body": {}}
    bodies = {"EXP5_pooled": d[d.body != BODY_COHORT], **{b: d[d.body == b] for b in sorted(d.body.unique())}}
    for b, g in bodies.items():
        x = g.CONS_early_home.to_numpy(float)
        out["by_body"][b] = {c: spear(x, g[c].to_numpy(float)) for c in comps if c in g.columns}
        out["by_body"][b]["n_concepts"] = int(len(g))
        out["by_body"][b]["n_CONS_finite"] = int(np.isfinite(x).sum())
    p = out["by_body"]["EXP5_pooled"]
    out["sanity"] = {
        "i_jaccard_rho_gt_0.3": bool((p["jaccard_exp11_early"]["rho"] or 0) > 0.3),
        "ii_CONS_in_0_1": bool(np.nanmin(d.CONS_early_home) >= -1e-12 and np.nanmax(d.CONS_early_home) <= 1 + 1e-12),
        "ii_median": float(np.nanmedian(d.CONS_early_home)),
        "iii_abs_rho_logvol": abs(p["logvol"]["rho"]) if p["logvol"]["rho"] is not None else None,
        "iii_size_laden_flag": bool(abs(p["logvol"]["rho"] or 0) > 0.6)}
    jdump(out, RES / "identity_check.json")
    logger.info(f"identity pooled: { {k: (v['rho'] if isinstance(v, dict) else v) for k, v in p.items()} }")
    logger.info(f"sanity: {out['sanity']}")
    return out
