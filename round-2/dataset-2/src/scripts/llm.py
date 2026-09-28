"""OpenRouter JSON calls with a disk cache, a running cost ledger, a hard $ cap and 403-budget stop."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re

from loguru import logger
from openai import APIStatusError, AsyncOpenAI

from common import CACHE, OUT

CAP_USD = 2.0
LEDGER = OUT / "llm_cost.json"
CACHE_FILE = CACHE / "llm" / "calls.jsonl"
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)


class BudgetStop(Exception):
    pass


class LLM:
    def __init__(self, concurrency: int = 16) -> None:
        self.client = AsyncOpenAI(base_url=os.environ["OPENROUTER_BASE_URL"], api_key=os.environ["OPENROUTER_API_KEY"])
        self.sem = asyncio.Semaphore(concurrency)
        self.stopped: str | None = None
        self.cache: dict[str, dict] = {}
        if CACHE_FILE.exists():
            for line in CACHE_FILE.open():
                r = json.loads(line)
                self.cache[r["key"]] = r
        led = json.loads(LEDGER.read_text()) if LEDGER.exists() else {}
        self.spent = float(led.get("total_usd", 0.0))
        self.by_task: dict[str, dict] = led.get("by_task", {})
        self.fh = CACHE_FILE.open("a")

    def _save_ledger(self) -> None:
        LEDGER.write_text(json.dumps({"cap_usd": CAP_USD, "total_usd": round(self.spent, 6), "by_task": self.by_task,
                                      "stopped": self.stopped}, indent=1))

    async def json_call(self, *, task: str, model: str, system: str, user: str, max_tokens: int = 800) -> tuple[dict | None, dict]:
        key = hashlib.sha256(f"{model}\n{system}\n{user}".encode()).hexdigest()
        if key in self.cache:
            r = self.cache[key]
            return r["parsed"], {"prompt_hash": key, "model": model, "cost": 0.0, "cached": True}
        if self.stopped:
            raise BudgetStop(self.stopped)
        async with self.sem:
            if self.stopped:          # re-check after acquiring the slot
                raise BudgetStop(self.stopped)
            if self.spent >= CAP_USD:
                self.stopped = f"artifact cap ${CAP_USD} reached"
                raise BudgetStop(self.stopped)
            txt, cost, parsed = "", 0.0, None
            for attempt in range(3):
                try:
                    resp = await self.client.chat.completions.create(
                        model=model, temperature=0, max_tokens=max_tokens,
                        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                        response_format={"type": "json_object"}, extra_body={"usage": {"include": True}})
                    txt = resp.choices[0].message.content or ""
                    u = resp.usage
                    cost += float(getattr(u, "cost", 0.0) or (u.model_extra or {}).get("cost", 0.0) or 0.0)
                    parsed = _parse(txt)
                    if parsed is not None:
                        break
                except APIStatusError as e:
                    msg = str(e)
                    if e.status_code == 403 and "AI Inventor per-run OpenRouter budget" in msg:
                        self.stopped = "phase budget exhausted (HTTP 403)"
                        self._save_ledger()
                        raise BudgetStop(self.stopped) from e
                    logger.warning(f"{model} HTTP {e.status_code}: {msg[:200]}")
                    await asyncio.sleep(2 * (attempt + 1))
                except (asyncio.TimeoutError, ValueError, IndexError) as e:
                    logger.warning(f"{model} {type(e).__name__}: {str(e)[:200]}")
                    await asyncio.sleep(2 * (attempt + 1))
            self.spent += cost
            t = self.by_task.setdefault(task, {"calls": 0, "usd": 0.0, "models": {}})
            t["calls"] += 1
            t["usd"] = round(t["usd"] + cost, 6)
            t["models"][model] = t["models"].get(model, 0) + 1
            rec = {"key": key, "task": task, "model": model, "parsed": parsed, "raw": txt[:4000], "cost": cost}
            self.cache[key] = rec
            self.fh.write(json.dumps(rec) + "\n")
            self.fh.flush()
            logger.debug(f"[{task}] {model} cost={cost:.6f} total={self.spent:.4f} out={txt[:300]!r}")
            if t["calls"] % 25 == 0:
                self._save_ledger()
            return parsed, {"prompt_hash": key, "model": model, "cost": cost, "cached": False}

    def close(self) -> None:
        self._save_ledger()
        self.fh.close()


def _parse(txt: str) -> dict | None:
    txt = txt.strip()
    txt = re.sub(r"^```(?:json)?\s*|\s*```$", "", txt)
    try:
        d = json.loads(txt)
        return d if isinstance(d, dict) else {"_list": d}
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}", txt, flags=re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except json.JSONDecodeError:
                return None
    return None
