#!/usr/bin/env python3
"""T7 INDEPENDENT RE-DERIVATION (after the unseal): minimal pandas code, sharing NO analysis code with s4/s5, recomputes
(a) the held-out group-level decomposition D_k and shares (pooled variant i and volume-stratified variant ii) per unit
to 1e-9, and (b) the OPEN_b ~ PC1 Spearman per held-out unit to 1e-6, and compares with the pipeline JSONs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
from common import E5, E8  # noqa: E402  (only the input-path constants; no analysis code)


def shares(df: pd.DataFrame) -> dict:
    lo, hi = df.O2r_resid.quantile([1 / 3, 2 / 3])
    top, bot = df[df.O2r_resid > hi], df[df.O2r_resid <= lo]
    f = lambda g: np.array([g.E2.mean(), g.EH.sum() / g.E2.sum(), g.Bn.sum() / g.EH.sum()])  # noqa: E731
    D = np.log(f(top)) - np.log(f(bot))
    return {"D_E2": D[0], "D_M": D[1], "D_rho": D[2], "s_E2": D[0] / D.sum(), "s_rho": D[2] / D.sum()}


def shares_vol(df: pd.DataFrame) -> dict:
    lo, hi = df.O2r_resid.quantile([1 / 3, 2 / 3])
    df = df.assign(top=df.O2r_resid > hi, bot=df.O2r_resid <= lo)
    edges = np.quantile(df.lv, [0.2, 0.4, 0.6, 0.8])
    df["q"] = np.searchsorted(edges, df.lv, side="right")
    num, W = np.zeros(3), 0.0
    for _, g in df.groupby("q"):
        t, b = g[g.top], g[g.bot]
        f = lambda x: np.array([x.E2.mean(), x.EH.sum() / x.E2.sum(), x.Bn.sum() / x.EH.sum()])  # noqa: E731
        w = len(t) + len(b)
        num += w * (np.log(f(t)) - np.log(f(b)))
        W += w
    D = num / W
    return {"D_E2": D[0], "D_M": D[1], "D_rho": D[2], "s_E2": D[0] / D.sum(), "s_rho": D[2] / D.sum()}


def main() -> None:
    fr = pd.read_csv(E5 / "frame_concepts.csv")
    fr["unit"] = np.where(fr.split == "COHORT", np.where(fr.group.isin(["CS", "Eng", "BGM", "Med"]), "COH_DEVHOME",
                                                         "COH_OTHER"), fr.group)
    oc = pd.read_parquet(E8 / "data/outcomes.parquet", columns=["ci", "O2r_resid"])
    di = pd.read_parquet(ROOT / "data/decomp_inputs.parquet", columns=["ci", "E2", "EH", "Bn"])
    T = fr[["ci", "unit", "split", "early_volume"]].merge(oc, on="ci").merge(di, on="ci")
    T["lv"] = np.log(T.early_volume)
    T = T[(T.split != "DEV") & T.O2r_resid.notna()]
    pipe = json.loads((ROOT / "results/decomposition_heldout.json").read_text())
    out = {"decomposition": {}, "open_pc1": {}}
    worst = 0.0
    for u, g in T.groupby("unit"):
        for var, fn in (("i_pooled", shares), ("ii_vol_PRIMARY", shares_vol)):
            mine = fn(g)
            p = pipe["units"][u]["variants"][var]["point"]
            d = max(abs(mine[k] - p[k]) for k in mine)
            worst = max(worst, d)
            out["decomposition"][f"{u}/{var}"] = {"max_abs_diff": d, "n": len(g)}
    out["decomposition_max_abs_diff"] = worst
    out["decomposition_pass_1e-9"] = bool(worst < 1e-9)
    tj = json.loads((ROOT / "results/trajectories_heldout.json").read_text())
    pa = pd.read_parquet(ROOT / "results/typology_heldout_assign.parquet")
    of = pd.read_parquet(ROOT / "open_features.parquet", columns=["ci", "OPEN_all", "OPEN_home", "OPEN_size"])
    X = fr[["ci", "unit"]].merge(pa, on="ci").merge(of, on="ci")
    w2 = 0.0
    for u, g in X.groupby("unit"):
        for b in ("all", "home", "size"):
            m = g[f"OPEN_{b}"].notna()
            rho = spearmanr(g[f"OPEN_{b}"][m], g.PC1[m]).statistic
            p = tj["open_on_axis_units_PC1"][u][b]["spearman"]["rho"]
            w2 = max(w2, abs(rho - p))
            out["open_pc1"][f"{u}/{b}"] = {"mine": float(rho), "pipeline": p}
    out["open_pc1_max_abs_diff"] = w2
    out["open_pc1_pass_1e-6"] = bool(w2 < 1e-6)
    (ROOT / "results/T7_rederivation.json").write_text(json.dumps(out, indent=1, default=float))
    print(f"T7 decomposition max diff {worst:.2e} (pass {worst < 1e-9}); OPEN~PC1 max diff {w2:.2e} (pass {w2 < 1e-6})")


if __name__ == "__main__":
    main()
