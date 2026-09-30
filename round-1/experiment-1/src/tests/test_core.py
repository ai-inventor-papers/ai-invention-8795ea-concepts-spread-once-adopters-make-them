"""T0 unit tests (no API calls)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from ground import Matcher  # noqa: E402
from lineage import F, mh_lor, tables  # noqa: E402
from oa import MAX_OR, cache_key, chunks  # noqa: E402
from pool import fit_reml, predict  # noqa: E402
from s0 import rarefied_richness  # noqa: E402


def test_rarefaction_matches_monte_carlo():
    counts = [50, 30, 10, 5, 3, 1, 1]
    pool = np.repeat(np.arange(len(counts)), counts)
    rng = np.random.default_rng(0)
    for m in (10, 30):
        mc = np.mean([len(np.unique(rng.choice(pool, m, replace=False))) for _ in range(10000)])
        assert abs(mc - rarefied_richness(counts, m)) < 0.02, (m, mc, rarefied_richness(counts, m))
    assert np.isnan(rarefied_richness([5, 5], 30))


def _simulate(gamma_c: float, gamma_bg: float, rng: np.random.Generator, t0: int = 2005):
    """Stock composition shifts from 90% home to 40% home; children cite parents from the stock of t-3..t-1 with a
    field-homophily tilt gamma_c (no naturalisation when gamma_c == gamma_bg); background refs come from a fixed
    50/50 pool with tilt gamma_bg. Fields: 0 = home H, 1 = off-home j."""
    years = np.arange(t0 - 3, t0 + 5)
    home_share = np.linspace(0.9, 0.4, len(years))
    stock = {y: rng.random(400) >= home_share[i] for i, y in enumerate(years)}  # True = paper in j
    C, P, B, Y = [], [], [], []
    naive_num = naive_den = 0.0
    for y in range(t0, t0 + 5):
        st = np.concatenate([stock[y - k] for k in (1, 2, 3)])
        for child_j in rng.random(150) < 0.4:
            w = np.where(st == child_j, np.exp(gamma_c), 1.0)
            ps = rng.choice(st, 3, p=w / w.sum())
            bw = np.array([np.exp(gamma_bg) if child_j else 1.0, 1.0 if child_j else np.exp(gamma_bg)])
            bs = rng.choice([True, False], 10, p=bw / bw.sum())
            c = np.zeros(F); c[1 if child_j else 0] = 1
            p = np.zeros(F); p[1] = ps.mean(); p[0] = 1 - ps.mean()
            b = np.zeros(F); b[1] = bs.mean(); b[0] = 1 - bs.mean()
            C.append(c); P.append(p); B.append(b); Y.append(y)
            if child_j:
                naive_num += ps.mean(); naive_den += 1
    C, P, B, Y = map(np.array, (C, P, B, Y))
    h = np.zeros(F); h[0] = 1
    rho = mh_lor(tables(C, P, Y, h, t0))[1] - mh_lor(tables(C, B, Y, h, t0))[1]
    return rho, naive_num / naive_den


def test_availability_cancellation_and_recovery():
    rng = np.random.default_rng(1)
    null = [_simulate(0.5, 0.5, rng) for _ in range(200)]
    rhos = np.array([r for r, _ in null])
    assert abs(rhos.mean()) < 0.1, rhos.mean()
    eff = np.array([_simulate(0.5 + 0.35, 0.5, rng)[0] for _ in range(100)])  # tilt on both rows -> log-OR +0.7
    assert abs(eff.mean() - 0.7) < 0.15, eff.mean()


def test_naive_rate_drifts_with_stock():
    """D1: the literal off-home-only same-field rate moves with stock composition although nothing naturalises."""
    rng = np.random.default_rng(2)

    def naive(share_start):
        years = 8
        hs = np.linspace(share_start, share_start - 0.5, years)
        return np.mean([(rng.random(1000) >= hs[i]).mean() for i in range(3, years)])
    assert naive(0.95) < naive(0.7) - 0.15


def test_reml_recovers_variance_components():
    rng = np.random.default_rng(3)
    tcs, tcjs, gain = [], [], []
    for _ in range(10):
        nc, nf = 50, 3
        u = rng.normal(0, 0.4, nc)
        cidx = np.repeat(np.arange(nc), nf)
        fields = ["A", "B", "C"] * nc
        v = rng.uniform(0.02, 0.1, nc * nf)
        truth = 0.2 + u[cidx] + rng.normal(0, 0.2, nc * nf)
        y = truth + rng.normal(0, np.sqrt(v))
        fit = fit_reml(y, v, cidx, nc, fields)
        tcs.append(fit.tau_c); tcjs.append(fit.tau_cj)
        pred = np.array([predict(fit, int(cidx[k]), fields[k], k)[0] for k in range(len(y))])
        gain.append(np.mean((y - truth) ** 2) - np.mean((pred - truth) ** 2))
    assert abs(np.mean(tcs) - 0.4) < 0.15 and abs(np.mean(tcjs) - 0.2) < 0.15, (np.mean(tcs), np.mean(tcjs))
    assert np.mean(gain) > 0


def test_matcher():
    cs = Matcher(["compressed sensing", "compressive sensing"])
    assert cs.match("A compressive-sensing approach") and cs.match("Compressed Sensing for MRI")
    assert Matcher(["optogenetics"]).match("new optogenetic tools")
    notes = Matcher(["natural orifice transluminal endoscopic surgery", "NOTES"])
    assert not notes.match("we took field notes during surgery")
    assert notes.match("NOTES cholecystectomy via transluminal endoscopic access")
    assert Matcher(["long noncoding RNA", "lncRNA"]).match("lncRNAs regulate")
    assert Matcher(["severe acute respiratory syndrome", "SARS coronavirus"]).match("the SARS-coronavirus spike")
    assert not Matcher(["mashup"]).match("smashup")


def test_batching_and_key_redaction():
    xs = [f"W{i}" for i in range(137)]
    assert all(len(c) <= MAX_OR for c in chunks(xs)) and sum(map(len, chunks(xs))) == 137
    k = os.environ.get("OPENALEX_API_KEY", "dummy-test-key-not-real")
    a = cache_key("/works", {"filter": "x", "api_key": k})
    assert a == cache_key("/works", {"filter": "x"}) and k not in a
    for p in [ROOT / "logs" / "credits.csv", *(ROOT / "logs").glob("*.log"), *(ROOT / "logs").glob("*.out")]:
        if p.exists():
            assert k not in p.read_text(errors="ignore"), p
