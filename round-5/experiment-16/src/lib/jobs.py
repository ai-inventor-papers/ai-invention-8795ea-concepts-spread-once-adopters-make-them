"""Job builders copied from EXP10 s7_ego.py (jobs_exp5 / jobs_cohort / home_codes_of) plus the body labels and a
compact HOME-build cache used by every S0-S2 stage.

A job is (ci, name, aliases, t0, rows, home_codes) with rows = [(year, topics tuple, vfield)] grounded early papers
t0-3..t0+2. HOME rows are rows whose vfield is in the concept's home codes (EXP10 definition)."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, EXP8, INPUTS, load_frame, read_parquet_parts

BODY_OF_SPLIT = {"DEV": "DEV", "HELDOUT": "OLDHO", "COHORT": "COH1014"}
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517"]
MIN_HOME = 10


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
    cf = pd.read_csv(DATA_IN / "cohort_candidates.csv")
    keep = set(pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci"]).ci)
    cf = cf[cf.ci.isin(keep)]
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["aliases_used"])
    if subset is not None:
        cf = cf[cf.ci.isin(subset)]
    em = pd.read_parquet(DATA_IN / "passC_early.parquet", columns=["ci", "year", "topics", "vfield", "tagstate"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    jobs = []
    for r in cf.itertuples():
        al = [a for a in str(lex.aliases_used.iat[r.ci]).split("|") if a and a not in ("nan", "None")]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def home_works(rows: list, home_codes: set[int]) -> list:
    return [(y, tp) for y, tp, v in rows if v in home_codes]


def build_home_cache(path: Path = DATA / "home_cache.pkl") -> dict:
    """{(frame, ci): dict(name, aliases, t0, body, works_home=[(year, topics)], n_home_early)} for ALL concepts."""
    if path.exists():
        return pickle.loads(path.read_bytes())
    fr = load_frame().set_index("ci")
    out = {}
    for j in jobs_exp5():
        ci, name, al, t0, rows, hc = j
        wh = home_works(rows, hc)
        out[("exp5", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body=BODY_OF_SPLIT[fr.at[ci, "split"]],
                                 works=wh, n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))
    for j in jobs_cohort():
        ci, name, al, t0, rows, hc = j
        wh = home_works(rows, hc)
        out[("cohort", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body="COH1517", works=wh,
                                   n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))
    path.write_bytes(pickle.dumps(out, protocol=5))
    return out


def uid_of(frame: str, ci: int) -> str:
    return f"{'E' if frame == 'exp5' else 'C'}{int(ci)}"
