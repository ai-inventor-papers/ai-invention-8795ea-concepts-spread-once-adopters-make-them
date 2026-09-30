#!/usr/bin/env python3
"""Do concepts spread from fields that KEEP them? Retained-frontier and abandonment-penalty test on concept x field
entry risk sets (conditional logit, concept-year strata), against the field-standard RCA>1 relatedness density.

Stages (in order):
  python method.py step1    EXP6 robustness: exact reproduction gate, then the nested ladder on EXP6's frame
  python method.py dev      EXP5-minus-EXP6 frame: de-duplication, DEV risk sets, every analysis on DEV, power table
  python method.py freeze   frozen_spec.json + sha256 into logs/seal.log + git commit
  python method.py heldout  held-out units scored ONCE (seal guard)
  python method.py outputs  frontier_result.json, figures, method_out.json
Environment overrides (smoke runs only): AII_NBOOT, AII_NPERM, AII_NREWIRE, AII_NPOWER, AII_NCROSS, AII_SMOKE_CONCEPTS."""
from __future__ import annotations

import json
import math
import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")  # parallelism comes from the thread map over resamples (lib/models.tmap)
import resource
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
import analysis as AN  # noqa: E402
import d3  # noqa: E402
import exp5 as X  # noqa: E402
import models as M  # noqa: E402
import seal  # noqa: E402

RES, LOGS, FIGS = ROOT / "results", ROOT / "logs", ROOT / "figures"
for _d in (RES, LOGS, FIGS):
    _d.mkdir(exist_ok=True)
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "method.log", rotation="30 MB", level="DEBUG")

SEED = 20261101
N_BOOT = int(os.environ.get("AII_NBOOT", 1000))
N_PERM = int(os.environ.get("AII_NPERM", 1000))
N_REWIRE = int(os.environ.get("AII_NREWIRE", 500))
N_REWIRE_FULL = int(os.environ.get("AII_NREWIRE_FULL", 100))
N_POWER = int(os.environ.get("AII_NPOWER", 200))
N_CROSS = int(os.environ.get("AII_NCROSS", 500))
N_UNIT_BOOT = int(os.environ.get("AII_NUNITBOOT", 500))
SMOKE = int(os.environ.get("AII_SMOKE_CONCEPTS", 0))
META5 = ["unit", "split", "group", "intersect", "weak_home", "home_med", "label_cov", "newborn_i"]
META6 = ["hgroup", "split", "group", "intersect", "weak_home", "home_med", "label_cov", "newborn_i"]
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
resource.setrlimit(resource.RLIMIT_AS, (26 * 1024**3, 26 * 1024**3))


def jdump(obj, path: Path) -> None:
    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating, float)):
            return None if not math.isfinite(float(o)) else float(o)
        if isinstance(o, np.bool_):
            return bool(o)
        if isinstance(o, np.ndarray):
            return clean(o.tolist())
        return o
    path.write_text(json.dumps(clean(obj), indent=1, default=str))


def deviation(key: str, text: str) -> None:
    p = RES / "deviations.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = text
    p.write_text(json.dumps(d, indent=1))


def to_parquet(df: pd.DataFrame, path: Path) -> None:
    d = df.copy()
    for c in d.columns:
        if d[c].dtype == np.float64:
            d[c] = d[c].astype(np.float32)
    d.to_parquet(path, index=False)


def build(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, bb: dict, horizon: int, meta: list[str], **kw) -> tuple[pd.DataFrame, dict]:
    st = d3.build_strata(frame, G, GF, horizon=horizon, **kw)
    df = d3.attach_meta(d3.covariates(st, bb["phi"], bb["gate"]), st, frame, meta)
    return df, st


def battery(tag: str, df_all: pd.DataFrame, st: dict, spec: dict, bb: dict, *, frame: pd.DataFrame, G: np.ndarray,
            GF: np.ndarray, horizon: int, meta: list[str], Gpt: np.ndarray | None, n_boot: int, full: bool = True) -> dict:
    """ladder + headline bootstraps + LPM + Guevara AUC + VIF + specificity + rebuild sensitivities."""
    t = time.time()
    rng = AN.rng_for(SEED, tag)
    prim, alls = AN.split_std(df_all, spec)
    out = {"label": tag, "resampling_unit": "concept"}
    out["ladder"] = AN.ladder_block(prim, alls)
    lad = out["ladder"]["frontier_primary_sample"]
    logger.info(f"[{tag}] ladder: " + ", ".join(f"{k} LR={v['LR']:.2f}" for k, v in lad["LR"].items()))
    logger.info(f"[{tag}] d0 in R3 = {lad['models']['R3_ret']['coef']['d0_ret_rel']:.4f}; "
                f"d0 in S_strict = {lad['models']['S_strict']['coef']['d0_ret_rel']:.4f}; "
                f"d_lost in A1 = {out['ladder']['abandonment_all_rows']['models']['A1_lost']['coef']['d_lost']:.4f}")
    out["convergence"] = {rn: {"converged": v["converged"], "max_grad": v["max_grad"],
                               "max_abs_beta": max(abs(x) for x in v["coef"].values())} for rn, v in lad["models"].items()}
    out["vif"] = AN.vif_block(prim, M.BASE + M.RIVALS_STRICT + ["d0_ret_rel", "d_lost"])
    out["lpm_concept_year_FE"] = M.lpm(prim, M.RUNGS["R3_ret"])
    out["guevara_comparable_auc"] = AN.guevara_auc(df_all, prim, lad["models"]["R3_ret"]["coef"])
    out["sparsity"] = {"share_strata_any_lost": float(alls.groupby("stratum").n_lost.max().gt(0).mean()),
                       "mean_n_lost_per_stratum": float(alls.groupby("stratum").n_lost.max().mean()),
                       "mean_n_ret_primary": float(prim.groupby("stratum").n_ret.max().mean())}
    if not full:
        return out
    out["boot"] = AN.headline_boots(prim, alls, rng, n_boot, second_seed=True)
    t2 = time.time()
    out["crossed_boot"] = {"d0_R3": M.crossed_boot(prim, M.RUNGS["R3_ret"], "d0_ret_rel", N_CROSS, rng),
                           "d_lost_A1": M.crossed_boot(alls, M.RUNGS["A1_lost"], "d_lost", N_CROSS, rng)}
    logger.info(f"[{tag}] crossed bootstrap {time.time()-t2:.0f}s: {out['crossed_boot']['d0_R3']['ci']}")
    out["specificity"] = AN.specificity(df_all, st, prim, alls, spec, bb, rng, n_boot, N_PERM, N_REWIRE, N_PERM, N_REWIRE_FULL)
    sp = out["specificity"]
    np.savez_compressed(RES / f"nulls_{tag}.npz", LR_obs=sp["a_permutation"]["LR_obs"], perm=sp["a_permutation"]["_null"],
                        perm_entoff=sp["a_permutation_secondary_all_entered_offhome"]["_null"],
                        rewire=sp["d_backbone_d0_only"]["rewire"]["_null"], label_perm=sp["d_backbone_d0_only"]["label_perm"]["_null"],
                        rewire_full=sp.get("d_backbone_full_recompute", {}).get("_lrs", np.array([])))
    t2 = time.time()
    out["specificity_rebuild"] = AN.rebuild_sens(frame, G, GF, bb, spec, horizon, meta, Gpt)
    logger.info(f"[{tag}] rebuild sensitivities {time.time()-t2:.0f}s; battery total {time.time()-t:.0f}s")
    return out


# =============================================================================== STEP 1
def stage_step1() -> None:
    t = time.time()
    bb = X.load_backbone()
    f6, Gd = X.exp6_frame()
    GF = X.exp6_GF()
    frames, Gs, dfs, sts = {}, {}, {}, {}
    for sp, mask in (("dev", f6.split == "dev"), ("heldout", f6.split != "dev")):
        fr = f6[mask].reset_index(drop=True)
        G = np.stack([Gd[int(c)] for c in fr.cidx])
        df, st = build(fr, G, GF, bb, 8, META6)
        old = pd.read_parquet(X.EXP6 / "results" / f"entry_risk_sets_{sp}.parquet")
        mm = old.merge(df, on=["cidx", "t", "field"], how="outer", indicator=True, suffixes=("_o", "_n"))
        diffs = {c: float(np.abs(mm[c + "_o"] - mm[c + "_n"]).max()) for c in
                 ["entered", "a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate", "d_lost_gate"]}
        same = bool((mm._merge == "both").all())
        logger.info(f"EXP6 {sp}: rebuilt {len(df):,} rows vs {len(old):,}; same row set {same}; max diffs {diffs}")
        assert same and max(diffs.values()) < 1e-9, "T1 reproduction gate failed (risk-set columns)"
        frames[sp], Gs[sp], dfs[sp], sts[sp] = fr, G, df, st
        dfs[sp]["_repro"] = 0
    gate_rec = {"risk_set_rows": {sp: int(len(dfs[sp])) for sp in dfs}, "columns_max_abs_diff_lt_1e-9": True}
    # EXP6 standardisation (frozen) + new covariates standardised on EXP6 DEV primary sample
    s6 = json.loads((X.EXP6 / "results" / "frozen_spec.json").read_text())["standardisation"]
    spec6 = M.make_spec(dfs["dev"][dfs["dev"].n_ret > 0], base=s6)
    prim, _ = AN.split_std(dfs["heldout"], spec6)
    r0 = M.model(prim, M.RUNGS["R0_M0"]).fit(); r1 = M.model(prim, M.RUNGS["EXP6_M1"]).fit()
    rl = M.model(prim, M.RUNGS["EXP6_M2lost"]).fit()
    LR = 2 * (r1["ll"] - r0["ll"])
    d0 = r1["coef"][-1]; dl_ = rl["coef"][-1]
    gate_rec.update({"LR_M1_vs_M0": LR, "d0_ret_rel": d0, "d_lost_gate": dl_, "targets": {"LR": 68.57, "d0": 0.2809, "d_lost_gate": -0.0632}})
    logger.info(f"T1 gate: LR={LR:.3f} d0={d0:.4f} d_lost_gate={dl_:.4f}")
    assert abs(LR - 68.5686) < 0.01 and abs(d0 - 0.2809) < 1e-3 and abs(dl_ + 0.0632) < 1e-3, "T1 reproduction gate failed (fit)"
    gate_rec["PASS"] = True
    for sp in dfs:
        dfs[sp] = dfs[sp].drop(columns="_repro")
        to_parquet(dfs[sp], RES / f"risk_sets_exp6_extended_{sp}.parquet")
    # Gpt (primary-topic field counts) exist for EXP6 frame concepts
    Gpt = {}
    for sp in ("dev", "heldout"):
        z = np.load(X.EXP6 / "scan" / f"frame_gpf_{sp}.npz")
        Gpt.update({int(c): z["g"][i] for i, c in enumerate(z["cidx"])})
    res = {"label": "ROBUSTNESS (EXP6 frame, evidence seen once)", "T1_reproduction_gate": gate_rec, "standardisation": spec6,
           "horizon": 8}
    for sp in ("dev", "heldout"):
        fr = frames[sp]
        gp = np.stack([Gpt[int(c)] for c in fr.cidx]) if all(int(c) in Gpt for c in fr.cidx) else None
        res[sp] = battery(f"exp6_{sp}", dfs[sp], sts[sp], spec6, bb, frame=fr, G=Gs[sp], GF=GF, horizon=8, meta=META6,
                          Gpt=gp, n_boot=N_BOOT, full=(sp == "heldout"))
    prim, alls = AN.split_std(dfs["heldout"], spec6)
    units = ["Physical", "LifeEnv", "Social", "Cohort"]
    res["heldout_units"] = AN.unit_fits(prim, alls, "hgroup", units, AN.rng_for(SEED, "exp6_units"), N_UNIT_BOOT)
    res["heldout_DL"] = AN.dl_block(res["heldout_units"], units)
    jdump(res, RES / "step1_exp6_robustness.json")
    logger.info(f"step1 done in {time.time()-t:.0f}s")


# =============================================================================== STEP 2 (DEV)
def exp5_inputs(splits: list[str]) -> tuple[pd.DataFrame, dict]:
    f5 = X.exp5_frame()
    f6, _ = X.exp6_frame()
    keep, rep = X.dedup(f5, f6)
    fr = keep[keep.split.isin(splits)].sort_values("cidx").reset_index(drop=True)
    if SMOKE:
        fr = fr.groupby("unit").head(SMOKE).reset_index(drop=True)
    A = X.grounded_arrays(fr.cidx.to_numpy())
    return fr, {"A": A, "overlap": rep}


def input_checks(fr: pd.DataFrame, A: dict, GF5: np.ndarray) -> dict:
    t0 = fr.t0.to_numpy()
    ev = np.array([A["N"][i, t0[i] - d3.Y0:t0[i] - d3.Y0 + 3].sum() for i in range(len(fr))])
    ev_ok = float(np.mean(np.isclose(ev, fr.early_volume.to_numpy(), atol=1e-3)))
    hm = [X.home_rule(A["V"][i], int(t0[i])) for i in range(len(fr))]
    home_ok = float(np.mean([h == hl for h, hl in zip(hm, fr.home_list)]))
    GF6 = X.exp6_GF()
    rho = [float(stats.spearmanr(GF5[y], GF6[y]).statistic) for y in range(d3.NY)]
    out = {"early_volume_agreement": ev_ok, "home_agreement": home_ok, "GF_spearman_min": min(rho),
           "GF_max_rel_diff": float(np.max(np.abs(GF5 - GF6) / np.maximum(GF6, 1))),
           "home_mismatch_cidx": [int(c) for c, h, hl in zip(fr.cidx, hm, fr.home_list) if h != hl][:50]}
    logger.info(f"input checks: {out}")
    if ev_ok < 0.95 or home_ok < 0.95:
        raise RuntimeError(f"EXP5 array re-implementation disagrees with the frame: {out}")
    out["pass_ev_995"] = ev_ok >= 0.995
    out["pass_home_99"] = home_ok >= 0.99
    return out


def state_panel(fr: pd.DataFrame, G: np.ndarray, GF: np.ndarray) -> pd.DataFrame:
    """(ci, field, year in t0-3..2022): 0 untouched, 1 entered, 2 retained, 3 lost, 4 home."""
    home = np.zeros((len(fr), 26), bool)
    for i, hl in enumerate(fr.home_list):
        for h in hl:
            home[i, h - 11] = True
    S = d3.panel_states(G, home)
    R = d3.rca_panel(S["x"], GF)
    code = np.zeros(S["x"].shape, np.int8)
    code[S["entered"]] = 1
    code[S["retaining"]] = 2
    code[S["lost"] & S["offhome"][:, None, :]] = 3
    code[np.broadcast_to(home[:, None, :], code.shape)] = 4
    C, NY, NF = code.shape
    ci, y, k = np.meshgrid(np.arange(C), np.arange(NY), np.arange(NF), indexing="ij")
    t0 = fr.t0.to_numpy()
    keep = (y + d3.Y0) >= (t0[ci] - 3)
    age = np.where(S["entered"], S["age"], -1)
    df = pd.DataFrame({"ci": fr.cidx.to_numpy()[ci[keep]].astype(np.int32), "concept_id": fr.concept_id.to_numpy()[ci[keep]].astype(np.int64),
                       "field": (k[keep] + 11).astype(np.int8), "year": (y[keep] + d3.Y0).astype(np.int16),
                       "n": S["x"][keep], "cum": S["cum"][keep], "w3": S["w3"][keep], "rca_1y": R["rca_1y"][keep],
                       "state": code[keep], "age_since_entry": age[keep].astype(np.int16)})
    return df


def stage_dev() -> None:
    t = time.time()
    bb = X.load_backbone()
    fr, inp = exp5_inputs(["DEV"])
    jdump(inp["overlap"], RES / "overlap_report.json")
    GF, gfshape = X.exp5_GF()
    A = inp["A"]
    res = {"label": "DEV (EXP5 minus EXP6; CS/Eng/BGM/Med homes, t0 2003-09)", "n_concepts": int(len(fr)),
           "input_checks": input_checks(fr, A, GF), "year_field_totals_keys": gfshape, "horizon": 10}
    df, st = build(fr, A["V"], GF, bb, 10, META5)
    res["ties_rca_1y_eq_1"] = int(st["ties_rca_1y"])
    spec5 = M.make_spec(df[df.n_ret > 0])
    res["standardisation"] = spec5
    to_parquet(df, RES / "risk_sets_exp5_minus_exp6_dev.parquet")
    sp = state_panel(fr, A["V"], GF)
    sp.to_parquet(RES / "state_panel_dev.parquet", index=False)
    logger.info(f"DEV risk sets {len(df):,} rows / {df.stratum.nunique():,} strata / {df.cidx.nunique():,} concepts; "
                f"state panel {len(sp):,} rows ({time.time()-t:.0f}s)")
    res["battery"] = battery("exp5_dev", df, st, spec5, bb, frame=fr, G=A["V"], GF=GF, horizon=10, meta=META5,
                             Gpt=A["P"], n_boot=N_BOOT, full=True)
    prim, alls = AN.split_std(df, spec5)
    # DEV home groups as pseudo-units (code path of the held-out per-unit analysis)
    res["dev_groups"] = AN.unit_fits(prim, alls, "group", X.DEV_GROUPS, AN.rng_for(SEED, "dev_groups"), min(N_UNIT_BOOT, 200))
    res["dev_groups_DL"] = AN.dl_block(res["dev_groups"], X.DEV_GROUPS)
    lad = res["battery"]["ladder"]["frontier_primary_sample"]
    res["T4_sanity"] = {"b_log_size>0": lad["models"]["R0_M0"]["coef"]["b_log_size"] > 0,
                        "c_density>0": lad["models"]["R0_M0"]["coef"]["c_density"] > 0,
                        "R0_within_auc": lad["auc_within"]["R0_M0"],
                        "R0_auc_in_[0.75,0.85]": 0.75 <= lad["auc_within"]["R0_M0"] <= 0.85}
    res["T3_shuffled_entered"] = AN.shuffled_control(prim, AN.rng_for(SEED, "shuffle"), 20)
    # power simulation at held-out unit sizes (counts from the frame only; no outcomes)
    f5 = X.exp5_frame(); f6, _ = X.exp6_frame(); keep, _ = X.dedup(f5, f6)
    sizes = keep[keep.split != "DEV"].unit.value_counts().to_dict()
    if SMOKE:
        sizes = {k: min(v, SMOKE) for k, v in sizes.items()}
    sizes["POOLED4"] = int(sum(sizes.get(u, 0) for u in HELD4))
    sizes["COHORT"] = int(sizes.get("COHORT_DEVHOME", 0) + sizes.get("COHORT_NONDEVHOME", 0))
    tp = time.time()
    res["power"] = AN.power_sim(prim, alls, {u: int(sizes[u]) for u in ["POOLED4"] + HELD4 + ["COHORT", "COHORT_DEVHOME", "COHORT_NONDEVHOME"]},
                                AN.rng_for(SEED, "power"), N_POWER, max(N_POWER // 2, 10))
    logger.info(f"power simulation {time.time()-tp:.0f}s")
    pt = res["power"]["table"]
    res["T3_planted"] = {"beta_d0_0.2_detect_pooled4": pt["POOLED4"]["d0"]["0.2"], "pass_ge_0.9": pt["POOLED4"]["d0"]["0.2"] >= 0.9,
                         "null_rejection_pooled4_alpha0.01": pt["POOLED4"]["d0"]["0"], "pass_le_0.02": pt["POOLED4"]["d0"]["0"] <= 0.02,
                         "d_lost_-0.10_power_pooled4": pt["POOLED4"]["d_lost"]["-0.1"]}
    jdump(res, RES / "step2_dev.json")
    logger.info(f"dev stage done in {time.time()-t:.0f}s")


# =============================================================================== FREEZE
VERDICT_RULES = {
    "FRONTIER_CONFIRMED_iff": [
        "(1) pooled-4 held-out d0_ret_rel in R3 > 0 with concept-clustered refit bootstrap 95% CI > 0 AND LR(R3 vs R2) p < 0.01",
        "(2) the same in S_strict (all four RCA>1 density variants + D_vol + D_vol_w3): d0 > 0, CI > 0, LR(S_strict vs S_strict0) p < 0.01",
        "(3) d0 > 0 in >= 3 of 4 held-out groups (or 3 of 3 if MATHDEC power at d=0.15 < 0.5) AND in the 2010-14 cohort",
        "(4) retained-label permutation p < 0.05 (primary pool)",
        "(5) volume-matched beta_R - beta_N > 0 with bootstrap CI > 0",
        "(6) EXP6 robustness: d0 in R3 on EXP6 held-out has concept-bootstrap CI > 0"],
    "PARTIAL": "(1) and (3) hold but (2) or (5) fail -> 'survives current RCA but not window-matched/persistence RCA' or "
               "'persistence confounded with volume'; (1),(3) hold and only (4) or (6) fail -> PARTIAL (named criterion)",
    "DISCONFIRMED": "pooled-4 CI of d0 in R3 includes 0, or the effect holds only on the EXP6 frame; "
                    "'relatedness principle unchanged' reading if R1/S_strict absorbs d0",
    "ABANDONMENT_CONFIRMED_iff": "pooled-4 held-out d_lost in A1 < 0 with concept-bootstrap CI < 0 and Holm (F3) p < 0.05; "
                                 "REJECTED if the point estimate >= 0; otherwise INCONCLUSIVE",
    "Holm_families": {"F1": ["d0 pooled-4 R3", "d0 S_strict", "d0 cohort"],
                      "F2": ["perm", "vol-matched", "dose trend", "rewire", "label-perm", "field FE"],
                      "F3": ["d_lost A1 pooled", "d_lost_short", "d_lost_long"]},
}


def git_commit(msg: str) -> str | None:
    try:
        gi = ROOT / ".gitignore"
        if not gi.exists():
            gi.write_text(".venv/\n__pycache__/\n*.pyc\n")
        subprocess.run(["git", "-C", str(ROOT), "add", "-A"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(ROOT), "-c", "user.name=AII executor", "-c", "user.email=aii@localhost", "commit", "-q",
                        "-m", msg + "\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"], check=True, capture_output=True)
        return subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.warning(f"git commit failed: {e}")
        return None


def stage_freeze() -> None:
    if (RES / "risk_sets_exp5_minus_exp6_heldout.parquet").exists():
        raise seal.SealedError("T5: held-out risk-set file exists before the freeze")
    dev = json.loads((RES / "step2_dev.json").read_text())
    f5 = X.exp5_frame(); f6, _ = X.exp6_frame(); keep, rep = X.dedup(f5, f6)
    held = keep[keep.split != "DEV"]
    pt = dev["power"]["table"]
    mathdec_counts = pt["MATHDEC"]["d0"]["0.15"] >= 0.5
    spec = {"artifact": "EXP7 retained-frontier test", "seed": SEED,
            "rungs": {k: v for k, v in M.RUNGS.items()}, "ladder": M.LADDER,
            "primary_sample": "concept-year strata with a non-empty retained set (EXP6 convention) for frontier rungs; all candidate rows for A1",
            "covariates": {"D_rca_1y": "sum_j U_j phi_jk / sum_j phi_jk with U = RCA_1y(t-1) > 1 (Hidalgo current portfolio; PRIMARY)",
                           "D_rca_w3": "U = RCA over t-3..t-1 > 1", "D_rca_cum": "U = cumulative RCA to t-1 > 1 (Guevara 2016)",
                           "D_rca_pers": "U = RCA(t-3..t-1) > 1 AND RCA(t-6..t-4) > 1", "D_vol": "share-weighted density (annual t-1)",
                           "D_vol_w3": "share-weighted density (t-3..t-1)", "d0_ret_rel": "mean_{j in RETAINED(t-1)} phi_jk",
                           "d_lost": "mean_{j in LOST(t-1) & off-home} phi_jk (unweighted)"},
            "standardisation_DEV": dev["standardisation"], "horizon": 10, "min_n": 2, "rca_rule": "RCA > 1 strict",
            "D_rca_primary": "D_rca_1y", "verdict_rules": VERDICT_RULES,
            "sign_rule": "3 of 4 groups + cohort" if mathdec_counts else "3 of 3 groups (PHYS, LIFEENV, SOC) + cohort",
            "mathdec_power_at_0.15": pt["MATHDEC"]["d0"]["0.15"], "mathdec_counts_in_sign_rule": mathdec_counts,
            "specificity": {"a": "POOL = entered(t-3) & off-home at t-1; |RET| drawn uniformly; secondary pool = entered off-home",
                            "b_bins": {"n_prev": [0, 1, "2-3", "4+"], "cum_prev": [2, "3-4", "5-9", "10+"]},
                            "c_dose_ages": [2, 3, "4+"], "d": {"n_rewire": N_REWIRE, "n_label_perm": N_PERM, "n_rewire_full": N_REWIRE_FULL}},
            "n": {"N_BOOT": N_BOOT, "N_PERM": N_PERM, "N_REWIRE": N_REWIRE, "N_CROSS": N_CROSS, "N_UNIT_BOOT": N_UNIT_BOOT, "N_POWER": N_POWER},
            "heldout_units": {u: sorted(map(int, held[held.unit == u].concept_id)) for u in sorted(held.unit.unique())},
            "heldout_unit_counts": held.unit.value_counts().to_dict(),
            "overlap_report_sha256": seal.sha(RES / "overlap_report.json"), "power_table": pt,
            "smoke": SMOKE}
    commit = git_commit("EXP7: pre-freeze snapshot (DEV analyses, frozen spec inputs)")
    h = seal.freeze(spec, commit)
    commit2 = git_commit("EXP7: frozen_spec.json + seal.log")
    logger.info(f"FROZEN: sha256={h}; git {commit} / {commit2}; sign rule: {spec['sign_rule']}")


# =============================================================================== HELD-OUT (once)
def stage_heldout(resume: str | None) -> None:
    t = time.time()
    entry = seal.unseal(resume)
    logger.info(f"UNSEALED: {entry}")
    spec = json.loads(seal.SPEC.read_text())
    std = spec["standardisation_DEV"]
    bb = X.load_backbone()
    fr, inp = exp5_inputs([s for s in X.exp5_frame().split.unique() if s != "DEV"])
    GF, _ = X.exp5_GF()
    A = inp["A"]
    # frozen unit lists must match the frame exactly
    for u, ids in spec["heldout_units"].items():
        got = sorted(map(int, fr[fr.unit == u].concept_id))
        assert got == ids, f"held-out unit {u} differs from the frozen list"
    res = {"label": "HELD-OUT (EXP5 minus EXP6), scored once with frozen DEV standardisation", "unseal": entry,
           "input_checks": input_checks(fr, A, GF), "n_concepts": fr.unit.value_counts().to_dict()}
    df, st = build(fr, A["V"], GF, bb, 10, META5)
    to_parquet(df, RES / "risk_sets_exp5_minus_exp6_heldout.parquet")
    sp = state_panel(fr, A["V"], GF)
    sp.to_parquet(RES / "state_panel_heldout.parquet", index=False)
    logger.info(f"held-out risk sets {len(df):,} rows; state panel {len(sp):,} ({time.time()-t:.0f}s)")
    # pooled-4 (primary), cohort, per unit
    p4 = df.unit.isin(HELD4).to_numpy()
    fr4 = fr[fr.unit.isin(HELD4)].reset_index(drop=True)
    st4 = d3.build_strata(fr4, A["V"][fr.unit.isin(HELD4).to_numpy()], GF, horizon=10)
    df4 = d3.attach_meta(d3.covariates(st4, bb["phi"], bb["gate"]), st4, fr4, META5)
    assert len(df4) == int(p4.sum())
    res["pooled4"] = battery("exp5_heldout_pooled4", df4, st4, std, bb, frame=fr4, G=A["V"][fr.unit.isin(HELD4).to_numpy()], GF=GF,
                             horizon=10, meta=META5, Gpt=A["P"][fr.unit.isin(HELD4).to_numpy()], n_boot=N_BOOT, full=True)
    frc = fr[fr.unit.str.startswith("COHORT")].reset_index(drop=True)
    mc = fr.unit.str.startswith("COHORT").to_numpy()
    stc = d3.build_strata(frc, A["V"][mc], GF, horizon=10)
    dfc = d3.attach_meta(d3.covariates(stc, bb["phi"], bb["gate"]), stc, frc, META5)
    res["cohort"] = battery("exp5_heldout_cohort", dfc, stc, std, bb, frame=frc, G=A["V"][mc], GF=GF, horizon=10, meta=META5,
                            Gpt=A["P"][mc], n_boot=N_BOOT, full=False)
    pc, ac = AN.split_std(dfc, std)
    res["cohort"]["boot"] = AN.headline_boots(pc, ac, AN.rng_for(SEED, "cohort_boot"), N_BOOT)
    prim, alls = AN.split_std(df, std)
    units = HELD4 + ["COHORT_DEVHOME", "COHORT_NONDEVHOME"]
    res["units"] = AN.unit_fits(prim, alls, "unit", units, AN.rng_for(SEED, "heldout_units"), N_UNIT_BOOT)
    res["DL_4groups"] = AN.dl_block(res["units"], HELD4)
    res["DL_4groups_plus_cohort_parts"] = AN.dl_block(res["units"], units)
    res["verdicts"] = verdicts(res, spec)
    jdump(res, RES / "step2_heldout.json")
    logger.info(f"VERDICTS: {json.dumps(res['verdicts'], default=str)[:2000]}")
    logger.info(f"held-out stage done in {time.time()-t:.0f}s")


def verdicts(res: dict, spec: dict) -> dict:
    p4 = res["pooled4"]
    lad = p4["ladder"]["frontier_primary_sample"]
    b = p4["boot"]
    s1 = json.loads((RES / "step1_exp6_robustness.json").read_text())
    d0 = lad["models"]["R3_ret"]["coef"]["d0_ret_rel"]
    ci = b["d0_R3"]["d0_ret_rel"]["ci"]
    lr3 = lad["LR"]["R3_ret_vs_R2_vol"]
    d0s = lad["models"]["S_strict"]["coef"]["d0_ret_rel"]
    cis = b["d0_S_strict"]["d0_ret_rel"]["ci"]
    lrs = lad["LR"]["S_strict_vs_S_strict0"]
    groups = HELD4 if spec["mathdec_counts_in_sign_rule"] else ["PHYS", "LIFEENV", "SOC"]
    need = 3
    pos = [g for g in groups if res["units"].get(g, {}).get("d0_R3", {}).get("coef", -1) > 0]
    coh = res["cohort"]["ladder"]["frontier_primary_sample"]
    coh_d0 = coh["models"]["R3_ret"]["coef"]["d0_ret_rel"]
    sp = p4["specificity"]
    perm_p = sp["a_permutation"]["p"]
    vm = sp["b_volume_matched"].get("contrast_R_minus_N", {})
    e6 = s1["heldout"]["boot"]["d0_R3"]["d0_ret_rel"]["ci"]
    c = {"1_pooled4_R3": bool(d0 > 0 and ci[0] > 0 and lr3["p"] < 0.01),
         "2_S_strict": bool(d0s > 0 and cis[0] > 0 and lrs["p"] < 0.01),
         "3_sign_rule": bool(len(pos) >= need and coh_d0 > 0),
         "4_permutation_p<0.05": bool(perm_p < 0.05),
         "5_volume_matched_CI>0": bool(vm.get("est", -1) > 0 and vm.get("ci", [-1])[0] > 0),
         "6_EXP6_R3_CI>0": bool(e6[0] > 0)}
    if all(c.values()):
        v = "CONFIRMED"
    elif ci[0] <= 0 <= ci[1] or d0 <= 0:
        v = "DISCONFIRMED" + (" (holds only on the EXP6 frame)" if c["6_EXP6_R3_CI>0"] else "")
        m1 = lad["models"]["EXP6_M1"]["coef"]["d0_ret_rel"]
        if m1 > 0 and lad["LR"]["EXP6_M1_vs_R0_M0"]["p"] < 0.01:
            v += "; relatedness principle unchanged (d0 is significant without the RCA>1/volume rivals but not with them)"
    elif c["1_pooled4_R3"] and c["3_sign_rule"]:
        fails = [k for k, ok in c.items() if not ok]
        if not c["2_S_strict"]:
            v = "PARTIAL: survives current RCA but not window-matched/persistence RCA"
        elif not c["5_volume_matched_CI>0"]:
            v = "PARTIAL: persistence confounded with volume"
        else:
            v = "PARTIAL: fails " + ", ".join(fails)
    else:
        v = "PARTIAL: fails " + ", ".join(k for k, ok in c.items() if not ok)
    # Holm families
    ab = p4["ladder"]["abandonment_all_rows"]
    dlc = ab["models"]["A1_lost"]
    z = dlc["coef"]["d_lost"] / dlc["se_concept"]["d_lost"]
    zs = ab["models"]["A1_split"]
    f1 = {"d0_pooled4_R3": lr3["p"], "d0_S_strict": lrs["p"], "d0_cohort": coh["LR"]["R3_ret_vs_R2_vol"]["p"]}
    dose = sp["c_dose"]["contrast_4p_minus_2"]
    fe = sp["g_target_field_FE"]["d0_R3"]
    f2 = {"perm": perm_p, "vol_matched": vm.get("p_one_sided", 1.0), "dose_trend": dose["p_one_sided"],
          "rewire": sp["d_backbone_d0_only"]["rewire"]["p"], "label_perm": sp["d_backbone_d0_only"]["label_perm"]["p"],
          "field_FE": fe["LR"]["p"]}
    f3 = {"d_lost_A1_pooled_one_sided": float(stats.norm.cdf(z)),
          "d_lost_short_2s": float(2 * stats.norm.sf(abs(zs["coef"]["d_lost_short"] / zs["se_concept"]["d_lost_short"]))),
          "d_lost_long_2s": float(2 * stats.norm.sf(abs(zs["coef"]["d_lost_long"] / zs["se_concept"]["d_lost_long"])))}
    holm = {"F1": {"raw": f1, "holm": M.holm(f1)}, "F2": {"raw": f2, "holm": M.holm(f2)}, "F3": {"raw": f3, "holm": M.holm(f3)}}
    bl = b["d_lost_A1"]["d_lost"]
    if bl["est"] >= 0:
        va = "REJECTED"
    elif bl["ci"][1] < 0 and holm["F3"]["holm"]["d_lost_A1_pooled_one_sided"] < 0.05:
        va = "CONFIRMED"
    else:
        va = "INCONCLUSIVE (negative point estimate, CI includes 0)"
    return {"criteria": c, "FRONTIER": v, "ABANDONMENT": va, "positive_groups": pos, "groups_in_sign_rule": groups,
            "cohort_d0": coh_d0, "d0_pooled4": d0, "d0_ci": ci, "d0_S_strict": d0s, "d0_S_strict_ci": cis,
            "d_lost_pooled4": bl["est"], "d_lost_ci": bl["ci"], "holm": holm}


def main() -> None:
    st = sys.argv[1] if len(sys.argv) > 1 else "outputs"  # default: rebuild outputs from the stored (sealed) stage results
    if st == "step1":
        stage_step1()
    elif st == "dev":
        stage_dev()
    elif st == "freeze":
        stage_freeze()
    elif st == "heldout":
        stage_heldout(sys.argv[2] if len(sys.argv) > 2 else None)
    elif st == "outputs":
        import outputs
        outputs.main()
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
