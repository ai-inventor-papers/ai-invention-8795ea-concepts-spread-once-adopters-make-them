# How concepts spread: contact versus keeping (RQ2 trajectories, cache-only re-run)

AI Inventor, invention loop iteration 4, artifact `gen_art_experiment_12` (plan `gen_plan_experiment_3_idx3`, RQ2).
It re-runs the failed iteration-3 RQ2 artifact (gen_art_experiment_9, never executed). Every input is a cached
array from EXP5, EXP6, EXP7 or EXP8 of this run. It makes **0 OpenAlex calls, no S3 reads and no LLM calls**; a network
guard in `lib/common.py` makes any HTTP or S3 client import fail.

> **Disclosure (second use of the frame).** EXP5, EXP7 and EXP8 already unsealed the held-out outcomes. This
> artifact's seal (`results/frozen_spec.json`, sha256 in `logs/seal.log`) guarantees only one thing: every analysis
> choice here (OPEN formula, z constants, typology variables, k, HMM states, PCA loadings, decomposition variants,
> pre-registered text, case and atlas rules) was fixed on DEV before this artifact read held-out states or outcomes.
> The held-out and cohort results are therefore **within-frame robustness checks, not confirmation**. Fresh
> confirmation (the 2015-16 cohort) belongs to another artifact.

## The question and the design

Do concepts that end up spread across many fields get there because they **reach** more fields early (contact and
exploration), or because they **keep** the fields they touch (retention)? And does the "openness" of a concept's
early topic neighbourhood line up with how it later spreads?

The frame is the 12,499 EXP5 concepts (onset t0 in 2003-2014). DEV has 4,771 concepts (CS, Eng, BGM, Med homes).
The held-out groups are PHYS 742, LIFEENV 1,113, SOC 1,352 and MATHDEC 165. The 2010-14 cohort has 4,356 concepts:
2,484 with DEV homes and 1,872 with other homes. Fields are the 26 OpenAlex venue fields. Field states follow the
EXP6/EXP7 D3 semantics:

- *entered*: cumulative grounded papers >= 2;
- *retained*: entered at least 2 years earlier and >= 2 papers in the last 3 years, off-home;
- *lost*: entered, but 0 papers in 3 years.

| stage | script | what it does |
|---|---|---|
| S0 | `s0_skeleton.py` | writes and validates the `method_out.json` skeleton FIRST (EXP9 died on output format); records sha256 provenance of the copied library code |
| S1-S2 | `s2_open.py` | join; **OPEN** openness score in three builds: ALL-PAPERS (EXP8 ego features), HOME-ONLY (home-venue papers only), SIZE-MATCHED (20 year-stratified subsamples of all papers down to the home-only count) |
| S3 | `s3_states.py` | D3 state sequences, ages 0..10, for all 12,499 concepts; verified cell by cell against the EXP7 state panel; per-age summaries |
| S4 | `s4_decomp.py` | exact decomposition **log Bn = log E2 + log M + log rho** of the top-vs-bottom O2r_resid tercile gap, with pre-registered verdicts |
| S5 | `s5_typology.py` | DTW k-medoids + Gaussian HMM typology under a strict naming rule, else a **PCA continuum**; OPEN on the axis |
| S6 | `s6_sequence.py` | light ordering test: home-prominence half-peak vs off-home take-off, with a mechanical-lag permutation null; intersection-born vs single-home |
| S7 | `s7_seal.py` | freeze -> T6 checklist -> unseal once -> held-out and cohort runs of S4-S6 |
| S8 | `s8_cases.py` | 7 most-similar case pairs (matched on volume and growth, opposite OPEN; outcome shown after selection) |
| S9 | `s9_atlas.py` | retrospective AI/CS atlas (37 concepts, 5 outcome types; outcome-selected by design) |
| S10 | `s10_outputs.py` | `pipeline_counts.json`, `method_out.json`, summary figures |
| T7 | `rederive.py` | independent pandas re-derivation of the held-out shares and the OPEN~PC1 Spearman |

The decomposition terms, per concept at horizon H = 8:

- E2 = off-home fields entered by age 2 (early **contact**);
- M = EH / E2 = frontier advance from age 2 to 8;
- rho = Bn / EH = share of entered fields still retained at age 8 (**retention**);
- Bn = retained off-home fields at t0+8.

At group level, mean Bn = mean E2 x (sum EH / sum E2) x (sum Bn / sum EH) holds exactly. The log ratio of each
factor (top vs bottom tercile) is its exact, unique Shapley share of the gap. The primary variant averages this
within early-volume quintiles, weighted by n. **These shares are an accounting identity for the breadth outcome, not
causal effects**: Bn at t0+8 is built from the same papers as O2r, and only E2 is early.

## Results

### 1. Breadth gaps are mostly early contact; retention is the smaller part (PR1 and PR1b SUPPORTED everywhere)

Volume-stratified decomposition of the top-vs-bottom O2r_resid tercile gap. D_k = log(top/bottom); shares sum to 1;
95% CIs from 2,000 concept bootstraps (terciles and quintiles recomputed in each resample).

| sample | n | D_E2 (contact) | D_M (frontier) | D_rho (retention) | s_E2 / s_M / s_rho | s_explore - s_ret [95% CI] |
|---|---|---|---|---|---|---|
| DEV, all homes (primary ii) | 3,188 | 1.050 | -0.062 | 0.393 | 0.76 / -0.05 / 0.29 | 0.431 [0.371, 0.493] |
| DEV, Medicine excluded (**PR1 variant iv**) | 1,469 | 0.866 | 0.032 | 0.202 | 0.79 / 0.03 / 0.18 | **0.633 [0.537, 0.727]** |
| Held-out pooled (PHYS/LIFEENV/SOC/MATHDEC), iv | 1,825 | 0.759 | 0.013 | 0.263 | 0.73 / 0.01 / 0.25 | **0.492 [0.403, 0.575]** |
| Cohort 2010-14 pooled, iv | 1,403 | 0.724 | 0.033 | 0.291 | 0.69 / 0.03 / 0.28 | **0.445 [0.358, 0.527]** |
| DL over held-out groups (PHYS, LIFEENV, SOC) | 3 groups | 0.772 | 0.005 | 0.246 | - | 0.504 [0.329, 0.679], I2 = 0.76 |

- PR1 is **SUPPORTED** on DEV, in every held-out group and in both cohort parts: PHYS 0.33, LIFEENV 0.55, SOC 0.62,
  MATHDEC 0.41, COH_DEVHOME 0.39, COH_OTHER 0.49, all with CI > 0 (`figures/fig_forest_explore_vs_retention.png`).
  s_ret < 0.5 in all of them.
- PR1b (contact alone beats retention) is **SUPPORTED**: DEV 0.604 [0.508, 0.698], held-out pooled 0.480
  [0.394, 0.570], cohort 0.414 [0.324, 0.494]. Holm p < 0.001 in family R2-A.
- **Frontier advance M carries almost nothing** (|D_M| <= 0.16 in every variant). Integrating concepts do not
  enter proportionally more *new* fields after age 2; the gap is set by contact already made by t0+2, plus
  somewhat better retention.
- **PR3 (descriptive):** D_rho is **positive** everywhere (DEV 0.20 [0.14, 0.27]; held-out 0.26; cohort 0.29).
  Integrating concepts keep a *larger* share of the fields they enter, so retention helps rather than hurts.
  Retention is simply the smaller of the two contributions.
- **Robust to**:
  - min_n = 3 or 5. At min_n = 5, D_rho on the held-out pool shrinks to 0.07 [-0.001, 0.16], so the retention part
    is the one that is sensitive to the threshold.
  - O2r_m50 instead of O2r_resid;
  - only sustained concepts (O1b = 1);
  - onset-restricted counts (pre-t0 papers removed; s_E2 = 0.86 on DEV);
  - excluding the 658 EXP6-overlap concepts;
  - additive Das Gupta decomposition (DEV shares 0.77 / -0.05 / 0.28, summing exactly to the gap);
  - concept-level covariance decomposition of var(log Bn) (DEV 0.59 / 0.03 / 0.38; held-out 0.56 / 0.01 / 0.44).
    At the concept level retention matters more than at the group level.
- **Medicine**: including Medicine homes raises the retention share (DEV Med group s_rho = 0.34 vs 0.07-0.21 for
  CS/Eng/BGM), which is why PR1 is judged with Medicine excluded.
- **Checks**:
  - T5: a second bootstrap seed moves CI ends by <= 0.004.
  - T9 placebo: with O2r_resid shuffled within group, D_k centres near 0 (Medicine-excluded D_total 0.04
    [-0.02, 0.11] vs observed 1.10). With all homes, a within-group shuffle leaves D_total 0.15 [0.10, 0.20]
    because group composition differs; the observed 1.38 is far outside that.
  - Shares are unstable under the null by construction (D_total ~ 0), so the D_k are the quantities to read.

Source: `results/decomposition_dev.json`, `results/decomposition_heldout.json`, `results/T7_rederivation.json`,
`figures/fig_decomposition_waterfall.png`, `figures/fig_forest_explore_vs_retention.png`.

### 2. PR2 ("localised concepts keep more early") is NOT supported as stated; only its partial clause holds

- The raw clause fails. The mean early retention ratio (t0..t0+2) of the bottom O2r_resid tercile minus the top
  tercile is:
  - DEV: -0.110 [-0.132, -0.086] (**REVERSED**: bottom 0.166 vs top 0.275);
  - held-out pooled: +0.011 [-0.019, 0.039] (NOT SUPPORTED);
  - cohort: -0.058 [-0.083, -0.031] (REVERSED).
- The partial clause holds everywhere. The partial Spearman of RETENTION_RATIO_early with O2r_resid given B5 is
  negative: DEV -0.169 [-0.202, -0.134], held-out -0.129 [-0.175, -0.086], cohort -0.173 [-0.212, -0.133].
  This replicates EXP8's -0.120 on the same frame and is not new evidence.
- Read together: *at equal early size and breadth*, concepts that keep a higher share of their early contacts end up
  narrower. Without that adjustment, integrating concepts keep more.
- Verdict per the frozen rule: PR2 = REVERSED on DEV, NOT SUPPORTED on held-out, REVERSED on the cohort.

Source: `results/decomposition_*.json` (keys `early_ratio_PR2`, `verdicts`).

### 3. No trajectory typology survives the naming rule; the result is a continuum

- DTW k-medoids on 9 yearly variables x ages 0..8 (4,771 DEV concepts) chose k = 4. It was the only k with median
  80%-subsample ARI >= 0.6 (0.87), but its silhouette is only 0.13; the gap statistic points to k = 8.
- The Gaussian HMM partition (BIC chose S = 5, the top of the tested range 3-5) agrees poorly: **ARI(DTW, HMM) =
  0.22 < 0.5**.
- Hennig bootstrap Jaccard: 0.69, 0.81, 0.82, 0.73.
- Re-clustering without Medicine gives ARI 0.46 < 0.5.
- Held-out re-clustering vs nearest-DEV-medoid assignment gives ARI 0.44 (held-out) and 0.38 (cohort), both < 0.5.
- The classes are not volume classes (ARI with volume tercile 0.02). They are Medicine-skewed: 849 of the 1,080
  concepts in class 1 are Medicine homes.
- **No class is named. The pre-registered CONTINUUM is reported**, and the EXP6 two-class typology stays NOT
  ESTABLISHED (ARI of our classes vs EXP6's on 122 overlapping concepts: 0.20).
- PCA of the same DEV trajectories (`figures/fig_pca_loadings.png`):
  - **PC1 (38.8%)** is a *breadth-of-spread* axis: fields entered, fields retained, field entropy and community
    span load positively at every age; home share loads negatively.
  - **PC2 (10.7%)** is a *keep-versus-lose* axis: retention share positive, fields lost and fields entered negative.
  - PC1 correlates only weakly with early volume (Spearman 0.15).
  - The bottom PC1 tercile is 76% Medicine-home concepts; the top tercile is 33%.

Source: `results/trajectories_dev.json`, `results/trajectories_heldout.json`, `figures/fig_dtw_hmm_agreement.png`.

### 4. Early openness goes with breadth of spread, not with keeping

Spearman of OPEN with PC1. "Partial" = given B5 and label coverage. 95% concept-bootstrap CIs; held-out pooled with
DerSimonian-Laird over the 4 held-out groups.

| OPEN build | DEV rho | DEV partial | held-out DL rho (I2) | held-out DL partial (I2) | cohort partial |
|---|---|---|---|---|---|
| ALL-PAPERS | 0.352 [0.325, 0.376] | 0.174 [0.146, 0.202] | 0.432 [0.312, 0.552] (0.94) | 0.120 [0.085, 0.155] (0.00) | 0.117 [0.087, 0.147] |
| HOME-ONLY | 0.174 [0.145, 0.202] | 0.117 [0.085, 0.146] | 0.212 [0.089, 0.335] (0.90) | 0.060 [0.023, 0.097] (0.00) | 0.121 [0.088, 0.153] |
| SIZE-MATCHED | 0.091 [0.063, 0.120] | 0.135 [0.107, 0.163] | 0.208 [0.005, 0.411] (0.97) | 0.094 [0.060, 0.129] (0.00) | 0.089 [0.058, 0.119] |

- The raw association is partly mechanical. The all-papers ego network gains off-home topics exactly as the concept
  spreads, which is why the HOME-ONLY and SIZE-MATCHED builds exist. Even so, a **positive partial association
  survives in all three builds and in every split**, and is homogeneous across held-out groups (I2 = 0 for the
  partials). It is small: 0.06-0.17.
- A within-group shuffle of OPEN gives null bands that cover 0 (T9).
- OPEN is **not** positively related to PC2, the keeping axis: DEV partial -0.07 to -0.11; held-out -0.04 to +0.01.
- Coverage of OPEN_home is 84.7%. Between-build Spearman correlations are 0.57 (all vs home) and 0.73 (all vs
  size). Source: `results/open_diagnostics.json`.

Source: `results/trajectories_*.json` (keys `open_on_axis*`, `DL_heldout_groups_PC1`, `T9_*`),
`figures/fig_open_vs_pc1_hexbin.png`.

### 5. Ordering (light test): no signal beyond the mechanical lag

- Home-prominence half-peak before off-home take-off (A < T) occurs in 25.6% of DEV concepts, against 26.4% under a
  1,000-permutation mechanical-lag null. The excess is:
  - DEV: -0.009 [-0.015, -0.003];
  - held-out: +0.011 [0.005, 0.016];
  - cohort: -0.017 [-0.023, -0.012].
- The frozen rule's verdict words are MIXED (DEV), HOME-FIRST (held-out) and MIXED (cohort). But the effect is about
  1 percentage point and flips sign, so **no ordering claim is made**.
- Intersection-born concepts (two home fields) take off off-home *later*: cloglog hazard ratio 0.47 [0.42, 0.54] on
  DEV, 0.45 held-out, 0.41 cohort (`figures/fig_km_takeoff.png`). This is largely mechanical, because a second
  home absorbs fields that would otherwise count as off-home.

Source: `results/sequence_light_*.json`.

### 6. Case pairs and AI atlas (illustration, not inference)

- **Seven most-similar pairs**, matched within reporting group on z(log volume) and z(growth) <= 0.25 and onset
  +/- 2 years, with opposite OPEN_all quintiles (`case_studies/pair*/`, `figures/fig_case_pairs.png`):
  - Graphics processing unit / Vertical axis wind turbine;
  - Shotgun proteomics / Image-guided radiation therapy;
  - Nanocarriers / Nanosheet;
  - Soft power / Autonomous learning;
  - Scopus / Oxygen reduction reaction;
  - Sclerostin / IgG4-related disease;
  - User-generated content / Mindfulness-based cognitive therapy.
- The pairs cover CS+Eng, BGM+Med, PHYS and SOC. LIFEENV and MATHDEC had no valid match.
- In **7 of 7** pairs the high-OPEN member has the higher O2r_resid. This is descriptive (n = 7, no p-value), and
  O2r was not used in selection.
- The OPEN_home order agrees with OPEN_all in all 7 pairs.
- Each pair directory holds:
  - `flow_raster.png`: state ribbons plus the field x age raster, ordered by backbone community;
  - `ego_snapshots.png`: W1-W3 topic ego networks, plus W3 home-only;
  - `pair.json`: B5, OPEN components in 3 builds, E2/M/rho, PC1, outcomes, and recognition events with lag to t0.
- **AI/CS atlas** (`ai_atlas/`; RETROSPECTIVE and OUTCOME-SELECTED BY DESIGN): 37 CS-home concepts. RAPID,
  GRADUAL, DIFFUSING and TRANSIENT have 8 each; LOCAL has only 5 eligible. AI-share tiers are relaxed per type and
  recorded.
- By the frozen written rule, these measures "looked meaningful" (DIFFUSING vs LOCAL >= 0.5 pooled SD at age 2, with
  the same sign as the frame-wide DEV correlation): early volume, field entropy, fields entered and retained,
  community span, frontier, ego-network communities, participation, ego density (negative), and OPEN_all and
  OPEN_home.
- Topic-level structure exists only for t0-3..t0+2 (a data limit of EXP8 Pass A), so the atlas cannot show
  topic-neighbour change after t0+2.

## Verification

- **T0 unit tests** (`tests/test_units.py` -> `results/unit_tests_T0.json`): all pass.
  - hand-built D3 states;
  - decomposition identity (error < 1e-15);
  - planted contact-only and retention-only gaps (shares ~1 / ~0);
  - planted 3-regime typology (DTW and HMM ARI = 1.0, choose_k = 3); pure noise fails the naming rule;
  - numba DTW equals tslearn;
  - OPEN formula;
  - seal refusals;
  - generic filter.
- **T2 reproduction**:
  - `lib/ego_open.py` reproduces EXP8 ego features exactly on 300 concepts (max |diff| = 0;
    `results/t2_ego_open_reproduction.json`);
  - the rebuilt D3 states equal the EXP7 state panel on all 5,557,942 cells of its 11,841 concepts (0 mismatches;
    the 658 missing concepts are exactly the EXP6 overlap);
  - RETENTION_RATIO_early and CONTACT_REACH are re-derived exactly;
  - O2r_m50 in EXP8 vs EXP5: rho = 1.0 (`results/states_verification.json`, `results/t2_o2r_crosscheck.json`).
- **T6**: pre-unseal checklist passed (`logs/T6_preunseal_checklist.json`).
- **T7**: independent re-derivation matches the pipeline to 6e-17 (shares) and 1e-16 (Spearman).
- **Headline audit** (`audit_headlines.py` -> `results/audit_headlines.json`):
  - separate code re-derives, from the raw per-concept files, PR1 on DEV, held-out and cohort, the PR2 partial
    Spearman, the three OPEN~PC1 partials and ARI(DTW, HMM), all to <= 6e-17;
  - every test fails on shuffled input: PR1 CIs span about -12..40 with the outcome shuffled; the PR2 partial is 0.02
    [-0.02, 0.05] with the ratio shuffled; the OPEN partials under full permutation are about 0 [-0.03, 0.03]. The
    observed 0.12-0.17 lie above the range of 100 within-group shuffles (max 0.046).
- `method_out.json` was validated against `exp_gen_sol_out` after every stage (`logs/validate.log`).

## Deviations

All are listed in `results/deviations.json`, each with its effect on the claims. The main ones:

- The plan's "O1c = 1" is implemented as O1b = 1, because O1c is continuous in EXP8.
- DTW uses a numba kernel identical to tslearn (tslearn projected 61 min).
- fasterpam is single-threaded per job.
- No git commit at the seal (the workspace is not a repository); the sha256 seal and one-time unseal marker are used
  instead.
- The atlas relaxes AI share per type.
- `in_exp6` is taken from EXP7's overlap report.
- The HMM uses min_covar = 1e-3.
- T3 was not run as a separate smoke test.
- Code was edited after the seal: a merge fix, figure layout, and the atlas AI-share relaxation changed from global
  to per type after the per-type counts were visible. None of these edits touches a frozen analysis rule.

## Layout

| path | content |
|---|---|
| `s0_skeleton.py` ... `s10_outputs.py`, `rederive.py` | pipeline stages (see the table above) |
| `lib/` | `common.py` (paths, seal-aware outcome loader, validation), `ego_open.py` (trimmed EXP8 ego code), `decomp.py`, `typology.py`, `cases_spec.py` (frozen case and atlas rules), `viz.py`; copied verbatim with sha256 in `logs/provenance.json`: `ego.py`, `ego_ctx.py` (path patch in `logs/ego_ctx_patch.diff`), `d3.py`, `rq1stats.py`, `traj_exp6.py`, `lib_outcomes.py`, `common_exp8.py`, `seal_exp8.py`, `build_features_exp8.py` |
| `method.py` | driver running every stage in order (`python method.py [--from STAGE]`) |
| `audit_headlines.py` | independent re-derivation of the headline numbers from raw files + placebo checks -> `results/audit_headlines.json` |
| `reproducibility.md` | exact environment, inputs (env vars per artifact id), commands, runtimes and expected numbers |
| `tests/test_units.py` | T0 unit tests |
| `method_out.json` (+ `full_`, `mini_`, `preview_`) | exp_gen_sol_out: dataset `rq2_concepts` (12,499 concepts; predict_open_axis = PC1, predict_decomposition = log factors) and `case_pairs` (7); metadata = headline results |
| `open_features.parquet` | OPEN components and scores in 3 builds, coverage, n_home |
| `panel.parquet` | per concept x age (0..10) summaries: contact, retention, frontier, entropy, home share, home prominence, community span, ... |
| `state_sequences.parquet` | per concept x age x field D3 state (0 untouched, 1 entered, 2 retained, 3 lost, 4 home, -1 after 2022) |
| `data/` | joined frame, decomposition inputs (min_n 2/3/5, onset-restricted), state codes, OPEN parts, frozen typology objects |
| `results/` | every JSON result, `frozen_spec.json`, `preregistration_R2.json`, `pipeline_counts.json` (every count read from files, for the methodology figure), `deviations.json` |
| `figures/` | decomposition waterfall, forest plot, PCA loadings, DTW-HMM agreement, OPEN-vs-PC1 hexbin, KM take-off, case-pair overview (PNG + PDF) |
| `case_studies/pairNN_*/` | per-pair figures and `pair.json` |
| `ai_atlas/` | `small_multiples.png`, `ego_W3_grid.png`, `table.csv`, `atlas.json` |
| `logs/` | stage logs, `seal.log`, `unsealed.json`, `validate.log`, provenance |

All of these are small and stay in the published repository. Nothing trained or irreproducible exceeds 100 MB.

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml
export AII_RUN_ROOT=<path to the run root holding 3_invention_loop/>   # defaults to four levels above this folder
.venv/bin/python s0_skeleton.py
.venv/bin/python s2_open.py --stage all --workers 24
.venv/bin/python s3_states.py
.venv/bin/python s4_decomp.py --scope dev
.venv/bin/python s5_typology.py --scope dev --workers 24
.venv/bin/python s6_sequence.py --scope dev
.venv/bin/python s7_seal.py --freeze      # freeze + checklist + ONE-TIME unseal (refuses a second time)
.venv/bin/python s7_seal.py --run         # held-out/cohort S4-S6
.venv/bin/python s8_cases.py && .venv/bin/python s9_atlas.py
.venv/bin/python s10_outputs.py && .venv/bin/python rederive.py
.venv/bin/python tests/test_units.py
```

Total wall time on 24 workers is about 45 min, most of it the HMM restarts. The inputs are the cached EXP5, EXP6,
EXP7 and EXP8 artifacts of the same run, read-only.

## Restoring removed files

Two paths are marked `delete` in `.aii/manifest.yaml`; both can be rebuilt:

- `.venv/` (the Python environment):
  `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml` (or `bash restore.sh`).
- `dtw_cache/` (DTW distance matrices, 408 MB, stored as row-chunk parts `D_<split>_part_NNN.npy` of <= 80 MB each, read back by `lib/typology.load_matrix_parts`):
  `.venv/bin/python s5_typology.py --scope dev && .venv/bin/python s5_typology.py --scope heldout`.
  The held-out call needs the existing unseal marker `logs/unsealed.json`; it recomputes and re-caches the matrices,
  and the results are deterministic given the seeds.
- `__pycache__/` directories (not shipped) are regenerated automatically by Python.
