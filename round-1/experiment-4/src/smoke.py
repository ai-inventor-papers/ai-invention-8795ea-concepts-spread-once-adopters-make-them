"""Stage-1 smoke test (~10 credits): OR syntax, groupability, cited_by OR, sources batch."""
import json, sys
from loguru import logger
import oa_client as oa
from panel import query, BASE_FILTER
logger.remove(); logger.add(sys.stdout, level="INFO")
out = {}
def yearly(filt, tag):
    d = oa.get("/works", {"filter": filt, "group_by": "publication_year"}, tag)
    return {int(g["key"]): g["count"] for g in d["group_by"] if str(g["key"]).isdigit()}
tot = yearly(BASE_FILTER, "ground:global"); out["global_2007"] = tot.get(2007)
a = yearly(f'title_and_abstract.search:"compressed sensing",{BASE_FILTER}', "smoke:cs1")
b = yearly(f'title_and_abstract.search:"compressive sensing",{BASE_FILTER}', "smoke:cs2")
c = yearly(query("compressed sensing/compressive sensing"), "ground:compressed sensing")
ok = all(max(a.get(y,0),b.get(y,0)) <= c.get(y,0) <= a.get(y,0)+b.get(y,0) for y in range(2005,2012))
out["or_check"] = {y:(a.get(y),b.get(y),c.get(y)) for y in range(2005,2012)}; out["or_ok"]=ok
d = oa.get("/works", {"filter": f"topics.field.id:17,publication_year:1998-2002,type:article|review", "group_by": "topics.field.id", "per_page": 200}, "backbone:A:17")
out["topics_field_groupby"] = d["group_by"][:5]
print(json.dumps(out, indent=1)); print(oa.credits_summary())
