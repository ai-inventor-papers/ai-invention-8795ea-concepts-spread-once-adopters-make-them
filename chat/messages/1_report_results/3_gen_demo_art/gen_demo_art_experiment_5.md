# gen_demo_art_experiment_5 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_5` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:01:41 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:01:47 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln/results/out.json`
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
id: art_N-mpomDZZ1ln
type: experiment
title: Where new scientific concepts spread next
summary: >-
  Full-corpus OpenAlex snapshot experiment (476M works, 0 API credits for data) on how 653 newborn concepts (legacy-concept
  lexicon, tag-AND-title grounding; benchmark precision 0.996, LLM+hand labelled, $0.007) enter new venue fields, using the
  frozen iteration-1 26-field PMI backbone. Dev = CS/Eng/BGM/Med homes, t0 2003-09 (274 concepts); held-out = other fields
  + 2010-14 cohort (369), run ONCE after a hashed freeze. H2 ENTRY (conditional logit on concept-year risk sets): relatedness
  to the off-home fields that currently RETAIN the concept predicts the next field entered beyond size, Hidalgo density, relatedness-to-home
  and own centrality: held-out LR 71.7 (p=2e-17), d=0.30 [0.24,0.37], positive in Physical/LifeEnv/Social/Cohort, DL pooled
  0.28 [0.22,0.35] I2=0, label-permutation p=0.001, rewired-backbone p=0.015 -> CONFIRMED by the frozen rule. BUT the gateway
  WEIGHTING adds nothing beyond plain retaining relatedness (M3 vs M1 g-only permutation p=0.17 held-out, 0.31 dev); target-field
  size is the strongest single block (AUC 0.76 vs density 0.59); incremental AUC only 0.809->0.817. ORDERING: first retained
  gateway field precedes the calibrated entropy take-off in 66% of broad concepts (sign p=0.003) vs 57% for peripheral fields
  (McNemar p=0.09) -> confirmed by rule, but the lead-lag gateway-permutation placebo (p=0.63) says the panel does not single
  out gateway fields. RESCUE (background-adjusted citation provenance, shared-author links removed; Hanski connectivity) and
  RELAY (availability-null) NOT supported on held-out; the iteration-1 gateway-retention lead did NOT replicate (coef ~0).
  TRAJECTORIES: DTW k-medoids k=2 stable (bootstrap ARI 1.0): volume-matched 'integrating' vs 'localized' classes (held-out
  independent recluster ARI 0.54; localized class dominated by Medicine homes). Independent audits: R1, p_gw and held-out
  AUCs reproduced exactly; exact-likelihood clogit gives LR 77.3, DL-pooled d 0.32 [0.25,0.39] (Breslow pipeline is conservative);
  within-stratum shuffled labels reject 0/20; random-year ordering placebo 0.43 << 0.66. Outputs: method_out.json (entry_events_dev/heldout
  with predict_M0 vs predict_M2 within-stratum probabilities; retention_episodes), results/*.json|csv (frame_concepts, episodes,
  dev/heldout results, frozen_spec, grounding report, deviations), figures/ (AUC forest, group forest, incidence curve, trajectory
  clusters, event studies, case field-flow plots). Caveats: 1,865 episodes (<4k target), MathDec untestable, sense filter
  uninformative, no Wikidata aliases.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/experiment-6/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/experiment-6/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/experiment-6/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 21:01:59 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 21:01:59 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 21:01:59 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 21:01:59 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 21:01:59 UTC

```
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; ls -la $W; wc -l $W/method.py; ls -la $W/results $W/figures 2>/dev/null | head -50
```

### [8] TOOL RESULT — Bash · 2026-09-29 21:02:01 UTC

```
{"stdout": "total 1986\ndrwxrwxrwx 3 aii-agent aii-agent 1002553 Sep 29 21:01 .\ndrwxrwxrwx 4 aii-agent aii-agent 1002555 Sep 29 21:01 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:01 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:01 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   26238 Sep 29 21:01 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:01 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002567 Sep 29 21:01 ..\ntotal 120749\ndrwxrwxrwx 11 aii-agent aii-agent  3000378 Sep 28 21:19 .\ndrwxrwxrwx  7 aii-agent aii-agent  3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 aii-agent aii-agent    39200 Sep 28 19:07 .aii\n-rw-rw-rw-  1 aii-agent aii-agent       54 Sep 28 17:09 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent     9588 Sep 28 19:07 .aii_worker_result.json\n-rw-rw-rw-  1 aii-agent aii-agent  1690358 Sep 28 19:07 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent     3234 Sep 28 18:57 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    13534 Sep 28 19:02 README.md\n-rw-rw-rw-  1 aii-agent aii-agent     4331 Sep 28 17:52 aggregate.py\n-rw-rw-rw-  1 aii-agent aii-agent     1608 Sep 28 17:32 agreement.py\n-rw-rw-rw-  1 aii-agent aii-agent     3309 Sep 28 18:44 audit.py\n-rw-rw-rw-  1 aii-agent aii-agent     3787 Sep 28 18:27 audit_api.py\n-rw-rw-rw-  1 aii-agent aii-agent     4334 Sep 28 18:54 audit_placebo.py\ndrwxrwxrwx  2 aii-agent aii-agent  1023674 Sep 28 18:20 benchmark\n-rw-rw-rw-  1 aii-agent aii-agent     2815 Sep 28 17:17 build_lexicon.py\n-rw-rw-rw-  1 aii-agent aii-agent     2826 Sep 28 17:21 cand.py\n-rw-rw-rw-  1 aii-agent aii-agent     1246 Sep 28 18:21 config.py\ndrwxrwxrwx  2 aii-agent aii-agent  2000104 Sep 28 18:43 figures\n-rw-rw-rw-  1 aii-agent aii-agent     7255 Sep 28 18:09 frame.py\n-rw-rw-rw-  1 aii-agent aii-agent 55464495 Sep 28 18:44 full_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     9530 Sep 28 17:26 grounding.py\ndrwxrwxrwx  3 aii-agent aii-agent  2001319 Sep 28 17:15 inputs\n-rwxrwxrwx  1 aii-agent aii-agent      396 Sep 28 18:53 install.sh\n-rw-rw-rw-  1 aii-agent aii-agent     4593 Sep 28 17:22 label_bench.py\ndrwxrwxrwx  2 aii-agent aii-agent  1005929 Sep 28 18:48 lib\ndrwxrwxrwx  2 aii-agent aii-agent  1017400 Sep 28 18:32 logs\n-rw-rw-rw-  1 aii-agent aii-agent    12758 Sep 28 17:32 make_outputs.py\n-rw-rw-rw-  1 aii-agent aii-agent    36455 Sep 28 18:28 method.py\n-rw-rw-rw-  1 aii-agent aii-agent 47217519 Sep 28 18:43 method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent    13390 Sep 28 18:44 mini_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     9458 Sep 28 17:18 pass1.py\n-rw-rw-rw-  1 aii-agent aii-agent     6895 Sep 28 17:21 pass2.py\n-rw-rw-rw-  1 aii-agent aii-agent    11206 Sep 28 18:44 preview_method_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     2317 Sep 28 18:53 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent     7702 Sep 28 18:56 reproducibility.md\n-rw-rw-rw-  1 aii-agent aii-agent     1451 Sep 28 18:53 requirements.lock.txt\ndrwxrwxrwx  2 aii-agent aii-agent  2000891 Sep 28 18:56 results\ndrwxrwxrwx  4 aii-agent aii-agent  3000365 Sep 28 18:09 scan\ndrwxrwxrwx  2 aii-agent aii-agent  1000310 Sep 28 17:23 tests\n624 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/method.py\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/figures:\ntotal 5964\ndrwxrwxrwx  2 aii-agent aii-agent 2000104 Sep 28 18:43 .\ndrwxrwxrwx 11 aii-agent aii-agent 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 aii-agent aii-agent   25046 Sep 28 18:43 fig_case_41020.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   97782 Sep 28 18:43 fig_case_41020.png\n-rw-rw-rw-  1 aii-agent aii-agent   32453 Sep 28 18:43 fig_case_57442.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  109621 Sep 28 18:43 fig_case_57442.png\n-rw-rw-rw-  1 aii-agent aii-agent   29788 Sep 28 18:43 fig_case_60310.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  104204 Sep 28 18:43 fig_case_60310.png\n-rw-rw-rw-  1 aii-agent aii-agent   28368 Sep 28 18:43 fig_case_94.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  103767 Sep 28 18:43 fig_case_94.png\n-rw-rw-rw-  1 aii-agent aii-agent   21183 Sep 28 18:43 fig_entry_auc_forest.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   57348 Sep 28 18:43 fig_entry_auc_forest.png\n-rw-rw-rw-  1 aii-agent aii-agent   15347 Sep 28 18:43 fig_event_study_dev.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   36970 Sep 28 18:43 fig_event_study_dev.png\n-rw-rw-rw-  1 aii-agent aii-agent   15347 Sep 28 18:43 fig_event_study_heldout.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   35058 Sep 28 18:43 fig_event_study_heldout.png\n-rw-rw-rw-  1 aii-agent aii-agent   16914 Sep 28 18:43 fig_heldout_group_forest.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   29975 Sep 28 18:43 fig_heldout_group_forest.png\n-rw-rw-rw-  1 aii-agent aii-agent   14402 Sep 28 18:43 fig_incidence_function.pdf\n-rw-rw-rw-  1 aii-agent aii-agent   71826 Sep 28 18:43 fig_incidence_function.png\n-rw-rw-rw-  1 aii-agent aii-agent   21213 Sep 28 18:43 fig_trajectory_clusters_dev.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  105959 Sep 28 18:43 fig_trajectory_clusters_dev.png\n-rw-rw-rw-  1 aii-agent aii-agent   21397 Sep 28 18:43 fig_trajectory_clusters_heldout.pdf\n-rw-rw-rw-  1 aii-agent aii-agent  105607 Sep 28 18:43 fig_trajectory_clusters_heldout.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results:\ntotal 14022\ndrwxrwxrwx  2 aii-agent aii-agent 2000891 Sep 28 18:56 .\ndrwxrwxrwx 11 aii-agent aii-agent 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 aii-agent aii-agent    1153 Sep 28 18:21 agreement.json\n-rw-rw-rw-  1 aii-agent aii-agent    4088 Sep 28 18:28 api_audit.csv\n-rw-rw-rw-  1 aii-agent aii-agent     232 Sep 28 18:28 api_audit.json\n-rw-rw-rw-  1 aii-agent aii-agent     625 Sep 28 18:45 audit.json\n-rw-rw-rw-  1 aii-agent aii-agent    1008 Sep 28 18:56 audit_placebo.json\n-rw-rw-rw-  1 aii-agent aii-agent  500897 Sep 28 17:54 candidates.csv\n-rw-rw-rw-  1 aii-agent aii-agent     358 Sep 28 17:54 candidates_summary.json\n-rw-rw-rw-  1 aii-agent aii-agent   10017 Sep 28 18:31 cluster_assign_dev.csv\n-rw-rw-rw-  1 aii-agent aii-agent   14722 Sep 28 18:42 cluster_assign_heldout.csv\n-rw-rw-rw-  1 aii-agent aii-agent    3294 Sep 28 18:28 credits_log.csv\n-rw-rw-rw-  1 aii-agent aii-agent   31868 Sep 28 18:31 dev_result.json\n-rw-rw-rw-  1 aii-agent aii-agent    7043 Sep 28 18:31 dev_spec_parts.json\n-rw-rw-rw-  1 aii-agent aii-agent    5552 Sep 28 18:47 deviations.json\n-rw-rw-rw-  1 aii-agent aii-agent  269458 Sep 28 18:27 entry_risk_sets_dev.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  397762 Sep 28 18:32 entry_risk_sets_heldout.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  272022 Sep 28 18:32 episodes.csv\n-rw-rw-rw-  1 aii-agent aii-agent  165004 Sep 28 18:32 frame_concepts.csv\n-rw-rw-rw-  1 aii-agent aii-agent    1775 Sep 28 18:21 frame_summary.json\n-rw-rw-rw-  1 aii-agent aii-agent     532 Sep 28 18:42 freeze_log.txt", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 21:02:03 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cat $W/method.py
```

### [10] TOOL RESULT — Bash · 2026-09-29 21:02:03 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"How concepts hop between fields: H2 next-field entry (gateway-weighted relatedness to RETAINING fields vs\nrelatedness-to-home / size / Hidalgo density / own centrality), rescue, relay, trajectories and ordering.\n\nStages (run in this order; the held-out stage is sealed until the freeze stage has logged frozen_spec.json):\n  python method.py dev      -> results/dev_result.json (+ dev tables)\n  python method.py freeze   -> results/fro... [truncated, 32033 chars total]
```

### [11] TOOL CALL — Read · 2026-09-29 21:02:05 UTC

```
/var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-N-mpomDZZ1ln/4661b92d-a05f-4b4c-a434-40ca1a08fef6/tool-results/b2cjdaofa.txt
```

### [12] TOOL RESULT — Read · 2026-09-29 21:02:05 UTC

```
{"type": "text", "file": {"filePath": "/var/lib/aii-agent/claude/projects/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-N-mpomDZZ1ln/4661b92d-a05f-4b4c-a434-40ca1a08fef6/tool-results/b2cjdaofa.txt", "content": "#!/usr/bin/env python3\n\"\"\"How concepts hop between fields: H2 next-field entry (gateway-weighted relatedness to RETAINING fields vs\nrelatedness-to-home / size / Hidalgo density / own centrality), rescue,... [truncated, 38898 chars total]
```

### [13] TOOL CALL — Bash · 2026-09-29 21:02:11 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cd $W; ls -la lib inputs inputs/* scan scan/* | head -60; wc -l lib/*.py; cat lib/config.py lib/frame_io.py
```

### [14] TOOL RESULT — Bash [ERROR] · 2026-09-29 21:02:11 UTC

```
Error: Exit code 1
-rw-rw-rw- 1 aii-agent aii-agent    53044 Sep 28 17:14 inputs/field_backbone.json
-rw-rw-rw- 1 aii-agent aii-agent    16314 Sep 28 17:14 inputs/field_outcomes.csv
-rw-rw-rw- 1 aii-agent aii-agent    15251 Sep 28 17:14 inputs/outcomes.csv
-rw-rw-rw- 1 aii-agent aii-agent  3311365 Sep 28 17:14 inputs/source_field.parquet
-rw-rw-rw- 1 aii-agent aii-agent   397668 Sep 28 17:14 inputs/works_manifest.json
-rw-rw-rw- 1 aii-agent aii-agent 73537390 Sep 28 17:53 scan/agg_counts.npz
-rw-rw-rw- 1 aii-agent aii-agent     4578 Sep 28 17:54 scan/cand_concepts.json
-rw-rw-rw- 1 aii-agent aii-agent    77484 Sep 28 18:21 scan/frame_g_dev.npz
-rw-rw-rw- 1 aii-agent aii-agent    89807 Sep 28 18:21 scan/frame_g_heldout.npz
-rw-rw-rw- 1 aii-agent aii-agent    69987 Sep 28 18:21 scan/frame_gpf_dev.npz
-rw-rw-rw- 1 aii-agent aii-agent    85282 Sep 28 18:21 scan/frame_gpf_heldout.npz
-rw-rw-rw- 1 aii-agent aii-agent     1445 Sep 28 17:14 scan/probe.py
-rw-rw-rw- 1 aii-agent aii-agent     1266 Sep 28 17:15 scan/probe2.py

inputs:
total 10545
drwxrwxrwx  3 aii-agent aii-agent 2001319 Sep 28 17:15 .
drwxrwxrwx 11 aii-agent aii-agent 3000378 Sep 28 21:19 ..
drwxrwxrwx  2 aii-agent aii-agent 2000958 Sep 28 17:16 concepts
-rw-rw-rw-  1 aii-agent aii-agent   53044 Sep 28 17:14 field_backbone.json
-rw-rw-rw-  1 aii-agent aii-agent   16314 Sep 28 17:14 field_outcomes.csv
-rw-rw-rw-  1 aii-agent aii-agent   15251 Sep 28 17:14 outcomes.csv
-rw-rw-rw-  1 aii-agent aii-agent 3311365 Sep 28 17:14 source_field.parquet
-rw-rw-rw-  1 aii-agent aii-agent  397668 Sep 28 17:14 works_manifest.json

inputs/concepts:
total 13723
drwxrwxrwx 2 aii-agent aii-agent 2000958 Sep 28 17:16 .
drwxrwxrwx 3 aii-agent aii-agent 2001319 Sep 28 17:15 ..
-rw-rw-rw- 1 aii-agent aii-agent    2440 Sep 28 17:15 manifest.json
-rw-rw-rw- 1 aii-agent aii-agent   10880 Sep 28 17:15 part_000.parquet
-rw-rw-rw- 1 aii-agent aii-agent   16606 Sep 28 17:15 part_001.parquet
-rw-rw-rw- 1 aii-agent aii-agent    9292 Sep 28 17:15 part_002.parquet
-rw-rw-rw- 1 aii-agent aii-agent   10738 Sep 28 17:15 part_003.parquet
-rw-rw-rw- 1 aii-agent aii-agent   11305 Sep 28 17:15 part_004.parquet
-rw-rw-rw- 1 aii-agent aii-agent   14734 Sep 28 17:15 part_005.parquet
-rw-rw-rw- 1 aii-agent aii-agent   16740 Sep 28 17:16 part_006.parquet
-rw-rw-rw- 1 aii-agent aii-agent   20261 Sep 28 17:16 part_007.parquet
-rw-rw-rw- 1 aii-agent aii-agent   20683 Sep 28 17:16 part_008.parquet
-rw-rw-rw- 1 aii-agent aii-agent   38935 Sep 28 17:16 part_009.parquet
-rw-rw-rw- 1 aii-agent aii-agent   87702 Sep 28 17:16 part_010.parquet
-rw-rw-rw- 1 aii-agent aii-agent 9785666 Sep 28 17:16 part_011.parquet

lib:
total 3974
drwxrwxrwx  2 aii-agent aii-agent 1005929 Sep 28 18:48 .
drwxrwxrwx 11 aii-agent aii-agent 3000378 Sep 28 21:19 ..
-rw-rw-rw-  1 aii-agent aii-agent    1465 Sep 28 17:25 frame_io.py
-rw-rw-rw-  1 aii-agent aii-agent    9067 Sep 28 18:26 h2.py
-rw-rw-rw-  1 aii-agent aii-agent    2524 Sep 28 17:21 lib_outcomes.py
-rw-rw-rw-  1 aii-agent aii-agent    2928 Sep 28 17:18 matcher.py
-rw-rw-rw-  1 aii-agent aii-agent    5326 Sep 28 17:14 rangefile.py
-rw-rw-rw-  1 aii-agent aii-agent    7300 Sep 28 17:27 rescue_relay.py
-rw-rw-rw-  1 aii-agent aii-agent   13680 Sep 28 17:14 scan_snapshot_iter1.py
-rw-rw-rw-  1 aii-agent aii-agent    8655 Sep 28 17:23 stats_core.py
-rw-rw-rw-  1 aii-agent aii-agent    9778 Sep 28 17:28 traj.py

scan:
total 83859
drwxrwxrwx  4 aii-agent aii-agent  3000365 Sep 28 18:09 .
   44 lib/frame_io.py
  193 lib/h2.py
   64 lib/lib_outcomes.py
   79 lib/matcher.py
  142 lib/rangefile.py
  166 lib/rescue_relay.py
  349 lib/scan_snapshot_iter1.py
  187 lib/stats_core.py
  216 lib/traj.py
 1440 total
cat: lib/config.py: No such file or directory
"""Guarded access to frame tables. Held-out outcome / entry data can only be loaded once results/freeze_log.txt
exists (T5 sealing guard)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from config import RES, SCAN


class SealedError(RuntimeError):
    pass


def frozen() -> bool:
    return (RES / "freeze_log.txt").exists()


def load_backbone() -> dict:
    b = json.loads((RES.parent / "inputs" / "field_backbone.json").read_text())
    b["phi"] = np.array(b["phi"]); b["g"] = np.array(b["gateway_eig"])
    b["g_deg"] = np.array(b["gateway_deg"]); b["g_btw"] = np.array(b["gateway_btw"])
    return b


def load_g(split: str) -> dict[int, np.ndarray]:
    """per-concept grounded counts [NY, 27] (slot 0 = no venue field, slot k = field 10+k)."""
    if split != "dev" and not frozen():
        raise SealedError(f"split {split!r} is sealed until frozen_spec.json is logged in freeze_log.txt")
    z = np.load(SCAN / f"frame_g_{'dev' if split == 'dev' else 'heldout'}.npz")
    return {int(c): z["g"][i] for i, c in enumerate(z["cidx"])}


def load_frame(split: str | None = None) -> pd.DataFrame:
    fc = pd.read_csv(RES / "frame_concepts.csv")
    if split is None:
        return fc
    if split != "dev" and not frozen():
        raise SealedError(f"split {split!r} is sealed")
    if split == "heldout":
        return fc[fc.split.isin(["heldout_field", "heldout_cohort"])]
    return fc[fc.split == split]
```

### [15] TOOL CALL — Bash · 2026-09-29 21:02:15 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cd $W; cat config.py lib/h2.py lib/stats_core.py
```

### [16] TOOL RESULT — Bash · 2026-09-29 21:02:15 UTC

```
{"stdout": "\"\"\"Frozen constants and paths shared by every module (paths derived from this file's location).\"\"\"\nfrom __future__ import annotations\n\nimport os\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nINP, RES, LOGS, FIGS, SCAN, BENCH = (ROOT / d for d in (\"inputs\", \"results\", \"logs\", \"figures\", \"scan\", \"benchmark\"))\nfor _d in (INP, RES, LOGS, FIGS, SCAN, BENCH):\n    _d.mkdir(parents=True, exist_ok=True)\nP1 = SCAN / \"pass1\"\nP2 = SCAN / \"pass2\"\n\nSEED = 20261001\nFIELDS = list(range(11, 37))\nNF = 26\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nDEV_HOME = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\"}\nHELDOUT_GROUP = {\"Physical\": [15, 16, 21, 25, 31], \"LifeEnv\": [11, 19, 23, 24, 28, 30],\n                 \"Social\": [12, 14, 20, 32, 33], \"MathDec\": [18, 26], \"OtherHealth\": [29, 34, 35, 36]}\nFIELD_GROUP = {f: g for g, fs in HELDOUT_GROUP.items() for f in fs}\nFIELD_GROUP.update({f: \"DEV_\" + s for f, s in DEV_HOME.items()})\nM_RAREFY, M_RAREFY_SENS = 30, 50\nEPISODE_MIN = 2\nRET_MIN = 2\nT0_MIN = 20\nTAG_SCORE = 0.3\nPREC_GATE = 0.8\nN_BOOT = int(os.environ.get(\"AII_NBOOT\", 2000))  # env overrides only for debugging runs\nN_PERM = int(os.environ.get(\"AII_NPERM\", 1000))\nN_REWIRE = int(os.environ.get(\"AII_NREWIRE\", 200))\nOPENROUTER_CAP_USD = 0.50\n\"\"\"H2 next-field entry: field-year state machine, concept-year risk sets, conditional-logit blocks, AUCs, placebos.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport networkx as nx\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom config import Y0\nfrom stats_core import CLogit, fe_ols\n\nREG = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"]\nMODELS = {\"M0\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\"],\n          \"M1\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\"],\n          \"M2\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_ret_gate\"],\n          \"M3\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"],\n          \"M2lost\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_lost_gate\"]}\n\n\ndef states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:\n    \"\"\"g: [NY, 27] grounded counts. Returns boolean [NY, 26] matrices (years Y0..).\"\"\"\n    x = g[:, 1:]\n    cum = np.cumsum(x, 0)\n    entered = cum >= min_n\n    w3 = x.copy()\n    w3[1:] += x[:-1]; w3[2:] += x[:-2]\n    ent_lag2 = np.zeros_like(entered); ent_lag2[2:] = entered[:-2]\n    offhome = np.ones(26, bool)\n    for h in home:\n        offhome[h - 11] = False\n    retaining = ent_lag2 & (w3 >= min_n) & offhome[None, :]\n    lost = entered & (w3 == 0)\n    return {\"entered\": entered, \"retaining\": retaining, \"lost\": lost, \"w3\": w3, \"cum\": cum, \"offhome\": offhome}\n\n\ndef rca_entered(g: np.ndarray, GF: np.ndarray) -> np.ndarray:\n    \"\"\"entry when cumulative count >= 2 and the field's cumulative share of the concept exceeds its share of all works.\"\"\"\n    x = np.cumsum(g[:, 1:], 0)\n    tot = x.sum(1, keepdims=True)\n    F = np.cumsum(GF, 0)\n    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)\n    share_c = x / np.maximum(tot, 1)\n    ok = (x >= 2) & (share_c > share_all)\n    return np.maximum.accumulate(ok.astype(int), 0).astype(bool)\n\n\ndef build_risk_sets(frame: pd.DataFrame, G: dict[int, np.ndarray], bb: dict, GF: np.ndarray,\n                    entry_def: str = \"count\", horizon: int = 8) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:\n    \"\"\"Rows = (concept, year t, candidate field k not entered by t-1, not home). Returns df, Ret matrix, Lost matrix.\"\"\"\n    phi, gate = bb[\"phi\"], bb[\"g\"]\n    colsum = phi.sum(0)\n    logGF = np.log(np.maximum(GF, 1))\n    rows, RET, LOST = [], [], []\n    for r in frame.itertuples():\n        c = int(r.cidx); t0 = int(r.t0)\n        home = [int(h) for h in str(r.home).split(\"|\")]\n        S = states(G[c], home)\n        ent = rca_entered(G[c], GF) if entry_def == \"rca\" else S[\"entered\"]\n        hidx = [h - 11 for h in home]\n        a = phi[hidx].mean(0)\n        for t in range(t0 + 1, min(t0 + horizon, 2022) + 1):\n            ti = t - Y0\n            E = ent[ti - 1]\n            cand = ~E & S[\"offhome\"]\n            if not cand.any():\n                continue\n            ev = ent[ti] & cand\n            Ret = S[\"retaining\"][ti - 1]\n            Lost = S[\"lost\"][ti - 1] & S[\"offhome\"]\n            dens = (phi[E].sum(0)) / np.where(colsum > 0, colsum, 1)\n            d0 = phi[Ret].mean(0) if Ret.any() else np.zeros(26)\n            d = (gate[Ret] @ phi[Ret]) / gate[Ret].sum() if Ret.any() and gate[Ret].sum() > 0 else np.zeros(26)\n            dl = (gate[Lost] @ phi[Lost]) / gate[Lost].sum() if Lost.any() and gate[Lost].sum() > 0 else np.zeros(26)\n            for k in np.nonzero(cand)[0]:\n                rows.append((c, t, t - t0, k + 11, int(ev[k]), a[k], logGF[ti - 1, k], dens[k], gate[k], d0[k], d[k], dl[k],\n                             int(Ret.sum()), int(Lost.sum()), r.group, r.split, int(r.intersection_born), float(r.home_gateway)))\n                RET.append(Ret); LOST.append(Lost)\n    df = pd.DataFrame(rows, columns=[\"cidx\", \"t\", \"age\", \"field\", \"entered\", \"a_phi_home\", \"b_log_size\", \"c_density\",\n                                     \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\", \"n_ret\", \"n_lost\", \"group\",\n                                     \"split\", \"intersection_born\", \"home_gateway\"])\n    df[\"stratum\"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)\n    return df, np.array(RET, bool).reshape(-1, 26), np.array(LOST, bool).reshape(-1, 26)\n\n\ndef standardise(df: pd.DataFrame, spec: dict | None, cols: list[str]) -> tuple[pd.DataFrame, dict]:\n    if spec is None:\n        spec = {c: {\"mean\": float(df[c].mean()), \"sd\": float(df[c].std() or 1.0)} for c in cols}\n    out = df.copy()\n    for c in cols:\n        out[c] = (df[c] - spec[c][\"mean\"]) / (spec[c][\"sd\"] if spec[c][\"sd\"] > 0 else 1.0)\n    return out, spec\n\n\ndef fit_model(df: pd.DataFrame, cols: list[str], ridge: float = 0.0) -> dict:\n    m = CLogit(df[cols].to_numpy(), df.entered.to_numpy(), df.stratum.to_numpy(), ridge=ridge).fit()\n    return {\"coef\": dict(zip(cols, map(float, m[\"coef\"]))), \"se\": dict(zip(cols, map(float, m[\"se\"]))), \"ll\": m[\"ll\"],\n            \"n_strata\": m[\"n_strata\"], \"n_events\": m.get(\"n_events\", 0), \"n_rows\": m.get(\"n_rows\", 0),\n            \"converged\": m[\"converged\"], \"_b\": m[\"coef\"]}\n\n\ndef lr_test(big: dict, small: dict, df_: int) -> dict:\n    lr = 2 * (big[\"ll\"] - small[\"ll\"])\n    return {\"LR\": float(lr), \"df\": df_, \"p\": float(stats.chi2.sf(max(lr, 0), df_))}\n\n\ndef within_auc(df: pd.DataFrame, score: np.ndarray) -> pd.Series:\n    \"\"\"mean-rank AUC per informative stratum.\"\"\"\n    d = pd.DataFrame({\"s\": df.stratum.to_numpy(), \"y\": df.entered.to_numpy(), \"x\": score})\n    d[\"r\"] = d.groupby(\"s\").x.rank(method=\"average\")\n    g = d.groupby(\"s\").agg(ntot=(\"y\", \"size\"), nev=(\"y\", \"sum\"))\n    re = d[d.y == 1].groupby(\"s\").r.sum()\n    g = g.join(re.rename(\"rs\")).fillna({\"rs\": 0})\n    g = g[(g.nev > 0) & (g.nev < g.ntot)]\n    nn = g.ntot - g.nev\n    return (g.rs - g.nev * (g.nev + 1) / 2) / (g.nev * nn)\n\n\ndef concept_boot_mean(series: pd.Series, n_boot: int, rng) -> list[float]:\n    \"\"\"series indexed by stratum id (cidx*100 + ...): concept-clustered bootstrap CI of the mean.\"\"\"\n    cid = (series.index.to_numpy() // 100)\n    u, inv = np.unique(cid, return_inverse=True)\n    sums = np.bincount(inv, weights=series.to_numpy()); cnts = np.bincount(inv)\n    bs = []\n    for _ in range(n_boot):\n        pick = rng.integers(0, len(u), len(u))\n        bs.append(sums[pick].sum() / max(cnts[pick].sum(), 1))\n    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]\n\n\ndef boot_coef(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng, small_cols: list[str] | None = None) -> dict:\n    \"\"\"concept-clustered bootstrap of a clogit coefficient (and the LR vs small model if given).\"\"\"\n    cids = df.cidx.unique()\n    by = {c: ix for c, ix in df.groupby(\"cidx\").indices.items()}\n    X = df[cols].to_numpy(); y = df.entered.to_numpy(); st = df.stratum.to_numpy()\n    Xs = df[small_cols].to_numpy() if small_cols else None\n    bs, lrs = [], []\n    for b in range(n_boot):\n        pick = rng.choice(cids, len(cids))\n        idx = np.concatenate([by[c] for c in pick])\n        rep = np.repeat(np.arange(len(pick)), [len(by[c]) for c in pick])\n        s2 = st[idx] * 10000 + rep  # relabel strata of repeated concepts\n        m = CLogit(X[idx], y[idx], s2).fit()\n        bs.append(m[\"coef\"][cols.index(target)])\n        if small_cols:\n            ms = CLogit(Xs[idx], y[idx], s2).fit()\n            lrs.append(2 * (m[\"ll\"] - ms[\"ll\"]))\n    bs = np.array(bs)\n    out = {\"ci\": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], \"se_boot\": float(np.nanstd(bs)),\n           \"n_boot\": n_boot}\n    if small_cols:\n        out[\"lr_boot\"] = [float(x) for x in np.percentile(lrs, [5, 25, 50, 75, 95])]\n        out[\"_lrs\"] = np.array(lrs)\n    return out\n\n\ndef recompute_d(RET: np.ndarray, fields: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:\n    k = fields - 11\n    w = RET * gate[None, :]\n    den = w.sum(1)\n    num = (w * phi[:, k].T).sum(1)\n    return np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)\n\n\ndef eig_gateway(phi: np.ndarray) -> np.ndarray:\n    Gx = nx.from_numpy_array(phi)\n    try:\n        ev = nx.eigenvector_centrality_numpy(Gx, weight=\"weight\")\n    except Exception:  # noqa: BLE001 -- disconnected graph after rewiring: fall back to power iteration\n        ev = nx.eigenvector_centrality(Gx, weight=\"weight\", max_iter=2000)\n    v = np.array([ev[i] for i in range(len(phi))])\n    v = np.abs(v)\n    return v / v.max()\n\n\ndef rewire(phi: np.ndarray, rng) -> np.ndarray:\n    \"\"\"degree-preserving double-edge swaps on the phi>0 graph; original weights reassigned at random to the new edges.\"\"\"\n    Gx = nx.Graph()\n    Gx.add_nodes_from(range(len(phi)))\n    iu = np.transpose(np.nonzero(np.triu(phi, 1) > 0))\n    Gx.add_edges_from(map(tuple, iu))\n    ne = Gx.number_of_edges()\n    try:\n        nx.double_edge_swap(Gx, nswap=10 * ne, max_tries=1000 * ne, seed=int(rng.integers(1 << 31)))\n    except nx.NetworkXAlgorithmError:\n        pass\n    w = phi[iu[:, 0], iu[:, 1]].copy()\n    rng.shuffle(w)\n    P = np.zeros_like(phi)\n    for (i, j), wt in zip(Gx.edges(), w):\n        P[i, j] = P[j, i] = wt\n    return P\n\"\"\"Estimators: vectorised conditional logit (Breslow form for multiple events per stratum), within-FE OLS with\ncluster-robust (CRV1) SEs, Poisson with concept FE, DerSimonian-Laird random-effects pooling, sign test.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import optimize, stats\n\n\nclass CLogit:\n    \"\"\"Each event row e in stratum s contributes x_e.b - log sum_{i in s} exp(x_i.b).\n    Rows must be sorted by stratum; `starts` are the first row index of each stratum.\"\"\"\n\n    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, ridge: float = 0.0):\n        o = np.argsort(strata, kind=\"stable\")\n        self.X, self.y, self.s = X[o].astype(float), y[o].astype(float), strata[o]\n        self.order = o\n        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)\n        self.nev = np.add.reduceat(self.y, self.starts)\n        keep_s = (self.nev > 0) & (self.nev < self.counts)  # informative strata only\n        rows = np.repeat(keep_s, self.counts)\n        self.X, self.y, self.s = self.X[rows], self.y[rows], self.s[rows]\n        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)\n        self.nev = np.add.reduceat(self.y, self.starts)\n        self.ridge = ridge\n\n    def nll(self, b: np.ndarray) -> tuple[float, np.ndarray]:\n        eta = self.X @ b\n        m = np.maximum.reduceat(eta, self.starts)\n        mm = np.repeat(m, self.counts)\n        w = np.exp(eta - mm)\n        S = np.add.reduceat(w, self.starts)\n        lse = np.log(S) + m\n        ll = float((self.y * eta).sum() - (self.nev * lse).sum())\n        p = w / np.repeat(S, self.counts)\n        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)  # per stratum expectation\n        g = (self.y[:, None] * self.X).sum(0) - (self.nev[:, None] * Ex).sum(0)\n        ll -= 0.5 * self.ridge * float(b @ b)\n        g = g - self.ridge * b\n        return -ll, -g\n\n    def hessian(self, b: np.ndarray) -> np.ndarray:\n        eta = self.X @ b\n        m = np.maximum.reduceat(eta, self.starts)\n        w = np.exp(eta - np.repeat(m, self.counts))\n        S = np.add.reduceat(w, self.starts)\n        p = w / np.repeat(S, self.counts)\n        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)\n        Exx = np.add.reduceat(p[:, None, None] * (self.X[:, :, None] * self.X[:, None, :]), self.starts)\n        cov = Exx - Ex[:, :, None] * Ex[:, None, :]\n        return (self.nev[:, None, None] * cov).sum(0) + self.ridge * np.eye(len(b))\n\n    def fit(self) -> dict:\n        k = self.X.shape[1]\n        if len(self.starts) == 0:\n            return {\"coef\": np.full(k, np.nan), \"se\": np.full(k, np.nan), \"ll\": np.nan, \"n_strata\": 0, \"converged\": False}\n        r = optimize.minimize(self.nll, np.zeros(k), jac=True, method=\"L-BFGS-B\", options={\"maxiter\": 500, \"gtol\": 1e-8})\n        H = self.hessian(r.x)\n        try:\n            se = np.sqrt(np.diag(np.linalg.inv(H)))\n        except np.linalg.LinAlgError:\n            se = np.full(k, np.nan)\n        return {\"coef\": r.x, \"se\": se, \"ll\": -r.fun, \"n_strata\": int(len(self.starts)), \"n_events\": int(self.y.sum()),\n                \"n_rows\": int(len(self.y)), \"converged\": bool(r.success)}\n\n\ndef ll_null_clogit(y: np.ndarray, strata: np.ndarray) -> float:\n    \"\"\"log-likelihood at b = 0 on informative strata.\"\"\"\n    _, inv, cnt = np.unique(strata, return_inverse=True, return_counts=True)\n    nev = np.bincount(inv, weights=y)\n    keep = (nev > 0) & (nev < cnt)\n    return float(-(nev[keep] * np.log(cnt[keep])).sum())\n\n\ndef demean(A: np.ndarray, groups: list[np.ndarray], iters: int = 50, tol: float = 1e-10) -> np.ndarray:\n    \"\"\"Alternating projections to sweep out several sets of fixed effects.\"\"\"\n    A = A.astype(float).copy()\n    if A.ndim == 1:\n        A = A[:, None]\n    for _ in range(iters if len(groups) > 1 else 1):\n        prev = A.copy()\n        for g in groups:\n            _, inv = np.unique(g, return_inverse=True)\n            cnt = np.bincount(inv)\n            for j in range(A.shape[1]):\n                A[:, j] -= (np.bincount(inv, weights=A[:, j]) / cnt)[inv]\n        if len(groups) > 1 and np.abs(A - prev).max() < tol:\n            break\n    return A\n\n\ndef fe_ols(y: np.ndarray, X: np.ndarray, fe: list[np.ndarray], cluster: np.ndarray, names: list[str]) -> dict:\n    \"\"\"OLS of y on X after sweeping out fixed effects `fe`; CRV1 SEs clustered on `cluster` (small-sample corrected).\"\"\"\n    ok = np.isfinite(y) & np.isfinite(X).all(1)\n    y, X, cluster = y[ok], X[ok], cluster[ok]\n    fe = [g[ok] for g in fe]\n    Z = demean(np.column_stack([y, X]), fe) if fe else np.column_stack([y - y.mean(), X - X.mean(0)])\n    yd, Xd = Z[:, 0], Z[:, 1:]\n    XtX = Xd.T @ Xd\n    try:\n        XtXi = np.linalg.pinv(XtX)\n    except np.linalg.LinAlgError:\n        return {\"error\": \"singular\"}\n    b = XtXi @ Xd.T @ yd\n    e = yd - Xd @ b\n    _, cinv = np.unique(cluster, return_inverse=True)\n    G = cinv.max() + 1\n    sc = np.zeros((G, Xd.shape[1]))\n    np.add.at(sc, cinv, Xd * e[:, None])\n    n, k = Xd.shape\n    corr = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)\n    V = corr * XtXi @ (sc.T @ sc) @ XtXi\n    se = np.sqrt(np.clip(np.diag(V), 0, None))\n    tcrit = stats.t.ppf(0.975, max(G - 1, 1))\n    out = {\"n\": int(n), \"n_clusters\": int(G), \"coef\": {}, \"V\": V.tolist()}\n    for i, nm in enumerate(names):\n        out[\"coef\"][nm] = {\"b\": float(b[i]), \"se\": float(se[i]), \"ci\": [float(b[i] - tcrit * se[i]), float(b[i] + tcrit * se[i])],\n                           \"p\": float(2 * stats.t.sf(abs(b[i] / se[i]), max(G - 1, 1))) if se[i] > 0 else float(\"nan\")}\n    out[\"_b\"] = b\n    return out\n\n\ndef fe_poisson(y: np.ndarray, X: np.ndarray, group: np.ndarray, names: list[str], offset: np.ndarray | None = None,\n               iters: int = 100) -> dict:\n    \"\"\"Poisson with group fixed effects (concentrated out: exp(alpha_g) = sum y / sum exp(xb+off) within g),\n    Newton on b; CRV1 sandwich SEs clustered by group.\"\"\"\n    ok = np.isfinite(y) & np.isfinite(X).all(1)\n    y, X, group = y[ok].astype(float), X[ok].astype(float), group[ok]\n    off = np.zeros(len(y)) if offset is None else offset[ok]\n    _, gi = np.unique(group, return_inverse=True)\n    sy = np.bincount(gi, weights=y)\n    keep = sy[gi] > 0  # groups with all-zero outcomes carry no information\n    y, X, off, gi = y[keep], X[keep], off[keep], gi[keep]\n    _, gi = np.unique(gi, return_inverse=True)\n    sy = np.bincount(gi, weights=y)\n    b = np.zeros(X.shape[1])\n    for _ in range(iters):\n        eta = X @ b + off\n        w = np.exp(eta - eta.max())\n        sw = np.bincount(gi, weights=w)\n        mu = w * (sy / sw)[gi]\n        # concentrated score / hessian: X demeaned by mu-weighted group means\n        xm = np.column_stack([np.bincount(gi, weights=mu * X[:, j]) / np.bincount(gi, weights=mu) for j in range(X.shape[1])])[gi]\n        Xc = X - xm\n        g = Xc.T @ (y - mu)\n        H = (Xc * mu[:, None]).T @ Xc\n        step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), g)\n        b = b + step\n        if np.abs(step).max() < 1e-9:\n            break\n    Hi = np.linalg.pinv(H)\n    sc = np.zeros((gi.max() + 1, X.shape[1]))\n    np.add.at(sc, gi, Xc * (y - mu)[:, None])\n    G = gi.max() + 1\n    V = G / max(G - 1, 1) * Hi @ (sc.T @ sc) @ Hi\n    se = np.sqrt(np.clip(np.diag(V), 0, None))\n    out = {\"n\": int(len(y)), \"n_clusters\": int(G), \"coef\": {}}\n    for i, nm in enumerate(names):\n        out[\"coef\"][nm] = {\"b\": float(b[i]), \"se\": float(se[i]), \"ci\": [float(b[i] - 1.96 * se[i]), float(b[i] + 1.96 * se[i])],\n                           \"p\": float(2 * stats.norm.sf(abs(b[i] / se[i]))) if se[i] > 0 else float(\"nan\")}\n    return out\n\n\ndef dersimonian_laird(b: np.ndarray, se: np.ndarray) -> dict:\n    b, se = np.asarray(b, float), np.asarray(se, float)\n    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n    b, se = b[ok], se[ok]\n    k = len(b)\n    if k == 0:\n        return {\"k\": 0}\n    w = 1 / se**2\n    bf = (w * b).sum() / w.sum()\n    Q = float((w * (b - bf) ** 2).sum())\n    C = w.sum() - (w**2).sum() / w.sum()\n    tau2 = max(0.0, (Q - (k - 1)) / C) if k > 1 and C > 0 else 0.0\n    ws = 1 / (se**2 + tau2)\n    bre = (ws * b).sum() / ws.sum()\n    sre = math.sqrt(1 / ws.sum())\n    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0\n    return {\"k\": k, \"b\": float(bre), \"se\": sre, \"ci\": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],\n            \"p\": float(2 * stats.norm.sf(abs(bre / sre))), \"tau2\": float(tau2), \"Q\": Q, \"I2\": float(I2)}\n\n\ndef sign_test(k_pos: int, n: int) -> float:\n    \"\"\"one-sided binomial P(X >= k_pos | p = 0.5).\"\"\"\n    return float(stats.binom.sf(k_pos - 1, n, 0.5)) if n > 0 else float(\"nan\")", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-09-29 21:02:23 UTC

```
I'm building a notebook that runs the paper's H2 next-field entry analysis. Next I'll check the data shapes so I can pick a small subset of concepts.
```

### [18] TOOL CALL — Bash · 2026-09-29 21:02:23 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cd $W; head -c 3000 preview_method_out.json; echo; head -3 results/frame_concepts.csv; python3 -c "
import numpy as np, json, pandas as pd
z=np.load('scan/agg_counts.npz'); print({k:(z[k].shape,z[k].dtype) for k in z.files})
z=np.load('scan/frame_g_dev.npz'); print({k:(z[k].shape,z[k].dtype) for k in z.files})
b=json.load(open('inputs/field_backbone.json')); print({k:(type(v).__name__, len(v) if hasattr(v,'__len__') else v) for k,v in b.items()})
fc=pd.read_csv('results/frame_concepts.csv'); print(fc.shape, fc.split.value_counts().to_dict(), fc.newborn.sum()); print(fc.columns.tolist())
print(fc[fc.newborn].groupby('split').group.value_counts())
"
```

### [19] TOOL RESULT — Bash · 2026-09-29 21:02:29 UTC

```
{"stdout": "{\n  \"metadata\": {\n    \"method_name\": \"Gateway-weighted relatedness to retaining fields (H2 next-field entry) + rescue, relay, trajectories\",\n    \"baselines\": \"M0 = relatedness-to-home + log field size + Hidalgo relatedness density + target field's own gateway centrality\",\n    \"frame\": {\n      \"n_candidates\": 653,\n      \"drops\": {\n        \"no_onset_after_grounding\": 0,\n        \"precision_below_gate\": 0,\n        \"n_early_lt30\": 0,\n        \"no_labelled\": 0\n      },\n      \"n_frame\": 653,\n      \"n_newborn\": 653,\n      \"by_split\": {\n        \"dev\": 279,\n        \"heldout_cohort\": 248,\n        \"heldout_field\": 126\n      },\n      \"by_split_newborn\": {\n        \"dev\": 279,\n        \"heldout_cohort\": 248,\n        \"heldout_field\": 126\n      },\n      \"by_group_newborn\": {\n        \"dev|DEV_BGM\": 27,\n        \"dev|DEV_CS\": 22,\n        \"dev|DEV_Eng\": 59,\n        \"dev|DEV_Med\": 171,\n        \"heldout_cohort|DEV_BGM\": 13,\n        \"heldout_cohort|DEV_CS\": 18,\n        \"heldout_cohort|DEV_Eng\": 37,\n        \"heldout_cohort|DEV_Med\": 109,\n        \"heldout_cohort|LifeEnv\": 13,\n        \"heldout_cohort|OtherHealth\": 2,\n        \"heldout_cohort|Physical\": 15,\n        \"heldout_cohort|Social\": 41,\n        \"heldout_field|LifeEnv\": 34,\n        \"heldout_field|OtherHealth\": 4,\n        \"heldout_field|Physical\": 34,\n        \"heldout_field|Social\": 54\n      },\n      \"n_episodes\": 1865,\n      \"episodes_by_split\": {\n        \"heldout_cohort\": 768,\n        \"dev\": 707,\n        \"heldout_field\": 390\n      },\n      \"o2r_resid_coef_dev\": [\n        -0.03808207780883798,\n        3.891852441738708\n      ],\n      \"t0_dist\": {\n        \"2003\": 79,\n        \"2004\": 64,\n        \"2005\": 57,\n        \"2006\": 55,\n        \"2007\": 53,\n        \"2008\": 40,\n        \"2009\": 57,\n        \"2010\": 51,\n        \"2011\": 54,\n        \"2012\": 46,\n        \"2013\": 51,\n        \"2014\": 46\n      },\n      \"home_primary_dist\": {\n        \"27\": 280,\n        \"22\": 96,\n        \"33\": 70,\n        \"17\": 40,\n        \"13\": 40,\n        \"31\": 29,\n        \"11\": 18,\n        \"16\": 14,\n        \"14\": 10,\n        \"23\": 10,\n        \"28\": 8,\n        \"20\": 8,\n        \"25\": 6,\n        \"19\": 6,\n        \"24\": 5,\n        \"36\": 5,\n        \"32\": 5,\n        \"12\": 2,\n        \"35\": 1\n      },\n      \"label_coverage_by_home\": {\n        \"11\": 0.567,\n        \"12\": 0.261,\n        \"13\": 0.779,\n        \"14\": 0.479,\n        \"16\": 0.81,\n        \"17\": 0.617,\n        \"19\": 0.608,\n        \"20\": 0.541,\n        \"22\": 0.747,\n        \"23\": 0.633,\n        \"24\": 0.835,\n        \"25\": 0.797,\n        \"27\": 0.84,\n        \"28\": 0.738,\n        \"31\": 0.791,\n        \"32\": 0.721,\n        \"33\": 0.498,\n        \"35\": 0.861,\n        \"36\": 0.315\n      }\n    },\n    \"grounding\": {\n      \"kappa_llm1_llm2\": 0.3901773533424283,\n      \"agreement_llm1_hand\": 0.8833333333333333,\n      \"rules_test\": {\n        \"title_only\": {\n          \"n\": 153,\n          \"precision_weighted\": 0.9876212453659056,\n          \"precision_raw\": 0.9738562091503268\n        },\n        \"exact_only\": {\n          \"n\": 95,\n      \nconcept_id,cidx,name,level,t0,newborn,home,home_primary,home_weak,home_thin,intersection_born,group,split,n_early,label_coverage_early,precision_est,p_notag,home_gateway,O1,O3,peak_year,N_outcome,O2r_m30,O2r_m50,O2_raw,O2r_resid\nhttps://openalex.org/C739882,94,Anomaly detection,2,2003,True,17,17,False,False,0,DEV_CS,dev,160.0,0.5875,0.970604733190633,1.0,0.0972089563793993,1.0,0.0,2010.0,343.0,4.18722225912469,5.162557984117685,2.0,0.4886429815110937\nhttps://openalex.org/C1124016,154,Biohydrogen,4,2004,True,22,22,True,False,0,DEV_Eng,dev,102.0,0.5588235294117647,0.9550605294225968,1.0,0.2427178906876991,0.0,0.0,2011.0,125.0,5.002240618280212,5.791064322153572,3.0,1.2865167510807556\n{'G': ((28,), dtype('int64')), 'GF': ((28, 26), dtype('int64')), 'n_rows': ((), dtype('int64')), 'n_base': ((), dtype('int64')), 'n_files': ((), dtype('int64')), 'T_all': ((60859, 28, 27), dtype('int32')), 'T_tag': ((60859, 28, 27), dtype('int32')), 'T_tag_exact': ((60859, 28, 27), dtype('int32')), 'T_untag': ((60859, 28, 27), dtype('int32')), 'T_none': ((60859, 28, 27), dtype('int32')), 'TO': ((60859, 28, 27), dtype('int32')), 'TPF_tag': ((60859, 28, 27), dtype('int32'))}\n{'cidx': ((279,), dtype('int64')), 'g': ((279, 28, 27), dtype('float64'))}\n{'slice': ('str', 9), 'fields': ('list', 26), 'field_ids': ('list', 26), 'domain': ('list', 26), 'N_works_with_primary_topic': ('float', 13151896.0), 'n_field': ('list', 26), 'cooc': ('list', 26), 'pmi': ('list', 26), 'phi': ('list', 26), 'phi_min': ('list', 26), 'gateway_eig': ('list', 26), 'gateway_eig_cv': ('float', 0.8772528943021967), 'gateway_deg': ('list', 26), 'gateway_btw': ('list', 26), 'gateway_eig_phimin': ('list', 26), 'n_positive_edges': ('int', 78), 'not_computed': ('dict', 3)}\n(653, 26) {'dev': 279, 'heldout_cohort': 248, 'heldout_field': 126} 653\n['concept_id', 'cidx', 'name', 'level', 't0', 'newborn', 'home', 'home_primary', 'home_weak', 'home_thin', 'intersection_born', 'group', 'split', 'n_early', 'label_coverage_early', 'precision_est', 'p_notag', 'home_gateway', 'O1', 'O3', 'peak_year', 'N_outcome', 'O2r_m30', 'O2r_m50', 'O2_raw', 'O2r_resid']\nsplit           group      \ndev             DEV_Med        171\n                DEV_Eng         59\n                DEV_BGM         27\n                DEV_CS          22\nheldout_cohort  DEV_Med        109\n                Social          41\n                DEV_Eng         37\n                DEV_CS          18\n                Physical        15\n                DEV_BGM         13\n                LifeEnv         13\n                OtherHealth      2\nheldout_field   Social          54\n                LifeEnv         34\n                Physical        34\n                OtherHealth      4\nName: count, dtype: int64", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-29 21:02:43 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cd $W; ls results; python3 -c "
import json
d=json.load(open('results/dev_result.json')); h=d['H2']; print(h.keys()); print(h['LR']); print({m:h['models'][m]['coef'] for m in h['models']}); print(h['perm_null'], h['rewired_null'], h['boot_d'])
print({k:v['mean'] for k,v in h['auc_within_stratum'].items()})
print(d.get('T0_planted_control'))
x=json.load(open('results/heldout_result.json')); print(x.keys()); print(x['H2_pooled']['LR']); print(x['H2_DL_pooled']); print({g:(v.get('d'),v.get('se')) for g,v in x['H2_per_group'].items()}); print(x['decisions']['H2_entry']); print(x['frozen_dev_coef_auc'])
"
```

### [21] TOOL RESULT — Bash · 2026-09-29 21:02:43 UTC

```
{"stdout": "agreement.json\napi_audit.csv\napi_audit.json\naudit.json\naudit_placebo.json\ncandidates.csv\ncandidates_summary.json\ncluster_assign_dev.csv\ncluster_assign_heldout.csv\ncredits_log.csv\ndev_result.json\ndev_spec_parts.json\ndeviations.json\nentry_risk_sets_dev.parquet\nentry_risk_sets_heldout.parquet\nepisodes.csv\nframe_concepts.csv\nframe_summary.json\nfreeze_log.txt\nfrozen_spec.json\ngrounding_concepts.csv\ngrounding_report.json\nheldout_result.json\nlexicon.parquet\nlexicon_dropped.csv\nlexicon_hash.txt\nlexicon_summary.json\nopenrouter_cost.json\nordering_dev.csv\nordering_heldout.csv\np0_dropped.csv\nrelay_dev.csv\nrelay_heldout.csv\nrescue_dev.csv\nrescue_heldout.csv\nsense_filter.pkl\ntrajectories_dev.csv\ntrajectories_heldout.csv\nunit_tests_T0.json\nworks_schema.json\ndict_keys(['n_rows', 'n_strata', 'n_concepts', 'n_events', 'entry_rate', 'models', 'LR', 'auc_within_stratum', 'boot_d', 'perm_null', 'gonly_perm_null_M3_vs_M1', 'rewired_null', 'size_vs_density_auc'])\n{'M2_vs_M0': {'LR': 38.62631818938462, 'df': 1, 'p': 5.132219947935693e-10}, 'M1_vs_M0': {'LR': 34.49334703380282, 'df': 1, 'p': 4.277107398524474e-09}, 'M3_vs_M1': {'LR': 4.5891047429058744, 'df': 1, 'p': 0.032175816366234046}, 'M2lost_vs_M0': {'LR': 2.264491627975076, 'df': 1, 'p': 0.13236964299426815}}\n{'M0': {'a_phi_home': 0.4085332083469411, 'b_log_size': 1.5879543709019577, 'c_density': 0.40320712150872384, 'e_gate_own': 0.19452142882993934}, 'M1': {'a_phi_home': 0.44458459874822653, 'b_log_size': 1.6569975544594562, 'c_density': 0.28094947112790447, 'e_gate_own': 0.14662316106316262, 'd0_ret_rel': 0.2280866067773825}, 'M2': {'a_phi_home': 0.4386005741738248, 'b_log_size': 1.6657980207237686, 'c_density': 0.2810169416258382, 'e_gate_own': 0.11254479933663726, 'd_ret_gate': 0.2501733171946087}, 'M3': {'a_phi_home': 0.4413562498827097, 'b_log_size': 1.6667770220681306, 'c_density': 0.2761375887643083, 'e_gate_own': 0.11822112082306563, 'd0_ret_rel': 0.05919272117617294, 'd_ret_gate': 0.1951283844477377}, 'M2lost': {'a_phi_home': 0.40666979702619155, 'b_log_size': 1.5881064911049378, 'c_density': 0.4110251923242626, 'e_gate_own': 0.19516180291825747, 'd_lost_gate': -0.06872820234442574}}\n{'n': 1000, 'lr_obs': 38.62631818938462, 'p': 0.008991008991008992, 'null_q': [2.4314920020569843, 14.081305961101135, 21.256212929167212, 35.59453830189886], 'null_mean': 5.350495486214151} {'n': 200, 'lr_obs': 38.62631818938462, 'p': 0.029850746268656716, 'null_q95': 26.15383167949332, 'null_median': 2.79862076309837, 'real_gain_le_null95': False} {'ci': [0.18226003805209737, 0.3208766317840767], 'se_boot': 0.035645392641930576, 'n_boot': 2000, 'lr_boot': [22.84589898715267, 31.185561864162764, 38.535957071148914, 46.76387306561969, 60.050626075440505]}\n{'M0': 0.800769410701218, 'M1': 0.8055165501516712, 'M2': 0.8052609350157525, 'M3': 0.8062582497052176, 'M2lost': 0.801795563632166, 'a_phi_home': 0.5800893060228165, 'b_log_size': 0.7076228699652565, 'c_density': 0.6061033235502905, 'e_gate_own': 0.48155933207186796, 'd0_ret_rel': 0.561123457063323, 'd_ret_gate': 0.5610132832561433, 'd_lost_gate': 0.4971998701268986}\n{'planted_beta1_p_median': 0.0, 'planted_detect_rate_p<0.001': 1.0, 'null_reject_rate_0.01': 0.02, 'n_null_sims': 100}\ndict_keys(['n_heldout_concepts', 'by_group', 'H2_pooled', 'frozen_dev_coef_auc', 'H2_per_group', 'H2_DL_pooled', 'H2_sign_count', 'rescue_relay', 'trajectories', 'ordering', 'decisions'])\n{'M2_vs_M0': {'LR': 71.71641463905598, 'df': 1, 'p': 2.4845706606291646e-17}, 'M1_vs_M0': {'LR': 68.56864172514634, 'df': 1, 'p': 1.2253722672182456e-16}, 'M3_vs_M1': {'LR': 5.359129220855721, 'df': 1, 'p': 0.02061406421285374}, 'M2lost_vs_M0': {'LR': 3.692783297256028, 'df': 1, 'p': 0.05464835230436948}}\n{'k': 4, 'b': 0.2835280026617289, 'se': 0.03470316750295396, 'ci': [0.21550979435593914, 0.35154621096751865], 'p': 3.081594151322099e-16, 'tau2': 0.0, 'Q': 0.7519451573302255, 'I2': 0.0}\n{'Physical': (0.33190390712722606, 0.16500811770727022), 'LifeEnv': (0.1782552843878218, 0.14439994076117874), 'Social': (0.24451473387184078, 0.13045899284853288), 'MathDec': (None, None), 'Cohort': (0.2916284471668024, 0.03815489939611666), 'OtherHealth': (None, None)}\n{'LR_p<0.01': True, 'd>0_CI>0': True, 'field_groups_positive>=3_of_3': True, 'cohort_positive': True, 'perm_p<0.05': True, 'rewired_gain_above_null95': True, 'CONFIRMED': True}\n{'M0': {'mean': 0.8070954731216242, 'ci': [0.7961158126587261, 0.8183723881714523]}, 'M2': {'mean': 0.8151394525018186, 'ci': [0.8041990479187258, 0.826213950278546]}}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Bash · 2026-09-29 21:02:59 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; OUT=/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln; cd $W; python3 - <<EOF
import json, numpy as np, pandas as pd
rng=np.random.default_rng(0)
fc=pd.read_csv('results/frame_concepts.csv'); fc=fc[fc.newborn]
quota=[('dev','DEV_Med',18),('dev','DEV_Eng',12),('dev','DEV_BGM',10),('dev','DEV_CS',10),
       ('heldout_field','Physical',10),('heldout_field','LifeEnv',10),('heldout_field','Social',10),('heldout_cohort',None,20)]
pick=[]
for sp,g,n in quota:
    d=fc[(fc.split==sp)&((fc.group==g) if g else True)]
    pick.append(d.sample(n, random_state=int(rng.integers(1e6))))
sel=pd.concat(pick)
G={}
for s in ('dev','heldout'):
    z=np.load(f'scan/frame_g_{s}.npz')
    for i,c in enumerate(z['cidx']): G[int(c)]=z['g'][i]
cols=['concept_id','cidx','name','t0','newborn','home','group','split','intersection_born','home_gateway']
concepts=[]
for r in sel.itertuples():
    g=G[int(r.cidx)]; assert np.allclose(g, np.round(g))
    row={c:getattr(r,c) for c in cols}
    row={k:(v.item() if hasattr(v,'item') else v) for k,v in row.items()}
    row['home']=str(row['home'])
    row['g']=np.round(g).astype(int).tolist()
    concepts.append(row)
b=json.load(open('inputs/field_backbone.json'))
bb={k:b[k] for k in ['fields','field_ids','phi','gateway_eig','gateway_deg','gateway_btw']}
GF=np.load('scan/agg_counts.npz')['GF'].tolist()
dev=json.load(open('results/dev_result.json')); ho=json.load(open('results/heldout_result.json'))
ref={'dev_LR_M2_vs_M0':dev['H2']['LR']['M2_vs_M0'],'dev_d':dev['H2']['models']['M2']['coef']['d_ret_gate'],
 'dev_boot_d_ci':dev['H2']['boot_d']['ci'],'dev_perm_p':dev['H2']['perm_null']['p'],'dev_rewired_p':dev['H2']['rewired_null']['p'],
 'dev_auc_within_stratum':{k:v['mean'] for k,v in dev['H2']['auc_within_stratum'].items()},
 'dev_n_concepts':dev['H2']['n_concepts'],
 'heldout_LR_M2_vs_M0':ho['H2_pooled']['LR']['M2_vs_M0'],'heldout_d':ho['H2_pooled']['models']['M2']['coef']['d_ret_gate'],
 'heldout_boot_d_ci':ho['H2_pooled']['boot_d']['ci'],'heldout_n_concepts':ho['H2_pooled']['n_concepts'],
 'heldout_per_group_d':{g:v.get('d') for g,v in ho['H2_per_group'].items()},
 'heldout_DL_pooled':ho['H2_DL_pooled'],'heldout_frozen_dev_coef_auc':{k:v['mean'] for k,v in ho['frozen_dev_coef_auc'].items()},
 'heldout_decisions_H2_entry':ho['decisions']['H2_entry']}
out={'description':'Curated subset (100 newborn concepts: 50 dev, 50 held-out) of the OpenAlex concept-diffusion frame used by method.py H2 next-field entry analysis. g = per-concept grounded work counts [28 years 1995-2022, 27 slots: slot 0 = no venue field, slot k = OpenAlex field 10+k]. backbone = frozen iteration-1 26-field PMI relatedness (phi) + gateway centralities. GF = all-works counts per [year, field]. reference_full_run = headline numbers from the full 653-concept run.',
 'config':{'SEED':20261001,'Y0':1995,'Y1':2022,'FIELDS':list(range(11,37))},
 'backbone':bb,'GF':GF,'concepts':concepts,'reference_full_run':ref}
json.dump(out,open('$OUT/mini_demo_data.json','w'))
print(sel.groupby(['split','group']).size())
EOF
ls -la $OUT/mini_demo_data.json
```

### [23] TOOL RESULT — Bash · 2026-09-29 21:03:07 UTC

```
{"stdout": "split           group      \ndev             DEV_BGM        10\n                DEV_CS         10\n                DEV_Eng        12\n                DEV_Med        18\nheldout_cohort  DEV_BGM         1\n                DEV_CS          1\n                DEV_Eng         2\n                DEV_Med         8\n                LifeEnv         2\n                OtherHealth     1\n                Social          5\nheldout_field   LifeEnv        10\n                Physical       10\n                Social         10\ndtype: int64\n-rw-rw-rw- 1 aii-agent aii-agent 276867 Sep 29 21:03 /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln/mini_demo_data.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-29 21:03:25 UTC

```
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cd $W; cat pyproject.toml | sed -n 1,60p; grep -n "tslearn\|hmmlearn" requirements.lock.txt
```

### [25] TOOL RESULT — Bash · 2026-09-29 21:03:25 UTC

```
{"stdout": "[project]\nname = \"concept-hopping-fields\"\nversion = \"0.1.0\"\ndescription = \"How newborn scientific concepts enter new fields: next-field entry, rescue, relay and trajectories on the OpenAlex snapshot\"\nrequires-python = \">=3.12\"\n# every package installed in .venv, pinned (uv pip freeze -> requirements.lock.txt);\n# torch is the CPU wheel: install it first with --index-url https://download.pytorch.org/whl/cpu (see install.sh)\ndependencies = [\n  \"annotated-doc==0.0.5\",\n  \"annotated-types==0.8.0\",\n  \"anyio==4.15.1\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"filelock==3.32.3\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"fsspec==2026.7.0\",\n  \"ftfy==6.3.1\",\n  \"h11==0.16.0\",\n  \"hf-xet==1.6.0\",\n  \"hmmlearn==0.3.3\",\n  \"httpcore==1.0.9\",\n  \"httpcore2==2.13.1\",\n  \"httpx==0.28.1\",\n  \"httpx2==2.13.1\",\n  \"huggingface-hub==1.33.0\",\n  \"idna==3.20\",\n  \"interface-meta==2.0.1\",\n  \"jinja2==3.1.6\",\n  \"jiter==0.17.0\",\n  \"joblib==1.6.0\",\n  \"kiwisolver==1.5.1\",\n  \"kmedoids==0.5.5\",\n  \"langcodes==3.5.1\",\n  \"llvmlite==0.49.0\",\n  \"locate==1.1.1\",\n  \"loguru==0.7.3\",\n  \"markdown-it-py==4.2.0\",\n  \"markupsafe==3.0.3\",\n  \"matplotlib==3.11.2\",\n  \"mdurl==0.1.2\",\n  \"mpmath==1.3.0\",\n  \"msgpack==1.2.2\",\n  \"narwhals==2.26.0\",\n  \"networkx==3.7\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"openai==3.20.0\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pillow==12.3.0\",\n  \"pyahocorasick==2.3.1\",\n  \"pyarrow==25.0.1\",\n  \"pydantic==2.13.5\",\n  \"pydantic-core==2.46.5\",\n17:hmmlearn==0.3.3\n78:tslearn==0.9.0", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_N-mpomDZZ1ln", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-29 21:06:25 UTC

```
Now writing the notebook builder.
```

### [27] TOOL CALL — Write · 2026-09-29 21:06:25 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [28] TOOL RESULT — Write · 2026-09-29 21:06:25 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [29] TOOL CALL — Bash · 2026-09-29 21:06:35 UTC

```
sed -i 's/^N_BOOT = 100 /N_BOOT = 10 /; s/^N_PERM = 100 /N_PERM = 10 /; s/^N_REWIRE = 20 /N_REWIRE = 2 /; s/^N_PLANTED_NULL = 20 /N_PLANTED_NULL = 5 /; s/^N_GROUP_BOOT = 100 /N_GROUP_BOOT = 10 /' build_notebook.py && grep -n "^N_" build_notebook.py && python3 build_notebook.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [30] TOOL RESULT — Bash · 2026-09-29 21:07:03 UTC

```
{"stdout": "121:N_BOOT = 10          # original: 2000  concept-clustered bootstrap draws (coefficient CI, AUC CIs, power check)\n122:N_PERM = 10          # original: 1000  label-permutation and gateway-only permutation nulls\n123:N_REWIRE = 2         # original: 200   degree-preserving rewired-backbone nulls\n124:N_PLANTED_NULL = 5   # original: 100   null simulations in the T0 planted positive control\n125:N_GROUP_BOOT = 10    # original: 500   per-held-out-group bootstrap of d\nwrote 34 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 204156 bytes to code_demo.ipynb\n\nreal\t0m24.700s\nuser\t0m20.943s\nsys\t0m1.468s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Bash · 2026-09-29 21:07:09 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[-1500:])
        elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
        elif 'text/plain' in o.get('data',{}): print(''.join(o['data']['text/plain'])[:800])
        elif 'image/png' in o.get('data',{}): print('[image]')
"
```

### [32] TOOL RESULT — Bash · 2026-09-29 21:07:09 UTC

```
{"stdout": "100 concepts; {'dev': 50, 'heldout_field': 30, 'heldout_cohort': 20}\n\nfields: ['Agricultural and Biological Sciences', 'Arts and Humanities', 'Biochemistry, Genetics and Molecular Biology', 'Business, Management and Accounting', 'Chemical Engineering'] ... | phi (26, 26) | GF (28, 26)\n cidx                      name   t0 home   group split\n36364               Bevacizumab 2004   27 DEV_Med   dev\n38988                Atazanavir 2003   27 DEV_Med   dev\n39390 High resolution manometry 2009   27 DEV_Med   dev\n33785               Tocilizumab 2007   27 DEV_Med   dev\n40718                Dabigatran 2007   27 DEV_Med   dev\n51269      Cardiorenal syndrome 2009   27 DEV_Med   dev\n45143                 Aliskiren 2006   27 DEV_Med   dev\n28984                Fingolimod 2008   27 DEV_Med   dev\n\n21:06:59|INFO   |dev risk sets: 8,350 rows, primary 6,484 rows / 320 strata (0s)\n\n    cidx     t  age  field  entered  a_phi_home  b_log_size  c_density  \\\n0  36364  2007    3     11        0         0.0   11.562392   0.179581   \n1  36364  2007    3     12        0         0.0   11.536886   0.150641   \n2  36364  2007    3     14        0         0.0   10.467551   0.489434   \n3  36364  2007    3     15        0         0.0    4.718499   0.000000   \n4  36364  2007    3     16        0         0.0   11.290669   0.082956   \n\n   e_gate_own  d0_ret_rel  d_ret_gate  d_lost_gate  n_ret  n_lost    group  \\\n0    0.284100    0.000000    0.000000          0.0      1       0  DEV_Med   \n1    0.025349    0.228902    0.228902          0.0      1       0  DEV_Med   \n2    0.077116    0.054282    0.054282          0.0      1       0  DEV_Med   \n3    0.963895    0.000000    0.000000      \n21:06:59|INFO   |bootstrap 10 in 0s\n\n21:06:59|INFO   |H2 dev: LR M2vsM0={'LR': 4.8599581842781845, 'df': 1, 'p': 0.02748700230657696}, d=0.194\n\n                M0     M1     M2     M3  M2lost\na_phi_home   0.337  0.364  0.361  0.365   0.337\nb_log_size   1.494  1.556  1.550  1.557   1.495\nc_density    0.406  0.319  0.326  0.316   0.403\ne_gate_own   0.184  0.135  0.103  0.114   0.184\nd0_ret_rel     NaN  0.187    NaN  0.097     NaN\nd_ret_gate     NaN    NaN  0.194  0.107     NaN\nd_lost_gate    NaN    NaN    NaN    NaN   0.035\n/tmp/ipykernel_299/2239439005.py:51: RuntimeWarning: invalid value encountered in sqrt\n  se = np.sqrt(np.diag(np.linalg.inv(H)))\n/tmp/ipykernel_299/2239439005.py:51: RuntimeWarning: invalid value encountered in sqrt\n  se = np.sqrt(np.diag(np.linalg.inv(H)))\n\n21:07:00|INFO   |planted control: {'planted_beta1_p_median': 2.4674014518582874e-64, 'planted_detect_rate_p<0.001': 1.0, 'null_reject_rate_0.01': 0.0, 'n_null_sims': 5}\n\n{\n \"LPM_conceptyear_field_FE\": \"...\",\n \"secondary_all_strata\": 0.1911260287962356,\n \"excl_intersection_born\": 0.22042992163463204,\n \"boundary_home_top_gateway\": \"...\",\n \"gateway_g_deg\": 0.1582480622056327,\n \"gateway_g_btw\": 0.1345817861226382,\n \"rca_entry\": 0.2730159088075623\n}\n{'planted_beta1_p_median': 2.4674014518582874e-64, 'planted_detect_rate_p<0.001': 1.0, 'null_reject_rate_0.01': 0.0, 'n_null_sims': 5}\n{'n_heldout_concepts': 50, 'scale_vs_dev': 1.0, 'P(p<0.01) at heldout n (LR scaled linearly)': 0.3}\n21:07:00|INFO   |dev stage (H2) done in 1s\n\nfrozen spec sha256 = 7e9dd60ecc2feeedff7fc52fa24f86afb6e7aa9cea5e6805bb905e144b115f76\n\n21:07:00|INFO   |bootstrap 10 in 0s\n\n{'Cohort': 20, 'Physical': 10, 'LifeEnv': 10, 'Social': 10}\n{'LR': 5.783714863476121, 'df': 1, 'p': 0.016175319444840512} d = 0.215 boot CI [0.13975175678347976, 0.31314916034477447]\n\n{'M0': {'mean': 0.817525736245304, 'ci': [0.7953936351205984, 0.8262201834124983]}, 'M2': {'mean': 0.8219842810260924, 'ci': [0.7986836922626216, 0.8341130362720467]}}\n{'k': 4, 'b': 0.18669676110449768, 'se': 0.09011235978666134, 'ci': [0.01007653592264146, 0.3633169862863539], 'p': 0.038282052884285336, 'tau2': 0.0, 'Q': 0.8449782188265704, 'I2': 0.0}\n{'positive': 3, 'of': 4, 'sign_test_p': 0.3125}\n\n21:07:00|INFO   |held-out decisions: {\"H2_entry\": {\"LR_p<0.01\": false, \"d>0_CI>0\": true, \"field_groups_positive>=3_of_3\": false, \"cohort_positive\": true, \"perm_p<0.05\": false, \"rewired_gain_above_null95\": false, \"CONFIRMED\": false}}\n\n21:07:00|INFO   |held-out stage (H2) done in 0s\n\net_gate (M2 coef)      0.1938          0.2502           0.2151                0.302\n                    d boot CI low     0.06857          0.1823           0.1398               0.2396\n                   d boot CI high      0.3153          0.3209           0.3131               0.3688\n              label-permutation p     0.09091        0.008991           0.1818                  NaN\n               rewired-backbone p      0.6667         0.02985           0.6667                  NaN\n   gateway-only perm p (M3 vs M1)      0.6364             NaN           0.7273                  NaN\n                           AUC M0      0.8019          0.8008           0.8253                  NaN\n                           AUC M2      0.8019          0.8053           0.8286                  NaN\nfrozen-dev-coef AUC M0 (held-out)         NaN             NaN           0.8175               0.8071\nfrozen-dev-coef AUC M2 (held-out)         NaN             NaN            0.822               0.8151\n          DL-pooled d over groups         NaN             NaN           0.1867               0.2835\n\nH2 entry decision (demo): {'LR_p<0.01': False, 'd>0_CI>0': True, 'field_groups_positive>=3_of_3': False, 'cohort_positive': True, 'perm_p<0.05': False, 'rewired_gain_above_null95': False, 'CONFIRMED': False}\nH2 entry decision (full run): {'LR_p<0.01': True, 'd>0_CI>0': True, 'field_groups_positive>=3_of_3': True, 'cohort_positive': True, 'perm_p<0.05': True, 'rewired_gain_above_null95': True, 'CONFIRMED': True}\n\n<Figure size 1700x480 with 3 Axes>", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] ASSISTANT · 2026-09-29 21:07:19 UTC

```
The minimum configuration runs in 25 s. Scaling up to the next round.
```

### [34] TOOL CALL — Bash · 2026-09-29 21:07:19 UTC

```
sed -i 's/^N_BOOT = 10  /N_BOOT = 200 /; s/^N_PERM = 10  /N_PERM = 200 /; s/^N_REWIRE = 2   /N_REWIRE = 40  /; s/^N_PLANTED_NULL = 5   /N_PLANTED_NULL = 40  /; s/^N_GROUP_BOOT = 10  /N_GROUP_BOOT = 200 /' build_notebook.py && grep -n "^N_" build_notebook.py && python3 build_notebook.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o 'done in [0-9]*s\|bootstrap [0-9]* in [0-9]*s' code_demo.ipynb
```

### [35] TOOL RESULT — Bash · 2026-09-29 21:07:55 UTC

```
{"stdout": "121:N_BOOT = 200         # original: 2000  concept-clustered bootstrap draws (coefficient CI, AUC CIs, power check)\n122:N_PERM = 200         # original: 1000  label-permutation and gateway-only permutation nulls\n123:N_REWIRE = 40        # original: 200   degree-preserving rewired-backbone nulls\n124:N_PLANTED_NULL = 40  # original: 100   null simulations in the T0 planted positive control\n125:N_GROUP_BOOT = 200   # original: 500   per-held-out-group bootstrap of d\nwrote 34 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 204852 bytes to code_demo.ipynb\n\nreal\t0m33.089s\nuser\t0m37.626s\nsys\t0m2.358s\nbootstrap 200 in 1s\ndone in 5s\nbootstrap 200 in 1s\ndone in 5s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-29 21:08:05 UTC

```
Each stage takes about 5 s at roughly a fifth of the original resampling counts, so the full original values should fit in the time limit. Trying them now.
```

### [37] TOOL CALL — Bash · 2026-09-29 21:08:05 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('build_notebook.py'); s=p.read_text()
old=s[s.index('# ---- tunable parameters'):s.index('# ---- frozen constants')]
new='''# ---- tunable parameters (all at the ORIGINAL config.py values; the notebook runs in ~2 min with them) ----
# for a quicker smoke test, e.g. N_BOOT=10, N_PERM=10, N_REWIRE=2, N_PLANTED_NULL=5, N_GROUP_BOOT=10
N_BOOT = 2000         # concept-clustered bootstrap draws (coefficient CI, AUC CIs, power check)
N_PERM = 1000         # label-permutation and gateway-only permutation nulls
N_REWIRE = 200        # degree-preserving rewired-backbone nulls
N_PLANTED_NULL = 100  # null simulations in the T0 planted positive control (planted_control default)
N_GROUP_BOOT = 500    # per-held-out-group bootstrap of d (hard-coded 500 in stage_heldout)

'''
s=s.replace(old,new)
s=s.replace("These are the constants from the original `config.py`. The resampling counts are set small for the demo; the original values are in the comments.",
 "These are the constants from the original `config.py`. On this 100-concept subset, the full original resampling counts (2000 bootstrap draws, 1000 permutations, 200 rewirings) still run in about two minutes, so they are kept. Lower them for a quick smoke test.")
s=s.replace("Bootstrap and permutation counts are reduced so the notebook runs in a few minutes.","The original bootstrap and permutation counts are kept; on this subset the notebook runs in a few minutes.")
s=s.replace("The table puts the demo numbers (100-concept subset, reduced resampling)","The table puts the demo numbers (100-concept subset)")
p.write_text(s)
EOF
grep -n "^N_\|reduced" build_notebook.py; python3 build_notebook.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o 'done in [0-9]*s\|bootstrap [0-9]* in [0-9]*s' code_demo.ipynb
```

### [38] TOOL RESULT — Bash · 2026-09-29 21:09:21 UTC

```
{"stdout": "122:N_BOOT = 2000         # concept-clustered bootstrap draws (coefficient CI, AUC CIs, power check)\n123:N_PERM = 1000         # label-permutation and gateway-only permutation nulls\n124:N_REWIRE = 200        # degree-preserving rewired-backbone nulls\n125:N_PLANTED_NULL = 100  # null simulations in the T0 planted positive control (planted_control default)\n126:N_GROUP_BOOT = 500    # per-held-out-group bootstrap of d (hard-coded 500 in stage_heldout)\nwrote 34 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 205280 bytes to code_demo.ipynb\n\nreal\t1m12.826s\nuser\t1m54.087s\nsys\t0m3.566s\nbootstrap 2000 in 10s\ndone in 26s\nbootstrap 2000 in 10s\ndone in 24s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-29 21:09:27 UTC

```
The full original configuration finishes in 73 s. Checking the results and the figure.
```

### [40] TOOL CALL — Bash · 2026-09-29 21:09:27 UTC

```
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
errs=0
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='error': errs+=1; print('ERR',o['ename'])
        if 'image/png' in o.get('data',{}): open('/tmp/claude-10001/fig_demo.png','wb').write(base64.b64decode(o['data']['image/png']))
print('errors',errs)
print(''.join(nb['cells'][-2]['outputs'][0]['text']))
" ; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/experiment-6/demo/mini_demo_data.json"' code_demo.ipynb
```

### [41] TOOL RESULT — Bash · 2026-09-29 21:09:27 UTC

```
{"stdout": "errors 0\n                         quantity  dev (demo)  dev (full run)  held-out (demo)  held-out (full run)\n      n concepts (primary sample)          50             274               49                  369\n                      LR M2 vs M0        4.86           38.63            5.784                71.72\n                  p (LR M2 vs M0)     0.02749       5.132e-10          0.01618            2.485e-17\n             d_ret_gate (M2 coef)      0.1938          0.2502           0.2151                0.302\n                    d boot CI low    0.002962          0.1823           0.1018               0.2396\n                   d boot CI high      0.3978          0.3209           0.3308               0.3688\n              label-permutation p     0.05195        0.008991          0.03097                  NaN\n               rewired-backbone p      0.1095         0.02985           0.0597                  NaN\n   gateway-only perm p (M3 vs M1)      0.5764             NaN           0.7682                  NaN\n                           AUC M0      0.8019          0.8008           0.8253                  NaN\n                           AUC M2      0.8019          0.8053           0.8286                  NaN\nfrozen-dev-coef AUC M0 (held-out)         NaN             NaN           0.8175               0.8071\nfrozen-dev-coef AUC M2 (held-out)         NaN             NaN            0.822               0.8151\n          DL-pooled d over groups         NaN             NaN           0.1867               0.2835\n\nH2 entry decision (demo): {'LR_p<0.01': False, 'd>0_CI>0': True, 'field_groups_positive>=3_of_3': False, 'cohort_positive': True, 'perm_p<0.05': True, 'rewired_gain_above_null95': False, 'CONFIRMED': False}\nH2 entry decision (full run): {'LR_p<0.01': True, 'd>0_CI>0': True, 'field_groups_positive>=3_of_3': True, 'cohort_positive': True, 'perm_p<0.05': True, 'rewired_gain_above_null95': True, 'CONFIRMED': True}\n\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-29 21:09:33 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb')); src='\n'.join(''.join(c['source']) for c in nb['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/experiment-6/demo/mini_demo_data.json\"' in src, 'urlopen(GITHUB_DATA_URL)' in src)"; ls /tmp/claude-10001/fig_demo.png
```

### [43] TOOL RESULT — Bash · 2026-09-29 21:09:33 UTC

```
{"stdout": "True True\n/tmp/claude-10001/fig_demo.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Read · 2026-09-29 21:09:35 UTC

```
/tmp/claude-10001/fig_demo.png
```

### [45] TOOL RESULT — Read · 2026-09-29 21:09:35 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [46] ASSISTANT · 2026-09-29 21:09:45 UTC

```
The figure looks right. I'll move the legend in panel (c) so it no longer covers the bars, then run the final test.
```

### [47] TOOL CALL — Bash · 2026-09-29 21:09:45 UTC

```
sed -i 's/axes\[2\].legend(fontsize=8)/axes[2].legend(fontsize=8, loc="lower center")/; s/# (c) planted-control\/permutation: observed dev LR/# (c) observed LR/' build_notebook.py && python3 build_notebook.py && UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_N-mpomDZZ1ln-62fca28ae5de/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; python3 -c "
import json
nb=json.load(open('code_demo.ipynb')); print('errors', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']), 'unexecuted', sum(c['execution_count'] is None for c in nb['cells'] if c['cell_type']=='code'))"; ls -la
```

### [48] TOOL RESULT — Bash · 2026-09-29 21:11:03 UTC

```
{"stdout": "wrote 34 cells\n[NbConvertApp] Writing 206213 bytes to code_demo.ipynb\n\nreal\t1m16.170s\nuser\t1m59.636s\nsys\t0m5.480s\nerrors 0 unexecuted 0\ntotal 3973\ndrwxrwxrwx 3 aii-agent aii-agent 1094795 Sep 29 21:09 .\ndrwxrwxrwx 5 aii-agent aii-agent 2000156 Sep 29 21:10 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:01 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:01 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  438276 Sep 29 21:11 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent   49274 Sep 29 21:09 build_notebook.py\n-rw-rw-rw- 1 aii-agent aii-agent  206231 Sep 29 21:11 code_demo.ipynb\n-rw-rw-rw- 1 aii-agent aii-agent  276867 Sep 29 21:03 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] ASSISTANT · 2026-09-29 21:11:23 UTC

```
Passing with the original parameters (76 s, no errors). Now writing the manifest, README and structured output.
```

### [50] TOOL CALL — Bash · 2026-09-29 21:11:23 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# Nothing in this workspace needs a decision: every file is text/code/JSON under the 10 MB auto-keep floor
# (code_demo.ipynb ~0.2 MB, mini_demo_data.json ~0.3 MB, build_notebook.py ~50 KB). No caches or venvs were created here
# (the notebook test venv lives on local disk outside the workspace and is removed by the pipeline).
entries: []
EOF
cat > README.md <<'EOF'
# Demo: where new scientific concepts spread next (H2 next-field entry)

This directory holds a runnable Colab/Jupyter demo of `method.py` from the experiment *"Where new scientific concepts spread next"*.

**The full experiment.** It covers 653 newborn concepts in a full OpenAlex snapshot and uses a frozen 26-field PMI relatedness backbone.

**What the demo does.** It runs the **H2 next-field entry** pipeline from `method.py` with the code copied unchanged:
- `h2_block`, which fits the conditional logit models M0-M3 and M2lost and computes:
  - LR tests
  - within-stratum AUCs
  - a concept-clustered bootstrap of `d`
  - label-permutation, gateway-only permutation and rewired-backbone nulls
- `h2_robust`, the robustness variants
- `planted_control`
- the dev → freeze → held-out stages, including per-group fits, DerSimonian-Laird pooling and the pre-registered H2 entry decision rule

The helper libraries `lib/h2.py` and `lib/stats_core.py` are inlined into the notebook unchanged. The demo input is a curated subset of **100 real concepts** (50 dev, 50 held-out).

The rescue/relay, trajectory and ordering blocks are not in the demo. They need multi-GB per-work citation tables and `tslearn`/`hmmlearn`.

## Layout
| path | what |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed. It loads `mini_demo_data.json` from GitHub and falls back to the local file. It runs in about 75 s with the **original** resampling counts (2000 bootstrap draws / 1000 permutations / 200 rewirings / 100 planted-null simulations / 500 per-group bootstrap draws). |
| `mini_demo_data.json` | The demo data: 100 concepts with frame metadata and per-concept `[28 years × 27 field-slot]` grounded work counts; the frozen 26-field backbone (`phi`, gateway eigenvector/degree/betweenness centralities); `GF` (all-works counts per year × field); and `reference_full_run` (headline numbers from the full 653-concept run). |
| `build_notebook.py` | Regenerates `code_demo.ipynb` from its cell sources: `python3 build_notebook.py`. |
| `.aii/manifest.yaml` | Storage manifest. There are no heavy files, so `entries: []`. |

## How to run
- **Colab:** open `code_demo.ipynb` and run all cells. The first cell installs `loguru` only; numpy, pandas, scipy, networkx and matplotlib come pre-installed.
- **Locally:** create a Python 3.12 venv with `jupyter`, then run:
  ```bash
  jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
  ```
  The install cell pins numpy, pandas, scipy, networkx and matplotlib to Colab's versions.
- **Quick smoke test:** lower `N_BOOT`, `N_PERM`, `N_REWIRE`, `N_PLANTED_NULL` and `N_GROUP_BOOT` in the config cell.

## Demo vs. full-run results
The demo uses about 7× fewer concepts than the full run. Its estimates point the same way, but its tests are weaker:

| | demo | full run |
|---|---|---|
| held-out `d` | 0.215, CI [0.10, 0.33] | 0.30, CI [0.24, 0.37] |
| held-out LR (M2 vs M0) | 5.8 (p = 0.016) | 71.7 |
| held-out prediction AUC, frozen dev coefficients (M0 → M2) | 0.8175 → 0.822 | 0.807 → 0.815 |

The notebook's final cells print the full comparison table and plot:
- per-block AUCs
- a forest plot of the per-group `d`
- the observed LR against the null quantiles

At this sample size the demo does **not** reach the pre-registered "CONFIRMED" verdict. It fails three of the rule's conditions:
- LR p < 0.01
- positive `d` in all three held-out field groups
- LR gain above the 95th percentile of the rewired-backbone null

## Restoring removed files
Nothing in this directory is marked `delete`, so nothing needs restoring. The demo data can be rebuilt from the parent experiment's `results/frame_concepts.csv`, `scan/frame_g_{dev,heldout}.npz`, `scan/agg_counts.npz` (array `GF`) and `inputs/field_backbone.json`. The subset is a seeded stratified sample: `numpy.random.default_rng(0)`, drawing per group 18 Med / 12 Eng / 10 BGM / 10 CS dev concepts; 10 Physical / 10 LifeEnv / 10 Social held-out-field concepts; and 20 held-out-cohort concepts.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json
````

### [51] TOOL RESULT — Bash · 2026-09-29 21:11:23 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] ASSISTANT · 2026-09-29 21:11:33 UTC

```
I've built `code_demo.ipynb` and `mini_demo_data.json`. The notebook ran from start to finish in the clean test environment in about 75 seconds with no errors, well under the 10-minute limit.

**What the notebook covers.** It runs only the headline H2 analysis from `method.py`: which field a new concept enters next.
- **Code:** the analysis functions and the dev → freeze → held-out steps are copied unchanged, split into cells with a short explanation before each. The two helper files they call (`lib/h2.py`, `lib/stats_core.py`) are pasted in as cells, also unchanged, because they don't exist on Colab.
- **Changes to the original:** the input files are replaced by loaders that read `data`, the log file and parquet writes are dropped, and the freeze step keeps the frozen spec in memory and hashes it instead of writing it to disk.
- **Left out:** the rescue/relay, trajectory and ordering parts don't run. They need multi-gigabyte per-paper tables that can't go in the demo data.

**Data.** `mini_demo_data.json` (277 KB) holds 100 real concepts drawn from the experiment's files: 50 dev and 50 held-out, spread across all the groups. It also holds the frozen field-relatedness network, the field sizes, and the headline numbers from the full run for comparison.

**Settings.** The notebook uses the original bootstrap and permutation counts (2000 bootstrap draws, 1000 permutations, 200 rewired networks), because on 100 concepts they fit easily. I scaled up in three rounds, from minimum values (25 s) to about a tenth of the originals (33 s) to the full values (75 s).

**Results.** The demo points the same way as the full run but is much weaker, because it has about 7 times fewer concepts:

| | Demo | Full run |
|---|---|---|
| Effect size `d` (held-out) | 0.215, CI [0.10, 0.33] | 0.30, CI [0.24, 0.37] |
| Likelihood-ratio test, M2 vs M0 (held-out) | 5.8, p = 0.016 | 71.7, p = 2e-17 |

At this size the demo does **not** reach the pre-registered "CONFIRMED" verdict. Three of the rule's six conditions fail:
- the likelihood-ratio test at p < 0.01;
- a positive effect in all three held-out field groups (Social comes out slightly negative, with only 9 concepts);
- beating the 95th percentile of the rewired-network null.

The notebook's results cell prints the verdict next to the full run's. It then shows a comparison table and a three-panel figure: prediction AUC by block, a forest plot of the effect per group, and the observed test statistic against the null distributions.

The notebook contains the exact GitHub URL and loads the data from it, falling back to the local copy until the files are pushed.

I also added a `README.md`, a `build_notebook.py` script that regenerates the notebook, a `.aii/manifest.yaml` with no entries (nothing is large enough to need one), and the required `.terminal_claude_agent_struct_out.json`.
```
