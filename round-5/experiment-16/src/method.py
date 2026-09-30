#!/usr/bin/env python3
"""Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.

Stages (each a standalone, resumable script; run in this order by `python method.py --run-all`):
  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)
  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)
  s1_freeze.py          frozen spec + seal (before any outcome join)
  s2_variants.py        RAW, V1 rarefaction, V2 permutation null, V2b Chao Jaccard, V4 split halves
  s3_nulls.py           V3a backbone rewiring, V3b k-matched density null, V3c curveball persistence null
  tests/u_nulls.py      U3 curveball uniformity, U4 rewire calibration
  tests/planted.py      PC1 stationary thin-sample simulation, PC2 planted churn
  s4_composites.py      clean composites, S1b constants seal, V4 reliability (X side)
  s4b_outcome_rel.py    outcome reliability (O2r_m50, m = 25 halves)
  s5_size.py            size-dependence diagnostics
  s6_assoc.py           partial Spearman ladder per body / pooled, paired clean-vs-raw, groups, PC3
  s7_verdict.py         DL, disattenuation, P1-P3, Holm, VERDICT, figures
  s8_power.py           Frame-N power simulation
  rederive.py           independent re-derivation of the P1-P3 numbers and the pooled SB
Then (this file): method_out.json in exp_gen_sol_out format -- one example per concept with finite O2r_m50;
predictions from OLS fitted on DEV only (B5 standardised with the frozen EXP10 constants) applied to every body;
results/prediction_check.json; the concept-key cross-check against art_O7Dq4L02QnDN."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

from common import DATA, O5DIR, RES, jdump, setup_logger

STAGES = [("s0_gate.py", RES / "gate_t0.json"), ("tests/u_fast6.py", RES / "unit_tests_fast6.json"),
          ("s1_freeze.py", RES / "frozen_spec.json"), ("s2_variants.py", DATA / "s2_scalars_full.parquet"),
          ("s3_nulls.py", DATA / "v3_nulls_full.parquet"), ("tests/u_nulls.py", RES / "unit_tests_nulls.json"),
          ("tests/planted.py", RES / "planted_checks.json"), ("s4_composites.py", DATA / "clean_variants.parquet"),
          ("s4b_outcome_rel.py", RES / "reliability.json"), ("s5_size.py", RES / "size_dependence.json"),
          ("s6_assoc.py", RES / "clean_vs_raw_psp_cells.json"), ("s7_verdict.py", RES / "clean_vs_raw_psp.json"),
          ("s8_power.py", RES / "power_frame_n.json"), ("rederive.py", RES / "rederive.json")]
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
PRED_X = {"B5": None, "B5_plus_NOVCHURN_raw": "NOVCHURN_raw", "B5_plus_NOVCHURN_exc": "NOVCHURN_exc",
          "B5_plus_NOVCHURN_cfg": "NOVCHURN_cfg", "B5_plus_OPEN_home": "OPEN_home",
          "B5_plus_OPEN_home_clean": "OPEN_home_clean"}
INPUT_COLS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
              "participation__raw", "NOVCHURN_raw", "OPEN_home", "NOV_res_rare10", "edge_persistence_rare10",
              "NOVCHURN_rare10", "NOV_res_rare5", "edge_persistence_rare5", "NOVCHURN_rare5", "NOV_res_exc",
              "edge_persistence_exc", "edge_persistence_nullmean", "NOVCHURN_exc", "EP_chao", "NOVCHURN_chao",
              "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean",
              "OPEN_home_exc"]


def run_stages(force: bool) -> None:
    for script, out in STAGES:
        if out.exists() and not force:
            logger.info(f"skip {script} ({out.name} exists)")
            continue
        if script == "s1_freeze.py" and out.exists():
            logger.warning("frozen_spec.json exists: never re-freeze (seal)")
            continue
        logger.info(f"running {script}")
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def concept_key_check() -> dict:
    """Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its
    concept_recognition table and agreement of the OpenAlex level."""
    cv = pd.read_parquet(DATA / "clean_variants.parquet", columns=["concept_id", "body"])
    from common import DATA_IN
    lev = pd.concat([pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["concept_id", "level"]),
                     pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["concept_id", "level"])])
    norm = lambda v: "C" + str(v).lstrip("C").split(".")[0]  # noqa: E731  (frame ids are numeric; O5 uses 'C...')
    lev = dict(zip(lev.concept_id.map(norm), lev.level))
    cv["concept_id"] = cv.concept_id.map(norm)
    ids = set(cv.concept_id)
    seen, level_ok, n_rec = {}, 0, 0
    for p in sorted((O5DIR / "full_data_out").glob("full_data_out_*.json")):
        d = json.loads(p.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for e in ds["examples"]:
                n_rec += 1
                cid = e.get("metadata_openalex_id")
                if cid in ids:
                    seen[cid] = e.get("metadata_level")
        del d
    for cid, lv in seen.items():
        if cid in lev and lv is not None and int(lv) == int(lev[cid]):
            level_ok += 1
    cov = cv.assign(found=cv.concept_id.isin(seen))
    return {"dependency": "art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)",
            "n_recognition_rows": n_rec, "n_analysed": int(len(ids)), "n_found": int(len(seen)),
            "coverage_by_body": cov.groupby("body").found.mean().round(4).to_dict(),
            "level_agreement": level_ok / max(len(seen), 1)}


def exp12_crosscheck() -> dict:
    """EXP12 (art_uw4OeagJP3rv) open_features.parquet: cross-check of the home-build component values where it
    overlaps (EXP5 frame). EXP12 used its own home-paper definition, so agreement is reported, not required."""
    from common import RUN_ROOT
    p = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_12/open_features.parquet"
    if not p.exists():
        return {"available": False}
    o = pd.read_parquet(p)
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    m = cv[cv.frame == "exp5"].merge(o, on="ci", suffixes=("", "_e12"))
    out = {"available": True, "n_overlap": int(len(m))}
    for k in ("new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"):
        a, b = m[f"{k}__raw"].to_numpy(float), m[f"{k}_home"].to_numpy(float)
        ok = np.isfinite(a) & np.isfinite(b)
        out[k] = {"n_both_finite": int(ok.sum()), "share_equal_1e9": float(np.mean(np.abs(a[ok] - b[ok]) <= 1e-9)),
                  "spearman": float(stats.spearmanr(a[ok], b[ok])[0]) if ok.sum() > 10 else None}
    return out


def build_outputs() -> None:
    from tables import load_tables
    spec = json.loads((RES / "frozen_spec.json").read_text())
    pm = spec["exp10_prediction_models"]["B5"]
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    pw = json.loads((RES / "power_frame_n.json").read_text())
    sz = json.loads((RES / "size_dependence.json").read_text())
    T = load_tables()["POOLED"]
    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
    Zb = np.column_stack([(T[c].to_numpy(float) - pm["mu"][c]) / pm["sd"][c] for c in B5])
    dev = (T.body == "DEV").to_numpy() & np.all(np.isfinite(Zb), 1)
    y = T.O2r_m50.to_numpy(float)
    preds, imputed, coefs = {}, {}, {}
    for nm, x in PRED_X.items():
        X = Zb.copy()
        if x is not None:
            v = T[x].to_numpy(float)
            med = float(np.nanmedian(v[dev]))
            imputed[nm] = ~np.isfinite(v)
            v = np.where(np.isfinite(v), v, med)
            X = np.c_[X, v]
        A = np.c_[np.ones(len(T)), X]
        okf = dev & np.all(np.isfinite(A), 1)
        b = np.linalg.lstsq(A[okf], y[okf], rcond=None)[0]
        coefs[nm] = b.tolist()
        preds[nm] = A @ b
    chk = {"note": "OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)", "coef": coefs}
    for body in ("OLDHO", "COH1014", "COH1517"):
        m = (T.body == body).to_numpy()
        ent = {}
        for nm, p in preds.items():
            ok = m & np.isfinite(p)
            ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > 20 else None
        ent["n"] = int(m.sum())
        ent["gain_vs_B5"] = {nm: (ent[nm] - ent["B5"]) if ent[nm] is not None and ent["B5"] is not None else None
                             for nm in PRED_X if nm != "B5"}
        chk[body] = ent
    jdump(chk, RES / "prediction_check.json")
    exs = []
    for i, r in T.iterrows():
        inp = {"concept_id": str(r.concept_id), "name": str(r["name"]), "body": r.body, "t0": int(r.t0),
               "n_home_early": int(r.n_home_early)}
        for c in INPUT_COLS:
            v = r[c]
            inp[c] = None if not np.isfinite(v) else round(float(v), 6)
        e = {"input": json.dumps(inp), "output": f"{r.O2r_m50:.6f}"}
        for nm, p in preds.items():
            e[f"predict_{nm}"] = f"{p[i]:.6f}" if np.isfinite(p[i]) else "nan"
        e["metadata_body"] = r.body
        e["metadata_agroup"] = r.agroup
        e["metadata_O2r_resid"] = None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)
        e["metadata_imputed_variants"] = [nm for nm in imputed if imputed[nm][i]]
        e["metadata_missing_clean_variants"] = [c for c in ("NOVCHURN_exc", "NOVCHURN_rare10", "NOVCHURN_cfg",
                                                            "OPEN_home_clean") if not np.isfinite(r[c])]
        exs.append(e)
    vd = V["verdict"]
    head = {h["variant"]: {b: h[b].get("psp") for b in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED")}
            for h in V["headline_R2_O2r_m50"]}
    meta = {"method_name": "Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled "
                           "variants)",
            "label": "selection data, outcomes previously unsealed: robustness evidence, not confirmation",
            "verdict": vd["verdict"], "DEGREE_ARTEFACT_PERSISTENCE": vd["DEGREE_ARTEFACT_PERSISTENCE"],
            "predictions_P1_P3": {k: v["holds"] for k, v in V["predictions"].items()},
            "P_detail": V["predictions"], "headline_psp_R2_O2r_m50": head,
            "reliability_pooled_SB": {k: v["pooled"]["SB"] for k, v in rel["variants"].items()},
            "outcome_reliability_SB": rel["outcome"]["O2r_m50"]["pooled"]["SB"],
            "thin_sample_share_R2": sz["thin_sample_share"]["POOLED"]["R2"],
            "power_plain_language": pw["plain_language"],
            "concept_key_check": concept_key_check(), "exp12_home_crosscheck": exp12_crosscheck(),
            "n_examples": len(exs), "prediction_models": "OLS on DEV (B5 standardised with EXP10 frozen mu/sd); "
                                                         "NaN variants imputed with the DEV median (flagged)"}
    out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts", "examples": exs}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)
                                                     and not math.isfinite(o) else str(o)))
    logger.info(f"method_out.json: {len(exs)} examples; verdict {vd['verdict']}")


@logger.catch(reraise=True)
def main() -> None:
    setup_logger("method")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-all", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.run_all:
        run_stages(a.force)
    build_outputs()


if __name__ == "__main__":
    main()
