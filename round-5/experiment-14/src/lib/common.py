"""Shared paths, constants and small helpers for the Cheng reach-vs-depth experiment.

Every upstream input is read BY PATH (read-only) under RUN_ROOT/3_invention_loop; nothing is written outside ROOT.
ego_ctx.py / ego.py (copied verbatim from Exp11) import INPUTS and DATA from here: INPUTS points at Exp11's
read-only inputs/ folder (topic ids, topic metadata, EXP3 backbone slices) so the SELF-topic rule is byte-identical."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np

LIB = Path(__file__).resolve().parent
ROOT = LIB.parent
sys.path.insert(0, str(LIB))

DATA = ROOT / "data"
RES = ROOT / "results"
LOGS = ROOT / "logs"
FIGS = ROOT / "figures"
for _d in (DATA, RES, LOGS, FIGS):
    _d.mkdir(parents=True, exist_ok=True)

RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(ROOT.parents[3])))
LOOP = RUN_ROOT / "."
EXP11 = LOOP / "iter_4/gen_art/gen_art_experiment_11"
EXP10 = LOOP / "round-4/experiment-10/src"
EXP8 = LOOP / "round-3/experiment-8/src"
EXP5 = LOOP / "round-2/experiment-5/src"
EXP3 = LOOP / "round-1/experiment-3/src"
RESEARCH3 = LOOP / "round-4/research-3/src"
INPUTS = EXP11 / "inputs"          # read-only (topic_ids.json, topic_meta.csv, backbone/slice{0,1,2}.npz)

SEED = 20260929
N_BOOT_STATIC = 2000
N_BOOT_PANEL = 500
MIN_PAPERS = 3                      # CONS / EMB defined iff >= 3 papers ...
MIN_TOPICS = 2                      # ... and >= 2 non-self topics in BOTH years (CONS) / in year t (EMB)
EMB_TOPN = 20
SOC_CAP = 200
SOC_MIN_AUTHORS = 3
SOC_MAX_AUTHORS_PER_PAPER = 15      # Cheng et al. 2023 Table 2: "We ignore papers with more than 15 authors"
SOC_LOOKBACK = 10                   # Cheng: ties "in the prior 10 years"

# frame group -> the five pooled groups of EXP10 (MATHDEC reported only)
GROUP5 = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med", "PHYS": "PHYS",
          "LIFEENV": "LIFEENV", "SOC": "SOC", "MATHDEC": "MATHDEC"}
GROUPS5 = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]
BODIES_EXP5 = ["DEV", "OLD_HELDOUT", "COHORT_2010_14"]
BODY_COHORT = "COHORT_2015_17"
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
DEPTH = ["O1c", "O1b", "O3"]
REACH = ["O2r_m50", "O2r_resid"]
SELECTION_LABEL = "selection data, not confirmation"


def body_of_split(split: str) -> str:
    if split == "DEV":
        return "DEV"
    if split == "COHORT":
        return "COHORT_2010_14"
    return "OLD_HELDOUT"


def home_codes(h) -> set[int]:
    """frame home string ('26', '17|22', '17;22') -> vfield codes (OpenAlex field id - 10)."""
    return {int(float(x)) - 10 for x in re.split(r"[|;]", str(h)) if x and x != "nan"}


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with Path(p).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    return o


def jdump(obj, path: Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))


def jload(path: Path):
    return json.loads(Path(path).read_text())


def add_deviation(key: str, text: str) -> None:
    p = RES / "deviations.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = text
    p.write_text(json.dumps(d, indent=1))


def read_parquet_parts(out_dir: Path, columns=None, filters=None):
    import pandas as pd
    parts = sorted(Path(out_dir).glob("part_*.parquet"))
    if not parts:
        raise FileNotFoundError(f"no parquet parts in {out_dir}")
    return pd.concat([pd.read_parquet(p, columns=columns, filters=filters) for p in parts], ignore_index=True)


def set_limits(ram_gb: float = 24.0) -> None:
    """Hard address-space cap so a runaway step raises MemoryError instead of OOM-killing the container (32 GB)."""
    import resource
    b = int(ram_gb * 1024**3)
    try:
        resource.setrlimit(resource.RLIMIT_AS, (b, b))
    except (ValueError, OSError):
        pass


def n_workers() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return max(1, math.ceil(int(parts[0]) / int(parts[1])))
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1
