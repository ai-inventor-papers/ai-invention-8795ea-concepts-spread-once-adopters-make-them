"""S0: write results/frozen_spec.json (definitions, tests, predictions, verdict rules, code hashes) and append
sha256(prereg.md + frozen_spec.json) with a timestamp to logs/seal.log. Runs BEFORE any model is fitted."""
from __future__ import annotations

import hashlib
import subprocess
import time

from common import (B5, BODIES_EXP5, BODY_COHORT, DEPTH, EMB_TOPN, GROUP5, GROUPS5, LIB, LOGS, MIN_PAPERS,
                    MIN_TOPICS, N_BOOT_PANEL, N_BOOT_STATIC, REACH, RES, ROOT, SEED, SOC_CAP, SOC_LOOKBACK,
                    SOC_MAX_AUTHORS_PER_PAPER, jdump, sha256_file)

SPEC = {
    "title": "Cheng reach-vs-depth reversal on the selection bodies",
    "label": "selection data, not confirmation",
    "seed": SEED,
    "definitions": {
        "paper_sets": {"HOME": "grounded papers with vfield in the frozen home set",
                       "ALL": "every grounded paper",
                       "grounding": "TAG (legacy concept tag score >= 0.3; EXP5 frame = Exp11 Pass M rows; "
                                    "cohort = EXP10 passC_early tagstate == 1)"},
        "self_topics": "Exp11/EXP8 ego.self_topics on ALL papers t0..t0+2 (lemma rule + share >= 0.20)",
        "v_t": "v_t[k] = # year-t papers of the concept in the paper set tagged with topic k (k not SELF)",
        "CONS": f"cosine(v_(t-1), v_t); defined iff both years >= {MIN_PAPERS} papers with >= 1 topic and >= "
                f"{MIN_TOPICS} non-self topics; else NaN",
        "CONS_r": "Cheng-verbatim sensitivity: cosine restricted to the t-1 neighbour support (0 if empty in t)",
        "EMB": f"ANALOGUE: co-usage-weighted (v_k v_l) mean positive backbone PMI over pairs of the top-{EMB_TOPN} "
               "year-t neighbours on EXP3 slice s(t); missing edge = 0; defined iff >= 3 papers, >= 2 topics",
        "EMB_cos": "EXPLORATORY: mean pairwise cosine of neighbours' backbone PMI rows (second-order similarity)",
        "SOC": f"density of prior-tie graph among year-t authors (papers <= {SOC_MAX_AUTHORS_PER_PAPER} authors; "
               f"cap {SOC_CAP} nodes, seeded by (ci, year)); edge iff co-authored any concept paper in "
               f"t-{SOC_LOOKBACK}..t-1; NaN if < 3 authors",
        "V": "TAG-grounded yearly count (tagstate == 1), all fields, EXP5 scan/agg_counts; checked vs Exp11 "
             "counts_m (sum over vfield); F3 fallback to counts_m if < 99% of checked cells match exactly",
        "V_cohort_t0p3": "sum of EXP10 sealed parts n at year t0+3 with tagstate == 1 (EXP10 s3 decision TAG); "
                         "read-only, seal2.unseal() not called",
        "static_early": "X_early = mean of defined X(t0+1), X(t0+2)",
    },
    "bodies": {"EXP5": BODIES_EXP5, "cohort": BODY_COHORT, "PRIMARY": "EXP5 pooled (DEV+OLD_HELDOUT+"
               "COHORT_2010_14, body dummies)", "REPLICATION": BODY_COHORT},
    "groups": {"map": GROUP5, "pooled": GROUPS5, "report_only": ["MATHDEC"]},
    "B5": B5, "depth_outcomes": DEPTH, "reach_outcomes": REACH, "transience_note": "O3 = transience (1 = spike "
    "then collapse); its predicted sign is <= 0 for a depth-supporting trait",
    "tests": {
        "A": {"rows": "EXP5 concept-years t0+1 <= t <= min(t0+10, 2021) with finite CONS_home(t)",
              "standardise": "z over the pooled panel rows of each model",
              "A1": "fepois V(t+1) ~ zCONS + zEMB + zSOC | age + year, CRV1 by ci (Cheng spec)",
              "A1_NB": "statsmodels NegativeBinomial with age + year dummies",
              "A2": "A1 + log1p V(t)", "A3": "A2 | ci + year",
              "variants": ["HOME", "ALL", "SOC-complete joint", "CONS-only"],
              "ratio": f"b_A2/b_A1 on CONS, {N_BOOT_PANEL}-draw concept-cluster bootstrap, same draws",
              "per_body_group": "per body and per group; DL across groups"},
        "B": {"raw": "Spearman(CONS_early_home, V(t0+3))", "size": "psp(CONS_early_home, V(t0+3) | log V(t0+2))",
              "depth": "psp with O1c, O1b, O3 | B5 + onset-year dummies (+ group, body dummies when pooled)",
              "reach": "psp with O2r_m50, O2r_resid | same", "bootstrap": N_BOOT_STATIC,
              "paired_diff": "psp(O1c) - psp(O2r_m50), same draws, common complete-case set",
              "DL": "5 groups, I2, sign count", "cohort_rungs": ["R2", "R3"],
              "also": ["EMB_early", "SOC_early", "CONS_early_all", "CONS_r_early", "EMB_cos_early"]},
        "C": {"C1": "fepois entries(t+1) ~ zCONS_home(t) + log1p_home + log1p_all + log1p_deg + log_at_risk | ci + "
                    "year, CRV1; Exp11 estimation sample (at_risk_next > 0, deg >= 2)",
              "C2": "feols dHomeShare(t+1) ~ same; home share = home-field grounded count / all grounded count "
                    "(counts_m)", "bootstrap": N_BOOT_PANEL},
        "D": {"model": "OLS on ranks: rank O ~ rank CONS_early + rank logvol_early + product + rank B5 + t0 "
                       "dummies (+ group/body dummies); O in {O3, O2r_m50}",
              "tercile": "psp of CONS_early by early-size (logvol) tercile",
              "palla_prediction": "interaction on O3 > 0"},
        "E": {"model": "paired bootstrap psp(CONS_early_all) - psp(CONS_early_home) on O2r_m50 and O1c"},
    },
    "predictions": {
        "P1": "raw Spearman(CONS_early_home, V(t0+3)) > 0 and A1 b_CONS > 0 on HOME",
        "P2": "RATIO A2/A1 < 0.5",
        "P3": "psp(CONS_early_home, O2r_m50 | B5) < 0",
        "P4": "psp(CONS_early_home, O3 | B5) <= 0",
        "P5": "psp(O1c) - psp(O2r_m50) > 0",
        "P6": "C1 b < 0",
    },
    "holm_family": ["P1-A1", "P2", "P3", "P4", "P5"],
    "holm_note": "PRIMARY body, one-sided in the predicted direction",
    "verdict_rules": {
        "REVERSAL CONFIRMED (on selection data)": "P1 raw rho > 0 with CI > 0 AND P3 psp < 0 with CI < 0 (PRIMARY)",
        "REVERSAL REPLICATED": "same on COHORT_2015_17 (CI < 0 not required if n < 600; report MDE)",
        "SIZE-DOMINATED": "A2/A1 ratio bootstrap CI upper bound < 0.5",
        "DEPTH-REACH SPLIT": "P5 CI > 0",
        "NULL-REVERSAL": "P3 CI includes 0",
        "other": "EXPLORATORY; no post-hoc subgroup claims",
    },
    "drop_order": ["A1-NB", "EMB", "SOC", "Palla terciles", "ALL build for test A"],
}


def run(logger) -> dict:
    spec = dict(SPEC)
    spec["created"] = time.strftime("%Y-%m-%d %H:%M:%S")
    spec["code_sha256"] = {p.name: sha256_file(p) for p in sorted(LIB.glob("*.py"))}
    spec["prereg_sha256"] = sha256_file(ROOT / "prereg.md")
    out = RES / "frozen_spec.json"
    if out.exists():
        logger.warning("frozen_spec.json already exists; keeping the sealed version (no overwrite)")
        return {"skipped": True}
    jdump(spec, out)
    h = hashlib.sha256((ROOT / "prereg.md").read_bytes() + out.read_bytes()).hexdigest()
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} sha256(prereg.md + frozen_spec.json) = {h}\n"
    with (LOGS / "seal.log").open("a") as f:
        f.write(line)
    logger.info(f"sealed: {line.strip()}")
    try:
        subprocess.run(["git", "-C", str(ROOT), "add", "prereg.md", "results/frozen_spec.json", "logs/seal.log",
                        "lib", "pyproject.toml"], check=True, capture_output=True)
        subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m",
                        "S0 seal: prereg + frozen spec\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"],
                       check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.warning(f"git commit failed: {e}")
    return {"sha": h}
