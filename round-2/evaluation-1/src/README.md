# Stress-testing the gateway-field retention lead

An iteration-1 experiment (art_33_KKk_G8Gw5, "exp4") found that an adopting field's eigenvector centrality on a
26-field 1998-2002 relatedness backbone (`gateway_j`) added **+0.103 AUC** to predicting whether the field still publishes
on a concept 6-8 years later (retention `R`). That result rested on 80 episodes and 28 concepts, with a fixed-prediction
CI. This artifact asks whether the lead survives outside that file. It makes **zero API calls**: it reads only
iteration-1 outputs, read-only.

## Verdict (pre-registered ladder, `prereg/verdict_ladder.json`): **FAILS**

The new-episodes-only panel (282 episodes that are not among exp4's 80) gives delta-AUC over M2 = **-0.0006**,
95% refit CI [-0.021, 0.017]. The lead does not replicate.

| dataset (rows / concepts) | draws | dAUC gateway over M0 | dAUC over **M2** [95% refit CI] | groups + |
|---|---|---|---|---|
| exp4 (80 / 28), venue labels | 2000* | **+0.103** [0.025, 0.197] | +0.037 [-0.018, 0.130] | 4/4 |
| exp1 (367 / 46), s2-fos crosswalk | 500 | +0.001 | +0.001 [-0.021, 0.009] | 2/4 |
| exp1 crosswalk-clean (238) | 500* | -0.003 | -0.005 [-0.032, 0.021] | 1/4 |
| exp3 (129 / 44), snapshot venue labels | 500 | -0.027 | -0.006 [-0.052, 0.070] | 1/4 |
| **union** (362 / 54), de-duplicated | 2000 | +0.002 [-0.019, 0.024] | **+0.001 [-0.012, 0.012]** | 1/4 |
| **new episodes only** (282 / 53) | 2000 | +0.000 | **-0.001 [-0.021, 0.017]** | 3/4 |
| union, R agrees across files (328) | 500 | +0.002 | +0.000 [-0.019, 0.008] | 1/4 |

M0 is the dataset's own field baseline (early log count, growth, share). M1 adds B5; M2 adds log field size,
relatedness to home (`phi_home_j`) and relatedness density. CIs come from a concept-clustered **refit** bootstrap
(every draw refits the full LOGO models). *Stratified-by-group resampling was used because more than 5% of plain draws
left a test group with one class. The DerSimonian-Laird pooled M2 delta over exp4/exp1/exp3 is +0.0015 (I² = 0; this is
descriptive, because the files share concepts).

Other blocks:
- **Refit CIs replace the iteration-1 ones (F5).** exp4's own M0 lead holds: +0.103 [0.010, 0.212] (iteration 1:
  [0.034, 0.167]). Size-controlled: +0.102 [0.017, 0.217]. The multi-feature rows now include 0:
  all_four_available +0.082 [-0.042, 0.204]; size_controlled_all_three +0.085 [-0.043, 0.220].
- **B1, field propensity.** Over M2 + P (leave-concept-out shrunken field retention mean), gateway adds +0.0015 on the
  union panel (CI [-0.008, 0.007]) and -0.004 on new episodes. P alone adds +0.022 [-0.013, 0.076] on the union panel.
  The pooled-P version is similar.
- **B2, field intercepts.** In exp4, gateway explains 50% of stage-1 field intercepts (WLS slope 4.9, permutation
  p = 0.14, 10 fields) and removes 74% of the field random-intercept variance. On the union panel this drops to R² = 0.03
  (p = 0.55, 20 fields) and 2.5% of the variance. The exp4 effect is a field-ranking coincidence in 10 fields. A static
  field-FE test is unidentifiable by construction.
- **B3, time-varying gateway.** The slice backbones validate (Spearman with exp4's gateway: 0.92), but the design is
  **NOT IDENTIFIABLE**: within-field SD / between-field SD = 0.023, below the 0.10 gate. The two slices correlate at 0.99.
  This test passes to the iteration-2 panel.
- **C, placebos.** C2 node-label permutation (1,000): the union real value sits at the 54th percentile (p = 0.46) and
  new episodes at the 41st. On exp4, M2 sits at the 92.5th percentile (p = 0.076). C1 degree- and connectivity-preserving
  rewiring (200 draws, discriminating: median Spearman(real, rewired) = 0.32): on exp4, M0 is at the 99.5th percentile
  (p = 0.01) and M2 at the 95.5th (p = 0.05); on the union panel they are at the 60th and 37th. C3: no rival centrality
  (strength, degree, betweenness, PageRank, closeness, k-core, phi_min eigenvector, size) is significant after Holm
  correction on any panel.
- **D, O1 artefact.** All 8 G-variant O1 gains reproduce exactly (G +0.072, G_all +0.112, G_deg +0.149, G_phimin
  +0.154, ...). All 8 are **ARTEFACTS**: once label_coverage_early and a training-fold O1 base rate are added to B5, each
  falls by at least 50% and its 90% CI covers 0 (G: +0.072 -> +0.002).
- **E, power.** Concept ICC = 0.135 (latent scale). The analytic MDE at 80% power is 0.009 at N = 1,000 and m = 5. A
  simulation with only concept random intercepts agrees. With a **field random intercept** (tau = 0.71, from B2), the
  simulated SD under a true delta of 0.05 is about 0.015 and **does not shrink with N** (0.016, 0.015 and 0.014 at 1k, 2k
  and 4k). The 26 fields put a floor under the MDE (about 0.02). A true delta of 0.05 is still detected with power
  close to 1 at N >= 1,000. The shrunken estimate (union lower 90% bound, -0.010) is <= 0, so no feasible panel has power
  for it. Held-out sizing: about 34 concepts per group for P(group delta > 0) >= 0.9, and about 14 for P(>= 3 of 4
  groups) >= 0.8 at 0.05, based on the alternative SD. The plan's null-SE sizing (1-4 concepts) is reported but
  flagged as optimistic.
- **F, record tables.** rho_B5 per experiment (0.834 / 0.770 / 0.327), A*_h medians (negative in 4/4 groups), exp3's
  portability table verbatim, and exp4's secondary screens (G_all, DOM_Physical and GATEWAY_REACH have 90% CIs wholly
  below 0).

**Independent audit (`audit.py` -> `results/audit_out.json`).** A separate L2-logistic solver (scipy L-BFGS),
Mann-Whitney AUC, and its own imputation and standardisation re-derive: exp4 0.10254 / 0.10222 (exact); exp4 M2 0.0375
(exact); union M2 +0.0012 (eval +0.0009); new episodes -0.0007 (eval -0.0006); union M0 +0.0022. The differences come
from optimizer tolerance. The C2 percentile on the one-to-one union rows is 54.0 (eval: 54.1). Placebos: with shuffled R
on the union panel, delta centres on 0 (-0.0001, 95% range [-0.030, 0.026]), so the "CI > 0" criterion fails as it
should. Caution: with shuffled R on exp4's 80 rows, the M0 delta has a 95th percentile of 0.130 (60 shuffles), above
the real 0.103. On 80 episodes, LOGO delta-AUC is too noisy to certify the original lead against a full label shuffle.
Not independently re-derived: the Block B2/B3, D and E numbers, and the bootstrap CIs themselves.

## Layout

| path | what |
|---|---|
| `eval.py` | main evaluation (Step 0 + Blocks A-F, verdict, figures, `eval_out.json`) |
| `lib.py` | LOGO models with fold-computed P / O1_base, refit-bootstrap / permutation / simulation workers; imports exp4's `screen.py` |
| `harmonise.py` | Step 0: attaches the exp4 backbone to all three files, crosswalk, overlap report, union panel |
| `audit.py` | independent re-derivation and placebo checks -> `results/audit_out.json` |
| `prereg/crosswalk.json`, `prereg/verdict_ladder.json` | pre-registration, written before any model was fitted |
| `eval_out.json`, `full_eval_out.json`, `mini_eval_out.json`, `preview_eval_out.json` | `exp_eval_sol_out` output: `metrics_agg` (336 flat numbers); `metadata` (every block's tables under A_replication, B_trait, C_placebo, D_O1_artefact, E_power, F_record, overlap, verdict, missing_inputs, deviations); `datasets` (per-episode OOF predictions for M2 and M2 + gateway for union, exp4, exp1 and exp3) |
| `results/union_episodes.csv` | harmonised, de-duplicated union panel (362 episodes, source flag, all covariates), for reuse in iteration 2 |
| `results/summary.json` | verdict and M2 headline per dataset |
| `results/cache/` | pickled intermediate results (regenerable; not published) |
| `figures/` | forest plot, C1/C2 placebo histograms, stage-2 field-intercept scatter, MDE-vs-N (PNG + PDF) |
| `logs/` | smoke run, the three production segments (part1: Block A to the end with exp4 from cache; part2: field-RE simulation added; part3_final: MDE figure update, all from cache) and the audit log |

## How to run

See `reproducibility.md`. In short:

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python <pinned deps from pyproject.toml>
export AII_ITER1=<folder holding gen_art_experiment_1/3/4>   # defaults to ../../../round-1
.venv/bin/python eval.py --n-boot 2000 --n-boot-exp4 2000 --n-boot-secondary 500 --n-boot-D 1000 --n-boot-F5 1000 \
    --n-perm 1000 --n-rewire 200 --n-sim 300
.venv/bin/python audit.py
```

Deviations from the plan are listed in `eval_out.json["metadata"]["deviations"]`. The main ones: secondary datasets use
500 bootstrap draws, per the plan's scaling rule on a heavily shared host; density_j for exp1/exp3 uses an approximation
of early field presence; the union panel adds source dummies; and the table blocks sit in `metadata`, because the schema's
`metrics_agg` accepts only numbers.

## Restoring removed files

The manifest `.aii/manifest.yaml` marks two paths for deletion. Both are regenerable:

- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy==2.5.3 pandas==3.0.6 scipy==1.18.1 scikit-learn==1.9.1 networkx==3.7 statsmodels==0.15.0 matplotlib==3.11.2 loguru==0.7.3`
  (full pin list in `pyproject.toml`).
- `__pycache__/`: recreated automatically by Python on import.

`results/cache/` (pickled intermediate block results, under the auto-keep floor) stays on the run's volume but is
excluded from the published repository. To rebuild it, run
`.venv/bin/python eval.py --n-boot 2000 --n-boot-exp4 2000 --n-boot-secondary 500 --n-boot-D 1000 --n-boot-F5 1000 --n-perm 1000 --n-rewire 200 --n-sim 300`
(about 30 min on 4 idle cores).
