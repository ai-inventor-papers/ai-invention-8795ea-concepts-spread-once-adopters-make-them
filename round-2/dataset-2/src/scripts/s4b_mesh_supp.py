#!/usr/bin/env python3
"""STEP 4b: MeSH Supplementary Concept Records (C-numbers) for the Wikidata P486 values not found in desc2026.

Streams supp2026.gz once and keeps only the needed UIs -> work/mesh_supp.parquet.
"""
from __future__ import annotations

import gzip

import pandas as pd
from lxml import etree
from loguru import logger

from common import RAW, WORK, setup_logging


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s4b_mesh_supp")
    need = set(pd.read_csv(WORK / "p486_not_in_desc.csv").p486)
    logger.info(f"{len(need)} P486 values not in desc2026; {sum(u.startswith('C') for u in need)} are C-numbers")
    rows = []
    with gzip.open(RAW / "mesh" / "supp2026.gz", "rb") as fh:
        for _, el in etree.iterparse(fh, events=("end",), tag="SupplementalRecord", load_dtd=False, no_network=True,
                                     resolve_entities=False, huge_tree=True):
            ui = el.findtext("SupplementalRecordUI")
            if ui in need:
                di = el.find("DateIntroduced")
                y = int(di.findtext("Year")) if di is not None and di.findtext("Year") else None
                mapped = [d.text.lstrip("*") for d in el.findall("HeadingMappedToList/HeadingMappedTo/DescriptorReferredTo/DescriptorUI") if d.text]
                terms = sorted({t.text for t in el.findall("ConceptList/Concept/TermList/Term/String") if t.text})
                rows.append({"mesh_ui": ui, "mesh_name": el.findtext("SupplementalRecordName/String"),
                             "scr_class": el.get("SCRClass"), "date_introduced_year": y,
                             "heading_mapped_to": mapped, "entry_terms": terms,
                             "note": (el.findtext("Note") or "").strip()[:300] or None})
            el.clear()
            while el.getprevious() is not None:
                del el.getparent()[0]
    df = pd.DataFrame(rows)
    df.to_parquet(WORK / "mesh_supp.parquet", index=False)
    logger.info(f"found {len(df)} of {len(need)}; year range {df.date_introduced_year.min()}-{df.date_introduced_year.max()}")


if __name__ == "__main__":
    main()
