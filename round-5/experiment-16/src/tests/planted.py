#!/usr/bin/env python3
"""Planted checks PC1 / PC2 on the fast engine (no outcomes).

PC1 stationary thin-sample simulation: for 300 real concepts (n_home_early >= 10, seed 21) the W1..W3 home papers are
    re-drawn with replacement from the concept's own POOLED W1..W3 papers at the real yearly counts (PRE unchanged), so
    the true partner distribution is identical across years. Raw persistence should still depend on n (reported);
    V2 excess persistence should average ~0 (|mean| < 0.02) and be size-free (|Spearman with log n| < 0.1).
PC2 planted churn: the same synthetic concepts, but 50% of the topic slots of every W3 paper are replaced by topics
    from a concept-specific set of 10 NEW topics outside the pooled set (so they can recur and become neighbours).
    V2 excess persistence must fall (paired sign test p < 0.01).
-> results/planted_checks.json"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np
from scipy import stats

import ego
from common import RES, jdump, setup_logger
from ego_ctx import rq1_context
from fast6 import fast6, permute_labels, prep
from jobs import build_home_cache


def v2_excess(c: dict, works: list, rng, D: int = 200) -> tuple[float, float, float]:
    P = prep(c["name"], c["aliases"], c["t0"], works)
    lab = P["lab"]
    obs = fast6(P, lab[None, :])["edge_persistence"][0]
    r = fast6(P, permute_labels(lab, D, rng))["edge_persistence"]
    f = np.isfinite(r)
    if f.sum() < D // 2 or not np.isfinite(obs):
        return float(obs), float("nan"), float("nan")
    return float(obs), float(r[f].mean()), float(obs - r[f].mean())


def main() -> None:
    logger = setup_logger("planted")
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    nt = ego.C["nt"]
    cache = build_home_cache()
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= 10)
    rng = np.random.default_rng(21)
    pick = [keys[i] for i in rng.choice(len(keys), 300, replace=False)]
    rows = []
    for k in pick:
        c = cache[k]
        t0 = c["t0"]
        W = [(y, tp) for y, tp in c["works"] if t0 <= y <= t0 + 2]
        pre = [(y, tp) for y, tp in c["works"] if y < t0]
        if len(W) < 3:
            continue
        ny = {y: sum(1 for yy, _ in W if yy == y) for y in (t0, t0 + 1, t0 + 2)}
        draw = rng.integers(0, len(W), len(W))
        syn, j = [], 0
        for y in (t0, t0 + 1, t0 + 2):
            for _ in range(ny[y]):
                syn.append((y, W[draw[j]][1]))
                j += 1
        pooled = {t for _, tp in W for t in tp}
        cand = np.setdiff1d(np.arange(nt), np.fromiter(pooled, int, len(pooled)))
        newt = rng.choice(cand, 10, replace=False)
        planted = []
        for y, tp in syn:
            if y == t0 + 2 and len(tp):
                tp = tuple(int(rng.choice(newt)) if rng.random() < 0.5 else t for t in tp)
            planted.append((y, tp))
        o_s, m_s, e_s = v2_excess(c, pre + syn, rng)
        o_p, m_p, e_p = v2_excess(c, pre + planted, rng)
        rows.append({"n": c["n_home_early"], "raw_stat": o_s, "null_stat": m_s, "exc_stat": e_s, "raw_plant": o_p,
                     "null_plant": m_p, "exc_plant": e_p})
    import pandas as pd
    d = pd.DataFrame(rows)
    ln = np.log(d.n)
    ok = d.exc_stat.notna()
    r_raw = stats.spearmanr(d.raw_stat[d.raw_stat.notna()], ln[d.raw_stat.notna()])[0]
    r_exc = stats.spearmanr(d.exc_stat[ok], ln[ok])[0]
    pc1 = {"n_concepts": int(ok.sum()), "raw_spearman_log_n": float(r_raw), "excess_mean": float(d.exc_stat[ok].mean()),
           "excess_spearman_log_n": float(r_exc),
           "pass": bool(abs(d.exc_stat[ok].mean()) < 0.02 and abs(r_exc) < 0.1)}
    both = d.exc_stat.notna() & d.exc_plant.notna()
    dec = int((d.exc_plant[both] < d.exc_stat[both]).sum())
    inc = int((d.exc_plant[both] > d.exc_stat[both]).sum())
    p = float(stats.binomtest(dec, dec + inc, 0.5, alternative="greater").pvalue) if dec + inc else float("nan")
    bothr = d.raw_stat.notna() & d.raw_plant.notna()
    rdec = int((d.raw_plant[bothr] < d.raw_stat[bothr]).sum())
    rinc = int((d.raw_plant[bothr] > d.raw_stat[bothr]).sum())
    rp = float(stats.binomtest(rdec, rdec + rinc, 0.5, alternative="greater").pvalue) if rdec + rinc else float("nan")
    pc2 = {"n_pairs": int(both.sum()), "n_excess_fell": dec, "n_excess_rose": inc, "sign_test_p": p,
           "mean_change": float((d.exc_plant[both] - d.exc_stat[both]).mean()), "pass": bool(p < 0.01),
           "raw_persistence": {"n_fell": rdec, "n_rose": rinc, "sign_test_p": rp,
                               "mean_change": float((d.raw_plant[bothr] - d.raw_stat[bothr]).mean())},
           "null_mean_change": float((d.null_plant[both] - d.null_stat[both]).mean())}
    out = {"PC1_stationary": pc1, "PC2_planted_churn": pc2}
    jdump(out, RES / "planted_checks.json")
    logger.info(out)


if __name__ == "__main__":
    main()
