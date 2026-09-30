# gen_demo_art_dataset_1 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_dataset_1` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 21:12:28 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 21:12:34 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_O7Dq4L02QnDN`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_O7Dq4L02QnDN/`:
GOOD: `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_O7Dq4L02QnDN/file.py`, `/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_O7Dq4L02QnDN/results/out.json`
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
id: art_O7Dq4L02QnDN
type: dataset
title: When research concepts were officially recognised
summary: |-
  External-recognition lookup table (outcome O5) for all 65,026 OpenAlex legacy concepts (64,723 target concepts at levels 2-5), built with zero OpenAlex credits and $1.49 of OpenRouter calls. Every event is dated and sourced, and carries year_usable, match_method, match_confidence and relation (same/narrower/broader, stated from the external entry's side). Present-day facts sit in a separate present_day block (year_known=false). sources_checked records found / not_found / not_applicable for each concept and source. There are no O5 flags and no t0 lags; the panel builder derives those.

  Sources: MeSH 2026 (20,872 concepts; DateIntroduced year; mesh_baseline flags years <=1966); English Wikipedia creation dates (6,540 exact first revisions with redirect-first repair; all other titles have a page-id estimate, 93% same calendar year in CV, and year_usable only for years that calibrate well); Wikidata P571/P575 (1,425 concepts); ACM CCS 1998/2012, MSC 2000/2010/2020 and PACS 2010/PhySH (taxonomy_in_version and taxonomy_added_between events); Nature Methods MoTY, Science BOTY, Physics World BOTY 2009-2025, MIT TR10, Gartner Hype Cycle 1995-2025 and Clarivate/CAS Research Fronts 2017-2025 (589 concepts); JEL as present-day membership only.

  Datasets (full_data_out/ parts): concept_recognition (65,026), external_entries_{mesh 31,830, acm_ccs 3,583, msc 17,872, pacs_physh 8,462, jel 1,015, curated_lists 2,666}, match_verifications (28,914 LLM judgements), crosswalk_level1_to_field (284) and spotcheck_p78 (78; 86% of the iteration-1 P78 concepts join). metadata_fold is a provisional dev/heldout/unassigned split from level-1 ancestors mapped to the OpenAlex fields and then to the hypothesis groups. It holds 19.6k/28.3k/17.1k concepts, and plurality group and share are included so the panel can apply S1's rule.

  Quality: all known-answer asserts pass (optogenetics NM 2010, iPSC NM 2009, CRISPR BOTY 2015, super-resolution NM 2008). Audit precision is 0.96 for label matches, 0.79 for ID links and 0.31 for alias-only matches, so alias matches were LLM-verified. Accepted LLM links are 0.97 precise on hand check. relation=same is reliable except for Research Fronts; narrower vs broader is only indicative. Inter-model kappa is 0.60 (accept/reject). Caveats: coverage is uneven (Social and Eng have no dated domain taxonomy, so use a Wikipedia/Wikidata-only O5 variant across groups), Wikipedia dates cluster in its 2001-2007 growth wave, and Research Fronts are citation-derived. See README.md, out/coverage_report.json and out/sources.json.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2
out_expected_files:
- data.py
- full_data_out.json
- preview_data_out.json
- mini_data_out.json
- reproducibility.md
out_demo_files:
- path: data.py
  description: Dataset fetching/generation script
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] ASSISTANT · 2026-09-29 21:12:40 UTC

```
I'll treat the pasted task spec as the request, since it's the whole message and only asks for work inside this workspace. Starting with the required skills.
```

### [4] TOOL CALL — Skill · 2026-09-29 21:12:40 UTC

```
aii-colab
```

### [5] TOOL CALL — Skill · 2026-09-29 21:12:40 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 21:12:40 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL RESULT — Skill · 2026-09-29 21:12:40 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-29 21:12:44 UTC

```
List artifact workspace and my workspace:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; ls -la $W; ls -la $W/full_data_out* 2>/dev/null | head; wc -l $W/data.py; ls -la .; ls -la .aii
```

### [9] TOOL RESULT — Bash · 2026-09-29 21:12:44 UTC

```
{"stdout": "total 21149\ndrwxrwxrwx 10 aii-agent aii-agent 2041367 Sep 28 21:21 .\ndrwxrwxrwx  7 aii-agent aii-agent 3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 aii-agent aii-agent 1000144 Sep 28 20:17 .aii\n-rw-rw-rw-  1 aii-agent aii-agent      54 Sep 28 17:07 .aii_claude_session.json\n-rw-rw-rw-  1 aii-agent aii-agent   19093 Sep 28 20:17 .aii_worker_result.json\n-rw-rw-rw-  1 aii-agent aii-agent 1940706 Sep 28 20:17 .repl_agent.ptylog\n-rw-rw-rw-  1 aii-agent aii-agent    3510 Sep 28 20:10 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 aii-agent aii-agent   27627 Sep 28 20:13 README.md\ndrwxrwxrwx  6 aii-agent aii-agent 2011048 Sep 28 17:50 cache\n-rw-rw-rw-  1 aii-agent aii-agent    4772 Sep 28 19:59 data.py\ndrwxrwxrwx  2 aii-agent aii-agent 2024518 Sep 28 20:06 full_data_out\ndrwxrwxrwx  2 aii-agent aii-agent 2000539 Sep 28 20:00 logs\n-rw-rw-rw-  1 aii-agent aii-agent 2421021 Sep 28 20:04 mini_data_out.json\ndrwxrwxrwx  2 aii-agent aii-agent 1046197 Sep 28 19:46 out\n-rw-rw-rw-  1 aii-agent aii-agent   72004 Sep 28 20:04 preview_data_out.json\n-rw-rw-rw-  1 aii-agent aii-agent     337 Sep 28 18:49 pyproject.toml\n-rw-rw-rw-  1 aii-agent aii-agent    3204 Sep 28 20:10 reproducibility.md\n-rwxrwxrwx  1 aii-agent aii-agent    2582 Sep 28 19:18 restore.sh\n-rwxrwxrwx  1 aii-agent aii-agent    2126 Sep 28 20:06 run_all.sh\ndrwxrwxrwx  2 aii-agent aii-agent 1022252 Sep 28 21:21 scripts\ndrwxrwxrwx  4 aii-agent aii-agent 1001509 Sep 28 20:06 temp\ndrwxrwxrwx  2 aii-agent aii-agent 2004763 Sep 28 21:21 work\ntotal 255048\ndrwxrwxrwx  2 aii-agent aii-agent  2024518 Sep 28 20:06 .\ndrwxrwxrwx 10 aii-agent aii-agent  2041367 Sep 28 21:21 ..\n-rw-rw-rw-  1 aii-agent aii-agent 90009907 Sep 28 20:04 full_data_out_1.json\n-rw-rw-rw-  1 aii-agent aii-agent 90008266 Sep 28 20:04 full_data_out_2.json\n-rw-rw-rw-  1 aii-agent aii-agent 77016616 Sep 28 20:04 full_data_out_3.json\n-rw-rw-rw-  1 aii-agent aii-agent    10594 Sep 28 20:06 mini_full_data_out_1.json\n-rw-rw-rw-  1 aii-agent aii-agent    13272 Sep 28 20:06 mini_full_data_out_2.json\n-rw-rw-rw-  1 aii-agent aii-agent    24929 Sep 28 20:06 mini_full_data_out_3.json\n-rw-rw-rw-  1 aii-agent aii-agent     3738 Sep 28 20:06 preview_full_data_out_1.json\n106 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/data.py\ntotal 2963\ndrwxrwxrwx 3 aii-agent aii-agent 1002807 Sep 29 21:12 .\ndrwxrwxrwx 6 aii-agent aii-agent 2000175 Sep 29 21:11 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:11 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:12 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent   28696 Sep 29 21:12 .repl_agent.ptylog\ntotal 980\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:11 .\ndrwxrwxrwx 3 aii-agent aii-agent 1002807 Sep 29 21:12 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-29 21:12:46 UTC

```
Read data.py, list scripts, preview data:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; cat $W/data.py; echo ----; ls $W/scripts $W/out; echo ----; head -c 4000 $W/preview_data_out.json
```

### [11] TOOL RESULT — Bash · 2026-09-29 21:12:46 UTC

```
{"stdout": "# /// script\n# requires-python = \">=3.12\"\n# dependencies = [\"pandas\", \"pyarrow\", \"loguru\", \"lemminflect\"]\n# ///\n\"\"\"Standardise the collected recognition sources into the exp_sel_data_out schema -> full_data_out.json.\n\nInputs: the source files indexed in temp/datasets/INDEX.md (downloads live under cache/), as processed by the pipeline\nscripts into work/ (concept_rows.pkl, entries.parquet, links.parquet, verifications.parquet, list_entries.parquet,\nconcept_keys.parquet, mesh_desc.parquet) and out/ (crosswalk_level1_to_field.csv, spotcheck_p78.csv).\nRun ./run_all.sh first on a fresh clone.\n\nOne example per data row (a concept, a taxonomy node / MeSH descriptor / list item, one LLM verification, one crosswalk\nrow, one P78 concept), grouped into 10 datasets:\n  concept_recognition, external_entries_{mesh,acm_ccs,msc,pacs_physh,jel,curated_lists}, match_verifications,\n  crosswalk_level1_to_field, spotcheck_p78\nSize rule (aii-file-size-limit): full_data_out.json above 95 MB is split into full_data_out/full_data_out_<n>.json\n(each part a valid exp_sel_data_out document, <= 90 MB) and the single file is removed.\nAlso writes mini_data_out.json (<= 200 examples per dataset, concept rows stratified by provisional group) and\npreview_data_out.json (10 per dataset, strings truncated).\n\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport random\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"scripts\"))\n\nimport pandas as pd  # noqa: E402\nfrom loguru import logger  # noqa: E402\n\nfrom s9_outputs import build_datasets, trunc, write_parts  # noqa: E402\n\nLIMIT_BYTES = 95_000_000\nREQUIRED = (\"input\", \"output\")\n\n\ndef check(ds: list[dict]) -> None:\n    \"\"\"Schema-level checks the validator does not do: one example per row, string input/output, flat metadata.\"\"\"\n    names = [d[\"dataset\"] for d in ds]\n    assert len(names) == len(set(names)) == 10, names\n    for d in ds:\n        assert d[\"examples\"], d[\"dataset\"]\n        for x in d[\"examples\"]:\n            assert all(isinstance(x[k], str) for k in REQUIRED)\n            bad = [k for k in x if k not in REQUIRED and not k.startswith(\"metadata_\")]\n            assert not bad, (d[\"dataset\"], bad)\n            assert not any(isinstance(v, dict) for k, v in x.items() if k.startswith(\"metadata_\")), d[\"dataset\"]\n\n\ndef mini_preview(ds: list[dict]) -> None:\n    rnd = random.Random(0)\n    mini, prev = [], []\n    for d in ds:\n        exs = d[\"examples\"]\n        if d[\"dataset\"] == \"concept_recognition\":\n            by = defaultdict(list)\n            for x in exs:\n                if x[\"metadata_level\"] >= 2:\n                    by[x[\"metadata_group\"]].append(x)\n            per = max(1, 200 // len(by))\n            m = []\n            for g in sorted(by):   # half the richest rows, half random, per provisional group\n                m += sorted(by[g], key=lambda x: -x[\"metadata_n_events\"])[:per // 2]\n                m += rnd.sample(by[g], min(len(by[g]), per - per // 2))\n            m = m[:200]\n        else:\n            m = exs if len(exs) <= 200 else rnd.sample(exs, 200)\n        mini.append({\"dataset\": d[\"dataset\"], \"examples\": m})\n        prev.append({\"dataset\": d[\"dataset\"], \"examples\": trunc(m[:10])})\n    (ROOT / \"mini_data_out.json\").write_text(json.dumps({\"datasets\": mini}, ensure_ascii=False, indent=1))\n    (ROOT / \"preview_data_out.json\").write_text(json.dumps({\"datasets\": prev}, ensure_ascii=False, indent=1))\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    R = pd.read_pickle(ROOT / \"work\" / \"concept_rows.pkl\")\n    logger.info(f\"concept rows {len(R)}\")\n    ds = build_datasets(R)\n    check(ds)\n    counts = {d[\"dataset\"]: len(d[\"examples\"]) for d in ds}\n    logger.info(f\"datasets: {counts}\")\n    fold = Counter(x[\"metadata_fold\"] for x in ds[0][\"examples\"])\n    logger.info(f\"concept_recognition folds: {dict(fold)}\")\n    out = ROOT / \"full_data_out.json\"\n    body = json.dumps({\"metadata\": {\"description\": \"External, dated recognition events for OpenAlex legacy concepts\",\n                                    \"n_examples\": counts}, \"datasets\": ds}, ensure_ascii=False)\n    out.write_text(body)\n    size = out.stat().st_size\n    logger.info(f\"full_data_out.json {size / 1e6:.1f} MB\")\n    if size > LIMIT_BYTES:\n        parts = write_parts(ds)\n        out.unlink()\n        logger.info(f\"above {LIMIT_BYTES / 1e6:.0f} MB -> split into {parts}; single file removed\")\n    mini_preview(ds)\n    logger.info(\"mini_data_out.json and preview_data_out.json written\")\n\n\nif __name__ == \"__main__\":\n    main()\n----\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/out:\ncoverage_report.json\ncrosswalk_level1_to_field.csv\nhand_check.csv\nhand_check_lists_v2.csv\nhand_check_research_fronts.csv\nllm_agreement.json\nllm_cost.json\nqc_checks.json\nsources.json\nspotcheck_p78.csv\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/scripts:\nREADME.template.md\ncommon.py\ncrosswalk_manual.json\nfill_readme.py\nhand_check.py\nhand_check_lists_v2_verdicts.json\nhand_check_rf_verdicts.json\nhand_check_verdicts.json\nllm.py\nresearch_fronts_urls.txt\ns0_concepts.py\ns10_provenance.py\ns1_crosswalk.py\ns2_wikidata.py\ns3_wikipedia.py\ns3b_pageids.py\ns4_mesh.py\ns4b_mesh_supp.py\ns5_taxonomies.py\ns6_lists.py\ns6b_research_fronts.py\ns7_candidates.py\ns7_keys.py\ns7_verify.py\ns7d_lists_v2.py\ns8_assemble.py\ns9_outputs.py\n----\n{\n \"datasets\": [\n  {\n   \"dataset\": \"concept_recognition\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C144501496\\\", \\\"qid\\\": \\\"Q5533489\\\", \\\"qid_resolved\\\": \\\"Q5533489\\\", \\\"label\\\": \\\"Genome editing\\\", \\\"label_norm\\\": \\\"genome editing\\\", \\\"aliases\\\": [\\\"genome editing\\\", \\\"Genome engineering\\\"], \\\"aliases_norm\\\": [\\\"genome engineering\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\": [\\\"C98108389\\\", \\\"C141231307\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"nature_methods_moty\\\", \\\"event_type\\\": \\\"nature_methods_method_of_the_year\\\", \\\"year\\\": 2011, \\\"date\\\": null, \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"embed+llm\\\", \\\"match_confidence\\\": 0.85, \\\"relation\\\": \\\"broader\\\", \\\"entry_id\\\": \\\"nature_methods_moty:2011:1.0:4\\\", \\\"detail\\\":...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 11,\n     \"metadata_n_events_year_usable\": 10,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C144501496\",\n     \"metadata_qid\": \"Q5533489\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C46111723\\\", \\\"qid\\\": \\\"Q471857\\\", \\\"qid_resolved\\\": \\\"Q471857\\\", \\\"label\\\": \\\"Proteomics\\\", \\\"label_norm\\\": \\\"proteomic\\\", \\\"aliases\\\": [\\\"proteomics\\\"], \\\"aliases_norm\\\": [], \\\"acronyms\\\": [], \\\"level\\\": 3, \\\"ancestor_ids\\\": [\\\"C104317684\\\", \\\"C55493867\\\", \\\"C54355233\\\", \\\"C86803240\\\", \\\"C185592680\\\"], \\\"level0_discipli...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2002, \\\"date\\\": \\\"2002-06-05\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Pr...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 9,\n     \"metadata_n_events_year_usable\": 9,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C46111723\",\n     \"metadata_qid\": \"Q471857\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C152662350\\\", \\\"qid\\\": \\\"Q815297\\\", \\\"qid_resolved\\\": \\\"Q815297\\\", \\\"label\\\": \\\"Systems biology\\\", \\\"label_norm\\\": \\\"systems biology\\\", \\\"aliases\\\": [\\\"systems biology\\\", \\\"systems approach to biology\\\", \\\"system biology\\\"], \\\"aliases_norm\\\": [\\\"system biology\\\", \\\"systems approach to biology\\\"], \\\"acronyms\\\": [], ...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2004, \\\"date\\\": \\\"2004-02-13\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Sy...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 2,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\"\n     ],\n     \"metadata_n_events\": 8,\n     \"metadata_n_events_year_usable\": 8,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C152662350\",\n     \"metadata_qid\": \"Q815297\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C189206191\\\", \\\"qid\\\": \\\"Q222046\\\", \\\"qid_resolved\\\": \\\"Q222046\\\", \\\"label\\\": \\\"Genomics\\\", \\\"label_norm\\\": \\\"genomic\\\", \\\"aliases\\\": [\\\"genomics\\\", \\\"genomic science\\\", \\\"genome science\\\", \\\"genome sciences\\\"], \\\"aliases_norm\\\": [\\\"genome science\\\",", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-29 21:12:50 UTC

```
Read s9_outputs.py and list work dir:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; wc -l $W/scripts/s9_outputs.py $W/scripts/common.py; cat $W/scripts/s9_outputs.py; ls -la $W/work | head -40
```

### [13] TOOL RESULT — Bash · 2026-09-29 21:12:50 UTC

```
{"stdout": "  303 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/scripts/s9_outputs.py\n  189 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/scripts/common.py\n  492 total\n#!/usr/bin/env python3\n\"\"\"STEP 9: coverage report, P78 spot check, hand-check sample, and the exp_sel_data_out JSON deliverables.\n\ndata_out: full_data_out/full_data_out_<n>.json (each part a valid exp_sel_data_out document, <= ~90 MB),\n          mini_data_out.json (<= 200 rows per dataset, concept rows stratified by provisional group),\n          preview_data_out.json (10 rows per dataset, long strings truncated).\n\"\"\"\nfrom __future__ import annotations\n\nimport ast\nimport json\nimport random\nfrom collections import Counter, defaultdict\n\nimport pandas as pd\nfrom loguru import logger\n\nfrom common import OUT, ROOT, WORK, norm_label, setup_logging\n\nP78 = ROOT.parents[2] / \"iter_1\" / \"gen_art\" / \"gen_art_experiment_4\" / \"outcomes.csv\"\nACCEPT = {\"same\", \"narrower_entry\", \"broader_entry\"}\nPART_BYTES = 90_000_000\n\n\ndef clean(x):\n    \"\"\"Recursively convert numpy scalars/arrays to Python and NaN/inf to None (strict JSON).\"\"\"\n    import math\n    if isinstance(x, dict):\n        return {str(k_): clean(v_) for k_, v_ in x.items()}\n    if isinstance(x, (list, tuple)):\n        return [clean(y) for y in x]\n    if hasattr(x, \"tolist\") and not isinstance(x, (str, bytes)):\n        return clean(x.tolist())\n    if isinstance(x, float):\n        return None if (math.isnan(x) or math.isinf(x)) else x\n    return x\n\n\ndef dumps(x) -> str:\n    return json.dumps(clean(x), ensure_ascii=False, allow_nan=False, default=str)\n\n\ndef coverage(R: pd.DataFrame, agr: dict) -> dict:\n    tgt = R[R.level >= 2]\n    ex = []\n    for r in tgt.itertuples(index=False):\n        for s, st in r.output[\"sources_checked\"].items():\n            evs = [x for x in r.output[\"events\"] if x[\"source\"] == s]\n            ex.append({\"source\": s, \"status\": st, \"level\": r.level, \"l0\": r.l0[0] if len(r.l0) == 1 else (\"multi\" if r.l0 else \"none\"),\n                       \"group\": r.group, \"n_ev\": len(evs), \"usable\": any(x[\"year_usable\"] for x in evs),\n                       \"years\": [x[\"year\"] for x in evs if x[\"year_usable\"] and x[\"year\"] is not None],\n                       \"methods\": [x[\"match_method\"] for x in evs]})\n    X = pd.DataFrame(ex)\n\n    def summ(d: pd.DataFrame) -> dict:\n        yrs = [y for ys in d.years for y in ys]\n        hist = Counter((y // 5) * 5 for y in yrs)\n        return {\"n_concepts\": int(len(d)), \"n_with_event\": int((d.n_ev > 0).sum()),\n                \"n_with_year_usable_event\": int(d.usable.sum()),\n                \"status\": {k: int(v) for k, v in d.status.value_counts().items()},\n                \"event_year_hist_5y\": {int(k): int(v) for k, v in sorted(hist.items())},\n                \"match_method_mix\": dict(Counter(m for ms in d.methods for m in ms))}\n    rep = {\"frame\": \"OpenAlex legacy concepts, levels 2-5 (levels 0-1 are ancestor-only rows)\",\n           \"n_target_concepts\": int(len(tgt)),\n           \"by_source\": {s: summ(d) for s, d in X.groupby(\"source\")},\n           \"by_source_level\": {f\"{s}|L{l}\": summ(d) for (s, l), d in X.groupby([\"source\", \"level\"])},\n           \"by_source_group\": {f\"{s}|{g}\": summ(d) for (s, g), d in X.groupby([\"source\", \"group\"])},\n           \"by_source_level0\": {f\"{s}|{l}\": summ(d) for (s, l), d in X.groupby([\"source\", \"l0\"])},\n           \"by_source_level_l0_group\": {f\"{s}|L{l}|{l0}|{g}\": {\"n\": int(len(d)), \"n_with_event\": int((d.n_ev > 0).sum()),\n                                                                \"n_year_usable\": int(d.usable.sum())}\n                                        for (s, l, l0, g), d in X.groupby([\"source\", \"level\", \"l0\", \"group\"])},\n           \"llm_audit_and_agreement\": agr}\n    # which groups have a dated taxonomy for their OWN domain (JEL is undated, so Social has none)\n    own = {\"CS\": [\"acm_ccs\"], \"MathDec\": [\"msc\"], \"Physical\": [\"pacs_physh\"], \"BGM\": [\"mesh\"], \"Med\": [\"mesh\"],\n           \"LifeEnv\": [\"mesh\"], \"Social\": [], \"Eng\": [], \"unassigned_health\": [\"mesh\"]}\n    dom = [\"acm_ccs\", \"msc\", \"pacs_physh\", \"mesh\", \"jel\"]\n    gaps = {}\n    for g, d in X[X.source.isin(dom)].groupby(\"group\"):\n        sh = {s_: float((z.n_ev > 0).mean()) for s_, z in d.groupby(\"source\")}\n        gaps[g] = {\"own_domain_dated_taxonomies\": own.get(g), \"share_with_event_by_domain_source\": sh,\n                   \"note\": (\"no dated domain taxonomy (JEL membership is undated); MeSH covers only its psychology/\"\n                            \"health-economics fringe\" if g == \"Social\" else\n                            (\"engineering has no dedicated dated taxonomy here; covered partly by ACM/PACS/MeSH\" if g == \"Eng\" else None))}\n    rep[\"dated_domain_taxonomy_by_group\"] = gaps\n    rep[\"groups_without_dated_domain_taxonomy\"] = sorted(g for g, v in own.items() if not v and g in gaps)\n    rep[\"recommendation\"] = (\"For cross-group O5 comparisons use a Wikipedia/Wikidata-only variant (sources wikipedia_en, \"\n                             \"wikidata), because domain taxonomies and curated lists cover groups unevenly.\")\n    return rep\n\n\ndef spot_p78(R: pd.DataFrame) -> pd.DataFrame:\n    if not P78.exists():\n        logger.warning(f\"P78 file missing at {P78}; join test skipped\")\n        return pd.DataFrame()\n    p = pd.read_csv(P78)\n    idx_l, idx_a = defaultdict(list), defaultdict(list)\n    for r in R.itertuples(index=False):\n        idx_l[r.input[\"label_norm\"]].append(r)\n        for a in r.input[\"aliases_norm\"]:\n            idx_a[a].append(r)\n    out = []\n    for q in p.itertuples(index=False):\n        names = [q.concept] + [x.strip() for x in str(q.aliases_used).split(\"|\") if x.strip() and x != \"nan\"]\n        hit, how = None, None\n        for n in names:\n            nn = norm_label(n)\n            if idx_l.get(nn):\n                hit, how = sorted(idx_l[nn], key=lambda r: -r.level)[0], \"label_norm\"\n                break\n        if hit is None:\n            for n in names:\n                nn = norm_label(n)\n                if idx_a.get(nn):\n                    hit, how = sorted(idx_a[nn], key=lambda r: -r.level)[0], \"alias_norm\"\n                    break\n        evs = hit.output[\"events\"] if hit is not None else []\n        out.append({\"concept\": q.concept, \"aliases_used\": q.aliases_used, \"iter1_group\": q.group, \"iter1_home\": q.home,\n                    \"t0\": q.t0, \"iter1_status\": q.status, \"joined\": hit is not None, \"join_on\": how,\n                    \"openalex_id\": hit.openalex_id if hit is not None else None,\n                    \"oa_label\": hit.input[\"label\"] if hit is not None else None,\n                    \"level\": hit.level if hit is not None else None,\n                    \"provisional_group\": hit.group if hit is not None else None,\n                    \"n_events\": len(evs),\n                    \"events\": \"; \".join(f\"{x['year']}:{x['source']}:{x['event_type']}\" + (f\"({x['relation']})\" if x['relation'] != 'same' else \"\")\n                                        for x in evs),\n                    \"sources_checked\": json.dumps(hit.output[\"sources_checked\"]) if hit is not None else None})\n    return pd.DataFrame(out)\n\n\ndef build_datasets(R: pd.DataFrame) -> list[dict]:\n    e = pd.read_parquet(WORK / \"entries.parquet\").set_index(\"entry_id\", drop=False)\n    L = pd.read_parquet(WORK / \"links.parquet\")\n    k = pd.read_parquet(WORK / \"concept_keys.parquet\").set_index(\"openalex_id\")\n    mesh = pd.read_parquet(WORK / \"mesh_desc.parquet\").set_index(\"mesh_ui\")\n    v = pd.read_parquet(WORK / \"verifications.parquet\")\n    ds = []\n    # 1 concept_recognition\n    ex = []\n    for r in R.itertuples(index=False):\n        ex.append({\"input\": dumps(r.input), \"output\": dumps(r.output), \"metadata_fold\": r.fold, \"metadata_group\": r.group,\n                   \"metadata_group_plurality\": r.group_plurality, \"metadata_group_plurality_share\": r.group_plurality_share,\n                   \"metadata_level\": int(r.level), \"metadata_l1_fields\": [str(x) for x in r.l1_fields],\n                   \"metadata_level0\": list(r.l0), \"metadata_n_events\": int(r.n_events),\n                   \"metadata_n_events_year_usable\": int(r.n_events_year_usable),\n                   \"metadata_frame_role\": r.input[\"frame_role\"], \"metadata_openalex_id\": r.openalex_id,\n                   \"metadata_qid\": r.input[\"qid\"]})\n    ds.append({\"dataset\": \"concept_recognition\", \"examples\": ex})\n    # 2-7 external_recognition_entries, one dataset per source family\n    Lg = {eid: g for eid, g in L.groupby(\"entry_id\")}\n    fam_name = {\"mesh\": \"external_entries_mesh\", \"acm_ccs\": \"external_entries_acm_ccs\", \"msc\": \"external_entries_msc\",\n                \"pacs_physh\": \"external_entries_pacs_physh\", \"jel\": \"external_entries_jel\", \"lists\": \"external_entries_curated_lists\"}\n    lst = pd.read_parquet(WORK / \"list_entries.parquet\").set_index(\"entry_id\")\n    for fam, name in fam_name.items():\n        ex = []\n        for r in e[e.family == fam].itertuples(index=False):\n            g = Lg.get(r.entry_id)\n            matched = [] if g is None else [\n                {\"openalex_id\": x.openalex_id, \"qid\": k.at[x.openalex_id, \"qid\"], \"label\": k.at[x.openalex_id, \"label\"],\n                 \"relation\": x.relation, \"match_method\": x.match_method, \"match_confidence\": round(float(x.match_confidence), 3),\n                 \"link_status\": x.link_status} for x in g.itertuples(index=False)]\n            as_int = lambda x: None if x is None or (isinstance(x, float) and x != x) else int(x)\n            inp = {\"entry_id\": r.entry_id, \"source\": r.source, \"version\": as_int(r.version), \"year\": as_int(r.year), \"code\": r.code,\n                   \"label\": r.label, \"label_norm\": r.label_norm, \"alt_labels\": list(r.alt_labels)[:20],\n                   \"descriptor\": r.descriptor if isinstance(r.descriptor, str) else None, \"generic_label\": bool(r.generic)}\n            if fam == \"mesh\" and r.source == \"mesh\":\n                m = mesh.loc[r.code]\n                inp.update({\"date_introduced\": m.date_introduced, \"history_note\": m.history_note,\n                            \"mesh_year_best\": m.mesh_year_best, \"mesh_year_rule\": m.mesh_year_rule,\n                            \"mesh_baseline\": bool(m.mesh_baseline), \"tree_numbers\": list(m.tree_numbers)[:12],\n                            \"top_branches\": list(m.top_branches)})\n            if fam == \"lists\":\n                li = lst.loc[r.entry_id]\n                inp.update({\"role\": li.role, \"rank\": None if pd.isna(li[\"rank\"]) else int(li[\"rank\"]), \"phase\": li.phase,\n                            \"wiki_links\": list(li.wiki_links), \"url\": li.url, \"primary_ref\": li.primary_ref})\n            ex.append({\"input\": dumps(inp), \"output\": dumps({\"matched_concepts\": matched, \"n_matched\": len(matched)}),\n                       \"metadata_source\": r.source, \"metadata_family\": fam,\n                       \"metadata_year\": None if r.year is None or pd.isna(r.year) else int(r.year),\n                       \"metadata_year_known\": fam != \"jel\", \"metadata_n_matched\": len(matched),\n                       \"metadata_entry_id\": r.entry_id})\n        ds.append({\"dataset\": name, \"examples\": ex})\n    # 8 match_verifications\n    ex = []\n    for r in v.itertuples(index=False):\n        en = e.loc[r.entry_id] if r.entry_id in e.index else None\n        ex.append({\"input\": dumps({\"entry_id\": r.entry_id, \"entry_text\": None if en is None else en.label,\n                                   \"entry_source\": None if en is None else en.source,\n                                   \"candidate_openalex_id\": r.openalex_id,\n                                   \"candidate_label\": k.at[r.openalex_id, \"label\"] if r.openalex_id in k.index else None,\n                                   \"candidate_methods\": list(r.methods)}),\n                   \"output\": dumps({\"relation\": r.relation, \"confidence\": r.confidence, \"accepted\": r.relation in ACCEPT}),\n                   \"metadata_task\": r.task, \"metadata_model\": r.model, \"metadata_prompt_hash\": r.prompt_hash,\n                   \"metadata_cost_usd\": float(r.cost or 0.0), \"metadata_status\": r.status,\n                   \"metadata_family\": None if en is None else en.family})\n    ds.append({\"dataset\": \"match_verifications\", \"examples\": ex})\n    # 9 crosswalk\n    xw = pd.read_csv(OUT / \"crosswalk_level1_to_field.csv\")\n    ds.append({\"dataset\": \"crosswalk_level1_to_field\", \"examples\": [\n        {\"input\": dumps({\"openalex_id\": r.openalex_id, \"display_name\": r.display_name,\n                         \"level0_parents\": ast.literal_eval(r.level0_parents) if isinstance(r.level0_parents, str) else []}),\n         \"output\": dumps({\"field_id\": r.field_id, \"field_name\": r.field_name, \"decided_by\": r.decided_by, \"reason\": r.reason}),\n         \"metadata_model_a\": str(r.model_a), \"metadata_model_b\": str(r.model_b), \"metadata_decided_by\": r.decided_by}\n        for r in xw.itertuples(index=False)]})\n    # 10 spot check\n    sp = pd.read_csv(OUT / \"spotcheck_p78.csv\") if (OUT / \"spotcheck_p78.csv\").exists() else pd.DataFrame()\n    if len(sp):\n        ds.append({\"dataset\": \"spotcheck_p78\", \"examples\": [\n            {\"input\": dumps({\"concept\": r.concept, \"aliases_used\": [a for a in str(r.aliases_used).split(\"|\") if a and a != \"nan\"],\n                             \"t0\": None if pd.isna(r.t0) else int(r.t0), \"iter1_group\": None if pd.isna(r.iter1_group) else r.iter1_group,\n                             \"iter1_home\": None if pd.isna(r.iter1_home) else r.iter1_home}),\n             \"output\": dumps({\"joined\": bool(r.joined), \"openalex_id\": None if pd.isna(r.openalex_id) else r.openalex_id,\n                              \"oa_label\": None if pd.isna(r.oa_label) else r.oa_label,\n                              \"provisional_group\": None if pd.isna(r.provisional_group) else r.provisional_group,\n                              \"events\": [e for e in str(r.events).split(\"; \") if e and e != \"nan\"],\n                              \"sources_checked\": json.loads(r.sources_checked) if isinstance(r.sources_checked, str) else None}),\n             \"metadata_joined\": bool(r.joined), \"metadata_iter1_status\": r.iter1_status}\n            for r in sp.itertuples(index=False)]})\n    return ds\n\n\ndef write_parts(ds: list[dict]) -> list[str]:\n    d = ROOT / \"full_data_out\"\n    d.mkdir(exist_ok=True)\n    for f in d.glob(\"full_data_out_*.json\"):\n        f.unlink()\n    parts, cur, cur_bytes = [], [], 0\n    meta = {\"description\": \"External, dated recognition events for OpenAlex legacy concepts (zero OpenAlex credits). \"\n                           \"See README.md for field definitions, source biases and lags.\",\n            \"parts_note\": \"Datasets are split across numbered parts; concatenate examples of equal 'dataset' names.\"}\n    for d_ in ds:\n        chunk = []\n        for x in d_[\"examples\"]:\n            sz = len(dumps(x)) + 2\n            if cur_bytes + sz > PART_BYTES and (chunk or cur):\n                if chunk:\n                    cur.append({\"dataset\": d_[\"dataset\"], \"examples\": chunk})\n                parts.append(cur)\n                cur, chunk, cur_bytes = [], [], 0\n            chunk.append(x)\n            cur_bytes += sz\n        if chunk:\n            cur.append({\"dataset\": d_[\"dataset\"], \"examples\": chunk})\n    if cur:\n        parts.append(cur)\n    names = []\n    for i, p in enumerate(parts, 1):\n        f = d / f\"full_data_out_{i}.json\"\n        f.write_text(json.dumps({\"metadata\": meta | {\"part\": i, \"n_parts\": len(parts)}, \"datasets\": p}, ensure_ascii=False))\n        names.append(str(f.relative_to(ROOT)))\n    return names\n\n\ndef trunc(x, n=300):\n    if isinstance(x, str):\n        return x if len(x) <= n else x[:n] + \"...\"\n    if isinstance(x, list):\n        return [trunc(y, n) for y in x]\n    if isinstance(x, dict):\n        return {k_: trunc(v_, n) for k_, v_ in x.items()}\n    return x\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    setup_logging(\"s9_outputs\")\n    R = pd.read_pickle(WORK / \"concept_rows.pkl\")\n    agr = json.loads((OUT / \"llm_agreement.json\").read_text())\n    rep = coverage(R, agr)\n    (OUT / \"coverage_report.json\").write_text(json.dumps(rep, indent=1, default=str))\n    logger.info(f\"coverage by source: \" + json.dumps({s: (d['n_with_event'], d['n_with_year_usable_event']) for s, d in rep['by_source'].items()}))\n    logger.info(f\"groups without dated domain taxonomy: {rep['groups_without_dated_domain_taxonomy']}\")\n    sp = spot_p78(R)\n    if len(sp):\n        sp.to_csv(OUT / \"spotcheck_p78.csv\", index=False)\n        logger.info(f\"P78 join rate {sp.joined.mean():.3f} ({sp.joined.sum()}/{len(sp)})\")\n    ds = build_datasets(R)\n    names = write_parts(ds)\n    logger.info(f\"full parts: {names}\")\n    rnd = random.Random(0)\n    mini, prev = [], []\n    for d_ in ds:\n        exs = d_[\"examples\"]\n        if d_[\"dataset\"] == \"concept_recognition\":\n            by = defaultdict(list)\n            for x in exs:\n                if x[\"metadata_level\"] >= 2:\n                    by[x[\"metadata_group\"]].append(x)\n            m = []\n            per = max(1, 200 // len(by))\n            for g in sorted(by):\n                cand = sorted(by[g], key=lambda x: -x[\"metadata_n_events\"])[:per // 2] + rnd.sample(by[g], min(len(by[g]), per - per // 2))\n                m += cand\n            m = m[:200]\n        else:\n            m = exs[:200] if len(exs) <= 200 else rnd.sample(exs, 200)\n        mini.append({\"dataset\": d_[\"dataset\"], \"examples\": m})\n        prev.append({\"dataset\": d_[\"dataset\"], \"examples\": trunc(m[:10])})\n    (ROOT / \"mini_data_out.json\").write_text(json.dumps({\"datasets\": mini}, ensure_ascii=False, indent=1))\n    (ROOT / \"preview_data_out.json\").write_text(json.dumps({\"datasets\": prev}, ensure_ascii=False, indent=1))\n    logger.info(\"mini and preview written; dataset sizes \" + json.dumps({d_[\"dataset\"]: len(d_[\"examples\"]) for d_ in ds}))\n\n\nif __name__ == \"__main__\":\n    main()\ntotal 52736\ndrwxrwxrwx  2 aii-agent aii-agent  2004763 Sep 28 21:21 .\ndrwxrwxrwx 10 aii-agent aii-agent  2041367 Sep 28 21:21 ..\n-rw-rw-rw-  1 aii-agent aii-agent   764423 Sep 28 19:40 candidates.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 18279859 Sep 28 17:57 concept_keys.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  9876985 Sep 28 17:24 concepts.parquet\n-rw-rw-rw-  1 aii-agent aii-agent      434 Sep 28 17:24 concepts_level_counts.json\n-rw-rw-rw-  1 aii-agent aii-agent    29680 Sep 28 17:42 crosswalk_disagreements.csv\n-rw-rw-rw-  1 aii-agent aii-agent    65071 Sep 28 17:42 crosswalk_raw.csv\n-rw-rw-rw-  1 aii-agent aii-agent  9944738 Sep 28 19:35 entries.parquet\n-rw-rw-rw-  1 aii-agent aii-agent     3278 Sep 28 18:46 hand_check_lists_v2.csv\n-rw-rw-rw-  1 aii-agent aii-agent     3649 Sep 28 19:45 hand_check_rf.csv\n-rw-rw-rw-  1 aii-agent aii-agent    10501 Sep 28 18:25 hand_check_sample.csv\n-rw-rw-rw-  1 aii-agent aii-agent   610627 Sep 28 19:54 links.parquet\n-rw-rw-rw-  1 aii-agent aii-agent   229149 Sep 28 19:34 list_entries.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  7312866 Sep 28 17:29 mesh_desc.parquet\n-rw-rw-rw-  1 aii-agent aii-agent      294 Sep 28 17:29 mesh_stats.json\n-rw-rw-rw-  1 aii-agent aii-agent   127878 Sep 28 18:04 mesh_supp.parquet\n-rw-rw-rw-  1 aii-agent aii-agent     2863 Sep 28 17:32 openalex_fields.csv\n-rw-rw-rw-  1 aii-agent aii-agent      238 Sep 28 19:35 p486_not_in_desc.csv\n-rw-rw-rw-  1 aii-agent aii-agent    63210 Sep 28 19:22 research_fronts.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  1216340 Sep 28 18:04 tax_entries.parquet\n-rw-rw-rw-  1 aii-agent aii-agent  1400811 Sep 28 19:41 verifications.parquet\n-rw-rw-rw-  1 aii-agent aii-agent     4187 Sep 28 19:37 wikilink_resolution.json\n-rw-rw-rw-  1 aii-agent aii-agent     2103 Sep 28 19:54 wp_calibration.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-29 21:13:06 UTC

```
Inspect mini data structure:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; python3 -c "
import json,collections
d=json.load(open('$W/mini_data_out.json'))
for x in d['datasets']:
    ex=x['examples']; print(x['dataset'],len(ex), sum(len(json.dumps(e)) for e in ex)//len(ex))
cr=d['datasets'][0]['examples']
print(collections.Counter(e['metadata_group'] for e in cr))
print(collections.Counter(e['metadata_fold'] for e in cr))
o=json.loads(cr[0]['output']); print(list(o.keys())); print(o['sources_checked']); print(o.get('present_day'))
print(collections.Counter(ev['source'] for e in cr for ev in json.loads(e['output'])['events']))
"
```

### [15] TOOL RESULT — Bash · 2026-09-29 21:13:08 UTC

```
{"stdout": "concept_recognition 200 5290\nexternal_entries_mesh 200 1149\nexternal_entries_acm_ccs 200 717\nexternal_entries_msc 200 593\nexternal_entries_pacs_physh 200 715\nexternal_entries_jel 200 572\nexternal_entries_curated_lists 200 1146\nmatch_verifications 200 601\ncrosswalk_level1_to_field 200 418\nspotcheck_p78 78 930\nCounter({'BGM': 20, 'CS': 20, 'Eng': 20, 'LifeEnv': 20, 'MathDec': 20, 'Med': 20, 'Physical': 20, 'Social': 20, 'unassigned_health': 20, 'unassigned_multi': 20})\nCounter({'dev': 80, 'heldout': 80, 'unassigned': 40})\n['events', 'sources_checked', 'present_day']\n{'wikidata': 'not_found', 'wikipedia_en': 'found_estimated', 'mesh': 'found', 'acm_ccs': 'not_applicable', 'msc': 'not_applicable', 'pacs_physh': 'not_applicable', 'jel': 'not_applicable', 'nature_methods_moty': 'found', 'science_boty': 'found', 'physics_world_boty': 'not_applicable', 'mit_tr10': 'found', 'gartner_hype_cycle': 'not_found', 'research_fronts': 'found'}\n{'year_known': False, 'n_wiki_sitelinks': 23, 'openalex_works_count': 50848, 'openalex_cited_by_count': 1486752, 'wikidata_n_claims': 19, 'wikidata_instance_of': [], 'wikidata_subclass_of': ['Q7692404', 'Q65363531'], 'wikidata_part_of': [], 'mesh_tree_codes_wikidata': [], 'jel': [], 'wikidata_mag_id_matches_openalex': True}\nCounter({'gartner_hype_cycle': 319, 'wikipedia_en': 200, 'mesh': 134, 'research_fronts': 112, 'pacs_physh': 96, 'acm_ccs': 93, 'msc': 81, 'mit_tr10': 40, 'physics_world_boty': 16, 'wikidata': 14, 'nature_methods_moty': 10, 'science_boty': 8})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-29 21:13:16 UTC

```
Create curated mini_demo_data.json:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_2/art_O7Dq4L02QnDN && python3 -c "
import json,random,collections
rnd=random.Random(0)
d=json.load(open('$W/mini_data_out.json'))
out=[]
for x in d['datasets']:
    ex=x['examples']
    if x['dataset']=='concept_recognition':
        by=collections.defaultdict(list)
        for e in ex: by[e['metadata_group']].append(e)
        m=[]
        for g in sorted(by):
            s=sorted(by[g],key=lambda e:-e['metadata_n_events'])
            m+=s[:2]+rnd.sample(s[2:],2)
    else:
        m=rnd.sample(ex,6)
    out.append({'dataset':x['dataset'],'examples':m})
meta={'description':'Demo subset of the external-recognition lookup table for OpenAlex legacy concepts (outcome O5): 40 concept_recognition rows (4 per provisional group) + 6 rows from each of the 9 other datasets, sampled from mini_data_out.json.','source_artifact':'art_O7Dq4L02QnDN','n_examples':{o['dataset']:len(o['examples']) for o in out}}
json.dump({'metadata':meta,'datasets':out},open('mini_demo_data.json','w'),ensure_ascii=False,indent=1)
print(meta['n_examples'], sum(meta['n_examples'].values()))
print([json.loads(e['input'])['label'] for e in out[0]['examples']])
"; ls -la mini_demo_data.json
```

### [17] TOOL RESULT — Bash · 2026-09-29 21:13:16 UTC

```
{"stdout": "{'concept_recognition': 40, 'external_entries_mesh': 6, 'external_entries_acm_ccs': 6, 'external_entries_msc': 6, 'external_entries_pacs_physh': 6, 'external_entries_jel': 6, 'external_entries_curated_lists': 6, 'match_verifications': 6, 'crosswalk_level1_to_field': 6, 'spotcheck_p78': 6} 94\n['Genome editing', 'Proteomics', 'Phytoplasma', 'CD146', 'Robotics', 'Analytics', 'Autonomous robot', 'Adversarial machine learning', '3d printed', '3d printer', 'Pallet', 'Crushed stone', 'Neural system', 'Genetic algorithm', 'Cichorium', 'Niclosamide', 'Stochastic process', 'Discrete-time stochastic process', 'Sampling time', 'Spatial network', 'Coronavirus disease 2019 (COVID-19)', 'Severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2)', 'Nerve conduction', 'Hypoactivity', '3D printing', 'Three dimensional printing', 'Microplastics', 'Pressure measurement', 'Cloud service provider', 'Social network analysis', 'Resource allocation', 'Game theory', 'Temporomandibular Joint Disorder', 'Temporomandibular disorder', 'End-of-life care', 'Tooth Abnormality', 'Cloud computing', 'Brain–computer interface', 'Allergic asthma', 'Generative model']\n-rw-rw-rw- 1 aii-agent aii-agent 375925 Sep 29 21:13 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-29 21:13:20 UTC

```
I've built `mini_demo_data.json`, a 94-row subset. Next I'm writing the notebook and test-running it.
```

### [19] TOOL CALL — Bash · 2026-09-29 21:13:20 UTC

```
Ensure scratchpad exists:
mkdir -p /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad && echo ok
```

### [20] TOOL RESULT — Bash · 2026-09-29 21:13:20 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Write · 2026-09-29 21:14:34 UTC

```
File: /tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/build_nb.py

"""Builds code_demo.ipynb for art_O7Dq4L02QnDN (data.py -> notebook with minimal changes)."""
import json
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
cells = []


def md(s):
    cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n").splitlines(keepends=True)})


def code(s):
    cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [],
                  "source": s.strip("\n").splitlines(keepends=True)})


md(r"""
# When research concepts were officially recognised: external-recognition lookup table (O5)

This notebook demonstrates the **final assembly step (`data.py`)** of a dataset that records, for all **65,026 OpenAlex
legacy concepts** (64,723 targets at levels 2-5), *when* each concept was recognised by an external authority. It cost
no OpenAlex credits and $1.49 of OpenRouter calls.

Every recognition **event** is dated and sourced. Each event carries `year_usable`, `match_method`, `match_confidence`
and `relation`, where `relation` is one of `same`, `narrower` or `broader`, stated from the external entry's side. The sources are:

| Source | What counts as an event |
|---|---|
| MeSH 2026 | `DateIntroduced` year (years <=1966 flagged `mesh_baseline`) |
| English Wikipedia | page creation date: exact first revision, or a calibrated page-id estimate |
| Wikidata | P571 (inception) / P575 (time of discovery) |
| ACM CCS 1998/2012, MSC 2000/2010/2020, PACS 2010/PhySH | `taxonomy_in_version`, `taxonomy_added_between` |
| Nature Methods MoTY, Science BOTY, Physics World BOTY, MIT TR10, Gartner Hype Cycle, Clarivate/CAS Research Fronts | curated list appearances |
| JEL | present-day membership only (undated) |

Present-day facts sit in a separate `present_day` block (`year_known=false`). `sources_checked` records
`found` / `not_found` / `not_applicable` for every concept and source.

**What `data.py` does.** It takes the processed pipeline tables (`work/*.parquet`, `work/concept_rows.pkl`) and runs
`build_datasets()` to standardise them into **10 datasets** in the `exp_sel_data_out` schema. It checks the schema,
writes `full_data_out.json`, splits the file into parts above 95 MB, and writes the mini and preview variants.

**In this demo.** The heavy upstream parquet/pickle files (about 50 MB, built by ~20 pipeline scripts and LLM calls) are
not shipped. So the notebook loads a **94-row curated subset** of the already standardised datasets
(`mini_demo_data.json`: 40 concept rows, 4 from each provisional group, plus 6 rows from each of the other 9 datasets).
It then runs the original checking, writing, splitting and mini/preview code from `data.py` on that subset. The last
section visualises the recognition events.
""")

md(r"""
## 1. Install dependencies
`loguru` is not pre-installed on Colab, so it is always installed. `pandas` and `matplotlib` are pre-installed on Colab
and are only installed locally, pinned to Colab's versions.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT on Colab, always install
_pip('loguru==0.7.3')

# pandas, matplotlib (+ pyarrow for pandas) — pre-installed on Colab, install locally only
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'pyarrow==18.1.0', 'matplotlib==3.10.0')
""")

md(r"""
## 2. Imports
This is the original import block of `data.py`. There are two notebook changes:
- `ROOT` was the script's directory. Here it is a local `demo_output/` folder, so the generated files stay separate.
- The original imported `build_datasets, trunc, write_parts` from `scripts/s9_outputs.py`. `build_datasets` needs the
  upstream parquet tables, so this demo replaces it with the pre-built datasets. The copied `trunc` and `write_parts`
  are defined in section 5.
""")

code(r"""
from __future__ import annotations

import json
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("demo_output")  # original: Path(__file__).resolve().parent
ROOT.mkdir(exist_ok=True)
# original: sys.path.insert(0, str(ROOT / "scripts"))

import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

# original: from s9_outputs import build_datasets, trunc, write_parts  # noqa: E402
#   -> trunc / write_parts (and their helpers clean / dumps) are copied from scripts/s9_outputs.py below;
#      build_datasets() is replaced by the pre-built datasets loaded from mini_demo_data.json.

# extra imports for the visualisation section
import matplotlib.pyplot as plt
""")

md(r"""
## 3. Data loading
The notebook first tries the GitHub URL, which works in Colab after the repository is published, and then falls back to a
local `mini_demo_data.json`.
""")

code(r"""
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json"
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
print({d["dataset"]: len(d["examples"]) for d in data["datasets"]})
""")

md(r"""
## 4. Configuration
These are all the tunable constants of `data.py` and `s9_outputs.py`. The original values are in the comments.
The mini, preview and truncation sizes use their original values, because the whole notebook runs in seconds.
The two **size limits are scaled down** so that the ~0.4 MB demo subset still goes through the
"too big, split into parts" branch. At the original 95 MB and 90 MB limits, the demo file would never be split.
""")

code(r"""
LIMIT_BYTES = 200_000       # original: 95_000_000 -> above this, full_data_out.json is split into parts
PART_BYTES = 150_000        # original: 90_000_000 (s9_outputs.PART_BYTES) -> max bytes per full_data_out_<n>.json
MINI_PER_DATASET = 200      # original: 200 -> max examples per dataset in mini_data_out.json
PREVIEW_N = 10              # original: 10  -> examples per dataset in preview_data_out.json
TRUNC_N = 300               # original: 300 -> max string length in preview_data_out.json
SEED = 0                    # original: 0   -> random.Random seed for mini sampling
REQUIRED = ("input", "output")
""")

md(r"""
## 5. Helpers copied from `scripts/s9_outputs.py`
These functions are copied unchanged, apart from `n=TRUNC_N` in `trunc`:
- `clean` / `dumps` convert values to strict JSON: numpy becomes Python, and NaN or inf becomes `null`.
- `write_parts` implements the file-size rule. It streams examples into numbered part files of at most `PART_BYTES`
  each. Each part is a valid `exp_sel_data_out` document, and a dataset may continue into the next part.
- `trunc` shortens long strings for the preview file.
""")

code(r"""
def clean(x):
    '''Recursively convert numpy scalars/arrays to Python and NaN/inf to None (strict JSON).'''
    import math
    if isinstance(x, dict):
        return {str(k_): clean(v_) for k_, v_ in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(y) for y in x]
    if hasattr(x, "tolist") and not isinstance(x, (str, bytes)):
        return clean(x.tolist())
    if isinstance(x, float):
        return None if (math.isnan(x) or math.isinf(x)) else x
    return x


def dumps(x) -> str:
    return json.dumps(clean(x), ensure_ascii=False, allow_nan=False, default=str)


def write_parts(ds: list[dict]) -> list[str]:
    d = ROOT / "full_data_out"
    d.mkdir(exist_ok=True)
    for f in d.glob("full_data_out_*.json"):
        f.unlink()
    parts, cur, cur_bytes = [], [], 0
    meta = {"description": "External, dated recognition events for OpenAlex legacy concepts (zero OpenAlex credits). "
                           "See README.md for field definitions, source biases and lags.",
            "parts_note": "Datasets are split across numbered parts; concatenate examples of equal 'dataset' names."}
    for d_ in ds:
        chunk = []
        for x in d_["examples"]:
            sz = len(dumps(x)) + 2
            if cur_bytes + sz > PART_BYTES and (chunk or cur):
                if chunk:
                    cur.append({"dataset": d_["dataset"], "examples": chunk})
                parts.append(cur)
                cur, chunk, cur_bytes = [], [], 0
            chunk.append(x)
            cur_bytes += sz
        if chunk:
            cur.append({"dataset": d_["dataset"], "examples": chunk})
    if cur:
        parts.append(cur)
    names = []
    for i, p in enumerate(parts, 1):
        f = d / f"full_data_out_{i}.json"
        f.write_text(json.dumps({"metadata": meta | {"part": i, "n_parts": len(parts)}, "datasets": p}, ensure_ascii=False))
        names.append(str(f.relative_to(ROOT)))
    return names


def trunc(x, n=TRUNC_N):  # original default: n=300
    if isinstance(x, str):
        return x if len(x) <= n else x[:n] + "..."
    if isinstance(x, list):
        return [trunc(y, n) for y in x]
    if isinstance(x, dict):
        return {k_: trunc(v_, n) for k_, v_ in x.items()}
    return x
""")

md(r"""
## 6. `data.py`: schema checks and mini/preview sampling
- `check()` runs the checks that the schema validator does not. There must be exactly **10 distinct datasets**, each
  non-empty. Every example needs string `input` and `output` fields, and all other keys must be flat `metadata_*` fields.
- `mini_preview()` builds `mini_data_out.json`. For **`concept_recognition`** it stratifies over the provisional
  hypothesis groups: in each group, half the rows are the richest (most events) and half are random target rows at level >=2.
  Every other dataset gets a random sample of up to `MINI_PER_DATASET`. `preview_data_out.json` holds the first
  `PREVIEW_N` rows of each dataset, with truncated strings.

The code is the original, except that the literals 200 and 10 now come from the config variables. With only 4 concept
rows per group in the demo subset, the "richest" and "random" halves overlap, so some mini rows repeat. With the
full 65k rows they rarely do.
""")

code(r"""
def check(ds: list[dict]) -> None:
    '''Schema-level checks the validator does not do: one example per row, string input/output, flat metadata.'''
    names = [d["dataset"] for d in ds]
    assert len(names) == len(set(names)) == 10, names
    for d in ds:
        assert d["examples"], d["dataset"]
        for x in d["examples"]:
            assert all(isinstance(x[k], str) for k in REQUIRED)
            bad = [k for k in x if k not in REQUIRED and not k.startswith("metadata_")]
            assert not bad, (d["dataset"], bad)
            assert not any(isinstance(v, dict) for k, v in x.items() if k.startswith("metadata_")), d["dataset"]


def mini_preview(ds: list[dict]) -> None:
    rnd = random.Random(SEED)
    mini, prev = [], []
    for d in ds:
        exs = d["examples"]
        if d["dataset"] == "concept_recognition":
            by = defaultdict(list)
            for x in exs:
                if x["metadata_level"] >= 2:
                    by[x["metadata_group"]].append(x)
            per = max(1, MINI_PER_DATASET // len(by))
            m = []
            for g in sorted(by):   # half the richest rows, half random, per provisional group
                m += sorted(by[g], key=lambda x: -x["metadata_n_events"])[:per // 2]
                m += rnd.sample(by[g], min(len(by[g]), per - per // 2))
            m = m[:MINI_PER_DATASET]
        else:
            m = exs if len(exs) <= MINI_PER_DATASET else rnd.sample(exs, MINI_PER_DATASET)
        mini.append({"dataset": d["dataset"], "examples": m})
        prev.append({"dataset": d["dataset"], "examples": trunc(m[:PREVIEW_N])})
    (ROOT / "mini_data_out.json").write_text(json.dumps({"datasets": mini}, ensure_ascii=False, indent=1))
    (ROOT / "preview_data_out.json").write_text(json.dumps({"datasets": prev}, ensure_ascii=False, indent=1))
""")

md(r"""
## 7. `data.py`: `main()`
This is the original `main()`, with one change. The original loaded `work/concept_rows.pkl` into `R` and called
`build_datasets(R)`, which joins concept rows, taxonomy/list entries, links and LLM verifications into the 10 datasets.
Here `ds` comes straight from the loaded demo data, which is exactly the structure `build_datasets` returns.
The rest is unchanged: check, count, fold summary, write `full_data_out.json`, split it when it is above `LIMIT_BYTES`,
then write the mini and preview files.
""")

code(r"""
@logger.catch(reraise=True)
def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")
    # original: R = pd.read_pickle(ROOT / "work" / "concept_rows.pkl")
    #           logger.info(f"concept rows {len(R)}")
    #           ds = build_datasets(R)
    ds = data["datasets"]
    logger.info(f"concept rows {len(ds[0]['examples'])}")
    check(ds)
    counts = {d["dataset"]: len(d["examples"]) for d in ds}
    logger.info(f"datasets: {counts}")
    fold = Counter(x["metadata_fold"] for x in ds[0]["examples"])
    logger.info(f"concept_recognition folds: {dict(fold)}")
    out = ROOT / "full_data_out.json"
    body = json.dumps({"metadata": {"description": "External, dated recognition events for OpenAlex legacy concepts",
                                    "n_examples": counts}, "datasets": ds}, ensure_ascii=False)
    out.write_text(body)
    size = out.stat().st_size
    logger.info(f"full_data_out.json {size / 1e6:.1f} MB")
    if size > LIMIT_BYTES:
        parts = write_parts(ds)
        out.unlink()
        logger.info(f"above {LIMIT_BYTES / 1e6:.1f} MB -> split into {parts}; single file removed")
    mini_preview(ds)
    logger.info("mini_data_out.json and preview_data_out.json written")


main()
""")

md(r"""
## 8. Check the written files
The split parts must reassemble to exactly the input datasets. This is the "concatenate examples of equal
`dataset` names" rule from the parts note.
""")

code(r"""
for f in sorted(ROOT.rglob("*.json")):
    print(f"{str(f.relative_to(ROOT)):40s} {f.stat().st_size / 1e3:8.1f} kB")

merged = defaultdict(list)
for f in sorted((ROOT / "full_data_out").glob("full_data_out_*.json"), key=lambda p: int(p.stem.split("_")[-1])):
    for d in json.loads(f.read_text())["datasets"]:
        merged[d["dataset"]] += d["examples"]
assert {k: len(v) for k, v in merged.items()} == {d["dataset"]: len(d["examples"]) for d in data["datasets"]}
print("parts reassemble to the input datasets:", {k: len(v) for k, v in merged.items()})
""")

md(r"""
## 9. Results: the recognition events of the demo concepts
Each `concept_recognition` row has a JSON `input` (concept identity: label, aliases, level, ancestors) and a JSON `output`
(`events`, `sources_checked`, `present_day`). The code below expands the events and shows:
1. one row per concept with its earliest usable recognition year and the source that gave it,
2. event counts per source, split into usable and unusable years,
3. the distribution of usable event years (note the Wikipedia 2001-2007 growth wave),
4. `sources_checked` status per source (`found` / `not_found` / `not_applicable`).
""")

code(r"""
rows, evs, chk = [], [], []
for x in data["datasets"][0]["examples"]:
    inp, out = json.loads(x["input"]), json.loads(x["output"])
    usable = [e for e in out["events"] if e["year_usable"] and e["year"] is not None]
    first = min(usable, key=lambda e: e["year"]) if usable else None
    rows.append({"label": inp["label"][:40], "level": x["metadata_level"], "group": x["metadata_group"],
                 "fold": x["metadata_fold"], "n_events": x["metadata_n_events"],
                 "n_usable": x["metadata_n_events_year_usable"],
                 "first_year": first["year"] if first else None, "first_source": first["source"] if first else None,
                 "first_relation": first["relation"] if first else None})
    for e in out["events"]:
        evs.append({"source": e["source"], "year": e["year"], "year_usable": e["year_usable"],
                    "match_method": e["match_method"], "relation": e["relation"]})
    for s, st in out["sources_checked"].items():
        chk.append({"source": s, "status": st})

C, E, K = pd.DataFrame(rows), pd.DataFrame(evs), pd.DataFrame(chk)
pd.set_option("display.width", 200)
print(C.sort_values(["group", "n_events"], ascending=[True, False]).to_string(index=False))
print("\nevents by match_method:\n", E.match_method.value_counts().to_string())
print("\nevents by relation:\n", E.relation.value_counts().to_string())
""")

code(r"""
fig, ax = plt.subplots(1, 3, figsize=(18, 5))

# (a) events per source, usable vs not
t = E.groupby(["source", "year_usable"]).size().unstack(fill_value=0).reindex(columns=[True, False], fill_value=0)
t = t.loc[t.sum(axis=1).sort_values().index]
t.plot.barh(stacked=True, ax=ax[0], color=["#2a7ab9", "#c8c8c8"])
ax[0].set_title("Recognition events per source (40 demo concepts)")
ax[0].set_xlabel("events"); ax[0].set_ylabel(""); ax[0].legend(["year_usable", "not usable"], frameon=False)

# (b) usable event years
yrs = E[E.year_usable & E.year.notna()]
for s, c in [("wikipedia_en", "#2a7ab9"), ("mesh", "#e08a2e")]:
    ax[1].hist(yrs[yrs.source == s].year, bins=range(1940, 2030, 3), alpha=0.7, label=s, color=c)
ax[1].hist(yrs[~yrs.source.isin(["wikipedia_en", "mesh"])].year, bins=range(1940, 2030, 3), alpha=0.5,
           label="taxonomies + curated lists + wikidata", color="#5a9e4b")
ax[1].set_title("Years of usable recognition events"); ax[1].set_xlabel("year"); ax[1].legend(frameon=False)

# (c) sources_checked status
st = K.groupby(["source", "status"]).size().unstack(fill_value=0)
st = st.loc[st.get("not_applicable", 0).sort_values(ascending=False).index] if "not_applicable" in st else st
st.plot.barh(stacked=True, ax=ax[2], colormap="tab20")
ax[2].set_title("sources_checked status per source"); ax[2].set_xlabel("concepts"); ax[2].set_ylabel("")
ax[2].legend(fontsize=8, frameon=False)
plt.tight_layout()
plt.show()
""")

code(r"""
# earliest usable recognition year per provisional group (only concepts with any usable event)
g = C.dropna(subset=["first_year"]).groupby("group").first_year.agg(["count", "median", "min", "max"])
print(g.to_string())
print("\nearliest-event source mix:\n", C.first_source.value_counts().to_string())
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                                   "language_info": {"name": "python"}},
      "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
OUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print("wrote", OUT)
```

### [22] TOOL RESULT — Write · 2026-09-29 21:14:34 UTC

```
{"type": "create", "filePath": "/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/build_nb.py", "content": "\"\"\"Builds code_demo.ipynb for art_O7Dq4L02QnDN (data.py -> notebook with minimal changes).\"\"\"\nimport json\nimport sys\nfrom pathlib import Path\n\nOUT = Path(sys.argv[1])\ncells = []\n\n\ndef md(s):\n    cells.append({\"cell_type\": \"markdown\", \"metadata\": {}, \"source\": s.strip(\"\\n\").splitlines(keepends=True)})\n\n\ndef code(s):\n    cells.append({\"cell_type\": \"code\", \"metadata\": {}, \"execution_count\": None, \"outputs\": [],\n                  \"source\": s.strip(\"\\n\").splitlines(keepends=True)})\n\n\nmd(r\"\"\"\n# When research concepts were officially recognised: external-recognition lookup table (O5)\n\nThis notebook demonstrates the **final assembly step (`data.py`)** of a dataset that records, for all **65,026 OpenAlex\nlegacy concepts** (64,723 targets at levels 2-5), *when* each concept was recognised by an external authority. It cost\nno OpenAlex credits and $1.49 of OpenRouter calls.\n\nEvery recognition **event** is dated and sourced. Each event carries `year_usable`, `match_method`, `match_confidence`\nand `relation`, where `relation` is one of `same`, `narrower` or `broader`, stated from the external entry's side. The sources are:\n\n| Source | What counts as an event |\n|---|---|\n| MeSH 2026 | `DateIntroduced` year (years <=1966 flagged `mesh_baseline`) |\n| English Wikipedia | page creation date: exact first revision, or a calibrated page-id estimate |\n| Wikidata | P571 (inception) / P575 (time of discovery) |\n| ACM CCS 1998/2012, MSC 2000/2010/2020, PACS 2010/PhySH | `taxonomy_in_version`, `taxonomy_added_between` |\n| Nature Methods MoTY, Science BOTY, Physics World BOTY, MIT TR10, Gartner Hype Cycle, Clarivate/CAS Research Fronts | curated list appearances |\n| JEL | present-day membership only (undated) |\n\nPresent-day facts sit in a separate `present_day` block (`year_known=false`). `sources_checked` records\n`found` / `not_found` / `not_applicable` for every concept and source.\n\n**What `data.py` does.** It takes the processed pipeline tables (`work/*.parquet`, `work/concept_rows.pkl`) and runs\n`build_datasets()` to standardise them into **10 datasets** in the `exp_sel_data_out` schema. It checks the schema,\nwrites `full_data_out.json`, splits the file into parts above 95 MB, and writes the mini and preview variants.\n\n**In this demo.** The heavy upstream parquet/pickle files (about 50 MB, built by ~20 pipeline scripts and LLM calls) are\nnot shipped. So the notebook loads a **94-row curated subset** of the already standardised datasets\n(`mini_demo_data.json`: 40 concept rows, 4 from each provisional group, plus 6 rows from each of the other 9 datasets).\nIt then runs the original checking, writing, splitting and mini/preview code from `data.py` on that subset. The last\nsection visualises the recognition events.\n\"\"\")\n\nmd(r\"\"\"\n## 1. Install dependencies\n`loguru` is not pre-installed on Colab, so it is always installed. `pandas` and `matplotlib` are pre-installed on Colab\nand are only installed locally, pinned to Colab's versions.\n\"\"\")\n\ncode(r\"\"\"\nimport subprocess, sys\ndef _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])\n\n# loguru — NOT on Colab, always install\n_pip('loguru==0.7.3')\n\n# pandas, matplotlib (+ pyarrow for pandas) — pre-installed on Colab, install locally only\nif 'google.colab' not in sys.modules:\n    _pip('numpy==2.0.2', 'pandas==2.2.2', 'pyarrow==18.1.0', 'matplotlib==3.10.0')\n\"\"\")\n\nmd(r\"\"\"\n## 2. Imports\nThis is the original import block of `data.py`. There are two notebook changes:\n- `ROOT` was the script's directory. Here it is a local `demo_output/` folder, so the generated files stay separate.\n- The original imported `build_datasets, trunc, write_parts` from `scripts/s9_outputs.py`. `build_datasets` needs the\n  upstream parquet tables, so this demo replaces it with the pre-built datasets. The copied `trunc` and `write_parts`\n  are defined in section 5.\n\"\"\")\n\ncode(r\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport random\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nROOT = Path(\"demo_output\")  # original: Path(__file__).resolve().parent\nROOT.mkdir(exist_ok=True)\n# original: sys.path.insert(0, str(ROOT / \"scripts\"))\n\nimport pandas as pd  # noqa: E402\nfrom loguru import logger  # noqa: E402\n\n# original: from s9_outputs import build_datasets, trunc, write_parts  # noqa: E402\n#   -> trunc / write_parts (and their helpers clean / dumps) are copied from scripts/s9_outputs.py below;\n#      build_datasets() is replaced by the pre-built datasets loaded from mini_demo_data.json.\n\n# extra imports for the visualisation section\nimport matplotlib.pyplot as plt\n\"\"\")\n\nmd(r\"\"\"\n## 3. Data loading\nThe notebook first tries the GitHub URL, which works in Colab after the repository is published, and then falls back to a\nlocal `mini_demo_data.json`.\n\"\"\")\n\ncode(r\"\"\"\nGITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json\"\nimport json\nfrom pathlib import Path\n\ndef load_data():\n    try:\n        import urllib.request\n        with urllib.request.urlopen(GITHUB_DATA_URL) as response:\n            return json.loads(response.read().decode())\n    except Exception: pass\n    local = Path(\"mini_demo_data.json\")\n    if local.exists(): return json.loads(local.read_text())\n    raise FileNotFoundError(\"Could not load mini_demo_data.json\")\n\"\"\")\n\ncode(r\"\"\"\ndata = load_data()\nprint(data[\"metadata\"][\"description\"])\nprint({d[\"dataset\"]: len(d[\"examples\"]) for d in data[\"datasets\"]})\n\"\"\")\n\nmd(r\"\"\"\n## 4. Configuration\nThese are all the tunable constants of `data.py` and `s9_outputs.py`. The original values are in the comments.\nThe mini, preview and truncation sizes use their original values, because the whole notebook runs in seconds.\nThe two **size limits are scaled down** so that the ~0.4 MB demo subset still goes through the\n\"too big, split into parts\" branch. At the original 95 MB and 90 MB limits, the demo file would never be split.\n\"\"\")\n\ncode(r\"\"\"\nLIMIT_BYTES = 200_000       # original: 95_000_000 -> above this, full_data_out.json is split into parts\nPART_BYTES = 150_000        # original: 90_000_000 (s9_outputs.PART_BYTES) -> max bytes per full_data_out_<n>.json\nMINI_PER_DATASET = 200      # original: 200 -> max examples per dataset in mini_data_out.json\nPREVIEW_N = 10              # original: 10  -> examples per dataset in preview_data_out.json\nTRUNC_N = 300               # original: 300 -> max string length in preview_data_out.json\nSEED = 0                    # original: 0   -> random.Random seed for mini sampling\nREQUIRED = (\"input\", \"output\")\n\"\"\")\n\nmd(r\"\"\"\n## 5. Helpers copied from `scripts/s9_outputs.py`\nThese functions are copied unchanged, apart from `n=TRUNC_N` in `trunc`:\n- `clean` / `dumps` convert values to strict JSON: numpy becomes Python, and NaN or inf becomes `null`.\n- `write_parts` implements the file-size rule. It streams examples into numbered part files of at most `PART_BYTES`\n  each. Each part is a valid `exp_sel_data_out` document, and a dataset may continue into the next part.\n- `trunc` shortens long strings for the preview file.\n\"\"\")\n\ncode(r\"\"\"\ndef clean(x):\n    '''Recursively convert numpy scalars/arrays to Python and NaN/inf to None (strict JSON).'''\n    import math\n    if isinstance(x, dict):\n        return {str(k_): clean(v_) for k_, v_ in x.items()}\n    if isinstance(x, (list, tuple)):\n        return [clean(y) for y in x]\n    if hasattr(x, \"tolist\") and not isinstance(x, (str, bytes)):\n        return clean(x.tolist())\n    if isinstance(x, float):\n        return None if (math.isnan(x) or math.isinf(x)) else x\n    return x\n\n\ndef dumps(x) -> str:\n    return json.dumps(clean(x), ensure_ascii=False, allow_nan=False, default=str)\n\n\ndef write_parts(ds: list[dict]) -> list[str]:\n    d = ROOT / \"full_data_out\"\n    d.mkdir(exist_ok=True)\n    for f in d.glob(\"full_data_out_*.json\"):\n        f.unlink()\n    parts, cur, cur_bytes = [], [], 0\n    meta = {\"description\": \"External, dated recognition events for OpenAlex legacy concepts (zero OpenAlex credits). \"\n                           \"See README.md for field definitions, source biases and lags.\",\n            \"parts_note\": \"Datasets are split across numbered parts; concatenate examples of equal 'dataset' names.\"}\n    for d_ in ds:\n        chunk = []\n        for x in d_[\"examples\"]:\n            sz = len(dumps(x)) + 2\n            if cur_bytes + sz > PART_BYTES and (chunk or cur):\n                if chunk:\n                    cur.append({\"dataset\": d_[\"dataset\"], \"examples\": chunk})\n                parts.append(cur)\n                cur, chunk, cur_bytes = [], [], 0\n            chunk.append(x)\n            cur_bytes += sz\n        if chunk:\n            cur.append({\"dataset\": d_[\"dataset\"], \"examples\": chunk})\n    if cur:\n        parts.append(cur)\n    names = []\n    for i, p in enumerate(parts, 1):\n        f = d / f\"full_data_out_{i}.json\"\n        f.write_text(json.dumps({\"metadata\": meta | {\"part\": i, \"n_parts\": len(parts)}, \"datasets\": p}, ensure_ascii=False))\n        names.append(str(f.relative_to(ROOT)))\n    return names\n\n\ndef trunc(x, n=TRUNC_N):  # original default: n=300\n    if isinstance(x, str):\n        return x if len(x) <= n else x[:n] + \"...\"\n    if isinstance(x, list):\n        return [trunc(y, n) for y in x]\n    if isinstance(x, dict):\n        return {k_: trunc(v_, n) for k_, v_ in x.items()}\n    return x\n\"\"\")\n\nmd(r\"\"\"\n## 6. `data.py`: schema checks and mini/preview sampling\n- `check()` runs the checks that the schema validator does not. There must be exactly **10 distinct datasets**, each\n  non-empty. Every example needs string `input` and `output` fields, and all other keys must be flat `metadata_*` fields.\n- `mini_preview()` builds `mini_data_out.json`. For **`concept_recognition`** it stratifies over the provisional\n  hypothesis groups: in each group, half the rows are the richest (most events) and half are random target rows at level >=2.\n  Every other dataset gets a random sample of up to `MINI_PER_DATASET`. `preview_data_out.json` holds the first\n  `PREVIEW_N` rows of each dataset, with truncated strings.\n\nThe code is the original, except that the literals 200 and 10 now come from the config variables. With only 4 concept\nrows per group in the demo subset, the \"richest\" and \"random\" halves overlap, so some mini rows repeat. With the\nfull 65k rows they rarely do.\n\"\"\")\n\ncode(r\"\"\"\ndef check(ds: list[dict]) -> None:\n    '''Schema-level checks the validator does not do: one example per row, string input/output, flat metadata.'''\n    names = [d[\"dataset\"] for d in ds]\n    assert len(names) == len(set(names)) == 10, names\n    for d in ds:\n        assert d[\"examples\"], d[\"dataset\"]\n        for x in d[\"examples\"]:\n            assert all(isinstance(x[k], str) for k in REQUIRED)\n            bad = [k for k in x if k not in REQUIRED and not k.startswith(\"metadata_\")]\n            assert not bad, (d[\"dataset\"], bad)\n            assert not any(isinstance(v, dict) for k, v in x.items() if k.startswith(\"metadata_\")), d[\"dataset\"]\n\n\ndef mini_preview(ds: list[dict]) -> None:\n    rnd = random.Random(SEED)\n    mini, prev = [], []\n    for d in ds:\n        exs = d[\"examples\"]\n        if d[\"dataset\"] == \"concept_recognition\":\n            by = defaultdict(list)\n            for x in exs:\n                if x[\"metadata_level\"] >= 2:\n                    by[x[\"metadata_group\"]].append(x)\n            per = max(1, MINI_PER_DATASET // len(by))\n            m = []\n            for g in sorted(by):   # half the richest rows, half random, per provisional group\n                m += sorted(by[g], key=lambda x: -x[\"metadata_n_events\"])[:per // 2]\n                m += rnd.sample(by[g], min(len(by[g]), per - per // 2))\n            m = m[:MINI_PER_DATASET]\n        else:\n            m = exs if len(exs) <= MINI_PER_DATASET else rnd.sample(exs, MINI_PER_DATASET)\n        mini.append({\"dataset\": d[\"dataset\"], \"examples\": m})\n        prev.append({\"dataset\": d[\"dataset\"], \"examples\": trunc(m[:PREVIEW_N])})\n    (ROOT / \"mini_data_out.json\").write_text(json.dumps({\"datasets\": mini}, ensure_ascii=False, indent=1))\n    (ROOT / \"preview_data_out.json\").write_text(json.dumps({\"datasets\": prev}, ensure_ascii=False, indent=1))\n\"\"\")\n\nmd(r\"\"\"\n## 7. `data.py`: `main()`\nThis is the original `main()`, with one change. The original loaded `work/concept_rows.pkl` into `R` and called\n`build_datasets(R)`, which joins concept rows, taxonomy/list entries, links and LLM verifications into the 10 datasets.\nHere `ds` comes straight from the loaded demo data, which is exactly the structure `build_datasets` returns.\nThe rest is unchanged: check, count, fold summary, write `full_data_out.json`, split it when it is above `LIMIT_BYTES`,\nthen write the mini and preview files.\n\"\"\")\n\ncode(r\"\"\"\n@logger.catch(reraise=True)\ndef main() -> None:\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(ROOT / \"logs\" / \"data.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    # original: R = pd.read_pickle(ROOT / \"work\" / \"concept_rows.pkl\")\n    #           logger.info(f\"concept rows {len(R)}\")\n    #           ds = build_datasets(R)\n    ds = data[\"datasets\"]\n    logger.info(f\"concept rows {len(ds[0]['examples'])}\")\n    check(ds)\n    counts = {d[\"dataset\"]: len(d[\"examples\"]) for d in ds}\n    logger.info(f\"datasets: {counts}\")\n    fold = Counter(x[\"metadata_fold\"] for x in ds[0][\"examples\"])\n    logger.info(f\"concept_recognition folds: {dict(fold)}\")\n    out = ROOT / \"full_data_out.json\"\n    body = json.dumps({\"metadata\": {\"description\": \"External, dated recognition events for OpenAlex legacy concepts\",\n                                    \"n_examples\": counts}, \"datasets\": ds}, ensure_ascii=False)\n    out.write_text(body)\n    size = out.stat().st_size\n    logger.info(f\"full_data_out.json {size / 1e6:.1f} MB\")\n    if size > LIMIT_BYTES:\n        parts = write_parts(ds)\n        out.unlink()\n        logger.info(f\"above {LIMIT_BYTES / 1e6:.1f} MB -> split into {parts}; single file removed\")\n    mini_preview(ds)\n    logger.info(\"mini_data_out.json and preview_data_out.json written\")\n\n\nmain()\n\"\"\")\n\nmd(r\"\"\"\n## 8. Check the written files\nThe split parts must reassemble to exactly the input datasets. This is the \"concatenate examples of equal\n`dataset` names\" rule from the parts note.\n\"\"\")\n\ncode(r\"\"\"\nfor f in sorted(ROOT.rglob(\"*.json\")):\n    print(f\"{str(f.relative_to(ROOT)):40s} {f.stat().st_size / 1e3:8.1f} kB\")\n\nmerged = defaultdict(list)\nfor f in sorted((ROOT / \"full_data_out\").glob(\"full_data_out_*.json\"), key=lambda p: int(p.stem.split(\"_\")[-1])):\n    for d in json.loads(f.read_text())[\"datasets\"]:\n        merged[d[\"dataset\"]] += d[\"examples\"]\nassert {k: len(v) for k, v in merged.items()} == {d[\"dataset\"]: len(d[\"examples\"]) for d in data[\"datasets\"]}\nprint(\"parts reassemble to the input datasets:\", {k: len(v) for k, v in merged.items()})\n\"\"\")\n\nmd(r\"\"\"\n## 9. Results: the recognition events of the demo concepts\nEach `concept_recognition` row has a JSON `input` (concept identity: label, aliases, level, ancestors) and a JSON `output`\n(`events`, `sources_checked`, `present_day`). The code below expands the events and shows:\n1. one row per concept with its earliest usable recognition year and the source that gave it,\n2. event counts per source, split into usable and unusable years,\n3. the distribution of usable event years (note the Wikipedia 2001-2007 growth wave),\n4. `sources_checked` status per source (`found` / `not_found` / `not_applicable`).\n\"\"\")\n\ncode(r\"\"\"\nrows, evs, chk = [], [], []\nfor x in data[\"datasets\"][0][\"examples\"]:\n    inp, out = json.loads(x[\"input\"]), json.loads(x[\"output\"])\n    usable = [e for e in out[\"events\"] if e[\"year_usable\"] and e[\"year\"] is not None]\n    first = min(usable, key=lambda e: e[\"year\"]) if usable else None\n    rows.append({\"label\": inp[\"label\"][:40], \"level\": x[\"metadata_level\"], \"group\": x[\"metadata_group\"],\n                 \"fold\": x[\"metadata_fold\"], \"n_events\": x[\"metadata_n_events\"],\n                 \"n_usable\": x[\"metadata_n_events_year_usable\"],\n                 \"first_year\": first[\"year\"] if first else None, \"first_source\": first[\"source\"] if first else None,\n                 \"first_relation\": first[\"relation\"] if first else None})\n    for e in out[\"events\"]:\n        evs.append({\"source\": e[\"source\"], \"year\": e[\"year\"], \"year_usable\": e[\"year_usable\"],\n                    \"match_method\": e[\"match_method\"], \"relation\": e[\"relation\"]})\n    for s, st in out[\"sources_checked\"].items():\n        chk.append({\"source\": s, \"status\": st})\n\nC, E, K = pd.DataFrame(rows), pd.DataFrame(evs), pd.DataFrame(chk)\npd.set_option(\"display.width\", 200)\nprint(C.sort_values([\"group\", \"n_events\"], ascending=[True, False]).to_string(index=False))\nprint(\"\\nevents by match_method:\\n\", E.match_method.value_counts().to_string())\nprint(\"\\nevents by relation:\\n\", E.relation.value_counts().to_string())\n\"\"\")\n\ncode(r\"\"\"\nfig, ax = plt.subplots(1, 3, figsize=(18, 5))\n\n# (a) events per source, usable vs not\nt = E.groupby([\"source\", \"year_usable\"]).size().unstack(fill_value=0).reindex(columns=[True, False], fill_value=0)\nt = t.loc[t.sum(axis=1).sort_values().index]\nt.plot.barh(stacked=True, ax=ax[0], color=[\"#2a7ab9\", \"#c8c8c8\"])\nax[0].set_title(\"Recognition events per source (40 demo concepts)\")\nax[0].set_xlabel(\"events\"); ax[0].set_ylabel(\"\"); ax[0].legend([\"year_usable\", \"not usable\"], frameon=False)\n\n# (b) usable event years\nyrs = E[E.year_usable & E.year.notna()]\nfor s, c in [(\"wikipedia_en\", \"#2a7ab9\"), (\"mesh\", \"#e08a2e\")]:\n    ax[1].hist(yrs[yrs.source == s].year, bins=range(1940, 2030, 3), alpha=0.7, label=s, color=c)\nax[1].hist(yrs[~yrs.source.isin([\"wikipedia_en\", \"mesh\"])].year, bins=range(1940, 2030, 3), alpha=0.5,\n           label=\"taxonomies + curated lists + wikidata\", color=\"#5a9e4b\")\nax[1].set_title(\"Years of usable recognition events\"); ax[1].set_xlabel(\"year\"); ax[1].legend(frameon=False)\n\n# (c) sources_checked status\nst = K.groupby([\"source\", \"status\"]).size().unstack(fill_value=0)\nst = st.loc[st.get(\"not_applicable\", 0).sort_values(ascending=False).index] if \"not_applicable\" in st else st\nst.plot.barh(stacked=True, ax=ax[2], colormap=\"tab20\")\nax[2].set_title(\"sources_checked status per source\"); ax[2].set_xlabel(\"concepts\"); ax[2].set_ylabel(\"\")\nax[2].legend(fontsize=8, frameon=False)\nplt.tight_layout()\nplt.show()\n\"\"\")\n\ncode(r\"\"\"\n# earliest usable recognition year per provisional group (only concepts with any usable event)\ng = C.dropna(subset=[\"first_year\"]).groupby(\"group\").first_year.agg([\"count\", \"median\", \"min\", \"max\"])\nprint(g.to_string())\nprint(\"\\nearliest-event source mix:\\n\", C.first_source.value_counts().to_string())\n\"\"\")\n\nnb = {\"cells\": cells, \"metadata\": {\"kernelspec\": {\"display_name\": \"Python 3\", \"language\": \"python\", \"name\": \"python3\"},\n                                   \"language_info\": {\"name\": \"python\"}},\n      \"nbformat\": 4, \"nbformat_minor\": 5}\nfor i, c in enumerate(nb[\"cells\"]):\n    c[\"id\"] = f\"cell-{i}\"\nOUT.write_text(json.dumps(nb, indent=1, ensure_ascii=False))\nprint(\"wrote\", OUT)\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [23] TOOL CALL — Bash · 2026-09-29 21:14:42 UTC

```
Build notebook with minimal config and test-run it:
SP=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad && sed -e 's/^MINI_PER_DATASET = 200 /MINI_PER_DATASET = 10  /' -e 's/^PREVIEW_N = 10 /PREVIEW_N = 1  /' $SP/build_nb.py > $SP/build_min.py && python3 $SP/build_min.py code_demo.ipynb && grep -o 'MINI_PER_DATASET = [0-9]*\|PREVIEW_N = [0-9]*' code_demo.ipynb | head -2 && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/python jupyter ipykernel && s=$(date +%s) && /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20; echo "runtime $(( $(date +%s)-s ))s"
```

### [24] TOOL RESULT — Bash · 2026-09-29 21:15:08 UTC

```
{"stdout": "wrote code_demo.ipynb\nMINI_PER_DATASET = 10\nPREVIEW_N = 1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 151178 bytes to code_demo.ipynb\nruntime 21s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-29 21:15:14 UTC

```
Minimal config passes (21s). Scaling to the original values (200 / 10):
```

### [26] TOOL CALL — Bash · 2026-09-29 21:15:14 UTC

```
Rebuild with original config, test-run, show outputs:
SP=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad && python3 $SP/build_nb.py code_demo.ipynb && rm -rf demo_output && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/python jupyter ipykernel && s=$(date +%s) && /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; echo "runtime $(( $(date +%s)-s ))s"; python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[:2500])
        elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
        elif 'image/png' in o.get('data',{}): print('[image]')
    print('-----')
"
```

### [27] TOOL RESULT — Bash · 2026-09-29 21:15:36 UTC

```
{"stdout": "wrote code_demo.ipynb\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 151352 bytes to code_demo.ipynb\nruntime 20s\n-----\n-----\n-----\nDemo subset of the external-recognition lookup table for OpenAlex legacy concepts (outcome O5): 40 concept_recognition rows (4 per provisional group) + 6 rows from each of the 9 other datasets, sampled from mini_data_out.json.\n{'concept_recognition': 40, 'external_entries_mesh': 6, 'external_entries_acm_ccs': 6, 'external_entries_msc': 6, 'external_entries_pacs_physh': 6, 'external_entries_jel': 6, 'external_entries_curated_lists': 6, 'match_verifications': 6, 'crosswalk_level1_to_field': 6, 'spotcheck_p78': 6}\n\n-----\n-----\n-----\n-----\n21:15:34|INFO   |concept rows 40\n\n21:15:34|INFO   |datasets: {'concept_recognition': 40, 'external_entries_mesh': 6, 'external_entries_acm_ccs': 6, 'external_entries_msc': 6, 'external_entries_pacs_physh': 6, 'external_entries_jel': 6, 'external_entries_curated_lists': 6, 'match_verifications': 6, 'crosswalk_level1_to_field': 6, 'spotcheck_p78': 6}\n\n21:15:34|INFO   |concept_recognition folds: {'dev': 16, 'heldout': 16, 'unassigned': 8}\n\n21:15:34|INFO   |full_data_out.json 0.4 MB\n\n21:15:34|INFO   |above 0.2 MB -> split into ['full_data_out/full_data_out_1.json', 'full_data_out/full_data_out_2.json', 'full_data_out/full_data_out_3.json']; single file removed\n\n21:15:34|INFO   |mini_data_out.json and preview_data_out.json written\n\n-----\nfull_data_out/full_data_out_1.json          134.2 kB\nfull_data_out/full_data_out_2.json          148.2 kB\nfull_data_out/full_data_out_3.json           86.5 kB\nmini_data_out.json                          704.9 kB\n\npreview_data_out.json                        49.0 kB\n\nparts reassemble to the input datasets: {'concept_recognition': 40, 'external_entries_mesh': 6, 'external_entries_acm_ccs': 6, 'external_entries_msc': 6, 'external_entries_pacs_physh': 6, 'external_entries_jel': 6, 'external_entries_curated_lists': 6, 'match_verifications': 6, 'crosswalk_level1_to_field': 6, 'spotcheck_p78': 6}\n\n-----\n                                   label  level             group       fold  n_events  n_usable  first_year        first_source first_relation\n                          Genome editing      4               BGM        dev        11        10        2011 nature_methods_moty        broader\n                              Proteomics      3               BGM        dev         9         9        2002        wikipedia_en           same\n                             Phytoplasma      5               BGM        dev         2         2        2004                mesh           same\n                                   CD146      4               BGM        dev         2         2        2006                mesh           same\n                                Robotics      3                CS        dev        23        22        1987                mesh           same\n                               Analytics      2                CS        dev        20        20        2004        wikipedia_en           same\n                        Autonomous robot      4                CS        dev        18        18        2002        wikipedia_en           same\n            Adversarial machine learning      3                CS        dev         3         2        2012             acm_ccs           same\n                              3d printed      2               Eng        dev        21        21        2004        wikipedia_en           same\n                              3d printer      2               Eng        dev         9         9        2004        wikipedia_en           same\n                                  Pallet      2               Eng        dev         1         1        2004        wikipedia_en           same\n                           Crushed stone      2               Eng        dev         1         1        2007        wikipedia_en           same\n                           Neural system      2           LifeEnv    heldout         7         7        1966                mesh           same\n                       Genetic algorithm      2           LifeEnv    heldout         7         7        1975            wikidata           same\n                             Niclosamide      2           LifeEnv    heldout         2         2        1973                mesh           same\n                               Cichorium      2           LifeEnv    heldout         1         1        2005        wikipedia_en           same\n                      Stochastic process      2     \n-----\n[image]\n-----\n                   count  median   min   max\ngroup                                       \nBGM                    4  2005.0  2002  2011\nCS                     4  2003.0  1987  2012\nEng                    4  2004.0  2004  2007\nLifeEnv                4  1974.0  1966  2005\nMathDec                4  1997.0  1991  2005\nMed                    4  2006.5  1968  2024\nPhysical               4  2004.0  2001  2017\nSocial                 4  2000.5  1969  2007\nunassigned_health      4  1949.5  1934  1968\nunassigned_multi       4  2002.5  1966  2007\n\nearliest-event source mix:\n first_source\nwikipedia_en           18\nmesh                   13\nwikidata                4\nacm_ccs                 2\nnature_methods_moty     1\nresearch_fronts         1\nmit_tr10                1\n\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] ASSISTANT · 2026-09-29 21:15:42 UTC

```
The notebook runs clean in 20s at the original config values. Next I'll look at the figure.
```

### [29] TOOL CALL — Bash · 2026-09-29 21:15:42 UTC

```
Extract figure from notebook:
python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [30] TOOL RESULT — Bash · 2026-09-29 21:15:42 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Read · 2026-09-29 21:15:44 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/fig.png
```

### [32] TOOL RESULT — Read · 2026-09-29 21:15:44 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [33] ASSISTANT · 2026-09-29 21:16:02 UTC

```
The figure reads fine. I'll fix the overlapping legend in panel (c) and draw the green histogram first, then re-run.
```

### [34] TOOL CALL — Bash · 2026-09-29 21:16:02 UTC

```
Patch plot, rebuild, re-run and verify URL:
SP=/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad && python3 - <<'EOF'
p="/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/build_nb.py"
s=open(p).read()
old_b='''for s, c in [("wikipedia_en", "#2a7ab9"), ("mesh", "#e08a2e")]:
    ax[1].hist(yrs[yrs.source == s].year, bins=range(1940, 2030, 3), alpha=0.7, label=s, color=c)
ax[1].hist(yrs[~yrs.source.isin(["wikipedia_en", "mesh"])].year, bins=range(1940, 2030, 3), alpha=0.5,
           label="taxonomies + curated lists + wikidata", color="#5a9e4b")
'''
new_b='''ax[1].hist(yrs[~yrs.source.isin(["wikipedia_en", "mesh"])].year, bins=range(1940, 2030, 3), alpha=0.5,
           label="taxonomies + curated lists + wikidata", color="#5a9e4b")
for s, c in [("wikipedia_en", "#2a7ab9"), ("mesh", "#e08a2e")]:
    ax[1].hist(yrs[yrs.source == s].year, bins=range(1940, 2030, 3), alpha=0.8, label=s, color=c)
'''
assert old_b in s; s=s.replace(old_b,new_b)
old_c='ax[2].legend(fontsize=8, frameon=False)'
new_c='ax[2].legend(fontsize=8, frameon=False, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=4)'
assert old_c in s; s=s.replace(old_c,new_c)
open(p,'w').write(s)
EOF
python3 $SP/build_nb.py code_demo.ipynb && rm -rf demo_output && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/python jupyter ipykernel && s=$(date +%s) && /tmp/aii_nb_test_envs/art_O7Dq4L02QnDN-e8fb55dfdcfe/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -1; echo "runtime $(( $(date +%s)-s ))s"; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
print('errors:',sum(o['output_type']=='error' for c in nb['cells'] for o in c.get('outputs',[])))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('$SP/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json"' code_demo.ipynb; du -sh . demo_output
```

### [35] TOOL RESULT — Bash · 2026-09-29 21:16:24 UTC

```
{"stdout": "wrote code_demo.ipynb\n[NbConvertApp] Writing 149605 bytes to code_demo.ipynb\nruntime 20s\nerrors: 0\n0\n6.7M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-29 21:16:28 UTC

```
Check workspace files and URL in notebook source:
ls -la; ls -R demo_output | head; python3 -c "
import json
src=''.join(''.join(c['source']) for c in json.load(open('code_demo.ipynb'))['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/fork/run_DVtwwCx0JbFq/round-2/dataset-2/demo/mini_demo_data.json\"' in src, 'urlopen(GITHUB_DATA_URL)' in src)"
```

### [37] TOOL RESULT — Bash · 2026-09-29 21:16:28 UTC

```
{"stdout": "total 6602\ndrwxrwxrwx 4 aii-agent aii-agent 2000179 Sep 29 21:16 .\ndrwxrwxrwx 6 aii-agent aii-agent 2000378 Sep 29 21:11 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 21:11 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 21:12 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  231252 Sep 29 21:16 .repl_agent.ptylog\n-rw-rw-rw- 1 aii-agent aii-agent  149611 Sep 29 21:16 code_demo.ipynb\ndrwxrwxrwx 4 aii-agent aii-agent 2000107 Sep 29 21:16 demo_output\n-rw-rw-rw- 1 aii-agent aii-agent  375925 Sep 29 21:13 mini_demo_data.json\ndemo_output:\nfull_data_out\nlogs\nmini_data_out.json\npreview_data_out.json\n\ndemo_output/full_data_out:\nfull_data_out_1.json\nfull_data_out_2.json\nfull_data_out_3.json\nTrue True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Read · 2026-09-29 21:16:30 UTC

```
/tmp/claude-10001/-ai-inventor-aii-data-runs-run-DVtwwCx0JbFq-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-2-art-O7Dq4L02QnDN/64ada37f-4d59-4cf6-b6b9-ab8341c86fca/scratchpad/fig.png
```

### [39] TOOL RESULT — Read · 2026-09-29 21:16:31 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [40] ASSISTANT · 2026-09-29 21:16:44 UTC

```
Good. Next I'll write the README, the manifest and the struct output.
```

### [41] TOOL CALL — Bash · 2026-09-29 21:16:44 UTC

```
Write manifest, README, struct output:
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is under the 10 MB auto-keep floor
# (code_demo.ipynb ~150 kB, mini_demo_data.json ~0.4 MB, demo_output/ ~1.1 MB of JSON/logs written by the notebook).
entries: []
EOF
cat > README.md <<'EOF'
# Demo: when research concepts were officially recognised (O5 lookup table)

This is a runnable notebook demo of the **`data.py`** assembly step of the external-recognition dataset
(artifact `art_O7Dq4L02QnDN`). The full dataset gives dated, sourced recognition events for 65,026 OpenAlex legacy
concepts. The sources are MeSH, Wikipedia, Wikidata, ACM CCS, MSC, PACS/PhySH, JEL, and curated "of the year" and hype lists.

The notebook keeps the original `data.py` code (`check`, `mini_preview`, `main`) and the helpers it imports from
`scripts/s9_outputs.py` (`clean`, `dumps`, `write_parts`, `trunc`). It splits them into cells, explains each one,
and ends with a summary and plots of the recognition events. `build_datasets()` needs about 50 MB of upstream
parquet tables, so the notebook replaces it with a pre-built 94-row subset of its output.

## Layout
| Path | What it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, already executed. It loads data from GitHub, falling back to the local file. |
| `mini_demo_data.json` | Curated subset of 94 examples: 40 `concept_recognition` rows (4 per provisional group) and 6 rows from each of the other 9 datasets, sampled from the artifact's `mini_data_out.json`. |
| `demo_output/` | Files the notebook writes: split `full_data_out/full_data_out_<n>.json` parts, `mini_data_out.json`, `preview_data_out.json`, `logs/data.log`. |

## How to run
- **Colab:** open `code_demo.ipynb` and run all cells. The install cell installs only `loguru`.
- **Locally (Python 3.12):** run `pip install jupyter` and then `jupyter nbconvert --to notebook --execute code_demo.ipynb`.
  The install cell pins numpy/pandas/pyarrow/matplotlib to Colab's versions. A full run takes about 20 s.

Config (notebook section 4) uses the original `data.py` values (mini 200, preview 10, truncation 300, seed 0). The one
exception is the file-size limits: 200 kB and 150 kB instead of 95 MB and 90 MB, so that the small demo file still
goes through the split-into-parts branch.

## Restoring removed files
Nothing is marked `delete` in `.aii/manifest.yaml`, because there are no heavy files. `demo_output/` is regenerated
by re-running the notebook.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; ls -la .aii
```

### [42] TOOL RESULT — Bash · 2026-09-29 21:16:44 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\ntotal 1975\ndrwxrwxrwx 2 aii-agent aii-agent   21100 Sep 29 21:16 .\ndrwxrwxrwx 4 aii-agent aii-agent 2000181 Sep 29 21:16 ..\n-rw-rw-rw- 1 aii-agent aii-agent     211 Sep 29 21:16 manifest.yaml", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] ASSISTANT · 2026-09-29 21:16:53 UTC

```
I've turned the dataset's `data.py` script into a demo notebook. It runs start to finish in a fresh test environment in about 20 seconds with no errors, well inside the 10-minute limit.

**What the notebook runs.** The original script needs about 50 MB of intermediate tables from the upstream pipeline to build its 10 datasets. Those aren't shipped, so that one build step is replaced by loading an already-built subset. Everything after it is the original code, split into cells with explanations between them:
- the schema checks;
- writing `full_data_out.json`, and splitting it into numbered parts when it is too large;
- writing the mini and preview files.

The small helpers that `data.py` imports from `scripts/s9_outputs.py` are copied into the notebook unchanged. The original import lines and the replaced loading lines are kept as comments.

**Settings.** The mini size (200), preview size (10), string truncation (300) and random seed (0) use the original values, since runtime was never an issue. The file-size limits are the exception: 200 kB and 150 kB instead of 95 MB and 90 MB, so the 0.4 MB demo file actually gets split. It splits into three parts, and the notebook checks that they rejoin into exactly the input. I did run the notebook once with the smallest settings first, then with these; both passed.

**Files, all in this workspace:**
- **`mini_demo_data.json`** (94 rows): 40 concept rows (4 from each of the 10 groups, half the richest and half random) plus 6 rows from each of the other 9 datasets. It comes from the dataset's existing mini file, not the full one. The task asked for "at most one dataset". I read that as one data file, because the original checks fail unless all 10 datasets are present.
- **`code_demo.ipynb`**: already executed, with outputs saved. It contains the exact `GITHUB_DATA_URL` line and falls back to the local file. The final section has a table per concept (earliest usable recognition year and which source gave it) and three plots: events per source, the years of those events, and found / not found / not applicable counts per source.
- **`demo_output/`**: the files the notebook writes when it runs.
- **`README.md`**, **`.aii/manifest.yaml`** and **`.terminal_claude_agent_struct_out.json`**. The manifest has no entries because every file is under the 10 MB threshold.

With only 4 concept rows per group, the original "half richest, half random" sampling picks some rows twice, so the notebook's own mini output has repeats. The notebook explains this; with the full 65,026 concepts it rarely happens.
```
