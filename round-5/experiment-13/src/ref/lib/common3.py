"""Shared helpers: data loaders for the scan outputs, rarefaction, entropy, content lemmas."""
from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from functools import lru_cache

import numpy as np
import pandas as pd
from scipy.special import gammaln

from config import PANEL, RES, ROOT, SLICES

SCAN = ROOT / "scan"
Y0 = 1995  # first year of the scan's background arrays


# ----------------------------------------------------------------------------- math
def lgC(n: float, k: float) -> float:
    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)


def rarefy(counts, m: int) -> float:
    """Exact hypergeometric rarefied richness E[S_m] = sum_j 1 - C(N-n_j,m)/C(N,m); NaN if N < m."""
    c = np.asarray([x for x in counts if x > 0], dtype=float)
    N = c.sum()
    if N < m:
        return float("nan")
    tot = 0.0
    for nj in c:
        if N - nj < m:
            tot += 1.0
        else:
            tot += 1.0 - math.exp(lgC(N - nj, m) - lgC(N, m))
    return float(tot)


def shannon(counts) -> float:
    c = np.asarray([x for x in counts if x > 0], dtype=float)
    if c.sum() == 0:
        return float("nan")
    p = c / c.sum()
    return float(-(p * np.log(p)).sum())


# ----------------------------------------------------------------------------- loaders
def load_api_yearly() -> tuple[dict[str, dict[int, int]], dict[int, int]]:
    d = json.loads((RES / "yearly_counts_api.json").read_text())
    conc = {k: {int(y): int(c) for y, c in v.items()} for k, v in d["concepts"].items()}
    G = {int(y): int(c) for y, c in d["G"].items()}
    return conc, G


def load_matches() -> pd.DataFrame:
    """One row per (title-matched base work, concept)."""
    rows = []
    single = SCAN / "matches.jsonl"  # written by scan_snapshot.py; split into scan/matches/matches_*.jsonl (<100 MB)
    files = [single] if single.exists() else sorted((SCAN / "matches").glob("matches_*.jsonl"))
    for fp in files:
        with fp.open() as f:
            for ln in f:
                if not ln.strip():
                    continue
                m = json.loads(ln)
                if not m["b"] or not (1990 <= m["y"] <= 2030):
                    continue
                for c in m["c"]:
                    rows.append((c, m["y"], m["s"], tuple(m["t"]), m["ti"]))
    df = pd.DataFrame(rows, columns=["ci", "year", "source", "topics", "title"])
    df["concept"] = df.ci.map(lambda i: PANEL[i][0])
    return df


def load_scan_aggregates():
    """(topic_ids, G_snap[year], Gt_snap[year], bg[year, topic], pair count dense arrays per slice)."""
    z = np.load(SCAN / "ckpt.npz")
    tids = json.loads((SCAN / "topic_ids.json").read_text())
    nt = len(tids)
    pairs = []
    for s in range(len(SLICES)):
        pairs.append((z[f"pk{s}"], z[f"pc{s}"]))
    years = list(range(Y0, Y0 + z["G"].shape[0]))
    G = dict(zip(years, z["G"].tolist()))
    Gt = dict(zip(years, z["Gt"].tolist()))
    return tids, G, Gt, z["bg"], pairs, nt, years


def load_source_field() -> dict[int, int | None]:
    sf = pd.read_parquet(RES / "source_field.parquet")
    return {int(s): (int(f) if pd.notna(f) else None) for s, f in zip(sf.source, sf.field)}


# ----------------------------------------------------------------------------- lemmas for self-topic detection
_STOP = set("a an and are as at be but by for if in into is it no not of on or such that the their then there these "
            "they this to was will with its via from using based".split())
_TOK = re.compile(r"[^\W_]+", re.UNICODE)


@lru_cache(maxsize=None)
def _stemmer():
    import snowballstemmer
    return snowballstemmer.stemmer("porter")


def lemmas(text: str) -> set[str]:
    t = re.sub(r"[\-‐-—/]", " ", text.lower())
    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}


def topic_lemma_df(names: list[str]) -> Counter:
    df = Counter()
    for n in names:
        df.update(lemmas(n))
    return df


def group_windows(t0: int) -> dict[str, list[int]]:
    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0, t0 + 1], "W2": [t0 + 2], "W3": [t0 + 3, t0 + 4]}


def slice_of(y: int) -> int:
    for i, (a, b) in enumerate(SLICES):
        if a <= y <= b:
            return i
    return 0 if y < SLICES[0][0] else len(SLICES) - 1


def nested_defaultdict():
    return defaultdict(lambda: defaultdict(int))
