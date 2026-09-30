#!/usr/bin/env python3
"""S0 FORMAT FIRST: write the method_out.json skeleton, validate it against exp_gen_sol_out (hard gate; EXP9 died on
output format), and record sha256 provenance of every copied library file."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
from common import E6, E7, E8, LIB, LOGS, ROOT, jdump, network_guard, setup_logger, sha256_file, validate_out  # noqa: E402

network_guard()
logger = setup_logger("s0")

COPIED = {"ego.py": E8 / "lib/ego.py", "ego_ctx.py": E8 / "lib/ego_ctx.py", "common_exp8.py": E8 / "lib/common.py",
          "rq1stats.py": E8 / "lib/rq1stats.py", "seal_exp8.py": E8 / "lib/seal.py",
          "build_features_exp8.py": E8 / "build_features.py", "d3.py": E7 / "lib/d3.py",
          "traj_exp6.py": E6 / "lib/traj.py", "lib_outcomes.py": E6 / "lib/lib_outcomes.py"}


@logger.catch(reraise=True)
def main() -> None:
    skel = {"metadata": {"artifact": "rq2_trajectories_rerun", "status": "skeleton", "stages_done": []},
            "datasets": [{"dataset": "rq2_concepts", "examples": [
                {"input": json.dumps({"name": "skeleton", "group": "CS+Eng", "split": "DEV"}),
                 "output": json.dumps({"O2r_resid_tercile": None}),
                 "predict_open_axis": "nan", "predict_decomposition": json.dumps({}),
                 "metadata_ci": 0, "metadata_split": "DEV", "metadata_group": "CS+Eng"}]}]}
    p = ROOT / "method_out.json"
    p.write_text(json.dumps(skel, indent=1))
    validate_out("S0", p, logger)
    prov = {}
    for name, src in COPIED.items():
        dst = LIB / name
        prov[name] = {"source": str(src.relative_to(src.parents[4])), "sha256_source": sha256_file(src),
                      "sha256_workspace": sha256_file(dst), "identical": sha256_file(src) == sha256_file(dst)}
    prov["ego_ctx.py"]["patch"] = (LOGS / "ego_ctx_patch.diff").read_text()
    jdump(prov, LOGS / "provenance.json")
    logger.info(f"provenance: {sum(v['identical'] for v in prov.values())}/{len(prov)} byte-identical copies "
                "(ego_ctx.py patched for paths)")


if __name__ == "__main__":
    main()
