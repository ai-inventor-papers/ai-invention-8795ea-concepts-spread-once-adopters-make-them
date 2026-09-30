"""Budgeted async OpenRouter client (EXP5 llm.py, copied; only paths and the cap changed).

* every call's usage.cost is appended to llm_cost_log.csv and summed; hard stop at COST_CAP (USD);
* the first HTTP 403 'AI Inventor per-run OpenRouter budget' cancels every queued / in-flight call;
* responses are cached on disk (scan/llm_cache/<sha1>.json, keyed by model+messages, no secrets)."""
from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import time

import aiohttp

from common import EXP5, RES, ROOT

COST_CAP = 3.00                      # hard cap for this artifact (USD, ledger total)
LEDGER = RES / "llm_cost_log.csv"
CACHE = ROOT / "llm_cache"
CACHE.mkdir(parents=True, exist_ok=True)
EXP5_CACHE = EXP5 / "scan/llm_cache"   # read-only lookup: identical EXP5 calls are re-used, never re-paid


class BudgetStop(Exception):
    pass


class LLM:
    def __init__(self, concurrency: int = 16, cap: float = COST_CAP):
        self.base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.concurrency = concurrency
        self._sem = None
        self._loop = None
        self.cap = cap
        self.stopped = False
        self.spent = self._ledger_total()
        self.n_calls = 0
        self.cache_hits = 0
        self.cache_hits_exp5 = 0

    @property
    def sem(self) -> asyncio.Semaphore:
        """One semaphore per running event loop (each asyncio.run() gets a fresh one)."""
        loop = asyncio.get_running_loop()
        if self._sem is None or self._loop is not loop:
            self._sem, self._loop = asyncio.Semaphore(self.concurrency), loop
        return self._sem

    @staticmethod
    def _ledger_total() -> float:
        if not LEDGER.exists():
            return 0.0
        with LEDGER.open() as f:
            return sum(float(r["cost"] or 0) for r in csv.DictReader(f))

    def _log(self, model: str, tag: str, usage: dict) -> None:
        new = not LEDGER.exists()
        with LEDGER.open("a", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["time", "model", "tag", "prompt_tokens", "completion_tokens", "cost"])
            w.writerow([time.strftime("%H:%M:%S"), model, tag, usage.get("prompt_tokens"),
                        usage.get("completion_tokens"), usage.get("cost", 0)])

    async def chat(self, session: aiohttp.ClientSession, model: str, messages: list[dict], tag: str,
                   max_tokens: int = 800, temperature: float = 0.0) -> str | None:
        ck = CACHE / (hashlib.sha1(json.dumps([model, messages, temperature]).encode()).hexdigest() + ".json")
        if ck.exists():
            self.cache_hits += 1
            return json.loads(ck.read_text())["content"]
        ck5 = EXP5_CACHE / ck.name
        if ck5.exists():
            self.cache_hits_exp5 += 1
            return json.loads(ck5.read_text())["content"]
        if self.stopped:
            return None
        async with self.sem:
            if self.stopped or self.spent >= self.cap:  # re-check after getting the slot
                self.stopped = True
                return None
            body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature,
                    "response_format": {"type": "json_object"}, "usage": {"include": True}}
            for k in range(4):
                try:
                    async with session.post(f"{self.base}/chat/completions", json=body,
                                            headers={"Authorization": f"Bearer {self.key}"},
                                            timeout=aiohttp.ClientTimeout(total=120)) as r:
                        txt = await r.text()
                        if r.status == 403 and "AI Inventor per-run OpenRouter budget" in txt:
                            self.stopped = True
                            raise BudgetStop(txt[:200])
                        if r.status != 200:
                            await asyncio.sleep(2 + 3 * k)
                            continue
                        d = json.loads(txt)
                        usage = d.get("usage", {}) or {}
                        self.spent += float(usage.get("cost") or 0)
                        self.n_calls += 1
                        self._log(model, tag, usage)
                        content = d["choices"][0]["message"]["content"] or ""
                        ck.write_text(json.dumps({"content": content}))
                        if self.spent >= self.cap:
                            self.stopped = True
                        return content
                except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError, KeyError):
                    await asyncio.sleep(2 + 3 * k)
            return None


def parse_json(txt: str | None):
    if not txt:
        return None
    try:
        return json.loads(txt)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", txt, re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None


SYSTEM = ("You are an expert scientific indexer. For each item you get a scientific CONCEPT (name and a short "
          "definition) and the TITLE of a publication that contains the concept's name (or an alias). Decide whether "
          "the title really refers to THIS concept in THIS sense (not a homonym, not a different technical meaning, "
          "not an accidental word sequence). Answer strictly as JSON: {\"labels\": [{\"id\": <id>, "
          "\"refers_to_concept\": true|false, \"confidence\": <0..1>}, ...]} with one entry per item.")


def batch_prompt(items: list[dict]) -> list[dict]:
    lines = []
    for it in items:
        d = it.get("description")
        d = d.strip() if isinstance(d, str) and d.strip() else "(no definition available)"
        lines.append(json.dumps({"id": it["id"], "concept": it["name"], "definition": d[:200],
                                 "title": it["title"][:300]}, ensure_ascii=False))
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Items (one JSON object per line):\n" + "\n".join(lines)}]
