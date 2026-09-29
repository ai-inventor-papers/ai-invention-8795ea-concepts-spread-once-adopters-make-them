"""Shared constants, paths and small helpers for the RQ1 held-out pipeline.

The title analyser / surface normaliser / matcher are imported from common5.py (EXP5's common.py, copied verbatim)
so the matching is byte-identical to the EXP5 scan that defined the frame."""
from __future__ import annotations

import hashlib
import json
import math
import os
import sys
from pathlib import Path

import numpy as np

LIB = Path(__file__).resolve().parent
ROOT = LIB.parent
sys.path.insert(0, str(LIB))

INPUTS = ROOT / "inputs"
DATA = ROOT / "data"
RES = ROOT / "results"
LOGS = ROOT / "logs"
FIGS = ROOT / "figures"
MODELS = ROOT / "models"
PASSA = ROOT / "passA" / "parts"
PASSB = ROOT / "passB" / "parts"
for _d in (DATA, RES, LOGS, FIGS, MODELS):
    _d.mkdir(parents=True, exist_ok=True)

RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(ROOT.parents[3])))
EXP5 = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_experiment_5"
EXP3 = RUN_ROOT / "3_invention_loop/iter_1/gen_art/gen_art_experiment_3"
EXP8 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_8"
EXP6 = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_experiment_6"
EVAL1 = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_evaluation_1"
O5DIR = RUN_ROOT / "3_invention_loop/iter_2/gen_art/gen_art_dataset_2"

SEED = 20260928
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
MATCH_Y0, MATCH_Y1 = 2000, 2016      # t0 in 2003..2014 -> feature windows t0-3..t0+2 lie in 2000..2016
TAG_MIN = 0.3
GROUP_OF_FIELD = {17: "CS", 22: "Eng", 13: "BGM", 27: "Med", 29: "Med", 35: "Med", 36: "Med",
                  15: "PHYS", 16: "PHYS", 19: "PHYS", 21: "PHYS", 25: "PHYS", 31: "PHYS",
                  11: "LIFEENV", 23: "LIFEENV", 24: "LIFEENV", 28: "LIFEENV", 30: "LIFEENV", 34: "LIFEENV",
                  12: "SOC", 14: "SOC", 20: "SOC", 32: "SOC", 33: "SOC",
                  26: "MATHDEC", 18: "MATHDEC"}
DEV_GROUPS = ["CS", "Eng", "BGM", "Med"]
HELD_GROUPS = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
UNITS = HELD_GROUPS + ["COH_DEVHOME", "COH_OTHER"]
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger


def mix64(x: np.ndarray) -> np.ndarray:
    """splitmix64 finaliser (identical to EXP5 scan_full.mix64)."""
    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)


def works_files() -> list[tuple[int, str, int, int]]:
    man = json.loads((ROOT / "snapshot/works_manifest.json").read_text())
    return [(i, f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"], f["meta"]["record_count"])
            for i, f in enumerate(man["files"])]


def source_field_lut() -> tuple[np.ndarray, np.ndarray]:
    """(sorted source ids, vfield code 0..26) -- identical to EXP5 common.source_field_lut."""
    import pandas as pd
    sf = pd.read_parquet(INPUTS / "source_field.parquet")
    sid = sf.source.to_numpy(np.int64)
    code = np.where(sf.field.isna(), 0, sf.field.fillna(11).astype(int) - 10).astype(np.int8)
    o = np.argsort(sid)
    return sid[o], code[o]


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
    if isinstance(o, (np.bool_,)):
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


def load_frame():
    import pandas as pd
    fr = pd.read_csv(EXP5 / "frame_concepts.csv")
    fr["split_raw"] = fr["split"]
    fr["split"] = np.where(fr.split_raw.str.startswith("HELDOUT"), "HELDOUT", fr.split_raw)
    dev_home = set(DEV_GROUPS)
    fr["cohort_part"] = np.where(fr.split == "COHORT",
                                 np.where(fr.group.isin(dev_home), "COH_DEVHOME", "COH_OTHER"), None)
    fr["unit"] = np.where(fr.split == "COHORT", fr.cohort_part, fr.group)
    return fr


def write_parquet_parts(df, out_dir: Path, rows_per_part: int = 1_500_000) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("part_*.parquet"):
        old.unlink()
    paths = []
    for k, i in enumerate(range(0, max(len(df), 1), rows_per_part), start=1):
        p = out_dir / f"part_{k:03d}.parquet"
        df.iloc[i:i + rows_per_part].to_parquet(p, index=False, compression="zstd")
        paths.append(p)
    return paths


def read_parquet_parts(out_dir: Path, columns=None):
    import pandas as pd
    parts = sorted(Path(out_dir).glob("part_*.parquet"))
    if not parts:
        raise FileNotFoundError(f"no parquet parts in {out_dir}")
    return pd.concat([pd.read_parquet(p, columns=columns) for p in parts], ignore_index=True)
