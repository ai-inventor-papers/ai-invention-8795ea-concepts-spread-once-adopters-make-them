"""Fetch Europe PMC full-text XML for given PMCIDs; save XML + plain text; print article structure."""
import sys, json, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "raw" / "epmc"
OUT.mkdir(parents=True, exist_ok=True)
def txt(e): return " ".join("".join(e.itertext()).split()) if e is not None else ""
res = {}
for pmcid in sys.argv[1:]:
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
    raw = urllib.request.urlopen(url, timeout=60).read()
    (OUT / f"{pmcid}.xml").write_bytes(raw)
    root = ET.fromstring(raw)
    title = txt(root.find(".//article-title"))
    abst = root.find(".//abstract")
    kw = [txt(k) for k in root.findall(".//kwd")]
    body = root.find(".//body")
    secs = [txt(s.find("title")) for s in body.findall("sec")] if body is not None else []
    back = root.find(".//back")
    backsecs = [txt(s.find("title")) for s in back.iter() if s.tag in ("sec","ack","fn-group","ref-list") and s.find("title") is not None] if back is not None else []
    bodytext = txt(body)
    (OUT / f"{pmcid}.txt").write_text(title + "\n\nABSTRACT: " + txt(abst) + "\n\nBODY: " + bodytext + "\n\nBACK: " + txt(back))
    decl = [txt(s) for s in root.iter() if s.tag == "sec" and re.search(r"(?i)declaration|competing|availab|contribut|funding", txt(s.find("title")))]
    r = dict(pmcid=pmcid, title=title, abstract_words=len(txt(abst).split()), abstract_structured=bool(abst is not None and abst.find("sec") is not None),
             keywords=kw, body_sections=secs, back_sections=backsecs, body_words=len(bodytext.split()),
             figures=len(root.findall(".//fig")), tables=len(root.findall(".//table-wrap")), references=len(root.findall(".//ref")),
             fig_captions=[txt(f.find("caption"))[:600] for f in root.findall(".//fig")][:3], declarations=[d[:400] for d in decl][:8])
    res[pmcid] = r
    print(json.dumps(r, indent=1, ensure_ascii=False)[:4000]); print("=====")
json.dump(res, open(OUT / f"struct_{'_'.join(sys.argv[1:])}.json", "w"), indent=1, ensure_ascii=False)
