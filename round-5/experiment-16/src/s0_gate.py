#!/usr/bin/env python3
"""S0 gate T0: (a) recompute the six HOME components with the copied EXP10 lib/ego.concept_core (n_null=0, seed=0,
compute_btw=False) for 300 random EXP5 concepts (seed 1) and ALL COH1517 concepts and compare with EXP10's
ego_open_*.parquet __home columns (max |diff| <= 1e-9); (b) OPEN_home from the frozen constants == the EXP10 frames;
(c) ladder.psp_df on analysis_cohort reproduces the published cohort R2 numbers (<= 1e-6).
Writes results/gate_t0.json."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA_IN, RES, jdump, setup_logger
from jobs import build_home_cache

COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def _init() -> None:
    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())


def core6_batch(items: list) -> list:
    import ego
    out = []
    for key, name, al, t0, works in items:
        t = time.time()
        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)
        out.append((key, {k: float(r[k]) for k in COMPONENTS}, time.time() - t))
    return out


def maxdiff(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    both_nan = np.isnan(a) & np.isnan(b)
    mism = np.isnan(a) ^ np.isnan(b)
    d = np.where(both_nan | mism, 0, np.abs(a - b))
    return float(np.nanmax(d)) if len(d) else 0.0, int(mism.sum())


def main() -> None:
    logger = setup_logger("s0_gate")
    cache = build_home_cache()
    logger.info(f"home cache: {len(cache)} concepts")
    spec = json.loads((DATA_IN.parent / "results/frozen_spec.json").read_text())
    rng = np.random.default_rng(1)
    exp5_keys = sorted(k for k in cache if k[0] == "exp5")
    pick = [exp5_keys[i] for i in rng.choice(len(exp5_keys), 300, replace=False)]
    coh_keys = sorted(k for k in cache if k[0] == "cohort")
    items = [(k, cache[k]["name"], cache[k]["aliases"], cache[k]["t0"], cache[k]["works"]) for k in pick + coh_keys]
    chunks = [items[i::4] for i in range(4)]
    t = time.time()
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        res = [r for part in ex.map(core6_batch, chunks) for r in part]
    logger.info(f"T0a recompute {len(res)} concepts in {time.time()-t:.1f}s; "
                f"median {np.median([r[2] for r in res])*1e3:.1f} ms/call")
    rec = pd.DataFrame([{"frame": k[0], "ci": k[1], **v} for k, v, _ in res])
    out: dict = {"T0a": {}, "T0b": {}, "T0c": {}}
    for frame, f in (("exp5", "ego_open_exp5.parquet"), ("cohort", "ego_open_cohort.parquet")):
        ref = pd.read_parquet(DATA_IN / f).set_index("ci")
        mine = rec[rec.frame == frame].set_index("ci")
        ref = ref.loc[mine.index]
        per = {}
        for k in COMPONENTS:
            per[k] = maxdiff(mine[k].to_numpy(float), ref[f"{k}__home"].to_numpy(float))
        out["T0a"][frame] = {"n": int(len(mine)), "max_abs_diff": {k: v[0] for k, v in per.items()},
                             "nan_mismatch": {k: v[1] for k, v in per.items()},
                             "pass": bool(all(v[0] <= 1e-9 and v[1] == 0 for v in per.values()))}
        logger.info(f"T0a {frame}: {out['T0a'][frame]}")
    # (b) OPEN_home from the frozen constants
    from ladder import open_score, psp_df
    const = spec["open_constants"]["home"]
    for nm, f in (("exp5", "features_exp5_open.parquet"), ("cohort", "analysis_cohort.parquet")):
        d = pd.read_parquet(DATA_IN / f)
        o, _ = open_score(d, "home", const)
        md, mm = maxdiff(o, d.OPEN_home.to_numpy(float))
        out["T0b"][nm] = {"max_abs_diff": md, "nan_mismatch": mm, "pass": bool(md <= 1e-9 and mm == 0)}
        logger.info(f"T0b {nm}: {out['T0b'][nm]}")
    # (c) published cohort numbers
    cr = json.loads((DATA_IN.parent / "results/cohort_result.json").read_text())
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet")
    targets = [("OPEN_home", cr["primary"]["OPEN_home|O2r_m50|R2"]),
               ("NOV_res__home", cr["components"]["NOV_res__home|O2r_m50|R2"]),
               ("edge_persistence__home", cr["components"]["edge_persistence__home|O2r_m50|R2"])]
    for x, ref in targets:
        r = psp_df(ac, x, "O2r_m50", "R2", 50, 20260929)
        out["T0c"][x] = {"mine": r["rho"], "published": ref["rho"], "n_mine": r["n"], "n_published": ref["n"],
                         "abs_diff": abs(r["rho"] - ref["rho"]), "pass": bool(abs(r["rho"] - ref["rho"]) <= 1e-6)}
        logger.info(f"T0c {x}: {out['T0c'][x]}")
    out["pass"] = bool(all(v["pass"] for s in ("T0a", "T0b", "T0c") for v in out[s].values()))
    out["timing_ms_per_call_median"] = float(np.median([r[2] for r in res]) * 1e3)
    jdump(out, RES / "gate_t0.json")
    logger.info(f"GATE T0 pass = {out['pass']}")


if __name__ == "__main__":
    main()
