#!/usr/bin/env python3
"""Step 0.4: legacy-concept lexicon from the OpenAlex concepts entity snapshot (0 credits); frozen by SHA-256."""
import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from loguru import logger
from wordfreq import zipf_frequency

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from config import INP, RES  # noqa: E402
from matcher import norm_py  # noqa: E402

logger.remove(); logger.add(sys.stdout, format="{time:HH:mm:ss}|{level:<7}|{message}")


@logger.catch(reraise=True)
def main() -> None:
    t = pa.concat_tables([pq.read_table(p, columns=["id", "display_name", "level", "wikidata", "description",
                                                    "works_count"]) for p in sorted((INP / "concepts").glob("*.parquet"))])
    df = t.to_pandas()
    n0 = len(df)
    df = df[df.level.between(2, 5) & df.wikidata.notna()].copy()
    df["oa_int"] = df.id.str.slice(22).astype("int64")
    df["name"] = df.display_name.astype(str).str.replace(r"\s*\(.*?\)\s*", " ", regex=True).str.strip()
    df["form"] = df.name.map(norm_py).str.strip()
    ntok = df.form.str.split(" ").str.len()
    single = ntok == 1
    drop_short = single & (df.form.str.len() <= 3)
    zf = df.form.where(single, "").map(lambda w: zipf_frequency(w, "en") if w else 0.0)
    drop_common = single & ((df.form.str.len() < 6) | (zf >= 3.5))
    drop_empty = df.form.str.len() < 3
    reasons = pd.Series("", index=df.index)
    reasons[drop_empty] = "empty"; reasons[drop_short] = "single_token_le3"; reasons[drop_common & ~drop_short] = "single_token_common_or_lt6"
    dropped = df[reasons != ""].assign(reason=reasons[reasons != ""])
    df = df[reasons == ""]
    df = df.drop_duplicates("oa_int").sort_values("oa_int").reset_index(drop=True)
    df["concept_idx"] = range(len(df))
    lex = df[["concept_idx", "oa_int", "id", "name", "form", "level", "wikidata", "description", "works_count"]]
    lex.to_parquet(RES / "lexicon.parquet", index=False)
    dropped[["id", "display_name", "level", "reason"]].to_csv(RES / "lexicon_dropped.csv", index=False)
    h = hashlib.sha256((RES / "lexicon.parquet").read_bytes()).hexdigest()
    (RES / "lexicon_hash.txt").write_text(h + "\n")
    logger.info(f"concepts {n0} -> levels2-5+wikidata -> lexicon {len(lex)} (dropped {len(dropped)}); sha256 {h[:12]}")
    (RES / "lexicon_summary.json").write_text(json.dumps({"n_entity": n0, "n_lexicon": len(lex), "n_dropped": len(dropped),
        "dropped_by_reason": dropped.reason.value_counts().to_dict(), "levels": lex.level.value_counts().to_dict(),
        "aliases": "NOT USED (Wikidata alias fetch skipped for time; see deviations.json)", "sha256": h}, indent=1))


if __name__ == "__main__":
    main()
