#!/usr/bin/env python3
"""T0 unit tests (no network, < 2 min). Writes results/unit_tests_T0.json."""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import analysis as AN  # noqa: E402
import d3  # noqa: E402
import exp5 as X  # noqa: E402
import h2_exp6 as H2  # noqa: E402
import models as M  # noqa: E402
import seal  # noqa: E402
from stats_core import CLogit  # noqa: E402

RESULTS: dict[str, dict] = {}


def check(name: str):
    def deco(fn):
        t = time.time()
        try:
            info = fn() or {}
            RESULTS[name] = {"pass": True, **info, "sec": round(time.time() - t, 2)}
        except AssertionError as e:
            RESULTS[name] = {"pass": False, "error": str(e), "sec": round(time.time() - t, 2)}
        print(f"{'PASS' if RESULTS[name]['pass'] else 'FAIL'}  {name}  {RESULTS[name]}")
        return fn
    return deco


@check("1_states_toy")
def _():
    g = np.zeros((d3.NY, 27))
    # field 13 (k=2) off-home: 1 work in 2000, 1 in 2001 -> entered 2001; 1 in 2003, 1 in 2004 -> retained 2004 (age 3)
    for y, n in ((2000, 1), (2001, 1), (2003, 1), (2004, 1)):
        g[y - 1995, 3] = n
    # field 20 (k=9): 2 works in 1996 then silence -> entered 1996, lost from 1999 (w3 == 0)
    g[1996 - 1995, 10] = 2
    home = np.zeros((1, 26), bool); home[0, 0] = True          # home = field 11
    S = d3.panel_states(g[None], home)
    yi = lambda y: y - 1995  # noqa: E731
    assert not S["entered"][0, yi(2000), 2] and S["entered"][0, yi(2001), 2]
    assert S["retaining"][0, yi(2004), 2] and not S["retaining"][0, yi(2002), 2]  # 2002: w3 = 1 (2001) + 0 -> < 2
    assert S["age"][0, yi(2004), 2] == 3
    assert S["lost"][0, yi(1999), 9] and not S["lost"][0, yi(1998), 9]
    assert S["tenure"][0, yi(1999), 9] == 0                     # last positive year == entry year
    # home field never retained
    g2 = g.copy(); g2[:, 1] = 5
    S2 = d3.panel_states(g2[None], home)
    assert not S2["retaining"][0, :, 0].any()
    return {}


@check("1b_states_equal_h2_exp6_on_50_real_concepts")
def _():
    fr, Gd = X.exp6_frame()
    rng = np.random.default_rng(0)
    pick = fr.sample(50, random_state=1)
    for r in pick.itertuples():
        g = Gd[int(r.cidx)]
        home = np.zeros((1, 26), bool)
        for h in r.home_list:
            home[0, h - 11] = True
        a = H2.states(g, r.home_list)
        b = d3.panel_states(g[None], home)
        for k in ("entered", "retaining", "lost"):
            assert (a[k] == b[k][0]).all(), k
        GF = X.exp6_GF()
        assert (H2.rca_entered(g, GF) == d3.rca_entered_panel(g[None], GF)[0]).all()
    return {"n": 50}


@check("2_rca_masks_toy")
def _():
    GF = np.ones((d3.NY, 26)) * 10.0                            # every field has share 1/26
    x = np.zeros((2, d3.NY, 26))
    x[0, 10, 0] = 3; x[0, 10, 1] = 1                            # year 10: shares 0.75, 0.25 vs 1/26 -> both RCA > 1
    x[1, 10, :] = 1                                             # uniform -> RCA exactly 1 everywhere (tie, strict > excludes)
    R = d3.rca_panel(x, GF)
    assert R["U_1y"][0, 10, 0] and R["U_1y"][0, 10, 1] and not R["U_1y"][0, 10, 2]
    assert not R["U_1y"][1, 10].any(), "RCA == 1 must not count (strict >)"
    assert R["ties_1y"] >= 26
    assert not R["U_1y"][0, 5].any(), "empty portfolio -> no RCA"
    assert R["U_cum"][0, 12, 0] and R["U_w3"][0, 12, 0] and not R["U_w3"][0, 13, 0]
    assert not R["U_pers"][0, 12, 0]                            # earlier window empty
    return {}


@check("3_density_dvol_mean_rel")
def _():
    rng = np.random.default_rng(3)
    phi = rng.random((26, 26)); phi = (phi + phi.T) / 2; np.fill_diagonal(phi, 0)
    Mk = np.zeros((1, 26), bool); Mk[0, [1, 4, 7]] = True
    k = 10
    assert np.isclose(d3._dens(Mk, phi)[0, k], phi[[1, 4, 7], k].sum() / phi[:, k].sum())
    assert np.isclose(d3._mrel(Mk, phi)[0, k], phi[[1, 4, 7], k].mean())
    s = rng.random((1, 26))
    assert np.isclose(d3._wdens(d3._share(s), phi)[0, k], (s[0] / s.sum() * phi[:, k]).sum() / phi[:, k].sum())
    assert d3._mrel(np.zeros((1, 26), bool), phi)[0, k] == 0
    bb = X.load_backbone()
    assert np.abs(np.diag(bb["phi"])).max() == 0 and np.allclose(bb["phi"], bb["phi"].T)
    return {}


@check("4_clogit_vs_statsmodels_and_stats_core")
def _():
    from statsmodels.discrete.conditional_models import ConditionalLogit
    rng = np.random.default_rng(4)
    S, J = 2000, 8
    X_ = rng.normal(size=(S * J, 3)); b = np.array([0.8, -0.5, 0.3])
    st = np.repeat(np.arange(S), J)
    u = (X_ @ b).reshape(S, J) + rng.gumbel(size=(S, J))
    y = np.zeros((S, J)); y[np.arange(S), u.argmax(1)] = 1; y = y.ravel()
    df = pd.DataFrame(X_, columns=["a", "b", "c"]); df["entered"] = y; df["stratum"] = st; df["cidx"] = st; df["field"] = np.tile(np.arange(11, 11 + J), S)
    r = M.model(df, ["a", "b", "c"]).fit()
    sm = ConditionalLogit(y, X_, groups=st).fit(disp=0)
    sc = CLogit(X_, y, st).fit()
    rel = np.abs(r["coef"] - sm.params) / np.abs(sm.params)
    assert rel.max() < 1e-3, rel
    assert np.abs(r["coef"] - sc["coef"]).max() < 1e-5
    assert np.abs(r["se"] - sm.bse).max() / sm.bse.min() < 1e-3
    return {"max_rel_diff_vs_statsmodels": float(rel.max())}


@check("4b_weighted_bootstrap_equals_duplicate_relabel")
def _():
    rng = np.random.default_rng(5)
    S, J = 300, 6
    X_ = rng.normal(size=(S * J, 2)); st = np.repeat(np.arange(S), J) + 100 * np.repeat(np.arange(S) // 3, J) * 0
    cid = np.repeat(np.arange(S) // 3, J)                        # 3 strata per concept
    st = cid * 100 + np.tile(np.repeat(np.arange(3), J), S // 3)
    y = np.zeros(S * J); y[np.arange(S) * J + rng.integers(0, J, S)] = 1
    df = pd.DataFrame(X_, columns=["a", "b"]); df["entered"] = y; df["stratum"] = st; df["cidx"] = cid; df["field"] = 11
    m = M.model(df, ["a", "b"])
    u = np.unique(cid); cnt = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)
    w = cnt[np.searchsorted(u, m.sid // 100)]
    rw = m.fit(w=w)
    # explicit duplication with relabelled strata (h2_exp6.boot_coef convention)
    parts = []
    for c in u:
        for rep in range(int(cnt[c])):
            d = df[df.cidx == c].copy(); d["stratum"] = d.stratum * 10000 + rep; parts.append(d)
    dd = pd.concat(parts)
    rd = CLogit(dd[["a", "b"]].to_numpy(), dd.entered.to_numpy(), dd.stratum.to_numpy()).fit()
    assert np.abs(rw["coef"] - rd["coef"]).max() < 1e-5, (rw["coef"], rd["coef"])
    return {}


@check("5_permutation_keeps_size_footprint_pool")
def _():
    rng = np.random.default_rng(6)
    P = rng.random((500, 26)) < 0.3
    RET = P & (rng.random((500, 26)) < 0.5)
    nret = RET.sum(1)
    for _ in range(20):
        Mk = AN.perm_masks(P, nret, rng)
        assert (Mk.sum(1) == nret).all()
        assert not (Mk & ~P).any()
    return {}


@check("6_rewire_preserves_degree_and_weights")
def _():
    bb = X.load_backbone()
    phi = bb["phi"]
    P = H2.rewire(phi, np.random.default_rng(7))
    deg = lambda A: (A > 0).sum(0)  # noqa: E731
    assert (np.sort(deg(P)) == np.sort(deg(phi))).all() and (deg(P) == deg(phi)).all()
    w1 = np.sort(phi[np.triu_indices(26, 1)]); w2 = np.sort(P[np.triu_indices(26, 1)])
    assert np.allclose(w1, w2)
    return {"edges": int((np.triu(phi, 1) > 0).sum())}


@check("7_crossed_offset_v1_equals_unweighted")
def _():
    rng = np.random.default_rng(8)
    S, J = 400, 7
    X_ = rng.normal(size=(S * J, 2)); st = np.repeat(np.arange(S), J)
    y = np.zeros(S * J); y[np.arange(S) * J + rng.integers(0, J, S)] = 1
    a = M.FastCLogit(X_, y, st).fit()
    b = M.FastCLogit(X_, y, st, offset=np.log(np.ones(S * J))).fit(w=np.ones(S))
    assert np.abs(a["coef"] - b["coef"]).max() < 1e-12
    return {}


@check("8_seal_guard")
def _():
    tmp = ROOT / "tests" / "_seal_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "logs").mkdir(parents=True); (tmp / "results").mkdir(); (tmp / "lib").mkdir()
    (tmp / "method.py").write_text("x = 1\n")
    old = (seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE)
    seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE = tmp, tmp / "results/frozen_spec.json", tmp / "logs/seal.log", tmp / "logs/unseal.log", ["method.py"]
    try:
        try:
            seal.unseal(); raise AssertionError("unseal before freeze did not raise")
        except seal.SealedError:
            pass
        seal.freeze({"a": 1}, None)
        (tmp / "method.py").write_text("x = 2\n")
        try:
            seal.unseal(); raise AssertionError("code edit did not raise")
        except seal.SealedError:
            pass
        (tmp / "method.py").write_text("x = 1\n")
        seal.unseal()
        try:
            seal.unseal(); raise AssertionError("second unseal did not raise")
        except seal.SealedError:
            pass
    finally:
        seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE = old
        shutil.rmtree(tmp, ignore_errors=True)
    return {}


if __name__ == "__main__":
    out = ROOT / "results" / "unit_tests_T0.json"
    out.write_text(json.dumps({"all_pass": all(v["pass"] for v in RESULTS.values()), "tests": RESULTS}, indent=1))
    print("ALL PASS" if all(v["pass"] for v in RESULTS.values()) else "SOME FAILED")
    sys.exit(0 if all(v["pass"] for v in RESULTS.values()) else 1)
