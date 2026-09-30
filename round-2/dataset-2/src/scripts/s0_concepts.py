#!/usr/bin/env python3
"""STEP 0: build the concept frame from the public OpenAlex concepts parquet snapshot (zero API credits)."""
from __future__ import annotations

import gzip
import json

import pandas as pd
import pyarrow.parquet as pq
from loguru import logger

from common import RAW, WORK, setup_logging


def _qid(u) -> str | None:
    if not isinstance(u, str) or not u:
        return None
    return u.rstrip("/").split("/")[-1]


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s0_concepts")
    files = sorted((RAW / "concepts").rglob("*.parquet"))
    logger.info(f"{len(files)} parquet parts")
    schema = pq.read_schema(files[0])
    logger.info(f"schema: {schema.names}")
    df = pd.concat([pq.read_table(f).to_pandas() for f in files], ignore_index=True)
    logger.info(f"rows={len(df)} cols={list(df.columns)}")
    ex = df.iloc[0].to_dict()
    logger.debug(f"example row: {str(ex)[:3000]}")
    recs = []
    for r in df.itertuples(index=False):
        d = r._asdict()
        ids = d.get("ids") if isinstance(d.get("ids"), dict) else {}
        anc = d.get("ancestors")
        anc_l = []
        if anc is not None:
            for a in list(anc):
                a = dict(a)
                anc_l.append({"id": str(a.get("id", "")).split("/")[-1], "level": a.get("level"),
                              "display_name": a.get("display_name")})
        intl = d.get("international")
        en_variants = []
        if isinstance(intl, dict):
            dn = intl.get("display_name")
            if isinstance(dn, dict):
                en_variants = sorted({v for k, v in dn.items() if k and str(k).startswith("en") and v})
        recs.append({
            "openalex_id": str(d["id"]).split("/")[-1],
            "display_name": d.get("display_name"),
            "level": int(d["level"]) if d.get("level") is not None else None,
            "wikidata_qid": _qid(d.get("wikidata") or ids.get("wikidata")),
            "mag_id": ids.get("mag"),
            "wikipedia_url": ids.get("wikipedia"),
            "umls_cui": list(ids.get("umls_cui") or []) if ids else [],
            "umls_aui": list(ids.get("umls_aui") or []) if ids else [],
            "description": d.get("description"),
            "ancestors": anc_l,
            "en_variants": en_variants,
            "present_day_works_count": d.get("works_count"),
            "present_day_cited_by_count": d.get("cited_by_count"),
            "created_date": str(d.get("created_date")) if d.get("created_date") is not None else None,
        })
    out = pd.DataFrame(recs)
    # The 2026 parquet snapshot leaves ancestors/international/mag empty; the legacy JSON snapshot
    # (s3://openalex/legacy-data/concepts/, same concept ids) carries them. Keep the latest record per id.
    leg: dict[str, dict] = {}
    for f in sorted((RAW / "concepts_legacy").rglob("part_*.gz")):
        with gzip.open(f, "rt") as fh:
            for line in fh:
                d = json.loads(line)
                cid = str(d["id"]).split("/")[-1]
                if cid not in leg or str(d.get("updated_date")) > str(leg[cid].get("updated_date")):
                    leg[cid] = d
    logger.info(f"legacy JSON concepts: {len(leg)}")
    anc_col, intl_col, mag_col, src_col = [], [], [], []
    for cid, anc0, en0 in zip(out["openalex_id"], out["ancestors"], out["en_variants"]):
        d = leg.get(cid)
        if d is None:
            anc_col.append(anc0); intl_col.append(en0); mag_col.append(None); src_col.append("parquet_only")
            continue
        anc_col.append([{"id": str(a.get("id", "")).split("/")[-1], "level": a.get("level"),
                         "display_name": a.get("display_name"), "wikidata": _qid(a.get("wikidata"))}
                        for a in (d.get("ancestors") or [])])
        dn = ((d.get("international") or {}).get("display_name") or {})
        intl_col.append(sorted({v for k, v in dn.items() if str(k).startswith("en") and v}))
        mag_col.append((d.get("ids") or {}).get("mag"))
        src_col.append("legacy_json")
    out["ancestors"] = anc_col
    out["en_variants"] = intl_col
    out["mag_id"] = mag_col
    out["ancestor_source"] = src_col
    logger.info(f"ancestor source counts: {out['ancestor_source'].value_counts().to_dict()}")
    dup = out["openalex_id"].duplicated().sum()
    if dup:
        logger.warning(f"{dup} duplicate openalex ids; keeping first")
        out = out.drop_duplicates("openalex_id")
    out.to_parquet(WORK / "concepts.parquet", index=False)
    by_level = out.groupby("level").agg(n=("openalex_id", "size"), with_qid=("wikidata_qid", lambda s: s.notna().sum()),
                                        with_wp=("wikipedia_url", lambda s: s.notna().sum()))
    logger.info(f"per level:\n{by_level}")
    (WORK / "concepts_level_counts.json").write_text(json.dumps(by_level.reset_index().to_dict("records"), indent=1,
                                                                default=int))


if __name__ == "__main__":
    main()
