#!/usr/bin/env python3
"""STEP 7d: second, stricter verification of curated-list items with a stronger model.

Why: the hand check found list-specific errors from the cheap primary model (e.g. Gartner 'Micro Fuel Cells'
judged 'same' as 'Microbial fuel cell'; Nature Methods 'Next-generation DNA sequencing' judged 'same' as the
generic 'DNA sequencing'). Lists are the scarcest O5 evidence, so every list item is re-judged by
openai/gpt-4.1-mini with direction-explicit labels (item_is_more_specific / item_is_more_general; a first v2 run with
narrower_entry/broader_entry labels showed this model flipping the direction), and recall is widened
with MiniLM candidates down to cosine 0.65 (top 8). s8 uses these v2 verdicts for list links; v1 verdicts stay
in match_verifications for the v1-vs-v2 agreement statistic.
"""
from __future__ import annotations

import asyncio
import json

import numpy as np
import pandas as pd
from loguru import logger

from common import OUT, WORK, setup_logging
from llm import LLM, BudgetStop
from s7_verify import ACCEPT, SRC_NAME, kappa

MODEL = "openai/gpt-4.1-mini"
MODEL_RF = "google/gemini-2.5-flash-lite"   # Research Fronts items (many, long phrases): cheap model, same strict prompt
SYSTEM = (
    "You link items from curated yearly lists of scientific/technological breakthroughs to concepts of a research-"
    "concept vocabulary. For EACH candidate concept choose ONE label describing the LIST ITEM relative to the CONCEPT:\n"
    "- same: the item names exactly this concept (synonym/plural/spelling variant)\n"
    "- item_is_more_specific: the item is a specific variant, generation, application, instance or result of the "
    "concept. Example: item 'Next-generation DNA sequencing' vs concept 'DNA sequencing' -> item_is_more_specific; "
    "item 'Super-resolution microscopy' vs concept 'Microscopy' -> item_is_more_specific\n"
    "- item_is_more_general: the item is a broader area or family that contains the concept. Example: item "
    "'Gene-editing nucleases' vs concept 'Zinc finger nuclease' -> item_is_more_general\n"
    "- related: topically related only, or a different technology with a similar name (e.g. item 'Micro fuel cells' "
    "(miniature fuel cells for devices) vs concept 'Microbial fuel cell' -> related)\n"
    "- different: unrelated or another sense of the word\n"
    'Return JSON only: {"judgements": [{"candidate_id": "<id>", "label": "<one of the five>", "confidence": <0-1>}]}')
MAP = {"same": "same", "item_is_more_specific": "narrower_entry", "item_is_more_general": "broader_entry",
       "related": "related", "different": "different"}


def main_sync() -> None:
    from sentence_transformers import SentenceTransformer
    k = pd.read_parquet(WORK / "concept_keys.parquet")
    ck = k[k.label.notna()].reset_index(drop=True)
    emb = np.load(WORK / "concept_label_emb.npy").astype(np.float32)
    e = pd.read_parquet(WORK / "entries.parquet")
    le = e[e.family == "lists"].reset_index(drop=True)
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    t1 = le.label.fillna("").tolist()
    t2 = (le.label.fillna("") + ". " + le.descriptor.fillna("").str[:200]).tolist()
    S = np.maximum(model.encode(t1, batch_size=256, normalize_embeddings=True) @ emb.T,
                   model.encode(t2, batch_size=256, normalize_embeddings=True) @ emb.T)
    c = pd.read_parquet(WORK / "candidates.parquet")
    c = c[~c.methods.map(lambda m: list(m) == ["embed065"])]
    have = set(zip(c.entry_id, c.openalex_id))
    new = []
    for i, eid in enumerate(le.entry_id):
        for j in np.argsort(-S[i])[:8]:
            if S[i, j] >= 0.65 and (eid, ck.openalex_id[j]) not in have:
                new.append({"entry_id": eid, "openalex_id": ck.openalex_id[j], "methods": ["embed065"], "score": float(S[i, j])})
    c = pd.concat([c, pd.DataFrame(new)], ignore_index=True)
    c.to_parquet(WORK / "candidates.parquet", index=False)
    logger.info(f"added {len(new)} embed065 candidates for list items")
    asyncio.run(verify(c, e, k))


async def verify(c: pd.DataFrame, e: pd.DataFrame, k: pd.DataFrame) -> None:
    ks = k.set_index("openalex_id")
    es = e.set_index("entry_id", drop=False)
    lc = c[c.entry_id.isin(set(e[e.family == "lists"].entry_id))]
    llm = LLM(concurrency=16)
    rows = []

    async def one(eid: str, g: pd.DataFrame) -> None:
        en = es.loc[eid]
        g = g.sort_values("score", ascending=False)
        # keep all non-embedding candidates first, then fill with embedding candidates up to 8
        pri = g[~g.methods.map(lambda m: set(m) <= {"embed", "embed065"})]
        rest = g[g.methods.map(lambda m: set(m) <= {"embed", "embed065"})]
        g = pd.concat([pri, rest]).head(8)
        lines = [f"LIST: {SRC_NAME.get(en.source, en.source)} ({int(en.year)})", f"LIST ITEM: {en.label}"]
        if isinstance(en.descriptor, str) and en.descriptor:
            lines.append(f"ITEM DESCRIPTION: {en.descriptor[:300]}")
        lines.append("CANDIDATE CONCEPTS:")
        for oid in g.openalex_id:
            r = ks.loc[oid]
            desc = r.description if isinstance(r.description, str) else ""
            lines.append(f"- id={oid} | {r.label} | {desc[:110]}")
        try:
            model = MODEL_RF if en.source == "research_fronts" else MODEL
            d, meta = await llm.json_call(task="verify_lists_v2", model=model, system=SYSTEM, user="\n".join(lines),
                                          max_tokens=600)
        except BudgetStop as ex:
            logger.error(f"budget stop: {ex}")
            return
        js = {str(j.get("candidate_id", "")).replace("id=", "").strip(): j for j in (d or {}).get("judgements", [])
              if isinstance(j, dict)}
        for oid, m in zip(g.openalex_id, g.methods):
            j = js.get(oid, {})
            rel = MAP.get(j.get("label") or j.get("relation"))
            rows.append({"entry_id": eid, "openalex_id": oid, "task": "verify_lists_v2", "model": model, "relation": rel,
                         "confidence": j.get("confidence"), "methods": list(m), "status": "ok" if rel else "unparsed",
                         "prompt_hash": meta["prompt_hash"], "cost": meta["cost"] / max(1, len(g))})

    await asyncio.gather(*(one(eid, g) for eid, g in lc.groupby("entry_id")))
    llm.close()
    v = pd.read_parquet(WORK / "verifications.parquet")
    v = pd.concat([v[v.task != "verify_lists_v2"], pd.DataFrame(rows)], ignore_index=True)
    v.to_parquet(WORK / "verifications.parquet", index=False)
    v1 = v[(v.task == "verify") & v.entry_id.isin(lc.entry_id)].drop_duplicates(["entry_id", "openalex_id"])
    v2 = pd.DataFrame(rows)
    j = v1.merge(v2, on=["entry_id", "openalex_id"], suffixes=("_1", "_2")).dropna(subset=["relation_1", "relation_2"])
    a = ["accept" if x in ACCEPT else "reject" for x in j.relation_1]
    b = ["accept" if x in ACCEPT else "reject" for x in j.relation_2]
    j = j[~j.entry_id.str.startswith("research_fronts")]   # v1-vs-v2 comparison only where v2 used the second model
    st = {"n_pairs": len(j), "v1_model": "google/gemini-2.5-flash-lite", "v2_model": MODEL,
          "raw_agreement_5class": float((j.relation_1 == j.relation_2).mean()),
          "kappa_5class": kappa(j.relation_1.tolist(), j.relation_2.tolist()),
          "raw_agreement_accept": float(np.mean([x == y for x, y in zip(a, b)])), "kappa_accept": kappa(a, b),
          "v2_accepted_pairs": int(v2.relation.isin(ACCEPT).sum()), "v2_same_pairs": int((v2.relation == "same").sum())}
    agr = json.loads((OUT / "llm_agreement.json").read_text())
    agr["lists_v1_vs_v2"] = st
    (OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
    logger.info(f"lists v2 done ${llm.spent:.4f}: {st}")


if __name__ == "__main__":
    setup_logging("s7d_lists_v2")
    main_sync()
