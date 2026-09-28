#!/usr/bin/env python3
"""End-to-end orchestrator: runs every step of the held-out gateway-retention test in order.

  lexicon -> prescreen (sample, names, wikidata aliases, aliases) -> full scan (+ merge) -> onset candidates (match)
  -> backbones -> grounding benchmark -> sense filter -> onset candidates (grounded) -> precision gate -> frame
  -> features -> T0 tests -> T1/T3 checks -> dev analysis + FREEZE -> UNSEAL (once) -> held-out scoring (+ H3)
  -> replication -> figures + method_out.json -> variants -> independent audit

Steps whose main output already exists are skipped (idempotent), so `python method.py` resumes; `--from STEP`
reruns from a step (the seal refuses a second unseal: the held-out steps can be rerun only after unsealing
once, and never re-freeze after an unseal). The step `handcheck` needs the executor's labels in
results/handcheck_labels.csv (kept in the repository).

Usage: python method.py [--from STEP] [--only STEP]"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time

from common import LOGS, RES, ROOT, SCAN, setup_logger

logger = setup_logger("method")
PY = sys.executable
STEPS = [
    ("lexicon", ["lexicon.py"], ROOT / "lexicon_v0.parquet"),
    ("prescreen_sample", ["prescreen.py", "sample"], SCAN / "sample_titles" / "part_001.parquet"),
    ("prescreen_names", ["prescreen.py", "names"], SCAN / "prescreen_survivors.parquet"),
    ("wikidata", ["wikidata_aliases.py"], SCAN / "wikidata_aliases.json"),
    ("prescreen_aliases", ["prescreen.py", "aliases"], ROOT / "lexicon_v1.parquet"),
    ("scan", ["scan_full.py", "--workers", "5"], None),
    ("merge", ["scan_full.py", "--merge"], SCAN / "agg_counts.parquet"),
    ("onset_match", ["frame.py", "match"], RES / "onset_candidates_match.csv"),
    ("backbones", ["backbones.py"], RES / "backbones.json"),
    ("bench", ["grounding.py", "bench"], ROOT / "grounding_benchmark.csv"),
    ("filter", ["grounding.py", "filter"], ROOT / "grounding_report.json"),
    ("onset_grounded", ["frame.py", "grounded"], RES / "onset_candidates_grounded.csv"),
    ("precision", ["grounding.py", "precision"], ROOT / "grounding_precision.csv"),
    ("frame", ["frame.py", "build"], ROOT / "frame_concepts.csv"),
    ("features", ["features.py"], ROOT / "episode_features.csv"),
    ("tests", ["tests/test_units.py"], RES / "unit_tests_T0.json"),
    ("t1", ["checks.py", "t1"], None),
    ("t3", ["checks.py", "t3"], RES / "p78_agreement.csv"),
    ("dev_freeze", ["models.py", "dev"], ROOT / "frozen_spec.json"),
    ("unseal", ["seal.py", "unseal"], ROOT / "sens_episodes_b5_t0p4.csv"),
    ("heldout", ["models.py", "heldout"], RES / "h3_results.json"),
    ("pigeonhole_fix", ["fix_pigeonhole.py"], None),
    ("replicate", ["checks.py", "replicate"], None),
    ("exploratory_domains", ["exploratory_domains.py"], RES / "exploratory_domain_specificity.json"),
    ("report", ["report.py"], ROOT / "method_out.json"),
    ("variants", ["make_variants.py"], ROOT / "preview_method_out.json"),
    ("audit", ["audit.py"], ROOT / "audit.json"),
    ("audit_placebo", ["audit_placebo.py"], RES / "audit_placebo.json"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default=None)
    ap.add_argument("--only", default=None)
    args = ap.parse_args()
    names = [s[0] for s in STEPS]
    i0 = names.index(args.start) if args.start else 0
    for name, cmd, out in STEPS[i0:]:
        if args.only and name != args.only:
            continue
        forced = bool(args.start or args.only)
        if out is not None and out.exists() and not forced:
            logger.info(f"[skip] {name}: {out.relative_to(ROOT)} exists")
            continue
        t = time.time()
        logger.info(f"[run ] {name}: {' '.join(cmd)}")
        r = subprocess.run([PY] + cmd, cwd=ROOT)
        if r.returncode != 0:
            logger.error(f"{name} failed with exit code {r.returncode}")
            raise SystemExit(r.returncode)
        logger.info(f"[done] {name} in {time.time()-t:.0f}s")
    (LOGS / "method_last_run.txt").write_text(time.strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
