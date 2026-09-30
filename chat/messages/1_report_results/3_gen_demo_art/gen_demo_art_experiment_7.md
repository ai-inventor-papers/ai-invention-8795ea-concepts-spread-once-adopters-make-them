# gen_demo_art_experiment_7 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_7` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:17:55 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:18:03 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/results/out.json`
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
id: art_dFQ6jbgNsR6Q
type: experiment
title: Which early network signals of new topics travel
summary: >-
  RQ1 held-out deliverable on the EXP5 frame (12,499 TAG-grounded OpenAlex concepts; DEV CS/Eng/BGM/Med 4,771; held-out PHYS
  742, LIFEENV 1,113, SOC 1,352, MATHDEC 165; 2010-14 cohort 2,484 DEV-home + 1,872 other). Two zero-credit OpenAlex S3 passes
  (Pass A reproduces EXP5 grounded counts exactly for all concepts; Pass B windowed citations). 53 indicators in 7 families
  over t0..t0+2 (popularity E, disciplinary F, landing G, retained-frontier FR, 27 co-occurrence ego-network A ported from
  EXP3 and validated to 1e-15, co-author S) plus B5 baseline. Outcomes: O1c/O1b uptake, O2r_m50/O2r_resid breadth, O3 transience,
  O4 field/year-normalised citation growth, O5/O5_WW external recognition (art_O7Dq4L02QnDN). DEV-only ranking (psp|B5, LOGO
  dAUC, refit bootstraps), frozen top-10s + ElasticNet/L1-logit + EBM, hash seal, single unseal, DL pooling, Holm. RESULTS:
  breadth is predictable beyond B5 and portable: 7/10 (O2r_m50) and 8/10 (O2r_resid) frozen indicators confirmed with 6/6
  unit sign agreement; M0_density_end psp +0.377 [0.280,0.466], D_vol_end +0.307, CONTACT_REACH +0.210, n_comm_W3 +0.164,
  NOV +0.152, ego_density_W3 -0.097, RETENTION_RATIO_early -0.120 (caveat: M0_density_end/D_vol_end use cumulative 1995..t0+2
  field history, i.e. partly a pre-onset footprint). O1c: only n_authors_early (+0.161). O4: REL_home -0.114, author_growth
  +0.065; EBM Spearman 0.188 vs B5 0.015. O5/O5_WW: no indicator or model beats B5+onset year. Learned: breadth ElasticNet
  0.765 vs B5 0.706 (+0.059 [0.046,0.073]). Pre-registered: P2 holds; P1,P3,P4,P5 fail. Robust to EXP6-overlap exclusion,
  coverage covariates, O2r_m30, EXP5 O2r_resid definition. Audits: T0-T8 pass; independent audit.py and rederive.py reproduce
  headline numbers, shuffled controls null. Key files: results/rq1_heldout.json, heldout_summary.json, portability_table.csv,
  learned_vs_single_heldout.json, prereg_verdicts.json, frozen_spec.json, deviations.json; figures/*; method_out.json (per-concept
  indicators, outcomes, predictions). Deviations: 1-yr ego windows (D family >30% missing so never frozen), betweenness cutoff
  3, O2r_resid per plan formula (EXP5 formula as sensitivity), linear onset-year term in O5 baselines. Second use of held-out
  outcomes (EXP5) disclosed; G family flagged previously scored.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-3/experiment-8/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-3/experiment-8/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-3/experiment-8/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 21:18:09 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 21:18:09 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 21:18:09 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 21:18:09 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 21:18:09 UTC

```
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls -la $W; wc -l $W/method.py; du -sh $W/*
```

### [8] TOOL RESULT — Bash · 2026-09-29 21:18:09 UTC

```
{"stdout": "total 2957\ndrwxrwxrwx 3 aii-agent aii-agent 1002285 Sep 29 21:17 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000188 Sep 29 21:16 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:16 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:17 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   23348 Sep 29 21:18 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:16 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002285 Sep 29 21:17 ..\ntotal 103012\ndrwxrwxrwx 15 aii-agent aii-agent  2045847 Sep 29 02:02 .\ndrwxrwxrwx  7 aii-agent aii-agent  2076345 Sep 28 21:29 ..\ndrwxrwxrwx  2 aii-agent aii-agent    67400 Sep 29 01:03 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 28 22:04 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent    12805 Sep 29 01:03 .aii_worker_result.json\ndrwxrwxrwx  8 aii-agent aii-agent  2000127 Sep 29 00:58 .git\n-rw-rw-rw-  1 aii-agent aii-agent       58 Sep 28 22:52 .gitignore\n-rw-rw-rw-  1 aii-agent aii-agent  4240606 Sep 29 01:03 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     2965 Sep 29 00:58 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    24369 Sep 29 01:00 README.md\n-rw-rw-rw-  1 aii-agent aii-agent     6911 Sep 29 00:52 audit.py\n-rw-rw-rw-  1 aii-agent aii-agent    14229 Sep 28 23:29 build_features.py\ndrwxrwxrwx  6 aii-agent aii-agent  2007277 Sep 29 00:35 data\n-rw-rw-rw-  1 aii-agent aii-agent    26217 Sep 28 22:42 dev_select.py\ndrwxrwxrwx  2 aii-agent aii-agent  2000168 Sep 29 00:53 figures\n-rw-rw-rw-  1 aii-agent aii-agent 40670893 Sep 29 00:55 full_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    22977 Sep 28 23:49 heldout.py\ndrwxrwxrwx  3 aii-agent aii-agent  2002001 Sep 28 22:05 inputs\ndrwxrwxrwx  2 aii-agent aii-agent  1016324 Sep 29 18:02 lib\ndrwxrwxrwx  2 aii-agent aii-agent  1021557 Sep 29 00:57 logs\n-rw-rw-rw-  1 aii-agent aii-agent    16806 Sep 29 00:54 make_outputs.py\n-rw-rw-rw-  1 aii-agent aii-agent     3283 Sep 28 22:43 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 36017353 Sep 29 00:54 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    31027 Sep 29 00:55 mini_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent  2005230 Sep 29 00:35 models\n-rw-rw-rw-  1 aii-agent aii-agent    13139 Sep 28 23:49 outcomes.py\ndrwxrwxrwx  3 aii-agent aii-agent  2016467 Sep 28 22:05 passA\n-rw-rw-rw-  1 aii-agent aii-agent    14385 Sep 28 22:10 passA.py\ndrwxrwxrwx  3 aii-agent aii-agent  2005733 Sep 28 22:05 passB\n-rw-rw-rw-  1 aii-agent aii-agent     7849 Sep 28 23:20 passB.py\n-rw-rw-rw-  1 aii-agent aii-agent    18465 Sep 29 00:55 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     2341 Sep 29 00:06 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent     4144 Sep 29 00:56 readme_tables.py\n-rw-rw-rw-  1 aii-agent aii-agent     7055 Sep 29 00:13 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent     6420 Sep 29 00:57 reproducibility.md\n-rw-rw-rw-  1 aii-agent aii-agent     1624 Sep 28 22:41 requirements.lock.txt\n-rwxrwxrwx  1 aii-agent aii-agent      870 Sep 28 22:41 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent  2001023 Sep 29 00:54 results\ndrwxrwxrwx  2 aii-agent aii-agent  1038834 Sep 28 22:05 snapshot\ndrwxrwxrwx  2 aii-agent aii-agent  1001594 Sep 28 22:46 tests\n68 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method.py\n24K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/README.md\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/audit.py\n14K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/build_features.py\n81M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data\n26K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/dev_select.py\n3.6M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/figures\n39M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/full_method_out.json\n23K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/heldout.py\n24M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs\n1.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib\n1.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/logs\n17K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/make_outputs.py\n3.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method.py\n35M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/method_out.json\n31K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/mini_method_out.json\n55M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models\n13K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/outcomes.py\n171M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA\n15K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passA.py\n63M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB\n8.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/passB.py\n19K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/preview_method_out.json\n2.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/pyproject.toml\n4.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/readme_tables.py\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/rederive.py\n6.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/reproducibility.md\n2.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/requirements.lock.txt\n1.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/restore.sh\n13M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results\n1.4M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/snapshot\n996K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/tests", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 21:18:11 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cat $W/method.py; cat $W/pyproject.toml; head -c 3000 $W/preview_method_out.json; echo; ls $W/results $W/lib $W/data $W/models $W/figures
```

### [10] TOOL RESULT — Bash · 2026-09-29 21:18:11 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"RQ1 held-out deliverable -- end-to-end orchestrator (idempotent; each step skips if its output exists).\n\n  0  tests/test_units.py            T0 unit tests (+ tests/t0_8_ego_port.py: the ego port reproduces EXP3 exactly)\n  1  passA.py                       zero-credit snapshot pass: grounded frame matches + work/topic/author ids, background\n  2  passB.py                       citations received by early works (O4) and by the reference sample\n  3  build_features.py              ~53 indicators in 7 families over t0..t0+2 (+ B5)\n  4  outcomes.py                    one outcome table; DEV rows / sealed HELDOUT+COHORT rows\n  5  dev_select.py                  DEV-only ranking (psp | B5, dAUC), top 10s, learned models, power, FREEZE + seal\n  6  heldout.py                     unseal ONCE; frozen scoring, DL pooling, Holm, portability, P1-P5, sensitivities\n  7  audit.py                       T7 independent re-derivation\n  8  make_outputs.py                rq1_heldout.json, figures, case exemplars, method_out.json\n\nUsage: python method.py [--from STEP] [--only STEP] [--workers 5]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport subprocess\nimport sys\nimport time\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\n\nfrom common import DATA, LOGS, RES, setup_logger  # noqa: E402\n\nPY = sys.executable\nSTEPS = [\n    (\"tests\", [[\"tests/test_units.py\"], [\"tests/t0_8_ego_port.py\"]], RES / \"t0_8_ego_port.json\"),\n    (\"passA\", [[\"passA.py\", \"--workers\", \"{w}\"], [\"passA.py\", \"--merge\"]], DATA / \"passA_info.json\"),\n    (\"passB\", [[\"passB.py\", \"--workers\", \"{w}\"], [\"passB.py\", \"--merge\"]], DATA / \"passB_info.json\"),\n    (\"features\", [[\"build_features.py\", \"--stage\", \"all\", \"--workers\", \"{w}\"]], RES / \"indicator_matrix.parquet\"),\n    (\"outcomes\", [[\"outcomes.py\"]], DATA / \"outcomes_sealed.parquet\"),\n    (\"dev_select\", [[\"dev_select.py\", \"--stage\", \"all\", \"--workers\", \"{w}\"]], LOGS / \"seal.log\"),\n    (\"heldout\", [[\"heldout.py\", \"--stage\", \"all\", \"--workers\", \"{w}\"]], RES / \"sensitivities_pooled.json\"),\n    (\"audit\", [[\"audit.py\"]], RES / \"audit.json\"),\n    (\"outputs\", [[\"make_outputs.py\"]], RES / \"rq1_heldout.json\"),\n]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--from\", dest=\"start\", default=None)\n    ap.add_argument(\"--only\", default=None)\n    ap.add_argument(\"--workers\", type=int, default=5)\n    a = ap.parse_args()\n    logger = setup_logger(\"method\")\n    names = [s[0] for s in STEPS]\n    i0 = names.index(a.start) if a.start else 0\n    for name, cmds, marker in STEPS[i0:]:\n        if a.only and name != a.only:\n            continue\n        if marker.exists() and not (a.only or a.start == name):\n            logger.info(f\"skip {name}: {marker.relative_to(ROOT)} exists\")\n            continue\n        for c in cmds:\n            cmd = [PY] + [x.format(w=a.workers) for x in c]\n            t = time.time()\n            logger.info(f\"run {' '.join(c)}\")\n            r = subprocess.run(cmd, cwd=ROOT)\n            if r.returncode != 0:\n                raise SystemExit(f\"step {name} failed ({' '.join(c)}), exit {r.returncode}\")\n            logger.info(f\"done {' '.join(c)} in {(time.time()-t)/60:.1f} min\")\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"rq1-heldout-indicators\"\nversion = \"0.1.0\"\ndescription = \"RQ1: which early network indicators of concept emergence travel across scientific domains (DEV freeze, sealed held-out scoring)\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"annotated-types==0.8.0\",\n  \"aplr==10.27.0\",\n  \"asttokens==3.0.2\",\n  \"blinker==1.9.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"comm==0.2.3\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"dash==4.4.1\",\n  \"dash-cytoscape==1.0.2\",\n  \"dill==0.4.1\",\n  \"executing==2.2.1\",\n  \"flask==3.1.3\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"gevent==26.9.0\",\n  \"greenlet==3.5.6\",\n  \"idna==3.20\",\n  \"igraph==1.0.0\",\n  \"importlib-metadata==9.0.1\",\n  \"interface-meta==2.0.1\",\n  \"interpret==0.7.8\",\n  \"interpret-core==0.7.8\",\n  \"ipython==9.17.1\",\n  \"ipython-pygments-lexers==1.1.1\",\n  \"ipywidgets==8.1.9\",\n  \"itsdangerous==2.2.0\",\n  \"janus==2.0.0\",\n  \"jedi==0.20.0\",\n  \"jinja2==3.1.6\",\n  \"joblib==1.6.0\",\n  \"jupyterlab-widgets==3.0.17\",\n  \"kiwisolver==1.5.1\",\n  \"leidenalg==0.12.0\",\n  \"llvmlite==0.49.0\",\n  \"loguru==0.7.3\",\n  \"markupsafe==3.0.3\",\n  \"matplotlib==3.11.2\",\n  \"matplotlib-inline==0.2.2\",\n  \"multiprocess==0.70.19\",\n  \"narwhals==2.26.0\",\n  \"nest-asyncio==1.6.0\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"parso==0.8.7\",\n  \"patsy==1.0.3\",\n  \"pexpect==4.9.0\",\n  \"pillow==12.3.0\",\n  \"plotly==7.1.0\",\n  \"prompt-toolkit==3.0.53\",\n  \"psutil==7.2.2\",\n  \"ptyprocess==0.7.0\",\n  \"pure-eval==0.2.4\",\n  \"pyahocorasick==2.3.1\",\n  \"pyarrow==25.0.1\",\n  \"pydantic==2.13.5\",\n  \"pydantic-core==2.46.5\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"python-dateutil==2.9.0.post0\",\n  \"python-igraph==1.0.0\",\n  \"pyyaml==6.0.3\",\n  \"requests==2.34.2\",\n  \"retrying==1.4.2\",\n  \"salib==1.6.0\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"setuptools==84.0.0\",\n  \"shap==0.52.0\",\n  \"six==1.17.0\",\n  \"slicer==0.0.8\",\n  \"snowballstemmer==3.1.1\",\n  \"stack-data==0.6.3\",\n  \"statsmodels==0.15.0\",\n  \"texttable==1.7.0\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"traitlets==5.16.1\",\n  \"typing-extensions==4.16.0\",\n  \"typing-inspection==0.4.4\",\n  \"urllib3==2.8.0\",\n  \"wcwidth==0.9.1\",\n  \"werkzeug==3.1.9\",\n  \"widgetsnbextension==4.0.16\",\n  \"wrapt==2.5.0\",\n  \"zipp==4.1.0\",\n  \"zope-event==6.2\",\n  \"zope-interface==8.6\",\n]\n{\n  \"metadata\": {\n    \"method_name\": \"RQ1 held-out indicator portability (DEV freeze -> sealed held-out scoring)\",\n    \"description\": \"One example per frame concept: input = the ~53 candidate indicators + B5 over t0..t0+2; output = the 8 outcomes; predict_* = B5-only, B5 + best single indicator (frozen DEV #1), ElasticNet/L1-logistic...\",\n    \"outcomes\": [\n      \"O1c\",\n      \"O2r_m50\",\n      \"O2r_resid\"\n    ],\n    \"indicators\": [\n      \"share\",\n      \"growth_ind\",\n      \"accel\"\n    ],\n    \"baseline\": [\n      \"logvol\",\n      \"growth_c\",\n      \"offhome_share\"\n    ]\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"rq1_cohort_2010_14_concepts\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Complete intersection\\\", \\\"concept_id\\\": \\\"C37253\\\", \\\"t0\\\": 2012, \\\"home_group\\\": \\\"MATHDEC\\\", \\\"indicators_t0_t0p2\\\": {\\\"share\\\": 3.848425, \\\"growth_ind\\\": 0.310155, \\\"accel\\\": 0.177303, \\\"burst\\\": 0.0, \\\"au...\",\n          \"output\": \"{\\\"O1c\\\": -0.212922, \\\"O2r_m50\\\": 2.960784, \\\"O2r_resid\\\": -1.481981, \\\"O4\\\": 0.144479, \\\"O1b\\\": 0.0, \\\"O3\\\": 0.0, \\\"O5\\\": null, \\\"O5_WW\\\": null}\",\n          \"metadata_split\": \"COHORT\",\n          \"metadata_unit\": \"COH_OTHER\",\n          \"metadata_ci\": 3,\n          \"metadata_prediction_type\": \"frozen DEV model applied once after the unseal\",\n          \"predict_B5_O1c\": \"0.428605\",\n          \"predict_best_single_O1c\": \"0.316920\",\n          \"predict_EBM_O1c\": \"0.190288\",\n          \"predict_linear_all_O1c\": \"0.362548\",\n          \"predict_B5_O2r_m50\": \"3.991043\",\n          \"predict_best_single_O2r_m50\": \"3.419979\",\n          \"predict_EBM_O2r_m50\": \"3.281189\",\n          \"predict_linear_all_O2r_m50\": \"3.085114\",\n          \"predict_B5_O2r_resid\": \"-0.451722\",\n          \"predict_best_single_O2r_resid\": \"-1.022786\",\n          \"predict_EBM_O2r_resid\": \"-1.106972\",\n          \"predict_linear_all_O2r_resid\": \"-1.236918\",\n          \"predict_B5_O4\": \"0.059010\",\n          \"predict_best_single_O4\": \"0.060190\",\n          \"predict_EBM_O4\": \"-0.136159\",\n          \"predict_linear_all_O4\": \"0.043606\",\n          \"predict_B5_O1b\": \"0.529306\",\n          \"predict_best_single_O1b\": \"0.448646\",\n          \"predict_EBM_O1b\": \"0.412613\",\n          \"predict_linear_all_O1b\": \"0.486887\",\n          \"predict_B5_O3\": \"0.035120\",\n          \"predict_best_single_O3\": \"0.079395\",\n          \"predict_EBM_O3\": \"0.071068\",\n          \"predict_linear_all_O3\": \"0.053725\",\n          \"predict_B5_O5\": \"0.096328\",\n          \"predict_best_single_O5\": \"0.107155\",\n          \"predict_EBM_O5\": \"0.267447\",\n          \"predict_linear_all_O5\": \"0.112239\",\n          \"predict_B5_O5_WW\": \"0.041720\",\n          \"predict_best_single_O5_WW\": \"0.046236\",\n          \"predict_EBM_O5_WW\": \"0.107915\",\n          \"predict_linear_all_O5_WW\": \"0.073493\"\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Early adopter\\\", \\\"concept_id\\\": \\\"C125502\\\", \\\"t0\\\": 2011, \\\"home_group\\\": \\\"SOC\\\", \\\"indicators_t0_t0p2\\\": {\\\"share\\\": 3.556216, \\\"growth_ind\\\": 0.367725, \\\"accel\\\": 0.306424, \\\"burst\\\": 0\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data:\nanalysis_table.parquet\nbg_topics.npz\ncites_early.parquet\ncounts_check.parquet\nego_features.parquet\nego_parts\nego_parts_c3\nego_timing\nfeatures_basic.parquet\nframe_arrays.npz\nframe_matches_early\no5_events.parquet\noutcomes.parquet\noutcomes_dev.parquet\noutcomes_sealed.parquet\npassA_info.json\npassB_info.json\npassB_targets.npy\nref_sample.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/figures:\nebm_shapes.pdf\nebm_shapes.png\nheldout_forest_O1b.pdf\nheldout_forest_O1b.png\nheldout_forest_O1c.pdf\nheldout_forest_O1c.png\nheldout_forest_O2r_m50.pdf\nheldout_forest_O2r_m50.png\nheldout_forest_O2r_resid.pdf\nheldout_forest_O2r_resid.png\nheldout_forest_O3.pdf\nheldout_forest_O3.png\nheldout_forest_O4.pdf\nheldout_forest_O4.png\nheldout_forest_O5.pdf\nheldout_forest_O5.png\nheldout_forest_O5_WW.pdf\nheldout_forest_O5_WW.png\nindicator_clusters.pdf\nindicator_clusters.png\nlearned_vs_single.pdf\nlearned_vs_single.png\no5_base_rates.pdf\no5_base_rates.png\nportability_heatmap.pdf\nportability_heatmap.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib:\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nframe_exp5.py\nh2.py\nindicators.py\nmatcher.py\nmodels_exp5.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal_exp5.py\nstats_core.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/models:\nebm_O1b.joblib\nebm_O1c.joblib\nebm_O2r_m50.joblib\nebm_O2r_resid.joblib\nebm_O3.joblib\nebm_O4.joblib\nebm_O5.joblib\nebm_O5_WW.joblib\nlinear_all_O1b.joblib\nlinear_all_O1c.joblib\nlinear_all_O2r_m50.joblib\nlinear_all_O2r_resid.joblib\nlinear_all_O3.joblib\nlinear_all_O4.joblib\nlinear_all_O5.joblib\nlinear_all_O5_WW.joblib\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results:\naudit.json\ncase_exemplars.json\nchecks.json\ndev_oof_predictions.parquet\ndev_ranking.csv\ndev_ranking_sensitivity.csv\ndeviations.json\nfeatures_config.json\nfrozen_spec.json\nheldout_predictions.parquet\nheldout_summary.json\nheldout_unit_results.csv\nindicator_clusters_dev.json\nindicator_corr_dev.csv\nindicator_dictionary.csv\nindicator_matrix.parquet\nlearned_model.json\nlearned_vs_single_heldout.json\no2r_resid_fit.json\no4_reference_expectations.csv\no5_join.json\noutcome_base_rates.json\nportability_table.csv\npower_dev.json\nprereg_b5_minus_reach.csv\nprereg_verdicts.json\nprovenance.json\nrederive.json\nrq1_dev_selection.json\nrq1_heldout.json\nsensitivities_heldout.csv\nsensitivities_pooled.json\nsize_diagnostic_dev.csv\nt0_8_ego_port.json\nt1_passA_exact_65_1125_1407_1918.json\nt4_ego_sanity.json\nt4_timing_nnull200_cut4.json\nunit_tests.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 21:18:17 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; python3 -c "
import json
d=json.load(open('mini_method_out.json'))
print(json.dumps(d['metadata'],indent=1)[:4000])
for ds in d['datasets']:
  print(ds['dataset'], len(ds['examples']))
  e=ds['examples'][0]
  print(json.dumps(json.loads(e['input']),indent=1)[:5000])
  print(e.keys())
"
```

### [12] TOOL RESULT — Bash · 2026-09-29 21:18:17 UTC

```
{"stdout": "{\n \"method_name\": \"RQ1 held-out indicator portability (DEV freeze -> sealed held-out scoring)\",\n \"description\": \"One example per frame concept: input = the ~53 candidate indicators + B5 over t0..t0+2; output = the 8 outcomes; predict_* = B5-only, B5 + best single indicator (frozen DEV #1), ElasticNet/L1-logistic on all indicators, and EBM, per outcome.\",\n \"outcomes\": [\n  \"O1c\",\n  \"O2r_m50\",\n  \"O2r_resid\",\n  \"O4\",\n  \"O1b\",\n  \"O3\",\n  \"O5\",\n  \"O5_WW\"\n ],\n \"indicators\": [\n  \"share\",\n  \"growth_ind\",\n  \"accel\",\n  \"burst\",\n  \"author_growth\",\n  \"n_authors_early\",\n  \"log_offhome_volume\",\n  \"rao_stirling\",\n  \"fields_gained_per_yr\",\n  \"G\",\n  \"G_A\",\n  \"G_btw\",\n  \"G_deg\",\n  \"G_phimin\",\n  \"REL_home\",\n  \"RS\",\n  \"CONTACT_REACH\",\n  \"RETAINED_REACH\",\n  \"RETENTION_RATIO_early\",\n  \"FRONTIER_POTENTIAL\",\n  \"D_rca_end\",\n  \"D_vol_end\",\n  \"M0_density_end\",\n  \"D_z\",\n  \"D_ratio\",\n  \"D_rare\",\n  \"D_sub\",\n  \"D_obs\",\n  \"NOV\",\n  \"NOV_res\",\n  \"F_res\",\n  \"F_z\",\n  \"deg_W1\",\n  \"deg_W3\",\n  \"deg_growth\",\n  \"str_growth\",\n  \"new_edge_rate\",\n  \"edge_persistence\",\n  \"turnover\",\n  \"participation\",\n  \"n_comm_W3\",\n  \"comm_entropy\",\n  \"comm_transitions\",\n  \"ego_density_W3\",\n  \"ego_density_change\",\n  \"btw_end\",\n  \"btw_change\",\n  \"kcore_end\",\n  \"constraint_end\",\n  \"constraint_change\",\n  \"S_comp\",\n  \"S_comp_n\",\n  \"S_isolated_share\"\n ],\n \"baseline\": [\n  \"logvol\",\n  \"growth_c\",\n  \"offhome_share\",\n  \"entropy\",\n  \"reach\"\n ]\n}\nrq1_cohort_2010_14_concepts 3\n{\n \"concept\": \"Complete intersection\",\n \"concept_id\": \"C37253\",\n \"t0\": 2012,\n \"home_group\": \"MATHDEC\",\n \"indicators_t0_t0p2\": {\n  \"share\": 3.848425,\n  \"growth_ind\": 0.310155,\n  \"accel\": 0.177303,\n  \"burst\": 0.0,\n  \"author_growth\": 0.405465,\n  \"n_authors_early\": 4.532599,\n  \"log_offhome_volume\": 2.397895,\n  \"rao_stirling\": 0.091606,\n  \"fields_gained_per_yr\": 1.0,\n  \"G\": 0.213796,\n  \"G_A\": 0.252659,\n  \"G_btw\": 0.056,\n  \"G_deg\": 0.488685,\n  \"G_phimin\": 0.416501,\n  \"REL_home\": 1.33968,\n  \"RS\": 0.23798,\n  \"CONTACT_REACH\": 2.0,\n  \"RETAINED_REACH\": 1.0,\n  \"RETENTION_RATIO_early\": 0.5,\n  \"FRONTIER_POTENTIAL\": 1.477727,\n  \"D_rca_end\": 2.0,\n  \"D_vol_end\": 2.0,\n  \"M0_density_end\": 0.05673,\n  \"D_z\": null,\n  \"D_ratio\": null,\n  \"D_rare\": null,\n  \"D_sub\": null,\n  \"D_obs\": null,\n  \"NOV\": null,\n  \"NOV_res\": null,\n  \"F_res\": -0.36206,\n  \"F_z\": -1.282886,\n  \"deg_W1\": 5.0,\n  \"deg_W3\": 6.0,\n  \"deg_growth\": 0.154151,\n  \"str_growth\": 0.047764,\n  \"new_edge_rate\": 0.0,\n  \"edge_persistence\": 0.614286,\n  \"turnover\": 0.2,\n  \"participation\": 0.0,\n  \"n_comm_W3\": 1.0,\n  \"comm_entropy\": -0.0,\n  \"comm_transitions\": 0.0,\n  \"ego_density_W3\": 0.866667,\n  \"ego_density_change\": -0.033333,\n  \"btw_end\": 3e-06,\n  \"btw_change\": 2e-06,\n  \"kcore_end\": 6.0,\n  \"constraint_end\": 0.218375,\n  \"constraint_change\": -0.071961,\n  \"S_comp\": 0.75,\n  \"S_comp_n\": 0.461538,\n  \"S_isolated_share\": 0.5,\n  \"logvol\": 4.290459,\n  \"growth_c\": 0.265703,\n  \"offhome_share\": 0.144928,\n  \"entropy\": 0.50234,\n  \"reach\": 3.0\n }\n}\ndict_keys(['input', 'output', 'metadata_split', 'metadata_unit', 'metadata_ci', 'metadata_prediction_type', 'predict_B5_O1c', 'predict_best_single_O1c', 'predict_EBM_O1c', 'predict_linear_all_O1c', 'predict_B5_O2r_m50', 'predict_best_single_O2r_m50', 'predict_EBM_O2r_m50', 'predict_linear_all_O2r_m50', 'predict_B5_O2r_resid', 'predict_best_single_O2r_resid', 'predict_EBM_O2r_resid', 'predict_linear_all_O2r_resid', 'predict_B5_O4', 'predict_best_single_O4', 'predict_EBM_O4', 'predict_linear_all_O4', 'predict_B5_O1b', 'predict_best_single_O1b', 'predict_EBM_O1b', 'predict_linear_all_O1b', 'predict_B5_O3', 'predict_best_single_O3', 'predict_EBM_O3', 'predict_linear_all_O3', 'predict_B5_O5', 'predict_best_single_O5', 'predict_EBM_O5', 'predict_linear_all_O5', 'predict_B5_O5_WW', 'predict_best_single_O5_WW', 'predict_EBM_O5_WW', 'predict_linear_all_O5_WW'])\nrq1_dev_concepts 3\n{\n \"concept\": \"Torque converter\",\n \"concept_id\": \"C39854\",\n \"t0\": 2004,\n \"home_group\": \"Eng\",\n \"indicators_t0_t0p2\": {\n  \"share\": 5.476314,\n  \"growth_ind\": -0.245122,\n  \"accel\": -0.06126,\n  \"burst\": 0.0,\n  \"author_growth\": -0.716678,\n  \"n_authors_early\": 4.430817,\n  \"log_offhome_volume\": 0.693147,\n  \"rao_stirling\": 0.036072,\n  \"fields_gained_per_yr\": 0.0,\n  \"G\": 0.097209,\n  \"G_A\": null,\n  \"G_btw\": 0.0,\n  \"G_deg\": 0.436383,\n  \"G_phimin\": 0.393321,\n  \"REL_home\": 0.015438,\n  \"RS\": 0.034075,\n  \"CONTACT_REACH\": 1.0,\n  \"RETAINED_REACH\": 0.0,\n  \"RETENTION_RATIO_early\": 0.0,\n  \"FRONTIER_POTENTIAL\": 0.0,\n  \"D_rca_end\": 0.0,\n  \"D_vol_end\": 0.0,\n  \"M0_density_end\": 0.032628,\n  \"D_z\": -5.643901,\n  \"D_ratio\": 0.194742,\n  \"D_rare\": null,\n  \"D_sub\": -4.050623,\n  \"D_obs\": 1.0,\n  \"NOV\": 0.0,\n  \"NOV_res\": -0.942442,\n  \"F_res\": 0.125316,\n  \"F_z\": 0.308408,\n  \"deg_W1\": 13.0,\n  \"deg_W3\": 5.0,\n  \"deg_growth\": -0.847298,\n  \"str_growth\": -0.885304,\n  \"new_edge_rate\": 0.142857,\n  \"edge_persistence\": 0.305556,\n  \"turnover\": 0.692308,\n  \"participation\": 0.0,\n  \"n_comm_W3\": 1.0,\n  \"comm_entropy\": -0.0,\n  \"comm_transitions\": 0.0,\n  \"ego_density_W3\": 0.7,\n  \"ego_density_change\": 0.174359,\n  \"btw_end\": 1.4e-05,\n  \"btw_change\": -6e-05,\n  \"kcore_end\": 5.0,\n  \"constraint_end\": 0.211547,\n  \"constraint_change\": 0.124618,\n  \"S_comp\": null,\n  \"S_comp_n\": null,\n  \"S_isolated_share\": null,\n  \"logvol\": 4.174387,\n  \"growth_c\": -0.367725,\n  \"offhome_share\": 0.018519,\n  \"entropy\": 0.092216,\n  \"reach\": 1.0\n }\n}\ndict_keys(['input', 'output', 'metadata_split', 'metadata_unit', 'metadata_ci', 'metadata_prediction_type', 'predict_B5_O1c', 'predict_best_single_O1c', 'predict_EBM_O1c', 'predict_linear_all_O1c', 'predict_B5_O2r_m50', 'predict_best_single_O2r_m50', 'predict_EBM_O2r_m50', 'predict_linear_all_O2r_m50', 'predict_B5_O2r_resid', 'predict_best_single_O2r_resid', 'predict_EBM_O2r_resid', 'predict_linear_all_O2r_resid', 'predict_B5_O4', 'predict_best_single_O4', 'predict_EBM_O4', 'predict_linear_all_O4', 'predict_B5_O1b', 'predict_best_single_O1b', 'predict_EBM_O1b', 'predict_linear_all_O1b', 'predict_B5_O3', 'predict_best_single_O3', 'predict_EBM_O3', 'predict_linear_all_O3', 'predict_B5_O5', 'predict_best_single_O5', 'predict_EBM_O5', 'predict_linear_all_O5', 'predict_B5_O5_WW', 'predict_best_single_O5_WW', 'predict_EBM_O5_WW', 'predict_linear_all_O5_WW'])\nrq1_heldout_concepts 3\n{\n \"concept\": \"Prospect theory\",\n \"concept_id\": \"C339426\",\n \"t0\": 2004,\n \"home_group\": \"SOC\",\n \"indicators_t0_t0p2\": {\n  \"share\": 6.246421,\n  \"growth_ind\": -0.03774,\n  \"accel\": -0.099042,\n  \"burst\": 0.0,\n  \"author_growth\": 0.430783,\n  \"n_authors_early\": 4.672829,\n  \"log_offhome_volume\": 3.401197,\n  \"rao_stirling\": 0.654843,\n  \"fields_gained_per_yr\": 0.5,\n  \"G\": 0.098171,\n  \"G_A\": 0.093785,\n  \"G_btw\": 0.021839,\n  \"G_deg\": 0.285994,\n  \"G_phimin\": 0.700877,\n  \"REL_home\": 0.362252,\n  \"RS\": 0.692409,\n  \"CONTACT_REACH\": 7.0,\n  \"RETAINED_REACH\": 3.0,\n  \"RETENTION_RATIO_early\": 0.428571,\n  \"FRONTIER_POTENTIAL\": 1.060691,\n  \"D_rca_end\": 3.0,\n  \"D_vol_end\": 4.0,\n  \"M0_density_end\": 0.09893,\n  \"D_z\": -1.822591,\n  \"D_ratio\": 0.758294,\n  \"D_rare\": null,\n  \"D_sub\": -2.071707,\n  \"D_obs\": 4.0,\n  \"NOV\": 0.833333,\n  \"NOV_res\": -0.118142,\n  \"F_res\": -0.340011,\n  \"F_z\": -0.986061,\n  \"deg_W1\": 5.0,\n  \"deg_W3\": 10.0,\n  \"deg_growth\": 0.606136,\n  \"str_growth\": 0.584121,\n  \"new_edge_rate\": 0.333333,\n  \"edge_persistence\": 0.25,\n  \"turnover\": 0.8,\n  \"participation\": 0.5952,\n  \"n_comm_W3\": 4.0,\n  \"comm_entropy\": 1.085245,\n  \"comm_transitions\": 1.0,\n  \"ego_density_W3\": 0.377778,\n  \"ego_density_change\": -0.122222,\n  \"btw_end\": 5e-05,\n  \"btw_change\": 3.7e-05,\n  \"kcore_end\": 9.0,\n  \"constraint_end\": 0.112144,\n  \"constraint_change\": -0.087856,\n  \"S_comp\": 1.0,\n  \"S_comp_n\": 0.725,\n  \"S_isolated_share\": 1.0,\n  \"logvol\": 4.304065,\n  \"growth_c\": 0.122602,\n  \"offhome_share\": 0.644444,\n  \"entropy\": 1.616613,\n  \"reach\": 4.0\n }\n}\ndict_keys(['input', 'output', 'metadata_split', 'metadata_unit', 'metadata_ci', 'metadata_prediction_type', 'predict_B5_O1c', 'predict_best_single_O1c', 'predict_EBM_O1c', 'predict_linear_all_O1c', 'predict_B5_O2r_m50', 'predict_best_single_O2r_m50', 'predict_EBM_O2r_m50', 'predict_linear_all_O2r_m50', 'predict_B5_O2r_resid', 'predict_best_single_O2r_resid', 'predict_EBM_O2r_resid', 'predict_linear_all_O2r_resid', 'predict_B5_O4', 'predict_best_single_O4', 'predict_EBM_O4', 'predict_linear_all_O4', 'predict_B5_O1b', 'predict_best_single_O1b', 'predict_EBM_O1b', 'predict_linear_all_O1b', 'predict_B5_O3', 'predict_best_single_O3', 'predict_EBM_O3', 'predict_linear_all_O3', 'predict_B5_O5', 'predict_best_single_O5', 'predict_EBM_O5', 'predict_linear_all_O5', 'predict_B5_O5_WW', 'predict_best_single_O5_WW', 'predict_EBM_O5_WW', 'predict_linear_all_O5_WW'])", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-29 21:18:25 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; cat lib/rq1stats.py | head -200; echo ======; sed -n 1,200p heldout.py
```

### [14] TOOL RESULT — Bash · 2026-09-29 21:18:25 UTC

```
{"stdout": "\"\"\"Statistics for RQ1: partial Spearman given a baseline (rank residualisation, refitted in every bootstrap\nresample), L2-logistic delta-AUC (leave-one-group-out, out-of-fold), DerSimonian-Laird pooling, Holm, sign tests.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\n\n# ----------------------------------------------------------------------------- partial Spearman\ndef dummies(v: np.ndarray, drop_first: bool = True) -> np.ndarray:\n    u = np.unique(v)\n    if len(u) <= 1:\n        return np.zeros((len(v), 0))\n    cols = u[1:] if drop_first else u\n    return (v[:, None] == cols[None, :]).astype(float)\n\n\ndef _resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:\n    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)\n    return Y - Z @ beta\n\n\ndef psp_point(x: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> float:\n    \"\"\"Pearson(resid(rank x ~ rank B + cat dummies), resid(rank y ~ same)). Rows must be complete.\"\"\"\n    Zc = [np.ones((len(x), 1))]\n    if B is not None and B.shape[1]:\n        Zc.append(rankdata(B, axis=0))\n    if cat is not None and cat.shape[1]:\n        Zc.append(cat)\n    Z = np.hstack(Zc)\n    R = _resid(Z, np.c_[rankdata(x), rankdata(y)])\n    sx, sy = R[:, 0].std(), R[:, 1].std()\n    if sx <= 1e-12 or sy <= 1e-12:\n        return float(\"nan\")\n    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])\n\n\ndef psp_boot(x, y, B, cat, n_boot: int, seed: int) -> dict:\n    \"\"\"Point + concept bootstrap (resample rows; ranks and residualisation recomputed in each resample).\"\"\"\n    ok = np.isfinite(x) & np.isfinite(y)\n    if B is not None:\n        ok &= np.all(np.isfinite(B), axis=1)\n    x, y = x[ok], y[ok]\n    Bs = B[ok] if B is not None else None\n    cs = cat[ok] if cat is not None else None\n    n = len(x)\n    if n < 20 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"rho\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"se\": float(\"nan\"), \"p\": float(\"nan\"),\n                \"boot\": np.array([])}\n    est = psp_point(x, y, Bs, cs)\n    rng = np.random.default_rng(seed)\n    bs = np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        bs[b] = psp_point(x[i], y[i], Bs[i] if Bs is not None else None, cs[i] if cs is not None else None)\n    bs = bs[np.isfinite(bs)]\n    lo, hi = np.percentile(bs, [2.5, 97.5]) if len(bs) else (np.nan, np.nan)\n    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))\n    se_z = float(np.std(z, ddof=1)) if len(z) > 2 else float(\"nan\")\n    ze = math.atanh(max(min(est, 0.999999), -0.999999)) if np.isfinite(est) else float(\"nan\")\n    p = float(2 * stats.norm.sf(abs(ze / se_z))) if se_z and np.isfinite(se_z) and se_z > 0 else float(\"nan\")\n    return {\"n\": int(n), \"rho\": est, \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"z\": ze, \"se_z\": se_z, \"p\": p, \"boot\": bs}\n\n\ndef spearman_raw(x, y) -> tuple[float, int]:\n    ok = np.isfinite(x) & np.isfinite(y)\n    if ok.sum() < 10 or np.unique(x[ok]).size < 3:\n        return float(\"nan\"), int(ok.sum())\n    return float(stats.spearmanr(x[ok], y[ok])[0]), int(ok.sum())\n\n\n# ----------------------------------------------------------------------------- L2 logistic (sklearn C=1 objective)\ndef logit_fit(X: np.ndarray, y: np.ndarray, lam: float = 1.0, iters: int = 50) -> np.ndarray:\n    \"\"\"Newton-IRLS for  sum log-loss + lam/2 ||w||^2 (intercept unpenalised). X excludes the intercept.\"\"\"\n    n, d = X.shape\n    A = np.c_[np.ones(n), X]\n    w = np.zeros(d + 1)\n    pen = np.full(d + 1, lam)\n    pen[0] = 0.0\n    for _ in range(iters):\n        eta = A @ w\n        p = 1 / (1 + np.exp(-np.clip(eta, -30, 30)))\n        g = A.T @ (p - y) + pen * w\n        W = p * (1 - p)\n        H = (A * W[:, None]).T @ A + np.diag(pen)\n        try:\n            step = np.linalg.solve(H, g)\n        except np.linalg.LinAlgError:\n            step = np.linalg.lstsq(H, g, rcond=None)[0]\n        w -= step\n        if np.max(np.abs(step)) < 1e-8:\n            break\n    return w\n\n\ndef logit_pred(w: np.ndarray, X: np.ndarray) -> np.ndarray:\n    return 1 / (1 + np.exp(-np.clip(w[0] + X @ w[1:], -30, 30)))\n\n\ndef auc(y: np.ndarray, s: np.ndarray) -> float:\n    y = np.asarray(y).astype(bool)\n    n1, n0 = y.sum(), (~y).sum()\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef _std_fit(X):\n    mu = X.mean(0)\n    sd = X.std(0)\n    sd[sd < 1e-12] = 1.0\n    return mu, sd\n\n\ndef logo_oof(X: np.ndarray, y: np.ndarray, grp: np.ndarray) -> np.ndarray:\n    \"\"\"Out-of-fold predictions, leave-one-group-out, standardisation fitted on the training folds.\"\"\"\n    pred = np.full(len(y), np.nan)\n    for g in np.unique(grp):\n        te = grp == g\n        tr = ~te\n        if y[tr].min() == y[tr].max():\n            continue\n        mu, sd = _std_fit(X[tr])\n        w = logit_fit((X[tr] - mu) / sd, y[tr])\n        pred[te] = logit_pred(w, (X[te] - mu) / sd)\n    return pred\n\n\ndef dauc_logo(Xb: np.ndarray, x: np.ndarray, y: np.ndarray, grp: np.ndarray) -> tuple[float, float, float]:\n    p0 = logo_oof(Xb, y, grp)\n    p1 = logo_oof(np.c_[Xb, x], y, grp)\n    ok = np.isfinite(p0) & np.isfinite(p1)\n    a0, a1 = auc(y[ok], p0[ok]), auc(y[ok], p1[ok])\n    return a1 - a0, a0, a1\n\n\ndef dauc_boot(Xb, x, y, grp, n_boot: int, seed: int) -> dict:\n    ok = np.all(np.isfinite(Xb), 1) & np.isfinite(x) & np.isfinite(y)\n    Xb, x, y, grp = Xb[ok], x[ok], y[ok].astype(float), grp[ok]\n    n = len(y)\n    if n < 50 or y.sum() < 10 or (n - y.sum()) < 10 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"dauc\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"p\": float(\"nan\"), \"boot\": np.array([])}\n    est, a0, a1 = dauc_logo(Xb, x, y, grp)\n    rng = np.random.default_rng(seed)\n    idx_by = {g: np.nonzero(grp == g)[0] for g in np.unique(grp)}\n    bs = []\n    for _ in range(n_boot):\n        i = np.concatenate([rng.choice(v, len(v)) for v in idx_by.values()])\n        bs.append(dauc_logo(Xb[i], x[i], y[i], grp[i])[0])\n    bs = np.array([b for b in bs if np.isfinite(b)])\n    se = float(np.std(bs, ddof=1)) if len(bs) > 2 else float(\"nan\")\n    return {\"n\": int(n), \"n_pos\": int(y.sum()), \"dauc\": est, \"auc_base\": a0, \"auc_full\": a1,\n            \"ci\": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) else [np.nan] * 2,\n            \"se\": se, \"p\": float(2 * stats.norm.sf(abs(est / se))) if se and se > 0 else float(\"nan\"), \"boot\": bs}\n\n\n# ----------------------------------------------------------------------------- pooling / multiplicity\ndef dersimonian_laird(b, se) -> dict:\n    \"\"\"EXP6 lib/stats_core.dersimonian_laird (verbatim logic).\"\"\"\n    b, se = np.asarray(b, float), np.asarray(se, float)\n    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n    b, se = b[ok], se[ok]\n    k = len(b)\n    if k == 0:\n        return {\"k\": 0, \"b\": float(\"nan\"), \"se\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"p\": float(\"nan\"),\n                \"tau2\": float(\"nan\"), \"I2\": float(\"nan\"), \"Q\": float(\"nan\")}\n    w = 1 / se**2\n    bf = (w * b).sum() / w.sum()\n    Q = float((w * (b - bf) ** 2).sum())\n    Cc = w.sum() - (w**2).sum() / w.sum()\n    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 and Cc > 0 else 0.0\n    ws = 1 / (se**2 + tau2)\n    bre = (ws * b).sum() / ws.sum()\n    sre = math.sqrt(1 / ws.sum())\n    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0\n    return {\"k\": k, \"b\": float(bre), \"se\": sre, \"ci\": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],\n            \"p\": float(2 * stats.norm.sf(abs(bre / sre))), \"tau2\": float(tau2), \"Q\": Q, \"I2\": float(I2)}\n\n\ndef holm(p: list[float]) -> list[float]:\n    p = np.asarray(p, float)\n    out = np.full(len(p), np.nan)\n    ok = np.isfinite(p)\n    idx = np.nonzero(ok)[0]\n    m = len(idx)\n    order = idx[np.argsort(p[idx])]\n    run = 0.0\n    for r, i in enumerate(order):\n        run = max(run, min(1.0, (m - r) * p[i]))\n        out[i] = run\n    return out.tolist()\n\n\ndef sign_test_two_sided(k_pos: int, n: int) -> float:\n    return float(stats.binomtest(k_pos, n, 0.5).pvalue) if n > 0 else float(\"nan\")\n======\n#!/usr/bin/env python3\n\"\"\"STEP 6: unseal ONCE (lib/seal.load_heldout) and score the frozen spec on the held-out groups and cohort parts.\n\n  * frozen top10 per outcome (+ union_top10) in every unit: psp | B5 (+ t0 dummies; + group dummies in cohort parts)\n    with 1,000 concept-bootstrap resamples (continuous); dAUC with the FROZEN DEV coefficients and a joint refit\n    bootstrap (resample DEV -> refit -> resample unit -> score) (binary)\n  * DL pooling over PHYS/LIFEENV/SOC/MATHDEC, sign agreement over 6 units, Holm within each outcome family\n  * learned (ElasticNet/L1-logit, EBM) vs B5 vs B5 + best single on the same units\n  * portability table (every indicator x 10 units x {O2r_m50, O2r_resid, O1c} + raw Spearman with O2r_m50)\n  * pre-registered predictions P1-P5; labelled post-seal sensitivities\nUsage: python heldout.py [--stage unseal|score|all] [--workers 5]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport multiprocessing as mp\nimport sys\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, EXP6, HELD_GROUPS, MODELS, RES, SEED, UNITS, jdump, setup_logger\nfrom indicators import B5, BIN_OUTCOMES, CONT_OUTCOMES, FAMILY_OF, INDICATORS, OUTCOMES, PREVIOUSLY_SCORED\n\nB_HELD = 1000\nB_PORT = 500\nB_SENS = 300\nMIN_POS = 20\nDEV_UNITS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nALL_UNITS = DEV_UNITS + UNITS\nG: dict = {}\n\n\ndef _init() -> None:\n    warnings.filterwarnings(\"ignore\")\n    G[\"A\"] = pd.read_parquet(DATA / \"analysis_table.parquet\")\n    G[\"spec\"] = json.loads((RES / \"frozen_spec.json\").read_text())\n\n\ndef cat_for(d: pd.DataFrame, unit: str) -> np.ndarray:\n    from rq1stats import dummies\n    parts = [dummies(d.t0.to_numpy())]\n    if unit in (\"COH_DEVHOME\", \"COH_OTHER\", \"ALL_DEV\"):\n        parts.append(dummies(d.group.to_numpy()))\n    return np.hstack(parts)\n\n\ndef std_b(d: pd.DataFrame, outcome: str, spec: dict) -> np.ndarray:\n    bs = spec[\"b5_spec\"]\n    from design import apply_design\n    Xb = apply_design(d, bs)\n    t0s = spec[\"learned\"].get(outcome, {}).get(\"t0_std\")\n    if outcome in (\"O5\", \"O5_WW\") and t0s:\n        Xb = np.c_[Xb, (d.t0.to_numpy(float) - t0s[0]) / t0s[1]]\n    return Xb\n\n\ndef job(args):\n    \"\"\"kind: cont | bin | port. Returns a dict row.\"\"\"\n    kind, ind, outcome, unit, nboot, seed, extra = args\n    from rq1stats import auc, logit_fit, logit_pred, psp_boot, spearman_raw\n    A = G[\"A\"]\n    spec = G[\"spec\"]\n    d = A[A.unit == unit] if unit != \"ALL_DEV\" else A[A.split == \"DEV\"]\n    if extra and extra.get(\"subset\") == \"no_exp6\":\n        d = d[~d.in_exp6]\n    if extra and extra.get(\"subset\") == \"no_intersection\":\n        d = d[d.intersect40 == 0]\n    y = d[outcome].to_numpy(float)\n    x = d[ind].to_numpy(float)\n    row = {\"indicator\": ind, \"outcome\": outcome, \"unit\": unit, \"kind\": kind}\n    if kind in (\"cont\", \"port\"):\n        cov = B5 + (extra.get(\"covs\", []) if extra else [])\n        if extra and extra.get(\"drop_reach\"):\n            cov = [c for c in cov if c != \"reach\"]\n        r = psp_boot(x, y, d[cov].to_numpy(float), cat_for(d, unit), nboot, seed)\n        raw, nraw = spearman_raw(x, y)\n        row.update(n=r[\"n\"], rho=r[\"rho\"], ci_lo=r[\"ci\"][0], ci_hi=r[\"ci\"][1], se=r[\"se\"], z=r.get(\"z\"),\n                   se_z=r.get(\"se_z\"), p=r[\"p\"], raw_rho=raw)\n        # raw Spearman CI (percentile bootstrap) for P1/P2\n        if kind == \"cont\" or (kind == \"port\" and outcome == \"O2r_m50\"):\n            ok = np.isfinite(x) & np.isfinite(y)\n            xs, ys = x[ok], y[ok]\n            rng = np.random.default_rng(seed + 1)\n            bs = []\n            if ok.sum() >= 20:\n                from scipy.stats import rankdata\n                for _ in range(min(nboot, 500)):\n                    i = rng.integers(0, len(xs), len(xs))\n                    bs.append(np.corrcoef(rankdata(xs[i]), rankdata(ys[i]))[0, 1])\n            row.update(raw_ci_lo=float(np.nanpercentile(bs, 2.5)) if bs else np.nan,\n                       raw_ci_hi=float(np.nanpercentile(bs, 97.5)) if bs else np.nan)\n        return row\n    # binary, frozen DEV coefficients + joint refit bootstrap\n    D = A[A.split == \"DEV\"]\n    yD = D[outcome].to_numpy(float)\n    okD = np.isfinite(yD) & np.isfinite(D[ind].to_numpy(float))\n    ok = np.isfinite(y) & np.isfinite(x)\n    npos = int(np.nansum(y[ok]))\n    row.update(n=int(ok.sum()), n_pos=npos)\n    if npos < MIN_POS or ok.sum() - npos < MIN_POS:\n        row.update(dauc=np.nan, status=f\"dropped (< {MIN_POS} positives or negatives)\")\n        return row\n    XbD = std_b(D, outcome, spec)[okD]\n    xD = D[ind].to_numpy(float)[okD]\n    mu, sd = float(xD.mean()), float(xD.std() or 1.0)\n    yD = yD[okD]\n    Xb = std_b(d, outcome, spec)[ok]\n    xs = (x[ok] - mu) / sd\n    yy = y[ok]\n    w0 = logit_fit(XbD, yD)\n    w1 = logit_fit(np.c_[XbD, (xD - mu) / sd], yD)\n    a0 = auc(yy, logit_pred(w0, Xb))\n    a1 = auc(yy, logit_pred(w1, np.c_[Xb, xs]))\n    rng = np.random.default_rng(seed)\n    grpD = D.group.to_numpy()[okD]\n    idxD = [np.nonzero(grpD == g)[0] for g in np.unique(grpD)]\n    bs = []\n    for _ in range(nboot):\n        i = np.concatenate([rng.choice(v, len(v)) for v in idxD])\n        ww0 = logit_fit(XbD[i], yD[i])\n        ww1 = logit_fit(np.c_[XbD[i], (xD[i] - mu) / sd], yD[i])\n        j = rng.integers(0, len(yy), len(yy))\n        bs.append(auc(yy[j], logit_pred(ww1, np.c_[Xb[j], xs[j]])) - auc(yy[j], logit_pred(ww0, Xb[j])))\n    bs = np.array([b for b in bs if np.isfinite(b)])\n    se = float(np.std(bs, ddof=1))\n    from scipy import stats\n    row.update(dauc=a1 - a0, auc_base=a0, auc_full=a1, ci_lo=float(np.percentile(bs, 2.5)),\n               ci_hi=float(np.percentile(bs, 97.5)), se=se,\n               p=float(2 * stats.norm.sf(abs((a1 - a0) / se))) if se > 0 else np.nan, status=\"scored\")\n    return row\n\n\ndef run(jobs, workers, logger, label):\n    t = time.time()\n    out = []\n    with ProcessPoolExecutor(workers, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex:\n        for i, r in enumerate(ex.map(job, jobs, chunksize=2)):\n            out.append(r)\n            if (i + 1) % 100 == 0 or i + 1 == len(jobs):\n                logger.info(f\"{label}: {i+1}/{len(jobs)} ({(time.time()-t)/60:.1f} min)\")\n    return pd.DataFrame(out)\n\n\ndef stage_unseal(logger) -> None:\n    import seal\n    held = seal.load_heldout()\n    X = pd.read_parquet(RES / \"indicator_matrix.parquet\")\n    dev = pd.read_parquet(DATA / \"outcomes_dev.parquet\")\n    Y = pd.concat([dev, held], ignore_index=True)\n    Y.to_parquet(DATA / \"outcomes.parquet\", index=False)\n    A = X.merge(Y[[\"ci\"] + OUTCOMES + [\"O5_sens\", \"O5_WW_sens\", \"O2r_m30\", \"O2r_resid_N\"]], on=\"ci\", how=\"left\")\n    e6 = pd.read_csv(EXP6 / \"results/frame_concepts.csv\")\n    idcol = \"concept_id\" if \"concept_id\" in e6.columns else e6.columns[0]\n    ids = set(pd.to_numeric(e6[idcol].astype(str).str.extract(r\"C?(\\d+)$\")[0], errors=\"coerce\").dropna()\n              .astype(np.int64))\n    A[\"in_exp6\"] = A.concept_id.astype(np.int64).isin(ids)\n    A.to_parquet(DATA / \"analysis_table.parquet\", index=False)\n    logger.info(f\"UNSEALED: {len(held)} held-out/cohort rows; analysis table {A.shape}; in_exp6 {int(A.in_exp6.sum())}\")\n\n\ndef pool_block(tab: pd.DataFrame, value: str, se: str) -> dict:\n    from rq1stats import dersimonian_laird\n    t = tab[tab.unit.isin(HELD_GROUPS)]\n    return dersimonian_laird(t[value].to_numpy(float), t[se].to_numpy(float))\n\n\ndef stage_score(logger, workers: int) -> None:\n    from rq1stats import holm, sign_test_two_sided\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    top = spec[\"top10\"]\n    union = spec[\"union_top10\"]\n    jobs = []\n    for o in OUTCOMES:\n        if o not in top:\n            continue\n        inds = list(dict.fromkeys([d[\"indicator\"] for d in top[o]] + union))\n        kind = \"cont\" if o in CONT_OUTCOMES else \"bin\"\n        for i, ind in enumerate(inds):\n            for u in UNITS:\n                jobs.append((kind, ind, o, u, B_HELD, SEED + 31 * i, None))\n    t = time.time()\n    tab = run(jobs, workers, logger, \"held-out frozen scoring\")\n    tab.to_csv(RES / \"heldout_unit_results.csv\", index=False)\n    # --------------- pooling, signs, Holm\n    summary = {}\n    for o in top:\n        is_c = o in CONT_OUTCOMES\n        members = [d[\"indicator\"] for d in top[o]]\n        inds = list(dict.fromkeys(members + union))\n        rows = []\n        for ind in inds:\n            tt = tab[(tab.outcome == o) & (tab.indicator == ind)]\n            sgn = spec[\"signs\"][o].get(ind, 1)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-29 21:18:39 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cd $W; sed -n 200,480p heldout.py; echo =====; python3 -c "
import json
s=json.load(open('results/frozen_spec.json')); print(s.keys()); print(json.dumps(s['top10'])[:1500]); print(s['union_top10']); print(json.dumps(s['signs'])[:500]); print(json.dumps(s['b5_spec'])[:800])
h=json.load(open('results/heldout_summary.json')); print(type(h), list(h.keys())[:20] if isinstance(h,dict) else len(h)); print(json.dumps(h)[:2500])
"; cat lib/common.py | grep -n "UNITS\|HELD_GROUPS\|SEED" ; grep -n "B5\s*=\|CONT_OUTCOMES\|BIN_OUTCOMES" lib/indicators.py
```

### [16] TOOL RESULT — Bash · 2026-09-29 21:18:39 UTC

```
{"stdout": "            sgn = spec[\"signs\"][o].get(ind, 1)\n            if is_c:\n                pl = pool_block(tt, \"z\", \"se_z\")\n                est = float(np.tanh(pl[\"b\"])) if pl[\"k\"] else np.nan\n                ci = [float(np.tanh(pl[\"ci\"][0])), float(np.tanh(pl[\"ci\"][1]))] if pl[\"k\"] else [np.nan] * 2\n                vals = tt.set_index(\"unit\").rho\n            else:\n                pl = pool_block(tt[tt.status == \"scored\"], \"dauc\", \"se\")\n                est, ci = pl[\"b\"], pl[\"ci\"]\n                vals = tt.set_index(\"unit\").dauc\n            signs = [int(np.sign(v)) == sgn for v in vals.reindex(UNITS).to_numpy() if np.isfinite(v)]\n            k_agree = int(sum(signs))\n            rows.append({\"indicator\": ind, \"family\": FAMILY_OF[ind], \"in_top10\": ind in members,\n                         \"in_union\": ind in union, \"frozen_sign\": sgn, \"pooled\": est, \"pooled_ci\": ci,\n                         \"pooled_p\": pl.get(\"p\"), \"tau2\": pl.get(\"tau2\"), \"I2\": pl.get(\"I2\"), \"k\": pl.get(\"k\"),\n                         \"sign_agree\": k_agree, \"n_units\": len(signs),\n                         \"sign_test_p\": sign_test_two_sided(k_agree, len(signs)),\n                         \"previously_scored\": ind in PREVIOUSLY_SCORED,\n                         \"per_unit\": {u: (None if not np.isfinite(v) else float(v))\n                                      for u, v in vals.reindex(UNITS).items()},\n                         \"per_unit_ci\": {r.unit: [r.ci_lo, r.ci_hi] for r in tt.itertuples()\n                                         if np.isfinite(getattr(r, \"ci_lo\", np.nan))},\n                         \"per_unit_n\": {r.unit: int(r.n) for r in tt.itertuples()}})\n        hp = holm([r[\"pooled_p\"] for r in rows if r[\"in_top10\"]])\n        k = 0\n        for r in rows:\n            if r[\"in_top10\"]:\n                r[\"holm_p\"] = hp[k]; k += 1\n                r[\"confirmed\"] = bool(np.isfinite(r[\"holm_p\"]) and r[\"holm_p\"] < 0.05\n                                      and np.sign(r[\"pooled\"]) == r[\"frozen_sign\"])\n        summary[o] = rows\n    jdump(summary, RES / \"heldout_summary.json\")\n    logger.info(f\"held-out scoring done in {(time.time()-t)/60:.1f} min\")\n\n\ndef stage_portability(logger, workers: int) -> None:\n    feats = INDICATORS + B5\n    jobs = []\n    for o in (\"O2r_m50\", \"O2r_resid\", \"O1c\"):\n        for i, ind in enumerate(feats):\n            for u in ALL_UNITS:\n                jobs.append((\"port\", ind, o, u, B_PORT, SEED + 7 * i, None))\n    tab = run(jobs, workers, logger, \"portability\")\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    frozen = {(o, d[\"indicator\"]) for o, lst in spec[\"top10\"].items() for d in lst}\n    tab[\"family\"] = tab.indicator.map(lambda c: FAMILY_OF.get(c, \"B5\"))\n    tab[\"status\"] = [(\"FROZEN\" if (o, i) in frozen else \"EXPLORATORY\") for o, i in zip(tab.outcome, tab.indicator)]\n    tab[\"previously_scored\"] = tab.indicator.isin(PREVIOUSLY_SCORED)\n    tab[\"unit_type\"] = tab.unit.map(lambda u: \"DEV\" if u in DEV_UNITS else (\"HELDOUT\" if u in HELD_GROUPS else \"COHORT\"))\n    cols = [\"indicator\", \"family\", \"unit\", \"unit_type\", \"outcome\", \"n\", \"rho\", \"ci_lo\", \"ci_hi\", \"raw_rho\",\n            \"raw_ci_lo\", \"raw_ci_hi\", \"status\", \"previously_scored\", \"se_z\", \"z\", \"p\"]\n    tab[[c for c in cols if c in tab.columns]].to_csv(RES / \"portability_table.csv\", index=False)\n    logger.info(f\"portability table: {len(tab)} rows\")\n\n\ndef stage_learned(logger) -> None:\n    \"\"\"Learned vs single vs B5 on the SAME held-out units (frozen models), paired concept bootstrap vs B5.\"\"\"\n    import joblib\n    from scipy.stats import spearmanr\n    from design import apply_design\n    from rq1stats import auc, logit_pred\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    A = pd.read_parquet(DATA / \"analysis_table.parquet\")\n    lm = json.loads((RES / \"learned_model.json\").read_text())\n    rng = np.random.default_rng(SEED)\n    res = {}\n    preds_all = []\n    for o, m in spec[\"learned\"].items():\n        is_bin = o in BIN_OUTCOMES\n        d = A[A.split != \"DEV\"].copy()\n        X = apply_design(d, spec[\"design_spec\"])\n        Xb = apply_design(d, spec[\"b5_spec\"])\n        extra = np.zeros((len(d), 0))\n        if m.get(\"t0_std\"):\n            extra = ((d.t0.to_numpy(float) - m[\"t0_std\"][0]) / m[\"t0_std\"][1])[:, None]\n        b_all = np.c_[Xb, extra]\n        P = {}\n        if is_bin:\n            P[\"B5\"] = logit_pred(np.array(m[\"B5_coef\"]), b_all)\n        else:\n            c = np.array(m[\"B5_coef\"]); P[\"B5\"] = c[0] + b_all @ c[1:]\n        if m.get(\"best_single\"):\n            mu, sd, med = m[\"best_single_std\"]\n            t1 = d[m[\"best_single\"]].to_numpy(float)\n            t1 = (np.where(np.isfinite(t1), t1, med) - mu) / sd\n            c = np.array(m[\"B5_best_single_coef\"])\n            P[\"B5_best_single\"] = logit_pred(c, np.c_[b_all, t1]) if is_bin else c[0] + np.c_[b_all, t1] @ c[1:]\n        lin = joblib.load(MODELS / f\"linear_all_{o}.joblib\")\n        P[\"linear_all\"] = lin.predict_proba(np.c_[X, extra])[:, 1] if is_bin else lin.predict(X)\n        if (MODELS / f\"ebm_{o}.joblib\").exists():\n            e = joblib.load(MODELS / f\"ebm_{o}.joblib\")\n            P[\"EBM\"] = e.predict_proba(np.c_[X, extra])[:, 1] if is_bin else e.predict(X)\n        pr = pd.DataFrame({\"ci\": d.ci.to_numpy(), **{f\"{o}__{k}\": v for k, v in P.items()}})\n        preds_all.append(pr.set_index(\"ci\"))\n        y = d[o].to_numpy(float)\n        res[o] = {}\n        for u in UNITS + [\"POOLED_HELDOUT\"]:\n            mk = (d.unit.isin(HELD_GROUPS) if u == \"POOLED_HELDOUT\" else (d.unit == u)).to_numpy() & np.isfinite(y)\n            if mk.sum() < 30 or (is_bin and (y[mk].sum() < MIN_POS or (1 - y[mk]).sum() < MIN_POS)):\n                res[o][u] = {\"n\": int(mk.sum()), \"status\": \"dropped\"}\n                continue\n            yy = y[mk]\n\n            def metric(p, yv):\n                if is_bin:\n                    return auc(yv, p)\n                return float(spearmanr(p, yv)[0])\n            r = {\"n\": int(mk.sum())}\n            for k, p in P.items():\n                pp = p[mk]\n                r[k] = {\"metric\": metric(pp, yy)}\n                if is_bin:\n                    r[k][\"brier\"] = float(np.mean((pp - yy) ** 2))\n                    lo = np.log(np.clip(pp, 1e-6, 1 - 1e-6) / (1 - np.clip(pp, 1e-6, 1 - 1e-6)))\n                    from rq1stats import logit_fit\n                    w = logit_fit(lo[:, None], yy, lam=1e-6)\n                    r[k][\"calibration_slope\"] = float(w[1])\n                else:\n                    r[k][\"r2\"] = float(1 - np.sum((yy - pp) ** 2) / np.sum((yy - yy.mean()) ** 2))\n            bs = {k: [] for k in P if k != \"B5\"}\n            for _ in range(500):\n                j = rng.integers(0, len(yy), len(yy))\n                b0 = metric(P[\"B5\"][mk][j], yy[j])\n                for k in bs:\n                    bs[k].append(metric(P[k][mk][j], yy[j]) - b0)\n            for k, v in bs.items():\n                v = np.array(v)\n                r[k][\"delta_vs_B5\"] = r[k][\"metric\"] - r[\"B5\"][\"metric\"]\n                r[k][\"delta_ci\"] = [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))]\n            res[o][u] = r\n    jdump(res, RES / \"learned_vs_single_heldout.json\")\n    pd.concat(preds_all, axis=1).reset_index().to_parquet(RES / \"heldout_predictions.parquet\", index=False)\n    logger.info(\"learned vs single scored\")\n\n\ndef stage_prereg(logger, workers: int) -> None:\n    \"\"\"P1-P5 verdicts from the portability table (+ B5-minus-reach runs for P4/P5).\"\"\"\n    from rq1stats import dersimonian_laird\n    port = pd.read_csv(RES / \"portability_table.csv\")\n    jobs = [(\"cont\", ind, o, u, B_HELD, SEED + 99, {\"drop_reach\": True})\n            for ind in (\"RETENTION_RATIO_early\", \"FRONTIER_POTENTIAL\", \"CONTACT_REACH\")\n            for o in (\"O2r_resid\", \"O1c\") for u in HELD_GROUPS]\n    nr = run(jobs, workers, logger, \"P4/P5 given B5-minus-reach\")\n    nr.to_csv(RES / \"prereg_b5_minus_reach.csv\", index=False)\n\n    def pooled(tab, ind, o):\n        t = tab[(tab.indicator == ind) & (tab.outcome == o) & tab.unit.isin(HELD_GROUPS)]\n        pl = dersimonian_laird(t.z.to_numpy(float), t.se_z.to_numpy(float))\n        if not pl[\"k\"]:\n            return np.nan, [np.nan, np.nan], t\n        return float(np.tanh(pl[\"b\"])), [float(np.tanh(pl[\"ci\"][0])), float(np.tanh(pl[\"ci\"][1]))], t\n\n    def raw_groups(ind):\n        t = port[(port.indicator == ind) & (port.outcome == \"O2r_m50\") & port.unit.isin(HELD_GROUPS)]\n        return int((t.raw_ci_lo > 0).sum()), t\n    V = {}\n    # P1\n    det = {}\n    ok_raw = True\n    for ind in (\"entropy\", \"D_rare\", \"D_ratio\", \"participation\", \"NOV_res\"):\n        k, t = raw_groups(ind)\n        det[ind] = {\"n_groups_raw_CI_gt0\": k, \"raw_rho\": dict(zip(t.unit, t.raw_rho))}\n        ok_raw &= k >= 3\n    ok_small = True\n    for ind in (\"D_rare\", \"D_ratio\", \"participation\", \"NOV_res\"):\n        est, ci, _ = pooled(port, ind, \"O2r_m50\")\n        det[ind].update(pooled_psp=est, pooled_ci=ci)\n        ok_small &= bool(np.isfinite(ci[1]) and ci[1] < 0.10)\n    V[\"P1\"] = {\"verdict\": \"HOLDS\" if (ok_raw and ok_small) else \"FAILS\", \"raw_part_holds\": bool(ok_raw),\n               \"adds_little_part_holds\": bool(ok_small), \"detail\": det}\n    # P2\n    est, ci, _ = pooled(port, \"edge_persistence\", \"O2r_m50\")\n    t = port[(port.indicator == \"edge_persistence\") & (port.outcome == \"O2r_m50\") & port.unit.isin(HELD_GROUPS)]\n    raw_mean = float(t.raw_rho.mean())\n    V[\"P2\"] = {\"verdict\": \"HOLDS\" if (raw_mean < 0 and est < 0) else \"FAILS\", \"pooled_psp\": est, \"pooled_ci\": ci,\n               \"mean_raw_rho_4_groups\": raw_mean, \"raw_rho\": dict(zip(t.unit, t.raw_rho))}\n    # P3\n    det = {}\n    allfail = True\n    for ind in (\"deg_growth\", \"str_growth\", \"new_edge_rate\"):\n        est, ci, t = pooled(port, ind, \"O2r_m50\")\n        s = np.sign(t.rho.to_numpy(float))\n        flips = int(min((s > 0).sum(), (s < 0).sum()))\n        fails = bool((ci[0] <= 0 <= ci[1]) or flips >= 2)\n        dev_cs = port[(port.indicator == ind) & (port.outcome == \"O2r_m50\") & (port.unit == \"CS\")]\n        det[ind] = {\"pooled_psp\": est, \"pooled_ci\": ci, \"sign_flips\": flips, \"fails_heldout\": fails,\n                    \"dev_CS_psp\": float(dev_cs.rho.iloc[0]) if len(dev_cs) else None}\n        allfail &= fails\n    V[\"P3\"] = {\"verdict\": \"HOLDS\" if allfail else \"FAILS\", \"detail\": det}\n    # P4\n    det = {}\n    ok4 = True\n    for ind in (\"RETENTION_RATIO_early\", \"FRONTIER_POTENTIAL\"):\n        for o in (\"O2r_resid\", \"O1c\"):\n            est, ci, _ = pooled(port, ind, o)\n            est2, ci2, _ = pooled(nr, ind, o)\n            det[f\"{ind}|{o}\"] = {\"pooled_psp\": est, \"pooled_ci\": ci, \"given_B5_minus_reach\": est2,\n                                 \"ci_B5_minus_reach\": ci2}\n            ok4 &= bool(np.isfinite(ci[0]) and ci[0] > 0)\n    V[\"P4\"] = {\"verdict\": \"HOLDS\" if ok4 else \"FAILS\", \"detail\": det}\n    est, ci, _ = pooled(port, \"CONTACT_REACH\", \"O2r_m50\")\n    est2, ci2, _ = pooled(nr, \"CONTACT_REACH\", \"O2r_resid\")\n    V[\"P5\"] = {\"verdict\": \"HOLDS\" if (ci[0] <= 0 <= ci[1]) else \"FAILS\", \"pooled_psp_O2r_m50\": est, \"pooled_ci\": ci,\n               \"given_B5_minus_reach_O2r_resid\": est2, \"ci_B5_minus_reach\": ci2}\n    jdump(V, RES / \"prereg_verdicts.json\")\n    logger.info(\"prereg verdicts: \" + \", \".join(f\"{k}={v['verdict']}\" for k, v in V.items()))\n\n\ndef stage_sens(logger, workers: int) -> None:\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    jobs = []\n    for o in (\"O2r_resid\", \"O1c\"):\n        for d_ in spec[\"top10\"].get(o, []):\n            ind = d_[\"indicator\"]\n            for u in HELD_GROUPS:\n                jobs.append((\"cont\", ind, o, u, B_SENS, SEED + 5, {\"subset\": \"no_exp6\", \"tag\": \"excl_in_exp6\"}))\n                jobs.append((\"cont\", ind, o, u, B_SENS, SEED + 5, {\"subset\": \"no_intersection\", \"tag\": \"excl_intersection\"}))\n                jobs.append((\"cont\", ind, o, u, B_SENS, SEED + 5, {\"covs\": [\"label_coverage_early\", \"tag_coverage\",\n                                                                             \"precision_c\"], \"tag\": \"coverage_covs\"}))\n    for d_ in spec[\"top10\"].get(\"O2r_resid\", []):\n        for u in HELD_GROUPS:\n            jobs.append((\"cont\", d_[\"indicator\"], \"O2r_resid_N\", u, B_SENS, SEED + 5, {\"tag\": \"O2r_resid_N_exp5_definition\"}))\n    for d_ in spec[\"top10\"].get(\"O2r_m50\", []):\n        for u in HELD_GROUPS:\n            jobs.append((\"cont\", d_[\"indicator\"], \"O2r_m30\", u, B_SENS, SEED + 5, {\"tag\": \"O2r_m30\"}))\n    for o, o2 in ((\"O5\", \"O5_sens\"), (\"O5_WW\", \"O5_WW_sens\")):\n        for d_ in spec[\"top10\"].get(o, []):\n            for u in UNITS:\n                jobs.append((\"bin\", d_[\"indicator\"], o2, u, B_SENS, SEED + 5, {\"tag\": \"relation_same_or_narrower\"}))\n    tags = [j[6][\"tag\"] for j in jobs]\n    tab = run(jobs, workers, logger, \"sensitivities\")\n    tab[\"sensitivity\"] = tags\n    tab.to_csv(RES / \"sensitivities_heldout.csv\", index=False)\n    from rq1stats import dersimonian_laird\n    summ = []\n    for (s, o, ind), t in tab[tab.unit.isin(HELD_GROUPS)].groupby([\"sensitivity\", \"outcome\", \"indicator\"]):\n        if \"z\" in t and t.z.notna().any():\n            pl = dersimonian_laird(t.z.to_numpy(float), t.se_z.to_numpy(float))\n            summ.append({\"sensitivity\": s, \"outcome\": o, \"indicator\": ind, \"pooled\": float(np.tanh(pl[\"b\"])) if pl[\"k\"] else None,\n                         \"ci\": [float(np.tanh(c)) for c in pl[\"ci\"]] if pl[\"k\"] else None, \"I2\": pl.get(\"I2\")})\n        elif \"dauc\" in t:\n            tt = t[t.get(\"status\", pd.Series(\"\")).eq(\"scored\")] if \"status\" in t else t\n            pl = dersimonian_laird(tt.dauc.to_numpy(float), tt.se.to_numpy(float)) if len(tt) else {\"k\": 0}\n            summ.append({\"sensitivity\": s, \"outcome\": o, \"indicator\": ind, \"pooled\": pl.get(\"b\"), \"ci\": pl.get(\"ci\"),\n                         \"I2\": pl.get(\"I2\")})\n    jdump(summ, RES / \"sensitivities_pooled.json\")\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--stage\", default=\"all\")\n    ap.add_argument(\"--workers\", type=int, default=5)\n    a = ap.parse_args()\n    logger = setup_logger(\"heldout\")\n    st = a.stage\n    if st in (\"all\", \"unseal\"):\n        stage_unseal(logger)\n    if st in (\"all\", \"score\"):\n        stage_score(logger, a.workers)\n    if st in (\"all\", \"learned\"):\n        stage_learned(logger)\n    if st in (\"all\", \"port\"):\n        stage_portability(logger, a.workers)\n    if st in (\"all\", \"prereg\"):\n        stage_prereg(logger, a.workers)\n    if st in (\"all\", \"sens\"):\n        stage_sens(logger, a.workers)\n\n\nif __name__ == \"__main__\":\n    main()\n=====\ndict_keys(['indicators', 'windows', 'features_config', 'B5', 'baseline_extra', 'psp_covariates', 'sensitivity_covariates', 'O2r_resid', 'O5_rules', 'top10', 'union_top10', 'signs', 'learned', 'design_spec', 'b5_spec', 'bootstrap', 'holm_families', 'pooling', 'power', 'preregistered_predictions', 'sha256'])\n{\"O1c\": [{\"indicator\": \"n_authors_early\", \"sign\": 1, \"est\": 0.09655205543164243, \"ci\": [0.06503094904028472, 0.12816604245710692], \"status\": \"eligible\", \"family\": \"E\"}, {\"indicator\": \"burst\", \"sign\": 1, \"est\": 0.05379668711608551, \"ci\": [0.022079038896682047, 0.08259189759811213], \"status\": \"eligible\", \"family\": \"E\"}, {\"indicator\": \"S_comp_n\", \"sign\": -1, \"est\": -0.05194312934059405, \"ci\": [-0.08097767248805716, -0.020525917896883294], \"status\": \"eligible\", \"family\": \"S\"}, {\"indicator\": \"CONTACT_REACH\", \"sign\": 1, \"est\": 0.05129724419959896, \"ci\": [0.020728554867137598, 0.0800612445846362], \"status\": \"eligible\", \"family\": \"FR\"}, {\"indicator\": \"author_growth\", \"sign\": 1, \"est\": 0.048862611130835086, \"ci\": [0.0199404410416292, 0.07490782359430798], \"status\": \"eligible\", \"family\": \"E\"}, {\"indicator\": \"growth_ind\", \"sign\": 1, \"est\": 0.03595574037767238, \"ci\": [0.0068499815910869405, 0.0636465783449603], \"status\": \"eligible\", \"family\": \"E\"}, {\"indicator\": \"comm_transitions\", \"sign\": -1, \"est\": -0.03568134304249678, \"ci\": [-0.06569630659480517, -0.007454171612808672], \"status\": \"eligible\", \"family\": \"A\"}, {\"indicator\": \"share\", \"sign\": 1, \"est\": 0.029800968359365677, \"ci\": [-0.004157658372985316, 0.06076795585389336], \"status\": \"filled\", \"family\": \"E\"}, {\"indicator\": \"fields_gained_per_yr\", \"sign\": 1, \"est\": 0.028924583611860684, \"ci\": [-4.015130680900842e-05, 0.055739389351164355], \"status\": \"filled\", \"family\": \"F\"}, {\"indicator\": \"new_edge_rate\", \"sign\": 1, \"est\": 0.0267654629664\n['S_comp_n', 'G_phimin', 'G', 'G_btw', 'REL_home', 'n_authors_early', 'rao_stirling', 'D_vol_end', 'CONTACT_REACH', 'M0_density_end']\n{\"O1c\": {\"share\": 1, \"growth_ind\": 1, \"accel\": 1, \"burst\": 1, \"author_growth\": 1, \"n_authors_early\": 1, \"log_offhome_volume\": 1, \"rao_stirling\": -1, \"fields_gained_per_yr\": 1, \"G\": -1, \"G_A\": 1, \"G_btw\": 1, \"G_deg\": 1, \"G_phimin\": -1, \"REL_home\": -1, \"RS\": -1, \"CONTACT_REACH\": 1, \"RETAINED_REACH\": 1, \"RETENTION_RATIO_early\": -1, \"FRONTIER_POTENTIAL\": 1, \"D_rca_end\": 1, \"D_vol_end\": -1, \"M0_density_end\": 1, \"D_z\": -1, \"D_ratio\": -1, \"D_rare\": -1, \"D_sub\": -1, \"D_obs\": 1, \"NOV\": -1, \"NOV_res\": -1,\n{\"cols\": [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"], \"median\": {\"logvol\": 4.219507705176107, \"growth_c\": -0.0339015804503378, \"offhome_share\": 0.1914893686771392, \"entropy\": 0.7059860821254011, \"reach\": 3.0}, \"flag\": [], \"mean\": {\"logvol\": 4.261049858517607, \"growth_c\": -0.03617905142196925, \"offhome_share\": 0.2454435671253153, \"entropy\": 0.7267584534454062, \"reach\": 2.9436176902116955}, \"sd\": {\"logvol\": 0.3436208920364866, \"growth_c\": 0.49364958595278796, \"offhome_share\": 0.20071584648612426, \"entropy\": 0.4663688334004332, \"reach\": 1.4318760245308504}}\n<class 'dict'> ['O1c', 'O2r_m50', 'O2r_resid', 'O4', 'O1b', 'O3', 'O5', 'O5_WW']\n{\"O1c\": [{\"indicator\": \"n_authors_early\", \"family\": \"E\", \"in_top10\": true, \"in_union\": true, \"frozen_sign\": 1, \"pooled\": 0.16097217592859014, \"pooled_ci\": [0.09006822898811072, 0.23025258110184765], \"pooled_p\": 1.0050807699732313e-05, \"tau2\": 0.0034922073267782392, \"I2\": 0.7036389083518305, \"k\": 4, \"sign_agree\": 6, \"n_units\": 6, \"sign_test_p\": 0.03125, \"previously_scored\": false, \"per_unit\": {\"PHYS\": 0.1251489749905933, \"LIFEENV\": 0.1182721763937073, \"SOC\": 0.23561787129182743, \"MATHDEC\": 0.1480399549855075, \"COH_DEVHOME\": 0.17050352850979322, \"COH_OTHER\": 0.13970394633871577}, \"per_unit_ci\": {\"PHYS\": [0.05230840714305774, 0.2042907476475076], \"LIFEENV\": [0.05528153162863838, 0.17753242951563417], \"SOC\": [0.18225864942693656, 0.2845941621269767], \"MATHDEC\": [-0.03315620523590732, 0.3194991734815962], \"COH_DEVHOME\": [0.12749007194255266, 0.20980824179783378], \"COH_OTHER\": [0.09332915293098511, 0.18701084674293347]}, \"per_unit_n\": {\"PHYS\": 742, \"LIFEENV\": 1113, \"SOC\": 1352, \"MATHDEC\": 165, \"COH_DEVHOME\": 2484, \"COH_OTHER\": 1872}, \"holm_p\": 0.00010050807699732313, \"confirmed\": true}, {\"indicator\": \"burst\", \"family\": \"E\", \"in_top10\": true, \"in_union\": false, \"frozen_sign\": 1, \"pooled\": 0.018646529906902822, \"pooled_ci\": [-0.05208614439819835, 0.0891930492081417], \"pooled_p\": 0.6055789870007119, \"tau2\": 0.0033538457423647216, \"I2\": 0.6890581517354707, \"k\": 4, \"sign_agree\": 4, \"n_units\": 6, \"sign_test_p\": 0.6875, \"previously_scored\": false, \"per_unit\": {\"PHYS\": 0.07195641114324997, \"LIFEENV\": 0.05034664851478747, \"SOC\": -0.06074560505433155, \"MATHDEC\": 0.022367481608022797, \"COH_DEVHOME\": 0.10611663257739176, \"COH_OTHER\": -0.014198923497803499}, \"per_unit_ci\": {\"PHYS\": [-0.0047358872399726965, 0.14617080565150145], \"LIFEENV\": [-0.009654155001808757, 0.10840284389019805], \"SOC\": [-0.12146420089120417, 0.0008161499597336775], \"MATHDEC\": [-0.1427975750451656, 0.18229192707412722], \"COH_DEVHOME\": [0.06622197805355214, 0.14743884170502933], \"COH_OTHER\": [-0.0614665703694154, 0.035799512028618634]}, \"per_unit_n\": {\"PHYS\": 742, \"LIFEENV\": 1113, \"SOC\": 1352, \"MATHDEC\": 165, \"COH_DEVHOME\": 2484, \"COH_OTHER\": 1872}, \"holm_p\": 1.0, \"confirmed\": false}, {\"indicator\": \"S_comp_n\", \"family\": \"S\", \"in_top10\": true, \"in_union\": true, \"frozen_sign\": -1, \"pooled\": -0.08666108015637443, \"pooled_ci\": [-0.20049432836562478, 0.029480969744343662], \"pooled_p\": 0.14338343646733656, \"tau2\": 0.011581246859618527, \"I2\": 0.8805925693401084, \"k\": 4, \"sign_agree\": 6, \"n_units\": 6, \"sign_test_\n38:SEED = 20260928\n49:HELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\n50:UNITS = HELD_GROUPS + [\"COH_DEVHOME\", \"COH_OTHER\"]\n4:B5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\n67:CONT_OUTCOMES = [\"O1c\", \"O2r_m50\", \"O2r_resid\", \"O4\"]\n68:BIN_OUTCOMES = [\"O1b\", \"O3\", \"O5\", \"O5_WW\"]\n69:OUTCOMES = CONT_OUTCOMES + BIN_OUTCOMES", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-09-29 21:18:45 UTC

```
Building the demo data now: I'm picking 100 held-out concepts (25 per domain) plus the frozen spec, then I'll write the notebook around the original held-out scoring code.
```

### [18] TOOL CALL — Bash · 2026-09-29 21:18:45 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; python3 -c "
import json, collections
d=json.load(open('$W/full_method_out.json'))
for ds in d['datasets']:
  ex=ds['examples']
  c=collections.Counter((e['metadata_unit'], e['metadata_split']) for e in ex)
  t=collections.Counter(json.loads(e['input'])['t0'] for e in ex)
  print(ds['dataset'], len(ex), dict(c), sorted(t.items()))
"
```

### [19] TOOL RESULT — Bash · 2026-09-29 21:18:47 UTC

```
{"stdout": "rq1_cohort_2010_14_concepts 4356 {('COH_OTHER', 'COHORT'): 1872, ('COH_DEVHOME', 'COHORT'): 2484} [(2010, 1010), (2011, 983), (2012, 859), (2013, 811), (2014, 693)]\nrq1_dev_concepts 4771 {('Eng', 'DEV'): 1345, ('CS', 'DEV'): 373, ('Med', 'DEV'): 2570, ('BGM', 'DEV'): 483} [(2003, 815), (2004, 748), (2005, 644), (2006, 680), (2007, 592), (2008, 648), (2009, 644)]\nrq1_heldout_concepts 3372 {('SOC', 'HELDOUT'): 1352, ('PHYS', 'HELDOUT'): 742, ('LIFEENV', 'HELDOUT'): 1113, ('MATHDEC', 'HELDOUT'): 165} [(2003, 524), (2004, 479), (2005, 438), (2006, 500), (2007, 484), (2008, 483), (2009, 464)]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-29 21:18:51 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; python3 -c "
import json
l=json.load(open('$W/results/learned_vs_single_heldout.json')); print(json.dumps(l['O2r_m50']['POOLED_HELDOUT'])[:1500])
s=json.load(open('$W/results/frozen_spec.json')); print(json.dumps(s['learned']['O2r_m50'])[:600])
"
```

### [21] TOOL RESULT — Bash · 2026-09-29 21:18:51 UTC

```
{"stdout": "{\"n\": 1833, \"B5\": {\"metric\": 0.7058744877566255, \"r2\": 0.517180326861433}, \"B5_best_single\": {\"metric\": 0.739351768512507, \"r2\": 0.5488979033211705, \"delta_vs_B5\": 0.03347728075588141, \"delta_ci\": [0.02153744592778955, 0.04461679528285289]}, \"linear_all\": {\"metric\": 0.7646699520730624, \"r2\": 0.5827346356128033, \"delta_vs_B5\": 0.058795464316436896, \"delta_ci\": [0.046338877887525415, 0.07285079485618494]}, \"EBM\": {\"metric\": 0.757396356177947, \"r2\": 0.5733129206046019, \"delta_vs_B5\": 0.05152186842132145, \"delta_ci\": [0.037224620705400474, 0.06656014565880622]}}\n{\"best_single\": \"M0_density_end\", \"best_single_std\": [0.13515520155838323, 0.07241775646560125, 0.1267413166766076], \"t0_std\": null, \"B5_coef\": [4.548325941584432, -0.07111230387540654, 0.021954616037054564, -0.3977201436856288, 1.6107644716746912, 0.2872583529340878], \"B5_best_single_coef\": [4.5306568530032285, -0.053045693169890225, 0.07238166013497449, -0.28192807807610576, 1.3840679268024403, -0.005569897925429312, 0.5774426397541141], \"linear_all\": {\"alpha\": 0.017628919161995077, \"l1_ratio\": 0.9, \"coef\": {\"share\": -0.05764262927691142, \"growth_ind\": 0.0, \"accel\": 0.0, \"burst\": 0.0, \"autho", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Write · 2026-09-29 21:19:05 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/build_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json: 100 held-out concepts (25 per held-out group, seeded stratified sample) from the
artifact's full_method_out.json, plus the frozen DEV spec and the full-run reference numbers the notebook compares to.

Usage: python build_mini_demo_data.py <artifact_dir>"""
import json
import random
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"
PER_GROUP = 25
SEED = 20260928

full = json.loads((SRC / "full_method_out.json").read_text())
ds = next(d for d in full["datasets"] if d["dataset"] == "rq1_heldout_concepts")
by_unit = {}
for e in ds["examples"]:
    by_unit.setdefault(e["metadata_unit"], []).append(e)
rng = random.Random(SEED)
examples = []
for u in ["PHYS", "LIFEENV", "SOC", "MATHDEC"]:
    examples += rng.sample(by_unit[u], PER_GROUP)

spec = json.loads((SRC / "results/frozen_spec.json").read_text())
summ = json.loads((SRC / "results/heldout_summary.json").read_text())
lvs = json.loads((SRC / "results/learned_vs_single_heldout.json").read_text())

meta = dict(full["metadata"])
meta["demo_subset"] = (f"{PER_GROUP} concepts per held-out group (PHYS, LIFEENV, SOC, MATHDEC), stratified random "
                       f"sample (seed {SEED}) of the 3,372 held-out concepts in full_method_out.json")
meta["frozen_spec"] = {k: spec[k] for k in ("B5", "top10", "union_top10", "signs", "bootstrap", "pooling")}
meta["full_run_reference"] = {
    "heldout_summary": {o: [{k: r.get(k) for k in ("indicator", "family", "in_top10", "frozen_sign", "pooled",
                                                   "pooled_ci", "holm_p", "confirmed", "sign_agree", "n_units")}
                            for r in rows] for o, rows in summ.items()},
    "learned_vs_single_pooled_heldout": {o: v.get("POOLED_HELDOUT") for o, v in lvs.items()},
}
out = {"metadata": meta, "datasets": [{"dataset": ds["dataset"], "examples": examples}]}
OUT.write_text(json.dumps(out, indent=1))
print(f"wrote {OUT} ({OUT.stat().st_size/1e3:.0f} kB, {len(examples)} examples)")
```

### [23] TOOL RESULT — Write · 2026-09-29 21:19:05 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/build_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json: 100 held-out concepts (25 per held-out group, seeded stratified sample) from the\nartifact's full_method_out.json, plus the frozen DEV spec and the full-run reference numbers the notebook compares to.\n\nUsage: python build_mini_demo_data.py <artifact_dir>\"\"\"\nimport json\nimport random\nimport sys\nfrom pathlib import Path\n\nSRC = Path(sys.argv[1])\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\nPER_GROUP = 25\nSEED = 20260928\n\nfull = json.loads((SRC / \"full_method_out.json\").read_text())\nds = next(d for d in full[\"datasets\"] if d[\"dataset\"] == \"rq1_heldout_concepts\")\nby_unit = {}\nfor e in ds[\"examples\"]:\n    by_unit.setdefault(e[\"metadata_unit\"], []).append(e)\nrng = random.Random(SEED)\nexamples = []\nfor u in [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]:\n    examples += rng.sample(by_unit[u], PER_GROUP)\n\nspec = json.loads((SRC / \"results/frozen_spec.json\").read_text())\nsumm = json.loads((SRC / \"results/heldout_summary.json\").read_text())\nlvs = json.loads((SRC / \"results/learned_vs_single_heldout.json\").read_text())\n\nmeta = dict(full[\"metadata\"])\nmeta[\"demo_subset\"] = (f\"{PER_GROUP} concepts per held-out group (PHYS, LIFEENV, SOC, MATHDEC), stratified random \"\n                       f\"sample (seed {SEED}) of the 3,372 held-out concepts in full_method_out.json\")\nmeta[\"frozen_spec\"] = {k: spec[k] for k in (\"B5\", \"top10\", \"union_top10\", \"signs\", \"bootstrap\", \"pooling\")}\nmeta[\"full_run_reference\"] = {\n    \"heldout_summary\": {o: [{k: r.get(k) for k in (\"indicator\", \"family\", \"in_top10\", \"frozen_sign\", \"pooled\",\n                                                   \"pooled_ci\", \"holm_p\", \"confirmed\", \"sign_agree\", \"n_units\")}\n                            for r in rows] for o, rows in summ.items()},\n    \"learned_vs_single_pooled_heldout\": {o: v.get(\"POOLED_HELDOUT\") for o, v in lvs.items()},\n}\nout = {\"metadata\": meta, \"datasets\": [{\"dataset\": ds[\"dataset\"], \"examples\": examples}]}\nOUT.write_text(json.dumps(out, indent=1))\nprint(f\"wrote {OUT} ({OUT.stat().st_size/1e3:.0f} kB, {len(examples)} examples)\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [24] TOOL CALL — Bash · 2026-09-29 21:19:05 UTC

```
python3 build_mini_demo_data.py /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8 && python3 -c "
import json; d=json.load(open('mini_demo_data.json')); print(d['metadata']['frozen_spec']['bootstrap'], d['metadata']['frozen_spec']['pooling']); print([r['indicator'] for r in d['metadata']['frozen_spec']['top10']['O2r_m50']])"
```

### [25] TOOL RESULT — Bash · 2026-09-29 21:19:05 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/mini_demo_data.json (396 kB, 100 examples)\n{'B_heldout': 1000, 'seed': 20260928, 'unit': 'concept'} DerSimonian-Laird over PHYS, LIFEENV, SOC, MATHDEC (Fisher z of psp with bootstrap SE; dAUC with bootstrap SE)\n['M0_density_end', 'D_vol_end', 'CONTACT_REACH', 'n_comm_W3', 'RS', 'G_btw', 'log_offhome_volume', 'RETENTION_RATIO_early', 'NOV', 'ego_density_W3']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-29 21:19:21 UTC

```
mkdir -p /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc
```

### [27] TOOL RESULT — Bash · 2026-09-29 21:19:21 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [28] TOOL CALL — Write · 2026-09-29 21:20:59 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc/make_nb.py

import json
from pathlib import Path

CELLS = []


def md(s):
    CELLS.append(("markdown", s.strip("\n")))


def code(s):
    CELLS.append(("code", s.strip("\n")))


md(r'''
# Which early network signals of new topics travel? — RQ1 held-out demo

This notebook demonstrates the **held-out scoring stage** of the RQ1 experiment: *do early (t0... [truncated, 27850 chars total]
```

### [29] TOOL RESULT — Write · 2026-09-29 21:20:59 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc/make_nb.py", "content": "import json\nfrom pathlib import Path\n\nCELLS = []\n\n\ndef md(s):\n    CELLS.append((\"markdown\", s.strip(\"\\n\")))\n\n\ndef code(s):\n    CELLS.append((\"code\", s.strip(\"\\n\")))\n\n\nmd(r'''\n# Which early network signals of new topics travel? — RQ1 held-out demo\n\nThis notebook demons... [truncated, 29422 chars total]
```

### [30] TOOL CALL — Bash · 2026-09-29 21:21:07 UTC

```
sed -i 's/^B_HELD = 1000 /B_HELD = 20   /; s/^B_LEARNED = 500 /B_LEARNED = 20  /' _nbsrc/make_nb.py && grep -n "^B_HELD\|^B_LEARNED" _nbsrc/make_nb.py && python3 _nbsrc/make_nb.py && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [31] TOOL RESULT — Bash · 2026-09-29 21:21:33 UTC

```
{"stdout": "112:B_HELD = 20              # concept-bootstrap resamples per (indicator, outcome, unit) psp   (original: 1000)\n113:B_LEARNED = 20           # paired bootstrap resamples, learned model vs B5                 (original: 500)\ncells: 22\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 147251 bytes to code_demo.ipynb\n\nreal\t0m22.354s\nuser\t0m18.132s\nsys\t0m1.392s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-29 21:21:39 UTC

```
The minimum-config test passed in 22 s. I'm checking the outputs now, then I'll scale the bootstraps up.
```

### [33] TOOL CALL — Bash · 2026-09-29 21:21:39 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[-3500:])
    elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
    elif 'data' in o: print(list(o['data'].keys()), ''.join(o['data'].get('text/plain',''))[:600])
  print('-----')
"
```

### [34] TOOL RESULT — Bash · 2026-09-29 21:21:39 UTC

```
{"stdout": "-----\n-----\n-----\nRQ1 held-out indicator portability (DEV freeze -> sealed held-out scoring)\n25 concepts per held-out group (PHYS, LIFEENV, SOC, MATHDEC), stratified random sample (seed 20260928) of the 3,372 held-out concepts in full_method_out.json\nexamples: 100\n\n-----\n-----\n[method] run tests/test_units.py\n[method] run tests/t0_8_ego_port.py\n[method] run passA.py --workers {w}\n[method] run passA.py --merge\n[method] run passB.py --workers {w}\n[method] run passB.py --merge\n[method] run build_features.py --stage all --workers {w}\n[method] run outcomes.py\n[method] run dev_select.py --stage all --workers {w}\n[method] run heldout.py --stage all --workers {w}\n[method] run audit.py\n[method] run make_outputs.py\n\n-----\n-----\n(100, 105)\nunit\nLIFEENV    25\nMATHDEC    25\nPHYS       25\nSOC        25\n\n['text/html', 'text/plain']                         concept  unit    t0    logvol  growth_c  \\\n0  Semiconductor nanostructures  PHYS  2003  4.343805 -0.080043   \n1                      Cardanol  PHYS  2006  3.912023 -0.271934   \n2                  Galaxy group  PHYS  2004  4.110874 -0.046520   \n3                  Matrix model  PHYS  2003  4.634729 -0.570545   \n4                  Mixing ratio  PHYS  2007  4.369448  0.133531   \n5                    Bell state  PHYS  2006  4.369448  0.035091   \n6        Color-glass condensate  PHYS  2005  3.988984 -0.344841   \n7                  Cinchonidine  PHYS  2004  4.007333 -0.154151 \n-----\n['text/plain'] indicator    M0_density_end\noutcome             O2r_m50\nunit                   PHYS\nkind                   cont\nn                         9\nrho                     NaN\nci_lo                   NaN\nci_hi                   NaN\nse                      NaN\nz                      None\nse_z                   None\np                       NaN\nraw_rho                 NaN\nraw_ci_lo               NaN\nraw_ci_hi               NaN\ndtype: object\n-----\nheld-out frozen scoring: 268 jobs in 1.6 s\nO1c        confirmed 0/10 frozen top-10: []\nO2r_m50    confirmed 0/10 frozen top-10: []\nO2r_resid  confirmed 0/10 frozen top-10: []\nO4         confirmed 0/10 frozen top-10: []\n\n-----\nO1c        n=100  B5=+0.399  B5_best_single=+0.380  linear_all=+0.391  EBM=+0.355\nO2r_m50    n= 51  B5=+0.775  B5_best_single=+0.790  linear_all=+0.833  EBM=+0.793\nO2r_resid  n= 51  B5=+0.768  B5_best_single=+0.780  linear_all=+0.822  EBM=+0.785\nO4         n=100  B5=+0.007  B5_best_single=-0.066  linear_all=+nan  EBM=+0.405\n\n-----\n          False    -0.008 [-0.04, +0.03]           False\n    comm_transitions           -1     0.123 [-0.67, +0.78]             0/2           False     0.021 [-0.04, +0.08]           False\n               share            1    -0.035 [-0.57, +0.52]             1/4           False     0.013 [-0.02, +0.05]           False\nfields_gained_per_yr            1    -0.027 [-0.53, +0.49]             1/4           False     0.002 [-0.03, +0.04]           False\n       new_edge_rate            1    -0.110 [-0.69, +0.56]             2/4           False    -0.002 [-0.04, +0.04]           False\n\n=== O4: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 6/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n                G_deg           -1     0.149 [-0.52, +0.71]             1/4           False    -0.021 [-0.07, +0.03]           False\n   log_offhome_volume           -1    -0.097 [-0.72, +0.61]             1/4           False    -0.002 [-0.07, +0.07]           False\n             REL_home           -1    -0.294 [-0.76, +0.36]             4/4           False    -0.114 [-0.18, -0.05]            True\n                burst           -1     0.038 [-0.48, +0.54]             2/4           False     0.014 [-0.04, +0.07]           False\n                  G_A           -1     0.046 [-0.48, +0.55]             2/4           False    -0.010 [-0.06, +0.04]           False\n        author_growth            1     0.139 [-0.40, +0.60]             2/4           False     0.065 [+0.02, +0.11]            True\n             G_phimin            1    -0.026 [-0.64, +0.61]             2/4           False     0.064 [-0.08, +0.21]           False\n   FRONTIER_POTENTIAL           -1     0.292 [-0.49, +0.81]             1/4           False    -0.017 [-0.06, +0.03]           False\nRETENTION_RATIO_early           -1    -0.010 [-0.73, +0.72]             2/4           False    -0.026 [-0.06, +0.01]           False\n        new_edge_rate           -1     0.282 [-0.56, +0.84]             0/4           False     0.003 [-0.03, +0.04]           False\n\n=== learned vs single vs B5, pooled held-out Spearman (demo n=100 | full run) ===\n  outcome          model   demo  demo_delta_vs_B5  full  full_delta_vs_B5\n      O1c             B5  0.399               NaN 0.312               NaN\n      O1c B5_best_single  0.380            -0.018 0.305            -0.007\n      O1c     linear_all  0.391            -0.008 0.303            -0.009\n      O1c            EBM  0.355            -0.044 0.313             0.002\n  O2r_m50             B5  0.775               NaN 0.706               NaN\n  O2r_m50 B5_best_single  0.790             0.016 0.739             0.033\n  O2r_m50     linear_all  0.833             0.059 0.765             0.059\n  O2r_m50            EBM  0.793             0.018 0.757             0.052\nO2r_resid             B5  0.768               NaN 0.704               NaN\nO2r_resid B5_best_single  0.780             0.012 0.738             0.034\nO2r_resid     linear_all  0.822             0.053 0.763             0.059\nO2r_resid            EBM  0.785             0.016 0.756             0.052\n       O4             B5  0.007               NaN 0.015               NaN\n       O4 B5_best_single -0.066            -0.073 0.028             0.013\n       O4     linear_all    NaN               NaN   NaN               NaN\n       O4            EBM  0.405             0.398 0.188             0.174\n\n-----\n['image/png', 'text/plain'] <Figure size 1700x520 with 3 Axes>\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] THINKING · 2026-09-29 21:21:49 UTC

```
The O2r_m50 breadth outcome is missing for about half the concepts, pushing groups below the n≥20 minimum and causing NaN scores. I'll redraw the sample using only concepts that have this outcome available.
```

### [36] TOOL CALL — Bash · 2026-09-29 21:21:49 UTC

```
python3 - <<'EOF'
import json, collections
d=json.load(open('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/full_method_out.json'))
ds=[x for x in d['datasets'] if x['dataset']=='rq1_heldout_concepts'][0]
c=collections.Counter(); c2=collections.Counter()
for e in ds['examples']:
    o=json.loads(e['output']); c[e['metadata_unit']]+=1
    if o['O2r_m50'] is not None: c2[e['metadata_unit']]+=1
print(c, c2)
EOF
```

### [37] TOOL RESULT — Bash · 2026-09-29 21:21:49 UTC

```
{"stdout": "Counter({'SOC': 1352, 'LIFEENV': 1113, 'PHYS': 742, 'MATHDEC': 165}) Counter({'SOC': 689, 'LIFEENV': 630, 'PHYS': 413, 'MATHDEC': 101})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-29 21:21:55 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('build_mini_demo_data.py'); s=p.read_text()
s=s.replace('''    by_unit.setdefault(e["metadata_unit"], []).append(e)''','''    # breadth (O2r_m50) is defined for ~54% of concepts; sample among those so every group keeps n >= 20
    if json.loads(e["output"])["O2r_m50"] is not None:
        by_unit.setdefault(e["metadata_unit"], []).append(e)''')
s=s.replace('''stratified random "
                       f"sample (seed {SEED}) of the 3,372 held-out concepts in full_method_out.json")''','''stratified random "
                       f"sample (seed {SEED}) of the 1,833 held-out concepts with a defined breadth outcome (O2r_m50) "
                       f"among the 3,372 held-out concepts in full_method_out.json")''')
s=s.replace('"""Build mini_demo_data.json: 100 held-out concepts (25 per held-out group, seeded stratified sample)','"""Build mini_demo_data.json: 100 held-out concepts (25 per held-out group, seeded stratified sample among\nconcepts with a defined O2r_m50)')
p.write_text(s)
EOF
python3 build_mini_demo_data.py /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8 && head -5 build_mini_demo_data.py
```

### [39] TOOL RESULT — Bash · 2026-09-29 21:21:57 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/mini_demo_data.json (397 kB, 100 examples)\n#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json: 100 held-out concepts (25 per held-out group, seeded stratified sample among\nconcepts with a defined O2r_m50) from the\nartifact's full_method_out.json, plus the frozen DEV spec and the full-run reference numbers the notebook compares to.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-29 21:22:05 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('_nbsrc/make_nb.py'); s=p.read_text()
old='''per-concept output (`method_out.json`): **100 held-out concepts (25 per held-out group)** with their indicators,
outcomes and the frozen models' predictions.'''
assert old in s
s=s.replace(old,'''per-concept output (`method_out.json`): **100 held-out concepts (25 per held-out group, drawn among the 1,833
held-out concepts whose breadth outcome O2r_m50 is defined)** with their indicators, outcomes and the frozen models'
predictions.''')
p.write_text(s)
EOF
python3 _nbsrc/make_nb.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3 && python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][14:]:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[:6000])
    elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
    elif 'data' in o: print(''.join(o['data'].get('text/plain',''))[:700])
  print('-----')
"
```

### [41] TOOL RESULT — Bash · 2026-09-29 21:22:31 UTC

```
{"stdout": "cells: 22\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 155143 bytes to code_demo.ipynb\n\nreal\t0m24.074s\nuser\t0m19.665s\nsys\t0m1.363s\nindicator    M0_density_end\noutcome             O2r_m50\nunit                   PHYS\nkind                   cont\nn                        25\nrho                0.316801\nci_lo             -0.214861\nci_hi              0.955639\nse                 0.358858\nz                  0.328088\nse_z               1.598088\np                  0.837338\nraw_rho            0.635385\nraw_ci_lo          0.376504\nraw_ci_hi          0.871242\ndtype: object\n-----\nheld-out frozen scoring: 268 jobs in 2.8 s\nO1c        confirmed 0/10 frozen top-10: []\nO2r_m50    confirmed 0/10 frozen top-10: []\nO2r_resid  confirmed 0/10 frozen top-10: []\nO4         confirmed 0/10 frozen top-10: []\n\n-----\nO1c        n=100  B5=+0.197  B5_best_single=+0.202  linear_all=+0.164  EBM=+0.200\nO2r_m50    n=100  B5=+0.768  B5_best_single=+0.823  linear_all=+0.837  EBM=+0.813\nO2r_resid  n=100  B5=+0.779  B5_best_single=+0.829  linear_all=+0.837  EBM=+0.818\nO4         n=100  B5=+0.032  B5_best_single=+0.129  linear_all=+nan  EBM=+0.381\n\n-----\n\n=== O2r_m50: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 10/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n       M0_density_end            1     0.369 [-0.90, +0.98]             4/4           False     0.375 [+0.28, +0.46]            True\n            D_vol_end            1     0.334 [-0.23, +0.73]             4/4           False     0.307 [+0.26, +0.36]            True\n        CONTACT_REACH            1     0.409 [-0.86, +0.97]             4/4           False     0.211 [+0.16, +0.26]            True\n            n_comm_W3            1     0.330 [-0.96, +0.99]             4/4           False     0.167 [+0.06, +0.27]            True\n                   RS           -1    -0.172 [-0.69, +0.46]             3/4           False    -0.072 [-0.15, +0.01]           False\n                G_btw            1     0.194 [-0.38, +0.66]             3/4           False     0.056 [-0.01, +0.12]           False\n   log_offhome_volume           -1    -0.186 [-0.72, +0.48]             1/4           False    -0.089 [-0.17, -0.01]           False\nRETENTION_RATIO_early           -1    -0.374 [-0.74, +0.16]             4/4           False    -0.114 [-0.16, -0.07]            True\n                  NOV            1     0.278 [-0.77, +0.92]             4/4           False     0.151 [+0.04, +0.26]            True\n       ego_density_W3           -1    -0.158 [-0.78, +0.63]             3/4           False    -0.102 [-0.15, -0.05]            True\n\n=== O2r_resid: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 9/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n       M0_density_end            1     0.412 [-0.90, +0.98]             4/4           False     0.377 [+0.28, +0.47]            True\n            D_vol_end            1     0.346 [-0.21, +0.73]             4/4           False     0.307 [+0.26, +0.36]            True\n        CONTACT_REACH            1     0.401 [-0.87, +0.98]             4/4           False     0.210 [+0.16, +0.26]            True\n            n_comm_W3            1     0.306 [-0.97, +0.99]             4/4           False     0.164 [+0.06, +0.27]            True\n                   RS           -1    -0.224 [-0.70, +0.38]             3/4           False    -0.073 [-0.15, +0.01]           False\n   log_offhome_volume           -1     0.049 [-0.42, +0.50]             2/4           False    -0.100 [-0.17, -0.03]            True\n                G_btw            1     0.100 [-0.61, +0.72]             3/4           False     0.055 [-0.01, +0.12]           False\nRETENTION_RATIO_early           -1    -0.402 [-0.73, +0.08]             4/4           False    -0.120 [-0.17, -0.07]            True\n                  NOV            1     0.262 [-0.82, +0.93]             4/4           False     0.152 [+0.04, +0.26]            True\n       ego_density_W3           -1    -0.166 [-0.78, +0.61]             2/4           False    -0.097 [-0.15, -0.05]            True\n\n=== O1c: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 6/10) ===\n           indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n     n_authors_early            1     0.356 [-0.93, +0.98]             3/4           False     0.161 [+0.09, +0.23]            True\n               burst            1     0.015 [-0.58, +0.60]             2/4           False     0.019 [-0.05, +0.09]           False\n            S_comp_n           -1    -0.047 [-0.96, +0.95]             2/4           False    -0.087 [-0.20, +0.03]           False\n       CONTACT_REACH            1    -0.214 [-0.98, +0.96]             1/4           False     0.048 [+0.01, +0.08]           False\n       author_growth            1     0.073 [-0.51, +0.61]             3/4           False     0.035 [-0.02, +0.09]           False\n          growth_ind            1     0.003 [-0.47, +0.48]             1/4           False    -0.008 [-0.04, +0.03]           False\n    comm_transitions           -1    -0.423 [-1.00, +1.00]             1/1           False     0.021 [-0.04, +0.08]           False\n               share            1    -0.344 [-0.78, +0.31]             2/4           False     0.013 [-0.02, +0.05]           False\nfields_gained_per_yr            1     0.051 [-0.58, +0.64]             2/4           False     0.002 [-0.03, +0.04]           False\n       new_edge_rate            1    -0.001 [-0.43, +0.43]             1/4           False    -0.002 [-0.04, +0.04]           False\n\n=== O4: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 6/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n                G_deg           -1    -0.203 [-0.97, +0.94]             3/4           False    -0.021 [-0.07, +0.03]           False\n   log_offhome_volume           -1     0.184 [-0.49, +0.72]             1/4           False    -0.002 [-0.07, +0.07]           False\n             REL_home           -1    -0.221 [-0.98, +0.95]             4/4           False    -0.114 [-0.18, -0.05]            True\n                burst           -1    -0.111 [-0.98, +0.97]             2/4           False     0.014 [-0.04, +0.07]           False\n                  G_A           -1     0.145 [-0.46, +0.66]             3/4           False    -0.010 [-0.06, +0.04]           False\n        author_growth            1     0.074 [-0.45, +0.56]             3/4           False     0.065 [+0.02, +0.11]            True\n             G_phimin            1     0.329 [-0.55, +0.86]             3/4           False     0.064 [-0.08, +0.21]           False\n   FRONTIER_POTENTIAL           -1     0.046 [-0.54, +0.60]             2/4           False    -0.01\n-----\n<Figure size 1700x520 with 3 Axes>\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] ASSISTANT · 2026-09-29 21:22:41 UTC

```
Breadth signs now match the full run for 10/10 frozen indicators. Next I'm scaling the bootstraps: 200/100 first, then the original 1000/500.
```

### [43] TOOL CALL — Bash · 2026-09-29 21:22:41 UTC

```
sed -i 's/^B_HELD = 20   /B_HELD = 200  /; s/^B_LEARNED = 20  /B_LEARNED = 100 /' _nbsrc/make_nb.py && grep -n "^B_HELD\|^B_LEARNED" _nbsrc/make_nb.py && python3 _nbsrc/make_nb.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][16:20]:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[:2200])
    elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
"
```

### [44] TOOL RESULT — Bash · 2026-09-29 21:23:25 UTC

```
{"stdout": "113:B_HELD = 200             # concept-bootstrap resamples per (indicator, outcome, unit) psp   (original: 1000)\n114:B_LEARNED = 100          # paired bootstrap resamples, learned model vs B5                 (original: 500)\ncells: 22\n[NbConvertApp] Writing 155240 bytes to code_demo.ipynb\n\nreal\t0m42.593s\nuser\t0m38.183s\nsys\t0m1.397s\nheld-out frozen scoring: 268 jobs in 20.4 s\nO1c        confirmed 0/10 frozen top-10: []\nO2r_m50    confirmed 0/10 frozen top-10: []\nO2r_resid  confirmed 0/10 frozen top-10: []\nO4         confirmed 0/10 frozen top-10: []\n\nO1c        n=100  B5=+0.197  B5_best_single=+0.202  linear_all=+0.164  EBM=+0.200\nO2r_m50    n=100  B5=+0.768  B5_best_single=+0.823  linear_all=+0.837  EBM=+0.813\nO2r_resid  n=100  B5=+0.779  B5_best_single=+0.829  linear_all=+0.837  EBM=+0.818\nO4         n=100  B5=+0.032  B5_best_single=+0.129  linear_all=+nan  EBM=+0.381", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] ASSISTANT · 2026-09-29 21:23:33 UTC

```
At 200/100 the notebook runs in 43 s. The original 1000/500 should take about 2.5 min, well within budget, so I'm switching to those.
```

### [46] TOOL CALL — Bash · 2026-09-29 21:23:33 UTC

```
sed -i 's/^B_HELD = 200  /B_HELD = 1000 /; s/^B_LEARNED = 100 /B_LEARNED = 500 /' _nbsrc/make_nb.py && grep -n "^B_HELD\|^B_LEARNED" _nbsrc/make_nb.py && python3 _nbsrc/make_nb.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells'][16:]:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[:3000])
    elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
  if any(o.get('output_type')=='display_data' for o in c['outputs']):
    import base64; png=[o for o in c['outputs'] if 'data' in o and 'image/png' in o['data']][0]['data']['image/png']; open('_nbsrc/fig.png','wb').write(base64.b64decode(png))
"
```

### [47] TOOL RESULT — Bash · 2026-09-29 21:25:27 UTC

```
{"stdout": "113:B_HELD = 1000            # concept-bootstrap resamples per (indicator, outcome, unit) psp   (original: 1000)\n114:B_LEARNED = 500          # paired bootstrap resamples, learned model vs B5                 (original: 500)\ncells: 22\n[NbConvertApp] Writing 155301 bytes to code_demo.ipynb\n\nreal\t1m51.399s\nuser\t1m47.082s\nsys\t0m1.877s\nheld-out frozen scoring: 268 jobs in 84.3 s\nO1c        confirmed 0/10 frozen top-10: []\nO2r_m50    confirmed 0/10 frozen top-10: []\nO2r_resid  confirmed 0/10 frozen top-10: []\nO4         confirmed 0/10 frozen top-10: []\n\nO1c        n=100  B5=+0.197  B5_best_single=+0.202  linear_all=+0.164  EBM=+0.200\nO2r_m50    n=100  B5=+0.768  B5_best_single=+0.823  linear_all=+0.837  EBM=+0.813\nO2r_resid  n=100  B5=+0.779  B5_best_single=+0.829  linear_all=+0.837  EBM=+0.818\nO4         n=100  B5=+0.032  B5_best_single=+0.129  linear_all=+nan  EBM=+0.381\n\n\n=== O2r_m50: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 10/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n       M0_density_end            1     0.352 [-0.74, +0.93]             4/4           False     0.375 [+0.28, +0.46]            True\n            D_vol_end            1     0.396 [-0.63, +0.92]             4/4           False     0.307 [+0.26, +0.36]            True\n        CONTACT_REACH            1     0.411 [-0.67, +0.93]             4/4           False     0.211 [+0.16, +0.26]            True\n            n_comm_W3            1     0.361 [-0.71, +0.93]             4/4           False     0.167 [+0.06, +0.27]            True\n                   RS           -1    -0.227 [-0.91, +0.79]             3/4           False    -0.072 [-0.15, +0.01]           False\n                G_btw            1     0.139 [-0.74, +0.84]             3/4           False     0.056 [-0.01, +0.12]           False\n   log_offhome_volume           -1    -0.040 [-0.87, +0.85]             1/4           False    -0.089 [-0.17, -0.01]           False\nRETENTION_RATIO_early           -1    -0.286 [-0.91, +0.73]             4/4           False    -0.114 [-0.16, -0.07]            True\n                  NOV            1     0.290 [-0.93, +0.98]             4/4           False     0.151 [+0.04, +0.26]            True\n       ego_density_W3           -1    -0.163 [-0.93, +0.86]             3/4           False    -0.102 [-0.15, -0.05]            True\n\n=== O2r_resid: frozen top-10, pooled psp | B5 over PHYS/LIFEENV/SOC/MATHDEC (demo sign = full-run sign for 10/10) ===\n            indicator  frozen_sign  demo_psp        demo_ci demo_sign_agree  demo_confirmed  full_psp        full_ci  full_confirmed\n       M0_density_end            1     0.388 [-0.73, +0.94]             4/4           False     0.377 [+0.28, +0.47]            True\n            D_vol_end            1     0.396 [-0.62, +0.92]             4/4           False     0.307 [+0.26, +0.36]            True\n        CONTACT_REACH            1     0.407 [-0.68, +0.93]             4/4           False     0.210 [+0.16, +0.26]            True\n            n_comm_W3            1     0.351 [-0.71, +0.93]             4/4           False     0.164 [+0.06, +0.27]            True\n                   RS           -1    -0.238 [-0.91, +0.79]             3/4           False    -0.073 [-0.15, +0.01]           False\n   log_offhome_volume           -1    -0.033 [-0.78, +0.75]             2/4           False    -0.100 [-0.17, -0.03]            True\n                G_btw            1     0.144 [-0.85, +0.91]             3/4           False     0.055 [-0.01, +0.12]           False\nRETENTION_RATIO_early           -1    -0.294 [-0.91, +0.72]             4/4           False    -0.120 [-0.17, -0.07]            True\n                  NOV            1     0.275 [-0.93, +0.98]             4/4           False     0.152 [+", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] TOOL CALL — Read · 2026-09-29 21:25:31 UTC

```
/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc/fig.png
```

### [49] TOOL RESULT — Read · 2026-09-29 21:25:31 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [50] ASSISTANT · 2026-09-29 21:25:45 UTC

```
Plots look right. Two small fixes before the final run: I'm moving the panel-c legend off the bars and correcting the n in the labels and the CI-width note.
```

### [51] TOOL CALL — Bash · 2026-09-29 21:25:45 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('_nbsrc/make_nb.py'); s=p.read_text()
reps=[('ax.legend(fontsize=8, ncol=2)','ax.legend(fontsize=8, ncol=2, loc="upper left")'),
('label="full run (n=3,372)"','label="full run (all held-out)"'),
('''The tables put the demo's pooled partial Spearman (100 concepts) next to the full-run value (3,372 held-out
concepts) for each frozen top-10 indicator, and the learned-model comparison next to its full-run counterpart.
The demo CIs are roughly 6× wider, so only the strongest breadth signals (e.g. `M0_density_end`, `D_vol_end`) are
expected to stand out; agreement in **sign** with the full run is the main thing to look for.''',
'''The tables put the demo's pooled partial Spearman (100 concepts) next to the full-run value (all held-out concepts
with a defined outcome: 1,833 for breadth, 3,372 for O1c/O4) for each frozen top-10 indicator, and the
learned-model comparison next to its full-run counterpart.

With 25 concepts per group and 12 nuisance columns (intercept, 5 B5 ranks, 6 onset-year dummies) absorbed before
correlating, many bootstrap resamples give residual correlations near ±1, which inflates the Fisher-z SE; the demo's
pooled CIs therefore span most of [-1, 1] and nothing is "confirmed" at this size. What *does* carry over is the
**direction and rough magnitude**: compare the `demo_psp` and `full_psp` columns, the per-group sign agreement,
and the learned-model gains over B5 for breadth.''')]
for a,b in reps:
    assert a in s, a; s=s.replace(a,b)
p.write_text(s)
EOF
python3 _nbsrc/make_nb.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
errs=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if o['output_type']=='error']
print('errors:',len(errs))
png=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if 'data' in o and 'image/png' in o['data']][0]['data']['image/png']; open('_nbsrc/fig.png','wb').write(base64.b64decode(png))
"; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-3/experiment-8/demo/mini_demo_data.json"' code_demo.ipynb
```

### [52] TOOL RESULT — Bash · 2026-09-29 21:27:39 UTC

```
{"stdout": "cells: 22\n[NbConvertApp] Writing 155296 bytes to code_demo.ipynb\n\nreal\t1m51.377s\nuser\t1m46.814s\nsys\t0m1.747s\nerrors: 0\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [53] TOOL CALL — Bash · 2026-09-29 21:27:45 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb')); src='\n'.join(''.join(c['source']) for c in nb['cells'])
print('url ok:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-3/experiment-8/demo/mini_demo_data.json\"' in src, 'urlopen' in src)
"; ls -la
```

### [54] TOOL RESULT — Bash · 2026-09-29 21:27:45 UTC

```
{"stdout": "url ok: True True\ntotal 5907\ndrwxrwxrwx 4 aii-agent aii-agent 2000108 Sep 29 21:21 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000409 Sep 29 21:16 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:16 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:17 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  480570 Sep 29 21:27 .repl_agent.ptylog\ndrwxrwxrwx 2 aii-agent aii-agent 1009926 Sep 29 21:25 _nbsrc\n-rw-rw-rw- 1 aii-agent aii-agent    2382 Sep 29 21:21 build_mini_demo_data.py\n-rw-rw-rw- 1 aii-agent aii-agent  155329 Sep 29 21:27 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent  396915 Sep 29 21:21 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Read · 2026-09-29 21:27:45 UTC

```
/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc/fig.png
```

### [56] TOOL RESULT — Read · 2026-09-29 21:27:45 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [57] TOOL CALL — Bash · 2026-09-29 21:27:57 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('_nbsrc/make_nb.py'); s=p.read_text()
a='ax.axhline(0, color="grey", lw=0.8)\nax.set_ylabel'
assert a in s
s=s.replace(a,'ax.axhline(0, color="grey", lw=0.8)\nax.set_ylim(top=1.12)   # room for the legend above the bars\nax.set_ylabel')
p.write_text(s)
EOF
python3 _nbsrc/make_nb.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_dFQ6jbgNsR6Q-7fd31b05f5a2/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1 && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
errs=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if o['output_type']=='error']
print('errors:',len(errs))
png=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if 'data' in o and 'image/png' in o['data']][0]['data']['image/png']; open('_nbsrc/fig.png','wb').write(base64.b64decode(png))
"
```

### [58] TOOL CALL — Read · 2026-09-29 21:27:57 UTC

```
/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_dFQ6jbgNsR6Q/_nbsrc/fig.png
```

### [59] TOOL RESULT — Bash · 2026-09-29 21:29:47 UTC

```
{"stdout": "cells: 22\n[NbConvertApp] Writing 152818 bytes to code_demo.ipynb\n\nreal\t1m51.173s\nuser\t1m46.270s\nsys\t0m2.113s\nerrors: 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL RESULT — Read · 2026-09-29 21:29:48 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [61] ASSISTANT · 2026-09-29 21:30:03 UTC

```
Final run is clean (0 errors, 1 min 51 s). Now I'm removing the scratch generator and writing the README, manifest and output JSON.
```

### [62] TOOL CALL — Bash · 2026-09-29 21:30:03 UTC

````
rm -rf _nbsrc && cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy: code_demo.ipynb (~150 kB), mini_demo_data.json (~400 kB) and
# build_mini_demo_data.py are all text files well under the 10 MB auto-keep floor. The test venv lives
# outside the workspace (/tmp) and is removed by the pipeline.
entries: []
EOF
cat > README.md <<'EOF'
# RQ1 held-out demo: which early network signals of new topics travel

A runnable Colab/Jupyter demo of the **held-out scoring stage** of the RQ1 experiment (artifact `art_dFQ6jbgNsR6Q`).
The experiment tests whether early (t0..t0+2) network indicators of newly emerging OpenAlex concepts predict how
those concepts later spread, beyond a 5-variable popularity baseline (B5). It also tests whether the indicators
frozen on the development domains (CS/Eng/BGM/Med) carry over to sealed held-out domains (PHYS, LIFEENV, SOC,
MATHDEC).

The full pipeline needs OpenAlex S3 snapshot passes (many CPU-hours), so it can't run in a notebook. The demo
starts from the artifact's per-concept output instead: 100 held-out concepts, 25 per group, drawn among concepts
with a defined breadth outcome. On that subset it re-runs the original code:

- `heldout.py::job`: partial Spearman given B5 + onset-year dummies, with a concept bootstrap.
- `heldout.py::stage_score`: DerSimonian–Laird pooling, sign agreement and Holm correction.
- `heldout.py::stage_learned`: B5 vs B5 + best single indicator vs ElasticNet vs EBM.

`method.py`'s orchestrator is shown as a dry run. The demo results are compared with the full-run results.

## Layout

| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook (executed; about 2 min end to end with the original bootstrap counts 1000/500) |
| `mini_demo_data.json` | 100 held-out concepts (indicators, outcomes, frozen-model predictions), the frozen DEV spec, and full-run reference numbers |
| `build_mini_demo_data.py` | Rebuilds `mini_demo_data.json` from the artifact's `full_method_out.json` (seeded stratified sample) |
| `.aii/manifest.yaml` | Storage manifest (no heavy files) |

## Running

Open `code_demo.ipynb` in Colab, or locally:

```bash
pip install jupyter ipykernel
jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```

The install cell installs numpy/pandas/scipy/matplotlib at Colab's versions only when it isn't running on Colab.
Data is loaded from the GitHub raw URL, falling back to the local `mini_demo_data.json`. The config cell holds
`B_HELD` (1000), `B_LEARNED` (500), `MIN_N_LEARNED` (20; the original is 30, lowered because the demo groups have
25 concepts) and `SEED`.

## What the demo shows

- **Breadth (O2r_m50 / O2r_resid):** the demo's pooled partial Spearman has the same sign as the full run for
  10/10 frozen indicators. The top four (`M0_density_end`, `D_vol_end`, `CONTACT_REACH`, `n_comm_W3`) agree in
  sign in 4/4 groups. Learned models beat B5 by about +0.05 to +0.07 in Spearman (full run: +0.059).
- **At n = 25 per group nothing is Holm-confirmed.** The bootstrap Fisher-z SEs are very wide, so the demo
  illustrates direction and magnitude, not significance.

## Restoring removed files

Nothing is marked `delete` in `.aii/manifest.yaml`, so nothing needs restoring. To rebuild `mini_demo_data.json`
from the source artifact, run `python build_mini_demo_data.py <path-to-artifact-dir>`. The directory must contain
`full_method_out.json` and `results/`.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
ls -la; cat .terminal_claude_agent_struct_out.json
````

### [63] TOOL RESULT — Bash · 2026-09-29 21:30:05 UTC

```
{"stdout": "total 5053\ndrwxrwxrwx 3 aii-agent aii-agent 2000108 Sep 29 21:30 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000409 Sep 29 21:16 ..\ndrwxrwxrwx 2 aii-agent aii-agent   27700 Sep 29 21:30 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:17 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  590268 Sep 29 21:30 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent      97 Sep 29 21:30 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 aii-agent aii-agent    3083 Sep 29 21:30 README.md\n-rw-rw-rw- 1 aii-agent aii-agent    2382 Sep 29 21:21 build_mini_demo_data.py\n-rw-rw-rw- 1 aii-agent aii-agent  152851 Sep 29 21:29 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent  396915 Sep 29 21:21 mini_demo_data.json\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [64] ASSISTANT · 2026-09-29 21:30:16 UTC

```
I built the demo notebook and its data file, and the notebook runs cleanly end to end in the fresh test venv in about 1 min 51 s (limit 10 min).

**How it works:** the original `method.py` only launches other scripts in sequence, and the early ones need OpenAlex S3 passes that take many CPU-hours. So the notebook starts from the per-concept results the experiment already produced. On a sample of held-out concepts it re-runs the original held-out scoring code from `heldout.py` and `lib/rq1stats.py`, split into cells with explanations between them:
- **Orchestrator:** `method.py`'s step list and `main()`, with an added `--dry-run` flag that prints each step's command instead of running it.
- **Indicator scoring:** each frozen indicator's partial Spearman with the outcome, given the B5 baseline and onset year, with 1,000 bootstrap resamples per domain group.
- **Pooling and confirmation:** the per-group results combined across the four held-out groups, plus sign agreement and the Holm correction.
- **Model comparison:** B5 alone vs B5 plus the best single indicator vs ElasticNet vs EBM, with a 500-resample paired bootstrap against B5.
- **Results:** tables and a three-panel figure putting the demo numbers next to the full-run numbers.

Changes to the original code:
- **Scoring:** jobs run one after another instead of in a process pool.
- **Models:** the saved prediction fields are used instead of loading the model files. The numbers are the same, because the models were fixed before the held-out data was opened.
- **Minimum group size:** lowered from 30 to 20 for the model comparison, because the demo groups have 25 concepts.
- **Binary outcomes left out:** O1b, O3, O5 and O5_WW need the development-set rows, which aren't in the demo data.
- **Bootstrap counts:** these are at the original values (1,000 and 500). I tested 20, then 200, then 1,000.

**Data:** `mini_demo_data.json` holds 100 held-out concepts, 25 from each of the four groups. They're drawn only from concepts that have a breadth outcome (O2r_m50). My first sample didn't do this, and about half the concepts lacked it, which left every group below the code's 20-concept minimum. The file also carries the frozen selections and the full-run reference numbers. `build_mini_demo_data.py` rebuilds it from the original experiment's output folder.

**What the demo shows:**
- **Direction:** for breadth, the demo's pooled estimate has the same sign as the full run for all 10 frozen indicators. The top four (`M0_density_end`, `D_vol_end`, `CONTACT_REACH`, `n_comm_W3`) point the same way in all four groups.
- **Models:** the learned models improve on B5 by about +0.05 to +0.07 Spearman, against +0.059 in the full run.
- **Significance:** nothing is confirmed after the Holm correction at this size. With 25 concepts per group, the pooled confidence intervals cover most of −1 to 1, so the demo shows direction and rough size only. The notebook says this.

All the checks passed: the notebook contains the exact `GITHUB_DATA_URL` and loads through it, falling back to the local file.

I also wrote `README.md` and `.aii/manifest.yaml`. The manifest has no entries because every file is small text. The required `.terminal_claude_agent_struct_out.json` is written too.

Files are in the workspace:
- code_demo.ipynb
- mini_demo_data.json
- build_mini_demo_data.py
- README.md
```
