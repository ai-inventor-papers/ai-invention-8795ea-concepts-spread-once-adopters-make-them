#!/usr/bin/env python3
"""T0 unit tests (no network). Run: .venv/bin/python tests/test_units.py  -> results/unit_tests_T0.json"""
from __future__ import annotations

import json
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(1, str(ROOT))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.metrics import adjusted_rand_score as ARI  # noqa: E402

import d3  # noqa: E402
import decomp as DC  # noqa: E402
import typology as TY  # noqa: E402
from cases_spec import generic_flags  # noqa: E402

RES = {}


def test(name):
    def deco(f):
        try:
            out = f()
            RES[name] = {"pass": True, **(out or {})}
        except Exception as e:  # noqa: BLE001 - a test harness records every failure
            RES[name] = {"pass": False, "error": repr(e), "trace": traceback.format_exc()[-1500:]}
        print(f"{name}: {'PASS' if RES[name]['pass'] else 'FAIL'}")
        return f
    return deco


@test("a_panel_states_hand_built")
def _a():
    G = np.zeros((1, d3.NY, 27))
    k_off, k_home = 5, 3              # field slots 6 (off-home) and 4 (home)
    G[0, 10, 1 + k_off] = 1           # year 10: 1 paper (cum 1 -> not entered)
    G[0, 11, 1 + k_off] = 1           # year 11: cum 2 -> ENTERED
    G[0, 13, 1 + k_off] = 2           # year 13: entered(11) & w3(13) = 2 >= 2 -> RETAINED (2-year lag)
    G[0, 12:14, 1 + k_home] = 5       # home field: never RETAINED (home excluded)
    home = np.zeros((1, 26), bool)
    home[0, k_home] = True
    S = d3.panel_states(G, home, 2)
    assert not S["entered"][0, 10, k_off] and S["entered"][0, 11, k_off]
    assert not S["retaining"][0, 12, k_off]           # entered at 11, lag-2 not yet satisfied at 12
    assert S["retaining"][0, 13, k_off]
    assert not S["retaining"][0, :, k_home].any()
    assert S["lost"][0, 17, k_off] and not S["lost"][0, 15, k_off]   # w3(17) = 0 (years 15-17 empty)
    return {}


@test("b_decomposition_identity")
def _b():
    rng = np.random.default_rng(1)
    E2 = rng.integers(0, 8, 1000).astype(float)
    EH = E2 + rng.integers(0, 6, 1000)
    Bn = np.floor(EH * rng.random(1000))
    m = (E2 >= 1) & (Bn >= 1)
    err = np.abs(np.log(Bn[m]) - (np.log(E2[m]) + np.log(EH[m] / E2[m]) + np.log(Bn[m] / EH[m]))).max()
    assert err < 1e-9
    top = rng.random(1000) < 0.33
    bot = ~top & (rng.random(1000) < 0.5)
    for g in (top, bot):
        a, b, c = DC._factors(E2[g], EH[g], Bn[g])
        assert abs(a * b * c - Bn[g].mean()) < 1e-9
    r = DC.gap(E2, EH, Bn, top, bot)
    assert abs(r["s_E2"] + r["s_M"] + r["s_rho"] - 1) < 1e-12
    dg = DC.das_gupta(E2, EH, Bn, top, bot)
    assert abs(dg["sum_effects"] - dg["gap_Bbar"]) < 1e-9
    return {"identity_max_err": float(err)}


def _planted(which: str, seed=2, n=1500):
    rng = np.random.default_rng(seed)
    y = rng.normal(size=n)
    top = y > np.quantile(y, 2 / 3)
    E2 = rng.poisson(4, n).astype(float) + 1
    if which == "contact":
        E2 = np.where(top, rng.poisson(8, n) + 1, E2).astype(float)
    M = np.full(n, 1.5)
    EH = np.round(E2 * M)
    rho = np.where(top & (which == "retention"), 0.8, 0.4)
    Bn = np.round(EH * rho)
    return E2, EH, Bn, y


@test("c_planted_decomposition")
def _c():
    out = {}
    for which, key in (("contact", "s_contact"), ("retention", "s_ret")):
        E2, EH, Bn, y = _planted(which)
        top, bot = DC.terciles(y, None)
        r = DC.gap(E2, EH, Bn, top, bot)
        other = "s_ret" if key == "s_contact" else "s_contact"
        out[which] = {key: r[key], other: r[other]}
        assert r[key] > 0.9 and abs(r[other]) < 0.1, (which, r)
    return out


@test("d_planted_typology")
def _d():
    rng = np.random.default_rng(3)
    n, T = 600, 9
    reg = np.repeat([0, 1, 2], n // 3)
    age = np.arange(T)
    X = np.zeros((n, T, len(TY.VARS)))
    for i, r in enumerate(reg):
        if r == 0:     # fast contact, low retention
            ent = 3 * age
            ret = 0.2 * age
        elif r == 1:   # slow contact, high retention
            ent = 0.8 * age
            ret = 0.7 * age
        else:          # spike then loss
            ent = np.minimum(age, 3) * 3
            ret = np.maximum(0, 3 - np.abs(age - 3))
        X[i, :, 0] = np.gradient(ent)
        X[i, :, 1] = ent
        X[i, :, 2] = ret
        X[i, :, 3] = np.maximum(0, ent - ret) * (r == 2)
        X[i, :, 4] = ret / np.maximum(1, ent)
        X[i, :, 5] = np.gradient(ent) / np.maximum(1, ret)
        X[i, :, 6] = np.log1p(ent)
        X[i, :, 7] = 1 / (1 + ent)
        X[i, :, 8] = np.minimum(4, 1 + ret / 2)
    X += rng.normal(0, 0.15, X.shape)
    Z = TY.zapply(X, TY.zspec_fit(X))
    D = TY.dtw_matrix(Z, n_jobs=8)
    ck = TY.choose_k(D, 0, range(2, 7), 30, n_jobs=8)
    lab, _ = TY.kmed(D, 3, 0)
    hm = TY.hmm_fit(Z, 0, states=(3, 4), restarts=3)
    lh, _ = TY.kmed(TY.euclid(TY.hmm_features(hm["model"], Z)), 3, 0)
    a_dtw, a_hmm = float(ARI(reg, lab)), float(ARI(reg, lh))
    assert ck["k"] == 3, ck
    assert a_dtw >= 0.8 and a_hmm >= 0.8, (a_dtw, a_hmm)
    # pure noise must FAIL the naming rule
    Zn = rng.normal(size=(300, T, len(TY.VARS)))
    Dn = TY.dtw_matrix(Zn, n_jobs=8)
    ln, _ = TY.kmed(Dn, 3, 0)
    hn = TY.hmm_fit(Zn, 0, states=(3,), restarts=2)
    lhn, _ = TY.kmed(TY.euclid(TY.hmm_features(hn["model"], Zn)), 3, 0)
    jac = TY.hennig_jaccard(Dn, ln, 3, 0, 20, n_jobs=8)["mean_jaccard"]
    rule = TY.naming_rule(float(ARI(ln, lhn)), jac, 0.0, [0.3] * 3, 0.0, None)
    assert not rule["any_named"]
    # numba DTW equals tslearn cdist_dtw
    diff = float(np.abs(TY.dtw_matrix(Z[:60]) - TY.dtw_matrix_tslearn(Z[:60])).max())
    assert diff < 1e-9
    return {"k_chosen": ck["k"], "ari_dtw": a_dtw, "ari_hmm": a_hmm, "noise_named": rule["any_named"],
            "noise_jaccard": jac, "dtw_vs_tslearn_max_abs_diff": diff}


@test("e_open_formula")
def _e():
    import s2_open as S2
    df = pd.DataFrame({f"{k}_x": v for k, v in zip(
        ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"],
        [[1, 2, 3, 4, 5], [1, 1, 2, 2, 3], [0.1, np.nan, np.nan, 0.4, 0.5], [np.nan, 0, 0.1, np.nan, 0.2],
         [np.nan, np.nan, 0.5, 0.2, 0.1], [0.5, np.nan, 0.3, 0.2, 0.1]])})
    zc = S2.zconst(df, "_x")
    o, n = S2.open_score(df, "_x", zc)
    # hand computation for row 3 (index 3): all but NOV_res present -> 5 components
    z = lambda k, v, s: s * (v - zc[k]["mean"]) / zc[k]["sd"]  # noqa: E731
    hand = np.mean([z("new_edge_rate", 4, 1), z("n_comm_W3", 2, 1), z("participation", 0.4, 1),
                    z("ego_density_W3", 0.2, -1), z("edge_persistence", 0.2, -1)])
    assert abs(o[3] - hand) < 1e-12
    assert n.tolist() == [4, 3, 5, 5, 6] and np.isnan(o[1]) and np.isfinite(o[0])
    assert zc["ego_density_W3"]["sd"] > 0
    return {"n_components": n.tolist()}


@test("f_seal")
def _f():
    import common
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        spec, seal, mark = td / "spec.json", td / "seal.log", td / "unsealed.json"
        spec.write_text(json.dumps({"a": 1}))
        seal.write_text(json.dumps({"frozen_spec_sha256": common.sha256_file(spec)}))
        old = (common.SPEC, common.SEAL, common.MARK)
        common.SPEC, common.SEAL, common.MARK = spec, seal, mark
        try:
            SF = common.SealedFrame(pd.DataFrame({"split": ["DEV", "HELDOUT"], "O2r_resid": [1.0, 2.0]}))
            assert len(SF.dev()) == 1
            try:
                SF.all()
                raise AssertionError("held-out access before the unseal did not raise")
            except common.SealError:
                pass
            mark.write_text("{}")
            assert len(SF.all()) == 2
            spec.write_text(json.dumps({"a": 2}))           # changed spec after the seal
            try:
                SF.all()
                raise AssertionError("changed spec did not raise")
            except common.SealError:
                pass
        finally:
            common.SPEC, common.SEAL, common.MARK = old
    # the real s7 freeze refuses when the unseal marker exists (second unseal)
    import s7_seal
    if common.MARK.exists():
        try:
            s7_seal.freeze()
            raise AssertionError("second freeze/unseal did not raise")
        except common.SealError:
            pass
    return {}


@test("g_generic_filter")
def _g():
    f, why = generic_flags(["Coefficient of variation", "Exponential growth", "Optogenetics"], [0, 0, 0], [100] * 3)
    assert f.tolist() == [True, True, False], (f, why)
    return {"why": why}


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    ok = all(v["pass"] for v in RES.values())
    (ROOT / "results/unit_tests_T0.json").write_text(json.dumps({"all_pass": ok, "tests": RES}, indent=1, default=str))
    print("ALL PASS" if ok else "SOME FAILED")
    sys.exit(0 if ok else 1)
