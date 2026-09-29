"""Paths and helpers for the iter-5 Part A / Part B code. All upstream artifacts are addressed RELATIVE to the run
root ($AII_RUN_ROOT, default: four levels above this workspace); nothing upstream is written."""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

LIB = Path(__file__).resolve().parent
WS = LIB.parent
RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[3])))
E5 = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_experiment_5"
E8 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_8"
E10 = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_10"
E11 = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_11"
O5DIR = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_dataset_2"
DATA, RES, LOGS, FIGS = WS / "data", WS / "results", WS / "logs", WS / "figures"
for _d in (DATA, RES, LOGS, FIGS):
    _d.mkdir(parents=True, exist_ok=True)
# lib_iter5 first (Exp10 ego.py with compute_btw), then the path-patched Exp11 lib (ego_ctx, rq1stats, fe_stats ...)
for _p in (str(WS / "exp11_code" / "lib"), str(LIB)):
    if _p in sys.path:
        sys.path.remove(_p)
    sys.path.insert(0, _p)
sys.path.remove(str(LIB)); sys.path.insert(0, str(LIB))

SEED = 20260929
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
HELD = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


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
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    return o


def jdump(obj, path: Path) -> None:
    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))


def add_deviation(key: str, text: str) -> None:
    p = RES / "deviations.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = text
    p.write_text(json.dumps(d, indent=1))


def read_parts(d: Path, columns=None):
    import pandas as pd
    parts = sorted(Path(d).glob("*.parquet"))
    if not parts:
        raise FileNotFoundError(f"no parquet parts in {d}")
    return pd.concat([pd.read_parquet(p, columns=columns) for p in parts], ignore_index=True)
