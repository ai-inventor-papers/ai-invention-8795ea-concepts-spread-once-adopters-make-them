#!/usr/bin/env python3
"""EXPLORATORY (post-unseal, NOT part of the frozen verdict): sensitivity of the headline psp to the frame definition.
  strict_gate      concepts also kept by M2 (gpt-4.1-mini boolean gate, same rule) -> higher-precision subset
  main_frame_only  t0 <= 2014 (drops the fallback-E 2015 extension)
  min_home_20      OPEN_home / NOVCHURN_home recomputed requiring >= 20 home papers
Writes results/exploratory.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, RES, jdump, setup_logger
from laddern import psp_df

logger = setup_logger("exploratory_n")


def main() -> None:
    df = pd.read_parquet(DATA / "analysis_frame_n.parquet")
    res = json.loads((RES / "frame_n_result.json").read_text())
    prim, seed = res["primary_outcome"], 20260929
    d2 = pd.read_csv(DATA / "gate_m2.csv")
    d2["keep_m2"] = d2.specific.astype(bool) & (d2.sense_share >= 0.9) & (d2.generic == 0)
    df = df.merge(d2[["ci", "keep_m2"]], on="ci", how="left")
    subsets = {"strict_gate_M2_also_keeps": df[df.keep_m2.fillna(False).astype(bool)],
               "main_frame_only_t0_le_2014": df[df.extension == 0], "all": df}
    out = {"label": "EXPLORATORY (post-unseal; not part of the frozen verdict)", "primary_outcome": prim}
    for name, d in subsets.items():
        for x in ("OPEN_home", "NOVCHURN_home"):
            for y in (prim, "O2r_m50"):
                for r in ("R3", "R5"):
                    c = psp_df(d, x, y, r, 2000, seed)
                    out[f"{name}|{x}|{y}|{r}"] = {k: c[k] for k in ("rho", "ci", "n", "p_one")}
    m = df.n_home_early >= 20
    for x in ("OPEN_home", "NOVCHURN_home"):
        d = df.copy()
        d.loc[~m, x] = np.nan
        for r in ("R3", "R5"):
            c = psp_df(d, x, prim, r, 2000, seed)
            out[f"min_home_20|{x}|{prim}|{r}"] = {k: c[k] for k in ("rho", "ci", "n", "p_one")}
    jdump(out, RES / "exploratory.json")
    for k, v in out.items():
        if isinstance(v, dict):
            logger.info(f"{k}: {v['rho']:+.3f} [{v['ci'][0]:+.3f}, {v['ci'][1]:+.3f}] n={v['n']}")


if __name__ == "__main__":
    main()
