"""Verify DOIs via api.crossref.org (anonymous). Usage: xref.py doi1 doi2 ... ; writes raw/crossref/verified.jsonl"""
import sys, json, time, urllib.request, urllib.parse, concurrent.futures as cf
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent / "raw" / "crossref"; OUT.mkdir(parents=True, exist_ok=True)
def get(doi):
  for k in range(6):
    time.sleep(1.5 + 3*k)
    try:
        u = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
        m = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "aii-research (mailto:none)"}), timeout=40))["message"]
        a = m.get("author", [])
        return dict(doi=doi, ok=True, title=(m.get("title") or [""])[0], first_author=(a[0].get("family","") if a else ""), authors=[f"{x.get('given','')} {x.get('family','')}".strip() for x in a],
                    year=(m.get("issued",{}).get("date-parts",[[None]])[0][0]), venue=(m.get("container-title") or [""])[0], volume=m.get("volume"), page=m.get("page") or m.get("article-number"))
    except Exception as e:
        err = str(e)[:100]
        if '429' not in err and '5' != err[11:12]: return dict(doi=doi, ok=False, err=err)
  return dict(doi=doi, ok=False, err=err)
with cf.ThreadPoolExecutor(2) as ex:
    rs = list(ex.map(get, sys.argv[1:]))
with open(OUT / "verified.jsonl", "a") as f:
    for r in rs:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(("OK " if r["ok"] else "FAIL ") + r["doi"], "|", r.get("first_author"), r.get("year"), "|", (r.get("title") or r.get("err",""))[:90], "|", r.get("venue"), r.get("volume"), r.get("page"))
