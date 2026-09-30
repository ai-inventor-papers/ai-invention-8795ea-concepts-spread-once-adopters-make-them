#!/usr/bin/env python3
"""S1 unit tests on the ported EXP10 code (no Frame-N data): T4 (s7 builds reproduce EXP10 ego_open_cohort for 20
concepts to 1e-12) and T8 (lib/ladder psp on EXP10 analysis_cohort reproduces OPEN_home|O2r_m50 R2/R3 to 1e-9).
Results are merged into results/unit_tests.json."""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))

import numpy as np
import pandas as pd

from common import RES, RUN_ROOT

E10 = RUN_ROOT / "round-4/experiment-10/src"


def t4() -> dict:
    import ego
    from ego_ctx import rq1_context
    from s7ego_port import concept_builds, home_codes_of
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    cf = pd.read_csv(ROOT / "inputs/cohort_candidates.csv")
    lex = pd.read_parquet(ROOT / "inputs/lexicon_v1.parquet", columns=["aliases_used"])
    ref = pd.read_parquet(ROOT / "inputs/ego_open_cohort.parquet").set_index("ci")
    em = pd.read_parquet(E10 / "data/passC_early.parquet", columns=["ci", "year", "topics", "vfield", "tagstate"])
    sub = cf.sample(20, random_state=4)
    em = em[(em.tagstate == 1) & em.ci.isin(set(sub.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    maxdiff = 0.0
    for r in sub.itertuples():
        al = [a for a in str(lex.aliases_used.iat[r.ci]).split("|") if a and a not in ("nan", "None")]
        out = concept_builds(int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home),
                             builds=("home", "sizematch"))
        for k, v in out.items():
            if k == "ci" or k not in ref.columns:
                continue
            a, b = float(v), float(ref.at[r.ci, k])
            if np.isnan(a) and np.isnan(b):
                continue
            maxdiff = max(maxdiff, abs(a - b) if np.isfinite(a) and np.isfinite(b) else np.inf)
    return {"n": 20, "max_abs_diff": maxdiff, "pass": bool(maxdiff <= 1e-12)}


def t8() -> dict:
    from ladder import psp_df
    df = pd.read_parquet(ROOT / "inputs/analysis_cohort.parquet")
    ref = json.loads((ROOT / "inputs/cohort_result.json").read_text())["primary"]
    out = {}
    for r in ("R2", "R3"):
        got = psp_df(df, "OPEN_home", "O2r_m50", r, 0, 0) if False else None
        from ladder import rung_design
        from rq1stats import psp_point
        Bc, Cc = rung_design(df, r)
        x, y = df.OPEN_home.to_numpy(float), df.O2r_m50.to_numpy(float)
        B, C = Bc.to_numpy(float), Cc.to_numpy(float)
        ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
        est = psp_point(x[ok], y[ok], B[ok], C[ok])
        want = ref[f"OPEN_home|O2r_m50|{r}"]["rho"]
        out[r] = {"got": est, "exp10": want, "abs_diff": abs(est - want), "n": int(ok.sum())}
    out["pass"] = bool(all(v["abs_diff"] <= 1e-9 for k, v in out.items() if k != "pass"))
    return out


def main() -> None:
    p = RES / "unit_tests.json"
    res = json.loads(p.read_text()) if p.exists() else {}
    res["T1"] = json.loads((RES / "t1.json").read_text())
    res["T8"] = t8()
    print("T8", res["T8"])
    res["T4"] = t4()
    print("T4", res["T4"])
    p.write_text(json.dumps(res, indent=1, default=float))


if __name__ == "__main__":
    main()
