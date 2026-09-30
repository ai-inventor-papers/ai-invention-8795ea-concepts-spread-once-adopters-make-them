#!/usr/bin/env python3
"""Frame-N confirmation pipeline driver: does the home-neighbourhood churn / novelty signal (OPEN_home, NOVCHURN_home)
anticipate later disciplinary breadth for vocabulary-free NEWBORN title phrases that are NOT in the legacy
OpenAlex/MAG vocabulary? Method (OPEN_home / NOVCHURN_home) and baselines (B5 volume/growth/reach/entropy/off-home
share rung ladder, the ALL and SIZEMATCH builds, and Cheng et al. 2023 ideational consistency) are scored side by side
in one pipeline, from a hash-sealed pre-registration, with a single unseal of the outcome counts.

Stages (each is its own resumable script; this driver runs them in order and stops at the first failure):
  S0  s0_prereg.py                      pre-registration + frozen_spec_v0 hashed into logs/seal.log
  S1  tests/unit_tests_port.py, tests/unit_tests_new.py   ported-code equivalence (T1/T4/T8) + T3/T5/T6
  S2  passM.py ; passM.py --merge       mining sample (every 5th snapshot file, titles 2000-2017)
  S3  s3_candidates.py                  candidate phrases (k_t = 4, exclusions, POS), recall benchmark
  S4  passN.py ; passN.py --merge       full-corpus counts 1995-2022, outcome rows sealed at write time
  S5  s5_onset.py ; s5_gate.py estimate|run|m2 --m2all|sheet ; s5_gate2.py eval|run|frame
                                        onset (masked), SEAL-B, dedup, home; LLM precision gate + categorical gate
  S6  s6_features.py                    B5, reach, footprint, ego builds, Cheng measures, clean variants
  S7  s7_freeze.py prepare|power|freeze indices, pre-seal diagnostics, fallback E, power, FREEZE
  S8  s8_unseal.py                      the single unseal + frozen scoring (refuses a second unseal)
  S9  audit_frame_n.py ; make_outputs_n.py   independent re-derivation, figures, method_out.json
The blind-check labels (results/blind_check_labels*.json) are written by the executor agent between the gate
sub-steps, so a fresh re-run of S5 needs those files (they are kept in results/).

Usage: python method.py --from S2 --to S9     (default: print the plan only; --run executes)"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent
PY = str(ROOT / ".venv" / "bin" / "python")
STAGES = [
    ("S0", [["s0_prereg.py"]]),
    ("S1", [["tests/unit_tests_port.py"], ["tests/unit_tests_new.py"]]),
    ("S2", [["passM.py", "--workers", "9"], ["passM.py", "--merge", "--workers", "6"]]),
    ("S3", [["s3_candidates.py", "--stage", "all"]]),
    ("S4", [["passN.py", "--workers", "9"], ["passN.py", "--merge"]]),
    ("S5", [["s5_onset.py"], ["s5_gate.py", "estimate"], ["s5_gate.py", "run"], ["s5_gate.py", "m2", "--m2all"],
            ["s5_gate.py", "sheet"], ["s5_gate.py", "score"], ["s5_gate.py", "m2rest"], ["s5_gate.py", "sheet2"],
            ["s5_gate2.py", "eval"], ["s5_gate2.py", "run"], ["s5_gate2.py", "frame"]]),
    ("S6", [["s6_features.py", "--workers", "9"]]),
    ("S7", [["s7_freeze.py", "prepare"], ["s7_freeze.py", "power"], ["s8_unseal.py", "--dryrun"],
            ["s7_freeze.py", "freeze"]]),
    ("S8", [["s8_unseal.py"]]),
    ("S9", [["audit_frame_n.py"], ["make_outputs_n.py"]]),
]


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="S0")
    ap.add_argument("--to", dest="end", default="S9")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    (ROOT / "logs").mkdir(exist_ok=True)
    logger.add(ROOT / "logs" / "method.log", rotation="30 MB", level="DEBUG")
    names = [s for s, _ in STAGES]
    todo = STAGES[names.index(a.start):names.index(a.end) + 1]
    env = dict(os.environ, PYTHONPATH=str(ROOT / "lib"), OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1",
               MKL_NUM_THREADS="1")
    for stage, cmds in todo:
        for c in cmds:
            logger.info(f"{stage}: {' '.join(c)}")
            if not a.run:
                continue
            t = time.time()
            r = subprocess.run([PY, *c], cwd=ROOT, env=env)
            if r.returncode != 0:
                logger.error(f"{stage} failed ({' '.join(c)}), exit {r.returncode}")
                raise SystemExit(r.returncode)
            logger.info(f"{stage} ok in {(time.time() - t) / 60:.1f} min")


if __name__ == "__main__":
    main()
