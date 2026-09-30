#!/usr/bin/env python3
"""S5c: CATEGORICAL concept gate (G2; declared deviation D_gate_v2, adopted BEFORE the freeze because the blind checks
of the boolean gate failed twice: keep-precision 0.37 (M1) and 0.43 (M1 AND M2) vs the executor's blind labels).

G2 = openai/gpt-4.1-mini, temperature 0, 8 phrases per call, the same 20 titles per phrase (seed 7919+ci). The model
names the phrase's CATEGORY; KEEP iff category == 'concept' (and the M1 sense rule still holds: M1 keep).
  eval      run G2 on the 100 executor-labelled phrases (both blind sheets) -> results/gate2_eval.json
  run       run G2 on every M1-kept phrase -> data/gate_g2.csv
  frame     frame_n_concepts.csv = M1 keep AND G2 concept
Usage: python s5_gate2.py eval|run|frame"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, RES, jdump, setup_logger

import s5_gate as g1

logger = setup_logger("s5_gate2")
G2 = "openai/gpt-4.1-mini"
CATS = ["concept", "named_entity", "non_english", "fragment_or_generic", "boilerplate"]
SYSTEM2 = (
    "You are an expert scientific indexer building a vocabulary of scientific CONCEPTS. Each item is a candidate "
    "PHRASE mined automatically from publication titles, with up to 20 titles that contain it. Classify each phrase "
    "into exactly one category:\n"
    "- concept: the phrase itself names one specific scientific or scholarly concept, written in English: a method, "
    "technique, procedure, instrument, device class, material, compound, gene / protein / biomarker, organism / strain "
    "/ virus, disease or condition, physical or biological phenomenon, measure / index / scoring system, theory, or a "
    "well-defined research topic. If the phrase is a truncated piece of a longer established term but in the titles it "
    "always refers to that one concept (e.g. 'coli o104' for E. coli O104:H4), it is still a concept.\n"
    "- named_entity: a proper name rather than a concept: person, place (country, region, district, city, lake, "
    "river, crater, site), organisation or institution, event (a specific outbreak, crisis, war, disaster, typhoon, "
    "earthquake), policy / programme / initiative / law, project / mission / expedition / survey, product / brand / "
    "software release, dataset, telescope or instrument network name, journal / series / section / report title.\n"
    "- non_english: the phrase is not English (e.g. Indonesian, Spanish, French, German, Portuguese words).\n"
    "- fragment_or_generic: a truncated fragment that does not identify one concept, or a generic word combination "
    "that is not a term of art (e.g. 'efficient hydrogen evolution', 'growth of graphene', 'antimicrobial potential', "
    "'ratio and platelet').\n"
    "- boilerplate: title boilerplate or paratext (lecture, session, talks, highlights, listings, report card, "
    "membership information, working paper series).\n"
    "Answer strictly as JSON: {\"labels\": [{\"id\": <id>, \"category\": \"concept|named_entity|non_english|"
    "fragment_or_generic|boilerplate\"}, ...]} with one entry per item.")


def run_g2(items: list[dict], tag: str) -> pd.DataFrame:
    """Reuses the budgeted client and retry rounds of s5_gate (only the system prompt / parsing differ)."""
    import asyncio

    import aiohttp

    from llmc import LLM, BudgetStop, parse_json
    out = []
    todo = list(items)
    for rnd in range(3):
        if not todo:
            break
        llm = LLM(concurrency=24, cap=g1.TOTAL_CAP)
        bs = 8 if rnd == 0 else 4
        batches = [todo[i:i + bs] for i in range(0, len(todo), bs)]

        async def go():
            async with aiohttp.ClientSession() as sess:
                async def one(b):
                    if llm.stopped:
                        return
                    lines = [json.dumps({"id": k, "phrase": it["name"], "titles": it["titles"]}, ensure_ascii=False)
                             for k, it in enumerate(b)]
                    msg = [{"role": "system", "content": SYSTEM2},
                           {"role": "user", "content": "Items (one JSON object per line):\n" + "\n".join(lines)
                            + (f"\n(round {rnd})" if rnd else "")}]
                    try:
                        txt = await llm.chat(sess, G2, msg, f"{tag}_r{rnd}", max_tokens=40 * len(b) + 100)
                    except BudgetStop as e:
                        logger.error(f"budget refusal -> batch stopped: {e}")
                        return
                    d = parse_json(txt)
                    for x in (d.get("labels", []) if isinstance(d, dict) else []):
                        try:
                            k = int(x["id"])
                            c = str(x.get("category", "")).strip()
                            if 0 <= k < len(b) and c in CATS:
                                out.append({"ci": b[k]["ci"], "category": c})
                        except (KeyError, TypeError, ValueError):
                            continue
                await asyncio.gather(*(one(b) for b in batches))
        asyncio.run(go())
        got = {o["ci"] for o in out}
        todo = [it for it in todo if it["ci"] not in got]
        logger.info(f"G2 {tag} round {rnd}: labelled {len(got)}; left {len(todo)}; ledger ${llm.spent:.4f}")
    return pd.DataFrame(out).drop_duplicates("ci")


def main() -> None:
    cmd = sys.argv[1]
    items = {it["ci"]: it for it in g1.items_all()}
    if cmd == "eval":
        lab = pd.concat([pd.DataFrame(json.loads((RES / f).read_text()))[["ci", "executor_keep"]]
                         for f in ("blind_check_labels.json", "blind_check_labels2.json")])
        d = run_g2([items[int(c)] for c in lab.ci], "gate2_eval")
        m = lab.merge(d, on="ci")
        m1 = pd.read_csv(DATA / "gate_m1.csv")[["ci", "keep"]]
        m = m.merge(m1, on="ci")
        m["g2_keep"] = (m.category == "concept") & m.keep.astype(bool)
        tp = int((m.g2_keep & m.executor_keep).sum())
        res = {"n": int(len(m)), "category_counts": m.category.value_counts().to_dict(),
               "keep_precision_vs_executor": float(m[m.g2_keep].executor_keep.mean()),
               "keep_recall_vs_executor": float(tp / max(int(m.executor_keep.sum()), 1)),
               "n_g2_keep": int(m.g2_keep.sum()), "n_executor_keep": int(m.executor_keep.sum()),
               "agreement": float((m.g2_keep == m.executor_keep).mean()),
               "note": "dev evaluation on the 100 executor-labelled phrases (sheets 1 and 2); executor = an LLM agent, "
                       "not a human annotator"}
        jdump(res, RES / "gate2_eval.json")
        logger.info(f"G2 eval: {res}")
        print(m[m.g2_keep != m.executor_keep].to_string())
    elif cmd == "run":
        m1 = pd.read_csv(DATA / "gate_m1.csv")
        todo = [items[int(c)] for c in m1[m1.gated & m1.keep.astype(bool)].ci]
        d = run_g2(todo, "gate2")
        d.to_csv(DATA / "gate_g2.csv", index=False)
        logger.info(f"G2 run: {len(d)} labelled; {d.category.value_counts().to_dict()}")
    elif cmd == "frame":
        on = pd.read_csv(DATA / "frame_n_onset.csv")
        m1 = pd.read_csv(DATA / "gate_m1.csv")
        b = json.loads((RES / "gate_benchmark.json").read_text())
        thr = b.get("sense_share_threshold", 0.8)
        m1 = m1[m1.gated].copy()
        m1["keep"] = g1.keep_rule(m1, thr)
        d = pd.read_csv(DATA / "gate_g2.csv")
        d2 = pd.read_csv(DATA / "gate_m2.csv")[["ci", "type"]].rename(columns={"type": "type_m2"})
        fr = on.merge(m1[["ci", "keep", "specific", "sense_share", "type", "generic", "gloss", "n_home_early",
                          "priority_rank"]], on="ci").merge(d, on="ci", how="left").merge(d2, on="ci", how="left")
        fr["type_agree"] = fr.type == fr.type_m2
        fr["gate_model"] = f"{g1.M1} (sense rule) AND {G2} category == concept (D_gate_v2)"
        n_m1 = int(fr.keep.sum())
        fr = fr[fr.keep & (fr.category == "concept")].drop(columns=["keep"])
        fr.to_csv(DATA / "frame_n_concepts.csv", index=False)
        b["gate_v2"] = {"n_m1_kept": n_m1, "n_final": int(len(fr)), "n_final_main": int((fr.extension == 0).sum()),
                        "g2_categories_on_m1_kept": d.category.value_counts().to_dict(),
                        "eval": json.loads((RES / "gate2_eval.json").read_text())}
        jdump(b, RES / "gate_benchmark.json")
        logger.info(f"frame_n_concepts: {len(fr)} (main {int((fr.extension == 0).sum())})")


if __name__ == "__main__":
    main()
