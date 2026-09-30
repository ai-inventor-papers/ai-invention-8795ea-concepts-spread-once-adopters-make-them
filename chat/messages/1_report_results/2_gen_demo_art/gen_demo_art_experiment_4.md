# gen_demo_art_experiment_4 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-30 01:37:42 UTC

```
model: Claude Opus 5.5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-30 01:37:50 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/`:
GOOD: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/file.py`, `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/.shared_cache`
`HF_HOME`, `HF_HUB_CACHE`, `TRANSFORMERS_CACHE`, `HF_DATASETS_CACHE`,
`TORCH_HOME`, `PIP_CACHE_DIR` and `UV_CACHE_DIR` are ALREADY set to point
there. Every step and every iteration of this run shares it, so a model or
dataset an earlier experiment downloaded is already on disk for you.

DO NOT override those variables. In particular do NOT write the common
pattern `os.environ["HF_HOME"] = <workspace>/hf_cache` — `HF_HOME` and
`TRANSFORMERS_CACHE` are read differently by `huggingface_hub` (one has
`/hub` appended, the other does not), so pointing both at one directory
stores every weight TWICE. That mistake cost one run 25 GB of identical
blobs. If you must set them, use the values above verbatim.

YOUR WORKING DIRECTORY IS A DELIVERABLE. When this module ends it must read
like a GitHub repository someone else can fork, resume and run — and the bulk
it holds must be either worth keeping or restorable. This run shares a storage
volume with the database; a run that fills it stops every other run on the box.

So before you finish, produce TWO files:

1. `.aii/manifest.yaml` — one entry per heavy path, each with EXACTLY ONE decision.
   The `.aii/` directory ALREADY EXISTS in your cwd: write the file into
   it. Do not create, replace or `touch` `.aii` itself — a plain file by
   that name makes the manifest unwritable for the rest of the module.

```yaml
entries:
  - path: results/
    keep: six GPU-hours of sweep output, not reproducible inside this run
  - path: hf_cache/
    delete: redownloadable
    source: "huggingface-cli download meta-llama/Llama-3-8B"
  - path: checkpoints/
    delete: regenerable
    source: "uv run train.py --epochs 3 --seed 0"
```

   - `keep:` takes a ONE-LINE reason. Use it for the expensive and the
     irreproducible: trained weights, long-running results, datasets you
     collected yourself.
   - `delete:` takes `redownloadable` (and a `source:` naming the repo id, URL
     or command) or `regenerable` (and a `source:` that is the command which
     rebuilds it). These are deleted AFTER the round ends, never mid-step.
   - Every path is RELATIVE TO YOUR CWD and must resolve INSIDE it. Absolute
     paths, `..`, and anything resolving outside are rejected.
   - Globs and whole directories are fine. A whole `hf_cache/` is ONE entry —
     do not list files individually.

2. `README.md` — written as if your cwd were a GitHub repository: what you
   did, the layout with a line per important file/directory, how to run it,
   and a **"Restoring removed files"** section giving the install/download
   command for EVERY `delete` entry. An `install.sh` or `restore.sh` beside it
   is welcome.

A CHECKER RUNS WHEN YOU SUBMIT. If anything heavy has no decision it fails
your submission and hands you the uncovered list, grouped by directory with
sizes, and you fix the manifest and submit again.

WHAT NEEDS NO DECISION — do not write entries for these:
- text and code files, at ANY size (source, JSON, CSV, YAML, logs, markdown);
- anything under the auto-keep floor (10 MB), whatever it holds.
Only large binaries and cache directories (`hf_cache/`, `.venv/`,
`node_modules/`, `checkpoints/`, `wandb/`, `__pycache__/`, …) need one.

NEVER mark your results, figures, papers, code, logs or anything a later step
reads as `delete`. If a later step needs it, it is a `keep`.

WHAT A `keep` BUYS YOU. Anything you do not mark `delete` stays exactly where
you wrote it, on this run's storage volume, at the path it already has — it is
not moved, renamed or copied. A later round reads it there, by that absolute
workspace path, so a checkpoint you keep is a checkpoint the next round can
load instead of retraining. It is also the ONLY copy: the publish step pushes
your cwd to GitHub but skips every file of 100 MB or
more, so trained weights and large binary artifacts never leave the volume.
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_wxWssKSUR45f
type: experiment
title: Do hub fields keep new concepts? Held-out test
summary: |-
  Sealed held-out test of H1 (does the adopting field's frozen 1998-2002 eigenvector gateway centrality predict retention of a newly adopted concept beyond B5, field size, phi(home,j), relatedness density, the field's leave-concept-out retention propensity P_j(-c), coverage and episode size?) and H3 (does gateway-weighted early landing G predict size-adjusted breadth O2r_resid given B5?).

  Data: one zero-credit scan of all 2,040 OpenAlex S3 works files (2026-09-23; 476,196,327 works; 129.4M base works 1995-2022), with Aho-Corasick title matching of 56,643 legacy concepts (levels 2-5) plus Wikidata aliases and stemmed verification: 60.0M verified matches. Grounding: legacy-tag rule TAG (test P 0.947, R 0.659), chosen on a 390-pair LLM benchmark with 60 hand-checked pairs (90% agreement), plus a per-concept LLM precision gate ($2.28 of OpenRouter).

  Authoritative S1 tables for iteration 3: frame_concepts.csv (12,499 concepts: DEV 4,771, held-out PHYS/LIFEENV/SOC/MATHDEC 742/1,113/1,352/165, cohort 4,356), episodes.csv (27,393 concept x off-home-field episodes with R and the R_abs1-3 sensitivity outcomes for all splits), concept_outcomes.csv (O1, O3, O2r_m30/m50) and concept_features_basic.csv (G, G_A, G_btw, REL_home, RS, DOM_*, count/label indicators, B5).

  The spec was frozen on DEV (sha256 in logs/seal.log) and unsealed once. H1: held-out dAUC -0.00001 [-0.0006, +0.0003] (DEV +0.00001), DL pooled -0.00004 (I2 = 0), cohort -0.0001. The placebo was not exceeded and the conditional logit is null. Verdict: DISCONFIRMED. Power: the minimum detectable dAUC is 0.004. The relatedness pair beats gateway on held-out (+0.0034 [0.0010, 0.0051] vs 0). The baseline ladder shows gateway's DEV signal (+0.0019 over the iteration-1 base) vanishes once P_j(-c) is added, and reverses on held-out (-0.0016). Gateway alone has AUC 0.605 on DEV vs 0.506 on held-out (0.41 in SOC): gateway is a domain-specific proxy for 'fields that keep things'. Iteration-1 replication: +0.023 (vs +0.10). H3: held-out partial rho G 0.030 / G_A 0.026 / G_btw 0.046 (Holm p = 0.0045); within-group DL pooled G 0.068 [0.029, 0.107]. The effect is small; the tests show 0/40 false positives on shuffled outcomes. REL_home is strongly negative (-0.14).

  An independent audit (sklearn, own AUC) matches to 1e-6. Deviations: no OpenAlex API audit or insularity (credits exhausted); LLM cap raised to $3.50; T3 t0 agreement 53%. See README.md, results/*.json and figures/.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-2/experiment-5/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-2/experiment-5/demo/mini_demo_data.json"
import json
from pathlib import Path

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    local = Path("mini_demo_data.json")
    if local.exists(): return json.loads(local.read_text())
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.
`UV_VENV_CLEAR=1` recreates the venv empty at the start of every test, so each test starts clean. Do NOT delete it yourself: the pipeline removes it after you finish. If you run a test in the background, wait for its result before starting the next test.

What happens: the venv starts with only pip, jupyter and ipykernel. When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-2/experiment-5/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] TOOL CALL — Skill · 2026-09-30 01:37:54 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-30 01:37:54 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-30 01:37:54 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-30 01:37:54 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-30 01:37:56 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls -la $A; du -sh $A/* | sort -h | tail -20; wc -l $A/method.py; ls -la; ls .aii
```

### [8] TOOL RESULT — Bash · 2026-09-30 01:37:58 UTC

```
{"stdout": "total 173386\ndrwxrwxrwx 10 aii-agent aii-agent  2077382 Sep 28 21:17 .\ndrwxrwxrwx  7 aii-agent aii-agent  3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 aii-agent aii-agent  1000130 Sep 28 19:41 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 28 17:08 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent    10057 Sep 28 19:41 .aii_worker_result.json\ndrwxrwxrwx  8 aii-agent aii-agent  2000761 Sep 28 19:31 .git\n-rw-rw-rw-  1 aii-agent aii-agent       42 Sep 28 17:57 .gitignore\n-rw-rw-rw-  1 aii-agent aii-agent  1481575 Sep 28 19:41 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     3255 Sep 28 19:31 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    20911 Sep 28 19:36 README.md\n-rw-rw-rw-  1 aii-agent aii-agent     3230 Sep 28 19:06 audit.json\n-rw-rw-rw-  1 aii-agent aii-agent     6020 Sep 28 18:21 audit.py\n-rw-rw-rw-  1 aii-agent aii-agent     6848 Sep 28 19:13 audit_placebo.py\n-rw-rw-rw-  1 aii-agent aii-agent     6825 Sep 28 17:39 backbones.py\n-rw-rw-rw-  1 aii-agent aii-agent     8526 Sep 28 17:49 checks.py\n-rw-rw-rw-  1 aii-agent aii-agent  5322082 Sep 28 18:57 cohort_episodes_with_pred.csv\n-rw-rw-rw-  1 aii-agent aii-agent    10717 Sep 28 19:20 common.py\n-rw-rw-rw-  1 aii-agent aii-agent  5196667 Sep 28 18:36 concept_features_basic.csv\n-rw-rw-rw-  1 aii-agent aii-agent   920533 Sep 28 18:48 concept_outcomes.csv\n-rw-rw-rw-  1 aii-agent aii-agent      123 Sep 28 17:38 credits_log.csv\n-rw-rw-rw-  1 aii-agent aii-agent  4733254 Sep 28 18:47 dev_episodes_with_oof.csv\n-rw-rw-rw-  1 aii-agent aii-agent 12358267 Sep 28 18:36 episode_features.csv\n-rw-rw-rw-  1 aii-agent aii-agent  4038818 Sep 28 18:48 episodes.csv\n-rw-rw-rw-  1 aii-agent aii-agent     3401 Sep 28 19:05 exploratory_domains.py\n-rw-rw-rw-  1 aii-agent aii-agent     8968 Sep 28 17:42 features.py\ndrwxrwxrwx  2 aii-agent aii-agent  1083930 Sep 28 19:01 figures\n-rw-rw-rw-  1 aii-agent aii-agent     1705 Sep 28 18:59 fix_pigeonhole.py\n-rw-rw-rw-  1 aii-agent aii-agent    12798 Sep 28 17:35 frame.py\n-rw-rw-rw-  1 aii-agent aii-agent  2290579 Sep 28 18:36 frame_concepts.csv\n-rw-rw-rw-  1 aii-agent aii-agent      252 Sep 28 17:37 frozen_lexicon.sha256\n-rw-rw-rw-  1 aii-agent aii-agent   109036 Sep 28 18:47 frozen_spec.json\n-rw-rw-rw-  1 aii-agent aii-agent 28377355 Sep 28 19:11 full_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    18349 Sep 28 19:20 grounding.py\n-rw-rw-rw-  1 aii-agent aii-agent   100286 Sep 28 18:14 grounding_benchmark.csv\n-rw-rw-rw-  1 aii-agent aii-agent   733111 Sep 28 19:31 grounding_precision.csv\n-rw-rw-rw-  1 aii-agent aii-agent     2585 Sep 28 18:19 grounding_report.json\n-rw-rw-rw-  1 aii-agent aii-agent  4679702 Sep 28 18:57 heldout_episodes_with_pred.csv\n-rw-rw-rw-  1 aii-agent aii-agent     4427 Sep 28 17:16 lexicon.py\n-rw-rw-rw-  1 aii-agent aii-agent  5464978 Sep 28 17:16 lexicon_v0.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  8354825 Sep 28 17:37 lexicon_v1.parquet\n-rw-rw-rw-  1 aii-agent aii-agent     5823 Sep 28 18:13 llm.py\n-rw-rw-rw-  1 aii-agent aii-agent   918507 Sep 28 18:30 llm_cost_log.csv\ndrwxrwxrwx  2 aii-agent aii-agent  1008735 Sep 28 19:04 logs\n-rw-rw-rw-  1 aii-agent aii-agent      879 Sep 28 19:02 make_variants.py\n-rw-rw-rw-  1 aii-agent aii-agent     1509 Sep 28 17:16 matcher.py\n-rw-rw-rw-  1 aii-agent aii-agent     4192 Sep 28 19:20 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 26650987 Sep 28 19:01 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    18739 Sep 28 19:11 mini_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    47860 Sep 28 18:59 models.py\n-rw-rw-rw-  1 aii-agent aii-agent     3866 Sep 28 18:13 oa_client.py\n-rw-rw-rw-  1 aii-agent aii-agent     4181 Sep 28 19:20 panel.py\n-rw-rw-rw-  1 aii-agent aii-agent    41728 Sep 28 18:13 placebo_gateways.npy\n-rw-rw-rw-  1 aii-agent aii-agent    41728 Sep 28 18:13 placebo_perm_gateways.npy\n-rw-rw-rw-  1 aii-agent aii-agent    11028 Sep 28 19:20 prescreen.py\n-rw-rw-rw-  1 aii-agent aii-agent    15150 Sep 28 19:11 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     1486 Sep 28 17:12 probe.py\n-rw-rw-rw-  1 aii-agent aii-agent     2160 Sep 28 19:12 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent     5326 Sep 28 17:09 rangefile.py\n-rw-rw-rw-  1 aii-agent aii-agent    13493 Sep 28 19:01 report.py\n-rw-rw-rw-  1 aii-agent aii-agent     8210 Sep 28 19:31 reproducibility.md\n-rwxrwxrwx  1 aii-agent aii-agent     1086 Sep 28 19:16 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent  2000415 Sep 28 19:13 results\ndrwxrwxrwx  8 aii-agent aii-agent  2059831 Sep 28 21:17 scan\n-rw-rw-rw-  1 aii-agent aii-agent    15148 Sep 28 19:21 scan_full.py\n-rw-rw-rw-  1 aii-agent aii-agent     5176 Sep 28 17:46 seal.py\n-rw-rw-rw-  1 aii-agent aii-agent 12891109 Sep 28 18:48 sens_episodes_b5_t0p4.csv\n-rw-rw-rw-  1 aii-agent aii-agent 17928388 Sep 28 18:48 sens_episodes_match.csv\n-rw-rw-rw-  1 aii-agent aii-agent 17356255 Sep 28 18:48 sens_episodes_ptopic.csv\n-rw-rw-rw-  1 aii-agent aii-agent     3256 Sep 28 18:17 sense_filter.joblib\ndrwxrwxrwx  3 aii-agent aii-agent  2000995 Sep 28 17:12 snapshot\ndrwxrwxrwx  2 aii-agent aii-agent  1000748 Sep 28 17:46 tests\n-rw-rw-rw-  1 aii-agent aii-agent     1335 Sep 28 17:13 timing_probe.py\n-rw-rw-rw-  1 aii-agent aii-agent     5678 Sep 28 17:22 wikidata_aliases.py\n985K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/tests\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/logs\n1.9M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/figures\n2.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv\n3.9M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/episodes.csv\n4.5M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/heldout_episodes_with_pred.csv\n4.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/dev_episodes_with_oof.csv\n5.0M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/concept_features_basic.csv\n5.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/cohort_episodes_with_pred.csv\n5.3M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/lexicon_v0.parquet\n6.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results\n8.0M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/lexicon_v1.parquet\n12M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/episode_features.csv\n13M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/sens_episodes_b5_t0p4.csv\n14M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/snapshot\n17M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/sens_episodes_ptopic.csv\n18M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/sens_episodes_match.csv\n26M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/method_out.json\n28M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/full_method_out.json\n617M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan\n83 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/method.py\ntotal 1986\ndrwxrwxrwx 3 aii-agent aii-agent 1002567 Sep 30 01:37 .\ndrwxrwxrwx 4 aii-agent aii-agent 1002569 Sep 30 01:36 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 01:36 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 01:37 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   26239 Sep 30 01:37 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-30 01:38:00 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cat $A/method.py; echo ----; cat $A/common.py; echo ----; cat $A/pyproject.toml; head -c 3000 $A/preview_method_out.json
```

### [10] TOOL RESULT — Bash · 2026-09-30 01:38:00 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"End-to-end orchestrator: runs every step of the held-out gateway-retention test in order.\n\n  lexicon -> prescreen (sample, names, wikidata aliases, aliases) -> full scan (+ merge) -> onset candidates (match)\n  -> backbones -> grounding benchmark -> sense filter -> onset candidates (grounded) -> precision gate -> frame\n  -> features -> T0 tests -> T1/T3 checks -> dev analysis + FREEZE -> UNSEAL (once) -> held-out scoring (+ H3)\n  -> replication -> figures + method_out.json -> variants -> independent audit\n\nSteps whose main output already exists are skipped (idempotent), so `python method.py` resumes; `--from STEP`\nreruns from a step (the seal refuses a second unseal: the held-out steps can be rerun only after unsealing\nonce, and never re-freeze after an unseal). The step `handcheck` needs the executor's labels in\nresults/handcheck_labels.csv (kept in the repository).\n\nUsage: python method.py [--from STEP] [--only STEP]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport subprocess\nimport sys\nimport time\n\nfrom common import LOGS, RES, ROOT, SCAN, setup_logger\n\nlogger = setup_logger(\"method\")\nPY = sys.executable\nSTEPS = [\n    (\"lexicon\", [\"lexicon.py\"], ROOT / \"lexicon_v0.parquet\"),\n    (\"prescreen_sample\", [\"prescreen.py\", \"sample\"], SCAN / \"sample_titles\" / \"part_001.parquet\"),\n    (\"prescreen_names\", [\"prescreen.py\", \"names\"], SCAN / \"prescreen_survivors.parquet\"),\n    (\"wikidata\", [\"wikidata_aliases.py\"], SCAN / \"wikidata_aliases.json\"),\n    (\"prescreen_aliases\", [\"prescreen.py\", \"aliases\"], ROOT / \"lexicon_v1.parquet\"),\n    (\"scan\", [\"scan_full.py\", \"--workers\", \"5\"], None),\n    (\"merge\", [\"scan_full.py\", \"--merge\"], SCAN / \"agg_counts.parquet\"),\n    (\"onset_match\", [\"frame.py\", \"match\"], RES / \"onset_candidates_match.csv\"),\n    (\"backbones\", [\"backbones.py\"], RES / \"backbones.json\"),\n    (\"bench\", [\"grounding.py\", \"bench\"], ROOT / \"grounding_benchmark.csv\"),\n    (\"filter\", [\"grounding.py\", \"filter\"], ROOT / \"grounding_report.json\"),\n    (\"onset_grounded\", [\"frame.py\", \"grounded\"], RES / \"onset_candidates_grounded.csv\"),\n    (\"precision\", [\"grounding.py\", \"precision\"], ROOT / \"grounding_precision.csv\"),\n    (\"frame\", [\"frame.py\", \"build\"], ROOT / \"frame_concepts.csv\"),\n    (\"features\", [\"features.py\"], ROOT / \"episode_features.csv\"),\n    (\"tests\", [\"tests/test_units.py\"], RES / \"unit_tests_T0.json\"),\n    (\"t1\", [\"checks.py\", \"t1\"], None),\n    (\"t3\", [\"checks.py\", \"t3\"], RES / \"p78_agreement.csv\"),\n    (\"dev_freeze\", [\"models.py\", \"dev\"], ROOT / \"frozen_spec.json\"),\n    (\"unseal\", [\"seal.py\", \"unseal\"], ROOT / \"sens_episodes_b5_t0p4.csv\"),\n    (\"heldout\", [\"models.py\", \"heldout\"], RES / \"h3_results.json\"),\n    (\"pigeonhole_fix\", [\"fix_pigeonhole.py\"], None),\n    (\"replicate\", [\"checks.py\", \"replicate\"], None),\n    (\"exploratory_domains\", [\"exploratory_domains.py\"], RES / \"exploratory_domain_specificity.json\"),\n    (\"report\", [\"report.py\"], ROOT / \"method_out.json\"),\n    (\"variants\", [\"make_variants.py\"], ROOT / \"preview_method_out.json\"),\n    (\"audit\", [\"audit.py\"], ROOT / \"audit.json\"),\n    (\"audit_placebo\", [\"audit_placebo.py\"], RES / \"audit_placebo.json\"),\n]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--from\", dest=\"start\", default=None)\n    ap.add_argument(\"--only\", default=None)\n    args = ap.parse_args()\n    names = [s[0] for s in STEPS]\n    i0 = names.index(args.start) if args.start else 0\n    for name, cmd, out in STEPS[i0:]:\n        if args.only and name != args.only:\n            continue\n        forced = bool(args.start or args.only)\n        if out is not None and out.exists() and not forced:\n            logger.info(f\"[skip] {name}: {out.relative_to(ROOT)} exists\")\n            continue\n        t = time.time()\n        logger.info(f\"[run ] {name}: {' '.join(cmd)}\")\n        r = subprocess.run([PY] + cmd, cwd=ROOT)\n        if r.returncode != 0:\n            logger.error(f\"{name} failed with exit code {r.returncode}\")\n            raise SystemExit(r.returncode)\n        logger.info(f\"[done] {name} in {time.time()-t:.0f}s\")\n    (LOGS / \"method_last_run.txt\").write_text(time.strftime(\"%Y-%m-%d %H:%M:%S\"))\n\n\nif __name__ == \"__main__\":\n    main()\n----\n\"\"\"Shared constants, paths, the OpenAlex-like title analyser (copied verbatim from art_yrradSC27HtQ\nscan_snapshot.py) and small helpers used by every step of the pipeline.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport re\nimport sys\nfrom functools import lru_cache\nfrom pathlib import Path\n\nimport numpy as np\n\nROOT = Path(__file__).resolve().parent\n\n\ndef _dep_dir(env: str, artifact_id: str, run_tree_rel: str) -> Path:\n    \"\"\"Input artifact directory: env var override, else the run tree (pipeline layout), else the sibling folder\n    of the published repository named by the artifact id.\"\"\"\n    import os\n    if os.environ.get(env):\n        return Path(os.environ[env])\n    run_tree = ROOT.parents[3] / run_tree_rel\n    return run_tree if run_tree.exists() else ROOT.parent / artifact_id\n\n\n# iteration-1 inputs (read-only): art_yrradSC27HtQ (scan/analyser/source-field map), art_33_KKk_G8Gw5 (frozen backbone)\nART3 = _dep_dir(\"AII_ART_YRRAD_DIR\", \"art_yrradSC27HtQ\", \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\nART33 = _dep_dir(\"AII_ART_33_DIR\", \"art_33_KKk_G8Gw5\", \"3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\nSNAP = ROOT / \"snapshot\"\nSCAN = ROOT / \"scan\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nfor _d in (SNAP, SCAN, RES, LOGS, FIGS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nFIELD_IDS = list(range(11, 37))            # the 26 OpenAlex fields; index k = fid - 11; vfield code = k + 1 (0 = unlabelled)\nFIELD_NAMES = {11: \"Agricultural and Biological Sciences\", 12: \"Arts and Humanities\",\n               13: \"Biochemistry, Genetics and Molecular Biology\", 14: \"Business, Management and Accounting\",\n               15: \"Chemical Engineering\", 16: \"Chemistry\", 17: \"Computer Science\", 18: \"Decision Sciences\",\n               19: \"Earth and Planetary Sciences\", 20: \"Economics, Econometrics and Finance\", 21: \"Energy\",\n               22: \"Engineering\", 23: \"Environmental Science\", 24: \"Immunology and Microbiology\",\n               25: \"Materials Science\", 26: \"Mathematics\", 27: \"Medicine\", 28: \"Neuroscience\", 29: \"Nursing\",\n               30: \"Pharmacology, Toxicology and Pharmaceutics\", 31: \"Physics and Astronomy\", 32: \"Psychology\",\n               33: \"Social Sciences\", 34: \"Veterinary\", 35: \"Dentistry\", 36: \"Health Professions\"}\n# fixed before any data were seen (plan step 5)\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nDOMAIN_OF = {11: \"Life\", 13: \"Life\", 24: \"Life\", 28: \"Life\", 30: \"Life\",\n             12: \"Social\", 14: \"Social\", 18: \"Social\", 20: \"Social\", 32: \"Social\", 33: \"Social\",\n             15: \"Physical\", 16: \"Physical\", 17: \"Physical\", 19: \"Physical\", 21: \"Physical\", 22: \"Physical\",\n             23: \"Physical\", 25: \"Physical\", 26: \"Physical\", 31: \"Physical\",\n             27: \"Health\", 29: \"Health\", 34: \"Health\", 35: \"Health\", 36: \"Health\"}\nMTYPES = [\"name_exact\", \"name_variant\", \"alias\"]\n\n# ----------------------------------------------------------------------------- analyser (verbatim from art_yrradSC27HtQ)\nES_STOP = set(\"a an and are as at be but by for if in into is it no not of on or such that the their then there \"\n              \"these they this to was will with\".split())\nTOKEN_RE = re.compile(r\"[^\\W_]+(?:\\.[^\\W_]+)*\", re.UNICODE)\n_STEMMER = None\n\n\ndef _stem(w: str) -> str:\n    global _STEMMER\n    if _STEMMER is None:\n        import snowballstemmer\n        _STEMMER = snowballstemmer.stemmer(\"porter\")\n    return _cached_stem(w)\n\n\n@lru_cache(maxsize=500_000)\ndef _cached_stem(w: str) -> str:\n    return _STEMMER.stemWord(w)\n\n\ndef normalise(text: str) -> str:\n    t = text.lower().replace(\"’\", \"'\")\n    t = re.sub(r\"'s\\b\", \"\", t)\n    return re.sub(r\"[\\-‐‑‒–—/]\", \" \", t)\n\n\ndef analyse(text: str) -> list[tuple[int, str]]:\n    \"\"\"(position, stem) for non-stop tokens; stop words keep their position slot (ES semantics).\"\"\"\n    out = []\n    for p, tok in enumerate(TOKEN_RE.findall(normalise(text))):\n        if tok in ES_STOP:\n            continue\n        out.append((p, _stem(tok)))\n    return out\n\n\ndef phrase_spec(phrase: str) -> tuple[tuple[int, str], ...]:\n    a = analyse(phrase)\n    if not a:\n        return ()\n    p0 = a[0][0]\n    return tuple((p - p0, s) for p, s in a)\n\n\ndef spec_in(pos: dict[str, list[int]], spec) -> bool:\n    \"\"\"match_title logic for one spec against a title's {stem: [positions]} index.\"\"\"\n    if not spec:\n        return False\n    first = spec[0][1]\n    for p0 in pos.get(first, ()):\n        if all(p0 + off in pos.get(s, ()) for off, s in spec[1:]):\n            return True\n    return False\n\n\ndef title_pos(title: str) -> dict[str, list[int]]:\n    pos: dict[str, list[int]] = {}\n    for p, s in analyse(title):\n        pos.setdefault(s, []).append(p)\n    return pos\n\n\n# ----------------------------------------------------------------------------- surface normalisation for Aho-Corasick\n_WS = re.compile(r\"\\s+\")\n_NONWORD = re.compile(r\"[^\\w\\s]\")\n\n\ndef surf(text: str) -> str:\n    \"\"\"Surface normalisation used for AC keys AND titles: lowercase, possessive strip, hyphen/slash -> space,\n    other punctuation -> space, collapse whitespace, pad with single spaces.\"\"\"\n    t = normalise(text)\n    t = _NONWORD.sub(\" \", t).replace(\"_\", \" \")\n    return \" \" + _WS.sub(\" \", t).strip() + \" \"\n\n\ndef surf_arrow(arr):\n    \"\"\"Vectorised (pyarrow) version of surf() for a string array.\"\"\"\n    import pyarrow.compute as pc\n    t = pc.utf8_lower(pc.fill_null(arr, \"\"))\n    t = pc.replace_substring(t, \"’\", \"'\")\n    t = pc.replace_substring_regex(t, r\"'s\\b\", \"\")\n    t = pc.replace_substring_regex(t, r\"[\\-‐‑‒–—/]\", \" \")\n    t = pc.replace_substring_regex(t, r\"[^\\w\\s]|_\", \" \")\n    t = pc.replace_substring_regex(t, r\"\\s+\", \" \")\n    t = pc.utf8_trim_whitespace(t)\n    return pc.binary_join_element_wise(pc.cast(\" \", \"string\"), t, pc.cast(\" \", \"string\"), \"\")\n\n\ndef plural_variants(form: str) -> set[str]:\n    \"\"\"Singular/plural variants of the LAST token (s | es | ies).\"\"\"\n    toks = form.split(\" \")\n    last = toks[-1]\n    out = {last}\n    if len(last) >= 4:\n        if last.endswith(\"ies\"):\n            out.add(last[:-3] + \"y\")\n        elif last.endswith(\"es\") and last[:-2].endswith((\"s\", \"x\", \"z\", \"ch\", \"sh\")):\n            out.add(last[:-2])\n        elif last.endswith(\"s\") and not last.endswith(\"ss\") and not last.endswith(\"us\") and not last.endswith(\"is\"):\n            out.add(last[:-1])\n        else:\n            if last.endswith(\"y\") and last[-2:-1] not in \"aeiou\":\n                out.add(last[:-1] + \"ies\")\n            elif last.endswith((\"s\", \"x\", \"z\", \"ch\", \"sh\")):\n                out.add(last + \"es\")\n            else:\n                out.add(last + \"s\")\n    return {\" \".join(toks[:-1] + [v]) for v in out}\n\n\n# ----------------------------------------------------------------------------- misc\ndef jdump(obj, path: Path) -> None:\n    def conv(o):\n        if isinstance(o, (np.integer,)):\n            return int(o)\n        if isinstance(o, (np.floating,)):\n            return None if not np.isfinite(o) else float(o)\n        if isinstance(o, np.ndarray):\n            return o.tolist()\n        if isinstance(o, float) and not math.isfinite(o):\n            return None\n        return str(o)\n\n    def clean(o):\n        if isinstance(o, dict):\n            return {str(k): clean(v) for k, v in o.items()}\n        if isinstance(o, (list, tuple)):\n            return [clean(v) for v in o]\n        if isinstance(o, float) and not math.isfinite(o):\n            return None\n        if isinstance(o, (np.floating,)):\n            return None if not np.isfinite(o) else float(o)\n        return o\n    path.write_text(json.dumps(clean(obj), indent=1, default=conv))\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef add_deviation(key: str, text: str) -> None:\n    p = RES / \"deviations.json\"\n    d = json.loads(p.read_text()) if p.exists() else {}\n    d[key] = text\n    p.write_text(json.dumps(d, indent=1))\n\n\ndef source_field_lut() -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"(sorted source ids, vfield code 0..26) from art_yrradSC27HtQ results/source_field.parquet.\"\"\"\n    import pandas as pd\n    p = RES / \"source_field.parquet\"\n    if not p.exists():\n        import shutil\n        shutil.copy(ART3 / \"results/source_field.parquet\", p)\n    sf = pd.read_parquet(p)\n    sid = sf.source.to_numpy(np.int64)\n    code = np.where(sf.field.isna(), 0, sf.field.fillna(11).astype(int) - 10).astype(np.int8)\n    o = np.argsort(sid)\n    return sid[o], code[o]\n\n\ndef works_files() -> list[tuple[int, str, int, int]]:\n    man = json.loads((SNAP / \"works_manifest.json\").read_text())\n    return [(i, f[\"url\"].replace(\"s3://openalex/\", \"\"), f[\"meta\"][\"content_length\"], f[\"meta\"][\"record_count\"])\n            for i, f in enumerate(man[\"files\"])]\n\n\n# ----------------------------------------------------------------------------- split parquet storage (< 100 MB per file)\ndef write_parquet_parts(df, out_dir: Path, rows_per_part: int = 400_000) -> list[Path]:\n    \"\"\"Write a DataFrame as out_dir/part_001.parquet, part_002.parquet, ... (zstd). Existing parts are replaced.\"\"\"\n    out_dir.mkdir(parents=True, exist_ok=True)\n    for old in out_dir.glob(\"part_*.parquet\"):\n        old.unlink()\n    paths = []\n    for k, i in enumerate(range(0, max(len(df), 1), rows_per_part), start=1):\n        p = out_dir / f\"part_{k:03d}.parquet\"\n        df.iloc[i:i + rows_per_part].to_parquet(p, index=False, compression=\"zstd\")\n        paths.append(p)\n    return paths\n\n\ndef read_parquet_parts(out_dir: Path, columns: list[str] | None = None):\n    \"\"\"Read the parts written by write_parquet_parts in sorted order and concatenate them.\"\"\"\n    import pandas as pd\n    parts = sorted(out_dir.glob(\"part_*.parquet\"))\n    if not parts:\n        raise FileNotFoundError(f\"no parquet parts in {out_dir}\")\n    return pd.concat([pd.read_parquet(p, columns=columns) for p in parts], ignore_index=True)\n\n\nRESERVOIR_DIR = SCAN / \"reservoir\"          # was scan/reservoir.parquet (136 MB)\nSAMPLE_TITLES_DIR = SCAN / \"sample_titles\"  # was scan/sample_titles.parquet (152 MB)\n----\n[project]\nname = \"gateway-retention-heldout\"\nversion = \"0.1.0\"\ndescription = \"Sealed held-out test of adopting-field gateway centrality for concept retention on the full OpenAlex snapshot\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n    \"aiohappyeyeballs==2.7.1\",\n    \"aiohttp==3.14.3\",\n    \"aiosignal==1.4.0\",\n    \"annotated-doc==0.0.5\",\n    \"anyio==4.15.1\",\n    \"attrs==26.1.0\",\n    \"certifi==2026.7.22\",\n    \"charset-normalizer==3.5.1\",\n    \"click==8.5.0\",\n    \"cloudpickle==3.1.2\",\n    \"contourpy==1.4.0\",\n    \"cycler==0.12.1\",\n    \"filelock==3.32.3\",\n    \"fonttools==4.66.0\",\n    \"formulaic==1.2.2\",\n    \"frozenlist==1.8.0\",\n    \"fsspec==2026.7.0\",\n    \"h11==0.16.0\",\n    \"hf-xet==1.6.0\",\n    \"httpcore==1.0.9\",\n    \"httpx==0.28.1\",\n    \"huggingface-hub==1.33.0\",\n    \"idna==3.20\",\n    \"interface-meta==2.0.1\",\n    \"jinja2==3.1.6\",\n    \"joblib==1.6.0\",\n    \"kiwisolver==1.5.1\",\n    \"linearmodels==7.0\",\n    \"loguru==0.7.3\",\n    \"markdown-it-py==4.2.0\",\n    \"markupsafe==3.0.3\",\n    \"matplotlib==3.11.2\",\n    \"mdurl==0.1.2\",\n    \"mpmath==1.3.0\",\n    \"multidict==6.9.1\",\n    \"mypy-extensions==1.1.0\",\n    \"narwhals==2.26.0\",\n    \"networkx==3.7\",\n    \"numpy==2.5.3\",\n    \"packaging==26.3\",\n    \"pandas==3.0.6\",\n    \"patsy==1.0.3\",\n    \"pillow==12.3.0\",\n    \"propcache==0.5.4\",\n    \"pyahocorasick==2.3.1\",\n    \"pyarrow==25.0.1\",\n    \"pygments==2.21.0\",\n    \"pyhdfe==0.2.0\",\n    \"pyparsing==3.3.3\",\n    \"python-dateutil==2.9.0.post0\",\n    \"pyyaml==6.0.3\",\n    \"regex==2026.9.10\",\n    \"requests==2.34.2\",\n    \"rich==15.0.0\",\n    \"safetensors==0.8.0\",\n    \"scikit-learn==1.9.1\",\n    \"scipy==1.18.1\",\n    \"sentence-transformers==6.1.0\",\n    \"setuptools==78.1.0\",\n    \"shellingham==1.5.4\",\n    \"six==1.17.0\",\n    \"snowballstemmer==3.1.1\",\n    \"statsmodels==0.15.0\",\n    \"sympy==1.14.0\",\n    \"tenacity==9.1.4\",\n    \"threadpoolctl==3.7.0\",\n    \"tokenizers==0.23.2\",\n    \"torch==2.14.0+cpu\",\n    \"tqdm==4.70.1\",\n    \"transformers==5.17.0\",\n    \"typer==0.27.2\",\n    \"typing-extensions==4.16.0\",\n    \"urllib3==2.8.0\",\n    \"wrapt==2.5.0\",\n    \"yarl==1.25.1\",\n]\n\n# torch is the CPU build: uv pip install torch==<pinned> --index-url https://download.pytorch.org/whl/cpu\n{\n  \"metadata\": {\n    \"method_name\": \"Held-out test of adopting-field gateway centrality for concept retention (H1) and concept-level gateway landing vs size-adjusted breadth (H3)\",\n    \"description\": \"One zero-credit scan of the full OpenAlex works snapshot (2,040 parquet files); legacy concept lexicon (levels 2-5) + Wikidata aliases; Aho-Corasick title matching with stemmed verification; grounding...\",\n    \"baseline\": \"X0 = B5 + log field size + phi(home,j) + relatedness density + P_j(-c) + coverage + episode size\",\n    \"method\": \"X1 = X0 + frozen 1998-2002 eigenvector gateway centrality of the adopting field\",\n    \"frame\": {\n      \"ladder\": [\n        {\n          \"early_min\": 30,\n          \"weak_home\": true,\n          \"n_concepts\": 12499,\n          \"n_episodes\": 27393\n        }\n      ],\n      \"n_concepts\": 12499,\n      \"n_episodes\": 27393,\n      \"by_split\": {\n        \"DEV\": 4771,\n        \"COHORT\": 4356,\n        \"HELDOUT_SOC\": 1352,\n        \"HELDOUT_LIFEENV\": 1113,\n        \"HELDOUT_PHYS\": 742,\n        \"HELDOUT_MATHDEC\": 165\n      },\n      \"episodes_by_split\": {\n        \"COHORT\": 9799,\n        \"DEV\": 9079,\n        \"HELDOUT_SOC\": 3320,\n        \"HELDOUT_LIFEENV\": 3099,\n        \"HELDOUT_PHYS\": 1662,\n        \"HELDOUT_MATHDEC\": 434\n      },\n      \"by_group\": {\n        \"Med\": 3868,\n        \"SOC\": 2211,\n        \"Eng\": 2087,\n        \"LIFEENV\": 1668,\n        \"PHYS\": 1097,\n        \"BGM\": 719,\n        \"CS\": 581,\n        \"MATHDEC\": 268\n      },\n      \"newborn_share\": 0.05392431394511561,\n      \"weak_home\": 1150,\n      \"intersect40\": 502,\n      \"dev_R_rate\": 0.29364467452362597\n    },\n    \"grounding\": {\n      \"frozen_grounding_rule\": \"c_TAG\",\n      \"kappa_l1_l2\": 0.199518587857716,\n      \"rules_test\": {\n        \"a_stemmed_any\": {\n          \"precision\": 0.8541666666666666,\n          \"recall\": 1.0,\n          \"f1\": 0.9213483146067416,\n          \"n_pred_pos\": 96\n        },\n        \"b_exact_name_only\": {\n          \"precision\": 0.8717948717948718,\n          \"recall\": 0.4146341463414634,\n          \"f1\": 0.5619834710743802,\n          \"n_pred_pos\": 39\n        },\n        \"c_TAG\": {\n          \"precision\": 0.9473684210526315,\n          \"recall\": 0.6585365853658537,\n          \"f1\": 0.776978417266187,\n          \"n_pred_pos\": 57\n        },\n        \"d_filter_p05\": {\n          \"precision\": 0.8617021276595744,\n          \"recall\": 0.9878048780487805,\n          \"f1\": 0.9204545454545454,\n          \"n_pred_pos\": 94\n        },\n        \"e_TAG_or_untagged_filter\": {\n          \"precision\": 0.9384615384615385,\n          \"recall\": 0.7439024390243902,\n          \"f1\": 0.8299319727891157,\n          \"n_pred_pos\": 65\n        }\n      },\n      \"handcheck\": {\n        \"n\": 60,\n        \"agree_with_gold\": 0.9,\n        \"agree_with_L1\": 0.8833333333333333\n      },\n      \"filter\": {\n        \"C\": 0.1,\n        \"test_auc\": 0.8710801393728222,\n        \"coef\": {\n          \"cos\": 0.917,\n          \"single_token\": -0.177,\n          \"is_alias\": -0.272,\n          \"is_variant\": 0.169,\n          \"ts1\": 0.216,", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-30 01:38:06 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cd $A; python3 -c "
import json
d=json.load(open('preview_method_out.json'))
def walk(o,p='',depth=0):
    if depth>3: return
    if isinstance(o,dict):
        for k,v in o.items():
            print('  '*depth+k, type(v).__name__, (len(v) if hasattr(v,'__len__') else v) if not isinstance(v,(int,float)) else v)
            walk(v,p+'.'+k,depth+1)
walk(d)
" | head -150; head -3 episodes.csv; head -3 episode_features.csv | cut -c1-1500; head -3 concept_features_basic.csv | cut -c1-800
```

### [12] TOOL RESULT — Bash · 2026-09-30 01:38:06 UTC

```
{"stdout": "metadata dict 13\n  method_name str 141\n  description str 203\n  baseline str 96\n  method str 79\n  frame dict 10\n    ladder list 1\n    n_concepts int 12499\n    n_episodes int 27393\n    by_split dict 6\n      DEV int 4771\n      COHORT int 4356\n      HELDOUT_SOC int 1352\n      HELDOUT_LIFEENV int 1113\n      HELDOUT_PHYS int 742\n      HELDOUT_MATHDEC int 165\n    episodes_by_split dict 6\n      COHORT int 9799\n      DEV int 9079\n      HELDOUT_SOC int 3320\n      HELDOUT_LIFEENV int 3099\n      HELDOUT_PHYS int 1662\n      HELDOUT_MATHDEC int 434\n    by_group dict 8\n      Med int 3868\n      SOC int 2211\n      Eng int 2087\n      LIFEENV int 1668\n      PHYS int 1097\n      BGM int 719\n      CS int 581\n      MATHDEC int 268\n    newborn_share float 0.05392431394511561\n    weak_home int 1150\n    intersect40 int 502\n    dev_R_rate float 0.29364467452362597\n  grounding dict 5\n    frozen_grounding_rule str 5\n    kappa_l1_l2 float 0.199518587857716\n    rules_test dict 5\n      a_stemmed_any dict 4\n      b_exact_name_only dict 4\n      c_TAG dict 4\n      d_filter_p05 dict 4\n      e_TAG_or_untagged_filter dict 4\n    handcheck dict 3\n      n int 60\n      agree_with_gold float 0.9\n      agree_with_L1 float 0.8833333333333333\n    filter dict 3\n      C float 0.1\n      test_auc float 0.8710801393728222\n      coef dict 9\n  H1_dev dict 9\n    n_episodes int 9079\n    n_concepts int 3987\n    R_rate float 0.29364467452362597\n    dauc float 1.3686565255799366e-05\n    ci95 list 2\n    per_group dict 4\n      CS float 2.341783267956199e-05\n      Eng float 9.334665149218768e-05\n      BGM float 0.00010189060702647801\n      Med float -5.499642523210113e-05\n    placebo_real_exceeds_p95 bool False\n    cond_logit dict 9\n      n_episodes_informative int 4671\n      n_concepts_informative int 1470\n      beta_gateway_std float 0.05760821669635307\n      se float 0.050620675092339903\n      z float 1.138037305730649\n      p_two_sided float 0.2551049050718702\n      LR float 1.2934423734448046\n      LR_p float 0.2554145329529829\n      method str 16\n    lpm dict 7\n      n int 9079\n      within_field_sd_of_regressor float 0.025486300560656133\n      beta_within_per_sd float -0.00345886836143571\n      se_concept float 0.03468988448996966\n      p_concept float 0.9205759349273591\n      se_twoway float 0.07500050998634529\n      p_twoway float 0.9632162541624284\n  H1_heldout dict 14\n    dauc float -8.9655543402678e-06\n    ci95 list 2\n    auc_X0 float 0.8372646639437369\n    auc_X1 float 0.8372556983893966\n    per_group dict 4\n      PHYS float 0.0004977576102344061\n      LIFEENV float -0.00025573305214199316\n      SOC float -0.00012125323271283683\n      MATHDEC float 0.0005239151873767112\n    dl_pool dict 7\n      k int 4\n      pooled float -4.3991314466003225e-05\n      se float 0.00019697749811468297\n      ci95 list 2\n      tau2 float 0.0\n      I2 float 0.0\n      Q float 1.6886147538161116\n    cohort_dauc float -0.00014840221616119198\n    cohort_ci95 list 2\n    verdict dict 2\n      verdict str 12\n      criteria dict 7\n    placebo_p95 float 0.00011013988603601445\n    cond_logit dict 9\n      n_episodes_informative int 5036\n      n_concepts_informative int 1452\n      beta_gateway_std float -0.0746527649197613\n      se float 0.06240505008412258\n      z float -1.1962615977253235\n      p_two_sided float 0.23159448975679897\n      LR float 1.4407798330089463\n      LR_p float 0.23001318820583636\n      method str 16\n    lpm dict 7\n      n int 8515\n      within_field_sd_of_regressor float 0.024114481018227937\n      beta_within_per_sd float 0.06778995979996934\n      se_concept float 0.0331393319594772\n      p_concept float 0.04079531852765418\n      se_twoway float 0.04966999749594251\n      p_twoway float 0.17231372111171483\n    rival_head_to_head dict 5\n      dauc_relatedness_pair float 0.0033563007447128257\n      relatedness_ci95 list 2\n      dauc_gateway float -4.8790806590703895e-05\n      gateway_ci95 list 2\n      diff_gateway_minus_relatedness float -0.0034050915513035296\n    pigeonhole_ci95 list 2\n  ladder_dev dict 5\n    L1_iter1_base float 0.0019460073189199179\n    L2_plus_relatedness float 0.0006932771708442198\n    L3_plus_Pj float 2.667125537048065e-05\n    L4_full_X0 float 1.3686565255799366e-05\n    L0_size_only float 0.004223358194140769\n  ladder_heldout dict 5\n    L1_iter1_base float -0.001621790818804647\n    L2_plus_relatedness float -0.0011816340749275511\n    L3_plus_Pj float -3.5147571725069326e-05\n    L4_full_X0 float -8.9655543402678e-06\n    L0_size_only float -0.0017103419098605244\n  gateway_alone_auc dict 2\n    dev float 0.6054439015180273\n    heldout float 0.5056949785879173\n  H3_heldout dict 8\n    G dict 3\n      partial_rho float 0.02950282637789586\nci,field,n_early,n_A,n_B,share_early,growth_j,concept_id,name,t0,group,split,home,n_out,share_out,R,R_abs1,R_abs2,R_abs3,lab_out\n3,17,7.0,3.0,4.0,0.1014492735266685,0.6931471805599453,37253,Complete intersection,2012,MATHDEC,COHORT,26,1.0,0.01923076994717121,0.0,1.0,0.0,0.0,52.0\n3,31,3.0,2.0,1.0,0.0434782616794109,0.0,37253,Complete intersection,2012,MATHDEC,COHORT,26,2.0,0.03846153989434242,0.0,1.0,1.0,0.0,52.0\nci,field,n_early,n_A,n_B,share_early,growth_j,concept_id,name,t0,group,split,home,n_out,share_out,R,R_abs1,R_abs2,R_abs3,lab_out,logvol,growth_c,offhome_share,entropy,reach,log_field_size,log_field_size_s,phi_home,density,log_n_early,gateway_j,gateway_js,gateway_deg,gateway_btw,gateway_phimin,gateway_S0rec,top_tercile_home,label_coverage_early,precision_c,tag_coverage,newborn,intersect40,weak_home\n3,17,7.0,3.0,4.0,0.1014492735266685,0.6931471805599453,37253,Complete intersection,2012,MATHDEC,COHORT,26,,,,,,,,4.290459441148391,0.2657032014957919,0.14492753148078918,0.5023395901069845,3,13.606041828610847,12.722190242075243,1.4630050170651157,0.4974969068143295,2.0794415416798357,0.09720895637939932,0.053987340894166666,0.4363827113448261,0.0,0.393320903832998,0.09802915137540266,0,0.9583333134651184,1.0,0.5901639461517334,False,0,0\n3,31,3.0,2.0,1.0,0.0434782616794109,0.0,37253,Complete intersection,2012,MATHDEC,COHORT,26,,,,,,,,4.290459441148391,0.2657032014957919,0.14492753148078918,0.5023395901069845,3,13.508763905792184,13.102717657797493,1.0519201429910805,0.25559373360589505,1.3862943611198906,0.4858337648309395,0.4413171942215754,0.6107235613440025,0.18666666666666668,0.47058675622183077,0.48612543393080454,0,0.9583333134651184,1.0,0.5901639461517334,False,0,0\nci,concept_id,G,G_A,G_btw,G_deg,G_phimin,REL_home,RS,DOM_Physical,DOM_Life,DOM_Health,DOM_Social,log_count,share,growth_ind,accel,burst,lab_entropy,lab_reach,lab_offhome_share,log_offhome_volume,logvol,growth_c,offhome_share,entropy,reach\n3,37253,0.21379639891486138,0.2526588797600154,0.05600000000000001,0.48868496634457903,0.4165006595496479,1.339679554842905,0.2379800770047855,0.9999999403953552,0.0,0.0,0.0,4.290459441148391,3.848425074798417,0.31015493625112545,0.1773033142089843,0.0,0.5023395901069845,3,0.14492753148078918,2.3978952727983707,4.290459441148391,0.2657032014957919,0.14492753148078918,0.5023395901069845,3\n4,39854,0.09720895637939932,,0.0,0.4363827113448261,0.393320903832998,0.01543785887767766,0.03407468869309204,1.0,0.0,0.0,0.0,4.174387269895637,5.476313958106027,-0.2451224679670925,-0.06126010417938217,0.0,0.0922160573371918,1,0.018518518656492233,0.6931471805599453,4.174387269895637,-0.36772475363436447,0.018518518656492233,0.0922160573371918,1", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-30 01:38:10 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cd $A; python3 -c "
import json
d=json.load(open('mini_method_out.json'))
print(list(d.keys()))
for k,v in d.items():
    if k!='metadata': print(k, type(v).__name__, len(v) if hasattr(v,'__len__') else v); 
    if isinstance(v,list): print(json.dumps(v[0])[:1500])
"; grep -n "^def \|^    def \|^if __name__\|^[A-Z_]* = " models.py | head -120
```

### [14] TOOL RESULT — Bash · 2026-09-30 01:38:10 UTC

```
{"stdout": "['metadata', 'datasets']\ndatasets list 3\n{\"dataset\": \"episodes_dev_LOGO_oof\", \"examples\": [{\"input\": \"{\\\"concept_id\\\": 252157, \\\"concept\\\": \\\"Scatternet\\\", \\\"adopting_field\\\": 22, \\\"adopting_field_name\\\": \\\"Engineering\\\", \\\"home\\\": \\\"17\\\", \\\"t0\\\": 2003, \\\"group\\\": \\\"CS\\\", \\\"split\\\": \\\"DEV\\\", \\\"covariates\\\": {\\\"logvol\\\": 4.35671, \\\"growth_c\\\": 0.0, \\\"offhome_share\\\": 0.30189, \\\"entropy\\\": 0.75814, \\\"reach\\\": 3.0, \\\"log_field_size\\\": 15.14617, \\\"phi_home\\\": 0.01544, \\\"density\\\": 0.25923, \\\"P_j\\\": 0.52571, \\\"label_coverage_early\\\": 0.68831, \\\"precision_c\\\": 1.0, \\\"tag_coverage\\\": 0.91667, \\\"log_n_early\\\": 2.63906, \\\"share_early\\\": 0.24528, \\\"growth_j\\\": 0.69315, \\\"gateway_j\\\": 0.24272}}\", \"output\": \"0\", \"predict_baseline\": \"0.887660\", \"predict_gateway\": \"0.886883\", \"metadata_split\": \"DEV\", \"metadata_group\": \"CS\", \"metadata_concept_id\": 252157, \"metadata_field\": 22, \"metadata_n_early\": 13.0, \"metadata_n_out\": 3.0, \"metadata_gateway_j\": 0.2427178906876991}, {\"input\": \"{\\\"concept_id\\\": 252157, \\\"concept\\\": \\\"Scatternet\\\", \\\"adopting_field\\\": 33, \\\"adopting_field_name\\\": \\\"Social Sciences\\\", \\\"home\\\": \\\"17\\\", \\\"t0\\\": 2003, \\\"group\\\": \\\"CS\\\", \\\"split\\\": \\\"DEV\\\", \\\"covariates\\\": {\\\"logvol\\\": 4.35671, \\\"growth_c\\\": 0.0, \\\"offhome_share\\\": 0.30189, \\\"entropy\\\": 0.75814, \\\"reach\\\": 3.0, \\\"log_field_size\\\": 15.21054, \\\"phi_home\\\": 0.0, \\\"density\\\": 0.55268, \\\"P_j\\\": 0.14204, \\\"label_coverage_early\\\": 0.68831, \\\"precision_c\\\": 1.0, \\\"tag_coverage\\\": 0.91667, \\\"log_n_early\\\": 1.38629, \\\"share_early\\\": 0.0566, \\\"growth_j\\\": 0.0, \\\"\n33:N_JOBS = 4\n36:GATE = \"gateway_j\"\n38:FE_VARY = [\"log_field_size\", \"phi_home\", \"density\", \"P_j\", \"log_n_early\", \"share_early\", \"growth_j\"]\n39:C_REG = 1.0\n40:PJ_M = 5.0      # shrinkage pseudo-count of the leave-concept-out propensity towards the split-set mean\n41:PJ_WIN = 2      # |t0' - t0| <= 2\n43:SMOKE = os.environ.get(\"SMOKE\") == \"1\"   # smoke test: small B, no freeze, separate output file\n44:B_MAIN = 60 if SMOKE else 2000\n45:B_SMALL = 20 if SMOKE else 500\n46:SPEC = ROOT / \"frozen_spec.json\"\n50:def split_set(s: str) -> str:\n54:def add_pj(df: pd.DataFrame, rcol: str = \"R\", out: str = \"P_j\") -> pd.DataFrame:\n73:def add_pj_train(df: pd.DataFrame, rcol: str = \"R\", out: str = \"P_j_trainset\") -> pd.DataFrame:\n92:def std_consts(df: pd.DataFrame, cols: list[str]) -> dict:\n96:def Z(df: pd.DataFrame, cols: list[str], sc: dict) -> np.ndarray:\n105:    def __init__(self, C: float = C_REG):\n108:    def fit(self, X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> \"L2Logit\":\n127:    def decision_function(self, X: np.ndarray) -> np.ndarray:\n130:    def predict_proba(self, X: np.ndarray) -> np.ndarray:\n135:def fit(X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> L2Logit:\n139:def auc(y, p, w=None) -> float:\n146:def logo_oof(df: pd.DataFrame, cols: list[str], sc: dict, y: np.ndarray, groups: np.ndarray,\n160:def dl_pool(est: list[float], se: list[float]) -> dict:\n180:def sign_test(vals: list[float]) -> dict:\n187:def concept_index(df: pd.DataFrame) -> dict:\n192:def _boot_logo(seed: int, df: pd.DataFrame, specs: dict, sc: dict, y: np.ndarray, grp: np.ndarray,\n211:def boot_logo(df, specs, sc, y, grp, B, seed0):\n219:def ci95(a) -> list[float]:\n225:def cond_logit(df: pd.DataFrame, y: np.ndarray, sc: dict, gate: str = GATE) -> dict:\n247:def mixed_logit_fallback(d, yy, sc, gate) -> dict:\n258:def lpm_fe(df: pd.DataFrame, y: np.ndarray, sc: dict, gcol: str = \"gateway_js\") -> dict:\n279:def boundary(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:\n296:def logit_twoway(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:\n313:def load_dev() -> tuple[pd.DataFrame, pd.DataFrame]:\n323:def logo_dauc(df, sc, y, grp, gate_col=GATE, base=None) -> dict:\n329:def placebo_dauc(df, sc, y, grp, vecs: np.ndarray, base) -> list[float]:\n332:    def one(v):\n342:def leave_field_out(df, sc, y, grp) -> dict:\n343:    def one(f):\n356:def pigeonhole(df, sc, y, grp, B: int, seed0: int, heldout=None) -> list[float]:\n361:    def one(b):\n379:def pigeonhole_heldout(dev: pd.DataFrame, ho: pd.DataFrame, sc: dict, B: int, seed0: int) -> list[float]:\n387:    def one(b):\n401:def _fit_eval(d, yy, ww, hd, hy, wh, sc):\n410:def power_sim(df, sc, y, n_heldout: int, seed: int = SEED) -> dict:\n417:    def sim(b, k):\n445:def partial_spearman(x, y, Zc: np.ndarray) -> float:\n459:LADDER = {\"L1_iter1_base\": B5 + [\"log_n_early\", \"share_early\", \"growth_j\", \"log_field_size\"]}\n467:def h3_table(fc: pd.DataFrame, co: pd.DataFrame, cf: pd.DataFrame, split_mask, resid_ab) -> pd.DataFrame:\n475:def cmd_dev() -> None:\n628:def _boot_ho(seed, dev, ydev, cidx_dev, dev_cg, ho, yho, cidx_ho, ho_cg, sc, cols_pair):\n646:def score_heldout(dev, ho, sc, cols0=X0, cols1=X1, rcol=\"R\", B=B_MAIN, seed=SEED, groups=HELD_GROUPS):\n680:def cmd_heldout() -> None:\n696:def smoke_heldout() -> None:\n717:def analyze_heldout(F: pd.DataFrame, sc: dict, sha: str, groups: list[str], dev_groups_for_logo=None) -> dict:\n762:    def pl_one(v):\n817:def sensitivities(F, dev, ho, sc, groups=HELD_GROUPS) -> dict:\n820:    def run(name, d, h, cols0=X0, cols1=X1, rcol=\"R\"):\n851:def h3_heldout(spec) -> None:\n903:if __name__ == \"__main__\":", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] ASSISTANT · 2026-09-30 01:38:12 UTC

```
I'm reading the artifact's code. `method.py` only orchestrates the pipeline, so the notebook has to show the core H1 analysis from `models.py` as well. Next I'll read `models.py`.
```

### [16] TOOL CALL — Bash · 2026-09-30 01:38:12 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; sed -n 1,340p $A/models.py
```

### [17] TOOL RESULT — Bash · 2026-09-30 01:38:12 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEPS 8-9 (analysis): H1 episode-level gateway-retention models and H3 concept-level partial Spearman.\n\n  python models.py dev       dev-only analysis, then FREEZE (frozen_spec.json, sha256 -> logs/seal.log, git commit)\n  python models.py heldout   score the frozen models ONCE on the unsealed held-out groups and the 2010-14 cohort\n\nPrimary: L2 logistic (C=1, lbfgs) of R on X0 vs X1 = X0 + gateway_j. Dev: leave-one-home-group-out OOF dAUC with a\n2,000-draw concept-clustered REFIT bootstrap. Held-out: fit on all dev, predict held-out, bootstrap resampling dev\nconcepts (refit) and held-out concepts (evaluate). Secondary: conditional logit (concept FE), LPM with field FE and\ntime-varying gateway_j,s (concept- and two-way clustered SEs), boundary interaction, relatedness head-to-head,\n200 rewired-backbone placebos (+ permutation placebo), leave-one-adopting-field-out, crossed concept x field\nbootstrap, power simulation.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport subprocess\nimport sys\nimport time\nimport warnings\n\nimport numpy as np\nimport pandas as pd\nfrom joblib import Parallel, delayed\nfrom scipy import stats\nfrom sklearn.metrics import roc_auc_score\n\nfrom common import DEV_GROUPS, HELD_GROUPS, LOGS, RES, ROOT, SEED, jdump, setup_logger\n\nwarnings.filterwarnings(\"ignore\")\nlogger = setup_logger(\"models\")\nN_JOBS = 4\nX0 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"log_field_size\", \"phi_home\", \"density\", \"P_j\",\n      \"label_coverage_early\", \"precision_c\", \"tag_coverage\", \"log_n_early\", \"share_early\", \"growth_j\"]\nGATE = \"gateway_j\"\nX1 = X0 + [GATE]\nFE_VARY = [\"log_field_size\", \"phi_home\", \"density\", \"P_j\", \"log_n_early\", \"share_early\", \"growth_j\"]\nC_REG = 1.0\nPJ_M = 5.0      # shrinkage pseudo-count of the leave-concept-out propensity towards the split-set mean\nPJ_WIN = 2      # |t0' - t0| <= 2\nimport os\nSMOKE = os.environ.get(\"SMOKE\") == \"1\"   # smoke test: small B, no freeze, separate output file\nB_MAIN = 60 if SMOKE else 2000\nB_SMALL = 20 if SMOKE else 500\nSPEC = ROOT / \"frozen_spec.json\"\n\n\n# ----------------------------------------------------------------------------- helpers\ndef split_set(s: str) -> str:\n    return \"HELDOUT\" if s.startswith(\"HELDOUT\") else s\n\n\ndef add_pj(df: pd.DataFrame, rcol: str = \"R\", out: str = \"P_j\") -> pd.DataFrame:\n    \"\"\"Leave-concept-out retention propensity of field j among OTHER concepts' episodes in the same split set\n    with |t0' - t0| <= 2, shrunk towards the split-set mean with pseudo-count PJ_M.\"\"\"\n    df = df.copy()\n    df[\"_ss\"] = df.split.map(split_set)\n    vals = np.full(len(df), np.nan)\n    for (ss, f), g in df.groupby([\"_ss\", \"field\"]):\n        mu = df.loc[(df._ss == ss) & df[rcol].notna(), rcol].mean()\n        gv = g[g[rcol].notna()]\n        t0 = gv.t0.to_numpy()\n        r = gv[rcol].to_numpy(float)\n        ci = gv.ci.to_numpy()\n        for idx, row in zip(g.index, g.itertuples()):\n            m = (np.abs(t0 - row.t0) <= PJ_WIN) & (ci != row.ci)\n            vals[df.index.get_loc(idx)] = (r[m].sum() + PJ_M * mu) / (m.sum() + PJ_M)\n    df[out] = vals\n    return df.drop(columns=\"_ss\")\n\n\ndef add_pj_train(df: pd.DataFrame, rcol: str = \"R\", out: str = \"P_j_trainset\") -> pd.DataFrame:\n    \"\"\"Variant P_j_train: dev-only retention propensity of field j (any t0, other concepts), shrunk to the dev mean.\"\"\"\n    df = df.copy()\n    dv = df[(df.split == \"DEV\") & df[rcol].notna()]\n    mu = dv[rcol].mean()\n    s = dv.groupby(\"field\")[rcol].sum()\n    n = dv.groupby(\"field\")[rcol].size()\n    own = dv.groupby([\"ci\", \"field\"])[rcol].agg([\"sum\", \"size\"])\n    vals = []\n    for r in df.itertuples():\n        a, b = float(s.get(r.field, 0.0)), float(n.get(r.field, 0))\n        if r.split == \"DEV\" and (r.ci, r.field) in own.index:\n            a -= float(own.at[(r.ci, r.field), \"sum\"])\n            b -= float(own.at[(r.ci, r.field), \"size\"])\n        vals.append((a + PJ_M * mu) / (b + PJ_M))\n    df[out] = vals\n    return df\n\n\ndef std_consts(df: pd.DataFrame, cols: list[str]) -> dict:\n    return {c: [float(df[c].mean()), float(df[c].std() or 1.0)] for c in cols}\n\n\ndef Z(df: pd.DataFrame, cols: list[str], sc: dict) -> np.ndarray:\n    X = np.column_stack([(df[c].to_numpy(float) - sc[c][0]) / (sc[c][1] if sc[c][1] > 0 else 1.0) for c in cols])\n    return np.nan_to_num(X, nan=0.0)  # NaN -> dev mean (0 after standardisation)\n\n\nclass L2Logit:\n    \"\"\"Exact Newton-IRLS for sklearn's L2 objective 0.5*||w||^2 + C * sum_i s_i * logloss_i (intercept unpenalised).\n    Fast for the ~16 standardised covariates used here; converges to the same optimum as lbfgs.\"\"\"\n\n    def __init__(self, C: float = C_REG):\n        self.C = C\n\n    def fit(self, X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> \"L2Logit\":\n        Xa = np.column_stack([np.ones(len(X)), X])\n        s = np.ones(len(X)) if w is None else np.asarray(w, float)\n        y = np.asarray(y, float)\n        P = np.eye(Xa.shape[1])\n        P[0, 0] = 0.0\n        b = np.zeros(Xa.shape[1])\n        for _ in range(100):\n            eta = np.clip(Xa @ b, -35, 35)\n            p = 1 / (1 + np.exp(-eta))\n            g = self.C * Xa.T @ (s * (p - y)) + P @ b\n            H = self.C * (Xa * (s * p * (1 - p))[:, None]).T @ Xa + P\n            step = np.linalg.solve(H, g)\n            b -= step\n            if np.abs(step).max() < 1e-10:\n                break\n        self.coef_, self.intercept_ = b[1:][None, :], np.array([b[0]])\n        return self\n\n    def decision_function(self, X: np.ndarray) -> np.ndarray:\n        return X @ self.coef_[0] + self.intercept_[0]\n\n    def predict_proba(self, X: np.ndarray) -> np.ndarray:\n        p = 1 / (1 + np.exp(-np.clip(self.decision_function(X), -35, 35)))\n        return np.column_stack([1 - p, p])\n\n\ndef fit(X: np.ndarray, y: np.ndarray, w: np.ndarray | None = None) -> L2Logit:\n    return L2Logit(C_REG).fit(X, y, w)\n\n\ndef auc(y, p, w=None) -> float:\n    y = np.asarray(y)\n    if len(np.unique(y)) < 2:\n        return math.nan\n    return float(roc_auc_score(y, p, sample_weight=w))\n\n\ndef logo_oof(df: pd.DataFrame, cols: list[str], sc: dict, y: np.ndarray, groups: np.ndarray,\n             w: np.ndarray | None = None) -> np.ndarray:\n    X = Z(df, cols, sc)\n    oof = np.full(len(df), np.nan)\n    for g in np.unique(groups):\n        te = groups == g\n        tr = ~te\n        if len(np.unique(y[tr])) < 2:\n            continue\n        m = fit(X[tr], y[tr], None if w is None else w[tr])\n        oof[te] = m.predict_proba(X[te])[:, 1]\n    return oof\n\n\ndef dl_pool(est: list[float], se: list[float]) -> dict:\n    y = np.array(est, float)\n    v = np.array(se, float) ** 2\n    ok = np.isfinite(y) & np.isfinite(v) & (v > 0)\n    y, v = y[ok], v[ok]\n    k = len(y)\n    if k == 0:\n        return {\"k\": 0}\n    w = 1 / v\n    ybar = (w * y).sum() / w.sum()\n    Q = float((w * (y - ybar) ** 2).sum())\n    tau2 = max(0.0, (Q - (k - 1)) / (w.sum() - (w ** 2).sum() / w.sum())) if k > 1 else 0.0\n    ws = 1 / (v + tau2)\n    mu = float((ws * y).sum() / ws.sum())\n    se_mu = float(math.sqrt(1 / ws.sum()))\n    I2 = float(max(0.0, (Q - (k - 1)) / Q)) if Q > 0 and k > 1 else 0.0\n    return {\"k\": k, \"pooled\": mu, \"se\": se_mu, \"ci95\": [mu - 1.96 * se_mu, mu + 1.96 * se_mu], \"tau2\": tau2,\n            \"I2\": I2, \"Q\": Q}\n\n\ndef sign_test(vals: list[float]) -> dict:\n    v = [x for x in vals if np.isfinite(x)]\n    k = sum(1 for x in v if x > 0)\n    return {\"n\": len(v), \"n_positive\": k, \"p_one_sided\": float(stats.binomtest(k, len(v), 0.5,\n                                                                                alternative=\"greater\").pvalue) if v else math.nan}\n\n\ndef concept_index(df: pd.DataFrame) -> dict:\n    return {c: np.nonzero(df.ci.to_numpy() == c)[0] for c in np.unique(df.ci)}\n\n\n# ----------------------------------------------------------------------------- dev: LOGO + refit bootstrap\ndef _boot_logo(seed: int, df: pd.DataFrame, specs: dict, sc: dict, y: np.ndarray, grp: np.ndarray,\n               cidx: dict, cgrp: dict) -> dict:\n    rng = np.random.default_rng(seed)\n    rows = []\n    for g in DEV_GROUPS:\n        cs = cgrp[g]\n        pick = rng.choice(cs, size=len(cs), replace=True)\n        rows.append(np.concatenate([cidx[c] for c in pick]))\n    idx = np.concatenate(rows)\n    d = df.iloc[idx]\n    yy, gg = y[idx], grp[idx]\n    out = {}\n    for name, cols in specs.items():\n        out[name] = logo_oof(d, cols, sc, yy, gg)\n    res = {name: auc(yy, p) for name, p in out.items()}\n    res[\"per_group\"] = {g: {name: auc(yy[gg == g], out[name][gg == g]) for name in specs} for g in DEV_GROUPS}\n    return res\n\n\ndef boot_logo(df, specs, sc, y, grp, B, seed0):\n    cidx = concept_index(df)\n    cg = df.groupby(\"ci\").group.first()\n    cgrp = {g: cg.index[cg == g].to_numpy() for g in DEV_GROUPS}\n    return Parallel(n_jobs=N_JOBS, batch_size=8)(delayed(_boot_logo)(seed0 + b, df, specs, sc, y, grp, cidx, cgrp)\n                                                 for b in range(B))\n\n\ndef ci95(a) -> list[float]:\n    a = np.asarray([x for x in a if np.isfinite(x)])\n    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))] if len(a) else [math.nan, math.nan]\n\n\n# ----------------------------------------------------------------------------- secondary models\ndef cond_logit(df: pd.DataFrame, y: np.ndarray, sc: dict, gate: str = GATE) -> dict:\n    from statsmodels.discrete.conditional_models import ConditionalLogit\n    g = df.ci.to_numpy()\n    mix = pd.Series(y).groupby(g).transform(lambda s: 0 < s.mean() < 1).to_numpy(bool)\n    d, yy = df[mix], y[mix]\n    cols0 = FE_VARY\n    X0_ = Z(d, cols0, sc)\n    X1_ = np.column_stack([X0_, Z(d, [gate], sc)])\n    out = {\"n_episodes_informative\": int(mix.sum()), \"n_concepts_informative\": int(d.ci.nunique())}\n    try:\n        m0 = ConditionalLogit(yy, X0_, groups=d.ci.to_numpy()).fit(disp=0, maxiter=200)\n        m1 = ConditionalLogit(yy, X1_, groups=d.ci.to_numpy()).fit(disp=0, maxiter=200)\n        b, se = float(m1.params[-1]), float(m1.bse[-1])\n        lr = 2 * (m1.llf - m0.llf)\n        out.update({\"beta_gateway_std\": b, \"se\": se, \"z\": b / se, \"p_two_sided\": float(2 * stats.norm.sf(abs(b / se))),\n                    \"LR\": float(lr), \"LR_p\": float(stats.chi2.sf(lr, 1)), \"method\": \"ConditionalLogit\"})\n    except (np.linalg.LinAlgError, ValueError) as e:\n        out.update({\"error\": repr(e)[:200]})\n        out.update(mixed_logit_fallback(d, yy, sc, gate))\n    return out\n\n\ndef mixed_logit_fallback(d, yy, sc, gate) -> dict:\n    from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM\n    X = np.column_stack([np.ones(len(d)), Z(d, FE_VARY + [gate], sc)])\n    codes = pd.factorize(d.ci)[0]\n    exog_vc = np.zeros((len(d), codes.max() + 1))\n    exog_vc[np.arange(len(d)), codes] = 1\n    m = BinomialBayesMixedGLM(yy, X, exog_vc, np.zeros(codes.max() + 1, int)).fit_vb()\n    b, se = float(m.fe_mean[-1]), float(m.fe_sd[-1])\n    return {\"method\": \"BinomialBayesMixedGLM (fallback)\", \"beta_gateway_std\": b, \"se\": se, \"z\": b / se}\n\n\ndef lpm_fe(df: pd.DataFrame, y: np.ndarray, sc: dict, gcol: str = \"gateway_js\") -> dict:\n    import statsmodels.api as sm\n    cols = [c for c in X0 if c != \"log_field_size\"]\n    X = pd.DataFrame(Z(df, cols, sc), columns=cols, index=df.index)\n    X[gcol] = (df[gcol] - df[gcol].mean()) / (df[gcol].std() or 1)\n    fe = pd.get_dummies(df.field.astype(str), prefix=\"f\", drop_first=True, dtype=float)\n    te = pd.get_dummies(df.t0.astype(str), prefix=\"t\", drop_first=True, dtype=float)\n    X = sm.add_constant(pd.concat([X, fe, te], axis=1))\n    out = {\"n\": int(len(df)), \"within_field_sd_of_regressor\": float(df.groupby(\"field\")[gcol].std().mean())}\n    try:\n        m1 = sm.OLS(y, X).fit(cov_type=\"cluster\", cov_kwds={\"groups\": pd.factorize(df.ci)[0]})\n        m2 = sm.OLS(y, X).fit(cov_type=\"cluster\", cov_kwds={\"groups\": np.column_stack(\n            [pd.factorize(df.ci)[0], pd.factorize(df.field)[0]])})\n        b = float(m1.params[gcol])\n        out.update({\"beta_within_per_sd\": b, \"se_concept\": float(m1.bse[gcol]), \"p_concept\": float(m1.pvalues[gcol]),\n                    \"se_twoway\": float(m2.bse[gcol]), \"p_twoway\": float(m2.pvalues[gcol])})\n    except (np.linalg.LinAlgError, ValueError) as e:\n        out[\"error\"] = repr(e)[:200]\n    return out\n\n\ndef boundary(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:\n    import statsmodels.api as sm\n    X = pd.DataFrame(Z(df, X1, sc), columns=X1, index=df.index)\n    X[\"gw_x_toptercile\"] = X[GATE] * df.top_tercile_home.to_numpy()\n    X[\"top_tercile_home\"] = df.top_tercile_home.to_numpy()\n    X = sm.add_constant(X)\n    try:\n        m = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type=\"cluster\",\n                               cov_kwds={\"groups\": pd.factorize(df.ci)[0]})\n        return {\"beta_interaction\": float(m.params[\"gw_x_toptercile\"]), \"se\": float(m.bse[\"gw_x_toptercile\"]),\n                \"p\": float(m.pvalues[\"gw_x_toptercile\"]), \"beta_gateway_main\": float(m.params[GATE]),\n                \"n_top_tercile_home_episodes\": int(df.top_tercile_home.sum()),\n                \"prediction\": \"negative interaction\", \"consistent\": bool(m.params[\"gw_x_toptercile\"] < 0)}\n    except (np.linalg.LinAlgError, ValueError, Exception) as e:  # noqa: BLE001 -- perfect separation etc.\n        return {\"error\": repr(e)[:200]}\n\n\ndef logit_twoway(df: pd.DataFrame, y: np.ndarray, sc: dict) -> dict:\n    import statsmodels.api as sm\n    X = sm.add_constant(pd.DataFrame(Z(df, X1, sc), columns=X1, index=df.index))\n    out = {}\n    for nm, grp in ((\"concept\", pd.factorize(df.ci)[0]),\n                    (\"twoway\", np.column_stack([pd.factorize(df.ci)[0], pd.factorize(df.field)[0]])),\n                    (\"field\", pd.factorize(df.field)[0])):\n        try:\n            m = sm.Logit(y, X).fit(disp=0, maxiter=200, cov_type=\"cluster\", cov_kwds={\"groups\": grp})\n            out[nm] = {\"beta_gateway_std\": float(m.params[GATE]), \"se\": float(m.bse[GATE]),\n                       \"p\": float(m.pvalues[GATE])}\n        except Exception as e:  # noqa: BLE001\n            out[nm] = {\"error\": repr(e)[:200]}\n    return out\n\n\n# ----------------------------------------------------------------------------- DEV phase\ndef load_dev() -> tuple[pd.DataFrame, pd.DataFrame]:\n    F = pd.read_csv(ROOT / \"episode_features.csv\")\n    co = pd.read_csv(ROOT / \"concept_outcomes.csv\")\n    dev = F[F.split == \"DEV\"].copy()\n    assert dev.R.notna().all(), \"dev outcomes missing\"\n    dev = add_pj(dev)\n    dev = dev.reset_index(drop=True)\n    return dev, co\n\n\ndef logo_dauc(df, sc, y, grp, gate_col=GATE, base=None) -> dict:\n    base = base if base is not None else logo_oof(df, X0, sc, y, grp)\n    p1 = logo_oof(df, X0 + [gate_col], sc, y, grp)\n    return {\"auc0\": auc(y, base), \"auc1\": auc(y, p1), \"dauc\": auc(y, p1) - auc(y, base), \"p0\": base, \"p1\": p1}\n\n\ndef placebo_dauc(df, sc, y, grp, vecs: np.ndarray, base) -> list[float]:\n    fidx = df.field.to_numpy() - 11\n\n    def one(v):\n        d = df.copy()\n        d[\"gw_pl\"] = v[fidx]\n        sc2 = dict(sc)\n        sc2[\"gw_pl\"] = [float(d.gw_pl.mean()), float(d.gw_pl.std() or 1)]\n        p1 = logo_oof(d, X0 + [\"gw_pl\"], sc2, y, grp)\n        return auc(y, p1) - auc(y, base)\n    return Parallel(n_jobs=N_JOBS)(delayed(one)(v) for v in vecs)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-30 01:38:14 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; sed -n 400,700p $A/models.py
```

### [19] TOOL RESULT — Bash · 2026-09-30 01:38:14 UTC

```
{"stdout": "def _fit_eval(d, yy, ww, hd, hy, wh, sc):\n    m0 = fit(Z(d, X0, sc), yy, ww)\n    m1 = fit(Z(d, X1, sc), yy, ww)\n    keep = wh > 0\n    p0 = m0.predict_proba(Z(hd, X0, sc))[:, 1]\n    p1 = m1.predict_proba(Z(hd, X1, sc))[:, 1]\n    return auc(hy[keep], p1[keep], wh[keep]) - auc(hy[keep], p0[keep], wh[keep])\n\n\ndef power_sim(df, sc, y, n_heldout: int, seed: int = SEED) -> dict:\n    X0m = Z(df, X0, sc)\n    eta = fit(X0m, y).decision_function(X0m)\n    gz = Z(df, [GATE], sc)[:, 0]\n    cs = np.unique(df.ci)\n    out = {}\n\n    def sim(b, k):\n        rng = np.random.default_rng(seed + 1000 * int(b * 10) + k)\n        ys = rng.random(len(df)) < 1 / (1 + np.exp(-(eta + b * gz)))\n        tr_c = set(rng.choice(cs, size=len(cs) // 2, replace=False))\n        tr = df.ci.isin(tr_c).to_numpy()\n        te_idx = np.nonzero(~tr)[0]\n        te_idx = rng.choice(te_idx, size=n_heldout, replace=True)\n        m0 = fit(X0m[tr], ys[tr])\n        m1 = fit(np.column_stack([X0m, gz])[tr], ys[tr])\n        p0 = m0.predict_proba(X0m[te_idx])[:, 1]\n        p1 = m1.predict_proba(np.column_stack([X0m, gz])[te_idx])[:, 1]\n        yt = ys[te_idx]\n        d = auc(yt, p1) - auc(yt, p0)\n        bs = []\n        for _ in range(150):\n            ii = rng.integers(0, len(te_idx), len(te_idx))\n            bs.append(auc(yt[ii], p1[ii]) - auc(yt[ii], p0[ii]))\n        return d, np.percentile(bs, 2.5) > 0\n    for b in (0.0, 0.1, 0.2, 0.3):\n        r = Parallel(n_jobs=N_JOBS)(delayed(sim)(b, k) for k in range(4 if SMOKE else 40))\n        out[str(b)] = {\"mean_dauc\": float(np.mean([x[0] for x in r])), \"power_ci_gt0\": float(np.mean([x[1] for x in r]))}\n    det = [float(v[\"mean_dauc\"]) for k, v in out.items() if v[\"power_ci_gt0\"] >= 0.8]\n    out[\"min_detectable_dauc_80pct\"] = min(det) if det else None\n    out[\"n_heldout_episodes_assumed\"] = n_heldout\n    out[\"note\"] = \"planted effect b in SD log-odds of standardised gateway_j on the dev covariate structure; 40 sims x 150 boot\"\n    return out\n\n\ndef partial_spearman(x, y, Zc: np.ndarray) -> float:\n    ok = np.isfinite(x) & np.isfinite(y) & np.isfinite(Zc).all(1)\n    if ok.sum() < 8:\n        return math.nan\n    rx, ry = stats.rankdata(x[ok]), stats.rankdata(y[ok])\n    RZ = np.column_stack([np.ones(ok.sum())] + [stats.rankdata(c) for c in Zc[ok].T])\n    ex = rx - RZ @ np.linalg.lstsq(RZ, rx, rcond=None)[0]\n    ey = ry - RZ @ np.linalg.lstsq(RZ, ry, rcond=None)[0]\n    return float(np.corrcoef(ex, ey)[0, 1])\n\n\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\n# pre-registered explanatory ladder (reported next to the primary, never used for the verdict): where does the\n# gateway increment disappear as the baseline grows from the iteration-1 base to the full X0?\nLADDER = {\"L1_iter1_base\": B5 + [\"log_n_early\", \"share_early\", \"growth_j\", \"log_field_size\"]}\nLADDER[\"L2_plus_relatedness\"] = LADDER[\"L1_iter1_base\"] + [\"phi_home\", \"density\"]\nLADDER[\"L3_plus_Pj\"] = LADDER[\"L2_plus_relatedness\"] + [\"P_j\"]\nLADDER[\"L4_full_X0\"] = X0\nLADDER[\"L0_size_only\"] = [\"log_n_early\", \"share_early\", \"log_field_size\"]\nH3_VARS = [\"G\", \"G_A\", \"G_btw\"]\n\n\ndef h3_table(fc: pd.DataFrame, co: pd.DataFrame, cf: pd.DataFrame, split_mask, resid_ab) -> pd.DataFrame:\n    d = fc[split_mask][[\"ci\", \"group\", \"split\"]].merge(co.drop(columns=[\"split\"], errors=\"ignore\"), on=\"ci\") \\\n        .merge(cf, on=[\"ci\"], suffixes=(\"\", \"_cf\"))\n    a, b = resid_ab\n    d[\"O2r_resid\"] = d.O2r_m30 - (a + b * np.log(d.N_outcome.clip(lower=1)))\n    return d\n\n\ndef cmd_dev() -> None:\n    t_start = time.time()\n    dev, co = load_dev()\n    fc = pd.read_csv(ROOT / \"frame_concepts.csv\")\n    cf = pd.read_csv(ROOT / \"concept_features_basic.csv\")\n    y = dev.R.to_numpy(int)\n    grp = dev.group.to_numpy()\n    sc = std_consts(dev, X1 + [\"gateway_js\", \"gateway_deg\", \"gateway_btw\", \"gateway_phimin\", \"gateway_S0rec\",\n                               \"log_field_size_s\"])\n    res = {\"n_episodes\": len(dev), \"n_concepts\": int(dev.ci.nunique()), \"R_rate\": float(y.mean()),\n           \"by_group\": dev.groupby(\"group\").agg(n=(\"R\", \"size\"), R=(\"R\", \"mean\"), concepts=(\"ci\", \"nunique\")).to_dict(\"index\")}\n    logger.info(f\"DEV: {res['n_episodes']} episodes / {res['n_concepts']} concepts, R rate {y.mean():.3f}\")\n    base = logo_oof(dev, X0, sc, y, grp)\n    prim = logo_dauc(dev, sc, y, grp, base=base)\n    res[\"primary\"] = {\"auc_X0\": prim[\"auc0\"], \"auc_X1\": prim[\"auc1\"], \"dauc\": prim[\"dauc\"],\n                      \"per_group\": {g: {\"auc_X0\": auc(y[grp == g], prim[\"p0\"][grp == g]),\n                                        \"auc_X1\": auc(y[grp == g], prim[\"p1\"][grp == g]),\n                                        \"dauc\": auc(y[grp == g], prim[\"p1\"][grp == g]) - auc(y[grp == g], prim[\"p0\"][grp == g]),\n                                        \"n\": int((grp == g).sum())} for g in DEV_GROUPS}}\n    dev[\"oof_X0\"], dev[\"oof_X1\"] = prim[\"p0\"], prim[\"p1\"]\n    logger.info(f\"DEV primary dAUC={prim['dauc']:+.4f} (AUC0 {prim['auc0']:.3f})\")\n    # refit bootstrap (2,000) -- also carries the rival head-to-head models (paired)\n    Xr = [c for c in X0 if c not in (\"phi_home\", \"density\")]\n    t = time.time()\n    bs = boot_logo(dev, {\"X0\": X0, \"X1\": X1}, sc, y, grp, B_MAIN, SEED)\n    d_boot = [b[\"X1\"] - b[\"X0\"] for b in bs]\n    res[\"primary\"][\"boot_ci95\"] = ci95(d_boot)\n    res[\"primary\"][\"boot_sd\"] = float(np.nanstd(d_boot))\n    res[\"primary\"][\"boot_p_le0\"] = float(np.mean(np.array(d_boot) <= 0))\n    for g in DEV_GROUPS:\n        gd = [b[\"per_group\"][g][\"X1\"] - b[\"per_group\"][g][\"X0\"] for b in bs]\n        res[\"primary\"][\"per_group\"][g][\"boot_se\"] = float(np.nanstd(gd))\n    res[\"primary\"][\"dl_pool_groups\"] = dl_pool([res[\"primary\"][\"per_group\"][g][\"dauc\"] for g in DEV_GROUPS],\n                                               [res[\"primary\"][\"per_group\"][g][\"boot_se\"] for g in DEV_GROUPS])\n    # T5 stability: second seed on 500 draws vs first 500\n    bs2 = boot_logo(dev, {\"X0\": X0, \"X1\": X1}, sc, y, grp, B_SMALL, SEED + 1_000_000)  # disjoint seed range\n    c1 = ci95(d_boot[:B_SMALL])\n    c2 = ci95([b[\"X1\"] - b[\"X0\"] for b in bs2])\n    res[\"T5_seed_stability\"] = {\"ci_seed1_500\": c1, \"ci_seed2_500\": c2, \"max_abs_diff\": float(np.max(np.abs(np.subtract(c1, c2))))}\n    logger.info(f\"bootstrap done in {time.time()-t:.0f}s; CI {res['primary']['boot_ci95']}\")\n    bsr = boot_logo(dev, {\"Xr\": Xr, \"Xr_rel\": Xr + [\"phi_home\", \"density\"], \"Xr_gw\": Xr + [GATE]}, sc, y, grp,\n                    B_SMALL, SEED + 3)\n    rel = [b[\"Xr_rel\"] - b[\"Xr\"] for b in bsr]\n    gw = [b[\"Xr_gw\"] - b[\"Xr\"] for b in bsr]\n    base_r = logo_oof(dev, Xr, sc, y, grp)\n    p_rel = logo_oof(dev, Xr + [\"phi_home\", \"density\"], sc, y, grp)\n    p_gw = logo_oof(dev, Xr + [GATE], sc, y, grp)\n    res[\"rival_head_to_head\"] = {\"dauc_relatedness_pair\": auc(y, p_rel) - auc(y, base_r),\n                                 \"dauc_gateway\": auc(y, p_gw) - auc(y, base_r),\n                                 \"diff_gateway_minus_relatedness\": (auc(y, p_gw) - auc(y, p_rel)),\n                                 \"diff_boot_ci95\": ci95(np.subtract(gw, rel)),\n                                 \"relatedness_boot_ci95\": ci95(rel), \"gateway_boot_ci95\": ci95(gw)}\n    # explanatory ladder (dev, LOGO, 500-draw refit bootstrap each)\n    res[\"ladder\"] = {}\n    for nm, cols in LADDER.items():\n        b0 = logo_oof(dev, cols, sc, y, grp)\n        b1 = logo_oof(dev, cols + [GATE], sc, y, grp)\n        bl = boot_logo(dev, {\"a\": cols, \"b\": cols + [GATE]}, sc, y, grp, B_SMALL, SEED + 5)\n        res[\"ladder\"][nm] = {\"cols\": cols, \"auc_base\": auc(y, b0), \"dauc\": auc(y, b1) - auc(y, b0),\n                             \"ci95\": ci95([x[\"b\"] - x[\"a\"] for x in bl])}\n    res[\"gateway_alone_auc\"] = auc(y, dev[GATE].to_numpy())\n    # secondary\n    res[\"cond_logit\"] = cond_logit(dev, y, sc)\n    res[\"lpm_field_fe\"] = lpm_fe(dev, y, sc)\n    res[\"boundary\"] = boundary(dev, y, sc)\n    res[\"logit_clustered_se\"] = logit_twoway(dev, y, sc)\n    # placebo\n    pl = np.load(ROOT / \"placebo_gateways.npy\")\n    pp = np.load(ROOT / \"placebo_perm_gateways.npy\")\n    pld = placebo_dauc(dev, sc, y, grp, pl, base)\n    ppd = placebo_dauc(dev, sc, y, grp, pp, base)\n    res[\"placebo_rewired\"] = {\"n\": len(pld), \"p95\": float(np.nanpercentile(pld, 95)), \"mean\": float(np.nanmean(pld)),\n                              \"real\": prim[\"dauc\"], \"share_ge_real\": float(np.mean(np.array(pld) >= prim[\"dauc\"])),\n                              \"real_exceeds_p95\": bool(prim[\"dauc\"] > np.nanpercentile(pld, 95)), \"values\": pld}\n    res[\"placebo_permutation\"] = {\"n\": len(ppd), \"p95\": float(np.nanpercentile(ppd, 95)),\n                                  \"share_ge_real\": float(np.mean(np.array(ppd) >= prim[\"dauc\"])), \"values\": ppd}\n    # field-level robustness\n    res[\"leave_one_field_out\"] = leave_field_out(dev, sc, y, grp)\n    ph = pigeonhole(dev, sc, y, grp, B_SMALL, SEED + 7)\n    res[\"pigeonhole_crossed_bootstrap\"] = {\"B\": B_SMALL, \"ci95\": ci95(ph), \"sd\": float(np.nanstd(ph))}\n    # power (held-out n known outcome-blind from the frame)\n    ep_all = pd.read_csv(ROOT / \"episodes.csv\", usecols=[\"split\"])\n    n_ho = int(ep_all.split.str.startswith(\"HELDOUT\").sum())\n    res[\"power\"] = power_sim(dev, sc, y, max(n_ho, 50))\n    # H3 on dev\n    dco = co[co.split == \"DEV\"].dropna(subset=[\"O2r_m30\", \"N_outcome\"])\n    bfit = np.polyfit(np.log(dco.N_outcome.clip(lower=1)), dco.O2r_m30, 1)\n    resid_ab = [float(bfit[1]), float(bfit[0])]\n    h = h3_table(fc, co, cf, (fc.split == \"DEV\").to_numpy(), resid_ab)\n    Zc = h[B5].to_numpy(float)\n    res[\"H3_dev\"] = {v: partial_spearman(h[v].to_numpy(float), h.O2r_resid.to_numpy(float), Zc) for v in H3_VARS + [\"REL_home\"]}\n    res[\"H3_dev\"][\"n\"] = int(h.O2r_resid.notna().sum())\n    res[\"runtime_s\"] = time.time() - t_start\n    if SMOKE:\n        jdump(res, RES / \"h1_dev_smoke.json\")\n        logger.info(f\"SMOKE done in {time.time()-t_start:.0f}s (no freeze)\")\n        return\n    dev.to_csv(ROOT / \"dev_episodes_with_oof.csv\", index=False)\n    jdump(res, RES / \"h1_dev.json\")\n    # --------------------------------------------------------------- FREEZE\n    ep = pd.read_csv(ROOT / \"episodes.csv\", usecols=[\"ci\", \"split\"])\n    lexh = (ROOT / \"frozen_lexicon.sha256\").read_text().strip().splitlines()[-1].split()[-1]\n    sfh = hashlib.sha256((ROOT / \"sense_filter.joblib\").read_bytes()).hexdigest()\n    spec = {\"created\": time.strftime(\"%Y-%m-%d %H:%M:%S\"), \"X0\": X0, \"X1\": X1, \"gateway\": GATE,\n            \"standardisation\": sc, \"C\": C_REG, \"solver\": \"Newton-IRLS (exact L2 optimum; sklearn objective)\", \"P_j\": {\"pseudo_count\": PJ_M, \"window\": PJ_WIN,\n                                                                                      \"split_sets\": [\"DEV\", \"HELDOUT\", \"COHORT\"]},\n            \"R_primary\": \"share_out >= 0.5*share_early AND n_out >= 9 (t0+6..t0+8)\",\n            \"R_sensitivities\": [\"R_abs1\", \"R_abs2\", \"R_abs3\"], \"episode_rule\": \"n_early >= 2 grounded labelled, j not home\",\n            \"group_map\": \"common.GROUP_OF_FIELD\", \"dev_groups\": DEV_GROUPS, \"heldout_groups\": HELD_GROUPS,\n            \"O2r_resid\": {\"a\": resid_ab[0], \"b\": resid_ab[1]}, \"bootstrap\": {\"B\": B_MAIN, \"seed\": SEED},\n            \"placebo_seeds\": f\"{SEED}+k, k=0..199\", \"verdict_rules\": {\n                \"pooled_dauc_min\": 0.05, \"ci_gt0\": True, \"sign_groups_min\": 3, \"cohort_same_sign\": True,\n                \"lpm_beta_within_gt0_p\": 0.05, \"placebo_real_gt_p95\": True},\n            \"lexicon_v1_sha256\": lexh, \"sense_filter_sha256\": sfh,\n            \"heldout_concept_ids\": sorted(int(c) for c in fc.loc[fc.split.str.startswith(\"HELDOUT\"), \"concept_id\"]),\n            \"cohort_concept_ids\": sorted(int(c) for c in fc.loc[fc.split == \"COHORT\", \"concept_id\"]),\n            \"insularity\": \"dropped (NA; API pool below floor)\", \"dev_primary_dauc\": prim[\"dauc\"],\n            \"ladder\": LADDER, \"sensitivities\": [\"R_abs1\", \"R_abs2\", \"R_abs3\", \"n_early_ge5\", \"newborn_only\",\n                                                \"excl_intersection_born\", \"P_j_train\", \"gateway_deg/btw/phimin/S0rec\",\n                                                \"log_field_size_slice\", \"without_P_j\", \"alt_ptopic\", \"alt_match\",\n                                                \"alt_b5_t0p4\"],\n            \"H3\": {\"vars\": H3_VARS, \"rival\": \"REL_home\", \"outcome\": \"O2r_resid\", \"controls\": B5,\n                   \"permutations\": 2000, \"holm\": True}}\n    try:\n        subprocess.run([\"git\", \"init\", \"-q\"], cwd=ROOT, check=False)\n        subprocess.run([\"git\", \"add\", \"-A\", \"--\", \"*.py\", \"tests\", \"pyproject.toml\", \"frozen_lexicon.sha256\",\n                        \"results\", \"frame_concepts.csv\", \"episodes.csv\", \"concept_outcomes.csv\", \".gitignore\"],\n                       cwd=ROOT, check=False, capture_output=True)\n        subprocess.run([\"git\", \"-c\", \"user.name=AMGrobelnik\", \"-c\", \"user.email=noreply@anthropic.com\", \"commit\", \"-q\",\n                        \"-m\", \"Freeze dev specification before unsealing held-out outcomes\\n\\n\"\n                        \"Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\"], cwd=ROOT, check=False,\n                       capture_output=True)\n        gh = subprocess.run([\"git\", \"rev-parse\", \"HEAD\"], cwd=ROOT, capture_output=True, text=True).stdout.strip()\n    except OSError:\n        gh = \"unavailable\"\n    spec[\"git_hash_code\"] = gh\n    SPEC.write_text(json.dumps(spec, indent=1))\n    h = hashlib.sha256(SPEC.read_bytes()).hexdigest()\n    # T6 pre-unseal checklist\n    held_rows = pd.read_csv(ROOT / \"episodes.csv\")\n    hmask = held_rows.split != \"DEV\"\n    t6 = {\"frozen_spec_complete\": all(k in spec for k in (\"X0\", \"X1\", \"standardisation\", \"heldout_concept_ids\")),\n          \"heldout_outcomes_absent_episodes\": bool(held_rows.loc[hmask, \"R\"].isna().all()),\n          \"heldout_outcomes_absent_concepts\": bool(pd.read_csv(ROOT / \"concept_outcomes.csv\").query(\"split != 'DEV'\")\n                                                   .get(\"O2r_m30\", pd.Series(dtype=float)).isna().all()),\n          \"git_commit\": gh}\n    with (LOGS / \"seal.log\").open(\"a\") as f:\n        f.write(f\"{time.strftime('%Y-%m-%d %H:%M:%S')} FREEZE sha256(frozen_spec.json)={h}\\n\")\n        f.write(f\"{time.strftime('%Y-%m-%d %H:%M:%S')} T6 {json.dumps(t6)}\\n\")\n    logger.info(f\"FROZEN: sha256={h[:16]} T6={t6} runtime {time.time()-t_start:.0f}s\")\n\n\n# ----------------------------------------------------------------------------- HELD-OUT phase\ndef _boot_ho(seed, dev, ydev, cidx_dev, dev_cg, ho, yho, cidx_ho, ho_cg, sc, cols_pair):\n    rng = np.random.default_rng(seed)\n    di = np.concatenate([cidx_dev[c] for g in dev_cg for c in rng.choice(dev_cg[g], len(dev_cg[g]), replace=True)])\n    hi_by_g = {g: np.concatenate([cidx_ho[c] for c in rng.choice(ho_cg[g], len(ho_cg[g]), replace=True)])\n               for g in ho_cg if len(ho_cg[g])}\n    d = dev.iloc[di]\n    m0 = fit(Z(d, cols_pair[0], sc), ydev[di])\n    m1 = fit(Z(d, cols_pair[1], sc), ydev[di])\n    out = {}\n    allidx = np.concatenate(list(hi_by_g.values()))\n    for key, idx in list(hi_by_g.items()) + [(\"pooled\", allidx)]:\n        h = ho.iloc[idx]\n        p0 = m0.predict_proba(Z(h, cols_pair[0], sc))[:, 1]\n        p1 = m1.predict_proba(Z(h, cols_pair[1], sc))[:, 1]\n        out[key] = auc(yho[idx], p1) - auc(yho[idx], p0)\n    return out\n\n\ndef score_heldout(dev, ho, sc, cols0=X0, cols1=X1, rcol=\"R\", B=B_MAIN, seed=SEED, groups=HELD_GROUPS):\n    \"\"\"Fit on all dev, evaluate on `ho`. Returns point estimates per group + pooled and bootstrap CIs.\"\"\"\n    ydev = dev[rcol].to_numpy(int)\n    yho = ho[rcol].to_numpy(int)\n    m0 = fit(Z(dev, cols0, sc), ydev)\n    m1 = fit(Z(dev, cols1, sc), ydev)\n    p0 = m0.predict_proba(Z(ho, cols0, sc))[:, 1]\n    p1 = m1.predict_proba(Z(ho, cols1, sc))[:, 1]\n    g = ho.group.to_numpy()\n    out = {\"n\": int(len(ho)), \"n_concepts\": int(ho.ci.nunique()), \"R_rate\": float(yho.mean()),\n           \"auc_X0\": auc(yho, p0), \"auc_X1\": auc(yho, p1), \"dauc\": auc(yho, p1) - auc(yho, p0), \"per_group\": {}}\n    for gg in groups:\n        m = g == gg\n        out[\"per_group\"][gg] = {\"n\": int(m.sum()), \"n_concepts\": int(ho[m].ci.nunique()),\n                                \"auc_X0\": auc(yho[m], p0[m]), \"auc_X1\": auc(yho[m], p1[m]),\n                                \"dauc\": auc(yho[m], p1[m]) - auc(yho[m], p0[m]) if m.sum() else math.nan}\n    if B:\n        cidx_dev = concept_index(dev)\n        dcg = dev.groupby(\"ci\").group.first()\n        dev_cg = {k: dcg.index[dcg == k].to_numpy() for k in dcg.unique()}\n        cidx_ho = concept_index(ho)\n        hcg = ho.groupby(\"ci\").group.first()\n        ho_cg = {k: hcg.index[hcg == k].to_numpy() for k in groups}\n        bs = Parallel(n_jobs=N_JOBS, batch_size=16)(delayed(_boot_ho)(seed + b, dev, ydev, cidx_dev, dev_cg, ho, yho,\n                                                                       cidx_ho, ho_cg, sc, (cols0, cols1)) for b in range(B))\n        out[\"boot_ci95\"] = ci95([b[\"pooled\"] for b in bs])\n        out[\"boot_p_le0\"] = float(np.mean(np.array([b[\"pooled\"] for b in bs]) <= 0))\n        for gg in groups:\n            vals = [b.get(gg, math.nan) for b in bs]\n            out[\"per_group\"][gg][\"boot_se\"] = float(np.nanstd(vals))\n            out[\"per_group\"][gg][\"boot_ci95\"] = ci95(vals)\n    return out, p0, p1\n\n\ndef cmd_heldout() -> None:\n    import seal\n    seal.assert_unsealed()\n    spec = json.loads(SPEC.read_text())\n    sc = spec[\"standardisation\"]\n    F = pd.read_csv(ROOT / \"episode_features.csv\")\n    ep = pd.read_csv(ROOT / \"episodes.csv\")\n    F = F.drop(columns=[c for c in (\"n_out\", \"share_out\", \"R\", \"R_abs1\", \"R_abs2\", \"R_abs3\", \"lab_out\") if c in F]) \\\n        .merge(ep[[\"ci\", \"field\", \"n_out\", \"share_out\", \"R\", \"R_abs1\", \"R_abs2\", \"R_abs3\", \"lab_out\"]], on=[\"ci\", \"field\"])\n    F = add_pj(F)\n    F = add_pj_train(F)\n    res = analyze_heldout(F, sc, seal.spec_sha(), HELD_GROUPS)\n    jdump(res, RES / \"h1_heldout.json\")\n    h3_heldout(spec)\n\n\ndef smoke_heldout() -> None:\n    \"\"\"Pre-unseal smoke test of the held-out code path on DEV data only: CS + Eng act as 'dev', BGM and Med as two\n    pseudo held-out groups (relabelled), a random half of dev concepts as a pseudo cohort. Nothing sealed is read.\"\"\"\n    F = pd.read_csv(ROOT / \"episode_features.csv\")\n    F = F[F.split == \"DEV\"].copy()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-30 01:38:22 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; cd $A; python3 -c "
import json, collections
d=json.load(open('full_method_out.json'))
print(list(d['metadata'].keys()))
for ds in d['datasets']:
    ex=ds['examples']
    print(ds['dataset'], len(ex), sorted(ex[0].keys()))
    print(collections.Counter(e.get('metadata_split') for e in ex).most_common(), collections.Counter(e.get('metadata_group') for e in ex).most_common())
    print(collections.Counter(e['output'] for e in ex).most_common(5))
    print(json.dumps(ex[0])[:800])
"; sed -n 700,910p models.py
```

### [21] TOOL RESULT — Bash · 2026-09-30 01:38:24 UTC

```
{"stdout": "['method_name', 'description', 'baseline', 'method', 'frame', 'grounding', 'H1_dev', 'H1_heldout', 'ladder_dev', 'ladder_heldout', 'gateway_alone_auc', 'H3_heldout', 'files']\nepisodes_dev_LOGO_oof 9079 ['input', 'metadata_concept_id', 'metadata_field', 'metadata_gateway_j', 'metadata_group', 'metadata_n_early', 'metadata_n_out', 'metadata_split', 'output', 'predict_baseline', 'predict_gateway']\n[('DEV', 9079)] [('Med', 3897), ('Eng', 3051), ('BGM', 1270), ('CS', 861)]\n[('0', 6413), ('1', 2666)]\n{\"input\": \"{\\\"concept_id\\\": 252157, \\\"concept\\\": \\\"Scatternet\\\", \\\"adopting_field\\\": 22, \\\"adopting_field_name\\\": \\\"Engineering\\\", \\\"home\\\": \\\"17\\\", \\\"t0\\\": 2003, \\\"group\\\": \\\"CS\\\", \\\"split\\\": \\\"DEV\\\", \\\"covariates\\\": {\\\"logvol\\\": 4.35671, \\\"growth_c\\\": 0.0, \\\"offhome_share\\\": 0.30189, \\\"entropy\\\": 0.75814, \\\"reach\\\": 3.0, \\\"log_field_size\\\": 15.14617, \\\"phi_home\\\": 0.01544, \\\"density\\\": 0.25923, \\\"P_j\\\": 0.52571, \\\"label_coverage_early\\\": 0.68831, \\\"precision_c\\\": 1.0, \\\"tag_coverage\\\": 0.91667, \\\"log_n_early\\\": 2.63906, \\\"share_early\\\": 0.24528, \\\"growth_j\\\": 0.69315, \\\"gateway_j\\\": 0.24272}}\", \"output\": \"0\", \"predict_baseline\": \"0.887660\", \"predict_gateway\": \"0.886883\", \"metadata_split\": \"DEV\", \"metadata_group\": \"CS\", \"metadata_concept_id\": 252157, \"metadata_field\": 22, \"metadata_n_earl\nepisodes_heldout_frozen_model 8515 ['input', 'metadata_concept_id', 'metadata_field', 'metadata_gateway_j', 'metadata_group', 'metadata_n_early', 'metadata_n_out', 'metadata_split', 'output', 'predict_baseline', 'predict_gateway']\n[('HELDOUT_SOC', 3320), ('HELDOUT_LIFEENV', 3099), ('HELDOUT_PHYS', 1662), ('HELDOUT_MATHDEC', 434)] [('SOC', 3320), ('LIFEENV', 3099), ('PHYS', 1662), ('MATHDEC', 434)]\n[('0', 5911), ('1', 2604)]\n{\"input\": \"{\\\"concept_id\\\": 339426, \\\"concept\\\": \\\"Prospect theory\\\", \\\"adopting_field\\\": 14, \\\"adopting_field_name\\\": \\\"Business, Management and Accounting\\\", \\\"home\\\": \\\"20\\\", \\\"t0\\\": 2004, \\\"group\\\": \\\"SOC\\\", \\\"split\\\": \\\"HELDOUT_SOC\\\", \\\"covariates\\\": {\\\"logvol\\\": 4.30407, \\\"growth_c\\\": 0.1226, \\\"offhome_share\\\": 0.64444, \\\"entropy\\\": 1.61661, \\\"reach\\\": 4.0, \\\"log_field_size\\\": 13.02173, \\\"phi_home\\\": 1.35632, \\\"density\\\": 0.48943, \\\"P_j\\\": 0.37026, \\\"label_coverage_early\\\": 0.61644, \\\"precision_c\\\": 0.96773, \\\"tag_coverage\\\": 0.73, \\\"log_n_early\\\": 2.07944, \\\"share_early\\\": 0.15556, \\\"growth_j\\\": 0.28768, \\\"gateway_j\\\": 0.07712}}\", \"output\": \"1\", \"predict_baseline\": \"0.583649\", \"predict_gateway\": \"0.566987\", \"metadata_split\": \"HELDOUT_SOC\", \"metadata_group\": \"SOC\", \"metadata_concept_\nepisodes_cohort_2010_2014_frozen_model 9798 ['input', 'metadata_concept_id', 'metadata_field', 'metadata_gateway_j', 'metadata_group', 'metadata_n_early', 'metadata_n_out', 'metadata_split', 'output', 'predict_baseline', 'predict_gateway']\n[('COHORT', 9798)] [('Med', 2267), ('SOC', 2068), ('Eng', 1680), ('LIFEENV', 1548), ('PHYS', 863), ('BGM', 622), ('CS', 534), ('MATHDEC', 216)]\n[('0', 7197), ('1', 2601)]\n{\"input\": \"{\\\"concept_id\\\": 37253, \\\"concept\\\": \\\"Complete intersection\\\", \\\"adopting_field\\\": 17, \\\"adopting_field_name\\\": \\\"Computer Science\\\", \\\"home\\\": \\\"26\\\", \\\"t0\\\": 2012, \\\"group\\\": \\\"MATHDEC\\\", \\\"split\\\": \\\"COHORT\\\", \\\"covariates\\\": {\\\"logvol\\\": 4.29046, \\\"growth_c\\\": 0.2657, \\\"offhome_share\\\": 0.14493, \\\"entropy\\\": 0.50234, \\\"reach\\\": 3.0, \\\"log_field_size\\\": 13.60604, \\\"phi_home\\\": 1.46301, \\\"density\\\": 0.4975, \\\"P_j\\\": 0.26654, \\\"label_coverage_early\\\": 0.95833, \\\"precision_c\\\": 1.0, \\\"tag_coverage\\\": 0.59016, \\\"log_n_early\\\": 2.07944, \\\"share_early\\\": 0.10145, \\\"growth_j\\\": 0.69315, \\\"gateway_j\\\": 0.09721}}\", \"output\": \"0\", \"predict_baseline\": \"0.425243\", \"predict_gateway\": \"0.416215\", \"metadata_split\": \"COHORT\", \"metadata_group\": \"MATHDEC\", \"metadata_concept_id\": 37253, \"metad\n    F = F[F.split == \"DEV\"].copy()\n    rng = np.random.default_rng(0)\n    coh_c = set(rng.choice(F[F.group.isin([\"CS\", \"Eng\"])].ci.unique(), 300, replace=False))\n    F.loc[F.group == \"BGM\", \"split\"] = \"HELDOUT_PSEUDO_A\"\n    F.loc[F.group == \"Med\", \"split\"] = \"HELDOUT_PSEUDO_B\"\n    F.loc[F.ci.isin(coh_c), \"split\"] = \"COHORT\"\n    F.loc[F.split == \"HELDOUT_PSEUDO_A\", \"group\"] = \"PSA\"\n    F.loc[F.split == \"HELDOUT_PSEUDO_B\", \"group\"] = \"PSB\"\n    F = add_pj(F)\n    F = add_pj_train(F)\n    sc = std_consts(F[F.split == \"DEV\"], X1 + [\"gateway_js\", \"gateway_deg\", \"gateway_btw\", \"gateway_phimin\",\n                                               \"gateway_S0rec\", \"log_field_size_s\"])\n    res = analyze_heldout(F, sc, \"smoke\", [\"PSA\", \"PSB\"], dev_groups_for_logo=[\"CS\", \"Eng\"])\n    jdump(res, RES / \"h1_heldout_smoke.json\")\n    logger.info(f\"smoke held-out: dAUC {res['primary']['dauc']:+.4f} verdict {res['verdict_H1']}\")\n\n\ndef analyze_heldout(F: pd.DataFrame, sc: dict, sha: str, groups: list[str], dev_groups_for_logo=None) -> dict:\n    n_undef = F[F.R.isna()].groupby(\"split\").size().to_dict()\n    F = F[F.R.notna()].copy()  # R undefined when no labelled outcome work exists (share_out = 0/0); excluded as in dev\n    dev = F[F.split == \"DEV\"].reset_index(drop=True)\n    ho = F[F.split.str.startswith(\"HELDOUT\")].reset_index(drop=True)\n    coh = F[F.split == \"COHORT\"].reset_index(drop=True)\n    res = {\"spec_sha256\": sha, \"n_dev\": len(dev), \"n_heldout\": len(ho), \"n_cohort\": len(coh),\n           \"n_R_undefined_excluded\": n_undef}\n    prim, p0, p1 = score_heldout(dev, ho, sc, groups=groups)\n    ho[\"pred_X0\"], ho[\"pred_X1\"] = p0, p1\n    res[\"primary\"] = prim\n    evaluable = [g for g in groups if prim[\"per_group\"][g][\"n_concepts\"] >= 15]\n    res[\"dl_pool\"] = dl_pool([prim[\"per_group\"][g][\"dauc\"] for g in evaluable],\n                             [prim[\"per_group\"][g][\"boot_se\"] for g in evaluable])\n    res[\"evaluable_groups\"] = evaluable\n    res[\"sign_test_groups\"] = sign_test([prim[\"per_group\"][g][\"dauc\"] for g in evaluable])\n    coh_groups = sorted(coh.group.unique())\n    coh_s, c0, c1 = score_heldout(dev, coh, sc, groups=coh_groups)\n    coh[\"pred_X0\"], coh[\"pred_X1\"] = c0, c1\n    res[\"cohort\"] = coh_s\n    logger.info(f\"HELD-OUT dAUC={prim['dauc']:+.4f} CI {prim.get('boot_ci95')}; cohort {coh_s['dauc']:+.4f}\")\n    yho = ho.R.to_numpy(int)\n    res[\"cond_logit\"] = cond_logit(ho, yho, sc)\n    res[\"lpm_field_fe\"] = lpm_fe(ho, yho, sc)\n    res[\"lpm_field_fe_all_splits\"] = lpm_fe(F.dropna(subset=[\"R\"]).reset_index(drop=True),\n                                            F.dropna(subset=[\"R\"]).R.to_numpy(int), sc)\n    res[\"boundary\"] = boundary(ho, yho, sc)\n    res[\"logit_clustered_se\"] = logit_twoway(ho, yho, sc)\n    # relatedness head-to-head on held-out (fit on dev)\n    Xr = [c for c in X0 if c not in (\"phi_home\", \"density\")]\n    rel, _, _ = score_heldout(dev, ho, sc, Xr, Xr + [\"phi_home\", \"density\"], B=B_SMALL, seed=SEED + 11, groups=groups)\n    gw, _, _ = score_heldout(dev, ho, sc, Xr, Xr + [GATE], B=B_SMALL, seed=SEED + 11, groups=groups)\n    res[\"rival_head_to_head\"] = {\"dauc_relatedness_pair\": rel[\"dauc\"], \"relatedness_ci95\": rel.get(\"boot_ci95\"),\n                                 \"dauc_gateway\": gw[\"dauc\"], \"gateway_ci95\": gw.get(\"boot_ci95\"),\n                                 \"diff_gateway_minus_relatedness\": gw[\"dauc\"] - rel[\"dauc\"]}\n    res[\"ladder\"] = {}\n    for nm, cols in LADDER.items():\n        r_, _, _ = score_heldout(dev, ho, sc, cols, cols + [GATE], B=B_SMALL, seed=SEED + 5, groups=groups)\n        res[\"ladder\"][nm] = {\"auc_base\": r_[\"auc_X0\"], \"dauc\": r_[\"dauc\"], \"ci95\": r_.get(\"boot_ci95\"),\n                             \"per_group\": {g: v[\"dauc\"] for g, v in r_[\"per_group\"].items()}}\n    res[\"gateway_alone_auc\"] = auc(yho, ho[GATE].to_numpy())\n    # placebo on held-out: dev-fit with placebo vector, evaluate on held-out\n    pl = np.load(ROOT / \"placebo_gateways.npy\")\n    pp = np.load(ROOT / \"placebo_perm_gateways.npy\")\n\n    def pl_one(v):\n        d, h = dev.copy(), ho.copy()\n        d[\"gw_pl\"] = v[d.field.to_numpy() - 11]\n        h[\"gw_pl\"] = v[h.field.to_numpy() - 11]\n        sc2 = dict(sc)\n        sc2[\"gw_pl\"] = [float(d.gw_pl.mean()), float(d.gw_pl.std() or 1)]\n        r, _, _ = score_heldout(d, h, sc2, X0, X0 + [\"gw_pl\"], B=0, groups=groups)\n        return r[\"dauc\"]\n    pld = Parallel(n_jobs=N_JOBS)(delayed(pl_one)(v) for v in pl)\n    ppd = Parallel(n_jobs=N_JOBS)(delayed(pl_one)(v) for v in pp)\n    res[\"placebo_rewired\"] = {\"p95\": float(np.nanpercentile(pld, 95)), \"mean\": float(np.nanmean(pld)),\n                              \"share_ge_real\": float(np.mean(np.array(pld) >= prim[\"dauc\"])),\n                              \"real_exceeds_p95\": bool(prim[\"dauc\"] > np.nanpercentile(pld, 95)), \"values\": pld}\n    res[\"placebo_permutation\"] = {\"p95\": float(np.nanpercentile(ppd, 95)),\n                                  \"share_ge_real\": float(np.mean(np.array(ppd) >= prim[\"dauc\"])), \"values\": ppd}\n    # field-level robustness on held-out\n    lofo = {}\n    for f in sorted(ho.field.unique()):\n        r, _, _ = score_heldout(dev[dev.field != f].reset_index(drop=True), ho[ho.field != f].reset_index(drop=True),\n                                sc, B=0, groups=groups)\n        lofo[str(f)] = r[\"dauc\"]\n    vals = np.array(list(lofo.values()))\n    infl = max(lofo, key=lambda k: abs(lofo[k] - prim[\"dauc\"]))\n    res[\"leave_one_field_out\"] = {\"by_field\": lofo, \"min\": float(np.nanmin(vals)), \"max\": float(np.nanmax(vals)),\n                                  \"most_influential_field\": int(infl), \"dauc_without_it\": lofo[infl]}\n    ph = pigeonhole_heldout(dev, ho, sc, B_SMALL, SEED + 17)\n    res[\"pigeonhole_crossed_bootstrap\"] = {\"B\": B_SMALL, \"ci95\": ci95(ph), \"sd\": float(np.nanstd(ph))}\n    # verdict\n    signs_ok = sum(1 for g in evaluable if prim[\"per_group\"][g][\"dauc\"] > 0)\n    lpm = res[\"lpm_field_fe\"]\n    crit = {\"pooled_dauc_ge_0.05\": bool(prim[\"dauc\"] >= 0.05),\n            \"refit_ci_gt0\": bool(prim[\"boot_ci95\"][0] > 0),\n            \"sign_ge3_of_4_evaluable\": bool(signs_ok >= 3), \"n_groups_positive\": signs_ok,\n            \"cohort_same_sign\": bool(np.sign(coh_s[\"dauc\"]) == np.sign(prim[\"dauc\"])),\n            \"lpm_beta_within_gt0_p05\": bool(lpm.get(\"beta_within_per_sd\", -1) > 0 and lpm.get(\"p_concept\", 1) < 0.05),\n            \"placebo_null\": res[\"placebo_rewired\"][\"real_exceeds_p95\"]}\n    core = [\"pooled_dauc_ge_0.05\", \"refit_ci_gt0\", \"sign_ge3_of_4_evaluable\", \"cohort_same_sign\",\n            \"lpm_beta_within_gt0_p05\", \"placebo_null\"]\n    if all(crit[k] for k in core):\n        verdict = \"CONFIRMED\"\n    elif prim[\"dauc\"] > 0 and prim[\"boot_ci95\"][0] > 0:\n        verdict = \"PARTIAL\"\n    elif prim[\"dauc\"] > 0 and signs_ok >= 3:\n        verdict = \"PARTIAL\"\n    else:\n        verdict = \"DISCONFIRMED\"\n    res[\"verdict_H1\"] = {\"verdict\": verdict, \"criteria\": crit}\n    res[\"sensitivities\"] = sensitivities(F, dev, ho, sc, groups)\n    if sha != \"smoke\":\n        ho.to_csv(ROOT / \"heldout_episodes_with_pred.csv\", index=False)\n        coh.to_csv(ROOT / \"cohort_episodes_with_pred.csv\", index=False)\n    logger.info(f\"H1 verdict {verdict}: {crit}\")\n    return res\n\n\ndef sensitivities(F, dev, ho, sc, groups=HELD_GROUPS) -> dict:\n    out = {}\n\n    def run(name, d, h, cols0=X0, cols1=X1, rcol=\"R\"):\n        try:\n            r, _, _ = score_heldout(d.dropna(subset=[rcol]).reset_index(drop=True),\n                                    h.dropna(subset=[rcol]).reset_index(drop=True), sc, cols0, cols1, rcol=rcol,\n                                    B=200, seed=SEED + 99, groups=groups)\n            out[name] = {\"dauc\": r[\"dauc\"], \"ci95\": r.get(\"boot_ci95\"), \"n\": r[\"n\"],\n                         \"per_group\": {g: v[\"dauc\"] for g, v in r[\"per_group\"].items()}}\n        except (ValueError, KeyError) as e:\n            out[name] = {\"error\": repr(e)[:200]}\n    for rc in (\"R_abs1\", \"R_abs2\", \"R_abs3\"):\n        run(rc, dev, ho, rcol=rc)\n    run(\"n_early_ge5\", dev[dev.n_early >= 5], ho[ho.n_early >= 5])\n    run(\"newborn_only\", dev[dev.newborn.astype(bool)], ho[ho.newborn.astype(bool)])\n    run(\"excl_intersection_born\", dev[dev.intersect40 == 0], ho[ho.intersect40 == 0])\n    d2, h2 = dev.copy(), ho.copy()\n    d2[\"P_j\"], h2[\"P_j\"] = d2.P_j_trainset, h2.P_j_trainset\n    run(\"P_j_train_instead_of_Pj\", d2, h2)\n    for gv in (\"gateway_deg\", \"gateway_btw\", \"gateway_phimin\", \"gateway_S0rec\"):\n        run(f\"gateway_variant_{gv}\", dev, ho, X0, X0 + [gv])\n    run(\"log_field_size_slice\", dev, ho, [c if c != \"log_field_size\" else \"log_field_size_s\" for c in X0],\n        [c if c != \"log_field_size\" else \"log_field_size_s\" for c in X1])\n    run(\"without_P_j\", dev, ho, [c for c in X0 if c != \"P_j\"], [c for c in X1 if c != \"P_j\"])\n    for alt in (\"ptopic\", \"match\", \"b5_t0p4\"):\n        p = ROOT / f\"sens_episodes_{alt}.csv\"\n        if p.exists():\n            A = pd.read_csv(p)\n            A = add_pj(A)\n            run(f\"alt_{alt}\", A[A.split == \"DEV\"], A[A.split.str.startswith(\"HELDOUT\")])\n    return out\n\n\ndef h3_heldout(spec) -> None:\n    import seal  # noqa: F401\n    fc = pd.read_csv(ROOT / \"frame_concepts.csv\")\n    co = pd.read_csv(ROOT / \"concept_outcomes.csv\")\n    cf = pd.read_csv(ROOT / \"concept_features_basic.csv\")\n    ab = (spec[\"O2r_resid\"][\"a\"], spec[\"O2r_resid\"][\"b\"])\n    h = h3_table(fc, co, cf, fc.split.str.startswith(\"HELDOUT\").to_numpy(), ab).dropna(subset=[\"O2r_resid\"])\n    Zc = h[B5].to_numpy(float)\n    rng = np.random.default_rng(SEED)\n    res = {\"n\": int(len(h))}\n    pvals = {}\n    for v in H3_VARS + [\"REL_home\"]:\n        x = h[v].to_numpy(float)\n        yv = h.O2r_resid.to_numpy(float)\n        rho = partial_spearman(x, yv, Zc)\n        perm = []\n        g = h.group.to_numpy()\n        for _ in range(2000):\n            xp = x.copy()\n            for gg in np.unique(g):\n                m = g == gg\n                xp[m] = rng.permutation(xp[m])\n            perm.append(partial_spearman(xp, yv, Zc))\n        p = float((1 + np.sum(np.array(perm) >= rho)) / (1 + len(perm)))\n        bs = []\n        for _ in range(1000):\n            ii = rng.integers(0, len(h), len(h))\n            bs.append(partial_spearman(x[ii], yv[ii], Zc[ii]))\n        per = {}\n        for gg in HELD_GROUPS:\n            m = g == gg\n            r_g = partial_spearman(x[m], yv[m], Zc[m]) if m.sum() >= 10 else math.nan\n            bsg = [partial_spearman(x[m][ii], yv[m][ii], Zc[m][ii])\n                   for ii in (rng.integers(0, m.sum(), m.sum()) for _ in range(300))] if m.sum() >= 10 else []\n            per[gg] = {\"rho\": r_g, \"n\": int(m.sum()), \"se\": float(np.nanstd(bsg)) if bsg else math.nan}\n        res[v] = {\"partial_rho\": rho, \"p_perm_one_sided\": p, \"ci95\": ci95(bs), \"per_group\": per,\n                  \"dl_pool\": dl_pool([per[k][\"rho\"] for k in HELD_GROUPS], [per[k][\"se\"] for k in HELD_GROUPS])}\n        if v in H3_VARS:\n            pvals[v] = p\n    order = sorted(pvals, key=pvals.get)\n    holm = {}\n    run_max = 0.0\n    for i, v in enumerate(order):\n        adj = min(1.0, (len(order) - i) * pvals[v])\n        run_max = max(run_max, adj)\n        holm[v] = run_max\n    res[\"holm_adjusted_p\"] = holm\n    res[\"verdict_H3\"] = \"CONFIRMED\" if any(holm[v] < 0.05 and res[v][\"partial_rho\"] > 0 for v in H3_VARS) else \"NOT CONFIRMED\"\n    jdump(res, RES / \"h3_results.json\")\n    logger.info(f\"H3 held-out: { {v: round(res[v]['partial_rho'], 3) for v in H3_VARS} } holm={holm}\")\n\n\nif __name__ == \"__main__\":\n    {\"dev\": cmd_dev, \"heldout\": cmd_heldout, \"smoke_heldout\": smoke_heldout}[sys.argv[1]]()", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] THINKING · 2026-09-30 01:39:10 UTC

```
Since `method.py` just runs the other pipeline scripts, I'll keep `STEPS` as an overview in the notebook and replay the H1 analysis from `models.py` unchanged on 100 real episodes from `full_method_out.json`. Next I'll build that data subset.
```

### [23] TOOL CALL — Write · 2026-09-30 01:39:10 UTC

```
File: /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/make_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json: a concept-clustered subset (<= 100 episodes) of the artifact's episode panel.

Source: full_method_out.json of art_wxWssKSUR45f (the episode panel exported by report.py). Whole concepts are
sampled per home group (4 DEV groups + 4 held-out groups) so that every group has both R=0 and R=1 episodes.
The full-run headline results (metadata) are copied alongside for comparison in the notebook.

Usage: python make_mini_demo_data.py [path/to/full_method_out.json]"""
import json
import random
import sys
from pathlib import Path

SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/full_method_out.json")
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"
PER_GROUP = 12          # target episodes per home group (8 groups -> ~100 episodes)
MAX_TOTAL = 100
rng = random.Random(20260928)

full = json.loads(SRC.read_text())
ds = {d["dataset"]: d["examples"] for d in full["datasets"]}
pool = ds["episodes_dev_LOGO_oof"] + ds["episodes_heldout_frozen_model"]
by_group: dict[str, dict[int, list]] = {}
for e in pool:
    by_group.setdefault(e["metadata_group"], {}).setdefault(e["metadata_concept_id"], []).append(e)

picked = []
for g in ["CS", "Eng", "BGM", "Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"]:
    concepts = [c for c, eps in by_group[g].items() if len(eps) <= 4]
    rng.shuffle(concepts)
    sel = []
    for c in concepts:
        eps = by_group[g][c]
        if len(sel) + len(eps) > PER_GROUP:
            continue
        sel.extend(eps)
        ys = {e["output"] for e in sel}
        if len(sel) >= PER_GROUP - 1 and ys == {"0", "1"}:
            break
    picked.extend(sel)
picked = picked[:MAX_TOTAL]

meta = full["metadata"]
keep = {k: meta[k] for k in ("method_name", "baseline", "method", "H1_dev", "H1_heldout", "ladder_dev",
                             "ladder_heldout", "gateway_alone_auc", "H3_heldout") if k in meta}
out = {"metadata": {"source": "full_method_out.json (datasets episodes_dev_LOGO_oof + episodes_heldout_frozen_model)",
                    "n_episodes": len(picked), "sampling": "whole concepts per home group, seed 20260928",
                    "full_run_results": keep},
       "episodes": picked}
OUT.write_text(json.dumps(out, indent=1))
from collections import Counter
print(len(picked), Counter(e["metadata_group"] for e in picked), Counter(e["output"] for e in picked),
      len({e["metadata_concept_id"] for e in picked}), f"{OUT.stat().st_size/1e3:.0f} kB")
```

### [24] TOOL RESULT — Write · 2026-09-30 01:39:10 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/make_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json: a concept-clustered subset (<= 100 episodes) of the artifact's episode panel.\n\nSource: full_method_out.json of art_wxWssKSUR45f (the episode panel exported by report.py). Whole concepts are\nsampled per home group (4 DEV groups + 4 held-out groups) so that every group has both R=0 and R=1 episodes.\nThe full-run headline results (metadata) are copied alongside for comparison in the notebook.\n\nUsage: python make_mini_demo_data.py [path/to/full_method_out.json]\"\"\"\nimport json\nimport random\nimport sys\nfrom pathlib import Path\n\nSRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(\n    \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/full_method_out.json\")\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\nPER_GROUP = 12          # target episodes per home group (8 groups -> ~100 episodes)\nMAX_TOTAL = 100\nrng = random.Random(20260928)\n\nfull = json.loads(SRC.read_text())\nds = {d[\"dataset\"]: d[\"examples\"] for d in full[\"datasets\"]}\npool = ds[\"episodes_dev_LOGO_oof\"] + ds[\"episodes_heldout_frozen_model\"]\nby_group: dict[str, dict[int, list]] = {}\nfor e in pool:\n    by_group.setdefault(e[\"metadata_group\"], {}).setdefault(e[\"metadata_concept_id\"], []).append(e)\n\npicked = []\nfor g in [\"CS\", \"Eng\", \"BGM\", \"Med\", \"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]:\n    concepts = [c for c, eps in by_group[g].items() if len(eps) <= 4]\n    rng.shuffle(concepts)\n    sel = []\n    for c in concepts:\n        eps = by_group[g][c]\n        if len(sel) + len(eps) > PER_GROUP:\n            continue\n        sel.extend(eps)\n        ys = {e[\"output\"] for e in sel}\n        if len(sel) >= PER_GROUP - 1 and ys == {\"0\", \"1\"}:\n            break\n    picked.extend(sel)\npicked = picked[:MAX_TOTAL]\n\nmeta = full[\"metadata\"]\nkeep = {k: meta[k] for k in (\"method_name\", \"baseline\", \"method\", \"H1_dev\", \"H1_heldout\", \"ladder_dev\",\n                             \"ladder_heldout\", \"gateway_alone_auc\", \"H3_heldout\") if k in meta}\nout = {\"metadata\": {\"source\": \"full_method_out.json (datasets episodes_dev_LOGO_oof + episodes_heldout_frozen_model)\",\n                    \"n_episodes\": len(picked), \"sampling\": \"whole concepts per home group, seed 20260928\",\n                    \"full_run_results\": keep},\n       \"episodes\": picked}\nOUT.write_text(json.dumps(out, indent=1))\nfrom collections import Counter\nprint(len(picked), Counter(e[\"metadata_group\"] for e in picked), Counter(e[\"output\"] for e in picked),\n      len({e[\"metadata_concept_id\"] for e in picked}), f\"{OUT.stat().st_size/1e3:.0f} kB\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [25] TOOL CALL — Bash · 2026-09-30 01:39:10 UTC

```
python3 make_mini_demo_data.py && python3 -c "
import json,collections;d=json.load(open('mini_demo_data.json'))
c=collections.defaultdict(collections.Counter)
for e in d['episodes']: c[e['metadata_group']][e['output']]+=1
print(dict(c)); print(json.dumps(d['metadata']['full_run_results']['H3_heldout'])[:600])"
```

### [26] TOOL RESULT — Bash · 2026-09-30 01:39:10 UTC

```
{"stdout": "91 Counter({'Eng': 12, 'PHYS': 12, 'MATHDEC': 12, 'CS': 11, 'BGM': 11, 'Med': 11, 'LIFEENV': 11, 'SOC': 11}) Counter({'0': 59, '1': 32}) 43 92 kB\n{'CS': Counter({'0': 7, '1': 4}), 'Eng': Counter({'0': 9, '1': 3}), 'BGM': Counter({'0': 7, '1': 4}), 'Med': Counter({'0': 9, '1': 2}), 'PHYS': Counter({'0': 11, '1': 1}), 'LIFEENV': Counter({'1': 6, '0': 5}), 'SOC': Counter({'1': 7, '0': 4}), 'MATHDEC': Counter({'0': 7, '1': 5})}\n{\"G\": {\"partial_rho\": 0.02950282637789586, \"p\": 0.001999000499750125, \"ci95\": [-0.005645316827696381, 0.06495220976417931]}, \"G_A\": {\"partial_rho\": 0.026181155490031614, \"p\": 0.00399800099950025, \"ci95\": [-0.01115668861449585, 0.06661133096553447]}, \"G_btw\": {\"partial_rho\": 0.04559887078144679, \"p\": 0.0014992503748125937, \"ci95\": [0.009104121849222446, 0.0862495145333611]}, \"REL_home\": {\"partial_rho\": -0.13639675894418873, \"p\": 1.0, \"ci95\": [-0.17351749913750902, -0.10147997097025221]}, \"holm\": {\"G_btw\": 0.004497751124437781, \"G\": 0.004497751124437781, \"G_A\": 0.004497751124437781}, \"verdict\":", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-30 01:41:58 UTC

```
Data subset done: 91 episodes from 43 concepts, 11–12 per home group, with both outcomes in every group. Now I'll write the notebook.
```

### [28] TOOL CALL — Write · 2026-09-30 01:41:58 UTC

```
File: /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/_build_notebook.py

"""Builds code_demo.ipynb (temporary helper, removed after the notebook is final)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
B_MAIN, B_SMALL, N_JOBS = (int(x) for x in (sys.argv[1:4] if len(sys.argv) > 3 else (2, 2, 2)))
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "met... [truncated, 40581 chars total]
```

### [29] TOOL RESULT — Write · 2026-09-30 01:41:58 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/_build_notebook.py", "content": "\"\"\"Builds code_demo.ipynb (temporary helper, removed after the notebook is final).\"\"\"\nimport json\nimport sys\nfrom pathlib import Path\n\nHERE = Path(__file__).resolve().parent\nB_MAIN, B_SMALL, N_JOBS = (int(x) for x in (sys.argv[1:4] if len(sys.argv) > 3 else (2, 2, 2)))\ncells = []\... [truncated, 43094 chars total]
```

### [30] TOOL CALL — Bash · 2026-09-30 01:42:04 UTC

```
python3 _build_notebook.py 2 2 2 && E=/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "runtime $(( $(date +%s)-S ))s"
```

### [31] TOOL RESULT — Bash · 2026-09-30 01:42:34 UTC

```
{"stdout": "wrote 34 cells\n------------------\nrows = []\nfor e in data[\"episodes\"]:\n    inp = json.loads(e[\"input\"])\n    rows.append({\"ci\": inp[\"concept_id\"], \"concept_id\": inp[\"concept_id\"], \"name\": inp[\"concept\"],\n                 \"field\": inp[\"adopting_field\"], \"home\": int(inp[\"home\"]), \"t0\": inp[\"t0\"], \"group\": inp[\"group\"],\n                 \"split\": inp[\"split\"], **inp[\"covariates\"], \"R\": float(e[\"output\"]),\n                 \"n_early\": e[\"metadata_n_early\"], \"n_out\": e[\"metadata_n_out\"],\n                 \"orig_pred_X0\": float(e[\"predict_baseline\"]), \"orig_pred_X1\": float(e[\"predict_gateway\"])})\nF = pd.DataFrame(rows)\nF = F[F.R.notna()].copy()  # R undefined when no labelled outcome work exists (share_out = 0/0); excluded as in dev\nprint(F.groupby([\"split\"]).agg(episodes=(\"R\", \"size\"), concepts=(\"ci\", \"nunique\"), R_rate=(\"R\", \"mean\")))\nF[[\"name\", \"field\", \"home\", \"t0\", \"group\", \"gateway_j\", \"P_j\", \"R\"]].head(8)\n------------------\n\n\n\u001b[31m---------------------------------------------------------------------------\u001b[39m\n\u001b[31mValueError\u001b[39m                                Traceback (most recent call last)\n\u001b[36mCell\u001b[39m\u001b[36m \u001b[39m\u001b[32mIn[10]\u001b[39m\u001b[32m, line 5\u001b[39m\n\u001b[32m      1\u001b[39m rows = []\n\u001b[32m      2\u001b[39m \u001b[38;5;28;01mfor\u001b[39;00m e \u001b[38;5;28;01min\u001b[39;00m data[\u001b[33m\"episodes\"\u001b[39m]:\n\u001b[32m      3\u001b[39m     inp = json.loads(e[\u001b[33m\"input\"\u001b[39m])\n\u001b[32m      4\u001b[39m     rows.append({\"ci\": inp[\"concept_id\"], \"concept_id\": inp[\"concept_id\"], \"name\": inp[\"concept\"],\n\u001b[32m----> \u001b[39m\u001b[32m5\u001b[39m                  \u001b[33m\"field\"\u001b[39m: inp[\u001b[33m\"adopting_field\"\u001b[39m], \u001b[33m\"home\"\u001b[39m: int(inp[\u001b[33m\"home\"\u001b[39m]), \u001b[33m\"t0\"\u001b[39m: inp[\u001b[33m\"t0\"\u001b[39m], \u001b[33m\"group\"\u001b[39m: inp[\u001b[33m\"group\"\u001b[39m],\n\u001b[32m      6\u001b[39m                  \u001b[33m\"split\"\u001b[39m: inp[\u001b[33m\"split\"\u001b[39m], **inp[\u001b[33m\"covariates\"\u001b[39m], \u001b[33m\"R\"\u001b[39m: float(e[\u001b[33m\"output\"\u001b[39m]),\n\u001b[32m      7\u001b[39m                  \u001b[33m\"n_early\"\u001b[39m: e[\u001b[33m\"metadata_n_early\"\u001b[39m], \u001b[33m\"n_out\"\u001b[39m: e[\u001b[33m\"metadata_n_out\"\u001b[39m],\n\u001b[32m      8\u001b[39m                  \u001b[33m\"orig_pred_X0\"\u001b[39m: float(e[\u001b[33m\"predict_baseline\"\u001b[39m]), \u001b[33m\"orig_pred_X1\"\u001b[39m: float(e[\u001b[33m\"predict_gateway\"\u001b[39m])})\n\n\u001b[31mValueError\u001b[39m: invalid literal for int() with base 10: '22;17'\n\nruntime 27s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-30 01:42:40 UTC

```
Some concepts have two home fields ("22;17"), so I'll keep `home` as a string.
```

### [33] TOOL CALL — Bash · 2026-09-30 01:42:40 UTC

```
sed -i 's/"home": int(inp\["home"\]), /"home": inp["home"], /' _build_notebook.py && grep -n '"home": inp' _build_notebook.py && python3 _build_notebook.py 2 2 2 && E=/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "runtime $(( $(date +%s)-S ))s"
```

### [34] TOOL RESULT — Bash · 2026-09-30 01:43:41 UTC

```
{"stdout": "436:                 \"field\": inp[\"adopting_field\"], \"home\": inp[\"home\"], \"t0\": inp[\"t0\"], \"group\": inp[\"group\"],\nwrote 34 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 201916 bytes to code_demo.ipynb\nruntime 58s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-09-30 01:43:45 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code' or i<3: continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(f'--[{i}]', o['text'][-1500:])
        elif o['output_type'] in ('execute_result','display_data'): print(f'--[{i}]', str(o['data'].get('text/plain',''))[:1500], list(o['data'].keys()))
        elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
"
```

### [36] TOOL RESULT — Bash · 2026-09-30 01:43:45 UTC

```
{"stdout": "--[6] ['91 episodes; whole concepts per home group, seed 20260928\\n']\n--[10] ['                lexicon              python lexicon.py\\n', '                prescreen_sample     python prescreen.py sample\\n', '                prescreen_names      python prescreen.py names\\n', '                wikidata             python wikidata_aliases.py\\n', '                prescreen_aliases    python prescreen.py aliases\\n', '                scan                 python scan_full.py --workers 5\\n', '                merge                python scan_full.py --merge\\n', '                onset_match          python frame.py match\\n', '                backbones            python backbones.py\\n', '                bench                python grounding.py bench\\n', '                filter               python grounding.py filter\\n', '                onset_grounded       python frame.py grounded\\n', '                precision            python grounding.py precision\\n', '                frame                python frame.py build\\n', '                features             python features.py\\n', '                tests                python tests/test_units.py\\n', '                t1                   python checks.py t1\\n', '                t3                   python checks.py t3\\n', '[replayed here] dev_freeze           python models.py dev\\n', '                unseal               python seal.py unseal\\n', '[replayed here] heldout              python models.py heldout\\n', '                pigeonhole_fix       python fix_pigeonhole.py\\n', '                replicate            python checks.py replicate\\n', '                exploratory_domains  python exploratory_domains.py\\n', '                report               python report.py\\n', '                variants             python make_variants.py\\n', '                audit                python audit.py\\n', '                audit_placebo        python audit_placebo.py\\n']\n--[18] ['                 episodes  concepts    R_rate\\n', 'split                                        \\n', 'DEV                    45        20  0.288889\\n', 'HELDOUT_LIFEENV        11         4  0.545455\\n', 'HELDOUT_MATHDEC        12         7  0.416667\\n', 'HELDOUT_PHYS           12         6  0.083333\\n', 'HELDOUT_SOC            11         6  0.636364\\n']\n--[18] ['                   name  field home    t0 group  gateway_j      P_j    R\\n', '0          Bloom filter     22   17  2006    CS    0.24272  0.46230  1.0\\n', '1          Bloom filter     26   17  2006    CS    0.17001  0.27797  0.0\\n', '2  Context-free grammar     13   17  2004    CS    0.41902  0.41901  0.0\\n', '3  Context-free grammar     22   17  2004    CS    0.24272  0.53061  0.0\\n', '4     Assembly language     22   17  2006    CS    0.24272  0.46230  1.0\\n', '5     Assembly language     33   17  2006    CS    0.02816  0.13576  0.0\\n', '6     Texture synthesis     22   17  2004    CS    0.24272  0.52768  1.0\\n', '7      XML Schema (W3C)     14   17  2003    CS    0.07712  0.26932  0.0'] ['text/html', 'text/plain']\n--[20] ['01:43:33|INFO   |DEV: 45 episodes / 20 concepts, R rate 0.289\\n']\n--[20] ['01:43:33|INFO   |DEV primary dAUC=-0.0096 (AUC0 0.728)\\n']\n--[20] ['       auc_X0    auc_X1      dauc     n\\n', 'CS   0.821429  0.821429  0.000000  11.0\\n', 'Eng  0.666667  0.666667  0.000000  12.0\\n', 'BGM  0.642857  0.607143 -0.035714  11.0\\n', 'Med  0.555556  0.555556  0.000000  11.0'] ['text/html', 'text/plain']\n--[22] ['01:43:35|INFO   |bootstrap done in 2s; CI [-0.018802521008403295, 0.01179971988795514]\\n']\n--[22] [\"DL pooled over DEV groups: {'k': 2, 'pooled': 0.0, 'se': 5.551115123125783e-17, 'tau2': 0.0, 'I2': 0.0, 'Q': 0.0}\\n\"]\n--[24] [\"rival: {'dauc_relatedness_pair': 0.00480769230769218, 'dauc_gateway': -1.1102230246251565e-16, 'diff_gateway_minus_relatedness': -0.004807692307692291, 'diff_boot_ci95': [-0.14697958381006862, 0.007379564740656057], 'relatedness_boot_ci95': [0.11463637013729981, 0.11665176868802447], 'gateway_boot_ci95': [-0.0323432136727688, 0.12403133342868053]}\\n\", \"ladder dAUC: {'L1_iter1_base': -0.0048, 'L2_plus_relatedness': -0.0096, 'L3_plus_Pj': -0.0096, 'L4_full_X0': -0.0096, 'L0_size_only': -0.0072}\\n\", 'gateway alone AUC (DEV): 0.667\\n', 'conditional logit: {\\'n_episodes_informative\\': 31, \\'n_concepts_informative\\': 10, \\'error\\': \"ValueError(\\'need covariance of parameters for computing (unnormalized) covariances\\')\", \\'method\\': \\'BinomialBayesMixedGLM (fallback)\\', \\'beta_gateway_std\\': -0.4971442487027575, \\'se\\': 0.7991499689248269, \\'z\\': -0.6220913070566884}\\n']\n--[24] ['/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages/statsmodels/base/model.py:595: HessianInversionWarning: Inverting hessian failed, no bse or cov_params available\\n', \"  warnings.warn('Inverting hessian failed, no bse or cov_params '\\n\"]\n--[26] ['01:43:35|INFO   |FROZEN (demo, in memory): sha256=bf52c04c1ff0f558\\n']\n--[29] ['01:43:35|INFO   |HELD-OUT dAUC=-0.0019 CI [-0.040040531015037566, 0.00984786184210517]\\n']\n--[29] ['          n n_concepts    auc_X0    auc_X1 dauc   boot_se\\n', 'PHYS     12          6  0.818182  0.818182  0.0       NaN\\n', 'LIFEENV  11          4       0.8       0.8  0.0  0.071429\\n', 'SOC      11          6  0.714286  0.714286  0.0  0.071429\\n', 'MATHDEC  12          7  0.857143  0.857143  0.0       0.0'] ['text/html', 'text/plain']\n--[31] ['/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages/statsmodels/base/model.py:595: HessianInversionWarning: Inverting hessian failed, no bse or cov_params available\\n', \"  warnings.warn('Inverting hessian failed, no bse or cov_params '\\n\"]\n--[31] [\"01:43:35|INFO   |H1 verdict (demo subset) DISCONFIRMED: {'pooled_dauc_ge_0.05': False, 'refit_ci_gt0': False, 'sign_ge3_of_4_evaluable': False, 'n_groups_positive': 0}\\n\"]\n--[31] [\"rival: {'dauc_relatedness_pair': -0.033138401559454134, 'relatedness_ci95': [-0.027586620002692224, -0.0029370036344055946], 'dauc_gateway': -0.0038986354775827348, 'gateway_ci95': [-0.10759469645981974, 0.006159779243505364], 'diff_gateway_minus_relatedness': 0.0292397660818714}\\n\", \"ladder dAUC: {'L1_iter1_base': -0.0292, 'L2_plus_relatedness': -0.0097, 'L3_plus_Pj': 0.0019, 'L4_full_X0': -0.0019, 'L0_size_only': -0.0136}\\n\", 'gateway alone AUC (held-out): 0.464\\n', 'conditional logit: {\\'n_episodes_informative\\': 19, \\'n_concepts_informative\\': 8, \\'error\\': \"ValueError(\\'need covariance of parameters for computing (unnormalized) covariances\\')\", \\'method\\': \\'BinomialBayesMixedGLM (fallback)\\', \\'beta_gateway_std\\': 0.9647957133469997, \\'se\\': 0.7906329548024198, \\'z\\': 1.220282695638589}\\n', 'held-out phase runtime 0.4s\\n']\n--[33] ['                                             demo (refit here) full-run preds on subset full run (all episodes)\\n', 'DEV LOGO dAUC                                          -0.0096                  +0.0048                 +0.0000\\n', '  95% CI                                    [-0.0188, +0.0118]                               [-0.0007, +0.0005]\\n', 'held-out dAUC                                          -0.0019                  -0.0078                 -0.0000\\n', '  95% CI                                    [-0.0400, +0.0098]                               [-0.0006, +0.0003]\\n', 'held-out AUC(X0)                                         0.793                    0.854                   0.837\\n', 'gateway-alone AUC DEV                                    0.667                                            0.605\\n', 'gateway-alone AUC held-out                               0.464                                            0.506\\n', 'held-out dAUC relatedness pair                         -0.0331                                          +0.0034\\n', 'H1 verdict                      DISCONFIRMED (3 of 6 criteria)                                     DISCONFIRMED\\n', '\\n', 'H3 (full run, held-out concepts): partial Spearman with O2r_resid given B5\\n', '          partial_rho  p_perm  holm_p\\n', 'G              0.0295  0.0020  0.0045\\n', 'G_A            0.0262  0.0040  0.0045\\n', 'G_btw          0.0456  0.0015  0.0045\\n', 'REL_home      -0.1364  1.0000     NaN\\n']\n--[33] ['<Figure size 1600x430 with 3 Axes>'] ['image/png', 'text/plain']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] ASSISTANT · 2026-09-30 01:43:53 UTC

```
The notebook runs end to end with minimum config (58s including installs). Next I'll scale the bootstraps: an intermediate step first, then the original 2000/500.
```

### [38] TOOL CALL — Bash · 2026-09-30 01:43:53 UTC

```
python3 _build_notebook.py 200 50 4 && E=/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; echo "runtime $(( $(date +%s)-S ))s"; nproc
```

### [39] TOOL RESULT — Bash · 2026-09-30 01:45:51 UTC

```
{"stdout": "wrote 34 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 201951 bytes to code_demo.ipynb\nruntime 107s\n2", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-09-30 01:45:59 UTC

```
At 200/50 it took 107s on 2 cores. Scaled linearly, the original 2000/500 would need about 500s of compute plus installs, which is too close to the 600s limit. Next I'll try 1000/200.
```

### [41] TOOL CALL — Bash · 2026-09-30 01:45:59 UTC

```
python3 _build_notebook.py 1000 200 4 && E=/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; echo "runtime $(( $(date +%s)-S ))s"
```

### [42] TOOL RESULT — Bash · 2026-09-30 01:48:49 UTC

```
{"stdout": "wrote 34 cells\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 201955 bytes to code_demo.ipynb\nruntime 162s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-30 01:48:55 UTC

```
1000/200 finished in 162s, well under the estimate. Next I'll try the original 2000/500.
```

### [44] TOOL CALL — Bash · 2026-09-30 01:48:55 UTC

```
cp code_demo.ipynb /tmp/aii_nb_test_envs/code_demo_1000_200.ipynb 2>/dev/null; python3 _build_notebook.py 2000 500 4 && E=/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; echo "runtime $(( $(date +%s)-S ))s"
```

### [45] TOOL RESULT — Bash · 2026-09-30 01:50:59 UTC

```
{"stdout": "wrote 34 cells\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 201959 bytes to code_demo.ipynb\nruntime 123s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-30 01:51:03 UTC

```
The original values (2000/500, 4 jobs) run in 123s, so the notebook keeps them. Next I'll check the outputs and the figure.
```

### [47] TOOL CALL — Bash · 2026-09-30 01:51:03 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
print(''.join(nb['cells'][8]['source']))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='error': print('ERR',i,o['ename'])
        if o['output_type']=='stream' and i in (22,24,29,31,33): print(f'--[{i}]', ''.join(o['text'])[-1400:])
        if o['output_type']=='display_data' and 'image/png' in o['data']:
            open('/tmp/aii_nb_test_envs/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; grep -c GITHUB_DATA_URL code_demo.ipynb
```

### [48] TOOL RESULT — Bash · 2026-09-30 01:51:05 UTC

```
{"stdout": "B_MAIN = 2000          # refit-bootstrap draws for the primary dAUC CI                     (original: 2000; SMOKE mode: 60)\nB_SMALL = 500          # draws for seed-stability, rival head-to-head, ladder bootstraps     (original: 500;  SMOKE mode: 20)\nN_JOBS = 4            # joblib workers                                                     (original: 4)\nMIN_CONCEPTS_EVAL = 3  # a held-out group is 'evaluable' with >= this many concepts           (original: 15; the demo has ~5 per group)\n--[22] 01:49:45|INFO   |bootstrap done in 25s; CI [-0.0514825248281131, 0.06906347684001128]\n\n--[22] DL pooled over DEV groups: {'k': 4, 'pooled': -0.010710708530826686, 'se': 0.028733205578547267, 'tau2': 0.0, 'I2': 0.0, 'Q': 0.3243785940207567}\n\n--[24] rival: {'dauc_relatedness_pair': 0.00480769230769218, 'dauc_gateway': -1.1102230246251565e-16, 'diff_gateway_minus_relatedness': -0.004807692307692291, 'diff_boot_ci95': [-0.12223410210479181, 0.08463533873960138], 'relatedness_boot_ci95': [-0.06165960682089715, 0.11217644424540968], 'gateway_boot_ci95': [-0.03804713804713808, 0.07011178476695695]}\nladder dAUC: {'L1_iter1_base': -0.0048, 'L2_plus_relatedness': -0.0096, 'L3_plus_Pj': -0.0096, 'L4_full_X0': -0.0096, 'L0_size_only': -0.0072}\ngateway alone AUC (DEV): 0.667\nconditional logit: {'n_episodes_informative': 31, 'n_concepts_informative': 10, 'error': \"ValueError('need covariance of parameters for computing (unnormalized) covariances')\", 'method': 'BinomialBayesMixedGLM (fallback)', 'beta_gateway_std': -0.49715064789518937, 'se': 0.7991529310180793, 'z': -0.6220970087187759}\n\n--[24] /tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages/statsmodels/base/model.py:595: HessianInversionWarning: Inverting hessian failed, no bse or cov_params available\n  warnings.warn('Inverting hessian failed, no bse or cov_params '\n\n--[29] 01:50:25|INFO   |HELD-OUT dAUC=-0.0019 CI [-0.14858698156682018, 0.03479871175523343]\n\n--[31] /tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages/statsmodels/base/model.py:595: HessianInversionWarning: Inverting hessian failed, no bse or cov_params available\n  warnings.warn('Inverting hessian failed, no bse or cov_params '\n\n--[31] 01:50:53|INFO   |H1 verdict (demo subset) DISCONFIRMED: {'pooled_dauc_ge_0.05': False, 'refit_ci_gt0': False, 'sign_ge3_of_4_evaluable': False, 'n_groups_positive': 0}\n\n--[31] rival: {'dauc_relatedness_pair': -0.033138401559454134, 'relatedness_ci95': [-0.1415370813397129, 0.033510101010100976], 'dauc_gateway': -0.0038986354775827348, 'gateway_ci95': [-0.19203485838779963, 0.02796394195915725], 'diff_gateway_minus_relatedness': 0.0292397660818714}\nladder dAUC: {'L1_iter1_base': -0.0292, 'L2_plus_relatedness': -0.0097, 'L3_plus_Pj': 0.0019, 'L4_full_X0': -0.0019, 'L0_size_only': -0.0136}\ngateway alone AUC (held-out): 0.464\nconditional logit: {'n_episodes_informative': 19, 'n_concepts_informative': 8, 'error': \"ValueError('need covariance of parameters for computing (unnormalized) covariances')\", 'method': 'BinomialBayesMixedGLM (fallback)', 'beta_gateway_std': 0.9647976117150855, 'se': 0.7906330455651375, 'z': 1.220284956626695}\nheld-out phase runtime 44.8s\n\n--[33]                                              demo (refit here) full-run preds on subset full run (all episodes)\nDEV LOGO dAUC                                          -0.0096                  +0.0048                 +0.0000\n  95% CI                                    [-0.0515, +0.0691]                               [-0.0007, +0.0005]\nheld-out dAUC                                          -0.0019                  -0.0078                 -0.0000\n  95% CI                                    [-0.1486, +0.0348]                               [-0.0006, +0.0003]\nheld-out AUC(X0)                                         0.793                    0.854                   0.837\ngateway-alone AUC DEV                                    0.667                                            0.605\ngateway-alone AUC held-out                               0.464                                            0.506\nheld-out dAUC relatedness pair                         -0.0331                                          +0.0034\nH1 verdict                      DISCONFIRMED (3 of 6 criteria)                                     DISCONFIRMED\n\nH3 (full run, held-out concepts): partial Spearman with O2r_resid given B5\n          partial_rho  p_perm  holm_p\nG              0.0295  0.0020  0.0045\nG_A            0.0262  0.0040  0.0045\nG_btw          0.0456  0.0015  0.0045\nREL_home      -0.1364  1.0000     NaN\n\n2", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Read · 2026-09-30 01:51:05 UTC

```
/tmp/aii_nb_test_envs/fig.png
```

### [50] TOOL RESULT — Read · 2026-09-30 01:51:05 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [51] ASSISTANT · 2026-09-30 01:51:15 UTC

```
The figure renders correctly. Last steps: delete the temporary builder, remove the absolute server path from the data script, and write the README, manifest and output JSON.
```

### [52] TOOL CALL — Bash · 2026-09-30 01:51:15 UTC

```
rm _build_notebook.py && python3 - <<'EOF'
from pathlib import Path
p=Path("make_mini_demo_data.py"); s=p.read_text()
s=s.replace('''SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/full_method_out.json")''',
'''SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("full_method_out.json")  # the experiment artifact's output''')
p.write_text(s)
EOF
grep -n "SRC =" make_mini_demo_data.py; grep -l "/ai-inventor" code_demo.ipynb make_mini_demo_data.py mini_demo_data.json; ls -la; du -sh .
```

### [53] TOOL RESULT — Bash · 2026-09-30 01:51:15 UTC

```
{"stdout": "14:SRC = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(\"full_method_out.json\")  # the experiment artifact's output\ncode_demo.ipynb\ntotal 3914\ndrwxrwxrwx 3 aii-agent aii-agent 1089424 Sep 30 01:51 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000258 Sep 30 01:46 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 01:36 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 01:37 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  619136 Sep 30 01:51 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent  201994 Sep 30 01:50 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent    2515 Sep 30 01:51 make_mini_demo_data.py\n-rw-rw-rw- 1 aii-agent aii-agent   92012 Sep 30 01:39 mini_demo_data.json\n2.0M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-30 01:51:19 UTC

```
The executed notebook contains an `/ai-inventor` path somewhere. I'll find where.
```

### [55] TOOL CALL — Bash · 2026-09-30 01:51:19 UTC

```
grep -o '.\{120\}/ai-inventor.\{80\}' code_demo.ipynb | head; grep -o '.\{60\}/tmp/aii_nb.\{60\}' code_demo.ipynb | head -3
```

### [56] TOOL RESULT — Bash · 2026-09-30 01:51:19 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] TOOL CALL — Bash · 2026-09-30 01:51:21 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    s=json.dumps(c)
    for key in ('/ai-inventor','/tmp/aii'):
        k=s.find(key)
        if k>=0: print(i,key,s[max(0,k-100):k+80])
"
```

### [58] TOOL RESULT — Bash · 2026-09-30 01:51:21 UTC

```
{"stdout": "5 /ai-inventor 1:49:19.955147Z\"}}, \"outputs\": [], \"source\": [\"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/\n24 /tmp/aii 529310180793, 'z': -0.6220970087187759}\\n\"]}, {\"name\": \"stderr\", \"output_type\": \"stream\", \"text\": [\"/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages\n31 /tmp/aii  \"2026-09-30T01:50:53.747047Z\"}}, \"outputs\": [{\"name\": \"stderr\", \"output_type\": \"stream\", \"text\": [\"/tmp/aii_nb_test_envs/art_wxWssKSUR45f-0b45df29118e/lib/python3.12/site-packages", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] THINKING · 2026-09-30 01:51:29 UTC

```
The `/ai-inventor` match is just the GitHub org name, and the `/tmp` venv paths are harmless statsmodels warning output—I'll remove those two stderr blocks from the saved notebook.
```

### [60] TOOL CALL — Bash · 2026-09-30 01:51:29 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
n=0
for c in nb['cells']:
    if c['cell_type']=='code':
        k=len(c['outputs'])
        c['outputs']=[o for o in c['outputs'] if not (o['output_type']=='stream' and o['name']=='stderr' and 'HessianInversionWarning' in ''.join(o['text']))]
        n+=k-len(c['outputs'])
json.dump(nb,open('code_demo.ipynb','w'),indent=1)
print('removed',n)
"; grep -c '/tmp/aii' code_demo.ipynb; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-2/experiment-5/demo/mini_demo_data.json"' code_demo.ipynb; grep -c 'urlopen(GITHUB_DATA_URL)' code_demo.ipynb
```

### [61] TOOL RESULT — Bash · 2026-09-30 01:51:29 UTC

```
{"stdout": "removed 2\n0\n0\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [62] TOOL CALL — Bash · 2026-09-30 01:51:33 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
src='\n'.join(''.join(c['source']) if isinstance(c['source'],list) else c['source'] for c in nb['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-2/experiment-5/demo/mini_demo_data.json\"' in src)
print(sum(1 for c in nb['cells'] for o in c.get('outputs',[]) if o['output_type']=='error'))
"
```

### [63] TOOL RESULT — Bash · 2026-09-30 01:51:33 UTC

```
{"stdout": "True\n0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] ASSISTANT · 2026-09-30 01:51:49 UTC

```
Checks pass. Now the README, manifest and output JSON.
```

### [65] TOOL CALL — Write · 2026-09-30 01:51:49 UTC

```
File: /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/README.md

# Demo: Do hub fields keep new concepts? Held-out test

A runnable Colab/Jupyter demo of the experiment artifact `art_wxWssKSUR45f`. The artifact is a sealed held-out test of whether an
adopting field's frozen gateway (eigenvector) centrality predicts retention of a newly adopted concept beyond a strong baseline.
The full-run verdict was H1 **DISCONFIRMED**, with held-out dAUC −0.00001 [−0.0006, +0.0003].

## What this demo does
The artifact's `method.py` is an orchestrator. It runs about 28 pipeline scripts, starting with a full scan of the OpenAlex
snapshot, so it cannot run in a notebook. `code_demo.ipynb`:

1. Lists `method.py`'s `STEPS` verbatim and marks the analysis steps it replays: `models.py dev` and `models.py heldout`.
2. Copies the analysis functions from `models.py` without changes to the algorithms: the `L2Logit` Newton-IRLS fit, LOGO
   out-of-fold dAUC, the concept-clustered refit bootstrap, DerSimonian–Laird pooling, the sign test, the conditional logit,
   `score_heldout` and the explanatory baseline ladder.
3. Runs them on a 91-episode, concept-clustered subset of the real episode panel: 45 DEV episodes and 46 held-out.
4. Compares the demo numbers with the full-run results in a table and a 3-panel figure.

The bootstrap sizes are the original ones (`B_MAIN=2000`, `B_SMALL=500`, `N_JOBS=4`). A full execution, including package
installs, takes about 2–3 minutes on 2 CPU cores.

The demo leaves three things out. They need data beyond the subset:
* the cohort replication
* the field-FE LPM
* the rewired-backbone placebo

Because of this, the demo verdict applies 3 of the 6 pre-registered H1 criteria. H3 is shown from the full-run results only.

## Layout
| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed. It loads data from GitHub and falls back to a local copy. |
| `mini_demo_data.json` | 91 episodes with covariates `X0`, `gateway_j`, outcome `R` and the full-run predictions, plus the full-run headline results in `metadata.full_run_results`. |
| `make_mini_demo_data.py` | Rebuilds `mini_demo_data.json` from the artifact's `full_method_out.json`. |
| `.aii/manifest.yaml` | Storage manifest. No heavy files are present. |

## How to run
* **Colab:** open `code_demo.ipynb` and run all cells. The install cell only installs `loguru`, because Colab already provides the rest.
* **Locally:** use Python 3.12 and run `jupyter nbconvert --to notebook --execute code_demo.ipynb`. The install cell pins Colab's
  versions of numpy, pandas, scipy, scikit-learn, statsmodels and matplotlib.
* **Regenerate the data subset:** `python make_mini_demo_data.py path/to/full_method_out.json`.

## Restoring removed files
Nothing in this directory is marked `delete`, so there is nothing to restore. The notebook installs its own dependencies when it runs.
```

### [66] TOOL RESULT — Write · 2026-09-30 01:51:49 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_wxWssKSUR45f/README.md", "content": "# Demo: Do hub fields keep new concepts? Held-out test\n\nA runnable Colab/Jupyter demo of the experiment artifact `art_wxWssKSUR45f`. The artifact is a sealed held-out test of whether an\nadopting field's frozen gateway (eigenvector) centrality predicts retention of a newly adopted concept beyond a strong baseline.\nThe full-run verdict was H1 **DISCONFIRMED**, with held-out dAUC −0.00001 [−0.0006, +0.0003].\n\n## What this demo does\nThe artifact's `method.py` is an orchestrator. It runs about 28 pipeline scripts, starting with a full scan of the OpenAlex\nsnapshot, so it cannot run in a notebook. `code_demo.ipynb`:\n\n1. Lists `method.py`'s `STEPS` verbatim and marks the analysis steps it replays: `models.py dev` and `models.py heldout`.\n2. Copies the analysis functions from `models.py` without changes to the algorithms: the `L2Logit` Newton-IRLS fit, LOGO\n   out-of-fold dAUC, the concept-clustered refit bootstrap, DerSimonian–Laird pooling, the sign test, the conditional logit,\n   `score_heldout` and the explanatory baseline ladder.\n3. Runs them on a 91-episode, concept-clustered subset of the real episode panel: 45 DEV episodes and 46 held-out.\n4. Compares the demo numbers with the full-run results in a table and a 3-panel figure.\n\nThe bootstrap sizes are the original ones (`B_MAIN=2000`, `B_SMALL=500`, `N_JOBS=4`). A full execution, including package\ninstalls, takes about 2–3 minutes on 2 CPU cores.\n\nThe demo leaves three things out. They need data beyond the subset:\n* the cohort replication\n* the field-FE LPM\n* the rewired-backbone placebo\n\nBecause of this, the demo verdict applies 3 of the 6 pre-registered H1 criteria. H3 is shown from the full-run results only.\n\n## Layout\n| Path | What it is |\n|---|---|\n| `code_demo.ipynb` | The demo notebook, executed. It loads data from GitHub and falls back to a local copy. |\n| `mini_demo_data.json` | 91 episodes with covariates `X0`, `gateway_j`, outcome `R` and the full-run predictions, plus the full-run headline results in `metadata.full_run_results`. |\n| `make_mini_demo_data.py` | Rebuilds `mini_demo_data.json` from the artifact's `full_method_out.json`. |\n| `.aii/manifest.yaml` | Storage manifest. No heavy files are present. |\n\n## How to run\n* **Colab:** open `code_demo.ipynb` and run all cells. The install cell only installs `loguru`, because Colab already provides the rest.\n* **Locally:** use Python 3.12 and run `jupyter nbconvert --to notebook --execute code_demo.ipynb`. The install cell pins Colab's\n  versions of numpy, pandas, scipy, scikit-learn, statsmodels and matplotlib.\n* **Regenerate the data subset:** `python make_mini_demo_data.py path/to/full_method_out.json`.\n\n## Restoring removed files\nNothing in this directory is marked `delete`, so there is nothing to restore. The notebook installs its own dependencies when it runs.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [67] TOOL CALL — Bash · 2026-09-30 01:51:49 UTC

```
printf 'entries: []\n' > .aii/manifest.yaml && printf '{\n  "out_expected_files": {\n    "notebook": "code_demo.ipynb",\n    "mini_data_file": "mini_demo_data.json"\n  }\n}\n' > .terminal_claude_agent_struct_out.json && cat .terminal_claude_agent_struct_out.json .aii/manifest.yaml && ls -la
```

### [68] TOOL RESULT — Bash · 2026-09-30 01:51:49 UTC

```
{"stdout": "{\n  \"out_expected_files\": {\n    \"notebook\": \"code_demo.ipynb\",\n    \"mini_data_file\": \"mini_demo_data.json\"\n  }\n}\nentries: []\ntotal 3965\ndrwxrwxrwx 3 aii-agent aii-agent 1093887 Sep 30 01:51 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000281 Sep 30 01:46 ..\ndrwxrwxrwx 2 aii-agent aii-agent    1200 Sep 30 01:51 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 01:37 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  665594 Sep 30 01:51 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent     113 Sep 30 01:51 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    2833 Sep 30 01:51 README.md\n-rw-rw-rw- 1 aii-agent aii-agent  201315 Sep 30 01:51 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent    2515 Sep 30 01:51 make_mini_demo_data.py\n-rw-rw-rw- 1 aii-agent aii-agent   92012 Sep 30 01:39 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [69] ASSISTANT · 2026-09-30 01:51:59 UTC

```
I built the demo notebook and its data file. It runs end to end in the clean Colab-like test venv, with no errors, in about 2–3 minutes including installs (limit: 10 minutes).

**Deviation from the brief:** the artifact's `method.py` only orchestrates the pipeline. It launches about 28 scripts in turn, starting with a full scan of the OpenAlex snapshot, so it can't be converted cell by cell. Instead the notebook:
- **Pipeline overview:** copies `method.py`'s step list verbatim and marks the two analysis steps it replays (`models.py dev` and `models.py heldout`).
- **Analysis code:** copies the functions from `models.py` without changing any algorithms, then runs the development-group phase and the held-out phase.
- **Comparison:** ends with a table and a 3-panel figure setting the demo results beside the full-run results.

**Data:** `mini_demo_data.json` holds 91 real episodes (45 development, 46 held-out) from 43 whole concepts, 11–12 per home group, with both outcomes in every group. It also carries the full-run headline numbers for the comparison. The field-retention covariate (`P_j`) comes precomputed from the full panel, because recomputing it on 91 episodes would be meaningless.

**Scaling:** the bootstraps started at 2 draws and went to 200/50, then 1000/200, then the original 2000/500 with 4 workers. All the original values fit, so the notebook uses them.

**Gaps you should know about:**
- **Verdict uses 3 of 6 criteria.** The demo checks only these three:
  - pooled dAUC ≥ 0.05
  - bootstrap CI above zero
  - at least 3 of 4 groups positive

  The other three need data outside the subset: the 2010–14 cohort, the field fixed-effects regression, and the rewired-network placebo. The notebook says so in the text and in the table. On these three criteria the demo verdict is DISCONFIRMED, the same as the full run.
- **H3 is not recomputed.** The concept-level result is shown from the full-run numbers only.
- **Conditional logit falls back.** On this small subset the conditional logit can't estimate its standard errors, so the original code's own fallback (a Bayesian mixed model) is what runs.
- **Demo numbers are noisy.** With about 45 episodes per phase, the demo shows the method runs; it isn't evidence either way. For example, held-out dAUC is −0.0019 with CI [−0.149, +0.035].

**Process notes:**
- **Construction:** no todo tool was available, so I didn't create the todo list. I also built the notebook with a script rather than NotebookEdit, and deleted that script afterwards.
- **Stripped warnings:** I removed two harmless statsmodels warnings from the saved outputs, because they printed local `/tmp` venv paths.
- **Verification:** the exact `GITHUB_DATA_URL` line is in the notebook, and data loads from GitHub with a local fallback.

**Cleanup files:** the manifest is empty because nothing in the workspace is over 10 MB. The README covers layout, how to run it and the restore section. The output JSON was written to `.terminal_claude_agent_struct_out.json`.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `make_mini_demo_data.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
