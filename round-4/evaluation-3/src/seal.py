#!/usr/bin/env python3
"""STEP 0: inputs manifest + hash-frozen boundary_spec.json + logs/seal.log (before ANY Part B statistic).

Only DEV rows (split == DEV: CS/Eng/BGM/Med homes, t0 2003-09) are read to freeze the OPEN z-constants and the
PC1 loadings. No held-out outcome column is touched here."""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"          # 4-CPU box: one BLAS thread per process (the previous attempt died on thread exhaustion)

import datetime as dt
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger

from common import (COMP_SIGN, COMPONENTS, DEV_UNITS, E5, E7, E8, E9, EV2, DS2, HELD4, LOGS, R2, REPORT, RES, RUN,
                    SEED, UNITS6, jdump, rel, sha256)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "seal_step.log", rotation="30 MB", level="DEBUG")

INPUTS = [E8 / p for p in ["data/analysis_table.parquet", "data/frame_arrays.npz", "data/features_basic.parquet",
                           "data/ego_features.parquet", "inputs/field_backbone.json", "lib/rq1stats.py", "rederive.py",
                           "build_features.py", "lib/indicators.py", "README.md"]] + \
    [E8 / "results" / f for f in ["portability_table.csv", "heldout_unit_results.csv", "heldout_summary.json",
                                  "rq1_heldout.json", "prereg_verdicts.json", "frozen_spec.json",
                                  "learned_vs_single_heldout.json", "sensitivities_pooled.json",
                                  "sensitivities_heldout.csv", "prereg_b5_minus_reach.csv", "indicator_dictionary.csv",
                                  "deviations.json", "case_exemplars.json"]] + \
    [E5 / "frame_concepts.csv", E5 / "concept_features_basic.csv", E5 / "scan/year_field_totals.npz"] + \
    [E7 / "results" / f for f in ["step2_dev.json", "step2_heldout.json", "frontier_result.json", "frozen_spec.json",
                                  "deviations.json", "state_panel_dev.parquet"]] + \
    [EV2 / f for f in ["text_corrections.md", "claims_ledger.csv", "o5_validation.json", "frame_agreement.json",
                       "record_tables/o5_associations.csv", "record_tables/o5_coverage_by_group_source.csv"]] + \
    [REPORT, E9 / ".aii_worker_result.json", R2 / "research_report.md"]

GENERIC_HEADS = ["variation", "growth", "rate", "coefficient", "model", "analysis", "method", "theory", "effect",
                 "system", "index", "distribution", "process", "function", "measure", "factor", "network", "structure"]


def dev_constants(A: pd.DataFrame) -> dict:
    D = A[A.split == "DEV"]
    assert set(D.unit.unique()) <= set(DEV_UNITS) and D.t0.max() <= 2009
    mu = {c: float(D[c].mean()) for c in COMPONENTS}
    sd = {c: float(D[c].std(ddof=1)) for c in COMPONENTS}
    Zd = np.column_stack([COMP_SIGN[c] * (D[c] - mu[c]) / sd[c] for c in COMPONENTS])
    comp = np.all(np.isfinite(Zd), 1)
    pcs = {}
    for s in range(2, 7):
        for sub in itertools.combinations(range(6), s):
            X = Zd[comp][:, sub]
            C = np.cov(X, rowvar=False)
            w, V = np.linalg.eigh(C)
            v = V[:, -1]
            # sign rule: new_edge_rate loading positive if present, else the sum of loadings positive
            anchor = v[list(sub).index(0)] if 0 in sub else v.sum()
            v = v * (1 if anchor >= 0 else -1)
            pcs["|".join(COMPONENTS[i] for i in sub)] = {"loadings": v.tolist(), "var_explained": float(w[-1] / w.sum())}
    return {"mu": mu, "sd": sd, "n_dev": int(len(D)), "n_dev_complete": int(comp.sum()), "pc1": pcs}


@logger.catch(reraise=True)
def main() -> None:
    man = []
    for p in INPUTS:
        man.append({"path": rel(p), "exists": p.exists(), "bytes": p.stat().st_size if p.exists() else None,
                    "sha256": sha256(p) if p.exists() else "NOT_FOUND"})
    jdump({"generated_utc": dt.datetime.now(dt.timezone.utc).isoformat(), "files": man}, RES / "inputs_manifest.json")
    logger.info(f"inputs manifest: {sum(m['exists'] for m in man)}/{len(man)} present")

    A = pd.read_parquet(E8 / "data/analysis_table.parquet",
                        columns=["ci", "split", "unit", "t0"] + COMPONENTS)
    const = dev_constants(A)
    logger.info(f"DEV constants from {const['n_dev']} DEV rows; complete {const['n_dev_complete']}")

    it4 = RUN / "round-4"
    listing = []
    for d in sorted(it4.iterdir()):
        if d.is_dir():
            files = [f for f in d.rglob("*") if f.is_file() and ".venv" not in f.parts][:4000]
            cohort_out = [rel(f) for f in files if any(k in f.name.lower() for k in ("cohort", "2015", "outcome"))
                          and f.suffix in (".parquet", ".csv", ".json")]
            listing.append({"dir": rel(d), "mtime_utc": dt.datetime.fromtimestamp(d.stat().st_mtime, dt.timezone.utc).isoformat(),
                            "n_files": len(files), "candidate_cohort_outcome_files": cohort_out})
    spec = {
        "title": "Openness boundary evaluation - frozen specification (Part B, EXPLORATORY on already-unsealed held-out)",
        "status": "EXPLORATORY: the Exp8 held-out groups were unsealed in Exp5 and Exp8; nothing here can confirm OPEN",
        "estimator": "Exp8 psp: rank x,y within unit; OLS-residualise on [1, rank(B5 + extra controls), t0 dummies "
                     "(+ group dummies in COH units)]; Pearson of residuals (vendor/rq1stats.psp_point)",
        "pooling": {"primary_record_comparable": "DL on Fisher z over the 4 held-out groups PHYS/LIFEENV/SOC/MATHDEC "
                    "(Exp8 heldout.pool_block; the record's +0.377 etc. are DL4)",
                    "plan_6unit": "DL over PHYS/LIFEENV/SOC/MATHDEC/COH_DEVHOME/COH_OTHER (reported alongside)",
                    "units4": HELD4, "units6": UNITS6,
                    "note": "The plan text says the record pools over 6 units; Exp8 heldout.py pools over HELD_GROUPS (4). "
                            "Both are reported; T0 uses DL4 with bootstrap se_z exactly as Exp8."},
        "B5": ["logvol", "growth_c", "offhome_share", "entropy", "reach"],
        "open_definition": {"components": COMPONENTS, "signs": COMP_SIGN,
                            "z": "z_c = sign_c * (x - mu_DEV) / sd_DEV (frozen constants below, applied to all rows)",
                            "OPEN": "mean of available component z; defined when >= 4 of 6 present",
                            "OPEN_PC1": "sum of loadings * z over the 6 components (complete cases), DEV PC1, "
                                        "sign so the new_edge_rate loading is positive",
                            "subset_rule": "subset of size s is defined when >= ceil(2s/3) of its components present",
                            "dev_constants": const},
        "spec_grid": {"subsets": "all 63 non-empty subsets of the 6 components",
                      "weightings": ["equal", "pc1 (refit on DEV for each subset of size >= 2)"],
                      "n_composites": 120,
                      "outcomes": ["O2r_m30", "O2r_m50", "O2r_resid", "O2r_resid_N"],
                      "controls": {"C0": "B5 (no t0 dummies; group dummies kept in COH units)",
                                   "C1": "B5 + t0 dummies (Exp8 default)",
                                   "C2": "C1 + rank(label_coverage_early) [column found in analysis_table]",
                                   "C3": "C1 + rank(CONTACT_REACH)"},
                      "label_coverage_column": "label_coverage_early",
                      "n_specs": 1920, "se": "analytic Fisher z, var = 1/(n - k - 3), k = columns of Z incl. intercept",
                      "null": {"type": "Freedman-Lane", "draws": 200,
                               "detail": "per unit x outcome x control: y* = fitted(y ~ Z_C) + within-unit permutation of "
                                         "residuals; all 1,920 specs recomputed per draw"},
                      "headline": {"subset": "all 6", "weights": "equal", "outcome": "O2r_m50", "control": "C1",
                                   "bootstrap_B": 2000},
                      "calibration": "headline + 50 random specs: 1,000-draw concept bootstrap; if the median "
                                     "bootstrap/analytic CI-width ratio > 1.2 the analytic SEs are inflated by it"},
        "B1": {"post": "states() on gw (years t0..t0+2 only, zero before t0) -> D_vol_post, M0_density_post",
               "footprint": {"D_vol_pre": "# off-home fields entered (full-history state machine) by t0-1",
                             "footprint_share": "D_vol_pre / max(D_vol_end, 1)",
                             "log_pre_papers": "log1p(sum N over t0-3..t0-1) (grounded papers)"},
               "verdict_rule": {"MOST": "upper CI of pooled psp_post < 0.5 * pooled psp_full",
                                "LITTLE": "paired difference (full - post) pooled CI includes 0",
                                "PARTIAL": "otherwise"},
               "bootstrap_B": 1000},
        "B4": {"subunits": "primary home field (first listed, 26-field level) x onset period (2003-09 / 2010-14) over "
                           "the 6 held-out units; cells with n (O2r_m50 non-missing and OPEN defined) < 60 merge into "
                           "'<unit>_other' (if still < 60 it is dropped); fallback threshold 40 if < 20 sub-units",
               "min_n": 60, "fallback_min_n": 40,
               "traits": ["median_label_coverage", "median_log_early_volume", "share_multi_home", "share_generic",
                          "median_O2r_m50", "sd_OPEN", "mean_t0"],
               "generic_rule": {"single_token_zipf_ge": 4.0, "wordfreq_lang": "en", "head_nouns": GENERIC_HEADS,
                                "head": "last token of the lower-cased label after stripping parentheses"},
               "meta_regression": "REML random effects, one trait at a time, Knapp-Hartung; permutation p (1,000 trait "
                                  "shuffles); Holm over the 7 traits; joint model with the 2 strongest",
               "lifeenv_verdict_rule": {
                   "COVERAGE": "coverage slope CI > 0 AND reweighted LIFEENV psp CI overlaps others' pooled CI",
                   "VARIANCE": "SD-ratio CI < 1 AND Thorndike-corrected LIFEENV psp inside others' pooled CI",
                   "UNEXPLAINED": "otherwise (domain boundary)"}},
        "seeds": {"master": SEED}, "bootstrap": {"table_cells": 1000, "headline": 2000, "null_draws": 200,
                                                  "meta_perm": 1000},
        "llm": "no LLM calls (optional GENERIC LLM check not run; $0 spent)",
        "iter4_gen_art_listing_at_seal": listing,
        "cohort_2015_16_statement": "At seal time no 2015-16 cohort outcome file is read by this evaluation; any file "
                                    "listed under candidate_cohort_outcome_files above belongs to other iteration-4 "
                                    "artifacts and is NOT read by Part B.",
    }
    jdump(spec, RES / "boundary_spec.json")
    h = sha256(RES / "boundary_spec.json")
    ts = dt.datetime.now(dt.timezone.utc).isoformat()
    with open(LOGS / "seal.log", "a") as f:
        f.write(f"sealed_utc {ts}\nsha256 {h}\n")
    logger.info(f"SEALED boundary_spec.json sha256={h} at {ts}")


if __name__ == "__main__":
    main()
