#!/usr/bin/env python3
"""Fetch English Wikidata labels/aliases/descriptions for legacy OpenAlex concepts (levels 2-5).
wbgetentities (50 QIDs per call) was rate-limited (HTTP 429, retry-after 35-55 s) on this host, so the free
Wikidata SPARQL endpoint is used instead (500 QIDs per query, sequential, User-Agent set).
Output: scan/wikidata_aliases.json {qid: {"label": str, "aliases": [str], "description": str}}"""
from __future__ import annotations

import json
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import pyarrow.parquet as pq
import requests

from common import SCAN, SNAP, setup_logger

logger = setup_logger("wikidata")
UA = "AI-Inventor-research/0.1 (scientometrics study; contact via OpenAlex polite pool)"
OUT = SCAN / "wikidata_aliases.json"


def load_concepts() -> pd.DataFrame:
    fs = sorted((SNAP / "concepts").glob("*.parquet"))
    df = pd.concat([pq.read_table(f, columns=["id", "display_name", "level", "description", "wikidata"]).to_pandas()
                    for f in fs]).drop_duplicates("id", keep="last")
    return df


def fetch_sparql(batch: list[str], sess: requests.Session) -> dict:
    vals = " ".join(f"wd:{q}" for q in batch)
    q = ("SELECT ?item ?kind ?v WHERE { VALUES ?item { " + vals + " } "
         "{ ?item skos:altLabel ?v . BIND('a' AS ?kind) } UNION { ?item rdfs:label ?v . BIND('l' AS ?kind) } "
         "UNION { ?item schema:description ?v . BIND('d' AS ?kind) } FILTER(LANG(?v) = 'en') }")
    for k in range(6):
        try:
            r = sess.post("https://query.wikidata.org/sparql", data={"query": q},
                          headers={"Accept": "application/sparql-results+json"}, timeout=120)
            if r.status_code == 200:
                out = {x: {"label": None, "aliases": [], "description": None} for x in batch}
                for b in r.json()["results"]["bindings"]:
                    qid = b["item"]["value"].rsplit("/", 1)[-1]
                    kind, v = b["kind"]["value"], b["v"]["value"]
                    e = out.setdefault(qid, {"label": None, "aliases": [], "description": None})
                    if kind == "a":
                        e["aliases"].append(v)
                    elif kind == "l":
                        e["label"] = v
                    else:
                        e["description"] = v
                return out
            logger.warning(f"SPARQL HTTP {r.status_code} retry-after={r.headers.get('retry-after')}")
            time.sleep(float(r.headers.get("retry-after") or (3 + 5 * k)))
        except (requests.RequestException, ValueError) as e:
            logger.warning(f"retry {k}: {e!r}"[:200])
            time.sleep(3 + 5 * k)
    logger.error(f"SPARQL batch failed {batch[0]}..")
    return {}


def fetch(batch: list[str], sess: requests.Session) -> dict:
    for k in range(6):
        try:
            r = sess.get("https://www.wikidata.org/w/api.php",
                         params={"action": "wbgetentities", "ids": "|".join(batch), "props": "labels|aliases|descriptions",
                                 "languages": "en", "format": "json"}, timeout=60)
            if r.status_code == 200:
                d = r.json()
                if "error" in d:
                    if d["error"].get("code") == "maxlag":
                        time.sleep(5 + 3 * k)
                        continue
                    logger.warning(f"wikidata error {d['error']}"[:300])
                    return {}
                out = {}
                for q, e in d.get("entities", {}).items():
                    if "missing" in e:
                        continue
                    out[q] = {"label": e.get("labels", {}).get("en", {}).get("value"),
                              "aliases": [a["value"] for a in e.get("aliases", {}).get("en", [])],
                              "description": e.get("descriptions", {}).get("en", {}).get("value")}
                return out
            logger.warning(f"HTTP {r.status_code} retry-after={r.headers.get('retry-after')}")
            time.sleep(float(r.headers.get("retry-after") or (2 + 3 * k)))
        except (requests.RequestException, ValueError) as e:
            logger.warning(f"retry {k}: {e!r}"[:200])
            time.sleep(2 + 3 * k)
    logger.error(f"batch failed {batch[0]}..")
    return {}


@logger.catch(reraise=True)
def main() -> None:
    df = load_concepts()
    df = df[df.level >= 2]
    surv = SCAN / "prescreen_survivors.parquet"
    if surv.exists():  # only concepts that survived the pre-screen and occur after 2002 in the 1% sample
        sv = pd.read_parquet(surv, columns=["qid", "post_hits"])
        keepq = set(sv.qid[sv.post_hits > 0])
        df = df[df.wikidata.fillna("").str.rsplit("/", n=1).str[-1].isin(keepq)]
    qids = sorted({w.rsplit("/", 1)[-1] for w in df.wikidata.dropna() if "/Q" in w})
    have = json.loads(OUT.read_text()) if OUT.exists() else {}
    todo = [q for q in qids if q not in have]
    batches = [todo[i:i + 500] for i in range(0, len(todo), 500)]
    logger.info(f"qids={len(qids)} cached={len(have)} batches={len(batches)}")
    sess = requests.Session()
    sess.headers["User-Agent"] = UA
    t0 = time.time()
    with ThreadPoolExecutor(1) as ex:
        for i, res in enumerate(ex.map(lambda b: fetch_sparql(b, sess), batches)):
            have.update(res)
            if i % 10 == 0:
                logger.info(f"{i}/{len(batches)} batches {time.time()-t0:.0f}s entities={len(have)}")
                OUT.write_text(json.dumps(have))
    OUT.write_text(json.dumps(have))
    logger.info(f"done: {len(have)} entities in {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
