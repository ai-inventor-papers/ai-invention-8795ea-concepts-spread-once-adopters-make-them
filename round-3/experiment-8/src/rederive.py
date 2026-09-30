#!/usr/bin/env python3
"""Independent re-derivation of the HEADLINE numbers from raw tables, through a different code path
(pandas rank + numpy normal equations + analytic Fisher-z SE + own DL; scipy/sklearn metrics on raw predictions),
plus shuffled-input versions that must FAIL. Writes results/rederive.json.

  H1  pooled held-out psp | B5 of every frozen top-10 indicator of the continuous outcomes (point, CI, sign)
  H2  learned / best-single vs B5 on the pooled held-out groups (Spearman or AUC from raw predictions)
  H3  shuffled controls: outcome permuted within unit -> pooled psp of the #1 indicator and learned-vs-B5 deltas ~ 0"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import norm, spearmanr
from sklearn.metrics import roc_auc_score

from common import DATA, HELD_GROUPS, RES, SEED, jdump

B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]


def psp_ne(d: pd.DataFrame, x: str, y: str) -> tuple[float, int, int]:
    d = d[[x, y, "t0"] + B5].dropna()
    n = len(d)
    if n < 20 or d[x].nunique() < 3:
        return float("nan"), n, 0
    Z = [np.ones(n)] + [d[c].rank().to_numpy() for c in B5] + \
        [(d.t0 == u).to_numpy(float) for u in sorted(d.t0.unique())[1:]]
    Z = np.column_stack(Z)
    P = Z @ np.linalg.pinv(Z.T @ Z) @ Z.T
    a = d[x].rank().to_numpy(); a = a - P @ a
    b = d[y].rank().to_numpy(); b = b - P @ b
    return float(a @ b / math.sqrt((a @ a) * (b @ b))), n, Z.shape[1]


def dl(z: np.ndarray, v: np.ndarray) -> tuple[float, float]:
    w = 1 / v
    zf = (w * z).sum() / w.sum()
    Q = (w * (z - zf) ** 2).sum()
    k = len(z)
    c = w.sum() - (w ** 2).sum() / w.sum()
    t2 = max(0.0, (Q - (k - 1)) / c) if k > 1 else 0.0
    ws = 1 / (v + t2)
    return float((ws * z).sum() / ws.sum()), float(math.sqrt(1 / ws.sum()))


def pooled(A: pd.DataFrame, x: str, y: str) -> dict:
    zs, vs = [], []
    for u in HELD_GROUPS:
        r, n, k = psp_ne(A[A.unit == u], x, y)
        if np.isfinite(r) and n - k - 3 > 0:
            zs.append(math.atanh(r)); vs.append(1 / (n - k - 3))
    if not zs:
        return {"pooled": None}
    m, s = dl(np.array(zs), np.array(vs))
    return {"pooled": math.tanh(m), "ci": [math.tanh(m - 1.96 * s), math.tanh(m + 1.96 * s)],
            "p": float(2 * norm.sf(abs(m / s)))}


def main() -> None:
    A = pd.read_parquet(DATA / "analysis_table.parquet")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    summ = json.loads((RES / "heldout_summary.json").read_text())
    out = {"H1_pooled_psp": [], "H2_learned": [], "H3_shuffled": {}}
    for o in ("O1c", "O2r_m50", "O2r_resid", "O4"):
        pipe = {r["indicator"]: r for r in summ.get(o, [])}
        for d_ in spec["top10"].get(o, []):
            ind = d_["indicator"]
            r = pooled(A, ind, o)
            p = pipe.get(ind, {})
            out["H1_pooled_psp"].append({"outcome": o, "indicator": ind, "rederived": r.get("pooled"),
                                         "rederived_ci": r.get("ci"), "pipeline": p.get("pooled"),
                                         "pipeline_ci": p.get("pooled_ci"),
                                         "abs_diff": (abs(r["pooled"] - p["pooled"]) if r.get("pooled") is not None
                                                      and p.get("pooled") is not None else None),
                                         "same_sign": (np.sign(r["pooled"]) == np.sign(p["pooled"]))
                                         if r.get("pooled") is not None and p.get("pooled") is not None else None,
                                         "ci_excludes_0_rederived": bool(r.get("ci") and (r["ci"][0] > 0 or r["ci"][1] < 0)),
                                         "ci_excludes_0_pipeline": bool(p.get("pooled_ci") and (p["pooled_ci"][0] > 0 or p["pooled_ci"][1] < 0))})
    # H2 learned vs B5 from raw predictions
    pr = pd.read_parquet(RES / "heldout_predictions.parquet")
    lv = json.loads((RES / "learned_vs_single_heldout.json").read_text())
    H = A[A.unit.isin(HELD_GROUPS)].merge(pr, on="ci")
    rng = np.random.default_rng(SEED)
    for o in ("O1c", "O2r_m50", "O2r_resid", "O4", "O1b", "O3", "O5", "O5_WW"):
        cols = [c for c in pr.columns if c.startswith(f"{o}__")]
        if not cols:
            continue
        d = H.dropna(subset=[o])
        rec = {"outcome": o, "n": len(d)}
        for c in cols:
            k = c.split("__")[1]
            if o in ("O1b", "O3", "O5", "O5_WW"):
                if d[o].sum() < 20:
                    continue
                m = roc_auc_score(d[o], d[c])
            else:
                m = spearmanr(d[c], d[o])[0]
            rec[k] = float(m)
            pv = lv.get(o, {}).get("POOLED_HELDOUT", {}).get(k, {}).get("metric")
            rec[f"{k}_pipeline"] = pv
        out["H2_learned"].append(rec)
    # H3 shuffled controls
    Ash = A.copy()
    for u in HELD_GROUPS:
        m = (Ash.unit == u).to_numpy()
        for o in ("O2r_resid", "O1c", "O2r_m50", "O4"):
            Ash.loc[m, o] = rng.permutation(Ash.loc[m, o].to_numpy())
    sh = {}
    for o in ("O1c", "O2r_m50", "O2r_resid", "O4"):
        if spec["top10"].get(o):
            ind = spec["top10"][o][0]["indicator"]
            r = pooled(Ash, ind, o)
            sh[f"{o}|{ind}"] = {"pooled": r.get("pooled"), "ci": r.get("ci"),
                                "ci_excludes_0": bool(r.get("ci") and (r["ci"][0] > 0 or r["ci"][1] < 0))}
    Hs = Ash[Ash.unit.isin(HELD_GROUPS)].merge(pr, on="ci")
    for o in ("O2r_resid", "O2r_m50"):
        d = Hs.dropna(subset=[o])
        for k in ("B5", "linear_all", "EBM"):
            c = f"{o}__{k}"
            if c in d:
                sh[f"learned_shuffled|{o}|{k}"] = float(spearmanr(d[c], d[o])[0])
    out["H3_shuffled"] = sh
    diffs = [r["abs_diff"] for r in out["H1_pooled_psp"] if r["abs_diff"] is not None]
    agree = [r["ci_excludes_0_rederived"] == r["ci_excludes_0_pipeline"] for r in out["H1_pooled_psp"]]
    out["summary"] = {"H1_max_abs_diff_point": max(diffs) if diffs else None,
                      "H1_share_same_significance_call": float(np.mean(agree)) if agree else None,
                      "H1_all_same_sign": bool(all(r["same_sign"] for r in out["H1_pooled_psp"] if r["same_sign"] is not None)),
                      "H2_max_abs_diff": max([abs(r[k] - r[f"{k}_pipeline"]) for r in out["H2_learned"] for k in
                                              ("B5", "B5_best_single", "linear_all", "EBM")
                                              if k in r and r.get(f"{k}_pipeline") is not None] or [None]),
                      "H3_shuffled_any_significant": bool(any(v.get("ci_excludes_0") for v in sh.values()
                                                              if isinstance(v, dict)))}
    jdump(out, RES / "rederive.json")
    print(json.dumps(out["summary"], indent=1))


if __name__ == "__main__":
    main()
