#!/usr/bin/env python3
"""STEP 7c: LLM verification of candidate links -> work/verifications.parquet (+ out/match_verifications.csv).

Tasks (one call per entry, <=5 candidates shown with descriptions):
  verify  : every list item (all its candidates) and every taxonomy node whose candidates are only fuzzy
            (unique entry text is verified once and the verdict reused across versions of a scheme)
  audit   : 100 random exact/ID-linked entries per source family (precision of accepted-without-LLM links)
  double  : 200 random verify/audit calls re-labelled by a second model from a different family (kappa)
Relation vocabulary (relative to the EXTERNAL ENTRY): same | narrower_entry | broader_entry | related | different.
Accepted: same, narrower_entry, broader_entry.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import random
import sys

import pandas as pd
from loguru import logger

from common import OUT, WORK, setup_logging
from llm import LLM, BudgetStop

PRIMARY = "google/gemini-2.5-flash-lite"
SECOND = "openai/gpt-4.1-mini"
MAX_VERIFY_CALLS = 4000
SYSTEM = (
    "You link entries from external scientific lists/classifications to concepts of a research-concept vocabulary "
    "(OpenAlex/Microsoft Academic 'fields of study'). For EACH candidate concept decide how the ENTRY relates to it:\n"
    "- same: entry and concept denote the same topic/technique/object (synonyms, spelling or plural variants count)\n"
    "- narrower_entry: the entry is a specific instance, application or sub-topic of the concept "
    "(e.g. entry 'Dolly the sheep, first mammal cloned from adult cells' vs concept 'Cloning')\n"
    "- broader_entry: the entry is a broader area that contains the concept\n"
    "- related: topically related but neither the same nor a clear sub/super-topic\n"
    "- different: unrelated or a different sense of the word\n"
    'Return JSON only: {"judgements": [{"candidate_id": "<id>", "relation": "<one of the five>", "confidence": <0-1>}]}')
SRC_NAME = {"mesh": "NLM Medical Subject Headings descriptor", "acm_ccs": "ACM Computing Classification System node",
            "msc": "Mathematics Subject Classification node", "pacs_physh": "physics classification (PACS/PhySH) node",
            "jel": "JEL economics classification node", "nature_methods_moty": "Nature Methods 'Method of the Year'",
            "science_boty": "Science 'Breakthrough of the Year'", "physics_world_boty": "Physics World 'Breakthrough of the Year' (winner or top-10)",
            "mit_tr10": "MIT Technology Review '10 Breakthrough Technologies'",
            "gartner_hype_cycle": "Gartner Hype Cycle for Emerging Technologies entry",
            "research_fronts": "Clarivate/CAS Research Fronts report (hot or emerging research front)"}
ACCEPT = {"same", "narrower_entry", "broader_entry"}


def prompt(entry: pd.Series, cands: pd.DataFrame, k: pd.DataFrame) -> str:
    lines = [f"ENTRY source: {SRC_NAME.get(entry.source, entry.source)}" + (f" ({int(entry.year)})" if pd.notna(entry.year) else ""),
             f"ENTRY text: {entry.label}"]
    if isinstance(entry.descriptor, str) and entry.descriptor:
        lines.append(f"ENTRY description: {entry.descriptor[:300]}")
    if entry.family not in ("lists",) and entry.parent_label:
        lines.append(f"ENTRY parent in its scheme: {entry.parent_label}")
    lines.append("CANDIDATE CONCEPTS:")
    for oid in cands.openalex_id:
        r = k.loc[oid]
        desc = r.description if isinstance(r.description, str) else ""
        top = ", ".join(sorted({a["display_name"] for a in r.ancestors if a["level"] == 0})) or "-"
        lines.append(f"- id={oid} | {r.label} | {desc[:110]} | field: {top}")
    return "\n".join(lines)


def kappa(a: list[str], b: list[str]) -> float:
    labs = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labs)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


async def run(mode: str) -> None:
    k = pd.read_parquet(WORK / "concept_keys.parquet").set_index("openalex_id")
    e = pd.read_parquet(WORK / "entries.parquet")
    tax = pd.read_parquet(WORK / "tax_entries.parquet")
    lab_by_code = {(s, v, c): l for s, v, c, l in zip(tax.source, tax.version, tax.code, tax.label)}
    par = {f"{s}:{v if pd.notna(v) else 'na'}:{c}": lab_by_code.get((s, v, p)) for s, v, c, p in
           zip(tax.source, tax.version, tax.code, tax.parent)}
    e["parent_label"] = e.entry_id.map(par)
    e = e.set_index("entry_id", drop=False)
    c = pd.read_parquet(WORK / "candidates.parquet")
    # Research Fronts items are verified only by the strict v2 pass (s7d_lists_v2.py); keeping them out of this pass
    # also keeps the audit and double-label samples identical to the original run
    c = c[~c.entry_id.str.startswith("research_fronts") & ~c.entry_id.str.startswith("physics_world_boty:2025")]
    c["auto"] = c.methods.map(lambda m: any(x in ("wikidata_property", "exact_norm_label", "exact_norm_alias") for x in m))
    fam = e.family
    c["family"] = c.entry_id.map(fam)

    # --- choose calls
    ent_auto = c.groupby("entry_id").auto.any()
    lists_e = sorted(set(c[c.family == "lists"].entry_id))
    fuzzy_e = sorted(set(c[(c.family != "lists")].entry_id) - set(ent_auto[ent_auto].index))
    # dedupe fuzzy taxonomy entries by (label_norm, candidate set) so versions of a scheme share one call
    key_of = {}
    for eid, g in c[c.entry_id.isin(fuzzy_e)].groupby("entry_id"):
        key_of[eid] = (e.at[eid, "source"], e.at[eid, "label_norm"], tuple(sorted(g.openalex_id)[:5]))
    uniq_fuzzy = {}
    for eid, kk in key_of.items():
        uniq_fuzzy.setdefault(kk, eid)
    verify_ids = lists_e + list(uniq_fuzzy.values())
    rnd = random.Random(0)
    audit_ids = []
    for f in sorted(c.family.dropna().unique()):
        ids = sorted(set(c[(c.family == f) & c.auto].entry_id))
        audit_ids += rnd.sample(ids, min(100, len(ids)))
    logger.info(f"verify calls planned: lists {len(lists_e)}, fuzzy unique {len(uniq_fuzzy)} (from {len(fuzzy_e)} entries); "
                f"audit {len(audit_ids)}")
    if len(verify_ids) > MAX_VERIFY_CALLS:
        logger.warning(f"capping verify calls at {MAX_VERIFY_CALLS}")
        verify_ids = lists_e + rnd.sample(list(uniq_fuzzy.values()), MAX_VERIFY_CALLS - len(lists_e))
    if mode == "plan":
        return
    llm = LLM(concurrency=24)
    rows = []

    async def one(eid: str, task: str, model: str) -> None:
        g = c[c.entry_id == eid].sort_values("score", ascending=False)
        if task == "audit":
            g = g[g.auto]
        g = g.head(5)
        user = prompt(e.loc[eid], g, k)
        try:
            d, meta = await llm.json_call(task=task, model=model, system=SYSTEM, user=user, max_tokens=400)
        except BudgetStop as ex:
            for oid, m in zip(g.openalex_id, g.methods):
                rows.append({"entry_id": eid, "openalex_id": oid, "task": task, "model": model, "relation": None,
                             "confidence": None, "methods": list(m), "status": f"not_verified: {ex}",
                             "prompt_hash": hashlib.sha256(user.encode()).hexdigest(), "cost": 0.0})
            return
        js = {str(j.get("candidate_id", "")).replace("id=", "").strip(): j for j in (d or {}).get("judgements", [])
              if isinstance(j, dict)}
        for oid, m in zip(g.openalex_id, g.methods):
            j = js.get(oid, {})
            rel = j.get("relation") if j.get("relation") in ACCEPT | {"related", "different"} else None
            rows.append({"entry_id": eid, "openalex_id": oid, "task": task, "model": model, "relation": rel,
                         "confidence": j.get("confidence"), "methods": list(m),
                         "status": "ok" if rel else "unparsed", "prompt_hash": meta["prompt_hash"],
                         "cost": meta["cost"] / max(1, len(g))})

    jobs = [(x, "verify", PRIMARY) for x in verify_ids] + [(x, "audit", PRIMARY) for x in audit_ids]
    await asyncio.gather(*(one(*j) for j in jobs))
    logger.info(f"primary pass done: ${llm.spent:.4f}")
    # double labelling: 200 random primary calls (verify+audit) re-asked with the second model
    dbl = rnd.sample(jobs, min(200, len(jobs)))
    await asyncio.gather(*(one(x, "double_" + t, SECOND) for x, t, _ in dbl))
    llm.close()
    v = pd.DataFrame(rows)
    # propagate deduped fuzzy verdicts to the other entries sharing (source, label_norm, candidates)
    rep = {eid: uniq_fuzzy[kk] for eid, kk in key_of.items() if uniq_fuzzy[kk] != eid}
    extra = []
    base = v[v.task == "verify"].set_index("entry_id")
    for eid, src in rep.items():
        if src in base.index:
            b = base.loc[[src]].reset_index()
            b["entry_id"] = eid
            b["status"] = b["status"] + f" (verdict reused from {src})"
            b["cost"] = 0.0
            extra.append(b)
    if extra:
        v = pd.concat([v] + extra, ignore_index=True)
    v.to_parquet(WORK / "verifications.parquet", index=False)
    # agreement
    p = v[v.task.isin(["verify", "audit"]) & ~v.status.str.contains("reused")].set_index(["entry_id", "openalex_id", "task"])
    q = v[v.task.str.startswith("double_")].copy()
    q["task"] = q.task.str.replace("double_", "")
    q = q.set_index(["entry_id", "openalex_id", "task"])
    j = p[["relation"]].join(q[["relation"]], rsuffix="_2", how="inner").dropna()
    a5, b5 = j.relation.tolist(), j.relation_2.tolist()
    a2 = ["accept" if x in ACCEPT else "reject" for x in a5]
    b2 = ["accept" if x in ACCEPT else "reject" for x in b5]
    agree = {"n_pairs": len(j), "raw_agreement_5class": sum(x == y for x, y in zip(a5, b5)) / max(1, len(j)),
             "kappa_5class": kappa(a5, b5) if j.shape[0] else None,
             "raw_agreement_accept": sum(x == y for x, y in zip(a2, b2)) / max(1, len(j)),
             "kappa_accept": kappa(a2, b2) if j.shape[0] else None, "primary": PRIMARY, "second": SECOND}
    au = v[v.task == "audit"]
    agree["audit_precision_by_family"] = {f: {"n_pairs": int(len(g)), "precision_accept": float(g.relation.isin(ACCEPT).mean()),
                                              "share_same": float((g.relation == "same").mean())}
                                          for f, g in au.assign(family=au.entry_id.map(fam)).groupby("family")}
    (OUT / "llm_agreement.json").write_text(json.dumps(agree, indent=1))
    logger.info(f"agreement {json.dumps(agree)[:1500]}")


def _kind(m) -> str:
    m = list(m)
    return "id" if "wikidata_property" in m else ("label" if "exact_norm_label" in m else
                                                  ("alias_only" if "exact_norm_alias" in m else "other"))


async def run_alias() -> None:
    """Second pass (added after the audit showed alias-only exact matches at 0.31 precision vs 0.96 for label
    matches): LLM-verify every alias-only pair (all families) and every MeSH label-only pair without an ID link."""
    k = pd.read_parquet(WORK / "concept_keys.parquet").set_index("openalex_id")
    e = pd.read_parquet(WORK / "entries.parquet")
    tax = pd.read_parquet(WORK / "tax_entries.parquet")
    lab_by_code = {(s_, v_, c_): l_ for s_, v_, c_, l_ in zip(tax.source, tax.version, tax.code, tax.label)}
    e["parent_label"] = [lab_by_code.get((s_, v_, p_)) for s_, v_, p_ in
                         zip(e.source, e.version, e.entry_id.map(dict(zip(
                             [f"{a}:{b if pd.notna(b) else 'na'}:{c_}" for a, b, c_ in zip(tax.source, tax.version, tax.code)],
                             tax.parent))))]
    e = e.set_index("entry_id", drop=False)
    c = pd.read_parquet(WORK / "candidates.parquet")
    c["family"] = c.entry_id.map(e.family)
    c["kind"] = c.methods.map(_kind)
    sel = c[(c.family != "lists") & ((c.kind == "alias_only") | ((c.family == "mesh") & (c.kind == "label")))]
    ids = sorted(sel.entry_id.unique())
    logger.info(f"alias pass: {len(sel)} pairs over {len(ids)} entries")
    llm = LLM(concurrency=24)
    rows = []

    async def one(eid: str) -> None:
        g = sel[sel.entry_id == eid].sort_values("score", ascending=False).head(5)
        user = prompt(e.loc[eid], g, k)
        try:
            d, meta = await llm.json_call(task="verify_alias", model=PRIMARY, system=SYSTEM, user=user, max_tokens=400)
        except BudgetStop as ex:
            for oid, m in zip(g.openalex_id, g.methods):
                rows.append({"entry_id": eid, "openalex_id": oid, "task": "verify_alias", "model": PRIMARY,
                             "relation": None, "confidence": None, "methods": list(m), "status": f"not_verified: {ex}",
                             "prompt_hash": hashlib.sha256(user.encode()).hexdigest(), "cost": 0.0})
            return
        js = {str(j.get("candidate_id", "")).replace("id=", "").strip(): j for j in (d or {}).get("judgements", [])
              if isinstance(j, dict)}
        for oid, m in zip(g.openalex_id, g.methods):
            j = js.get(oid, {})
            rel = j.get("relation") if j.get("relation") in ACCEPT | {"related", "different"} else None
            rows.append({"entry_id": eid, "openalex_id": oid, "task": "verify_alias", "model": PRIMARY, "relation": rel,
                         "confidence": j.get("confidence"), "methods": list(m), "status": "ok" if rel else "unparsed",
                         "prompt_hash": meta["prompt_hash"], "cost": meta["cost"] / max(1, len(g))})

    await asyncio.gather(*(one(x) for x in ids))
    llm.close()
    v = pd.read_parquet(WORK / "verifications.parquet")
    v = pd.concat([v[v.task != "verify_alias"], pd.DataFrame(rows)], ignore_index=True)
    v.to_parquet(WORK / "verifications.parquet", index=False)
    a = pd.DataFrame(rows)
    a["kind"] = a.methods.map(_kind)
    a["acc"] = a.relation.isin(ACCEPT)
    a["family"] = a.entry_id.map(e.family)
    stats = a.groupby(["family", "kind"]).acc.agg(["mean", "size"]).reset_index().to_dict("records")
    agr = json.loads((OUT / "llm_agreement.json").read_text())
    agr["alias_pass_accept_rate"] = stats
    (OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
    logger.info(f"alias pass done ${llm.spent:.4f}: {stats}")


if __name__ == "__main__":
    setup_logging("s7_verify")
    mode = sys.argv[1] if len(sys.argv) > 1 else "run"
    asyncio.run(run_alias() if mode == "alias" else run(mode))
