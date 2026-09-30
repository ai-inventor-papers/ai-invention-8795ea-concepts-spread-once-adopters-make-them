#!/usr/bin/env python3
"""WP4 hand check (100 items: 50 O5_main positives, 50 negatives; seed 20260928; stratified by source and group).
Step 1 reuse art_O7Dq4L02QnDN hand-check verdicts where (concept, entry) overlaps; step 2 LLM judge (OpenRouter,
openai/gpt-4.1-mini, hard cap $1) for positives; step 3 free MediaWiki first-revision date check for every Wikipedia
positive and every negative (<= 1 request/s); step 4 executor verdicts (results/executor_verdicts.json, written by the
executor after reading the items) and the final metrics (--finalize). Labelled 'executor-checked', never 'human-checked'."""
from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import re
import time

import numpy as np
import pandas as pd
import requests
from loguru import logger
from openai import AsyncOpenAI

import common as C

MODEL = "openai/gpt-4.1-mini"
CAP_USD = 1.0
UA = "aii-record-audit/0.1 (research evaluation; contact: run owner)"
POS_ALLOC = {"wikipedia_en": 20, "mesh": 10, "tax": 8, "list": 7, "wikidata": 5}


def src_bucket(s: str) -> str:
    if s in ("acm_ccs", "msc", "pacs_physh"):
        return "tax"
    if s in ("gartner_hype_cycle", "mit_tr10", "nature_methods_moty", "science_boty", "physics_world_boty", "research_fronts"):
        return "list"
    return s


def sample(panel: pd.DataFrame, ev: pd.DataFrame, rng) -> pd.DataFrame:
    import wp4_o5 as W
    evq = ev[ev.apply(lambda r: W.qualifies({"source": r.source, "event_type": r.event_type, "year": r.year, "relation": r.relation,
                                             "year_usable": r.year_usable, "mesh_baseline": r.mesh_baseline}) and r.t0 < r.year <= r.t0 + 8, axis=1)]
    first = evq.sort_values("year").groupby("id").head(1).copy()
    first["bucket"] = first.source.map(src_bucket)
    first = first.merge(panel[["id", "gkey", "name", "level"]], on="id")
    items = []
    for b, k in POS_ALLOC.items():
        pool = first[first.bucket == b]
        # stratify by group: round-robin over groups in random order
        order = []
        byg = {g: list(rng.permutation(d.index.to_numpy())) for g, d in pool.groupby("gkey")}
        while byg and len(order) < k:
            for g in list(rng.permutation(sorted(byg))):
                if byg[g]:
                    order.append(byg[g].pop())
                if not byg[g]:
                    del byg[g]
                if len(order) >= k:
                    break
        for i in order:
            r = pool.loc[i]
            items.append({"item": f"P{len(items)+1:02d}", "kind": "positive", "id": r.id, "name": r["name"], "gkey": r.gkey, "t0": int(r.t0),
                          "source": r.source, "event_type": r.event_type, "year": int(r.year), "entry_title": r.title, "entry_id": r.entry_id,
                          "match_method": r.match_method, "relation": r.relation, "date_precision": r.date_precision, "bucket": b})
    neg_pool = panel[(panel.O5_main == 0) & panel.chk_wikipedia_en.isin(["found", "found_estimated", "not_found"])]
    byg = {g: list(rng.permutation(d.index.to_numpy())) for g, d in neg_pool.groupby("gkey")}
    order = []
    while len(order) < 50 and byg:
        for g in list(rng.permutation(sorted(byg))):
            if byg[g]:
                order.append(byg[g].pop())
            if not byg[g]:
                del byg[g]
            if len(order) >= 50:
                break
    for i in order:
        r = neg_pool.loc[i]
        items.append({"item": f"N{len(items)-49:02d}", "kind": "negative", "id": r.id, "name": r["name"], "gkey": r.gkey, "t0": int(r.t0),
                      "source": None, "event_type": None, "year": None, "entry_title": None, "entry_id": None, "match_method": None,
                      "relation": None, "date_precision": None, "bucket": "negative"})
    return pd.DataFrame(items)


def reuse(items: pd.DataFrame) -> pd.DataFrame:
    reused = {}
    for f in ("out/hand_check.csv", "out/hand_check_lists_v2.csv", "out/hand_check_research_fronts.csv"):
        p = C.D2 / f
        if not p.exists():
            continue
        d = C.read_csv(p)
        for _, r in d.iterrows():
            reused[(str(r.get("openalex_id")), str(r.get("entry_id")))] = (f, r.get("hand"))
    items["reused_verdict"] = [reused.get((r.id, str(r.entry_id)), (None, None))[1] for r in items.itertuples()]
    items["reused_from"] = [reused.get((r.id, str(r.entry_id)), (None, None))[0] for r in items.itertuples()]
    return items


PROMPT = """You are auditing an external-recognition dataset for scientific concepts.
Concept (OpenAlex legacy concept): "{name}" (level {level}); aliases: {aliases}.
Onset year of the concept in the literature (t0): {t0}.
Matched external entry: source = {source}; event = {event_type}; entry title/label = "{entry_title}"; dated year = {year};
match method = {match_method}; stated relation (entry side) = {relation}.
Questions: (1) Does the external entry denote the SAME concept (not a broader field, narrower sub-topic or homonym)?
(2) Is the dated year plausibly the FIRST recognition of this concept by that source (e.g. the year the Wikipedia article
or MeSH descriptor was created, the year the taxonomy added it, the year the list featured it)?
Answer ONLY with JSON: {{"same_concept": "yes"|"no"|"partial", "date_is_first_recognition": "yes"|"no"|"unclear", "reason": "<= 30 words"}}"""


async def llm_judge(items: pd.DataFrame, aliases: dict) -> tuple[list, float]:
    client = AsyncOpenAI(base_url=os.environ["OPENROUTER_BASE_URL"], api_key=os.environ["OPENROUTER_API_KEY"])
    sem = asyncio.Semaphore(8)
    spent = {"usd": 0.0, "stop": False}
    out = [None] * len(items)

    async def one(i, r):
        async with sem:
            if spent["stop"] or spent["usd"] >= CAP_USD:
                return
            msg = PROMPT.format(name=r.name, level=r.level if hasattr(r, "level") else "?", aliases=aliases.get(r.id, [])[:6], t0=r.t0,
                                source=r.source, event_type=r.event_type, entry_title=r.entry_title, year=r.year, match_method=r.match_method,
                                relation=r.relation)
            for attempt in range(3):
                try:
                    resp = await client.chat.completions.create(model=MODEL, messages=[{"role": "user", "content": msg}], temperature=0,
                                                                max_tokens=200, response_format={"type": "json_object"},
                                                                extra_body={"usage": {"include": True}})
                    cost = float(getattr(resp.usage, "cost", 0) or (resp.usage.model_extra or {}).get("cost", 0) or 0)
                    spent["usd"] += cost
                    txt = resp.choices[0].message.content
                    logger.debug(f"LLM {r.item}: {msg[:200]} -> {txt[:300]} (${cost:.5f})")
                    out[i] = {**json.loads(txt), "cost": cost}
                    return
                except Exception as e:  # noqa: BLE001 - network / JSON errors are retried, budget refusal stops the batch
                    if "AI Inventor per-run OpenRouter budget" in str(e):
                        spent["stop"] = True
                        logger.error("budget refusal; stopping batch")
                        return
                    logger.warning(f"LLM {r.item} attempt {attempt}: {repr(e)[:200]}")
                    await asyncio.sleep(2 * (attempt + 1))

    await asyncio.gather(*[one(i, r) for i, r in enumerate(items.itertuples()) if r.kind == "positive" and not isinstance(r.reused_verdict, str)])
    return out, spent["usd"]


def wiki_first_rev(titles: list[str]) -> dict:
    """First revision of the first title that resolves to an existing page (redirects followed and recorded)."""
    for t in titles:
        if not t:
            continue
        try:
            r = requests.get("https://en.wikipedia.org/w/api.php", params={"action": "query", "prop": "revisions", "rvdir": "newer", "rvlimit": 1,
                                                                             "rvprop": "timestamp", "titles": t, "redirects": 1, "format": "json"},
                             headers={"User-Agent": UA}, timeout=20)
            time.sleep(1.0)
            q = r.json().get("query", {})
            for pid, pg in q.get("pages", {}).items():
                if int(pid) > 0 and pg.get("revisions"):
                    return {"query_title": t, "page_title": pg["title"], "redirected": bool(q.get("redirects")),
                            "first_rev": pg["revisions"][0]["timestamp"], "first_rev_year": int(pg["revisions"][0]["timestamp"][:4])}
        except (requests.RequestException, ValueError) as e:
            logger.warning(f"wiki {t}: {e}")
            time.sleep(1.0)
    return {"query_title": titles[0] if titles else None, "page_title": None, "redirected": None, "first_rev": None, "first_rev_year": None}


def wiki_retry(budget_s: float = 480.0) -> None:
    """Re-query items whose first-revision lookup failed (HTTP 429 from the shared IP) with exponential backoff that
    honours Retry-After; one title per item (the dataset's enwiki_title, else the label); stops when the time budget ends."""
    C.setup_logging("wp4_handcheck")
    it = pd.read_csv(C.TAB / "o5_handcheck_items.csv")
    joined = {json.loads(l)["openalex_id"]: json.loads(l) for l in open(C.RES / "o5_joined.jsonl")}
    need = it[((it.kind == "negative") | (it.source == "wikipedia_en")) & it.wiki_first_rev_year.isna()]
    t_end = time.time() + budget_s
    n_ok, n_429, wait = 0, 0, 2.0
    status = {}
    for i, r in need.iterrows():
        if time.time() > t_end:
            break
        j = joined.get(r.id, {})
        title = (r.entry_title if r.source == "wikipedia_en" and isinstance(r.entry_title, str) else None) or j.get("enwiki_title") or j.get("label")
        for attempt in range(6):
            if time.time() > t_end:
                break
            try:
                resp = requests.get("https://en.wikipedia.org/w/api.php", params={"action": "query", "prop": "revisions", "rvdir": "newer", "rvlimit": 1,
                                    "rvprop": "timestamp", "titles": title, "redirects": 1, "format": "json", "maxlag": 5},
                                    headers={"User-Agent": UA}, timeout=20)
            except requests.RequestException as e:
                logger.warning(f"wiki {title}: {e}")
                time.sleep(wait)
                continue
            if resp.status_code == 429:
                n_429 += 1
                ra = resp.headers.get("Retry-After")
                wait = min(60.0, float(ra) if ra and ra.isdigit() else wait * 2)
                logger.warning(f"429 for {title}; sleeping {wait:.0f}s")
                time.sleep(wait)
                continue
            wait = 2.0
            q = resp.json().get("query", {})
            found = False
            for pid, pg in q.get("pages", {}).items():
                if int(pid) > 0 and pg.get("revisions"):
                    ts = pg["revisions"][0]["timestamp"]
                    it.loc[i, ["wiki_query_title", "wiki_page_title", "wiki_redirected", "wiki_first_rev", "wiki_first_rev_year"]] = [
                        title, pg["title"], bool(q.get("redirects")), ts, int(ts[:4])]
                    found = True
            status[r.item] = "found" if found else "no_page"
            if not found:
                it.loc[i, "wiki_query_title"] = title
            n_ok += 1
            time.sleep(1.5)
            break
    it["wiki_lookup_status"] = it.item.map(status).fillna(it.wiki_first_rev_year.notna().map({True: "found", False: "not_attempted_or_failed"}))
    it.to_csv(C.TAB / "o5_handcheck_items.csv", index=False)
    C.dump({"n_needed": int(len(need)), "n_resolved": n_ok, "n_429": n_429, "budget_s": budget_s}, C.RES / "o5_handcheck_wiki_retry.json")
    logger.info(f"wiki retry: needed {len(need)}, resolved {n_ok}, 429s {n_429}")


def run() -> None:
    C.setup_logging("wp4_handcheck")
    rng = np.random.default_rng(C.SEED)
    panel = C.read_csv(C.TAB / "o5_concept_panel.csv")
    ev = C.read_csv(C.RES / "o5_events_frame.csv")
    items = sample(panel, ev, rng)
    items = items.drop(columns=["level"], errors="ignore").merge(panel[["id", "level"]], on="id", how="left")
    items = reuse(items)
    joined = {json.loads(l)["openalex_id"]: json.loads(l) for l in open(C.RES / "o5_joined.jsonl")}
    aliases = {k: v.get("aliases", []) for k, v in joined.items()}
    res, usd = asyncio.run(llm_judge(items, aliases))
    items["llm_same_concept"] = [r.get("same_concept") if r else None for r in res]
    items["llm_date_first"] = [r.get("date_is_first_recognition") if r else None for r in res]
    items["llm_reason"] = [r.get("reason") if r else None for r in res]
    items["llm_cost_usd"] = [r.get("cost") if r else 0.0 for r in res]
    logger.info(f"LLM spend ${usd:.4f}")
    wk = []
    for r in items.itertuples():
        if r.kind == "negative" or r.source == "wikipedia_en":
            j = joined.get(r.id, {})
            titles = [r.entry_title] if r.source == "wikipedia_en" and r.entry_title else []
            titles += [j.get("enwiki_title"), j.get("label")] + list(j.get("aliases", []))[:2]
            seen, tl = set(), []
            for t in titles:
                if t and t.lower() not in seen:
                    seen.add(t.lower())
                    tl.append(t)
            wk.append(wiki_first_rev(tl[:3]))
        else:
            wk.append({})
    W = pd.DataFrame(wk, index=items.index).add_prefix("wiki_")
    items = pd.concat([items, W], axis=1)
    items.to_csv(C.TAB / "o5_handcheck_items.csv", index=False)
    C.dump({"model": MODEL, "llm_cost_usd": usd, "n_llm_calls": int(sum(1 for r in res if r)), "cap_usd": CAP_USD}, C.RES / "o5_handcheck_llm_meta.json")
    C.save_manifest("wp4_handcheck")


def finalize() -> None:
    C.setup_logging("wp4_handcheck")
    it = pd.read_csv(C.TAB / "o5_handcheck_items.csv")
    exv = json.loads((C.RES / "executor_verdicts.json").read_text())["verdicts"]
    it["exec_same"] = it.item.map(lambda k: exv.get(k, {}).get("same_concept"))
    it["exec_date"] = it.item.map(lambda k: exv.get(k, {}).get("date_ok"))
    it["exec_fn"] = it.item.map(lambda k: exv.get(k, {}).get("false_negative"))
    it["exec_note"] = it.item.map(lambda k: exv.get(k, {}).get("note"))
    it["exec_emergence"] = it.item.map(lambda k: exv.get(k, {}).get("emergence_meaningful"))
    pos = it[it.kind == "positive"].copy()
    neg = it[it.kind == "negative"].copy()
    # final same-concept verdict: executor where read, else reused hand verdict, else LLM
    def final_same(r):
        if isinstance(r.exec_same, str):
            return r.exec_same
        if isinstance(r.reused_verdict, str):
            return "yes" if r.reused_verdict == "same" else "no"
        return r.llm_same_concept
    pos["final_same"] = pos.apply(final_same, axis=1)
    strict = float((pos.final_same == "yes").mean())
    lenient = float(pos.final_same.isin(["yes", "partial"]).mean())
    k_strict = int((pos.final_same == "yes").sum())
    wpos = pos[(pos.source == "wikipedia_en") & pos.wiki_first_rev_year.notna()]
    derr = (wpos.year - wpos.wiki_first_rev_year).abs()
    # dates for non-Wikipedia positives: executor date verdict, else LLM
    other = pos[pos.source != "wikipedia_en"]
    oth_ok = other.apply(lambda r: r.exec_date if isinstance(r.exec_date, str) else r.llm_date_first, axis=1)
    date_ok_share_wiki = float((derr <= 1).mean()) if len(derr) else math.nan
    n_date_checked = int(len(derr) + oth_ok.isin(["yes", "no"]).sum())
    date_ok_all = (int((derr <= 1).sum()) + int((oth_ok == "yes").sum())) / n_date_checked if n_date_checked else math.nan
    # negatives: FN = a Wikipedia page for the concept (no redirect to another title) first revised in (t0, t0+8]
    neg["wiki_fn"] = (neg.wiki_first_rev_year.notna() & (neg.wiki_first_rev_year > neg.t0) & (neg.wiki_first_rev_year <= neg.t0 + 8))
    neg["wiki_fn_exact_page"] = neg.wiki_fn & (neg.wiki_redirected != True)  # noqa: E712
    neg["final_fn"] = neg.apply(lambda r: r.exec_fn if isinstance(r.exec_fn, str) else ("yes" if r.wiki_fn_exact_page else "no"), axis=1)
    fn_rate = float((neg.final_fn == "yes").mean())
    # executor vs LLM agreement (positives read by both)
    both = pos[pos.exec_same.notna() & pos.llm_same_concept.notna()]
    kap = C.cohen_kappa(both.exec_same.to_numpy(), both.llm_same_concept.to_numpy(), ["yes", "partial", "no"]) if len(both) else math.nan
    agree = float((both.exec_same == both.llm_same_concept).mean()) if len(both) else math.nan
    by_bucket = pos.groupby("bucket").apply(lambda d: pd.Series({"n": len(d), "precision_strict": (d.final_same == "yes").mean(),
                                                                "precision_lenient": d.final_same.isin(["yes", "partial"]).mean()})).reset_index()
    meta = json.loads((C.RES / "o5_handcheck_llm_meta.json").read_text())
    fit = bool(strict >= 0.85 and (date_ok_all >= 0.80 if np.isfinite(date_ok_all) else False))
    out = {"label": "executor-checked (LLM judge + executor reading + MediaWiki first-revision API); NOT a human expert annotation",
           "n_items": int(len(it)), "n_positive": int(len(pos)), "n_negative": int(len(neg)),
           "n_executor_read": int(it.exec_same.notna().sum() + it.exec_fn.notna().sum()),
           "n_reused_verdicts": int(it.reused_verdict.notna().sum()),
           "positive_precision_strict": strict, "positive_precision_strict_wilson95": C.wilson(k_strict, len(pos)),
           "positive_precision_lenient_partial_counts": lenient, "precision_by_source_bucket": by_bucket.to_dict("records"),
           "wikipedia_date_error_years": {"n": int(len(derr)), "median": float(derr.median()) if len(derr) else math.nan,
                                          "share_le_1": date_ok_share_wiki, "share_eq_0": float((derr == 0).mean()) if len(derr) else math.nan,
                                          "distribution": {str(int(k)): int(v) for k, v in derr.value_counts().sort_index().items()}},
           "non_wikipedia_date_first_recognition": oth_ok.value_counts().to_dict(),
           "date_error_le_1y_share_all_checked": date_ok_all, "n_date_checked": n_date_checked,
           "negatives_false_negative_rate": fn_rate, "negatives_false_negative_wilson95": C.wilson(int((neg.final_fn == "yes").sum()), len(neg)),
           "negatives_wiki_page_any_in_window": float(neg.wiki_fn.mean()),
           "negatives_wiki_page_exists_share": float(neg.wiki_first_rev_year.notna().mean()),
           "negatives_wiki_page_precedes_t0_share": float((neg.wiki_first_rev_year <= neg.t0).mean()),
           "fn_note": "lower bound: only Wikipedia was checked for false negatives (not MeSH/taxonomies)",
           "positives_emergence_meaningful_share": float((pos.exec_emergence == "yes").mean()),
           "positives_emergence_meaningful_note": "executor judgement: does the event plausibly mark recognition of a NEW concept (vs dating a long-known phenomenon)?",
           "executor_vs_llm_kappa_same_concept": kap, "executor_vs_llm_pct_agree": agree, "n_executor_llm_pairs": int(len(both)),
           "llm": meta, "FIT_FOR_USE_rule": "precision_strict >= 0.85 AND date error <= 1 year in >= 80% of checked positives",
           "FIT_FOR_USE": fit}
    C.dump(out, C.RES / "o5_handcheck_summary.json")
    it.merge(pos[["item", "final_same"]], on="item", how="left").merge(neg[["item", "final_fn", "wiki_fn"]], on="item", how="left") \
        .to_csv(C.TAB / "o5_handcheck_items_final.csv", index=False)
    logger.info({k: v for k, v in out.items() if not isinstance(v, (list, dict))})


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--finalize", action="store_true")
    ap.add_argument("--wiki-retry", action="store_true")
    a = ap.parse_args()
    if a.wiki_retry:
        wiki_retry()
    elif a.finalize:
        finalize()
    else:
        run()
