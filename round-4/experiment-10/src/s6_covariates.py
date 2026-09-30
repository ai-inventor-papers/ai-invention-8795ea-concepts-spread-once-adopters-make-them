#!/usr/bin/env python3
"""S6 + S7(basic): pre-onset footprint and the basic early-window covariates for BOTH frames (EXP5 12,499; cohort).

Every quantity uses years < t0 (footprint) or t0-3..t0+2 (features) only. Grounded yearly counts: EXP5
scan/agg_counts.parquet under TAG (tagstate == 1), cohort years > t0+2 zeroed before anything is computed.
  footprint   fp_logN = log1p(grounded papers t0-10..t0-1); fp_nfields = # venue fields with >= 1 grounded paper
              before t0 (1995..t0-1); fp_reemerge = 1 if any year 1995..t0-1 has >= 25% of the t0+2 count;
              fp_wiki_pre = 1 if art_O7Dq4L02QnDN has a wikipedia_en creation event (year_usable, relation 'same')
              with year < t0; fp_ext_pre (sensitivity) = the same for any dated source except research fronts;
              newborn (EXP5 rule); level (legacy level 2-5)
  B5          logvol, growth_c, offhome_share, entropy, reach (EXP5 features.b5, same code)
  FR          CONTACT_REACH, RETAINED_REACH, RETENTION_RATIO_early (EXP8 build_features.stage_basic, same code)
  E           n_authors_early = log1p(# distinct author ids on grounded papers t0..t0+2)
  coverage    label_coverage_early = venue-labelled share of grounded early papers
Writes data/covariates_exp5.parquet, data/covariates_cohort.parquet, data/o5_events_all.parquet, results/s6_checks.json"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP5, EXP8, INPUTS, O5DIR, RES, jdump, load_frame, setup_logger

logger = setup_logger("s6_covariates")
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
EXT_SOURCES = {"mesh", "wikipedia_en", "wikidata", "acm_ccs", "msc", "pacs_physh", "gartner_hype_cycle", "mit_tr10",
               "physics_world_boty", "science_boty", "nature_methods_moty"}


def yi(y: int) -> int:
    return y - Y0


def shannon(v) -> float:
    v = np.asarray([x for x in v if x > 0], float)
    if v.sum() == 0:
        return math.nan
    p = v / v.sum()
    return float(-(p * np.log(p)).sum())


def b5(N: np.ndarray, V: np.ndarray, t0: int, home_idx: list[int], end_off: int = 2) -> dict:
    """EXP5 features.b5 (verbatim)."""
    ys = slice(yi(t0), yi(t0 + end_off) + 1)
    lab = V[ys, 1:27].sum(0)
    labt = lab.sum()
    vol = N[ys].sum()
    return {"logvol": math.log1p(vol), "growth_c": math.log((N[yi(t0 + end_off)] + 1) / (N[yi(t0)] + 1)),
            "offhome_share": float(sum(lab[k] for k in range(26) if k not in home_idx) / labt) if labt else math.nan,
            "entropy": shannon(lab), "reach": int((lab >= 2 - 1e-9).sum())}


def fr_block(V: np.ndarray, t0: int, home: list[int]) -> dict:
    """EXP8 stage_basic CONTACT_REACH / RETAINED_REACH / RETENTION_RATIO_early (window t0..t0+2)."""
    off = np.ones(26, bool)
    for h in home:
        off[h - 11] = False
    x = V[yi(t0):yi(t0 + 2) + 1, 1:]
    contact = int(((x.sum(0) >= 1) & off).sum())
    retained = ((x >= 2).sum(0) >= 2) & off
    rr = int(retained.sum())
    return {"CONTACT_REACH": contact, "RETAINED_REACH": rr, "RETENTION_RATIO_early": rr / max(contact, 1),
            "RETENTION_RATIO_missing": int(contact == 0)}


def arrays(cis: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(cis.tolist()))]
    pos = pd.Series(np.arange(len(cis)), index=cis)
    f = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    f, y, vf, n = f[ok], y[ok], ag.vfield.to_numpy(np.int64)[ok], ag.n.to_numpy(np.float64)[ok]
    N = np.bincount(f * NY + y, weights=n, minlength=len(cis) * NY).reshape(len(cis), NY)
    V = np.bincount((f * NY + y) * 27 + vf, weights=n, minlength=len(cis) * NY * 27).reshape(len(cis), NY, 27)
    return N, V


def o5_events(concept_ids: set[int]) -> pd.DataFrame:
    cache = DATA / "o5_events_all.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    rows = []
    for p in sorted((O5DIR / "full_data_out").glob("full_data_out_*.json")):
        d = json.loads(p.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for ex in ds["examples"]:
                inp = json.loads(ex["input"])
                cid = int(str(inp["openalex_id"]).lstrip("C"))
                if cid not in concept_ids:
                    continue
                for ev in json.loads(ex["output"])["events"]:
                    rows.append((cid, ev["source"], ev["event_type"], ev.get("year"), bool(ev.get("year_usable")),
                                 ev.get("relation")))
        del d
    ev = pd.DataFrame(rows, columns=["concept_id", "source", "event_type", "year", "year_usable", "relation"])
    ev.to_parquet(cache, index=False)
    return ev


def frame_covariates(fr: pd.DataFrame, cap_t0p2: bool, ev: pd.DataFrame, lex: pd.DataFrame,
                     authors: dict) -> pd.DataFrame:
    cis = fr.ci.to_numpy()
    N, V = arrays(cis)
    if cap_t0p2:  # cohort: nothing after t0+2 may enter a covariate
        for f, t0 in enumerate(fr.t0.to_numpy()):
            N[f, yi(t0 + 3):] = 0
            V[f, yi(t0 + 3):] = 0
    wiki = ev[(ev.source == "wikipedia_en") & ev.year_usable & (ev.relation == "same") & ev.year.notna()]
    wiki_first = wiki.groupby("concept_id").year.min()
    ext = ev[ev.source.isin(EXT_SOURCES) & ev.year_usable & (ev.relation == "same") & ev.year.notna()
             & (ev.event_type != "taxonomy_in_version")]
    ext_first = ext.groupby("concept_id").year.min()
    joined = set(ev.concept_id)
    rows = []
    for f, r in enumerate(fr.itertuples()):
        t0 = int(r.t0)
        home = [int(float(x)) for x in str(r.home).split(";") if x and x != "nan"]
        home_idx = [h - 11 for h in home]
        n = N[f]
        pre = V[f, :yi(t0), 1:27].sum(0)
        cid = int(lex.concept_id.iat[r.ci])
        rec = {"ci": int(r.ci), "fp_logN": math.log1p(n[max(yi(t0 - 10), 0):yi(t0)].sum()),
               "fp_nfields": int((pre >= 1).sum()),
               "fp_reemerge": int(any(n[yi(y)] >= 0.25 * n[yi(t0 + 2)] for y in range(Y0, t0))),
               "fp_wiki_pre": int(cid in wiki_first.index and wiki_first[cid] < t0),
               "fp_ext_pre": int(cid in ext_first.index and ext_first[cid] < t0),
               "o5_joined": int(cid in joined),
               "newborn": int(all(n[yi(t0 - k)] < 0.25 * n[yi(t0 + 2)] for k in (1, 2, 3))),
               "level": int(lex.level.iat[r.ci])}
        rec.update(b5(n, V[f], t0, home_idx))
        rec.update(fr_block(V[f], t0, home))
        early = n[yi(t0):yi(t0 + 2) + 1].sum()
        rec["label_coverage_early"] = float(V[f, yi(t0):yi(t0 + 2) + 1, 1:27].sum() / early) if early else math.nan
        a = authors.get(int(r.ci))
        rec["n_authors_early"] = math.log1p(len(a)) if a is not None else math.nan
        rows.append(rec)
    return pd.DataFrame(rows)


@logger.catch(reraise=True)
def main() -> None:
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "level"])
    fr5 = load_frame()
    cc = pd.read_csv(DATA / "cohort_candidates.csv")
    ids = set(lex.concept_id.iloc[fr5.ci].astype(np.int64)) | set(lex.concept_id.iloc[cc.ci].astype(np.int64))
    ev = o5_events(ids)
    logger.info(f"O5 events: {len(ev)} for {ev.concept_id.nunique()} concepts")
    frames = sys.argv[1:] or ["exp5", "cohort"]
    if "cohort" in frames:
        # authors: EXP5 from EXP8 features (identical definition); cohort from Pass C early rows
        em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "tagstate", "authors"])
        em = em[em.tagstate == 1].merge(cc[["ci", "t0"]], on="ci")
        em = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)]
        auth_c = {int(ci): {a for lst in g.authors for a in lst} for ci, g in em.groupby("ci")}
        cov_c = frame_covariates(cc, True, ev, lex, auth_c)
        cov_c.to_parquet(DATA / "covariates_cohort.parquet", index=False)
        summ_c = {"n_cohort": len(cov_c), "o5_join_rate_cohort": float(cov_c.o5_joined.mean()),
                  "fp_means_cohort": cov_c[["fp_logN", "fp_nfields", "fp_reemerge", "fp_wiki_pre",
                                            "newborn"]].mean().to_dict()}
        jdump(summ_c, RES / "s6_checks_cohort.json")
        logger.info(f"S6 cohort: {summ_c}")
    if "exp5" not in frames:
        return
    cov5 = frame_covariates(fr5, False, ev, lex, {})
    fb = pd.read_parquet(EXP8 / "data/features_basic.parquet",
                         columns=["ci", "n_authors_early", "CONTACT_REACH", "RETENTION_RATIO_early", "logvol",
                                  "growth_c", "offhome_share", "entropy", "reach"])
    chk = cov5.merge(fb, on="ci", suffixes=("", "_exp8"))
    checks = {}
    for c in ["CONTACT_REACH", "RETENTION_RATIO_early", "logvol", "growth_c", "offhome_share", "entropy", "reach"]:
        a, b = chk[c].to_numpy(float), chk[f"{c}_exp8"].to_numpy(float)
        checks[c] = float(np.nanmax(np.abs(a - b)))
    cov5 = cov5.drop(columns=["n_authors_early"]).merge(fb[["ci", "n_authors_early"]], on="ci", how="left")
    cov5.to_parquet(DATA / "covariates_exp5.parquet", index=False)
    summ = {"reproduction_max_abs_diff_vs_exp8": checks, "n_exp5": len(cov5),
            "o5_join_rate_exp5": float(cov5.o5_joined.mean()),
            "fp_means_exp5": cov5[["fp_logN", "fp_nfields", "fp_reemerge", "fp_wiki_pre", "newborn"]].mean().to_dict()}
    jdump(summ, RES / "s6_checks.json")
    logger.info(f"S6: {summ}")


if __name__ == "__main__":
    main()
