#!/usr/bin/env python3
"""S1: outcome-blind cohort candidate frame (years <= t0+2 only) + the 300 EXP5 control concepts.

Grounded yearly counts come from EXP5 scan/agg_counts.parquet under the frozen EXP5 grounding rule (TAG:
tagstate == 1; EXP5's grounding_report froze c_TAG, untagged rows are NOT counted). Rules:
  t0 = first year in 2000..2017 with >= 20 grounded works (EXP5 panel.onset with the upper bound moved 2014 -> 2017);
  keep t0 in {2015, 2016, 2017}; early volume (t0..t0+2) >= 30 (EXP5 realised threshold, frame_summary.json);
  ci not in EXP5 frame_concepts.csv;
  home = EXP5 frame.home_rule on the first 30 venue-labelled grounded works from t0 on, with the counts CAPPED at
         t0+2 (outcome-blind; EXP5 did not need the cap because its outcome years were sealed differently);
  diffuse_born / no_labels are dropped (EXP5 rule); newborn = EXP5 rule.
2017 onsets are FALLBACK candidates (role='fallback').
Writes data/cohort_candidates.csv, data/controls.csv, data/pre_counts.npz (grounded N/V 1995..2022 for candidates,
controls; years > t0+2 of candidates are zeroed so nothing downstream can read them)."""
from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, EXP5, GROUP_OF_FIELD, INPUTS, RES, jdump, setup_logger

logger = setup_logger("s1_candidates")
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
FIELD_IDS = list(range(11, 37))
T0_MIN, T0_MAX = 2015, 2017
EARLY_MIN = 30.0
HOME_N = 30


def yi(y: int) -> int:
    return y - Y0


def home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:
    """EXP5 frame.home_rule (verbatim logic) on V[NY, 27]; caller caps V at t0+2."""
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
    return res


def dense(ag: pd.DataFrame, cis: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    pos = {c: i for i, c in enumerate(cis)}
    sub = ag[ag.ci.isin(pos)]
    r = sub.ci.map(pos).to_numpy(np.int64)
    y = sub.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    r, y, n, vf = r[ok], y[ok], sub.n.to_numpy(np.float64)[ok], sub.vfield.to_numpy(np.int64)[ok]
    N = np.bincount(r * NY + y, weights=n, minlength=len(cis) * NY).reshape(len(cis), NY)
    V = np.bincount((r * NY + y) * 27 + vf, weights=n, minlength=len(cis) * NY * 27).reshape(len(cis), NY, 27)
    return N, V


@logger.catch(reraise=True)
def main() -> None:
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "qid", "name", "level"])
    logger.info(f"lexicon {len(lex)} concepts")
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[ag.tagstate == 1].groupby(["ci", "year", "vfield"], as_index=False)["n"].sum()
    logger.info(f"grounded (TAG) agg rows {len(ag)}")
    Nall = np.bincount(ag.ci.to_numpy(np.int64) * NY + (ag.year.to_numpy(np.int64) - Y0),
                       weights=ag.n.to_numpy(np.float64), minlength=len(lex) * NY).reshape(len(lex), NY)
    fr = pd.read_csv(EXP5 / "frame_concepts.csv")
    in_frame = set(fr.ci)
    rows, drops = [], {"in_exp5_frame": 0, "early_lt_30": 0, "diffuse_born": 0, "no_labels": 0}
    cand = np.nonzero((Nall[:, yi(2015):yi(2017) + 1] >= 20).any(1) & (Nall[:, yi(2000):yi(2014) + 1] < 20).all(1))[0]
    logger.info(f"prefilter: {len(cand)} concepts with first >=20 year in 2015-2017")
    Nc, Vc = dense(ag, cand)
    for k, ci in enumerate(cand):
        yc = Nc[k]
        t0 = next(y for y in range(2000, 2018) if yc[yi(y)] >= 20)
        if not (T0_MIN <= t0 <= T0_MAX):
            continue
        if ci in in_frame:
            drops["in_exp5_frame"] += 1
            continue
        early = float(yc[yi(t0):yi(t0 + 2) + 1].sum())
        if early < EARLY_MIN:
            drops["early_lt_30"] += 1
            continue
        V = Vc[k].copy()
        V[yi(t0 + 3):] = 0  # outcome-blind cap
        h = home_rule(V, t0)
        if h["status"] in ("diffuse_born", "no_labels"):
            drops[h["status"]] += 1
            continue
        newborn = all(yc[yi(t0 - j)] < 0.25 * yc[yi(t0 + 2)] for j in (1, 2, 3))
        early_lab = V[yi(t0):yi(t0 + 2) + 1, 1:27].sum()
        rows.append({"ci": int(ci), "concept_id": int(lex.concept_id.iat[ci]), "qid": lex.qid.iat[ci],
                     "name": lex["name"].iat[ci], "level": int(lex.level.iat[ci]), "t0": t0, "newborn": bool(newborn),
                     "home": ";".join(map(str, h["home"])), "n_home": h["n_home"], "weak_home": h["weak_home"],
                     "intersect40": h["intersect40"], "intersect25": h["intersect25"],
                     "home_top_share": h["top_share"], "group": GROUP_OF_FIELD[h["home"][0]],
                     "early_volume": early,
                     "label_coverage_early": float(early_lab / early) if early else math.nan,
                     "role": "primary" if t0 <= 2016 else "fallback"})
    cc = pd.DataFrame(rows)
    cc.to_csv(DATA / "cohort_candidates.csv", index=False)
    # 300 EXP5 control concepts, stratified by group, seed 7
    rng = np.random.default_rng(7)
    groups = sorted(fr.group.unique())
    per = {g: 300 // len(groups) + (1 if i < 300 % len(groups) else 0) for i, g in enumerate(groups)}
    ctl = []
    for g in groups:
        sub = fr[fr.group == g].sort_values("ci")
        ctl.append(sub.iloc[rng.choice(len(sub), size=min(per[g], len(sub)), replace=False)])
    ctl = pd.concat(ctl)[["ci", "concept_id", "name", "t0", "home", "group", "split"]].sort_values("ci")
    ctl.to_csv(DATA / "controls.csv", index=False)
    summ = {"n_prefilter": int(len(cand)), "drops": drops, "n_candidates": int(len(cc)),
            "by_t0": cc.t0.value_counts().sort_index().to_dict(),
            "by_t0_group": cc.groupby(["t0", "group"]).size().unstack(fill_value=0).to_dict(orient="index"),
            "n_controls": int(len(ctl)), "controls_by_group": ctl.group.value_counts().to_dict(),
            "newborn_share": float(cc.newborn.mean()), "weak_home": int(cc.weak_home.sum()),
            "intersect40": int(cc.intersect40.sum())}
    jdump(summ, RES / "s1_candidates_summary.json")
    logger.info(f"S1: {summ}")


if __name__ == "__main__":
    main()
