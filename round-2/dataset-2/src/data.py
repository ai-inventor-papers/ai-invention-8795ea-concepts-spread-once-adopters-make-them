# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas", "pyarrow", "loguru", "lemminflect"]
# ///
"""Standardise the collected recognition sources into the exp_sel_data_out schema -> full_data_out.json.

Inputs: the source files indexed in temp/datasets/INDEX.md (downloads live under cache/), as processed by the pipeline
scripts into work/ (concept_rows.pkl, entries.parquet, links.parquet, verifications.parquet, list_entries.parquet,
concept_keys.parquet, mesh_desc.parquet) and out/ (crosswalk_level1_to_field.csv, spotcheck_p78.csv).
Run ./run_all.sh first on a fresh clone.

One example per data row (a concept, a taxonomy node / MeSH descriptor / list item, one LLM verification, one crosswalk
row, one P78 concept), grouped into 10 datasets:
  concept_recognition, external_entries_{mesh,acm_ccs,msc,pacs_physh,jel,curated_lists}, match_verifications,
  crosswalk_level1_to_field, spotcheck_p78
Size rule (aii-file-size-limit): full_data_out.json above 95 MB is split into full_data_out/full_data_out_<n>.json
(each part a valid exp_sel_data_out document, <= 90 MB) and the single file is removed.
Also writes mini_data_out.json (<= 200 examples per dataset, concept rows stratified by provisional group) and
preview_data_out.json (10 per dataset, strings truncated).
"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "scripts"))

import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

from s9_outputs import build_datasets, trunc, write_parts  # noqa: E402

LIMIT_BYTES = 95_000_000
REQUIRED = ("input", "output")


def check(ds: list[dict]) -> None:
    """Schema-level checks the validator does not do: one example per row, string input/output, flat metadata."""
    names = [d["dataset"] for d in ds]
    assert len(names) == len(set(names)) == 10, names
    for d in ds:
        assert d["examples"], d["dataset"]
        for x in d["examples"]:
            assert all(isinstance(x[k], str) for k in REQUIRED)
            bad = [k for k in x if k not in REQUIRED and not k.startswith("metadata_")]
            assert not bad, (d["dataset"], bad)
            assert not any(isinstance(v, dict) for k, v in x.items() if k.startswith("metadata_")), d["dataset"]


def mini_preview(ds: list[dict]) -> None:
    rnd = random.Random(0)
    mini, prev = [], []
    for d in ds:
        exs = d["examples"]
        if d["dataset"] == "concept_recognition":
            by = defaultdict(list)
            for x in exs:
                if x["metadata_level"] >= 2:
                    by[x["metadata_group"]].append(x)
            per = max(1, 200 // len(by))
            m = []
            for g in sorted(by):   # half the richest rows, half random, per provisional group
                m += sorted(by[g], key=lambda x: -x["metadata_n_events"])[:per // 2]
                m += rnd.sample(by[g], min(len(by[g]), per - per // 2))
            m = m[:200]
        else:
            m = exs if len(exs) <= 200 else rnd.sample(exs, 200)
        mini.append({"dataset": d["dataset"], "examples": m})
        prev.append({"dataset": d["dataset"], "examples": trunc(m[:10])})
    (ROOT / "mini_data_out.json").write_text(json.dumps({"datasets": mini}, ensure_ascii=False, indent=1))
    (ROOT / "preview_data_out.json").write_text(json.dumps({"datasets": prev}, ensure_ascii=False, indent=1))


@logger.catch(reraise=True)
def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")
    R = pd.read_pickle(ROOT / "work" / "concept_rows.pkl")
    logger.info(f"concept rows {len(R)}")
    ds = build_datasets(R)
    check(ds)
    counts = {d["dataset"]: len(d["examples"]) for d in ds}
    logger.info(f"datasets: {counts}")
    fold = Counter(x["metadata_fold"] for x in ds[0]["examples"])
    logger.info(f"concept_recognition folds: {dict(fold)}")
    out = ROOT / "full_data_out.json"
    body = json.dumps({"metadata": {"description": "External, dated recognition events for OpenAlex legacy concepts",
                                    "n_examples": counts}, "datasets": ds}, ensure_ascii=False)
    out.write_text(body)
    size = out.stat().st_size
    logger.info(f"full_data_out.json {size / 1e6:.1f} MB")
    if size > LIMIT_BYTES:
        parts = write_parts(ds)
        out.unlink()
        logger.info(f"above {LIMIT_BYTES / 1e6:.0f} MB -> split into {parts}; single file removed")
    mini_preview(ds)
    logger.info("mini_data_out.json and preview_data_out.json written")


if __name__ == "__main__":
    main()
