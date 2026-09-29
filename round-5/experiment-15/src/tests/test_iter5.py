#!/usr/bin/env python3
"""T0 unit tests for the iter-5 Part A / Part B code (no real outcomes are read; synthetic outcomes only).

  G2  home build reproduces Exp10 NOV_res__home / new_edge_rate__home / edge_persistence__home (all concepts, 1e-9)
  b   decomposition identities on 200 random concepts and on all concepts (1e-12)
  c   Shapley efficiency and symmetry
  d   planted signal: y = B5 + 0.4 z(METHOD-only NOVCHURN) + noise -> Shapley gives > 70% to METHOD in >= 90% of 50
      simulations; no plant -> the METHOD-DOMAIN novnull contrast CI excludes 0 at about the 5% rate
  e   ICC recovery: simulated panel with the real unbalanced structure and ICC 0.5 -> estimate within +/- 0.03
  f   degree-weighted median cut: mean null share of the low class 0.50 +/- 0.02
  s   vectorised Scorer == EXP8 rq1stats.psp_point (1e-10)
Writes results/unit_tests_iter5.json."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "lib_iter5"))
sys.path.insert(0, str(WS))

import numpy as np
import pandas as pd

from common_iter5 import B5, DATA, E8, E10, E11, RES, jdump, read_parts, setup_logger


def test_g2() -> dict:
    out = {}
    for frame, f10 in (("exp5", "ego_open_exp5.parquet"), ("cohort", "ego_open_cohort.parquet")):
        c = pd.read_parquet(DATA / f"partner_home_components_{frame}.parquet")
        e = pd.read_parquet(E10 / "data" / f10)
        m = c.merge(e, on="ci", suffixes=("", "_e10"))
        r = {"n_concepts": int(len(m))}
        for a, b in (("NOV_res", "NOV_res__home"), ("new_edge_rate", "new_edge_rate__home"),
                     ("edge_persistence", "edge_persistence__home"), ("M", "M__home"), ("n_home_early", "n_home_early_e10")):
            x, y = m[a].to_numpy(float), m[b].to_numpy(float)
            ok = np.isfinite(x) & np.isfinite(y)
            r[a] = {"nan_pattern_equal": bool((np.isnan(x) == np.isnan(y)).all()),
                    "max_abs_diff": float(np.abs(x[ok] - y[ok]).max()) if ok.any() else 0.0, "n_finite": int(ok.sum())}
        r["pass"] = bool(all(v["nan_pattern_equal"] and v["max_abs_diff"] < 1e-9 for k, v in r.items() if isinstance(v, dict)))
        out[frame] = r
    out["pass"] = bool(out["exp5"]["pass"] and out["cohort"]["pass"])
    return out


def feats(frame: str):
    import score_partA as S
    spec_k = json.loads((E10 / "results/frozen_spec.json").read_text())["open_constants"]["home"]
    k = {"NOV_res": spec_k["NOV_res"], "edge_persistence": spec_k["edge_persistence"]}
    comp = pd.read_parquet(DATA / f"partner_home_components_{frame}.parquet")
    rows = read_parts(DATA / f"partner_home_rows_{frame}")
    F, ident = S.build_features(comp, rows, k)
    return F, ident, rows, k


def test_b(F, ident, rows) -> dict:
    rng = np.random.default_rng(1)
    sub = F.sample(200, random_state=1)
    errs = {}
    for ax, cl in {"type": ["METHOD", "DOMAIN", "OTHER"], "deg": ["low", "high"], "carrier": ["mixed", "pure"]}.items():
        errs[f"nov_{ax}"] = float(np.nanmax(np.abs(sub[[f"nov_{ax}_{X}" for X in cl]].sum(1, min_count=1) - sub.NOV_res)))
    for ax, cl in {"type": ["METHOD", "DOMAIN", "OTHER"], "comm": ["new", "old", "unk"], "deg": ["low", "high"],
                   "carrier": ["mixed", "pure"]}.items():
        errs[f"ner_{ax}"] = float(np.nanmax(np.abs(sub[[f"ner_{ax}_{X}" for X in cl]].sum(1) - sub.new_edge_rate)))
        errs[f"churn_{ax}"] = float(np.nanmax(np.abs(sub[[f"chd_{ax}_{X}" for X in cl] + [f"cha_{ax}_{X}" for X in cl]]
                                                  .sum(1, min_count=1) - (1 - sub.edge_persistence))))
    # rows reproduce the parts
    r = rows[rows.ci.isin(set(sub.ci))]
    g = r[r.role == "new"].groupby(["ci", "type"]).w_ner.sum().unstack(fill_value=0)
    errs["rows_ner_type_METHOD"] = float(np.abs(sub.set_index("ci").ner_type_METHOD.reindex(g.index) - g.get("METHOD", 0)).max())
    gn = r[r.role == "new"].groupby(["ci", "deg"]).w_nov.sum().unstack(fill_value=0)
    s2 = sub.set_index("ci").nov_deg_low.reindex(gn.index)
    ok = np.isfinite(s2)
    errs["rows_nov_deg_low"] = float(np.abs(s2[ok] - gn.get("low", 0)[ok]).max())
    return {"errors": errs, "all_concepts": ident, "pass": bool(max(errs.values()) < 1e-12 and
                                                               max(v for k, v in ident.items() if not k.endswith("_min")) < 1e-12)}


def test_c() -> dict:
    from partA_stats import shapley, subsets
    rng = np.random.default_rng(3)
    pl = ["a", "b", "c", "d"]
    w = rng.normal(size=4)
    v = {S: float(sum(w[pl.index(p)] for p in S) + 0.3 * (("a" in S) and ("b" in S))) for S in subsets(pl)}
    phi = shapley(pl, v)
    eff = abs(sum(phi.values()) - (v[frozenset(pl)] - v[frozenset()]))
    pl2 = ["x", "y", "z"]
    v2 = {S: float(len(S & {"x", "y"}) ** 1.5 + 0.2 * ("z" in S)) for S in subsets(pl2)}
    phi2 = shapley(pl2, v2)
    return {"efficiency_err": eff, "symmetry_err": abs(phi2["x"] - phi2["y"]), "phi": phi,
            "pass": bool(eff < 1e-12 and abs(phi2["x"] - phi2["y"]) < 1e-12)}


def test_s() -> dict:
    from partA_stats import Scorer
    from rq1stats import dummies, psp_point
    rng = np.random.default_rng(4)
    n = 600
    B = rng.normal(size=(n, 5))
    cat = dummies(rng.integers(0, 4, n))
    y = B.sum(1) + rng.normal(size=n)
    X = np.c_[rng.normal(size=n), rng.poisson(2, n).astype(float), rng.normal(size=n)]
    X[rng.random(n) < 0.2, 2] = np.nan
    sc = Scorer(X, ["a", "b", "c"], y, B, cat)
    p = sc.eval()
    ref = []
    for j in range(3):
        ok = np.isfinite(X[:, j])
        ref.append(psp_point(X[ok, j], y[ok], B[ok], cat[ok]))
    err = float(np.max(np.abs(p - np.array(ref))))
    return {"max_abs_err": err, "pass": bool(err < 1e-10)}


def synth_body(F: pd.DataFrame) -> pd.DataFrame:
    A = pd.read_parquet(E8 / "data/analysis_table.parquet", columns=["ci", "t0", "group", "split"] + B5)
    d = A.merge(F, on="ci")
    d = d[d.split == "DEV"].reset_index(drop=True)
    return d


def test_d(F: pd.DataFrame, k: dict, n_sim: int = 50) -> dict:
    import score_partA as S
    from partA_stats import Scorer, shapley
    d = synth_body(F)
    G = S.games(d, k)
    pl, cmap, _ = G["NOVCHURN_type"]
    tM = cmap[frozenset({"METHOD"})]
    zM = (tM - np.nanmean(tM)) / np.nanstd(tM)
    base = d[B5].rank().sum(1).to_numpy(float)
    base = (base - base.mean()) / base.std()
    Bm, cat = S.design(d, "DEV", None)
    rng = np.random.default_rng(7)
    shares, rej = [], []
    keys = list(cmap)
    X = np.column_stack([cmap[s] for s in keys] + [d.novnull_type_METHOD.to_numpy(float), d.novnull_type_DOMAIN.to_numpy(float)])
    for i in range(n_sim):
        y = base + 0.4 * np.nan_to_num(zM) + rng.normal(size=len(d))
        y[~np.isfinite(zM)] = np.nan
        sc = Scorer(X, [str(i) for i in range(X.shape[1])], y, Bm, cat)
        p = sc.eval()
        v = {s: (0.0 if len(s) == 0 else p[j]) for j, s in enumerate(keys)}
        phi = shapley(pl, v)
        tot = sum(phi.values())
        shares.append(phi["METHOD"] / tot if tot else np.nan)
        # null: no plant, METHOD-DOMAIN novnull contrast, 100-draw paired bootstrap
        y0 = base + rng.normal(size=len(d))
        sc0 = Scorer(X[:, -2:], ["m", "d"], y0, Bm, cat)
        p0 = sc0.eval()
        bs = sc0.boot(100, 1000 + i)
        dd = bs[:, 0] - bs[:, 1]
        lo, hi = np.nanpercentile(dd, [2.5, 97.5])
        rej.append(bool(lo > 0 or hi < 0))
    shares = np.array(shares)
    frac = float(np.mean(shares > 0.7))
    return {"share_METHOD_mean": float(np.nanmean(shares)), "frac_sims_share_gt_0.7": frac,
            "null_rejection_rate": float(np.mean(rej)), "n_sim": n_sim,
            "pass": bool(frac >= 0.9 and np.mean(rej) <= 0.12)}


def test_e() -> dict:
    import trait_stability as T
    d = pd.read_parquet(E11 / "data/yearly_features.parquet", columns=["ci", "year", "age", "deg"])
    d = d[d.deg >= 2]
    rng = np.random.default_rng(11)
    ids = d.ci.unique()
    ests = []
    for s in range(5):
        u = dict(zip(ids, rng.normal(0, 1, len(ids))))
        x = d.ci.map(u).to_numpy() + rng.normal(0, 1, len(d))           # ICC = 1 / (1 + 1) = 0.5
        ests.append(T.icc1(T.resid(x, T.design_Z(d.assign(age=d.age), False)), d.ci.to_numpy()))
    err = float(np.max(np.abs(np.array(ests) - 0.5)))
    return {"estimates": ests, "max_abs_err": err, "pass": bool(err < 0.03)}


def test_f(F: pd.DataFrame) -> dict:
    v = F.null_low_share.to_numpy(float)
    v = v[np.isfinite(v)]
    m = float(v.mean())
    return {"mean_null_low_share": m, "median": float(np.median(v)), "n": int(len(v)),
            "note": "share of the degree-weighted null mass strictly below the cut key (cut topic excluded)",
            "pass": bool(abs(m - 0.5) <= 0.02)}


def main() -> None:
    logger = setup_logger("test_iter5")
    out = {}
    t = time.time()
    out["G2_reproduction"] = test_g2()
    logger.info(f"G2: {out['G2_reproduction']['pass']}")
    F, ident, rows, k = feats("exp5")
    for nm, fn in (("b_identities", lambda: test_b(F, ident, rows)), ("c_shapley", test_c), ("s_scorer", test_s),
                   ("d_planted", lambda: test_d(F, k)), ("e_icc", test_e), ("f_degcut", lambda: test_f(F))):
        t1 = time.time()
        try:
            out[nm] = fn()
        except Exception as e:  # noqa: BLE001 -- report every test
            logger.exception(f"{nm} crashed")
            out[nm] = {"pass": False, "error": repr(e)[:400]}
        out[nm]["seconds"] = round(time.time() - t1, 1)
        logger.info(f"{nm}: {json.dumps(out[nm], default=str)[:400]}")
    out["all_pass"] = bool(all(v.get("pass") for v in out.values() if isinstance(v, dict)))
    out["seconds"] = time.time() - t
    jdump(out, RES / "unit_tests_iter5.json")
    logger.info(f"ALL PASS: {out['all_pass']}")


if __name__ == "__main__":
    main()
