"""Credit-capped, disk-cached OpenAlex API client (audits and insularity only).

The key is read from env OPENALEX_API_KEY and never written to disk, logs or cache keys. Every call is logged to
credits_log.csv (tag, endpoint, x-ratelimit-remaining). Hard cap: CREDIT_CAP calls-worth of credits; the API is
skipped when the pool reports < MIN_POOL remaining."""
from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import time

import aiohttp

from common import ROOT, SCAN

CREDIT_CAP = 1000
MIN_POOL = 1500
LEDGER = ROOT / "credits_log.csv"
CACHE = SCAN / "oa_cache"
CACHE.mkdir(parents=True, exist_ok=True)
BASE = "https://api.openalex.org"


class OA:
    def __init__(self, concurrency: int = 6):
        self.key = os.environ.get("OPENALEX_API_KEY", "")
        self.sem = asyncio.Semaphore(concurrency)
        self.used = self._ledger_used()
        self.remaining = None
        self.stopped = False

    @staticmethod
    def _ledger_used() -> int:
        if not LEDGER.exists():
            return 0
        with LEDGER.open() as f:
            return sum(int(r["credits"] or 0) for r in csv.DictReader(f))

    def _log(self, tag: str, path: str, credits: int, remaining) -> None:
        new = not LEDGER.exists()
        with LEDGER.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["time", "tag", "path", "credits", "ratelimit_remaining"])
            w.writerow([time.strftime("%H:%M:%S"), tag, path, credits, remaining])

    async def get(self, session: aiohttp.ClientSession, path: str, params: dict, tag: str):
        ck = CACHE / (hashlib.sha1(json.dumps([path, sorted(params.items())]).encode()).hexdigest() + ".json")
        if ck.exists():
            return json.loads(ck.read_text())
        if self.stopped or self.used >= CREDIT_CAP:
            self.stopped = True
            return None
        async with self.sem:
            if self.stopped or self.used >= CREDIT_CAP:
                return None
            q = dict(params)
            if self.key:
                q["api_key"] = self.key
            for k in range(4):
                try:
                    async with session.get(BASE + path, params=q, timeout=aiohttp.ClientTimeout(total=60)) as r:
                        rem = r.headers.get("x-ratelimit-remaining")
                        if rem is not None:
                            try:
                                self.remaining = int(float(rem))
                            except ValueError:
                                pass
                        if r.status == 429:
                            self._log(tag, path, 0, rem)
                            self.stopped = True
                            return None
                        if r.status != 200:
                            await asyncio.sleep(1 + 2 * k)
                            continue
                        d = await r.json()
                        cost = int(float(r.headers.get("x-ratelimit-credits-used", 1) or 1))
                        self.used += cost
                        self._log(tag, path, cost, rem)
                        ck.write_text(json.dumps(d))
                        if self.remaining is not None and self.remaining < MIN_POOL:
                            self.stopped = True
                        return d
                except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError):
                    await asyncio.sleep(1 + 2 * k)
            return None


async def probe() -> dict:
    """One cheap call to read the pool state."""
    oa = OA(1)
    async with aiohttp.ClientSession() as s:
        d = await oa.get(s, "/works", {"filter": "publication_year:2000", "per-page": 1, "select": "id"}, "probe")
    return {"ok": d is not None, "remaining": oa.remaining, "used": oa.used}
