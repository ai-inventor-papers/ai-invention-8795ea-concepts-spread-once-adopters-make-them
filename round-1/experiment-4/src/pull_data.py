"""All OpenAlex downloads, in priority order; every response cached once (re-running costs 0 credits).

Usage: OPENALEX_API_KEY=... python pull_data.py <stage>   stage in {A, backbone, BD, C, insularity, p5, all}
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd
from loguru import logger

import oa_client as oa
from panel import name, query
from s0_labels import DEV_FIELDS, field_counts, home_of, pull_many

ROOT = Path(__file__).resolve().parent
FIELD_IDS = list(range(11, 37))
SLICE_A = "1998-2002"
STATE_FILE = ROOT / "cache" / "pull_state.json"


def load_ground() -> list[dict]:
    return json.loads((ROOT / "grounding_log.json").read_text())["concepts"]


def lookup_from(results: dict) -> None:
    ids = [sid for r in results.values() for sid in r["groups"]]
    try:
        oa.lookup_sources(ids)
    except oa.BudgetStop as e:
        logger.warning(f"source lookup budget stop: {e}")


def stage_A() -> dict:
    g = [c for c in load_ground() if c["status"] == "dev_candidate"]
    jobs = [(c["concept"], c["panel_entry"], int(c["t0"]), "A") for c in g]
    res = pull_many(jobs, "home_labels")
    lookup_from(res)
    homes = {}
    for c in g:
        r = res.get((c["concept"], "A"))
        if r is None:
            homes[c["concept"]] = {"status": "not_pulled"}
            continue
        fc = field_counts(r)
        thin = fc["labelled"] < 10
        cnt = Counter(fc["fields"])
        if thin:  # also use t0+2 before deciding
            rb = pull_many([(c["concept"], c["panel_entry"], int(c["t0"]), "B")], "home_labels")
            lookup_from(rb)
            if (c["concept"], "B") in rb:
                cnt += Counter(field_counts(rb[(c["concept"], "B")])["fields"])
        h = home_of(cnt)
        dev = bool(h) and all(x in DEV_FIELDS for x in h)
        homes[c["concept"]] = {"home": h, "thin_home": thin, "labelled_A": fc["labelled"], "total_A": fc["total"],
                               "status": "dev" if dev else ("sealed_home_dropped" if h else "no_labelled_home")}
        logger.info(f"{c['concept']:40s} home={h} lab={fc['labelled']}/{fc['total']} -> {homes[c['concept']]['status']}")
    (ROOT / "cache" / "homes.json").write_text(json.dumps(homes, indent=1))
    return homes


def dev_list() -> list[dict]:
    homes = json.loads((ROOT / "cache" / "homes.json").read_text())
    return [c for c in load_ground() if homes.get(c["concept"], {}).get("status") == "dev"]


def stage_windows(ws: list[str], tag_map: dict[str, str]) -> None:
    dev = dev_list()
    for w in ws:
        jobs = [(c["concept"], c["panel_entry"], int(c["t0"]), w) for c in dev]
        res = pull_many(jobs, tag_map[w])
        lookup_from(res)
        logger.info(f"window {w}: pulled {len(res)}/{len(jobs)}; {oa.credits_summary()}")


def stage_backbone() -> None:
    for f in FIELD_IDS:
        try:
            oa.get("/works", {"filter": f"topics.field.id:{f},publication_year:{SLICE_A},type:article|review",
                              "group_by": "topics.field.id", "per_page": 200}, f"backbone:A:{f}")
        except oa.BudgetStop as e:
            logger.warning(f"backbone stop {e}")
            return
    oa.get("/works", {"filter": f"publication_year:{SLICE_A},type:article|review", "group_by": "primary_topic.field.id",
                      "per_page": 200}, "backbone:A:N")


def stage_insularity(n_batches: int = 2) -> None:
    """Topic-label insularity (degrade-ladder step 2): per field j, a seeded sample of 50*n_batches citing
    works (primary_topic field j, 1998-2002, articles with >4 refs); their references grouped by
    primary_topic.field.id via OR-joined cited_by filters (50 IDs per call)."""
    # smoke: OR on cited_by must behave like a union
    s = oa.get("/works", {"filter": f"primary_topic.field.id:17,publication_year:{SLICE_A},type:article,"
                                    "referenced_works_count:>4", "sample": 50 * n_batches, "seed": 20260928,
                          "per_page": 50 * n_batches, "select": "id"}, "insularity:sample:17")
    ids = [w["id"].split("/")[-1] for w in s["results"]]
    one = oa.get("/works", {"filter": f"cited_by:{ids[0]}", "group_by": "primary_topic.field.id"}, "insularity:smoke1")
    two = oa.get("/works", {"filter": f"cited_by:{ids[0]}|{ids[1]}", "group_by": "primary_topic.field.id"},
                 "insularity:smoke2")
    n1, n2 = one["meta"]["count"], two["meta"]["count"]
    logger.info(f"cited_by OR smoke: single={n1} pair={n2}")
    (ROOT / "cache" / "citedby_smoke.json").write_text(json.dumps({"single": n1, "pair": n2, "or_ok": n2 >= n1}))
    for f in FIELD_IDS:
        try:
            s = oa.get("/works", {"filter": f"primary_topic.field.id:{f},publication_year:{SLICE_A},type:article,"
                                            "referenced_works_count:>4", "sample": 50 * n_batches,
                                  "seed": 20260928, "per_page": 50 * n_batches, "select": "id"},
                       f"insularity:sample:{f}")
            ids = [w["id"].split("/")[-1] for w in s["results"]]
            for b in range(0, len(ids), 50):
                oa.get("/works", {"filter": "cited_by:" + "|".join(ids[b:b + 50]),
                                  "group_by": "primary_topic.field.id"}, f"insularity:refs:{f}:{b // 50}")
        except oa.BudgetStop as e:
            logger.warning(f"insularity stop at field {f}: {e}")
            return


def stage_p5() -> None:
    dev = dev_list()
    for c in dev:
        t0 = int(c["t0"])
        for yr, tag in ((f"{t0}-{t0 + 4}", "W5"), (f"{t0}-{t0 + 1}", "A")):
            try:
                oa.get("/works", {"filter": query(c["panel_entry"]) + f",publication_year:{yr}",
                                  "group_by": "primary_topic.field.id", "per_page": 200},
                       f"primary_topic:{c['concept']}:{tag}")
            except oa.BudgetStop as e:
                logger.warning(f"p5 stop: {e}")
                return


if __name__ == "__main__":
    logger.remove(); logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "pull.log", rotation="30 MB", level="DEBUG")
    st = sys.argv[1]
    tm = {"B": "feat_years", "C": "feat_years", "D": "outcome_win"}
    if st in ("A", "all"):
        stage_A()
    if st in ("backbone", "all"):
        stage_backbone()
    if st in ("BD", "all"):
        stage_windows(["B", "D"], tm)
    if st in ("C", "all"):
        stage_windows(["C"], tm)
    if st in ("insularity", "all"):
        stage_insularity()
    if st in ("p5",):
        stage_p5()
    logger.info(f"credits: {oa.credits_summary()}")
