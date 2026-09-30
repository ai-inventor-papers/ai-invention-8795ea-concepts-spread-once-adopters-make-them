#!/usr/bin/env python3
"""S7 (family A): the six OPEN components under three builds -- ALL, HOME, SIZEMATCH -- over t0-3..t0+2 only.

Components (EXP8 lib/ego.concept_core, n_null = 0, compute_btw = False): new_edge_rate, n_comm_W3, participation,
NOV_res, ego_density_W3, edge_persistence.
  ALL        every grounded early paper (EXP8 definition)
  HOME       only grounded papers whose venue field is in the concept's home set (PRE and W1-W3); unlabelled dropped
  SIZEMATCH  20 seeded subsamples (seed = 1000 + ci) of ALL papers, each window (PRE, W1, W2, W3) cut to that window's
             HOME count; components averaged over the draws

Usage: python s7_ego.py --frame exp5|cohort [--builds home,sizematch,all] [--workers 3] [--limit N] [--subset ci,...]"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP8, load_frame, read_parquet_parts, setup_logger

COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
N_DRAWS = 20
OUT = DATA / "ego_open"


def _init() -> None:
    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())


def core6(name: str, aliases: list[str], t0: int, works: list) -> dict:
    import ego
    r = ego.concept_core(name, aliases, t0, works, 0, 0, compute_btw=False)
    return {k: float(r[k]) for k in COMPONENTS} | {"M": int(r["M"])}


def window_of(y: int, t0: int) -> int:
    return 0 if y < t0 else y - t0 + 1        # 0 = PRE, 1..3 = W1..W3


def concept_builds(ci: int, name: str, aliases: list[str], t0: int, rows: list, home_codes: set[int],
                   builds: tuple[str, ...]) -> dict:
    """rows = [(year, topics tuple, vfield)] grounded early papers t0-3..t0+2."""
    out: dict = {"ci": ci}
    works_all = [(y, tp) for y, tp, _ in rows]
    home_mask = np.array([v in home_codes for _, _, v in rows], bool)
    works_home = [w for w, h in zip(works_all, home_mask) if h]
    yrs = np.array([y for y, _, _ in rows], np.int64)
    in_early = (yrs >= t0) & (yrs <= t0 + 2)
    out["n_all_early"] = int(in_early.sum())
    out["n_home_early"] = int((in_early & home_mask).sum())
    out["n_all_pre"] = int((yrs < t0).sum())
    out["n_home_pre"] = int(((yrs < t0) & home_mask).sum())
    try:
        if "full" in builds:   # EXP8 family-A settings (N_NULL 200, betweenness cutoff 3) for the learned models
            import ego
            r = ego.concept_core(name, aliases, t0, works_all, 200, 20260928 + int(ci), btw_cutoff=3, nb_min_w=2)
            out.update({f"{k}__full": float(r[k]) for k in ego.EGO_OUT})
        if "all" in builds:
            out.update({f"{k}__all": v for k, v in core6(name, aliases, t0, works_all).items()})
        if "home" in builds:
            out.update({f"{k}__home": v for k, v in core6(name, aliases, t0, works_home).items()})
        if "sizematch" in builds:
            rng = np.random.default_rng(1000 + int(ci))
            win = np.array([window_of(y, t0) for y in yrs], np.int64)
            idx_by = [np.nonzero(win == w)[0] for w in range(4)]
            need = [int((home_mask & (win == w)).sum()) for w in range(4)]
            acc = {k: [] for k in COMPONENTS + ["M"]}
            for _ in range(N_DRAWS):
                pick = np.concatenate([rng.choice(idx_by[w], size=need[w], replace=False) if need[w] else
                                       np.zeros(0, np.int64) for w in range(4)])
                pick.sort()
                r = core6(name, aliases, t0, [works_all[i] for i in pick])
                for k in acc:
                    acc[k].append(r[k])
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", RuntimeWarning)
                for k, v in acc.items():
                    v = np.asarray(v, float)
                    # a component is defined for the build if it is finite in >= half of the draws
                    out[f"{k}__sizematch"] = float(np.nanmean(v)) if np.isfinite(v).sum() >= N_DRAWS / 2 else np.nan
    except (ValueError, IndexError, ZeroDivisionError) as e:
        out["ego_error"] = repr(e)[:200]
    return out


def run_chunk(k: int, jobs: list, builds: tuple[str, ...]) -> tuple[int, list, float]:
    t = time.time()
    res = [concept_builds(*j, builds=builds) for j in jobs]
    return k, res, time.time() - t


def home_codes_of(h) -> set[int]:
    return {int(float(x)) - 10 for x in str(h).split(";") if x and x != "nan"}


def jobs_exp5(subset=None) -> list:
    fr = load_frame()
    if subset is not None:
        fr = fr[fr.ci.isin(subset)]
    em = read_parquet_parts(EXP8 / "data/frame_matches_early", columns=["ci", "year", "topics", "vfield"])
    em = em[em.ci.isin(set(fr.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    jobs = []
    for r in fr.itertuples():
        al = [a for a in str(r.aliases_used).split("|") if a and a != "nan"]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def jobs_cohort(subset=None) -> list:
    cf = pd.read_csv(DATA / "cohort_candidates.csv")
    lex = pd.read_parquet(Path(__file__).resolve().parent / "inputs/lexicon_v1.parquet", columns=["aliases_used"])
    if subset is not None:
        cf = cf[cf.ci.isin(subset)]
    em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "topics", "vfield", "tagstate"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    jobs = []
    for r in cf.itertuples():
        al = [a for a in str(lex.aliases_used.iat[r.ci]).split("|") if a and a not in ("nan", "None")]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--frame", required=True, choices=["exp5", "cohort"])
    ap.add_argument("--builds", default="home,sizematch")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument("--subset", default="")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    logger = setup_logger(f"s7_ego_{a.frame}{a.tag}")
    builds = tuple(a.builds.split(","))
    subset = [int(x) for x in a.subset.split(",")] if a.subset else None
    jobs = jobs_exp5(subset) if a.frame == "exp5" else jobs_cohort(subset)
    if a.limit:
        jobs = jobs[:a.limit]
    outdir = OUT / f"{a.frame}{a.tag}"
    outdir.mkdir(parents=True, exist_ok=True)
    chunks = [jobs[i:i + a.chunk] for i in range(0, len(jobs), a.chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.parquet").exists()]
    logger.info(f"{a.frame}: {len(jobs)} concepts, builds {builds}, {len(chunks)} chunks, todo {len(todo)}, "
                f"workers {a.workers}")
    t0 = time.time()
    done_n = 0
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_chunk, k, chunks[k], builds) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, res, dt = fu.result()
            pd.DataFrame(res).to_parquet(outdir / f"chunk_{k:05d}.parquet", index=False)
            done_n += len(res)
            el = time.time() - t0
            logger.info(f"chunk {i+1}/{len(futs)} ({done_n} concepts) {el/60:.1f} min; {dt/len(res):.2f} s/concept/"
                        f"worker; eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min")
    parts = sorted(outdir.glob("chunk_*.parquet"))
    df = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)
    df.to_parquet(DATA / f"ego_open_{a.frame}{a.tag}.parquet", index=False)
    logger.info(f"wrote {len(df)} rows -> data/ego_open_{a.frame}{a.tag}.parquet")


if __name__ == "__main__":
    main()
