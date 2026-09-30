#!/usr/bin/env python3
"""STEP 7a: concept join keys (openalex_id, QID incl. resolved redirect, label_norm, aliases_norm, acronyms)
merged with the compact Wikidata claims -> work/concept_keys.parquet."""
from __future__ import annotations

import json

import pandas as pd
from loguru import logger

from common import CACHE, WORK, acronyms, norm_label, setup_logging


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s7_keys")
    c = pd.read_parquet(WORK / "concepts.parquet")
    wd = {}
    for line in (CACHE / "wikidata" / "entities.jsonl").open():
        r = json.loads(line)
        wd[r["req"]] = r
    logger.info(f"concepts {len(c)}, wikidata records {len(wd)}")
    rows = []
    for r in c.itertuples(index=False):
        w = wd.get(r.wikidata_qid) or {}
        cl = w.get("claims") or {}
        al = [r.display_name] + list(r.en_variants) + ([w["label_en"]] if w.get("label_en") else []) + list(w.get("aliases_en") or [])
        seen, aliases = set(), []
        for a in al:
            if a and a not in seen:
                seen.add(a)
                aliases.append(a)
        aliases = aliases[1:21]   # exclude the display name itself, cap 20
        ln = norm_label(r.display_name)
        an = sorted({norm_label(a) for a in aliases} - {ln, ""})

        def vals(p):
            return [v["v"] for v in cl.get(p, []) if v.get("v") is not None]
        rows.append({
            "openalex_id": r.openalex_id, "qid": r.wikidata_qid,
            "qid_resolved": w.get("resolved_qid") or w.get("id") or r.wikidata_qid,
            "qid_redirected": bool(w.get("redirect_from")), "wikidata_missing": bool(w.get("missing", not w)),
            "label": r.display_name, "label_norm": ln, "aliases": aliases, "aliases_norm": an,
            "acronyms": acronyms(aliases), "level": r.level, "description": r.description,
            "ancestor_ids": [a["id"] for a in r.ancestors], "ancestors": r.ancestors,
            "enwiki_title": w.get("enwiki_title"), "wikipedia_url": r.wikipedia_url,
            "p486": vals("P486"), "p6694": vals("P6694"), "p672": vals("P672"), "p2179": vals("P2179"),
            "p3285": vals("P3285"), "p571": json.dumps(cl.get("P571", [])), "p575": json.dumps(cl.get("P575", [])),
            "p61": vals("P61"), "p31": vals("P31"), "p279": vals("P279"), "p361": vals("P361"), "p6366": vals("P6366"),
            "n_wiki_sitelinks": w.get("n_wiki_sitelinks"), "n_claims_total": w.get("n_claims_total"),
            "present_day_works_count": r.present_day_works_count,
            "present_day_cited_by_count": r.present_day_cited_by_count, "mag_id": r.mag_id,
        })
    k = pd.DataFrame(rows)
    # sanity join: Wikidata P6366 (Microsoft Academic ID) should equal the OpenAlex concept's MAG id / numeric id
    num = k.openalex_id.str[1:]
    has = k.p6366.map(len) > 0
    agree = [n in v for n, v in zip(num[has], k.p6366[has])]
    logger.info(f"P6366 present for {has.sum()} concepts; equals OpenAlex numeric id for {sum(agree)} ({sum(agree) / max(1, has.sum()):.3f})")
    k["p6366_agrees"] = [(n in v) if len(v) else None for n, v in zip(num, k.p6366)]
    k.to_parquet(WORK / "concept_keys.parquet", index=False)
    logger.info(f"keys written; enwiki titles {k.enwiki_title.notna().sum()}, P486 {int((k.p486.map(len) > 0).sum())}, "
                f"P2179 {int((k.p2179.map(len) > 0).sum())}, P3285 {int((k.p3285.map(len) > 0).sum())}, "
                f"P571 {int((k.p571 != '[]').sum())}, P575 {int((k.p575 != '[]').sum())}, redirected {int(k.qid_redirected.sum())}")


if __name__ == "__main__":
    main()
