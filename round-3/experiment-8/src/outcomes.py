#!/usr/bin/env python3
"""STEP 4: one outcome table, one fold assignment (the EXP5 frame split), then the OUTCOME SEAL.

O1c  log(1 + N_grounded t0+6..t0+8) - log(1 + N_grounded t0..t0+2)                     (continuous; agg_counts TAG)
O1b  EXP5 concept_outcomes.O1 (sustained-share rule)                                       (binary)
O2r_m50 / O2r_m30  EXP5 exact hypergeometric rarefied venue-field richness t0+6..t0+8
O2r_resid  O2r_m50 - (a + b * logvol); a, b by OLS on DEV ONLY (frozen; EXP5's a = 4.790, b = -0.219 reported)
O3   EXP5 concept_outcomes.O3 (art_33 transience rule)                                     (binary)
O4   field- and year-normalised citation growth of the concept's early works (Pass B), see o4()
O5   external recognition (art_O7Dq4L02QnDN), O5_WW Wikipedia/Wikidata only; see o5()

Writes data/outcomes_dev.parquet (DEV rows) and data/outcomes_sealed.parquet (HELDOUT + COHORT rows; sha256 logged).
Nothing downstream of this script may read the sealed file before lib/seal.load_heldout() allows it."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP5, LOGS, NY, O5DIR, RES, Y0, add_deviation, jdump, load_frame, read_parquet_parts, \
    setup_logger, sha256_file

O5_ALL_SOURCES = {"mesh", "wikipedia_en", "wikidata", "acm_ccs", "msc", "pacs_physh", "gartner_hype_cycle",
                  "mit_tr10", "physics_world_boty", "science_boty", "nature_methods_moty"}   # NOT research_fronts
O5_WW_SOURCES = {"wikipedia_en", "wikidata"}
LATE_REQUIRES_GT_T0 = {"mesh", "acm_ccs", "msc", "pacs_physh"}
MIN_REF_CELL = 30


def load_o5_events(logger, fr: pd.DataFrame) -> pd.DataFrame:
    """Flatten the concept_recognition events of frame concepts (join on concept_id; fallback qid_resolved)."""
    cache = DATA / "o5_events.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    want = set(fr.concept_id.astype(np.int64).tolist())
    qid_of = dict(zip(fr.qid.astype(str), fr.concept_id.astype(np.int64)))
    rows, joined, by_qid = [], set(), 0
    parts = sorted((O5DIR / "full_data_out").glob("full_data_out_*.json"))
    for p in parts:
        d = json.loads(p.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for ex in ds["examples"]:
                inp = json.loads(ex["input"])
                cid = int(str(inp["openalex_id"]).lstrip("C"))
                if cid not in want:
                    q = inp.get("qid_resolved") or inp.get("qid")
                    if q in qid_of and qid_of[q] not in joined:
                        cid = int(qid_of[q]); by_qid += 1
                    else:
                        continue
                joined.add(cid)
                for ev in json.loads(ex["output"])["events"]:
                    rows.append((cid, ev["source"], ev["event_type"], ev.get("year"), bool(ev.get("year_usable")),
                                 ev.get("relation"), bool((ev.get("detail") or {}).get("mesh_baseline", False))))
        del d
    ev = pd.DataFrame(rows, columns=["concept_id", "source", "event_type", "year", "year_usable", "relation",
                                     "mesh_baseline"])
    ev["joined"] = True
    ev.to_parquet(cache, index=False)
    info = {"frame_concepts": len(want), "joined": len(joined), "join_rate": len(joined) / len(want),
            "joined_via_qid": by_qid, "events": len(ev)}
    jdump(info, RES / "o5_join.json")
    logger.info(f"O5 join: {info}")
    return ev


def o5(fr: pd.DataFrame, ev: pd.DataFrame, relations: tuple[str, ...], sources: set[str]) -> pd.DataFrame:
    """At-risk flag and outcome per concept. Qualifying: year_usable, relation in relations, source in sources,
    event types that DATE a recognition (taxonomy_in_version is a membership, not a date, and is excluded)."""
    q = ev[ev.year_usable & ev.relation.isin(relations) & ev.source.isin(sources)
           & (ev.event_type != "taxonomy_in_version") & ev.year.notna()].copy()
    base = ev[(ev.source == "mesh") & ev.mesh_baseline & ev.relation.isin(relations)].concept_id.unique() \
        if "mesh" in sources else np.array([], np.int64)
    q = q[~((q.source == "mesh") & q.mesh_baseline)]
    t0 = fr.set_index("concept_id").t0
    q["t0"] = q.concept_id.map(t0)
    q = q[q.t0.notna()]
    q["year"] = q.year.astype(int)
    prior = set(q[q.year < q.t0].concept_id)
    strict = q.source.isin(LATE_REQUIRES_GT_T0)
    hit_ok = ((q.year >= q.t0) & (q.year <= q.t0 + 8) & ~strict) | ((q.year > q.t0) & (q.year <= q.t0 + 8) & strict)
    pos = set(q[hit_ok].concept_id)
    joined = set(ev.concept_id)
    cid = fr.concept_id.astype(np.int64)
    at_risk = cid.isin(joined) & ~cid.isin(prior) & ~cid.isin(set(base))
    y = np.where(at_risk, cid.isin(pos).astype(float), np.nan)
    return pd.DataFrame({"concept_id": cid, "at_risk": at_risk.to_numpy(), "y": y})


def o4(logger, fr: pd.DataFrame) -> pd.DataFrame:
    """O4 = log((1 + C_late/6) / (1 + C_early/3)) - log((1 + E_late/6) / (1 + E_early/3)), where C_* are the
    citations received by the concept's early works (pub. year t0..t0+2) in citing years t0..t0+2 (early) and
    t0+3..t0+8 (late), and E_* the same sums of the ref-sample expectation for each early work's (pub year, venue
    field, offset d = pub year - t0) cell (year-level fallback for cells with < 30 reference works)."""
    ce = pd.read_parquet(DATA / "cites_early.parquet")
    em = read_parquet_parts(DATA / "frame_matches_early", columns=["ci", "year", "work_id", "vfield"])
    em = em.merge(fr[["ci", "t0"]], on="ci")
    em = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)].copy()
    em["d"] = em.year - em.t0
    rs = pd.read_parquet(DATA / "ref_sample.parquet", columns=["work_id", "year", "vfield"])
    cy = np.arange(2003, 2023)
    M = ce.pivot_table(index="work_id", columns="citing_year", values="n", aggfunc="sum", fill_value=0)
    M = M.reindex(columns=cy, fill_value=0)
    cum = np.concatenate([np.zeros((len(M), 1)), np.cumsum(M.to_numpy(float), 1)], 1)
    pos = pd.Series(np.arange(len(M)), index=M.index)

    def window_sum(ids: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:
        p = pos.reindex(ids).to_numpy()
        has = ~np.isnan(p)
        out = np.zeros(len(ids))
        pi = p[has].astype(int)
        lo = np.clip(a[has] - 2003, 0, 20)
        hi = np.clip(b[has] - 2003 + 1, 0, 20)
        out[has] = cum[pi, hi] - cum[pi, lo]
        return out
    em["c_early"] = window_sum(em.work_id.to_numpy(), em.t0.to_numpy(), em.t0.to_numpy() + 2)
    em["c_late"] = window_sum(em.work_id.to_numpy(), em.t0.to_numpy() + 3, em.t0.to_numpy() + 8)
    # ref-sample expectations per (pub year, vfield, d)
    exp_rows = []
    for d in (0, 1, 2):
        t0r = rs.year.to_numpy() - d
        rr = rs.assign(e=window_sum(rs.work_id.to_numpy(), t0r, t0r + 2),
                       l=window_sum(rs.work_id.to_numpy(), t0r + 3, t0r + 8))
        cell = rr.groupby(["year", "vfield"]).agg(n=("e", "size"), e=("e", "mean"), l=("l", "mean")).reset_index()
        yr = rr.groupby("year").agg(ey=("e", "mean"), ly=("l", "mean")).reset_index()
        cell = cell.merge(yr, on="year")
        small = cell.n < MIN_REF_CELL
        cell.loc[small, "e"] = cell.loc[small, "ey"]
        cell.loc[small, "l"] = cell.loc[small, "ly"]
        exp_rows.append(cell.assign(d=d)[["year", "vfield", "d", "e", "l", "n"]])
        yr_only = yr.rename(columns={"ey": "e_y", "ly": "l_y"}).assign(d=d)
        exp_rows[-1] = exp_rows[-1].merge(yr_only, on=["year", "d"], how="left")
    ex = pd.concat(exp_rows, ignore_index=True)
    ex.to_csv(RES / "o4_reference_expectations.csv", index=False)
    em = em.merge(ex[["year", "vfield", "d", "e", "l"]], on=["year", "vfield", "d"], how="left")
    yfb = ex.groupby(["year", "d"])[["e_y", "l_y"]].first().reset_index()
    em = em.merge(yfb, on=["year", "d"], how="left")
    em["e"] = em.e.fillna(em.e_y)
    em["l"] = em.l.fillna(em.l_y)
    g = em.groupby("ci").agg(C_early=("c_early", "sum"), C_late=("c_late", "sum"), E_early=("e", "sum"),
                             E_late=("l", "sum"), n_early_works=("work_id", "size"))
    g["O4_raw"] = np.log((1 + g.C_late / 6) / (1 + g.C_early / 3))
    g["O4_exp"] = np.log((1 + g.E_late / 6) / (1 + g.E_early / 3))
    g["O4"] = g.O4_raw - g.O4_exp
    logger.info(f"O4: {len(g)} concepts; median C_early {g.C_early.median():.0f}, C_late {g.C_late.median():.0f}; "
                f"O4 mean {g.O4.mean():.3f} sd {g.O4.std():.3f}")
    return g.reset_index()


def main() -> None:
    logger = setup_logger("outcomes")
    fr = load_frame()
    from build_features import load_arrays
    N, _ = load_arrays(fr)
    t0 = fr.t0.to_numpy()
    f = np.arange(len(fr))
    early = sum(N[f, t0 - Y0 + k] for k in range(3))
    late = sum(N[f, t0 - Y0 + k] for k in range(6, 9))
    out = fr[["ci", "concept_id", "t0", "group", "split", "unit"]].copy()
    out["O1c"] = np.log1p(late) - np.log1p(early)
    co = pd.read_csv(EXP5 / "concept_outcomes.csv")
    out = out.merge(co[["ci", "O1", "O3", "O2r_m30", "O2r_m50", "N_outcome"]].rename(columns={"O1": "O1b"}),
                    on="ci", how="left")
    basic = pd.read_csv(EXP5 / "concept_features_basic.csv", usecols=["ci", "logvol"])
    out = out.merge(basic, on="ci", how="left")
    dev = (out.split == "DEV") & out.O2r_m50.notna() & out.logvol.notna()
    A = np.c_[np.ones(dev.sum()), out.loc[dev, "logvol"]]
    a, b = np.linalg.lstsq(A, out.loc[dev, "O2r_m50"].to_numpy(), rcond=None)[0]
    spec5 = json.loads((EXP5 / "frozen_spec.json").read_text())
    out["O2r_resid"] = out.O2r_m50 - (a + b * out.logvol)
    # EXP5's own O2r_resid definition (O2r_m30 on log outcome-window volume), refitted on DEV: sensitivity only
    lnN = np.log(out.N_outcome.clip(lower=1))
    devN = dev & out.O2r_m30.notna() & out.N_outcome.notna()
    aN, bN = np.linalg.lstsq(np.c_[np.ones(devN.sum()), lnN[devN]], out.loc[devN, "O2r_m30"].to_numpy(), rcond=None)[0]
    out["O2r_resid_N"] = out.O2r_m30 - (aN + bN * lnN)
    jdump({"a_dev": a, "b_dev": b, "n_dev": int(dev.sum()), "O2r_resid_N_exp5_definition_dev_fit": {"a": aN, "b": bN},
           "note": "EXP5 defined O2r_resid = O2r_m30 - (a + b log N_outcome) (outcome-window volume); this plan's primary "
                   "O2r_resid = O2r_m50 - (a + b logvol) (early volume). EXP5's constants belong to the other formula, "
                   "so they are not a consistency check here; O2r_resid_N reproduces EXP5's definition as a sensitivity.",
           "exp5_constants": {
        k: v for k, v in spec5.items() if "resid" in k.lower() or k in ("a", "b")}}, RES / "o2r_resid_fit.json")
    logger.info(f"O2r_resid DEV fit: a={a:.3f} b={b:.3f} (EXP5: a=4.790, b=-0.219)")
    try:
        g = o4(logger, fr)
        out = out.merge(g[["ci", "O4", "O4_raw", "O4_exp", "C_early", "C_late"]], on="ci", how="left")
    except FileNotFoundError as e:
        logger.error(f"O4 dropped: {e}")
        add_deviation("O4_dropped", f"Pass B output missing: {e}")
        out["O4"] = np.nan
    ev = load_o5_events(logger, fr)
    for nm, rel, src in (("O5", ("same",), O5_ALL_SOURCES), ("O5_WW", ("same",), O5_WW_SOURCES),
                         ("O5_sens", ("same", "narrower"), O5_ALL_SOURCES),
                         ("O5_WW_sens", ("same", "narrower"), O5_WW_SOURCES)):
        r = o5(fr, ev, rel, src)
        out[nm] = r.y.to_numpy()
        out[f"{nm}_at_risk"] = r.at_risk.to_numpy()
    base_rates = out.groupby("unit").agg(**{f"{nm}_{s}": (nm, s) for nm in ("O5", "O5_WW", "O1b", "O3")
                                            for s in ("count", "sum")})
    jdump({"base_rates_by_unit": base_rates.reset_index().to_dict(orient="records"),
           "O5_by_t0": out.groupby("t0").agg(n=("O5", "count"), pos=("O5", "sum"), n_ww=("O5_WW", "count"),
                                             pos_ww=("O5_WW", "sum")).reset_index().to_dict(orient="records")},
          RES / "outcome_base_rates.json")
    cols = ["ci", "concept_id", "t0", "group", "split", "unit", "O1c", "O1b", "O2r_m50", "O2r_m30", "O2r_resid",
            "O2r_resid_N", "O3", "O4", "O5", "O5_WW", "O5_sens", "O5_WW_sens", "O5_at_risk", "O5_WW_at_risk", "N_outcome"]
    extra = [c for c in ("O4_raw", "O4_exp", "C_early", "C_late") if c in out.columns]
    out = out[cols + extra]
    out[out.split == "DEV"].to_parquet(DATA / "outcomes_dev.parquet", index=False)
    sealed = DATA / "outcomes_sealed.parquet"
    out[out.split != "DEV"].to_parquet(sealed, index=False)
    h = sha256_file(sealed)
    (LOGS / "outcome_seal.log").write_text(json.dumps({"sealed_file": "data/outcomes_sealed.parquet", "sha256": h,
                                                       "rows": int((out.split != "DEV").sum())}, indent=1))
    logger.info(f"outcomes: DEV {int((out.split == 'DEV').sum())} rows; sealed {int((out.split != 'DEV').sum())} "
                f"rows sha256 {h[:16]}")


if __name__ == "__main__":
    main()
