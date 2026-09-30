#!/usr/bin/env python3
"""STEP 5: the common outcome-blind frame S1.

  match      onset candidates on UNGROUNDED match counts (benchmark sampling frame) -> results/onset_candidates_match.csv
  grounded   onset candidates on grounded counts (precision-gate frame)             -> results/onset_candidates_grounded.csv
  build      frame_concepts.csv, episodes.csv, concept_outcomes.csv. Outcome columns are computed ONLY for DEV
             rows; held-out and cohort outcome columns stay blank until seal.py unseals them once.

Rules (art_33 definitions): t0 = first year 2000..2014 with >= 20 grounded works (all venues); keep
2003 <= t0 <= 2014 and early volume (t0..t0+2) >= 30; precision_c >= 0.8; home = fields with >= 40% of the
first 30 venue-labelled grounded works from t0 on (weak_home: top field >= 25%; else diffuse_born, dropped);
episode (c, j): j not in home and >= 2 grounded labelled works in j over t0..t0+2;
R = [share_out_j >= 0.5 * share_early_j AND n_out_cj >= 9] over t0+6..t0+8."""
from __future__ import annotations

import json
import math
import sys

import numpy as np
import pandas as pd

from common import (ART33, DEV_GROUPS, FIELD_IDS, GROUP_OF_FIELD, NY, RES, ROOT, SCAN, Y0, add_deviation, jdump,
                    setup_logger)
from panel import build_arrays, onset, onset_table, yi

logger = setup_logger("frame")
HOME_N = 30
EARLY_MIN = 30.0
P78_NAMES = None


def n_concepts() -> int:
    return len(pd.read_parquet(ROOT / "lexicon_v1.parquet", columns=["concept_id"]))


def year_totals() -> tuple[np.ndarray, np.ndarray]:
    z = np.load(SCAN / "year_field_totals.npz")
    return z["G"].astype(float), z["VF"].astype(float)


# ----------------------------------------------------------------------------- math (art_33 features.py, unchanged)
def rarefied_richness(counts, m: int) -> float:
    from scipy.special import gammaln
    n = np.asarray([c for c in counts if c > 0], dtype=float)
    N = n.sum()
    if N < m:
        return math.nan
    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)  # noqa: E731
    out = 0.0
    for nj in n:
        if N - nj < m:
            out += 1.0
        else:
            out += 1.0 - math.exp(lc(N - nj, m) - lc(N, m))
    return out


def rarefied_richness_frac(counts, m: int) -> float:
    """Rarefaction for (possibly fractional) counts: counts are rounded to integers first."""
    return rarefied_richness([int(round(c)) for c in counts], m)


def shannon(v) -> float:
    v = np.asarray([x for x in v if x > 0], float)
    if v.sum() == 0:
        return math.nan
    p = v / v.sum()
    return float(-(p * np.log(p)).sum())


# ----------------------------------------------------------------------------- home rule
def home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:
    """V: [NY, 27] grounded counts by venue-field code. First n_first labelled works from t0 on in year order;
    the boundary year contributes proportionally (expected composition of a hash-random tie break)."""
    acc = np.zeros(26)
    got = 0.0
    for y in range(t0, Y0 + NY):
        row = V[yi(y), 1:27].astype(float)
        tot = row.sum()
        if tot <= 0:
            continue
        need = n_first - got
        if tot <= need:
            acc += row
            got += tot
        else:
            acc += row * need / tot
            got += need
        if got >= n_first - 1e-9:
            break
    if got <= 0:
        return {"home": [], "status": "no_labels", "n_home": 0.0}
    sh = acc / got
    order = np.argsort(sh)[::-1]
    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]
    res = {"n_home": float(got), "top_share": float(sh[order[0]]), "second_share": float(sh[order[1]]),
           "intersect40": int(len(home) >= 2), "intersect25": int(sh[order[1]] >= 0.25), "weak_home": 0}
    if home:
        home = sorted(home, key=lambda f: -sh[f - 11])
        res.update(home=home, status="ok")
    elif sh[order[0]] >= 0.25:
        res.update(home=[FIELD_IDS[order[0]]], status="weak_home", weak_home=1)
    else:
        res.update(home=[], status="diffuse_born")
    if got < n_first:
        res["status_home_n"] = "thin_home"
    return res


def split_of(group: str, t0: int) -> str:
    if 2010 <= t0 <= 2014:
        return "COHORT"
    return "DEV" if group in DEV_GROUPS else "HELDOUT_" + group


# ----------------------------------------------------------------------------- episode + outcome functions
def episode_rows(ci: int, V: np.ndarray, t0: int, home: list[int]) -> list[dict]:
    """Episode covariates (no outcome). V = grounded [NY, 27]."""
    early = V[yi(t0):yi(t0 + 2) + 1, 1:27]
    ne = early.sum(0)
    lab = ne.sum()
    nA = V[yi(t0):yi(t0 + 1) + 1, 1:27].sum(0)
    nB = V[yi(t0 + 2), 1:27]
    rows = []
    for k in range(26):
        j = FIELD_IDS[k]
        if j in home or ne[k] < 2 - 1e-9:
            continue
        rows.append({"ci": ci, "field": j, "n_early": float(ne[k]), "n_A": float(nA[k]), "n_B": float(nB[k]),
                     "share_early": float(ne[k] / lab) if lab else math.nan,
                     "growth_j": math.log((nB[k] + 1) / (nA[k] / 2 + 1))})
    return rows


def episode_outcomes(V: np.ndarray, t0: int, field: int, share_early: float) -> dict:
    out = V[yi(t0 + 6):yi(t0 + 8) + 1, 1:27].sum(0)
    lab = out.sum()
    n_out = float(out[field - 11])
    s_out = n_out / lab if lab else math.nan
    R = int(s_out >= 0.5 * share_early and n_out >= 9 - 1e-9) if np.isfinite(s_out) else math.nan
    return {"n_out": n_out, "share_out": s_out, "R": R, "R_abs1": int(n_out >= 1 - 1e-9),
            "R_abs2": int(n_out >= 2 - 1e-9), "R_abs3": int(n_out >= 3 - 1e-9), "lab_out": float(lab)}


def concept_outcomes(N: np.ndarray, V: np.ndarray, G: np.ndarray, t0: int) -> dict:
    """art_33 features.outcomes() on grounded yearly counts; O2r over ALL grounded labelled works t0+6..t0+8."""
    sh = lambda y: N[yi(y)] / G[yi(y)]  # noqa: E731
    o1 = int(np.mean([sh(y) for y in range(t0 + 6, t0 + 9)]) >= sh(t0 + 5))
    seq = [N[yi(y)] for y in range(t0, t0 + 9)]
    peak_y = t0 + int(np.argmax(seq))
    late = np.mean([N[yi(t0 + 7)], N[yi(t0 + 8)]])
    o3 = int(t0 + 3 <= peak_y <= t0 + 8 and max(seq) / max(late, 1e-9) >= 2)
    counts = V[yi(t0 + 6):yi(t0 + 8) + 1, 1:27].sum(0)
    Nout = float(counts.sum())
    return {"O1": o1, "O3": o3, "peak_year": peak_y, "N_outcome": Nout,
            "O2r_m30": rarefied_richness_frac(counts, 30), "O2r_m50": rarefied_richness_frac(counts, 50),
            "O2_raw": int((counts >= 15).sum())}


# ----------------------------------------------------------------------------- commands
def cmd_match() -> None:
    A = build_arrays("match", n_concepts())
    ot = onset_table(A["N"])
    ot.to_csv(RES / "onset_candidates_match.csv", index=False)
    logger.info(f"match onset candidates: {len(ot)} (t0 2003-2014, early >= 30)")


def cmd_grounded() -> None:
    A = build_arrays("grounded", n_concepts())
    ot = onset_table(A["N"])
    ot.to_csv(RES / "onset_candidates_grounded.csv", index=False)
    logger.info(f"grounded onset candidates: {len(ot)}")


def p78_names() -> set[str]:
    sys.path.insert(0, str(ART33))
    names = set()
    try:
        oc = pd.read_csv(ART33 / "outcomes.csv")
        names |= {str(x).lower() for x in oc.concept}
    except (FileNotFoundError, KeyError, pd.errors.ParserError) as e:
        logger.warning(f"P78 names not loadable: {e!r}")
    return names


def build(early_min: float = EARLY_MIN, allow_weak: bool = True) -> tuple[pd.DataFrame, pd.DataFrame]:
    lex = pd.read_parquet(ROOT / "lexicon_v1.parquet", columns=["concept_id", "qid", "name", "level", "aliases_used"])
    A = build_arrays("grounded", len(lex))
    N, V = A["N"], A["V"]
    G, _ = year_totals()
    prec = pd.read_csv(ROOT / "grounding_precision.csv")
    prec_map = prec.set_index("ci")
    ot = onset_table(N, min_early=early_min)
    p78 = p78_names()
    crows, erows, drops = [], [], {"precision": 0, "diffuse_born": 0, "no_labels": 0, "weak_home_excluded": 0,
                                   "no_precision_label": 0}
    for r in ot.itertuples():
        ci, t0 = r.ci, r.t0
        if ci not in prec_map.index or not np.isfinite(prec_map.at[ci, "precision_c"]):
            drops["no_precision_label"] += 1
            continue
        pc_ = float(prec_map.at[ci, "precision_c"])
        if pc_ < 0.8:
            drops["precision"] += 1
            continue
        h = home_rule(V[ci], t0)
        if h["status"] in ("diffuse_born", "no_labels"):
            drops[h["status"]] += 1
            continue
        if h["status"] == "weak_home" and not allow_weak:
            drops["weak_home_excluded"] += 1
            continue
        home = h["home"]
        group = GROUP_OF_FIELD[home[0]]
        early_lab = V[ci, yi(t0):yi(t0 + 2) + 1, 1:27].sum()
        early_all = N[ci, yi(t0):yi(t0 + 2) + 1].sum()
        m_early = A["M"][ci, yi(t0):yi(t0 + 2) + 1].sum()
        t1_early = A["T1"][ci, yi(t0):yi(t0 + 2) + 1].sum()
        nm = lex["name"].iat[ci]
        crows.append({"ci": ci, "concept_id": int(lex.concept_id.iat[ci]), "qid": lex.qid.iat[ci], "name": nm,
                      "level": int(lex.level.iat[ci]), "aliases_used": lex.aliases_used.iat[ci], "t0": t0,
                      "newborn": bool(r.newborn), "home": ";".join(map(str, home)), "n_home": h["n_home"],
                      "weak_home": h["weak_home"], "intersect40": h["intersect40"], "intersect25": h["intersect25"],
                      "home_top_share": h["top_share"], "group": group, "split": split_of(group, t0),
                      "precision_c": pc_, "n_labelled_prec": prec_map.at[ci, "n_labelled_prec"],
                      "precision_source": prec_map.at[ci, "precision_source"],
                      "label_coverage_early": float(early_lab / early_all) if early_all else math.nan,
                      "tag_coverage": float(t1_early / m_early) if m_early else math.nan,
                      "early_volume": float(early_all), "in_P78": int(nm.lower() in p78)})
        for e in episode_rows(ci, V[ci], t0, home):
            erows.append(e)
    fc = pd.DataFrame(crows)
    ep = pd.DataFrame(erows).merge(fc[["ci", "concept_id", "name", "t0", "group", "split", "home"]], on="ci")
    jdump({"early_min": early_min, "allow_weak": allow_weak, "onset_candidates": len(ot), "drops": drops,
           "n_concepts": len(fc), "n_episodes": len(ep)}, RES / f"frame_build_em{int(early_min)}_w{int(allow_weak)}.json")
    return fc, ep


def cmd_build() -> None:
    # relaxation ladder (outcome-blind, stops as soon as targets are met); weak_home is admitted by default
    # as in the plan's home rule, so the ladder starts from the plan's own primary definition.
    fc, ep = build(EARLY_MIN, True)
    ladder = [{"early_min": 30, "weak_home": True, "n_concepts": len(fc), "n_episodes": len(ep)}]
    if len(fc) < 400 or len(ep) < 4000:
        fc, ep = build(20.0, True)
        ladder.append({"early_min": 20, "weak_home": True, "n_concepts": len(fc), "n_episodes": len(ep)})
        add_deviation("frame_relaxation", f"targets not met at early>=30; relaxed to early volume >= 20: {ladder}")
    G, _ = year_totals()
    lexN = n_concepts()
    A = build_arrays("grounded", lexN)
    N, V = A["N"], A["V"]
    # DEV outcomes only (held-out / cohort stay sealed)
    dev = fc.split == "DEV"
    co = []
    for r in fc.itertuples():
        base = {"ci": r.ci, "concept_id": r.concept_id, "split": r.split}
        if r.split == "DEV":
            base.update(concept_outcomes(N[r.ci], V[r.ci], G, r.t0))
        co.append(base)
    co = pd.DataFrame(co)
    outs = []
    t0m = fc.set_index("ci").t0
    for r in ep.itertuples():
        if r.split == "DEV":
            outs.append(episode_outcomes(V[r.ci], int(t0m[r.ci]), r.field, r.share_early))
        else:
            outs.append({})
    ep = pd.concat([ep.reset_index(drop=True), pd.DataFrame(outs)], axis=1)
    fc.to_csv(ROOT / "frame_concepts.csv", index=False)
    ep.to_csv(ROOT / "episodes.csv", index=False)
    co.to_csv(ROOT / "concept_outcomes.csv", index=False)
    summ = {"ladder": ladder, "n_concepts": len(fc), "n_episodes": len(ep),
            "by_split": fc.split.value_counts().to_dict(), "episodes_by_split": ep.split.value_counts().to_dict(),
            "by_group": fc.group.value_counts().to_dict(), "newborn_share": float(fc.newborn.mean()),
            "weak_home": int(fc.weak_home.sum()), "intersect40": int(fc.intersect40.sum()),
            "dev_R_rate": float(ep.loc[ep.split == "DEV", "R"].mean()) if dev.any() else None}
    jdump(summ, RES / "frame_summary.json")
    logger.info(f"frame: {summ}")


if __name__ == "__main__":
    {"match": cmd_match, "grounded": cmd_grounded, "build": cmd_build}[sys.argv[1]]()
