"""S0(c)-(d): venue-field labels per concept window, home field, dev gate.

Windows (pooled, one group_by=primary_location.source.id call each, top-200 sources, max_pages from config):
  A = t0..t0+1 (home), B = t0+2 (A+B = W3, G window), C = t0+3..t0+4 (A+B+C = W5), D = t0+6..t0+8 (outcome).
Budget deviation (logged): per-year pulls were pooled into these 4 windows because the shared key had only
~2,100 credits left for five artifacts; the next-field entry test uses the step A -> B -> C -> D.
"""
from __future__ import annotations

import json
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from loguru import logger

import oa_client as oa
from panel import query

ROOT = Path(__file__).resolve().parent
LAB_FILE = ROOT / "cache" / "window_labels.json"
DEV_FIELDS = ["Computer Science", "Engineering", "Biochemistry, Genetics and Molecular Biology", "Medicine"]
GROUP_SHORT = {"Computer Science": "CS", "Engineering": "Eng",
               "Biochemistry, Genetics and Molecular Biology": "BGM", "Medicine": "Med"}


def windows(t0: int) -> dict[str, tuple[int, int]]:
    return {"A": (t0, t0 + 1), "B": (t0 + 2, t0 + 2), "C": (t0 + 3, t0 + 4), "D": (t0 + 6, t0 + 8)}


def pull_window(concept_entry: str, t0: int, w: str, tag: str, max_pages: int = 1) -> dict:
    y0, y1 = windows(t0)[w]
    yr = f"{y0}" if y0 == y1 else f"{y0}-{y1}"
    return oa.group_by_all(query(concept_entry) + f",publication_year:{yr}", "primary_location.source.id",
                           tag=tag, max_pages=max_pages)


def field_counts(res: dict) -> dict:
    """Map a source group_by result to field counts using the SRC cache."""
    fc: Counter = Counter()
    lab = 0
    for sid, n in res["groups"].items():
        f = oa.src_field(sid)
        if f:
            fc[f] += n
            lab += n
    return {"fields": dict(fc), "labelled": lab, "total": res["meta_count"], "top200_covered":
            sum(res["groups"].values()), "truncated_share": res["truncated_share"], "complete": res["complete"],
            "n_sources": len(res["groups"])}


def home_of(fc: Counter) -> list[str]:
    tot = sum(fc.values())
    if not tot:
        return []
    h = [f for f, n in fc.items() if n / tot >= 0.40]
    return sorted(h) if h else [fc.most_common(1)[0][0]]


def pull_many(jobs: list[tuple[str, str, int, str]], tag: str, max_pages: int = 1) -> dict:
    """jobs: (concept_name, entry, t0, window) -> {(name, w): raw result}; stops cleanly on BudgetStop."""
    out = {}

    def one(j):
        nm, entry, t0, w = j
        try:
            return j, pull_window(entry, t0, w, f"{tag}:{nm}:{w}", max_pages=max_pages)
        except oa.BudgetStop as e:
            logger.warning(f"BudgetStop {nm} {w}: {e}")
            return j, None
    with ThreadPoolExecutor(3) as ex:
        for j, r in ex.map(one, jobs):
            if r is not None:
                out[(j[0], j[3])] = r
    return out
