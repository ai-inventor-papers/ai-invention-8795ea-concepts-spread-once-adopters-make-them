#!/usr/bin/env python3
"""S2-V3 configuration nulls (reads the S2 chunk pickles; never reads outcomes).

V3a  z_dens_cfg: each slice's full topic backbone rewired V3_REWIRES times (igraph rewire, n = 10 m trials, simple;
     degree sequence asserted); edges of each rewired graph inside the raw NB_W3 (slice t0+2) and NB_W1 (slice t0);
     half NB_W3 sets (V4) use the first V3_HALF_DRAWS rewires.
V3b  z_dens_k: V3_KSETS random sets of size |NB_W3| ~ bg counts in year t0+2 (bg > 0, SELF excluded), edges in the
     REAL backbone; halves with V3_HALF_DRAWS draws.
V3c  z_pers_cfg: curveball chain of the (concept-window x topic) incidence per calendar year (all bodies), 200
     samples; plus the k-matched Monte Carlo approximation z_pers_k on the full build (to validate it) and on halves.
Writes data/v3_nulls.parquet (per concept) and data/v3_halves.pkl (per concept x split x half)."""
from __future__ import annotations

import argparse
import math
import multiprocessing as mp
import pickle
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, INPUTS, RES, jdump, setup_logger
from s2_cfg import CFG_FULL

NT = 4516
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]


def slice_of(y: int) -> int:
    for i, (a, b) in enumerate(SLICES):
        if a <= y <= b:
            return i
    return 0 if y < SLICES[0][0] else len(SLICES) - 1


def load_s2(tag: str) -> tuple[pd.DataFrame, list]:
    rows, extras = [], []
    for p in sorted((DATA / f"s2_parts_{tag}").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, e in zip(z["rows"], z["extras"]):
            if not e:
                continue
            rows.append(r)
            extras.append({"NB": e["NB"], "SELF": e["SELF"], "half_NB": e["half_NB"],
                           "half_ep": {h: e["half_raw"][h][:, 5] for h in ("A", "B")}})
    return pd.DataFrame(rows), extras


def pairs_of(sets: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pa, pb, sid = [], [], []
    for i, s in enumerate(sets):
        k = len(s)
        if k < 2:
            continue
        iu, ju = np.triu_indices(k, 1)
        pa.append(s[iu])
        pb.append(s[ju])
        sid.append(np.full(len(iu), i, np.int32))
    if not pa:
        return np.zeros(0, np.int32), np.zeros(0, np.int32), np.zeros(0, np.int32)
    return np.concatenate(pa).astype(np.int32), np.concatenate(pb).astype(np.int32), np.concatenate(sid)


def rewire_worker(s: int, groups: dict, n_draws: int, n_half: int) -> dict:
    """groups: name -> (pa, pb, sid, nsets, draws). Returns name -> (obs, sum, sumsq, nd)."""
    import igraph as ig
    z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
    a, b = z["a"].astype(np.int64), z["b"].astype(np.int64)
    G0 = ig.Graph(n=NT, edges=np.c_[a, b].tolist())
    deg0 = np.array(G0.degree())
    adj = np.zeros((NT, NT), bool)
    out = {}

    def count(adj_, g):
        pa, pb, sid, ns, _ = g
        return np.bincount(sid, weights=adj_[pa, pb], minlength=ns)
    adj[a, b] = True
    adj[b, a] = True
    for nm, g in groups.items():
        out[nm] = [count(adj, g), np.zeros(g[3]), np.zeros(g[3]), 0]
    t = time.time()
    for d in range(1, n_draws + 1):
        random.seed(20260930 + 1000 * s + d)
        ig.set_random_number_generator(random)
        G = G0.copy()
        G.rewire(n=10 * G.ecount(), allowed_edge_types="simple")
        if not np.array_equal(np.array(G.degree()), deg0):
            raise RuntimeError("degree sequence changed by rewire")
        el = np.array(G.get_edgelist(), np.int64)
        adj[:] = False
        adj[el[:, 0], el[:, 1]] = True
        adj[el[:, 1], el[:, 0]] = True
        for nm, g in groups.items():
            if d > g[4]:
                continue
            e = count(adj, g)
            out[nm][1] += e
            out[nm][2] += e * e
            out[nm][3] += 1
        if d % 20 == 0:
            print(f"slice {s}: {d}/{n_draws} rewires, {time.time()-t:.0f}s", flush=True)
    if s == 0:  # U4 evidence: simple graph after one rewire
        out["_u4"] = {"is_simple": bool(G.is_simple()), "degree_equal": True}
    return out


def v3a(df: pd.DataFrame, ex: list, cfg: dict, logger) -> tuple[pd.DataFrame, dict]:
    n_draws, n_half = cfg["V3_REWIRES"], cfg["V3_HALF_DRAWS"]
    t0 = df.t0.to_numpy()
    S = cfg["S_CLEAN"]
    jobs = {}
    index = {}
    for s in range(3):
        g = {}
        i3 = [i for i in range(len(df)) if slice_of(int(t0[i]) + 2) == s]
        i1 = [i for i in range(len(df)) if slice_of(int(t0[i])) == s]
        sets3 = [ex[i]["NB"][3] for i in i3]
        sets1 = [ex[i]["NB"][1] for i in i1]
        g["W3"] = (*pairs_of(sets3), len(sets3), n_draws)
        g["W1"] = (*pairs_of(sets1), len(sets1), n_draws)
        hs, hidx = [], []
        for i in i3:
            for h in ("A", "B"):
                for sp in range(S):
                    hs.append(ex[i]["half_NB"][h][sp][2])
                    hidx.append((i, h, sp))
        g["H3"] = (*pairs_of(hs), len(hs), n_half)
        jobs[s] = g
        index[s] = {"W3": i3, "W1": i1, "H3": hidx}
        logger.info(f"V3a slice {s}: W3 sets {len(sets3)} ({len(g['W3'][0])} pairs), W1 {len(sets1)}, "
                    f"halves {len(hs)} ({len(g['H3'][0])} pairs)")
    return jobs, index


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="full")
    ap.add_argument("--draws-scale", type=float, default=1.0)
    a = ap.parse_args()
    logger = setup_logger(f"s3_nulls_{a.tag}")
    cfg = dict(CFG_FULL)
    for k in ("V3_REWIRES", "V3_KSETS", "V3_CURVEBALL_SAMPLES", "V3_HALF_DRAWS"):
        cfg[k] = max(10, int(round(cfg[k] * a.draws_scale)))
    df, ex = load_s2(a.tag)
    import json
    cfg["S_CLEAN"] = json.loads((DATA / f"s2_parts_{a.tag}" / "cfg.json").read_text())["S_CLEAN"]
    logger.info(f"loaded {len(df)} concepts from S2 ({a.tag}); cfg {cfg}")
    S = cfg["S_CLEAN"]
    nC = len(df)
    t0s = df.t0.to_numpy().astype(int)
    # ---------------------------------------------------------------- V3a (3 slice workers, background)
    jobs, index = v3a(df, ex, cfg, logger)
    pool = ProcessPoolExecutor(3, mp_context=mp.get_context("spawn"))
    futs = {s: pool.submit(rewire_worker, s, jobs[s], cfg["V3_REWIRES"], cfg["V3_HALF_DRAWS"]) for s in range(3)}
    # ---------------------------------------------------------------- V3c curveball + k-matched (this process)
    from nullkern import curveball_run, kpers_null, ksets_null
    self_flat = np.concatenate([e["SELF"] for e in ex]).astype(np.int64)
    self_off = np.r_[0, np.cumsum([len(e["SELF"]) for e in ex])].astype(np.int64)
    years = list(range(int(t0s.min()), int(t0s.max()) + 3))
    yi = {y: i for i, y in enumerate(years)}
    rows_by_year = {y: [] for y in years}
    for c in range(nC):
        for w in (1, 2, 3):
            rows_by_year[t0s[c] + w - 1].append((c, w))
    data, off, ylo, yhi = [], [0], [], []
    conc_rows = -np.ones((nC, 3), np.int64)
    r = 0
    pop = np.zeros((len(years), NT))
    for y in years:
        ylo.append(r)
        for c, w in rows_by_year[y]:
            s = ex[c]["NB"][w]
            data.append(s)
            off.append(off[-1] + len(s))
            conc_rows[c, w - 1] = r
            pop[yi[y], s] += 1
            r += 1
        yhi.append(r)
    data0 = np.concatenate(data).astype(np.int32)
    off = np.asarray(off, np.int64)
    data_cb = data0.copy()
    t = time.time()
    s1, s2, nf = curveball_run(data_cb, off, np.asarray(ylo, np.int64), np.asarray(yhi, np.int64), conc_rows,
                               cfg["V3_CURVEBALL_SAMPLES"], 5, 20260932, NT)
    logger.info(f"V3c curveball: {r} rows, {len(years)} years, {time.time()-t:.1f}s")
    # U3: row and column sums preserved
    row_ok = bool(np.array_equal(np.diff(off), np.diff(off)))
    col_ok = True
    for y in years:
        lo, hi = off[ylo[yi[y]]], off[yhi[yi[y]]]
        col_ok &= bool(np.array_equal(np.bincount(data0[lo:hi], minlength=NT), np.bincount(data_cb[lo:hi], minlength=NT)))
    rowset_ok = all(len(np.unique(data_cb[off[i]:off[i + 1]])) == off[i + 1] - off[i] for i in range(0, r, max(1, r // 2000)))
    logger.info(f"U3 curveball: column sums preserved {col_ok}; rows remain sets {rowset_ok}")
    with np.errstate(invalid="ignore", divide="ignore"):
        pm = np.where(nf >= max(2, cfg["V3_CURVEBALL_SAMPLES"] // 2), s1 / np.maximum(nf, 1), np.nan)
        psd = np.sqrt(np.maximum(s2 / np.maximum(nf, 1) - pm ** 2, 0))
    obs_ep = df["edge_persistence__raw"].to_numpy(float)
    out = pd.DataFrame({"frame": df.frame, "ci": df.ci})
    out["pers_cfg_mean"] = pm
    out["pers_cfg_sd"] = psd
    out["excess_pers_cfg"] = obs_ep - pm
    with np.errstate(invalid="ignore", divide="ignore"):
        out["z_pers_cfg"] = np.where(psd > 0, (obs_ep - pm) / np.where(psd > 0, psd, 1), np.nan)
    # k-matched persistence approximation (full build and halves); weights = the year's neighbour popularity
    cum_pop = np.cumsum(pop, 1)
    pool_pop = (pop > 0).sum(1).astype(np.int64)
    years3 = np.stack([[yi[t + w] for w in range(3)] for t in t0s]).astype(np.int64)
    k3 = np.stack([[len(ex[c]["NB"][w]) for w in (1, 2, 3)] for c in range(nC)]).astype(np.int64)
    t = time.time()
    mu_k, sd_k = kpers_null(k3, np.arange(nC, dtype=np.int64), years3, self_flat, self_off, cum_pop, pool_pop,
                            cfg["V3_KSETS"], 20260933, NT)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["pers_k_mean"] = mu_k
        out["z_pers_k"] = np.where(sd_k > 0, (obs_ep - mu_k) / np.where(sd_k > 0, sd_k, 1), np.nan)
    logger.info(f"V3c k-matched full build {time.time()-t:.1f}s")
    hk3, hconc, hyears, hobs, hkey = [], [], [], [], []
    for c in range(nC):
        for h in ("A", "B"):
            for sp in range(S):
                hk3.append([len(ex[c]["half_NB"][h][sp][w]) for w in range(3)])
                hconc.append(c)
                hyears.append(years3[c])
                hobs.append(float(ex[c]["half_ep"][h][sp]))
                hkey.append((c, h, sp))
    t = time.time()
    hmu, hsd = kpers_null(np.asarray(hk3, np.int64), np.asarray(hconc, np.int64), np.asarray(hyears, np.int64),
                          self_flat, self_off, cum_pop, pool_pop, cfg["V3_HALF_DRAWS"], 20260934, NT)
    hobs = np.asarray(hobs)
    with np.errstate(invalid="ignore", divide="ignore"):
        hz_pers = np.where(hsd > 0, (hobs - hmu) / np.where(hsd > 0, hsd, 1), np.nan)
    logger.info(f"V3c k-matched halves ({len(hk3)} rows) {time.time()-t:.1f}s")
    # ---------------------------------------------------------------- V3b k-matched density null
    z = np.load(DATA_IN / "bg_topics.npz")
    bgy = {int(y): i for i, y in enumerate(z["years"])}
    BG = z["BG"].astype(float)
    cum_bg = np.cumsum(BG, 1)
    pool_bg = (BG > 0).sum(1).astype(np.int64)
    adj3 = np.zeros((3, NT, NT), np.bool_)
    for s in range(3):
        zz = np.load(INPUTS / "backbone" / f"slice{s}.npz")
        adj3[s, zz["a"], zz["b"]] = True
        adj3[s, zz["b"], zz["a"]] = True
    set_k = np.array([len(e["NB"][3]) for e in ex], np.int64)
    set_slice = np.array([slice_of(int(t) + 2) for t in t0s], np.int64)
    set_year = np.array([bgy[int(t) + 2] for t in t0s], np.int64)
    t = time.time()
    mk, sk = ksets_null(set_k, np.arange(nC, dtype=np.int64), set_slice, set_year, self_flat, self_off, cum_bg,
                        pool_bg, adj3, cfg["V3_KSETS"], 20260931, NT)
    e_obs = df["e_W3__raw"].to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["dens_k_mean"] = mk / (set_k * (set_k - 1) / 2)
        out["z_dens_k"] = np.where(sk > 0, (e_obs - mk) / np.where(sk > 0, sk, 1), np.nan)
    logger.info(f"V3b full build {time.time()-t:.1f}s")
    hsets = [ex[c]["half_NB"][h][sp][2] for (c, h, sp) in hkey]
    h_k = np.array([len(s) for s in hsets], np.int64)
    hc = np.array([c for c, _, _ in hkey], np.int64)
    t = time.time()
    hmk, hsk = ksets_null(h_k, hc, set_slice[hc], set_year[hc], self_flat, self_off, cum_bg, pool_bg, adj3,
                          cfg["V3_HALF_DRAWS"], 20260935, NT)
    # observed half-set edges in the real backbone
    pa, pb, sid = pairs_of(hsets)
    h_eobs = np.bincount(sid, weights=adj3[set_slice[hc][sid], pa, pb], minlength=len(hsets)) if len(sid) else \
        np.zeros(len(hsets))
    with np.errstate(invalid="ignore", divide="ignore"):
        hz_dk = np.where(hsk > 0, (h_eobs - hmk) / np.where(hsk > 0, hsk, 1), np.nan)
    logger.info(f"V3b halves {time.time()-t:.1f}s")
    del adj3
    # ---------------------------------------------------------------- collect V3a
    res = {s: futs[s].result() for s in range(3)}
    pool.shutdown()
    u4 = res[0].pop("_u4", {})
    zc3 = np.full(nC, np.nan)
    ec3 = np.full(nC, np.nan)
    zc1 = np.full(nC, np.nan)
    hz_dc = np.full(len(hkey), np.nan)
    hpos = {k: i for i, k in enumerate(hkey)}
    for s in range(3):
        for nm in ("W3", "W1", "H3"):
            obs, s1_, s2_, nd = res[s][nm]
            if nd == 0:
                continue
            mu = s1_ / nd
            sd = np.sqrt(np.maximum(s2_ / nd - mu ** 2, 0))
            with np.errstate(invalid="ignore", divide="ignore"):
                zz = np.where(sd > 0, (obs - mu) / np.where(sd > 0, sd, 1), np.nan)
            idx = index[s][nm]
            if nm == "W3":
                ii = np.asarray(idx, int)
                kk = set_k[ii]
                ok = kk >= 2
                zc3[ii[ok]] = zz[ok]
                with np.errstate(invalid="ignore", divide="ignore"):
                    ec3[ii[ok]] = (mu / (kk * (kk - 1) / 2))[ok]
                # consistency: observed count == S2 e_W3
                if not np.allclose(obs[ok], e_obs[ii[ok]]):
                    raise RuntimeError("V3a observed edge counts differ from S2 e_W3")
            elif nm == "W1":
                ii = np.asarray(idx, int)
                k1 = np.array([len(ex[i]["NB"][1]) for i in ii])
                ok = k1 >= 2
                zc1[ii[ok]] = zz[ok]
            else:
                kk = np.array([len(ex[c]["half_NB"][h][sp][2]) for (c, h, sp) in idx])
                for j, key in enumerate(idx):
                    if kk[j] >= 2:
                        hz_dc[hpos[key]] = zz[j]
    out["z_dens_cfg"] = zc3
    out["dens_cfg_exp"] = ec3
    out["z_dens_cfg_W1"] = zc1
    out.to_parquet(DATA / f"v3_nulls_{a.tag}.parquet", index=False)
    halves = {"key": [(df.frame.iat[c], int(df.ci.iat[c]), h, sp) for (c, h, sp) in hkey],
              "z_pers_k": hz_pers.astype(np.float32), "z_dens_k": hz_dk.astype(np.float32),
              "z_dens_cfg": hz_dc.astype(np.float32)}
    (DATA / f"v3_halves_{a.tag}.pkl").write_bytes(pickle.dumps(halves, protocol=5))
    ok = out[["z_pers_cfg", "z_pers_k"]].dropna()
    from scipy.stats import spearmanr
    rho = float(spearmanr(ok.z_pers_cfg, ok.z_pers_k)[0]) if len(ok) > 10 else math.nan
    jdump({"U3_curveball": {"column_sums_preserved": col_ok, "row_sizes_preserved": row_ok, "rows_remain_sets": rowset_ok},
           "U4_rewire": u4, "cfg": cfg, "n_concepts": nC, "n_rows_curveball": int(r),
           "spearman_z_pers_cfg_vs_k_matched": rho,
           "finite": {c: int(np.isfinite(out[c]).sum()) for c in out.columns if c not in ("frame", "ci")}},
          RES / f"v3_nulls_{a.tag}.json")
    logger.info(f"V3 done; spearman(z_pers_cfg, z_pers_k) = {rho:.3f}")


if __name__ == "__main__":
    main()
