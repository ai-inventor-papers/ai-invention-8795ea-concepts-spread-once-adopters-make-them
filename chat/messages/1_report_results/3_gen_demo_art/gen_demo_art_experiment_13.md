# gen_demo_art_experiment_13 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_13` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:35:09 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:35:17 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/.shared_cache`
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
id: art_NGXDZpLy-s1z
type: experiment
title: Is research-topic churn real or small-sample noise?
summary: >-
  Cache-only ($0 LLM) confound check of the home-only churn/novelty signal on 13,444 selection concepts (DEV 4670, OLDHO 3214,
  COH1014 4195, COH1517 1365; n_home_early>=10). Gate T0 reproduces EXP10 exactly (diff 0; cohort OPEN_home +0.0906, NOV_res
  +0.1337, edge_persistence -0.1123). A validated vectorised engine (lib/fast6.py == ego.concept_core to 1e-16) computes raw
  indicators and noise-controlled variants: V1 fixed-n rarefaction (n=5/10/20, 50 draws), V2 within-concept year-permutation
  null (200) + Chao-2005 Jaccard, V3 configuration nulls (200 igraph backbone rewires for density, k-matched set null, numba
  curveball for persistence), V4 split-half reliability; composites NOVCHURN_* and OPEN_home_clean/exc with constants sealed
  before outcome join. Findings (partial Spearman with O2r_m50 | B5+R2, B=2000, results/clean_vs_raw_psp.json): mechanical
  verdict PARTLY_THIN. Pooled NOVCHURN_raw +0.116 [0.09,0.14]; V2 excess NOVCHURN_exc +0.008 (retention 0.06; P1 fails: 0.40
  COH1517, 0.05 OLDHO); fixed-n NOVCHURN_rare10 +0.078 (retention 0.68; 0.76 COH1517, 0.64 OLDHO); Chao/curveball composites
  keep 91-100%. Raw persistence is 66% explained by its own V2 null mean (thin-sample share), rho with log n +0.72, and the
  V2 null mean predicts the outcome (-0.120) at least as strongly as raw persistence (-0.088): the signal is a static topical-dispersion
  property of the home topic mix, not temporal partner turnover. V2 excess variants have split-half SB ~0.01-0.05 and PC2
  (planted churn) fails, so V2 cannot adjudicate temporal churn at ~10 papers/year. Degree normalisation helps: z_dens_cfg
  -0.091 (raw density null), OPEN_home_clean +0.115 vs OPEN_home +0.092 same sample (diff +0.022 [0.011,0.034]); P2 z_pers_cfg
  -0.116 holds; P3 holds. Reliability SB: NOVCHURN_raw 0.48, OPEN_home 0.49, OPEN_home_clean 0.58, outcome O2r_m50 0.895;
  disattenuated pooled NOVCHURN_raw 0.178 (approx). Frame-N joint power (OPEN R3&R5&NOVCHURN R3): 0.07/0.26 at n=800/2500
  with T3, 0.31/0.75 with T2. Reusable outputs: data/clean_variants.parquet (per-concept raw+clean variants, no outcomes),
  results/reliability.json, size_dependence.json, power_frame_n.json, frozen_spec.json + frozen_constants_S1b.json (hash-sealed),
  method_out.json (7,748 examples; DEV-fitted OLS predictions B5 +/- variants). Selection data, outcomes previously unsealed:
  robustness evidence, not confirmation. Independently re-derived (rederive.py, tests/headline_check.py, different code path;
  shuffled-outcome controls null): P1-P3 psp, pooled NOVCHURN_raw/exc/rare10, null-mean persistence, OPEN_home_clean psp,
  SB of NOVCHURN_raw, thin-sample share. Not re-derived: power simulation, DL pooling, disattenuation CIs.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] ASSISTANT · 2026-09-29 21:35:21 UTC

```
I'll start by loading the required skills and inspecting the workspace and artifact.
```

### [4] TOOL CALL — Skill · 2026-09-29 21:35:21 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-29 21:35:21 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-29 21:35:21 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-29 21:35:21 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-29 21:35:21 UTC

```
ls -la && ls -la .aii 2>/dev/null; A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; ls -la $A; du -sh $A/* 2>/dev/null | sort -h | tail -30
```

### [9] TOOL RESULT — Bash · 2026-09-29 21:35:23 UTC

```
{"stdout": "total 2960\ndrwxrwxrwx 3 aii-agent aii-agent 1002543 Sep 29 21:35 .\ndrwxrwxrwx 7 aii-agent aii-agent 2000267 Sep 29 21:34 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:34 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:35 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   25994 Sep 29 21:35 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:34 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002543 Sep 29 21:35 ..\ntotal 38533\ndrwxrwxrwx 10 aii-agent aii-agent  2027924 Sep 29 09:02 .\ndrwxrwxrwx  7 aii-agent aii-agent  3000249 Sep 29 05:17 ..\ndrwxrwxrwx  2 aii-agent aii-agent   100800 Sep 29 06:28 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 29 05:18 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent     9154 Sep 29 06:28 .aii_worker_result.json\n-rw-rw-rw-  1 aii-agent aii-agent  1918369 Sep 29 06:28 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     3354 Sep 29 06:26 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    13917 Sep 29 06:27 README.md\ndrwxrwxrwx  3 aii-agent aii-agent  2025210 Sep 29 09:02 data\ndrwxrwxrwx  2 aii-agent aii-agent  1056430 Sep 29 06:19 figures\n-rw-rw-rw-  1 aii-agent aii-agent 12422709 Sep 29 06:26 full_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent  1009698 Sep 29 18:01 lib\ndrwxrwxrwx  2 aii-agent aii-agent  1010536 Sep 29 06:24 logs\n-rw-rw-rw-  1 aii-agent aii-agent    12025 Sep 29 06:21 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 11688840 Sep 29 06:21 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    15065 Sep 29 06:26 mini_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent        1 Sep 29 06:25 models\n-rw-rw-rw-  1 aii-agent aii-agent    12774 Sep 29 06:26 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent      839 Sep 29 06:25 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent     6760 Sep 29 05:56 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent     7108 Sep 29 06:26 reproducibility.md\n-rwxrwxrwx  1 aii-agent aii-agent      772 Sep 29 06:23 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent  2000137 Sep 29 06:25 results\n-rw-rw-rw-  1 aii-agent aii-agent     5133 Sep 29 05:24 s0_gate.py\n-rw-rw-rw-  1 aii-agent aii-agent    10781 Sep 29 05:31 s1_freeze.py\n-rw-rw-rw-  1 aii-agent aii-agent     9379 Sep 29 05:31 s2_variants.py\n-rw-rw-rw-  1 aii-agent aii-agent    15659 Sep 29 05:36 s3_nulls.py\n-rw-rw-rw-  1 aii-agent aii-agent    13130 Sep 29 05:39 s4_composites.py\n-rw-rw-rw-  1 aii-agent aii-agent     6646 Sep 29 05:40 s4b_outcome_rel.py\n-rw-rw-rw-  1 aii-agent aii-agent     7685 Sep 29 05:44 s5_size.py\n-rw-rw-rw-  1 aii-agent aii-agent     8735 Sep 29 05:43 s6_assoc.py\n-rw-rw-rw-  1 aii-agent aii-agent    15374 Sep 29 05:53 s7_verdict.py\n-rw-rw-rw-  1 aii-agent aii-agent    10981 Sep 29 06:19 s8_power.py\ndrwxrwxrwx  2 aii-agent aii-agent  1002156 Sep 29 06:25 tests\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/models\n1.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/pyproject.toml\n1.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/restore.sh\n5.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s0_gate.py\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4b_outcome_rel.py\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/rederive.py\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/reproducibility.md\n8.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s5_size.py\n9.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s6_assoc.py\n9.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s2_variants.py\n11K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s1_freeze.py\n11K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s8_power.py\n12K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/method.py\n13K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/preview_method_out.json\n13K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py\n14K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/README.md\n15K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/mini_method_out.json\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s7_verdict.py\n1002K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/logs\n1.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/figures\n3.3M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/results\n12M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/full_method_out.json\n12M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/method_out.json\n257M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/data", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-29 21:35:25 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat $A/method.py; echo ----; cat $A/pyproject.toml; echo ----; head -c 4000 $A/preview_method_out.json; echo; ls -la $A/data $A/data/* $A/lib $A/results | head -80
```

### [11] TOOL RESULT — Bash · 2026-09-29 21:35:25 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.\n\nStages (each a standalone, resumable script; run in this order by `python method.py --run-all`):\n  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)\n  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)\n  s1_freeze.py          frozen spec + seal (before any outcome jo... [truncated, 24123 chars total]
```

### [12] TOOL CALL — Bash · 2026-09-29 21:35:35 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; ls -la $A/lib $A/results $A/figures; cat $A/lib/common.py | head -80; echo ----; cat $A/lib/tables.py
```

### [13] TOOL RESULT — Bash · 2026-09-29 21:35:35 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/figures:\ntotal 3578\ndrwxrwxrwx  2 aii-agent aii-agent 1056430 Sep 29 06:19 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027924 Sep 29 09:02 ..\n-rw-rw-rw-  1 aii-agent aii-agent  113379 Sep 29 06:17 forest_raw_vs_clean.png\n-rw-rw-rw-  1 aii-agent aii-agent  228829 Sep 29 05:50 persistence_vs_n.png\n-rw-rw-rw-  1 aii-agent aii-agent  131645 Sep 29 06:20 power_curves.png\n-rw-rw-rw-  1 aii-agent aii-agent  104000 Sep 29 06:17 reliability_bars.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib:\ntotal 3067\ndrwxrwxrwx  2 aii-agent aii-agent 1009698 Sep 29 18:01 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027924 Sep 29 09:02 ..\n-rw-rw-rw-  1 aii-agent aii-agent    5891 Sep 29 05:23 common.py\n-rw-rw-rw-  1 aii-agent aii-agent    4421 Sep 29 05:23 common3.py\n-rw-rw-rw-  1 aii-agent aii-agent   10723 Sep 29 05:23 common5.py\n-rw-rw-rw-  1 aii-agent aii-agent    1759 Sep 29 05:23 design.py\n-rw-rw-rw-  1 aii-agent aii-agent   12932 Sep 29 05:23 ego.py\n-rw-rw-rw-  1 aii-agent aii-agent    2020 Sep 29 05:23 ego_ctx.py\n-rw-rw-rw-  1 aii-agent aii-agent   11737 Sep 29 05:27 fast6.py\n-rw-rw-rw-  1 aii-agent aii-agent    4856 Sep 29 05:41 fastpsp.py\n-rw-rw-rw-  1 aii-agent aii-agent    3629 Sep 29 05:24 jobs.py\n-rw-rw-rw-  1 aii-agent aii-agent    9137 Sep 29 05:23 ladder.py\n-rw-rw-rw-  1 aii-agent aii-agent    9585 Sep 29 05:33 nullkern.py\n-rw-rw-rw-  1 aii-agent aii-agent    2049 Sep 29 05:23 outc.py\n-rw-rw-rw-  1 aii-agent aii-agent    8080 Sep 29 05:23 rq1stats.py\n-rw-rw-rw-  1 aii-agent aii-agent     378 Sep 29 05:31 s2_cfg.py\n-rw-rw-rw-  1 aii-agent aii-agent    1452 Sep 29 05:30 seal.py\n-rw-rw-rw-  1 aii-agent aii-agent    8655 Sep 29 05:23 stats_core.py\n-rw-rw-rw-  1 aii-agent aii-agent    2011 Sep 29 05:42 tables.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/results:\ntotal 5344\ndrwxrwxrwx  2 aii-agent aii-agent 2000137 Sep 29 06:25 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027924 Sep 29 09:02 ..\n-rw-rw-rw-  1 aii-agent aii-agent  693635 Sep 29 06:17 clean_vs_raw_psp.json\n-rw-rw-rw-  1 aii-agent aii-agent  514025 Sep 29 06:15 clean_vs_raw_psp_cells.json\n-rw-rw-rw-  1 aii-agent aii-agent    4140 Sep 29 06:23 deviations.json\n-rw-rw-rw-  1 aii-agent aii-agent    4134 Sep 29 05:47 frozen_constants_S1b.json\n-rw-rw-rw-  1 aii-agent aii-agent    9939 Sep 29 05:31 frozen_spec.json\n-rw-rw-rw-  1 aii-agent aii-agent    1615 Sep 29 05:25 gate_t0.json\n-rw-rw-rw-  1 aii-agent aii-agent    1272 Sep 29 06:25 headline_check.json\n-rw-rw-rw-  1 aii-agent aii-agent     879 Sep 29 06:19 placebo_calibration.json\n-rw-rw-rw-  1 aii-agent aii-agent     575 Sep 29 05:46 planted_checks.json\n-rw-rw-rw-  1 aii-agent aii-agent   20480 Sep 29 06:20 power_frame_n.json\n-rw-rw-rw-  1 aii-agent aii-agent    2933 Sep 29 06:21 prediction_check.json\n-rw-rw-rw-  1 aii-agent aii-agent    2144 Sep 29 06:18 rederive.json\n-rw-rw-rw-  1 aii-agent aii-agent   38862 Sep 29 05:52 reliability.json\n-rw-rw-rw-  1 aii-agent aii-agent   37658 Sep 29 05:49 reliability_x.json\n-rw-rw-rw-  1 aii-agent aii-agent  100198 Sep 29 05:50 size_dependence.json\n-rw-rw-rw-  1 aii-agent aii-agent    1371 Sep 29 06:22 unit_tests.json\n-rw-rw-rw-  1 aii-agent aii-agent    2038 Sep 29 05:29 unit_tests_fast6.json\n-rw-rw-rw-  1 aii-agent aii-agent     820 Sep 29 05:42 unit_tests_fastpsp.json\n-rw-rw-rw-  1 aii-agent aii-agent    1139 Sep 29 05:49 unit_tests_nulls.json\n-rw-rw-rw-  1 aii-agent aii-agent     852 Sep 29 05:46 v3_nulls_full.json\n\"\"\"Shared constants, paths and small helpers for the RQ1 held-out pipeline.\n\nThe title analyser / surface normaliser / matcher are imported from common5.py (EXP5's common.py, copied verbatim)\nso the matching is byte-identical to the EXP5 scan that defined the frame.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\n\nLIB = Path(__file__).resolve().parent\nROOT = LIB.parent\nsys.path.insert(0, str(LIB))\n\nDATA = ROOT / \"data\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nMODELS = ROOT / \"models\"\nPASSA = ROOT / \"passA\" / \"parts\"\nPASSB = ROOT / \"passB\" / \"parts\"\nfor _d in (DATA, RES, LOGS, FIGS, MODELS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nRUN_ROOT = Path(os.environ.get(\"AII_RUN_ROOT\", str(ROOT.parents[3])))\nEXP5 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_5\"\nEXP3 = RUN_ROOT / \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\"\nEXP8 = RUN_ROOT / \"3_invention_loop/iter_3/gen_art/gen_art_experiment_8\"\n# EXP16 patch: inputs and data are read (read-only) from EXP10; everything written stays under ROOT\nSRC10 = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_10\"\nINPUTS = SRC10 / \"inputs\"\nDATA_IN = SRC10 / \"data\"\nEXP6 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"\nEVAL1 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_evaluation_1\"\nO5DIR = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nMATCH_Y0, MATCH_Y1 = 2000, 2016      # t0 in 2003..2014 -> feature windows t0-3..t0+2 lie in 2000..2016\nTAG_MIN = 0.3\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nUNITS = HELD_GROUPS + [\"COH_DEVHOME\", \"COH_OTHER\"]\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef mix64(x: np.ndarray) -> np.ndarray:\n    \"\"\"splitmix64 finaliser (identical to EXP5 scan_full.mix64).\"\"\"\n    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)\n    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)\n    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)\n    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)\n\n\ndef works_files() -> list[tuple[int, str, int, int]]:\n    man = json.loads((ROOT / \"snapshot/works_manifest.json\").read_text())\n    return [(i, f[\"url\"].replace(\"s3://openalex/\", \"\"), f[\"meta\"][\"content_length\"], f[\"meta\"][\"record_count\"])\n            for i, f in enumerate(man[\"files\"])]\n\n\ndef source_field_lut() -> tuple[np.ndarray, np.ndarray]:\n----\n\"\"\"Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.\nSelection data, outcomes previously unsealed by EXP5/EXP8/EXP10.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN\nfrom ladder import rung_design\n\nCOV = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\", \"type\", \"generic\", \"level\",\n       \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\", \"newborn\", \"t0\", \"agroup\", \"label_coverage_early\",\n       \"home_coverage_early\", \"n_all_early\", \"O2r_m50\", \"O2r_resid\"]\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"]\n\n\ndef load_tables() -> dict[str, pd.DataFrame]:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    cv = cv.drop(columns=[c for c in (\"t0\",) if c in cv.columns])\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\"] + COV)\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\"] + COV + [\"window_flag\"])\n    cv = cv.drop(columns=[c for c in (\"agroup\",) if c in cv.columns])\n    e = cv[cv.frame == \"exp5\"].merge(fe, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    e[\"window_flag\"] = 0\n    c = cv[cv.frame == \"cohort\"].merge(ac, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    pooled = pd.concat([e, c], ignore_index=True)\n    pooled[\"window_flag\"] = pooled.window_flag.fillna(0).astype(int)\n    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}\n    out[\"POOLED\"] = pooled\n    return out\n\n\ndef design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:\n    Bc, Cc = rung_design(df, rung, drop_group=drop_group)\n    if pooled and df.body.nunique() > 1:\n        bs = sorted(df.body.unique())[1:]\n        Cc = pd.concat([Cc, pd.DataFrame({f\"body_{b}\": (df.body == b).astype(float) for b in bs}, index=df.index)],\n                       axis=1)\n        Cc = Cc.loc[:, Cc.std() > 0]\n    return Bc.to_numpy(float), Cc.to_numpy(float)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-29 21:35:43 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cd $A; ls $A/.venv 2>/dev/null | head -2; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data/ | head; python3 - <<'EOF'
import json
V=json.load(open('results/clean_vs_raw_psp.json')); print(V.keys()); print(V['verdict'].keys()); print(type(V['headline_R2_O2r_m50']), len(V['headline_R2_O2r_m50'])); h=V['headline_R2_O2r_m50'][0]; print({k:(v if not isinstance(v,dict) else list(v.keys())) for k,v in h.items()})
rel=json.load(open('results/reliability.json')); print(rel.keys(), list(rel['variants'].keys())[:40]); print(rel['outcome']['O2r_m50']['pooled'])
pw=json.load(open('results/power_frame_n.json')); print(pw['plain_language'])
sz=json.load(open('results/size_dependence.json')); print(sz['thin_sample_share']['POOLED'])
spec=json.load(open('results/frozen_spec.json')); print(spec['exp10_prediction_models']['B5'])
print(json.dumps(json.load(open('results/prediction_check.json')))[:1500])
EOF
```

### [15] TOOL RESULT — Bash · 2026-09-29 21:35:43 UTC

```
{"stdout": "analysis_cohort.parquet\nbg_topics.npz\ncohort_candidates.csv\ncohort_candidates_gated.csv\ncohort_predictions.parquet\nconcept_types.csv\ncontrols.csv\ncovariates_cohort.parquet\ncovariates_exp5.parquet\nego_open\ndict_keys(['label', 'B', 'seed', 'resampling_unit', 'groups', 'disattenuated', 'F6_contingency', 'predictions', 'verdict', 'holm', 'headline_R2_O2r_m50', 'cells', 'confounds_removed'])\ndict_keys(['verdict', 'DEGREE_ARTEFACT_PERSISTENCE', 'clauses', 'label'])\n<class 'list'> 23\n{'variant': 'NOVCHURN_raw', 'DEV': ['psp', 'ci', 'n'], 'OLDHO': ['psp', 'ci', 'n'], 'COH1014': ['psp', 'ci', 'n'], 'COH1517': ['psp', 'ci', 'n'], 'POOLED': ['psp', 'ci', 'n']}\ndict_keys(['method', 'notes', 'variants', 'outcome']) ['new_edge_rate__raw', 'n_comm_W3__raw', 'participation__raw', 'NOV_res__raw', 'ego_density_W3__raw', 'edge_persistence__raw', 'NOVCHURN_raw', 'OPEN_home', 'NOV_res_exc', 'edge_persistence_exc', 'ego_density_W3_exc', 'new_edge_rate_exc', 'NOV_res_zperm', 'edge_persistence_zperm', 'ego_density_W3_zperm', 'NOV_res_rare5', 'edge_persistence_rare5', 'ego_density_W3_rare5', 'z_pers_cfg', 'z_dens_cfg', 'z_dens_k', 'edge_persistence_nullmean', 'NOVCHURN_exc', 'NOVCHURN_zperm', 'NOVCHURN_rare5', 'NOVCHURN_cfg', 'OPEN_home_clean', 'OPEN_home_exc']\n{'r_half': 0.8099349043555275, 'SB': 0.8949878831624887, 'n': 7748, 'SB_ci': [0.8904772486259972, 0.8988260126382953], 'SB_boot_sd': 0.002030466617169411}\nAt n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.\n{'R2': 0.6596194882526905, 'n': 12330, 'coef': [-0.0010767111256983803, 0.9746957571903339]}\n{'coef': [4.766039224098753, -0.05511164665586871, 0.008765664104716067, -0.42563667808882066, 1.6369692811444325, 0.2840929545239369], 'mu': {'logvol': 4.387217461299273, 'growth_c': 0.13591487868338373, 'offhome_share': 0.2628714872549475, 'entropy': 0.7831561038968538, 'reach': 3.228179741051028}, 'sd': {'logvol': 0.3554731095580416, 'growth_c': 0.43536192389233147, 'offhome_share': 0.19848326295216012, 'entropy': 0.4615603694432812, 'reach': 1.550401785313322}}\n{\"note\": \"OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)\", \"coef\": {\"B5\": [4.741089772404464, -0.06804331615114713, 0.016388333733478488, -0.406903700770024, 1.592823828887357, 0.3167518054848495], \"B5_plus_NOVCHURN_raw\": [4.761006866155193, -0.03299651604617797, 0.01261448756066987, -0.42944795146740805, 1.5694784603644882, 0.31822557960802045, 0.18248951439219754], \"B5_plus_NOVCHURN_exc\": [4.741295106450962, -0.06796436730522869, 0.016421974425589667, -0.40664295196568057, 1.5925916600012568, 0.3167162330705365, -0.0065696966887872], \"B5_plus_NOVCHURN_cfg\": [4.747372192520593, -0.050183538922654106, 0.012753361414263373, -0.4107547899809194, 1.5826607948744529, 0.3133902947990248, 0.14892150785436734], \"B5_plus_OPEN_home\": [4.70605345345373, -0.08029229574081918, -0.017204893404418983, -0.3904254670001875, 1.5669140635803154, 0.3071971026723472, 0.2723005431840688], \"B5_plus_OPEN_home_clean\": [4.6839746355706975, -0.0646304815065352, -0.009262789105233125, -0.3965453117211448, 1.568633056671445, 0.30486973438454074, 0.3175921708950457]}, \"OLDHO\": {\"B5\": 0.7051373001226132, \"B5_plus_NOVCHURN_raw\": 0.7101084462185041, \"B5_plus_NOVCHURN_exc\": 0.7050944917206757, \"B5_plus_NOVCHURN_cfg\": 0.7068478577727112, \"B5_plus_OPEN_home\": 0.7067743632263194, \"B5_plus_OPEN_home_clean\": 0.7069992391675923, \"n\": 1797, \"gain_vs_B5\": {\"B5_plus_NOVCHURN_raw\": 0.004971146095890888, \"B5_plus_NOVCHURN_exc\": -4.280840193748858e-05, \"B5_plus_NOVCHURN_cfg\": 0.00171", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-29 21:35:47 UTC

```
python3 -c "import pandas, pyarrow, numpy, scipy; print(pandas.__version__, pyarrow.__version__)"; which uv
```

### [17] TOOL RESULT — Bash · 2026-09-29 21:35:49 UTC

```
{"stdout": "2.3.3 25.0.0\n/usr/bin/uv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-29 21:36:11 UTC

```
mkdir -p /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/scripts && cat > /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/scripts/make_mini_data.py <<'EOF'
"""Build mini_demo_data.json from the gen_art_experiment_16 artifact (read-only).

100 concepts (25 per body: DEV, OLDHO, COH1014, COH1517), spread evenly over the O2r_m50 range within each body,
plus the small result summaries (frozen B5 constants, headline psp, P1-P3, reliability, size, power) that
method.py's build_outputs() reads from results/*.json."""
import json, math, sys
from pathlib import Path
import numpy as np

ART = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16")
sys.path.insert(0, str(ART / "lib"))
from tables import load_tables  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "mini_demo_data.json"
N_PER_BODY = 25
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
INPUT_COLS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
              "participation__raw", "NOVCHURN_raw", "OPEN_home", "NOV_res_rare10", "edge_persistence_rare10",
              "NOVCHURN_rare10", "NOV_res_rare5", "edge_persistence_rare5", "NOVCHURN_rare5", "NOV_res_exc",
              "edge_persistence_exc", "edge_persistence_nullmean", "NOVCHURN_exc", "EP_chao", "NOVCHURN_chao",
              "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean",
              "OPEN_home_exc"]
COLS = ["concept_id", "name", "body", "agroup", "t0", "n_home_early", "O2r_m50", "O2r_resid"] + B5 + INPUT_COLS


def clean(v):
    if isinstance(v, (np.floating, float)):
        return None if not math.isfinite(float(v)) else round(float(v), 6)
    if isinstance(v, np.integer):
        return int(v)
    return v if isinstance(v, (int, str)) or v is None else str(v)


T = load_tables()["POOLED"]
T = T[np.isfinite(T.O2r_m50) & np.all(np.isfinite(T[B5].to_numpy(float)), 1)].reset_index(drop=True)
rows = []
for body in ("DEV", "OLDHO", "COH1014", "COH1517"):
    s = T[T.body == body].sort_values("O2r_m50").reset_index(drop=True)
    idx = np.unique(np.linspace(0, len(s) - 1, N_PER_BODY).round().astype(int))  # evenly spread over outcome range
    for _, r in s.iloc[idx].iterrows():
        rows.append({c: clean(r[c]) for c in COLS})

R = ART / "results"
spec = json.loads((R / "frozen_spec.json").read_text())
V = json.loads((R / "clean_vs_raw_psp.json").read_text())
rel = json.loads((R / "reliability.json").read_text())
pw = json.loads((R / "power_frame_n.json").read_text())
sz = json.loads((R / "size_dependence.json").read_text())
pc = json.loads((R / "prediction_check.json").read_text())
meta = {
    "description": "Mini subset of the EXP16 selection concepts (25 per body, spread over O2r_m50) plus the small "
                   "full-run result summaries that method.py build_outputs() reads.",
    "n_full_pooled_finite_outcome": int(len(T)),
    "frozen_spec": {"exp10_prediction_models": {"B5": spec["exp10_prediction_models"]["B5"]}},
    "clean_vs_raw_psp": {"verdict": V["verdict"], "predictions": V["predictions"],
                          "headline_R2_O2r_m50": V["headline_R2_O2r_m50"]},
    "reliability": {"variants": {k: {"pooled": {"SB": v["pooled"]["SB"]}} for k, v in rel["variants"].items()},
                    "outcome": {"O2r_m50": {"pooled": {"SB": rel["outcome"]["O2r_m50"]["pooled"]["SB"]}}}},
    "power_frame_n": {"plain_language": pw["plain_language"]},
    "size_dependence": {"thin_sample_share": {"POOLED": sz["thin_sample_share"]["POOLED"]}},
    "full_run_prediction_check": pc,
}
out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts", "examples": rows}]}
OUT.write_text(json.dumps(out, indent=1, default=lambda o: None))
print(OUT, len(rows), OUT.stat().st_size)
EOF
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z && python3 scripts/make_mini_data.py && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));e=d['datasets'][0]['examples'];print(e[0]);import collections;print(collections.Counter(x['body'] for x in e)); print(sum(any(x[c] is None for c in ['NOVCHURN_exc','OPEN_home_clean','NOVCHURN_cfg']) for x in e))"
```

### [19] TOOL RESULT — Bash · 2026-09-29 21:36:13 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/mini_demo_data.json 100 171903\n{'concept_id': 2779619083, 'name': 'Essure', 'body': 'DEV', 'agroup': 'BGM+Med', 't0': 2007, 'n_home_early': 91, 'O2r_m50': 1.0, 'O2r_resid': -3.555508, 'logvol': 4.574711, 'growth_c': 0.060625, 'offhome_share': 0.01087, 'entropy': 0.05996, 'reach': 1, 'NOV_res__raw': None, 'edge_persistence__raw': 0.466667, 'ego_density_W3__raw': 1.0, 'new_edge_rate__raw': 0.0, 'n_comm_W3__raw': 3.0, 'participation__raw': 0.65625, 'NOVCHURN_raw': None, 'OPEN_home': -0.141717, 'NOV_res_rare10': None, 'edge_persistence_rare10': 0.105, 'NOVCHURN_rare10': None, 'NOV_res_rare5': None, 'edge_persistence_rare5': 0.035714, 'NOVCHURN_rare5': None, 'NOV_res_exc': None, 'edge_persistence_exc': -0.023699, 'edge_persistence_nullmean': 0.490366, 'NOVCHURN_exc': None, 'EP_chao': 0.589709, 'NOVCHURN_chao': None, 'z_dens_cfg': 12.917785, 'z_dens_k': 7.374662, 'z_pers_cfg': None, 'excess_pers_cfg': 0.466667, 'NOVCHURN_cfg': None, 'OPEN_home_clean': 0.546166, 'OPEN_home_exc': 0.476757}\nCounter({'DEV': 25, 'OLDHO': 25, 'COH1014': 25, 'COH1517': 25})\n49", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] ASSISTANT · 2026-09-29 21:36:25 UTC

```
Building the mini dataset is done (100 concepts, 25 per body). Now I'm writing the notebook.
```

### [21] TOOL CALL — Bash · 2026-09-29 21:36:25 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; grep -n "def jdump" -A8 $A/lib/common.py; python3 -c "import nbformat; print(nbformat.__version__)"
```

### [22] TOOL RESULT — Bash [ERROR] · 2026-09-29 21:36:25 UTC

```
Error: Exit code 1
114:def jdump(obj, path: Path) -> None:
115-    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))
116-
117-
118-def add_deviation(key: str, text: str) -> None:
119-    p = RES / "deviations.json"
120-    d = json.loads(p.read_text()) if p.exists() else {}
121-    d[key] = text
122-    p.write_text(json.dumps(d, indent=1))
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'nbformat'
```

### [23] TOOL CALL — Bash · 2026-09-29 21:36:27 UTC

```
sed -n 95,116p /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/common.py
```

### [24] TOOL RESULT — Bash · 2026-09-29 21:36:27 UTC

```
{"stdout": "    return h.hexdigest()\n\n\ndef _clean(o):\n    if isinstance(o, dict):\n        return {str(k): _clean(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [_clean(v) for v in o]\n    if isinstance(o, np.ndarray):\n        return _clean(o.tolist())\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, (np.bool_,)):\n        return bool(o)\n    if isinstance(o, (np.floating, float)):\n        return None if not math.isfinite(float(o)) else float(o)\n    return o\n\n\ndef jdump(obj, path: Path) -> None:\n    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Write · 2026-09-29 21:37:37 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/scripts/build_notebook.py

"""Writes code_demo.ipynb (plain nbformat-4 JSON; no nbformat dependency needed)."""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "code_demo.ipynb"
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": s.strip("\n")})


md(r"""
# Is research-topic churn real or small-sample noise?

**A thin-sample confound check of the home-only churn/novelty signal, demonstrated on 100 concepts.**

The research artifact asks whether a concept's *neighbourhood churn* — how quickly its co-occurring topics
turn over in the early years — really predicts later spread, or whether it is an artefact of thin samples
(about 10 home papers a year). The full pipeline (stages `s0`–`s8`, run by `method.py --run-all`) computed, for
13,444 selection concepts in four bodies (DEV, OLDHO, COH1014, COH1517):

* **raw** ego-network indicators (`NOV_res`, `edge_persistence`, `ego_density_W3`, …) and the composites
  `NOVCHURN_raw` / `OPEN_home`;
* **noise-controlled variants**: V1 fixed-n rarefaction (`*_rare5`, `*_rare10`), V2 within-concept year-permutation
  null excess (`*_exc`) and Chao Jaccard (`EP_chao`), V3 configuration nulls (`z_dens_cfg`, `z_pers_cfg`, …), and the
  cleaned composites `NOVCHURN_*`, `OPEN_home_clean` / `OPEN_home_exc`;
* partial Spearman correlations with the outcome `O2r_m50`, reliability, size dependence and a power simulation.

**This notebook shows `method.py`, the orchestrator's final step (`build_outputs`).** That step:
1. standardises the five baseline covariates **B5** with the frozen EXP10 constants,
2. fits OLS models (B5 alone, and B5 plus each churn variant) on **DEV only**,
3. applies them to the held-out bodies and reports the out-of-DEV Spearman correlation with `O2r_m50`
   (the gain over B5 alone should be about 0),
4. writes one example per concept in `exp_gen_sol_out` format together with the headline verdict metadata.

The per-concept table and the full-run result summaries come from `mini_demo_data.json`: 25 concepts per body,
spread evenly over the outcome range. With 100 concepts instead of 7,748 the correlations are noisy. The
full-run values are shown next to them for comparison.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT pre-installed on Colab, always install
_pip('loguru==0.7.3')

# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
""")

md(r"""
## Imports

This is the original import block of `method.py`. The artifact's `lib/common.py` helpers (`jdump` and the path
constants) are not shipped with the demo, so the two small helpers `build_outputs` uses (`_clean`, `jdump`) are
copied verbatim below. `RES` and `ROOT` point at a local output folder. `matplotlib` is added for the final plots.
""")

code(r"""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

import matplotlib.pyplot as plt


# --- copied verbatim from the artifact's lib/common.py (only what build_outputs needs) ---
def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return _clean(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else float(o)
    return o


def jdump(obj, path: Path) -> None:
    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))
""")

md(r"""
## Load the demo data

The data loads from the GitHub URL, with a local fallback so the same code runs in Colab and on a local
machine.
""")

code(r"""
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json"
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
""")

code(r"""
data = load_data()
print("examples:", len(data["datasets"][0]["examples"]))
print("full-run pooled concepts with finite outcome:", data["metadata"]["n_full_pooled_finite_outcome"])
""")

md(r"""
## Configuration

* `N_PER_BODY` sets how many of the 25 demo concepts per body to use. The original run used every concept with a
  finite `O2r_m50`: 7,748 in total.
* `MIN_N_SPEARMAN` is the original rule in `build_outputs`: a body's Spearman correlation is reported only when
  it has more than this many concepts. It is set to 20, as in `method.py`. Because of this rule,
  `N_PER_BODY` must be at least 21 for any out-of-DEV correlation to appear.
* `OUT_DIR` is where `prediction_check.json` and `method_out.json` are written. The original wrote them to
  `results/` and to the repository root.
""")

code(r"""
N_PER_BODY = 25          # max 25 in mini_demo_data.json (original: all concepts, 7,748 pooled)
MIN_N_SPEARMAN = 20      # original: `if ok.sum() > 20`
OUT_DIR = Path("demo_outputs")

OUT_DIR.mkdir(exist_ok=True)
ROOT = OUT_DIR           # method.py writes method_out.json to ROOT
RES = OUT_DIR            # ... and prediction_check.json to RES
""")

md(r"""
## Constants from `method.py`

* **B5** lists the five baseline covariates: log volume, growth, off-home share, entropy and reach.
* **PRED_X** maps each prediction model to the churn variant it adds to B5.
* **INPUT_COLS** lists the per-concept indicators copied into each output example. Suffixes: `__raw` is the raw
  indicator, `_rare5`/`_rare10` is V1 fixed-n rarefaction, `_exc` is V2 excess over the year-permutation null,
  `_nullmean` is the V2 null mean, `EP_chao` is the V2b Chao Jaccard, and `z_*_cfg`/`z_dens_k` are the V3
  configuration-null z-scores.

The original file also defines `STAGES`, `run_stages()`, `concept_key_check()` and `exp12_crosscheck()`. Those
re-run the upstream pipeline scripts or read about 250 MB of parquet files and other artifacts' outputs, so the
demo leaves them out. Their results are marked as unavailable in the metadata below.
""")

code(r"""
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
""")

md(r"""
## `build_outputs()`, part 1: inputs

In the original, `spec`, `V`, `rel`, `pw` and `sz` are read from `results/*.json`, and `T` comes from
`tables.load_tables()["POOLED"]`, which joins `clean_variants.parquet` with the EXP10 covariates and outcomes.
Here they come from `data`. Missing values arrive as JSON `null` and become `NaN` again, so the `np.isfinite`
logic works as in the original. The last line, which keeps only concepts with a finite outcome, is unchanged.
""")

code(r"""
meta_in = data["metadata"]
spec = meta_in["frozen_spec"]                  # was: json.loads((RES / "frozen_spec.json").read_text())
pm = spec["exp10_prediction_models"]["B5"]
V = meta_in["clean_vs_raw_psp"]                # was: results/clean_vs_raw_psp.json
rel = meta_in["reliability"]                   # was: results/reliability.json
pw = meta_in["power_frame_n"]                  # was: results/power_frame_n.json
sz = meta_in["size_dependence"]                # was: results/size_dependence.json

# was: T = load_tables()["POOLED"]
T = pd.DataFrame(data["datasets"][0]["examples"])
T = T.groupby("body", sort=False).head(N_PER_BODY).reset_index(drop=True)   # demo: subsample per body
for c in T.columns:
    if c not in ("name", "body", "agroup"):
        T[c] = pd.to_numeric(T[c], errors="coerce").astype(float)           # JSON null -> NaN
T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
print(T.body.value_counts().to_dict())
print("frozen B5 mu:", pm["mu"])
T.head()
""")

md(r"""
## Part 2: fit OLS on DEV and predict every body

The B5 covariates are standardised with the frozen EXP10 `mu`/`sd`, **not** refitted on this sample. For each
model that adds a churn variant, NaN values are imputed with the DEV median and flagged. The OLS coefficients
come from the DEV rows only and are then applied to every concept. This code is unchanged.
""")

code(r"""
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
for nm in coefs:
    print(f"{nm:26s} n_DEV_fit={int(dev.sum()):3d}  coef={np.round(coefs[nm], 3).tolist()}")
""")

md(r"""
## Part 3: out-of-DEV check

For each held-out body, this computes the Spearman correlation between each model's prediction and the observed
`O2r_m50`, and the gain over B5 alone. In the full run every gain was about 0 (below +0.005). The churn variants
add almost nothing to *out-of-sample prediction* beyond B5, although their partial correlations are non-zero.
The code is unchanged except that `20` is now the config variable `MIN_N_SPEARMAN`.
""")

code(r"""
chk = {"note": "OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)", "coef": coefs}
for body in ("OLDHO", "COH1014", "COH1517"):
    m = (T.body == body).to_numpy()
    ent = {}
    for nm, p in preds.items():
        ok = m & np.isfinite(p)
        ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > MIN_N_SPEARMAN else None
    ent["n"] = int(m.sum())
    ent["gain_vs_B5"] = {nm: (ent[nm] - ent["B5"]) if ent[nm] is not None and ent["B5"] is not None else None
                         for nm in PRED_X if nm != "B5"}
    chk[body] = ent
jdump(chk, RES / "prediction_check.json")
print(json.dumps({b: {k: v for k, v in chk[b].items() if k != "gain_vs_B5"} for b in ("OLDHO", "COH1014", "COH1517")},
                 indent=1))
""")

md(r"""
## Part 4: one output example per concept (`exp_gen_sol_out` format)

Each example stores the concept's raw and cleaned indicators as the JSON `input` and `O2r_m50` as the `output`.
It also holds one `predict_<model>` field per OLS model and metadata flags that show which variants were imputed
or missing. This code is unchanged.
""")

code(r"""
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
print(len(exs), "examples; first one:")
print(json.dumps(exs[0], indent=1)[:1500])
""")

md(r"""
## Part 5: verdict metadata and `method_out.json`

This part assembles the headline metadata from the full-run summaries:
* the mechanical verdict (`PARTLY_THIN`);
* whether predictions P1–P3 hold;
* the headline partial Spearman (psp, controlling for B5 and R2) of each variant with `O2r_m50`;
* the Spearman–Brown reliabilities;
* the thin-sample share of raw persistence;
* the plain-language power statement.

`concept_key_check()` and `exp12_crosscheck()` are replaced by an "unavailable in demo" note, because they read
external artifacts. The rest is unchanged.
""")

code(r"""
vd = V["verdict"]
head = {h["variant"]: {b: h[b].get("psp") for b in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED")}
        for h in V["headline_R2_O2r_m50"]}
_NA = {"available": False, "note": "needs external artifacts; not run in the demo"}
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
        "concept_key_check": _NA, "exp12_home_crosscheck": _NA,   # was: concept_key_check(), exp12_crosscheck()
        "n_examples": len(exs), "prediction_models": "OLS on DEV (B5 standardised with EXP10 frozen mu/sd); "
                                                     "NaN variants imputed with the DEV median (flagged)"}
out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts", "examples": exs}]}
(ROOT / "method_out.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)
                                                 and not math.isfinite(o) else str(o)))
logger.info(f"method_out.json: {len(exs)} examples; verdict {vd['verdict']}")
print("P1-P3 hold:", meta["predictions_P1_P3"])
print("thin-sample share of raw persistence (R2):", round(meta["thin_sample_share_R2"], 3))
print("power:", meta["power_plain_language"])
""")

md(r"""
## Results and visualisation

1. **Out-of-DEV Spearman**: each model's value on the demo subset next to the full run. The absolute values
   differ because of the small sample, but in both the churn variants barely change the B5 baseline.
2. **Headline partial Spearman** (full run, pooled, 95% bootstrap CI) of the raw and noise-controlled churn
   variants. The V2 excess variants (`*_exc`, `*_zperm`) collapse to about 0. Rarefaction keeps part of the
   signal, and Chao and configuration-null composites keep most of it. This is the `PARTLY_THIN` verdict.
3. **Predicted vs observed** `O2r_m50` on the demo concepts for B5 alone and for B5 + `NOVCHURN_raw`.
""")

code(r"""
full_pc = meta_in["full_run_prediction_check"]
rows = []
for body in ("OLDHO", "COH1014", "COH1517"):
    for nm in PRED_X:
        rows.append({"body": body, "model": nm, "demo_spearman": chk[body][nm],
                     "full_spearman": full_pc[body][nm], "demo_n": chk[body]["n"], "full_n": full_pc[body]["n"]})
res = pd.DataFrame(rows)
pd.set_option("display.width", 160)
print("Out-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run")
print(res.round(4).to_string(index=False))

print("\nVerdict:", meta["verdict"], "| P1-P3:", meta["predictions_P1_P3"])
print("Reliability (Spearman-Brown, pooled):",
      {k: round(meta["reliability_pooled_SB"][k], 3) for k in ("NOVCHURN_raw", "NOVCHURN_exc", "OPEN_home", "OPEN_home_clean")
       if k in meta["reliability_pooled_SB"]}, "| outcome:", round(meta["outcome_reliability_SB"], 3))

fig, axes = plt.subplots(1, 3, figsize=(18, 5.2))

# (1) out-of-DEV spearman, demo vs full
ax = axes[0]
piv_d = res.pivot(index="model", columns="body", values="demo_spearman").loc[list(PRED_X)]
piv_f = res.pivot(index="model", columns="body", values="full_spearman").loc[list(PRED_X)]
xx = np.arange(len(PRED_X))
for j, body in enumerate(("OLDHO", "COH1014", "COH1517")):
    ax.plot(xx, piv_f[body], "o-", color=f"C{j}", label=f"{body} full")
    ax.plot(xx, piv_d[body].astype(float), "s--", color=f"C{j}", alpha=0.6, label=f"{body} demo")
ax.set_xticks(xx, [m.replace("B5_plus_", "+") for m in PRED_X], rotation=35, ha="right")
ax.set_ylabel("Spearman(prediction, O2r_m50)")
ax.set_title("Out-of-DEV prediction check (OLS fitted on DEV)")
ax.legend(fontsize=7, ncol=2)

# (2) headline pooled psp with CI for the churn variants
ax = axes[1]
hv = [h for h in V["headline_R2_O2r_m50"] if h["variant"].startswith(("NOVCHURN", "OPEN_home"))]
names = [h["variant"] for h in hv]
ps = np.array([h["POOLED"]["psp"] for h in hv], float)
ci = np.array([h["POOLED"]["ci"] for h in hv], float)
yy = np.arange(len(hv))[::-1]
ax.errorbar(ps, yy, xerr=[ps - ci[:, 0], ci[:, 1] - ps], fmt="o", color="k", ecolor="grey", capsize=3)
ax.axvline(0, color="r", lw=0.8)
ax.set_yticks(yy, names)
ax.set_xlabel("pooled partial Spearman with O2r_m50 | B5+R2 (full run)")
ax.set_title("Raw vs noise-controlled churn (verdict: %s)" % vd["verdict"])

# (3) predicted vs observed on the demo subset
ax = axes[2]
for nm, mk in (("B5", "o"), ("B5_plus_NOVCHURN_raw", "x")):
    ax.scatter(preds[nm], y, marker=mk, alpha=0.6, label=nm)
ax.set_xlabel("OLS prediction (DEV fit)")
ax.set_ylabel("observed O2r_m50")
ax.set_title(f"Demo subset: n={len(T)} concepts")
ax.legend()
plt.tight_layout()
plt.show()
""")

nb = {"cells": cells,
      "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i:02d}"
OUT.write_text(json.dumps(nb, indent=1))
print(OUT)
```

### [26] TOOL RESULT — Write · 2026-09-29 21:37:37 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/scripts/build_notebook.py", "content": "\"\"\"Writes code_demo.ipynb (plain nbformat-4 JSON; no nbformat dependency needed).\"\"\"\nimport json\nfrom pathlib import Path\n\nOUT = Path(__file__).resolve().parents[1] / \"code_demo.ipynb\"\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [],\n                  \"source\": s.strip(\"\\n\")})\n\n\nmd(r\"\"\"\n# Is research-topic churn real or small-sample noise?\n\n**A thin-sample confound check of the home-only churn/novelty signal, demonstrated on 100 concepts.**\n\nThe research artifact asks whether a concept's *neighbourhood churn* — how quickly its co-occurring topics\nturn over in the early years — really predicts later spread, or whether it is an artefact of thin samples\n(about 10 home papers a year). The full pipeline (stages `s0`–`s8`, run by `method.py --run-all`) computed, for\n13,444 selection concepts in four bodies (DEV, OLDHO, COH1014, COH1517):\n\n* **raw** ego-network indicators (`NOV_res`, `edge_persistence`, `ego_density_W3`, …) and the composites\n  `NOVCHURN_raw` / `OPEN_home`;\n* **noise-controlled variants**: V1 fixed-n rarefaction (`*_rare5`, `*_rare10`), V2 within-concept year-permutation\n  null excess (`*_exc`) and Chao Jaccard (`EP_chao`), V3 configuration nulls (`z_dens_cfg`, `z_pers_cfg`, …), and the\n  cleaned composites `NOVCHURN_*`, `OPEN_home_clean` / `OPEN_home_exc`;\n* partial Spearman correlations with the outcome `O2r_m50`, reliability, size dependence and a power simulation.\n\n**This notebook shows `method.py`, the orchestrator's final step (`build_outputs`).** That step:\n1. standardises the five baseline covariates **B5** with the frozen EXP10 constants,\n2. fits OLS models (B5 alone, and B5 plus each churn variant) on **DEV only**,\n3. applies them to the held-out bodies and reports the out-of-DEV Spearman correlation with `O2r_m50`\n   (the gain over B5 alone should be about 0),\n4. writes one example per concept in `exp_gen_sol_out` format together with the headline verdict metadata.\n\nThe per-concept table and the full-run result summaries come from `mini_demo_data.json`: 25 concepts per body,\nspread evenly over the outcome range. With 100 concepts instead of 7,748 the correlations are noisy. The\nfull-run values are shown next to them for comparison.\n\"\"\")\n\ncode(r\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — NOT pre-installed on Colab, always install\n_pip('loguru==0.7.3')\n\n# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (Colab's exact versions)\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(r\"\"\"\n## Imports\n\nThis is the original import block of `method.py`. The artifact's `lib/common.py` helpers (`jdump` and the path\nconstants) are not shipped with the demo, so the two small helpers `build_outputs` uses (`_clean`, `jdump`) are\ncopied verbatim below. `RES` and `ROOT` point at a local output folder. `matplotlib` is added for the final plots.\n\"\"\")\n\ncode(r\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport math\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy import stats\n\nimport matplotlib.pyplot as plt\n\n\n# --- copied verbatim from the artifact's lib/common.py (only what build_outputs needs) ---\ndef _clean(o):\n    if isinstance(o, dict):\n        return {str(k): _clean(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [_clean(v) for v in o]\n    if isinstance(o, np.ndarray):\n        return _clean(o.tolist())\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, (np.bool_,)):\n        return bool(o)\n    if isinstance(o, (np.floating, float)):\n        return None if not math.isfinite(float(o)) else float(o)\n    return o\n\n\ndef jdump(obj, path: Path) -> None:\n    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))\n\"\"\")\n\nmd(r\"\"\"\n## Load the demo data\n\nThe data loads from the GitHub URL, with a local fallback so the same code runs in Colab and on a local\nmachine.\n\"\"\")\n\ncode(r\"\"\"\nGITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n\"\"\")\n\ncode(r\"\"\"\ndata = load_data()\nprint(\"examples:\", len(data[\"datasets\"][0][\"examples\"]))\nprint(\"full-run pooled concepts with finite outcome:\", data[\"metadata\"][\"n_full_pooled_finite_outcome\"])\n\"\"\")\n\nmd(r\"\"\"\n## Configuration\n\n* `N_PER_BODY` sets how many of the 25 demo concepts per body to use. The original run used every concept with a\n  finite `O2r_m50`: 7,748 in total.\n* `MIN_N_SPEARMAN` is the original rule in `build_outputs`: a body's Spearman correlation is reported only when\n  it has more than this many concepts. It is set to 20, as in `method.py`. Because of this rule,\n  `N_PER_BODY` must be at least 21 for any out-of-DEV correlation to appear.\n* `OUT_DIR` is where `prediction_check.json` and `method_out.json` are written. The original wrote them to\n  `results/` and to the repository root.\n\"\"\")\n\ncode(r\"\"\"\nN_PER_BODY = 25          # max 25 in mini_demo_data.json (original: all concepts, 7,748 pooled)\nMIN_N_SPEARMAN = 20      # original: `if ok.sum() > 20`\nOUT_DIR = Path(\"demo_outputs\")\n\nOUT_DIR.mkdir(exist_ok=True)\nROOT = OUT_DIR           # method.py writes method_out.json to ROOT\nRES = OUT_DIR            # ... and prediction_check.json to RES\n\"\"\")\n\nmd(r\"\"\"\n## Constants from `method.py`\n\n* **B5** lists the five baseline covariates: log volume, growth, off-home share, entropy and reach.\n* **PRED_X** maps each prediction model to the churn variant it adds to B5.\n* **INPUT_COLS** lists the per-concept indicators copied into each output example. Suffixes: `__raw` is the raw\n  indicator, `_rare5`/`_rare10` is V1 fixed-n rarefaction, `_exc` is V2 excess over the year-permutation null,\n  `_nullmean` is the V2 null mean, `EP_chao` is the V2b Chao Jaccard, and `z_*_cfg`/`z_dens_k` are the V3\n  configuration-null z-scores.\n\nThe original file also defines `STAGES`, `run_stages()`, `concept_key_check()` and `exp12_crosscheck()`. Those\nre-run the upstream pipeline scripts or read about 250 MB of parquet files and other artifacts' outputs, so the\ndemo leaves them out. Their results are marked as unavailable in the metadata below.\n\"\"\")\n\ncode(r\"\"\"\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nPRED_X = {\"B5\": None, \"B5_plus_NOVCHURN_raw\": \"NOVCHURN_raw\", \"B5_plus_NOVCHURN_exc\": \"NOVCHURN_exc\",\n          \"B5_plus_NOVCHURN_cfg\": \"NOVCHURN_cfg\", \"B5_plus_OPEN_home\": \"OPEN_home\",\n          \"B5_plus_OPEN_home_clean\": \"OPEN_home_clean\"}\nINPUT_COLS = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"new_edge_rate__raw\", \"n_comm_W3__raw\",\n              \"participation__raw\", \"NOVCHURN_raw\", \"OPEN_home\", \"NOV_res_rare10\", \"edge_persistence_rare10\",\n              \"NOVCHURN_rare10\", \"NOV_res_rare5\", \"edge_persistence_rare5\", \"NOVCHURN_rare5\", \"NOV_res_exc\",\n              \"edge_persistence_exc\", \"edge_persistence_nullmean\", \"NOVCHURN_exc\", \"EP_chao\", \"NOVCHURN_chao\",\n              \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\", \"excess_pers_cfg\", \"NOVCHURN_cfg\", \"OPEN_home_clean\",\n              \"OPEN_home_exc\"]\n\"\"\")\n\nmd(r\"\"\"\n## `build_outputs()`, part 1: inputs\n\nIn the original, `spec`, `V`, `rel`, `pw` and `sz` are read from `results/*.json`, and `T` comes from\n`tables.load_tables()[\"POOLED\"]`, which joins `clean_variants.parquet` with the EXP10 covariates and outcomes.\nHere they come from `data`. Missing values arrive as JSON `null` and become `NaN` again, so the `np.isfinite`\nlogic works as in the original. The last line, which keeps only concepts with a finite outcome, is unchanged.\n\"\"\")\n\ncode(r\"\"\"\nmeta_in = data[\"metadata\"]\nspec = meta_in[\"frozen_spec\"]                  # was: json.loads((RES / \"frozen_spec.json\").read_text())\npm = spec[\"exp10_prediction_models\"][\"B5\"]\nV = meta_in[\"clean_vs_raw_psp\"]                # was: results/clean_vs_raw_psp.json\nrel = meta_in[\"reliability\"]                   # was: results/reliability.json\npw = meta_in[\"power_frame_n\"]                  # was: results/power_frame_n.json\nsz = meta_in[\"size_dependence\"]                # was: results/size_dependence.json\n\n# was: T = load_tables()[\"POOLED\"]\nT = pd.DataFrame(data[\"datasets\"][0][\"examples\"])\nT = T.groupby(\"body\", sort=False).head(N_PER_BODY).reset_index(drop=True)   # demo: subsample per body\nfor c in T.columns:\n    if c not in (\"name\", \"body\", \"agroup\"):\n        T[c] = pd.to_numeric(T[c], errors=\"coerce\").astype(float)           # JSON null -> NaN\nT = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)\nprint(T.body.value_counts().to_dict())\nprint(\"frozen B5 mu:\", pm[\"mu\"])\nT.head()\n\"\"\")\n\nmd(r\"\"\"\n## Part 2: fit OLS on DEV and predict every body\n\nThe B5 covariates are standardised with the frozen EXP10 `mu`/`sd`, **not** refitted on this sample. For each\nmodel that adds a churn variant, NaN values are imputed with the DEV median and flagged. The OLS coefficients\ncome from the DEV rows only and are then applied to every concept. This code is unchanged.\n\"\"\")\n\ncode(r\"\"\"\nZb = np.column_stack([(T[c].to_numpy(float) - pm[\"mu\"][c]) / pm[\"sd\"][c] for c in B5])\ndev = (T.body == \"DEV\").to_numpy() & np.all(np.isfinite(Zb), 1)\ny = T.O2r_m50.to_numpy(float)\npreds, imputed, coefs = {}, {}, {}\nfor nm, x in PRED_X.items():\n    X = Zb.copy()\n    if x is not None:\n        v = T[x].to_numpy(float)\n        med = float(np.nanmedian(v[dev]))\n        imputed[nm] = ~np.isfinite(v)\n        v = np.where(np.isfinite(v), v, med)\n        X = np.c_[X, v]\n    A = np.c_[np.ones(len(T)), X]\n    okf = dev & np.all(np.isfinite(A), 1)\n    b = np.linalg.lstsq(A[okf], y[okf], rcond=None)[0]\n    coefs[nm] = b.tolist()\n    preds[nm] = A @ b\nfor nm in coefs:\n    print(f\"{nm:26s} n_DEV_fit={int(dev.sum()):3d}  coef={np.round(coefs[nm], 3).tolist()}\")\n\"\"\")\n\nmd(r\"\"\"\n## Part 3: out-of-DEV check\n\nFor each held-out body, this computes the Spearman correlation between each model's prediction and the observed\n`O2r_m50`, and the gain over B5 alone. In the full run every gain was about 0 (below +0.005). The churn variants\nadd almost nothing to *out-of-sample prediction* beyond B5, although their partial correlations are non-zero.\nThe code is unchanged except that `20` is now the config variable `MIN_N_SPEARMAN`.\n\"\"\")\n\ncode(r\"\"\"\nchk = {\"note\": \"OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)\", \"coef\": coefs}\nfor body in (\"OLDHO\", \"COH1014\", \"COH1517\"):\n    m = (T.body == body).to_numpy()\n    ent = {}\n    for nm, p in preds.items():\n        ok = m & np.isfinite(p)\n        ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > MIN_N_SPEARMAN else None\n    ent[\"n\"] = int(m.sum())\n    ent[\"gain_vs_B5\"] = {nm: (ent[nm] - ent[\"B5\"]) if ent[nm] is not None and ent[\"B5\"] is not None else None\n                         for nm in PRED_X if nm != \"B5\"}\n    chk[body] = ent\njdump(chk, RES / \"prediction_check.json\")\nprint(json.dumps({b: {k: v for k, v in chk[b].items() if k != \"gain_vs_B5\"} for b in (\"OLDHO\", \"COH1014\", \"COH1517\")},\n                 indent=1))\n\"\"\")\n\nmd(r\"\"\"\n## Part 4: one output example per concept (`exp_gen_sol_out` format)\n\nEach example stores the concept's raw and cleaned indicators as the JSON `input` and `O2r_m50` as the `output`.\nIt also holds one `predict_<model>` field per OLS model and metadata flags that show which variants were imputed\nor missing. This code is unchanged.\n\"\"\")\n\ncode(r\"\"\"\nexs = []\nfor i, r in T.iterrows():\n    inp = {\"concept_id\": str(r.concept_id), \"name\": str(r[\"name\"]), \"body\": r.body, \"t0\": int(r.t0),\n           \"n_home_early\": int(r.n_home_early)}\n    for c in INPUT_COLS:\n        v = r[c]\n        inp[c] = None if not np.isfinite(v) else round(float(v), 6)\n    e = {\"input\": json.dumps(inp), \"output\": f\"{r.O2r_m50:.6f}\"}\n    for nm, p in preds.items():\n        e[f\"predict_{nm}\"] = f\"{p[i]:.6f}\" if np.isfinite(p[i]) else \"nan\"\n    e[\"metadata_body\"] = r.body\n    e[\"metadata_agroup\"] = r.agroup\n    e[\"metadata_O2r_resid\"] = None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)\n    e[\"metadata_imputed_variants\"] = [nm for nm in imputed if imputed[nm][i]]\n    e[\"metadata_missing_clean_variants\"] = [c for c in (\"NOVCHURN_exc\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\",\n                                                        \"OPEN_home_clean\") if not np.isfinite(r[c])]\n    exs.append(e)\nprint(len(exs), \"examples; first one:\")\nprint(json.dumps(exs[0], indent=1)[:1500])\n\"\"\")\n\nmd(r\"\"\"\n## Part 5: verdict metadata and `method_out.json`\n\nThis part assembles the headline metadata from the full-run summaries:\n* the mechanical verdict (`PARTLY_THIN`);\n* whether predictions P1–P3 hold;\n* the headline partial Spearman (psp, controlling for B5 and R2) of each variant with `O2r_m50`;\n* the Spearman–Brown reliabilities;\n* the thin-sample share of raw persistence;\n* the plain-language power statement.\n\n`concept_key_check()` and `exp12_crosscheck()` are replaced by an \"unavailable in demo\" note, because they read\nexternal artifacts. The rest is unchanged.\n\"\"\")\n\ncode(r\"\"\"\nvd = V[\"verdict\"]\nhead = {h[\"variant\"]: {b: h[b].get(\"psp\") for b in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\")}\n        for h in V[\"headline_R2_O2r_m50\"]}\n_NA = {\"available\": False, \"note\": \"needs external artifacts; not run in the demo\"}\nmeta = {\"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled \"\n                       \"variants)\",\n        \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n        \"verdict\": vd[\"verdict\"], \"DEGREE_ARTEFACT_PERSISTENCE\": vd[\"DEGREE_ARTEFACT_PERSISTENCE\"],\n        \"predictions_P1_P3\": {k: v[\"holds\"] for k, v in V[\"predictions\"].items()},\n        \"P_detail\": V[\"predictions\"], \"headline_psp_R2_O2r_m50\": head,\n        \"reliability_pooled_SB\": {k: v[\"pooled\"][\"SB\"] for k, v in rel[\"variants\"].items()},\n        \"outcome_reliability_SB\": rel[\"outcome\"][\"O2r_m50\"][\"pooled\"][\"SB\"],\n        \"thin_sample_share_R2\": sz[\"thin_sample_share\"][\"POOLED\"][\"R2\"],\n        \"power_plain_language\": pw[\"plain_language\"],\n        \"concept_key_check\": _NA, \"exp12_home_crosscheck\": _NA,   # was: concept_key_check(), exp12_crosscheck()\n        \"n_examples\": len(exs), \"prediction_models\": \"OLS on DEV (B5 standardised with EXP10 frozen mu/sd); \"\n                                                     \"NaN variants imputed with the DEV median (flagged)\"}\nout = {\"metadata\": meta, \"datasets\": [{\"dataset\": \"selection_concepts\", \"examples\": exs}]}\n(ROOT / \"method_out.json\").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)\n                                                 and not math.isfinite(o) else str(o)))\nlogger.info(f\"method_out.json: {len(exs)} examples; verdict {vd['verdict']}\")\nprint(\"P1-P3 hold:\", meta[\"predictions_P1_P3\"])\nprint(\"thin-sample share of raw persistence (R2):\", round(meta[\"thin_sample_share_R2\"], 3))\nprint(\"power:\", meta[\"power_plain_language\"])\n\"\"\")\n\nmd(r\"\"\"\n## Results and visualisation\n\n1. **Out-of-DEV Spearman**: each model's value on the demo subset next to the full run. The absolute values\n   differ because of the small sample, but in both the churn variants barely change the B5 baseline.\n2. **Headline partial Spearman** (full run, pooled, 95% bootstrap CI) of the raw and noise-controlled churn\n   variants. The V2 excess variants (`*_exc`, `*_zperm`) collapse to about 0. Rarefaction keeps part of the\n   signal, and Chao and configuration-null composites keep most of it. This is the `PARTLY_THIN` verdict.\n3. **Predicted vs observed** `O2r_m50` on the demo concepts for B5 alone and for B5 + `NOVCHURN_raw`.\n\"\"\")\n\ncode(r\"\"\"\nfull_pc = meta_in[\"full_run_prediction_check\"]\nrows = []\nfor body in (\"OLDHO\", \"COH1014\", \"COH1517\"):\n    for nm in PRED_X:\n        rows.append({\"body\": body, \"model\": nm, \"demo_spearman\": chk[body][nm],\n                     \"full_spearman\": full_pc[body][nm], \"demo_n\": chk[body][\"n\"], \"full_n\": full_pc[body][\"n\"]})\nres = pd.DataFrame(rows)\npd.set_option(\"display.width\", 160)\nprint(\"Out-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run\")\nprint(res.round(4).to_string(index=False))\n\nprint(\"\\nVerdict:\", meta[\"verdict\"], \"| P1-P3:\", meta[\"predictions_P1_P3\"])\nprint(\"Reliability (Spearman-Brown, pooled):\",\n      {k: round(meta[\"reliability_pooled_SB\"][k], 3) for k in (\"NOVCHURN_raw\", \"NOVCHURN_exc\", \"OPEN_home\", \"OPEN_home_clean\")\n       if k in meta[\"reliability_pooled_SB\"]}, \"| outcome:\", round(meta[\"outcome_reliability_SB\"], 3))\n\nfig, axes = plt.subplots(1, 3, figsize=(18, 5.2))\n\n# (1) out-of-DEV spearman, demo vs full\nax = axes[0]\npiv_d = res.pivot(index=\"model\", columns=\"body\", values=\"demo_spearman\").loc[list(PRED_X)]\npiv_f = res.pivot(index=\"model\", columns=\"body\", values=\"full_spearman\").loc[list(PRED_X)]\nxx = np.arange(len(PRED_X))\nfor j, body in enumerate((\"OLDHO\", \"COH1014\", \"COH1517\")):\n    ax.plot(xx, piv_f[body], \"o-\", color=f\"C{j}\", label=f\"{body} full\")\n    ax.plot(xx, piv_d[body].astype(float), \"s--\", color=f\"C{j}\", alpha=0.6, label=f\"{body} demo\")\nax.set_xticks(xx, [m.replace(\"B5_plus_\", \"+\") for m in PRED_X], rotation=35, ha=\"right\")\nax.set_ylabel(\"Spearman(prediction, O2r_m50)\")\nax.set_title(\"Out-of-DEV prediction check (OLS fitted on DEV)\")\nax.legend(fontsize=7, ncol=2)\n\n# (2) headline pooled psp with CI for the churn variants\nax = axes[1]\nhv = [h for h in V[\"headline_R2_O2r_m50\"] if h[\"variant\"].startswith((\"NOVCHURN\", \"OPEN_home\"))]\nnames = [h[\"variant\"] for h in hv]\nps = np.array([h[\"POOLED\"][\"psp\"] for h in hv], float)\nci = np.array([h[\"POOLED\"][\"ci\"] for h in hv], float)\nyy = np.arange(len(hv))[::-1]\nax.errorbar(ps, yy, xerr=[ps - ci[:, 0], ci[:, 1] - ps], fmt=\"o\", color=\"k\", ecolor=\"grey\", capsize=3)\nax.axvline(0, color=\"r\", lw=0.8)\nax.set_yticks(yy, names)\nax.set_xlabel(\"pooled partial Spearman with O2r_m50 | B5+R2 (full run)\")\nax.set_title(\"Raw vs noise-controlled churn (verdict: %s)\" % vd[\"verdict\"])\n\n# (3) predicted vs observed on the demo subset\nax = axes[2]\nfor nm, mk in ((\"B5\", \"o\"), (\"B5_plus_NOVCHURN_raw\", \"x\")):\n    ax.scatter(preds[nm], y, marker=mk, alpha=0.6, label=nm)\nax.set_xlabel(\"OLS prediction (DEV fit)\")\nax.set_ylabel(\"observed O2r_m50\")\nax.set_title(f\"Demo subset: n={len(T)} concepts\")\nax.legend()\nplt.tight_layout()\nplt.show()\n\"\"\")\n\nnb = {\"cells\": cells,\n      \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                   \"language_info\": {\"name\": \"python\", \"version\": \"3.12\"}},\n      \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"cell-{i:02d}\"\nOUT.write_text(json.dumps(nb, indent=1))\nprint(OUT)\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [27] TOOL CALL — Bash · 2026-09-29 21:37:43 UTC

```
python3 scripts/build_notebook.py && sed -i 's/N_PER_BODY = 25 /N_PER_BODY = 21 /' code_demo.ipynb && grep -c "N_PER_BODY = 21" code_demo.ipynb && E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [28] TOOL RESULT — Bash · 2026-09-29 21:38:09 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb\n1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 246968 bytes to code_demo.ipynb\n\nreal\t0m21.473s\nuser\t0m16.213s\nsys\t0m1.277s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-29 21:38:13 UTC

```
The minimal config (21 per body) passes in 21 s. Next I'll check the outputs, then scale up to all 25 per body.
```

### [30] TOOL CALL — Bash · 2026-09-29 21:38:13 UTC

```
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o['output_type']=='stream': print(o['text'][-1200:] if isinstance(o['text'],str) else ''.join(o['text'])[-1200:])
      elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
      else: print('[',o['output_type'],list(o.get('data',{}).keys()),']')
"
```

### [31] TOOL RESULT — Bash · 2026-09-29 21:38:13 UTC

```
{"stdout": "examples: 100\nfull-run pooled concepts with finite outcome: 7748\n\n{'DEV': 21, 'OLDHO': 21, 'COH1014': 21, 'COH1517': 21}\nfrozen B5 mu: {'logvol': 4.387217461299273, 'growth_c': 0.13591487868338373, 'offhome_share': 0.2628714872549475, 'entropy': 0.7831561038968538, 'reach': 3.228179741051028}\n\n[ execute_result ['text/html', 'text/plain'] ]\nB5                         n_DEV_fit= 21  coef=[4.742, -0.521, 0.587, -1.655, 3.157, -0.567]\nB5_plus_NOVCHURN_raw       n_DEV_fit= 21  coef=[4.616, -0.396, 0.438, -1.462, 2.784, -0.458, 0.491]\nB5_plus_NOVCHURN_exc       n_DEV_fit= 21  coef=[4.366, -0.574, 0.487, -0.952, 2.352, -0.36, 0.631]\nB5_plus_NOVCHURN_cfg       n_DEV_fit= 21  coef=[4.546, -0.502, 0.554, -1.491, 2.941, -0.567, 0.437]\nB5_plus_OPEN_home          n_DEV_fit= 21  coef=[4.217, -0.391, 0.09, -0.343, 1.102, 0.116, 0.754]\nB5_plus_OPEN_home_clean    n_DEV_fit= 21  coef=[4.318, -0.526, 0.389, -0.606, 1.754, -0.218, 0.55]\n\n{\n \"OLDHO\": {\n  \"B5\": 0.39610389610389607,\n  \"B5_plus_NOVCHURN_raw\": 0.27662337662337666,\n  \"B5_plus_NOVCHURN_exc\": 0.3038961038961039,\n  \"B5_plus_NOVCHURN_cfg\": 0.23766233766233766,\n  \"B5_plus_OPEN_home\": 0.46753246753246747,\n  \"B5_plus_OPEN_home_clean\": 0.3207792207792208,\n  \"n\": 21\n },\n \"COH1014\": {\n  \"B5\": 0.7948051948051948,\n  \"B5_plus_NOVCHURN_raw\": 0.7129870129870131,\n  \"B5_plus_NOVCHURN_exc\": 0.764935064935065,\n  \"B5_plus_NOVCHURN_cfg\": 0.7883116883116883,\n  \"B5_plus_OPEN_home\": 0.6701298701298701,\n  \"B5_plus_OPEN_home_clean\": 0.7701298701298702,\n  \"n\": 21\n },\n \"COH1517\": {\n  \"B5\": 0.47402597402597396,\n  \"B5_plus_NOVCHURN_raw\": 0.5558441558441559,\n  \"B5_plus_NOVCHURN_exc\": 0.5194805194805194,\n  \"B5_plus_NOVCHURN_cfg\": 0.5155844155844156,\n  \"B5_plus_OPEN_home\": 0.4623376623376624,\n  \"B5_plus_OPEN_home_clean\": 0.5844155844155844,\n  \"n\": 21\n }\n}\n\n\"participation__raw\\\": 0.65625, \\\"NOVCHURN_raw\\\": null, \\\"OPEN_home\\\": -0.141717, \\\"NOV_res_rare10\\\": null, \\\"edge_persistence_rare10\\\": 0.105, \\\"NOVCHURN_rare10\\\": null, \\\"NOV_res_rare5\\\": null, \\\"edge_persistence_rare5\\\": 0.035714, \\\"NOVCHURN_rare5\\\": null, \\\"NOV_res_exc\\\": null, \\\"edge_persistence_exc\\\": -0.023699, \\\"edge_persistence_nullmean\\\": 0.490366, \\\"NOVCHURN_exc\\\": null, \\\"EP_chao\\\": 0.589709, \\\"NOVCHURN_chao\\\": null, \\\"z_dens_cfg\\\": 12.917785, \\\"z_dens_k\\\": 7.374662, \\\"z_pers_cfg\\\": null, \\\"excess_pers_cfg\\\": 0.466667, \\\"NOVCHURN_cfg\\\": null, \\\"OPEN_home_clean\\\": 0.546166, \\\"OPEN_home_exc\\\": 0.476757}\",\n \"output\": \"1.000000\",\n \"predict_B5\": \"2.334990\",\n \"predict_B5_plus_NOVCHURN_raw\": \"2.568288\",\n \"predict_B5_plus_NOVCHURN_exc\": \"2.149292\",\n \"predict_B5_plus_NOVCHURN_cfg\": \"2.425930\",\n \"predict_B5_plus_OPEN_home\": \"2.431283\",\n \"predict_B5_plus_OPEN_home_clean\": \"2.608107\",\n \"metadata_body\": \"DEV\",\n \"metadata_agroup\": \"BGM+Med\",\n \"metadata_O2r_resid\": -3.555508,\n \"metadata_imputed_variants\": [\n  \"B5_plus_NOVCHURN_raw\",\n  \"B5_plus_NOVCHURN_exc\",\n  \"B5_plus_NOVCHURN_cfg\"\n ],\n \"metadata_missing_clean_variants\": [\n  \"NOVCHURN_exc\",\n  \"NOVCHURN_rare10\",\n  \"NOVCHURN_cfg\"\n ]\n}\n\n\u001b[32m2026-09-29 21:38:06.546\u001b[0m | \u001b[1mINFO    \u001b[0m | \u001b[36m__main__\u001b[0m:\u001b[36m<module>\u001b[0m:\u001b[36m21\u001b[0m - \u001b[1mmethod_out.json: 84 examples; verdict PARTLY_THIN\u001b[0m\n\nP1-P3 hold: {'P1': False, 'P2': True, 'P3': True}\nthin-sample share of raw persistence (R2): 0.66\npower: At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.\n\n         0.3208         0.7070      21    1797\nCOH1014                      B5         0.7948         0.7589      21    2154\nCOH1014    B5_plus_NOVCHURN_raw         0.7130         0.7621      21    2154\nCOH1014    B5_plus_NOVCHURN_exc         0.7649         0.7588      21    2154\nCOH1014    B5_plus_NOVCHURN_cfg         0.7883         0.7608      21    2154\nCOH1014       B5_plus_OPEN_home         0.6701         0.7610      21    2154\nCOH1014 B5_plus_OPEN_home_clean         0.7701         0.7622      21    2154\nCOH1517                      B5         0.4740         0.7851      21     628\nCOH1517    B5_plus_NOVCHURN_raw         0.5558         0.7889      21     628\nCOH1517    B5_plus_NOVCHURN_exc         0.5195         0.7850      21     628\nCOH1517    B5_plus_NOVCHURN_cfg         0.5156         0.7861      21     628\nCOH1517       B5_plus_OPEN_home         0.4623         0.7875      21     628\nCOH1517 B5_plus_OPEN_home_clean         0.5844         0.7889      21     628\n\nVerdict: PARTLY_THIN | P1-P3: {'P1': False, 'P2': True, 'P3': True}\nReliability (Spearman-Brown, pooled): {'NOVCHURN_raw': 0.476, 'NOVCHURN_exc': 0.014, 'OPEN_home': 0.485, 'OPEN_home_clean': 0.577} | outcome: 0.895\n\n[ display_data ['image/png', 'text/plain'] ]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-29 21:38:25 UTC

```
python3 - <<'EOF'
p='scripts/build_notebook.py'; s=open(p).read()
old='T = T.groupby("body", sort=False).head(N_PER_BODY).reset_index(drop=True)   # demo: subsample per body'
new='''# demo: keep N_PER_BODY concepts per body, spread evenly over the (outcome-sorted) demo rows
T = pd.concat([g.iloc[np.unique(np.linspace(0, len(g) - 1, min(N_PER_BODY, len(g))).round().astype(int))]
               for _, g in T.groupby("body", sort=False)], ignore_index=True)'''
assert old in s; open(p,'w').write(s.replace(old,new))
EOF
python3 scripts/build_notebook.py && E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-bc4a8c6a968e && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3 && python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
      if 'image/png' in o.get('data',{}): open('/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/88654581-f25c-4cd4-b8a1-a9905062316c/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
      if o['output_type']=='stream' and 'Out-of-DEV' in ''.join(o['text']): print(''.join(o['text'])[:2500])
"
```

### [33] TOOL RESULT — Bash · 2026-09-29 21:38:47 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 240853 bytes to code_demo.ipynb\n\nreal\t0m20.478s\nuser\t0m16.467s\nsys\t0m1.283s\nOut-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run\n   body                   model  demo_spearman  full_spearman  demo_n  full_n\n  OLDHO                      B5         0.5154         0.7051      25    1797\n  OLDHO    B5_plus_NOVCHURN_raw         0.5208         0.7101      25    1797\n  OLDHO    B5_plus_NOVCHURN_exc         0.5008         0.7051      25    1797\n  OLDHO    B5_plus_NOVCHURN_cfg         0.5208         0.7068      25    1797\n  OLDHO       B5_plus_OPEN_home         0.5115         0.7068      25    1797\n  OLDHO B5_plus_OPEN_home_clean         0.5269         0.7070      25    1797\nCOH1014                      B5         0.7315         0.7589      25    2154\nCOH1014    B5_plus_NOVCHURN_raw         0.7262         0.7621      25    2154\nCOH1014    B5_plus_NOVCHURN_exc         0.7277         0.7588      25    2154\nCOH1014    B5_plus_NOVCHURN_cfg         0.7354         0.7608      25    2154\nCOH1014       B5_plus_OPEN_home         0.7569         0.7610      25    2154\nCOH1014 B5_plus_OPEN_home_clean         0.7438         0.7622      25    2154\nCOH1517                      B5         0.4169         0.7851      25     628\nCOH1517    B5_plus_NOVCHURN_raw         0.4123         0.7889      25     628\nCOH1517    B5_plus_NOVCHURN_exc         0.4154         0.7850      25     628\nCOH1517    B5_plus_NOVCHURN_cfg         0.4000         0.7861      25     628\nCOH1517       B5_plus_OPEN_home         0.3638         0.7875      25     628\nCOH1517 B5_plus_OPEN_home_clean         0.4115         0.7889      25     628\n\nVerdict: PARTLY_THIN | P1-P3: {'P1': False, 'P2': True, 'P3': True}\nReliability (Spearman-Brown, pooled): {'NOVCHURN_raw': 0.476, 'NOVCHURN_exc': 0.014, 'OPEN_home': 0.485, 'OPEN_home_clean': 0.577} | outcome: 0.895", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Read · 2026-09-29 21:38:49 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/88654581-f25c-4cd4-b8a1-a9905062316c/scratchpad/fig.png
```

### [35] TOOL RESULT — Read · 2026-09-29 21:38:49 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [36] ASSISTANT · 2026-09-29 21:38:57 UTC

```
Scaling is done: 25 per body is all the demo data holds, and the run takes about 20 s. Next I'll verify the files and write the manifest, README and struct output.
```

### [37] TOOL CALL — Bash · 2026-09-29 21:38:57 UTC

```
grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urlopen(GITHUB_DATA_URL)" code_demo.ipynb; du -ah --max-depth=2 . | sort -h | tail -12; ls -la .aii
```

### [38] TOOL RESULT — Bash · 2026-09-29 21:38:57 UTC

```
{"stdout": "1\n1\n512\t./.aii\n512\t./.aii_claude_session.json\n3.0K\t./demo_outputs/prediction_check.json\n4.0K\t./scripts/make_mini_data.py\n20K\t./scripts/build_notebook.py\n155K\t./demo_outputs/method_out.json\n168K\t./mini_demo_data.json\n215K\t./.repl_agent.ptylog\n236K\t./code_demo.ipynb\n1003K\t./scripts\n1.2M\t./demo_outputs\n3.8M\t.\ntotal 1055\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:34 .\ndrwxrwxrwx 5 aii-agent aii-agent 1079764 Sep 29 21:38 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] TOOL CALL — Bash · 2026-09-29 21:39:13 UTC

```
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is a large binary or a cache directory: every file is small text/JSON/notebook
# (the whole workspace is ~4 MB), so no keep/delete decisions are required.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: is research-topic churn real or small-sample noise? (experiment 16)

A Colab-ready notebook that demonstrates the final step (`build_outputs`) of the experiment-16 orchestrator
`method.py`. That experiment ran a thin-sample confound check of the home-only churn/novelty signal on 13,444
selection concepts. The notebook keeps the original code. It splits the code into cells and adds explanations
between them.

The notebook does four things:

1. It standardises the five baseline covariates (B5) with the frozen EXP10 constants.
2. It fits OLS models on the DEV body only: B5 alone, and B5 plus each churn variant (`NOVCHURN_raw`, `_exc`,
   `_cfg`, `OPEN_home`, `OPEN_home_clean`).
3. It reports the out-of-DEV Spearman correlation between the predictions and the outcome `O2r_m50` for the OLDHO,
   COH1014 and COH1517 bodies, and compares it with the full-run values.
4. It writes `method_out.json` in `exp_gen_sol_out` format with the headline verdict metadata (`PARTLY_THIN`,
   P1–P3, reliabilities, thin-sample share, power statement), then plots the results.

The run takes about 20 s.

## Layout

| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook. It loads `mini_demo_data.json` from GitHub and falls back to the local copy. |
| `mini_demo_data.json` | 100 concepts (25 per body: DEV, OLDHO, COH1014, COH1517), spread evenly over the `O2r_m50` range. Each has its B5 covariates, raw and noise-controlled indicators and outcome. The file also holds the small full-run summaries that `build_outputs` reads (frozen B5 mu/sd, headline psp with CIs, P1–P3, reliability, size dependence, power, full-run prediction check). |
| `scripts/make_mini_data.py` | Builds `mini_demo_data.json` from the experiment-16 artifact's `data/` and `results/`. |
| `scripts/build_notebook.py` | Writes `code_demo.ipynb`. |
| `demo_outputs/` | Written when the notebook runs: `prediction_check.json` and `method_out.json` for the demo subset. |

## How to run

- **Colab:** open `code_demo.ipynb` and choose *Run all*. The first cell installs `loguru` and nothing else.
- **Locally:** use Python 3.12 and run
  `pip install jupyter ipykernel && jupyter nbconvert --to notebook --execute code_demo.ipynb`.
  Outside Colab, the install cell pins numpy 2.0.2, pandas 2.2.2, scipy 1.16.3 and matplotlib 3.10.0 to Colab's
  versions.

Tunable settings are in the notebook's config cell:

- `N_PER_BODY`: at most 25. The original used all 7,748 concepts with a finite outcome.
- `MIN_N_SPEARMAN = 20`: the original rule.

Parts of `method.py` are left out because they need about 250 MB of upstream parquet files and other artifacts:
`run_stages()`, which re-runs the `s0`–`s8` pipeline scripts, `concept_key_check()` and `exp12_crosscheck()`. The
notebook marks their results as unavailable.

## Restoring removed files

Nothing is marked `delete` in `.aii/manifest.yaml`, so nothing needs restoring. Running the notebook regenerates
`demo_outputs/`. To rebuild the data and the notebook from the experiment-16 artifact, run
`python scripts/make_mini_data.py && python scripts/build_notebook.py` (needs pandas and pyarrow).
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json
```

### [40] TOOL RESULT — Bash · 2026-09-29 21:39:13 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] ASSISTANT · 2026-09-29 21:39:19 UTC

```
The published-files rule says no absolute server paths, so I'll make the artifact path in `make_mini_data.py` an environment variable.
```

### [42] TOOL CALL — Bash · 2026-09-29 21:39:19 UTC

```
python3 - <<'EOF'
p='scripts/make_mini_data.py'; s=open(p).read()
s=s.replace('import json, math, sys','import json, math, os, sys')
s=s.replace('ART = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16")',
 'ART = Path(os.environ["EXP16_DIR"])  # path to the experiment-16 artifact checkout (with data/, results/, lib/)')
open(p,'w').write(s)
p='README.md'; s=open(p).read()
s=s.replace('`python scripts/make_mini_data.py && python scripts/build_notebook.py`','`EXP16_DIR=<path to experiment-16 artifact> python scripts/make_mini_data.py && python scripts/build_notebook.py`')
open(p,'w').write(s)
EOF
grep -rn "/ai-inventor" README.md scripts code_demo.ipynb mini_demo_data.json | head; EXP16_DIR=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 python3 scripts/make_mini_data.py && git status --short | head
```

### [43] TOOL RESULT — Bash · 2026-09-29 21:39:23 UTC

```
{"stdout": "scripts/build_notebook.py:114:GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json\"\ncode_demo.ipynb:150:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-5/experiment-16/demo/mini_demo_data.json\\\"\\n\",\n/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/mini_demo_data.json 100 171903\nfatal: not a git repository (or any parent up to mount point /ai-inventor)\nStopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] ASSISTANT · 2026-09-29 21:39:33 UTC

```
I've built `code_demo.ipynb` and `mini_demo_data.json`. The notebook ran from start to finish in the clean Colab-like test environment with no errors, in about 20 seconds.

**What the notebook covers.** The file to convert was `method.py`, which is only the orchestrator. The notebook runs its final step, `build_outputs()`, split into cells with explanations in between; the code is otherwise unchanged:
1. It scales the five baseline covariates (B5) with the fixed constants from the earlier experiment.
2. It fits least-squares models on the DEV group only: B5 alone, and B5 plus each churn variant.
3. It checks those predictions against the outcome in the other three groups (OLDHO, COH1014, COH1517).
4. It writes the per-concept results and the summary (verdict `PARTLY_THIN`, P1 fails, P2 and P3 hold).

The last cell prints a table and draws three plots: the demo correlations next to the full-run ones, the pooled churn-variant correlations with their confidence intervals, and predicted vs. observed outcome.

**What I left out.** Three parts of `method.py` can't run from the demo data: re-running the upstream pipeline scripts, and two cross-checks against other experiments' outputs. Together they need about 250 MB of data files and other experiments' results. The notebook explains this and marks those two results as not available. Two small helpers (`jdump`, `_clean`) are copied word for word from the artifact's `lib/common.py`, since that folder isn't shipped with the demo.

**The data.** `mini_demo_data.json` holds 100 concepts, 25 per group, spread evenly across the range of outcome values. It also carries the small full-run summaries the code reads.

**Scale.** The first test used 21 concepts per group, the smallest number for which the original code reports any correlation (it needs more than 20). The final setting is all 25 per group. The original run used 7,748 concepts, and that value is noted in a comment in the config cell. With only 25 concepts per group, the demo correlations are noisier and lower than the full run (for example 0.52 vs. 0.71 in OLDHO for B5 alone). In both, the churn variants add almost nothing over B5 alone.

**Checks.** The notebook contains the exact `GITHUB_DATA_URL` and loads from it first, falling back to the local file.

**Repo files.** `.aii/manifest.yaml` has no entries, because nothing in the workspace is large (about 4 MB in total). `README.md` covers the layout, how to run it, and a "Restoring removed files" section, which says nothing needs restoring. The script that builds the demo data reads the artifact's location from an `EXP16_DIR` environment variable, so no server paths appear in published files. The result JSON is at `./.terminal_claude_agent_struct_out.json`.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `scripts/make_mini_data.py`
- `scripts/build_notebook.py`
```
