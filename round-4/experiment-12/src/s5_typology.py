#!/usr/bin/env python3
"""S5 TYPOLOGY (DEV fit, frozen; held-out after the unseal) under a strict naming rule, else a PCA CONTINUUM,
plus OPEN on the axis (Spearman and partial Spearman given B5 + label coverage) for all three OPEN builds.

Usage: python s5_typology.py --scope dev | heldout"""
from __future__ import annotations

import argparse
import json
import pickle
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from joblib import Parallel, delayed  # noqa: E402
from sklearn.metrics import adjusted_rand_score as ARI  # noqa: E402

import typology as TY  # noqa: E402
from common import (B5, DATA, DEV_GROUPS, DISCLOSURE, E6, HELD_GROUPS, RES, ROOT, SEED, UNITS, add_deviation,  # noqa: E402
                    jdump, load_outcomes, network_guard, setup_logger, update_status)
from rq1stats import dersimonian_laird, psp_boot  # noqa: E402

network_guard()
logger = setup_logger("s5_typology")
DTW_CACHE = ROOT / "dtw_cache"
DTW_CACHE.mkdir(exist_ok=True)
FROZEN = DATA / "typology_frozen.pkl"
BUILDS = ("all", "home", "size")
N_BOOT_OPEN = 2000


def load_base():
    J = pd.read_parquet(DATA / "joined.parquet")
    P = pd.read_parquet(ROOT / "panel.parquet")
    O = pd.read_parquet(ROOT / "open_features.parquet")[["ci"] + [f"OPEN_{b}" for b in BUILDS]]
    return J.merge(O, on="ci"), P


def open_on_axis(T: pd.DataFrame, axis: str, seed: int, n_boot: int = N_BOOT_OPEN) -> dict:
    out = {}
    cov = T[B5 + ["label_coverage_early"]].to_numpy(float)
    for k, b in enumerate(BUILDS):
        x = T[f"OPEN_{b}"].to_numpy(float)
        y = T[axis].to_numpy(float)
        raw = psp_boot(x, y, None, None, n_boot, seed + 10 * k)
        par = psp_boot(x, y, cov, None, n_boot, seed + 10 * k + 1)
        out[b] = {"spearman": {kk: raw[kk] for kk in ("n", "rho", "ci", "se", "p")},
                  "partial_given_B5_labelcov": {kk: par[kk] for kk in ("n", "rho", "ci", "se", "p")}}
    return out


def open_null(T: pd.DataFrame, axis: str, seed: int, n: int = 200) -> dict:
    """T9: shuffle OPEN within group; Spearman with the axis (null band must cover 0)."""
    from scipy.stats import spearmanr
    rng = np.random.default_rng(seed)
    out = {}
    for b in BUILDS:
        S = T[np.isfinite(T[f"OPEN_{b}"])]
        v = []
        for _ in range(n):
            xs = S.groupby("group")[f"OPEN_{b}"].transform(lambda s: rng.permutation(s.to_numpy()))
            v.append(spearmanr(xs, S[axis]).statistic)
        out[b] = {"q025_q975": np.percentile(v, [2.5, 97.5]).tolist(), "mean": float(np.mean(v)),
                  "covers_0": bool(np.percentile(v, 2.5) <= 0 <= np.percentile(v, 97.5))}
    return out


def e6_map() -> dict:
    fc = pd.read_csv(E6 / "results/frame_concepts.csv", usecols=["cidx", "concept_id"])
    fc["cid"] = fc.concept_id.str.replace("https://openalex.org/C", "", regex=False).astype(np.int64)
    return dict(zip(fc.cidx, fc.cid))


def old_typology(labels: pd.Series, which: str) -> dict:
    """ARI of our labels vs EXP6 cluster_assign on overlapping concepts (labels indexed by concept_id)."""
    ca = pd.read_csv(E6 / f"results/cluster_assign_{which}.csv")
    ca["cid"] = ca.cidx.map(e6_map())
    m = ca[ca.cid.isin(labels.index)]
    if len(m) < 5:
        return {"n_overlap": int(len(m))}
    return {"n_overlap": int(len(m)), "ari": float(ARI(m.cluster, labels.loc[m.cid].to_numpy())),
            "exp6_verdict": "Exp6 two-class typology: NOT ESTABLISHED (HMM-DTW ARI 0.094)"}


def profiles(T: pd.DataFrame, lab_col: str, X: np.ndarray, O: pd.DataFrame | None) -> dict:
    out = {"sizes": T[lab_col].value_counts().sort_index().to_dict(),
           "x_group": pd.crosstab(T[lab_col], T.group).to_dict(orient="index"),
           "med_share": T.groupby(lab_col).med_home.mean().to_dict(),
           "label_coverage_median": T.groupby(lab_col).label_coverage_early.median().to_dict(),
           "logvol_median": T.groupby(lab_col).logvol.median().to_dict(),
           "open_all_mean": T.groupby(lab_col).OPEN_all.mean().to_dict(),
           "open_home_mean": T.groupby(lab_col).OPEN_home.mean().to_dict(),
           "open_size_mean": T.groupby(lab_col).OPEN_size.mean().to_dict()}
    if O is not None:
        M = T[["ci", lab_col]].merge(O, on="ci")
        out["outcomes"] = {o: M.groupby(lab_col)[o].agg(["mean", "median", "count"]).to_dict(orient="index")
                           for o in ("O1c", "O1b", "O2r_resid", "O3", "O4")}
    out["mean_series"] = {int(c): {v: X[(T[lab_col] == c).to_numpy(), :, j].mean(0).round(4).tolist()
                                   for j, v in enumerate(TY.VARS)} for c in sorted(T[lab_col].unique())}
    return out


# ============================================================================== DEV
def stage_dev(workers: int) -> None:
    T, P = load_base()
    T = T[T.split == "DEV"].reset_index(drop=True)
    cis = T.ci.to_numpy()
    Xr = TY.build_X(P, cis)
    zs = TY.zspec_fit(Xr)
    Z = TY.zapply(Xr, zs)
    logger.info(f"DEV X {Z.shape}")
    res = {"n": len(T), "VARS": TY.VARS, "asinh": TY.ASINH_VARS, "zspec": zs, "ages": list(range(9))}
    # ---- DTW (time 500 first; extrapolate)
    TY.dtw_matrix(Z[:20], n_jobs=workers)          # numba JIT warm-up
    t = time.time()
    TY.dtw_matrix(Z[:500], n_jobs=workers)
    t500 = time.time() - t
    proj = t500 * (len(Z) / 500) ** 2 / 60
    res["dtw_timing"] = {"t500_s": t500, "projected_full_min": proj}
    logger.info(f"DTW 500: {t500:.1f}s -> projected {proj:.1f} min for {len(Z)}")
    sub_idx = np.arange(len(Z))
    if proj > 25:
        sub_idx = np.sort(np.random.default_rng(SEED).choice(len(Z), 3000, replace=False))
        add_deviation("dtw_subsample", f"DTW projected {proj:.0f} min > 25", "k selected on a 3,000 DEV subsample")
    D = TY.load_matrix_parts(DTW_CACHE, "D_dev")      # split cache: dtw_cache/D_dev_part_NNN.npy
    if D is None:
        D = TY.dtw_matrix(Z, n_jobs=workers)
        TY.save_matrix_parts(D, DTW_CACHE, "D_dev")
    logger.info(f"DTW matrix {D.shape} in {time.time()-t:.0f}s")
    # ---- k selection (parallel over k) + gap
    ks = list(range(2, 9))
    t = time.time()
    res["choose_k"] = TY.choose_k(np.ascontiguousarray(D[np.ix_(sub_idx, sub_idx)]), SEED, ks, 100, n_jobs=workers)
    k = res["choose_k"]["k"]
    logger.info(f"choose_k in {time.time()-t:.0f}s: " + ", ".join(f"k{kk}: sil {v['silhouette']:.3f} ARI "
                                                             f"{v['ari_median']:.3f}" for kk, v in res["choose_k"]["grid"].items()))
    res["gap"] = TY.gap_statistic(Z.reshape(len(Z), -1), seed=SEED)
    lab_dtw, med = TY.kmed(D, k, SEED)
    logger.info(f"k = {k} ({res['choose_k']['flag']}); sizes {np.bincount(lab_dtw).tolist()}; gap k {res['gap']['k_gap']}")
    # ---- HMM (restarts in parallel)
    def fit_state(s):
        return s, TY.hmm_fit(Z, SEED, states=(s,), restarts=10)
    fits = dict(Parallel(n_jobs=3)(delayed(fit_state)(s) for s in (3, 4, 5)))
    hgrid = {s: f["grid"][s] for s, f in fits.items()}
    S_best = min(hgrid, key=lambda s: hgrid[s]["bic"])
    hmm = fits[S_best]["model"]
    Fh = TY.hmm_features(hmm, Z)
    Dh = TY.euclid(Fh)
    lab_hmm, _ = TY.kmed(Dh, k, SEED)
    ari_dh = float(ARI(lab_dtw, lab_hmm))
    res["hmm"] = {"grid": hgrid, "n_states": S_best, "means": hmm.means_.tolist(), "transmat": hmm.transmat_.tolist(),
                  "ari_dtw_hmm": ari_dh}
    logger.info(f"HMM S = {S_best}; ARI(DTW, HMM) = {ari_dh:.3f}")
    # ---- stability, Medicine, volume
    jac = TY.hennig_jaccard(D, lab_dtw, k, SEED, 100, n_jobs=workers)
    nm = (T.med_home == 0).to_numpy()
    lab_nm, _ = TY.kmed(D[np.ix_(nm, nm)], k, SEED)
    ari_nm = float(ARI(lab_dtw[nm], lab_nm))
    share_nm = [float(((lab_dtw == c) & nm).sum() / nm.sum()) for c in range(k)]
    vt = pd.qcut(T.logvol.rank(method="first"), 3, labels=False).to_numpy()
    ari_vol = float(ARI(lab_dtw, vt))
    rule = TY.naming_rule(ari_dh, jac["mean_jaccard"], ari_nm, share_nm, ari_vol, None)
    res["stability"] = {"hennig": jac, "ari_nomed_recluster": ari_nm, "share_nonMed": share_nm,
                        "ari_volume_tercile": ari_vol, "ari_hmm_volume_tercile": float(ARI(lab_hmm, vt))}
    res["naming_rule_pre_heldout"] = rule
    T["dtw_class"], T["hmm_class"] = lab_dtw, lab_hmm
    # T8 sanity printed BEFORE any naming
    res["T8_sanity"] = {"class_x_volume_tercile_ari": ari_vol,
                        "class_x_med": pd.crosstab(T.dtw_class, T.med_home).to_dict(orient="index"),
                        "class_x_group": pd.crosstab(T.dtw_class, T.group).to_dict(orient="index")}
    logger.info(f"T8: vol ARI {ari_vol:.3f}; med table {res['T8_sanity']['class_x_med']}")
    logger.info(f"Hennig Jaccard {np.round(jac['mean_jaccard'], 3).tolist()}; ARI noMed {ari_nm:.3f}; "
                f"any class passes pre-heldout conditions: {rule['any_named']}")
    # ---- PCA continuum (always computed; reported as THE result when no class is named)
    pc = TY.pca_fit(Z)
    S = TY.pca_project(Z, pc)
    e8 = Xr[:, 8, TY.VARS.index("n_ent_off")]
    r8 = Xr[:, 8, TY.VARS.index("n_ret")]
    sign = np.ones(pc["keep"])
    for j in range(pc["keep"]):
        ref = e8 if j == 0 else r8
        if np.corrcoef(S[:, j], ref)[0, 1] < 0:
            sign[j] = -1
    pc["components"] = pc["components"] * sign[:, None]
    S = TY.pca_project(Z, pc)
    for j in range(pc["keep"]):
        T[f"PC{j+1}"] = S[:, j]
    res["pca"] = {"explained": pc["explained"], "keep": pc["keep"],
                  "orientation": "PC1 correlates positively with asinh n_ent_off at age 8; PC2+ with asinh n_ret at age 8",
                  "loadings": {f"PC{j+1}": {v: pc["components"][j].reshape(9, len(TY.VARS))[:, i].round(4).tolist()
                                            for i, v in enumerate(TY.VARS)} for j in range(pc["keep"])},
                  "pc1_corr_logvol": float(np.corrcoef(T.PC1, T.logvol)[0, 1]),
                  "pc1_spearman_logvol": float(pd.Series(T.PC1).rank().corr(T.logvol.rank()))}
    logger.info(f"PCA explained {np.round(pc['explained'][:4], 3).tolist()}; keep {pc['keep']}")
    # ---- OPEN on the axis
    res["open_on_axis"] = {"pooled": {f"PC{j+1}": open_on_axis(T, f"PC{j+1}", SEED + 50 + j) for j in range(pc["keep"])}}
    res["open_on_axis"]["per_group_PC1"] = {g: open_on_axis(T[T.group == g], "PC1", SEED + 60 + i)
                                            for i, g in enumerate(DEV_GROUPS)}
    res["open_on_axis"]["noMed_PC1"] = open_on_axis(T[T.med_home == 0], "PC1", SEED + 70)
    res["open_on_axis"]["DL_dev_groups_PC1"] = {
        b: {kind: dersimonian_laird([res["open_on_axis"]["per_group_PC1"][g][b][kind]["rho"] for g in DEV_GROUPS],
                                    [res["open_on_axis"]["per_group_PC1"][g][b][kind]["se"] for g in DEV_GROUPS])
            for kind in ("spearman", "partial_given_B5_labelcov")} for b in BUILDS}
    res["T9_open_shuffle_null_PC1"] = open_null(T, "PC1", SEED + 80)
    for b in BUILDS:
        r = res["open_on_axis"]["pooled"]["PC1"][b]
        logger.info(f"OPEN_{b} ~ PC1: rho {r['spearman']['rho']:.3f} {np.round(r['spearman']['ci'], 3).tolist()}; "
                    f"partial {r['partial_given_B5_labelcov']['rho']:.3f} "
                    f"{np.round(r['partial_given_B5_labelcov']['ci'], 3).tolist()}")
    # ---- profiles, old typology
    O = load_outcomes().dev()
    T["PC1_tercile"] = pd.qcut(T.PC1, 3, labels=False)
    res["profiles_dtw"] = profiles(T, "dtw_class", Xr, O)
    res["profiles_pc1_tercile"] = profiles(T, "PC1_tercile", Xr, O)
    res["medoids"] = [{"class": c, "ci": int(T.ci.iloc[m]), "name": str(T.name.iloc[m]), "group": str(T.group.iloc[m]),
                       "series": {v: Xr[m, :, j].round(3).tolist() for j, v in enumerate(TY.VARS)}}
                      for c, m in enumerate(med)]
    lab_cid = pd.Series(T.dtw_class.to_numpy(), index=T.concept_id.to_numpy())
    pc1_med = pd.Series((T.PC1 > T.PC1.median()).astype(int).to_numpy(), index=T.concept_id.to_numpy())
    res["old_typology_exp6_dev"] = {"dtw_class": old_typology(lab_cid, "dev"), "pc1_median_split": old_typology(pc1_med, "dev")}
    res["outcome"] = "TYPOLOGY (classes named)" if rule["any_named"] else "CONTINUUM (no class passes the naming rule)"
    res["Source"] = "s5_typology.py --scope dev; inputs panel.parquet (S3), open_features.parquet (S2)"
    jdump(res, RES / "trajectories_dev.json")
    T[["ci", "dtw_class", "hmm_class"] + [f"PC{j+1}" for j in range(pc["keep"])]].to_parquet(
        RES / "typology_dev_assign.parquet", index=False)
    with FROZEN.open("wb") as f:
        pickle.dump({"zspec": zs, "k": k, "S": S_best, "medoid_ci": T.ci.iloc[med].tolist(), "Z_medoids": Z[med],
                     "pca": pc, "hmm": hmm, "dev_ci": cis}, f)
    logger.info(f"S5 DEV outcome: {res['outcome']}")
    update_status("S5_typology_DEV", {"typology_dev": {"k": k, "ari_dtw_hmm": ari_dh, "outcome": res["outcome"]}})


# ============================================================================== held-out
def stage_heldout(workers: int) -> None:
    load_outcomes().all()      # raises unless unsealed
    with FROZEN.open("rb") as f:
        fz = pickle.load(f)
    T, P = load_base()
    T = T[T.split != "DEV"].reset_index(drop=True)
    Xr = TY.build_X(P, T.ci.to_numpy())
    Z = TY.zapply(Xr, fz["zspec"])
    k = fz["k"]
    Dm = TY.dtw_matrix(Z, Z2=fz["Z_medoids"], n_jobs=workers)
    T["dtw_class_nearest"] = Dm.argmin(1)
    S = TY.pca_project(Z, fz["pca"])
    for j in range(fz["pca"]["keep"]):
        T[f"PC{j+1}"] = S[:, j]
    res = {"disclosure": DISCLOSURE, "n": len(T), "k": k, "rule4": {}}
    for part in ("HELDOUT", "COHORT"):
        m = (T.split == part).to_numpy()
        Dp = TY.load_matrix_parts(DTW_CACHE, f"D_{part}")
        if Dp is None:
            Dp = TY.dtw_matrix(Z[m], n_jobs=workers)
            TY.save_matrix_parts(Dp, DTW_CACHE, f"D_{part}")
        lab, _ = TY.kmed(Dp, k, SEED)
        res["rule4"][part] = {"n": int(m.sum()), "ari_recluster_vs_nearest_dev_medoid":
                              float(ARI(lab, T.dtw_class_nearest[m]))}
        logger.info(f"rule 4 {part}: ARI {res['rule4'][part]['ari_recluster_vs_nearest_dev_medoid']:.3f}")
    dev = json.loads((RES / "trajectories_dev.json").read_text())
    st = dev["stability"]
    ari_h = res["rule4"]["HELDOUT"]["ari_recluster_vs_nearest_dev_medoid"]
    res["naming_rule_final"] = TY.naming_rule(dev["hmm"]["ari_dtw_hmm"], st["hennig"]["mean_jaccard"],
                                              st["ari_nomed_recluster"], st["share_nonMed"], st["ari_volume_tercile"], ari_h)
    res["outcome"] = ("TYPOLOGY (classes named)" if res["naming_rule_final"]["any_named"]
                      else "CONTINUUM (no class passes the naming rule)")
    # OPEN on the axis: per unit, pooled, DL over held-out groups
    ax = {}
    for i, u in enumerate(UNITS):
        ax[u] = open_on_axis(T[T.unit == u], "PC1", SEED + 700 + i)
    res["open_on_axis_units_PC1"] = ax
    H4 = T[T.unit.isin(HELD_GROUPS)]
    res["open_on_axis_pooled_heldout4"] = {f"PC{j+1}": open_on_axis(H4, f"PC{j+1}", SEED + 720 + j)
                                           for j in range(fz["pca"]["keep"])}
    res["open_on_axis_heldout4_noMed_PC1"] = open_on_axis(H4[H4.med_home == 0], "PC1", SEED + 730)
    res["open_on_axis_heldout4_noEXP6_PC1"] = open_on_axis(H4[H4.in_exp6 == 0], "PC1", SEED + 731)
    res["open_on_axis_cohort_PC1"] = open_on_axis(T[T.split == "COHORT"], "PC1", SEED + 732)
    res["DL_heldout_groups_PC1"] = {
        b: {kind: {"units": HELD_GROUPS, **dersimonian_laird([ax[u][b][kind]["rho"] for u in HELD_GROUPS],
                                                            [ax[u][b][kind]["se"] for u in HELD_GROUPS])}
            for kind in ("spearman", "partial_given_B5_labelcov")} for b in BUILDS}
    res["T9_open_shuffle_null_PC1_heldout4"] = open_null(H4, "PC1", SEED + 740)
    for b in BUILDS:
        d = res["DL_heldout_groups_PC1"][b]
        logger.info(f"held-out DL OPEN_{b} ~ PC1: rho {d['spearman']['b']:.3f} {np.round(d['spearman']['ci'], 3).tolist()}"
                    f" I2 {d['spearman']['I2']:.2f}; partial {d['partial_given_B5_labelcov']['b']:.3f} "
                    f"{np.round(d['partial_given_B5_labelcov']['ci'], 3).tolist()}")
    O = load_outcomes().all()
    T["PC1_tercile"] = pd.qcut(T.PC1, 3, labels=False)
    res["profiles_pc1_tercile"] = profiles(T, "PC1_tercile", Xr, O)
    res["profiles_nearest_class"] = profiles(T, "dtw_class_nearest", Xr, O)
    lab_cid = pd.Series(T.dtw_class_nearest.to_numpy(), index=T.concept_id.to_numpy())
    res["old_typology_exp6_heldout"] = old_typology(lab_cid, "heldout")
    res["pc_distribution_shift"] = {u: {"PC1_median": float(T[T.unit == u].PC1.median()),
                                        "PC1_iqr": np.percentile(T[T.unit == u].PC1, [25, 75]).tolist()} for u in UNITS}
    res["Source"] = "s5_typology.py --scope heldout; frozen z / k / medoids / PCA loadings from data/typology_frozen.pkl"
    jdump(res, RES / "trajectories_heldout.json")
    T[["ci", "dtw_class_nearest"] + [f"PC{j+1}" for j in range(fz["pca"]["keep"])]].to_parquet(
        RES / "typology_heldout_assign.parquet", index=False)
    update_status("S5_typology_heldout", {"typology_final_outcome": res["outcome"]})


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default="dev", choices=["dev", "heldout"])
    ap.add_argument("--workers", type=int, default=16)
    a = ap.parse_args()
    (stage_dev if a.scope == "dev" else stage_heldout)(a.workers)


if __name__ == "__main__":
    main()
