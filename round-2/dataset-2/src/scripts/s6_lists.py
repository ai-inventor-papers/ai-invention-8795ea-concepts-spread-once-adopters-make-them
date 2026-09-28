#!/usr/bin/env python3
"""STEP 6: curated yearly lists -> work/list_entries.parquet (one row per list item, stored raw).

Nature Methods Method of the Year (2007-2025), Science Breakthrough of the Year winners (1996-2025) and
Physics World Breakthrough of the Year winners + top-10 (2009-2024) come from the English Wikipedia pages
(wikitext of a pinned revision). MIT Technology Review TR10 and the Gartner Hype Cycle for Emerging
Technologies come from Envisioning's Hindsight normalized claims (CC BY 4.0; spot-checked, see README).
Wiki links inside an item ([[Target|text]]) are kept: they give exact enwiki titles for matching.
"""
from __future__ import annotations

import json
import re

import pandas as pd
from loguru import logger

from common import RAW, WORK, norm_label, setup_logging

L = RAW / "lists"
LINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|([^\]]+))?\]\]")


def wiki_clean(s: str) -> tuple[str, list[str]]:
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref[^>]*>.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"<[^>]+>", "", s)
    links = [m.group(1).strip() for m in LINK.finditer(s)]
    s = LINK.sub(lambda m: (m.group(2) or m.group(1)).strip(), s)
    s = re.sub(r"\{\{[^{}]*\}\}", "", s)
    s = s.replace("'''", "").replace("''", "").replace("&nbsp;", " ")
    s = re.sub(r"\s+", " ", s).strip(" \"'.:;")
    return s, links


def _wt(name: str) -> tuple[str, int]:
    d = json.loads((L / f"wp_{name}.json").read_text())["parse"]
    return d["wikitext"], d["revid"]


def nature_methods() -> list[dict]:
    s, rev = _wt("Nature_Methods")
    i = s.find("=== Selections by year ===")
    tab = s[i:s.find("|}", i)]
    rows = []
    for m in re.finditer(r"^\| (\d{4}) \|\| (.*?) \|\| (.*?) \|\| (.*)$", tab, flags=re.M):
        name, links = wiki_clean(m.group(2))
        desc, dlinks = wiki_clean(m.group(3))
        doi = re.search(r"doi=([^ |}]+)", m.group(4))
        rows.append({"source": "nature_methods_moty", "year": int(m.group(1)), "rank": 1, "role": "winner",
                     "item_text": name, "descriptor": desc, "wiki_links": links, "descriptor_links": dlinks,
                     "phase": None, "url": f"https://en.wikipedia.org/w/index.php?oldid={rev}",
                     "primary_ref": f"https://doi.org/{doi.group(1)}" if doi else None})
    return rows


def science_boty() -> list[dict]:
    s, rev = _wt("Breakthrough_of_the_Year")
    rows = []
    for m in re.finditer(r"^\* ?(\d{4}): (.*)$", s, flags=re.M):
        txt, links = wiki_clean(m.group(2))
        url = re.search(r"url=(https?://[^ |}]+)", m.group(2))
        rows.append({"source": "science_boty", "year": int(m.group(1)), "rank": 1, "role": "winner",
                     "item_text": txt, "descriptor": None, "wiki_links": links, "descriptor_links": [],
                     "phase": None, "url": f"https://en.wikipedia.org/w/index.php?oldid={rev}",
                     "primary_ref": url.group(1) if url else None})
    # Molecule of the Year 1989-1995 (the award's earlier name) if listed as bullets in the page body
    return rows


def physics_world() -> list[dict]:
    s, rev = _wt("Physics_World")
    i = s.find("Top 10 works and winners of the Breakthrough of the Year")
    j = s.find("Book of the Year", i + 10)
    sec = s[i:j if j > 0 else None]
    rows = []
    parts = re.split(r"^'''(\d{4})''':", sec, flags=re.M)
    for k in range(1, len(parts), 2):
        yr, body = int(parts[k]), parts[k + 1]
        lines = body.split("\n")
        win, wl = wiki_clean(lines[0])
        url = re.search(r"url=(https?://[^ |}]+)", body)
        rows.append({"source": "physics_world_boty", "year": yr, "rank": 1, "role": "winner", "item_text": win,
                     "descriptor": None, "wiki_links": wl, "descriptor_links": [], "phase": None,
                     "url": f"https://en.wikipedia.org/w/index.php?oldid={rev}",
                     "primary_ref": url.group(1) if url else None})
        r = 2
        for ln in lines[1:]:
            if ln.strip().startswith("*"):
                t, tl = wiki_clean(ln.strip().lstrip("*"))
                if t:
                    rows.append({"source": "physics_world_boty", "year": yr, "rank": r, "role": "top10",
                                 "item_text": t, "descriptor": None, "wiki_links": tl, "descriptor_links": [],
                                 "phase": None, "url": f"https://en.wikipedia.org/w/index.php?oldid={rev}",
                                 "primary_ref": None})
                    r += 1
    return rows


def hindsight(name: str, source: str) -> list[dict]:
    d = json.loads((L / f"hindsight_{name}.json").read_text())
    rows = []
    for x in d:
        yr = int(x["source_edition_id"].rsplit("-", 1)[1])
        if source == "mit_tr10":
            item = x["statement"].split(": ", 1)[1].rstrip(".") if ": " in x["statement"] else x["quote"]
            desc = x.get("quote")
            rank = int(re.search(r"(\d+)", x.get("position") or "0").group(1) or 0)
            role = "list_member"
        else:
            item = x["quote"]
            desc = None
            m = re.search(r"rank (\d+)", x.get("position") or "")
            rank = int(m.group(1)) if m else None
            role = "hype_cycle_entry"
        rows.append({"source": source, "year": yr, "rank": rank, "role": role, "item_text": item,
                     "descriptor": desc, "wiki_links": [], "descriptor_links": [], "phase": x.get("phase"),
                     "url": "https://github.com/envisioning/hindsight/blob/main/data/normalized/claims/" + name + ".json",
                     "primary_ref": x["id"], "subject_ids": x.get("subject_ids", [])})
    return rows


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s6_lists")
    rows = []
    for fn, args in ((nature_methods, ()), (science_boty, ()), (physics_world, ()),
                     (hindsight, ("mit-tr-10-breakthrough", "mit_tr10")),
                     (hindsight, ("gartner-hype-cycle", "gartner_hype_cycle"))):
        r = fn(*args)
        logger.info(f"{fn.__name__}{args}: {len(r)} items; years {min(x['year'] for x in r)}-{max(x['year'] for x in r)}")
        rows.extend(r)
    rf_p = WORK / "research_fronts.parquet"
    if rf_p.exists():   # Clarivate/CAS Research Fronts (s6b_research_fronts.py)
        rf = pd.read_parquet(rf_p)
        for r in rf.itertuples(index=False):
            rows.append({"source": "research_fronts", "year": int(r.year), "rank": int(r.rank), "role": r.role,
                         "item_text": r.item_text,
                         "descriptor": f"{r.role.replace('_', ' ')} in {r.field}; mean publication year of core papers {r.mean_year_core}",
                         "wiki_links": [], "descriptor_links": [], "phase": None, "url": r.url,
                         "primary_ref": f"core_papers={r.core_papers}; citations={r.citations}; field={r.field}"})
        logger.info(f"research_fronts: {len(rf)} items; years {sorted(rf.year.unique())}")
    pw25 = L / "physics_world_2025.json"   # appended last so earlier entry ids stay stable
    if pw25.exists():
        d = json.loads(pw25.read_text())
        for it in d["items"]:
            rows.append({"source": "physics_world_boty", "year": 2025, "rank": it["rank"], "role": it["role"],
                         "item_text": it["item_text"], "descriptor": it["descriptor"], "wiki_links": [],
                         "descriptor_links": [], "phase": None, "url": d["source_urls"][0 if it["rank"] > 1 else 1],
                         "primary_ref": "physicsworld.com (transcribed)"})
    df = pd.DataFrame(rows)
    df["label_norm"] = df.item_text.map(norm_label)
    df["entry_id"] = df.apply(lambda r: f"{r.source}:{r.year}:{r['rank'] if pd.notna(r['rank']) else 'x'}:{r.name}", axis=1)
    df.to_parquet(WORK / "list_entries.parquet", index=False)
    for src in df.source.unique():
        logger.info(f"{src}: {df[df.source == src].head(3)[['year', 'item_text', 'wiki_links']].to_dict('records')}")
    # known answers
    nm = df[df.source == "nature_methods_moty"].set_index("year").item_text.to_dict()
    assert "ptogenetic" in nm[2010] and "luripotent" in nm[2009] and "uper-resolution" in nm[2008], nm
    sb = df[df.source == "science_boty"].set_index("year").item_text.to_dict()
    assert "CRISPR" in sb[2015], sb.get(2015)


if __name__ == "__main__":
    main()
