#!/usr/bin/env python3
"""Item 10 (references): one cumulative reference list.

Inputs: the report's two References sections (list A = iteration-2 list, list B = end-of-report list), Research 2
references_new.json (verified_new; unverified are excluded), Research 3 raw/verify.json (Crossref-verified DOIs) and
DOI-bearing sources of Research 1/3 research_out.json. De-duplication: DOI (lower-cased), then arXiv id, then
first-author surname + year + first 6 title words. Research 3 DOI corrections applied. Numbering: order of first
citation in report_corrected.md, then alphabetical for uncited entries. In-text [n] citations in report_corrected.md are
rewritten region by region (before the first References heading -> list A numbers; after -> list B numbers), list A is
replaced by a pointer and list B by the master list. No network access.
Outputs: references_master.json / .md (with the old->new map), results/refs_summary.json."""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from loguru import logger

from paths import LOGS, R1, R2, R3, RES, WS, jdump

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "refs.log", rotation="30 MB", level="DEBUG")

DOI_FIX = {"chen2012": "10.1002/asi.21694", "moser": "10.1257/0002828041301407", "feldman": "10.1093/icc/dtr040"}
BAD_DOI = {"10.1002/asi.22662": "10.1002/asi.21694"}
EXCLUDE = [("van noorden", "2014"), ("shinn", "2002"), ("fujimura", "1992"), ("arxiv", "2209.03687"),
           ("arxiv", "2408.06839"), ("arxiv", "2606.25320")]
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\)\],;]+", re.I)
AX_RE = re.compile(r"(?:arXiv[:\s]*|arxiv\.org/(?:abs|pdf)/)(\d{4}\.\d{4,5})", re.I)


def norm(s: str) -> str:
    s = re.sub(r"[\u2010-\u2015\u2212]", " ", s or "")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def surname(authors: str) -> str:
    """First author's surname for 'Surname, I., ...' and for 'First M. Last, ...' styles."""
    first = re.split(r",|&| and ", authors or "")[0].strip()
    toks = norm(first).split()
    if not toks:
        return ""
    return toks[0] if len(toks) == 1 else toks[-1]


def key_of(e: dict) -> tuple:
    if e.get("doi"):
        return ("doi", e["doi"].lower().rstrip("."))
    if e.get("arxiv", "").lower().startswith("arxiv"):
        e["arxiv"] = e["arxiv"].split(":")[-1]
    if e.get("arxiv"):
        return ("arxiv", e["arxiv"])
    sur = surname(e.get("authors", ""))
    head = re.split(r"[:?]", e.get("title", "") or "")[0]      # title head (before : or ?), max 5 words
    return ("aty", sur, str(e.get("year")), " ".join(norm(head).split()[:5]))


def parse_report_list(lines: list[str]) -> list[dict]:
    out = []
    for ln in lines:
        m = re.match(r"^\[(\d+)\]\s+(.*)$", ln.strip())
        if not m:
            continue
        n, rest = int(m.group(1)), m.group(2)
        ma = re.match(r"^(.*?)\s*\((\d{4})[a-z]?\)\.?\s*(.*)$", rest)
        authors, year, tail = (ma.group(1), ma.group(2), ma.group(3)) if ma else ("", "", rest)
        title, _, venue = tail.partition(". ")
        doi = DOI_RE.search(rest)
        ax = AX_RE.search(rest)
        out.append({"n": n, "raw": rest, "authors": authors.strip().rstrip(","), "year": year, "title": title.strip(),
                    "venue": venue.strip(), "doi": doi.group(0).rstrip(".") if doi else "",
                    "arxiv": ax.group(1) if ax else ""})
    return out


def excluded(e: dict) -> str:
    a = norm(e.get("authors", "") + " " + e.get("title", ""))
    for who, y in EXCLUDE:
        if who == "arxiv" and (e.get("arxiv") == y or y in e.get("raw", "")):
            return f"arXiv {y}"
        if who != "arxiv" and who in a and str(e.get("year")) == y:
            return f"{who.title()} {y}"
    return ""


def fix_doi(e: dict) -> dict:
    if (e.get("doi") or "").lower().startswith("arxiv"):
        e["arxiv"], e["doi"] = e["doi"].split(":")[-1], ""
    if e.get("doi") in BAD_DOI:
        e["doi_corrected_from"] = e["doi"]
        e["doi"] = BAD_DOI[e["doi"]]
    a, y = norm(e.get("authors", "")), str(e.get("year"))
    if "moser" in a and y == "2004" and e.get("doi") != DOI_FIX["moser"]:
        e["doi_corrected_from"], e["doi"] = e.get("doi", ""), DOI_FIX["moser"]
    if "feldman" in a and y == "2012" and e.get("doi") != DOI_FIX["feldman"]:
        e["doi_corrected_from"], e["doi"] = e.get("doi", ""), DOI_FIX["feldman"]
    if a.startswith("chen") and y == "2012" and "structural variation" in norm(e.get("title", "")):
        if e.get("doi") != DOI_FIX["chen2012"]:
            e["doi_corrected_from"], e["doi"] = e.get("doi", ""), DOI_FIX["chen2012"]
    return e


@logger.catch(reraise=True)
def main() -> None:
    rc = WS / "report_corrected.md"
    lines = rc.read_text().splitlines()
    heads = [i for i, s in enumerate(lines) if s.startswith("## References")]
    assert len(heads) == 2, heads

    def span(i):
        j = i + 1
        while j < len(lines) and not lines[j].startswith("#"):
            j += 1
        return j

    A = parse_report_list(lines[heads[0] + 1:span(heads[0])])
    B = parse_report_list(lines[heads[1] + 1:span(heads[1])])
    ver = json.loads((R3 / "raw/verify.json").read_text())
    r2 = json.loads((R2 / "references_new.json").read_text())
    entries: list[dict] = []
    for lst, tag in ((A, "A"), (B, "B")):
        for e in lst:
            e = fix_doi(dict(e))
            e["verified_by"] = ("Research 3 Crossref verify.json" if e.get("doi") and e["doi"].lower() in
                                {k.lower() for k in ver} else "carried, not re-verified")
            e["source"] = f"report list {tag}"
            e["old_numbers"] = [f"{tag}{e['n']}"]
            entries.append(e)
    for e in r2["verified_new"]:
        d = e.get("doi_or_arxiv", "")
        au = e.get("authors", [])
        entries.append(fix_doi({"authors": ", ".join(au) if isinstance(au, list) else str(au or ""),
                                "year": str(e.get("year")), "title": e.get("title", ""), "venue": e.get("venue", ""),
                                "doi": d if d.startswith("10.") else "", "arxiv": (AX_RE.search("arXiv:" + d) or
                                                                                   [None, ""])[1] if not d.startswith("10.") else "",
                                "verified_by": f"Research 2 ({e.get('verified_via', '')})", "source": "Research 2",
                                "old_numbers": [], "raw": e.get("key", "")}))
    for d, v in ver.items():
        if v.get("ok"):
            au = v.get("authors", [])
            entries.append(fix_doi({"authors": ", ".join(au) if isinstance(au, list) else str(au or ""), "year": str(v.get("year")),
                                    "title": v.get("title", ""), "venue": (v.get("venue") or [""])[0],
                                    "doi": d, "arxiv": "", "verified_by": "Research 3 Crossref verify.json",
                                    "source": "Research 3", "old_numbers": [], "raw": ""}))
    for R, tag in ((R1, "Research 1"), (R3, "Research 3")):
        for s in json.loads((R / "research_out.json").read_text()).get("sources", []):
            u = s.get("url", "")
            dm, am = DOI_RE.search(u), AX_RE.search(u)
            if not (dm or am):
                continue
            entries.append(fix_doi({"authors": "", "year": "", "title": s.get("title", ""), "venue": "",
                                    "doi": dm.group(0).rstrip(".") if dm else "", "arxiv": am.group(1) if am else "",
                                    "verified_by": f"{tag} source URL (not re-verified)", "source": tag,
                                    "old_numbers": [], "raw": u}))
    # exclusions
    excl, kept = [], []
    for e in entries:
        why = excluded(e)
        (excl if why else kept).append((e, why))
    found = {w for _, w in excl}
    r3names = ["Van Noorden 2014", "Shinn 2002", "Fujimura 1992", "arXiv 2209.03687", "arXiv 2408.06839",
               "arXiv 2606.25320"]
    excl_list = ([f"Research 3 unverified: {n} ({'matched and removed' if n in found else 'not present in any input list'})"
                  for n in r3names]
                 + [f"Research 2 unverified: {u.get('key')} (never entered; listed in references_new.json -> unverified)"
                    for u in r2["unverified"]])
    kept = [e for e, _ in kept]
    # de-duplicate (earlier entries win; richer metadata merged)
    master: dict[tuple, dict] = {}
    alias: dict[tuple, tuple] = {}
    for e in kept:
        k = key_of(e)
        k2 = ("aty",) + key_of({**e, "doi": "", "arxiv": ""})[1:] if e.get("authors") else None
        hit = master.get(k) or (master.get(alias.get(k2)) if k2 else None)
        if hit is None:
            master[k] = e
            if k2:
                alias[k2] = k
        else:
            hit["old_numbers"] += e["old_numbers"]
            for f in ("authors", "year", "title", "venue", "doi", "arxiv"):
                if not hit.get(f) and e.get(f):
                    hit[f] = e[f]
            if "Crossref" in e["verified_by"] and "Crossref" not in hit["verified_by"]:
                hit["verified_by"] = e["verified_by"]
    M = list(master.values())
    # second pass: same first-author surname + year and one title a word-prefix (>= 2 words) of the other
    # (the end-of-report list abbreviates titles, e.g. 'The Product Space', 'Co-word analysis')
    merged = []
    for e in M:
        te = norm(re.split(r"[:?]", e.get("title", "") or "")[0]).split()
        hit = None
        for m in merged:
            tm = norm(re.split(r"[:?]", m.get("title", "") or "")[0]).split()
            k = min(len(te), len(tm))
            if (surname(e.get("authors", "")) and surname(e.get("authors", "")) == surname(m.get("authors", ""))
                    and str(e.get("year")) == str(m.get("year")) and k >= 2 and te[:k] == tm[:k]):
                hit = m
                break
        if hit is None:
            merged.append(e)
            continue
        hit["old_numbers"] += e["old_numbers"]
        for f in ("doi", "arxiv", "venue"):
            if not hit.get(f) and e.get(f):
                hit[f] = e[f]
        if len(norm(e.get("title", ""))) > len(norm(hit.get("title", ""))):
            hit["title"] = e["title"]
        if "Crossref" in e["verified_by"] and "Crossref" not in hit["verified_by"]:
            hit["verified_by"] = e["verified_by"]
    M = merged
    # entries with no author and no year (bare URLs) are listed only if they came from a report list
    M = [e for e in M if e.get("authors") or e.get("old_numbers")]
    # required additions
    need = {}
    for who in ("fernandes", "nomaler"):
        hit = next((e for e in M if norm(e.get("authors", "")).startswith(who) or who in norm(e.get("raw", ""))), None)
        need[who] = "present" if hit else "to be verified (absent from Research 2 references_new.json)"
    # numbering by first citation
    old2m = {}
    for i, e in enumerate(M):
        for o in e["old_numbers"]:
            old2m[o] = i
    region_b = heads[0]
    cite_re = re.compile(r"\[(\d{1,2}(?:\s*,\s*\d{1,2})*)\]")
    first_pos = {}
    for li, ln in enumerate(lines):
        if li in (heads[0], heads[1]) or (heads[0] < li < span(heads[0])) or li > heads[1]:
            continue
        tag = "A" if li < region_b else "B"
        for m in cite_re.finditer(ln):
            for x in m.group(1).split(","):
                o = f"{tag}{int(x)}"
                if o in old2m:
                    first_pos.setdefault(old2m[o], (li, m.start()))
    cited = sorted(first_pos, key=lambda i: first_pos[i])
    uncited = sorted([i for i in range(len(M)) if i not in first_pos],
                     key=lambda i: (norm(M[i].get("authors", "")) or "zzz", M[i].get("year", "")))
    order = cited + uncited
    newnum = {i: k + 1 for k, i in enumerate(order)}
    n_rewritten = 0

    def repl(m, tag):
        nonlocal n_rewritten
        xs = [x.strip() for x in m.group(1).split(",")]
        if not all(f"{tag}{int(x)}" in old2m for x in xs):
            return m.group(0)
        n_rewritten += 1
        return "[" + ", ".join(str(newnum[old2m[f"{tag}{int(x)}"]]) for x in xs) + "]"

    out = []
    for li, ln in enumerate(lines):
        if heads[0] < li < span(heads[0]) or li > heads[1]:
            continue
        if li == heads[0]:
            out += ["## References (iteration 2 list)", "",
                    "[Correction, iteration 5, from this evaluation] Merged into the single numbered reference list at "
                    "the end of the report; in-text numbers were renumbered (map in `references_master.md`).", ""]
            continue
        if li == heads[1]:
            continue
        tag = "A" if li < region_b else "B"
        out.append(cite_re.sub(lambda m: repl(m, tag), ln))
    ref_lines = ["## References", "",
                 "[Correction, iteration 5, from this evaluation] One cumulative list: the report's two lists plus "
                 "Research 1-3, de-duplicated (DOI, arXiv id, then author + year + title), Research 3 DOI corrections "
                 "applied, unverified items excluded. Numbered by first citation, then alphabetically.", ""]
    rows = []
    for i in order:
        e = M[i]
        doi = f" https://doi.org/{e['doi']}" if e.get("doi") else (f" arXiv:{e['arxiv']}" if e.get("arxiv") else "")
        txt = f"[{newnum[i]}] {e.get('authors') or 'n.a.'} ({e.get('year') or 'n.d.'}). {e.get('title', '').rstrip('.')}." \
              + (f" {e['venue']}." if e.get("venue") and e.get("source", "").startswith("Research") else
                 (f" {e['venue']}" if e.get("venue") else "")) + doi
        ref_lines += [txt.replace("..", "."), ""]
        rows.append({"id": newnum[i], "authors": e.get("authors", ""), "year": e.get("year", ""),
                     "title": e.get("title", ""), "venue": e.get("venue", ""), "doi": e.get("doi", ""),
                     "arxiv": e.get("arxiv", ""), "verified_by": e.get("verified_by", ""),
                     "doi_corrected_from": e.get("doi_corrected_from", ""), "old_numbers": e["old_numbers"],
                     "cited_in_report": i in first_pos})
    rc.write_text("\n".join(out).rstrip() + "\n\n" + "\n".join(ref_lines).rstrip() + "\n")
    jdump(WS / "references_master.json", {"entries": rows, "excluded_unverified": excl_list,
                                          "required_additions": need, "n_in_text_citations_rewritten": n_rewritten})
    mp = sorted(((o, newnum[old2m[o]]) for o in old2m), key=lambda t: (t[0][0], int(t[0][1:])))
    md = ["# Cumulative reference list (iteration 5)", "",
          f"{len(rows)} entries ({len(cited)} cited in report_corrected.md, {len(uncited)} uncited). "
          f"In-text citation groups rewritten: {n_rewritten}.", "",
          "Excluded as unverified: " + "; ".join(excl_list) + ".", "",
          "Required additions: " + "; ".join(f"{k}: {v}" for k, v in need.items()) + ".", "",
          "## Old -> new number map", "", "| old (list A = iteration-2 list, B = end list) | new |", "|---|---|"]
    md += [f"| {o} | {n} |" for o, n in mp]
    md += ["", "## List", ""] + ref_lines[4:]
    (WS / "references_master.md").write_text("\n".join(md) + "\n")
    summ = {"n_master": len(rows), "n_cited": len(cited), "n_uncited": len(uncited), "n_list_A": len(A),
            "n_list_B": len(B), "n_excluded": len(excl_list), "n_rewritten_citation_groups": n_rewritten,
            "required_additions": need, "n_doi_corrected": sum(bool(r["doi_corrected_from"]) for r in rows)}
    jdump(RES / "refs_summary.json", summ)
    logger.info(f"references: {summ}")


if __name__ == "__main__":
    main()
