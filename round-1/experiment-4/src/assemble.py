"""Assemble per-concept window field counts from the frozen cache (0 credits).

Venue-field labels: API /sources look-ups (S0 rule) where cached; sources never looked up because the shared key
fell below its floor are labelled from the free public OpenAlex S3 sources snapshot (same rule, same topic
profiles; agreement on the overlap is reported).
"""
from __future__ import annotations

import glob
import json
from collections import Counter
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from loguru import logger

import oa_client as oa
from s0_labels import DEV_FIELDS, GROUP_SHORT, pull_window

ROOT = Path(__file__).resolve().parent
SNAP_FILE = ROOT / "cache" / "snapshot_source_labels.json"
YEARS = list(range(1995, 2023))


def cached_window(entry: str, t0: int, w: str) -> dict | None:
    try:
        return pull_window(entry, t0, w, f"offline:{w}")
    except (oa.BudgetStop, RuntimeError) as e:
        logger.debug(f"window {w} not cached for {entry}: {str(e)[:80]}")
        return None


def snapshot_labels(ids: set[str]) -> dict[str, dict]:
    if SNAP_FILE.exists():
        have = json.loads(SNAP_FILE.read_text())
        if ids <= set(have):
            return have
    out = {}
    full = {"https://openalex.org/" + i for i in ids}
    for f in sorted(glob.glob(str(ROOT / "snapshot" / "sources" / "*" / "*.parquet"))):
        t = pq.read_table(f, columns=["id", "type", "display_name", "topics"]).to_pylist()
        for s in t:
            if s["id"] in full:
                out[s["id"].split("/")[-1]] = oa._label(s)
        del t
    SNAP_FILE.write_text(json.dumps(out))
    logger.info(f"snapshot labels: {len(out)}/{len(ids)} sources found")
    return out


def assemble() -> dict:
    g = json.loads((ROOT / "grounding_log.json").read_text())["concepts"]
    homes = json.loads((ROOT / "cache" / "homes.json").read_text())
    yc_df = pd.read_csv(ROOT / "yearly_counts.csv").set_index("concept")
    gt = pd.read_csv(ROOT / "global_totals.csv").set_index("year")["total"].to_dict()
    raw: dict[str, dict] = {}
    for c in g:
        h = homes.get(c["concept"], {})
        if h.get("status") != "dev":
            continue
        t0 = int(c["t0"])
        raw[c["concept"]] = {w: cached_window(c["panel_entry"], t0, w) for w in "ABCD"}
    need = {sid.split("/")[-1] for r in raw.values() for x in r.values() if x for sid in x["groups"]}
    api_known = {k for k in need if k in oa.SRC and oa.SRC[k].get("type") is not None}
    snap = snapshot_labels(need)
    agree = [(oa.SRC[k]["field"], snap[k]["field"]) for k in api_known if k in snap]
    agreement = sum(a == b for a, b in agree) / len(agree) if agree else float("nan")

    def lab(sid: str) -> tuple[str | None, str]:
        k = sid.split("/")[-1]
        if k in api_known:
            return oa.SRC[k]["field"], "api"
        if k in snap:
            return snap[k]["field"], "snapshot"
        return None, "missing"

    concepts = {}
    for c in g:
        nm = c["concept"]
        rec = {"concept": nm, "panel_entry": c["panel_entry"], "t0": c["t0"], "newborn": c["newborn"],
               "status": c["status"], "intended_group": c["intended_group"], "aliases_used": c["aliases_used"],
               "yc": {int(y): int(yc_df.loc[nm, str(y)]) for y in YEARS}}
        h = homes.get(nm, {})
        if c["status"] == "dev_candidate":
            rec["status"] = h.get("status", "not_pulled")
            rec["home"] = h.get("home", [])
            rec["thin_home"] = h.get("thin_home")
        if nm in raw:
            wins = {}
            src_mode = Counter()
            for w, r in raw[nm].items():
                if r is None:
                    wins[w] = None
                    continue
                fc: Counter = Counter()
                for sid, n in r["groups"].items():
                    f, mode = lab(sid)
                    src_mode[mode] += n
                    if f:
                        fc[f] += n
                wins[w] = {"fields": dict(fc), "labelled": sum(fc.values()), "total": r["meta_count"],
                           "top200_covered": sum(r["groups"].values()), "truncated_share": r["truncated_share"],
                           "complete": r["complete"], "n_sources": len(r["groups"])}
            rec["windows"] = wins
            rec["label_source_papers"] = dict(src_mode)
            hA = Counter(wins["A"]["fields"]) if wins.get("A") else Counter()
            homes_dev = [x for x in rec["home"] if x in DEV_FIELDS]
            rec["group"] = GROUP_SHORT[max(homes_dev, key=lambda x: hA.get(x, 0))] if homes_dev else None
        concepts[nm] = rec
    meta = {"api_snapshot_label_agreement": agreement, "n_overlap": len(agree), "n_sources_needed": len(need),
            "n_api_labelled": len(api_known), "global_totals": {int(k): int(v) for k, v in gt.items()}}
    return {"concepts": concepts, "meta": meta}


if __name__ == "__main__":
    import sys
    logger.remove(); logger.add(sys.stdout, level="INFO")
    d = assemble()
    print(d["meta"]["api_snapshot_label_agreement"], d["meta"]["n_overlap"])
    for nm, r in d["concepts"].items():
        if "windows" in r:
            w = r["windows"]
            print(nm[:30], r["group"], {k: (v["labelled"], v["total"], round(v["truncated_share"], 2)) if v else None
                                         for k, v in w.items()})
