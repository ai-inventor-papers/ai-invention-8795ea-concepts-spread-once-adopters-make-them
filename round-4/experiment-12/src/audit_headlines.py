#!/usr/bin/env python3
"""HEADLINE AUDIT (independent re-derivation + placebo). Reads the raw per-concept files (EXP5 frame, EXP8 outcomes and
features, this artifact's decomp_inputs / open_features / typology assignments) and recomputes each headline number with
its own pandas/scipy code (no import of lib/decomp.py, lib/typology.py or rq1stats). Then reruns each test on shuffled
input and checks that it FAILS there. Writes results/audit_headlines.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import rankdata
from sklearn.metrics import adjusted_rand_score

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
from common import E5, E8  # noqa: E402  (input-path constants only)

RNG = np.random.default_rng(7)
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]


def load() -> pd.DataFrame:
    fr = pd.read_csv(E5 / "frame_concepts.csv")
    fr["split2"] = np.where(fr.split.str.startswith("HELDOUT"), "HELDOUT", fr.split)
    fr["unit"] = np.where(fr.split2 == "COHORT", np.where(fr.group.isin(["CS", "Eng", "BGM", "Med"]), "COH_DEVHOME",
                                                          "COH_OTHER"), fr.group)
    fr["med"] = fr.home.astype(str).map(lambda h: "27" in h.replace("|", ";").split(";"))
    oc = pd.read_parquet(E8 / "data/outcomes.parquet", columns=["ci", "O2r_resid"])
    fb = pd.read_parquet(E8 / "data/features_basic.parquet",
                         columns=["ci", "RETENTION_RATIO_early", "RETENTION_RATIO_missing"] + B5)
    di = pd.read_parquet(ROOT / "data/decomp_inputs.parquet", columns=["ci", "E2", "EH", "Bn"])
    of = pd.read_parquet(ROOT / "open_features.parquet", columns=["ci", "OPEN_all", "OPEN_home", "OPEN_size"])
    pc = pd.concat([pd.read_parquet(ROOT / "results/typology_dev_assign.parquet", columns=["ci", "PC1"]),
                    pd.read_parquet(ROOT / "results/typology_heldout_assign.parquet", columns=["ci", "PC1"])])
    T = (fr[["ci", "split2", "unit", "group", "med", "early_volume", "label_coverage_early"]]
         .merge(oc, on="ci").merge(fb, on="ci").merge(di, on="ci").merge(of, on="ci").merge(pc, on="ci"))
    T["lv"] = np.log(T.early_volume)
    return T


def cell_gap(df: pd.DataFrame, y: str, within: str | None) -> np.ndarray:
    """n-weighted mean over (within-level x volume-quintile) cells of log(top/bottom) factor ratios."""
    num, W = np.zeros(3), 0.0
    for _, g in (df.groupby(within) if within else [(None, df)]):
        lo, hi = np.quantile(g[y], [1 / 3, 2 / 3])
        g = g.assign(top=g[y] > hi, bot=g[y] <= lo,
                     q=np.searchsorted(np.quantile(g.lv, [0.2, 0.4, 0.6, 0.8]), g.lv, side="right"))
        for _, c in g.groupby("q"):
            t, b = c[c.top], c[c.bot]
            if len(t) == 0 or len(b) == 0 or min(t.E2.sum(), b.E2.sum(), t.Bn.sum(), b.Bn.sum()) <= 0:
                continue
            ft = np.array([t.E2.mean(), t.EH.sum() / t.E2.sum(), t.Bn.sum() / t.EH.sum()])
            fb = np.array([b.E2.mean(), b.EH.sum() / b.E2.sum(), b.Bn.sum() / b.EH.sum()])
            w = len(t) + len(b)
            num += w * (np.log(ft) - np.log(fb))
            W += w
    return num / W


def pr1(D: np.ndarray) -> dict:
    s = D / D.sum()
    return {"D_E2": D[0], "D_M": D[1], "D_rho": D[2], "D_total": D.sum(), "s_explore_minus_s_ret": s[0] + s[1] - s[2]}


def boot_pr1(df, y, within, n=300) -> list[float]:
    v = []
    for _ in range(n):
        idx = np.concatenate([RNG.choice(np.flatnonzero(df[within].to_numpy() == u), (df[within] == u).sum())
                              for u in df[within].unique()]) if within else RNG.integers(0, len(df), len(df))
        v.append(pr1(cell_gap(df.iloc[idx], y, within))["s_explore_minus_s_ret"])
    return np.percentile(v, [2.5, 97.5]).tolist()


def partial_spearman(x, y, Z) -> float:
    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Z).all(1)      # complete cases
    x, y, Z = x[ok], y[ok], Z[ok]
    R = np.column_stack([np.ones(len(x))] + [rankdata(z) for z in Z.T])
    rx = rankdata(x) - R @ np.linalg.lstsq(R, rankdata(x), rcond=None)[0]
    ry = rankdata(y) - R @ np.linalg.lstsq(R, rankdata(y), rcond=None)[0]
    return float(np.corrcoef(rx, ry)[0, 1])


def boot_ps(x, y, Z, n=300) -> list[float]:
    v = []
    for _ in range(n):
        i = RNG.integers(0, len(x), len(x))
        v.append(partial_spearman(x[i], y[i], Z[i]))
    return np.percentile(v, [2.5, 97.5]).tolist()


def shuffle_within(df, col, by="group"):
    return df.groupby(by)[col].transform(lambda s: RNG.permutation(s.to_numpy()))


def main() -> None:
    T = load()
    Y = T[T.O2r_resid.notna()]
    pipe_d = json.loads((ROOT / "results/decomposition_dev.json").read_text())
    pipe_h = json.loads((ROOT / "results/decomposition_heldout.json").read_text())
    pipe_t = json.loads((ROOT / "results/trajectories_dev.json").read_text())
    out = {"headlines": {}, "placebo": {}}
    # --- PR1 (variant iv: volume-stratified, Medicine excluded)
    samples = {"DEV": (Y[(Y.split2 == "DEV") & ~Y.med], None, pipe_d["variants"]["iv_vol_noMed_PR1"]["point"]),
               "HELDOUT4": (Y[(Y.split2 == "HELDOUT") & ~Y.med], "unit",
                            pipe_h["pooled_heldout4"]["variants"]["iv_vol_noMed_PR1"]["point"]),
               "COHORT": (Y[(Y.split2 == "COHORT") & ~Y.med], "unit",
                          pipe_h["pooled_cohort"]["variants"]["iv_vol_noMed_PR1"]["point"])}
    for k, (df, within, p) in samples.items():
        mine = pr1(cell_gap(df, "O2r_resid", within))
        out["headlines"][f"PR1_{k}"] = {"mine": mine, "pipeline_diff": p["diff_explore_ret"],
                                        "abs_diff": abs(mine["s_explore_minus_s_ret"] - p["diff_explore_ret"]),
                                        "mine_ci_300boot": boot_pr1(df, "O2r_resid", within)}
        # placebo: outcome shuffled within home group -> the PR1 test must fail (CI not strictly > 0 or D_total ~ 0)
        dfs = df.assign(y_shuf=shuffle_within(df, "O2r_resid"))
        pm = pr1(cell_gap(dfs, "y_shuf", within))
        pci = boot_pr1(dfs, "y_shuf", within, 200)
        out["placebo"][f"PR1_{k}"] = {"D_total_shuffled": pm["D_total"], "ci_shuffled": pci,
                                      "test_fails_on_shuffle": bool(not (pci[0] > 0) or abs(pm["D_total"]) < 0.2)}
    # --- PR2 partial clause and OPEN ~ PC1 partial (DEV)
    D = T[(T.split2 == "DEV") & T.O2r_resid.notna() & (T.RETENTION_RATIO_missing == 0)]
    x, y, Z = D.RETENTION_RATIO_early.to_numpy(), D.O2r_resid.to_numpy(), D[B5].to_numpy()
    ps = partial_spearman(x, y, Z)
    out["headlines"]["PR2_psp_DEV"] = {"mine": ps, "pipeline": pipe_d["verdicts"]["PR2"]["psp"],
                                       "abs_diff": abs(ps - pipe_d["verdicts"]["PR2"]["psp"]), "mine_ci": boot_ps(x, y, Z)}
    xs = RNG.permutation(x)
    out["placebo"]["PR2_psp_DEV"] = {"shuffled": partial_spearman(xs, y, Z), "ci": boot_ps(xs, y, Z, 200)}
    out["placebo"]["PR2_psp_DEV"]["test_fails_on_shuffle"] = bool(out["placebo"]["PR2_psp_DEV"]["ci"][1] >= 0)
    for b in ("all", "home", "size"):
        Dv = T[(T.split2 == "DEV") & T[f"OPEN_{b}"].notna()]
        Z2 = Dv[B5 + ["label_coverage_early"]].to_numpy()
        ps = partial_spearman(Dv[f"OPEN_{b}"].to_numpy(), Dv.PC1.to_numpy(), Z2)
        pp = pipe_t["open_on_axis"]["pooled"]["PC1"][b]["partial_given_B5_labelcov"]["rho"]
        out["headlines"][f"OPEN_{b}_PC1_partial_DEV"] = {"mine": ps, "pipeline": pp, "abs_diff": abs(ps - pp)}
        xf = RNG.permutation(Dv[f"OPEN_{b}"].to_numpy())            # full permutation = the pure null
        ci = boot_ps(xf, Dv.PC1.to_numpy(), Z2, 200)
        # within-group shuffles keep each group's OPEN mean (group is not a covariate), so they form a
        # composition-only null: the observed partial must lie far outside its 100-draw range
        wg = [partial_spearman(shuffle_within(Dv, f"OPEN_{b}").to_numpy(), Dv.PC1.to_numpy(), Z2) for _ in range(100)]
        out["placebo"][f"OPEN_{b}_PC1_partial_DEV"] = {
            "full_permutation": partial_spearman(xf, Dv.PC1.to_numpy(), Z2), "full_permutation_ci": ci,
            "within_group_shuffle_range_100": [float(min(wg)), float(max(wg))], "observed": ps,
            "test_fails_on_shuffle": bool(ci[0] <= 0 <= ci[1] and ps > max(wg))}
    # --- DTW vs HMM agreement (the typology-naming failure)
    A = pd.read_parquet(ROOT / "results/typology_dev_assign.parquet")
    ari = adjusted_rand_score(A.dtw_class, A.hmm_class)
    out["headlines"]["ARI_DTW_HMM_DEV"] = {"mine": ari, "pipeline": pipe_t["hmm"]["ari_dtw_hmm"],
                                           "abs_diff": abs(ari - pipe_t["hmm"]["ari_dtw_hmm"])}
    out["placebo"]["ARI_DTW_HMM_DEV"] = {"shuffled": adjusted_rand_score(A.dtw_class, RNG.permutation(A.hmm_class))}
    out["all_headlines_match_1e-9"] = bool(all(v["abs_diff"] < 1e-9 for v in out["headlines"].values()))
    out["all_placebos_fail"] = bool(all(v.get("test_fails_on_shuffle", True) for v in out["placebo"].values()))
    (ROOT / "results/audit_headlines.json").write_text(json.dumps(out, indent=1, default=float))
    for k, v in out["headlines"].items():
        print(f"{k}: diff {v['abs_diff']:.1e}")
    for k, v in out["placebo"].items():
        print(f"placebo {k}: {json.dumps(v, default=float)[:200]}")
    print("MATCH", out["all_headlines_match_1e-9"], "PLACEBOS FAIL", out["all_placebos_fail"])


if __name__ == "__main__":
    main()
