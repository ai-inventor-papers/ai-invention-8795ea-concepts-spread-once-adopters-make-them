#!/usr/bin/env python3
"""S5: concept TYPE labels (method | object | property | topic) + generic flag, for the EXP5 frame and the cohort.

M1 = google/gemini-2.5-flash-lite (temperature 0, 20 concepts per call) labels every concept.
Benchmark: 300 concepts (50 per analysis group, both frames) are labelled by M2 = openai/gpt-4.1-mini (other family);
the executor agent reads 60 of them (15 per M1 class) BLIND to both models' labels (results/type_gold_sheet.csv ->
results/type_gold_labels.csv) and the gate (M1 precision >= 0.85 for method AND object) is evaluated.

Usage: python s5_typing.py exp5|cohort|bench|sheet|gate [--prompt v1|v2] [--limit N]"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import aiohttp
import numpy as np
import pandas as pd

from common import DATA, EXP5, INPUTS, RES, add_deviation, jdump, load_frame, read_parquet_parts, setup_logger
from llmc import LLM, BudgetStop, parse_json

logger = setup_logger("s5_typing")
M1 = "google/gemini-2.5-flash-lite"
M2 = "openai/gpt-4.1-mini"
BS = 20
TYPES = ["method", "object", "property", "topic"]
ANALYSIS_GROUP = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med", "PHYS": "PHYS",
                  "LIFEENV": "LIFEENV", "SOC": "SOC", "MATHDEC": "MATHDEC"}

SYSTEM_V1 = (
    "You are an expert scientific indexer. For each scientific CONCEPT (name, short definition, ontology level, and up to "
    "3 titles of early papers that use it) assign exactly one TYPE:\n"
    "- method: a technique, tool, algorithm, instrument, assay, software, procedure or model class used to DO research "
    "(e.g. 'Random forest', 'CRISPR interference', 'Mass cytometry', 'Difference in differences').\n"
    "- object: a thing that is studied: material, organism, disease, device studied as an object, molecule, gene, "
    "compound, phenomenon-entity, place or population (e.g. 'Graphene', 'Zika virus', 'Perovskite solar cell', "
    "'Long non-coding RNA').\n"
    "- property: a measure, statistic, index, quantity, theory, law, principle or property (e.g. 'Coefficient of "
    "variation', 'Band gap', 'Social capital theory').\n"
    "- topic: a field, research area, application domain or problem area (e.g. 'Smart city', 'Precision agriculture').\n"
    "Also set generic = 1 if the term was in common scientific use well BEFORE the given onset year (an established, "
    "general term such as 'Exponential growth' or 'Coefficient of variation'), else 0; and a confidence in [0, 1].\n"
    "Answer strictly as JSON: {\"labels\": [{\"id\": <id>, \"type\": \"method|object|property|topic\", "
    "\"generic\": 0|1, \"confidence\": <0..1>}, ...]} with one entry per concept.")


def batch_messages(items: list[dict], system: str) -> list[dict]:
    lines = []
    for it in items:
        lines.append(json.dumps({"id": it["id"], "concept": it["name"], "definition": it["desc"][:200],
                                 "level": it["level"], "onset_year": it["t0"],
                                 "early_titles": [t[:200] for t in it["titles"][:3]]}, ensure_ascii=False))
    return [{"role": "system", "content": system},
            {"role": "user", "content": "Concepts (one JSON object per line):\n" + "\n".join(lines)}]


def lex_desc() -> pd.DataFrame:
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "name", "level", "description",
                                                                  "wd_description"])
    lex["desc"] = [(d if isinstance(d, str) and d.strip() else (w if isinstance(w, str) and w.strip() else ""))
                   for d, w in zip(lex.description, lex.wd_description)]
    return lex


def exp5_items() -> list[dict]:
    fr = load_frame()
    lex = lex_desc()
    rs = read_parquet_parts(EXP5 / "scan/reservoir", columns=["ci", "h", "year", "tagstate", "title"])
    rs = rs[(rs.tagstate == 1) & rs.ci.isin(set(fr.ci))].merge(fr[["ci", "t0"]], on="ci")
    rs["inwin"] = (rs.year >= rs.t0) & (rs.year <= rs.t0 + 2)
    rs = rs.sort_values(["ci", "inwin", "h"], ascending=[True, False, True])
    titles = {ci: g.title.head(3).tolist() for ci, g in rs.groupby("ci")}
    return [{"ci": int(r.ci), "name": r.name, "desc": lex.desc.iat[r.ci], "level": int(lex.level.iat[r.ci]),
             "t0": int(r.t0), "titles": titles.get(r.ci, []), "frame": "exp5", "group": r.group} for r in fr.itertuples()]


def cohort_items() -> list[dict]:
    cf = pd.read_csv(DATA / "cohort_candidates.csv")
    lex = lex_desc()
    em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "work_id", "tagstate", "title"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))].merge(cf[["ci", "t0"]], on="ci")
    em = em[(em.year >= em.t0) & (em.year <= em.t0 + 2)]
    em["h"] = [int(hashlib.sha1(f"{w}".encode()).hexdigest()[:12], 16) for w in em.work_id]
    em = em.sort_values(["ci", "h"])
    titles = {ci: g.title.head(3).tolist() for ci, g in em.groupby("ci")}
    return [{"ci": int(r.ci), "name": r.name, "desc": lex.desc.iat[r.ci], "level": int(lex.level.iat[r.ci]),
             "t0": int(r.t0), "titles": titles.get(r.ci, []), "frame": "cohort", "group": r.group}
            for r in cf.itertuples()]


def label(items: list[dict], model: str, system: str, tag: str, llm: LLM, bs: int = BS) -> dict:
    for k, it in enumerate(items):
        it["id"] = k
    batches = [items[i:i + bs] for i in range(0, len(items), bs)]
    out: dict = {}

    async def run():
        async with aiohttp.ClientSession() as sess:
            async def one(b):
                if llm.stopped:
                    return
                try:
                    txt = await llm.chat(sess, model, batch_messages(b, system), tag, max_tokens=45 * len(b) + 100)
                except BudgetStop as e:
                    logger.error(f"budget refusal -> batch stopped: {e}")
                    return
                d = parse_json(txt)
                ids_b = {it["id"] for it in b}
                for x in (d or {}).get("labels", []) if isinstance(d, dict) else []:
                    try:
                        t = str(x["type"]).strip().lower()
                        if t not in TYPES:
                            continue
                        i = int(x["id"])
                        if i in ids_b:
                            out[i] = (t, int(x.get("generic", 0)), float(x.get("confidence", math.nan)))
                    except (KeyError, TypeError, ValueError):
                        continue
            await asyncio.gather(*(one(b) for b in batches))
    asyncio.run(run())
    return {items[i]["ci"]: v for i, v in out.items() if 0 <= i < len(items)}


def system_prompt(version: str) -> str:
    if version == "v1":
        return SYSTEM_V1
    return (RES / "type_prompt_v2.txt").read_text()


def cmd_label(frame: str, version: str, limit: int) -> None:
    items = exp5_items() if frame == "exp5" else cohort_items()
    if limit:
        items = items[:limit]
    llm = LLM(concurrency=24)
    logger.info(f"{frame}: {len(items)} concepts, {math.ceil(len(items)/BS)} calls, spent so far ${llm.spent:.3f}")
    lab = label(items, M1, system_prompt(version), f"type:{frame}:{version}", llm)
    miss = [dict(it) for it in items if it["ci"] not in lab]
    if miss:  # one retry for unparsed concepts, in new batches of 10 (different messages -> a fresh call)
        lab.update(label(miss, M1, system_prompt(version), f"type:{frame}:{version}:retry", llm, bs=10))
        logger.info(f"retry: {len(miss)} unparsed -> {sum(it['ci'] in lab for it in miss)} labelled")
    df = pd.DataFrame([{"ci": it["ci"], "frame": frame, "group": it["group"], "name": it["name"], "t0": it["t0"],
                        "n_titles": len(it["titles"]), "type_m1": lab.get(it["ci"], (None,))[0],
                        "generic_m1": lab.get(it["ci"], (None, None))[1],
                        "conf_m1": lab.get(it["ci"], (None, None, None))[2]} for it in items])
    df.to_csv(DATA / f"types_{frame}_{version}.csv", index=False)
    logger.info(f"{frame}: parsed {df.type_m1.notna().mean():.3%}; types {df.type_m1.value_counts().to_dict()}; "
                f"generic {df.generic_m1.mean():.3f}; spent ${llm.spent:.3f}; calls {llm.n_calls}; "
                f"cache hits {llm.cache_hits}")


def bench_set() -> pd.DataFrame:
    """300 concepts, 50 per analysis group (both frames pooled), seeded."""
    e = pd.read_csv(DATA / "types_exp5_v1.csv")
    c = pd.read_csv(DATA / "types_cohort_v1.csv")
    allc = pd.concat([e, c], ignore_index=True)
    allc["agroup"] = allc.group.map(ANALYSIS_GROUP)
    pick = []
    for g, d in allc.groupby("agroup"):
        pick.append(d.sample(min(50, len(d)), random_state=20260929))
    return pd.concat(pick).reset_index(drop=True)


def cmd_bench(version: str) -> None:
    b = bench_set()   # the SAME 300 concepts for every prompt version (sampled once from the v1 label files)
    if version != "v1":
        lab = pd.concat([pd.read_csv(DATA / f"types_{f}_{version}.csv") for f in ("exp5", "cohort")])
        b = b.drop(columns=["type_m1", "generic_m1", "conf_m1"]).merge(
            lab[["ci", "frame", "type_m1", "generic_m1", "conf_m1"]], on=["ci", "frame"], how="left")
    items_all = {it["ci"]: it for it in exp5_items() + cohort_items()}
    items = [dict(items_all[ci]) for ci in b.ci]
    llm = LLM(concurrency=16)
    lab = label(items, M2, system_prompt(version), f"type:bench:M2:{version}", llm)
    b["type_m2"] = b.ci.map(lambda c: lab.get(c, (None,))[0])
    b["generic_m2"] = b.ci.map(lambda c: lab.get(c, (None, None))[1])
    b.to_csv(RES / f"type_benchmark_{version}.csv", index=False)
    ok = b.type_m1.notna() & b.type_m2.notna()
    from sklearn.metrics import cohen_kappa_score
    k = float(cohen_kappa_score(b.type_m1[ok], b.type_m2[ok]))
    logger.info(f"bench {version}: n={ok.sum()} kappa M1-M2 = {k:.3f}; agreement {(b.type_m1[ok]==b.type_m2[ok]).mean():.3f};"
                f" spent ${llm.spent:.3f}")


def cmd_sheet(version: str) -> None:
    """60 benchmark concepts, 15 per M1 class, shuffled; the sheet shows NO model label (blind reading)."""
    b = pd.read_csv(RES / f"type_benchmark_{version}.csv")
    pick = []
    for t in TYPES:
        d = b[b.type_m1 == t]
        pick.append(d.sample(min(15, len(d)), random_state=7))
    s = pd.concat(pick).sample(frac=1, random_state=11).reset_index(drop=True)
    items_all = {it["ci"]: it for it in exp5_items() + cohort_items()}
    s["definition"] = [items_all[c]["desc"][:200] for c in s.ci]
    s["titles"] = [" || ".join(t[:150] for t in items_all[c]["titles"][:3]) for c in s.ci]
    s[["ci", "name", "t0", "definition", "titles"]].to_csv(RES / f"type_gold_sheet_{version}.csv", index=False)
    logger.info(f"gold sheet {len(s)} rows (blind)")


def wilson(k: int, n: int) -> list[float]:
    if n == 0:
        return [math.nan, math.nan]
    z = 1.96
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [c - h, c + h]


def cmd_gate(version: str) -> None:
    from sklearn.metrics import cohen_kappa_score
    b = pd.read_csv(RES / f"type_benchmark_{version}.csv")
    g = pd.read_csv(RES / f"type_gold_labels_{version}.csv")
    m = g.merge(b[["ci", "type_m1", "type_m2", "generic_m1", "generic_m2"]], on="ci")
    res = {"version": version, "n_gold": int(len(m)), "per_class": {}}
    for t in TYPES:
        d = m[m.type_m1 == t]
        k = int((d.gold_type == t).sum())
        res["per_class"][t] = {"n_m1": int(len(d)), "correct": k, "precision": k / len(d) if len(d) else math.nan,
                               "wilson95": wilson(k, len(d)),
                               "recall": float(((m.gold_type == t) & (m.type_m1 == t)).sum() / max((m.gold_type == t).sum(), 1))}
    ok = b.type_m1.notna() & b.type_m2.notna()
    res["kappa_m1_m2_300"] = float(cohen_kappa_score(b.type_m1[ok], b.type_m2[ok]))
    res["agree_m1_m2_300"] = float((b.type_m1[ok] == b.type_m2[ok]).mean())
    res["kappa_m1_gold"] = float(cohen_kappa_score(m.gold_type, m.type_m1))
    res["kappa_m2_gold"] = float(cohen_kappa_score(m.gold_type, m.type_m2.fillna("none")))
    res["acc_m1_gold"] = float((m.gold_type == m.type_m1).mean())
    res["acc_m2_gold"] = float((m.gold_type == m.type_m2).mean())
    res["confusion_m1_vs_gold"] = pd.crosstab(m.type_m1, m.gold_type).to_dict()
    res["confusion_m1_vs_m2_300"] = pd.crosstab(b.type_m1[ok], b.type_m2[ok]).to_dict()
    res["method_object_confusion_m1_m2"] = int(((b.type_m1 == "method") & (b.type_m2 == "object")).sum()
                                               + ((b.type_m1 == "object") & (b.type_m2 == "method")).sum())
    if "gold_generic" in m.columns:
        res["generic_agree_m1_gold"] = float((m.gold_generic == m.generic_m1).mean())
    res["gate_pass"] = bool(res["per_class"]["method"]["precision"] >= 0.85
                            and res["per_class"]["object"]["precision"] >= 0.85)
    res["gold_reader"] = "executor agent (LLM), blind to M1/M2 labels; disclosed as not a human annotator"
    jdump(res, RES / f"type_benchmark_{version}.json")
    logger.info(f"gate {version}: {json.dumps({k: res[k] for k in ('kappa_m1_m2_300', 'acc_m1_gold', 'gate_pass')})} "
                f"precision method {res['per_class']['method']['precision']:.3f} object "
                f"{res['per_class']['object']['precision']:.3f}")


def cmd_m2all(version: str) -> None:
    """Gate failed twice (declared fallback): M2 labels every concept M1 put in method / object, both frames;
    within-type tests then use M1 = M2 concepts only. Writes data/concept_types.csv."""
    items_all = {("exp5", it["ci"]): it for it in exp5_items()}
    items_all.update({("cohort", it["ci"]): it for it in cohort_items()})
    lab = pd.concat([pd.read_csv(DATA / f"types_{f}_{version}.csv") for f in ("exp5", "cohort")], ignore_index=True)
    want = lab[lab.type_m1.isin(["method", "object"])]
    llm = LLM(concurrency=24)
    out = {}
    for f in ("exp5", "cohort"):
        its = [dict(items_all[(f, c)]) for c in want[want.frame == f].ci]
        logger.info(f"M2 on {f}: {len(its)} method/object concepts; spent so far ${llm.spent:.3f}")
        r = label(its, M2, system_prompt(version), f"type:m2all:{f}:{version}", llm)
        miss = [dict(it) for it in its if it["ci"] not in r]
        if miss:
            r.update(label(miss, M2, system_prompt(version), f"type:m2all:{f}:{version}:retry", llm, bs=10))
        out.update({(f, c): v for c, v in r.items()})
    lab["type_m2"] = [out.get((f, c), (None,))[0] for f, c in zip(lab.frame, lab.ci)]
    lab["type"] = lab.type_m1
    lab["generic"] = lab.generic_m1.fillna(0).astype(int)
    lab["type_agree"] = lab.type_m1.isin(["method", "object"]) & (lab.type_m1 == lab.type_m2)
    lab["type_version"] = version
    lab[["ci", "frame", "name", "type", "generic", "type_m1", "type_m2", "type_agree", "conf_m1", "type_version"]].to_csv(
        DATA / "concept_types.csv", index=False)
    s = lab[lab.type_m1.isin(["method", "object"])]
    info = {"n_method_object": int(len(s)), "m2_labelled": int(s.type_m2.notna().sum()),
            "agree_share": float(s.type_agree.mean()),
            "agree_by_frame_type": s.groupby(["frame", "type_m1"]).type_agree.mean().round(3).to_dict().__repr__(),
            "llm_spent_total_usd": llm.spent}
    jdump(info, RES / "type_m2all.json")
    logger.info(f"m2all: {info}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd")
    ap.add_argument("--prompt", default="v1")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    if a.cmd in ("exp5", "cohort"):
        cmd_label(a.cmd, a.prompt, a.limit)
    elif a.cmd == "bench":
        cmd_bench(a.prompt)
    elif a.cmd == "sheet":
        cmd_sheet(a.prompt)
    elif a.cmd == "gate":
        cmd_gate(a.prompt)
    elif a.cmd == "m2all":
        cmd_m2all(a.prompt)


if __name__ == "__main__":
    main()
