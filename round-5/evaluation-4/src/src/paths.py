"""Paths to the run's earlier artifacts (READ-ONLY) and to this workspace, plus small helpers."""
from __future__ import annotations

import hashlib
import json
import math
import os
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
# Run root = the directory that contains 3_invention_loop/ (four levels above this folder in the run tree).
# Override with AII_RUN_ROOT; see reproducibility.md for arranging a cloned repository into this layout.
RUN = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[3])))
assert (RUN / ".").exists(), f"set AII_RUN_ROOT: no 3_invention_loop/ under {RUN}"
L = RUN / "."
EXP5 = L / "round-2/experiment-5/src"
EXP7 = L / "round-3/experiment-7/src"
E8 = L / "round-3/experiment-8/src"
E10 = L / "round-4/experiment-10/src"
E11 = L / "iter_4/gen_art/gen_art_experiment_11"
E12 = L / "round-4/experiment-12/src"
EVAL3 = L / "round-4/evaluation-3/src"
R1 = L / "round-2/research-1/src"
R2 = L / "round-3/research-2/src"
R3 = L / "round-4/research-3/src"
DS2 = L / "round-2/dataset-2/src"
REPORT5 = L / "iter_5/gen_strat/current_report.md"
REPORT4 = L / "iter_4/gen_strat/current_report.md"

RES, FIG, LOGS, COR = WS / "results", WS / "figures", WS / "logs", WS / "corrections_iter5"
for _d in (RES, FIG, LOGS, COR):
    _d.mkdir(parents=True, exist_ok=True)


def rel(p: Path) -> str:
    """RUN-relative path string (the ledger's source_file convention)."""
    p = Path(p).resolve()
    try:
        return str(p.relative_to(RUN))
    except ValueError:
        return str(p.relative_to(WS))


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def jdump(p: Path, obj) -> None:
    Path(p).write_text(json.dumps(_clean(obj), indent=1))


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()
