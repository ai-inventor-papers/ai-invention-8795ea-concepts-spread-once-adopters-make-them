#!/usr/bin/env python3
"""STEP 3b: page ids (and redirect resolution) for every enwiki title, 50 titles per call.

MediaWiki assigns page_id sequentially when a page is created, so page_id is a monotone proxy of the page's
creation time. s8 fits a monotone (isotonic) map page_id -> first-revision timestamp on the titles whose first
revision was fetched exactly (s3) and uses it only for titles s3 could not reach under the IP rate limit.
Output: cache/wikipedia/pageids.jsonl (resumable).
"""
from __future__ import annotations

import asyncio
import json
import time

import aiohttp
from loguru import logger

from common import CACHE, UA, Pace, get_json, setup_logging
from s3_wikipedia import load_titles

API = "https://en.wikipedia.org/w/api.php"
OUT_FILE = CACHE / "wikipedia" / "pageids.jsonl"


@logger.catch(reraise=True)
async def amain() -> None:
    setup_logging("s3b_pageids")
    titles = [t for t, _ in load_titles()]
    done = set()
    if OUT_FILE.exists():
        for line in OUT_FILE.open():
            done.add(json.loads(line)["title_req"])
    todo = [t for t in titles if t not in done]
    batches = [todo[i:i + 50] for i in range(0, len(todo), 50)]
    logger.info(f"{len(titles)} titles, {len(done)} cached, {len(batches)} calls")
    sem = asyncio.Semaphore(2)
    pace = Pace(rate=1.0, max_rate=3.0, min_rate=0.2)
    fh = OUT_FILE.open("a")
    t0 = time.time()
    async with aiohttp.ClientSession(headers={"User-Agent": UA, "Accept-Encoding": "gzip"}) as s:
        q: asyncio.Queue = asyncio.Queue()
        for b in batches:
            q.put_nowait(b)

        async def worker() -> None:
            n = 0
            while not q.empty():
                b = q.get_nowait()
                try:
                    d = await get_json(s, API, {"action": "query", "prop": "info", "titles": "|".join(b), "redirects": 1,
                                                "format": "json", "formatversion": 2, "maxlag": 5}, sem, pace=pace,
                                       tries=20)
                except RuntimeError as e:
                    logger.error(str(e)[:200])
                    continue
                qd = d.get("query", {})
                norm = {x["from"]: x["to"] for x in qd.get("normalized", [])}
                red = {x["from"]: x["to"] for x in qd.get("redirects", [])}
                pages = {p["title"]: p for p in qd.get("pages", [])}
                for t in b:
                    u = norm.get(t, t)
                    tgt = red.get(u, u)
                    p = pages.get(tgt, {})
                    fh.write(json.dumps({"title_req": t, "title_final": tgt, "redirected": tgt != u,
                                         "pageid": p.get("pageid"), "missing": bool(p.get("missing", not p)),
                                         "length": p.get("length"), "lastrevid": p.get("lastrevid")}) + "\n")
                fh.flush()
                n += 1
                if q.qsize() % 50 == 0:
                    el = time.time() - t0
                    logger.info(f"{len(batches) - q.qsize()}/{len(batches)} calls, {el:.0f}s, pace {pace.rate:.2f}/s, 429s {pace.n429}")

        await asyncio.gather(*(worker() for _ in range(2)))
    fh.close()
    logger.info("pageids done")


if __name__ == "__main__":
    asyncio.run(amain())
