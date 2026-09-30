#!/usr/bin/env python3
"""S6 FEATURES for Frame N (t0-3..t0+2 rows only; no sealed file is opened).

Per concept (open/early_frame.parquet detail rows + open/passN_pre_agg.parquet for years < t_det-5):
  B5 (EXP5 features.b5 via the EXP10 s6 port), CONTACT_REACH / RETENTION_RATIO_early (EXP8 fr_block), footprint
  fp_logN / fp_nfields (+ fp_reemerge / newborn, constant by construction, checked), label / home coverage,
  n_authors_early.
  EGO: EXP10 s7 concept_builds (HOME / ALL / SIZEMATCH, N_DRAWS = 20, seed 1000+ci) with the EXP10 rq1 context.
  CHENG (Cheng et al. 2023 operationalisation, OpenAlex topics as terms, SELF topics removed):
    consistency_{home,all} = mean over y in {t0+1, t0+2} of cosine(c_{y-1}[S], c_y[S]), S = {k: c_{y-1}[k] >= 1}
    (0 if S empty or c_y[S] all zero); embeddedness_home = mean pairwise cosine of the t0+2 co-used topics in a 200-dim
    PPMI-SVD embedding of backbone slice(t0+2) (>= 2 topics); prominence_home = count-weighted mean log background
    frequency (year t0+2) of the co-used topics.
  CLEAN (home build): (a) ego_density_W3_cz vs 200 degree-preserving rewirings of the slice backbone (+ Chung-Lu),
    (a') edge_persistence_sz (size-conditioned pool null, 200 draws), (b) NOVCHURN_home_rare (10 home papers per early
    year, 50 draws, seed 5000+ci), (c) edge_persistence_excess (200 within-concept year-label permutations).
Writes data/features_frame_n.parquet (NO outcome columns; asserted) and results/s6_diagnostics.json.
Usage: python s6_features.py [--workers 9] [--limit N] [--frame main|ext|all]"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, INPUTS, RES, ROOT, jdump, setup_logger, sha256_file

logger = setup_logger("s6_features")
Y0 = 1995
NY = 2022 - Y0 + 1
N_REWIRE = 200
N_SZ = 200
N_RARE = 50
N_PERM = 200
EMB = DATA / "topic_emb_ppmi_svd200.npz"
_W: dict = {}


# ----------------------------------------------------------------------------- embeddings (once, in main)
def build_embeddings() -> None:
    if EMB.exists():
        return
    from scipy.sparse import coo_matrix
    from scipy.sparse.linalg import svds
    out = {}
    for s in range(3):
        z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
        a, b, c, ck, W = z["a"], z["b"], z["c"].astype(float), z["ck"].astype(float), float(z["W"])
        with np.errstate(divide="ignore", invalid="ignore"):
            pmi = np.log(c * W / (ck[a] * ck[b]))
        ok = np.isfinite(pmi) & (pmi > 0)
        nt = len(ck)
        M = coo_matrix((np.r_[pmi[ok], pmi[ok]], (np.r_[a[ok], b[ok]], np.r_[b[ok], a[ok]])), shape=(nt, nt)).tocsr()
        U, S, _ = svds(M.astype(float), k=200, random_state=0)
        E = U * np.sqrt(S)
        E /= np.maximum(np.linalg.norm(E, axis=1, keepdims=True), 1e-12)
        out[f"E{s}"] = E.astype(np.float32)
    np.savez(EMB, **out)


# ----------------------------------------------------------------------------- worker
def _init() -> None:
    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    z = np.load(EMB)
    _W["E"] = [z[f"E{s}"] for s in range(3)]
    _W["logbg"] = {y: np.log1p(ego.C["bg"][ego.C["yidx"][y]].astype(float)) for y in ego.C["years"]}


def nb_sets(name: str, aliases: list[str], t0: int, works: list, SELF: np.ndarray | None = None) -> dict:
    """Replicates the neighbour-set lines of ego.concept_core (EXP3 PMI rule, SELF rule) and returns the sets.
    SELF depends only on the pooled t0..t0+2 counts, so a year-label permutation may pass it in (identical value)."""
    import ego
    win = ego.rq1_windows(t0)
    early_years = sorted(set(win["W1"] + win["W2"] + win["W3"]))
    if SELF is None:
        n_early, nc_early = ego.window_counts(works, early_years)
        SELF = ego.self_topics(name, aliases, n_early, nc_early)
    cnt, nc, bgw, NW, NB = {}, {}, {}, {}, {}
    for w, ys in win.items():
        cnt[w], nc[w] = ego.window_counts(works, ys)
        bgw[w], NW[w] = ego.bg_window(ys)
    for w in ("W1", "W2", "W3"):
        NB[w], _ = ego.neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, 2)
    return {"SELF": SELF, "cnt": cnt, "nc": nc, "bgw": bgw, "NW": NW, "NB": NB, "win": win}


def jac(a: np.ndarray, b: np.ndarray) -> float:
    u = (a | b).sum()
    return (a & b).sum() / u if u else float("nan")


def persistence(NB: dict) -> float:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        return float(np.nanmean([jac(NB["W1"], NB["W2"]), jac(NB["W2"], NB["W3"])]))


def cheng_cos(a: np.ndarray, b: np.ndarray) -> float:
    """Cheng et al. 2023 ideational consistency for one year pair: cosine of the co-usage counts over the t-1
    neighbours S = {k: a[k] >= 1}; 0 if S is empty or no t-1 neighbour is co-used in t."""
    S = a >= 1
    if not S.any() or b[S].sum() == 0:
        return 0.0
    return float(a[S] @ b[S] / (np.linalg.norm(a[S]) * np.linalg.norm(b[S])))


def cheng(works: list, t0: int, SELF: np.ndarray, nt: int) -> dict:
    import ego

    def cy(y):
        c = np.zeros(nt)
        for yy, tp in works:
            if yy == y:
                for k in tp:
                    c[k] += 1
        c[SELF] = 0
        return c
    cos = [cheng_cos(cy(y - 1), cy(y)) for y in (t0 + 1, t0 + 2)]
    out = {"consistency": float(np.mean(cos))}
    c2 = cy(t0 + 2)
    idx = np.nonzero(c2 > 0)[0]
    if len(idx) >= 2:
        E = _W["E"][ego.slice_of(t0 + 2)][idx]
        G = E @ E.T
        iu = np.triu_indices(len(idx), 1)
        out["embeddedness"] = float(G[iu].mean())
    else:
        out["embeddedness"] = float("nan")
    y = t0 + 2 if (t0 + 2) in _W["logbg"] else max(_W["logbg"])
    out["prominence"] = float((c2[idx] * _W["logbg"][y][idx]).sum() / c2[idx].sum()) if len(idx) else float("nan")
    return out


def gumbel_topk(pool: np.ndarray, w: np.ndarray, k: int, rng) -> np.ndarray:
    if k <= 0 or len(pool) == 0:
        return np.zeros(0, np.int64)
    k = min(k, len(pool))
    g = np.log(w[pool]) + rng.gumbel(size=len(pool))
    return pool[np.argpartition(-g, k - 1)[:k]]


def concept_features(job: dict) -> dict:
    import ego
    from s7ego_port import concept_builds, core6
    ci, name, aliases, t0 = job["ci"], job["name"], job["aliases"], job["t0"]
    rows, home = job["rows"], job["home_codes"]
    nt = ego.C["nt"]
    out = concept_builds(ci, name, aliases, t0, rows, home, builds=("home", "all", "sizematch"))
    works_all = [(y, tp) for y, tp, _ in rows]
    works_home = [(y, tp) for y, tp, v in rows if v in home]
    try:
        # ---------------- Cheng (home + all)
        sh = nb_sets(name, aliases, t0, works_home)
        ch = cheng(works_home, t0, sh["SELF"], nt)
        out.update({f"CHENG_{k}_home": v for k, v in ch.items()})
        sa = nb_sets(name, aliases, t0, works_all)
        out["CHENG_consistency_all"] = cheng(works_all, t0, sa["SELF"], nt)["consistency"]
        # sanity: replicated persistence equals the core's edge_persistence (home)
        out["_persist_replica_diff"] = abs(persistence(sh["NB"]) - out.get("edge_persistence__home", np.nan)) \
            if np.isfinite(out.get("edge_persistence__home", np.nan)) else 0.0
        out["_nbW3_home"] = np.nonzero(sh["NB"]["W3"])[0].astype(np.int32).tolist()
        out["_slice_W3"] = int(ego.slice_of(t0 + 2))
        # ---------------- (a') size-conditioned persistence null
        obs = persistence(sh["NB"])
        if np.isfinite(obs):
            rng = np.random.default_rng(3000 + ci)
            pools = {w: np.nonzero((sh["bgw"][w] > 0) & ~sh["SELF"])[0] for w in ("W1", "W2", "W3")}
            sizes = {w: int(sh["NB"][w].sum()) for w in ("W1", "W2", "W3")}
            nulls = []
            for _ in range(N_SZ):
                d = {}
                for w in ("W1", "W2", "W3"):
                    m = np.zeros(nt, bool)
                    m[gumbel_topk(pools[w], sh["bgw"][w], sizes[w], rng)] = True
                    d[w] = m
                nulls.append(persistence(d))
            nulls = np.asarray(nulls, float)
            nulls = nulls[np.isfinite(nulls)]
            sd = nulls.std() if len(nulls) > 2 else np.nan
            out["edge_persistence_sz"] = float((obs - nulls.mean()) / sd) if sd and sd > 0 else float("nan")
            out["edge_persistence_sz_nullmean"] = float(nulls.mean()) if len(nulls) else float("nan")
        else:
            out["edge_persistence_sz"] = out["edge_persistence_sz_nullmean"] = float("nan")
        # ---------------- (c) year-label permutation excess
        early = [(y, tp) for y, tp in works_home if t0 <= y <= t0 + 2]
        prew = [(y, tp) for y, tp in works_home if y < t0]
        if np.isfinite(obs) and len(early) >= 3:
            rng = np.random.default_rng(4000 + ci)
            ys = np.array([y for y, _ in early])
            perm_vals = []
            for _ in range(N_PERM):
                py = rng.permutation(ys)
                wk = prew + [(int(y), tp) for y, (_, tp) in zip(py, early)]
                s2 = nb_sets(name, aliases, t0, wk, SELF=sh["SELF"])
                perm_vals.append(persistence(s2["NB"]))
            pv = np.asarray(perm_vals, float)
            out["edge_persistence_excess"] = float(obs - np.nanmean(pv)) if np.isfinite(pv).any() else float("nan")
        else:
            out["edge_persistence_excess"] = float("nan")
        # ---------------- (b) rarefied NOVCHURN (10 home papers per early year)
        byy = {y: [i for i, (yy, _) in enumerate(works_home) if yy == y] for y in (t0, t0 + 1, t0 + 2)}
        if all(len(v) >= 10 for v in byy.values()):
            rng = np.random.default_rng(5000 + ci)
            pre_i = [i for i, (yy, _) in enumerate(works_home) if yy < t0]
            nv, ep = [], []
            for _ in range(N_RARE):
                pick = sorted(pre_i + [int(i) for y in byy for i in rng.choice(byy[y], 10, replace=False)])
                r = core6(name, aliases, t0, [works_home[i] for i in pick])
                nv.append(r["NOV_res"]); ep.append(r["edge_persistence"])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                out["NOV_res_rare"] = float(np.nanmean(nv)) if np.isfinite(nv).sum() >= N_RARE / 2 else float("nan")
                out["edge_persistence_rare"] = float(np.nanmean(ep)) if np.isfinite(ep).sum() >= N_RARE / 2 \
                    else float("nan")
        else:
            out["NOV_res_rare"] = out["edge_persistence_rare"] = float("nan")
    except (ValueError, IndexError, ZeroDivisionError) as e:
        out["feat_error"] = repr(e)[:200]
    return out


def run_chunk(k: int, jobs: list) -> tuple[int, list, float]:
    t = time.time()
    return k, [concept_features(j) for j in jobs], time.time() - t


# ----------------------------------------------------------------------------- rewiring null for ego density
def rewire_task(s: int, r: int, sets: list[tuple[int, np.ndarray]]) -> tuple[int, int, list[tuple[int, int]]]:
    import igraph as ig
    from scipy.sparse import coo_matrix
    z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
    a, b = z["a"], z["b"]
    nt = len(z["ck"])
    g = ig.Graph(n=nt, edges=np.c_[a, b].tolist(), directed=False)
    import random
    random.seed(31 + r)
    ig.set_random_number_generator(random)
    g.rewire(n=10 * g.ecount(), allowed_edge_types="simple")
    el = np.asarray(g.get_edgelist(), np.int64)
    A = coo_matrix((np.ones(2 * len(el)), (np.r_[el[:, 0], el[:, 1]], np.r_[el[:, 1], el[:, 0]])),
                   shape=(nt, nt)).tocsr()
    assert np.array_equal(np.asarray(A.sum(1)).ravel(), np.bincount(np.r_[a, b], minlength=nt)), "degree changed"
    res = []
    for ci, idx in sets:
        res.append((ci, int(A[idx][:, idx].sum() // 2)))
    return s, r, res


def ego_density_cz(feat: pd.DataFrame, workers: int) -> pd.DataFrame:
    from scipy.sparse import coo_matrix
    sets = {s: [] for s in range(3)}
    for ci, idx, s in zip(feat.ci, feat._nbW3_home, feat._slice_W3):
        idx = np.asarray(idx, np.int64)
        if len(idx) >= 2:
            sets[int(s)].append((int(ci), idx))
    obs, chung = {}, {}
    for s in range(3):
        z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
        a, b = z["a"], z["b"]
        nt = len(z["ck"])
        A = coo_matrix((np.ones(2 * len(a)), (np.r_[a, b], np.r_[b, a])), shape=(nt, nt)).tocsr()
        deg = np.bincount(np.r_[a, b], minlength=nt).astype(float)
        m2 = deg.sum()
        for ci, idx in sets[s]:
            obs[ci] = int(A[idx][:, idx].sum() // 2)
            d = deg[idx]
            chung[ci] = float((d.sum() ** 2 - (d ** 2).sum()) / 2 / m2)
    acc = {ci: [] for s in sets for ci, _ in sets[s]}
    t = time.time()
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn")) as ex:
        futs = [ex.submit(rewire_task, s, r, sets[s]) for s in range(3) if sets[s] for r in range(N_REWIRE)]
        for i, fu in enumerate(as_completed(futs)):
            _, _, res = fu.result()
            for ci, e in res:
                acc[ci].append(e)
            if i % 100 == 0:
                logger.info(f"rewiring {i+1}/{len(futs)} ({(time.time()-t)/60:.1f} min)")
    rows = []
    for ci, v in acc.items():
        v = np.asarray(v, float)
        sd = v.std()
        rows.append({"ci": ci, "ego_density_W3_cz": (obs[ci] - v.mean()) / sd if sd > 0 else float("nan"),
                     "ego_edges_W3_obs": obs[ci], "ego_edges_W3_rewire_mean": v.mean(),
                     "ego_edges_W3_chunglu": chung[ci]})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------------- covariates
def covariates(fr: pd.DataFrame, early: pd.DataFrame, pre: pd.DataFrame) -> pd.DataFrame:
    from s6cov_port import b5, fr_block
    cis = fr.ci.to_numpy()
    pos = pd.Series(np.arange(len(cis)), index=cis)
    N = np.zeros((len(cis), NY))
    V = np.zeros((len(cis), NY, 27))
    for d, is_agg in ((pre, True), (early, False)):
        d = d[d.ci.isin(set(cis))]
        w = d.n.to_numpy(float) if is_agg else np.ones(len(d))
        f = pos.loc[d.ci.to_numpy()].to_numpy()
        y = d.year.to_numpy(np.int64) - Y0
        ok = (y >= 0) & (y < NY)
        np.add.at(N, (f[ok], y[ok]), w[ok])
        np.add.at(V, (f[ok], y[ok], d.vfield.to_numpy(np.int64)[ok]), w[ok])
    auth = early.merge(fr[["ci", "t0"]], on="ci")
    auth = auth[(auth.year >= auth.t0) & (auth.year <= auth.t0 + 2)]
    authors = {int(ci): {a for lst in g.authors for a in lst} for ci, g in auth.groupby("ci")}
    rows = []
    for f, r in enumerate(fr.itertuples()):
        t0 = int(r.t0)
        assert N[f, t0 + 3 - Y0:].sum() == 0, "a count beyond t0+2 reached the covariates"
        home = [int(float(x)) for x in str(r.home).split(";") if x and x != "nan"]
        n = N[f]
        pre_v = V[f, :t0 - Y0, 1:27].sum(0)
        rec = {"ci": int(r.ci), "fp_logN": math.log1p(n[max(t0 - 10 - Y0, 0):t0 - Y0].sum()),
               "fp_nfields": int((pre_v >= 1).sum()),
               "fp_reemerge": int(any(n[y - Y0] >= 0.25 * n[t0 + 2 - Y0] for y in range(Y0, t0))),
               "newborn": int(all(n[t0 - k - Y0] < 0.25 * n[t0 + 2 - Y0] for k in (1, 2, 3)))}
        rec.update(b5(n, V[f], t0, [h - 11 for h in home]))
        rec.update(fr_block(V[f], t0, home))
        early_n = n[t0 - Y0:t0 + 3 - Y0].sum()
        rec["label_coverage_early"] = float(V[f, t0 - Y0:t0 + 3 - Y0, 1:27].sum() / early_n) if early_n else math.nan
        rec["N_t0p2"] = float(n[t0 + 2 - Y0])
        rec["logN2"] = math.log1p(n[t0 + 2 - Y0])
        a = authors.get(int(r.ci))
        rec["n_authors_early"] = math.log1p(len(a)) if a else math.nan
        rows.append(rec)
    return pd.DataFrame(rows)


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=9)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--chunk", type=int, default=25)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    import s6cov_port
    s6cov_port.logger = logger
    fr = pd.read_csv(DATA / "frame_n_concepts.csv").rename(columns={"n_home_early": "n_home_early_gate"})
    if a.limit:
        fr = fr.head(a.limit)
    early = pd.read_parquet(ROOT / "open/early_frame.parquet")
    early = early[early.ci.isin(set(fr.ci))]
    early = early.merge(fr[["ci", "t0"]], on="ci")
    assert (early.year <= early.t0 + 2).all(), "early_frame holds a year beyond t0+2"
    early = early.drop(columns=["t0"])
    pre = pd.read_parquet(ROOT / "open/passN_pre_agg.parquet")
    pre = pre[pre.ci.isin(set(fr.ci))].groupby(["ci", "year", "vfield"], as_index=False)["n"].sum()
    cov = covariates(fr, early, pre)
    logger.info(f"covariates for {len(cov)}; fp_reemerge mean {cov.fp_reemerge.mean():.3f}, newborn mean "
                f"{cov.newborn.mean():.3f}")
    build_embeddings()
    # ego jobs
    e6 = early.merge(fr[["ci", "t0"]], on="ci")
    e6 = e6[e6.year >= e6.t0 - 3]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(int(x) for x in t) for t in d.topics],
                       d.vfield.astype(int).tolist())) for ci, d in e6.groupby("ci")}
    jobs = []
    for r in fr.itertuples():
        al = [x for x in str(r.aliases).split("|") if x and x != "nan"]
        jobs.append({"ci": int(r.ci), "name": str(r.name), "aliases": al, "t0": int(r.t0), "rows": by.get(r.ci, []),
                     "home_codes": {int(float(x)) - 10 for x in str(r.home).split(";") if x}})
    outdir = DATA / f"feat_chunks{a.tag}"
    outdir.mkdir(parents=True, exist_ok=True)
    chunks = [jobs[i:i + a.chunk] for i in range(0, len(jobs), a.chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.pkl").exists()]
    logger.info(f"ego/cheng/clean: {len(jobs)} concepts, {len(chunks)} chunks, todo {len(todo)}")
    t = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_chunk, k, chunks[k]) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, res, dt = fu.result()
            pd.DataFrame(res).to_pickle(outdir / f"chunk_{k:05d}.pkl")
            if i % 10 == 0 or i == len(futs) - 1:
                el = time.time() - t
                logger.info(f"chunk {i+1}/{len(futs)} {el/60:.1f} min; {dt/len(res):.2f} s/concept/worker; "
                            f"eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min")
    feat = pd.concat([pd.read_pickle(p) for p in sorted(outdir.glob("chunk_*.pkl"))], ignore_index=True)
    logger.info(f"persistence replica max diff {feat._persist_replica_diff.max():.2e}")
    cz = ego_density_cz(feat, a.workers)
    feat = feat.merge(cz, on="ci", how="left")
    df = fr.merge(cov, on="ci").merge(feat.drop(columns=["_nbW3_home"]), on="ci")
    df["home_coverage_early"] = df.n_home_early / df.n_all_early.replace(0, np.nan)
    out_cols = [c for c in df.columns if c.startswith(("O1", "O2", "O3", "V_next"))]
    assert not out_cols, f"outcome columns in the feature table: {out_cols}"
    df.to_parquet(DATA / f"features_frame_n{a.tag}.parquet", index=False)
    logger.info(f"wrote features_frame_n{a.tag}.parquet: {df.shape}")


if __name__ == "__main__":
    main()
