"""Verify DOIs via Crossref and arXiv IDs via the arXiv API; writes raw/verify.json."""
import json, time, re, sys
from pathlib import Path
import requests
W = Path(__file__).resolve().parent.parent
DOIS = """10.1007/BF02019280
10.1016/j.joi.2010.10.002
10.1002/asi.22688
10.1016/j.joi.2026.101877
10.1371/journal.pone.0054847
10.1038/nature05670
10.1073/pnas.1116502109
10.1086/421787
10.1086/661238
10.1016/j.respol.2017.06.006
10.1126/science.1240474
10.1177/0003122415601618
10.1038/s41467-023-36741-4
10.1038/srep05890
10.1103/PhysRevLett.120.048301
10.1073/pnas.1915378117
10.1002/asi.21694
10.1103/PhysRevX.4.041036
10.1038/srep01069
10.1016/j.joi.2020.101092
10.1016/0304-4076(94)01598-T
10.1080/10438599700000006
10.1016/j.respol.2020.104013
10.1016/j.joi.2018.03.007
10.18653/v1/P16-1111
10.1371/journal.pone.0270131
10.18653/v1/2020.findings-emnlp.158
10.1145/3148011.3148030
10.1287/orsc.2.1.71
10.1177/030631289019003001
10.1073/pnas.1509757112
10.1177/2329496514540131
10.15195/v1.a15
10.1103/PhysRevE.67.026112
10.1046/j.1461-0248.2001.00230.x
10.1016/0197-2456(86)90046-2
10.1002/sim.1186
10.1016/j.jeconom.2020.09.006
10.1016/j.jeconom.2020.12.001
10.1016/j.jeconom.2021.03.014
10.1145/1963405.1963503
10.1007/s11192-025-05356-5
10.1016/j.techfore.2021.120944
10.3386/w10901
10.1038/s41587-021-00907-6
10.1371/journal.pone.0008694
10.1111/j.1472-4642.2009.00594.x
10.1177/00031224231166955
10.1038/srep02522
10.1126/science.1185231
10.7717/peerj-cs.119
10.1145/3197026.3197052
10.1016/j.respol.2014.02.005
10.1016/j.respol.2015.06.006
10.1002/asi.21509
10.1016/j.tree.2005.02.004
10.1002/asi.22662
10.1257/0002828041301418
10.1093/icc/dts012
10.1787/5k4522wkw1r8-en""".split()
ARX = ["2606.03919", "2510.03240", "2606.07994", "1708.03850", "2603.06436", "2501.02429", "2511.18631"]
out = {}
s = requests.Session(); s.headers["User-Agent"] = "aii-research-verify/1.0 (mailto:research-bot@example.org)"
for d in DOIS:
    rec = {"doi": d, "ok": False}
    for attempt in range(4):
        try:
            r = s.get(f"https://api.crossref.org/works/{d}", timeout=30)
            if r.status_code == 429:
                time.sleep(3 * (attempt + 1)); continue
            if r.status_code == 200:
                m = r.json()["message"]
                rec.update(ok=True, title=(m.get("title") or [""])[0], venue=(m.get("container-title") or [""])[:1],
                           year=(m.get("issued", {}).get("date-parts") or [[None]])[0][0],
                           authors=[f"{a.get('given','')} {a.get('family','')}".strip() for a in m.get("author", [])][:8],
                           volume=m.get("volume"), page=m.get("page") or m.get("article-number"))
            else:
                rec["status"] = r.status_code
            break
        except Exception as e:  # network errors are recorded, not fatal
            rec["error"] = str(e); time.sleep(2)
    out[d] = rec; time.sleep(0.4)
for a in ARX:
    try:
        r = s.get(f"http://export.arxiv.org/api/query?id_list={a}", timeout=30)
        t = re.findall(r"<title>(.*?)</title>", r.text, re.S)
        au = re.findall(r"<name>(.*?)</name>", r.text)
        pub = re.findall(r"<published>(\d{4})", r.text)
        out["arXiv:" + a] = {"ok": len(t) > 1, "title": " ".join(t[1].split()) if len(t) > 1 else None, "authors": au[:8], "year": int(pub[0]) if pub else None}
    except Exception as e:
        out["arXiv:" + a] = {"ok": False, "error": str(e)}
    time.sleep(3)
(W / "raw" / "verify.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print(sum(v["ok"] for v in out.values()), "of", len(out), "resolved")
