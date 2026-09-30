"""Seal gate for the within-concept mechanism test.

freeze(spec) writes results/frozen_spec.json (with sha256 of every lib/*.py file and of data/yearly_features.parquet)
and records its sha256 in logs/seal.log. attach_outcomes(panel) joins the D3 outcome table ONLY IF the spec exists,
its sha256 equals the sealed one, and the features file is unchanged since the seal; it raises on a second attach
within the same process (a second look at outcomes must be a new, logged run). Each attach is appended to
logs/attach.log."""
from __future__ import annotations

import json
import time
from pathlib import Path

import pandas as pd

from common import DATA_IN, LIB, LOGS, LOGS_IN, RES_IN, jdump, sha256_file

SPEC = RES_IN / "frozen_spec.json"
SEAL = LOGS_IN / "seal.log"
ATTACH_LOG = LOGS / "attach.log"
OUTCOME_FILE = DATA_IN / "d3_concept_year.parquet"
_STATE = {"attached": False}


class SealError(RuntimeError):
    pass


def code_hashes() -> dict[str, str]:
    return {p.name: sha256_file(p) for p in sorted(LIB.glob("*.py"))}


def freeze(spec: dict, extra: dict | None = None, spec_path: Path = SPEC, seal_path: Path = SEAL) -> str:
    jdump(spec, spec_path)
    h = sha256_file(spec_path)
    rec = {"frozen_spec_sha256": h, "time": time.strftime("%Y-%m-%d %H:%M:%S"), **(extra or {})}
    seal_path.write_text(json.dumps(rec, indent=1))
    return h


def check_seal(spec_path: Path = SPEC, seal_path: Path = SEAL) -> dict:
    if not spec_path.exists():
        raise SealError("frozen_spec.json missing: freeze before attaching outcomes")
    if not seal_path.exists():
        raise SealError("seal.log missing")
    rec = json.loads(seal_path.read_text())
    if sha256_file(spec_path) != rec["frozen_spec_sha256"]:
        raise SealError("frozen_spec.json changed after the seal")
    spec = json.loads(spec_path.read_text())
    fh = spec.get("sha256", {}).get("yearly_features.parquet")
    if fh and sha256_file(DATA_IN / "yearly_features.parquet") != fh:
        raise SealError("yearly_features.parquet changed after the seal")
    return rec


def attach_outcomes(panel: pd.DataFrame, spec_path: Path = SPEC, seal_path: Path = SEAL,
                    outcome_file: Path = OUTCOME_FILE, reason: str = "") -> pd.DataFrame:
    if _STATE["attached"]:
        raise SealError("outcomes already attached in this process")
    rec = check_seal(spec_path, seal_path)
    d3 = pd.read_parquet(outcome_file)
    _STATE["attached"] = True
    with ATTACH_LOG.open("a") as f:
        f.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "spec_sha": rec["frozen_spec_sha256"],
                            "reason": reason}) + "\n")
    return panel.merge(d3, on=["ci", "year"], how="left")


def reset_for_tests() -> None:
    _STATE["attached"] = False
