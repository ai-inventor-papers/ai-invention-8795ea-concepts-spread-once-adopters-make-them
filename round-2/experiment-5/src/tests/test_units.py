#!/usr/bin/env python3
"""T0 unit tests (no network, < 2 min): rarefaction, Kleinberg, matcher, onset, home rule, episode R, seal gate,
planted positive control, placebo generator. Writes results/unit_tests_T0.json. Run: .venv/bin/python tests/test_units.py"""
from __future__ import annotations

import json
import sys
import tempfile
import traceback
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import NY, RES, Y0, surf  # noqa: E402

RESULTS = {}


def test(fn):
    try:
        fn()
        RESULTS[fn.__name__] = "pass"
    except Exception as e:  # noqa: BLE001 -- a test report must survive any failure
        RESULTS[fn.__name__] = f"FAIL: {e!r}"
        traceback.print_exc()
    return fn


@test
def t_a_rarefaction_vs_mc():
    from frame import rarefied_richness
    rng = np.random.default_rng(0)
    counts = [40, 20, 10, 5, 3, 1, 1]
    pool = np.repeat(np.arange(len(counts)), counts)
    mc = np.mean([len(set(rng.choice(pool, 30, replace=False))) for _ in range(20000)])
    ex = rarefied_richness(counts, 30)
    assert abs(mc - ex) < 0.03, (mc, ex)
    assert np.isnan(rarefied_richness([5, 5], 30))


@test
def t_a2_kleinberg_spike():
    from features import kleinberg_batched
    r = [5, 5, 5, 60, 70, 5, 5]
    d = [1000] * 7
    w = kleinberg_batched(r, d)
    assert w > 0
    assert kleinberg_batched([5] * 7, d) == 0.0


def _auto(entries):
    from matcher import build_automaton
    return build_automaton(entries)


@test
def t_b_matcher():
    from common import plural_variants
    from matcher import match
    lex = [("optogenetics", 0), ("internet of things", 1), ("microrna", 2), ("graphene", 3)]
    entries = []
    for name, ci in lex:
        f = surf(name)
        entries.append((f, ci, "name_exact"))
        for v in plural_variants(f.strip()):
            entries.append((" " + v + " ", ci, "name_variant"))
    A, specs = _auto(entries)

    def m(t):
        return set(match(surf(t), t, A, specs))
    assert 0 in m("Optogenetic control of neural circuits"), "stem/singular variant"
    assert 1 in m("Internet-of-Things security: a survey")
    assert 1 in m("A study of the internet of things")
    assert 2 in m("microRNAs regulate development")
    assert 3 not in m("Polygraphene sheets"), "word-internal substring must not match"
    assert 3 in m("Graphene: a review")
    # TAVI alias dropped: an all-caps <= 5 char alias never enters the automaton
    assert "tavi" not in {e[0].strip() for e in entries}


@test
def t_c_onset():
    from panel import onset, yi
    yc = np.zeros(NY)
    for y, n in {2004: 25, 2005: 40, 2006: 80}.items():
        yc[yi(y)] = n
    t0, nb = onset(yc)
    assert t0 == 2004 and nb is True
    yc2 = yc.copy()
    yc2[yi(2002)] = 30   # re-emerging, crosses 20 in 2002 -> t0 = 2002 (excluded by 2003 <= t0 rule)
    assert onset(yc2)[0] == 2002
    yc3 = yc.copy()
    yc3[yi(2003)] = 19   # pre-period substantial (19 >= 0.25 * n(2006) = 10) -> not newborn
    yc3[yi(2006)] = 40
    assert onset(yc3) == (2004.0, False)


@test
def t_d_home_rule():
    from frame import home_rule
    from panel import yi
    V = np.zeros((NY, 27))
    V[yi(2005), 7] = 20   # CS (field 17 -> code 7)
    V[yi(2005), 12] = 10  # Eng
    h = home_rule(V, 2005)
    assert h["home"] == [17] and h["intersect40"] == 0 and h["intersect25"] == 1
    V2 = np.zeros((NY, 27))
    V2[yi(2005), 7] = 10
    V2[yi(2005), 3] = 10
    V2[yi(2006), 7] = 100  # boundary year contributes 10 proportionally
    h2 = home_rule(V2, 2005)
    assert h2["home"][0] == 17 and abs(h2["n_home"] - 30) < 1e-9
    V3 = np.zeros((NY, 27))
    for k in range(1, 6):
        V3[yi(2005), k] = 6   # 20% each -> diffuse_born
    assert home_rule(V3, 2005)["status"] == "diffuse_born"
    V4 = np.zeros((NY, 27))
    V4[yi(2005), 7] = 15
    V4[yi(2005), 13] = 15
    h4 = home_rule(V4, 2005)
    assert h4["intersect40"] == 1 and set(h4["home"]) == {17, 23}


@test
def t_e_episode_R():
    from frame import episode_outcomes, episode_rows
    from panel import yi
    V = np.zeros((NY, 27))
    V[yi(2005), 7] = 20; V[yi(2005), 12] = 4; V[yi(2007), 12] = 2   # early: CS 20, Eng 6 -> share 6/26
    V[yi(2011), 7] = 50; V[yi(2012), 12] = 10                       # outcome: Eng 10 of 60
    rows = episode_rows(0, V, 2005, [17])
    assert len(rows) == 1 and rows[0]["field"] == 22 and rows[0]["n_early"] == 6
    o = episode_outcomes(V, 2005, 22, rows[0]["share_early"])
    # share_out = 10/60 = 0.167 >= 0.5 * 6/26 = 0.115 and n_out = 10 >= 9 -> R = 1
    assert o["R"] == 1 and o["R_abs2"] == 1
    V[yi(2012), 12] = 8
    assert episode_outcomes(V, 2005, 22, rows[0]["share_early"])["R"] == 0   # n_out 8 < 9


@test
def t_f_seal_gate():
    import seal
    with tempfile.TemporaryDirectory() as d:
        spec, log = Path(d) / "spec.json", Path(d) / "seal.log"
        try:
            seal.begin_unseal(spec, log)
            raise AssertionError("no spec must raise")
        except seal.SealError:
            pass
        spec.write_text('{"a": 1}')
        log.write_text(f"t FREEZE sha256(frozen_spec.json)={seal.spec_sha(spec)}\n")
        h = seal.begin_unseal(spec, log)
        seal.mark_unsealed(h, log)
        try:
            seal.begin_unseal(spec, log)
            raise AssertionError("second unseal must raise")
        except seal.SealError:
            pass
        spec.write_text('{"a": 2}')
        try:
            seal.assert_frozen(spec, log)
            raise AssertionError("hash mismatch must raise")
        except seal.SealError:
            pass


@test
def t_g_planted_control():
    import pandas as pd
    import models
    rng = np.random.default_rng(1)
    n_c, per = 240, 6
    rows = []
    fe = rng.normal(size=26)
    for c in range(n_c):
        g = models.DEV_GROUPS[c % 4]
        for k in rng.choice(26, per, replace=False):
            x = rng.normal(size=len(models.X0))
            rows.append({"ci": c, "group": g, "field": 11 + k, **dict(zip(models.X0, x)), "gateway_j": fe[k]})
    df = pd.DataFrame(rows)
    eta = 0.5 * df[models.X0[0]] + 1.2 * df.gateway_j
    df["R"] = (rng.random(len(df)) < 1 / (1 + np.exp(-eta))).astype(int)
    sc = models.std_consts(df, models.X1)
    y, grp = df.R.to_numpy(), df.group.to_numpy()
    bs = models.boot_logo(df, {"X0": models.X0, "X1": models.X1}, sc, y, grp, 60, 5)
    ci = models.ci95([b["X1"] - b["X0"] for b in bs])
    assert ci[0] > 0, ci
    df["gateway_j"] = fe[rng.permutation(26)][df.field - 11] * 0 + rng.permutation(df.gateway_j.to_numpy())
    sc = models.std_consts(df, models.X1)
    bs = models.boot_logo(df, {"X0": models.X0, "X1": models.X1}, sc, y, grp, 60, 5)
    ci2 = models.ci95([b["X1"] - b["X0"] for b in bs])
    assert ci2[0] <= 0 <= ci2[1] or ci2[1] < 0.02, ci2


@test
def t_h_placebo_generator():
    from backbones import rewire
    rng = np.random.default_rng(2)
    n = 26
    phi = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < 0.24:
                phi[i, j] = phi[j, i] = rng.random() * 2
    new, mode = rewire(phi, 7)
    assert np.array_equal((phi > 0).sum(1), (new > 0).sum(1)), "binary degree sequence preserved"
    w0 = np.sort(phi[np.triu_indices(n, 1)][phi[np.triu_indices(n, 1)] > 0])
    w1 = np.sort(new[np.triu_indices(n, 1)][new[np.triu_indices(n, 1)] > 0])
    assert np.allclose(w0, w1), "weight multiset preserved"


if __name__ == "__main__":
    (RES / "unit_tests_T0.json").write_text(json.dumps(RESULTS, indent=1))
    print(json.dumps(RESULTS, indent=1))
    sys.exit(0 if all(v == "pass" for v in RESULTS.values()) else 1)
