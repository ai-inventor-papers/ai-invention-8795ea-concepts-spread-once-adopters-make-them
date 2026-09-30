#!/usr/bin/env python3
"""Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).

Usage: python method.py [--only STEP] [--from STEP] [--list]
Steps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort
                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate
                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report
Note: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable
STEPS = [
    ("s0", [PY, "s0_prereg.py"]),
    ("s1", [PY, "s1_candidates.py"]),
    ("passC", [PY, "passC.py", "--workers", "9"]),
    ("passC_merge", [PY, "passC.py", "--merge"]),
    ("s3", [PY, "s3_checks.py"]),
    ("s4", [PY, "s4_gate.py", "run"]),
    ("s4_retry", [PY, "s4_gate.py", "retry"]),
    ("s7_exp5", [PY, "s7_ego.py", "--frame", "exp5", "--builds", "all,home,sizematch", "--workers", "3", "--chunk", "200"]),
    ("s7_cohort", [PY, "s7_ego.py", "--frame", "cohort", "--builds", "all,home,sizematch", "--workers", "3", "--chunk", "50"]),
    ("s7_cohort_full", [PY, "s7_ego.py", "--frame", "cohort", "--builds", "full", "--workers", "5", "--chunk", "20",
                        "--tag", "_full"]),
    ("s6", [PY, "s6_covariates.py"]),
    ("s5_exp5", [PY, "s5_typing.py", "exp5"]),
    ("s5_cohort", [PY, "s5_typing.py", "cohort"]),
    ("s5_bench", [PY, "s5_typing.py", "bench"]),
    ("s5_sheet", [PY, "s5_typing.py", "sheet"]),
    ("s5_gate", [PY, "s5_typing.py", "gate"]),
    ("s5_v2", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,'s5_typing.py',c,'--prompt','v2'],check=True) "
                          "for c in ('exp5','cohort','bench','gate')]"]),
    ("s5_m2all", [PY, "s5_typing.py", "m2all", "--prompt", "v2"]),
    ("s8", [PY, "s8_select.py", "--nboot", "500"]),
    ("s9", [PY, "s9_unseal.py"]),
    ("learned", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,'s_learned.py',c],check=True) "
                           "for c in ('validate','features','score')]"]),
    ("audit", [PY, "audit.py"]),
    ("tests", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,t],check=True) for t in "
                         "('tests/test_output.py','tests/t_ego_flags.py','tests/t_outcomes.py','tests/test_units.py')]"]),
    ("outputs", [PY, "make_outputs.py"]),
    ("report", [PY, "make_report.py"]),
    ("rederive", [PY, "rederive.py"]),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    names = [n for n, _ in STEPS]
    if a.list:
        print("\n".join(names))
        return
    todo = STEPS
    if a.only:
        todo = [s for s in STEPS if s[0] == a.only]
    elif a.start:
        todo = STEPS[names.index(a.start):]
    for name, cmd in todo:
        print(f"== {name}: {' '.join(cmd[:4])}", flush=True)
        subprocess.run(cmd, cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
