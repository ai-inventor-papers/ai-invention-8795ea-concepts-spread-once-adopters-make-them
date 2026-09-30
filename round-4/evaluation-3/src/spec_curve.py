#!/usr/bin/env python3
"""B3: specification curve for OPEN (120 composites x 4 outcomes x 4 control sets = 1,920 specs), each DL-pooled
over the held-out units with analytic Fisher-z SEs, plus a 200-draw Freedman-Lane permutation null, the headline
spec with a 2,000-draw concept bootstrap and leave-one-unit-out pooling, and a bootstrap/analytic SE calibration.

Usage: python spec_curve.py [--null 200] [--workers 12] [--mini]"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"          # 4-CPU box: one BLAS thread per process (the previous attempt died on thread exhaustion)

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats
from scipy.stats import rankdata

from common import B5, COMPONENTS, HELD4, LOGS, RES, SEED, UNITS6, assert_sealed, cat_for, dl, jdump
from data import all_composites, composite, zmat

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "spec_curve.log", rotation="30 MB", level="DEBUG")

OUTCOMES = ["O2r_m30", "O2r_m50", "O2r_resid", "O2r_resid_N"]
CONTROLS = {"C0": ([], False), "C1": ([], True), "C2": (["label_coverage_early"], True), "C3": (["CONTACT_REACH"], True)}


def basis(Z: np.ndarray) -> tuple[np.ndarray, int]:
    U, s, _ = np.linalg.svd(Z, full_matrices=False)
    r = int((s > s.max() * 1e-10).sum())
    return U[:, :r], r


def proj_out(U: np.ndarray, v: np.ndarray) -> np.ndarray:
    return v - U @ (U.T @ v)


class Cell:
    """One (unit, outcome, control) cell: base rows, mask groups, precomputed residualised composite ranks."""

    def __init__(self, d: pd.DataFrame, comps: np.ndarray, unit: str, outcome: str, ctrl: str):
        extra, t0d = CONTROLS[ctrl]
        cols = B5 + extra
        y = d[outcome].to_numpy(float)
        Bc = d[cols].to_numpy(float)
        cat = cat_for(d.t0.to_numpy(), d.group.to_numpy(), unit, t0_dummies=t0d)
        base = np.isfinite(y) & np.all(np.isfinite(Bc), 1)
        self.base = np.nonzero(base)[0]
        self.y = y[self.base]
        Zb = np.hstack([np.ones((len(self.base), 1)), rankdata(Bc[self.base], axis=0), cat[self.base]])
        self.Ub, _ = basis(Zb)
        self.fit = self.Ub @ (self.Ub.T @ self.y)
        self.res = self.y - self.fit
        C = comps[self.base]                                   # [nb, 120]
        fin = np.isfinite(C)
        keys = {}
        for j in range(C.shape[1]):
            keys.setdefault(fin[:, j].tobytes(), []).append(j)
        self.groups = []
        for kb, js in keys.items():
            m = np.frombuffer(kb, dtype=bool)
            idx = np.nonzero(m)[0]
            if len(idx) < 20:
                continue
            Z = np.hstack([np.ones((len(idx), 1)), rankdata(Bc[self.base][idx], axis=0), cat[self.base][idx]])
            U, r = basis(Z)
            X = np.column_stack([proj_out(U, rankdata(C[idx, j])) for j in js])
            nrm = np.sqrt((X ** 2).sum(0))
            nrm[nrm < 1e-12] = np.nan
            self.groups.append({"idx": idx, "js": np.array(js), "U": U, "X": X / nrm, "n": len(idx), "k": r})

    def psp(self, yv: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        r = np.full(120, np.nan)
        v = np.full(120, np.nan)
        for g in self.groups:
            yr = proj_out(g["U"], rankdata(yv[g["idx"]]))
            yr = yr / max(np.sqrt(yr @ yr), 1e-12)
            r[g["js"]] = g["X"].T @ yr
            v[g["js"]] = 1.0 / (g["n"] - g["k"] - 3)
        return r, v


def dl_vec(z: np.ndarray, v: np.ndarray) -> dict:
    """Vectorised DL over the last axis (specs x units); NaNs dropped per row."""
    ok = np.isfinite(z) & np.isfinite(v)
    w = np.where(ok, 1 / np.where(ok, v, 1), 0)
    z0 = np.where(ok, z, 0)
    k = ok.sum(-1)
    sw = w.sum(-1)
    zf = (w * z0).sum(-1) / sw
    Q = (w * (z0 - zf[..., None]) ** 2).sum(-1)
    c = sw - (w ** 2).sum(-1) / sw
    t2 = np.where((k > 1) & (c > 0), np.maximum(0, (Q - (k - 1)) / np.where(c > 0, c, 1)), 0)
    ws = np.where(ok, 1 / (np.where(ok, v, 1) + t2[..., None]), 0)
    m = (ws * z0).sum(-1) / ws.sum(-1)
    s = np.sqrt(1 / ws.sum(-1))
    I2 = np.where((Q > 0) & (k > 1), np.maximum(0, (Q - (k - 1)) / np.where(Q > 0, Q, 1)), 0)
    return {"est": np.tanh(m), "lo": np.tanh(m - 1.96 * s), "hi": np.tanh(m + 1.96 * s), "I2": I2, "k": k,
            "npos": (np.where(ok, z, 0) > 0).sum(-1), "z": m, "se": s}


def pooled_all(cells: dict, ys: dict, n_comp: int) -> dict:
    """Return pooled arrays [n_outcome*n_ctrl*120] for DL4 and DL6 given outcome vectors per cell."""
    out = {}
    R = {u: {} for u in UNITS6}
    for (u, o, c), cell in cells.items():
        R[u][(o, c)] = cell.psp(ys[(u, o, c)])
    for tag, units in (("DL4", HELD4), ("DL6", UNITS6)):
        Zs, Vs = [], []
        for o in OUTCOMES:
            for c in CONTROLS:
                r = np.column_stack([R[u][(o, c)][0] for u in units])
                v = np.column_stack([R[u][(o, c)][1] for u in units])
                Zs.append(np.arctanh(np.clip(r, -.999999, .999999))); Vs.append(v)
        out[tag] = dl_vec(np.vstack(Zs), np.vstack(Vs))
    out["unit_r"] = R
    return out


def summarise(P: dict) -> dict:
    est, lo = P["est"], P["lo"]
    return {"share_ci_gt0": float(np.mean(lo > 0)), "share_est_gt0": float(np.mean(est > 0)),
            "median": float(np.median(est)), "iqr": [float(np.percentile(est, 25)), float(np.percentile(est, 75))],
            "share_ci_lt0": float(np.mean(P["hi"] < 0))}


# ----------------------------------------------------------------------------- bootstrap workers
G: dict = {}


def _init() -> None:
    import warnings
    warnings.filterwarnings("ignore")
    sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
    G["B"] = pd.read_parquet(RES / "b_table.parquet")
    G["spec"] = json.loads((RES / "boundary_spec.json").read_text())
    G["Z"] = zmat(G["B"], G["spec"])


def job_spec_boot(args):
    from rq1stats import psp_boot
    sub, weights, outcome, ctrl, unit, nboot, seed = args
    B = G["B"]
    m = (B.unit == unit).to_numpy()
    d = B[m]
    x = composite(G["Z"][m], tuple(sub), weights, G["spec"])
    extra, t0d = CONTROLS[ctrl]
    cat = cat_for(d.t0.to_numpy(), d.group.to_numpy(), unit, t0_dummies=t0d)
    r = psp_boot(x, d[outcome].to_numpy(float), d[B5 + extra].to_numpy(float), cat, nboot, seed)
    return {"sub": list(sub), "weights": weights, "outcome": outcome, "ctrl": ctrl, "unit": unit, "n": r["n"],
            "rho": r["rho"], "ci": r["ci"], "z": r.get("z"), "se_z": r.get("se_z"), "boot": r["boot"]}


def run_pool(jobs, workers, label):
    t = time.time()
    out = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        for i, r in enumerate(ex.map(job_spec_boot, jobs, chunksize=1)):
            out.append(r)
            if (i + 1) % 50 == 0 or i + 1 == len(jobs):
                logger.info(f"{label}: {i+1}/{len(jobs)} ({time.time()-t:.0f}s)")
    return out


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--null", type=int, default=200)
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--headline_boot", type=int, default=2000)
    ap.add_argument("--calib_boot", type=int, default=1000)
    ap.add_argument("--n_calib", type=int, default=50)
    a = ap.parse_args()
    spec = assert_sealed()
    B = pd.read_parquet(RES / "b_table.parquet")
    Z = zmat(B, spec)
    comps_meta = all_composites(spec)
    Call = np.column_stack([composite(Z, c["sub"], c["weights"], spec) for c in comps_meta])
    t = time.time()
    cells, ys = {}, {}
    for u in UNITS6:
        m = (B.unit == u).to_numpy()
        d = B[m]
        for o in OUTCOMES:
            for c in CONTROLS:
                cells[(u, o, c)] = Cell(d, Call[m], u, o, c)
                ys[(u, o, c)] = cells[(u, o, c)].y
    logger.info(f"precomputed {len(cells)} cells in {time.time()-t:.1f}s; mask groups/cell "
                f"{np.mean([len(c.groups) for c in cells.values()]):.1f}")
    obs = pooled_all(cells, ys, 120)
    # spec table
    rows = []
    i = 0
    for o in OUTCOMES:
        for c in CONTROLS:
            for j, cm in enumerate(comps_meta):
                r = {"spec_id": i, "composite": cm["name"], "weights": cm["weights"], "size": cm["size"],
                     "outcome": o, "control": c}
                for comp_i, comp in enumerate(COMPONENTS):
                    r[f"has_{comp}"] = int(comp_i in cm["sub"])
                for tag in ("DL4", "DL6"):
                    P = obs[tag]
                    r.update({f"{tag}_est": P["est"][i], f"{tag}_lo": P["lo"][i], f"{tag}_hi": P["hi"][i],
                              f"{tag}_I2": P["I2"][i], f"{tag}_k": int(P["k"][i]), f"{tag}_npos": int(P["npos"][i])})
                for u in UNITS6:
                    r[f"r_{u}"] = obs["unit_r"][u][(o, c)][0][j]
                    vv = obs["unit_r"][u][(o, c)][1][j]
                    r[f"dfz_{u}"] = int(round(1 / vv)) if np.isfinite(vv) else None   # n - k - 3
                rows.append(r)
                i += 1
    S = pd.DataFrame(rows)
    S.to_csv(RES / "spec_curve_specs.csv", index=False)
    summ = {tag: summarise(obs[tag]) for tag in ("DL4", "DL6")}
    marg = {}
    for tag in ("DL4", "DL6"):
        e, lo = S[f"{tag}_est"], S[f"{tag}_lo"]
        mm = {}
        for col in ["outcome", "control", "size", "weights"]:
            mm[col] = {str(k): {"n": int(len(g)), "share_ci_gt0": float((g[f"{tag}_lo"] > 0).mean()),
                                "share_est_gt0": float((g[f"{tag}_est"] > 0).mean()),
                                "median": float(g[f"{tag}_est"].median())} for k, g in S.groupby(col)}
        mm["leave_component"] = {}
        for comp in COMPONENTS:
            for flag, g in S.groupby(f"has_{comp}"):
                mm["leave_component"][f"{comp}|{'with' if flag else 'without'}"] = {
                    "n": int(len(g)), "share_ci_gt0": float((g[f"{tag}_lo"] > 0).mean()),
                    "median": float(g[f"{tag}_est"].median())}
        single = S[(S["size"] == 1) & (S.control == "C1") & (S.outcome == "O2r_m50")]
        mm["single_components_O2r_m50_C1"] = {r.composite: {"est": r[f"{tag}_est"], "ci": [r[f"{tag}_lo"], r[f"{tag}_hi"]]}
                                              for _, r in single.iterrows()}
        marg[tag] = mm
    logger.info(f"observed: {summ}")
    # ------------------------------------------------------------ Freedman-Lane null
    rng = np.random.default_rng(SEED + 3)
    null = {"DL4": [], "DL6": []}
    t = time.time()
    for b in range(a.null):
        ysb = {}
        for key, cell in cells.items():
            ysb[key] = cell.fit + rng.permutation(cell.res)
        P = pooled_all(cells, ysb, 120)
        for tag in ("DL4", "DL6"):
            null[tag].append(summarise(P[tag]))
        if (b + 1) % 20 == 0:
            logger.info(f"null {b+1}/{a.null} ({time.time()-t:.0f}s)")
    nulls = {}
    for tag in ("DL4", "DL6"):
        nd = pd.DataFrame(null[tag])
        o = summ[tag]
        nulls[tag] = {"p_share_ci_gt0": float((1 + (nd.share_ci_gt0 >= o["share_ci_gt0"]).sum()) / (1 + len(nd))),
                      "p_median": float((1 + (nd["median"] >= o["median"]).sum()) / (1 + len(nd))),
                      "p_share_est_gt0": float((1 + (nd.share_est_gt0 >= o["share_est_gt0"]).sum()) / (1 + len(nd))),
                      "null_share_ci_gt0_mean": float(nd.share_ci_gt0.mean()),
                      "null_share_ci_gt0_q95": float(nd.share_ci_gt0.quantile(.95)),
                      "null_median_mean": float(nd["median"].mean()), "null_median_q95": float(nd["median"].quantile(.95)),
                      "null_median_q05": float(nd["median"].quantile(.05)), "n_draws": int(len(nd))}
        nd.to_csv(RES / f"spec_curve_null_{tag}.csv", index=False)
    logger.info(f"null: {nulls}")
    # ------------------------------------------------------------ headline + calibration bootstraps
    full6 = list(range(6))
    jobs = [(full6, "equal", "O2r_m50", "C1", u, a.headline_boot, SEED + 17) for u in UNITS6]
    head = run_pool(jobs, a.workers, "headline bootstrap")
    hl = {}
    for tag, units in (("DL4", HELD4), ("DL6", UNITS6)):
        hs = [h for h in head if h["unit"] in units]
        P = dl([h["z"] for h in hs], [h["se_z"] ** 2 for h in hs])
        louo = {}
        for drop in units:
            hh = [h for h in hs if h["unit"] != drop]
            q = dl([h["z"] for h in hh], [h["se_z"] ** 2 for h in hh])
            louo[drop] = {"est": q["est"], "ci": q["ci"], "I2": q["I2"]}
        hl[tag] = P | {"louo": louo}
    hl["per_unit"] = {h["unit"]: {"rho": h["rho"], "ci": h["ci"], "n": h["n"], "se_z": h["se_z"]} for h in head}
    sid = S[(S.composite == comps_meta[[k for k, c in enumerate(comps_meta) if c["size"] == 6 and c["weights"] == "equal"][0]]["name"])
            & (S.outcome == "O2r_m50") & (S.control == "C1")]
    hl["analytic_spec_row"] = sid.iloc[0].to_dict()
    # calibration: 50 random specs x 6 units, 1,000 draws
    rs = np.random.default_rng(SEED + 5)
    pick = rs.choice(len(S), a.n_calib, replace=False)
    cj = []
    for sidx in pick:
        r = S.iloc[sidx]
        cm = comps_meta[int(sidx) % 120]
        for u in UNITS6:
            cj.append((list(cm["sub"]), cm["weights"], r.outcome, r.control, u, a.calib_boot, SEED + int(sidx)))
    cal = run_pool(cj, a.workers, "calibration bootstrap")
    ratios = []
    for c in cal:
        if c["n"] and np.isfinite(c["se_z"] or np.nan):
            cm_key = (c["outcome"], c["ctrl"])
            # analytic se from the same cell
            j = [k for k, m in enumerate(comps_meta) if list(m["sub"]) == c["sub"] and m["weights"] == c["weights"]][0]
            v = obs["unit_r"][c["unit"]][cm_key][1][j]
            if np.isfinite(v):
                ratios.append(c["se_z"] / math.sqrt(v))
    for h in head:
        j = [k for k, m in enumerate(comps_meta) if m["size"] == 6 and m["weights"] == "equal"][0]
        v = obs["unit_r"][h["unit"]][("O2r_m50", "C1")][1][j]
        ratios.append(h["se_z"] / math.sqrt(v))
    ratios = np.array(ratios)
    med = float(np.median(ratios))
    calib = {"n_unit_specs": int(len(ratios)), "median_ratio_boot_over_analytic": med,
             "q25": float(np.percentile(ratios, 25)), "q75": float(np.percentile(ratios, 75)),
             "inflate_applied": bool(med > 1.2)}
    if med > 1.2:
        # re-pool with inflated variances and redo summaries (observed and null summaries both scale)
        calib["note"] = f"analytic SEs inflated by {med:.3f} (median ratio > 1.2)"
        for tag in ("DL4", "DL6"):
            P = obs[tag]
            lo, hi = np.tanh(P["z"] - 1.96 * med * P["se"]), np.tanh(P["z"] + 1.96 * med * P["se"])
            summ[tag + "_inflated"] = {"share_ci_gt0": float(np.mean(lo > 0)), "share_ci_lt0": float(np.mean(hi < 0))}
    jdump({"n_specs": int(len(S)), "summary": summ, "null": nulls, "marginals": marg, "headline": hl,
           "calibration": calib, "grid": {"outcomes": OUTCOMES, "controls": list(CONTROLS), "n_composites": 120},
           "pool_primary": "DL4 (record-comparable); DL6 alongside (plan)"}, RES / "spec_curve.json")
    logger.info(f"headline DL4 {hl['DL4']['est']:.3f} {hl['DL4']['ci']}; calib {calib}")


if __name__ == "__main__":
    main()
