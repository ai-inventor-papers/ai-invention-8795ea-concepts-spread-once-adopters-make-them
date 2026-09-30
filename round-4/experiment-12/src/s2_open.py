#!/usr/bin/env python3
"""S1 LOAD+JOIN and S2 OPEN covariates in three builds (outcome-free; all 12,499 concepts before the seal).

  ALL-PAPERS   : EXP8 ego_features (the 6 OPEN components), reproduced here by lib/ego_open.py (T2 test)
  HOME-ONLY    : ego_open on the concept's frame_matches_early rows whose venue field is a home field
  SIZE-MATCHED : ego_open on 20 year-stratified random subsamples of ALL t0..t0+2 works down to n_home, averaged
OPEN = mean of available [z(new_edge_rate), z(n_comm_W3), z(participation), z(NOV_res), -z(ego_density_W3),
-z(edge_persistence)] when >= 4 of 6 are present; z constants over all 12,499 frame concepts, per build (ddof = 0).

Usage: python s2_open.py --stage {join,test,timing,home,size,assemble,all} [--workers 24]"""
from __future__ import annotations

import argparse
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from common import (DATA, E8_DATA, LOGS, OPEN_COMPONENTS, RES, SEED, add_deviation, jdump, load_frame,  # noqa: E402
                    network_guard, setup_logger, spearman, update_status)

network_guard()
logger = setup_logger("s2_open")
PARTS = DATA / "open_parts"
KEYS = [k for k, _ in OPEN_COMPONENTS]
N_DRAWS = 20


# ----------------------------------------------------------------------------- S1
def stage_join() -> pd.DataFrame:
    fr = load_frame()
    A = pd.read_parquet(E8_DATA / "analysis_table.parquet")
    outc = {"O1c", "O2r_m50", "O2r_resid", "O4", "O1b", "O3", "O5", "O5_WW", "O5_sens", "O5_WW_sens", "O2r_m30",
            "O2r_resid_N"}
    keep = ["ci", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "RETAINED_REACH",
            "RETENTION_RATIO_early", "RETENTION_RATIO_missing", "n_authors_early", "D_vol_end", "M0_density_end",
            "label_coverage_early"] + KEYS + ["ego_density_W1", "M", "NOV", "deg_W1", "deg_W3"]
    assert not (set(keep) & outc)
    A = A[keep].rename(columns={k: f"{k}_all" for k in KEYS}).rename(columns={"label_coverage_early": "lc_e8"})
    J = fr.merge(A, on="ci", how="left", validate="1:1")
    assert len(J) == 12499 and J.logvol.notna().all()
    J = J.drop(columns=["home_list"]).assign(home_list=[";".join(map(str, h)) for h in fr.home_list])
    J.to_parquet(DATA / "joined.parquet", index=False)
    counts = {"n": len(J), "by_split": J.split.value_counts().to_dict(),
              "by_split_group": J.groupby(["split", "group"]).size().rename("n").reset_index().to_dict("records"),
              "by_rgroup": J.rgroup.value_counts().to_dict(), "med_home": int(J.med_home.sum()),
              "med_home_by_split": J.groupby("split").med_home.sum().to_dict(),
              "intersection_born": int(J.intersection_born.sum()), "in_exp6": int(J.in_exp6.sum()),
              "label_coverage_equal_e8": bool(np.allclose(J.label_coverage_early, J.lc_e8, equal_nan=True))}
    jdump(counts, LOGS / "join.json")
    logger.info(f"S1 join: {counts['by_split']}; med_home {counts['med_home']}; in_exp6 {counts['in_exp6']}")
    return J


# ----------------------------------------------------------------------------- workers
def _init() -> None:
    import ego_open
    from ego_ctx import rq1_context
    ego_open.set_context(rq1_context())


def _run_one(name, aliases, t0, works, nb_min_w=2) -> dict:
    import ego_open
    try:
        return ego_open.concept_open(name, aliases, t0, works, nb_min_w=nb_min_w)
    except (ValueError, IndexError, ZeroDivisionError) as e:
        return {"ego_error": repr(e)[:200]}


def chunk_plain(chunk_id: int, jobs: list, nb_min_w: int) -> tuple[int, list, float]:
    t = time.time()
    out = []
    for ci, name, aliases, t0, works in jobs:
        r = _run_one(name, aliases, t0, works, nb_min_w)
        r["ci"] = int(ci)
        out.append(r)
    return chunk_id, out, time.time() - t


def _alloc(counts: np.ndarray, n: int) -> np.ndarray:
    """largest-remainder allocation of n over years proportional to counts (never above a year's count)."""
    tot = counts.sum()
    q = counts * n / tot
    a = np.floor(q).astype(int)
    rem = n - a.sum()
    for j in np.argsort(-(q - a), kind="stable")[:rem]:
        a[j] += 1
    return np.minimum(a, counts)


def chunk_size(chunk_id: int, jobs: list) -> tuple[int, list, float]:
    t = time.time()
    out = []
    for ci, name, aliases, t0, pre, early, n_home in jobs:
        years = sorted({y for y, _ in early})
        by = {y: [w for w in early if w[0] == y] for y in years}
        cnts = np.array([len(by[y]) for y in years])
        alloc = _alloc(cnts, n_home)
        rs = []
        for r_ in range(N_DRAWS):
            rng = np.random.default_rng(SEED + int(ci) * 100 + r_)
            sub = []
            for y, a in zip(years, alloc):
                if a > 0:
                    idx = rng.choice(len(by[y]), a, replace=False)
                    sub += [by[y][i] for i in sorted(idx)]
            rs.append(_run_one(name, aliases, t0, pre + sub))
        rec = {"ci": int(ci), "n_draws": N_DRAWS}
        for k in KEYS + ["M", "deg_W1", "deg_W3"]:
            v = np.array([r.get(k, np.nan) for r in rs], float)
            rec[k] = float(np.nanmean(v)) if np.isfinite(v).any() else np.nan
            rec[f"{k}_ndef"] = int(np.isfinite(v).sum())
        out.append(rec)
    return chunk_id, out, time.time() - t


def run_pool(kind: str, jobs: list, workers: int, chunk: int, outdir: Path, nb_min_w: int = 2) -> dict:
    outdir.mkdir(parents=True, exist_ok=True)
    chunks = [jobs[i:i + chunk] for i in range(0, len(jobs), chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.parquet").exists()]
    logger.info(f"{kind}: {len(jobs)} jobs, {len(chunks)} chunks, todo {len(todo)}, workers {workers}")
    t0 = time.time()
    per = []
    with ProcessPoolExecutor(workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        if kind == "size":
            futs = [ex.submit(chunk_size, k, chunks[k]) for k in todo]
        else:
            futs = [ex.submit(chunk_plain, k, chunks[k], nb_min_w) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, out, dt = fu.result()
            pd.DataFrame(out).to_parquet(outdir / f"chunk_{k:05d}.parquet", index=False)
            per.append(dt / max(len(out), 1))
            if i % 20 == 0 or i == len(futs) - 1:
                el = time.time() - t0
                logger.info(f"{kind} {i+1}/{len(futs)} {el/60:.1f} min; {np.mean(per):.3f} s/job/worker; "
                            f"eta {el / (i+1) * (len(futs) - i - 1) / 60:.1f} min")
    return {"n_jobs": len(jobs), "wall_s": time.time() - t0, "s_per_job_worker": float(np.mean(per)) if per else None}


def read_parts(d: Path) -> pd.DataFrame:
    ps = sorted(d.glob("chunk_*.parquet"))
    return pd.concat([pd.read_parquet(p) for p in ps], ignore_index=True) if ps else pd.DataFrame({"ci": []})


# ----------------------------------------------------------------------------- jobs
def load_works() -> dict:
    em = pd.read_parquet(E8_DATA / "frame_matches_early/part_001.parquet", columns=["ci", "year", "vfield", "topics"])
    return {ci: (d.year.astype(int).to_numpy(), d.vfield.astype(int).to_numpy(), [tuple(t) for t in d.topics])
            for ci, d in em.groupby("ci")}


def aliases_of(r) -> list[str]:
    return [a for a in str(r.aliases_used).split("|") if a and a != "nan"]


def jobs_for(J: pd.DataFrame, W: dict, build: str) -> tuple[list, pd.DataFrame]:
    jobs, cov = [], []
    for r in J.itertuples():
        y, vf, tp = W.get(r.ci, (np.array([], int), np.array([], int), []))
        hcodes = {int(h) - 10 for h in str(r.home_list).split(";")}
        early = (y >= r.t0) & (y <= r.t0 + 2)
        ishome = np.isin(vf, list(hcodes))
        n_home = int((early & ishome).sum())
        cov.append({"ci": r.ci, "n_early_rows": int(early.sum()), "n_home": n_home,
                    "n_unlab_early": int((early & (vf == 0)).sum()),
                    "home_cov": n_home / early.sum() if early.sum() else np.nan})
        if build == "all":
            jobs.append((int(r.ci), str(r.name), aliases_of(r), int(r.t0), list(zip(y.tolist(), tp))))
        elif build == "home":
            jobs.append((int(r.ci), str(r.name), aliases_of(r), int(r.t0),
                         [(int(a), t) for a, t, h in zip(y, tp, ishome) if h]))
        elif build == "size" and n_home >= 5:
            pre = [(int(a), t) for a, t, e in zip(y, tp, early) if not e]
            ew = [(int(a), t) for a, t, e in zip(y, tp, early) if e]
            jobs.append((int(r.ci), str(r.name), aliases_of(r), int(r.t0), pre, ew, n_home))
    return jobs, pd.DataFrame(cov)


# ----------------------------------------------------------------------------- stages
def stage_test(J, W, workers: int) -> dict:
    """T2: ego_open on ALL-PAPERS input reproduces EXP8 ego_features for the 6 components (<= 1e-12)."""
    sub = J.sample(300, random_state=SEED)
    jobs, _ = jobs_for(sub, W, "all")
    outdir = DATA / "open_test"
    for p in outdir.glob("chunk_*.parquet"):
        p.unlink()
    tim = run_pool("test_all", jobs, workers, 10, outdir)
    got = read_parts(outdir).set_index("ci")
    ref = pd.read_parquet(E8_DATA / "ego_features.parquet").set_index("ci").loc[got.index]
    res = {"n": len(got), "timing": tim, "components": {}}
    ok_all = True
    for k in KEYS + ["M", "NOV", "deg_W1", "deg_W3"]:
        a, b = got[k].to_numpy(float), ref[k].to_numpy(float)
        nan_same = bool((np.isnan(a) == np.isnan(b)).all())
        m = ~np.isnan(a) & ~np.isnan(b)
        mad = float(np.max(np.abs(a[m] - b[m]))) if m.any() else 0.0
        ok = nan_same and mad <= 1e-12
        ok_all &= ok if k in KEYS else True
        res["components"][k] = {"nan_pattern_identical": nan_same, "max_abs_diff": mad, "pass": ok}
    res["PASS"] = ok_all
    jdump(res, RES / "t2_ego_open_reproduction.json")
    logger.info(f"T2 ego_open reproduction on {len(got)}: PASS={ok_all}; "
                + ", ".join(f"{k}:{v['max_abs_diff']:.1e}" for k, v in res["components"].items()))
    if not ok_all:
        raise RuntimeError("ego_open failed the 1e-12 reproduction test (fallback 3 applies)")
    return res


def stage_timing(J, W, workers: int) -> dict:
    sub = J.sample(200, random_state=SEED + 1)
    out = {}
    for build in ("home", "size"):
        jobs, _ = jobs_for(sub, W, build)
        d = DATA / f"open_timing_{build}"
        for p in d.glob("chunk_*.parquet"):
            p.unlink()
        out[build] = run_pool(build, jobs, workers, 5, d)
        n_full = {"home": 12499, "size": int(0.8 * 12499)}[build]
        out[build]["projected_min"] = out[build]["s_per_job_worker"] * n_full / workers / 60
    jdump(out, RES / "t4_open_timing.json")
    logger.info(f"timing: " + "; ".join(f"{b}: {v['s_per_job_worker']:.3f} s/job/worker -> "
                                          f"{v['projected_min']:.1f} min" for b, v in out.items()))
    return out


def zconst(df: pd.DataFrame, suffix: str) -> dict:
    return {k: {"mean": float(np.nanmean(df[f"{k}{suffix}"])), "sd": float(np.nanstd(df[f"{k}{suffix}"]))}
            for k in KEYS}


def open_score(df: pd.DataFrame, suffix: str, zc: dict) -> tuple[np.ndarray, np.ndarray]:
    Z = np.column_stack([s * (df[f"{k}{suffix}"].to_numpy(float) - zc[k]["mean"]) / zc[k]["sd"]
                         for k, s in OPEN_COMPONENTS])
    n = np.isfinite(Z).sum(1)
    with np.errstate(invalid="ignore"):
        o = np.where(n >= 4, np.nanmean(np.where(np.isfinite(Z), Z, np.nan), axis=1), np.nan)
    return o, n


def stage_assemble(J, W) -> None:
    _, cov = jobs_for(J, W, "none")
    home = read_parts(PARTS / "home").rename(columns={k: f"{k}_home" for k in KEYS + ["M", "deg_W1", "deg_W3", "NOV"]})
    size = read_parts(PARTS / "size")
    size = size.rename(columns={k: f"{k}_size" for k in KEYS + ["M", "deg_W1", "deg_W3"]})
    size = size[["ci"] + [c for c in size.columns if c.endswith("_size")]]
    O = J[["ci", "split", "group", "rgroup", "med_home"] + [f"{k}_all" for k in KEYS]].merge(cov, on="ci")
    O = O.merge(home[["ci"] + [c for c in home.columns if c.endswith("_home")]], on="ci", how="left")
    O = O.merge(size, on="ci", how="left")
    zc = {}
    for b in ("all", "home", "size"):
        zc[b] = zconst(O, f"_{b}")
        O[f"OPEN_{b}"], O[f"n_components_{b}"] = open_score(O, f"_{b}", zc[b])
    O.to_parquet(ROOT_OPEN, index=False)
    jdump({"z_constants": zc, "rule": ">= 4 of 6 components; z over all 12,499 frame concepts per build, ddof=0",
           "components": OPEN_COMPONENTS}, DATA / "open_zconst.json")
    diag = {"spearman_between_builds": {f"{a}~{b}": spearman(O[f"OPEN_{a}"], O[f"OPEN_{b}"])
                                        for a, b in (("all", "home"), ("all", "size"), ("home", "size"))},
            "component_spearman_all_vs_home": {k: spearman(O[f"{k}_all"], O[f"{k}_home"]) for k in KEYS},
            "coverage": {b: {"overall": float(O[f"OPEN_{b}"].notna().mean()),
                             "by_group": O.groupby("group")[f"OPEN_{b}"].apply(lambda s: float(s.notna().mean())).to_dict(),
                             "by_split": O.groupby("split")[f"OPEN_{b}"].apply(lambda s: float(s.notna().mean())).to_dict()}
                         for b in ("all", "home", "size")},
            "home_cov": {"median": float(O.home_cov.median()), "by_group": O.groupby("group").home_cov.median().to_dict()},
            "n_home_ge5": int((O.n_home >= 5).sum())}
    # selection check (fallback 5): B5 of covered vs uncovered HOME-ONLY concepts
    cov_m = O.OPEN_home.notna().to_numpy()
    diag["home_selection_check_B5_median"] = {
        c: {"covered": float(J.loc[cov_m, c].median()), "uncovered": float(J.loc[~cov_m, c].median())}
        for c in ("logvol", "growth_c", "offhome_share", "entropy", "reach")}
    jdump(diag, RES / "open_diagnostics.json")
    logger.info(f"OPEN coverage: " + ", ".join(f"{b} {v['overall']:.3f}" for b, v in diag["coverage"].items()))
    logger.info(f"OPEN Spearman between builds: {diag['spearman_between_builds']}")
    if diag["coverage"]["home"]["overall"] < 0.5:
        add_deviation("open_home_coverage", f"OPEN_home defined for {diag['coverage']['home']['overall']:.1%} < 50%",
                      "OPEN-on-axis for the HOME-ONLY build runs on the covered subset; selection check reported")


ROOT_OPEN = Path(__file__).resolve().parent / "open_features.parquet"


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--workers", type=int, default=24)
    a = ap.parse_args()
    J = stage_join() if a.stage in ("join", "all") or not (DATA / "joined.parquet").exists() \
        else pd.read_parquet(DATA / "joined.parquet")
    if a.stage == "join":
        return
    W = load_works()
    logger.info(f"works loaded for {len(W)} concepts")
    if a.stage in ("test", "all"):
        stage_test(J, W, a.workers)
    if a.stage in ("timing", "all"):
        stage_timing(J, W, a.workers)
    if a.stage in ("home", "all"):
        jobs, _ = jobs_for(J, W, "home")
        jdump(run_pool("home", jobs, a.workers, 40, PARTS / "home"), LOGS / "open_home_run.json")
    if a.stage in ("size", "all"):
        jobs, _ = jobs_for(J, W, "size")
        jdump(run_pool("size", jobs, a.workers, 10, PARTS / "size"), LOGS / "open_size_run.json")
    if a.stage in ("assemble", "all"):
        stage_assemble(J, W)
        update_status("S2_open")


if __name__ == "__main__":
    main()
