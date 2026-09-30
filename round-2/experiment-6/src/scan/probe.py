import json, struct, sys, time
sys.path.insert(0, "lib")
import pyarrow as pa, pyarrow.parquet as pq
from rangefile import _get_range, RangeFile, S3_HTTP
man = json.load(open("inputs/works_manifest.json"))["files"]
f = sorted(man, key=lambda x: -x["meta"]["content_length"])[0]
key = f["url"].replace("s3://openalex/", ""); size = f["meta"]["content_length"]
url = S3_HTTP + key
tail = _get_range(url, size - (2 << 20), size - 1)
flen = struct.unpack("<I", tail[-8:-4])[0]
meta = pq.ParquetFile(pa.PythonFile(RangeFile(size, {size - (2 << 20): tail}), mode="r")).metadata
sz = {}
for rg in range(meta.num_row_groups):
    r = meta.row_group(rg)
    for c in range(r.num_columns):
        col = r.column(c); sz[col.path_in_schema] = sz.get(col.path_in_schema, 0) + col.total_compressed_size
print(key, size/1e6, "MB rows", meta.num_rows, "rgs", meta.num_row_groups)
json.dump({"file": key, "rows": meta.num_rows, "col_bytes": sz}, open("results/works_schema.json", "w"), indent=1)
for k, v in sorted(sz.items(), key=lambda x: -x[1])[:200]:
    if any(s in k for s in ["title","year","type","paratext","xpac","primary_location.source.id","primary_topic","concepts","topics.list.element.id","authorships.list.element.author.id","referenced_works","display_name","abstract"]) or v > 20e6:
        print(f"{v/1e6:9.2f}  {k}")
print("total MB", sum(sz.values())/1e6, "n files", len(man), "total GB", sum(x['meta']['content_length'] for x in man)/1e9)
