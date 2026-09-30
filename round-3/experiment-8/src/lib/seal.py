"""Freeze / unseal gate (EXP5 seal.py pattern).

freeze(spec) writes results/frozen_spec.json and appends its sha256 to logs/seal.log.
load_heldout() returns the sealed held-out/cohort outcome table ONLY IF results/frozen_spec.json exists and its
sha256 equals the one recorded in logs/seal.log, and ONLY ONCE (logs/unsealed.json marks the unseal)."""
from __future__ import annotations

import json
import time

import pandas as pd

from common import DATA, LOGS, RES, jdump, sha256_file

SPEC = RES / "frozen_spec.json"
SEAL = LOGS / "seal.log"
MARK = LOGS / "unsealed.json"


class SealError(RuntimeError):
    pass


def freeze(spec: dict, extra: dict | None = None) -> str:
    jdump(spec, SPEC)
    h = sha256_file(SPEC)
    rec = {"frozen_spec_sha256": h, "time": time.strftime("%Y-%m-%d %H:%M:%S"), **(extra or {})}
    SEAL.write_text(json.dumps(rec, indent=1))
    return h


def load_heldout(spec_path=SPEC, seal_path=SEAL, mark_path=MARK, sealed=DATA / "outcomes_sealed.parquet"):
    if not spec_path.exists():
        raise SealError("frozen_spec.json missing: freeze before unsealing")
    if not seal_path.exists():
        raise SealError("seal.log missing")
    rec = json.loads(seal_path.read_text())
    if sha256_file(spec_path) != rec["frozen_spec_sha256"]:
        raise SealError("frozen_spec.json changed after the seal")
    if mark_path.exists():
        raise SealError(f"held-out outcomes were already unsealed ({mark_path.read_text()[:200]})")
    df = pd.read_parquet(sealed)
    mark_path.write_text(json.dumps({"unsealed_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                                     "frozen_spec_sha256": rec["frozen_spec_sha256"],
                                     "sealed_sha256": sha256_file(sealed)}, indent=1))
    return df
