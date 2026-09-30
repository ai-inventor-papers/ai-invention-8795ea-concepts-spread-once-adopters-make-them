#!/usr/bin/env python3
"""STEP 7: episode covariates and concept-level indicators (no outcome is read here).

Episode covariates: B5_c (log early volume, growth, early off-home share, early venue entropy, early reach), frozen
log field size, phi_home_j, relatedness density_j (art_33 formula), coverage (label coverage, precision_c, tag
coverage), the episode's own early size (log1p n_early, share_early, growth_j), frozen gateway_j and variants
(deg, btw, phimin, recomputed S0) and the time-varying gateway_j,s. P_j(-c) needs outcomes and is added in
models.py. Concept-level: G, G_A, G_btw, REL_home (art_33 g_family), plus the reference indicators of art_33
(count_indicators, label_indicators, RS, DOM_*) -> concept_features_basic.csv.

`build_features(arr_key, variant)` is reused by the sensitivities (primary-topic fields; ungrounded matches;
B5 over t0..t0+4)."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

from common import FIELD_IDS, RES, ROOT, SCAN, Y0, jdump, setup_logger
from frame import episode_rows, home_rule, n_concepts, shannon, year_totals
from panel import build_arrays, yi

logger = setup_logger("features")


class BB:
    def __init__(self):
        b = json.loads((RES / "backbones.json").read_text())
        self.phi = np.array(b["phi_frozen"])
        from common import ART33
        self.phimin = np.array(json.loads((ART33 / "field_backbone.json").read_text())["phi_min"])
        self.gate = np.array(b["gateway_frozen"])
        self.var = {"gateway_deg": np.array(b["gateway_deg"]), "gateway_btw": np.array(b["gateway_btw"]),
                    "gateway_phimin": np.array(b["gateway_phimin"]),
                    "gateway_S0rec": np.array(b["recomputed"]["S0"]["eig"])}
        self.slice_eig = {k: np.array(v["eig"]) for k, v in b["recomputed"].items()}
        self.logsize = np.log(np.array(b["n_field_frozen"]))
        self.logsize_s = {k: np.array(v) for k, v in b["log_field_size_slice"].items()}
        self.domain = b["domain"]
        self.top_tercile = set(np.argsort(self.gate)[::-1][:9])  # 26 fields -> top 9 = top tercile


def slice_for_t0(t0: int) -> str:
    return "S0" if t0 <= 2007 else ("S1" if t0 <= 2012 else "S2")


def kleinberg_batched(r, d, s: float = 2.0, gamma: float = 1.0) -> float:
    """art_33 kleinberg_batched (2-state batched burst) -> burst weight."""
    r = np.asarray(r, float)
    d = np.asarray(d, float)
    n = len(r)
    p0 = r.sum() / d.sum()
    if p0 <= 0:
        return 0.0
    p1 = min(s * p0, 0.9999)

    def cost(p):
        return -(r * math.log(p) + (d - r) * math.log(1 - p))
    c = np.vstack([cost(p0), cost(p1)])
    trans = gamma * math.log(n)
    V = np.zeros((2, n))
    back = np.zeros((2, n), int)
    V[0, 0], V[1, 0] = c[0, 0], c[1, 0] + trans
    for t in range(1, n):
        for q in (0, 1):
            cand = [V[0, t - 1] + (trans if q == 1 else 0), V[1, t - 1]]
            back[q, t] = int(np.argmin(cand))
            V[q, t] = min(cand) + c[q, t]
    st = [int(np.argmin(V[:, -1]))]
    for t in range(n - 1, 0, -1):
        st.append(back[st[-1], t])
    st = st[::-1]
    return float(sum(c[0, t] - c[1, t] for t in range(n) if st[t] == 1))


def g_family(fc: np.ndarray, home_idx: list[int], bb: BB) -> dict:
    """art_33 g_family on a 26-vector of labelled counts."""
    tot = fc.sum()
    off = np.array([fc[k] if k not in home_idx else 0.0 for k in range(26)])
    offt = off.sum()
    out = {}
    for nm, vec in (("G", bb.gate), ("G_deg", bb.var["gateway_deg"]), ("G_btw", bb.var["gateway_btw"]),
                    ("G_phimin", bb.var["gateway_phimin"])):
        out[nm] = float((off * vec).sum() / offt) if offt > 0 else math.nan
    out["REL_home"] = (float(sum(off[k] * np.mean([bb.phi[h, k] for h in home_idx]) for k in range(26)) / offt)
                       if offt > 0 and home_idx else math.nan)
    if tot > 0:
        p = fc / tot
        D = 1 - bb.phimin  # art_33 RS: Rao-Stirling with 1 - phi_min distances
        np.fill_diagonal(D, 0)
        out["RS"] = float(p @ D @ p)
        for dom in ("Physical", "Life", "Health", "Social"):
            out[f"DOM_{dom}"] = float(sum(p[k] for k in range(26) if bb.domain[k] == dom))
    else:
        out["RS"] = math.nan
        for dom in ("Physical", "Life", "Health", "Social"):
            out[f"DOM_{dom}"] = math.nan
    return out


def b5(N: np.ndarray, V: np.ndarray, t0: int, home_idx: list[int], end_off: int = 2) -> dict:
    ys = slice(yi(t0), yi(t0 + end_off) + 1)
    lab = V[ys, 1:27].sum(0)
    labt = lab.sum()
    vol = N[ys].sum()
    return {"logvol": math.log1p(vol), "growth_c": math.log((N[yi(t0 + end_off)] + 1) / (N[yi(t0)] + 1)),
            "offhome_share": float(sum(lab[k] for k in range(26) if k not in home_idx) / labt) if labt else math.nan,
            "entropy": shannon(lab), "reach": int((lab >= 2 - 1e-9).sum())}


def build_features(fc: pd.DataFrame, ep: pd.DataFrame, A: dict, arr: str = "V", b5_end: int = 2) -> pd.DataFrame:
    """Episode covariates for episodes `ep` of frame concepts `fc` using count array A[arr] (V venue / P ptopic)."""
    bb = BB()
    N, X = A["N"], A[arr]
    crow = {}
    for r in fc.itertuples():
        home_idx = [int(h) - 11 for h in str(r.home).split(";") if h]
        lab = X[r.ci, yi(r.t0):yi(r.t0 + 2) + 1, 1:27].sum(0)
        K = {k for k in range(26) if lab[k] >= 2 - 1e-9}
        crow[r.ci] = {"home_idx": home_idx, "K": K, **b5(N[r.ci], X[r.ci], r.t0, home_idx, b5_end)}
    rows = []
    for r in ep.itertuples():
        c = crow[r.ci]
        k = r.field - 11
        Kj = c["K"] - {k}
        den = bb.phi[:, k].sum()
        dens = bb.phi[list(Kj), k].sum() / den if Kj and den > 0 else 0.0
        s = slice_for_t0(r.t0)
        rows.append({"logvol": c["logvol"], "growth_c": c["growth_c"], "offhome_share": c["offhome_share"],
                     "entropy": c["entropy"], "reach": c["reach"], "log_field_size": bb.logsize[k],
                     "log_field_size_s": bb.logsize_s[s][k],
                     "phi_home": float(np.mean([bb.phi[h, k] for h in c["home_idx"]])) if c["home_idx"] else 0.0,
                     "density": float(dens), "log_n_early": math.log1p(r.n_early),
                     "gateway_j": float(bb.gate[k]), "gateway_js": float(bb.slice_eig[s][k]),
                     **{nm: float(v[k]) for nm, v in bb.var.items()},
                     "top_tercile_home": int(any(h in bb.top_tercile for h in c["home_idx"]))})
    F = pd.DataFrame(rows, index=ep.index)
    return pd.concat([ep, F], axis=1)


def concept_level(fc: pd.DataFrame, A: dict) -> pd.DataFrame:
    """H3 variants + art_33 reference indicators (no outcome)."""
    bb = BB()
    N, V = A["N"], A["V"]
    G, _ = year_totals()
    rows = []
    for r in fc.itertuples():
        home_idx = [int(h) - 11 for h in str(r.home).split(";") if h]
        lab3 = V[r.ci, yi(r.t0):yi(r.t0 + 2) + 1, 1:27].sum(0)
        labA = V[r.ci, yi(r.t0):yi(r.t0 + 1) + 1, 1:27].sum(0)
        gf = g_family(lab3, home_idx, bb)
        gA = g_family(labA, home_idx, bb)
        ys = list(range(r.t0, r.t0 + 3))
        n = np.array([N[r.ci, yi(y)] for y in ys])
        yrs = list(range(r.t0 - 3, r.t0 + 3))
        ci = {"log_count": math.log1p(n.sum()), "share": n.sum() / sum(G[yi(y)] for y in ys) * 1e6,
              "growth_ind": math.log((N[r.ci, yi(r.t0 + 2)] + 1) / (N[r.ci, yi(r.t0 + 1)] + 1)),
              "accel": float(np.polyfit(np.arange(3.0), np.log1p(n), 2)[0]),
              "burst": kleinberg_batched([N[r.ci, yi(y)] for y in yrs], [G[yi(y)] for y in yrs])}
        labt = lab3.sum()
        li = {"lab_entropy": shannon(lab3), "lab_reach": int((lab3 >= 2 - 1e-9).sum()),
              "lab_offhome_share": float(sum(lab3[k] for k in range(26) if k not in home_idx) / labt) if labt else math.nan,
              "log_offhome_volume": math.log1p(sum(lab3[k] for k in range(26) if k not in home_idx))}
        rows.append({"ci": r.ci, "concept_id": r.concept_id, "G": gf["G"], "G_A": gA["G"], "G_btw": gf["G_btw"],
                     "G_deg": gf["G_deg"], "G_phimin": gf["G_phimin"], "REL_home": gf["REL_home"], "RS": gf["RS"],
                     **{k: gf[k] for k in gf if k.startswith("DOM_")}, **ci, **li,
                     **b5(N[r.ci], V[r.ci], r.t0, home_idx)})
    return pd.DataFrame(rows)


def main() -> None:
    fc = pd.read_csv(ROOT / "frame_concepts.csv")
    ep = pd.read_csv(ROOT / "episodes.csv")
    A = build_arrays("grounded", n_concepts())
    F = build_features(fc, ep, A, "V")
    F = F.merge(fc[["ci", "label_coverage_early", "precision_c", "tag_coverage", "newborn", "intersect40",
                    "weak_home"]], on="ci", how="left")
    F.to_csv(ROOT / "episode_features.csv", index=False)
    cl = concept_level(fc, A)
    cl.to_csv(ROOT / "concept_features_basic.csv", index=False)
    logger.info(f"features: {len(F)} episodes, {len(cl)} concepts")


if __name__ == "__main__":
    main()
