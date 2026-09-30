#!/usr/bin/env python3
"""STEP 3: English Wikipedia first-revision timestamps (one title per call), with a redirect-first repair.

Titles come from the Wikidata enwiki sitelink (current title; page moves carry history, so the first revision
is the original creation even under an older title), falling back to the OpenAlex wikipedia URL.
Ordered by concept level 2,3,4,5,1,0 so a time-out leaves the most important levels complete.
Results are appended to cache/wikipedia/first_rev.jsonl; re-running resumes.
"""
from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from urllib.parse import unquote

import aiohttp
import pandas as pd
from loguru import logger

from common import CACHE, UA, WORK, Pace, get_json, setup_logging

API = "https://en.wikipedia.org/w/api.php"
OUT_DIR = CACHE / "wikipedia"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "first_rev.jsonl"
CONC = int(sys.argv[1]) if len(sys.argv) > 1 else 8
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 0
RATE = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0


def load_titles() -> list[tuple[str, int]]:
    c = pd.read_parquet(WORK / "concepts.parquet", columns=["openalex_id", "wikidata_qid", "level", "wikipedia_url"])
    wd = {}
    ent = CACHE / "wikidata" / "entities.jsonl"
    if ent.exists():
        for line in ent.open():
            r = json.loads(line)
            wd[r["req"]] = r.get("enwiki_title")
    rows = []
    for r in c.itertuples(index=False):
        t = wd.get(r.wikidata_qid)
        if not t and isinstance(r.wikipedia_url, str) and "/wiki/" in r.wikipedia_url:
            t = unquote(r.wikipedia_url.split("/wiki/", 1)[1]).replace("_", " ")
        if t:
            rows.append((t, int(r.level)))
    order = {2: 0, 3: 1, 4: 2, 5: 3, 1: 4, 0: 5}
    best: dict[str, int] = {}
    for t, lv in rows:
        best[t] = min(best.get(t, 9), order[lv])
    # within a level the order is a seeded random shuffle, so a partial run is a random sample of that level
    import hashlib
    return sorted(best.items(), key=lambda x: (x[1], hashlib.md5(x[0].encode()).hexdigest()))


@logger.catch(reraise=True)
async def amain() -> None:
    setup_logging("s3_wikipedia")
    titles = load_titles()
    done = set()
    if OUT_FILE.exists():
        for line in OUT_FILE.open():
            done.add(json.loads(line)["title_req"])
    todo = [t for t, _ in titles if t not in done]
    if LIMIT:
        todo = todo[:LIMIT]
    logger.info(f"{len(titles)} titles, {len(done)} cached, {len(todo)} to fetch, concurrency {CONC}")
    sem = asyncio.Semaphore(CONC)
    pace = Pace(rate=RATE, max_rate=RATE * 2, min_rate=0.3)
    fh = OUT_FILE.open("a")
    import signal
    signal.signal(signal.SIGTERM, lambda *_: (fh.flush(), fh.close(), os._exit(0)))   # stop without losing buffered rows
    t0 = time.time()
    n = 0
    n_err = 0

    async with aiohttp.ClientSession(headers={"User-Agent": UA, "Accept-Encoding": "gzip"}) as s:
        async def first(title: str, extra: dict) -> dict:
            p = {"action": "query", "prop": "revisions", "titles": title, "rvdir": "newer", "format": "json",
                 "formatversion": 2, "maxlag": 5, "redirects": 1}
            p.update(extra)
            return await get_json(s, API, p, sem, pace=pace)

        async def one(title: str) -> None:
            nonlocal n, n_err
            rec: dict = {"title_req": title}
            try:
                d = await first(title, {"rvlimit": 1, "rvprop": "ids|timestamp|size|comment"})
                pg = d["query"]["pages"][0]
                rec["norm_title"] = pg.get("title")
                rec["followed_redirect"] = bool(d["query"].get("redirects"))
                if pg.get("missing") or "revisions" not in pg:
                    rec["missing"] = True
                else:
                    rv = pg["revisions"][0]
                    rec.update({"pageid": pg.get("pageid"), "first_rev_id": rv.get("revid"),
                                "first_rev_ts": rv.get("timestamp"), "first_rev_size": rv.get("size"),
                                "first_rev_comment": (rv.get("comment") or "")[:300]})
                    susp = (rv.get("size") or 0) < 200 or "redirect" in (rv.get("comment") or "").lower()
                    rec["first_is_redirect"] = False
                    if susp:
                        d2 = await first(title, {"rvlimit": 1, "rvprop": "content", "rvslots": "main"})
                        rv2 = d2["query"]["pages"][0]["revisions"][0]
                        content = (rv2.get("slots", {}).get("main", {}).get("content") or "")
                        rec["first_rev_content_head"] = content[:120]
                        if content.lstrip().upper().startswith("#REDIRECT"):
                            rec["first_is_redirect"] = True
                            d3 = await first(title, {"rvlimit": 50, "rvprop": "timestamp|size"})
                            revs = d3["query"]["pages"][0].get("revisions", [])
                            art = next((r for r in revs if (r.get("size") or 0) >= 500), None)
                            rec["first_article_ts"] = art["timestamp"] if art else None
                            rec["first_article_size"] = art["size"] if art else None
                            rec["n_revs_scanned"] = len(revs)
                    if not rec["first_is_redirect"]:
                        rec["first_article_ts"] = rec["first_rev_ts"]
            except (RuntimeError, KeyError, IndexError) as e:
                rec["error"] = f"{type(e).__name__}: {str(e)[:200]}"
                n_err += 1
            fh.write(json.dumps(rec) + "\n")
            n += 1
            if n % 25 == 0:
                fh.flush()      # the shared filesystem makes per-record flushes slow
            if n % 250 == 0:
                fh.flush()
                el = time.time() - t0
                logger.info(f"{n}/{len(todo)} {n / el:.1f} titles/s pace={pace.rate:.2f}/s 429s={pace.n429} errors={n_err} "
                            f"eta {(len(todo) - n) / (n / el) / 60:.1f} min")

        # bounded fan-out: feed tasks in chunks so memory stays flat
        CH = 2000
        for i in range(0, len(todo), CH):
            await asyncio.gather(*(one(t) for t in todo[i:i + CH]))
            fh.flush()
    fh.close()
    logger.info(f"done {n} titles in {time.time() - t0:.0f}s, errors={n_err}")


if __name__ == "__main__":
    asyncio.run(amain())
