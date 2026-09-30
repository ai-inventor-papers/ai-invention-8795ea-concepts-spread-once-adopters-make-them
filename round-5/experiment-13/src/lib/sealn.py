"""Hash-chained seal for Frame N (EXP10 lib/seal2.py pattern, paths adapted).

logs/seal.log is JSON lines; every record carries prev = sha256 of the previous line (a hash chain).
  record(stage, **payload)   append a record
  freeze(spec)               write results/frozen_spec.json and append its sha256 as stage 'S7_freeze'
  check_sealed_untouched()   every sealed/parts file still has the sha256 logged at write time
  unseal()                   returns the sealed agg rows (A + B) ONLY IF the spec hash matches the S7 record, the chain
                             is intact, the sealed parts are untouched and no earlier unseal happened
                             (logs/unsealed.json); then marks the unseal. A second call raises SealError."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import pandas as pd

from common import LOGS, RES, ROOT, jdump, sha256_file

SPEC = RES / "frozen_spec.json"
SEAL = LOGS / "seal.log"
MARK = LOGS / "unsealed.json"
SEALED_PARTS = ROOT / "sealed" / "parts"
SEALED_LOG = LOGS / "sealed_files.log"


class SealError(RuntimeError):
    pass


def _lines() -> list[str]:
    return [l for l in SEAL.read_text().splitlines() if l.strip()] if SEAL.exists() else []


def record(stage: str, **payload) -> dict:
    lines = _lines()
    prev = hashlib.sha256(lines[-1].encode()).hexdigest() if lines else None
    rec = {"stage": stage, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "prev": prev, **payload}
    with SEAL.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    return rec


def stages() -> list[dict]:
    return [json.loads(l) for l in _lines()]


def verify_chain() -> bool:
    lines = _lines()
    for a, b in zip(lines, lines[1:]):
        if json.loads(b)["prev"] != hashlib.sha256(a.encode()).hexdigest():
            return False
    return True


def log_sealed_parts() -> int:
    parts = sorted(SEALED_PARTS.glob("sealed*.parquet"))
    with SEALED_LOG.open("w") as f:
        for p in parts:
            f.write(f"{p.name}\t{sha256_file(p)}\n")
    return len(parts)


def check_sealed_untouched() -> dict:
    want = dict(l.split("\t") for l in SEALED_LOG.read_text().splitlines() if l.strip())
    have = {p.name for p in SEALED_PARTS.glob("sealed*.parquet")}
    bad = [n for n, h in want.items() if n not in have or sha256_file(SEALED_PARTS / n) != h]
    extra = sorted(have - set(want))
    return {"n_logged": len(want), "n_present": len(have), "mismatch": bad, "unlogged": extra,
            "ok": not bad and not extra}


def freeze(spec: dict) -> str:
    jdump(spec, SPEC)
    h = sha256_file(SPEC)
    record("S7_freeze", frozen_spec_sha256=h)
    return h


def unseal(spec_path: Path = SPEC, mark: Path = MARK) -> pd.DataFrame:
    if not spec_path.exists():
        raise SealError("frozen_spec.json missing: freeze before unsealing")
    fr = [r for r in stages() if r["stage"] == "S7_freeze"]
    if not fr:
        raise SealError("no S7_freeze record in seal.log")
    if sha256_file(spec_path) != fr[-1]["frozen_spec_sha256"]:
        raise SealError("frozen_spec.json changed after the freeze")
    if not verify_chain():
        raise SealError("seal.log hash chain broken")
    if mark.exists():
        raise SealError(f"Frame-N outcomes were already unsealed ({mark.read_text()[:200]})")
    chk = check_sealed_untouched()
    if not chk["ok"]:
        raise SealError(f"sealed parts changed: {chk}")
    df = pd.concat([pd.read_parquet(p) for p in sorted(SEALED_PARTS.glob("sealed*.parquet"))], ignore_index=True)
    jdump({"unsealed_at": time.strftime("%Y-%m-%d %H:%M:%S"), "frozen_spec_sha256": fr[-1]["frozen_spec_sha256"],
           "n_sealed_parts": chk["n_logged"], "rows": len(df)}, mark)
    record("S8_unseal", frozen_spec_sha256=fr[-1]["frozen_spec_sha256"], rows=len(df))
    return df
