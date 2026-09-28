#!/usr/bin/env python3
"""WP4 step 1: read art_O7Dq4L02QnDN full_data_out_{1,2,3}.json one part per process and keep only the concept_recognition
examples whose openalex_id is in the Exp5 frame. Writes results/o5_joined.jsonl (one concept per line)."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from loguru import logger

import common as C

KEEP_EV = ("source", "event_type", "year", "date", "date_precision", "year_usable", "match_method",
           "match_confidence", "relation", "entry_id")


def _scan(args) -> tuple[list[dict], dict]:
    path, ids, limit = args
    out, n_seen, n_cr = [], 0, 0
    # the parts contain bare NaN literals (invalid for yajl/ijson), so each part is parsed with the stdlib json
    # module in its own process (one part per worker, ~90 MB each) and freed before returning
    data = json.loads(Path(path).read_text())
    examples = (ex for ds in data["datasets"] if ds.get("dataset") == "concept_recognition" for ex in ds["examples"])
    if True:
        for ex in examples:
            n_seen += 1
            if limit and n_seen > limit:
                break
            oid = ex.get("metadata_openalex_id")
            if not oid or "metadata_frame_role" not in ex:
                continue
            n_cr += 1
            if oid not in ids:
                continue
            inp = json.loads(ex["input"])
            o = json.loads(ex["output"])
            evs = []
            for e in o.get("events", []):
                d = {k: e.get(k) for k in KEEP_EV}
                det = e.get("detail") or {}
                d["detail_title"] = det.get("title") or det.get("name") or det.get("node_label") or det.get("item_text")
                d["mesh_baseline"] = det.get("mesh_baseline")
                d["date_method"] = det.get("date_method")
                d["redirect"] = det.get("title_followed_redirect")
                evs.append(d)
            out.append({"openalex_id": oid, "label": inp.get("label"), "aliases": inp.get("aliases", []),
                        "ancestor_ids": inp.get("ancestor_ids", []), "level": inp.get("level"),
                        "enwiki_title": inp.get("enwiki_title"), "qid": inp.get("qid"),
                        "fold": ex.get("metadata_fold"), "d2_group": ex.get("metadata_group"),
                        "sources_checked": o.get("sources_checked", {}), "events": evs,
                        "n_present_day": len(o.get("present_day", []) or [])})
    del data
    return out, {"file": Path(path).name, "n_examples_seen": n_seen, "n_concept_recognition": n_cr, "n_kept": len(out)}


@logger.catch(reraise=True)
def main(limit: int = 0) -> None:
    C.setup_logging("wp4_extract")
    fc = C.read_csv(C.E5 / "frame_concepts.csv", usecols=["concept_id"])
    ids = {C.norm_id(x) for x in fc.concept_id}
    assert len(ids) == len(fc), "duplicate Exp5 concept ids"
    assert all(C.norm_id(i) == i for i in list(ids)[:500]), "norm_id not idempotent"
    parts = sorted((C.D2 / "full_data_out").glob("full_data_out_*.json"))
    parts = [p for p in parts if p.name.split("_")[-1].split(".")[0].isdigit()]
    for p in parts:
        C.track(p)
    logger.info(f"streaming {len(parts)} parts for {len(ids)} Exp5 concepts")
    rows, stats = [], []
    with ProcessPoolExecutor(len(parts), mp_context=mp.get_context("spawn")) as ex:
        for r, s in ex.map(_scan, [(str(p), ids, limit) for p in parts]):
            rows.extend(r)
            stats.append(s)
            logger.info(s)
    seen = set()
    with open(C.RES / "o5_joined.jsonl", "w") as f:
        for r in rows:
            if r["openalex_id"] in seen:
                continue
            seen.add(r["openalex_id"])
            f.write(json.dumps(r) + "\n")
    C.dump({"parts": stats, "n_frame": len(ids), "n_joined": len(seen)}, C.RES / "o5_extract_stats.json")
    C.save_manifest("wp4_extract")
    logger.info(f"joined {len(seen)} / {len(ids)}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
