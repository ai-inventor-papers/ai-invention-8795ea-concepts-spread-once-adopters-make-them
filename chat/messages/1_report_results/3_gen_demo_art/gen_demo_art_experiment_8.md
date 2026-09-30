# gen_demo_art_experiment_8 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_8` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:17:45 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:17:53 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-4/experiment-10/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-4/experiment-10/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-4/experiment-10/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 21:17:57 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 21:17:57 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 21:17:57 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 21:17:57 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 21:17:57 UTC

```
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; ls -la $W; wc -l $W/method.py; du -sh $W/*
```

### [8] TOOL RESULT — Bash · 2026-09-29 21:17:59 UTC

```
{"stdout": "total 1982\ndrwxrwxrwx 3 aii-agent aii-agent 1002283 Sep 29 21:17 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002283 Sep 29 21:17 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:17 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:17 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   23461 Sep 29 21:17 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:17 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002283 Sep 29 21:17 ..\ntotal 25280\ndrwxrwxrwx 15 aii-agent aii-agent 2023575 Sep 29 05:04 .\ndrwxrwxrwx  7 aii-agent aii-agent 2078275 Sep 29 02:14 ..\ndrwxrwxrwx  2 aii-agent aii-agent   62500 Sep 29 03:52 .aii\n-rw-rw-rw-  1 aii-agent aii-agent      54 Sep 29 02:15 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent    5923 Sep 29 03:52 .aii_worker_result.json\ndrwxrwxrwx  8 aii-agent aii-agent 2005249 Sep 29 03:46 .git\n-rw-rw-rw-  1 aii-agent aii-agent      72 Sep 29 02:35 .gitignore\n-rw-rw-rw-  1 aii-agent aii-agent 1014045 Sep 29 03:52 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent    2709 Sep 29 03:42 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent   22764 Sep 29 03:46 README.md\n-rw-rw-rw-  1 aii-agent aii-agent    6204 Sep 29 02:40 audit.py\ndrwxrwxrwx  4 aii-agent aii-agent 2005380 Sep 29 03:28 data\ndrwxrwxrwx  2 aii-agent aii-agent 1054146 Sep 29 03:29 figures\n-rw-rw-rw-  1 aii-agent aii-agent 2208500 Sep 29 03:39 full_method_out.json\ndrwxrwxrwx  3 aii-agent aii-agent 2002001 Sep 29 02:16 inputs\ndrwxrwxrwx  2 aii-agent aii-agent 1019408 Sep 29 05:04 lib\ndrwxrwxrwx  2 aii-agent aii-agent 2000386 Sep 29 03:10 llm_cache\ndrwxrwxrwx  2 aii-agent aii-agent 1091170 Sep 29 03:28 logs\n-rw-rw-rw-  1 aii-agent aii-agent   10220 Sep 29 03:33 make_outputs.py\n-rw-rw-rw-  1 aii-agent aii-agent    3893 Sep 29 03:32 make_report.py\n-rwxrwxrwx  1 aii-agent aii-agent    3310 Sep 29 03:42 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 1951651 Sep 29 03:39 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    5145 Sep 29 03:39 mini_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent       1 Sep 29 02:21 models\ndrwxrwxrwx  3 aii-agent aii-agent 2009748 Sep 29 02:23 passC\n-rw-rw-rw-  1 aii-agent aii-agent   15598 Sep 29 02:23 passC.py\n-rw-rw-rw-  1 aii-agent aii-agent    6406 Sep 29 02:26 prereg.md\n-rw-rw-rw-  1 aii-agent aii-agent    5145 Sep 29 03:39 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    2521 Sep 29 03:36 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent    4143 Sep 29 03:34 readme_tables.py\n-rw-rw-rw-  1 aii-agent aii-agent    4536 Sep 29 03:41 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent    8650 Sep 29 03:42 reproducibility.md\n-rw-rw-rw-  1 aii-agent aii-agent    1777 Sep 29 03:36 requirements.lock.txt\n-rwxrwxrwx  1 aii-agent aii-agent     366 Sep 29 03:36 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent 1057843 Sep 29 03:40 results\n-rw-rw-rw-  1 aii-agent aii-agent    2620 Sep 29 02:35 s0_prereg.py\n-rw-rw-rw-  1 aii-agent aii-agent    7305 Sep 29 02:21 s1_candidates.py\n-rw-rw-rw-  1 aii-agent aii-agent    8269 Sep 29 02:36 s3_checks.py\n-rw-rw-rw-  1 aii-agent aii-agent    9669 Sep 29 03:10 s4_gate.py\n-rw-rw-rw-  1 aii-agent aii-agent   16136 Sep 29 03:07 s5_typing.py\n-rw-rw-rw-  1 aii-agent aii-agent    9779 Sep 29 02:45 s6_covariates.py\n-rw-rw-rw-  1 aii-agent aii-agent    8397 Sep 29 02:42 s7_ego.py\n-rw-rw-rw-  1 aii-agent aii-agent   15897 Sep 29 03:11 s8_select.py\n-rw-rw-rw-  1 aii-agent aii-agent   15663 Sep 29 03:21 s9_unseal.py\n-rw-rw-rw-  1 aii-agent aii-agent    6457 Sep 29 02:42 s_learned.py\ndrwxrwxrwx  2 aii-agent aii-agent 1077669 Sep 29 02:20 snapshot\ndrwxrwxrwx  2 aii-agent aii-agent 1001197 Sep 29 03:30 tests\n73 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/method.py\n23K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/README.md\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/audit.py\n68M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data\n1.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/figures\n2.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/full_method_out.json\n24M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/inputs\n1.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/lib\n6.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/llm_cache\n2.0M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/logs\n10K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/make_outputs.py\n4.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/make_report.py\n3.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/method.py\n1.9M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/method_out.json\n5.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/mini_method_out.json\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/models\n104M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/passC\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/passC.py\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/prereg.md\n5.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/preview_method_out.json\n2.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/pyproject.toml\n4.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/readme_tables.py\n4.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/rederive.py\n8.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/reproducibility.md\n2.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/requirements.lock.txt\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/restore.sh\n1.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results\n3.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s0_prereg.py\n7.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s1_candidates.py\n8.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s3_checks.py\n9.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s4_gate.py\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s5_typing.py\n10K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s6_covariates.py\n8.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s7_ego.py\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s8_select.py\n16K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s9_unseal.py\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s_learned.py\n1.8M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/snapshot\n992K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/tests", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 21:18:01 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $W/method.py; echo ----; cat $W/preview_method_out.json; echo ----; cat $W/pyproject.toml; ls $W/lib $W/results $W/data
```

### [10] TOOL RESULT — Bash · 2026-09-29 21:18:01 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).\n\nUsage: python method.py [--only STEP] [--from STEP] [--list]\nSteps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort\n                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate\n                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report\nNote: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nPY = sys.executable\nSTEPS = [\n    (\"s0\", [PY, \"s0_prereg.py\"]),\n    (\"s1\", [PY, \"s1_candidates.py\"]),\n    (\"passC\", [PY, \"passC.py\", \"--workers\", \"9\"]),\n    (\"passC_merge\", [PY, \"passC.py\", \"--merge\"]),\n    (\"s3\", [PY, \"s3_checks.py\"]),\n    (\"s4\", [PY, \"s4_gate.py\", \"run\"]),\n    (\"s4_retry\", [PY, \"s4_gate.py\", \"retry\"]),\n    (\"s7_exp5\", [PY, \"s7_ego.py\", \"--frame\", \"exp5\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"200\"]),\n    (\"s7_cohort\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"50\"]),\n    (\"s7_cohort_full\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"full\", \"--workers\", \"5\", \"--chunk\", \"20\",\n                        \"--tag\", \"_full\"]),\n    (\"s6\", [PY, \"s6_covariates.py\"]),\n    (\"s5_exp5\", [PY, \"s5_typing.py\", \"exp5\"]),\n    (\"s5_cohort\", [PY, \"s5_typing.py\", \"cohort\"]),\n    (\"s5_bench\", [PY, \"s5_typing.py\", \"bench\"]),\n    (\"s5_sheet\", [PY, \"s5_typing.py\", \"sheet\"]),\n    (\"s5_gate\", [PY, \"s5_typing.py\", \"gate\"]),\n    (\"s5_v2\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s5_typing.py',c,'--prompt','v2'],check=True) \"\n                          \"for c in ('exp5','cohort','bench','gate')]\"]),\n    (\"s5_m2all\", [PY, \"s5_typing.py\", \"m2all\", \"--prompt\", \"v2\"]),\n    (\"s8\", [PY, \"s8_select.py\", \"--nboot\", \"500\"]),\n    (\"s9\", [PY, \"s9_unseal.py\"]),\n    (\"learned\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s_learned.py',c],check=True) \"\n                           \"for c in ('validate','features','score')]\"]),\n    (\"audit\", [PY, \"audit.py\"]),\n    (\"tests\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,t],check=True) for t in \"\n                         \"('tests/test_output.py','tests/t_ego_flags.py','tests/t_outcomes.py','tests/test_units.py')]\"]),\n    (\"outputs\", [PY, \"make_outputs.py\"]),\n    (\"report\", [PY, \"make_report.py\"]),\n    (\"rederive\", [PY, \"rederive.py\"]),\n]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--only\")\n    ap.add_argument(\"--from\", dest=\"start\")\n    ap.add_argument(\"--list\", action=\"store_true\")\n    a = ap.parse_args()\n    names = [n for n, _ in STEPS]\n    if a.list:\n        print(\"\\n\".join(names))\n        return\n    todo = STEPS\n    if a.only:\n        todo = [s for s in STEPS if s[0] == a.only]\n    elif a.start:\n        todo = STEPS[names.index(a.start):]\n    for name, cmd in todo:\n        print(f\"== {name}: {' '.join(cmd[:4])}\", flush=True)\n        subprocess.run(cmd, cwd=ROOT, check=True)\n\n\nif __name__ == \"__main__\":\n    main()\n----\n{\n  \"metadata\": {\n    \"method_name\": \"OPEN (open-neighbourhood composite) vs B5 baseline, fresh 2015-2017 onset cohort (2017 = declared power extension)\",\n    \"verdict\": \"CONFIRMED\",\n    \"primary_outcome\": \"O2r_m50\",\n    \"predict_B5\": \"frozen OLS of O2r_m50 on standardised B5 fitted on the EXP5 frame\",\n    \"predict_B5_plus_OPEN_home\": \"frozen OLS on B5 + OPEN_home fitted on the EXP5 frame\",\n    \"outcome_grounding\": \"TAG\",\n    \"n\": 1443\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"fresh_cohort_2015_2017_open\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Electrical impedance myography\\\", \\\"openalex_id\\\": \\\"C1918360\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"BGM+Med\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"4.95097\",\n          \"predict_B5_plus_OPEN_home\": \"5.04306\",\n          \"metadata_OPEN_home\": 0.32132431470264056,\n          \"metadata_OPEN_all\": -0.12508189070586714,\n          \"metadata_OPEN_sizematch\": 0.12254799950962321,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 3,\n          \"metadata_fp_logN\": 4.04305126783455,\n          \"metadata_fp_nfields\": 3,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": null,\n          \"metadata_O1c\": -0.24116205681688863,\n          \"metadata_O1b\": 1,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": null,\n          \"metadata_O2r_m50_MATCH\": null,\n          \"metadata_logvol\": 4.02535169073515,\n          \"metadata_growth_c\": -0.3364722366212129,\n          \"metadata_offhome_share\": 0.19047619047619047,\n          \"metadata_entropy\": 0.7385104891120922,\n          \"metadata_reach\": 4,\n          \"metadata_CONTACT_REACH\": 4,\n          \"metadata_RETENTION_RATIO_early\": 0.0,\n          \"metadata_n_authors_early\": 4.962844630259907,\n          \"metadata_n_home_early\": 34,\n          \"metadata_n_all_early\": 55,\n          \"metadata_precision_c\": 0.9,\n          \"metadata_home\": \"27\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Persistent homology\\\", \\\"openalex_id\\\": \\\"C2874115\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"PHYS\\\"}\",\n          \"output\": \"9.39058\",\n          \"predict_B5\": \"7.45805\",\n          \"predict_B5_plus_OPEN_home\": \"NA\",\n          \"metadata_OPEN_home\": null,\n          \"metadata_OPEN_all\": 1.0279867793278947,\n          \"metadata_OPEN_sizematch\": null,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 2,\n          \"metadata_fp_logN\": 4.304065093204169,\n          \"metadata_fp_nfields\": 8,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": 4.921541872785715,\n          \"metadata_O1c\": 0.6061358035703153,\n          \"metadata_O1b\": 0,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": 9.390583535312317,\n          \"metadata_O2r_m50_MATCH\": 9.761747385271264,\n          \"metadata_logvol\": 4.356708826689592,\n          \"metadata_growth_c\": 0.3184537311185346,\n          \"metadata_offhome_share\": 0.7450980392156863,\n          \"metadata_entropy\": 1.6881963704692144,\n          \"metadata_reach\": 6,\n          \"metadata_CONTACT_REACH\": 7,\n          \"metadata_RETENTION_RATIO_early\": 0.42857142857142855,\n          \"metadata_n_authors_early\": 5.389071729816501,\n          \"metadata_n_home_early\": 13,\n          \"metadata_n_all_early\": 77,\n          \"metadata_precision_c\": 1.0,\n          \"metadata_home\": \"31\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Job rotation\\\", \\\"openalex_id\\\": \\\"C3082036\\\", \\\"t0\\\": 2015, \\\"home_group\\\": \\\"SOC\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"7.92326\",\n          \"predict_B5_plus_OPEN_home\": \"7.88886\",\n          \"metadata_OPEN_home\": 0.02274310364663708,\n          \"metadata_OPEN_all\": 0.8155822010123192,\n          \"metadata_OPEN_sizematch\": 0.21973513732250882,\n          \"metadata_type\": \"topic\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 5,\n          \"metadata_fp_logN\": 4.634728988229636,\n          \"metadata_fp_nfields\": 9,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 1,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": null,\n          \"metadata_O1c\": -0.029852963149681777,\n          \"metadata_O1b\": 0,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": null,\n          \"metadata_O2r_m50_MATCH\": 6.959276018099548,\n          \"metadata_logvol\": 4.219507705176107,\n          \"metadata_growth_c\": 0.16034265007517948,\n          \"metadata_offhome_share\": 0.6388888888888888,\n          \"metadata_entropy\": 1.7500458374633958,\n          \"metadata_reach\": 6,\n          \"metadata_CONTACT_REACH\": 7,\n          \"metadata_RETENTION_RATIO_early\": 0.14285714285714285,\n          \"metadata_n_authors_early\": 5.0369526024136295,\n          \"metadata_n_home_early\": 13,\n          \"metadata_n_all_early\": 67,\n          \"metadata_precision_c\": 1.0,\n          \"metadata_home\": \"14\",\n          \"metadata_window_flag\": 0\n        }\n      ]\n    }\n  ]\n}----\n[project]\nname = \"rq1-fresh-cohort-open\"\nversion = \"0.1.0\"\ndescription = \"RQ1 fresh-cohort test: do open early ego-neighbourhoods anticipate disciplinary breadth (sealed single unseal)\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.12.15\",\n  \"aiosignal==1.4.0\",\n  \"annotated-types==0.8.0\",\n  \"aplr==10.27.0\",\n  \"asttokens==3.0.2\",\n  \"attrs==26.1.0\",\n  \"blinker==1.9.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"comm==0.2.3\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"dash==4.4.1\",\n  \"dash-cytoscape==1.0.2\",\n  \"dill==0.4.1\",\n  \"executing==2.2.1\",\n  \"flask==3.1.3\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"frozenlist==1.8.0\",\n  \"gevent==26.9.0\",\n  \"greenlet==3.5.6\",\n  \"idna==3.20\",\n  \"igraph==1.0.0\",\n  \"importlib-metadata==9.0.1\",\n  \"interface-meta==2.0.1\",\n  \"interpret==0.7.8\",\n  \"interpret-core==0.7.8\",\n  \"ipython==9.17.1\",\n  \"ipython-pygments-lexers==1.1.1\",\n  \"ipywidgets==8.1.9\",\n  \"itsdangerous==2.2.0\",\n  \"janus==2.0.0\",\n  \"jedi==0.20.0\",\n  \"jinja2==3.1.6\",\n  \"joblib==1.6.0\",\n  \"jupyterlab-widgets==3.0.17\",\n  \"kiwisolver==1.5.1\",\n  \"leidenalg==0.12.0\",\n  \"llvmlite==0.49.0\",\n  \"loguru==0.7.3\",\n  \"markupsafe==3.0.3\",\n  \"matplotlib==3.11.2\",\n  \"matplotlib-inline==0.2.2\",\n  \"multidict==6.9.1\",\n  \"multiprocess==0.70.19\",\n  \"narwhals==2.26.0\",\n  \"nest-asyncio==1.6.0\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"parso==0.8.7\",\n  \"patsy==1.0.3\",\n  \"pexpect==4.9.0\",\n  \"pillow==12.3.0\",\n  \"plotly==7.1.0\",\n  \"prompt-toolkit==3.0.53\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"ptyprocess==0.7.0\",\n  \"pure-eval==0.2.4\",\n  \"pyahocorasick==2.3.1\",\n  \"pyarrow==25.0.1\",\n  \"pydantic==2.13.5\",\n  \"pydantic-core==2.46.5\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"python-dateutil==2.9.0.post0\",\n  \"python-igraph==1.0.0\",\n  \"pyyaml==6.0.3\",\n  \"requests==2.34.2\",\n  \"retrying==1.4.2\",\n  \"salib==1.6.0\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"setuptools==84.0.0\",\n  \"shap==0.52.0\",\n  \"six==1.17.0\",\n  \"slicer==0.0.8\",\n  \"snowballstemmer==3.1.1\",\n  \"stack-data==0.6.3\",\n  \"statsmodels==0.15.0\",\n  \"tenacity==9.1.4\",\n  \"texttable==1.7.0\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"traitlets==5.16.1\",\n  \"typing-extensions==4.16.0\",\n  \"typing-inspection==0.4.4\",\n  \"urllib3==2.8.0\",\n  \"wcwidth==0.9.1\",\n  \"werkzeug==3.1.9\",\n  \"widgetsnbextension==4.0.16\",\n  \"wrapt==2.5.0\",\n  \"yarl==1.25.1\",\n  \"zipp==4.1.0\",\n  \"zope-event==6.2\",\n  \"zope-interface==8.6\",\n]\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data:\nanalysis_cohort.parquet\nbg_topics.npz\ncohort_candidates.csv\ncohort_candidates_gated.csv\ncohort_predictions.parquet\nconcept_types.csv\ncontrols.csv\ncovariates_cohort.parquet\ncovariates_exp5.parquet\nego_open\nego_open_cohort.parquet\nego_open_cohort_full.parquet\nego_open_exp5.parquet\nego_open_exp5_u2.parquet\nexp5_o2r_match_vs_tag.parquet\nfeatures_cohort.parquet\nfeatures_exp5_open.parquet\nlearned_features_cohort.parquet\no5_events_all.parquet\noutcomes_cohort.parquet\npassC_bg.npz\npassC_early.parquet\npassC_info.json\npassC_pre_agg.parquet\npassC_totals.npz\nprecision_cohort.csv\nsealed\ntypes_cohort_v1.csv\ntypes_cohort_v2.csv\ntypes_exp5_v1.csv\ntypes_exp5_v2.csv\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/lib:\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nfeatport.py\nframe_exp5.py\nh2.py\nindicators.py\nladder.py\nllmc.py\nmatcher.py\nmodels_exp5.py\noutc.py\noutjson.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal2.py\nseal_exp5.py\nstats_core.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results:\naudit.json\ncohort_report.json\ncohort_result.json\ncoverage_by_year.csv\ndeviations.json\nexp5_selection_result.json\nfrozen_spec.json\nfrozen_spec_v0.json\nlearned_models_cohort.json\nlearned_port_validation.json\nllm_cost_log.csv\nreadme_tables.md\nrederive.json\ns1_candidates_summary.json\ns2_checks.json\ns3_decision.json\ns4_gate_summary.json\ns6_checks.json\ns6_checks_cohort.json\ntype_benchmark_final.json\ntype_benchmark_v1.csv\ntype_benchmark_v1.json\ntype_benchmark_v2.csv\ntype_benchmark_v2.json\ntype_gold_labels_v1.csv\ntype_gold_labels_v2.csv\ntype_gold_sheet_v1.csv\ntype_m2all.json\ntype_prompt_v2.txt\nu2_ego_flags.json\nu5_outcomes.json\nu8_prompt_identity.json\nunit_tests.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 21:18:05 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $W/rederive.py; echo -----; cat $W/audit.py; echo ----; cat $W/make_outputs.py
```

### [12] TOOL RESULT — Bash · 2026-09-29 21:18:05 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Short INDEPENDENT re-derivation of the headline numbers (TODO 5), separate from the pipeline code path.\n\nReads the raw per-concept tables only (data/features_cohort.parquet components, data/outcomes_cohort.parquet,\nresults/frozen_spec.json constants, data/cohort_predictions.parquet) -- NOT results/cohort_result.json fields -- and\n(1) rebuilds OPEN_home / OPEN_all from the six raw components with the frozen constants (pandas, own loop);\n(2) recomputes the partial Spearman at R2 with its own design matrix (pandas ranks + numpy QR residuals, no\n    lib/ladder.rung_design, no rq1stats); a 400-draw bootstrap CI;\n(3) the B5 vs B5+OPEN_home prediction Spearman gain (scipy on the stored frozen predictions);\n(4) the same R2 statistic on shuffled outcomes (200 permutations) and on a random OPEN, which must NOT look significant.\nWrites results/rederive.json.\"\"\"\nimport json\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import spearmanr\n\nROOT = Path(__file__).resolve().parent\nspec = json.loads((ROOT / \"results/frozen_spec.json\").read_text())\nF = pd.read_parquet(ROOT / \"data/features_cohort.parquet\")\nO = pd.read_parquet(ROOT / \"data/outcomes_cohort.parquet\")[[\"ci\", \"O2r_m50\"]]\nD = F.merge(O, on=\"ci\")\nSIGN = {\"new_edge_rate\": 1, \"n_comm_W3\": 1, \"participation\": 1, \"NOV_res\": 1, \"ego_density_W3\": -1,\n        \"edge_persistence\": -1}\n\n\ndef open_score(build):\n    c = spec[\"open_constants\"][build]\n    zs = []\n    for k, s in SIGN.items():\n        v = D[f\"{k}__{build}\"].clip(c[k][\"lo\"], c[k][\"hi\"])\n        zs.append(s * (v - c[k][\"mu\"]) / c[k][\"sd\"])\n    Z = pd.concat(zs, axis=1)\n    o = Z.mean(axis=1, skipna=True).where(Z.notna().sum(axis=1) >= 4)\n    if build != \"all\":\n        o = o.where(D.n_home_early >= 10)\n    return o\n\n\ndef design(d):\n    cont = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\"]\n    X = [np.ones(len(d))] + [d[c].rank().to_numpy() for c in cont]\n    for y in (2016, 2017):\n        X.append((d.t0 == y).to_numpy(float))\n    for t in (\"method\", \"object\", \"property\"):\n        X.append((d[\"type\"] == t).to_numpy(float))\n    X.append(d[\"generic\"].to_numpy(float))\n    for lv in (3, 4, 5):\n        X.append((d.level == lv).to_numpy(float))\n    return np.column_stack(X)\n\n\ndef psp(x, y, X):\n    keep = np.abs(np.linalg.qr(X)[1].diagonal()) > 1e-9      # drop collinear / empty dummy columns\n    Q, _ = np.linalg.qr(X[:, keep])\n    rx = pd.Series(x).rank().to_numpy(); ry = pd.Series(y).rank().to_numpy()\n    rx = rx - Q @ (Q.T @ rx); ry = ry - Q @ (Q.T @ ry)\n    return float(np.corrcoef(rx, ry)[0, 1])\n\n\nout = {}\nfor b in (\"home\", \"all\"):\n    o = open_score(b)\n    out[f\"OPEN_{b}_max_abs_diff_vs_frozen_table\"] = float(np.nanmax(np.abs(o - F[f\"OPEN_{b}\"])))\n    d = D.assign(o=o).dropna(subset=[\"o\", \"O2r_m50\", \"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"])\n    d = d.reset_index(drop=True)\n    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))\n    rng = np.random.default_rng(1)\n    bs = []\n    for _ in range(400):\n        i = rng.integers(0, len(d), len(d))\n        di = d.iloc[i].reset_index(drop=True)\n        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))\n    out[f\"OPEN_{b}_psp_R2\"] = {\"n\": len(d), \"est\": est, \"ci95_400boot\": [float(np.percentile(bs, 2.5)),\n                                                                          float(np.percentile(bs, 97.5))]}\n    if b == \"home\":\n        # placebo 1: within-group shuffled outcome; placebo 2: random OPEN\n        perm = []\n        for _ in range(200):\n            y = d.O2r_m50.to_numpy().copy()\n            for g in d.agroup.unique():\n                m = (d.agroup == g).to_numpy()\n                y[m] = rng.permutation(y[m])\n            perm.append(psp(d.o.to_numpy(), y, design(d)))\n        perm = np.abs(perm)\n        out[\"placebo_shuffled_outcome\"] = {\"q95_abs\": float(np.percentile(perm, 95)),\n                                           \"share_ge_observed\": float((perm >= abs(est)).mean())}\n        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))\n        out[\"placebo_random_open_psp\"] = rnd\nP = pd.read_parquet(ROOT / \"data/cohort_predictions.parquet\").merge(O, on=\"ci\").dropna()\ns0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]\nout[\"prediction_spearman\"] = {\"n\": len(P), \"B5\": float(s0), \"B5_plus_OPEN_home\": float(s1), \"diff\": float(s1 - s0)}\n(ROOT / \"results/rederive.json\").write_text(json.dumps(out, indent=1))\nprint(json.dumps(out, indent=1))\n-----\n#!/usr/bin/env python3\n\"\"\"Post-unseal audit with INDEPENDENT code (statsmodels OLS residuals, scipy ranks/hypergeometric, hand DL).\n\nA1  primary OPEN_home psp (O2r_m50) at R2 and R3 re-derived with statsmodels (target |diff| < 1e-8)\nA2  DL pooled estimate re-derived by hand from the per-group estimates / SEs in cohort_result.json\nA3  O2r_m50 re-computed for 30 random cohort concepts straight from the sealed parts with scipy.stats.hypergeom\nA4  within-group shuffled-outcome control (200 draws; 95th percentile of |psp|) with the independent psp\nA5  planted-signal recovery (psp = 0.10) with the independent psp and a 1,000-draw bootstrap\nWrites results/audit.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\nfrom scipy.stats import hypergeom, rankdata\n\nfrom common import DATA, RES, jdump, setup_logger\nfrom ladder import rung_design\n\nlogger = setup_logger(\"audit\")\n\n\ndef psp_sm(x, y, B, C) -> float:\n    Z = sm.add_constant(np.c_[np.column_stack([rankdata(B[:, j]) for j in range(B.shape[1])]), C], has_constant=\"add\")\n    rx = sm.OLS(rankdata(x), Z).fit().resid\n    ry = sm.OLS(rankdata(y), Z).fit().resid\n    return float(np.corrcoef(rx, ry)[0, 1])\n\n\ndef design(df, rung, xcol, ycol):\n    Bc, Cc = rung_design(df, rung)\n    x, y = df[xcol].to_numpy(float), df[ycol].to_numpy(float)\n    B, C = Bc.to_numpy(float), Cc.to_numpy(float)\n    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)\n    return x[ok], y[ok], B[ok], C[ok], df[ok]\n\n\ndef rarefy_indep(counts, m=50) -> float:\n    counts = np.asarray([int(c) for c in counts if c > 0])\n    N = counts.sum()\n    if N < m:\n        return math.nan\n    return float(sum(1 - hypergeom(N, int(c), m).pmf(0) for c in counts))\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    res = json.loads((RES / \"cohort_result.json\").read_text())\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    df = pd.read_parquet(DATA / \"analysis_cohort.parquet\")\n    out: dict = {}\n    a1 = {}\n    for r in (\"R2\", \"R3\"):\n        x, y, B, C, _ = design(df, r, \"OPEN_home\", \"O2r_m50\")\n        v = psp_sm(x, y, B, C)\n        ref = res[\"primary\"][f\"OPEN_home|O2r_m50|{r}\"][\"rho\"]\n        a1[r] = {\"statsmodels\": v, \"pipeline\": ref, \"abs_diff\": abs(v - ref), \"pass\": abs(v - ref) < 1e-8}\n    out[\"A1_psp_rederivation\"] = a1\n    a2 = {}\n    for key, g in res[\"groups\"].items():\n        b = np.array([g[\"groups\"][k][\"rho\"] for k in (\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\")], float)\n        se = np.array([g[\"groups\"][k][\"se\"] for k in (\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\")], float)\n        ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n        b, se = b[ok], se[ok]\n        w = 1 / se ** 2\n        mf = np.sum(w * b) / np.sum(w)\n        Q = np.sum(w * (b - mf) ** 2)\n        k = len(b)\n        tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w))) if k > 1 else 0.0\n        ws = 1 / (se ** 2 + tau2)\n        est = float(np.sum(ws * b) / np.sum(ws))\n        a2[key] = {\"hand\": est, \"pipeline\": g[\"DL\"][\"b\"], \"abs_diff\": abs(est - g[\"DL\"][\"b\"])}\n    out[\"A2_DL_rederivation\"] = {\"max_abs_diff\": max(v[\"abs_diff\"] for v in a2.values()), \"items\": a2}\n    # A3 O2r_m50 from the sealed parts (independent code; grounding as frozen)\n    sealed = pd.concat([pd.read_parquet(p) for p in sorted((DATA / \"sealed/parts\").glob(\"sealed_*.parquet\"))])\n    use_match = spec[\"outcome_grounding\"] == \"MATCH\"\n    rng = np.random.default_rng(3)\n    pick = rng.choice(df.ci[np.isfinite(df.O2r_m50)].to_numpy(), size=min(30, int(np.isfinite(df.O2r_m50).sum())),\n                      replace=False)\n    diffs = []\n    for ci in pick:\n        t0 = int(df.t0[df.ci == ci].iat[0])\n        sh = 1 if t0 == 2017 else 0\n        d = sealed[(sealed.ci == ci) & (sealed.year >= t0 + 6 - sh) & (sealed.year <= t0 + 8 - sh) & (sealed.vfield > 0)]\n        if not use_match:\n            d = d[d.tagstate == 1]\n        cnt = d.groupby(\"vfield\").n.sum()\n        v = rarefy_indep(cnt.to_numpy())\n        diffs.append(abs(v - float(df.O2r_m50[df.ci == ci].iat[0])))\n    out[\"A3_O2r_from_sealed\"] = {\"n\": len(diffs), \"max_abs_diff\": float(np.nanmax(diffs)), \"pass\": float(np.nanmax(diffs)) < 1e-8}\n    # A4 shuffled control\n    x, y, B, C, d = design(df, \"R2\", \"OPEN_home\", \"O2r_m50\")\n    g = d.agroup.to_numpy()\n    r4 = np.random.default_rng(11)\n    vals = []\n    for _ in range(200):\n        yp = y.copy()\n        for gg in np.unique(g):\n            m = g == gg\n            yp[m] = r4.permutation(yp[m])\n        vals.append(psp_sm(x, yp, B, C))\n    vals = np.abs(vals)\n    out[\"A4_shuffled\"] = {\"q95_abs_psp\": float(np.percentile(vals, 95)), \"mean_abs\": float(vals.mean()),\n                          \"share_lt_0.05\": float((vals < 0.05).mean())}\n    # A5 planted\n    Z = sm.add_constant(np.c_[np.column_stack([rankdata(B[:, j]) for j in range(B.shape[1])]), C], has_constant=\"add\")\n    rx = sm.OLS(rankdata(x), Z).fit().resid\n    yp = y.copy()\n    for gg in np.unique(g):\n        m = g == gg\n        yp[m] = r4.permutation(yp[m])\n    zr = (rankdata(yp) - rankdata(yp).mean()) / rankdata(yp).std()\n    yplant = zr + 0.10 / math.sqrt(1 - 0.01) * rx / rx.std()\n    est = psp_sm(x, yplant, B, C)\n    bs = []\n    for _ in range(1000):\n        i = r4.integers(0, len(x), len(x))\n        Ci = C[i]\n        bs.append(psp_sm(x[i], yplant[i], B[i], Ci[:, Ci.std(0) > 0]))\n    out[\"A5_planted\"] = {\"target\": 0.10, \"estimate\": est, \"ci\": [float(np.percentile(bs, 2.5)),\n                                                                 float(np.percentile(bs, 97.5))],\n                         \"recovered_ci_gt0\": bool(np.percentile(bs, 2.5) > 0)}\n    out[\"all_rederivations_pass\"] = bool(all(v[\"pass\"] for v in a1.values()) and out[\"A3_O2r_from_sealed\"][\"pass\"]\n                                         and out[\"A2_DL_rederivation\"][\"max_abs_diff\"] < 1e-10)\n    jdump(out, RES / \"audit.json\")\n    logger.info(f\"audit: {json.dumps({k: v for k, v in out.items() if k != 'A2_DL_rederivation'})[:1500]}\")\n\n\nif __name__ == \"__main__\":\n    main()\n----\n#!/usr/bin/env python3\n\"\"\"S10: figures (PNG + PDF) and the exp_gen_sol_out method output (one example per cohort concept).\n\nfig_ladder          psp by rung, three builds, O2r_m50 / O2r_resid panels; cohort (solid, 95% CI) vs EXP5 (dashed)\nfig_forest_groups   per-group psp of OPEN_home at R2 with the DL diamond, cohort and EXP5 side by side\nfig_components      the six components alone at R2 (HOME / ALL builds), cohort vs EXP5\nfig_within_type     OPEN builds within method / object / property / topic concepts (R3 minus type dummies)\nfig_coverage_audit  legacy-tag rate, control TAG/MATCH ratio and venue-label coverage by year (S3 audit)\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport matplotlib\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, FIGS, RES, ROOT, jdump, setup_logger\nfrom ladder import BUILDS, COMPONENTS, POOL_GROUPS, RUNGS\nfrom outjson import make_method_out\n\nlogger = setup_logger(\"make_outputs\")\nplt.rcParams.update({\"font.size\": 9, \"pdf.fonttype\": 42, \"ps.fonttype\": 42, \"axes.spines.top\": False,\n                     \"axes.spines.right\": False})\nCOL = {\"home\": \"#1b6ca8\", \"all\": \"#c0392b\", \"sizematch\": \"#7d8a2e\"}\nLAB = {\"home\": \"HOME-ONLY\", \"all\": \"ALL-PAPERS\", \"sizematch\": \"SIZE-MATCHED\"}\n\n\ndef save(fig, name: str) -> None:\n    fig.savefig(FIGS / f\"{name}.png\", dpi=200, bbox_inches=\"tight\")\n    fig.savefig(FIGS / f\"{name}.pdf\", bbox_inches=\"tight\")\n    plt.close(fig)\n\n\ndef fig_ladder(res: dict, sel: dict) -> None:\n    fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)\n    xs = np.arange(len(RUNGS))\n    for ax, y in zip(axs, (\"O2r_m50\", \"O2r_resid\")):\n        for j, b in enumerate(BUILDS):\n            est = [res[\"primary\"][f\"OPEN_{b}|{y}|{r}\"][\"rho\"] for r in RUNGS]\n            lo = [res[\"primary\"][f\"OPEN_{b}|{y}|{r}\"][\"ci\"][0] for r in RUNGS]\n            hi = [res[\"primary\"][f\"OPEN_{b}|{y}|{r}\"][\"ci\"][1] for r in RUNGS]\n            off = (j - 1) * 0.12\n            ax.errorbar(xs + off, est, yerr=[np.subtract(est, lo), np.subtract(hi, est)], fmt=\"o-\", color=COL[b],\n                        ms=4, lw=1.2, capsize=2, label=f\"{LAB[b]} cohort\")\n            se = [sel[\"ladder\"][f\"OPEN_{b}|{y}|{r}\"][\"rho\"] for r in RUNGS]\n            ax.plot(xs + off, se, ls=\"--\", marker=\"x\", color=COL[b], alpha=0.6, lw=1, label=f\"{LAB[b]} EXP5 (selection)\")\n        ax.axhline(0, color=\"k\", lw=0.6)\n        ax.set_xticks(xs, [\"R0\\nB5\\n+year\", \"R1\\n+reach\", \"R2\\n+type\", \"R3\\n+foot-\\nprint\", \"R4\\n+cover-\\nage\",\n                           \"R5\\n+group\\nFE\"], fontsize=7)\n        ax.set_title(f\"{y}\", fontsize=9)\n    axs[0].set_ylabel(\"partial Spearman with OPEN (95% CI)\")\n    h, l = axs[0].get_legend_handles_labels()\n    fig.legend(h, l, fontsize=7, frameon=False, loc=\"lower center\", ncol=3, bbox_to_anchor=(0.5, -0.12))\n    save(fig, \"fig_ladder\")\n\n\ndef fig_forest(res: dict, sel: dict) -> None:\n    fig, ax = plt.subplots(figsize=(5.2, 3.6))\n    rows = POOL_GROUPS + [\"MATHDEC\"]\n    for k, (src, lab, dy, c) in enumerate(((res[\"groups\"][\"OPEN_home|O2r_m50|R2\"], \"cohort 2015-17\", -0.15, \"#1b6ca8\"),\n                                           (sel[\"groups\"][\"OPEN_home|O2r_m50|R2\"], \"EXP5 2003-14 (selection)\", 0.15,\n                                            \"#888888\"))):\n        for i, g in enumerate(rows):\n            r = src[\"groups\"][g]\n            if not np.isfinite(r[\"rho\"]):\n                ax.text(0, i + dy, f\"  not estimable (n={r['n']} < 30)\", fontsize=6, color=c, va=\"center\")\n                continue\n            ax.errorbar(r[\"rho\"], i + dy, xerr=[[r[\"rho\"] - r[\"ci\"][0]], [r[\"ci\"][1] - r[\"rho\"]]], fmt=\"o\", color=c,\n                        ms=4, capsize=2, label=lab if i == 0 else None)\n            ax.text(1.02, i + dy, f\"n={r['n']}\", transform=ax.get_yaxis_transform(), fontsize=6, color=c, va=\"center\")\n        dl = src[\"DL\"]\n        yv = len(rows) + dy\n        ax.fill([dl[\"ci\"][0], dl[\"b\"], dl[\"ci\"][1], dl[\"b\"]], [yv, yv + 0.12, yv, yv - 0.12], color=c, alpha=0.8)\n    ax.set_yticks(list(range(len(rows))) + [len(rows)], rows + [f\"DL pooled (5 groups)\"])\n    ax.axvline(0, color=\"k\", lw=0.6)\n    ax.invert_yaxis()\n    ax.set_xlabel(\"partial Spearman OPEN_home ~ O2r_m50 | R2 (95% CI)\")\n    ax.legend(fontsize=7, frameon=False, loc=\"upper left\", bbox_to_anchor=(0.0, -0.13), ncol=2)\n    save(fig, \"fig_forest_groups\")\n\n\ndef fig_components(res: dict, sel: dict) -> None:\n    fig, axs = plt.subplots(1, 2, figsize=(9, 3.2), sharey=True)\n    for ax, b in zip(axs, (\"home\", \"all\")):\n        xs = np.arange(len(COMPONENTS))\n        c = [res[\"components\"][f\"{k}__{b}|O2r_m50|R2\"] for k in COMPONENTS]\n        s = [sel[\"components\"][f\"{k}__{b}|O2r_m50|R2\"] for k in COMPONENTS]\n        ax.errorbar(xs - 0.1, [r[\"rho\"] for r in c], yerr=[[r[\"rho\"] - r[\"ci\"][0] for r in c],\n                                                            [r[\"ci\"][1] - r[\"rho\"] for r in c]],\n                    fmt=\"o\", color=COL[b], capsize=2, ms=4, label=\"cohort\")\n        ax.errorbar(xs + 0.1, [r[\"rho\"] for r in s], yerr=[[r[\"rho\"] - r[\"ci\"][0] for r in s],\n                                                            [r[\"ci\"][1] - r[\"rho\"] for r in s]],\n                    fmt=\"s\", color=\"#888888\", capsize=2, ms=3, label=\"EXP5 (selection)\")\n        ax.axhline(0, color=\"k\", lw=0.6)\n        short = {\"new_edge_rate\": \"new edge\\nrate (+)\", \"n_comm_W3\": \"n comm\\nW3 (+)\", \"participation\": \"partici-\\npation (+)\",\n                 \"NOV_res\": \"NOV_res\\n(+)\", \"ego_density_W3\": \"ego dens.\\nW3 (-)\", \"edge_persistence\": \"edge pers-\\nistence (-)\"}\n        ax.set_xticks(xs, [short[k] for k in COMPONENTS], fontsize=7)\n        ax.set_title(f\"{LAB[b]} build, O2r_m50 | R2\", fontsize=9)\n    axs[0].set_ylabel(\"partial Spearman (95% CI)\")\n    axs[0].legend(fontsize=7, frameon=False)\n    save(fig, \"fig_components\")\n\n\ndef fig_within_type(res: dict, sel: dict) -> None:\n    fig, ax = plt.subplots(figsize=(6, 3.2))\n    types = [\"method\", \"object\", \"property\", \"topic\"]\n    for j, b in enumerate(BUILDS):\n        xs = np.arange(len(types)) + (j - 1) * 0.22\n        r = [res[\"within_type\"][f\"OPEN_{b}|{t}|R3\"] for t in types]\n        est = np.array([v[\"rho\"] for v in r], float)\n        ax.errorbar(xs, est, yerr=[est - np.array([v[\"ci\"][0] for v in r]), np.array([v[\"ci\"][1] for v in r]) - est],\n                    fmt=\"o\", color=COL[b], capsize=2, ms=4, label=f\"{LAB[b]} cohort\")\n        s = [sel[\"within_type\"][f\"OPEN_{b}|{t}|R3\"][\"rho\"] for t in types]\n        ax.plot(xs, s, \"x\", color=COL[b], alpha=0.6)\n    ax.axhline(0, color=\"k\", lw=0.6)\n    ax.set_xticks(np.arange(4), [f\"{t}\\n(n={res['within_type'][f'OPEN_home|{t}|R3']['n']})\" for t in types])\n    ax.set_ylabel(\"partial Spearman | R3 - type (95% CI)\")\n    ax.set_title(\"OPEN within concept type (x = EXP5 selection estimate)\", fontsize=9)\n    ax.legend(fontsize=7, frameon=False)\n    save(fig, \"fig_within_type\")\n\n\ndef fig_coverage() -> None:\n    cov = pd.read_csv(RES / \"coverage_by_year.csv\")\n    cov = cov[cov.year >= 2008]\n    fig, ax = plt.subplots(figsize=(6, 3))\n    ax.plot(cov.year, cov.tag03_rate, \"o-\", ms=3, label=\"base works with a legacy tag >= 0.3\")\n    ax.plot(cov.year, cov.tagany_rate, \"s-\", ms=3, label=\"base works with any legacy tag\")\n    ax.plot(cov.year, cov.control_tag_over_match, \"^-\", ms=3, label=\"controls: TAG / title-match hits\")\n    ax.plot(cov.year, cov.venue_label_coverage, \"d-\", ms=3, label=\"venue-field label coverage\")\n    ax.axvspan(2020.5, 2024.5, color=\"0.9\", zorder=0)\n    ax.set_ylim(0, 1.05)\n    ax.set_xticks(range(2008, 2025, 2))\n    ax.set_xlabel(\"publication year\")\n    ax.set_ylabel(\"share\")\n    ax.set_title(\"Outcome-window measurement audit (shaded: cohort outcome years)\", fontsize=9)\n    ax.legend(fontsize=7, frameon=False, loc=\"lower left\")\n    save(fig, \"fig_coverage_audit\")\n\n\ndef method_out(res: dict) -> None:\n    A = pd.read_parquet(DATA / \"analysis_cohort.parquet\")\n    P = pd.read_parquet(DATA / \"cohort_predictions.parquet\")\n    A = A.merge(P, on=\"ci\", how=\"left\")\n    rows = []\n    for r in A.itertuples():\n        d = {\"label\": r.name, \"openalex_id\": r.concept_id, \"t0\": r.t0, \"group\": r.agroup, \"O2r_m50\": r.O2r_m50,\n             \"pred_b5\": r.pred_b5, \"pred_b5_open\": r.pred_b5_open}\n        for c in (\"OPEN_home\", \"OPEN_all\", \"OPEN_sizematch\", \"type\", \"generic\", \"level\", \"fp_logN\", \"fp_nfields\",\n                  \"fp_reemerge\", \"fp_wiki_pre\", \"newborn\", \"O2r_resid\", \"O1c\", \"O1b\", \"O3\", \"O2r_m50_TAG\",\n                  \"O2r_m50_MATCH\", \"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\",\n                  \"RETENTION_RATIO_early\", \"n_authors_early\", \"n_home_early\", \"n_all_early\", \"precision_c\",\n                  \"home\", \"window_flag\"):\n            v = getattr(r, c)\n            d[f\"meta_{c}\"] = v.item() if hasattr(v, \"item\") else v\n        rows.append(d)\n    meta = {\"method_name\": \"OPEN (open-neighbourhood composite) vs B5 baseline, fresh 2015-2017 onset cohort (2017 = declared power extension)\",\n            \"verdict\": res[\"verdict\"][\"verdict\"], \"primary_outcome\": \"O2r_m50\",\n            \"predict_B5\": \"frozen OLS of O2r_m50 on standardised B5 fitted on the EXP5 frame\",\n            \"predict_B5_plus_OPEN_home\": \"frozen OLS on B5 + OPEN_home fitted on the EXP5 frame\",\n            \"outcome_grounding\": res[\"grounding\"], \"n\": len(rows)}\n    out = make_method_out(rows, meta)\n    (ROOT / \"full_method_out.json\").write_text(json.dumps(out, indent=1))\n    logger.info(f\"method_out: {len(rows)} examples\")\n\n\ndef nan_none(o):\n    \"\"\"JSON null (NaN written by jdump) -> float NaN, recursively.\"\"\"\n    if isinstance(o, dict):\n        return {k: nan_none(v) for k, v in o.items()}\n    if isinstance(o, list):\n        return [nan_none(v) for v in o]\n    return float(\"nan\") if o is None else o\n\n\ndef main() -> None:\n    res = nan_none(json.loads((RES / \"cohort_result.json\").read_text()))\n    sel = nan_none(json.loads((RES / \"exp5_selection_result.json\").read_text()))\n    fig_ladder(res, sel)\n    fig_forest(res, sel)\n    fig_components(res, sel)\n    fig_within_type(res, sel)\n    fig_coverage()\n    method_out(res)\n\n\nif __name__ == \"__main__\":\n    main()", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-29 21:18:17 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cd $W; ls .venv 2>/dev/null | head -2; which python3; python3 - <<'EOF'
import pandas as pd, json
F=pd.read_parquet("data/features_cohort.parquet"); print(F.shape); print(list(F.columns))
O=pd.read_parquet("data/outcomes_cohort.parquet"); print(O.shape, list(O.columns))
P=pd.read_parquet("data/cohort_predictions.parquet"); print(P.shape, list(P.columns))
spec=json.load(open("results/frozen_spec.json")); print(list(spec.keys())); print(json.dumps(spec["open_constants"])[:1500])
print(F.head(2).T.to_string()[:4000])
EOF
cat results/rederive.json
```

### [14] TOOL RESULT — Bash · 2026-09-29 21:18:19 UTC

```
{"stdout": "/usr/local/bin/python3\n(1443, 72)\n['ci', 'concept_id', 'qid', 'name', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'early_volume', 'role', 'intersection_born', 'precision_c', 'n_labelled_prec', 'precision_source', 'pass_gate', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'agroup', 'home_coverage_early', 'window_flag', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch']\n(1443, 42) ['ci', 'O1b_TAG', 'O3_TAG', 'peak_year_TAG', 'N_outcome_TAG', 'O2r_m50_TAG', 'O2r_m30_TAG', 'O1c_TAG', 'N_late_all_TAG', 'O1b_MATCH', 'O3_MATCH', 'peak_year_MATCH', 'N_outcome_MATCH', 'O2r_m50_MATCH', 'O2r_m30_MATCH', 'O1c_MATCH', 'N_late_all_MATCH', 'O1b', 'O3', 'O2r_m50', 'O2r_m30', 'O1c', 'N_outcome', 'O2r_resid', 'O2r_m50_le2022_TAG', 'O2r_resid_le2022_TAG', 'O1b_TAG_le2022', 'O3_TAG_le2022', 'peak_year_TAG_le2022', 'N_outcome_TAG_le2022', 'O2r_m50_TAG_le2022', 'O2r_m30_TAG_le2022', 'O1c_TAG_le2022', 'N_late_all_TAG_le2022', 'O1b_MATCH_le2022', 'O3_MATCH_le2022', 'peak_year_MATCH_le2022', 'N_outcome_MATCH_le2022', 'O2r_m50_MATCH_le2022', 'O2r_m30_MATCH_le2022', 'O1c_MATCH_le2022', 'N_late_all_MATCH_le2022']\n(1443, 3) ['ci', 'pred_b5', 'pred_b5_open']\n['prereg_sha256', 'spec_v0_sha256', 'open_constants', 'open_min_home_papers', 'open_min_components', 'outcome_grounding', 'primary', 'O2r_resid', 'extension_2017', 'power', 'type_labels_sha256', 'type_benchmark', 'rungs', 'groups', 'holm_family', 'directions', 'bootstrap', 'prediction_models', 'cohort_n', 'cohort_n_by_t0', 'sha256', 'code_sha256', 'pre_unseal_checklist']\n{\"home\": {\"new_edge_rate\": {\"lo\": 0.0, \"hi\": 2.0, \"mu\": 0.24226876611794407, \"sd\": 0.29476323739891586, \"sign\": 1, \"n\": 12499}, \"n_comm_W3\": {\"lo\": 0.0, \"hi\": 5.0, \"mu\": 1.251940155212417, \"sd\": 1.1109950408968348, \"sign\": 1, \"n\": 12499}, \"participation\": {\"lo\": 0.0, \"hi\": 0.7422196372922436, \"mu\": 0.23128455585636246, \"sd\": 0.2522103838072288, \"sign\": 1, \"n\": 8968}, \"NOV_res\": {\"lo\": -0.9844771539499432, \"hi\": 0.09593876134862721, \"mu\": -0.540875353868789, \"sd\": 0.3801298233025086, \"sign\": 1, \"n\": 9475}, \"ego_density_W3\": {\"lo\": 0.0, \"hi\": 1.0, \"mu\": 0.7333316442122908, \"sd\": 0.2796180574838275, \"sign\": -1, \"n\": 6810}, \"edge_persistence\": {\"lo\": 0.0, \"hi\": 0.6739705882352984, \"mu\": 0.12122673391085216, \"sd\": 0.15763666320353067, \"sign\": -1, \"n\": 11236}}, \"all\": {\"new_edge_rate\": {\"lo\": 0.0, \"hi\": 1.3333333333333333, \"mu\": 0.2137749421116557, \"sd\": 0.18712524937508748, \"sign\": 1, \"n\": 12499}, \"n_comm_W3\": {\"lo\": 0.0, \"hi\": 8.0, \"mu\": 2.5383630690455234, \"sd\": 1.4439512430434749, \"sign\": 1, \"n\": 12499}, \"participation\": {\"lo\": 0.0, \"hi\": 0.8162630102040815, \"mu\": 0.3770766100053555, \"sd\": 0.2530890675222482, \"sign\": 1, \"n\": 12167}, \"NOV_res\": {\"lo\": -0.9817103130304184, \"hi\": 0.09383222083132174, \"mu\": -0.4551814113804676, \"sd\": 0.33277132442558904, \"sign\": 1, \"n\": 11747}, \"ego_density_W3\": {\"lo\": 0.0, \"hi\": 1.0, \"mu\": 0.6560566200808624, \"sd\": 0.22979526084840923, \"sign\": -1, \"n\": 11547}, \"edge_persistence\": {\"lo\": 0.0, \"hi\": 0.7083333333333333, \"mu\": 0.2470663128945874, \"sd\"\n                                                          0                    1\nci                                                      233                  346\nconcept_id                                          1918360              2874115\nqid                                                Q5357720            Q17099562\nname                         Electrical impedance myography  Persistent homology\nt0                                                     2016                 2016\nnewborn                                                   0                    0\nhome                                                     27                   31\nn_home                                                 30.0                 30.0\nweak_home                                                 0                    1\nintersect40                                               0                    0\nintersect25                                               0                    1\nhome_top_share                                     0.804444             0.366667\ngroup                                                   Med                 PHYS\nearly_volume                                           55.0                 77.0\nrole                                                primary              primary\nintersection_born                                         0                    0\nprecision_c                                             0.9                  1.0\nn_labelled_prec                                        10.0                 10.0\nprecision_source                                        llm                  llm\npass_gate                                              True                 True\nn_all_early                                              55                   77\nn_home_early                                             34                   13\nn_all_pre                                                30                   41\nn_home_pre                                               17                    7\nnew_edge_rate__all                                 0.166667                  0.2\nn_comm_W3__all                                          1.0                  6.0\nparticipation__all                                      0.0                 0.76\nNOV_res__all                                       0.094784            -0.310906\nego_density_W3__all                                     NaN             0.392857\nedge_persistence__all                              0.166667             0.133333\nM__all                                                    1                    3\nnew_edge_rate__home                                0.333333                  0.0\nn_comm_W3__home                                         1.0                  0.0\nparticipation__home                                     0.0                  NaN\nNOV_res__home                                      0.094874                  NaN\nego_density_W3__home                                    NaN                  NaN\nedge_persistence__home                                  0.0                  NaN\nM__home                                                   1                    0\nnew_edge_rate__sizematch                           0.227778                 0.15\nn_comm_W3__sizematch                                    0.6                  0.0\nparticipation__sizematch                              0.098                  NaN\nNOV_res__sizematch                                -0.019693                  NaN\nego_density_W3__sizematch                               NaN                  NaN\nedge_persistence__sizematch                        0.083333                  0.0\nM__sizematch                                            1.1                  0.5\nfp_logN                                            4.043051             4.304065\nfp_nfields                                                3                    8\nfp_reemerge                                               1                    1\nfp_wiki_pre                    \n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 573,\n  \"est\": 0.09059049284973039,\n  \"ci95_400boot\": [\n   0.010749623103553041,\n   0.1650051005616541\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.07152646838735872,\n  \"share_ge_observed\": 0.015\n },\n \"placebo_random_open_psp\": -0.027111739316867493,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 630,\n  \"est\": 0.17410165420736984,\n  \"ci95_400boot\": [\n   0.09568838543012635,\n   0.25899626408340093\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 573,\n  \"B5\": 0.7679289162717833,\n  \"B5_plus_OPEN_home\": 0.7703431304689959,\n  \"diff\": 0.0024142141972126607\n }\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-29 21:18:41 UTC

```
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF; cat > make_mini_data.py <<'EOF'
"""Build mini_demo_data.json: 100 fresh-cohort concepts (stratified by group x onset year) with every column that
rederive.py reads, plus the frozen OPEN constants and the full-cohort headline numbers for comparison."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

SRC = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10")
COMP = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
COLS = (["ci", "concept_id", "name", "t0", "agroup", "n_home_early"]
        + [f"{k}__{b}" for b in ("all", "home") for k in COMP]
        + ["OPEN_home", "OPEN_all", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH",
           "type", "generic", "level"])
F = pd.read_parquet(SRC / "data/features_cohort.parquet")[COLS]
O = pd.read_parquet(SRC / "data/outcomes_cohort.parquet")[["ci", "O2r_m50"]]
P = pd.read_parquet(SRC / "data/cohort_predictions.parquet")
D = F.merge(O, on="ci").merge(P, on="ci")
D = D.dropna(subset=["OPEN_home", "OPEN_all", "O2r_m50", "pred_b5", "pred_b5_open", "logvol", "growth_c",
                     "offhome_share", "entropy", "reach"]).reset_index(drop=True)
print("eligible", len(D))
# stratified sample: proportional to group x t0 cells, 100 concepts
rng = np.random.default_rng(0)
N = 100
cells = D.groupby(["agroup", "t0"]).indices
alloc = {k: max(1, round(N * len(v) / len(D))) for k, v in cells.items()}
while sum(alloc.values()) > N:
    k = max(alloc, key=alloc.get); alloc[k] -= 1
while sum(alloc.values()) < N:
    k = max(alloc, key=lambda c: len(cells[c]) - alloc[c]); alloc[k] += 1
pick = np.concatenate([rng.choice(v, alloc[k], replace=False) for k, v in cells.items()])
S = D.iloc[np.sort(pick)].reset_index(drop=True)
print(S.groupby(["agroup", "t0"]).size().to_string(), S["type"].value_counts().to_dict())


def clean(v):
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating, float)): return None if not np.isfinite(v) else float(v)
    if isinstance(v, (np.bool_,)): return bool(v)
    return v


rows = [{k: clean(v) for k, v in r.items()} for r in S.to_dict("records")]
spec = json.loads((SRC / "results/frozen_spec.json").read_text())
full = json.loads((SRC / "results/rederive.json").read_text())
out = {
    "description": "100 concepts from the fresh 2015-2017 OpenAlex onset cohort (stratified by analysis group x onset year, "
                   "restricted to concepts with OPEN_home, OPEN_all, the O2r_m50 outcome and frozen predictions). Each row has "
                   "the six raw ego-network components for the ALL and HOME builds, the frozen OPEN scores, the B5 + reach "
                   "covariates, LLM concept type/generic/level, the O2r_m50 outcome and the frozen B5 / B5+OPEN_home predictions.",
    "open_constants": {b: spec["open_constants"][b] for b in ("home", "all")},
    "full_cohort_rederive_result": full,
    "n_examples": len(rows),
    "examples": rows,
}
Path("mini_demo_data.json").write_text(json.dumps(out, indent=1))
print("wrote", len(rows))
EOF
python3 make_mini_data.py && ls -la mini_demo_data.json && head -c 1500 mini_demo_data.json
```

### [16] TOOL RESULT — Bash · 2026-09-29 21:18:43 UTC

```
{"stdout": "eligible 571\nagroup   t0  \nBGM+Med  2015    18\n         2016    16\n         2017    12\nCS+Eng   2015     6\n         2016     8\n         2017     5\nLIFEENV  2015     3\n         2016     2\n         2017     4\nMATHDEC  2015     1\n         2016     1\n         2017     1\nPHYS     2015     1\n         2016     2\n         2017     2\nSOC      2015     6\n         2016     7\n         2017     5 {'object': 57, 'method': 17, 'topic': 17, 'property': 9}\nwrote 100\n-rw-rw-rw- 1 aii-agent aii-agent 104481 Sep 29 21:18 mini_demo_data.json\n{\n \"description\": \"100 concepts from the fresh 2015-2017 OpenAlex onset cohort (stratified by analysis group x onset year, restricted to concepts with OPEN_home, OPEN_all, the O2r_m50 outcome and frozen predictions). Each row has the six raw ego-network components for the ALL and HOME builds, the frozen OPEN scores, the B5 + reach covariates, LLM concept type/generic/level, the O2r_m50 outcome and the frozen B5 / B5+OPEN_home predictions.\",\n \"open_constants\": {\n  \"home\": {\n   \"new_edge_rate\": {\n    \"lo\": 0.0,\n    \"hi\": 2.0,\n    \"mu\": 0.24226876611794407,\n    \"sd\": 0.29476323739891586,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"n_comm_W3\": {\n    \"lo\": 0.0,\n    \"hi\": 5.0,\n    \"mu\": 1.251940155212417,\n    \"sd\": 1.1109950408968348,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"participation\": {\n    \"lo\": 0.0,\n    \"hi\": 0.7422196372922436,\n    \"mu\": 0.23128455585636246,\n    \"sd\": 0.2522103838072288,\n    \"sign\": 1,\n    \"n\": 8968\n   },\n   \"NOV_res\": {\n    \"lo\": -0.9844771539499432,\n    \"hi\": 0.09593876134862721,\n    \"mu\": -0.540875353868789,\n    \"sd\": 0.3801298233025086,\n    \"sign\": 1,\n    \"n\": 9475\n   },\n   \"ego_density_W3\": {\n    \"lo\": 0.0,\n    \"hi\": 1.0,\n    \"mu\": 0.7333316442122908,\n    \"sd\": 0.2796180574838275,\n    \"sign\": -1,\n    \"n\": 6810\n   },\n   \"edge_persistence\": {\n    \"lo\": 0.0,\n    \"hi\": 0.6739705882352984,\n    \"mu\": 0.12122673391085216,\n    \"sd\": 0.15763666320353067,\n    \"sign\": -1,\n    \"n\": 11236\n   }\n  },\n  \"all\": {\n   \"new_edge_rate\": {\n    \"lo\": 0.0,\n    \"hi\": 1.33333333333", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-09-29 21:19:59 UTC

```
I've built `mini_demo_data.json`: 100 concepts from the cohort, sampled across groups and onset years. Next I'm writing the notebook and test-running it.
```

### [18] TOOL CALL — Bash · 2026-09-29 21:19:59 UTC

```
mkdir -p /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b6c96088-0c31-4c10-956e-70b479fbc32a/scratchpad; cat > /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b6c96088-0c31-4c10-956e-70b479fbc32a/scratchpad/build_nb.py <<'PYEOF'
import json, sys
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md(r'''
# Do open-neighbourhood concepts spread? Fresh-cohort test (demo)

This notebook demos the experiment **"Do open-neighbourhood concepts spread? Fresh-cohort test"**. It is a single-unseal check of the RQ1 openness claim (from EXP8) on a new cohort of OpenAlex legacy concepts with 2015-2017 onsets.

**The question.** A concept's *early ego-network* is the network of concepts it co-occurs with in its first years. Is a concept with a more **open** early ego-network (new edges, many communities, high participation, novel residual links, low density, low edge persistence) later used across **more disciplines**? Breadth is measured by `O2r_m50`, the rarefied number of venue fields at m = 50 papers, 6-8 years after onset. The test controls for the B5 baseline (volume, growth, off-home share, entropy, reach) and further covariates.

**OPEN** is the mean of six signed, z-scored ego-network components. Its clip/centre/scale constants were **frozen** on the 12,499 EXP5 concepts before the unseal. It is built from ALL papers or HOME-field papers only.

**What the original `method.py` is.** It is an *orchestrator*: it runs about 25 pipeline scripts in order. These cover OpenAlex snapshot passes, the LLM precision gate, LLM concept typing, ego-network construction, the sealed outcome unseal, audits and figures. That full pipeline needs a 100+ GB OpenAlex snapshot and paid LLM calls, so it cannot run in Colab.

**What this demo runs.** It does two things:
1. It shows the original orchestrator (`method.py`) verbatim, run with `--list` so it only prints the step order.
2. It runs the artifact's **independent re-derivation of the headline numbers** (`rederive.py`) nearly verbatim on a 100-concept subset of the cohort (`mini_demo_data.json`). This script uses only the raw per-concept tables and the frozen constants. It:
   - rebuilds OPEN_home / OPEN_all from the six raw components;
   - computes the partial Spearman of OPEN with `O2r_m50` at ladder rung R2, with a bootstrap CI;
   - runs a shuffled-outcome placebo and a random-OPEN placebo;
   - compares prediction quality of the frozen B5 model with the frozen B5 + OPEN_home model.

Full-cohort result (n = 573): OPEN_home partial Spearman is **+0.091 [+0.013, +0.171]** at R2. The verdict is CONFIRMED but marginal, and there is no practical prediction gain (B5 Spearman 0.768 vs 0.770). With only 100 concepts, the demo estimates are much noisier.
''')

code(r'''
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# All packages used here are pre-installed on Colab -- install locally only (at Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0', 'pyarrow==18.1.0')
''')

md(r'''
## Imports
The first block is the original import block of `method.py` (the orchestrator). The second is the original import block of `rederive.py` (the analysis this demo runs). `matplotlib` is added for the final visualization.
''')

code(r'''
# --- method.py (orchestrator) imports, as in the original ---
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# --- rederive.py imports, as in the original ---
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# --- added for the notebook's visualization ---
import matplotlib.pyplot as plt
''')

md(r'''
## Data loading
`mini_demo_data.json` holds 100 cohort concepts, sampled proportionally across analysis group × onset year. All of them have OPEN_home, OPEN_all, the outcome and the frozen predictions. It also holds the **frozen OPEN constants** (`open_constants`, from `results/frozen_spec.json`) and the full-cohort `rederive.json` result for comparison. The file is loaded from GitHub, with a local fallback.
''')

code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-4/experiment-10/demo/mini_demo_data.json"
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

code(r'''
data = load_data()
print(data["n_examples"], "concepts;", data["description"][:200], "...")
''')

md(r'''
## Config
The tunable parameters of the re-derivation. In the original script they are hard-coded as `range(400)` bootstrap draws, `range(200)` within-group permutations and the complete cohort. On 100 concepts the original values run in seconds, so the demo uses them unchanged.
''')

code(r'''
N_EXAMPLES = 100   # concepts used from mini_demo_data.json (max 100; the original used the full cohort, n = 573 / 630)
N_BOOT = 400       # bootstrap draws for the psp CI (original: 400)
N_PERM = 200       # within-group shuffled-outcome placebo draws (original: 200)
''')

md(r'''
## 1. The original orchestrator (`method.py`)
This is `method.py` verbatim. `STEPS` lists every pipeline stage in execution order:
- `s0`: pre-registration hash seal
- `s1`: candidate cohort
- `passC`: OpenAlex snapshot pass
- `s3`: coverage audit
- `s4`: LLM precision gate
- `s7`: ego networks for the EXP5 and cohort frames
- `s6`: covariates
- `s5`: LLM concept typing and its gate
- `s8`: selection on EXP5
- `s9`: the **single unseal** of the sealed outcomes
- then the learned-model replication, audit, tests, figures/outputs, report and `rederive`

`subprocess.run` would launch each script. Those scripts need the OpenAlex snapshot, so the only change here is calling `main()` with `--list`, which prints the step order without running anything.
''')

code(r'''
ROOT = Path.cwd()  # original: Path(__file__).resolve().parent (no __file__ in a notebook)
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


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only")
    ap.add_argument("--from", dest="start")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
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


# notebook: list the step order only (running the steps needs the OpenAlex snapshot + LLM access)
sys.argv = ["method.py", "--list"]
main()
''')

md(r'''
## 2. Load the per-concept tables (`rederive.py` setup)
The original reads three tables and one JSON file:
- `data/features_cohort.parquet`: raw ego-network components and covariates;
- `data/outcomes_cohort.parquet`: the `O2r_m50` outcome;
- `data/cohort_predictions.parquet`: the frozen predictions;
- `results/frozen_spec.json`: the frozen constants.

Here the same frames `F`, `O`, `P` and `spec` are built from `data`. After this cell, the code is the original.

`SIGN` holds the pre-registered direction of each component. Openness means **more** new edges, communities, participation and residual novelty, and **less** ego density and edge persistence.
''')

code(r'''
ex = pd.DataFrame(data["examples"]).iloc[:N_EXAMPLES]
spec = {"open_constants": data["open_constants"]}                      # original: results/frozen_spec.json
F = ex.drop(columns=["O2r_m50", "pred_b5", "pred_b5_open"])            # original: data/features_cohort.parquet
O = ex[["ci", "O2r_m50"]]                                               # original: data/outcomes_cohort.parquet
D = F.merge(O, on="ci")
SIGN = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
        "edge_persistence": -1}
print(D.shape)
D[["name", "t0", "agroup", "type", "OPEN_home", "OPEN_all", "O2r_m50"]].head()
''')

md(r'''
## 3. OPEN score, ladder design matrix and partial Spearman
- **`open_score(build)`** does four things for each of the six components. It clips the component to the frozen `[lo, hi]` range, centres and scales it with the frozen EXP5 `mu` / `sd`, and applies the sign. It then takes the mean over components. A score is kept only if at least 4 components exist. For the HOME build it also needs at least 10 home-field early papers.
- **`design(d)`** builds rung **R2** of the covariate ladder:
  - the intercept;
  - the ranks of the B5 covariates (`logvol`, `growth_c`, `offhome_share`, `entropy`, `reach`) plus `CONTACT_REACH`;
  - onset-year dummies;
  - LLM concept-type dummies, the `generic` flag and level dummies.
- **`psp(x, y, X)`** is the partial Spearman correlation. It ranks x and y, residualises both on X with a QR projection, and correlates the residuals. Collinear or empty dummy columns are dropped first, which matters on a 100-concept subset where some dummy levels are empty.
''')

code(r'''
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
''')

md(r'''
## 4. Re-derive OPEN, the R2 partial Spearman and its CI, plus the placebos
For each build (HOME, ALL) the loop does three things:
1. It checks that the rebuilt OPEN matches the frozen table (`max_abs_diff` should be 0).
2. It estimates the R2 partial Spearman of OPEN with `O2r_m50`, with an `N_BOOT`-draw percentile bootstrap CI.
3. For HOME only, it runs two placebos. The first shuffles the outcome **within analysis group** `N_PERM` times; the observed |psp| should sit in the tail of that null. The second computes the psp for a pure-noise OPEN, which should be about 0.

The only change from the original is that `range(400)` / `range(200)` became `range(N_BOOT)` / `range(N_PERM)`.
''')

code(r'''
out = {}
for b in ("home", "all"):
    o = open_score(b)
    out[f"OPEN_{b}_max_abs_diff_vs_frozen_table"] = float(np.nanmax(np.abs(o - F[f"OPEN_{b}"])))
    d = D.assign(o=o).dropna(subset=["o", "O2r_m50", "logvol", "growth_c", "offhome_share", "entropy", "reach"])
    d = d.reset_index(drop=True)
    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))
    rng = np.random.default_rng(1)
    bs = []
    for _ in range(N_BOOT):
        i = rng.integers(0, len(d), len(d))
        di = d.iloc[i].reset_index(drop=True)
        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))
    out[f"OPEN_{b}_psp_R2"] = {"n": len(d), "est": est, "ci95_400boot": [float(np.percentile(bs, 2.5)),
                                                                          float(np.percentile(bs, 97.5))]}
    out[f"_boot_{b}"] = bs  # notebook addition: keep the bootstrap draws for the plot below
    if b == "home":
        # placebo 1: within-group shuffled outcome; placebo 2: random OPEN
        perm = []
        for _ in range(N_PERM):
            y = d.O2r_m50.to_numpy().copy()
            for g in d.agroup.unique():
                m = (d.agroup == g).to_numpy()
                y[m] = rng.permutation(y[m])
            perm.append(psp(d.o.to_numpy(), y, design(d)))
        perm = np.abs(perm)
        out["placebo_shuffled_outcome"] = {"q95_abs": float(np.percentile(perm, 95)),
                                           "share_ge_observed": float((perm >= abs(est)).mean())}
        out["_perm_abs"] = perm  # notebook addition: keep the placebo null for the plot below
        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))
        out["placebo_random_open_psp"] = rnd
''')

md(r'''
## 5. Prediction check: frozen B5 vs frozen B5 + OPEN_home
Both OLS models were fitted on the EXP5 frame and frozen before the unseal. This cell compares the Spearman correlation of each model's predictions with the realised `O2r_m50`. On the full cohort the gain is only +0.002, meaning OPEN adds no practical prediction.
''')

code(r'''
P = ex[["ci", "pred_b5", "pred_b5_open"]].merge(O, on="ci").dropna()   # original: data/cohort_predictions.parquet
s0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]
out["prediction_spearman"] = {"n": len(P), "B5": float(s0), "B5_plus_OPEN_home": float(s1), "diff": float(s1 - s0)}
print(json.dumps({k: v for k, v in out.items() if not k.startswith("_")}, indent=1))
''')

md(r'''
## 6. Results: demo subset vs full cohort
The table below puts the demo numbers (100 concepts) next to the artifact's full-cohort `rederive.json`. The figure has three panels:
- **(a)** the R2 partial Spearman of OPEN_home and OPEN_all with 95% bootstrap CIs, demo vs full cohort;
- **(b)** the bootstrap distributions against the shuffled-outcome placebo null;
- **(c)** predicted vs realised breadth for the frozen B5 and B5 + OPEN_home models.

With n ≈ 100 the CIs are about 2.4× wider than on the full cohort (n = 573), so the demo estimate can land on either side of 0. The full-cohort numbers are the reference.
''')

code(r'''
full = data["full_cohort_rederive_result"]
rows = []
for b in ("home", "all"):
    k = f"OPEN_{b}_psp_R2"
    rows.append({"quantity": f"psp(OPEN_{b}, O2r_m50 | R2)",
                 "demo": f"{out[k]['est']:+.3f} [{out[k]['ci95_400boot'][0]:+.3f}, {out[k]['ci95_400boot'][1]:+.3f}] (n={out[k]['n']})",
                 "full cohort": f"{full[k]['est']:+.3f} [{full[k]['ci95_400boot'][0]:+.3f}, {full[k]['ci95_400boot'][1]:+.3f}] (n={full[k]['n']})"})
    rows.append({"quantity": f"OPEN_{b} rebuild max |diff| vs frozen table",
                 "demo": f"{out[f'OPEN_{b}_max_abs_diff_vs_frozen_table']:.2e}",
                 "full cohort": f"{full[f'OPEN_{b}_max_abs_diff_vs_frozen_table']:.2e}"})
rows.append({"quantity": "shuffled placebo: q95 |psp|", "demo": f"{out['placebo_shuffled_outcome']['q95_abs']:.3f}",
             "full cohort": f"{full['placebo_shuffled_outcome']['q95_abs']:.3f}"})
rows.append({"quantity": "shuffled placebo: share |psp| >= observed", "demo": f"{out['placebo_shuffled_outcome']['share_ge_observed']:.3f}",
             "full cohort": f"{full['placebo_shuffled_outcome']['share_ge_observed']:.3f}"})
rows.append({"quantity": "random-OPEN placebo psp", "demo": f"{out['placebo_random_open_psp']:+.3f}",
             "full cohort": f"{full['placebo_random_open_psp']:+.3f}"})
for k in ("B5", "B5_plus_OPEN_home", "diff"):
    rows.append({"quantity": f"prediction Spearman: {k}", "demo": f"{out['prediction_spearman'][k]:+.3f}",
                 "full cohort": f"{full['prediction_spearman'][k]:+.3f}"})
summary = pd.DataFrame(rows).set_index("quantity")
print(summary.to_string())

fig, axs = plt.subplots(1, 3, figsize=(15, 4.2))
# (a) psp with CI: demo vs full
ax = axs[0]
for j, (lab, src) in enumerate((("demo (100 concepts)", out), ("full cohort", full))):
    for i, b in enumerate(("home", "all")):
        r = src[f"OPEN_{b}_psp_R2"]
        ax.errorbar(i + (j - 0.5) * 0.25, r["est"], yerr=[[r["est"] - r["ci95_400boot"][0]], [r["ci95_400boot"][1] - r["est"]]],
                    fmt="o" if j == 0 else "s", color=["#1b6ca8", "#888888"][j], capsize=3, label=lab if i == 0 else None)
ax.axhline(0, color="k", lw=0.6)
ax.set_xticks([0, 1], ["OPEN_home", "OPEN_all"])
ax.set_ylabel("partial Spearman with O2r_m50 | R2 (95% CI)")
ax.set_title("(a) OPEN vs later disciplinary breadth")
ax.legend(frameon=False, fontsize=8)
# (b) bootstrap vs placebo null
ax = axs[1]
ax.hist(out["_boot_home"], bins=30, alpha=0.6, color="#1b6ca8", label="bootstrap psp, OPEN_home")
ax.hist(out["_boot_all"], bins=30, alpha=0.5, color="#c0392b", label="bootstrap psp, OPEN_all")
ax.hist(out["_perm_abs"], bins=30, alpha=0.5, color="#888888", label="|psp| shuffled-outcome placebo")
ax.axvline(out["OPEN_home_psp_R2"]["est"], color="#1b6ca8", ls="--")
ax.axvline(out["placebo_shuffled_outcome"]["q95_abs"], color="#555555", ls=":", label="placebo q95")
ax.set_xlabel("partial Spearman")
ax.set_title("(b) bootstrap vs placebo null (demo)")
ax.legend(frameon=False, fontsize=7)
# (c) predictions vs outcome
ax = axs[2]
ax.scatter(P.pred_b5, P.O2r_m50, s=14, alpha=0.6, label=f"B5 (Spearman {s0:.3f})")
ax.scatter(P.pred_b5_open, P.O2r_m50, s=14, alpha=0.6, marker="x", label=f"B5 + OPEN_home (Spearman {s1:.3f})")
lim = [min(P.pred_b5.min(), P.O2r_m50.min()), max(P.pred_b5.max(), P.O2r_m50.max())]
ax.plot(lim, lim, color="k", lw=0.6)
ax.set_xlabel("frozen prediction of O2r_m50")
ax.set_ylabel("realised O2r_m50 (fields @ m=50)")
ax.set_title("(c) frozen predictions (demo)")
ax.legend(frameon=False, fontsize=8)
plt.tight_layout()
plt.show()
''')

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
    c["source"] = c["source"].splitlines(keepends=True)
json.dump(nb, open(sys.argv[1], "w"), indent=1)
PYEOF
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF && python3 /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b6c96088-0c31-4c10-956e-70b479fbc32a/scratchpad/build_nb.py code_demo.ipynb && echo ok
```

### [19] TOOL RESULT — Bash · 2026-09-29 21:19:59 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [20] TOOL CALL — Bash · 2026-09-29 21:20:07 UTC

```
sed -i 's/N_BOOT = 400 /N_BOOT = 10 /; s/N_PERM = 200 /N_PERM = 10 /' code_demo.ipynb && grep -n "N_BOOT = \|N_PERM = " code_demo.ipynb && E=/tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [21] TOOL RESULT — Bash · 2026-09-29 21:20:37 UTC

```
{"stdout": "138:    \"N_BOOT = 10       # bootstrap draws for the psp CI (original: 400)\\n\",\n139:    \"N_PERM = 10       # within-group shuffled-outcome placebo draws (original: 200)\"\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 162040 bytes to code_demo.ipynb\n\nreal\t0m25.418s\nuser\t0m20.272s\nsys\t0m1.672s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] ASSISTANT · 2026-09-29 21:20:43 UTC

```
Minimal config passes (25 s). Scaling to the original 400/200 draws:
```

### [23] TOOL CALL — Bash · 2026-09-29 21:20:43 UTC

```
sed -i 's/N_BOOT = 10 /N_BOOT = 400 /; s/N_PERM = 10 /N_PERM = 200 /' code_demo.ipynb && grep -n "N_BOOT = \|N_PERM = " code_demo.ipynb && E=/tmp/aii_nb_test_envs/art_NMe386dX9GLF-0b2113e902d8 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; python3 - <<'EOF'
import json
nb=json.load(open("code_demo.ipynb"))
for c in nb["cells"]:
    if c["cell_type"]!="code": continue
    for o in c["outputs"]:
        if o.get("output_type")=="stream": print("".join(o["text"])[-2500:])
        elif o.get("output_type")=="error": print("ERR", o["ename"], o["evalue"])
        else: print("[", o["output_type"], list(o.get("data",{}).keys()), "]")
EOF
```

### [24] TOOL RESULT — Bash · 2026-09-29 21:21:07 UTC

```
{"stdout": "182:    \"N_BOOT = 400       # bootstrap draws for the psp CI (original: 400)\\n\",\n183:    \"N_PERM = 200       # within-group shuffled-outcome placebo draws (original: 200)\"\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 155876 bytes to code_demo.ipynb\n\nreal\t0m22.316s\nuser\t0m18.177s\nsys\t0m1.343s\n100 concepts; 100 concepts from the fresh 2015-2017 OpenAlex onset cohort (stratified by analysis group x onset year, restricted to concepts with OPEN_home, OPEN_all, the O2r_m50 outcome and frozen predictions). Ea ...\n\ns0\ns1\npassC\npassC_merge\ns3\ns4\ns4_retry\ns7_exp5\ns7_cohort\ns7_cohort_full\ns6\ns5_exp5\ns5_cohort\ns5_bench\ns5_sheet\ns5_gate\ns5_v2\ns5_m2all\ns8\ns9\nlearned\naudit\ntests\noutputs\nreport\nrederive\n\n(100, 30)\n\n[ execute_result ['text/html', 'text/plain'] ]\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.1053259175844299,\n  \"ci95_400boot\": [\n   -0.13246781718093978,\n   0.3340983296624912\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.193062073472901,\n  \"share_ge_observed\": 0.375\n },\n \"placebo_random_open_psp\": -0.08769447149512687,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.12316177235847509,\n  \"ci95_400boot\": [\n   -0.12727413815702454,\n   0.3261704005131703\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 100,\n  \"B5\": 0.7932997098736871,\n  \"B5_plus_OPEN_home\": 0.799216319284483,\n  \"diff\": 0.005916609410795859\n }\n}\n\n                                                                         demo                      full cohort\nquantity                                                                                                      \npsp(OPEN_home, O2r_m50 | R2)                  +0.105 [-0.132, +0.334] (n=100)  +0.091 [+0.011, +0.165] (n=573)\nOPEN_home rebuild max |diff| vs frozen table                         0.00e+00                         0.00e+00\npsp(OPEN_all, O2r_m50 | R2)                   +0.123 [-0.127, +0.326] (n=100)  +0.174 [+0.096, +0.259] (n=630)\nOPEN_all rebuild max |diff| vs frozen table                          0.00e+00                         0.00e+00\nshuffled placebo: q95 |psp|                                             0.193                            0.072\nshuffled placebo: share |psp| >= observed                               0.375                            0.015\nrandom-OPEN placebo psp                                                -0.088                           -0.027\nprediction Spearman: B5                                                +0.793                           +0.768\nprediction Spearman: B5_plus_OPEN_home                                 +0.799                           +0.770\nprediction Spearman: diff                                              +0.006                           +0.002\n\n[ display_data ['image/png', 'text/plain'] ]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-29 21:21:13 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b6c96088-0c31-4c10-956e-70b479fbc32a/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; grep -c GITHUB_DATA_URL code_demo.ipynb; grep -o 'GITHUB_DATA_URL = \\"[^\\]*' code_demo.ipynb; du -sh .
```

### [26] TOOL RESULT — Bash · 2026-09-29 21:21:13 UTC

```
{"stdout": "2\nGITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-4/experiment-10/demo/mini_demo_data.json\n1.5M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Read · 2026-09-29 21:21:13 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b6c96088-0c31-4c10-956e-70b479fbc32a/scratchpad/fig.png
```

### [28] TOOL RESULT — Read · 2026-09-29 21:21:14 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [29] THINKING · 2026-09-29 21:21:31 UTC

```
The notebook runs end-to-end in 22 seconds with the original parameters. Now I'll clean up the absolute path in the builder script and write the README, manifest, and struct output.
```

### [30] TOOL CALL — Bash · 2026-09-29 21:21:31 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path("make_mini_data.py"); s=p.read_text()
s=s.replace('import json\nfrom pathlib import Path', 'import json\nimport sys\nfrom pathlib import Path')
s=s.replace('SRC = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10")',
 'SRC = Path(sys.argv[1])  # the source experiment directory (holds data/ and results/)')
s=s.replace('rederive.py reads,', 'rederive.py reads,\n...', 0)
s=s.replace('plus the frozen OPEN constants and the full-cohort headline numbers for comparison."""',
 'plus the frozen OPEN constants and the full-cohort headline numbers for comparison.\n\nUsage: python make_mini_data.py <experiment_dir>"""')
p.write_text(s)
EOF
head -12 make_mini_data.py; grep -n "ai-inventor" make_mini_data.py code_demo.ipynb mini_demo_data.json | grep -v raw.githubusercontent | head
cat > README.md <<'EOF'
# Demo: do open-neighbourhood concepts spread? (fresh-cohort test)

This is a Colab-ready demo notebook for the experiment *"Do open-neighbourhood concepts spread? Fresh-cohort test"*. The experiment asks whether an OpenAlex concept whose early ego-network is more **open** is later used across more disciplines. The outcome is `O2r_m50`: the rarefied number of venue fields at m = 50 papers, 6-8 years after onset. The test controls for the B5 baseline and a covariate ladder.

The original `method.py` only orchestrates about 25 pipeline scripts. Those scripts need a full OpenAlex snapshot and LLM calls, so the notebook:

1. shows `method.py` verbatim and runs it with `--list`, which only prints the step order;
2. runs the artifact's independent re-derivation script (`rederive.py`) nearly verbatim on a 100-concept subset of the cohort. That script rebuilds OPEN from the six raw ego-network components with the frozen constants and computes the R2 partial Spearman with a 400-draw bootstrap CI. It also runs the shuffled-outcome and random-OPEN placebos and compares the frozen B5 predictions with the B5 + OPEN_home predictions.

The demo results are close to the full cohort's, with wider CIs because n = 100:

| quantity | demo (n=100) | full cohort |
|---|---|---|
| psp(OPEN_home, O2r_m50 \| R2) | +0.105 [-0.132, +0.334] | +0.091 [+0.011, +0.165] (n=573) |
| psp(OPEN_all, O2r_m50 \| R2) | +0.123 [-0.127, +0.326] | +0.174 [+0.096, +0.259] (n=630) |
| prediction Spearman, B5 → B5+OPEN_home | 0.793 → 0.799 | 0.768 → 0.770 |

## Layout

- `code_demo.ipynb`: the demo notebook, already executed with outputs. It takes about 25 s, plus package installs.
- `mini_demo_data.json`: 100 concepts from the cohort, sampled across analysis group × onset year. Each row has the raw ego-network components (ALL and HOME builds), the covariates, the LLM concept type, the outcome and the frozen predictions. The file also holds the frozen OPEN constants and the full-cohort `rederive.json` for comparison.
- `make_mini_data.py`: rebuilds `mini_demo_data.json` from the source experiment directory (`data/` and `results/`).
- `.aii/manifest.yaml`: the storage manifest. Nothing here is heavy.

## How to run

- **Colab:** open `code_demo.ipynb` and run all cells. The data loads from the GitHub raw URL.
- **Locally:** run `jupyter nbconvert --to notebook --execute code_demo.ipynb`. The notebook falls back to the local `mini_demo_data.json`.
- **Rebuild the demo data:** run `python make_mini_data.py <experiment_dir>`.

## Restoring removed files

No files are marked `delete` in `.aii/manifest.yaml`, so there is nothing to restore. Every file in this directory is small text or code.
EOF
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy in this workspace: all files are small text/code (< 2 MB total), so no decisions are required.
entries: []
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
ls -la; cat .aii/manifest.yaml
```

### [31] TOOL RESULT — Bash · 2026-09-29 21:21:33 UTC

```
{"stdout": "\"\"\"Build mini_demo_data.json: 100 fresh-cohort concepts (stratified by group x onset year) with every column that\nrederive.py reads, plus the frozen OPEN constants and the full-cohort headline numbers for comparison.\n\nUsage: python make_mini_data.py <experiment_dir>\"\"\"\nimport json\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\n\nSRC = Path(sys.argv[1])  # the source experiment directory (holds data/ and results/)\ntotal 2529\ndrwxrwxrwx 3 aii-agent aii-agent 1044758 Sep 29 21:21 .\ndrwxrwxrwx 4 aii-agent aii-agent 1070633 Sep 29 21:18 ..\ndrwxrwxrwx 2 aii-agent aii-agent   12300 Sep 29 21:21 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:17 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  194420 Sep 29 21:21 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent      97 Sep 29 21:21 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    2697 Sep 29 21:21 README.md\n-rw-rw-rw- 1 aii-agent aii-agent  155884 Sep 29 21:21 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent    3143 Sep 29 21:21 make_mini_data.py\n-rw-rw-rw- 1 aii-agent aii-agent  104481 Sep 29 21:18 mini_demo_data.json\n# Nothing heavy in this workspace: all files are small text/code (< 2 MB total), so no decisions are required.\nentries: []", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-29 21:21:42 UTC

```
I've built the demo notebook and its data file. The notebook runs cleanly from a fresh Colab-matched environment in about 22 seconds, using the original 400 bootstrap and 200 permutation draws.

The original `method.py` only launches about 25 other scripts in order. Those scripts need a full OpenAlex snapshot and paid LLM calls, so they can't run in Colab. The notebook therefore does two things:
- **Orchestrator:** `method.py` appears verbatim and is run with `--list`, so it prints the step order without launching anything. The only change is `ROOT = Path.cwd()`, because a notebook has no `__file__`.
- **Analysis:** the artifact's own `rederive.py` runs almost unchanged on 100 of the cohort's concepts. It independently recomputes the headline numbers: it rebuilds the openness score from the six raw components using the frozen constants, computes the partial correlation with a bootstrap confidence interval, and runs the placebo and prediction checks. The only edits are that the file paths now read from the loaded data and the draw counts are config variables.

**Results on the 100-concept subset, next to the full cohort:**

| Quantity | Demo (n = 100) | Full cohort |
|---|---|---|
| Openness score (home-only build) vs later breadth | +0.105 [−0.132, +0.334] | +0.091 [+0.011, +0.165] (n = 573) |
| Openness score (all-papers build) vs later breadth | +0.123 [−0.127, +0.326] | +0.174 [+0.096, +0.259] (n = 630) |
| Prediction quality, baseline → baseline + openness | 0.793 → 0.799 | 0.768 → 0.770 |

The rebuilt openness scores match the frozen table exactly. The point estimates are close to the full cohort's, but with only 100 concepts every interval includes zero. The notebook says the full-cohort numbers are the reference. The final cell prints this comparison and draws a three-panel figure: estimates with intervals, bootstrap vs placebo distributions, and predicted vs actual breadth.

**Checks:**
- The notebook contains the exact `GITHUB_DATA_URL` and uses the GitHub-with-local-fallback loader.
- `mini_demo_data.json` exists: 100 concepts sampled across analysis groups and onset years, plus the frozen constants and the full-cohort results.
- I couldn't keep a todo list because no todo tool was available in this session. I followed the six steps in order.

I also wrote the files the checker needs:
- `README.md`
- `.aii/manifest.yaml`, with no entries because nothing in the workspace is large
- `make_mini_data.py`, which rebuilds the data file and now takes the source folder as an argument instead of an absolute server path
- `.terminal_claude_agent_struct_out.json`

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
```
