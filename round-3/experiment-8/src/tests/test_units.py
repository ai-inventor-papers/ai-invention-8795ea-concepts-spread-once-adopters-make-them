#!/usr/bin/env python3
"""T0 unit tests (no network). Writes results/unit_tests.json."""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
sys.path.insert(0, str(ROOT))

import numpy as np
import pandas as pd

from common import RES, jdump


def t1_states():
    from build_features import states
    NY = 28
    g = np.zeros((NY, 27))
    # field code 1 (fid 11) = home; field code 2 (fid 12): 2 works in years 0 and 1 -> entered at 1, retaining at 3
    g[0, 1] = 5
    g[0, 2] = 1; g[1, 2] = 1; g[2, 2] = 1; g[3, 2] = 1
    g[1, 3] = 2                          # fid 13 enters at year 1, then nothing -> lost at year 4
    S = states(g, home=[11])
    ok = bool(S["entered"][1, 1] and not S["entered"][0, 1])            # cum >= 2 at year 1
    ok &= bool(S["retaining"][3, 1])                                    # entered 2 yrs earlier and w3 >= 2
    ok &= bool(not S["retaining"][2, 1])                                # entered at 1 -> lag-2 not yet at 2
    ok &= bool(not S["retaining"][5, 0])                                # home never retaining
    ok &= bool(S["lost"][4, 2] and not S["lost"][3, 2])                 # no works in years 2..4 -> lost at 4
    return ok


def t2_frontier():
    phi = np.array([[0, 1.0, 0.2], [1.0, 0, 0.5], [0.2, 0.5, 0]])
    retained = np.array([False, True, False])
    cand = np.array([False, False, True])
    fp = float(phi[np.ix_(retained, cand)].mean(0).sum())
    x = np.array([[0, 2, 1], [0, 2, 0], [0, 0, 0]])  # 3 years x 3 fields; field 1 has >=2 in 2 years
    rr = int((((x >= 2).sum(0) >= 2)).sum())
    return abs(fp - 0.5) < 1e-12 and rr == 1


def t3_psp():
    from rq1stats import psp_point
    rng = np.random.default_rng(1)
    B = rng.normal(size=(400, 3))
    x = rng.normal(size=400)
    y = B @ np.array([1.0, 0.5, -0.3]) + rng.normal(size=400)
    # equality with the Pearson of rank residuals
    from scipy.stats import rankdata
    Z = np.c_[np.ones(400), rankdata(B, axis=0)]
    rx = rankdata(x) - Z @ np.linalg.lstsq(Z, rankdata(x), rcond=None)[0]
    ry = rankdata(y) - Z @ np.linalg.lstsq(Z, rankdata(y), rcond=None)[0]
    eq = abs(np.corrcoef(rx, ry)[0, 1] - psp_point(x, y, B, None)) < 1e-12
    sims = [psp_point(rng.normal(size=400), (Bb := rng.normal(size=(400, 3))) @ np.ones(3) + rng.normal(size=400),
                      Bb, None) for _ in range(200)]
    return bool(eq and abs(np.mean(sims)) < 0.01), float(np.mean(sims))


def t4_dauc():
    from rq1stats import dauc_logo
    rng = np.random.default_rng(2)
    n = 3000
    Xb = rng.normal(size=(n, 3))
    x = rng.normal(size=n)
    grp = rng.integers(0, 4, n)
    lo = Xb @ np.array([0.8, -0.5, 0.3]) + 0.5 * x - 0.5
    y = (rng.random(n) < 1 / (1 + np.exp(-lo))).astype(float)
    planted = dauc_logo(Xb, x, y, grp)[0]
    shuf = [dauc_logo(Xb, rng.permutation(x), y, grp)[0] for _ in range(20)]
    return bool(planted > 0.02 and abs(np.mean(shuf)) < 0.005), float(planted), float(np.mean(shuf))


def t5_dl():
    """metafor dat.bcg (log risk ratios): DL tau2 = 0.3088 (metafor default REML 0.313; DL published 0.3088)."""
    from rq1stats import dersimonian_laird
    tpos = np.array([4, 6, 3, 62, 33, 180, 8, 505, 29, 17, 186, 5, 27]); tneg = np.array(
        [119, 300, 228, 13536, 5036, 1361, 2537, 87886, 7470, 1699, 50448, 2493, 16886])
    cpos = np.array([11, 29, 11, 248, 47, 372, 10, 499, 45, 65, 141, 3, 29]); cneg = np.array(
        [128, 274, 209, 12619, 5761, 1079, 619, 87892, 7232, 1600, 27197, 2338, 17825])
    yi = np.log((tpos / (tpos + tneg)) / (cpos / (cpos + cneg)))
    vi = 1 / tpos - 1 / (tpos + tneg) + 1 / cpos - 1 / (cpos + cneg)
    r = dersimonian_laird(yi, np.sqrt(vi))
    return bool(abs(r["tau2"] - 0.3088) < 0.001 and abs(r["b"] - (-0.7141)) < 0.001), r["tau2"], r["b"]


def t6_seal():
    import seal
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        sp, sl, mk, sealed = d / "spec.json", d / "seal.log", d / "mark.json", d / "s.parquet"
        pd.DataFrame({"a": [1]}).to_parquet(sealed)
        try:
            seal.load_heldout(sp, sl, mk, sealed)
            return False
        except seal.SealError:
            pass
        sp.write_text("{}")
        from common import sha256_file
        sl.write_text(json.dumps({"frozen_spec_sha256": sha256_file(sp)}))
        seal.load_heldout(sp, sl, mk, sealed)
        try:
            seal.load_heldout(sp, sl, mk, sealed)
            return False
        except seal.SealError:
            return True


def t7_o5():
    from outcomes import O5_ALL_SOURCES, o5
    fr = pd.DataFrame({"concept_id": [1, 2, 3, 4], "t0": [2005, 2005, 2005, 2005]})
    ev = pd.DataFrame([
        (1, "wikipedia_en", "wikipedia_article_created", 2003, True, "same", False),   # before t0 -> not at risk
        (2, "wikipedia_en", "wikipedia_article_created", 2013, True, "same", False),   # t0+8 inclusive -> 1
        (3, "research_fronts", "research_front_listed", 2008, True, "same", False),    # ignored -> 0
        (4, "mesh", "mesh_descriptor_introduced", 2005, True, "same", False),          # MeSH needs year > t0 -> 0
    ], columns=["concept_id", "source", "event_type", "year", "year_usable", "relation", "mesh_baseline"])
    r = o5(fr, ev, ("same",), O5_ALL_SOURCES)
    y = r.y.tolist()
    return bool(np.isnan(y[0]) and y[1] == 1 and y[2] == 0 and y[3] == 0 and not r.at_risk[0])


def main():
    res = {}
    for nm, fn in [("1_states", t1_states), ("2_frontier", t2_frontier), ("3_psp", t3_psp), ("4_dauc", t4_dauc),
                   ("5_dl_bcg", t5_dl), ("6_seal_gate", t6_seal), ("7_o5_rule", t7_o5)]:
        try:
            v = fn()
            res[nm] = {"pass": bool(v[0] if isinstance(v, tuple) else v),
                       "detail": list(v[1:]) if isinstance(v, tuple) else None}
        except Exception as e:  # noqa: BLE001 -- report every failing test
            res[nm] = {"pass": False, "error": repr(e)}
    jdump(res, RES / "unit_tests.json")
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
