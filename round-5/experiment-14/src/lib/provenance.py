"""Record sha256 + size of every upstream input read by this artifact (results/provenance.json).
Paths are stored RELATIVE to the run's 3_invention_loop directory (no absolute server paths are published)."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import EXP3, EXP5, EXP8, EXP10, EXP11, LOOP, RES, RESEARCH3, jdump, sha256_file

FILES = [*sorted((EXP11 / "data/frame_matches_long").glob("part_*.parquet")), EXP11 / "data/yearly_panel.parquet",
         EXP11 / "data/counts_m.parquet", EXP11 / "inputs/topic_ids.json", EXP11 / "inputs/topic_meta.csv",
         *[EXP11 / f"inputs/backbone/slice{s}.npz" for s in range(3)], EXP5 / "frame_concepts.csv",
         EXP5 / "scan/agg_counts.parquet", EXP8 / "data/analysis_table.parquet", EXP8 / "lib/rq1stats.py",
         EXP10 / "data/passC_early.parquet", EXP10 / "data/analysis_cohort.parquet",
         EXP10 / "data/passC_pre_agg.parquet", EXP10 / "data/ego_open_exp5.parquet",
         EXP10 / "data/ego_open_cohort.parquet", EXP10 / "results/frozen_spec.json",
         EXP10 / "results/s3_decision.json", EXP10 / "logs/sealed_files.log",
         RESEARCH3 / "raw/fetch/cheng_all.txt", EXP3 / "backbone/slice0.npz"]


def main() -> None:
    out = {"root": "paths relative to <run>/3_invention_loop", "files": {}}
    for p in FILES:
        out["files"][str(p.relative_to(LOOP))] = {"sha256": sha256_file(p), "bytes": p.stat().st_size}
    out["note"] = ("EXP10 data/sealed/parts/sealed_*.parquet (2,040 files) are checked against EXP10 "
                   "logs/sealed_files.log inside S1 (results/s1_build.json -> V_cohort.sealed_ok)")
    jdump(out, RES / "provenance.json")


if __name__ == "__main__":
    main()
