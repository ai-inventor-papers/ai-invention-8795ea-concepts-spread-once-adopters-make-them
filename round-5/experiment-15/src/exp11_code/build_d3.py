#!/usr/bin/env python3
"""Step 2: D3 off-home diffusion states for ALL 12,499 frame concepts from EXP5 agg_counts (tagstate == 1), with the
SAME code EXP7 used (lib/d3.panel_states, min_n = 2), validated cell-for-cell against the EXP7 state panels.

Writes data/d3_concept_year.parquet (OUTCOME file; it is only joined to the features after the seal):
  ci, year, entries (# off-home fields whose cum first reaches 2 in `year`), any_entry, at_risk (# off-home fields not
  yet entered by the end of year-1), cum_entries_prev, retained (# off-home fields in the retaining state), lost
  (# off-home fields entered but with no work in the last 3 years), and data/grounded_V.npz (G [C, NY, 27] counts)."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

import d3
import h2_exp6
from common import DATA, EXP5, NY, RES, RUN_ROOT, Y0, jdump, load_frame, setup_logger

EXP7 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_7"


def home_list(h) -> list[int]:
    import re
    return [int(float(x)) for x in re.split(r"[|;]", str(h)) if x and x != "nan"]


def grounded_V(ci: np.ndarray) -> np.ndarray:
    ag = pd.read_parquet(EXP5 / "scan" / "agg_counts.parquet", filters=[("tagstate", "==", 1)],
                         columns=["ci", "year", "vfield", "n"])
    pos = pd.Series(np.arange(len(ci)), index=ci)
    ag = ag[ag.ci.isin(pos.index)]
    r = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    r, y, n, vf = r[ok], y[ok], ag.n.to_numpy(np.float64)[ok], ag.vfield.to_numpy(np.int64)[ok]
    return np.bincount((r * NY + y) * 27 + vf, weights=n, minlength=len(ci) * NY * 27).reshape(len(ci), NY, 27)


def d3_counts(S: dict, home: np.ndarray) -> tuple[np.ndarray, ...]:
    """Per concept-year over OFF-HOME fields: entries (first year cum >= 2), at_risk (not entered by end of year-1),
    cum_entries_prev, retained (retaining state), lost (entered, no work in the last 3 years)."""
    off = ~home
    ent = S["entered"] & off[:, None, :]
    ent_prev = np.zeros_like(ent)
    ent_prev[:, 1:] = ent[:, :-1]
    return ((ent & ~ent_prev).sum(2), (off[:, None, :] & ~ent_prev).sum(2), ent_prev.sum(2),
            (S["retaining"] & off[:, None, :]).sum(2), (S["lost"] & off[:, None, :]).sum(2))


def main() -> None:
    logger = setup_logger("build_d3")
    t = time.time()
    fr = load_frame()
    assert len(fr) == 12499, len(fr)
    ci = fr.ci.to_numpy()
    G = grounded_V(ci)
    np.savez_compressed(DATA / "grounded_V.npz", G=G.astype(np.float32), ci=ci)
    home = np.zeros((len(fr), 26), bool)
    for i, h in enumerate(fr.home):
        for f in home_list(h):
            home[i, f - 11] = True
    S = d3.panel_states(G, home)
    off = ~home
    entries, at_risk, cum_prev, retained, lost = d3_counts(S, home)
    t0 = fr.t0.to_numpy()
    rows = []
    for i in range(len(fr)):
        ys = np.arange(t0[i] - 3, 2023)
        yi = ys - Y0
        rows.append(pd.DataFrame({"ci": ci[i], "year": ys.astype(np.int16), "entries": entries[i, yi].astype(np.int16),
                                  "at_risk": at_risk[i, yi].astype(np.int16),
                                  "cum_entries_prev": cum_prev[i, yi].astype(np.int16),
                                  "retained": retained[i, yi].astype(np.int16), "lost": lost[i, yi].astype(np.int16),
                                  "n_off_home_works": G[i, yi][:, 1:][:, off[i]].sum(1).astype(np.float32),
                                  "n_home_works_venue": G[i, yi][:, 1:][:, home[i]].sum(1).astype(np.float32)}))
    df = pd.concat(rows, ignore_index=True)
    df["any_entry"] = (df.entries > 0).astype(np.int8)
    df.to_parquet(DATA / "d3_concept_year.parquet", index=False)
    logger.info(f"D3 concept-year table {df.shape} in {time.time()-t:.0f}s")
    # ---- validation vs EXP7 state panels (T3) and vs h2_exp6.states
    sp = pd.concat([pd.read_parquet(EXP7 / "results" / f"state_panel_{s}.parquet") for s in ("dev", "heldout")])
    in_sp = set(sp.ci.unique())
    missing = [int(c) for c in ci if c not in in_sp]
    rng = np.random.default_rng(20260929)
    pick = rng.choice(np.array(sorted(in_sp)), size=200, replace=False)
    pos = pd.Series(np.arange(len(ci)), index=ci)
    n_cells = n_bad = n_bad_h2 = 0
    for c in pick:
        i = pos[c]
        s = sp[sp.ci == c]
        code = np.zeros((NY, 26), np.int8)
        code[S["entered"][i]] = 1
        code[S["retaining"][i]] = 2
        code[S["lost"][i] & S["offhome"][i][None, :]] = 3
        code[:, home[i]] = 4
        mine = code[s.year.to_numpy() - Y0, s.field.to_numpy() - 11]
        n_cells += len(s)
        n_bad += int((mine != s.state.to_numpy()).sum())
        st = h2_exp6.states(G[i], home_list(fr.home.iloc[i]))
        n_bad_h2 += int((st["entered"] != S["entered"][i]).sum() + (st["retaining"] != S["retaining"][i]).sum())
    out = {"n_frame": len(fr), "n_in_exp7_state_panels": len(in_sp & set(ci.tolist())), "n_missing_from_exp7": len(missing),
           "missing_by_split": fr[fr.ci.isin(missing)].split.value_counts().to_dict(),
           "validation_concepts": 200, "cells_compared": n_cells, "cells_mismatch": n_bad,
           "h2_exp6_states_mismatch_cells": n_bad_h2, "rows": int(len(df)), "seconds": time.time() - t}
    jdump(out, RES / "d3_validation.json")
    logger.info(f"T3 D3 validation: {out}")
    assert n_bad == 0 and n_bad_h2 == 0, "D3 states differ from EXP7 / h2_exp6"


if __name__ == "__main__":
    main()
