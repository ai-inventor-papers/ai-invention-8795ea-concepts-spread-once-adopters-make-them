# gen_demo_art_experiment_8 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_8` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 11:17:51 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 11:17:57 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/.shared_cache`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

Please work on the following task, work as an experienced researcher that would to publish in the following journal-special issue:
https://link.springer.com/collections/fgcaicgjah 
Please be considerate with resources use – do not spend unnecessary resources, first evaluate what would be the most economical and efficient way. While semantical grounding process first see if there is any similar dataset already available or if you create training-test labelled  datasets and then train your own models. 
Research task: Exploring emerging scientific concepts through evolving knowledge networks
The objective of this task is to investigate whether temporal changes in the structure of scientific knowledge networks can reveal and explain the emergence of scientific concepts. The study should use an OpenAlex-based scholarly dataset, or a comparable large-scale publication dataset containing publication dates, textual metadata, disciplinary classifications, and, where useful, citation information.
Scientific emergence should be treated as a dynamic network process rather than simply as increasing popularity. A concept may emerge by acquiring new semantic or co-occurrence relations, becoming more structurally central, connecting previously separated research communities, or spreading from a specialized disciplinary context into a broader scientific landscape. The study should therefore identify which structural signals accompany or anticipate such changes and determine whether these signals generalize across scientific domains.
The study should address the following research questions:
RQ1: Which temporal network indicators reliably characterize and anticipate the emergence of scientific concepts across different scientific domains?
RQ2: How do emerging scientific concepts diffuse across disciplinary communities over time, and which network trajectories distinguish locally concentrated concepts from concepts that become broadly integrated into the scientific knowledge network?
A possible execution scenario is:
1.    Explore a focused set of concepts and network trajectories. Begin with one well-defined, rapidly evolving scientific area, for example Artificial Intelligence, and construct a semantically grounded temporal knowledge network for a manageable set of concepts. Inspect the network evolution openly before fixing the final methodology. Examine how known concepts change over time in terms of connectivity, new neighbors, community membership, centrality, and disciplinary distribution. Include concepts with visibly different trajectories: rapid emergence, gradual growth, local specialization, cross-disciplinary diffusion, and temporary expansion. The purpose of this stage is exploratory: identify which structural changes appear meaningful and which graph representations best capture them.
2.    Design a broad set of candidate emergence indicators. Based on the exploratory analysis and relevant literature on temporal networks, knowledge graphs, scientometrics, innovation diffusion, and community evolution, define a relatively large set of candidate indicators, for example 30--50 measures. These may include degree and weighted-degree growth, new-edge formation, edge persistence, neighborhood novelty, centrality change, community transitions, participation coefficient, brokerage, disciplinary reach, disciplinary entropy, diffusion velocity, and changes in local clustering. Include several simple concept-level temporal measures as reference points so that it is possible to determine whether sophisticated network information provides useful additional signal. The indicators should not all be minor variations of the same measure; they should reflect different aspects of network emergence.
3.    Test the indicators on a substantially wider collection of scientific domains and concepts. Apply all candidate indicators beyond the exploratory domain. Include fast- and slow-evolving fields, concepts originating in different scientific communities, concepts that remain discipline-specific, and concepts that subsequently become interdisciplinary. The evaluation should explicitly test whether indicators generalize across domains rather than working only in one field. Reserve complete scientific fields, time intervals, or concept groups as a held-out evaluation set that is not used when selecting or tuning the indicators. Selecting the best indicators and testing them on the same concepts would otherwise overestimate their usefulness.
4.    Define independent ground truth for scientific emergence and diffusion. Validation should not rely only on visual inspection of the constructed network or on a single operational definition of emergence. Establish several measurable outcomes representing different aspects of scientific emergence. These may include subsequent sustained publication uptake of a concept, future citation growth, expansion into previously unrelated subfields, persistence over several future periods, or externally documented recognition of a technology or research topic. Where feasible, use external sources such as scientific taxonomies, technology reports, review papers, curated emerging-topic lists, or other independent evidence. Emergence should not be defined only as rapid growth: a short-lived spike should not automatically be considered equivalent to persistent scientific integration. Similarly, a concept that becomes very frequent within one narrow subfield should be distinguishable from one that diffuses broadly across science.
5.    Identify and validate the strongest network indicators. Select the most promising indicators using only the development data, and evaluate approximately the 10 strongest measures on the held-out concepts/domains. Test their association with the ground-truth outcomes using correlation, ranking, or predictive evaluation as appropriate. Report results both globally and within individual scientific fields. The resampling unit should be clearly defined—for example concepts, subfields, or temporal windows—and results should be aggregated both across concepts and across domains. If an indicator performs well only in one domain, such as Artificial Intelligence, but fails to generalize to other scientific fields, this should be reported as an important negative result rather than averaged away.
6.    Use the strongest indicators to investigate RQ2 and derive diffusion trajectories. For concepts identified as emerging, analyze how their structural position changes over time. Study disciplinary reach, entropy, community transitions, brokerage, and cross-community connectivity. Rather than defining classes beforehand, derive recurring trajectories empirically. Possible outcomes may include localized emergence, rapid interdisciplinary diffusion, gradual network integration, transient expansion, or increasing structural brokerage. Examine whether there are systematic temporal sequences—for example whether concepts first become central within their original community and subsequently diffuse across disciplines, or whether some concepts emerge directly at the intersection of several communities.
Additional analysis -- explaining why the strongest indicators work. If one or more measures prove particularly robust, perform a detailed network analysis of what they are capturing. Identify which periods, network neighborhoods, edge types, communities, or structural transitions generate the signal. Representative concept case studies should be selected from the quantitative results and used to visualize these mechanisms.
Optional extension -- learned emergence model. Instead of relying exclusively on individual predefined metrics, train a small interpretable model using temporal network features to predict future emergence or diffusion outcomes. Compare it with the strongest individual indicators on the same held-out evaluation set. If the learned model performs substantially better, analyze which network features and temporal patterns it uses and whether these patterns have a meaningful interpretation in terms of scientific knowledge evolution.
Expected outcome
The expected outcome is not merely a list or ranking of emerging scientific concepts, but a validated framework for identifying and explaining scientific emergence through temporal network structure. The study should determine which network signals are robust across scientific domains, which signals are domain-specific, and how concepts transition from local research topics to broadly connected elements of the scientific knowledge network. 
We expect the final result as publication in the specific journal format mentioned above, in the structure that other papers from this journal have, with citations from the related work from the selected journal, with comparison to the related work. For each research question we would like to have experimental setup, comparison to related work if available, produced results and discussed outcomes. We would also like to have a general methodology presented in graphical form and clearly explained in the paper. Use the following API key for OpenAlex: q0jD2k15XbNV0E3SFHhpr0
````

### [3] TOOL CALL — Skill · 2026-09-29 11:18:03 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 11:18:03 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 11:18:03 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 11:18:03 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 11:18:05 UTC

```
List artifact workspace and current dir:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; ls -la $W; ls -la $W/results 2>/dev/null | head -30; wc -l $W/method.py; ls -la .aii; ls -la
```

### [8] TOOL RESULT — Bash · 2026-09-29 11:18:05 UTC

```
{"stdout": "total 26180\ndrwxr-xr-x 15 root   root   2023575 Sep 29 05:04 .\ndrwxr-xr-x  7 root   root   3000186 Sep 29 02:14 ..\ndrwxr-xr-x  2 root   root     62500 Sep 29 03:52 .aii\n-rw-------  1 165536 165536      54 Sep 29 02:15 .aii_claude_session.json\n-rw-------  1 165536 165536    5923 Sep 29 03:52 .aii_worker_result.json\ndrwxr-xr-x  8 165536 165536 2005249 Sep 29 03:46 .git\n-rw-r--r--  1 165536 165536      72 Sep 29 02:35 .gitignore\n-rw-r--r--  1 165536 165536 1014045 Sep 29 03:52 .repl_agent.ptylog\n-rw-r--r--  1 165536 165536    2709 Sep 29 03:42 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 165536 165536   22764 Sep 29 03:46 README.md\n-rw-r--r--  1 165536 165536    6204 Sep 29 02:40 audit.py\ndrwxr-xr-x  4 165536 165536 2005380 Sep 29 03:28 data\ndrwxr-xr-x  2 165536 165536 1054146 Sep 29 03:29 figures\n-rw-r--r--  1 165536 165536 2208500 Sep 29 03:39 full_method_out.json\ndrwxr-xr-x  3 165536 165536 2002001 Sep 29 02:16 inputs\ndrwxr-xr-x  2 165536 165536 1019408 Sep 29 05:04 lib\ndrwxr-xr-x  2 165536 165536 2000386 Sep 29 03:10 llm_cache\ndrwxr-xr-x  2 165536 165536 1091170 Sep 29 03:28 logs\n-rw-rw-rw-  1 165536 165536   10220 Sep 29 03:33 make_outputs.py\n-rw-r--r--  1 165536 165536    3893 Sep 29 03:32 make_report.py\n-rwxrwxrwx  1 165536 165536    3310 Sep 29 03:42 method.py\n-rw-r--r--  1 165536 165536 1951651 Sep 29 03:39 method_out.json\n-rw-r--r--  1 165536 165536    5145 Sep 29 03:39 mini_method_out.json\ndrwxr-xr-x  2 165536 165536       1 Sep 29 02:21 models\ndrwxr-xr-x  3 165536 165536 2009748 Sep 29 02:23 passC\n-rw-r--r--  1 165536 165536   15598 Sep 29 02:23 passC.py\n-rw-r--r--  1 165536 165536    6406 Sep 29 02:26 prereg.md\n-rw-r--r--  1 165536 165536    5145 Sep 29 03:39 preview_method_out.json\n-rw-rw-rw-  1 165536 165536    2521 Sep 29 03:36 pyproject.toml\n-rw-r--r--  1 165536 165536    4143 Sep 29 03:34 readme_tables.py\n-rw-r--r--  1 165536 165536    4536 Sep 29 03:41 rederive.py\n-rw-r--r--  1 165536 165536    8650 Sep 29 03:42 reproducibility.md\n-rw-r--r--  1 165536 165536    1777 Sep 29 03:36 requirements.lock.txt\n-rwxrwxrwx  1 165536 165536     366 Sep 29 03:36 restore.sh\ndrwxr-xr-x  2 165536 165536 1057843 Sep 29 03:40 results\n-rw-r--r--  1 165536 165536    2620 Sep 29 02:35 s0_prereg.py\n-rw-r--r--  1 165536 165536    7305 Sep 29 02:21 s1_candidates.py\n-rw-rw-rw-  1 165536 165536    8269 Sep 29 02:36 s3_checks.py\n-rw-rw-rw-  1 165536 165536    9669 Sep 29 03:10 s4_gate.py\n-rw-r--r--  1 165536 165536   16136 Sep 29 03:07 s5_typing.py\n-rw-r--r--  1 165536 165536    9779 Sep 29 02:45 s6_covariates.py\n-rw-r--r--  1 165536 165536    8397 Sep 29 02:42 s7_ego.py\n-rw-r--r--  1 165536 165536   15897 Sep 29 03:11 s8_select.py\n-rw-r--r--  1 165536 165536   15663 Sep 29 03:21 s9_unseal.py\n-rw-r--r--  1 165536 165536    6457 Sep 29 02:42 s_learned.py\ndrwxr-xr-x  2 165536 165536 1077669 Sep 29 02:20 snapshot\ndrwxr-xr-x  2 165536 165536 1001197 Sep 29 03:30 tests\ntotal 3597\ndrwxr-xr-x  2 165536 165536 1057843 Sep 29 03:40 .\ndrwxr-xr-x 15 root   root   2023575 Sep 29 05:04 ..\n-rw-r--r--  1 165536 165536    2304 Sep 29 03:29 audit.json\n-rw-r--r--  1 165536 165536   91250 Sep 29 03:37 cohort_report.json\n-rw-r--r--  1 165536 165536   72704 Sep 29 03:27 cohort_result.json\n-rw-r--r--  1 165536 165536    2632 Sep 29 03:01 coverage_by_year.csv\n-rw-r--r--  1 165536 165536    1570 Sep 29 03:21 deviations.json\n-rw-r--r--  1 165536 165536   59579 Sep 29 03:20 exp5_selection_result.json\n-rw-r--r--  1 165536 165536   15890 Sep 29 03:20 frozen_spec.json\n-rw-r--r--  1 165536 165536    2442 Sep 29 02:35 frozen_spec_v0.json\n-rw-r--r--  1 165536 165536     943 Sep 29 03:28 learned_models_cohort.json\n-rw-r--r--  1 165536 165536     719 Sep 29 02:42 learned_port_validation.json\n-rw-r--r--  1 165536 165536  245108 Sep 29 03:10 llm_cost_log.csv\n-rw-r--r--  1 165536 165536    6154 Sep 29 03:34 readme_tables.md\n-rw-r--r--  1 165536 165536     670 Sep 29 03:41 rederive.json\n-rw-r--r--  1 165536 165536     874 Sep 29 02:22 s1_candidates_summary.json\n-rw-r--r--  1 165536 165536     423 Sep 29 03:01 s2_checks.json\n-rw-r--r--  1 165536 165536    1205 Sep 29 03:01 s3_decision.json\n-rw-r--r--  1 165536 165536     342 Sep 29 03:03 s4_gate_summary.json\n-rw-r--r--  1 165536 165536     525 Sep 29 02:46 s6_checks.json\n-rw-r--r--  1 165536 165536     265 Sep 29 03:02 s6_checks_cohort.json\n-rw-r--r--  1 165536 165536    2857 Sep 29 03:10 type_benchmark_final.json\n-rw-r--r--  1 165536 165536   21384 Sep 29 03:02 type_benchmark_v1.csv\n-rw-r--r--  1 165536 165536    1861 Sep 29 03:04 type_benchmark_v1.json\n-rw-r--r--  1 165536 165536   20750 Sep 29 03:06 type_benchmark_v2.csv\n-rw-r--r--  1 165536 165536    1877 Sep 29 03:07 type_benchmark_v2.json\n-rw-r--r--  1 165536 165536    5962 Sep 29 03:03 type_gold_labels_v1.csv\n-rw-r--r--  1 165536 165536    5962 Sep 29 03:04 type_gold_labels_v2.csv\n-rw-r--r--  1 165536 165536   21841 Sep 29 03:03 type_gold_sheet_v1.csv\n73 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/method.py\ntotal 982\ndrwxr-xr-x 2 root root       1 Sep 29 11:17 .\ndrwxr-xr-x 3 root root 1004178 Sep 29 11:17 ..\ntotal 2005\ndrwxr-xr-x 3 root root 1004178 Sep 29 11:17 .\ndrwxr-xr-x 3 root root 1004178 Sep 29 11:17 ..\ndrwxr-xr-x 2 root root       1 Sep 29 11:17 .aii\n-rw------- 1 root root      54 Sep 29 11:17 .aii_claude_session.json\n-rw-r--r-- 1 root root   42731 Sep 29 11:18 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 11:18:09 UTC

```
Read method.py, preview output, rederive and audit scripts:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $W/method.py; echo ----; cat $W/preview_method_out.json | head -c 4000; echo; echo ----; cat $W/rederive.py; echo ---; cat $W/audit.py | head -80
```

### [10] TOOL RESULT — Bash · 2026-09-29 11:18:09 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).\n\nUsage: python method.py [--only STEP] [--from STEP] [--list]\nSteps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort\n                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate\n                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report\nNote: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nPY = sys.executable\nSTEPS = [\n    (\"s0\", [PY, \"s0_prereg.py\"]),\n    (\"s1\", [PY, \"s1_candidates.py\"]),\n    (\"passC\", [PY, \"passC.py\", \"--workers\", \"9\"]),\n    (\"passC_merge\", [PY, \"passC.py\", \"--merge\"]),\n    (\"s3\", [PY, \"s3_checks.py\"]),\n    (\"s4\", [PY, \"s4_gate.py\", \"run\"]),\n    (\"s4_retry\", [PY, \"s4_gate.py\", \"retry\"]),\n    (\"s7_exp5\", [PY, \"s7_ego.py\", \"--frame\", \"exp5\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"200\"]),\n    (\"s7_cohort\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"all,home,sizematch\", \"--workers\", \"3\", \"--chunk\", \"50\"]),\n    (\"s7_cohort_full\", [PY, \"s7_ego.py\", \"--frame\", \"cohort\", \"--builds\", \"full\", \"--workers\", \"5\", \"--chunk\", \"20\",\n                        \"--tag\", \"_full\"]),\n    (\"s6\", [PY, \"s6_covariates.py\"]),\n    (\"s5_exp5\", [PY, \"s5_typing.py\", \"exp5\"]),\n    (\"s5_cohort\", [PY, \"s5_typing.py\", \"cohort\"]),\n    (\"s5_bench\", [PY, \"s5_typing.py\", \"bench\"]),\n    (\"s5_sheet\", [PY, \"s5_typing.py\", \"sheet\"]),\n    (\"s5_gate\", [PY, \"s5_typing.py\", \"gate\"]),\n    (\"s5_v2\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s5_typing.py',c,'--prompt','v2'],check=True) \"\n                          \"for c in ('exp5','cohort','bench','gate')]\"]),\n    (\"s5_m2all\", [PY, \"s5_typing.py\", \"m2all\", \"--prompt\", \"v2\"]),\n    (\"s8\", [PY, \"s8_select.py\", \"--nboot\", \"500\"]),\n    (\"s9\", [PY, \"s9_unseal.py\"]),\n    (\"learned\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,'s_learned.py',c],check=True) \"\n                           \"for c in ('validate','features','score')]\"]),\n    (\"audit\", [PY, \"audit.py\"]),\n    (\"tests\", [PY, \"-c\", \"import subprocess,sys;[subprocess.run([sys.executable,t],check=True) for t in \"\n                         \"('tests/test_output.py','tests/t_ego_flags.py','tests/t_outcomes.py','tests/test_units.py')]\"]),\n    (\"outputs\", [PY, \"make_outputs.py\"]),\n    (\"report\", [PY, \"make_report.py\"]),\n    (\"rederive\", [PY, \"rederive.py\"]),\n]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--only\")\n    ap.add_argument(\"--from\", dest=\"start\")\n    ap.add_argument(\"--list\", action=\"store_true\")\n    a = ap.parse_args()\n    names = [n for n, _ in STEPS]\n    if a.list:\n        print(\"\\n\".join(names))\n        return\n    todo = STEPS\n    if a.only:\n        todo = [s for s in STEPS if s[0] == a.only]\n    elif a.start:\n        todo = STEPS[names.index(a.start):]\n    for name, cmd in todo:\n        print(f\"== {name}: {' '.join(cmd[:4])}\", flush=True)\n        subprocess.run(cmd, cwd=ROOT, check=True)\n\n\nif __name__ == \"__main__\":\n    main()\n----\n{\n  \"metadata\": {\n    \"method_name\": \"OPEN (open-neighbourhood composite) vs B5 baseline, fresh 2015-2017 onset cohort (2017 = declared power extension)\",\n    \"verdict\": \"CONFIRMED\",\n    \"primary_outcome\": \"O2r_m50\",\n    \"predict_B5\": \"frozen OLS of O2r_m50 on standardised B5 fitted on the EXP5 frame\",\n    \"predict_B5_plus_OPEN_home\": \"frozen OLS on B5 + OPEN_home fitted on the EXP5 frame\",\n    \"outcome_grounding\": \"TAG\",\n    \"n\": 1443\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"fresh_cohort_2015_2017_open\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Electrical impedance myography\\\", \\\"openalex_id\\\": \\\"C1918360\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"BGM+Med\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"4.95097\",\n          \"predict_B5_plus_OPEN_home\": \"5.04306\",\n          \"metadata_OPEN_home\": 0.32132431470264056,\n          \"metadata_OPEN_all\": -0.12508189070586714,\n          \"metadata_OPEN_sizematch\": 0.12254799950962321,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 3,\n          \"metadata_fp_logN\": 4.04305126783455,\n          \"metadata_fp_nfields\": 3,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": null,\n          \"metadata_O1c\": -0.24116205681688863,\n          \"metadata_O1b\": 1,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": null,\n          \"metadata_O2r_m50_MATCH\": null,\n          \"metadata_logvol\": 4.02535169073515,\n          \"metadata_growth_c\": -0.3364722366212129,\n          \"metadata_offhome_share\": 0.19047619047619047,\n          \"metadata_entropy\": 0.7385104891120922,\n          \"metadata_reach\": 4,\n          \"metadata_CONTACT_REACH\": 4,\n          \"metadata_RETENTION_RATIO_early\": 0.0,\n          \"metadata_n_authors_early\": 4.962844630259907,\n          \"metadata_n_home_early\": 34,\n          \"metadata_n_all_early\": 55,\n          \"metadata_precision_c\": 0.9,\n          \"metadata_home\": \"27\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Persistent homology\\\", \\\"openalex_id\\\": \\\"C2874115\\\", \\\"t0\\\": 2016, \\\"home_group\\\": \\\"PHYS\\\"}\",\n          \"output\": \"9.39058\",\n          \"predict_B5\": \"7.45805\",\n          \"predict_B5_plus_OPEN_home\": \"NA\",\n          \"metadata_OPEN_home\": null,\n          \"metadata_OPEN_all\": 1.0279867793278947,\n          \"metadata_OPEN_sizematch\": null,\n          \"metadata_type\": \"method\",\n          \"metadata_generic\": 0,\n          \"metadata_level\": 2,\n          \"metadata_fp_logN\": 4.304065093204169,\n          \"metadata_fp_nfields\": 8,\n          \"metadata_fp_reemerge\": 1,\n          \"metadata_fp_wiki_pre\": 0,\n          \"metadata_newborn\": 0,\n          \"metadata_O2r_resid\": 4.921541872785715,\n          \"metadata_O1c\": 0.6061358035703153,\n          \"metadata_O1b\": 0,\n          \"metadata_O3\": 0,\n          \"metadata_O2r_m50_TAG\": 9.390583535312317,\n          \"metadata_O2r_m50_MATCH\": 9.761747385271264,\n          \"metadata_logvol\": 4.356708826689592,\n          \"metadata_growth_c\": 0.3184537311185346,\n          \"metadata_offhome_share\": 0.7450980392156863,\n          \"metadata_entropy\": 1.6881963704692144,\n          \"metadata_reach\": 6,\n          \"metadata_CONTACT_REACH\": 7,\n          \"metadata_RETENTION_RATIO_early\": 0.42857142857142855,\n          \"metadata_n_authors_early\": 5.389071729816501,\n          \"metadata_n_home_early\": 13,\n          \"metadata_n_all_early\": 77,\n          \"metadata_precision_c\": 1.0,\n          \"metadata_home\": \"31\",\n          \"metadata_window_flag\": 0\n        },\n        {\n          \"input\": \"{\\\"concept\\\": \\\"Job rotation\\\", \\\"openalex_id\\\": \\\"C3082036\\\", \\\"t0\\\": 2015, \\\"home_group\\\": \\\"SOC\\\"}\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"7.92326\",\n          \"predict_B5_plus_OPEN_home\": \"7.88886\",\n          \"metadata_OPEN_home\": 0.02274310364663708,\n          \"metadata_OPEN_all\": 0.8155822010123192,\n          \"metadata_OPEN_sizematch\": 0.21973513732250882,\n----\n#!/usr/bin/env python3\n\"\"\"Short INDEPENDENT re-derivation of the headline numbers (TODO 5), separate from the pipeline code path.\n\nReads the raw per-concept tables only (data/features_cohort.parquet components, data/outcomes_cohort.parquet,\nresults/frozen_spec.json constants, data/cohort_predictions.parquet) -- NOT results/cohort_result.json fields -- and\n(1) rebuilds OPEN_home / OPEN_all from the six raw components with the frozen constants (pandas, own loop);\n(2) recomputes the partial Spearman at R2 with its own design matrix (pandas ranks + numpy QR residuals, no\n    lib/ladder.rung_design, no rq1stats); a 400-draw bootstrap CI;\n(3) the B5 vs B5+OPEN_home prediction Spearman gain (scipy on the stored frozen predictions);\n(4) the same R2 statistic on shuffled outcomes (200 permutations) and on a random OPEN, which must NOT look significant.\nWrites results/rederive.json.\"\"\"\nimport json\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import spearmanr\n\nROOT = Path(__file__).resolve().parent\nspec = json.loads((ROOT / \"results/frozen_spec.json\").read_text())\nF = pd.read_parquet(ROOT / \"data/features_cohort.parquet\")\nO = pd.read_parquet(ROOT / \"data/outcomes_cohort.parquet\")[[\"ci\", \"O2r_m50\"]]\nD = F.merge(O, on=\"ci\")\nSIGN = {\"new_edge_rate\": 1, \"n_comm_W3\": 1, \"participation\": 1, \"NOV_res\": 1, \"ego_density_W3\": -1,\n        \"edge_persistence\": -1}\n\n\ndef open_score(build):\n    c = spec[\"open_constants\"][build]\n    zs = []\n    for k, s in SIGN.items():\n        v = D[f\"{k}__{build}\"].clip(c[k][\"lo\"], c[k][\"hi\"])\n        zs.append(s * (v - c[k][\"mu\"]) / c[k][\"sd\"])\n    Z = pd.concat(zs, axis=1)\n    o = Z.mean(axis=1, skipna=True).where(Z.notna().sum(axis=1) >= 4)\n    if build != \"all\":\n        o = o.where(D.n_home_early >= 10)\n    return o\n\n\ndef design(d):\n    cont = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\"]\n    X = [np.ones(len(d))] + [d[c].rank().to_numpy() for c in cont]\n    for y in (2016, 2017):\n        X.append((d.t0 == y).to_numpy(float))\n    for t in (\"method\", \"object\", \"property\"):\n        X.append((d[\"type\"] == t).to_numpy(float))\n    X.append(d[\"generic\"].to_numpy(float))\n    for lv in (3, 4, 5):\n        X.append((d.level == lv).to_numpy(float))\n    return np.column_stack(X)\n\n\ndef psp(x, y, X):\n    keep = np.abs(np.linalg.qr(X)[1].diagonal()) > 1e-9      # drop collinear / empty dummy columns\n    Q, _ = np.linalg.qr(X[:, keep])\n    rx = pd.Series(x).rank().to_numpy(); ry = pd.Series(y).rank().to_numpy()\n    rx = rx - Q @ (Q.T @ rx); ry = ry - Q @ (Q.T @ ry)\n    return float(np.corrcoef(rx, ry)[0, 1])\n\n\nout = {}\nfor b in (\"home\", \"all\"):\n    o = open_score(b)\n    out[f\"OPEN_{b}_max_abs_diff_vs_frozen_table\"] = float(np.nanmax(np.abs(o - F[f\"OPEN_{b}\"])))\n    d = D.assign(o=o).dropna(subset=[\"o\", \"O2r_m50\", \"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"])\n    d = d.reset_index(drop=True)\n    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))\n    rng = np.random.default_rng(1)\n    bs = []\n    for _ in range(400):\n        i = rng.integers(0, len(d), len(d))\n        di = d.iloc[i].reset_index(drop=True)\n        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))\n    out[f\"OPEN_{b}_psp_R2\"] = {\"n\": len(d), \"est\": est, \"ci95_400boot\": [float(np.percentile(bs, 2.5)),\n                                                                          float(np.percentile(bs, 97.5))]}\n    if b == \"home\":\n        # placebo 1: within-group shuffled outcome; placebo 2: random OPEN\n        perm = []\n        for _ in range(200):\n            y = d.O2r_m50.to_numpy().copy()\n            for g in d.agroup.unique():\n                m = (d.agroup == g).to_numpy()\n                y[m] = rng.permutation(y[m])\n            perm.append(psp(d.o.to_numpy(), y, design(d)))\n        perm = np.abs(perm)\n        out[\"placebo_shuffled_outcome\"] = {\"q95_abs\": float(np.percentile(perm, 95)),\n                                           \"share_ge_observed\": float((perm >= abs(est)).mean())}\n        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))\n        out[\"placebo_random_open_psp\"] = rnd\nP = pd.read_parquet(ROOT / \"data/cohort_predictions.parquet\").merge(O, on=\"ci\").dropna()\ns0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]\nout[\"prediction_spearman\"] = {\"n\": len(P), \"B5\": float(s0), \"B5_plus_OPEN_home\": float(s1), \"diff\": float(s1 - s0)}\n(ROOT / \"results/rederive.json\").write_text(json.dumps(out, indent=1))\nprint(json.dumps(out, indent=1))\n---\n#!/usr/bin/env python3\n\"\"\"Post-unseal audit with INDEPENDENT code (statsmodels OLS residuals, scipy ranks/hypergeometric, hand DL).\n\nA1  primary OPEN_home psp (O2r_m50) at R2 and R3 re-derived with statsmodels (target |diff| < 1e-8)\nA2  DL pooled estimate re-derived by hand from the per-group estimates / SEs in cohort_result.json\nA3  O2r_m50 re-computed for 30 random cohort concepts straight from the sealed parts with scipy.stats.hypergeom\nA4  within-group shuffled-outcome control (200 draws; 95th percentile of |psp|) with the independent psp\nA5  planted-signal recovery (psp = 0.10) with the independent psp and a 1,000-draw bootstrap\nWrites results/audit.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nimport statsmodels.api as sm\nfrom scipy.stats import hypergeom, rankdata\n\nfrom common import DATA, RES, jdump, setup_logger\nfrom ladder import rung_design\n\nlogger = setup_logger(\"audit\")\n\n\ndef psp_sm(x, y, B, C) -> float:\n    Z = sm.add_constant(np.c_[np.column_stack([rankdata(B[:, j]) for j in range(B.shape[1])]), C], has_constant=\"add\")\n    rx = sm.OLS(rankdata(x), Z).fit().resid\n    ry = sm.OLS(rankdata(y), Z).fit().resid\n    return float(np.corrcoef(rx, ry)[0, 1])\n\n\ndef design(df, rung, xcol, ycol):\n    Bc, Cc = rung_design(df, rung)\n    x, y = df[xcol].to_numpy(float), df[ycol].to_numpy(float)\n    B, C = Bc.to_numpy(float), Cc.to_numpy(float)\n    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)\n    return x[ok], y[ok], B[ok], C[ok], df[ok]\n\n\ndef rarefy_indep(counts, m=50) -> float:\n    counts = np.asarray([int(c) for c in counts if c > 0])\n    N = counts.sum()\n    if N < m:\n        return math.nan\n    return float(sum(1 - hypergeom(N, int(c), m).pmf(0) for c in counts))\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    res = json.loads((RES / \"cohort_result.json\").read_text())\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    df = pd.read_parquet(DATA / \"analysis_cohort.parquet\")\n    out: dict = {}\n    a1 = {}\n    for r in (\"R2\", \"R3\"):\n        x, y, B, C, _ = design(df, r, \"OPEN_home\", \"O2r_m50\")\n        v = psp_sm(x, y, B, C)\n        ref = res[\"primary\"][f\"OPEN_home|O2r_m50|{r}\"][\"rho\"]\n        a1[r] = {\"statsmodels\": v, \"pipeline\": ref, \"abs_diff\": abs(v - ref), \"pass\": abs(v - ref) < 1e-8}\n    out[\"A1_psp_rederivation\"] = a1\n    a2 = {}\n    for key, g in res[\"groups\"].items():\n        b = np.array([g[\"groups\"][k][\"rho\"] for k in (\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\")], float)\n        se = np.array([g[\"groups\"][k][\"se\"] for k in (\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\")], float)\n        ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n        b, se = b[ok], se[ok]\n        w = 1 / se ** 2\n        mf = np.sum(w * b) / np.sum(w)\n        Q = np.sum(w * (b - mf) ** 2)\n        k = len(b)\n        tau2 = max(0.0, (Q - (k - 1)) / (np.sum(w) - np.sum(w ** 2) / np.sum(w))) if k > 1 else 0.0\n        ws = 1 / (se ** 2 + tau2)\n        est = float(np.sum(ws * b) / np.sum(ws))\n        a2[key] = {\"hand\": est, \"pipeline\": g[\"DL\"][\"b\"], \"abs_diff\": abs(est - g[\"DL\"][\"b\"])}\n    out[\"A2_DL_rederivation\"] = {\"max_abs_diff\": max(v[\"abs_diff\"] for v in a2.values()), \"items\": a2}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 11:18:21 UTC

```
Inspect data files, lib, frozen spec and rederive results:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cd $W; du -sh data/* snapshot inputs passC lib llm_cache 2>/dev/null; ls lib; ls data/*; cat results/rederive.json; head -c 1500 results/frozen_spec.json; echo; python3 -c "
import pandas as pd
for f in ['data/features_cohort.parquet','data/outcomes_cohort.parquet','data/cohort_predictions.parquet','data/analysis_cohort.parquet']:
    d=pd.read_parquet(f); print(f,d.shape); print(list(d.columns))
"
```

### [12] TOOL RESULT — Bash · 2026-09-29 11:18:23 UTC

```
{"stdout": "472K\tdata/analysis_cohort.parquet\n292K\tdata/bg_topics.npz\n181K\tdata/cohort_candidates.csv\n211K\tdata/cohort_candidates_gated.csv\n35K\tdata/cohort_predictions.parquet\n846K\tdata/concept_types.csv\n16K\tdata/controls.csv\n70K\tdata/covariates_cohort.parquet\n366K\tdata/covariates_exp5.parquet\n13M\tdata/ego_open\n131K\tdata/ego_open_cohort.parquet\n202K\tdata/ego_open_cohort_full.parquet\n900K\tdata/ego_open_exp5.parquet\n28K\tdata/ego_open_exp5_u2.parquet\n226K\tdata/exp5_o2r_match_vs_tag.parquet\n300K\tdata/features_cohort.parquet\n2.1M\tdata/features_exp5_open.parquet\n353K\tdata/learned_features_cohort.parquet\n161K\tdata/o5_events_all.parquet\n181K\tdata/outcomes_cohort.parquet\n76K\tdata/passC_bg.npz\n31M\tdata/passC_early.parquet\n512\tdata/passC_info.json\n303K\tdata/passC_pre_agg.parquet\n9.0K\tdata/passC_totals.npz\n36K\tdata/precision_cohort.csv\n15M\tdata/sealed\n82K\tdata/types_cohort_v1.csv\n82K\tdata/types_cohort_v2.csv\n641K\tdata/types_exp5_v1.csv\n641K\tdata/types_exp5_v2.csv\n1.8M\tsnapshot\n24M\tinputs\n104M\tpassC\n1.2M\tlib\n6.6M\tllm_cache\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nfeatport.py\nframe_exp5.py\nh2.py\nindicators.py\nladder.py\nllmc.py\nmatcher.py\nmodels_exp5.py\noutc.py\noutjson.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal2.py\nseal_exp5.py\nstats_core.py\ndata/analysis_cohort.parquet\ndata/bg_topics.npz\ndata/cohort_candidates.csv\ndata/cohort_candidates_gated.csv\ndata/cohort_predictions.parquet\ndata/concept_types.csv\ndata/controls.csv\ndata/covariates_cohort.parquet\ndata/covariates_exp5.parquet\ndata/ego_open_cohort.parquet\ndata/ego_open_cohort_full.parquet\ndata/ego_open_exp5.parquet\ndata/ego_open_exp5_u2.parquet\ndata/exp5_o2r_match_vs_tag.parquet\ndata/features_cohort.parquet\ndata/features_exp5_open.parquet\ndata/learned_features_cohort.parquet\ndata/o5_events_all.parquet\ndata/outcomes_cohort.parquet\ndata/passC_bg.npz\ndata/passC_early.parquet\ndata/passC_info.json\ndata/passC_pre_agg.parquet\ndata/passC_totals.npz\ndata/precision_cohort.csv\ndata/types_cohort_v1.csv\ndata/types_cohort_v2.csv\ndata/types_exp5_v1.csv\ndata/types_exp5_v2.csv\n\ndata/ego_open:\ncohort\ncohort_full\nexp5\nexp5_u2\n\ndata/sealed:\nparts\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 573,\n  \"est\": 0.09059049284973039,\n  \"ci95_400boot\": [\n   0.010749623103553041,\n   0.1650051005616541\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.07152646838735872,\n  \"share_ge_observed\": 0.015\n },\n \"placebo_random_open_psp\": -0.027111739316867493,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 630,\n  \"est\": 0.17410165420736984,\n  \"ci95_400boot\": [\n   0.09568838543012635,\n   0.25899626408340093\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 573,\n  \"B5\": 0.7679289162717833,\n  \"B5_plus_OPEN_home\": 0.7703431304689959,\n  \"diff\": 0.0024142141972126607\n }\n}{\n \"prereg_sha256\": \"36cd2be9c9eaf6c4492ffeee9e9c4a8cd127063949dd57cd7b52bb4e5a732a19\",\n \"spec_v0_sha256\": \"afb00efe4ab8e0903f569f3a4e3ec4f7fa4b7d06106980fd7472c5bee72ccddf\",\n \"open_constants\": {\n  \"home\": {\n   \"new_edge_rate\": {\n    \"lo\": 0.0,\n    \"hi\": 2.0,\n    \"mu\": 0.24226876611794407,\n    \"sd\": 0.29476323739891586,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"n_comm_W3\": {\n    \"lo\": 0.0,\n    \"hi\": 5.0,\n    \"mu\": 1.251940155212417,\n    \"sd\": 1.1109950408968348,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"participation\": {\n    \"lo\": 0.0,\n    \"hi\": 0.7422196372922436,\n    \"mu\": 0.23128455585636246,\n    \"sd\": 0.2522103838072288,\n    \"sign\": 1,\n    \"n\": 8968\n   },\n   \"NOV_res\": {\n    \"lo\": -0.9844771539499432,\n    \"hi\": 0.09593876134862721,\n    \"mu\": -0.540875353868789,\n    \"sd\": 0.3801298233025086,\n    \"sign\": 1,\n    \"n\": 9475\n   },\n   \"ego_density_W3\": {\n    \"lo\": 0.0,\n    \"hi\": 1.0,\n    \"mu\": 0.7333316442122908,\n    \"sd\": 0.2796180574838275,\n    \"sign\": -1,\n    \"n\": 6810\n   },\n   \"edge_persistence\": {\n    \"lo\": 0.0,\n    \"hi\": 0.6739705882352984,\n    \"mu\": 0.12122673391085216,\n    \"sd\": 0.15763666320353067,\n    \"sign\": -1,\n    \"n\": 11236\n   }\n  },\n  \"all\": {\n   \"new_edge_rate\": {\n    \"lo\": 0.0,\n    \"hi\": 1.3333333333333333,\n    \"mu\": 0.2137749421116557,\n    \"sd\": 0.18712524937508748,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"n_comm_W3\": {\n    \"lo\": 0.0,\n    \"hi\": 8.0,\n    \"mu\": 2.5383630690455234,\n    \"sd\": 1.4439512430434749,\n    \"sign\": 1,\n    \"n\": 12499\n   },\n   \"participation\": {\n\ndata/features_cohort.parquet (1443, 72)\n['ci', 'concept_id', 'qid', 'name', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'early_volume', 'role', 'intersection_born', 'precision_c', 'n_labelled_prec', 'precision_source', 'pass_gate', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'agroup', 'home_coverage_early', 'window_flag', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch']\ndata/outcomes_cohort.parquet (1443, 42)\n['ci', 'O1b_TAG', 'O3_TAG', 'peak_year_TAG', 'N_outcome_TAG', 'O2r_m50_TAG', 'O2r_m30_TAG', 'O1c_TAG', 'N_late_all_TAG', 'O1b_MATCH', 'O3_MATCH', 'peak_year_MATCH', 'N_outcome_MATCH', 'O2r_m50_MATCH', 'O2r_m30_MATCH', 'O1c_MATCH', 'N_late_all_MATCH', 'O1b', 'O3', 'O2r_m50', 'O2r_m30', 'O1c', 'N_outcome', 'O2r_resid', 'O2r_m50_le2022_TAG', 'O2r_resid_le2022_TAG', 'O1b_TAG_le2022', 'O3_TAG_le2022', 'peak_year_TAG_le2022', 'N_outcome_TAG_le2022', 'O2r_m50_TAG_le2022', 'O2r_m30_TAG_le2022', 'O1c_TAG_le2022', 'N_late_all_TAG_le2022', 'O1b_MATCH_le2022', 'O3_MATCH_le2022', 'peak_year_MATCH_le2022', 'N_outcome_MATCH_le2022', 'O2r_m50_MATCH_le2022', 'O2r_m30_MATCH_le2022', 'O1c_MATCH_le2022', 'N_late_all_MATCH_le2022']\ndata/cohort_predictions.parquet (1443, 3)\n['ci', 'pred_b5', 'pred_b5_open']\ndata/analysis_cohort.parquet (1443, 113)\n['ci', 'concept_id', 'qid', 'name', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'early_volume', 'role', 'intersection_born', 'precision_c', 'n_labelled_prec', 'precision_source', 'pass_gate', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'agroup', 'home_coverage_early', 'window_flag', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch', 'O1b_TAG', 'O3_TAG', 'peak_year_TAG', 'N_outcome_TAG', 'O2r_m50_TAG', 'O2r_m30_TAG', 'O1c_TAG', 'N_late_all_TAG', 'O1b_MATCH', 'O3_MATCH', 'peak_year_MATCH', 'N_outcome_MATCH', 'O2r_m50_MATCH', 'O2r_m30_MATCH', 'O1c_MATCH', 'N_late_all_MATCH', 'O1b', 'O3', 'O2r_m50', 'O2r_m30', 'O1c', 'N_outcome', 'O2r_resid', 'O2r_m50_le2022_TAG', 'O2r_resid_le2022_TAG', 'O1b_TAG_le2022', 'O3_TAG_le2022', 'peak_year_TAG_le2022', 'N_outcome_TAG_le2022', 'O2r_m50_TAG_le2022', 'O2r_m30_TAG_le2022', 'O1c_TAG_le2022', 'N_late_all_TAG_le2022', 'O1b_MATCH_le2022', 'O3_MATCH_le2022', 'peak_year_MATCH_le2022', 'N_outcome_MATCH_le2022', 'O2r_m50_MATCH_le2022', 'O2r_m30_MATCH_le2022', 'O1c_MATCH_le2022', 'N_late_all_MATCH_le2022']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] TOOL CALL — Bash · 2026-09-29 11:18:53 UTC

```
Build 100-concept mini_demo_data.json from cohort tables:
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/make_mini.py <<'EOF'
import json, numpy as np, pandas as pd
from pathlib import Path
W = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10")
OUT = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/mini_demo_data.json")
spec = json.loads((W/"results/frozen_spec.json").read_text())
F = pd.read_parquet(W/"data/features_cohort.parquet")
O = pd.read_parquet(W/"data/outcomes_cohort.parquet")[["ci","O2r_m50"]]
P = pd.read_parquet(W/"data/cohort_predictions.parquet")
D = F.merge(O, on="ci").merge(P, on="ci")
comps = ["new_edge_rate","n_comm_W3","participation","NOV_res","ego_density_W3","edge_persistence"]
cols = (["ci","concept_id","name","t0","agroup","n_home_early","n_all_early"]
        + [f"{k}__{b}" for b in ("home","all") for k in comps]
        + ["OPEN_home","OPEN_all","logvol","growth_c","offhome_share","entropy","reach","CONTACT_REACH",
           "type","generic","level","O2r_m50","pred_b5","pred_b5_open"])
cov = ["logvol","growth_c","offhome_share","entropy","reach","CONTACT_REACH"]
pool = D.dropna(subset=["OPEN_home","OPEN_all","O2r_m50","pred_b5","pred_b5_open"]+cov)
print("eligible", len(pool), pool.agroup.value_counts().to_dict())
rng = np.random.default_rng(0)
parts = []
groups = sorted(pool.agroup.unique())
per = 100 // len(groups)
for g in groups:
    s = pool[pool.agroup == g]
    # spread across the outcome range: sort by O2r_m50 and take evenly spaced rows
    s = s.sort_values("O2r_m50")
    idx = np.unique(np.linspace(0, len(s)-1, min(per, len(s))).round().astype(int))
    parts.append(s.iloc[idx])
M = pd.concat(parts)[cols].reset_index(drop=True)
print(len(M), M.t0.value_counts().to_dict(), M["type"].value_counts().to_dict(), M.level.value_counts().to_dict())
def clean(v):
    if isinstance(v, (np.integer,)): return int(v)
    if isinstance(v, (np.floating, float)): return None if not np.isfinite(v) else float(v)
    return v
ex = [{k: clean(v) for k, v in r.items()} for r in M.to_dict(orient="records")]
ref = json.loads((W/"results/rederive.json").read_text())
data = {
  "description": "Curated 100-concept subset (20 per analysis group, spread over the outcome range) of the fresh 2015-2017 "
                 "onset cohort of OpenAlex legacy concepts, with the six raw ego-network OPEN components (HOME-ONLY and ALL "
                 "builds), the frozen EXP5 z-score constants, R2-ladder covariates, the primary outcome O2r_m50 and the "
                 "frozen B5 / B5+OPEN_home predictions.",
  "source_files": ["data/features_cohort.parquet", "data/outcomes_cohort.parquet", "data/cohort_predictions.parquet",
                   "results/frozen_spec.json", "results/rederive.json"],
  "frozen_open_constants": {b: spec["open_constants"][b] for b in ("home", "all")},
  "reference_full_run": ref,
  "examples": ex,
}
OUT.write_text(json.dumps(data, indent=1))
print(OUT.stat().st_size)
EOF
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/make_mini.py
```

### [14] TOOL RESULT — Bash · 2026-09-29 11:18:53 UTC

```
{"stdout": "eligible 571 {'BGM+Med': 275, 'CS+Eng': 114, 'SOC': 96, 'LIFEENV': 49, 'PHYS': 27, 'MATHDEC': 10}\n90 {2016: 35, 2015: 34, 2017: 21} {'object': 42, 'topic': 23, 'method': 16, 'property': 9} {3: 45, 2: 25, 4: 15, 5: 5}\n95926", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] ASSISTANT · 2026-09-29 11:18:59 UTC

```
Building the demo data subset now: 90 concepts were selected, so I'm topping it up to 100 before writing the notebook.
```

### [16] TOOL CALL — Bash · 2026-09-29 11:18:59 UTC

```
Top up mini subset to 100 concepts and rebuild:
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/make_mini.py
python3 - "$S" <<'EOF'
import sys
p=sys.argv[1]; s=open(p).read()
s=s.replace('M = pd.concat(parts)[cols].reset_index(drop=True)',
'''M = pd.concat(parts)
rest = pool.drop(M.index)
M = pd.concat([M, rest.sample(100 - len(M), random_state=0)])[cols].reset_index(drop=True)
print(M.agroup.value_counts().to_dict())''')
open(p,'w').write(s)
EOF
python3 $S
```

### [17] TOOL RESULT — Bash · 2026-09-29 11:19:01 UTC

```
{"stdout": "eligible 571 {'BGM+Med': 275, 'CS+Eng': 114, 'SOC': 96, 'LIFEENV': 49, 'PHYS': 27, 'MATHDEC': 10}\n{'BGM+Med': 20, 'CS+Eng': 18, 'SOC': 18, 'LIFEENV': 17, 'PHYS': 17, 'MATHDEC': 10}\n100 {2015: 38, 2016: 37, 2017: 25} {'object': 45, 'topic': 26, 'method': 18, 'property': 11} {3: 49, 2: 28, 4: 17, 5: 6}\n106308", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-29 11:20:21 UTC

```
Generate code_demo.ipynb from builder script:
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/build_nb.py <<'PYEOF'
import json
from pathlib import Path
OUT = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb")
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md(r"""
# Do open-neighbourhood concepts spread? Fresh-cohort test (demo)

This notebook demos **experiment 10**. It is a single-unseal confirmation of the RQ1 *openness* claim, run on a
**fresh 2015–2017 onset cohort** of OpenAlex legacy concepts that no earlier screen had touched.

**What the experiment does**
* **OPEN** is the mean of **six signed, z-scored ego-network components** of a concept's early co-occurrence
  neighbourhood: `new_edge_rate`, `n_comm_W3`, `participation`, `NOV_res`, `−ego_density_W3` and `−edge_persistence`.
  The z-score constants are **frozen** on the 12,499 EXP5 concepts. OPEN comes in three builds: ALL, HOME-ONLY and
  SIZE-MATCHED.
* The primary outcome, **O2r_m50**, is later diffusion breadth: the rarefied number of distinct fields reached at 50 papers.
* The test statistic is the **partial Spearman** (`psp`) of OPEN with O2r_m50. It controls for a ladder of covariates:
  B5 early-size and diffusion baselines, onset year, contact reach, LLM concept type and concept level (rung R2).
* **Full-run result:** the frozen verdict is CONFIRMED but marginal. OPEN_home psp at R2 is +0.091 [+0.013, +0.171]
  (n = 573). OPEN_all is +0.174, which shows that part of the signal is mechanical coupling. OPEN_home adds no practical
  prediction: the B5 Spearman is 0.768 and B5 + OPEN_home is 0.770.

**What this notebook runs**
1. `method.py`, the artifact's demo file. It is an **orchestrator** that chains the 25 pipeline steps as subprocesses:
   an OpenAlex snapshot pass, the LLM precision gate, ego-network builds, the sealed unseal and so on. These steps need
   the full OpenAlex snapshot (about 100 GB of intermediates) and paid LLM calls, so here we only *list* them.
2. The artifact's **independent re-derivation of the headline numbers** (`rederive.py`), which the orchestrator runs as
   its final step, on a curated **100-concept subset** (`mini_demo_data.json`). The code is the original code. Only the
   data loading and the iteration counts differ.
   * Rebuild OPEN_home and OPEN_all from the six raw components with the frozen constants.
   * Compute the R2 partial Spearman, with a bootstrap CI.
   * Run the within-group shuffled-outcome and random-OPEN placebos.
   * Measure the Spearman gain of the B5 + OPEN_home prediction over the B5 prediction.

> With 100 concepts instead of 573, the psp estimates are noisy. A signal of +0.09 is below what n = 100 can resolve.
> The notebook therefore prints the full-run reference values next to the demo values.
""")

code(r"""
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# All packages used here are pre-installed on Colab -> install locally only, at Colab's exact versions
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
""")

md(r"""
## Imports
The first block is `method.py`'s original import block. The second block is `rederive.py`'s. Matplotlib is added for
the final visualisation.
""")
code(r"""
# --- method.py imports (original) ---
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

# --- rederive.py imports (original) ---
import json

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

# --- added for the notebook ---
import matplotlib.pyplot as plt
""")

md(r"""
## Data loading
The data is fetched from GitHub, with a fallback to a local copy of `mini_demo_data.json`.
""")
code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json"
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
code(r"""
data = load_data()
print(data["description"])
print("concepts in demo subset:", len(data["examples"]))
""")

md(r"""
## Config
These are the tunable parameters of the re-derivation. The original values in `rederive.py` are 400 bootstrap draws and
200 within-group permutations, both seeded with `np.random.default_rng(1)`. On 100 concepts the full values run in
seconds, so the demo uses them unchanged.
""")
code(r"""
N_BOOT = 400      # bootstrap draws for the psp CI            (original: 400)
N_PERM = 200      # within-group shuffled-outcome placebos     (original: 200)
SEED = 1          # rng seed                                   (original: 1)
""")

md(r"""
## Step 1: the `method.py` orchestrator
This is the artifact's `method.py`, copied verbatim. There is one notebook fix: `__file__` does not exist in a notebook,
so `ROOT` points at the current directory. Each entry in `STEPS` is a stand-alone script of the pipeline:

| steps | what they do |
|---|---|
| `s0` | hash-seal the preregistration |
| `s1`, `passC*` | candidate concepts plus one zero-credit pass over the OpenAlex snapshot (2026-09-23) |
| `s3` | outcome-blind checks (T1–T3) and TAG-vs-MATCH outcome grounding |
| `s4*` | LLM precision gate (94% of candidates pass) |
| `s7_*` | ego-network builds: ALL / HOME-ONLY / SIZE-MATCHED, for EXP5 and the cohort |
| `s6`, `s5_*` | covariates, LLM concept typing and its gold-label gate |
| `s8` | indicator selection on EXP5 (the frame the constants are frozen on) |
| `s9` | the **single unseal** of the sealed outcomes and the ladder R0–R5 |
| `learned`, `audit`, `tests`, `outputs`, `report`, `rederive` | replications, independent audits and deliverables |

Running a step requires the snapshot and the LLM cache, so the demo only calls `main()` with `--list`.
""")
code(r'''
"""Orchestrator for the fresh-cohort OPEN test. Runs the steps in order (each is also runnable on its own).

Usage: python method.py [--only STEP] [--from STEP] [--list]
Steps (in order): s0 s1 passC passC_merge s3 s4 s4_retry s7_exp5 s7_cohort s7_cohort_full s6 s5_exp5 s5_cohort
                  s5_bench s5_sheet [gold labels are read by hand -> results/type_gold_labels_v1.csv] s5_gate
                  s5_v2 s5_m2all s8 s9 learned audit tests outputs report
Note: s9 performs the SINGLE unseal; a second run only resumes scoring from the hashed outcome file."""

ROOT = Path.cwd()  # notebook fix: original was Path(__file__).resolve().parent
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
''')
code(r"""
# notebook fix: argparse reads sys.argv, which holds the kernel's arguments in Jupyter -> emulate `python method.py --list`
_argv = sys.argv
sys.argv = ["method.py", "--list"]
main()
sys.argv = _argv
""")

md(r"""
## Step 2: the final pipeline step, `rederive.py`
From here on the code is the artifact's `rederive.py`. It re-derives the headline numbers *independently* of the
pipeline code path. The original reads `data/features_cohort.parquet`, `data/outcomes_cohort.parquet`,
`results/frozen_spec.json` and `data/cohort_predictions.parquet`. The demo takes the same columns and constants from
`data` instead.

`SIGN` fixes each component's direction. More new edges, more communities, higher participation and more residual
novelty count as *open*. A denser ego network and more persistent edges count as *closed*.
""")
code(r"""
ROOT = Path.cwd()
spec = {"open_constants": data["frozen_open_constants"]}   # original: json.loads((ROOT / "results/frozen_spec.json").read_text())
F = pd.DataFrame(data["examples"])                          # original: pd.read_parquet(ROOT / "data/features_cohort.parquet")
O = F[["ci", "O2r_m50"]]                                    # original: pd.read_parquet(ROOT / "data/outcomes_cohort.parquet")[["ci", "O2r_m50"]]
D = F.drop(columns=["O2r_m50"]).merge(O, on="ci")
SIGN = {"new_edge_rate": 1, "n_comm_W3": 1, "participation": 1, "NOV_res": 1, "ego_density_W3": -1,
        "edge_persistence": -1}
print(D.shape)
D[["name", "t0", "agroup", "type", "OPEN_home", "OPEN_all", "O2r_m50"]].head(8)
""")

md(r"""
### Rebuilding OPEN from its six raw components
For each component, the value is clipped to the frozen `[lo, hi]` range and z-scored with the frozen EXP5 `mu`/`sd`.
It is then multiplied by its sign. OPEN is the mean of the six z-scores and needs at least 4 non-missing components.
The HOME-ONLY and SIZE-MATCHED builds also require ≥ 10 early papers in the concept's home field.

`design()` builds the **R2 rung** of the covariate ladder. It has these columns:
* rank-transformed B5 covariates plus CONTACT_REACH;
* onset-year dummies;
* LLM concept-type dummies, with `topic` as the reference;
* a generic flag;
* concept-level dummies.

`psp()` is the partial Spearman. It ranks x and y, residualises both on the design via QR (dropping collinear or
empty dummy columns) and correlates the residuals.
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
### Partial Spearman at R2, bootstrap CI and placebos
This loop runs once for the HOME-ONLY build and once for the ALL build. For each build it:
1. rebuilds OPEN and checks it against the stored frozen table, where `max_abs_diff` should be 0;
2. computes the R2 psp with O2r_m50 and a percentile bootstrap CI over concepts (`N_BOOT` draws).

For HOME it also runs two placebos. Both should look null.
* **Shuffled outcome:** O2r_m50 is permuted *within analysis group* (`N_PERM` draws). The observed |psp| is compared
  with the permutation distribution.
* **Random OPEN:** a standard-normal vector replaces OPEN.

In the full run, ALL − HOME measures *mechanical coupling*. The ALL build includes off-home neighbours, which are partly
the same papers that later count toward diffusion breadth.
""")
code(r"""
out = {}
boot_draws = {}   # notebook addition: keep the draws for plotting
for b in ("home", "all"):
    o = open_score(b)
    out[f"OPEN_{b}_max_abs_diff_vs_frozen_table"] = float(np.nanmax(np.abs(o - F[f"OPEN_{b}"])))
    d = D.assign(o=o).dropna(subset=["o", "O2r_m50", "logvol", "growth_c", "offhome_share", "entropy", "reach"])
    d = d.reset_index(drop=True)
    est = psp(d.o.to_numpy(), d.O2r_m50.to_numpy(), design(d))
    rng = np.random.default_rng(SEED)
    bs = []
    for _ in range(N_BOOT):
        i = rng.integers(0, len(d), len(d))
        di = d.iloc[i].reset_index(drop=True)
        bs.append(psp(di.o.to_numpy(), di.O2r_m50.to_numpy(), design(di)))
    boot_draws[b] = bs
    out[f"OPEN_{b}_psp_R2"] = {"n": len(d), "est": est, "ci95_boot": [float(np.percentile(bs, 2.5)),
                                                                       float(np.percentile(bs, 97.5))]}
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
        rnd = psp(rng.normal(size=len(d)), d.O2r_m50.to_numpy(), design(d))
        out["placebo_random_open_psp"] = rnd
""")

md(r"""
### Practical prediction: B5 vs B5 + OPEN_home
Both predictions are **frozen OLS models** fitted on the EXP5 frame and stored per concept. The first uses B5 alone and
the second uses B5 + OPEN_home. We compare their Spearman correlation with the realised O2r_m50. In the full run the
gain is +0.002, i.e. no practical improvement.
""")
code(r"""
P = D[["ci", "pred_b5", "pred_b5_open"]].merge(O, on="ci").dropna()   # original: pd.read_parquet(ROOT / "data/cohort_predictions.parquet").merge(O, on="ci").dropna()
s0, s1 = spearmanr(P.pred_b5, P.O2r_m50)[0], spearmanr(P.pred_b5_open, P.O2r_m50)[0]
out["prediction_spearman"] = {"n": len(P), "B5": float(s0), "B5_plus_OPEN_home": float(s1), "diff": float(s1 - s0)}
# original wrote results/rederive.json; the notebook just prints it
print(json.dumps(out, indent=1))
""")

md(r"""
## Results: demo subset vs full run
The table lists each headline quantity for the 100-concept demo subset next to the full-cohort run (`rederive.json`).
The figure has three panels:
* **(a)** the psp estimates with their bootstrap CIs;
* **(b)** the bootstrap distributions on the demo subset;
* **(c)** the frozen B5 prediction against realised diffusion breadth, coloured by OPEN_home.
""")
code(r"""
ref = data["reference_full_run"]
rows = [
    ("OPEN_home psp R2", out["OPEN_home_psp_R2"], ref["OPEN_home_psp_R2"]),
    ("OPEN_all psp R2", out["OPEN_all_psp_R2"], ref["OPEN_all_psp_R2"]),
]
tab = pd.DataFrame([{
    "quantity": name, "demo n": o_["n"], "demo est": round(o_["est"], 3),
    "demo 95% CI": f"[{o_['ci95_boot'][0]:+.3f}, {o_['ci95_boot'][1]:+.3f}]",
    "full n": r_["n"], "full est": round(r_["est"], 3),
    "full 95% CI": f"[{r_['ci95_400boot'][0]:+.3f}, {r_['ci95_400boot'][1]:+.3f}]"} for name, o_, r_ in rows])
extra = pd.DataFrame([
    {"quantity": "OPEN rebuild max |diff| (home / all)",
     "demo": f"{out['OPEN_home_max_abs_diff_vs_frozen_table']:.1e} / {out['OPEN_all_max_abs_diff_vs_frozen_table']:.1e}",
     "full": f"{ref['OPEN_home_max_abs_diff_vs_frozen_table']:.1e} / {ref['OPEN_all_max_abs_diff_vs_frozen_table']:.1e}"},
    {"quantity": "shuffled-outcome placebo q95 |psp|", "demo": f"{out['placebo_shuffled_outcome']['q95_abs']:.3f}",
     "full": f"{ref['placebo_shuffled_outcome']['q95_abs']:.3f}"},
    {"quantity": "share of placebos >= observed", "demo": f"{out['placebo_shuffled_outcome']['share_ge_observed']:.3f}",
     "full": f"{ref['placebo_shuffled_outcome']['share_ge_observed']:.3f}"},
    {"quantity": "random-OPEN placebo psp", "demo": f"{out['placebo_random_open_psp']:+.3f}",
     "full": f"{ref['placebo_random_open_psp']:+.3f}"},
    {"quantity": "Spearman B5 -> B5+OPEN_home",
     "demo": f"{out['prediction_spearman']['B5']:.3f} -> {out['prediction_spearman']['B5_plus_OPEN_home']:.3f}",
     "full": f"{ref['prediction_spearman']['B5']:.3f} -> {ref['prediction_spearman']['B5_plus_OPEN_home']:.3f}"},
])
pd.set_option("display.width", 200)
print(tab.to_string(index=False)); print(); print(extra.to_string(index=False))

fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
# (a) point estimates + CIs, demo vs full
labels = ["OPEN_home", "OPEN_all"]
for j, (lab, (_, o_, r_)) in enumerate(zip(labels, rows)):
    ax[0].errorbar(j - 0.12, o_["est"], yerr=[[o_["est"] - o_["ci95_boot"][0]], [o_["ci95_boot"][1] - o_["est"]]],
                   fmt="o", color="tab:orange", capsize=4, label="demo (n=100)" if j == 0 else None)
    ax[0].errorbar(j + 0.12, r_["est"], yerr=[[r_["est"] - r_["ci95_400boot"][0]], [r_["ci95_400boot"][1] - r_["est"]]],
                   fmt="s", color="tab:blue", capsize=4, label="full cohort" if j == 0 else None)
ax[0].axhline(0, color="grey", lw=0.8, ls="--")
ax[0].set_xticks([0, 1]); ax[0].set_xticklabels(labels); ax[0].set_xlim(-0.5, 1.5)
ax[0].set_ylabel("partial Spearman with O2r_m50 (R2)"); ax[0].set_title("(a) OPEN psp, 95% bootstrap CI"); ax[0].legend()
# (b) bootstrap distributions
for b, col in (("home", "tab:orange"), ("all", "tab:green")):
    ax[1].hist(boot_draws[b], bins=25, alpha=0.55, color=col, label=f"OPEN_{b}")
ax[1].axvline(0, color="grey", lw=0.8, ls="--")
ax[1].set_xlabel("bootstrap psp"); ax[1].set_title(f"(b) demo bootstrap draws (N_BOOT={N_BOOT})"); ax[1].legend()
# (c) frozen B5 prediction vs realised outcome
sc = ax[2].scatter(P.pred_b5, P.O2r_m50, c=D.set_index("ci").loc[P.ci, "OPEN_home"], cmap="viridis", s=22)
lim = [min(P.pred_b5.min(), P.O2r_m50.min()), max(P.pred_b5.max(), P.O2r_m50.max())]
ax[2].plot(lim, lim, color="grey", lw=0.8, ls="--")
ax[2].set_xlabel("frozen B5 prediction"); ax[2].set_ylabel("realised O2r_m50 (fields at 50 papers)")
ax[2].set_title(f"(c) B5 Spearman {out['prediction_spearman']['B5']:.3f}; +OPEN_home "
                f"{out['prediction_spearman']['B5_plus_OPEN_home']:.3f}")
plt.colorbar(sc, ax=ax[2], label="OPEN_home")
plt.tight_layout(); plt.show()
""")

md(r"""
**How to read this.**
* The OPEN rebuild from raw components reproduces the frozen table exactly.
* On the full cohort, OPEN_home has a small positive partial association with later diffusion breadth, +0.091 with a CI
  just above 0. OPEN_all is about twice as large, which reflects mechanical coupling with the off-home neighbourhood.
* Neither the shuffled-outcome placebo nor the random-OPEN placebo produces a comparable signal.
* The frozen B5 baseline already predicts O2r_m50 well, and adding OPEN_home leaves the Spearman practically unchanged.
* On the 100-concept demo subset the CIs are about 2.4× wider (√(573/100)), so the demo estimates should be read as an
  illustration of the procedure, not as a replication of the verdict.
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
for i, c in enumerate(nb["cells"]):
    c["id"] = f"cell-{i}"
OUT.write_text(json.dumps(nb, indent=1))
print("wrote", OUT)
PYEOF
python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/build_nb.py
```

### [19] TOOL RESULT — Bash · 2026-09-29 11:20:21 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF/code_demo.ipynb", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] ASSISTANT · 2026-09-29 11:20:27 UTC

```
Notebook written. First test at minimum config (N_BOOT=10, N_PERM=5), then scale to the original 400/200.
```

### [21] TOOL CALL — Bash · 2026-09-29 11:20:27 UTC

```
Test-run notebook at minimum config in clean venv:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
sed -i 's/N_BOOT = 400 /N_BOOT = 10  /; s/N_PERM = 200 /N_PERM = 5   /' code_demo.ipynb; grep -o 'N_BOOT = [0-9]*\|N_PERM = [0-9]*' code_demo.ipynb | head
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/python jupyter ipykernel
time /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20
```

### [22] TOOL RESULT — Bash · 2026-09-29 11:21:11 UTC

```
{"stdout": "N_BOOT = 10\nN_PERM = 5\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 157894 bytes to code_demo.ipynb\n\nreal\t0m18.539s\nuser\t0m14.941s\nsys\t0m1.377s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] ASSISTANT · 2026-09-29 11:21:15 UTC

```
Passed in 18.5 s. Now scaling to 100/50, then to the original 400/200.
```

### [24] TOOL CALL — Bash · 2026-09-29 11:21:15 UTC

```
Scale notebook config in two rounds and time each run:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
J=/tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/jupyter
sed -i 's/N_BOOT = 10  /N_BOOT = 100 /; s/N_PERM = 5   /N_PERM = 50  /' code_demo.ipynb
( time $J nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb ) 2>&1 | grep -E 'real|Error'
sed -i 's/N_BOOT = 100 /N_BOOT = 400 /; s/N_PERM = 50  /N_PERM = 200 /' code_demo.ipynb; grep -o 'N_BOOT = [0-9]*\|N_PERM = [0-9]*' code_demo.ipynb|head -2
( time $J nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb ) 2>&1 | grep -E 'real|Error'
```

### [25] TOOL RESULT — Bash · 2026-09-29 11:21:27 UTC

```
{"stdout": "real\t0m5.360s\nN_BOOT = 400\nN_PERM = 200\nreal\t0m5.825s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-29 11:21:33 UTC

```
Print executed notebook outputs and verify URL:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
python3 -c "
import json; nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(o['text'][-2500:] if isinstance(o['text'],str) else ''.join(o['text'])[-2500:])
        elif o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
        else: print('[',o['output_type'], list(o.get('data',{}).keys()),']')
"; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json"' code_demo.ipynb; ls -la
```

### [27] TOOL RESULT — Bash · 2026-09-29 11:21:33 UTC

```
{"stdout": "Curated 100-concept subset (20 per analysis group, spread over the outcome range) of the fresh 2015-2017 onset cohort of OpenAlex legacy concepts, with the six raw ego-network OPEN components (HOME-ONLY and ALL builds), the frozen EXP5 z-score constants, R2-ladder covariates, the primary outcome O2r_m50 and the frozen B5 / B5+OPEN_home predictions.\nconcepts in demo subset: 100\n\ns0\ns1\npassC\npassC_merge\ns3\ns4\ns4_retry\ns7_exp5\ns7_cohort\ns7_cohort_full\ns6\ns5_exp5\ns5_cohort\ns5_bench\ns5_sheet\ns5_gate\ns5_v2\ns5_m2all\ns8\ns9\nlearned\naudit\ntests\noutputs\nreport\nrederive\n\n(100, 33)\n\n[ execute_result ['text/html', 'text/plain'] ]\n{\n \"OPEN_home_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_home_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.19417387123372648,\n  \"ci95_boot\": [\n   -0.058985189064649245,\n   0.42733744197445656\n  ]\n },\n \"placebo_shuffled_outcome\": {\n  \"q95_abs\": 0.23466376674979347,\n  \"share_ge_observed\": 0.12\n },\n \"placebo_random_open_psp\": -0.10675824498939766,\n \"OPEN_all_max_abs_diff_vs_frozen_table\": 0.0,\n \"OPEN_all_psp_R2\": {\n  \"n\": 100,\n  \"est\": 0.25704521503759253,\n  \"ci95_boot\": [\n   0.027359370530844078,\n   0.45737953711659707\n  ]\n },\n \"prediction_spearman\": {\n  \"n\": 100,\n  \"B5\": 0.8027867710777288,\n  \"B5_plus_OPEN_home\": 0.8087455636003793,\n  \"diff\": 0.0059587925226505245\n }\n}\n\n        quantity  demo n  demo est      demo 95% CI  full n  full est      full 95% CI\nOPEN_home psp R2     100     0.194 [-0.059, +0.427]     573     0.091 [+0.011, +0.165]\n OPEN_all psp R2     100     0.257 [+0.027, +0.457]     630     0.174 [+0.096, +0.259]\n\n                            quantity              demo              full\nOPEN rebuild max |diff| (home / all) 0.0e+00 / 0.0e+00 0.0e+00 / 0.0e+00\n  shuffled-outcome placebo q95 |psp|             0.235             0.072\n       share of placebos >= observed             0.120             0.015\n             random-OPEN placebo psp            -0.107            -0.027\n         Spearman B5 -> B5+OPEN_home    0.803 -> 0.809    0.768 -> 0.770\n\n[ display_data ['image/png', 'text/plain'] ]\n0\ntotal 2536\ndrwxr-xr-x  3 root root 1048430 Sep 29 11:21 .\ndrwxr-xr-x  4 root root 1050005 Sep 29 11:20 ..\ndrwxr-xr-x  2 root root       1 Sep 29 11:17 .aii\n-rw-------  1 root root      54 Sep 29 11:17 .aii_claude_session.json\n-rw-r--r--  1 root root  232581 Sep 29 11:21 .repl_agent.ptylog\n-rw-r--r--+ 1 root root  157254 Sep 29 11:21 code_demo.ipynb\n-rw-r--r--  1 root root  106308 Sep 29 11:18 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] ASSISTANT · 2026-09-29 11:21:43 UTC

```
The run passes at the original 400/200 in about 6 s. Next I'll fix an inaccurate "20 per group" description in the data, then do a final clean-venv run and verify the URL.
```

### [29] TOOL CALL — Bash · 2026-09-29 11:21:43 UTC

```
Rebuild data, run final clean-venv test, verify URL:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad
sed -i 's/Curated 100-concept subset (20 per analysis group, spread over the outcome range)/Curated 100-concept subset (up to 16 per analysis group, evenly spread over the outcome range, topped up at random to 100)/' $S/make_mini.py
python3 $S/make_mini.py | tail -1
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/python jupyter ipykernel
( time /tmp/aii_nb_test_envs/art_NMe386dX9GLF-6fd0b7bb7ed1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb ) 2>&1 | grep -E 'real|Error|Writing'
python3 -c "
import json; nb=json.load(open('code_demo.ipynb'))
src=''.join(''.join(c['source']) for c in nb['cells'])
print('URL exact:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-4/experiment-10/demo/mini_demo_data.json\"' in src)
print('urlopen:', 'urllib.request.urlopen(GITHUB_DATA_URL)' in src)
print('errors:', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))
print('config:', [l for l in src.splitlines() if l.startswith(('N_BOOT','N_PERM'))])
"
```

### [30] TOOL RESULT — Bash · 2026-09-29 11:22:53 UTC

```
{"stdout": "106349\n[NbConvertApp] Writing 157278 bytes to code_demo.ipynb\nreal\t1m6.978s\nURL exact: True\nurlopen: True\nerrors: 0\nconfig: ['N_PERM = 200      # within-group shuffled-outcome placebos     (original: 200)']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] ASSISTANT · 2026-09-29 11:23:01 UTC

```
Clean run passed: 67 s, no errors, exact URL present. I'll check the figure.
```

### [32] TOOL CALL — Bash · 2026-09-29 11:23:01 UTC

```
Extract figure PNG to scratchpad:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
python3 -c "
import json,base64; nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if 'image/png' in o.get('data',{}): open('$HOME/../tmp/claude-0/fig.png','wb') if False else None; open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
print([l for c in nb['cells'] for l in ''.join(c['source']).splitlines() if 'N_BOOT =' in l])
"
```

### [33] TOOL RESULT — Bash · 2026-09-29 11:23:01 UTC

```
{"stdout": "['N_BOOT = 400      # bootstrap draws for the psp CI            (original: 400)']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Read · 2026-09-29 11:23:01 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-4-art-NMe386dX9GLF/b7ada402-b91f-4909-8825-9c2d370e1242/scratchpad/fig.png
```

### [35] TOOL RESULT — Read · 2026-09-29 11:23:02 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [36] ASSISTANT · 2026-09-29 11:23:13 UTC

```
The figure looks right. Last step: the manifest, README and structured output.
```

### [37] TOOL CALL — Bash · 2026-09-29 11:23:13 UTC

```
Write manifest, README and structured output JSON:
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_4/art_NMe386dX9GLF
cat > .aii/manifest.yaml <<'EOF'
# Nothing heavy in this workspace: code_demo.ipynb (~160 KB) and mini_demo_data.json (~105 KB) are small text files.
# The test venv lives outside the workspace (/tmp) and is removed by the pipeline.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: do open-neighbourhood concepts spread? (fresh-cohort test, experiment 10)

This is a Colab-ready demo notebook for the fresh 2015–2017 onset-cohort test of the RQ1 **openness (OPEN)** claim.
OPEN is the mean of six signed, z-scored ego-network components, with z-score constants frozen on the 12,499 EXP5
concepts. The test asks whether a concept's OPEN score predicts its later diffusion breadth, **O2r_m50**, beyond the B5
baseline covariates.

## What the notebook does
1. It shows the artifact's `method.py` orchestrator verbatim and lists its 25 pipeline steps. The steps are not
   executed, because they need the full OpenAlex snapshot and paid LLM calls.
2. It runs the artifact's independent re-derivation (`rederive.py`, the orchestrator's last step) essentially unchanged
   on a curated 100-concept subset. The re-derivation covers:
   * the OPEN_home and OPEN_all rebuild from raw components with the frozen constants;
   * the R2 partial Spearman with O2r_m50 and a 400-draw bootstrap CI;
   * a within-group shuffled-outcome placebo (200 draws) and a random-OPEN placebo;
   * the Spearman of B5 vs B5 + OPEN_home.
3. It prints demo vs full-cohort values side by side and plots them.

The full-cohort reference values are OPEN_home psp +0.091 [+0.011, +0.165] (n = 573) and OPEN_all +0.174. The B5 → B5 +
OPEN_home Spearman goes from 0.768 to 0.770. With n = 100 the demo CIs are about 2.4× wider, so the demo illustrates
the procedure and does not replicate the verdict.

## Layout
| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook (runs in ~1 min in a clean env, incl. installs; ~6 s of compute) |
| `mini_demo_data.json` | 100 cohort concepts spread across 6 analysis groups and the outcome range; frozen OPEN constants; full-run reference numbers |
| `.aii/manifest.yaml` | storage manifest (no heavy files) |

## How to run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The data loads from the GitHub raw URL and falls back to
the local `mini_demo_data.json`. Locally, the install cell pins numpy/pandas/scipy/matplotlib to Colab's versions.

## Restoring removed files
Nothing is marked `delete` in the manifest, so there is nothing to restore.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; ls -la
```

### [38] TOOL RESULT — Bash · 2026-09-29 11:23:13 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\ntotal 2686\ndrwxr-xr-x 3 root root 1057462 Sep 29 11:23 .\ndrwxr-xr-x 4 root root 1080429 Sep 29 11:20 ..\ndrwxr-xr-x 2 root root   21200 Sep 29 11:23 .aii\n-rw------- 1 root root      54 Sep 29 11:17 .aii_claude_session.json\n-rw-r--r-- 1 root root  324134 Sep 29 11:23 .repl_agent.ptylog\n-rw-r--r-- 1 root root      97 Sep 29 11:23 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root    2217 Sep 29 11:23 README.md\n-rw-r--r-- 1 root root  157295 Sep 29 11:22 code_demo.ipynb\n-rw-r--r-- 1 root root  106349 Sep 29 11:21 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-29 11:23:24 UTC

```
The demo notebook runs from top to bottom in a clean Python 3.12 environment with no errors. It takes about 67 s including package installs, well under the 10-minute limit, and uses the original parameters: 400 bootstrap draws and 200 permutations.

**What "the script" turned out to be.** The artifact's `method.py` is only a launcher that runs 25 pipeline scripts in turn. Those scripts need the full OpenAlex snapshot (about 100 GB of intermediate files) and paid LLM calls, so the notebook can't run them. It shows `method.py` unchanged and only lists the steps with `--list`. Two small notebook fixes were needed: `ROOT` points at the current directory, and `sys.argv` is set before calling `main()`.

**What actually runs.** The computation comes from `rederive.py`, the pipeline's final step, which independently recomputes the headline numbers. Its code is unchanged except that it reads from the loaded data instead of the parquet files, the iteration counts come from the config cell, and it prints results instead of writing `results/rederive.json`. It does four things:
- rebuilds `OPEN_home` and `OPEN_all` from the six network components using the frozen constants;
- computes the R2 partial Spearman with a bootstrap confidence interval;
- runs the shuffled-outcome and random-OPEN placebos;
- compares how well B5 and B5 + `OPEN_home` predict the outcome.

**Data.** `mini_demo_data.json` holds 100 cohort concepts from all six field groups, spread across the outcome range. It also carries the frozen constants and the full-run reference numbers.

**Results on 100 concepts vs the full cohort:**

| Quantity | Demo (n = 100) | Full run |
|---|---|---|
| OPEN rebuild vs stored table | exact (difference 0) | exact (difference 0) |
| `OPEN_home` partial Spearman (R2) | +0.194 [−0.059, +0.427] | +0.091 [+0.011, +0.165] (n = 573) |
| `OPEN_all` partial Spearman (R2) | +0.257 | +0.174 |
| Spearman, B5 → B5 + `OPEN_home` | 0.803 → 0.809 | 0.768 → 0.770 |

With only 100 concepts the intervals are about 2.4× wider, and the demo's `OPEN_home` interval includes zero. The notebook shows the full-run values alongside and says the demo illustrates the procedure rather than repeating the CONFIRMED verdict. The final cell prints this comparison table and a three-panel figure.

- **Figure panels:** the estimates with their intervals, the bootstrap distributions, and B5 predictions against actual diffusion breadth coloured by `OPEN_home`.
- **Checks:** the GitHub URL line matches exactly, and the loader tries that URL first and falls back to the local file.
- **Storage and repo files:** there are no large files, so `.aii/manifest.yaml` has an empty entry list. The `README.md` is written, and the structured output file points to the notebook and the data file.

Files are in `art_NMe386dX9GLF/`:
- code_demo.ipynb
- mini_demo_data.json
- README.md
- .aii/manifest.yaml
- .terminal_claude_agent_struct_out.json
```
