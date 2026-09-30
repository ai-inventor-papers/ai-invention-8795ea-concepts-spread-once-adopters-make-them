#!/usr/bin/env python3
"""S5 POWER FOR FRAME N (simulation from selection data).

Targets theta (per index x rung R3 / R5):
  T1 disattenuated POOLED estimate (true scale) -> observed Frame-N scale = T1 x sqrt(SB_x(mix) x rel_y)
  T2 COH1517 raw estimate (observed scale; scenario S_B attenuated by sqrt(SB_x(S_B) / SB_x(S_A)))
  T3 half the POOLED raw estimate (EXP10 convention; same scenario scaling as T2)
Indices: OPEN_home, NOVCHURN_raw, and NOVCHURN_exc unless the verdict is CHURN_THIN.
Scenarios: S_A = EXP5 n_home_early mix (>= 10); S_B = pessimistic, n-bin weights shifted one bin down (sampling
importance-reweighted within agroup). Draws: n concepts resampled with replacement from POOLED, stratified by agroup
(EXP5 mix); psp at R3 and R5 for every index on the same draw; shifted by (target - full-sample estimate);
SE = infl / sqrt(n - k - 3) with infl = bootstrap SE_z / analytic SE on COH1517; pass iff atanh(est) - 1.96 SE > 0.
-> results/power_frame_n.json, figures/power_curves.png"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import FIGS, RES, jdump, setup_logger

NS = [800, 1500, 2500]
DRAWS = 1000
BINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]
BIN_KEYS = ["n10-19", "n20-49", "n50-99", "n100-inf"]


def bin_of(n: np.ndarray) -> np.ndarray:
    return np.digitize(n, [20, 50, 100])


def sim_task(args: tuple) -> dict:
    import warnings
    warnings.simplefilter("ignore", RuntimeWarning)
    from rq1stats import psp_point
    from tables import design, load_tables
    scen, n, indices, seed = args
    T = load_tables()["POOLED"]
    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
    ex5 = T.frame == "exp5"
    mix = T[ex5].agroup.value_counts(normalize=True)
    b = bin_of(T.n_home_early.to_numpy())
    wA = np.bincount(bin_of(T[ex5].n_home_early.to_numpy()), minlength=4) / ex5.sum()
    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]
    imp = (wB / np.where(wA > 0, wA, 1))[b] if scen == "S_B" else np.ones(len(T))
    rng = np.random.default_rng(seed)
    des = {r: design(T, r, pooled=True) for r in ("R3", "R5")}
    k = {r: des[r][0].shape[1] + des[r][1].shape[1] for r in des}
    groups = {g: np.nonzero((T.agroup == g).to_numpy())[0] for g in mix.index}
    y = T.O2r_m50.to_numpy(float)
    X = {x: T[x].to_numpy(float) for x in indices}
    est = {f"{x}|{r}": np.full(DRAWS, np.nan) for x in indices for r in des}
    neff = {f"{x}|{r}": np.full(DRAWS, np.nan) for x in indices for r in des}
    for d in range(DRAWS):
        idx = []
        for g, share in mix.items():
            m = int(round(n * share))
            p = imp[groups[g]]
            p = p / p.sum()
            idx.append(rng.choice(groups[g], m, replace=True, p=p))
        i = np.concatenate(idx)
        for r in des:
            Bm, Cm = des[r][0][i], des[r][1][i]
            keep = Cm.std(0) > 0
            Cm = Cm[:, keep]
            for x in indices:
                xv = X[x][i]
                ok = np.isfinite(xv) & np.all(np.isfinite(Bm), 1)
                if ok.sum() < 50:
                    continue
                est[f"{x}|{r}"][d] = psp_point(xv[ok], y[i][ok], Bm[ok], Cm[ok])
                neff[f"{x}|{r}"][d] = ok.sum()
    return {"scen": scen, "n": n, "est": est, "neff": neff, "k": k}


def main() -> None:
    logger = setup_logger("s8_power")
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    verdict = V["verdict"]["verdict"]
    indices = ["OPEN_home", "NOVCHURN_raw"] + ([] if verdict == "CHURN_THIN" else ["NOVCHURN_exc"])
    cells = V["cells"]["psp"]
    rel_y = rel["outcome"]["O2r_m50"]["pooled"]["SB"]
    from tables import design, load_tables
    TT = load_tables()
    T = TT["POOLED"]
    k_coh = {r: sum(m.shape[1] for m in design(TT["COH1517"], r, pooled=False)) for r in ("R3", "R5")}
    k_pool = {r: sum(m.shape[1] for m in design(T, r, pooled=True)) for r in ("R3", "R5")}
    ex5 = T[(T.frame == "exp5") & np.isfinite(T.O2r_m50)]
    wA = np.bincount(bin_of(ex5.n_home_early.to_numpy()), minlength=4) / len(ex5)
    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]

    def sb_mix(x, w):
        vals = np.array([rel["variants"][x][bk]["SB"] if rel["variants"][x][bk]["SB"] is not None else np.nan
                         for bk in BIN_KEYS], float)
        vals = np.where(np.isfinite(vals), vals, np.nanmean(vals))
        return float(np.sum(w * vals))
    targets = {}
    for x in indices:
        sbA, sbB = sb_mix(x, wA), sb_mix(x, wB)
        sb_pool = rel["variants"][x]["pooled"]["SB"]
        for r in ("R3", "R5"):
            pool = cells.get(f"POOLED|{x}|O2r_m50|{r}", {})
            coh = cells.get(f"COH1517|{x}|O2r_m50|{r}", {})
            full = pool.get("rho", math.nan)
            t1 = full / math.sqrt(max(sb_pool, 1e-6) * rel_y) if sb_pool and sb_pool > 0.05 else math.nan
            infl = math.nan
            if coh.get("se_z") and coh.get("n"):
                # analytic SE with the COH1517 rung size (k from the rung definition)
                kk = k_coh[r]
                infl = coh["se_z"] * math.sqrt(max(coh["n"] - kk - 3, 1))
            targets[f"{x}|{r}"] = {
                "full_sample_pooled": full, "SB_pooled": sb_pool, "SB_S_A": sbA, "SB_S_B": sbB, "rel_y": rel_y,
                "infl": infl,
                "S_A": {"T1": t1 * math.sqrt(sbA * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan), "T3": 0.5 * full},
                "S_B": {"T1": t1 * math.sqrt(sbB * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan) * math.sqrt(sbB / sbA) if sbA >= 0.10 else math.nan,
                        "T3": 0.5 * full * math.sqrt(sbB / sbA) if sbA >= 0.10 else math.nan},
                "note": ("index essentially unreliable (SB < 0.10): T1 undefined, S_B scaling undefined; power for "
                         "this index is not interpretable" if (sb_pool is None or sb_pool < 0.10) else ""),
                "T1_true_scale": t1}
    logger.info(f"targets: { {k: v['S_A'] for k, v in targets.items()} }")
    tasks = [(s, n, indices, 20260940 + 10 * i + j) for i, s in enumerate(("S_A", "S_B")) for j, n in enumerate(NS)]
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn")) as ex:
        sims = list(ex.map(sim_task, tasks))
    res: dict = {"label": "selection data, outcomes previously unsealed; simulated Frame-N power", "draws": DRAWS,
                 "indices": indices, "targets": targets, "scenarios": {"S_A": {"n_bin_weights": wA.tolist()},
                                                                       "S_B": {"n_bin_weights": wB.tolist()}},
                 "results": {}}
    infl_used = {}
    for sim in sims:
        s, n = sim["scen"], sim["n"]
        for tname in ("T1", "T2", "T3"):
            passes = {}
            mde = {}
            for key, e in sim["est"].items():
                tg = targets[key][s][tname]
                infl = targets[key]["infl"] if np.isfinite(targets[key]["infl"]) else 1.0
                infl_used[key] = infl
                full = targets[key]["full_sample_pooled"]
                sh = e + (tg - full)
                se = infl / np.sqrt(np.maximum(sim["neff"][key] - sim["k"][key.split("|")[1]] - 3, 1))
                zlo = np.arctanh(np.clip(sh, -0.999, 0.999)) - 1.96 * se
                passes[key] = np.where(np.isfinite(zlo), zlo > 0, False)
                mde[key] = float(np.tanh(2.8 * np.nanmedian(se)))
            nov = "NOVCHURN_raw"
            joint = passes["OPEN_home|R3"] & passes["OPEN_home|R5"] & passes[f"{nov}|R3"]
            valid = {k: bool(np.isfinite(targets[k][s][tname])) for k in passes}
            ent = {"marginal": {k: (float(v.mean()) if valid[k] else None) for k, v in passes.items()},
                   "joint_OPEN_R3_R5_NOVCHURN_R3":
                   float(joint.mean()), "MDE_r": mde,
                   "targets_observed_scale": {k: targets[k][s][tname] for k in passes}}
            if "NOVCHURN_exc|R3" in passes and valid["NOVCHURN_exc|R3"]:
                ent["joint_with_NOVCHURN_exc"] = float((passes["OPEN_home|R3"] & passes["OPEN_home|R5"] &
                                                        passes["NOVCHURN_exc|R3"]).mean())
            res["results"][f"{s}|{tname}|n{n}"] = ent
    # analytic n for 0.8 marginal power (one-sided lower bound > 0 at alpha 0.025): n = (2.8 infl / atanh t)^2 + k + 3
    n80 = {}
    for key, t in targets.items():
        kk = k_pool[key.split("|")[1]]
        for s in ("S_A", "S_B"):
            for tn in ("T1", "T2", "T3"):
                th = t[s][tn]
                n80[f"{key}|{s}|{tn}"] = (float((2.8 * infl_used.get(key, 1.0) / math.atanh(th)) ** 2 + kk + 3)
                                          if th is not None and np.isfinite(th) and th > 0 else None)
    res["n_for_80pct_marginal"] = n80
    a = res["results"]
    res["plain_language"] = (
        f"At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = "
        f"{a['S_A|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}; at n = 2500 it is "
        f"{a['S_A|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. With T2 (COH1517 raw) it is "
        f"{a['S_A|T2|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / {a['S_A|T2|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}"
        f". Pessimistic n-mix (S_B, T3): {a['S_B|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / "
        f"{a['S_B|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. The fallback O2r_m30 outcome set is not simulated "
        f"here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.")
    jdump(res, RES / "power_frame_n.json")
    logger.info(res["plain_language"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, s in zip(axes, ("S_A", "S_B")):
        for tn, ls in (("T1", "-"), ("T2", "--"), ("T3", ":")):
            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["joint_OPEN_R3_R5_NOVCHURN_R3"] for n in NS], "o" + ls, label=f"joint {tn}")
            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["marginal"]["OPEN_home|R3"] or np.nan for n in NS], "s" + ls, alpha=0.5,
                    label=f"OPEN_home R3 {tn}")
        ax.axhline(0.8, color="grey", lw=0.8)
        ax.set_xlabel("Frame-N concepts with outcome")
        ax.set_title(f"scenario {s}")
    axes[0].set_ylabel("power (lower 95% bound > 0)")
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGS / "power_curves.png", dpi=150)


if __name__ == "__main__":
    main()
