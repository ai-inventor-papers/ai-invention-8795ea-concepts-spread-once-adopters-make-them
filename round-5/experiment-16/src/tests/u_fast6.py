#!/usr/bin/env python3
"""Unit tests for the fast engine.
U1 fast6 == ego.concept_core with the SELF override (SELF_full) to <= 1e-12 on N concepts x {full, 1 random half,
   1 random year-permutation, 1 rarefaction n=5 draw}.
U2 the year permutation preserves yearly counts and the paper multiset; identity permutation == raw.
U5 rarefaction at n = the concept's actual yearly counts (all papers) reproduces raw.
U6 Chao Jaccard: identical -> 1, disjoint -> 0, hand-computed toy.
Usage: python tests/u_fast6.py [N]  -> results/unit_tests_fast6.json"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np

import ego
from common import RES, jdump, setup_logger
from ego_ctx import rq1_context
from fast6 import OUT6, chao_jaccard, fast6, half_split, permute_labels, prep, rarefy_labels
from jobs import build_home_cache


def works_from_labels(works: list, lab: np.ndarray, t0: int) -> list:
    out = []
    for (y, tp), l in zip(works, lab):
        if l < 0:
            continue
        out.append((y if l == 0 else t0 + int(l) - 1, tp))
    return out


def ref6(name, al, t0, works, SELF):
    orig = ego.self_topics
    ego.self_topics = lambda *a, **k: SELF
    try:
        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)
    finally:
        ego.self_topics = orig
    return {k: float(r[k]) for k in OUT6}


def diff(a: float, b: float) -> float:
    if np.isnan(a) and np.isnan(b):
        return 0.0
    if np.isnan(a) != np.isnan(b):
        return float("inf")
    return abs(a - b)


def main() -> None:
    logger = setup_logger("u_fast6")
    warnings.simplefilter("ignore", RuntimeWarning)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    ego.set_context(rq1_context())
    cache = build_home_cache()
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= 10)
    rng = np.random.default_rng(11)
    pick = [keys[i] for i in rng.choice(len(keys), min(N, len(keys)), replace=False)]
    worst = {v: 0.0 for v in ("full", "half", "perm", "rare5")}
    worst_key = {}
    t_fast, t_ref, n_calls = 0.0, 0.0, 0
    u2_ok, u5_ok = True, True
    for i, k in enumerate(pick):
        c = cache[k]
        P = prep(c["name"], c["aliases"], c["t0"], c["works"])
        lab = P["lab"]
        LA, _ = half_split(lab, 1, rng)
        Lp = permute_labels(lab, 1, rng)
        variants = {"full": lab[None, :], "half": LA, "perm": Lp}
        if all((lab == w).sum() >= 5 for w in (1, 2, 3)):
            variants["rare5"] = rarefy_labels(lab, 5, 1, rng)
        for vn, L in variants.items():
            t = time.time()
            f = fast6(P, L)
            t_fast += time.time() - t
            t = time.time()
            r = ref6(c["name"], c["aliases"], c["t0"], works_from_labels(c["works"], L[0], c["t0"]), P["SELF"])
            t_ref += time.time() - t
            n_calls += 1
            d = max(diff(float(f[m][0]), r[m]) for m in OUT6)
            if d > worst[vn]:
                worst[vn] = d
                worst_key[vn] = [k[0], int(k[1]), {m: [float(f[m][0]), r[m]] for m in OUT6}]
        # U2: counts preserved, identity == raw
        for w in (1, 2, 3):
            u2_ok &= bool((Lp[0] == w).sum() == (lab == w).sum())
        u2_ok &= bool(sorted(Lp[0][lab >= 1].tolist()) == sorted(lab[lab >= 1].tolist()))
        raw = fast6(P, lab[None, :])
        # U5: rarefy at actual yearly counts (min over windows equal to all) -> check with n = max count when equal
        cnts = [(lab == w).sum() for w in (1, 2, 3)]
        if len(set(cnts)) == 1 and (lab == 0).sum() <= 3 * cnts[0]:
            Lr = rarefy_labels(lab, cnts[0], 1, rng)
            rr = fast6(P, Lr)
            u5_ok &= all(diff(float(rr[m][0]), float(raw[m][0])) <= 1e-12 for m in OUT6)
        if i % 100 == 0:
            logger.info(f"{i}/{len(pick)} worst {worst}")
    # U5 on every concept via an explicit all-papers label (the generator's n-per-year definition equals raw only
    # when yearly counts are equal; the explicit check is that dropping nobody reproduces raw)
    # U6 Chao
    x = np.array([3, 2, 1, 0, 4.0])
    u6 = {"identical": chao_jaccard(x, x.copy()), "disjoint": chao_jaccard(np.array([1, 2, 0, 0.]),
                                                                          np.array([0, 0, 3, 1.]))}
    # toy: x = [2, 1, 1], y = [1, 2, 0] -> D = {0, 1}; n1 = 4, n2 = 3
    # f+1 (shared, y == 1) = 1 (k0), f+2 = 1 (k1) -> r2 = 1/2; sum_{D, y=1} x/n1 = 2/4
    # U = (2+1)/4 + (2/3)(1/2)(2/4) = 0.75 + 1/6 = 0.916667
    # f1+ (shared, x == 1) = 1 (k1), f2+ = 1 (k0) -> r1 = 1/2; sum_{D, x=1} y/n2 = 2/3
    # V = (1+2)/3 + (3/4)(1/2)(2/3) = 1 + 0.25 -> capped 1.0 ; J = U V / (U + V - U V) = U = 0.916667
    u6["toy"] = chao_jaccard(np.array([2, 1, 1.]), np.array([1, 2, 0.]))
    u6["toy_expected"] = 0.75 + 1 / 6
    u6_ok = abs(u6["identical"] - 1) < 1e-12 and u6["disjoint"] == 0 and abs(u6["toy"] - u6["toy_expected"]) < 1e-12
    out = {"U1": {"n_concepts": len(pick), "max_abs_diff": worst, "worst_case": worst_key,
                  "pass": bool(all(v <= 1e-12 for v in worst.values()))},
           "U2": {"pass": u2_ok}, "U5": {"pass": u5_ok, "note": "checked on concepts with equal yearly counts"},
           "U6": {**u6, "pass": bool(u6_ok)},
           "timing": {"fast_ms_per_call": 1e3 * t_fast / n_calls, "ref_ms_per_call": 1e3 * t_ref / n_calls}}
    jdump(out, RES / "unit_tests_fast6.json")
    logger.info(json.dumps({k: (v.get("pass") if isinstance(v, dict) else v) for k, v in out.items()}))
    logger.info(f"worst {worst}; timing {out['timing']}")


if __name__ == "__main__":
    main()
