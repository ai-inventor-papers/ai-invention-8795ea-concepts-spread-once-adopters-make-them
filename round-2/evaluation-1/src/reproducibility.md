# Reproducing the gateway-lead stress test

These are the steps that were actually run to produce `eval_out.json`. No API calls of any kind are made: no
OpenAlex, OpenRouter or other network access, and no API keys are needed.

## 1. Get the artifact and its inputs

This workspace is published as one folder of a public GitHub repository. Clone that repository and `cd` into this
artifact's folder:

```bash
git clone <repository-url>
cd <repository>/<this-artifact-folder>        # the folder holding eval.py
```

The evaluation reads three iteration-1 artifacts **read-only**. The repository publishes them as sibling folders:

| artifact id | expected folder name | files read |
|---|---|---|
| art_33_KKk_G8Gw5 | `gen_art_experiment_4` | `field_outcomes.csv`, `field_backbone.json`, `features.csv`, `outcomes.csv`, `screen_result.json`, `screen.py` (imported) |
| art_xp8BGBJZsxeI | `gen_art_experiment_1` | `results/field_outcomes.csv`, `results/field_features.csv`, `results/features.csv`, `results/outcomes.csv`, `results/screen_result.json` |
| art_yrradSC27HtQ | `gen_art_experiment_3` | `results/field_outcomes.csv`, `results/outcomes.csv`, `results/field_names.csv`, `results/topic_meta.csv`, `results/screen_result.json`, `scan/ckpt.npz`, `scan/topic_ids.json` |

The code finds them through ONE setting: the environment variable `AII_ITER1`, which names the folder that holds these
three sub-folders. When it is unset, `lib.py` defaults to `../../../round-1` relative to this folder, which is
the pipeline's layout. In a clone where the three folders are siblings of this one, run:

```bash
export AII_ITER1=..        # the parent folder that holds gen_art_experiment_1/3/4
```

`scan/ckpt.npz` (37 MB) is needed only for Block B3. If it is missing, B3 is skipped and listed in
`missing_inputs`. No user-uploaded files are used (the run's upload folder was empty).

## 2. Environment

- OS: Ubuntu/Debian Linux, x86-64. Actual run: Debian 12 container, 4 CPUs (AMD EPYC 9655P), 29 GB RAM cgroup limit,
  **no GPU**. The host was heavily shared (load average ~180).
- Python **3.12.14**, managed with `uv`. No system packages beyond a C toolchain-free Python.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(python3 - <<'EOF'
import tomllib; print("\n".join(tomllib.load(open("pyproject.toml","rb"))["project"]["dependencies"]))
EOF
)
```

The pinned versions (identical to `pyproject.toml`) include numpy 2.5.3, pandas 3.0.6, scipy 1.18.1,
scikit-learn 1.9.1, networkx 3.7, statsmodels 0.15.0, matplotlib 3.11.2 and loguru 0.7.3.

## 3. Pre-registration (already in the repository)

`prereg/crosswalk.json` (S2-to-OpenAlex field crosswalk, group harmonisation, union priority) and
`prereg/verdict_ladder.json` (REPLICATES / ATTENUATES / FIELD-TRAIT / FAILS rules) were written before any model was
fitted. `eval.py` reads them and does not modify them.

## 4. Commands, in the order they were run

```bash
# (a) smoke test with tiny draw counts (~9 min on the shared host); it checks every block end to end
.venv/bin/python eval.py --n-boot 20 --n-boot-secondary 20 --n-perm 16 --n-rewire 8 --n-sim 8

# (b) production run. The first attempt used 2,000 draws everywhere. It finished exp4's 2,000-draw bootstrap (cached
#     in results/cache/A_exp4_2000.pkl, ~15 min) and was then stopped because the shared host made each draw cost
#     1-1.7 s. It was restarted with the plan's scaling rule and --use-cache (log: logs/full_run_part1.log, ~14 min):
.venv/bin/python eval.py --use-cache --n-boot 2000 --n-boot-exp4 2000 --n-boot-secondary 500 \
    --n-boot-D 1000 --n-boot-F5 1000 --n-perm 1000 --n-rewire 200 --n-sim 300
#     The same command was then re-run twice (--use-cache; only new work recomputed): after adding the
#     field-random-intercept power simulation (logs/full_run_part2.log, ~2 min), and after adding those points to
#     the MDE figure (logs/full_run_part3_final.log, 27 s). The final eval_out.json comes from that last run, so its
#     metadata.runtime_s (27 s) reflects cache reads, not the full compute.
#     Running the command once without --use-cache and without results/cache/ reproduces everything in ~30-35 min
#     on 4 shared cores.

# (c) independent re-derivation audit (own L2-logistic solver, rank AUC, shuffled-label and node-permutation placebos)
AUDIT_N_SHUF=60 AUDIT_N_PERM=100 .venv/bin/python audit.py        # writes results/audit_out.json

# (d) full / mini / preview variants of the output (aii-json skill script; any equivalent truncation works)
python aii_json_format_mini_preview.py --input eval_out.json
```

Seeds: the base seed is `SEED = 20260928` (eval.py). Bootstrap draw k of dataset i uses seed `SEED + 100000*i + k`;
C1 rewiring uses `SEED+1`/`SEED+2`; the C2 permutations use `SEED+3`; Block D uses `SEED+9000+k`; Block E uses
`SEED + 10*N + m (+500000 for the alternative)`; the audit uses seed 99. Workers are a spawn-context
`ProcessPoolExecutor` with 4 workers and `OMP_NUM_THREADS=1`. Results do not depend on worker scheduling, because
seeds are fixed per draw.

Total compute on the shared 4-CPU host was about 32 min (15 min for exp4's 2,000 draws, 14 min for the restarted
run, 2 min for the field-RE simulation). On an idle 4-core machine, expect about half of that. The audit takes about
1 min.

## 5. What you should get

- `eval_out.json` / `full_eval_out.json` (schema `exp_eval_sol_out`, validated), plus `mini_` and `preview_` variants.
- `metadata.reproduction`: exp4's iteration-1 field-level deltas reproduce exactly (0.10254 and 0.10222).
- `metadata.verdict.verdict`: the pre-registered verdict, with every condition listed (see README.md for the values).
- `metrics_agg`: flat headline numbers. For example, `A_union_M2_delta_auc` with `..._ci95_lo/hi` is the primary
  estimand, and `A_new_eps_M2_delta_auc` is the cleanest replication.
- `results/union_episodes.csv`: the harmonised de-duplicated union panel, reusable by iteration 2.
- `results/summary.json`: verdict and M2 headline per dataset. `results/audit_out.json`: independent re-derivation.
- `figures/forest_delta_auc.png|pdf`, `figures/placebo_hist.png|pdf`, `figures/stage2_field_intercepts.png|pdf`,
  `figures/mde_vs_n.png|pdf`.

In the paper, these numbers feed the section that re-evaluates the field-retention (RQ2 diffusion) lead: the replication
table (Block A), the trait-confound and placebo analyses (Blocks B and C), the O1 artefact note (Block D), the power
and sample-size statement for the held-out panel (Block E), and the corrected iteration-1 record tables (Block F).
