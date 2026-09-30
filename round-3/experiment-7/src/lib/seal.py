"""Freeze / unseal gate (EXP5 seal.py pattern): the held-out stage refuses to run unless logs/seal.log records the
sha256 of results/frozen_spec.json and of every analysis .py file, and refuses a second unseal."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "results" / "frozen_spec.json"
SEAL = ROOT / "logs" / "seal.log"
UNSEAL = ROOT / "logs" / "unseal.log"
CODE = ["method.py", "lib/d3.py", "lib/models.py", "lib/analysis.py", "lib/exp5.py", "lib/h2_exp6.py", "lib/stats_core.py",
        "lib/cfg_exp6.py", "lib/seal.py"]


class SealedError(RuntimeError):
    pass


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def code_hashes() -> dict[str, str]:
    return {c: sha(ROOT / c) for c in CODE if (ROOT / c).exists()}


def freeze(spec: dict, git_commit: str | None) -> str:
    SPEC.write_text(json.dumps(spec, indent=1, default=str))
    h = sha(SPEC)
    rec = {"time": datetime.now(timezone.utc).isoformat(), "frozen_spec_sha256": h, "code_sha256": code_hashes(),
           "git_commit": git_commit}
    SEAL.write_text(json.dumps(rec, indent=1))
    return h


def unseal(resume_reason: str | None = None) -> dict:
    """checks the seal, then records the (single) unseal. `resume_reason` allows re-entry after a crash of the
    held-out stage itself; every re-entry is appended to logs/unseal.log (never silent)."""
    if not SEAL.exists() or not SPEC.exists():
        raise SealedError("held-out data are sealed: run `method.py freeze` first")
    rec = json.loads(SEAL.read_text())
    if sha(SPEC) != rec["frozen_spec_sha256"]:
        raise SealedError("frozen_spec.json changed after the freeze")
    now = code_hashes()
    changed = [c for c, h in rec["code_sha256"].items() if now.get(c) != h]
    if UNSEAL.exists() and resume_reason is None:
        raise SealedError("held-out data were already unsealed once (logs/unseal.log exists)")
    if changed and resume_reason is None:
        raise SealedError(f"code changed after the freeze: {changed}")
    entry = {"time": datetime.now(timezone.utc).isoformat(), "frozen_spec_sha256": rec["frozen_spec_sha256"],
             "code_changed_since_freeze": changed, "resume_reason": resume_reason}
    with UNSEAL.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
