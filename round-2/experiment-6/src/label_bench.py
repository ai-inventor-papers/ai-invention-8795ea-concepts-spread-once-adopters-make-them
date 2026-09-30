#!/usr/bin/env python3
"""Step 3.2: LLM sense labels for the grounding benchmark (OpenRouter; running cost total, hard stop at the cap,
whole batch stops on the first 'AI Inventor per-run OpenRouter budget' refusal).
Usage: python label_bench.py --model M --n N --out benchmark/labels_<tag>.csv"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd
from loguru import logger
from openai import AsyncOpenAI, PermissionDeniedError, APIError

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import BENCH, LOGS, OPENROUTER_CAP_USD, RES  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "labels.log", rotation="30 MB", level="DEBUG")

PROMPT = """You check whether a scientific paper title uses a term in a specific sense.
Concept: "{name}"
Meaning of the concept: {desc}
Paper title: "{title}"
Does this title refer to this concept in the meaning given above (not a different sense of the same words, and not an accidental word sequence)?
Answer only with JSON: {{"label": "yes"}} or {{"label": "no"}} or {{"label": "unsure"}}."""
COST_FILE = RES / "openrouter_cost.json"


def _load_cost() -> dict:
    return json.loads(COST_FILE.read_text()) if COST_FILE.exists() else {"total_usd": 0.0, "calls": 0, "by_model": {}}


async def main_async(args) -> None:
    pairs = pd.read_csv(BENCH / "bench_pairs.csv")
    pairs = pairs.head(args.n) if args.n else pairs
    out_path = Path(args.out)
    done = pd.read_csv(out_path) if out_path.exists() else pd.DataFrame(columns=["pair_id", "label", "raw", "cost"])
    todo = pairs[~pairs.pair_id.isin(done.pair_id)]
    cost = _load_cost()
    client = AsyncOpenAI(base_url=os.environ["OPENROUTER_BASE_URL"], api_key=os.environ["OPENROUTER_API_KEY"])
    sem = asyncio.Semaphore(12)
    stop = {"flag": False}
    rows = []

    async def one(r) -> None:
        async with sem:
            if stop["flag"] or cost["total_usd"] >= OPENROUTER_CAP_USD:
                stop["flag"] = True
                return
            desc = r.description if isinstance(r.description, str) and r.description else "(no description)"
            msg = PROMPT.format(name=r["name"], desc=desc, title=r.title)
            for attempt in range(3):
                try:
                    resp = await client.chat.completions.create(model=args.model, temperature=0, max_tokens=20,
                                                                messages=[{"role": "user", "content": msg}],
                                                                extra_body={"usage": {"include": True}}, timeout=60)
                    break
                except PermissionDeniedError as e:
                    if "AI Inventor per-run OpenRouter budget" in str(e):
                        logger.error("phase budget refused -> stopping whole batch")
                        stop["flag"] = True
                        return
                    raise
                except APIError as e:
                    logger.warning(f"retry {attempt}: {e!r}"[:200])
                    await asyncio.sleep(2 + 3 * attempt)
            else:
                return
            if stop["flag"]:
                return
            txt = (resp.choices[0].message.content or "").strip()
            m = re.search(r'"label"\s*:\s*"(yes|no|unsure)"', txt.lower())
            c = float(getattr(resp, "usage", None) and (resp.usage.model_extra or {}).get("cost", 0.0) or 0.0)
            cost["total_usd"] += c; cost["calls"] += 1
            cost["by_model"][args.model] = cost["by_model"].get(args.model, 0.0) + c
            rows.append({"pair_id": r.pair_id, "label": m.group(1) if m else "unparsed", "raw": txt[:80], "cost": c})
            logger.debug(f"{r.pair_id} | {r['name']} | {r.title[:80]} -> {txt[:40]}")
    await asyncio.gather(*(one(r) for _, r in todo.iterrows()), return_exceptions=False)
    res = pd.concat([done, pd.DataFrame(rows)], ignore_index=True)
    res.to_csv(out_path, index=False)
    COST_FILE.write_text(json.dumps(cost, indent=1))
    logger.info(f"{args.model}: labelled {len(rows)} new ({len(res)} total); run cost ${cost['total_usd']:.4f}; "
                f"labels {res.label.value_counts().to_dict()}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=0)
    ap.add_argument("--out", required=True)
    asyncio.run(main_async(ap.parse_args()))
