# gen_demo_art_experiment_1 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_1` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:01:56 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:02:04 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/results/out.json`
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
id: art_xp8BGBJZsxeI
type: experiment
title: Does citing a concept 'as your own' predict its spread?
summary: |-
  Screen of candidate L, the background-adjusted naturalisation gap A*_h, on the frozen P78 dev panel. Headline: it does NOT survive the pre-registered rule.
  PANEL: 48 dev concepts (Biochem 13, CS 21, Engineering 3, Medicine 11). Dropped: 22 with t0 outside 2003-2009 and 8 with a sealed home field.
  RULE CLAUSES:
  - LOGO Delta-rho for O2r over B5 = -0.006, 90% concept-bootstrap CI [-0.034, 0.017]; rho_B5 = 0.834. FAIL.
  - Positive left-out groups: 0 of 4. FAIL.
  - Split-half reliability (Spearman-Brown) = 0.58. FAIL (bar 0.6).
  - Abs Spearman with log early volume / early growth = 0.14 / 0.18. PASS.
  OTHER RESULTS:
  - A*_h's within-field sign flips: Medicine +0.45, CS -0.18.
  - Field-level rho*_cj -> R_j: Delta-AUC +0.002, CI [-0.011, 0.016], over 367 units.
  - O1 uptake: Delta-AUC -0.026. O3 transience is degenerate (4 positives of 48).
  - M1: R^2 of raw lineage log-OR on background log-OR = 0.66; the background log-OR is positive for 48/48 concepts. Raw lineage is mostly homophily.
  - Reliability vs n: 0.72 only above 60 off-home children. On those 11 concepts Delta-rho = +0.118, CI [0, 0.355], underpowered.
  - REML tau_c = 0.29, tau_cj = 0.65. PyMC NUTS check passes (Spearman 0.9996 with REML).
  - None of the 14 candidate and foil features, scored as exploratory candidates, beats B5.
  DATA DEVIATION: the shared OpenAlex credit pool ran dry (139 own credits spent). Yearly counts (t0, O1, O3, volume, growth) are OpenAlex S0 exactly. Field labels, concept papers, citation lineage and background-reference fields come from free Semantic Scholar data: fractional s2-fos text-classifier fields. Child reference lists come from free OpenAlex singleton GETs. The S2 and OpenAlex O2r agree with Spearman 0.87 on 11 concepts.
  AUDIT (audit/rederive.py, independent code paths): Delta-rho, rho_B, the size correlations, O1 Delta-AUC and M1 are re-derived exactly; field-level Delta-AUC is 0.0020. A shuffled-A*_h placebo passes 0 of 200 times. Power caveat: with rho_B5 = 0.83, a feature needs Spearman of about 0.95 or more with O2r to pass the Delta >= 0.10 clause. Reliability 0.58 was NOT independently re-derived.
  FILES: results/features.csv, field_features.csv, outcomes.csv, field_outcomes.csv, screen_result.json (all statistics and deviations), screen_table.csv (OOF predictions), dropped.csv, audit/rederive_out.json. method_out.json follows exp_gen_sol_out and holds per-concept B5 and B5+A*_h predictions plus field-retention units.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 21:02:10 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 21:02:10 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 21:02:10 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 21:02:10 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 21:02:10 UTC

```
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; ls -la $W; du -sh $W/*; wc -l $W/method.py
```

### [8] TOOL RESULT — Bash · 2026-09-29 21:02:12 UTC

```
{"stdout": "total 1985\ndrwxrwxrwx 3 aii-agent aii-agent 1002266 Sep 29 21:01 .\ndrwxrwxrwx 5 aii-agent aii-agent 1005137 Sep 29 21:01 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:01 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:01 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   23251 Sep 29 21:02 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:01 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002266 Sep 29 21:01 ..\ntotal 15794\ndrwxrwxrwx 8 aii-agent aii-agent 2012504 Sep 28 16:51 .\ndrwxrwxrwx 7 aii-agent aii-agent 2066645 Sep 28 11:43 ..\ndrwxrwxrwx 2 aii-agent aii-agent   71500 Sep 28 14:13 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 28 12:16 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   11022 Sep 28 14:13 .aii_worker_result.json\n-rw-rw-rw- 1 aii-agent aii-agent 3347802 Sep 28 14:13 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent    3139 Sep 28 14:07 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 aii-agent aii-agent   12557 Sep 28 14:10 README.md\ndrwxrwxrwx 2 aii-agent aii-agent 1000989 Sep 28 14:06 audit\ndrwxrwxrwx 3 aii-agent aii-agent 2006699 Sep 28 13:49 cache\n-rw-rw-rw- 1 aii-agent aii-agent    4294 Sep 28 12:54 fetch_bg.py\n-rw-rw-rw- 1 aii-agent aii-agent    4502 Sep 28 12:39 fetch_s2.py\n-rw-rw-rw- 1 aii-agent aii-agent  255536 Sep 28 14:05 full_method_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    2273 Sep 28 12:32 ground.py\n-rw-rw-rw- 1 aii-agent aii-agent   15743 Sep 28 13:23 lineage.py\ndrwxrwxrwx 2 aii-agent aii-agent 2000126 Sep 28 13:50 logs\n-rw-rw-rw- 1 aii-agent aii-agent   46747 Sep 28 13:55 method.py\n-rw-rw-rw- 1 aii-agent aii-agent  236543 Sep 28 14:00 method_out.json\n-rw-rw-rw- 1 aii-agent aii-agent   10412 Sep 28 14:05 mini_method_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    7051 Sep 28 12:51 oa.py\n-rw-rw-rw- 1 aii-agent aii-agent    2963 Sep 28 12:23 panel.py\n-rw-rw-rw- 1 aii-agent aii-agent    6645 Sep 28 12:40 pool.py\n-rw-rw-rw- 1 aii-agent aii-agent    7930 Sep 28 14:05 preview_method_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    1728 Sep 28 14:05 pyproject.toml\n-rw-rw-rw- 1 aii-agent aii-agent       9 Sep 28 12:43 pytest.ini\n-rw-rw-rw- 1 aii-agent aii-agent    5850 Sep 28 14:07 reproducibility.md\ndrwxrwxrwx 4 aii-agent aii-agent 2005296 Sep 28 13:58 results\n-rw-rw-rw- 1 aii-agent aii-agent    8720 Sep 28 12:28 s0.py\n-rw-rw-rw- 1 aii-agent aii-agent    3460 Sep 28 12:44 s2.py\n-rw-rw-rw- 1 aii-agent aii-agent    4653 Sep 28 13:55 screen.py\ndrwxrwxrwx 2 aii-agent aii-agent 1000532 Sep 28 16:51 tests\n13K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/README.md\n989K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/audit\n73M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/cache\n4.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/fetch_bg.py\n4.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/fetch_s2.py\n250K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/full_method_out.json\n2.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/ground.py\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py\n3.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/logs\n46K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py\n231K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method_out.json\n11K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/mini_method_out.json\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/oa.py\n3.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/panel.py\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/pool.py\n8.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/preview_method_out.json\n2.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/pyproject.toml\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/pytest.ini\n6.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/reproducibility.md\n129M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results\n9.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py\n3.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s2.py\n5.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/screen.py\n983K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/tests\n808 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 21:02:16 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; sed -n 1,300p $W/method.py
```

### [10] TOOL RESULT — Bash · 2026-09-29 21:02:16 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Screen of candidate L, the background-adjusted naturalisation gap A*_h, on the frozen dev panel P78.\n\nPipeline (see README.md for the deviations forced by the shared OpenAlex credit pool running dry):\n  S0      OpenAlex yearly counts (t0, newborn, O1, O3, log early volume, early growth) + S2 field distributions\n          (home, dev restriction with sealed held-out fields, O2r rarefied breadth, field retention R_j, B5 reach).\n  Lineage concept-paper citation links (S2 citation lists), self links split off, fractional S2 field labels.\n  Stage 1 per concept x off-home field j: year-stratified MH log-OR (child j vs H) x (parent j vs H) minus the same\n          log-OR on the same children's background references; child-bootstrap variance.\n  Stage 2 REML crossed random-effects pooling -> rho*_cj, A*_h = sum_j pi_cj rho*_cj (PyMC NUTS headline check,\n          statsmodels BinomialBayesMixedGLM robustness).\n  Screen  LOGO (4 dev home-field groups) ridge Delta-rho over B5 for O2r (2,000 concept bootstrap), per-group signs,\n          split-half reliability (50 splits, Spearman-Brown), size correlations, O1/O3 Delta-AUC, field-level\n          rho*_cj -> R_j test (concept-clustered bootstrap), M1, foils, pre-registered survival rule.\nUsage: python method.py [--max-concepts N] [--splits 50] [--no-pymc] [--no-glmm]\n\"\"\"\nfrom __future__ import annotations\n\nimport os\n\nfor _v in (\"OMP_NUM_THREADS\", \"OPENBLAS_NUM_THREADS\", \"MKL_NUM_THREADS\"):  # small matrices: avoid BLAS oversubscription\n    os.environ.setdefault(_v, \"1\")\n\nimport argparse\nimport gzip\nimport json\nimport math\nimport multiprocessing as mp\nimport pickle\nimport resource\nimport sys\nimport time\nfrom concurrent.futures import ProcessPoolExecutor\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy.stats import spearmanr\n\nROOT = Path(__file__).resolve().parent\nRES = ROOT / \"results\"\nsys.path.insert(0, str(ROOT))\n\nfrom lineage import (F, S2_DEV, S2_FIELDS, Concept, crude_lor, foils, load_concept, load_raw, membership,  # noqa: E402\n                     stage1)\nfrom panel import DEV_FIELDS, seeded_order, slug  # noqa: E402\nfrom pool import fit_dl, fit_pymc, fit_reml, predict, var_of  # noqa: E402\nfrom s0 import compute_s0, newborn, onset, rarefied_richness, shannon  # noqa: E402\nfrom screen import compare, rho, spearman_brown  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n(ROOT / \"logs\").mkdir(exist_ok=True)\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSEED = 20260928\nPROBE_CRUDE = {\"optogenetics\": -0.551, \"crowdsourcing\": 0.382, \"extreme learning machine\": -1.063,\n               \"induced pluripotent stem cell\": -0.628, \"compressed sensing\": 0.243}\nB5_COLS = [\"B_logvol\", \"B_growth\", \"B_offhome\", \"B_entropy\", \"B_nfields\"]\nBINS = [(0, 15), (15, 30), (30, 60), (60, 10**9)]\n\n\ndef set_limits() -> None:\n    ram = 16 * 1024 ** 3\n    resource.setrlimit(resource.RLIMIT_AS, (ram * 2, ram * 2))\n\n\ndef jsonable(o):\n    if isinstance(o, dict):\n        return {str(k): jsonable(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [jsonable(v) for v in o]\n    if isinstance(o, (np.floating, float)):\n        return None if not np.isfinite(o) else float(o)\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, np.ndarray):\n        return jsonable(o.tolist())\n    if isinstance(o, (np.bool_,)):\n        return bool(o)\n    return o\n\n\n# ------------------------------------------------------------------ S0\ndef s0_openalex() -> tuple[dict, pd.DataFrame, pd.DataFrame]:\n    raw = json.loads((RES / \"s0_raw.json\").read_text())\n    G = {int(k): v for k, v in raw[\"_G\"].items()}\n    counts = {}\n    for c in seeded_order():\n        v = raw[c[\"canonical\"]]\n        counts[c[\"canonical\"]] = {int(k): x for k, x in v[\"yc\"].items()} if isinstance(v[\"yc\"], dict) else None\n    rows, frows, dropped = compute_s0(raw, seeded_order())  # OpenAlex topic-field S0 (credit-bound subset)\n    return {\"G\": G, \"yc\": counts, \"oa_home_raw\": raw}, pd.DataFrame(rows), pd.DataFrame(dropped)\n\n\ndef count_outcomes(yc: dict[int, int], G: dict[int, int], t0: int) -> dict:\n    share = lambda y: yc.get(y, 0) / G[y]\n    peak = max(yc.get(y, 0) for y in range(t0 + 3, t0 + 9))\n    tail = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])\n    return {\"t0\": t0, \"newborn\": bool(newborn(yc, t0)),\n            \"O1\": int(np.mean([share(y) for y in range(t0 + 6, t0 + 9)]) >= share(t0 + 5)),\n            \"O3\": int(tail == 0 or peak / tail >= 2),\n            \"B_logvol\": math.log1p(sum(yc.get(y, 0) for y in range(t0, t0 + 5))),\n            \"B_growth\": math.log((yc.get(t0 + 4, 0) + 1) / (yc.get(t0 + 1, 0) + 1))}\n\n\ndef s0_s2(c: Concept) -> tuple[dict, list[dict]]:\n    \"\"\"Field-based S0 parts from the S2 paper sample (fractional labels, scaled by the thinning factor).\"\"\"\n    t0 = c.t0\n    lab = c.labelled\n\n    def mass(y0: int, y1: int) -> np.ndarray:\n        m = lab & (c.year >= y0) & (c.year <= y1)\n        return c.M[m].sum(0) * c.thin_early\n\n    fe, f01, f34 = mass(t0, t0 + 4), mass(t0, t0 + 1), mass(t0 + 3, t0 + 4)\n    fl = c.late_mass * c.thin_late\n    H = c.H\n    Ne, Nl = fe.sum(), fl.sum()\n    offm = np.ones(F, bool)\n    offm[H] = False\n    row = {\"home_s2\": \"|\".join(S2_FIELDS[h] for h in H),\n           \"O2r\": rarefied_richness(list(fl), 30), \"O2r_m50\": rarefied_richness(list(fl), 50),\n           \"O2r_m20\": rarefied_richness(list(fl), 20), \"N_late\": float(Nl), \"O2r_hurdle\": int(Nl >= 30),\n           \"B_offhome\": float(fe[offm].sum() / Ne) if Ne else np.nan,\n           \"B_entropy\": shannon(list(fe)), \"B_nfields\": int((fe >= 2).sum()),\n           \"off_early_vol\": math.log1p(fe[offm].sum()),\n           \"off_growth\": math.log((f34[offm].sum() + 1) / (f01[offm].sum() + 1)),\n           \"label_coverage_early\": float(lab.mean()) if len(lab) else np.nan,\n           \"late_sample_n\": int(round(c.late_mass.sum())), \"thin_early\": c.thin_early, \"thin_late\": c.thin_late}\n    frows = []\n    for j in np.where(offm & (fe >= 5))[0]:\n        se, sl = fe[j] / Ne, (fl[j] / Nl if Nl else 0.0)\n        frows.append({\"concept\": c.name, \"field\": S2_FIELDS[j], \"j\": int(j), \"R_j\": int(sl >= 0.5 * se and fl[j] >= 9),\n                      \"n_j_early\": float(fe[j]), \"n_j_late\": float(fl[j]), \"log_n_j_early\": math.log(fe[j]),\n                      \"growth_j\": math.log((f34[j] + 1) / (f01[j] + 1)), \"share_j\": float(se)})\n    return row, frows\n\n\ndef load_bg(c: Concept, sl: str) -> tuple[np.ndarray, np.ndarray]:\n    p = RES / \"concepts\" / sl / \"bg.json.gz\"\n    n = len(c.child_idx)\n    B = np.zeros((n, F))\n    has = np.zeros(n, bool)\n    if not p.exists():\n        return B, has\n    d = json.loads(gzip.decompress(p.read_bytes()))\n    pos = {c.ids[ci]: k for k, ci in enumerate(c.child_idx)}\n    for pid, refs in d[\"refs\"].items():\n        k = pos.get(pid)\n        if k is None:\n            continue\n        ms = [membership(d[\"fos\"].get(r)) for r in refs]\n        ms = [m for m in ms if m is not None]\n        if ms:\n            B[k] = np.mean(ms, axis=0)\n            has[k] = True\n    return B, has\n\n\n# ------------------------------------------------------------------ stage 2 wrapper\ndef pool_all(units: list[dict], names: list[str], n_off: dict, engine: str = \"reml\"):\n    \"\"\"units: stage-1 data rows {ci, field, k-order}. Returns fit and per-concept feature dict.\"\"\"\n    y = np.array([u[\"rho_hat\"] for u in units])\n    v = np.array([u[\"v\"] for u in units])\n    cidx = np.array([u[\"ci\"] for u in units])\n    fields = [u[\"field\"] for u in units]\n    fit = (fit_reml if engine == \"reml\" else fit_dl)(y, v, cidx, len(names), fields)\n    return fit\n\n\ndef concept_features(fit, units: list[dict], names: list[str], child_mass: dict) -> dict:\n    by_c: dict[int, list[int]] = {}\n    for k, u in enumerate(units):\n        by_c.setdefault(u[\"ci\"], []).append(k)\n    p = len(fit.beta)\n    nc = len(fit.u)\n    grand = float(np.mean(fit.X @ fit.beta)) if len(units) else float(\"nan\")\n    out = {}\n    for ci, name in enumerate(names):\n        ks = by_c.get(ci, [])\n        if not ks:\n            out[name] = {\"A_h\": grand, \"A_h_sd\": float(\"nan\"), \"A_h_missing\": 1, \"A_h_u\": float(fit.u[ci]),\n                         \"n_nat_fields\": 0, \"max_rho\": float(\"nan\"), \"n_data_fields\": 0}\n            continue\n        wts = np.array([child_mass[(ci, units[k][\"field\"])] for k in ks])\n        wts = wts / wts.sum()\n        L = np.zeros(len(fit.Cinv))\n        vals, n_nat = [], 0\n        for w_, k in zip(wts, ks):\n            val, l = predict(fit, ci, units[k][\"field\"], k)\n            sd = math.sqrt(max(var_of(fit, l), 1e-12))\n            vals.append(val)\n            n_nat += int(val > 0 and 0.5 * (1 + math.erf(val / sd / math.sqrt(2))) > 0.8)\n            L += w_ * l\n        lu = np.zeros(len(fit.Cinv))\n        lu[p + ci] = 1\n        out[name] = {\"A_h\": float(L[:p] @ fit.beta + (L[p:p + nc] @ fit.u) + (L[p + nc:] @ fit.w)),\n                     \"A_h_sd\": math.sqrt(max(var_of(fit, L), 0)), \"A_h_missing\": 0, \"A_h_u\": float(fit.u[ci]),\n                     \"A_h_u_sd\": math.sqrt(max(var_of(fit, lu), 0)),\n                     \"n_nat_fields\": n_nat, \"max_rho\": float(max(vals)), \"n_data_fields\": len(ks)}\n    return out\n\n\ndef stage1_units(concepts: list[Concept], bgs: list, subs: list | None = None, n_boot: int = 200,\n                 seed: int = SEED) -> tuple[list[dict], dict, list]:\n    units, child_mass, s1s = [], {}, []\n    for ci, c in enumerate(concepts):\n        B, has = bgs[ci]\n        sub = None if subs is None else subs[ci]\n        if len(c.child_idx) == 0 or (sub is not None and len(sub) == 0):\n            s1s.append(None)\n            continue\n        s = stage1(c, B, has, sub=sub, n_boot=n_boot, seed=seed + ci)\n        s1s.append(s)\n        for j in np.where(np.isfinite(s.rho_hat) & (s.n_child_j >= 1.0))[0]:\n            units.append({\"ci\": ci, \"field\": S2_FIELDS[j], \"j\": int(j), \"rho_hat\": float(s.rho_hat[j]),\n                          \"v\": float(s.v[j]), \"lor_c\": float(s.lor_c[j]), \"lor_bg\": float(s.lor_bg[j]),\n                          \"n_child_j\": float(s.n_child_j[j])})\n            child_mass[(ci, S2_FIELDS[j])] = float(s.n_child_j[j])\n    return units, child_mass, s1s\n\n\n# ------------------------------------------------------------------ split-half reliability (worker)\n_W: dict = {}\n\n\ndef _init_worker(pkl: str) -> None:\n    import os\n    os.environ.setdefault(\"OMP_NUM_THREADS\", \"1\")\n    logger.remove()\n    _W[\"data\"] = pickle.loads(Path(pkl).read_bytes())\n\n\ndef _half_crude(c: Concept, B: np.ndarray, has: np.ndarray, sub: np.ndarray) -> tuple[float, float]:\n    cH = c.cH[sub]\n    Pm = c.P[sub]\n    tot = Pm.sum(1)\n    par_off = np.where(tot > 0, 1 - (Pm @ c.hmask) / np.where(tot > 0, tot, 1), 0)\n    br = has[sub]\n    if not br.any():\n        return float(\"nan\"), float(\"nan\")\n    Bm = B[sub][br]\n    bt = Bm.sum(1)\n    b_off = np.where(bt > 0, 1 - (Bm @ c.hmask) / np.where(bt > 0, bt, 1), 0)\n    bgl = crude_lor(1 - cH[br], b_off)\n    return bgl, crude_lor(1 - cH[br], par_off[br]) - bgl\n\n\ndef run_split(s: int) -> dict:\n    concepts, bgs, names = _W[\"data\"]\n    rng = np.random.default_rng(SEED + 1000 + s)\n    halves = [[], []]\n    for c in concepts:\n        n = len(c.child_idx)\n        if n == 0:\n            halves[0].append(np.zeros(0, int)); halves[1].append(np.zeros(0, int))\n            continue\n        cH = c.cH\n        h0, h1 = [], []\n        for grp in (np.where(cH >= 0.5)[0], np.where(cH < 0.5)[0]):\n            g = rng.permutation(grp)\n            h0 += list(g[: len(g) // 2]); h1 += list(g[len(g) // 2:])\n        halves[0].append(np.array(sorted(h0), int)); halves[1].append(np.array(sorted(h1), int))\n    res = {}\n    for h in (0, 1):\n        units, cm, s1s = stage1_units(concepts, bgs, subs=halves[h], n_boot=200, seed=SEED + 7 * s + h)\n        feats = {}\n        if len(units) >= 5:\n            try:\n                fit = pool_all(units, names, {})\n                feats = concept_features(fit, units, names, cm)\n            except (np.linalg.LinAlgError, ValueError) as e:\n                logger.warning(f\"split {s} half {h}: pooling failed {e!r}\")\n        rows = {}\n        for ci, name in enumerate(names):\n            c = concepts[ci]\n            sub = halves[h][ci]\n            n_off = int((c.cH[sub] < 0.5).sum()) if len(sub) else 0\n            bgl, crude = _half_crude(c, *bgs[ci], sub) if len(sub) else (np.nan, np.nan)\n            f = feats.get(name, {})\n            rows[name] = {\"A_h\": f.get(\"A_h\", np.nan) if not f.get(\"A_h_missing\", 1) else np.nan,\n                          \"A_h_u\": f.get(\"A_h_u\", np.nan) if not f.get(\"A_h_missing\", 1) else np.nan,\n                          \"max_rho\": f.get(\"max_rho\", np.nan), \"n_nat_fields\": f.get(\"n_nat_fields\", np.nan),\n                          \"n_off\": n_off, \"bg_LOR\": bgl, \"A_h_crude\": crude,\n                          \"A_h_MH\": s1s[ci].A_h_MH if s1s[ci] is not None else np.nan}\n        field_units = {}\n        if feats:\n            for k, u in enumerate(units):\n                val, _ = predict(fit, u[\"ci\"], u[\"field\"], k)\n                field_units[(names[u[\"ci\"]], u[\"field\"])] = (val, u[\"n_child_j\"])\n        res[h] = {\"rows\": rows, \"field\": field_units}\n    return res\n\n\ndef reliability(results: list[dict], names: list[str]) -> dict:\n    out = {}\n    for feat in (\"A_h\", \"A_h_u\", \"max_rho\", \"n_nat_fields\", \"bg_LOR\", \"A_h_crude\", \"A_h_MH\"):\n        rs = []", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 21:02:16 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cat $W/pyproject.toml; cat $W/reproducibility.md; ls -la $W/results $W/results/* $W/cache | head -60; du -sh $W/results/* $W/cache/*
```

### [12] TOOL RESULT — Bash · 2026-09-29 21:02:28 UTC

```
{"stdout": "[project]\nname = \"naturalisation-gap-screen\"\nversion = \"0.1.0\"\ndescription = \"Screen of the background-adjusted naturalisation gap (candidate L) on the P78 dev panel\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n    \"arro3-core==0.8.3\",\n    \"arviz==1.3.0\",\n    \"arviz-base==1.3.1\",\n    \"arviz-plots==1.3.2\",\n    \"arviz-stats==1.3.3\",\n    \"cachetools==6.2.6\",\n    \"certifi==2026.7.22\",\n    \"charset-normalizer==3.5.1\",\n    \"cloudp... [truncated, 30957 chars total]
```

### [13] TOOL CALL — Bash · 2026-09-29 21:02:32 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; sed -n 300,808p $W/method.py
```

### [14] TOOL RESULT — Bash · 2026-09-29 21:02:32 UTC

```
{"stdout": "        rs = []\n        for r in results:\n            a = np.array([r[0][\"rows\"][n][feat] for n in names], float)\n            b = np.array([r[1][\"rows\"][n][feat] for n in names], float)\n            ok = np.array([min(r[0][\"rows\"][n][\"n_off\"], r[1][\"rows\"][n][\"n_off\"]) >= 10 for n in names])\n            if feat == \"bg_LOR\":\n                ok = np.ones(len(names), bool)\n            rs.append(rho(a[ok], b[ok]))\n        rs = np.array(rs, float)\n... [truncated, 32018 chars total]
```

### [15] TOOL CALL — Bash · 2026-09-29 21:02:32 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cat $W/reproducibility.md; ls $W/results | head; ls $W/results/concepts | head; ls $W/results/concepts | wc -l; du -sh $W/results/* | sort -h | tail; ls $W/cache; ls $W/results/concepts/$(ls $W/results/concepts|head -1)
```

### [16] TOOL RESULT — Bash · 2026-09-29 21:02:32 UTC

````
{"stdout": "# Reproducing the naturalisation-gap screen (candidate L)\n\nThis is what was actually run, in order. All paths are relative to this artifact's folder.\n\n## 1. Get the artifact\nThis workspace is published as one folder, `gen_art_experiment_1`, of the run's public GitHub repository:\n```bash\ngit clone <repository-url>\ncd <repository>/<path-to>/gen_art_experiment_1\n```\nThe raw API response cache (`cache/`, 73 MB of hash-named files) is **not** published. The pe... [truncated, 30987 chars total]
````

### [17] TOOL CALL — Read · 2026-09-29 21:02:36 UTC

```
/var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/tool-results/bg9rozuyu.txt
```

### [18] TOOL RESULT — Read · 2026-09-29 21:02:38 UTC

```
{"type": "text", "file": {"filePath": "/var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/tool-results/bg9rozuyu.txt", "content": "        rs = []\n        for r in results:\n            a = np.array([r[0][\"rows\"][n][feat] for n in names], float)\n            b = np.array([r[1][\"rows\"][n][feat] for n in names], float)\n            ok... [truncated, 35520 chars total]
```

### [19] TOOL CALL — Bash · 2026-09-29 21:02:44 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; sed -n 1,200p /var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/tool-results/bj1c1urib.txt | head -120; ls $W/results | grep -v '^concepts$'; ls $W/results/concepts | wc -l; du -sh $W/results/concepts $W/results/*.json; ls -la $W/results/concepts/* | head -20
```

### [20] TOOL RESULT — Bash · 2026-09-29 21:02:46 UTC

````
{"stdout": "# Reproducing the naturalisation-gap screen (candidate L)\n\nThis is what was actually run, in order. All paths are relative to this artifact's folder.\n\n## 1. Get the artifact\nThis workspace is published as one folder, `gen_art_experiment_1`, of the run's public GitHub repository:\n```bash\ngit clone <repository-url>\ncd <repository>/<path-to>/gen_art_experiment_1\n```\nThe raw API response cache (`cache/`, 73 MB of hash-named files) is **not** published. The per-concept data the analysis actually reads (`results/concepts/<slug>/s2_raw.json.gz` and `bg.json.gz`) and `results/s0_raw.json` **are** published, so step 4 reproduces every reported number exactly without any API call.\n\nNo input from another artifact or from user uploads is used. The artifact pulls its own data.\n\n## 2. System, Python and libraries\n- The run used Ubuntu/Debian Linux in a 4-CPU container with a 29 GB RAM limit and **no GPU**.\n- Python 3.12.14.\n- `uv` 0.x; pip is not used.\n\n```bash\nuv venv .venv --python=3.12\nuv pip install --python .venv/bin/python -r <(python3 -c \"import tomllib;print('\\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))\")\n```\n`pyproject.toml` pins all 63 installed packages to the exact versions used. The main ones:\n- numpy==2.5.3, pandas==3.0.6, scipy==1.18.1, scikit-learn==1.9.1;\n- statsmodels==0.15.0, pymc==6.3.2, nutpie==0.16.11, arviz==1.3.0;\n- loguru==0.7.3, requests==2.34.2, matplotlib==3.11.2, pyarrow==25.0.1, psutil==7.2.2, pytest==9.1.1.\n\n## 3. Environment variables and keys (names only)\n- `OPENALEX_API_KEY` is needed only to re-pull data (steps 5.2 and 5.4). It is never written to logs, cache keys or outputs.\n- Semantic Scholar is used anonymously; no key is needed.\n- No OpenRouter or LLM calls are made ($0).\n- Optional: `OA_OWN_CAP` (default 3500) and `OA_SHARED_FLOOR` (default 1000) are the credit guards in `oa.py`.\n\n## 4. Reproduce the reported numbers from the published data (no network)\n```bash\n.venv/bin/python -m pytest -q -c pytest.ini tests/          # T0 unit tests, 6 pass, ~1 min\n.venv/bin/python method.py --splits 50 --n-boot 2000         # full screen, ~4-5 min on 4 CPUs\n.venv/bin/python audit/rederive.py                           # independent re-derivation, ~1 min\n```\nTo regenerate the method output variants, use the aii-json skill's formatter, or copy `method_out.json` to `full_method_out.json` and take the first 3 examples per dataset for the mini version:\n```bash\npython <aii-json-skill>/scripts/aii_json_format_mini_preview.py --input method_out.json\n```\n\nSeeds:\n- The panel order uses `random.Random(20260928)`.\n- Bootstraps, split halves, child sampling and parent thinning use 20260928 or seeds derived from it (e.g. SHA-1 of the child id XOR 20260928).\n- The PyMC seed is 20260928 (4 chains x 1,000 draws, nutpie).\n\nThe re-runs were deterministic: two full runs gave identical statistics. The PyMC R-hat varies in the third decimal.\n\n## 5. How the data were pulled (only needed to rebuild `results/concepts/` from scratch; counts drift daily)\n1. **Unit tests** (as above).\n2. **OpenAlex S0 pulls**, 139 credits in total. `panel.seeded_order()` gives the 78-concept order, and `s0.fetch_s0(Client(), order)` writes `results/s0_raw.json`:\n   ```python\n   import json; from oa import Client; from panel import seeded_order; from s0 import fetch_s0\n   order = seeded_order(); open('results/panel_order.json','w').write(json.dumps(order, indent=1))\n   open('results/s0_raw.json','w').write(json.dumps(fetch_s0(Client(), order)))\n   ```\n   On 2026-09-28 the shared daily pool dropped below the 1,000-credit sibling floor during this step. Yearly counts exist for all 78 concepts; OpenAlex topic-field windows exist for 11 dev concepts.\n3. **Semantic Scholar pull**: `python fetch_s2.py`, about 70 min with anonymous rate limits. For each of the 53 dev-eligible concepts it writes `results/concepts/<slug>/s2_raw.json.gz`, containing:\n   - all phrase-matched papers of t0-3..t0+4, up to 25,000;\n   - a late-window t0+6..t0+8 field sample, capped at 3,000 in paperId-hash order;\n   - citation lists for a seeded sample of at most 1,500 parents.\n4. **Background references**: `OPENALEX_API_KEY=... python fetch_bg.py`, about 60 min, 0 credits. It uses free OpenAlex singleton GETs for children's reference lists and S2 MAG-id lookups for their fields, and writes `results/concepts/<slug>/bg.json.gz`.\n5. **Analysis**: `python method.py --splits 50 --n-boot 2000`.\n\nThe per-call ledger of every OpenAlex response and its credits is in `logs/credits.csv`: 139 credits over 12,023 responses, most of them free singletons.\n\n## 6. Expected outputs and numbers\n`results/screen_result.json` (key: value):\n- `n_used`: 48 dev concepts.\n- `delta_rho`: **-0.0056**; `ci90`: [-0.034, 0.017]; `rho_B`: 0.834; `rho_BC`: 0.828.\n- `n_pos_groups`: 0.\n- `reliability.A_h.reliability_SB`: **0.58**.\n- `size_corr`: vol 0.145, growth -0.177.\n- `delta_auc_O1.delta`: -0.026.\n- `field_level.delta`: +0.002, ci90 [-0.011, 0.016], 367 units.\n- `M1.R2`: 0.659.\n- `pymc_check.pass`: true (Spearman with REML 0.9996).\n- `survives`: **false**. The clause results are in `clause_results`.\n\nOther outputs:\n- `results/features.csv`, `field_features.csv`, `outcomes.csv`, `field_outcomes.csv`, `dropped.csv`, and `screen_table.csv` (with OOF predictions).\n- `results/figures/screen_overview.png`, with three panels: A*_h vs O2r, the M1 scatter, and reliability vs n.\n- `method_out.json` and its `full_`, `mini_` and `preview_` variants, in the exp_gen_sol_out schema.\n- `audit/rederive_out.json`: independently recomputed values, a shuffled-A*_h placebo (0% passing) and a positive-control power ladder.\n\nIn the paper these numbers belong to the RQ1 screening section, as the \"naturalisation gap\" candidate: the concept-level Delta-rho table, the field-level retention test and the reliability-vs-n curve.\nconcepts\ndropped.csv\nfeatures.csv\nfield_features.csv\nfield_outcomes.csv\nfigures\noutcomes.csv\noutcomes_openalex_s0.csv\npanel_order.json\ns0_raw.json\ncancer_stem_cell\ncarbon_capture_and_storage\nchip_seq\ncloud_computing\ncognitive_radio\ncomparative_effectiveness_research\ncompressed_sensing\ncopy_number_variation\ncrowdsourcing\ncyber_physical_system\n53\n9.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/panel_order.json\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/outcomes.csv\n20K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/features.csv\n30K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/screen_result.json\n34K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/screen_table.csv\n48K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/field_features.csv\n53K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/field_outcomes.csv\n73K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/s0_raw.json\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/figures\ndropped.csv\nfeatures.csv\nfield_features.csv\nfield_outcomes.csv\nfigures\noutcomes.csv\noutcomes_openalex_s0.csv\npanel_order.json\ns0_raw.json\nscreen_result.json\nscreen_table.csv\n53\n126M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/concepts\n9.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/panel_order.json\n73K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/s0_raw.json\n30K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/screen_result.json\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/concepts/cancer_stem_cell:\ntotal 3764\ndrwxrwxrwx  2 aii-agent aii-agent 1075418 Sep 28 12:52 .\ndrwxrwxrwx 55 aii-agent aii-agent 2005258 Sep 28 13:49 ..\n-rw-rw-rw-  1 aii-agent aii-agent   14121 Sep 28 12:52 bg.json.gz\n-rw-rw-rw-  1 aii-agent aii-agent  758164 Sep 28 12:46 s2_raw.json.gz\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/concepts/carbon_capture_and_storage:\ntotal 3882\ndrwxrwxrwx  2 aii-agent aii-agent 1086126 Sep 28 13:25 .\ndrwxrwxrwx 55 aii-agent aii-agent 2005258 Sep 28 13:49 ..\n-rw-rw-rw-  1 aii-agent aii-agent   18679 Sep 28 13:25 bg.json.gz\n-rw-rw-rw-  1 aii-agent aii-agent  863254 Sep 28 13:25 s2_raw.json.gz\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/results/concepts/chip_seq:\ntotal 5052\ndrwxrwxrwx  2 aii-agent aii-agent 2000111 Sep 28 13:47 .\ndrwxrwxrwx 55 aii-agent aii-agent 2005258 Sep 28 13:49 ..\n-rw-rw-rw-  1 aii-agent aii-agent   17548 Sep 28 13:47 bg.json.gz\n-rw-rw-rw-  1 aii-agent aii-agent 1149305 Sep 28 13:46 s2_raw.json.gz", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [21] ASSISTANT · 2026-09-29 21:02:52 UTC

```
Reading the helper modules (lineage, pool, s0, screen, panel) that method.py imports, to decide how to package data.
```

### [22] TOOL CALL — Bash · 2026-09-29 21:02:52 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cat $W/lineage.py $W/panel.py
```

### [23] TOOL RESULT — Bash · 2026-09-29 21:02:52 UTC

```
{"stdout": "\"\"\"Concept lineage network, S2-based S0 field distributions, stage-1 field-stratified MH contrasts and foils.\n\nLabels: each paper carries a FRACTIONAL field-membership vector over the Semantic Scholar fields of study\n(s2-fos-model categories, a title/abstract text classifier, uniform over the predicted categories; the MAG\n'external' categories are used only when the model has none). Text-based labels do not encode the paper's own\nreferences, so they are not circular for citation-flow contrasts (the concern that ruled out OpenAlex topics).\n\"\"\"\nfrom __future__ import annotations\n\nimport gzip\nimport hashlib\nimport json\nimport math\nimport warnings\nfrom dataclasses import dataclass, field\nfrom pathlib import Path\n\nimport numpy as np\n\nROOT = Path(__file__).resolve().parent\nS2_FIELDS = [\"Computer Science\", \"Engineering\", \"Biology\", \"Medicine\", \"Chemistry\", \"Materials Science\", \"Physics\",\n             \"Mathematics\", \"Environmental Science\", \"Agricultural and Food Sciences\", \"Geology\", \"Geography\",\n             \"Psychology\", \"Sociology\", \"Economics\", \"Business\", \"Political Science\", \"Education\", \"Law\",\n             \"Linguistics\", \"Philosophy\", \"History\", \"Art\"]\nFIDX = {f: i for i, f in enumerate(S2_FIELDS)}\nF = len(S2_FIELDS)\nS2_DEV = {\"Computer Science\": \"Computer Science\", \"Engineering\": \"Engineering\",\n          \"Biology\": \"Biochemistry, Genetics and Molecular Biology\", \"Medicine\": \"Medicine\"}\nSEED = 20260928\n\n\ndef membership(fos: list[dict] | None) -> np.ndarray | None:\n    fos = fos or []\n    cats = sorted({f[\"category\"] for f in fos if f.get(\"source\") == \"s2-fos-model\" and f[\"category\"] in FIDX})\n    if not cats:\n        cats = sorted({f[\"category\"] for f in fos if f[\"category\"] in FIDX})\n    if not cats:\n        return None\n    v = np.zeros(F)\n    for c in cats:\n        v[FIDX[c]] = 1.0 / len(cats)\n    return v\n\n\ndef stable_seed(s: str) -> int:\n    return int(hashlib.sha1(s.encode()).hexdigest()[:12], 16) ^ SEED\n\n\ndef home_set(mass: np.ndarray) -> list[int]:\n    tot = mass.sum()\n    if tot <= 0:\n        return []\n    h = [i for i in range(F) if mass[i] / tot >= 0.40]\n    return h or [int(np.argmax(mass))]\n\n\n@dataclass\nclass Concept:\n    name: str\n    t0: int\n    ids: list[str]\n    year: np.ndarray\n    M: np.ndarray                       # (n, F) membership (rows of unlabelled papers are all zero)\n    labelled: np.ndarray                # (n,) bool\n    authors: list[set]\n    mag: list[str | None]\n    doi: list[str | None]\n    gstatus: list[str]\n    H: list[int]\n    hmask: np.ndarray\n    late_mass: np.ndarray\n    thin_early: float\n    thin_late: float\n    exact_share: float\n    # lineage\n    child_idx: np.ndarray = field(default_factory=lambda: np.zeros(0, int))\n    P: np.ndarray = field(default_factory=lambda: np.zeros((0, F)))       # mean CROSS-parent membership per child\n    n_cross: np.ndarray = field(default_factory=lambda: np.zeros(0))\n    n_self: np.ndarray = field(default_factory=lambda: np.zeros(0))\n    has_any_parent: np.ndarray = field(default_factory=lambda: np.zeros(0, bool))\n    links: list = field(default_factory=list)                              # (child, parent, self)\n    indeg_before: dict = field(default_factory=dict)\n\n    @property\n    def C(self) -> np.ndarray:\n        return self.M[self.child_idx]\n\n    @property\n    def cH(self) -> np.ndarray:\n        return self.C @ self.hmask\n\n    @property\n    def child_year(self) -> np.ndarray:\n        return self.year[self.child_idx]\n\n\ndef load_concept(raw: dict) -> Concept:\n    t0 = raw[\"t0\"]\n    E = [p for p in raw[\"early\"] if p.get(\"year\") and p[\"gstatus\"] != \"rejected\"]\n    ids = [p[\"paperId\"] for p in E]\n    year = np.array([p[\"year\"] for p in E])\n    mem = [membership(p.get(\"s2FieldsOfStudy\")) for p in E]\n    labelled = np.array([m is not None for m in mem])\n    M = np.array([m if m is not None else np.zeros(F) for m in mem]).reshape(len(E), F)\n    authors = [{a[\"authorId\"] for a in p.get(\"authors\") or [] if a.get(\"authorId\")} for p in E]\n    ext = [p.get(\"externalIds\") or {} for p in E]\n    early_mask = (year >= t0) & (year <= t0 + 1)\n    H = home_set(M[early_mask].sum(0))\n    hmask = np.zeros(F)\n    hmask[H] = 1.0\n    late = np.zeros(F)\n    for p in raw[\"late\"]:\n        m = membership(p.get(\"s2FieldsOfStudy\"))\n        if m is not None:\n            late += m\n    n_ver = sum(p[\"gstatus\"] != \"unverifiable\" for p in raw[\"early\"])\n    n_conf = sum(p[\"gstatus\"] == \"confirmed\" for p in raw[\"early\"])\n    c = Concept(name=raw[\"concept\"], t0=t0, ids=ids, year=year, M=M, labelled=labelled, authors=authors,\n                mag=[e.get(\"MAG\") for e in ext], doi=[e.get(\"DOI\") for e in ext],\n                gstatus=[p[\"gstatus\"] for p in E], H=H, hmask=hmask, late_mass=late,\n                thin_early=(raw.get(\"total_early\") or len(raw[\"early\"])) / max(len(raw[\"early\"]), 1),\n                thin_late=(raw.get(\"total_late\") or len(raw[\"late\"])) / max(len(raw[\"late\"]), 1),\n                exact_share=n_conf / n_ver if n_ver else float(\"nan\"))\n    build_lineage(c, raw[\"citations\"])\n    return c\n\n\ndef build_lineage(c: Concept, citations: dict[str, list[str]]) -> None:\n    pos = {pid: i for i, pid in enumerate(c.ids)}\n    cross: dict[int, list[int]] = {}\n    selfp: dict[int, list[int]] = {}\n    indeg: dict[int, dict[int, int]] = {}\n    for q_id, citing in citations.items():\n        q = pos.get(q_id)\n        if q is None or not c.labelled[q]:\n            continue\n        for p_id in citing:\n            p = pos.get(p_id)\n            if p is None or not c.labelled[p]:\n                continue\n            tp, tq = c.year[p], c.year[q]\n            if tp > tq:\n                for yy in range(tp + 1, c.t0 + 6):   # in-citations received strictly before year yy\n                    indeg.setdefault(q, {}).setdefault(yy, 0)\n                    indeg[q][yy] += 1\n            if not (c.t0 <= tp <= c.t0 + 4 and 1 <= tp - tq <= 3):\n                continue\n            is_self = bool(c.authors[p] & c.authors[q])\n            c.links.append((p, q, is_self))\n            (selfp if is_self else cross).setdefault(p, []).append(q)\n    anyp = sorted(set(cross) | set(selfp))\n    kids = sorted(cross)\n    c.child_idx = np.array(kids, int)\n    c.P = np.array([c.M[cross[k]].mean(0) for k in kids]).reshape(len(kids), F)\n    c.n_cross = np.array([len(cross[k]) for k in kids], float)\n    c.n_self = np.array([len(selfp.get(k, [])) for k in kids], float)\n    c.has_any_parent = np.zeros(len(c.ids), bool)\n    c.has_any_parent[anyp] = True\n    c._selfp, c._cross = selfp, cross\n    c.indeg_before = indeg\n\n\n# ---------------------------------------------------------------- stage-1 tables\nT_STRATA = 5\n\n\ndef contribs(Cm: np.ndarray, Pm: np.ndarray, hmask: np.ndarray) -> np.ndarray:\n    \"\"\"Per-child contributions (4, n, F) to the cells a, b, c', d of every field-j table.\n    Rows: child in j vs child in H; columns: parent in j vs parent in H; third-field parent mass is excluded and each\n    child's retained parent mass renormalised to 1 (children with no retained mass contribute nothing).\"\"\"\n    cH = Cm @ hmask\n    pH = Pm @ hmask\n    ret = Pm + pH[:, None]\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        pj = np.where(ret > 0, Pm / ret, 0.0)\n        ph = np.where(ret > 0, pH[:, None] / ret, 0.0)\n    return np.stack([Cm * pj, Cm * ph, cH[:, None] * pj, cH[:, None] * ph])\n\n\ndef onehot_years(years: np.ndarray, t0: int) -> np.ndarray:\n    return np.eye(T_STRATA)[np.clip(years - t0, 0, T_STRATA - 1)]          # (n, T)\n\n\ndef tables_w(con: np.ndarray, oh: np.ndarray, W: np.ndarray) -> np.ndarray:\n    \"\"\"Weighted year-stratified tables for a batch of child weight vectors W (B, n) -> (4, B, T, F).\"\"\"\n    return np.einsum(\"bn,nt,knf->kbtf\", W, oh, con, optimize=True)\n\n\ndef tables(Cm: np.ndarray, Pm: np.ndarray, years: np.ndarray, hmask: np.ndarray, t0: int) -> np.ndarray:\n    \"\"\"Year-stratified 2x2 tables for every field j at once. Returns (4, T, F): a, b, c', d.\"\"\"\n    if len(Cm) == 0:\n        return np.zeros((4, T_STRATA, F))\n    return tables_w(contribs(Cm, Pm, hmask), onehot_years(years, t0), np.ones((1, len(Cm))))[:, 0]\n\n\ndef mh_lor(tab: np.ndarray) -> np.ndarray:\n    \"\"\"Mantel-Haenszel pooled log-OR over the strata axis (-2). tab (4, ..., T, F) -> (..., F). Strata with an empty\n    row/column margin are skipped; strata with any zero cell get +0.5 in every cell (Haldane).\"\"\"\n    a, b, c, d = tab[0], tab[1], tab[2], tab[3]\n    valid = ((a + b) > 0) & ((c + d) > 0) & ((a + c) > 0) & ((b + d) > 0)\n    corr = 0.5 * (valid & ((a == 0) | (b == 0) | (c == 0) | (d == 0)))\n    a, b, c, d = a + corr, b + corr, c + corr, d + corr\n    n = a + b + c + d\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        num = np.where(valid, a * d / n, 0).sum(-2)\n        den = np.where(valid, b * c / n, 0).sum(-2)\n        return np.where((num > 0) & (den > 0), np.log(num / den), np.nan)\n\n\ndef mh_lor_pooled(tab: np.ndarray, cols: np.ndarray) -> float:\n    \"\"\"MH over all (j, t) strata jointly for the given field columns -> one concept-level log-OR.\"\"\"\n    sub = tab[:, :, cols].reshape(4, -1, 1)\n    return float(mh_lor(sub)[0])\n\n\n@dataclass\nclass Stage1:\n    rho_hat: np.ndarray          # (F,) concept minus background MH log-OR, NaN where undefined\n    lor_c: np.ndarray\n    lor_bg: np.ndarray\n    v: np.ndarray                # bootstrap variance\n    n_child_j: np.ndarray        # linked child mass in j\n    A_h_MH: float\n    A_h_MH_c: float\n    A_h_MH_bg: float\n\n\ndef stage1(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray, sub: np.ndarray | None = None,\n           n_boot: int = 200, seed: int = SEED) -> Stage1:\n    \"\"\"bgB: (n_children, F) mean background-reference membership per child (zero rows where no background, which\n    therefore contribute nothing to the background tables); sub: optional child subset (split-half).\n    Bootstrap = multinomial child weights (resampling children with replacement; each child's concept links and\n    background references move together, so the covariance between the two terms is kept).\"\"\"\n    idx = np.arange(len(c.child_idx)) if sub is None else sub\n    Cm, Pm, yrs = c.C[idx], c.P[idx], c.child_year[idx]\n    Bm = np.where(bg_rows[idx][:, None], bgB[idx], 0.0)\n    off = np.ones(F, bool)\n    off[c.H] = False\n    n = len(idx)\n    conc, conb = contribs(Cm, Pm, c.hmask), contribs(Cm, Bm, c.hmask)\n    oh = onehot_years(yrs, c.t0)\n    tc = tables_w(conc, oh, np.ones((1, n)))[:, 0]\n    tb = tables_w(conb, oh, np.ones((1, n)))[:, 0]\n    lc, lb = mh_lor(tc), mh_lor(tb)\n    rho = lc - lb\n    rho[~off] = np.nan\n    nj = Cm.sum(0)\n    rho[nj <= 0] = np.nan\n    rng = np.random.default_rng(seed)\n    boots = np.full((n_boot, F), np.nan)\n    for s0 in range(0, n_boot, 100):\n        B = min(100, n_boot - s0)\n        W = np.stack([np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(B)]).astype(float)\n        boots[s0:s0 + B] = mh_lor(tables_w(conc, oh, W)) - mh_lor(tables_w(conb, oh, W))\n    ok = np.isfinite(boots).mean(0) >= 0.5\n    with warnings.catch_warnings():  # all-NaN / single-value columns are expected for fields without data\n        warnings.simplefilter(\"ignore\", RuntimeWarning)\n        v = np.nanvar(boots, axis=0, ddof=1) if n_boot > 1 else np.full(F, np.nan)\n    rho[~ok] = np.nan\n    v = np.where(np.isfinite(rho), np.maximum(v, 1e-3), np.nan)\n    cols = np.where(off & (nj > 0))[0]\n    amc = mh_lor_pooled(tc, cols) if len(cols) else float(\"nan\")\n    amb = mh_lor_pooled(tb, cols) if len(cols) else float(\"nan\")\n    return Stage1(rho_hat=rho, lor_c=lc, lor_bg=lb, v=v, n_child_j=nj, A_h_MH=amc - amb, A_h_MH_c=amc, A_h_MH_bg=amb)\n\n\n# ---------------------------------------------------------------- foils\ndef crude_lor(child_off: np.ndarray, par_off: np.ndarray) -> float:\n    \"\"\"Unstratified 2x2 (child off-home vs home) x (parent off-home vs home) with Haldane 0.5 (probe definition).\"\"\"\n    a = (child_off * par_off).sum() + .5\n    b = (child_off * (1 - par_off)).sum() + .5\n    cc = ((1 - child_off) * par_off).sum() + .5\n    d = ((1 - child_off) * (1 - par_off)).sum() + .5\n    return math.log(a * d / (b * cc))\n\n\ndef logit_s(p: float, n: float) -> float:\n    return math.log((p * n + 0.5) / ((1 - p) * n + 0.5))\n\n\ndef foils(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray) -> dict:\n    out: dict = {}\n    if len(c.child_idx) == 0:\n        return {k: float(\"nan\") for k in (\"raw_LOR\", \"bg_LOR\", \"A_h_crude\", \"A_unif\", \"A_imp\", \"relay_share\",\n                                          \"R_away\", \"raw_LOR_sampled\")} | {\n            \"self_share\": _self_share(c), \"coverage\": _coverage(c)}\n    Cm, Pm, cH = c.C, c.P, c.cH\n    tot = Pm.sum(1)\n    pH = Pm @ c.hmask\n    par_off = np.where(tot > 0, 1 - pH / np.where(tot > 0, tot, 1), 0)\n    out[\"raw_LOR\"] = crude_lor(1 - cH, par_off)\n    br = bg_rows\n    if br.any():\n        bt = bgB[br].sum(1)\n        b_off = np.where(bt > 0, 1 - (bgB[br] @ c.hmask) / np.where(bt > 0, bt, 1), 0)\n        out[\"bg_LOR\"] = crude_lor(1 - cH[br], b_off)\n        out[\"raw_LOR_sampled\"] = crude_lor(1 - cH[br], par_off[br])\n        out[\"A_h_crude\"] = out[\"raw_LOR_sampled\"] - out[\"bg_LOR\"]\n    else:\n        out[\"bg_LOR\"] = out[\"raw_LOR_sampled\"] = out[\"A_h_crude\"] = float(\"nan\")\n    # relay share: off-home child mass whose parents sit in third fields\n    offc = Cm * (1 - c.hmask)\n    third = 1 - Pm - pH[:, None]\n    third = np.clip(third, 0, 1)\n    den = offc.sum()\n    out[\"relay_share\"] = float((offc * third).sum() / den) if den > 0 else float(\"nan\")\n    out[\"self_share\"] = _self_share(c)\n    out[\"coverage\"] = _coverage(c)\n    # A_unif / A_imp (probe definitions, fractional): off-home children's share of off-home parents vs stock\n    w_off = 1 - cH\n    A = (w_off * par_off).sum() / w_off.sum() if w_off.sum() > 0 else float(\"nan\")\n    e_u = e_i = 0.0\n    wsum = 0.0\n    lab = np.where(c.labelled)[0]\n    for k, ci in enumerate(c.child_idx):\n        if w_off[k] <= 0:\n            continue\n        y = c.year[ci]\n        stock = lab[(c.year[lab] >= y - 3) & (c.year[lab] < y)]\n        if len(stock) == 0:\n            continue\n        so = 1 - c.M[stock] @ c.hmask\n        wi = np.array([1 + c.indeg_before.get(int(q), {}).get(int(y), 0) for q in stock], float)\n        e_u += w_off[k] * so.mean()\n        e_i += w_off[k] * (so * wi).sum() / wi.sum()\n        wsum += w_off[k]\n    if wsum > 0 and np.isfinite(A):\n        out[\"A_unif\"] = logit_s(A, wsum) - logit_s(e_u / wsum, wsum)\n        out[\"A_imp\"] = logit_s(A, wsum) - logit_s(e_i / wsum, wsum)\n    else:\n        out[\"A_unif\"] = out[\"A_imp\"] = float(\"nan\")\n    out[\"R_away\"] = r_away(c)\n    return out\n\n\ndef _self_share(c: Concept) -> float:\n    tot = {}\n    for p, q, s in c.links:\n        tot.setdefault(p, [0, 0])\n        tot[p][0] += s\n        tot[p][1] += 1\n    if not tot:\n        return float(\"nan\")\n    return float(np.mean([a / b for a, b in tot.values()]))\n\n\ndef _coverage(c: Concept) -> float:\n    m = c.labelled & (c.year >= c.t0) & (c.year <= c.t0 + 4)\n    return float(c.has_any_parent[m].mean()) if m.any() else float(\"nan\")\n\n\ndef r_away(c: Concept) -> float:\n    \"\"\"Spectral radius of K[a,b] = cross-link mass child-field a -> parent-field b / stock mass of b in parent\n    years, restricted to off-home fields with >= 5 papers of stock.\"\"\"\n    K = c.C.T @ c.P                                     # (F, F) child field x parent field link mass\n    stock = c.M[(c.year >= c.t0 - 3) & (c.year <= c.t0 + 3)].sum(0)\n    keep = [i for i in range(F) if i not in c.H and stock[i] >= 5]\n    if not keep:\n        return float(\"nan\")\n    Ks = K[np.ix_(keep, keep)] / stock[keep][None, :]\n    return float(np.max(np.abs(np.linalg.eigvals(Ks))))\n\n\ndef load_raw(slug_: str) -> dict:\n    return json.loads(gzip.decompress((ROOT / \"results\" / \"concepts\" / slug_ / \"s2_raw.json.gz\").read_bytes()))\n\"\"\"Frozen screen panel P78 (identical in every screen artifact) and the seeded processing order.\"\"\"\nfrom __future__ import annotations\n\nimport random\n\nGROUPS = {\n    \"CS/AI\": \"extreme learning machine; compressed sensing/compressive sensing; crowdsourcing; cloud computing; deep belief network; dictionary learning; folksonomy; social tagging; Web 2.0; mashup; service-oriented architecture; MapReduce; NoSQL; cognitive radio; network coding; vehicular ad hoc network/VANET; wireless body area network; internet of things; cyber-physical system; sentiment analysis; latent Dirichlet allocation; differential privacy; learning to rank; microblog\",\n    \"Engineering\": \"smart grid; microgrid; vehicle-to-grid; plug-in hybrid electric vehicle; energy harvesting; microbial fuel cell; carbon capture and storage; WiMAX; ZigBee; LTE-Advanced; virtual power plant; piezoelectric nanogenerator; memristor; ultra-wideband; demand response; structural health monitoring\",\n    \"Biochem/Genetics\": \"induced pluripotent stem cell; optogenetics; ChIP-seq; RNA-seq; next-generation sequencing; copy number variation; genome-wide association study/GWAS; exome sequencing; long noncoding RNA/lncRNA; piRNA; synthetic biology; metagenomics; human microbiome; cancer stem cell; zinc finger nuclease; lipidomics; interactome; DNA barcoding; sirtuin; nanopore sequencing\",\n    \"Medicine\": \"severe acute respiratory syndrome/SARS coronavirus; H5N1; pandemic H1N1/swine flu; transcatheter aortic valve implantation/TAVI; natural orifice transluminal endoscopic surgery/NOTES; single-incision laparoscopic surgery; drug-eluting stent; cardiac resynchronization therapy; HPV vaccine; biosimilar; pay for performance; comparative effectiveness research; patient-centered medical home; ribotype 027; chronic traumatic encephalopathy; mHealth; capsule endoscopy; takotsubo cardiomyopathy\",\n}\n\n# aliases that are common English words when lower-cased: never sent to the (case-insensitive) search filter\nNOT_SEARCHED = {\"NOTES\"}\nACRONYMS = {\"GWAS\", \"VANET\", \"lncRNA\", \"TAVI\", \"SARS coronavirus\", \"NOTES\"}\nSEED = 20260928\nDEV_FIELDS = [\"Computer Science\", \"Engineering\", \"Biochemistry, Genetics and Molecular Biology\", \"Medicine\"]\n\n\ndef panel() -> list[dict]:\n    out = []\n    for g, s in GROUPS.items():\n        for item in s.split(\";\"):\n            names = [x.strip() for x in item.split(\"/\")]\n            out.append({\"canonical\": names[0], \"aliases\": names, \"panel_group\": g})\n    assert len(out) == 78, len(out)\n    return out\n\n\ndef seeded_order() -> list[dict]:\n    order = panel()[:]\n    random.Random(SEED).shuffle(order)\n    return order\n\n\ndef slug(name: str) -> str:\n    return \"\".join(ch if ch.isalnum() else \"_\" for ch in name.lower()).strip(\"_\")\n\n\ndef search_filter(c: dict) -> str:\n    phrases = [a for a in c[\"aliases\"] if a not in NOT_SEARCHED]\n    return \"title_and_abstract.search:\" + \"|\".join(f'\"{p}\"' for p in phrases)\n\n\nBASE_FILTER = \"type:article|review,is_paratext:false\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-29 21:02:52 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cat $W/pool.py $W/s0.py $W/screen.py
```

### [25] TOOL RESULT — Bash · 2026-09-29 21:02:52 UTC

```
{"stdout": "\"\"\"Stage 2: partial pooling of the concept x field contrasts rho_hat_cj.\n\nModel: y_k = x_k beta + u_c(k) + w_k + e_k, u ~ N(0, tau_c^2), w ~ N(0, tau_cj^2), e ~ N(0, v_k) (v_k known from the\nstage-1 child bootstrap). Engine: REML over (log tau_c, log tau_cj) (L-BFGS-B, 3 starts), then Henderson's\nmixed-model equations for beta, BLUPs and the full prediction-error covariance. Fallback (F4): DerSimonian-Laird\none-level empirical Bayes. Headline check: the same model in PyMC (non-centred, NUTS).\n\"\"\"\nfrom __future__ import annotations\n\nfrom dataclasses import dataclass\n\nimport numpy as np\nfrom loguru import logger\nfrom scipy.optimize import minimize\n\n\n@dataclass\nclass PoolFit:\n    beta: np.ndarray\n    tau_c: float\n    tau_cj: float\n    u: np.ndarray            # (n_concepts,)\n    w: np.ndarray            # (K,)\n    Cinv: np.ndarray         # PEV of [beta, u, w]\n    X: np.ndarray\n    fields_x: list[str]      # column meaning of X (intercept + dummies)\n    engine: str\n    converged: bool\n\n\ndef design(field_of_k: list[str], min_cells: int = 5) -> tuple[np.ndarray, list[str]]:\n    vals, cnt = np.unique(field_of_k, return_counts=True)\n    keep = [v for v, n in zip(vals, cnt) if n >= min_cells]\n    if len(keep) == len(vals) and keep:  # every field frequent: the most common one becomes the reference\n        keep.remove(vals[np.argmax(cnt)])\n    cols = [\"intercept\"] + keep\n    X = np.zeros((len(field_of_k), len(cols)))\n    X[:, 0] = 1\n    for k, f in enumerate(field_of_k):\n        if f in keep:\n            X[k, cols.index(f)] = 1\n    return X, cols\n\n\ndef x_row(field: str, cols: list[str]) -> np.ndarray:\n    x = np.zeros(len(cols))\n    x[0] = 1\n    if field in cols[1:]:\n        x[cols.index(field)] = 1\n    return x\n\n\ndef _reml_nll(theta: np.ndarray, y: np.ndarray, X: np.ndarray, Zc: np.ndarray, v: np.ndarray) -> float:\n    tc2, tcj2 = np.exp(2 * theta)\n    S = tc2 * Zc @ Zc.T + np.diag(tcj2 + v)\n    try:\n        L = np.linalg.cholesky(S)\n    except np.linalg.LinAlgError:\n        return 1e10\n    Si = np.linalg.inv(S)\n    XtSiX = X.T @ Si @ X\n    sgn, ld2 = np.linalg.slogdet(XtSiX)\n    if sgn <= 0:\n        return 1e10\n    P = Si - Si @ X @ np.linalg.solve(XtSiX, X.T @ Si)\n    return 0.5 * (2 * np.log(np.diag(L)).sum() + ld2 + y @ P @ y)\n\n\ndef mme(y: np.ndarray, X: np.ndarray, Zc: np.ndarray, v: np.ndarray, tc2: float, tcj2: float):\n    K, p = X.shape\n    nc = Zc.shape[1]\n    Z = np.hstack([Zc, np.eye(K)])\n    Ri = np.diag(1.0 / v)\n    Gi = np.diag(np.r_[np.full(nc, 1 / max(tc2, 1e-6)), np.full(K, 1 / max(tcj2, 1e-6))])\n    C = np.block([[X.T @ Ri @ X, X.T @ Ri @ Z], [Z.T @ Ri @ X, Z.T @ Ri @ Z + Gi]])\n    rhs = np.r_[X.T @ Ri @ y, Z.T @ Ri @ y]\n    Cinv = np.linalg.pinv(C)\n    sol = Cinv @ rhs\n    return sol[:p], sol[p:p + nc], sol[p + nc:], Cinv\n\n\ndef fit_reml(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str]) -> PoolFit:\n    X, cols = design(fields)\n    Zc = np.zeros((len(y), n_concepts))\n    Zc[np.arange(len(y)), cidx] = 1\n    best = None\n    for start in ([np.log(0.3), np.log(0.3)], [np.log(1.0), np.log(0.1)], [np.log(0.1), np.log(1.0)]):\n        r = minimize(_reml_nll, np.array(start), args=(y, X, Zc, v), method=\"L-BFGS-B\",\n                     bounds=[(np.log(1e-3), np.log(10))] * 2)\n        if best is None or r.fun < best.fun:\n            best = r\n    tc, tcj = np.exp(best.x)\n    boundary = min(tc, tcj) <= 1.01e-3\n    if not best.success:\n        logger.warning(f\"REML not converged: {best.message}; using DerSimonian-Laird fallback\")\n        return fit_dl(y, v, cidx, n_concepts, fields)\n    beta, u, w, Cinv = mme(y, X, Zc, v, tc ** 2, tcj ** 2)\n    logger.info(f\"REML: tau_c={tc:.3f} tau_cj={tcj:.3f} beta={np.round(beta, 3)} boundary={boundary}\")\n    return PoolFit(beta=beta, tau_c=float(tc), tau_cj=float(tcj), u=u, w=w, Cinv=Cinv, X=X, fields_x=cols,\n                   engine=\"REML\" + (\"(tau at boundary)\" if boundary else \"\"), converged=True)\n\n\ndef fit_dl(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str]) -> PoolFit:\n    \"\"\"F4 fallback: DerSimonian-Laird tau_c^2 (tau_cj^2 = 0) and one-level empirical-Bayes shrinkage.\"\"\"\n    X, cols = design(fields)\n    w0 = 1 / v\n    mu = (w0 * y).sum() / w0.sum()\n    Q = (w0 * (y - mu) ** 2).sum()\n    tau2 = max(0.0, (Q - (len(y) - 1)) / (w0.sum() - (w0 ** 2).sum() / w0.sum()))\n    Zc = np.zeros((len(y), n_concepts))\n    Zc[np.arange(len(y)), cidx] = 1\n    beta, u, w, Cinv = mme(y, X, Zc, v, max(tau2, 1e-6), 1e-6)\n    return PoolFit(beta=beta, tau_c=float(np.sqrt(tau2)), tau_cj=0.0, u=u, w=w, Cinv=Cinv, X=X, fields_x=cols,\n                   engine=\"DerSimonian-Laird\", converged=True)\n\n\ndef predict(fit: PoolFit, concept: int, field: str, k: int | None) -> tuple[float, np.ndarray]:\n    \"\"\"rho*_cj point prediction and its l-vector over [beta, u, w] (w part only when the unit has data).\"\"\"\n    p = len(fit.beta)\n    nc = len(fit.u)\n    K = len(fit.w)\n    l = np.zeros(p + nc + K)\n    l[:p] = x_row(field, fit.fields_x)\n    l[p + concept] = 1\n    if k is not None:\n        l[p + nc + k] = 1\n    val = l[:p] @ fit.beta + fit.u[concept] + (fit.w[k] if k is not None else 0.0)\n    return float(val), l\n\n\ndef var_of(fit: PoolFit, l: np.ndarray, extra: float = 0.0) -> float:\n    return float(l @ fit.Cinv @ l + extra)\n\n\ndef fit_pymc(y: np.ndarray, v: np.ndarray, cidx: np.ndarray, n_concepts: int, fields: list[str],\n             draws: int = 1000, chains: int = 4, seed: int = 20260928):\n    \"\"\"Headline check: same crossed random-effects model, non-centred, NUTS. Returns (idata, X, cols).\"\"\"\n    import pymc as pm\n    X, cols = design(fields)\n    with pm.Model() as m:\n        beta = pm.Normal(\"beta\", 0, 2, shape=X.shape[1])\n        tau_c = pm.HalfNormal(\"tau_c\", 1)\n        tau_cj = pm.HalfNormal(\"tau_cj\", 1)\n        zc = pm.Normal(\"zc\", 0, 1, shape=n_concepts)\n        zk = pm.Normal(\"zk\", 0, 1, shape=len(y))\n        u = pm.Deterministic(\"u\", tau_c * zc)\n        w = pm.Deterministic(\"w\", tau_cj * zk)\n        mu = pm.math.dot(X, beta) + u[cidx] + w\n        pm.Normal(\"y\", mu, pm.math.sqrt(v), observed=y)\n        try:\n            idata = pm.sample(draws=draws, tune=1000, chains=chains, random_seed=seed, target_accept=0.95,\n                              nuts_sampler=\"nutpie\", progressbar=False)\n        except (ImportError, ValueError, RuntimeError) as e:\n            logger.warning(f\"nutpie unavailable ({e!r:.100}); using the PyMC NUTS sampler\")\n            idata = pm.sample(draws=draws, tune=1000, chains=min(chains, 4), cores=min(chains, 4),\n                              random_seed=seed, target_accept=0.95, progressbar=False)\n    return idata, X, cols\n\"\"\"Shared screen protocol S0: onset, newborn flag, home field, dev restriction, outcomes O1/O2r/O3, R_j, B5.\n\nCredit-bound deviation D8 (documented): field labels for S0 (home, early/late field distributions, B5, O2r, R_j)\ncome from ONE group_by=primary_topic.field.id call per window (1 credit) instead of source group_by + venue\nlabelling of every source (hundreds of credits per concept). The candidate lineage feature keeps VENUE labels,\nso outcome labels and feature labels come from different label systems (no shared-measurement leakage).\n\"\"\"\nfrom __future__ import annotations\n\nimport math\nfrom concurrent.futures import ThreadPoolExecutor\n\nimport numpy as np\nfrom loguru import logger\nfrom scipy.special import gammaln\n\nfrom oa import CapReached, Client, OAError, SharedPoolLow\nfrom panel import BASE_FILTER, DEV_FIELDS, search_filter\n\nFIELD_GB = \"primary_topic.field.id\"\n\n\ndef yearly(cl: Client, c: dict) -> dict[int, int]:\n    d = cl.get(\"/works\", {\"filter\": f\"{search_filter(c)},{BASE_FILTER}\", \"group_by\": \"publication_year\"},\n               summary=f\"yc {c['canonical']}\")\n    return {int(g[\"key\"]): g[\"count\"] for g in d[\"group_by\"] if str(g[\"key\"]).isdigit()}\n\n\ndef global_counts(cl: Client) -> dict[int, int]:\n    d = cl.get(\"/works\", {\"filter\": BASE_FILTER, \"group_by\": \"publication_year\"}, summary=\"global G\")\n    return {int(g[\"key\"]): g[\"count\"] for g in d[\"group_by\"] if str(g[\"key\"]).isdigit()}\n\n\ndef field_counts(cl: Client, c: dict, y0: int, y1: int) -> dict[str, int]:\n    d = cl.get(\"/works\", {\"filter\": f\"{search_filter(c)},{BASE_FILTER},publication_year:{y0}-{y1}\",\n                          \"group_by\": FIELD_GB}, summary=f\"fields {c['canonical']} {y0}-{y1}\")\n    return {g[\"key_display_name\"]: g[\"count\"] for g in d[\"group_by\"]\n            if g[\"key_display_name\"] and g[\"key\"] not in (\"unknown\", None)}\n\n\ndef onset(yc: dict[int, int]) -> int | None:\n    ys = [y for y in range(2000, 2015) if yc.get(y, 0) >= 20]\n    return min(ys) if ys else None\n\n\ndef newborn(yc: dict[int, int], t0: int) -> bool:\n    return all(yc.get(t0 - k, 0) < 0.25 * yc.get(t0 + 2, 0) for k in (1, 2, 3))\n\n\ndef home_fields(fc: dict[str, int]) -> list[str]:\n    tot = sum(fc.values())\n    if not tot:\n        return []\n    h = [f for f, n in fc.items() if n / tot >= 0.40]\n    return h or [max(fc, key=fc.get)]\n\n\ndef rarefied_richness(counts: list[int], m: int) -> float:\n    \"\"\"Exact hypergeometric rarefaction E[S_m] = sum_j 1 - C(N-n_j, m)/C(N, m) (Hurlbert 1971).\"\"\"\n    N = int(sum(counts))\n    if N < m:\n        return float(\"nan\")\n\n    def lnC(n: int, k: int) -> float:\n        return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1) if 0 <= k <= n else -np.inf\n\n    s = 0.0\n    for n_j in counts:\n        if n_j <= 0:\n            continue\n        s += 1 - (math.exp(lnC(N - n_j, m) - lnC(N, m)) if N - n_j >= m else 0.0)\n    return s\n\n\ndef shannon(counts: list[int]) -> float:\n    a = np.asarray([x for x in counts if x > 0], float)\n    if a.sum() == 0:\n        return 0.0\n    p = a / a.sum()\n    return float(-(p * np.log(p)).sum())\n\n\ndef fetch_s0(cl: Client, order: list[dict]) -> dict:\n    \"\"\"All raw S0 pulls in seeded order; returns {canonical: raw dict}. Stops cleanly on credit guards.\"\"\"\n    raw: dict[str, dict] = {}\n    stop = None\n    try:\n        G = global_counts(cl)\n    except (CapReached, SharedPoolLow) as e:\n        return {\"_G\": None, \"_stop\": repr(e)}\n\n    def counts(c: dict) -> tuple[str, dict | str]:\n        try:\n            return c[\"canonical\"], yearly(cl, c)\n        except (CapReached, SharedPoolLow, OAError) as e:\n            return c[\"canonical\"], repr(e)\n\n    with ThreadPoolExecutor(3) as ex:\n        for name, yc in ex.map(counts, order):\n            raw[name] = {\"yc\": yc}\n    # windows only for concepts with an onset in the dev window\n    def windows(c: dict) -> tuple[str, dict]:\n        r = raw[c[\"canonical\"]]\n        out: dict = {}\n        if not isinstance(r[\"yc\"], dict):\n            return c[\"canonical\"], out\n        t0 = onset(r[\"yc\"])\n        if t0 is None or not 2003 <= t0 <= 2009:\n            return c[\"canonical\"], out\n        try:\n            out[\"f_t0_t1\"] = field_counts(cl, c, t0, t0 + 1)\n            if any(h not in DEV_FIELDS for h in home_fields(out[\"f_t0_t1\"])):\n                return c[\"canonical\"], out  # sealed: fetch nothing further\n            out[\"f_early\"] = field_counts(cl, c, t0, t0 + 4)\n            out[\"f_t3_t4\"] = field_counts(cl, c, t0 + 3, t0 + 4)\n            out[\"f_late\"] = field_counts(cl, c, t0 + 6, t0 + 8)\n        except (CapReached, SharedPoolLow, OAError) as e:\n            out[\"error\"] = repr(e)\n        return c[\"canonical\"], out\n\n    with ThreadPoolExecutor(3) as ex:\n        for name, w in ex.map(windows, order):\n            raw[name].update(w)\n    raw[\"_G\"] = G\n    raw[\"_stop\"] = stop\n    return raw\n\n\ndef compute_s0(raw: dict, order: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:\n    \"\"\"Returns (outcome rows for all concepts incl. dropped, field-retention rows, dropped rows).\"\"\"\n    G = {int(k): v for k, v in raw[\"_G\"].items()}\n    rows, frows, dropped = [], [], []\n    for c in order:\n        name = c[\"canonical\"]\n        r = raw.get(name, {})\n        yc = r.get(\"yc\")\n        if isinstance(yc, dict):\n            yc = {int(k): v for k, v in yc.items()}\n        row = {\"concept\": name, \"panel_group\": c[\"panel_group\"]}\n        if not isinstance(yc, dict):\n            dropped.append({\"concept\": name, \"reason\": f\"no_counts:{yc}\"})\n            continue\n        t0 = onset(yc)\n        row.update(t0=t0, yc={str(k): v for k, v in sorted(yc.items()) if 1995 <= k <= 2025})\n        if t0 is None:\n            dropped.append({\"concept\": name, \"reason\": \"no_onset\"})\n            continue\n        row[\"newborn\"] = newborn(yc, t0)\n        if not 2003 <= t0 <= 2009:\n            dropped.append({\"concept\": name, \"reason\": \"t0_out_of_dev\"})\n            continue\n        f01 = r.get(\"f_t0_t1\")\n        if f01 is None:\n            dropped.append({\"concept\": name, \"reason\": f\"no_home_data:{r.get('error')}\"})\n            continue\n        H = home_fields(f01)\n        sealed = [h for h in H if h not in DEV_FIELDS]\n        if sealed:\n            dropped.append({\"concept\": name, \"reason\": f\"home_sealed:{sealed[0]}\"})\n            continue\n        if \"f_late\" not in r:\n            dropped.append({\"concept\": name, \"reason\": f\"no_window_data:{r.get('error')}\"})\n            continue\n        dev_group = max(H, key=lambda h: f01.get(h, 0))\n        fe, fl, f34 = r[\"f_early\"], r[\"f_late\"], r[\"f_t3_t4\"]\n        Ne, Nl = sum(fe.values()), sum(fl.values())\n        tot_e = sum(yc.get(y, 0) for y in range(t0, t0 + 5))\n        tot_l = sum(yc.get(y, 0) for y in range(t0 + 6, t0 + 9))\n        share = lambda y: yc.get(y, 0) / G[y]\n        o1 = int(np.mean([share(y) for y in range(t0 + 6, t0 + 9)]) >= share(t0 + 5))\n        peak = max(yc.get(y, 0) for y in range(t0 + 3, t0 + 9))\n        tail = np.mean([yc.get(t0 + 7, 0), yc.get(t0 + 8, 0)])\n        o3 = int(tail == 0 or peak / tail >= 2)\n        lc = list(fl.values())\n        row.update(\n            home=\"|\".join(H), dev_group=dev_group,\n            label_coverage_early=Ne / tot_e if tot_e else np.nan,\n            label_coverage_late=Nl / tot_l if tot_l else np.nan,\n            O1=o1, O2r=rarefied_richness(lc, 30), O2r_m50=rarefied_richness(lc, 50),\n            O2r_m20=rarefied_richness(lc, 20), O3=o3, N_late=Nl, O2r_hurdle=int(Nl >= 30),\n            # B5\n            B_logvol=math.log1p(tot_e),\n            B_growth=math.log((yc.get(t0 + 4, 0) + 1) / (yc.get(t0 + 1, 0) + 1)),\n            B_offhome=(sum(n for f, n in fe.items() if f not in H) / Ne) if Ne else np.nan,\n            B_entropy=shannon(list(fe.values())),\n            B_nfields=sum(1 for n in fe.values() if n >= 2),\n            off_early_vol=math.log1p(sum(n for f, n in fe.items() if f not in H)),\n            off_growth=math.log((sum(n for f, n in f34.items() if f not in H) + 1)\n                                / (sum(n for f, n in f01.items() if f not in H) + 1)),\n        )\n        rows.append(row)\n        for j, nje in fe.items():\n            if j in H or nje < 5:\n                continue\n            njl = fl.get(j, 0)\n            se, sl = nje / Ne, (njl / Nl if Nl else 0.0)\n            frows.append({\"concept\": name, \"field\": j, \"dev_group\": dev_group,\n                          \"R_j\": int(sl >= 0.5 * se and njl >= 9), \"n_j_early\": nje, \"n_j_late\": njl,\n                          \"log_n_j_early\": math.log(nje),\n                          \"growth_j\": math.log((f34.get(j, 0) + 1) / (f01.get(j, 0) + 1)),\n                          \"share_j\": se})\n    logger.info(f\"S0: {len(rows)} dev concepts, {len(frows)} field units, {len(dropped)} dropped\")\n    return rows, frows, dropped\n\"\"\"Screen statistics: leave-one-dev-group-out (LOGO) prediction of B5 vs B5+candidate, bootstrap CIs, per-group\nsigns, AUC deltas, the field-level test and reliability helpers.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nfrom scipy.stats import spearmanr\nfrom sklearn.linear_model import LogisticRegression, Ridge\nfrom sklearn.metrics import roc_auc_score\nfrom sklearn.preprocessing import StandardScaler\n\nSEED = 20260928\n\n\ndef _impute(Xtr: np.ndarray, Xte: np.ndarray) -> tuple[np.ndarray, np.ndarray]:\n    med = np.nanmedian(Xtr, axis=0)\n    med = np.where(np.isfinite(med), med, 0.0)\n    return np.where(np.isfinite(Xtr), Xtr, med), np.where(np.isfinite(Xte), Xte, med)\n\n\ndef logo_oof(X: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str = \"ridge\") -> np.ndarray:\n    \"\"\"Out-of-fold predictions; training-fold median imputation + standardisation inside each fold.\"\"\"\n    oof = np.full(len(y), np.nan)\n    for g in np.unique(groups):\n        te = groups == g\n        tr = ~te\n        if tr.sum() < 3:\n            continue\n        Xtr, Xte = _impute(X[tr], X[te])\n        sc = StandardScaler().fit(Xtr)\n        Xtr, Xte = sc.transform(Xtr), sc.transform(Xte)\n        Xtr, Xte = np.nan_to_num(Xtr), np.nan_to_num(Xte)\n        if kind == \"ridge\":\n            oof[te] = Ridge(alpha=1.0).fit(Xtr, y[tr]).predict(Xte)\n        else:\n            if len(np.unique(y[tr])) < 2:\n                oof[te] = y[tr].mean()\n                continue\n            oof[te] = LogisticRegression(C=1.0, max_iter=2000).fit(Xtr, y[tr]).predict_proba(Xte)[:, 1]\n    return oof\n\n\ndef rho(a: np.ndarray, b: np.ndarray) -> float:\n    m = np.isfinite(a) & np.isfinite(b)\n    if m.sum() < 4 or np.std(a[m]) == 0 or np.std(b[m]) == 0:\n        return float(\"nan\")\n    return float(spearmanr(a[m], b[m])[0])\n\n\ndef auc(y: np.ndarray, p: np.ndarray) -> float:\n    m = np.isfinite(p) & np.isfinite(y)\n    if len(np.unique(y[m])) < 2:\n        return float(\"nan\")\n    return float(roc_auc_score(y[m], p[m]))\n\n\ndef compare(XB: np.ndarray, Xc: np.ndarray, y: np.ndarray, groups: np.ndarray, kind: str = \"ridge\",\n            n_boot: int = 2000, n_refit: int = 0, clusters: np.ndarray | None = None) -> dict:\n    \"\"\"B vs B+cand under LOGO. Metric: Spearman (ridge) or AUC (logistic). Bootstrap over concepts (or clusters)\n    on the fixed OOF pairs, plus an optional refit bootstrap. Per-group deltas and signs.\"\"\"\n    XBC = np.hstack([XB, Xc])\n    oB = logo_oof(XB, y, groups, kind)\n    oBC = logo_oof(XBC, y, groups, kind)\n    met = rho if kind == \"ridge\" else (lambda p, yy: auc(yy, p))\n    mB, mBC = met(oB, y), met(oBC, y)\n    rng = np.random.default_rng(SEED)\n    units = clusters if clusters is not None else np.arange(len(y))\n    uu = np.unique(units)\n    rows_of = {u: np.where(units == u)[0] for u in uu}\n    deltas = []\n    for _ in range(n_boot):\n        pick = rng.choice(uu, len(uu))\n        ii = np.concatenate([rows_of[u] for u in pick])\n        deltas.append(met(oBC[ii], y[ii]) - met(oB[ii], y[ii]))\n    deltas = np.array(deltas)\n    ci = [float(np.nanpercentile(deltas, 5)), float(np.nanpercentile(deltas, 95))] if np.isfinite(deltas).any() else [np.nan, np.nan]\n    refit = None\n    if n_refit:\n        rd = []\n        for _ in range(n_refit):\n            pick = rng.choice(uu, len(uu))\n            ii = np.concatenate([rows_of[u] for u in pick])\n            if len(np.unique(groups[ii])) < 2:\n                continue\n            a = logo_oof(XB[ii], y[ii], groups[ii], kind)\n            b = logo_oof(XBC[ii], y[ii], groups[ii], kind)\n            rd.append(met(b, y[ii]) - met(a, y[ii]))\n        rd = np.array(rd)\n        refit = {\"n\": int(np.isfinite(rd).sum()), \"ci90\": [float(np.nanpercentile(rd, 5)), float(np.nanpercentile(rd, 95))],\n                 \"mean\": float(np.nanmean(rd))} if np.isfinite(rd).any() else None\n    per = {}\n    for g in np.unique(groups):\n        m = groups == g\n        n = int(m.sum()) if clusters is None else int(len(np.unique(clusters[m])))\n        d = met(oBC[m], y[m]) - met(oB[m], y[m])\n        per[str(g)] = {\"n\": n, \"metric_B\": met(oB[m], y[m]), \"metric_BC\": met(oBC[m], y[m]), \"delta\": d,\n                       \"sign\": (\"insufficient\" if n < 5 or not np.isfinite(d) else (\"+\" if d > 1e-12 else (\"-\" if d < -1e-12 else \"0\")))}\n    return {\"metric_B\": mB, \"metric_BC\": mBC, \"delta\": mBC - mB, \"ci90\": ci, \"refit_bootstrap\": refit,\n            \"per_group\": per, \"n_pos_groups\": sum(1 for v in per.values() if v[\"sign\"] == \"+\"),\n            \"n\": int(np.isfinite(y).sum()), \"oof_B\": oB, \"oof_BC\": oBC}\n\n\ndef spearman_brown(r: float) -> float:\n    return 2 * r / (1 + r) if np.isfinite(r) and r > -1 else float(\"nan\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-29 21:03:22 UTC

```
Now measuring raw per-concept data sizes to decide what fits into `mini_demo_data.json`.
```

### [27] TOOL CALL — Bash · 2026-09-29 21:03:22 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cd $W; python3 - <<'EOF'
import json,gzip,glob,os
from pathlib import Path
tot=0;tott=0
d=json.loads(gzip.decompress(Path("results/concepts/chip_seq/s2_raw.json.gz").read_bytes()))
print(d.keys()); print({k:(len(v) if hasattr(v,'__len__') else v) for k,v in d.items()})
print(json.dumps(d["early"][0])[:1500]); print(json.dumps(d["late"][0])[:600])
b=json.loads(gzip.decompress(Path("results/concepts/chip_seq/bg.json.gz").read_bytes()))
print(b.keys(), {k:len(v) if hasattr(v,'__len__') else v for k,v in b.items()})
k=next(iter(b["refs"])); print(k,b["refs"][k][:3]); r=b["refs"][k][0]; print(b["fos"].get(r))
EOF
head -3 logs/credits.csv; wc -l logs/credits.csv; head -5 results/dropped.csv; python3 -c "
import pandas as pd; print(pd.read_csv('results/outcomes.csv')[['concept','dev_group']].groupby('dev_group').concept.apply(list).to_dict())"
```

### [28] TOOL RESULT — Bash · 2026-09-29 21:03:24 UTC

```
{"stdout": "dict_keys(['concept', 't0', 'query', 'early', 'late', 'total_early', 'total_late', 'citations', 'n_parents_all', 'parent_thin'])\n{'concept': 8, 't0': 2008, 'query': 10, 'early': 1375, 'late': 2439, 'total_early': 1375, 'total_late': 2439, 'citations': 826, 'n_parents_all': 826, 'parent_thin': 1.0}\n{\"paperId\": \"00489d5626c499f010a423cfb59815ab2346d833\", \"externalIds\": {\"PubMedCentral\": \"2924305\", \"MAG\": \"2080849609\", \"DOI\": \"10.1371/journal.pgen.1001065\", \"CorpusId\": 215780349, \"PubMed\": \"20808887\"}, \"title\": \"Genome-Wide Profiling of p63 DNA\\u2013Binding Sites Identifies an Element that Regulates Gene Expression during Limb Development in the 7q21 SHFM1 Locus\", \"venue\": \"PLoS Genetics\", \"year\": 2010, \"openAccessPdf\": {\"url\": \"https://journals.plos.org/plosgenetics/article/file?id=10.1371/journal.pgen.1001065&type=printable\", \"status\": \"GOLD\", \"license\": \"CCBY\", \"disclaimer\": \"Notice: Paper or abstract available at https://pmc.ncbi.nlm.nih.gov/articles/PMC2924305, which is subject to the license by the author or copyright owner provided with this content. Please go to the source to verify the license and copyright information for your use.\"}, \"s2FieldsOfStudy\": [{\"category\": \"Biology\", \"source\": \"external\"}, {\"category\": \"Medicine\", \"source\": \"external\"}, {\"category\": \"Biology\", \"source\": \"s2-fos-model\"}, {\"category\": \"Medicine\", \"source\": \"s2-fos-model\"}], \"publicationTypes\": [\"JournalArticle\"], \"authors\": [{\"authorId\": \"34746755\", \"name\": \"Evelyn N. Kouwenhoven\"}, {\"authorId\": \"7467252\", \"name\": \"S. J. van Heeringen\"}, {\"authorId\": \"2454574\", \"name\": \"J. Tena\"}, {\"authorId\": \"144783156\", \"name\": \"M. Oti\"}, {\"authorId\": \"1837495\", \"name\": \"B. Dutilh\"}, {\"authorId\": \"113801292\", \"name\": \"M. Alonso\"}, {\"authorId\": \"2461557304\", \"name\": \"Elisa de la Calle-Mustienes\"}, {\"a\n{\"paperId\": \"0002a62555af9db2ae750bec763068ab65cb44b6\", \"year\": 2015, \"s2FieldsOfStudy\": [{\"category\": \"Biology\", \"source\": \"external\"}, {\"category\": \"Biology\", \"source\": \"s2-fos-model\"}]}\ndict_keys(['children', 'refs', 'fos']) {'children': 114, 'refs': 110, 'fos': 833}\n01fa28ef314f50186f11831f7d8a49cfd4aff3bb ['https://openalex.org/W2151166716', 'https://openalex.org/W1983409497', 'https://openalex.org/W2155337211']\n[{'category': 'Biology', 'source': 'external'}, {'category': 'Medicine', 'source': 'external'}, {'category': 'Biology', 'source': 's2-fos-model'}, {'category': 'Medicine', 'source': 's2-fos-model'}]\nts,path,summary,credits,remaining\r\n2026-09-28T12:22:14,/works,\"type:article|review,is_paratext:false\",0,0\r\n2026-09-28T12:22:16,/works,\"type:article|review,is_paratext:false\",0,0\r\n12024 logs/credits.csv\nconcept,reason\nbiosimilar,home_sealed:Immunology and Microbiology (OpenAlex S0)\ncardiac resynchronization therapy,t0_out_of_dev\ndictionary learning,t0_out_of_dev\ndrug-eluting stent,t0_out_of_dev\n{'Biochemistry, Genetics and Molecular Biology': ['zinc finger nuclease', 'DNA barcoding', 'synthetic biology', 'long noncoding RNA', 'sirtuin', 'piRNA', 'human microbiome', 'RNA-seq', 'optogenetics', 'metagenomics', 'ChIP-seq', 'copy number variation', 'interactome'], 'Computer Science': ['Web 2.0', 'sentiment analysis', 'crowdsourcing', 'mashup', 'WiMAX', 'latent Dirichlet allocation', 'social tagging', 'ZigBee', 'extreme learning machine', 'learning to rank', 'service-oriented architecture', 'network coding', 'cognitive radio', 'MapReduce', 'cyber-physical system', 'vehicular ad hoc network', 'compressed sensing', 'internet of things', 'folksonomy', 'LTE-Advanced', 'cloud computing'], 'Engineering': ['smart grid', 'energy harvesting', 'wireless body area network'], 'Medicine': ['cancer stem cell', 'pandemic H1N1', 'comparative effectiveness research', 'next-generation sequencing', 'takotsubo cardiomyopathy', 'severe acute respiratory syndrome', 'induced pluripotent stem cell', 'ribotype 027', 'patient-centered medical home', 'natural orifice transluminal endoscopic surgery', 'single-incision laparoscopic surgery']}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-29 21:03:34 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; cd $W; python3 - <<'EOF'
import json,gzip
from pathlib import Path
import pandas as pd
names=pd.read_csv('results/outcomes.csv').concept.tolist()
slug=lambda n:"".join(ch if ch.isalnum() else "_" for ch in n.lower()).strip("_")
def trim_fos(f): return [{"category":x["category"],"source":x.get("source")} for x in (f or [])]
tot=0;rows=[]
for n in names:
    sl=slug(n)
    d=json.loads(gzip.decompress(Path(f"results/concepts/{sl}/s2_raw.json.gz").read_bytes()))
    b=json.loads(gzip.decompress(Path(f"results/concepts/{sl}/bg.json.gz").read_bytes()))
    e=[{"paperId":p["paperId"],"year":p.get("year"),"gstatus":p["gstatus"],"s2FieldsOfStudy":trim_fos(p.get("s2FieldsOfStudy")),
        "authors":[{"authorId":a.get("authorId")} for a in p.get("authors") or []],
        "externalIds":{k:v for k,v in (p.get("externalIds") or {}).items() if k in("MAG","DOI")}} for p in d["early"]]
    s=len(json.dumps({"early":e,"late":[{"s2FieldsOfStudy":trim_fos(p.get("s2FieldsOfStudy"))} for p in d["late"]],"cit":d["citations"],"bg":b}))
    rows.append((n,len(d["early"]),len(d["late"]),len(d["citations"]),s/1e6)); tot+=s
for r in sorted(rows,key=lambda r:r[-1]): print(r)
print(tot/1e6)
EOF
```

### [30] TOOL RESULT — Bash · 2026-09-29 21:03:44 UTC

```
{"stdout": "('zinc finger nuclease', 152, 629, 99, 0.725432)\n('ribotype 027', 260, 209, 196, 0.731437)\n('takotsubo cardiomyopathy', 380, 630, 260, 0.777474)\n('sirtuin', 288, 1101, 192, 0.969207)\n('internet of things', 391, 3000, 232, 1.035989)\n('single-incision laparoscopic surgery', 683, 311, 540, 1.050309)\n('human microbiome', 466, 1049, 274, 1.110105)\n('social tagging', 789, 583, 508, 1.205642)\n('natural orifice transluminal endoscopic surgery', 813, 349, 642, 1.336313)\n('next-generation sequencing', 479, 3000, 141, 1.360016)\n('piRNA', 535, 689, 390, 1.424013)\n('patient-centered medical home', 859, 1083, 564, 1.447455)\n('learning to rank', 747, 737, 581, 1.465469)\n('long noncoding RNA', 571, 3000, 262, 1.474242)\n('latent Dirichlet allocation', 845, 1478, 564, 1.60519)\n('interactome', 645, 1207, 427, 1.677239)\n('folksonomy', 1081, 477, 793, 1.714445)\n('cloud computing', 1503, 3000, 263, 1.715116)\n('DNA barcoding', 797, 1994, 466, 1.825635)\n('sentiment analysis', 962, 3000, 588, 1.92251)\n('extreme learning machine', 726, 2797, 426, 1.92963)\n('cancer stem cell', 944, 3000, 446, 2.047194)\n('wireless body area network', 1039, 1679, 740, 2.120825)\n('metagenomics', 945, 2539, 562, 2.146173)\n('synthetic biology', 924, 2373, 522, 2.187031)\n('copy number variation', 1125, 2417, 642, 2.242993)\n('LTE-Advanced', 1749, 1644, 1077, 2.355222)\n('mashup', 2093, 1023, 1500, 2.533244)\n('energy harvesting', 1147, 3000, 680, 2.647525)\n('cyber-physical system', 1520, 3000, 865, 2.668573)\n('network coding', 1524, 3000, 866, 2.696073)\n('comparative effectiveness research', 1794, 746, 1380, 2.721712)\n('ChIP-seq', 1375, 2439, 826, 2.756755)\n('ZigBee', 2480, 3000, 1425, 2.869093)\n('pandemic H1N1', 1541, 747, 1243, 2.904778)\n('optogenetics', 1609, 3000, 909, 3.0953)\n('crowdsourcing', 2152, 3000, 1112, 3.466062)\n('WiMAX', 4020, 3000, 1500, 3.582064)\n('service-oriented architecture', 3723, 3000, 1500, 3.963722)\n('MapReduce', 2720, 3000, 1500, 4.048447)\n('vehicular ad hoc network', 2422, 3000, 1500, 4.06857)\n('induced pluripotent stem cell', 2646, 3000, 1403, 4.315599)\n('compressed sensing', 4194, 3000, 1500, 5.019454)\n('cognitive radio', 4684, 3000, 1500, 5.020904)\n('RNA-seq', 3642, 2999, 1500, 5.117143)\n('severe acute respiratory syndrome', 6006, 1189, 1500, 5.574414)\n('Web 2.0', 13044, 3000, 1500, 6.724115)\n('smart grid', 9367, 3000, 1500, 7.119963)\n124.515816", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] ASSISTANT · 2026-09-29 21:04:30 UTC

```
I'll package 18 of the 48 dev concepts (spread across all 4 field groups, ~25 MB after trimming unused keys) plus the full S0 count file. The builder script comes first.
```

### [32] TOOL CALL — Write · 2026-09-29 21:04:30 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/make_mini_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json for code_demo.ipynb from the original artifact's published per-concept data.

Keeps 18 of the 48 dev concepts (all four dev field groups) and only the paper keys that method.py actually reads
(paperId, year, gstatus, s2FieldsOfStudy, authors[].authorId, externalIds.MAG/DOI), so the analysis code runs
unchanged on the subset. Also embeds the full S0 yearly-count file (all 78 panel concepts), the OpenAlex credit
ledger column and the headline numbers of the original full 48-concept run for comparison.
Usage: python make_mini_data.py <path-to-original-artifact-folder>
"""
import gzip
import json
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"
CONCEPTS = [
    # Biochemistry, Genetics and Molecular Biology
    "zinc finger nuclease", "sirtuin", "human microbiome", "piRNA", "interactome",
    # Medicine
    "ribotype 027", "takotsubo cardiomyopathy", "single-incision laparoscopic surgery",
    "natural orifice transluminal endoscopic surgery", "patient-centered medical home",
    # Computer Science
    "internet of things", "social tagging", "learning to rank", "latent Dirichlet allocation", "folksonomy",
    "cloud computing",
    # Engineering
    "wireless body area network", "energy harvesting",
]


def slug(name: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in name.lower()).strip("_")


def trim_fos(f):
    return [{"category": x["category"], "source": x.get("source")} for x in (f or [])]


def trim_early(p):
    return {"paperId": p["paperId"], "year": p.get("year"), "gstatus": p["gstatus"],
            "s2FieldsOfStudy": trim_fos(p.get("s2FieldsOfStudy")),
            "authors": [{"authorId": a.get("authorId")} for a in p.get("authors") or []],
            "externalIds": {k: v for k, v in (p.get("externalIds") or {}).items() if k in ("MAG", "DOI")}}


concepts = {}
for name in CONCEPTS:
    sl = slug(name)
    d = json.loads(gzip.decompress((SRC / "results" / "concepts" / sl / "s2_raw.json.gz").read_bytes()))
    b = json.loads(gzip.decompress((SRC / "results" / "concepts" / sl / "bg.json.gz").read_bytes()))
    d["early"] = [trim_early(p) for p in d["early"]]
    d["late"] = [{"paperId": p["paperId"], "year": p.get("year"), "s2FieldsOfStudy": trim_fos(p.get("s2FieldsOfStudy"))}
                 for p in d["late"]]
    b["fos"] = {k: (trim_fos(v) if v is not None else None) for k, v in b["fos"].items()}
    concepts[sl] = {"s2_raw": d, "bg": b}

sr = json.loads((SRC / "results" / "screen_result.json").read_text())
reference = {k: sr[k] for k in ("n_used", "delta_rho", "ci90", "rho_B", "rho_BC", "n_pos_groups", "size_corr",
                                "survives", "eligibility_threshold")}
reference["reliability_A_h_SB"] = sr["reliability"]["A_h"]["reliability_SB"]
reference["delta_auc_O1"] = sr["delta_auc_O1"]["delta"]
reference["field_level_delta"] = sr["field_level"]["delta"]
reference["M1_R2"] = sr["M1"]["R2"]
reference["tau_c"], reference["tau_cj"] = sr["pooling"]["tau_c"], sr["pooling"]["tau_cj"]

credits = [int(line.split(",")[-2]) for line in (SRC / "logs" / "credits.csv").read_text().splitlines()[1:]]
out = {"description": "Mini demo data for the naturalisation-gap (A*_h) screen: 18 of 48 P78 dev concepts",
       "concept_names": CONCEPTS,
       "s0_raw": json.loads((SRC / "results" / "s0_raw.json").read_text()),
       "concepts": concepts, "credits": credits, "reference_full_run": reference}
OUT.write_text(json.dumps(out, separators=(",", ":")))
print(OUT, OUT.stat().st_size / 1e6, "MB")
```

### [33] TOOL RESULT — Write · 2026-09-29 21:04:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/make_mini_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json for code_demo.ipynb from the original artifact's published per-concept data.\n\nKeeps 18 of the 48 dev concepts (all four dev field groups) and only the paper keys that method.py actually reads\n(paperId, year, gstatus, s2FieldsOfStudy, authors[].authorId, externalIds.MAG/DOI), so the analysis code runs\nunchanged on the subset. Also embeds the full S0 yearly-count file (all 78 panel concepts), the OpenAlex credit\nledger column and the headline numbers of the original full 48-concept run for comparison.\nUsage: python make_mini_data.py <path-to-original-artifact-folder>\n\"\"\"\nimport gzip\nimport json\nimport sys\nfrom pathlib import Path\n\nSRC = Path(sys.argv[1])\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\nCONCEPTS = [\n    # Biochemistry, Genetics and Molecular Biology\n    \"zinc finger nuclease\", \"sirtuin\", \"human microbiome\", \"piRNA\", \"interactome\",\n    # Medicine\n    \"ribotype 027\", \"takotsubo cardiomyopathy\", \"single-incision laparoscopic surgery\",\n    \"natural orifice transluminal endoscopic surgery\", \"patient-centered medical home\",\n    # Computer Science\n    \"internet of things\", \"social tagging\", \"learning to rank\", \"latent Dirichlet allocation\", \"folksonomy\",\n    \"cloud computing\",\n    # Engineering\n    \"wireless body area network\", \"energy harvesting\",\n]\n\n\ndef slug(name: str) -> str:\n    return \"\".join(ch if ch.isalnum() else \"_\" for ch in name.lower()).strip(\"_\")\n\n\ndef trim_fos(f):\n    return [{\"category\": x[\"category\"], \"source\": x.get(\"source\")} for x in (f or [])]\n\n\ndef trim_early(p):\n    return {\"paperId\": p[\"paperId\"], \"year\": p.get(\"year\"), \"gstatus\": p[\"gstatus\"],\n            \"s2FieldsOfStudy\": trim_fos(p.get(\"s2FieldsOfStudy\")),\n            \"authors\": [{\"authorId\": a.get(\"authorId\")} for a in p.get(\"authors\") or []],\n            \"externalIds\": {k: v for k, v in (p.get(\"externalIds\") or {}).items() if k in (\"MAG\", \"DOI\")}}\n\n\nconcepts = {}\nfor name in CONCEPTS:\n    sl = slug(name)\n    d = json.loads(gzip.decompress((SRC / \"results\" / \"concepts\" / sl / \"s2_raw.json.gz\").read_bytes()))\n    b = json.loads(gzip.decompress((SRC / \"results\" / \"concepts\" / sl / \"bg.json.gz\").read_bytes()))\n    d[\"early\"] = [trim_early(p) for p in d[\"early\"]]\n    d[\"late\"] = [{\"paperId\": p[\"paperId\"], \"year\": p.get(\"year\"), \"s2FieldsOfStudy\": trim_fos(p.get(\"s2FieldsOfStudy\"))}\n                 for p in d[\"late\"]]\n    b[\"fos\"] = {k: (trim_fos(v) if v is not None else None) for k, v in b[\"fos\"].items()}\n    concepts[sl] = {\"s2_raw\": d, \"bg\": b}\n\nsr = json.loads((SRC / \"results\" / \"screen_result.json\").read_text())\nreference = {k: sr[k] for k in (\"n_used\", \"delta_rho\", \"ci90\", \"rho_B\", \"rho_BC\", \"n_pos_groups\", \"size_corr\",\n                                \"survives\", \"eligibility_threshold\")}\nreference[\"reliability_A_h_SB\"] = sr[\"reliability\"][\"A_h\"][\"reliability_SB\"]\nreference[\"delta_auc_O1\"] = sr[\"delta_auc_O1\"][\"delta\"]\nreference[\"field_level_delta\"] = sr[\"field_level\"][\"delta\"]\nreference[\"M1_R2\"] = sr[\"M1\"][\"R2\"]\nreference[\"tau_c\"], reference[\"tau_cj\"] = sr[\"pooling\"][\"tau_c\"], sr[\"pooling\"][\"tau_cj\"]\n\ncredits = [int(line.split(\",\")[-2]) for line in (SRC / \"logs\" / \"credits.csv\").read_text().splitlines()[1:]]\nout = {\"description\": \"Mini demo data for the naturalisation-gap (A*_h) screen: 18 of 48 P78 dev concepts\",\n       \"concept_names\": CONCEPTS,\n       \"s0_raw\": json.loads((SRC / \"results\" / \"s0_raw.json\").read_text()),\n       \"concepts\": concepts, \"credits\": credits, \"reference_full_run\": reference}\nOUT.write_text(json.dumps(out, separators=(\",\", \":\")))\nprint(OUT, OUT.stat().st_size / 1e6, \"MB\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [34] TOOL CALL — Bash · 2026-09-29 21:04:34 UTC

```
python3 make_mini_data.py /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1 && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));print(sum(d['credits']),len(d['credits']),d['reference_full_run'])"
```

### [35] TOOL RESULT — Bash · 2026-09-29 21:04:38 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/mini_demo_data.json 25.132861 MB\n139 12023 {'n_used': 48, 'delta_rho': -0.005644811115935844, 'ci90': [-0.033844584160467935, 0.016635147457856648], 'rho_B': 0.8338037342596614, 'rho_BC': 0.8281589231437255, 'n_pos_groups': 0, 'size_corr': {'vol': 0.1447182724846087, 'growth': -0.17652806531130816, 'offhome_vol': 0.07469330192753998, 'offhome_growth': -0.033112582976598394}, 'survives': False, 'eligibility_threshold': 60, 'reliability_A_h_SB': 0.5835386475610421, 'delta_auc_O1': -0.02626262626262621, 'field_level_delta': 0.0019293924466337042, 'M1_R2': 0.658649967417526, 'tau_c': 0.29435799946446634, 'tau_cj': 0.6480102378952861}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-29 21:05:20 UTC

```
Next I'll build the notebook. To keep the original code byte-exact, the builder script slices the source files by line range and applies only a few listed substitutions. First, the line numbers:
```

### [37] TOOL CALL — Bash · 2026-09-29 21:05:20 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; grep -n "^def \|^# ---\|^@\|^_W\|^SEED\|^if __name\|    # ----------------\|^ROOT\|^RES\|^logger\|^from\|^import\|^class\|^@dataclass\|^T_STRATA\|^FIELD_GB\|^BINS\|^B5\|^PROBE" $W/method.py $W/s0.py $W/lineage.py | grep -v "^.*lineage.py.*def \(contribs\|onehot\|tables\|mh_\|logit_s\|_self\|_cov\|r_away\|crude\)"
```

### [38] TOOL RESULT — Bash · 2026-09-29 21:05:20 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:8:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:10:import math\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:11:from concurrent.futures import ThreadPoolExecutor\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:13:import numpy as np\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:14:from loguru import logger\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:15:from scipy.special import gammaln\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:17:from oa import CapReached, Client, OAError, SharedPoolLow\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:18:from panel import BASE_FILTER, DEV_FIELDS, search_filter\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:20:FIELD_GB = \"primary_topic.field.id\"\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:23:def yearly(cl: Client, c: dict) -> dict[int, int]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:29:def global_counts(cl: Client) -> dict[int, int]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:34:def field_counts(cl: Client, c: dict, y0: int, y1: int) -> dict[str, int]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:41:def onset(yc: dict[int, int]) -> int | None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:46:def newborn(yc: dict[int, int], t0: int) -> bool:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:50:def home_fields(fc: dict[str, int]) -> list[str]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:58:def rarefied_richness(counts: list[int], m: int) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:75:def shannon(counts: list[int]) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:83:def fetch_s0(cl: Client, order: list[dict]) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/s0.py:129:def compute_s0(raw: dict, order: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:17:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:19:import os\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:24:import argparse\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:25:import gzip\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:26:import json\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:27:import math\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:28:import multiprocessing as mp\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:29:import pickle\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:30:import resource\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:31:import sys\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:32:import time\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:33:from concurrent.futures import ProcessPoolExecutor\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:34:from pathlib import Path\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:36:import numpy as np\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:37:import pandas as pd\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:38:from loguru import logger\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:39:from scipy.stats import spearmanr\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:41:ROOT = Path(__file__).resolve().parent\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:42:RES = ROOT / \"results\"\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:45:from lineage import (F, S2_DEV, S2_FIELDS, Concept, crude_lor, foils, load_concept, load_raw, membership,  # noqa: E402\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:47:from panel import DEV_FIELDS, seeded_order, slug  # noqa: E402\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:48:from pool import fit_dl, fit_pymc, fit_reml, predict, var_of  # noqa: E402\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:49:from s0 import compute_s0, newborn, onset, rarefied_richness, shannon  # noqa: E402\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:50:from screen import compare, rho, spearman_brown  # noqa: E402\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:52:logger.remove()\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:53:logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:55:logger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:57:SEED = 20260928\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:58:PROBE_CRUDE = {\"optogenetics\": -0.551, \"crowdsourcing\": 0.382, \"extreme learning machine\": -1.063,\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:60:B5_COLS = [\"B_logvol\", \"B_growth\", \"B_offhome\", \"B_entropy\", \"B_nfields\"]\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:61:BINS = [(0, 15), (15, 30), (30, 60), (60, 10**9)]\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:64:def set_limits() -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:69:def jsonable(o):\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:85:# ------------------------------------------------------------------ S0\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:86:def s0_openalex() -> tuple[dict, pd.DataFrame, pd.DataFrame]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:97:def count_outcomes(yc: dict[int, int], G: dict[int, int], t0: int) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:108:def s0_s2(c: Concept) -> tuple[dict, list[dict]]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:141:def load_bg(c: Concept, sl: str) -> tuple[np.ndarray, np.ndarray]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:162:# ------------------------------------------------------------------ stage 2 wrapper\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:163:def pool_all(units: list[dict], names: list[str], n_off: dict, engine: str = \"reml\"):\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:173:def concept_features(fit, units: list[dict], names: list[str], child_mass: dict) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:206:def stage1_units(concepts: list[Concept], bgs: list, subs: list | None = None, n_boot: int = 200,\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:225:# ------------------------------------------------------------------ split-half reliability (worker)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:226:_W: dict = {}\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:229:def _init_worker(pkl: str) -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:236:def _half_crude(c: Concept, B: np.ndarray, has: np.ndarray, sub: np.ndarray) -> tuple[float, float]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:251:def run_split(s: int) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:297:def reliability(results: list[dict], names: list[str]) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:326:def reliability_vs_n(results: list[dict], names: list[str], n_off_full: dict) -> list[dict]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:342:# ------------------------------------------------------------------ GLMM robustness\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:343:def glmm_check(concepts: list[Concept], bgs: list, names: list[str], max_rows: int = 50000) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:399:# ------------------------------------------------------------------ main\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:400:@logger.catch(reraise=True)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:401:def main() -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:414:    # ---------------- S0 (OpenAlex counts + OpenAlex topic-field S0 where the pool allowed)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:465:    # ---------------- stage 1 + stage 2\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:489:    # ---------------- features table\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:504:    # ---------------- reliability (split halves) -> eligibility\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:523:    # ---------------- screen\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:630:    # ---------------- PyMC headline check + GLMM robustness\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:673:    # ---------------- rule\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:694:    # ---------------- outputs\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:750:def write_method_out(D: pd.DataFrame, FL: pd.DataFrame, sr: dict) -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:786:def figures(D: pd.DataFrame, feat: pd.DataFrame, rel_n: list[dict]) -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/method.py:807:if __name__ == \"__main__\":\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:8:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:10:import gzip\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:11:import hashlib\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:12:import json\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:13:import math\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:14:import warnings\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:15:from dataclasses import dataclass, field\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:16:from pathlib import Path\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:18:import numpy as np\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:20:ROOT = Path(__file__).resolve().parent\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:29:SEED = 20260928\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:32:def membership(fos: list[dict] | None) -> np.ndarray | None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:45:def stable_seed(s: str) -> int:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:49:def home_set(mass: np.ndarray) -> list[int]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:57:@dataclass\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:58:class Concept:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:97:def load_concept(raw: dict) -> Concept:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:128:def build_lineage(c: Concept, citations: dict[str, list[str]]) -> None:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:163:# ---------------------------------------------------------------- stage-1 tables\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:164:T_STRATA = 5\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:216:@dataclass\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:217:class Stage1:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:228:def stage1(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray, sub: np.ndarray | None = None,\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:267:# ---------------------------------------------------------------- foils\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:281:def foils(c: Concept, bgB: np.ndarray, bg_rows: np.ndarray) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1/lineage.py:364:def load_raw(slug_: str) -> dict:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] TOOL CALL — Bash · 2026-09-29 21:05:36 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1; grep -n "    # " $W/method.py | sed -n 1,200p | awk -F: '$1>400'; sed -n 400,414p $W/method.py; sed -n 740,750p $W/method.py; sed -n 360,370p $W/lineage.py
```

### [40] TOOL RESULT — Bash · 2026-09-29 21:05:36 UTC

```
{"stdout": "414:    # ---------------- S0 (OpenAlex counts + OpenAlex topic-field S0 where the pool allowed)\n465:    # ---------------- stage 1 + stage 2\n489:    # ---------------- features table\n504:    # ---------------- reliability (split halves) -> eligibility\n523:    # ---------------- screen\n540:    # size checks\n546:    # eligible subset + newborn-only sensitivity\n556:    # O2r m50 / m20 sensitivity\n562:    # foils and secondaries as candidates (exploratory comparison table)\n578:    # field-level test\n592:        # restricted to units with a stage-1 datum\n599:    # M1: raw concept LOR vs background LOR\n610:    # agreement with the probe\n621:    # cross-source validation of S0 (OpenAlex topic fields vs S2 fields) where both exist\n630:    # ---------------- PyMC headline check + GLMM robustness\n673:    # ---------------- rule\n694:    # ---------------- outputs\n@logger.catch(reraise=True)\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--max-concepts\", type=int, default=10**6)\n    ap.add_argument(\"--splits\", type=int, default=50)\n    ap.add_argument(\"--n-boot\", type=int, default=2000)\n    ap.add_argument(\"--no-pymc\", action=\"store_true\")\n    ap.add_argument(\"--no-glmm\", action=\"store_true\")\n    ap.add_argument(\"--workers\", type=int, default=4)\n    args = ap.parse_args()\n    set_limits()\n    t_start = time.time()\n    RES.mkdir(exist_ok=True)\n\n    # ---------------- S0 (OpenAlex counts + OpenAlex topic-field S0 where the pool allowed)\n    (RES / \"screen_result.json\").write_text(json.dumps(screen_result, indent=1))\n    write_method_out(D, FL, screen_result)\n    try:\n        figures(D, feat, rel_n)\n    except Exception as e:\n        logger.error(f\"figures failed: {e!r}\")\n    logger.info(f\"SURVIVES={survives} clauses={ {k: v['pass'] for k, v in clauses.items()} } \"\n                f\"runtime {time.time()-t_start:.0f}s\")\n\n\ndef write_method_out(D: pd.DataFrame, FL: pd.DataFrame, sr: dict) -> None:\n    Ks = K[np.ix_(keep, keep)] / stock[keep][None, :]\n    return float(np.max(np.abs(np.linalg.eigvals(Ks))))\n\n\ndef load_raw(slug_: str) -> dict:\n    return json.loads(gzip.decompress((ROOT / \"results\" / \"concepts\" / slug_ / \"s2_raw.json.gz\").read_bytes()))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] ASSISTANT · 2026-09-29 21:07:04 UTC

```
Now the notebook builder (lives in the scratchpad; it slices the originals and asserts each substitution matches exactly once):
```

### [42] TOOL CALL — Write · 2026-09-29 21:07:04 UTC

```
File: /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/build_nb.py

"""Build code_demo.ipynb by slicing the ORIGINAL source files (so the code is copied verbatim) and applying a small,
explicit list of notebook-context substitutions (each asserted to match exactly once)."""
import json
import sys
import textwrap
from pathlib import Path

SRC = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1")
OUT = Path("/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/"
           "art_xp8BGBJZsxeI/code_demo.ipynb")
CFG = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}

M = (SRC / "method.py").read_text().splitlines()
LIN = (SRC / "lineage.py").read_text().splitlines()
S0 = (SRC / "s0.py").read_text().splitlines()


def L(lines, a, b):  # 1-indexed inclusive
    return "\n".join(lines[a - 1:b])


def sub(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


def body(a, b):  # dedent a slice of main()'s body
    return textwrap.dedent(L(M, a, b)).strip("\n")


cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": textwrap.dedent(s).strip("\n")})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": s.strip("\n")})


# ------------------------------------------------------------------ setup
md("""
# Does citing a concept "as your own" predict its spread? — the naturalisation-gap screen (candidate L)

This notebook is a runnable demo of the experiment script `method.py` (plus the helper modules it imports:
`panel.py`, `s0.py`, `lineage.py`, `pool.py`, `screen.py`). The code is the original code, split into cells, with
explanations added between the sections.

**What it tests.** Take a research concept (e.g. *compressed sensing*, *optogenetics*). Its early papers (years
t0..t0+4) cite each other. When a paper from an *off-home* field j cites an earlier concept paper, is that parent
more likely to come from field j as well (the concept is being "naturalised" in j) than from the concept's home
field H? The candidate feature is **A\\*_h**, a *background-adjusted naturalisation gap*:

1. **Stage 1.** For each concept × off-home field j, compute a year-stratified Mantel–Haenszel log odds ratio
   (child in j vs H) × (parent in j vs H). Subtract the same log-OR computed on the *same children's background
   reference lists*, which removes plain field homophily. Get a variance from a child bootstrap.
2. **Stage 2.** Pool these ρ̂_cj with a crossed random-effects model fitted by REML (concept effect τ_c, cell effect
   τ_cj). Then A\\*_h = Σ_j π_cj ρ\\*_cj.
3. **Screen.** Does A\\*_h improve on the common 5-feature count baseline **B5** (early volume, growth, off-home
   share, field entropy, number of fields)? The outcome is later field breadth **O2r**, evaluated under
   leave-one-field-group-out (LOGO) ridge prediction. The pre-registered survival rule has four clauses:
   Δρ ≥ 0.10 with CI low > 0, at least 3 of 4 groups positive, split-half reliability ≥ 0.6, and |ρ| with size ≤ 0.6.

**Headline of the original full run (48 dev concepts): A\\*_h does NOT survive.** Δρ = −0.006, 90% CI
[−0.034, 0.017]; 0 of 4 groups are positive; reliability is 0.58.

**Demo data.** `mini_demo_data.json` holds the full S0 yearly-count file for all 78 panel concepts. It also holds
the Semantic Scholar concept papers, citation lineage and background references for **18 of the 48** dev concepts
(all four field groups), trimmed to the keys the code reads. The other concepts follow the original
"not fetched" drop path. With 18 concepts the numbers are noisier than the full run's. The final cell compares
them with the full-run reference values stored in the data file.
""")

code("""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT on Colab, always install
_pip('loguru==0.7.3')

# numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib — pre-installed on Colab, install locally only
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'scikit-learn==1.6.1', 'statsmodels==0.14.6',
         'matplotlib==3.10.0')
""" + CFG.get("pymc_install", ""))

md("""
## Imports

This is the original import block of `method.py`. The five helper modules it imported (`lineage`, `panel`, `pool`,
`s0`, `screen`) are defined inline in the cells below, each with its own import lines.
""")
code(L(M, 19, 39) + "\nimport argparse  # notebook: config namespace replaces the CLI\nimport matplotlib.pyplot as plt")

md("## Data loading\nThe data comes from GitHub, with a fallback to a local `mini_demo_data.json`.")
code('''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json"
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
''')
code('''
data = load_data()
print(f"{len(data['concepts'])} concepts with S2 lineage data:", data["concept_names"])
print(f"S0 yearly counts for {len([k for k in data['s0_raw'] if not k.startswith('_')])} panel concepts")
''')

md("""
## Config

These values replace the original command-line arguments of `method.py`
(`--max-concepts`, `--splits`, `--n-boot`, `--no-pymc`, `--no-glmm`, `--workers`).
The demo values are chosen to finish well inside 10 minutes. The original full-run values are in the comments.
""")
code(CFG["config"])

# ------------------------------------------------------------------ helper modules
md("""
## Helper module `panel.py`: the frozen P78 panel

There are 78 concepts in 4 field groups. They are processed in an order seeded with 20260928.
""")
code((SRC / "panel.py").read_text())

s0_src = L(S0, 1, 16) + "\n" + L(S0, 18, 22) + "\n" + L(S0, 41, 82) + "\n" + L(S0, 129, len(S0))
md("""
## Helper module `s0.py`: shared screen protocol S0

This module defines the onset t0 (first year with ≥ 20 papers), the *newborn* flag, the home field, the exact
rarefied richness (Hurlbert 1971) used for the breadth outcome **O2r** (m = 30), Shannon entropy, and
`compute_s0` for the OpenAlex topic-field version of S0.
*Notebook change:* the OpenAlex API pull functions (`yearly`, `global_counts`, `field_counts`, `fetch_s0`) and
their `oa` client import are left out. They only fetch raw data, and the demo loads that data from
`mini_demo_data.json` instead.
""")
code(s0_src)

lin_src = "\n".join(LIN)
lin_src = sub(lin_src, 'ROOT = Path(__file__).resolve().parent\n', '')
lin_src = sub(lin_src, '''def load_raw(slug_: str) -> dict:
    return json.loads(gzip.decompress((ROOT / "results" / "concepts" / slug_ / "s2_raw.json.gz").read_bytes()))''',
              '''def load_raw(slug_: str) -> dict:
    return data["concepts"][slug_]["s2_raw"]  # notebook: from mini_demo_data.json (was results/concepts/<slug>/s2_raw.json.gz)''')
md("""
## Helper module `lineage.py`: concept lineage, stage-1 contrasts and foils

- Each paper gets a **fractional field membership** over the 23 Semantic Scholar fields of study
  (s2-fos-model, a title/abstract text classifier).
- `build_lineage` keeps concept-paper → concept-paper citation links where the child is in t0..t0+4 and the
  parent is 1–3 years older. Self-citations (shared author) are split off.
- `stage1` builds the year-stratified MH log-OR for every off-home field j, for concept parents and for the
  children's background references. ρ̂_cj is their difference. A multinomial child bootstrap gives the variance.
- `foils` computes the comparison features (raw/background crude log-ORs, relay share, self share,
  coverage, A_unif / A_imp, and R_away, the spectral radius of the cross-field link kernel).
""")
code(lin_src)

md("""
## Helper module `pool.py`: stage 2 partial pooling

The model is y_k = x_k β + u_c(k) + w_k + e_k, with u ~ N(0, τ_c²), w ~ N(0, τ_cj²) and e ~ N(0, v_k).
REML over (log τ_c, log τ_cj) is followed by Henderson's mixed-model equations. The fallback is
DerSimonian–Laird. `fit_pymc` fits the same model with NUTS as a headline check.
""")
code((SRC / "pool.py").read_text())

md("""
## Helper module `screen.py`: LOGO comparison of B5 vs B5 + candidate

`compare` fits a ridge (for O2r) or a logistic model (for O1/O3/R_j) with leave-one-dev-group-out folds. It
compares out-of-fold Spearman ρ (or AUC) and bootstraps concepts (or clusters) on the fixed OOF pairs. It also
reports per-group deltas and signs.
""")
code((SRC / "screen.py").read_text())

# ------------------------------------------------------------------ method.py definitions
hdr = L(M, 41, 82)
hdr = sub(hdr, 'ROOT = Path(__file__).resolve().parent', 'ROOT = Path(".").resolve()  # notebook: outputs go to ./results and ./logs')
hdr = sub(hdr, '''sys.path.insert(0, str(ROOT))

from lineage import (F, S2_DEV, S2_FIELDS, Concept, crude_lor, foils, load_concept, load_raw, membership,  # noqa: E402
                     stage1)
from panel import DEV_FIELDS, seeded_order, slug  # noqa: E402
from pool import fit_dl, fit_pymc, fit_reml, predict, var_of  # noqa: E402
from s0 import compute_s0, newborn, onset, rarefied_richness, shannon  # noqa: E402
from screen import compare, rho, spearman_brown  # noqa: E402
''', '# notebook: the helper modules (lineage, panel, pool, s0, screen) are defined in the cells above\n')
md("""
## `method.py`: constants, logging, resource limits

B5 is the count baseline. `PROBE_CRUDE` holds the crude values from an earlier probe, used for an agreement
check. `BINS` are the off-home-children bins for the reliability-vs-n curve.
""")
code(hdr)

s0m = L(M, 85, 161)
s0m = sub(s0m, '''    raw = json.loads((RES / "s0_raw.json").read_text())''',
          '''    raw = data["s0_raw"]  # notebook: from mini_demo_data.json (was results/s0_raw.json)''')
s0m = sub(s0m, '''    p = RES / "concepts" / sl / "bg.json.gz"
    n = len(c.child_idx)
    B = np.zeros((n, F))
    has = np.zeros(n, bool)
    if not p.exists():
        return B, has
    d = json.loads(gzip.decompress(p.read_bytes()))''', '''    d = data["concepts"].get(sl, {}).get("bg")  # notebook: from mini_demo_data.json (was results/concepts/<slug>/bg.json.gz)
    n = len(c.child_idx)
    B = np.zeros((n, F))
    has = np.zeros(n, bool)
    if d is None:
        return B, has''')
md("""
## S0 outcomes and baseline features

- `count_outcomes` uses OpenAlex yearly counts to get t0, newborn, **O1** (uptake: the share of the literature
  in t0+6..t0+8 is at least the share at t0+5), **O3** (transience) and the count parts of B5.
- `s0_s2` uses the fractional S2 field labels to get the home field, **O2r** (rarefied venue-field breadth in
  t0+6..t0+8), the field-based B5 terms, and the per-field retention units **R_j**.
- `load_bg` loads each child's background references and turns them into a mean field-membership row.
""")
code(s0m)

md("""
## Stage-2 wrapper, per-concept feature A\\*_h, and stage-1 units

`concept_features` aggregates the pooled ρ\\*_cj into A\\*_h with child-mass weights π_cj. It also returns the
posterior SD, the number of fields with Pr(ρ\\* > 0) > 0.8 (`n_nat_fields`), and `max_rho`.
""")
code(L(M, 162, 224))

md("""
## Split-half reliability helpers

Each split divides every concept's children into two halves, stratified on home vs off-home children. Stage 1
and stage 2 are re-run on each half, and the Spearman ρ between the halves' A\\*_h is stepped up with
Spearman–Brown. `reliability_vs_n` repeats this within bins of off-home children.
""")
rel_src = L(M, 225, 341)
code(rel_src)

md("""
## GLMM robustness check

This is a one-stage `BinomialBayesMixedGLM` (variational Bayes) on link-level rows, with discrete labels drawn
from the fractional memberships.
""")
code(L(M, 342, 398))

fig_src = L(M, 750, 805)
fig_src = sub(fig_src, '''    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
''', '''    import matplotlib.pyplot as plt  # notebook: inline backend instead of matplotlib.use("Agg")
''')
fig_src = sub(fig_src, '''fig.savefig(fig_dir / "screen_overview.png", dpi=130); plt.close(fig)''',
              '''fig.savefig(fig_dir / "screen_overview.png", dpi=130); plt.show(); plt.close(fig)''')
md("""
## Output writers

`write_method_out` writes `method_out.json` in the pipeline's exp_gen_sol_out format. `figures` draws the
three-panel overview. In the original script both are defined after `main()`; here they must be defined before
they are called.
""")
code(fig_src)

# ------------------------------------------------------------------ main() body, split into cells
md("""
# Running the screen: the body of `main()`, section by section

### 1. Assemble the dev panel

Walk the 78 concepts in seeded order. Drop a concept if its onset t0 is outside 2003–2009, if its home field is
sealed (outside CS / Engineering / Biology / Medicine), or if its lineage data is not available (here: not in the
18-concept demo subset). Build the S0 rows, the field-retention units and the `Concept` objects.
""")
s1 = body(410, 463)
s1 = sub(s1, '''        p = RES / "concepts" / sl / "s2_raw.json.gz"
        if not p.exists():''', '''        if sl not in data["concepts"]:  # notebook: was the file check RES / "concepts" / sl / "s2_raw.json.gz"''')
code(s1)

md("""
### 2. Stage 1 (per concept × field MH contrasts) and stage 2 (REML pooling)

This step also builds the field-level table of ρ\\*_cj for every (concept, off-home field) unit, including units
with no stage-1 datum (those get the concept-level prediction).
""")
code(body(465, 487))

md("### 3. Feature table: A\\*_h, its secondaries, and the foils for every concept")
code(body(489, 502))

rs = body(504, 521)
rs = sub(rs, '''    pkl = RES / "_concepts.pkl"
    pkl.write_bytes(pickle.dumps((concepts, bgs, names)))
    t = time.time()
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context("spawn"),
                             initializer=_init_worker, initargs=(str(pkl),)) as ex:
        split_res = list(ex.map(run_split, range(args.splits)))
    pkl.unlink()
''', '''    t = time.time()
    # notebook: the original ran the splits in a spawn-based ProcessPoolExecutor (args.workers processes, data passed
    # via a pickle file); spawned workers cannot import functions defined in a notebook, so they run in-process here.
    _W["data"] = (concepts, bgs, names)
    split_res = list(map(run_split, range(args.splits)))
''')
md("""
### 4. Split-half reliability, and the eligibility threshold

The eligibility floor is the lowest off-home-children bin from which every larger bin (with ≥ 4 concepts) reaches
reliability 0.6. The default is 30. *Most of the notebook's runtime is spent here:* each split re-runs stages
1 and 2 twice.
""")
code(rs)

md("""
### 5. The screen: LOGO B5 vs B5 + A\\*_h

- **Main test:** O2r, ridge, bootstrap CI and refit bootstrap.
- O1 / O3 ΔAUC and the hurdle.
- **Size checks:** |ρ| of A\\*_h with log early volume and growth.
- Subsets (eligible, newborn-only, full parent sample) and the O2r m = 50 / m = 20 sensitivities.
""")
code(body(523, 561))

md("""
### 6. Exploratory candidate table

Each secondary and foil is scored as if it were the candidate, against the same B5 baseline.
""")
code(body(562, 577))

md("""
### 7. Field-level test, the M1 mechanism check, probe agreement, and S0 cross-source validation

- **Field level:** does ρ\\*_cj predict whether field j retains the concept (R_j) beyond field size, growth,
  share and the background log-OR? The bootstrap is clustered by concept.
- **M1:** how much of the raw lineage log-OR is explained by the background log-OR, i.e. by plain field
  homophily?
""")
code(body(578, 628))

pm_src = body(630, 671)
pm_src = sub(pm_src, "idata, X_, cols_ = fit_pymc(y_, v_, cidx, len(names), fl_)",
             "idata, X_, cols_ = fit_pymc(y_, v_, cidx, len(names), fl_, draws=args.pymc_draws, chains=args.pymc_chains)")
md("""
### 8. Robustness: PyMC NUTS headline check and the one-stage GLMM

Both are wrapped in `try`, as in the original: a failure here never blocks the screen. PyMC runs only when
`args.no_pymc` is False (see the config cell).
""")
code(pm_src)

md("### 9. The pre-registered survival rule")
code(body(673, 692))

md("""
### 10. Outputs

This step writes the CSVs, `screen_result.json`, `method_out.json` and the overview figure under `./results`.
The figure's three panels show A\\*_h vs O2r, the M1 scatter, and reliability vs n.
""")
code(body(694, 747))

# ------------------------------------------------------------------ results
md("""
## Results summary

The table below sets the demo's key statistics beside the reference values from the original full 48-concept run.
The plots show out-of-fold predictions and the exploratory candidate comparison.
""")
code('''
ref = data["reference_full_run"]
rows = [("n dev concepts used", screen_result["n_used"], ref["n_used"]),
        ("rho_B5 (LOGO OOF Spearman)", screen_result["rho_B"], ref["rho_B"]),
        ("rho_B5+A*_h", screen_result["rho_BC"], ref["rho_BC"]),
        ("Delta-rho", screen_result["delta_rho"], ref["delta_rho"]),
        ("Delta-rho 90% CI low", screen_result["ci90"][0], ref["ci90"][0]),
        ("Delta-rho 90% CI high", screen_result["ci90"][1], ref["ci90"][1]),
        ("positive left-out groups", screen_result["n_pos_groups"], ref["n_pos_groups"]),
        ("reliability A*_h (Spearman-Brown)", (screen_result["reliability"].get("A_h") or {}).get("reliability_SB"),
         ref["reliability_A_h_SB"]),
        ("|rho| with log early volume", abs(screen_result["size_corr"]["vol"]), abs(ref["size_corr"]["vol"])),
        ("|rho| with early growth", abs(screen_result["size_corr"]["growth"]), abs(ref["size_corr"]["growth"])),
        ("O1 Delta-AUC", screen_result["delta_auc_O1"]["delta"], ref["delta_auc_O1"]),
        ("field-level Delta-AUC (R_j)", (screen_result["field_level"] or {}).get("delta"), ref["field_level_delta"]),
        ("M1 R^2 (raw vs background log-OR)", (screen_result["M1"] or {}).get("R2"), ref["M1_R2"]),
        ("REML tau_c", screen_result["pooling"]["tau_c"], ref["tau_c"]),
        ("REML tau_cj", screen_result["pooling"]["tau_cj"], ref["tau_cj"]),
        ("SURVIVES pre-registered rule", screen_result["survives"], ref["survives"])]
summary = pd.DataFrame(rows, columns=["statistic", "demo (this run)", "full run (48 concepts)"])
pd.set_option("display.width", 140)
print(summary.to_string(index=False, float_format=lambda x: f"{x:.3f}"))
print("\\nClause results (demo):")
for k, v in screen_result["clause_results"].items():
    print(f"  {k:<40} pass={v['pass']}  value={v['value']}")
print("\\nPer-group Delta-rho (demo):")
for g, v in screen_result["per_group"].items():
    print(f"  {g:<45} n={v['n']:>2}  delta={v['delta'] if v['delta'] is not None else float('nan'):+.3f}  sign={v['sign']}")

fig, ax = plt.subplots(1, 2, figsize=(14, 4.8))
for g, s_ in D.groupby("dev_group"):
    ax[0].scatter(s_["oof_B5"], s_["O2r"], marker="o", label=f"B5 — {g[:20]}", alpha=.8)
    ax[0].scatter(s_["oof_B5_plus_A_h"], s_["O2r"], marker="x", color=ax[0].collections[-1].get_facecolor()[0], alpha=.8)
ax[0].set_xlabel("out-of-fold prediction (o = B5, x = B5 + A*_h)"); ax[0].set_ylabel("observed O2r")
ax[0].set_title(f"LOGO ridge: rho_B5={screen_result['rho_B']:.3f}, rho_B5+A*_h={screen_result['rho_BC']:.3f}")
ax[0].legend(fontsize=7)
ct = pd.DataFrame({k: {"delta": v["delta_rho"], "lo": v["ci90"][0], "hi": v["ci90"][1]}
                   for k, v in screen_result["candidate_comparison_table"].items()}).T.sort_values("delta")
ax[1].barh(ct.index, ct["delta"], xerr=[ct["delta"] - ct["lo"], ct["hi"] - ct["delta"]], color="tab:gray")
ax[1].axvline(0.10, color="r", ls="--", label="rule bar Delta-rho = 0.10"); ax[1].axvline(0, color="k", lw=.8)
ax[1].set_xlabel("Delta-rho over B5 (90% bootstrap CI)"); ax[1].set_title("Exploratory candidates and foils")
ax[1].legend(fontsize=8)
fig.tight_layout(); plt.show()
''')

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i:02d}"
OUT.write_text(json.dumps(nb, indent=1))
print("cells:", len(cells))
```

### [43] TOOL RESULT — Write · 2026-09-29 21:07:04 UTC

```
{"type": "create", "filePath": "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/build_nb.py", "content": "\"\"\"Build code_demo.ipynb by slicing the ORIGINAL source files (so the code is copied verbatim) and applying a small,\nexplicit list of notebook-context substitutions (each asserted to match exactly once).\"\"\"\nimport json\nimport sys\nimport textwrap\nfrom pathlib import Path\n\nSRC = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_1/gen_art/gen_art_experiment_1\")\nOUT = Path(\"/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/\"\n           \"art_xp8BGBJZsxeI/code_demo.ipynb\")\nCFG = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}\n\nM = (SRC / \"method.py\").read_text().splitlines()\nLIN = (SRC / \"lineage.py\").read_text().splitlines()\nS0 = (SRC / \"s0.py\").read_text().splitlines()\n\n\ndef L(lines, a, b):  # 1-indexed inclusive\n    return \"\\n\".join(lines[a - 1:b])\n\n\ndef sub(text, old, new):\n    assert text.count(old) == 1, (old, text.count(old))\n    return text.replace(old, new)\n\n\ndef body(a, b):  # dedent a slice of main()'s body\n    return textwrap.dedent(L(M, a, b)).strip(\"\\n\")\n\n\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": textwrap.dedent(s).strip(\"\\n\")})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [],\n                  \"source\": s.strip(\"\\n\")})\n\n\n# ------------------------------------------------------------------ setup\nmd(\"\"\"\n# Does citing a concept \"as your own\" predict its spread? — the naturalisation-gap screen (candidate L)\n\nThis notebook is a runnable demo of the experiment script `method.py` (plus the helper modules it imports:\n`panel.py`, `s0.py`, `lineage.py`, `pool.py`, `screen.py`). The code is the original code, split into cells, with\nexplanations added between the sections.\n\n**What it tests.** Take a research concept (e.g. *compressed sensing*, *optogenetics*). Its early papers (years\nt0..t0+4) cite each other. When a paper from an *off-home* field j cites an earlier concept paper, is that parent\nmore likely to come from field j as well (the concept is being \"naturalised\" in j) than from the concept's home\nfield H? The candidate feature is **A\\\\*_h**, a *background-adjusted naturalisation gap*:\n\n1. **Stage 1.** For each concept × off-home field j, compute a year-stratified Mantel–Haenszel log odds ratio\n   (child in j vs H) × (parent in j vs H). Subtract the same log-OR computed on the *same children's background\n   reference lists*, which removes plain field homophily. Get a variance from a child bootstrap.\n2. **Stage 2.** Pool these ρ̂_cj with a crossed random-effects model fitted by REML (concept effect τ_c, cell effect\n   τ_cj). Then A\\\\*_h = Σ_j π_cj ρ\\\\*_cj.\n3. **Screen.** Does A\\\\*_h improve on the common 5-feature count baseline **B5** (early volume, growth, off-home\n   share, field entropy, number of fields)? The outcome is later field breadth **O2r**, evaluated under\n   leave-one-field-group-out (LOGO) ridge prediction. The pre-registered survival rule has four clauses:\n   Δρ ≥ 0.10 with CI low > 0, at least 3 of 4 groups positive, split-half reliability ≥ 0.6, and |ρ| with size ≤ 0.6.\n\n**Headline of the original full run (48 dev concepts): A\\\\*_h does NOT survive.** Δρ = −0.006, 90% CI\n[−0.034, 0.017]; 0 of 4 groups are positive; reliability is 0.58.\n\n**Demo data.** `mini_demo_data.json` holds the full S0 yearly-count file for all 78 panel concepts. It also holds\nthe Semantic Scholar concept papers, citation lineage and background references for **18 of the 48** dev concepts\n(all four field groups), trimmed to the keys the code reads. The other concepts follow the original\n\"not fetched\" drop path. With 18 concepts the numbers are noisier than the full run's. The final cell compares\nthem with the full-run reference values stored in the data file.\n\"\"\")\n\ncode(\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — NOT on Colab, always install\n_pip('loguru==0.7.3')\n\n# numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib — pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'scikit-learn==1.6.1', 'statsmodels==0.14.6',\n         'matplotlib==3.10.0')\n\"\"\" + CFG.get(\"pymc_install\", \"\"))\n\nmd(\"\"\"\n## Imports\n\nThis is the original import block of `method.py`. The five helper modules it imported (`lineage`, `panel`, `pool`,\n`s0`, `screen`) are defined inline in the cells below, each with its own import lines.\n\"\"\")\ncode(L(M, 19, 39) + \"\\nimport argparse  # notebook: config namespace replaces the CLI\\nimport matplotlib.pyplot as plt\")\n\nmd(\"## Data loading\\nThe data comes from GitHub, with a fallback to a local `mini_demo_data.json`.\")\ncode('''\nGITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n''')\ncode('''\ndata = load_data()\nprint(f\"{len(data['concepts'])} concepts with S2 lineage data:\", data[\"concept_names\"])\nprint(f\"S0 yearly counts for {len([k for k in data['s0_raw'] if not k.startswith('_')])} panel concepts\")\n''')\n\nmd(\"\"\"\n## Config\n\nThese values replace the original command-line arguments of `method.py`\n(`--max-concepts`, `--splits`, `--n-boot`, `--no-pymc`, `--no-glmm`, `--workers`).\nThe demo values are chosen to finish well inside 10 minutes. The original full-run values are in the comments.\n\"\"\")\ncode(CFG[\"config\"])\n\n# ------------------------------------------------------------------ helper modules\nmd(\"\"\"\n## Helper module `panel.py`: the frozen P78 panel\n\nThere are 78 concepts in 4 field groups. They are processed in an order seeded with 20260928.\n\"\"\")\ncode((SRC / \"panel.py\").read_text())\n\ns0_src = L(S0, 1, 16) + \"\\n\" + L(S0, 18, 22) + \"\\n\" + L(S0, 41, 82) + \"\\n\" + L(S0, 129, len(S0))\nmd(\"\"\"\n## Helper module `s0.py`: shared screen protocol S0\n\nThis module defines the onset t0 (first year with ≥ 20 papers), the *newborn* flag, the home field, the exact\nrarefied richness (Hurlbert 1971) used for the breadth outcome **O2r** (m = 30), Shannon entropy, and\n`compute_s0` for the OpenAlex topic-field version of S0.\n*Notebook change:* the OpenAlex API pull functions (`yearly`, `global_counts`, `field_counts`, `fetch_s0`) and\ntheir `oa` client import are left out. They only fetch raw data, and the demo loads that data from\n`mini_demo_data.json` instead.\n\"\"\")\ncode(s0_src)\n\nlin_src = \"\\n\".join(LIN)\nlin_src = sub(lin_src, 'ROOT = Path(__file__).resolve().parent\\n', '')\nlin_src = sub(lin_src, '''def load_raw(slug_: str) -> dict:\n    return json.loads(gzip.decompress((ROOT / \"results\" / \"concepts\" / slug_ / \"s2_raw.json.gz\").read_bytes()))''',\n              '''def load_raw(slug_: str) -> dict:\n    return data[\"concepts\"][slug_][\"s2_raw\"]  # notebook: from mini_demo_data.json (was results/concepts/<slug>/s2_raw.json.gz)''')\nmd(\"\"\"\n## Helper module `lineage.py`: concept lineage, stage-1 contrasts and foils\n\n- Each paper gets a **fractional field membership** over the 23 Semantic Scholar fields of study\n  (s2-fos-model, a title/abstract text classifier).\n- `build_lineage` keeps concept-paper → concept-paper citation links where the child is in t0..t0+4 and the\n  parent is 1–3 years older. Self-citations (shared author) are split off.\n- `stage1` builds the year-stratified MH log-OR for every off-home field j, for concept parents and for the\n  children's background references. ρ̂_cj is their difference. A multinomial child bootstrap gives the variance.\n- `foils` computes the comparison features (raw/background crude log-ORs, relay share, self share,\n  coverage, A_unif / A_imp, and R_away, the spectral radius of the cross-field link kernel).\n\"\"\")\ncode(lin_src)\n\nmd(\"\"\"\n## Helper module `pool.py`: stage 2 partial pooling\n\nThe model is y_k = x_k β + u_c(k) + w_k + e_k, with u ~ N(0, τ_c²), w ~ N(0, τ_cj²) and e ~ N(0, v_k).\nREML over (log τ_c, log τ_cj) is followed by Henderson's mixed-model equations. The fallback is\nDerSimonian–Laird. `fit_pymc` fits the same model with NUTS as a headline check.\n\"\"\")\ncode((SRC / \"pool.py\").read_text())\n\nmd(\"\"\"\n## Helper module `screen.py`: LOGO comparison of B5 vs B5 + candidate\n\n`compare` fits a ridge (for O2r) or a logistic model (for O1/O3/R_j) with leave-one-dev-group-out folds. It\ncompares out-of-fold Spearman ρ (or AUC) and bootstraps concepts (or clusters) on the fixed OOF pairs. It also\nreports per-group deltas and signs.\n\"\"\")\ncode((SRC / \"screen.py\").read_text())\n\n# ------------------------------------------------------------------ method.py definitions\nhdr = L(M, 41, 82)\nhdr = sub(hdr, 'ROOT = Path(__file__).resolve().parent', 'ROOT = Path(\".\").resolve()  # notebook: outputs go to ./results and ./logs')\nhdr = sub(hdr, '''sys.path.insert(0, str(ROOT))\n\nfrom lineage import (F, S2_DEV, S2_FIELDS, Concept, crude_lor, foils, load_concept, load_raw, membership,  # noqa: E402\n                     stage1)\nfrom panel import DEV_FIELDS, seeded_order, slug  # noqa: E402\nfrom pool import fit_dl, fit_pymc, fit_reml, predict, var_of  # noqa: E402\nfrom s0 import compute_s0, newborn, onset, rarefied_richness, shannon  # noqa: E402\nfrom screen import compare, rho, spearman_brown  # noqa: E402\n''', '# notebook: the helper modules (lineage, panel, pool, s0, screen) are defined in the cells above\\n')\nmd(\"\"\"\n## `method.py`: constants, logging, resource limits\n\nB5 is the count baseline. `PROBE_CRUDE` holds the crude values from an earlier probe, used for an agreement\ncheck. `BINS` are the off-home-children bins for the reliability-vs-n curve.\n\"\"\")\ncode(hdr)\n\ns0m = L(M, 85, 161)\ns0m = sub(s0m, '''    raw = json.loads((RES / \"s0_raw.json\").read_text())''',\n          '''    raw = data[\"s0_raw\"]  # notebook: from mini_demo_data.json (was results/s0_raw.json)''')\ns0m = sub(s0m, '''    p = RES / \"concepts\" / sl / \"bg.json.gz\"\n    n = len(c.child_idx)\n    B = np.zeros((n, F))\n    has = np.zeros(n, bool)\n    if not p.exists():\n        return B, has\n    d = json.loads(gzip.decompress(p.read_bytes()))''', '''    d = data[\"concepts\"].get(sl, {}).get(\"bg\")  # notebook: from mini_demo_data.json (was results/concepts/<slug>/bg.json.gz)\n    n = len(c.child_idx)\n    B = np.zeros((n, F))\n    has = np.zeros(n, bool)\n    if d is None:\n        return B, has''')\nmd(\"\"\"\n## S0 outcomes and baseline features\n\n- `count_outcomes` uses OpenAlex yearly counts to get t0, newborn, **O1** (uptake: the share of the literature\n  in t0+6..t0+8 is at least the share at t0+5), **O3** (transience) and the count parts of B5.\n- `s0_s2` uses the fractional S2 field labels to get the home field, **O2r** (rarefied venue-field breadth in\n  t0+6..t0+8), the field-based B5 terms, and the per-field retention units **R_j**.\n- `load_bg` loads each child's background references and turns them into a mean field-membership row.\n\"\"\")\ncode(s0m)\n\nmd(\"\"\"\n## Stage-2 wrapper, per-concept feature A\\\\*_h, and stage-1 units\n\n`concept_features` aggregates the pooled ρ\\\\*_cj into A\\\\*_h with child-mass weights π_cj. It also returns the\nposterior SD, the number of fields with Pr(ρ\\\\* > 0) > 0.8 (`n_nat_fields`), and `max_rho`.\n\"\"\")\ncode(L(M, 162, 224))\n\nmd(\"\"\"\n## Split-half reliability helpers\n\nEach split divides every concept's children into two halves, stratified on home vs off-home children. Stage 1\nand stage 2 are re-run on each half, and the Spearman ρ between the halves' A\\\\*_h is stepped up with\nSpearman–Brown. `reliability_vs_n` repeats this within bins of off-home children.\n\"\"\")\nrel_src = L(M, 225, 341)\ncode(rel_src)\n\nmd(\"\"\"\n## GLMM robustness check\n\nThis is a one-stage `BinomialBayesMixedGLM` (variational Bayes) on link-level rows, with discrete labels drawn\nfrom the fractional memberships.\n\"\"\")\ncode(L(M, 342, 398))\n\nfig_src = L(M, 750, 805)\nfig_src = sub(fig_src, '''    import matplotlib\n    matplotlib.use(\"Agg\")\n    import matplotlib.pyplot as plt\n''', '''    import matplotlib.pyplot as plt  # notebook: inline backend instead of matplotlib.use(\"Agg\")\n''')\nfig_src = sub(fig_src, '''fig.savefig(fig_dir / \"screen_overview.png\", dpi=130); plt.close(fig)''',\n              '''fig.savefig(fig_dir / \"screen_overview.png\", dpi=130); plt.show(); plt.close(fig)''')\nmd(\"\"\"\n## Output writers\n\n`write_method_out` writes `method_out.json` in the pipeline's exp_gen_sol_out format. `figures` draws the\nthree-panel overview. In the original script both are defined after `main()`; here they must be defined before\nthey are called.\n\"\"\")\ncode(fig_src)\n\n# ------------------------------------------------------------------ main() body, split into cells\nmd(\"\"\"\n# Running the screen: the body of `main()`, section by section\n\n### 1. Assemble the dev panel\n\nWalk the 78 concepts in seeded order. Drop a concept if its onset t0 is outside 2003–2009, if its home field is\nsealed (outside CS / Engineering / Biology / Medicine), or if its lineage data is not available (here: not in the\n18-concept demo subset). Build the S0 rows, the field-retention units and the `Concept` objects.\n\"\"\")\ns1 = body(410, 463)\ns1 = sub(s1, '''        p = RES / \"concepts\" / sl / \"s2_raw.json.gz\"\n        if not p.exists():''', '''        if sl not in data[\"concepts\"]:  # notebook: was the file check RES / \"concepts\" / sl / \"s2_raw.json.gz\"''')\ncode(s1)\n\nmd(\"\"\"\n### 2. Stage 1 (per concept × field MH contrasts) and stage 2 (REML pooling)\n\nThis step also builds the field-level table of ρ\\\\*_cj for every (concept, off-home field) unit, including units\nwith no stage-1 datum (those get the concept-level prediction).\n\"\"\")\ncode(body(465, 487))\n\nmd(\"### 3. Feature table: A\\\\*_h, its secondaries, and the foils for every concept\")\ncode(body(489, 502))\n\nrs = body(504, 521)\nrs = sub(rs, '''    pkl = RES / \"_concepts.pkl\"\n    pkl.write_bytes(pickle.dumps((concepts, bgs, names)))\n    t = time.time()\n    with ProcessPoolExecutor(max_workers=args.workers, mp_context=mp.get_context(\"spawn\"),\n                             initializer=_init_worker, initargs=(str(pkl),)) as ex:\n        split_res = list(ex.map(run_split, range(args.splits)))\n    pkl.unlink()\n''', '''    t = time.time()\n    # notebook: the original ran the splits in a spawn-based ProcessPoolExecutor (args.workers processes, data passed\n    # via a pickle file); spawned workers cannot import functions defined in a notebook, so they run in-process here.\n    _W[\"data\"] = (concepts, bgs, names)\n    split_res = list(map(run_split, range(args.splits)))\n''')\nmd(\"\"\"\n### 4. Split-half reliability, and the eligibility threshold\n\nThe eligibility floor is the lowest off-home-children bin from which every larger bin (with ≥ 4 concepts) reaches\nreliability 0.6. The default is 30. *Most of the notebook's runtime is spent here:* each split re-runs stages\n1 and 2 twice.\n\"\"\")\ncode(rs)\n\nmd(\"\"\"\n### 5. The screen: LOGO B5 vs B5 + A\\\\*_h\n\n- **Main test:** O2r, ridge, bootstrap CI and refit bootstrap.\n- O1 / O3 ΔAUC and the hurdle.\n- **Size checks:** |ρ| of A\\\\*_h with log early volume and growth.\n- Subsets (eligible, newborn-only, full parent sample) and the O2r m = 50 / m = 20 sensitivities.\n\"\"\")\ncode(body(523, 561))\n\nmd(\"\"\"\n### 6. Exploratory candidate table\n\nEach secondary and foil is scored as if it were the candidate, against the same B5 baseline.\n\"\"\")\ncode(body(562, 577))\n\nmd(\"\"\"\n### 7. Field-level test, the M1 mechanism check, probe agreement, and S0 cross-source validation\n\n- **Field level:** does ρ\\\\*_cj predict whether field j retains the concept (R_j) beyond field size, growth,\n  share and the background log-OR? The bootstrap is clustered by concept.\n- **M1:** how much of the raw lineage log-OR is explained by the background log-OR, i.e. by plain field\n  homophily?\n\"\"\")\ncode(body(578, 628))\n\npm_src = body(630, 671)\npm_src = sub(pm_src, \"idata, X_, cols_ = fit_pymc(y_, v_, cidx, len(names), fl_)\",\n             \"idata, X_, cols_ = fit_pymc(y_, v_, cidx, len(names), fl_, draws=args.pymc_draws, chains=args.pymc_chains)\")\nmd(\"\"\"\n### 8. Robustness: PyMC NUTS headline check and the one-stage GLMM\n\nBoth are wrapped in `try`, as in the original: a failure here never blocks the screen. PyMC runs only when\n`args.no_pymc` is False (see the config cell).\n\"\"\")\ncode(pm_src)\n\nmd(\"### 9. The pre-registered survival rule\")\ncode(body(673, 692))\n\nmd(\"\"\"\n### 10. Outputs\n\nThis step writes the CSVs, `screen_result.json`, `method_out.json` and the overview figure under `./results`.\nThe figure's three panels show A\\\\*_h vs O2r, the M1 scatter, and reliability vs n.\n\"\"\")\ncode(body(694, 747))\n\n# ------------------------------------------------------------------ results\nmd(\"\"\"\n## Results summary\n\nThe table below sets the demo's key statistics beside the reference values from the original full 48-concept run.\nThe plots show out-of-fold predictions and the exploratory candidate comparison.\n\"\"\")\ncode('''\nref = data[\"reference_full_run\"]\nrows = [(\"n dev concepts used\", screen_result[\"n_used\"], ref[\"n_used\"]),\n        (\"rho_B5 (LOGO OOF Spearman)\", screen_result[\"rho_B\"], ref[\"rho_B\"]),\n        (\"rho_B5+A*_h\", screen_result[\"rho_BC\"], ref[\"rho_BC\"]),\n        (\"Delta-rho\", screen_result[\"delta_rho\"], ref[\"delta_rho\"]),\n        (\"Delta-rho 90% CI low\", screen_result[\"ci90\"][0], ref[\"ci90\"][0]),\n        (\"Delta-rho 90% CI high\", screen_result[\"ci90\"][1], ref[\"ci90\"][1]),\n        (\"positive left-out groups\", screen_result[\"n_pos_groups\"], ref[\"n_pos_groups\"]),\n        (\"reliability A*_h (Spearman-Brown)\", (screen_result[\"reliability\"].get(\"A_h\") or {}).get(\"reliability_SB\"),\n         ref[\"reliability_A_h_SB\"]),\n        (\"|rho| with log early volume\", abs(screen_result[\"size_corr\"][\"vol\"]), abs(ref[\"size_corr\"][\"vol\"])),\n        (\"|rho| with early growth\", abs(screen_result[\"size_corr\"][\"growth\"]), abs(ref[\"size_corr\"][\"growth\"])),\n        (\"O1 Delta-AUC\", screen_result[\"delta_auc_O1\"][\"delta\"], ref[\"delta_auc_O1\"]),\n        (\"field-level Delta-AUC (R_j)\", (screen_result[\"field_level\"] or {}).get(\"delta\"), ref[\"field_level_delta\"]),\n        (\"M1 R^2 (raw vs background log-OR)\", (screen_result[\"M1\"] or {}).get(\"R2\"), ref[\"M1_R2\"]),\n        (\"REML tau_c\", screen_result[\"pooling\"][\"tau_c\"], ref[\"tau_c\"]),\n        (\"REML tau_cj\", screen_result[\"pooling\"][\"tau_cj\"], ref[\"tau_cj\"]),\n        (\"SURVIVES pre-registered rule\", screen_result[\"survives\"], ref[\"survives\"])]\nsummary = pd.DataFrame(rows, columns=[\"statistic\", \"demo (this run)\", \"full run (48 concepts)\"])\npd.set_option(\"display.width\", 140)\nprint(summary.to_string(index=False, float_format=lambda x: f\"{x:.3f}\"))\nprint(\"\\\\nClause results (demo):\")\nfor k, v in screen_result[\"clause_results\"].items():\n    print(f\"  {k:<40} pass={v['pass']}  value={v['value']}\")\nprint(\"\\\\nPer-group Delta-rho (demo):\")\nfor g, v in screen_result[\"per_group\"].items():\n    print(f\"  {g:<45} n={v['n']:>2}  delta={v['delta'] if v['delta'] is not None else float('nan'):+.3f}  sign={v['sign']}\")\n\nfig, ax = plt.subplots(1, 2, figsize=(14, 4.8))\nfor g, s_ in D.groupby(\"dev_group\"):\n    ax[0].scatter(s_[\"oof_B5\"], s_[\"O2r\"], marker=\"o\", label=f\"B5 — {g[:20]}\", alpha=.8)\n    ax[0].scatter(s_[\"oof_B5_plus_A_h\"], s_[\"O2r\"], marker=\"x\", color=ax[0].collections[-1].get_facecolor()[0], alpha=.8)\nax[0].set_xlabel(\"out-of-fold prediction (o = B5, x = B5 + A*_h)\"); ax[0].set_ylabel(\"observed O2r\")\nax[0].set_title(f\"LOGO ridge: rho_B5={screen_result['rho_B']:.3f}, rho_B5+A*_h={screen_result['rho_BC']:.3f}\")\nax[0].legend(fontsize=7)\nct = pd.DataFrame({k: {\"delta\": v[\"delta_rho\"], \"lo\": v[\"ci90\"][0], \"hi\": v[\"ci90\"][1]}\n                   for k, v in screen_result[\"candidate_comparison_table\"].items()}).T.sort_values(\"delta\")\nax[1].barh(ct.index, ct[\"delta\"], xerr=[ct[\"delta\"] - ct[\"lo\"], ct[\"hi\"] - ct[\"delta\"]], color=\"tab:gray\")\nax[1].axvline(0.10, color=\"r\", ls=\"--\", label=\"rule bar Delta-rho = 0.10\"); ax[1].axvline(0, color=\"k\", lw=.8)\nax[1].set_xlabel(\"Delta-rho over B5 (90% bootstrap CI)\"); ax[1].set_title(\"Exploratory candidates and foils\")\nax[1].legend(fontsize=8)\nfig.tight_layout(); plt.show()\n''')\n\nnb = {\"cells\": cells, \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                   \"language_info\": {\"name\": \"python\"}}, \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"cell-{i:02d}\"\nOUT.write_text(json.dumps(nb, indent=1))\nprint(\"cells:\", len(cells))\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [44] TOOL CALL — Bash · 2026-09-29 21:07:22 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad && sed -i 's/s0_src = L(S0, 1, 16) + "\\n" + L(S0, 18, 22)/s0_src = L(S0, 1, 16) + "\\n" + L(S0, 19, 22)/' build_nb.py && grep -n "s0_src =" build_nb.py && cat > cfg_min.py <<'EOF'
import json
config = '''# Original full-run values in comments (python method.py --splits 50 --n-boot 2000, ~4-5 min on 4 CPUs for 48 concepts)
MAX_CONCEPTS = 10**6   # original: 10**6 (no cap: every dev concept in the data)
SPLITS = 2             # original: 50 split-half replicates for reliability
N_BOOT = 50            # original: 2000 concept-bootstrap resamples for every Delta-rho / Delta-AUC CI
NO_PYMC = True         # original: False (PyMC NUTS headline check)
NO_GLMM = True         # original: False (one-stage BinomialBayesMixedGLM robustness check)
WORKERS = 1            # original: 4 (process pool); the notebook runs the splits in-process
PYMC_DRAWS = 1000      # original: 1000 draws (+1000 tune)
PYMC_CHAINS = 4        # original: 4 chains

args = argparse.Namespace(max_concepts=MAX_CONCEPTS, splits=SPLITS, n_boot=N_BOOT, no_pymc=NO_PYMC, no_glmm=NO_GLMM,
                          workers=WORKERS, pymc_draws=PYMC_DRAWS, pymc_chains=PYMC_CHAINS)
print(args)'''
print(json.dumps({"config": config}))
EOF
python3 build_nb.py "$(python3 cfg_min.py)"
```

### [45] TOOL RESULT — Bash [ERROR] · 2026-09-29 21:07:22 UTC

```
Error: Exit code 1
136:s0_src = L(S0, 1, 16) + "\n" + L(S0, 19, 22) + "\n" + L(S0, 41, 82) + "\n" + L(S0, 129, len(S0))
Traceback (most recent call last):
  File "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/build_nb.py", line 287, in <module>
    s1 = sub(s1, '''        p = RES / "concepts" / sl / "s2_raw.json.gz"
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/build_nb.py", line 23, in sub
    assert text.count(old) == 1, (old, text.count(old))
           ^^^^^^^^^^^^^^^^^^^^
AssertionError: ('        p = RES / "concepts" / sl / "s2_raw.json.gz"\n        if not p.exists():', 0)
```

### [46] TOOL CALL — Bash · 2026-09-29 21:07:30 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad && python3 - <<'EOF'
p='build_nb.py'; s=open(p).read()
s=s.replace("""'''        p = RES / "concepts" / sl / "s2_raw.json.gz"
        if not p.exists():''', '''        if sl not in data""","""'''    p = RES / "concepts" / sl / "s2_raw.json.gz"
    if not p.exists():''', '''    if sl not in data""")
open(p,'w').write(s)
EOF
python3 build_nb.py "$(python3 cfg_min.py)"
```

### [47] TOOL RESULT — Bash · 2026-09-29 21:07:30 UTC

```
{"stdout": "cells: 53", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] ASSISTANT · 2026-09-29 21:07:40 UTC

```
Notebook built (53 cells). First test run with minimum config in the clean venv:
```

### [49] TOOL CALL — Bash · 2026-09-29 21:07:40 UTC

```
E=/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run1.log 2>&1; echo "exit $? runtime $(( $(date +%s)-S ))s"; tail -30 /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run1.log
```

### [50] TOOL RESULT — Bash · 2026-09-29 21:08:46 UTC

```
{"stdout": "exit 1 runtime 42s\n\u001b[32m   1882\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mmode\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1883\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mencoding\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43moptions\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mget\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mencoding\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43;01mNone\u001b[39;49;00m\u001b[30;43m)\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1884\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mcompression\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43moptions\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mget\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mcompression\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43;01mNone\u001b[39;49;00m\u001b[30;43m)\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1885\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mmemory_map\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43moptions\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mget\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mmemory_map\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43;01mFalse\u001b[39;49;00m\u001b[30;43m)\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1886\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mis_text\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mis_text\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1887\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43merrors\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43moptions\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mget\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mencoding_errors\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mstrict\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m)\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1888\u001b[39m \u001b[30;43m    \u001b[39;49m\u001b[30;43mstorage_options\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mself\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43moptions\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mget\u001b[39;49m\u001b[30;43m(\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43mstorage_options\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\u001b[30;43m \u001b[39;49m\u001b[30;43;01mNone\u001b[39;49;00m\u001b[30;43m)\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m   1889\u001b[39m \u001b[30;43m\u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m   1890\u001b[39m \u001b[38;5;28;01massert\u001b[39;00m \u001b[38;5;28mself\u001b[39m.handles \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m\n\u001b[32m   1891\u001b[39m f = \u001b[38;5;28mself\u001b[39m.handles.handle\n\n\u001b[36mFile \u001b[39m\u001b[32m/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc/lib/python3.12/site-packages/pandas/io/common.py:873\u001b[39m, in \u001b[36mget_handle\u001b[39m\u001b[34m(path_or_buf, mode, encoding, compression, memory_map, is_text, errors, storage_options)\u001b[39m\n\u001b[32m    868\u001b[39m \u001b[38;5;28;01melif\u001b[39;00m \u001b[38;5;28misinstance\u001b[39m(handle, \u001b[38;5;28mstr\u001b[39m):\n\u001b[32m    869\u001b[39m     \u001b[38;5;66;03m# Check whether the filename is to be opened in binary mode.\u001b[39;00m\n\u001b[32m    870\u001b[39m     \u001b[38;5;66;03m# Binary mode does not support 'encoding' and 'newline'.\u001b[39;00m\n\u001b[32m    871\u001b[39m     \u001b[38;5;28;01mif\u001b[39;00m ioargs.encoding \u001b[38;5;129;01mand\u001b[39;00m \u001b[33m\"\u001b[39m\u001b[33mb\u001b[39m\u001b[33m\"\u001b[39m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;129;01min\u001b[39;00m ioargs.mode:\n\u001b[32m    872\u001b[39m         \u001b[38;5;66;03m# Encoding\u001b[39;00m\n\u001b[32m--> \u001b[39m\u001b[32m873\u001b[39m         handle = \u001b[30;43mopen\u001b[39;49m\u001b[30;43m(\u001b[39;49m\n\u001b[32m    874\u001b[39m \u001b[30;43m            \u001b[39;49m\u001b[30;43mhandle\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m    875\u001b[39m \u001b[30;43m            \u001b[39;49m\u001b[30;43mioargs\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mmode\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m    876\u001b[39m \u001b[30;43m            \u001b[39;49m\u001b[30;43mencoding\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43mioargs\u001b[39;49m\u001b[30;43m.\u001b[39;49m\u001b[30;43mencoding\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m    877\u001b[39m \u001b[30;43m            \u001b[39;49m\u001b[30;43merrors\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43merrors\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m    878\u001b[39m \u001b[30;43m            \u001b[39;49m\u001b[30;43mnewline\u001b[39;49m\u001b[30;43m=\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m\"\u001b[39;49m\u001b[30;43m,\u001b[39;49m\n\u001b[32m    879\u001b[39m \u001b[30;43m        \u001b[39;49m\u001b[30;43m)\u001b[39;49m\n\u001b[32m    880\u001b[39m     \u001b[38;5;28;01melse\u001b[39;00m:\n\u001b[32m    881\u001b[39m         \u001b[38;5;66;03m# Binary mode\u001b[39;00m\n\u001b[32m    882\u001b[39m         handle = \u001b[38;5;28mopen\u001b[39m(handle, ioargs.mode)\n\n\u001b[31mFileNotFoundError\u001b[39m: [Errno 2] No such file or directory: '/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI/logs/credits.csv'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-29 21:09:01 UTC

```
Fast (42 s). Only failure: the credit ledger CSV path. Fixing that substitution:
```

### [52] TOOL CALL — Bash · 2026-09-29 21:09:01 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad && python3 - <<'EOF'
p='build_nb.py'; s=open(p).read()
s=s.replace("""code(body(694, 747))""","""out_src = body(694, 747)
out_src = sub(out_src, 'credits = pd.read_csv(ROOT / "logs" / "credits.csv")',
              'credits = pd.DataFrame({"credits": data["credits"]})  # notebook: OpenAlex credit ledger column (was logs/credits.csv)')
code(out_src)""")
open(p,'w').write(s)
EOF
python3 build_nb.py "$(python3 cfg_min.py)" && cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI && E=/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run2.log 2>&1; echo "exit $? runtime $(( $(date +%s)-S ))s"; tail -5 /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run2.log
```

### [53] TOOL RESULT — Bash · 2026-09-29 21:09:43 UTC

```
{"stdout": "cells: 53\nexit 0 runtime 40s\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 305507 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-29 21:09:47 UTC

```
Passes at minimum config. Checking the outputs for sanity:
```

### [55] TOOL CALL — Bash · 2026-09-29 21:09:47 UTC

```
python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        t=o.get('text') or ''.join(o.get('data',{}).get('text/plain',''))
        if isinstance(t,list): t=''.join(t)
        if o.get('output_type')=='error' or 'Warning' in t or 'ERROR' in t or i>=14:
            print(i, o.get('output_type'), (t or str(o.get('data',{}).keys()))[-1500:])
EOF
```

### [56] TOOL RESULT — Bash · 2026-09-29 21:09:47 UTC

```
{"stdout": "32 stream 21:09:26|INFO   |S0: 11 dev concepts, 86 field units, 67 dropped\n\n32 stream 21:09:27|INFO   |dev concepts: 18; dropped: {'not_fetched (time/rate budget)': 35, 't0_out_of_dev': 22, 'home_sealed': 3}\n\n34 stream 21:09:28|INFO   |stage 1: 50 concept x field cells with data (1s)\n\n34 stream 21:09:28|INFO   |REML: tau_c=0.001 tau_cj=0.548 beta=[ 0.128 -0.473 -0.604 -0.219] boundary=True\n\n38 stream 21:09:28|INFO   |REML: tau_c=0.001 tau_cj=0.180 beta=[ 0.106 -0.319 -0.242 -0.156] boundary=True\n\n38 stream 21:09:29|INFO   |REML: tau_c=0.001 tau_cj=0.382 beta=[-0.052 -0.207 -0.2  ] boundary=True\n\n38 stream 21:09:29|INFO   |REML: tau_c=0.292 tau_cj=0.320 beta=[ 0.004 -0.325 -0.21 ] boundary=False\n\n38 stream 21:09:30|INFO   |REML: tau_c=0.130 tau_cj=0.001 beta=[-0.159 -0.118  0.074] boundary=True\n\n38 stream 21:09:30|INFO   |reliability (2 splits, 2s): {'A_h': 0.5909090909090908, 'A_h_u': -0.01680672268907568, 'max_rho': 0.4242424242424242, 'n_nat_fields': 0.48799690161998455, 'bg_LOR': 0.9250292260930559, 'A_h_crude': -1.026315789473684, 'A_h_MH': 0.9444444444444444, 'rho_star_field': 0.2606914155210246}\n\n40 stream 21:09:31|INFO   |O2r Delta-rho = 0.033 CI90 [0.   0.12] (rho_B=0.874, rho_BC=0.907, n=18)\n\n50 display_data <Figure size 1500x450 with 3 Axes>\n50 stream 21:09:39|INFO   |SURVIVES=False clauses={'delta_rho_ge_0.10_and_ci_low_gt_0': False, 'positive_groups_ge_3_of_4': False, 'reliability_ge_0.6': False, 'size_abs_rho_le_0.6': True} runtime 13s\n\n52 stream 90% CI high           0.120                  0.017\n         positive left-out groups               2                      0\nreliability A*_h (Spearman-Brown)           0.591                  0.584\n      |rho| with log early volume           0.356                  0.145\n          |rho| with early growth           0.154                  0.177\n                     O1 Delta-AUC          -0.014                 -0.026\n      field-level Delta-AUC (R_j)           0.016                  0.002\nM1 R^2 (raw vs background log-OR)           0.638                  0.659\n                       REML tau_c           0.001                  0.294\n                      REML tau_cj           0.548                  0.648\n     SURVIVES pre-registered rule           False                  False\n\nClause results (demo):\n  delta_rho_ge_0.10_and_ci_low_gt_0        pass=False  value=[0.03302373581011364, [0.0, 0.12024075041599519]]\n  positive_groups_ge_3_of_4                pass=False  value=2\n  reliability_ge_0.6                       pass=False  value=0.5909090909090908\n  size_abs_rho_le_0.6                      pass=True  value=[0.3560371517027864, -0.15376676986584106]\n\nPer-group Delta-rho (demo):\n  Biochemistry, Genetics and Molecular Biology  n= 5  delta=-0.100  sign=-\n  Computer Science                              n= 6  delta=+0.057  sign=+\n  Engineering                                   n= 2  delta=+nan  sign=insufficient\n  Medicine                                      n= 5  delta=+0.100  sign=+\n\n52 display_data <Figure size 1400x480 with 2 Axes>", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] ASSISTANT · 2026-09-29 21:09:53 UTC

```
Min config works (method runtime 13 s). Scaling: next round turns on the original splits/bootstraps, the GLMM, and PyMC. Checking which pymc version resolves against Colab's numpy/scipy:
```

### [58] TOOL CALL — Bash · 2026-09-29 21:09:53 UTC

```
cd /tmp && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip compile --python-version 3.12 - <<'EOF' 2>&1 | grep -iE "^(pymc|pytensor|numpy|scipy|arviz|pandas)==|error" 
pymc
numpy==2.0.2
scipy==1.16.3
pandas==2.2.2
matplotlib==3.10.0
EOF
```

### [59] TOOL RESULT — Bash · 2026-09-29 21:09:53 UTC

```
{"stdout": "arviz==1.3.0\nnumpy==2.0.2\npandas==2.2.2\npymc==6.3.2\npytensor==3.3.2\nscipy==1.16.3", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] ASSISTANT · 2026-09-29 21:10:13 UTC

```
pymc 6.3.2 (the version the original used) resolves against Colab's numpy 2.0.2. Round 2 uses the original full values:
```

### [61] TOOL CALL — Bash · 2026-09-29 21:10:13 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad && cat > cfg_full.py <<'EOF'
import json
config = '''# Demo values; the original full-run values (python method.py --splits 50 --n-boot 2000) are in the comments.
MAX_CONCEPTS = 10**6   # original: 10**6 (no cap: every dev concept in the data)
SPLITS = 50            # original: 50 split-half replicates for reliability
N_BOOT = 2000          # original: 2000 concept-bootstrap resamples for every Delta-rho / Delta-AUC CI
NO_PYMC = False        # original: False (PyMC NUTS headline check; set True to skip it and save time)
NO_GLMM = False        # original: False (one-stage BinomialBayesMixedGLM robustness check)
WORKERS = 1            # original: 4 (process pool); the notebook runs the splits in-process
PYMC_DRAWS = 1000      # original: 1000 draws (+1000 tune)
PYMC_CHAINS = 4        # original: 4 chains

args = argparse.Namespace(max_concepts=MAX_CONCEPTS, splits=SPLITS, n_boot=N_BOOT, no_pymc=NO_PYMC, no_glmm=NO_GLMM,
                          workers=WORKERS, pymc_draws=PYMC_DRAWS, pymc_chains=PYMC_CHAINS)
print(args)'''
pymc_install = '''
# pymc — used only by the optional PyMC NUTS check (config NO_PYMC); Colab usually ships it, install only if missing
try:
    import pymc  # noqa: F401
except ImportError:
    _pip('pymc==6.3.2')'''
print(json.dumps({"config": config, "pymc_install": pymc_install}))
EOF
python3 build_nb.py "$(python3 cfg_full.py)" && cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI && E=/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run3.log 2>&1; echo "exit $? runtime $(( $(date +%s)-S ))s"; tail -3 /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run3.log
```

### [62] TOOL RESULT — Bash · 2026-09-29 21:12:47 UTC

```
{"stdout": "cells: 53\nexit 0 runtime 152s\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 326041 bytes to code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] ASSISTANT · 2026-09-29 21:12:51 UTC

```
The full original parameters finish in 152 s, well under the 600 s budget. Checking whether the PyMC and GLMM checks actually ran rather than silently erroring:
```

### [64] TOOL CALL — Bash · 2026-09-29 21:12:51 UTC

```
python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code' or i<30: continue
    for o in c['outputs']:
        t=o.get('text') or ''
        if isinstance(t,list): t=''.join(t)
        if o.get('output_type')=='error': print(i,'ERROR',o['ename'],o['evalue'])
        elif t: print(i, t[-900:])
EOF
python3 -c "
import json;r=json.load(open('results/screen_result.json'));print(r['pymc_check']);print(r['glmm_check']);print(r['runtime_s'])"
```

### [65] TOOL RESULT — Bash · 2026-09-29 21:12:51 UTC

```
{"stdout": "32 21:10:54|INFO   |S0: 11 dev concepts, 86 field units, 67 dropped\n\n32 21:10:55|INFO   |dev concepts: 18; dropped: {'not_fetched (time/rate budget)': 35, 't0_out_of_dev': 22, 'home_sealed': 3}\n\n34 21:10:56|INFO   |stage 1: 50 concept x field cells with data (1s)\n\n34 21:10:56|INFO   |REML: tau_c=0.001 tau_cj=0.548 beta=[ 0.128 -0.473 -0.604 -0.219] boundary=True\n\n38 21:10:56|INFO   |REML: tau_c=0.001 tau_cj=0.180 beta=[ 0.106 -0.319 -0.242 -0.156] boundary=True\n\n38 21:10:57|INFO   |REML: tau_c=0.001 tau_cj=0.382 beta=[-0.052 -0.207 -0.2  ] boundary=True\n\n38 21:10:57|INFO   |REML: tau_c=0.292 tau_cj=0.320 beta=[ 0.004 -0.325 -0.21 ] boundary=False\n\n38 21:10:58|INFO   |REML: tau_c=0.130 tau_cj=0.001 beta=[-0.159 -0.118  0.074] boundary=True\n\n38 21:10:58|INFO   |REML: tau_c=0.001 tau_cj=0.333 beta=[-0.001 -0.062 -0.284 -0.187] boundary=True\n\n38 21:10:58|INFO   |REML: tau_c=0.095 tau_cj=0.053 beta=[-0.087 -0.376  0.002] boundary=False\n\n38 21:10:59|INFO   |REML: tau_c=0.092 tau_cj=0.219 beta=[ 0.045 -0.387 -0.14 ] boundary=False\n\n38 21:10:59|INFO   |REML: tau_c=0.074 tau_cj=0.156 beta=[-0.099 -0.106 -0.003] boundary=False\n\n38 21:11:00|INFO   |REML: tau_c=0.106 tau_cj=0.452 beta=[ 0.081 -0.459 -0.075] boundary=False\n\n38 21:11:00|INFO   |REML: tau_c=0.203 tau_cj=0.001 beta=[-0.139  0.019  0.017] boundary=True\n\n38 21:11:01|INFO   |REML: tau_c=0.001 tau_cj=0.221 beta=[-0.071 -0.114 -0.025] boundary=True\n\n38 21:11:01|INFO   |REML: tau_c=0.001 tau_cj=0.064 beta=[-0.031 -0.209 -0.097] boundary=True\n\n38 21:11:01|INFO   |REML: tau_c=0.172 tau_cj=0.001 beta=[-0.05  -0.334  0.027] boundary=True\n\n38 21:11:02|INFO   |REML: tau_c=0.001 tau_cj=0.243 beta=[ 0.036 -0.247 -0.276] boundary=True\n\n38 21:11:02|INFO   |REML: tau_c=0.001 tau_cj=0.111 beta=[-0.05  -0.235 -0.076] boundary=True\n\n38 21:11:03|INFO   |REML: tau_c=0.104 tau_cj=0.001 beta=[-0.062 -0.143 -0.1  ] boundary=True\n\n38 21:11:03|INFO   |REML: tau_c=0.001 tau_cj=0.136 beta=[-0.002 -0.378 -0.199] boundary=True\n\n38 21:11:04|INFO   |REML: tau_c=0.077 tau_cj=0.083 beta=[-0.032 -0.025 -0.145 -0.001] boundary=False\n\n38 21:11:04|INFO   |REML: tau_c=0.072 tau_cj=0.137 beta=[-0.14  -0.227 -0.01 ] boundary=False\n\n38 21:11:05|INFO   |REML: tau_c=0.034 tau_cj=0.442 beta=[ 0.139 -0.296 -0.345] boundary=False\n\n38 21:11:05|INFO   |REML: tau_c=0.001 tau_cj=0.715 beta=[ 0.14  -0.534 -0.15 ] boundary=True\n\n38 21:11:05|INFO   |REML: tau_c=0.209 tau_cj=0.099 beta=[ 0.07  -0.198 -0.185] boundary=False\n\n38 21:11:06|INFO   |REML: tau_c=0.162 tau_cj=0.001 beta=[-0.162 -0.307  0.194  0.127] boundary=True\n\n38 21:11:06|INFO   |REML: tau_c=0.172 tau_cj=0.604 beta=[ 0.171 -0.272 -0.293] boundary=False\n\n38 21:11:07|INFO   |REML: tau_c=0.281 tau_cj=0.209 beta=[-0.049 -0.201 -0.122] boundary=False\n\n38 21:11:07|INFO   |REML: tau_c=0.001 tau_cj=0.371 beta=[-0.021 -0.261  0.011] boundary=True\n\n38 21:11:08|INFO   |REML: tau_c=0.001 tau_cj=0.319 beta=[ 0.107 -0.403 -0.373] boundary=True\n\n38 21:11:08|INFO   |REML: tau_c=0.001 tau_cj=0.475 beta=[-0.052 -0.112  0.005] boundary=True\n\n38 21:11:09|INFO   |REML: tau_c=0.001 tau_cj=0.100 beta=[ 0.016 -0.145 -0.15  -0.141] boundary=True\n\n38 21:11:09|INFO   |REML: tau_c=0.001 tau_cj=0.465 beta=[ 0.151 -0.517  0.006] boundary=True\n\n38 21:11:09|INFO   |REML: tau_c=0.001 tau_cj=0.190 beta=[-0.051 -0.153  0.006] boundary=True\n\n38 21:11:10|INFO   |REML: tau_c=0.001 tau_cj=0.354 beta=[ 0.111 -0.404 -0.405] boundary=True\n\n38 21:11:10|INFO   |REML: tau_c=0.064 tau_cj=0.001 beta=[-0.012 -0.398 -0.062] boundary=True\n\n38 21:11:11|INFO   |REML: tau_c=0.130 tau_cj=0.366 beta=[-0.036 -0.088 -0.16 ] boundary=False\n\n38 21:11:11|INFO   |REML: tau_c=0.001 tau_cj=0.377 beta=[-0.016 -0.261 -0.207] boundary=True\n\n38 21:11:12|INFO   |REML: tau_c=0.001 tau_cj=0.576 beta=[ 0.115 -0.399 -0.265 -0.533] boundary=True\n\n38 21:11:12|INFO   |REML: tau_c=0.001 tau_cj=0.344 beta=[ 0.028 -0.2   -0.101] boundary=True\n\n38 21:11:13|INFO   |REML: tau_c=0.139 tau_cj=0.164 beta=[-0.035 -0.297 -0.187] boundary=False\n\n38 21:11:13|INFO   |REML: tau_c=0.081 tau_cj=0.171 beta=[ 0.032 -0.232 -0.117] boundary=False\n\n38 21:11:13|INFO   |REML: tau_c=0.001 tau_cj=0.404 beta=[ 0.037 -0.432 -0.106] boundary=True\n\n38 21:11:14|INFO   |REML: tau_c=0.001 tau_cj=0.153 beta=[-0.    -0.298 -0.16 ] boundary=True\n\n38 21:11:14|INFO   |REML: tau_c=0.059 tau_cj=0.099 beta=[-0.077 -0.152  0.039] boundary=False\n\n38 21:11:15|INFO   |REML: tau_c=0.199 tau_cj=0.343 beta=[ 0.04  -0.306  0.011] boundary=False\n\n38 21:11:15|INFO   |REML: tau_c=0.202 tau_cj=0.171 beta=[-0.033 -0.138 -0.054] boundary=False\n\n38 21:11:16|INFO   |REML: tau_c=0.001 tau_cj=0.342 beta=[-0.082 -0.062] boundary=True\n\n38 21:11:16|INFO   |REML: tau_c=0.119 tau_cj=0.119 beta=[-0.093 -0.082 -0.031] boundary=False\n\n38 21:11:17|INFO   |REML: tau_c=0.001 tau_cj=0.347 beta=[ 0.057 -0.382 -0.274] boundary=True\n\n38 21:11:17|INFO   |REML: tau_c=0.001 tau_cj=0.122 beta=[-0.025 -0.178 -0.09 ] boundary=True\n\n38 21:11:17|INFO   |REML: tau_c=0.086 tau_cj=0.001 beta=[ 0.037 -0.343 -0.121] boundary=True\n\n38 21:11:18|INFO   |REML: tau_c=0.001 tau_cj=0.697 beta=[ 0.104 -0.422 -0.199] boundary=True\n\n38 21:11:18|INFO   |REML: tau_c=0.001 tau_cj=0.291 beta=[ 0.102 -0.328 -0.24  -0.151] boundary=True\n\n38 21:11:19|INFO   |REML: tau_c=0.001 tau_cj=0.237 beta=[ 0.03  -0.34  -0.198] boundary=True\n\n38 21:11:19|INFO   |REML: tau_c=0.001 tau_cj=0.393 beta=[-0.046 -0.168 -0.06 ] boundary=True\n\n38 21:11:20|INFO   |REML: tau_c=0.001 tau_cj=0.347 beta=[ 0.09  -0.413 -0.169] boundary=True\n\n38 21:11:20|INFO   |REML: tau_c=0.192 tau_cj=0.556 beta=[ 0.121 -0.396 -0.379] boundary=False\n\n38 21:11:21|INFO   |REML: tau_c=0.031 tau_cj=0.100 beta=[-0.019 -0.172 -0.155] boundary=False\n\n38 21:11:21|INFO   |REML: tau_c=0.001 tau_cj=0.391 beta=[ 0.054 -0.202 -0.314 -0.027] boundary=True\n\n38 21:11:21|INFO   |REML: tau_c=0.095 tau_cj=0.001 beta=[-0.071 -0.25  -0.096] boundary=True\n\n38 21:11:22|INFO   |REML: tau_c=0.001 tau_cj=0.415 beta=[ 0.013 -0.276 -0.187] boundary=True\n\n38 21:11:22|INFO   |REML: tau_c=0.001 tau_cj=0.168 beta=[ 0.029 -0.267 -0.204] boundary=True\n\n38 21:11:23|INFO   |REML: tau_c=0.001 tau_cj=0.108 beta=[-0.063 -0.131 -0.076] boundary=True\n\n38 21:11:23|INFO   |REML: tau_c=0.001 tau_cj=0.471 beta=[ 0.14  -0.376 -0.51  -0.372] boundary=True\n\n38 21:11:24|INFO   |REML: tau_c=0.098 tau_cj=0.001 beta=[-0.075  0.014 -0.075] boundary=True\n\n38 21:11:24|INFO   |REML: tau_c=0.230 tau_cj=0.210 beta=[ 0.02  -0.466 -0.086] boundary=False\n\n38 21:11:25|INFO   |REML: tau_c=0.001 tau_cj=0.040 beta=[-0.046  0.03  -0.115] boundary=True\n\n38 21:11:25|INFO   |REML: tau_c=0.126 tau_cj=0.001 beta=[-0.066 -0.262 -0.095] boundary=True\n\n38 21:11:25|INFO   |REML: tau_c=0.001 tau_cj=0.233 beta=[-0.08  -0.145 -0.08   0.029] boundary=True\n\n38 21:11:26|INFO   |REML: tau_c=0.001 tau_cj=0.407 beta=[ 0.043 -0.5   -0.247] boundary=True\n\n38 21:11:26|INFO   |REML: tau_c=0.001 tau_cj=0.131 beta=[-0.004 -0.093 -0.168] boundary=True\n\n38 21:11:27|INFO   |REML: tau_c=0.357 tau_cj=0.179 beta=[-0.018 -0.383 -0.046] boundary=False\n\n38 21:11:27|INFO   |REML: tau_c=0.001 tau_cj=0.331 beta=[ 0.073 -0.394 -0.319] boundary=True\n\n38 21:11:28|INFO   |REML: tau_c=0.108 tau_cj=0.105 beta=[-0.143 -0.081  0.04 ] boundary=False\n\n38 21:11:28|INFO   |REML: tau_c=0.001 tau_cj=0.308 beta=[ 0.013 -0.339 -0.197] boundary=True\n\n38 21:11:28|INFO   |REML: tau_c=0.001 tau_cj=0.163 beta=[-0.009 -0.096 -0.12 ] boundary=True\n\n38 21:11:29|INFO   |REML: tau_c=0.001 tau_cj=0.001 beta=[-0.063 -0.281 -0.04  -0.067] boundary=True\n\n38 21:11:29|INFO   |REML: tau_c=0.001 tau_cj=0.296 beta=[ 0.03  -0.21  -0.237] boundary=True\n\n38 21:11:30|INFO   |REML: tau_c=0.001 tau_cj=0.337 beta=[ 0.106 -0.451 -0.313 -0.295] boundary=True\n\n38 21:11:30|INFO   |REML: tau_c=0.001 tau_cj=0.243 beta=[-0.018 -0.163 -0.157] boundary=True\n\n38 21:11:31|INFO   |REML: tau_c=0.001 tau_cj=0.390 beta=[ 0.071 -0.375 -0.254] boundary=True\n\n38 21:11:31|INFO   |REML: tau_c=0.001 tau_cj=0.198 beta=[-0.047 -0.194 -0.097] boundary=True\n\n38 21:11:32|INFO   |REML: tau_c=0.001 tau_cj=0.490 beta=[ 0.09  -0.323 -0.374] boundary=True\n\n38 21:11:32|INFO   |REML: tau_c=0.097 tau_cj=0.001 beta=[-0.087 -0.25   0.04 ] boundary=True\n\n38 21:11:32|INFO   |REML: tau_c=0.153 tau_cj=0.001 beta=[-0.154 -0.044 -0.016] boundary=True\n\n38 21:11:33|INFO   |REML: tau_c=0.001 tau_cj=0.355 beta=[ 0.171 -0.441 -0.319 -0.361] boundary=True\n\n38 21:11:33|INFO   |REML: tau_c=0.163 tau_cj=0.001 beta=[-0.155 -0.149  0.156  0.077] boundary=True\n\n38 21:11:34|INFO   |REML: tau_c=0.001 tau_cj=0.241 beta=[-0.03  -0.249 -0.141] boundary=True\n\n38 21:11:34|INFO   |REML: tau_c=0.215 tau_cj=0.087 beta=[-0.086 -0.205 -0.118] boundary=False\n\n38 21:11:35|INFO   |REML: tau_c=0.001 tau_cj=0.284 beta=[-0.053 -0.239 -0.044  0.067] boundary=True\n\n38 21:11:35|INFO   |REML: tau_c=0.001 tau_cj=0.487 beta=[ 0.096 -0.403 -0.101] boundary=True\n\n38 21:11:35|INFO   |REML: tau_c=0.121 tau_cj=0.073 beta=[-0.07  -0.169 -0.077] boundary=False\n\n38 21:11:36|INFO   |REML: tau_c=0.001 tau_cj=0.395 beta=[ 0.02  -0.329 -0.346 -0.006] boundary=True\n\n38 21:11:36|INFO   |REML: tau_c=0.001 tau_cj=0.290 beta=[ 0.069 -0.496 -0.265] boundary=True\n\n38 21:11:37|INFO   |REML: tau_c=0.206 tau_cj=0.001 beta=[-0.096 -0.066  0.055] boundary=True\n\n38 21:11:37|INFO   |REML: tau_c=0.001 tau_cj=0.265 beta=[ 0.059 -0.434 -0.327] boundary=True\n\n38 21:11:38|INFO   |REML: tau_c=0.001 tau_cj=0.001 beta=[-0.067 -0.149  0.082 -0.089] boundary=True\n\n38 21:11:38|INFO   |REML: tau_c=0.184 tau_cj=0.001 beta=[-0.053 -0.299  0.028] boundary=True\n\n38 21:11:39|INFO   |REML: tau_c=0.001 tau_cj=0.307 beta=[ 0.148 -0.373 -0.261] boundary=True\n\n38 21:11:39|INFO   |REML: tau_c=0.001 tau_cj=0.456 beta=[-0.022 -0.323 -0.131] boundary=True\n\n38 21:11:39|INFO   |REML: tau_c=0.001 tau_cj=0.464 beta=[ 0.098 -0.344 -0.358] boundary=True\n\n38 21:11:40|INFO   |REML: tau_c=0.189 tau_cj=0.099 beta=[-0.054 -0.141 -0.089] boundary=False\n\n38 21:11:40|INFO   |reliability (50 splits, 44s): {'A_h': 0.6734577788912154, 'A_h_u': 0.20495746083981378, 'max_rho': 0.6039711784603424, 'n_nat_fields': 0.3198114305653949, 'bg_LOR': 0.9104256639507892, 'A_h_crude': -1.6867164122427272, 'A_h_MH': 0.5221860011333695, 'rho_star_field': 0.3814365514074985}\n\n40 21:11:42|INFO   |O2r Delta-rho = 0.033 CI90 [-0.019  0.139] (rho_B=0.874, rho_BC=0.907, n=18)\n\n46 NUTS[nutpie]: [beta, tau_c, tau_cj, zc, zk]\n\n46 21:12:12|WARNING|nutpie unavailable (ImportError('nutpie not found. Install it with conda install -c conda-forge nutpie')); using the PyMC NUTS sampler\n\n46 Initializing NUTS using jitter+adapt_diag...\n\n46 Multiprocess sampling (4 chains in 4 jobs)\n\n46 NUTS: [beta, tau_c, tau_cj, zc, zk]\n\n46 Sampling 4 chains for 1_000 tune and 1_000 draw iterations (4_000 + 4_000 draws total) took 12 seconds.\n\n46 There was 1 divergence after tuning. Increase `target_accept` or reparameterize.\n\n46 21:12:32|INFO   |PyMC check: {'max_rhat': 1.00328774743095, 'spearman_vs_reml': 0.9926470588235295, 'tau_c_mean': 0.1293419812006177, 'tau_cj_mean': 0.5568679658660662, 'seconds': 20.019259691238403, 'divergences': 1, 'pass': True}\n\n46 21:12:42|INFO   |GLMM: 13667 rows, 132 strata, 9s, fixed cx=-0.594\n\n50 21:12:42|INFO   |SURVIVES=False clauses={'delta_rho_ge_0.10_and_ci_low_gt_0': False, 'positive_groups_ge_3_of_4': False, 'reliability_ge_0.6': True, 'size_abs_rho_le_0.6': True} runtime 108s\n\n52             0.294\n                      REML tau_cj           0.548                  0.648\n     SURVIVES pre-registered rule           False                  False\n\nClause results (demo):\n  delta_rho_ge_0.10_and_ci_low_gt_0        pass=False  value=[0.03302373581011364, [-0.018751957202505463, 0.13856363676110525]]\n  positive_groups_ge_3_of_4                pass=False  value=2\n  reliability_ge_0.6                       pass=True  value=0.6734577788912154\n  size_abs_rho_le_0.6                      pass=True  value=[0.3560371517027864, -0.15376676986584106]\n\nPer-group Delta-rho (demo):\n  Biochemistry, Genetics and Molecular Biology  n= 5  delta=-0.100  sign=-\n  Computer Science                              n= 6  delta=+0.057  sign=+\n  Engineering                                   n= 2  delta=+nan  sign=insufficient\n  Medicine                                      n= 5  delta=+0.100  sign=+\n\n{'max_rhat': 1.00328774743095, 'spearman_vs_reml': 0.9926470588235295, 'tau_c_mean': 0.1293419812006177, 'tau_cj_mean': 0.5568679658660662, 'seconds': 20.019259691238403, 'divergences': 1, 'pass': True}\n{'n_rows': 13667, 'fixed_cx': -0.5938644776301134, 'seconds': 9.475276947021484, 'spearman_vs_primary': 0.27554179566563464}\n107.27953958511353", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [66] THINKING · 2026-09-29 21:13:09 UTC

```
Full-scale run completed successfully (50 splits, 2000 bootstraps, PyMC, GLMM) in 152s with no need for reduced demo values. I'll update the config markdown to reflect this and rebuild for a final verification run.
```

### [67] TOOL CALL — Bash · 2026-09-29 21:13:09 UTC

```
cd /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad && python3 - <<'EOF'
p='build_nb.py'; s=open(p).read()
old='''The demo values are chosen to finish well inside 10 minutes. The original full-run values are in the comments.'''
new='''On the 18-concept demo subset, the **original full-run values** (50 splits, 2000 bootstraps, PyMC and GLMM
checks on) finish in about 2 minutes of compute, plus about 1 minute for the install. For a quicker look, lower
`SPLITS` / `N_BOOT` or set `NO_PYMC = True`.'''
assert s.count(old)==1; s=s.replace(old,new); open(p,'w').write(s)
EOF
sed -i 's/^config = .# Demo values; the original full-run values (python method.py --splits 50 --n-boot 2000) are in the comments./config = '"'''"'# Original full-run values: python method.py --splits 50 --n-boot 2000 (all flags at their defaults)/' cfg_full.py; head -3 cfg_full.py
python3 build_nb.py "$(python3 cfg_full.py)" && cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_xp8BGBJZsxeI && rm -rf results logs method_out.json && E=/tmp/aii_nb_test_envs/art_xp8BGBJZsxeI-ffbc98f770cc && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb > /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/run4.log 2>&1; echo "exit $? runtime $(( $(date +%s)-S ))s"; grep -c '"output_type": "error"' code_demo.ipynb; ls; du -sh *
```

### [68] TOOL RESULT — Bash · 2026-09-29 21:15:43 UTC

```
{"stdout": "import json\nconfig = '''# Demo values; the original full-run values (python method.py --splits 50 --n-boot 2000) are in the comments.\nMAX_CONCEPTS = 10**6   # original: 10**6 (no cap: every dev concept in the data)\ncells: 53\nexit 0 runtime 152s\n0\ncode_demo.ipynb\nlogs\nmake_mini_data.py\nmethod_out.json\nmini_demo_data.json\nresults\n319K\tcode_demo.ipynb\n994K\tlogs\n4.0K\tmake_mini_data.py\n70K\tmethod_out.json\n24M\tmini_demo_data.json\n2.1M\tresults", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [69] ASSISTANT · 2026-09-29 21:15:53 UTC

```
The final run passed with 0 error outputs in 152 s. One cosmetic fix: the config comment still says "Demo values". It's a comment-only change, so I'll patch it in place without re-executing.
```

### [70] TOOL CALL — Bash · 2026-09-29 21:15:53 UTC

```
python3 - <<'EOF'
import json
old="# Demo values; the original full-run values (python method.py --splits 50 --n-boot 2000) are in the comments."
new="# Original full-run values: python method.py --splits 50 --n-boot 2000 (all other flags at their defaults)"
for p in ["code_demo.ipynb","/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-xp8BGBJZsxeI/49262d42-e371-4418-8dfb-948fc98da6d1/scratchpad/cfg_full.py"]:
    s=open(p).read(); assert s.count(old)==1, p; open(p,'w').write(s.replace(old,new))
nb=json.load(open("code_demo.ipynb")); print(len(nb["cells"]))
EOF
grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-1/experiment-1/demo/mini_demo_data.json\\"' code_demo.ipynb; du -sh logs/* results/* | sort -h | tail -4; rm -rf logs results method_out.json; ls -a
```

### [71] TOOL RESULT — Bash · 2026-09-29 21:15:55 UTC

```
{"stdout": "53\n1\n14K\tresults/field_outcomes.csv\n15K\tlogs/method.log\n26K\tresults/screen_result.json\n1.1M\tresults/figures\n.\n..\n.aii\n.aii_claude_session.json\n.repl_agent.ptylog\ncode_demo.ipynb\nmake_mini_data.py\nmini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [72] ASSISTANT · 2026-09-29 21:16:15 UTC

```
Last step: README and manifest. The only large file is `mini_demo_data.json` (24 MB). It is text/JSON, so it needs no manifest decision, and the manifest's entry list stays empty.
```

### [73] TOOL CALL — Bash · 2026-09-29 21:16:15 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy needs a decision: the only large file, mini_demo_data.json (~24 MB), is JSON text and is kept
# and published (it is the data the notebook loads). No caches, venvs or binaries are left in this folder.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: does citing a concept "as your own" predict its spread? (naturalisation-gap screen, candidate L)

This is a runnable Colab/Jupyter demo of the experiment script `method.py` and the five helper modules it imports
(`panel.py`, `s0.py`, `lineage.py`, `pool.py`, `screen.py`). The screen tests one candidate feature,
**A\*_h**. It is a background-adjusted, field-stratified, partially pooled lineage "naturalisation gap". The
question is whether A\*_h predicts a concept's later field breadth (O2r) beyond the count baseline B5, under
leave-one-field-group-out prediction.

The original code is copied verbatim, split into cells, with markdown between them. The notebook differs from
the script only in how it runs, not in the analysis:
- data is read from `mini_demo_data.json` instead of `results/…`;
- the CLI arguments come from a config cell;
- the split-half reliability replicates run in-process instead of in a spawn process pool;
- the OpenAlex pull functions are omitted, because the data is already packaged;
- figures show inline.

The original full run used 48 dev concepts, and **A\*_h does not survive the pre-registered rule**:
Δρ = −0.006, 90% CI [−0.034, 0.017]; 0 of 4 groups are positive; reliability is 0.58.

The demo runs the same pipeline on **18 of the 48** dev concepts (Biochem 5, Medicine 5, CS 6, Engineering 2), at
the original full-run settings: 50 splits, 2000 bootstraps, and the PyMC NUTS and GLMM checks. In our clean-venv
test it took about 150 s, including the package install. The rule is still failed on the subset. The last cell
prints the demo statistics next to the full-run reference values.

## Layout
| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed, with outputs. It loads the data from GitHub and falls back to the local file. |
| `mini_demo_data.json` | Demo data (~24 MB): the full S0 yearly-count file for all 78 panel concepts, the S2 concept papers, citation lineage and background references for 18 dev concepts (trimmed to the keys the code reads), the OpenAlex credit-ledger column, and the full-run reference numbers. |
| `make_mini_data.py` | Rebuilds `mini_demo_data.json` from the original experiment folder's `results/` and `logs/credits.csv`. |
| `.aii/manifest.yaml` | Storage manifest. Nothing heavy needs a decision. |

Running the notebook writes `results/` (CSVs, `screen_result.json`, `figures/screen_overview.png`), `logs/method.log`
and `method_out.json` next to it. These are regenerated on every run and are not part of the repository.

## How to run
- **Colab:** open `code_demo.ipynb` and choose *Run all*. The first cell installs `loguru`, plus `pymc==6.3.2` if
  pymc is missing. Colab's own numpy, pandas, scipy, scikit-learn, statsmodels and matplotlib are used as they are.
- **Locally (Python 3.12):**
  ```bash
  python -m venv .venv && .venv/bin/pip install jupyter ipykernel
  .venv/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
  ```
  Outside Colab, the install cell pins Colab's versions: numpy 2.0.2, pandas 2.2.2, scipy 1.16.3,
  scikit-learn 1.6.1, statsmodels 0.14.6, matplotlib 3.10.0.
- For a faster run, lower `SPLITS` / `N_BOOT` or set `NO_PYMC = True` in the config cell.

## Restoring removed files
Nothing in this folder is marked `delete`, so nothing needs to be restored. `mini_demo_data.json` can be rebuilt
from the original experiment artifact (`gen_art_experiment_1`, published in the same repository) with:
```bash
python make_mini_data.py <path-to>/gen_art_experiment_1
```
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
python3 -c "import json,yaml;json.load(open('.terminal_claude_agent_struct_out.json'));print(yaml.safe_load(open('.aii/manifest.yaml')))" 2>&1; grep -c "load_data\|urlopen" code_demo.ipynb
````

### [74] TOOL RESULT — Bash · 2026-09-29 21:16:15 UTC

```
{"stdout": "{'entries': []}\n3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [75] ASSISTANT · 2026-09-29 21:16:27 UTC

```
I've built the demo notebook and its data file. The notebook runs cleanly in the fresh test venv at the original full-run settings, finishing in 152 s with no errors against the 600 s budget.

**What's in the workspace**
- **`code_demo.ipynb`** (53 cells, saved with outputs): contains the exact `GITHUB_DATA_URL` and the required `load_data()` pattern that falls back to the local file. The builder copied the code by slicing `method.py` and the five helper modules it imports, so the analysis code is unchanged. Only these things differ:
  - Data is read from the loaded `data` object instead of the `results/…` files, and the credit ledger comes from `data["credits"]` instead of `logs/credits.csv`.
  - The command-line arguments are replaced by a config cell.
  - The 50 split-half replicates run in-process, because spawned worker processes can't import functions defined in a notebook.
  - The OpenAlex download functions and their `oa` import are left out, since the data is already packaged.
  - The figures show inline instead of only being saved.
  - `fit_pymc` gets the draws and chains from config.
  - `main()`'s body is split into 10 cells.
- **`mini_demo_data.json`** (24 MB):
  - The yearly-count file for all 78 panel concepts.
  - The paper, citation and background-reference data for 18 of the 48 dev concepts, from all four field groups, trimmed to the fields the code reads. The other 30 go down the original "not fetched" drop path.
  - The headline numbers from the full 48-concept run, for comparison.
- **`make_mini_data.py`** rebuilds that data file; **`README.md`** covers layout and how to run it; **`.aii/manifest.yaml`** has no entries, because the only large file is JSON and needs no decision.

**Results on the 18-concept subset**
- A\*_h still fails the pre-registered rule: Δρ = +0.033, 90% CI [−0.019, 0.139], and 2 of 4 field groups are positive.
- Unlike the full run, the reliability clause passes on the subset (0.67 vs 0.58), and Δρ is positive rather than −0.006. The last cell prints both runs side by side, so readers can see the subset gives noisier numbers.
- The PyMC check passes: R-hat 1.003, Spearman 0.993 with REML.

**Things to know**
- The notebook installs `pymc==6.3.2`, the version the original used, only if pymc isn't already available. On Colab it would use whatever pymc version is preinstalled, which I couldn't test here.
- I deleted the `results/`, `logs/` and `method_out.json` files my test runs created, since every notebook run regenerates them.

The result file `.terminal_claude_agent_struct_out.json` is written with `code_demo.ipynb` and `mini_demo_data.json`.
```
