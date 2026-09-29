"""Fetch abstracts/TLDRs for a DOI list via the Semantic Scholar batch endpoint and fix bad DOIs via Crossref query."""
import json, time
from pathlib import Path
import requests
W = Path(__file__).resolve().parent.parent
ids = ["DOI:10.1038/srep05890", "DOI:10.1103/PhysRevLett.120.048301", "DOI:10.1038/srep01069", "DOI:10.1103/PhysRevX.4.041036",
       "DOI:10.1016/j.joi.2020.101092", "DOI:10.1016/j.respol.2020.104013", "DOI:10.1016/j.joi.2018.03.007", "DOI:10.1145/3148011.3148030",
       "DOI:10.15195/v1.a15", "DOI:10.1177/2329496514540131", "DOI:10.1126/science.1185231", "DOI:10.1126/science.1240474",
       "DOI:10.1145/3197026.3197052", "DOI:10.1016/j.techfore.2021.120944", "DOI:10.1371/journal.pone.0008694", "DOI:10.1016/j.joi.2026.101877",
       "DOI:10.1073/pnas.1509757112", "DOI:10.1016/j.respol.2014.02.005", "ARXIV:2510.03240", "ARXIV:2511.18631"]
out = {}
for attempt in range(5):
    r = requests.post("https://api.semanticscholar.org/graph/v1/paper/batch", params={"fields": "title,year,venue,abstract,tldr,externalIds"}, json={"ids": ids}, timeout=60)
    if r.status_code == 200:
        for i, p in zip(ids, r.json()):
            out[i] = p
        break
    time.sleep(5 * (attempt + 1))
else:
    out["error"] = r.status_code
q = {"Moser Nicholas 2004 Was electricity a general purpose technology? Evidence from historical patent citations": None,
     "Feldman Yoon 2012 An empirical test for general purpose technology: an examination of the Cohen-Boyer rDNA technology": None,
     "Coulter Monarch Konda 1998 Software engineering as seen through its research literature: a study in co-word analysis": None,
     "Chen 2009 Towards an explanatory and computational theory of scientific discovery structural variation Journal of Informetrics": None}
for k in q:
    r = requests.get("https://api.crossref.org/works", params={"query.bibliographic": k, "rows": 2, "select": "DOI,title,author,container-title,issued,volume,page"}, timeout=30)
    q[k] = r.json()["message"]["items"] if r.status_code == 200 else r.status_code
    time.sleep(1)
out["crossref_queries"] = q
(W / "raw" / "s2_batch.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("done", len(out))
