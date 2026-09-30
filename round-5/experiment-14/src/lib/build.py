"""S1: build the Cheng measures (CONS, CONS_r, EMB, EMB_cos, SOC) per concept x year x build (HOME/ALL), the static
early traits, and the yearly grounded volume V(t).

Inputs (read-only): Exp11 data/frame_matches_long (EXP5 frame, t0-3..min(t0+10, 2022)), EXP10 data/passC_early
(2015-17 cohort, t0-3..t0+2, tagstate == 1 kept), EXP5 frame_concepts.csv, EXP10 analysis_cohort.parquet,
EXP5 scan/agg_counts.parquet (V), Exp11 counts_m.parquet (V check), EXP10 passC_pre_agg + sealed parts (cohort V).
Outputs: data/cheng_features.parquet, data/cheng_static.parquet, data/V_exp5.parquet, data/V_cohort.parquet,
results/s1_build.json (timing, NaN shares, V check)."""
from __future__ import annotations

import multiprocessing as mp
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

from common import (BODY_COHORT, DATA, EXP5, EXP10, EXP11, GROUP5, RES, SEED, add_deviation, body_of_split,
                    home_codes, jdump, n_workers, sha256_file)

MEAS = ["CONS", "CONS_r", "EMB", "EMB_cos", "SOC"]


def _init() -> None:
    import cheng
    cheng.init_context()


def run_chunk(k: int, jobs: list) -> tuple[int, list, float, list]:
    import cheng
    t = time.time()
    rows, errs = [], []
    for j in jobs:
        try:
            rows.extend(cheng.concept_measures(**j))
        except (ValueError, IndexError, KeyError, ZeroDivisionError) as e:
            errs.append((j["ci"], repr(e)[:300]))
    return k, rows, time.time() - t, errs


def load_flat(tab: pa.Table) -> dict:
    """Sort a (ci, year, vfield, topics, authors) table by (ci, year) and return flat numpy arrays + row ranges."""
    idx = pc.sort_indices(tab, sort_keys=[("ci", "ascending"), ("year", "ascending")])
    tab = tab.take(idx)
    ci = tab.column("ci").to_numpy().astype(np.int64)
    top = tab.column("topics").combine_chunks()
    aut = tab.column("authors").combine_chunks()
    out = {"ci": ci, "year": tab.column("year").to_numpy().astype(np.int64),
           "vfield": tab.column("vfield").to_numpy().astype(np.int64),
           "t_off": top.offsets.to_numpy().astype(np.int64), "tflat": top.values.to_numpy().astype(np.int64),
           "a_off": aut.offsets.to_numpy().astype(np.int64),
           "aflat": pc.fill_null(aut.values, -1).to_numpy().astype(np.int64)}
    u, start, cnt = np.unique(ci, return_index=True, return_counts=True)
    out["ranges"] = {int(c): (int(s), int(s + n)) for c, s, n in zip(u, start, cnt)}
    return out


def job_for(F: dict, ci: int, **kw) -> dict | None:
    if ci not in F["ranges"]:
        return None
    s, e = F["ranges"][ci]
    t0f, t1f = F["t_off"][s], F["t_off"][e]
    a0f, a1f = F["a_off"][s], F["a_off"][e]
    return dict(ci=ci, years=F["year"][s:e], vfield=F["vfield"][s:e], t_off=F["t_off"][s:e + 1] - t0f,
                tflat=F["tflat"][t0f:t1f], a_off=F["a_off"][s:e + 1] - a0f, aflat=F["aflat"][a0f:a1f], **kw)


def run_pool(jobs: list[dict], workers: int, logger, chunk: int = 40) -> tuple[pd.DataFrame, dict]:
    t = time.time()
    chunks = [jobs[i:i + chunk] for i in range(0, len(jobs), chunk)]
    rows, errs, cpu = [], [], 0.0
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_chunk, k, c) for k, c in enumerate(chunks)]
        for n_done, f in enumerate(as_completed(futs), 1):
            k, r, dt, e = f.result()
            rows.extend(r)
            errs.extend(e)
            cpu += dt
            if n_done % 25 == 0 or n_done == len(chunks):
                logger.info(f"  chunks {n_done}/{len(chunks)} {(time.time() - t) / 60:.1f} min errors={len(errs)}")
    df = pd.DataFrame(rows)
    timing = {"concepts": len(jobs), "wall_s": time.time() - t, "cpu_s_per_1000_concepts": 1000 * cpu / max(len(jobs), 1),
              "n_errors": len(errs), "errors": errs[:20]}
    return df, timing


# ----------------------------------------------------------------------------- V(t)
def build_V_exp5(fr: pd.DataFrame, logger) -> tuple[pd.DataFrame, dict]:
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "tagstate", "n"],
                         filters=[("tagstate", "==", 1)])
    ag = ag[ag.ci.isin(set(fr.ci))]
    V = ag.groupby(["ci", "year"], as_index=False).n.sum().rename(columns={"n": "V_agg"})
    del ag
    cm = pd.read_parquet(EXP11 / "data/counts_m.parquet")
    cm = cm[cm.ci.isin(set(fr.ci))].groupby(["ci", "year"], as_index=False).n.sum().rename(columns={"n": "V_m"})
    rng = np.random.default_rng(SEED)
    pick = rng.choice(fr.ci.to_numpy(), 200, replace=False)
    grid = pd.MultiIndex.from_product([pick, range(2000, 2023)], names=["ci", "year"]).to_frame(index=False)
    chk = grid.merge(V, on=["ci", "year"], how="left").merge(cm, on=["ci", "year"], how="left").fillna(0)
    exact = float((chk.V_agg == chk.V_m).mean())
    rel = float((np.abs(chk.V_agg - chk.V_m) / np.maximum(chk.V_m, 1)).mean())
    corr = float(np.corrcoef(chk.V_agg, chk.V_m)[0, 1])
    use = "agg_counts" if exact >= 0.99 else "counts_m"
    info = {"U5_cells": int(len(chk)), "U5_share_exact": exact, "U5_mean_rel_diff": rel, "U5_pearson": corr,
            "V_source": use, "sum_agg": float(chk.V_agg.sum()), "sum_m": float(chk.V_m.sum())}
    logger.info(f"U5 V check: {info}")
    if use == "counts_m":
        add_deviation("F3_V_source", f"agg_counts tagstate==1 matched counts_m exactly in {exact:.3f} of 200x23 "
                      f"cells (< 0.99): V(t) for EXP5 = Exp11 counts_m summed over vfield (Pass M TAG counts), "
                      f"fixed before any model. mean rel diff {rel:.4f}, r = {corr:.4f}")
    grid = pd.MultiIndex.from_product([fr.ci.to_numpy(), range(1995, 2023)], names=["ci", "year"]).to_frame(index=False)
    out = grid.merge(V, on=["ci", "year"], how="left").merge(cm, on=["ci", "year"], how="left").fillna(0)
    out["V"] = out.V_agg if use == "agg_counts" else out.V_m
    return out[["ci", "year", "V", "V_agg", "V_m"]], info


def build_V_cohort(coh: pd.DataFrame, logger) -> tuple[pd.DataFrame, dict]:
    cis = set(coh.ci)
    pre = pd.read_parquet(EXP10 / "data/passC_pre_agg.parquet")
    pre = pre[(pre.tagstate == 1) & pre.ci.isin(cis)]
    parts = sorted((EXP10 / "data/sealed/parts").glob("sealed_*.parquet"))
    logf = EXP10 / "logs/sealed_files.log"
    want = dict(l.split("\t") for l in logf.read_text().splitlines() if l.strip()) if logf.exists() else {}
    bad = [p.name for p in parts if p.name in want and sha256_file(p) != want[p.name]]
    missing = [n for n in want if not (EXP10 / "data/sealed/parts" / n).exists()]
    sealed_ok = bool(parts) and not bad and not missing
    info = {"n_sealed_parts": len(parts), "n_logged": len(want), "sha_mismatch": bad[:10], "missing": missing[:10],
            "sealed_ok": sealed_ok}
    logger.info(f"cohort sealed parts check: {info}")
    V = pre.groupby(["ci", "year"], as_index=False).n.sum()
    if sealed_ok:
        sl = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)
        sl = sl[(sl.tagstate == 1) & sl.ci.isin(cis)]
        V2 = sl.groupby(["ci", "year"], as_index=False).n.sum()
        V = pd.concat([V, V2]).groupby(["ci", "year"], as_index=False).n.sum()
    else:
        add_deviation("F4_cohort_V", "sealed parts missing or sha mismatch: cohort V(t0+3) not evaluable")
    m = coh[["ci", "t0"]].copy()
    rec = []
    for r in m.itertuples():
        d = V[V.ci == r.ci].set_index("year").n
        rec.append({"ci": int(r.ci), "V_t0p2": float(d.get(r.t0 + 2, 0.0)),
                    "V_t0p3": float(d.get(r.t0 + 3, 0.0)) if sealed_ok else float("nan"),
                    "V_t0": float(d.get(r.t0, 0.0)), "V_t0p1": float(d.get(r.t0 + 1, 0.0))})
    return pd.DataFrame(rec), info


# ----------------------------------------------------------------------------- static early traits
def static_table(feat: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:
    f = feat.merge(meta[["ci", "t0"]], on="ci")
    f = f[(f.year >= f.t0 + 1) & (f.year <= f.t0 + 2)]
    g = f.groupby(["ci", "build"])[MEAS].mean().unstack("build")
    g.columns = [f"{m}_early_{b.lower()}" for m, b in g.columns]
    g = g.reset_index()
    # early support diagnostics (HOME build)
    fh = f[f.build == "HOME"].groupby("ci").agg(n_papers_early_home=("n_papers", "sum"),
                                                deg_early_home=("n_topics", "mean"),
                                                n_authors_early_home=("n_authors", "sum")).reset_index()
    return meta[["ci", "body", "t0", "group", "group5"]].merge(g, on="ci", how="left").merge(fh, on="ci", how="left")


def run(logger, sample: int = 0, workers: int = 0) -> None:
    t_all = time.time()
    W = workers or n_workers()
    fr = pd.read_csv(EXP5 / "frame_concepts.csv")
    fr["body"] = fr.split.map(body_of_split)
    fr["group5"] = fr.group.map(GROUP5)
    coh = pd.read_parquet(EXP10 / "data/analysis_cohort.parquet", columns=["ci", "t0", "home", "name", "group"])
    coh["body"] = BODY_COHORT
    coh["group5"] = coh.group.map(GROUP5)
    sfx = f"_sample{sample}" if sample else ""
    if sample:
        fr = fr.sample(sample, random_state=SEED)
    # ---------------- EXP5 frame
    t = time.time()
    tab = pa.concat_tables([pq.read_table(p, columns=["ci", "year", "vfield", "topics", "authors"])
                            for p in sorted((EXP11 / "data/frame_matches_long").glob("part_*.parquet"))])
    tab = tab.filter(pc.is_in(tab.column("ci"), value_set=pa.array(fr.ci.astype(np.int32).to_numpy())))
    n_rows_exp5 = tab.num_rows
    F = load_flat(tab)
    del tab
    logger.info(f"EXP5 long rows {n_rows_exp5:,} for {len(F['ranges']):,} concepts loaded in {time.time() - t:.0f}s")
    jobs = []
    for r in fr.itertuples():
        al = [a for a in str(r.aliases_used).split("|") if a and a != "nan"]
        j = job_for(F, int(r.ci), name=str(r.name), aliases=al, t0=int(r.t0), y_lo=int(r.t0),
                    y_hi=int(min(r.t0 + 10, 2022)), home=home_codes(r.home))
        if j is not None:
            jobs.append(j)
    del F
    logger.info(f"EXP5 jobs {len(jobs)} (workers={W})")
    feat5, tim5 = run_pool(jobs, W, logger)
    del jobs
    # ---------------- 2015-17 cohort
    tim_c = {}
    featc = pd.DataFrame()
    if not sample:
        t = time.time()
        tab = pq.read_table(EXP10 / "data/passC_early.parquet", columns=["ci", "year", "vfield", "tagstate",
                                                                            "topics", "authors"])
        tab = tab.filter(pc.equal(tab.column("tagstate"), 1)).drop(["tagstate"])
        tab = tab.filter(pc.is_in(tab.column("ci"), value_set=pa.array(coh.ci.astype(np.int32).to_numpy())))
        n_rows_c = tab.num_rows
        Fc = load_flat(tab)
        del tab
        jobs = []
        for r in coh.itertuples():
            j = job_for(Fc, int(r.ci), name=str(r.name), aliases=[], t0=int(r.t0), y_lo=int(r.t0),
                        y_hi=int(r.t0 + 2), home=home_codes(r.home))
            if j is not None:
                jobs.append(j)
        logger.info(f"cohort rows {n_rows_c:,}, jobs {len(jobs)} loaded in {time.time() - t:.0f}s")
        featc, tim_c = run_pool(jobs, W, logger)
        tim_c["n_rows"] = n_rows_c
        add_deviation("cohort_aliases", "2015-17 cohort SELF topics use the concept name only (EXP10 "
                      "analysis_cohort has no aliases_used column); the share >= 0.20 rule applies unchanged")
    feat5["body_src"] = "EXP5"
    if len(featc):
        featc["body_src"] = "COHORT_2015_17"
    feat = pd.concat([feat5, featc], ignore_index=True)
    meta = pd.concat([fr[["ci", "body", "t0", "group", "group5"]], coh[["ci", "body", "t0", "group", "group5"]]],
                     ignore_index=True) if not sample else fr[["ci", "body", "t0", "group", "group5"]]
    st = static_table(feat, meta)
    # ---------------- diagnostics
    early = feat.merge(meta[["ci", "t0"]], on="ci")
    early = early[(early.year >= early.t0 + 1) & (early.year <= early.t0 + 2) & (early.build == "HOME")]
    ce = st["CONS_early_home"].to_numpy(float)
    diag = {"n_feature_rows": int(len(feat)), "n_static": int(len(st)),
            "nan_share_CONS_early_home": float(np.mean(~np.isfinite(ce))),
            "nan_share_CONS_yearly_home_early": float(early.CONS.isna().mean()),
            "share_exact_0_or_1_CONS_yearly_home_early": float(early.CONS.isin([0.0, 1.0]).mean()),
            "CONS_early_home_quantiles": np.nanquantile(ce, [0, .1, .25, .5, .75, .9, 1]).tolist()
            if np.isfinite(ce).any() else None,
            "nan_share_by_body": st.groupby("body").CONS_early_home.apply(lambda s: float(s.isna().mean())).to_dict(),
            "nan_share_SOC_early_home": float(st.SOC_early_home.isna().mean()),
            "nan_share_EMB_early_home": float(st.EMB_early_home.isna().mean())}
    logger.info(f"diagnostics: {diag}")
    info = {"timing_exp5": tim5, "timing_cohort": tim_c, "n_rows_exp5": n_rows_exp5, "diagnostics": diag}
    if sample:
        jdump(info, RES / f"s1_build{sfx}.json")
        feat.to_parquet(DATA / f"cheng_features{sfx}.parquet", index=False)
        st.to_parquet(DATA / f"cheng_static{sfx}.parquet", index=False)
        return
    V5, vinfo = build_V_exp5(fr, logger)
    V5.to_parquet(DATA / "V_exp5.parquet", index=False)
    Vc, cinfo = build_V_cohort(coh, logger)
    Vc.to_parquet(DATA / "V_cohort.parquet", index=False)
    info.update({"V_exp5": vinfo, "V_cohort": cinfo, "wall_min": (time.time() - t_all) / 60})
    feat.to_parquet(DATA / "cheng_features.parquet", index=False)
    st.to_parquet(DATA / "cheng_static.parquet", index=False)
    jdump(info, RES / "s1_build.json")
    if diag["nan_share_CONS_early_home"] > 0.40 or diag["share_exact_0_or_1_CONS_yearly_home_early"] > 0.30:
        add_deviation("F5_degenerate", f"CONS degenerate by the F5 rule: {diag}; primary kept frozen; pooled "
                      "2-year-window sensitivity and ALL build reported")
    logger.info(f"S1 done in {(time.time() - t_all) / 60:.1f} min")
