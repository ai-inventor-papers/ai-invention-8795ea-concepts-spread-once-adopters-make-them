#!/usr/bin/env python3
"""RQ1 held-out deliverable -- end-to-end orchestrator (idempotent; each step skips if its output exists).

  0  tests/test_units.py            T0 unit tests (+ tests/t0_8_ego_port.py: the ego port reproduces EXP3 exactly)
  1  passA.py                       zero-credit snapshot pass: grounded frame matches + work/topic/author ids, background
  2  passB.py                       citations received by early works (O4) and by the reference sample
  3  build_features.py              ~53 indicators in 7 families over t0..t0+2 (+ B5)
  4  outcomes.py                    one outcome table; DEV rows / sealed HELDOUT+COHORT rows
  5  dev_select.py                  DEV-only ranking (psp | B5, dAUC), top 10s, learned models, power, FREEZE + seal
  6  heldout.py                     unseal ONCE; frozen scoring, DL pooling, Holm, portability, P1-P5, sensitivities
  7  audit.py                       T7 independent re-derivation
  8  make_outputs.py                rq1_heldout.json, figures, case exemplars, method_out.json

Usage: python method.py [--from STEP] [--only STEP] [--workers 5]"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))

from common import DATA, LOGS, RES, setup_logger  # noqa: E402

PY = sys.executable
STEPS = [
    ("tests", [["tests/test_units.py"], ["tests/t0_8_ego_port.py"]], RES / "t0_8_ego_port.json"),
    ("passA", [["passA.py", "--workers", "{w}"], ["passA.py", "--merge"]], DATA / "passA_info.json"),
    ("passB", [["passB.py", "--workers", "{w}"], ["passB.py", "--merge"]], DATA / "passB_info.json"),
    ("features", [["build_features.py", "--stage", "all", "--workers", "{w}"]], RES / "indicator_matrix.parquet"),
    ("outcomes", [["outcomes.py"]], DATA / "outcomes_sealed.parquet"),
    ("dev_select", [["dev_select.py", "--stage", "all", "--workers", "{w}"]], LOGS / "seal.log"),
    ("heldout", [["heldout.py", "--stage", "all", "--workers", "{w}"]], RES / "sensitivities_pooled.json"),
    ("audit", [["audit.py"]], RES / "audit.json"),
    ("outputs", [["make_outputs.py"]], RES / "rq1_heldout.json"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default=None)
    ap.add_argument("--only", default=None)
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    logger = setup_logger("method")
    names = [s[0] for s in STEPS]
    i0 = names.index(a.start) if a.start else 0
    for name, cmds, marker in STEPS[i0:]:
        if a.only and name != a.only:
            continue
        if marker.exists() and not (a.only or a.start == name):
            logger.info(f"skip {name}: {marker.relative_to(ROOT)} exists")
            continue
        for c in cmds:
            cmd = [PY] + [x.format(w=a.workers) for x in c]
            t = time.time()
            logger.info(f"run {' '.join(c)}")
            r = subprocess.run(cmd, cwd=ROOT)
            if r.returncode != 0:
                raise SystemExit(f"step {name} failed ({' '.join(c)}), exit {r.returncode}")
            logger.info(f"done {' '.join(c)} in {(time.time()-t)/60:.1f} min")


if __name__ == "__main__":
    main()
