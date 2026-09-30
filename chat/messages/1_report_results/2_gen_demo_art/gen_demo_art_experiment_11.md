# gen_demo_art_experiment_11 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_11` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-30 02:09:51 UTC

```
model: Claude Opus 5.5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-30 02:09:59 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/`:
GOOD: `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/file.py`, `/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/results/out.json`
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
id: art_UkIMstVveAFx
type: experiment
title: 'Cheng''s consistency: size effect, not reach'
summary: >-
  Rebuilds Cheng et al. (2023, ASR) 'ideational consistency' (cosine of a concept's topic co-usage vector t-1 -> t), a PMI
  embeddedness analogue and co-author tie density for 12,499 EXP5 frame concepts (t0..t0+10) and the 1,443-concept 2015-17
  EXP10 cohort, from cached grounded OpenAlex rows ($0, 0 credits). Spec and verdict rules sealed before fitting (git commit
  1). TEST A (Cheng design, 105,839 concept-years): NB twin reproduces Cheng almost exactly (b=0.428, +53.5%/SD vs Cheng .43/+53%);
  PPML +83% [+71,+97]; adding log V(t) leaves +1.3% [+0.5,+2.1]; A2/A1 ratio 0.021 [0.009,0.035] (500-draw concept-cluster
  bootstrap) -> SIZE-DOMINATED; concept FE +1.4%. TEST B (early trait, psp | B5 + dummies, 2,000 draws): raw Spearman with
  V(t0+3) +0.256 [0.239,0.274] but psp with rarefied cross-field reach O2r_m50 -0.069 [-0.093,-0.047] (DL over 5 groups -0.079,
  I2=0, 5/5 negative), O2r_resid -0.077; replicated on 2015-17 cohort -0.111 [-0.197,-0.030], n=615 (R3 rung -0.098). Depth
  outcomes null (O1c -0.000, O1b -0.004, O3 -0.001); paired diff O1c-O2r_m50 +0.035 [0.004,0.066] (DL CI incl. 0). Frozen
  verdict: REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT (the split is null-depth
  vs negative-reach). TEST C (within concept, ci+year FE): consistent years followed by slightly MORE off-home entries (b=+0.025,
  boot CI [0.004,0.048]) -> P6 fails; reach penalty is a between-concept trait. TEST D: no Palla size x consistency interaction.
  TEST E: ALL-papers build more negative for reach (diff -0.032). Identity: Spearman 0.77 with Exp11 Jaccard persistence,
  0.34 with log early volume. Adding CONS to a DEV-fitted B5 rank model does not improve held-out prediction (delta ~0). All
  bodies are selection data (outcomes previously read), not confirmation. Independent re-derivation (rederive.py: statsmodels
  GLM full panel, QR psp from raw inputs) matches all headline numbers except C1 (not re-derived); placebos fail. Key files:
  results/cheng_verdict.json, cheng_panel_models.json, cheng_static.json, panel_C.json, palla.json, coupling.json, identity_check.json,
  rederive.json, audit.json; reconciling_cheng.md (paper paragraph with JSON key paths); data/cheng_features.parquet, cheng_static.parquet;
  figures/fig_cheng_ladder, fig_reach_depth_forest, fig_palla; method_out.json (per-concept O2r_m50 with predict_B5 vs predict_B5_plus_CONS).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-30 02:10:03 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-30 02:10:03 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-30 02:10:03 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-30 02:10:03 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-30 02:10:05 UTC

```
List artifact workspace files:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; ls -la $W; ls -la $W/data $W/results 2>/dev/null; wc -l $W/method.py; ls -la /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx
```

### [8] TOOL RESULT — Bash · 2026-09-30 02:10:07 UTC

```
{"stdout": "total 41904\ndrwxrwxrwx 10 aii-agent aii-agent  2006256 Sep 29 09:00 .\ndrwxrwxrwx  7 aii-agent aii-agent  3000249 Sep 29 05:17 ..\ndrwxrwxrwx  2 aii-agent aii-agent    62500 Sep 29 06:21 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 29 05:18 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent     9750 Sep 29 06:21 .aii_worker_result.json\ndrwxrwxrwx  8 aii-agent aii-agent  2001902 Sep 29 06:17 .git\n-rw-rw-rw-  1 aii-agent aii-agent       85 Sep 29 06:12 .gitignore\n-rw-rw-rw-  1 aii-agent aii-agent   576603 Sep 29 06:21 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     2987 Sep 29 06:17 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    13617 Sep 29 06:17 README.md\n-rw-rw-rw-  1 aii-agent aii-agent     6994 Sep 29 05:45 audit.py\ndrwxrwxrwx  2 aii-agent aii-agent  2001535 Sep 29 05:40 data\ndrwxrwxrwx  2 aii-agent aii-agent  1027933 Sep 29 06:08 figures\n-rw-rw-rw-  1 aii-agent aii-agent 14901382 Sep 29 06:14 full_method_out.json\ndrwxrwxrwx  2 aii-agent aii-agent  1016396 Sep 29 09:00 lib\ndrwxrwxrwx  3 aii-agent aii-agent  1004277 Sep 29 06:17 logs\n-rw-rw-rw-  1 aii-agent aii-agent     3761 Sep 29 06:02 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 13186742 Sep 29 06:09 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     6964 Sep 29 06:14 mini_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     7714 Sep 29 05:29 prereg.md\n-rw-rw-rw-  1 aii-agent aii-agent     6964 Sep 29 06:14 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     2023 Sep 29 06:14 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent       22 Sep 29 05:32 pytest.ini\n-rw-rw-rw-  1 aii-agent aii-agent     4750 Sep 29 06:09 reconciling_cheng.md\n-rw-rw-rw-  1 aii-agent aii-agent     9126 Sep 29 06:15 rederive.py\n-rw-rw-rw-  1 aii-agent aii-agent     9081 Sep 29 06:17 reproducibility.md\n-rw-rw-rw-  1 aii-agent aii-agent     1305 Sep 29 06:14 requirements.lock.txt\n-rwxrwxrwx  1 aii-agent aii-agent      343 Sep 29 06:17 restore.sh\ndrwxrwxrwx  2 aii-agent aii-agent  1028115 Sep 29 06:16 results\ndrwxrwxrwx  2 aii-agent aii-agent  1001230 Sep 29 09:00 tests\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/data:\ntotal 19638\ndrwxrwxrwx  2 aii-agent aii-agent 2001535 Sep 29 05:40 .\ndrwxrwxrwx 10 aii-agent aii-agent 2006256 Sep 29 09:00 ..\n-rw-rw-rw-  1 aii-agent aii-agent   18147 Sep 29 05:36 V_cohort.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 1386293 Sep 29 05:35 V_exp5.parquet\n-rw-rw-rw-  1 aii-agent aii-agent    8128 Sep 29 05:57 boot_ratio_ALL_joint.npy\n-rw-rw-rw-  1 aii-agent aii-agent    8128 Sep 29 05:47 boot_ratio_HOME_joint.npy\n-rw-rw-rw-  1 aii-agent aii-agent 9530698 Sep 29 05:36 cheng_features.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 1380894 Sep 29 05:36 cheng_static.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 1651491 Sep 29 05:36 identity_table.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 2115491 Sep 29 06:02 static_analysis_table.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/results:\ntotal 3249\ndrwxrwxrwx  2 aii-agent aii-agent 1028115 Sep 29 06:16 .\ndrwxrwxrwx 10 aii-agent aii-agent 2006256 Sep 29 09:00 ..\n-rw-rw-rw-  1 aii-agent aii-agent    1364 Sep 29 06:07 audit.json\n-rw-rw-rw-  1 aii-agent aii-agent   66186 Sep 29 06:02 cheng_panel_models.json\n-rw-rw-rw-  1 aii-agent aii-agent  152913 Sep 29 06:03 cheng_static.json\n-rw-rw-rw-  1 aii-agent aii-agent    3521 Sep 29 06:09 cheng_verdict.json\n-rw-rw-rw-  1 aii-agent aii-agent    6403 Sep 29 06:04 coupling.json\n-rw-rw-rw-  1 aii-agent aii-agent    3514 Sep 29 06:07 deviations.json\n-rw-rw-rw-  1 aii-agent aii-agent    6396 Sep 29 05:30 frozen_spec.json\n-rw-rw-rw-  1 aii-agent aii-agent    3347 Sep 29 06:09 headline_numbers.json\n-rw-rw-rw-  1 aii-agent aii-agent    7653 Sep 29 05:36 identity_check.json\n-rw-rw-rw-  1 aii-agent aii-agent   10505 Sep 29 06:03 palla.json\n-rw-rw-rw-  1 aii-agent aii-agent   13181 Sep 29 06:06 panel_C.json\n-rw-rw-rw-  1 aii-agent aii-agent    1616 Sep 29 06:09 predictive_comparison.json\n-rw-rw-rw-  1 aii-agent aii-agent    5032 Sep 29 06:03 provenance.json\n-rw-rw-rw-  1 aii-agent aii-agent    2180 Sep 29 06:16 rederive.json\n-rw-rw-rw-  1 aii-agent aii-agent    1411 Sep 29 05:36 s1_build.json\n-rw-rw-rw-  1 aii-agent aii-agent     748 Sep 29 05:33 s1_build_sample50.json\n-rw-rw-rw-  1 aii-agent aii-agent     804 Sep 29 05:33 s1_build_sample500.json\n-rw-rw-rw-  1 aii-agent aii-agent    1131 Sep 29 06:05 unit_tests.json\n89 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method.py\ntotal 1989\ndrwxrwxrwx 3 aii-agent aii-agent 1002460 Sep 30 02:09 .\ndrwxrwxrwx 4 aii-agent aii-agent 1007420 Sep 30 02:09 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 02:09 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 02:09 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   25333 Sep 30 02:10 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-30 02:10:09 UTC

```
Read method.py, lib listing, preview:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/method.py; echo ----; ls -la $W/lib $W/tests; head -c 3000 $W/preview_method_out.json; echo; cat $W/pyproject.toml
```

### [10] TOOL RESULT — Bash · 2026-09-30 02:10:09 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator: Cheng et al. (2023) ideational consistency -- replication, size control and the reach-vs-depth\nreversal on this run's selection bodies (EXP5 frame + EXP10 2015-17 cohort). Cache only, CPU only, $0 LLM.\n\nSteps (run all in order, or one with --only):\n  S0  frozen spec + seal (before any model)             lib/s0_spec.py\n  S1  build Cheng measures (cheng_features / static)     lib/build.py         [--sample N for staged scale-up]\n  S2  construct-identity check                           lib/identity.py\n  S3  test A: Cheng replication panel (A1/A1-NB/A2/A3)   lib/panel_cheng.py\n  S3NB  re-fit A1-NB only (patches cheng_panel_models.json)  lib/panel_cheng.py\n  S4  test B: static early trait, reach vs depth         lib/static_cheng.py\n  S5  test C: within-panel reach vs depth                lib/panel_cheng.py\n  S6  test D: Palla size x turnover                      lib/static_cheng.py\n  S7  test E: HOME vs ALL coupling                       lib/static_cheng.py\n  S8  verdict, figures, method_out.json, write-up        lib/outputs.py\nUsage: uv run method.py [--only S3] [--sample 500] [--quick]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport sys\n\nfor _v in (\"OMP_NUM_THREADS\", \"OPENBLAS_NUM_THREADS\", \"MKL_NUM_THREADS\"):   # one BLAS thread per process: the\n    os.environ.setdefault(_v, \"1\")                                         # steps parallelise across processes\nimport time\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nfrom common import set_limits, setup_logger  # noqa: E402\n\nSTEPS = [\"S0\", \"S1\", \"S2\", \"S3\", \"S4\", \"S5\", \"S6\", \"S7\", \"S8\"]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--only\", type=str, default=\"\")\n    ap.add_argument(\"--sample\", type=int, default=0, help=\"S1: number of EXP5 concepts (staged scale-up)\")\n    ap.add_argument(\"--quick\", action=\"store_true\", help=\"S3-S7: 10%% of concepts, few bootstrap draws (timing)\")\n    ap.add_argument(\"--workers\", type=int, default=0)\n    args = ap.parse_args()\n    logger = setup_logger(\"method\")\n    set_limits(26.0)\n    steps = [s.strip() for s in args.only.split(\",\")] if args.only else STEPS\n\n    @logger.catch(reraise=True)\n    def _run() -> None:\n        for s in steps:\n            t = time.time()\n            logger.info(f\"===== {s} start\")\n            if s == \"S0\":\n                import s0_spec\n                s0_spec.run(logger)\n            elif s == \"S1\":\n                import build\n                build.run(logger, sample=args.sample, workers=args.workers)\n            elif s == \"S2\":\n                import identity\n                identity.run(logger)\n            elif s == \"S3\":\n                import panel_cheng\n                panel_cheng.run_A(logger, quick=args.quick, workers=args.workers)\n            elif s == \"S3NB\":\n                import panel_cheng\n                panel_cheng.refit_nb(logger)\n            elif s == \"S4\":\n                import static_cheng\n                static_cheng.run_B(logger, quick=args.quick)\n            elif s == \"S5\":\n                import panel_cheng\n                panel_cheng.run_C(logger, quick=args.quick, workers=args.workers)\n            elif s == \"S6\":\n                import static_cheng\n                static_cheng.run_D(logger, quick=args.quick)\n            elif s == \"S7\":\n                import static_cheng\n                static_cheng.run_E(logger, quick=args.quick)\n            elif s == \"S8\":\n                import outputs\n                outputs.run(logger)\n            else:\n                raise ValueError(f\"unknown step {s}\")\n            logger.info(f\"===== {s} done in {(time.time() - t) / 60:.1f} min\")\n\n    _run()\n\n\nif __name__ == \"__main__\":\n    main()\n----\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib:\ntotal 3120\ndrwxrwxrwx  2 aii-agent aii-agent 1016396 Sep 29 09:00 .\ndrwxrwxrwx 10 aii-agent aii-agent 2006256 Sep 29 09:00 ..\n-rw-rw-rw-  1 aii-agent aii-agent   14185 Sep 29 05:31 build.py\n-rw-rw-rw-  1 aii-agent aii-agent   10060 Sep 29 05:31 cheng.py\n-rw-rw-rw-  1 aii-agent aii-agent    5216 Sep 29 05:27 common.py\n-rw-rw-rw-  1 aii-agent aii-agent   12721 Sep 29 05:26 ego.py\n-rw-rw-rw-  1 aii-agent aii-agent    1945 Sep 29 05:26 ego_ctx.py\n-rw-rw-rw-  1 aii-agent aii-agent    9852 Sep 29 05:26 ego_yearly.py\n-rw-rw-rw-  1 aii-agent aii-agent    8949 Sep 29 05:26 fe_stats.py\n-rw-rw-rw-  1 aii-agent aii-agent    5212 Sep 29 05:35 identity.py\n-rw-rw-rw-  1 aii-agent aii-agent    9137 Sep 29 05:34 ladder.py\n-rw-rw-rw-  1 aii-agent aii-agent   20838 Sep 29 06:09 outputs.py\n-rw-rw-rw-  1 aii-agent aii-agent   18372 Sep 29 06:02 panel_cheng.py\n-rw-rw-rw-  1 aii-agent aii-agent    4457 Sep 29 05:26 panel_m.py\n-rw-rw-rw-  1 aii-agent aii-agent    1777 Sep 29 06:03 provenance.py\n-rw-rw-rw-  1 aii-agent aii-agent    8080 Sep 29 05:26 rq1stats.py\n-rw-rw-rw-  1 aii-agent aii-agent    7569 Sep 29 05:29 s0_spec.py\n-rw-rw-rw-  1 aii-agent aii-agent   20877 Sep 29 05:59 static_cheng.py\n-rw-rw-rw-  1 aii-agent aii-agent    8655 Sep 29 05:26 stats_core.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/tests:\ntotal 2951\ndrwxrwxrwx  2 aii-agent aii-agent 1001230 Sep 29 09:00 .\ndrwxrwxrwx 10 aii-agent aii-agent 2006256 Sep 29 09:00 ..\n-rw-rw-rw-  1 aii-agent aii-agent    1779 Sep 29 06:14 exp_gen_sol_out.schema.json\n-rw-rw-rw-  1 aii-agent aii-agent    5186 Sep 29 05:32 test_measures.py\n-rw-rw-rw-  1 aii-agent aii-agent    2064 Sep 29 06:14 test_output.py\n-rw-rw-rw-  1 aii-agent aii-agent    3572 Sep 29 05:43 test_stats.py\n{\n  \"metadata\": {\n    \"method_name\": \"Cheng ideational consistency (count-weighted topic co-usage cosine) added to the B5 baseline\",\n    \"baseline\": \"predict_B5 = rank-OLS on B5 fitted on DEV\",\n    \"method\": \"predict_B5_plus_CONS = same + CONS_early_home, fitted on DEV, applied frozen\",\n    \"output\": \"O2r_m50 (rarefied venue-field richness at t0+6..t0+8); 'NA' where undefined\",\n    \"label\": \"selection data, not confirmation\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"EXP5_frame\",\n      \"examples\": [\n        {\n          \"input\": \"Complete intersection | ci=3 | t0=2012 | group=MATHDEC | body=COHORT_2010_14\",\n          \"output\": \"2.9608\",\n          \"predict_B5\": \"3.8994\",\n          \"predict_B5_plus_CONS\": \"3.8302\",\n          \"metadata_ci\": 3,\n          \"metadata_t0\": 2012,\n          \"metadata_group\": \"MATHDEC\",\n          \"metadata_group5\": \"MATHDEC\",\n          \"metadata_body\": \"COHORT_2010_14\",\n          \"metadata_CONS_early_home\": 0.6306984195836987,\n          \"metadata_CONS_early_all\": 0.6953313198436348,\n          \"metadata_CONS_r_early_home\": 0.6900652119564956,\n          \"metadata_EMB_early_home_analogue\": 3.2053415177599422,\n          \"metadata_SOC_early_home\": 0.008658008658008658,\n          \"metadata_V_t0p2\": 29.0,\n          \"metadata_V_t0p3\": 26.0,\n          \"metadata_CONS_imputed_dev_median\": false,\n          \"metadata_label\": \"selection data, not confirmation\",\n          \"metadata_O2r_m50\": 2.96078431372549,\n          \"metadata_O2r_resid\": -1.4819808004866881,\n          \"metadata_O1c\": -0.21292199724267125,\n          \"metadata_O1b\": 0.0,\n          \"metadata_O3\": 0.0\n        },\n        {\n          \"input\": \"Torque converter | ci=4 | t0=2004 | group=Eng | body=DEV\",\n          \"output\": \"2.8987\",\n          \"predict_B5\": \"2.7238\",\n          \"predict_B5_plus_CONS\": \"2.6578\",\n          \"metadata_ci\": 4,\n          \"metadata_t0\": 2004,\n          \"metadata_group\": \"Eng\",\n          \"metadata_group5\": \"CS+Eng\",\n          \"metadata_body\": \"DEV\",\n          \"metadata_CONS_early_home\": 0.6011880046495223,\n          \"metadata_CONS_early_all\": 0.5838037184897182,\n          \"metadata_CONS_r_early_home\": 0.7068124284415241,\n          \"metadata_EMB_early_home_analogue\": 1.5183806686663486,\n          \"metadata_SOC_early_home\": 0.0,\n          \"metadata_V_t0p2\": 17.0,\n          \"metadata_V_t0p3\": 19.0,\n          \"metadata_CONS_imputed_dev_median\": false,\n          \"metadata_label\": \"selection data, not confirmation\",\n          \"metadata_O2r_m50\": 2.8987341772151547,\n          \"metadata_O2r_resid\": -1.4979931361786871,\n          \"metadata_O1c\": 0.34740130715340367,\n          \"metadata_O1b\": 1.0,\n          \"metadata_O3\": 0.0\n        },\n        {\n          \"input\": \"Early adopter | ci=16 | t0=2011 | group=SOC | body=COHORT_2010_14\",\n          \"output\": \"9.8824\",\n          \"predict_B5\": \"6.8889\",\n          \"predict_B5_plus_CONS\": \"6.7665\",\n          \"metadata_ci\": 16,\n          \"metadata_t0\": 2011,\n          \"metadata_group\": \"SOC\",\n          \"metadata_group5\": \"\n[project]\nname = \"cheng-reach-depth\"\nversion = \"0.1.0\"\ndescription = \"Cheng et al. 2023 ideational consistency: replication, size control and reach-vs-depth reversal on selection bodies\"\nrequires-python = \"==3.12.*\"\n# every package installed in .venv, pinned exactly (uv pip freeze; identical to requirements.lock.txt)\ndependencies = [\n  \"asttokens==3.0.2\",\n  \"attrs==26.1.0\",\n  \"babel==2.18.0\",\n  \"cffi==2.1.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"executing==2.2.1\",\n  \"faicons==0.2.2\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"great-tables==1.0.0\",\n  \"htmltools==0.7.0\",\n  \"igraph==1.0.0\",\n  \"importlib-metadata==9.0.1\",\n  \"importlib-resources==7.1.0\",\n  \"iniconfig==2.3.0\",\n  \"interface-meta==2.0.1\",\n  \"ipython==9.17.1\",\n  \"ipython-pygments-lexers==1.1.1\",\n  \"jedi==0.20.0\",\n  \"joblib==1.6.0\",\n  \"jsonschema==4.26.0\",\n  \"jsonschema-specifications==2025.9.1\",\n  \"kiwisolver==1.5.1\",\n  \"leidenalg==0.12.0\",\n  \"loguru==0.7.3\",\n  \"lxml==6.1.3\",\n  \"maketables==0.1.8\",\n  \"matplotlib==3.11.2\",\n  \"matplotlib-inline==0.2.2\",\n  \"multimark==0.3.2\",\n  \"narwhals==2.26.0\",\n  \"networkx==3.7\",\n  \"nokap==0.1.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==2.3.3\",\n  \"parso==0.8.7\",\n  \"patsy==1.0.3\",\n  \"pexpect==4.9.0\",\n  \"pillow==12.3.0\",\n  \"pluggy==1.6.0\",\n  \"prompt-toolkit==3.0.53\",\n  \"psutil==7.2.2\",\n  \"ptyprocess==0.7.0\",\n  \"pure-eval==0.2.4\",\n  \"pyarrow==25.0.1\",\n  \"pycparser==3.0\",\n  \"pyfixest==0.60.0\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"python-docx==1.2.0\",\n  \"pytz==2026.4\",\n  \"pyyaml==6.0.3\",\n  \"referencing==0.37.0\",\n  \"rpds-py==2026.6.3\",\n  \"scipy==1.18.1\",\n  \"seaborn==0.13.2\",\n  \"six==1.17.0\",\n  \"snowballstemmer==3.1.1\",\n  \"stack-data==0.6.3\",\n  \"statsmodels==0.15.0\",\n  \"tabulate==0.10.0\",\n  \"texttable==1.7.0\",\n  \"tqdm==4.70.1\",\n  \"traitlets==5.16.1\",\n  \"typing-extensions==4.16.0\",\n  \"tzdata==2026.4\",\n  \"wcwidth==0.9.1\",\n  \"websockets==17.1\",\n  \"wrapt==2.5.0\",\n  \"zipp==4.1.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-30 02:10:13 UTC

```
Read cheng.py, common.py, README:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/lib/cheng.py $W/lib/common.py; cat $W/README.md | head -120
```

### [12] TOOL RESULT — Bash · 2026-09-30 02:10:13 UTC

```
{"stdout": "\"\"\"Cheng et al. (2023, ASR 88:522-561) resonance measures rebuilt on OpenAlex topic co-usage (frozen in S0).\n\nFor concept c, paper set P (HOME = grounded papers whose venue field is in the frozen home set; ALL = every grounded\npaper) and calendar year t:\n  v_t[k]   = # year-t papers of c in P tagged with topic k, k not in SELF(c)       (neighbour co-usage vector)\n  CONS(t)  = cosine(v_{t-1}, v_t)                                  defined iff both years have ... [truncated, 25675 chars total]
```

### [13] TOOL CALL — Bash · 2026-09-30 02:10:17 UTC

```
Read panel_cheng.py:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/lib/panel_cheng.py
```

### [14] TOOL RESULT — Bash · 2026-09-30 02:10:17 UTC

```
{"stdout": "\"\"\"S3 (test A, Cheng replication panel) and S5 (test C, within-panel reach vs depth).\n\nTest A: EXP5 concept-years t0+1 <= t <= min(t0+10, 2021) with finite CONS_b(t) (b = HOME / ALL).\n  A1    fepois V(t+1) ~ zCONS + zEMB + zSOC | age + year          (Cheng's spec; CRV1 by concept)\n  A1c   fepois V(t+1) ~ zCONS | age + year                        (CONS-only variant, all CONS rows)\n  A1-NB statsmodels NB2 with age + year dummies (cluster-robust by concept)\n  A2    A1 + log1p V(t);  A3  A2 | ci + year\n  RATIO b_A2 / b_A1 on CONS, 500-draw concept-cluster bootstrap, same draws for A1 and A2 (numpy Poisson IRLS with\n        age/year dummies, validated against pyfixest on the point estimate)\nTest C: Exp11 yearly_panel estimation sample (at_risk_next > 0, deg >= 2), finite CONS_home(t).\n  C1 fepois entries(t+1) ~ zCONS_home(t) + log1p_home + log1p_all + log1p_deg + log_at_risk | ci + year\n  C2 feols dHomeShare(t+1) ~ same | ci + year\n  500-draw concept-cluster bootstrap (duplicated concepts relabelled as new FE units).\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport multiprocessing as mp\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import (DATA, EXP5, EXP11, GROUP5, GROUPS5, N_BOOT_PANEL, RES, SEED, SELECTION_LABEL, add_deviation,\n                    body_of_split, home_codes, jdump, n_workers)\nfrom rq1stats import dersimonian_laird\n\nXS_JOINT = [\"zCONS\", \"zEMB\", \"zSOC\"]\n\n\n# ----------------------------------------------------------------------------- data\ndef panel_A(build: str) -> pd.DataFrame:\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\", usecols=[\"ci\", \"t0\", \"group\", \"split\"])\n    fr[\"body\"] = fr.split.map(body_of_split)\n    fr[\"group5\"] = fr.group.map(GROUP5)\n    f = pd.read_parquet(DATA / \"cheng_features.parquet\")\n    f = f[(f.body_src == \"EXP5\") & (f.build == build)][[\"ci\", \"year\", \"CONS\", \"EMB\", \"SOC\", \"n_papers\", \"n_topics\"]]\n    V = pd.read_parquet(DATA / \"V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    d = f.merge(fr, on=\"ci\")\n    d = d[(d.year >= d.t0 + 1) & (d.year <= np.minimum(d.t0 + 10, 2021))]\n    d = d.merge(V, on=[\"ci\", \"year\"], how=\"left\").merge(\n        V.assign(year=V.year - 1).rename(columns={\"V\": \"V_next\"}), on=[\"ci\", \"year\"], how=\"left\")\n    d = d[np.isfinite(d.CONS)].copy()\n    d[\"age\"] = d.year - d.t0\n    d[\"logV\"] = np.log1p(d.V)\n    return d.reset_index(drop=True)\n\n\ndef zcols(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:\n    d = d.copy()\n    for c in cols:\n        v = d[c].to_numpy(float)\n        d[\"z\" + c] = (v - np.nanmean(v)) / np.nanstd(v)\n    return d\n\n\n# ----------------------------------------------------------------------------- numpy Poisson IRLS (dummies FE)\ndef dummy_design(d: pd.DataFrame, xs: list[str], fe: list[str]) -> tuple[np.ndarray, list[str]]:\n    cols = [np.ones(len(d))]\n    names = [\"_const\"]\n    for c in xs:\n        cols.append(d[c].to_numpy(float))\n        names.append(c)\n    for f in fe:\n        v = d[f].to_numpy()\n        for u in np.unique(v)[1:]:\n            cols.append((v == u).astype(float))\n            names.append(f\"{f}={u}\")\n    return np.column_stack(cols), names\n\n\ndef poisson_irls(X: np.ndarray, y: np.ndarray, iters: int = 100, tol: float = 1e-10) -> np.ndarray:\n    mu = y.mean() + 0.1\n    b = np.zeros(X.shape[1])\n    b[0] = math.log(mu)\n    eta = X @ b\n    for _ in range(iters):\n        mu = np.exp(np.clip(eta, -30, 30))\n        z = eta + (y - mu) / mu\n        XtW = X.T * mu\n        H = XtW @ X\n        try:\n            bn = np.linalg.solve(H, XtW @ z)\n        except np.linalg.LinAlgError:\n            bn = np.linalg.lstsq(H, XtW @ z, rcond=None)[0]\n        if np.max(np.abs(bn - b)) < tol:\n            b = bn\n            break\n        b = bn\n        eta = X @ b\n    return b\n\n\ndef _boot_ratio_worker(args) -> list[tuple[float, float]]:\n    X1, X2, y, cl_idx, seeds = args\n    out = []\n    for s in seeds:\n        rng = np.random.default_rng(s)\n        pick = rng.integers(0, len(cl_idx), len(cl_idx))\n        rows = np.concatenate([cl_idx[p] for p in pick])\n        b1 = poisson_irls(X1[rows], y[rows])[1]\n        b2 = poisson_irls(X2[rows], y[rows])[1]\n        out.append((b1, b2))\n    return out\n\n\ndef cluster_index(ci: np.ndarray) -> list[np.ndarray]:\n    order = np.argsort(ci, kind=\"stable\")\n    u, start = np.unique(ci[order], return_index=True)\n    return np.split(order, start[1:])\n\n\ndef boot_ratio(d: pd.DataFrame, xs: list[str], n_boot: int, seed: int, workers: int) -> dict:\n    \"\"\"Cluster bootstrap of b_A1 and b_A2 on the first regressor (zCONS), same draws.\"\"\"\n    X1, _ = dummy_design(d, xs, [\"age\", \"year\"])\n    X2, _ = dummy_design(d, xs + [\"logV\"], [\"age\", \"year\"])\n    y = d.V_next.to_numpy(float)\n    cl = cluster_index(d.ci.to_numpy())\n    b1p, b2p = poisson_irls(X1, y)[1], poisson_irls(X2, y)[1]\n    seeds = [seed + k for k in range(n_boot)]\n    parts = [seeds[i::workers] for i in range(workers)]\n    res = []\n    if workers > 1:\n        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex:\n            for r in ex.map(_boot_ratio_worker, [(X1, X2, y, cl, p) for p in parts]):\n                res.extend(r)\n    else:\n        res = _boot_ratio_worker((X1, X2, y, cl, seeds))\n    B = np.array(res)\n    ratio = B[:, 1] / B[:, 0]\n    pr = b2p / b1p\n    return {\"b_A1_irls\": b1p, \"b_A2_irls\": b2p, \"ratio\": pr,\n            \"ratio_ci\": np.percentile(ratio, [2.5, 97.5]).tolist(), \"ratio_boot_median\": float(np.median(ratio)),\n            \"b_A1_ci_boot\": np.percentile(B[:, 0], [2.5, 97.5]).tolist(),\n            \"b_A2_ci_boot\": np.percentile(B[:, 1], [2.5, 97.5]).tolist(),\n            \"p_one_ratio_lt_0.5\": float((np.sum(ratio >= 0.5) + 1) / (len(ratio) + 1)),\n            \"p_one_A1_gt_0\": float((np.sum(B[:, 0] <= 0) + 1) / (len(B) + 1)),\n            \"n_boot\": int(len(B)), \"resampling_unit\": \"concept (cluster bootstrap)\", \"boot_b\": B}\n\n\n# ----------------------------------------------------------------------------- pyfixest wrappers\ndef fepois(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:\n    import pyfixest as pf\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        fit = pf.fepois(f\"{y} ~ {' + '.join(xs)} | {fe}\", data=d, vcov={\"CRV1\": \"ci\"})\n    return summarize(fit, xs, d)\n\n\ndef feols(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:\n    import pyfixest as pf\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        fit = pf.feols(f\"{y} ~ {' + '.join(xs)} | {fe}\", data=d, vcov={\"CRV1\": \"ci\"})\n    return summarize(fit, xs, d)\n\n\ndef summarize(fit, xs: list[str], d: pd.DataFrame) -> dict:\n    co, se, pv = fit.coef(), fit.se(), fit.pvalue()\n    ci = fit.confint()\n    out = {\"n_rows\": int(fit._N), \"n_concepts\": int(d.ci.nunique()), \"coef\": {}}\n    for x in xs:\n        if x not in co.index:\n            continue\n        b = float(co[x])\n        out[\"coef\"][x] = {\"b\": b, \"se\": float(se[x]), \"ci\": [float(ci.loc[x].iloc[0]), float(ci.loc[x].iloc[1])],\n                          \"p\": float(pv[x]), \"pct_per_sd\": math.exp(b) - 1,\n                          \"pct_ci\": [math.exp(float(ci.loc[x].iloc[0])) - 1, math.exp(float(ci.loc[x].iloc[1])) - 1]}\n    return out\n\n\ndef nb_fit(d: pd.DataFrame, xs: list[str]) -> dict:\n    import statsmodels.api as sm\n    X, names = dummy_design(d, xs, [\"age\", \"year\"])\n    y = d.V_next.to_numpy(float)\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        m = sm.NegativeBinomial(y, X, loglike_method=\"nb2\")\n        try:\n            r = m.fit(disp=0, maxiter=300, method=\"bfgs\", cov_type=\"cluster\", cov_kwds={\"groups\": d.ci.to_numpy()})\n            how = \"bfgs\"\n        except np.linalg.LinAlgError:\n            # retry: Newton from the Poisson IRLS solution and alpha = 0.5\n            sp0 = np.r_[poisson_irls(X, y), 0.5]\n            r = m.fit(start_params=sp0, disp=0, maxiter=100, method=\"newton\", cov_type=\"cluster\",\n                      cov_kwds={\"groups\": d.ci.to_numpy()})\n            how = \"newton (retry after singular bfgs)\"\n    out = {\"n_rows\": int(len(y)), \"alpha\": float(r.params[-1]), \"converged\": bool(r.mle_retvals.get(\"converged\", True)),\n           \"optimizer\": how, \"coef\": {}}\n    for i, nm in enumerate(names):\n        if nm in xs:\n            b, s = float(r.params[i]), float(r.bse[i])\n            out[\"coef\"][nm] = {\"b\": b, \"se\": s, \"ci\": [b - 1.96 * s, b + 1.96 * s], \"pct_per_sd\": math.exp(b) - 1,\n                               \"p\": float(2 * stats.norm.sf(abs(b / s)))}\n    return out\n\n\n# ----------------------------------------------------------------------------- test A\ndef fit_A_set(d: pd.DataFrame, xs: list[str], with_A3: bool = True, with_nb: bool = False) -> dict:\n    out = {\"A1\": fepois(d, \"V_next\", xs, \"age + year\"),\n           \"A2\": fepois(d, \"V_next\", xs + [\"logV\"], \"age + year\")}\n    if with_A3:\n        out[\"A3\"] = fepois(d, \"V_next\", xs + [\"logV\"], \"ci + year\")\n    if with_nb:\n        try:\n            out[\"A1_NB\"] = nb_fit(d, xs)\n        except (ValueError, np.linalg.LinAlgError) as e:\n            out[\"A1_NB\"] = {\"error\": repr(e)[:300]}\n    b1 = out[\"A1\"][\"coef\"].get(\"zCONS\", {}).get(\"b\", np.nan)\n    b2 = out[\"A2\"][\"coef\"].get(\"zCONS\", {}).get(\"b\", np.nan)\n    out[\"ratio_point\"] = b2 / b1 if b1 else float(\"nan\")\n    return out\n\n\ndef run_A(logger, quick: bool = False, workers: int = 0) -> dict:\n    W = workers or n_workers()\n    nb = 60 if quick else N_BOOT_PANEL\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_boot\": nb,\n           \"spec\": \"PPML (pyfixest fepois); CRV1 by concept; X standardised over the rows of each model\",\n           \"EMB_note\": \"EMB is an ANALOGUE of Cheng's word2vec embeddedness (backbone PMI), not the same measure\",\n           \"builds\": {}}\n    for build in [\"HOME\", \"ALL\"]:\n        t = time.time()\n        d0 = panel_A(build)\n        if quick:\n            keep = d0.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)\n            d0 = d0[d0.ci.isin(keep)]\n        d0 = d0[np.isfinite(d0.V_next)]\n        dj = zcols(d0.dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n        dc = zcols(d0, [\"CONS\"])\n        B = {\"n_rows_CONS\": int(len(dc)), \"n_rows_joint\": int(len(dj)), \"n_concepts_joint\": int(dj.ci.nunique()),\n             \"share_rows_dropped_for_EMB_SOC\": 1 - len(dj) / max(len(dc), 1),\n             \"CONS_mean\": float(d0.CONS.mean()), \"CONS_sd\": float(d0.CONS.std())}\n        B[\"joint\"] = fit_A_set(dj, XS_JOINT, with_A3=True, with_nb=(build == \"HOME\"))\n        B[\"cons_only\"] = fit_A_set(dc, [\"zCONS\"], with_A3=True, with_nb=(build == \"HOME\"))\n        logger.info(f\"A {build}: joint A1 {B['joint']['A1']['coef']['zCONS']} A2 {B['joint']['A2']['coef']['zCONS']}\")\n        # bootstrap ratio (headline = HOME joint), plus CONS-only\n        br = boot_ratio(dj, XS_JOINT, nb, SEED, W)\n        pf1 = B[\"joint\"][\"A1\"][\"coef\"][\"zCONS\"][\"b\"]\n        br[\"irls_vs_pyfixest_abs_diff_A1\"] = abs(br[\"b_A1_irls\"] - pf1)\n        np.save(DATA / f\"boot_ratio_{build}_joint.npy\", br.pop(\"boot_b\"))\n        B[\"joint\"][\"ratio_boot\"] = br\n        brc = boot_ratio(dc, [\"zCONS\"], nb, SEED + 7, W)\n        brc.pop(\"boot_b\")\n        B[\"cons_only\"][\"ratio_boot\"] = brc\n        logger.info(f\"A {build}: ratio {br['ratio']:.3f} CI {br['ratio_ci']} (irls-pf diff \"\n                    f\"{br['irls_vs_pyfixest_abs_diff_A1']:.2e}); cons-only {brc['ratio']:.3f} {brc['ratio_ci']}\")\n        # per body / per group (joint, A1 and A2, CRV1) + DL across groups\n        B[\"by_body\"] = {}\n        for bd in sorted(d0.body.unique()):\n            g = zcols(d0[d0.body == bd].dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n            B[\"by_body\"][bd] = fit_A_set(g, XS_JOINT, with_A3=False)\n        B[\"by_group\"] = {}\n        for gname in GROUPS5 + [\"MATHDEC\"]:\n            g = zcols(d0[d0.group5 == gname].dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n            if g.ci.nunique() < 30:\n                continue\n            B[\"by_group\"][gname] = fit_A_set(g, XS_JOINT, with_A3=False)\n        for m in [\"A1\", \"A2\"]:\n            bs = [B[\"by_group\"][g][m][\"coef\"][\"zCONS\"][\"b\"] for g in GROUPS5 if g in B[\"by_group\"]]\n            ss = [B[\"by_group\"][g][m][\"coef\"][\"zCONS\"][\"se\"] for g in GROUPS5 if g in B[\"by_group\"]]\n            B[f\"DL_{m}_groups\"] = dersimonian_laird(bs, ss)\n        res[\"builds\"][build] = B\n        logger.info(f\"A {build} done in {(time.time() - t) / 60:.1f} min\")\n    jdump(res, RES / (\"cheng_panel_models_quick.json\" if quick else \"cheng_panel_models.json\"))\n    return res\n\n\ndef refit_nb(logger) -> None:\n    \"\"\"Re-fit A1-NB for both HOME specs and patch results/cheng_panel_models.json (used when the joint NB fit hit a\n    singular Hessian in the main S3 run).\"\"\"\n    from common import jload\n    res = jload(RES / \"cheng_panel_models.json\")\n    d0 = panel_A(\"HOME\")\n    d0 = d0[np.isfinite(d0.V_next)]\n    dj = zcols(d0.dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n    dc = zcols(d0, [\"CONS\"])\n    for spec, d, xs in ((\"joint\", dj, XS_JOINT), (\"cons_only\", dc, [\"zCONS\"])):\n        try:\n            res[\"builds\"][\"HOME\"][spec][\"A1_NB\"] = nb_fit(d, xs)\n        except (ValueError, np.linalg.LinAlgError) as e:\n            res[\"builds\"][\"HOME\"][spec][\"A1_NB\"] = {\"error\": repr(e)[:300]}\n        logger.info(f\"A1-NB {spec}: {res['builds']['HOME'][spec]['A1_NB']}\")\n    jdump(res, RES / \"cheng_panel_models.json\")\n\n\n# ----------------------------------------------------------------------------- test C\ndef panel_C() -> pd.DataFrame:\n    yp = pd.read_parquet(EXP11 / \"data/yearly_panel.parquet\",\n                         columns=[\"ci\", \"year\", \"t0\", \"h_end\", \"body\", \"group\", \"y_next\", \"at_risk_next\", \"deg\",\n                                  \"log1p_home\", \"log1p_all\", \"log1p_deg\", \"log_at_risk\"])\n    yp = yp[(yp.at_risk_next > 0) & (yp.deg >= 2) & yp.y_next.notna()]\n    f = pd.read_parquet(DATA / \"cheng_features.parquet\")\n    f = f[(f.body_src == \"EXP5\") & (f.build == \"HOME\")][[\"ci\", \"year\", \"CONS\"]]\n    d = yp.merge(f, on=[\"ci\", \"year\"], how=\"left\")\n    d = d[np.isfinite(d.CONS)].copy()\n    # home share from Exp11 counts_m (grounded counts per ci x year x vfield)\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\", usecols=[\"ci\", \"home\"])\n    hm = {int(r.ci): home_codes(r.home) for r in fr.itertuples()}\n    cm = pd.read_parquet(EXP11 / \"data/counts_m.parquet\")\n    cm = cm[cm.ci.isin(set(d.ci))]\n    cm[\"is_home\"] = [v in hm.get(c, ()) for c, v in zip(cm.ci.to_numpy(), cm.vfield.to_numpy())]\n    tot = cm.groupby([\"ci\", \"year\"]).n.sum().rename(\"tot\")\n    hom = cm[cm.is_home].groupby([\"ci\", \"year\"]).n.sum().rename(\"hom\")\n    hs = pd.concat([tot, hom], axis=1).fillna(0).reset_index()\n    hs[\"hshare\"] = np.where(hs.tot > 0, hs.hom / hs.tot.clip(lower=1), np.nan)\n    d = d.merge(hs[[\"ci\", \"year\", \"hshare\"]], on=[\"ci\", \"year\"], how=\"left\").merge(\n        hs[[\"ci\", \"year\", \"hshare\"]].assign(year=hs.year - 1).rename(columns={\"hshare\": \"hshare_next\"}),\n        on=[\"ci\", \"year\"], how=\"left\")\n    d[\"dHomeShare_next\"] = d.hshare_next - d.hshare\n    d[\"group5\"] = d.group.map(GROUP5)\n    return zcols(d, [\"CONS\"]).reset_index(drop=True)\n\n\nCTRL = [\"log1p_home\", \"log1p_all\", \"log1p_deg\", \"log_at_risk\"]\n\n\ndef _boot_C_worker(args) -> list[tuple[float, float]]:\n    d, cl, seeds = args\n    import pyfixest as pf\n    out = []\n    for s in seeds:\n        rng = np.random.default_rng(s)\n        pick = rng.integers(0, len(cl), len(cl))\n        rows = np.concatenate([cl[p] for p in pick])\n        newid = np.concatenate([np.full(len(cl[p]), j) for j, p in enumerate(pick)])\n        b = d.iloc[rows].copy()\n        b[\"ci\"] = newid\n        with warnings.catch_warnings():\n            warnings.simplefilter(\"ignore\")\n            try:\n                b1 = float(pf.fepois(f\"y_next ~ zCONS + {' + '.join(CTRL)} | ci + year\", data=b,\n                                     vcov=\"iid\").coef()[\"zCONS\"])\n            except (ValueError, RuntimeError, np.linalg.LinAlgError):\n                b1 = float(\"nan\")\n            bb = b.dropna(subset=[\"dHomeShare_next\"])\n            try:\n                b2 = float(pf.feols(f\"dHomeShare_next ~ zCONS + {' + '.join(CTRL)} | ci + year\", data=bb,\n                                    vcov=\"iid\").coef()[\"zCONS\"])\n            except (ValueError, RuntimeError, np.linalg.LinAlgError):\n                b2 = float(\"nan\")\n        out.append((b1, b2))\n    return out\n\n\ndef run_C(logger, quick: bool = False, workers: int = 0) -> dict:\n    W = workers or n_workers()\n    nb = 40 if quick else N_BOOT_PANEL\n    t = time.time()\n    d = panel_C()\n    if quick:\n        keep = d.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)\n        d = d[d.ci.isin(keep)].reset_index(drop=True)\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_rows\": int(len(d)),\n           \"n_concepts\": int(d.ci.nunique()),\n           \"C1\": fepois(d, \"y_next\", [\"zCONS\"] + CTRL, \"ci + year\"),\n           \"C2\": feols(d.dropna(subset=[\"dHomeShare_next\"]), \"dHomeShare_next\", [\"zCONS\"] + CTRL, \"ci + year\"),\n           \"C1_by_body\": {}, \"C2_by_body\": {}}\n    for bd in sorted(d.body.unique()):\n        g = d[d.body == bd]\n        res[\"C1_by_body\"][bd] = fepois(g, \"y_next\", [\"zCONS\"] + CTRL, \"ci + year\")\n        res[\"C2_by_body\"][bd] = feols(g.dropna(subset=[\"dHomeShare_next\"]), \"dHomeShare_next\", [\"zCONS\"] + CTRL,\n                                      \"ci + year\")\n    logger.info(f\"C1 {res['C1']['coef']['zCONS']}  C2 {res['C2']['coef']['zCONS']}  ({time.time() - t:.0f}s)\")\n    cl = cluster_index(d.ci.to_numpy())\n    seeds = [SEED + 500 + k for k in range(nb)]\n    parts = [seeds[i::W] for i in range(W)]\n    out = []\n    t = time.time()\n    with ProcessPoolExecutor(max_workers=W, mp_context=mp.get_context(\"spawn\")) as ex:\n        for r in ex.map(_boot_C_worker, [(d, cl, p) for p in parts]):\n            out.extend(r)\n    B = np.array(out)\n    for j, k in enumerate([\"C1\", \"C2\"]):\n        v = B[:, j]\n        v = v[np.isfinite(v)]\n        res[k][\"boot\"] = {\"n_boot\": int(len(v)), \"ci\": np.percentile(v, [2.5, 97.5]).tolist(),\n                          \"p_one_lt_0\": float((np.sum(v >= 0) + 1) / (len(v) + 1))}\n    logger.info(f\"C bootstrap {nb} draws in {(time.time() - t) / 60:.1f} min: C1 {res['C1']['boot']} \"\n                f\"C2 {res['C2']['boot']}\")\n    jdump(res, RES / (\"panel_C_quick.json\" if quick else \"panel_C.json\"))\n    return res", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] ASSISTANT · 2026-09-30 02:10:19 UTC

```
I'm reading the artifact's library modules so I can decide what goes into the self-contained demo notebook.
```

### [16] TOOL CALL — Bash · 2026-09-30 02:10:19 UTC

```
Read static_cheng.py and stats helpers:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/lib/static_cheng.py | head -250; grep -n "def " $W/lib/stats_core.py $W/lib/rq1stats.py
```

### [17] TOOL RESULT — Bash · 2026-09-30 02:10:19 UTC

```
{"stdout": "\"\"\"S4 (test B: static early trait vs reach / depth), S6 (test D: Palla size x turnover), S7 (test E: coupling).\n\npsp = partial Spearman = Pearson(resid(rank x | Z), resid(rank y | Z)), Z = [1, rank(B5), dummies]; ranks and the\nresidualisation are recomputed inside every concept-bootstrap draw (EXP8 rq1stats.psp_point logic). Several x / y\ncolumns share one draw (same resampled concepts), so paired differences use the SAME draws on a common complete-case\nset. Covariates: B5 + onset-year dummies; + 8-group dummies when groups are pooled; + body dummies when bodies are\npooled; + window_flag for the 2015-17 cohort (EXP10 R0). All tables: selection data, not confirmation.\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport multiprocessing as mp\nimport time\nfrom concurrent.futures import ProcessPoolExecutor\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\nfrom common import (B5, BODY_COHORT, DATA, DEPTH, EXP8, EXP10, GROUP5, GROUPS5, N_BOOT_STATIC, REACH, RES, SEED,\n                    SELECTION_LABEL, body_of_split, jdump, n_workers)\nfrom rq1stats import dersimonian_laird\n\nOUTS = REACH + DEPTH\nTRAITS2 = [\"EMB_early_home\", \"SOC_early_home\", \"CONS_early_all\", \"CONS_r_early_home\", \"EMB_cos_early_home\"]\nPRIMARY = \"EXP5_pooled\"\n\n\n# ----------------------------------------------------------------------------- data\ndef static_frame() -> pd.DataFrame:\n    st = pd.read_parquet(DATA / \"cheng_static.parquet\")\n    a5 = pd.read_parquet(EXP8 / \"data/analysis_table.parquet\",\n                         columns=[\"ci\", \"t0\", \"group\", \"split\", \"name\"] + B5 + OUTS)\n    a5[\"body\"] = a5.split.map(body_of_split)\n    a5[\"window_flag\"] = 0\n    V = pd.read_parquet(DATA / \"V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    a5 = a5.merge(V.rename(columns={\"year\": \"y2\", \"V\": \"V_t0p2\"}).assign(y2=lambda x: x.y2), how=\"left\",\n                  left_on=[\"ci\", a5.t0 + 2], right_on=[\"ci\", \"y2\"]).drop(columns=[\"y2\"])\n    a5 = a5.merge(V.rename(columns={\"year\": \"y3\", \"V\": \"V_t0p3\"}), how=\"left\",\n                  left_on=[\"ci\", a5.t0 + 3], right_on=[\"ci\", \"y3\"]).drop(columns=[\"y3\"])\n    a5 = a5.drop(columns=[c for c in a5.columns if c.startswith(\"key_\")])\n    ac = pd.read_parquet(EXP10 / \"data/analysis_cohort.parquet\")\n    ac[\"body\"] = BODY_COHORT\n    ac[\"split\"] = \"COHORT_2015_17\"\n    vc = pd.read_parquet(DATA / \"V_cohort.parquet\", columns=[\"ci\", \"V_t0p2\", \"V_t0p3\"])\n    ac = ac.merge(vc, on=\"ci\", how=\"left\")\n    keep = [\"ci\", \"t0\", \"group\", \"split\", \"name\", \"body\", \"window_flag\", \"V_t0p2\", \"V_t0p3\"] + B5 + OUTS\n    extra = [\"CONTACT_REACH\", \"type\", \"generic\", \"level\", \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\",\n             \"newborn\", \"label_coverage_early\", \"home_coverage_early\", \"agroup\"]\n    df = pd.concat([a5[keep], ac[keep + extra]], ignore_index=True)\n    s = st.drop(columns=[\"body\", \"t0\", \"group\"])\n    df = df.merge(s, on=\"ci\", how=\"left\", suffixes=(\"\", \"_st\"))\n    df[\"group5\"] = df.group.map(GROUP5)\n    df[\"logV_t0p2\"] = np.log1p(df.V_t0p2)\n    return df\n\n\ndef body_frames(df: pd.DataFrame) -> dict[str, pd.DataFrame]:\n    out = {PRIMARY: df[df.body != BODY_COHORT]}\n    for b in [\"DEV\", \"OLD_HELDOUT\", \"COHORT_2010_14\", BODY_COHORT]:\n        out[b] = df[df.body == b]\n    return out\n\n\ndef dummies(v: np.ndarray) -> np.ndarray:\n    u = np.unique(v)\n    if len(u) <= 1:\n        return np.zeros((len(v), 0))\n    return (v[:, None] == u[None, 1:]).astype(float)\n\n\ndef design(d: pd.DataFrame, cont: list[str] | None = None, groups: bool = True) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"(continuous covariates to be ranked, raw dummy matrix).\"\"\"\n    cont = B5 if cont is None else cont\n    cat = [dummies(d.t0.to_numpy())]\n    if groups:\n        cat.append(dummies(d.group.astype(str).to_numpy()))\n    cat.append(dummies(d.body.astype(str).to_numpy()))\n    if d.window_flag.nunique() > 1:\n        cat.append(d[[\"window_flag\"]].to_numpy(float))\n    return d[cont].to_numpy(float), np.hstack(cat)\n\n\n# ----------------------------------------------------------------------------- multi-psp bootstrap engine\ndef _resid_corr(xr: np.ndarray, yr: np.ndarray, Br: np.ndarray, C: np.ndarray) -> np.ndarray:\n    Z = np.hstack([np.ones((len(xr), 1)), Br, C])\n    Yall = np.hstack([xr, yr])\n    beta, *_ = np.linalg.lstsq(Z, Yall, rcond=None)\n    R = Yall - Z @ beta\n    R -= R.mean(0)\n    s = R.std(0)\n    s[s < 1e-12] = np.nan\n    R /= s\n    nx = xr.shape[1]\n    return (R[:, :nx].T @ R[:, nx:]) / len(R)                      # [nx, ny] Pearson of residuals\n\n\ndef psp_multi(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:\n    Br = rankdata(B, axis=0) if B.shape[1] else np.zeros((len(X), 0))\n    return _resid_corr(rankdata(X, axis=0), rankdata(Y, axis=0), Br, C)\n\n\ndef unique_ids(M: np.ndarray) -> list[tuple[np.ndarray, int]]:\n    \"\"\"Per column: ids of the value-sorted unique values (so ranks of any resample follow from bincounts).\"\"\"\n    out = []\n    for j in range(M.shape[1]):\n        _, inv = np.unique(M[:, j], return_inverse=True)\n        out.append((inv.astype(np.int64), int(inv.max()) + 1))\n    return out\n\n\ndef resample_ranks(uids: list[tuple[np.ndarray, int]], idx: np.ndarray) -> np.ndarray:\n    \"\"\"Average ranks (identical to scipy rankdata 'average') of every column within the resample idx, scaled by\n    1/n. For unique value k with c_k copies: rank = cumsum(c)_k - (c_k - 1)/2. No sort needed.\"\"\"\n    n = len(idx)\n    R = np.empty((n, len(uids)))\n    for j, (u, U) in enumerate(uids):\n        ui = u[idx]\n        c = np.bincount(ui, minlength=U)\n        avg = np.cumsum(c) - (c - 1) / 2.0\n        R[:, j] = avg[ui] / n\n    return R\n\n\ndef fast_corr(RX: np.ndarray, RY: np.ndarray, RB: np.ndarray, C: np.ndarray) -> np.ndarray:\n    \"\"\"Residual-correlation matrix via the pseudo-inverse of Z'Z (min-norm LS; exact projection even when the\n    dummy block is rank deficient).\"\"\"\n    Z = np.hstack([np.ones((len(RX), 1)), RB, C])\n    V = np.hstack([RX, RY])\n    ZtZ = Z.T @ Z\n    beta = np.linalg.pinv(ZtZ, rcond=1e-12, hermitian=True) @ (Z.T @ V)\n    R = V - Z @ beta\n    R -= R.mean(0)\n    s = R.std(0)\n    s[s < 1e-12] = np.nan\n    R /= s\n    nx = RX.shape[1]\n    return (R[:, :nx].T @ R[:, nx:]) / len(R)\n\n\ndef multi_boot(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray, n_boot: int, seed: int,\n               check: bool = True) -> dict:\n    ok = np.all(np.isfinite(X), 1) & np.all(np.isfinite(Y), 1) & np.all(np.isfinite(B), 1)\n    X, Y, B, C = X[ok], Y[ok], B[ok], C[ok]\n    n = len(X)\n    if n < 30:\n        return {\"n\": n, \"est\": np.full((X.shape[1], Y.shape[1]), np.nan), \"boot\": np.zeros((0, X.shape[1], Y.shape[1]))}\n    keep = C.std(0) > 0\n    est = psp_multi(X, Y, B, C[:, keep])                           # exact path (lstsq, scipy rankdata)\n    ux, uy, ub = unique_ids(X), unique_ids(Y), unique_ids(B)\n    rng = np.random.default_rng(seed)\n    bs = np.empty((n_boot, X.shape[1], Y.shape[1]))\n    max_dev = 0.0\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        bs[b] = fast_corr(resample_ranks(ux, i), resample_ranks(uy, i), resample_ranks(ub, i), C[i])\n        if check and b < 2:                                         # fast path == exact path on the first draws\n            Ci = C[i]\n            ex = psp_multi(X[i], Y[i], B[i], Ci[:, Ci.std(0) > 0])\n            max_dev = max(max_dev, float(np.nanmax(np.abs(ex - bs[b]))))\n    if max_dev > 1e-8:\n        raise ValueError(f\"fast bootstrap path deviates from exact psp by {max_dev:.2e}\")\n    return {\"n\": n, \"est\": est, \"boot\": bs, \"fast_path_max_dev\": max_dev}\n\n\ndef summ(est: float, bs: np.ndarray, direction: int = -1) -> dict:\n    bs = bs[np.isfinite(bs)]\n    if not len(bs) or not np.isfinite(est):\n        return {\"rho\": None, \"ci\": [None, None], \"se\": None}\n    lo, hi = np.percentile(bs, [2.5, 97.5])\n    return {\"rho\": float(est), \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"p_one_pred\": float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1)),\n            \"p_two\": float(min(1.0, 2 * min((np.sum(bs <= 0) + 1) / (len(bs) + 1), (np.sum(bs >= 0) + 1) / (len(bs) + 1)))),\n            \"n_boot\": int(len(bs))}\n\n\ndef task_trait(args) -> dict:\n    \"\"\"One trait x one body: depth set (O1c, O1b, O3 own complete cases) and reach set (O2r_* complete cases, with\n    the depth outcomes on the SAME rows for the paired differences).\"\"\"\n    name, d, x, n_boot, seed, groups = args\n    out = {\"task\": name, \"x\": x, \"n_body\": int(len(d))}\n    B, C = design(d, groups=groups)\n    xv = d[[x]].to_numpy(float)\n    r1 = multi_boot(xv, d[DEPTH].to_numpy(float), B, C, n_boot, seed)\n    r2 = multi_boot(xv, d[REACH + DEPTH].to_numpy(float), B, C, n_boot, seed + 1)\n    res = {}\n    for j, y in enumerate(DEPTH):\n        res[y] = summ(r1[\"est\"][0, j], r1[\"boot\"][:, 0, j], direction=-1 if y == \"O3\" else 1)\n        res[y][\"n\"] = r1[\"n\"]\n    for j, y in enumerate(REACH):\n        res[y] = summ(r2[\"est\"][0, j], r2[\"boot\"][:, 0, j], direction=-1)\n        res[y][\"n\"] = r2[\"n\"]\n    diffs = {}\n    for a, b in [(\"O1c\", \"O2r_m50\"), (\"O1b\", \"O2r_m50\"), (\"O1c\", \"O2r_resid\"), (\"O3\", \"O2r_m50\")]:\n        ia, ib = (REACH + DEPTH).index(a), (REACH + DEPTH).index(b)\n        e = r2[\"est\"][0, ia] - r2[\"est\"][0, ib]\n        bs = r2[\"boot\"][:, 0, ia] - r2[\"boot\"][:, 0, ib]\n        diffs[f\"{a}-{b}\"] = summ(e, bs, direction=1)\n        diffs[f\"{a}-{b}\"][\"n_common\"] = r2[\"n\"]\n        diffs[f\"{a}-{b}\"][\"psp_a_common\"] = float(r2[\"est\"][0, ia])\n        diffs[f\"{a}-{b}\"][\"psp_b_common\"] = float(r2[\"est\"][0, ib])\n    out.update({\"psp\": res, \"paired_diff\": diffs})\n    return out\n\n\ndef task_volume(args) -> dict:\n    name, d, x, n_boot, seed = args\n    xv, v3, v2 = d[x].to_numpy(float), d.V_t0p3.to_numpy(float), d.logV_t0p2.to_numpy(float)\n    ok = np.isfinite(xv) & np.isfinite(v3) & np.isfinite(v2)\n    xv, v3, v2 = xv[ok], v3[ok], v2[ok]\n    n = len(xv)\n    out = {\"task\": name, \"x\": x, \"n\": int(n)}\n    if n < 30:\n        return out\n    rng = np.random.default_rng(seed)\n    body_c = dummies(d.body.astype(str).to_numpy()[ok])\n    Zc = np.hstack([v2[:, None], body_c])\n    raw = float(stats.spearmanr(xv, v3)[0])\n    ps = float(_resid_corr(rankdata(xv)[:, None], rankdata(v3)[:, None], rankdata(v2)[:, None], body_c)[0, 0])\n    Bb, Cb = design(d[ok])\n    ok5 = np.all(np.isfinite(Bb), 1)                               # B5 variant: complete B5 rows only\n    x5, y5, Bb, Cb = xv[ok5], v3[ok5], Bb[ok5], Cb[ok5]\n    n5 = len(x5)\n    ps5 = float(psp_multi(x5[:, None], y5[:, None], Bb, Cb[:, Cb.std(0) > 0])[0, 0])\n    br, bp, bp5 = np.empty(n_boot), np.empty(n_boot), np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        br[b] = stats.spearmanr(xv[i], v3[i])[0]\n        k = body_c[i].std(0) > 0\n        bp[b] = _resid_corr(rankdata(xv[i])[:, None], rankdata(v3[i])[:, None], rankdata(v2[i])[:, None],\n                            body_c[i][:, k])[0, 0]\n        j = rng.integers(0, n5, n5)\n        Ci = Cb[j]\n        bp5[b] = psp_multi(x5[j][:, None], y5[j][:, None], Bb[j], Ci[:, Ci.std(0) > 0])[0, 0]\n    out[\"n_B5_variant\"] = int(n5)\n    out[\"B_raw_spearman_V_t0p3\"] = summ(raw, br, direction=1)\n    out[\"B_size_psp_V_t0p3_given_logV_t0p2\"] = summ(ps, bp, direction=1)\n    out[\"B_size_psp_V_t0p3_given_B5_dummies\"] = summ(ps5, bp5, direction=1)\n    return out\n\n\ndef run_tasks(tasks: list, fn, workers: int) -> list[dict]:\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex:\n        return list(ex.map(fn, tasks))\n\n\ndef mde(se: float | None) -> float | None:\n    return 2.8 * se if se else None\n\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:15:    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, ridge: float = 0.0):\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:28:    def nll(self, b: np.ndarray) -> tuple[float, np.ndarray]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:43:    def hessian(self, b: np.ndarray) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:54:    def fit(self) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:68:def ll_null_clogit(y: np.ndarray, strata: np.ndarray) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:76:def demean(A: np.ndarray, groups: list[np.ndarray], iters: int = 50, tol: float = 1e-10) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:93:def fe_ols(y: np.ndarray, X: np.ndarray, fe: list[np.ndarray], cluster: np.ndarray, names: list[str]) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:124:def fe_poisson(y: np.ndarray, X: np.ndarray, group: np.ndarray, names: list[str], offset: np.ndarray | None = None,\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:165:def dersimonian_laird(b: np.ndarray, se: np.ndarray) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/stats_core.py:185:def sign_test(k_pos: int, n: int) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:13:def dummies(v: np.ndarray, drop_first: bool = True) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:21:def _resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:26:def psp_point(x: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:41:def psp_boot(x, y, B, cat, n_boot: int, seed: int) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:69:def spearman_raw(x, y) -> tuple[float, int]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:77:def logit_fit(X: np.ndarray, y: np.ndarray, lam: float = 1.0, iters: int = 50) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:100:def logit_pred(w: np.ndarray, X: np.ndarray) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:104:def auc(y: np.ndarray, s: np.ndarray) -> float:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:113:def _std_fit(X):\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:120:def logo_oof(X: np.ndarray, y: np.ndarray, grp: np.ndarray) -> np.ndarray:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:134:def dauc_logo(Xb: np.ndarray, x: np.ndarray, y: np.ndarray, grp: np.ndarray) -> tuple[float, float, float]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:142:def dauc_boot(Xb, x, y, grp, n_boot: int, seed: int) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:163:def dersimonian_laird(b, se) -> dict:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:185:def holm(p: list[float]) -> list[float]:\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/rq1stats.py:199:def sign_test_two_sided(k_pos: int, n: int) -> float:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-30 02:10:29 UTC

```
Read build.py and rq1stats:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; sed -n 1,200p $W/lib/build.py; sed -n 1,80p $W/lib/rq1stats.py; sed -n 160,200p $W/lib/rq1stats.py
```

### [19] TOOL RESULT — Bash · 2026-09-30 02:10:29 UTC

```
{"stdout": "\"\"\"S1: build the Cheng measures (CONS, CONS_r, EMB, EMB_cos, SOC) per concept x year x build (HOME/ALL), the static\nearly traits, and the yearly grounded volume V(t).\n\nInputs (read-only): Exp11 data/frame_matches_long (EXP5 frame, t0-3..min(t0+10, 2022)), EXP10 data/passC_early\n(2015-17 cohort, t0-3..t0+2, tagstate == 1 kept), EXP5 frame_concepts.csv, EXP10 analysis_cohort.parquet,\nEXP5 scan/agg_counts.parquet (V), Exp11 counts_m.parquet (V check), EXP10 passC_pre_agg + sealed parts (cohort V).\nOutputs: data/cheng_features.parquet, data/cheng_static.parquet, data/V_exp5.parquet, data/V_cohort.parquet,\nresults/s1_build.json (timing, NaN shares, V check).\"\"\"\nfrom __future__ import annotations\n\nimport multiprocessing as mp\nimport time\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\n\nimport numpy as np\nimport pandas as pd\nimport pyarrow as pa\nimport pyarrow.compute as pc\nimport pyarrow.parquet as pq\n\nfrom common import (BODY_COHORT, DATA, EXP5, EXP10, EXP11, GROUP5, RES, SEED, add_deviation, body_of_split,\n                    home_codes, jdump, n_workers, sha256_file)\n\nMEAS = [\"CONS\", \"CONS_r\", \"EMB\", \"EMB_cos\", \"SOC\"]\n\n\ndef _init() -> None:\n    import cheng\n    cheng.init_context()\n\n\ndef run_chunk(k: int, jobs: list) -> tuple[int, list, float, list]:\n    import cheng\n    t = time.time()\n    rows, errs = [], []\n    for j in jobs:\n        try:\n            rows.extend(cheng.concept_measures(**j))\n        except (ValueError, IndexError, KeyError, ZeroDivisionError) as e:\n            errs.append((j[\"ci\"], repr(e)[:300]))\n    return k, rows, time.time() - t, errs\n\n\ndef load_flat(tab: pa.Table) -> dict:\n    \"\"\"Sort a (ci, year, vfield, topics, authors) table by (ci, year) and return flat numpy arrays + row ranges.\"\"\"\n    idx = pc.sort_indices(tab, sort_keys=[(\"ci\", \"ascending\"), (\"year\", \"ascending\")])\n    tab = tab.take(idx)\n    ci = tab.column(\"ci\").to_numpy().astype(np.int64)\n    top = tab.column(\"topics\").combine_chunks()\n    aut = tab.column(\"authors\").combine_chunks()\n    out = {\"ci\": ci, \"year\": tab.column(\"year\").to_numpy().astype(np.int64),\n           \"vfield\": tab.column(\"vfield\").to_numpy().astype(np.int64),\n           \"t_off\": top.offsets.to_numpy().astype(np.int64), \"tflat\": top.values.to_numpy().astype(np.int64),\n           \"a_off\": aut.offsets.to_numpy().astype(np.int64),\n           \"aflat\": pc.fill_null(aut.values, -1).to_numpy().astype(np.int64)}\n    u, start, cnt = np.unique(ci, return_index=True, return_counts=True)\n    out[\"ranges\"] = {int(c): (int(s), int(s + n)) for c, s, n in zip(u, start, cnt)}\n    return out\n\n\ndef job_for(F: dict, ci: int, **kw) -> dict | None:\n    if ci not in F[\"ranges\"]:\n        return None\n    s, e = F[\"ranges\"][ci]\n    t0f, t1f = F[\"t_off\"][s], F[\"t_off\"][e]\n    a0f, a1f = F[\"a_off\"][s], F[\"a_off\"][e]\n    return dict(ci=ci, years=F[\"year\"][s:e], vfield=F[\"vfield\"][s:e], t_off=F[\"t_off\"][s:e + 1] - t0f,\n                tflat=F[\"tflat\"][t0f:t1f], a_off=F[\"a_off\"][s:e + 1] - a0f, aflat=F[\"aflat\"][a0f:a1f], **kw)\n\n\ndef run_pool(jobs: list[dict], workers: int, logger, chunk: int = 40) -> tuple[pd.DataFrame, dict]:\n    t = time.time()\n    chunks = [jobs[i:i + chunk] for i in range(0, len(jobs), chunk)]\n    rows, errs, cpu = [], [], 0.0\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex:\n        futs = [ex.submit(run_chunk, k, c) for k, c in enumerate(chunks)]\n        for n_done, f in enumerate(as_completed(futs), 1):\n            k, r, dt, e = f.result()\n            rows.extend(r)\n            errs.extend(e)\n            cpu += dt\n            if n_done % 25 == 0 or n_done == len(chunks):\n                logger.info(f\"  chunks {n_done}/{len(chunks)} {(time.time() - t) / 60:.1f} min errors={len(errs)}\")\n    df = pd.DataFrame(rows)\n    timing = {\"concepts\": len(jobs), \"wall_s\": time.time() - t, \"cpu_s_per_1000_concepts\": 1000 * cpu / max(len(jobs), 1),\n              \"n_errors\": len(errs), \"errors\": errs[:20]}\n    return df, timing\n\n\n# ----------------------------------------------------------------------------- V(t)\ndef build_V_exp5(fr: pd.DataFrame, logger) -> tuple[pd.DataFrame, dict]:\n    ag = pd.read_parquet(EXP5 / \"scan/agg_counts.parquet\", columns=[\"ci\", \"year\", \"tagstate\", \"n\"],\n                         filters=[(\"tagstate\", \"==\", 1)])\n    ag = ag[ag.ci.isin(set(fr.ci))]\n    V = ag.groupby([\"ci\", \"year\"], as_index=False).n.sum().rename(columns={\"n\": \"V_agg\"})\n    del ag\n    cm = pd.read_parquet(EXP11 / \"data/counts_m.parquet\")\n    cm = cm[cm.ci.isin(set(fr.ci))].groupby([\"ci\", \"year\"], as_index=False).n.sum().rename(columns={\"n\": \"V_m\"})\n    rng = np.random.default_rng(SEED)\n    pick = rng.choice(fr.ci.to_numpy(), 200, replace=False)\n    grid = pd.MultiIndex.from_product([pick, range(2000, 2023)], names=[\"ci\", \"year\"]).to_frame(index=False)\n    chk = grid.merge(V, on=[\"ci\", \"year\"], how=\"left\").merge(cm, on=[\"ci\", \"year\"], how=\"left\").fillna(0)\n    exact = float((chk.V_agg == chk.V_m).mean())\n    rel = float((np.abs(chk.V_agg - chk.V_m) / np.maximum(chk.V_m, 1)).mean())\n    corr = float(np.corrcoef(chk.V_agg, chk.V_m)[0, 1])\n    use = \"agg_counts\" if exact >= 0.99 else \"counts_m\"\n    info = {\"U5_cells\": int(len(chk)), \"U5_share_exact\": exact, \"U5_mean_rel_diff\": rel, \"U5_pearson\": corr,\n            \"V_source\": use, \"sum_agg\": float(chk.V_agg.sum()), \"sum_m\": float(chk.V_m.sum())}\n    logger.info(f\"U5 V check: {info}\")\n    if use == \"counts_m\":\n        add_deviation(\"F3_V_source\", f\"agg_counts tagstate==1 matched counts_m exactly in {exact:.3f} of 200x23 \"\n                      f\"cells (< 0.99): V(t) for EXP5 = Exp11 counts_m summed over vfield (Pass M TAG counts), \"\n                      f\"fixed before any model. mean rel diff {rel:.4f}, r = {corr:.4f}\")\n    grid = pd.MultiIndex.from_product([fr.ci.to_numpy(), range(1995, 2023)], names=[\"ci\", \"year\"]).to_frame(index=False)\n    out = grid.merge(V, on=[\"ci\", \"year\"], how=\"left\").merge(cm, on=[\"ci\", \"year\"], how=\"left\").fillna(0)\n    out[\"V\"] = out.V_agg if use == \"agg_counts\" else out.V_m\n    return out[[\"ci\", \"year\", \"V\", \"V_agg\", \"V_m\"]], info\n\n\ndef build_V_cohort(coh: pd.DataFrame, logger) -> tuple[pd.DataFrame, dict]:\n    cis = set(coh.ci)\n    pre = pd.read_parquet(EXP10 / \"data/passC_pre_agg.parquet\")\n    pre = pre[(pre.tagstate == 1) & pre.ci.isin(cis)]\n    parts = sorted((EXP10 / \"data/sealed/parts\").glob(\"sealed_*.parquet\"))\n    logf = EXP10 / \"logs/sealed_files.log\"\n    want = dict(l.split(\"\\t\") for l in logf.read_text().splitlines() if l.strip()) if logf.exists() else {}\n    bad = [p.name for p in parts if p.name in want and sha256_file(p) != want[p.name]]\n    missing = [n for n in want if not (EXP10 / \"data/sealed/parts\" / n).exists()]\n    sealed_ok = bool(parts) and not bad and not missing\n    info = {\"n_sealed_parts\": len(parts), \"n_logged\": len(want), \"sha_mismatch\": bad[:10], \"missing\": missing[:10],\n            \"sealed_ok\": sealed_ok}\n    logger.info(f\"cohort sealed parts check: {info}\")\n    V = pre.groupby([\"ci\", \"year\"], as_index=False).n.sum()\n    if sealed_ok:\n        sl = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)\n        sl = sl[(sl.tagstate == 1) & sl.ci.isin(cis)]\n        V2 = sl.groupby([\"ci\", \"year\"], as_index=False).n.sum()\n        V = pd.concat([V, V2]).groupby([\"ci\", \"year\"], as_index=False).n.sum()\n    else:\n        add_deviation(\"F4_cohort_V\", \"sealed parts missing or sha mismatch: cohort V(t0+3) not evaluable\")\n    m = coh[[\"ci\", \"t0\"]].copy()\n    rec = []\n    for r in m.itertuples():\n        d = V[V.ci == r.ci].set_index(\"year\").n\n        rec.append({\"ci\": int(r.ci), \"V_t0p2\": float(d.get(r.t0 + 2, 0.0)),\n                    \"V_t0p3\": float(d.get(r.t0 + 3, 0.0)) if sealed_ok else float(\"nan\"),\n                    \"V_t0\": float(d.get(r.t0, 0.0)), \"V_t0p1\": float(d.get(r.t0 + 1, 0.0))})\n    return pd.DataFrame(rec), info\n\n\n# ----------------------------------------------------------------------------- static early traits\ndef static_table(feat: pd.DataFrame, meta: pd.DataFrame) -> pd.DataFrame:\n    f = feat.merge(meta[[\"ci\", \"t0\"]], on=\"ci\")\n    f = f[(f.year >= f.t0 + 1) & (f.year <= f.t0 + 2)]\n    g = f.groupby([\"ci\", \"build\"])[MEAS].mean().unstack(\"build\")\n    g.columns = [f\"{m}_early_{b.lower()}\" for m, b in g.columns]\n    g = g.reset_index()\n    # early support diagnostics (HOME build)\n    fh = f[f.build == \"HOME\"].groupby(\"ci\").agg(n_papers_early_home=(\"n_papers\", \"sum\"),\n                                                deg_early_home=(\"n_topics\", \"mean\"),\n                                                n_authors_early_home=(\"n_authors\", \"sum\")).reset_index()\n    return meta[[\"ci\", \"body\", \"t0\", \"group\", \"group5\"]].merge(g, on=\"ci\", how=\"left\").merge(fh, on=\"ci\", how=\"left\")\n\n\ndef run(logger, sample: int = 0, workers: int = 0) -> None:\n    t_all = time.time()\n    W = workers or n_workers()\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\")\n    fr[\"body\"] = fr.split.map(body_of_split)\n    fr[\"group5\"] = fr.group.map(GROUP5)\n    coh = pd.read_parquet(EXP10 / \"data/analysis_cohort.parquet\", columns=[\"ci\", \"t0\", \"home\", \"name\", \"group\"])\n    coh[\"body\"] = BODY_COHORT\n    coh[\"group5\"] = coh.group.map(GROUP5)\n    sfx = f\"_sample{sample}\" if sample else \"\"\n    if sample:\n        fr = fr.sample(sample, random_state=SEED)\n    # ---------------- EXP5 frame\n    t = time.time()\n    tab = pa.concat_tables([pq.read_table(p, columns=[\"ci\", \"year\", \"vfield\", \"topics\", \"authors\"])\n                            for p in sorted((EXP11 / \"data/frame_matches_long\").glob(\"part_*.parquet\"))])\n    tab = tab.filter(pc.is_in(tab.column(\"ci\"), value_set=pa.array(fr.ci.astype(np.int32).to_numpy())))\n    n_rows_exp5 = tab.num_rows\n    F = load_flat(tab)\n    del tab\n    logger.info(f\"EXP5 long rows {n_rows_exp5:,} for {len(F['ranges']):,} concepts loaded in {time.time() - t:.0f}s\")\n    jobs = []\n    for r in fr.itertuples():\n        al = [a for a in str(r.aliases_used).split(\"|\") if a and a != \"nan\"]\n        j = job_for(F, int(r.ci), name=str(r.name), aliases=al, t0=int(r.t0), y_lo=int(r.t0),\n                    y_hi=int(min(r.t0 + 10, 2022)), home=home_codes(r.home))\n        if j is not None:\n            jobs.append(j)\n    del F\n    logger.info(f\"EXP5 jobs {len(jobs)} (workers={W})\")\n    feat5, tim5 = run_pool(jobs, W, logger)\n    del jobs\n    # ---------------- 2015-17 cohort\n    tim_c = {}\n    featc = pd.DataFrame()\n    if not sample:\n\"\"\"Statistics for RQ1: partial Spearman given a baseline (rank residualisation, refitted in every bootstrap\nresample), L2-logistic delta-AUC (leave-one-group-out, out-of-fold), DerSimonian-Laird pooling, Holm, sign tests.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\n\n# ----------------------------------------------------------------------------- partial Spearman\ndef dummies(v: np.ndarray, drop_first: bool = True) -> np.ndarray:\n    u = np.unique(v)\n    if len(u) <= 1:\n        return np.zeros((len(v), 0))\n    cols = u[1:] if drop_first else u\n    return (v[:, None] == cols[None, :]).astype(float)\n\n\ndef _resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:\n    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)\n    return Y - Z @ beta\n\n\ndef psp_point(x: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> float:\n    \"\"\"Pearson(resid(rank x ~ rank B + cat dummies), resid(rank y ~ same)). Rows must be complete.\"\"\"\n    Zc = [np.ones((len(x), 1))]\n    if B is not None and B.shape[1]:\n        Zc.append(rankdata(B, axis=0))\n    if cat is not None and cat.shape[1]:\n        Zc.append(cat)\n    Z = np.hstack(Zc)\n    R = _resid(Z, np.c_[rankdata(x), rankdata(y)])\n    sx, sy = R[:, 0].std(), R[:, 1].std()\n    if sx <= 1e-12 or sy <= 1e-12:\n        return float(\"nan\")\n    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])\n\n\ndef psp_boot(x, y, B, cat, n_boot: int, seed: int) -> dict:\n    \"\"\"Point + concept bootstrap (resample rows; ranks and residualisation recomputed in each resample).\"\"\"\n    ok = np.isfinite(x) & np.isfinite(y)\n    if B is not None:\n        ok &= np.all(np.isfinite(B), axis=1)\n    x, y = x[ok], y[ok]\n    Bs = B[ok] if B is not None else None\n    cs = cat[ok] if cat is not None else None\n    n = len(x)\n    if n < 20 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"rho\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"se\": float(\"nan\"), \"p\": float(\"nan\"),\n                \"boot\": np.array([])}\n    est = psp_point(x, y, Bs, cs)\n    rng = np.random.default_rng(seed)\n    bs = np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        bs[b] = psp_point(x[i], y[i], Bs[i] if Bs is not None else None, cs[i] if cs is not None else None)\n    bs = bs[np.isfinite(bs)]\n    lo, hi = np.percentile(bs, [2.5, 97.5]) if len(bs) else (np.nan, np.nan)\n    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))\n    se_z = float(np.std(z, ddof=1)) if len(z) > 2 else float(\"nan\")\n    ze = math.atanh(max(min(est, 0.999999), -0.999999)) if np.isfinite(est) else float(\"nan\")\n    p = float(2 * stats.norm.sf(abs(ze / se_z))) if se_z and np.isfinite(se_z) and se_z > 0 else float(\"nan\")\n    return {\"n\": int(n), \"rho\": est, \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"z\": ze, \"se_z\": se_z, \"p\": p, \"boot\": bs}\n\n\ndef spearman_raw(x, y) -> tuple[float, int]:\n    ok = np.isfinite(x) & np.isfinite(y)\n    if ok.sum() < 10 or np.unique(x[ok]).size < 3:\n        return float(\"nan\"), int(ok.sum())\n    return float(stats.spearmanr(x[ok], y[ok])[0]), int(ok.sum())\n\n\n# ----------------------------------------------------------------------------- L2 logistic (sklearn C=1 objective)\ndef logit_fit(X: np.ndarray, y: np.ndarray, lam: float = 1.0, iters: int = 50) -> np.ndarray:\n    \"\"\"Newton-IRLS for  sum log-loss + lam/2 ||w||^2 (intercept unpenalised). X excludes the intercept.\"\"\"\n    n, d = X.shape\n    A = np.c_[np.ones(n), X]\n\n\n# ----------------------------------------------------------------------------- pooling / multiplicity\ndef dersimonian_laird(b, se) -> dict:\n    \"\"\"EXP6 lib/stats_core.dersimonian_laird (verbatim logic).\"\"\"\n    b, se = np.asarray(b, float), np.asarray(se, float)\n    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n    b, se = b[ok], se[ok]\n    k = len(b)\n    if k == 0:\n        return {\"k\": 0, \"b\": float(\"nan\"), \"se\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"p\": float(\"nan\"),\n                \"tau2\": float(\"nan\"), \"I2\": float(\"nan\"), \"Q\": float(\"nan\")}\n    w = 1 / se**2\n    bf = (w * b).sum() / w.sum()\n    Q = float((w * (b - bf) ** 2).sum())\n    Cc = w.sum() - (w**2).sum() / w.sum()\n    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 and Cc > 0 else 0.0\n    ws = 1 / (se**2 + tau2)\n    bre = (ws * b).sum() / ws.sum()\n    sre = math.sqrt(1 / ws.sum())\n    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0\n    return {\"k\": k, \"b\": float(bre), \"se\": sre, \"ci\": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],\n            \"p\": float(2 * stats.norm.sf(abs(bre / sre))), \"tau2\": float(tau2), \"Q\": Q, \"I2\": float(I2)}\n\n\ndef holm(p: list[float]) -> list[float]:\n    p = np.asarray(p, float)\n    out = np.full(len(p), np.nan)\n    ok = np.isfinite(p)\n    idx = np.nonzero(ok)[0]\n    m = len(idx)\n    order = idx[np.argsort(p[idx])]\n    run = 0.0\n    for r, i in enumerate(order):\n        run = max(run, min(1.0, (m - r) * p[i]))\n        out[i] = run\n    return out.tolist()\n\n\ndef sign_test_two_sided(k_pos: int, n: int) -> float:\n    return float(stats.binomtest(k_pos, n, 0.5).pvalue) if n > 0 else float(\"nan\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-30 02:10:43 UTC

```
Inspect artifact parquet tables and upstream inputs:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cd $W && ls .venv 2>/dev/null | head -2; which python3; python3 -c "
import pandas as pd
for f in ['static_analysis_table','cheng_features','cheng_static','V_exp5']:
    d=pd.read_parquet('data/'+f+'.parquet'); print(f,d.shape); print(d.dtypes.to_string()); print(d.head(3).to_string())
"; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/ /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/inputs
```

### [21] TOOL RESULT — Bash · 2026-09-30 02:10:45 UTC

```
{"stdout": "/usr/local/bin/python3\nstatic_analysis_table (13942, 46)\nci                        int64\nt0                        int64\ngroup                    object\nsplit                    object\nname                     object\nbody                     object\nwindow_flag               int64\nV_t0p2                  float64\nV_t0p3                  float64\nlogvol                  float64\ngrowth_c                float64\noffhome_share           float64\nentropy                 float64\nreach                     int64\nO2r_m50                 float64\nO2r_resid               float64\nO1c                     float64\nO1b                     float64\nO3                      float64\nCONTACT_REACH           float64\ntype                     object\ngeneric                 float64\nlevel                   float64\nfp_logN                 float64\nfp_nfields              float64\nfp_reemerge             float64\nfp_wiki_pre             float64\nnewborn                 float64\nlabel_coverage_early    float64\nhome_coverage_early     float64\nagroup                   object\ngroup5                   object\nCONS_early_all          float64\nCONS_early_home         float64\nCONS_r_early_all        float64\nCONS_r_early_home       float64\nEMB_early_all           float64\nEMB_early_home          float64\nEMB_cos_early_all       float64\nEMB_cos_early_home      float64\nSOC_early_all           float64\nSOC_early_home          float64\nn_papers_early_home       int64\ndeg_early_home          float64\nn_authors_early_home      int64\nlogV_t0p2               float64\n   ci    t0    group   split                   name            body  window_flag  V_t0p2  V_t0p3    logvol  growth_c  offhome_share   entropy  reach   O2r_m50  O2r_resid       O1c  O1b   O3  CONTACT_REACH  type  generic  level  fp_logN  fp_nfields  fp_reemerge  fp_wiki_pre  newborn  label_coverage_early  home_coverage_early agroup   group5  CONS_early_all  CONS_early_home  CONS_r_early_all  CONS_r_early_home  EMB_early_all  EMB_early_home  EMB_cos_early_all  EMB_cos_early_home  SOC_early_all  SOC_early_home  n_papers_early_home  deg_early_home  n_authors_early_home  logV_t0p2\n0   3  2012  MATHDEC  COHORT  Complete intersection  COHORT_2010_14            0    29.0    26.0  4.290459  0.265703       0.144928  0.502340      3  2.960784  -1.481981 -0.212922  0.0  0.0            NaN  None      NaN    NaN      NaN         NaN          NaN          NaN      NaN                   NaN                  NaN   None  MATHDEC        0.695331         0.630698          0.759040           0.690065       3.012849        3.205342           0.436913            0.439953       0.006877        0.008658                   39            10.5                    55   3.401197\n1   4  2004      Eng     DEV       Torque converter             DEV            0    17.0    19.0  4.174387 -0.367725       0.018519  0.092216      1  2.898734  -1.497993  0.347401  1.0  0.0            NaN  None      NaN    NaN      NaN         NaN          NaN          NaN      NaN                   NaN                  NaN   None   CS+Eng        0.583804         0.601188          0.681216           0.706812       1.447065        1.518381           0.265305            0.270136       0.000000        0.000000                   31            13.5                    38   2.890372\n2  16  2011      SOC  COHORT          Early adopter  COHORT_2010_14            0    25.0    27.0  4.174387  0.122602       0.750000  2.144001      7  9.882396   5.485668  0.207639  1.0  0.0            NaN  None      NaN    NaN      NaN         NaN          NaN          NaN      NaN                   NaN                  NaN   None      SOC        0.323199              NaN          0.577074                NaN       0.913265             NaN           0.112644                 NaN       0.000000        0.000000                    4             4.5                     7   3.258097\ncheng_features (279242, 12)\nci             int64\nyear           int64\nbuild         object\nn_papers       int64\nn_topics       int64\nCONS         float64\nCONS_r       float64\nEMB          float64\nEMB_cos      float64\nn_authors      int64\nSOC          float64\nbody_src      object\n    ci  year build  n_papers  n_topics      CONS    CONS_r       EMB   EMB_cos  n_authors       SOC body_src\n0  198  2004  HOME         7        16  0.133333  0.471405  1.295245  0.211323         21  0.000000     EXP5\n1  198  2005  HOME         5        14  0.436564  0.600000  1.278191  0.176086         21  0.004762     EXP5\n2  198  2006  HOME         5        10  0.076696  0.242536  0.847812  0.123788         16  0.000000     EXP5\ncheng_static (13942, 18)\nci                        int64\nbody                     object\nt0                        int64\ngroup                    object\ngroup5                   object\nCONS_early_all          float64\nCONS_early_home         float64\nCONS_r_early_all        float64\nCONS_r_early_home       float64\nEMB_early_all           float64\nEMB_early_home          float64\nEMB_cos_early_all       float64\nEMB_cos_early_home      float64\nSOC_early_all           float64\nSOC_early_home          float64\nn_papers_early_home       int64\ndeg_early_home          float64\nn_authors_early_home      int64\n   ci            body    t0    group   group5  CONS_early_all  CONS_early_home  CONS_r_early_all  CONS_r_early_home  EMB_early_all  EMB_early_home  EMB_cos_early_all  EMB_cos_early_home  SOC_early_all  SOC_early_home  n_papers_early_home  deg_early_home  n_authors_early_home\n0   3  COHORT_2010_14  2012  MATHDEC  MATHDEC        0.695331         0.630698          0.759040           0.690065       3.012849        3.205342           0.436913            0.439953       0.006877        0.008658                   39            10.5                    55\n1   4             DEV  2004      Eng   CS+Eng        0.583804         0.601188          0.681216           0.706812       1.447065        1.518381           0.265305            0.270136       0.000000        0.000000                   31            13.5                    38\n2  16  COHORT_2010_14  2011      SOC      SOC        0.323199              NaN          0.577074                NaN       0.913265             NaN           0.112644                 NaN       0.000000        0.000000                    4             4.5                     7\nV_exp5 (349972, 5)\nci         int64\nyear       int64\nV        float64\nV_agg    float64\nV_m      float64\n   ci  year    V  V_agg  V_m\n0   3  1995  8.0    8.0  0.0\n1   3  1996  4.0    4.0  0.0\n2   3  1997  5.0    5.0  0.0\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/:\nbg_topics.npz\nboot_fe_DEV.parquet\nbridging_papers.parquet\nclosure_jumps.parquet\ncounts_m.parquet\nd3_concept_year.parquet\nframe_matches_long\ngrounded_V.npz\npartner_indicators.parquet\npassM_info.json\nport_static.parquet\nstatic_partners.parquet\nstatic_partners_typed.parquet\nw3_comms.json\nyearly_features.parquet\nyearly_panel.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/inputs:\nbackbone\nfield_backbone.json\nfrozen_lexicon.sha256\nlexicon_v1.parquet\nsource_field.parquet\ntopic_ids.json\ntopic_meta.csv", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Bash · 2026-09-30 02:10:59 UTC

```
Read ego_ctx and rest of static_cheng:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/lib/ego_ctx.py; grep -n "def \|^import\|^from" $W/lib/ego.py; sed -n 250,420p $W/lib/static_cheng.py
```

### [23] TOOL RESULT — Bash · 2026-09-30 02:10:59 UTC

```
{"stdout": "\"\"\"Context for lib/ego.py: EXP3 Leiden-gamma-3 topic backbones (slices 2000-04/05-09/10-14), topic metadata,\ncontent lemmas (verbatim from EXP3 common.py), and the Pass A full-corpus topic background.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport re\nfrom collections import Counter\nfrom functools import lru_cache\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, INPUTS\n\n_STOP = set(\"a an and are as at be but by for if in into is it no not of on or such that the their then there these \"\n            \"they this to was will with its via from using based\".split())\n_TOK = re.compile(r\"[^\\W_]+\", re.UNICODE)\n\n\n@lru_cache(maxsize=None)\ndef _stemmer():\n    import snowballstemmer\n    return snowballstemmer.stemmer(\"porter\")\n\n\ndef lemmas(text: str) -> set[str]:\n    t = re.sub(r\"[\\-‐-—/]\", \" \", str(text).lower())\n    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}\n\n\ndef topic_lemma_df(names: list[str]) -> Counter:\n    df = Counter()\n    for n in names:\n        df.update(lemmas(n))\n    return df\n\n\ndef backbone_context() -> dict:\n    tids = json.loads((INPUTS / \"topic_ids.json\").read_text())\n    tm = pd.read_csv(INPUTS / \"topic_meta.csv\").set_index(\"topic\").loc[tids]\n    sl = [np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\") for s in range(3)]\n    names = tm.name.tolist()\n    return dict(nt=len(tids), comm=[z[\"comm\"] for z in sl], comm_q=[z[\"comm_q\"] for z in sl],\n                deg=[z[\"deg\"] for z in sl], knn=[(z[\"ka\"], z[\"kb\"]) for z in sl],\n                full_edges=[(z[\"a\"], z[\"b\"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,\n                ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names], lemmas=lemmas)\n\n\ndef rq1_context() -> dict:\n    ctx = backbone_context()\n    z = np.load(DATA / \"bg_topics.npz\")\n    years = z[\"years\"].tolist()\n    ctx.update(years=years, bg=z[\"BG\"], Gt=dict(zip(years, z[\"GT\"].tolist())))\n    return ctx\n12:from __future__ import annotations\n14:import math\n15:import warnings\n16:from collections import Counter\n18:import igraph as ig\n19:import numpy as np\n30:def slice_of(y: int) -> int:\n37:def rq1_windows(t0: int) -> dict[str, list[int]]:\n41:def exp3_windows(t0: int) -> dict[str, list[int]]:\n45:def lgC(n: float, k: float) -> float:\n50:def set_context(ctx: dict) -> None:\n59:def knn_graph(s: int) -> ig.Graph:\n66:def bg_window(years: list[int]) -> tuple[np.ndarray, float]:\n71:def window_counts(works, years) -> tuple[np.ndarray, int]:\n83:def pmi(nck, nc, nbg, N):\n90:def neighbours(nck, nc, nbg, N, excl, min_n: int = 2):\n96:def topS(nck, p, nb, top: int = TOPN_F):\n104:def self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:\n116:def distinct_null(pool_idx, w, M, labels, rng, n):\n133:def f_null(p_mix, pool, T1, T3, nc1, nc3, nbg1, N1, nbg3, N3, rng, n):\n138:    def S(T, nc, nbg, N):\n153:def _centrality(idx: np.ndarray, s: int, cutoff: int | None) -> tuple[float, int, float]:\n165:def concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,\n195:    def dz(labels_by_slice, pool_idx, new_list):\n256:    def jac(a, b):\n\n# ----------------------------------------------------------------------------- test B\ndef run_B(logger, quick: bool = False) -> dict:\n    t = time.time()\n    W = n_workers()\n    nb = 100 if quick else N_BOOT_STATIC\n    nb2 = 60 if quick else 500\n    nbg = 100 if quick else 1000\n    df = static_frame()\n    df.to_parquet(DATA / \"static_analysis_table.parquet\", index=False)\n    bodies = body_frames(df)\n    tasks_t, tasks_v = [], []\n    for bi, (bn, d) in enumerate(bodies.items()):\n        tasks_t.append((f\"{bn}|CONS_early_home\", d, \"CONS_early_home\", nb, SEED + 10 * bi, True))\n        tasks_v.append((f\"{bn}|volume\", d, \"CONS_early_home\", nb, SEED + 10 * bi + 5))\n        for k, x in enumerate(TRAITS2):\n            tasks_t.append((f\"{bn}|{x}\", d, x, nb2, SEED + 1000 + 10 * bi + k, True))\n        tasks_v.append((f\"{bn}|volume_all\", d, \"CONS_early_all\", nb2, SEED + 2000 + 10 * bi))\n    # per group within PRIMARY and within the 2015-17 cohort\n    for bn in [PRIMARY, BODY_COHORT]:\n        d = bodies[bn]\n        for gi, g in enumerate(GROUPS5 + [\"MATHDEC\"]):\n            dg = d[d.group5 == g]\n            if len(dg) >= 40:\n                tasks_t.append((f\"{bn}|group={g}|CONS_early_home\", dg, \"CONS_early_home\", nbg, SEED + 3000 + gi,\n                                True))\n    logger.info(f\"B: {len(tasks_t)} trait tasks + {len(tasks_v)} volume tasks on {W} workers\")\n    rt = run_tasks(tasks_t, task_trait, W)\n    rv = run_tasks(tasks_v, task_volume, W)\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_boot_primary\": nb, \"n_boot_secondary\": nb2,\n           \"n_boot_group\": nbg, \"covariates\": \"rank(B5) + onset-year dummies + 8-group dummies + body dummies \"\n           \"(pooled) + window_flag (2015-17 cohort)\", \"primary_body\": PRIMARY, \"replication_body\": BODY_COHORT,\n           \"EMB_note\": \"EMB_* = analogue (backbone PMI), not Cheng's word2vec measure\",\n           \"trait\": {r[\"task\"]: r for r in rt}, \"volume\": {r[\"task\"]: r for r in rv}}\n    # DL over groups (primary trait) for each outcome and the paired diffs\n    res[\"DL\"] = {}\n    for bn in [PRIMARY, BODY_COHORT]:\n        res[\"DL\"][bn] = {}\n        keys = OUTS + [\"O1c-O2r_m50\", \"O1c-O2r_resid\"]\n        for y in keys:\n            bs, ss, per = [], [], {}\n            for g in GROUPS5:\n                r = res[\"trait\"].get(f\"{bn}|group={g}|CONS_early_home\")\n                if r is None:\n                    continue\n                v = r[\"psp\"][y] if y in r[\"psp\"] else r[\"paired_diff\"][y]\n                per[g] = {\"rho\": v[\"rho\"], \"ci\": v[\"ci\"], \"n\": v.get(\"n\", v.get(\"n_common\"))}\n                bs.append(v[\"rho\"] if v[\"rho\"] is not None else np.nan)\n                ss.append(v[\"se\"] if v[\"se\"] is not None else np.nan)\n            dl = dersimonian_laird(bs, ss)\n            dl[\"n_negative\"] = int(sum(1 for b in bs if np.isfinite(b) and b < 0))\n            dl[\"n_positive\"] = int(sum(1 for b in bs if np.isfinite(b) and b > 0))\n            dl[\"per_group\"] = per\n            m = res[\"trait\"].get(f\"{bn}|group=MATHDEC|CONS_early_home\")\n            if m is not None:\n                dl[\"MATHDEC_report_only\"] = (m[\"psp\"][y] if y in m[\"psp\"] else m[\"paired_diff\"][y])[\"rho\"]\n            res[\"DL\"][bn][y] = dl\n    # cohort rungs R2 / R3 (EXP10 ladder)\n    try:\n        import ladder\n        dc = bodies[BODY_COHORT].copy()\n        res[\"cohort_rungs\"] = {}\n        for rung in [\"R2\", \"R3\"]:\n            for y in [\"O2r_m50\", \"O2r_resid\", \"O1c\", \"O3\"]:\n                r = ladder.psp_df(dc, \"CONS_early_home\", y, rung, 200 if quick else 1000, SEED + 4000,\n                                  direction=1 if y == \"O1c\" else -1)\n                r.pop(\"boot\", None)\n                res[\"cohort_rungs\"][f\"{rung}|{y}\"] = r\n    except (ImportError, KeyError, ValueError) as e:\n        res[\"cohort_rungs\"] = {\"error\": repr(e)[:300]}\n    # cohort MDE for the P3 test\n    c = res[\"trait\"][f\"{BODY_COHORT}|CONS_early_home\"][\"psp\"][\"O2r_m50\"]\n    res[\"cohort_MDE_O2r_m50\"] = {\"n\": c.get(\"n\"), \"se\": c.get(\"se\"), \"MDE_2.8SE\": mde(c.get(\"se\"))}\n    jdump(res, RES / (\"cheng_static_quick.json\" if quick else \"cheng_static.json\"))\n    p = res[\"trait\"][f\"{PRIMARY}|CONS_early_home\"]\n    logger.info(f\"B primary: \" + \", \".join(f\"{y} {p['psp'][y]['rho']:+.3f} {np.round(p['psp'][y]['ci'], 3)}\"\n                                          for y in OUTS))\n    logger.info(f\"B primary diff O1c-O2r_m50 {p['paired_diff']['O1c-O2r_m50']}\")\n    logger.info(f\"B volume primary {res['volume'][f'{PRIMARY}|volume']}\")\n    logger.info(f\"S4 done in {(time.time() - t) / 60:.1f} min\")\n    return res\n\n\n# ----------------------------------------------------------------------------- test D (Palla)\ndef cr(v: np.ndarray) -> np.ndarray:\n    r = rankdata(v) / len(v)\n    return r - r.mean()\n\n\ndef palla_fit(d: pd.DataFrame, y: str, i: np.ndarray | None = None) -> float:\n    x, s, yy = d.CONS_early_home.to_numpy(float), d.logvol.to_numpy(float), d[y].to_numpy(float)\n    other = d[[\"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]].to_numpy(float)\n    _, C = design(d)\n    if i is not None:\n        x, s, yy, other, C = x[i], s[i], yy[i], other[i], C[i]\n    C = C[:, C.std(0) > 0]\n    rx, rs = cr(x), cr(s)\n    Z = np.column_stack([np.ones(len(x)), rx, rs, rx * rs, rankdata(other, axis=0) / len(x), C])\n    beta, *_ = np.linalg.lstsq(Z, cr(yy), rcond=None)\n    return float(beta[3]), float(beta[1])\n\n\ndef task_palla(args) -> dict:\n    name, d, y, n_boot, seed = args\n    d = d[np.isfinite(d.CONS_early_home) & np.isfinite(d[y]) & d[B5].notna().all(1)].reset_index(drop=True)\n    n = len(d)\n    est, main = palla_fit(d, y)\n    rng = np.random.default_rng(seed)\n    bs = np.array([palla_fit(d, y, rng.integers(0, n, n)) for _ in range(n_boot)])\n    out = {\"task\": name, \"y\": y, \"n\": n, \"interaction\": summ(est, bs[:, 0], direction=1),\n           \"main_rank_CONS\": summ(main, bs[:, 1], direction=-1)}\n    # psp by early-size tercile\n    q = np.quantile(d.logvol, [1 / 3, 2 / 3])\n    terc = np.digitize(d.logvol, q)\n    out[\"by_size_tercile\"] = {}\n    for k, lab in enumerate([\"small\", \"medium\", \"large\"]):\n        dk = d[terc == k]\n        B, C = design(dk)\n        r = multi_boot(dk[[\"CONS_early_home\"]].to_numpy(float), dk[[y]].to_numpy(float), B, C, n_boot, seed + 7 + k)\n        out[\"by_size_tercile\"][lab] = {**summ(r[\"est\"][0, 0], r[\"boot\"][:, 0, 0]), \"n\": r[\"n\"],\n                                       \"logvol_range\": [float(dk.logvol.min()), float(dk.logvol.max())]}\n    return out\n\n\ndef run_D(logger, quick: bool = False) -> dict:\n    df = pd.read_parquet(DATA / \"static_analysis_table.parquet\")\n    bodies = body_frames(df)\n    nb = 100 if quick else 1000\n    tasks = [(f\"{bn}|{y}\", bodies[bn], y, nb, SEED + 5000 + 10 * k + j)\n             for k, bn in enumerate([PRIMARY, BODY_COHORT]) for j, y in enumerate([\"O3\", \"O2r_m50\", \"O1c\"])]\n    rs = run_tasks(tasks, task_palla, n_workers())\n    res = {\"label\": SELECTION_LABEL, \"model\": \"OLS on centred ranks/n: rank O ~ rank CONS_early + rank logvol + \"\n           \"product + rank(other B5) + onset-year/group/body dummies; concept bootstrap\",\n           \"palla_prediction\": \"interaction on O3 (transience) > 0: stability helps small concepts survive, turnover \"\n           \"helps large ones\", \"results\": {r[\"task\"]: r for r in rs}}\n    jdump(res, RES / (\"palla_quick.json\" if quick else \"palla.json\"))\n    for r in rs:\n        logger.info(f\"D {r['task']}: interaction {r['interaction']['rho']:+.4f} {r['interaction']['ci']}\")\n    return res\n\n\n# ----------------------------------------------------------------------------- test E (coupling)\ndef task_coupling(args) -> dict:\n    name, d, n_boot, seed = args\n    B, C = design(d)\n    X = d[[\"CONS_early_all\", \"CONS_early_home\"]].to_numpy(float)\n    out = {\"task\": name}\n    for tag, ys in ((\"reach_set\", [\"O2r_m50\", \"O1c\"]), (\"full_set\", [\"O1c\"])):\n        r = multi_boot(X, d[ys].to_numpy(float), B, C, n_boot, seed)\n        for j, y in enumerate(ys):\n            e = r[\"est\"][0, j] - r[\"est\"][1, j]\n            bs = r[\"boot\"][:, 0, j] - r[\"boot\"][:, 1, j]\n            out[f\"{tag}|{y}\"] = {\"n_common\": r[\"n\"], \"psp_all\": float(r[\"est\"][0, j]),\n                                 \"psp_home\": float(r[\"est\"][1, j]), \"diff_all_minus_home\": summ(e, bs, direction=1)}\n    return out\n\n\ndef run_E(logger, quick: bool = False) -> dict:\n    df = pd.read_parquet(DATA / \"static_analysis_table.parquet\")\n    bodies = body_frames(df)\n    nb = 100 if quick else N_BOOT_STATIC\n    tasks = [(bn, bodies[bn], nb, SEED + 6000 + k) for k, bn in enumerate([PRIMARY, BODY_COHORT, \"DEV\",\n                                                                          \"OLD_HELDOUT\", \"COHORT_2010_14\"])]\n    rs = run_tasks(tasks, task_coupling, n_workers())\n    res = {\"label\": SELECTION_LABEL, \"test\": \"paired concept bootstrap psp(CONS_early_all) - psp(CONS_early_home), \"\n           \"common complete-case set\", \"results\": {r[\"task\"]: r for r in rs}}\n    jdump(res, RES / (\"coupling_quick.json\" if quick else \"coupling.json\"))\n    for r in rs:\n        logger.info(f\"E {r['task']}: \" + \"; \".join(f\"{k} {v['diff_all_minus_home']['rho']:+.3f} \"\n                                                  f\"{np.round(v['diff_all_minus_home']['ci'], 3)}\"\n                                                  for k, v in r.items() if k != \"task\"))", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-30 02:11:03 UTC

```
Check python packages and upstream data:
python3 -c "import igraph, snowballstemmer, pyfixest, loguru; print('ok')"; python3 -c "import pandas, numpy, scipy; print(pandas.__version__, numpy.__version__, scipy.__version__)"; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long | head; du -sh /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long; sed -n 25,60p /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/ego.py; sed -n 100,116p /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib/ego.py
```

### [25] TOOL RESULT — Bash · 2026-09-30 02:11:05 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'igraph'\n2.3.3 2.2.6 1.16.3\npart_001.parquet\npart_002.parquet\npart_003.parquet\npart_004.parquet\npart_005.parquet\npart_006.parquet\n126M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\nC: dict = {}\n\n\ndef slice_of(y: int) -> int:\n    for i, (a, b) in enumerate(SLICES):\n        if a <= y <= b:\n            return i\n    return 0 if y < SLICES[0][0] else len(SLICES) - 1\n\n\ndef rq1_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0], \"W2\": [t0 + 1], \"W3\": [t0 + 2]}\n\n\ndef exp3_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0, t0 + 1], \"W2\": [t0 + 2], \"W3\": [t0 + 3, t0 + 4]}\n\n\ndef lgC(n: float, k: float) -> float:\n    from scipy.special import gammaln\n    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)\n\n\ndef set_context(ctx: dict) -> None:\n    \"\"\"ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,\n    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable).\"\"\"\n    C.clear()\n    C.update(ctx)\n    C[\"graphs\"] = {}\n    C[\"yidx\"] = {y: i for i, y in enumerate(ctx[\"years\"])}\n\n\ndef knn_graph(s: int) -> ig.Graph:\n    if s not in C[\"graphs\"]:\n    order = idx[np.lexsort((-p[idx], -nck[idx]))][:top]\n    return float(np.mean(p[order])), len(order)\n\n\ndef self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:\n    lem = C[\"lemmas\"]\n    sets = []\n    for ph in [name] + aliases:\n        cl = {l for l in lem(ph) if C[\"ldf\"].get(l, 0) <= SELF_DF_MAX}\n        if cl:\n            sets.append(cl)\n    lex = np.array([any(cl <= tl for cl in sets) for tl in C[\"tlem\"]])\n    share = n_early / nc_early if nc_early else np.zeros(C[\"nt\"])\n    return lex | (share >= SELF_SHARE)\n\n\ndef distinct_null(pool_idx, w, M, labels, rng, n):", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-30 02:11:17 UTC

```
Create scratch venv for data extraction:
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad; mkdir -p $S; cd $S && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --python /usr/local/bin/python3.12 $S/xenv && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $S/xenv/bin/python pandas==2.3.3 numpy scipy pyarrow igraph snowballstemmer loguru 2>&1 | tail -3; $S/xenv/bin/python -c "import igraph, snowballstemmer; print('ok')"
```

### [27] TOOL RESULT — Bash · 2026-09-30 02:11:21 UTC

```
{"stdout": "ok", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] ASSISTANT · 2026-09-30 02:11:25 UTC

```
Writing the extraction script that builds `mini_demo_data.json` (100 concepts, with raw per-year topic vectors).
```

### [29] TOOL CALL — Bash · 2026-09-30 02:11:25 UTC

```
Read headline numbers and frame header:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $W/results/headline_numbers.json; head -3 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv
```

### [30] TOOL RESULT — Bash · 2026-09-30 02:11:25 UTC

```
{"stdout": "{\n \"label\": \"selection data, not confirmation\",\n \"numbers\": {\n  \"cheng_panel_models.json:builds.HOME.joint.A1.n_concepts\": 12311,\n  \"cheng_panel_models.json:builds.HOME.joint.A1.n_rows\": 105839,\n  \"cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS.b\": 0.42844875149581085,\n  \"cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS.pct_per_sd\": 0.534874703764965,\n  \"cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS.pct_per_sd\": 0.8310134412961416,\n  \"cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS.pct_ci\": [\n   0.7061383262187568,\n   0.9650283747141353\n  ],\n  \"cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS.pct_per_sd\": 0.01267281109684637,\n  \"cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS.pct_ci\": [\n   0.004507033106396552,\n   0.020904969837247656\n  ],\n  \"cheng_panel_models.json:builds.HOME.joint.ratio_boot.ratio\": 0.02081966579806125,\n  \"cheng_panel_models.json:builds.HOME.joint.ratio_boot.ratio_ci\": [\n   0.009042373304763021,\n   0.035263909109610046\n  ],\n  \"cheng_panel_models.json:builds.HOME.joint.A3.coef.zCONS.pct_per_sd\": 0.013650621232445426,\n  \"cheng_panel_models.json:builds.ALL.joint.ratio_boot.ratio\": 0.02440911703216719,\n  \"cheng_static.json:volume.EXP5_pooled|volume.B_raw_spearman_V_t0p3.rho\": 0.2563712518701778,\n  \"cheng_static.json:volume.EXP5_pooled|volume.B_raw_spearman_V_t0p3.ci\": [\n   0.23921330023442366,\n   0.27389032248349954\n  ],\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O2r_m50.rho\": -0.0693013812628014,\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O2r_m50.ci\": [\n   -0.09288056610535206,\n   -0.04668336498751107\n  ],\n  \"cheng_static.json:DL.EXP5_pooled.O2r_m50.b\": -0.07859604430871031,\n  \"cheng_static.json:DL.EXP5_pooled.O2r_m50.I2\": 0.0,\n  \"cheng_static.json:DL.EXP5_pooled.O2r_m50.n_negative\": 5,\n  \"cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.rho\": -0.11103014804768521,\n  \"cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.ci\": [\n   -0.19728438257060163,\n   -0.030301558125793968\n  ],\n  \"cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.n\": 615,\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O1c.rho\": -0.00031746728758710543,\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O1c.ci\": [\n   -0.01884882260240145,\n   0.017447304434020514\n  ],\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O3.rho\": -0.0005121127935191378,\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O3.ci\": [\n   -0.019918268683094018,\n   0.017313010786273893\n  ],\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.paired_diff.O1c-O2r_m50.rho\": 0.034599704092448426,\n  \"cheng_static.json:trait.EXP5_pooled|CONS_early_home.paired_diff.O1c-O2r_m50.ci\": [\n   0.003522947741278198,\n   0.06608571140699572\n  ],\n  \"cheng_static.json:DL.EXP5_pooled.O1c-O2r_m50.ci\": [\n   -0.008575753562913034,\n   0.08271703404599004\n  ],\n  \"identity_check.json:by_body.EXP5_pooled.jaccard_exp11_early.rho\": 0.7669421825423538,\n  \"panel_C.json:C1.coef.zCONS.pct_per_sd\": 0.0252668282237698,\n  \"panel_C.json:C1.boot.ci\": [\n   0.0035054524164536993,\n   0.0478451849161699\n  ],\n  \"palla.json:results.EXP5_pooled|O3.interaction.rho\": -0.0008563755582464466,\n  \"palla.json:results.EXP5_pooled|O3.interaction.ci\": [\n   -0.021279512359615185,\n   0.020030842072367914\n  ]\n }\n}ci,concept_id,qid,name,level,aliases_used,t0,newborn,home,n_home,weak_home,intersect40,intersect25,home_top_share,group,split,precision_c,n_labelled_prec,precision_source,label_coverage_early,tag_coverage,early_volume,in_P78\n3,37253,Q5156502,Complete intersection,2,,2012,False,26,30.0,0,0,0,0.8933333333333333,MATHDEC,COHORT,1.0,10.0,llm,0.9583333134651184,0.5901639461517334,72.0,0\n4,39854,Q84115,Torque converter,3,,2004,False,22,30.0,0,0,0,1.0,Eng,DEV,0.9,10.0,llm,0.84375,0.8648648858070374,64.0,0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Write · 2026-09-30 02:11:53 UTC

```
File: /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/make_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json for code_demo.ipynb: 100 EXP5 frame concepts (stratified over the 8 field groups and
the 3 EXP5 bodies), each carrying
  * its static row of data/static_analysis_table.parquet (B5 baseline, outcomes, V(t0+2), V(t0+3), CONS_early_home)
  * its raw HOME-build neighbour topic co-usage vectors v_t (self topics removed) for t0..min(t0+10, 2022), built with
    the artifact's own lib/cheng.py + lib/ego.py code (so the notebook can recompute CONS(t) = cos(v_{t-1}, v_t))
  * the per-year HOME EMB / SOC / CONS reference values from data/cheng_features.parquet
  * the yearly grounded volume V(t), t0..t0+11
plus the full-run headline numbers (results/headline_numbers.json) for comparison.

Reads the source artifact read-only (ART below); writes only mini_demo_data.json next to this script.
Run with a Python that has pandas, pyarrow, scipy, igraph, snowballstemmer, loguru."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
ART = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14")
sys.path.insert(0, str(ART / "lib"))

import cheng  # noqa: E402
import ego  # noqa: E402
from common import B5, DEPTH, EXP5, EXP11, REACH, home_codes  # noqa: E402

N_PICK = 100
SEED = 20260929


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, np.ndarray):
        return clean(o.tolist())
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if not math.isfinite(float(o)) else round(float(o), 6)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


def main() -> None:
    st = pd.read_parquet(ART / "data/static_analysis_table.parquet")
    st = st[st.body.isin(["DEV", "OLD_HELDOUT", "COHORT_2010_14"])]
    ok = st[B5 + REACH + DEPTH + ["CONS_early_home", "V_t0p2", "V_t0p3"]].notna().all(1)
    st = st[ok].copy()
    # stratified pick: equal share per group (8 groups), within group spread over bodies
    rng = np.random.default_rng(SEED)
    groups = sorted(st.group.unique())
    per = {g: N_PICK // len(groups) + (1 if i < N_PICK % len(groups) else 0) for i, g in enumerate(groups)}
    pick = []
    for g in groups:
        sg = st[st.group == g]
        pick.extend(rng.choice(sg.ci.to_numpy(), per[g], replace=False).tolist())
    st = st[st.ci.isin(pick)].sort_values("ci").reset_index(drop=True)
    print("picked", len(st), st.group.value_counts().to_dict(), st.body.value_counts().to_dict())

    fr = pd.read_csv(EXP5 / "frame_concepts.csv").set_index("ci")
    feat = pd.read_parquet(ART / "data/cheng_features.parquet")
    feat = feat[(feat.body_src == "EXP5") & (feat.build == "HOME") & feat.ci.isin(pick)]
    V = pd.read_parquet(ART / "data/V_exp5.parquet", columns=["ci", "year", "V"])
    V = V[V.ci.isin(pick)]

    cheng.init_context()
    nt = ego.C["nt"]
    tab = pa.concat_tables([pq.read_table(p, columns=["ci", "year", "vfield", "topics", "authors"])
                            for p in sorted((EXP11 / "data/frame_matches_long").glob("part_*.parquet"))])
    tab = tab.filter(pc.is_in(tab.column("ci"), value_set=pa.array(np.asarray(pick, np.int32))))
    df_long = tab.to_pandas()

    examples = []
    max_dev = 0.0
    for r in st.itertuples():
        ci, t0 = int(r.ci), int(r.t0)
        f = fr.loc[ci]
        y_hi = int(min(t0 + 10, 2022))
        rows = df_long[(df_long.ci == ci) & (df_long.year >= t0 - 3) & (df_long.year <= y_hi)].sort_values("year")
        years, vfield, t_off, tflat, a_off, aflat = cheng.pack(rows)
        home = home_codes(f.home)
        aliases = [a for a in str(f.aliases_used).split("|") if a and a != "nan"]
        # --- verbatim steps of cheng.concept_measures up to the HOME neighbour vectors
        Y = np.arange(t0 - 3, y_hi + 1)
        iy = {int(y): i for i, y in enumerate(Y)}
        is_home = np.isin(vfield, list(home)) if home else np.zeros(len(years), bool)
        cA, ncA = cheng._year_vectors(years, t_off, tflat, np.ones(len(years), bool), Y, nt)
        cH, ncH = cheng._year_vectors(years, t_off, tflat, is_home, Y, nt)
        e_idx = [iy[y] for y in (t0, t0 + 1, t0 + 2) if y in iy]
        SELF = ego.self_topics(str(f["name"]), aliases, cA[e_idx].sum(0), float(ncA[e_idx].sum()))
        keep = ~SELF
        vec = {}
        for t in range(t0, y_hi + 1):
            v = cH[iy[t]] * keep
            nz = np.nonzero(v)[0]
            vec[str(t)] = {"n_papers": int(ncH[iy[t]]), "topics": nz.tolist(), "counts": v[nz].astype(int).tolist()}
        # self-check: recompute CONS with cheng.cons and compare with the artifact's stored value
        fc = feat[feat.ci == ci].set_index("year")
        for t in range(t0 + 1, y_hi + 1):
            c, _ = cheng.cons(cH[iy[t - 1]] * keep, cH[iy[t]] * keep, int(ncH[iy[t - 1]]), int(ncH[iy[t]]))
            ref = fc.CONS.get(t, np.nan)
            if np.isfinite(c) or np.isfinite(ref):
                max_dev = max(max_dev, abs(c - ref) if np.isfinite(c) and np.isfinite(ref) else 1.0)
        vy = V[V.ci == ci].set_index("year").V
        panel = {str(t): {"V": float(vy.get(t, 0.0)),
                          "CONS_ref": fc.CONS.get(t, np.nan), "EMB": fc.EMB.get(t, np.nan),
                          "SOC": fc.SOC.get(t, np.nan)} for t in range(t0, min(t0 + 11, 2022) + 1)}
        ex = {"input": f"{r.name} | ci={ci} | t0={t0} | group={r.group} | body={r.body}",
              "output": f"{r.O2r_m50:.4f}",
              "ci": ci, "name": r.name, "t0": t0, "group": r.group, "group5": r.group5, "body": r.body,
              "window_flag": int(r.window_flag), "V_t0p2": r.V_t0p2, "V_t0p3": r.V_t0p3,
              **{k: getattr(r, k) for k in B5 + REACH + DEPTH},
              "CONS_early_home_ref": r.CONS_early_home,
              "home_vectors": vec, "panel": panel}
        examples.append(ex)
    print(f"max |CONS recomputed - stored| = {max_dev:.2e}")
    head = json.loads((ART / "results/headline_numbers.json").read_text())["numbers"]
    out = {"metadata": {
        "description": "100 EXP5 frame concepts (stratified over 8 field groups) for the Cheng ideational-"
                       "consistency demo: raw HOME neighbour topic co-usage vectors per year, yearly volume V(t), "
                       "per-year EMB/SOC, B5 baseline covariates and reach/depth outcomes",
        "label": "selection data, not confirmation", "n_topics_vocab": int(nt), "seed": SEED,
        "full_run_headline_numbers": head},
        "datasets": [{"dataset": "cheng_demo_concepts", "examples": examples}]}
    p = HERE / "mini_demo_data.json"
    p.write_text(json.dumps(clean(out), separators=(",", ":")))
    print("wrote", p, p.stat().st_size / 1e6, "MB")


if __name__ == "__main__":
    main()
```

### [32] TOOL RESULT — Write · 2026-09-30 02:11:53 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/make_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json for code_demo.ipynb: 100 EXP5 frame concepts (stratified over the 8 field groups and\nthe 3 EXP5 bodies), each carrying\n  * its static row of data/static_analysis_table.parquet (B5 baseline, outcomes, V(t0+2), V(t0+3), CONS_early_home)\n  * its raw HOME-build neighbour topic co-usage vectors v_t (self topics removed) for t0..min(t0+10, 2022), built with\n    the artifact's own lib/cheng.py + lib/ego.py code (so the notebook can recompute CONS(t) = cos(v_{t-1}, v_t))\n  * the per-year HOME EMB / SOC / CONS reference values from data/cheng_features.parquet\n  * the yearly grounded volume V(t), t0..t0+11\nplus the full-run headline numbers (results/headline_numbers.json) for comparison.\n\nReads the source artifact read-only (ART below); writes only mini_demo_data.json next to this script.\nRun with a Python that has pandas, pyarrow, scipy, igraph, snowballstemmer, loguru.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nimport pyarrow as pa\nimport pyarrow.compute as pc\nimport pyarrow.parquet as pq\n\nHERE = Path(__file__).resolve().parent\nART = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14\")\nsys.path.insert(0, str(ART / \"lib\"))\n\nimport cheng  # noqa: E402\nimport ego  # noqa: E402\nfrom common import B5, DEPTH, EXP5, EXP11, REACH, home_codes  # noqa: E402\n\nN_PICK = 100\nSEED = 20260929\n\n\ndef clean(o):\n    if isinstance(o, dict):\n        return {str(k): clean(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [clean(v) for v in o]\n    if isinstance(o, np.ndarray):\n        return clean(o.tolist())\n    if isinstance(o, np.integer):\n        return int(o)\n    if isinstance(o, (np.floating, float)):\n        return None if not math.isfinite(float(o)) else round(float(o), 6)\n    if isinstance(o, np.bool_):\n        return bool(o)\n    return o\n\n\ndef main() -> None:\n    st = pd.read_parquet(ART / \"data/static_analysis_table.parquet\")\n    st = st[st.body.isin([\"DEV\", \"OLD_HELDOUT\", \"COHORT_2010_14\"])]\n    ok = st[B5 + REACH + DEPTH + [\"CONS_early_home\", \"V_t0p2\", \"V_t0p3\"]].notna().all(1)\n    st = st[ok].copy()\n    # stratified pick: equal share per group (8 groups), within group spread over bodies\n    rng = np.random.default_rng(SEED)\n    groups = sorted(st.group.unique())\n    per = {g: N_PICK // len(groups) + (1 if i < N_PICK % len(groups) else 0) for i, g in enumerate(groups)}\n    pick = []\n    for g in groups:\n        sg = st[st.group == g]\n        pick.extend(rng.choice(sg.ci.to_numpy(), per[g], replace=False).tolist())\n    st = st[st.ci.isin(pick)].sort_values(\"ci\").reset_index(drop=True)\n    print(\"picked\", len(st), st.group.value_counts().to_dict(), st.body.value_counts().to_dict())\n\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\").set_index(\"ci\")\n    feat = pd.read_parquet(ART / \"data/cheng_features.parquet\")\n    feat = feat[(feat.body_src == \"EXP5\") & (feat.build == \"HOME\") & feat.ci.isin(pick)]\n    V = pd.read_parquet(ART / \"data/V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    V = V[V.ci.isin(pick)]\n\n    cheng.init_context()\n    nt = ego.C[\"nt\"]\n    tab = pa.concat_tables([pq.read_table(p, columns=[\"ci\", \"year\", \"vfield\", \"topics\", \"authors\"])\n                            for p in sorted((EXP11 / \"data/frame_matches_long\").glob(\"part_*.parquet\"))])\n    tab = tab.filter(pc.is_in(tab.column(\"ci\"), value_set=pa.array(np.asarray(pick, np.int32))))\n    df_long = tab.to_pandas()\n\n    examples = []\n    max_dev = 0.0\n    for r in st.itertuples():\n        ci, t0 = int(r.ci), int(r.t0)\n        f = fr.loc[ci]\n        y_hi = int(min(t0 + 10, 2022))\n        rows = df_long[(df_long.ci == ci) & (df_long.year >= t0 - 3) & (df_long.year <= y_hi)].sort_values(\"year\")\n        years, vfield, t_off, tflat, a_off, aflat = cheng.pack(rows)\n        home = home_codes(f.home)\n        aliases = [a for a in str(f.aliases_used).split(\"|\") if a and a != \"nan\"]\n        # --- verbatim steps of cheng.concept_measures up to the HOME neighbour vectors\n        Y = np.arange(t0 - 3, y_hi + 1)\n        iy = {int(y): i for i, y in enumerate(Y)}\n        is_home = np.isin(vfield, list(home)) if home else np.zeros(len(years), bool)\n        cA, ncA = cheng._year_vectors(years, t_off, tflat, np.ones(len(years), bool), Y, nt)\n        cH, ncH = cheng._year_vectors(years, t_off, tflat, is_home, Y, nt)\n        e_idx = [iy[y] for y in (t0, t0 + 1, t0 + 2) if y in iy]\n        SELF = ego.self_topics(str(f[\"name\"]), aliases, cA[e_idx].sum(0), float(ncA[e_idx].sum()))\n        keep = ~SELF\n        vec = {}\n        for t in range(t0, y_hi + 1):\n            v = cH[iy[t]] * keep\n            nz = np.nonzero(v)[0]\n            vec[str(t)] = {\"n_papers\": int(ncH[iy[t]]), \"topics\": nz.tolist(), \"counts\": v[nz].astype(int).tolist()}\n        # self-check: recompute CONS with cheng.cons and compare with the artifact's stored value\n        fc = feat[feat.ci == ci].set_index(\"year\")\n        for t in range(t0 + 1, y_hi + 1):\n            c, _ = cheng.cons(cH[iy[t - 1]] * keep, cH[iy[t]] * keep, int(ncH[iy[t - 1]]), int(ncH[iy[t]]))\n            ref = fc.CONS.get(t, np.nan)\n            if np.isfinite(c) or np.isfinite(ref):\n                max_dev = max(max_dev, abs(c - ref) if np.isfinite(c) and np.isfinite(ref) else 1.0)\n        vy = V[V.ci == ci].set_index(\"year\").V\n        panel = {str(t): {\"V\": float(vy.get(t, 0.0)),\n                          \"CONS_ref\": fc.CONS.get(t, np.nan), \"EMB\": fc.EMB.get(t, np.nan),\n                          \"SOC\": fc.SOC.get(t, np.nan)} for t in range(t0, min(t0 + 11, 2022) + 1)}\n        ex = {\"input\": f\"{r.name} | ci={ci} | t0={t0} | group={r.group} | body={r.body}\",\n              \"output\": f\"{r.O2r_m50:.4f}\",\n              \"ci\": ci, \"name\": r.name, \"t0\": t0, \"group\": r.group, \"group5\": r.group5, \"body\": r.body,\n              \"window_flag\": int(r.window_flag), \"V_t0p2\": r.V_t0p2, \"V_t0p3\": r.V_t0p3,\n              **{k: getattr(r, k) for k in B5 + REACH + DEPTH},\n              \"CONS_early_home_ref\": r.CONS_early_home,\n              \"home_vectors\": vec, \"panel\": panel}\n        examples.append(ex)\n    print(f\"max |CONS recomputed - stored| = {max_dev:.2e}\")\n    head = json.loads((ART / \"results/headline_numbers.json\").read_text())[\"numbers\"]\n    out = {\"metadata\": {\n        \"description\": \"100 EXP5 frame concepts (stratified over 8 field groups) for the Cheng ideational-\"\n                       \"consistency demo: raw HOME neighbour topic co-usage vectors per year, yearly volume V(t), \"\n                       \"per-year EMB/SOC, B5 baseline covariates and reach/depth outcomes\",\n        \"label\": \"selection data, not confirmation\", \"n_topics_vocab\": int(nt), \"seed\": SEED,\n        \"full_run_headline_numbers\": head},\n        \"datasets\": [{\"dataset\": \"cheng_demo_concepts\", \"examples\": examples}]}\n    p = HERE / \"mini_demo_data.json\"\n    p.write_text(json.dumps(clean(out), separators=(\",\", \":\")))\n    print(\"wrote\", p, p.stat().st_size / 1e6, \"MB\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [33] TOOL CALL — Bash · 2026-09-30 02:11:57 UTC

```
Run extraction script:
time /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/xenv/bin/python -B make_mini_demo_data.py
```

### [34] TOOL RESULT — Bash · 2026-09-30 02:12:03 UTC

```
{"stdout": "picked 100 {'BGM': 13, 'LIFEENV': 13, 'Eng': 13, 'CS': 13, 'SOC': 12, 'MATHDEC': 12, 'PHYS': 12, 'Med': 12} {'OLD_HELDOUT': 40, 'DEV': 34, 'COHORT_2010_14': 26}\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json 0.327613 MB\n\nreal\t0m6.007s\nuser\t0m3.893s\nsys\t0m0.367s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] ASSISTANT · 2026-09-30 02:12:09 UTC

```
Data built (CONS recomputation matches the artifact exactly). Now checking whether `pyfixest` installs alongside Colab's pinned packages.
```

### [36] TOOL CALL — Bash · 2026-09-30 02:12:09 UTC

```
Test pyfixest install against Colab pins:
E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && time $E/bin/python -m pip install -q numpy==2.0.2 pandas==2.2.2 scipy==1.16.3 matplotlib==3.10.0 statsmodels==0.14.6 pyarrow==18.1.0 2>&1 | tail -2; time $E/bin/python -m pip install -q pyfixest==0.60.0 2>&1 | tail -5; $E/bin/python -m pip list 2>/dev/null | grep -iE "numpy|scipy|pandas|pyfixest|polars|narwhals|numba|formulaic|jax"
```

### [37] TOOL RESULT — Bash · 2026-09-30 02:12:47 UTC

```
{"stdout": "real\t0m21.944s\nuser\t0m16.773s\nsys\t0m1.302s\n\nreal\t0m11.248s\nuser\t0m3.216s\nsys\t0m0.306s\nformulaic                 1.2.2\nnarwhals                  2.26.0\nnumpy                     2.0.2\npandas                    2.2.2\npyfixest                  0.60.0\nscipy                     1.16.3", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-30 02:12:49 UTC

```
Smoke test pyfixest fepois:
E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924; $E/bin/python -c "
import pyfixest as pf, numpy as np, pandas as pd
rng=np.random.default_rng(0); n=500
d=pd.DataFrame({'x':rng.normal(size=n),'g':rng.integers(0,5,n),'ci':rng.integers(0,50,n)}); d['y']=rng.poisson(np.exp(0.3*d.x))
f=pf.fepois('y ~ x | g', data=d, vcov={'CRV1':'ci'}); print(f.coef(), f._N)
"; $E/bin/python -m pip show pyfixest | grep -i requires
```

### [39] TOOL RESULT — Bash · 2026-09-30 02:12:53 UTC

```
{"stdout": "Coefficient\nx    0.270263\nName: Estimate, dtype: float64 500\nRequires: formulaic, joblib, maketables, narwhals, numpy, pandas, scipy, seaborn, tabulate, tqdm", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-09-30 02:13:27 UTC

```
Now building the notebook (generated from a builder script so the original functions are copied verbatim).
```

### [41] TOOL CALL — Bash · 2026-09-30 02:13:27 UTC

```
Look at identity and verdict rules:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; sed -n 1,60p $W/lib/identity.py; grep -n "verdict\|SIZE-DOM\|REVERSAL" $W/lib/outputs.py | head -30
```

### [42] TOOL RESULT — Bash · 2026-09-30 02:13:27 UTC

```
{"stdout": "\"\"\"S2: construct-identity check -- is Cheng's count-weighted consistency 'the same as' this run's older measures?\n\nSpearman of CONS_early_home (per body) with\n  * Exp11 unweighted Jaccard persistence (HOME PMI neighbours), mean over t0+1..t0+2        [EXP5 bodies only]\n  * EXP10 edge_persistence__home (static t0..t0+2 Jaccard)                                  [all bodies]\n  * -NOVCHURN_home, NOVCHURN_home = mean(z NOV_res_home, -z edge_persistence_home) with the EXP10 frozen\n    open_constants['home'] (winsorised at the frozen lo/hi, both components required)       [all bodies]\n  * log early volume (B5 logvol) and home degree (mean # non-self HOME topics over t0+1..t0+2)\nCIs: Fisher-z 95% (n - 3). This step reads NO outcome.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import BODY_COHORT, DATA, EXP8, EXP10, EXP11, RES, jdump, jload\n\n\ndef spear(a: np.ndarray, b: np.ndarray) -> dict:\n    ok = np.isfinite(a) & np.isfinite(b)\n    n = int(ok.sum())\n    if n < 20:\n        return {\"rho\": None, \"n\": n, \"ci\": [None, None]}\n    r = float(stats.spearmanr(a[ok], b[ok])[0])\n    z, se = math.atanh(max(min(r, 0.999999), -0.999999)), 1 / math.sqrt(n - 3)\n    return {\"rho\": r, \"n\": n, \"ci\": [math.tanh(z - 1.96 * se), math.tanh(z + 1.96 * se)]}\n\n\ndef novchurn(df: pd.DataFrame) -> np.ndarray:\n    k = jload(EXP10 / \"results/frozen_spec.json\")[\"open_constants\"][\"home\"]\n    zn = (np.clip(df.NOV_res__home.to_numpy(float), k[\"NOV_res\"][\"lo\"], k[\"NOV_res\"][\"hi\"]) - k[\"NOV_res\"][\"mu\"]) \\\n        / k[\"NOV_res\"][\"sd\"]\n    ep = k[\"edge_persistence\"]\n    ze = (np.clip(df.edge_persistence__home.to_numpy(float), ep[\"lo\"], ep[\"hi\"]) - ep[\"mu\"]) / ep[\"sd\"]\n    return (zn - ze) / 2.0\n\n\ndef load_static_covars() -> pd.DataFrame:\n    \"\"\"ci, logvol (B5) for both frames; EXP10 ego_open (edge persistence, NOV_res) for both frames.\"\"\"\n    a5 = pd.read_parquet(EXP8 / \"data/analysis_table.parquet\", columns=[\"ci\", \"logvol\"])\n    ac = pd.read_parquet(EXP10 / \"data/analysis_cohort.parquet\", columns=[\"ci\", \"logvol\"])\n    eo = pd.concat([pd.read_parquet(EXP10 / \"data/ego_open_exp5.parquet\",\n                                    columns=[\"ci\", \"edge_persistence__home\", \"NOV_res__home\"]).assign(src=\"EXP5\"),\n                    pd.read_parquet(EXP10 / \"data/ego_open_cohort.parquet\",\n                                    columns=[\"ci\", \"edge_persistence__home\", \"NOV_res__home\"]).assign(src=\"COH\")])\n    return pd.concat([a5, ac]), eo\n\n\ndef run(logger) -> dict:\n    st = pd.read_parquet(DATA / \"cheng_static.parquet\")\n    lv, eo = load_static_covars()\n    st5 = st[st.body != BODY_COHORT].merge(lv, on=\"ci\", how=\"left\").merge(\n        eo[eo.src == \"EXP5\"].drop(columns=\"src\"), on=\"ci\", how=\"left\")\n    stc = st[st.body == BODY_COHORT].merge(lv, on=\"ci\", how=\"left\").merge(\n        eo[eo.src == \"COH\"].drop(columns=\"src\"), on=\"ci\", how=\"left\")\n    yp = pd.read_parquet(EXP11 / \"data/yearly_panel.parquet\", columns=[\"ci\", \"year\", \"t0\", \"persistence\"])\n    yp = yp[(yp.year >= yp.t0 + 1) & (yp.year <= yp.t0 + 2)].groupby(\"ci\").persistence.mean().rename(\n        \"jaccard_exp11_early\").reset_index()\n1:\"\"\"S8: Holm over the declared family, the mechanical verdict (results/cheng_verdict.json), figures, method_out.json\n32:# ----------------------------------------------------------------------------- verdict\n33:def verdict() -> dict:\n75:        labels.append(\"REVERSAL CONFIRMED (on selection data)\")\n77:        labels.append(\"REVERSAL REPLICATED\")\n79:        labels.append(\"SIZE-DOMINATED\")\n84:        labels.append(\"NULL-REVERSAL\")\n85:    out = {\"label\": SELECTION_LABEL, \"verdicts\": labels, \"predictions\": pred,\n93:           \"rules\": jload(RES / \"frozen_spec.json\")[\"verdict_rules\"]}\n94:    jdump(out, RES / \"cheng_verdict.json\")\n289:    v = verdict()\n290:    logger.info(f\"VERDICT: {v['verdicts']}\")\n302:    J = {f: jload(RES / f) for f in [\"cheng_panel_models.json\", \"cheng_static.json\", \"cheng_verdict.json\",\n318:    P, S, Vd = \"cheng_panel_models.json\", \"cheng_static.json\", \"cheng_verdict.json\"\n361:    verdict_line = \", \".join(J[Vd][\"verdicts\"]) if Vd in J else \"n/a\"\n363:           f\"Frozen verdict (`results/cheng_verdict.json:verdicts`): **{verdict_line}** \"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Bash · 2026-09-30 02:13:29 UTC

```
Read verdict function:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; sed -n 32,95p $W/lib/outputs.py
```

### [44] TOOL RESULT — Bash · 2026-09-30 02:13:29 UTC

```
{"stdout": "# ----------------------------------------------------------------------------- verdict\ndef verdict() -> dict:\n    A = jload(RES / \"cheng_panel_models.json\")\n    S = jload(RES / \"cheng_static.json\")\n    C = jload(RES / \"panel_C.json\")\n    K = {}\n\n    def put(name, file, path, obj):\n        K[name] = {\"value\": g(obj, path), \"source\": f\"{file}:{path}\"}\n        return K[name][\"value\"]\n\n    a1 = put(\"A1_HOME_joint_zCONS\", \"cheng_panel_models.json\", \"builds.HOME.joint.A1.coef.zCONS\", A)\n    a2 = put(\"A2_HOME_joint_zCONS\", \"cheng_panel_models.json\", \"builds.HOME.joint.A2.coef.zCONS\", A)\n    rb = put(\"RATIO_HOME_joint\", \"cheng_panel_models.json\", \"builds.HOME.joint.ratio_boot\", A)\n    raw = put(\"B_raw_primary\", \"cheng_static.json\", f\"volume.{PRIMARY}|volume.B_raw_spearman_V_t0p3\", S)\n    p3 = put(\"P3_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.psp.O2r_m50\", S)\n    p4 = put(\"P4_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.psp.O3\", S)\n    p5 = put(\"P5_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.paired_diff.O1c-O2r_m50\", S)\n    rawc = put(\"B_raw_cohort\", \"cheng_static.json\", f\"volume.{BODY_COHORT}|volume.B_raw_spearman_V_t0p3\", S)\n    p3c = put(\"P3_cohort\", \"cheng_static.json\", f\"trait.{BODY_COHORT}|CONS_early_home.psp.O2r_m50\", S)\n    c1 = put(\"C1\", \"panel_C.json\", \"C1\", C)\n    # one-sided p-values in the predicted direction\n    p_a1 = float(stats.norm.sf(a1[\"b\"] / a1[\"se\"]))\n    fam = {\"P1-A1\": p_a1, \"P2\": rb[\"p_one_ratio_lt_0.5\"], \"P3\": p3[\"p_one_pred\"], \"P4\": p4[\"p_one_pred\"],\n           \"P5\": p5[\"p_one_pred\"]}\n    hp = dict(zip(fam, holm(list(fam.values()))))\n    pred = {\n        \"P1\": {\"holds\": bool(raw[\"rho\"] > 0 and raw[\"ci\"][0] > 0 and a1[\"b\"] > 0 and a1[\"ci\"][0] > 0),\n               \"raw_rho\": raw[\"rho\"], \"raw_ci\": raw[\"ci\"], \"A1_b\": a1[\"b\"], \"A1_ci\": a1[\"ci\"]},\n        \"P2\": {\"holds\": bool(rb[\"ratio_ci\"][1] < 0.5), \"ratio\": rb[\"ratio\"], \"ratio_ci\": rb[\"ratio_ci\"]},\n        \"P3\": {\"holds\": bool(p3[\"rho\"] < 0 and p3[\"ci\"][1] < 0), \"psp\": p3[\"rho\"], \"ci\": p3[\"ci\"]},\n        \"P4\": {\"holds\": bool(p4[\"rho\"] <= 0 and p4[\"ci\"][1] <= 0), \"psp\": p4[\"rho\"], \"ci\": p4[\"ci\"],\n               \"point_holds\": bool(p4[\"rho\"] <= 0)},\n        \"P5\": {\"holds\": bool(p5[\"rho\"] > 0 and p5[\"ci\"][0] > 0), \"diff\": p5[\"rho\"], \"ci\": p5[\"ci\"]},\n        \"P6\": {\"holds\": bool(c1[\"coef\"][\"zCONS\"][\"b\"] < 0 and c1[\"boot\"][\"ci\"][1] < 0),\n               \"b\": c1[\"coef\"][\"zCONS\"][\"b\"], \"boot_ci\": c1[\"boot\"][\"ci\"], \"crv1_ci\": c1[\"coef\"][\"zCONS\"][\"ci\"]},\n    }\n    confirmed = bool(raw[\"rho\"] > 0 and raw[\"ci\"][0] > 0 and p3[\"rho\"] < 0 and p3[\"ci\"][1] < 0)\n    n_c = p3c.get(\"n\") or 0\n    rep = bool(rawc[\"rho\"] is not None and rawc[\"rho\"] > 0 and rawc[\"ci\"][0] > 0 and p3c[\"rho\"] is not None\n               and p3c[\"rho\"] < 0 and (n_c < 600 or p3c[\"ci\"][1] < 0))\n    labels = []\n    if confirmed:\n        labels.append(\"REVERSAL CONFIRMED (on selection data)\")\n    if rep:\n        labels.append(\"REVERSAL REPLICATED\")\n    if pred[\"P2\"][\"holds\"]:\n        labels.append(\"SIZE-DOMINATED\")\n    if pred[\"P5\"][\"holds\"]:\n        labels.append(\"DEPTH-REACH SPLIT\")\n    null_rev = bool(p3[\"ci\"][0] <= 0 <= p3[\"ci\"][1])\n    if null_rev:\n        labels.append(\"NULL-REVERSAL\")\n    out = {\"label\": SELECTION_LABEL, \"verdicts\": labels, \"predictions\": pred,\n           \"holm_family_one_sided\": {k: {\"p\": fam[k], \"p_holm\": hp[k]} for k in fam},\n           \"replication\": {\"body\": BODY_COHORT, \"n\": n_c, \"raw\": rawc, \"psp_O2r_m50\": p3c,\n                           \"MDE_2.8SE\": S[\"cohort_MDE_O2r_m50\"][\"MDE_2.8SE\"],\n                           \"CI_required\": n_c >= 600, \"replicated\": rep},\n           \"null_reversal_note\": \"consistency predicts volume but carries no breadth information net of size\"\n           if null_rev else None,\n           \"sources\": {k: v[\"source\"] for k, v in K.items()},\n           \"rules\": jload(RES / \"frozen_spec.json\")[\"verdict_rules\"]}\n    jdump(out, RES / \"cheng_verdict.json\")\n    return out", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] TOOL CALL — Write · 2026-09-30 02:15:47 UTC

```
File: /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/build_nb.py

import sys
import nbformat as nbf

OUT = sys.argv[1]
cells = []


def md(s):
    cells.append(nbf.v4.new_markdown_cell(s.strip("\n")))


def code(s):
    cells.append(nbf.v4.new_code_cell(s.strip("\n")))


md(r"""
# Cheng's ideational consistency: a size effect, not reach

This not... [truncated, 38413 chars total]
```

### [46] TOOL RESULT — Write · 2026-09-30 02:15:47 UTC

```
{"type": "create", "filePath": "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/build_nb.py", "content": "import sys\nimport nbformat as nbf\n\nOUT = sys.argv[1]\ncells = []\n\n\ndef md(s):\n    cells.append(nbf.v4.new_markdown_cell(s.strip(\"\\n\")))\n\n\ndef code(s):\n    cells.append(nbf.v4.new_code_cell(s.strip(\"\\n\")))\n\n\nmd(r\"\"... [truncated, 40770 chars total]
```

### [47] TOOL CALL — Bash · 2026-09-30 02:16:01 UTC

```
Fix quoting, set minimum config, build notebook:
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad; cd $S && grep -c "'''" build_nb.py; sed -i -e "s/r\"\"\"/r'''/g" -e "s/^\"\"\")$/''')/" -e 's/\\"\\"\\"/"""/g' build_nb.py && grep -n '\\"' build_nb.py | head; grep -c "r'''" build_nb.py; sed -i -e 's/^N_BOOT_PANEL = 500 /N_BOOT_PANEL = 10  /' -e 's/^N_BOOT_STATIC = 2000 /N_BOOT_STATIC = 10  /' build_nb.py; grep -n "^N_BOOT" build_nb.py; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $S/xenv/bin/python nbformat && $S/xenv/bin/python build_nb.py /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/code_demo.ipynb
```

### [48] TOOL RESULT — Bash · 2026-09-30 02:16:01 UTC

```
{"stdout": "0\n35\n132:N_BOOT_PANEL = 10         # Test A ratio bootstrap draws   (original: N_BOOT_PANEL = 500)\n133:N_BOOT_STATIC = 10       # Test B psp bootstrap draws     (original: N_BOOT_STATIC = 2000)\nwrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/code_demo.ipynb 35 cells", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] ASSISTANT · 2026-09-30 02:16:05 UTC

```
Notebook built with minimum bootstrap draws (10/10). Running the first clean-venv test.
```

### [50] TOOL CALL — Bash · 2026-09-30 02:16:05 UTC

```
Test-run notebook in clean venv:
E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "runtime $(( $(date +%s) - S ))s"
```

### [51] TOOL RESULT — Bash · 2026-09-30 02:16:57 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 171732 bytes to code_demo.ipynb\nruntime 50s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] TOOL CALL — Bash · 2026-09-30 02:17:01 UTC

```
Show notebook outputs:
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c.get('outputs',[]):
        if o.get('output_type')=='stream': print(i,'|',o['text'][:2500])
        elif o.get('output_type')=='error': print(i,'ERR',o['ename'],o['evalue'])
        elif 'data' in o: print(i,'|', list(o['data'].keys()), str(o['data'].get('text/plain',''))[:300])
"
```

### [53] TOOL RESULT — Bash · 2026-09-30 02:17:01 UTC

```
{"stdout": "6 | ['100 concepts, topic vocabulary 4516\\n', \"{'BGM': 13, 'LIFEENV': 13, 'Eng': 13, 'CS': 13, 'SOC': 12, 'MATHDEC': 12, 'PHYS': 12, 'Med': 12}\\n\"]\n12 | ['1088 concept-years, 953 with finite CONS; max |CONS recomputed - artifact| = 5.00e-07 (0.0s)\\n']\n12 | ['text/html', 'text/plain'] ['   ci  year build  n_papers  n_topics      CONS    CONS_r       EMB       SOC  \\\\\\n', '0  60  2003  HOME        21        22       NaN       NaN  0.753771  0.006581   \\n', '1  60  2004  HOME        48        41  0.673252  0.792527  0.829415  0.007136   \\n', '2  60  2005  HOME        52        44  \n14 | ['max |CONS_early_home - artifact| = 4.981693845773627e-07\\n']\n14 | ['text/html', 'text/plain'] ['     ci         body    t0    group   group5  CONS_early_home  \\\\\\n', '0    60          DEV  2003      BGM  BGM+Med         0.719125   \\n', '1   444  OLD_HELDOUT  2007  MATHDEC  MATHDEC         0.353218   \\n', '2   562  OLD_HELDOUT  2003  LIFEENV  LIFEENV         0.463777   \\n', '3  1422  OLD_HELD\n22 | ['Test A (937 concept-years, 100 concepts) in 1.0s\\n', '  A1    b(zCONS) = +0.733  [+0.327, +1.140]  -> +108.2% per SD\\n', '  A1_NB b(zCONS) = +0.465  [+0.268, +0.662]  -> +59.2% per SD\\n', '  A2    b(zCONS) = +0.005  [-0.021, +0.031]  -> +0.5% per SD\\n', '  A3    b(zCONS) = +0.018  [-0.012, +0.048]  -> +1.8% per SD\\n', '  RATIO b_A2/b_A1 = 0.007  boot CI [-0.035  0.068]  (10 draws); |IRLS - pyfixest| = 6.1e-12\\n']\n30 | ['Test B on 100 concepts, 10 draws, in 0.0s\\n', '  raw Spearman(CONS_early_home, V(t0+3)) = +0.231 [0.137 0.457]\\n', '  psp(CONS_early_home, O2r_m50   | B5 + dummies) = -0.099  [-0.350, +0.198]  n=100\\n', '  psp(CONS_early_home, O2r_resid | B5 + dummies) = -0.118  [-0.353, +0.207]  n=100\\n', '  psp(CONS_early_home, O1c       | B5 + dummies) = -0.005  [-0.314, +0.204]  n=100\\n', '  psp(CONS_early_home, O1b       | B5 + dummies) = +0.070  [-0.032, +0.249]  n=100\\n', '  psp(CONS_early_home, O3        | B5 + dummies) = +0.055  [-0.080, +0.192]  n=100\\n', '  paired diff psp(O1c) - psp(O2r_m50) = +0.094 [-0.188  0.255]\\n']\n32 | [\"demo predictions: {'P1': True, 'P2': True, 'P3': False, 'P5': False}\\n\", \"demo verdict   : ['SIZE-DOMINATED', 'NULL-REVERSAL (CI of the reach partial includes 0)']\\n\", 'full-run verdict: REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT\\n']\n34 | ['                                    demo (100 concepts)  full run\\n', 'quantity                                                         \\n', 'A1 PPML %/SD (zCONS)                            108.184    83.101\\n', 'A1-NB b (zCONS)                                   0.465     0.428\\n', 'A2 PPML %/SD (+ log V(t))                         0.512     1.267\\n', 'A3 PPML %/SD (+ concept FE)                       1.800     1.365\\n', 'RATIO b_A2/b_A1                                   0.007     0.021\\n', 'raw Spearman CONS_early vs V(t0+3)                0.231     0.256\\n', 'psp reach O2r_m50                                -0.099    -0.069\\n', 'psp depth O1c                                    -0.005    -0.000\\n', 'psp depth O3                                      0.055    -0.001\\n', 'paired diff O1c - O2r_m50                         0.094     0.035\\n']\n34 | ['image/png', 'text/plain'] ['<Figure size 1600x460 with 3 Axes>']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-30 02:17:13 UTC

```
Minimum config passes in 50s (mostly installs), and the demo estimates are close to the full run. Scaling the bootstrap draws: first 100/200.
```

### [55] TOOL CALL — Bash · 2026-09-30 02:17:13 UTC

```
Scale to 100/200 draws and test:
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad; sed -i -e 's/^N_BOOT_PANEL = 10  /N_BOOT_PANEL = 100 /' -e 's/^N_BOOT_STATIC = 10  /N_BOOT_STATIC = 200 /' -e 's/max |CONS recomputed - artifact| = {dev:.2e}/max |CONS recomputed - artifact| = {dev:.2e} (JSON keeps 6 decimals)/' $S/build_nb.py && grep -n "^N_BOOT" $S/build_nb.py && cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx && $S/xenv/bin/python $S/build_nb.py code_demo.ipynb && E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && T=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s) - T ))s"; python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i in (22,30):
    for o in nb['cells'][i].get('outputs',[]):
        if o.get('output_type')=='stream': print(o['text'])
"
```

### [56] TOOL RESULT — Bash · 2026-09-30 02:18:03 UTC

```
{"stdout": "132:N_BOOT_PANEL = 100        # Test A ratio bootstrap draws   (original: N_BOOT_PANEL = 500)\n133:N_BOOT_STATIC = 200      # Test B psp bootstrap draws     (original: N_BOOT_STATIC = 2000)\nwrote code_demo.ipynb 35 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 172370 bytes to code_demo.ipynb\nruntime 48s\n['Test A (937 concept-years, 100 concepts) in 1.1s\\n', '  A1    b(zCONS) = +0.733  [+0.327, +1.140]  -> +108.2% per SD\\n', '  A1_NB b(zCONS) = +0.465  [+0.268, +0.662]  -> +59.2% per SD\\n', '  A2    b(zCONS) = +0.005  [-0.021, +0.031]  -> +0.5% per SD\\n', '  A3    b(zCONS) = +0.018  [-0.012, +0.048]  -> +1.8% per SD\\n', '  RATIO b_A2/b_A1 = 0.007  boot CI [-0.04   0.063]  (100 draws); |IRLS - pyfixest| = 6.0e-12\\n']\n['Test B on 100 concepts, 200 draws, in 0.3s\\n', '  raw Spearman(CONS_early_home, V(t0+3)) = +0.231 [0.018 0.387]\\n', '  psp(CONS_early_home, O2r_m50   | B5 + dummies) = -0.099  [-0.358, +0.203]  n=100\\n', '  psp(CONS_early_home, O2r_resid | B5 + dummies) = -0.118  [-0.382, +0.159]  n=100\\n', '  psp(CONS_early_home, O1c       | B5 + dummies) = -0.005  [-0.255, +0.244]  n=100\\n', '  psp(CONS_early_home, O1b       | B5 + dummies) = +0.070  [-0.189, +0.316]  n=100\\n', '  psp(CONS_early_home, O3        | B5 + dummies) = +0.055  [-0.134, +0.224]  n=100\\n', '  paired diff psp(O1c) - psp(O2r_m50) = +0.094 [-0.228  0.378]\\n']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] ASSISTANT · 2026-09-30 02:18:15 UTC

```
Very fast (Test A ≈1s, Test B 0.3s), so the original values (500 / 2000 draws) fit easily. Final run at the original values:
```

### [58] TOOL CALL — Bash · 2026-09-30 02:18:15 UTC

```
Run with original bootstrap counts:
S=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad; sed -i -e 's/^N_BOOT_PANEL = 100 /N_BOOT_PANEL = 500 /' -e 's/^N_BOOT_STATIC = 200 /N_BOOT_STATIC = 2000/' $S/build_nb.py && grep -n "^N_BOOT" $S/build_nb.py && cd /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx && $S/xenv/bin/python $S/build_nb.py code_demo.ipynb && E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-937812c77924 && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && T=$(date +%s) && $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s) - T ))s"; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    for o in c.get('outputs',[]):
        if o.get('output_type')=='error': print('ERR',i,o['ename'])
for i in (22,30,32,34):
    for o in nb['cells'][i].get('outputs',[]):
        if o.get('output_type')=='stream': print(''.join(o['text']))
        if 'data' in o and 'image/png' in o['data']: open('/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [59] TOOL RESULT — Bash · 2026-09-30 02:19:07 UTC

```
{"stdout": "132:N_BOOT_PANEL = 500        # Test A ratio bootstrap draws   (original: N_BOOT_PANEL = 500)\n133:N_BOOT_STATIC = 2000     # Test B psp bootstrap draws     (original: N_BOOT_STATIC = 2000)\nwrote code_demo.ipynb 35 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 172375 bytes to code_demo.ipynb\nruntime 50s\nTest A (937 concept-years, 100 concepts) in 1.8s\n  A1    b(zCONS) = +0.733  [+0.327, +1.140]  -> +108.2% per SD\n  A1_NB b(zCONS) = +0.465  [+0.268, +0.662]  -> +59.2% per SD\n  A2    b(zCONS) = +0.005  [-0.021, +0.031]  -> +0.5% per SD\n  A3    b(zCONS) = +0.018  [-0.012, +0.048]  -> +1.8% per SD\n  RATIO b_A2/b_A1 = 0.007  boot CI [-0.045  0.062]  (500 draws); |IRLS - pyfixest| = 6.0e-12\n\nTest B on 100 concepts, 2000 draws, in 2.7s\n  raw Spearman(CONS_early_home, V(t0+3)) = +0.231 [0.034 0.418]\n  psp(CONS_early_home, O2r_m50   | B5 + dummies) = -0.099  [-0.368, +0.169]  n=100\n  psp(CONS_early_home, O2r_resid | B5 + dummies) = -0.118  [-0.382, +0.132]  n=100\n  psp(CONS_early_home, O1c       | B5 + dummies) = -0.005  [-0.303, +0.254]  n=100\n  psp(CONS_early_home, O1b       | B5 + dummies) = +0.070  [-0.199, +0.323]  n=100\n  psp(CONS_early_home, O3        | B5 + dummies) = +0.055  [-0.127, +0.246]  n=100\n  paired diff psp(O1c) - psp(O2r_m50) = +0.094 [-0.248  0.409]\n\ndemo predictions: {'P1': True, 'P2': True, 'P3': False, 'P5': False}\ndemo verdict   : ['SIZE-DOMINATED', 'NULL-REVERSAL (CI of the reach partial includes 0)']\nfull-run verdict: REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT\n\n                                    demo (100 concepts)  full run\nquantity                                                         \nA1 PPML %/SD (zCONS)                            108.184    83.101\nA1-NB b (zCONS)                                   0.465     0.428\nA2 PPML %/SD (+ log V(t))                         0.512     1.267\nA3 PPML %/SD (+ concept FE)                       1.800     1.365\nRATIO b_A2/b_A1                                   0.007     0.021\nraw Spearman CONS_early vs V(t0+3)                0.231     0.256\npsp reach O2r_m50                                -0.099    -0.069\npsp depth O1c                                    -0.005    -0.000\npsp depth O3                                      0.055    -0.001\npaired diff O1c - O2r_m50                         0.094     0.035", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL CALL — Read · 2026-09-30 02:19:11 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/fig.png
```

### [61] TOOL RESULT — Read · 2026-09-30 02:19:11 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [62] ASSISTANT · 2026-09-30 02:19:21 UTC

```
The notebook runs at the original bootstrap counts in about 50s, most of it package installs. Last steps: README, manifest, verification and the struct output.
```

### [63] TOOL CALL — Bash · 2026-09-30 02:19:21 UTC

```
Copy builder, list workspace, verify URL:
cp /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/build_nb.py build_notebook.py && ls -la . .aii && du -sh . && grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json"' code_demo.ipynb; grep -c "urlopen(GITHUB_DATA_URL)" code_demo.ipynb; find . -name __pycache__
```

### [64] TOOL RESULT — Bash · 2026-09-30 02:19:21 UTC

```
{"stdout": ".:\ntotal 4045\ndrwxrwxrwx 3 aii-agent aii-agent 1101317 Sep 30 02:19 .\ndrwxrwxrwx 7 aii-agent aii-agent 2000319 Sep 30 02:14 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 02:09 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 30 02:09 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  495549 Sep 30 02:19 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent   38194 Sep 30 02:19 build_notebook.py\n-rw-rw-rw- 1 aii-agent aii-agent  172393 Sep 30 02:19 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent    7079 Sep 30 02:11 make_mini_demo_data.py\n-rw-rw-rw- 1 aii-agent aii-agent  327613 Sep 30 02:12 mini_demo_data.json\n\n.aii:\ntotal 1077\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 30 02:09 .\ndrwxrwxrwx 3 aii-agent aii-agent 1101317 Sep 30 02:19 ..\n2.1M\t.\n0\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [65] TOOL CALL — Bash · 2026-09-30 02:19:25 UTC

```
Verify exact GitHub URL line in notebook:
python3 -c "
import json
nb=json.load(open('code_demo.ipynb')); src='\n'.join(''.join(c['source']) for c in nb['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json\"' in src)"
```

### [66] TOOL RESULT — Bash · 2026-09-30 02:19:25 UTC

```
{"stdout": "True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [67] TOOL CALL — Bash · 2026-09-30 02:19:45 UTC

```
Write manifest, README, struct output:
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace is heavy (whole directory ~2 MB, every file < 10 MB, no caches or venvs).
# The test venv lives outside the workspace on local disk and is removed by the pipeline.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: Cheng's ideational consistency, a size effect rather than reach

This is a runnable Colab demo of the experiment *"Cheng's consistency: size effect, not reach"* (invention loop
iteration 5, `gen_art_experiment_14`).

The experiment rebuilds the *ideational consistency* of Cheng et al. (2023, *ASR*): the cosine of a concept's
neighbour topic co-usage vector from year t-1 to year t. It then tests two things:

- **Test A.** Does Cheng's next-year volume effect replicate, and does it survive a current-size control?
- **Test B.** As an early trait, and net of the B5 size/growth/breadth baseline, does consistency predict later
  cross-field **reach** or **depth**?

The original `method.py` is an orchestrator over `lib/` modules and about 280k cached concept-year rows. The notebook
keeps those modules' functions nearly verbatim (`cheng.py`, `panel_cheng.py`, `static_cheng.py`) and runs them on a
curated 100-concept subset. It recomputes CONS from each concept's raw per-year neighbour vectors; this matches the
artifact's stored values to within 5e-7, the JSON rounding.

## Layout

| path | content |
|---|---|
| `code_demo.ipynb` | The demo notebook. Covers the install cell, the GitHub/local data loader, the config, S1 (CONS measure and static early traits), S3 (Test A: PPML A1/A2/A3, NB2 twin, cluster-bootstrap ratio), S4 (Test B: partial Spearman bootstrap for reach vs depth), the verdict rules, and a comparison table and figure against the full run. |
| `mini_demo_data.json` | 100 EXP5 frame concepts, stratified over 8 field groups. Each has per-year HOME neighbour topic vectors (sparse), yearly volume V(t), per-year EMB/SOC, B5 covariates and outcomes. The file also holds the full-run headline numbers under `metadata`. |
| `make_mini_demo_data.py` | Builds `mini_demo_data.json` from the source artifact (read-only), using its own `lib/cheng.py` and `lib/ego.py` code. |
| `build_notebook.py` | Generates `code_demo.ipynb` (`python build_notebook.py code_demo.ipynb`; needs `nbformat`). |

## How to run

- **Colab:** open `code_demo.ipynb` and run all cells. The data is fetched from the GitHub raw URL.
- **Locally:** run `jupyter nbconvert --to notebook --execute code_demo.ipynb`. If the URL is unreachable, the
  notebook falls back to the local `mini_demo_data.json`.

The config cell uses the original bootstrap counts (`N_BOOT_PANEL = 500`, `N_BOOT_STATIC = 2000`). The whole
notebook runs in about 50 s, most of it package installation.

## Demo results (100 concepts) vs the full run

| quantity | demo | full run |
|---|---|---|
| A1 PPML, % per SD of CONS | +108% | +83% |
| A1-NB b | 0.465 | 0.428 (Cheng: .43) |
| A2 (+ log V(t)), % per SD | +0.5% | +1.3% |
| ratio b_A2 / b_A1 | 0.007 [-0.045, 0.062] | 0.021 [0.009, 0.035] |
| raw Spearman, CONS_early vs V(t0+3) | +0.231 | +0.256 |
| psp, reach O2r_m50 | -0.099 [-0.368, +0.169] | -0.069 [-0.093, -0.047] |
| psp, depth O1c | -0.005 | -0.000 |

The demo reproduces the size-domination result, **SIZE-DOMINATED**. It also reproduces the signs of the reach and
depth partials. With n = 100, however, the reach CI includes 0, so the demo cannot confirm the reversal. That
confirmation needs the full sample, and is labelled "selection data, not confirmation" there as well.

The demo leaves out Tests C, D and E, the ALL-papers build, and the by-group and by-body refits. They need upstream
tables, or more concepts per cell, than a 100-concept demo holds.

## Restoring removed files

Nothing is marked `delete` in `.aii/manifest.yaml`, and no heavy files exist in this workspace. To regenerate the
demo data, run `make_mini_demo_data.py` with access to the source artifact; it needs pandas, pyarrow, scipy, igraph,
snowballstemmer and loguru.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; python3 -c "import yaml;print(yaml.safe_load(open('.aii/manifest.yaml')))"
```

### [68] TOOL RESULT — Bash · 2026-09-30 02:19:45 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n{'entries': []}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [69] ASSISTANT · 2026-09-30 02:19:57 UTC

```
The data script hardcodes an absolute server path, and that file gets published. Switching it to an environment variable:
```

### [70] TOOL CALL — Bash · 2026-09-30 02:19:57 UTC

```
Remove absolute path from data script, re-verify:
python3 - <<'EOF'
from pathlib import Path
p = Path("make_mini_demo_data.py"); s = p.read_text()
s = s.replace('ART = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14")',
              'ART = Path(os.environ["AII_SOURCE_ARTIFACT"])   # the source artifact folder (gen_art_experiment_14)')
s = s.replace("import json\nimport math\nimport sys\n", "import json\nimport math\nimport os\nimport sys\n")
s = s.replace("Reads the source artifact read-only (ART below)", "Reads the source artifact read-only ($AII_SOURCE_ARTIFACT)")
p.write_text(s)
EOF
sed -i 's/To regenerate the\ndemo data/X/' README.md; sed -i 's/run `make_mini_demo_data.py` with access to the source artifact;/run `AII_SOURCE_ARTIFACT=<path to gen_art_experiment_14> python make_mini_demo_data.py`;/' README.md
grep -rn "/ai-inventor" README.md make_mini_demo_data.py build_notebook.py code_demo.ipynb | head; grep -n "AII_SOURCE" README.md make_mini_demo_data.py
AII_SOURCE_ARTIFACT=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14 /tmp/claude-10001/-ai-inventor-aii-data-runs-run-kLBLH5WmvR9Y-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/5a7a632f-6ab8-4062-9bde-1e94a3cfb389/scratchpad/xenv/bin/python -B make_mini_demo_data.py && md5sum mini_demo_data.json
```

### [71] TOOL RESULT — Bash · 2026-09-30 02:20:03 UTC

```
{"stdout": "code_demo.ipynb:136:    \"GITHUB_DATA_URL = \\\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json\\\"\\n\",\nbuild_notebook.py:98:GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_kLBLH5WmvR9Y/round-5/experiment-14/demo/mini_demo_data.json\"\nREADME.md:58:demo data, run `AII_SOURCE_ARTIFACT=<path to gen_art_experiment_14> python make_mini_demo_data.py`; it needs pandas, pyarrow, scipy, igraph,\nmake_mini_demo_data.py:11:Reads the source artifact read-only ($AII_SOURCE_ARTIFACT); writes only mini_demo_data.json next to this script.\nmake_mini_demo_data.py:28:ART = Path(os.environ[\"AII_SOURCE_ARTIFACT\"])   # the source artifact folder (gen_art_experiment_14)\npicked 100 {'BGM': 13, 'LIFEENV': 13, 'Eng': 13, 'CS': 13, 'SOC': 12, 'MATHDEC': 12, 'PHYS': 12, 'Med': 12} {'OLD_HELDOUT': 40, 'DEV': 34, 'COHORT_2010_14': 26}\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_kLBLH5WmvR9Y/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json 0.327613 MB\n4aa25792360748825f1b84d466ea75e9  mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [72] ASSISTANT · 2026-09-30 02:20:12 UTC

```
I built the demo notebook and its data file. The notebook runs cleanly in a fresh environment set up like Colab, in about 50 seconds (mostly package installs), using the original bootstrap counts (500 and 2000 draws).

**How the notebook works.** `method.py` itself only calls modules in `lib/`, which read about 280k cached rows from earlier experiments. So the notebook copies the functions from those modules nearly verbatim instead of calling them. The only changes are that data comes from the JSON instead of parquet files, and bootstraps run on one process instead of in parallel. It recomputes Cheng's consistency score from each concept's raw yearly topic counts; this matches the artifact's stored values to within 5e-7, which is just JSON rounding.

**Demo results (100 concepts) against the full run:**

| quantity | demo | full run |
|---|---|---|
| Test A, Cheng's model (A1), % per SD | +108% | +83% |
| Negative-binomial twin of A1, coefficient | 0.465 | 0.428 (Cheng: .43) |
| Test A with current size added (A2), % per SD | +0.5% | +1.3% |
| Ratio A2 / A1 | 0.007 [-0.045, 0.062] | 0.021 [0.009, 0.035] |
| Early consistency vs later reach (partial Spearman) | -0.099 [-0.37, +0.17] | -0.069 [-0.093, -0.047] |
| Early consistency vs depth (O1c) | -0.005 | -0.000 |

- **Size result reproduces.** The demo gets the same "size-dominated" label as the full run.
- **Reach result does not reach significance.** The reach and depth estimates have the full-run signs, but with only 100 concepts the reach confidence interval includes 0. The demo cannot confirm the reversal, and the notebook says so.
- **Left out.** Tests C, D and E, the all-papers version of the measure, and the per-group and per-body refits are not in the demo. They need upstream tables, or more concepts per group, than a 100-concept sample has.

**Data file.** `mini_demo_data.json` (0.33 MB) holds 100 concepts spread evenly over the 8 field groups and all three sample bodies. It also carries the full-run headline numbers, which the notebook's final table and three-panel figure compare against.

**Checks.** The notebook contains the required `GITHUB_DATA_URL` line exactly. It loads from GitHub first and falls back to the local file.

**Housekeeping.**
- `.aii/manifest.yaml` has no entries, because nothing in the workspace is large.
- I removed a hardcoded server path from `make_mini_demo_data.py`. It now reads the source folder from the `AII_SOURCE_ARTIFACT` environment variable, and a rerun produced the same file.
- Nothing was committed.

Files are in `art_UkIMstVveAFx/`:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `make_mini_demo_data.py` (rebuilds the data file)
- `build_notebook.py` (regenerates the notebook)
- `README.md`
- `.terminal_claude_agent_struct_out.json`
```
