"""Semantic Scholar Graph API client (free, anonymous tier): polite single-lane pacing, jittered backoff, disk cache.

Used because the shared OpenAlex daily pool fell below the sibling-reserve floor (deviation D9): concept papers,
their reference lists and background references come from S2 at zero credit cost.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import random
import threading
import time
from pathlib import Path

import requests
from loguru import logger

BASE = "https://api.semanticscholar.org/graph/v1"
ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache" / "s2"
_lock = threading.Lock()
_last = [0.0]
MIN_GAP = 1.05  # seconds between requests (anonymous tier ~1 rps)
STATS = {"calls": 0, "hits": 0, "retries": 0}


class S2Error(RuntimeError):
    pass


def _ck(kind: str, payload: dict) -> Path:
    h = hashlib.sha1((kind + json.dumps(payload, sort_keys=True)).encode()).hexdigest()
    return CACHE / f"{h}.json.gz"


def _request(method: str, url: str, **kw) -> dict:
    for attempt in range(40):
        with _lock:
            gap = time.time() - _last[0]
            if gap < MIN_GAP:
                time.sleep(MIN_GAP - gap)
            _last[0] = time.time()
        try:
            r = requests.request(method, url, timeout=120, **kw)
        except requests.RequestException as e:
            logger.warning(f"S2 request error {e!r:.150}")
            time.sleep(min(60, 2 ** min(attempt, 5)) + random.random())
            continue
        STATS["calls"] += 1
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504):
            STATS["retries"] += 1
            time.sleep(min(8, 1.0 * 2 ** min(attempt, 3)) + random.random() * 2)
            continue
        raise S2Error(f"HTTP {r.status_code}: {r.text[:300]}")
    raise S2Error(f"S2 failed after retries: {url}")


def cached_call(kind: str, payload: dict, fn) -> dict:
    CACHE.mkdir(parents=True, exist_ok=True)
    p = _ck(kind, payload)
    if p.exists():
        STATS["hits"] += 1
        return json.loads(gzip.decompress(p.read_bytes()))
    d = fn()
    p.write_bytes(gzip.compress(json.dumps(d).encode()))
    return d


def bulk_search(query: str, year: str, fields: str, max_pages: int = 30) -> list[dict]:
    """/paper/search/bulk with token paging (1000 per page). Returns all results."""
    out: list[dict] = []
    token = None
    for page in range(max_pages):
        params = {"query": query, "year": year, "fields": fields}
        if token:
            params["token"] = token
        d = cached_call("bulk", params, lambda: _request("GET", BASE + "/paper/search/bulk", params=params))
        out += d.get("data") or []
        token = d.get("token")
        if not token:
            break
    else:
        logger.warning(f"bulk_search page cap hit for {query} {year}")
    return out


def batch(ids: list[str], fields: str, size: int = 500) -> list[dict | None]:
    """/paper/batch (POST, <=500 ids per call). Order follows ids; unknown ids -> None."""
    out: list[dict | None] = []
    for i in range(0, len(ids), size):
        chunk = ids[i:i + size]
        payload = {"ids": chunk, "fields": fields}
        d = cached_call("batch", payload, lambda: _request("POST", BASE + "/paper/batch",
                                                          params={"fields": fields}, json={"ids": chunk}))
        out += d
    return out
