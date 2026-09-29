# gen_demo_art_experiment_13 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_13` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 11:42:52 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 11:42:58 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-16/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-16/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-16/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 11:43:04 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 11:43:04 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 11:43:04 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 11:43:04 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 11:43:04 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 && ls -la && ls lib data results tests 2>/dev/null | head -50 && wc -l method.py && ls -la /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z
```

### [8] TOOL RESULT — Bash · 2026-09-29 11:43:06 UTC

```
{"stdout": "total 38533\ndrwxrwxrwx 10 root root  2027924 Sep 29 09:02 .\ndrwxrwxrwx  7 root root  3000249 Sep 29 05:17 ..\ndrwxrwxrwx  2 root root   100800 Sep 29 06:28 .aii\n-rw-rw-rw-  1 root root       54 Sep 29 05:18 .aii_claude_session.json\n-rw-rw-rw-  1 root root     9154 Sep 29 06:28 .aii_worker_result.json\n-rw-rw-rw-  1 root root  1918369 Sep 29 06:28 .repl_agent.ptylog\n-rw-rw-rw-  1 root root     3354 Sep 29 06:26 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 root root    13917 Sep 29 06:27 README.md\ndrwxrwxrwx  3 root root  2025210 Sep 29 09:02 data\ndrwxrwxrwx  2 root root  1056430 Sep 29 06:19 figures\n-rw-rw-rw-  1 root root 12422709 Sep 29 06:26 full_method_out.json\ndrwxrwxrwx  2 root root  1009698 Sep 29 09:02 lib\ndrwxrwxrwx  2 root root  1010536 Sep 29 06:24 logs\n-rw-rw-rw-  1 root root    12025 Sep 29 06:21 method.py\n-rw-rw-rw-  1 root root 11688840 Sep 29 06:21 method_out.json\n-rw-rw-rw-  1 root root    15065 Sep 29 06:26 mini_method_out.json\ndrwxrwxrwx  2 root root        1 Sep 29 06:25 models\n-rw-rw-rw-  1 root root    12774 Sep 29 06:26 preview_method_out.json\n-rw-rw-rw-  1 root root      839 Sep 29 06:25 pyproject.toml\n-rw-rw-rw-  1 root root     6760 Sep 29 05:56 rederive.py\n-rw-rw-rw-  1 root root     7108 Sep 29 06:26 reproducibility.md\n-rwxrwxrwx  1 root root      772 Sep 29 06:23 restore.sh\ndrwxrwxrwx  2 root root  2000137 Sep 29 06:25 results\n-rw-rw-rw-  1 root root     5133 Sep 29 05:24 s0_gate.py\n-rw-rw-rw-  1 root root    10781 Sep 29 05:31 s1_freeze.py\n-rw-rw-rw-  1 root root     9379 Sep 29 05:31 s2_variants.py\n-rw-rw-rw-  1 root root    15659 Sep 29 05:36 s3_nulls.py\n-rw-rw-rw-  1 root root    13130 Sep 29 05:39 s4_composites.py\n-rw-rw-rw-  1 root root     6646 Sep 29 05:40 s4b_outcome_rel.py\n-rw-rw-rw-  1 root root     7685 Sep 29 05:44 s5_size.py\n-rw-rw-rw-  1 root root     8735 Sep 29 05:43 s6_assoc.py\n-rw-rw-rw-  1 root root    15374 Sep 29 05:53 s7_verdict.py\n-rw-rw-rw-  1 root root    10981 Sep 29 06:19 s8_power.py\ndrwxrwxrwx  2 root root  1002156 Sep 29 06:25 tests\ndata:\nclean_variants.parquet\npsp_boot.npz\ns2_parts_full\ns2_scalars_full.parquet\nv3_nulls_full.parquet\nv4_half_means.npz\n\nlib:\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nfast6.py\nfastpsp.py\njobs.py\nladder.py\nnullkern.py\noutc.py\nrq1stats.py\ns2_cfg.py\nseal.py\nstats_core.py\ntables.py\n\nresults:\nclean_vs_raw_psp.json\nclean_vs_raw_psp_cells.json\ndeviations.json\nfrozen_constants_S1b.json\nfrozen_spec.json\ngate_t0.json\nheadline_check.json\nplacebo_calibration.json\nplanted_checks.json\npower_frame_n.json\nprediction_check.json\nrederive.json\nreliability.json\nreliability_x.json\nsize_dependence.json\nunit_tests.json\nunit_tests_fast6.json\nunit_tests_fastpsp.json\nunit_tests_nulls.json\nv3_nulls_full.json\n\ntests:\n215 method.py\ntotal 2968\ndrwxrwxrwx 3 root root 1003269 Sep 29 11:42 .\ndrwxrwxrwx 7 root root 2000510 Sep 29 11:41 ..\ndrwxrwxrwx 2 root root       1 Sep 29 11:41 .aii\n-rw-rw-rw- 1 root root      54 Sep 29 11:42 .aii_claude_session.json\n-rw-rw-rw- 1 root root   33430 Sep 29 11:43 .repl_agent.ptylog", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 11:43:08 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 && cat method.py && cat pyproject.toml && head -c 3000 preview_method_out.json
```

### [10] TOOL RESULT — Bash · 2026-09-29 11:43:08 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.\n\nStages (each a standalone, resumable script; run in this order by `python method.py --run-all`):\n  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)\n  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)\n  s1_freeze.py          frozen spec + seal (before any outcome join)\n  s2_variants.py        RAW, V1 rarefaction, V2 permutation null, V2b Chao Jaccard, V4 split halves\n  s3_nulls.py           V3a backbone rewiring, V3b k-matched density null, V3c curveball persistence null\n  tests/u_nulls.py      U3 curveball uniformity, U4 rewire calibration\n  tests/planted.py      PC1 stationary thin-sample simulation, PC2 planted churn\n  s4_composites.py      clean composites, S1b constants seal, V4 reliability (X side)\n  s4b_outcome_rel.py    outcome reliability (O2r_m50, m = 25 halves)\n  s5_size.py            size-dependence diagnostics\n  s6_assoc.py           partial Spearman ladder per body / pooled, paired clean-vs-raw, groups, PC3\n  s7_verdict.py         DL, disattenuation, P1-P3, Holm, VERDICT, figures\n  s8_power.py           Frame-N power simulation\n  rederive.py           independent re-derivation of the P1-P3 numbers and the pooled SB\nThen (this file): method_out.json in exp_gen_sol_out format -- one example per concept with finite O2r_m50;\npredictions from OLS fitted on DEV only (B5 standardised with the frozen EXP10 constants) applied to every body;\nresults/prediction_check.json; the concept-key cross-check against art_O7Dq4L02QnDN.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport math\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy import stats\n\nfrom common import DATA, O5DIR, RES, jdump, setup_logger\n\nSTAGES = [(\"s0_gate.py\", RES / \"gate_t0.json\"), (\"tests/u_fast6.py\", RES / \"unit_tests_fast6.json\"),\n          (\"s1_freeze.py\", RES / \"frozen_spec.json\"), (\"s2_variants.py\", DATA / \"s2_scalars_full.parquet\"),\n          (\"s3_nulls.py\", DATA / \"v3_nulls_full.parquet\"), (\"tests/u_nulls.py\", RES / \"unit_tests_nulls.json\"),\n          (\"tests/planted.py\", RES / \"planted_checks.json\"), (\"s4_composites.py\", DATA / \"clean_variants.parquet\"),\n          (\"s4b_outcome_rel.py\", RES / \"reliability.json\"), (\"s5_size.py\", RES / \"size_dependence.json\"),\n          (\"s6_assoc.py\", RES / \"clean_vs_raw_psp_cells.json\"), (\"s7_verdict.py\", RES / \"clean_vs_raw_psp.json\"),\n          (\"s8_power.py\", RES / \"power_frame_n.json\"), (\"rederive.py\", RES / \"rederive.json\")]\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nPRED_X = {\"B5\": None, \"B5_plus_NOVCHURN_raw\": \"NOVCHURN_raw\", \"B5_plus_NOVCHURN_exc\": \"NOVCHURN_exc\",\n          \"B5_plus_NOVCHURN_cfg\": \"NOVCHURN_cfg\", \"B5_plus_OPEN_home\": \"OPEN_home\",\n          \"B5_plus_OPEN_home_clean\": \"OPEN_home_clean\"}\nINPUT_COLS = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"new_edge_rate__raw\", \"n_comm_W3__raw\",\n              \"participation__raw\", \"NOVCHURN_raw\", \"OPEN_home\", \"NOV_res_rare10\", \"edge_persistence_rare10\",\n              \"NOVCHURN_rare10\", \"NOV_res_rare5\", \"edge_persistence_rare5\", \"NOVCHURN_rare5\", \"NOV_res_exc\",\n              \"edge_persistence_exc\", \"edge_persistence_nullmean\", \"NOVCHURN_exc\", \"EP_chao\", \"NOVCHURN_chao\",\n              \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\", \"excess_pers_cfg\", \"NOVCHURN_cfg\", \"OPEN_home_clean\",\n              \"OPEN_home_exc\"]\n\n\ndef run_stages(force: bool) -> None:\n    for script, out in STAGES:\n        if out.exists() and not force:\n            logger.info(f\"skip {script} ({out.name} exists)\")\n            continue\n        if script == \"s1_freeze.py\" and out.exists():\n            logger.warning(\"frozen_spec.json exists: never re-freeze (seal)\")\n            continue\n        logger.info(f\"running {script}\")\n        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)\n\n\ndef concept_key_check() -> dict:\n    \"\"\"Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its\n    concept_recognition table and agreement of the OpenAlex level.\"\"\"\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\", columns=[\"concept_id\", \"body\"])\n    from common import DATA_IN\n    lev = pd.concat([pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"concept_id\", \"level\"]),\n                     pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"concept_id\", \"level\"])])\n    norm = lambda v: \"C\" + str(v).lstrip(\"C\").split(\".\")[0]  # noqa: E731  (frame ids are numeric; O5 uses 'C...')\n    lev = dict(zip(lev.concept_id.map(norm), lev.level))\n    cv[\"concept_id\"] = cv.concept_id.map(norm)\n    ids = set(cv.concept_id)\n    seen, level_ok, n_rec = {}, 0, 0\n    for p in sorted((O5DIR / \"full_data_out\").glob(\"full_data_out_*.json\")):\n        d = json.loads(p.read_text())\n        for ds in d[\"datasets\"]:\n            if ds[\"dataset\"] != \"concept_recognition\":\n                continue\n            for e in ds[\"examples\"]:\n                n_rec += 1\n                cid = e.get(\"metadata_openalex_id\")\n                if cid in ids:\n                    seen[cid] = e.get(\"metadata_level\")\n        del d\n    for cid, lv in seen.items():\n        if cid in lev and lv is not None and int(lv) == int(lev[cid]):\n            level_ok += 1\n    cov = cv.assign(found=cv.concept_id.isin(seen))\n    return {\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\",\n            \"n_recognition_rows\": n_rec, \"n_analysed\": int(len(ids)), \"n_found\": int(len(seen)),\n            \"coverage_by_body\": cov.groupby(\"body\").found.mean().round(4).to_dict(),\n            \"level_agreement\": level_ok / max(len(seen), 1)}\n\n\ndef exp12_crosscheck() -> dict:\n    \"\"\"EXP12 (art_uw4OeagJP3rv) open_features.parquet: cross-check of the home-build component values where it\n    overlaps (EXP5 frame). EXP12 used its own home-paper definition, so agreement is reported, not required.\"\"\"\n    from common import RUN_ROOT\n    p = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_12/open_features.parquet\"\n    if not p.exists():\n        return {\"available\": False}\n    o = pd.read_parquet(p)\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    m = cv[cv.frame == \"exp5\"].merge(o, on=\"ci\", suffixes=(\"\", \"_e12\"))\n    out = {\"available\": True, \"n_overlap\": int(len(m))}\n    for k in (\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"):\n        a, b = m[f\"{k}__raw\"].to_numpy(float), m[f\"{k}_home\"].to_numpy(float)\n        ok = np.isfinite(a) & np.isfinite(b)\n        out[k] = {\"n_both_finite\": int(ok.sum()), \"share_equal_1e9\": float(np.mean(np.abs(a[ok] - b[ok]) <= 1e-9)),\n                  \"spearman\": float(stats.spearmanr(a[ok], b[ok])[0]) if ok.sum() > 10 else None}\n    return out\n\n\ndef build_outputs() -> None:\n    from tables import load_tables\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    pm = spec[\"exp10_prediction_models\"][\"B5\"]\n    V = json.loads((RES / \"clean_vs_raw_psp.json\").read_text())\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    pw = json.loads((RES / \"power_frame_n.json\").read_text())\n    sz = json.loads((RES / \"size_dependence.json\").read_text())\n    T = load_tables()[\"POOLED\"]\n    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)\n    Zb = np.column_stack([(T[c].to_numpy(float) - pm[\"mu\"][c]) / pm[\"sd\"][c] for c in B5])\n    dev = (T.body == \"DEV\").to_numpy() & np.all(np.isfinite(Zb), 1)\n    y = T.O2r_m50.to_numpy(float)\n    preds, imputed, coefs = {}, {}, {}\n    for nm, x in PRED_X.items():\n        X = Zb.copy()\n        if x is not None:\n            v = T[x].to_numpy(float)\n            med = float(np.nanmedian(v[dev]))\n            imputed[nm] = ~np.isfinite(v)\n            v = np.where(np.isfinite(v), v, med)\n            X = np.c_[X, v]\n        A = np.c_[np.ones(len(T)), X]\n        okf = dev & np.all(np.isfinite(A), 1)\n        b = np.linalg.lstsq(A[okf], y[okf], rcond=None)[0]\n        coefs[nm] = b.tolist()\n        preds[nm] = A @ b\n    chk = {\"note\": \"OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)\", \"coef\": coefs}\n    for body in (\"OLDHO\", \"COH1014\", \"COH1517\"):\n        m = (T.body == body).to_numpy()\n        ent = {}\n        for nm, p in preds.items():\n            ok = m & np.isfinite(p)\n            ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > 20 else None\n        ent[\"n\"] = int(m.sum())\n        ent[\"gain_vs_B5\"] = {nm: (ent[nm] - ent[\"B5\"]) if ent[nm] is not None and ent[\"B5\"] is not None else None\n                             for nm in PRED_X if nm != \"B5\"}\n        chk[body] = ent\n    jdump(chk, RES / \"prediction_check.json\")\n    exs = []\n    for i, r in T.iterrows():\n        inp = {\"concept_id\": str(r.concept_id), \"name\": str(r[\"name\"]), \"body\": r.body, \"t0\": int(r.t0),\n               \"n_home_early\": int(r.n_home_early)}\n        for c in INPUT_COLS:\n            v = r[c]\n            inp[c] = None if not np.isfinite(v) else round(float(v), 6)\n        e = {\"input\": json.dumps(inp), \"output\": f\"{r.O2r_m50:.6f}\"}\n        for nm, p in preds.items():\n            e[f\"predict_{nm}\"] = f\"{p[i]:.6f}\" if np.isfinite(p[i]) else \"nan\"\n        e[\"metadata_body\"] = r.body\n        e[\"metadata_agroup\"] = r.agroup\n        e[\"metadata_O2r_resid\"] = None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)\n        e[\"metadata_imputed_variants\"] = [nm for nm in imputed if imputed[nm][i]]\n        e[\"metadata_missing_clean_variants\"] = [c for c in (\"NOVCHURN_exc\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\",\n                                                            \"OPEN_home_clean\") if not np.isfinite(r[c])]\n        exs.append(e)\n    vd = V[\"verdict\"]\n    head = {h[\"variant\"]: {b: h[b].get(\"psp\") for b in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\")}\n            for h in V[\"headline_R2_O2r_m50\"]}\n    meta = {\"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled \"\n                           \"variants)\",\n            \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n            \"verdict\": vd[\"verdict\"], \"DEGREE_ARTEFACT_PERSISTENCE\": vd[\"DEGREE_ARTEFACT_PERSISTENCE\"],\n            \"predictions_P1_P3\": {k: v[\"holds\"] for k, v in V[\"predictions\"].items()},\n            \"P_detail\": V[\"predictions\"], \"headline_psp_R2_O2r_m50\": head,\n            \"reliability_pooled_SB\": {k: v[\"pooled\"][\"SB\"] for k, v in rel[\"variants\"].items()},\n            \"outcome_reliability_SB\": rel[\"outcome\"][\"O2r_m50\"][\"pooled\"][\"SB\"],\n            \"thin_sample_share_R2\": sz[\"thin_sample_share\"][\"POOLED\"][\"R2\"],\n            \"power_plain_language\": pw[\"plain_language\"],\n            \"concept_key_check\": concept_key_check(), \"exp12_home_crosscheck\": exp12_crosscheck(),\n            \"n_examples\": len(exs), \"prediction_models\": \"OLS on DEV (B5 standardised with EXP10 frozen mu/sd); \"\n                                                         \"NaN variants imputed with the DEV median (flagged)\"}\n    out = {\"metadata\": meta, \"datasets\": [{\"dataset\": \"selection_concepts\", \"examples\": exs}]}\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)\n                                                     and not math.isfinite(o) else str(o)))\n    logger.info(f\"method_out.json: {len(exs)} examples; verdict {vd['verdict']}\")\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    setup_logger(\"method\")\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--run-all\", action=\"store_true\")\n    ap.add_argument(\"--force\", action=\"store_true\")\n    a = ap.parse_args()\n    if a.run_all:\n        run_stages(a.force)\n    build_outputs()\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"churn-thin-sample-check\"\nversion = \"0.1.0\"\ndescription = \"Is home-neighbourhood churn real or thin-sample noise? Raw vs noise-controlled ego-network variants\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"igraph==1.0.0\",\n  \"interface-meta==2.0.1\",\n  \"kiwisolver==1.5.1\",\n  \"llvmlite==0.49.0\",\n  \"loguru==0.7.3\",\n  \"matplotlib==3.11.2\",\n  \"narwhals==2.26.0\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"patsy==1.0.3\",\n  \"pillow==12.3.0\",\n  \"psutil==7.2.2\",\n  \"pyarrow==25.0.1\",\n  \"pyparsing==3.3.3\",\n  \"python-dateutil==2.9.0.post0\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"snowballstemmer==3.1.1\",\n  \"statsmodels==0.15.0\",\n  \"texttable==1.7.0\",\n  \"typing-extensions==4.16.0\",\n  \"wrapt==2.5.0\",\n]\n{\n  \"metadata\": {\n    \"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled variants)\",\n    \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n    \"verdict\": \"PARTLY_THIN\",\n    \"DEGREE_ARTEFACT_PERSISTENCE\": false,\n    \"predictions_P1_P3\": {\n      \"P1\": false,\n      \"P2\": true,\n      \"P3\": true\n    },\n    \"P_detail\": {\n      \"P1\": {\n        \"holds\": false,\n        \"per_body\": {\n          \"COH1517\": false,\n          \"OLDHO\": false\n        },\n        \"rule\": \"psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, COH1517 AND OLDHO\",\n        \"detail\": {\n          \"COH1517\": {\n            \"ratio\": 0.39594449273340393,\n            \"ratio_ci\": [\n              -0.26906748871819375,\n              0.8842632275100695\n            ],\n            \"psp_exc\": 0.06317913710216283,\n            \"psp_raw_same_sample\": 0.15956564180500524,\n            \"n\": 490\n          },\n          \"OLDHO\": {\n            \"ratio\": 0.046849438574826936,\n            \"ratio_ci\": [\n              -0.5585492463643292,\n              0.44451008406689974\n            ],\n            \"psp_exc\": 0.00558634333483666,\n            \"psp_raw_same_sample\": 0.1192403474785353,\n            \"n\": 1321\n          }\n        }\n      },\n      \"P2\": {\n        \"holds\": true,\n        \"psp\": -0.11558300476164542,\n        \"ci\": [\n          -0.14529406903883194,\n          -0.08637301651544306\n        ],\n        \"n\": 4262\n      },\n      \"P3\": {\n        \"holds\": true,\n        \"spearman_NOVCHURN_exc_log_n_all\": 0.033912654545104295,\n        \"ci\": [\n          0.015390987055309715,\n          0.05379348390665524\n        ],\n        \"n\": 9945,\n        \"spearman_on_analysis_sample\": 0.025460592516112258,\n        \"n_analysis\": 6203\n      }\n    },\n    \"headline_psp_R2_O2r_m50\": {\n      \"NOVCHURN_raw\": {\n        \"DEV\": 0.11582989542542993,\n        \"OLDHO\": 0.11299617572105293,\n        \"COH1014\": 0.11291907864162055,\n        \"COH1517\": 0.16119061802773654,\n        \"POOLED\": 0.11623313287281345\n      },\n      \"NOVCHURN_exc\": {\n        \"DEV\": 0.008098203486714372,\n        \"OLDHO\": 0.00558634333483666,\n        \"COH1014\": -0.006870368459004022,\n        \"COH1517\": 0.06317913710216283,\n        \"POOLED\": 0.007587062448167491\n      },\n      \"NOVCHURN_zperm\": {\n        \"DEV\": 0.006916483037342574,\n        \"OLDHO\": 0.021111779061880425,\n        \"COH1014\": -0.003119936374835825,\n        \"COH1517\": 0.07310759071781775,\n        \"POOLED\": 0.01180160291013356\n      },\n      \"NOVCHURN_rare5\": {\n        \"DEV\": 0.12745259057751135,\n        \"OLDHO\": 0.13960059816790388,\n        \"COH1014\": 0.14930816562962054,\n        \"COH1517\": 0.10532291566998955,\n        \"POOLED\": 0.12996354052682005\n      },\n      \"NOVCHURN_rare10\": {\n        \"DEV\": 0.06569371381097262,\n        \"OLDHO\": 0.04379950262510909,\n        \"COH1014\": 0.07637129759177229,\n        \"COH1517\": 0.17575151285385798,\n        \"POOLED\": 0.07816923082828127\n      },\n      \"NOVCHURN_cfg\": {", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 11:43:14 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 && cat lib/tables.py && sed -n 1,80p lib/common.py && ls -la results data && cat reproducibility.md | head -60
```

### [12] TOOL RESULT — Bash · 2026-09-29 11:43:16 UTC

````
{"stdout": "\"\"\"Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.\nSelection data, outcomes previously unsealed by EXP5/EXP8/EXP10.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN\nfrom ladder import rung_design\n\nCOV = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\", \"type\", \"generic\", \"level\",\n       \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\", \"newborn\", \"t0\", \"agroup\", \"label_coverage_early\",\n       \"home_coverage_early\", \"n_all_early\", \"O2r_m50\", \"O2r_resid\"]\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"]\n\n\ndef load_tables() -> dict[str, pd.DataFrame]:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    cv = cv.drop(columns=[c for c in (\"t0\",) if c in cv.columns])\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\"] + COV)\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\"] + COV + [\"window_flag\"])\n    cv = cv.drop(columns=[c for c in (\"agroup\",) if c in cv.columns])\n    e = cv[cv.frame == \"exp5\"].merge(fe, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    e[\"window_flag\"] = 0\n    c = cv[cv.frame == \"cohort\"].merge(ac, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    pooled = pd.concat([e, c], ignore_index=True)\n    pooled[\"window_flag\"] = pooled.window_flag.fillna(0).astype(int)\n    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}\n    out[\"POOLED\"] = pooled\n    return out\n\n\ndef design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:\n    Bc, Cc = rung_design(df, rung, drop_group=drop_group)\n    if pooled and df.body.nunique() > 1:\n        bs = sorted(df.body.unique())[1:]\n        Cc = pd.concat([Cc, pd.DataFrame({f\"body_{b}\": (df.body == b).astype(float) for b in bs}, index=df.index)],\n                       axis=1)\n        Cc = Cc.loc[:, Cc.std() > 0]\n    return Bc.to_numpy(float), Cc.to_numpy(float)\n\"\"\"Shared constants, paths and small helpers for the RQ1 held-out pipeline.\n\nThe title analyser / surface normaliser / matcher are imported from common5.py (EXP5's common.py, copied verbatim)\nso the matching is byte-identical to the EXP5 scan that defined the frame.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\n\nLIB = Path(__file__).resolve().parent\nROOT = LIB.parent\nsys.path.insert(0, str(LIB))\n\nDATA = ROOT / \"data\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nMODELS = ROOT / \"models\"\nPASSA = ROOT / \"passA\" / \"parts\"\nPASSB = ROOT / \"passB\" / \"parts\"\nfor _d in (DATA, RES, LOGS, FIGS, MODELS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nRUN_ROOT = Path(os.environ.get(\"AII_RUN_ROOT\", str(ROOT.parents[3])))\nEXP5 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_5\"\nEXP3 = RUN_ROOT / \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\"\nEXP8 = RUN_ROOT / \"3_invention_loop/iter_3/gen_art/gen_art_experiment_8\"\n# EXP16 patch: inputs and data are read (read-only) from EXP10; everything written stays under ROOT\nSRC10 = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_10\"\nINPUTS = SRC10 / \"inputs\"\nDATA_IN = SRC10 / \"data\"\nEXP6 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"\nEVAL1 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_evaluation_1\"\nO5DIR = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nMATCH_Y0, MATCH_Y1 = 2000, 2016      # t0 in 2003..2014 -> feature windows t0-3..t0+2 lie in 2000..2016\nTAG_MIN = 0.3\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nUNITS = HELD_GROUPS + [\"COH_DEVHOME\", \"COH_OTHER\"]\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef mix64(x: np.ndarray) -> np.ndarray:\n    \"\"\"splitmix64 finaliser (identical to EXP5 scan_full.mix64).\"\"\"\n    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)\n    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)\n    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)\n    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)\n\n\ndef works_files() -> list[tuple[int, str, int, int]]:\n    man = json.loads((ROOT / \"snapshot/works_manifest.json\").read_text())\n    return [(i, f[\"url\"].replace(\"s3://openalex/\", \"\"), f[\"meta\"][\"content_length\"], f[\"meta\"][\"record_count\"])\n            for i, f in enumerate(man[\"files\"])]\n\n\ndef source_field_lut() -> tuple[np.ndarray, np.ndarray]:\ndata:\ntotal 19996\ndrwxrwxrwx  3 root root 2025210 Sep 29 09:02 .\ndrwxrwxrwx 10 root root 2027924 Sep 29 09:02 ..\n-rw-rw-rw-  1 root root 4634477 Sep 29 05:47 clean_variants.parquet\n-rw-rw-rw-  1 root root 3595049 Sep 29 06:15 psp_boot.npz\ndrwxrwxrwx  2 root root 2023837 Sep 29 05:34 s2_parts_full\n-rw-rw-rw-  1 root root 2834797 Sep 29 05:34 s2_scalars_full.parquet\n-rw-rw-rw-  1 root root  488773 Sep 29 05:46 v3_nulls_full.parquet\n-rw-rw-rw-  1 root root 2844086 Sep 29 05:49 v4_half_means.npz\n\nresults:\ntotal 5344\ndrwxrwxrwx  2 root root 2000137 Sep 29 06:25 .\ndrwxrwxrwx 10 root root 2027924 Sep 29 09:02 ..\n-rw-rw-rw-  1 root root  693635 Sep 29 06:17 clean_vs_raw_psp.json\n-rw-rw-rw-  1 root root  514025 Sep 29 06:15 clean_vs_raw_psp_cells.json\n-rw-rw-rw-  1 root root    4140 Sep 29 06:23 deviations.json\n-rw-rw-rw-  1 root root    4134 Sep 29 05:47 frozen_constants_S1b.json\n-rw-rw-rw-  1 root root    9939 Sep 29 05:31 frozen_spec.json\n-rw-rw-rw-  1 root root    1615 Sep 29 05:25 gate_t0.json\n-rw-rw-rw-  1 root root    1272 Sep 29 06:25 headline_check.json\n-rw-rw-rw-  1 root root     879 Sep 29 06:19 placebo_calibration.json\n-rw-rw-rw-  1 root root     575 Sep 29 05:46 planted_checks.json\n-rw-rw-rw-  1 root root   20480 Sep 29 06:20 power_frame_n.json\n-rw-rw-rw-  1 root root    2933 Sep 29 06:21 prediction_check.json\n-rw-rw-rw-  1 root root    2144 Sep 29 06:18 rederive.json\n-rw-rw-rw-  1 root root   38862 Sep 29 05:52 reliability.json\n-rw-rw-rw-  1 root root   37658 Sep 29 05:49 reliability_x.json\n-rw-rw-rw-  1 root root  100198 Sep 29 05:50 size_dependence.json\n-rw-rw-rw-  1 root root    1371 Sep 29 06:22 unit_tests.json\n-rw-rw-rw-  1 root root    2038 Sep 29 05:29 unit_tests_fast6.json\n-rw-rw-rw-  1 root root     820 Sep 29 05:42 unit_tests_fastpsp.json\n-rw-rw-rw-  1 root root    1139 Sep 29 05:49 unit_tests_nulls.json\n-rw-rw-rw-  1 root root     852 Sep 29 05:46 v3_nulls_full.json\n# Reproducibility: \"Is neighbourhood churn real or thin-sample noise?\"\n\nThese are the exact steps that produced the results in this folder. Every path below is relative to this folder.\n\n## 1. Get the artifact\nThis folder is published as one folder of a public GitHub repository:\n```bash\ngit clone <repository-url>\ncd <repository>/<this-artifact-folder>      # the folder that contains method.py and this file\n```\n\n## 2. System, Python and libraries\n- Ubuntu or Debian (the run used Debian 12 in a Docker container), with no extra system packages.\n- Hardware: 4 vCPU (AMD EPYC 9655P), a 29 GB RAM cgroup limit, no GPU. Peak RAM was about 3 GB.\n- Python **3.12.14**. Environments are created with `uv`; the run never used pip.\n\n```bash\nuv venv .venv --python=3.12\nuv pip install --python .venv/bin/python -r <(python3 - <<'EOF'\nimport tomllib; print(\"\\n\".join(tomllib.load(open(\"pyproject.toml\",\"rb\"))[\"project\"][\"dependencies\"]))\nEOF\n)\n```\n\nThe exact versions installed are pinned in `pyproject.toml`: numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, igraph 1.0.0, numba 0.67.0, pyarrow 25.0.1, matplotlib 3.11.2, statsmodels 0.15.0, loguru 0.7.3, snowballstemmer 3.1.1, psutil 7.2.2, plus their dependencies. These are the same numpy, pandas, scipy and igraph versions EXP10 used.\n\nAlways run with `OMP_NUM_THREADS=1`. Multi-threaded BLAS inside process pools made `psp_point` 10-30× slower in this run.\n\n## 3. Inputs (no downloads, no API keys, $0 LLM spend)\nAll inputs are read, read-only, from earlier artifacts of the same run. The code resolves them through ONE root: the environment variable `AII_RUN_ROOT`. When it is unset, the root defaults to the folder three levels above this one (`lib/common.py`: `RUN_ROOT`). Under that root the code expects these sub-folders:\n\n| artifact id | expected relative location under `AII_RUN_ROOT` | what is read |\n|---|---|---|\n| art_NMe386dX9GLF (EXP10) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_10` | `inputs/` (topic backbone slices, topic meta, lexicon), `data/{ego_open_*, features_exp5_open, analysis_cohort, passC_early, passC_pre_agg, cohort_candidates.csv, bg_topics.npz, sealed/parts}`, `results/{frozen_spec, cohort_result}.json` |\n| art_dFQ6jbgNsR6Q (EXP8) | `3_invention_loop/iter_3/gen_art/gen_art_experiment_8` | `data/frame_matches_early/part_*.parquet` |\n| art_wxWssKSUR45f (EXP5) | `3_invention_loop/iter_2/gen_art/gen_art_experiment_5` | `frame_concepts.csv`, `scan/agg_counts.parquet` (outcome-window field counts) |\n| art_uw4OeagJP3rv (EXP12) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_12` | `open_features.parquet` (cross-check only) |\n| art_O7Dq4L02QnDN (dataset) | `3_invention_loop/iter_2/gen_art/gen_art_dataset_2` | `full_data_out/*.json` (concept key cross-check only) |\n\nIf your clone lays these artifacts out differently, create that directory tree with symlinks and `export AII_RUN_ROOT=<that dir>`.\n\nSome input files are 100 MB or larger (for example EXP5 `scan/agg_counts.parquet`), and the publisher does not push those. Rebuild them with the owning artifact's own `reproducibility.md`.\n\nNo user-uploaded material was used.\n\n## 4. Commands, in the order they were run\nEach stage writes its outputs and is skipped by `method.py --run-all` when the output exists. All seeds are fixed in `results/frozen_spec.json`.\n\n```bash\nexport OMP_NUM_THREADS=1\n.venv/bin/python s0_gate.py                  # ~40 s   gate T0 -> results/gate_t0.json (all diffs 0.0)\n.venv/bin/python tests/u_fast6.py 1000       # ~1 min  U1/U2/U5/U6 -> results/unit_tests_fast6.json\n.venv/bin/python s1_freeze.py                # seal 1 -> results/frozen_spec.json, logs/seal.log\n.venv/bin/python s2_variants.py --tag full --workers 4   # ~3 min, 13,444 concepts\n.venv/bin/python s3_nulls.py --tag full      # ~10 min (600 igraph rewires in 3 processes + numba curveball)\n.venv/bin/python tests/u_nulls.py            # ~3 min  U3 toy curveball, U4 rewire calibration\n.venv/bin/python tests/planted.py            # ~30 s   PC1, PC2\n.venv/bin/python s4_composites.py            # ~2 min  seal 2 (constants) + split-half reliability\n.venv/bin/python s4b_outcome_rel.py          # ~1 min  outcome reliability\n.venv/bin/python s5_size.py                  # ~5 s", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [13] TOOL CALL — Bash · 2026-09-29 11:43:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 && head -30 lib/ladder.py; python3 -c "import json;d=json.load(open('results/clean_vs_raw_psp.json'));print(list(d.keys()));print(json.dumps(d['verdict'])[:1500]);h=d['headline_R2_O2r_m50'];print(len(h), json.dumps(h[0])[:800])"; python3 -c "
import json
r=json.load(open('results/reliability.json'));print(list(r.keys()), list(r['variants'].keys()))
p=json.load(open('results/power_frame_n.json'));print(p['plain_language'])
s=json.load(open('results/size_dependence.json'));print(s['thin_sample_share']['POOLED'])
f=json.load(open('results/frozen_spec.json'));print(f['exp10_prediction_models']['B5'])
m=json.load(open('preview_method_out.json'))['metadata'];print(json.dumps(m['concept_key_check']));print(json.dumps(m['exp12_home_crosscheck']))
"
```

### [14] TOOL RESULT — Bash · 2026-09-29 11:43:30 UTC

```
{"stdout": "\"\"\"Ladder machinery: OPEN construction from frozen constants, rung design matrices, partial Spearman with a refit\nconcept bootstrap (EXP8 rq1stats.psp_point), DL pooling over groups, one-sided bootstrap p, Holm.\n\npsp = Pearson(resid(rank x | ranks of continuous covariates + dummies), resid(rank y | same)); the residualisation is\nrefitted in every bootstrap draw (ranks recomputed within the draw). Resampling unit: concept.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom rq1stats import dersimonian_laird, holm, psp_point\n\nCOMPONENTS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\nSIGNS = {\"new_edge_rate\": 1, \"n_comm_W3\": 1, \"participation\": 1, \"NOV_res\": 1, \"ego_density_W3\": -1,\n         \"edge_persistence\": -1}\nBUILDS = [\"home\", \"all\", \"sizematch\"]\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nFOOTPRINT = [\"fp_logN\", \"fp_nfields\"]\nFOOTPRINT_BIN = [\"fp_reemerge\", \"fp_wiki_pre\", \"newborn\"]\nCOVERAGE = [\"label_coverage_early\", \"home_coverage_early\"]\nANALYSIS_GROUP = {\"CS\": \"CS+Eng\", \"Eng\": \"CS+Eng\", \"BGM\": \"BGM+Med\", \"Med\": \"BGM+Med\", \"PHYS\": \"PHYS\",\n                  \"LIFEENV\": \"LIFEENV\", \"SOC\": \"SOC\", \"MATHDEC\": \"MATHDEC\"}\nPOOL_GROUPS = [\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\"]\nRUNGS = [\"R0\", \"R1\", \"R2\", \"R3\", \"R4\", \"R5\"]\nMIN_HOME_PAPERS = 10\n\n\n['label', 'B', 'seed', 'resampling_unit', 'groups', 'disattenuated', 'F6_contingency', 'predictions', 'verdict', 'holm', 'headline_R2_O2r_m50', 'cells', 'confounds_removed']\n{\"verdict\": \"PARTLY_THIN\", \"DEGREE_ARTEFACT_PERSISTENCE\": false, \"clauses\": {\"P1\": false, \"P3\": true, \"V1_keeps_ge_50pct_in_COH1517_or_OLDHO\": true, \"V1_retention\": {\"COH1517\": 0.7643013231828545, \"OLDHO\": 0.6362526801996564}, \"raw_NOVCHURN_ci_excludes_0\": {\"COH1517\": true, \"OLDHO\": true}, \"exc_and_rare_keep_lt_30pct\": {\"COH1517\": false, \"OLDHO\": false}, \"P2\": true, \"raw_edge_persistence_pooled_ci_lt0\": true}, \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\"}\n23 {\"variant\": \"NOVCHURN_raw\", \"DEV\": {\"psp\": 0.11582989542542993, \"ci\": [0.07645046097791196, 0.15251138320592492], \"n\": 2741}, \"OLDHO\": {\"psp\": 0.11299617572105293, \"ci\": [0.0608781889632089, 0.16301318924648014], \"n\": 1404}, \"COH1014\": {\"psp\": 0.11291907864162055, \"ci\": [0.06651637981915953, 0.1584739885511837], \"n\": 1799}, \"COH1517\": {\"psp\": 0.16119061802773654, \"ci\": [0.07066270969979721, 0.25172767820496067], \"n\": 506}, \"POOLED\": {\"psp\": 0.11623313287281345, \"ci\": [0.09133946495128593, 0.1399456352463288], \"n\": 6450}}\n['method', 'notes', 'variants', 'outcome'] ['new_edge_rate__raw', 'n_comm_W3__raw', 'participation__raw', 'NOV_res__raw', 'ego_density_W3__raw', 'edge_persistence__raw', 'NOVCHURN_raw', 'OPEN_home', 'NOV_res_exc', 'edge_persistence_exc', 'ego_density_W3_exc', 'new_edge_rate_exc', 'NOV_res_zperm', 'edge_persistence_zperm', 'ego_density_W3_zperm', 'NOV_res_rare5', 'edge_persistence_rare5', 'ego_density_W3_rare5', 'z_pers_cfg', 'z_dens_cfg', 'z_dens_k', 'edge_persistence_nullmean', 'NOVCHURN_exc', 'NOVCHURN_zperm', 'NOVCHURN_rare5', 'NOVCHURN_cfg', 'OPEN_home_clean', 'OPEN_home_exc']\nAt n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.\n{'R2': 0.6596194882526905, 'n': 12330, 'coef': [-0.0010767111256983803, 0.9746957571903339]}\n{'coef': [4.766039224098753, -0.05511164665586871, 0.008765664104716067, -0.42563667808882066, 1.6369692811444325, 0.2840929545239369], 'mu': {'logvol': 4.387217461299273, 'growth_c': 0.13591487868338373, 'offhome_share': 0.2628714872549475, 'entropy': 0.7831561038968538, 'reach': 3.228179741051028}, 'sd': {'logvol': 0.3554731095580416, 'growth_c': 0.43536192389233147, 'offhome_share': 0.19848326295216012, 'entropy': 0.4615603694432812, 'reach': 1.550401785313322}}\n{\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\", \"n_recognition_rows\": 65026, \"n_analysed\": 13444, \"n_found\": 13444, \"coverage_by_body\": {\"COH1014\": 1.0, \"COH1517\": 1.0, \"DEV\": 1.0, \"OLDHO\": 1.0}, \"level_agreement\": 1.0}\n{\"available\": true, \"n_overlap\": 12079, \"new_edge_rate\": {\"n_both_finite\": 12079, \"share_equal_1e9\": 1.0, \"spearman\": 1.0}, \"n_comm_W3\": {\"n_both_finite\": 12079, \"share_equal_1e9\": 1.0, \"spearman\": 0.9999999999999999}, \"participation\": {\"n_both_finite\": 8968, \"share_equal_1e9\": 1.0, \"spearman\": 0.9999999058066041}, \"NOV_res\": {\"n_both_finite\": 9475, \"share_equal_1e9\": 1.0, \"spearman\": 1.0}, \"ego_density_W3\": {\"n_both_finite\": 6810, \"share_equal_1e9\": 1.0, \"spearman\": 1.0}, \"edge_persistence\": {\"n_both_finite\": 11236, \"share_equal_1e9\": 1.0, \"spearman\": 1.0}}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-29 11:43:50 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad && cat > /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/make_mini_demo_data.py <<'EOF'
"""Build mini_demo_data.json: a stratified 100-concept slice of the EXP16 POOLED analysis table
(tables.load_tables()["POOLED"], finite O2r_m50) plus the small summary results that method.py's
build_outputs() reads. Run from anywhere; SRC points at the (read-only) experiment artifact."""
import json, math, sys
from pathlib import Path
import numpy as np

SRC = Path(sys.argv[1])
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"
sys.path.insert(0, str(SRC / "lib"))
from tables import load_tables  # noqa: E402

B5 = ["logvol", "growth_c", "offhome_share", "entropy", "reach"]
INPUT_COLS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
              "participation__raw", "NOVCHURN_raw", "OPEN_home", "NOV_res_rare10", "edge_persistence_rare10",
              "NOVCHURN_rare10", "NOV_res_rare5", "edge_persistence_rare5", "NOVCHURN_rare5", "NOV_res_exc",
              "edge_persistence_exc", "edge_persistence_nullmean", "NOVCHURN_exc", "EP_chao", "NOVCHURN_chao",
              "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean",
              "OPEN_home_exc"]
PER_BODY = {"DEV": 34, "OLDHO": 22, "COH1014": 22, "COH1517": 22}

T = load_tables()["POOLED"]
T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
rng = np.random.default_rng(20260928)
parts = []
for b, k in PER_BODY.items():
    sub = T[T.body == b]
    # prefer concepts with all B5 covariates finite (needed for the DEV OLS fit)
    sub = sub[np.all(np.isfinite(sub[B5].to_numpy(float)), 1)]
    parts.append(sub.iloc[np.sort(rng.choice(len(sub), size=k, replace=False))])
import pandas as pd
S = pd.concat(parts, ignore_index=True)

def f(v):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return None
    return round(v, 6) if math.isfinite(v) else None

rows = []
for _, r in S.iterrows():
    d = {"concept_id": str(r.concept_id), "name": str(r["name"]), "body": r.body, "agroup": r.agroup,
         "t0": int(r.t0), "n_home_early": int(r.n_home_early), "O2r_m50": f(r.O2r_m50), "O2r_resid": f(r.O2r_resid)}
    for c in B5 + INPUT_COLS:
        d[c] = f(r[c])
    rows.append(d)

R = SRC / "results"
spec = json.loads((R / "frozen_spec.json").read_text())
V = json.loads((R / "clean_vs_raw_psp.json").read_text())
rel = json.loads((R / "reliability.json").read_text())
pw = json.loads((R / "power_frame_n.json").read_text())
sz = json.loads((R / "size_dependence.json").read_text())
meta = json.loads((SRC / "preview_method_out.json").read_text())["metadata"]
V_small = {"verdict": V["verdict"], "predictions": V["predictions"],
           "headline_R2_O2r_m50": [{k: ({"psp": h[k]["psp"], "ci": h[k].get("ci"), "n": h[k].get("n")}
                                        if isinstance(h[k], dict) else h[k]) for k in h}
                                   for h in V["headline_R2_O2r_m50"]]}
rel_small = {"variants": {k: {"pooled": {"SB": v["pooled"]["SB"]}} for k, v in rel["variants"].items()},
             "outcome": {"O2r_m50": {"pooled": {"SB": rel["outcome"]["O2r_m50"]["pooled"]["SB"]}}}}
out = {
    "description": "EXP16 thin-sample churn check: 100-concept stratified slice of the POOLED analysis table "
                   "(34 DEV + 22 each OLDHO/COH1014/COH1517, finite O2r_m50 and B5) plus the small full-run summary "
                   "results that method.py build_outputs() reads.",
    "concepts": rows,
    "frozen_spec": {"exp10_prediction_models": {"B5": spec["exp10_prediction_models"]["B5"]}},
    "clean_vs_raw_psp": V_small,
    "reliability": rel_small,
    "power_frame_n": {"plain_language": pw["plain_language"]},
    "size_dependence": {"thin_sample_share": {"POOLED": sz["thin_sample_share"]["POOLED"]}},
    "precomputed_crosschecks": {"concept_key_check": meta["concept_key_check"],
                                "exp12_home_crosscheck": meta["exp12_home_crosscheck"]},
    "full_run_n_examples": meta["n_examples"],
}
OUT.write_text(json.dumps(out, indent=1))
print(OUT, len(rows), S.body.value_counts().to_dict())
EOF
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv run --no-project --python 3.12 --with pandas --with pyarrow --with numpy --with scipy python make_mini_demo_data.py /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16 2>&1 | tail -20; ls -la mini_demo_data.json
```

### [16] TOOL RESULT — Bash · 2026-09-29 11:43:54 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z/mini_demo_data.json 100 {'DEV': 34, 'OLDHO': 22, 'COH1014': 22, 'COH1517': 22}\n-rw-rw-rw- 1 root root 138245 Sep 29 11:43 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] ASSISTANT · 2026-09-29 11:45:10 UTC

```
I built `mini_demo_data.json`: 100 concepts sampled across the four bodies, plus the summary results. Next I'm writing the notebook.
```

### [18] TOOL CALL — Bash · 2026-09-29 11:45:10 UTC

```
cat > /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad/mk_nb.py <<'PYEOF'
import json
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": s.strip("\n")})

md(r'''
# Is research-topic churn real or small-sample noise? (EXP16 demo)

This notebook is a runnable walkthrough of **`method.py`**, the final stage of experiment 16. The experiment asks whether the *home-only neighbourhood churn/novelty* signal is real. That signal is the finding that concepts whose early co-occurrence neighbourhood keeps changing (new partners, low edge persistence) later diffuse more broadly. The alternative is that the signal is a **thin-sample artefact**: with about 10 home papers per year, a concept's neighbourhood looks unstable simply because it was sampled sparsely.

The full pipeline (`s0_gate.py … s8_power.py`) ran on **13,444 selection concepts** from OpenAlex. It computed raw ego-network indicators and several noise-controlled variants:
* **V1**: fixed-n rarefaction (`*_rare5`, `*_rare10`)
* **V2**: within-concept year-permutation null, reported as excess over the null (`*_exc`), plus Chao-2005 Jaccard (`EP_chao`)
* **V3**: configuration / curveball nulls (`z_dens_cfg`, `z_pers_cfg`, `NOVCHURN_cfg`)
* **V4**: split-half reliability

Each variant was then related to the outcome `O2r_m50` (later broad diffusion) with partial Spearman correlations conditioned on the baseline covariates **B5** (`logvol`, `growth_c`, `offhome_share`, `entropy`, `reach`).

`method.py` itself does three things, all reproduced here:
1. Fit **OLS on the DEV body only**, using the B5 covariates standardised with the frozen EXP10 constants, with and without each churn variant. It then applies these models to every body and checks out-of-DEV Spearman with the outcome (`prediction_check.json`).
2. Build one `exp_gen_sol_out` example per concept (`input` = indicator values, `output` = `O2r_m50`, `predict_*` = model predictions).
3. Collect the headline verdict metadata (psp table, P1–P3, reliability, power, thin-sample share).

**Demo scale:** the demo uses a stratified **100-concept slice** of the full 7,748-concept analysis table: 34 DEV, and 22 each from OLDHO, COH1014 and COH1517. The expensive upstream stages (null models, bootstraps, cross-checks against dependency artifacts over 100 MB) are loaded as their precomputed full-run results. Code cells copy `method.py` as closely as possible.
''')

code(r'''
import subprocess, sys
def _pip(*a): subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *a])

# loguru — NOT on Colab, always install (method.py uses it for logging)
_pip('loguru==0.7.3')

# numpy, pandas, scipy, matplotlib — pre-installed on Colab, install locally only (Colab's exact versions)
if 'google.colab' not in sys.modules:
    _pip('numpy==2.0.2', 'pandas==2.2.2', 'scipy==1.16.3', 'matplotlib==3.10.0')
''')

md(r'''
## Imports
This is the original import block of `method.py`. The `argparse`, `subprocess` and `lib/` path imports were only used for the CLI and the stage runner, so they are kept but not needed here. `common.jdump` / `setup_logger` come from the artifact's `lib/`, so the notebook defines two tiny stand-ins below. `matplotlib` is added for the final plots.
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

import matplotlib.pyplot as plt

# --- notebook stand-ins for lib/common.py helpers (jdump, setup_logger) ---
RES = Path("demo_results"); RES.mkdir(exist_ok=True)
def jdump(obj, path):
    Path(path).write_text(json.dumps(obj, indent=1, default=lambda o: None if isinstance(o, float) and not math.isfinite(o) else str(o)))
def setup_logger(name):
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    return logger
''')

md("## Data loading\n`mini_demo_data.json` is fetched from the GitHub repository. If that fails, the notebook falls back to a local copy.")

code(r'''
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-16/demo/mini_demo_data.json"
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
print(data["description"])
print("concepts in demo slice:", len(data["concepts"]), "| full-run examples:", data["full_run_n_examples"])
''')

md(r'''
## Configuration
This cell holds the model/column constants from `method.py` and the few tunable knobs.
* `MAX_CONCEPTS`: how many concepts of the demo slice to use. The demo uses all 100; the full run used 7,748 with finite `O2r_m50`.
* `MIN_BODY_N`: the minimum per-body sample size before a Spearman is reported. The original is `ok.sum() > 20`.
* `EVAL_BODIES`: the held-out bodies that the DEV-fitted models are applied to.

`method.py` has no iterations or bootstraps of its own. The B = 2000 bootstraps and 200 null draws belong to the upstream stages, whose results are loaded precomputed.
''')

code(r'''
MAX_CONCEPTS = 100            # demo slice size (full run: 7748 concepts with finite O2r_m50)
MIN_BODY_N = 20               # original: Spearman reported only if ok.sum() > 20
EVAL_BODIES = ("OLDHO", "COH1014", "COH1517")

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
## Upstream stages (not re-run here)
In the original, `run_stages()` runs 14 scripts in order: the gate, the fast engine, the seal, variants, nulls, composites, reliability, size, association, verdict, power and rederive. Each one is skipped if its output exists. These stages need the OpenAlex-derived ego networks from earlier artifacts and take about 30 minutes on 4 CPUs, so this demo does **not** call `run_stages`. The function is kept for reference.
''')

code(r'''
STAGES = [("s0_gate.py", "gate_t0.json"), ("tests/u_fast6.py", "unit_tests_fast6.json"),
          ("s1_freeze.py", "frozen_spec.json"), ("s2_variants.py", "s2_scalars_full.parquet"),
          ("s3_nulls.py", "v3_nulls_full.parquet"), ("tests/u_nulls.py", "unit_tests_nulls.json"),
          ("tests/planted.py", "planted_checks.json"), ("s4_composites.py", "clean_variants.parquet"),
          ("s4b_outcome_rel.py", "reliability.json"), ("s5_size.py", "size_dependence.json"),
          ("s6_assoc.py", "clean_vs_raw_psp_cells.json"), ("s7_verdict.py", "clean_vs_raw_psp.json"),
          ("s8_power.py", "power_frame_n.json"), ("rederive.py", "rederive.json")]


def run_stages(force: bool) -> None:   # original orchestrator (NOT called in the demo)
    for script, out in STAGES:
        out = RES / out
        if out.exists() and not force:
            logger.info(f"skip {script} ({out.name} exists)")
            continue
        if script == "s1_freeze.py" and out.exists():
            logger.warning("frozen_spec.json exists: never re-freeze (seal)")
            continue
        logger.info(f"running {script}")
        subprocess.run([sys.executable, script], check=True)

print("stages (precomputed in the full run):", [s for s, _ in STAGES])
''')

md(r'''
## Dependency cross-checks
`concept_key_check()` checks that every analysed concept id appears in the OpenAlex concept-recognition table of the dataset artifact art_O7Dq4L02QnDN, and that its level agrees. `exp12_crosscheck()` checks that the home-build component values match EXP12's `open_features.parquet`. Both read dependency files over 100 MB, so the notebook versions return the stored full-run results. The originals found 100% coverage, 100% level agreement, and component values identical to 1e-9.
''')

code(r'''
def concept_key_check() -> dict:
    """Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its
    concept_recognition table and agreement of the OpenAlex level. (Demo: precomputed full-run result.)"""
    return data["precomputed_crosschecks"]["concept_key_check"]


def exp12_crosscheck() -> dict:
    """EXP12 (art_uw4OeagJP3rv) open_features.parquet: cross-check of the home-build component values where it
    overlaps (EXP5 frame). (Demo: precomputed full-run result.)"""
    return data["precomputed_crosschecks"]["exp12_home_crosscheck"]

print(json.dumps(concept_key_check(), indent=1))
''')

md(r'''
## Load the analysis table and the stage results
In `build_outputs()`, the first lines read the frozen spec, which holds the EXP10 B5 standardisation constants `mu`/`sd`. They also read the verdict file (`clean_vs_raw_psp.json`), the reliability, power and size-dependence results, and the POOLED analysis table from `tables.load_tables()`. The table has one row per concept, with its body, the B5 covariates, all raw and clean churn variants, and the outcome `O2r_m50`. Here all of these come from `data`.
''')

code(r'''
spec = data["frozen_spec"]
pm = spec["exp10_prediction_models"]["B5"]
V = data["clean_vs_raw_psp"]
rel = data["reliability"]
pw = data["power_frame_n"]
sz = data["size_dependence"]
T = pd.DataFrame(data["concepts"]).head(MAX_CONCEPTS)                 # was: load_tables()["POOLED"]
T = T.apply(lambda s: pd.to_numeric(s) if s.name in B5 + INPUT_COLS + ["O2r_m50", "O2r_resid"] else s)
T[B5 + INPUT_COLS + ["O2r_m50", "O2r_resid"]] = T[B5 + INPUT_COLS + ["O2r_m50", "O2r_resid"]].astype(float)
T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
print(T.body.value_counts().to_dict())
T[["concept_id", "name", "body", "n_home_early", "NOVCHURN_raw", "NOVCHURN_exc", "OPEN_home", "O2r_m50"]].head(8)
''')

md(r'''
## DEV-only OLS prediction models
The B5 covariates are standardised with the **frozen** EXP10 `mu`/`sd`, so nothing is re-estimated on the evaluation data. For each model in `PRED_X`, an OLS is fitted on **DEV concepts only**, either B5 alone or B5 plus one churn variant. A missing variant value is imputed with the DEV median, and the imputation is flagged. The coefficients are then applied to every concept.
''')

code(r'''
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
print("DEV concepts used for the fit:", int(dev.sum()))
pd.DataFrame({nm: np.round(c, 4) for nm, c in coefs.items()}.items(), columns=["model", "coef (intercept, B5..., variant)"])
''')

md(r'''
## Out-of-DEV check (`prediction_check.json`)
For each held-out body, compute the Spearman correlation between every model's prediction and the outcome, and the **gain over B5**. In the full run this gain is about 0. The churn variants add little *predictive* signal beyond the B5 baseline, even though some of them have non-zero partial correlations.
''')

code(r'''
chk = {"note": "OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)", "coef": coefs}
for body in EVAL_BODIES:
    m = (T.body == body).to_numpy()
    ent = {}
    for nm, p in preds.items():
        ok = m & np.isfinite(p)
        ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > MIN_BODY_N else None
    ent["n"] = int(m.sum())
    ent["gain_vs_B5"] = {nm: (ent[nm] - ent["B5"]) if ent[nm] is not None and ent["B5"] is not None else None
                         for nm in PRED_X if nm != "B5"}
    chk[body] = ent
jdump(chk, RES / "prediction_check.json")
pd.DataFrame({b: {nm: chk[b][nm] for nm in PRED_X} for b in EVAL_BODIES}).round(3)
''')

md(r'''
## Build `method_out.json` (`exp_gen_sol_out` format)
This step writes one example per concept: `input` is a JSON string with the concept id, body, `t0`, `n_home_early` and all 27 indicator variants; `output` is `O2r_m50`; each `predict_*` field holds a model prediction. Metadata records the body, the analysis group, the residualised outcome, and which clean variants are missing or imputed.
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
print(len(exs), "examples; first:")
print(json.dumps(exs[0], indent=1)[:900])
''')

md(r'''
## Verdict metadata
This step collects the full-run headline results: the mechanical verdict (`PARTLY_THIN`), predictions P1–P3, and the partial-Spearman (psp) table of each variant with `O2r_m50 | B5 + R2` per body. It also gathers the split-half reliabilities, the thin-sample share, and the power statement. Then it writes the demo's `method_out.json`.
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
Path("method_out.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)
                                              and not math.isfinite(o) else str(o)))
setup_logger("method")
logger.info(f"method_out.json: {len(exs)} examples; verdict {vd['verdict']}")
''')

md(r'''
## Results and visualisation
**Left panel:** the full-run pooled partial Spearman (with 95% bootstrap CI) of the raw churn composite and its noise-controlled variants. Most of the raw signal disappears under the V2 permutation-excess variant, and about 70% survives fixed-n rarefaction. **Middle panel:** in the demo slice, raw edge persistence and its V2 null mean against `log n_home_early`. The null mean follows the sample size, which is the thin-sample share. **Right panel:** out-of-DEV Spearman for each model on the demo slice. With only 22 concepts per body these values are noisy; the full-run values are in the artifact's `results/prediction_check.json`.
''')

code(r'''
print(f"VERDICT: {meta['verdict']} | P1-P3: {meta['predictions_P1_P3']} | thin-sample share R2 = {meta['thin_sample_share_R2']:.2f}")
print(f"Outcome reliability SB = {meta['outcome_reliability_SB']:.3f}")
show = ["NOVCHURN_raw", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_chao", "NOVCHURN_cfg", "NOVCHURN_exc",
        "NOVCHURN_zperm", "OPEN_home", "OPEN_home_clean", "z_dens_cfg", "z_pers_cfg"]
H = {h["variant"]: h for h in V["headline_R2_O2r_m50"]}
show = [s for s in show if s in H]
tab = pd.DataFrame({s: {**{b: H[s][b]["psp"] for b in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED")},
                        "SB_pooled": meta["reliability_pooled_SB"].get(s)} for s in show}).T
print("\nFull-run partial Spearman with O2r_m50 | B5+R2 (B=2000):")
print(tab.round(3).to_string())

fig, ax = plt.subplots(1, 3, figsize=(17, 5))
ps = [H[s]["POOLED"]["psp"] for s in show]
lo = [H[s]["POOLED"]["psp"] - H[s]["POOLED"]["ci"][0] for s in show]
hi = [H[s]["POOLED"]["ci"][1] - H[s]["POOLED"]["psp"] for s in show]
ax[0].barh(show[::-1], ps[::-1], xerr=[lo[::-1], hi[::-1]], color=["#c44" if "raw" in s or s == "OPEN_home" else "#4a7" for s in show[::-1]])
ax[0].axvline(0, color="k", lw=0.8); ax[0].set_xlabel("pooled psp with O2r_m50 (full run, 95% CI)")
ax[0].set_title("Raw (red) vs noise-controlled (green)")

ln = np.log(T.n_home_early.astype(float))
ax[1].scatter(ln, T.edge_persistence__raw, s=18, label="raw edge persistence")
ax[1].scatter(ln, T.edge_persistence_nullmean, s=18, marker="x", label="V2 null mean")
ok = np.isfinite(T.edge_persistence__raw) & np.isfinite(T.edge_persistence_nullmean)
r_null = stats.spearmanr(T.edge_persistence__raw[ok], T.edge_persistence_nullmean[ok])[0]
ax[1].set_xlabel("log n_home_early"); ax[1].set_ylabel("edge persistence")
ax[1].set_title(f"Demo slice: raw vs its null mean (rho={r_null:.2f})"); ax[1].legend()

pc = pd.DataFrame({b: {nm: chk[b][nm] for nm in PRED_X} for b in EVAL_BODIES})
pc.plot.bar(ax=ax[2]); ax[2].set_ylabel("Spearman(pred, O2r_m50)")
ax[2].set_title(f"Demo slice: out-of-DEV prediction (n≈{chk['OLDHO']['n']}/body)")
ax[2].tick_params(axis="x", rotation=60)
plt.tight_layout(); plt.show()
''')

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python", "version": "3.12"}}, "nbformat": 4, "nbformat_minor": 5}
import sys
json.dump(nb, open(sys.argv[1], "w"), indent=1)
PYEOF
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z && python3 /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad/mk_nb.py code_demo.ipynb && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | tail -20
```

### [19] TOOL RESULT — Bash · 2026-09-29 11:45:34 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n/tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/lib/python3.12/site-packages/nbformat/validator.py:434: MissingIDFieldWarning: Cell is missing an id field, this will become a hard error in future nbformat versions. You may want to use `normalize()` on your notebooks before validations (available since nbformat 5.1.4). Previous versions of nbformat are fixing this issue transparently, and will stop doing so in the future.\n  _validate(nbdict, ref, version, version_minor, relax_add_props)\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 197753 bytes to code_demo.ipynb\n\nreal\t0m19.433s\nuser\t0m16.947s\nsys\t0m1.991s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] ASSISTANT · 2026-09-29 11:45:40 UTC

```
The notebook ran cleanly in 19 s. Next I'm checking the outputs.
```

### [21] TOOL CALL — Bash · 2026-09-29 11:45:40 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        t=o.get('text') or o.get('data',{}).get('text/plain') or ''
        if isinstance(t,list): t=''.join(t)
        if o['output_type']=='error': print('ERR',i,o['ename'])
        print(i, o['output_type'], t[:700] if 'image/png' not in o.get('data',{}) else '[IMAGE]'); 
" ; ls; cat .aii/* 2>/dev/null | head
```

### [22] TOOL RESULT — Bash · 2026-09-29 11:45:40 UTC

```
{"stdout": "6 stream EXP16 thin-sample churn check: 100-concept stratified slice of the POOLED analysis table (34 DEV + 22 each OLDHO/COH1014/COH1517, finite O2r_m50 and B5) plus the small full-run summary results that method.py build_outputs() reads.\nconcepts in demo slice: 100 | full-run examples: 7748\n\n10 stream stages (precomputed in the full run): ['s0_gate.py', 'tests/u_fast6.py', 's1_freeze.py', 's2_variants.py', 's3_nulls.py', 'tests/u_nulls.py', 'tests/planted.py', 's4_composites.py', 's4b_outcome_rel.py', 's5_size.py', 's6_assoc.py', 's7_verdict.py', 's8_power.py', 'rederive.py']\n\n12 stream {\n \"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\",\n \"n_recognition_rows\": 65026,\n \"n_analysed\": 13444,\n \"n_found\": 13444,\n \"coverage_by_body\": {\n  \"COH1014\": 1.0,\n  \"COH1517\": 1.0,\n  \"DEV\": 1.0,\n  \"OLDHO\": 1.0\n },\n \"level_agreement\": 1.0\n}\n\n14 stream {'DEV': 34, 'OLDHO': 22, 'COH1014': 22, 'COH1517': 22}\n\n14 execute_result    concept_id                       name body  n_home_early  NOVCHURN_raw  \\\n0  2776251621                  Acetonide  DEV           283     -1.226929   \n1  2778510232  High resolution manometry  DEV            96     -1.271196   \n2  2776433454                 Rimonabant  DEV           114     -0.116658   \n3  2780434240         Urban rail transit  DEV            85     -0.669253   \n4  2909437798      Transversus abdominis  DEV            87     -1.193110   \n5   184150571                       SGK1  DEV            61     -0.953710   \n6  2993319417                 Coal fired  DEV            68     -0.064206   \n7  2910678782     Postpartum haemorrhage  DEV            62     -0.377455   \n\n   NOV\n16 stream DEV concepts used for the fit: 34\n\n16 execute_result                      model                   coef (intercept, B5..., variant)\n0                       B5  [4.5946, -0.0869, 0.1978, -0.0605, 0.5595, 0.8...\n1     B5_plus_NOVCHURN_raw  [4.6301, 0.0684, 0.1818, -0.2364, 0.8781, 0.53...\n2     B5_plus_NOVCHURN_exc  [4.5916, -0.0361, 0.2381, -0.1295, 0.7096, 0.6...\n3     B5_plus_NOVCHURN_cfg  [4.6015, 0.0048, 0.1878, -0.1205, 0.6688, 0.69...\n4        B5_plus_OPEN_home  [4.5745, -0.0728, 0.1642, -0.0856, 0.6454, 0.7...\n5  B5_plus_OPEN_home_clean  [4.5657, -0.0459, 0.1622, -0.0889, 0.6485, 0.7...\n18 execute_result                          OLDHO  COH1014  COH1517\nB5                       0.616    0.632    0.329\nB5_plus_NOVCHURN_raw     0.650    0.680    0.362\nB5_plus_NOVCHURN_exc     0.530    0.557    0.298\nB5_plus_NOVCHURN_cfg     0.615    0.658    0.327\nB5_plus_OPEN_home        0.612    0.626    0.268\nB5_plus_OPEN_home_clean  0.635    0.652    0.282\n20 stream 100 examples; first:\n{\n \"input\": \"{\\\"concept_id\\\": \\\"2776251621\\\", \\\"name\\\": \\\"Acetonide\\\", \\\"body\\\": \\\"DEV\\\", \\\"t0\\\": 2003, \\\"n_home_early\\\": 283, \\\"NOV_res__raw\\\": -0.748178, \\\"edge_persistence__raw\\\": 0.422078, \\\"ego_density_W3__raw\\\": 0.787879, \\\"new_edge_rate__raw\\\": 0.866667, \\\"n_comm_W3__raw\\\": 4.0, \\\"participation__raw\\\": 0.507324, \\\"NOVCHURN_raw\\\": -1.226929, \\\"OPEN_home\\\": 0.506227, \\\"NOV_res_rare10\\\": -0.882794, \\\"edge_persistence_rare10\\\": 0.174167, \\\"NOVCHURN_rare10\\\": -0.767041, \\\"NOV_res_rare5\\\": null, \\\"edge_persistence_rare5\\\": 0.074324, \\\"NOVCHURN_rare5\\\": null, \\\"NOV_res_exc\\\": -0.095007, \\\"edge_persistence_exc\\\": -0.014901, \\\"edge_persistence_nullmean\\\": 0.436979, \\\"NOVCH\n22 stream 11:45:32|INFO   |method_out.json: 100 examples; verdict PARTLY_THIN\n\n24 stream VERDICT: PARTLY_THIN | P1-P3: {'P1': False, 'P2': True, 'P3': True} | thin-sample share R2 = 0.66\nOutcome reliability SB = 0.895\n\nFull-run partial Spearman with O2r_m50 | B5+R2 (B=2000):\n                   DEV  OLDHO  COH1014  COH1517  POOLED  SB_pooled\nNOVCHURN_raw     0.116  0.113    0.113    0.161   0.116      0.476\nNOVCHURN_rare5   0.127  0.140    0.149    0.105   0.130      0.359\nNOVCHURN_rare10  0.066  0.044    0.076    0.176   0.078        NaN\nNOVCHURN_chao    0.107  0.123    0.099    0.153   0.108        NaN\nNOVCHURN_cfg     0.115  0.071    0.114    0.088   0.106      0.618\nNOVCHURN_exc     0.008  0.006   -0.007    0.063   0.008      0.014\nNOVCHURN_zperm   0.007  0.021   -0.003    0.\n24 display_data [IMAGE]\ncode_demo.ipynb\ndemo_results\nmake_mini_demo_data.py\nmethod_out.json\nmini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] ASSISTANT · 2026-09-29 11:45:50 UTC

```
The notebook runs correctly, and `method.py` has no iteration parameters, so there is nothing to scale up. Next I'm checking the figure and finishing the manifest, README and output JSON.
```

### [24] TOOL CALL — Bash · 2026-09-29 11:45:50 UTC

```
rm -rf demo_results method_out.json && /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/python -c "
import nbformat,base64
nb=nbformat.read('code_demo.ipynb',as_version=4); nbformat.validator.normalize(nb)
_,nb=nbformat.validator.normalize(nb); nbformat.write(nbformat.from_dict(nb),'code_demo.ipynb')
nb=nbformat.read('code_demo.ipynb',as_version=4)
for c in nb.cells:
  for o in c.get('outputs',[]):
    if 'image/png' in o.get('data',{}): open('$HOME/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
print(all('id' in c for c in nb.cells))
" 2>&1 | tail -2; grep -c 'raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-16/demo/mini_demo_data.json' code_demo.ipynb; cp ~/fig.png /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad/fig.png; rm ~/fig.png
```

### [25] TOOL CALL — Read · 2026-09-29 11:45:50 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad/fig.png
```

### [26] TOOL RESULT — Bash · 2026-09-29 11:45:50 UTC

```
{"stdout": "True\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL RESULT — Read · 2026-09-29 11:45:50 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [28] ASSISTANT · 2026-09-29 11:46:06 UTC

```
The legend in panel 3 covers the bars. I'm fixing that and re-running the test.
```

### [29] TOOL CALL — Bash · 2026-09-29 11:46:06 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad && sed -i 's/pc.plot.bar(ax=ax\[2\]); ax\[2\].set_ylabel/pc.plot.bar(ax=ax[2]); ax[2].set_ylim(top=max(0.9, float(np.nanmax(pc.to_numpy(float))) + 0.2)); ax[2].legend(ncol=3, loc="upper center", fontsize=8); ax[2].set_ylabel/' $S/mk_nb.py && grep -c 'ncol=3' $S/mk_nb.py && cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_NGXDZpLy-s1z && python3 $S/mk_nb.py code_demo.ipynb && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/python jupyter ipykernel nbformat && /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/python -c "
import nbformat; nb=nbformat.read('code_demo.ipynb',as_version=4); _,nb=nbformat.validator.normalize(nb); nbformat.write(nbformat.from_dict(nb),'code_demo.ipynb')" && time /tmp/aii_nb_test_envs/art_NGXDZpLy-s1z-88dd16d8b3a1/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | grep -v WARNING | tail -5; python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
errs=[o for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs'] if o['output_type']=='error'];print('errors',len(errs))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if 'image/png' in o.get('data',{}): open('$S/fig2.png','wb').write(base64.b64decode(o['data']['image/png']))
"; rm -rf demo_results method_out.json
```

### [30] TOOL CALL — Read · 2026-09-29 11:46:06 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-NGXDZpLy-s1z/072c37f8-5f60-498b-b974-af966df68486/scratchpad/fig2.png
```

### [31] TOOL RESULT — Bash · 2026-09-29 11:46:24 UTC

```
{"stdout": "1\n[NbConvertApp] Writing 197151 bytes to code_demo.ipynb\n\nreal\t0m18.675s\nuser\t0m16.076s\nsys\t0m1.899s\nerrors 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL RESULT — Read · 2026-09-29 11:46:24 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [33] ASSISTANT · 2026-09-29 11:46:36 UTC

```
Now the README, manifest and structured output.
```

### [34] TOOL CALL — Bash · 2026-09-29 11:46:36 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# No heavy binaries or cache directories in this workspace: every file is a small text/JSON/notebook file
# (all under the 10 MB auto-keep floor), so no keep/delete decisions are required.
entries: []
EOF
cat > README.md <<'EOF'
# EXP16 demo: is research-topic churn real or small-sample noise?

This is a Colab-ready demo notebook for experiment 16 (artifact `art_NGXDZpLy-s1z`). The experiment is a zero-cost check of whether the
*home-only neighbourhood churn/novelty* signal in OpenAlex concept networks is real, or an artefact of thin samples at about 10 home papers per year.
The notebook reproduces the experiment's `method.py` (`build_outputs`) with minimal changes:
- OLS models fitted on DEV only, using the B5 baseline plus each raw or noise-controlled churn variant;
- the out-of-DEV Spearman check;
- the `exp_gen_sol_out` examples;
- the verdict metadata (`PARTLY_THIN`, P1–P3, the partial-Spearman table, reliabilities).

The notebook runs on a stratified 100-concept slice of the full 7,748-concept analysis table.

## Layout
| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook (executed, about 20 s including installs) |
| `mini_demo_data.json` | 100 concepts (34 DEV, 22 each OLDHO / COH1014 / COH1517) with B5 covariates, 27 indicator variants and the `O2r_m50` outcome, plus the small full-run summary results that `build_outputs()` reads |
| `make_mini_demo_data.py` | the script that built `mini_demo_data.json` from the experiment artifact's `tables.load_tables()` and `results/*.json` |
| `.aii/manifest.yaml` | storage manifest (nothing heavy) |

## How to run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The notebook loads the data from the GitHub raw URL and falls back to the local `mini_demo_data.json`.
To test locally in a clean environment:
```bash
uv venv --seed --python 3.12 /tmp/nbenv && uv pip install --python /tmp/nbenv/bin/python jupyter ipykernel
/tmp/nbenv/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```
To rebuild the mini data, you need the experiment artifact folder and its upstream inputs:
`uv run --no-project --with pandas --with pyarrow --with numpy --with scipy python make_mini_demo_data.py <experiment-16-folder>`.

## Restoring removed files
Nothing was marked `delete`, so there is nothing to restore. The notebook writes `method_out.json` and `demo_results/prediction_check.json` when it runs. These are regenerated by re-running the notebook.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
ls -la; du -sh .
````

### [35] TOOL RESULT — Bash · 2026-09-29 11:46:36 UTC

```
{"stdout": "total 3586\ndrwxrwxrwx 3 root root 1057621 Sep 29 11:46 .\ndrwxrwxrwx 7 root root 2000651 Sep 29 11:41 ..\ndrwxrwxrwx 2 root root   20100 Sep 29 11:46 .aii\n-rw-rw-rw- 1 root root      54 Sep 29 11:42 .aii_claude_session.json\n-rw-rw-rw- 1 root root  247959 Sep 29 11:46 .repl_agent.ptylog\n-rw-rw-rw- 1 root root      97 Sep 29 11:46 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 root root    2255 Sep 29 11:46 README.md\n-rw-rw-rw- 1 root root  197163 Sep 29 11:46 code_demo.ipynb\n-rw-rw-rw- 1 root root    4067 Sep 29 11:43 make_mini_demo_data.py\n-rw-rw-rw- 1 root root  138245 Sep 29 11:43 mini_demo_data.json\n1.6M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] ASSISTANT · 2026-09-29 11:46:46 UTC

```
The demo notebook is finished. It runs start to finish with no errors in a clean Python 3.12 environment set up like Colab, in about 19 seconds including package installs.

**Files in the workspace**
- **`code_demo.ipynb`** has 25 cells. It follows `method.py` step by step: it fits the prediction models on the DEV body only, using the five baseline covariates (B5, standardised with the frozen EXP10 constants) plus each churn variant. It then checks those models on the held-out bodies, writes one output example per concept, and assembles the verdict metadata. Code is copied from the original with only notebook-level changes, and a short explanation sits before each section. It contains the exact `GITHUB_DATA_URL` and loads the data from GitHub, falling back to the local file.
- **`mini_demo_data.json`** (138 KB) holds 100 concepts sampled from the full 7,748: 34 DEV and 22 from each held-out body. Each concept has its baseline covariates, all 27 raw and noise-controlled indicators, and the outcome. The file also includes the small full-run result files that `method.py` reads.
- **`make_mini_demo_data.py`** is the script that built the data file from the experiment folder.
- **`README.md`**, **`.aii/manifest.yaml`** (nothing large, so no entries) and **`.terminal_claude_agent_struct_out.json`**.

**What is not re-run**
- **Upstream stages:** the 14 upstream pipeline scripts (null models, 2,000-draw bootstraps, power simulation) take about 30 minutes and need earlier artifacts. They are not run; the notebook loads their saved results, and the stage-runner function is kept for reference.
- **Cross-checks:** the two cross-checks against other artifacts need input files over 100 MB, so the notebook reports their stored full-run results. Those showed full concept coverage and identical component values.

**Scaling:** `method.py` has no iteration or sample-size settings of its own. The 100-concept cap on the demo data is the only size limit, and it already runs far inside the 10-minute budget, so there was nothing to scale up.

**Results shown in the last cell**
- **Headline:** the full-run verdict is `PARTLY_THIN`, with P1 failing and P2 and P3 holding.
- **Main table:** it lists partial correlations with the outcome by body. The raw churn composite is +0.116 pooled; its permutation-excess version drops to +0.008, and the rarefied version keeps +0.078.
- **Plot 1:** raw versus noise-controlled variants, with confidence intervals.
- **Plot 2:** raw edge persistence tracks its own null mean in the demo sample (rho 0.87).
- **Plot 3:** out-of-DEV prediction accuracy per model. With only 22 concepts per body these numbers are noisy, and the notebook says so.

My task-tracking tool wasn't available in this session, so I followed the six-item todo list in order without recording it.
```
