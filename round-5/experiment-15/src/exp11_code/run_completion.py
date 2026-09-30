#!/usr/bin/env python3
"""iter-5 STEP 1 (Part C.1): complete the sealed Exp11 body models from the SEALED code (analysis_fe.py, unchanged
except for paths). Reporting only -- the DEV verdict (NOT SUPPORTED) is copied, not re-decided.

  1. rebuild the panel through the seal gate (seal_m.attach_outcomes, reason='iter5 completion') and assert equality
     with the cached Exp11 data/yearly_panel.parquet
  2. gate G1: DEV point estimates (n_boot=0) must equal Exp11 fe_results.json DEV within 1e-8
  3. OLD_HELDOUT and COHORT body models (500 concept-cluster bootstrap refits each, as declared in Exp11 deviations)
  4. the pre-declared DEV robustness list (never ran in Exp11) and out-of-fold PPML predictions + deviance by body
  5. H-M5 (signs of H-M1 / H-M2 on OLD_HELDOUT and COHORT)
Writes results/fe_results_completed.json, data/predictions.parquet, data/boot_fe_{OLD_HELDOUT,COHORT}.parquet."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, LOGS_IN, RES, RES_IN, jdump, load_frame, setup_logger
from panel_m import BODIES, build_panel, estimation_sample, frame_plus

KEYS_G1 = [("H_M1_density", "b"), ("H_M2_open", "b"), ("lpm_density", "b"), ("lpm_open", "b"),
           ("H_M3_point", "b_fwd"), ("H_M3_point", "b_rev"), ("H_M3_point", "diff")]


def compare_panels(a: pd.DataFrame, b: pd.DataFrame) -> dict:
    cols = ["y_next", "density", "OPEN_home", "log1p_home", "log1p_all", "log1p_deg", "log_at_risk", "any_next"]
    a = a.sort_values(["ci", "year"]).reset_index(drop=True)
    b = b.sort_values(["ci", "year"]).reset_index(drop=True)
    out = {"shape_rebuilt": list(a.shape), "shape_cached": list(b.shape),
           "keys_equal": bool(len(a) == len(b) and (a.ci.to_numpy() == b.ci.to_numpy()).all()
                              and (a.year.to_numpy() == b.year.to_numpy()).all())}
    if out["keys_equal"]:
        for c in cols:
            x, y = a[c].to_numpy(float), b[c].to_numpy(float)
            nan_eq = bool((np.isnan(x) == np.isnan(y)).all())
            ok = np.isfinite(x) & np.isfinite(y)
            out[c] = {"nan_pattern_equal": nan_eq, "max_abs_diff": float(np.max(np.abs(x[ok] - y[ok]))) if ok.any() else 0.0}
    out["equal"] = bool(out["keys_equal"] and all(out[c]["nan_pattern_equal"] and out[c]["max_abs_diff"] == 0
                                                   for c in cols))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot-other", type=int, default=500)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--skip-boot", action="store_true")
    args = ap.parse_args()
    logger = setup_logger("run_completion")
    import analysis_fe as A
    t = time.time()
    from seal_m import attach_outcomes
    spec = json.loads((RES_IN / "frozen_spec.json").read_text())
    zc = spec["features"]["z_constants"]
    fr = frame_plus(load_frame())
    yf = pd.read_parquet(DATA_IN / "yearly_features.parquet")
    yo = attach_outcomes(yf, reason="iter5 completion (exp11_code/run_completion.py)")
    p = build_panel(yo, fr, zc)
    cached = pd.read_parquet(DATA_IN / "yearly_panel.parquet")
    cmp_ = compare_panels(p, cached)
    logger.info(f"panel rebuilt {p.shape} vs cached {cached.shape}: equal={cmp_['equal']}")
    del cached, yo
    old = json.loads((RES_IN / "fe_results.json").read_text())
    res: dict = {"dev_verdict": "DEV verdict unchanged: NOT SUPPORTED (both H-M1 and H-M2 CIs include 0 on DEV)",
                 "spec_sha": json.loads((LOGS_IN / "seal.log").read_text())["frozen_spec_sha256"],
                 "panel_rebuild_check": cmp_, "sample_counts": old["sample_counts"], "DEV": old["DEV"]}
    # ---- G1
    dev0 = A.body_results(p, "DEV", 0, args.workers, logger)
    g1 = {}
    for k, s in KEYS_G1:
        a, b = dev0[k][s], old["DEV"][k][s]
        g1[f"{k}.{s}"] = {"new": a, "exp11": b, "abs_diff": abs(a - b)}
    g1_pass = all(v["abs_diff"] < 1e-8 for v in g1.values())
    res["G1_dev_reproduction"] = {"pass": g1_pass, "cells": g1}
    logger.info(f"G1 pass={g1_pass}: max diff {max(v['abs_diff'] for v in g1.values()):.2e}")
    if not g1_pass:
        jdump(res, RES / "fe_results_completed.json")
        raise RuntimeError("G1 failed: DEV point estimates do not reproduce Exp11")
    jdump(res, RES / "fe_results_completed.json")
    for b in ("OLD_HELDOUT", "COHORT"):
        res[b] = A.body_results(p, b, 0 if args.skip_boot else args.boot_other, args.workers, logger)
        jdump(res, RES / "fe_results_completed.json")
    # H-M5 signs
    h5 = {}
    for b in ("OLD_HELDOUT", "COHORT"):
        r = res[b]
        bd, bo = r["H_M1_density"], r["H_M2_open"]
        bs = r.get("bootstrap", {})
        h5[b] = {"b_density": bd["b"], "ci_density_crv1": bd["ci"], "ci_density_boot": bs.get("b_density", {}).get("ci"),
                 "b_OPEN": bo["b"], "ci_OPEN_crv1": bo["ci"], "ci_OPEN_boot": bs.get("b_open", {}).get("ci"),
                 "sign_density_negative": bool(bd["b"] < 0), "sign_OPEN_positive": bool(bo["b"] > 0),
                 "DL_density": r.get("DL_density"), "DL_OPEN_home": r.get("DL_OPEN_home")}
    res["H_M5"] = {"by_body": h5, "holds_signs": bool(all(v["sign_density_negative"] and v["sign_OPEN_positive"]
                                                         for v in h5.values())),
                   "note": "H-M5 is a sign condition; the sealed verdict needs H-M1 & H-M2 on DEV, which failed."}
    res["H_M3"] = {b: {"point": res[b]["H_M3_point"], "boot_diff": res[b].get("bootstrap", {}).get("diff")}
                   for b in BODIES}
    jdump(res, RES / "fe_results_completed.json")
    res["robustness_DEV"] = A.robustness(p, logger)
    jdump(res, RES / "fe_results_completed.json")
    pr = A.oof_predictions(p, logger)
    pr.to_parquet(DATA / "predictions.parquet", index=False)
    res["prediction_deviance"] = {b: {m: A.deviance(d.y_next.to_numpy(float), d[f"pred_{m}"].to_numpy(float))
                                      for m in ("fe_density", "fe_open", "controls_only")}
                                  for b, d in pr.groupby("body")}
    res["seconds"] = time.time() - t
    jdump(res, RES / "fe_results_completed.json")
    logger.info(f"completion done in {(time.time()-t)/60:.1f} min")


if __name__ == "__main__":
    main()
