#!/usr/bin/env python3
"""S2-composites + S1b seal + V4 split-half reliability (no outcome is read here).

1. merge S2 scalars and V3 nulls; fit the clean-variant z constants on ALL EXP5-frame concepts (n_home_early >= 10,
   variant finite; winsor 0.5/99.5, mean/sd == ladder.fit_open_constants) -> results/frozen_constants_S1b.json,
   sealed (entry S1b_constants) BEFORE any outcome join
2. composites NOVCHURN_* / OPEN_home_clean / OPEN_home_exc -> data/clean_variants.parquet (no outcome columns)
3. V4 split-half reliability of every raw and clean variant -> results/reliability.json (X side; the outcome side is
   added by s4b_outcome_rel.py)"""
from __future__ import annotations

import json
import math
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import DATA, DATA_IN, RES, jdump, setup_logger
from seal import seal_file

logger = setup_logger("s4_composites")
OUT6 = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
NBINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]
# clean columns needing new constants: column -> sign
NEW_CONST = {**{f"NOV_res_rare{n}": 1 for n in (5, 10, 20)}, **{f"edge_persistence_rare{n}": -1 for n in (5, 10, 20)},
             "NOV_res_exc": 1, "edge_persistence_exc": -1, "NOV_res_zperm": 1, "edge_persistence_zperm": -1,
             "z_pers_cfg": -1, "EP_chao": -1, "z_dens_cfg": -1, "ego_density_W3_exc": -1, "z_dens_k": -1,
             "excess_pers_cfg": -1, "z_pers_k": -1}


def fit_const(v: np.ndarray, sign: int) -> dict:
    v = v[np.isfinite(v)]
    lo, hi = np.percentile(v, [0.5, 99.5])
    w = np.clip(v, lo, hi)
    return {"lo": float(lo), "hi": float(hi), "mu": float(w.mean()), "sd": float(w.std()) or 1.0, "sign": sign,
            "n": int(len(v))}


def zs(v, c: dict) -> np.ndarray:
    return c["sign"] * (np.clip(np.asarray(v, float), c["lo"], c["hi"]) - c["mu"]) / c["sd"]


def mean_req(*zz, min_fin: int | None = None) -> np.ndarray:
    Z = np.column_stack(zz)
    nf = np.isfinite(Z).sum(1)
    with np.errstate(invalid="ignore"):
        m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)
    m[nf < (Z.shape[1] if min_fin is None else min_fin)] = np.nan
    return m


def composites(d: pd.DataFrame, K10: dict, KN: dict, suffix_map: dict | None = None) -> pd.DataFrame:
    """d holds raw columns '<m>__raw' and clean columns; returns composite columns."""
    o = pd.DataFrame(index=d.index)
    zN = zs(d["NOV_res__raw"], K10["NOV_res"])
    o["NOVCHURN_raw"] = mean_req(zN, zs(d["edge_persistence__raw"], K10["edge_persistence"]))
    for n in (5, 10, 20):
        if f"NOV_res_rare{n}" in d:
            o[f"NOVCHURN_rare{n}"] = mean_req(zs(d[f"NOV_res_rare{n}"], KN[f"NOV_res_rare{n}"]),
                                              zs(d[f"edge_persistence_rare{n}"], KN[f"edge_persistence_rare{n}"]))
    if "NOV_res_exc" in d:
        o["NOVCHURN_exc"] = mean_req(zs(d["NOV_res_exc"], KN["NOV_res_exc"]),
                                     zs(d["edge_persistence_exc"], KN["edge_persistence_exc"]))
        o["NOVCHURN_zperm"] = mean_req(zs(d["NOV_res_zperm"], KN["NOV_res_zperm"]),
                                       zs(d["edge_persistence_zperm"], KN["edge_persistence_zperm"]))
    if "z_pers_cfg" in d:
        o["NOVCHURN_cfg"] = mean_req(zN, zs(d["z_pers_cfg"], KN["z_pers_cfg"]))
    if "EP_chao" in d:
        o["NOVCHURN_chao"] = mean_req(zN, zs(d["EP_chao"], KN["EP_chao"]))
    raw6 = {m: zs(d[f"{m}__raw"], K10[m]) for m in OUT6}
    o["OPEN_home"] = mean_req(*raw6.values(), min_fin=4)
    if "z_dens_cfg" in d and "z_pers_cfg" in d:
        cl = dict(raw6)
        cl["ego_density_W3"] = zs(d["z_dens_cfg"], KN["z_dens_cfg"])
        cl["edge_persistence"] = zs(d["z_pers_cfg"], KN["z_pers_cfg"])
        o["OPEN_home_clean"] = mean_req(*cl.values(), min_fin=4)
    if "ego_density_W3_exc" in d:
        ce = dict(raw6)
        ce["ego_density_W3"] = zs(d["ego_density_W3_exc"], KN["ego_density_W3_exc"])
        ce["edge_persistence"] = zs(d["edge_persistence_exc"], KN["edge_persistence_exc"])
        o["OPEN_home_exc"] = mean_req(*ce.values(), min_fin=4)
    return o


# ----------------------------------------------------------------------------- reliability helpers
def spearman_cols(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Spearman per row s of A[s], B[s] (pairwise finite)."""
    out = np.full(A.shape[0], np.nan)
    for s in range(A.shape[0]):
        ok = np.isfinite(A[s]) & np.isfinite(B[s])
        if ok.sum() < 20:
            continue
        a, b = rankdata(A[s, ok]), rankdata(B[s, ok])
        if a.std() == 0 or b.std() == 0:
            continue
        out[s] = np.corrcoef(a, b)[0, 1]
    return out


def sb_of(rs: np.ndarray) -> tuple[float, float, int]:
    rs = rs[np.isfinite(rs)]
    if not len(rs):
        return math.nan, math.nan, 0
    r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))
    return r, 2 * r / (1 + r) if r > -1 else math.nan, int(len(rs))


def main() -> None:
    s2 = pd.read_parquet(DATA / "s2_scalars_full.parquet")
    v3 = pd.read_parquet(DATA / "v3_nulls_full.parquet")
    d = s2.merge(v3, on=["frame", "ci"], how="left", validate="1:1")
    logger.info(f"merged {len(d)} concepts")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    K10 = spec["exp10_open_constants_home"]
    ex5 = d.frame == "exp5"
    KN = {c: fit_const(d.loc[ex5, c].to_numpy(float), s) for c, s in NEW_CONST.items()}
    cpath = RES / "frozen_constants_S1b.json"
    jdump({"rule": spec["composites"]["z_rule_new_constants"], "fitted_on": "EXP5-frame concepts, n_home_early >= 10",
           "constants": KN, "exp10_constants_used_for_raw": K10}, cpath)
    ent = seal_file("S1b_constants", cpath)
    logger.info(f"sealed constants sha256 {ent['sha256']}")
    comp = composites(d, K10, KN)
    d = pd.concat([d, comp], axis=1)
    # metadata (no outcome columns)
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet",
                         columns=["ci", "concept_id", "name", "agroup", "group", "OPEN_home", "n_home_early"])
    fe["frame"] = "exp5"
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet",
                         columns=["ci", "concept_id", "name", "agroup", "group", "OPEN_home", "n_home_early"])
    ac["frame"] = "cohort"
    meta = pd.concat([fe, ac], ignore_index=True).rename(columns={"OPEN_home": "OPEN_home_exp10",
                                                                   "n_home_early": "n_home_early_exp10"})
    d = d.merge(meta, on=["frame", "ci"], how="left", validate="1:1")
    chk = np.nanmax(np.abs(d.OPEN_home - d.OPEN_home_exp10))
    mism = int((np.isnan(d.OPEN_home) ^ np.isnan(d.OPEN_home_exp10)).sum())
    assert (d.n_home_early == d.n_home_early_exp10).all()
    logger.info(f"OPEN_home recomputed vs EXP10: max diff {chk:.2e}, NaN mismatches {mism}")
    d["log_n_home_early"] = np.log(d.n_home_early)
    d["uid"] = np.where(d.frame == "exp5", "E", "C") + d.ci.astype(str)
    d.to_parquet(DATA / "clean_variants.parquet", index=False)
    logger.info(f"wrote data/clean_variants.parquet {d.shape}")
    # ------------------------------------------------------------------ V4 reliability
    pos = {(f, int(c)): i for i, (f, c) in enumerate(zip(d.frame, d.ci))}
    nC = len(d)
    S_RAW, S_CL = 100, 20
    H = {h: {m: np.full((S_RAW, nC), np.nan, np.float32) for m in OUT6} for h in ("A", "B")}
    HC: dict = {"A": {}, "B": {}}
    for p in sorted((DATA / "s2_parts_full").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, e in zip(z["rows"], z["extras"]):
            if not e:
                continue
            i = pos[(r["frame"], int(r["ci"]))]
            for h in ("A", "B"):
                for j, m in enumerate(OUT6):
                    H[h][m][:, i] = e["half_raw"][h][:, j]
                hc = e["half_clean"][h]
                for c in hc.columns:
                    HC[h].setdefault(c, np.full((S_CL, nC), np.nan, np.float32))[:, i] = hc[c].to_numpy()
    v3h = pickle.loads((DATA / "v3_halves_full.pkl").read_bytes())
    for c in ("z_pers_k", "z_dens_k", "z_dens_cfg"):
        for h in ("A", "B"):
            HC[h][f"{c}_v3"] = np.full((S_CL, nC), np.nan, np.float32)
    for j, (f, ci, h, sp) in enumerate(v3h["key"]):
        i = pos[(f, int(ci))]
        for c in ("z_pers_k", "z_dens_k", "z_dens_cfg"):
            HC[h][f"{c}_v3"][sp, i] = v3h[c][j]
    # variant half matrices (S x nC) for A and B
    VAR: dict = {}
    for h in ("A", "B"):
        V = {}
        for m in OUT6:
            V[f"{m}__raw"] = H[h][m].astype(float)
        raw_c = []
        for s in range(S_RAW):
            ds = pd.DataFrame({f"{m}__raw": H[h][m][s].astype(float) for m in OUT6})
            raw_c.append(composites(ds, K10, KN)[["NOVCHURN_raw", "OPEN_home"]])
        V["NOVCHURN_raw"] = np.stack([c.NOVCHURN_raw.to_numpy() for c in raw_c])
        V["OPEN_home"] = np.stack([c.OPEN_home.to_numpy() for c in raw_c])
        cl = []
        for s in range(S_CL):
            ds = pd.DataFrame({f"{m}__raw": H[h][m][s].astype(float) for m in OUT6})
            for c, arr in HC[h].items():
                ds[c] = arr[s].astype(float)
            ds["z_pers_cfg"] = ds["z_pers_k_v3"]          # declared approximation (k-matched MC on halves)
            ds["z_dens_cfg"] = ds["z_dens_cfg_v3"]
            ds["z_dens_k"] = ds["z_dens_k_v3"]
            cc = composites(ds, K10, KN)
            cl.append((ds, cc))
        for col in ["NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "new_edge_rate_exc", "NOV_res_zperm",
                    "edge_persistence_zperm", "ego_density_W3_zperm", "NOV_res_rare5", "edge_persistence_rare5",
                    "ego_density_W3_rare5", "z_pers_cfg", "z_dens_cfg", "z_dens_k", "edge_persistence_nullmean"]:
            V[col] = np.stack([ds[col].to_numpy(float) for ds, _ in cl])
        for col in ["NOVCHURN_exc", "NOVCHURN_zperm", "NOVCHURN_rare5", "NOVCHURN_cfg", "OPEN_home_clean",
                    "OPEN_home_exc"]:
            V[col] = np.stack([cc[col].to_numpy(float) for _, cc in cl])
        VAR[h] = V
    notes = {"z_pers_cfg": "halves use the k-matched Monte Carlo approximation of the curveball null (declared)",
             "NOVCHURN_cfg": "halves use z_pers_k (k-matched MC) in place of the curveball z (declared)",
             "OPEN_home_clean": "halves use z_pers_k for z_pers_cfg (declared)",
             "NOV_res_rare5": "V1 on halves at n = 5 (concepts with >= 10 papers per W-year); used as the reliability "
                              "proxy for every rarefied variant (rare10 cannot be split into halves of 10)",
             "NOVCHURN_rare5": "proxy for NOVCHURN_rare10 reliability"}
    body = d.body.to_numpy()
    nh = d.n_home_early.to_numpy()
    rel: dict = {"method": "r_s = Spearman(v_A, v_B) across concepts per split; r = tanh(mean atanh r_s); "
                           "SB = 2r/(1+r); 100 splits raw, 20 clean", "notes": notes, "variants": {}}
    rng = np.random.default_rng(20260936)
    boot_idx = [rng.integers(0, nC, nC) for _ in range(200)]
    for v in VAR["A"]:
        A, B = VAR["A"][v], VAR["B"][v]
        ent: dict = {}
        r, sb, ns = sb_of(spearman_cols(A, B))
        ent["pooled"] = {"r_half": r, "SB": sb, "n_splits": ns,
                         "n_concepts_mean": float(np.mean((np.isfinite(A) & np.isfinite(B)).sum(1)))}
        for bd in ("DEV", "OLDHO", "COH1014", "COH1517"):
            m = body == bd
            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))
            ent[bd] = {"r_half": r, "SB": sb, "n_splits": ns,
                       "n_concepts_mean": float(np.mean((np.isfinite(A[:, m]) & np.isfinite(B[:, m])).sum(1)))}
        for lo, hi in NBINS:
            m = (nh >= lo) & (nh <= hi)
            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))
            ent[f"n{lo}-{hi if hi < 10**9 else 'inf'}"] = {"r_half": r, "SB": sb, "n_splits": ns,
                                                           "n_concepts": int(m.sum())}
        # concept bootstrap of pooled SB (first 10 splits for speed)
        Ab, Bb = A[:10], B[:10]
        bs = []
        for idx in boot_idx:
            bs.append(sb_of(spearman_cols(Ab[:, idx], Bb[:, idx]))[1])
        bs = np.asarray(bs, float)
        bs = bs[np.isfinite(bs)]
        ent["pooled"]["SB_ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) else None
        ent["pooled"]["SB_boot_sd"] = float(bs.std()) if len(bs) else None
        rel["variants"][v] = ent
        logger.info(f"rel {v}: pooled SB {ent['pooled']['SB']:.3f}; COH1517 {ent['COH1517']['SB']:.3f}")
    jdump(rel, RES / "reliability_x.json")
    # keep per-concept split-averaged half values for power / rederive
    np.savez_compressed(DATA / "v4_half_means.npz",
                        **{f"{h}__{v}": np.nanmean(VAR[h][v], 0) for h in ("A", "B") for v in VAR[h]})


if __name__ == "__main__":
    main()
