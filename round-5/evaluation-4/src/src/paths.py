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
EXP5 = L / "iter_2/gen_art/gen_art_experiment_5"
EXP7 = L / "iter_3/gen_art/gen_art_experiment_7"
E8 = L / "iter_3/gen_art/gen_art_experiment_8"
E10 = L / "iter_4/gen_art/gen_art_experiment_10"
E11 = L / "iter_4/gen_art/gen_art_experiment_11"
E12 = L / "iter_4/gen_art/gen_art_experiment_12"
EVAL3 = L / "iter_4/gen_art/gen_art_evaluation_3"
R1 = L / "iter_2/gen_art/gen_art_research_1"
R2 = L / "iter_3/gen_art/gen_art_research_2"
R3 = L / "iter_4/gen_art/gen_art_research_3"
DS2 = L / "iter_2/gen_art/gen_art_dataset_2"
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
