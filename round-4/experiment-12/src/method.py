#!/usr/bin/env python3
"""Driver: runs the RQ2 pipeline stages in the order they were run for this artifact.

  S0 s0_skeleton -> S1/S2 s2_open -> S3 s3_states -> S4/S5/S6 on DEV -> S7 seal + one-time unseal + held-out runs
  -> S8 cases -> S9 atlas -> S10 outputs -> T7 rederive -> T0 unit tests -> headline audit.

Usage: python method.py [--from STAGE] [--workers 24]
The seal is one-shot: once logs/unsealed.json exists, '--from S7' skips the freeze and only reruns the held-out stage."""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable


def steps(workers: int) -> list[tuple[str, list[str]]]:
    return [("S0", ["s0_skeleton.py"]),
            ("S2", ["s2_open.py", "--stage", "all", "--workers", str(workers)]),
            ("S3", ["s3_states.py"]),
            ("S4", ["s4_decomp.py", "--scope", "dev"]),
            ("S5", ["s5_typology.py", "--scope", "dev", "--workers", str(workers)]),
            ("S6", ["s6_sequence.py", "--scope", "dev"]),
            ("S7", ["s7_seal.py", "--freeze"] if not (ROOT / "logs/unsealed.json").exists() else []),
            ("S7run", ["s7_seal.py", "--run"]),
            ("S8", ["s8_cases.py"]),
            ("S9", ["s9_atlas.py"]),
            ("S10", ["s10_outputs.py"]),
            ("T7", ["rederive.py"]),
            ("T0", ["tests/test_units.py"]),
            ("AUDIT", ["audit_headlines.py"])]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="S0")
    ap.add_argument("--workers", type=int, default=24)
    a = ap.parse_args()
    plan = steps(a.workers)
    names = [n for n, _ in plan]
    for name, cmd in plan[names.index(a.start):]:
        if not cmd:
            print(f"[{name}] skipped (already unsealed)")
            continue
        t = time.time()
        r = subprocess.run([PY, str(ROOT / cmd[0])] + cmd[1:], cwd=ROOT)
        print(f"[{name}] exit {r.returncode} in {time.time() - t:.0f}s")
        if r.returncode != 0:
            sys.exit(r.returncode)


if __name__ == "__main__":
    main()
