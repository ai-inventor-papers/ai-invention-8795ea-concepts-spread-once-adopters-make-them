#!/usr/bin/env python3
"""STEP 6b: Clarivate/CAS 'Research Fronts' reports 2016-2025 (English PDFs hosted by CAS-ISD) -> list items.

Each report has, per broad field, a 'Top 10 hot Research Fronts' table and an 'emerging Research Fronts' table:
rank | front name | core papers | citations | mean year of core papers. Output: work/research_fronts.parquet
(appended to the curated lists by s6_lists.py when present).
"""
from __future__ import annotations

import re

import pandas as pd
import pymupdf
from loguru import logger

from common import RAW, WORK, setup_logging

SRC = RAW / "research_fronts"
URL = {}
for line in (SRC / "main.txt").read_text().splitlines():
    y, u = line.split()
    URL[int(y)] = u
INT = re.compile(r"^\d{1,5}$")
YEARF = re.compile(r"^(19|20)\d\d(\.\d)?$")
TITLE = re.compile(r"Table\s*\d+\s*[:：]?\s*(.*Research Fronts?.*)", re.I)


def parse_report(year: int) -> list[dict]:
    doc = pymupdf.open(SRC / f"rf_{year}.pdf")
    lines = []
    for p in doc:
        lines += [ln.strip() for ln in p.get_text().splitlines() if ln.strip()]
    rows = []
    i = 0
    while i < len(lines):
        m = TITLE.match(lines[i])
        if not m:
            i += 1
            continue
        title = m.group(1)
        j = i + 1
        while j < len(lines) and j < i + 4 and not TITLE.match(lines[j]) and not re.search(r"Mean Year|Year", lines[j]):
            title += " " + lines[j]   # wrapped title
            j += 1
        kind = "emerging" if re.search(r"emerging", title, re.I) else ("hot" if re.search(r"top\s*10|hot", title, re.I) else None)
        title = re.split(r"\s+(?:Rank|Number|No\.|Hot Research Fronts?|Emerging Research Fronts?|Core [Pp]apers)\b", title)[0]
        fm = re.search(r"\bin\s+(?:the\s+)?(?:field of\s+)?(.+?)\s*$", title, re.I)
        field = fm.group(1).strip().rstrip(".").lower() if fm else None
        # skip header cells until the first rank '1'
        k = i + 1
        while k < len(lines) and k < i + 15 and lines[k] != "1":
            k += 1
        if k >= len(lines) or lines[k] != "1" or kind is None:
            i += 1
            continue
        expected, n_found = 1, 0
        while k < len(lines) and lines[k] == str(expected):
            name, q = [], k + 1
            while q < len(lines) and q < k + 12:
                if (q + 2 < len(lines) and INT.match(lines[q]) and INT.match(lines[q + 1]) and YEARF.match(lines[q + 2])):
                    break
                name.append(lines[q])
                q += 1
            if (q + 2 >= len(lines) or not name or not INT.match(lines[q]) or not INT.match(lines[q + 1])
                    or not YEARF.match(lines[q + 2])):
                break
            rows.append({"year": year, "role": f"{kind}_research_front", "rank": expected, "field": field,
                         "item_text": re.sub(r"\s+", " ", " ".join(name)).strip(),
                         "core_papers": int(lines[q]), "citations": int(lines[q + 1]), "mean_year_core": float(lines[q + 2]),
                         "table_title": title[:160], "url": URL.get(year)})
            n_found += 1
            expected += 1
            k = q + 3
        i = k if n_found else i + 1
    return rows


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s6b_research_fronts")
    allr = []
    for y in sorted(URL):
        f = SRC / f"rf_{y}.pdf"
        try:
            r = parse_report(y)
        except (RuntimeError, ValueError, pymupdf.FileDataError) as e:   # truncated download
            logger.error(f"{y}: {e}")
            continue
        logger.info(f"{y}: {len(r)} fronts ({sum(x['role'].startswith('hot') for x in r)} hot, "
                    f"{sum(x['role'].startswith('emerging') for x in r)} emerging) in {len({x['field'] for x in r})} fields")
        allr += r
    df = pd.DataFrame(allr).drop_duplicates(["year", "role", "field", "rank"])
    df.to_parquet(WORK / "research_fronts.parquet", index=False)
    logger.info(f"total {len(df)}; sample {df.sample(min(5, len(df)), random_state=0)[['year', 'role', 'field', 'item_text']].to_dict('records')}")


if __name__ == "__main__":
    main()
