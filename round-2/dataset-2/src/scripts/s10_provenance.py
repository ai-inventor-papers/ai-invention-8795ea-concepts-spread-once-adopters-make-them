#!/usr/bin/env python3
"""Write out/sources.json: URL, version, retrieval date, sha256, licence, record count and known biases per source,
plus the P2 sources that were attempted and not delivered."""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from common import CACHE, OUT, RAW, WORK, sha256_file

RETRIEVED = "2026-09-28"


def sh(p: Path) -> str | None:
    return sha256_file(p) if p.exists() else None


def main() -> None:
    tax = pd.read_parquet(WORK / "tax_entries.parquet")
    lst = pd.read_parquet(WORK / "list_entries.parquet")
    n = lambda s, v=None: int(((tax.source == s) & ((tax.version == v) if v is not None else True)).sum())
    nl = lambda s: int((lst.source == s).sum())
    yrs = lambda s: sorted({int(y) for y in lst[lst.source == s].year})
    wp = CACHE / "wikipedia" / "first_rev.jsonl"
    n_wp = sum(1 for _ in wp.open()) if wp.exists() else 0
    cal = json.loads((WORK / "wp_calibration.json").read_text()) if (WORK / "wp_calibration.json").exists() else {}
    wdp = json.loads((CACHE / "wikidata" / "properties.json").read_text())
    concept_files = sorted((RAW / "concepts").rglob("*.parquet"))
    src = [
        {"id": "openalex_concepts_parquet", "role": "concept frame", "url": "https://openalex.s3.amazonaws.com/data/parquet/concepts/manifest.json",
         "version": "snapshot parts updated_date=2026-09-11..", "retrieved": RETRIEVED, "records": 65026,
         "sha256": {f.parent.name: sha256_file(f) for f in concept_files}, "licence": "CC0 (OpenAlex)",
         "notes": "zero API credits; this parquet leaves ancestors/international/ids.mag empty"},
        {"id": "openalex_concepts_legacy_json", "role": "ancestors, MAG ids, English name variants",
         "url": "https://openalex.s3.amazonaws.com/legacy-data/concepts/manifest", "retrieved": RETRIEVED,
         "records": 65073, "licence": "CC0 (OpenAlex)", "notes": "same concept ids; latest record per id kept"},
        {"id": "openalex_fields", "role": "26 field ids for the crosswalk",
         "url": "https://openalex.s3.amazonaws.com/data/parquet/fields/updated_date=2026-09-23/part_0000.parquet",
         "retrieved": RETRIEVED, "records": 26, "sha256": sh(RAW / "fields" / "fields.parquet"), "licence": "CC0"},
        {"id": "wikidata", "role": "P486/P6694/P672 MeSH ids, P2179 ACM 2012, P3285 MSC, P571 inception, P575 discovery, P61, P31/P279/P361, P6366, sitelinks, aliases",
         "url": "https://www.wikidata.org/w/api.php?action=wbgetentities (50 QIDs per call)", "retrieved": RETRIEVED,
         "records": 58910, "licence": "CC0", "properties_verified": wdp.get("verify", {}).get("verified"),
         "property_search": {k_: [x["id"] + ":" + str(x["label"]) for x in v_] for k_, v_ in wdp.get("verify", {}).get("search", {}).items()},
         "notes": "No Wikidata property for PhySH or JEL codes was found by wbsearchentities(type=property). maxlag=5 was honoured "
                  "for 3 retries per request; while WDQS lag stayed >5 s requests were sent without maxlag (read-only, 4 concurrent)."},
        {"id": "wikipedia_en_first_revision", "role": "article creation dates",
         "url": "https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvdir=newer&rvlimit=1 (one title per call)",
         "retrieved": RETRIEVED, "records_exact": n_wp, "licence": "CC BY-SA 4.0 (metadata only stored)",
         "notes": "Throttled to ~2-3 req/s by Wikimedia for this shared IP; titles fetched level 2 first, random order within level. "
                  "Remaining titles carry a page-id-based estimate (see pageid calibration)."},
        {"id": "wikipedia_en_pageids", "role": "page ids for every title (50 per call) -> isotonic creation-date estimate",
         "url": "https://en.wikipedia.org/w/api.php?action=query&prop=info", "retrieved": RETRIEVED, "records": 58932,
         "calibration": cal},
        {"id": "mesh_descriptors", "role": "MeSH descriptor introduction years", "url": "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2026.gz",
         "version": "MeSH 2026 (DTD nlmdescriptorrecordset_20260101)", "retrieved": RETRIEVED, "records": 31110,
         "sha256": sh(RAW / "mesh" / "desc2026.gz"), "licence": "NLM terms (public, attribution requested)",
         "notes": "2026 DTD: DateIntroduced replaces DateEstablished; DateCreated/DateRevised removed from DescriptorRecord"},
        {"id": "mesh_supplementary", "role": "SCRs for Wikidata P486 C-numbers", "url": "https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/supp2026.gz",
         "retrieved": RETRIEVED, "records": int(len(pd.read_parquet(WORK / "mesh_supp.parquet"))), "sha256": sh(RAW / "mesh" / "supp2026.gz"),
         "licence": "NLM terms"},
        {"id": "acm_ccs_2012", "url": "https://dl.acm.org/pb-assets/dl_ccs/acm_ccs2012-1626988337597.xml", "version": 2012,
         "retrieved": RETRIEVED, "records": n("acm_ccs", 2012), "sha256": sh(RAW / "tax" / "acm_ccs2012.xml"),
         "licence": "ACM: free for educational and research use"},
        {"id": "acm_ccs_1998", "url": "https://www.mi.sanu.ac.rs/~zorano/acm/ccs98.html", "version": 1998,
         "retrieved": RETRIEVED, "records": n("acm_ccs", 1998), "sha256": sh(RAW / "tax" / "ccs98.html"),
         "licence": "ACM copyright notice reproduced in the mirror (research use)",
         "notes": "mirror of the ACM 1998 CCS page (acm.org returned 403); its NEW! markers flag nodes added relative to CCS 1991"},
        {"id": "msc_2020", "url": "https://msc2020.org/MSC_2020.csv", "version": 2020, "retrieved": RETRIEVED,
         "records": n("msc", 2020), "sha256": sh(RAW / "tax" / "MSC_2020.csv"), "licence": "CC BY-NC-SA 4.0"},
        {"id": "msc_2010", "url": "https://cran.r-project.org/web/classifications/MSC-2010.html", "version": 2010,
         "retrieved": RETRIEVED, "records": n("msc", 2010), "sha256": sh(RAW / "tax" / "cran_MSC-2010.html"),
         "licence": "CC BY-NC-SA (AMS/zbMATH)"},
        {"id": "msc_2000", "url": "https://mathscinet.ams.org/msnhtml/classification.pdf", "version": 2000,
         "retrieved": RETRIEVED, "records": n("msc", 2000), "sha256": sh(RAW / "tax" / "msc2000.pdf"),
         "licence": "AMS", "notes": "parsed from the PDF (code line followed by label lines); running heads removed"},
        {"id": "pacs_2010", "url": "https://raw.githubusercontent.com/canderson/PACS/master/pacs.yml", "version": 2010,
         "retrieved": RETRIEVED, "records": n("pacs_physh", 2010), "sha256": sh(RAW / "tax" / "pacs.yml"),
         "licence": "AIP PACS content; repository has no licence file (codes/labels/structure only stored)"},
        {"id": "physh", "url": "https://raw.githubusercontent.com/physh-org/PhySH/master/physh.ttl", "version": "current (first release 2016)",
         "retrieved": RETRIEVED, "records": n("pacs_physh", 2016), "sha256": sh(RAW / "tax" / "physh.ttl"), "licence": "CC0 1.0"},
        {"id": "jel", "url": "https://www.aeaweb.org/econlit/classificationTree.xml", "version": "current, undated",
         "retrieved": RETRIEVED, "records": int((tax.source == "jel").sum()), "sha256": sh(RAW / "tax" / "jel_classificationTree.xml"),
         "licence": "AEA", "notes": "present-day membership only (year_known=false)"},
        {"id": "nature_methods_moty", "url": "https://en.wikipedia.org/wiki/Nature_Methods (revision in item url)",
         "retrieved": RETRIEVED, "records": nl("nature_methods_moty"), "years": yrs("nature_methods_moty"),
         "sha256": sh(RAW / "lists" / "wp_Nature_Methods.json"), "licence": "CC BY-SA (facts only)"},
        {"id": "science_boty", "url": "https://en.wikipedia.org/wiki/Breakthrough_of_the_Year", "retrieved": RETRIEVED,
         "records": nl("science_boty"), "years": yrs("science_boty"), "sha256": sh(RAW / "lists" / "wp_Breakthrough_of_the_Year.json"),
         "licence": "CC BY-SA (facts only)",
         "notes": "winners 1996-2025 only; runners-up NOT delivered (science.org returns 403 to scripted access); 1989-1995 'Molecule of the Year' not listed as bullets on the page"},
        {"id": "physics_world_boty", "url": "https://en.wikipedia.org/wiki/Physics_World", "retrieved": RETRIEVED,
         "records": nl("physics_world_boty"), "years": yrs("physics_world_boty"), "sha256": sh(RAW / "lists" / "wp_Physics_World.json"),
         "licence": "CC BY-SA (facts only)", "notes": "winner + top-10 per year 2009-2024 from Wikipedia; 2025 (winner + 9 others) transcribed from physicsworld.com (cache/raw/lists/physics_world_2025.json)"},
        {"id": "mit_tr10", "url": "https://github.com/envisioning/hindsight/blob/main/data/normalized/claims/mit-tr-10-breakthrough.json",
         "retrieved": RETRIEVED, "records": nl("mit_tr10"), "years": yrs("mit_tr10"),
         "sha256": sh(RAW / "lists" / "hindsight_mit-tr-10-breakthrough.json"), "licence": "CC BY 4.0 (Envisioning, Hindsight)",
         "notes": "secondary compilation (pre-release repository created 2026-09-27); spot check: 2010 list 10/10 identical to technologyreview.com/10-breakthrough-technologies/2010"},
        {"id": "gartner_hype_cycle", "url": "https://github.com/envisioning/hindsight/blob/main/data/normalized/claims/gartner-hype-cycle.json",
         "retrieved": RETRIEVED, "records": nl("gartner_hype_cycle"), "years": yrs("gartner_hype_cycle"),
         "sha256": sh(RAW / "lists" / "hindsight_gartner-hype-cycle.json"), "licence": "CC BY 4.0 (Envisioning, Hindsight); names/year/phase only, no Gartner graphics",
         "notes": "labels transcribed from the charts by Hindsight (their extraction confidence notes are kept upstream); phase is present for a subset only; "
                  "spot check: 2023 edition has 25 entries, matching Gartner's published count; gartner.com returns 403 to scripted access"},
        {"id": "research_fronts", "url": "http://english.casisd.cas.cn/research/rp/ (English 'Research Fronts YYYY' reports, CAS-ISD / NSL-CAS / Clarivate)",
         "retrieved": RETRIEVED, "records": nl("research_fronts"), "years": yrs("research_fronts"),
         "sha256": {f.name: sha256_file(f) for f in sorted((RAW / "research_fronts").glob("rf_*.pdf"))},
         "licence": "report text (c) CAS-ISD/Clarivate; only front names, ranks and counts are stored",
         "notes": "hot (top 10 per broad field) and emerging fronts per report year, parsed from the report tables "
                  "(rank | front | core papers | citations | mean year of core papers). Clarivate's own download page is "
                  "lead-gen gated; the identical English reports are public on the CAS-ISD site. Front names are long "
                  "phrases, so most links are relation 'narrower'."},
    ]
    rf_years = set(yrs("research_fronts"))
    not_delivered = [
        {"id": "research_fronts_missing_years", "status": "partially delivered",
         "reason": f"delivered {sorted(rf_years)}; 2016 report lists fronts without ranks/counts (layout not parseable reliably); "
                   "2014-2015 English reports are not on the CAS-ISD page; any other missing year failed to download/parse"},
        {"id": "science_boty_runners_up", "status": "attempted, not delivered", "reason": "science.org returns HTTP 403 to scripted requests"},
        {"id": "pacs_2003_2006_2008_editions", "status": "not attempted within time box", "reason": "only PACS 2010 is available in structured form"},
        {"id": "science_molecule_of_the_year_1989_1995", "status": "not delivered", "reason": "not listed as parseable items on the Wikipedia page"},
    ]
    llm = json.loads((OUT / "llm_cost.json").read_text())
    (OUT / "sources.json").write_text(json.dumps({"retrieved": RETRIEVED, "openalex_api_credits_used": 0,
                                                  "llm_spend_usd": llm.get("total_usd"), "sources": src,
                                                  "attempted_not_delivered": not_delivered}, indent=1, default=str))
    print(f"sources.json written ({len(src)} sources, {len(not_delivered)} not delivered)")


if __name__ == "__main__":
    main()
