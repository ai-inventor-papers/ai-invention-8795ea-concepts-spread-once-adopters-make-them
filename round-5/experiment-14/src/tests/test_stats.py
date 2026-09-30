"""U5-U7: statistics unit tests. U6 reproduces EXP8's published held-out psp; U7 checks the PPML / lagged-DV logic.
(U5, the V(t) check, runs inside S1 on real data: results/s1_build.json -> V_exp5.)"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

from common import B5, EXP8, RES, jload  # noqa: E402
from rq1stats import dummies, psp_point  # noqa: E402
from static_cheng import multi_boot, psp_multi  # noqa: E402


def test_u5_v_check_recorded() -> None:
    p = RES / "s1_build.json"
    if p.exists():
        v = jload(p)["V_exp5"]
        assert v["U5_share_exact"] >= 0.99 or v["V_source"] == "counts_m"


def test_u6_reproduce_exp8_psp() -> None:
    a = pd.read_parquet(EXP8 / "data/analysis_table.parquet")
    d = a[a.unit == "PHYS"]
    x, y = d.n_authors_early.to_numpy(float), d.O1c.to_numpy(float)
    B, C = d[B5].to_numpy(float), dummies(d.t0.to_numpy())
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1)
    published = 0.1251489749905933            # EXP8 results/heldout_unit_results.csv, n_authors_early|O1c|PHYS
    r1 = psp_point(x[ok], y[ok], B[ok], C[ok])
    r2 = psp_multi(x[ok][:, None], y[ok][:, None], B[ok], C[ok])[0, 0]
    assert abs(r1 - published) < 1e-10
    assert abs(r2 - published) < 1e-10


def test_u6_planted_effect() -> None:
    rng = np.random.default_rng(1)
    n = 3000
    B = rng.normal(size=(n, 5))
    y = B @ np.array([0.5, 0.3, 0, 0, 0.2]) + rng.normal(size=n)
    e = rng.normal(size=n)
    x = B[:, 0] * 0.4 - 0.105 * np.sqrt(1.0) * (y - B @ np.array([0.5, 0.3, 0, 0, 0.2])) + e
    C = dummies(rng.integers(0, 4, n))
    r = multi_boot(x[:, None], y[:, None], B, C, 300, 7)
    lo, hi = np.percentile(r["boot"][:, 0, 0], [2.5, 97.5])
    assert -0.16 < r["est"][0, 0] < -0.05 and hi < 0


def test_u7_ppml_recovers_and_lagged_dv() -> None:
    import pyfixest as pf
    rng = np.random.default_rng(3)
    n_c, T = 1500, 6
    ci = np.repeat(np.arange(n_c), T)
    year = np.tile(np.arange(T), n_c)
    x = rng.normal(size=n_c * T)
    mu = np.exp(1.0 + 0.43 * x + 0.05 * year)
    y = rng.poisson(mu)
    d = pd.DataFrame({"ci": ci, "year": year, "x": x, "y": y, "age": year})
    fit = pf.fepois("y ~ x | age + year", data=d, vcov={"CRV1": "ci"})
    lo, hi = fit.confint().loc["x"].to_numpy(float)
    assert lo < 0.43 < hi
    # X affects V(t+1) only through V(t): V(t) = Pois(exp(a + b x)), V(t+1) = Pois(V(t)+1 scaled)
    v_t = rng.poisson(np.exp(2.0 + 0.6 * x))
    v_next = rng.poisson(1.0 * (v_t + 1))
    d2 = pd.DataFrame({"ci": ci, "year": year, "age": year, "x": x, "V": v_next, "logV": np.log1p(v_t)})
    b_a1 = float(pf.fepois("V ~ x | age + year", data=d2).coef()["x"])
    b_a2 = float(pf.fepois("V ~ x + logV | age + year", data=d2).coef()["x"])
    assert b_a1 > 0.4 and abs(b_a2) < 0.1 * b_a1


def test_u7_irls_matches_pyfixest() -> None:
    import pyfixest as pf
    from panel_cheng import dummy_design, poisson_irls
    rng = np.random.default_rng(5)
    n = 4000
    d = pd.DataFrame({"ci": rng.integers(0, 800, n), "age": rng.integers(1, 8, n), "year": rng.integers(2005, 2015, n),
                      "zCONS": rng.normal(size=n)})
    d["V_next"] = rng.poisson(np.exp(1 + 0.3 * d.zCONS + 0.1 * d.age))
    X, _ = dummy_design(d, ["zCONS"], ["age", "year"])
    b = poisson_irls(X, d.V_next.to_numpy(float))[1]
    b_pf = float(pf.fepois("V_next ~ zCONS | age + year", data=d).coef()["zCONS"])
    assert abs(b - b_pf) < 1e-6
