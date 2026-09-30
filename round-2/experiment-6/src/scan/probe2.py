import json, sys, time
sys.path.insert(0, "lib")
import pyarrow as pa, pyarrow.compute as pc
from rangefile import read_columns
man = json.load(open("inputs/works_manifest.json"))["files"]
f = sorted(man, key=lambda x: -x["meta"]["content_length"])[5]
key = f["url"].replace("s3://openalex/", ""); size = f["meta"]["content_length"]
sch = json.load(open("results/works_schema.json"))["col_bytes"]
print("id bytes", sch.get("id"), [k for k in sch if k.startswith("concepts") or k.startswith("primary_topic.field") or k=="id"])
for cols in [["title","publication_year","type","is_paratext","is_xpac","primary_location.source.id","primary_topic.field.id"],
             ["concepts.list.element.id","concepts.list.element.score"],
             ["id","referenced_works.list.element","authorships.list.element.author.id"]]:
    t=time.time(); tb=read_columns(key,size,cols,n_threads=12); dt=time.time()-t
    print(cols[:2], tb.num_rows, f"{dt:.1f}s", tb.nbytes/1e6,"MB mem")
    print(tb.schema)
    if "concepts" in tb.column_names:
        c=tb.column("concepts").combine_chunks(); fl=pc.list_flatten(c); print(fl.type, len(fl), fl[:2])
    if "title" in tb.column_names: print(tb.column("title")[:3], tb.column("primary_location")[:2], tb.column("primary_topic")[:2])
