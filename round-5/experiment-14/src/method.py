#!/usr/bin/env python3
"""Orchestrator: Cheng et al. (2023) ideational consistency -- replication, size control and the reach-vs-depth
reversal on this run's selection bodies (EXP5 frame + EXP10 2015-17 cohort). Cache only, CPU only, $0 LLM.

Steps (run all in order, or one with --only):
  S0  frozen spec + seal (before any model)             lib/s0_spec.py
  S1  build Cheng measures (cheng_features / static)     lib/build.py         [--sample N for staged scale-up]
  S2  construct-identity check                           lib/identity.py
  S3  test A: Cheng replication panel (A1/A1-NB/A2/A3)   lib/panel_cheng.py
  S3NB  re-fit A1-NB only (patches cheng_panel_models.json)  lib/panel_cheng.py
  S4  test B: static early trait, reach vs depth         lib/static_cheng.py
  S5  test C: within-panel reach vs depth                lib/panel_cheng.py
  S6  test D: Palla size x turnover                      lib/static_cheng.py
  S7  test E: HOME vs ALL coupling                       lib/static_cheng.py
  S8  verdict, figures, method_out.json, write-up        lib/outputs.py
Usage: uv run method.py [--only S3] [--sample 500] [--quick]"""
from __future__ import annotations

import argparse
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):   # one BLAS thread per process: the
    os.environ.setdefault(_v, "1")                                         # steps parallelise across processes
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import set_limits, setup_logger  # noqa: E402

STEPS = ["S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", type=str, default="")
    ap.add_argument("--sample", type=int, default=0, help="S1: number of EXP5 concepts (staged scale-up)")
    ap.add_argument("--quick", action="store_true", help="S3-S7: 10%% of concepts, few bootstrap draws (timing)")
    ap.add_argument("--workers", type=int, default=0)
    args = ap.parse_args()
    logger = setup_logger("method")
    set_limits(26.0)
    steps = [s.strip() for s in args.only.split(",")] if args.only else STEPS

    @logger.catch(reraise=True)
    def _run() -> None:
        for s in steps:
            t = time.time()
            logger.info(f"===== {s} start")
            if s == "S0":
                import s0_spec
                s0_spec.run(logger)
            elif s == "S1":
                import build
                build.run(logger, sample=args.sample, workers=args.workers)
            elif s == "S2":
                import identity
                identity.run(logger)
            elif s == "S3":
                import panel_cheng
                panel_cheng.run_A(logger, quick=args.quick, workers=args.workers)
            elif s == "S3NB":
                import panel_cheng
                panel_cheng.refit_nb(logger)
            elif s == "S4":
                import static_cheng
                static_cheng.run_B(logger, quick=args.quick)
            elif s == "S5":
                import panel_cheng
                panel_cheng.run_C(logger, quick=args.quick, workers=args.workers)
            elif s == "S6":
                import static_cheng
                static_cheng.run_D(logger, quick=args.quick)
            elif s == "S7":
                import static_cheng
                static_cheng.run_E(logger, quick=args.quick)
            elif s == "S8":
                import outputs
                outputs.run(logger)
            else:
                raise ValueError(f"unknown step {s}")
            logger.info(f"===== {s} done in {(time.time() - t) / 60:.1f} min")

    _run()


if __name__ == "__main__":
    main()
