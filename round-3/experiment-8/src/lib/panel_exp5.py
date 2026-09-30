"""Dense per-concept count arrays from scan/agg_counts.parquet (built once, cached compressed in scan/arrays_<variant>.npz).

Variants: 'grounded' = frozen grounding rule (TAG, plus untagged rows weighted by the sense-filter pass rate
of their (concept, mtype)); 'match' = every verified title match (the ungrounded sensitivity).
Arrays (float32): N[ci, y] all venues; V[ci, y, 27] by venue-field code (0 = unlabelled);
P[ci, y, 27] by primary-topic field code; plus T1[ci, y] (tagstate==1) and M[ci, y] (all matches)."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

from common import NY, ROOT, SCAN, Y0, Y1

YEARS = list(range(Y0, Y1 + 1))


def yi(y: int) -> int:
    return y - Y0


def grounding_rule() -> str:
    p = ROOT / "grounding_report.json"
    return json.loads(p.read_text())["frozen_grounding_rule"] if p.exists() else "c_TAG"


def build_arrays(variant: str, n_concepts: int) -> dict[str, np.ndarray]:
    cache = SCAN / f"arrays_{variant}.npz"
    if cache.exists():
        z = np.load(cache)
        return {k: z[k] for k in z.files}
    ag = pd.read_parquet(SCAN / "agg_counts.parquet")
    if variant == "grounded":
        rule = grounding_rule()
        if rule == "b_exact_name_only":
            w = (ag.mt == 0).astype(np.float32).to_numpy()
        else:
            w = (ag.tagstate == 1).astype(np.float32).to_numpy()
            pr_p = SCAN / "untagged_passrate.parquet"
            ts3 = (ag.tagstate == 3).to_numpy()
            if rule == "e_TAG_or_untagged_filter" and ts3.any():
                pr = pd.read_parquet(pr_p) if pr_p.exists() else pd.DataFrame(columns=["ci", "mt", "passrate"])
                glob = float(pr.passrate.mean()) if len(pr) else 0.0
                m = ag[ts3][["ci", "mt"]].merge(pr[["ci", "mt", "passrate"]], on=["ci", "mt"], how="left")
                w[ts3] = m.passrate.fillna(glob).to_numpy(np.float32)
    else:
        w = np.ones(len(ag), np.float32)
    n = ag.n.to_numpy(np.float32) * w
    ci = ag.ci.to_numpy(np.int64)
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    ci, y, n, vf, pt = ci[ok], y[ok], n[ok], ag.vfield.to_numpy(np.int64)[ok], ag.ptfield.to_numpy(np.int64)[ok]
    ts1 = (ag.tagstate.to_numpy()[ok] == 1)
    raw = ag.n.to_numpy(np.float32)[ok]
    C = n_concepts
    N = np.bincount(ci * NY + y, weights=n, minlength=C * NY).reshape(C, NY).astype(np.float32)
    V = np.bincount((ci * NY + y) * 27 + vf, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    P = np.bincount((ci * NY + y) * 27 + pt, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    T1 = np.bincount(ci * NY + y, weights=raw * ts1, minlength=C * NY).reshape(C, NY).astype(np.float32)
    M = np.bincount(ci * NY + y, weights=raw, minlength=C * NY).reshape(C, NY).astype(np.float32)
    out = {"N": N, "V": V, "P": P, "T1": T1, "M": M}
    np.savez_compressed(cache, **out)  # mostly zeros: compressed stays well under 100 MB
    return out


def onset(yc: np.ndarray) -> tuple[float, bool | None]:
    """art_33 s0_ground.onset: t0 = first year 2000..2014 with >= 20 works; newborn = each of t0-3..t0-1 <
    0.25 * n(t0+2). yc indexed by year - Y0."""
    ts = [y for y in range(2000, 2015) if yc[yi(y)] >= 20]
    if not ts:
        return math.nan, None
    t0 = ts[0]
    newborn = all(yc[yi(t0 - k)] < 0.25 * yc[yi(t0 + 2)] for k in (1, 2, 3))
    return float(t0), bool(newborn)


def onset_table(N: np.ndarray, min_early: float = 30.0) -> pd.DataFrame:
    rows = []
    # fast prefilter: some year 2003..2014 >= 20 and every year 2000..2002 < 20
    cand = np.nonzero((N[:, yi(2003):yi(2014) + 1] >= 20).any(1) & (N[:, yi(2000):yi(2002) + 1] < 20).all(1))[0]
    for ci in cand:
        t0, nb = onset(N[ci])
        if not np.isfinite(t0) or not (2003 <= t0 <= 2014):
            continue
        t0 = int(t0)
        early = float(N[ci, yi(t0):yi(t0 + 2) + 1].sum())
        if early < min_early:
            continue
        rows.append({"ci": int(ci), "t0": t0, "newborn": nb, "early_volume": early})
    return pd.DataFrame(rows, columns=["ci", "t0", "newborn", "early_volume"])
