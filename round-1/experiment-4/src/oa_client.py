"""OpenAlex HTTP client: disk cache (never re-query), credit ledger, sub-budgets, BudgetStop.

Adapted from the run's probe (probe_null_decomposition.py): get() retry wrapper, x-ratelimit-cost-usd
accounting, yearly group_by, and the source -> venue-field labelling rule (type != repository, dominant
field >= 40% of summed topic counts). /works ID batches are capped at 50 (the probe's 100-ID batch failed).
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

import requests
from loguru import logger

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache" / "raw"
CACHE.mkdir(parents=True, exist_ok=True)
LEDGER = ROOT / "credits_log.csv"
BASE = "https://api.openalex.org"
HARD_CAP = 1200.0
FLOOR = 1000.0
SUB_BUDGETS = {"ground": 90, "home_labels": 130, "feat_years": 200, "outcome_win": 260, "source_lookup": 260,
               "backbone": 70, "insularity": 160, "primary_topic": 60, "smoke": 20}


class BudgetStop(RuntimeError):
    """Raised when a hard cap, sub-budget, or the shared-key floor would be crossed."""


class _State:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.cum = 0.0
        self.by_tag: Counter = Counter()
        self.last_remaining: float | None = None
        self.n_calls = 0
        self.n_cache_hits = 0
        if LEDGER.exists():
            with LEDGER.open() as f:
                for row in csv.DictReader(f):
                    c = float(row["cost"])
                    self.cum += c
                    self.by_tag[row["tag"].split(":")[0]] += c
                    if row["remaining"] not in ("", "None", "0") and float(row["cost"]) > 0:
                        self.last_remaining = float(row["remaining"])
        else:
            LEDGER.write_text("ts,tag,path,cost,remaining,cumulative\n")


STATE = _State()


def _key(path: str, params: dict[str, Any]) -> str:
    clean = {k: str(v) for k, v in params.items() if k != "api_key"}
    raw = path + "?" + json.dumps(sorted(clean.items()))
    return hashlib.sha1(raw.encode()).hexdigest()


def cached(path: str, params: dict[str, Any]) -> bool:
    return (CACHE / f"{_key(path, params)}.json").exists()


def get(path: str, params: dict[str, Any], tag: str, expected_cost: float = 1.0) -> dict:
    """GET with cache; tag prefix (before ':') selects the sub-budget."""
    k = _key(path, params)
    fp = CACHE / f"{k}.json"
    if fp.exists():
        with STATE.lock:
            STATE.n_cache_hits += 1
        return json.loads(fp.read_text())["response"]
    sub = tag.split(":")[0]
    with STATE.lock:
        if STATE.cum + expected_cost > HARD_CAP:
            raise BudgetStop(f"hard cap {HARD_CAP} reached at {STATE.cum:.0f} ({tag})")
        if sub in SUB_BUDGETS and STATE.by_tag[sub] + expected_cost > SUB_BUDGETS[sub] * SUB_SCALE.get(sub, 1.0):
            raise BudgetStop(f"sub-budget {sub} exhausted ({STATE.by_tag[sub]:.0f})")
        if STATE.last_remaining is not None and STATE.last_remaining < FLOOR:
            raise BudgetStop(f"shared key remaining {STATE.last_remaining} < floor {FLOOR}")
    key = os.environ.get("OPENALEX_API_KEY")
    if not key:
        raise RuntimeError("OPENALEX_API_KEY not set")
    q = dict(params)
    q["api_key"] = key
    last_err = ""
    for attempt in range(8):
        if attempt:
            time.sleep(min(5 * attempt, 20) if last_err[:8] != "HTTP 429" else 1.0 + attempt)
        _throttle()
        try:
            r = requests.get(BASE + path, params=q, timeout=120)
        except requests.RequestException as e:
            last_err = repr(e)[:200]
            logger.warning(f"net error {tag} attempt {attempt}: {last_err}")
            continue
        cost_usd = r.headers.get("x-ratelimit-cost-usd")
        cost = float(cost_usd) / 0.0001 if cost_usd not in (None, "") else 1.0
        if r.status_code == 429:
            cost = 0.0  # per-second rate-limit rejections are not charged (logged with cost 0)
        rem = r.headers.get("x-ratelimit-remaining")
        with STATE.lock:
            STATE.cum += cost
            STATE.by_tag[sub] += cost
            STATE.n_calls += 1
            try:
                if r.status_code != 429 and rem not in (None, ""):
                    STATE.last_remaining = float(rem)
            except ValueError:
                pass
            with LEDGER.open("a") as f:
                f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')},{tag},{path},{cost:.3f},{rem},{STATE.cum:.3f}\n")
        if r.status_code == 200:
            resp = r.json()
            fp.write_text(json.dumps({"request": {"path": path, "params": {k2: v for k2, v in params.items()}},
                                      "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%S"), "cost": cost,
                                      "response": resp}))
            return resp
        body = r.text[:300]
        if r.status_code in (402, 403) or "budget" in body.lower() or "insufficient" in body.lower():
            raise BudgetStop(f"API refusal {r.status_code}: {body}")
        if r.status_code in (400, 404):
            raise ValueError(f"HTTP {r.status_code} for {path} {params}: {body}")
        last_err = f"HTTP {r.status_code}: {body}"
        logger.warning(f"{tag} attempt {attempt}: {last_err}")
    raise RuntimeError(f"failed {path} {params}: {last_err}")


SUB_SCALE: dict[str, float] = {}
_T_LOCK = threading.Lock()
_T_LAST = [0.0]
MIN_GAP = 0.25  # <= 4 requests/s from this artifact (the key's 30 req/s limit is shared with siblings)


def _throttle() -> None:
    with _T_LOCK:
        wait = _T_LAST[0] + MIN_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        _T_LAST[0] = time.time()


def credits_summary() -> dict:
    return {"cumulative": round(STATE.cum, 2), "by_subbudget": {k: round(v, 2) for k, v in STATE.by_tag.items()},
            "last_remaining": STATE.last_remaining, "n_network_calls_this_process": STATE.n_calls,
            "n_cache_hits_this_process": STATE.n_cache_hits}


def group_by_all(filt: str, group_by: str, tag: str, max_pages: int = 1) -> dict:
    """Top-200 page without cursor; if more groups and max_pages>1, cursor paging (sorted by key).

    Returns {'groups': {key: count}, 'meta_count': int, 'groups_count': int|None, 'truncated_share': float,
    'complete': bool}.  If the cursor pull is truncated the top-200 result is kept (cursor pages are key-sorted).
    """
    d = get("/works", {"filter": filt, "group_by": group_by, "per_page": 200}, tag)
    groups = {str(g["key"]): int(g["count"]) for g in d.get("group_by", [])}
    meta = d.get("meta", {})
    total = int(meta.get("count") or 0)
    gcount = meta.get("groups_count")
    complete = len(groups) < 200
    if not complete and max_pages > 1:
        cur, pages, allg = "*", 0, {}
        try:
            while cur and pages < max_pages:
                dd = get("/works", {"filter": filt, "group_by": group_by, "per_page": 200, "cursor": cur}, tag)
                for g in dd.get("group_by", []):
                    allg[str(g["key"])] = int(g["count"])
                cur = dd.get("meta", {}).get("next_cursor")
                pages += 1
                if not dd.get("group_by"):
                    break
            if not cur:
                groups, complete = allg, True
        except BudgetStop:
            logger.warning(f"budget stop during cursor paging for {tag}; keeping top-200")
    covered = sum(v for k, v in groups.items() if k not in ("unknown", "null", "None"))
    trunc = max(0.0, 1 - covered / total) if total and not complete else 0.0
    return {"groups": groups, "meta_count": total, "groups_count": gcount, "truncated_share": trunc,
            "complete": complete}


# ------------------------------------------------------------------ sources
SRC_FILE = ROOT / "cache" / "source_profiles.json"
SRC: dict[str, dict] = json.loads(SRC_FILE.read_text()) if SRC_FILE.exists() else {}
_SRC_LOCK = threading.Lock()


def _label(s: dict) -> dict:
    c: Counter = Counter()
    dom: Counter = Counter()
    for t in s.get("topics") or []:
        f = (t.get("field") or {}).get("display_name")
        if f:
            c[f] += t.get("count", 0) or 0
        dn = (t.get("domain") or {}).get("display_name")
        if dn:
            dom[dn] += t.get("count", 0) or 0
    tot = sum(c.values())
    top, share = (c.most_common(1)[0] if c else (None, 0))
    share = share / tot if tot else 0.0
    ok = bool(tot) and s.get("type") != "repository" and share >= 0.40
    return {"field": top if ok else None, "top_field": top, "share": round(share, 4), "type": s.get("type"),
            "name": s.get("display_name"), "profile": dict(c), "domains": dict(dom)}


def lookup_sources(ids: list[str], tag: str = "source_lookup", workers: int = 4) -> None:
    todo = sorted({i.split("/")[-1] for i in ids if i} - set(SRC))
    if not todo:
        return
    batch = 100

    def one(ch: list[str]) -> list[dict]:
        p = {"filter": "openalex_id:" + "|".join(ch), "per_page": len(ch), "select": "id,type,topics,display_name"}
        try:
            return get("/sources", p, tag)["results"]
        except (ValueError, RuntimeError):
            out = []
            for j in range(0, len(ch), 50):
                sub = ch[j:j + 50]
                out += get("/sources", {"filter": "openalex_id:" + "|".join(sub), "per_page": len(sub),
                                        "select": "id,type,topics,display_name"}, tag)["results"]
            return out

    chunks = [todo[i:i + batch] for i in range(0, len(todo), batch)]
    with ThreadPoolExecutor(workers) as ex:
        for res in ex.map(one, chunks):
            with _SRC_LOCK:
                for s in res:
                    SRC[s["id"].split("/")[-1]] = _label(s)
    with _SRC_LOCK:
        for s in todo:
            SRC.setdefault(s, {"field": None, "top_field": None, "share": 0, "type": None, "name": None,
                               "profile": {}, "domains": {}})
        SRC_FILE.write_text(json.dumps(SRC))


def src_field(sid: str) -> str | None:
    rec = SRC.get(str(sid).split("/")[-1])
    return rec["field"] if rec else None
