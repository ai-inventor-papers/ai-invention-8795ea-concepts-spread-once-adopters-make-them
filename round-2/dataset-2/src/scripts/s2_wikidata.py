#!/usr/bin/env python3
"""STEP 2: Wikidata claims for every concept QID via wbgetentities (50 per call), compacted on the fly.

Raw entity JSON is large (all external IDs), so each response is reduced to the properties this dataset uses
and appended to cache/wikidata/entities.jsonl, keyed by the requested QID. Re-running resumes from that file.
"""
from __future__ import annotations

import asyncio
import json
import time

import aiohttp
import pandas as pd
from loguru import logger

from common import CACHE, UA, WORK, get_json, setup_logging

API = "https://www.wikidata.org/w/api.php"
PROPS = {  # property id -> expected English label (asserted before use)
    "P486": "MeSH descriptor ID", "P6694": "MeSH concept ID", "P672": "MeSH tree code",
    "P2179": "ACM Classification Code (2012)", "P3285": "Mathematics Subject Classification ID",
    "P571": "inception", "P575": "time of discovery or invention", "P61": "discoverer or inventor",
    "P31": "instance of", "P279": "subclass of", "P361": "part of", "P6366": "Microsoft Academic ID",
}
OUT_DIR = CACHE / "wikidata"
OUT_DIR.mkdir(parents=True, exist_ok=True)
ENT_FILE = OUT_DIR / "entities.jsonl"


def _val(snak: dict):
    dv = snak.get("datavalue")
    if not dv:
        return None
    v = dv.get("value")
    t = dv.get("type")
    if t == "wikibase-entityid":
        return v.get("id")
    if t == "time":
        return {"time": v.get("time"), "precision": v.get("precision"), "calendar": str(v.get("calendarmodel", "")).split("/")[-1]}
    if t == "string":
        return v
    if t == "monolingualtext":
        return v.get("text")
    return v


def compact(ent: dict, keep_props: list[str]) -> dict:
    claims = ent.get("claims", {}) or {}
    out_claims = {}
    for p in keep_props:
        vals = []
        for c in claims.get(p, []):
            if c.get("rank") == "deprecated":
                continue
            q = {}
            for qp, qs in (c.get("qualifiers") or {}).items():
                q[qp] = [_val(s) for s in qs]
            refs = len(c.get("references") or [])
            vals.append({"v": _val(c.get("mainsnak", {})), "rank": c.get("rank"), "q": q or None, "n_refs": refs})
        if vals:
            out_claims[p] = vals
    sl = ent.get("sitelinks", {}) or {}
    wiki_sl = [k for k in sl if k.endswith("wiki") and k not in ("commonswiki", "specieswiki", "metawiki",
                                                                     "mediawikiwiki", "wikidatawiki", "sourceswiki")]
    return {
        "id": ent.get("id"),
        "label_en": (ent.get("labels", {}).get("en") or {}).get("value"),
        "aliases_en": [a["value"] for a in ent.get("aliases", {}).get("en", [])],
        "enwiki_title": (sl.get("enwiki") or {}).get("title"),
        "n_wiki_sitelinks": len(wiki_sl),
        "n_sitelinks_all": len(sl),
        "claims": out_claims,
        "n_claims_total": sum(len(v) for v in claims.values()),
        "missing": "missing" in ent,
    }


async def verify_props(session: aiohttp.ClientSession, sem) -> dict:
    d = await get_json(session, API, {"action": "wbgetentities", "ids": "|".join(PROPS), "props": "labels",
                                      "languages": "en", "format": "json", "maxlag": 5}, sem)
    got = {p: d["entities"][p]["labels"]["en"]["value"] for p in PROPS}
    for p, lab in PROPS.items():
        assert got[p].casefold().startswith(lab.casefold()), f"property {p}: expected {lab!r}, got {got[p]!r}"
    extra = {}
    for q in ["PhySH", "JEL", "Journal of Economic Literature classification", "PACS"]:
        s = await get_json(session, API, {"action": "wbsearchentities", "search": q, "type": "property",
                                          "language": "en", "limit": 10, "format": "json"}, sem)
        extra[q] = [{"id": x["id"], "label": x.get("label"), "description": x.get("description")}
                    for x in s.get("search", [])]
    logger.info(f"verified properties: {got}")
    logger.info(f"property search: {json.dumps(extra)[:2000]}")
    return {"verified": got, "search": extra}


@logger.catch(reraise=True)
async def amain() -> None:
    setup_logging("s2_wikidata")
    c = pd.read_parquet(WORK / "concepts.parquet", columns=["openalex_id", "wikidata_qid", "level"])
    qids = sorted(set(c["wikidata_qid"].dropna()), key=lambda q: int(q[1:]) if q[1:].isdigit() else 0)
    done = set()
    if ENT_FILE.exists():
        for line in ENT_FILE.open():
            done.add(json.loads(line)["req"])
    todo = [q for q in qids if q not in done]
    logger.info(f"{len(qids)} QIDs, {len(done)} cached, {len(todo)} to fetch")
    sem = asyncio.Semaphore(4)
    headers = {"User-Agent": UA, "Accept-Encoding": "gzip"}
    async with aiohttp.ClientSession(headers=headers) as session:
        pv = await verify_props(session, sem)
        keep = list(PROPS)
        for lst in pv["search"].values():
            for x in lst:
                lab = (x.get("label") or "")
                if ("PhySH" in lab or "JEL" in lab or "PACS" in lab) and x["id"] not in keep:
                    keep.append(x["id"])
                    PROPS[x["id"]] = lab
        (OUT_DIR / "properties.json").write_text(json.dumps({"verify": pv, "kept": {p: PROPS[p] for p in keep}},
                                                            indent=1))
        batches = [todo[i:i + 50] for i in range(0, len(todo), 50)]
        t0 = time.time()
        fh = ENT_FILE.open("a")
        n_done = 0

        async def one(b: list[str]) -> None:
            nonlocal n_done
            params = {"action": "wbgetentities", "ids": "|".join(b), "props": "labels|aliases|claims|sitelinks",
                      "languages": "en", "format": "json", "maxlag": 5}
            try:
                d = await get_json(session, API, params, sem)
            except RuntimeError as e:
                logger.error(str(e))
                return
            ents = d.get("entities", {})
            for q in b:
                ent = ents.get(q)
                rec = {"req": q}
                if ent is None:
                    # redirected ids may be keyed by the target; search by 'redirects'
                    for e in ents.values():
                        if (e.get("redirects") or {}).get("from") == q:
                            ent = e
                            break
                if ent is None:
                    rec.update({"id": None, "missing": True})
                else:
                    rec.update(compact(ent, keep))
                    rd = ent.get("redirects")
                    rec["redirect_from"] = rd.get("from") if rd else None
                    rec["resolved_qid"] = ent.get("id") or q
                fh.write(json.dumps(rec) + "\n")
            n_done += 1
            fh.flush()
            if n_done % 50 == 0:
                el = time.time() - t0
                logger.info(f"{n_done}/{len(batches)} batches, {el:.0f}s, eta {(len(batches) - n_done) * el / n_done:.0f}s")

        q: asyncio.Queue = asyncio.Queue()
        for b in batches:
            q.put_nowait(b)

        async def worker() -> None:
            while not q.empty():
                b = q.get_nowait()
                await asyncio.wait_for(one(b), timeout=600)

        await asyncio.gather(*(worker() for _ in range(4)), return_exceptions=True)
        fh.close()
    logger.info("wikidata done")


if __name__ == "__main__":
    asyncio.run(amain())
