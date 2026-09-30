# gen_demo_art_experiment_8 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_8` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-30 01:59:10 UTC

```
model: Claude Opus 5.5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-30 01:59:18 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/`:
GOOD: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/file.py`, `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/results/out.json`
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
id: art_NMe386dX9GLF
type: experiment
title: Do open-neighbourhood concepts spread? Fresh-cohort test
summary: >-
  Single-unseal confirmation of the RQ1 openness claim from EXP8, on a fresh 2015-2017 onset cohort of OpenAlex legacy concepts
  that no earlier screen had touched. One zero-credit S3 pass covered the snapshot of 2026-09-23 (identical to EXP5; checks
  T1-T3 exact). The outcome-blind S3 audit kept TAG grounding: legacy tags still cover 2021-24, with the control ratio at
  a minimum of 0.902. The LLM precision gate passed 94% of candidates, leaving 1,070 concepts with 2015-16 onsets. Pre-seal
  power was 0.16, so the declared 2017 extension applied (n = 1,443; 634 with O2r_m50; 573 with OPEN_home). OPEN is the mean
  of six signed, z-scored ego-network components, with constants frozen on the 12,499 EXP5 concepts; it was built ALL / HOME-ONLY
  / SIZE-MATCHED. The ladder runs R0 = B5 + onset year, then adds contact reach, LLM concept type, pre-onset footprint, coverage
  and group FE. The spec was hash-sealed before the unseal. RESULT: the frozen verdict is CONFIRMED but marginal. OPEN_home
  partial Spearman with O2r_m50 is +0.091 [+0.013, +0.171] at R2 and +0.080 [+0.001, +0.162] at R3. The CIs include 0 at R4/R5,
  the DL pool over groups is +0.083 [-0.007, +0.173], and Holm p = 0.048. It adds no practical prediction (B5 Spearman 0.768
  vs 0.770). Mechanical coupling is large: OPEN_all +0.174, ALL minus HOME +0.093 [+0.016, +0.169], with size-matched in between.
  Home-only signal comes from NOV_res (+0.134) and low edge persistence (-0.112), not from the community count. Type and footprint
  do not absorb OPEN. Replications: CONTACT_REACH (+0.211), n_authors_early on O1c (+0.115), RETENTION_RATIO_early < 0 at
  R0 only; the EXP8 ElasticNet beats B5 by +0.030. The type gate failed twice, so the declared M1 = M2 fallback was used.
  O4 was not run. Independent re-derivations (audit.py, rederive.py) reproduce psp exactly; the shuffled and random-OPEN placebos
  are null. LLM spend $2.04. Deliverables: results/cohort_report.json, cohort_result.json, exp5_selection_result.json, figures/,
  full_method_out.json (predict_B5 vs predict_B5_plus_OPEN_home per concept).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-4/experiment-10/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-4/experiment-10/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-4/experiment-10/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] ASSISTANT · 2026-09-30 01:59:24 UTC

```
I'll start by loading the two required skills and looking at the artifact.
```

### [4] TOOL CALL — Skill · 2026-09-30 01:59:24 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-30 01:59:24 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-30 01:59:24 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-30 01:59:24 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-30 01:59:24 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; ls -la $W; ls -la $W/results $W/figures 2>/dev/null | head -50; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
```

### [9] TOOL RESULT — Bash · 2026-09-30 01:59:26 UTC

```
{"stdout": "total 25280\ndrwxrwxrwx 15 aii-agent aii-agent 2023575 Sep 29 05:04 .\ndrwxrwxrwx  7 aii-agent aii-agent 2078275 Sep 29 02:14 ..\ndrwxrwxrwx  2 aii-agent aii-agent   62500 Sep 29 03:52 .aii\n-rw-rw-rw-  1 aii-agent aii-agent      54 Sep 29 02:15 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent    5923 Sep 29 03:52 .aii_worker_result.json\ndrwxrwxrwx  8 aii-agent aii-agent 2005249 Sep 29 03:46 .git\n-rw-rw-rw-  1 aii-agent aii-agent      72 Sep 29 02:35 .gitignore\n-rw-rw-rw-  1 aii-agent aii-agent 1014045 Sep 29 03:52 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent    2709 Sep 29 03:42 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent   22764 Sep 29 03:46 README.md\n-rw-rw-rw-  1 aii-agent aii-agent    6204 Sep 29 02:40 audit.py\ndrwxrwxrwx  4 aii-agent aii-agent 2005380 Sep 29 03:28 data\ndrwxrwxrwx  2 aii-agent aii-agent 1054146 Sep 29 03:29 figures\n-rw-rw-rw-  1 aii-agent aii-agent 2208500 Sep 29 03:39 full_method_out.json\ndrwxrwxrwx  3 aii-agent aii-agent 2002001 Sep 29 02:16 inputs\ndrwxrwxrwx  2 aii-agent aii-agent 1019408 Sep 29 05:04 lib\ndrwxrwxrwx  2 aii-agent aii-agent 2000386 Sep 29 03:10 llm_cache\ndrwxrwxrwx  2 aii-agent aii-agent 1091170 Sep 29 03:28 logs\n-rw-rw-rw-  1 aii-agent aii-agent   10220 Sep 29 03:33 make_outputs.py\n-rw-rw-rw-  1 aii-agent aii-agent    3893 Sep 29 03:32 make_report.py\n-rwxrwxrwx  1 aii-agent aii-agent    3310 Sep 29 03:42 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 1951651 Sep 29 03:39 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    5145 Sep 29 03:39 mini_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent       1 Sep 29 02:21 models\ndrwxrwxrwx  3 aii-agent aii-agent 2009748 Sep 29 02:23 passC\n-rw-rw-rw-  1 aii-agent aii-agent   15598 Sep 29 02:23 passC.py\n-rw-rw-rw-  1 aii-agent aii-agent    6406 Sep 29 02:26 prereg.md\n-rw-rw-rw-  1 aii-agent aii-agent    5145 Sep 29 03:39 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    2521 Sep 29 03:36 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent    4143 Sep 29 03:34 readme_tables.py\n-rw-rw-rw-  1 aii-agent aii-agent    4536 Sep 29 03:41 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent    8650 Sep 29 03:42 reproducibility.md\n-rw-rw-rw-  1 aii-agent aii-agent    1777 Sep 29 03:36 requirements.lock.txt\n-rwxrwxrwx  1 aii-agent aii-agent     366 Sep 29 03:36 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent 1057843 Sep 29 03:40 results\n-rw-rw-rw-  1 aii-agent aii-agent    2620 Sep 29 02:35 s0_prereg.py\n-rw-rw-rw-  1 aii-agent aii-agent    7305 Sep 29 02:21 s1_candidates.py\n-rw-rw-rw-  1 aii-agent aii-agent    8269 Sep 29 02:36 s3_checks.py\n-rw-rw-rw-  1 aii-agent aii-agent    9669 Sep 29 03:10 s4_gate.py\n-rw-rw-rw-  1 aii-agent aii-agent   16136 Sep 29 03:07 s5_typing.py\n-rw-rw-rw-  1 aii-agent aii-agent    9779 Sep 29 02:45 s6_covariates.py\n-rw-rw-rw-  1 aii-agent aii-agent    8397 Sep 29 02:42 s7_ego.py\n-rw-rw-rw-  1 aii-agent aii-agent   15897 Sep 29 03:11 s8_select.py\n-rw-rw-rw-  1 aii-agent aii-agent   15663 Sep 29 03:21 s9_unseal.py\n-rw-rw-rw-  1 aii-agent aii-agent    6457 Sep 29 02:42 s_learned.py\ndrwxrwxrwx  2 aii-agent aii-agent 1077669 Sep 29 02:20 snapshot\ndrwxrwxrwx  2 aii-agent aii-agent 1001197 Sep 29 03:30 tests\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/figures:\ntotal 3551\ndrwxrwxrwx  2 aii-agent aii-agent 1054146 Sep 29 03:29 .\ndrwxrwxrwx 15 aii-agent aii-agent 2023575 Sep 29 05:04 ..\n-rw-rw-rw-  1 aii-agent aii-agent   17469 Sep 29 03:33 fig_components.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   78772 Sep 29 03:33 fig_components.png\n-rw-rw-rw-  1 aii-agent aii-agent   19362 Sep 29 03:33 fig_coverage_audit.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   71754 Sep 29 03:33 fig_coverage_audit.png\n-rw-rw-rw-  1 aii-agent aii-agent   18071 Sep 29 03:33 fig_forest_groups.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   73826 Sep 29 03:33 fig_forest_groups.png\n-rw-rw-rw-  1 aii-agent aii-agent   23048 Sep 29 03:33 fig_ladder.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  165547 Sep 29 03:33 fig_ladder.png\n-rw-rw-rw-  1 aii-agent aii-agent   18046 Sep 29 03:33 fig_within_type.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   68568 Sep 29 03:33 fig_within_type.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results:\ntotal 3597\ndrwxrwxrwx  2 aii-agent aii-agent 1057843 Sep 29 03:40 .\ndrwxrwxrwx 15 aii-agent aii-agent 2023575 Sep 29 05:04 ..\n-rw-rw-rw-  1 aii-agent aii-agent    2304 Sep 29 03:29 audit.json\n-rw-rw-rw-  1 aii-agent aii-agent   91250 Sep 29 03:37 cohort_report.json\n-rw-rw-rw-  1 aii-agent aii-agent   72704 Sep 29 03:27 cohort_result.json\n-rw-rw-rw-  1 aii-agent aii-agent    2632 Sep 29 03:01 coverage_by_year.csv\n-rw-rw-rw-  1 aii-agent aii-agent    1570 Sep 29 03:21 deviations.json\n-rw-rw-rw-  1 aii-agent aii-agent   59579 Sep 29 03:20 exp5_selection_result.json\n-rw-rw-rw-  1 aii-agent aii-agent   15890 Sep 29 03:20 frozen_spec.json\n-rw-rw-rw-  1 aii-agent aii-agent    2442 Sep 29 02:35 frozen_spec_v0.json\n-rw-rw-rw-  1 aii-agent aii-agent     943 Sep 29 03:28 learned_models_cohort.json\n-rw-rw-rw-  1 aii-agent aii-agent     719 Sep 29 02:42 learned_port_validation.json\n-rw-rw-rw-  1 aii-agent aii-agent  245108 Sep 29 03:10 llm_cost_log.csv\n-rw-rw-rw-  1 aii-agent aii-agent    6154 Sep 29 03:34 readme_tables.md\n-rw-rw-rw-  1 aii-agent aii-agent     670 Sep 29 03:41 rederive.json\n-rw-rw-rw-  1 aii-agent aii-agent     874 Sep 29 02:22 s1_candidates_summary.json\n-rw-rw-rw-  1 aii-agent aii-agent     423 Sep 29 03:01 s2_checks.json\n-rw-rw-rw-  1 aii-agent aii-agent    1205 Sep 29 03:01 s3_decision.json\n-rw-rw-rw-  1 aii-agent aii-agent     342 Sep 29 03:03 s4_gate_summary.json\n-rw-rw-rw-  1 aii-agent aii-agent     525 Sep 29 02:46 s6_checks.json\n-rw-rw-rw-  1 aii-agent aii-agent     265 Sep 29 03:02 s6_checks_cohort.json\n-rw-rw-rw-  1 aii-agent aii-agent    2857 Sep 29 03:10 type_benchmark_final.json\n-rw-rw-rw-  1 aii-agent aii-agent   21384 Sep 29 03:02 type_benchmark_v1.csv\n-rw-rw-rw-  1 aii-agent aii-agent    1861 Sep 29 03:04 type_benchmark_v1.json\n-rw-rw-rw-  1 aii-agent aii-agent   20750 Sep 29 03:06 type_benchmark_v2.csv\n-rw-rw-rw-  1 aii-agent aii-agent    1877 Sep 29 03:07 type_benchmark_v2.json\n-rw-rw-rw-  1 aii-agent aii-agent    5962 Sep 29 03:03 type_gold_labels_v1.csv\n-rw-rw-rw-  1 aii-agent aii-agent    5962 Sep 29 03:04 type_gold_labels_v2.csv\n-rw-rw-rw-  1 aii-agent aii-agent   21841 Sep 29 03:03 type_gold_sheet_v1.csv\n-rw-rw-rw-  1 aii-agent aii-agent     270 Sep 29 03:09 type_m2all.json\n-rw-rw-rw-  1 aii-agent aii-agent    2196 Sep 29 03:04 type_prompt_v2.txt\n-rw-rw-rw-  1 aii-agent aii-agent     472 Sep 29 02:28 u2_ego_flags.json\n-rw-rw-rw-  1 aii-agent aii-agent     444 Sep 29 03:31 u5_outcomes.json\n73 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/method.py\ntotal 1986\ndrwxrwxrwx 3 aii-agent aii-agent 1002581 Sep 30 01:59 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002581 Sep 30 01:58 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 01:58 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 01:59 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   26378 Sep 30 01:59 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-30 01:59:28 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $W/method.py; echo ----; cat $W/preview_method_out.json; echo ----; cat $W/reproducibility.md | head -80; ls $W/lib
```

### [11] TOOL RESULT — Bash · 2026-09-30 01:59:28 UTC

````
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).\n\nUsage: python method.py [--only STEP] [--from STEP] [--list]\nSteps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort\n                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate\n                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report\nNote: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nPY = sys.executable\nSTEPS = [\n    (\"s0\", [PY, \"s0_prereg.py\"]),\n    (\"s1\", [PY, \"s1_candidates.py\"]),\n    (\"passC\", [PY, \"passC.py\", \"--workers\", \"9\"]),\n    (\"passC_merge\", [PY, \"passC.py\", \"--merge\"]),\n    (\"s3\", [PY, \"s3_checks.py\"]),\n    (\"s4\", [PY, \"s4_gate.py\", \"run\"]),\n    (\"s4_retry\", [PY, \"s4_gate.py\", \"retry\"]),\n    (\"s7_exp5\", [PY, \"s7_ego.py\", \"--frame\", \"exp5\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"200\"]),\n    (\"s7_cohort\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"50\"]),\n    (\"s7_cohort_full\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"full\", \"--workers\", \"5\", \"--chunk\", \"20\",\n                        \"--tag\", \"_full\"]),\n    (\"s6\", [PY, \"s6_covariates.py\"]),\n    (\"s5_exp5\", [PY, \"s5_typing.py\", \"exp5\"]),\n    (\"s5_cohort\", [PY, \"s5_typing.py\", \"cohort\"]),\n    (\"s5_bench\", [PY, \"s5_typing.py\", \"bench\"]),\n    (\"s5_sheet\", [PY, \"s5_typing.py\", \"sheet\"]),\n    (\"s5_gate\", [PY, \"s5_typing.py\", \"gate\"]),\n    (\"s5_v2\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s5_typing.py',c,'--prompt','v2'],check=True) \"\n                          \"for c in ('exp5','cohort','bench','gate')]\"]),\n    (\"s5_m2all\", [PY, \"s5_typing.py\", \"m2all\", \"--prompt\", \"v2\"]),\n    (\"s8\", [PY, \"s8_select.py\", \"--nboot\", \"500\"]),\n    (\"s9\", [PY, \"s9_unseal.py\"]),\n    (\"learned\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s_learned.py',c],check=True) \"\n                           \"for c in ('validate','features','score')]\"]),\n    (\"audit\", [PY, \"audit.py\"]),\n    (\"tests\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,t],check=True) for t in \"\n                         \"('tests/test_output.py','tests/t_ego_flags.py','tests/t_outcomes.py','tests/test_units.py')]\"]),\n    (\"outputs\", [PY, \"make_outputs.py\"]),\n    (\"report\", [PY, \"make_report.py\"]),\n    (\"rederive\", [PY, \"rederive.py\"]),\n]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--only\")\n    ap.add_argument(\"--from\", dest=\"start\")\n    ap.add_argument(\"--list\", action=\"store_true\")\n    a = ap.parse_args()\n    names = [n for n, _ in STEPS]\n    if a.list:\n        print(\"\\n\".join(names))\n        return\n    todo = STEPS\n    if a.only:\n        todo = [s for s in STEPS if s[0] == a.only]\n    elif a.start:\n        todo = STEPS[names.index(a.start):]\n    for name, cmd in todo:\n        print(f\"== {name}: {' '.join(cmd[:4])}\", flush=True)\n        subprocess.run(cmd, cwd=ROOT, check=True)\n\n\nif __name__ == \"__main__\":\n    main()\n----\n{\n  \"metadata\": {\n    \"method_name\": \"OPEN (open-neighbourhood composite) vs B5 baseline, fresh 2015-2017 onset cohort (2017 = declared power extension)\",\n    \"verdict\": \"CONFIRMED\",\n    \"primary_outcome\": \"O2r_m50\",\n    \"predict_B5\": \"frozen OLS of O2r_m50 on standardised B5 fitted on the EXP5 frame\",\n    \"predict_B5_plus_OPEN_home\": \"frozen OLS on B5 + OPEN_home fitted on the EXP5 frame\",\n    \"outcome_grounding\": \"TAG\",\n    \"n\": 1443\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"fresh_cohort_2015_2017_open\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Electrical impedance myography\\\", \\\"openalex_id\\\": \\\"C1918360\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"BGM+Med\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"4.95097\",\n          \"predict_B5_plus_OPEN_home\": \"5.04306\",\n          \"metadata_OPEN_home\": 0.32132431470264056,\n          \"metadata_OPEN_all\": -0.12508189070586714,\n          \"metadata_OPEN_sizematch\": 0.12254799950962321,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 3,\n          \"metadata_fp_logN\": 4.04305126783455,\n          \"metadata_fp_nfields\": 3,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": null,\n          \"metadata_O1c\": -0.24116205681688863,\n          \"metadata_O1b\": 1,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": null,\n          \"metadata_O2r_m50_MATCH\": null,\n          \"metadata_logvol\": 4.02535169073515,\n          \"metadata_growth_c\": -0.3364722366212129,\n          \"metadata_offhome_share\": 0.19047619047619047,\n          \"metadata_entropy\": 0.7385104891120922,\n          \"metadata_reach\": 4,\n          \"metadata_CONTACT_REACH\": 4,\n          \"metadata_RETENTION_RATIO_early\": 0.0,\n          \"metadata_n_authors_early\": 4.962844630259907,\n          \"metadata_n_home_early\": 34,\n          \"metadata_n_all_early\": 55,\n          \"metadata_precision_c\": 0.9,\n          \"metadata_home\": \"27\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Persistent homology\\\", \\\"openalex_id\\\": \\\"C2874115\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"PHYS\\\"}\",\n          \"output\": \"9.39058\",\n          \"predict_B5\": \"7.45805\",\n          \"predict_B5_plus_OPEN_home\": \"NA\",\n          \"metadata_OPEN_home\": null,\n          \"metadata_OPEN_all\": 1.0279867793278947,\n          \"metadata_OPEN_sizematch\": null,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 2,\n          \"metadata_fp_logN\": 4.304065093204169,\n          \"metadata_fp_nfields\": 8,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": 4.921541872785715,\n          \"metadata_O1c\": 0.6061358035703153,\n          \"metadata_O1b\": 0,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": 9.390583535312317,\n          \"metadata_O2r_m50_MATCH\": 9.761747385271264,\n          \"metadata_logvol\": 4.356708826689592,\n          \"metadata_growth_c\": 0.3184537311185346,\n          \"metadata_offhome_share\": 0.7450980392156863,\n          \"metadata_entropy\": 1.6881963704692144,\n          \"metadata_reach\": 6,\n          \"metadata_CONTACT_REACH\": 7,\n          \"metadata_RETENTION_RATIO_early\": 0.42857142857142855,\n          \"metadata_n_authors_early\": 5.389071729816501,\n          \"metadata_n_home_early\": 13,\n          \"metadata_n_all_early\": 77,\n          \"metadata_precision_c\": 1.0,\n          \"metadata_home\": \"31\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Job rotation\\\", \\\"openalex_id\\\": \\\"C3082036\\\", \\\"t0\\\": 2015, \\\"home_group\\\": \\\"SOC\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"7.92326\",\n          \"predict_B5_plus_OPEN_home\": \"7.88886\",\n          \"metadata_OPEN_home\": 0.02274310364663708,\n          \"metadata_OPEN_all\": 0.8155822010123192,\n          \"metadata_OPEN_sizematch\": 0.21973513732250882,\n          \"metadata_type\": \"topic\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 5,\n          \"metadata_fp_logN\": 4.634728988229636,\n          \"metadata_fp_nfields\": 9,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 1,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": null,\n          \"metadata_O1c\": -0.029852963149681777,\n          \"metadata_O1b\": 0,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": null,\n          \"metadata_O2r_m50_MATCH\": 6.959276018099548,\n          \"metadata_logvol\": 4.219507705176107,\n          \"metadata_growth_c\": 0.16034265007517948,\n          \"metadata_offhome_share\": 0.6388888888888888,\n          \"metadata_entropy\": 1.7500458374633958,\n          \"metadata_reach\": 6,\n          \"metadata_CONTACT_REACH\": 7,\n          \"metadata_RETENTION_RATIO_early\": 0.14285714285714285,\n          \"metadata_n_authors_early\": 5.0369526024136295,\n          \"metadata_n_home_early\": 13,\n          \"metadata_n_all_early\": 67,\n          \"metadata_precision_c\": 1.0,\n          \"metadata_home\": \"14\",\n          \"metadata_window_flag\": 0\n        }\n      ]\n    }\n  ]\n}----\n# Reproducing the fresh-cohort OPEN test (RQ1)\n\nThis file describes what was actually run for this artifact (AI Inventor run, iteration 4, `gen_art_experiment_10`,\nplan `gen_plan_experiment_1_idx1`) on 2026-09-29. Every path below is relative to this folder.\n\n## 1. Get the artifact and its sibling inputs\n\nThis workspace is published as one folder of a public GitHub repository. Clone the repository and `cd` into this\nartifact's folder (`gen_art_experiment_10`). The code reads other run artifacts, which the repository publishes as\nsibling folders. All of them resolve through ONE constant, `RUN_ROOT` in `lib/common.py`, which defaults to four levels\nabove this folder (the run-tree layout: `<RUN_ROOT>/3_invention_loop/iter_N/gen_art/<folder>`). Set the environment\nvariable `AII_RUN_ROOT` to the folder that contains `3_invention_loop/` if your checkout is laid out differently.\n\n| input | artifact id / folder | what is read |\n|---|---|---|\n| EXP5 frame + scan | art_wxWssKSUR45f, `iter_2/gen_art/gen_art_experiment_5` | `frame_concepts.csv`, `scan/agg_counts.parquet`, `scan/year_field_totals.npz`, `scan/reservoir/`, `scan/llm_cache/` (read-only cache lookup), `concept_features_basic.csv`, `grounding_precision.csv`, `results/backbones.json` |\n| EXP8 indicators + frozen models | art_dFQ6jbgNsR6Q, `iter_3/gen_art/gen_art_experiment_8` | `data/frame_matches_early/`, `data/ego_features.parquet`, `data/features_basic.parquet`, `data/outcomes.parquet`, `data/bg_topics.npz` (copied into `data/`), `data/analysis_table.parquet`, `results/indicator_matrix.parquet`, `results/frozen_spec.json`, `results/learned_model.json`, `models/*.joblib`, `inputs/` (copied into `inputs/`) |\n| art_33 field backbone | `iter_1/gen_art/gen_art_experiment_4` | `field_backbone.json` (`phi_min`, learned-model inputs only) |\n| external recognition (declared dependency) | art_O7Dq4L02QnDN, `iter_2/gen_art/gen_art_dataset_2` | `full_data_out/full_data_out_{1,2,3}.json` (Wikipedia creation years -> `fp_wiki_pre`) |\n\nNo user-uploaded file is used.\n\n## 2. System, Python, libraries\n\n* Ubuntu / Debian 12 container, Python **3.12.14**, [uv](https://github.com/astral-sh/uv), curl.\n* Environment: `./restore.sh`. It runs `uv venv .venv --python=3.12` followed by\n  `uv pip install --python .venv/bin/python -r requirements.lock.txt`. The same pins are in `pyproject.toml`.\n* Key versions: numpy 2.5.3, pandas 3.0.6, pyarrow 25.0.1, scipy 1.18.1, scikit-learn 1.9.1, interpret 0.7.8,\n  python-igraph 1.0.0, leidenalg 0.12.0, statsmodels 0.15.0, pyahocorasick 2.3.1, snowballstemmer 3.1.1,\n  matplotlib 3.11.2, loguru 0.7.3, aiohttp 3.12.15. These are the EXP8 pins, so the frozen EXP8 joblib models unpickle.\n* Hardware used: 11 vCPU (cgroup quota 10.2 CPUs), 57 GB RAM. The GPU (RTX A4500) was **not** used.\n\n## 3. Data, credentials\n\n* **OpenAlex works snapshot 2026-09-23.** It is read over HTTP range requests from the public S3 bucket\n  `https://openalex.s3.amazonaws.com/data/parquet/works/`. The manifest in `snapshot/works_manifest.json` has 2,040\n  files and is identical to EXP5's (checked against the live `manifest.json`, kept in `snapshot/current_manifest.json`).\n  No API key is needed; **0 OpenAlex credits** were used.\n* **LLM calls (OpenRouter).** Env vars `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` (names only). Models:\n  google/gemini-2.5-flash-lite (precision gate + types) and openai/gpt-4.1-mini (type benchmark/fallback), temperature 0,\n  JSON mode. The total was **$2.04** (`results/llm_cost_log.csv`). Every response is cached in `llm_cache/`, keyed by\n  sha1 of (model, messages, temperature), so a re-run with the cache present makes no paid call.\n* Optional: `AII_RUN_ROOT` (see 1) and `AII_JSON_SKILL_DIR` (AI Inventor JSON validator; `tests/test_output.py` falls\n  back to a structural check).\n\n## 4. Commands, in the order they were run (`method.py --list` gives the same order)\n\nSeeds: bootstrap 20260929; SIZEMATCH draws 1000 + ci; control sample 7; EXP8 family-A nulls 20260928 + ci; benchmark\nand gold-sheet samples 20260929 / 7 / 11.\n\n```bash\n./restore.sh\n.venv/bin/python tests/test_output.py                       # U1\n.venv/bin/python s0_prereg.py                               # S0 pre-registration -> logs/seal.log\n.venv/bin/python s1_candidates.py                           # S1 1,535 candidates (t0 2015-17), 300 controls (<1 min)\n.venv/bin/python passC.py --files 65,1125,1407 --workers 3  # 3-file test\n.venv/bin/python passC.py --workers 9                       # S2 pass; run with 7, then 9, then 16 workers (resumable); ~30 min total\n.venv/bin/python passC.py --merge                           # ~2.5 min\n.venv/bin/python s7_ego.py --frame exp5 --builds all,home,sizematch --workers 2 --chunk 200   # 15 min\n.venv/bin/python tests/t_ego_flags.py                       # U2 (run on the 100-concept --tag _u2 subset first)\n.venv/bin/python s5_typing.py exp5                          # types v1, $0.31\n.venv/bin/python s4_gate.py u8                              # U8\n.venv/bin/python s6_covariates.py exp5\n.venv/bin/python s3_checks.py                               # T1-T3 + S3 decision (TAG)\n.venv/bin/python s4_gate.py run && .venv/bin/python s4_gate.py retry     # precision gate, $0.29\n.venv/bin/python s7_ego.py --frame cohort --builds all,home,sizematch --workers 3 --chunk 50\n.venv/bin/python s7_ego.py --frame cohort --builds full --workers 5 --chunk 20 --tag _full\n.venv/bin/python s6_covariates.py cohort\n.venv/bin/python s5_typing.py cohort && .venv/bin/python s5_typing.py bench && .venv/bin/python s5_typing.py sheet\n#   the executor agent read results/type_gold_sheet_v1.csv blind -> results/type_gold_labels_v1.csv (copied to _v2)\n.venv/bin/python s5_typing.py gate                          # gate v1 fails (method 0.73)\nfor c in exp5 cohort bench gate; do .venv/bin/python s5_typing.py $c --prompt v2; done   # gate v2 fails (method 0.80)\n.venv/bin/python s5_typing.py m2all --prompt v2             # declared fallback -> data/concept_types.csv\n.venv/bin/python tests/test_units.py && .venv/bin/python tests/t_outcomes.py   # U3, U4, U6, U7, U5\n.venv/bin/python s8_select.py --nboot 500                   # S8 selection + power + FREEZE (~8 min)\n.venv/bin/python s9_unseal.py --dryrun                      # synthetic counts, nothing unsealed\n.venv/bin/python s9_unseal.py                               # the SINGLE unseal + scoring (~5 min)\n.venv/bin/python s_learned.py validate && .venv/bin/python s_learned.py features && .venv/bin/python s_learned.py score\n.venv/bin/python audit.py                                   # independent audit (~2 min)\n.venv/bin/python make_outputs.py && .venv/bin/python make_report.py && .venv/bin/python readme_tables.py > results/readme_tables.md\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nfeatport.py\nframe_exp5.py\nh2.py\nindicators.py\nladder.py\nllmc.py\nmatcher.py\nmodels_exp5.py\noutc.py\noutjson.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal2.py\nseal_exp5.py\nstats_core.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [12] THINKING · 2026-09-30 01:59:34 UTC

```
`method.py` just orchestrates ~25 step scripts via subprocess, and since they need S3, OpenRouter LLM calls, and hours of compute, they can't run in a notebook. Now I'll dig into the scoring and statistics code so the demo can reproduce the headline numbers from the per-concept output.
```

### [13] TOOL CALL — Bash · 2026-09-30 01:59:34 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $W/s9_unseal.py; echo ======; cat $W/rederive.py; echo =====; wc -l $W/lib/*.py
```

### [14] TOOL RESULT — Bash · 2026-09-30 01:59:34 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"S9: the SINGLE unseal and the frozen scoring of the fresh 2015-2016(-2017) cohort.\n\n1. lib/seal2.unseal() (refuses without the matching frozen-spec hash, if the sealed parts changed, or on a 2nd call)\n2. cohort outcomes (lib/outc.outcomes, frozen windows; grounding from the frozen S3 decision) -> data/outcomes_cohort.parquet\n   (sha256 hash-chained into logs/seal.log)\n3. frozen ladder, groups (DL), within type, components, RETENTI... [truncated, 24397 chars total]
```

### [15] THINKING · 2026-09-30 01:59:46 UTC

```
I'll verify the per-concept input files that rederive.py depends on actually exist before running it to reproduce OPEN, the partial Spearman, and the placebo checks.
```

### [16] TOOL CALL — Bash · 2026-09-30 01:59:46 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; ls -la $W/data | head -60; cat $W/results/rederive.json; python3 -c "
import json;s=json.load(open('$W/results/frozen_spec.json'));print(list(s.keys()));print(json.dumps(s['open_constants'],indent=0)[:1500])"
```

### [17] TOOL RESULT — Bash · 2026-09-30 01:59:46 UTC

```
{"stdout": "total 47819\ndrwxrwxrwx  4 aii-agent aii-agent  2005380 Sep 29 03:28 .\ndrwxrwxrwx 15 aii-agent aii-agent  2023575 Sep 29 05:04 ..\n-rw-rw-rw-  1 aii-agent aii-agent   482680 Sep 29 03:22 analysis_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   298030 Sep 29 02:27 bg_topics.npz\n-rw-rw-rw-  1 aii-agent aii-agent   185249 Sep 29 02:22 cohort_candidates.csv\n-rw-rw-rw-  1 aii-agent aii-agent   215822 Sep 29 03:10 cohort_candidates_gated.csv\n-rw-rw-rw-  1 aii-agent aii-agent    35246 Sep 29 03:26 cohort_predictions.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   865822 Sep 29 03:09 concept_types.csv\n-rw-rw-rw-  1 aii-agent aii-agent    16381 Sep 29 02:22 controls.csv\n-rw-rw-rw-  1 aii-agent aii-agent    70902 Sep 29 03:02 covariates_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   374283 Sep 29 02:46 covariates_exp5.parquet\ndrwxrwxrwx  6 aii-agent aii-agent  2000456 Sep 29 03:02 ego_open\n-rw-rw-rw-  1 aii-agent aii-agent   133393 Sep 29 03:03 ego_open_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   206452 Sep 29 03:07 ego_open_cohort_full.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   921374 Sep 29 02:44 ego_open_exp5.parquet\n-rw-rw-rw-  1 aii-agent aii-agent    27700 Sep 29 02:28 ego_open_exp5_u2.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   230564 Sep 29 03:01 exp5_o2r_match_vs_tag.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   306889 Sep 29 03:20 features_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  2140942 Sep 29 03:20 features_exp5_open.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   360590 Sep 29 03:28 learned_features_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   164860 Sep 29 02:46 o5_events_all.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   184976 Sep 29 03:22 outcomes_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent    77636 Sep 29 03:00 passC_bg.npz\n-rw-rw-rw-  1 aii-agent aii-agent 31791546 Sep 29 03:00 passC_early.parquet\n-rw-rw-rw-  1 aii-agent aii-agent      264 Sep 29 03:01 passC_info.json\n-rw-rw-rw-  1 aii-agent aii-agent   309784 Sep 29 03:00 passC_pre_agg.parquet\n-rw-rw-rw-  1 aii-agent aii-agent     8753 Sep 29 03:00 passC_totals.npz\n-rw-rw-rw-  1 aii-agent aii-agent    36633 Sep 29 03:10 precision_cohort.csv\ndrwxrwxrwx  3 aii-agent aii-agent  2001021 Sep 29 02:23 sealed\n-rw-rw-rw-  1 aii-agent aii-agent    83560 Sep 29 03:02 types_cohort_v1.csv\n-rw-rw-rw-  1 aii-agent aii-agent    83575 Sep 29 03:06 types_cohort_v2.csv\n-rw-rw-rw-  1 aii-agent aii-agent   656036 Sep 29 02:39 types_exp5_v1.csv\n-rw-rw-rw-  1 aii-agent aii-agent   656108 Sep 29 03:06 types_exp5_v2.csv\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 573,\n  \"est\": 0.09059049284973039,\n  \"ci95_400boot\": [\n   0.010749623103553041,\n   0.1650051005616541\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.07152646838735872,\n  \"share_ge_observed\": 0.015\n },\n \"placebo_random_open_psp\": -0.027111739316867493,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 630,\n  \"est\": 0.17410165420736984,\n  \"ci95_400boot\": [\n   0.09568838543012635,\n   0.25899626408340093\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 573,\n  \"B5\": 0.7679289162717833,\n  \"B5_plus_OPEN_home\": 0.7703431304689959,\n  \"diff\": 0.0024142141972126607\n }\n}['prereg_sha256', 'spec_v0_sha256', 'open_constants', 'open_min_home_papers', 'open_min_components', 'outcome_grounding', 'primary', 'O2r_resid', 'extension_2017', 'power', 'type_labels_sha256', 'type_benchmark', 'rungs', 'groups', 'holm_family', 'directions', 'bootstrap', 'prediction_models', 'cohort_n', 'cohort_n_by_t0', 'sha256', 'code_sha256', 'pre_unseal_checklist']\n{\n\"home\": {\n\"new_edge_rate\": {\n\"lo\": 0.0,\n\"hi\": 2.0,\n\"mu\": 0.24226876611794407,\n\"sd\": 0.29476323739891586,\n\"sign\": 1,\n\"n\": 12499\n},\n\"n_comm_W3\": {\n\"lo\": 0.0,\n\"hi\": 5.0,\n\"mu\": 1.251940155212417,\n\"sd\": 1.1109950408968348,\n\"sign\": 1,\n\"n\": 12499\n},\n\"participation\": {\n\"lo\": 0.0,\n\"hi\": 0.7422196372922436,\n\"mu\": 0.23128455585636246,\n\"sd\": 0.2522103838072288,\n\"sign\": 1,\n\"n\": 8968\n},\n\"NOV_res\": {\n\"lo\": -0.9844771539499432,\n\"hi\": 0.09593876134862721,\n\"mu\": -0.540875353868789,\n\"sd\": 0.3801298233025086,\n\"sign\": 1,\n\"n\": 9475\n},\n\"ego_density_W3\": {\n\"lo\": 0.0,\n\"hi\": 1.0,\n\"mu\": 0.7333316442122908,\n\"sd\": 0.2796180574838275,\n\"sign\": -1,\n\"n\": 6810\n},\n\"edge_persistence\": {\n\"lo\": 0.0,\n\"hi\": 0.6739705882352984,\n\"mu\": 0.12122673391085216,\n\"sd\": 0.15763666320353067,\n\"sign\": -1,\n\"n\": 11236\n}\n},\n\"all\": {\n\"new_edge_rate\": {\n\"lo\": 0.0,\n\"hi\": 1.3333333333333333,\n\"mu\": 0.2137749421116557,\n\"sd\": 0.18712524937508748,\n\"sign\": 1,\n\"n\": 12499\n},\n\"n_comm_W3\": {\n\"lo\": 0.0,\n\"hi\": 8.0,\n\"mu\": 2.5383630690455234,\n\"sd\": 1.4439512430434749,\n\"sign\": 1,\n\"n\": 12499\n},\n\"participation\": {\n\"lo\": 0.0,\n\"hi\": 0.8162630102040815,\n\"mu\": 0.3770766100053555,\n\"sd\": 0.2530890675222482,\n\"sign\": 1,\n\"n\": 12167\n},\n\"NOV_res\": {\n\"lo\": -0.9817103130304184,\n\"hi\": 0.09383222083132174,\n\"mu\": -0.4551814113804676,\n\"sd\": 0.33277132442558904,\n\"sign\": 1,\n\"n\": 11747\n},\n\"ego_density_W3\": {\n\"lo\": 0.0,\n\"hi\": 1.0,\n\"mu\": 0.6560566200808624,\n\"sd\": 0.22979526084840923,\n\"sign\": -1,\n\"n\": 11547\n},\n\"edge_persistence\": {\n\"lo\": 0.0,\n\"hi\": 0.7083333333333333,\n\"mu", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-30 01:59:58 UTC

```
The per-concept tables and frozen constants are all there. I'll check the columns I need, using a throwaway uv environment in the scratchpad.
```

### [19] TOOL CALL — Bash · 2026-09-30 01:59:58 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad 2>/dev/null || mkdir -p /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --python /usr/local/bin/python3.12 $S/venv && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $S/venv/bin/python pandas pyarrow scipy
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10
$S/venv/bin/python -c "
import pandas as pd
F=pd.read_parquet('$W/data/features_cohort.parquet'); print(F.shape); print(list(F.columns))
print(F[['agroup','type','t0','level','generic']].describe(include='all'))
print(F.agroup.value_counts())
O=pd.read_parquet('$W/data/outcomes_cohort.parquet'); print(O.shape, [c for c in O.columns][:20])
P=pd.read_parquet('$W/data/cohort_predictions.parquet'); print(P.head())
"
```

### [20] TOOL RESULT — Bash · 2026-09-30 02:00:02 UTC

```
{"stdout": "(1443, 72)\n['ci', 'concept_id', 'qid', 'name', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'early_volume', 'role', 'intersection_born', 'precision_c', 'n_labelled_prec', 'precision_source', 'pass_gate', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'agroup', 'home_coverage_early', 'window_flag', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch']\n         agroup    type           t0        level      generic\ncount      1443    1443  1443.000000  1443.000000  1443.000000\nunique        6       4          NaN          NaN          NaN\ntop     BGM+Med  object          NaN          NaN          NaN\nfreq        585     721          NaN          NaN          NaN\nmean        NaN     NaN  2015.863479     3.102564     0.006930\nstd         NaN     NaN     0.797058     0.888679     0.082986\nmin         NaN     NaN  2015.000000     2.000000     0.000000\n25%         NaN     NaN  2015.000000     2.000000     0.000000\n50%         NaN     NaN  2016.000000     3.000000     0.000000\n75%         NaN     NaN  2017.000000     4.000000     0.000000\nmax         NaN     NaN  2017.000000     5.000000     1.000000\nagroup\nBGM+Med    585\nSOC        299\nCS+Eng     239\nLIFEENV    167\nPHYS       123\nMATHDEC     30\nName: count, dtype: int64\n(1443, 42) ['ci', 'O1b_TAG', 'O3_TAG', 'peak_year_TAG', 'N_outcome_TAG', 'O2r_m50_TAG', 'O2r_m30_TAG', 'O1c_TAG', 'N_late_all_TAG', 'O1b_MATCH', 'O3_MATCH', 'peak_year_MATCH', 'N_outcome_MATCH', 'O2r_m50_MATCH', 'O2r_m30_MATCH', 'O1c_MATCH', 'N_late_all_MATCH', 'O1b', 'O3', 'O2r_m50']\n    ci   pred_b5  pred_b5_open\n0  233  4.950966      5.043059\n1  346  7.458054           NaN\n2  378  7.923256      7.888856\n3  380  6.543314      6.721870\n4  390  5.580782           NaN", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-30 02:00:20 UTC

```
Next I'll build `mini_demo_data.json`: 100 concepts from the analysis set, sampled by group, plus the frozen constants and the full-cohort reference numbers.
```

### [22] TOOL CALL — Bash · 2026-09-30 02:00:20 UTC

```
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
OUT=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
cat > $S/make_mini.py <<'EOF'
import json, math
import numpy as np, pandas as pd
W = "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10"
OUT = "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/mini_demo_data.json"
F = pd.read_parquet(f"{W}/data/features_cohort.parquet")
O = pd.read_parquet(f"{W}/data/outcomes_cohort.parquet")[["ci", "O2r_m50"]]
P = pd.read_parquet(f"{W}/data/cohort_predictions.parquet")
spec = json.load(open(f"{W}/results/frozen_spec.json"))
res = json.load(open(f"{W}/results/cohort_result.json"))
red = json.load(open(f"{W}/results/rederive.json"))
D = F.merge(O, on="ci").merge(P, on="ci")
B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
ok = D.OPEN_home.notna() & D.O2r_m50.notna() & D[B5].notna().all(1) & D.pred_b5_open.notna()
A = D[ok]
print("analysis set", len(A))
# proportional stratified sample by group, 100 concepts
rng = np.random.default_rng(20260929)
N = 100
share = A.agroup.value_counts(normalize=True)
k = (share * N).round().astype(int)
while k.sum() > N: k[k.idxmax()] -= 1
while k.sum() < N: k[k.idxmin()] += 1
parts = [A[A.agroup == g].sample(n=int(n), random_state=int(rng.integers(1e9))) for g, n in k.items() if n > 0]
S_ = pd.concat(parts).sort_values("ci")
comps = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
cols = (["ci", "concept_id", "name", "t0", "agroup", "type", "generic", "level", "n_home_early", "n_all_early"]
        + B5 + ["CONTACT_REACH"] + [f"{c}__{b}" for b in ("home", "all") for c in comps]
        + ["OPEN_home", "OPEN_all", "O2r_m50", "pred_b5", "pred_b5_open"])
def clean(v):
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating, float)): return None if not math.isfinite(float(v)) else float(v)
    return v
rows = [{c: clean(r[c]) for c in cols} for _, r in S_.iterrows()]
Pm = res["primary"]
ref = {"primary_ladder": {k: {"rho": v["rho"], "ci": v["ci"], "n": v.get("n")} for k, v in Pm.items()
                          if "|O2r_m50|" in k},
       "verdict": res["verdict"]["verdict"],
       "frozen_prediction_O2r_m50": res["secondary"]["frozen_prediction_O2r_m50"],
       "rederive": red}
data = {"metadata": {"description": "100-concept stratified (by analysis group) sample of the 573-concept analysis set "
                     "(finite OPEN_home and O2r_m50) of the fresh 2015-2017 OpenAlex onset cohort; per-concept raw "
                     "ego-network components, B5 covariates, outcome, and frozen B5 / B5+OPEN_home predictions.",
                     "n_examples": len(rows), "n_analysis_set_full": int(len(A)), "n_cohort_full": int(len(F)),
                     "sample_seed": 20260929},
        "open_constants": {b: spec["open_constants"][b] for b in ("home", "all")},
        "open_min_home_papers": spec["open_min_home_papers"], "open_min_components": spec["open_min_components"],
        "full_cohort_reference": ref,
        "concepts": rows}
json.dump(data, open(OUT, "w"), indent=1)
print(k.to_dict(), len(rows))
print(spec["open_min_home_papers"], spec["open_min_components"])
print(list(ref["primary_ladder"].keys())[:8])
EOF
$S/venv/bin/python $S/make_mini.py && ls -la $OUT/mini_demo_data.json
```

### [23] TOOL RESULT — Bash · 2026-09-30 02:00:20 UTC

```
{"stdout": "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad/make_mini.py:13: Pandas4Warning: Starting with pandas version 4.0 all arguments of all will be keyword-only.\n  ok = D.OPEN_home.notna() & D.O2r_m50.notna() & D[B5].notna().all(1) & D.pred_b5_open.notna()\nanalysis set 573\n{'BGM+Med': 47, 'CS+Eng': 20, 'SOC': 17, 'LIFEENV': 9, 'PHYS': 5, 'MATHDEC': 2} 100\n10 4\n['OPEN_home|O2r_m50|R0', 'OPEN_home|O2r_m50|R1', 'OPEN_home|O2r_m50|R2', 'OPEN_home|O2r_m50|R3', 'OPEN_home|O2r_m50|R4', 'OPEN_home|O2r_m50|R5', 'OPEN_all|O2r_m50|R0', 'OPEN_all|O2r_m50|R1']\n-rw-rw-rw- 1 aii-agent aii-agent 110055 Sep 30 02:00 /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] ASSISTANT · 2026-09-30 02:01:48 UTC

```
The mini data is ready: 100 concepts, sampled to match each group's share of the 573-concept analysis set. Now I'll write the notebook generator.
```

### [25] TOOL CALL — Bash · 2026-09-30 02:01:48 UTC

```
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
cat > $S/make_nb.py <<'PYEOF'
import json, sys
OUT = "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb"
N_BOOT, N_PERM = sys.argv[1], sys.argv[2]
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md(r"""
# Do open-neighbourhood concepts spread? Fresh-cohort test (demo)

This notebook demos the **fresh-cohort OPEN test** (research question RQ1). We ask whether a new scientific concept spreads further
when its early co-occurrence neighbourhood is *open* (new edges, many communities, novel pairings, low density and
persistence). The cohort is OpenAlex legacy concepts whose onset year is 2015–2017.

**What the full experiment did**
- One S3 pass over the OpenAlex works snapshot (2026-09-23), then an LLM precision gate. This left **1,443 concepts**:
  634 have the primary outcome `O2r_m50`, and 573 have `OPEN_home`.
- **OPEN** is the mean of six signed, z-scored ego-network components. The clip and z constants were frozen on the 12,499 EXP5
  concepts. OPEN is built three ways: ALL, HOME-ONLY and SIZE-MATCHED.
- The test statistic is the **partial Spearman** between OPEN and the outcome, after controlling for a ladder of covariate
  sets (R0 = B5 + onset year, then contact reach, LLM concept type, footprint, coverage and group FE).
  The spec was hash-sealed before the single unseal.
- **Result:** CONFIRMED but marginal. `OPEN_home` has psp = +0.091 [+0.013, +0.171] at R2. It adds no practical prediction
  (B5 Spearman 0.768 vs 0.770). `OPEN_all` gives +0.174, so there is large mechanical coupling.

**What this notebook runs**
1. The original `method.py` orchestrator. It lists the 25 pipeline steps in order. Those steps need S3 access, paid LLM calls
   and hours of compute, so they are **listed, not executed**.
2. The artifact's own *independent re-derivation* of the headline numbers (`rederive.py`), with the code unchanged. It runs
   on a **100-concept stratified sample** of the 573-concept analysis set. It rebuilds OPEN from the raw components with
   the frozen constants, computes the R2 partial Spearman with a bootstrap CI, runs the two placebos, and compares the
   B5 and B5+OPEN_home predictions.
3. A results cell that compares the sample estimates with the full-cohort numbers stored in the data file.

> With only 100 of the 573 concepts, the confidence intervals are about 2.4× wider than in the paper. The point
> estimates show what the method does; they are not a replication of the full result.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# All packages used here are pre-installed on Colab -> install locally only, at Colab's exact versions
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
""")

code(r"""
# --- original imports of method.py (orchestrator) ---
import argparse
import subprocess
import sys
from pathlib import Path

# --- original imports of rederive.py (independent re-derivation of the headline numbers) ---
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# --- added for the notebook's results cell ---
import time
import matplotlib.pyplot as plt
""")

code(r"""
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-4/experiment-10/demo/mini_demo_data.json"
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
print(data["metadata"]["description"])
print("concepts in demo file:", len(data["concepts"]),
      "| full analysis set:", data["metadata"]["n_analysis_set_full"],
      "| full cohort:", data["metadata"]["n_cohort_full"])
""")

md(r"""
## Configuration

These are all the tunable parameters. The original values are noted in the comments. The notebook runs in seconds even at
the original values, so the original values are used.
""")

code(f"""
N_CONCEPTS = 100    # concepts from the demo file to use (max 100; the full analysis set has 573 OPEN_home / 630 OPEN_all)
N_BOOT = {N_BOOT}        # bootstrap draws for the partial-Spearman CI   (original rederive.py: 400; s9_unseal.py: B from frozen spec)
N_PERM = {N_PERM}        # within-group outcome permutations (placebo)    (original: 200)
BOOT_SEED = 1       # original rederive.py seed (np.random.default_rng(1))
""")

md(r"""
## 1. The pipeline orchestrator (`method.py`)

`method.py` is the artifact's entry point. It runs each research step as a separate script, in the order below:

| step(s) | what it does |
|---|---|
| `s0` | pre-registration (hash-sealed) |
| `s1` | 1,535 candidate concepts with 2015–17 onsets, plus 300 controls |
| `passC`, `passC_merge` | one zero-credit S3 pass over the OpenAlex works snapshot; outcome-window counts are **sealed** |
| `s3` | snapshot checks T1–T3 and the outcome-blind TAG vs MATCH grounding decision |
| `s4`, `s4_retry` | LLM precision gate (94 % pass) |
| `s7_*` | ego-network components for the ALL / HOME / SIZE-MATCHED builds (EXP5 frame and the cohort) |
| `s6` | B5 covariates, contact reach, footprint |
| `s5_*` | LLM concept typing, gold-label benchmark and type gate (failed twice → declared M1 = M2 fallback) |
| `s8` | selection, power check (0.16 → declared 2017 extension), **freeze** of the spec |
| `s9` | the **single unseal**, then scoring against the frozen ladder, groups, contrasts, Holm and the verdict |
| `learned`, `audit`, `tests`, `outputs`, `report`, `rederive` | EXP8 learned-model replication, independent audit, unit tests, output files |

The code below is the original script. There are two notebook-only changes: `ROOT` is the current directory (a notebook
has no `__file__`), and `main()` takes an `argv` list instead of reading the command line. We call it with `--list`: the
step scripts and the sealed data are not part of this demo, so running a step would fail.
""")

code(r'''
"""Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).

Usage: python method.py [--only STEP] [--from STEP] [--list]
Steps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort
                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate
                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report
Note: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file."""

ROOT = Path.cwd()  # notebook: was Path(__file__).resolve().parent
PY = sys.executable
STEPS = [
    ("s0", [PY, "s0_prereg.py"]),
    ("s1", [PY, "s1_candidates.py"]),
    ("passC", [PY, "passC.py", "--workers", "9"]),
    ("passC_merge", [PY, "passC.py", "--merge"]),
    ("s3", [PY, "s3_checks.py"]),
    ("s4", [PY, "s4_gate.py", "run"]),
    ("s4_retry", [PY, "s4_gate.py", "retry"]),
    ("s7_exp5", [PY, "s7_ego.py", "--frame", "exp5", "--builds", "all,home,sizematch", "--workers", "3", "--chunk", "200"]),
    ("s7_cohort", [PY, "s7_ego.py", "--frame", "cohort", "--builds", "all,home,sizematch", "--workers", "3", "--chunk", "50"]),
    ("s7_cohort_full", [PY, "s7_ego.py", "--frame", "cohort", "--builds", "full", "--workers", "5", "--chunk", "20",
                        "--tag", "_full"]),
    ("s6", [PY, "s6_covariates.py"]),
    ("s5_exp5", [PY, "s5_typing.py", "exp5"]),
    ("s5_cohort", [PY, "s5_typing.py", "cohort"]),
    ("s5_bench", [PY, "s5_typing.py", "bench"]),
    ("s5_sheet", [PY, "s5_typing.py", "sheet"]),
    ("s5_gate", [PY, "s5_typing.py", "gate"]),
    ("s5_v2", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,'s5_typing.py',c,'--prompt','v2'],check=True) "
                          "for c in ('exp5','cohort','bench','gate')]"]),
    ("s5_m2all", [PY, "s5_typing.py", "m2all", "--prompt", "v2"]),
    ("s8", [PY, "s8_select.py", "--nboot", "500"]),
    ("s9", [PY, "s9_unseal.py"]),
    ("learned", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,'s_learned.py',c],check=True) "
                           "for c in ('validate','features','score')]"]),
    ("audit", [PY, "audit.py"]),
    ("tests", [PY, "-c", "import subprocess,sys;[subprocess.run([sys.executable,t],check=True) for t in "
                         "('tests/test_output.py','tests/t_ego_flags.py','tests/t_outcomes.py','tests/test_units.py')]"]),
    ("outputs", [PY, "make_outputs.py"]),
    ("report", [PY, "make_report.py"]),
    ("rederive", [PY, "rederive.py"]),
]


def main(argv=None) -> None:  # notebook: argv parameter added (was: command line)
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args(argv)
    names = [n for n, _ in STEPS]
    if a.list:
        print("\n".join(names))
        return
    todo = STEPS
    if a.only:
        todo = [s for s in STEPS if s[0] == a.only]
    elif a.start:
        todo = STEPS[names.index(a.start):]
    for name, cmd in todo:
        print(f"== {name}: {' '.join(cmd[:4])}", flush=True)
        subprocess.run(cmd, cwd=ROOT, check=True)


main(["--list"])   # was: `python method.py --list`
''')

md(r"""
## 2. Load the per-concept tables

The original `rederive.py` reads four files: `data/features_cohort.parquet` (raw components and covariates),
`data/outcomes_cohort.parquet` (the unsealed outcome `O2r_m50`), `results/frozen_spec.json` (frozen OPEN constants) and
`data/cohort_predictions.parquet` (frozen B5 / B5+OPEN_home predictions). The demo file holds the same columns for 100
concepts, so we rebuild the same `spec`, `F`, `O` and `D` objects from it. `SIGN` gives the frozen direction of each of
the six components.
""")

code(r"""
# notebook: the parquet / JSON reads of rederive.py are replaced by the demo data
C = pd.DataFrame(data["concepts"]).head(N_CONCEPTS)
spec = {"open_constants": data["open_constants"]}                  # was: results/frozen_spec.json
F = C.drop(columns=["O2r_m50", "pred_b5", "pred_b5_open"])         # was: data/features_cohort.parquet
O = C[["ci", "O2r_m50"]]                                           # was: data/outcomes_cohort.parquet
D = F.merge(O, on="ci")
SIGN = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
        "edge_persistence": -1}

print(D.shape)
print(D.agroup.value_counts().to_dict())
D[["name", "t0", "agroup", "type", "OPEN_home", "OPEN_all", "O2r_m50"]].head()
""")

md(r"""
## 3. Rebuild OPEN from the six raw components

For each component: clip it to the frozen `[lo, hi]` range, z-score it with the frozen EXP5 `mu`/`sd`, and apply its sign.
OPEN is the mean of the available signed z-scores. It is defined only when at least 4 of the 6 components are present,
and, for the HOME build, only when the concept has at least 10 home-field papers in the early window.
""")

code(r"""
def open_score(build):
    c = spec["open_constants"][build]
    zs = []
    for k, s in SIGN.items():
        v = D[f"{k}__{build}"].clip(c[k]["lo"], c[k]["hi"])
        zs.append(s * (v - c[k]["mu"]) / c[k]["sd"])
    Z = pd.concat(zs, axis=1)
    o = Z.mean(axis=1, skipna=True).where(Z.notna().sum(axis=1) >= 4)
    if build != "all":
        o = o.where(D.n_home_early >= 10)
    return o
""")

md(r"""
## 4. The R2 design matrix and the partial Spearman

Rung **R2** controls for three things:
- the ranks of the five B5 covariates (log early volume, growth, off-home share, field entropy, field reach) and
  `CONTACT_REACH`;
- onset-year dummies;
- LLM concept type, generic flag and OpenAlex level dummies.

The **partial Spearman** ranks OPEN and the outcome, regresses both rank vectors on the design matrix (by QR projection),
and correlates the residuals. Columns that are collinear or empty are dropped first. With a small sample this matters,
because some dummy levels do not appear.
""")

code(r"""
def design(d):
    cont = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH"]
    X = [np.ones(len(d))] + [d[c].rank().to_numpy() for c in cont]
    for y in (2016, 2017):
        X.append((d.t0 == y).to_numpy(float))
    for t in ("method", "object", "property"):
        X.append((d["type"] == t).to_numpy(float))
    X.append(d["generic"].to_numpy(float))
    for lv in (3, 4, 5):
        X.append((d.level == lv).to_numpy(float))
    return np.column_stack(X)


def psp(x, y, X):
    keep = np.abs(np.linalg.qr(X)[1].diagonal()) > 1e-9      # drop collinear / empty dummy columns
    Q, _ = np.linalg.qr(X[:, keep])
    rx = pd.Series(x).rank().to_numpy(); ry = pd.Series(y).rank().to_numpy()
    rx = rx - Q @ (Q.T @ rx); ry = ry - Q @ (Q.T @ ry)
    return float(np.corrcoef(rx, ry)[0, 1])
""")

md(r"""
## 5. Re-derive the headline statistic, with bootstrap CI and placebos

For both builds (HOME and ALL), this cell does four things:
1. Checks that the rebuilt OPEN matches the stored value exactly (`max_abs_diff` should be 0).
2. Computes the R2 partial Spearman with OPEN → `O2r_m50`, plus a concept-level bootstrap CI.
3. For HOME only, runs the placebos. Placebo 1 shuffles the outcome within analysis groups; the observed estimate should
   exceed most of these values. Placebo 2 replaces OPEN with random noise, which should give a value near 0.

The loop is the original code. Only the draw counts use `N_BOOT` / `N_PERM` instead of the hard-coded 400 / 200.
""")

code(r"""
t_start = time.time()
out = {}
for b in ("home", "all"):
    o = open_score(b)
    out[f"OPEN_{b}_max_abs_diff_vs_frozen_table"] = float(np.nanmax(np.abs(o - F[f"OPEN_{b}"])))
    d = D.assign(o=o).dropna(subset=["o", "O2r_m50", "logvol", "growth_c", "offhome_share", "entropy", "reach"])
    d = d.reset_index(drop=True)
    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))
    rng = np.random.default_rng(BOOT_SEED)
    bs = []
    for _ in range(N_BOOT):                                   # original: range(400)
        i = rng.integers(0, len(d), len(d))
        di = d.iloc[i].reset_index(drop=True)
        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))
    out[f"OPEN_{b}_psp_R2"] = {"n": len(d), "est": est, "ci95_400boot": [float(np.percentile(bs, 2.5)),
                                                                          float(np.percentile(bs, 97.5))]}
    if b == "home":
        # placebo 1: within-group shuffled outcome; placebo 2: random OPEN
        perm = []
        for _ in range(N_PERM):                               # original: range(200)
            y = d.O2r_m50.to_numpy().copy()
            for g in d.agroup.unique():
                m = (d.agroup == g).to_numpy()
                y[m] = rng.permutation(y[m])
            perm.append(psp(d.o.to_numpy(), y, design(d)))
        perm = np.abs(perm)
        out["placebo_shuffled_outcome"] = {"q95_abs": float(np.percentile(perm, 95)),
                                           "share_ge_observed": float((perm >= abs(est)).mean())}
        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))
        out["placebo_random_open_psp"] = rnd
print(f"elapsed {time.time() - t_start:.1f}s")
""")

md(r"""
## 6. Does OPEN_home add predictive value? (frozen B5 vs B5 + OPEN_home)

Both prediction models are frozen OLS fits on the EXP5 frame, applied here without refitting. We compare the Spearman
correlation of each model's prediction with the realised `O2r_m50`. In the full cohort the gain is only +0.002.
""")

code(r"""
P = C[["ci", "pred_b5", "pred_b5_open"]].merge(O, on="ci").dropna()   # was: data/cohort_predictions.parquet
s0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]
out["prediction_spearman"] = {"n": len(P), "B5": float(s0), "B5_plus_OPEN_home": float(s1), "diff": float(s1 - s0)}
# (ROOT / "results/rederive.json").write_text(json.dumps(out, indent=1))   # notebook: not written to disk
print(json.dumps(out, indent=1))
""")

md(r"""
## 7. Results: 100-concept demo vs the full sealed cohort

The table puts this notebook's estimates next to the full-cohort numbers (n = 573 / 630) from the artifact's
`results/rederive.json` and `results/cohort_result.json`. The three plots show:
- **(a)** the R2 estimates with 95 % CIs, demo vs full;
- **(b)** the full-cohort ladder R0 → R5 for the three OPEN builds;
- **(c)** the frozen B5 prediction against the realised outcome for the demo concepts.
""")

code(r"""
ref = data["full_cohort_reference"]
red = ref["rederive"]
rows = []
for b in ("home", "all"):
    k = f"OPEN_{b}_psp_R2"
    rows.append({"quantity": f"psp(OPEN_{b}, O2r_m50 | R2)",
                 "demo": f"{out[k]['est']:+.3f} [{out[k]['ci95_400boot'][0]:+.3f}, {out[k]['ci95_400boot'][1]:+.3f}]  n={out[k]['n']}",
                 "full cohort": f"{red[k]['est']:+.3f} [{red[k]['ci95_400boot'][0]:+.3f}, {red[k]['ci95_400boot'][1]:+.3f}]  n={red[k]['n']}"})
    rows.append({"quantity": f"OPEN_{b} rebuild max |diff|", "demo": f"{out[f'OPEN_{b}_max_abs_diff_vs_frozen_table']:.2e}",
                 "full cohort": f"{red[f'OPEN_{b}_max_abs_diff_vs_frozen_table']:.2e}"})
rows.append({"quantity": "placebo: shuffled-outcome q95 |psp|", "demo": f"{out['placebo_shuffled_outcome']['q95_abs']:.3f}",
             "full cohort": f"{red['placebo_shuffled_outcome']['q95_abs']:.3f}"})
rows.append({"quantity": "placebo: share |perm| >= |observed|", "demo": f"{out['placebo_shuffled_outcome']['share_ge_observed']:.3f}",
             "full cohort": f"{red['placebo_shuffled_outcome']['share_ge_observed']:.3f}"})
rows.append({"quantity": "placebo: random-OPEN psp", "demo": f"{out['placebo_random_open_psp']:+.3f}",
             "full cohort": f"{red['placebo_random_open_psp']:+.3f}"})
for m in ("B5", "B5_plus_OPEN_home", "diff"):
    rows.append({"quantity": f"prediction Spearman: {m}", "demo": f"{out['prediction_spearman'][m]:+.3f}",
                 "full cohort": f"{red['prediction_spearman'][m]:+.3f}"})
summary = pd.DataFrame(rows).set_index("quantity")
print("Frozen verdict (full cohort):", ref["verdict"])
print(summary.to_string())

fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
# (a) R2 estimates, demo vs full
ax = axes[0]
labels, ests, los, his, cols = [], [], [], [], []
for b in ("home", "all"):
    k = f"OPEN_{b}_psp_R2"
    for src, dct, col in (("demo", out, "tab:orange"), ("full", red, "tab:blue")):
        labels.append(f"OPEN_{b}\n({src}, n={dct[k]['n']})")
        ests.append(dct[k]["est"]); los.append(dct[k]["ci95_400boot"][0]); his.append(dct[k]["ci95_400boot"][1]); cols.append(col)
yy = np.arange(len(labels))[::-1]
for yi, e, lo, hi, c in zip(yy, ests, los, his, cols):
    ax.errorbar(e, yi, xerr=[[e - lo], [hi - e]], fmt="o", color=c, capsize=4)
ax.axvline(0, color="grey", lw=1, ls="--")
ax.set_yticks(yy); ax.set_yticklabels(labels, fontsize=8)
ax.set_xlabel("partial Spearman with O2r_m50 (R2), 95% CI")
ax.set_title("(a) Re-derived R2 statistic: demo vs full")

# (b) full-cohort ladder
ax = axes[1]
L = ref["primary_ladder"]
rungs = ["R0", "R1", "R2", "R3", "R4", "R5"]
for j, (b, c) in enumerate((("home", "tab:blue"), ("sizematch", "tab:green"), ("all", "tab:red"))):
    xs = np.arange(len(rungs)) + (j - 1) * 0.2
    r = [L[f"OPEN_{b}|O2r_m50|{g}"]["rho"] for g in rungs]
    lo = [L[f"OPEN_{b}|O2r_m50|{g}"]["ci"][0] for g in rungs]
    hi = [L[f"OPEN_{b}|O2r_m50|{g}"]["ci"][1] for g in rungs]
    ax.errorbar(xs, r, yerr=[np.subtract(r, lo), np.subtract(hi, r)], fmt="o", color=c, capsize=3, label=f"OPEN_{b}")
ax.axhline(0, color="grey", lw=1, ls="--")
ax.set_xticks(range(len(rungs))); ax.set_xticklabels(rungs)
ax.set_ylabel("partial Spearman with O2r_m50")
ax.set_title("(b) Full cohort: covariate ladder R0 -> R5")
ax.legend(fontsize=8)

# (c) frozen predictions vs outcome (demo concepts)
ax = axes[2]
ax.scatter(P.pred_b5, P.O2r_m50, s=18, alpha=0.7, label=f"B5 (rho={out['prediction_spearman']['B5']:.3f})")
ax.scatter(P.pred_b5_open, P.O2r_m50, s=18, alpha=0.7, marker="x",
           label=f"B5+OPEN_home (rho={out['prediction_spearman']['B5_plus_OPEN_home']:.3f})")
ax.set_xlabel("frozen prediction of O2r_m50"); ax.set_ylabel("realised O2r_m50")
ax.set_title("(c) Frozen predictions, demo concepts")
ax.legend(fontsize=8)
plt.tight_layout()
plt.show()
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
json.dump(nb, open(OUT, "w"), indent=1)
print("wrote", OUT, len(cells), "cells")
PYEOF
$S/venv/bin/python $S/make_nb.py 10 10
```

### [26] TOOL RESULT — Bash · 2026-09-30 02:01:48 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb 21 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-30 02:01:54 UTC

```
Test run at the minimal config (10 bootstrap draws, 10 permutations):
```

### [28] TOOL CALL — Bash · 2026-09-30 02:01:54 UTC

```
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5; echo "runtime $(( $(date +%s)-T0 ))s"
```

### [29] TOOL RESULT — Bash · 2026-09-30 02:02:22 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 168953 bytes to code_demo.ipynb\nruntime 24s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-30 02:02:26 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[-1500:])
        elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
        elif 'text/plain' in o.get('data',{}): print(''.join(o['data']['text/plain'])[:600])
    print('-----')
"
```

### [31] TOOL RESULT — Bash · 2026-09-30 02:02:26 UTC

```
{"stdout": "-----\n-----\n-----\n100-concept stratified (by analysis group) sample of the 573-concept analysis set (finite OPEN_home and O2r_m50) of the fresh 2015-2017 OpenAlex onset cohort; per-concept raw ego-network components, B5 covariates, outcome, and frozen B5 / B5+OPEN_home predictions.\nconcepts in demo file: 100 | full analysis set: 573 | full cohort: 1443\n\n-----\n-----\ns0\ns1\npassC\npassC_merge\ns3\ns4\ns4_retry\ns7_exp5\ns7_cohort\ns7_cohort_full\ns6\ns5_exp5\ns5_cohort\ns5_bench\ns5_sheet\ns5_gate\ns5_v2\ns5_m2all\ns8\ns9\nlearned\naudit\ntests\noutputs\nreport\nrederive\n\n-----\n(100, 31)\n{'BGM+Med': 47, 'CS+Eng': 20, 'SOC': 17, 'LIFEENV': 9, 'PHYS': 5, 'MATHDEC': 2}\n\n                      name    t0   agroup      type  OPEN_home  OPEN_all  \\\n0     Bilevel optimization  2016   CS+Eng    method   0.076289  0.015344   \n1  Cognitive restructuring  2016      SOC    method  -0.414827  0.135138   \n2       Market value added  2017      SOC  property  -0.355677 -0.151155   \n3    Material point method  2015   CS+Eng    method   0.096802 -0.123865   \n4     Planetary boundaries  2016  LIFEENV     topic  -0.173572  0.254732   \n\n     O2r_m50  \n0   5.522978  \n1   3.983368  \n2   2.000000  \n3   3.953069  \n4  10.971015  \n-----\n-----\n-----\nelapsed 0.1s\n\n-----\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.09040114517573995,\n  \"ci95_400boot\": [\n   -0.05157477049172967,\n   0.4180530149466577\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.1799438633252416,\n  \"share_ge_observed\": 0.5\n },\n \"placebo_random_open_psp\": 0.10747372379729529,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.05629523571970651,\n  \"ci95_400boot\": [\n   -0.19255593074533545,\n   0.3508800719398139\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 100,\n  \"B5\": 0.7417866293960695,\n  \"B5_plus_OPEN_home\": 0.7492634219362134,\n  \"diff\": 0.007476792540143884\n }\n}\n\n-----\nFrozen verdict (full cohort): CONFIRMED\n                                                                  demo                     full cohort\nquantity                                                                                              \npsp(OPEN_home, O2r_m50 | R2)            +0.090 [-0.052, +0.418]  n=100  +0.091 [+0.011, +0.165]  n=573\nOPEN_home rebuild max |diff|                                  0.00e+00                        0.00e+00\npsp(OPEN_all, O2r_m50 | R2)             +0.056 [-0.193, +0.351]  n=100  +0.174 [+0.096, +0.259]  n=630\nOPEN_all rebuild max |diff|                                   0.00e+00                        0.00e+00\nplacebo: shuffled-outcome q95 |psp|                              0.180                           0.072\nplacebo: share |perm| >= |observed|                              0.500                           0.015\nplacebo: random-OPEN psp                                        +0.107                          -0.027\nprediction Spearman: B5                                         +0.742                          +0.768\nprediction Spearman: B5_plus_OPEN_home                          +0.749                          +0.770\nprediction Spearman: diff                                       +0.007                          +0.002\n\n<Figure size 1700x480 with 3 Axes>\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-30 02:02:36 UTC

```
The minimal run passes in 24 s total; the analysis cell itself took 0.1 s. The original counts (400 bootstrap draws, 200 permutations) will clearly fit, so I'll scale straight to them.
```

### [33] TOOL CALL — Bash · 2026-09-30 02:02:36 UTC

```
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF && $S/venv/bin/python $S/make_nb.py 400 200 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -2; echo "runtime $(( $(date +%s)-T0 ))s"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][-5:]:
    for o in c.get('outputs',[]):
        if o['output_type']=='stream': print(''.join(o['text'])[-2500:])
        elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
        elif 'image/png' in o.get('data',{}): print('[image]')
"
```

### [34] TOOL RESULT — Bash · 2026-09-30 02:03:02 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb 21 cells\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 168746 bytes to code_demo.ipynb\nruntime 26s\nelapsed 1.1s\n\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.09040114517573995,\n  \"ci95_400boot\": [\n   -0.10912630133608538,\n   0.3048045046190029\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.18340327879592852,\n  \"share_ge_observed\": 0.38\n },\n \"placebo_random_open_psp\": -0.04170792754696268,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.05629523571970651,\n  \"ci95_400boot\": [\n   -0.17697593265702985,\n   0.2632704899771419\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 100,\n  \"B5\": 0.7417866293960695,\n  \"B5_plus_OPEN_home\": 0.7492634219362134,\n  \"diff\": 0.007476792540143884\n }\n}\n\nFrozen verdict (full cohort): CONFIRMED\n                                                                  demo                     full cohort\nquantity                                                                                              \npsp(OPEN_home, O2r_m50 | R2)            +0.090 [-0.109, +0.305]  n=100  +0.091 [+0.011, +0.165]  n=573\nOPEN_home rebuild max |diff|                                  0.00e+00                        0.00e+00\npsp(OPEN_all, O2r_m50 | R2)             +0.056 [-0.177, +0.263]  n=100  +0.174 [+0.096, +0.259]  n=630\nOPEN_all rebuild max |diff|                                   0.00e+00                        0.00e+00\nplacebo: shuffled-outcome q95 |psp|                              0.183                           0.072\nplacebo: share |perm| >= |observed|                              0.380                           0.015\nplacebo: random-OPEN psp                                        -0.042                          -0.027\nprediction Spearman: B5                                         +0.742                          +0.768\nprediction Spearman: B5_plus_OPEN_home                          +0.749                          +0.770\nprediction Spearman: diff                                       +0.007                          +0.002\n\n[image]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] ASSISTANT · 2026-09-30 02:03:10 UTC

```
The notebook passes at the original values: 400 bootstrap draws and 200 permutations. The whole run takes 26 s, and the analysis cell takes 1.1 s. I'll check the figure.
```

### [36] TOOL CALL — Bash · 2026-09-30 02:03:10 UTC

```
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for o in nb['cells'][-1]['outputs']:
    if 'image/png' in o.get('data',{}): open('$S/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [37] TOOL RESULT — Bash · 2026-09-30 02:03:10 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Read · 2026-09-30 02:03:10 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad/fig.png
```

### [39] TOOL RESULT — Read · 2026-09-30 02:03:10 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [40] ASSISTANT · 2026-09-30 02:03:26 UTC

```
The figure renders correctly. I'll add a short interpretation cell at the end, re-run the notebook, and then write the README, manifest and output JSON.
```

### [41] TOOL CALL — Bash · 2026-09-30 02:03:26 UTC

```
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad
python3 - <<'EOF'
p="/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/05cef561-5d70-4293-8d87-1700d2666012/scratchpad/make_nb.py"
s=open(p).read()
add='''
md(r"""
### Reading the results

- **The OPEN rebuild is exact.** Rebuilding OPEN from the raw components with the frozen constants reproduces the stored
  values (max |diff| = 0), just as it does on the full cohort.
- **The point estimate matches, the sample is too small.** On 100 concepts, the `OPEN_home` R2 estimate is close to the
  full-cohort value, but its CI crosses 0. This is expected: in the full cohort the effect is only marginal
  (+0.091, CI lower bound +0.011, Holm p = 0.048), and it needs the full n = 573 to clear zero.
- **The ALL vs HOME gap needs the full cohort.** In the full cohort `OPEN_all` > `OPEN_sizematch` > `OPEN_home` at every
  rung of panel (b), because papers outside the home field feed back into the neighbourhood. A 100-concept sample is too
  noisy to show this ordering.
- **OPEN adds no practical prediction.** Adding `OPEN_home` to the frozen B5 model barely moves the prediction Spearman,
  both here and in the full cohort (0.768 → 0.770).
- To get the full-cohort numbers, run the original pipeline (`python method.py`, which needs the sealed data and the
  sibling run artifacts), or run `rederive.py` in the artifact folder on the full per-concept tables.
""")
'''
s=s.replace('\nnb = {"cells"', add+'\nnb = {"cells"')
open(p,"w").write(s)
EOF
cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF && $S/venv/bin/python $S/make_nb.py 400 200 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/python jupyter ipykernel && T0=$(date +%s) && /tmp/aii_nb_test_envs/art_NMe386dX9GLF-af31f9885a79/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "runtime $(( $(date +%s)-T0 ))s"
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
print(sum(1 for c in nb['cells'] for o in c.get('outputs',[]) if o['output_type']=='error'),'errors')
src=''.join(''.join(c['source']) for c in nb['cells'])
print('URL ok:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-4/experiment-10/demo/mini_demo_data.json\"' in src, 'urlopen' in src)
"; ls -la
```

### [42] TOOL RESULT — Bash · 2026-09-30 02:03:52 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb 22 cells\n[NbConvertApp] Writing 170163 bytes to code_demo.ipynb\nruntime 24s\n0 errors\nURL ok: True True\ntotal 2603\ndrwxrwxrwx 3 aii-agent aii-agent 1052795 Sep 30 02:01 .\ndrwxrwxrwx 4 aii-agent aii-agent 1069654 Sep 30 02:02 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 01:58 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 01:59 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  260337 Sep 30 02:03 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent  170180 Sep 30 02:03 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent  110055 Sep 30 02:00 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-30 02:04:02 UTC

```
Everything passes. Last, the README, the manifest (nothing heavy was created) and the output JSON.
```

### [44] TOOL CALL — Bash · 2026-09-30 02:04:02 UTC

````
cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: this workspace holds only a notebook (~170 KB) and a JSON data file (~110 KB).
# The test venv lives outside the workspace on local disk and is removed by the pipeline.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: do open-neighbourhood concepts spread? (fresh-cohort test)

This is a Colab-ready demo notebook for the experiment artifact **art_NMe386dX9GLF**. It is the single-unseal
confirmation test of the RQ1 openness claim, run on a fresh 2015–2017 onset cohort of OpenAlex legacy concepts.

## What is here

| path | what it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, already executed with outputs. It contains two pieces of the artifact's original code: the `method.py` orchestrator (it lists the 25 pipeline steps) and the `rederive.py` independent re-derivation (it rebuilds OPEN, computes the R2 partial Spearman with a 400-draw bootstrap CI, runs 200 shuffled-outcome permutations plus a random-OPEN placebo, and compares the frozen B5 and B5+OPEN_home predictions). A final cell compares the demo numbers with the full cohort. |
| `mini_demo_data.json` | 100 concepts sampled from the 573-concept analysis set, keeping each analysis group's share (seed 20260929). For each concept it holds the raw ego-network components (HOME and ALL builds), the B5 covariates, `CONTACT_REACH`, type, level, `O2r_m50` and the frozen predictions. It also holds the frozen OPEN constants and the full-cohort reference results: the R0–R5 ladder, the verdict and `rederive.json`. |

## How to run

- **Colab:** open `code_demo.ipynb` and choose *Run all*. The data file loads from the GitHub raw URL.
- **Locally:** keep `mini_demo_data.json` next to the notebook. If the URL cannot be reached, the notebook falls back to
  the local file.
  ```bash
  uv venv --seed --python 3.12 .venv && uv pip install --python .venv/bin/python jupyter ipykernel
  .venv/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
  ```
  The whole notebook runs in about 25 s, including the install cell. It uses the original 400 bootstrap draws and
  200 permutations.

The config cell exposes `N_CONCEPTS` (up to 100), `N_BOOT` (original 400) and `N_PERM` (original 200).
The full pipeline (`method.py`) needs the sealed OpenAlex outcome data, the sibling run artifacts and OpenRouter
credentials, so the notebook only lists its steps and does not run them.

## Restoring removed files

Nothing is marked for deletion in `.aii/manifest.yaml`, so there is nothing to restore.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json
````

### [45] TOOL RESULT — Bash · 2026-09-30 02:04:04 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-30 02:04:13 UTC

```
I built the demo notebook and its data file. The notebook runs cleanly in the fresh test venv in about 24 s, at the original 400 bootstrap draws and 200 permutations.

**What was in the artifact:** `method.py` only runs the pipeline: it calls about 25 step scripts in order through subprocess. Those steps need the sealed OpenAlex outcome data, S3 access and paid LLM calls, so they can't run in a notebook. The notebook therefore has two parts:
1. **`method.py` as written**, with two small changes: `ROOT = Path.cwd()` because a notebook has no `__file__`, and `main(argv)` in place of the command line. It is called with `--list`, so it prints the step order and runs nothing.
2. **The artifact's own `rederive.py` re-derivation**, with the code unchanged. Only the parquet and JSON reads were swapped for the loaded data, and the draw counts now come from config variables. It rebuilds OPEN from the six raw components using the frozen constants, computes the R2 partial Spearman with a bootstrap CI, runs the shuffled-outcome and random-OPEN placebos, and compares the frozen B5 and B5+OPEN_home predictions.

**Results on the 100-concept sample** (full-cohort values from the artifact in brackets):

| Check | Demo, n=100 | Full cohort |
|---|---|---|
| OPEN rebuilt from components vs stored value | exact match | exact match |
| OPEN_home partial Spearman (R2) | +0.090, CI [−0.109, +0.305] | +0.091, CI [+0.011, +0.165], n=573 |
| OPEN_all partial Spearman (R2) | +0.056 | +0.174, n=630 |
| Prediction Spearman, B5 → B5+OPEN_home | 0.742 → 0.749 | 0.768 → 0.770 |

The OPEN_home point estimate matches the paper, but its CI includes 0 on this sample. That is expected, since the full-cohort effect is marginal and needs all 573 concepts to clear zero. The sample also can't reproduce the ALL-above-HOME gap. The notebook text says both things so a reader doesn't take the demo as a replication.

The final cell prints a demo-vs-full table and draws three panels: the estimates with their CIs, the full-cohort R0–R5 ladder for the three OPEN builds, and the frozen predictions against the realised outcome.

**Data file:** `mini_demo_data.json` holds 100 concepts sampled so each analysis group keeps its share of the 573. It also stores the frozen OPEN constants and the full-cohort reference numbers used in the comparison.

**Checks:** the exact `GITHUB_DATA_URL` string is in the notebook, it loads from the URL with a local-file fallback, and there were no cell errors. `.terminal_claude_agent_struct_out.json` is written. No heavy files were created, so `.aii/manifest.yaml` has no entries.

Files are in `art_NMe386dX9GLF/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
