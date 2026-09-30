#!/usr/bin/env python3
"""STEP 1: map each level-1 OpenAlex concept to one of the 26 OpenAlex fields (11-36) or 'multi'.

Two models from different families label all level-1 concepts (batches of 50). Disagreements are written to
work/crosswalk_disagreements.csv and resolved by hand in scripts/crosswalk_manual.json (with a reason each).
Run with --finalize after the manual file exists to write out/crosswalk_level1_to_field.csv.
"""
from __future__ import annotations

import asyncio
import json
import sys

import pandas as pd
from loguru import logger

from common import OUT, ROOT, WORK, setup_logging
from llm import LLM

MODELS = ["google/gemini-2.5-flash-lite", "openai/gpt-4.1-nano"]
MANUAL = ROOT / "scripts" / "crosswalk_manual.json"
SYSTEM = ("You map research-area concepts to the OpenAlex/Scopus ASJC field taxonomy. Return JSON only: "
          '{"mappings": [{"id": "<concept id>", "field_id": <int 11-36> or "multi", "why": "<=8 words"}]}. '
          "Pick the single field where the bulk of the concept's literature is published. Use \"multi\" only if "
          "no field plausibly holds most of it.")


def _prompt(batch: pd.DataFrame, fields: pd.DataFrame) -> str:
    fl = "\n".join(f"{r.fid}: {r.display_name}" for r in fields.itertuples())
    items = "\n".join(f"- id={r.openalex_id} | {r.display_name} | parent: {', '.join(r.parents) or 'none'} | "
                      f"{str(r.description if isinstance(r.description, str) else '')[:90]}" for r in batch.itertuples())
    return f"FIELDS:\n{fl}\n\nCONCEPTS (level-1 OpenAlex concepts with their level-0 parent):\n{items}\n\nMap every concept."


async def label() -> pd.DataFrame:
    c = pd.read_parquet(WORK / "concepts.parquet")
    l1 = c[c.level == 1].copy()
    l1["parents"] = l1.ancestors.apply(lambda a: [x["display_name"] for x in a if x["level"] == 0])
    fields = pd.read_csv(WORK / "openalex_fields.csv").sort_values("fid")
    llm = LLM(concurrency=8)
    out = {m: {} for m in MODELS}

    async def run(m: str, b: pd.DataFrame) -> None:
        d, meta = await llm.json_call(task="crosswalk", model=m, system=SYSTEM, user=_prompt(b, fields), max_tokens=4000)
        for x in (d or {}).get("mappings", []):
            out[m][str(x.get("id"))] = (x.get("field_id"), x.get("why"))

    batches = [l1.iloc[i:i + 50] for i in range(0, len(l1), 50)]
    await asyncio.gather(*(run(m, b) for m in MODELS for b in batches))
    for m in MODELS:   # re-ask for items a model skipped, in small batches
        miss = l1[~l1.openalex_id.isin(out[m].keys())]
        if len(miss):
            logger.info(f"{m}: re-asking {len(miss)} skipped concepts")
            await asyncio.gather(*(run(m, miss.iloc[i:i + 10]) for i in range(0, len(miss), 10)))
    llm.close()
    l1["field_a"] = l1.openalex_id.map(lambda i: out[MODELS[0]].get(i, (None, None))[0])
    l1["why_a"] = l1.openalex_id.map(lambda i: out[MODELS[0]].get(i, (None, None))[1])
    l1["field_b"] = l1.openalex_id.map(lambda i: out[MODELS[1]].get(i, (None, None))[0])
    l1["why_b"] = l1.openalex_id.map(lambda i: out[MODELS[1]].get(i, (None, None))[1])
    def _norm(v):
        if v is None or (isinstance(v, float) and v != v):
            return None
        sv = str(v).strip().lower()
        try:
            return str(int(float(sv)))
        except ValueError:
            return sv
    l1["field_a"] = l1.field_a.map(_norm)
    l1["field_b"] = l1.field_b.map(_norm)
    l1["agree"] = l1.field_a.notna() & (l1.field_a == l1.field_b)
    logger.info(f"level-1 concepts {len(l1)}; missing a={l1.field_a.isna().sum()} b={l1.field_b.isna().sum()}; "
                f"agreement {l1.agree.mean():.3f}; LLM spend so far ${llm.spent:.4f}")
    keep = ["openalex_id", "display_name", "parents", "description", "field_a", "why_a", "field_b", "why_b", "agree"]
    l1[keep].to_csv(WORK / "crosswalk_raw.csv", index=False)
    l1[~l1.agree][keep].to_csv(WORK / "crosswalk_disagreements.csv", index=False)
    return l1


def finalize() -> None:
    raw = pd.read_csv(WORK / "crosswalk_raw.csv")
    manual = json.loads(MANUAL.read_text()) if MANUAL.exists() else {}
    fields = pd.read_csv(WORK / "openalex_fields.csv").set_index("fid")["display_name"].to_dict()
    rows = []
    for r in raw.itertuples():
        if r.openalex_id in manual:
            f, how, why = manual[r.openalex_id]["field"], "manual", manual[r.openalex_id]["reason"]
        elif r.agree:
            f, how, why = r.field_a, "both_models_agree", r.why_a
        else:
            raise SystemExit(f"unresolved disagreement {r.openalex_id} {r.display_name}")
        f = "multi" if str(f) == "multi" else int(float(f))
        rows.append({"openalex_id": r.openalex_id, "display_name": r.display_name, "level0_parents": r.parents,
                     "field_id": f, "field_name": fields.get(f, "multi") if f != "multi" else "multi",
                     "decided_by": how, "reason": why, "model_a": r.field_a, "model_b": r.field_b})
    df = pd.DataFrame(rows)
    df.to_csv(OUT / "crosswalk_level1_to_field.csv", index=False)
    logger.info(f"crosswalk written: {df.decided_by.value_counts().to_dict()}; multi={int((df.field_id == 'multi').sum())}")


if __name__ == "__main__":
    setup_logging("s1_crosswalk")
    if "--finalize" in sys.argv:
        finalize()
    else:
        asyncio.run(label())
