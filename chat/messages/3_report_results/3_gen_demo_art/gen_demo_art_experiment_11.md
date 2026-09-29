# gen_demo_art_experiment_11 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_11` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 11:29:00 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 11:29:08 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/`:
GOOD: `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/file.py`, `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-14/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-14/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-14/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] TOOL CALL — Skill · 2026-09-29 11:29:12 UTC

```
aii-colab
```

### [4] TOOL RESULT — Skill · 2026-09-29 11:29:12 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [5] TOOL CALL — Skill · 2026-09-29 11:29:12 UTC

```
aii-long-running-tasks
```

### [6] TOOL RESULT — Skill · 2026-09-29 11:29:12 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [7] TOOL CALL — Bash · 2026-09-29 11:29:12 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; ls -la; ls -la .aii; A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; ls -la $A; du -sh $A/* | sort -h | tail -30; wc -l $A/method.py
```

### [8] TOOL RESULT — Bash · 2026-09-29 11:29:12 UTC

```
{"stdout": "total 1999\ndrwxr-xr-x 3 root root 1003475 Sep 29 11:29 .\ndrwxr-xr-x 4 root root 1006019 Sep 29 11:28 ..\ndrwxr-xr-x 2 root root       1 Sep 29 11:28 .aii\n-rw------- 1 root root      54 Sep 29 11:29 .aii_claude_session.json\n-rw-r--r-- 1 root root   35797 Sep 29 11:29 .repl_agent.ptylog\ntotal 981\ndrwxr-xr-x 2 root root       1 Sep 29 11:28 .\ndrwxr-xr-x 3 root root 1003475 Sep 29 11:29 ..\ntotal 41904\ndrwxr-xr-x 10 root root  2006256 Sep 29 09:00 .\ndrwxr-xr-x  7 root root  3000249 Sep 29 05:17 ..\ndrwxr-xr-x  2 root root    62500 Sep 29 06:21 .aii\n-rw-------  1 root root       54 Sep 29 05:18 .aii_claude_session.json\n-rw-------  1 root root     9750 Sep 29 06:21 .aii_worker_result.json\ndrwxr-xr-x  8 root root  2001902 Sep 29 06:17 .git\n-rw-r--r--  1 root root       85 Sep 29 06:12 .gitignore\n-rw-r--r--  1 root root   576603 Sep 29 06:21 .repl_agent.ptylog\n-rw-r--r--  1 root root     2987 Sep 29 06:17 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root    13617 Sep 29 06:17 README.md\n-rw-r--r--  1 root root     6994 Sep 29 05:45 audit.py\ndrwxr-xr-x  2 root root  2001535 Sep 29 05:40 data\ndrwxr-xr-x  2 root root  1027933 Sep 29 06:08 figures\n-rw-r--r--  1 root root 14901382 Sep 29 06:14 full_method_out.json\ndrwxr-xr-x  2 root root  1016396 Sep 29 09:00 lib\ndrwxr-xr-x  3 root root  1004277 Sep 29 06:17 logs\n-rw-r--r--  1 root root     3761 Sep 29 06:02 method.py\n-rw-r--r--  1 root root 13186742 Sep 29 06:09 method_out.json\n-rw-r--r--  1 root root     6964 Sep 29 06:14 mini_method_out.json\n-rw-r--r--  1 root root     7714 Sep 29 05:29 prereg.md\n-rw-r--r--  1 root root     6964 Sep 29 06:14 preview_method_out.json\n-rw-r--r--  1 root root     2023 Sep 29 06:14 pyproject.toml\n-rw-r--r--  1 root root       22 Sep 29 05:32 pytest.ini\n-rw-r--r--  1 root root     4750 Sep 29 06:09 reconciling_cheng.md\n-rw-r--r--  1 root root     9126 Sep 29 06:15 rederive.py\n-rw-r--r--  1 root root     9081 Sep 29 06:17 reproducibility.md\n-rw-r--r--  1 root root     1305 Sep 29 06:14 requirements.lock.txt\n-rwxr-xr-x  1 root root      343 Sep 29 06:17 restore.sh\ndrwxr-xr-x  2 root root  1028115 Sep 29 06:16 results\ndrwxr-xr-x  2 root root  1001230 Sep 29 09:00 tests\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/pytest.ini\n512\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/restore.sh\n1.5K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/requirements.lock.txt\n2.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/pyproject.toml\n4.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method.py\n5.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/reconciling_cheng.md\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/audit.py\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/mini_method_out.json\n7.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/preview_method_out.json\n8.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/prereg.md\n9.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/rederive.py\n9.0K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/reproducibility.md\n14K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/README.md\n992K\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/tests\n1.1M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/logs\n1.2M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib\n1.3M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/figures\n1.3M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/results\n13M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method_out.json\n15M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/full_method_out.json\n18M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/data\n89 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/method.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] TOOL CALL — Bash · 2026-09-29 11:29:14 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $A/method.py; echo ----; cat $A/preview_method_out.json | head -c 4000; echo; ls -la $A/lib $A/data $A/results; cat $A/pyproject.toml
```

### [10] TOOL RESULT — Bash · 2026-09-29 11:29:14 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Orchestrator: Cheng et al. (2023) ideational consistency -- replication, size control and the reach-vs-depth\nreversal on this run's selection bodies (EXP5 frame + EXP10 2015-17 cohort). Cache only, CPU only, $0 LLM.\n\nSteps (run all in order, or one with --only):\n  S0  frozen spec + seal (before any model)             lib/s0_spec.py\n  S1  build Cheng measures (cheng_features / static)     lib/build.py         [--sample N for staged scale-up]\n  S2  construct-identity check                           lib/identity.py\n  S3  test A: Cheng replication panel (A1/A1-NB/A2/A3)   lib/panel_cheng.py\n  S3NB  re-fit A1-NB only (patches cheng_panel_models.json)  lib/panel_cheng.py\n  S4  test B: static early trait, reach vs depth         lib/static_cheng.py\n  S5  test C: within-panel reach vs depth                lib/panel_cheng.py\n  S6  test D: Palla size x turnover                      lib/static_cheng.py\n  S7  test E: HOME vs ALL coupling                       lib/static_cheng.py\n  S8  verdict, figures, method_out.json, write-up        lib/outputs.py\nUsage: uv run method.py [--only S3] [--sample 500] [--quick]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport sys\n\nfor _v in (\"OMP_NUM_THREADS\", \"OPENBLAS_NUM_THREADS\", \"MKL_NUM_THREADS\"):   # one BLAS thread per process: the\n    os.environ.setdefault(_v, \"1\")                                         # steps parallelise across processes\nimport time\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nfrom common import set_limits, setup_logger  # noqa: E402\n\nSTEPS = [\"S0\", \"S1\", \"S2\", \"S3\", \"S4\", \"S5\", \"S6\", \"S7\", \"S8\"]\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--only\", type=str, default=\"\")\n    ap.add_argument(\"--sample\", type=int, default=0, help=\"S1: number of EXP5 concepts (staged scale-up)\")\n    ap.add_argument(\"--quick\", action=\"store_true\", help=\"S3-S7: 10%% of concepts, few bootstrap draws (timing)\")\n    ap.add_argument(\"--workers\", type=int, default=0)\n    args = ap.parse_args()\n    logger = setup_logger(\"method\")\n    set_limits(26.0)\n    steps = [s.strip() for s in args.only.split(\",\")] if args.only else STEPS\n\n    @logger.catch(reraise=True)\n    def _run() -> None:\n        for s in steps:\n            t = time.time()\n            logger.info(f\"===== {s} start\")\n            if s == \"S0\":\n                import s0_spec\n                s0_spec.run(logger)\n            elif s == \"S1\":\n                import build\n                build.run(logger, sample=args.sample, workers=args.workers)\n            elif s == \"S2\":\n                import identity\n                identity.run(logger)\n            elif s == \"S3\":\n                import panel_cheng\n                panel_cheng.run_A(logger, quick=args.quick, workers=args.workers)\n            elif s == \"S3NB\":\n                import panel_cheng\n                panel_cheng.refit_nb(logger)\n            elif s == \"S4\":\n                import static_cheng\n                static_cheng.run_B(logger, quick=args.quick)\n            elif s == \"S5\":\n                import panel_cheng\n                panel_cheng.run_C(logger, quick=args.quick, workers=args.workers)\n            elif s == \"S6\":\n                import static_cheng\n                static_cheng.run_D(logger, quick=args.quick)\n            elif s == \"S7\":\n                import static_cheng\n                static_cheng.run_E(logger, quick=args.quick)\n            elif s == \"S8\":\n                import outputs\n                outputs.run(logger)\n            else:\n                raise ValueError(f\"unknown step {s}\")\n            logger.info(f\"===== {s} done in {(time.time() - t) / 60:.1f} min\")\n\n    _run()\n\n\nif __name__ == \"__main__\":\n    main()\n----\n{\n  \"metadata\": {\n    \"method_name\": \"Cheng ideational consistency (count-weighted topic co-usage cosine) added to the B5 baseline\",\n    \"baseline\": \"predict_B5 = rank-OLS on B5 fitted on DEV\",\n    \"method\": \"predict_B5_plus_CONS = same + CONS_early_home, fitted on DEV, applied frozen\",\n    \"output\": \"O2r_m50 (rarefied venue-field richness at t0+6..t0+8); 'NA' where undefined\",\n    \"label\": \"selection data, not confirmation\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"EXP5_frame\",\n      \"examples\": [\n        {\n          \"input\": \"Complete intersection | ci=3 | t0=2012 | group=MATHDEC | body=COHORT_2010_14\",\n          \"output\": \"2.9608\",\n          \"predict_B5\": \"3.8994\",\n          \"predict_B5_plus_CONS\": \"3.8302\",\n          \"metadata_ci\": 3,\n          \"metadata_t0\": 2012,\n          \"metadata_group\": \"MATHDEC\",\n          \"metadata_group5\": \"MATHDEC\",\n          \"metadata_body\": \"COHORT_2010_14\",\n          \"metadata_CONS_early_home\": 0.6306984195836987,\n          \"metadata_CONS_early_all\": 0.6953313198436348,\n          \"metadata_CONS_r_early_home\": 0.6900652119564956,\n          \"metadata_EMB_early_home_analogue\": 3.2053415177599422,\n          \"metadata_SOC_early_home\": 0.008658008658008658,\n          \"metadata_V_t0p2\": 29.0,\n          \"metadata_V_t0p3\": 26.0,\n          \"metadata_CONS_imputed_dev_median\": false,\n          \"metadata_label\": \"selection data, not confirmation\",\n          \"metadata_O2r_m50\": 2.96078431372549,\n          \"metadata_O2r_resid\": -1.4819808004866881,\n          \"metadata_O1c\": -0.21292199724267125,\n          \"metadata_O1b\": 0.0,\n          \"metadata_O3\": 0.0\n        },\n        {\n          \"input\": \"Torque converter | ci=4 | t0=2004 | group=Eng | body=DEV\",\n          \"output\": \"2.8987\",\n          \"predict_B5\": \"2.7238\",\n          \"predict_B5_plus_CONS\": \"2.6578\",\n          \"metadata_ci\": 4,\n          \"metadata_t0\": 2004,\n          \"metadata_group\": \"Eng\",\n          \"metadata_group5\": \"CS+Eng\",\n          \"metadata_body\": \"DEV\",\n          \"metadata_CONS_early_home\": 0.6011880046495223,\n          \"metadata_CONS_early_all\": 0.5838037184897182,\n          \"metadata_CONS_r_early_home\": 0.7068124284415241,\n          \"metadata_EMB_early_home_analogue\": 1.5183806686663486,\n          \"metadata_SOC_early_home\": 0.0,\n          \"metadata_V_t0p2\": 17.0,\n          \"metadata_V_t0p3\": 19.0,\n          \"metadata_CONS_imputed_dev_median\": false,\n          \"metadata_label\": \"selection data, not confirmation\",\n          \"metadata_O2r_m50\": 2.8987341772151547,\n          \"metadata_O2r_resid\": -1.4979931361786871,\n          \"metadata_O1c\": 0.34740130715340367,\n          \"metadata_O1b\": 1.0,\n          \"metadata_O3\": 0.0\n        },\n        {\n          \"input\": \"Early adopter | ci=16 | t0=2011 | group=SOC | body=COHORT_2010_14\",\n          \"output\": \"9.8824\",\n          \"predict_B5\": \"6.8889\",\n          \"predict_B5_plus_CONS\": \"6.7665\",\n          \"metadata_ci\": 16,\n          \"metadata_t0\": 2011,\n          \"metadata_group\": \"SOC\",\n          \"metadata_group5\": \"SOC\",\n          \"metadata_body\": \"COHORT_2010_14\",\n          \"metadata_CONS_early_home\": null,\n          \"metadata_CONS_early_all\": 0.3231991272444683,\n          \"metadata_CONS_r_early_home\": null,\n          \"metadata_EMB_early_home_analogue\": null,\n          \"metadata_SOC_early_home\": 0.0,\n          \"metadata_V_t0p2\": 25.0,\n          \"metadata_V_t0p3\": 27.0,\n          \"metadata_CONS_imputed_dev_median\": true,\n          \"metadata_label\": \"selection data, not confirmation\",\n          \"metadata_O2r_m50\": 9.882395628788526,\n          \"metadata_O2r_resid\": 5.485668315394684,\n          \"metadata_O1c\": 0.2076393647782444,\n          \"metadata_O1b\": 1.0,\n          \"metadata_O3\": 0.0\n        }\n      ]\n    },\n    {\n      \"dataset\": \"COHORT_2015_17\",\n      \"examples\": [\n        {\n          \"input\": \"Electrical impedance myography | ci=233 | t0=2016 | group=Med | body=COHORT_2015_17\",\n          \"output\": \"NA\",\n          \"predict_B5\": \"4.5590\",\n          \"predict_B5_plus_CONS\": \"4.6175\",\n          \n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/data:\ntotal 19638\ndrwxr-xr-x  2 root root 2001535 Sep 29 05:40 .\ndrwxr-xr-x 10 root root 2006256 Sep 29 09:00 ..\n-rw-r--r--  1 root root   18147 Sep 29 05:36 V_cohort.parquet\n-rw-r--r--  1 root root 1386293 Sep 29 05:35 V_exp5.parquet\n-rw-r--r--  1 root root    8128 Sep 29 05:57 boot_ratio_ALL_joint.npy\n-rw-r--r--  1 root root    8128 Sep 29 05:47 boot_ratio_HOME_joint.npy\n-rw-r--r--  1 root root 9530698 Sep 29 05:36 cheng_features.parquet\n-rw-r--r--  1 root root 1380894 Sep 29 05:36 cheng_static.parquet\n-rw-r--r--  1 root root 1651491 Sep 29 05:36 identity_table.parquet\n-rw-r--r--  1 root root 2115491 Sep 29 06:02 static_analysis_table.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/lib:\ntotal 3120\ndrwxr-xr-x  2 root root 1016396 Sep 29 09:00 .\ndrwxr-xr-x 10 root root 2006256 Sep 29 09:00 ..\n-rw-r--r--  1 root root   14185 Sep 29 05:31 build.py\n-rw-r--r--  1 root root   10060 Sep 29 05:31 cheng.py\n-rw-r--r--  1 root root    5216 Sep 29 05:27 common.py\n-rw-r--r--  1 root root   12721 Sep 29 05:26 ego.py\n-rw-r--r--  1 root root    1945 Sep 29 05:26 ego_ctx.py\n-rw-r--r--  1 root root    9852 Sep 29 05:26 ego_yearly.py\n-rw-r--r--  1 root root    8949 Sep 29 05:26 fe_stats.py\n-rw-r--r--  1 root root    5212 Sep 29 05:35 identity.py\n-rw-r--r--  1 root root    9137 Sep 29 05:34 ladder.py\n-rw-r--r--  1 root root   20838 Sep 29 06:09 outputs.py\n-rw-r--r--  1 root root   18372 Sep 29 06:02 panel_cheng.py\n-rw-r--r--  1 root root    4457 Sep 29 05:26 panel_m.py\n-rw-r--r--  1 root root    1777 Sep 29 06:03 provenance.py\n-rw-r--r--  1 root root    8080 Sep 29 05:26 rq1stats.py\n-rw-r--r--  1 root root    7569 Sep 29 05:29 s0_spec.py\n-rw-r--r--  1 root root   20877 Sep 29 05:59 static_cheng.py\n-rw-r--r--  1 root root    8655 Sep 29 05:26 stats_core.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/results:\ntotal 3249\ndrwxr-xr-x  2 root root 1028115 Sep 29 06:16 .\ndrwxr-xr-x 10 root root 2006256 Sep 29 09:00 ..\n-rw-r--r--  1 root root    1364 Sep 29 06:07 audit.json\n-rw-r--r--  1 root root   66186 Sep 29 06:02 cheng_panel_models.json\n-rw-r--r--  1 root root  152913 Sep 29 06:03 cheng_static.json\n-rw-r--r--  1 root root    3521 Sep 29 06:09 cheng_verdict.json\n-rw-r--r--  1 root root    6403 Sep 29 06:04 coupling.json\n-rw-r--r--  1 root root    3514 Sep 29 06:07 deviations.json\n-rw-r--r--  1 root root    6396 Sep 29 05:30 frozen_spec.json\n-rw-r--r--  1 root root    3347 Sep 29 06:09 headline_numbers.json\n-rw-r--r--  1 root root    7653 Sep 29 05:36 identity_check.json\n-rw-r--r--  1 root root   10505 Sep 29 06:03 palla.json\n-rw-r--r--  1 root root   13181 Sep 29 06:06 panel_C.json\n-rw-r--r--  1 root root    1616 Sep 29 06:09 predictive_comparison.json\n-rw-r--r--  1 root root    5032 Sep 29 06:03 provenance.json\n-rw-r--r--  1 root root    2180 Sep 29 06:16 rederive.json\n-rw-r--r--  1 root root    1411 Sep 29 05:36 s1_build.json\n-rw-r--r--  1 root root     748 Sep 29 05:33 s1_build_sample50.json\n-rw-r--r--  1 root root     804 Sep 29 05:33 s1_build_sample500.json\n-rw-r--r--  1 root root    1131 Sep 29 06:05 unit_tests.json\n[project]\nname = \"cheng-reach-depth\"\nversion = \"0.1.0\"\ndescription = \"Cheng et al. 2023 ideational consistency: replication, size control and reach-vs-depth reversal on selection bodies\"\nrequires-python = \"==3.12.*\"\n# every package installed in .venv, pinned exactly (uv pip freeze; identical to requirements.lock.txt)\ndependencies = [\n  \"asttokens==3.0.2\",\n  \"attrs==26.1.0\",\n  \"babel==2.18.0\",\n  \"cffi==2.1.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"executing==2.2.1\",\n  \"faicons==0.2.2\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"great-tables==1.0.0\",\n  \"htmltools==0.7.0\",\n  \"igraph==1.0.0\",\n  \"importlib-metadata==9.0.1\",\n  \"importlib-resources==7.1.0\",\n  \"iniconfig==2.3.0\",\n  \"interface-meta==2.0.1\",\n  \"ipython==9.17.1\",\n  \"ipython-pygments-lexers==1.1.1\",\n  \"jedi==0.20.0\",\n  \"joblib==1.6.0\",\n  \"jsonschema==4.26.0\",\n  \"jsonschema-specifications==2025.9.1\",\n  \"kiwisolver==1.5.1\",\n  \"leidenalg==0.12.0\",\n  \"loguru==0.7.3\",\n  \"lxml==6.1.3\",\n  \"maketables==0.1.8\",\n  \"matplotlib==3.11.2\",\n  \"matplotlib-inline==0.2.2\",\n  \"multimark==0.3.2\",\n  \"narwhals==2.26.0\",\n  \"networkx==3.7\",\n  \"nokap==0.1.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==2.3.3\",\n  \"parso==0.8.7\",\n  \"patsy==1.0.3\",\n  \"pexpect==4.9.0\",\n  \"pillow==12.3.0\",\n  \"pluggy==1.6.0\",\n  \"prompt-toolkit==3.0.53\",\n  \"psutil==7.2.2\",\n  \"ptyprocess==0.7.0\",\n  \"pure-eval==0.2.4\",\n  \"pyarrow==25.0.1\",\n  \"pycparser==3.0\",\n  \"pyfixest==0.60.0\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"python-docx==1.2.0\",\n  \"pytz==2026.4\",\n  \"pyyaml==6.0.3\",\n  \"referencing==0.37.0\",\n  \"rpds-py==2026.6.3\",\n  \"scipy==1.18.1\",\n  \"seaborn==0.13.2\",\n  \"six==1.17.0\",\n  \"snowballstemmer==3.1.1\",\n  \"stack-data==0.6.3\",\n  \"statsmodels==0.15.0\",\n  \"tabulate==0.10.0\",\n  \"texttable==1.7.0\",\n  \"tqdm==4.70.1\",\n  \"traitlets==5.16.1\",\n  \"typing-extensions==4.16.0\",\n  \"tzdata==2026.4\",\n  \"wcwidth==0.9.1\",\n  \"websockets==17.1\",\n  \"wrapt==2.5.0\",\n  \"zipp==4.1.0\",\n]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-29 11:29:18 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $A/lib/common.py $A/lib/cheng.py; sed -n 1,400p $A/lib/build.py
```

### [12] TOOL RESULT — Bash · 2026-09-29 11:29:18 UTC

```
{"stdout": "\"\"\"Shared paths, constants and small helpers for the Cheng reach-vs-depth experiment.\n\nEvery upstream input is read BY PATH (read-only) under RUN_ROOT/3_invention_loop; nothing is written outside ROOT.\nego_ctx.py / ego.py (copied verbatim from Exp11) import INPUTS and DATA from here: INPUTS points at Exp11's\nread-only inputs/ folder (topic ids, topic metadata, EXP3 backbone slices) so the SELF-topic rule is byte-identical.\"\"\"\nfrom __future__ import annot... [truncated, 30990 chars total]
```

### [13] TOOL CALL — Bash · 2026-09-29 11:29:24 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $A/lib/panel_cheng.py
```

### [14] TOOL RESULT — Bash · 2026-09-29 11:29:24 UTC

```
{"stdout": "\"\"\"S3 (test A, Cheng replication panel) and S5 (test C, within-panel reach vs depth).\n\nTest A: EXP5 concept-years t0+1 <= t <= min(t0+10, 2021) with finite CONS_b(t) (b = HOME / ALL).\n  A1    fepois V(t+1) ~ zCONS + zEMB + zSOC | age + year          (Cheng's spec; CRV1 by concept)\n  A1c   fepois V(t+1) ~ zCONS | age + year                        (CONS-only variant, all CONS rows)\n  A1-NB statsmodels NB2 with age + year dummies (cluster-robust by concept)\n  A2    A1 + log1p V(t);  A3  A2 | ci + year\n  RATIO b_A2 / b_A1 on CONS, 500-draw concept-cluster bootstrap, same draws for A1 and A2 (numpy Poisson IRLS with\n        age/year dummies, validated against pyfixest on the point estimate)\nTest C: Exp11 yearly_panel estimation sample (at_risk_next > 0, deg >= 2), finite CONS_home(t).\n  C1 fepois entries(t+1) ~ zCONS_home(t) + log1p_home + log1p_all + log1p_deg + log_at_risk | ci + year\n  C2 feols dHomeShare(t+1) ~ same | ci + year\n  500-draw concept-cluster bootstrap (duplicated concepts relabelled as new FE units).\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport multiprocessing as mp\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import (DATA, EXP5, EXP11, GROUP5, GROUPS5, N_BOOT_PANEL, RES, SEED, SELECTION_LABEL, add_deviation,\n                    body_of_split, home_codes, jdump, n_workers)\nfrom rq1stats import dersimonian_laird\n\nXS_JOINT = [\"zCONS\", \"zEMB\", \"zSOC\"]\n\n\n# ----------------------------------------------------------------------------- data\ndef panel_A(build: str) -> pd.DataFrame:\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\", usecols=[\"ci\", \"t0\", \"group\", \"split\"])\n    fr[\"body\"] = fr.split.map(body_of_split)\n    fr[\"group5\"] = fr.group.map(GROUP5)\n    f = pd.read_parquet(DATA / \"cheng_features.parquet\")\n    f = f[(f.body_src == \"EXP5\") & (f.build == build)][[\"ci\", \"year\", \"CONS\", \"EMB\", \"SOC\", \"n_papers\", \"n_topics\"]]\n    V = pd.read_parquet(DATA / \"V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    d = f.merge(fr, on=\"ci\")\n    d = d[(d.year >= d.t0 + 1) & (d.year <= np.minimum(d.t0 + 10, 2021))]\n    d = d.merge(V, on=[\"ci\", \"year\"], how=\"left\").merge(\n        V.assign(year=V.year - 1).rename(columns={\"V\": \"V_next\"}), on=[\"ci\", \"year\"], how=\"left\")\n    d = d[np.isfinite(d.CONS)].copy()\n    d[\"age\"] = d.year - d.t0\n    d[\"logV\"] = np.log1p(d.V)\n    return d.reset_index(drop=True)\n\n\ndef zcols(d: pd.DataFrame, cols: list[str]) -> pd.DataFrame:\n    d = d.copy()\n    for c in cols:\n        v = d[c].to_numpy(float)\n        d[\"z\" + c] = (v - np.nanmean(v)) / np.nanstd(v)\n    return d\n\n\n# ----------------------------------------------------------------------------- numpy Poisson IRLS (dummies FE)\ndef dummy_design(d: pd.DataFrame, xs: list[str], fe: list[str]) -> tuple[np.ndarray, list[str]]:\n    cols = [np.ones(len(d))]\n    names = [\"_const\"]\n    for c in xs:\n        cols.append(d[c].to_numpy(float))\n        names.append(c)\n    for f in fe:\n        v = d[f].to_numpy()\n        for u in np.unique(v)[1:]:\n            cols.append((v == u).astype(float))\n            names.append(f\"{f}={u}\")\n    return np.column_stack(cols), names\n\n\ndef poisson_irls(X: np.ndarray, y: np.ndarray, iters: int = 100, tol: float = 1e-10) -> np.ndarray:\n    mu = y.mean() + 0.1\n    b = np.zeros(X.shape[1])\n    b[0] = math.log(mu)\n    eta = X @ b\n    for _ in range(iters):\n        mu = np.exp(np.clip(eta, -30, 30))\n        z = eta + (y - mu) / mu\n        XtW = X.T * mu\n        H = XtW @ X\n        try:\n            bn = np.linalg.solve(H, XtW @ z)\n        except np.linalg.LinAlgError:\n            bn = np.linalg.lstsq(H, XtW @ z, rcond=None)[0]\n        if np.max(np.abs(bn - b)) < tol:\n            b = bn\n            break\n        b = bn\n        eta = X @ b\n    return b\n\n\ndef _boot_ratio_worker(args) -> list[tuple[float, float]]:\n    X1, X2, y, cl_idx, seeds = args\n    out = []\n    for s in seeds:\n        rng = np.random.default_rng(s)\n        pick = rng.integers(0, len(cl_idx), len(cl_idx))\n        rows = np.concatenate([cl_idx[p] for p in pick])\n        b1 = poisson_irls(X1[rows], y[rows])[1]\n        b2 = poisson_irls(X2[rows], y[rows])[1]\n        out.append((b1, b2))\n    return out\n\n\ndef cluster_index(ci: np.ndarray) -> list[np.ndarray]:\n    order = np.argsort(ci, kind=\"stable\")\n    u, start = np.unique(ci[order], return_index=True)\n    return np.split(order, start[1:])\n\n\ndef boot_ratio(d: pd.DataFrame, xs: list[str], n_boot: int, seed: int, workers: int) -> dict:\n    \"\"\"Cluster bootstrap of b_A1 and b_A2 on the first regressor (zCONS), same draws.\"\"\"\n    X1, _ = dummy_design(d, xs, [\"age\", \"year\"])\n    X2, _ = dummy_design(d, xs + [\"logV\"], [\"age\", \"year\"])\n    y = d.V_next.to_numpy(float)\n    cl = cluster_index(d.ci.to_numpy())\n    b1p, b2p = poisson_irls(X1, y)[1], poisson_irls(X2, y)[1]\n    seeds = [seed + k for k in range(n_boot)]\n    parts = [seeds[i::workers] for i in range(workers)]\n    res = []\n    if workers > 1:\n        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex:\n            for r in ex.map(_boot_ratio_worker, [(X1, X2, y, cl, p) for p in parts]):\n                res.extend(r)\n    else:\n        res = _boot_ratio_worker((X1, X2, y, cl, seeds))\n    B = np.array(res)\n    ratio = B[:, 1] / B[:, 0]\n    pr = b2p / b1p\n    return {\"b_A1_irls\": b1p, \"b_A2_irls\": b2p, \"ratio\": pr,\n            \"ratio_ci\": np.percentile(ratio, [2.5, 97.5]).tolist(), \"ratio_boot_median\": float(np.median(ratio)),\n            \"b_A1_ci_boot\": np.percentile(B[:, 0], [2.5, 97.5]).tolist(),\n            \"b_A2_ci_boot\": np.percentile(B[:, 1], [2.5, 97.5]).tolist(),\n            \"p_one_ratio_lt_0.5\": float((np.sum(ratio >= 0.5) + 1) / (len(ratio) + 1)),\n            \"p_one_A1_gt_0\": float((np.sum(B[:, 0] <= 0) + 1) / (len(B) + 1)),\n            \"n_boot\": int(len(B)), \"resampling_unit\": \"concept (cluster bootstrap)\", \"boot_b\": B}\n\n\n# ----------------------------------------------------------------------------- pyfixest wrappers\ndef fepois(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:\n    import pyfixest as pf\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        fit = pf.fepois(f\"{y} ~ {' + '.join(xs)} | {fe}\", data=d, vcov={\"CRV1\": \"ci\"})\n    return summarize(fit, xs, d)\n\n\ndef feols(d: pd.DataFrame, y: str, xs: list[str], fe: str) -> dict:\n    import pyfixest as pf\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        fit = pf.feols(f\"{y} ~ {' + '.join(xs)} | {fe}\", data=d, vcov={\"CRV1\": \"ci\"})\n    return summarize(fit, xs, d)\n\n\ndef summarize(fit, xs: list[str], d: pd.DataFrame) -> dict:\n    co, se, pv = fit.coef(), fit.se(), fit.pvalue()\n    ci = fit.confint()\n    out = {\"n_rows\": int(fit._N), \"n_concepts\": int(d.ci.nunique()), \"coef\": {}}\n    for x in xs:\n        if x not in co.index:\n            continue\n        b = float(co[x])\n        out[\"coef\"][x] = {\"b\": b, \"se\": float(se[x]), \"ci\": [float(ci.loc[x].iloc[0]), float(ci.loc[x].iloc[1])],\n                          \"p\": float(pv[x]), \"pct_per_sd\": math.exp(b) - 1,\n                          \"pct_ci\": [math.exp(float(ci.loc[x].iloc[0])) - 1, math.exp(float(ci.loc[x].iloc[1])) - 1]}\n    return out\n\n\ndef nb_fit(d: pd.DataFrame, xs: list[str]) -> dict:\n    import statsmodels.api as sm\n    X, names = dummy_design(d, xs, [\"age\", \"year\"])\n    y = d.V_next.to_numpy(float)\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\")\n        m = sm.NegativeBinomial(y, X, loglike_method=\"nb2\")\n        try:\n            r = m.fit(disp=0, maxiter=300, method=\"bfgs\", cov_type=\"cluster\", cov_kwds={\"groups\": d.ci.to_numpy()})\n            how = \"bfgs\"\n        except np.linalg.LinAlgError:\n            # retry: Newton from the Poisson IRLS solution and alpha = 0.5\n            sp0 = np.r_[poisson_irls(X, y), 0.5]\n            r = m.fit(start_params=sp0, disp=0, maxiter=100, method=\"newton\", cov_type=\"cluster\",\n                      cov_kwds={\"groups\": d.ci.to_numpy()})\n            how = \"newton (retry after singular bfgs)\"\n    out = {\"n_rows\": int(len(y)), \"alpha\": float(r.params[-1]), \"converged\": bool(r.mle_retvals.get(\"converged\", True)),\n           \"optimizer\": how, \"coef\": {}}\n    for i, nm in enumerate(names):\n        if nm in xs:\n            b, s = float(r.params[i]), float(r.bse[i])\n            out[\"coef\"][nm] = {\"b\": b, \"se\": s, \"ci\": [b - 1.96 * s, b + 1.96 * s], \"pct_per_sd\": math.exp(b) - 1,\n                               \"p\": float(2 * stats.norm.sf(abs(b / s)))}\n    return out\n\n\n# ----------------------------------------------------------------------------- test A\ndef fit_A_set(d: pd.DataFrame, xs: list[str], with_A3: bool = True, with_nb: bool = False) -> dict:\n    out = {\"A1\": fepois(d, \"V_next\", xs, \"age + year\"),\n           \"A2\": fepois(d, \"V_next\", xs + [\"logV\"], \"age + year\")}\n    if with_A3:\n        out[\"A3\"] = fepois(d, \"V_next\", xs + [\"logV\"], \"ci + year\")\n    if with_nb:\n        try:\n            out[\"A1_NB\"] = nb_fit(d, xs)\n        except (ValueError, np.linalg.LinAlgError) as e:\n            out[\"A1_NB\"] = {\"error\": repr(e)[:300]}\n    b1 = out[\"A1\"][\"coef\"].get(\"zCONS\", {}).get(\"b\", np.nan)\n    b2 = out[\"A2\"][\"coef\"].get(\"zCONS\", {}).get(\"b\", np.nan)\n    out[\"ratio_point\"] = b2 / b1 if b1 else float(\"nan\")\n    return out\n\n\ndef run_A(logger, quick: bool = False, workers: int = 0) -> dict:\n    W = workers or n_workers()\n    nb = 60 if quick else N_BOOT_PANEL\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_boot\": nb,\n           \"spec\": \"PPML (pyfixest fepois); CRV1 by concept; X standardised over the rows of each model\",\n           \"EMB_note\": \"EMB is an ANALOGUE of Cheng's word2vec embeddedness (backbone PMI), not the same measure\",\n           \"builds\": {}}\n    for build in [\"HOME\", \"ALL\"]:\n        t = time.time()\n        d0 = panel_A(build)\n        if quick:\n            keep = d0.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)\n            d0 = d0[d0.ci.isin(keep)]\n        d0 = d0[np.isfinite(d0.V_next)]\n        dj = zcols(d0.dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n        dc = zcols(d0, [\"CONS\"])\n        B = {\"n_rows_CONS\": int(len(dc)), \"n_rows_joint\": int(len(dj)), \"n_concepts_joint\": int(dj.ci.nunique()),\n             \"share_rows_dropped_for_EMB_SOC\": 1 - len(dj) / max(len(dc), 1),\n             \"CONS_mean\": float(d0.CONS.mean()), \"CONS_sd\": float(d0.CONS.std())}\n        B[\"joint\"] = fit_A_set(dj, XS_JOINT, with_A3=True, with_nb=(build == \"HOME\"))\n        B[\"cons_only\"] = fit_A_set(dc, [\"zCONS\"], with_A3=True, with_nb=(build == \"HOME\"))\n        logger.info(f\"A {build}: joint A1 {B['joint']['A1']['coef']['zCONS']} A2 {B['joint']['A2']['coef']['zCONS']}\")\n        # bootstrap ratio (headline = HOME joint), plus CONS-only\n        br = boot_ratio(dj, XS_JOINT, nb, SEED, W)\n        pf1 = B[\"joint\"][\"A1\"][\"coef\"][\"zCONS\"][\"b\"]\n        br[\"irls_vs_pyfixest_abs_diff_A1\"] = abs(br[\"b_A1_irls\"] - pf1)\n        np.save(DATA / f\"boot_ratio_{build}_joint.npy\", br.pop(\"boot_b\"))\n        B[\"joint\"][\"ratio_boot\"] = br\n        brc = boot_ratio(dc, [\"zCONS\"], nb, SEED + 7, W)\n        brc.pop(\"boot_b\")\n        B[\"cons_only\"][\"ratio_boot\"] = brc\n        logger.info(f\"A {build}: ratio {br['ratio']:.3f} CI {br['ratio_ci']} (irls-pf diff \"\n                    f\"{br['irls_vs_pyfixest_abs_diff_A1']:.2e}); cons-only {brc['ratio']:.3f} {brc['ratio_ci']}\")\n        # per body / per group (joint, A1 and A2, CRV1) + DL across groups\n        B[\"by_body\"] = {}\n        for bd in sorted(d0.body.unique()):\n            g = zcols(d0[d0.body == bd].dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n            B[\"by_body\"][bd] = fit_A_set(g, XS_JOINT, with_A3=False)\n        B[\"by_group\"] = {}\n        for gname in GROUPS5 + [\"MATHDEC\"]:\n            g = zcols(d0[d0.group5 == gname].dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n            if g.ci.nunique() < 30:\n                continue\n            B[\"by_group\"][gname] = fit_A_set(g, XS_JOINT, with_A3=False)\n        for m in [\"A1\", \"A2\"]:\n            bs = [B[\"by_group\"][g][m][\"coef\"][\"zCONS\"][\"b\"] for g in GROUPS5 if g in B[\"by_group\"]]\n            ss = [B[\"by_group\"][g][m][\"coef\"][\"zCONS\"][\"se\"] for g in GROUPS5 if g in B[\"by_group\"]]\n            B[f\"DL_{m}_groups\"] = dersimonian_laird(bs, ss)\n        res[\"builds\"][build] = B\n        logger.info(f\"A {build} done in {(time.time() - t) / 60:.1f} min\")\n    jdump(res, RES / (\"cheng_panel_models_quick.json\" if quick else \"cheng_panel_models.json\"))\n    return res\n\n\ndef refit_nb(logger) -> None:\n    \"\"\"Re-fit A1-NB for both HOME specs and patch results/cheng_panel_models.json (used when the joint NB fit hit a\n    singular Hessian in the main S3 run).\"\"\"\n    from common import jload\n    res = jload(RES / \"cheng_panel_models.json\")\n    d0 = panel_A(\"HOME\")\n    d0 = d0[np.isfinite(d0.V_next)]\n    dj = zcols(d0.dropna(subset=[\"EMB\", \"SOC\"]), [\"CONS\", \"EMB\", \"SOC\"])\n    dc = zcols(d0, [\"CONS\"])\n    for spec, d, xs in ((\"joint\", dj, XS_JOINT), (\"cons_only\", dc, [\"zCONS\"])):\n        try:\n            res[\"builds\"][\"HOME\"][spec][\"A1_NB\"] = nb_fit(d, xs)\n        except (ValueError, np.linalg.LinAlgError) as e:\n            res[\"builds\"][\"HOME\"][spec][\"A1_NB\"] = {\"error\": repr(e)[:300]}\n        logger.info(f\"A1-NB {spec}: {res['builds']['HOME'][spec]['A1_NB']}\")\n    jdump(res, RES / \"cheng_panel_models.json\")\n\n\n# ----------------------------------------------------------------------------- test C\ndef panel_C() -> pd.DataFrame:\n    yp = pd.read_parquet(EXP11 / \"data/yearly_panel.parquet\",\n                         columns=[\"ci\", \"year\", \"t0\", \"h_end\", \"body\", \"group\", \"y_next\", \"at_risk_next\", \"deg\",\n                                  \"log1p_home\", \"log1p_all\", \"log1p_deg\", \"log_at_risk\"])\n    yp = yp[(yp.at_risk_next > 0) & (yp.deg >= 2) & yp.y_next.notna()]\n    f = pd.read_parquet(DATA / \"cheng_features.parquet\")\n    f = f[(f.body_src == \"EXP5\") & (f.build == \"HOME\")][[\"ci\", \"year\", \"CONS\"]]\n    d = yp.merge(f, on=[\"ci\", \"year\"], how=\"left\")\n    d = d[np.isfinite(d.CONS)].copy()\n    # home share from Exp11 counts_m (grounded counts per ci x year x vfield)\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\", usecols=[\"ci\", \"home\"])\n    hm = {int(r.ci): home_codes(r.home) for r in fr.itertuples()}\n    cm = pd.read_parquet(EXP11 / \"data/counts_m.parquet\")\n    cm = cm[cm.ci.isin(set(d.ci))]\n    cm[\"is_home\"] = [v in hm.get(c, ()) for c, v in zip(cm.ci.to_numpy(), cm.vfield.to_numpy())]\n    tot = cm.groupby([\"ci\", \"year\"]).n.sum().rename(\"tot\")\n    hom = cm[cm.is_home].groupby([\"ci\", \"year\"]).n.sum().rename(\"hom\")\n    hs = pd.concat([tot, hom], axis=1).fillna(0).reset_index()\n    hs[\"hshare\"] = np.where(hs.tot > 0, hs.hom / hs.tot.clip(lower=1), np.nan)\n    d = d.merge(hs[[\"ci\", \"year\", \"hshare\"]], on=[\"ci\", \"year\"], how=\"left\").merge(\n        hs[[\"ci\", \"year\", \"hshare\"]].assign(year=hs.year - 1).rename(columns={\"hshare\": \"hshare_next\"}),\n        on=[\"ci\", \"year\"], how=\"left\")\n    d[\"dHomeShare_next\"] = d.hshare_next - d.hshare\n    d[\"group5\"] = d.group.map(GROUP5)\n    return zcols(d, [\"CONS\"]).reset_index(drop=True)\n\n\nCTRL = [\"log1p_home\", \"log1p_all\", \"log1p_deg\", \"log_at_risk\"]\n\n\ndef _boot_C_worker(args) -> list[tuple[float, float]]:\n    d, cl, seeds = args\n    import pyfixest as pf\n    out = []\n    for s in seeds:\n        rng = np.random.default_rng(s)\n        pick = rng.integers(0, len(cl), len(cl))\n        rows = np.concatenate([cl[p] for p in pick])\n        newid = np.concatenate([np.full(len(cl[p]), j) for j, p in enumerate(pick)])\n        b = d.iloc[rows].copy()\n        b[\"ci\"] = newid\n        with warnings.catch_warnings():\n            warnings.simplefilter(\"ignore\")\n            try:\n                b1 = float(pf.fepois(f\"y_next ~ zCONS + {' + '.join(CTRL)} | ci + year\", data=b,\n                                     vcov=\"iid\").coef()[\"zCONS\"])\n            except (ValueError, RuntimeError, np.linalg.LinAlgError):\n                b1 = float(\"nan\")\n            bb = b.dropna(subset=[\"dHomeShare_next\"])\n            try:\n                b2 = float(pf.feols(f\"dHomeShare_next ~ zCONS + {' + '.join(CTRL)} | ci + year\", data=bb,\n                                    vcov=\"iid\").coef()[\"zCONS\"])\n            except (ValueError, RuntimeError, np.linalg.LinAlgError):\n                b2 = float(\"nan\")\n        out.append((b1, b2))\n    return out\n\n\ndef run_C(logger, quick: bool = False, workers: int = 0) -> dict:\n    W = workers or n_workers()\n    nb = 40 if quick else N_BOOT_PANEL\n    t = time.time()\n    d = panel_C()\n    if quick:\n        keep = d.ci.drop_duplicates().sample(frac=0.1, random_state=SEED)\n        d = d[d.ci.isin(keep)].reset_index(drop=True)\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_rows\": int(len(d)),\n           \"n_concepts\": int(d.ci.nunique()),\n           \"C1\": fepois(d, \"y_next\", [\"zCONS\"] + CTRL, \"ci + year\"),\n           \"C2\": feols(d.dropna(subset=[\"dHomeShare_next\"]), \"dHomeShare_next\", [\"zCONS\"] + CTRL, \"ci + year\"),\n           \"C1_by_body\": {}, \"C2_by_body\": {}}\n    for bd in sorted(d.body.unique()):\n        g = d[d.body == bd]\n        res[\"C1_by_body\"][bd] = fepois(g, \"y_next\", [\"zCONS\"] + CTRL, \"ci + year\")\n        res[\"C2_by_body\"][bd] = feols(g.dropna(subset=[\"dHomeShare_next\"]), \"dHomeShare_next\", [\"zCONS\"] + CTRL,\n                                      \"ci + year\")\n    logger.info(f\"C1 {res['C1']['coef']['zCONS']}  C2 {res['C2']['coef']['zCONS']}  ({time.time() - t:.0f}s)\")\n    cl = cluster_index(d.ci.to_numpy())\n    seeds = [SEED + 500 + k for k in range(nb)]\n    parts = [seeds[i::W] for i in range(W)]\n    out = []\n    t = time.time()\n    with ProcessPoolExecutor(max_workers=W, mp_context=mp.get_context(\"spawn\")) as ex:\n        for r in ex.map(_boot_C_worker, [(d, cl, p) for p in parts]):\n            out.extend(r)\n    B = np.array(out)\n    for j, k in enumerate([\"C1\", \"C2\"]):\n        v = B[:, j]\n        v = v[np.isfinite(v)]\n        res[k][\"boot\"] = {\"n_boot\": int(len(v)), \"ci\": np.percentile(v, [2.5, 97.5]).tolist(),\n                          \"p_one_lt_0\": float((np.sum(v >= 0) + 1) / (len(v) + 1))}\n    logger.info(f\"C bootstrap {nb} draws in {(time.time() - t) / 60:.1f} min: C1 {res['C1']['boot']} \"\n                f\"C2 {res['C2']['boot']}\")\n    jdump(res, RES / (\"panel_C_quick.json\" if quick else \"panel_C.json\"))\n    return res", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [15] TOOL CALL — Bash · 2026-09-29 11:29:24 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $A/lib/static_cheng.py
```

### [16] TOOL RESULT — Bash · 2026-09-29 11:29:24 UTC

```
{"stdout": "\"\"\"S4 (test B: static early trait vs reach / depth), S6 (test D: Palla size x turnover), S7 (test E: coupling).\n\npsp = partial Spearman = Pearson(resid(rank x | Z), resid(rank y | Z)), Z = [1, rank(B5), dummies]; ranks and the\nresidualisation are recomputed inside every concept-bootstrap draw (EXP8 rq1stats.psp_point logic). Several x / y\ncolumns share one draw (same resampled concepts), so paired differences use the SAME draws on a common complete-case\nset. Covariates: B5 + onset-year dummies; + 8-group dummies when groups are pooled; + body dummies when bodies are\npooled; + window_flag for the 2015-17 cohort (EXP10 R0). All tables: selection data, not confirmation.\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport multiprocessing as mp\nimport time\nfrom concurrent.futures import ProcessPoolExecutor\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\nfrom common import (B5, BODY_COHORT, DATA, DEPTH, EXP8, EXP10, GROUP5, GROUPS5, N_BOOT_STATIC, REACH, RES, SEED,\n                    SELECTION_LABEL, body_of_split, jdump, n_workers)\nfrom rq1stats import dersimonian_laird\n\nOUTS = REACH + DEPTH\nTRAITS2 = [\"EMB_early_home\", \"SOC_early_home\", \"CONS_early_all\", \"CONS_r_early_home\", \"EMB_cos_early_home\"]\nPRIMARY = \"EXP5_pooled\"\n\n\n# ----------------------------------------------------------------------------- data\ndef static_frame() -> pd.DataFrame:\n    st = pd.read_parquet(DATA / \"cheng_static.parquet\")\n    a5 = pd.read_parquet(EXP8 / \"data/analysis_table.parquet\",\n                         columns=[\"ci\", \"t0\", \"group\", \"split\", \"name\"] + B5 + OUTS)\n    a5[\"body\"] = a5.split.map(body_of_split)\n    a5[\"window_flag\"] = 0\n    V = pd.read_parquet(DATA / \"V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    a5 = a5.merge(V.rename(columns={\"year\": \"y2\", \"V\": \"V_t0p2\"}).assign(y2=lambda x: x.y2), how=\"left\",\n                  left_on=[\"ci\", a5.t0 + 2], right_on=[\"ci\", \"y2\"]).drop(columns=[\"y2\"])\n    a5 = a5.merge(V.rename(columns={\"year\": \"y3\", \"V\": \"V_t0p3\"}), how=\"left\",\n                  left_on=[\"ci\", a5.t0 + 3], right_on=[\"ci\", \"y3\"]).drop(columns=[\"y3\"])\n    a5 = a5.drop(columns=[c for c in a5.columns if c.startswith(\"key_\")])\n    ac = pd.read_parquet(EXP10 / \"data/analysis_cohort.parquet\")\n    ac[\"body\"] = BODY_COHORT\n    ac[\"split\"] = \"COHORT_2015_17\"\n    vc = pd.read_parquet(DATA / \"V_cohort.parquet\", columns=[\"ci\", \"V_t0p2\", \"V_t0p3\"])\n    ac = ac.merge(vc, on=\"ci\", how=\"left\")\n    keep = [\"ci\", \"t0\", \"group\", \"split\", \"name\", \"body\", \"window_flag\", \"V_t0p2\", \"V_t0p3\"] + B5 + OUTS\n    extra = [\"CONTACT_REACH\", \"type\", \"generic\", \"level\", \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\",\n             \"newborn\", \"label_coverage_early\", \"home_coverage_early\", \"agroup\"]\n    df = pd.concat([a5[keep], ac[keep + extra]], ignore_index=True)\n    s = st.drop(columns=[\"body\", \"t0\", \"group\"])\n    df = df.merge(s, on=\"ci\", how=\"left\", suffixes=(\"\", \"_st\"))\n    df[\"group5\"] = df.group.map(GROUP5)\n    df[\"logV_t0p2\"] = np.log1p(df.V_t0p2)\n    return df\n\n\ndef body_frames(df: pd.DataFrame) -> dict[str, pd.DataFrame]:\n    out = {PRIMARY: df[df.body != BODY_COHORT]}\n    for b in [\"DEV\", \"OLD_HELDOUT\", \"COHORT_2010_14\", BODY_COHORT]:\n        out[b] = df[df.body == b]\n    return out\n\n\ndef dummies(v: np.ndarray) -> np.ndarray:\n    u = np.unique(v)\n    if len(u) <= 1:\n        return np.zeros((len(v), 0))\n    return (v[:, None] == u[None, 1:]).astype(float)\n\n\ndef design(d: pd.DataFrame, cont: list[str] | None = None, groups: bool = True) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"(continuous covariates to be ranked, raw dummy matrix).\"\"\"\n    cont = B5 if cont is None else cont\n    cat = [dummies(d.t0.to_numpy())]\n    if groups:\n        cat.append(dummies(d.group.astype(str).to_numpy()))\n    cat.append(dummies(d.body.astype(str).to_numpy()))\n    if d.window_flag.nunique() > 1:\n        cat.append(d[[\"window_flag\"]].to_numpy(float))\n    return d[cont].to_numpy(float), np.hstack(cat)\n\n\n# ----------------------------------------------------------------------------- multi-psp bootstrap engine\ndef _resid_corr(xr: np.ndarray, yr: np.ndarray, Br: np.ndarray, C: np.ndarray) -> np.ndarray:\n    Z = np.hstack([np.ones((len(xr), 1)), Br, C])\n    Yall = np.hstack([xr, yr])\n    beta, *_ = np.linalg.lstsq(Z, Yall, rcond=None)\n    R = Yall - Z @ beta\n    R -= R.mean(0)\n    s = R.std(0)\n    s[s < 1e-12] = np.nan\n    R /= s\n    nx = xr.shape[1]\n    return (R[:, :nx].T @ R[:, nx:]) / len(R)                      # [nx, ny] Pearson of residuals\n\n\ndef psp_multi(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray) -> np.ndarray:\n    Br = rankdata(B, axis=0) if B.shape[1] else np.zeros((len(X), 0))\n    return _resid_corr(rankdata(X, axis=0), rankdata(Y, axis=0), Br, C)\n\n\ndef unique_ids(M: np.ndarray) -> list[tuple[np.ndarray, int]]:\n    \"\"\"Per column: ids of the value-sorted unique values (so ranks of any resample follow from bincounts).\"\"\"\n    out = []\n    for j in range(M.shape[1]):\n        _, inv = np.unique(M[:, j], return_inverse=True)\n        out.append((inv.astype(np.int64), int(inv.max()) + 1))\n    return out\n\n\ndef resample_ranks(uids: list[tuple[np.ndarray, int]], idx: np.ndarray) -> np.ndarray:\n    \"\"\"Average ranks (identical to scipy rankdata 'average') of every column within the resample idx, scaled by\n    1/n. For unique value k with c_k copies: rank = cumsum(c)_k - (c_k - 1)/2. No sort needed.\"\"\"\n    n = len(idx)\n    R = np.empty((n, len(uids)))\n    for j, (u, U) in enumerate(uids):\n        ui = u[idx]\n        c = np.bincount(ui, minlength=U)\n        avg = np.cumsum(c) - (c - 1) / 2.0\n        R[:, j] = avg[ui] / n\n    return R\n\n\ndef fast_corr(RX: np.ndarray, RY: np.ndarray, RB: np.ndarray, C: np.ndarray) -> np.ndarray:\n    \"\"\"Residual-correlation matrix via the pseudo-inverse of Z'Z (min-norm LS; exact projection even when the\n    dummy block is rank deficient).\"\"\"\n    Z = np.hstack([np.ones((len(RX), 1)), RB, C])\n    V = np.hstack([RX, RY])\n    ZtZ = Z.T @ Z\n    beta = np.linalg.pinv(ZtZ, rcond=1e-12, hermitian=True) @ (Z.T @ V)\n    R = V - Z @ beta\n    R -= R.mean(0)\n    s = R.std(0)\n    s[s < 1e-12] = np.nan\n    R /= s\n    nx = RX.shape[1]\n    return (R[:, :nx].T @ R[:, nx:]) / len(R)\n\n\ndef multi_boot(X: np.ndarray, Y: np.ndarray, B: np.ndarray, C: np.ndarray, n_boot: int, seed: int,\n               check: bool = True) -> dict:\n    ok = np.all(np.isfinite(X), 1) & np.all(np.isfinite(Y), 1) & np.all(np.isfinite(B), 1)\n    X, Y, B, C = X[ok], Y[ok], B[ok], C[ok]\n    n = len(X)\n    if n < 30:\n        return {\"n\": n, \"est\": np.full((X.shape[1], Y.shape[1]), np.nan), \"boot\": np.zeros((0, X.shape[1], Y.shape[1]))}\n    keep = C.std(0) > 0\n    est = psp_multi(X, Y, B, C[:, keep])                           # exact path (lstsq, scipy rankdata)\n    ux, uy, ub = unique_ids(X), unique_ids(Y), unique_ids(B)\n    rng = np.random.default_rng(seed)\n    bs = np.empty((n_boot, X.shape[1], Y.shape[1]))\n    max_dev = 0.0\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        bs[b] = fast_corr(resample_ranks(ux, i), resample_ranks(uy, i), resample_ranks(ub, i), C[i])\n        if check and b < 2:                                         # fast path == exact path on the first draws\n            Ci = C[i]\n            ex = psp_multi(X[i], Y[i], B[i], Ci[:, Ci.std(0) > 0])\n            max_dev = max(max_dev, float(np.nanmax(np.abs(ex - bs[b]))))\n    if max_dev > 1e-8:\n        raise ValueError(f\"fast bootstrap path deviates from exact psp by {max_dev:.2e}\")\n    return {\"n\": n, \"est\": est, \"boot\": bs, \"fast_path_max_dev\": max_dev}\n\n\ndef summ(est: float, bs: np.ndarray, direction: int = -1) -> dict:\n    bs = bs[np.isfinite(bs)]\n    if not len(bs) or not np.isfinite(est):\n        return {\"rho\": None, \"ci\": [None, None], \"se\": None}\n    lo, hi = np.percentile(bs, [2.5, 97.5])\n    return {\"rho\": float(est), \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"p_one_pred\": float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1)),\n            \"p_two\": float(min(1.0, 2 * min((np.sum(bs <= 0) + 1) / (len(bs) + 1), (np.sum(bs >= 0) + 1) / (len(bs) + 1)))),\n            \"n_boot\": int(len(bs))}\n\n\ndef task_trait(args) -> dict:\n    \"\"\"One trait x one body: depth set (O1c, O1b, O3 own complete cases) and reach set (O2r_* complete cases, with\n    the depth outcomes on the SAME rows for the paired differences).\"\"\"\n    name, d, x, n_boot, seed, groups = args\n    out = {\"task\": name, \"x\": x, \"n_body\": int(len(d))}\n    B, C = design(d, groups=groups)\n    xv = d[[x]].to_numpy(float)\n    r1 = multi_boot(xv, d[DEPTH].to_numpy(float), B, C, n_boot, seed)\n    r2 = multi_boot(xv, d[REACH + DEPTH].to_numpy(float), B, C, n_boot, seed + 1)\n    res = {}\n    for j, y in enumerate(DEPTH):\n        res[y] = summ(r1[\"est\"][0, j], r1[\"boot\"][:, 0, j], direction=-1 if y == \"O3\" else 1)\n        res[y][\"n\"] = r1[\"n\"]\n    for j, y in enumerate(REACH):\n        res[y] = summ(r2[\"est\"][0, j], r2[\"boot\"][:, 0, j], direction=-1)\n        res[y][\"n\"] = r2[\"n\"]\n    diffs = {}\n    for a, b in [(\"O1c\", \"O2r_m50\"), (\"O1b\", \"O2r_m50\"), (\"O1c\", \"O2r_resid\"), (\"O3\", \"O2r_m50\")]:\n        ia, ib = (REACH + DEPTH).index(a), (REACH + DEPTH).index(b)\n        e = r2[\"est\"][0, ia] - r2[\"est\"][0, ib]\n        bs = r2[\"boot\"][:, 0, ia] - r2[\"boot\"][:, 0, ib]\n        diffs[f\"{a}-{b}\"] = summ(e, bs, direction=1)\n        diffs[f\"{a}-{b}\"][\"n_common\"] = r2[\"n\"]\n        diffs[f\"{a}-{b}\"][\"psp_a_common\"] = float(r2[\"est\"][0, ia])\n        diffs[f\"{a}-{b}\"][\"psp_b_common\"] = float(r2[\"est\"][0, ib])\n    out.update({\"psp\": res, \"paired_diff\": diffs})\n    return out\n\n\ndef task_volume(args) -> dict:\n    name, d, x, n_boot, seed = args\n    xv, v3, v2 = d[x].to_numpy(float), d.V_t0p3.to_numpy(float), d.logV_t0p2.to_numpy(float)\n    ok = np.isfinite(xv) & np.isfinite(v3) & np.isfinite(v2)\n    xv, v3, v2 = xv[ok], v3[ok], v2[ok]\n    n = len(xv)\n    out = {\"task\": name, \"x\": x, \"n\": int(n)}\n    if n < 30:\n        return out\n    rng = np.random.default_rng(seed)\n    body_c = dummies(d.body.astype(str).to_numpy()[ok])\n    Zc = np.hstack([v2[:, None], body_c])\n    raw = float(stats.spearmanr(xv, v3)[0])\n    ps = float(_resid_corr(rankdata(xv)[:, None], rankdata(v3)[:, None], rankdata(v2)[:, None], body_c)[0, 0])\n    Bb, Cb = design(d[ok])\n    ok5 = np.all(np.isfinite(Bb), 1)                               # B5 variant: complete B5 rows only\n    x5, y5, Bb, Cb = xv[ok5], v3[ok5], Bb[ok5], Cb[ok5]\n    n5 = len(x5)\n    ps5 = float(psp_multi(x5[:, None], y5[:, None], Bb, Cb[:, Cb.std(0) > 0])[0, 0])\n    br, bp, bp5 = np.empty(n_boot), np.empty(n_boot), np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        br[b] = stats.spearmanr(xv[i], v3[i])[0]\n        k = body_c[i].std(0) > 0\n        bp[b] = _resid_corr(rankdata(xv[i])[:, None], rankdata(v3[i])[:, None], rankdata(v2[i])[:, None],\n                            body_c[i][:, k])[0, 0]\n        j = rng.integers(0, n5, n5)\n        Ci = Cb[j]\n        bp5[b] = psp_multi(x5[j][:, None], y5[j][:, None], Bb[j], Ci[:, Ci.std(0) > 0])[0, 0]\n    out[\"n_B5_variant\"] = int(n5)\n    out[\"B_raw_spearman_V_t0p3\"] = summ(raw, br, direction=1)\n    out[\"B_size_psp_V_t0p3_given_logV_t0p2\"] = summ(ps, bp, direction=1)\n    out[\"B_size_psp_V_t0p3_given_B5_dummies\"] = summ(ps5, bp5, direction=1)\n    return out\n\n\ndef run_tasks(tasks: list, fn, workers: int) -> list[dict]:\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\")) as ex:\n        return list(ex.map(fn, tasks))\n\n\ndef mde(se: float | None) -> float | None:\n    return 2.8 * se if se else None\n\n\n# ----------------------------------------------------------------------------- test B\ndef run_B(logger, quick: bool = False) -> dict:\n    t = time.time()\n    W = n_workers()\n    nb = 100 if quick else N_BOOT_STATIC\n    nb2 = 60 if quick else 500\n    nbg = 100 if quick else 1000\n    df = static_frame()\n    df.to_parquet(DATA / \"static_analysis_table.parquet\", index=False)\n    bodies = body_frames(df)\n    tasks_t, tasks_v = [], []\n    for bi, (bn, d) in enumerate(bodies.items()):\n        tasks_t.append((f\"{bn}|CONS_early_home\", d, \"CONS_early_home\", nb, SEED + 10 * bi, True))\n        tasks_v.append((f\"{bn}|volume\", d, \"CONS_early_home\", nb, SEED + 10 * bi + 5))\n        for k, x in enumerate(TRAITS2):\n            tasks_t.append((f\"{bn}|{x}\", d, x, nb2, SEED + 1000 + 10 * bi + k, True))\n        tasks_v.append((f\"{bn}|volume_all\", d, \"CONS_early_all\", nb2, SEED + 2000 + 10 * bi))\n    # per group within PRIMARY and within the 2015-17 cohort\n    for bn in [PRIMARY, BODY_COHORT]:\n        d = bodies[bn]\n        for gi, g in enumerate(GROUPS5 + [\"MATHDEC\"]):\n            dg = d[d.group5 == g]\n            if len(dg) >= 40:\n                tasks_t.append((f\"{bn}|group={g}|CONS_early_home\", dg, \"CONS_early_home\", nbg, SEED + 3000 + gi,\n                                True))\n    logger.info(f\"B: {len(tasks_t)} trait tasks + {len(tasks_v)} volume tasks on {W} workers\")\n    rt = run_tasks(tasks_t, task_trait, W)\n    rv = run_tasks(tasks_v, task_volume, W)\n    res = {\"label\": SELECTION_LABEL, \"resampling_unit\": \"concept\", \"n_boot_primary\": nb, \"n_boot_secondary\": nb2,\n           \"n_boot_group\": nbg, \"covariates\": \"rank(B5) + onset-year dummies + 8-group dummies + body dummies \"\n           \"(pooled) + window_flag (2015-17 cohort)\", \"primary_body\": PRIMARY, \"replication_body\": BODY_COHORT,\n           \"EMB_note\": \"EMB_* = analogue (backbone PMI), not Cheng's word2vec measure\",\n           \"trait\": {r[\"task\"]: r for r in rt}, \"volume\": {r[\"task\"]: r for r in rv}}\n    # DL over groups (primary trait) for each outcome and the paired diffs\n    res[\"DL\"] = {}\n    for bn in [PRIMARY, BODY_COHORT]:\n        res[\"DL\"][bn] = {}\n        keys = OUTS + [\"O1c-O2r_m50\", \"O1c-O2r_resid\"]\n        for y in keys:\n            bs, ss, per = [], [], {}\n            for g in GROUPS5:\n                r = res[\"trait\"].get(f\"{bn}|group={g}|CONS_early_home\")\n                if r is None:\n                    continue\n                v = r[\"psp\"][y] if y in r[\"psp\"] else r[\"paired_diff\"][y]\n                per[g] = {\"rho\": v[\"rho\"], \"ci\": v[\"ci\"], \"n\": v.get(\"n\", v.get(\"n_common\"))}\n                bs.append(v[\"rho\"] if v[\"rho\"] is not None else np.nan)\n                ss.append(v[\"se\"] if v[\"se\"] is not None else np.nan)\n            dl = dersimonian_laird(bs, ss)\n            dl[\"n_negative\"] = int(sum(1 for b in bs if np.isfinite(b) and b < 0))\n            dl[\"n_positive\"] = int(sum(1 for b in bs if np.isfinite(b) and b > 0))\n            dl[\"per_group\"] = per\n            m = res[\"trait\"].get(f\"{bn}|group=MATHDEC|CONS_early_home\")\n            if m is not None:\n                dl[\"MATHDEC_report_only\"] = (m[\"psp\"][y] if y in m[\"psp\"] else m[\"paired_diff\"][y])[\"rho\"]\n            res[\"DL\"][bn][y] = dl\n    # cohort rungs R2 / R3 (EXP10 ladder)\n    try:\n        import ladder\n        dc = bodies[BODY_COHORT].copy()\n        res[\"cohort_rungs\"] = {}\n        for rung in [\"R2\", \"R3\"]:\n            for y in [\"O2r_m50\", \"O2r_resid\", \"O1c\", \"O3\"]:\n                r = ladder.psp_df(dc, \"CONS_early_home\", y, rung, 200 if quick else 1000, SEED + 4000,\n                                  direction=1 if y == \"O1c\" else -1)\n                r.pop(\"boot\", None)\n                res[\"cohort_rungs\"][f\"{rung}|{y}\"] = r\n    except (ImportError, KeyError, ValueError) as e:\n        res[\"cohort_rungs\"] = {\"error\": repr(e)[:300]}\n    # cohort MDE for the P3 test\n    c = res[\"trait\"][f\"{BODY_COHORT}|CONS_early_home\"][\"psp\"][\"O2r_m50\"]\n    res[\"cohort_MDE_O2r_m50\"] = {\"n\": c.get(\"n\"), \"se\": c.get(\"se\"), \"MDE_2.8SE\": mde(c.get(\"se\"))}\n    jdump(res, RES / (\"cheng_static_quick.json\" if quick else \"cheng_static.json\"))\n    p = res[\"trait\"][f\"{PRIMARY}|CONS_early_home\"]\n    logger.info(f\"B primary: \" + \", \".join(f\"{y} {p['psp'][y]['rho']:+.3f} {np.round(p['psp'][y]['ci'], 3)}\"\n                                          for y in OUTS))\n    logger.info(f\"B primary diff O1c-O2r_m50 {p['paired_diff']['O1c-O2r_m50']}\")\n    logger.info(f\"B volume primary {res['volume'][f'{PRIMARY}|volume']}\")\n    logger.info(f\"S4 done in {(time.time() - t) / 60:.1f} min\")\n    return res\n\n\n# ----------------------------------------------------------------------------- test D (Palla)\ndef cr(v: np.ndarray) -> np.ndarray:\n    r = rankdata(v) / len(v)\n    return r - r.mean()\n\n\ndef palla_fit(d: pd.DataFrame, y: str, i: np.ndarray | None = None) -> float:\n    x, s, yy = d.CONS_early_home.to_numpy(float), d.logvol.to_numpy(float), d[y].to_numpy(float)\n    other = d[[\"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]].to_numpy(float)\n    _, C = design(d)\n    if i is not None:\n        x, s, yy, other, C = x[i], s[i], yy[i], other[i], C[i]\n    C = C[:, C.std(0) > 0]\n    rx, rs = cr(x), cr(s)\n    Z = np.column_stack([np.ones(len(x)), rx, rs, rx * rs, rankdata(other, axis=0) / len(x), C])\n    beta, *_ = np.linalg.lstsq(Z, cr(yy), rcond=None)\n    return float(beta[3]), float(beta[1])\n\n\ndef task_palla(args) -> dict:\n    name, d, y, n_boot, seed = args\n    d = d[np.isfinite(d.CONS_early_home) & np.isfinite(d[y]) & d[B5].notna().all(1)].reset_index(drop=True)\n    n = len(d)\n    est, main = palla_fit(d, y)\n    rng = np.random.default_rng(seed)\n    bs = np.array([palla_fit(d, y, rng.integers(0, n, n)) for _ in range(n_boot)])\n    out = {\"task\": name, \"y\": y, \"n\": n, \"interaction\": summ(est, bs[:, 0], direction=1),\n           \"main_rank_CONS\": summ(main, bs[:, 1], direction=-1)}\n    # psp by early-size tercile\n    q = np.quantile(d.logvol, [1 / 3, 2 / 3])\n    terc = np.digitize(d.logvol, q)\n    out[\"by_size_tercile\"] = {}\n    for k, lab in enumerate([\"small\", \"medium\", \"large\"]):\n        dk = d[terc == k]\n        B, C = design(dk)\n        r = multi_boot(dk[[\"CONS_early_home\"]].to_numpy(float), dk[[y]].to_numpy(float), B, C, n_boot, seed + 7 + k)\n        out[\"by_size_tercile\"][lab] = {**summ(r[\"est\"][0, 0], r[\"boot\"][:, 0, 0]), \"n\": r[\"n\"],\n                                       \"logvol_range\": [float(dk.logvol.min()), float(dk.logvol.max())]}\n    return out\n\n\ndef run_D(logger, quick: bool = False) -> dict:\n    df = pd.read_parquet(DATA / \"static_analysis_table.parquet\")\n    bodies = body_frames(df)\n    nb = 100 if quick else 1000\n    tasks = [(f\"{bn}|{y}\", bodies[bn], y, nb, SEED + 5000 + 10 * k + j)\n             for k, bn in enumerate([PRIMARY, BODY_COHORT]) for j, y in enumerate([\"O3\", \"O2r_m50\", \"O1c\"])]\n    rs = run_tasks(tasks, task_palla, n_workers())\n    res = {\"label\": SELECTION_LABEL, \"model\": \"OLS on centred ranks/n: rank O ~ rank CONS_early + rank logvol + \"\n           \"product + rank(other B5) + onset-year/group/body dummies; concept bootstrap\",\n           \"palla_prediction\": \"interaction on O3 (transience) > 0: stability helps small concepts survive, turnover \"\n           \"helps large ones\", \"results\": {r[\"task\"]: r for r in rs}}\n    jdump(res, RES / (\"palla_quick.json\" if quick else \"palla.json\"))\n    for r in rs:\n        logger.info(f\"D {r['task']}: interaction {r['interaction']['rho']:+.4f} {r['interaction']['ci']}\")\n    return res\n\n\n# ----------------------------------------------------------------------------- test E (coupling)\ndef task_coupling(args) -> dict:\n    name, d, n_boot, seed = args\n    B, C = design(d)\n    X = d[[\"CONS_early_all\", \"CONS_early_home\"]].to_numpy(float)\n    out = {\"task\": name}\n    for tag, ys in ((\"reach_set\", [\"O2r_m50\", \"O1c\"]), (\"full_set\", [\"O1c\"])):\n        r = multi_boot(X, d[ys].to_numpy(float), B, C, n_boot, seed)\n        for j, y in enumerate(ys):\n            e = r[\"est\"][0, j] - r[\"est\"][1, j]\n            bs = r[\"boot\"][:, 0, j] - r[\"boot\"][:, 1, j]\n            out[f\"{tag}|{y}\"] = {\"n_common\": r[\"n\"], \"psp_all\": float(r[\"est\"][0, j]),\n                                 \"psp_home\": float(r[\"est\"][1, j]), \"diff_all_minus_home\": summ(e, bs, direction=1)}\n    return out\n\n\ndef run_E(logger, quick: bool = False) -> dict:\n    df = pd.read_parquet(DATA / \"static_analysis_table.parquet\")\n    bodies = body_frames(df)\n    nb = 100 if quick else N_BOOT_STATIC\n    tasks = [(bn, bodies[bn], nb, SEED + 6000 + k) for k, bn in enumerate([PRIMARY, BODY_COHORT, \"DEV\",\n                                                                          \"OLD_HELDOUT\", \"COHORT_2010_14\"])]\n    rs = run_tasks(tasks, task_coupling, n_workers())\n    res = {\"label\": SELECTION_LABEL, \"test\": \"paired concept bootstrap psp(CONS_early_all) - psp(CONS_early_home), \"\n           \"common complete-case set\", \"results\": {r[\"task\"]: r for r in rs}}\n    jdump(res, RES / (\"coupling_quick.json\" if quick else \"coupling.json\"))\n    for r in rs:\n        logger.info(f\"E {r['task']}: \" + \"; \".join(f\"{k} {v['diff_all_minus_home']['rho']:+.3f} \"\n                                                  f\"{np.round(v['diff_all_minus_home']['ci'], 3)}\"\n                                                  for k, v in r.items() if k != \"task\"))\n    return res", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-09-29 11:29:40 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop; ls $R/iter_4/gen_art/gen_art_experiment_11/data | head; ls $R/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long | head -3; du -sh $R/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long $R/iter_4/gen_art/gen_art_experiment_11/inputs; ls $R/iter_3/gen_art/gen_art_experiment_8/data/analysis_table.parquet; A=$R/iter_5/gen_art/gen_art_experiment_14; cat $A/lib/rq1stats.py | sed -n 1,80p | grep -n "def dersimonian" -A30; which python3; python3 -c "import pandas, pyarrow, scipy, pyfixest; print('ok')"; ls $A/.venv 2>&1 | head -2; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/.shared_cache | head
```

### [18] TOOL RESULT — Bash · 2026-09-29 11:29:40 UTC

```
{"stdout": "bg_topics.npz\nboot_fe_DEV.parquet\nbridging_papers.parquet\nclosure_jumps.parquet\ncounts_m.parquet\nd3_concept_year.parquet\nframe_matches_long\ngrounded_V.npz\npartner_indicators.parquet\npassM_info.json\npart_001.parquet\npart_002.parquet\npart_003.parquet\n126M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/data/frame_matches_long\n24M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_11/inputs\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/analysis_table.parquet\n/usr/local/bin/python3\nTraceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'pyfixest'\nls: cannot access '/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/.venv': No such file or directory\nhf\npip\nuv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] ASSISTANT · 2026-09-29 11:29:44 UTC

```
Reading the pipeline's library modules to decide which pieces the notebook can reproduce from a small data subset.
```

### [20] TOOL CALL — Bash · 2026-09-29 11:29:44 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; grep -n "def dersimonian" -A35 $A/lib/rq1stats.py; cat $A/lib/ego_ctx.py; grep -n "def self_topics\|def set_context\|def slice_of" -A25 $A/lib/ego.py | head -90; python3 -c "import pandas,pyarrow,scipy,statsmodels;print(pandas.__version__)"
```

### [21] TOOL RESULT — Bash [ERROR] · 2026-09-29 11:29:46 UTC

```
Error: Exit code 1
163:def dersimonian_laird(b, se) -> dict:
164-    """EXP6 lib/stats_core.dersimonian_laird (verbatim logic)."""
165-    b, se = np.asarray(b, float), np.asarray(se, float)
166-    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)
167-    b, se = b[ok], se[ok]
168-    k = len(b)
169-    if k == 0:
170-        return {"k": 0, "b": float("nan"), "se": float("nan"), "ci": [float("nan")] * 2, "p": float("nan"),
171-                "tau2": float("nan"), "I2": float("nan"), "Q": float("nan")}
172-    w = 1 / se**2
173-    bf = (w * b).sum() / w.sum()
174-    Q = float((w * (b - bf) ** 2).sum())
175-    Cc = w.sum() - (w**2).sum() / w.sum()
176-    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 and Cc > 0 else 0.0
177-    ws = 1 / (se**2 + tau2)
178-    bre = (ws * b).sum() / ws.sum()
179-    sre = math.sqrt(1 / ws.sum())
180-    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0
181-    return {"k": k, "b": float(bre), "se": sre, "ci": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],
182-            "p": float(2 * stats.norm.sf(abs(bre / sre))), "tau2": float(tau2), "Q": Q, "I2": float(I2)}
183-
184-
185-def holm(p: list[float]) -> list[float]:
186-    p = np.asarray(p, float)
187-    out = np.full(len(p), np.nan)
188-    ok = np.isfinite(p)
189-    idx = np.nonzero(ok)[0]
190-    m = len(idx)
191-    order = idx[np.argsort(p[idx])]
192-    run = 0.0
193-    for r, i in enumerate(order):
194-        run = max(run, min(1.0, (m - r) * p[i]))
195-        out[i] = run
196-    return out.tolist()
197-
198-
"""Context for lib/ego.py: EXP3 Leiden-gamma-3 topic backbones (slices 2000-04/05-09/10-14), topic metadata,
content lemmas (verbatim from EXP3 common.py), and the Pass A full-corpus topic background."""
from __future__ import annotations

import json
import re
from collections import Counter
from functools import lru_cache

import numpy as np
import pandas as pd

from common import DATA, INPUTS

_STOP = set("a an and are as at be but by for if in into is it no not of on or such that the their then there these "
            "they this to was will with its via from using based".split())
_TOK = re.compile(r"[^\W_]+", re.UNICODE)


@lru_cache(maxsize=None)
def _stemmer():
    import snowballstemmer
    return snowballstemmer.stemmer("porter")


def lemmas(text: str) -> set[str]:
    t = re.sub(r"[\-‐-—/]", " ", str(text).lower())
    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}


def topic_lemma_df(names: list[str]) -> Counter:
    df = Counter()
    for n in names:
        df.update(lemmas(n))
    return df


def backbone_context() -> dict:
    tids = json.loads((INPUTS / "topic_ids.json").read_text())
    tm = pd.read_csv(INPUTS / "topic_meta.csv").set_index("topic").loc[tids]
    sl = [np.load(INPUTS / "backbone" / f"slice{s}.npz") for s in range(3)]
    names = tm.name.tolist()
    return dict(nt=len(tids), comm=[z["comm"] for z in sl], comm_q=[z["comm_q"] for z in sl],
                deg=[z["deg"] for z in sl], knn=[(z["ka"], z["kb"]) for z in sl],
                full_edges=[(z["a"], z["b"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,
                ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names], lemmas=lemmas)


def rq1_context() -> dict:
    ctx = backbone_context()
    z = np.load(DATA / "bg_topics.npz")
    years = z["years"].tolist()
    ctx.update(years=years, bg=z["BG"], Gt=dict(zip(years, z["GT"].tolist())))
    return ctx
30:def slice_of(y: int) -> int:
31-    for i, (a, b) in enumerate(SLICES):
32-        if a <= y <= b:
33-            return i
34-    return 0 if y < SLICES[0][0] else len(SLICES) - 1
35-
36-
37-def rq1_windows(t0: int) -> dict[str, list[int]]:
38-    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0], "W2": [t0 + 1], "W3": [t0 + 2]}
39-
40-
41-def exp3_windows(t0: int) -> dict[str, list[int]]:
42-    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0, t0 + 1], "W2": [t0 + 2], "W3": [t0 + 3, t0 + 4]}
43-
44-
45-def lgC(n: float, k: float) -> float:
46-    from scipy.special import gammaln
47-    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)
48-
49-
50:def set_context(ctx: dict) -> None:
51-    """ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,
52-    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable)."""
53-    C.clear()
54-    C.update(ctx)
55-    C["graphs"] = {}
56-    C["yidx"] = {y: i for i, y in enumerate(ctx["years"])}
57-
58-
59-def knn_graph(s: int) -> ig.Graph:
60-    if s not in C["graphs"]:
61-        ka, kb = C["knn"][s]
62-        C["graphs"][s] = ig.Graph(n=C["nt"], edges=list(zip(ka.tolist(), kb.tolist())), directed=False)
63-    return C["graphs"][s]
64-
65-
66-def bg_window(years: list[int]) -> tuple[np.ndarray, float]:
67-    yi = [C["yidx"][y] for y in years if y in C["yidx"]]
68-    return C["bg"][yi].sum(axis=0).astype(float), float(sum(C["Gt"].get(y, 0) for y in years))
69-
70-
71-def window_counts(works, years) -> tuple[np.ndarray, int]:
72-    nck = np.zeros(C["nt"], dtype=float)
73-    ncw = 0
74-    ys = set(years)
75-    for y, tp in works:
--
104:def self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:
105-    lem = C["lemmas"]
106-    sets = []
107-    for ph in [name] + aliases:
108-        cl = {l for l in lem(ph) if C["ldf"].get(l, 0) <= SELF_DF_MAX}
109-        if cl:
110-            sets.append(cl)
111-    lex = np.array([any(cl <= tl for cl in sets) for tl in C["tlem"]])
112-    share = n_early / nc_early if nc_early else np.zeros(C["nt"])
113-    return lex | (share >= SELF_SHARE)
114-
115-
116-def distinct_null(pool_idx, w, M, labels, rng, n):
117-    if M <= 0 or len(pool_idx) == 0:
118-        return np.zeros(n)
119-    M = min(M, len(pool_idx))
120-    lw = np.log(w[pool_idx])
121-    out = np.empty(n)
122-    lab = labels[pool_idx]
123-    chunk = max(1, 2_000_000 // len(pool_idx))
124-    for s in range(0, n, chunk):
125-        m = min(chunk, n - s)
126-        g = lw[None, :] + rng.gumbel(size=(m, len(pool_idx)))
127-        top = np.argpartition(-g, M - 1, axis=1)[:, :M]
128-        L = np.sort(lab[top], axis=1)
129-        out[s:s + m] = 1 + (np.diff(L, axis=1) != 0).sum(axis=1)
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'statsmodels'
```

### [22] TOOL CALL — Bash · 2026-09-29 11:30:02 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; cat $A/results/headline_numbers.json; grep -n "def \|verdict\|SIZE-DOM\|REVERSAL" $A/lib/outputs.py | head -60; sed -n 1,40p $A/lib/ego.py; python3 -c "import igraph, snowballstemmer" 
```

### [23] TOOL RESULT — Bash [ERROR] · 2026-09-29 11:30:02 UTC

```
Error: Exit code 1
{
 "label": "selection data, not confirmation",
 "numbers": {
  "cheng_panel_models.json:builds.HOME.joint.A1.n_concepts": 12311,
  "cheng_panel_models.json:builds.HOME.joint.A1.n_rows": 105839,
  "cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS.b": 0.42844875149581085,
  "cheng_panel_models.json:builds.HOME.joint.A1_NB.coef.zCONS.pct_per_sd": 0.534874703764965,
  "cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS.pct_per_sd": 0.8310134412961416,
  "cheng_panel_models.json:builds.HOME.joint.A1.coef.zCONS.pct_ci": [
   0.7061383262187568,
   0.9650283747141353
  ],
  "cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS.pct_per_sd": 0.01267281109684637,
  "cheng_panel_models.json:builds.HOME.joint.A2.coef.zCONS.pct_ci": [
   0.004507033106396552,
   0.020904969837247656
  ],
  "cheng_panel_models.json:builds.HOME.joint.ratio_boot.ratio": 0.02081966579806125,
  "cheng_panel_models.json:builds.HOME.joint.ratio_boot.ratio_ci": [
   0.009042373304763021,
   0.035263909109610046
  ],
  "cheng_panel_models.json:builds.HOME.joint.A3.coef.zCONS.pct_per_sd": 0.013650621232445426,
  "cheng_panel_models.json:builds.ALL.joint.ratio_boot.ratio": 0.02440911703216719,
  "cheng_static.json:volume.EXP5_pooled|volume.B_raw_spearman_V_t0p3.rho": 0.2563712518701778,
  "cheng_static.json:volume.EXP5_pooled|volume.B_raw_spearman_V_t0p3.ci": [
   0.23921330023442366,
   0.27389032248349954
  ],
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O2r_m50.rho": -0.0693013812628014,
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O2r_m50.ci": [
   -0.09288056610535206,
   -0.04668336498751107
  ],
  "cheng_static.json:DL.EXP5_pooled.O2r_m50.b": -0.07859604430871031,
  "cheng_static.json:DL.EXP5_pooled.O2r_m50.I2": 0.0,
  "cheng_static.json:DL.EXP5_pooled.O2r_m50.n_negative": 5,
  "cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.rho": -0.11103014804768521,
  "cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.ci": [
   -0.19728438257060163,
   -0.030301558125793968
  ],
  "cheng_static.json:trait.COHORT_2015_17|CONS_early_home.psp.O2r_m50.n": 615,
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O1c.rho": -0.00031746728758710543,
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O1c.ci": [
   -0.01884882260240145,
   0.017447304434020514
  ],
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O3.rho": -0.0005121127935191378,
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.psp.O3.ci": [
   -0.019918268683094018,
   0.017313010786273893
  ],
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.paired_diff.O1c-O2r_m50.rho": 0.034599704092448426,
  "cheng_static.json:trait.EXP5_pooled|CONS_early_home.paired_diff.O1c-O2r_m50.ci": [
   0.003522947741278198,
   0.06608571140699572
  ],
  "cheng_static.json:DL.EXP5_pooled.O1c-O2r_m50.ci": [
   -0.008575753562913034,
   0.08271703404599004
  ],
  "identity_check.json:by_body.EXP5_pooled.jaccard_exp11_early.rho": 0.7669421825423538,
  "panel_C.json:C1.coef.zCONS.pct_per_sd": 0.0252668282237698,
  "panel_C.json:C1.boot.ci": [
   0.0035054524164536993,
   0.0478451849161699
  ],
  "palla.json:results.EXP5_pooled|O3.interaction.rho": -0.0008563755582464466,
  "palla.json:results.EXP5_pooled|O3.interaction.ci": [
   -0.021279512359615185,
   0.020030842072367914
  ]
 }
}1:"""S8: Holm over the declared family, the mechanical verdict (results/cheng_verdict.json), figures, method_out.json
20:def g(d: dict, path: str):
32:# ----------------------------------------------------------------------------- verdict
33:def verdict() -> dict:
39:    def put(name, file, path, obj):
75:        labels.append("REVERSAL CONFIRMED (on selection data)")
77:        labels.append("REVERSAL REPLICATED")
79:        labels.append("SIZE-DOMINATED")
84:        labels.append("NULL-REVERSAL")
85:    out = {"label": SELECTION_LABEL, "verdicts": labels, "predictions": pred,
93:           "rules": jload(RES / "frozen_spec.json")["verdict_rules"]}
94:    jdump(out, RES / "cheng_verdict.json")
99:def figures() -> None:
192:    def __init__(self, dev: pd.DataFrame, feats: list[str], y: str = "O2r_m50"):
202:    def _X(self, d: pd.DataFrame) -> np.ndarray:
210:    def predict(self, d: pd.DataFrame) -> np.ndarray:
215:def make_method_out(df: pd.DataFrame, pred0: np.ndarray, pred1: np.ndarray) -> dict:
216:    def fmt(v):
219:    def num(v):
247:def method_out() -> dict:
288:def run(logger) -> None:
289:    v = verdict()
290:    logger.info(f"VERDICT: {v['verdicts']}")
300:def write_report() -> dict:
302:    J = {f: jload(RES / f) for f in ["cheng_panel_models.json", "cheng_static.json", "cheng_verdict.json",
307:    def v(file: str, path: str, fmt: str = "{:+.3f}", scale: float = 1.0) -> str:
313:    def ci(file: str, path: str, fmt: str = "{:+.3f}", scale: float = 1.0) -> str:
318:    P, S, Vd = "cheng_panel_models.json", "cheng_static.json", "cheng_verdict.json"
361:    verdict_line = ", ".join(J[Vd]["verdicts"]) if Vd in J else "n/a"
363:           f"Frozen verdict (`results/cheng_verdict.json:verdicts`): **{verdict_line}** "
"""Co-occurrence ego-network indicators (family A), ported from art_yrradSC27HtQ features.concept_core.

Port changes (all logged in results/deviations.json):
  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)
    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).
  * the background comes from the context (Pass A BG/GT for RQ1; EXP3's ckpt for the port-validation test T0-8).
  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.
  * dropped near-duplicate variants: D_lag, D_q, D_withself, F_bg; the per-field block is not needed.
  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.
Everything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,
NOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code."""
from __future__ import annotations

import math
import warnings
from collections import Counter

import igraph as ig
import numpy as np

SELF_DF_MAX = 100
SELF_SHARE = 0.20
TOPN_F = 20
R_RARE = 10
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]

C: dict = {}


def slice_of(y: int) -> int:
    for i, (a, b) in enumerate(SLICES):
        if a <= y <= b:
            return i
    return 0 if y < SLICES[0][0] else len(SLICES) - 1


def rq1_windows(t0: int) -> dict[str, list[int]]:
    return {"PRE": [t0 - 3, t0 - 2, t0 - 1], "W1": [t0], "W2": [t0 + 1], "W3": [t0 + 2]}


Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'igraph'
```

### [24] TOOL CALL — Bash · 2026-09-29 11:30:10 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; sed -n 20,98p $A/lib/outputs.py; python3 -c "import json;print(json.dumps(json.load(open('$A/results/frozen_spec.json'))['verdict_rules'],indent=1))"
```

### [25] TOOL RESULT — Bash · 2026-09-29 11:30:10 UTC

```
{"stdout": "def g(d: dict, path: str):\n    \"\"\"Get a value by a dotted key path; list indices allowed as [i]; keys may contain '|' and '-'.\"\"\"\n    cur = d\n    for part in path.split(\".\"):\n        if \"[\" in part:\n            k, i = part[:-1].split(\"[\")\n            cur = cur[k][int(i)]\n        else:\n            cur = cur[part]\n    return cur\n\n\n# ----------------------------------------------------------------------------- verdict\ndef verdict() -> dict:\n    A = jload(RES / \"cheng_panel_models.json\")\n    S = jload(RES / \"cheng_static.json\")\n    C = jload(RES / \"panel_C.json\")\n    K = {}\n\n    def put(name, file, path, obj):\n        K[name] = {\"value\": g(obj, path), \"source\": f\"{file}:{path}\"}\n        return K[name][\"value\"]\n\n    a1 = put(\"A1_HOME_joint_zCONS\", \"cheng_panel_models.json\", \"builds.HOME.joint.A1.coef.zCONS\", A)\n    a2 = put(\"A2_HOME_joint_zCONS\", \"cheng_panel_models.json\", \"builds.HOME.joint.A2.coef.zCONS\", A)\n    rb = put(\"RATIO_HOME_joint\", \"cheng_panel_models.json\", \"builds.HOME.joint.ratio_boot\", A)\n    raw = put(\"B_raw_primary\", \"cheng_static.json\", f\"volume.{PRIMARY}|volume.B_raw_spearman_V_t0p3\", S)\n    p3 = put(\"P3_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.psp.O2r_m50\", S)\n    p4 = put(\"P4_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.psp.O3\", S)\n    p5 = put(\"P5_primary\", \"cheng_static.json\", f\"trait.{PRIMARY}|CONS_early_home.paired_diff.O1c-O2r_m50\", S)\n    rawc = put(\"B_raw_cohort\", \"cheng_static.json\", f\"volume.{BODY_COHORT}|volume.B_raw_spearman_V_t0p3\", S)\n    p3c = put(\"P3_cohort\", \"cheng_static.json\", f\"trait.{BODY_COHORT}|CONS_early_home.psp.O2r_m50\", S)\n    c1 = put(\"C1\", \"panel_C.json\", \"C1\", C)\n    # one-sided p-values in the predicted direction\n    p_a1 = float(stats.norm.sf(a1[\"b\"] / a1[\"se\"]))\n    fam = {\"P1-A1\": p_a1, \"P2\": rb[\"p_one_ratio_lt_0.5\"], \"P3\": p3[\"p_one_pred\"], \"P4\": p4[\"p_one_pred\"],\n           \"P5\": p5[\"p_one_pred\"]}\n    hp = dict(zip(fam, holm(list(fam.values()))))\n    pred = {\n        \"P1\": {\"holds\": bool(raw[\"rho\"] > 0 and raw[\"ci\"][0] > 0 and a1[\"b\"] > 0 and a1[\"ci\"][0] > 0),\n               \"raw_rho\": raw[\"rho\"], \"raw_ci\": raw[\"ci\"], \"A1_b\": a1[\"b\"], \"A1_ci\": a1[\"ci\"]},\n        \"P2\": {\"holds\": bool(rb[\"ratio_ci\"][1] < 0.5), \"ratio\": rb[\"ratio\"], \"ratio_ci\": rb[\"ratio_ci\"]},\n        \"P3\": {\"holds\": bool(p3[\"rho\"] < 0 and p3[\"ci\"][1] < 0), \"psp\": p3[\"rho\"], \"ci\": p3[\"ci\"]},\n        \"P4\": {\"holds\": bool(p4[\"rho\"] <= 0 and p4[\"ci\"][1] <= 0), \"psp\": p4[\"rho\"], \"ci\": p4[\"ci\"],\n               \"point_holds\": bool(p4[\"rho\"] <= 0)},\n        \"P5\": {\"holds\": bool(p5[\"rho\"] > 0 and p5[\"ci\"][0] > 0), \"diff\": p5[\"rho\"], \"ci\": p5[\"ci\"]},\n        \"P6\": {\"holds\": bool(c1[\"coef\"][\"zCONS\"][\"b\"] < 0 and c1[\"boot\"][\"ci\"][1] < 0),\n               \"b\": c1[\"coef\"][\"zCONS\"][\"b\"], \"boot_ci\": c1[\"boot\"][\"ci\"], \"crv1_ci\": c1[\"coef\"][\"zCONS\"][\"ci\"]},\n    }\n    confirmed = bool(raw[\"rho\"] > 0 and raw[\"ci\"][0] > 0 and p3[\"rho\"] < 0 and p3[\"ci\"][1] < 0)\n    n_c = p3c.get(\"n\") or 0\n    rep = bool(rawc[\"rho\"] is not None and rawc[\"rho\"] > 0 and rawc[\"ci\"][0] > 0 and p3c[\"rho\"] is not None\n               and p3c[\"rho\"] < 0 and (n_c < 600 or p3c[\"ci\"][1] < 0))\n    labels = []\n    if confirmed:\n        labels.append(\"REVERSAL CONFIRMED (on selection data)\")\n    if rep:\n        labels.append(\"REVERSAL REPLICATED\")\n    if pred[\"P2\"][\"holds\"]:\n        labels.append(\"SIZE-DOMINATED\")\n    if pred[\"P5\"][\"holds\"]:\n        labels.append(\"DEPTH-REACH SPLIT\")\n    null_rev = bool(p3[\"ci\"][0] <= 0 <= p3[\"ci\"][1])\n    if null_rev:\n        labels.append(\"NULL-REVERSAL\")\n    out = {\"label\": SELECTION_LABEL, \"verdicts\": labels, \"predictions\": pred,\n           \"holm_family_one_sided\": {k: {\"p\": fam[k], \"p_holm\": hp[k]} for k in fam},\n           \"replication\": {\"body\": BODY_COHORT, \"n\": n_c, \"raw\": rawc, \"psp_O2r_m50\": p3c,\n                           \"MDE_2.8SE\": S[\"cohort_MDE_O2r_m50\"][\"MDE_2.8SE\"],\n                           \"CI_required\": n_c >= 600, \"replicated\": rep},\n           \"null_reversal_note\": \"consistency predicts volume but carries no breadth information net of size\"\n           if null_rev else None,\n           \"sources\": {k: v[\"source\"] for k, v in K.items()},\n           \"rules\": jload(RES / \"frozen_spec.json\")[\"verdict_rules\"]}\n    jdump(out, RES / \"cheng_verdict.json\")\n    return out\n\n\n# ----------------------------------------------------------------------------- figures\n{\n \"REVERSAL CONFIRMED (on selection data)\": \"P1 raw rho > 0 with CI > 0 AND P3 psp < 0 with CI < 0 (PRIMARY)\",\n \"REVERSAL REPLICATED\": \"same on COHORT_2015_17 (CI < 0 not required if n < 600; report MDE)\",\n \"SIZE-DOMINATED\": \"A2/A1 ratio bootstrap CI upper bound < 0.5\",\n \"DEPTH-REACH SPLIT\": \"P5 CI > 0\",\n \"NULL-REVERSAL\": \"P3 CI includes 0\",\n \"other\": \"EXPLORATORY; no post-hoc subgroup claims\"\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] TOOL CALL — Bash · 2026-09-29 11:30:10 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; mkdir -p $S; cd $S; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --python /usr/local/bin/python3.12 $S/xenv && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $S/xenv/bin/python numpy==2.0.2 pandas==2.2.2 scipy==1.16.3 pyarrow==18.1.0 igraph snowballstemmer loguru statsmodels==0.14.6 pyfixest 2>&1 | tail -5; $S/xenv/bin/python -m pip list 2>/dev/null | head -0; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip list --python $S/xenv/bin/python | grep -i -E "pyfixest|numpy|pandas|scipy|formulaic|narwhals|polars|numba|jax"
```

### [27] TOOL RESULT — Bash · 2026-09-29 11:30:14 UTC

```
{"stdout": "Using Python 3.12.14 environment at: xenv\nformulaic               1.2.2\nnarwhals                2.26.0\nnumpy                   2.0.2\npandas                  2.2.2\npyfixest                0.60.0\nscipy                   1.16.3", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] TOOL CALL — Bash · 2026-09-29 11:30:24 UTC

```
A=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; $S/xenv/bin/python -c "
import pandas as pd
d=pd.read_parquet('$A/data/static_analysis_table.parquet'); print(d.shape); print(d.dtypes.to_string()); print(d.body.value_counts()); print(d.t0.describe())
f=pd.read_parquet('$A/data/cheng_features.parquet'); print(f.shape, f.columns.tolist()); print(f.head())
"; python3 -c "import json;d=json.load(open('$A/results/frozen_spec.json'));print(list(d.keys()))"
```

### [29] TOOL RESULT — Bash · 2026-09-29 11:30:26 UTC

```
{"stdout": "(13942, 46)\nci                        int64\nt0                        int64\ngroup                    object\nsplit                    object\nname                     object\nbody                     object\nwindow_flag               int64\nV_t0p2                  float64\nV_t0p3                  float64\nlogvol                  float64\ngrowth_c                float64\noffhome_share           float64\nentropy                 float64\nreach                     int64\nO2r_m50                 float64\nO2r_resid               float64\nO1c                     float64\nO1b                     float64\nO3                      float64\nCONTACT_REACH           float64\ntype                     object\ngeneric                 float64\nlevel                   float64\nfp_logN                 float64\nfp_nfields              float64\nfp_reemerge             float64\nfp_wiki_pre             float64\nnewborn                 float64\nlabel_coverage_early    float64\nhome_coverage_early     float64\nagroup                   object\ngroup5                   object\nCONS_early_all          float64\nCONS_early_home         float64\nCONS_r_early_all        float64\nCONS_r_early_home       float64\nEMB_early_all           float64\nEMB_early_home          float64\nEMB_cos_early_all       float64\nEMB_cos_early_home      float64\nSOC_early_all           float64\nSOC_early_home          float64\nn_papers_early_home       int64\ndeg_early_home          float64\nn_authors_early_home      int64\nlogV_t0p2               float64\nbody\nDEV               4771\nCOHORT_2010_14    4356\nOLD_HELDOUT       3372\nCOHORT_2015_17    1443\nName: count, dtype: int64\ncount    13942.000000\nmean      2008.773777\nstd          4.003070\nmin       2003.000000\n25%       2005.000000\n50%       2008.000000\n75%       2012.000000\nmax       2017.000000\nName: t0, dtype: float64\n(279242, 12) ['ci', 'year', 'build', 'n_papers', 'n_topics', 'CONS', 'CONS_r', 'EMB', 'EMB_cos', 'n_authors', 'SOC', 'body_src']\n    ci  year build  n_papers  ...   EMB_cos  n_authors       SOC  body_src\n0  198  2004  HOME         7  ...  0.211323         21  0.000000      EXP5\n1  198  2005  HOME         5  ...  0.176086         21  0.004762      EXP5\n2  198  2006  HOME         5  ...  0.123788         16  0.000000      EXP5\n3  198  2007  HOME         5  ...  0.194930         15  0.028571      EXP5\n4  198  2008  HOME         7  ...  0.132741         29  0.000000      EXP5\n\n[5 rows x 12 columns]\n['title', 'label', 'seed', 'definitions', 'bodies', 'groups', 'B5', 'depth_outcomes', 'reach_outcomes', 'transience_note', 'tests', 'predictions', 'holm_family', 'holm_note', 'verdict_rules', 'drop_order', 'created', 'code_sha256', 'prereg_sha256']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Write · 2026-09-29 11:31:06 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/make_mini_demo_data.py

#!/usr/bin/env python3
"""Build mini_demo_data.json for code_demo.ipynb: 100 EXP5 frame concepts (stratified by field group x body).

Per concept it stores
  * the static row of data/static_analysis_table.parquet (B5 baseline, outcomes, early Cheng traits, V(t0+2), V(t0+3));
  * one record per year t0-1 .. min(t0+11, 2022) with
      - the HOME-build non-SELF topic co-usage vector v_t (sparse: topic ids + counts) and the number of papers with
        >= 1 topic, recomputed with the artifact's own lib/cheng.py + lib/ego.py code from the Exp11 grounded rows,
        so the notebook can rebuild CONS(t) = cos(v_{t-1}, v_t) from scratch;
      - the stored HOME-build measures (CONS, CONS_r, EMB, EMB_cos, SOC, n_authors) and the ALL-build CONS;
      - the grounded yearly volume V(t) (data/V_exp5.parquet).
The source artifact directory is read-only; only mini_demo_data.json is written (next to this script).
Run: python make_mini_demo_data.py   (needs numpy, pandas, pyarrow, scipy, igraph, snowballstemmer, loguru)"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ART = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14")
OUT = Path(__file__).resolve().parent / "mini_demo_data.json"
sys.path.insert(0, str(ART / "lib"))

import pyarrow as pa  # noqa: E402
import pyarrow.compute as pc  # noqa: E402
import pyarrow.parquet as pq  # noqa: E402

import cheng  # noqa: E402
import ego  # noqa: E402
from build import job_for, load_flat  # noqa: E402
from common import B5, DEPTH, EXP5, EXP11, REACH, home_codes  # noqa: E402

N_PER_GROUP = {"CS+Eng": 17, "BGM+Med": 17, "PHYS": 17, "LIFEENV": 17, "SOC": 17, "MATHDEC": 15}
SEED = 20260929


def num(v):
    if v is None:
        return None
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return None if not math.isfinite(float(v)) else float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    return v


def main() -> None:
    st = pd.read_parquet(ART / "data/static_analysis_table.parquet")
    st = st[st.body != "COHORT_2015_17"]
    need = ["CONS_early_home", "CONS_early_all", "V_t0p2", "V_t0p3"] + B5 + REACH + DEPTH
    st = st[st[need].notna().all(1)]
    feat = pd.read_parquet(ART / "data/cheng_features.parquet")
    feat = feat[feat.body_src == "EXP5"]
    nrows = feat[(feat.build == "HOME")].groupby("ci").CONS.apply(lambda s: int(s.notna().sum()))
    st = st[st.ci.map(nrows).fillna(0) >= 6]                  # >= 6 finite yearly CONS rows (panel test A)
    rng = np.random.default_rng(SEED)
    pick = []
    for g, k in N_PER_GROUP.items():
        d = st[st.group5 == g]
        # spread over the three EXP5 bodies
        per_body = {b: d[d.body == b] for b in ["DEV", "OLD_HELDOUT", "COHORT_2010_14"]}
        for j, (b, db) in enumerate(per_body.items()):
            m = k // 3 + (1 if j < k % 3 else 0)
            pick.extend(db.ci.to_numpy()[rng.permutation(len(db))[:m]].tolist())
    st = st[st.ci.isin(pick)].sort_values(["group5", "body", "ci"]).reset_index(drop=True)
    print(f"picked {len(st)} concepts", st.group5.value_counts().to_dict(), st.body.value_counts().to_dict())

    # ---- per-year HOME non-SELF topic vectors with the artifact's own code (lib/cheng.py, lib/ego.py)
    cheng.init_context()
    nt = ego.C["nt"]
    fr = pd.read_csv(EXP5 / "frame_concepts.csv").set_index("ci")
    tab = pa.concat_tables([pq.read_table(p, columns=["ci", "year", "vfield", "topics", "authors"])
                            for p in sorted((EXP11 / "data/frame_matches_long").glob("part_*.parquet"))])
    tab = tab.filter(pc.is_in(tab.column("ci"), value_set=pa.array(st.ci.astype(np.int32).to_numpy())))
    F = load_flat(tab)
    V = pd.read_parquet(ART / "data/V_exp5.parquet", columns=["ci", "year", "V"])
    V = V[V.ci.isin(set(st.ci))].set_index(["ci", "year"]).V
    fh = feat[feat.ci.isin(set(st.ci)) & (feat.build == "HOME")].set_index(["ci", "year"])
    fa = feat[feat.ci.isin(set(st.ci)) & (feat.build == "ALL")].set_index(["ci", "year"])

    examples, max_dev = [], 0.0
    for r in st.itertuples():
        ci, t0 = int(r.ci), int(r.t0)
        fm = fr.loc[ci]
        y_hi = int(min(t0 + 10, 2022))
        al = [a for a in str(fm.aliases_used).split("|") if a and a != "nan"]
        home = home_codes(fm.home)
        j = job_for(F, ci, name=str(fm["name"]), aliases=al, t0=t0, y_lo=t0, y_hi=y_hi, home=home)
        # --- verbatim steps of cheng.concept_measures up to the HOME count vectors
        Y = np.arange(t0 - 3, y_hi + 1)
        iy = {int(y): i for i, y in enumerate(Y)}
        is_home = np.isin(j["vfield"], list(home)) if home else np.zeros(len(j["years"]), bool)
        allm = np.ones(len(j["years"]), bool)
        cA, ncA = cheng._year_vectors(j["years"], j["t_off"], j["tflat"], allm, Y, nt)
        cH, ncH = cheng._year_vectors(j["years"], j["t_off"], j["tflat"], is_home, Y, nt)
        e_idx = [iy[y] for y in (t0, t0 + 1, t0 + 2) if y in iy]
        SELF = ego.self_topics(str(fm["name"]), al, cA[e_idx].sum(0), float(ncA[e_idx].sum()))
        keep = ~SELF
        years = []
        for t in range(t0 - 1, min(t0 + 11, 2022) + 1):
            rec = {"year": t, "V": num(V.get((ci, t), 0.0))}
            if t in iy and t <= y_hi:
                v = cH[iy[t]] * keep
                nz = np.nonzero(v)[0]
                rec.update(n_papers_topic=int(ncH[iy[t]]), topic_ids=nz.tolist(), topic_counts=v[nz].astype(int).tolist())
            if (ci, t) in fh.index:
                h = fh.loc[(ci, t)]
                rec.update({k: num(h[k]) for k in ["n_papers", "n_topics", "CONS", "CONS_r", "EMB", "EMB_cos",
                                                     "SOC", "n_authors"]})
                rec["CONS_all"] = num(fa.loc[(ci, t)].CONS) if (ci, t) in fa.index else None
                # self-check: rebuild CONS from the stored vectors with the original function
                if t - 1 in iy:
                    c, _ = cheng.cons(cH[iy[t - 1]] * keep, v, int(ncH[iy[t - 1]]), int(ncH[iy[t]]))
                    s = h.CONS
                    if math.isfinite(c) or math.isfinite(s):
                        max_dev = max(max_dev, abs(c - s) if (math.isfinite(c) and math.isfinite(s)) else 1.0)
            years.append(rec)
        ex = {"input": f"{fm['name']} | ci={ci} | t0={t0} | group={r.group} | body={r.body}",
              "output": f"{r.O2r_m50:.4f}"}
        for k in ["ci", "t0", "group", "group5", "body", "split", "name", "window_flag", "V_t0p2", "V_t0p3",
                  "logV_t0p2"] + B5 + REACH + DEPTH + ["CONS_early_home", "CONS_early_all", "CONS_r_early_home",
                                                      "EMB_early_home", "EMB_cos_early_home", "SOC_early_home"]:
            ex[f"metadata_{k}"] = num(getattr(r, k))
        ex["metadata_home_vfields"] = sorted(int(h) for h in home)
        ex["metadata_n_self_topics"] = int(SELF.sum())
        ex["metadata_years"] = years
        examples.append(ex)
    print(f"max |CONS recomputed - stored| = {max_dev:.2e}")
    assert max_dev < 1e-9, max_dev
    head = json.loads((ART / "results/headline_numbers.json").read_text())["numbers"]
    out = {"metadata": {
        "description": "Demo subset of experiment art_UkIMstVveAFx (Cheng et al. 2023 ideational consistency on "
                       "OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body.",
        "n_topics": int(nt), "seed": SEED, "label": "selection data, not confirmation",
        "per_year_fields": "V = grounded yearly volume; topic_ids/topic_counts = HOME-build non-SELF topic co-usage "
                           "vector v_t; n_papers_topic = HOME papers with >= 1 topic; CONS/CONS_r/EMB/EMB_cos/SOC = "
                           "stored HOME measures; CONS_all = ALL-build CONS",
        "full_run_headline_numbers": head},
        "datasets": [{"dataset": "EXP5_frame_demo", "examples": examples}]}
    OUT.write_text(json.dumps(out, separators=(",", ":")))
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)")


if __name__ == "__main__":
    main()
```

### [31] TOOL RESULT — Write · 2026-09-29 11:31:06 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/make_mini_demo_data.py", "content": "#!/usr/bin/env python3\n\"\"\"Build mini_demo_data.json for code_demo.ipynb: 100 EXP5 frame concepts (stratified by field group x body).\n\nPer concept it stores\n  * the static row of data/static_analysis_table.parquet (B5 baseline, outcomes, early Cheng traits, V(t0+2), V(t0+3));\n  * one record per year t0-1 .. min(t0+11, 2022) with\n      - the HOME-build non-SELF topic co-usage vector v_t (sparse: topic ids + counts) and the number of papers with\n        >= 1 topic, recomputed with the artifact's own lib/cheng.py + lib/ego.py code from the Exp11 grounded rows,\n        so the notebook can rebuild CONS(t) = cos(v_{t-1}, v_t) from scratch;\n      - the stored HOME-build measures (CONS, CONS_r, EMB, EMB_cos, SOC, n_authors) and the ALL-build CONS;\n      - the grounded yearly volume V(t) (data/V_exp5.parquet).\nThe source artifact directory is read-only; only mini_demo_data.json is written (next to this script).\nRun: python make_mini_demo_data.py   (needs numpy, pandas, pyarrow, scipy, igraph, snowballstemmer, loguru)\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\n\nART = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14\")\nOUT = Path(__file__).resolve().parent / \"mini_demo_data.json\"\nsys.path.insert(0, str(ART / \"lib\"))\n\nimport pyarrow as pa  # noqa: E402\nimport pyarrow.compute as pc  # noqa: E402\nimport pyarrow.parquet as pq  # noqa: E402\n\nimport cheng  # noqa: E402\nimport ego  # noqa: E402\nfrom build import job_for, load_flat  # noqa: E402\nfrom common import B5, DEPTH, EXP5, EXP11, REACH, home_codes  # noqa: E402\n\nN_PER_GROUP = {\"CS+Eng\": 17, \"BGM+Med\": 17, \"PHYS\": 17, \"LIFEENV\": 17, \"SOC\": 17, \"MATHDEC\": 15}\nSEED = 20260929\n\n\ndef num(v):\n    if v is None:\n        return None\n    if isinstance(v, (np.integer,)):\n        return int(v)\n    if isinstance(v, (np.floating, float)):\n        return None if not math.isfinite(float(v)) else float(v)\n    if isinstance(v, (np.bool_,)):\n        return bool(v)\n    return v\n\n\ndef main() -> None:\n    st = pd.read_parquet(ART / \"data/static_analysis_table.parquet\")\n    st = st[st.body != \"COHORT_2015_17\"]\n    need = [\"CONS_early_home\", \"CONS_early_all\", \"V_t0p2\", \"V_t0p3\"] + B5 + REACH + DEPTH\n    st = st[st[need].notna().all(1)]\n    feat = pd.read_parquet(ART / \"data/cheng_features.parquet\")\n    feat = feat[feat.body_src == \"EXP5\"]\n    nrows = feat[(feat.build == \"HOME\")].groupby(\"ci\").CONS.apply(lambda s: int(s.notna().sum()))\n    st = st[st.ci.map(nrows).fillna(0) >= 6]                  # >= 6 finite yearly CONS rows (panel test A)\n    rng = np.random.default_rng(SEED)\n    pick = []\n    for g, k in N_PER_GROUP.items():\n        d = st[st.group5 == g]\n        # spread over the three EXP5 bodies\n        per_body = {b: d[d.body == b] for b in [\"DEV\", \"OLD_HELDOUT\", \"COHORT_2010_14\"]}\n        for j, (b, db) in enumerate(per_body.items()):\n            m = k // 3 + (1 if j < k % 3 else 0)\n            pick.extend(db.ci.to_numpy()[rng.permutation(len(db))[:m]].tolist())\n    st = st[st.ci.isin(pick)].sort_values([\"group5\", \"body\", \"ci\"]).reset_index(drop=True)\n    print(f\"picked {len(st)} concepts\", st.group5.value_counts().to_dict(), st.body.value_counts().to_dict())\n\n    # ---- per-year HOME non-SELF topic vectors with the artifact's own code (lib/cheng.py, lib/ego.py)\n    cheng.init_context()\n    nt = ego.C[\"nt\"]\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\").set_index(\"ci\")\n    tab = pa.concat_tables([pq.read_table(p, columns=[\"ci\", \"year\", \"vfield\", \"topics\", \"authors\"])\n                            for p in sorted((EXP11 / \"data/frame_matches_long\").glob(\"part_*.parquet\"))])\n    tab = tab.filter(pc.is_in(tab.column(\"ci\"), value_set=pa.array(st.ci.astype(np.int32).to_numpy())))\n    F = load_flat(tab)\n    V = pd.read_parquet(ART / \"data/V_exp5.parquet\", columns=[\"ci\", \"year\", \"V\"])\n    V = V[V.ci.isin(set(st.ci))].set_index([\"ci\", \"year\"]).V\n    fh = feat[feat.ci.isin(set(st.ci)) & (feat.build == \"HOME\")].set_index([\"ci\", \"year\"])\n    fa = feat[feat.ci.isin(set(st.ci)) & (feat.build == \"ALL\")].set_index([\"ci\", \"year\"])\n\n    examples, max_dev = [], 0.0\n    for r in st.itertuples():\n        ci, t0 = int(r.ci), int(r.t0)\n        fm = fr.loc[ci]\n        y_hi = int(min(t0 + 10, 2022))\n        al = [a for a in str(fm.aliases_used).split(\"|\") if a and a != \"nan\"]\n        home = home_codes(fm.home)\n        j = job_for(F, ci, name=str(fm[\"name\"]), aliases=al, t0=t0, y_lo=t0, y_hi=y_hi, home=home)\n        # --- verbatim steps of cheng.concept_measures up to the HOME count vectors\n        Y = np.arange(t0 - 3, y_hi + 1)\n        iy = {int(y): i for i, y in enumerate(Y)}\n        is_home = np.isin(j[\"vfield\"], list(home)) if home else np.zeros(len(j[\"years\"]), bool)\n        allm = np.ones(len(j[\"years\"]), bool)\n        cA, ncA = cheng._year_vectors(j[\"years\"], j[\"t_off\"], j[\"tflat\"], allm, Y, nt)\n        cH, ncH = cheng._year_vectors(j[\"years\"], j[\"t_off\"], j[\"tflat\"], is_home, Y, nt)\n        e_idx = [iy[y] for y in (t0, t0 + 1, t0 + 2) if y in iy]\n        SELF = ego.self_topics(str(fm[\"name\"]), al, cA[e_idx].sum(0), float(ncA[e_idx].sum()))\n        keep = ~SELF\n        years = []\n        for t in range(t0 - 1, min(t0 + 11, 2022) + 1):\n            rec = {\"year\": t, \"V\": num(V.get((ci, t), 0.0))}\n            if t in iy and t <= y_hi:\n                v = cH[iy[t]] * keep\n                nz = np.nonzero(v)[0]\n                rec.update(n_papers_topic=int(ncH[iy[t]]), topic_ids=nz.tolist(), topic_counts=v[nz].astype(int).tolist())\n            if (ci, t) in fh.index:\n                h = fh.loc[(ci, t)]\n                rec.update({k: num(h[k]) for k in [\"n_papers\", \"n_topics\", \"CONS\", \"CONS_r\", \"EMB\", \"EMB_cos\",\n                                                     \"SOC\", \"n_authors\"]})\n                rec[\"CONS_all\"] = num(fa.loc[(ci, t)].CONS) if (ci, t) in fa.index else None\n                # self-check: rebuild CONS from the stored vectors with the original function\n                if t - 1 in iy:\n                    c, _ = cheng.cons(cH[iy[t - 1]] * keep, v, int(ncH[iy[t - 1]]), int(ncH[iy[t]]))\n                    s = h.CONS\n                    if math.isfinite(c) or math.isfinite(s):\n                        max_dev = max(max_dev, abs(c - s) if (math.isfinite(c) and math.isfinite(s)) else 1.0)\n            years.append(rec)\n        ex = {\"input\": f\"{fm['name']} | ci={ci} | t0={t0} | group={r.group} | body={r.body}\",\n              \"output\": f\"{r.O2r_m50:.4f}\"}\n        for k in [\"ci\", \"t0\", \"group\", \"group5\", \"body\", \"split\", \"name\", \"window_flag\", \"V_t0p2\", \"V_t0p3\",\n                  \"logV_t0p2\"] + B5 + REACH + DEPTH + [\"CONS_early_home\", \"CONS_early_all\", \"CONS_r_early_home\",\n                                                      \"EMB_early_home\", \"EMB_cos_early_home\", \"SOC_early_home\"]:\n            ex[f\"metadata_{k}\"] = num(getattr(r, k))\n        ex[\"metadata_home_vfields\"] = sorted(int(h) for h in home)\n        ex[\"metadata_n_self_topics\"] = int(SELF.sum())\n        ex[\"metadata_years\"] = years\n        examples.append(ex)\n    print(f\"max |CONS recomputed - stored| = {max_dev:.2e}\")\n    assert max_dev < 1e-9, max_dev\n    head = json.loads((ART / \"results/headline_numbers.json\").read_text())[\"numbers\"]\n    out = {\"metadata\": {\n        \"description\": \"Demo subset of experiment art_UkIMstVveAFx (Cheng et al. 2023 ideational consistency on \"\n                       \"OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body.\",\n        \"n_topics\": int(nt), \"seed\": SEED, \"label\": \"selection data, not confirmation\",\n        \"per_year_fields\": \"V = grounded yearly volume; topic_ids/topic_counts = HOME-build non-SELF topic co-usage \"\n                           \"vector v_t; n_papers_topic = HOME papers with >= 1 topic; CONS/CONS_r/EMB/EMB_cos/SOC = \"\n                           \"stored HOME measures; CONS_all = ALL-build CONS\",\n        \"full_run_headline_numbers\": head},\n        \"datasets\": [{\"dataset\": \"EXP5_frame_demo\", \"examples\": examples}]}\n    OUT.write_text(json.dumps(out, separators=(\",\", \":\")))\n    print(f\"wrote {OUT} ({OUT.stat().st_size / 1e6:.2f} MB)\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [32] TOOL CALL — Bash · 2026-09-29 11:31:10 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; PYTHONDONTWRITEBYTECODE=1 timeout 900 $S/xenv/bin/python make_mini_demo_data.py 2>&1 | tail -20
```

### [33] TOOL RESULT — Bash · 2026-09-29 11:31:16 UTC

```
{"stdout": "picked 65 concepts {'BGM+Med': 11, 'CS+Eng': 11, 'LIFEENV': 11, 'PHYS': 11, 'SOC': 11, 'MATHDEC': 10} {'COHORT_2010_14': 30, 'OLD_HELDOUT': 23, 'DEV': 12}\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json (0.36 MB)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] ASSISTANT · 2026-09-29 11:31:28 UTC

```
Recomputed CONS matches the stored values exactly (max deviation 0). Only 65 concepts were picked, though, so I'm fixing the stratified selection to reach 100.
```

### [35] TOOL CALL — Bash · 2026-09-29 11:31:28 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; python3 - <<'EOF'
p='make_mini_demo_data.py'
s=open(p).read()
old='''        per_body = {b: d[d.body == b] for b in ["DEV", "OLD_HELDOUT", "COHORT_2010_14"]}
        for j, (b, db) in enumerate(per_body.items()):
            m = k // 3 + (1 if j < k % 3 else 0)
            pick.extend(db.ci.to_numpy()[rng.permutation(len(db))[:m]].tolist())'''
new='''        got = []
        for j, b in enumerate(["DEV", "OLD_HELDOUT", "COHORT_2010_14"]):
            db = d[d.body == b]
            m = k // 3 + (1 if j < k % 3 else 0)
            got.extend(db.ci.to_numpy()[rng.permutation(len(db))[:m]].tolist())
        rest = d[~d.ci.isin(got)].ci.to_numpy()                   # top up from any body if one body is short
        got.extend(rest[rng.permutation(len(rest))[:k - len(got)]].tolist())
        pick.extend(got)'''
assert old in s; s=s.replace(old,new); open(p,'w').write(s)
EOF
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; $S/xenv/bin/python -c "
import pandas as pd
A='/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14'
st=pd.read_parquet(A+'/data/static_analysis_table.parquet'); print(st.ci.duplicated().sum()); st=st[st.body!='COHORT_2015_17']
print(pd.crosstab(st.group5, st.body))"
```

### [36] TOOL RESULT — Bash · 2026-09-29 11:31:28 UTC

```
{"stdout": "0\nbody     COHORT_2010_14   DEV  OLD_HELDOUT\ngroup5                                    \nBGM+Med            1534  3053            0\nCS+Eng              950  1718            0\nLIFEENV             555     0         1113\nMATHDEC             103     0          165\nPHYS                355     0          742\nSOC                 859     0         1352", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Bash · 2026-09-29 11:31:34 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; PYTHONDONTWRITEBYTECODE=1 timeout 900 $S/xenv/bin/python make_mini_demo_data.py 2>&1 | tail -5; python3 -c "
import json;d=json.load(open('mini_demo_data.json'));e=d['datasets'][0]['examples'];print(len(e));x=e[0];print({k:v for k,v in x.items() if k!='metadata_years'});print(x['metadata_years'][:3])"
```

### [38] TOOL RESULT — Bash · 2026-09-29 11:31:38 UTC

```
{"stdout": "picked 100 concepts {'BGM+Med': 17, 'CS+Eng': 17, 'LIFEENV': 17, 'PHYS': 17, 'SOC': 17, 'MATHDEC': 15} {'COHORT_2010_14': 44, 'OLD_HELDOUT': 35, 'DEV': 21}\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json (0.55 MB)\n100\n{'input': 'Oculocutaneous albinism | ci=26449 | t0=2011 | group=Med | body=COHORT_2010_14', 'output': '3.4925', 'metadata_ci': 26449, 'metadata_t0': 2011, 'metadata_group': 'Med', 'metadata_group5': 'BGM+Med', 'metadata_body': 'COHORT_2010_14', 'metadata_split': 'COHORT', 'metadata_name': 'Oculocutaneous albinism', 'metadata_window_flag': 0, 'metadata_V_t0p2': 24.0, 'metadata_V_t0p3': 28.0, 'metadata_logV_t0p2': 3.2188758248682006, 'metadata_logvol': 4.143134726391533, 'metadata_growth_c': 0.0833815898655645, 'metadata_offhome_share': 0.282608687877655, 'metadata_entropy': 0.7480666720469508, 'metadata_reach': 3, 'metadata_O2r_m50': 3.492537313432843, 'metadata_O2r_resid': -0.8917942779082484, 'metadata_O1c': 0.2995165300987841, 'metadata_O1b': 1.0, 'metadata_O3': 0.0, 'metadata_CONS_early_home': 0.3758166683528513, 'metadata_CONS_early_all': 0.500513915640711, 'metadata_CONS_r_early_home': 0.5987955178251971, 'metadata_EMB_early_home': 1.2566453729922609, 'metadata_EMB_cos_early_home': 0.17886283014347842, 'metadata_SOC_early_home': 0.01808138061334992, 'metadata_home_vfields': [17], 'metadata_n_self_topics': 3}\n[{'year': 2010, 'V': 16.0, 'n_papers_topic': 7, 'topic_ids': [249, 1148, 1193, 1327, 1479, 1687, 1766, 1867, 2354, 2630, 2662, 2987, 3382], 'topic_counts': [1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1]}, {'year': 2011, 'V': 22.0, 'n_papers_topic': 12, 'topic_ids': [380, 391, 970, 1012, 1166, 1532, 1552, 1558, 2285, 2815, 2917, 2987], 'topic_counts': [1, 1, 1, 1, 1, 1, 5, 1, 1, 1, 1, 2], 'n_papers': 12, 'n_topics': 12, 'CONS': 0.08006407690254357, 'CONS_r': 0.25, 'EMB': 1.5046640592217446, 'EMB_cos': 0.19607091330286036, 'SOC': 0.00482897384305835, 'n_authors': 71, 'CONS_all': 0.4233382458667935}, {'year': 2012, 'V': 16.0, 'n_papers_topic': 8, 'topic_ids': [105, 690, 1012, 1212, 1552, 1707, 1771, 2231], 'topic_counts': [1, 1, 2, 1, 1, 1, 1, 1], 'n_papers': 8, 'n_topics': 8, 'CONS': 0.3379631847096873, 'CONS_r': 0.501280411827603, 'EMB': 1.0478479657854354, 'EMB_cos': 0.13470634716368046, 'SOC': 0.02252252252252252, 'n_authors': 37, 'CONS_all': 0.4895650243261648}]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-29 11:32:28 UTC

```
Data file done (100 concepts, 0.55 MB). Now writing the notebook builder with the original lib functions split into cells.
```

### [40] TOOL CALL — Bash · 2026-09-29 11:32:28 UTC

```
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip show --python $S/xenv/bin/python pyfixest | grep -i requires; python3 -c "import nbformat; print(nbformat.__version__)"
```

### [41] TOOL RESULT — Bash [ERROR] · 2026-09-29 11:32:28 UTC

```
Error: Exit code 1
Using Python 3.12.14 environment at: /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/xenv
Requires: formulaic, joblib, maketables, narwhals, numpy, pandas, scipy, seaborn, tabulate, tqdm
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'nbformat'
```

### [42] TOOL CALL — Write · 2026-09-29 11:36:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [43] TOOL RESULT — Write · 2026-09-29 11:36:09 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [44] TOOL CALL — Bash · 2026-09-29 11:36:20 UTC

```
cd /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad && python3 - <<'EOF'
p='build_nb.py'
s=open(p).read()
old='''        if t == "code":
            for k, v in CFG.items():
                s = s.replace("{" + k + "}", str(v))
        c = {'''
new='''        s = s.replace('\\\\"\\\\"\\\\"', '"""')
        if t == "code" and "N_BOOT_PANEL = {" in s:
            for k, v in CFG.items():
                s = s.replace("{" + k + "}", str(v))
        c = {'''
assert old in s; s=s.replace(old,new)
old2=s[s.index('    # also dump the code'):s.index('\n\nbuild()')]
new2='''    # also dump the code (minus install cell) as a script for quick local checks
    src = "\\n\\n".join(("".join(c["source"])) for c in nb["cells"] if c["cell_type"] == "code")
    src = src.split("\\n\\n", 1)[1] if False else "\\n\\n".join("".join(c["source"]) for c in nb["cells"][1:] if c["cell_type"] == "code" and "_pip(" not in "".join(c["source"]))
    Path(__file__).with_name("nb_code.py").write_text("import matplotlib; matplotlib.use('Agg')\\n" + src.replace("from __future__ import annotations", ""))'''
s=s.replace(old2,new2)
open(p,'w').write(s)
EOF
python3 build_nb.py '{"N_CONCEPTS":100,"N_BOOT_PANEL":10,"N_BOOT_STATIC":10,"N_BOOT_SECONDARY":10,"N_BOOT_GROUP":10,"N_BOOT_PALLA":10}' && grep -n '\\"' nb_code.py | head; grep -n "N_BOOT_PANEL =" nb_code.py; cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx && time /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/xenv/bin/python /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/nb_code.py 2>&1 | tail -60
```

### [45] TOOL RESULT — Bash · 2026-09-29 11:36:26 UTC

```
{"stdout": "46:N_BOOT_PANEL = 10        # original: 500  (test A: concept-cluster bootstrap of the A2/A1 ratio)\nDemo subset of experiment art_UkIMstVveAFx (Cheng et al. 2023 ideational consistency on OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body.\nconcepts in file: 100 | OpenAlex topics: 4516\n100 concepts; {'BGM+Med': 17, 'CS+Eng': 17, 'LIFEENV': 17, 'PHYS': 17, 'SOC': 17, 'MATHDEC': 15} {'COHORT_2010_14': 44, 'OLD_HELDOUT': 35, 'DEV': 21}\nfeature rows: 2158 (1079 HOME); finite HOME CONS: 1040\nmax |recomputed CONS - stored CONS| = 0.00e+00\nHOME CONS quantiles: [0.    0.179 0.34  0.513 0.669 0.802 0.983]\nmax |CONS_early_home - stored| = 0.0\nmax |CONS_early_all  - stored| = 0.0\nA HOME: joint A1 {'b': 0.537445816610149, 'se': 0.11265038184946556, 'ci': [0.3166551253405119, 0.7582365078797861], 'p': 1.833875279189101e-06, 'pct_per_sd': 0.7116294586860437, 'pct_ci': [0.37252913977305835, 1.13450871019488]} A2 {'b': 0.005615475910528, 'se': 0.019301404044940306, 'ci': [-0.032214580868610725, 0.04344553268966673], 'p': 0.7711001636573185, 'pct_per_sd': 0.0056312722495242, 'pct_ci': [-0.031701218608616744, 0.04440310693465066]}\nA HOME: ratio 0.010 CI [-0.038  0.049] (irls-pf diff 1.15e-12); cons-only 0.017 [-0.037  0.055]\nA HOME done in 0.04 min\n\nTest A done in 2.2s | joint rows 933, concepts 100\n  A1: zCONS b = +0.537  -> +71.2% per SD  [+37.3, +113.5]\n  A2: zCONS b = +0.006  -> +0.6% per SD  [-3.2, +4.4]\n  A3: zCONS b = +0.043  -> +4.4% per SD  [+1.3, +7.6]\n  A1-NB: zCONS b = +0.373 -> +45.2% per SD (Cheng 2023: b = .43, +53%)\n  ratio A2/A1 = 0.010  boot CI [-0.038  0.049]\nB: 24 trait tasks + 8 volume tasks on 1 worker(s)\nB primary: O2r_m50 +0.005 [-0.246  0.097], O2r_resid +0.014 [-0.228  0.112], O1c +0.085 [-0.019  0.208], O1b -0.174 [-0.238 -0.003]\nB primary diff O1c-O2r_m50 +0.080 [-0.137  0.315]\nB volume primary: raw Spearman(CONS_early_home, V(t0+3)) +0.153 [0.03  0.237]\nS4 done in 0.00 min\nD EXP5_pooled|O3: interaction -0.0000 [-0.  0.]\nD EXP5_pooled|O2r_m50: interaction +0.0854 [-0.3108  0.391 ]\nD EXP5_pooled|O1c: interaction +0.7020 [0.154 1.35 ]\nE EXP5_pooled: reach_set|O2r_m50 -0.055 [-0.161  0.08 ]; reach_set|O1c +0.024 [-0.131  0.279]; full_set|O1c +0.024 [-0.131  0.279]\nE DEV: \nE OLD_HELDOUT: reach_set|O2r_m50 -0.065 [-0.41   0.615]; reach_set|O1c -0.053 [-0.272  0.414]; full_set|O1c -0.053 [-0.272  0.414]\nE COHORT_2010_14: reach_set|O2r_m50 -0.005 [-0.338  0.221]; reach_set|O1c +0.143 [-0.072  0.404]; full_set|O1c +0.143 [-0.072  0.404]\nTraceback (most recent call last):\n  File \"/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/nb_code.py\", line 826, in <module>\n    V_out = verdict(resA, resB)\n            ^^^^^^^^^^^^^^^^^^^\n  File \"/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/nb_code.py\", line 799, in verdict\n    fam = {\"P1-A1\": p_a1, \"P2\": rb[\"p_one_ratio_lt_0.5\"], \"P3\": p3[\"p_one_pred\"], \"P4\": p4[\"p_one_pred\"],\n                                                                                        ~~^^^^^^^^^^^^^^\nKeyError: 'p_one_pred'\n\nreal\t0m5.418s\nuser\t0m4.654s\nsys\t0m0.456s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-29 11:36:34 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; python3 -c "
import json,collections;d=json.load(open('mini_demo_data.json'));e=d['datasets'][0]['examples']
print(collections.Counter(x['metadata_O3'] for x in e), collections.Counter(x['metadata_O1b'] for x in e))"
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/xenv/bin/python -c "
import pandas as pd;d=pd.read_parquet('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_14/data/static_analysis_table.parquet');print(d.O3.value_counts(dropna=False))"
```

### [47] TOOL RESULT — Bash · 2026-09-29 11:36:36 UTC

```
{"stdout": "Counter({0.0: 100}) Counter({1.0: 66, 0.0: 34})\nO3\n0.0    13406\n1.0      536\nName: count, dtype: int64", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] TOOL CALL — Bash · 2026-09-29 11:36:48 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; python3 - <<'EOF'
p='make_mini_demo_data.py'
s=open(p).read()
old='''    st = st[st.ci.map(nrows).fillna(0) >= 6]                  # >= 6 finite yearly CONS rows (panel test A)'''
new='''    st["n_cons_rows"] = st.ci.map(nrows).fillna(0)
    # >= 6 finite yearly CONS rows (panel test A); transient concepts (O3 == 1, ~4% of the frame) need >= 2 rows so
    # that the rare outcome O3 varies within the demo subset
    st = st[(st.n_cons_rows >= 6) | ((st.O3 == 1) & (st.n_cons_rows >= 2))]'''
assert old in s; s=s.replace(old,new)
old='''        got = []
'''
new='''        tr = d[d.O3 == 1].ci.to_numpy()
        got = tr[rng.permutation(len(tr))[:2]].tolist()           # 2 transient concepts per group
        d = d[(d.n_cons_rows >= 6) & ~d.ci.isin(got)]
'''
assert old in s; s=s.replace(old,new)
old='''            m = k // 3 + (1 if j < k % 3 else 0)'''
new='''            m = (k - 2) // 3 + (1 if j < (k - 2) % 3 else 0)'''
assert old in s; s=s.replace(old,new)
open(p,'w').write(s)
EOF
S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; PYTHONDONTWRITEBYTECODE=1 timeout 900 $S/xenv/bin/python make_mini_demo_data.py 2>&1 | tail -4; python3 -c "
import json,collections;d=json.load(open('mini_demo_data.json'));e=d['datasets'][0]['examples']
print(len(e), collections.Counter(x['metadata_O3'] for x in e), len(set(x['metadata_ci'] for x in e)))"
```

### [49] TOOL RESULT — Bash · 2026-09-29 11:36:52 UTC

```
{"stdout": "picked 100 concepts {'BGM+Med': 17, 'CS+Eng': 17, 'LIFEENV': 17, 'PHYS': 17, 'SOC': 17, 'MATHDEC': 15} {'COHORT_2010_14': 42, 'OLD_HELDOUT': 37, 'DEV': 21}\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json (0.56 MB)\n100 Counter({0.0: 88, 1.0: 12}) 100", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] TOOL CALL — Bash · 2026-09-29 11:37:00 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; sed -i 's|"OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body."|"OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body; transient "\n                       "concepts (O3 == 1) oversampled to 2 per group so that the rare transience outcome varies."|' make_mini_demo_data.py; grep -n "oversampled" -B2 make_mini_demo_data.py; S=/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; PYTHONDONTWRITEBYTECODE=1 $S/xenv/bin/python make_mini_demo_data.py 2>&1 | tail -2 && time $S/xenv/bin/python $S/nb_code.py 2>&1 | tail -45
```

### [51] TOOL RESULT — Bash · 2026-09-29 11:37:08 UTC

```
{"stdout": "147-        \"description\": \"Demo subset of experiment art_UkIMstVveAFx (Cheng et al. 2023 ideational consistency on \"\n148-                       \"OpenAlex topic co-usage): 100 EXP5 frame concepts stratified by field group and body; transient \"\n149:                       \"concepts (O3 == 1) oversampled to 2 per group so that the rare transience outcome varies.\",\nmax |CONS recomputed - stored| = 0.00e+00\nwrote /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/mini_demo_data.json (0.56 MB)\nmax |CONS_early_home - stored| = 0.0\nmax |CONS_early_all  - stored| = 0.0\nA HOME: joint A1 {'b': 0.24053638843858696, 'se': 0.06486840796127699, 'ci': [0.11339664510003272, 0.3676761317771412], 'p': 0.000208847588432981, 'pct_per_sd': 0.2719312165780745, 'pct_ci': [0.12007611755463032, 0.44437417631741805]} A2 {'b': 0.0181778159700857, 'se': 0.013246256011722106, 'ci': [-0.007784368742886811, 0.044140000683058206], 'p': 0.16997056260695187, 'pct_per_sd': 0.018344038124502804, 'pct_ci': [-0.0077541490092146725, 0.04512866337331678]}\nA HOME: ratio 0.076 CI [0.01  0.145] (irls-pf diff 1.79e-10); cons-only 0.070 [-0.03  0.16]\nA HOME done in 0.01 min\n\nTest A done in 0.7s | joint rows 947, concepts 100\n  A1: zCONS b = +0.241  -> +27.2% per SD  [+12.0, +44.4]\n  A2: zCONS b = +0.018  -> +1.8% per SD  [-0.8, +4.5]\n  A3: zCONS b = +0.033  -> +3.4% per SD  [-0.1, +6.9]\n  A1-NB: zCONS b = +0.190 -> +20.9% per SD (Cheng 2023: b = .43, +53%)\n  ratio A2/A1 = 0.076  boot CI [0.01  0.145]\nB: 24 trait tasks + 8 volume tasks on 1 worker(s)\nB primary: O2r_m50 -0.263 [-0.405 -0.24 ], O2r_resid -0.277 [-0.42  -0.266], O1c -0.125 [-0.241  0.137], O1b -0.051 [-0.237  0.085], O3 -0.065 [-0.253  0.126]\nB primary diff O1c-O2r_m50 +0.137 [0.113 0.457]\nB volume primary: raw Spearman(CONS_early_home, V(t0+3)) +0.206 [-0.041  0.312]\nS4 done in 0.00 min\nD EXP5_pooled|O3: interaction +0.2392 [-0.3818  0.7688]\nD EXP5_pooled|O2r_m50: interaction -0.2524 [-0.5984  0.5046]\nD EXP5_pooled|O1c: interaction +0.5501 [0.3632 0.8377]\nE EXP5_pooled: reach_set|O2r_m50 +0.034 [-0.181  0.134]; reach_set|O1c -0.051 [-0.234  0.137]; full_set|O1c -0.051 [-0.234  0.137]\nE DEV: \nE OLD_HELDOUT: reach_set|O2r_m50 +0.193 [-0.579  0.599]; reach_set|O1c -0.204 [-0.854  0.101]; full_set|O1c -0.204 [-0.854  0.101]\nE COHORT_2010_14: reach_set|O2r_m50 -0.091 [-0.352  0.234]; reach_set|O1c +0.120 [-0.277  0.223]; full_set|O1c +0.120 [-0.277  0.223]\nDEMO VERDICT: ['SIZE-DOMINATED', 'DEPTH-REACH SPLIT']\n  P1: holds=False\n  P2: holds=True\n  P3: holds=True\n  P4: holds=False\n  P5: holds=True\nFULL-RUN VERDICT: REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT\n                                quantity     demo (100 concepts)                full run\n  A: A1-NB zCONS, % per SD (Cheng: +53%)                  +20.9%                  +53.5%\n              A: A1 PPML zCONS, % per SD   +27.2% [+12.0, +44.4]   +83.1% [+70.6, +96.5]\n      A: A2 (+ log V(t)) zCONS, % per SD      +1.8% [-0.8, +4.5]      +1.3% [+0.5, +2.1]\n      A: A3 (concept FE) zCONS, % per SD                   +3.4%                   +1.4%\n                    A: ratio b_A2 / b_A1 +0.076 [+0.010, +0.145] +0.021 [+0.009, +0.035]\n    B: raw Spearman(CONS_early, V(t0+3)) +0.206 [-0.041, +0.312] +0.256 [+0.239, +0.274]\nB: psp(CONS_early, O2r_m50 | B5) [reach] -0.263 [-0.405, -0.240] -0.069 [-0.093, -0.047]\n    B: psp(CONS_early, O1c | B5) [depth] -0.125 [-0.241, +0.137] -0.000 [-0.019, +0.017]\nB: psp(CONS_early, O3 | B5) [transience] -0.065 [-0.253, +0.126] -0.001 [-0.020, +0.017]\n            B: paired diff O1c - O2r_m50 +0.137 [+0.113, +0.457] +0.035 [+0.004, +0.066]\n              D: Palla interaction on O3 +0.239 [-0.382, +0.769] -0.001 [-0.021, +0.020]\n\nDemo verdict: ['SIZE-DOMINATED', 'DEPTH-REACH SPLIT']\n\nreal\t0m2.540s\nuser\t0m2.466s\nsys\t0m0.178s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] ASSISTANT · 2026-09-29 11:37:14 UTC

```
Minimal config runs end-to-end in ~3 s locally: it reproduces the size-dominated result (A2/A1 ratio ≈ 0.08) and the negative reach psp. Next I'm testing the notebook in the clean Colab-like venv.
```

### [53] TOOL CALL — Bash · 2026-09-29 11:37:14 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae; (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel) 2>&1 | tail -3; start=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -5; echo "elapsed $(( $(date +%s)-start ))s"
```

### [54] TOOL RESULT — Bash · 2026-09-29 11:37:58 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 268247 bytes to code_demo.ipynb\nelapsed 40s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Bash · 2026-09-29 11:38:12 UTC

```
cd /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; python3 -c "
import json;nb=json.load(open('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx/code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    if o['output_type']=='stream' and o['name']=='stderr': print('STDERR', ''.join(o['text'])[:300])
    if o['output_type']=='display_data': print('display', list(o['data'].keys()))
"; python3 build_nb.py '{"N_CONCEPTS":100,"N_BOOT_PANEL":500,"N_BOOT_STATIC":2000,"N_BOOT_SECONDARY":500,"N_BOOT_GROUP":1000,"N_BOOT_PALLA":1000}'; cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; time /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/xenv/bin/python /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/nb_code.py 2>&1 | tail -40
```

### [56] TOOL RESULT — Bash · 2026-09-29 11:38:26 UTC

```
{"stdout": "display ['image/png', 'text/plain']\n\nTest A done in 1.3s | joint rows 947, concepts 100\n  A1: zCONS b = +0.241  -> +27.2% per SD  [+12.0, +44.4]\n  A2: zCONS b = +0.018  -> +1.8% per SD  [-0.8, +4.5]\n  A3: zCONS b = +0.033  -> +3.4% per SD  [-0.1, +6.9]\n  A1-NB: zCONS b = +0.190 -> +20.9% per SD (Cheng 2023: b = .43, +53%)\n  ratio A2/A1 = 0.076  boot CI [-0.067  0.169]\nB: 24 trait tasks + 8 volume tasks on 1 worker(s)\nB primary: O2r_m50 -0.263 [-0.481  0.01 ], O2r_resid -0.277 [-0.502 -0.003], O1c -0.125 [-0.339  0.116], O1b -0.051 [-0.275  0.191], O3 -0.065 [-0.313  0.177]\nB primary diff O1c-O2r_m50 +0.137 [-0.239  0.505]\nB volume primary: raw Spearman(CONS_early_home, V(t0+3)) +0.206 [-0.002  0.386]\nS4 done in 0.13 min\nD EXP5_pooled|O3: interaction +0.2392 [-0.3347  0.782 ]\nD EXP5_pooled|O2r_m50: interaction -0.2524 [-0.7814  0.3295]\nD EXP5_pooled|O1c: interaction +0.5501 [-0.2203  1.3073]\nE EXP5_pooled: reach_set|O2r_m50 +0.034 [-0.163  0.253]; reach_set|O1c -0.051 [-0.292  0.183]; full_set|O1c -0.051 [-0.292  0.183]\nE DEV: \nE OLD_HELDOUT: reach_set|O2r_m50 +0.193 [-0.316  0.754]; reach_set|O1c -0.204 [-0.759  0.472]; full_set|O1c -0.204 [-0.759  0.472]\nE COHORT_2010_14: reach_set|O2r_m50 -0.091 [-0.457  0.44 ]; reach_set|O1c +0.120 [-0.337  0.481]; full_set|O1c +0.120 [-0.337  0.481]\nDEMO VERDICT: ['SIZE-DOMINATED', 'NULL-REVERSAL']\n  P1: holds=False\n  P2: holds=True\n  P3: holds=False\n  P4: holds=False\n  P5: holds=False\nFULL-RUN VERDICT: REVERSAL CONFIRMED (on selection data), REVERSAL REPLICATED, SIZE-DOMINATED, DEPTH-REACH SPLIT\n                                quantity     demo (100 concepts)                full run\n  A: A1-NB zCONS, % per SD (Cheng: +53%)                  +20.9%                  +53.5%\n              A: A1 PPML zCONS, % per SD   +27.2% [+12.0, +44.4]   +83.1% [+70.6, +96.5]\n      A: A2 (+ log V(t)) zCONS, % per SD      +1.8% [-0.8, +4.5]      +1.3% [+0.5, +2.1]\n      A: A3 (concept FE) zCONS, % per SD                   +3.4%                   +1.4%\n                    A: ratio b_A2 / b_A1 +0.076 [-0.067, +0.169] +0.021 [+0.009, +0.035]\n    B: raw Spearman(CONS_early, V(t0+3)) +0.206 [-0.002, +0.386] +0.256 [+0.239, +0.274]\nB: psp(CONS_early, O2r_m50 | B5) [reach] -0.263 [-0.481, +0.010] -0.069 [-0.093, -0.047]\n    B: psp(CONS_early, O1c | B5) [depth] -0.125 [-0.339, +0.116] -0.000 [-0.019, +0.017]\nB: psp(CONS_early, O3 | B5) [transience] -0.065 [-0.313, +0.177] -0.001 [-0.020, +0.017]\n            B: paired diff O1c - O2r_m50 +0.137 [-0.239, +0.505] +0.035 [+0.004, +0.066]\n              D: Palla interaction on O3 +0.239 [-0.335, +0.782] -0.001 [-0.021, +0.020]\n\nDemo verdict: ['SIZE-DOMINATED', 'NULL-REVERSAL']\n\nreal\t0m15.213s\nuser\t0m15.128s\nsys\t0m0.201s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] ASSISTANT · 2026-09-29 11:38:44 UTC

```
Using the full original bootstrap counts (500/2000/500/1000/1000) takes about 15 s, so the demo keeps the original values. I'm tidying the markdown, then running the final clean-venv test.
```

### [58] TOOL CALL — Bash · 2026-09-29 11:38:44 UTC

```
cd /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; python3 - <<'EOF'
p='build_nb.py'
s=open(p).read()
old="""The demo data (`mini_demo_data.json`) holds 100 EXP5 frame concepts, stratified over the six field groups. Each concept"""
new="""The demo data (`mini_demo_data.json`) holds 100 EXP5 frame concepts, stratified over the six field groups. Transient
concepts ($O3=1$, about 4% of the frame) are oversampled to 2 per group so that the transience outcome varies. Each concept"""
assert old in s; s=s.replace(old,new)
old="""At 100 concepts the reach test has little power, so NULL-REVERSAL is the expected demo outcome even though the full run
confirms the reversal."""
new="""At 100 concepts the confidence intervals are about 10 times wider than in the full run. The size result (Test A)
survives at this scale. The reach reversal keeps the full run's sign, but its CI can reach 0, so the demo can return
NULL-REVERSAL even though the full run confirms the reversal."""
assert old in s; s=s.replace(old,new)
open(p,'w').write(s)
EOF
python3 build_nb.py '{"N_CONCEPTS":100,"N_BOOT_PANEL":500,"N_BOOT_STATIC":2000,"N_BOOT_SECONDARY":500,"N_BOOT_GROUP":1000,"N_BOOT_PALLA":1000}'
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae; (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel) 2>&1 | tail -3; start=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "elapsed $(( $(date +%s)-start ))s"
python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    if o['output_type']=='display_data' and 'image/png' in o['data']: open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [59] TOOL RESULT — Bash · 2026-09-29 11:39:34 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 267790 bytes to code_demo.ipynb\nelapsed 48s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL CALL — Read · 2026-09-29 11:39:38 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/fig.png
```

### [61] TOOL RESULT — Read · 2026-09-29 11:39:39 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [62] ASSISTANT · 2026-09-29 11:39:55 UTC

```
Figure renders correctly. One fix: the legend in panel (c) overlaps the O3 row, so I'm moving it below the axes and running a final test.
```

### [63] TOOL CALL — Bash · 2026-09-29 11:39:55 UTC

```
cd /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad; sed -i 's|ax\[2\].legend(fontsize=8, loc="lower right")|ax[2].legend(fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2)|' build_nb.py && grep -c 'bbox_to_anchor' build_nb.py && python3 build_nb.py '{"N_CONCEPTS":100,"N_BOOT_PANEL":500,"N_BOOT_STATIC":2000,"N_BOOT_SECONDARY":500,"N_BOOT_GROUP":1000,"N_BOOT_PALLA":1000}'
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; E=/tmp/aii_nb_test_envs/art_UkIMstVveAFx-d3b858eaf4ae; (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel) 2>&1 | tail -3; start=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "elapsed $(( $(date +%s)-start ))s"
python3 -c "
import json,base64;nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
    if o['output_type']=='display_data' and 'image/png' in o['data']: open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
print(sum(1 for c in nb['cells'] if c['cell_type']=='code'), 'code cells', sum(1 for c in nb['cells'] if c['cell_type']=='markdown'),'md')
"; grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-14/demo/mini_demo_data.json"' code_demo.ipynb; ls -la
```

### [64] TOOL RESULT — Bash · 2026-09-29 11:40:49 UTC

```
{"stdout": "1\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 266242 bytes to code_demo.ipynb\nelapsed 52s\n24 code cells 20 md\n0\ntotal 5313\ndrwxr-xr-x 3 root root 2000137 Sep 29 11:37 .\ndrwxr-xr-x 6 root root 2000386 Sep 29 11:39 ..\ndrwxr-xr-x 2 root root       1 Sep 29 11:28 .aii\n-rw------- 1 root root      54 Sep 29 11:29 .aii_claude_session.json\n-rw-r--r-- 1 root root  603745 Sep 29 11:40 .repl_agent.ptylog\n-rw-r--r-- 1 root root  266259 Sep 29 11:40 code_demo.ipynb\n-rw-r--r-- 1 root root    8924 Sep 29 11:37 make_mini_demo_data.py\n-rw-r--r-- 1 root root  557774 Sep 29 11:37 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [65] TOOL CALL — Bash · 2026-09-29 11:40:55 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));src='\n'.join(''.join(c['source']) for c in nb['cells'])
print('GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-8795ea-concepts-spread-once-adopters-make-them/main/round-5/experiment-14/demo/mini_demo_data.json\"' in src, 'urlopen(GITHUB_DATA_URL)' in src)
for c in nb['cells']:
  if c['cell_type']=='code':
    for o in c['outputs']:
      if o['output_type']=='stream' and 'quantity' in ''.join(o['text']): print(''.join(o['text']))
"
```

### [66] TOOL RESULT — Bash · 2026-09-29 11:40:55 UTC

```
{"stdout": "True True\n                                quantity     demo (100 concepts)                full run\n  A: A1-NB zCONS, % per SD (Cheng: +53%)                  +20.9%                  +53.5%\n              A: A1 PPML zCONS, % per SD   +27.2% [+12.0, +44.4]   +83.1% [+70.6, +96.5]\n      A: A2 (+ log V(t)) zCONS, % per SD      +1.8% [-0.8, +4.5]      +1.3% [+0.5, +2.1]\n      A: A3 (concept FE) zCONS, % per SD                   +3.4%                   +1.4%\n                    A: ratio b_A2 / b_A1 +0.076 [-0.067, +0.169] +0.021 [+0.009, +0.035]\n    B: raw Spearman(CONS_early, V(t0+3)) +0.206 [-0.002, +0.386] +0.256 [+0.239, +0.274]\nB: psp(CONS_early, O2r_m50 | B5) [reach] -0.263 [-0.481, +0.010] -0.069 [-0.093, -0.047]\n    B: psp(CONS_early, O1c | B5) [depth] -0.125 [-0.339, +0.116] -0.000 [-0.019, +0.017]\nB: psp(CONS_early, O3 | B5) [transience] -0.065 [-0.313, +0.177] -0.001 [-0.020, +0.017]\n            B: paired diff O1c - O2r_m50 +0.137 [-0.239, +0.505] +0.035 [+0.004, +0.066]\n              D: Palla interaction on O3 +0.239 [-0.335, +0.782] -0.001 [-0.021, +0.020]\n\nDemo verdict: ['SIZE-DOMINATED', 'NULL-REVERSAL']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [67] TOOL CALL — Read · 2026-09-29 11:40:55 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-UkIMstVveAFx/fde0499e-f83a-439f-991e-5474ac4bcdca/scratchpad/fig.png
```

### [68] TOOL RESULT — Read · 2026-09-29 11:40:55 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [69] ASSISTANT · 2026-09-29 11:41:13 UTC

```
The notebook passes end-to-end in 52 s. Last step: the README, the manifest and the structured output.
```

### [70] TOOL CALL — Bash · 2026-09-29 11:41:13 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_UkIMstVveAFx; cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is a small text/code/JSON file (< 1 MB) and is kept as-is.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: Cheng's ideational consistency is a size effect, not reach

This is a runnable, Colab-ready demo notebook for the experiment `art_UkIMstVveAFx`. The experiment rebuilds the
**ideational consistency** measure of Cheng et al. (2023, *ASR*), CONS(t) = cos(v_{t-1}, v_t) over a concept's
OpenAlex topic co-usage vectors. It then tests whether CONS predicts a concept's *reach* across fields or only its *size*.

The notebook splits the original `method.py` orchestrator and the `lib/` step modules it calls into cells, with
explanations between them. The code is the original code, changed only where needed to read in-memory data in place of
parquet files. It runs on a curated subset of 100 concepts:

* **S1**: CONS and CONS_r are recomputed from the stored per-year topic vectors and match the original run exactly
  (max deviation 0). EMB and SOC are loaded from the stored run.
* **S3, Test A**: Cheng panel regressions (PPML A1 / A2 / A3, negative binomial) plus the concept-cluster bootstrap of the
  A2/A1 ratio.
* **S4, Test B**: partial Spearman of early CONS against reach and depth outcomes, controlling for the B5 baseline.
* **S6, Test D**: Palla size × consistency interaction.
* **S7, Test E**: HOME vs ALL coupling.
* **S8**: the mechanical verdict.

S2 (identity check) and S5 (Test C) need upstream Exp11 tables that are not part of the demo, so they are left out.
The bootstrap counts are the original ones (500 / 2000 / 500 / 1000 / 1000). The whole notebook, including the package
install, runs in about 1 minute.

Demo result (100 concepts): **SIZE-DOMINATED** holds. A1 gives +27% next-year volume per SD of CONS; after the size
control (A2) this falls to +1.8%, a ratio of 0.08. The reach psp keeps the full run's sign (−0.26), but its CI reaches 0
(NULL-REVERSAL at this n). The full run (12,499 concepts) finds REVERSAL CONFIRMED, REVERSAL REPLICATED, SIZE-DOMINATED
and DEPTH-REACH SPLIT. The last notebook cell lists these numbers side by side. All numbers are selection data, not
confirmation.

## Layout

| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook (executed; loads the data from GitHub, falling back to the local file) |
| `mini_demo_data.json` | 100 EXP5 frame concepts (17 per field group, 15 MATHDEC; transient concepts oversampled to 2 per group). Per concept: B5 baseline, outcomes, early traits and per-year records (sparse HOME topic co-usage vector, stored CONS/EMB/SOC, grounded volume V(t)). The metadata also carries the full-run headline numbers. |
| `make_mini_demo_data.py` | builds `mini_demo_data.json` from the source experiment's parquet caches, using that experiment's own `lib/cheng.py` and `lib/ego.py` code (SELF-topic rule, yearly vectors), and asserts that the recomputed CONS equals the stored CONS |
| `.aii/manifest.yaml` | storage manifest (no heavy paths) |

## How to run

* **Colab**: open `code_demo.ipynb` and run all cells. The install cell adds only `pyfixest==0.60.0` and uses Colab's
  own numpy, pandas, scipy, statsmodels and matplotlib.
* **Locally** (Python 3.12):
  `jupyter nbconvert --to notebook --execute code_demo.ipynb`. Outside Colab, the install cell also pins
  numpy 2.0.2, pandas 2.2.2, scipy 1.16.3, statsmodels 0.14.6 and matplotlib 3.10.0 to Colab's versions.
* **Rebuilding the demo data** needs the source run's caches, which are not included here:
  `python make_mini_demo_data.py` (dependencies: numpy, pandas, pyarrow, scipy, igraph, snowballstemmer, loguru).

## Restoring removed files

No files are marked `delete` in `.aii/manifest.yaml`, so nothing needs restoring. Every file listed above is kept in the
repository.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; du -sh .
```

### [71] TOOL RESULT — Bash · 2026-09-29 11:41:13 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n3.4M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [72] ASSISTANT · 2026-09-29 11:41:23 UTC

```
I built the demo notebook and its 100-concept data file. The notebook runs cleanly in the Colab-like test venv in about 52 s, including package installs, using the original bootstrap counts.

The artifact's `method.py` only calls the step modules in `lib/`, so the notebook copies those step functions into cells, with markdown between sections. The code is changed only where it has to be:
- it reads the loaded `data` instead of the parquet files;
- it runs sequentially instead of in a process pool;
- it skips the parts the demo has no data for (see below).

**What the notebook runs:**
- **Consistency measure:** it recomputes CONS and CONS_r from the per-year topic vectors. They match the full run exactly (difference 0), and so do the early-trait averages.
- **Test A (Cheng's panel):** consistency predicts +27% next-year volume per SD without a size control and +1.8% with one. The ratio of the two is 0.08, so the demo also comes out size-dominated (full run: +83%, +1.3%, 0.021).
- **Test B (reach and depth):** the reach correlation is −0.26, the same sign as the full run's −0.069, but with 100 concepts its confidence interval just reaches 0.
- **Tests D and E and the verdict:** the demo verdict is size-dominated plus null-reversal, where the full run confirms the reversal. The last cell puts every demo number next to its full-run value and shows a 3-panel figure.

**Limitations:**
- **Two steps are left out:** the construct-identity check and Test C need upstream tables from an earlier experiment that are not in the demo.
- **Some measures come from the full run:** the embeddedness and co-author tie-density numbers are loaded from the stored run rather than recomputed, because they need a topic-association matrix and author lists that aren't shipped.
- **ALL-papers panel dropped:** Test A runs on each concept's home-field papers only; the all-papers version needs those same missing measures.
- **Transient concepts are oversampled:** they make up about 4% of the full set but 12 of the 100 here (2 per field group). Without this the transience outcome was zero for every demo concept and couldn't be tested. The data file's metadata and the README both say so.
- **Single-group results are skipped:** each field group has only about 17 concepts, below the original minimum, so the per-group results and the pooling across groups don't run.

Nothing in the workspace is large, so the storage manifest has no entries. The README explains the layout and how to run the notebook, and the output JSON is written.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `make_mini_demo_data.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
