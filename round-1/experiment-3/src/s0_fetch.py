#!/usr/bin/env python3
"""S0 step (a): yearly counts of phrase-matched works per concept (ONE group_by=publication_year call each),
the global per-year denominator G[y], and the one-off OR-syntax test (Step 0a of the plan).
All responses are cached (cache/) and never re-queried. Writes results/yearly_counts_api.json."""
from __future__ import annotations

import json
import sys
from concurrent.futures import ThreadPoolExecutor

from loguru import logger

from config import BASEF, LOGS, ORDER, PANEL, RES
import oa_client as oa

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "s0_fetch.log", rotation="30 MB", level="DEBUG")

SYNTAX_FILE = RES / "or_syntax_test.json"


def search_filter(phrases: list[str], syntax: str) -> str:
    """title_and_abstract.search over the quoted phrase(s), OR-joined with the frozen syntax."""
    q = [f'"{p}"' for p in phrases]
    if len(q) == 1:
        s = q[0]
    elif syntax == "pipe":
        s = "|".join(q)
    else:
        s = "(" + " OR ".join(q) + ")"
    return f"{BASEF},title_and_abstract.search:{s}"


def or_syntax_test() -> str:
    if SYNTAX_FILE.exists():
        return json.loads(SYNTAX_FILE.read_text())["frozen"]
    a, b = "compressed sensing", "compressive sensing"
    ya = oa.yearly_counts(search_filter([a], "pipe"), kind="or_test")
    yb = oa.yearly_counts(search_filter([b], "pipe"), kind="or_test")
    res = {"single_a": ya, "single_b": yb, "checks": {}}
    frozen = None
    for syn in ("pipe", "boolean"):
        try:
            yo = oa.yearly_counts(search_filter([a, b], syn), kind="or_test")
        except ValueError as e:  # query rejected
            res["checks"][syn] = {"error": str(e)[:300]}
            continue
        ok = all(max(ya.get(y, 0), yb.get(y, 0)) <= yo.get(y, 0) <= ya.get(y, 0) + yb.get(y, 0)
                 for y in range(2008, 2013))
        res["checks"][syn] = {"ok": ok, "or": yo}
        if ok and frozen is None:
            frozen = syn
    res["frozen"] = frozen or "per_alias_sum"
    SYNTAX_FILE.write_text(json.dumps(res, indent=1))
    logger.info(f"OR syntax test -> {res['frozen']}  checks={ {k: v.get('ok') for k, v in res['checks'].items()} }")
    return res["frozen"]


def concept_yearly(i: int, syntax: str) -> dict[int, int]:
    name, aliases, _ = PANEL[i]
    phrases = [name] + aliases
    if syntax == "per_alias_sum" and aliases:
        tot: dict[int, int] = {}
        for p in phrases:
            for y, c in oa.yearly_counts(search_filter([p], "pipe"), kind="yearly").items():
                tot[y] = tot.get(y, 0) + c
        return tot
    return oa.yearly_counts(search_filter(phrases, syntax), kind="yearly")


@logger.catch(reraise=True)
def main() -> None:
    syntax = or_syntax_test()
    G = oa.yearly_counts(BASEF, kind="global")
    out = {"syntax": syntax, "G": G, "concepts": {}}
    with ThreadPoolExecutor(4) as ex:
        futs = {i: ex.submit(concept_yearly, i, syntax) for i in ORDER}
        for i in ORDER:
            try:
                out["concepts"][PANEL[i][0]] = futs[i].result()
            except oa.BudgetStop as e:
                logger.error(f"budget stop at {PANEL[i][0]}: {e}")
                break
    (RES / "yearly_counts_api.json").write_text(json.dumps(out, indent=1))
    logger.info(f"yearly counts for {len(out['concepts'])} concepts; credits used {oa.credits_used()} "
                f"remaining header {oa.STATE.get('last_remaining')}")


if __name__ == "__main__":
    main()
