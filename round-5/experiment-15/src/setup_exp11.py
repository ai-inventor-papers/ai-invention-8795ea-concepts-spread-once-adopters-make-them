#!/usr/bin/env python3
"""STEP 0: copy the sealed Exp11 code into ./exp11_code with a PATH-ONLY patch, write patch_diff.txt (asserting
that only path lines changed) and verify the Exp11 seal (gate G0) on the ORIGINAL files.

Reads (read-only) the Exp11 artifact under $AII_RUN_ROOT/3_invention_loop/iter_4/gen_art/gen_art_experiment_11.
Writes exp11_code/**, exp11_code/patch_diff.txt, results/seal_verification.json."""
from __future__ import annotations

import difflib
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parent
RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(WS.parents[3])))
E11_REL = "3_invention_loop/iter_4/gen_art/gen_art_experiment_11"
E11 = RUN_ROOT / E11_REL
DST = WS / "exp11_code"
SCRIPTS = ["analysis_fe.py", "event_study.py", "sequence.py", "partners.py", "unit_tests.py", "build_d3.py"]

# (file, old, new) -- every replacement is a path line; asserted below
COMMON_OLD = '''INPUTS = ROOT / "inputs"
DATA = ROOT / "data"'''
COMMON_NEW = '''RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(ROOT.parents[4])))
SRC = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_11"
INPUTS = SRC / "inputs"
DATA_IN = SRC / "data"
RES_IN = SRC / "results"
LOGS_IN = SRC / "logs"
DATA = ROOT / "data"'''
PATCHES = [
    ("lib/common.py", COMMON_OLD, COMMON_NEW),
    ("lib/common.py", 'RUN_ROOT = Path(os.environ.get("AII_RUN_ROOT", str(ROOT.parents[3])))\n', ""),
    ("lib/seal_m.py", "from common import DATA, LIB, LOGS, RES, jdump, sha256_file",
     "from common import DATA_IN, LIB, LOGS, LOGS_IN, RES_IN, jdump, sha256_file"),
    ("lib/seal_m.py", 'SPEC = RES / "frozen_spec.json"', 'SPEC = RES_IN / "frozen_spec.json"'),
    ("lib/seal_m.py", 'SEAL = LOGS / "seal.log"', 'SEAL = LOGS_IN / "seal.log"'),
    ("lib/seal_m.py", 'OUTCOME_FILE = DATA / "d3_concept_year.parquet"',
     'OUTCOME_FILE = DATA_IN / "d3_concept_year.parquet"'),
    ("lib/seal_m.py", 'sha256_file(DATA / "yearly_features.parquet")', 'sha256_file(DATA_IN / "yearly_features.parquet")'),
    ("lib/ego_ctx.py", "from common import DATA, INPUTS", "from common import DATA_IN as DATA, INPUTS"),
    ("analysis_fe.py", "from common import DATA, RES, jdump, load_frame, setup_logger",
     "from common import DATA, DATA_IN, LOGS_IN, RES, RES_IN, jdump, load_frame, setup_logger"),
    ("analysis_fe.py", '(RES / "frozen_spec.json")', '(RES_IN / "frozen_spec.json")'),
    ("analysis_fe.py", 'pd.read_parquet(DATA / "yearly_features.parquet")', 'pd.read_parquet(DATA_IN / "yearly_features.parquet")'),
    ("analysis_fe.py", '(Path(__file__).resolve().parent / "logs" / "seal.log")', '(LOGS_IN / "seal.log")'),
    ("event_study.py", "from common import DATA, RES, jdump, setup_logger",
     "from common import DATA, DATA_IN, RES, RES_IN, jdump, setup_logger"),
    ("event_study.py", 'pd.read_parquet(DATA / "yearly_panel.parquet")', 'pd.read_parquet(DATA_IN / "yearly_panel.parquet")'),
    ("event_study.py", 'pd.read_parquet(DATA / "closure_jumps.parquet")', 'pd.read_parquet(DATA_IN / "closure_jumps.parquet")'),
    ("event_study.py", '(RES / "frozen_spec.json")', '(RES_IN / "frozen_spec.json")'),
    ("sequence.py", "from common import DATA, RES, jdump, load_frame, setup_logger",
     "from common import DATA, DATA_IN, RES, jdump, load_frame, setup_logger"),
    ("sequence.py", 'np.load(DATA / "grounded_V.npz")', 'np.load(DATA_IN / "grounded_V.npz")'),
    ("sequence.py", 'pd.read_parquet(DATA / "yearly_features.parquet")', 'pd.read_parquet(DATA_IN / "yearly_features.parquet")'),
    ("sequence.py", 'pd.read_parquet(DATA / "yearly_panel.parquet")', 'pd.read_parquet(DATA_IN / "yearly_panel.parquet")'),
    ("partners.py", "from common import DATA, INPUTS, RES, RUN_ROOT, jdump, load_frame, read_parquet_parts, setup_logger",
     "from common import DATA, DATA_IN, INPUTS, RES, RES_IN, RUN_ROOT, jdump, load_frame, read_parquet_parts, setup_logger"),
    ("partners.py", '(RES / "topic_types.csv")', '(RES_IN / "topic_types.csv")'),
    ("partners.py", '(DATA / "static_partners.parquet")', '(DATA_IN / "static_partners.parquet")'),
    ("partners.py", '(DATA / "port_static.parquet")', '(DATA_IN / "port_static.parquet")'),
    ("partners.py", '(DATA / "w3_comms.json")', '(DATA_IN / "w3_comms.json")'),
    ("partners.py", 'read_parquet_parts(DATA / "frame_matches_long"', 'read_parquet_parts(DATA_IN / "frame_matches_long"'),
    ("partners.py", '(RES / "topic_type_benchmark.json")', '(RES_IN / "topic_type_benchmark.json")'),
]
PATH_TOKENS = ("DATA", "RES", "LOGS", "INPUTS", "RUN_ROOT", "SRC", "ROOT", "Path(", "from common import")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def copy_and_patch() -> dict:
    (DST / "lib").mkdir(parents=True, exist_ok=True)
    files = SCRIPTS + [f"lib/{p.name}" for p in sorted((E11 / "lib").glob("*.py"))]
    texts = {f: (E11 / f).read_text() for f in files}
    new = dict(texts)
    for f, old, rep in PATCHES:
        if old not in new[f]:
            raise RuntimeError(f"patch anchor not found in {f}: {old[:60]}")
        new[f] = new[f].replace(old, rep)
    diff_lines, changed = [], []
    for f in files:
        (DST / f).write_text(new[f])
        if new[f] != texts[f]:
            changed.append(f)
            d = list(difflib.unified_diff(texts[f].splitlines(), new[f].splitlines(), f"E11/{f}", f"exp11_code/{f}",
                                          lineterm="", n=0))
            diff_lines += d
            for ln in d:
                if ln.startswith(("+", "-")) and not ln.startswith(("+++", "---")):
                    body = ln[1:].strip()
                    if body and not any(t in body for t in PATH_TOKENS):
                        raise RuntimeError(f"non-path line changed in {f}: {ln}")
    (DST / "patch_diff.txt").write_text("\n".join(diff_lines) + "\n")
    for d in ("data", "results", "logs", "figures"):
        (DST / d).mkdir(exist_ok=True)
    return {"files_copied": files, "files_patched": changed, "n_diff_lines": len(diff_lines),
            "only_path_lines_changed": True}


def verify_seal() -> dict:
    spec_p, seal_p = E11 / "results/frozen_spec.json", E11 / "logs/seal.log"
    rec = json.loads(seal_p.read_text())
    spec = json.loads(spec_p.read_text())
    out = {"time": time.strftime("%Y-%m-%d %H:%M:%S"), "source_artifact": E11_REL,
           "frozen_spec_sha256_sealed": rec["frozen_spec_sha256"], "frozen_spec_sha256_now": sha(spec_p)}
    out["frozen_spec_ok"] = out["frozen_spec_sha256_now"] == rec["frozen_spec_sha256"]
    files = {}
    for name, h in spec["sha256"].items():
        cands = [E11 / "lib" / name, E11 / "data" / name, E11 / name]
        p = next((c for c in cands if c.exists()), None)
        now = sha(p) if p else None
        files[name] = {"sealed": h, "now": now, "ok": now == h, "path": str(p.relative_to(E11)) if p else None}
    out["files"] = files
    out["n_files"] = len(files)
    out["n_ok"] = sum(v["ok"] for v in files.values())
    out["G0_pass"] = bool(out["frozen_spec_ok"] and out["n_ok"] == len(files))
    out["mismatches"] = [k for k, v in files.items() if not v["ok"]]
    return out


def main() -> None:
    info = copy_and_patch()
    g0 = verify_seal()
    g0["copy"] = info
    (WS / "results").mkdir(exist_ok=True)
    (WS / "results/seal_verification.json").write_text(json.dumps(g0, indent=1))
    print(json.dumps({k: g0[k] for k in ("frozen_spec_ok", "n_files", "n_ok", "G0_pass", "mismatches")}))
    print("patched:", info["files_patched"])
    if not g0["G0_pass"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
