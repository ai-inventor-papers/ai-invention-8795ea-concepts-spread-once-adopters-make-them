# Co-occurrence screen: structural diversity (D) and frequency-free selectivity (F)

AI Inventor, invention loop iteration 1, artifact `gen_art_experiment_3` (wide screen, strategy `gen_strat_1`).

**Question.** Do early *co-occurrence* signals of a newly emerging concept predict whether it later becomes
broadly integrated across science (size-adjusted venue-field breadth, **O2r**), beyond simple count, growth and
reach baselines (**B5**)? The two candidates make opposite predictions:

* **D**: *structural diversity* of newly acquired topic neighbours, meaning how many distinct communities of the
  topic knowledge network they reach, normalised by a frequency-matched null. D predicts that the gain
  concentrates on breadth.
* **F**: *frequency-free selectivity*, meaning growth of the mean PMI of the top-20 topic neighbours minus a
  size-matched, concept-preserving null. F predicts equal gains for uptake and breadth.

Both are scored on the frozen 78-concept dev panel **P78** under the shared protocol **S0** and the pre-registered
selection rule: Delta-rho >= 0.10, 90% CI low > 0, >= 3/4 groups positive, split-half SB >= 0.6, and |rho| <= 0.6
with log early volume and with early growth.

## Headline results (47 dev concepts: BIO 16, CS 12, MED 10, ENG 9; all have O2r)

| candidate | Delta-rho vs B5 (O2r, LOGO) | 90% CI | groups + | split-half SB | size rho (logvol / growth) | survives |
|---|---|---|---|---|---|---|
| **D** = `D_ratio` (primary D, pre-declared T3 fallback) | +0.006 | [-0.092, +0.135] | 3/4 (BIO +0.19, CS +0.01, ENG -0.08, MED +0.01) | 0.83 | 0.11 / 0.02 | no |
| **F** = `F_res` | -0.060 | [-0.158, +0.014] | 1/4 (CS -0.22) | 0.44 | 0.04 / -0.09 | no |
| `D_z` (the plan's literal primary; superseded) | +0.017 | [-0.101, +0.087] | 4/4 | 0.90 | **-0.63** / -0.09 | no (size relabel) |

* **The B5 baseline is strong.** Its LOGO Spearman with O2r is 0.77 (early venue entropy alone reaches 0.70),
  its AUC is 0.80 for O1 (uptake) and 0.86 for the top tercile of O2r.
* **No candidate survives.** Per the pre-registered rule, the top-ranked candidate by Delta-rho (**D**) is
  carried forward as the best available result, and the null is reported.
* **Uptake/breadth dissociation.** Both verdicts are *inconclusive*. For D, dAUC(O2r_top) - dAUC(O1) = -0.017,
  90% CI [-0.083, 0.075]. For F it is -0.081, 90% CI [-0.181, 0.045], so F's equivalence prediction is not met.
* **O3 (transience) is not estimable** under leave-one-group-out: all 4 transient concepts (pandemic H1N1,
  SARS, NOTES, single-incision laparoscopic surgery) have Medicine as home. The reach30 hurdle is not estimable
  either, because every dev concept reaches N >= 30.
* **Field-level retention R_j** (129 concept x off-home field rows, base AUC 0.76). Adding Dj gives dAUC +0.000,
  90% CI [-0.044, 0.028]; adding Fj gives -0.008, 90% CI [-0.088, 0.034].
* **Indicator portability.** Several co-occurrence breadth indicators are associated with O2r in *every* group,
  but they are not incremental under the screen statistic:
  * `D_ratio`: pooled rho 0.53 (0.33-0.63 per group);
  * `D_rare`: pooled rho 0.63;
  * `participation`: pooled rho 0.51;
  * `NOV_res`: pooled rho 0.45.

  **Negative result:** degree growth, strength growth and new-edge rate work in CS/AI only (CS rho about +0.45,
  BIO and ENG negative), so they are flagged `CS-only`. Kendall's W of indicator ranks across the 4 groups is 0.52.
* **Exploratory, not pre-registered.** With B5 at rho 0.77, Delta-rho is close to its ceiling: in-sample, adding
  D_ratio raises it by only 0.016 even though D_ratio's partial Spearman with O2r given B5 is 0.47. An
  out-of-group *partial* association (residuals on B5 fitted on the training groups) gives:
  * D_ratio +0.34, 90% CI [0.02, 0.65], 3/4 groups positive;
  * F_res -0.27.

  A permutation test puts the D_ratio value at p = 0.037 (one-sided, 1,000 permutations), which is marginal.
  This suggests D-type diversity carries non-redundant but modest information. The next iteration should use a
  statistic that is not saturated by a strong baseline. This analysis is never used for selection.

Every number above comes from `results/screen_result.json`, `results/exploratory_partial_association.json` and
`method_out.json`.

## What was done (and how it departs from the plan)

The shared OpenAlex key had **0 credits left** when this artifact started (`x-ratelimit-remaining: 0`, resetting
in about 11.7 h), so the design was adapted to be **almost credit-free**. Every change is logged in
`results/deviations.json`.

1. **S0 grounding via the API (156 credits, public anonymous pool).** For each concept, one
   `group_by=publication_year` call with quoted `title_and_abstract.search`, `type:article|review` and
   `is_paratext:false`. These counts give t0, the newborn flag, the dev cohort (2003 <= t0 <= 2009), O1, O3,
   log volume and growth, exactly as in S0.
2. **Everything else from the free OpenAlex S3 works snapshot (0 credits).** `scan_snapshot.py` streamed 7 leaf
   columns of all **476,196,327** works (2,040 parquet files) over HTTP range requests in 17 minutes. It
   produced:
   * **title matches** for every P78 phrase, using analysis that mimics OpenAlex search (lowercase, stop words
     with position gaps, Porter stems, positional phrase match): 576k concept-work rows;
   * exact **yearly background topic prevalence**. The snapshot's base-work counts match the API's global
     counts within 0.5%.
   * **full-corpus topic co-occurrence** for the backbone slices 2000-04, 2005-09 and 2010-14 (15-30M works
     each). The plan used 10k-work samples instead.

   Venue-field compositions (home field, O2r, R_j, early off-home share, entropy and reach) and ego topic counts
   therefore use **title-matched** works: a median 48% of the API count, with Spearman 0.88 against the API's
   early volume.
3. **Backbone.** PMI edges (c >= 3, PMI > 0; mean degree 157-188), clustered with Leiden. The plan's gamma rule
   (maximum median modularity) gave only about 8 communities on this dense full-corpus graph. Before any outcome
   was seen, the rule was changed to "highest-Q gamma with >= 20 non-trivial communities", which gives
   **gamma = 3**: 25, 26 and 23 communities, aligned across slices with a median Jaccard of 0.81-0.82. The
   plan-rule partition is reported as `D_q`.
4. **Ego networks, D and F, and rivals** (`features.py`):
   * Windows: PRE t0-3..t0-1, W1 t0..t0+1, W2 t0+2, W3 t0+3..t0+4.
   * PMI against the exact background.
   * SELF topics are excluded. A topic is SELF if its name contains all content lemmas of a concept phrase, or
     if it tags >= 20% of the concept's early papers.
   * Nulls use 1,000 draws each.
   * The same ego data give about 25 rival indicators: degree, strength and new-edge growth, persistence,
     turnover, participation, community transitions, ego density, and betweenness, k-core and constraint of
     the concept inserted into a kNN-sparsified backbone.
   * Split-half reliability uses **real paper-level halves** (50 splits), not binomial thinning.
5. **T3 STOP-AND-FIX fired for D.** 70% of the D_z values are below -5, and Spearman(D_z, M) = -0.69: the
   frequency-matched null draws from all of science, while real neighbours are topically concentrated, so z
   scales with the number of new neighbours. As the plan pre-specified, the primary D became `D_ratio`, which
   has a smaller |rho| with M than `D_rare` (0.23 against 0.29). This choice used outcome-blind diagnostics only.
6. **Screen** (`screen.py`):
   * leave-one-home-field-group-out ridge regression (alpha = 1) for O2r;
   * L2 logistic regression (C = 1; an exact Newton solver, which matches sklearn to 1e-7) for O1, O3,
     O2r_top and reach30;
   * 2,000 group-stratified concept bootstraps; concept-clustered bootstraps for R_j;
   * the dissociation tests, portability (within-group rho, Kendall's W, the CS-only flag), and sensitivities:
     newborn only, O2r at m = 50, label coverage or has_self_topic added to the baseline, and the variants
     D_lag, D_sub, D_withself, D_q, D_rare, F_bg, F_z and NOV_res.

**Tests.**
* **T0 (synthetic):** 5 of 6 pass (`results/unit_tests_T0.json`). The F null has a small negative plug-in bias:
  F_res is -0.14 under pure 10x growth with a fixed mix (SD 0.46), against +2.0 under injected selectivity.
* **T6:** a second bootstrap seed changes the CI endpoints by at most 0.0125
  (`results/t6_bootstrap_stability.json`).
* **Audit (`results/audit.json`):** independent code reproduces every headline number exactly. Permuted
  candidates never pass Delta-rho >= 0.10 (0 of 200); a planted feature does (Delta-rho 0.114).
* **API key:** it never appears in any file written by this code; the key is read from the environment and
  excluded from cache keys.

**Known data issues for the next iteration:**
* Non-English trade magazines (Japanese, Korean, Russian) receive a *Social Sciences* venue label from their
  topic profile. This is why ZigBee, WiMAX, LTE-Advanced, microblog, mashup and Web 2.0 fall outside the dev
  fields.
* The alias `TAVI` is polysemous in physics titles.
* The O3 base rate (8.5%) is below the expected 10-35%.

## Layout

| path | content |
|---|---|
| `method.py` | end-to-end orchestrator (steps below; idempotent, cached) |
| `config.py` | frozen P78 panel (verbatim; the `NOTES` alias is dropped and logged), seeded order, S0 constants, caps |
| `oa_client.py` | credit-aware, disk-cached OpenAlex client (ledger in `results/credit_ledger.json`) |
| `s0_fetch.py` | S0 yearly counts, global denominator, OR-syntax test |
| `snapshot_meta.py` | source -> venue field (>= 40% rule; repositories unlabelled) and topic metadata from the snapshot |
| `rangefile.py`, `scan_snapshot.py` | column-pruned HTTP-range reader and the resumable full-snapshot scan |
| `s0_outcomes.py` | onset, dev restriction, O1 / O2r / O2r_m50 / O3 / R_j, B5 and B_field baselines |
| `backbone.py` | full-corpus PMI backbone, Leiden gamma grid, slice alignment, kNN copy |
| `features.py` | ego networks, D and F with nulls, secondaries, rivals, field-level features, split-half |
| `screen.py` | LOGO models, bootstrap, selection rule, dissociation, portability, sensitivities |
| `extra_analyses.py` | EXPLORATORY out-of-group partial association and Delta-rho robustness |
| `make_outputs.py` | figures and `method_out.json` |
| `tests/test_synthetic.py` | T0 unit tests on synthetic data |
| `audit.py` | independent re-derivation of the headline numbers, placebo (permuted candidate) and planted positive control, written to `results/audit.json` |
| `t6_check.py` | T6 bootstrap-seed stability check |
| `reproducibility.md` | exact step-by-step reproduction (versions, commands, seeds, runtimes, expected numbers) |
| `pyproject.toml` | all dependencies pinned to the installed versions |
| `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json` | full / 3-item / truncated variants of `method_out.json` |
| `method_out.json` | executor-contract output (exp_gen_sol_out schema; 47 + 47 + 129 examples with LOGO predictions) |
| `results/outcomes.csv` | per-concept S0 outcomes, B5, coverage, drop reasons (all 78 concepts) |
| `results/features.csv` | per dev concept: B5 plus every candidate, secondary and rival indicator |
| `results/field_outcomes.csv` | concept x off-home field: R_j, B_field, Dj, Fj |
| `results/screen_result.json` | full screen: deltas, CIs, per-group values, reliability, criteria, portability, sensitivities |
| `results/screen_result_seed2.json`, `results/t6_bootstrap_stability.json` | T6 check |
| `results/exploratory_partial_association.json` | exploratory statistic (not used for selection) |
| `results/deviations.json` | every departure from the plan, with reasons |
| `results/backbone_summary.json`, `results/topic_communities.csv` | backbone diagnostics and communities per slice |
| `results/neighbour_audit.json` | top-10 PMI neighbours and SELF topics per concept (sanity / case studies) |
| `results/reliability_splits.csv` | 50 paper-level split-half recomputations per concept |
| `results/yearly_counts_api.json`, `results/or_syntax_test.json`, `results/credit_ledger.json` | S0 API data and credit use |
| `results/source_field.parquet`, `results/topic_meta.csv`, `results/field_names.csv` | venue labels and topic metadata |
| `scan/` | scan aggregates (`ckpt.npz`: per-year background, per-slice topic pairs) and title matches (`matches/matches_*.jsonl`, 3 parts under 100 MB) |
| `backbone/slice{0,1,2}.npz` | PMI edges, kNN edges, degrees, communities per slice |
| `cache/` | raw API responses (never re-queried) |
| `figures/` | `D_F_vs_O2r`, `delta_rho_forest`, `portability_heatmap` (PNG + PDF) |
| `logs/` | run logs |

The kept artifacts `scan/`, `backbone/`, `cache/` and `results/` stay on the run's storage volume at these
relative paths. They are all under the 100 MB publish limit, so they are also published.

## How to run

```bash
./restore.sh                                    # .venv + snapshot metadata (free)
.venv/bin/python tests/test_synthetic.py        # T0 unit tests (no network)
.venv/bin/python method.py                      # full pipeline; cached steps are skipped
.venv/bin/python method.py --from s0_outcomes   # recompute everything from the kept scan + cache
```

`s0_fetch` needs `OPENALEX_API_KEY` in the environment (or `OPENALEX_ANON=1` for the public pool) only when
`cache/` is missing. The snapshot scan needs no credentials. The full run takes about 17 min of scanning plus about
20 min of analysis on 4 CPUs.

## Restoring removed files

| deleted path | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` (exact pinned versions) |
| `snapshot/` | `./restore.sh`. It downloads the manifests from `https://openalex.s3.amazonaws.com/data/parquet/<entity>/manifest.json` and the parquet files of `sources`, `topics`, `subfields` and `fields`. Equivalent: `aws s3 sync s3://openalex/data/parquet/<entity> snapshot/<entity> --no-sign-request`. |
| `__pycache__/` | regenerated automatically by Python |

Note: the snapshot is updated monthly. A re-scan against a later snapshot will differ slightly from the kept
`scan/`, which was built from the 2026-09-23 snapshot.
