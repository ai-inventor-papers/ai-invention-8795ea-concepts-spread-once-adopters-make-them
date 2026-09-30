"""Credit-aware, disk-cached OpenAlex client.

Every raw response is cached once under cache/<sha1>.json and never re-queried (the run's probe saw counts
drift between same-day calls). Credits are read from the x-ratelimit-cost-usd header (1 credit = $0.0001)
and persisted in results/credit_ledger.json after every paid call. The API key is read from the
OPENALEX_API_KEY environment variable and is never written to disk (cache keys exclude it)."""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from typing import Any

import requests
from loguru import logger

from config import API_SESSION_CAP, CACHE, CREDIT_CAP, RES, RESERVE_STOP_REMAINING

BASE = "https://api.openalex.org"
LEDGER = RES / "credit_ledger.json"
_LOCK = threading.Lock()


class BudgetStop(RuntimeError):
    """Raised when the credit cap is reached or OpenAlex refuses with 403."""


def _load_ledger() -> dict[str, Any]:
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    return {"credits_used": 0, "usd": 0.0, "n_calls": 0, "n_cache_hits": 0, "last_remaining": None,
            "cost_by_kind": {}, "stop_new_downloads": False}


STATE = _load_ledger()
_consec_403 = [0]
_session = requests.Session()


def _save_ledger() -> None:
    LEDGER.write_text(json.dumps(STATE, indent=1))


def cache_key(path: str, params: dict[str, Any]) -> str:
    p = {k: v for k, v in params.items() if k != "api_key"}
    s = path + "?" + json.dumps(p, sort_keys=True)
    return hashlib.sha1(s.encode()).hexdigest()


def is_cached(path: str, params: dict[str, Any]) -> bool:
    return (CACHE / f"{cache_key(path, params)}.json").exists()


def get(path: str, params: dict[str, Any], kind: str = "other") -> dict[str, Any]:
    """Cached GET. `kind` only labels the ledger breakdown."""
    fp = CACHE / f"{cache_key(path, params)}.json"
    if fp.exists():
        with _LOCK:
            STATE["n_cache_hits"] += 1
        return json.loads(fp.read_text())["body"]
    with _LOCK:
        if STATE["credits_used"] >= min(CREDIT_CAP, API_SESSION_CAP) - 5:
            raise BudgetStop(f"credit cap reached ({STATE['credits_used']})")
    q = dict(params)
    if os.environ.get("OPENALEX_ANON") == "1":
        pass  # public per-IP anonymous pool (used when the shared key's daily allowance is exhausted)
    else:
        key = os.environ.get("OPENALEX_API_KEY")
        if not key:
            raise BudgetStop("OPENALEX_API_KEY not set (and OPENALEX_ANON!=1) and response not cached")
        q["api_key"] = key
    last_err = None
    for k in range(6):
        if k:
            time.sleep(5 * k)
        try:
            r = _session.get(BASE + path, params=q, timeout=120)
        except requests.RequestException as e:
            last_err = repr(e)
            logger.warning(f"request error ({k}) {path}: {last_err[:200]}")
            continue
        cost = r.headers.get("x-ratelimit-cost-usd")
        rem = r.headers.get("x-ratelimit-remaining")
        if r.status_code == 200:
            _consec_403[0] = 0
            body = r.json()
            if cost is not None:
                credits = round(float(cost) / 0.0001)
            else:
                credits = 10 if ("search" in str(params.get("filter", "")) and not params.get("group_by")
                                 and not params.get("sample")) else 1
            with _LOCK:
                STATE["credits_used"] += credits
                STATE["usd"] += float(cost or 0)
                STATE["n_calls"] += 1
                STATE["cost_by_kind"][kind] = STATE["cost_by_kind"].get(kind, 0) + credits
                if rem is not None:
                    STATE["last_remaining"] = rem
                    try:
                        if float(rem) < RESERVE_STOP_REMAINING:
                            STATE["stop_new_downloads"] = True
                    except ValueError:
                        pass
                _save_ledger()
            tmp = fp.with_suffix(".tmp")
            tmp.write_text(json.dumps({"path": path, "params": {kk: vv for kk, vv in params.items() if kk != "api_key"},
                                       "credits": credits, "t": time.time(), "body": body}))
            tmp.replace(fp)
            logger.debug(f"GET {path} {kind} credits={credits} remaining={rem} total={STATE['credits_used']}")
            return body
        if r.status_code == 403:
            _consec_403[0] += 1
            logger.error(f"403 from OpenAlex: {r.text[:200]}")
            if _consec_403[0] >= 3 or "budget" in r.text.lower() or "credit" in r.text.lower():
                raise BudgetStop(f"403: {r.text[:200]}")
            continue
        if r.status_code in (429,) or r.status_code >= 500:
            last_err = f"HTTP {r.status_code}: {r.text[:200]}"
            logger.warning(f"retry ({k}) {path}: {last_err}")
            continue
        # 4xx other than 403/429: a query error, do not retry
        raise ValueError(f"HTTP {r.status_code} for {path} {params}: {r.text[:300]}")
    raise RuntimeError(f"failed {path} {params}: {last_err}")


def group_all(filt: str, group_by: str, kind: str = "group") -> list[dict[str, Any]]:
    """Full group_by listing with mandatory cursor paging (groups are sorted by key, so page to the end)."""
    out: list[dict[str, Any]] = []
    cur = "*"
    while cur:
        d = get("/works", {"filter": filt, "group_by": group_by, "per_page": 200, "cursor": cur}, kind=kind)
        g = d.get("group_by") or []
        out += g
        # a short page is the last one: skip the (paid) empty follow-up page
        cur = d.get("meta", {}).get("next_cursor") if len(g) >= 200 else None
    return out


def yearly_counts(filt: str, kind: str = "yearly") -> dict[int, int]:
    g = group_all(filt, "publication_year", kind=kind)
    return {int(a["key"]): int(a["count"]) for a in g if str(a["key"]).isdigit()}


def credits_used() -> int:
    return int(STATE["credits_used"])


def stop_flag() -> bool:
    return bool(STATE.get("stop_new_downloads"))
