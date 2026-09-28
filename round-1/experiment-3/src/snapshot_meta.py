#!/usr/bin/env python3
"""Free metadata from the OpenAlex snapshot (0 credits).

SOURCE_FIELD[sid] = OpenAlex field (26-level) holding >= 40% of the source's summed topic counts, else None;
repositories are unlabelled (S0 rule, same as the run's probe). TOPIC_META[tid] = (name, subfield, field).
Writes results/source_field.parquet and results/topic_meta.csv."""
from __future__ import annotations

import sys
from collections import defaultdict

import pandas as pd
import pyarrow.parquet as pq
from loguru import logger

from config import LOGS, RES, SNAP, SRC_FIELD_SHARE

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "snapshot_meta.log", rotation="30 MB", level="DEBUG")


def _num(x: str) -> int:
    return int(x.rstrip("/").split("/")[-1].lstrip("STFfsd").lstrip("ields/").lstrip("ubfields/"))


def topic_meta() -> pd.DataFrame:
    rows = {}
    for f in sorted((SNAP / "topics").rglob("*.parquet")):  # sorted by updated_date -> latest wins
        t = pq.read_table(f, columns=["id", "display_name", "subfield", "field", "keywords"]).to_pylist()
        for r in t:
            tid = int(r["id"].split("/T")[-1])
            rows[tid] = {"topic": tid, "name": r["display_name"],
                         "subfield": int(r["subfield"]["id"].split("/")[-1]), "subfield_name": r["subfield"]["display_name"],
                         "field": int(r["field"]["id"].split("/")[-1]), "field_name": r["field"]["display_name"],
                         "keywords": "; ".join(r.get("keywords") or [])}
    return pd.DataFrame(sorted(rows.values(), key=lambda r: r["topic"]))


def source_field() -> pd.DataFrame:
    latest: dict[int, tuple] = {}
    files = sorted((SNAP / "sources").rglob("*.parquet"))
    for f in files:
        t = pq.read_table(f, columns=["id", "type", "topics"])
        ids = t.column("id").to_pylist()
        types = t.column("type").to_pylist()
        tops = t.column("topics").to_pylist()
        for sid, ty, tp in zip(ids, types, tops):
            s = int(sid.split("/S")[-1])
            c: dict[int, int] = defaultdict(int)
            for x in tp or []:
                c[int(x["field"]["id"].split("/")[-1])] += int(x.get("count") or 0)
            latest[s] = (ty, dict(c))
        del t
    out = []
    for s, (ty, c) in latest.items():
        tot = sum(c.values())
        lab = None
        share = None
        if tot > 0:
            fbest = max(c, key=c.get)
            share = c[fbest] / tot
            if share >= SRC_FIELD_SHARE and ty != "repository":
                lab = fbest
        out.append({"source": s, "type": ty, "field": lab, "top_share": share, "topic_total": tot})
    df = pd.DataFrame(out)
    df["field"] = df["field"].astype("Int64")
    return df


@logger.catch(reraise=True)
def main() -> None:
    tm = topic_meta()
    tm.to_csv(RES / "topic_meta.csv", index=False)
    logger.info(f"topics: {len(tm)}  fields: {tm.field.nunique()}  subfields: {tm.subfield.nunique()}")
    sf = source_field()
    sf.to_parquet(RES / "source_field.parquet", index=False)
    logger.info(f"sources: {len(sf)}  labelled: {sf.field.notna().sum()}  types: {sf.type.value_counts().head(6).to_dict()}")
    fields = tm.drop_duplicates("field")[["field", "field_name"]].sort_values("field")
    fields.to_csv(RES / "field_names.csv", index=False)


if __name__ == "__main__":
    main()
