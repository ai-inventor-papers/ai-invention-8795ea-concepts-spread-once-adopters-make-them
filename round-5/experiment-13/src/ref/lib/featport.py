"""Ports (no logic change) of the EXP5 concept-level indicators (features.concept_level: E, F, G families) and the
EXP8 build_features.stage_basic families (FR, F, E, S), written for an arbitrary frame table so the frozen EXP8
learned models can be applied to the cohort. Inputs are read-only files of EXP5 / EXP8 / art_33."""
from __future__ import annotations

import json
import math

import numpy as np
import pandas as pd

from common import EXP5, EXP8, RUN_ROOT

ART33 = RUN_ROOT / "round-1/experiment-4/src"
Y0 = 1995


def yi(y: int) -> int:
    return y - Y0


def shannon(v) -> float:
    v = np.asarray([x for x in v if x > 0], float)
    if v.sum() == 0:
        return math.nan
    p = v / v.sum()
    return float(-(p * np.log(p)).sum())


class BB:
    """EXP5 features.BB (frozen field backbone)."""
    def __init__(self):
        b = json.loads((EXP5 / "results/backbones.json").read_text())
        self.phi = np.array(b["phi_frozen"])
        self.phimin = np.array(json.loads((ART33 / "field_backbone.json").read_text())["phi_min"])
        self.gate = np.array(b["gateway_frozen"])
        self.var = {"gateway_deg": np.array(b["gateway_deg"]), "gateway_btw": np.array(b["gateway_btw"]),
                    "gateway_phimin": np.array(b["gateway_phimin"])}
        self.domain = b["domain"]


def kleinberg_batched(r, d, s: float = 2.0, gamma: float = 1.0) -> float:
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
        D = 1 - bb.phimin
        np.fill_diagonal(D, 0)
        out["RS"] = float(p @ D @ p)
    else:
        out["RS"] = math.nan
    return out


def exp5_concept_level(fr: pd.DataFrame, N: np.ndarray, V: np.ndarray, G: np.ndarray) -> pd.DataFrame:
    """EXP5 features.concept_level (E/F/G reference indicators); N, V indexed by frame row f; G base totals."""
    bb = BB()
    rows = []
    for f, r in enumerate(fr.itertuples()):
        t0 = int(r.t0)
        home_idx = [int(float(h)) - 11 for h in str(r.home).split(";") if h and h != "nan"]
        lab3 = V[f, yi(t0):yi(t0 + 2) + 1, 1:27].sum(0)
        labA = V[f, yi(t0):yi(t0 + 1) + 1, 1:27].sum(0)
        gf = g_family(lab3, home_idx, bb)
        gA = g_family(labA, home_idx, bb)
        ys = list(range(t0, t0 + 3))
        n = np.array([N[f, yi(y)] for y in ys])
        yrs = list(range(t0 - 3, t0 + 3))
        rows.append({"ci": int(r.ci), "G": gf["G"], "G_A": gA["G"], "G_btw": gf["G_btw"], "G_deg": gf["G_deg"],
                     "G_phimin": gf["G_phimin"], "REL_home": gf["REL_home"], "RS": gf["RS"],
                     "share": n.sum() / sum(G[yi(y)] for y in ys) * 1e6,
                     "growth_ind": math.log((N[f, yi(t0 + 2)] + 1) / (N[f, yi(t0 + 1)] + 1)),
                     "accel": float(np.polyfit(np.arange(3.0), np.log1p(n), 2)[0]),
                     "burst": kleinberg_batched([N[f, yi(y)] for y in yrs], [G[yi(y)] for y in yrs]),
                     "log_offhome_volume": math.log1p(sum(lab3[k] for k in range(26) if k not in home_idx))})
    return pd.DataFrame(rows)


def states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:
    x = g[:, 1:]
    cum = np.cumsum(x, 0)
    entered = cum >= min_n
    w3 = x.copy()
    w3[1:] += x[:-1]; w3[2:] += x[:-2]
    ent_lag2 = np.zeros_like(entered); ent_lag2[2:] = entered[:-2]
    offhome = np.ones(26, bool)
    for h in home:
        offhome[h - 11] = False
    retaining = ent_lag2 & (w3 >= min_n) & offhome[None, :]
    lost = entered & (w3 == 0)
    return {"entered": entered, "retaining": retaining, "lost": lost, "w3": w3, "cum": cum, "offhome": offhome}


def rca_entered(g: np.ndarray, GF: np.ndarray) -> np.ndarray:
    x = np.cumsum(g[:, 1:], 0)
    tot = x.sum(1, keepdims=True)
    F = np.cumsum(GF, 0)
    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)
    share_c = x / np.maximum(tot, 1)
    ok = (x >= 2) & (share_c > share_all)
    return np.maximum.accumulate(ok.astype(int), 0).astype(bool)


def social(e: pd.DataFrame, home_codes: set[int]) -> dict:
    off = e[(e.vfield > 0) & (~e.vfield.isin(home_codes))]
    n_off = len(off)
    if n_off == 0:
        return {"S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan}
    au = [a for a in off.authors if len(a)]
    cov = len(au) / n_off
    if cov < 0.5 or len(au) < 2:
        return {"S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan}
    parent: dict = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for a in au:
        for x in a:
            parent.setdefault(x, x)
        r0 = find(a[0])
        for x in a[1:]:
            rx = find(x)
            if rx != r0:
                parent[rx] = r0
    roots = {find(x) for x in parent}
    comp_papers = {}
    for a in au:
        rr = find(a[0])
        comp_papers[rr] = comp_papers.get(rr, 0) + 1
    iso = sum(1 for v in comp_papers.values() if v == 1)
    return {"S_comp": len(roots) / len(au), "S_comp_n": len(roots) / len(parent), "S_isolated_share": iso / len(au)}


def exp8_basic(fr: pd.DataFrame, V: np.ndarray, GF: np.ndarray, early: pd.DataFrame) -> pd.DataFrame:
    """EXP8 build_features.stage_basic families FR / F / E / S (early = grounded rows with year, vfield, authors)."""
    bb = json.loads((EXP8 / "inputs/field_backbone.json").read_text())
    phi = np.asarray(bb["phi"], float)
    phin = phi / phi.max()
    D = 1 - phin
    np.fill_diagonal(D, 0)
    colsum = phi.sum(0)
    groups = dict(tuple(early.groupby("ci")))
    rows = []
    for f, r in enumerate(fr.itertuples()):
        home = [int(float(x)) for x in str(r.home).split(";") if x and x != "nan"]
        hcodes = {h - 10 for h in home}
        t0 = int(r.t0)
        g = V[f].copy()
        gw = np.zeros_like(g)
        gw[yi(t0):yi(t0 + 2) + 1] = g[yi(t0):yi(t0 + 2) + 1]
        S = states(gw, home)
        ent_end = S["entered"][yi(t0 + 2)] & S["offhome"]
        ent_start = S["entered"][yi(t0)] & S["offhome"]
        x = g[yi(t0):yi(t0 + 2) + 1, 1:]
        off = S["offhome"]
        retained = ((x >= 2).sum(0) >= 2) & off
        rr = int(retained.sum())
        rec = {"ci": int(r.ci)}
        cand = ~ent_end & off
        rec["FRONTIER_POTENTIAL"] = float(phi[np.ix_(retained, cand)].mean(0).sum()) if rr else 0.0
        rec["fields_gained_per_yr"] = (int(ent_end.sum()) - int(ent_start.sum())) / 2.0
        S_full = states(g, home)
        E_full = S_full["entered"][yi(t0 + 2)]
        rca = rca_entered(g, GF)[yi(t0 + 2)] & off
        rec["D_rca_end"] = int(rca.sum())
        rec["D_vol_end"] = int((E_full & off).sum())
        cand_f = ~E_full & off
        dens = phi[E_full].sum(0) / np.where(colsum > 0, colsum, 1)
        rec["M0_density_end"] = float(dens[cand_f].mean()) if cand_f.any() else np.nan
        lab = x.sum(0)
        tot = lab.sum()
        rec["rao_stirling"] = float((lab / tot) @ D @ (lab / tot)) if tot > 0 else np.nan
        e = groups.get(r.ci)
        if e is not None and len(e):
            e = e[(e.year >= t0) & (e.year <= t0 + 2)]
            a0 = {a for lst in e[e.year == t0].authors for a in lst}
            a2 = {a for lst in e[e.year == t0 + 2].authors for a in lst}
            rec["author_growth"] = math.log1p(len(a2)) - math.log1p(len(a0))
            rec.update(social(e, hcodes))
        else:
            rec.update({"author_growth": np.nan, "S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan})
        rows.append(rec)
    return pd.DataFrame(rows)
