"""S0(a)-(b): yearly counts for all 78 concepts (one group_by each), global totals, t0, newborn flag, status."""
from __future__ import annotations

import json
import math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
from loguru import logger

import oa_client as oa
from panel import BASE_FILTER, INTENDED_GROUP, aliases, name, order, query, DROPPED_ALIASES, ADDED_ALIASES

ROOT = Path(__file__).resolve().parent
YEARS = list(range(1995, 2023))


def yearly(filt: str, tag: str) -> dict[int, int]:
    d = oa.get("/works", {"filter": filt, "group_by": "publication_year"}, tag)
    return {int(g["key"]): int(g["count"]) for g in d["group_by"] if str(g["key"]).isdigit()}


def onset(yc: dict[int, int]) -> tuple[float, bool | None, str]:
    ts = [y for y in range(2000, 2015) if yc.get(y, 0) >= 20]
    if not ts:
        return math.nan, None, "no_onset"
    t0 = ts[0]
    newborn = all(yc.get(t0 - k, 0) < 0.25 * yc.get(t0 + 2, 0) for k in (1, 2, 3))
    if t0 < 2003:
        st = "t0_out_of_dev"
    elif t0 <= 2009:
        st = "dev_candidate"
    else:
        st = "cohort_2010_2014"
    return float(t0), newborn, st


def run() -> pd.DataFrame:
    gtot = yearly(BASE_FILTER, "ground:global")
    pd.DataFrame({"year": YEARS, "total": [gtot.get(y, 0) for y in YEARS]}).to_csv(ROOT / "global_totals.csv",
                                                                                   index=False)
    o = order()
    with ThreadPoolExecutor(3) as ex:
        ycs = list(ex.map(lambda c: yearly(query(c), f"ground:{name(c)}"), o))
    rows, log = [], []
    for c, yc in zip(o, ycs):
        t0, nb, st = onset(yc)
        rows.append({"concept": name(c), "panel_entry": c, **{str(y): yc.get(y, 0) for y in YEARS}})
        log.append({"concept": name(c), "panel_entry": c, "intended_group": INTENDED_GROUP[c],
                    "aliases_used": aliases(c), "query": query(c), "t0": t0, "newborn": nb, "status": st,
                    "pre3": [yc.get(int(t0) - k, 0) for k in (3, 2, 1)] if not math.isnan(t0) else None,
                    "n_t0p2": yc.get(int(t0) + 2, 0) if not math.isnan(t0) else None})
        logger.info(f"{name(c):45s} t0={t0} newborn={nb} {st}")
    pd.DataFrame(rows).to_csv(ROOT / "yearly_counts.csv", index=False)
    # probe sanity anchor: the probe queried without the type/paratext filter
    anchors = {}
    for ph, yrs in {"compressed sensing": {2006: 40, 2007: 120}, "crowdsourcing": {2007: 21, 2008: 59},
                    "optogenetics": {2009: 46, 2010: 157}}.items():
        mine = next(r for r in ycs if True) if False else None
        c = next(x for x in o if name(x) == ph)
        yc = dict(zip(YEARS, [rows[o.index(c)][str(y)] for y in YEARS]))
        anchors[ph] = {str(y): {"probe_no_type_filter": v, "this_run_S0_filter": yc.get(y, 0),
                                "rel_diff": round(yc.get(y, 0) / v - 1, 3)} for y, v in yrs.items()}
    try:
        raw = yearly('title_and_abstract.search:"compressed sensing"', "ground:anchor_nofilter")
        anchors["compressed sensing"]["same_query_as_probe_no_filter"] = {str(y): raw.get(y, 0) for y in (2006, 2007)}
    except oa.BudgetStop as e:
        logger.warning(f"anchor skipped: {e}")
    (ROOT / "grounding_log.json").write_text(json.dumps({
        "query_template": "title_and_abstract.search:\"a1\" OR \"a2\" ...," + BASE_FILTER,
        "or_syntax_check": "compressed sensing / compressive sensing / combined gave identical yearly counts "
                           "(OpenAlex stemming maps both to the same stem); combined >= max and <= sum holds",
        "alias_drops": DROPPED_ALIASES, "alias_additions": ADDED_ALIASES,
        "onset_rule": "t0 = first year 2000..2014 with >= 20 works; newborn = each of t0-3..t0-1 < 0.25*n(t0+2)",
        "probe_anchors": anchors, "concepts": log}, indent=1))
    return pd.DataFrame(log)


if __name__ == "__main__":
    import sys
    logger.remove(); logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "run.log", rotation="30 MB", level="DEBUG")
    df = run()
    print(df["status"].value_counts()); print(oa.credits_summary())
