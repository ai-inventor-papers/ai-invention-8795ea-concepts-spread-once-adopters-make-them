"""STEP 0b: time column reads with / without legacy-tag columns on 5 random files; extrapolate scan ETA."""
import json, random, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from rangefile import read_columns
ROOT = Path(__file__).resolve().parent
man = json.loads((ROOT/"snapshot/works_manifest.json").read_text())
files = [(f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"], f["meta"]["record_count"]) for f in man["files"]]
REQ = ["title", "publication_year", "type", "is_paratext", "is_xpac", "primary_location.source.id",
       "topics.list.element.field.id", "primary_topic.field.id"]
TAG = ["concepts.list.element.id", "concepts.list.element.score"]
rnd = random.Random(20260928); pick = rnd.sample(files, 5)
out = {}
for name, cols in (("req", REQ), ("req+tags", REQ + TAG)):
    t = time.time(); rows = 0; byt = 0
    def rd(f):
        tb = read_columns(f[0], f[1], cols, n_threads=8); return tb.num_rows, tb.nbytes
    with ThreadPoolExecutor(4) as ex:
        for n, b in ex.map(rd, pick): rows += n; byt += b
    el = time.time() - t
    tot_rows = sum(f[2] for f in files)
    out[name] = {"sec": el, "rows": rows, "eta_min_4par": el / rows * tot_rows / 60}
    print(name, out[name], flush=True)
(ROOT/"logs/timing_probe.json").write_text(json.dumps(out, indent=1))
