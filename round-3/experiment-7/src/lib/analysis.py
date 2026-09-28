"""Analysis battery shared by every frame and split (EXP6 robustness, EXP5-minus-EXP6 DEV, held-out):
ladder, bootstraps, specificity (a)-(o), abandonment, per-unit fits, power simulation."""
from __future__ import annotations

import time
import zlib

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats
from sklearn.metrics import roc_auc_score

import d3
import h2_exp6 as H2
import models as M

M.RUNGS.update({
    "A1_split": M.BASE + ["d_lost_short", "d_lost_long"],
    "VM0": M.RUNGS["R2_vol"],
    "VM": M.RUNGS["R2_vol"] + ["d_R_m", "d_N_m"],
    "VMF": M.RUNGS["R2_vol"] + ["d_R_mf", "d_N_mf"],
    "DOSE": M.RUNGS["R2_vol"] + ["d_ret_a2", "d_ret_a3", "d_ret_a4p"],
    "R3_Dcum": M.RUNGS["R3_ret"] + ["D_cum"],
    "R2_Dcum": M.RUNGS["R2_vol"] + ["D_cum"],
})
PRIM_RUNGS = ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost", "S_strict0", "S_strict", "S_pca0", "S_pca", "EXP6_M1", "EXP6_M2lost"]


def rng_for(seed: int, tag: str) -> np.random.Generator:
    return np.random.default_rng([seed, zlib.crc32(tag.encode())])


def split_std(df_all: pd.DataFrame, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(primary = strata with a non-empty retained set [EXP6 convention], all candidate rows), both standardised."""
    alls = M.standardise(df_all, spec)
    return alls[df_all.n_ret.to_numpy() > 0], alls


def coef_row(df: pd.DataFrame, cols: list[str], target: str, small: list[str] | None = None) -> dict:
    m = M.model(df, cols)
    r = m.fit()
    j = cols.index(target)
    out = {"coef": float(r["coef"][j]), "se_model": float(r["se"][j]), "n_strata": r["n_strata"], "n_events": r["n_events"],
           "n_concepts": int(df.cidx.nunique()), "converged": r["converged"]}
    if r["n_strata"] > 0:
        out["se_concept"] = float(m.cluster_se(r, "concept")[j])
        out["p_wald_concept_2s"] = float(2 * stats.norm.sf(abs(out["coef"] / out["se_concept"]))) if out["se_concept"] > 0 else None
    if small is not None:
        rs = M.model(df, small).fit(want_cov=False)
        out["LR"] = M.lr(r, rs, len(cols) - len(small))
    return out


def sens_pair(prim: pd.DataFrame, alls: pd.DataFrame, extra: list[str] | None = None, drop: list[str] | None = None) -> dict:
    """d0 in R3 (LR vs R2) on the primary sample and d_lost in A1 (LR vs R0) on all rows."""
    extra = extra or []
    drop = drop or []
    f = lambda c: [x for x in c if x not in drop] + extra  # noqa: E731
    return {"d0_R3": coef_row(prim, f(M.RUNGS["R3_ret"]), "d0_ret_rel", f(M.RUNGS["R2_vol"])),
            "d_lost_A1": coef_row(alls, f(M.RUNGS["A1_lost"]), "d_lost", f(M.RUNGS["R0_M0"]))}


def vif_block(prim: pd.DataFrame, cols: list[str]) -> dict:
    d = M.informative(prim)
    Z = d[cols].to_numpy(float)
    _, inv = np.unique(d.stratum.to_numpy(), return_inverse=True)
    cnt = np.bincount(inv)
    for j in range(Z.shape[1]):
        Z[:, j] -= (np.bincount(inv, weights=Z[:, j]) / cnt)[inv]
    Z = Z / np.maximum(Z.std(0), 1e-12)
    Cm = np.corrcoef(Z, rowvar=False)
    try:
        vif = np.diag(np.linalg.inv(Cm))
    except np.linalg.LinAlgError:
        vif = np.full(len(cols), np.inf)
    return {"vif_within_stratum": dict(zip(cols, map(float, vif))), "condition_number": float(np.linalg.cond(Z)),
            "corr_within": pd.DataFrame(Cm, index=cols, columns=cols).round(3).to_dict()}


# ----------------------------------------------------------------------------- nulls
def _d0_from_masks(Mk: np.ndarray, phi: np.ndarray, pos: np.ndarray, k: np.ndarray) -> np.ndarray:
    return d3._mrel(Mk, phi)[pos, k]


def perm_masks(P: np.ndarray, nret: np.ndarray, rng) -> np.ndarray:
    """per row: nret[s] fields drawn uniformly without replacement from the pool P[s] (requires |P| >= nret)."""
    key = rng.random(P.shape)
    key[~P] = 2.0
    rank = key.argsort(1).argsort(1)
    return rank < nret[:, None]


def perm_null(prim: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n: int, pool: str = "POOL") -> dict:
    """(a) retained-label permutation within concept-year: |RET| fields drawn uniformly from the pool of age-eligible
    entered off-home fields (footprint and set size kept, persistence scrambled). Statistic LR(R3 vs R2)."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    m3 = M.model(prim, c3); r3 = m3.fit(want_cov=False)
    ll2 = M.model(prim, c2).fit(want_cov=False)["ll"]
    obs = 2 * (r3["ll"] - ll2)
    sidx = prim.s_idx.to_numpy(); k = prim.field.to_numpy() - 11
    us, pos = np.unique(sidx, return_inverse=True)
    RET, P = st["RET"][us], st[pool][us]
    nret = RET.sum(1)
    assert (P | RET).sum() == P.sum(), "pool must contain RET"
    j = c3.index("d0_ret_rel")
    mu, sd = spec["d0_ret_rel"]["mean"], spec["d0_ret_rel"]["sd"]
    strat_of_us = prim.groupby("s_idx").stratum.first().loc[us].to_numpy()
    inf_s = np.isin(strat_of_us, m3.sid)
    nontriv = float(((P.sum(1) > nret) & (nret > 0))[inf_s].mean())
    null = []
    for _ in range(n):
        Mk = perm_masks(P, nret, rng)
        m3.set_col(j, (_d0_from_masks(Mk, phi, pos, k) - mu) / sd)
        null.append(2 * (m3.fit(b0=r3["coef"], want_cov=False)["ll"] - ll2))
    null = np.array(null)
    return {"pool": pool, "n_perm": n, "LR_obs": float(obs), "p": float((1 + (null >= obs).sum()) / (1 + n)),
            "null_q": [float(x) for x in np.percentile(null, [50, 90, 95, 99])], "null_mean": float(null.mean()),
            "share_strata_nontrivial": nontriv, "resampling_unit": "within concept-year stratum (label permutation)",
            "_null": null}


def backbone_null(prim: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n_rewire: int, n_label: int) -> dict:
    """(d) PRIMARY: recompute d0 only on (i) degree-preserving rewired phi, (ii) node-label-permuted phi."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    m3 = M.model(prim, c3); r3 = m3.fit(want_cov=False)
    ll2 = M.model(prim, c2).fit(want_cov=False)["ll"]
    obs = 2 * (r3["ll"] - ll2)
    sidx = prim.s_idx.to_numpy(); k = prim.field.to_numpy() - 11
    us, pos = np.unique(sidx, return_inverse=True)
    RET = st["RET"][us]
    j = c3.index("d0_ret_rel")
    mu, sd = spec["d0_ret_rel"]["mean"], spec["d0_ret_rel"]["sd"]
    out = {"LR_obs": float(obs)}
    for name, nn in (("rewire", n_rewire), ("label_perm", n_label)):
        null = []
        for _ in range(nn):
            if name == "rewire":
                P = H2.rewire(phi, rng)
            else:
                p = rng.permutation(26)
                P = phi[np.ix_(p, p)]
            m3.set_col(j, (_d0_from_masks(RET, P, pos, k) - mu) / sd)
            null.append(2 * (m3.fit(b0=r3["coef"], want_cov=False)["ll"] - ll2))
        null = np.array(null)
        out[name] = {"n": nn, "p": float((1 + (null >= obs).sum()) / (1 + nn)),
                     "null_q": [float(x) for x in np.percentile(null, [50, 90, 95, 99])], "_null": null}
    return out


def backbone_null_full(df_all: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n: int) -> dict:
    """(d) SECONDARY: every phi covariate and the gateway recomputed on each rewired backbone; LR(R3 vs R2) and d0."""
    prim_mask = df_all.n_ret.to_numpy() > 0
    base = df_all[["cidx", "t", "field", "entered", "stratum", "s_idx", "b_log_size"]].reset_index(drop=True)
    lrs, d0s = [], []
    for _ in range(n):
        P = H2.rewire(phi, rng)
        gp = H2.eig_gateway(P)
        cv = d3.covariates(st, P, gp)
        assert len(cv) == len(base) and (cv.s_idx.to_numpy() == base.s_idx.to_numpy()).all()
        d = base.copy()
        for c in d3.PHI_COLS + ["e_gate_own"]:
            d[c] = cv[c].to_numpy()
        d = M.standardise(d[prim_mask], spec)
        r3 = M.model(d, M.RUNGS["R3_ret"]).fit(want_cov=False)
        r2 = M.model(d, M.RUNGS["R2_vol"]).fit(want_cov=False)
        lrs.append(2 * (r3["ll"] - r2["ll"])); d0s.append(r3["coef"][-1])
    return {"n": n, "LR_null_q": [float(x) for x in np.percentile(lrs, [50, 90, 95, 99])],
            "d0_null_q": [float(x) for x in np.percentile(d0s, [5, 50, 95])], "_lrs": np.array(lrs)}


# ----------------------------------------------------------------------------- battery
def ladder_block(prim: pd.DataFrame, alls: pd.DataFrame) -> dict:
    lad = M.fit_ladder(prim, PRIM_RUNGS, two_way=["R3_ret"])
    lad.pop("_fits")
    ab = M.fit_ladder(alls, ["R0_M0", "A1_lost", "A1_split"], two_way=["A1_lost"])
    ab.pop("_fits")
    ab["LR"]["A1_split_vs_R0_M0"] = M.lr({"ll": ab["models"]["A1_split"]["ll"]}, {"ll": ab["models"]["R0_M0"]["ll"]}, 2)
    return {"frontier_primary_sample": lad, "abandonment_all_rows": ab}


def headline_boots(prim: pd.DataFrame, alls: pd.DataFrame, rng, n_boot: int, second_seed: bool = False) -> dict:
    t = time.time()
    out = {"d0_R3": M.boot_refit(prim, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["R2_vol"]),
           "d0_S_strict": M.boot_refit(prim, M.RUNGS["S_strict"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["S_strict0"]),
           "d0_S_pca": M.boot_refit(prim, M.RUNGS["S_pca"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["S_pca0"]),
           "d_lost_A1": M.boot_refit(alls, M.RUNGS["A1_lost"], ["d_lost"], n_boot, rng, small_cols=M.RUNGS["R0_M0"]),
           "R4": M.boot_refit(prim, M.RUNGS["R4_lost"], ["d0_ret_rel", "d_lost"], n_boot, rng)}
    if second_seed:
        b2 = M.boot_refit(prim, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, np.random.default_rng(rng.integers(1 << 31)))
        a, b = out["d0_R3"]["d0_ret_rel"]["ci"], b2["d0_ret_rel"]["ci"]
        out["T6_seed_stability_d0_R3"] = {"ci_seed1": a, "ci_seed2": b, "max_endpoint_shift": float(max(abs(a[0] - b[0]), abs(a[1] - b[1]))),
                                          "pass_lt_0.01": bool(max(abs(a[0] - b[0]), abs(a[1] - b[1])) < 0.01)}
    for v in out.values():
        if isinstance(v, dict):
            v.pop("_B", None)
    logger.info(f"headline bootstraps ({n_boot}) in {time.time()-t:.0f}s")
    return out


def specificity(df_all: pd.DataFrame, st: dict, prim: pd.DataFrame, alls: pd.DataFrame, spec: dict, bb: dict, rng,
                n_boot: int, n_perm: int, n_rewire: int, n_label: int, n_rewire_full: int) -> dict:
    phi = bb["phi"]
    out = {}
    t = time.time()
    out["a_permutation"] = perm_null(prim, st, phi, spec, rng, n_perm, "POOL")
    out["a_permutation_secondary_all_entered_offhome"] = perm_null(prim, st, phi, spec, rng, max(n_perm // 2, 20), "ENTOFF")
    logger.info(f"  (a) permutation {time.time()-t:.0f}s p={out['a_permutation']['p']:.4f}")
    # (b) volume-matched contrast
    vm = prim[prim.has_match == 1]
    b = {"match_rate_strata": float(prim.groupby("stratum").has_match.max().mean()), "n_rows": int(len(vm)),
         "n_strata": int(vm.stratum.nunique()), "n_concepts": int(vm.cidx.nunique())}
    if vm.cidx.nunique() >= 20:
        b["fit"] = coef_row(vm, M.RUNGS["VM"], "d_R_m", M.RUNGS["VM0"])
        b["fit_N"] = coef_row(vm, M.RUNGS["VM"], "d_N_m")
        b["contrast_R_minus_N"] = M.contrast_boot(vm, M.RUNGS["VM"], "d_R_m", "d_N_m", n_boot, rng)
        # balance of matched fields: mean n(t-1) and cum(t-1) for matched R vs N fields
        us = np.unique(vm.s_idx.to_numpy())
        Rm, Nm = d3.vol_matched_masks({k_: st[k_][us] for k_ in ("xprev", "cumprev", "RET", "ENTOFF")})
        b["balance"] = {"mean_n_prev_R": float(st["xprev"][us][Rm].mean()), "mean_n_prev_N": float(st["xprev"][us][Nm].mean()),
                        "mean_cum_prev_R": float(st["cumprev"][us][Rm].mean()), "mean_cum_prev_N": float(st["cumprev"][us][Nm].mean()),
                        "n_matched_R_fields": int(Rm.sum()), "n_matched_N_fields": int(Nm.sum())}
    else:
        b["status"] = "too few matched concepts"
    out["b_volume_matched"] = b
    vf = prim[prim.has_match_f == 1]
    bf = {"bins": "fine (added before the EXP5 freeze)", "match_rate_strata": float(prim.groupby("stratum").has_match_f.max().mean()),
          "n_rows": int(len(vf)), "n_concepts": int(vf.cidx.nunique())}
    if vf.cidx.nunique() >= 20:
        bf["fit"] = coef_row(vf, M.RUNGS["VMF"], "d_R_mf", M.RUNGS["VM0"])
        bf["contrast_R_minus_N"] = M.contrast_boot(vf, M.RUNGS["VMF"], "d_R_mf", "d_N_mf", n_boot, rng)
        us = np.unique(vf.s_idx.to_numpy())
        Rm, Nm = d3.vol_matched_masks({k_: st[k_][us] for k_ in ("xprev", "cumprev", "RET", "ENTOFF")}, fine=True)
        bf["balance"] = {"mean_n_prev_R": float(st["xprev"][us][Rm].mean()), "mean_n_prev_N": float(st["xprev"][us][Nm].mean()),
                         "mean_cum_prev_R": float(st["cumprev"][us][Rm].mean()), "mean_cum_prev_N": float(st["cumprev"][us][Nm].mean()),
                         "n_matched_R_fields": int(Rm.sum()), "n_matched_N_fields": int(Nm.sum())}
    out["b2_volume_matched_fine"] = bf
    out["b_D_cum_rival"] = coef_row(prim, M.RUNGS["R3_Dcum"], "d0_ret_rel", M.RUNGS["R2_Dcum"])
    # (c) dose
    cdose = M.RUNGS["DOSE"]
    dose = {"fit": {c: coef_row(prim, cdose, c) for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")}}
    dose["contrast_4p_minus_2"] = M.contrast_boot(prim, cdose, "d_ret_a4p", "d_ret_a2", n_boot, rng)
    bet = [dose["fit"][c]["coef"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
    dose["betas_by_age"] = dict(zip(["2", "3", "4+"], bet))
    dose["monotone_nondecreasing"] = bool(bet[0] <= bet[1] <= bet[2])
    dose["spearman_beta_age"] = float(stats.spearmanr([2, 3, 4], bet).statistic)
    out["c_dose"] = dose
    # (d) backbone nulls
    t = time.time()
    out["d_backbone_d0_only"] = backbone_null(prim, st, phi, spec, rng, n_rewire, n_label)
    if n_rewire_full > 0:
        out["d_backbone_full_recompute"] = backbone_null_full(df_all, st, phi, spec, rng, n_rewire_full)
        out["d_backbone_full_recompute"]["LR_obs"] = out["d_backbone_d0_only"]["LR_obs"]
        nl = out["d_backbone_full_recompute"]["_lrs"]
        out["d_backbone_full_recompute"]["p"] = float((1 + (nl >= out["d_backbone_d0_only"]["LR_obs"]).sum()) / (1 + len(nl)))
    logger.info(f"  (d) backbone nulls {time.time()-t:.0f}s")
    # (e), (g)-(j), (n), (o): subsets / FE
    sub = lambda m: sens_pair(prim[m(prim)], alls[m(alls)])  # noqa: E731
    out["e_excl_intersection_born"] = sub(lambda d: d.intersect == 0)
    fe_cols = [f"fe_{f}" for f in range(12, 37)]
    pf, af = prim.copy(), alls.copy()
    for f in range(12, 37):
        pf[f"fe_{f}"] = (pf.field == f).astype(float); af[f"fe_{f}"] = (af.field == f).astype(float)
    out["g_target_field_FE"] = sens_pair(pf, af, extra=fe_cols, drop=["e_gate_own"])
    out["g_target_field_FE"]["note"] = "25 field dummies; e_gate_own is field-constant and absorbed, so dropped"
    out["h_horizon8"] = sub(lambda d: d.age <= 8)
    out["i_excl_weak_home"] = sub(lambda d: d.weak_home == 0)
    out["j_excl_medicine_home"] = sub(lambda d: d.home_med == 0)
    out["n_newborn_only_descriptive"] = sub(lambda d: d.newborn_i == 1) if (prim.newborn_i == 1).any() else {"status": "none"}
    out["o_label_coverage_ge_0.5"] = sub(lambda d: d.label_cov >= 0.5)
    return out


def rebuild_sens(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, bb: dict, spec: dict, horizon: int, meta: list[str],
                 Gpt: np.ndarray | None = None) -> dict:
    """(f) min_n 3 / 5, (k) primary-topic fields, (l) RCA-defined entry event, (m) min-CP proximity: rebuild and refit."""
    import exp5 as X
    out = {}
    jobs = [("f_min_n_3", dict(min_n=3)), ("f_min_n_5", dict(min_n=5)), ("l_rca_entry_event", dict(entry_def="rca"))]
    for name, kw in jobs:
        st = d3.build_strata(frame, G, GF, horizon=horizon, **kw)
        df = d3.attach_meta(d3.covariates(st, bb["phi"], bb["gate"]), st, frame, meta)
        p, a = split_std(df, spec)
        out[name] = sens_pair(p, a)
        out[name]["n_events_all"] = int(df.entered.sum())
    if Gpt is not None:
        st = d3.build_strata(frame, Gpt, GF, horizon=horizon)
        df = d3.attach_meta(d3.covariates(st, bb["phi"], bb["gate"]), st, frame, meta)
        p, a = split_std(df, spec)
        out["k_primary_topic_fields"] = sens_pair(p, a)
    phm = X.phi_min_cp()
    st = d3.build_strata(frame, G, GF, horizon=horizon)
    df = d3.attach_meta(d3.covariates(st, phm, bb["gate"]), st, frame, meta)
    # min-CP covariates live on a different scale: standardise on this frame's own moments (reported as such)
    sp2 = M.make_spec(df[df.n_ret > 0])
    p, a = split_std(df, sp2)
    out["m_min_conditional_probability_proximity"] = {"ladder": {k: v for k, v in M.fit_ladder(p, ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost"]).items() if k != "_fits"},
                                                      **sens_pair(p, a), "note": "standardised on this sample's own moments"}
    return out


def unit_fits(prim: pd.DataFrame, alls: pd.DataFrame, unit_col: str, units: list[str], rng, n_boot: int) -> dict:
    out = {}
    for u in units:
        p, a = prim[prim[unit_col] == u], alls[alls[unit_col] == u]
        if p.cidx.nunique() < 5:
            out[u] = {"status": "too few concepts", "n_concepts": int(p.cidx.nunique())}
            continue
        r = sens_pair(p, a)
        bt = M.boot_refit(p, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, rng)
        r["d0_R3"]["boot_ci"] = bt["d0_ret_rel"]["ci"]
        bl = M.boot_refit(a, M.RUNGS["A1_lost"], ["d_lost"], n_boot, rng)
        r["d_lost_A1"]["boot_ci"] = bl["d_lost"]["ci"]
        r["resampling_unit"] = "concept"
        r["n_boot"] = n_boot
        r["within_auc_R3_vs_R2"] = {}
        for rn in ("R2_vol", "R3_ret"):
            cols = M.RUNGS[rn]
            b = M.model(p, cols).fit(want_cov=False)["coef"]
            r["within_auc_R3_vs_R2"][rn] = float(H2.within_auc(p, p[cols].to_numpy() @ b).mean())
        r["sparsity"] = {"share_strata_any_lost": float(a.groupby("stratum").n_lost.max().gt(0).mean()),
                         "mean_n_lost_per_stratum": float(a.groupby("stratum").n_lost.max().mean())}
        out[u] = r
    return out


def dl_block(units: dict, names: list[str]) -> dict:
    res = {}
    for key, tg in (("d0_R3", "d0"), ("d_lost_A1", "d_lost")):
        use = [u for u in names if key in units.get(u, {})]
        b = [units[u][key]["coef"] for u in use]
        se = [units[u][key].get("se_concept", units[u][key]["se_model"]) for u in use]
        res[tg] = {"units": use, **M.dl(b, se), "n_positive": int(sum(x > 0 for x in b)), "n_negative": int(sum(x < 0 for x in b)),
                   "se_type": "concept-clustered sandwich"}
    return res


def guevara_auc(df_all: pd.DataFrame, prim: pd.DataFrame, coef_R3: dict) -> dict:
    y = df_all.entered.to_numpy()
    out = {"note": "GLOBAL (pooled, not within-stratum) AUC over all candidate rows; unit = concept x target field x year, "
                   "event = D3 count entry; Guevara et al. 2016 report 0.896 (individuals), 0.715 (organisations), 0.682 "
                   "(countries) for RCA-transition entry into research fields: different unit, event and proximity",
           "D_rca_cum_alone": float(roc_auc_score(y, df_all.D_rca_cum)), "D_rca_1y_alone": float(roc_auc_score(y, df_all.D_rca_1y)),
           "c_density_alone": float(roc_auc_score(y, df_all.c_density)), "b_log_size_alone": float(roc_auc_score(y, df_all.b_log_size))}
    cols = M.RUNGS["R3_ret"]
    lp = prim[cols].to_numpy() @ np.array([coef_R3[c] for c in cols])
    out["R3_linear_predictor_primary_rows"] = float(roc_auc_score(prim.entered, lp))
    return out


# ----------------------------------------------------------------------------- power simulation
def _sim_events(m: M.FastCLogit, eta: np.ndarray, rng) -> np.ndarray:
    """keep the observed number of events per stratum; draw them without replacement with p ~ exp(eta) (Gumbel top-m)."""
    gum = eta - np.log(-np.log(rng.random(len(eta))))
    # rank within stratum, descending key
    order = np.lexsort((-gum, m.row_s))
    rank = np.empty(len(eta), np.int64)
    pos_in = np.arange(len(eta)) - np.repeat(m.starts, m.counts)
    rank[order] = pos_in
    return (rank < m.nev[m.row_s]).astype(float)


def power_sim(prim_dev: pd.DataFrame, alls_dev: pd.DataFrame, unit_sizes: dict[str, int], rng, n_pooled: int, n_unit: int,
              grid_d0=(0, .05, .10, .15, .20, .28), grid_lost=(0, -.03, -.06, -.10)) -> dict:
    c4, c3, c2, ca, c0 = M.RUNGS["R4_lost"], M.RUNGS["R3_ret"], M.RUNGS["R2_vol"], M.RUNGS["A1_lost"], M.RUNGS["R0_M0"]
    ip = M.informative(prim_dev); ia = M.informative(alls_dev)
    b4 = M.model(ip, c4).fit(want_cov=False)["coef"]
    ba = M.model(ia, ca).fit(want_cov=False)["coef"]
    cp = ip.cidx.unique(); caa = ia.cidx.unique()
    res = {"truth_R4_dev": dict(zip(c4, map(float, b4))), "truth_A1_dev": dict(zip(ca, map(float, ba))), "table": {}}
    for u, n in unit_sizes.items():
        ns = n_pooled if u == "POOLED4" else n_unit
        row = {"n_concepts": n, "n_sims": ns, "d0": {}, "d_lost": {}, "n_capped_at_dev_size": bool(n > len(cp))}

        def sim_d0(args):
            bd, seed = args
            r_ = np.random.default_rng(seed)
            pick = r_.choice(cp, min(n, len(cp)), replace=False)
            d = ip[ip.cidx.isin(pick)]
            m = M.model(d, c4)
            bt = b4.copy(); bt[c4.index("d0_ret_rel")] = bd
            ysim = _sim_events(m, m.X @ bt, r_)
            m3 = M.FastCLogit(m.X[:, :len(c3)], ysim, m.sid[m.row_s]); m2 = M.FastCLogit(m.X[:, :len(c2)], ysim, m.sid[m.row_s])
            r3 = m3.fit(want_cov=False); r2 = m2.fit(want_cov=False)
            lrv = 2 * (r3["ll"] - r2["ll"])
            return bool(stats.chi2.sf(max(lrv, 0), 1) < 0.01 and r3["coef"][-1] > 0)

        def sim_lost(args):
            bl, seed = args
            r_ = np.random.default_rng(seed)
            pick = r_.choice(caa, min(n, len(caa)), replace=False)
            d = ia[ia.cidx.isin(pick)]
            m = M.model(d, ca)
            bt = ba.copy(); bt[-1] = bl
            ysim = _sim_events(m, m.X @ bt, r_)
            r = M.FastCLogit(m.X, ysim, m.sid[m.row_s]).fit()
            return bool(stats.norm.cdf(r["coef"][-1] / r["se"][-1]) < 0.05)
        for bd in grid_d0:
            row["d0"][str(bd)] = float(np.mean(M.tmap(sim_d0, [(bd, s_) for s_ in rng.integers(1 << 62, size=ns)])))
        for bl in grid_lost:
            row["d_lost"][str(bl)] = float(np.mean(M.tmap(sim_lost, [(bl, s_) for s_ in rng.integers(1 << 62, size=ns)])))
        row["MDE80_d0"] = _mde(row["d0"], grid_d0)
        row["MDE80_d_lost"] = _mde(row["d_lost"], grid_lost)
        res["table"][u] = row
        logger.info(f"  power {u} (n={n}): d0 {row['d0']} | d_lost {row['d_lost']}")
    return res


def _mde(pw: dict, grid) -> float | None:
    xs = [abs(g) for g in grid]
    ys = [pw[str(g)] for g in grid]
    for i in range(1, len(xs)):
        if ys[i] >= 0.8 and ys[i - 1] < 0.8:
            return float(xs[i - 1] + (0.8 - ys[i - 1]) * (xs[i] - xs[i - 1]) / max(ys[i] - ys[i - 1], 1e-9))
    return float(xs[0]) if ys[0] >= 0.8 else None


def shuffled_control(prim: pd.DataFrame, rng, n: int = 20) -> dict:
    """shuffle 'entered' within strata; LR(R3 vs R2) p < 0.01 should occur in <= 1 of 20."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    d = M.informative(prim).copy()
    strata = d.stratum.to_numpy(); y0 = d.entered.to_numpy()
    srt = np.argsort(strata, kind="stable")
    rej = []
    for _ in range(n):
        idx = np.lexsort((rng.random(len(d)), strata))
        ynew = np.empty_like(y0); ynew[srt] = y0[idx]
        d["entered"] = ynew
        r3 = M.model(d, c3).fit(want_cov=False); r2 = M.model(d, c2).fit(want_cov=False)
        rej.append(stats.chi2.sf(max(2 * (r3["ll"] - r2["ll"]), 0), 1) < 0.01)
    return {"n": n, "n_reject_p<0.01": int(sum(rej)), "pass_le_1": bool(sum(rej) <= 1)}
