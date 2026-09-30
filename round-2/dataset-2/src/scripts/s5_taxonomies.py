#!/usr/bin/env python3
"""STEP 5: parse every node of the dated classification schemes into one table (work/tax_entries.parquet).

Columns: source, version (int year), code, label, parent, alt_labels, flags (dict), label_norm.
Schemes: ACM CCS 1998 (HTML mirror of the ACM page, incl. its NEW! markers vs CCS 1991) and 2012 (SKOS),
MSC 2000 (AMS PDF), 2010 (CRAN HTML), 2020 (msc2020.org CSV), PACS 2010 (canderson/PACS YAML),
PhySH (physh-org TTL; first release 2016), JEL (AEA XML; undated, present-day membership only).
"""
from __future__ import annotations

import html
import json
import re

import pandas as pd
import yaml
from bs4 import BeautifulSoup
from loguru import logger

from common import RAW, WORK, norm_label, setup_logging

T = RAW / "tax"


def _clean(s: str) -> str:
    s = html.unescape(s)
    s = re.sub(r"\s*\[(?:See also|For [^\]]*|See [^\]]*)[^\]]*\]", "", s)   # MSC cross-reference notes
    s = re.sub(r"\s+", " ", s).strip(" .;")
    return s


def acm2012() -> list[dict]:
    from lxml import etree
    ns = {"skos": "http://www.w3.org/2004/02/skos/core#", "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}
    root = etree.parse(str(T / "acm_ccs2012.xml")).getroot()
    rows = []
    for c in root.findall("skos:Concept", ns):
        cid = c.get("{%s}about" % ns["rdf"])
        pl = c.findtext("skos:prefLabel", namespaces=ns)
        alts = [a.text for a in c.findall("skos:altLabel", ns) if a.text]
        br = [b.get("{%s}resource" % ns["rdf"]) for b in c.findall("skos:broader", ns)]
        rows.append({"source": "acm_ccs", "version": 2012, "code": cid, "label": pl, "parent": br[0] if br else None,
                     "alt_labels": alts, "flags": {"n_broader": len(br)}})
    return rows


def acm1998() -> list[dict]:
    s = (T / "ccs98.html").read_text(encoding="latin-1")
    start = s.find('<a name = "A">')
    body = s[start:] if start > 0 else s
    rows = []
    cur_code = None
    for line in body.splitlines():
        m = re.match(r'\s*<li><a name = "([A-K](?:\.[0-9m]+)*)">[^<]*</a>\s*(.*)', line)
        if m:
            code, rest = m.group(1), m.group(2)
            new = "NEW!" in rest
            lab = _clean(re.sub(r"<[^>]+>", "", rest.split("(<a")[0]).replace("(NEW!)", ""))
            parent = code.rsplit(".", 1)[0] if "." in code else None
            rows.append({"source": "acm_ccs", "version": 1998, "code": code, "label": lab.title() if lab.isupper() else lab,
                         "parent": parent, "alt_labels": [], "flags": {"new_in_1998": new, "kind": "category",
                                                                          "retired_marker": "note2" in rest}})
            cur_code = code
            continue
        m2 = re.match(r"\s*<li><em>(.*?)</em>(.*)", line)
        if m2 and cur_code:
            inner = m2.group(1)
            new = "NEW!" in inner or "NEW!" in m2.group(2)
            lab = _clean(re.sub(r"<[^>]+>", "", inner).replace("NEW!", ""))
            if lab:
                rows.append({"source": "acm_ccs", "version": 1998, "code": f"{cur_code}::{lab}", "label": lab,
                             "parent": cur_code, "alt_labels": [],
                             "flags": {"new_in_1998": new, "kind": "subject_descriptor",
                                       "retired_marker": "note2" in m2.group(2)}})
        m3 = re.match(r'\s*<li><a name = "([A-K])">[^<]*</a>\s*(.*)', line)
        if m3:
            pass
    # top-level letters appear as <h2>/<a name="A"> headings; add them from the contents list
    have = {r["code"] for r in rows}
    for m in re.finditer(r'<li><a href = "#([A-K])">[A-K]\. ([^<]+)</a>', s):
        if m.group(1) in have:
            continue
        rows.append({"source": "acm_ccs", "version": 1998, "code": m.group(1), "label": _clean(m.group(2)),
                     "parent": None, "alt_labels": [], "flags": {"kind": "top"}})
    return rows


def msc2020() -> list[dict]:
    df = pd.read_csv(T / "MSC_2020.csv", sep="\t", dtype=str, keep_default_na=False, encoding="cp1252")
    rows = []
    for r in df.itertuples(index=False):
        code = r.code.strip()
        rows.append({"source": "msc", "version": 2020, "code": code, "label": _clean(r.text),
                     "parent": _msc_parent(code), "alt_labels": [], "flags": {}})
    return rows


def _msc_parent(code: str) -> str | None:
    if re.fullmatch(r"\d\d-XX", code):
        return None
    if re.fullmatch(r"\d\d[A-Z]xx", code) or re.fullmatch(r"\d\d-\d\d", code):
        return code[:2] + "-XX"
    if re.fullmatch(r"\d\d[A-Z]\d\d", code):
        return code[:3] + "xx"
    return None


def msc2010() -> list[dict]:
    s = (T / "cran_MSC-2010.html").read_text(encoding="utf-8", errors="replace")
    rows = []
    for m in re.finditer(r'<li id="code:([0-9]{2}[A-Z0-9x\-]{3})">(.*?)(?=<li|</ul>|$)', s, flags=re.S):
        code = m.group(1)
        txt = re.sub(r"<[^>]+>", "", m.group(2))
        txt = txt.replace(code, "", 1)
        lab = _clean(txt)
        if lab:
            rows.append({"source": "msc", "version": 2010, "code": code, "label": lab, "parent": _msc_parent(code),
                         "alt_labels": [], "flags": {}})
    return rows


def msc2000() -> list[dict]:
    import pymupdf
    doc = pymupdf.open(str(T / "msc2000.pdf"))
    lines = []
    for p in doc:
        lines.extend([ln.strip() for ln in p.get_text().splitlines()])
    code_re = re.compile(r"^(\d\d-XX|\d\d[A-Z]xx|\d\d-\d\d|\d\d[A-Z]\d\d)$")
    rows, cur, buf = [], None, []

    def flush():
        if cur and buf:
            lab = _clean(" ".join(buf).replace("- ", "-"))
            lab = re.sub(r"(\w)- (\w)", r"\1\2", lab)
            rows.append({"source": "msc", "version": 2000, "code": cur, "label": lab, "parent": _msc_parent(cur),
                         "alt_labels": [], "flags": {}})
    for ln in lines:
        if not ln or ln.startswith("MATHEMATICS SUBJECT CLASSIFICATION") or re.fullmatch(r"\d+", ln):
            continue
        if code_re.match(ln):
            flush()
            cur, buf = ln, []
        elif cur is not None:
            if len(" ".join(buf)) < 400:
                buf.append(ln)
    flush()
    # page headers repeat codes (e.g. '14Dxx' running heads) -> keep the entry with the longest label per code
    best: dict[str, dict] = {}
    for r in rows:
        if r["code"] not in best or len(r["label"]) > len(best[r["code"]]["label"]):
            best[r["code"]] = r
    return list(best.values())


def pacs2010() -> list[dict]:
    d = yaml.safe_load((T / "pacs.yml").read_text())
    rows = []
    for code, n in d.items():
        rows.append({"source": "pacs_physh", "version": 2010, "code": str(code), "label": _clean(n.get("name") or ""),
                     "parent": n.get("parent"), "alt_labels": [],
                     "flags": {"scheme": "PACS", "level": n.get("level"), "year_s": n.get("year_s")}})
    return rows


def physh() -> list[dict]:
    import rdflib
    from rdflib.namespace import SKOS
    g = rdflib.Graph()
    g.parse(str(T / "physh.ttl"), format="turtle")
    rows = []
    for s in set(g.subjects(rdflib.RDF.type, SKOS.Concept)):
        pl = [str(o) for o in g.objects(s, SKOS.prefLabel) if getattr(o, "language", "en") in (None, "en")]
        if not pl:
            continue
        alts = sorted({str(o) for o in g.objects(s, SKOS.altLabel)})
        br = [str(o) for o in g.objects(s, SKOS.broader)]
        rows.append({"source": "pacs_physh", "version": 2016, "code": str(s).split("/")[-1], "label": pl[0],
                     "parent": br[0].split("/")[-1] if br else None, "alt_labels": alts,
                     "flags": {"scheme": "PhySH", "version_note": "current PhySH release; first public release 2016"}})
    return rows


def jel() -> list[dict]:
    from lxml import etree
    root = etree.parse(str(T / "jel_classificationTree.xml")).getroot()
    rows = []

    def walk(el, parent):
        for c in el.findall("classification"):
            code = c.findtext("code")
            desc = html.unescape(c.findtext("description") or "")
            rows.append({"source": "jel", "version": None, "code": code, "label": desc.replace("•", ";"),
                         "parent": parent, "alt_labels": [p.strip() for p in desc.split("•")][1:] if "•" in desc else [],
                         "flags": {"year_known": False, "level": c.get("level")}})
            walk(c, code)
    walk(root, None)
    return rows


@logger.catch(reraise=True)
def main() -> None:
    setup_logging("s5_taxonomies")
    allrows = []
    for fn in (acm1998, acm2012, msc2000, msc2010, msc2020, pacs2010, physh, jel):
        try:
            r = fn()
            logger.info(f"{fn.__name__}: {len(r)} nodes; e.g. {[x['label'] for x in r[5:8]]}")
            allrows.extend(r)
        except (OSError, ValueError, KeyError) as e:
            logger.error(f"{fn.__name__} failed: {e}")
    df = pd.DataFrame(allrows)
    df["label"] = df["label"].fillna("").astype(str)
    df["label_norm"] = df["label"].map(norm_label)
    df["flags"] = df["flags"].map(json.dumps)
    df["version"] = df["version"].astype("Int64")
    df = df[df.label_norm != ""]
    df.to_parquet(WORK / "tax_entries.parquet", index=False)
    logger.info(f"total {len(df)}\n{df.groupby(['source', 'version'], dropna=False).size()}")


if __name__ == "__main__":
    main()
