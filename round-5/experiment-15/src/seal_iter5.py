#!/usr/bin/env python3
"""iter-5 STEP 5: freeze the Part A / Part B analysis spec BEFORE any outcome is joined to the new home-partner
features, and seal it together with the feature files.

  python seal_iter5.py freeze   -> results/frozen_spec_iter5.json (+ sha256 of every new .py file)
  python seal_iter5.py seal     -> logs/seal_iter5.log {spec_sha, feature_sha, time, git commit}
check() is imported by score_partA.py / trait_stability.py and refuses to run if the spec or a feature file changed.
Honest note: the outcomes (O2r_m50, O2r_resid) were unsealed several times before (EXP5/7/8/12, Eval3, Exp10); this
seal only fixes THIS analysis's degrees of freedom. Every Part A number is exploratory."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib_iter5"))

from common_iter5 import DATA, E10, LOGS, RES, WS, jdump, sha256_file

SPEC = RES / "frozen_spec_iter5.json"
SEAL = LOGS / "seal_iter5.log"
FEATURES = ["partner_home_components_exp5.parquet", "partner_home_components_cohort.parquet",
            "partner_home_components_retest.parquet"]
CODE = ["partners_home.py", "score_partA.py", "trait_stability.py", "seal_iter5.py", "lib_iter5/common_iter5.py",
        "lib_iter5/ego.py", "lib_iter5/ladder.py", "lib_iter5/partA_stats.py"]


class SealError(RuntimeError):
    pass


def spec() -> dict:
    e10 = json.loads((E10 / "results/frozen_spec.json").read_text())
    hc = e10["open_constants"]["home"]
    return {
        "created": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "EXPLORATORY (selection data): outcomes were unsealed before; this seal fixes only this analysis",
        "seed": 20260929, "N_BOOT": 2000, "N_BOOT_cohort": 2000, "N_PLACEBO": 200,
        "paper_set": "HOME-ONLY (grounded papers whose venue field is a home field), PRE t0-3..t0-1, W1..W3 = t0..t0+2",
        "build": "partners_home.home_partners = EXP8 ego.concept_core preamble (same calls), SELF rule, PMI>0 & count>=2",
        "classes": {
            "type": "METHOD | DOMAIN (| OTHER) from Exp11 results/topic_types.csv",
            "comm": "new | old | unk: backbone community of the partner in the slice of its (first) year vs the "
                    "concept's t0 modal community C0 (W1 count-weighted); unk if C0 undefined",
            "deg": "low | high: key (deg_s0(k), k) below / at-or-above the degree-weighted median key of the NOV null "
                   "pool (non-PRE, non-SELF topics with background mass); P_null(low) = 0.5",
            "carrier": "mixed | pure: some home paper of the partner's (first) year containing k also carries a non-SELF "
                       "topic whose field is outside the concept's home fields"},
        "components": {
            "NOV_res": "sum_X nov_X, nov_X = (1/M) sum_{k in NEW&X} (1[comm_k != C0] - E); axes type, deg, carrier "
                       "(community axis NOT applied: NOV_res IS the new-community share -> tautological)",
            "novnull_X": "NOV_X - E_X with E_X the class-specific degree-weighted null (carrier: E_X = E)",
            "new_edge_rate": "sum_X ner_X, ner_X = (|NEW & X| / 3) / (n1 + 1); all four axes",
            "churn": "1 - edge_persistence = sum_X (chd_X + cha_X): dropped / added partner shares of the union, "
                     "averaged over the defined transitions W1->W2, W2->W3",
            "NOVCHURN_home": "mean(z(NOV_res), -z(edge_persistence)) with the Exp10 EXP5-frozen HOME OPEN constants "
                             "(winsorised at lo/hi, then (v-mu)/sd); defined iff both finite and n_home_early >= 10",
            "bridging_share_home": "share of early home papers that introduce >= 1 new-community new partner in its "
                                   "first year"},
        "novchurn_constants": {"source": "Exp10 results/frozen_spec.json open_constants.home",
                               "NOV_res": hc["NOV_res"], "edge_persistence": hc["edge_persistence"]},
        "open_home_constants": {"source": "Exp10 results/frozen_spec.json open_constants.home", "min_home_papers": 10,
                                "min_components": 4},
        "bodies": {"DEV": "EXP5 split DEV (selection, disclosed)", "OLD_HELDOUT": "EXP5 split HELDOUT_* (+ per group "
                   "PHYS/LIFEENV/SOC/MATHDEC, DL on Fisher z with I2)", "COHORT_2010_14": "EXP5 split COHORT",
                   "POOLED_EXP5": "DEV + OLD_HELDOUT + COHORT_2010_14 with body and group dummies (the powered body)",
                   "COHORT_2015_17": "Exp10 analysis_cohort at rungs R0 and R3 (Exp10 ladder.rung_design)"},
        "outcomes": {"primary": "O2r_m50", "secondary": ["O2r_resid", "O5_WW (EXP8, recognition; secondary only)"]},
        "baseline": "B5 (logvol, growth_c, offhome_share, entropy, reach) ranks + t0 dummies (+ group and body dummies "
                    "when pooled); 2015-17: Exp10 rungs R0 / R3",
        "estimator": "partial Spearman (EXP8 rq1stats.psp_point); concept bootstrap, the SAME resample indices for every "
                     "component within a body (paired differences valid); percentile 95% CIs",
        "shapley": {"games": {
            "type": "players METHOD, DOMAIN; NOV and churn parts of the player's class",
            "deg": "players low, high", "carrier": "players mixed, pure",
            "direction": "players NOV (all new-partner novelty), DROP (dropped-partner churn), ADD (added-partner churn)",
            "type_x_comm_ner": "4 players METHOD-new, METHOD-old, DOMAIN-new, DOMAIN-old on psp(new_edge_rate)",
            "type_x_comm_churn": "the same 4 players on psp(churn)"},
            "value": "v(S) = psp of the target rebuilt with the parts of players not in S replaced by their body mean; "
                     "v(empty) = 0 (constant score); exact enumeration of all orderings; efficiency checked (1e-9)",
            "fair_share": "the class's share of the relevant partners (new partners for NOV/ner, churn events for churn)",
            "F5": "if |v(full)| < 0.03 report absolute phi with CIs, not shares"},
        "holm_family": {"body": "POOLED_EXP5", "outcome": "O2r_m50", "contrasts": [
            "C1 METHOD-DOMAIN: psp(novnull_type_METHOD) - psp(novnull_type_DOMAIN)",
            "C2 comm_new-comm_old: psp(ner_comm_new) - psp(ner_comm_old)",
            "C3 lowdeg-highdeg: psp(nov_deg_low) - psp(nov_deg_high)",
            "C4 mixed-pure carrier: psp(ner_carrier_mixed) - psp(ner_carrier_pure)",
            "C5 dropped-added: psp(chd_all) - psp(cha_all)"],
            "p": "two-sided paired-bootstrap p (2 x min tail share), Holm-adjusted over the 5"},
        "predictions": {
            "P-A1": "METHOD share of the NOVCHURN Shapley (type game) > METHOD share of new partners",
            "P-A2": "new-community new partners carry more new_edge_rate signal than same-community ones (C2 > 0)",
            "P-A3": "low-degree partners carry more NOV_res signal than high-degree ones (C3 > 0)",
            "P-A4": "mixed-carrier > pure-home (C4 > 0)",
            "P-A5": "dropped-partner churn carries more signal than added-partner churn (|psp| of chd_all > cha_all; "
                    "C5 on the churn scale where churn predicts spread positively)",
            "P-B1": "TRAIT: ICC(OPEN_home yearly) >= 0.40 AND early-later Spearman >= 0.40 on DEV AND OLD_HELDOUT",
            "P-B2": "same for NOVCHURN (reported separately)"},
        "part_B": {
            "yearly": "Exp11 yearly_features (HOME, 1-year windows) rows t0..h_end with deg >= 2; OPEN_home_y = "
                      "panel_m.open_home with Exp11 frozen yearly constants; NOVCHURN_y = mean(z nov_res, -z persistence)",
            "ICC": "one-way random-effects ICC(1) on x residualised on year and age dummies (ANOVA estimator, k0 = (N - sum n_i^2 / N) / (g - 1) "
                   "for unbalanced groups), concept bootstrap 500; MixedLM REML point as a cross-check; size-adjusted version "
                   "residualised also on log1p_deg, log1p_home_works, log1p_all_works",
            "test_retest": "Spearman(mean x over t0..t0+2, mean x over t0+3..t0+5), >= 2 defined years each; partial "
                           "given early log volume and mean log degree; Spearman-Brown odd/even reliability; "
                           "disattenuated", "positive_control": "ICC of log1p_home_works > 0.6",
            "static": "same HOME build on t0+3..t0+5 (PRE t0..t0+2) from Exp11 frame_matches_long; Spearman early vs "
                      "later of static OPEN_home and NOVCHURN, raw and size-partial"},
        "thresholds": {"ICC_floor": 0.40, "retest_floor": 0.40, "F5_small_v": 0.03},
    }


def freeze() -> str:
    s = spec()
    s["code_sha256"] = {c: sha256_file(WS / c) for c in CODE if (WS / c).exists()}
    jdump(s, SPEC)
    h = sha256_file(SPEC)
    print("spec sha", h)
    return h


def seal() -> dict:
    git = subprocess.run(["git", "rev-parse", "HEAD"], cwd=WS, capture_output=True, text=True).stdout.strip()
    rec = {"spec_sha": sha256_file(SPEC), "feature_sha": {f: sha256_file(DATA / f) for f in FEATURES},
           "time": time.strftime("%Y-%m-%d %H:%M:%S"), "git_commit": git or None}
    SEAL.write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))
    return rec


def check() -> dict:
    if not SPEC.exists() or not SEAL.exists():
        raise SealError("spec or seal missing: run seal_iter5.py freeze && seal before scoring")
    rec = json.loads(SEAL.read_text())
    if sha256_file(SPEC) != rec["spec_sha"]:
        raise SealError("frozen_spec_iter5.json changed after the seal")
    for f, h in rec["feature_sha"].items():
        if sha256_file(DATA / f) != h:
            raise SealError(f"{f} changed after the seal")
    return rec


if __name__ == "__main__":
    {"freeze": freeze, "seal": seal, "check": lambda: print(check())}[sys.argv[1]]()
