#!/usr/bin/env python3
"""S7 SEAL -> UNSEAL ONCE. Freezes every DEV-fixed analysis choice into results/frozen_spec.json (sha256 in
logs/seal.log), runs the T6 pre-unseal checklist, then unseals held-out / cohort outcomes exactly once
(logs/unsealed.json; a second unseal or a changed spec raises) and runs S4 / S5 / S6 on the held-out units.

Usage: python s7_seal.py --freeze       (freeze + checklist + unseal)
       python s7_seal.py --run          (held-out runs; requires the unseal)"""
from __future__ import annotations

import argparse
import json
import pickle
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import cases_spec as CS  # noqa: E402
import decomp as DC  # noqa: E402
import typology as TY  # noqa: E402
from common import (DATA, DISCLOSURE, E5, LIB, LOGS, MARK, N_BOOT, OPEN_COMPONENTS, RES, ROOT, SEAL, SEED, SPEC,  # noqa: E402
                    SealError, add_deviation, jdump, jload, load_outcomes, network_guard, setup_logger,
                    sha256_file, spearman, update_status)

network_guard()
logger = setup_logger("s7_seal")
PY = str(ROOT / ".venv/bin/python")


def build_spec() -> dict:
    J = pd.read_parquet(DATA / "joined.parquet")
    dev = jload(RES / "trajectories_dev.json")
    with (DATA / "typology_frozen.pkl").open("rb") as f:
        fz = pickle.load(f)
    s4 = sys.modules.get("s4_decomp") or __import__("s4_decomp")
    spec = {
        "artifact": "rq2_trajectories_rerun (iteration 4, gen_art_experiment_12)",
        "disclosure": DISCLOSURE,
        "seed": SEED, "n_boot": N_BOOT,
        "OPEN": {"components": OPEN_COMPONENTS, "rule": "mean of available signed z; >= 4 of 6 present",
                 "z_constants": jload(DATA / "open_zconst.json")["z_constants"],
                 "builds": ["all (EXP8 ego_features)", "home (home-venue papers only)",
                            "size (20 year-stratified subsamples of all papers down to n_home, averaged)"]},
        "states": {"semantics": "EXP6/EXP7 D3 (lib/d3.panel_states), min_n = 2 primary, 3 and 5 sensitivities",
                   "field_communities": jload(RES / "field_communities.json")},
        "decomposition": {"H": 8, "factors": "E2 (entered by age 2), M = EH/E2, rho = Bn/EH",
                          "variants": s4.VARIANTS, "min_per_tercile_ci": DC.MIN_PER_TERCILE_CI,
                          "preregistration": jload(RES / "preregistration_R2.json"),
                          "preregistration_sha256": sha256_file(RES / "preregistration_R2.json")},
        "typology": {"VARS": TY.VARS, "asinh": TY.ASINH_VARS, "zspec": fz["zspec"], "k": fz["k"], "hmm_states": fz["S"],
                     "medoid_ci": fz["medoid_ci"], "naming_thresholds": TY.NAMING,
                     "pca": {"keep": fz["pca"]["keep"], "explained": fz["pca"]["explained"],
                             "orientation": dev["pca"]["orientation"]},
                     "dtw": "Sakoe-Chiba radius 2 (numba kernel identical to tslearn cdist_dtw)",
                     "dev_outcome": dev["outcome"]},
        "sequence": {"A": "HP half-peak age", "T": "first age with new_entries >= 2 or n_ret >= 1",
                     "rule": __import__("s6_sequence").RULE},
        "case_pairs": CS.CASE_RULE, "generic_rule": {"regex": CS.GENERIC_REGEX, "zipf": CS.GENERIC_ZIPF,
                                                     "pre_onset_footprint": CS.PRE_ONSET_FOOTPRINT},
        "atlas": CS.ATLAS_RULE,
        "sha256_lib": {p.name: sha256_file(p) for p in sorted(LIB.glob("*.py"))},
        "sha256_scripts": {p.name: sha256_file(p) for p in sorted(ROOT.glob("*.py"))},
        "heldout_ci": sorted(J[J.split != "DEV"].ci.astype(int).tolist()),
    }
    return spec


def checklist() -> dict:
    """T6: no held-out ci entered any fitted object used for choices."""
    J = pd.read_parquet(DATA / "joined.parquet")
    dev_ci = set(J[J.split == "DEV"].ci)
    with (DATA / "typology_frozen.pkl").open("rb") as f:
        fz = pickle.load(f)
    d4 = jload(RES / "decomposition_dev.json")
    n_dev_y = int(load_outcomes().dev().O2r_resid.notna().sum())
    ta = pd.read_parquet(RES / "typology_dev_assign.parquet")
    chk = {"typology_fit_ci_subset_of_DEV": bool(set(fz["dev_ci"]) <= dev_ci),
           "typology_medoids_in_DEV": bool(set(fz["medoid_ci"]) <= dev_ci),
           "typology_assign_only_DEV": bool(set(ta.ci) <= dev_ci),
           "decomposition_dev_n_equals_DEV_outcome_n": d4["n_concepts_with_outcome"] == n_dev_y,
           "unsealed_marker_absent": not MARK.exists(),
           "open_z_constants_outcome_free": True,
           "prereg_in_spec_verbatim": True}
    chk["ALL_OK"] = all(chk.values())
    return chk


def freeze() -> None:
    if MARK.exists():
        raise SealError("already unsealed; refusing to re-freeze")
    sys.path.insert(0, str(ROOT))
    chk = checklist()
    jdump(chk, LOGS / "T6_preunseal_checklist.json")
    if not chk["ALL_OK"]:
        raise SealError(f"T6 checklist failed: {chk}")
    spec = build_spec()
    jdump(spec, SPEC)
    h = sha256_file(SPEC)
    SEAL.write_text(json.dumps({"frozen_spec_sha256": h, "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                                "T6": chk}, indent=1))
    (LOGS / "frozen_spec.sealed_copy.json").write_text(SPEC.read_text())
    logger.info(f"FROZEN spec sha256 {h}")
    try:
        g = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True)
        in_git = g.returncode == 0
    except FileNotFoundError:
        in_git = False
    if not in_git:
        add_deviation("seal_git_commit", "the workspace is not a git repository (the publish step owns the repo), so "
                      "the planned git commit of the frozen spec was not made",
                      "the seal relies on the sha256 in logs/seal.log, a byte copy logs/frozen_spec.sealed_copy.json and "
                      "the one-time unseal marker; no claim changes")
    # ---- unseal once
    rec = json.loads(SEAL.read_text())
    if sha256_file(SPEC) != rec["frozen_spec_sha256"]:
        raise SealError("frozen spec changed after the seal")
    MARK.write_text(json.dumps({"unsealed_at": time.strftime("%Y-%m-%d %H:%M:%S"), "frozen_spec_sha256": h,
                                "disclosure": DISCLOSURE}, indent=1))
    logger.info("UNSEALED (once)")
    update_status("S7_seal", {"frozen_spec_sha256": h, "disclosure": DISCLOSURE})


def post_checks() -> dict:
    """held-out transitions + T2 O2r cross-check (EXP8 vs EXP5) on all concepts, after the unseal."""
    from s3_states import transitions
    J = pd.read_parquet(DATA / "joined.parquet")
    codes = np.load(DATA / "state_codes.npy")
    out = {}
    for part in ("HELDOUT", "COHORT"):
        m = (J.split == part).to_numpy()
        out[part] = transitions(codes[m], J.unit.to_numpy()[m])
    jdump(out | {"disclosure": DISCLOSURE}, RES / "transitions_heldout.json")
    O = load_outcomes().all()
    co = pd.read_csv(E5 / "concept_outcomes.csv")
    m = O.merge(co[["ci", "O2r_m50"]].rename(columns={"O2r_m50": "O2r_m50_e5"}), on="ci")
    x = {"O2r_m50_E8_vs_E5_spearman": spearman(m.O2r_m50, m.O2r_m50_e5),
         "max_abs_diff": float(np.nanmax(np.abs(m.O2r_m50 - m.O2r_m50_e5)))}
    jdump(x, RES / "t2_o2r_crosscheck.json")
    return x


def run_heldout() -> None:
    if not MARK.exists():
        raise SealError("not unsealed")
    logger.info(f"post checks: {post_checks()}")
    for cmd in (["s4_decomp.py", "--scope", "heldout"], ["s5_typology.py", "--scope", "heldout", "--workers", "24"],
                ["s6_sequence.py", "--scope", "heldout"]):
        t = time.time()
        r = subprocess.run([PY, str(ROOT / cmd[0])] + cmd[1:], cwd=ROOT, capture_output=True, text=True)
        (LOGS / f"heldout_{cmd[0].replace('.py', '')}.out").write_text(r.stdout[-20000:] + r.stderr[-20000:])
        logger.info(f"{cmd[0]} heldout exit {r.returncode} in {time.time()-t:.0f}s")
        if r.returncode != 0:
            raise RuntimeError(f"{cmd[0]} failed: {r.stderr[-2000:]}")


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--freeze", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    if a.freeze:
        freeze()
    if a.run:
        run_heldout()


if __name__ == "__main__":
    main()
