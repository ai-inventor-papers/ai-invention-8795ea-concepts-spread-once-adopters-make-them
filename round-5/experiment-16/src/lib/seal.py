"""Hash-chained seal log (logs/seal.log): every entry records the sha256 of the sealed file(s), a timestamp and the
hash of the previous entry, so any later edit of a sealed file or of the log itself is detectable."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from common import LOGS, sha256_file

LOG = LOGS / "seal.log"


def _lines() -> list[str]:
    return [l for l in LOG.read_text().splitlines() if l.strip()] if LOG.exists() else []


def record(stage: str, **kw) -> dict:
    prev = _lines()
    prev_hash = hashlib.sha256(prev[-1].encode()).hexdigest() if prev else "GENESIS"
    ent = {"stage": stage, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "prev": prev_hash, **kw}
    with LOG.open("a") as f:
        f.write(json.dumps(ent, sort_keys=True) + "\n")
    return ent


def verify_chain() -> bool:
    L = _lines()
    for i, l in enumerate(L):
        e = json.loads(l)
        want = hashlib.sha256(L[i - 1].encode()).hexdigest() if i else "GENESIS"
        if e["prev"] != want:
            return False
    return True


def seal_file(stage: str, path: Path, **kw) -> dict:
    return record(stage, file=str(Path(path).name), sha256=sha256_file(path), **kw)


def check_sealed(stage: str, path: Path) -> bool:
    ents = [json.loads(l) for l in _lines() if json.loads(l)["stage"] == stage]
    return bool(ents) and ents[-1]["sha256"] == sha256_file(path) and verify_chain()
