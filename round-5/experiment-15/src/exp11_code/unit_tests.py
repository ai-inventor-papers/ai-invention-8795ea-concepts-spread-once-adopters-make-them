#!/usr/bin/env python3
"""T0 unit tests (no network): writes results/unit_tests.json.
 (1) ego_year on a hand-built 6-topic toy backbone      (2) dens_null calibration
 (3) D3 entries / at_risk vs hand values and h2_exp6     (4) PPML with concept + year FE on simulated data
 (5) Sun-Abraham IW vs plain TWFE under heterogeneous cohort effects
 (6) reverse-path paired bootstrap (one-directional vs symmetric feedback)
 (7) seal gate                                           (8) psp = EXP8 rq1stats, reproduces EXP8 held-out numbers"""
from __future__ import annotations

import json
import shutil
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import RES, RUN_ROOT, jdump, setup_logger

warnings.filterwarnings("ignore")
EXP8 = RUN_ROOT / "round-3/experiment-8/src"


def toy_context(nt: int, edges: list[tuple[int, int]], comm: np.ndarray) -> dict:
    import ego
    from ego_ctx import lemmas, topic_lemma_df
    a = np.array([e[0] for e in edges], int)
    b = np.array([e[1] for e in edges], int)
    deg = np.bincount(np.r_[a, b], minlength=nt)
    names = [f"toytopic{k}" for k in range(nt)]
    years = list(range(1995, 2023))
    ctx = dict(nt=nt, comm=[comm] * 3, comm_q=[0] * 3, deg=[deg] * 3, knn=[(a, b)] * 3, full_edges=[(a, b)] * 3,
               subfield=np.zeros(nt, int), names=names, ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names],
               lemmas=lemmas, years=years, bg=np.full((len(years), nt), 100.0), Gt={y: 10000 for y in years})
    ego.set_context(ctx)
    import ego_yearly
    ego_yearly._ADJ.clear()
    return ctx


def test1() -> dict:
    import ego
    import ego_yearly
    toy_context(6, [(0, 1), (1, 2), (0, 2), (3, 4)], np.array([0, 0, 0, 1, 1, 2]))
    old = ego.SELF_SHARE
    ego.SELF_SHARE = 1.01
    W = []   # (year, vfield, topics)
    W += [(2002, 1, (5,))]
    W += [(2004, 1, (0,))] * 2
    W += [(2005, 1, (0,))] * 2 + [(2005, 1, (1,))] * 2 + [(2005, 1, (5,))] * 2 + [(2005, 2, (2,))] * 2
    W += [(2006, 1, (3,))] * 2 + [(2006, 1, (4,))] * 2 + [(2006, 1, (0,))] * 2
    years = np.array([w[0] for w in W]); vf = np.array([w[1] for w in W])
    t_off = np.r_[0, np.cumsum([len(w[2]) for w in W])]
    tflat = np.concatenate([np.array(w[2]) for w in W])
    rows, _, _ = ego_yearly.concept_yearly(ci=0, name="qqq", aliases=[], t0=2005, h_end=2006, years=years, vfield=vf,
                                           t_off=t_off, tflat=tflat, home_codes={1}, min_n=2, seed=1, do_null=False)
    ego.SELF_SHARE = old
    r5, r6 = rows[0], rows[1]
    exp = {2005: dict(deg=3, new_rate=0.5, n_comm=2, participation=4 / 9, density=1 / 3, persistence=1 / 3,
                      nov_res=-1 / 3),
           2006: dict(deg=3, new_rate=0.5, n_comm=2, participation=4 / 9, density=1 / 3, persistence=1 / 5)}
    errs = {}
    for r, y in ((r5, 2005), (r6, 2006)):
        for k, v in exp[y].items():
            errs[f"{y}_{k}"] = abs(float(r[k]) - v)
    ok = max(errs.values()) < 1e-12
    return {"pass": bool(ok), "max_abs_err": max(errs.values()), "errors": errs,
            "note": "off-home works (vfield 2, topic 2) must not enter the home-only neighbourhood"}


def test2() -> dict:
    import ego_yearly
    rng = np.random.default_rng(3)
    nt = 60
    toy_context(nt, [(i, j) for i in range(nt) for j in range(i + 1, nt)], np.zeros(nt, int))
    w = np.ones(nt)
    full = ego_yearly.density_null(10, np.arange(nt), w, 0, rng, n=200)
    toy_context(nt, [(0, 1)], np.zeros(nt, int))
    empty = ego_yearly.density_null(10, np.arange(2, nt), w, 0, rng, n=200)
    nt = 200
    ed = [(i, j) for i in range(nt) for j in range(i + 1, nt) if rng.random() < 0.3]
    toy_context(nt, ed, np.zeros(nt, int))
    gd = len(ed) / (nt * (nt - 1) / 2)
    rnd = ego_yearly.density_null(20, np.arange(nt), np.ones(nt), 0, rng, n=2000)
    return {"pass": bool(abs(full - 1) < 1e-12 and abs(empty) < 1e-12 and abs(rnd - gd) < 0.01 and abs(gd - 0.3) < 0.01),
            "complete": full, "empty": empty, "random_p0.3_mean": rnd, "graph_density": gd}


def test3() -> dict:
    import d3
    import h2_exp6
    from build_d3 import d3_counts
    NY = d3.NY
    G = np.zeros((1, NY, 27))
    # home field 11 (slot 1); off-home fields 12 (slot 2), 13 (slot 3), 14 (slot 4), 15 (slot 5)
    G[0, 10, 1] = 5
    G[0, 10, 2] = 1; G[0, 11, 2] = 1            # field 12: cum reaches 2 in year index 11
    G[0, 12, 3] = 3                              # field 13: entered at index 12
    G[0, 13, 4] = 1                              # field 14: never reaches 2
    G[0, 14, 5] = 1; G[0, 17, 5] = 1             # field 15: entered at index 17
    home = np.zeros((1, 26), bool); home[0, 0] = True
    S = d3.panel_states(G, home)
    entries, at_risk, cum_prev, _, _ = d3_counts(S, home)
    exp_entries = np.zeros(NY, int); exp_entries[[11, 12, 17]] = 1
    exp_risk = np.full(NY, 25); exp_risk[12:] = 24; exp_risk[13:] = 23; exp_risk[18:] = 22
    st = h2_exp6.states(G[0], [11])
    same = bool((st["entered"] == S["entered"][0]).all())
    ok = bool((entries[0] == exp_entries).all() and (at_risk[0] == exp_risk).all() and same)
    return {"pass": ok, "entries_match": bool((entries[0] == exp_entries).all()),
            "at_risk_match": bool((at_risk[0] == exp_risk).all()), "h2_exp6_equal": same}


def test4(n_sim: int = 100) -> dict:
    from fe_stats import ppml
    rng = np.random.default_rng(4)
    b_eff, b_null, cover = [], [], []
    for s in range(n_sim):
        C, T = 2000, 10
        ci = np.repeat(np.arange(C), T); yr = np.tile(np.arange(T), C)
        a = rng.normal(-1, 0.5, C)[ci]; d = rng.normal(0, 0.3, T)[yr]
        x = rng.normal(0, 1, C * T) + 0.5 * a
        y = rng.poisson(np.exp(a + d + 0.3 * x))
        df = pd.DataFrame({"ci": ci, "year": yr, "x": x, "y": y})
        f = ppml(df, "y", ["x"])
        b_eff.append(float(f.coef()["x"]))
        df["y0"] = rng.poisson(np.exp(a + d))
        f0 = ppml(df, "y0", ["x"])
        b0 = float(f0.coef()["x"]); lo, hi = f0.confint().loc["x"].to_numpy(float)
        b_null.append(b0); cover.append(lo <= 0 <= hi)
    m, mn, cv = float(np.mean(b_eff)), float(np.mean(np.abs(b_null))), float(np.mean(cover))
    return {"pass": bool(abs(m - 0.3) < 0.02 and mn < 0.01 and 0.93 <= cv <= 0.97), "mean_beta_effect": m,
            "mean_abs_beta_null": mn, "crv1_coverage_null": cv, "n_sim": n_sim,
            "note": "coverage checked with the CRV1 intervals used for per-group results; the bootstrap is the "
                    "same resampling unit (concept)"}


def test5() -> dict:
    from fe_stats import feols_np, sun_abraham
    rng = np.random.default_rng(5)
    N, years = 3000, np.arange(2000, 2016)
    coh = rng.choice([2005, 2008, 2011, np.nan], size=N, p=[0.2, 0.25, 0.25, 0.3])
    mult = {2005: 1.0, 2008: 2.0, 2011: 3.0}
    rows = []
    a = rng.normal(0, 1, N)
    d = rng.normal(0, 0.5, len(years))
    for i in range(N):
        for j, y in enumerate(years):
            e = y - coh[i] if np.isfinite(coh[i]) else np.nan
            eff = 0.1 * (e + 1) * mult[coh[i]] if np.isfinite(e) and e >= 0 else 0.0
            rows.append((i, y, coh[i], a[i] + d[j] + eff + rng.normal(0, 0.3), eff, e))
    df = pd.DataFrame(rows, columns=["ci", "year", "g", "y", "eff", "e"])
    r = sun_abraham(df, "y", [], "g", "never")
    true = {k: float(df[(df.e == k)].eff.mean()) for k in (0, 1, 2, 3, 4)}
    err = max(abs(r["att"][k] - true[k]) for k in true)
    # plain TWFE event study: pooled relative-time dummies, no cohort interaction, never-treated + all cohorts
    rel = [k for k in range(-3, 5) if k != -1]
    X = np.column_stack([(df.e == k).to_numpy(float) for k in rel] +
                        [(df.e < -3).to_numpy(float), (df.e > 4).to_numpy(float)])
    tw = feols_np(df.y.to_numpy(), X, [df.ci.to_numpy(), df.year.to_numpy()], df.ci.to_numpy(),
                  [f"e{k}" for k in rel] + ["lo", "hi"])
    tw_err = max(abs(tw["b"][f"e{k}"] - true[k]) for k in true)
    lead_err = max(abs(r["att"][k]) for k in (-3, -2))
    return {"pass": bool(err < 0.02 and tw_err > 0.05 and lead_err < 0.03), "iw_max_abs_err": err,
            "twfe_max_abs_err": tw_err, "iw_max_abs_lead": lead_err, "true_att": true,
            "iw_att": {k: r["att"][k] for k in r["att"]}, "twfe": {k: tw["b"][f"e{k}"] for k in rel}}


def hm3_sim(rng, feedback: bool, n_boot: int = 150) -> bool:
    from fe_stats import cluster_index, cluster_resample, feols_np, within_sd
    N, T = 600, 10
    x = np.zeros((N, T)); y = np.zeros((N, T))
    ax, ay = rng.normal(0, 1, N), rng.normal(0, 1, N)
    x[:, 0] = ax + rng.normal(0, 1, N); y[:, 0] = ay + rng.normal(0, 1, N)
    for t in range(1, T):
        x[:, t] = ax + 0.3 * (y[:, t - 1] - ay if feedback else 0) + rng.normal(0, 1, N)
        y[:, t] = ay + 0.3 * (x[:, t - 1] - ax) + rng.normal(0, 1, N)
    ci = np.repeat(np.arange(N), T - 1); yr = np.tile(np.arange(T - 1), N)
    df = pd.DataFrame({"ci": ci, "year": yr, "x": x[:, :-1].ravel(), "y": y[:, :-1].ravel(),
                       "x_next": x[:, 1:].ravel(), "y_next": y[:, 1:].ravel()})

    def stat(d):
        c, t_ = d.ci.to_numpy(), d.year.to_numpy()
        f = feols_np(d.y_next.to_numpy(), d[["x"]].to_numpy(), [c, t_], c, ["x"])["b"]["x"]
        r = feols_np(d.x_next.to_numpy(), d[["y"]].to_numpy(), [c, t_], c, ["y"])["b"]["y"]
        sx, sy = within_sd(d.x.to_numpy(), c, t_), within_sd(d.y.to_numpy(), c, t_)
        return abs(f * sx / sy) - abs(r * sy / sx)
    idx = cluster_index(df.ci.to_numpy())
    bs = [stat(cluster_resample(df, idx, rng)) for _ in range(n_boot)]
    return bool(np.percentile(bs, 2.5) > 0)


def test6(n_sim: int = 40) -> dict:
    rng = np.random.default_rng(6)
    one = float(np.mean([hm3_sim(rng, False) for _ in range(n_sim)]))
    sym = float(np.mean([hm3_sim(rng, True) for _ in range(n_sim)]))
    return {"pass": bool(one >= 0.9 and sym <= 0.1), "share_HM3_one_directional": one,
            "share_HM3_symmetric": sym, "n_sim": n_sim}


def test7() -> dict:
    import seal_m
    tmp = RES / "_t7"
    tmp.mkdir(exist_ok=True)
    spec, seal = tmp / "spec.json", tmp / "seal.log"
    ofile = tmp / "out.parquet"
    pd.DataFrame({"ci": [1], "year": [2000], "entries": [1]}).to_parquet(ofile)
    panel = pd.DataFrame({"ci": [1], "year": [2000]})
    res = {}
    for f in (spec, seal):
        if f.exists():
            f.unlink()
    try:
        seal_m.attach_outcomes(panel, spec, seal, ofile)
        res["missing_spec_raises"] = False
    except seal_m.SealError:
        res["missing_spec_raises"] = True
    seal_m.freeze({"a": 1}, spec_path=spec, seal_path=seal)
    spec.write_text(json.dumps({"a": 2}))
    try:
        seal_m.attach_outcomes(panel, spec, seal, ofile)
        res["hash_mismatch_raises"] = False
    except seal_m.SealError:
        res["hash_mismatch_raises"] = True
    seal_m.freeze({"a": 1}, spec_path=spec, seal_path=seal)
    seal_m.reset_for_tests()
    ok1 = len(seal_m.attach_outcomes(panel, spec, seal, ofile, reason="unit test")) == 1
    try:
        seal_m.attach_outcomes(panel, spec, seal, ofile)
        res["second_attach_raises"] = False
    except seal_m.SealError:
        res["second_attach_raises"] = True
    seal_m.reset_for_tests()
    shutil.rmtree(tmp)
    res["valid_attach_ok"] = ok1
    res["pass"] = all(res.values())
    return res


def test8() -> dict:
    from rq1stats import dersimonian_laird, dummies, psp_point
    A = pd.read_parquet(EXP8 / "data" / "analysis_table.parquet")
    hu = pd.read_csv(EXP8 / "results" / "portability_table.csv")
    B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
    errs, zs, ses = {}, [], []
    for u in ("PHYS", "LIFEENV", "SOC", "MATHDEC"):
        d = A[A.unit == u]
        d = d[np.isfinite(d.new_edge_rate) & np.isfinite(d.O2r_m50) & np.isfinite(d[B5]).all(1)]
        rho = psp_point(d.new_edge_rate.to_numpy(float), d.O2r_m50.to_numpy(float), d[B5].to_numpy(float),
                        dummies(d.t0.to_numpy()))
        ref = hu[(hu.indicator == "new_edge_rate") & (hu.outcome == "O2r_m50") & (hu.unit == u)].iloc[0]
        errs[u] = abs(rho - ref.rho)
        errs[u + "_n"] = int(len(d)) - int(ref.n)
        zs.append(ref.z); ses.append(ref.se_z)
    pl = dersimonian_laird(np.array(zs), np.array(ses))
    pooled = float(np.tanh(pl["b"]))
    return {"pass": bool(max(abs(v) for v in errs.values()) < 1e-6 and abs(pooled - 0.118) < 0.0015), "unit_abs_err": errs,
            "pooled_from_stored_z": pooled, "exp8_reported": 0.118}


def main() -> None:
    logger = setup_logger("unit_tests")
    out = {}
    for name, fn in [("t1_ego_year_toy", test1), ("t2_dens_null", test2), ("t3_d3", test3), ("t7_seal", test7),
                     ("t8_psp_exp8", test8), ("t5_sun_abraham", test5), ("t6_reverse_path", test6),
                     ("t4_ppml_sim", test4)]:
        t = time.time()
        try:
            out[name] = fn()
        except Exception as e:  # noqa: BLE001 -- report every test even if one crashes
            logger.exception(f"{name} crashed")
            out[name] = {"pass": False, "error": repr(e)[:500]}
        out[name]["seconds"] = round(time.time() - t, 1)
        logger.info(f"{name}: {json.dumps(out[name], default=str)[:600]}")
    out["all_pass"] = all(v.get("pass") for v in out.values() if isinstance(v, dict))
    jdump(out, RES / "unit_tests.json")
    logger.info(f"ALL PASS: {out['all_pass']}")


if __name__ == "__main__":
    main()
