#!/usr/bin/env python3
"""Stage A (free, S2): per dev-eligible concept, download phrase-matched papers of t0-3..t0+4 (cap 2,000, paperId-hash
order = uniform thinning), a late-window field sample t0+6..t0+8 (cap 3,000) and the citation lists of candidate
parents (t0-3..t0+3). Saves results/concepts/<slug>/s2_raw.json.gz. Usage: fetch_s2.py [max_concepts]"""
from __future__ import annotations

import gzip
import json
import random
import sys
import time
from pathlib import Path

from loguru import logger

import s2
from ground import Matcher, status
from panel import DEV_FIELDS, NOT_SEARCHED, SEED, seeded_order, slug
from s0 import home_fields, onset

ROOT = Path(__file__).resolve().parent
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "fetch_s2.log", rotation="30 MB", level="DEBUG")

EARLY_FIELDS = "paperId,year,title,abstract,authors,s2FieldsOfStudy,externalIds,publicationTypes,venue"
LATE_FIELDS = "paperId,year,s2FieldsOfStudy"
EARLY_PAGES, LATE_PAGES, MAX_PARENTS = 25, 3, 1500


def eligible() -> list[tuple[dict, int]]:
    raw = json.loads((ROOT / "results" / "s0_raw.json").read_text())
    out = []
    for c in seeded_order():
        v = raw[c["canonical"]]
        yc = {int(k): x for k, x in v["yc"].items()} if isinstance(v["yc"], dict) else None
        t0 = onset(yc) if yc else None
        if t0 is None or not 2003 <= t0 <= 2009:
            continue
        f = v.get("f_t0_t1")
        if f is not None and any(h not in DEV_FIELDS for h in home_fields(f)):
            continue  # sealed by the OpenAlex S0 home check: never fetched
        out.append((c, t0))
    return out


def s2_query(c: dict) -> str:
    return " | ".join(f'"{a}"' for a in c["aliases"] if a not in NOT_SEARCHED)


@logger.catch(reraise=True)
def fetch_one(c: dict, t0: int) -> dict:
    out_p = ROOT / "results" / "concepts" / slug(c["canonical"]) / "s2_raw.json.gz"
    if out_p.exists():
        return json.loads(gzip.decompress(out_p.read_bytes()))
    q = s2_query(c)
    early = s2.bulk_search(q, f"{t0-3}-{t0+4}", EARLY_FIELDS, max_pages=EARLY_PAGES)
    late = s2.bulk_search(q, f"{t0+6}-{t0+8}", LATE_FIELDS, max_pages=LATE_PAGES)
    # total counts (first page meta) for thinning factors
    tot_e = s2.cached_call("bulk", {"query": q, "year": f"{t0-3}-{t0+4}", "fields": EARLY_FIELDS}, lambda: None).get("total")
    tot_l = s2.cached_call("bulk", {"query": q, "year": f"{t0+6}-{t0+8}", "fields": LATE_FIELDS}, lambda: None).get("total")
    m = Matcher(c["aliases"])
    for p in early:
        p["gstatus"] = status(m, p.get("title"), p.get("abstract"))
        p.pop("abstract", None)  # keep the snapshot small
    parents = [p["paperId"] for p in early if p["gstatus"] != "rejected" and p.get("year") and p["year"] <= t0 + 3]
    n_par_all = len(parents)
    if len(parents) > MAX_PARENTS:  # uniform parent thinning: links thin linearly and the thinning cancels in the OR
        parents = sorted(random.Random(SEED).sample(parents, MAX_PARENTS))
    cits = s2.batch(parents, "citations.paperId,citations.year", size=300)
    cit = {pid: [x["paperId"] for x in (r or {}).get("citations") or [] if x.get("paperId")]
           for pid, r in zip(parents, cits)}
    d = {"concept": c["canonical"], "t0": t0, "query": q, "early": early, "late": late,
         "total_early": tot_e, "total_late": tot_l, "citations": cit,
         "n_parents_all": n_par_all, "parent_thin": n_par_all / max(len(parents), 1)}
    out_p.parent.mkdir(parents=True, exist_ok=True)
    out_p.write_bytes(gzip.compress(json.dumps(d).encode()))
    return d


def main() -> None:
    lim = int(sys.argv[1]) if len(sys.argv) > 1 else 10**6
    el = eligible()[:lim]
    logger.info(f"{len(el)} eligible concepts to fetch")
    for i, (c, t0) in enumerate(el):
        t = time.time()
        try:
            d = fetch_one(c, t0)
        except s2.S2Error as e:
            logger.error(f"{c['canonical']}: {e!r:.300}")
            continue
        n_conf = sum(p["gstatus"] == "confirmed" for p in d["early"])
        logger.info(f"[{i+1}/{len(el)}] parent_thin={d['parent_thin']:.2f} {c['canonical']} t0={t0} early={len(d['early'])}/{d['total_early']} "
                    f"confirmed={n_conf} late={len(d['late'])}/{d['total_late']} parents={len(d['citations'])} "
                    f"{time.time()-t:.0f}s S2={s2.STATS}")


if __name__ == "__main__":
    main()
    (ROOT / "logs" / "fetch_s2.done").write_text("done")
