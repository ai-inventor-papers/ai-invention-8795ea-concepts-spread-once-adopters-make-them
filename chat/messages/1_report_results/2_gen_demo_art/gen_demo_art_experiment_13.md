# gen_demo_art_experiment_13 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_13` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-30 02:15:21 UTC

```
model: Claude Opus 5.5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-30 02:15:35 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/`:
GOOD: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/file.py`, `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-16/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-16/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-16/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-30 02:15:37 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-30 02:15:37 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-30 02:15:37 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-30 02:15:39 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-30 02:15:41 UTC

```
List artifact workspace and own workspace:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; ls -la $W; ls -la $W/lib $W/data $W/results 2>/dev/null | head -80; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/ /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/.aii
```

### [8] TOOL RESULT — Bash · 2026-09-30 02:15:45 UTC

```
{"stdout": "total 38538\ndrwxrwxrwx 10 aii-agent aii-agent  2027929 Sep 29 09:02 .\ndrwxrwxrwx  7 aii-agent aii-agent  3000249 Sep 29 05:17 ..\ndrwxrwxrwx  2 aii-agent aii-agent   100800 Sep 29 06:28 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 29 05:18 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent     9154 Sep 29 06:28 .aii_worker_result.json\n-rw-rw-rw-  1 aii-agent aii-agent  1918369 Sep 29 06:28 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     3354 Sep 29 06:26 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    13917 Sep 29 06:27 README.md\ndrwxrwxrwx  3 aii-agent aii-agent  2025210 Sep 29 09:02 data\ndrwxrwxrwx  2 aii-agent aii-agent  1056430 Sep 29 06:19 figures\n-rw-rw-rw-  1 aii-agent aii-agent 12422709 Sep 29 06:26 full_method_out.json\ndrwxrwxrwx  3 aii-agent aii-agent  1014531 Sep 29 21:36 lib\ndrwxrwxrwx  2 aii-agent aii-agent  1010536 Sep 29 06:24 logs\n-rw-rw-rw-  1 aii-agent aii-agent    12025 Sep 29 06:21 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 11688840 Sep 29 06:21 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    15065 Sep 29 06:26 mini_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent        1 Sep 29 06:25 models\n-rw-rw-rw-  1 aii-agent aii-agent    12774 Sep 29 06:26 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent      839 Sep 29 06:25 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent     6760 Sep 29 05:56 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent     7108 Sep 29 06:26 reproducibility.md\n-rwxrwxrwx  1 aii-agent aii-agent      772 Sep 29 06:23 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent  2000137 Sep 29 06:25 results\n-rw-rw-rw-  1 aii-agent aii-agent     5133 Sep 29 05:24 s0_gate.py\n-rw-rw-rw-  1 aii-agent aii-agent    10781 Sep 29 05:31 s1_freeze.py\n-rw-rw-rw-  1 aii-agent aii-agent     9379 Sep 29 05:31 s2_variants.py\n-rw-rw-rw-  1 aii-agent aii-agent    15659 Sep 29 05:36 s3_nulls.py\n-rw-rw-rw-  1 aii-agent aii-agent    13130 Sep 29 05:39 s4_composites.py\n-rw-rw-rw-  1 aii-agent aii-agent     6646 Sep 29 05:40 s4b_outcome_rel.py\n-rw-rw-rw-  1 aii-agent aii-agent     7685 Sep 29 05:44 s5_size.py\n-rw-rw-rw-  1 aii-agent aii-agent     8735 Sep 29 05:43 s6_assoc.py\n-rw-rw-rw-  1 aii-agent aii-agent    15374 Sep 29 05:53 s7_verdict.py\n-rw-rw-rw-  1 aii-agent aii-agent    10981 Sep 29 06:19 s8_power.py\ndrwxrwxrwx  2 aii-agent aii-agent  1002156 Sep 29 06:25 tests\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/data:\ntotal 19996\ndrwxrwxrwx  3 aii-agent aii-agent 2025210 Sep 29 09:02 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027929 Sep 29 09:02 ..\n-rw-rw-rw-  1 aii-agent aii-agent 4634477 Sep 29 05:47 clean_variants.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 3595049 Sep 29 06:15 psp_boot.npz\ndrwxrwxrwx  2 aii-agent aii-agent 2023837 Sep 29 05:34 s2_parts_full\n-rw-rw-rw-  1 aii-agent aii-agent 2834797 Sep 29 05:34 s2_scalars_full.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  488773 Sep 29 05:46 v3_nulls_full.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 2844086 Sep 29 05:49 v4_half_means.npz\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib:\ntotal 4053\ndrwxrwxrwx  3 aii-agent aii-agent 1014531 Sep 29 21:36 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027929 Sep 29 09:02 ..\ndrwxrwxrwx  2 aii-agent aii-agent 1004832 Sep 29 21:36 __pycache__\n-rw-rw-rw-  1 aii-agent aii-agent    5891 Sep 29 05:23 common.py\n-rw-rw-rw-  1 aii-agent aii-agent    4421 Sep 29 05:23 common3.py\n-rw-rw-rw-  1 aii-agent aii-agent   10723 Sep 29 05:23 common5.py\n-rw-rw-rw-  1 aii-agent aii-agent    1759 Sep 29 05:23 design.py\n-rw-rw-rw-  1 aii-agent aii-agent   12932 Sep 29 05:23 ego.py\n-rw-rw-rw-  1 aii-agent aii-agent    2020 Sep 29 05:23 ego_ctx.py\n-rw-rw-rw-  1 aii-agent aii-agent   11737 Sep 29 05:27 fast6.py\n-rw-rw-rw-  1 aii-agent aii-agent    4856 Sep 29 05:41 fastpsp.py\n-rw-rw-rw-  1 aii-agent aii-agent    3629 Sep 29 05:24 jobs.py\n-rw-rw-rw-  1 aii-agent aii-agent    9137 Sep 29 05:23 ladder.py\n-rw-rw-rw-  1 aii-agent aii-agent    9585 Sep 29 05:33 nullkern.py\n-rw-rw-rw-  1 aii-agent aii-agent    2049 Sep 29 05:23 outc.py\n-rw-rw-rw-  1 aii-agent aii-agent    8080 Sep 29 05:23 rq1stats.py\n-rw-rw-rw-  1 aii-agent aii-agent     378 Sep 29 05:31 s2_cfg.py\n-rw-rw-rw-  1 aii-agent aii-agent    1452 Sep 29 05:30 seal.py\n-rw-rw-rw-  1 aii-agent aii-agent    8655 Sep 29 05:23 stats_core.py\n-rw-rw-rw-  1 aii-agent aii-agent    2011 Sep 29 05:42 tables.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/results:\ntotal 5344\ndrwxrwxrwx  2 aii-agent aii-agent 2000137 Sep 29 06:25 .\ndrwxrwxrwx 10 aii-agent aii-agent 2027929 Sep 29 09:02 ..\n-rw-rw-rw-  1 aii-agent aii-agent  693635 Sep 29 06:17 clean_vs_raw_psp.json\n-rw-rw-rw-  1 aii-agent aii-agent  514025 Sep 29 06:15 clean_vs_raw_psp_cells.json\n-rw-rw-rw-  1 aii-agent aii-agent    4140 Sep 29 06:23 deviations.json\n-rw-rw-rw-  1 aii-agent aii-agent    4134 Sep 29 05:47 frozen_constants_S1b.json\n-rw-rw-rw-  1 aii-agent aii-agent    9939 Sep 29 05:31 frozen_spec.json\n-rw-rw-rw-  1 aii-agent aii-agent    1615 Sep 29 05:25 gate_t0.json\n-rw-rw-rw-  1 aii-agent aii-agent    1272 Sep 29 06:25 headline_check.json\n-rw-rw-rw-  1 aii-agent aii-agent     879 Sep 29 06:19 placebo_calibration.json\n-rw-rw-rw-  1 aii-agent aii-agent     575 Sep 29 05:46 planted_checks.json\n-rw-rw-rw-  1 aii-agent aii-agent   20480 Sep 29 06:20 power_frame_n.json\n-rw-rw-rw-  1 aii-agent aii-agent    2933 Sep 29 06:21 prediction_check.json\n-rw-rw-rw-  1 aii-agent aii-agent    2144 Sep 29 06:18 rederive.json\n-rw-rw-rw-  1 aii-agent aii-agent   38862 Sep 29 05:52 reliability.json\n-rw-rw-rw-  1 aii-agent aii-agent   37658 Sep 29 05:49 reliability_x.json\n-rw-rw-rw-  1 aii-agent aii-agent  100198 Sep 29 05:50 size_dependence.json\n-rw-rw-rw-  1 aii-agent aii-agent    1371 Sep 29 06:22 unit_tests.json\n-rw-rw-rw-  1 aii-agent aii-agent    2038 Sep 29 05:29 unit_tests_fast6.json\n-rw-rw-rw-  1 aii-agent aii-agent     820 Sep 29 05:42 unit_tests_fastpsp.json\n-rw-rw-rw-  1 aii-agent aii-agent    1139 Sep 29 05:49 unit_tests_nulls.json\n-rw-rw-rw-  1 aii-agent aii-agent     852 Sep 29 05:46 v3_nulls_full.json\n215 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/method.py\n/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/:\ntotal 2961\ndrwxrwxrwx 3 aii-agent aii-agent 1002698 Sep 30 02:15 .\ndrwxrwxrwx 7 aii-agent aii-agent 2000170 Sep 30 02:14 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 02:14 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 02:15 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   27685 Sep 30 02:15 .repl_agent.ptylog\n\n/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/.aii:\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 02:14 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002698 Sep 30 02:15 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-30 02:15:47 UTC

```
Read method.py and preview output:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat $W/method.py; echo ======; cat $W/preview_method_out.json | head -c 6000; echo; cat $W/pyproject.toml
```

### [10] TOOL RESULT — Bash · 2026-09-30 02:15:49 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.\n\nStages (each a standalone, resumable script; run in this order by `python method.py --run-all`):\n  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)\n  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)\n  s1_freeze.py          frozen spec + seal (before any outcome join)\n  s2_variants.py        RAW, V1 rarefaction, V2 permutation null, V2b Chao Jaccard, V4 split halves\n  s3_nulls.py           V3a backbone rewiring, V3b k-matched density null, V3c curveball persistence null\n  tests/u_nulls.py      U3 curveball uniformity, U4 rewire calibration\n  tests/planted.py      PC1 stationary thin-sample simulation, PC2 planted churn\n  s4_composites.py      clean composites, S1b constants seal, V4 reliability (X side)\n  s4b_outcome_rel.py    outcome reliability (O2r_m50, m = 25 halves)\n  s5_size.py            size-dependence diagnostics\n  s6_assoc.py           partial Spearman ladder per body / pooled, paired clean-vs-raw, groups, PC3\n  s7_verdict.py         DL, disattenuation, P1-P3, Holm, VERDICT, figures\n  s8_power.py           Frame-N power simulation\n  rederive.py           independent re-derivation of the P1-P3 numbers and the pooled SB\nThen (this file): method_out.json in exp_gen_sol_out format -- one example per concept with finite O2r_m50;\npredictions from OLS fitted on DEV only (B5 standardised with the frozen EXP10 constants) applied to every body;\nresults/prediction_check.json; the concept-key cross-check against art_O7Dq4L02QnDN.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport math\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy import stats\n\nfrom common import DATA, O5DIR, RES, jdump, setup_logger\n\nSTAGES = [(\"s0_gate.py\", RES / \"gate_t0.json\"), (\"tests/u_fast6.py\", RES / \"unit_tests_fast6.json\"),\n          (\"s1_freeze.py\", RES / \"frozen_spec.json\"), (\"s2_variants.py\", DATA / \"s2_scalars_full.parquet\"),\n          (\"s3_nulls.py\", DATA / \"v3_nulls_full.parquet\"), (\"tests/u_nulls.py\", RES / \"unit_tests_nulls.json\"),\n          (\"tests/planted.py\", RES / \"planted_checks.json\"), (\"s4_composites.py\", DATA / \"clean_variants.parquet\"),\n          (\"s4b_outcome_rel.py\", RES / \"reliability.json\"), (\"s5_size.py\", RES / \"size_dependence.json\"),\n          (\"s6_assoc.py\", RES / \"clean_vs_raw_psp_cells.json\"), (\"s7_verdict.py\", RES / \"clean_vs_raw_psp.json\"),\n          (\"s8_power.py\", RES / \"power_frame_n.json\"), (\"rederive.py\", RES / \"rederive.json\")]\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nPRED_X = {\"B5\": None, \"B5_plus_NOVCHURN_raw\": \"NOVCHURN_raw\", \"B5_plus_NOVCHURN_exc\": \"NOVCHURN_exc\",\n          \"B5_plus_NOVCHURN_cfg\": \"NOVCHURN_cfg\", \"B5_plus_OPEN_home\": \"OPEN_home\",\n          \"B5_plus_OPEN_home_clean\": \"OPEN_home_clean\"}\nINPUT_COLS = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"new_edge_rate__raw\", \"n_comm_W3__raw\",\n              \"participation__raw\", \"NOVCHURN_raw\", \"OPEN_home\", \"NOV_res_rare10\", \"edge_persistence_rare10\",\n              \"NOVCHURN_rare10\", \"NOV_res_rare5\", \"edge_persistence_rare5\", \"NOVCHURN_rare5\", \"NOV_res_exc\",\n              \"edge_persistence_exc\", \"edge_persistence_nullmean\", \"NOVCHURN_exc\", \"EP_chao\", \"NOVCHURN_chao\",\n              \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\", \"excess_pers_cfg\", \"NOVCHURN_cfg\", \"OPEN_home_clean\",\n              \"OPEN_home_exc\"]\n\n\ndef run_stages(force: bool) -> None:\n    for script, out in STAGES:\n        if out.exists() and not force:\n            logger.info(f\"skip {script} ({out.name} exists)\")\n            continue\n        if script == \"s1_freeze.py\" and out.exists():\n            logger.warning(\"frozen_spec.json exists: never re-freeze (seal)\")\n            continue\n        logger.info(f\"running {script}\")\n        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)\n\n\ndef concept_key_check() -> dict:\n    \"\"\"Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its\n    concept_recognition table and agreement of the OpenAlex level.\"\"\"\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\", columns=[\"concept_id\", \"body\"])\n    from common import DATA_IN\n    lev = pd.concat([pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"concept_id\", \"level\"]),\n                     pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"concept_id\", \"level\"])])\n    norm = lambda v: \"C\" + str(v).lstrip(\"C\").split(\".\")[0]  # noqa: E731  (frame ids are numeric; O5 uses 'C...')\n    lev = dict(zip(lev.concept_id.map(norm), lev.level))\n    cv[\"concept_id\"] = cv.concept_id.map(norm)\n    ids = set(cv.concept_id)\n    seen, level_ok, n_rec = {}, 0, 0\n    for p in sorted((O5DIR / \"full_data_out\").glob(\"full_data_out_*.json\")):\n        d = json.loads(p.read_text())\n        for ds in d[\"datasets\"]:\n            if ds[\"dataset\"] != \"concept_recognition\":\n                continue\n            for e in ds[\"examples\"]:\n                n_rec += 1\n                cid = e.get(\"metadata_openalex_id\")\n                if cid in ids:\n                    seen[cid] = e.get(\"metadata_level\")\n        del d\n    for cid, lv in seen.items():\n        if cid in lev and lv is not None and int(lv) == int(lev[cid]):\n            level_ok += 1\n    cov = cv.assign(found=cv.concept_id.isin(seen))\n    return {\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\",\n            \"n_recognition_rows\": n_rec, \"n_analysed\": int(len(ids)), \"n_found\": int(len(seen)),\n            \"coverage_by_body\": cov.groupby(\"body\").found.mean().round(4).to_dict(),\n            \"level_agreement\": level_ok / max(len(seen), 1)}\n\n\ndef exp12_crosscheck() -> dict:\n    \"\"\"EXP12 (art_uw4OeagJP3rv) open_features.parquet: cross-check of the home-build component values where it\n    overlaps (EXP5 frame). EXP12 used its own home-paper definition, so agreement is reported, not required.\"\"\"\n    from common import RUN_ROOT\n    p = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_12/open_features.parquet\"\n    if not p.exists():\n        return {\"available\": False}\n    o = pd.read_parquet(p)\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    m = cv[cv.frame == \"exp5\"].merge(o, on=\"ci\", suffixes=(\"\", \"_e12\"))\n    out = {\"available\": True, \"n_overlap\": int(len(m))}\n    for k in (\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"):\n        a, b = m[f\"{k}__raw\"].to_numpy(float), m[f\"{k}_home\"].to_numpy(float)\n        ok = np.isfinite(a) & np.isfinite(b)\n        out[k] = {\"n_both_finite\": int(ok.sum()), \"share_equal_1e9\": float(np.mean(np.abs(a[ok] - b[ok]) <= 1e-9)),\n                  \"spearman\": float(stats.spearmanr(a[ok], b[ok])[0]) if ok.sum() > 10 else None}\n    return out\n\n\ndef build_outputs() -> None:\n    from tables import load_tables\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    pm = spec[\"exp10_prediction_models\"][\"B5\"]\n    V = json.loads((RES / \"clean_vs_raw_psp.json\").read_text())\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    pw = json.loads((RES / \"power_frame_n.json\").read_text())\n    sz = json.loads((RES / \"size_dependence.json\").read_text())\n    T = load_tables()[\"POOLED\"]\n    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)\n    Zb = np.column_stack([(T[c].to_numpy(float) - pm[\"mu\"][c]) / pm[\"sd\"][c] for c in B5])\n    dev = (T.body == \"DEV\").to_numpy() & np.all(np.isfinite(Zb), 1)\n    y = T.O2r_m50.to_numpy(float)\n    preds, imputed, coefs = {}, {}, {}\n    for nm, x in PRED_X.items():\n        X = Zb.copy()\n        if x is not None:\n            v = T[x].to_numpy(float)\n            med = float(np.nanmedian(v[dev]))\n            imputed[nm] = ~np.isfinite(v)\n            v = np.where(np.isfinite(v), v, med)\n            X = np.c_[X, v]\n        A = np.c_[np.ones(len(T)), X]\n        okf = dev & np.all(np.isfinite(A), 1)\n        b = np.linalg.lstsq(A[okf], y[okf], rcond=None)[0]\n        coefs[nm] = b.tolist()\n        preds[nm] = A @ b\n    chk = {\"note\": \"OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)\", \"coef\": coefs}\n    for body in (\"OLDHO\", \"COH1014\", \"COH1517\"):\n        m = (T.body == body).to_numpy()\n        ent = {}\n        for nm, p in preds.items():\n            ok = m & np.isfinite(p)\n            ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > 20 else None\n        ent[\"n\"] = int(m.sum())\n        ent[\"gain_vs_B5\"] = {nm: (ent[nm] - ent[\"B5\"]) if ent[nm] is not None and ent[\"B5\"] is not None else None\n                             for nm in PRED_X if nm != \"B5\"}\n        chk[body] = ent\n    jdump(chk, RES / \"prediction_check.json\")\n    exs = []\n    for i, r in T.iterrows():\n        inp = {\"concept_id\": str(r.concept_id), \"name\": str(r[\"name\"]), \"body\": r.body, \"t0\": int(r.t0),\n               \"n_home_early\": int(r.n_home_early)}\n        for c in INPUT_COLS:\n            v = r[c]\n            inp[c] = None if not np.isfinite(v) else round(float(v), 6)\n        e = {\"input\": json.dumps(inp), \"output\": f\"{r.O2r_m50:.6f}\"}\n        for nm, p in preds.items():\n            e[f\"predict_{nm}\"] = f\"{p[i]:.6f}\" if np.isfinite(p[i]) else \"nan\"\n        e[\"metadata_body\"] = r.body\n        e[\"metadata_agroup\"] = r.agroup\n        e[\"metadata_O2r_resid\"] = None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)\n        e[\"metadata_imputed_variants\"] = [nm for nm in imputed if imputed[nm][i]]\n        e[\"metadata_missing_clean_variants\"] = [c for c in (\"NOVCHURN_exc\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\",\n                                                            \"OPEN_home_clean\") if not np.isfinite(r[c])]\n        exs.append(e)\n    vd = V[\"verdict\"]\n    head = {h[\"variant\"]: {b: h[b].get(\"psp\") for b in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\")}\n            for h in V[\"headline_R2_O2r_m50\"]}\n    meta = {\"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled \"\n                           \"variants)\",\n            \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n            \"verdict\": vd[\"verdict\"], \"DEGREE_ARTEFACT_PERSISTENCE\": vd[\"DEGREE_ARTEFACT_PERSISTENCE\"],\n            \"predictions_P1_P3\": {k: v[\"holds\"] for k, v in V[\"predictions\"].items()},\n            \"P_detail\": V[\"predictions\"], \"headline_psp_R2_O2r_m50\": head,\n            \"reliability_pooled_SB\": {k: v[\"pooled\"][\"SB\"] for k, v in rel[\"variants\"].items()},\n            \"outcome_reliability_SB\": rel[\"outcome\"][\"O2r_m50\"][\"pooled\"][\"SB\"],\n            \"thin_sample_share_R2\": sz[\"thin_sample_share\"][\"POOLED\"][\"R2\"],\n            \"power_plain_language\": pw[\"plain_language\"],\n            \"concept_key_check\": concept_key_check(), \"exp12_home_crosscheck\": exp12_crosscheck(),\n            \"n_examples\": len(exs), \"prediction_models\": \"OLS on DEV (B5 standardised with EXP10 frozen mu/sd); \"\n                                                         \"NaN variants imputed with the DEV median (flagged)\"}\n    out = {\"metadata\": meta, \"datasets\": [{\"dataset\": \"selection_concepts\", \"examples\": exs}]}\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)\n                                                     and not math.isfinite(o) else str(o)))\n    logger.info(f\"method_out.json: {len(exs)} examples; verdict {vd['verdict']}\")\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    setup_logger(\"method\")\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--run-all\", action=\"store_true\")\n    ap.add_argument(\"--force\", action=\"store_true\")\n    a = ap.parse_args()\n    if a.run_all:\n        run_stages(a.force)\n    build_outputs()\n\n\nif __name__ == \"__main__\":\n    main()\n======\n{\n  \"metadata\": {\n    \"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled variants)\",\n    \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n    \"verdict\": \"PARTLY_THIN\",\n    \"DEGREE_ARTEFACT_PERSISTENCE\": false,\n    \"predictions_P1_P3\": {\n      \"P1\": false,\n      \"P2\": true,\n      \"P3\": true\n    },\n    \"P_detail\": {\n      \"P1\": {\n        \"holds\": false,\n        \"per_body\": {\n          \"COH1517\": false,\n          \"OLDHO\": false\n        },\n        \"rule\": \"psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, COH1517 AND OLDHO\",\n        \"detail\": {\n          \"COH1517\": {\n            \"ratio\": 0.39594449273340393,\n            \"ratio_ci\": [\n              -0.26906748871819375,\n              0.8842632275100695\n            ],\n            \"psp_exc\": 0.06317913710216283,\n            \"psp_raw_same_sample\": 0.15956564180500524,\n            \"n\": 490\n          },\n          \"OLDHO\": {\n            \"ratio\": 0.046849438574826936,\n            \"ratio_ci\": [\n              -0.5585492463643292,\n              0.44451008406689974\n            ],\n            \"psp_exc\": 0.00558634333483666,\n            \"psp_raw_same_sample\": 0.1192403474785353,\n            \"n\": 1321\n          }\n        }\n      },\n      \"P2\": {\n        \"holds\": true,\n        \"psp\": -0.11558300476164542,\n        \"ci\": [\n          -0.14529406903883194,\n          -0.08637301651544306\n        ],\n        \"n\": 4262\n      },\n      \"P3\": {\n        \"holds\": true,\n        \"spearman_NOVCHURN_exc_log_n_all\": 0.033912654545104295,\n        \"ci\": [\n          0.015390987055309715,\n          0.05379348390665524\n        ],\n        \"n\": 9945,\n        \"spearman_on_analysis_sample\": 0.025460592516112258,\n        \"n_analysis\": 6203\n      }\n    },\n    \"headline_psp_R2_O2r_m50\": {\n      \"NOVCHURN_raw\": {\n        \"DEV\": 0.11582989542542993,\n        \"OLDHO\": 0.11299617572105293,\n        \"COH1014\": 0.11291907864162055,\n        \"COH1517\": 0.16119061802773654,\n        \"POOLED\": 0.11623313287281345\n      },\n      \"NOVCHURN_exc\": {\n        \"DEV\": 0.008098203486714372,\n        \"OLDHO\": 0.00558634333483666,\n        \"COH1014\": -0.006870368459004022,\n        \"COH1517\": 0.06317913710216283,\n        \"POOLED\": 0.007587062448167491\n      },\n      \"NOVCHURN_zperm\": {\n        \"DEV\": 0.006916483037342574,\n        \"OLDHO\": 0.021111779061880425,\n        \"COH1014\": -0.003119936374835825,\n        \"COH1517\": 0.07310759071781775,\n        \"POOLED\": 0.01180160291013356\n      },\n      \"NOVCHURN_rare5\": {\n        \"DEV\": 0.12745259057751135,\n        \"OLDHO\": 0.13960059816790388,\n        \"COH1014\": 0.14930816562962054,\n        \"COH1517\": 0.10532291566998955,\n        \"POOLED\": 0.12996354052682005\n      },\n      \"NOVCHURN_rare10\": {\n        \"DEV\": 0.06569371381097262,\n        \"OLDHO\": 0.04379950262510909,\n        \"COH1014\": 0.07637129759177229,\n        \"COH1517\": 0.17575151285385798,\n        \"POOLED\": 0.07816923082828127\n      },\n      \"NOVCHURN_cfg\": {\n        \"DEV\": 0.11457462304585964,\n        \"OLDHO\": 0.07131234431760923,\n        \"COH1014\": 0.1140931024481054,\n        \"COH1517\": 0.08826828288683536,\n        \"POOLED\": 0.10594463038390994\n      },\n      \"NOVCHURN_chao\": {\n        \"DEV\": 0.10698152321165955,\n        \"OLDHO\": 0.1233546575600449,\n        \"COH1014\": 0.099045199917499,\n        \"COH1517\": 0.15319217229137455,\n        \"POOLED\": 0.10765879115195423\n      },\n      \"NOV_res__raw\": {\n        \"DEV\": 0.07601610353281611,\n        \"OLDHO\": 0.09334461134824705,\n        \"COH1014\": 0.045834617054131964,\n        \"COH1517\": 0.13368999979699825,\n        \"POOLED\": 0.07289621747723708\n      },\n      \"NOV_res_exc\": {\n        \"DEV\": 0.007533048635831106,\n        \"OLDHO\": 0.0017376715450483126,\n        \"COH1014\": -0.023751446414070534,\n        \"COH1517\": 0.07131162741116023,\n        \"POOLED\": 0.0032460635261664567\n      },\n      \"NOV_res_rare10\": {\n        \"DEV\": 0.10165822252527676,\n        \"OLDHO\": 0.06530481243633442,\n        \"COH1014\": 0.04802076491418512,\n        \"COH1517\": 0.20466345078916523,\n        \"POOLED\": 0.09262401396258926\n      },\n      \"edge_persistence__raw\": {\n        \"DEV\": -0.07583315838957445,\n        \"OLDHO\": -0.08575088873836685,\n        \"COH1014\": -0.11596446400103604,\n        \"COH1517\": -0.11231075452403051,\n        \"POOLED\": -0.08781529774927933\n      },\n      \"edge_persistence_exc\": {\n        \"DEV\": 0.005937692599779365,\n        \"OLDHO\": -0.006244389103162552,\n        \"COH1014\": -0.013080007383405107,\n        \"COH1517\": 0.0005956974232039896,\n        \"POOLED\": -0.0034878300740269516\n      },\n      \"edge_persistence_rare10\": {\n        \"DEV\": -0.010345930698610381,\n        \"OLDHO\": -0.03727546428156594,\n        \"COH1014\": -0.05527635256173312,\n        \"COH1517\": -0.05757495031230385,\n        \"POOLED\": -0.030067188997465806\n      },\n      \"z_pers_cfg\": {\n        \"DEV\": -0.10037343516001303,\n        \"OLDHO\": -0.12241732480122985,\n        \"COH1014\": -0.17221528438154363,\n        \"COH1517\": -0.06620030825988972,\n        \"POOLED\": -0.11558300476164542\n      },\n      \"excess_pers_cfg\": {\n        \"DEV\": -0.07661303283377978,\n        \"OLDHO\": -0.0809637692087994,\n        \"COH1014\": -0.11498272444808606,\n        \"COH1517\": -0.12456264454140648,\n        \"POOLED\": -0.08865575533540888\n      },\n      \"EP_chao\": {\n        \"DEV\": -0.08097694830349997,\n        \"OLDHO\": -0.10497623889831854,\n        \"COH1014\": -0.08864289913052632,\n        \"COH1517\": -0.09918889393534806,\n        \"POOLED\": -0.08296530394471821\n      },\n      \"edge_persistence_nullmean\": {\n        \"DEV\": -0.10898168481063225,\n        \"OLDHO\": -0.11635514351174502,\n        \"COH1014\": -0.1428844549750125,\n        \"COH1517\": -0.12303725109093244,\n        \"POOLED\": -0.11965237417042597\n      },\n      \"ego_density_W3__raw\": {\n        \"DEV\": -0.05210843980974512,\n        \"OLDHO\": 0.006218934054215574,\n        \"COH1014\": 0.030366363588382215,\n        \"COH1517\": 0.018455071645998102,\n        \"POOLED\": -0.012520619834223408\n      },\n      \"z_de\n[project]\nname = \"churn-thin-sample-check\"\nversion = \"0.1.0\"\ndescription = \"Is home-neighbourhood churn real or thin-sample noise? Raw vs noise-controlled ego-network variants\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"igraph==1.0.0\",\n  \"interface-meta==2.0.1\",\n  \"kiwisolver==1.5.1\",\n  \"llvmlite==0.49.0\",\n  \"loguru==0.7.3\",\n  \"matplotlib==3.11.2\",\n  \"narwhals==2.26.0\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pillow==12.3.0\",\n  \"psutil==7.2.2\",\n  \"pyarrow==25.0.1\",\n  \"pyparsing==3.3.3\",\n  \"python-dateutil==2.9.0.post0\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"snowballstemmer==3.1.1\",\n  \"statsmodels==0.15.0\",\n  \"texttable==1.7.0\",\n  \"typing-extensions==4.16.0\",\n  \"wrapt==2.5.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-30 02:15:57 UTC

```
Read tables.py, common.py, README:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat $W/lib/tables.py; sed -n 1,80p $W/lib/common.py; cat $W/README.md | head -80
```

### [12] TOOL RESULT — Bash · 2026-09-30 02:15:57 UTC

```
{"stdout": "\"\"\"Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.\nSelection data, outcomes previously unsealed by EXP5/EXP8/EXP10.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN\nfrom ladder import rung_design\n\nCOV = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\", \"type\", \"generic\", \"level\",\n       \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\", \"newborn\", \"t0\", \"agroup\", \"label_coverage_early\",\n       \"home_coverage_early\", \"n_all_early\", \"O2r_m50\", \"O2r_resid\"]\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"]\n\n\ndef load_tables() -> dict[str, pd.DataFrame]:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    cv = cv.drop(columns=[c for c in (\"t0\",) if c in cv.columns])\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\"] + COV)\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\"] + COV + [\"window_flag\"])\n    cv = cv.drop(columns=[c for c in (\"agroup\",) if c in cv.columns])\n    e = cv[cv.frame == \"exp5\"].merge(fe, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    e[\"window_flag\"] = 0\n    c = cv[cv.frame == \"cohort\"].merge(ac, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    pooled = pd.concat([e, c], ignore_index=True)\n    pooled[\"window_flag\"] = pooled.window_flag.fillna(0).astype(int)\n    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}\n    out[\"POOLED\"] = pooled\n    return out\n\n\ndef design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:\n    Bc, Cc = rung_design(df, rung, drop_group=drop_group)\n    if pooled and df.body.nunique() > 1:\n        bs = sorted(df.body.unique())[1:]\n        Cc = pd.concat([Cc, pd.DataFrame({f\"body_{b}\": (df.body == b).astype(float) for b in bs}, index=df.index)],\n                       axis=1)\n        Cc = Cc.loc[:, Cc.std() > 0]\n    return Bc.to_numpy(float), Cc.to_numpy(float)\n\"\"\"Shared constants, paths and small helpers for the RQ1 held-out pipeline.\n\nThe title analyser / surface normaliser / matcher are imported from common5.py (EXP5's common.py, copied verbatim)\nso the matching is byte-identical to the EXP5 scan that defined the frame.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\n\nLIB = Path(__file__).resolve().parent\nROOT = LIB.parent\nsys.path.insert(0, str(LIB))\n\nDATA = ROOT / \"data\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nMODELS = ROOT / \"models\"\nPASSA = ROOT / \"passA\" / \"parts\"\nPASSB = ROOT / \"passB\" / \"parts\"\nfor _d in (DATA, RES, LOGS, FIGS, MODELS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nRUN_ROOT = Path(os.environ.get(\"AII_RUN_ROOT\", str(ROOT.parents[3])))\nEXP5 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_5\"\nEXP3 = RUN_ROOT / \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\"\nEXP8 = RUN_ROOT / \"3_invention_loop/iter_3/gen_art/gen_art_experiment_8\"\n# EXP16 patch: inputs and data are read (read-only) from EXP10; everything written stays under ROOT\nSRC10 = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_10\"\nINPUTS = SRC10 / \"inputs\"\nDATA_IN = SRC10 / \"data\"\nEXP6 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"\nEVAL1 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_evaluation_1\"\nO5DIR = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nMATCH_Y0, MATCH_Y1 = 2000, 2016      # t0 in 2003..2014 -> feature windows t0-3..t0+2 lie in 2000..2016\nTAG_MIN = 0.3\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nUNITS = HELD_GROUPS + [\"COH_DEVHOME\", \"COH_OTHER\"]\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef mix64(x: np.ndarray) -> np.ndarray:\n    \"\"\"splitmix64 finaliser (identical to EXP5 scan_full.mix64).\"\"\"\n    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)\n    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)\n    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)\n    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)\n\n\ndef works_files() -> list[tuple[int, str, int, int]]:\n    man = json.loads((ROOT / \"snapshot/works_manifest.json\").read_text())\n    return [(i, f[\"url\"].replace(\"s3://openalex/\", \"\"), f[\"meta\"][\"content_length\"], f[\"meta\"][\"record_count\"])\n            for i, f in enumerate(man[\"files\"])]\n\n\ndef source_field_lut() -> tuple[np.ndarray, np.ndarray]:\n# Is neighbourhood churn real or thin-sample noise?\n\nA $0-LLM, cache-only confound check of the home-only \"churn / novelty\" signal found by earlier experiments. On the 2015-17 cohort that signal was NOV_res +0.134 and edge_persistence −0.112 (partial Spearman with O2r_m50 at rung R2, EXP10). This artifact asks two things: is the signal real, or a by-product of few papers per year? And is it an artefact of degree dependence?\n\nIt recomputes the raw home-build indicators exactly, then builds noise-controlled versions:\n- **V1**: fixed-n rarefaction.\n- **V2**: a within-concept year-label permutation null, plus a Chao-corrected Jaccard (**V2b**).\n- **V3**: degree-preserving configuration nulls: backbone rewiring, a k-matched random-set null, and curveball-randomised persistence.\n- **V4**: split-half reliability of every variant.\n\nAll variants are compared side by side on the same concepts, with the EXP10 covariate ladder, per body and pooled.\n\n**Label: selection data, outcomes previously unsealed.** Every body's outcomes were already unsealed by EXP5/EXP8/EXP10. The seal (`logs/seal.log`) is a pre-analysis commitment, not a blind. These results are robustness evidence, not confirmation.\n\n## Headline\n\n**Mechanical verdict: `PARTLY_THIN`** (`results/clean_vs_raw_psp.json` → `verdict`). The flag `DEGREE_ARTEFACT_PERSISTENCE` is false.\n\nPartial Spearman with O2r_m50 given B5 + rung R2, 95% concept-bootstrap CI (B = 2000). Source: `results/clean_vs_raw_psp.json → headline_R2_O2r_m50`. \"ret\" is the retention ratio clean/raw on the same concepts, from the paired bootstrap.\n\n| variant | COH1517 | OLDHO | POOLED (n) | pooled ret |\n|---|---|---|---|---|\n| NOVCHURN_raw (EXP10 z's) | +0.161 [0.07, 0.25] | +0.113 [0.06, 0.16] | +0.116 [0.09, 0.14] (6450) | – |\n| NOVCHURN_exc (V2 excess) | +0.063 [−0.02, 0.15] | +0.006 [−0.05, 0.06] | +0.008 [−0.02, 0.03] | 0.06 |\n| NOVCHURN_rare10 (V1, n = 10/yr) | +0.176 [0.05, 0.29] | +0.044 [−0.07, 0.15] | +0.078 [0.04, 0.11] (2874) | 0.68 |\n| NOVCHURN_cfg (V3c curveball z) | +0.088 [−0.02, 0.20] | +0.071 [−0.01, 0.15] | +0.106 [0.07, 0.14] | 1.00 |\n| NOVCHURN_chao (V2b) | +0.153 [0.07, 0.24] | +0.123 [0.07, 0.18] | +0.108 [0.08, 0.13] | 0.91 |\n| edge_persistence raw | −0.112 [−0.20, −0.02] | −0.086 [−0.13, −0.04] | −0.088 [−0.11, −0.07] | – |\n| edge_persistence V2 **null mean** | −0.123 | −0.116 | **−0.120** [−0.14, −0.10] | – |\n| edge_persistence_exc (V2) | +0.001 | −0.006 | −0.003 [−0.03, 0.02] | 0.04 |\n| edge_persistence_rare10 | −0.058 | −0.037 | −0.030 [−0.06, 0.00] | 0.45 |\n| z_pers_cfg (V3c) | −0.066 | −0.122 | −0.116 [−0.15, −0.09] | 1.00 |\n| NOV_res raw | +0.134 | +0.093 | +0.073 | – |\n| NOV_res_exc (V2) | +0.071 | +0.002 | +0.003 | 0.04 |\n| NOV_res_rare10 | +0.205 | +0.065 | +0.093 | 1.01 |\n| ego_density_W3 raw | +0.018 | +0.006 | −0.013 [−0.04, 0.01] | – |\n| z_dens_cfg (V3a) | −0.047 | −0.089 | **−0.091** [−0.12, −0.06] | same-sample diff −0.079 [−0.11, −0.04] |\n| OPEN_home | +0.091 | +0.070 | +0.085 | – |\n| OPEN_home_clean (V3 subs) | +0.129 | +0.094 | **+0.115** [0.09, 0.14] | 1.24 [1.11, 1.43] |\n\n### Reading\n1. **Raw persistence is mostly a sample-size artefact.**\n   - Raw edge persistence has Spearman +0.72 with log n_home_early (`results/size_dependence.json → spearman.edge_persistence__raw.POOLED`).\n   - Its bin means rise 0.00 → 0.09 → 0.27 → 0.38 over n bins 10-19 / 20-49 / 50-99 / ≥100. The V2 null mean (same papers, years shuffled) tracks it almost exactly: 0.00 / 0.10 / 0.28 / 0.39 (`binned_persistence`).\n   - The \"thin-sample share\" (R² of raw persistence on its own V2 null mean) is **0.66** (`thin_sample_share.POOLED.R2`).\n   - At fixed n = 10 papers per year, persistence is nearly flat (0.11 → 0.15). See `figures/persistence_vs_n.png`.\n2. **The churn → outcome association is not temporal churn.**\n   - The excess over the within-concept permutation null carries nothing: NOVCHURN_exc pooled +0.008, retention 0.06. P1 fails: retention is 0.40 in COH1517 and 0.05 in OLDHO.\n   - The V2 null mean itself predicts the outcome as strongly as raw persistence (−0.120 vs −0.088).\n   - So what predicts disciplinary breadth is a static property of the concept's pooled home topic mix at its sample size: how redundant or concentrated its partner topics are. It is not the year-to-year turnover of partners.\n3. **The association is also not \"just paper count\".**\n   - Fixed-n rarefaction keeps 68% pooled; 76% in COH1517 and 64% in OLDHO (`verdict.clauses.V1_retention`).\n   - The Chao-corrected and degree-normalised composites keep 91-100%.\n   - NOV_res survives rarefaction fully (retention 1.01) and is nearly size-free (ρ with log n +0.05).\n   - DL over the 5 pooled groups at R2: NOVCHURN_raw +0.110 [0.085, 0.136], I² = 0, positive in 5/5 groups; NOVCHURN_rare10 +0.081 [0.042, 0.119], 5/5 (`groups`).\n4. **The V2 excess cannot adjudicate on its own.**\n   - Split-half reliability of every V2-excess variant is ≈ 0: NOVCHURN_exc SB = 0.014, edge_persistence_exc 0.046, NOV_res_exc 0.020 (`results/reliability.json → variants.*.pooled.SB`).\n   - The planted-churn check PC2 fails: V2 absorbs about 80% of a planted 50% W3 topic replacement (`results/planted_checks.json`).\n   - So a null V2 result means \"temporal order is unmeasurable at ~10 papers per year\", not \"no churn\".\n5. **Degree normalisation helps OPEN.**\n   - Replacing raw density and persistence by their configuration z's raises OPEN_home pooled from +0.092 to +0.115 on the same sample. The difference is +0.022 [0.011, 0.034] at R2 and +0.023 [0.011, 0.034] at R3.\n   - Raw ego density was null because of its degree dependence (ρ with log degree −0.38). Its degree-normalised version z_dens_cfg is −0.091 pooled: neighbourhoods *less* interlinked than their partners' degrees imply go with broader later uptake.\n   - P2 holds: z_pers_cfg is −0.116 [−0.145, −0.086].\n   - The curveball z does **not** remove size dependence (ρ with log n +0.63), because its null expected Jaccard is ≈ 0 and z ≈ obs/sd.\n\n**Recommended wording for the paper.** Rename \"churn\" to *topical non-redundancy / dispersion of the home neighbourhood*. It is robust to fixed-n rarefaction and to undersampling correction. It is not evidence of year-to-year partner turnover.\n\n### Predictions (frozen in `results/frozen_spec.json`; evaluated in `clean_vs_raw_psp.json → predictions`)\n- **P1 fails.** The same-sample ratio psp(NOVCHURN_exc)/psp(NOVCHURN_raw) at R2 is 0.40 [−0.27, 0.88] in COH1517 (n 490) and 0.05 [−0.56, 0.44] in OLDHO (n 1321).\n- **P2 holds.** z_pers_cfg pooled is −0.116 [−0.145, −0.086] (n 4262).\n- **P3 holds.** Spearman(NOVCHURN_exc, log n) = +0.034 [0.015, 0.054] (n 9945).\n- **Holm (reported only):** p = 0.41 / 0.0005 / 0.002, Holm-adjusted 0.41 / 0.0015 / 0.004.\n- **F6 contingency:** COH1517 has 235 concepts with finite NOVCHURN_rare10 and outcome (≥ 150), so n = 10 stays primary.\n\n### Reliability and disattenuation (`results/reliability.json`)\nPooled Spearman-Brown split-half reliability:\n\n| variant | SB | variant | SB |\n|---|---|---|---|\n| NOV_res | 0.48 | V2 null mean of persistence | 0.71 |", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-30 02:16:07 UTC

```
Inspect result JSON structures:
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M; ls -la $R/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data/ | head; which python3 uv; python3 -c "import pandas, pyarrow; print(pandas.__version__)"; W=$R/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 -c "
import json;V=json.load(open('$W/results/clean_vs_raw_psp.json'));print(list(V.keys()));print(list(V['verdict'].keys()));print(json.dumps(V['headline_R2_O2r_m50'][0])[:1500])
S=json.load(open('$W/results/frozen_spec.json'));print(json.dumps(S['exp10_prediction_models']['B5'])[:800])
rel=json.load(open('$W/results/reliability.json'));print(list(rel['variants'].keys()));print(rel['outcome']['O2r_m50']['pooled'])
pw=json.load(open('$W/results/power_frame_n.json'));print(pw['plain_language'])
sz=json.load(open('$W/results/size_dependence.json'));print(sz['thin_sample_share']['POOLED'])
"
```

### [14] TOOL RESULT — Bash · 2026-09-30 02:16:15 UTC

```
{"stdout": "total 47819\ndrwxrwxrwx  4 aii-agent aii-agent  2005380 Sep 29 03:28 .\ndrwxrwxrwx 15 aii-agent aii-agent  2023575 Sep 29 05:04 ..\n-rw-rw-rw-  1 aii-agent aii-agent   482680 Sep 29 03:22 analysis_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   298030 Sep 29 02:27 bg_topics.npz\n-rw-rw-rw-  1 aii-agent aii-agent   185249 Sep 29 02:22 cohort_candidates.csv\n-rw-rw-rw-  1 aii-agent aii-agent   215822 Sep 29 03:10 cohort_candidates_gated.csv\n-rw-rw-rw-  1 aii-agent aii-agent    35246 Sep 29 03:26 cohort_predictions.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   865822 Sep 29 03:09 concept_types.csv\n-rw-rw-rw-  1 aii-agent aii-agent    16381 Sep 29 02:22 controls.csv\n/usr/local/bin/python3\n/usr/bin/uv\n2.3.3\n['label', 'B', 'seed', 'resampling_unit', 'groups', 'disattenuated', 'F6_contingency', 'predictions', 'verdict', 'holm', 'headline_R2_O2r_m50', 'cells', 'confounds_removed']\n['verdict', 'DEGREE_ARTEFACT_PERSISTENCE', 'clauses', 'label']\n{\"variant\": \"NOVCHURN_raw\", \"DEV\": {\"psp\": 0.11582989542542993, \"ci\": [0.07645046097791196, 0.15251138320592492], \"n\": 2741}, \"OLDHO\": {\"psp\": 0.11299617572105293, \"ci\": [0.0608781889632089, 0.16301318924648014], \"n\": 1404}, \"COH1014\": {\"psp\": 0.11291907864162055, \"ci\": [0.06651637981915953, 0.1584739885511837], \"n\": 1799}, \"COH1517\": {\"psp\": 0.16119061802773654, \"ci\": [0.07066270969979721, 0.25172767820496067], \"n\": 506}, \"POOLED\": {\"psp\": 0.11623313287281345, \"ci\": [0.09133946495128593, 0.1399456352463288], \"n\": 6450}}\n{\"coef\": [4.766039224098753, -0.05511164665586871, 0.008765664104716067, -0.42563667808882066, 1.6369692811444325, 0.2840929545239369], \"mu\": {\"logvol\": 4.387217461299273, \"growth_c\": 0.13591487868338373, \"offhome_share\": 0.2628714872549475, \"entropy\": 0.7831561038968538, \"reach\": 3.228179741051028}, \"sd\": {\"logvol\": 0.3554731095580416, \"growth_c\": 0.43536192389233147, \"offhome_share\": 0.19848326295216012, \"entropy\": 0.4615603694432812, \"reach\": 1.550401785313322}}\n['new_edge_rate__raw', 'n_comm_W3__raw', 'participation__raw', 'NOV_res__raw', 'ego_density_W3__raw', 'edge_persistence__raw', 'NOVCHURN_raw', 'OPEN_home', 'NOV_res_exc', 'edge_persistence_exc', 'ego_density_W3_exc', 'new_edge_rate_exc', 'NOV_res_zperm', 'edge_persistence_zperm', 'ego_density_W3_zperm', 'NOV_res_rare5', 'edge_persistence_rare5', 'ego_density_W3_rare5', 'z_pers_cfg', 'z_dens_cfg', 'z_dens_k', 'edge_persistence_nullmean', 'NOVCHURN_exc', 'NOVCHURN_zperm', 'NOVCHURN_rare5', 'NOVCHURN_cfg', 'OPEN_home_clean', 'OPEN_home_exc']\n{'r_half': 0.8099349043555275, 'SB': 0.8949878831624887, 'n': 7748, 'SB_ci': [0.8904772486259972, 0.8988260126382953], 'SB_boot_sd': 0.002030466617169411}\nAt n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.\n{'R2': 0.6596194882526905, 'n': 12330, 'coef': [-0.0010767111256983803, 0.9746957571903339]}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] ASSISTANT · 2026-09-30 02:16:39 UTC

```
Building the demo subset now: sampling 100 concepts across the four bodies from the artifact's analysis table, plus the aggregate results that `build_outputs()` reads.
```

### [16] TOOL CALL — Bash · 2026-09-30 02:16:39 UTC

```
Write and run mini demo data builder:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; mkdir -p $WS/scripts; cat > $WS/scripts/make_mini_demo_data.py <<'EOF'
"""Build mini_demo_data.json for code_demo.ipynb from the experiment-16 artifact (read-only source).
One dataset: 100 selection concepts (34 DEV + 22 each of OLDHO/COH1014/COH1517) with every column that
method.py:build_outputs() reads, plus the small result-JSON pieces it reads (frozen B5 mu/sd, verdict,
headline psp, reliability, size dependence, power)."""
import json, math, sys
from pathlib import Path
import numpy as np

SRC = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16")
OUT = Path(__file__).resolve().parents[1] / "mini_demo_data.json"
sys.path.insert(0, str(SRC / "lib"))
from tables import load_tables  # noqa: E402

B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
INPUT_COLS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
              "participation__raw", "NOVCHURN_raw", "OPEN_home", "NOV_res_rare10", "edge_persistence_rare10",
              "NOVCHURN_rare10", "NOV_res_rare5", "edge_persistence_rare5", "NOVCHURN_rare5", "NOV_res_exc",
              "edge_persistence_exc", "edge_persistence_nullmean", "NOVCHURN_exc", "EP_chao", "NOVCHURN_chao",
              "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean",
              "OPEN_home_exc"]
N_PER_BODY = {"DEV": 34, "OLDHO": 22, "COH1014": 22, "COH1517": 22}

T = load_tables()["POOLED"]
T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
rng = np.random.default_rng(0)
rows = []
for body, k in N_PER_BODY.items():
    sub = T[(T.body == body) & np.all(np.isfinite(T[B5].to_numpy(float)), 1)]
    # diverse: stratify on outcome quantiles, then sample within strata
    sub = sub.assign(_q=pd_q) if False else sub
    order = np.argsort(sub.O2r_m50.to_numpy())
    picks = np.unique(np.linspace(0, len(order) - 1, k).round().astype(int))
    rows.append(sub.iloc[order[picks]])
import pandas as pd  # noqa: E402
D = pd.concat(rows, ignore_index=True)

def clean(v):
    if isinstance(v, (float, np.floating)):
        return None if not math.isfinite(float(v)) else round(float(v), 6)
    if isinstance(v, (np.integer,)):
        return int(v)
    return v

cols = ["concept_id", "name", "body", "t0", "n_home_early", "agroup", "O2r_m50", "O2r_resid"] + B5 + INPUT_COLS
exs = [{c: clean(r[c]) if c not in ("concept_id", "name", "body", "agroup") else str(r[c]) for c in cols}
       for _, r in D.iterrows()]

spec = json.loads((SRC / "results/frozen_spec.json").read_text())
V = json.loads((SRC / "results/clean_vs_raw_psp.json").read_text())
rel = json.loads((SRC / "results/reliability.json").read_text())
pw = json.loads((SRC / "results/power_frame_n.json").read_text())
sz = json.loads((SRC / "results/size_dependence.json").read_text())
pc = json.loads((SRC / "results/prediction_check.json").read_text())
meta = {
    "description": "Curated 100-concept subset of the experiment-16 analysis table (POOLED, finite O2r_m50) plus the "
                   "result-JSON fragments read by method.py:build_outputs(). Selection data, outcomes previously "
                   "unsealed: robustness evidence, not confirmation.",
    "n_full_table": int(len(T)),
    "n_per_body_demo": N_PER_BODY,
    "frozen_spec": {"exp10_prediction_models": {"B5": {k: spec["exp10_prediction_models"]["B5"][k] for k in ("mu", "sd")}}},
    "clean_vs_raw_psp": {"verdict": {k: V["verdict"][k] for k in ("verdict", "DEGREE_ARTEFACT_PERSISTENCE")},
                         "predictions": V["predictions"],
                         "headline_R2_O2r_m50": V["headline_R2_O2r_m50"]},
    "reliability": {"variants": {k: {"pooled": {"SB": v["pooled"]["SB"]}} for k, v in rel["variants"].items()},
                    "outcome": {"O2r_m50": {"pooled": {"SB": rel["outcome"]["O2r_m50"]["pooled"]["SB"]}}}},
    "power_frame_n": {"plain_language": pw["plain_language"]},
    "size_dependence": {"thin_sample_share": {"POOLED": sz["thin_sample_share"]["POOLED"]}},
    "full_run_prediction_check": {b: {k: pc[b][k] for k in pc[b] if k != "gain_vs_B5"} for b in ("OLDHO", "COH1014", "COH1517")},
}
out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts_table", "examples": exs}]}
OUT.write_text(json.dumps(out, indent=1))
print(OUT, len(exs), D.body.value_counts().to_dict(), OUT.stat().st_size)
EOF
sed -i 's/^    sub = sub.assign(_q=pd_q) if False else sub\n//' $WS/scripts/make_mini_demo_data.py; python3 - <<'EOF'
p='/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/scripts/make_mini_demo_data.py'
s=open(p).read().replace("    sub = sub.assign(_q=pd_q) if False else sub\n","").replace("import pandas as pd  # noqa: E402\nD =","D =").replace("import numpy as np\n","import numpy as np\nimport pandas as pd\n",1)
open(p,'w').write(s)
EOF
cd $WS && python3 scripts/make_mini_demo_data.py
```

### [17] TOOL RESULT — Bash · 2026-09-30 02:16:53 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/mini_demo_data.json 100 {'DEV': 34, 'OLDHO': 22, 'COH1014': 22, 'COH1517': 22} 169301", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-30 02:16:57 UTC

```
Check whether bytecode was written to source lib:
ls -la --time-style=full-iso /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/__pycache__ | head -30; date
```

### [19] TOOL RESULT — Bash · 2026-09-30 02:16:57 UTC

```
{"stdout": "total 2022\ndrwxrwxrwx 2 aii-agent aii-agent 1004832 2026-09-29 21:36:12.000000000 +0000 .\ndrwxrwxrwx 3 aii-agent aii-agent 1014531 2026-09-29 21:36:09.000000000 +0000 ..\n-rw-rw-rw- 1 aii-agent aii-agent   11373 2026-09-29 21:36:10.000000000 +0000 common.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent   16986 2026-09-29 21:36:10.000000000 +0000 ladder.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent   17294 2026-09-29 21:36:12.000000000 +0000 rq1stats.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent    3831 2026-09-29 21:36:09.000000000 +0000 tables.cpython-312.pyc\nWed Sep 30 02:16:56 UTC 2026", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-30 02:17:01 UTC

```
Show jdump helper:
grep -n "def jdump" -A8 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/common.py
```

### [21] TOOL RESULT — Bash · 2026-09-30 02:17:03 UTC

```
{"stdout": "114:def jdump(obj, path: Path) -> None:\n115-    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))\n116-\n117-\n118-def add_deviation(key: str, text: str) -> None:\n119-    p = RES / \"deviations.json\"\n120-    d = json.loads(p.read_text()) if p.exists() else {}\n121-    d[key] = text\n122-    p.write_text(json.dumps(d, indent=1))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Bash · 2026-09-30 02:17:03 UTC

```
Show _clean helper:
sed -n 95,113p /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/common.py
```

### [23] TOOL RESULT — Bash · 2026-09-30 02:17:05 UTC

```
{"stdout": "    return h.hexdigest()\n\n\ndef _clean(o):\n    if isinstance(o, dict):\n        return {str(k): _clean(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [_clean(v) for v in o]\n    if isinstance(o, np.ndarray):\n        return _clean(o.tolist())\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, (np.bool_,)):\n        return bool(o)\n    if isinstance(o, (np.floating, float)):\n        return None if not math.isfinite(float(o)) else float(o)\n    return o", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-30 02:18:31 UTC

````
Generate the demo notebook:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; cat > $WS/scripts/make_notebook.py <<'PYEOF'
"""Generate code_demo.ipynb (cells below). Re-run after editing: python3 scripts/make_notebook.py"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "code_demo.ipynb"
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md(r'''
# Is research-topic churn real or small-sample noise?

**Demo of `method.py`: the orchestrator and output stage of the thin-sample confound check.**

Earlier experiments found that a concept's *home-neighbourhood churn/novelty* (how much its partner topics turn over, and how novel they are, in its early years) predicts how broadly the concept later spreads across disciplines (outcome `O2r_m50`). This experiment asks whether that signal is **real** or a **by-product of thin samples**: concepts with ~10 papers per year will show "churn" just from sampling noise.

The full pipeline (stages `s0_gate.py` … `s8_power.py`) computes raw indicators and several noise-controlled variants for 13,444 concepts:

| variant family | what it controls for |
|---|---|
| `*_raw`, `NOVCHURN_raw`, `OPEN_home` | nothing (original EXP10 indicators) |
| V1 `*_rare5`, `*_rare10` | fixed-n rarefaction (n papers per year) |
| V2 `*_exc`, `*_nullmean`; V2b `EP_chao` | within-concept year-permutation null; Chao-corrected Jaccard |
| V3 `z_dens_cfg`, `z_pers_cfg`, `NOVCHURN_cfg`, `OPEN_home_clean` | degree-preserving configuration nulls |
| V4 | split-half reliability |

`method.py` then (i) optionally runs every stage (`--run-all`) and (ii) always runs **`build_outputs()`**. That function:
1. standardises the B5 baseline covariates with the frozen EXP10 constants,
2. fits OLS predictors of `O2r_m50` **on the DEV body only**: B5 alone and B5 + each churn variant,
3. checks out-of-DEV Spearman on the held-out bodies (OLDHO, COH1014, COH1517),
4. writes `method_out.json`, with one example per concept plus a metadata block summarising the verdict.

This notebook runs step (ii) **with the original code**, on a curated 100-concept subset (`mini_demo_data.json`). The stage scripts need the multi-GB OpenAlex cache, so their *aggregate results* are loaded from the same JSON: frozen spec, verdict, headline partial Spearman, reliability, size dependence and power.

> Label: selection data, outcomes previously unsealed. These results are robustness evidence, not confirmation.
''')

code(r'''
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT pre-installed on Colab, always install
_pip('loguru==0.7.3')

# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
''')

md(r'''
## Imports
This is the original import block of `method.py`. `argparse`, `subprocess` and `sys` are only needed by the CLI and stage runner. The `sys.path` insert and `from common import ...` are replaced further down by small in-notebook equivalents. `matplotlib` is added for the final visualisation.
''')

code(r'''
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

import matplotlib.pyplot as plt  # added for the demo visualisation
''')

md(r'''
## Data loading
`mini_demo_data.json` is fetched from the GitHub repo, with a fallback to a local copy. It holds one dataset, `selection_concepts_table`: 100 concepts (34 DEV + 22 each of OLDHO / COH1014 / COH1517), spread across the outcome range. Each row has every column `build_outputs()` reads. The file's `metadata` also holds the result-JSON fragments the function reads.
''')

code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-16/demo/mini_demo_data.json"
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
print(data["metadata"]["description"])
print("demo rows:", len(data["datasets"][0]["examples"]), "| full analysis table:", data["metadata"]["n_full_table"], "concepts")
''')

md(r'''
## Config
The original `build_outputs()` has no iteration counts. Its only size knob is how many concepts enter the table: all 7,748 with a finite outcome in the full run. The one hard-coded threshold is the minimum body size for reporting an out-of-DEV Spearman (`ok.sum() > 20`).

* `MAX_PER_BODY`: concepts kept per body from the demo table (the demo file has at most 34 DEV / 22 per other body). A value of at least 21 is needed for a held-out body to pass the `> 20` rule.
* `MIN_N_SPEARMAN`: the original threshold, 20.
''')

code(r'''
MAX_PER_BODY = 34      # demo: all 100 rows (34 DEV + 22 x 3). Original full run: no cap (7,748 concepts; DEV 2,7xx)
MIN_N_SPEARMAN = 20    # original hard-coded value in build_outputs(): `ok.sum() > 20`
''')

md(r'''
## Constants (verbatim from `method.py`)
* `STAGES`: the pipeline stage scripts and the output file each produces. It is used only by `run_stages()`, which is shown for reference below.
* `B5`: the five baseline covariates: log volume, growth, off-home share, entropy, reach.
* `PRED_X`: the prediction models. Each is B5 alone or B5 plus one churn variant.
* `INPUT_COLS`: the raw and noise-controlled indicator columns copied into every output example.
''')

code(r'''
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
''')

md(r'''
## Helpers replacing `lib/common.py` and `lib/tables.py`
The original imports `ROOT`, `RES`, `jdump` and `setup_logger` from `lib/common.py`, and `load_tables` from `lib/tables.py`. The original `load_tables()` joins `data/clean_variants.parquet` with the EXP10 covariate/outcome frames. Here it returns the same POOLED table, built from the demo rows (capped at `MAX_PER_BODY` per body). `jdump` and `_clean` are copied verbatim. The result files that the original reads from `results/*.json` come from `data["metadata"]`.
''')

code(r'''
ROOT = Path(".")
RES = ROOT / "results"
RES.mkdir(exist_ok=True)


def _clean(o):  # verbatim from lib/common.py
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


def jdump(obj, path: Path) -> None:  # verbatim from lib/common.py
    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))


def load_tables() -> dict[str, pd.DataFrame]:
    """Demo stand-in for lib/tables.load_tables(): POOLED table from mini_demo_data.json (None -> NaN)."""
    df = pd.DataFrame(data["datasets"][0]["examples"])
    num = [c for c in df.columns if c not in ("concept_id", "name", "body", "agroup")]
    df[num] = df[num].astype(float)
    df = df.groupby("body", sort=False, group_keys=False).head(MAX_PER_BODY).reset_index(drop=True)
    return {"POOLED": df}


logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
''')

md(r'''
### Stage runner and dependency cross-checks (reference only)
`run_stages()` runs the 14 stage scripts in order. `concept_key_check()` and `exp12_crosscheck()` read other artifacts' multi-GB files: the OpenAlex concept-recognition key and the EXP12 feature parquet. None of these can run in a notebook. Their bodies are kept as markdown and replaced by stubs that say they were not run.

```python
def run_stages(force: bool) -> None:
    for script, out in STAGES:
        if out.exists() and not force:
            logger.info(f"skip {script} ({out.name} exists)"); continue
        ...
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)
```
In the full run, `concept_key_check()` found all analysed concepts in the recognition table, with the OpenAlex level agreeing. `exp12_crosscheck()` reported agreement with EXP12's home-build components (informational only).
''')

code(r'''
def concept_key_check() -> dict:
    # needs art_O7Dq4L02QnDN full_data_out/*.json (not shipped with the demo)
    return {"available": False, "note": "not run in demo (needs dependency artifact files)"}


def exp12_crosscheck() -> dict:
    # needs EXP12 open_features.parquet (not shipped with the demo)
    return {"available": False}
''')

md(r'''
## `build_outputs()` step 1: read the frozen spec and results, standardise B5
The code below is the body of `build_outputs()` split into cells. The four `json.loads(... .read_text())` calls now read the same objects from `data["metadata"]`. `pm` holds the **frozen EXP10** mean and sd of the B5 covariates. They were sealed before any outcome join, so standardisation cannot leak outcome information. `dev` marks the DEV-body rows with finite covariates. Only these rows are used for fitting.
''')

code(r'''
M = data["metadata"]
spec = M["frozen_spec"]                   # was: json.loads((RES / "frozen_spec.json").read_text())
pm = spec["exp10_prediction_models"]["B5"]
V = M["clean_vs_raw_psp"]                 # was: json.loads((RES / "clean_vs_raw_psp.json").read_text())
rel = M["reliability"]                    # was: json.loads((RES / "reliability.json").read_text())
pw = M["power_frame_n"]                   # was: json.loads((RES / "power_frame_n.json").read_text())
sz = M["size_dependence"]                 # was: json.loads((RES / "size_dependence.json").read_text())
T = load_tables()["POOLED"]
T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
Zb = np.column_stack([(T[c].to_numpy(float) - pm["mu"][c]) / pm["sd"][c] for c in B5])
dev = (T.body == "DEV").to_numpy() & np.all(np.isfinite(Zb), 1)
y = T.O2r_m50.to_numpy(float)
print(T.body.value_counts().to_dict(), "| DEV rows used for fitting:", int(dev.sum()))
''')

md(r'''
## Step 2: fit the DEV-only OLS prediction models
For each model in `PRED_X`, the design matrix is intercept + standardised B5, plus the churn variant if the model has one. A missing variant value (NaN, e.g. too few papers for rarefaction) is imputed with the **DEV median** and flagged in `imputed`. Coefficients come from least squares on DEV rows only, and predictions are made for every row.
''')

code(r'''
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
for nm, b in coefs.items():
    print(f"{nm:<26} intercept {b[0]:+.3f}   extra-variant coef {'' if len(b) == 6 else f'{b[-1]:+.3f}'}")
''')

md(r'''
## Step 3: out-of-DEV check
For each held-out body, the code computes the Spearman correlation between each model's prediction and the observed outcome, then each variant model's **gain over B5**. The artifact expects this gain to be about 0: the churn variants add little *predictive* signal beyond B5, even when their partial correlations are nonzero. The only edit is that `20` is now `MIN_N_SPEARMAN`.
''')

code(r'''
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
print(json.dumps({b: {k: (round(v, 3) if isinstance(v, float) else v) for k, v in chk[b].items() if k != "gain_vs_B5"}
                  for b in ("OLDHO", "COH1014", "COH1517")}, indent=1))
''')

md(r'''
## Step 4: build one output example per concept (`exp_gen_sol_out` format)
Each example carries:
* `input`: a JSON string with the concept id, name, body, `t0`, `n_home_early` and all `INPUT_COLS`,
* `output`: the observed `O2r_m50`,
* `predict_<model>`: each model's prediction,
* flags for imputed or missing clean variants.
''')

code(r'''
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
''')

md(r'''
## Step 5: metadata block and `method_out.json`
The metadata block summarises the whole pipeline:
* the mechanical **verdict** (`PARTLY_THIN`),
* whether predictions P1–P3 hold,
* the headline partial Spearman ρ of each variant with `O2r_m50` given B5 + R2, per body and pooled,
* pooled split-half (Spearman–Brown) reliabilities,
* the thin-sample share: R² of raw persistence on its own permutation-null mean,
* the power statement.
''')

code(r'''
vd = V["verdict"]
head = {h["variant"]: {b: h[b].get("psp") for b in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED")}
        for h in V["headline_R2_O2r_m50"]}
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
        "concept_key_check": concept_key_check(), "exp12_home_crosscheck": exp12_crosscheck(),
        "n_examples": len(exs), "prediction_models": "OLS on DEV (B5 standardised with EXP10 frozen mu/sd); "
                                                     "NaN variants imputed with the DEV median (flagged)"}
out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts", "examples": exs}]}
(ROOT / "method_out.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)
                                                 and not math.isfinite(o) else str(o)))
logger.info(f"method_out.json: {len(exs)} examples; verdict {vd['verdict']}")
''')

md(r'''
## Results
Three views follow:
1. **Verdict and predictions.**
2. **Headline partial Spearman (pooled, full run of 6k+ concepts).** Raw churn vs its noise-controlled variants. The V2 permutation-excess variants (`*_exc`) collapse to about 0. Fixed-n rarefaction (`rare10`), Chao and configuration-null variants keep most of the signal. So the association reflects a *static* dispersion of the home topic mix, not temporal partner turnover.
3. **Demo re-run of `build_outputs()`.** Out-of-DEV Spearman of each model's prediction on this 100-concept subset, next to the full-run values, plus a scatter of predictions against outcomes. With only 22 held-out concepts per body, the demo numbers are noisy. Read them as a working demonstration of the code, not a replication.
''')

code(r'''
print(f"VERDICT: {meta['verdict']}   DEGREE_ARTEFACT_PERSISTENCE: {meta['DEGREE_ARTEFACT_PERSISTENCE']}")
for k, v in V["predictions"].items():
    print(f"  {k}: {'holds' if v['holds'] else 'FAILS'}")
print(f"thin-sample share R2 (raw persistence ~ its V2 null mean): {meta['thin_sample_share_R2']:.2f}")
print(f"outcome reliability SB: {meta['outcome_reliability_SB']:.3f}")
print("power:", meta["power_plain_language"][:200], "...")

# --- headline table (full run) ---
hd = pd.DataFrame(head).T[["DEV", "OLDHO", "COH1014", "COH1517", "POOLED"]]
sb = pd.Series(meta["reliability_pooled_SB"], name="SB_pooled")
hd = hd.join(sb, how="left")
print("\nHeadline partial Spearman with O2r_m50 | B5 + R2 (full run):")
print(hd.round(3).to_string())

# --- demo vs full-run out-of-DEV Spearman ---
full_pc = M["full_run_prediction_check"]
rows = []
for body in ("OLDHO", "COH1014", "COH1517"):
    for nm in PRED_X:
        rows.append({"body": body, "model": nm, "demo_rho": chk[body][nm], "full_rho": full_pc[body][nm]})
cmp = pd.DataFrame(rows).pivot(index="model", columns="body", values=["demo_rho", "full_rho"])
print("\nOut-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run")
print(cmp.round(3).to_string())

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
# (a) headline pooled psp with CIs
H = {h["variant"]: h["POOLED"] for h in V["headline_R2_O2r_m50"]}
order = [v for v in ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_rare10", "NOVCHURN_chao", "NOVCHURN_cfg",
                     "edge_persistence__raw", "edge_persistence_nullmean", "edge_persistence_exc", "z_pers_cfg",
                     "ego_density_W3__raw", "z_dens_cfg", "OPEN_home", "OPEN_home_clean"] if v in H]
ps = np.array([H[v]["psp"] for v in order])
ci = np.array([H[v].get("ci") or [np.nan, np.nan] for v in order], dtype=float)
col = ["tab:gray" if ("raw" in v or v == "OPEN_home") else ("tab:red" if ("exc" in v or "nullmean" in v) else "tab:blue")
       for v in order]
ax = axes[0]
ax.barh(range(len(order)), ps, color=col, xerr=np.abs(np.vstack([ps - ci[:, 0], ci[:, 1] - ps])), capsize=3)
ax.set_yticks(range(len(order))); ax.set_yticklabels(order, fontsize=8); ax.invert_yaxis(); ax.axvline(0, c="k", lw=.8)
ax.set_xlabel("pooled partial Spearman with O2r_m50 | B5+R2"); ax.set_title("(a) full run: raw (grey) vs V2 null (red) vs other clean (blue)")
# (b) demo vs full out-of-DEV rho
ax = axes[1]
models = list(PRED_X); xs = np.arange(len(models)); w = 0.13
for j, body in enumerate(("OLDHO", "COH1014", "COH1517")):
    ax.bar(xs + (2 * j - 2.5) * w, [chk[body][m] if chk[body][m] is not None else np.nan for m in models], w,
           label=f"demo {body}", alpha=.9)
    ax.bar(xs + (2 * j - 1.5) * w, [full_pc[body][m] for m in models], w, label=f"full {body}", alpha=.45)
ax.set_xticks(xs); ax.set_xticklabels([m.replace("B5_plus_", "+") for m in models], rotation=30, ha="right", fontsize=8)
ax.set_ylabel("out-of-DEV Spearman"); ax.set_title("(b) DEV-fitted OLS: demo subset vs full run"); ax.legend(fontsize=7, ncol=2)
# (c) scatter predictions vs outcome
ax = axes[2]
for body, mk in zip(("DEV", "OLDHO", "COH1014", "COH1517"), "osD^"):
    m = (T.body == body).to_numpy()
    ax.scatter(preds["B5_plus_NOVCHURN_raw"][m], y[m], marker=mk, s=25, alpha=.75, label=body)
ax.set_xlabel("predicted O2r_m50 (B5 + NOVCHURN_raw, DEV-fitted)"); ax.set_ylabel("observed O2r_m50")
ax.set_title("(c) demo: prediction vs outcome"); ax.legend(fontsize=8)
plt.tight_layout(); plt.show()
''')

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python", "version": "3.12"}},
      "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i:02d}"
    c["source"] = c["source"].splitlines(keepends=True)
OUT.write_text(json.dumps(nb, indent=1))
print("wrote", OUT, len(cells), "cells")
PYEOF
cd $WS && python3 scripts/make_notebook.py
````

### [25] TOOL RESULT — Bash · 2026-09-30 02:18:33 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb 27 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-30 02:18:39 UTC

```
Notebook generated. Testing first at the minimum config (21 concepts per body), then scaling up.
```

### [27] TOOL CALL — Bash · 2026-09-30 02:18:39 UTC

```
Test-run notebook at minimum config:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; cd $WS && sed -i 's/^MAX_PER_BODY = 34 /MAX_PER_BODY = 21 /' scripts/make_notebook.py && python3 scripts/make_notebook.py && grep -c "MAX_PER_BODY = 21" code_demo.ipynb
E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && start=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20; echo "runtime $(( $(date +%s)-start ))s"
```

### [28] TOOL RESULT — Bash · 2026-09-30 02:20:37 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb 27 cells\n1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 184128 bytes to code_demo.ipynb\nruntime 104s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-30 02:20:41 UTC

```
Show notebook outputs:
python3 -c "
import json;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': print(''.join(o['text'])[:2500]); print('---')
    elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    else: print(o['output_type'], list(o.get('data',{}).keys()))
"
```

### [30] TOOL RESULT — Bash · 2026-09-30 02:20:43 UTC

```
{"stdout": "Curated 100-concept subset of the experiment-16 analysis table (POOLED, finite O2r_m50) plus the result-JSON fragments read by method.py:build_outputs(). Selection data, outcomes previously unsealed: robustness evidence, not confirmation.\ndemo rows: 100 | full analysis table: 7748 concepts\n\n---\nexecute_result ['text/plain']\n{'DEV': 21, 'OLDHO': 21, 'COH1014': 21, 'COH1517': 21} | DEV rows used for fitting: 21\n\n---\nB5                         intercept +3.449   extra-variant coef \nB5_plus_NOVCHURN_raw       intercept +3.478   extra-variant coef -0.150\nB5_plus_NOVCHURN_exc       intercept +3.500   extra-variant coef -0.130\nB5_plus_NOVCHURN_cfg       intercept +3.441   extra-variant coef -0.032\nB5_plus_OPEN_home          intercept +3.433   extra-variant coef +0.650\nB5_plus_OPEN_home_clean    intercept +3.497   extra-variant coef +0.319\n\n---\n{\n \"OLDHO\": {\n  \"B5\": -0.056,\n  \"B5_plus_NOVCHURN_raw\": -0.027,\n  \"B5_plus_NOVCHURN_exc\": -0.016,\n  \"B5_plus_NOVCHURN_cfg\": -0.056,\n  \"B5_plus_OPEN_home\": 0.016,\n  \"B5_plus_OPEN_home_clean\": 0.004,\n  \"n\": 21\n },\n \"COH1014\": {\n  \"B5\": 0.397,\n  \"B5_plus_NOVCHURN_raw\": 0.414,\n  \"B5_plus_NOVCHURN_exc\": 0.43,\n  \"B5_plus_NOVCHURN_cfg\": 0.394,\n  \"B5_plus_OPEN_home\": 0.388,\n  \"B5_plus_OPEN_home_clean\": 0.404,\n  \"n\": 21\n },\n \"COH1517\": {\n  \"B5\": 0.531,\n  \"B5_plus_NOVCHURN_raw\": 0.432,\n  \"B5_plus_NOVCHURN_exc\": 0.512,\n  \"B5_plus_NOVCHURN_cfg\": 0.495,\n  \"B5_plus_OPEN_home\": 0.63,\n  \"B5_plus_OPEN_home_clean\": 0.636,\n  \"n\": 21\n }\n}\n\n---\n84 examples; first one:\n{\n \"input\": \"{\\\"concept_id\\\": \\\"2779619083\\\", \\\"name\\\": \\\"Essure\\\", \\\"body\\\": \\\"DEV\\\", \\\"t0\\\": 2007, \\\"n_home_early\\\": 91, \\\"NOV_res__raw\\\": null, \\\"edge_persistence__raw\\\": 0.466667, \\\"ego_density_W3__raw\\\": 1.0, \\\"new_edge_rate__raw\\\": 0.0, \\\"n_comm_W3__raw\\\": 3.0, \\\"participation__raw\\\": 0.65625, \\\"NOVCHURN_raw\\\": null, \\\"OPEN_home\\\": -0.141717, \\\"NOV_res_rare10\\\": null, \\\"edge_persistence_rare10\\\": 0.105, \\\"NOVCHURN_rare10\\\": null, \\\"NOV_res_rare5\\\": null, \\\"edge_persistence_rare5\\\": 0.035714, \\\"NOVCHURN_rare5\\\": null, \\\"NOV_res_exc\\\": null, \\\"edge_persistence_exc\\\": -0.023699, \\\"edge_persistence_nullmean\\\": 0.490366, \\\"NOVCHURN_exc\\\": null, \\\"EP_chao\\\": 0.589709, \\\"NOVCHURN_chao\\\": null, \\\"z_dens_cfg\\\": 12.917785, \\\"z_dens_k\\\": 7.374662, \\\"z_pers_cfg\\\": null, \\\"excess_pers_cfg\\\": 0.466667, \\\"NOVCHURN_cfg\\\": null, \\\"OPEN_home_clean\\\": 0.546166, \\\"OPEN_home_exc\\\": 0.476757}\",\n \"output\": \"1.000000\",\n \"predict_B5\": \"2.593242\",\n \"predict_B5_plus_NOVCHURN_raw\": \"2.484840\",\n \"predict_B5_plus_NOVCHURN_exc\": \"2.551036\",\n \"predict_B5_plus_NOVCHURN_cfg\": \"2.592274\",\n \"predict_B5_plus_OPEN_home\": \"2.627751\",\n \"predict_B5_plus_OPEN_home_clean\": \"2.695922\",\n \"metadata_body\": \"DEV\",\n \"metadata_agroup\": \"BGM+Med\",\n \"metadata_O2r_resid\": -3.555508,\n \"metadata_imputed_variants\": [\n  \"B5_plus_NOVCHURN_raw\",\n  \"B5_plus_NOVCHURN_exc\",\n  \"B5_plus_NOVCHURN_cfg\"\n ],\n \"metadata_missing_clean_variants\": [\n  \"NOVCHURN_exc\",\n  \"NOVCHURN_rare10\",\n  \"NOVCHURN_cfg\"\n ]\n}\n\n---\n02:20:32|INFO   |method_out.json: 84 examples; verdict PARTLY_THIN\n\n---\nVERDICT: PARTLY_THIN   DEGREE_ARTEFACT_PERSISTENCE: False\n  P1: FAILS\n  P2: holds\n  P3: holds\nthin-sample share R2 (raw persistence ~ its V2 null mean): 0.66\noutcome reliability SB: 0.895\npower: At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T ...\n\nHeadline partial Spearman with O2r_m50 | B5 + R2 (full run):\n\n---\n                             DEV  OLDHO  COH1014  COH1517  POOLED  SB_pooled\nNOVCHURN_raw               0.116  0.113    0.113    0.161   0.116      0.476\nNOVCHURN_exc               0.008  0.006   -0.007    0.063   0.008      0.014\nNOVCHURN_zperm             0.007  0.021   -0.003    0.073   0.012      0.023\nNOVCHURN_rare5             0.127  0.140    0.149    0.105   0.130      0.359\nNOVCHURN_rare10            0.066  0.044    0.076    0.176   0.078        NaN\nNOVCHURN_cfg               0.115  0.071    0.114    0.088   0.106      0.618\nNOVCHURN_chao              0.107  0.123    0.099    0.153   0.108        NaN\nNOV_res__raw               0.076  0.093    0.046    0.134   0.073      0.478\nNOV_res_exc                0.008  0.002   -0.024    0.071   0.003      0.020\nNOV_res_rare10             0.102  0.065    0.048    0.205   0.093        NaN\nedge_persistence__raw     -0.076 -0.086   -0.116   -0.112  -0.088      0.570\nedge_persistence_exc       0.006 -0.006   -0.013    0.001  -0.003      0.046\nedge_persistence_rare10   -0.010 -0.037   -0.055   -0.058  -0.030        NaN\nz_pers_cfg                -0.100 -0.122   -0.172   -0.066  -0.116      0.709\nexcess_pers_cfg           -0.077 -0.081   -0.115   -0.125  -0.089        NaN\nEP_chao                   -0.081 -0.105   -0.089   -0.099  -0.083        NaN\nedge_persistence_nullmean -0.109 -0.116   -0.143   -0.123  -0.120      0.707\nego_density_W3__raw       -0.052  0.006    0.030    0.018  -0.013      0.412\nz_dens_cfg                -0.087 -0.089   -0.127   -0.047  -0.091      0.698\nz_dens_k                  -0.052 -0.050   -0.083    0.042  -0.047      0.657\nOPEN_home                  0.109  0.070    0.074    0.091   0.085      0.485\nOPEN_home_clean            0.133  0.094    0.108    0.129   0.115      0.577\nOPEN_home_exc              0.072  0.035    0.041    0.070   0.052      0.486\n\nOut-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run\n                        demo_rho                full_rho               \nbody                     COH1014 COH1517  OLDHO  COH1014 COH1517  OLDHO\nmodel                                                                  \nB5                         0.397   0.531 -0.056    0.759   0.785  0.705\nB5_plus_NOVCHURN_cfg       0.394   0.495 -0.056    0.761   0.786  0.707\nB5_plus_NOVCHURN_exc       0.430   0.512 -0.016    0.759   0.785  0.705\nB5_plus_NOVCHURN_raw       0.414   0.432 -0.027    0.762   0.789  0.710\nB5_plus_OPEN_home          0.388   0.630  0.016    0.761   0.787  0.707\nB5_plus_O\n---\ndisplay_data ['image/png', 'text/plain']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] THINKING · 2026-09-30 02:20:57 UTC

```
Runs cleanly in 104 s at minimum config, but I noticed the demo rows are sorted by outcome, so taking the first N keeps only low-outcome concepts and skews the demo ρ down. I'll shuffle the rows and prioritize concepts with churn variants defined.
```

### [32] TOOL CALL — Bash · 2026-09-30 02:20:57 UTC

```
Regenerate shuffled data and retest at 21/body:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; cd $WS && python3 - <<'EOF'
p='scripts/make_mini_demo_data.py'
s=open(p).read()
s=s.replace('''    sub = T[(T.body == body) & np.all(np.isfinite(T[B5].to_numpy(float)), 1)]
''','''    sub = T[(T.body == body) & np.all(np.isfinite(T[B5].to_numpy(float)), 1)
            & np.isfinite(T.NOVCHURN_raw) & np.isfinite(T.OPEN_home)]
''')
s=s.replace('''    rows.append(sub.iloc[order[picks]])''','''    # spread over the outcome range, then shuffled so any head(k) of a body is itself a diverse subset
    rows.append(sub.iloc[rng.permutation(order[picks])])''')
open(p,'w').write(s)
p='scripts/make_notebook.py'
s=open(p).read()
s=s.replace('logger.remove()\nlogger.add(sys.stdout','logger.remove()\n_ = logger.add(sys.stdout')
s=s.replace("The demo file has at most 34 DEV / 22 per other body","The demo file has at most 34 DEV / 22 per other body, rows shuffled")
open(p,'w').write(s)
EOF
grep -n "permutation\|isfinite(T.NOV" scripts/make_mini_demo_data.py; python3 scripts/make_mini_demo_data.py && python3 scripts/make_notebook.py
E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && start=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s)-start ))s"
```

### [33] TOOL RESULT — Bash · 2026-09-30 02:23:01 UTC

```
{"stdout": "30:            & np.isfinite(T.NOVCHURN_raw) & np.isfinite(T.OPEN_home)]\n35:    rows.append(sub.iloc[rng.permutation(order[picks])])\n/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/mini_demo_data.json 100 {'DEV': 34, 'OLDHO': 22, 'COH1014': 22, 'COH1517': 22} 169820\nwrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb 27 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 186532 bytes to code_demo.ipynb\nruntime 103s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] ASSISTANT · 2026-09-30 02:23:11 UTC

```
Passes at 21/body. Scaling to the full demo subset (34 DEV + 22 per held-out body, 100 concepts):
```

### [35] TOOL CALL — Bash · 2026-09-30 02:23:11 UTC

```
Scale to all demo rows, test, show outputs:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; cd $WS && sed -i 's/^MAX_PER_BODY = 21 /MAX_PER_BODY = 34 /' scripts/make_notebook.py && python3 scripts/make_notebook.py
E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && start=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s)-start ))s"
python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  if c['cell_type']!='code': continue
  for o in c['outputs']:
    if o['output_type']=='stream': t=''.join(o['text']); print(t[:600] if 'first one' in t else t[-1800:]); print('---')
    elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    elif 'image/png' in o.get('data',{}): open('$WS/../_viz_check_NGX.png' if False else '/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/41924b7b-d3aa-47d3-96e2-a7d39ff94c5a/scratchpad/viz.png','wb').write(base64.b64decode(o['data']['image/png']))
" 2>&1 | tail -60
```

### [36] TOOL RESULT — Bash · 2026-09-30 02:24:59 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb 27 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 186210 bytes to code_demo.ipynb\nruntime 102s\n  \"B5_plus_OPEN_home\": 0.746,\n  \"B5_plus_OPEN_home_clean\": 0.731,\n  \"n\": 22\n },\n \"COH1014\": {\n  \"B5\": 0.842,\n  \"B5_plus_NOVCHURN_raw\": 0.869,\n  \"B5_plus_NOVCHURN_exc\": 0.846,\n  \"B5_plus_NOVCHURN_cfg\": 0.85,\n  \"B5_plus_OPEN_home\": 0.853,\n  \"B5_plus_OPEN_home_clean\": 0.855,\n  \"n\": 22\n },\n \"COH1517\": {\n  \"B5\": 0.774,\n  \"B5_plus_NOVCHURN_raw\": 0.78,\n  \"B5_plus_NOVCHURN_exc\": 0.797,\n  \"B5_plus_NOVCHURN_cfg\": 0.753,\n  \"B5_plus_OPEN_home\": 0.805,\n  \"B5_plus_OPEN_home_clean\": 0.801,\n  \"n\": 22\n }\n}\n\n---\n100 examples; first one:\n{\n \"input\": \"{\\\"concept_id\\\": \\\"2778079797\\\", \\\"name\\\": \\\"Infratemporal fossa\\\", \\\"body\\\": \\\"DEV\\\", \\\"t0\\\": 2005, \\\"n_home_early\\\": 45, \\\"NOV_res__raw\\\": -0.91676, \\\"edge_persistence__raw\\\": 0.0, \\\"ego_density_W3__raw\\\": 0.785714, \\\"new_edge_rate__raw\\\": 0.074074, \\\"n_comm_W3__raw\\\": 1.0, \\\"participation__raw\\\": 0.0, \\\"NOVCHURN_raw\\\": -0.109903, \\\"OPEN_home\\\": -0.353592, \\\"NOV_res_rare10\\\": null, \\\"edge_persistence_rare10\\\": null, \\\"NOVCHURN_rare10\\\": null, \\\"NOV_res_rare5\\\": null, \\\"edge_persistence_rare5\\\": 0.0, \\\"NOVCHURN_rare5\\\": null, \\\"NOV_res_exc\\\": -0.0, \\\"edge\n---\n02:24:53|INFO   |method_out.json: 100 examples; verdict PARTLY_THIN\n\n---\n 0.020\nNOV_res_rare10             0.102  0.065    0.048    0.205   0.093        NaN\nedge_persistence__raw     -0.076 -0.086   -0.116   -0.112  -0.088      0.570\nedge_persistence_exc       0.006 -0.006   -0.013    0.001  -0.003      0.046\nedge_persistence_rare10   -0.010 -0.037   -0.055   -0.058  -0.030        NaN\nz_pers_cfg                -0.100 -0.122   -0.172   -0.066  -0.116      0.709\nexcess_pers_cfg           -0.077 -0.081   -0.115   -0.125  -0.089        NaN\nEP_chao                   -0.081 -0.105   -0.089   -0.099  -0.083        NaN\nedge_persistence_nullmean -0.109 -0.116   -0.143   -0.123  -0.120      0.707\nego_density_W3__raw       -0.052  0.006    0.030    0.018  -0.013      0.412\nz_dens_cfg                -0.087 -0.089   -0.127   -0.047  -0.091      0.698\nz_dens_k                  -0.052 -0.050   -0.083    0.042  -0.047      0.657\nOPEN_home                  0.109  0.070    0.074    0.091   0.085      0.485\nOPEN_home_clean            0.133  0.094    0.108    0.129   0.115      0.577\nOPEN_home_exc              0.072  0.035    0.041    0.070   0.052      0.486\n\nOut-of-DEV Spearman(prediction, O2r_m50): demo subset vs full run\n                        demo_rho                full_rho               \nbody                     COH1014 COH1517  OLDHO  COH1014 COH1517  OLDHO\nmodel                                                                  \nB5                         0.842   0.774  0.800    0.759   0.785  0.705\nB5_plus_NOVCHURN_cfg       0.850   0.753  0.799    0.761   0.786  0.707\nB5_plus_NOVCHURN_exc       0.846   0.797  0.756    0.759   0.785  0.705\nB5_plus_NOVCHURN_raw       0.869   0.780  0.815    0.762   0.789  0.710\nB5_plus_OPEN_home          0.853   0.805  0.746    0.761   0.787  0.707\nB5_plus_OPEN_home_clean    0.855   0.801  0.731    0.762   0.789  0.707\n\n---", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] ASSISTANT · 2026-09-30 02:25:01 UTC

```
Demo ρ now matches the full-run values (0.73–0.87 vs 0.71–0.79). Checking the figure:
```

### [38] TOOL CALL — Read · 2026-09-30 02:25:01 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/41924b7b-d3aa-47d3-96e2-a7d39ff94c5a/scratchpad/viz.png
```

### [39] TOOL RESULT — Read · 2026-09-30 02:25:01 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [40] ASSISTANT · 2026-09-30 02:25:17 UTC

```
Figure panel (b) needs cleaner colours: each body should get one hue, dark for the demo and light for the full run, with the legend moved off the bars.
```

### [41] TOOL CALL — Bash · 2026-09-30 02:25:17 UTC

```
Fix panel b styling and retest:
WS=/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z; cd $WS && python3 - <<'EOF'
p='scripts/make_notebook.py'
s=open(p).read()
old='''for j, body in enumerate(("OLDHO", "COH1014", "COH1517")):
    ax.bar(xs + (2 * j - 2.5) * w, [chk[body][m] if chk[body][m] is not None else np.nan for m in models], w,
           label=f"demo {body}", alpha=.9)
    ax.bar(xs + (2 * j - 1.5) * w, [full_pc[body][m] for m in models], w, label=f"full {body}", alpha=.45)'''
new='''for j, (body, cc) in enumerate(zip(("OLDHO", "COH1014", "COH1517"), ("tab:orange", "tab:green", "tab:red"))):
    ax.bar(xs + (2 * j - 2.5) * w, [chk[body][m] if chk[body][m] is not None else np.nan for m in models], w,
           label=f"demo {body}", color=cc, alpha=.95)
    ax.bar(xs + (2 * j - 1.5) * w, [full_pc[body][m] for m in models], w, label=f"full {body}", color=cc, alpha=.35,
           hatch="//", edgecolor="white")'''
assert old in s
s=s.replace(old,new)
s=s.replace('''ax.set_ylabel("out-of-DEV Spearman"); ax.set_title("(b) DEV-fitted OLS: demo subset vs full run"); ax.legend(fontsize=7, ncol=2)''',
 '''ax.set_ylim(0, 1.15); ax.set_ylabel("out-of-DEV Spearman"); ax.set_title("(b) DEV-fitted OLS: demo (solid) vs full run (hatched)")
ax.legend(fontsize=7, ncol=3, loc="upper center")''')
open(p,'w').write(s)
EOF
python3 scripts/make_notebook.py
E=/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-f03864fe3aed
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && start=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -3; echo "runtime $(( $(date +%s)-start ))s"
python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    elif 'image/png' in o.get('data',{}): open('/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/41924b7b-d3aa-47d3-96e2-a7d39ff94c5a/scratchpad/viz.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [42] TOOL RESULT — Bash · 2026-09-30 02:27:06 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/code_demo.ipynb 27 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 209050 bytes to code_demo.ipynb\nruntime 101s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Read · 2026-09-30 02:27:08 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/41924b7b-d3aa-47d3-96e2-a7d39ff94c5a/scratchpad/viz.png
```

### [44] TOOL RESULT — Read · 2026-09-30 02:27:10 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [45] ASSISTANT · 2026-09-30 02:27:14 UTC

```
The figure reads well now. Next: verification checks, then the README, manifest and struct output.
```

### [46] TOOL CALL — Bash · 2026-09-30 02:27:14 UTC

```
Verify URL, data file, workspace sizes:
grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-16/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la mini_demo_data.json; du -ah --max-depth=2 . | sort -h | tail -12
```

### [47] TOOL RESULT — Bash · 2026-09-30 02:27:14 UTC

```
{"stdout": "1\n1\n-rw-rw-rw- 1 aii-agent aii-agent 169820 Sep 30 02:21 mini_demo_data.json\n512\t./.aii\n512\t./.aii_claude_session.json\n3.0K\t./results/prediction_check.json\n4.5K\t./scripts/make_mini_demo_data.py\n22K\t./scripts/make_notebook.py\n154K\t./method_out.json\n166K\t./mini_demo_data.json\n205K\t./code_demo.ipynb\n510K\t./.repl_agent.ptylog\n980K\t./results\n1006K\t./scripts\n4.9M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] ASSISTANT · 2026-09-30 02:27:28 UTC

```
Nothing heavy is in the workspace, so the manifest has no entries. Writing the README, manifest and struct output:
```

### [49] TOOL CALL — Bash · 2026-09-30 02:27:28 UTC

````
Write manifest, README, and struct output:
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy (total < 5 MB, all text/JSON/notebook); no keep/delete decisions required.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: is research-topic churn real or small-sample noise? (experiment 16)

A Colab-ready notebook demo of `method.py` from the thin-sample confound-check experiment. The experiment asks whether the home-neighbourhood "churn/novelty" signal is real temporal partner turnover or an artefact of few papers per year. It compares raw indicators against noise-controlled variants: rarefaction, a permutation null, Chao correction and configuration nulls. **Verdict: `PARTLY_THIN`.** The association survives fixed-n rarefaction and degree normalisation. It vanishes against the within-concept year-permutation null. So it reflects a static dispersion of the home topic mix, not year-to-year churn.

The notebook runs the original `build_outputs()` code, split into cells with explanations between them. It uses a curated 100-concept subset:
- standardise the B5 covariates with the frozen EXP10 constants,
- fit the OLS models on DEV only (B5, and B5 plus each churn variant),
- compute the out-of-DEV Spearman,
- write `method_out.json`.

The upstream stage scripts need the multi-GB OpenAlex cache. The notebook reads their aggregate results (verdict, headline partial Spearman, reliability, power) from `mini_demo_data.json`.

## Layout
| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook: loads data from GitHub, with a fallback to the local copy. Runs in about 100 s, mostly package installs |
| `mini_demo_data.json` | one dataset `selection_concepts_table`: 100 concepts (34 DEV, 22 OLDHO, 22 COH1014, 22 COH1517), plus result-JSON fragments in `metadata` |
| `scripts/make_mini_demo_data.py` | builds `mini_demo_data.json` from the experiment-16 artifact (needs that artifact's data on the run volume) |
| `scripts/make_notebook.py` | generates `code_demo.ipynb` |
| `method_out.json`, `results/prediction_check.json` | outputs written by the last local test run of the notebook |

## How to run
Open `code_demo.ipynb` in Colab and run all cells. To run it locally:
```bash
uv venv --seed --python 3.12 .venv && uv pip install --python .venv/bin/python jupyter ipykernel
.venv/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
Config cell: `MAX_PER_BODY` is the number of concepts per body (demo maximum 34). `MIN_N_SPEARMAN = 20` is the original threshold. The original full run used all 7,748 concepts with a finite outcome.

## Restoring removed files
No files are marked for deletion (`.aii/manifest.yaml` has no entries). To regenerate the notebook outputs, re-run the notebook. To rebuild the data file, run `python3 scripts/make_mini_demo_data.py` (needs pandas and pyarrow, plus the experiment-16 artifact on the run volume). To rebuild the notebook, run `python3 scripts/make_notebook.py`.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
python3 -c "import json;print(json.load(open('.terminal_claude_agent_struct_out.json')))"
````

### [50] TOOL RESULT — Bash · 2026-09-30 02:27:30 UTC

```
{"stdout": "{'out_expected_files': {'notebook': 'code_demo.ipynb', 'mini_data_file': 'mini_demo_data.json'}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-30 02:27:38 UTC

```
I've built the demo notebook and its data file. The notebook runs cleanly from a fresh Python 3.12 environment matching Colab in about 100 s, well under the 600 s limit, and most of that time is package installs.

**What the notebook runs:** `method.py` is mainly a stage runner, and the real work is in `build_outputs()`. I split that function into cells with explanations between them and kept the code lines the same. It standardises the five baseline covariates (B5) with the frozen EXP10 constants and fits the prediction models on the DEV body only: B5 alone, and B5 plus each churn variant. It then checks those models on the three held-out bodies and writes `method_out.json`.

**What it can't run:** the 14 stage scripts, `concept_key_check()` and `exp12_crosscheck()` all need the multi-GB OpenAlex cache or other artifacts' files.
- Their summary results come from the data file instead: the verdict (`PARTLY_THIN`), P1–P3, the headline partial Spearman per body, reliability, size dependence and power.
- The two cross-checks are replaced by stubs that say they weren't run, and the notebook explains this.

**Changes to the original code:**
- The `results/*.json` reads come from the data file instead.
- `load_tables()` is a small stand-in that builds the same table from the demo rows.
- `jdump` and `_clean` are copied from `lib/common.py`.
- The hard-coded minimum of 20 concepts for reporting a Spearman is now a config value.

**Data file:** 100 concepts: 34 DEV and 22 in each held-out body. I picked concepts across the whole outcome range and shuffled them. My first version was sorted by outcome, so capping the rows kept only low-outcome concepts and gave misleadingly low correlations. On the held-out bodies, the demo correlations between prediction and outcome are 0.73–0.87, close to the full run's 0.71–0.79. With only 22 concepts per body they are noisy, and the notebook says so.

**Scaling:** the only real size setting is `MAX_PER_BODY`. It passed at the minimum of 21 per body and at 34, which uses all 100 demo rows; runtime was the same. The full run used all 7,748 concepts with a known outcome, and the config cell notes this.

**Other files:**
- `README.md` describes the layout and how to run it.
- `.aii/manifest.yaml` has no entries because nothing in the workspace is large (about 5 MB total).
- `.terminal_claude_agent_struct_out.json` is written.
- `scripts/` holds the two scripts that rebuild the data file and the notebook.

The GitHub raw URL won't work until the files are pushed, so for now the notebook falls back to the local copy.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
```
