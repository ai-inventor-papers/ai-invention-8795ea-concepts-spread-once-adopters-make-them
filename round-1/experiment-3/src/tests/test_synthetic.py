#!/usr/bin/env python3
"""T0 synthetic unit tests (no network, no credits). Run: .venv/bin/python tests/test_synthetic.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import features as F  # noqa: E402
from common import rarefy  # noqa: E402
from config import RES  # noqa: E402
from screen import eval_concept, reliability  # noqa: E402

rng = np.random.default_rng(1)
report = {}


def t_rarefy():
    counts = [50, 20, 10, 5, 3, 1, 1]
    m = 30
    pool = np.repeat(np.arange(len(counts)), counts)
    sims = [len(set(rng.choice(pool, m, replace=False))) for _ in range(20000)]
    exact = rarefy(counts, m)
    ok = abs(np.mean(sims) - exact) < 0.02
    report["rarefy"] = {"exact": exact, "brute_force": float(np.mean(sims)), "pass": bool(ok)}


def t_pmi_independent():
    nt = 300
    p = rng.dirichlet(np.ones(nt) * 0.5)
    N = 1_000_000
    nbg = rng.multinomial(N, p).astype(float)
    nc = 5000
    nck = rng.multinomial(nc, nbg / nbg.sum()).astype(float)
    F.C["nt"] = nt
    pm = F.pmi(nck, nc, nbg, N)
    w = nck / nck.sum()
    wmean = float(np.nansum(w * pm))
    report["pmi_independent"] = {"weighted_mean_pmi": wmean, "pass": bool(abs(wmean) < 0.05)}


def t_dz_null():
    nt = 800
    labels = rng.integers(0, 40, nt)
    w = rng.lognormal(0, 1.5, nt)
    pool = np.arange(nt)
    zs = []
    for _ in range(200):
        M = int(rng.integers(5, 60))
        g = np.log(w) + rng.gumbel(size=nt)
        pick = np.argpartition(-g, M - 1)[:M]
        obs = len(set(labels[pick]))
        nl = F.distinct_null(pool, w, M, labels, rng, 1000)
        zs.append((obs - nl.mean()) / nl.std())
    zs = np.array(zs)
    report["D_z_null_calibration"] = {"mean": float(zs.mean()), "sd": float(zs.std()),
                                      "pass": bool(abs(zs.mean()) < 0.1 and 0.8 < zs.std() < 1.2)}


def t_f_null():
    nt = 400
    F.C["nt"] = nt
    bgp = rng.dirichlet(np.ones(nt) * 0.3)
    N = 2_000_000
    nbg = bgp * N
    mix = np.zeros(nt)
    sup = rng.choice(nt, 60, replace=False)
    mix[sup] = rng.dirichlet(np.ones(60))

    def sim(T1, T3, mix1, mix3):
        n1 = rng.multinomial(T1, mix1).astype(float)
        n3 = rng.multinomial(T3, mix3).astype(float)
        nc1, nc3 = max(1, T1 // 2), max(1, T3 // 2)
        nb1, p1 = F.neighbours(n1, nc1, nbg, N, np.zeros(nt, bool))
        nb3, p3 = F.neighbours(n3, nc3, nbg, N, np.zeros(nt, bool))
        S1, _ = F.topS(n1, p1, nb1)
        S3, _ = F.topS(n3, p3, nb3)
        pooled = n1 + n3
        pool = np.nonzero(pooled > 0)[0]
        ng = F.f_null(pooled, pool, T1, T3, nc1, nc3, nbg, N, nbg, N, rng, 500)
        return (S3 - S1) - np.nanmean(ng)
    growth = [sim(100, 1000, mix, mix) for _ in range(40)]
    # injected selectivity: in W3 the concept concentrates on its 15 most over-represented topics
    enr = np.where(mix > 0, mix / np.maximum(bgp, 1e-12), 0)
    top = np.argsort(-enr)[:15]
    mix3 = mix.copy()
    mix3[top] *= 6
    mix3 /= mix3.sum()
    sel = [sim(100, 1000, mix, mix3) for _ in range(40)]
    report["F_res_size_null"] = {"mean_F_res_10x_growth_fixed_mix": float(np.mean(growth)),
                                 "sd": float(np.std(growth)),
                                 "mean_F_res_injected_selectivity": float(np.mean(sel)),
                                 "pass": bool(abs(np.mean(growth)) < 0.1 and np.mean(sel) > 0.1)}


def t_sb():
    n = 60
    rel_half = 0.5
    true = rng.normal(size=n)
    rows = []
    for sp in range(50):
        e_sd = np.sqrt((1 - rel_half) / rel_half)
        a = true + rng.normal(scale=e_sd, size=n)
        b = true + rng.normal(scale=e_sd, size=n)
        for i in range(n):
            rows.append({"concept": f"c{i}", "split": sp, "X_A": a[i], "X_B": b[i]})
    r = reliability(pd.DataFrame(rows), "X", [f"c{i}" for i in range(n)])
    expected = 2 * rel_half / (1 + rel_half)
    report["spearman_brown"] = {"expected_full_reliability": expected, "estimated_SB_median": r["SB_median"],
                                "pass": bool(abs(r["SB_median"] - expected) < 0.1)}


def t_logo_planted():
    n = 64
    groups = np.repeat(["CS", "ENG", "BIO", "MED"], n // 4)
    X = rng.normal(size=(n, 5))
    planted = rng.normal(size=n)
    y = 0.3 * X[:, 0] + 1.0 * planted + rng.normal(scale=0.5, size=n)
    df = pd.DataFrame(X, columns=["logvol", "growth", "offhome_share", "entropy", "nfields2"])
    df["cand"] = planted
    df["O2r"] = y
    df["group"] = groups
    df["concept"] = [f"c{i}" for i in range(n)]
    r = eval_concept(df, ["cand"], ["logvol", "growth", "offhome_share", "entropy", "nfields2"], {"O2r": "cont"},
                     per_group=True)["O2r"]
    signs = [v > 0 for v in r["cand__per_group"].values()]
    report["logo_planted"] = {"delta_rho": r["cand"], "per_group": r["cand__per_group"],
                              "pass": bool(r["cand"] > 0 and all(signs))}


if __name__ == "__main__":
    for t in (t_rarefy, t_pmi_independent, t_dz_null, t_f_null, t_sb, t_logo_planted):
        t()
        print(t.__name__, json.dumps(report[list(report)[-1]], default=float))
    (RES / "unit_tests_T0.json").write_text(json.dumps(report, indent=1, default=float))
    print("ALL PASS" if all(v["pass"] for v in report.values()) else "SOME FAILED")
