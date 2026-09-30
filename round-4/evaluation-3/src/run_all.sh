#!/usr/bin/env bash
# Full pipeline, in order. One BLAS thread per process and <= 3 workers (4-CPU box; see README "Resource note").
set -euo pipefail
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
uv sync
# STEP 0 seal: only re-run if you intend to re-freeze (it rewrites results/boundary_spec.json and logs/seal.log)
# uv run python seal.py
uv run python partb_core.py --stage t0 --workers 3                   # GATE T0 (stops Part B on failure)
uv run python partb_core.py --stage b1 --workers 3 --nboot 1000      # B1 post-onset re-score
uv run python partb_core.py --stage b2 --workers 3 --nboot 1000      # B2 per-group table
uv run python spec_curve.py --null 200 --workers 3                   # B3 specification curve (~5 min)
uv run python heterogeneity.py --nperm 1000 --nboot 1000             # B4 sub-units, meta-regression, LIFEENV
uv run python step3_drca.py                                          # STEP 3 D_rca_pers vs D_rca_persist_k
uv run python figures.py
uv run python build_corrections.py                                   # STEP 4 corrections pack + ledger
uv run python verify_ledger.py                                       # STEP 5 independent ledger check
uv run python eval.py                                                # STEP 6 eval_out.json
uv run python audit_headlines.py                                     # independent re-derivation + shuffled placebo
