#!/usr/bin/env python3
"""How concepts hop between fields: H2 next-field entry (gateway-weighted relatedness to RETAINING fields vs
relatedness-to-home / size / Hidalgo density / own centrality), rescue, relay, trajectories and ordering.

Stages (run in this order; the held-out stage is sealed until the freeze stage has logged frozen_spec.json):
  python method.py dev      -> results/dev_result.json (+ dev tables)
  python method.py freeze   -> results/frozen_spec.json, results/freeze_log.txt
  python method.py heldout  -> results/heldout_result.json (run ONCE)
  python method.py outputs  -> method_out.json (exp_gen_sol_out schema) + figures
Prerequisites: pass1.py -> aggregate.py -> cand.py -> pass2.py -> grounding.py -> frame.py (see README)."""
from __future__ import annotations

import hashlib
import json
import math
import resource
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
from config import FIELD_GROUP, N_BOOT, N_PERM, N_REWIRE, RES, SCAN, SEED, Y0  # noqa: E402
from frame_io import SealedError, frozen, load_backbone, load_frame, load_g  # noqa: E402
import h2 as H2  # noqa: E402
import traj as TR  # noqa: E402
from stats_core import dersimonian_laird, fe_ols, fe_poisson, sign_test  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")
REGS = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate", "d_lost_gate"]
HELD_GROUPS = ["Physical", "LifeEnv", "Social", "MathDec", "Cohort"]


def jdump(obj, path: Path) -> None:
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, (set, tuple)):
            return list(o)
        return str(o)

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items() if not str(k).startswith("_")}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, float) and not math.isfinite(o):
            return None
        return o
    path.write_text(json.dumps(clean(obj), indent=1, default=conv))


def gate_terciles(gate: np.ndarray) -> tuple[float, float]:
    return float(np.quantile(gate, 1 / 3)), float(np.quantile(gate, 2 / 3))


def agg():
    z = np.load(SCAN / "agg_counts.npz")
    return z["G"], z["GF"]


# =============================================================================== H2
def h2_block(df: pd.DataFrame, spec: dict | None, rng, n_boot: int, n_perm: int, n_rewire: int, bb: dict,
             RET: np.ndarray, full: bool = True) -> tuple[dict, dict]:
    """fit M0-M3 on the primary sample (strata with a non-empty retaining set)."""
    dfs, spec = H2.standardise(df, spec, REGS)
    res = {"n_rows": len(dfs), "n_strata": int(dfs.stratum.nunique()), "n_concepts": int(dfs.cidx.nunique()),
           "n_events": int(dfs.entered.sum()), "entry_rate": float(dfs.entered.mean())}
    fits = {m: H2.fit_model(dfs, cols) for m, cols in H2.MODELS.items()}
    res["models"] = {m: {k: v for k, v in f.items() if k != "_b"} for m, f in fits.items()}
    res["LR"] = {"M2_vs_M0": H2.lr_test(fits["M2"], fits["M0"], 1), "M1_vs_M0": H2.lr_test(fits["M1"], fits["M0"], 1),
                 "M3_vs_M1": H2.lr_test(fits["M3"], fits["M1"], 1), "M2lost_vs_M0": H2.lr_test(fits["M2lost"], fits["M0"], 1)}
    # within-stratum AUC per block (linear predictor) and per single regressor
    auc = {}
    for m, cols in H2.MODELS.items():
        s = H2.within_auc(dfs, dfs[cols].to_numpy() @ fits[m]["_b"])
        auc[m] = {"mean": float(s.mean()), "ci": H2.concept_boot_mean(s, n_boot, rng), "n_strata": int(len(s))}
    for c in REGS:
        s = H2.within_auc(dfs, dfs[c].to_numpy())
        auc[c] = {"mean": float(s.mean()), "ci": H2.concept_boot_mean(s, n_boot, rng)}
    res["auc_within_stratum"] = auc
    if not full:
        return res, spec
    t = time.time()
    res["boot_d"] = H2.boot_coef(dfs, H2.MODELS["M2"], "d_ret_gate", n_boot, rng, small_cols=H2.MODELS["M0"])
    logger.info(f"bootstrap {n_boot} in {time.time()-t:.0f}s")
    # label-permutation null for d (phi and g permuted jointly across fields)
    phi, gate = bb["phi"], bb["g"]
    lr_obs = res["LR"]["M2_vs_M0"]["LR"]
    fields = df.field.to_numpy()
    base = dfs.copy()
    mu, sd = spec["d_ret_gate"]["mean"], spec["d_ret_gate"]["sd"]
    perm = []
    for _ in range(n_perm):
        p = rng.permutation(26)
        dp = H2.recompute_d(RET, fields, phi[np.ix_(p, p)], gate[p])
        base["d_ret_gate"] = (dp - mu) / sd
        perm.append(2 * (H2.fit_model(base, H2.MODELS["M2"])["ll"] - fits["M0"]["ll"]))
    perm = np.array(perm)
    res["perm_null"] = {"n": n_perm, "lr_obs": lr_obs, "p": float((1 + (perm >= lr_obs).sum()) / (1 + n_perm)),
                        "null_q": np.percentile(perm, [50, 90, 95, 99]).tolist(), "null_mean": float(perm.mean())}
    gperm = []
    lr31 = res["LR"]["M3_vs_M1"]["LR"]
    for _ in range(n_perm):
        p = rng.permutation(26)
        dp = H2.recompute_d(RET, fields, phi, gate[p])
        base["d_ret_gate"] = (dp - mu) / sd
        gperm.append(2 * (H2.fit_model(base, H2.MODELS["M3"])["ll"] - fits["M1"]["ll"]))
    gperm = np.array(gperm)
    res["gonly_perm_null_M3_vs_M1"] = {"n": n_perm, "lr_obs": lr31, "p": float((1 + (gperm >= lr31).sum()) / (1 + n_perm)),
                                       "null_q": np.percentile(gperm, [50, 90, 95, 99]).tolist()}
    base["d_ret_gate"] = dfs["d_ret_gate"]
    rew = []
    for _ in range(n_rewire):
        P = H2.rewire(phi, rng)
        gp = H2.eig_gateway(P)
        dp = H2.recompute_d(RET, fields, P, gp)
        base["d_ret_gate"] = (dp - mu) / sd
        rew.append(2 * (H2.fit_model(base, H2.MODELS["M2"])["ll"] - fits["M0"]["ll"]))
    rew = np.array(rew)
    res["rewired_null"] = {"n": n_rewire, "lr_obs": lr_obs, "p": float((1 + (rew >= lr_obs).sum()) / (1 + n_rewire)),
                           "null_q95": float(np.percentile(rew, 95)), "null_median": float(np.median(rew)),
                           "real_gain_le_null95": bool(lr_obs <= np.percentile(rew, 95))}
    res["_lrs_boot"] = res["boot_d"].pop("_lrs")
    return res, spec


def h2_robust(df_all: pd.DataFrame, spec: dict, frame: pd.DataFrame, G: dict, bb: dict, GF: np.ndarray, Gpf: dict | None) -> dict:
    out = {}
    prim = df_all[df_all.n_ret > 0]
    dfs, _ = H2.standardise(prim, spec, REGS)
    # LPM with concept-year and field FE, CRV1 by concept
    X = dfs[["a_phi_home", "b_log_size", "c_density", "d_ret_gate"]].to_numpy()
    r = fe_ols(dfs.entered.to_numpy().astype(float), X, [dfs.stratum.to_numpy(), dfs.field.to_numpy()], dfs.cidx.to_numpy(),
               ["a_phi_home", "b_log_size", "c_density", "d_ret_gate"])
    out["LPM_conceptyear_field_FE"] = {k: v for k, v in r.items() if k not in ("_b", "V")}
    # secondary sample: all strata with an empty-retaining-set indicator
    dall, _ = H2.standardise(df_all, spec, REGS)
    dall["ret_empty"] = (df_all.n_ret == 0).astype(float).to_numpy()
    f0 = H2.fit_model(dall, H2.MODELS["M0"] + ["ret_empty"]); f2 = H2.fit_model(dall, H2.MODELS["M2"] + ["ret_empty"])
    out["secondary_all_strata"] = {"d_coef": f2["coef"]["d_ret_gate"], "d_se": f2["se"]["d_ret_gate"],
                                   "LR": H2.lr_test(f2, f0, 1), "n_strata": f2["n_strata"]}
    # excluding intersection-born
    d = dfs[dfs.intersection_born == 0]
    f0 = H2.fit_model(d, H2.MODELS["M0"]); f2 = H2.fit_model(d, H2.MODELS["M2"])
    out["excl_intersection_born"] = {"d_coef": f2["coef"]["d_ret_gate"], "d_se": f2["se"]["d_ret_gate"], "LR": H2.lr_test(f2, f0, 1)}
    # boundary stratum: home is a top-tercile gateway
    lo, hi = gate_terciles(bb["g"])
    d = dfs.copy()
    d["home_top"] = (d.home_gateway >= hi).astype(float)
    d["d_x_home_top"] = d.d_ret_gate * d.home_top
    f = H2.fit_model(d, H2.MODELS["M2"] + ["d_x_home_top"])
    out["boundary_home_top_gateway"] = {"d_coef_home_not_top": f["coef"]["d_ret_gate"], "interaction": f["coef"]["d_x_home_top"],
                                        "interaction_se": f["se"]["d_x_home_top"], "n_home_top_concepts": int(d[d.home_top == 1].cidx.nunique())}
    # alternative gateway definitions (degree, betweenness) for d
    for kind in ("g_deg", "g_btw"):
        bb2 = dict(bb); bb2["g"] = bb[kind]
        dfk, RETk, _ = H2.build_risk_sets(frame, G, bb2, GF)
        dfk = dfk[dfk.n_ret > 0]
        dks, _ = H2.standardise(dfk, None, REGS)
        f0 = H2.fit_model(dks, H2.MODELS["M0"]); f2 = H2.fit_model(dks, H2.MODELS["M2"])
        out[f"gateway_{kind}"] = {"d_coef": f2["coef"]["d_ret_gate"], "d_se": f2["se"]["d_ret_gate"], "LR": H2.lr_test(f2, f0, 1)}
    # RCA-based entry definition
    dfr, _, _ = H2.build_risk_sets(frame, G, bb, GF, entry_def="rca")
    dfr = dfr[dfr.n_ret > 0]
    drs, _ = H2.standardise(dfr, None, REGS)
    f0 = H2.fit_model(drs, H2.MODELS["M0"]); f2 = H2.fit_model(drs, H2.MODELS["M2"])
    out["rca_entry"] = {"d_coef": f2["coef"]["d_ret_gate"], "d_se": f2["se"]["d_ret_gate"], "LR": H2.lr_test(f2, f0, 1),
                        "n_events": f2["n_events"]}
    if Gpf is not None:
        dfp, _, _ = H2.build_risk_sets(frame[frame.cidx.isin(list(Gpf))], Gpf, bb, GF)
        dfp = dfp[dfp.n_ret > 0]
        dps, _ = H2.standardise(dfp, None, REGS)
        f0 = H2.fit_model(dps, H2.MODELS["M0"]); f2 = H2.fit_model(dps, H2.MODELS["M2"])
        out["primary_topic_field_labels"] = {"d_coef": f2["coef"]["d_ret_gate"], "d_se": f2["se"]["d_ret_gate"],
                                             "LR": H2.lr_test(f2, f0, 1)}
    return out


def planted_control(df: pd.DataFrame, spec: dict, rng, n_sim: int = 100) -> dict:
    """T0 planted positive control on the REAL risk-set structure: one event per stratum with P ~ exp(beta*d)."""
    dfs, _ = H2.standardise(df, spec, REGS)
    dfs = dfs.sort_values("stratum").reset_index(drop=True)
    st = dfs.stratum.to_numpy(); u, starts = np.unique(st, return_index=True)
    ends = np.append(starts[1:], len(st))

    def sim(beta: float) -> float:
        y = np.zeros(len(dfs))
        eta = beta * dfs.d_ret_gate.to_numpy() + 0.8 * dfs.b_log_size.to_numpy()
        for s, e in zip(starts, ends):
            p = np.exp(eta[s:e] - eta[s:e].max()); p /= p.sum()
            y[s + rng.choice(e - s, p=p)] = 1
        d2 = dfs.assign(entered=y)
        return H2.lr_test(H2.fit_model(d2, H2.MODELS["M2"]), H2.fit_model(d2, H2.MODELS["M0"]), 1)["p"]
    pos = [sim(1.0) for _ in range(10)]
    null = [sim(0.0) for _ in range(n_sim)]
    return {"planted_beta1_p_median": float(np.median(pos)), "planted_detect_rate_p<0.001": float(np.mean(np.array(pos) < 1e-3)),
            "null_reject_rate_0.01": float(np.mean(np.array(null) < 0.01)), "n_null_sims": n_sim}


# =============================================================================== rescue / relay
def rescue_relay(frame: pd.DataFrame, eps: pd.DataFrame, G: dict, bb: dict, rng, n_boot: int) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    import rescue_relay as RR
    lo, hi = gate_terciles(bb["g"])
    pno = dict(zip(frame.cidx, frame.p_notag.fillna(1.0)))
    Hw, W = RR.load_works(set(frame.cidx), pno)
    logger.info(f"rescue/relay: {len(Hw):,} grounded (work, concept) rows, {len(W):,} works")
    eps = eps.copy()
    eps["gate_ter"] = np.where(eps.gateway_j >= hi, 2, np.where(eps.gateway_j >= lo, 1, 0))
    # leave-concept-out generic retention propensity of field j among same-cohort concepts
    P = []
    for e in eps.itertuples():
        m = (eps.field == e.field) & (eps.cidx != e.cidx) & ((eps.t0 - e.t0).abs() <= 2)
        P.append(eps.loc[m, "R_cj"].mean() if m.any() else np.nan)
    eps["P_generic"] = P
    resc = RR.rescue_table(frame, eps, Hw, W, G, bb["phi"])
    R = eps.merge(resc, on=["cidx", "field"], how="inner")
    R["log_n_early_j"] = np.log(R.n_early_j)
    R["ret_x_top"] = R.R_cj * (R.gate_ter == 2); R["ret_x_mid"] = R.R_cj * (R.gate_ter == 1)
    R["top"] = (R.gate_ter == 2).astype(float); R["mid"] = (R.gate_ter == 1).astype(float)
    out = {"n_episodes_rescue": int(len(R)), "n_with_crefs": int((R.n_cref > 0).sum()),
           "self_lineage_share_of_crefs": float(R.self_lineage.sum() / max(R.n_cref.sum(), 1))}
    names = ["R_cj", "top", "mid", "ret_x_top", "ret_x_mid", "log_n_early_j", "log_size_j"]
    for yv in ("resc", "s_other"):
        d = R[R[yv].notna()]
        if len(d) > 30 and d.cidx.nunique() > 10:
            r = fe_ols(d[yv].to_numpy(), d[names].to_numpy().astype(float), [d.cidx.to_numpy()], d.cidx.to_numpy(), names)
            out[f"R1_{yv}"] = {k: v for k, v in r.items() if k not in ("_b", "V")}
    # R2: H1 replication and mediation (same sample for both models)
    d = R[R.resc.notna() & R.P_generic.notna()].copy()
    base = ["gateway_j", "log_size_j", "phi_home_j", "P_generic", "log_n_early_j"]
    full = base + ["S_hanski", "resc"]
    for c in full:
        d[c + "_z"] = (d[c] - d[c].mean()) / (d[c].std() or 1)
    bz = [c + "_z" for c in base]; fz = [c + "_z" for c in full]
    if len(d) > 30:
        r0 = fe_ols(d.R_cj.to_numpy().astype(float), d[bz].to_numpy(), [d.cidx.to_numpy()], d.cidx.to_numpy(), bz)
        r1 = fe_ols(d.R_cj.to_numpy().astype(float), d[fz].to_numpy(), [d.cidx.to_numpy()], d.cidx.to_numpy(), fz)
        ind = r0["coef"]["gateway_j_z"]["b"] - r1["coef"]["gateway_j_z"]["b"]
        cids = d.cidx.unique(); by = d.groupby("cidx").indices
        bs = []
        for _ in range(n_boot):
            pick = rng.choice(cids, len(cids))
            idx = np.concatenate([by[c] for c in pick]); rep = np.repeat(np.arange(len(pick)), [len(by[c]) for c in pick])
            dd = d.iloc[idx]
            cl = dd.cidx.to_numpy() * 10000 + rep
            a0 = fe_ols(dd.R_cj.to_numpy().astype(float), dd[bz].to_numpy(), [cl], cl, bz)
            a1 = fe_ols(dd.R_cj.to_numpy().astype(float), dd[fz].to_numpy(), [cl], cl, fz)
            bs.append(a0["coef"]["gateway_j_z"]["b"] - a1["coef"]["gateway_j_z"]["b"])
        out["R2_base"] = {k: v for k, v in r0.items() if k not in ("_b", "V")}
        out["R2_full"] = {k: v for k, v in r1.items() if k not in ("_b", "V")}
        out["R2_mediation"] = {"indirect": float(ind), "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                               "share_mediated": float(ind / r0["coef"]["gateway_j_z"]["b"]) if r0["coef"]["gateway_j_z"]["b"] else None,
                               "n": int(len(d)), "n_concepts": int(d.cidx.nunique())}
    # H1 replication on all episodes (no provenance needed)
    e2 = eps[eps.P_generic.notna()].copy()
    e2["log_n_early_j"] = np.log(e2.n_early_j)
    for c in base:
        e2[c + "_z"] = (e2[c] - e2[c].mean()) / (e2[c].std() or 1)
    rr = fe_ols(e2.R_cj.to_numpy().astype(float), e2[bz].to_numpy(), [e2.cidx.to_numpy()], e2.cidx.to_numpy(), bz)
    out["H1_replication_all_episodes"] = {k: v for k, v in rr.items() if k not in ("_b", "V")}
    # R3 incidence-function curve: P(retained) by S_hanski quintile, gateway top vs bottom tercile
    R["S_bin"] = pd.qcut(R.S_hanski.rank(method="first"), 5, labels=False)
    out["R3_incidence"] = {ter: R[R.gate_ter == t].groupby("S_bin").R_cj.agg(["mean", "size"]).reset_index().to_dict("records")
                           for ter, t in (("top", 2), ("mid", 1), ("bottom", 0))}
    # relay
    rel = RR.relay_table(frame, eps, Hw, W)
    Rl = eps.merge(rel, on=["cidx", "field"], how="inner")
    Rl["log_n_early_j"] = np.log(Rl.n_early_j)
    Rl["ret_x_top"] = Rl.R_cj * (Rl.gate_ter == 2); Rl["ret_x_mid"] = Rl.R_cj * (Rl.gate_ter == 1)
    Rl["top"] = (Rl.gate_ter == 2).astype(float); Rl["mid"] = (Rl.gate_ter == 1).astype(float)
    d = Rl[Rl.n_later_fields > 0].copy()
    d["ret_x_gate"] = d.R_cj * d.gateway_j
    out["relay_n_episodes"] = int(len(d))
    # tercile-dummy Poisson separated on dev (empty cells) -> continuous gateway interaction (decided before freeze)
    pn = ["R_cj", "gateway_j", "ret_x_gate", "log_n_early_j", "log_size_j"]
    if len(d) > 30:
        pr = fe_poisson(d.relay.to_numpy(), d[pn].to_numpy().astype(float), d.cidx.to_numpy(), pn)
        pr2 = fe_poisson(d.relay.to_numpy(), d[pn].to_numpy().astype(float), d.cidx.to_numpy(), pn,
                         offset=np.log(d.E_avail.to_numpy() + 0.1))
        ol = fe_ols(d.relay_excess.to_numpy(), d[names].to_numpy().astype(float), [d.cidx.to_numpy()], d.cidx.to_numpy(), names)
        out["relay_fepois"] = pr; out["relay_fepois_offset"] = pr2
        out["relay_excess_ols"] = {k: v for k, v in ol.items() if k not in ("_b", "V")}
        gr = d[(d.R_cj == 1) & (d.gate_ter == 2)].relay_excess
        out["relay_excess_gateway_retained"] = {"mean": float(gr.mean()), "n": int(len(gr)),
                                                "ci": [float(x) for x in np.percentile([rng.choice(gr.to_numpy(), len(gr)).mean()
                                                                                         for _ in range(2000)], [2.5, 97.5])] if len(gr) > 1 else None}
        out["relay_excess_by_cell"] = d.groupby(["R_cj", "gate_ter"]).relay_excess.agg(["mean", "size"]).reset_index().to_dict("records")
    return out, R, Rl


# =============================================================================== trajectories
def traj_block(frame: pd.DataFrame, G: dict, bb: dict, rng, spec: dict | None) -> tuple[dict, pd.DataFrame, dict]:
    gate = bb["g"]; lo, hi = gate_terciles(gate)
    top, bot = gate >= hi, gate < lo
    P = TR.panel(frame, G, gate, top, bot)
    out = {}
    fr = frame.set_index("cidx")
    sub = frame[(frame.O1 == 1) & (frame.intersection_born == 0)]
    Pc = P[P.cidx.isin(sub.cidx)]
    if spec is None:
        zspec = {v: (float(Pc[v].mean()), float(Pc[v].std() or 1.0)) for v in TR.VARS}
    else:
        zspec = spec["zspec"]
    ids, Z = TR.to_array(Pc, zspec)
    out["n_concepts_clustered"] = int(len(ids)); out["n_intersection_born_O1"] = int(((frame.O1 == 1) & (frame.intersection_born == 1)).sum())
    D = TR.dtw_matrix(Z)
    tspec = {"zspec": zspec}
    if spec is None:
        ck = TR.choose_k(D, SEED)
        k = ck["k"]
        lab, med = TR.kmed(D, k, SEED)
        out["k_selection"] = ck
        tspec.update({"k": k, "medoid_cidx": [int(ids[m]) for m in med], "medoid_series": [Z[m].tolist() for m in med],
                      "k_flag": ck["flag"]})
    else:
        from tslearn.metrics import cdist_dtw
        from sklearn.metrics import adjusted_rand_score
        M = np.array(spec["medoid_series"])
        Dm = cdist_dtw(Z, M, global_constraint="sakoe_chiba", sakoe_chiba_radius=2)
        lab = Dm.argmin(1)
        k = spec["k"]
        lab_ind, _ = TR.kmed(D, k, SEED)
        out["heldout_independent_recluster_ARI"] = float(adjusted_rand_score(lab, lab_ind))
    out["cluster_sizes"] = np.bincount(lab, minlength=k).tolist()
    Pc = Pc.copy(); Pc["cluster"] = Pc.cidx.map(dict(zip(ids, lab)))
    out["cluster_mean_series"] = {int(c): Pc[Pc.cluster == c].groupby("age")[TR.VARS].mean().round(3).to_dict("list") for c in range(k)}
    out["cluster_by_group"] = pd.crosstab(Pc.drop_duplicates("cidx").cidx.map(fr.group), Pc.drop_duplicates("cidx").cluster).to_dict()
    cl_df = pd.DataFrame({"cidx": ids, "cluster": lab})
    cl_df = cl_df.merge(frame[["cidx", "name", "group", "O2r_m30", "O2r_resid", "O3"]] if "O2r_resid" in frame else frame[["cidx", "name", "group"]], on="cidx")
    out["cluster_outcomes"] = cl_df.groupby("cluster")[[c for c in ("O2r_m30", "O3") if c in cl_df]].mean().round(3).to_dict()
    # HMM on the same series
    if spec is None:
        hm = TR.hmm_fit(Z, SEED)
        tspec["hmm"] = {"n_states": hm["n_states"], "means": hm["means"], "transmat": hm["transmat"]}
        paths = hm["paths"]
        out["hmm"] = {"n_states": hm["n_states"], "bic_grid": hm["grid"], "state_means": hm["means"], "transmat": hm["transmat"]}
    else:
        from hmmlearn.hmm import GaussianHMM
        hm = TR.hmm_fit(Z, SEED, n_states=[spec["hmm"]["n_states"]])
        paths = hm["paths"]
        out["hmm"] = {"n_states": hm["n_states"], "note": "refit with the frozen number of states"}
    from sklearn.metrics import adjusted_rand_score
    sig = [TR.collapse(p) for p in paths]
    out["hmm_vs_dtw_ARI"] = float(adjusted_rand_score(lab, pd.factorize(pd.Series(sig))[0]))
    out["hmm_top_paths"] = pd.Series(sig).value_counts().head(8).to_dict()
    cl_df["hmm_path"] = sig
    return out, P, {"tspec": tspec, "clusters": cl_df}


def ordering_block(P: pd.DataFrame, frame: pd.DataFrame, bb: dict, rng, pen: float | None, o2r_cut: float | None) -> tuple[dict, dict]:
    out = {}
    fr = frame[frame.O2r_resid.notna()]
    if o2r_cut is None:
        o2r_cut = float(fr.O2r_resid.quantile(2 / 3))
    top_o2r = set(fr[fr.O2r_resid >= o2r_cut].cidx)
    Hs = {c: d.sort_values("t").H.to_numpy() for c, d in P.groupby("cidx")}
    if pen is None:
        cal_ids = fr[fr.O2r_resid <= fr.O2r_resid.quantile(1 / 3)].cidx
        cal = TR.calibrate_pen([Hs[c] for c in cal_ids if c in Hs], SEED)
        if cal["far_fresh"] > 0.07:
            cal = TR.calibrate_pen(list(Hs.values()), SEED)
            cal["note"] = "F7: calibrated on all dev concepts"
        out["calibration"] = cal
        pen = cal["pen"]
    res, O = TR.ordering(P, frame, pen, top_o2r)
    out.update(res)
    out["lead_lag"] = TR.lead_lag(P)
    # placebo: permute gateway scores across fields; lead-lag coefficient should vanish
    gate = bb["g"]; lo, hi = gate_terciles(gate)
    coefs = []
    Gd = {}
    for _ in range(200):
        gp = rng.permutation(gate)
        topp = gp >= hi
        P2 = P.copy()
        # recompute ret_gw from the per-year retaining sets
        P2["ret_gw"] = P2["_ret"].map(lambda r: int((np.asarray(r) & topp).sum()))
        ll = TR.lead_lag(P2)
        coefs.append(ll["forward_dH_on_ret"]["coef"]["ret_gw"]["b"])
    obs = out["lead_lag"]["forward_dH_on_ret"]["coef"]["ret_gw"]["b"]
    out["lead_lag_placebo"] = {"n": 200, "obs": obs, "null_q": np.percentile(coefs, [2.5, 50, 97.5]).tolist(),
                               "p_two_sided": float((1 + (np.abs(np.array(coefs)) >= abs(obs)).sum()) / 201)}
    return out, {"pen": pen, "o2r_cut": o2r_cut, "orders": O}


def add_ret_sets(P: pd.DataFrame, frame: pd.DataFrame, G: dict) -> pd.DataFrame:
    rets = []
    fr = frame.set_index("cidx")
    for c, d in P.groupby("cidx", sort=False):
        home = [int(h) for h in str(fr.loc[c, "home"]).split("|")]
        S = H2.states(G[c], home)
        for t in d.t:
            rets.append((c, t, S["retaining"][t - Y0].copy()))
    m = {(c, t): r for c, t, r in rets}
    P = P.copy()
    P["_ret"] = [m[(c, t)] for c, t in zip(P.cidx, P.t)]
    return P


# =============================================================================== stages
def stage_dev() -> None:
    rng = np.random.default_rng(SEED)
    bb = load_backbone(); G_tot, GF = agg()
    frame = load_frame("dev"); frame = frame[frame.newborn]
    G = load_g("dev")
    eps = pd.read_csv(RES / "episodes.csv"); eps = eps[(eps.split == "dev") & eps.cidx.isin(frame.cidx)]
    res = {"n_dev_concepts_newborn": int(len(frame)), "n_dev_episodes": int(len(eps)),
           "dev_by_group": frame.group.value_counts().to_dict()}
    t = time.time()
    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)
    df_all.to_parquet(RES / "entry_risk_sets_dev.parquet", index=False)
    prim = df_all.n_ret > 0
    df, RET = df_all[prim].reset_index(drop=True), RET_all[prim.to_numpy()]
    logger.info(f"dev risk sets: {len(df_all):,} rows, primary {len(df):,} rows / {df.stratum.nunique():,} strata "
                f"({time.time()-t:.0f}s)")
    h, spec = h2_block(df, None, rng, N_BOOT, N_PERM, N_REWIRE, bb, RET)
    lrs = h.pop("_lrs_boot")
    res["H2"] = h
    res["H2"]["size_vs_density_auc"] = {"size": h["auc_within_stratum"]["b_log_size"]["mean"],
                                        "density": h["auc_within_stratum"]["c_density"]["mean"]}
    logger.info(f"H2 dev: LR M2vsM0={h['LR']['M2_vs_M0']}, d={h['models']['M2']['coef']['d_ret_gate']:.3f}")
    Gpf = None
    pfp = SCAN / "frame_gpf_dev.npz"
    if pfp.exists():
        z = np.load(pfp); Gpf = {int(c): z["g"][i] for i, c in enumerate(z["cidx"])}
    res["H2_robustness"] = h2_robust(df_all, spec, frame, G, bb, GF, Gpf)
    res["T0_planted_control"] = planted_control(df, spec, rng)
    logger.info(f"planted control: {res['T0_planted_control']}")
    # power at held-out n: share of bootstrap LR draws significant at 0.01, rescaled to the held-out concept count
    nh = len(pd.read_csv(RES / "frame_concepts.csv").query("split != 'dev' and newborn"))
    scale = nh / max(frame.shape[0], 1)
    from scipy import stats as st
    res["power_check"] = {"n_heldout_concepts": nh, "scale_vs_dev": scale,
                          "P(p<0.01) at heldout n (LR scaled linearly)": float(np.mean(st.chi2.sf(lrs * scale, 1) < 0.01))}
    # rescue / relay
    try:
        rr, R, Rl = rescue_relay(frame, eps, G, bb, rng, N_BOOT)
        res["rescue_relay"] = rr
        R.drop(columns=[c for c in R.columns if c.startswith("_")]).to_csv(RES / "rescue_dev.csv", index=False)
        Rl.to_csv(RES / "relay_dev.csv", index=False)
    except (FileNotFoundError, ValueError, KeyError) as e:
        logger.exception("rescue/relay failed")
        res["rescue_relay"] = {"status": f"NOT RUN: {e!r}"}
    # trajectories + ordering
    tr, P, tsp = traj_block(frame, G, bb, rng, None)
    res["trajectories"] = tr
    P = add_ret_sets(P, frame, G)
    od, osp = ordering_block(P, frame, bb, rng, None, None)
    res["ordering"] = od
    P.drop(columns=["_ret"]).to_csv(RES / "trajectories_dev.csv", index=False)
    tsp["clusters"].to_csv(RES / "cluster_assign_dev.csv", index=False)
    osp["orders"].to_csv(RES / "ordering_dev.csv", index=False)
    jdump(res, RES / "dev_result.json")
    lo, hi = gate_terciles(bb["g"])
    jdump({"standardisation": spec, "tspec": tsp["tspec"], "pen": osp["pen"], "o2r_cut_resid": osp["o2r_cut"],
           "gate_terciles": [lo, hi]}, RES / "dev_spec_parts.json")
    logger.info("dev stage done")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def stage_freeze() -> None:
    parts = json.loads((RES / "dev_spec_parts.json").read_text())
    fs = json.loads((RES / "frame_summary.json").read_text())
    code = hashlib.sha256(b"".join(sha(p).encode() for p in sorted(list(ROOT.glob("*.py")) + list((ROOT / "lib").glob("*.py"))))).hexdigest()
    spec = {"created": datetime.now(timezone.utc).isoformat(),
            "regressors": {"a_phi_home": "mean_h phi[h,k] over home fields", "b_log_size": "log venue-field works in k at t-1",
                           "c_density": "Hidalgo density sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]",
                           "e_gate_own": "gateway_eig of k", "d0_ret_rel": "mean_{j in Ret(t-1)} phi[j,k]",
                           "d_ret_gate": "sum_{j in Ret(t-1)} g_j phi[j,k] / sum_{j in Ret} g_j",
                           "d_lost_gate": "same over LOST fields (placebo)"},
            "models": H2.MODELS, "primary_sample": "strata (concept, t) with non-empty retaining set; t = t0+1..t0+8",
            "standardisation": parts["standardisation"], "gate_terciles": parts["gate_terciles"],
            "o2r_resid_coef_dev": fs.get("o2r_resid_coef_dev"), "o2r_top_tercile_cut_resid": parts["o2r_cut_resid"],
            "changepoint_pen": parts["pen"], **parts["tspec"],
            "rescue": "R1 resc ~ retained x gate tercile + log n_early_j + log size_j | concept; R2 LPM with S_hanski, resc mediators",
            "relay": "fepois relay ~ retained + gateway_j + retained x gateway_j + log n_early_j + log size_j | concept (continuous interaction; tercile dummies separated on dev); OLS relay_excess ~ retained x gate tercile",
            "hashes": {"lexicon": (RES / "lexicon_hash.txt").read_text().strip(), "sense_filter": sha(RES / "sense_filter.pkl"),
                       "backbone": sha(ROOT / "inputs" / "field_backbone.json"), "code": code},
            "decision_rules": {
                "H2_entry_CONFIRMED": "LR M2 vs M0 p<0.01 AND pooled d>0 with concept-bootstrap 95% CI>0 AND d>0 in >= ceil(0.75 x available held-out FIELD groups) (MathDec has no concepts -> 3 of 3: Physical, LifeEnv, Social) AND d>0 in the 2010-14 cohort AND permutation p<0.05 AND real LR gain > 95th pct of the rewired-backbone null",
                "H2_ordering_CONFIRMED": "p_gw>=0.60 with one-sided sign test p<0.05 AND p_gw > peripheral share",
                "RESCUE_SUPPORTED": "R1 retained x top-gateway interaction >0 with CI>0 AND R2 indirect effect >0",
                "RELAY_SUPPORTED": "retained x gateway_j fepois coefficient >0 with CI>0 AND mean relay_excess of top-tercile-gateway retained episodes >0"}}
    jdump(spec, RES / "frozen_spec.json")
    h = sha(RES / "frozen_spec.json")
    with (RES / "freeze_log.txt").open("a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} frozen_spec.json sha256={h}\n")
    logger.info(f"frozen: {h}")


def stage_heldout() -> None:
    if not frozen():
        raise SealedError("freeze first")
    import frame as FR
    spec = json.loads((RES / "frozen_spec.json").read_text())
    rng = np.random.default_rng(SEED + 7)
    bb = load_backbone(); G_tot, GF = agg()
    fc = pd.read_csv(RES / "frame_concepts.csv")
    G = load_g("heldout")
    # unseal: held-out outcomes and episode outcomes
    for i, r in fc[fc.split != "dev"].iterrows():
        o = FR.concept_outcomes(G[int(r.cidx)], int(r.t0), G_tot)
        for k, v in o.items():
            fc.loc[i, k] = v
    coef = spec["o2r_resid_coef_dev"]
    m = fc.split != "dev"
    fc.loc[m, "O2r_resid"] = fc.loc[m, "O2r_m30"] - np.polyval(coef, np.log(fc.loc[m, "n_early"]))
    fc.to_csv(RES / "frame_concepts.csv", index=False)
    eps = pd.read_csv(RES / "episodes.csv")
    for i, e in eps[eps.split != "dev"].iterrows():
        eps.loc[i, "R_cj"] = FR.episode_outcome(G[int(e.cidx)], int(e.t0), int(e.field))
    eps.to_csv(RES / "episodes.csv", index=False)
    frame = fc[(fc.split != "dev") & fc.newborn].copy()
    frame["hgroup"] = np.where(frame.split == "heldout_cohort", "Cohort", frame.group)
    res = {"n_heldout_concepts": int(len(frame)), "by_group": frame.hgroup.value_counts().to_dict()}
    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)
    df_all["hgroup"] = df_all.cidx.map(dict(zip(frame.cidx, frame.hgroup)))
    df_all.to_parquet(RES / "entry_risk_sets_heldout.parquet", index=False)
    prim = (df_all.n_ret > 0).to_numpy()
    df, RET = df_all[prim].reset_index(drop=True), RET_all[prim]
    std = spec["standardisation"]
    h, _ = h2_block(df, std, rng, N_BOOT, N_PERM, N_REWIRE, bb, RET)
    h.pop("_lrs_boot", None)
    res["H2_pooled"] = h
    # frozen dev coefficients scored on held-out (prediction AUC, no refit)
    dev = json.loads((RES / "dev_result.json").read_text())
    dfs, _ = H2.standardise(df, std, REGS)
    for mname in ("M0", "M2"):
        b = np.array([dev["H2"]["models"][mname]["coef"][c] for c in H2.MODELS[mname]])
        s = H2.within_auc(dfs, dfs[H2.MODELS[mname]].to_numpy() @ b)
        res.setdefault("frozen_dev_coef_auc", {})[mname] = {"mean": float(s.mean()), "ci": H2.concept_boot_mean(s, N_BOOT, rng)}
    per = {}
    for gname in HELD_GROUPS + ["OtherHealth"]:
        d = df[df.hgroup == gname]
        if d.cidx.nunique() < 5:
            per[gname] = {"n_concepts": int(d.cidx.nunique()), "status": "too few concepts"}
            continue
        ds, _ = H2.standardise(d, std, REGS)
        f0 = H2.fit_model(ds, H2.MODELS["M0"]); f2 = H2.fit_model(ds, H2.MODELS["M2"])
        bt = H2.boot_coef(ds, H2.MODELS["M2"], "d_ret_gate", 500, rng)
        per[gname] = {"n_concepts": int(d.cidx.nunique()), "n_events": f2["n_events"], "d": f2["coef"]["d_ret_gate"],
                      "se": f2["se"]["d_ret_gate"], "boot_ci": bt["ci"], "LR": H2.lr_test(f2, f0, 1)}
    res["H2_per_group"] = per
    use = [g for g in HELD_GROUPS if "d" in per.get(g, {})]
    res["H2_DL_pooled"] = dersimonian_laird(np.array([per[g]["d"] for g in use]), np.array([per[g]["se"] for g in use]))
    npos = sum(per[g]["d"] > 0 for g in use)
    res["H2_sign_count"] = {"positive": int(npos), "of": len(use), "sign_test_p": sign_test(npos, len(use))}
    eps_h = eps[(eps.split != "dev") & eps.cidx.isin(frame.cidx)]
    try:
        rr, R, Rl = rescue_relay(frame, eps_h, G, bb, rng, N_BOOT)
        res["rescue_relay"] = rr
        R.to_csv(RES / "rescue_heldout.csv", index=False); Rl.to_csv(RES / "relay_heldout.csv", index=False)
    except (FileNotFoundError, ValueError, KeyError) as e:
        logger.exception("held-out rescue/relay failed")
        res["rescue_relay"] = {"status": f"NOT RUN: {e!r}"}
    tr, P, tsp = traj_block(frame, G, bb, rng, spec)
    res["trajectories"] = tr
    P = add_ret_sets(P, frame, G)
    od, osp = ordering_block(P, frame, bb, rng, spec["changepoint_pen"], spec["o2r_top_tercile_cut_resid"])
    res["ordering"] = od
    P.drop(columns=["_ret"]).to_csv(RES / "trajectories_heldout.csv", index=False)
    tsp["clusters"].to_csv(RES / "cluster_assign_heldout.csv", index=False)
    osp["orders"].to_csv(RES / "ordering_heldout.csv", index=False)
    # decisions
    lr = h["LR"]["M2_vs_M0"]
    ci = h["boot_d"]["ci"]
    fg = [g for g in ("Physical", "LifeEnv", "Social", "MathDec") if "d" in per.get(g, {})]
    grp_pos = sum(per[g]["d"] > 0 for g in fg)
    need = math.ceil(0.75 * len(fg))
    dec = {"H2_entry": {"LR_p<0.01": lr["p"] < 0.01, "d>0_CI>0": h["models"]["M2"]["coef"]["d_ret_gate"] > 0 and ci[0] > 0,
                        f"field_groups_positive>={need}_of_{len(fg)}": grp_pos >= need,
                        "cohort_positive": per.get("Cohort", {}).get("d", -1) > 0, "perm_p<0.05": h["perm_null"]["p"] < 0.05,
                        "rewired_gain_above_null95": not h["rewired_null"]["real_gain_le_null95"]}}
    dec["H2_entry"]["CONFIRMED"] = all(dec["H2_entry"].values())
    gw = od["gateway"]; pe = od["peripheral"]
    dec["H2_ordering"] = {"p_gw": gw["share_before_excl_ties"], "sign_p": gw["sign_test_p_one_sided"],
                          "peripheral_share": pe["share_before_excl_ties"],
                          "CONFIRMED": bool(gw["share_before_excl_ties"] >= 0.6 and gw["sign_test_p_one_sided"] < 0.05
                                            and gw["share_before_excl_ties"] > (pe["share_before_excl_ties"] if pe["share_before_excl_ties"] == pe["share_before_excl_ties"] else 0))}
    rrh = res["rescue_relay"]
    try:
        r1 = rrh["R1_resc"]["coef"]["ret_x_top"]; med = rrh["R2_mediation"]
        dec["RESCUE"] = {"R1_interaction": r1["b"], "R1_ci": r1["ci"], "indirect": med["indirect"], "indirect_ci": med["ci"],
                         "SUPPORTED": bool(r1["b"] > 0 and r1["ci"][0] > 0 and med["indirect"] > 0)}
        rp = rrh["relay_fepois"]["coef"]["ret_x_gate"]; ex = rrh["relay_excess_gateway_retained"]
        dec["RELAY"] = {"fepois_ret_x_gate": rp["b"], "ci": rp["ci"], "mean_excess_gw_retained": ex["mean"],
                        "SUPPORTED": bool(rp["b"] > 0 and rp["ci"][0] > 0 and ex["mean"] > 0)}
    except (KeyError, TypeError) as e:
        dec["RESCUE_RELAY_status"] = f"not evaluable: {e!r}"
    res["decisions"] = dec
    jdump(res, RES / "heldout_result.json")
    with (RES / "freeze_log.txt").open("a") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} heldout stage run; heldout_result.json sha256={sha(RES / 'heldout_result.json')}\n")
    logger.info(f"held-out decisions: {json.dumps(dec, default=str)}")


@logger.catch(reraise=True)
def main() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (24 * 1024**3, 24 * 1024**3))
    stage = sys.argv[1] if len(sys.argv) > 1 else "dev"
    if stage == "outputs":
        import make_outputs
        make_outputs.main()
        return
    {"dev": stage_dev, "freeze": stage_freeze, "heldout": stage_heldout}[stage]()


if __name__ == "__main__":
    main()
