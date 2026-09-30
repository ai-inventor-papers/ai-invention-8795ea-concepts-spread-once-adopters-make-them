"""OpenAlex client: disk cache (gzip JSON keyed by sha1 of the key-free URL), credit ledger, budget guards.

Every raw response is cached once and never re-queried (same-day counts drift). The API key is read from the
environment (OPENALEX_API_KEY) and is never written to any cache key, log line, csv or json.
"""
from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import random
import threading
import time
from pathlib import Path
from urllib.parse import urlencode

import requests
from loguru import logger

BASE = "https://api.openalex.org"
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
LEDGER = ROOT / "logs" / "credits.csv"
OWN_CAP = int(os.environ.get("OA_OWN_CAP", "3500"))
SHARED_FLOOR = int(os.environ.get("OA_SHARED_FLOOR", "1000"))
MAX_OR = 50  # OpenAlex caps pipe-ORed filters at 50 values


class CapReached(RuntimeError):
    """This artifact's own credit cap would be exceeded."""


class SharedPoolLow(RuntimeError):
    """The shared daily pool fell below the floor reserved for sibling artifacts."""


class FreeCallCharged(RuntimeError):
    """A call expected to be free was charged."""


class OAError(RuntimeError):
    """A request failed permanently."""


def _key() -> str:
    k = os.environ.get("OPENALEX_API_KEY", "")
    if not k:
        raise RuntimeError("OPENALEX_API_KEY not set")
    return k


def cache_key(path: str, params: dict) -> str:
    """sha1 of the canonical URL WITHOUT the api key."""
    clean = {k: v for k, v in params.items() if k != "api_key"}
    url = path + "?" + urlencode(sorted(clean.items()))
    return hashlib.sha1(url.encode()).hexdigest()


def redact(s: str) -> str:
    k = os.environ.get("OPENALEX_API_KEY", "")
    return s.replace(k, "<REDACTED>") if k else s


class Client:
    def __init__(self, concurrency: int = 3) -> None:
        CACHE.mkdir(parents=True, exist_ok=True)
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        self.sem = threading.Semaphore(concurrency)
        self.lock = threading.Lock()
        self.own_total = 0
        self.remaining: int | None = None
        self.calls = 0
        self.cache_hits = 0
        self.free_broken = False
        if LEDGER.exists():  # keep the spend record across restarts
            with LEDGER.open() as f:
                for row in csv.DictReader(f):
                    self.own_total += int(row["credits"])
                    if row["remaining"] and int(row["remaining"]) > 0:
                        self.remaining = int(row["remaining"])
        else:
            with LEDGER.open("w", newline="") as f:
                csv.writer(f).writerow(["ts", "path", "summary", "credits", "remaining"])
        logger.info(f"OA client: own_total so far={self.own_total}, last remaining={self.remaining}")

    def _guard(self, projected: int) -> None:
        if self.own_total + projected > OWN_CAP:
            raise CapReached(f"own_total {self.own_total} + {projected} > cap {OWN_CAP}")
        if self.remaining is not None and self.remaining < SHARED_FLOOR:
            raise SharedPoolLow(f"shared remaining {self.remaining} < floor {SHARED_FLOOR}")

    def cached(self, path: str, params: dict) -> dict | None:
        p = CACHE / (cache_key(path, params) + ".json.gz")
        if p.exists():
            return json.loads(gzip.decompress(p.read_bytes()))
        return None

    def get(self, path: str, params: dict, projected: int = 1, summary: str = "", free: bool = False) -> dict:
        """free=True: a documented zero-credit call (singleton GET). It bypasses the credit guards but aborts
        (FreeCallCharged) the moment the API reports a non-zero cost, so it can never draw on the shared pool."""
        params = {k: v for k, v in params.items() if v is not None}
        ck = cache_key(path, params)
        cp = CACHE / (ck + ".json.gz")
        if cp.exists():
            self.cache_hits += 1
            return json.loads(gzip.decompress(cp.read_bytes()))
        if not free:
            self._guard(projected)
        if self.free_broken and free:
            raise FreeCallCharged("singleton GETs are being charged; stopped")
        with self.sem:
            if not free:
                self._guard(projected)
            q = dict(params)
            q["api_key"] = _key()
            last = ""
            n429 = 0
            for attempt in range(20):
                if attempt:
                    # per-second 429s: short jittered waits; other failures: exponential backoff (max 6 real tries)
                    time.sleep(0.4 + random.random() if last.startswith("HTTP 429") else min(32, 2 ** attempt) + random.random())
                try:
                    r = requests.get(BASE + path, params=q, timeout=120)
                except requests.RequestException as e:
                    last = redact(repr(e))
                    logger.warning(f"request error {path} attempt {attempt}: {last[:200]}")
                    continue
                cost = float(r.headers.get("x-ratelimit-cost-usd", 0) or 0)
                credits = int(round(cost * 10000))
                rem = r.headers.get("x-ratelimit-remaining")
                with self.lock:
                    self.own_total += credits
                    self.calls += 1
                    # 429 (per-second rate limit) responses report remaining=0: only trust successful responses
                    if r.status_code == 200 and rem is not None and rem.lstrip("-").isdigit():
                        self.remaining = int(rem)
                    with LEDGER.open("a", newline="") as f:
                        csv.writer(f).writerow([time.strftime("%Y-%m-%dT%H:%M:%S"), path,
                                                redact(summary or str(params.get("filter", ""))[:120]),
                                                credits, self.remaining if self.remaining is not None else ""])
                if free and credits > 0:
                    self.free_broken = True
                    raise FreeCallCharged(f"free call charged {credits} credits: {path}")
                if r.status_code == 200:
                    data = r.json()
                    cp.write_bytes(gzip.compress(json.dumps(data).encode()))
                    return data
                last = f"HTTP {r.status_code}: {redact(r.text[:300])}"
                if r.status_code == 429:
                    n429 += 1
                    logger.debug(f"{path} 429 (attempt {attempt})")
                    continue
                if r.status_code in (500, 502, 503, 504):
                    logger.warning(f"{path} {last[:200]} (attempt {attempt})")
                    if attempt - n429 >= 6:
                        break
                    continue
                raise OAError(last)
            raise OAError(f"failed after retries: {path} {last}")


def chunks(xs: list, n: int = MAX_OR) -> list[list]:
    assert n <= MAX_OR
    return [xs[i:i + n] for i in range(0, len(xs), n)]


def short(oid: str) -> str:
    return oid.rsplit("/", 1)[-1]
