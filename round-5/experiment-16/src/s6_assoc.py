#!/usr/bin/env python3
"""S4 ASSOCIATIONS (selection data, outcomes previously unsealed): partial Spearman given the EXP10 rung ladder for raw
and clean variants per body and POOLED, paired clean-vs-raw bootstraps (diff and retention ratio), per-group DL,
disattenuation, planted-association checks (PC3), and the mechanical evaluation of P1-P3 and the VERDICT.
Writes results/clean_vs_raw_psp.json and data/psp_boot.npz."""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, RES, jdump, setup_logger

LABEL = "selection data, outcomes previously unsealed"
SEED = 20260930
RAW = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "NOVCHURN_raw", "OPEN_home"]
CLEAN = ["NOV_res_rare5", "NOV_res_rare10", "NOV_res_rare20", "edge_persistence_rare5", "edge_persistence_rare10",
         "edge_persistence_rare20", "ego_density_W3_rare10", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_rare20",
         "NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "NOV_res_zperm", "edge_persistence_zperm",
         "NOVCHURN_exc", "NOVCHURN_zperm", "EP_chao", "NOVCHURN_chao", "z_dens_cfg", "z_dens_k", "z_pers_cfg",
         "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean", "OPEN_home_exc", "edge_persistence_nullmean"]
NEG = {"edge_persistence__raw", "ego_density_W3__raw", "edge_persistence_rare5", "edge_persistence_rare10",
       "edge_persistence_rare20", "ego_density_W3_rare10", "edge_persistence_exc", "ego_density_W3_exc",
       "edge_persistence_zperm", "EP_chao", "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg",
       "edge_persistence_nullmean"}
PAIRS = [("NOVCHURN_exc", "NOVCHURN_raw"), ("NOVCHURN_rare5", "NOVCHURN_raw"), ("NOVCHURN_rare10", "NOVCHURN_raw"),
         ("NOVCHURN_rare20", "NOVCHURN_raw"), ("NOVCHURN_cfg", "NOVCHURN_raw"), ("NOVCHURN_chao", "NOVCHURN_raw"),
         ("NOVCHURN_zperm", "NOVCHURN_raw"), ("NOV_res_exc", "NOV_res__raw"), ("NOV_res_rare10", "NOV_res__raw"),
         ("NOV_res_zperm", "NOV_res__raw"), ("edge_persistence_exc", "edge_persistence__raw"),
         ("edge_persistence_rare10", "edge_persistence__raw"), ("z_pers_cfg", "edge_persistence__raw"),
         ("EP_chao", "edge_persistence__raw"), ("edge_persistence_zperm", "edge_persistence__raw"),
         ("excess_pers_cfg", "edge_persistence__raw"), ("z_dens_cfg", "ego_density_W3__raw"),
         ("z_dens_k", "ego_density_W3__raw"), ("ego_density_W3_exc", "ego_density_W3__raw"),
         ("OPEN_home_clean", "OPEN_home"), ("OPEN_home_exc", "OPEN_home")]
GROUP_X = ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_cfg", "NOVCHURN_rare10", "OPEN_home", "OPEN_home_clean"]
BODY_KEYS = ["DEV", "OLDHO", "COH1014", "COH1517", "POOLED"]
_T: dict = {}


def _init() -> None:
    import warnings
    warnings.simplefilter("ignore", RuntimeWarning)
    from tables import load_tables
    _T.update(load_tables())


def run_task(task: tuple) -> tuple:
    from fastpsp import paired_fast, psp_boot2_fast
    from tables import design
    kind = task[0]
    t = time.time()
    if kind == "psp":
        _, body, x, y, rung, B, sub = task
        df = _T[body]
        if sub is not None:
            df = df[df.agroup == sub].reset_index(drop=True)
        Bm, Cm = design(df, rung, body == "POOLED", drop_group=sub is not None)
        r = psp_boot2_fast(df[x].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B,
                           SEED + (101 * (1 + ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"].index(sub))
                                   if sub else 0), -1 if x in NEG else 1)
        return task, r, time.time() - t
    if kind == "pair":
        _, body, xa, xb, y, rung, B = task
        df = _T[body]
        Bm, Cm = design(df, rung, body == "POOLED")
        r = paired_fast(df[xa].to_numpy(float), df[xb].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B, SEED)
        return task, r, time.time() - t
    if kind == "planted":
        _, body, B = task
        df = _T[body]
        Bm, Cm = design(df, "R2", body == "POOLED")
        y = df["O2r_m50"].to_numpy(float)
        rr = df["O2r_resid"].to_numpy(float)
        rng = np.random.default_rng(SEED + 7)
        ok = np.isfinite(rr)
        rk = np.full(len(rr), np.nan)
        rk[ok] = stats.rankdata(rr[ok])
        sd = np.nanstd(rk)
        x = rk + rng.normal(0, 3 * sd, len(rk))
        res = {"planted": _strip(psp_boot2_fast(x, y, Bm, Cm, B, SEED))}
        pl = []
        for k in range(20):
            xs = x.copy()
            xs[ok] = rng.permutation(x[ok])
            pl.append(_strip(psp_boot2_fast(xs, y, Bm, Cm, B, SEED + k)))
        res["placebos"] = pl
        res["n_placebo_ci_excl0"] = int(sum(1 for p in pl if np.isfinite(p["rho"]) and (p["ci"][0] > 0 or p["ci"][1] < 0)))
        return task, res, time.time() - t
    raise ValueError(kind)


def _strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "boot"}


def build_tasks(B: int, B2: int) -> list:
    tasks = []
    for body in BODY_KEYS:
        for x in RAW + CLEAN:
            for rung in ("R0", "R2", "R3"):
                tasks.append(("psp", body, x, "O2r_m50", rung, B, None))
            for rung in ("R0", "R2", "R3"):
                tasks.append(("psp", body, x, "O2r_resid", rung, B2, None))
        for xa, xb in PAIRS:
            for rung in ("R2", "R3"):
                tasks.append(("pair", body, xa, xb, "O2r_m50", rung, B))
        tasks.append(("planted", body, 1000))
    for x in GROUP_X:
        for g in ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"]:
            tasks.append(("psp", "POOLED", x, "O2r_m50", "R2", B, g))
    for x in ["OPEN_home", "NOVCHURN_raw", "NOVCHURN_exc"]:
        tasks.append(("psp", "POOLED", x, "O2r_m50", "R5", B, None))
        tasks.append(("psp", "COH1517", x, "O2r_m50", "R5", B, None))
    return tasks


def cost(t: tuple) -> float:
    base = {"POOLED": 7, "DEV": 3, "COH1014": 2.5, "OLDHO": 2, "COH1517": 0.6}[t[1]]
    return base * (2 if t[0] == "pair" else 20 if t[0] == "planted" else 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--B2", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    logger = setup_logger(f"s6_assoc{a.tag}")
    tasks = build_tasks(a.B, a.B2)
    if a.limit:
        tasks = tasks[:: max(1, len(tasks) // a.limit)]
    tasks.sort(key=lambda t: -cost(t))
    logger.info(f"{len(tasks)} tasks, B = {a.B}, workers {a.workers}")
    res_psp, res_pair, res_grp, res_pl, boots = {}, {}, {}, {}, {}
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_task, t) for t in tasks]
        for i, fu in enumerate(as_completed(futs)):
            task, r, dt = fu.result()
            if task[0] == "psp":
                _, body, x, y, rung, B, sub = task
                key = f"{body}|{x}|{y}|{rung}"
                if sub is not None:
                    res_grp.setdefault(f"{x}|{y}|{rung}", {})[sub] = _strip(r)
                else:
                    if y == "O2r_m50" and len(r.get("boot", [])):
                        boots[key] = r["boot"].astype(np.float32)
                    res_psp[key] = _strip(r) | {"x": x, "y": y, "rung": rung, "body": body}
            elif task[0] == "pair":
                _, body, xa, xb, y, rung, B = task
                res_pair[f"{body}|{xa}|{xb}|{y}|{rung}"] = r
            else:
                res_pl[task[1]] = r
            if i % 50 == 0:
                el = time.time() - t0
                logger.info(f"{i+1}/{len(tasks)} done; {el/60:.1f} min; eta {el/(i+1)*(len(tasks)-i-1)/60:.1f} min")
    np.savez_compressed(DATA / f"psp_boot{a.tag}.npz", **{k.replace("|", "__"): v for k, v in boots.items()})
    out = {"label": LABEL, "B": a.B, "B_O2r_resid": a.B2, "seed": SEED, "resampling_unit": "concept",
           "psp": res_psp, "paired": res_pair, "groups_raw": res_grp, "planted_PC3": res_pl}
    jdump(out, RES / f"clean_vs_raw_psp_cells{a.tag}.json")
    logger.info(f"done in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
