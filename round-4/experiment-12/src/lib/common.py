"""Shared constants, input paths, seal-aware loaders and small helpers for the RQ2 trajectories re-run.

Every input is a cached artifact of this run (EXP5/EXP6/EXP7/EXP8); all input paths are READ-ONLY.
No network access is allowed in this artifact: `network_guard()` makes importing requests/boto/urllib3 fail."""
from __future__ import annotations

import builtins
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

LIB = Path(__file__).resolve().parent
ROOT = LIB.parent
sys.path.insert(0, str(LIB))

DATA = ROOT / "data"
RES = ROOT / "results"
LOGS = ROOT / "logs"
FIGS = ROOT / "figures"
CASES = ROOT / "case_studies"
ATLAS = ROOT / "ai_atlas"
for _d in (DATA, RES, LOGS, FIGS, CASES, ATLAS):
    _d.mkdir(parents=True, exist_ok=True)

RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(ROOT.parents[3])))
# input artifacts (read-only); each can be pointed elsewhere with its own environment variable
E5 = Path(os.environ.get("AII_EXP5_DIR", RUN_ROOT / "round-2/experiment-5/src"))  # art_wxWssKSUR45f
E6 = Path(os.environ.get("AII_EXP6_DIR", RUN_ROOT / "round-2/experiment-6/src"))  # art_N-mpomDZZ1ln
E7 = Path(os.environ.get("AII_EXP7_DIR", RUN_ROOT / "round-3/experiment-7/src"))  # art_22ppE1snfHKj
E8 = Path(os.environ.get("AII_EXP8_DIR", RUN_ROOT / "round-3/experiment-8/src"))  # art_dFQ6jbgNsR6Q
DS2 = Path(os.environ.get("AII_DS2_DIR", RUN_ROOT / "round-2/dataset-2/src"))  # art_O7Dq4L02QnDN
E8_DATA = E8 / "data"
E8_INPUTS = E8 / "inputs"

SEED = 20260929
N_BOOT = 2000
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
NF = 26
AGES = list(range(0, 11))          # state sequences t0..t0+10 (ages 9-10 'extended')
AN_AGES = list(range(0, 9))        # analysis ages 0..8 (every concept has them: t0 <= 2014)
H = 8                              # decomposition horizon (age)
MED_FIELD = 27

GROUP8_TO_RG = {"CS": "CS+Eng", "Eng": "CS+Eng", "BGM": "BGM+Med", "Med": "BGM+Med", "PHYS": "PHYS",
                "LIFEENV": "LIFEENV", "SOC": "SOC", "MATHDEC": "MATHDEC"}
DEV_GROUPS = ["CS", "Eng", "BGM", "Med"]
HELD_GROUPS = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
UNITS = HELD_GROUPS + ["COH_DEVHOME", "COH_OTHER"]
REPORT_GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"]

DISCLOSURE = ("held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's "
              "analysis choices (fixed on DEV before held-out states/outcomes were read by this artifact)")

OPEN_COMPONENTS = [("new_edge_rate", +1), ("n_comm_W3", +1), ("participation", +1), ("NOV_res", +1),
                   ("ego_density_W3", -1), ("edge_persistence", -1)]
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
OUTCOMES = ["O1c", "O1b", "O2r_m50", "O2r_m30", "O2r_resid", "O2r_resid_N", "O3", "O4", "O5", "O5_WW"]


# ----------------------------------------------------------------------------- logging / io
def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger


def network_guard() -> None:
    """Cache-only artifact: any attempt to import an HTTP / S3 client raises."""
    banned = {"requests", "boto3", "botocore", "aiohttp", "httpx", "urllib3", "s3fs"}
    real = builtins.__import__

    def guarded(name, *a, **k):
        if name.split(".")[0] in banned:
            raise ImportError(f"network guard: importing '{name}' is forbidden in this cache-only artifact")
        return real(name, *a, **k)
    builtins.__import__ = guarded


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
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))


def jload(path: Path):
    return json.loads(Path(path).read_text())


def add_deviation(key: str, reason: str, effect: str) -> None:
    p = RES / "deviations.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = {"reason": reason, "effect_on_claims": effect, "time": time.strftime("%Y-%m-%d %H:%M:%S")}
    p.write_text(json.dumps(d, indent=1))


# ----------------------------------------------------------------------------- frame
def home_list(h) -> list[int]:
    return [int(float(x)) for x in re.split(r"[;|]", str(h)) if x and x != "nan"]


def load_frame():
    """EXP5 frame (12,499 concepts) with reporting groups, units and flags. Outcome-free."""
    import pandas as pd
    fr = pd.read_csv(E5 / "frame_concepts.csv")
    fr["split_raw"] = fr["split"]
    fr["split"] = np.where(fr.split_raw.str.startswith("HELDOUT"), "HELDOUT", fr.split_raw)
    fr["cohort_part"] = np.where(fr.split == "COHORT",
                                 np.where(fr.group.isin(DEV_GROUPS), "COH_DEVHOME", "COH_OTHER"), None)
    fr["unit"] = np.where(fr.split == "COHORT", fr.cohort_part, fr.group)
    fr["home_list"] = [home_list(h) for h in fr.home]
    fr["rgroup"] = fr.group.map(GROUP8_TO_RG)
    fr["med_home"] = [int(MED_FIELD in h) for h in fr.home_list]
    fr["intersection_born"] = (fr.intersect40 == 1).astype(int)
    # EXP6 overlap = the 658 concepts EXP7 dropped (id OR qid OR label match; results/overlap_report.json)
    ov = json.loads((E7 / "results/overlap_report.json").read_text())
    fr["in_exp6"] = fr.concept_id.isin(set(ov["dropped_concept_ids"])).astype(int)
    return fr


def home_mask(fr) -> np.ndarray:
    m = np.zeros((len(fr), NF), bool)
    for i, hl in enumerate(fr.home_list):
        for h in hl:
            m[i, h - 11] = True
    return m


# ----------------------------------------------------------------------------- seal-aware outcomes
MARK = LOGS / "unsealed.json"
SEAL = LOGS / "seal.log"
SPEC = RES / "frozen_spec.json"


class SealError(RuntimeError):
    pass


def is_unsealed() -> bool:
    if not MARK.exists():
        return False
    rec = json.loads(SEAL.read_text())
    if sha256_file(SPEC) != rec["frozen_spec_sha256"]:
        raise SealError("frozen_spec.json changed after the seal")
    return True


class SealedFrame:
    """Outcome table wrapper: DEV rows are readable; non-DEV outcome columns raise until the one-time unseal."""

    def __init__(self, df):
        self._df = df

    def dev(self):
        return self._df[self._df.split == "DEV"].copy()

    def all(self):
        if not is_unsealed():
            raise SealError("held-out/cohort outcomes are sealed: run s7_seal.py first")
        return self._df.copy()


def load_outcomes() -> SealedFrame:
    import pandas as pd
    cols = ["ci", "split", "O1c", "O1b", "O2r_m50", "O2r_m30", "O2r_resid", "O2r_resid_N", "O3", "O4", "O5",
            "O5_WW", "N_outcome"]
    df = pd.read_parquet(E8_DATA / "outcomes.parquet", columns=cols)
    df["split"] = np.where(df.split.str.startswith("HELDOUT"), "HELDOUT", df.split)
    return SealedFrame(df)


# ----------------------------------------------------------------------------- output validation
AII_JSON = Path(os.environ.get("AII_JSON_SKILL", str(ROOT.parents[6] / ".claude/skills/aii-json")))  # schema validator


def validate_out(stage: str, path: Path | None = None, logger=None) -> bool:
    path = path or (ROOT / "method_out.json")
    py = AII_JSON.parent / ".ability_client_venv/bin/python"
    r = subprocess.run([str(py), str(AII_JSON / "scripts/aii_json_validate_schema.py"), "--format", "exp_gen_sol_out",
                        "--file", str(path)], capture_output=True, text=True, timeout=600)
    ok = "PASSED" in r.stdout
    msg = f"[{stage}] validate {'OK' if ok else 'FAILED'} {path.name}"
    with (LOGS / "validate.log").open("a") as f:
        f.write(time.strftime("%H:%M:%S ") + msg + ("" if ok else "\n" + r.stdout[-2000:] + r.stderr[-2000:]) + "\n")
    if logger:
        (logger.info if ok else logger.error)(msg)
    if not ok:
        raise RuntimeError(msg + "\n" + r.stdout[-3000:])
    return ok


def update_status(stage: str, extra_meta: dict | None = None) -> None:
    """Record a finished stage in method_out.json metadata and re-validate (method_out must never be invalid)."""
    p = ROOT / "method_out.json"
    d = json.loads(p.read_text())
    md = d.setdefault("metadata", {})
    if stage not in md.setdefault("stages_done", []):
        md["stages_done"].append(stage)
    if extra_meta:
        md.update(_clean(extra_meta))
    tmp = ROOT / "method_out.tmp.json"
    tmp.write_text(json.dumps(d, indent=1))
    validate_out(stage, tmp)
    tmp.replace(p)


# ----------------------------------------------------------------------------- small stats helpers
def spearman(x, y) -> tuple[float, int]:
    from scipy.stats import spearmanr
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 5:
        return float("nan"), int(ok.sum())
    return float(spearmanr(x[ok], y[ok]).statistic), int(ok.sum())


def boot_ci(v: np.ndarray) -> list[float]:
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if len(v) < 10:
        return [float("nan"), float("nan")]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
