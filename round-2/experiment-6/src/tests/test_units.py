"""T0 unit tests (subset that needs no scan data). Run: .venv/bin/python tests/test_units.py -> results/unit_tests_T0.json"""
import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib")); sys.path.insert(0, str(ROOT))
from lib_outcomes import onset, rarefied_richness  # noqa: E402
from matcher import build_automaton, match, norm_py  # noqa: E402
from stats_core import CLogit, dersimonian_laird, fe_ols  # noqa: E402

res = {}
rng = np.random.default_rng(0)
# matcher boundaries and plurals
A = build_automaton({0: ["in vitro"], 1: ["smart grid"], 2: ["metamaterial"]})
res["matcher"] = {
    "invitrogen_no_match": 0 not in match(A, norm_py("Invitrogen reagents")),
    "in-vitro_match": match(A, norm_py("An in-vitro study")).get(0) == 0,
    "plural_variant": match(A, norm_py("Smart grids today")).get(1) == 1,
    "plural_s": match(A, norm_py("Metamaterials for optics")).get(2) == 1}
# rarefaction vs Monte Carlo
counts = [50, 20, 10, 5, 3, 1, 1]
pool = np.repeat(np.arange(len(counts)), counts)
mc = np.mean([len(set(rng.choice(pool, 30, replace=False))) for _ in range(20000)])
res["rarefaction"] = {"exact": rarefied_richness(counts, 30), "mc": float(mc),
                      "pass": abs(rarefied_richness(counts, 30) - mc) < 0.02}
# onset
res["onset"] = {"newborn": onset({2004: 5, 2005: 25, 2006: 40, 2007: 60}) == (2005.0, True),
                "reemerging": onset({2001: 15, 2002: 18, 2003: 19, 2004: 25, 2005: 30, 2006: 30}) == (2004.0, False),
                "never": math.isnan(onset({2005: 5})[0])}
# conditional logit vs statsmodels on 300 single-event strata
from statsmodels.discrete.conditional_models import ConditionalLogit  # noqa: E402
S, K = 300, 12
X = rng.normal(size=(S * K, 3)); beta = np.array([1.0, -0.5, 0.3])
strata = np.repeat(np.arange(S), K)
y = np.zeros(S * K)
for s in range(S):
    e = X[s * K:(s + 1) * K] @ beta
    p = np.exp(e) / np.exp(e).sum()
    y[s * K + rng.choice(K, p=p)] = 1
own = CLogit(X, y, strata).fit()
sm = ConditionalLogit(y, X, groups=strata).fit(disp=0)
rel = np.abs(own["coef"] - sm.params) / np.abs(sm.params)
res["clogit_vs_statsmodels"] = {"own": own["coef"].tolist(), "statsmodels": np.asarray(sm.params).tolist(),
                                "max_rel_diff": float(rel.max()), "pass": bool(rel.max() < 0.02),
                                "se_own": own["se"].tolist(), "se_sm": np.asarray(sm.bse).tolist()}
# FE OLS recovers planted slope
n = 5000; g = rng.integers(0, 200, n); x = rng.normal(size=n) + 0.1 * g
yv = 2.0 * x + 0.05 * g + rng.normal(size=n)
r = fe_ols(yv, x[:, None], [g], g, ["x"])
res["fe_ols"] = {"b": r["coef"]["x"]["b"], "pass": abs(r["coef"]["x"]["b"] - 2) < 0.05}
dl = dersimonian_laird(np.array([0.2, 0.3, 0.25, 0.1]), np.array([0.1, 0.1, 0.1, 0.1]))
res["dersimonian_laird"] = {"b": dl["b"], "pass": abs(dl["b"] - 0.2125) < 1e-6}
res["all_pass"] = all(v.get("pass", all(v.values())) if isinstance(v, dict) else v for v in res.values())
(ROOT / "results" / "unit_tests_T0.json").write_text(json.dumps(res, indent=1, default=float))
print(json.dumps(res, indent=1, default=float))
