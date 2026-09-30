#!/usr/bin/env python3
"""STEP 4: stream the NLM MeSH descriptor XML (desc2026) into a compact table.

2026 DTD: DateIntroduced replaces DateEstablished; DateCreated/DateRevised were removed from DescriptorRecord
(DateCreated survives only on Term). Year rule (recorded per row in mesh_year_rule):
  1. year(DateIntroduced)                        -> 'date_introduced'
  2. else the leading year of HistoryNote        -> 'history_note'
  3. else the earliest Term DateCreated year     -> 'term_date_created_min'
HistoryNote begins with a 2-digit year (e.g. '91(75); ...' = current form 1991, earlier form 1975).
"""
from __future__ import annotations

import gzip
import json
import re

import pandas as pd
from lxml import etree
from loguru import logger

from common import RAW, WORK, setup_logging

SRC = RAW / "mesh" / "desc2026.gz"
FILE_YEAR = 2026


def _yy(s: str) -> int:
    y = int(s)
    return 1900 + y if y >= 30 else 2000 + y


def hist_years(note: str | None) -> tuple[int | None, int | None]:
    if not note:
        return None, None
    m = re.match(r"\s*(\d{2,4})\s*(?:\((\d{2,4})\))?", note)
    if not m:
        return None, None
    a = int(m.group(1)) if len(m.group(1)) == 4 else _yy(m.group(1))
    b = None
    if m.group(2):
        b = int(m.group(2)) if len(m.group(2)) == 4 else _yy(m.group(2))
    return a, b


def _date(el) -> str | None:
    if el is None:
        return None
    y, mo, d = el.findtext("Year"), el.findtext("Month"), el.findtext("Day")
    return f"{y}-{mo}-{d}" if y else None


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s4_mesh")
    rows = []
    with gzip.open(SRC, "rb") as fh:
        for _, el in etree.iterparse(fh, events=("end",), tag="DescriptorRecord", load_dtd=False,
                                     no_network=True, resolve_entities=False, huge_tree=True):
            ui = el.findtext("DescriptorUI")
            name = el.findtext("DescriptorName/String")
            di = _date(el.find("DateIntroduced"))
            lu = _date(el.find("LastUpdated"))
            hn = (el.findtext("HistoryNote") or "").strip()
            pmn = (el.findtext("PublicMeSHNote") or "").strip()
            prev = [p.text.strip() for p in el.findall("PreviousIndexingList/PreviousIndexing") if p.text]
            trees = [t.text.strip() for t in el.findall("TreeNumberList/TreeNumber") if t.text]
            terms, term_dates, scope = [], [], None
            for c in el.findall("ConceptList/Concept"):
                if c.get("PreferredConceptYN") == "Y" and scope is None:
                    sn = (c.findtext("ScopeNote") or "").strip()
                    scope = re.split(r"(?<=[.;])\s", sn, maxsplit=1)[0][:400] if sn else None
                for t in c.findall("TermList/Term"):
                    s = t.findtext("String")
                    if s:
                        terms.append(s)
                    dc = _date(t.find("DateCreated"))
                    if dc:
                        term_dates.append(dc)
            hy, hy_prev = hist_years(hn)
            y_int = int(di[:4]) if di else None
            if y_int:
                best, rule = y_int, "date_introduced"
            elif hy:
                best, rule = hy, "history_note"
            elif term_dates:
                best, rule = int(min(term_dates)[:4]), "term_date_created_min"
            else:
                best, rule = None, "none"
            rows.append({
                "mesh_ui": ui, "mesh_name": name, "descriptor_class": el.get("DescriptorClass"),
                "date_introduced": di, "last_updated": lu, "history_note": hn[:500] or None,
                "public_mesh_note": pmn[:500] or None, "previous_indexing": prev, "tree_numbers": trees,
                "top_branches": sorted({t[0] for t in trees}), "entry_terms": sorted(set(terms)),
                "term_date_created_min": min(term_dates) if term_dates else None,
                "scope_first_sentence": scope, "history_year": hy, "history_year_earlier": hy_prev,
                "mesh_year_best": best, "mesh_year_rule": rule,
                "mesh_baseline": bool(best is not None and best <= 1966),
            })
            el.clear()
            while el.getprevious() is not None:
                del el.getparent()[0]
    df = pd.DataFrame(rows)
    df.to_parquet(WORK / "mesh_desc.parquet", index=False)
    logger.info(f"{len(df)} descriptors; rule counts {df.mesh_year_rule.value_counts().to_dict()}")
    logger.info(f"year range {df.mesh_year_best.min()}-{df.mesh_year_best.max()}; baseline {df.mesh_baseline.sum()}")
    yh = (df.mesh_year_best // 5 * 5).value_counts().sort_index()
    logger.info(f"5y histogram {yh.to_dict()}")
    agree = df.dropna(subset=["history_year"])
    d = (agree["mesh_year_best"] - agree["history_year"])
    logger.info(f"DateIntroduced - HistoryNote year: {d.describe().to_dict()}; share equal {float((d == 0).mean()):.3f}")
    assert df.mesh_year_best.dropna().between(1954, FILE_YEAR).all()
    (WORK / "mesh_stats.json").write_text(json.dumps({"n": len(df), "rules": df.mesh_year_rule.value_counts().to_dict(),
                                                      "hist5": {int(k): int(v) for k, v in yh.items()}}, indent=1))


if __name__ == "__main__":
    main()
