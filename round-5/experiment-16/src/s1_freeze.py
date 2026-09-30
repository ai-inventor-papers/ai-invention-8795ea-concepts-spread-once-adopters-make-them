#!/usr/bin/env python3
"""S1 FREEZE (before any outcome is joined): variant definitions, draw counts, seeds, constants rule, predictions
P1-P3 and verdict rules -> results/frozen_spec.json, sha256 -> logs/seal.log (entry S1_freeze).
The z constants of the clean composites are appended later by s4_composites.py (entry S1b_constants), still before
any outcome join. NOTE: the outcomes of every body were already unsealed by EXP5/EXP8/EXP10 -- this is a
pre-analysis commitment on selection data, not a blind."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import DATA_IN, RES, jdump, setup_logger, sha256_file
from s2_cfg import CFG_FULL
from seal import LOG, seal_file

logger = setup_logger("s1_freeze")


def main() -> None:
    exp10 = json.loads((DATA_IN.parent / "results/frozen_spec.json").read_text())
    spec = {
        "status": "pre-analysis commitment on SELECTION data; outcomes previously unsealed by EXP5/EXP8/EXP10",
        "bodies": {
            "DEV": "EXP5 frame split DEV (t0 2003-09; CS/Eng/BGM/Med home groups)",
            "OLDHO": "EXP5 frame split HELDOUT (t0 2003-09; PHYS/LIFEENV/SOC/MATHDEC)",
            "COH1014": "EXP5 frame split COHORT (t0 2010-14)",
            "COH1517": "EXP10 fresh cohort (t0 2015-17), analysis_cohort.parquet",
            "POOLED": "all four stacked; body dummies added to the categorical block of every rung; year dummies span "
                      "t0 2003-2017"},
        "inclusion": "HOME build; n_home_early (home papers t0..t0+2, EXP10 count) >= 10 for every variant and "
                     "analysis (the OPEN_home rule); drop counts per body reported",
        "engine": {"fast6": "lib/fast6.py, validated == ego.concept_core (SELF override) to <= 1e-12 (U1)",
                   "SELF": "computed once on the FULL home build (ego.self_topics) and held FIXED in every resampled "
                           "variant (definitional exclusion of the concept's own name topics)"},
        "draws": CFG_FULL,
        "seeds": {"V1": "numpy default_rng([7000000, sk, n])", "V2": "default_rng([8000000, sk])",
                  "V4_splits": "default_rng([9000000, sk])", "V4_V2_halves": "default_rng([9100000, sk])",
                  "V4_V1_halves": "default_rng([9200000, sk])",
                  "sk": "ci for EXP5-frame concepts, 100000 + ci for COH1517 (ci spaces overlap)",
                  "V3a_rewire": "random.seed / igraph RNG = 20260930 + 1000 s + d", "V3b": "default_rng([20260931, sk])",
                  "V3c_curveball": "numba seed 20260932 + year", "bootstrap": 20260930,
                  "note": "seed streams via SeedSequence lists replace the plan's additive seeds (7e6 + 100 ci + n "
                          "etc.) because COH1517 and EXP5 ci values overlap; declared pre-run"},
        "variants": {
            "RAW": "six EXP10 components on the full home build: new_edge_rate, n_comm_W3, participation, NOV_res, "
                   "ego_density_W3, edge_persistence",
            "V1_rare{n}": "n in (5, 10, 20): concepts with >= n home papers in EACH of W1, W2, W3; each draw keeps "
                          "exactly n papers per W-year and min(|PRE|, 3n) PRE papers (without replacement); "
                          "D_RARE draws; nanmean over draws, NaN unless >= half finite. n = 10 primary.",
            "V1_contingency_F6": "if fewer than 150 COH1517 concepts have finite NOVCHURN_rare10 and O2r_m50, n = 5 is "
                                 "primary for COH1517 (NOVCHURN_rare_primary); if < 100 even at n = 5 V1 is reported "
                                 "not estimable on COH1517 and P1 is decided on V2 alone",
            "V2": "D_PERM permutations of the W1..W3 year labels among the concept's W home papers (yearly counts "
                  "kept, PRE fixed); per metric null mean, null sd, excess = obs - null mean (*_exc), zperm = "
                  "excess / null sd (NaN if sd == 0); NaN unless >= half the draws finite",
            "V2b_EP_chao": "Chao et al. 2005 abundance-based Jaccard (bias-corrected f2 = 0 form, U, V capped at 1) on "
                           "the non-SELF topic count vectors of W1-W2 and W2-W3, mean of the finite pairs; "
                           "exploratory sensitivity",
            "V3a_z_dens_cfg": "full topic backbone of slice s rewired 200 times (igraph Graph.rewire(n = 10 m, "
                              "mode='simple'), degree sequence asserted); e_null = edges of the rewired graph inside "
                              "S = raw NB_W3 (|S| >= 2); z = (e_obs - mean) / sd; also z_dens_cfg_W1 on NB_W1 / "
                              "slice(t0)",
            "V3b_z_dens_k": "200 random sets of size |S| drawn without replacement with probability proportional to "
                            "bg counts in year t0+2 among topics with bg > 0 and not SELF; edges counted in the REAL "
                            "backbone; z = (e_obs - mean) / sd",
            "V3c_z_pers_cfg": "curveball randomisation (Strona 2014) of the bipartite (concept-window x partner topic) "
                              "incidence of raw non-SELF NB sets within each calendar year, pooled over all bodies; "
                              "burn-in 5 x n_rows trades, 200 samples each n_rows trades apart; null persistence = "
                              "mean(J(W1, W2), J(W2, W3)) of the concept's rows in the same sample index; z = (obs - "
                              "mean) / sd; excess_pers_cfg = obs - mean. Null expected Jaccard is near 0, so z is "
                              "mostly obs / sd (degree normalisation, not a coherence test)",
            "V4": "split-half reliability: S_RAW random within-window half splits for RAW; the first S_CLEAN of them "
                  "for clean variants (V2 with D_PERM_HALF perms per half; V1 n = 5 with D_RARE_HALF draws per half, "
                  "concepts with >= 10 papers per W-year; V3a/V3b with 50 null draws per half; V3c on halves via the "
                  "k-matched Monte Carlo approximation: row sizes from the half, column weights = that year's topic "
                  "neighbour popularity, 50 draws). r_s = Spearman(v_A, v_B) across concepts; r = tanh(mean atanh "
                  "r_s); SB = 2r / (1 + r); per body, pooled, per n_home_early bin (10-19, 20-49, 50-99, >= 100); "
                  "200-resample concept bootstrap CI for pooled SB (split-averaged half values)",
            "outcome_reliability": "O2r_m50: papers of the outcome window (t0+6..t0+8, field counts) split by "
                                   "multivariate hypergeometric thinning into halves (100 splits), exact "
                                   "hypergeometric rarefied richness at m = 25 per half (concepts with >= 50 outcome "
                                   "papers); SB; flagged 'conservative, m = 25 halves'. rel_y = 1 (flagged) if the "
                                   "counts are not cached"},
        "composites": {
            "z_rule_new_constants": "winsorise at 0.5 / 99.5 percentiles, mean / sd of the winsorised values over ALL "
                                    "EXP5-frame concepts (n_home_early >= 10) with the variant finite (== "
                                    "ladder.fit_open_constants); written to this spec as S1b before outcomes join",
            "raw_constants": "EXP10 frozen open_constants.home for raw components",
            "NOVCHURN_raw": "mean(z NOV_res__home, -z edge_persistence__home), EXP10 constants, both finite",
            "NOVCHURN_rare10": "mean(z NOV_res_rare10, -z edge_persistence_rare10), new constants, both finite "
                               "(also rare5 / rare20)",
            "NOVCHURN_exc": "mean(z NOV_res_exc, -z edge_persistence_exc), new constants, both finite",
            "NOVCHURN_zperm": "mean(z NOV_res_zperm, -z edge_persistence_zperm) (sensitivity)",
            "NOVCHURN_cfg": "mean(z NOV_res (EXP10 const), -z z_pers_cfg (new)), both finite",
            "NOVCHURN_chao": "mean(z NOV_res (EXP10 const), -z EP_chao (new)), both finite",
            "OPEN_home_clean": "six-component mean, ego_density_W3 -> z_dens_cfg (sign -1), edge_persistence -> "
                               "z_pers_cfg (sign -1), others raw with EXP10 constants; >= 4 finite; n_home_early >= 10",
            "OPEN_home_exc": "same with ego_density_W3_exc and edge_persistence_exc (sign -1)"},
        "outcomes": {"primary": "O2r_m50", "secondary": "O2r_resid"},
        "rungs": ["R0", "R2", "R3"], "rung_definition": "EXP10 lib/ladder.rung_design (+ body dummies for POOLED)",
        "groups": exp10["groups"], "bootstrap": {"B": 2000, "seed": 20260930, "unit": "concept"},
        "exp10_open_constants_home": exp10["open_constants"]["home"],
        "exp10_prediction_models": exp10["prediction_models"],
        "direction_convention": "psp is reported on the variant as stored; persistence/density variants are "
                                "expected negative, NOVCHURN / OPEN positive; retention ratio = psp_clean / psp_raw on "
                                "the SAME concepts (both finite), per bootstrap resample with shared indices",
        "predictions": {
            "P1": "psp(NOVCHURN_exc | R2, O2r_m50) >= 0.70 x psp(NOVCHURN_raw) on COH1517 AND on OLDHO (same-sample "
                  "ratio; point ratio decides, paired-bootstrap percentile CI reported)",
            "P2": "z_pers_cfg keeps a negative psp with 95% CI < 0 on POOLED (R2, body dummies)",
            "P3": "|Spearman(NOVCHURN_exc, log n_home_early)| < 0.20 on POOLED"},
        "verdict_rules": {
            "CHURN_NOT_THIN": "P1 and P3 hold AND V1 (NOVCHURN_rare10, or the F6 primary n) keeps >= 50% of the raw "
                              "psp (same-sample ratio) in COH1517 or OLDHO",
            "CHURN_THIN": "raw NOVCHURN CI excludes 0 (in the body considered) but NOVCHURN_exc AND NOVCHURN_rare10 "
                          "keep < 30% of it in BOTH COH1517 and OLDHO",
            "PARTLY_THIN": "otherwise",
            "DEGREE_ARTEFACT_PERSISTENCE": "flag added if P2 fails while raw edge_persistence has CI < 0 on POOLED"},
        "holm": "Holm over the P1-P3 family (one-sided bootstrap p), reported only",
        "power": {"targets": "T1 disattenuated pooled R3/R5, T2 COH1517 raw, T3 half pooled raw", "n": [800, 1500, 2500],
                  "draws": 1000, "scenarios": "S_A EXP5 n-mix; S_B pessimistic (n-bin weights shifted one bin down)"},
    }
    p = RES / "frozen_spec.json"
    jdump(spec, p)
    ent = seal_file("S1_freeze", p)
    logger.info(f"sealed frozen_spec.json sha256 {ent['sha256']} -> {LOG}")


if __name__ == "__main__":
    main()
