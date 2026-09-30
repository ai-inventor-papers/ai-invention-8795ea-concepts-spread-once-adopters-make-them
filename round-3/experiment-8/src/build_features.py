#!/usr/bin/env python3
"""STEP 3: the RQ1 indicator matrix over the feature window t0..t0+2 ONLY (about 53 indicators, 7 families).

  E  popularity / count references : share, growth_ind, accel, burst (EXP5), author_growth, n_authors_early (Pass A)
  F  disciplinary                  : log_offhome_volume (EXP5), rao_stirling (phi-distance), fields_gained_per_yr
  G  landing (EXP5; previously scored on held-out for O2r_resid): G, G_A, G_btw, G_deg, G_phimin, REL_home, RS
  FR retained frontier (D3 of EXP6): CONTACT_REACH, RETAINED_REACH, RETENTION_RATIO_early, FRONTIER_POTENTIAL,
                                     D_rca_end, D_vol_end, M0_density_end
  A  co-occurrence ego network     : 27 indicators (lib/ego.py)
  S  social (co-author components) : S_comp, S_comp_n, S_isolated_share
  B5 baseline (not a candidate)    : logvol, growth_c, offhome_share, entropy, reach (EXP5, identical definitions)

Usage: python build_features.py --stage {basic,ego,assemble,all} [--workers 5] [--limit N] [--timing 60]"""
from __future__ import annotations

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import (DATA, EXP5, INPUTS, NY, RES, SEED, Y0, add_deviation, jdump, load_frame, read_parquet_parts,
                    setup_logger)

EGO_DIR = DATA / "ego_parts_c3"
EGO_DIR.mkdir(parents=True, exist_ok=True)
N_NULL = 200
BTW_CUTOFF = 3
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]


def yi(y: int) -> int:
    return y - Y0


def home_list(h) -> list[int]:
    return [int(float(x)) for x in str(h).split(";") if x and x != "nan"]


# ----------------------------------------------------------------------------- D3 state machine (EXP6 lib/h2.py, verbatim)
def states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:
    """g: [NY, 27] grounded counts. Returns boolean [NY, 26] matrices (years Y0..)."""
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
    """EXP6 h2.rca_entered verbatim."""
    x = np.cumsum(g[:, 1:], 0)
    tot = x.sum(1, keepdims=True)
    F = np.cumsum(GF, 0)
    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)
    share_c = x / np.maximum(tot, 1)
    ok = (x >= 2) & (share_c > share_all)
    return np.maximum.accumulate(ok.astype(int), 0).astype(bool)


def load_arrays(fr: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
    """N[f, y] grounded (TAG) counts all venues, V[f, y, 27] by venue-field code, for frame rows f."""
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[ag.tagstate == 1]
    pos = pd.Series(np.arange(len(fr)), index=fr.ci.to_numpy())
    ag = ag[ag.ci.isin(pos.index)]
    f = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    f, y, vf, n = f[ok], y[ok], ag.vfield.to_numpy(np.int64)[ok], ag.n.to_numpy(np.float64)[ok]
    NF = len(fr)
    N = np.bincount(f * NY + y, weights=n, minlength=NF * NY).reshape(NF, NY)
    V = np.bincount((f * NY + y) * 27 + vf, weights=n, minlength=NF * NY * 27).reshape(NF, NY, 27)
    return N, V


def social(e: pd.DataFrame, home_codes: set[int]) -> dict:
    """Family S: co-author components among the concept's OFF-HOME labelled early works (t0..t0+2)."""
    off = e[(e.vfield > 0) & (~e.vfield.isin(home_codes))]
    n_off = len(off)
    if n_off == 0:
        return {"S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan, "S_author_coverage": np.nan,
                "n_offhome_early": 0}
    au = [a for a in off.authors if len(a)]
    cov = len(au) / n_off
    if cov < 0.5 or len(au) < 2:
        return {"S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan, "S_author_coverage": cov,
                "n_offhome_early": n_off}
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
    # papers per component -> isolated papers (share no author with any other off-home paper)
    comp_papers = {}
    for a in au:
        rr = find(a[0])
        comp_papers[rr] = comp_papers.get(rr, 0) + 1
    iso = sum(1 for v in comp_papers.values() if v == 1)
    return {"S_comp": len(roots) / len(au), "S_comp_n": len(roots) / len(parent), "S_isolated_share": iso / len(au),
            "S_author_coverage": cov, "n_offhome_early": n_off}


def stage_basic(logger) -> None:
    fr = load_frame()
    N, V = load_arrays(fr)
    np.savez_compressed(DATA / "frame_arrays.npz", N=N.astype(np.float32), V=V.astype(np.float32),
                        ci=fr.ci.to_numpy())
    bb = json.loads((INPUTS / "field_backbone.json").read_text())
    phi = np.asarray(bb["phi"], float)
    phin = phi / phi.max()
    D = 1 - phin
    np.fill_diagonal(D, 0)
    colsum = phi.sum(0)
    GF = np.load(EXP5 / "scan/year_field_totals.npz")["VF"][:, 1:].astype(float)  # [NY, 26] venue-field base totals
    basic = pd.read_csv(EXP5 / "concept_features_basic.csv")
    em = read_parquet_parts(DATA / "frame_matches_early", columns=["ci", "year", "work_id", "vfield", "authors"])
    em = em.merge(fr[["ci", "t0"]], on="ci")
    em = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)]
    groups = dict(tuple(em.groupby("ci")))
    rows = []
    for f, r in enumerate(fr.itertuples()):
        home = home_list(r.home)
        hcodes = {h - 10 for h in home}
        t0 = int(r.t0)
        g = V[f].copy()                       # [NY, 27]
        # --- window-restricted counts (t0..t0+2 only; D3 state machine applied to the window)
        gw = np.zeros_like(g)
        gw[yi(t0):yi(t0 + 2) + 1] = g[yi(t0):yi(t0 + 2) + 1]
        S = states(gw, home)
        ent_end = S["entered"][yi(t0 + 2)] & S["offhome"]
        ent_start = S["entered"][yi(t0)] & S["offhome"]
        x = g[yi(t0):yi(t0 + 2) + 1, 1:]      # [3, 26]
        off = S["offhome"]
        contact = int(((x.sum(0) >= 1) & off).sum())
        retained = ((x >= 2).sum(0) >= 2) & off
        rr = int(retained.sum())
        rec = {"ci": r.ci, "CONTACT_REACH": contact, "RETAINED_REACH": rr,
               "RETENTION_RATIO_early": rr / max(contact, 1), "RETENTION_RATIO_missing": int(contact == 0)}
        cand = ~ent_end & off
        rec["FRONTIER_POTENTIAL"] = float(phi[np.ix_(retained, cand)].mean(0).sum()) if rr else 0.0
        rec["fields_gained_per_yr"] = (int(ent_end.sum()) - int(ent_start.sum())) / 2.0
        # D3 end-of-window states on the FULL history up to t0+2 (as in EXP6)
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
        if tot > 0:
            p = lab / tot
            rec["rao_stirling"] = float(p @ D @ p)
        else:
            rec["rao_stirling"] = np.nan
        e = groups.get(r.ci)
        if e is not None and len(e):
            a0 = {a for lst in e[e.year == t0].authors for a in lst}
            a2 = {a for lst in e[e.year == t0 + 2].authors for a in lst}
            aall = {a for lst in e.authors for a in lst}
            rec["author_growth"] = math.log1p(len(a2)) - math.log1p(len(a0))
            rec["n_authors_early"] = math.log1p(len(aall))
            rec["author_id_coverage"] = float(np.mean([len(a) > 0 for a in e.authors]))
            rec["n_early_works_passA"] = int(len(e))
            rec.update(social(e, hcodes))
        else:
            rec.update({"author_growth": np.nan, "n_authors_early": np.nan, "author_id_coverage": np.nan,
                        "n_early_works_passA": 0, "S_comp": np.nan, "S_comp_n": np.nan, "S_isolated_share": np.nan,
                        "S_author_coverage": np.nan, "n_offhome_early": 0})
        rows.append(rec)
    df = pd.DataFrame(rows).merge(basic.drop(columns=["concept_id"]), on="ci", how="left")
    df.to_parquet(DATA / "features_basic.parquet", index=False)
    logger.info(f"basic families: {df.shape}")


# ----------------------------------------------------------------------------- family A (parallel)
_CTX_LOADED = {"ok": False}


def _init_ego() -> None:
    import ego
    from ego_ctx import rq1_context
    ego.set_context(rq1_context())
    _CTX_LOADED["ok"] = True


def ego_chunk(chunk_id: int, jobs: list, n_null: int, btw_cutoff: int, nb_min_w: int) -> tuple[int, list, float]:
    import ego
    t = time.time()
    out = []
    for ci, name, aliases, t0, works in jobs:
        try:
            r = ego.concept_core(name, aliases, t0, works, n_null, SEED + int(ci), btw_cutoff=btw_cutoff,
                                 nb_min_w=nb_min_w)
            r["_top_nb_W3"] = json.dumps(r["_top_nb_W3"])
        except (ValueError, IndexError, ZeroDivisionError) as e:
            r = {"ego_error": repr(e)[:200]}
        r["ci"] = int(ci)
        out.append(r)
    return chunk_id, out, time.time() - t


def ego_jobs(fr: pd.DataFrame) -> list:
    em = read_parquet_parts(DATA / "frame_matches_early", columns=["ci", "year", "topics"])
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics])) for ci, d in em.groupby("ci")}
    jobs = []
    for r in fr.itertuples():
        al = [a for a in str(r.aliases_used).split("|") if a and a != "nan"]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, [])))
    return jobs


def stage_ego(logger, workers: int, limit: int = 0, timing: int = 0, n_null: int = N_NULL,
              btw_cutoff: int = BTW_CUTOFF, nb_min_w: int = 2, chunk: int = 40, subset: list[int] | None = None) -> dict:
    fr = load_frame()
    if subset is not None:
        fr = fr[fr.ci.isin(subset)]
    if timing:
        fr = fr[fr.split == "DEV"].sample(timing, random_state=SEED)
    jobs = ego_jobs(fr)
    if limit:
        jobs = jobs[:limit]
    outdir = EGO_DIR if not timing else DATA / "ego_timing"
    outdir.mkdir(parents=True, exist_ok=True)
    chunks = [jobs[i:i + chunk] for i in range(0, len(jobs), chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.parquet").exists()] if not timing \
        else list(range(len(chunks)))
    logger.info(f"ego: {len(jobs)} concepts, {len(chunks)} chunks, todo {len(todo)}, workers {workers}, "
                f"N_NULL {n_null}, btw cutoff {btw_cutoff}, nb_min_w {nb_min_w}")
    t0 = time.time()
    per = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init_ego) as ex:
        futs = [ex.submit(ego_chunk, k, chunks[k], n_null, btw_cutoff, nb_min_w) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, out, dt = fu.result()
            pd.DataFrame(out).to_parquet(outdir / f"chunk_{k:05d}.parquet", index=False)
            per.append(dt / max(len(out), 1))
            if i % 10 == 0 or i == len(futs) - 1:
                el = time.time() - t0
                logger.info(f"ego chunk {i+1}/{len(futs)} {el/60:.1f} min; {np.mean(per):.2f} s/concept/worker; "
                            f"eta {el / (i+1) * (len(futs) - i - 1) / 60:.1f} min")
    return {"n": len(jobs), "wall_s": time.time() - t0, "s_per_concept_worker": float(np.mean(per)) if per else None}


def stage_assemble(logger) -> None:
    fr = load_frame()
    b = pd.read_parquet(DATA / "features_basic.parquet")
    parts = sorted(EGO_DIR.glob("chunk_*.parquet"))
    eg = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True) if parts else pd.DataFrame({"ci": []})
    eg.to_parquet(DATA / "ego_features.parquet", index=False)
    X = fr[["ci", "concept_id", "name", "t0", "group", "split", "unit", "home", "intersect40",
            "label_coverage_early", "tag_coverage", "precision_c", "early_volume"]].merge(b, on="ci", how="left")
    X = X.merge(eg.drop(columns=[c for c in eg.columns if c.startswith("_")], errors="ignore"), on="ci", how="left")
    X.to_parquet(RES / "indicator_matrix.parquet", index=False)
    logger.info(f"indicator matrix {X.shape}; ego rows {len(eg)}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--timing", type=int, default=0)
    ap.add_argument("--n_null", type=int, default=N_NULL)
    ap.add_argument("--btw_cutoff", type=int, default=BTW_CUTOFF)
    ap.add_argument("--nb_min_w", type=int, default=2)
    a = ap.parse_args()
    logger = setup_logger("features")
    if a.stage in ("basic", "all"):
        stage_basic(logger)
    if a.stage in ("ego", "all") or a.timing:
        r = stage_ego(logger, a.workers, a.limit, a.timing, a.n_null, a.btw_cutoff, a.nb_min_w,
                      chunk=4 if a.timing else 40)
        if a.timing:
            jdump({**r, "n_null": a.n_null, "btw_cutoff": a.btw_cutoff, "nb_min_w": a.nb_min_w},
                  RES / f"t4_timing_nnull{a.n_null}_cut{a.btw_cutoff}.json")
            return
    if a.stage in ("assemble", "all"):
        stage_assemble(logger)


if __name__ == "__main__":
    main()
