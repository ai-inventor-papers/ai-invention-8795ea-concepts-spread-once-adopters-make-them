#!/usr/bin/env python3
"""S4 DECOMPOSITION: log Bn = log E2 (early contact) + log M (frontier advance) + log rho (retention); shares of the
top-vs-bottom O2r_resid tercile gap, volume-stratified, Medicine-adjusted / excluded, with 2,000 concept-bootstrap
CIs and the pre-registered verdicts PR1 / PR1b / PR2 (+ PR3 descriptive).

Usage: python s4_decomp.py --scope dev          (before the seal; DEV only)
       python s4_decomp.py --scope heldout      (after s7_seal.py unsealed once)"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import decomp as DC  # noqa: E402
from common import (B5, DATA, DISCLOSURE, HELD_GROUPS, N_BOOT, RES, SEED, UNITS, jdump, load_outcomes,  # noqa: E402
                    network_guard, setup_logger, sha256_file, update_status)
from rq1stats import dersimonian_laird, holm, psp_boot  # noqa: E402

network_guard()
logger = setup_logger("s4_decomp")

PREREG = {
    "PR1": ("EXPLORATION > RETENTION: in variant (iv) [volume-stratified (early-volume quintiles), concepts with a "
            "Medicine (field 27) home excluded], s_explore - s_ret > 0 with the 95% concept-bootstrap CI > 0, where "
            "s_explore = s_E2 + s_M and s_ret = s_rho are the shares of the top-vs-bottom O2r_resid tercile gap in "
            "log mean breadth (Bn = retained off-home fields at t0+8). Equivalently s_ret < 0.5; both are printed "
            "(shares sum to 1)."),
    "PR1b": "(secondary, Holm family R2-A with PR1 and PR2): s_contact - s_ret > 0 with CI > 0 (s_contact = s_E2).",
    "PR2": ("LOCALISED KEEP MORE EARLY: mean RETENTION_RATIO_early(bottom O2r_resid tercile) - mean(top tercile) > 0 "
            "with CI > 0, AND the partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 < 0 (CI < 0). The "
            "latter is flagged 'replication on the same frame as EXP8, not new evidence'."),
    "PR3": "(descriptive, not tested): the sign of D_rho, i.e. whether late retention probability is lower for "
           "integrating (top-tercile) concepts.",
    "verdict_rule": "per clause: SUPPORTED (CI on the predicted side) / NOT SUPPORTED (CI covers 0) / REVERSED "
                    "(CI on the opposite side); evaluated separately on DEV and on held-out.",
    "holm_family_R2A": ["PR1", "PR1b", "PR2"],
}

VARIANTS = {   # name: (strata, subset, y column, decomp suffix)
    "i_pooled": ("none", None, "O2r_resid", ""),
    "ii_vol_PRIMARY": ("vol", None, "O2r_resid", ""),
    "iii_vol_med_adjusted": ("vol_med", None, "O2r_resid", ""),
    "iv_vol_noMed_PR1": ("vol", "nomed", "O2r_resid", ""),
    "v_minn3": ("vol", None, "O2r_resid", "_mn3"),
    "v_minn5": ("vol", None, "O2r_resid", "_mn5"),
    "v_minn3_noMed": ("vol", "nomed", "O2r_resid", "_mn3"),
    "v_minn5_noMed": ("vol", "nomed", "O2r_resid", "_mn5"),
    "vi_O2r_m50": ("vol", None, "O2r_m50", ""),
    "vi_O1b_sustained_only": ("vol", "o1b", "O2r_resid", ""),
    "viii_onset_restricted": ("vol", None, "O2r_resid", "_onset"),
    "viii_onset_restricted_noMed": ("vol", "nomed", "O2r_resid", "_onset"),
    "ix_noEXP6_noMed": ("vol", "noexp6_nomed", "O2r_resid", ""),
}
BOOT_KEYS = ["D_E2", "D_M", "D_rho", "diff_explore_ret", "diff_contact_ret", "s_ret"]


def write_prereg() -> str:
    p = RES / "preregistration_R2.json"
    if not p.exists():
        jdump(PREREG, p)
    return sha256_file(p)


def load_table(scope: str) -> pd.DataFrame:
    J = pd.read_parquet(DATA / "joined.parquet")
    Dd = pd.read_parquet(DATA / "decomp_inputs.parquet")
    SF = load_outcomes()
    O = SF.dev() if scope == "dev" else SF.all()
    T = J.merge(Dd, on="ci").merge(O.drop(columns=["split"]), on="ci", how="inner")
    T["logvol_early"] = np.log(T.early_volume)
    return T


def arrays(T: pd.DataFrame, suffix: str, ycol: str, tby=None, rs=None) -> dict:
    return {"E2": T[f"E2{suffix}"].to_numpy(float), "EH": T[f"EH{suffix}"].to_numpy(float),
            "Bn": T[f"Bn{suffix}"].to_numpy(float), "y": T[ycol].to_numpy(float),
            "logvol_early": T.logvol_early.to_numpy(float), "med": T.med_home.to_numpy(int),
            "tby": None if tby is None else T[tby].to_numpy(), "rs": None if rs is None else T[rs].to_numpy()}


def subset(T: pd.DataFrame, which: str | None) -> pd.DataFrame:
    if which is None:
        return T
    if which == "nomed":
        return T[T.med_home == 0]
    if which == "o1b":   # plan says 'O1c = 1'; O1c is continuous in EXP8, the binary sustained-uptake outcome is O1b
        return T[T.O1b == 1]
    if which == "noexp6_nomed":
        return T[(T.med_home == 0) & (T.in_exp6 == 0)]
    raise ValueError(which)


def _job(args):
    name, T, spec, tby, rs, seed, n_boot = args
    strata, sub, ycol, suf = spec
    S = subset(T, sub)
    S = S[np.isfinite(S[ycol])]
    res = DC.run_variant(arrays(S, suf, ycol, tby, rs), {"strata": strata}, np.random.default_rng(seed), n_boot)
    B = res.pop("_boot", None)
    res["boot_quantiles"] = {k: np.nanpercentile(B[k], [2.5, 5, 25, 50, 75, 95, 97.5]).tolist()
                             for k in BOOT_KEYS} if B is not None else None
    res["spec"] = {"strata": strata, "subset": sub, "y": ycol, "counts_suffix": suf or "min_n=2"}
    tn = min(res["point"]["n_top"], res["point"]["n_bot"])
    res["ci_reported"] = tn >= DC.MIN_PER_TERCILE_CI
    return name, res


def early_ratio(T: pd.DataFrame, seed: int, n_boot: int, tby=None) -> dict:
    """PR2: RETENTION_RATIO_early bottom - top tercile (concepts with >= 1 off-home contact) + psp given B5."""
    S = T[np.isfinite(T.O2r_resid) & (T.RETENTION_RATIO_missing == 0)]
    y = S.O2r_resid.to_numpy()
    rr = S.RETENTION_RATIO_early.to_numpy()
    tb = None if tby is None else S[tby].to_numpy()
    rng = np.random.default_rng(seed)

    def diff(idx):
        top, bot = DC.terciles(y[idx], None if tb is None else tb[idx])
        return rr[idx][bot].mean() - rr[idx][top].mean()
    n = len(S)
    pt = diff(np.arange(n))
    bs = np.array([diff(rng.integers(0, n, n)) for _ in range(n_boot)])
    ps = psp_boot(rr, y, S[B5].to_numpy(float), None, n_boot, seed + 7)
    top, bot = DC.terciles(y, tb)
    return {"n": n, "mean_bottom": float(rr[bot].mean()), "mean_top": float(rr[top].mean()),
            "diff_bottom_minus_top": float(pt), "ci": np.percentile(bs, [2.5, 97.5]).tolist(),
            "se": float(bs.std(ddof=1)), "p_two_sided": float(min(1, 2 * min((bs <= 0).mean(), (bs >= 0).mean()))),
            "psp_given_B5": {k: ps[k] for k in ("n", "rho", "ci", "se", "p")},
            "note_psp": "replication on the same frame as EXP8, not new evidence"}


def analyze(T: pd.DataFrame, label: str, seed: int, tby=None, rs=None, n_boot: int = N_BOOT,
            variants=VARIANTS, workers: int = 13) -> dict:
    jobs = [(name, T, spec, tby, rs, seed + k, n_boot) for k, (name, spec) in enumerate(variants.items())]
    with ProcessPoolExecutor(min(workers, len(jobs))) as ex:
        res = dict(ex.map(_job, jobs))
    out = {"label": label, "n_concepts_with_outcome": int(np.isfinite(T.O2r_resid).sum()), "variants": res}
    S = T[np.isfinite(T.O2r_resid)]
    top, bot = DC.terciles(S.O2r_resid.to_numpy(), None if tby is None else S[tby].to_numpy())
    a = arrays(S, "", "O2r_resid")
    out["das_gupta_pooled"] = DC.das_gupta(a["E2"], a["EH"], a["Bn"], top, bot)
    out["concept_level_cov"] = DC.concept_cov(a["E2"], a["EH"], a["Bn"])
    out["early_ratio_PR2"] = early_ratio(T, seed + 99, n_boot, tby)
    out["early_ratio_PR2_noMed"] = early_ratio(T[T.med_home == 0], seed + 98, n_boot, tby)
    return out


def verdicts(res: dict) -> dict:
    v = res["variants"]["iv_vol_noMed_PR1"]
    er = res["early_ratio_PR2"]
    p1 = v["p_two_sided"]["diff_explore_ret"]
    p1b = v["p_two_sided"]["diff_contact_ret"]
    p2 = max(er["p_two_sided"], er["psp_given_B5"]["p"])
    ph = holm([p1, p1b, p2])
    pr2a = DC.verdict(er["ci"])
    pr2b = DC.verdict([-er["psp_given_B5"]["ci"][1], -er["psp_given_B5"]["ci"][0]])
    pr2 = "SUPPORTED" if (pr2a == pr2b == "SUPPORTED") else ("REVERSED" if "REVERSED" in (pr2a, pr2b)
                                                              else "NOT SUPPORTED")
    return {"PR1": {"verdict": DC.verdict(v["ci"]["diff_explore_ret"]), "s_explore_minus_s_ret": v["point"]["diff_explore_ret"],
                    "ci": v["ci"]["diff_explore_ret"], "s_ret": v["point"]["s_ret"], "s_ret_ci": v["ci"]["s_ret"],
                    "s_ret_below_0.5": bool(v["ci"]["s_ret"][1] < 0.5), "p": p1, "p_holm": ph[0]},
            "PR1b": {"verdict": DC.verdict(v["ci"]["diff_contact_ret"]), "s_contact_minus_s_ret": v["point"]["diff_contact_ret"],
                     "ci": v["ci"]["diff_contact_ret"], "p": p1b, "p_holm": ph[1]},
            "PR2": {"verdict": pr2, "clause_diff": pr2a, "clause_psp_negative": pr2b, "p_iut": p2, "p_holm": ph[2],
                    "diff": er["diff_bottom_minus_top"], "diff_ci": er["ci"], "psp": er["psp_given_B5"]["rho"],
                    "psp_ci": er["psp_given_B5"]["ci"]},
            "PR3_descriptive": {"D_rho": v["point"]["D_rho"], "ci": v["ci"]["D_rho"],
                                "sign": "negative (integrating concepts keep a SMALLER share of entered fields)"
                                if v["point"]["D_rho"] < 0 else "positive (integrating concepts keep a LARGER share)"}}


def placebo(T: pd.DataFrame, seed: int, n: int = 200, by: str = "group") -> dict:
    """T9: shuffle O2r_resid within group; primary (ii) and PR1 (iv) point estimates under the null."""
    rng = np.random.default_rng(seed)
    S = T[np.isfinite(T.O2r_resid)].copy()
    out = {}
    for name in ("ii_vol_PRIMARY", "iv_vol_noMed_PR1"):
        strata, sub, ycol, suf = VARIANTS[name]
        X = subset(S, sub).copy()
        vals = {k: [] for k in ("diff_explore_ret", "D_E2", "D_M", "D_rho", "D_total")}
        for _ in range(n):
            X["y_shuf"] = X.groupby(by).O2r_resid.transform(lambda s: rng.permutation(s.to_numpy()))
            r = DC.run_variant(arrays(X, suf, "y_shuf"), {"strata": strata}, None, 0)["point"]
            for k in vals:
                vals[k].append(r[k])
        out[name] = {k: {"mean": float(np.nanmean(v)), "q025_q975": np.nanpercentile(v, [2.5, 97.5]).tolist(),
                         "nan_share": float(np.mean(~np.isfinite(v)))} for k, v in vals.items()}
    out["note"] = ("under the null the total gap D_total is ~0, so shares are unstable by construction; the D_k "
                   "log-ratios are the stable quantities")
    return out


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", default="dev", choices=["dev", "heldout"])
    ap.add_argument("--n_boot", type=int, default=N_BOOT)
    a = ap.parse_args()
    h = write_prereg()
    logger.info(f"pre-registration sha256 {h}")
    T = load_table(a.scope)
    if a.scope == "dev":
        res = analyze(T, "DEV", SEED + 400, n_boot=a.n_boot)
        res["verdicts"] = verdicts(res)
        res["dev_groups"] = {g: analyze(T[T.group == g], f"DEV_{g}", SEED + 410 + k, n_boot=a.n_boot,
                                        variants={kk: VARIANTS[kk] for kk in ("ii_vol_PRIMARY", "i_pooled")})
                             for k, g in enumerate(["CS", "Eng", "BGM", "Med"])}
        # T5: second bootstrap seed for the PR1 variant
        _, r2 = _job(("iv_seed2", T, VARIANTS["iv_vol_noMed_PR1"], None, None, SEED + 777, a.n_boot))
        v1 = res["variants"]["iv_vol_noMed_PR1"]["ci"]
        res["T5_second_seed"] = {k: {"seed1": v1[k], "seed2": r2["ci"][k],
                                     "max_end_shift": float(np.max(np.abs(np.subtract(v1[k], r2["ci"][k]))))}
                                 for k in ("diff_explore_ret", "diff_contact_ret", "D_E2", "D_M", "D_rho")}
        res["T9_placebo"] = placebo(T, SEED + 900)
        res["resampling_unit"] = "concept (2,000 bootstrap resamples within DEV; terciles and volume quintiles recomputed)"
        res["prereg_sha256"] = h
        res["Source"] = "s4_decomp.py --scope dev; inputs data/decomp_inputs.parquet (S3), EXP8 outcomes (DEV rows)"
        jdump(res, RES / "decomposition_dev.json")
        v = res["verdicts"]
        logger.info(f"DEV PR1 {v['PR1']['verdict']} diff {v['PR1']['s_explore_minus_s_ret']:.3f} {v['PR1']['ci']}; "
                    f"PR1b {v['PR1b']['verdict']}; PR2 {v['PR2']['verdict']} ({v['PR2']['clause_diff']}, "
                    f"{v['PR2']['clause_psp_negative']}); D_rho {v['PR3_descriptive']['D_rho']:.3f}")
        update_status("S4_decomposition_DEV", {"dev_verdicts": {k: v[k]["verdict"] for k in ("PR1", "PR1b", "PR2")}})
        return
    # ------------------------------------------------------------------ held-out (after the one-time unseal)
    H = T[T.split != "DEV"].copy()
    out = {"disclosure": DISCLOSURE, "units": {}}
    for k, u in enumerate(UNITS):
        U = H[H.unit == u]
        n_y = int(np.isfinite(U.O2r_resid).sum())
        r = analyze(U, u, SEED + 500 + k, n_boot=a.n_boot)
        r["verdicts"] = verdicts(r)
        r["n_with_outcome"] = n_y
        out["units"][u] = r
        logger.info(f"{u}: n_y {n_y}; PR1 {r['verdicts']['PR1']['verdict']} "
                    f"{r['verdicts']['PR1']['s_explore_minus_s_ret']:.3f} {r['verdicts']['PR1']['ci']}")
    H4 = H[H.unit.isin(HELD_GROUPS)]
    r = analyze(H4, "HELDOUT4_pooled", SEED + 600, tby="unit", rs="unit", n_boot=a.n_boot)
    r["verdicts"] = verdicts(r)
    out["pooled_heldout4"] = r
    HC = H[H.split == "COHORT"]
    r = analyze(HC, "COHORT_pooled", SEED + 610, tby="unit", rs="unit", n_boot=a.n_boot)
    r["verdicts"] = verdicts(r)
    out["pooled_cohort"] = r
    # DL pooling over the held-out groups (MATHDEC excluded when < 150 concepts with an outcome)
    dl = {}
    for key, var in (("diff_explore_ret", "iv_vol_noMed_PR1"), ("diff_contact_ret", "iv_vol_noMed_PR1"),
                     ("D_E2", "ii_vol_PRIMARY"), ("D_M", "ii_vol_PRIMARY"), ("D_rho", "ii_vol_PRIMARY"),
                     ("diff_explore_ret_primary", "ii_vol_PRIMARY")):
        kk = key.replace("_primary", "")
        units = [u for u in HELD_GROUPS if out["units"][u]["n_with_outcome"] >= 150
                 and out["units"][u]["variants"][var]["ci_reported"]]
        b = [out["units"][u]["variants"][var]["point"][kk] for u in units]
        se = [out["units"][u]["variants"][var]["se"][kk] for u in units]
        dl[key] = {"variant": var, "units": units, **dersimonian_laird(b, se)}
    out["DL_heldout_groups"] = dl
    out["Source"] = "s4_decomp.py --scope heldout (after s7_seal.py); frozen definitions from results/frozen_spec.json"
    jdump(out, RES / "decomposition_heldout.json")
    update_status("S4_decomposition_heldout",
                  {"heldout_verdicts_pooled4": {k: out["pooled_heldout4"]["verdicts"][k]["verdict"]
                                                for k in ("PR1", "PR1b", "PR2")}})


if __name__ == "__main__":
    main()
