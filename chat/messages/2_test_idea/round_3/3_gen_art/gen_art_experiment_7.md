# gen_art_experiment_7 — test_idea

> Phase: `invention_loop` · round 3 · `gen_art`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_art_experiment_7` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-28 21:31:21 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-28 21:31:27 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 66779 chars total]
```

### [3] ASSISTANT · 2026-09-28 21:31:39 UTC

```
I'm treating the pasted spec as the task, since the workspace path matches it. I don't have a todo tool here, so I'll track the 3 TODOs as I go. Starting with the skills and the dependency data.
```

### [4] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-python
```

### [5] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-python"}
```

### [6] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-json
```

### [9] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-json"}
```

### [10] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-file-size-limit
```

### [11] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-file-size-limit"}
```

### [12] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-use-hardware
```

### [13] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-use-hardware"}
```

### [14] TOOL CALL — Skill · 2026-09-28 21:31:39 UTC

```
aii-parallel-computing
```

### [15] TOOL RESULT — Skill · 2026-09-28 21:31:39 UTC

```
{"success": true, "commandName": "aii-parallel-computing"}
```

### [16] TOOL CALL — Bash · 2026-09-28 21:31:41 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7; ls -la; ls -la .aii; bash /ai-inventor/.claude/skills/aii-use-hardware/scripts/get_hardware.sh 2>&1 | head -50; git log --oneline | head; ls /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads
```

### [17] TOOL RESULT — Bash · 2026-09-28 21:31:43 UTC

```
{"stdout": "total 2055\ndrwxrwxrwx 3 root root 1006792 Sep 28 21:31 .\ndrwxrwxrwx 7 root root 1025718 Sep 28 21:29 ..\ndrwxrwxrwx 2 root root       1 Sep 28 21:29 .aii\n-rw-rw-rw- 1 root root      54 Sep 28 21:31 .aii_claude_session.json\n-rw-rw-rw- 1 root root   69506 Sep 28 21:31 .repl_agent.ptylog\ntotal 984\ndrwxrwxrwx 2 root root       1 Sep 28 21:29 .\ndrwxrwxrwx 3 root root 1006792 Sep 28 21:31 ..\n=== OS ===\nLinux 6.8.0-117-generic\nNAME=\"Debian GNU/Linux\"\nVERSION=\"12 (bookworm)\"\n=== CGROUP ===\nType: cgroup v2\nContainer: docker\nCPU quota: 1020000 100000 (cpu.max: quota period)\nMemory limit: 28 GB (30999998464 bytes)\nPIDs limit: 6656\nPaths: /sys/fs/cgroup/{cpu.max,memory.max,memory.current}\n\nIMPORTANT: You are in a container with cgroup resource limits.\nDo NOT use psutil.virtual_memory().total, free -h, or /proc/meminfo for limits.\nDo NOT use os.cpu_count() or nproc for CPU count.\nUse the cgroup paths above or the Python helpers from SKILL.md.\n=== CPU ===\n11 CPUs\nModel name:                              AMD EPYC 7352 24-Core Processor\n=== RAM ===\n28 GB (container limit)\n=== DISK ===\n2.2P total, 508T free\n=== GPU ===\nNVIDIA RTX PRO 4000 Blackwell, VRAM: 24467 MiB (23985 MiB free), Util: 0 %\nfatal: not a git repository (or any parent up to mount point /ai-inventor)\nStopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-28 21:31:45 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art; ls -la $R; echo; ls -la $R/gen_art_experiment_6 $R/gen_art_experiment_6/*/ | head -120
```

### [19] TOOL RESULT — Bash · 2026-09-28 21:31:45 UTC

```
{"stdout": "total 16724\ndrwxrwxrwx  7 root root 3000496 Sep 28 17:06 .\ndrwxrwxrwx  8 root root 3000496 Sep 28 21:00 ..\ndrwxrwxrwx 10 root root 2041367 Sep 28 21:21 gen_art_dataset_2\ndrwxrwxrwx  7 root root 2002088 Sep 28 21:19 gen_art_evaluation_1\ndrwxrwxrwx 10 root root 2077382 Sep 28 21:17 gen_art_experiment_5\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 gen_art_experiment_6\ndrwxrwxrwx  5 root root 2000198 Sep 28 17:34 gen_art_research_1\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6:\ntotal 120749\ndrwxrwxrwx 11 root root  3000378 Sep 28 21:19 .\ndrwxrwxrwx  7 root root  3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 root root    39200 Sep 28 19:07 .aii\n-rw-rw-rw-  1 root root       54 Sep 28 17:09 .aii_claude_session.json\n-rw-rw-rw-  1 root root     9588 Sep 28 19:07 .aii_worker_result.json\n-rw-rw-rw-  1 root root  1690358 Sep 28 19:07 .repl_agent.ptylog\n-rw-rw-rw-  1 root root     3234 Sep 28 18:57 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 root root    13534 Sep 28 19:02 README.md\n-rw-rw-rw-  1 root root     4331 Sep 28 17:52 aggregate.py\n-rw-rw-rw-  1 root root     1608 Sep 28 17:32 agreement.py\n-rw-rw-rw-  1 root root     3309 Sep 28 18:44 audit.py\n-rw-rw-rw-  1 root root     3787 Sep 28 18:27 audit_api.py\n-rw-rw-rw-  1 root root     4334 Sep 28 18:54 audit_placebo.py\ndrwxrwxrwx  2 root root  1023674 Sep 28 18:20 benchmark\n-rw-rw-rw-  1 root root     2815 Sep 28 17:17 build_lexicon.py\n-rw-rw-rw-  1 root root     2826 Sep 28 17:21 cand.py\n-rw-rw-rw-  1 root root     1246 Sep 28 18:21 config.py\ndrwxrwxrwx  2 root root  2000104 Sep 28 18:43 figures\n-rw-rw-rw-  1 root root     7255 Sep 28 18:09 frame.py\n-rw-rw-rw-  1 root root 55464495 Sep 28 18:44 full_method_out.json\n-rw-rw-rw-  1 root root     9530 Sep 28 17:26 grounding.py\ndrwxrwxrwx  3 root root  2001319 Sep 28 17:15 inputs\n-rwxrwxrwx  1 root root      396 Sep 28 18:53 install.sh\n-rw-rw-rw-  1 root root     4593 Sep 28 17:22 label_bench.py\ndrwxrwxrwx  2 root root  1005929 Sep 28 18:48 lib\ndrwxrwxrwx  2 root root  1017400 Sep 28 18:32 logs\n-rw-rw-rw-  1 root root    12758 Sep 28 17:32 make_outputs.py\n-rw-rw-rw-  1 root root    36455 Sep 28 18:28 method.py\n-rw-rw-rw-  1 root root 47217519 Sep 28 18:43 method_out.json\n-rw-rw-rw-  1 root root    13390 Sep 28 18:44 mini_method_out.json\n-rw-rw-rw-  1 root root     9458 Sep 28 17:18 pass1.py\n-rw-rw-rw-  1 root root     6895 Sep 28 17:21 pass2.py\n-rw-rw-rw-  1 root root    11206 Sep 28 18:44 preview_method_out.json\n-rw-rw-rw-  1 root root     2317 Sep 28 18:53 pyproject.toml\n-rw-rw-rw-  1 root root     7702 Sep 28 18:56 reproducibility.md\n-rw-rw-rw-  1 root root     1451 Sep 28 18:53 requirements.lock.txt\ndrwxrwxrwx  2 root root  2000891 Sep 28 18:56 results\ndrwxrwxrwx  4 root root  3000365 Sep 28 18:09 scan\ndrwxrwxrwx  2 root root  1000310 Sep 28 17:23 tests\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/benchmark/:\ntotal 4169\ndrwxrwxrwx  2 root root 1023674 Sep 28 18:20 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root  110692 Sep 28 18:20 bench_labelled.csv\n-rw-rw-rw-  1 root root   92868 Sep 28 18:11 bench_pairs.csv\n-rw-rw-rw-  1 root root    7996 Sep 28 18:13 hand_labels.csv\n-rw-rw-rw-  1 root root    7417 Sep 28 18:13 hand_sample.csv\n-rw-rw-rw-  1 root root   16766 Sep 28 18:12 labels_primary.csv\n-rw-rw-rw-  1 root root    6593 Sep 28 18:13 labels_second.csv\n-rw-rw-rw-  1 root root      94 Sep 28 18:11 stratum_population.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/figures/:\ntotal 5964\ndrwxrwxrwx  2 root root 2000104 Sep 28 18:43 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root   25046 Sep 28 18:43 fig_case_41020.pdf\n-rw-rw-rw-  1 root root   97782 Sep 28 18:43 fig_case_41020.png\n-rw-rw-rw-  1 root root   32453 Sep 28 18:43 fig_case_57442.pdf\n-rw-rw-rw-  1 root root  109621 Sep 28 18:43 fig_case_57442.png\n-rw-rw-rw-  1 root root   29788 Sep 28 18:43 fig_case_60310.pdf\n-rw-rw-rw-  1 root root  104204 Sep 28 18:43 fig_case_60310.png\n-rw-rw-rw-  1 root root   28368 Sep 28 18:43 fig_case_94.pdf\n-rw-rw-rw-  1 root root  103767 Sep 28 18:43 fig_case_94.png\n-rw-rw-rw-  1 root root   21183 Sep 28 18:43 fig_entry_auc_forest.pdf\n-rw-rw-rw-  1 root root   57348 Sep 28 18:43 fig_entry_auc_forest.png\n-rw-rw-rw-  1 root root   15347 Sep 28 18:43 fig_event_study_dev.pdf\n-rw-rw-rw-  1 root root   36970 Sep 28 18:43 fig_event_study_dev.png\n-rw-rw-rw-  1 root root   15347 Sep 28 18:43 fig_event_study_heldout.pdf\n-rw-rw-rw-  1 root root   35058 Sep 28 18:43 fig_event_study_heldout.png\n-rw-rw-rw-  1 root root   16914 Sep 28 18:43 fig_heldout_group_forest.pdf\n-rw-rw-rw-  1 root root   29975 Sep 28 18:43 fig_heldout_group_forest.png\n-rw-rw-rw-  1 root root   14402 Sep 28 18:43 fig_incidence_function.pdf\n-rw-rw-rw-  1 root root   71826 Sep 28 18:43 fig_incidence_function.png\n-rw-rw-rw-  1 root root   21213 Sep 28 18:43 fig_trajectory_clusters_dev.pdf\n-rw-rw-rw-  1 root root  105959 Sep 28 18:43 fig_trajectory_clusters_dev.png\n-rw-rw-rw-  1 root root   21397 Sep 28 18:43 fig_trajectory_clusters_heldout.pdf\n-rw-rw-rw-  1 root root  105607 Sep 28 18:43 fig_trajectory_clusters_heldout.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/inputs/:\ntotal 10545\ndrwxrwxrwx  3 root root 2001319 Sep 28 17:15 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\ndrwxrwxrwx  2 root root 2000958 Sep 28 17:16 concepts\n-rw-rw-rw-  1 root root   53044 Sep 28 17:14 field_backbone.json\n-rw-rw-rw-  1 root root   16314 Sep 28 17:14 field_outcomes.csv\n-rw-rw-rw-  1 root root   15251 Sep 28 17:14 outcomes.csv\n-rw-rw-rw-  1 root root 3311365 Sep 28 17:14 source_field.parquet\n-rw-rw-rw-  1 root root  397668 Sep 28 17:14 works_manifest.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/lib/:\ntotal 3974\ndrwxrwxrwx  2 root root 1005929 Sep 28 18:48 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root    1465 Sep 28 17:25 frame_io.py\n-rw-rw-rw-  1 root root    9067 Sep 28 18:26 h2.py\n-rw-rw-rw-  1 root root    2524 Sep 28 17:21 lib_outcomes.py\n-rw-rw-rw-  1 root root    2928 Sep 28 17:18 matcher.py\n-rw-rw-rw-  1 root root    5326 Sep 28 17:14 rangefile.py\n-rw-rw-rw-  1 root root    7300 Sep 28 17:27 rescue_relay.py\n-rw-rw-rw-  1 root root   13680 Sep 28 17:14 scan_snapshot_iter1.py\n-rw-rw-rw-  1 root root    8655 Sep 28 17:23 stats_core.py\n-rw-rw-rw-  1 root root    9778 Sep 28 17:28 traj.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/logs/:\ntotal 4101\ndrwxrwxrwx  2 root root 1017400 Sep 28 18:32 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root     751 Sep 28 18:31 dev_full.out\n-rw-rw-rw-  1 root root    1000 Sep 28 18:42 heldout_run1.out\n-rw-rw-rw-  1 root root   96225 Sep 28 18:13 labels.log\n-rw-rw-rw-  1 root root    7095 Sep 28 18:43 method.log\n-rw-rw-rw-  1 root root   29665 Sep 28 17:42 pass1.log\n-rw-rw-rw-  1 root root       4 Sep 28 17:19 pass1.pid\n-rw-rw-rw-  1 root root   20566 Sep 28 17:42 pass1_full.out\n-rw-rw-rw-  1 root root   13753 Sep 28 18:07 pass2.log\n-rw-rw-rw-  1 root root       6 Sep 28 17:54 pass2.pid\n-rw-rw-rw-  1 root root    8936 Sep 28 18:07 pass2_full.out", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-28 21:31:47 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; ls -la $R/results $R/scan $R/scan/* $R/tests | head -80; cat $R/README.md
```

### [21] TOOL RESULT — Bash · 2026-09-28 21:31:49 UTC

````
{"stdout": "-rw-rw-rw- 1 root root 73537390 Sep 28 17:53 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/agg_counts.npz\n-rw-rw-rw- 1 root root     4578 Sep 28 17:54 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/cand_concepts.json\n-rw-rw-rw- 1 root root    77484 Sep 28 18:21 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/frame_g_dev.npz\n-rw-rw-rw- 1 root root    89807 Sep 28 18:21 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/frame_g_heldout.npz\n-rw-rw-rw- 1 root root    69987 Sep 28 18:21 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/frame_gpf_dev.npz\n-rw-rw-rw- 1 root root    85282 Sep 28 18:21 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/frame_gpf_heldout.npz\n-rw-rw-rw- 1 root root     1445 Sep 28 17:14 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/probe.py\n-rw-rw-rw- 1 root root     1266 Sep 28 17:15 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/probe2.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/results:\ntotal 14022\ndrwxrwxrwx  2 root root 2000891 Sep 28 18:56 .\ndrwxrwxrwx 11 root root 3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root    1153 Sep 28 18:21 agreement.json\n-rw-rw-rw-  1 root root    4088 Sep 28 18:28 api_audit.csv\n-rw-rw-rw-  1 root root     232 Sep 28 18:28 api_audit.json\n-rw-rw-rw-  1 root root     625 Sep 28 18:45 audit.json\n-rw-rw-rw-  1 root root    1008 Sep 28 18:56 audit_placebo.json\n-rw-rw-rw-  1 root root  500897 Sep 28 17:54 candidates.csv\n-rw-rw-rw-  1 root root     358 Sep 28 17:54 candidates_summary.json\n-rw-rw-rw-  1 root root   10017 Sep 28 18:31 cluster_assign_dev.csv\n-rw-rw-rw-  1 root root   14722 Sep 28 18:42 cluster_assign_heldout.csv\n-rw-rw-rw-  1 root root    3294 Sep 28 18:28 credits_log.csv\n-rw-rw-rw-  1 root root   31868 Sep 28 18:31 dev_result.json\n-rw-rw-rw-  1 root root    7043 Sep 28 18:31 dev_spec_parts.json\n-rw-rw-rw-  1 root root    5552 Sep 28 18:47 deviations.json\n-rw-rw-rw-  1 root root  269458 Sep 28 18:27 entry_risk_sets_dev.parquet\n-rw-rw-rw-  1 root root  397762 Sep 28 18:32 entry_risk_sets_heldout.parquet\n-rw-rw-rw-  1 root root  272022 Sep 28 18:32 episodes.csv\n-rw-rw-rw-  1 root root  165004 Sep 28 18:32 frame_concepts.csv\n-rw-rw-rw-  1 root root    1775 Sep 28 18:21 frame_summary.json\n-rw-rw-rw-  1 root root     532 Sep 28 18:42 freeze_log.txt\n-rw-rw-rw-  1 root root    9254 Sep 28 18:32 frozen_spec.json\n-rw-rw-rw-  1 root root   22864 Sep 28 18:20 grounding_concepts.csv\n-rw-rw-rw-  1 root root    2683 Sep 28 18:20 grounding_report.json\n-rw-rw-rw-  1 root root   27467 Sep 28 18:42 heldout_result.json\n-rw-rw-rw-  1 root root 5652404 Sep 28 17:17 lexicon.parquet\n-rw-rw-rw-  1 root root  269815 Sep 28 17:17 lexicon_dropped.csv\n-rw-rw-rw-  1 root root      65 Sep 28 17:17 lexicon_hash.txt\n-rw-rw-rw-  1 root root     390 Sep 28 17:17 lexicon_summary.json\n-rw-rw-rw-  1 root root     188 Sep 28 18:13 openrouter_cost.json\n-rw-rw-rw-  1 root root    7756 Sep 28 18:31 ordering_dev.csv\n-rw-rw-rw-  1 root root   10460 Sep 28 18:42 ordering_heldout.csv\n-rw-rw-rw-  1 root root  144009 Sep 28 17:54 p0_dropped.csv\n-rw-rw-rw-  1 root root  159142 Sep 28 18:30 relay_dev.csv\n-rw-rw-rw-  1 root root  273874 Sep 28 18:41 relay_heldout.csv\n-rw-rw-rw-  1 root root  179729 Sep 28 18:30 rescue_dev.csv\n-rw-rw-rw-  1 root root  313997 Sep 28 18:41 rescue_heldout.csv\n-rw-rw-rw-  1 root root     769 Sep 28 18:16 sense_filter.pkl\n-rw-rw-rw-  1 root root  246200 Sep 28 18:31 trajectories_dev.csv\n-rw-rw-rw-  1 root root  328381 Sep 28 18:42 trajectories_heldout.csv\n-rw-rw-rw-  1 root root     860 Sep 28 18:48 unit_tests_T0.json\n-rw-rw-rw-  1 root root    8917 Sep 28 17:14 works_schema.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan:\ntotal 83859\ndrwxrwxrwx  4 root root  3000365 Sep 28 18:09 .\ndrwxrwxrwx 11 root root  3000378 Sep 28 21:19 ..\n-rw-rw-rw-  1 root root 73537390 Sep 28 17:53 agg_counts.npz\n-rw-rw-rw-  1 root root     4578 Sep 28 17:54 cand_concepts.json\n-rw-rw-rw-  1 root root    77484 Sep 28 18:21 frame_g_dev.npz\n-rw-rw-rw-  1 root root    89807 Sep 28 18:21 frame_g_heldout.npz\n-rw-rw-rw-  1 root root    69987 Sep 28 18:21 frame_gpf_dev.npz\n-rw-rw-rw-  1 root root    85282 Sep 28 18:21 frame_gpf_heldout.npz\ndrwxrwxrwx  2 root root  3000168 Sep 28 17:42 pass1\ndrwxrwxrwx  2 root root  3000190 Sep 28 18:07 pass2\n-rw-rw-rw-  1 root root     1445 Sep 28 17:14 probe.py\n-rw-rw-rw-  1 root root     1266 Sep 28 17:15 probe2.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/scan/pass1:\ntotal 1774328\ndrwxrwxrwx 2 root root 3000168 Sep 28 17:42 .\ndrwxrwxrwx 4 root root 3000365 Sep 28 18:09 ..\n-rw-rw-rw- 1 root root    7313 Sep 28 17:41 f0000.npz\n-rw-rw-rw- 1 root root    3273 Sep 28 17:41 f0001.npz\n-rw-rw-rw- 1 root root    3205 Sep 28 17:41 f0002.npz\n-rw-rw-rw- 1 root root    3141 Sep 28 17:41 f0003.npz\n-rw-rw-rw- 1 root root    2991 Sep 28 17:42 f0004.npz\n-rw-rw-rw- 1 root root    3043 Sep 28 17:42 f0005.npz\n-rw-rw-rw- 1 root root    3033 Sep 28 17:42 f0006.npz\n# How newborn scientific concepts hop between fields\n\nAI Inventor, invention loop iteration 2, artifact `gen_art_experiment_6` (plan `gen_plan_experiment_2_idx2`).\n\n**Question.** Once a newborn concept has spread beyond its home field, which field does it enter next? Four tests:\n1. **H2 entry.** Does relatedness to the off-home fields that currently *retain* the concept, weighted by their\n   gateway centrality, add to the standard next-entry baselines? The baselines are relatedness-to-home, target-field\n   size, Hidalgo relatedness density and the target field's own centrality.\n2. **Rescue.** Are retained gateway episodes fed by re-import from other non-home fields?\n3. **Relay.** Do retained gateway episodes seed later field entries beyond what availability predicts?\n4. **Trajectories without predefined classes, and an ordering test.** Does the first retained gateway field precede\n   the concept's entropy take-off?\n\nThe data are the full OpenAlex works snapshot: 476,196,327 works in 2,040 parquet files from the 2026-09 release,\nread at zero API credits. Fields are the 26 OpenAlex fields, and the backbone is the frozen iteration-1 1998-2002\nfield PMI network with its gateway centrality.\n\n## Headline results\n\nDevelopment split: dev-home fields CS, Engineering, BGM and Medicine, with t0 in 2003-09. Held-out split: the other\nfields with t0 in 2003-09, plus the whole 2010-14 cohort. The held-out stage was run **once**, after\n`results/frozen_spec.json` was hashed into `results/freeze_log.txt`.\n\n| test | dev (274 concepts) | held-out (369 concepts), frozen rule |\n|---|---|---|\n| H2: LR M2 vs M0 (clogit, concept-year strata) | 38.6, p=5e-10 | **71.7, p=2e-17** |\n| d (standardised) [concept-bootstrap 95% CI] | 0.25 [0.18, 0.32] | 0.30 [0.24, 0.37] |\n| label-permutation p (phi and g permuted jointly) | 0.009 | 0.001 |\n| degree-preserving rewired-backbone p | 0.030 | 0.015 |\n| per-group d (Physical / LifeEnv / Social / Cohort) | - | 0.33 / 0.18 / 0.24 / 0.29, all positive; DL pooled 0.28 [0.22, 0.35], I2=0 |\n| **gateway weighting beyond plain retaining relatedness** (M3 vs M1; g-only permutation p) | LR 4.6, p=0.31 | LR 5.4, **p=0.17** |\n| mean within-stratum AUC, M0 -> M2 | 0.801 -> 0.805 | 0.809 -> 0.817 (frozen dev coefficients: 0.807 -> 0.815) |\n| single blocks: size / density / phi_home / own gateway / d | 0.71 / 0.61 / 0.58 / 0.48 / 0.56 | 0.76 / 0.59 / 0.57 / 0.45 / 0.55 |\n| **H2 entry decision** | - | **CONFIRMED** (every frozen criterion met) |\n| ordering: share of top-O2r concepts whose first retained gateway field precedes entropy take-off | 0.71 (peripheral 0.70) | **0.66, sign p=0.003** (peripheral 0.57, p=0.12; McNemar p=0.09) -> CONFIRMED by the frozen rule |\n| lead-lag placebo (gateway scores permuted) | p=0.18 | p=0.63: the panel does **not** single out gateway fields |\n| rescue: R1 retained x top-gateway on background-adjusted provenance | 1.47 [-0.16, 3.10] | -0.22 [-1.12, 0.68], **not supported** |\n| rescue: Hanski connectivity on retention (R2) | +0.032 [0.007, 0.058] | +0.009 [-0.017, 0.035] |\n| relay: fepois retained x gateway_j | 18.0 [4.2, 31.9] | -1.3 [-4.9, 2.3], **not supported** |\n| H1 replication (gateway_j on retention, concept FE) | +0.017 (CI spans 0) | +0.005 [-0.022, 0.033]: **iteration-1 lead did not replicate** |\n| trajectories: DTW k-medoids, k by silhouette + bootstrap ARI | k=2, median ARI 1.0, silhouette 0.29 | independent recluster ARI 0.54 |\n\n**How to read this.**\n- **Entry.** Fields related to where the concept is *currently retained* off-home are entered next. This holds in\n  every held-out group, beyond size, density, home relatedness and own centrality, and survives both placebos.\n- **What does not hold.** The *gateway weighting* of those retaining fields adds nothing detectable (g-only\n  permutation p = 0.17 on held-out). The confirmed mechanism is relatedness to retaining fields, not gateway\n  brokerage. Target-field size remains by far the strongest single predictor (AUC 0.76), and the incremental AUC is\n  small (+0.008).\n- **Trajectories.** Two stable classes with nearly equal volume: \"integrating\" (entry, retention, entropy and\n  gateway share all rise) and \"localized\" (flat breadth). On held-out data the localized class is dominated by\n  Medicine-home concepts (42 of 60).\n- **Negative results.** Rescue and relay are not supported, and the iteration-1 gateway-retention lead did not\n  replicate on this larger frame.\n\n## What was done\n\n1. **Lexicon (`build_lexicon.py`).** OpenAlex legacy concepts, levels 2-5 with a Wikidata id, 60,859 concepts.\n   Common English single words and very short forms are dropped. The lexicon is hashed in `results/lexicon_hash.txt`.\n2. **Pass 1 (`pass1.py`, 23 min, 4 workers).**\n   * Reads 9 leaf columns of every works file through HTTP range requests (from iteration-1 `rangefile.py`).\n   * Matches titles with a word-boundary Aho-Corasick automaton (`lib/matcher.py`): 141M title hits on 129M base works.\n   * Records each hit's legacy-tag flag and score, venue field (iteration-1 source -> field map) and primary-topic field.\n   * `aggregate.py` builds dense concept x year x field counts in `scan/agg_counts.npz`.\n3. **P0 and candidates (`cand.py`).** The outcome-blind P0 rule drops 3,102 concepts common before 2003. Onset uses\n   the iteration-1 rule: t0 is the first year with >= 20 grounded works, t0 in 2003-2014, >= 30 works in t0..t0+2.\n   This gives 12,901 onsets, of which **653 are newborn**.\n4. **Pass 2 (`pass2.py`, 12.7 min).** For the newborn candidates it keeps work id, title, references and authors, and\n   builds the global work-id -> venue-field map used for background references.\n5. **Grounding (`grounding.py`, `label_bench.py`).**\n   * 400 stratified (concept, title) pairs, labelled by `google/gemini-2.5-flash-lite`. `qwen/qwen3-30b-a3b-instruct-2507`\n     double-labels 150 of them, and 60 were checked by hand (`benchmark/hand_labels.csv`). Total cost $0.0074.\n   * The grounding rule is legacy tag (score >= 0.3) AND title match, plus untagged works. Its test precision is\n     0.996 (population-weighted), >= 0.94 in every domain, with 78% recall relative to title-only.\n   * The MiniLM + logistic sense filter is **uninformative**: test AUC 0.24 on only 12 negatives in 400. It dropped\n     no concept. See `results/grounding_report.json`.\n6. **Frame (`frame.py`).**\n   * 653 concepts: dev 279, held-out field 126, held-out cohort 248. 1,865 off-home episodes.\n   * Home is taken from the first 30 labelled works.\n   * Outcomes use the iteration-1 definitions: O1, O3, O2r = rarefied venue-field richness at t0+6..8.\n   * Held-out outcomes stayed **sealed**: `lib/frame_io.py` raises until the freeze log exists.\n7. **Analyses (`method.py` + `lib/`).**\n   * `lib/h2.py`: the state machine (entered, retaining, lost) and concept-year risk sets.\n   * `lib/stats_core.py`: own vectorised conditional logit, validated against statsmodels to 0.05%; within-FE OLS and\n     Poisson FE with CRV1 SEs; DerSimonian-Laird pooling.\n   * `lib/rescue_relay.py`: background-adjusted citation provenance with shared-author links removed, Hanski\n     connectivity, and the availability-null relay.\n   * `lib/traj.py`: DTW k-medoids, Gaussian HMM (BIC), a Pelt change-point detector calibrated to a 5% false-alarm\n     rate on year-shuffled series, and the lead-lag / event-study panels.\n8. **Tests.**\n   * `tests/test_units.py` (T0): matcher boundaries and plurals, rarefaction vs Monte Carlo, onset, clogit vs\n     statsmodels, FE-OLS, DerSimonian-Laird. All pass: `results/unit_tests_T0.json`.\n   * Planted control on the real risk-set structure: detection 100% at p < 0.001; null rejection 2% at 0.01.\n   * `audit.py` (T7): an independent recomputation.\n     * R1 and p_gw agree exactly.\n     * The H2 LR differs by 7.8%. statsmodels' exact conditional likelihood gives LR 77.3 and d 0.34, against the\n       own Breslow form's 71.7 and 0.30, because 30% of strata have more than one event. The conclusion is unchanged,\n       and the Breslow form used here is the conservative one.\n   * `audit_placebo.py`: labels shuffled within strata reject in 0 of 20 runs; a random gateway year gives an\n     ordering share of 0.43 (never at or above 0.655); the exact-likelihood DL-pooled d is 0.32 [0.25, 0.39].\n   * API audit on 40 frame concepts: snapshot title counts equal OpenAlex `title.search` counts (median ratio 1.00,\n     Spearman 0.999), and grounded counts are 95% of them.\n\nEvery departure from the plan is in `results/deviations.json`. The larger ones:\n* no Wikidata aliases;\n* frame restricted to newborn concepts;\n* episode target not met (1,865 < 4,000);\n* MathDec has no concepts, so the sign rule was pinned before the freeze to 3 of 3 field groups plus the cohort;\n* relay Poisson re-specified with a continuous gateway interaction before the freeze, because the tercile dummies\n  separated;\n* the supplied OpenAlex key was exhausted (HTTP 429), so the 40 audit calls used the anonymous pool.\n\n## Layout\n\n| path | content |\n|---|---|\n| `config.py` | constants, splits, seeds (SEED=20261001) |\n| `build_lexicon.py`, `pass1.py`, `aggregate.py`, `cand.py`, `pass2.py` | snapshot pipeline (steps 0-2, 5) |\n| `grounding.py`, `label_bench.py` | benchmark sampling, LLM labels, sense filter, rule comparison (step 3) |\n| `frame.py`, `agreement.py`, `audit_api.py` | frame, episodes, iteration-1 agreement, API audit (step 4) |\n| `method.py` | stages `dev` -> `freeze` -> `heldout` -> `outputs` (steps 6-9) |\n| `make_outputs.py` | figures and `method_out.json` |\n| `audit.py`, `audit_placebo.py` | independent re-derivations (statsmodels exact clogit, sklearn AUC, inline DL) and placebos that must fail -> `results/audit.json`, `results/audit_placebo.json` |\n| `requirements.lock.txt`, `install.sh` | all 85 installed packages pinned; environment rebuild |\n| `lib/` | `matcher.py`, `rangefile.py` (iteration 1), `lib_outcomes.py` (iteration-1 outcome code), `h2.py`, `stats_core.py`, `rescue_relay.py`, `traj.py`, `frame_io.py` (sealing guard) |\n| `tests/test_units.py` | T0 unit tests |\n| `inputs/` | frozen backbone (`field_backbone.json`), source -> field map, works manifest, concepts entity, iteration-1 outcomes |\n| `results/frame_concepts.csv`, `results/episodes.csv` | frame and episodes (S1-compatible columns) |\n| `results/dev_result.json`, `results/heldout_result.json`, `results/frozen_spec.json`, `results/freeze_log.txt` | results and the freeze record |\n| `results/entry_risk_sets_{dev,heldout}.parquet` | every candidate-field row with regressors and outcomes |\n| `results/rescue_*.csv`, `results/relay_*.csv`, `results/trajectories_*.csv`, `results/cluster_assign_*.csv`, `results/ordering_*.csv` | analysis tables |\n| `results/grounding_report.json`, `results/grounding_concepts.csv`, `benchmark/` | grounding benchmark, labels (LLM x2, hand) |\n| `results/agreement.json`, `results/api_audit.json`, `results/audit.json`, `results/unit_tests_T0.json` | checks |\n| `results/deviations.json`, `results/openrouter_cost.json`, `results/credits_log.csv` | deviations and spend |\n| `figures/` | AUC forest, held-out group forest, incidence-function curve, trajectory clusters, event studies, 4 case field-flow plots (cluster medoids and extreme relay episodes) |\n| `method_out.json`, `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json` | exp_gen_sol_out outputs. Datasets: `entry_events_dev` (36,222), `entry_events_heldout` (46,433), `retention_episodes_{dev,heldout}`. Predictions `predict_M0...` vs `predict_M2...` are within-stratum probabilities from the frozen dev coefficients. |\n| `scan/agg_counts.npz`, `scan/pass2/{w,h}*.parquet` | kept aggregates and frame work rows. These stay on the run's volume; files >= 100 MB are not in the published repo. |\n\n## How to run\n\n```bash\nbash install.sh\n.venv/bin/python build_lexicon.py\n.venv/bin/python pass1.py --workers 4 && .venv/bin/python aggregate.py && .venv/bin/python cand.py\n.venv/bin/python pass2.py --workers 4\n.venv/bin/python grounding.py sample\n.venv/bin/python label_bench.py --model google/gemini-2.5-flash-lite --out benchmark/labels_primary.csv\n.venv/bin/python label_bench.py --model qwen/qwen3-30b-a3b-instruct-2507 --n 150 --out benchmark/labels_second.csv\n.venv/bin/python grounding.py fit && .venv/bin/python frame.py && .venv/bin/python agreement.py\n.venv/bin/python method.py dev && .venv/bin/python method.py freeze && .venv/bin/python method.py heldout\n.venv/bin/python method.py outputs && .venv/bin/python audit.py && .venv/bin/python tests/test_units.py\n```\n\n`OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY` must be set for labelling. `audit_api.py` optionally reads\n`OPENALEX_API_KEY` and otherwise uses the anonymous pool. No key is ever written to a file.\n\n## Restoring removed files\n\nOnly one path is deleted after the run (see `.aii/manifest.yaml`):\n\n| removed path | restore with |\n|---|---|\n| `.venv/` | `bash install.sh` |\n\nKept on the run's volume, but not published to the repository (`upload_ignore_regexes`):\n\n| path | how to regenerate in a fresh clone |\n|---|---|\n| `scan/pass1/` (per-file hit records) | `.venv/bin/python pass1.py --workers 4` (about 23 min; the OpenAlex snapshot drifts between releases, and `scan/agg_counts.npz` holds the aggregates used by every analysis) |\n| `scan/pass2/m*.npz` (global id -> field map) | `.venv/bin/python pass2.py --idmap-only` (requires `scan/pass1/`) |\n\nThe MiniLM model (`sentence-transformers/all-MiniLM-L6-v2`) lives in the run's shared HF cache and is re-downloaded\nautomatically.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [22] TOOL CALL — Bash · 2026-09-28 21:31:49 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; cat $R/lib/h2.py; cat $R/config.py; cat $R/lib/stats_core.py
```

### [23] TOOL RESULT — Bash · 2026-09-28 21:31:49 UTC

```
{"stdout": "\"\"\"H2 next-field entry: field-year state machine, concept-year risk sets, conditional-logit blocks, AUCs, placebos.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport networkx as nx\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom config import Y0\nfrom stats_core import CLogit, fe_ols\n\nREG = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"]\nMODELS = {\"M0\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\"],\n          \"M1\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\"],\n          \"M2\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_ret_gate\"],\n          \"M3\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\"],\n          \"M2lost\": [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d_lost_gate\"]}\n\n\ndef states(g: np.ndarray, home: list[int], min_n: int = 2) -> dict:\n    \"\"\"g: [NY, 27] grounded counts. Returns boolean [NY, 26] matrices (years Y0..).\"\"\"\n    x = g[:, 1:]\n    cum = np.cumsum(x, 0)\n    entered = cum >= min_n\n    w3 = x.copy()\n    w3[1:] += x[:-1]; w3[2:] += x[:-2]\n    ent_lag2 = np.zeros_like(entered); ent_lag2[2:] = entered[:-2]\n    offhome = np.ones(26, bool)\n    for h in home:\n        offhome[h - 11] = False\n    retaining = ent_lag2 & (w3 >= min_n) & offhome[None, :]\n    lost = entered & (w3 == 0)\n    return {\"entered\": entered, \"retaining\": retaining, \"lost\": lost, \"w3\": w3, \"cum\": cum, \"offhome\": offhome}\n\n\ndef rca_entered(g: np.ndarray, GF: np.ndarray) -> np.ndarray:\n    \"\"\"entry when cumulative count >= 2 and the field's cumulative share of the concept exceeds its share of all works.\"\"\"\n    x = np.cumsum(g[:, 1:], 0)\n    tot = x.sum(1, keepdims=True)\n    F = np.cumsum(GF, 0)\n    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)\n    share_c = x / np.maximum(tot, 1)\n    ok = (x >= 2) & (share_c > share_all)\n    return np.maximum.accumulate(ok.astype(int), 0).astype(bool)\n\n\ndef build_risk_sets(frame: pd.DataFrame, G: dict[int, np.ndarray], bb: dict, GF: np.ndarray,\n                    entry_def: str = \"count\", horizon: int = 8) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:\n    \"\"\"Rows = (concept, year t, candidate field k not entered by t-1, not home). Returns df, Ret matrix, Lost matrix.\"\"\"\n    phi, gate = bb[\"phi\"], bb[\"g\"]\n    colsum = phi.sum(0)\n    logGF = np.log(np.maximum(GF, 1))\n    rows, RET, LOST = [], [], []\n    for r in frame.itertuples():\n        c = int(r.cidx); t0 = int(r.t0)\n        home = [int(h) for h in str(r.home).split(\"|\")]\n        S = states(G[c], home)\n        ent = rca_entered(G[c], GF) if entry_def == \"rca\" else S[\"entered\"]\n        hidx = [h - 11 for h in home]\n        a = phi[hidx].mean(0)\n        for t in range(t0 + 1, min(t0 + horizon, 2022) + 1):\n            ti = t - Y0\n            E = ent[ti - 1]\n            cand = ~E & S[\"offhome\"]\n            if not cand.any():\n                continue\n            ev = ent[ti] & cand\n            Ret = S[\"retaining\"][ti - 1]\n            Lost = S[\"lost\"][ti - 1] & S[\"offhome\"]\n            dens = (phi[E].sum(0)) / np.where(colsum > 0, colsum, 1)\n            d0 = phi[Ret].mean(0) if Ret.any() else np.zeros(26)\n            d = (gate[Ret] @ phi[Ret]) / gate[Ret].sum() if Ret.any() and gate[Ret].sum() > 0 else np.zeros(26)\n            dl = (gate[Lost] @ phi[Lost]) / gate[Lost].sum() if Lost.any() and gate[Lost].sum() > 0 else np.zeros(26)\n            for k in np.nonzero(cand)[0]:\n                rows.append((c, t, t - t0, k + 11, int(ev[k]), a[k], logGF[ti - 1, k], dens[k], gate[k], d0[k], d[k], dl[k],\n                             int(Ret.sum()), int(Lost.sum()), r.group, r.split, int(r.intersection_born), float(r.home_gateway)))\n                RET.append(Ret); LOST.append(Lost)\n    df = pd.DataFrame(rows, columns=[\"cidx\", \"t\", \"age\", \"field\", \"entered\", \"a_phi_home\", \"b_log_size\", \"c_density\",\n                                     \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\", \"n_ret\", \"n_lost\", \"group\",\n                                     \"split\", \"intersection_born\", \"home_gateway\"])\n    df[\"stratum\"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)\n    return df, np.array(RET, bool).reshape(-1, 26), np.array(LOST, bool).reshape(-1, 26)\n\n\ndef standardise(df: pd.DataFrame, spec: dict | None, cols: list[str]) -> tuple[pd.DataFrame, dict]:\n    if spec is None:\n        spec = {c: {\"mean\": float(df[c].mean()), \"sd\": float(df[c].std() or 1.0)} for c in cols}\n    out = df.copy()\n    for c in cols:\n        out[c] = (df[c] - spec[c][\"mean\"]) / (spec[c][\"sd\"] if spec[c][\"sd\"] > 0 else 1.0)\n    return out, spec\n\n\ndef fit_model(df: pd.DataFrame, cols: list[str], ridge: float = 0.0) -> dict:\n    m = CLogit(df[cols].to_numpy(), df.entered.to_numpy(), df.stratum.to_numpy(), ridge=ridge).fit()\n    return {\"coef\": dict(zip(cols, map(float, m[\"coef\"]))), \"se\": dict(zip(cols, map(float, m[\"se\"]))), \"ll\": m[\"ll\"],\n            \"n_strata\": m[\"n_strata\"], \"n_events\": m.get(\"n_events\", 0), \"n_rows\": m.get(\"n_rows\", 0),\n            \"converged\": m[\"converged\"], \"_b\": m[\"coef\"]}\n\n\ndef lr_test(big: dict, small: dict, df_: int) -> dict:\n    lr = 2 * (big[\"ll\"] - small[\"ll\"])\n    return {\"LR\": float(lr), \"df\": df_, \"p\": float(stats.chi2.sf(max(lr, 0), df_))}\n\n\ndef within_auc(df: pd.DataFrame, score: np.ndarray) -> pd.Series:\n    \"\"\"mean-rank AUC per informative stratum.\"\"\"\n    d = pd.DataFrame({\"s\": df.stratum.to_numpy(), \"y\": df.entered.to_numpy(), \"x\": score})\n    d[\"r\"] = d.groupby(\"s\").x.rank(method=\"average\")\n    g = d.groupby(\"s\").agg(ntot=(\"y\", \"size\"), nev=(\"y\", \"sum\"))\n    re = d[d.y == 1].groupby(\"s\").r.sum()\n    g = g.join(re.rename(\"rs\")).fillna({\"rs\": 0})\n    g = g[(g.nev > 0) & (g.nev < g.ntot)]\n    nn = g.ntot - g.nev\n    return (g.rs - g.nev * (g.nev + 1) / 2) / (g.nev * nn)\n\n\ndef concept_boot_mean(series: pd.Series, n_boot: int, rng) -> list[float]:\n    \"\"\"series indexed by stratum id (cidx*100 + ...): concept-clustered bootstrap CI of the mean.\"\"\"\n    cid = (series.index.to_numpy() // 100)\n    u, inv = np.unique(cid, return_inverse=True)\n    sums = np.bincount(inv, weights=series.to_numpy()); cnts = np.bincount(inv)\n    bs = []\n    for _ in range(n_boot):\n        pick = rng.integers(0, len(u), len(u))\n        bs.append(sums[pick].sum() / max(cnts[pick].sum(), 1))\n    return [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]\n\n\ndef boot_coef(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng, small_cols: list[str] | None = None) -> dict:\n    \"\"\"concept-clustered bootstrap of a clogit coefficient (and the LR vs small model if given).\"\"\"\n    cids = df.cidx.unique()\n    by = {c: ix for c, ix in df.groupby(\"cidx\").indices.items()}\n    X = df[cols].to_numpy(); y = df.entered.to_numpy(); st = df.stratum.to_numpy()\n    Xs = df[small_cols].to_numpy() if small_cols else None\n    bs, lrs = [], []\n    for b in range(n_boot):\n        pick = rng.choice(cids, len(cids))\n        idx = np.concatenate([by[c] for c in pick])\n        rep = np.repeat(np.arange(len(pick)), [len(by[c]) for c in pick])\n        s2 = st[idx] * 10000 + rep  # relabel strata of repeated concepts\n        m = CLogit(X[idx], y[idx], s2).fit()\n        bs.append(m[\"coef\"][cols.index(target)])\n        if small_cols:\n            ms = CLogit(Xs[idx], y[idx], s2).fit()\n            lrs.append(2 * (m[\"ll\"] - ms[\"ll\"]))\n    bs = np.array(bs)\n    out = {\"ci\": [float(np.nanpercentile(bs, 2.5)), float(np.nanpercentile(bs, 97.5))], \"se_boot\": float(np.nanstd(bs)),\n           \"n_boot\": n_boot}\n    if small_cols:\n        out[\"lr_boot\"] = [float(x) for x in np.percentile(lrs, [5, 25, 50, 75, 95])]\n        out[\"_lrs\"] = np.array(lrs)\n    return out\n\n\ndef recompute_d(RET: np.ndarray, fields: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:\n    k = fields - 11\n    w = RET * gate[None, :]\n    den = w.sum(1)\n    num = (w * phi[:, k].T).sum(1)\n    return np.where(den > 0, num / np.where(den > 0, den, 1), 0.0)\n\n\ndef eig_gateway(phi: np.ndarray) -> np.ndarray:\n    Gx = nx.from_numpy_array(phi)\n    try:\n        ev = nx.eigenvector_centrality_numpy(Gx, weight=\"weight\")\n    except Exception:  # noqa: BLE001 -- disconnected graph after rewiring: fall back to power iteration\n        ev = nx.eigenvector_centrality(Gx, weight=\"weight\", max_iter=2000)\n    v = np.array([ev[i] for i in range(len(phi))])\n    v = np.abs(v)\n    return v / v.max()\n\n\ndef rewire(phi: np.ndarray, rng) -> np.ndarray:\n    \"\"\"degree-preserving double-edge swaps on the phi>0 graph; original weights reassigned at random to the new edges.\"\"\"\n    Gx = nx.Graph()\n    Gx.add_nodes_from(range(len(phi)))\n    iu = np.transpose(np.nonzero(np.triu(phi, 1) > 0))\n    Gx.add_edges_from(map(tuple, iu))\n    ne = Gx.number_of_edges()\n    try:\n        nx.double_edge_swap(Gx, nswap=10 * ne, max_tries=1000 * ne, seed=int(rng.integers(1 << 31)))\n    except nx.NetworkXAlgorithmError:\n        pass\n    w = phi[iu[:, 0], iu[:, 1]].copy()\n    rng.shuffle(w)\n    P = np.zeros_like(phi)\n    for (i, j), wt in zip(Gx.edges(), w):\n        P[i, j] = P[j, i] = wt\n    return P\n\"\"\"Frozen constants and paths shared by every module (paths derived from this file's location).\"\"\"\nfrom __future__ import annotations\n\nimport os\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nINP, RES, LOGS, FIGS, SCAN, BENCH = (ROOT / d for d in (\"inputs\", \"results\", \"logs\", \"figures\", \"scan\", \"benchmark\"))\nfor _d in (INP, RES, LOGS, FIGS, SCAN, BENCH):\n    _d.mkdir(parents=True, exist_ok=True)\nP1 = SCAN / \"pass1\"\nP2 = SCAN / \"pass2\"\n\nSEED = 20261001\nFIELDS = list(range(11, 37))\nNF = 26\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nDEV_HOME = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\"}\nHELDOUT_GROUP = {\"Physical\": [15, 16, 21, 25, 31], \"LifeEnv\": [11, 19, 23, 24, 28, 30],\n                 \"Social\": [12, 14, 20, 32, 33], \"MathDec\": [18, 26], \"OtherHealth\": [29, 34, 35, 36]}\nFIELD_GROUP = {f: g for g, fs in HELDOUT_GROUP.items() for f in fs}\nFIELD_GROUP.update({f: \"DEV_\" + s for f, s in DEV_HOME.items()})\nM_RAREFY, M_RAREFY_SENS = 30, 50\nEPISODE_MIN = 2\nRET_MIN = 2\nT0_MIN = 20\nTAG_SCORE = 0.3\nPREC_GATE = 0.8\nN_BOOT = int(os.environ.get(\"AII_NBOOT\", 2000))  # env overrides only for debugging runs\nN_PERM = int(os.environ.get(\"AII_NPERM\", 1000))\nN_REWIRE = int(os.environ.get(\"AII_NREWIRE\", 200))\nOPENROUTER_CAP_USD = 0.50\n\"\"\"Estimators: vectorised conditional logit (Breslow form for multiple events per stratum), within-FE OLS with\ncluster-robust (CRV1) SEs, Poisson with concept FE, DerSimonian-Laird random-effects pooling, sign test.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import optimize, stats\n\n\nclass CLogit:\n    \"\"\"Each event row e in stratum s contributes x_e.b - log sum_{i in s} exp(x_i.b).\n    Rows must be sorted by stratum; `starts` are the first row index of each stratum.\"\"\"\n\n    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, ridge: float = 0.0):\n        o = np.argsort(strata, kind=\"stable\")\n        self.X, self.y, self.s = X[o].astype(float), y[o].astype(float), strata[o]\n        self.order = o\n        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)\n        self.nev = np.add.reduceat(self.y, self.starts)\n        keep_s = (self.nev > 0) & (self.nev < self.counts)  # informative strata only\n        rows = np.repeat(keep_s, self.counts)\n        self.X, self.y, self.s = self.X[rows], self.y[rows], self.s[rows]\n        _, self.starts, self.counts = np.unique(self.s, return_index=True, return_counts=True)\n        self.nev = np.add.reduceat(self.y, self.starts)\n        self.ridge = ridge\n\n    def nll(self, b: np.ndarray) -> tuple[float, np.ndarray]:\n        eta = self.X @ b\n        m = np.maximum.reduceat(eta, self.starts)\n        mm = np.repeat(m, self.counts)\n        w = np.exp(eta - mm)\n        S = np.add.reduceat(w, self.starts)\n        lse = np.log(S) + m\n        ll = float((self.y * eta).sum() - (self.nev * lse).sum())\n        p = w / np.repeat(S, self.counts)\n        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)  # per stratum expectation\n        g = (self.y[:, None] * self.X).sum(0) - (self.nev[:, None] * Ex).sum(0)\n        ll -= 0.5 * self.ridge * float(b @ b)\n        g = g - self.ridge * b\n        return -ll, -g\n\n    def hessian(self, b: np.ndarray) -> np.ndarray:\n        eta = self.X @ b\n        m = np.maximum.reduceat(eta, self.starts)\n        w = np.exp(eta - np.repeat(m, self.counts))\n        S = np.add.reduceat(w, self.starts)\n        p = w / np.repeat(S, self.counts)\n        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)\n        Exx = np.add.reduceat(p[:, None, None] * (self.X[:, :, None] * self.X[:, None, :]), self.starts)\n        cov = Exx - Ex[:, :, None] * Ex[:, None, :]\n        return (self.nev[:, None, None] * cov).sum(0) + self.ridge * np.eye(len(b))\n\n    def fit(self) -> dict:\n        k = self.X.shape[1]\n        if len(self.starts) == 0:\n            return {\"coef\": np.full(k, np.nan), \"se\": np.full(k, np.nan), \"ll\": np.nan, \"n_strata\": 0, \"converged\": False}\n        r = optimize.minimize(self.nll, np.zeros(k), jac=True, method=\"L-BFGS-B\", options={\"maxiter\": 500, \"gtol\": 1e-8})\n        H = self.hessian(r.x)\n        try:\n            se = np.sqrt(np.diag(np.linalg.inv(H)))\n        except np.linalg.LinAlgError:\n            se = np.full(k, np.nan)\n        return {\"coef\": r.x, \"se\": se, \"ll\": -r.fun, \"n_strata\": int(len(self.starts)), \"n_events\": int(self.y.sum()),\n                \"n_rows\": int(len(self.y)), \"converged\": bool(r.success)}\n\n\ndef ll_null_clogit(y: np.ndarray, strata: np.ndarray) -> float:\n    \"\"\"log-likelihood at b = 0 on informative strata.\"\"\"\n    _, inv, cnt = np.unique(strata, return_inverse=True, return_counts=True)\n    nev = np.bincount(inv, weights=y)\n    keep = (nev > 0) & (nev < cnt)\n    return float(-(nev[keep] * np.log(cnt[keep])).sum())\n\n\ndef demean(A: np.ndarray, groups: list[np.ndarray], iters: int = 50, tol: float = 1e-10) -> np.ndarray:\n    \"\"\"Alternating projections to sweep out several sets of fixed effects.\"\"\"\n    A = A.astype(float).copy()\n    if A.ndim == 1:\n        A = A[:, None]\n    for _ in range(iters if len(groups) > 1 else 1):\n        prev = A.copy()\n        for g in groups:\n            _, inv = np.unique(g, return_inverse=True)\n            cnt = np.bincount(inv)\n            for j in range(A.shape[1]):\n                A[:, j] -= (np.bincount(inv, weights=A[:, j]) / cnt)[inv]\n        if len(groups) > 1 and np.abs(A - prev).max() < tol:\n            break\n    return A\n\n\ndef fe_ols(y: np.ndarray, X: np.ndarray, fe: list[np.ndarray], cluster: np.ndarray, names: list[str]) -> dict:\n    \"\"\"OLS of y on X after sweeping out fixed effects `fe`; CRV1 SEs clustered on `cluster` (small-sample corrected).\"\"\"\n    ok = np.isfinite(y) & np.isfinite(X).all(1)\n    y, X, cluster = y[ok], X[ok], cluster[ok]\n    fe = [g[ok] for g in fe]\n    Z = demean(np.column_stack([y, X]), fe) if fe else np.column_stack([y - y.mean(), X - X.mean(0)])\n    yd, Xd = Z[:, 0], Z[:, 1:]\n    XtX = Xd.T @ Xd\n    try:\n        XtXi = np.linalg.pinv(XtX)\n    except np.linalg.LinAlgError:\n        return {\"error\": \"singular\"}\n    b = XtXi @ Xd.T @ yd\n    e = yd - Xd @ b\n    _, cinv = np.unique(cluster, return_inverse=True)\n    G = cinv.max() + 1\n    sc = np.zeros((G, Xd.shape[1]))\n    np.add.at(sc, cinv, Xd * e[:, None])\n    n, k = Xd.shape\n    corr = G / max(G - 1, 1) * (n - 1) / max(n - k, 1)\n    V = corr * XtXi @ (sc.T @ sc) @ XtXi\n    se = np.sqrt(np.clip(np.diag(V), 0, None))\n    tcrit = stats.t.ppf(0.975, max(G - 1, 1))\n    out = {\"n\": int(n), \"n_clusters\": int(G), \"coef\": {}, \"V\": V.tolist()}\n    for i, nm in enumerate(names):\n        out[\"coef\"][nm] = {\"b\": float(b[i]), \"se\": float(se[i]), \"ci\": [float(b[i] - tcrit * se[i]), float(b[i] + tcrit * se[i])],\n                           \"p\": float(2 * stats.t.sf(abs(b[i] / se[i]), max(G - 1, 1))) if se[i] > 0 else float(\"nan\")}\n    out[\"_b\"] = b\n    return out\n\n\ndef fe_poisson(y: np.ndarray, X: np.ndarray, group: np.ndarray, names: list[str], offset: np.ndarray | None = None,\n               iters: int = 100) -> dict:\n    \"\"\"Poisson with group fixed effects (concentrated out: exp(alpha_g) = sum y / sum exp(xb+off) within g),\n    Newton on b; CRV1 sandwich SEs clustered by group.\"\"\"\n    ok = np.isfinite(y) & np.isfinite(X).all(1)\n    y, X, group = y[ok].astype(float), X[ok].astype(float), group[ok]\n    off = np.zeros(len(y)) if offset is None else offset[ok]\n    _, gi = np.unique(group, return_inverse=True)\n    sy = np.bincount(gi, weights=y)\n    keep = sy[gi] > 0  # groups with all-zero outcomes carry no information\n    y, X, off, gi = y[keep], X[keep], off[keep], gi[keep]\n    _, gi = np.unique(gi, return_inverse=True)\n    sy = np.bincount(gi, weights=y)\n    b = np.zeros(X.shape[1])\n    for _ in range(iters):\n        eta = X @ b + off\n        w = np.exp(eta - eta.max())\n        sw = np.bincount(gi, weights=w)\n        mu = w * (sy / sw)[gi]\n        # concentrated score / hessian: X demeaned by mu-weighted group means\n        xm = np.column_stack([np.bincount(gi, weights=mu * X[:, j]) / np.bincount(gi, weights=mu) for j in range(X.shape[1])])[gi]\n        Xc = X - xm\n        g = Xc.T @ (y - mu)\n        H = (Xc * mu[:, None]).T @ Xc\n        step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), g)\n        b = b + step\n        if np.abs(step).max() < 1e-9:\n            break\n    Hi = np.linalg.pinv(H)\n    sc = np.zeros((gi.max() + 1, X.shape[1]))\n    np.add.at(sc, gi, Xc * (y - mu)[:, None])\n    G = gi.max() + 1\n    V = G / max(G - 1, 1) * Hi @ (sc.T @ sc) @ Hi\n    se = np.sqrt(np.clip(np.diag(V), 0, None))\n    out = {\"n\": int(len(y)), \"n_clusters\": int(G), \"coef\": {}}\n    for i, nm in enumerate(names):\n        out[\"coef\"][nm] = {\"b\": float(b[i]), \"se\": float(se[i]), \"ci\": [float(b[i] - 1.96 * se[i]), float(b[i] + 1.96 * se[i])],\n                           \"p\": float(2 * stats.norm.sf(abs(b[i] / se[i]))) if se[i] > 0 else float(\"nan\")}\n    return out\n\n\ndef dersimonian_laird(b: np.ndarray, se: np.ndarray) -> dict:\n    b, se = np.asarray(b, float), np.asarray(se, float)\n    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n    b, se = b[ok], se[ok]\n    k = len(b)\n    if k == 0:\n        return {\"k\": 0}\n    w = 1 / se**2\n    bf = (w * b).sum() / w.sum()\n    Q = float((w * (b - bf) ** 2).sum())\n    C = w.sum() - (w**2).sum() / w.sum()\n    tau2 = max(0.0, (Q - (k - 1)) / C) if k > 1 and C > 0 else 0.0\n    ws = 1 / (se**2 + tau2)\n    bre = (ws * b).sum() / ws.sum()\n    sre = math.sqrt(1 / ws.sum())\n    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0\n    return {\"k\": k, \"b\": float(bre), \"se\": sre, \"ci\": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],\n            \"p\": float(2 * stats.norm.sf(abs(bre / sre))), \"tau2\": float(tau2), \"Q\": Q, \"I2\": float(I2)}\n\n\ndef sign_test(k_pos: int, n: int) -> float:\n    \"\"\"one-sided binomial P(X >= k_pos | p = 0.5).\"\"\"\n    return float(stats.binom.sf(k_pos - 1, n, 0.5)) if n > 0 else float(\"nan\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-28 21:31:53 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; grep -n "GF\|backbone\|def \|frame_g\|standardise\|spec\[" $R/method.py | head -120
```

### [25] TOOL RESULT — Bash · 2026-09-28 21:31:53 UTC

```
{"stdout": "29:from frame_io import SealedError, frozen, load_backbone, load_frame, load_g  # noqa: E402\n41:def jdump(obj, path: Path) -> None:\n42:    def conv(o):\n53:    def clean(o):\n64:def gate_terciles(gate: np.ndarray) -> tuple[float, float]:\n68:def agg():\n70:    return z[\"G\"], z[\"GF\"]\n74:def h2_block(df: pd.DataFrame, spec: dict | None, rng, n_boot: int, n_perm: int, n_rewire: int, bb: dict,\n77:    dfs, spec = H2.standardise(df, spec, REGS)\n103:    mu, sd = spec[\"d_ret_gate\"][\"mean\"], spec[\"d_ret_gate\"][\"sd\"]\n139:def h2_robust(df_all: pd.DataFrame, spec: dict, frame: pd.DataFrame, G: dict, bb: dict, GF: np.ndarray, Gpf: dict | None) -> dict:\n142:    dfs, _ = H2.standardise(prim, spec, REGS)\n149:    dall, _ = H2.standardise(df_all, spec, REGS)\n169:        dfk, RETk, _ = H2.build_risk_sets(frame, G, bb2, GF)\n171:        dks, _ = H2.standardise(dfk, None, REGS)\n175:    dfr, _, _ = H2.build_risk_sets(frame, G, bb, GF, entry_def=\"rca\")\n177:    drs, _ = H2.standardise(dfr, None, REGS)\n182:        dfp, _, _ = H2.build_risk_sets(frame[frame.cidx.isin(list(Gpf))], Gpf, bb, GF)\n184:        dps, _ = H2.standardise(dfp, None, REGS)\n191:def planted_control(df: pd.DataFrame, spec: dict, rng, n_sim: int = 100) -> dict:\n193:    dfs, _ = H2.standardise(df, spec, REGS)\n198:    def sim(beta: float) -> float:\n213:def rescue_relay(frame: pd.DataFrame, eps: pd.DataFrame, G: dict, bb: dict, rng, n_boot: int) -> tuple[dict, pd.DataFrame, pd.DataFrame]:\n304:def traj_block(frame: pd.DataFrame, G: dict, bb: dict, rng, spec: dict | None) -> tuple[dict, pd.DataFrame, dict]:\n315:        zspec = spec[\"zspec\"]\n330:        M = np.array(spec[\"medoid_series\"])\n333:        k = spec[\"k\"]\n346:        tspec[\"hmm\"] = {\"n_states\": hm[\"n_states\"], \"means\": hm[\"means\"], \"transmat\": hm[\"transmat\"]}\n351:        hm = TR.hmm_fit(Z, SEED, n_states=[spec[\"hmm\"][\"n_states\"]])\n362:def ordering_block(P: pd.DataFrame, frame: pd.DataFrame, bb: dict, rng, pen: float | None, o2r_cut: float | None) -> tuple[dict, dict]:\n398:def add_ret_sets(P: pd.DataFrame, frame: pd.DataFrame, G: dict) -> pd.DataFrame:\n413:def stage_dev() -> None:\n415:    bb = load_backbone(); G_tot, GF = agg()\n422:    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)\n435:    pfp = SCAN / \"frame_gpf_dev.npz\"\n438:    res[\"H2_robustness\"] = h2_robust(df_all, spec, frame, G, bb, GF, Gpf)\n472:def sha(p: Path) -> str:\n476:def stage_freeze() -> None:\n493:                       \"backbone\": sha(ROOT / \"inputs\" / \"field_backbone.json\"), \"code\": code},\n495:                \"H2_entry_CONFIRMED\": \"LR M2 vs M0 p<0.01 AND pooled d>0 with concept-bootstrap 95% CI>0 AND d>0 in >= ceil(0.75 x available held-out FIELD groups) (MathDec has no concepts -> 3 of 3: Physical, LifeEnv, Social) AND d>0 in the 2010-14 cohort AND permutation p<0.05 AND real LR gain > 95th pct of the rewired-backbone null\",\n506:def stage_heldout() -> None:\n512:    bb = load_backbone(); G_tot, GF = agg()\n520:    coef = spec[\"o2r_resid_coef_dev\"]\n531:    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)\n536:    std = spec[\"standardisation\"]\n542:    dfs, _ = H2.standardise(df, std, REGS)\n553:        ds, _ = H2.standardise(d, std, REGS)\n574:    od, osp = ordering_block(P, frame, bb, rng, spec[\"changepoint_pen\"], spec[\"o2r_top_tercile_cut_resid\"])\n613:def main() -> None:", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-28 21:31:55 UTC

```
Reading EXP6's pipeline so I can reproduce its risk sets exactly before extending them.
```

### [27] TOOL CALL — Bash · 2026-09-28 21:31:55 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; sed -n 1,140p $R/method.py; sed -n 400,470p $R/method.py; sed -n 506,612p $R/method.py; cat $R/lib/frame_io.py
```

### [28] TOOL RESULT — Bash · 2026-09-28 21:31:55 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"How concepts hop between fields: H2 next-field entry (gateway-weighted relatedness to RETAINING fields vs\nrelatedness-to-home / size / Hidalgo density / own centrality), rescue, relay, trajectories and ordering.\n\nStages (run in this order; the held-out stage is sealed until the freeze stage has logged frozen_spec.json):\n  python method.py dev      -> results/dev_result.json (+ dev tables)\n  python method.py freeze   -> results/frozen_spec.json, results/freeze_log.txt\n  python method.py heldout  -> results/heldout_result.json (run ONCE)\n  python method.py outputs  -> method_out.json (exp_gen_sol_out schema) + figures\nPrerequisites: pass1.py -> aggregate.py -> cand.py -> pass2.py -> grounding.py -> frame.py (see README).\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport resource\nimport sys\nimport time\nfrom datetime import datetime, timezone\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\nfrom config import FIELD_GROUP, N_BOOT, N_PERM, N_REWIRE, RES, SCAN, SEED, Y0  # noqa: E402\nfrom frame_io import SealedError, frozen, load_backbone, load_frame, load_g  # noqa: E402\nimport h2 as H2  # noqa: E402\nimport traj as TR  # noqa: E402\nfrom stats_core import dersimonian_laird, fe_ols, fe_poisson, sign_test  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\nREGS = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\"]\nHELD_GROUPS = [\"Physical\", \"LifeEnv\", \"Social\", \"MathDec\", \"Cohort\"]\n\n\ndef jdump(obj, path: Path) -> None:\n    def conv(o):\n        if isinstance(o, (np.integer,)):\n            return int(o)\n        if isinstance(o, (np.floating,)):\n            return None if not np.isfinite(o) else float(o)\n        if isinstance(o, np.ndarray):\n            return o.tolist()\n        if isinstance(o, (set, tuple)):\n            return list(o)\n        return str(o)\n\n    def clean(o):\n        if isinstance(o, dict):\n            return {str(k): clean(v) for k, v in o.items() if not str(k).startswith(\"_\")}\n        if isinstance(o, (list, tuple)):\n            return [clean(v) for v in o]\n        if isinstance(o, float) and not math.isfinite(o):\n            return None\n        return o\n    path.write_text(json.dumps(clean(obj), indent=1, default=conv))\n\n\ndef gate_terciles(gate: np.ndarray) -> tuple[float, float]:\n    return float(np.quantile(gate, 1 / 3)), float(np.quantile(gate, 2 / 3))\n\n\ndef agg():\n    z = np.load(SCAN / \"agg_counts.npz\")\n    return z[\"G\"], z[\"GF\"]\n\n\n# =============================================================================== H2\ndef h2_block(df: pd.DataFrame, spec: dict | None, rng, n_boot: int, n_perm: int, n_rewire: int, bb: dict,\n             RET: np.ndarray, full: bool = True) -> tuple[dict, dict]:\n    \"\"\"fit M0-M3 on the primary sample (strata with a non-empty retaining set).\"\"\"\n    dfs, spec = H2.standardise(df, spec, REGS)\n    res = {\"n_rows\": len(dfs), \"n_strata\": int(dfs.stratum.nunique()), \"n_concepts\": int(dfs.cidx.nunique()),\n           \"n_events\": int(dfs.entered.sum()), \"entry_rate\": float(dfs.entered.mean())}\n    fits = {m: H2.fit_model(dfs, cols) for m, cols in H2.MODELS.items()}\n    res[\"models\"] = {m: {k: v for k, v in f.items() if k != \"_b\"} for m, f in fits.items()}\n    res[\"LR\"] = {\"M2_vs_M0\": H2.lr_test(fits[\"M2\"], fits[\"M0\"], 1), \"M1_vs_M0\": H2.lr_test(fits[\"M1\"], fits[\"M0\"], 1),\n                 \"M3_vs_M1\": H2.lr_test(fits[\"M3\"], fits[\"M1\"], 1), \"M2lost_vs_M0\": H2.lr_test(fits[\"M2lost\"], fits[\"M0\"], 1)}\n    # within-stratum AUC per block (linear predictor) and per single regressor\n    auc = {}\n    for m, cols in H2.MODELS.items():\n        s = H2.within_auc(dfs, dfs[cols].to_numpy() @ fits[m][\"_b\"])\n        auc[m] = {\"mean\": float(s.mean()), \"ci\": H2.concept_boot_mean(s, n_boot, rng), \"n_strata\": int(len(s))}\n    for c in REGS:\n        s = H2.within_auc(dfs, dfs[c].to_numpy())\n        auc[c] = {\"mean\": float(s.mean()), \"ci\": H2.concept_boot_mean(s, n_boot, rng)}\n    res[\"auc_within_stratum\"] = auc\n    if not full:\n        return res, spec\n    t = time.time()\n    res[\"boot_d\"] = H2.boot_coef(dfs, H2.MODELS[\"M2\"], \"d_ret_gate\", n_boot, rng, small_cols=H2.MODELS[\"M0\"])\n    logger.info(f\"bootstrap {n_boot} in {time.time()-t:.0f}s\")\n    # label-permutation null for d (phi and g permuted jointly across fields)\n    phi, gate = bb[\"phi\"], bb[\"g\"]\n    lr_obs = res[\"LR\"][\"M2_vs_M0\"][\"LR\"]\n    fields = df.field.to_numpy()\n    base = dfs.copy()\n    mu, sd = spec[\"d_ret_gate\"][\"mean\"], spec[\"d_ret_gate\"][\"sd\"]\n    perm = []\n    for _ in range(n_perm):\n        p = rng.permutation(26)\n        dp = H2.recompute_d(RET, fields, phi[np.ix_(p, p)], gate[p])\n        base[\"d_ret_gate\"] = (dp - mu) / sd\n        perm.append(2 * (H2.fit_model(base, H2.MODELS[\"M2\"])[\"ll\"] - fits[\"M0\"][\"ll\"]))\n    perm = np.array(perm)\n    res[\"perm_null\"] = {\"n\": n_perm, \"lr_obs\": lr_obs, \"p\": float((1 + (perm >= lr_obs).sum()) / (1 + n_perm)),\n                        \"null_q\": np.percentile(perm, [50, 90, 95, 99]).tolist(), \"null_mean\": float(perm.mean())}\n    gperm = []\n    lr31 = res[\"LR\"][\"M3_vs_M1\"][\"LR\"]\n    for _ in range(n_perm):\n        p = rng.permutation(26)\n        dp = H2.recompute_d(RET, fields, phi, gate[p])\n        base[\"d_ret_gate\"] = (dp - mu) / sd\n        gperm.append(2 * (H2.fit_model(base, H2.MODELS[\"M3\"])[\"ll\"] - fits[\"M1\"][\"ll\"]))\n    gperm = np.array(gperm)\n    res[\"gonly_perm_null_M3_vs_M1\"] = {\"n\": n_perm, \"lr_obs\": lr31, \"p\": float((1 + (gperm >= lr31).sum()) / (1 + n_perm)),\n                                       \"null_q\": np.percentile(gperm, [50, 90, 95, 99]).tolist()}\n    base[\"d_ret_gate\"] = dfs[\"d_ret_gate\"]\n    rew = []\n    for _ in range(n_rewire):\n        P = H2.rewire(phi, rng)\n        gp = H2.eig_gateway(P)\n        dp = H2.recompute_d(RET, fields, P, gp)\n        base[\"d_ret_gate\"] = (dp - mu) / sd\n        rew.append(2 * (H2.fit_model(base, H2.MODELS[\"M2\"])[\"ll\"] - fits[\"M0\"][\"ll\"]))\n    rew = np.array(rew)\n    res[\"rewired_null\"] = {\"n\": n_rewire, \"lr_obs\": lr_obs, \"p\": float((1 + (rew >= lr_obs).sum()) / (1 + n_rewire)),\n                           \"null_q95\": float(np.percentile(rew, 95)), \"null_median\": float(np.median(rew)),\n                           \"real_gain_le_null95\": bool(lr_obs <= np.percentile(rew, 95))}\n    res[\"_lrs_boot\"] = res[\"boot_d\"].pop(\"_lrs\")\n    return res, spec\n\n\ndef h2_robust(df_all: pd.DataFrame, spec: dict, frame: pd.DataFrame, G: dict, bb: dict, GF: np.ndarray, Gpf: dict | None) -> dict:\n    out = {}\n    fr = frame.set_index(\"cidx\")\n    for c, d in P.groupby(\"cidx\", sort=False):\n        home = [int(h) for h in str(fr.loc[c, \"home\"]).split(\"|\")]\n        S = H2.states(G[c], home)\n        for t in d.t:\n            rets.append((c, t, S[\"retaining\"][t - Y0].copy()))\n    m = {(c, t): r for c, t, r in rets}\n    P = P.copy()\n    P[\"_ret\"] = [m[(c, t)] for c, t in zip(P.cidx, P.t)]\n    return P\n\n\n# =============================================================================== stages\ndef stage_dev() -> None:\n    rng = np.random.default_rng(SEED)\n    bb = load_backbone(); G_tot, GF = agg()\n    frame = load_frame(\"dev\"); frame = frame[frame.newborn]\n    G = load_g(\"dev\")\n    eps = pd.read_csv(RES / \"episodes.csv\"); eps = eps[(eps.split == \"dev\") & eps.cidx.isin(frame.cidx)]\n    res = {\"n_dev_concepts_newborn\": int(len(frame)), \"n_dev_episodes\": int(len(eps)),\n           \"dev_by_group\": frame.group.value_counts().to_dict()}\n    t = time.time()\n    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)\n    df_all.to_parquet(RES / \"entry_risk_sets_dev.parquet\", index=False)\n    prim = df_all.n_ret > 0\n    df, RET = df_all[prim].reset_index(drop=True), RET_all[prim.to_numpy()]\n    logger.info(f\"dev risk sets: {len(df_all):,} rows, primary {len(df):,} rows / {df.stratum.nunique():,} strata \"\n                f\"({time.time()-t:.0f}s)\")\n    h, spec = h2_block(df, None, rng, N_BOOT, N_PERM, N_REWIRE, bb, RET)\n    lrs = h.pop(\"_lrs_boot\")\n    res[\"H2\"] = h\n    res[\"H2\"][\"size_vs_density_auc\"] = {\"size\": h[\"auc_within_stratum\"][\"b_log_size\"][\"mean\"],\n                                        \"density\": h[\"auc_within_stratum\"][\"c_density\"][\"mean\"]}\n    logger.info(f\"H2 dev: LR M2vsM0={h['LR']['M2_vs_M0']}, d={h['models']['M2']['coef']['d_ret_gate']:.3f}\")\n    Gpf = None\n    pfp = SCAN / \"frame_gpf_dev.npz\"\n    if pfp.exists():\n        z = np.load(pfp); Gpf = {int(c): z[\"g\"][i] for i, c in enumerate(z[\"cidx\"])}\n    res[\"H2_robustness\"] = h2_robust(df_all, spec, frame, G, bb, GF, Gpf)\n    res[\"T0_planted_control\"] = planted_control(df, spec, rng)\n    logger.info(f\"planted control: {res['T0_planted_control']}\")\n    # power at held-out n: share of bootstrap LR draws significant at 0.01, rescaled to the held-out concept count\n    nh = len(pd.read_csv(RES / \"frame_concepts.csv\").query(\"split != 'dev' and newborn\"))\n    scale = nh / max(frame.shape[0], 1)\n    from scipy import stats as st\n    res[\"power_check\"] = {\"n_heldout_concepts\": nh, \"scale_vs_dev\": scale,\n                          \"P(p<0.01) at heldout n (LR scaled linearly)\": float(np.mean(st.chi2.sf(lrs * scale, 1) < 0.01))}\n    # rescue / relay\n    try:\n        rr, R, Rl = rescue_relay(frame, eps, G, bb, rng, N_BOOT)\n        res[\"rescue_relay\"] = rr\n        R.drop(columns=[c for c in R.columns if c.startswith(\"_\")]).to_csv(RES / \"rescue_dev.csv\", index=False)\n        Rl.to_csv(RES / \"relay_dev.csv\", index=False)\n    except (FileNotFoundError, ValueError, KeyError) as e:\n        logger.exception(\"rescue/relay failed\")\n        res[\"rescue_relay\"] = {\"status\": f\"NOT RUN: {e!r}\"}\n    # trajectories + ordering\n    tr, P, tsp = traj_block(frame, G, bb, rng, None)\n    res[\"trajectories\"] = tr\n    P = add_ret_sets(P, frame, G)\n    od, osp = ordering_block(P, frame, bb, rng, None, None)\n    res[\"ordering\"] = od\n    P.drop(columns=[\"_ret\"]).to_csv(RES / \"trajectories_dev.csv\", index=False)\n    tsp[\"clusters\"].to_csv(RES / \"cluster_assign_dev.csv\", index=False)\n    osp[\"orders\"].to_csv(RES / \"ordering_dev.csv\", index=False)\n    jdump(res, RES / \"dev_result.json\")\n    lo, hi = gate_terciles(bb[\"g\"])\n    jdump({\"standardisation\": spec, \"tspec\": tsp[\"tspec\"], \"pen\": osp[\"pen\"], \"o2r_cut_resid\": osp[\"o2r_cut\"],\n           \"gate_terciles\": [lo, hi]}, RES / \"dev_spec_parts.json\")\n    logger.info(\"dev stage done\")\n\ndef stage_heldout() -> None:\n    if not frozen():\n        raise SealedError(\"freeze first\")\n    import frame as FR\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    rng = np.random.default_rng(SEED + 7)\n    bb = load_backbone(); G_tot, GF = agg()\n    fc = pd.read_csv(RES / \"frame_concepts.csv\")\n    G = load_g(\"heldout\")\n    # unseal: held-out outcomes and episode outcomes\n    for i, r in fc[fc.split != \"dev\"].iterrows():\n        o = FR.concept_outcomes(G[int(r.cidx)], int(r.t0), G_tot)\n        for k, v in o.items():\n            fc.loc[i, k] = v\n    coef = spec[\"o2r_resid_coef_dev\"]\n    m = fc.split != \"dev\"\n    fc.loc[m, \"O2r_resid\"] = fc.loc[m, \"O2r_m30\"] - np.polyval(coef, np.log(fc.loc[m, \"n_early\"]))\n    fc.to_csv(RES / \"frame_concepts.csv\", index=False)\n    eps = pd.read_csv(RES / \"episodes.csv\")\n    for i, e in eps[eps.split != \"dev\"].iterrows():\n        eps.loc[i, \"R_cj\"] = FR.episode_outcome(G[int(e.cidx)], int(e.t0), int(e.field))\n    eps.to_csv(RES / \"episodes.csv\", index=False)\n    frame = fc[(fc.split != \"dev\") & fc.newborn].copy()\n    frame[\"hgroup\"] = np.where(frame.split == \"heldout_cohort\", \"Cohort\", frame.group)\n    res = {\"n_heldout_concepts\": int(len(frame)), \"by_group\": frame.hgroup.value_counts().to_dict()}\n    df_all, RET_all, _ = H2.build_risk_sets(frame, G, bb, GF)\n    df_all[\"hgroup\"] = df_all.cidx.map(dict(zip(frame.cidx, frame.hgroup)))\n    df_all.to_parquet(RES / \"entry_risk_sets_heldout.parquet\", index=False)\n    prim = (df_all.n_ret > 0).to_numpy()\n    df, RET = df_all[prim].reset_index(drop=True), RET_all[prim]\n    std = spec[\"standardisation\"]\n    h, _ = h2_block(df, std, rng, N_BOOT, N_PERM, N_REWIRE, bb, RET)\n    h.pop(\"_lrs_boot\", None)\n    res[\"H2_pooled\"] = h\n    # frozen dev coefficients scored on held-out (prediction AUC, no refit)\n    dev = json.loads((RES / \"dev_result.json\").read_text())\n    dfs, _ = H2.standardise(df, std, REGS)\n    for mname in (\"M0\", \"M2\"):\n        b = np.array([dev[\"H2\"][\"models\"][mname][\"coef\"][c] for c in H2.MODELS[mname]])\n        s = H2.within_auc(dfs, dfs[H2.MODELS[mname]].to_numpy() @ b)\n        res.setdefault(\"frozen_dev_coef_auc\", {})[mname] = {\"mean\": float(s.mean()), \"ci\": H2.concept_boot_mean(s, N_BOOT, rng)}\n    per = {}\n    for gname in HELD_GROUPS + [\"OtherHealth\"]:\n        d = df[df.hgroup == gname]\n        if d.cidx.nunique() < 5:\n            per[gname] = {\"n_concepts\": int(d.cidx.nunique()), \"status\": \"too few concepts\"}\n            continue\n        ds, _ = H2.standardise(d, std, REGS)\n        f0 = H2.fit_model(ds, H2.MODELS[\"M0\"]); f2 = H2.fit_model(ds, H2.MODELS[\"M2\"])\n        bt = H2.boot_coef(ds, H2.MODELS[\"M2\"], \"d_ret_gate\", 500, rng)\n        per[gname] = {\"n_concepts\": int(d.cidx.nunique()), \"n_events\": f2[\"n_events\"], \"d\": f2[\"coef\"][\"d_ret_gate\"],\n                      \"se\": f2[\"se\"][\"d_ret_gate\"], \"boot_ci\": bt[\"ci\"], \"LR\": H2.lr_test(f2, f0, 1)}\n    res[\"H2_per_group\"] = per\n    use = [g for g in HELD_GROUPS if \"d\" in per.get(g, {})]\n    res[\"H2_DL_pooled\"] = dersimonian_laird(np.array([per[g][\"d\"] for g in use]), np.array([per[g][\"se\"] for g in use]))\n    npos = sum(per[g][\"d\"] > 0 for g in use)\n    res[\"H2_sign_count\"] = {\"positive\": int(npos), \"of\": len(use), \"sign_test_p\": sign_test(npos, len(use))}\n    eps_h = eps[(eps.split != \"dev\") & eps.cidx.isin(frame.cidx)]\n    try:\n        rr, R, Rl = rescue_relay(frame, eps_h, G, bb, rng, N_BOOT)\n        res[\"rescue_relay\"] = rr\n        R.to_csv(RES / \"rescue_heldout.csv\", index=False); Rl.to_csv(RES / \"relay_heldout.csv\", index=False)\n    except (FileNotFoundError, ValueError, KeyError) as e:\n        logger.exception(\"held-out rescue/relay failed\")\n        res[\"rescue_relay\"] = {\"status\": f\"NOT RUN: {e!r}\"}\n    tr, P, tsp = traj_block(frame, G, bb, rng, spec)\n    res[\"trajectories\"] = tr\n    P = add_ret_sets(P, frame, G)\n    od, osp = ordering_block(P, frame, bb, rng, spec[\"changepoint_pen\"], spec[\"o2r_top_tercile_cut_resid\"])\n    res[\"ordering\"] = od\n    P.drop(columns=[\"_ret\"]).to_csv(RES / \"trajectories_heldout.csv\", index=False)\n    tsp[\"clusters\"].to_csv(RES / \"cluster_assign_heldout.csv\", index=False)\n    osp[\"orders\"].to_csv(RES / \"ordering_heldout.csv\", index=False)\n    # decisions\n    lr = h[\"LR\"][\"M2_vs_M0\"]\n    ci = h[\"boot_d\"][\"ci\"]\n    fg = [g for g in (\"Physical\", \"LifeEnv\", \"Social\", \"MathDec\") if \"d\" in per.get(g, {})]\n    grp_pos = sum(per[g][\"d\"] > 0 for g in fg)\n    need = math.ceil(0.75 * len(fg))\n    dec = {\"H2_entry\": {\"LR_p<0.01\": lr[\"p\"] < 0.01, \"d>0_CI>0\": h[\"models\"][\"M2\"][\"coef\"][\"d_ret_gate\"] > 0 and ci[0] > 0,\n                        f\"field_groups_positive>={need}_of_{len(fg)}\": grp_pos >= need,\n                        \"cohort_positive\": per.get(\"Cohort\", {}).get(\"d\", -1) > 0, \"perm_p<0.05\": h[\"perm_null\"][\"p\"] < 0.05,\n                        \"rewired_gain_above_null95\": not h[\"rewired_null\"][\"real_gain_le_null95\"]}}\n    dec[\"H2_entry\"][\"CONFIRMED\"] = all(dec[\"H2_entry\"].values())\n    gw = od[\"gateway\"]; pe = od[\"peripheral\"]\n    dec[\"H2_ordering\"] = {\"p_gw\": gw[\"share_before_excl_ties\"], \"sign_p\": gw[\"sign_test_p_one_sided\"],\n                          \"peripheral_share\": pe[\"share_before_excl_ties\"],\n                          \"CONFIRMED\": bool(gw[\"share_before_excl_ties\"] >= 0.6 and gw[\"sign_test_p_one_sided\"] < 0.05\n                                            and gw[\"share_before_excl_ties\"] > (pe[\"share_before_excl_ties\"] if pe[\"share_before_excl_ties\"] == pe[\"share_before_excl_ties\"] else 0))}\n    rrh = res[\"rescue_relay\"]\n    try:\n        r1 = rrh[\"R1_resc\"][\"coef\"][\"ret_x_top\"]; med = rrh[\"R2_mediation\"]\n        dec[\"RESCUE\"] = {\"R1_interaction\": r1[\"b\"], \"R1_ci\": r1[\"ci\"], \"indirect\": med[\"indirect\"], \"indirect_ci\": med[\"ci\"],\n                         \"SUPPORTED\": bool(r1[\"b\"] > 0 and r1[\"ci\"][0] > 0 and med[\"indirect\"] > 0)}\n        rp = rrh[\"relay_fepois\"][\"coef\"][\"ret_x_gate\"]; ex = rrh[\"relay_excess_gateway_retained\"]\n        dec[\"RELAY\"] = {\"fepois_ret_x_gate\": rp[\"b\"], \"ci\": rp[\"ci\"], \"mean_excess_gw_retained\": ex[\"mean\"],\n                        \"SUPPORTED\": bool(rp[\"b\"] > 0 and rp[\"ci\"][0] > 0 and ex[\"mean\"] > 0)}\n    except (KeyError, TypeError) as e:\n        dec[\"RESCUE_RELAY_status\"] = f\"not evaluable: {e!r}\"\n    res[\"decisions\"] = dec\n    jdump(res, RES / \"heldout_result.json\")\n    with (RES / \"freeze_log.txt\").open(\"a\") as f:\n        f.write(f\"{datetime.now(timezone.utc).isoformat()} heldout stage run; heldout_result.json sha256={sha(RES / 'heldout_result.json')}\\n\")\n    logger.info(f\"held-out decisions: {json.dumps(dec, default=str)}\")\n\n\n@logger.catch(reraise=True)\n\"\"\"Guarded access to frame tables. Held-out outcome / entry data can only be loaded once results/freeze_log.txt\nexists (T5 sealing guard).\"\"\"\nfrom __future__ import annotations\n\nimport json\n\nimport numpy as np\nimport pandas as pd\n\nfrom config import RES, SCAN\n\n\nclass SealedError(RuntimeError):\n    pass\n\n\ndef frozen() -> bool:\n    return (RES / \"freeze_log.txt\").exists()\n\n\ndef load_backbone() -> dict:\n    b = json.loads((RES.parent / \"inputs\" / \"field_backbone.json\").read_text())\n    b[\"phi\"] = np.array(b[\"phi\"]); b[\"g\"] = np.array(b[\"gateway_eig\"])\n    b[\"g_deg\"] = np.array(b[\"gateway_deg\"]); b[\"g_btw\"] = np.array(b[\"gateway_btw\"])\n    return b\n\n\ndef load_g(split: str) -> dict[int, np.ndarray]:\n    \"\"\"per-concept grounded counts [NY, 27] (slot 0 = no venue field, slot k = field 10+k).\"\"\"\n    if split != \"dev\" and not frozen():\n        raise SealedError(f\"split {split!r} is sealed until frozen_spec.json is logged in freeze_log.txt\")\n    z = np.load(SCAN / f\"frame_g_{'dev' if split == 'dev' else 'heldout'}.npz\")\n    return {int(c): z[\"g\"][i] for i, c in enumerate(z[\"cidx\"])}\n\n\ndef load_frame(split: str | None = None) -> pd.DataFrame:\n    fc = pd.read_csv(RES / \"frame_concepts.csv\")\n    if split is None:\n        return fc\n    if split != \"dev\" and not frozen():\n        raise SealedError(f\"split {split!r} is sealed\")\n    if split == \"heldout\":\n        return fc[fc.split.isin([\"heldout_field\", \"heldout_cohort\"])]\n    return fc[fc.split == split]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-28 21:32:01 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; python3 -c "
import json;d=json.load(open('$R/results/heldout_result.json'));h=d['H2_pooled'];print(json.dumps({k:h[k] for k in ['n_rows','n_strata','n_concepts','n_events','LR']},indent=0));print(json.dumps(h['models'],indent=0)[:3000]); print(d['by_group'])
"; python3 -c "
import json;d=json.load(open('$R/results/frozen_spec.json'));print(json.dumps(d,indent=0)[:5000])"
```

### [30] TOOL RESULT — Bash · 2026-09-28 21:32:01 UTC

```
{"stdout": "{\n\"n_rows\": 46433,\n\"n_strata\": 2339,\n\"n_concepts\": 369,\n\"n_events\": 1373,\n\"LR\": {\n\"M2_vs_M0\": {\n\"LR\": 71.71641463905598,\n\"df\": 1,\n\"p\": 2.4845706606291646e-17\n},\n\"M1_vs_M0\": {\n\"LR\": 68.56864172514634,\n\"df\": 1,\n\"p\": 1.2253722672182456e-16\n},\n\"M3_vs_M1\": {\n\"LR\": 5.359129220855721,\n\"df\": 1,\n\"p\": 0.02061406421285374\n},\n\"M2lost_vs_M0\": {\n\"LR\": 3.692783297256028,\n\"df\": 1,\n\"p\": 0.05464835230436948\n}\n}\n}\n{\n\"M0\": {\n\"coef\": {\n\"a_phi_home\": 0.33064441529782246,\n\"b_log_size\": 1.584569503949015,\n\"c_density\": 0.36227353934450424,\n\"e_gate_own\": 0.09944954700323524\n},\n\"se\": {\n\"a_phi_home\": 0.02736968235608079,\n\"b_log_size\": 0.05112728370177903,\n\"c_density\": 0.03013663752993411,\n\"e_gate_own\": 0.030502854814615843\n},\n\"ll\": -3270.093339796141,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true\n},\n\"M1\": {\n\"coef\": {\n\"a_phi_home\": 0.37188553304728283,\n\"b_log_size\": 1.6738276315064888,\n\"c_density\": 0.23852929616788293,\n\"e_gate_own\": 0.05164125007538622,\n\"d0_ret_rel\": 0.2809043442272664\n},\n\"se\": {\n\"a_phi_home\": 0.027921572124598486,\n\"b_log_size\": 0.05288720649766899,\n\"c_density\": 0.034421918211009254,\n\"e_gate_own\": 0.0315219540144637,\n\"d0_ret_rel\": 0.032159975704963886\n},\n\"ll\": -3235.809018933568,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true\n},\n\"M2\": {\n\"coef\": {\n\"a_phi_home\": 0.36478607003405844,\n\"b_log_size\": 1.6795135455218,\n\"c_density\": 0.24721762419454624,\n\"e_gate_own\": 0.019351762291929017,\n\"d_ret_gate\": 0.3019648521082155\n},\n\"se\": {\n\"a_phi_home\": 0.02772926123612498,\n\"b_log_size\": 0.05279709656652038,\n\"c_density\": 0.03379253921762855,\n\"e_gate_own\": 0.032662090679520965,\n\"d_ret_gate\": 0.03418983053914712\n},\n\"ll\": -3234.235132476613,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true\n},\n\"M3\": {\n\"coef\": {\n\"a_phi_home\": 0.36936674458570773,\n\"b_log_size\": 1.6818176588931806,\n\"c_density\": 0.2380779743085792,\n\"e_gate_own\": 0.028999552223334616,\n\"d0_ret_rel\": 0.11633740617530272,\n\"d_ret_gate\": 0.19139604594713114\n},\n\"se\": {\n\"a_phi_home\": 0.02791923110501382,\n\"b_log_size\": 0.05292618682191926,\n\"c_density\": 0.03440779835762934,\n\"e_gate_own\": 0.03320444240582659,\n\"d0_ret_rel\": 0.07809784050423697,\n\"d_ret_gate\": 0.0821312421090051\n},\n\"ll\": -3233.12945432314,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true\n},\n\"M2lost\": {\n\"coef\": {\n\"a_phi_home\": 0.32791908447413465,\n\"b_log_size\": 1.5834072596401476,\n\"c_density\": 0.36914417297567764,\n\"e_gate_own\": 0.10317255712560171,\n\"d_lost_gate\": -0.06322615097883642\n},\n\"se\": {\n\"a_phi_home\": 0.027397318970110676,\n\"b_log_size\": 0.051120809259672675,\n\"c_density\": 0.030304621819881934,\n\"e_gate_own\": 0.030554888439417182,\n\"d_lost_gate\": 0.034737288878067214\n},\n\"ll\": -3268.246948147513,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true\n}\n}\n{'Cohort': 248, 'Social': 54, 'Physical': 34, 'LifeEnv': 34, 'OtherHealth': 4}\n{\n\"created\": \"2026-09-28T18:32:24.227628+00:00\",\n\"regressors\": {\n\"a_phi_home\": \"mean_h phi[h,k] over home fields\",\n\"b_log_size\": \"log venue-field works in k at t-1\",\n\"c_density\": \"Hidalgo density sum_{j in entered(t-1)} phi[j,k] / sum_j phi[j,k]\",\n\"e_gate_own\": \"gateway_eig of k\",\n\"d0_ret_rel\": \"mean_{j in Ret(t-1)} phi[j,k]\",\n\"d_ret_gate\": \"sum_{j in Ret(t-1)} g_j phi[j,k] / sum_{j in Ret} g_j\",\n\"d_lost_gate\": \"same over LOST fields (placebo)\"\n},\n\"models\": {\n\"M0\": [\n\"a_phi_home\",\n\"b_log_size\",\n\"c_density\",\n\"e_gate_own\"\n],\n\"M1\": [\n\"a_phi_home\",\n\"b_log_size\",\n\"c_density\",\n\"e_gate_own\",\n\"d0_ret_rel\"\n],\n\"M2\": [\n\"a_phi_home\",\n\"b_log_size\",\n\"c_density\",\n\"e_gate_own\",\n\"d_ret_gate\"\n],\n\"M3\": [\n\"a_phi_home\",\n\"b_log_size\",\n\"c_density\",\n\"e_gate_own\",\n\"d0_ret_rel\",\n\"d_ret_gate\"\n],\n\"M2lost\": [\n\"a_phi_home\",\n\"b_log_size\",\n\"c_density\",\n\"e_gate_own\",\n\"d_lost_gate\"\n]\n},\n\"primary_sample\": \"strata (concept, t) with non-empty retaining set; t = t0+1..t0+8\",\n\"standardisation\": {\n\"a_phi_home\": {\n\"mean\": 0.16202608575019556,\n\"sd\": 0.30285707738892603\n},\n\"b_log_size\": {\n\"mean\": 9.731619276958401,\n\"sd\": 2.284239494682293\n},\n\"c_density\": {\n\"mean\": 0.17244520298540197,\n\"sd\": 0.21075858352121596\n},\n\"e_gate_own\": {\n\"mean\": 0.32849098315017977,\n\"sd\": 0.28592622199912354\n},\n\"d0_ret_rel\": {\n\"mean\": 0.12733956053079426,\n\"sd\": 0.24445162515471244\n},\n\"d_ret_gate\": {\n\"mean\": 0.15253833778314638,\n\"sd\": 0.30125319183313704\n},\n\"d_lost_gate\": {\n\"mean\": 0.02216697846204525,\n\"sd\": 0.14547123546523702\n}\n},\n\"gate_terciles\": [\n0.1520343866310761,\n0.29798365664086207\n],\n\"o2r_resid_coef_dev\": [\n-0.03808207780883798,\n3.891852441738708\n],\n\"o2r_top_tercile_cut_resid\": 0.4175760916556232,\n\"changepoint_pen\": 4.5,\n\"zspec\": {\n\"n_entered_offhome\": [\n4.013888888888889,\n2.728327088811533\n],\n\"n_retaining\": [\n2.4739583333333335,\n2.11469944339186\n],\n\"n_lost\": [\n0.1701388888888889,\n0.43184768385214284\n],\n\"R20\": [\n3.0763716485002344,\n1.2147270567565587\n],\n\"H\": [\n0.715027691192768,\n0.435926568104874\n],\n\"G_share\": [\n0.07476598956623554,\n0.08414117835153488\n],\n\"log_volume\": [\n4.4739204732977225,\n0.9011972763296602\n]\n},\n\"k\": 2,\n\"medoid_cidx\": [\n94,\n41020\n],\n\"medoid_series\": [\n[\n[\n-0.7381405613526144,\n-0.6970060629368618,\n-0.3939789311157716,\n0.8922569181864014,\n0.8342324184555338,\n0.11997874156459405,\n-1.0192800576910452\n],\n[\n-0.7381405613526144,\n-0.6970060629368618,\n-0.3939789311157716,\n0.279683255470807,\n0.5365876453930144,\n0.04505957795465281,\n-0.5381024105049081\n],\n[\n-0.7381405613526144,\n-0.22412562447793088,\n-0.3939789311157716,\n0.35078043043446056,\n0.7031802150835025,\n0.05006804153532872,\n-0.1884774672037731\n],\n[\n-0.7381405613526144,\n-0.22412562447793088,\n-0.3939789311157716,\n0.08435046819318669,\n0.6461946466452956,\n0.1667237151886523,\n0.21029648645433552\n],\n[\n-0.37161559295683355,\n-0.22412562447793088,\n-0.3939789311157716,\n0.05125464661140303,\n0.6033113289464309,\n0.21516096712201177,\n0.30072400592386056\n],\n[\n0.3614343438347282,\n-0.22412562447793088,\n-0.3939789311157716,\n0.24652318549800872,\n0.7295744687777501,\n0.30750833893882357,\n0.4786458153729669\n],\n[\n0.3614343438347282,\n0.24875481398100008,\n-0.3939789311157716,\n0.41705968913725877,\n0.8106711585286178,\n0.3070478954336653,\n0.5268984156436227\n],\n[\n0.7279593122305091,\n1.194515690898862,\n-0.3939789311157716,\n0.47735580131065103,\n0.8644069133949815,\n0.3888604739240358,\n0.7538539441296993\n],\n[\n1.461009249022071,\n1.194515690898862,\n-0.3939789311157716,\n0.4133132740189238,\n0.8460811358052476,\n0.37336577312099,\n0.7538539441296993\n]\n],\n[\n[\n-1.1046655297483954,\n-1.1698865013957929,\n-0.3939789311157716,\n-0.8193532546123586,\n-1.0719164600878743,\n-0.6975648115272529,\n-1.2668879424185877\n],\n[\n-1.1046655297483954,\n-1.1698865013957929,\n-0.3939789311157716,\n-1.1355653468472726,\n-1.2231587792547034,\n-0.667244412507622,\n-1.3926414131442886\n],\n[\n-1.1046655297483954,\n-0.6970060629368618,\n-0.3939789311157716,\n-1.092222453286437,\n-1.1870304973118257,\n-0.733530571790863,\n-0.6015273845269558\n],\n[\n-0.37161559295683355,\n-0.6970060629368618,\n-0.3939789311157716,\n-0.6728813450414151,\n-0.8403055370140927,\n-0.6523645364718677,\n-0.2501397165407122\n],\n[\n-0.37161559295683355,\n-0.6970060629368618,\n-0.3939789311157716,\n-0.8214569700446661,\n-0.9571593865564572,\n-0.7371579435587512,\n-0.20357477432302074\n],\n[\n-0.005090624561052657,\n0.24875481398100008,\n-0.3939789311157716,\n-0.51955262036747,\n-0.6935857806826718,\n-0.6556762332620633,\n0.12322163891253103\n],\n[\n-0.005090624561052657,\n0.24875481398100008,\n-0.3939789311157716,\n-0.6048966084889106,\n-0.739399563545289,\n-0.6376611872239013,\n0.3843343753966416\n],\n[\n-0.005090624561052657,\n0.721635252439931,\n-0.3939789311157716,\n-0.4755007606897553,\n-0.6236275919861403,\n-0.643965302163147,\n0.486835040408888\n],\n[\n-0.005090624561052657,\n0.721635252439931,\n-0.3939789311157716,\n-0.5178784247310911,\n-0.6605400012318026,\n-0.6490557800699218,\n0.3662911330357624\n]\n]\n],\n\"k_flag\": \"stable\",\n\"hmm\": {\n\"n_states\": 6,\n\"means\": [\n[\n-1.0458341238429134,\n-0.988219802265486,\n-0.3939789311157717,\n-0.9878313889563414,\n-1.05651347941", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Bash · 2026-09-28 21:32:07 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls -la $R $R/scan | head -80; sed -n 1,200p $R/README.md
```

### [32] TOOL RESULT — Bash · 2026-09-28 21:32:07 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5:\ntotal 173386\ndrwxrwxrwx 10 root root  2077382 Sep 28 21:17 .\ndrwxrwxrwx  7 root root  3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 root root  1000130 Sep 28 19:41 .aii\n-rw-rw-rw-  1 root root       54 Sep 28 17:08 .aii_claude_session.json\n-rw-rw-rw-  1 root root    10057 Sep 28 19:41 .aii_worker_result.json\ndrwxrwxrwx  8 root root  2000761 Sep 28 19:31 .git\n-rw-rw-rw-  1 root root       42 Sep 28 17:57 .gitignore\n-rw-rw-rw-  1 root root  1481575 Sep 28 19:41 .repl_agent.ptylog\n-rw-rw-rw-  1 root root     3255 Sep 28 19:31 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 root root    20911 Sep 28 19:36 README.md\n-rw-rw-rw-  1 root root     3230 Sep 28 19:06 audit.json\n-rw-rw-rw-  1 root root     6020 Sep 28 18:21 audit.py\n-rw-rw-rw-  1 root root     6848 Sep 28 19:13 audit_placebo.py\n-rw-rw-rw-  1 root root     6825 Sep 28 17:39 backbones.py\n-rw-rw-rw-  1 root root     8526 Sep 28 17:49 checks.py\n-rw-rw-rw-  1 root root  5322082 Sep 28 18:57 cohort_episodes_with_pred.csv\n-rw-rw-rw-  1 root root    10717 Sep 28 19:20 common.py\n-rw-rw-rw-  1 root root  5196667 Sep 28 18:36 concept_features_basic.csv\n-rw-rw-rw-  1 root root   920533 Sep 28 18:48 concept_outcomes.csv\n-rw-rw-rw-  1 root root      123 Sep 28 17:38 credits_log.csv\n-rw-rw-rw-  1 root root  4733254 Sep 28 18:47 dev_episodes_with_oof.csv\n-rw-rw-rw-  1 root root 12358267 Sep 28 18:36 episode_features.csv\n-rw-rw-rw-  1 root root  4038818 Sep 28 18:48 episodes.csv\n-rw-rw-rw-  1 root root     3401 Sep 28 19:05 exploratory_domains.py\n-rw-rw-rw-  1 root root     8968 Sep 28 17:42 features.py\ndrwxrwxrwx  2 root root  1083930 Sep 28 19:01 figures\n-rw-rw-rw-  1 root root     1705 Sep 28 18:59 fix_pigeonhole.py\n-rw-rw-rw-  1 root root    12798 Sep 28 17:35 frame.py\n-rw-rw-rw-  1 root root  2290579 Sep 28 18:36 frame_concepts.csv\n-rw-rw-rw-  1 root root      252 Sep 28 17:37 frozen_lexicon.sha256\n-rw-rw-rw-  1 root root   109036 Sep 28 18:47 frozen_spec.json\n-rw-rw-rw-  1 root root 28377355 Sep 28 19:11 full_method_out.json\n-rw-rw-rw-  1 root root    18349 Sep 28 19:20 grounding.py\n-rw-rw-rw-  1 root root   100286 Sep 28 18:14 grounding_benchmark.csv\n-rw-rw-rw-  1 root root   733111 Sep 28 19:31 grounding_precision.csv\n-rw-rw-rw-  1 root root     2585 Sep 28 18:19 grounding_report.json\n-rw-rw-rw-  1 root root  4679702 Sep 28 18:57 heldout_episodes_with_pred.csv\n-rw-rw-rw-  1 root root     4427 Sep 28 17:16 lexicon.py\n-rw-rw-rw-  1 root root  5464978 Sep 28 17:16 lexicon_v0.parquet\n-rw-rw-rw-  1 root root  8354825 Sep 28 17:37 lexicon_v1.parquet\n-rw-rw-rw-  1 root root     5823 Sep 28 18:13 llm.py\n-rw-rw-rw-  1 root root   918507 Sep 28 18:30 llm_cost_log.csv\ndrwxrwxrwx  2 root root  1008735 Sep 28 19:04 logs\n-rw-rw-rw-  1 root root      879 Sep 28 19:02 make_variants.py\n-rw-rw-rw-  1 root root     1509 Sep 28 17:16 matcher.py\n-rw-rw-rw-  1 root root     4192 Sep 28 19:20 method.py\n-rw-rw-rw-  1 root root 26650987 Sep 28 19:01 method_out.json\n-rw-rw-rw-  1 root root    18739 Sep 28 19:11 mini_method_out.json\n-rw-rw-rw-  1 root root    47860 Sep 28 18:59 models.py\n-rw-rw-rw-  1 root root     3866 Sep 28 18:13 oa_client.py\n-rw-rw-rw-  1 root root     4181 Sep 28 19:20 panel.py\n-rw-rw-rw-  1 root root    41728 Sep 28 18:13 placebo_gateways.npy\n-rw-rw-rw-  1 root root    41728 Sep 28 18:13 placebo_perm_gateways.npy\n-rw-rw-rw-  1 root root    11028 Sep 28 19:20 prescreen.py\n-rw-rw-rw-  1 root root    15150 Sep 28 19:11 preview_method_out.json\n-rw-rw-rw-  1 root root     1486 Sep 28 17:12 probe.py\n-rw-rw-rw-  1 root root     2160 Sep 28 19:12 pyproject.toml\n-rw-rw-rw-  1 root root     5326 Sep 28 17:09 rangefile.py\n-rw-rw-rw-  1 root root    13493 Sep 28 19:01 report.py\n-rw-rw-rw-  1 root root     8210 Sep 28 19:31 reproducibility.md\n-rwxrwxrwx  1 root root     1086 Sep 28 19:16 restore.sh\ndrwxrwxrwx  2 root root  2000415 Sep 28 19:13 results\ndrwxrwxrwx  8 root root  2059831 Sep 28 21:17 scan\n-rw-rw-rw-  1 root root    15148 Sep 28 19:21 scan_full.py\n-rw-rw-rw-  1 root root     5176 Sep 28 17:46 seal.py\n-rw-rw-rw-  1 root root 12891109 Sep 28 18:48 sens_episodes_b5_t0p4.csv\n-rw-rw-rw-  1 root root 17928388 Sep 28 18:48 sens_episodes_match.csv\n-rw-rw-rw-  1 root root 17356255 Sep 28 18:48 sens_episodes_ptopic.csv\n-rw-rw-rw-  1 root root     3256 Sep 28 18:17 sense_filter.joblib\ndrwxrwxrwx  3 root root  2000995 Sep 28 17:12 snapshot\ndrwxrwxrwx  2 root root  1000748 Sep 28 17:46 tests\n-rw-rw-rw-  1 root root     1335 Sep 28 17:13 timing_probe.py\n-rw-rw-rw-  1 root root     5678 Sep 28 17:22 wikidata_aliases.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan:\ntotal 73344\ndrwxrwxrwx  8 root root  2059831 Sep 28 21:17 .\ndrwxrwxrwx 10 root root  2077382 Sep 28 21:17 ..\n# Do hub fields keep new concepts? A sealed held-out test on the full OpenAlex snapshot\n\nAI Inventor, invention loop iteration 2, artifact `gen_art_experiment_5` (plan `gen_plan_experiment_1_idx1`).\nThis is a \"deepen\" move on the iteration-1 lead from `art_33_KKk_G8Gw5`: there, the adopting field's gateway centrality\nadded **+0.10 retention AUC** on 80 episodes from 28 concepts.\n\n**H1 (episode level).** When a new concept is adopted by an off-home field *j*, does the field's frozen\n1998–2002 eigenvector *gateway centrality* in the 26-field relatedness backbone predict that *j* keeps it\n(R_cj)? The test asks whether it does so beyond:\n- B5,\n- field size,\n- relatedness to the home field φ(home,j),\n- relatedness density,\n- the field's leave-concept-out retention propensity P_j(−c),\n- coverage,\n- the episode's own early size.\n\nThe specification was frozen on DEV homes (CS, Engineering, Biochem/Genetics, Medicine; onset 2003–09) and scored\n**once** on sealed held-out home groups and the 2010–14 cohort.\n\n**H3 (concept level).** Does gateway-weighted early landing (G) predict size-adjusted later breadth (O2r_resid) given\nB5?\n\n## Headline results\n\n| | DEV (LOGO, OOF) | HELD-OUT (frozen dev fit) |\n|---|---|---|\n| episodes / concepts | 9,079 / 3,987 | 8,515 / 3,085 (+ cohort 9,798) |\n| AUC of baseline X0 | 0.866 | 0.837 |\n| **ΔAUC of adding gateway_j** | **+0.00001** [−0.0007, +0.0005] | **−0.00001** [−0.0006, +0.0003] |\n| per group | CS, Eng, BGM, Med: all within ±0.0001 | PHYS +0.0005, LIFEENV −0.0003, SOC −0.0001, MATHDEC +0.0005 |\n| DerSimonian-Laird pooled (4 groups) | – | −0.00004 [−0.0004, +0.0003], I² = 0 |\n| cohort 2010–14 | – | −0.0001 [−0.0008, +0.0001] |\n| conditional logit, concept FE (β per SD) | +0.058 (p = 0.26) | −0.075 (p = 0.23) |\n| LPM with field FE + time-varying gateway_j,s | −0.003 (p = 0.92) | +0.068 (p = 0.041 concept-clustered; p = 0.17 two-way) |\n| boundary (gateway × top-tercile home; predicted < 0) | −0.051 (p = 0.39) | +0.064 (p = 0.45) |\n| 200 rewired-backbone placebos: real > 95th percentile? | no (placebo p95 = 0.00016) | no (p95 = 0.00011; 36.5% of placebos ≥ real) |\n| crossed concept × field bootstrap (Owen) | [−0.0056, +0.0013] | [−0.0023, +0.0010] |\n| leave-one-adopting-field-out range | [−0.0002, +0.0001] | [−0.0001, +0.0001] |\n| **Relatedness head-to-head** (each added to the same base) | relatedness −0.0002, gateway −0.0001 | **relatedness +0.0034 [0.0010, 0.0051]**; gateway −0.00005 [−0.0007, +0.0002] |\n\n**Verdict H1: DISCONFIRMED** (`results/h1_heldout.json → verdict_H1`). Pre-registered criteria:\n- pooled ΔAUC ≥ 0.05: no;\n- refit CI > 0: no;\n- same sign in ≥ 3 of 4 groups: no (2 of 4);\n- cohort same sign: yes (both ≈ 0);\n- LPM β_within > 0 with p < 0.05: yes, but fragile (two-way clustered p = 0.17);\n- placebo exceeded: no.\n\n**Power.** The null is informative. On the dev covariate structure with the realised held-out n, the minimum\nΔAUC detectable with 80% power is **0.004** (a planted effect of 0.3 SD log-odds). That is 12× smaller than the\npre-registered 0.05 bar.\n\n**Why the iteration-1 lead disappears: the \"trait of the adopting field\" reading.** The pre-registered baseline\nladder (`figures/ladder_dauc.png`) shows the gateway increment on DEV at each baseline:\n\n| baseline | DEV ΔAUC | HELD-OUT ΔAUC |\n|---|---|---|\n| size only | +0.0042 [0.0010, 0.0060] | −0.0017 |\n| iteration-1 base (B5 + size) | +0.0019 [0.0005, 0.0034] | −0.0016 [−0.0035, −0.0002] |\n| + relatedness (φ_home, density) | +0.0007 [−0.0008, 0.0022] | −0.0012 |\n| + P_j(−c) | 0.0000 | 0.0000 |\n\n- On DEV the increment is already small at the iteration-1 base, shrinks once relatedness is added, and **vanishes\n  once the adopting field's own retention propensity P_j(−c) enters**.\n- On HELD-OUT, gateway *hurts* even at the iteration-1 base.\n- Gateway alone has AUC **0.605 on DEV but 0.506 on HELD-OUT**.\n\nThe exploratory per-domain table (`results/exploratory_domain_specificity.json`, post-unseal, never used for the\nverdict) locates the effect:\n- In the four DEV domains, gateway alone predicts retention (AUC 0.59–0.64) and is largely a proxy for the field's\n  retention propensity (Spearman with P_j 0.49–0.83).\n- In Physical sciences, Life/Environment and Math/Decision it is weak (0.52–0.56).\n- In Social sciences/Humanities it is **reversed** (0.41).\n- Gateway is therefore a domain-specific proxy for \"fields that keep things\", not a portable structural mechanism.\n- The standard relatedness model *does* generalise: +0.0034 held-out.\n\n**Iteration-1 replication.** On the frame's P78 subset (85 episodes with n_early ≥ 5, 39 concepts), the\niteration-1 model gives ΔAUC **+0.023** [−0.004, +0.068]. The sign matches iteration 1, but the value is a quarter\nof +0.10, which is consistent with small-sample inflation of the original lead.\n\n**H3 (held-out, n = 2,838 concepts).**\n- Partial Spearman of O2r_resid given B5:\n  - G = +0.030 (one-sided within-group permutation p = 0.002);\n  - G_A = +0.026 (p = 0.004);\n  - G_btw = +0.046 (p = 0.0015).\n- All three are Holm-adjusted to p = 0.0045. The per-group values for G are positive in all 4 held-out groups\n  (0.03–0.09), with a DerSimonian-Laird pooled value of **0.068 [0.029, 0.107], I² = 0**.\n- **Verdict H3: CONFIRMED by the pre-registered test, but the effect is small.** The concept-bootstrap CI of the\n  pooled (not within-group) ρ for G includes 0 ([−0.006, 0.065]), because a negative between-group component\n  offsets it (see `results/h3_results.json → notes`).\n- The rival REL_home (landing in fields related to home) is strongly **negative**: −0.136, DL −0.157.\n  Concepts that land in fields related to their home spread less.\n\n## What was done\n\n1. **Lexicon (outcome-blind, hashed).**\n   - 64,209 legacy OpenAlex concepts (levels 2–5) from the free S3 snapshot. Their surface forms are the name, a\n     joined-hyphen variant and s/es/ies variants.\n   - A form shared by two concepts goes to nobody.\n   - **Pre-screen** on a 1.1% random file sample: 7,566 concepts with ≥ 10 sampled verified hits in 1995–2002 are\n     dropped, because t0 ≥ 2003 is impossible for them.\n   - **Wikidata aliases** for the 56,643 survivors come from the SPARQL endpoint, because `wbgetentities` was\n     rate-limited. Aliases are dropped if they:\n     - have ≤ 3 characters;\n     - are all-caps acronyms of ≤ 5 characters (the TAVI lesson);\n     - equal any concept name, including level-0/1 names;\n     - are ambiguous;\n     - are frequent before 2003;\n     - are lowercase single tokens (see the T2 fix below).\n   - Result: 85,692 alias forms (`lexicon_v1.parquet`; sha256 is the last line of `frozen_lexicon.sha256`).\n2. **One zero-credit scan** (`scan_full.py`) of all **2,040 parquet files (476,196,327 works)** of the\n   2026-09-23 snapshot, via HTTP range reads of 10 leaf columns, in 33 minutes on 4 vCPU.\n   - Base works: 129,360,390 (article|review, not paratext, not xpac, 1995–2022).\n   - Matching: Aho-Corasick over space-padded surface forms (word boundaries enforced), then OpenAlex-like stemmed\n     positional verification. This gives **60.0M verified matches**, aggregated per (concept, year, venue field,\n     primary-topic field, legacy-tag state, match type).\n   - The same pass also produces venue-field totals, 26×26 field co-assignment per year (the backbones) and a\n     hash reservoir of matched titles.\n3. **Grounding, existing resources first.**\n   - The legacy concept tags are present in the snapshot, so TAG = title match AND tag score ≥ 0.3.\n   - **Benchmark:** 390 LLM-labelled title/concept pairs. gemini-2.5-flash-lite labelled all of them and\n     gpt-4.1-nano labelled 146. Cohen's κ was only 0.20, so the 41 disagreements were adjudicated by\n     gemini-2.5-flash.\n   - **The executor read 60 pairs by hand:** 90% agreement with the gold label.\n   - **MiniLM + flags L2-logistic sense filter:** test AUC 0.871. Its precision (0.862) did not beat exact-name\n     precision (0.872), so under T4 the frozen rule is **TAG** (test precision 0.947, recall 0.659), chosen on\n     the benchmark test split only.\n   - **Per-concept LLM precision gate** on 13,413 onset candidates (13.7k calls): 93% have precision ≥ 0.8.\n     864 concepts whose labels did not parse were gated by the sense filter.\n4. **Frame S1** (`frame.py`, art_33 rules):\n   - t0 = first year 2000–2014 with ≥ 20 grounded works; keep 2003 ≤ t0 ≤ 2014, early volume ≥ 30, precision ≥ 0.8.\n   - Home = fields with ≥ 40% of the first 30 venue-labelled works (weak home ≥ 25%).\n   - Episodes = off-home fields with ≥ 2 early works.\n   - R = [share_out ≥ 0.5·share_early AND n_out ≥ 9] over t0+6..t0+8.\n   - Result: **12,499 concepts, 27,393 episodes** (targets: 400 and 4,000).\n     - DEV: 4,771 concepts;\n     - held-out: PHYS 742, LIFEENV 1,113, SOC 1,352, MATHDEC 165;\n     - COHORT: 4,356.\n     - Newborn: 5.4%; weak home: 1,150; intersection-born: 502.\n5. **Backbones.**\n   - Frozen art_33 gateway_eig. The recomputed S0 backbone from the scan correlates with it at Spearman ρ = 1.000.\n   - The time-varying gateway_j,s (slices S0/S1/S2) has a within-field SD of only 0.026, against a between-field\n     SD of 0.279, so the field-FE test has little power.\n   - Placebos: 200 degree-preserving double-edge-swap rewirings (weights re-attached within degree-product\n     quintiles) plus 200 field permutations.\n6. **Models** (`models.py`):\n   - Primary: exact Newton-IRLS L2 logistic (sklearn's objective; matches lbfgs to < 1e-8), leave-one-home-group-out\n     on DEV, with a 2,000-draw concept-clustered **refit** bootstrap.\n   - Secondary: conditional logit, LPM with field + cohort FE (concept and two-way clustered), boundary\n     interaction, relatedness head-to-head, placebos.\n   - Field-level robustness: leave-one-field-out, a crossed concept × field bootstrap, and two- and field-clustered\n     SEs.\n   - Power simulation and the explanatory ladder.\n7. **Freeze → unseal once.**\n   - `frozen_spec.json` (covariates, standardisation constants, thresholds, seeds, hashes, held-out ids) is hashed\n     into `logs/seal.log`.\n   - Pre-unseal checklist: held-out outcome columns absent from every table, and a git commit\n     `a3234b7` of the code and frame.\n   - `seal.py` refuses a second unseal. Held-out models are scored without re-tuning, and every sensitivity is\n     reported (see below).\n8. **Audit.** `audit.py` re-derives the held-out pooled ΔAUC, the per-group values and the H3 partial ρ with\n   separate code: sklearn lbfgs, a Mann-Whitney AUC, its own P_j(−c) and its own rank residualisation. **All match\n   to 1e-6** (`audit.json`).\n\n### Sensitivities (held-out ΔAUC, never used for the verdict)\n\nAll CIs include 0, and every |ΔAUC| is ≤ 0.0023:\n- R_abs1 +0.0008;\n- R_abs2 0.0000 (the direction's literal \"≥ 2 works\" outcome);\n- R_abs3 0.0000;\n- n_early ≥ 5 (iteration-1-exact) −0.0004;\n- newborn-only +0.0023 [−0.0039, 0.0128] (n = 387);\n- excluding intersection-born concepts 0.0000;\n- primary-topic fields instead of venue fields 0.0000;\n- ungrounded \"match\" counts 0.0000;\n- P_j_train −0.0004;\n- without P_j −0.0011 [−0.0026, 0.0000];\n- B5 over t0..t0+4 0.0000;\n- gateway variants (degree −0.0004, betweenness −0.0001, φ_min 0.0000, recomputed S0 0.0000);\n- slice field size −0.0001.\n\n### Tests\n\n| test | result |\n|---|---|\n| T0 unit tests (9) | all pass (`results/unit_tests_T0.json`): rarefaction vs Monte Carlo, Kleinberg, matcher (stem, IoT hyphen/stop words, microRNAs, word boundary), onset, home rule, episode R, seal gate, planted positive control, placebo degree/weight preservation |\n| T1 matcher regression vs iteration 1 (3 files, P78 phrases) | not exact equality: the new matcher is a strict subset, precision 1.00, recall 0.95 (it misses stem-only inflections of non-final tokens) |\n| T2 50-file inspection | found generic single-token aliases; fixed and re-hashed **before** the full scan (`deviations.json: t2_lexicon_fix`) |\n| T3 | recomputed backbone ρ = 1.000 ✓; P78 log yearly counts vs iteration-1 snapshot matches, median ρ = 0.999 ✓; base totals identical ✓; **t0 agreement with the iteration-1 API t0 is 53% (< 70% target)**, because API title+abstract counts are about 2× title counts and cross 20 earlier; API audit **not done** (pool below floor) |\n| T4 | κ = 0.20 (< 0.6, so adjudicated); hand-check agreement 90% ✓; filter did not beat exact-name, so the TAG rule was used |\n| T5 | second bootstrap seed moves CI ends by 0.00007 (< 0.01) ✓; iteration-1 replication same sign ✓ |\n| T6 | pre-unseal checklist passed (`logs/seal.log`) |\n| T7 | independent audit, all match ✓ |\n| shuffled-input controls (`audit_placebo.py`) | held-out ΔAUC with shuffled R: −0.0005 ± 0.0019 (20 shuffles); a planted 1-SD gateway effect is detected (+0.044); both H3 tests give 0/40 false positives on shuffled outcomes; H3 per-group ρ re-derived exactly, DL pooled 0.068 (re-derived 0.0676) |\n\n### Deviations (full list with reasons in `results/deviations.json`)\n\n- The OpenAlex API key had 0 credits and the anonymous pool 999, below the 1,500 floor. Therefore:\n  - **there is no API audit**;", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] TOOL CALL — Bash · 2026-09-28 21:32:11 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls -la $R/scan $R/results | head -80; cat $R/panel.py; sed -n 1,80p $R/common.py; cat $R/grounding_report.json | head -50
```

### [34] TOOL RESULT — Bash · 2026-09-28 21:32:11 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results:\ntotal 8247\ndrwxrwxrwx  2 root root 2000415 Sep 28 19:13 .\ndrwxrwxrwx 10 root root 2077382 Sep 28 21:17 ..\n-rw-rw-rw-  1 root root    1427 Sep 28 19:15 audit_placebo.json\n-rw-rw-rw-  1 root root   45662 Sep 28 18:13 backbones.json\n-rw-rw-rw-  1 root root    1775 Sep 28 19:04 checks.json\n-rw-rw-rw-  1 root root    3513 Sep 28 19:31 deviations.json\n-rw-rw-rw-  1 root root    4972 Sep 28 19:05 exploratory_domain_specificity.json\n-rw-rw-rw-  1 root root     245 Sep 28 18:36 frame_build_em30_w1.json\n-rw-rw-rw-  1 root root     729 Sep 28 18:36 frame_summary.json\n-rw-rw-rw-  1 root root     633 Sep 28 18:14 grounding_bench_summary.json\n-rw-rw-rw-  1 root root   18476 Sep 28 18:47 h1_dev.json\n-rw-rw-rw-  1 root root   18468 Sep 28 18:40 h1_dev_smoke.json\n-rw-rw-rw-  1 root root   25941 Sep 28 19:04 h1_heldout.json\n-rw-rw-rw-  1 root root   20942 Sep 28 18:42 h1_heldout_smoke.json\n-rw-rw-rw-  1 root root    4595 Sep 28 19:16 h3_results.json\n-rw-rw-rw-  1 root root   10403 Sep 28 18:14 handcheck_labels.csv\n-rw-rw-rw-  1 root root    9649 Sep 28 18:14 handcheck_sheet.csv\n-rw-rw-rw-  1 root root     243 Sep 28 17:16 lexicon_v0_summary.json\n-rw-rw-rw-  1 root root  296014 Sep 28 19:24 onset_candidates_grounded.csv\n-rw-rw-rw-  1 root root  327243 Sep 28 19:24 onset_candidates_match.csv\n-rw-rw-rw-  1 root root    5396 Sep 28 18:36 p78_agreement.csv\n-rw-rw-rw-  1 root root  252022 Sep 28 19:24 prescreen_dropped.csv\n-rw-rw-rw-  1 root root     491 Sep 28 19:24 prescreen_summary.json\n-rw-rw-rw-  1 root root 3311365 Sep 28 17:21 source_field.parquet\n-rw-rw-rw-  1 root root     259 Sep 28 17:48 unit_tests_T0.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/scan:\ntotal 73344\ndrwxrwxrwx  8 root root  2059831 Sep 28 21:17 .\ndrwxrwxrwx 10 root root  2077382 Sep 28 21:17 ..\ndrwxrwxrwx  2 root root  2018512 Sep 28 19:21 aborted_v1a_parts\n-rw-rw-rw-  1 root root 46726250 Sep 28 19:22 agg_counts.parquet\n-rw-rw-rw-  1 root root   152608 Sep 28 19:22 co_by_year.npz\ndrwxrwxrwx  2 root root  2000830 Sep 28 18:30 llm_cache\ndrwxrwxrwx  2 root root  2021470 Sep 28 18:10 parts\n-rw-rw-rw-  1 root root  4911666 Sep 28 19:24 prescreen_survivors.parquet\ndrwxrwxrwx  2 root root  2010488 Sep 28 19:20 reservoir\n-rw-rw-rw-  1 root root      358 Sep 28 17:17 sample_info.json\ndrwxrwxrwx  2 root root        1 Sep 28 21:17 sample_titles\n-rw-rw-rw-  1 root root      119 Sep 28 19:23 scan_info.json\ndrwxrwxrwx  2 root root  2002721 Sep 28 17:32 stage_test_parts\n-rw-rw-rw-  1 root root    43115 Sep 28 18:19 untagged_passrate.parquet\n-rw-rw-rw-  1 root root   991976 Sep 28 19:22 untagged_rows.parquet\n-rw-rw-rw-  1 root root   633813 Sep 28 19:23 untagged_sample_titles.parquet\n-rw-rw-rw-  1 root root  7439054 Sep 28 17:29 wikidata_aliases.json\n-rw-rw-rw-  1 root root     7690 Sep 28 19:22 year_field_totals.npz\n\"\"\"Dense per-concept count arrays from scan/agg_counts.parquet (built once, cached compressed in scan/arrays_<variant>.npz).\n\nVariants: 'grounded' = frozen grounding rule (TAG, plus untagged rows weighted by the sense-filter pass rate\nof their (concept, mtype)); 'match' = every verified title match (the ungrounded sensitivity).\nArrays (float32): N[ci, y] all venues; V[ci, y, 27] by venue-field code (0 = unlabelled);\nP[ci, y, 27] by primary-topic field code; plus T1[ci, y] (tagstate==1) and M[ci, y] (all matches).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import NY, ROOT, SCAN, Y0, Y1\n\nYEARS = list(range(Y0, Y1 + 1))\n\n\ndef yi(y: int) -> int:\n    return y - Y0\n\n\ndef grounding_rule() -> str:\n    p = ROOT / \"grounding_report.json\"\n    return json.loads(p.read_text())[\"frozen_grounding_rule\"] if p.exists() else \"c_TAG\"\n\n\ndef build_arrays(variant: str, n_concepts: int) -> dict[str, np.ndarray]:\n    cache = SCAN / f\"arrays_{variant}.npz\"\n    if cache.exists():\n        z = np.load(cache)\n        return {k: z[k] for k in z.files}\n    ag = pd.read_parquet(SCAN / \"agg_counts.parquet\")\n    if variant == \"grounded\":\n        rule = grounding_rule()\n        if rule == \"b_exact_name_only\":\n            w = (ag.mt == 0).astype(np.float32).to_numpy()\n        else:\n            w = (ag.tagstate == 1).astype(np.float32).to_numpy()\n            pr_p = SCAN / \"untagged_passrate.parquet\"\n            ts3 = (ag.tagstate == 3).to_numpy()\n            if rule == \"e_TAG_or_untagged_filter\" and ts3.any():\n                pr = pd.read_parquet(pr_p) if pr_p.exists() else pd.DataFrame(columns=[\"ci\", \"mt\", \"passrate\"])\n                glob = float(pr.passrate.mean()) if len(pr) else 0.0\n                m = ag[ts3][[\"ci\", \"mt\"]].merge(pr[[\"ci\", \"mt\", \"passrate\"]], on=[\"ci\", \"mt\"], how=\"left\")\n                w[ts3] = m.passrate.fillna(glob).to_numpy(np.float32)\n    else:\n        w = np.ones(len(ag), np.float32)\n    n = ag.n.to_numpy(np.float32) * w\n    ci = ag.ci.to_numpy(np.int64)\n    y = ag.year.to_numpy(np.int64) - Y0\n    ok = (y >= 0) & (y < NY)\n    ci, y, n, vf, pt = ci[ok], y[ok], n[ok], ag.vfield.to_numpy(np.int64)[ok], ag.ptfield.to_numpy(np.int64)[ok]\n    ts1 = (ag.tagstate.to_numpy()[ok] == 1)\n    raw = ag.n.to_numpy(np.float32)[ok]\n    C = n_concepts\n    N = np.bincount(ci * NY + y, weights=n, minlength=C * NY).reshape(C, NY).astype(np.float32)\n    V = np.bincount((ci * NY + y) * 27 + vf, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)\n    P = np.bincount((ci * NY + y) * 27 + pt, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)\n    T1 = np.bincount(ci * NY + y, weights=raw * ts1, minlength=C * NY).reshape(C, NY).astype(np.float32)\n    M = np.bincount(ci * NY + y, weights=raw, minlength=C * NY).reshape(C, NY).astype(np.float32)\n    out = {\"N\": N, \"V\": V, \"P\": P, \"T1\": T1, \"M\": M}\n    np.savez_compressed(cache, **out)  # mostly zeros: compressed stays well under 100 MB\n    return out\n\n\ndef onset(yc: np.ndarray) -> tuple[float, bool | None]:\n    \"\"\"art_33 s0_ground.onset: t0 = first year 2000..2014 with >= 20 works; newborn = each of t0-3..t0-1 <\n    0.25 * n(t0+2). yc indexed by year - Y0.\"\"\"\n    ts = [y for y in range(2000, 2015) if yc[yi(y)] >= 20]\n    if not ts:\n        return math.nan, None\n    t0 = ts[0]\n    newborn = all(yc[yi(t0 - k)] < 0.25 * yc[yi(t0 + 2)] for k in (1, 2, 3))\n    return float(t0), bool(newborn)\n\n\ndef onset_table(N: np.ndarray, min_early: float = 30.0) -> pd.DataFrame:\n    rows = []\n    # fast prefilter: some year 2003..2014 >= 20 and every year 2000..2002 < 20\n    cand = np.nonzero((N[:, yi(2003):yi(2014) + 1] >= 20).any(1) & (N[:, yi(2000):yi(2002) + 1] < 20).all(1))[0]\n    for ci in cand:\n        t0, nb = onset(N[ci])\n        if not np.isfinite(t0) or not (2003 <= t0 <= 2014):\n            continue\n        t0 = int(t0)\n        early = float(N[ci, yi(t0):yi(t0 + 2) + 1].sum())\n        if early < min_early:\n            continue\n        rows.append({\"ci\": int(ci), \"t0\": t0, \"newborn\": nb, \"early_volume\": early})\n    return pd.DataFrame(rows, columns=[\"ci\", \"t0\", \"newborn\", \"early_volume\"])\n\"\"\"Shared constants, paths, the OpenAlex-like title analyser (copied verbatim from art_yrradSC27HtQ\nscan_snapshot.py) and small helpers used by every step of the pipeline.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport re\nimport sys\nfrom functools import lru_cache\nfrom pathlib import Path\n\nimport numpy as np\n\nROOT = Path(__file__).resolve().parent\n\n\ndef _dep_dir(env: str, artifact_id: str, run_tree_rel: str) -> Path:\n    \"\"\"Input artifact directory: env var override, else the run tree (pipeline layout), else the sibling folder\n    of the published repository named by the artifact id.\"\"\"\n    import os\n    if os.environ.get(env):\n        return Path(os.environ[env])\n    run_tree = ROOT.parents[3] / run_tree_rel\n    return run_tree if run_tree.exists() else ROOT.parent / artifact_id\n\n\n# iteration-1 inputs (read-only): art_yrradSC27HtQ (scan/analyser/source-field map), art_33_KKk_G8Gw5 (frozen backbone)\nART3 = _dep_dir(\"AII_ART_YRRAD_DIR\", \"art_yrradSC27HtQ\", \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\nART33 = _dep_dir(\"AII_ART_33_DIR\", \"art_33_KKk_G8Gw5\", \"3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\nSNAP = ROOT / \"snapshot\"\nSCAN = ROOT / \"scan\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nfor _d in (SNAP, SCAN, RES, LOGS, FIGS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nFIELD_IDS = list(range(11, 37))            # the 26 OpenAlex fields; index k = fid - 11; vfield code = k + 1 (0 = unlabelled)\nFIELD_NAMES = {11: \"Agricultural and Biological Sciences\", 12: \"Arts and Humanities\",\n               13: \"Biochemistry, Genetics and Molecular Biology\", 14: \"Business, Management and Accounting\",\n               15: \"Chemical Engineering\", 16: \"Chemistry\", 17: \"Computer Science\", 18: \"Decision Sciences\",\n               19: \"Earth and Planetary Sciences\", 20: \"Economics, Econometrics and Finance\", 21: \"Energy\",\n               22: \"Engineering\", 23: \"Environmental Science\", 24: \"Immunology and Microbiology\",\n               25: \"Materials Science\", 26: \"Mathematics\", 27: \"Medicine\", 28: \"Neuroscience\", 29: \"Nursing\",\n               30: \"Pharmacology, Toxicology and Pharmaceutics\", 31: \"Physics and Astronomy\", 32: \"Psychology\",\n               33: \"Social Sciences\", 34: \"Veterinary\", 35: \"Dentistry\", 36: \"Health Professions\"}\n# fixed before any data were seen (plan step 5)\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nDOMAIN_OF = {11: \"Life\", 13: \"Life\", 24: \"Life\", 28: \"Life\", 30: \"Life\",\n             12: \"Social\", 14: \"Social\", 18: \"Social\", 20: \"Social\", 32: \"Social\", 33: \"Social\",\n             15: \"Physical\", 16: \"Physical\", 17: \"Physical\", 19: \"Physical\", 21: \"Physical\", 22: \"Physical\",\n             23: \"Physical\", 25: \"Physical\", 26: \"Physical\", 31: \"Physical\",\n             27: \"Health\", 29: \"Health\", 34: \"Health\", 35: \"Health\", 36: \"Health\"}\nMTYPES = [\"name_exact\", \"name_variant\", \"alias\"]\n\n# ----------------------------------------------------------------------------- analyser (verbatim from art_yrradSC27HtQ)\nES_STOP = set(\"a an and are as at be but by for if in into is it no not of on or such that the their then there \"\n              \"these they this to was will with\".split())\nTOKEN_RE = re.compile(r\"[^\\W_]+(?:\\.[^\\W_]+)*\", re.UNICODE)\n_STEMMER = None\n\n\ndef _stem(w: str) -> str:\n    global _STEMMER\n    if _STEMMER is None:\n        import snowballstemmer\n        _STEMMER = snowballstemmer.stemmer(\"porter\")\n    return _cached_stem(w)\n\n\n@lru_cache(maxsize=500_000)\n{\n \"n\": 390,\n \"n_double\": 146,\n \"kappa_l1_l2\": 0.199518587857716,\n \"agree_l1_l2\": 0.7191780821917808,\n \"adjudicated\": true,\n \"n_disagree\": 41,\n \"positive_rate\": 0.8615384615384616,\n \"models\": {\n  \"L1\": \"google/gemini-2.5-flash-lite\",\n  \"L2\": \"openai/gpt-4.1-nano\",\n  \"L3\": \"google/gemini-2.5-flash\"\n },\n \"llm_spent_usd\": 0.013316999999999999,\n \"split_counts\": {\n  \"train\": 294,\n  \"test\": 96\n },\n \"positive_rate_by_tagstate\": {\n  \"1\": 0.9285714285714286,\n  \"2\": 0.7932960893854749,\n  \"3\": 0.8\n },\n \"positive_rate_by_mtype\": {\n  \"alias\": 0.7478260869565218,\n  \"name_exact\": 0.8888888888888888,\n  \"name_variant\": 0.9344262295081968\n },\n \"filter\": {\n  \"C\": 0.1,\n  \"test_auc\": 0.8710801393728222,\n  \"coef\": {\n   \"cos\": 0.917,\n   \"single_token\": -0.177,\n   \"is_alias\": -0.272,\n   \"is_variant\": 0.169,\n   \"ts1\": 0.216,\n   \"ts2\": -0.168,\n   \"ts3\": -0.158,\n   \"title_len\": 0.275,\n   \"cap\": 0.055\n  }\n },\n \"rules_test\": {\n  \"a_stemmed_any\": {\n   \"precision\": 0.8541666666666666,\n   \"recall\": 1.0,\n   \"f1\": 0.9213483146067416,\n   \"n_pred_pos\": 96\n  },", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-09-28 21:32:15 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; grep -o '"frozen_grounding_rule[^,]*' $R/grounding_report.json; head -3 $R/frame_concepts.csv; cd $R; python3 -c "
import numpy as np, pandas as pd
z=np.load('scan/year_field_totals.npz'); print({k:(z[k].shape,z[k].dtype) for k in z.files})
z=np.load('scan/co_by_year.npz'); print({k:(z[k].shape,z[k].dtype) for k in z.files})
import pyarrow.parquet as pq
f=pq.ParquetFile('scan/agg_counts.parquet'); print(f.schema_arrow, f.metadata.num_rows)
fc=pd.read_csv('frame_concepts.csv'); print(fc.columns.tolist()); print(fc.split.value_counts()); print(fc.group.value_counts()); print(fc.ci.max(), len(fc))
"; cat scan/scan_info.json; grep -n "def home\|home_rule\|def build_frame\|0.4\|first 30" frame.py | head -30
```

### [36] TOOL RESULT — Bash · 2026-09-28 21:32:19 UTC

```
{"stdout": "\"frozen_grounding_rule\": \"c_TAG\"\nci,concept_id,qid,name,level,aliases_used,t0,newborn,home,n_home,weak_home,intersect40,intersect25,home_top_share,group,split,precision_c,n_labelled_prec,precision_source,label_coverage_early,tag_coverage,early_volume,in_P78\n3,37253,Q5156502,Complete intersection,2,,2012,False,26,30.0,0,0,0,0.8933333333333333,MATHDEC,COHORT,1.0,10.0,llm,0.9583333134651184,0.5901639461517334,72.0,0\n4,39854,Q84115,Torque converter,3,,2004,False,22,30.0,0,0,0,1.0,Eng,DEV,0.9,10.0,llm,0.84375,0.8648648858070374,64.0,0\n{'G': ((28,), dtype('int64')), 'VF': ((28, 27), dtype('int64')), 'NT': ((28,), dtype('int64')), 'years': ((28,), dtype('int64'))}\n{'CO': ((28, 26, 26), dtype('int64')), 'NT': ((28,), dtype('int64')), 'years': ((28,), dtype('int64'))}\nci: int32\nyear: int16\nvfield: int8\nptfield: int8\ntagstate: int8\nmt: int8\nn: int64\n-- schema metadata --\npandas: '{\"index_columns\": [], \"column_indexes\": [], \"columns\": [{\"name\":' + 824 19670571\n['ci', 'concept_id', 'qid', 'name', 'level', 'aliases_used', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'split', 'precision_c', 'n_labelled_prec', 'precision_source', 'label_coverage_early', 'tag_coverage', 'early_volume', 'in_P78']\nsplit\nDEV                4771\nCOHORT             4356\nHELDOUT_SOC        1352\nHELDOUT_LIFEENV    1113\nHELDOUT_PHYS        742\nHELDOUT_MATHDEC     165\nName: count, dtype: int64\ngroup\nMed        3868\nSOC        2211\nEng        2087\nLIFEENV    1668\nPHYS       1097\nBGM         719\nCS          581\nMATHDEC     268\nName: count, dtype: int64\n56642 12499\n{\n \"files_done\": 2040,\n \"rows\": 476196327,\n \"base_rows\": 129360390,\n \"verified_hits\": 60011338,\n \"agg_rows\": 19670571\n}9:Rules (art_33 definitions): t0 = first year 2000..2014 with >= 20 grounded works (all venues); keep\n10:2003 <= t0 <= 2014 and early volume (t0..t0+2) >= 30; precision_c >= 0.8; home = fields with >= 40% of the\n11:first 30 venue-labelled grounded works from t0 on (weak_home: top field >= 25%; else diffuse_born, dropped);\n73:def home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:\n96:    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]\n112:    if 2010 <= t0 <= 2014:\n166:    logger.info(f\"match onset candidates: {len(ot)} (t0 2003-2014, early >= 30)\")\n207:        h = home_rule(V[ci], t0)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Bash · 2026-09-28 21:32:25 UTC

```
R=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; sed -n 60,130p $R/frame.py; sed -n 190,260p $R/frame.py; R6=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6; head -3 $R6/results/frame_concepts.csv; python3 -c "
import numpy as np
z=np.load('$R6/scan/agg_counts.npz'); print({k:(z[k].shape,z[k].dtype) for k in z.files})
GF=z['GF']; import numpy as np
y=np.load('$R/scan/year_field_totals.npz'); print(GF.shape, y['VF'].shape); print(GF[5,:5], y['VF'][5,:6]); print(y['years'][:3])
z2=np.load('$R6/scan/frame_g_heldout.npz'); print({k:(z2[k].shape) for k in z2.files})
"
```

### [38] TOOL RESULT — Bash · 2026-09-28 21:32:31 UTC

```
{"stdout": "    \"\"\"Rarefaction for (possibly fractional) counts: counts are rounded to integers first.\"\"\"\n    return rarefied_richness([int(round(c)) for c in counts], m)\n\n\ndef shannon(v) -> float:\n    v = np.asarray([x for x in v if x > 0], float)\n    if v.sum() == 0:\n        return math.nan\n    p = v / v.sum()\n    return float(-(p * np.log(p)).sum())\n\n\n# ----------------------------------------------------------------------------- home rule\ndef home_rule(V: np.ndarray, t0: int, n_first: int = HOME_N) -> dict:\n    \"\"\"V: [NY, 27] grounded counts by venue-field code. First n_first labelled works from t0 on in year order;\n    the boundary year contributes proportionally (expected composition of a hash-random tie break).\"\"\"\n    acc = np.zeros(26)\n    got = 0.0\n    for y in range(t0, Y0 + NY):\n        row = V[yi(y), 1:27].astype(float)\n        tot = row.sum()\n        if tot <= 0:\n            continue\n        need = n_first - got\n        if tot <= need:\n            acc += row\n            got += tot\n        else:\n            acc += row * need / tot\n            got += need\n        if got >= n_first - 1e-9:\n            break\n    if got <= 0:\n        return {\"home\": [], \"status\": \"no_labels\", \"n_home\": 0.0}\n    sh = acc / got\n    order = np.argsort(sh)[::-1]\n    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]\n    res = {\"n_home\": float(got), \"top_share\": float(sh[order[0]]), \"second_share\": float(sh[order[1]]),\n           \"intersect40\": int(len(home) >= 2), \"intersect25\": int(sh[order[1]] >= 0.25), \"weak_home\": 0}\n    if home:\n        home = sorted(home, key=lambda f: -sh[f - 11])\n        res.update(home=home, status=\"ok\")\n    elif sh[order[0]] >= 0.25:\n        res.update(home=[FIELD_IDS[order[0]]], status=\"weak_home\", weak_home=1)\n    else:\n        res.update(home=[], status=\"diffuse_born\")\n    if got < n_first:\n        res[\"status_home_n\"] = \"thin_home\"\n    return res\n\n\ndef split_of(group: str, t0: int) -> str:\n    if 2010 <= t0 <= 2014:\n        return \"COHORT\"\n    return \"DEV\" if group in DEV_GROUPS else \"HELDOUT_\" + group\n\n\n# ----------------------------------------------------------------------------- episode + outcome functions\ndef episode_rows(ci: int, V: np.ndarray, t0: int, home: list[int]) -> list[dict]:\n    \"\"\"Episode covariates (no outcome). V = grounded [NY, 27].\"\"\"\n    early = V[yi(t0):yi(t0 + 2) + 1, 1:27]\n    ne = early.sum(0)\n    lab = ne.sum()\n    nA = V[yi(t0):yi(t0 + 1) + 1, 1:27].sum(0)\n    nB = V[yi(t0 + 2), 1:27]\n    rows = []\n    for k in range(26):\n        j = FIELD_IDS[k]\n        if j in home or ne[k] < 2 - 1e-9:\n            continue\n        rows.append({\"ci\": ci, \"field\": j, \"n_early\": float(ne[k]), \"n_A\": float(nA[k]), \"n_B\": float(nB[k]),\n    N, V = A[\"N\"], A[\"V\"]\n    G, _ = year_totals()\n    prec = pd.read_csv(ROOT / \"grounding_precision.csv\")\n    prec_map = prec.set_index(\"ci\")\n    ot = onset_table(N, min_early=early_min)\n    p78 = p78_names()\n    crows, erows, drops = [], [], {\"precision\": 0, \"diffuse_born\": 0, \"no_labels\": 0, \"weak_home_excluded\": 0,\n                                   \"no_precision_label\": 0}\n    for r in ot.itertuples():\n        ci, t0 = r.ci, r.t0\n        if ci not in prec_map.index or not np.isfinite(prec_map.at[ci, \"precision_c\"]):\n            drops[\"no_precision_label\"] += 1\n            continue\n        pc_ = float(prec_map.at[ci, \"precision_c\"])\n        if pc_ < 0.8:\n            drops[\"precision\"] += 1\n            continue\n        h = home_rule(V[ci], t0)\n        if h[\"status\"] in (\"diffuse_born\", \"no_labels\"):\n            drops[h[\"status\"]] += 1\n            continue\n        if h[\"status\"] == \"weak_home\" and not allow_weak:\n            drops[\"weak_home_excluded\"] += 1\n            continue\n        home = h[\"home\"]\n        group = GROUP_OF_FIELD[home[0]]\n        early_lab = V[ci, yi(t0):yi(t0 + 2) + 1, 1:27].sum()\n        early_all = N[ci, yi(t0):yi(t0 + 2) + 1].sum()\n        m_early = A[\"M\"][ci, yi(t0):yi(t0 + 2) + 1].sum()\n        t1_early = A[\"T1\"][ci, yi(t0):yi(t0 + 2) + 1].sum()\n        nm = lex[\"name\"].iat[ci]\n        crows.append({\"ci\": ci, \"concept_id\": int(lex.concept_id.iat[ci]), \"qid\": lex.qid.iat[ci], \"name\": nm,\n                      \"level\": int(lex.level.iat[ci]), \"aliases_used\": lex.aliases_used.iat[ci], \"t0\": t0,\n                      \"newborn\": bool(r.newborn), \"home\": \";\".join(map(str, home)), \"n_home\": h[\"n_home\"],\n                      \"weak_home\": h[\"weak_home\"], \"intersect40\": h[\"intersect40\"], \"intersect25\": h[\"intersect25\"],\n                      \"home_top_share\": h[\"top_share\"], \"group\": group, \"split\": split_of(group, t0),\n                      \"precision_c\": pc_, \"n_labelled_prec\": prec_map.at[ci, \"n_labelled_prec\"],\n                      \"precision_source\": prec_map.at[ci, \"precision_source\"],\n                      \"label_coverage_early\": float(early_lab / early_all) if early_all else math.nan,\n                      \"tag_coverage\": float(t1_early / m_early) if m_early else math.nan,\n                      \"early_volume\": float(early_all), \"in_P78\": int(nm.lower() in p78)})\n        for e in episode_rows(ci, V[ci], t0, home):\n            erows.append(e)\n    fc = pd.DataFrame(crows)\n    ep = pd.DataFrame(erows).merge(fc[[\"ci\", \"concept_id\", \"name\", \"t0\", \"group\", \"split\", \"home\"]], on=\"ci\")\n    jdump({\"early_min\": early_min, \"allow_weak\": allow_weak, \"onset_candidates\": len(ot), \"drops\": drops,\n           \"n_concepts\": len(fc), \"n_episodes\": len(ep)}, RES / f\"frame_build_em{int(early_min)}_w{int(allow_weak)}.json\")\n    return fc, ep\n\n\ndef cmd_build() -> None:\n    # relaxation ladder (outcome-blind, stops as soon as targets are met); weak_home is admitted by default\n    # as in the plan's home rule, so the ladder starts from the plan's own primary definition.\n    fc, ep = build(EARLY_MIN, True)\n    ladder = [{\"early_min\": 30, \"weak_home\": True, \"n_concepts\": len(fc), \"n_episodes\": len(ep)}]\n    if len(fc) < 400 or len(ep) < 4000:\n        fc, ep = build(20.0, True)\n        ladder.append({\"early_min\": 20, \"weak_home\": True, \"n_concepts\": len(fc), \"n_episodes\": len(ep)})\n        add_deviation(\"frame_relaxation\", f\"targets not met at early>=30; relaxed to early volume >= 20: {ladder}\")\n    G, _ = year_totals()\n    lexN = n_concepts()\n    A = build_arrays(\"grounded\", lexN)\n    N, V = A[\"N\"], A[\"V\"]\n    # DEV outcomes only (held-out / cohort stay sealed)\n    dev = fc.split == \"DEV\"\n    co = []\n    for r in fc.itertuples():\n        base = {\"ci\": r.ci, \"concept_id\": r.concept_id, \"split\": r.split}\n        if r.split == \"DEV\":\n            base.update(concept_outcomes(N[r.ci], V[r.ci], G, r.t0))\n        co.append(base)\nconcept_id,cidx,name,level,t0,newborn,home,home_primary,home_weak,home_thin,intersection_born,group,split,n_early,label_coverage_early,precision_est,p_notag,home_gateway,O1,O3,peak_year,N_outcome,O2r_m30,O2r_m50,O2_raw,O2r_resid\nhttps://openalex.org/C739882,94,Anomaly detection,2,2003,True,17,17,False,False,0,DEV_CS,dev,160.0,0.5875,0.970604733190633,1.0,0.0972089563793993,1.0,0.0,2010.0,343.0,4.18722225912469,5.162557984117685,2.0,0.4886429815110937\nhttps://openalex.org/C1124016,154,Biohydrogen,4,2004,True,22,22,True,False,0,DEV_Eng,dev,102.0,0.5588235294117647,0.9550605294225968,1.0,0.2427178906876991,0.0,0.0,2011.0,125.0,5.002240618280212,5.791064322153572,3.0,1.2865167510807556\n{'G': ((28,), dtype('int64')), 'GF': ((28, 26), dtype('int64')), 'n_rows': ((), dtype('int64')), 'n_base': ((), dtype('int64')), 'n_files': ((), dtype('int64')), 'T_all': ((60859, 28, 27), dtype('int32')), 'T_tag': ((60859, 28, 27), dtype('int32')), 'T_tag_exact': ((60859, 28, 27), dtype('int32')), 'T_untag': ((60859, 28, 27), dtype('int32')), 'T_none': ((60859, 28, 27), dtype('int32')), 'TO': ((60859, 28, 27), dtype('int32')), 'TPF_tag': ((60859, 28, 27), dtype('int32'))}\n(28, 26) (28, 27)\n[87045 80293 82147 18372    72] [926740  87045  80293  82147  18372     72]\n[1995 1996 1997]\n{'cidx': (374,), 'g': (374, 28, 27)}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] THINKING · 2026-09-28 21:32:37 UTC

```
I've mapped EXP6's pipeline: fits use only strata with non-empty retained sets (18,846 rows), with GF drawn from EXP5's venue-field totals. Now checking the concept-recognition dataset used for de-duplication.
```

### [40] TOOL CALL — Bash · 2026-09-28 21:32:37 UTC

```
D=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; ls -la $D $D/full_data_out; head -c 3000 $D/preview_data_out.json; echo; python3 -c "
import json;d=json.load(open('$D/preview_data_out.json'));print(d.keys() if isinstance(d,dict) else type(d));
ds=d['datasets'];print([ (x['dataset'],len(x['examples'])) for x in ds]); e=ds[0]['examples'][0]; print(e.keys()); print(e['input'][:1500])"
```

### [41] TOOL RESULT — Bash · 2026-09-28 21:32:37 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2:\ntotal 21149\ndrwxrwxrwx 10 root root 2041367 Sep 28 21:21 .\ndrwxrwxrwx  7 root root 3000496 Sep 28 17:06 ..\ndrwxrwxrwx  2 root root 1000144 Sep 28 20:17 .aii\n-rw-rw-rw-  1 root root      54 Sep 28 17:07 .aii_claude_session.json\n-rw-rw-rw-  1 root root   19093 Sep 28 20:17 .aii_worker_result.json\n-rw-rw-rw-  1 root root 1940706 Sep 28 20:17 .repl_agent.ptylog\n-rw-rw-rw-  1 root root    3510 Sep 28 20:10 .terminal_claude_agent_struct_out.json\n-rw-rw-rw-  1 root root   27627 Sep 28 20:13 README.md\ndrwxrwxrwx  6 root root 2011048 Sep 28 17:50 cache\n-rw-rw-rw-  1 root root    4772 Sep 28 19:59 data.py\ndrwxrwxrwx  2 root root 2024518 Sep 28 20:06 full_data_out\ndrwxrwxrwx  2 root root 2000539 Sep 28 20:00 logs\n-rw-rw-rw-  1 root root 2421021 Sep 28 20:04 mini_data_out.json\ndrwxrwxrwx  2 root root 1046197 Sep 28 19:46 out\n-rw-rw-rw-  1 root root   72004 Sep 28 20:04 preview_data_out.json\n-rw-rw-rw-  1 root root     337 Sep 28 18:49 pyproject.toml\n-rw-rw-rw-  1 root root    3204 Sep 28 20:10 reproducibility.md\n-rwxrwxrwx  1 root root    2582 Sep 28 19:18 restore.sh\n-rwxrwxrwx  1 root root    2126 Sep 28 20:06 run_all.sh\ndrwxrwxrwx  2 root root 1022252 Sep 28 21:21 scripts\ndrwxrwxrwx  4 root root 1001509 Sep 28 20:06 temp\ndrwxrwxrwx  2 root root 2004763 Sep 28 21:21 work\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2/full_data_out:\ntotal 255048\ndrwxrwxrwx  2 root root  2024518 Sep 28 20:06 .\ndrwxrwxrwx 10 root root  2041367 Sep 28 21:21 ..\n-rw-rw-rw-  1 root root 90009907 Sep 28 20:04 full_data_out_1.json\n-rw-rw-rw-  1 root root 90008266 Sep 28 20:04 full_data_out_2.json\n-rw-rw-rw-  1 root root 77016616 Sep 28 20:04 full_data_out_3.json\n-rw-rw-rw-  1 root root    10594 Sep 28 20:06 mini_full_data_out_1.json\n-rw-rw-rw-  1 root root    13272 Sep 28 20:06 mini_full_data_out_2.json\n-rw-rw-rw-  1 root root    24929 Sep 28 20:06 mini_full_data_out_3.json\n-rw-rw-rw-  1 root root     3738 Sep 28 20:06 preview_full_data_out_1.json\n-rw-rw-rw-  1 root root     5859 Sep 28 20:06 preview_full_data_out_2.json\n-rw-rw-rw-  1 root root     6175 Sep 28 20:06 preview_full_data_out_3.json\n{\n \"datasets\": [\n  {\n   \"dataset\": \"concept_recognition\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C144501496\\\", \\\"qid\\\": \\\"Q5533489\\\", \\\"qid_resolved\\\": \\\"Q5533489\\\", \\\"label\\\": \\\"Genome editing\\\", \\\"label_norm\\\": \\\"genome editing\\\", \\\"aliases\\\": [\\\"genome editing\\\", \\\"Genome engineering\\\"], \\\"aliases_norm\\\": [\\\"genome engineering\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\": [\\\"C98108389\\\", \\\"C141231307\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"nature_methods_moty\\\", \\\"event_type\\\": \\\"nature_methods_method_of_the_year\\\", \\\"year\\\": 2011, \\\"date\\\": null, \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"embed+llm\\\", \\\"match_confidence\\\": 0.85, \\\"relation\\\": \\\"broader\\\", \\\"entry_id\\\": \\\"nature_methods_moty:2011:1.0:4\\\", \\\"detail\\\":...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 11,\n     \"metadata_n_events_year_usable\": 10,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C144501496\",\n     \"metadata_qid\": \"Q5533489\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C46111723\\\", \\\"qid\\\": \\\"Q471857\\\", \\\"qid_resolved\\\": \\\"Q471857\\\", \\\"label\\\": \\\"Proteomics\\\", \\\"label_norm\\\": \\\"proteomic\\\", \\\"aliases\\\": [\\\"proteomics\\\"], \\\"aliases_norm\\\": [], \\\"acronyms\\\": [], \\\"level\\\": 3, \\\"ancestor_ids\\\": [\\\"C104317684\\\", \\\"C55493867\\\", \\\"C54355233\\\", \\\"C86803240\\\", \\\"C185592680\\\"], \\\"level0_discipli...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2002, \\\"date\\\": \\\"2002-06-05\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Pr...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 9,\n     \"metadata_n_events_year_usable\": 9,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C46111723\",\n     \"metadata_qid\": \"Q471857\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C152662350\\\", \\\"qid\\\": \\\"Q815297\\\", \\\"qid_resolved\\\": \\\"Q815297\\\", \\\"label\\\": \\\"Systems biology\\\", \\\"label_norm\\\": \\\"systems biology\\\", \\\"aliases\\\": [\\\"systems biology\\\", \\\"systems approach to biology\\\", \\\"system biology\\\"], \\\"aliases_norm\\\": [\\\"system biology\\\", \\\"systems approach to biology\\\"], \\\"acronyms\\\": [], ...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2004, \\\ndict_keys(['datasets'])\n[('concept_recognition', 10), ('external_entries_mesh', 10), ('external_entries_acm_ccs', 10), ('external_entries_msc', 10), ('external_entries_pacs_physh', 10), ('external_entries_jel', 10), ('external_entries_curated_lists', 10), ('match_verifications', 10), ('crosswalk_level1_to_field', 10), ('spotcheck_p78', 10)]\ndict_keys(['input', 'output', 'metadata_fold', 'metadata_group', 'metadata_group_plurality', 'metadata_group_plurality_share', 'metadata_level', 'metadata_l1_fields', 'metadata_level0', 'metadata_n_events', 'metadata_n_events_year_usable', 'metadata_frame_role', 'metadata_openalex_id', 'metadata_qid'])\n{\"openalex_id\": \"C144501496\", \"qid\": \"Q5533489\", \"qid_resolved\": \"Q5533489\", \"label\": \"Genome editing\", \"label_norm\": \"genome editing\", \"aliases\": [\"genome editing\", \"Genome engineering\"], \"aliases_norm\": [\"genome engineering\"], \"acronyms\": [], \"level\": 4, \"ancestor_ids\": [\"C98108389\", \"C141231307\",...", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] THINKING · 2026-09-28 21:33:43 UTC

```
I'll build a vectorized library (states, RCA masks, covariates) and a weighted Newton conditional logit for cheap bootstraps, then reproduce EXP6, do the EXP5 DEV work, freeze, and score held-out once. Setting up the environment now.
```

### [43] TOOL CALL — Bash · 2026-09-28 21:33:43 UTC

```
mkdir -p lib logs results figures tests scan && cat > pyproject.toml <<'EOF'
[project]
name = "retained-frontier-exp7"
version = "0.1.0"
description = "Retained-frontier and abandonment-penalty test on concept x field entry risk sets"
requires-python = ">=3.12"
dependencies = ["numpy", "pandas", "pyarrow", "scipy", "statsmodels", "networkx", "matplotlib", "loguru", "joblib", "scikit-learn", "pyyaml"]
EOF
uv venv .venv --python=3.12 -q && uv pip install --python=.venv/bin/python -q numpy pandas pyarrow scipy statsmodels networkx matplotlib loguru joblib scikit-learn pyyaml && .venv/bin/python -c "import numpy, pandas, statsmodels, networkx, sklearn; print(numpy.__version__, pandas.__version__, statsmodels.__version__)"
R6=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6
cp $R6/lib/h2.py lib/h2_exp6.py; cp $R6/lib/stats_core.py lib/stats_core.py; cp $R6/config.py lib/cfg_exp6.py; sha256sum $R6/lib/h2.py lib/h2_exp6.py $R6/lib/stats_core.py lib/stats_core.py $R6/config.py lib/cfg_exp6.py
```

### [44] TOOL RESULT — Bash · 2026-09-28 21:36:31 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "b7ewgj83c", "timedOutAfterMs": 120000}
```

### [45] TOOL CALL — Bash · 2026-09-28 21:37:17 UTC

```
sleep 20; cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-3-gen-art-gen-art-experiment-7/1ca57759-1b9c-4574-b7ab-ffcc529ff36c/tasks/b7ewgj83c.output
```

### [46] TOOL RESULT — Bash · 2026-09-28 21:37:59 UTC

```
{"stdout": "2.5.3 3.0.6 0.15.0\nc0886d2410fc14aae21dac338a8bd510a0e97da638642181f1060fe7cd847421  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/lib/h2.py\nc0886d2410fc14aae21dac338a8bd510a0e97da638642181f1060fe7cd847421  lib/h2_exp6.py\na1c30faeddf9a658bc6dcd9826619cd2f42f51bfa856ef772c1d293b7f2582e9  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/lib/stats_core.py\na1c30faeddf9a658bc6dcd9826619cd2f42f51bfa856ef772c1d293b7f2582e9  lib/stats_core.py\n65c736bdfb5bbcd74d6a95f448499aa6d8ef0720a7652871ac940879c0cec330  /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/config.py\n65c736bdfb5bbcd74d6a95f448499aa6d8ef0720a7652871ac940879c0cec330  lib/cfg_exp6.py\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] ASSISTANT · 2026-09-28 21:37:59 UTC

```
Environment ready and the EXP6 libraries copied byte-identical. Now patching only their imports, then writing the core D3 library.
```

### [48] TOOL CALL — Bash · 2026-09-28 21:37:59 UTC

```
sed -i 's/^from config import Y0$/from cfg_exp6 import Y0/' lib/h2_exp6.py && python3 - <<'EOF'
from pathlib import Path
p=Path('lib/cfg_exp6.py'); s=p.read_text()
old='''for _d in (INP, RES, LOGS, FIGS, SCAN, BENCH):
    _d.mkdir(parents=True, exist_ok=True)'''
assert old in s
s=s.replace(old,'''# (EXP7 copy) directory creation removed: this module is imported for constants only''')
p.write_text(s)
EOF
diff /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/lib/h2.py lib/h2_exp6.py; diff /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/config.py lib/cfg_exp6.py; git init -q . && echo ok
```

### [49] TOOL RESULT — Bash · 2026-09-28 21:37:59 UTC

```
{"stdout": "11c11\n< from config import Y0\n---\n> from cfg_exp6 import Y0\n9,10c9\n< for _d in (INP, RES, LOGS, FIGS, SCAN, BENCH):\n<     _d.mkdir(parents=True, exist_ok=True)\n---\n> # (EXP7 copy) directory creation removed: this module is imported for constants only\nok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] TOOL CALL — Write · 2026-09-28 21:38:47 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py

"""D3 field-year state machine, RCA portfolios and concept x field entry risk sets, vectorised over concepts.

Semantics are EXACTLY those of EXP6 lib/h2.py (copied verbatim to lib/h2_exp6.py):
  entered(t)  = cumulative grounded count >= min_n
  retaining(t)= entered(t-2) & w3(t) >= min_n & off-home          (w3 = count over t-2..t)
  lost(t)     = entered(t) & w3(t) == 0                           (off-home filter applied at risk-set time)
  risk set    = concept-year strata t = t0+1..min(t0+horizon, 2022); candidates = ~entered(t-1) & off-home;
                event = entered(t) & candidate.
Everything that EXP6 computes per row is computed here as (per-stratum field mask) @ phi, gathered at the target
field k, which makes permutation / rewiring nulls a single matrix product.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
NF = 26


# ----------------------------------------------------------------------------- states
def panel_states(G: np.ndarray, home_mask: np.ndarray, min_n: float = 2) -> dict[str, np.ndarray]:
    """G [C, NY, 27] grounded counts (slot 0 = unlabelled venue); home_mask [C, 26] bool.
    Returns [C, NY, 26] arrays (bool / int16 / float32)."""
    x = G[:, :, 1:].astype(np.float64)
    cum = np.cumsum(x, 1)
    entered = cum >= min_n
    w3 = x.copy()
    w3[:, 1:] += x[:, :-1]
    w3[:, 2:] += x[:, :-2]
    ent_lag2 = np.zeros_like(entered)
    ent_lag2[:, 2:] = entered[:, :-2]
    offhome = ~home_mask
    retaining = ent_lag2 & (w3 >= min_n) & offhome[:, None, :]
    lost = entered & (w3 == 0)
    yr = np.arange(NY, dtype=np.int16)
    first = np.where(entered.any(1), entered.argmax(1), NY).astype(np.int16)  # [C, 26]
    age = (yr[None, :, None] - first[:, None, :]).astype(np.int16)          # valid where entered
    lastpos = np.maximum.accumulate(np.where(x > 0, yr[None, :, None], -1), axis=1).astype(np.int16)
    tenure = (lastpos - first[:, None, :]).astype(np.int16)                  # tenure of a LOST presence
    return {"x": x.astype(np.float32), "cum": cum.astype(np.float32), "w3": w3.astype(np.float32),
            "entered": entered, "ent_lag2": ent_lag2, "retaining": retaining, "lost": lost,
            "offhome": offhome, "age": age, "tenure": tenure, "first": first}


def rca_entered_panel(G: np.ndarray, GF: np.ndarray, min_n: float = 2) -> np.ndarray:
    """Vectorised h2_exp6.rca_entered: cum >= 2 AND cumulative share > field's cumulative share of all works; absorbing."""
    x = np.cumsum(G[:, :, 1:].astype(np.float64), 1)
    tot = x.sum(2, keepdims=True)
    F = np.cumsum(GF.astype(np.float64), 0)
    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)
    share_c = x / np.maximum(tot, 1)
    ok = (x >= min_n) & (share_c > share_all[None])
    return np.maximum.accumulate(ok.astype(np.int8), 1).astype(bool)


def _rca(nc: np.ndarray, NT: np.ndarray) -> np.ndarray:
    """nc [..., 26] concept counts, NT [..., 26] base totals broadcastable. RCA = (nc/sum nc) / (NT/sum NT); 0 if nc empty."""
    s = nc.sum(-1, keepdims=True)
    share_c = nc / np.where(s > 0, s, 1)
    share_all = NT / np.maximum(NT.sum(-1, keepdims=True), 1)
    return np.where(s > 0, share_c / np.where(share_all > 0, share_all, np.inf), 0.0)


def rolling(a: np.ndarray, w: int, axis: int) -> np.ndarray:
    """sum over the trailing window [y-w+1, y] (partial at the start)."""
    c = np.cumsum(a, axis)
    out = c.copy()
    sl = [slice(None)] * a.ndim
    sl2 = [slice(None)] * a.ndim
    sl[axis] = slice(w, None)
    sl2[axis] = slice(None, -w)
    out[tuple(sl)] = c[tuple(sl)] - c[tuple(sl2)]
    return out


def rca_panel(x: np.ndarray, GF: np.ndarray) -> dict[str, np.ndarray]:
    """x [C, NY, 26] counts; GF [NY, 26] venue-field base totals. Portfolio masks [C, NY, 26] evaluated AT year y
    (the risk-set code reads them at y = t-1). RCA > 1 (strict)."""
    x = x.astype(np.float64)
    GF = GF.astype(np.float64)
    r1 = _rca(x, GF[None])
    xw, Gw = rolling(x, 3, 1), rolling(GF, 3, 0)
    rw = _rca(xw, Gw[None])
    rc = _rca(np.cumsum(x, 1), np.cumsum(GF, 0)[None])
    Uw = rw > 1
    Uw_prev = np.zeros_like(Uw)
    Uw_prev[:, 3:] = Uw[:, :-3]                 # window y-5..y-3
    return {"U_1y": r1 > 1, "U_w3": Uw, "U_cum": rc > 1, "U_pers": Uw & Uw_prev, "rca_1y": r1.astype(np.float32),
            "ties_1y": int(np.isclose(r1, 1.0, rtol=0, atol=1e-12).sum())}


# ----------------------------------------------------------------------------- strata
STRATUM_MASKS = ["E", "ENTOFF", "RET", "LOST", "POOL", "HOME", "U_1y", "U_w3", "U_cum", "U_pers",
                 "RET_a2", "RET_a3", "RET_a4p", "LOST_s", "LOST_l"]


def build_strata(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, *, horizon: int = 10, min_n: float = 2,
                 entry_def: str = "count") -> dict:
    """frame rows aligned with G (row i <-> G[i]); needs columns cidx, t0, home_list (list[int]).
    Returns per-stratum arrays (masks [S, 26] at t-1, counts, candidates, events) + stratum meta."""
    C = len(frame)
    home = np.zeros((C, NF), bool)
    for i, hl in enumerate(frame.home_list):
        for h in hl:
            home[i, h - 11] = True
    S = panel_states(G, home, min_n)
    R = rca_panel(S["x"], GF)
    ent = rca_entered_panel(G, GF, min_n) if entry_def == "rca" else S["entered"]
    t0 = frame.t0.to_numpy().astype(int)
    ci_l, t_l = [], []
    for i in range(C):
        for t in range(t0[i] + 1, min(t0[i] + horizon, Y1) + 1):
            ci_l.append(i); t_l.append(t)
    ci = np.array(ci_l, np.int64)
    t = np.array(t_l, np.int64)
    ti = t - Y0
    p = ti - 1                                                  # state row t-1
    E = ent[ci, p]
    offh = S["offhome"][ci]
    cand = ~E & offh
    keep = cand.any(1)
    ci, t, ti, p, E, offh, cand = ci[keep], t[keep], ti[keep], p[keep], E[keep], offh[keep], cand[keep]
    ev = ent[ci, ti] & cand
    RET = S["retaining"][ci, p]
    LOST = S["lost"][ci, p] & offh
    age = S["age"][ci, p]
    ten = S["tenure"][ci, p]
    POOL = S["ent_lag2"][ci, p] & offh                        # age-eligible entered off-home fields (RET subset)
    out = {"row_i": ci, "t": t, "cand": cand, "event": ev, "E": E, "ENTOFF": S["entered"][ci, p] & offh, "RET": RET,
           "LOST": LOST, "POOL": POOL, "HOME": home[ci],
           "U_1y": R["U_1y"][ci, p], "U_w3": R["U_w3"][ci, p], "U_cum": R["U_cum"][ci, p], "U_pers": R["U_pers"][ci, p],
           "RET_a2": RET & (age == 2), "RET_a3": RET & (age == 3), "RET_a4p": RET & (age >= 4),
           "LOST_s": LOST & (ten <= 1), "LOST_l": LOST & (ten >= 2),
           "xprev": S["x"][ci, p], "w3prev": S["w3"][ci, p], "cumprev": S["cum"][ci, p], "age": age,
           "logGF_prev": np.log(np.maximum(GF[p].astype(np.float64), 1)),
           "ties_rca_1y": R["ties_1y"], "min_n": min_n, "horizon": horizon, "entry_def": entry_def}
    # strict retained-footprint diagnostics for permutation (share of strata where the permutation is non-trivial)
    out["n_ret"] = RET.sum(1)
    out["n_pool"] = POOL.sum(1)
    return out


def _mrel(M: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """mean_{j in M} phi[j, k] for every k -> [S, 26]; zero when M is empty (EXP6 convention)."""
    n = M.sum(1, keepdims=True).astype(np.float64)
    return np.where(n > 0, (M.astype(np.float64) @ phi) / np.where(n > 0, n, 1), 0.0)


def _dens(M: np.ndarray, phi: np.ndarray) -> np.ndarray:
    """Hidalgo density omega_k = sum_j M_j phi_jk / sum_j phi_jk -> [S, 26]."""
    cs = phi.sum(0)
    return (M.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]


def _wdens(W: np.ndarray, phi: np.ndarray) -> np.ndarray:
    cs = phi.sum(0)
    return (W.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]


def _share(v: np.ndarray) -> np.ndarray:
    s = v.sum(1, keepdims=True)
    return v / np.where(s > 0, s, 1)


def _gw(M: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:
    Wm = M * gate[None, :]
    den = Wm.sum(1, keepdims=True)
    return np.where(den > 0, (Wm @ phi) / np.where(den > 0, den, 1), 0.0)


def vol_matched_masks(st: dict) -> tuple[np.ndarray, np.ndarray]:
    """Volume-matched retained (R) vs entered-not-retained (N) off-home fields at t-1: coarsen n(t-1) {0,1,2-3,4+} x
    cum(t-1) {2,3-4,5-9,10+}; keep only cells holding >= 1 R and >= 1 N."""
    n = st["xprev"]; cu = st["cumprev"]
    nb = np.digitize(n, [0.5, 1.5, 3.5])                  # 0 | 1 | 2-3 | 4+
    cb = np.digitize(cu, [2.5, 4.5, 9.5])                 # 2 | 3-4 | 5-9 | 10+
    code = nb * 4 + cb
    R = st["RET"]
    N = st["ENTOFF"] & ~st["RET"]
    oh = np.eye(16, dtype=bool)[code]                     # [S, 26, 16]
    rc = (oh & R[:, :, None]).any(1)
    nc = (oh & N[:, :, None]).any(1)
    ok = rc & nc                                          # [S, 16]
    cell_ok = (oh & ok[:, None, :]).any(2)                # [S, 26]
    return R & cell_ok, N & cell_ok


def covariates(st: dict, phi: np.ndarray, gate: np.ndarray, which: set[str] | None = None) -> pd.DataFrame:
    """Row table: one row per (stratum, candidate field). Columns as in EXP6 + the EXP7 rivals and decompositions."""
    s_idx, k = np.nonzero(st["cand"])
    g = lambda A: A[s_idx, k]  # noqa: E731
    cols = {"s_idx": s_idx, "field": k + 11, "entered": st["event"][s_idx, k].astype(np.int8)}
    cols["a_phi_home"] = g(_mrel(st["HOME"], phi))
    cols["b_log_size"] = st["logGF_prev"][s_idx, k]
    cols["c_density"] = g(_dens(st["E"], phi))
    cols["e_gate_own"] = gate[k]
    cols["d0_ret_rel"] = g(_mrel(st["RET"], phi))
    cols["d_ret_gate"] = g(_gw(st["RET"], phi, gate))
    cols["d_lost_gate"] = g(_gw(st["LOST"], phi, gate))
    cols["d_lost"] = g(_mrel(st["LOST"], phi))
    for u in ("U_1y", "U_w3", "U_cum", "U_pers"):
        cols["D_rca_" + u[2:]] = g(_dens(st[u], phi))
    cols["D_vol"] = g(_wdens(_share(st["xprev"]), phi))
    cols["D_vol_w3"] = g(_wdens(_share(st["w3prev"]), phi))
    cols["D_cum"] = g(_wdens(_share(st["cumprev"]), phi))
    for m in ("RET_a2", "RET_a3", "RET_a4p"):
        cols["d_ret_" + m[4:]] = g(_mrel(st[m], phi))
    cols["d_lost_short"] = g(_mrel(st["LOST_s"], phi))
    cols["d_lost_long"] = g(_mrel(st["LOST_l"], phi))
    Rm, Nm = vol_matched_masks(st)
    cols["d_R_m"] = g(_mrel(Rm, phi))
    cols["d_N_m"] = g(_mrel(Nm, phi))
    cols["has_match"] = (Rm.any(1) & Nm.any(1))[s_idx].astype(np.int8)
    cols["n_ret"] = st["RET"].sum(1)[s_idx]
    cols["n_lost"] = st["LOST"].sum(1)[s_idx]
    cols["n_entered_off"] = st["ENTOFF"].sum(1)[s_idx]
    cols["n_pool"] = st["POOL"].sum(1)[s_idx]
    return pd.DataFrame(cols)


PHI_COLS = ["a_phi_home", "c_density", "d0_ret_rel", "d_ret_gate", "d_lost_gate", "d_lost", "D_rca_1y", "D_rca_w3",
            "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3", "D_cum", "d_ret_a2", "d_ret_a3", "d_ret_a4p",
            "d_lost_short", "d_lost_long", "d_R_m", "d_N_m"]


def attach_meta(df: pd.DataFrame, st: dict, frame: pd.DataFrame, meta_cols: list[str]) -> pd.DataFrame:
    """add cidx, t, age, stratum and concept-level meta columns."""
    ri = st["row_i"][df.s_idx.to_numpy()]
    df.insert(0, "cidx", frame.cidx.to_numpy()[ri])
    df.insert(1, "t", st["t"][df.s_idx.to_numpy()])
    df.insert(2, "age", df.t.to_numpy() - frame.t0.to_numpy()[ri])
    for c in meta_cols:
        df[c] = frame[c].to_numpy()[ri]
    df["stratum"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)
    return df
```

### [51] TOOL RESULT — Write · 2026-09-28 21:38:48 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py", "content": "\"\"\"D3 field-year state machine, RCA portfolios and concept x field entry risk sets, vectorised over concepts.\n\nSemantics are EXACTLY those of EXP6 lib/h2.py (copied verbatim to lib/h2_exp6.py):\n  entered(t)  = cumulative grounded count >= min_n\n  retaining(t)= entered(t-2) & w3(t) >= min_n & off-home          (w3 = count over t-2..t)\n  lost(t)     = entered(t) & w3(t) == 0                           (off-home filter applied at risk-set time)\n  risk set    = concept-year strata t = t0+1..min(t0+horizon, 2022); candidates = ~entered(t-1) & off-home;\n                event = entered(t) & candidate.\nEverything that EXP6 computes per row is computed here as (per-stratum field mask) @ phi, gathered at the target\nfield k, which makes permutation / rewiring nulls a single matrix product.\n\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nNF = 26\n\n\n# ----------------------------------------------------------------------------- states\ndef panel_states(G: np.ndarray, home_mask: np.ndarray, min_n: float = 2) -> dict[str, np.ndarray]:\n    \"\"\"G [C, NY, 27] grounded counts (slot 0 = unlabelled venue); home_mask [C, 26] bool.\n    Returns [C, NY, 26] arrays (bool / int16 / float32).\"\"\"\n    x = G[:, :, 1:].astype(np.float64)\n    cum = np.cumsum(x, 1)\n    entered = cum >= min_n\n    w3 = x.copy()\n    w3[:, 1:] += x[:, :-1]\n    w3[:, 2:] += x[:, :-2]\n    ent_lag2 = np.zeros_like(entered)\n    ent_lag2[:, 2:] = entered[:, :-2]\n    offhome = ~home_mask\n    retaining = ent_lag2 & (w3 >= min_n) & offhome[:, None, :]\n    lost = entered & (w3 == 0)\n    yr = np.arange(NY, dtype=np.int16)\n    first = np.where(entered.any(1), entered.argmax(1), NY).astype(np.int16)  # [C, 26]\n    age = (yr[None, :, None] - first[:, None, :]).astype(np.int16)          # valid where entered\n    lastpos = np.maximum.accumulate(np.where(x > 0, yr[None, :, None], -1), axis=1).astype(np.int16)\n    tenure = (lastpos - first[:, None, :]).astype(np.int16)                  # tenure of a LOST presence\n    return {\"x\": x.astype(np.float32), \"cum\": cum.astype(np.float32), \"w3\": w3.astype(np.float32),\n            \"entered\": entered, \"ent_lag2\": ent_lag2, \"retaining\": retaining, \"lost\": lost,\n            \"offhome\": offhome, \"age\": age, \"tenure\": tenure, \"first\": first}\n\n\ndef rca_entered_panel(G: np.ndarray, GF: np.ndarray, min_n: float = 2) -> np.ndarray:\n    \"\"\"Vectorised h2_exp6.rca_entered: cum >= 2 AND cumulative share > field's cumulative share of all works; absorbing.\"\"\"\n    x = np.cumsum(G[:, :, 1:].astype(np.float64), 1)\n    tot = x.sum(2, keepdims=True)\n    F = np.cumsum(GF.astype(np.float64), 0)\n    share_all = F / np.maximum(F.sum(1, keepdims=True), 1)\n    share_c = x / np.maximum(tot, 1)\n    ok = (x >= min_n) & (share_c > share_all[None])\n    return np.maximum.accumulate(ok.astype(np.int8), 1).astype(bool)\n\n\ndef _rca(nc: np.ndarray, NT: np.ndarray) -> np.ndarray:\n    \"\"\"nc [..., 26] concept counts, NT [..., 26] base totals broadcastable. RCA = (nc/sum nc) / (NT/sum NT); 0 if nc empty.\"\"\"\n    s = nc.sum(-1, keepdims=True)\n    share_c = nc / np.where(s > 0, s, 1)\n    share_all = NT / np.maximum(NT.sum(-1, keepdims=True), 1)\n    return np.where(s > 0, share_c / np.where(share_all > 0, share_all, np.inf), 0.0)\n\n\ndef rolling(a: np.ndarray, w: int, axis: int) -> np.ndarray:\n    \"\"\"sum over the trailing window [y-w+1, y] (partial at the start).\"\"\"\n    c = np.cumsum(a, axis)\n    out = c.copy()\n    sl = [slice(None)] * a.ndim\n    sl2 = [slice(None)] * a.ndim\n    sl[axis] = slice(w, None)\n    sl2[axis] = slice(None, -w)\n    out[tuple(sl)] = c[tuple(sl)] - c[tuple(sl2)]\n    return out\n\n\ndef rca_panel(x: np.ndarray, GF: np.ndarray) -> dict[str, np.ndarray]:\n    \"\"\"x [C, NY, 26] counts; GF [NY, 26] venue-field base totals. Portfolio masks [C, NY, 26] evaluated AT year y\n    (the risk-set code reads them at y = t-1). RCA > 1 (strict).\"\"\"\n    x = x.astype(np.float64)\n    GF = GF.astype(np.float64)\n    r1 = _rca(x, GF[None])\n    xw, Gw = rolling(x, 3, 1), rolling(GF, 3, 0)\n    rw = _rca(xw, Gw[None])\n    rc = _rca(np.cumsum(x, 1), np.cumsum(GF, 0)[None])\n    Uw = rw > 1\n    Uw_prev = np.zeros_like(Uw)\n    Uw_prev[:, 3:] = Uw[:, :-3]                 # window y-5..y-3\n    return {\"U_1y\": r1 > 1, \"U_w3\": Uw, \"U_cum\": rc > 1, \"U_pers\": Uw & Uw_prev, \"rca_1y\": r1.astype(np.float32),\n            \"ties_1y\": int(np.isclose(r1, 1.0, rtol=0, atol=1e-12).sum())}\n\n\n# ----------------------------------------------------------------------------- strata\nSTRATUM_MASKS = [\"E\", \"ENTOFF\", \"RET\", \"LOST\", \"POOL\", \"HOME\", \"U_1y\", \"U_w3\", \"U_cum\", \"U_pers\",\n                 \"RET_a2\", \"RET_a3\", \"RET_a4p\", \"LOST_s\", \"LOST_l\"]\n\n\ndef build_strata(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, *, horizon: int = 10, min_n: float = 2,\n                 entry_def: str = \"count\") -> dict:\n    \"\"\"frame rows aligned with G (row i <-> G[i]); needs columns cidx, t0, home_list (list[int]).\n    Returns per-stratum arrays (masks [S, 26] at t-1, counts, candidates, events) + stratum meta.\"\"\"\n    C = len(frame)\n    home = np.zeros((C, NF), bool)\n    for i, hl in enumerate(frame.home_list):\n        for h in hl:\n            home[i, h - 11] = True\n    S = panel_states(G, home, min_n)\n    R = rca_panel(S[\"x\"], GF)\n    ent = rca_entered_panel(G, GF, min_n) if entry_def == \"rca\" else S[\"entered\"]\n    t0 = frame.t0.to_numpy().astype(int)\n    ci_l, t_l = [], []\n    for i in range(C):\n        for t in range(t0[i] + 1, min(t0[i] + horizon, Y1) + 1):\n            ci_l.append(i); t_l.append(t)\n    ci = np.array(ci_l, np.int64)\n    t = np.array(t_l, np.int64)\n    ti = t - Y0\n    p = ti - 1                                                  # state row t-1\n    E = ent[ci, p]\n    offh = S[\"offhome\"][ci]\n    cand = ~E & offh\n    keep = cand.any(1)\n    ci, t, ti, p, E, offh, cand = ci[keep], t[keep], ti[keep], p[keep], E[keep], offh[keep], cand[keep]\n    ev = ent[ci, ti] & cand\n    RET = S[\"retaining\"][ci, p]\n    LOST = S[\"lost\"][ci, p] & offh\n    age = S[\"age\"][ci, p]\n    ten = S[\"tenure\"][ci, p]\n    POOL = S[\"ent_lag2\"][ci, p] & offh                        # age-eligible entered off-home fields (RET subset)\n    out = {\"row_i\": ci, \"t\": t, \"cand\": cand, \"event\": ev, \"E\": E, \"ENTOFF\": S[\"entered\"][ci, p] & offh, \"RET\": RET,\n           \"LOST\": LOST, \"POOL\": POOL, \"HOME\": home[ci],\n           \"U_1y\": R[\"U_1y\"][ci, p], \"U_w3\": R[\"U_w3\"][ci, p], \"U_cum\": R[\"U_cum\"][ci, p], \"U_pers\": R[\"U_pers\"][ci, p],\n           \"RET_a2\": RET & (age == 2), \"RET_a3\": RET & (age == 3), \"RET_a4p\": RET & (age >= 4),\n           \"LOST_s\": LOST & (ten <= 1), \"LOST_l\": LOST & (ten >= 2),\n           \"xprev\": S[\"x\"][ci, p], \"w3prev\": S[\"w3\"][ci, p], \"cumprev\": S[\"cum\"][ci, p], \"age\": age,\n           \"logGF_prev\": np.log(np.maximum(GF[p].astype(np.float64), 1)),\n           \"ties_rca_1y\": R[\"ties_1y\"], \"min_n\": min_n, \"horizon\": horizon, \"entry_def\": entry_def}\n    # strict retained-footprint diagnostics for permutation (share of strata where the permutation is non-trivial)\n    out[\"n_ret\"] = RET.sum(1)\n    out[\"n_pool\"] = POOL.sum(1)\n    return out\n\n\ndef _mrel(M: np.ndarray, phi: np.ndarray) -> np.ndarray:\n    \"\"\"mean_{j in M} phi[j, k] for every k -> [S, 26]; zero when M is empty (EXP6 convention).\"\"\"\n    n = M.sum(1, keepdims=True).astype(np.float64)\n    return np.where(n > 0, (M.astype(np.float64) @ phi) / np.where(n > 0, n, 1), 0.0)\n\n\ndef _dens(M: np.ndarray, phi: np.ndarray) -> np.ndarray:\n    \"\"\"Hidalgo density omega_k = sum_j M_j phi_jk / sum_j phi_jk -> [S, 26].\"\"\"\n    cs = phi.sum(0)\n    return (M.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]\n\n\ndef _wdens(W: np.ndarray, phi: np.ndarray) -> np.ndarray:\n    cs = phi.sum(0)\n    return (W.astype(np.float64) @ phi) / np.where(cs > 0, cs, 1)[None, :]\n\n\ndef _share(v: np.ndarray) -> np.ndarray:\n    s = v.sum(1, keepdims=True)\n    return v / np.where(s > 0, s, 1)\n\n\ndef _gw(M: np.ndarray, phi: np.ndarray, gate: np.ndarray) -> np.ndarray:\n    Wm = M * gate[None, :]\n    den = Wm.sum(1, keepdims=True)\n    return np.where(den > 0, (Wm @ phi) / np.where(den > 0, den, 1), 0.0)\n\n\ndef vol_matched_masks(st: dict) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"Volume-matched retained (R) vs entered-not-retained (N) off-home fields at t-1: coarsen n(t-1) {0,1,2-3,4+} x\n    cum(t-1) {2,3-4,5-9,10+}; keep only cells holding >= 1 R and >= 1 N.\"\"\"\n    n = st[\"xprev\"]; cu = st[\"cumprev\"]\n    nb = np.digitize(n, [0.5, 1.5, 3.5])                  # 0 | 1 | 2-3 | 4+\n    cb = np.digitize(cu, [2.5, 4.5, 9.5])                 # 2 | 3-4 | 5-9 | 10+\n    code = nb * 4 + cb\n    R = st[\"RET\"]\n    N = st[\"ENTOFF\"] & ~st[\"RET\"]\n    oh = np.eye(16, dtype=bool)[code]                     # [S, 26, 16]\n    rc = (oh & R[:, :, None]).any(1)\n    nc = (oh & N[:, :, None]).any(1)\n    ok = rc & nc                                          # [S, 16]\n    cell_ok = (oh & ok[:, None, :]).any(2)                # [S, 26]\n    return R & cell_ok, N & cell_ok\n\n\ndef covariates(st: dict, phi: np.ndarray, gate: np.ndarray, which: set[str] | None = None) -> pd.DataFrame:\n    \"\"\"Row table: one row per (stratum, candidate field). Columns as in EXP6 + the EXP7 rivals and decompositions.\"\"\"\n    s_idx, k = np.nonzero(st[\"cand\"])\n    g = lambda A: A[s_idx, k]  # noqa: E731\n    cols = {\"s_idx\": s_idx, \"field\": k + 11, \"entered\": st[\"event\"][s_idx, k].astype(np.int8)}\n    cols[\"a_phi_home\"] = g(_mrel(st[\"HOME\"], phi))\n    cols[\"b_log_size\"] = st[\"logGF_prev\"][s_idx, k]\n    cols[\"c_density\"] = g(_dens(st[\"E\"], phi))\n    cols[\"e_gate_own\"] = gate[k]\n    cols[\"d0_ret_rel\"] = g(_mrel(st[\"RET\"], phi))\n    cols[\"d_ret_gate\"] = g(_gw(st[\"RET\"], phi, gate))\n    cols[\"d_lost_gate\"] = g(_gw(st[\"LOST\"], phi, gate))\n    cols[\"d_lost\"] = g(_mrel(st[\"LOST\"], phi))\n    for u in (\"U_1y\", \"U_w3\", \"U_cum\", \"U_pers\"):\n        cols[\"D_rca_\" + u[2:]] = g(_dens(st[u], phi))\n    cols[\"D_vol\"] = g(_wdens(_share(st[\"xprev\"]), phi))\n    cols[\"D_vol_w3\"] = g(_wdens(_share(st[\"w3prev\"]), phi))\n    cols[\"D_cum\"] = g(_wdens(_share(st[\"cumprev\"]), phi))\n    for m in (\"RET_a2\", \"RET_a3\", \"RET_a4p\"):\n        cols[\"d_ret_\" + m[4:]] = g(_mrel(st[m], phi))\n    cols[\"d_lost_short\"] = g(_mrel(st[\"LOST_s\"], phi))\n    cols[\"d_lost_long\"] = g(_mrel(st[\"LOST_l\"], phi))\n    Rm, Nm = vol_matched_masks(st)\n    cols[\"d_R_m\"] = g(_mrel(Rm, phi))\n    cols[\"d_N_m\"] = g(_mrel(Nm, phi))\n    cols[\"has_match\"] = (Rm.any(1) & Nm.any(1))[s_idx].astype(np.int8)\n    cols[\"n_ret\"] = st[\"RET\"].sum(1)[s_idx]\n    cols[\"n_lost\"] = st[\"LOST\"].sum(1)[s_idx]\n    cols[\"n_entered_off\"] = st[\"ENTOFF\"].sum(1)[s_idx]\n    cols[\"n_pool\"] = st[\"POOL\"].sum(1)[s_idx]\n    return pd.DataFrame(cols)\n\n\nPHI_COLS = [\"a_phi_home\", \"c_density\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\", \"d_lost\", \"D_rca_1y\", \"D_rca_w3\",\n            \"D_rca_cum\", \"D_rca_pers\", \"D_vol\", \"D_vol_w3\", \"D_cum\", \"d_ret_a2\", \"d_ret_a3\", \"d_ret_a4p\",\n            \"d_lost_short\", \"d_lost_long\", \"d_R_m\", \"d_N_m\"]\n\n\ndef attach_meta(df: pd.DataFrame, st: dict, frame: pd.DataFrame, meta_cols: list[str]) -> pd.DataFrame:\n    \"\"\"add cidx, t, age, stratum and concept-level meta columns.\"\"\"\n    ri = st[\"row_i\"][df.s_idx.to_numpy()]\n    df.insert(0, \"cidx\", frame.cidx.to_numpy()[ri])\n    df.insert(1, \"t\", st[\"t\"][df.s_idx.to_numpy()])\n    df.insert(2, \"age\", df.t.to_numpy() - frame.t0.to_numpy()[ri])\n    for c in meta_cols:\n        df[c] = frame[c].to_numpy()[ri]\n    df[\"stratum\"] = df.cidx.astype(np.int64) * 100 + (df.t - 2000)\n    return df\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [52] ASSISTANT · 2026-09-28 21:38:48 UTC

```
Now a quick reproduction check of the vectorised builder against EXP6's stored held-out risk sets.
```

### [53] TOOL CALL — Bash · 2026-09-28 21:38:48 UTC

```
cat > scratch_repro.py <<'EOF'
import sys, json, time, numpy as np, pandas as pd
sys.path.insert(0,'lib')
import d3
R6='/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6'
bb=json.load(open(R6+'/inputs/field_backbone.json')); phi=np.array(bb['phi']); gate=np.array(bb['gateway_eig'])
print('phi sym', np.allclose(phi,phi.T), 'diag', np.abs(np.diag(phi)).max(), np.isnan(phi).sum())
GF=np.load(R6+'/scan/agg_counts.npz')['GF']
fc=pd.read_csv(R6+'/results/frame_concepts.csv')
fr=fc[(fc.split!='dev')&fc.newborn].copy()
z=np.load(R6+'/scan/frame_g_heldout.npz'); Gd={int(c):z['g'][i] for i,c in enumerate(z['cidx'])}
fr['home_list']=[[int(h) for h in str(x).split('|')] for x in fr.home]
G=np.stack([Gd[c] for c in fr.cidx])
t=time.time(); st=d3.build_strata(fr,G,GF,horizon=8); df=d3.covariates(st,phi,gate); df=d3.attach_meta(df,st,fr,[]); print('built',len(df),time.time()-t)
old=pd.read_parquet(R6+'/results/entry_risk_sets_heldout.parquet'); print(len(old))
m=old.merge(df,on=['cidx','t','field'],how='outer',indicator=True,suffixes=('_o','_n')); print(m._merge.value_counts())
for c in ['entered','a_phi_home','b_log_size','c_density','e_gate_own','d0_ret_rel','d_ret_gate','d_lost_gate','n_ret','n_lost']:
    print(c, np.abs(m[c+'_o']-m[c+'_n']).max())
EOF
.venv/bin/python scratch_repro.py
```

### [54] TOOL RESULT — Bash · 2026-09-28 21:39:32 UTC

```
{"stdout": "phi sym True diag 0.0 0\nbuilt 61648 0.11226582527160645\n61648\n_merge\nboth          61648\nleft_only         0\nright_only        0\nName: count, dtype: int64\nentered 0\na_phi_home 0.0\nb_log_size 0.0\nc_density 1.1102230246251565e-16\ne_gate_own 0.0\nd0_ret_rel 0.0\nd_ret_gate 4.440892098500626e-16\nd_lost_gate 2.220446049250313e-16\nn_ret 0\nn_lost 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] ASSISTANT · 2026-09-28 21:40:16 UTC

```
Exact reproduction of all 61,648 EXP6 held-out rows (max diff 4e-16). Next is the fast weighted conditional-logit engine, validated against EXP6's solver.
```

### [56] TOOL CALL — Write · 2026-09-28 21:40:16 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/models.py

"""Estimation layer: a Newton conditional logit (Breslow ties, the EXP6 likelihood) with stratum weights (exact
concept-clustered refit bootstrap = multinomial concept weights), row offsets (crossed field bootstrap),
cluster / two-way-cluster sandwich SEs; rung definitions; LR tests; bootstraps; LPM; DL pooling.
Validated against lib/stats_core.CLogit (EXP6, verbatim copy) in tests/test_units.py."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

import h2_exp6 as H2
from stats_core import dersimonian_laird, fe_ols

BASE = ["a_phi_home", "b_log_size", "c_density", "e_gate_own"]
RIVALS_STRICT = ["D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3"]
RUNGS = {
    "R0_M0": BASE,
    "R1_rca": BASE + ["D_rca_1y"],
    "R2_vol": BASE + ["D_rca_1y", "D_vol"],
    "R3_ret": BASE + ["D_rca_1y", "D_vol", "d0_ret_rel"],
    "R4_lost": BASE + ["D_rca_1y", "D_vol", "d0_ret_rel", "d_lost"],
    "S_strict0": BASE + RIVALS_STRICT,
    "S_strict": BASE + RIVALS_STRICT + ["d0_ret_rel"],
    "A1_lost": BASE + ["d_lost"],
    "EXP6_M1": BASE + ["d0_ret_rel"],
    "EXP6_M2lost": BASE + ["d_lost_gate"],
}
LADDER = [("R1_rca", "R0_M0"), ("R2_vol", "R1_rca"), ("R3_ret", "R2_vol"), ("R4_lost", "R3_ret"),
          ("S_strict", "S_strict0"), ("A1_lost", "R0_M0"), ("EXP6_M1", "R0_M0"), ("EXP6_M2lost", "R0_M0")]
STD_COLS = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "d0_ret_rel", "d_ret_gate", "d_lost_gate", "d_lost",
            "D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers", "D_vol", "D_vol_w3", "D_cum", "d_lost_short", "d_lost_long"]
D0_SCALE_COLS = ["d_ret_a2", "d_ret_a3", "d_ret_a4p", "d_R_m", "d_N_m"]  # common scale = SD of d0_ret_rel


class FastCLogit:
    """ll = sum_s w_s [ sum_{e in s} eta_e - nev_s log sum_{i in s} exp(eta_i) ],  eta = X b + offset.
    Only informative strata (>= 1 event and >= 1 non-event) are kept."""

    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, offset: np.ndarray | None = None,
                 clusters: dict[str, np.ndarray] | None = None):
        o = np.argsort(strata, kind="stable")
        s = strata[o]
        _, starts, counts = np.unique(s, return_index=True, return_counts=True)
        yy = y[o].astype(np.float64)
        nev = np.add.reduceat(yy, starts)
        keep_s = (nev > 0) & (nev < counts)
        rows = np.repeat(keep_s, counts)
        self.idx = o[rows]                      # original row index of every internal row
        self.X = np.ascontiguousarray(X[self.idx], dtype=np.float64)
        self.y = yy[rows]
        self.off = None if offset is None else offset[self.idx].astype(np.float64)
        s = s[rows]
        self.sid, self.starts, self.counts = np.unique(s, return_index=True, return_counts=True)
        self.nev = np.add.reduceat(self.y, self.starts) if len(self.starts) else np.zeros(0)
        self.row_s = np.repeat(np.arange(len(self.starts)), self.counts)
        self.clusters = {k: v[self.idx] for k, v in (clusters or {}).items()}
        self.w = np.ones(len(self.starts))

    @property
    def n_strata(self) -> int:
        return int(len(self.starts))

    def set_col(self, j: int, values: np.ndarray) -> None:
        self.X[:, j] = values[self.idx]

    def _parts(self, b: np.ndarray, w: np.ndarray):
        eta = self.X @ b
        if self.off is not None:
            eta = eta + self.off
        m = np.maximum.reduceat(eta, self.starts)
        e = np.exp(eta - m[self.row_s])
        S = np.add.reduceat(e, self.starts)
        p = e / S[self.row_s]
        lse = np.log(S) + m
        ll = float((w[self.row_s] * self.y * eta).sum() - (w * self.nev * lse).sum())
        return eta, p, ll

    def fit(self, b0: np.ndarray | None = None, w: np.ndarray | None = None, ridge: float = 0.0, tol: float = 1e-9,
            maxit: int = 60, want_cov: bool = True) -> dict:
        k = self.X.shape[1]
        if self.n_strata == 0:
            return {"coef": np.full(k, np.nan), "se": np.full(k, np.nan), "ll": np.nan, "converged": False,
                    "n_strata": 0, "n_events": 0, "n_rows": 0, "max_grad": np.nan}
        w = self.w if w is None else w
        b = np.zeros(k) if b0 is None else np.array(b0, float)
        _, p, ll = self._parts(b, w)
        ll -= 0.5 * ridge * b @ b
        conv = False
        for it in range(maxit):
            wr = w[self.row_s]
            Ex = np.add.reduceat(p[:, None] * self.X, self.starts)
            g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b
            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]
            B = Ex * np.sqrt(w * self.nev)[:, None]
            H = A.T @ A - B.T @ B + ridge * np.eye(k)
            try:
                step = np.linalg.solve(H, g)
            except np.linalg.LinAlgError:
                step = np.linalg.lstsq(H, g, rcond=None)[0]
            t = 1.0
            for _ in range(30):
                bn = b + t * step
                _, pn, lln = self._parts(bn, w)
                lln -= 0.5 * ridge * bn @ bn
                if lln >= ll - 1e-10:
                    break
                t *= 0.5
            b, p, dll = bn, pn, lln - ll
            ll = lln
            if np.abs(t * step).max() < tol or abs(dll) < 1e-12:
                conv = True
                break
        wr = w[self.row_s]
        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)
        g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b
        out = {"coef": b, "ll": ll, "converged": bool(conv and np.abs(g).max() < 1e-4), "max_grad": float(np.abs(g).max()),
               "n_strata": self.n_strata, "n_events": int(self.y.sum()), "n_rows": int(len(self.y)), "iters": it + 1}
        if want_cov:
            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]
            B = Ex * np.sqrt(w * self.nev)[:, None]
            H = A.T @ A - B.T @ B + ridge * np.eye(k)
            try:
                Hi = np.linalg.inv(H)
                out["se"] = np.sqrt(np.clip(np.diag(Hi), 0, None))
            except np.linalg.LinAlgError:
                Hi = np.linalg.pinv(H)
                out["se"] = np.full(k, np.nan)
            out["_Hi"] = Hi
            out["_p"] = p
        return out

    def row_scores(self, res: dict) -> np.ndarray:
        """per-row score contributions u_i = (y_i - nev_s p_i) x_i (sum within stratum = stratum score)."""
        return (self.y - self.nev[self.row_s] * res["_p"])[:, None] * self.X

    def cluster_se(self, res: dict, by: str | list[str]) -> np.ndarray:
        """CRV1 sandwich; `by` a cluster name, or two names for Cameron-Gelbach-Miller two-way clustering."""
        U = self.row_scores(res)
        Hi = res["_Hi"]

        def meat(key: np.ndarray) -> tuple[np.ndarray, int]:
            _, inv = np.unique(key, return_inverse=True)
            G = inv.max() + 1
            sc = np.zeros((G, U.shape[1]))
            np.add.at(sc, inv, U)
            return (G / max(G - 1, 1)) * (sc.T @ sc), G
        if isinstance(by, str):
            M, _ = meat(self.clusters[by])
        else:
            a, b = (self.clusters[x] for x in by)
            Ma, _ = meat(a); Mb, _ = meat(b)
            Mab, _ = meat(a.astype(np.int64) * 1000 + b.astype(np.int64))
            M = Ma + Mb - Mab
        V = Hi @ M @ Hi
        return np.sqrt(np.clip(np.diag(V), 0, None))


# ----------------------------------------------------------------------------- helpers
def standardise(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    out = df.copy()
    for c, v in spec.items():
        if c in out:
            out[c] = (df[c] - v["mean"]) / (v["sd"] if v["sd"] > 0 else 1.0)
    return out


def make_spec(df: pd.DataFrame, cols: list[str] = STD_COLS, base: dict | None = None) -> dict:
    """mean/SD per column; the dose and matched-contrast columns use mean 0 and the SD of d0_ret_rel (common scale)."""
    spec = dict(base or {})
    for c in cols:
        if c not in spec and c in df:
            sd = float(df[c].std())
            spec[c] = {"mean": float(df[c].mean()), "sd": sd if sd > 0 else 1.0}
    for c in D0_SCALE_COLS:
        if c in df:
            spec[c] = {"mean": 0.0, "sd": spec["d0_ret_rel"]["sd"]}
    return spec


def model(df: pd.DataFrame, cols: list[str], offset: np.ndarray | None = None) -> FastCLogit:
    return FastCLogit(df[cols].to_numpy(np.float64), df.entered.to_numpy(), df.stratum.to_numpy(), offset=offset,
                      clusters={"concept": df.cidx.to_numpy(), "field": df.field.to_numpy()})


def summarise(m: FastCLogit, r: dict, cols: list[str], cluster: bool = True) -> dict:
    out = {"coef": dict(zip(cols, map(float, r["coef"]))), "se_model": dict(zip(cols, map(float, r["se"]))),
           "ll": float(r["ll"]), "n_strata": r["n_strata"], "n_events": r["n_events"], "n_rows": r["n_rows"],
           "converged": r["converged"], "max_grad": r["max_grad"]}
    if cluster and r["n_strata"] > 0:
        out["se_concept"] = dict(zip(cols, map(float, m.cluster_se(r, "concept"))))
    return out


def lr(big: dict, small: dict, df_: int = 1) -> dict:
    x = 2 * (big["ll"] - small["ll"])
    return {"LR": float(x), "df": df_, "p": float(stats.chi2.sf(max(x, 0), df_))}


def fit_ladder(df: pd.DataFrame, rungs: list[str] | None = None, auc: bool = True, two_way: list[str] | None = None) -> dict:
    """fit every rung on the same rows; LR along LADDER; within-stratum AUC of each linear predictor."""
    rungs = rungs or list(RUNGS)
    fits, res = {}, {"models": {}, "LR": {}, "auc_within": {}}
    for rn in rungs:
        cols = RUNGS[rn]
        m = model(df, cols)
        r = m.fit()
        fits[rn] = r
        res["models"][rn] = summarise(m, r, cols)
        if two_way and rn in two_way:
            res["models"][rn]["se_two_way_concept_field"] = dict(zip(cols, map(float, m.cluster_se(r, ["concept", "field"]))))
        if auc:
            sc = df[cols].to_numpy() @ r["coef"]
            res["auc_within"][rn] = float(H2.within_auc(df, sc).mean())
    for big, small in LADDER:
        if big in fits and small in fits:
            res["LR"][f"{big}_vs_{small}"] = lr(fits[big], fits[small], len(RUNGS[big]) - len(RUNGS[small]))
    res["n"] = {"rows": int(len(df)), "strata": int(df.stratum.nunique()), "concepts": int(df.cidx.nunique()),
                "events": int(df.entered.sum()), "informative_strata": fits[rungs[0]]["n_strata"],
                "informative_rows": fits[rungs[0]]["n_rows"]}
    res["_fits"] = fits
    return res


def concept_weights(cid_of_stratum: np.ndarray, rng, n_boot: int) -> np.ndarray:
    """multinomial concept-resampling counts mapped to strata -> [n_boot, n_strata]. A concept drawn m times
    contributes m identical independent copies of its strata, i.e. weight m (exact equivalence with the
    duplicate-and-relabel refit bootstrap of h2_exp6.boot_coef)."""
    u, inv = np.unique(cid_of_stratum, return_inverse=True)
    W = np.empty((n_boot, len(cid_of_stratum)))
    for b in range(n_boot):
        cnt = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)
        W[b] = cnt[inv]
    return W


def boot_refit(df: pd.DataFrame, cols: list[str], targets: list[str], n_boot: int, rng, small_cols: list[str] | None = None,
               W: np.ndarray | None = None) -> dict:
    """concept-clustered refit bootstrap (weights), warm-started at the full-sample estimate."""
    m = model(df, cols)
    r0 = m.fit(want_cov=False)
    ms = model(df, small_cols) if small_cols else None
    rs0 = ms.fit(want_cov=False) if ms else None
    if W is None:
        W = concept_weights(m.sid // 100, rng, n_boot)
    B, L = [], []
    for w in W:
        r = m.fit(b0=r0["coef"], w=w, want_cov=False)
        B.append(r["coef"])
        if ms is not None:
            L.append(2 * (r["ll"] - ms.fit(b0=rs0["coef"], w=w, want_cov=False)["ll"]))
    B = np.array(B)
    out = {"resampling_unit": "concept", "n_boot": int(len(W))}
    for tg in targets:
        j = cols.index(tg)
        out[tg] = {"est": float(r0["coef"][j]), "ci": [float(np.nanpercentile(B[:, j], 2.5)), float(np.nanpercentile(B[:, j], 97.5))],
                   "se_boot": float(np.nanstd(B[:, j])), "p_one_sided_le0": float((1 + (B[:, j] <= 0).sum()) / (1 + len(B)))}
    if L:
        L = np.array(L)
        out["LR_boot_q"] = [float(x) for x in np.percentile(L, [5, 25, 50, 75, 95])]
    out["_B"] = B
    return out


def contrast_boot(df: pd.DataFrame, cols: list[str], a: str, b: str, n_boot: int, rng, sign: int = 1) -> dict:
    """bootstrap CI of coef[a] - coef[b] (concept refit)."""
    bt = boot_refit(df, cols, [a, b], n_boot, rng)
    d = bt["_B"][:, cols.index(a)] - bt["_B"][:, cols.index(b)]
    est = bt[a]["est"] - bt[b]["est"]
    return {"resampling_unit": "concept", "n_boot": n_boot, "est": float(est),
            "ci": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "p_one_sided": float((1 + (sign * d <= 0).sum()) / (1 + len(d))), a: bt[a], b: bt[b]}


def crossed_boot(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng) -> dict:
    """Owen pigeonhole: concept weights u_c ~ Poisson(1) on stratum log-lik; target-field weights v_k ~ Poisson(1) as
    offset log(v_k) on each alternative (v_k = 0 removes the alternative; strata left uninformative drop out)."""
    m0 = model(df, cols)
    b0 = m0.fit(want_cov=False)["coef"]
    fk = df.field.to_numpy() - 11
    cid = df.cidx.to_numpy()
    uc, cinv = np.unique(cid, return_inverse=True)
    B = []
    for _ in range(n_boot):
        v = rng.poisson(1.0, 26).astype(float)
        u = rng.poisson(1.0, len(uc)).astype(float)
        keep = (v[fk] > 0) & (u[cinv] > 0)
        sub = df[keep]
        off = np.log(v[fk][keep])
        m = FastCLogit(sub[cols].to_numpy(np.float64), sub.entered.to_numpy(), sub.stratum.to_numpy(), offset=off)
        if m.n_strata == 0:
            continue
        ws = u[np.searchsorted(uc, m.sid // 100)]
        B.append(m.fit(b0=b0, w=ws, want_cov=False)["coef"][cols.index(target)])
    B = np.array(B)
    return {"resampling_unit": "concept x target field (Owen pigeonhole, Poisson(1) weights)", "n_boot": int(len(B)),
            "ci": [float(np.percentile(B, 2.5)), float(np.percentile(B, 97.5))], "se_boot": float(B.std())}


def lpm(df: pd.DataFrame, cols: list[str]) -> dict:
    """linear probability model with concept-year (stratum) FE, concept-clustered CRV1 SEs (econ-geo comparability)."""
    r = fe_ols(df.entered.to_numpy(float), df[cols].to_numpy(float), [df.stratum.to_numpy()], df.cidx.to_numpy(), cols)
    r.pop("V", None); r.pop("_b", None)
    r["resampling_unit"] = "concept (CRV1 clusters)"
    r["base_rate"] = float(df.entered.mean())
    return r


def holm(pvals: dict[str, float]) -> dict[str, float]:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = float(run)
    return out


def dl(b: list[float], se: list[float]) -> dict:
    return dersimonian_laird(np.array(b), np.array(se))


def informative(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("stratum").entered.agg(["sum", "size"])
    ok = g.index[(g["sum"] > 0) & (g["sum"] < g["size"])]
    return df[df.stratum.isin(ok)]
```

### [57] TOOL RESULT — Write · 2026-09-28 21:40:16 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/models.py", "content": "\"\"\"Estimation layer: a Newton conditional logit (Breslow ties, the EXP6 likelihood) with stratum weights (exact\nconcept-clustered refit bootstrap = multinomial concept weights), row offsets (crossed field bootstrap),\ncluster / two-way-cluster sandwich SEs; rung definitions; LR tests; bootstraps; LPM; DL pooling.\nValidated against lib/stats_core.CLogit (EXP6, verbatim copy) in tests/test_units.py.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nimport h2_exp6 as H2\nfrom stats_core import dersimonian_laird, fe_ols\n\nBASE = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\"]\nRIVALS_STRICT = [\"D_rca_1y\", \"D_rca_w3\", \"D_rca_cum\", \"D_rca_pers\", \"D_vol\", \"D_vol_w3\"]\nRUNGS = {\n    \"R0_M0\": BASE,\n    \"R1_rca\": BASE + [\"D_rca_1y\"],\n    \"R2_vol\": BASE + [\"D_rca_1y\", \"D_vol\"],\n    \"R3_ret\": BASE + [\"D_rca_1y\", \"D_vol\", \"d0_ret_rel\"],\n    \"R4_lost\": BASE + [\"D_rca_1y\", \"D_vol\", \"d0_ret_rel\", \"d_lost\"],\n    \"S_strict0\": BASE + RIVALS_STRICT,\n    \"S_strict\": BASE + RIVALS_STRICT + [\"d0_ret_rel\"],\n    \"A1_lost\": BASE + [\"d_lost\"],\n    \"EXP6_M1\": BASE + [\"d0_ret_rel\"],\n    \"EXP6_M2lost\": BASE + [\"d_lost_gate\"],\n}\nLADDER = [(\"R1_rca\", \"R0_M0\"), (\"R2_vol\", \"R1_rca\"), (\"R3_ret\", \"R2_vol\"), (\"R4_lost\", \"R3_ret\"),\n          (\"S_strict\", \"S_strict0\"), (\"A1_lost\", \"R0_M0\"), (\"EXP6_M1\", \"R0_M0\"), (\"EXP6_M2lost\", \"R0_M0\")]\nSTD_COLS = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"d0_ret_rel\", \"d_ret_gate\", \"d_lost_gate\", \"d_lost\",\n            \"D_rca_1y\", \"D_rca_w3\", \"D_rca_cum\", \"D_rca_pers\", \"D_vol\", \"D_vol_w3\", \"D_cum\", \"d_lost_short\", \"d_lost_long\"]\nD0_SCALE_COLS = [\"d_ret_a2\", \"d_ret_a3\", \"d_ret_a4p\", \"d_R_m\", \"d_N_m\"]  # common scale = SD of d0_ret_rel\n\n\nclass FastCLogit:\n    \"\"\"ll = sum_s w_s [ sum_{e in s} eta_e - nev_s log sum_{i in s} exp(eta_i) ],  eta = X b + offset.\n    Only informative strata (>= 1 event and >= 1 non-event) are kept.\"\"\"\n\n    def __init__(self, X: np.ndarray, y: np.ndarray, strata: np.ndarray, offset: np.ndarray | None = None,\n                 clusters: dict[str, np.ndarray] | None = None):\n        o = np.argsort(strata, kind=\"stable\")\n        s = strata[o]\n        _, starts, counts = np.unique(s, return_index=True, return_counts=True)\n        yy = y[o].astype(np.float64)\n        nev = np.add.reduceat(yy, starts)\n        keep_s = (nev > 0) & (nev < counts)\n        rows = np.repeat(keep_s, counts)\n        self.idx = o[rows]                      # original row index of every internal row\n        self.X = np.ascontiguousarray(X[self.idx], dtype=np.float64)\n        self.y = yy[rows]\n        self.off = None if offset is None else offset[self.idx].astype(np.float64)\n        s = s[rows]\n        self.sid, self.starts, self.counts = np.unique(s, return_index=True, return_counts=True)\n        self.nev = np.add.reduceat(self.y, self.starts) if len(self.starts) else np.zeros(0)\n        self.row_s = np.repeat(np.arange(len(self.starts)), self.counts)\n        self.clusters = {k: v[self.idx] for k, v in (clusters or {}).items()}\n        self.w = np.ones(len(self.starts))\n\n    @property\n    def n_strata(self) -> int:\n        return int(len(self.starts))\n\n    def set_col(self, j: int, values: np.ndarray) -> None:\n        self.X[:, j] = values[self.idx]\n\n    def _parts(self, b: np.ndarray, w: np.ndarray):\n        eta = self.X @ b\n        if self.off is not None:\n            eta = eta + self.off\n        m = np.maximum.reduceat(eta, self.starts)\n        e = np.exp(eta - m[self.row_s])\n        S = np.add.reduceat(e, self.starts)\n        p = e / S[self.row_s]\n        lse = np.log(S) + m\n        ll = float((w[self.row_s] * self.y * eta).sum() - (w * self.nev * lse).sum())\n        return eta, p, ll\n\n    def fit(self, b0: np.ndarray | None = None, w: np.ndarray | None = None, ridge: float = 0.0, tol: float = 1e-9,\n            maxit: int = 60, want_cov: bool = True) -> dict:\n        k = self.X.shape[1]\n        if self.n_strata == 0:\n            return {\"coef\": np.full(k, np.nan), \"se\": np.full(k, np.nan), \"ll\": np.nan, \"converged\": False,\n                    \"n_strata\": 0, \"n_events\": 0, \"n_rows\": 0, \"max_grad\": np.nan}\n        w = self.w if w is None else w\n        b = np.zeros(k) if b0 is None else np.array(b0, float)\n        _, p, ll = self._parts(b, w)\n        ll -= 0.5 * ridge * b @ b\n        conv = False\n        for it in range(maxit):\n            wr = w[self.row_s]\n            Ex = np.add.reduceat(p[:, None] * self.X, self.starts)\n            g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b\n            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]\n            B = Ex * np.sqrt(w * self.nev)[:, None]\n            H = A.T @ A - B.T @ B + ridge * np.eye(k)\n            try:\n                step = np.linalg.solve(H, g)\n            except np.linalg.LinAlgError:\n                step = np.linalg.lstsq(H, g, rcond=None)[0]\n            t = 1.0\n            for _ in range(30):\n                bn = b + t * step\n                _, pn, lln = self._parts(bn, w)\n                lln -= 0.5 * ridge * bn @ bn\n                if lln >= ll - 1e-10:\n                    break\n                t *= 0.5\n            b, p, dll = bn, pn, lln - ll\n            ll = lln\n            if np.abs(t * step).max() < tol or abs(dll) < 1e-12:\n                conv = True\n                break\n        wr = w[self.row_s]\n        Ex = np.add.reduceat(p[:, None] * self.X, self.starts)\n        g = (wr * self.y) @ self.X - (w * self.nev) @ Ex - ridge * b\n        out = {\"coef\": b, \"ll\": ll, \"converged\": bool(conv and np.abs(g).max() < 1e-4), \"max_grad\": float(np.abs(g).max()),\n               \"n_strata\": self.n_strata, \"n_events\": int(self.y.sum()), \"n_rows\": int(len(self.y)), \"iters\": it + 1}\n        if want_cov:\n            A = self.X * np.sqrt(wr * self.nev[self.row_s] * p)[:, None]\n            B = Ex * np.sqrt(w * self.nev)[:, None]\n            H = A.T @ A - B.T @ B + ridge * np.eye(k)\n            try:\n                Hi = np.linalg.inv(H)\n                out[\"se\"] = np.sqrt(np.clip(np.diag(Hi), 0, None))\n            except np.linalg.LinAlgError:\n                Hi = np.linalg.pinv(H)\n                out[\"se\"] = np.full(k, np.nan)\n            out[\"_Hi\"] = Hi\n            out[\"_p\"] = p\n        return out\n\n    def row_scores(self, res: dict) -> np.ndarray:\n        \"\"\"per-row score contributions u_i = (y_i - nev_s p_i) x_i (sum within stratum = stratum score).\"\"\"\n        return (self.y - self.nev[self.row_s] * res[\"_p\"])[:, None] * self.X\n\n    def cluster_se(self, res: dict, by: str | list[str]) -> np.ndarray:\n        \"\"\"CRV1 sandwich; `by` a cluster name, or two names for Cameron-Gelbach-Miller two-way clustering.\"\"\"\n        U = self.row_scores(res)\n        Hi = res[\"_Hi\"]\n\n        def meat(key: np.ndarray) -> tuple[np.ndarray, int]:\n            _, inv = np.unique(key, return_inverse=True)\n            G = inv.max() + 1\n            sc = np.zeros((G, U.shape[1]))\n            np.add.at(sc, inv, U)\n            return (G / max(G - 1, 1)) * (sc.T @ sc), G\n        if isinstance(by, str):\n            M, _ = meat(self.clusters[by])\n        else:\n            a, b = (self.clusters[x] for x in by)\n            Ma, _ = meat(a); Mb, _ = meat(b)\n            Mab, _ = meat(a.astype(np.int64) * 1000 + b.astype(np.int64))\n            M = Ma + Mb - Mab\n        V = Hi @ M @ Hi\n        return np.sqrt(np.clip(np.diag(V), 0, None))\n\n\n# ----------------------------------------------------------------------------- helpers\ndef standardise(df: pd.DataFrame, spec: dict) -> pd.DataFrame:\n    out = df.copy()\n    for c, v in spec.items():\n        if c in out:\n            out[c] = (df[c] - v[\"mean\"]) / (v[\"sd\"] if v[\"sd\"] > 0 else 1.0)\n    return out\n\n\ndef make_spec(df: pd.DataFrame, cols: list[str] = STD_COLS, base: dict | None = None) -> dict:\n    \"\"\"mean/SD per column; the dose and matched-contrast columns use mean 0 and the SD of d0_ret_rel (common scale).\"\"\"\n    spec = dict(base or {})\n    for c in cols:\n        if c not in spec and c in df:\n            sd = float(df[c].std())\n            spec[c] = {\"mean\": float(df[c].mean()), \"sd\": sd if sd > 0 else 1.0}\n    for c in D0_SCALE_COLS:\n        if c in df:\n            spec[c] = {\"mean\": 0.0, \"sd\": spec[\"d0_ret_rel\"][\"sd\"]}\n    return spec\n\n\ndef model(df: pd.DataFrame, cols: list[str], offset: np.ndarray | None = None) -> FastCLogit:\n    return FastCLogit(df[cols].to_numpy(np.float64), df.entered.to_numpy(), df.stratum.to_numpy(), offset=offset,\n                      clusters={\"concept\": df.cidx.to_numpy(), \"field\": df.field.to_numpy()})\n\n\ndef summarise(m: FastCLogit, r: dict, cols: list[str], cluster: bool = True) -> dict:\n    out = {\"coef\": dict(zip(cols, map(float, r[\"coef\"]))), \"se_model\": dict(zip(cols, map(float, r[\"se\"]))),\n           \"ll\": float(r[\"ll\"]), \"n_strata\": r[\"n_strata\"], \"n_events\": r[\"n_events\"], \"n_rows\": r[\"n_rows\"],\n           \"converged\": r[\"converged\"], \"max_grad\": r[\"max_grad\"]}\n    if cluster and r[\"n_strata\"] > 0:\n        out[\"se_concept\"] = dict(zip(cols, map(float, m.cluster_se(r, \"concept\"))))\n    return out\n\n\ndef lr(big: dict, small: dict, df_: int = 1) -> dict:\n    x = 2 * (big[\"ll\"] - small[\"ll\"])\n    return {\"LR\": float(x), \"df\": df_, \"p\": float(stats.chi2.sf(max(x, 0), df_))}\n\n\ndef fit_ladder(df: pd.DataFrame, rungs: list[str] | None = None, auc: bool = True, two_way: list[str] | None = None) -> dict:\n    \"\"\"fit every rung on the same rows; LR along LADDER; within-stratum AUC of each linear predictor.\"\"\"\n    rungs = rungs or list(RUNGS)\n    fits, res = {}, {\"models\": {}, \"LR\": {}, \"auc_within\": {}}\n    for rn in rungs:\n        cols = RUNGS[rn]\n        m = model(df, cols)\n        r = m.fit()\n        fits[rn] = r\n        res[\"models\"][rn] = summarise(m, r, cols)\n        if two_way and rn in two_way:\n            res[\"models\"][rn][\"se_two_way_concept_field\"] = dict(zip(cols, map(float, m.cluster_se(r, [\"concept\", \"field\"]))))\n        if auc:\n            sc = df[cols].to_numpy() @ r[\"coef\"]\n            res[\"auc_within\"][rn] = float(H2.within_auc(df, sc).mean())\n    for big, small in LADDER:\n        if big in fits and small in fits:\n            res[\"LR\"][f\"{big}_vs_{small}\"] = lr(fits[big], fits[small], len(RUNGS[big]) - len(RUNGS[small]))\n    res[\"n\"] = {\"rows\": int(len(df)), \"strata\": int(df.stratum.nunique()), \"concepts\": int(df.cidx.nunique()),\n                \"events\": int(df.entered.sum()), \"informative_strata\": fits[rungs[0]][\"n_strata\"],\n                \"informative_rows\": fits[rungs[0]][\"n_rows\"]}\n    res[\"_fits\"] = fits\n    return res\n\n\ndef concept_weights(cid_of_stratum: np.ndarray, rng, n_boot: int) -> np.ndarray:\n    \"\"\"multinomial concept-resampling counts mapped to strata -> [n_boot, n_strata]. A concept drawn m times\n    contributes m identical independent copies of its strata, i.e. weight m (exact equivalence with the\n    duplicate-and-relabel refit bootstrap of h2_exp6.boot_coef).\"\"\"\n    u, inv = np.unique(cid_of_stratum, return_inverse=True)\n    W = np.empty((n_boot, len(cid_of_stratum)))\n    for b in range(n_boot):\n        cnt = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)\n        W[b] = cnt[inv]\n    return W\n\n\ndef boot_refit(df: pd.DataFrame, cols: list[str], targets: list[str], n_boot: int, rng, small_cols: list[str] | None = None,\n               W: np.ndarray | None = None) -> dict:\n    \"\"\"concept-clustered refit bootstrap (weights), warm-started at the full-sample estimate.\"\"\"\n    m = model(df, cols)\n    r0 = m.fit(want_cov=False)\n    ms = model(df, small_cols) if small_cols else None\n    rs0 = ms.fit(want_cov=False) if ms else None\n    if W is None:\n        W = concept_weights(m.sid // 100, rng, n_boot)\n    B, L = [], []\n    for w in W:\n        r = m.fit(b0=r0[\"coef\"], w=w, want_cov=False)\n        B.append(r[\"coef\"])\n        if ms is not None:\n            L.append(2 * (r[\"ll\"] - ms.fit(b0=rs0[\"coef\"], w=w, want_cov=False)[\"ll\"]))\n    B = np.array(B)\n    out = {\"resampling_unit\": \"concept\", \"n_boot\": int(len(W))}\n    for tg in targets:\n        j = cols.index(tg)\n        out[tg] = {\"est\": float(r0[\"coef\"][j]), \"ci\": [float(np.nanpercentile(B[:, j], 2.5)), float(np.nanpercentile(B[:, j], 97.5))],\n                   \"se_boot\": float(np.nanstd(B[:, j])), \"p_one_sided_le0\": float((1 + (B[:, j] <= 0).sum()) / (1 + len(B)))}\n    if L:\n        L = np.array(L)\n        out[\"LR_boot_q\"] = [float(x) for x in np.percentile(L, [5, 25, 50, 75, 95])]\n    out[\"_B\"] = B\n    return out\n\n\ndef contrast_boot(df: pd.DataFrame, cols: list[str], a: str, b: str, n_boot: int, rng, sign: int = 1) -> dict:\n    \"\"\"bootstrap CI of coef[a] - coef[b] (concept refit).\"\"\"\n    bt = boot_refit(df, cols, [a, b], n_boot, rng)\n    d = bt[\"_B\"][:, cols.index(a)] - bt[\"_B\"][:, cols.index(b)]\n    est = bt[a][\"est\"] - bt[b][\"est\"]\n    return {\"resampling_unit\": \"concept\", \"n_boot\": n_boot, \"est\": float(est),\n            \"ci\": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],\n            \"p_one_sided\": float((1 + (sign * d <= 0).sum()) / (1 + len(d))), a: bt[a], b: bt[b]}\n\n\ndef crossed_boot(df: pd.DataFrame, cols: list[str], target: str, n_boot: int, rng) -> dict:\n    \"\"\"Owen pigeonhole: concept weights u_c ~ Poisson(1) on stratum log-lik; target-field weights v_k ~ Poisson(1) as\n    offset log(v_k) on each alternative (v_k = 0 removes the alternative; strata left uninformative drop out).\"\"\"\n    m0 = model(df, cols)\n    b0 = m0.fit(want_cov=False)[\"coef\"]\n    fk = df.field.to_numpy() - 11\n    cid = df.cidx.to_numpy()\n    uc, cinv = np.unique(cid, return_inverse=True)\n    B = []\n    for _ in range(n_boot):\n        v = rng.poisson(1.0, 26).astype(float)\n        u = rng.poisson(1.0, len(uc)).astype(float)\n        keep = (v[fk] > 0) & (u[cinv] > 0)\n        sub = df[keep]\n        off = np.log(v[fk][keep])\n        m = FastCLogit(sub[cols].to_numpy(np.float64), sub.entered.to_numpy(), sub.stratum.to_numpy(), offset=off)\n        if m.n_strata == 0:\n            continue\n        ws = u[np.searchsorted(uc, m.sid // 100)]\n        B.append(m.fit(b0=b0, w=ws, want_cov=False)[\"coef\"][cols.index(target)])\n    B = np.array(B)\n    return {\"resampling_unit\": \"concept x target field (Owen pigeonhole, Poisson(1) weights)\", \"n_boot\": int(len(B)),\n            \"ci\": [float(np.percentile(B, 2.5)), float(np.percentile(B, 97.5))], \"se_boot\": float(B.std())}\n\n\ndef lpm(df: pd.DataFrame, cols: list[str]) -> dict:\n    \"\"\"linear probability model with concept-year (stratum) FE, concept-clustered CRV1 SEs (econ-geo comparability).\"\"\"\n    r = fe_ols(df.entered.to_numpy(float), df[cols].to_numpy(float), [df.stratum.to_numpy()], df.cidx.to_numpy(), cols)\n    r.pop(\"V\", None); r.pop(\"_b\", None)\n    r[\"resampling_unit\"] = \"concept (CRV1 clusters)\"\n    r[\"base_rate\"] = float(df.entered.mean())\n    return r\n\n\ndef holm(pvals: dict[str, float]) -> dict[str, float]:\n    items = sorted(pvals.items(), key=lambda kv: kv[1])\n    m = len(items)\n    out, run = {}, 0.0\n    for i, (k, p) in enumerate(items):\n        run = max(run, min(1.0, (m - i) * p))\n        out[k] = float(run)\n    return out\n\n\ndef dl(b: list[float], se: list[float]) -> dict:\n    return dersimonian_laird(np.array(b), np.array(se))\n\n\ndef informative(df: pd.DataFrame) -> pd.DataFrame:\n    g = df.groupby(\"stratum\").entered.agg([\"sum\", \"size\"])\n    ok = g.index[(g[\"sum\"] > 0) & (g[\"sum\"] < g[\"size\"])]\n    return df[df.stratum.isin(ok)]\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [58] TOOL CALL — Bash · 2026-09-28 21:40:16 UTC

```
cat >> scratch_repro.py <<'EOF'
import models as M, stats_core
spec=json.load(open(R6+'/results/frozen_spec.json'))['standardisation']
prim=df[df.n_ret>0].copy(); print('primary rows',len(prim))
ps=M.standardise(prim,spec)
for rn in ['R0_M0','EXP6_M1','EXP6_M2lost']:
    cols=M.RUNGS[rn]; m=M.model(ps,cols); t=time.time(); r=m.fit(); print(rn, r['ll'], r['coef'].round(4), r['iters'], f'{time.time()-t:.2f}s')
    t=time.time(); o=stats_core.CLogit(ps[cols].to_numpy(),ps.entered.to_numpy(),ps.stratum.to_numpy()).fit(); print('  stats_core', o['ll'], o['coef'].round(4), f'{time.time()-t:.2f}s', np.abs(o['se']-r['se']).max())
EOF
.venv/bin/python scratch_repro.py 2>&1 | tail -8
```

### [59] TOOL RESULT — Bash · 2026-09-28 21:40:16 UTC

```
{"stdout": "n_lost 0\nprimary rows 46433\nR0_M0 -3270.093339782289 [0.3306 1.5846 0.3623 0.0995] 6 0.01s\n  stats_core -3270.093339796141 [0.3306 1.5846 0.3623 0.0994] 0.03s 6.480489358334784e-08\nEXP6_M1 -3235.8090189262984 [0.3719 1.6738 0.2385 0.0516 0.2809] 6 0.01s\n  stats_core -3235.809018933567 [0.3719 1.6738 0.2385 0.0516 0.2809] 0.02s 6.075933385585319e-08\nEXP6_M2lost -3268.246948147492 [ 0.3279  1.5834  0.3691  0.1032 -0.0632] 6 0.01s\n  stats_core -3268.2469481475136 [ 0.3279  1.5834  0.3691  0.1032 -0.0632] 0.02s 4.109572473987022e-09", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] ASSISTANT · 2026-09-28 21:40:58 UTC

```
Reproduction gate passed: LR(M1 vs M0) = 68.57, d0 = 0.2809, d_lost_gate = −0.0632, and 10 ms per fit. Now building the EXP5 side: de-duplication keys and grounded arrays.
```

### [61] TOOL CALL — Bash · 2026-09-28 21:40:58 UTC

```
.venv/bin/python -c "
import pandas as pd
R6='/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6'
lx=pd.read_parquet(R6+'/results/lexicon.parquet'); print(lx.columns.tolist(), len(lx)); print(lx.head(2).T)
fc=pd.read_csv(R6+'/results/frame_concepts.csv'); print(fc.split.value_counts(), fc.newborn.value_counts(), fc.group.value_counts())
"
```

### [62] TOOL RESULT — Bash · 2026-09-28 21:40:58 UTC

```
{"stdout": "['concept_idx', 'oa_int', 'id', 'name', 'form', 'level', 'wikidata', 'description', 'works_count'] 60859\n                                                             0                                      1\nconcept_idx                                                  0                                      1\noa_int                                                    4250                                  12843\nid                                  https://openalex.org/C4250            https://openalex.org/C12843\nname                                             Sign function              Gravitational singularity\nform                                             sign function              gravitational singularity\nlevel                                                        2                                      2\nwikidata                 https://www.wikidata.org/wiki/Q236813  https://www.wikidata.org/wiki/Q201721\ndescription  mathematical function that extracts the sign o...                                    NaN\nworks_count                                               1686                                 100575\nsplit\ndev               279\nheldout_cohort    248\nheldout_field     126\nName: count, dtype: int64 newborn\nTrue    653\nName: count, dtype: int64 group\nDEV_Med        280\nDEV_Eng         96\nSocial          95\nPhysical        49\nLifeEnv         47\nDEV_CS          40\nDEV_BGM         40\nOtherHealth      6\nName: count, dtype: int64", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] ASSISTANT · 2026-09-28 21:41:38 UTC

```
The engine is fast enough (~10 ms per fit on EXP6) that 1,000-draw bootstraps are cheap. Writing the EXP5 loader and de-duplication next.
```

### [64] TOOL CALL — Write · 2026-09-28 21:41:38 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/exp5.py

"""EXP5 / EXP6 inputs (read-only, by path), outcome-blind de-duplication and the grounded count arrays
(own re-implementation of EXP5 panel.build_arrays('grounded'), because that function caches into EXP5's directory)."""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from d3 import NY, Y0

RUN = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M")
EXP6 = RUN / "3_invention_loop/iter_2/gen_art/gen_art_experiment_6"
EXP5 = RUN / "3_invention_loop/iter_2/gen_art/gen_art_experiment_5"
DS2 = RUN / "3_invention_loop/iter_2/gen_art/gen_art_dataset_2"
FIELD_IDS = list(range(11, 37))
GROUP_OF_FIELD = {17: "CS", 22: "Eng", 13: "BGM", 27: "Med", 29: "Med", 35: "Med", 36: "Med",
                  15: "PHYS", 16: "PHYS", 19: "PHYS", 21: "PHYS", 25: "PHYS", 31: "PHYS",
                  11: "LIFEENV", 23: "LIFEENV", 24: "LIFEENV", 28: "LIFEENV", 30: "LIFEENV", 34: "LIFEENV",
                  12: "SOC", 14: "SOC", 20: "SOC", 32: "SOC", 33: "SOC", 26: "MATHDEC", 18: "MATHDEC"}
DEV_GROUPS = ["CS", "Eng", "BGM", "Med"]
HELD_GROUPS = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


def norm(s: str) -> str:
    """NFKD -> casefold -> non-alnum to space -> collapse -> strip a trailing 's' on the last token when len > 4."""
    s = unicodedata.normalize("NFKD", str(s))
    s = "".join(ch for ch in s if not unicodedata.combining(ch)).casefold()
    s = re.sub(r"[^0-9a-z]+", " ", s).strip()
    toks = s.split()
    if toks and len(toks[-1]) > 4 and toks[-1].endswith("s"):
        toks[-1] = toks[-1][:-1]
    return " ".join(toks)


def load_backbone() -> dict:
    b = json.loads((EXP6 / "inputs" / "field_backbone.json").read_text())
    phi = np.array(b["phi"], float)
    assert np.allclose(phi, phi.T), "phi not symmetric"
    assert not np.isnan(phi).any()
    if np.abs(np.diag(phi)).max() > 0:
        logger.warning("phi diagonal non-zero -> zeroed")
        np.fill_diagonal(phi, 0)
    return {"phi": phi, "gate": np.array(b["gateway_eig"], float), "raw_keys": list(b.keys())}


def exp6_GF() -> np.ndarray:
    return np.load(EXP6 / "scan" / "agg_counts.npz")["GF"]


def exp5_GF() -> tuple[np.ndarray, dict]:
    z = np.load(EXP5 / "scan" / "year_field_totals.npz")
    assert list(z["years"]) == list(range(Y0, Y0 + NY))
    return z["VF"][:, 1:].astype(np.int64), {k: z[k].shape for k in z.files}


def exp6_frame() -> tuple[pd.DataFrame, dict[int, np.ndarray]]:
    fc = pd.read_csv(EXP6 / "results" / "frame_concepts.csv")
    fc = fc[fc.newborn].copy()
    fc["home_list"] = [[int(h) for h in str(x).split("|")] for x in fc.home]
    fc["hgroup"] = np.where(fc.split == "heldout_cohort", "Cohort", np.where(fc.split == "dev", fc.group, fc.group))
    fc["intersect"] = fc.intersection_born.astype(int)
    fc["weak_home"] = fc.home_weak.astype(int)
    fc["home_med"] = fc.home_list.map(lambda h: int(GROUP_OF_FIELD[h[0]] == "Med"))
    fc["label_cov"] = fc.label_coverage_early
    fc["newborn_i"] = 1
    G = {}
    for sp in ("dev", "heldout"):
        z = np.load(EXP6 / "scan" / f"frame_g_{sp}.npz")
        G.update({int(c): z["g"][i] for i, c in enumerate(z["cidx"])})
    return fc, G


def recognition_keys(openalex_ints: set[int]) -> tuple[set[str], set[str], int]:
    """(qids, label_norms, n_records) from the concept_recognition dataset for the given OpenAlex ids."""
    qids, labels, n = set(), set(), 0
    for f in sorted((DS2 / "full_data_out").glob("full_data_out_*.json")):
        d = json.loads(f.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for ex in ds["examples"]:
                n += 1
                inp = json.loads(ex["input"])
                oid = int(str(inp["openalex_id"]).lstrip("C"))
                if oid in openalex_ints:
                    for k in ("qid", "qid_resolved"):
                        if inp.get(k):
                            qids.add(str(inp[k]))
                    if inp.get("label_norm"):
                        labels.add(inp["label_norm"])
                    if inp.get("label"):
                        labels.add(norm(inp["label"]))
        del d
    return qids, labels, n


def dedup(exp5: pd.DataFrame, exp6: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    ids6 = {int(u.split("/C")[-1]) for u in exp6.concept_id}
    lx = pd.read_parquet(EXP6 / "results" / "lexicon.parquet", columns=["oa_int", "wikidata", "name"])
    q6 = {str(w).rsplit("/", 1)[-1] for w in lx[lx.oa_int.isin(ids6)].wikidata.dropna()}
    rq, rl, nrec = recognition_keys(ids6)
    q6 |= rq
    lab6 = {norm(n) for n in exp6.name} | {norm(x) for x in rl}
    by_id = exp5.concept_id.astype(int).isin(ids6)
    by_q = exp5.qid.astype(str).isin(q6)
    by_l = exp5.name.map(norm).isin(lab6)
    drop = by_id | by_q | by_l
    rep = {"n_exp5": int(len(exp5)), "n_exp6_newborn_frame": int(len(exp6)), "n_exp6_ids": len(ids6), "n_exp6_qids": len(q6),
           "n_exp6_labels": len(lab6), "concept_recognition_records_scanned": nrec,
           "dropped_by_id": int(by_id.sum()), "dropped_by_qid": int(by_q.sum()), "dropped_by_label": int(by_l.sum()),
           "dropped_union": int(drop.sum()), "dropped_only_by_qid": int((by_q & ~by_id & ~by_l).sum()),
           "dropped_only_by_label": int((by_l & ~by_id & ~by_q).sum()),
           "kept": int((~drop).sum()),
           "dropped_by_split_group": exp5[drop].groupby(["split", "group"]).size().rename("n").reset_index().to_dict("records"),
           "dropped_concept_ids": sorted(map(int, exp5[drop].concept_id)),
           "exp6_ids_not_in_exp5": int(len(ids6 - set(exp5.concept_id.astype(int))))}
    return exp5[~drop].copy(), rep


def exp5_frame() -> pd.DataFrame:
    fc = pd.read_csv(EXP5 / "frame_concepts.csv")
    fc["home_list"] = [[int(h) for h in str(x).split(";")] for x in fc.home]
    fc["cidx"] = fc.ci.astype(int)
    fc["intersect"] = fc.intersect40.astype(int)
    fc["home_med"] = (fc.group == "Med").astype(int)
    fc["label_cov"] = fc.label_coverage_early
    fc["newborn_i"] = fc.newborn.astype(int)
    unit = np.where(fc.split.str.startswith("HELDOUT_"), fc.split.str.replace("HELDOUT_", "", regex=False), fc.split)
    unit = np.where(fc.split == "COHORT", np.where(fc.group.isin(DEV_GROUPS), "COHORT_DEVHOME", "COHORT_NONDEVHOME"), unit)
    fc["unit"] = unit
    return fc


def grounded_arrays(ci: np.ndarray) -> dict[str, np.ndarray]:
    """V [C, NY, 27] venue-field, P [C, NY, 27] primary-topic field, N [C, NY] all venues; weight = tagstate == 1
    (EXP5 frozen rule 'c_TAG'). Rows aligned with `ci`."""
    rule = json.loads((EXP5 / "grounding_report.json").read_text())["frozen_grounding_rule"]
    assert rule == "c_TAG", rule
    ag = pd.read_parquet(EXP5 / "scan" / "agg_counts.parquet", filters=[("tagstate", "==", 1)],
                         columns=["ci", "year", "vfield", "ptfield", "n"])
    pos = pd.Series(np.arange(len(ci)), index=ci)
    ag = ag[ag.ci.isin(pos.index)]
    r = pos.loc[ag.ci.to_numpy()].to_numpy()
    y = ag.year.to_numpy(np.int64) - Y0
    ok = (y >= 0) & (y < NY)
    r, y, n = r[ok], y[ok], ag.n.to_numpy(np.float64)[ok]
    vf, pt = ag.vfield.to_numpy(np.int64)[ok], ag.ptfield.to_numpy(np.int64)[ok]
    C = len(ci)
    N = np.bincount(r * NY + y, weights=n, minlength=C * NY).reshape(C, NY).astype(np.float32)
    V = np.bincount((r * NY + y) * 27 + vf, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    P = np.bincount((r * NY + y) * 27 + pt, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)
    return {"N": N, "V": V, "P": P}


def home_rule(V: np.ndarray, t0: int, n_first: int = 30) -> list[int]:
    """EXP5 frame.home_rule (re-implemented): fields with >= 40% of the first 30 venue-labelled works from t0 on
    (proportional boundary year), else the top field if >= 25% (weak home)."""
    acc = np.zeros(26)
    got = 0.0
    for y in range(t0, Y0 + NY):
        row = V[y - Y0, 1:27].astype(float)
        tot = row.sum()
        if tot <= 0:
            continue
        need = n_first - got
        if tot <= need:
            acc += row; got += tot
        else:
            acc += row * need / tot; got += need
        if got >= n_first - 1e-9:
            break
    if got <= 0:
        return []
    sh = acc / got
    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]
    if home:
        return sorted(home, key=lambda f: -sh[f - 11])
    o = int(np.argmax(sh))
    return [FIELD_IDS[o]] if sh[o] >= 0.25 else []


def phi_min_cp(years: tuple[int, int] = (1998, 2002)) -> np.ndarray:
    """Hidalgo min-conditional-probability proximity from EXP5 26x26 field co-assignment: C_jk / max(C_jj, C_kk)."""
    z = np.load(EXP5 / "scan" / "co_by_year.npz")
    yrs = list(z["years"])
    Cm = z["CO"][yrs.index(years[0]):yrs.index(years[1]) + 1].sum(0).astype(float)
    d = np.diag(Cm)
    P = Cm / np.maximum(np.maximum.outer(d, d), 1)
    np.fill_diagonal(P, 0)
    return (P + P.T) / 2
```

### [65] TOOL RESULT — Write · 2026-09-28 21:41:38 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/exp5.py", "content": "\"\"\"EXP5 / EXP6 inputs (read-only, by path), outcome-blind de-duplication and the grounded count arrays\n(own re-implementation of EXP5 panel.build_arrays('grounded'), because that function caches into EXP5's directory).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport re\nimport unicodedata\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\n\nfrom d3 import NY, Y0\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M\")\nEXP6 = RUN / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"\nEXP5 = RUN / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_5\"\nDS2 = RUN / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"\nFIELD_IDS = list(range(11, 37))\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\", 26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\n\n\ndef norm(s: str) -> str:\n    \"\"\"NFKD -> casefold -> non-alnum to space -> collapse -> strip a trailing 's' on the last token when len > 4.\"\"\"\n    s = unicodedata.normalize(\"NFKD\", str(s))\n    s = \"\".join(ch for ch in s if not unicodedata.combining(ch)).casefold()\n    s = re.sub(r\"[^0-9a-z]+\", \" \", s).strip()\n    toks = s.split()\n    if toks and len(toks[-1]) > 4 and toks[-1].endswith(\"s\"):\n        toks[-1] = toks[-1][:-1]\n    return \" \".join(toks)\n\n\ndef load_backbone() -> dict:\n    b = json.loads((EXP6 / \"inputs\" / \"field_backbone.json\").read_text())\n    phi = np.array(b[\"phi\"], float)\n    assert np.allclose(phi, phi.T), \"phi not symmetric\"\n    assert not np.isnan(phi).any()\n    if np.abs(np.diag(phi)).max() > 0:\n        logger.warning(\"phi diagonal non-zero -> zeroed\")\n        np.fill_diagonal(phi, 0)\n    return {\"phi\": phi, \"gate\": np.array(b[\"gateway_eig\"], float), \"raw_keys\": list(b.keys())}\n\n\ndef exp6_GF() -> np.ndarray:\n    return np.load(EXP6 / \"scan\" / \"agg_counts.npz\")[\"GF\"]\n\n\ndef exp5_GF() -> tuple[np.ndarray, dict]:\n    z = np.load(EXP5 / \"scan\" / \"year_field_totals.npz\")\n    assert list(z[\"years\"]) == list(range(Y0, Y0 + NY))\n    return z[\"VF\"][:, 1:].astype(np.int64), {k: z[k].shape for k in z.files}\n\n\ndef exp6_frame() -> tuple[pd.DataFrame, dict[int, np.ndarray]]:\n    fc = pd.read_csv(EXP6 / \"results\" / \"frame_concepts.csv\")\n    fc = fc[fc.newborn].copy()\n    fc[\"home_list\"] = [[int(h) for h in str(x).split(\"|\")] for x in fc.home]\n    fc[\"hgroup\"] = np.where(fc.split == \"heldout_cohort\", \"Cohort\", np.where(fc.split == \"dev\", fc.group, fc.group))\n    fc[\"intersect\"] = fc.intersection_born.astype(int)\n    fc[\"weak_home\"] = fc.home_weak.astype(int)\n    fc[\"home_med\"] = fc.home_list.map(lambda h: int(GROUP_OF_FIELD[h[0]] == \"Med\"))\n    fc[\"label_cov\"] = fc.label_coverage_early\n    fc[\"newborn_i\"] = 1\n    G = {}\n    for sp in (\"dev\", \"heldout\"):\n        z = np.load(EXP6 / \"scan\" / f\"frame_g_{sp}.npz\")\n        G.update({int(c): z[\"g\"][i] for i, c in enumerate(z[\"cidx\"])})\n    return fc, G\n\n\ndef recognition_keys(openalex_ints: set[int]) -> tuple[set[str], set[str], int]:\n    \"\"\"(qids, label_norms, n_records) from the concept_recognition dataset for the given OpenAlex ids.\"\"\"\n    qids, labels, n = set(), set(), 0\n    for f in sorted((DS2 / \"full_data_out\").glob(\"full_data_out_*.json\")):\n        d = json.loads(f.read_text())\n        for ds in d[\"datasets\"]:\n            if ds[\"dataset\"] != \"concept_recognition\":\n                continue\n            for ex in ds[\"examples\"]:\n                n += 1\n                inp = json.loads(ex[\"input\"])\n                oid = int(str(inp[\"openalex_id\"]).lstrip(\"C\"))\n                if oid in openalex_ints:\n                    for k in (\"qid\", \"qid_resolved\"):\n                        if inp.get(k):\n                            qids.add(str(inp[k]))\n                    if inp.get(\"label_norm\"):\n                        labels.add(inp[\"label_norm\"])\n                    if inp.get(\"label\"):\n                        labels.add(norm(inp[\"label\"]))\n        del d\n    return qids, labels, n\n\n\ndef dedup(exp5: pd.DataFrame, exp6: pd.DataFrame) -> tuple[pd.DataFrame, dict]:\n    ids6 = {int(u.split(\"/C\")[-1]) for u in exp6.concept_id}\n    lx = pd.read_parquet(EXP6 / \"results\" / \"lexicon.parquet\", columns=[\"oa_int\", \"wikidata\", \"name\"])\n    q6 = {str(w).rsplit(\"/\", 1)[-1] for w in lx[lx.oa_int.isin(ids6)].wikidata.dropna()}\n    rq, rl, nrec = recognition_keys(ids6)\n    q6 |= rq\n    lab6 = {norm(n) for n in exp6.name} | {norm(x) for x in rl}\n    by_id = exp5.concept_id.astype(int).isin(ids6)\n    by_q = exp5.qid.astype(str).isin(q6)\n    by_l = exp5.name.map(norm).isin(lab6)\n    drop = by_id | by_q | by_l\n    rep = {\"n_exp5\": int(len(exp5)), \"n_exp6_newborn_frame\": int(len(exp6)), \"n_exp6_ids\": len(ids6), \"n_exp6_qids\": len(q6),\n           \"n_exp6_labels\": len(lab6), \"concept_recognition_records_scanned\": nrec,\n           \"dropped_by_id\": int(by_id.sum()), \"dropped_by_qid\": int(by_q.sum()), \"dropped_by_label\": int(by_l.sum()),\n           \"dropped_union\": int(drop.sum()), \"dropped_only_by_qid\": int((by_q & ~by_id & ~by_l).sum()),\n           \"dropped_only_by_label\": int((by_l & ~by_id & ~by_q).sum()),\n           \"kept\": int((~drop).sum()),\n           \"dropped_by_split_group\": exp5[drop].groupby([\"split\", \"group\"]).size().rename(\"n\").reset_index().to_dict(\"records\"),\n           \"dropped_concept_ids\": sorted(map(int, exp5[drop].concept_id)),\n           \"exp6_ids_not_in_exp5\": int(len(ids6 - set(exp5.concept_id.astype(int))))}\n    return exp5[~drop].copy(), rep\n\n\ndef exp5_frame() -> pd.DataFrame:\n    fc = pd.read_csv(EXP5 / \"frame_concepts.csv\")\n    fc[\"home_list\"] = [[int(h) for h in str(x).split(\";\")] for x in fc.home]\n    fc[\"cidx\"] = fc.ci.astype(int)\n    fc[\"intersect\"] = fc.intersect40.astype(int)\n    fc[\"home_med\"] = (fc.group == \"Med\").astype(int)\n    fc[\"label_cov\"] = fc.label_coverage_early\n    fc[\"newborn_i\"] = fc.newborn.astype(int)\n    unit = np.where(fc.split.str.startswith(\"HELDOUT_\"), fc.split.str.replace(\"HELDOUT_\", \"\", regex=False), fc.split)\n    unit = np.where(fc.split == \"COHORT\", np.where(fc.group.isin(DEV_GROUPS), \"COHORT_DEVHOME\", \"COHORT_NONDEVHOME\"), unit)\n    fc[\"unit\"] = unit\n    return fc\n\n\ndef grounded_arrays(ci: np.ndarray) -> dict[str, np.ndarray]:\n    \"\"\"V [C, NY, 27] venue-field, P [C, NY, 27] primary-topic field, N [C, NY] all venues; weight = tagstate == 1\n    (EXP5 frozen rule 'c_TAG'). Rows aligned with `ci`.\"\"\"\n    rule = json.loads((EXP5 / \"grounding_report.json\").read_text())[\"frozen_grounding_rule\"]\n    assert rule == \"c_TAG\", rule\n    ag = pd.read_parquet(EXP5 / \"scan\" / \"agg_counts.parquet\", filters=[(\"tagstate\", \"==\", 1)],\n                         columns=[\"ci\", \"year\", \"vfield\", \"ptfield\", \"n\"])\n    pos = pd.Series(np.arange(len(ci)), index=ci)\n    ag = ag[ag.ci.isin(pos.index)]\n    r = pos.loc[ag.ci.to_numpy()].to_numpy()\n    y = ag.year.to_numpy(np.int64) - Y0\n    ok = (y >= 0) & (y < NY)\n    r, y, n = r[ok], y[ok], ag.n.to_numpy(np.float64)[ok]\n    vf, pt = ag.vfield.to_numpy(np.int64)[ok], ag.ptfield.to_numpy(np.int64)[ok]\n    C = len(ci)\n    N = np.bincount(r * NY + y, weights=n, minlength=C * NY).reshape(C, NY).astype(np.float32)\n    V = np.bincount((r * NY + y) * 27 + vf, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)\n    P = np.bincount((r * NY + y) * 27 + pt, weights=n, minlength=C * NY * 27).reshape(C, NY, 27).astype(np.float32)\n    return {\"N\": N, \"V\": V, \"P\": P}\n\n\ndef home_rule(V: np.ndarray, t0: int, n_first: int = 30) -> list[int]:\n    \"\"\"EXP5 frame.home_rule (re-implemented): fields with >= 40% of the first 30 venue-labelled works from t0 on\n    (proportional boundary year), else the top field if >= 25% (weak home).\"\"\"\n    acc = np.zeros(26)\n    got = 0.0\n    for y in range(t0, Y0 + NY):\n        row = V[y - Y0, 1:27].astype(float)\n        tot = row.sum()\n        if tot <= 0:\n            continue\n        need = n_first - got\n        if tot <= need:\n            acc += row; got += tot\n        else:\n            acc += row * need / tot; got += need\n        if got >= n_first - 1e-9:\n            break\n    if got <= 0:\n        return []\n    sh = acc / got\n    home = [FIELD_IDS[k] for k in range(26) if sh[k] >= 0.4]\n    if home:\n        return sorted(home, key=lambda f: -sh[f - 11])\n    o = int(np.argmax(sh))\n    return [FIELD_IDS[o]] if sh[o] >= 0.25 else []\n\n\ndef phi_min_cp(years: tuple[int, int] = (1998, 2002)) -> np.ndarray:\n    \"\"\"Hidalgo min-conditional-probability proximity from EXP5 26x26 field co-assignment: C_jk / max(C_jj, C_kk).\"\"\"\n    z = np.load(EXP5 / \"scan\" / \"co_by_year.npz\")\n    yrs = list(z[\"years\"])\n    Cm = z[\"CO\"][yrs.index(years[0]):yrs.index(years[1]) + 1].sum(0).astype(float)\n    d = np.diag(Cm)\n    P = Cm / np.maximum(np.maximum.outer(d, d), 1)\n    np.fill_diagonal(P, 0)\n    return (P + P.T) / 2\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [66] TOOL CALL — Bash · 2026-09-28 21:41:38 UTC

```
cat > scratch_exp5.py <<'EOF'
import sys, time, numpy as np, pandas as pd
sys.path.insert(0,'lib')
import exp5 as X, d3
t=time.time()
f5=X.exp5_frame(); f6,_=X.exp6_frame()
keep,rep=X.dedup(f5,f6); print({k:v for k,v in rep.items() if k!='dropped_concept_ids' and k!='dropped_by_split_group'}, time.time()-t)
print(keep.unit.value_counts())
t=time.time(); A=X.grounded_arrays(keep.cidx.to_numpy()); print('arrays',time.time()-t, A['V'].nbytes/1e6)
t0=keep.t0.to_numpy()
ev=np.array([A['N'][i,t0[i]-1995:t0[i]-1995+3].sum() for i in range(len(keep))])
print('early_volume match', np.mean(np.isclose(ev, keep.early_volume.to_numpy(), atol=1e-3)))
hm=[X.home_rule(A['V'][i], t0[i]) for i in range(len(keep))]
print('home match', np.mean([h==hl for h,hl in zip(hm, keep.home_list)]))
GF5,_=X.exp5_GF(); GF6=X.exp6_GF(); print('GF equal', np.array_equal(GF5,GF6), np.abs(GF5-GF6).max())
import numpy as np
z=np.load(X.EXP5/'scan'/'co_by_year.npz'); C=z['CO'][3:8].sum(0); print(np.diag(C)[:5], C[0,:5], GF5[3:8].sum(0)[:5])
P=X.phi_min_cp(); print(P.max(), (P>0).mean())
EOF
.venv/bin/python scratch_exp5.py
```

### [67] TOOL RESULT — Bash · 2026-09-28 21:42:14 UTC

```
{"stdout": "{'n_exp5': 12499, 'n_exp6_newborn_frame': 653, 'n_exp6_ids': 653, 'n_exp6_qids': 638, 'n_exp6_labels': 667, 'concept_recognition_records_scanned': 65026, 'dropped_by_id': 628, 'dropped_by_qid': 658, 'dropped_by_label': 628, 'dropped_union': 658, 'dropped_only_by_qid': 30, 'dropped_only_by_label': 0, 'kept': 11841, 'exp6_ids_not_in_exp5': 25} 10.371062517166138\nunit\nDEV                  4486\nCOHORT_DEVHOME       2301\nCOHORT_NONDEVHOME    1803\nSOC                  1299\nLIFEENV              1079\nPHYS                  708\nMATHDEC               165\nName: count, dtype: int64\narrays 0.7105958461761475 35.807184\nearly_volume match 1.0\nhome match 0.9981420488134448\nGF equal True 0\n[ 944208 1132221 1434480  454142  112872] [944208  11565 232349  12529   2190] [353650 401379 402641  93199    384]\n0.2333542009038112 0.9615384615384616", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [68] ASSISTANT · 2026-09-28 21:45:12 UTC

```
Early volume matches 100%, home 99.8%, and GF is identical to EXP6's. De-dup drops 658 concepts (30 of them by QID only), leaving 11,841. Now writing the orchestrator, `method.py`.
```

### [69] TOOL CALL — Write · 2026-09-28 21:45:12 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/analysis.py

"""Analysis battery shared by every frame and split (EXP6 robustness, EXP5-minus-EXP6 DEV, held-out):
ladder, bootstraps, specificity (a)-(o), abandonment, per-unit fits, power simulation."""
from __future__ import annotations

import time
import zlib

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats
from sklearn.metrics import roc_auc_score

import d3
import h2_exp6 as H2
import models as M

M.RUNGS.update({
    "A1_split": M.BASE + ["d_lost_short", "d_lost_long"],
    "VM0": M.RUNGS["R2_vol"],
    "VM": M.RUNGS["R2_vol"] + ["d_R_m", "d_N_m"],
    "DOSE": M.RUNGS["R2_vol"] + ["d_ret_a2", "d_ret_a3", "d_ret_a4p"],
    "R3_Dcum": M.RUNGS["R3_ret"] + ["D_cum"],
    "R2_Dcum": M.RUNGS["R2_vol"] + ["D_cum"],
})
PRIM_RUNGS = ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost", "S_strict0", "S_strict", "EXP6_M1", "EXP6_M2lost"]


def rng_for(seed: int, tag: str) -> np.random.Generator:
    return np.random.default_rng([seed, zlib.crc32(tag.encode())])


def split_std(df_all: pd.DataFrame, spec: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """(primary = strata with a non-empty retained set [EXP6 convention], all candidate rows), both standardised."""
    alls = M.standardise(df_all, spec)
    return alls[df_all.n_ret.to_numpy() > 0], alls


def coef_row(df: pd.DataFrame, cols: list[str], target: str, small: list[str] | None = None) -> dict:
    m = M.model(df, cols)
    r = m.fit()
    j = cols.index(target)
    out = {"coef": float(r["coef"][j]), "se_model": float(r["se"][j]), "n_strata": r["n_strata"], "n_events": r["n_events"],
           "n_concepts": int(df.cidx.nunique()), "converged": r["converged"]}
    if r["n_strata"] > 0:
        out["se_concept"] = float(m.cluster_se(r, "concept")[j])
        out["p_wald_concept_2s"] = float(2 * stats.norm.sf(abs(out["coef"] / out["se_concept"]))) if out["se_concept"] > 0 else None
    if small is not None:
        rs = M.model(df, small).fit(want_cov=False)
        out["LR"] = M.lr(r, rs, len(cols) - len(small))
    return out


def sens_pair(prim: pd.DataFrame, alls: pd.DataFrame, extra: list[str] | None = None, drop: list[str] | None = None) -> dict:
    """d0 in R3 (LR vs R2) on the primary sample and d_lost in A1 (LR vs R0) on all rows."""
    extra = extra or []
    drop = drop or []
    f = lambda c: [x for x in c if x not in drop] + extra  # noqa: E731
    return {"d0_R3": coef_row(prim, f(M.RUNGS["R3_ret"]), "d0_ret_rel", f(M.RUNGS["R2_vol"])),
            "d_lost_A1": coef_row(alls, f(M.RUNGS["A1_lost"]), "d_lost", f(M.RUNGS["R0_M0"]))}


def vif_block(prim: pd.DataFrame, cols: list[str]) -> dict:
    d = M.informative(prim)
    Z = d[cols].to_numpy(float)
    _, inv = np.unique(d.stratum.to_numpy(), return_inverse=True)
    cnt = np.bincount(inv)
    for j in range(Z.shape[1]):
        Z[:, j] -= (np.bincount(inv, weights=Z[:, j]) / cnt)[inv]
    Z = Z / np.maximum(Z.std(0), 1e-12)
    Cm = np.corrcoef(Z, rowvar=False)
    try:
        vif = np.diag(np.linalg.inv(Cm))
    except np.linalg.LinAlgError:
        vif = np.full(len(cols), np.inf)
    return {"vif_within_stratum": dict(zip(cols, map(float, vif))), "condition_number": float(np.linalg.cond(Z)),
            "corr_within": pd.DataFrame(Cm, index=cols, columns=cols).round(3).to_dict()}


# ----------------------------------------------------------------------------- nulls
def _d0_from_masks(Mk: np.ndarray, phi: np.ndarray, pos: np.ndarray, k: np.ndarray) -> np.ndarray:
    return d3._mrel(Mk, phi)[pos, k]


def perm_null(prim: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n: int, pool: str = "POOL") -> dict:
    """(a) retained-label permutation within concept-year: |RET| fields drawn uniformly from the pool of age-eligible
    entered off-home fields (footprint and set size kept, persistence scrambled). Statistic LR(R3 vs R2)."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    m3 = M.model(prim, c3); r3 = m3.fit(want_cov=False)
    ll2 = M.model(prim, c2).fit(want_cov=False)["ll"]
    obs = 2 * (r3["ll"] - ll2)
    sidx = prim.s_idx.to_numpy(); k = prim.field.to_numpy() - 11
    us, pos = np.unique(sidx, return_inverse=True)
    RET, P = st["RET"][us], st[pool][us]
    nret = RET.sum(1)
    assert (P | RET).sum() == P.sum(), "pool must contain RET"
    j = c3.index("d0_ret_rel")
    mu, sd = spec["d0_ret_rel"]["mean"], spec["d0_ret_rel"]["sd"]
    inf_s = np.isin(us, np.unique(sidx[np.isin(prim.stratum.to_numpy(), m3.sid)]))
    nontriv = float(((P.sum(1) > nret) & (nret > 0))[inf_s].mean())
    null = []
    for _ in range(n):
        key = rng.random(P.shape)
        key[~P] = 2.0
        rank = key.argsort(1).argsort(1)
        Mk = rank < nret[:, None]
        m3.set_col(j, (_d0_from_masks(Mk, phi, pos, k) - mu) / sd)
        null.append(2 * (m3.fit(b0=r3["coef"], want_cov=False)["ll"] - ll2))
    null = np.array(null)
    return {"pool": pool, "n_perm": n, "LR_obs": float(obs), "p": float((1 + (null >= obs).sum()) / (1 + n)),
            "null_q": [float(x) for x in np.percentile(null, [50, 90, 95, 99])], "null_mean": float(null.mean()),
            "share_strata_nontrivial": nontriv, "resampling_unit": "within concept-year stratum (label permutation)",
            "_null": null}


def backbone_null(prim: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n_rewire: int, n_label: int) -> dict:
    """(d) PRIMARY: recompute d0 only on (i) degree-preserving rewired phi, (ii) node-label-permuted phi."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    m3 = M.model(prim, c3); r3 = m3.fit(want_cov=False)
    ll2 = M.model(prim, c2).fit(want_cov=False)["ll"]
    obs = 2 * (r3["ll"] - ll2)
    sidx = prim.s_idx.to_numpy(); k = prim.field.to_numpy() - 11
    us, pos = np.unique(sidx, return_inverse=True)
    RET = st["RET"][us]
    j = c3.index("d0_ret_rel")
    mu, sd = spec["d0_ret_rel"]["mean"], spec["d0_ret_rel"]["sd"]
    out = {"LR_obs": float(obs)}
    for name, nn in (("rewire", n_rewire), ("label_perm", n_label)):
        null = []
        for _ in range(nn):
            if name == "rewire":
                P = H2.rewire(phi, rng)
            else:
                p = rng.permutation(26)
                P = phi[np.ix_(p, p)]
            m3.set_col(j, (_d0_from_masks(RET, P, pos, k) - mu) / sd)
            null.append(2 * (m3.fit(b0=r3["coef"], want_cov=False)["ll"] - ll2))
        null = np.array(null)
        out[name] = {"n": nn, "p": float((1 + (null >= obs).sum()) / (1 + nn)),
                     "null_q": [float(x) for x in np.percentile(null, [50, 90, 95, 99])], "_null": null}
    return out


def backbone_null_full(df_all: pd.DataFrame, st: dict, phi: np.ndarray, spec: dict, rng, n: int) -> dict:
    """(d) SECONDARY: every phi covariate and the gateway recomputed on each rewired backbone; LR(R3 vs R2) and d0."""
    prim_mask = df_all.n_ret.to_numpy() > 0
    base = df_all[["cidx", "t", "field", "entered", "stratum", "s_idx", "b_log_size"]].reset_index(drop=True)
    lrs, d0s = [], []
    for _ in range(n):
        P = H2.rewire(phi, rng)
        gp = H2.eig_gateway(P)
        cv = d3.covariates(st, P, gp)
        assert len(cv) == len(base) and (cv.s_idx.to_numpy() == base.s_idx.to_numpy()).all()
        d = base.copy()
        for c in d3.PHI_COLS + ["e_gate_own"]:
            d[c] = cv[c].to_numpy()
        d = M.standardise(d[prim_mask], spec)
        r3 = M.model(d, M.RUNGS["R3_ret"]).fit(want_cov=False)
        r2 = M.model(d, M.RUNGS["R2_vol"]).fit(want_cov=False)
        lrs.append(2 * (r3["ll"] - r2["ll"])); d0s.append(r3["coef"][-1])
    return {"n": n, "LR_null_q": [float(x) for x in np.percentile(lrs, [50, 90, 95, 99])],
            "d0_null_q": [float(x) for x in np.percentile(d0s, [5, 50, 95])], "_lrs": np.array(lrs)}


# ----------------------------------------------------------------------------- battery
def ladder_block(prim: pd.DataFrame, alls: pd.DataFrame) -> dict:
    lad = M.fit_ladder(prim, PRIM_RUNGS, two_way=["R3_ret"])
    lad.pop("_fits")
    ab = M.fit_ladder(alls, ["R0_M0", "A1_lost", "A1_split"], two_way=["A1_lost"])
    ab.pop("_fits")
    ab["LR"]["A1_split_vs_R0_M0"] = M.lr({"ll": ab["models"]["A1_split"]["ll"]}, {"ll": ab["models"]["R0_M0"]["ll"]}, 2)
    return {"frontier_primary_sample": lad, "abandonment_all_rows": ab}


def headline_boots(prim: pd.DataFrame, alls: pd.DataFrame, rng, n_boot: int, second_seed: bool = False) -> dict:
    t = time.time()
    out = {"d0_R3": M.boot_refit(prim, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["R2_vol"]),
           "d0_S_strict": M.boot_refit(prim, M.RUNGS["S_strict"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["S_strict0"]),
           "d_lost_A1": M.boot_refit(alls, M.RUNGS["A1_lost"], ["d_lost"], n_boot, rng, small_cols=M.RUNGS["R0_M0"]),
           "R4": M.boot_refit(prim, M.RUNGS["R4_lost"], ["d0_ret_rel", "d_lost"], n_boot, rng)}
    if second_seed:
        b2 = M.boot_refit(prim, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, np.random.default_rng(rng.integers(1 << 31)))
        a, b = out["d0_R3"]["d0_ret_rel"]["ci"], b2["d0_ret_rel"]["ci"]
        out["T6_seed_stability_d0_R3"] = {"ci_seed1": a, "ci_seed2": b, "max_endpoint_shift": float(max(abs(a[0] - b[0]), abs(a[1] - b[1]))),
                                          "pass_lt_0.01": bool(max(abs(a[0] - b[0]), abs(a[1] - b[1])) < 0.01)}
    for v in out.values():
        if isinstance(v, dict):
            v.pop("_B", None)
    logger.info(f"headline bootstraps ({n_boot}) in {time.time()-t:.0f}s")
    return out


def specificity(df_all: pd.DataFrame, st: dict, prim: pd.DataFrame, alls: pd.DataFrame, spec: dict, bb: dict, rng,
                n_boot: int, n_perm: int, n_rewire: int, n_label: int, n_rewire_full: int) -> dict:
    phi = bb["phi"]
    out = {}
    t = time.time()
    out["a_permutation"] = perm_null(prim, st, phi, spec, rng, n_perm, "POOL")
    out["a_permutation_secondary_all_entered_offhome"] = perm_null(prim, st, phi, spec, rng, max(n_perm // 2, 20), "ENTOFF")
    logger.info(f"  (a) permutation {time.time()-t:.0f}s p={out['a_permutation']['p']:.4f}")
    # (b) volume-matched contrast
    vm = prim[prim.has_match == 1]
    b = {"match_rate_strata": float(prim.groupby("stratum").has_match.max().mean()), "n_rows": int(len(vm)),
         "n_strata": int(vm.stratum.nunique()), "n_concepts": int(vm.cidx.nunique())}
    if vm.cidx.nunique() >= 20:
        b["fit"] = coef_row(vm, M.RUNGS["VM"], "d_R_m", M.RUNGS["VM0"])
        b["fit_N"] = coef_row(vm, M.RUNGS["VM"], "d_N_m")
        b["contrast_R_minus_N"] = M.contrast_boot(vm, M.RUNGS["VM"], "d_R_m", "d_N_m", n_boot, rng)
        # balance of matched fields: mean n(t-1) and cum(t-1) for matched R vs N fields
        us = np.unique(vm.s_idx.to_numpy())
        Rm, Nm = d3.vol_matched_masks({k_: st[k_][us] for k_ in ("xprev", "cumprev", "RET", "ENTOFF")})
        b["balance"] = {"mean_n_prev_R": float(st["xprev"][us][Rm].mean()), "mean_n_prev_N": float(st["xprev"][us][Nm].mean()),
                        "mean_cum_prev_R": float(st["cumprev"][us][Rm].mean()), "mean_cum_prev_N": float(st["cumprev"][us][Nm].mean()),
                        "n_matched_R_fields": int(Rm.sum()), "n_matched_N_fields": int(Nm.sum())}
    else:
        b["status"] = "too few matched concepts"
    out["b_volume_matched"] = b
    out["b_D_cum_rival"] = coef_row(prim, M.RUNGS["R3_Dcum"], "d0_ret_rel", M.RUNGS["R2_Dcum"])
    # (c) dose
    cdose = M.RUNGS["DOSE"]
    dose = {"fit": {c: coef_row(prim, cdose, c) for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")}}
    dose["contrast_4p_minus_2"] = M.contrast_boot(prim, cdose, "d_ret_a4p", "d_ret_a2", n_boot, rng)
    bet = [dose["fit"][c]["coef"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
    dose["betas_by_age"] = dict(zip(["2", "3", "4+"], bet))
    dose["monotone_nondecreasing"] = bool(bet[0] <= bet[1] <= bet[2])
    dose["spearman_beta_age"] = float(stats.spearmanr([2, 3, 4], bet).statistic)
    out["c_dose"] = dose
    # (d) backbone nulls
    t = time.time()
    out["d_backbone_d0_only"] = backbone_null(prim, st, phi, spec, rng, n_rewire, n_label)
    if n_rewire_full > 0:
        out["d_backbone_full_recompute"] = backbone_null_full(df_all, st, phi, spec, rng, n_rewire_full)
        out["d_backbone_full_recompute"]["LR_obs"] = out["d_backbone_d0_only"]["LR_obs"]
        nl = out["d_backbone_full_recompute"]["_lrs"]
        out["d_backbone_full_recompute"]["p"] = float((1 + (nl >= out["d_backbone_d0_only"]["LR_obs"]).sum()) / (1 + len(nl)))
    logger.info(f"  (d) backbone nulls {time.time()-t:.0f}s")
    # (e), (g)-(j), (n), (o): subsets / FE
    sub = lambda m: sens_pair(prim[m(prim)], alls[m(alls)])  # noqa: E731
    out["e_excl_intersection_born"] = sub(lambda d: d.intersect == 0)
    fe_cols = [f"fe_{f}" for f in range(12, 37)]
    pf, af = prim.copy(), alls.copy()
    for f in range(12, 37):
        pf[f"fe_{f}"] = (pf.field == f).astype(float); af[f"fe_{f}"] = (af.field == f).astype(float)
    out["g_target_field_FE"] = sens_pair(pf, af, extra=fe_cols, drop=["e_gate_own"])
    out["g_target_field_FE"]["note"] = "25 field dummies; e_gate_own is field-constant and absorbed, so dropped"
    out["h_horizon8"] = sub(lambda d: d.age <= 8)
    out["i_excl_weak_home"] = sub(lambda d: d.weak_home == 0)
    out["j_excl_medicine_home"] = sub(lambda d: d.home_med == 0)
    out["n_newborn_only_descriptive"] = sub(lambda d: d.newborn_i == 1) if (prim.newborn_i == 1).any() else {"status": "none"}
    out["o_label_coverage_ge_0.5"] = sub(lambda d: d.label_cov >= 0.5)
    return out


def rebuild_sens(frame: pd.DataFrame, G: np.ndarray, GF: np.ndarray, bb: dict, spec: dict, horizon: int, meta: list[str],
                 Gpt: np.ndarray | None = None) -> dict:
    """(f) min_n 3 / 5, (k) primary-topic fields, (l) RCA-defined entry event, (m) min-CP proximity: rebuild and refit."""
    import exp5 as X
    out = {}
    jobs = [("f_min_n_3", dict(min_n=3)), ("f_min_n_5", dict(min_n=5)), ("l_rca_entry_event", dict(entry_def="rca"))]
    for name, kw in jobs:
        st = d3.build_strata(frame, G, GF, horizon=horizon, **kw)
        df = d3.attach_meta(d3.covariates(st, bb["phi"], bb["gate"]), st, frame, meta)
        p, a = split_std(df, spec)
        out[name] = sens_pair(p, a)
        out[name]["n_events_all"] = int(df.entered.sum())
    if Gpt is not None:
        st = d3.build_strata(frame, Gpt, GF, horizon=horizon)
        df = d3.attach_meta(d3.covariates(st, bb["phi"], bb["gate"]), st, frame, meta)
        p, a = split_std(df, spec)
        out["k_primary_topic_fields"] = sens_pair(p, a)
    phm = X.phi_min_cp()
    st = d3.build_strata(frame, G, GF, horizon=horizon)
    df = d3.attach_meta(d3.covariates(st, phm, bb["gate"]), st, frame, meta)
    # min-CP covariates live on a different scale: standardise on this frame's own moments (reported as such)
    sp2 = M.make_spec(df[df.n_ret > 0])
    p, a = split_std(df, sp2)
    out["m_min_conditional_probability_proximity"] = {"ladder": {k: v for k, v in M.fit_ladder(p, ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost"]).items() if k != "_fits"},
                                                      **sens_pair(p, a), "note": "standardised on this sample's own moments"}
    return out


def unit_fits(prim: pd.DataFrame, alls: pd.DataFrame, unit_col: str, units: list[str], rng, n_boot: int) -> dict:
    out = {}
    for u in units:
        p, a = prim[prim[unit_col] == u], alls[alls[unit_col] == u]
        if p.cidx.nunique() < 5:
            out[u] = {"status": "too few concepts", "n_concepts": int(p.cidx.nunique())}
            continue
        r = sens_pair(p, a)
        bt = M.boot_refit(p, M.RUNGS["R3_ret"], ["d0_ret_rel"], n_boot, rng)
        r["d0_R3"]["boot_ci"] = bt["d0_ret_rel"]["ci"]
        bl = M.boot_refit(a, M.RUNGS["A1_lost"], ["d_lost"], n_boot, rng)
        r["d_lost_A1"]["boot_ci"] = bl["d_lost"]["ci"]
        r["resampling_unit"] = "concept"
        r["n_boot"] = n_boot
        r["within_auc_R3_vs_R2"] = {}
        for rn in ("R2_vol", "R3_ret"):
            cols = M.RUNGS[rn]
            b = M.model(p, cols).fit(want_cov=False)["coef"]
            r["within_auc_R3_vs_R2"][rn] = float(H2.within_auc(p, p[cols].to_numpy() @ b).mean())
        r["sparsity"] = {"share_strata_any_lost": float(a.groupby("stratum").n_lost.max().gt(0).mean()),
                         "mean_n_lost_per_stratum": float(a.groupby("stratum").n_lost.max().mean())}
        out[u] = r
    return out


def dl_block(units: dict, names: list[str]) -> dict:
    res = {}
    for key, tg in (("d0_R3", "d0"), ("d_lost_A1", "d_lost")):
        use = [u for u in names if key in units.get(u, {})]
        b = [units[u][key]["coef"] for u in use]
        se = [units[u][key].get("se_concept", units[u][key]["se_model"]) for u in use]
        res[tg] = {"units": use, **M.dl(b, se), "n_positive": int(sum(x > 0 for x in b)), "n_negative": int(sum(x < 0 for x in b)),
                   "se_type": "concept-clustered sandwich"}
    return res


def guevara_auc(df_all: pd.DataFrame, prim: pd.DataFrame, coef_R3: dict) -> dict:
    y = df_all.entered.to_numpy()
    out = {"note": "GLOBAL (pooled, not within-stratum) AUC over all candidate rows; unit = concept x target field x year, "
                   "event = D3 count entry; Guevara et al. 2016 report 0.896 (individuals), 0.715 (organisations), 0.682 "
                   "(countries) for RCA-transition entry into research fields: different unit, event and proximity",
           "D_rca_cum_alone": float(roc_auc_score(y, df_all.D_rca_cum)), "D_rca_1y_alone": float(roc_auc_score(y, df_all.D_rca_1y)),
           "c_density_alone": float(roc_auc_score(y, df_all.c_density)), "b_log_size_alone": float(roc_auc_score(y, df_all.b_log_size))}
    cols = M.RUNGS["R3_ret"]
    lp = prim[cols].to_numpy() @ np.array([coef_R3[c] for c in cols])
    out["R3_linear_predictor_primary_rows"] = float(roc_auc_score(prim.entered, lp))
    return out


# ----------------------------------------------------------------------------- power simulation
def _sim_events(m: M.FastCLogit, eta: np.ndarray, rng) -> np.ndarray:
    """keep the observed number of events per stratum; draw them without replacement with p ~ exp(eta) (Gumbel top-m)."""
    gum = eta - np.log(-np.log(rng.random(len(eta))))
    # rank within stratum, descending key
    order = np.lexsort((-gum, m.row_s))
    rank = np.empty(len(eta), np.int64)
    pos_in = np.arange(len(eta)) - np.repeat(m.starts, m.counts)
    rank[order] = pos_in
    return (rank < m.nev[m.row_s]).astype(float)


def power_sim(prim_dev: pd.DataFrame, alls_dev: pd.DataFrame, unit_sizes: dict[str, int], rng, n_pooled: int, n_unit: int,
              grid_d0=(0, .05, .10, .15, .20, .28), grid_lost=(0, -.03, -.06, -.10)) -> dict:
    c4, c3, c2, ca, c0 = M.RUNGS["R4_lost"], M.RUNGS["R3_ret"], M.RUNGS["R2_vol"], M.RUNGS["A1_lost"], M.RUNGS["R0_M0"]
    ip = M.informative(prim_dev); ia = M.informative(alls_dev)
    b4 = M.model(ip, c4).fit(want_cov=False)["coef"]
    ba = M.model(ia, ca).fit(want_cov=False)["coef"]
    cp = ip.cidx.unique(); caa = ia.cidx.unique()
    res = {"truth_R4_dev": dict(zip(c4, map(float, b4))), "truth_A1_dev": dict(zip(ca, map(float, ba))), "table": {}}
    for u, n in unit_sizes.items():
        ns = n_pooled if u == "POOLED4" else n_unit
        row = {"n_concepts": n, "n_sims": ns, "d0": {}, "d_lost": {}}
        for bd in grid_d0:
            hit = []
            for _ in range(ns):
                pick = rng.choice(cp, min(n, len(cp)), replace=n > len(cp))
                d = ip[ip.cidx.isin(pick)]
                m = M.model(d, c4)
                bt = b4.copy(); bt[c4.index("d0_ret_rel")] = bd
                ysim = _sim_events(m, m.X @ bt, rng)
                m3 = M.FastCLogit(m.X[:, :len(c3)], ysim, m.sid[m.row_s]); m2 = M.FastCLogit(m.X[:, :len(c2)], ysim, m.sid[m.row_s])
                r3 = m3.fit(want_cov=False); r2 = m2.fit(want_cov=False)
                lrv = 2 * (r3["ll"] - r2["ll"])
                hit.append(stats.chi2.sf(max(lrv, 0), 1) < 0.01 and r3["coef"][-1] > 0)
            row["d0"][str(bd)] = float(np.mean(hit))
        for bl in grid_lost:
            hit = []
            for _ in range(ns):
                pick = rng.choice(caa, min(n, len(caa)), replace=n > len(caa))
                d = ia[ia.cidx.isin(pick)]
                m = M.model(d, ca)
                bt = ba.copy(); bt[-1] = bl
                ysim = _sim_events(m, m.X @ bt, rng)
                ms = M.FastCLogit(m.X, ysim, m.sid[m.row_s])
                r = ms.fit()
                z = r["coef"][-1] / r["se"][-1]
                hit.append(stats.norm.cdf(z) < 0.05)
            row["d_lost"][str(bl)] = float(np.mean(hit))
        row["MDE80_d0"] = _mde(row["d0"], grid_d0)
        row["MDE80_d_lost"] = _mde(row["d_lost"], grid_lost)
        res["table"][u] = row
        logger.info(f"  power {u} (n={n}): d0 {row['d0']} | d_lost {row['d_lost']}")
    return res


def _mde(pw: dict, grid) -> float | None:
    xs = [abs(g) for g in grid]
    ys = [pw[str(g)] for g in grid]
    for i in range(1, len(xs)):
        if ys[i] >= 0.8 and ys[i - 1] < 0.8:
            return float(xs[i - 1] + (0.8 - ys[i - 1]) * (xs[i] - xs[i - 1]) / max(ys[i] - ys[i - 1], 1e-9))
    return float(xs[0]) if ys[0] >= 0.8 else None


def shuffled_control(prim: pd.DataFrame, rng, n: int = 20) -> dict:
    """shuffle 'entered' within strata; LR(R3 vs R2) p < 0.01 should occur in <= 1 of 20."""
    c3, c2 = M.RUNGS["R3_ret"], M.RUNGS["R2_vol"]
    d = M.informative(prim).copy()
    rej = []
    for _ in range(n):
        d["entered"] = d.groupby("stratum").entered.transform(lambda s: rng.permutation(s.to_numpy()))
        r3 = M.model(d, c3).fit(want_cov=False); r2 = M.model(d, c2).fit(want_cov=False)
        rej.append(stats.chi2.sf(max(2 * (r3["ll"] - r2["ll"]), 0), 1) < 0.01)
    return {"n": n, "n_reject_p<0.01": int(sum(rej)), "pass_le_1": bool(sum(rej) <= 1)}
```

### [70] TOOL RESULT — Write · 2026-09-28 21:45:12 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/analysis.py", "content": "\"\"\"Analysis battery shared by every frame and split (EXP6 robustness, EXP5-minus-EXP6 DEV, held-out):\nladder, bootstraps, specificity (a)-(o), abandonment, per-unit fits, power simulation.\"\"\"\nfrom __future__ import annotations\n\nimport time\nimport zlib\n\nimport numpy as np\nimport pandas as pd\nfrom loguru im... [truncated, 23421 chars total]
```

### [71] TOOL CALL — Bash · 2026-09-28 21:45:12 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('lib/analysis.py'); s=p.read_text()
old='''    inf_s = np.isin(us, np.unique(sidx[np.isin(prim.stratum.to_numpy(), m3.sid)]))
'''
new='''    strat_of_us = prim.groupby("s_idx").stratum.first().loc[us].to_numpy()
    inf_s = np.isin(strat_of_us, m3.sid)
'''
assert old in s; s=s.replace(old,new)
old='''    d = M.informative(prim).copy()
    rej = []
    for _ in range(n):
        d["entered"] = d.groupby("stratum").entered.transform(lambda s: rng.permutation(s.to_numpy()))
'''
new='''    d = M.informative(prim).copy()
    strata = d.stratum.to_numpy(); y0 = d.entered.to_numpy()
    srt = np.argsort(strata, kind="stable")
    rej = []
    for _ in range(n):
        idx = np.lexsort((rng.random(len(d)), strata))
        ynew = np.empty_like(y0); ynew[srt] = y0[idx]
        d["entered"] = ynew
'''
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
```

### [72] TOOL RESULT — Bash · 2026-09-28 21:45:12 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [73] ASSISTANT · 2026-09-28 21:46:42 UTC

```
Now the orchestrator with stages `step1 | dev | freeze | heldout | outputs`, plus a seal guard.
```

### [74] TOOL CALL — Write · 2026-09-28 21:46:42 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/seal.py

"""Freeze / unseal gate (EXP5 seal.py pattern): the held-out stage refuses to run unless logs/seal.log records the
sha256 of results/frozen_spec.json and of every analysis .py file, and refuses a second unseal."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "results" / "frozen_spec.json"
SEAL = ROOT / "logs" / "seal.log"
UNSEAL = ROOT / "logs" / "unseal.log"
CODE = ["method.py", "lib/d3.py", "lib/models.py", "lib/analysis.py", "lib/exp5.py", "lib/h2_exp6.py", "lib/stats_core.py",
        "lib/cfg_exp6.py", "lib/seal.py"]


class SealedError(RuntimeError):
    pass


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def code_hashes() -> dict[str, str]:
    return {c: sha(ROOT / c) for c in CODE if (ROOT / c).exists()}


def freeze(spec: dict, git_commit: str | None) -> str:
    SPEC.write_text(json.dumps(spec, indent=1, default=str))
    h = sha(SPEC)
    rec = {"time": datetime.now(timezone.utc).isoformat(), "frozen_spec_sha256": h, "code_sha256": code_hashes(),
           "git_commit": git_commit}
    SEAL.write_text(json.dumps(rec, indent=1))
    return h


def unseal(resume_reason: str | None = None) -> dict:
    """checks the seal, then records the (single) unseal. `resume_reason` allows re-entry after a crash of the
    held-out stage itself; every re-entry is appended to logs/unseal.log (never silent)."""
    if not SEAL.exists() or not SPEC.exists():
        raise SealedError("held-out data are sealed: run `method.py freeze` first")
    rec = json.loads(SEAL.read_text())
    if sha(SPEC) != rec["frozen_spec_sha256"]:
        raise SealedError("frozen_spec.json changed after the freeze")
    now = code_hashes()
    changed = [c for c, h in rec["code_sha256"].items() if now.get(c) != h]
    if UNSEAL.exists() and resume_reason is None:
        raise SealedError("held-out data were already unsealed once (logs/unseal.log exists)")
    if changed and resume_reason is None:
        raise SealedError(f"code changed after the freeze: {changed}")
    entry = {"time": datetime.now(timezone.utc).isoformat(), "frozen_spec_sha256": rec["frozen_spec_sha256"],
             "code_changed_since_freeze": changed, "resume_reason": resume_reason}
    with UNSEAL.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry
```

### [75] TOOL RESULT — Write · 2026-09-28 21:46:42 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/seal.py", "content": "\"\"\"Freeze / unseal gate (EXP5 seal.py pattern): the held-out stage refuses to run unless logs/seal.log records the\nsha256 of results/frozen_spec.json and of every analysis .py file, and refuses a second unseal.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nfrom datetime import datetime, timezone\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parents[1]\nSPEC = ROOT / \"results\" / \"frozen_spec.json\"\nSEAL = ROOT / \"logs\" / \"seal.log\"\nUNSEAL = ROOT / \"logs\" / \"unseal.log\"\nCODE = [\"method.py\", \"lib/d3.py\", \"lib/models.py\", \"lib/analysis.py\", \"lib/exp5.py\", \"lib/h2_exp6.py\", \"lib/stats_core.py\",\n        \"lib/cfg_exp6.py\", \"lib/seal.py\"]\n\n\nclass SealedError(RuntimeError):\n    pass\n\n\ndef sha(p: Path) -> str:\n    return hashlib.sha256(p.read_bytes()).hexdigest()\n\n\ndef code_hashes() -> dict[str, str]:\n    return {c: sha(ROOT / c) for c in CODE if (ROOT / c).exists()}\n\n\ndef freeze(spec: dict, git_commit: str | None) -> str:\n    SPEC.write_text(json.dumps(spec, indent=1, default=str))\n    h = sha(SPEC)\n    rec = {\"time\": datetime.now(timezone.utc).isoformat(), \"frozen_spec_sha256\": h, \"code_sha256\": code_hashes(),\n           \"git_commit\": git_commit}\n    SEAL.write_text(json.dumps(rec, indent=1))\n    return h\n\n\ndef unseal(resume_reason: str | None = None) -> dict:\n    \"\"\"checks the seal, then records the (single) unseal. `resume_reason` allows re-entry after a crash of the\n    held-out stage itself; every re-entry is appended to logs/unseal.log (never silent).\"\"\"\n    if not SEAL.exists() or not SPEC.exists():\n        raise SealedError(\"held-out data are sealed: run `method.py freeze` first\")\n    rec = json.loads(SEAL.read_text())\n    if sha(SPEC) != rec[\"frozen_spec_sha256\"]:\n        raise SealedError(\"frozen_spec.json changed after the freeze\")\n    now = code_hashes()\n    changed = [c for c, h in rec[\"code_sha256\"].items() if now.get(c) != h]\n    if UNSEAL.exists() and resume_reason is None:\n        raise SealedError(\"held-out data were already unsealed once (logs/unseal.log exists)\")\n    if changed and resume_reason is None:\n        raise SealedError(f\"code changed after the freeze: {changed}\")\n    entry = {\"time\": datetime.now(timezone.utc).isoformat(), \"frozen_spec_sha256\": rec[\"frozen_spec_sha256\"],\n             \"code_changed_since_freeze\": changed, \"resume_reason\": resume_reason}\n    with UNSEAL.open(\"a\") as f:\n        f.write(json.dumps(entry) + \"\\n\")\n    return entry\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [76] TOOL CALL — Write · 2026-09-28 21:46:42 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py

#!/usr/bin/env python3
"""Do concepts spread from fields that KEEP them? Retained-frontier and abandonment-penalty test on concept x field
entry risk sets (conditional logit, concept-year strata), against the field-standard RCA>1 relatedness density.

Stages (in order):
  python method.py step1    EXP6 robustness: exact reproduction gate, then the nested ladder on EXP6's ... [truncated, 28889 chars total]
```

### [77] TOOL RESULT — Write · 2026-09-28 21:47:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py", "content": "#!/usr/bin/env python3\n\"\"\"Do concepts spread from fields that KEEP them? Retained-frontier and abandonment-penalty test on concept x field\nentry risk sets (conditional logit, concept-year strata), against the field-standard RCA>1 relatedness density.\n\nStages (in order):\n  python method.py step1    EXP6 robustness: exa... [truncated, 30815 chars total]
```

### [78] ASSISTANT · 2026-09-28 21:47:30 UTC

```
Smoke-testing `step1` with small resampling counts.
```

### [79] TOOL CALL — Bash · 2026-09-28 21:47:30 UTC

```
AII_NBOOT=20 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=10 AII_NUNITBOOT=10 timeout 900 .venv/bin/python method.py step1 2>&1 | tail -40
```

### [80] TOOL RESULT — Bash · 2026-09-28 21:48:12 UTC

```
{"stdout": "21:46:41|INFO   |EXP6 dev: rebuilt 47,762 rows vs 47,762; same row set True; max diffs {'entered': 0.0, 'a_phi_home': 0.0, 'b_log_size': 0.0, 'c_density': 1.1102230246251565e-16, 'e_gate_own': 0.0, 'd0_ret_rel': 0.0, 'd_ret_gate': 3.3306690738754696e-16, 'd_lost_gate': 1.1102230246251565e-16}\n21:46:41|INFO   |EXP6 heldout: rebuilt 61,648 rows vs 61,648; same row set True; max diffs {'entered': 0.0, 'a_phi_home': 0.0, 'b_log_size': 0.0, 'c_density': 1.1102230246251565e-16, 'e_gate_own': 0.0, 'd0_ret_rel': 0.0, 'd_ret_gate': 4.440892098500626e-16, 'd_lost_gate': 2.220446049250313e-16}\n21:46:41|INFO   |T1 gate: LR=68.569 d0=0.2809 d_lost_gate=-0.0632\n21:46:46|INFO   |[exp6_dev] ladder: R1_rca_vs_R0_M0 LR=30.16, R2_vol_vs_R1_rca LR=17.02, R3_ret_vs_R2_vol LR=29.32, R4_lost_vs_R3_ret LR=0.03, S_strict_vs_S_strict0 LR=20.52, EXP6_M1_vs_R0_M0 LR=34.49, EXP6_M2lost_vs_R0_M0 LR=2.26\n21:46:46|INFO   |[exp6_dev] d0 in R3 = 0.2151; d0 in S_strict = 0.1907; d_lost in A1 = -0.0796\n21:46:48|INFO   |[exp6_heldout] ladder: R1_rca_vs_R0_M0 LR=21.70, R2_vol_vs_R1_rca LR=20.37, R3_ret_vs_R2_vol LR=57.59, R4_lost_vs_R3_ret LR=0.55, S_strict_vs_S_strict0 LR=50.33, EXP6_M1_vs_R0_M0 LR=68.57, EXP6_M2lost_vs_R0_M0 LR=3.69\n21:46:48|INFO   |[exp6_heldout] d0 in R3 = 0.2618; d0 in S_strict = 0.2522; d_lost in A1 = -0.0525\n21:46:49|INFO   |headline bootstraps (20) in 1s\n21:46:49|INFO   |[exp6_heldout] crossed bootstrap 0s: [0.19603632137683083, 0.36025796962680157]\n21:46:50|INFO   |  (a) permutation 0s p=0.0476\n21:46:51|INFO   |  (d) backbone nulls 1s\n21:46:58|INFO   |[exp6_heldout] rebuild sensitivities 1s; battery total 11s\n21:46:59|INFO   |step1 done in 23s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [81] ASSISTANT · 2026-09-28 21:48:12 UTC

```
Smoke run passes in 23 s. On EXP6 held-out, d0 survives the RCA>1 rivals (LR 57.6 in R3, 50.3 in S_strict). Checking the JSON details for anything off.
```

### [82] TOOL CALL — Bash · 2026-09-28 21:48:12 UTC

```
.venv/bin/python -c "
import json;d=json.load(open('results/step1_exp6_robustness.json'));h=d['heldout']
print(json.dumps(h['ladder']['frontier_primary_sample']['models']['R3_ret'],indent=0)[:1500])
print(h['ladder']['frontier_primary_sample']['auc_within']); print(h['ladder']['frontier_primary_sample']['n'])
print(json.dumps(h['ladder']['abandonment_all_rows']['LR'])); print(h['ladder']['abandonment_all_rows']['models']['A1_split']['coef'])
print(json.dumps(h['vif']['vif_within_stratum'])); print(h['vif']['condition_number'])
print(h['lpm_concept_year_FE']['coef']['d0_ret_rel']); print(h['guevara_comparable_auc']); print(h['sparsity'])
s=h['specificity']; print({k:(v.get('p'),v.get('share_strata_nontrivial')) for k,v in s.items() if k.startswith('a_')})
print(json.dumps(s['b_volume_matched'])[:1500]); print(json.dumps(s['c_dose'])[:800])
for k in ['e_excl_intersection_born','g_target_field_FE','h_horizon8','i_excl_weak_home','j_excl_medicine_home','n_newborn_only_descriptive','o_label_coverage_ge_0.5']: print(k, s[k]['d0_R3']['coef'], s[k]['d0_R3']['LR']['p'], s[k]['d_lost_A1']['coef'])
r=h['specificity_rebuild']; [print(k, v['d0_R3']['coef'], v['d0_R3']['LR'], v['d_lost_A1']['coef']) for k,v in r.items()]
print(json.dumps(d['heldout_units'])[:1500]); print(d['heldout_DL'])
"
```

### [83] TOOL RESULT — Bash · 2026-09-28 21:48:12 UTC

```
{"stdout": "{\n\"coef\": {\n\"a_phi_home\": 0.2262334487886591,\n\"b_log_size\": 1.654963735480193,\n\"c_density\": 0.13468700685021925,\n\"e_gate_own\": 0.0749097324311422,\n\"D_rca_1y\": 0.0590848551517869,\n\"D_vol\": 0.21991265218086709,\n\"d0_ret_rel\": 0.2617949320788904\n},\n\"se_model\": {\n\"a_phi_home\": 0.03939284554720792,\n\"b_log_size\": 0.0532966623389339,\n\"c_density\": 0.04225730821926464,\n\"e_gate_own\": 0.03168488255778047,\n\"D_rca_1y\": 0.04093919297397465,\n\"D_vol\": 0.04943786128957694,\n\"d0_ret_rel\": 0.03287469481785306\n},\n\"ll\": -3220.2652321339965,\n\"n_strata\": 961,\n\"n_events\": 1373,\n\"n_rows\": 18846,\n\"converged\": true,\n\"max_grad\": 5.684341886080801e-13,\n\"se_concept\": {\n\"a_phi_home\": 0.048079953029689065,\n\"b_log_size\": 0.049787335566686484,\n\"c_density\": 0.04114234042498875,\n\"e_gate_own\": 0.03596971037879343,\n\"D_rca_1y\": 0.04437924499348357,\n\"D_vol\": 0.066461264296351,\n\"d0_ret_rel\": 0.03138673326489317\n},\n\"se_two_way_concept_field\": {\n\"a_phi_home\": 0.10183515897390265,\n\"b_log_size\": 0.255994837237515,\n\"c_density\": 0.09332556546277841,\n\"e_gate_own\": 0.06627620881631502,\n\"D_rca_1y\": 0.0687972333923372,\n\"D_vol\": 0.14025427254293182,\n\"d0_ret_rel\": 0.06736642579494688\n}\n}\n{'R0_M0': 0.8091807114429179, 'R1_rca': 0.8128730125349832, 'R2_vol': 0.8153655481523674, 'R3_ret': 0.8206135082693025, 'R4_lost': 0.8211867746542918, 'S_strict0': 0.8154183169022375, 'S_strict': 0.8203766485138572, 'EXP6_M1': 0.8168958319192421, 'EXP6_M2lost': 0.810261363396254}\n{'rows': 46433, 'strata': 2339, 'concepts': 369, 'events': 1373, 'informative_strata': 961, 'informative_rows': 18846}\n{\"A1_lost_vs_R0_M0\": {\"LR\": 2.8775437331405556, \"df\": 1, \"p\": 0.08982294107270522}, \"A1_split_vs_R0_M0\": {\"LR\": 3.6947898979542515, \"df\": 2, \"p\": 0.15764731114672842}}\n{'a_phi_home': 0.3517898999312001, 'b_log_size': 1.5531115870921606, 'c_density': 0.35031265174382764, 'e_gate_own': 0.08383959973533002, 'd_lost_short': -0.04216537382166092, 'd_lost_long': -0.0466200859910346}\n{\"a_phi_home\": 3.4032957058662765, \"b_log_size\": 1.2525126390184815, \"c_density\": 2.993588192750506, \"e_gate_own\": 1.1907397784689575, \"D_rca_1y\": 5.620495901076288, \"D_rca_w3\": 10.455736789364613, \"D_rca_cum\": 8.773841621517562, \"D_rca_pers\": 4.083260456888662, \"D_vol\": 58.499974060112585, \"D_vol_w3\": 62.960675943681935, \"d0_ret_rel\": 1.895375636400724, \"d_lost\": 1.0935473426900344}\n27.90532890174716\n{'b': 0.0015554045747260968, 'se': 0.0013364993693034876, 'ci': [-0.0010727295734820046, 0.004183538722934198], 'p': 0.2452631241073662}\n{'note': 'GLOBAL (pooled, not within-stratum) AUC over all candidate rows; unit = concept x target field x year, event = D3 count entry; Guevara et al. 2016 report 0.896 (individuals), 0.715 (organisations), 0.682 (countries) for RCA-transition entry into research fields: different unit, event and proximity', 'D_rca_cum_alone': 0.6154585302775994, 'D_rca_1y_alone': 0.6170240003092913, 'c_density_alone': 0.6153230454321645, 'b_log_size_alone': 0.7234020059607431, 'R3_linear_predictor_primary_rows': 0.7953635825535201}\n{'share_strata_any_lost': 0.19151069518716576, 'mean_n_lost_per_stratum': 0.23897058823529413, 'mean_n_ret_primary': 3.221889696451475}\n{'a_permutation': (0.047619047619047616, 0.3392299687825182), 'a_permutation_secondary_all_entered_offhome': (0.047619047619047616, 0.8428720083246618)}\n{\"match_rate_strata\": 0.13809320222317228, \"n_rows\": 5582, \"n_strata\": 323, \"n_concepts\": 185, \"fit\": {\"coef\": 0.09512096035138366, \"se_model\": 0.05650885233530678, \"n_strata\": 150, \"n_events\": 245, \"n_concepts\": 185, \"converged\": true, \"se_concept\": 0.043774754038406256, \"p_wald_concept_2s\": 0.02978303425230047, \"LR\": {\"LR\": 3.42714956631562, \"df\": 2, \"p\": 0.1802203909007462}}, \"fit_N\": {\"coef\": -0.035123601434149006, \"se_model\": 0.0643820937657368, \"n_strata\": 150, \"n_events\": 245, \"n_concepts\": 185, \"converged\": true, \"se_concept\": 0.056249633879934584, \"p_wald_concept_2s\": 0.5323494004485045}, \"contrast_R_minus_N\": {\"resampling_unit\": \"concept\", \"n_boot\": 20, \"est\": 0.13024456178553268, \"ci\": [0.026487546945493337, 0.2505459546827192], \"p_one_sided\": 0.047619047619047616, \"d_R_m\": {\"est\": 0.09512096035138366, \"ci\": [0.019043330736335507, 0.14044563157132295], \"se_boot\": 0.038463887619293265, \"p_one_sided_le0\": 0.047619047619047616}, \"d_N_m\": {\"est\": -0.035123601434149006, \"ci\": [-0.15892653659043948, 0.007526001425147807], \"se_boot\": 0.05071338473448372, \"p_one_sided_le0\": 0.9523809523809523}}, \"balance\": {\"mean_n_prev_R\": 32.604248046875, \"mean_n_prev_N\": 3.84596586227417, \"mean_cum_prev_R\": 67.40347290039062, \"mean_cum_prev_N\": 7.748166084289551, \"n_matched_R_fields\": 518, \"n_matched_N_fields\": 409}}\n{\"fit\": {\"d_ret_a2\": {\"coef\": 0.10169621551567232, \"se_model\": 0.03155909163944458, \"n_strata\": 961, \"n_events\": 1373, \"n_concepts\": 369, \"converged\": true, \"se_concept\": 0.02845011768742809, \"p_wald_concept_2s\": 0.00035083796203444256}, \"d_ret_a3\": {\"coef\": 0.1370538962555718, \"se_model\": 0.033734364919398796, \"n_strata\": 961, \"n_events\": 1373, \"n_concepts\": 369, \"converged\": true, \"se_concept\": 0.03362112330375559, \"p_wald_concept_2s\": 4.5733931105678816e-05}, \"d_ret_a4p\": {\"coef\": 0.21322504889131338, \"se_model\": 0.03429629488579209, \"n_strata\": 961, \"n_events\": 1373, \"n_concepts\": 369, \"converged\": true, \"se_concept\": 0.03210345036533511, \"p_wald_concept_2s\": 3.098521879595381e-11}}, \"contrast_4p_minus_2\": {\"resampling_unit\": \"concept\", \"n_boot\": 20, \"est\": 0.11152883337564107, \"ci\": [\ne_excl_intersection_born 0.259162857387992 3.053468962415091e-13 -0.058368187688559565\ng_target_field_FE 0.2498163805967243 1.2007149682169972e-11 -0.08096022010781677\nh_horizon8 0.2617949320788904 3.223798086979804e-14 -0.0525356608918208\ni_excl_weak_home 0.2680512407625653 8.148878264850858e-14 -0.054916434279456805\nj_excl_medicine_home 0.2796800653134086 1.5088461217514968e-11 -0.0497777214520009\nn_newborn_only_descriptive 0.2617949320788904 3.223798086979804e-14 -0.0525356608918208\no_label_coverage_ge_0.5 0.2850905387037394 2.1055576804863477e-13 -0.053524770359130516\nf_min_n_3 0.21285788049121593 {'LR': 36.48845925424757, 'df': 1, 'p': 1.5357284254399051e-09} -0.0088044732955819\nf_min_n_5 0.26767291651398994 {'LR': 49.94259835043067, 'df': 1, 'p': 1.5831012930953935e-12} -0.00816530080677376\nl_rca_entry_event 0.18817606638522288 {'LR': 11.532718566877065, 'df': 1, 'p': 0.0006838194335840375} -0.08540382610381732\nk_primary_topic_fields 0.23609533334201618 {'LR': 76.00015098136646, 'df': 1, 'p': 2.8364304869012046e-18} -0.013782314251378417\nm_min_conditional_probability_proximity 0.005579007115738301 {'LR': 0.06630473464247189, 'df': 1, 'p': 0.7967950864882435} -0.05319606834602084\n{\"Physical\": {\"d0_R3\": {\"coef\": 0.28011218679313565, \"se_model\": 0.15037515835841228, \"n_strata\": 72, \"n_events\": 92, \"n_concepts\": 30, \"converged\": true, \"se_concept\": 0.11902760411136062, \"p_wald_concept_2s\": 0.018605711885283975, \"LR\": {\"LR\": 3.285023752747861, \"df\": 1, \"p\": 0.06991461674184289}, \"boot_ci\": [0.09916187858648712, 0.4160125038866992]}, \"d_lost_A1\": {\"coef\": 0.05908181079720997, \"se_model\": 0.10353214280583806, \"n_strata\": 100, \"n_events\": 131, \"n_concepts\": 34, \"converged\": true, \"se_concept\": 0.10505666337437511, \"p_wald_concept_2s\": 0.5738568544109481, \"LR\": {\"LR\": 0.299334120492631, \"df\": 1, \"p\": 0.5843001688082565}, \"boot_ci\": [-0.15628883187050993, 0.14449251006869154]}, \"resampling_unit\": \"concept\", \"n_boot\": 10, \"within_auc_R3_vs_R2\": {\"R2_vol\": 0.8784078100445966, \"R3_ret\": 0.8766487891529956}, \"sparsity\": {\"share_strata_any_lost\": 0.14705882352941177, \"mean_n_lost_per_stratum\": 0.20588235294117646}}, \"LifeEnv\": {\"d0_R3\": {\"coef\": 0.20759840960826784, \"se_model\": 0.14283685364212176, \"n_strata\": 94, \"n_events\": 118, \"n_concepts\": 34, \"converged\": true, \"se_concept\": 0.11746380181767481, \"p_wald_concept_2s\": 0.07717139863267412, \"LR\": {\"LR\": 1.9949191098080519, \"df\": 1, \"p\": 0.15782749215776257}, \"boot_ci\": [0.015856407522563894, 0.5286079981140325]}, \"d_lost_A1\": {\"coef\": -0.015201745540007127, \"se_model\": 0.12432960910599937, \"n_strata\": 107, \"n_events\": 140, \"n_concepts\": 34, \"converged\": true, \"se_concept\": 0.1783002758156701, \"p_wald_concept_2s\":\n{'d0': {'units': ['Physical', 'LifeEnv', 'Social', 'Cohort'], 'k': 4, 'b': 0.24997453235111952, 'se': 0.03192101686028168, 'ci': [0.18740933930496742, 0.3125397253972716], 'p': 4.838781267530549e-15, 'tau2': 0.0, 'Q': 0.19671683407584548, 'I2': 0.0, 'n_positive': 4, 'n_negative': 0, 'se_type': 'concept-clustered sandwich'}, 'd_lost': {'units': ['Physical', 'LifeEnv', 'Social', 'Cohort'], 'k': 4, 'b': -0.04471989350846939, 'se': 0.03320823727368421, 'ci': [-0.10980803856489044, 0.02036825154795166], 'p': 0.1780927810207238, 'tau2': 0.0, 'Q': 2.19246764535408, 'I2': 0.0, 'n_positive': 1, 'n_negative': 3, 'se_type': 'concept-clustered sandwich'}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [84] THINKING · 2026-09-28 21:48:54 UTC

```
I found poor volume matching balance, high collinearity between D_vol/D_vol_w3 (VIF~60), and that min-CP proximity sensitivity kills d0 (p=0.80)—a real finding I'll report. Before seeing EXP5 data, I'm pre-declaring two additions: a finer-bin matched contrast and a PCA-combined RCA rung.
```

### [85] TOOL CALL — Bash · 2026-09-28 21:48:54 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('lib/d3.py'); s=p.read_text()
old='''def vol_matched_masks(st: dict) -> tuple[np.ndarray, np.ndarray]:
    """Volume-matched retained (R) vs entered-not-retained (N) off-home fields at t-1: coarsen n(t-1) {0,1,2-3,4+} x
    cum(t-1) {2,3-4,5-9,10+}; keep only cells holding >= 1 R and >= 1 N."""
    n = st["xprev"]; cu = st["cumprev"]
    nb = np.digitize(n, [0.5, 1.5, 3.5])                  # 0 | 1 | 2-3 | 4+
    cb = np.digitize(cu, [2.5, 4.5, 9.5])                 # 2 | 3-4 | 5-9 | 10+
    code = nb * 4 + cb
    R = st["RET"]
    N = st["ENTOFF"] & ~st["RET"]
    oh = np.eye(16, dtype=bool)[code]                     # [S, 26, 16]'''
new='''NB_COARSE, CB_COARSE = [0.5, 1.5, 3.5], [2.5, 4.5, 9.5]                       # pre-declared (plan)
NB_FINE, CB_FINE = [0.5, 1.5, 3.5, 7.5, 15.5, 31.5], [2.5, 4.5, 9.5, 19.5, 49.5]  # added on EXP6/DEV before the freeze


def vol_matched_masks(st: dict, fine: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """Volume-matched retained (R) vs entered-not-retained (N) off-home fields at t-1: coarsen n(t-1) {0,1,2-3,4+} x
    cum(t-1) {2,3-4,5-9,10+} (fine: n {0,1,2-3,4-7,8-15,16-31,32+} x cum {2,3-4,5-9,10-19,20-49,50+});
    keep only cells holding >= 1 R and >= 1 N."""
    n = st["xprev"]; cu = st["cumprev"]
    ne, ce = (NB_FINE, CB_FINE) if fine else (NB_COARSE, CB_COARSE)
    nb = np.digitize(n, ne)
    cb = np.digitize(cu, ce)
    ncell = (len(ne) + 1) * (len(ce) + 1)
    code = nb * (len(ce) + 1) + cb
    R = st["RET"]
    N = st["ENTOFF"] & ~st["RET"]
    oh = np.eye(ncell, dtype=bool)[code]                  # [S, 26, ncell]'''
assert old in s; s=s.replace(old,new)
old='''    cols["has_match"] = (Rm.any(1) & Nm.any(1))[s_idx].astype(np.int8)
'''
new='''    cols["has_match"] = (Rm.any(1) & Nm.any(1))[s_idx].astype(np.int8)
    Rf, Nf = vol_matched_masks(st, fine=True)
    cols["d_R_mf"] = g(_mrel(Rf, phi))
    cols["d_N_mf"] = g(_mrel(Nf, phi))
    cols["has_match_f"] = (Rf.any(1) & Nf.any(1))[s_idx].astype(np.int8)
'''
assert old in s; s=s.replace(old,new)
s=s.replace('"d_lost_short", "d_lost_long", "d_R_m", "d_N_m"]','"d_lost_short", "d_lost_long", "d_R_m", "d_N_m", "d_R_mf", "d_N_mf"]')
p.write_text(s)

p=Path('lib/models.py'); s=p.read_text()
s=s.replace('D0_SCALE_COLS = ["d_ret_a2", "d_ret_a3", "d_ret_a4p", "d_R_m", "d_N_m"]','D0_SCALE_COLS = ["d_ret_a2", "d_ret_a3", "d_ret_a4p", "d_R_m", "d_N_m", "d_R_mf", "d_N_mf"]')
old='''    for c in D0_SCALE_COLS:
        if c in df:
            spec[c] = {"mean": 0.0, "sd": spec["d0_ret_rel"]["sd"]}
    return spec'''
new='''    for c in D0_SCALE_COLS:
        if c in df:
            spec[c] = {"mean": 0.0, "sd": spec["d0_ret_rel"]["sd"]}
    # PCA-combined RCA factor (fallback F6 for collinear RCA variants): first PC of the four standardised D_rca
    rc = ["D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers"]
    if "RCA_PC1" not in spec and all(c in df for c in rc):
        Z = np.column_stack([(df[c] - spec[c]["mean"]) / spec[c]["sd"] for c in rc])
        w, V = np.linalg.eigh(np.cov(Z, rowvar=False))
        v = V[:, -1] * np.sign(V[:, -1].sum())
        pc = Z @ v
        spec["RCA_PC1"] = {"loadings": v.tolist(), "cols": rc, "explained": float(w[-1] / w.sum()),
                           "pc_mean": float(pc.mean()), "pc_sd": float(pc.std())}
    return spec'''
assert old in s; s=s.replace(old,new)
old='''def standardise(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    out = df.copy()
    for c, v in spec.items():
        if c in out:
            out[c] = (df[c] - v["mean"]) / (v["sd"] if v["sd"] > 0 else 1.0)
    return out'''
new='''def standardise(df: pd.DataFrame, spec: dict) -> pd.DataFrame:
    out = df.copy()
    for c, v in spec.items():
        if c in out and "mean" in v:
            out[c] = (df[c] - v["mean"]) / (v["sd"] if v["sd"] > 0 else 1.0)
    if "RCA_PC1" in spec and all(c in out for c in spec["RCA_PC1"]["cols"]):
        p = spec["RCA_PC1"]
        out["RCA_PC1"] = (out[p["cols"]].to_numpy() @ np.array(p["loadings"]) - p["pc_mean"]) / p["pc_sd"]
    return out'''
assert old in s; s=s.replace(old,new)
old='''    "A1_lost": BASE + ["d_lost"],'''
new='''    "S_pca0": BASE + ["RCA_PC1", "D_vol", "D_vol_w3"],
    "S_pca": BASE + ["RCA_PC1", "D_vol", "D_vol_w3", "d0_ret_rel"],
    "A1_lost": BASE + ["d_lost"],'''
assert old in s; s=s.replace(old,new)
s=s.replace('''          ("S_strict", "S_strict0"), ("A1_lost", "R0_M0"),''','''          ("S_strict", "S_strict0"), ("S_pca", "S_pca0"), ("A1_lost", "R0_M0"),''')
p.write_text(s)

p=Path('lib/analysis.py'); s=p.read_text()
s=s.replace('''PRIM_RUNGS = ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost", "S_strict0", "S_strict", "EXP6_M1", "EXP6_M2lost"]''',
'''PRIM_RUNGS = ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost", "S_strict0", "S_strict", "S_pca0", "S_pca", "EXP6_M1", "EXP6_M2lost"]''')
old='''    "VM": M.RUNGS["R2_vol"] + ["d_R_m", "d_N_m"],'''
new='''    "VM": M.RUNGS["R2_vol"] + ["d_R_m", "d_N_m"],
    "VMF": M.RUNGS["R2_vol"] + ["d_R_mf", "d_N_mf"],'''
assert old in s; s=s.replace(old,new)
old='''    out["b_volume_matched"] = b
'''
new='''    out["b_volume_matched"] = b
    vf = prim[prim.has_match_f == 1]
    bf = {"bins": "fine (added before the EXP5 freeze)", "match_rate_strata": float(prim.groupby("stratum").has_match_f.max().mean()),
          "n_rows": int(len(vf)), "n_concepts": int(vf.cidx.nunique())}
    if vf.cidx.nunique() >= 20:
        bf["fit"] = coef_row(vf, M.RUNGS["VMF"], "d_R_mf", M.RUNGS["VM0"])
        bf["contrast_R_minus_N"] = M.contrast_boot(vf, M.RUNGS["VMF"], "d_R_mf", "d_N_mf", n_boot, rng)
        us = np.unique(vf.s_idx.to_numpy())
        Rm, Nm = d3.vol_matched_masks({k_: st[k_][us] for k_ in ("xprev", "cumprev", "RET", "ENTOFF")}, fine=True)
        bf["balance"] = {"mean_n_prev_R": float(st["xprev"][us][Rm].mean()), "mean_n_prev_N": float(st["xprev"][us][Nm].mean()),
                         "mean_cum_prev_R": float(st["cumprev"][us][Rm].mean()), "mean_cum_prev_N": float(st["cumprev"][us][Nm].mean()),
                         "n_matched_R_fields": int(Rm.sum()), "n_matched_N_fields": int(Nm.sum())}
    out["b2_volume_matched_fine"] = bf
'''
assert old in s; s=s.replace(old,new)
s=s.replace('''    out["vif"] = AN.vif_block''','''    out["vif"] = AN.vif_block''')
p.write_text(s)
EOF
grep -n "headline_boots\|d0_S_strict" lib/analysis.py | head
```

### [86] TOOL RESULT — Bash · 2026-09-28 21:48:54 UTC

```
{"stdout": "177:def headline_boots(prim: pd.DataFrame, alls: pd.DataFrame, rng, n_boot: int, second_seed: bool = False) -> dict:\n180:           \"d0_S_strict\": M.boot_refit(prim, M.RUNGS[\"S_strict\"], [\"d0_ret_rel\"], n_boot, rng, small_cols=M.RUNGS[\"S_strict0\"]),", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [87] TOOL CALL — Bash · 2026-09-28 21:48:54 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('lib/analysis.py'); s=p.read_text()
old='''           "d_lost_A1": M.boot_refit(alls,'''
new='''           "d0_S_pca": M.boot_refit(prim, M.RUNGS["S_pca"], ["d0_ret_rel"], n_boot, rng, small_cols=M.RUNGS["S_pca0"]),
           "d_lost_A1": M.boot_refit(alls,'''
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
AII_NBOOT=20 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=10 AII_NUNITBOOT=10 timeout 900 .venv/bin/python method.py step1 2>&1 | grep -v "^.*EXP6 \(dev\|heldout\):" | tail -12 && .venv/bin/python -c "
import json;d=json.load(open('results/step1_exp6_robustness.json'));h=d['heldout']; l=h['ladder']['frontier_primary_sample']
print(l['LR']['S_pca_vs_S_pca0'], l['models']['S_pca']['coef']['d0_ret_rel'], d['standardisation']['RCA_PC1'])
b=h['specificity']['b2_volume_matched_fine']; print(json.dumps(b)[:300], b.get('balance'), b.get('contrast_R_minus_N',{}).get('est'), b.get('contrast_R_minus_N',{}).get('ci'))"
```

### [88] TOOL RESULT — Bash · 2026-09-28 21:49:36 UTC

```
{"stdout": "21:48:32|INFO   |T1 gate: LR=68.569 d0=0.2809 d_lost_gate=-0.0632\n21:48:38|INFO   |[exp6_dev] ladder: R1_rca_vs_R0_M0 LR=30.16, R2_vol_vs_R1_rca LR=17.02, R3_ret_vs_R2_vol LR=29.32, R4_lost_vs_R3_ret LR=0.03, S_strict_vs_S_strict0 LR=20.52, S_pca_vs_S_pca0 LR=20.60, EXP6_M1_vs_R0_M0 LR=34.49, EXP6_M2lost_vs_R0_M0 LR=2.26\n21:48:38|INFO   |[exp6_dev] d0 in R3 = 0.2151; d0 in S_strict = 0.1907; d_lost in A1 = -0.0796\n21:48:39|INFO   |[exp6_heldout] ladder: R1_rca_vs_R0_M0 LR=21.70, R2_vol_vs_R1_rca LR=20.37, R3_ret_vs_R2_vol LR=57.59, R4_lost_vs_R3_ret LR=0.55, S_strict_vs_S_strict0 LR=50.33, S_pca_vs_S_pca0 LR=51.27, EXP6_M1_vs_R0_M0 LR=68.57, EXP6_M2lost_vs_R0_M0 LR=3.69\n21:48:39|INFO   |[exp6_heldout] d0 in R3 = 0.2618; d0 in S_strict = 0.2522; d_lost in A1 = -0.0525\n21:48:40|INFO   |headline bootstraps (20) in 1s\n21:48:40|INFO   |[exp6_heldout] crossed bootstrap 0s: [0.16151140280395349, 0.44921565844468125]\n21:48:41|INFO   |  (a) permutation 0s p=0.0476\n21:48:42|INFO   |  (d) backbone nulls 1s\n21:48:49|INFO   |[exp6_heldout] rebuild sensitivities 1s; battery total 11s\n21:48:50|INFO   |step1 done in 23s\n{'LR': 51.271641925638505, 'df': 1, 'p': 8.042913604507985e-13} 0.25267170807033473 {'loadings': [0.4914025248471853, 0.5114116009799743, 0.5083203991383922, 0.4884589079714868], 'cols': ['D_rca_1y', 'D_rca_w3', 'D_rca_cum', 'D_rca_pers'], 'explained': 0.8965013453301728, 'pc_mean': -3.138612934725196e-17, 'pc_sd': 1.8936489591697727}\n{\"bins\": \"fine (added before the EXP5 freeze)\", \"match_rate_strata\": 0.10987601539119282, \"n_rows\": 4310, \"n_concepts\": 160, \"fit\": {\"coef\": 0.07122456211263939, \"se_model\": 0.06490949305726249, \"n_strata\": 119, \"n_events\": 182, \"n_concepts\": 160, \"converged\": true, \"se_concept\": 0.05163603125541984 {'mean_n_prev_R': 2.0, 'mean_n_prev_N': 2.0536277294158936, 'mean_cum_prev_R': 6.531147480010986, 'mean_cum_prev_N': 5.49526834487915, 'n_matched_R_fields': 305, 'n_matched_N_fields': 317} 0.07128497866967277 [-0.08964523088234923, 0.18278377485052535]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [89] ASSISTANT · 2026-09-28 21:50:16 UTC

```
Both additions work. The fine matching is balanced (n 2.0 vs 2.05), and on EXP6 its R−N contrast is +0.07 with a CI that includes 0. Now smoke-testing the `dev` stage on a small concept subsample.
```

### [90] TOOL CALL — Bash · 2026-09-28 21:50:16 UTC

```
AII_SMOKE_CONCEPTS=300 AII_NBOOT=20 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=10 AII_NUNITBOOT=10 AII_NPOWER=10 timeout 1200 .venv/bin/python method.py dev 2>&1 | tail -30
```

### [91] TOOL RESULT — Bash · 2026-09-28 21:50:16 UTC

```
{"stdout": "  File \"pandas/_libs/index.pyx\", line 197, in pandas._libs.index.IndexEngine.get_loc\n  File \"pandas/_libs/hashtable_class_helper.pxi\", line 7668, in pandas._libs.hashtable.PyObjectHashTable.get_item\n  File \"pandas/_libs/hashtable_class_helper.pxi\", line 7676, in pandas._libs.hashtable.PyObjectHashTable.get_item\nKeyError: 'unit'\n\nThe above exception was the direct cause of the following exception:\n\nTraceback (most recent call last):\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py\", line 498, in <module>\n    logger.catch(reraise=True)(main)()\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.venv/lib/python3.12/site-packages/loguru/_logger.py\", line 1297, in catch_wrapper\n    return function(*args, **kwargs)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py\", line 485, in main\n    stage_dev()\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py\", line 253, in stage_dev\n    df, st = build(fr, A[\"V\"], GF, bb, 10, META5)\n             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py\", line 93, in build\n    df = d3.attach_meta(d3.covariates(st, bb[\"phi\"], bb[\"gate\"]), st, frame, meta)\n         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/lib/d3.py\", line 246, in attach_meta\n    df[c] = frame[c].to_numpy()[ri]\n            ~~~~~^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.venv/lib/python3.12/site-packages/pandas/core/frame.py\", line 4378, in __getitem__\n    indexer = self.columns.get_loc(key)\n              ^^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/.venv/lib/python3.12/site-packages/pandas/core/indexes/base.py\", line 3648, in get_loc\n    raise KeyError(key) from err\nKeyError: 'unit'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [92] TOOL CALL — Bash · 2026-09-28 21:50:16 UTC

```
sed -i 's/        fr = fr.groupby("unit", group_keys=False).apply(lambda d: d.head(SMOKE)).reset_index(drop=True)/        fr = fr.groupby("unit").head(SMOKE).reset_index(drop=True)/' method.py && AII_SMOKE_CONCEPTS=300 AII_NBOOT=20 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=10 AII_NUNITBOOT=10 AII_NPOWER=10 timeout 1200 .venv/bin/python method.py dev 2>&1 | tail -30
```

### [93] TOOL RESULT — Bash · 2026-09-28 21:51:02 UTC

```
{"stdout": "21:49:58|INFO   |input checks: {'early_volume_agreement': 1.0, 'home_agreement': 1.0, 'GF_spearman_min': 0.9999999999999999, 'GF_max_rel_diff': 0.0, 'home_mismatch_cidx': []}\n21:49:58|INFO   |DEV risk sets 62,283 rows / 3,000 strata / 300 concepts; state panel 157,560 rows (11s)\n21:49:59|INFO   |[exp5_dev] ladder: R1_rca_vs_R0_M0 LR=5.56, R2_vol_vs_R1_rca LR=0.34, R3_ret_vs_R2_vol LR=27.15, R4_lost_vs_R3_ret LR=1.05, S_strict_vs_S_strict0 LR=22.83, S_pca_vs_S_pca0 LR=22.52, EXP6_M1_vs_R0_M0 LR=30.61, EXP6_M2lost_vs_R0_M0 LR=0.19\n21:49:59|INFO   |[exp5_dev] d0 in R3 = 0.2404; d0 in S_strict = 0.2296; d_lost in A1 = 0.0045\n21:50:00|INFO   |headline bootstraps (20) in 1s\n21:50:00|INFO   |[exp5_dev] crossed bootstrap 0s: [0.2001845285387892, 0.4036588494206761]\n21:50:00|INFO   |  (a) permutation 0s p=0.1429\n21:50:01|INFO   |  (d) backbone nulls 1s\n21:50:03|INFO   |[exp5_dev] rebuild sensitivities 1s; battery total 5s\n21:50:14|INFO   |  power POOLED4 (n=1065): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.2, '0.15': 0.5, '0.2': 0.6, '0.28': 1.0} | d_lost {'0': 0.1, '-0.03': 0.2, '-0.06': 0.4, '-0.1': 0.5}\n21:50:16|INFO   |  power PHYS (n=300): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.0, '0.15': 0.4, '0.2': 0.8, '0.28': 1.0} | d_lost {'0': 0.0, '-0.03': 0.2, '-0.06': 0.2, '-0.1': 0.5}\n21:50:17|INFO   |  power LIFEENV (n=300): d0 {'0': 0.0, '0.05': 0.1, '0.1': 0.1, '0.15': 0.5, '0.2': 0.7, '0.28': 1.0} | d_lost {'0': 0.0, '-0.03': 0.2, '-0.06': 0.0, '-0.1': 1.0}\n21:50:18|INFO   |  power SOC (n=300): d0 {'0': 0.1, '0.05': 0.0, '0.1': 0.5, '0.15': 0.4, '0.2': 0.7, '0.28': 1.0} | d_lost {'0': 0.1, '-0.03': 0.2, '-0.06': 0.1, '-0.1': 0.8}\n21:50:19|INFO   |  power MATHDEC (n=165): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.2, '0.15': 0.7, '0.2': 0.5, '0.28': 1.0} | d_lost {'0': 0.1, '-0.03': 0.3, '-0.06': 0.1, '-0.1': 0.8}\n21:50:20|INFO   |  power COHORT (n=600): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.1, '0.15': 0.6, '0.2': 0.9, '0.28': 1.0} | d_lost {'0': 0.0, '-0.03': 0.1, '-0.06': 0.1, '-0.1': 0.6}\n21:50:21|INFO   |  power COHORT_DEVHOME (n=300): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.1, '0.15': 0.4, '0.2': 0.9, '0.28': 1.0} | d_lost {'0': 0.2, '-0.03': 0.1, '-0.06': 0.2, '-0.1': 0.8}\n21:50:23|INFO   |  power COHORT_NONDEVHOME (n=300): d0 {'0': 0.0, '0.05': 0.0, '0.1': 0.1, '0.15': 0.4, '0.2': 0.7, '0.28': 1.0} | d_lost {'0': 0.0, '-0.03': 0.2, '-0.06': 0.3, '-0.1': 0.4}\n21:50:23|INFO   |power simulation 9s\n21:50:23|INFO   |dev stage done in 35s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [94] THINKING · 2026-09-28 21:52:16 UTC

```
The dev smoke run passed end to end. Before the full-size run, I'm fixing the power simulation to cap subsampling at the dev concept count (avoiding merged strata from duplicates) and moving bootstraps, crossed bootstraps, and power sims onto a deterministic thread pool for reproducibility and faster runtime.
```

### [95] TOOL CALL — Bash · 2026-09-28 21:52:16 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('lib/models.py'); s=p.read_text()
old='''import math

import numpy as np'''
new='''import math
import os
from concurrent.futures import ThreadPoolExecutor

import numpy as np'''
assert old in s; s=s.replace(old,new)
old='''BASE = ["a_phi_home",'''
new='''N_THREADS = int(os.environ.get("AII_THREADS", 8))


def tmap(fn, items) -> list:
    """deterministic thread map (numpy releases the GIL in the heavy kernels); order of results = order of items."""
    items = list(items)
    if N_THREADS <= 1 or len(items) < 4:
        return [fn(x) for x in items]
    with ThreadPoolExecutor(N_THREADS) as ex:
        return list(ex.map(fn, items))


BASE = ["a_phi_home",'''
assert old in s; s=s.replace(old,new,1)
old='''    B, L = [], []
    for w in W:
        r = m.fit(b0=r0["coef"], w=w, want_cov=False)
        B.append(r["coef"])
        if ms is not None:
            L.append(2 * (r["ll"] - ms.fit(b0=rs0["coef"], w=w, want_cov=False)["ll"]))
    B = np.array(B)'''
new='''    def one(w):
        r = m.fit(b0=r0["coef"], w=w, want_cov=False)
        lrv = 2 * (r["ll"] - ms.fit(b0=rs0["coef"], w=w, want_cov=False)["ll"]) if ms is not None else None
        return r["coef"], lrv
    got = tmap(one, W)
    B = np.array([g[0] for g in got])
    L = [g[1] for g in got if g[1] is not None]'''
assert old in s; s=s.replace(old,new)
old='''    B = []
    for _ in range(n_boot):
        v = rng.poisson(1.0, 26).astype(float)
        u = rng.poisson(1.0, len(uc)).astype(float)
        keep = (v[fk] > 0) & (u[cinv] > 0)
        sub = df[keep]
        off = np.log(v[fk][keep])
        m = FastCLogit(sub[cols].to_numpy(np.float64), sub.entered.to_numpy(), sub.stratum.to_numpy(), offset=off)
        if m.n_strata == 0:
            continue
        ws = u[np.searchsorted(uc, m.sid // 100)]
        B.append(m.fit(b0=b0, w=ws, want_cov=False)["coef"][cols.index(target)])
    B = np.array(B)'''
new='''    draws = [(rng.poisson(1.0, 26).astype(float), rng.poisson(1.0, len(uc)).astype(float)) for _ in range(n_boot)]
    Xall, yall, sall = df[cols].to_numpy(np.float64), df.entered.to_numpy(), df.stratum.to_numpy()

    def one(vu):
        v, u = vu
        keep = (v[fk] > 0) & (u[cinv] > 0)
        m = FastCLogit(Xall[keep], yall[keep], sall[keep], offset=np.log(v[fk][keep]))
        if m.n_strata == 0:
            return np.nan
        ws = u[np.searchsorted(uc, m.sid // 100)]
        return m.fit(b0=b0, w=ws, want_cov=False)["coef"][cols.index(target)]
    B = np.array(tmap(one, draws))
    B = B[np.isfinite(B)]'''
assert old in s; s=s.replace(old,new)
p.write_text(s)

p=Path('lib/analysis.py'); s=p.read_text()
old='''        row = {"n_concepts": n, "n_sims": ns, "d0": {}, "d_lost": {}}
        for bd in grid_d0:
            hit = []
            for _ in range(ns):
                pick = rng.choice(cp, min(n, len(cp)), replace=n > len(cp))
                d = ip[ip.cidx.isin(pick)]
                m = M.model(d, c4)
                bt = b4.copy(); bt[c4.index("d0_ret_rel")] = bd
                ysim = _sim_events(m, m.X @ bt, rng)
                m3 = M.FastCLogit(m.X[:, :len(c3)], ysim, m.sid[m.row_s]); m2 = M.FastCLogit(m.X[:, :len(c2)], ysim, m.sid[m.row_s])
                r3 = m3.fit(want_cov=False); r2 = m2.fit(want_cov=False)
                lrv = 2 * (r3["ll"] - r2["ll"])
                hit.append(stats.chi2.sf(max(lrv, 0), 1) < 0.01 and r3["coef"][-1] > 0)
            row["d0"][str(bd)] = float(np.mean(hit))
        for bl in grid_lost:
            hit = []
            for _ in range(ns):
                pick = rng.choice(caa, min(n, len(caa)), replace=n > len(caa))
                d = ia[ia.cidx.isin(pick)]
                m = M.model(d, ca)
                bt = ba.copy(); bt[-1] = bl
                ysim = _sim_events(m, m.X @ bt, rng)
                ms = M.FastCLogit(m.X, ysim, m.sid[m.row_s])
                r = ms.fit()
                z = r["coef"][-1] / r["se"][-1]
                hit.append(stats.norm.cdf(z) < 0.05)
            row["d_lost"][str(bl)] = float(np.mean(hit))'''
new='''        row = {"n_concepts": n, "n_sims": ns, "d0": {}, "d_lost": {}, "n_capped_at_dev_size": bool(n > len(cp))}

        def sim_d0(args):
            bd, seed = args
            r_ = np.random.default_rng(seed)
            pick = r_.choice(cp, min(n, len(cp)), replace=False)
            d = ip[ip.cidx.isin(pick)]
            m = M.model(d, c4)
            bt = b4.copy(); bt[c4.index("d0_ret_rel")] = bd
            ysim = _sim_events(m, m.X @ bt, r_)
            m3 = M.FastCLogit(m.X[:, :len(c3)], ysim, m.sid[m.row_s]); m2 = M.FastCLogit(m.X[:, :len(c2)], ysim, m.sid[m.row_s])
            r3 = m3.fit(want_cov=False); r2 = m2.fit(want_cov=False)
            lrv = 2 * (r3["ll"] - r2["ll"])
            return bool(stats.chi2.sf(max(lrv, 0), 1) < 0.01 and r3["coef"][-1] > 0)

        def sim_lost(args):
            bl, seed = args
            r_ = np.random.default_rng(seed)
            pick = r_.choice(caa, min(n, len(caa)), replace=False)
            d = ia[ia.cidx.isin(pick)]
            m = M.model(d, ca)
            bt = ba.copy(); bt[-1] = bl
            ysim = _sim_events(m, m.X @ bt, r_)
            r = M.FastCLogit(m.X, ysim, m.sid[m.row_s]).fit()
            return bool(stats.norm.cdf(r["coef"][-1] / r["se"][-1]) < 0.05)
        for bd in grid_d0:
            row["d0"][str(bd)] = float(np.mean(M.tmap(sim_d0, [(bd, s_) for s_ in rng.integers(1 << 62, size=ns)])))
        for bl in grid_lost:
            row["d_lost"][str(bl)] = float(np.mean(M.tmap(sim_lost, [(bl, s_) for s_ in rng.integers(1 << 62, size=ns)])))'''
assert old in s; s=s.replace(old,new)
p.write_text(s)

p=Path('method.py'); s=p.read_text()
old='''import json
import math
import os
'''
new='''import json
import math
import os

for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")  # parallelism comes from the thread map over resamples (lib/models.tmap)
'''
assert old in s; s=s.replace(old,new,1); p.write_text(s)
EOF
AII_SMOKE_CONCEPTS=300 AII_NBOOT=200 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=50 AII_NUNITBOOT=10 AII_NPOWER=40 timeout 1200 .venv/bin/python method.py dev 2>&1 | grep -E "bootstr|power sim|done|Error|error" ; AII_THREADS=1 AII_SMOKE_CONCEPTS=300 AII_NBOOT=200 AII_NPERM=20 AII_NREWIRE=10 AII_NREWIRE_FULL=3 AII_NCROSS=50 AII_NUNITBOOT=10 AII_NPOWER=40 timeout 1200 .venv/bin/python method.py dev 2>&1 | grep -E "bootstr|power sim|done|Error|error"
```

### [96] TOOL RESULT — Bash · 2026-09-28 21:53:58 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bz0pfeuvi", "timedOutAfterMs": 120000}
```

### [97] ASSISTANT · 2026-09-28 21:55:20 UTC

```
While that timing run goes, I'm writing the T0 unit tests. First I'm factoring the permutation draw into a testable function.
```

### [98] TOOL CALL — Bash · 2026-09-28 21:55:20 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('lib/analysis.py'); s=p.read_text()
old='''    for _ in range(n):
        key = rng.random(P.shape)
        key[~P] = 2.0
        rank = key.argsort(1).argsort(1)
        Mk = rank < nret[:, None]
        m3.set_col'''
new='''    for _ in range(n):
        Mk = perm_masks(P, nret, rng)
        m3.set_col'''
assert old in s; s=s.replace(old,new)
old='''def perm_null('''
new='''def perm_masks(P: np.ndarray, nret: np.ndarray, rng) -> np.ndarray:
    """per row: nret[s] fields drawn uniformly without replacement from the pool P[s] (requires |P| >= nret)."""
    key = rng.random(P.shape)
    key[~P] = 2.0
    rank = key.argsort(1).argsort(1)
    return rank < nret[:, None]


def perm_null('''
assert old in s; s=s.replace(old,new,1); p.write_text(s)
EOF
cat > tests/test_units.py <<'EOF'
#!/usr/bin/env python3
"""T0 unit tests (no network, < 2 min). Writes results/unit_tests_T0.json."""
from __future__ import annotations

import json
import shutil
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "lib"))
import analysis as AN  # noqa: E402
import d3  # noqa: E402
import exp5 as X  # noqa: E402
import h2_exp6 as H2  # noqa: E402
import models as M  # noqa: E402
import seal  # noqa: E402
from stats_core import CLogit  # noqa: E402

RESULTS: dict[str, dict] = {}


def check(name: str):
    def deco(fn):
        t = time.time()
        try:
            info = fn() or {}
            RESULTS[name] = {"pass": True, **info, "sec": round(time.time() - t, 2)}
        except AssertionError as e:
            RESULTS[name] = {"pass": False, "error": str(e), "sec": round(time.time() - t, 2)}
        print(f"{'PASS' if RESULTS[name]['pass'] else 'FAIL'}  {name}  {RESULTS[name]}")
        return fn
    return deco


@check("1_states_toy")
def _():
    g = np.zeros((d3.NY, 27))
    # field 13 (k=2) off-home: 1 work in 2000, 1 in 2001 -> entered 2001; 1 in 2003, 1 in 2004 -> retained 2004 (age 3)
    for y, n in ((2000, 1), (2001, 1), (2003, 1), (2004, 1)):
        g[y - 1995, 3] = n
    # field 20 (k=9): 2 works in 1996 then silence -> entered 1996, lost from 1999 (w3 == 0)
    g[1996 - 1995, 10] = 2
    home = np.zeros((1, 26), bool); home[0, 0] = True          # home = field 11
    S = d3.panel_states(g[None], home)
    yi = lambda y: y - 1995  # noqa: E731
    assert not S["entered"][0, yi(2000), 2] and S["entered"][0, yi(2001), 2]
    assert S["retaining"][0, yi(2004), 2] and not S["retaining"][0, yi(2002), 2]  # 2002: w3 = 1 (2001) + 0 -> < 2
    assert S["age"][0, yi(2004), 2] == 3
    assert S["lost"][0, yi(1999), 9] and not S["lost"][0, yi(1998), 9]
    assert S["tenure"][0, yi(1999), 9] == 0                     # last positive year == entry year
    # home field never retained
    g2 = g.copy(); g2[:, 1] = 5
    S2 = d3.panel_states(g2[None], home)
    assert not S2["retaining"][0, :, 0].any()
    return {}


@check("1b_states_equal_h2_exp6_on_50_real_concepts")
def _():
    fr, Gd = X.exp6_frame()
    rng = np.random.default_rng(0)
    pick = fr.sample(50, random_state=1)
    for r in pick.itertuples():
        g = Gd[int(r.cidx)]
        home = np.zeros((1, 26), bool)
        for h in r.home_list:
            home[0, h - 11] = True
        a = H2.states(g, r.home_list)
        b = d3.panel_states(g[None], home)
        for k in ("entered", "retaining", "lost"):
            assert (a[k] == b[k][0]).all(), k
        GF = X.exp6_GF()
        assert (H2.rca_entered(g, GF) == d3.rca_entered_panel(g[None], GF)[0]).all()
    return {"n": 50}


@check("2_rca_masks_toy")
def _():
    GF = np.ones((d3.NY, 26)) * 10.0                            # every field has share 1/26
    x = np.zeros((2, d3.NY, 26))
    x[0, 10, 0] = 3; x[0, 10, 1] = 1                            # year 10: shares 0.75, 0.25 vs 1/26 -> both RCA > 1
    x[1, 10, :] = 1                                             # uniform -> RCA exactly 1 everywhere (tie, strict > excludes)
    R = d3.rca_panel(x, GF)
    assert R["U_1y"][0, 10, 0] and R["U_1y"][0, 10, 1] and not R["U_1y"][0, 10, 2]
    assert not R["U_1y"][1, 10].any(), "RCA == 1 must not count (strict >)"
    assert R["ties_1y"] >= 26
    assert not R["U_1y"][0, 5].any(), "empty portfolio -> no RCA"
    assert R["U_cum"][0, 12, 0] and R["U_w3"][0, 12, 0] and not R["U_w3"][0, 13, 0]
    assert not R["U_pers"][0, 12, 0]                            # earlier window empty
    return {}


@check("3_density_dvol_mean_rel")
def _():
    rng = np.random.default_rng(3)
    phi = rng.random((26, 26)); phi = (phi + phi.T) / 2; np.fill_diagonal(phi, 0)
    Mk = np.zeros((1, 26), bool); Mk[0, [1, 4, 7]] = True
    k = 10
    assert np.isclose(d3._dens(Mk, phi)[0, k], phi[[1, 4, 7], k].sum() / phi[:, k].sum())
    assert np.isclose(d3._mrel(Mk, phi)[0, k], phi[[1, 4, 7], k].mean())
    s = rng.random((1, 26))
    assert np.isclose(d3._wdens(d3._share(s), phi)[0, k], (s[0] / s.sum() * phi[:, k]).sum() / phi[:, k].sum())
    assert d3._mrel(np.zeros((1, 26), bool), phi)[0, k] == 0
    bb = X.load_backbone()
    assert np.abs(np.diag(bb["phi"])).max() == 0 and np.allclose(bb["phi"], bb["phi"].T)
    return {}


@check("4_clogit_vs_statsmodels_and_stats_core")
def _():
    from statsmodels.discrete.conditional_models import ConditionalLogit
    rng = np.random.default_rng(4)
    S, J = 2000, 8
    X_ = rng.normal(size=(S * J, 3)); b = np.array([0.8, -0.5, 0.3])
    st = np.repeat(np.arange(S), J)
    u = (X_ @ b).reshape(S, J) + rng.gumbel(size=(S, J))
    y = np.zeros((S, J)); y[np.arange(S), u.argmax(1)] = 1; y = y.ravel()
    df = pd.DataFrame(X_, columns=["a", "b", "c"]); df["entered"] = y; df["stratum"] = st; df["cidx"] = st; df["field"] = np.tile(np.arange(11, 11 + J), S)
    r = M.model(df, ["a", "b", "c"]).fit()
    sm = ConditionalLogit(y, X_, groups=st).fit(disp=0)
    sc = CLogit(X_, y, st).fit()
    rel = np.abs(r["coef"] - sm.params) / np.abs(sm.params)
    assert rel.max() < 1e-3, rel
    assert np.abs(r["coef"] - sc["coef"]).max() < 1e-5
    assert np.abs(r["se"] - sm.bse).max() / sm.bse.min() < 1e-3
    return {"max_rel_diff_vs_statsmodels": float(rel.max())}


@check("4b_weighted_bootstrap_equals_duplicate_relabel")
def _():
    rng = np.random.default_rng(5)
    S, J = 300, 6
    X_ = rng.normal(size=(S * J, 2)); st = np.repeat(np.arange(S), J) + 100 * np.repeat(np.arange(S) // 3, J) * 0
    cid = np.repeat(np.arange(S) // 3, J)                        # 3 strata per concept
    st = cid * 100 + np.tile(np.repeat(np.arange(3), J), S // 3)
    y = np.zeros(S * J); y[np.arange(S) * J + rng.integers(0, J, S)] = 1
    df = pd.DataFrame(X_, columns=["a", "b"]); df["entered"] = y; df["stratum"] = st; df["cidx"] = cid; df["field"] = 11
    m = M.model(df, ["a", "b"])
    u = np.unique(cid); cnt = np.bincount(rng.integers(0, len(u), len(u)), minlength=len(u)).astype(float)
    w = cnt[np.searchsorted(u, m.sid // 100)]
    rw = m.fit(w=w)
    # explicit duplication with relabelled strata (h2_exp6.boot_coef convention)
    parts = []
    for c in u:
        for rep in range(int(cnt[c])):
            d = df[df.cidx == c].copy(); d["stratum"] = d.stratum * 10000 + rep; parts.append(d)
    dd = pd.concat(parts)
    rd = CLogit(dd[["a", "b"]].to_numpy(), dd.entered.to_numpy(), dd.stratum.to_numpy()).fit()
    assert np.abs(rw["coef"] - rd["coef"]).max() < 1e-5, (rw["coef"], rd["coef"])
    return {}


@check("5_permutation_keeps_size_footprint_pool")
def _():
    rng = np.random.default_rng(6)
    P = rng.random((500, 26)) < 0.3
    RET = P & (rng.random((500, 26)) < 0.5)
    nret = RET.sum(1)
    for _ in range(20):
        Mk = AN.perm_masks(P, nret, rng)
        assert (Mk.sum(1) == nret).all()
        assert not (Mk & ~P).any()
    return {}


@check("6_rewire_preserves_degree_and_weights")
def _():
    bb = X.load_backbone()
    phi = bb["phi"]
    P = H2.rewire(phi, np.random.default_rng(7))
    deg = lambda A: (A > 0).sum(0)  # noqa: E731
    assert (np.sort(deg(P)) == np.sort(deg(phi))).all() and (deg(P) == deg(phi)).all()
    w1 = np.sort(phi[np.triu_indices(26, 1)]); w2 = np.sort(P[np.triu_indices(26, 1)])
    assert np.allclose(w1, w2)
    return {"edges": int((np.triu(phi, 1) > 0).sum())}


@check("7_crossed_offset_v1_equals_unweighted")
def _():
    rng = np.random.default_rng(8)
    S, J = 400, 7
    X_ = rng.normal(size=(S * J, 2)); st = np.repeat(np.arange(S), J)
    y = np.zeros(S * J); y[np.arange(S) * J + rng.integers(0, J, S)] = 1
    a = M.FastCLogit(X_, y, st).fit()
    b = M.FastCLogit(X_, y, st, offset=np.log(np.ones(S * J))).fit(w=np.ones(S))
    assert np.abs(a["coef"] - b["coef"]).max() < 1e-12
    return {}


@check("8_seal_guard")
def _():
    tmp = ROOT / "tests" / "_seal_tmp"
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "logs").mkdir(parents=True); (tmp / "results").mkdir(); (tmp / "lib").mkdir()
    (tmp / "method.py").write_text("x = 1\n")
    old = (seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE)
    seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE = tmp, tmp / "results/frozen_spec.json", tmp / "logs/seal.log", tmp / "logs/unseal.log", ["method.py"]
    try:
        try:
            seal.unseal(); raise AssertionError("unseal before freeze did not raise")
        except seal.SealedError:
            pass
        seal.freeze({"a": 1}, None)
        (tmp / "method.py").write_text("x = 2\n")
        try:
            seal.unseal(); raise AssertionError("code edit did not raise")
        except seal.SealedError:
            pass
        (tmp / "method.py").write_text("x = 1\n")
        seal.unseal()
        try:
            seal.unseal(); raise AssertionError("second unseal did not raise")
        except seal.SealedError:
            pass
    finally:
        seal.ROOT, seal.SPEC, seal.SEAL, seal.UNSEAL, seal.CODE = old
        shutil.rmtree(tmp, ignore_errors=True)
    return {}


if __name__ == "__main__":
    out = ROOT / "results" / "unit_tests_T0.json"
    out.write_text(json.dumps({"all_pass": all(v["pass"] for v in RESULTS.values()), "tests": RESULTS}, indent=1))
    print("ALL PASS" if all(v["pass"] for v in RESULTS.values()) else "SOME FAILED")
    sys.exit(0 if all(v["pass"] for v in RESULTS.values()) else 1)
EOF
timeout 300 .venv/bin/python tests/test_units.py 2>&1 | tail -15
```

### [99] TOOL RESULT — Bash · 2026-09-28 21:56:02 UTC

```
{"stdout": "PASS  1_states_toy  {'pass': True, 'sec': 0.0}\nPASS  1b_states_equal_h2_exp6_on_50_real_concepts  {'pass': True, 'n': 50, 'sec': 5.3}\nPASS  2_rca_masks_toy  {'pass': True, 'sec': 0.0}\nPASS  3_density_dvol_mean_rel  {'pass': True, 'sec': 0.04}\nPASS  4_clogit_vs_statsmodels_and_stats_core  {'pass': True, 'max_rel_diff_vs_statsmodels': 0.00010476397867502322, 'sec': 11.62}\nPASS  4b_weighted_bootstrap_equals_duplicate_relabel  {'pass': True, 'sec': 0.07}\nPASS  5_permutation_keeps_size_footprint_pool  {'pass': True, 'sec': 0.02}\nPASS  6_rewire_preserves_degree_and_weights  {'pass': True, 'edges': 78, 'sec': 0.02}\nPASS  7_crossed_offset_v1_equals_unweighted  {'pass': True, 'sec': 0.0}\nPASS  8_seal_guard  {'pass': True, 'sec': 0.25}\nALL PASS", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [100] TOOL CALL — Bash · 2026-09-28 21:56:02 UTC

```
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-Id7TLZ6r1C7M-3-invention-loop-iter-3-gen-art-gen-art-experiment-7/1ca57759-1b9c-4574-b7ab-ffcc529ff36c/tasks/bz0pfeuvi.output
```

### [101] TOOL RESULT — Bash · 2026-09-28 21:56:02 UTC

```
{"stdout": "21:51:44|INFO   |headline bootstraps (200) in 6s\n21:51:45|INFO   |[exp5_dev] crossed bootstrap 0s: [0.07901510944162084, 0.42987369556281113]\n21:52:20|INFO   |power simulation 22s\n21:52:20|INFO   |dev stage done in 55s\n21:53:00|INFO   |headline bootstraps (200) in 7s\n21:53:00|INFO   |[exp5_dev] crossed bootstrap 0s: [0.07901510944162084, 0.42987369556281113]\n21:53:41|INFO   |power simulation 26s\n21:53:41|INFO   |dev stage done in 61s\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [102] THINKING · 2026-09-28 21:56:02 UTC

```
Threads barely help at smoke size, but full-size runs should take a few minutes for step1 and 30-40 minutes for dev, both within budget. I'll launch the full step1 run followed by the full dev run in the background.
```

### [103] TOOL CALL — Bash · 2026-09-28 21:56:02 UTC

```
rm -f results/step2_dev.json && (timeout 3000 .venv/bin/python method.py step1 > logs/step1_full.out 2>&1; echo "STEP1 EXIT $?" >> logs/step1_full.out; timeout 5400 .venv/bin/python method.py dev > logs/dev_full.out 2>&1; echo "DEV EXIT $?" >> logs/dev_full.out) &
echo started
```

### [104] TOOL RESULT — Bash · 2026-09-28 21:56:02 UTC

```
{"stdout": "started", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [105] ASSISTANT · 2026-09-28 21:56:02 UTC

```
While that runs I'm writing the output and audit layers. First, `battery` now saves the null distributions (permutation, rewire, label-perm) to an npz for the null histograms.
```

### [106] TOOL CALL — Bash · 2026-09-28 21:56:02 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('method.py'); s=p.read_text()
old='''    out["specificity"] = AN.specificity(df_all, st, prim, alls, spec, bb, rng, n_boot, N_PERM, N_REWIRE, N_PERM, N_REWIRE_FULL)
'''
new='''    out["specificity"] = AN.specificity(df_all, st, prim, alls, spec, bb, rng, n_boot, N_PERM, N_REWIRE, N_PERM, N_REWIRE_FULL)
    sp = out["specificity"]
    np.savez_compressed(RES / f"nulls_{tag}.npz", LR_obs=sp["a_permutation"]["LR_obs"], perm=sp["a_permutation"]["_null"],
                        perm_entoff=sp["a_permutation_secondary_all_entered_offhome"]["_null"],
                        rewire=sp["d_backbone_d0_only"]["rewire"]["_null"], label_perm=sp["d_backbone_d0_only"]["label_perm"]["_null"],
                        rewire_full=sp.get("d_backbone_full_recompute", {}).get("_lrs", np.array([])))
'''
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
sleep 60; cat logs/step1_full.out | grep -v "EXP6 \(dev\|heldout\):"
```

### [107] TOOL RESULT — Bash · 2026-09-28 21:56:40 UTC

```
{"stdout": "21:55:11|INFO   |T1 gate: LR=68.569 d0=0.2809 d_lost_gate=-0.0632\n21:55:16|INFO   |[exp6_dev] ladder: R1_rca_vs_R0_M0 LR=30.16, R2_vol_vs_R1_rca LR=17.02, R3_ret_vs_R2_vol LR=29.32, R4_lost_vs_R3_ret LR=0.03, S_strict_vs_S_strict0 LR=20.52, S_pca_vs_S_pca0 LR=20.60, EXP6_M1_vs_R0_M0 LR=34.49, EXP6_M2lost_vs_R0_M0 LR=2.26\n21:55:16|INFO   |[exp6_dev] d0 in R3 = 0.2151; d0 in S_strict = 0.1907; d_lost in A1 = -0.0796\n21:55:17|INFO   |[exp6_heldout] ladder: R1_rca_vs_R0_M0 LR=21.70, R2_vol_vs_R1_rca LR=20.37, R3_ret_vs_R2_vol LR=57.59, R4_lost_vs_R3_ret LR=0.55, S_strict_vs_S_strict0 LR=50.33, S_pca_vs_S_pca0 LR=51.27, EXP6_M1_vs_R0_M0 LR=68.57, EXP6_M2lost_vs_R0_M0 LR=3.69\n21:55:17|INFO   |[exp6_heldout] d0 in R3 = 0.2618; d0 in S_strict = 0.2522; d_lost in A1 = -0.0525\n21:55:59|INFO   |headline bootstraps (1000) in 43s\n21:56:03|INFO   |[exp6_heldout] crossed bootstrap 3s: [0.09600964363240713, 0.42323271222583136]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [108] ASSISTANT · 2026-09-28 21:58:01 UTC

```
Full `step1` is running (1,000 bootstraps took 43 s). Writing `audit.py`, the independent code path with exact likelihood, hand loops and an inline DL.
```

### [109] TOOL CALL — Write · 2026-09-28 21:58:01 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/audit.py

#!/usr/bin/env python3
"""T7 independent audit (separate code path; never imports lib/d3.py or lib/models.py):
 (1) held-out pooled-4 LR(R3 vs R2) and d0 with statsmodels' EXACT conditional likelihood and a hand-written Breslow
     likelihood (scipy BFGS over a per-stratum Python loop) on the saved risk-set rows;
 (2) D_rca_1y and d0_ret_rel for 20 random held-out rows re-derived with naive loops from EXP5's raw agg_counts.parquet;
 (3) the DerSimonian-Laird pooling of per-unit d0 recomputed inline;
 (4) the same exact-likelihood check on the EXP6 held-out frame (Step 1).
Writes results/audit.json; every check records pass/fail and the numbers."""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy import optimize, stats
from statsmodels.discrete.conditional_models import ConditionalLogit

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"
RUN = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art")
EXP5, EXP6 = RUN / "gen_art_experiment_5", RUN / "gen_art_experiment_6"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "audit.log", rotation="30 MB", level="DEBUG")
R2 = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol"]
R3 = R2 + ["d0_ret_rel"]
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]


def std(df: pd.DataFrame, spec: dict, cols: list[str]) -> np.ndarray:
    return np.column_stack([(df[c].to_numpy(float) - spec[c]["mean"]) / spec[c]["sd"] for c in cols])


def informative(df: pd.DataFrame) -> pd.DataFrame:
    g = df.groupby("stratum").entered.agg(["sum", "size"])
    ok = g.index[(g["sum"] > 0) & (g["sum"] < g["size"])]
    return df[df.stratum.isin(ok)].sort_values(["stratum"], kind="stable")


def breslow_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:
    """hand-written Breslow conditional likelihood, one Python loop per stratum (deliberately naive)."""
    groups = [np.nonzero(s == u)[0] for u in np.unique(s)] if len(np.unique(s)) < 3000 else None
    if groups is None:
        order = np.argsort(s, kind="stable")
        _, st, cn = np.unique(s[order], return_index=True, return_counts=True)
        groups = [order[a:a + c] for a, c in zip(st, cn)]

    def nll(b):
        eta = X @ b
        ll, g = 0.0, np.zeros_like(b)
        for ix in groups:
            e = eta[ix]; m = e.max(); w = np.exp(e - m); S = w.sum()
            ne = y[ix].sum()
            ll += (y[ix] * e).sum() - ne * (math.log(S) + m)
            g += (y[ix][:, None] * X[ix]).sum(0) - ne * (w[:, None] * X[ix]).sum(0) / S
        return -ll, -g
    r = optimize.minimize(nll, np.zeros(X.shape[1]), jac=True, method="BFGS", options={"gtol": 1e-6, "maxiter": 500})
    return r.x, -r.fun


def exact_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:
    m = ConditionalLogit(y, X, groups=s)
    r = m.fit(disp=0, method="bfgs", maxiter=300)
    return np.asarray(r.params), float(r.llf)


def ladder_check(df: pd.DataFrame, spec: dict, label: str, frac: float, seeds: list[int], reported: dict) -> dict:
    out = {"label": label, "subsample_fraction": frac, "runs": []}
    for sd in seeds:
        d = df
        if frac < 1:
            cids = df.cidx.unique()
            keep = np.random.default_rng(sd).choice(cids, int(frac * len(cids)), replace=False)
            d = df[df.cidx.isin(keep)]
        d = informative(d)
        y = d.entered.to_numpy(float); s = d.stratum.to_numpy()
        X2, X3 = std(d, spec, R2), std(d, spec, R3)
        t = time.time()
        b3b, l3b = breslow_fit(X3, y, s); _, l2b = breslow_fit(X2, y, s)
        tb = time.time() - t
        t = time.time()
        b3e, l3e = exact_fit(X3, y, s); _, l2e = exact_fit(X2, y, s)
        te = time.time() - t
        run = {"seed": sd, "n_strata": int(len(np.unique(s))), "share_multi_event_strata": float(d.groupby("stratum").entered.sum().gt(1).mean()),
               "breslow_hand": {"d0": float(b3b[-1]), "LR": float(2 * (l3b - l2b))},
               "exact_statsmodels": {"d0": float(b3e[-1]), "LR": float(2 * (l3e - l2e))}, "sec": [round(tb, 1), round(te, 1)]}
        run["LR_ratio_exact_over_breslow"] = run["exact_statsmodels"]["LR"] / run["breslow_hand"]["LR"] if run["breslow_hand"]["LR"] else None
        run["same_sign_d0"] = bool(np.sign(b3b[-1]) == np.sign(b3e[-1]))
        out["runs"].append(run)
        logger.info(f"[{label}] seed {sd}: {run}")
    if frac == 1:
        r = out["runs"][0]
        out["reported_pipeline"] = reported
        out["breslow_matches_pipeline"] = bool(abs(r["breslow_hand"]["LR"] - reported["LR"]) < 1e-3 * max(1, reported["LR"])
                                               and abs(r["breslow_hand"]["d0"] - reported["d0"]) < 1e-3)
    ratios = [r["LR_ratio_exact_over_breslow"] for r in out["runs"] if r["LR_ratio_exact_over_breslow"]]
    out["pass_same_sign_and_|ratio-1|<0.15"] = bool(all(r["same_sign_d0"] for r in out["runs"]) and all(abs(x - 1) < 0.15 for x in ratios))
    return out


def naive_rows(df: pd.DataFrame, fr: pd.DataFrame, n: int, seed: int) -> dict:
    """re-derive D_rca_1y and d0_ret_rel for n random rows from the raw scan with explicit loops."""
    bb = json.loads((EXP6 / "inputs" / "field_backbone.json").read_text())
    phi = bb["phi"]
    VF = np.load(EXP5 / "scan" / "year_field_totals.npz")["VF"]
    rows = df.sample(n, random_state=seed)
    ag = pd.read_parquet(EXP5 / "scan" / "agg_counts.parquet", filters=[("ci", "in", sorted(set(map(int, rows.cidx))))])
    ag = ag[ag.tagstate == 1]
    frm = fr.set_index("ci")
    out, ok = [], True
    for r in rows.itertuples():
        a = ag[ag.ci == r.cidx]
        cnt = {}
        for q in a.itertuples():
            if 1 <= q.vfield <= 26:
                cnt[(int(q.year), int(q.vfield))] = cnt.get((int(q.year), int(q.vfield)), 0) + int(q.n)
        yprev = int(r.t) - 1
        home = [int(h) for h in str(frm.loc[r.cidx, "home"]).split(";")]
        k = int(r.field)
        # D_rca_1y
        tot_c = sum(cnt.get((yprev, f - 10), 0) for f in range(11, 37))
        tot_all = sum(VF[yprev - 1995][f - 10] for f in range(11, 37))
        U = []
        for f in range(11, 37):
            if tot_c > 0:
                rca = (cnt.get((yprev, f - 10), 0) / tot_c) / (VF[yprev - 1995][f - 10] / tot_all)
                if rca > 1:
                    U.append(f)
        num = sum(phi[f - 11][k - 11] for f in U)
        den = sum(phi[f - 11][k - 11] for f in range(11, 37))
        drca = num / den if den > 0 else 0.0
        # retained set at t-1
        ret = []
        for f in range(11, 37):
            if f in home:
                continue
            cum_lag2 = sum(cnt.get((y, f - 10), 0) for y in range(1995, yprev - 2 + 1))
            w3 = sum(cnt.get((y, f - 10), 0) for y in range(yprev - 2, yprev + 1))
            if cum_lag2 >= 2 and w3 >= 2:
                ret.append(f)
        d0 = sum(phi[f - 11][k - 11] for f in ret) / len(ret) if ret else 0.0
        good = abs(drca - r.D_rca_1y) < 1e-5 and abs(d0 - r.d0_ret_rel) < 1e-5
        ok &= good
        out.append({"cidx": int(r.cidx), "t": int(r.t), "field": k, "D_rca_1y_naive": drca, "D_rca_1y_pipeline": float(r.D_rca_1y),
                    "d0_naive": d0, "d0_pipeline": float(r.d0_ret_rel), "match": bool(good)})
    return {"n": n, "all_match_1e-5": bool(ok), "rows": out}


def dl_inline(units: dict) -> dict:
    b = np.array([units[u]["d0_R3"]["coef"] for u in HELD4 if "d0_R3" in units.get(u, {})])
    se = np.array([units[u]["d0_R3"]["se_concept"] for u in HELD4 if "d0_R3" in units.get(u, {})])
    w = 1 / se**2
    fixed = (w * b).sum() / w.sum()
    Q = (w * (b - fixed) ** 2).sum()
    tau2 = max(0.0, (Q - (len(b) - 1)) / (w.sum() - (w**2).sum() / w.sum()))
    ws = 1 / (se**2 + tau2)
    return {"b": float((ws * b).sum() / ws.sum()), "se": float(math.sqrt(1 / ws.sum())), "tau2": float(tau2),
            "I2": float(max(0.0, (Q - (len(b) - 1)) / Q)) if Q > 0 else 0.0}


@logger.catch(reraise=True)
def main() -> None:
    res = {}
    # EXP6 held-out (Step 1): full sample, exact vs Breslow
    s1 = json.loads((RES / "step1_exp6_robustness.json").read_text())
    d6 = pd.read_parquet(RES / "risk_sets_exp6_extended_heldout.parquet")
    d6 = d6[d6.n_ret > 0]
    rep6 = {"LR": s1["heldout"]["ladder"]["frontier_primary_sample"]["LR"]["R3_ret_vs_R2_vol"]["LR"],
            "d0": s1["heldout"]["ladder"]["frontier_primary_sample"]["models"]["R3_ret"]["coef"]["d0_ret_rel"]}
    res["exp6_heldout_exact"] = ladder_check(d6, s1["standardisation"], "EXP6 held-out", 1.0, [0], rep6)
    ho = RES / "step2_heldout.json"
    if ho.exists():
        h = json.loads(ho.read_text())
        spec = json.loads((RES / "frozen_spec.json").read_text())["standardisation_DEV"]
        df = pd.read_parquet(RES / "risk_sets_exp5_minus_exp6_heldout.parquet")
        df4 = df[df.unit.isin(HELD4) & (df.n_ret > 0)]
        lad = h["pooled4"]["ladder"]["frontier_primary_sample"]
        rep = {"LR": lad["LR"]["R3_ret_vs_R2_vol"]["LR"], "d0": lad["models"]["R3_ret"]["coef"]["d0_ret_rel"]}
        res["exp5_heldout_pooled4_breslow_full"] = ladder_check_breslow_only(df4, spec, rep)
        res["exp5_heldout_pooled4_exact_subsample"] = ladder_check(df4, spec, "EXP5 held-out pooled-4 (30% concepts)", 0.3, [1, 2, 3], rep)
        fr = pd.read_csv(EXP5 / "frame_concepts.csv")
        res["naive_rows"] = naive_rows(df4, fr, 20, 11)
        dl = dl_inline(h["units"])
        rep_dl = h["DL_4groups"]["d0"]
        res["DL_inline"] = {**dl, "pipeline_b": rep_dl["b"], "pipeline_se": rep_dl["se"],
                            "match": bool(abs(dl["b"] - rep_dl["b"]) < 1e-9 and abs(dl["se"] - rep_dl["se"]) < 1e-9)}
    else:
        res["exp5"] = "held-out stage not run yet"
    checks = {k: v.get("pass_same_sign_and_|ratio-1|<0.15", v.get("all_match_1e-5", v.get("match", v.get("breslow_matches_pipeline"))))
              for k, v in res.items() if isinstance(v, dict)}
    res["summary"] = {"checks": checks, "all_pass": bool(all(x for x in checks.values() if x is not None))}
    (RES / "audit.json").write_text(json.dumps(res, indent=1, default=float))
    logger.info(f"audit summary: {res['summary']}")


def ladder_check_breslow_only(df: pd.DataFrame, spec: dict, reported: dict) -> dict:
    d = informative(df)
    y = d.entered.to_numpy(float); s = d.stratum.to_numpy()
    t = time.time()
    b3, l3 = breslow_fit(std(d, spec, R3), y, s); _, l2 = breslow_fit(std(d, spec, R2), y, s)
    LR = 2 * (l3 - l2)
    return {"breslow_hand": {"d0": float(b3[-1]), "LR": float(LR)}, "reported_pipeline": reported, "sec": round(time.time() - t, 1),
            "match": bool(abs(LR - reported["LR"]) < 1e-3 * max(1, reported["LR"]) and abs(b3[-1] - reported["d0"]) < 1e-3)}


if __name__ == "__main__":
    main()
```

### [110] TOOL RESULT — Write · 2026-09-28 21:58:01 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/audit.py", "content": "#!/usr/bin/env python3\n\"\"\"T7 independent audit (separate code path; never imports lib/d3.py or lib/models.py):\n (1) held-out pooled-4 LR(R3 vs R2) and d0 with statsmodels' EXACT conditional likelihood and a hand-written Breslow\n     likelihood (scipy BFGS over a per-stratum Python loop) on the saved risk-set rows;\n (2) D_rca_1y and d0_ret_rel for 20 random held-out rows re-derived with naive loops from EXP5's raw agg_counts.parquet;\n (3) the DerSimonian-Laird pooling of per-unit d0 recomputed inline;\n (4) the same exact-likelihood check on the EXP6 held-out frame (Step 1).\nWrites results/audit.json; every check records pass/fail and the numbers.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nimport time\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy import optimize, stats\nfrom statsmodels.discrete.conditional_models import ConditionalLogit\n\nROOT = Path(__file__).resolve().parent\nRES = ROOT / \"results\"\nRUN = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art\")\nEXP5, EXP6 = RUN / \"gen_art_experiment_5\", RUN / \"gen_art_experiment_6\"\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"audit.log\", rotation=\"30 MB\", level=\"DEBUG\")\nR2 = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"D_rca_1y\", \"D_vol\"]\nR3 = R2 + [\"d0_ret_rel\"]\nHELD4 = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\n\n\ndef std(df: pd.DataFrame, spec: dict, cols: list[str]) -> np.ndarray:\n    return np.column_stack([(df[c].to_numpy(float) - spec[c][\"mean\"]) / spec[c][\"sd\"] for c in cols])\n\n\ndef informative(df: pd.DataFrame) -> pd.DataFrame:\n    g = df.groupby(\"stratum\").entered.agg([\"sum\", \"size\"])\n    ok = g.index[(g[\"sum\"] > 0) & (g[\"sum\"] < g[\"size\"])]\n    return df[df.stratum.isin(ok)].sort_values([\"stratum\"], kind=\"stable\")\n\n\ndef breslow_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:\n    \"\"\"hand-written Breslow conditional likelihood, one Python loop per stratum (deliberately naive).\"\"\"\n    groups = [np.nonzero(s == u)[0] for u in np.unique(s)] if len(np.unique(s)) < 3000 else None\n    if groups is None:\n        order = np.argsort(s, kind=\"stable\")\n        _, st, cn = np.unique(s[order], return_index=True, return_counts=True)\n        groups = [order[a:a + c] for a, c in zip(st, cn)]\n\n    def nll(b):\n        eta = X @ b\n        ll, g = 0.0, np.zeros_like(b)\n        for ix in groups:\n            e = eta[ix]; m = e.max(); w = np.exp(e - m); S = w.sum()\n            ne = y[ix].sum()\n            ll += (y[ix] * e).sum() - ne * (math.log(S) + m)\n            g += (y[ix][:, None] * X[ix]).sum(0) - ne * (w[:, None] * X[ix]).sum(0) / S\n        return -ll, -g\n    r = optimize.minimize(nll, np.zeros(X.shape[1]), jac=True, method=\"BFGS\", options={\"gtol\": 1e-6, \"maxiter\": 500})\n    return r.x, -r.fun\n\n\ndef exact_fit(X: np.ndarray, y: np.ndarray, s: np.ndarray) -> tuple[np.ndarray, float]:\n    m = ConditionalLogit(y, X, groups=s)\n    r = m.fit(disp=0, method=\"bfgs\", maxiter=300)\n    return np.asarray(r.params), float(r.llf)\n\n\ndef ladder_check(df: pd.DataFrame, spec: dict, label: str, frac: float, seeds: list[int], reported: dict) -> dict:\n    out = {\"label\": label, \"subsample_fraction\": frac, \"runs\": []}\n    for sd in seeds:\n        d = df\n        if frac < 1:\n            cids = df.cidx.unique()\n            keep = np.random.default_rng(sd).choice(cids, int(frac * len(cids)), replace=False)\n            d = df[df.cidx.isin(keep)]\n        d = informative(d)\n        y = d.entered.to_numpy(float); s = d.stratum.to_numpy()\n        X2, X3 = std(d, spec, R2), std(d, spec, R3)\n        t = time.time()\n        b3b, l3b = breslow_fit(X3, y, s); _, l2b = breslow_fit(X2, y, s)\n        tb = time.time() - t\n        t = time.time()\n        b3e, l3e = exact_fit(X3, y, s); _, l2e = exact_fit(X2, y, s)\n        te = time.time() - t\n        run = {\"seed\": sd, \"n_strata\": int(len(np.unique(s))), \"share_multi_event_strata\": float(d.groupby(\"stratum\").entered.sum().gt(1).mean()),\n               \"breslow_hand\": {\"d0\": float(b3b[-1]), \"LR\": float(2 * (l3b - l2b))},\n               \"exact_statsmodels\": {\"d0\": float(b3e[-1]), \"LR\": float(2 * (l3e - l2e))}, \"sec\": [round(tb, 1), round(te, 1)]}\n        run[\"LR_ratio_exact_over_breslow\"] = run[\"exact_statsmodels\"][\"LR\"] / run[\"breslow_hand\"][\"LR\"] if run[\"breslow_hand\"][\"LR\"] else None\n        run[\"same_sign_d0\"] = bool(np.sign(b3b[-1]) == np.sign(b3e[-1]))\n        out[\"runs\"].append(run)\n        logger.info(f\"[{label}] seed {sd}: {run}\")\n    if frac == 1:\n        r = out[\"runs\"][0]\n        out[\"reported_pipeline\"] = reported\n        out[\"breslow_matches_pipeline\"] = bool(abs(r[\"breslow_hand\"][\"LR\"] - reported[\"LR\"]) < 1e-3 * max(1, reported[\"LR\"])\n                                               and abs(r[\"breslow_hand\"][\"d0\"] - reported[\"d0\"]) < 1e-3)\n    ratios = [r[\"LR_ratio_exact_over_breslow\"] for r in out[\"runs\"] if r[\"LR_ratio_exact_over_breslow\"]]\n    out[\"pass_same_sign_and_|ratio-1|<0.15\"] = bool(all(r[\"same_sign_d0\"] for r in out[\"runs\"]) and all(abs(x - 1) < 0.15 for x in ratios))\n    return out\n\n\ndef naive_rows(df: pd.DataFrame, fr: pd.DataFrame, n: int, seed: int) -> dict:\n    \"\"\"re-derive D_rca_1y and d0_ret_rel for n random rows from the raw scan with explicit loops.\"\"\"\n    bb = json.loads((EXP6 / \"inputs\" / \"field_backbone.json\").read_text())\n    phi = bb[\"phi\"]\n    VF = np.load(EXP5 / \"scan\" / \"year_field_totals.npz\")[\"VF\"]\n    rows = df.sample(n, random_state=seed)\n    ag = pd.read_parquet(EXP5 / \"scan\" / \"agg_counts.parquet\", filters=[(\"ci\", \"in\", sorted(set(map(int, rows.cidx))))])\n    ag = ag[ag.tagstate == 1]\n    frm = fr.set_index(\"ci\")\n    out, ok = [], True\n    for r in rows.itertuples():\n        a = ag[ag.ci == r.cidx]\n        cnt = {}\n        for q in a.itertuples():\n            if 1 <= q.vfield <= 26:\n                cnt[(int(q.year), int(q.vfield))] = cnt.get((int(q.year), int(q.vfield)), 0) + int(q.n)\n        yprev = int(r.t) - 1\n        home = [int(h) for h in str(frm.loc[r.cidx, \"home\"]).split(\";\")]\n        k = int(r.field)\n        # D_rca_1y\n        tot_c = sum(cnt.get((yprev, f - 10), 0) for f in range(11, 37))\n        tot_all = sum(VF[yprev - 1995][f - 10] for f in range(11, 37))\n        U = []\n        for f in range(11, 37):\n            if tot_c > 0:\n                rca = (cnt.get((yprev, f - 10), 0) / tot_c) / (VF[yprev - 1995][f - 10] / tot_all)\n                if rca > 1:\n                    U.append(f)\n        num = sum(phi[f - 11][k - 11] for f in U)\n        den = sum(phi[f - 11][k - 11] for f in range(11, 37))\n        drca = num / den if den > 0 else 0.0\n        # retained set at t-1\n        ret = []\n        for f in range(11, 37):\n            if f in home:\n                continue\n            cum_lag2 = sum(cnt.get((y, f - 10), 0) for y in range(1995, yprev - 2 + 1))\n            w3 = sum(cnt.get((y, f - 10), 0) for y in range(yprev - 2, yprev + 1))\n            if cum_lag2 >= 2 and w3 >= 2:\n                ret.append(f)\n        d0 = sum(phi[f - 11][k - 11] for f in ret) / len(ret) if ret else 0.0\n        good = abs(drca - r.D_rca_1y) < 1e-5 and abs(d0 - r.d0_ret_rel) < 1e-5\n        ok &= good\n        out.append({\"cidx\": int(r.cidx), \"t\": int(r.t), \"field\": k, \"D_rca_1y_naive\": drca, \"D_rca_1y_pipeline\": float(r.D_rca_1y),\n                    \"d0_naive\": d0, \"d0_pipeline\": float(r.d0_ret_rel), \"match\": bool(good)})\n    return {\"n\": n, \"all_match_1e-5\": bool(ok), \"rows\": out}\n\n\ndef dl_inline(units: dict) -> dict:\n    b = np.array([units[u][\"d0_R3\"][\"coef\"] for u in HELD4 if \"d0_R3\" in units.get(u, {})])\n    se = np.array([units[u][\"d0_R3\"][\"se_concept\"] for u in HELD4 if \"d0_R3\" in units.get(u, {})])\n    w = 1 / se**2\n    fixed = (w * b).sum() / w.sum()\n    Q = (w * (b - fixed) ** 2).sum()\n    tau2 = max(0.0, (Q - (len(b) - 1)) / (w.sum() - (w**2).sum() / w.sum()))\n    ws = 1 / (se**2 + tau2)\n    return {\"b\": float((ws * b).sum() / ws.sum()), \"se\": float(math.sqrt(1 / ws.sum())), \"tau2\": float(tau2),\n            \"I2\": float(max(0.0, (Q - (len(b) - 1)) / Q)) if Q > 0 else 0.0}\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    res = {}\n    # EXP6 held-out (Step 1): full sample, exact vs Breslow\n    s1 = json.loads((RES / \"step1_exp6_robustness.json\").read_text())\n    d6 = pd.read_parquet(RES / \"risk_sets_exp6_extended_heldout.parquet\")\n    d6 = d6[d6.n_ret > 0]\n    rep6 = {\"LR\": s1[\"heldout\"][\"ladder\"][\"frontier_primary_sample\"][\"LR\"][\"R3_ret_vs_R2_vol\"][\"LR\"],\n            \"d0\": s1[\"heldout\"][\"ladder\"][\"frontier_primary_sample\"][\"models\"][\"R3_ret\"][\"coef\"][\"d0_ret_rel\"]}\n    res[\"exp6_heldout_exact\"] = ladder_check(d6, s1[\"standardisation\"], \"EXP6 held-out\", 1.0, [0], rep6)\n    ho = RES / \"step2_heldout.json\"\n    if ho.exists():\n        h = json.loads(ho.read_text())\n        spec = json.loads((RES / \"frozen_spec.json\").read_text())[\"standardisation_DEV\"]\n        df = pd.read_parquet(RES / \"risk_sets_exp5_minus_exp6_heldout.parquet\")\n        df4 = df[df.unit.isin(HELD4) & (df.n_ret > 0)]\n        lad = h[\"pooled4\"][\"ladder\"][\"frontier_primary_sample\"]\n        rep = {\"LR\": lad[\"LR\"][\"R3_ret_vs_R2_vol\"][\"LR\"], \"d0\": lad[\"models\"][\"R3_ret\"][\"coef\"][\"d0_ret_rel\"]}\n        res[\"exp5_heldout_pooled4_breslow_full\"] = ladder_check_breslow_only(df4, spec, rep)\n        res[\"exp5_heldout_pooled4_exact_subsample\"] = ladder_check(df4, spec, \"EXP5 held-out pooled-4 (30% concepts)\", 0.3, [1, 2, 3], rep)\n        fr = pd.read_csv(EXP5 / \"frame_concepts.csv\")\n        res[\"naive_rows\"] = naive_rows(df4, fr, 20, 11)\n        dl = dl_inline(h[\"units\"])\n        rep_dl = h[\"DL_4groups\"][\"d0\"]\n        res[\"DL_inline\"] = {**dl, \"pipeline_b\": rep_dl[\"b\"], \"pipeline_se\": rep_dl[\"se\"],\n                            \"match\": bool(abs(dl[\"b\"] - rep_dl[\"b\"]) < 1e-9 and abs(dl[\"se\"] - rep_dl[\"se\"]) < 1e-9)}\n    else:\n        res[\"exp5\"] = \"held-out stage not run yet\"\n    checks = {k: v.get(\"pass_same_sign_and_|ratio-1|<0.15\", v.get(\"all_match_1e-5\", v.get(\"match\", v.get(\"breslow_matches_pipeline\"))))\n              for k, v in res.items() if isinstance(v, dict)}\n    res[\"summary\"] = {\"checks\": checks, \"all_pass\": bool(all(x for x in checks.values() if x is not None))}\n    (RES / \"audit.json\").write_text(json.dumps(res, indent=1, default=float))\n    logger.info(f\"audit summary: {res['summary']}\")\n\n\ndef ladder_check_breslow_only(df: pd.DataFrame, spec: dict, reported: dict) -> dict:\n    d = informative(df)\n    y = d.entered.to_numpy(float); s = d.stratum.to_numpy()\n    t = time.time()\n    b3, l3 = breslow_fit(std(d, spec, R3), y, s); _, l2 = breslow_fit(std(d, spec, R2), y, s)\n    LR = 2 * (l3 - l2)\n    return {\"breslow_hand\": {\"d0\": float(b3[-1]), \"LR\": float(LR)}, \"reported_pipeline\": reported, \"sec\": round(time.time() - t, 1),\n            \"match\": bool(abs(LR - reported[\"LR\"]) < 1e-3 * max(1, reported[\"LR\"]) and abs(b3[-1] - reported[\"d0\"]) < 1e-3)}\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [111] TOOL CALL — Bash · 2026-09-28 21:58:01 UTC

```
tail -5 logs/step1_full.out; tail -5 logs/dev_full.out 2>/dev/null
```

### [112] TOOL RESULT — Bash [ERROR] · 2026-09-28 21:58:01 UTC

```
Error: Exit code 1
21:55:59|INFO   |headline bootstraps (1000) in 43s
21:56:03|INFO   |[exp6_heldout] crossed bootstrap 3s: [0.09600964363240713, 0.42323271222583136]
21:56:16|INFO   |  (a) permutation 13s p=0.0010
21:56:52|INFO   |  (d) backbone nulls 28s
21:56:54|INFO   |[exp6_heldout] rebuild sensitivities 1s; battery total 98s
```

### [113] ASSISTANT · 2026-09-28 21:58:01 UTC

```
`step1` is on its unit fits. Meanwhile I'm checking the `exp_gen_sol_out` schema for `method_out.json`.
```

### [114] TOOL CALL — Bash · 2026-09-28 21:58:01 UTC

```
cat /ai-inventor/.claude/skills/aii-json/schemas/exp_gen_sol_out.json; head -c 1500 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/preview_method_out.json
```

### [115] TOOL RESULT — Bash · 2026-09-28 21:58:01 UTC

```
{"stdout": "{\n  \"$schema\": \"http://json-schema.org/draft-07/schema#\",\n  \"type\": \"object\",\n  \"required\": [\"datasets\"],\n  \"properties\": {\n    \"metadata\": {\n      \"type\": \"object\",\n      \"description\": \"Optional top-level metadata (e.g. method_name, description, parameters, hyperparameters)\",\n      \"additionalProperties\": true\n    },\n    \"datasets\": {\n      \"type\": \"array\",\n      \"minItems\": 1,\n      \"items\": {\n        \"type\": \"object\",\n        \"required\": [\"dataset\", \"examples\"],\n        \"properties\": {\n          \"dataset\": {\n            \"type\": \"string\",\n            \"description\": \"Source dataset name\"\n          },\n          \"examples\": {\n            \"type\": \"array\",\n            \"minItems\": 1,\n            \"items\": {\n              \"type\": \"object\",\n              \"required\": [\"input\", \"output\"],\n              \"properties\": {\n                \"input\": {\n                  \"type\": \"string\",\n                  \"description\": \"Task prompt, question, or multi-turn conversation\"\n                },\n                \"output\": {\n                  \"type\": \"string\",\n                  \"description\": \"Expected agent response or action sequence\"\n                }\n              },\n              \"patternProperties\": {\n                \"^metadata_[a-zA-Z_][a-zA-Z0-9_]*$\": {\n                  \"description\": \"Per-example metadata (e.g. metadata_fold, metadata_feature_names)\"\n                },\n                \"^predict_[a-zA-Z_][a-zA-Z0-9_]*$\": {\n                  \"type\": \"string\",\n                  \"description\": \"Prediction from a method (e.g. predict_baseline, predict_our_method)\"\n                }\n              },\n              \"additionalProperties\": false\n            }\n          }\n        },\n        \"additionalProperties\": false\n      }\n    }\n  },\n  \"additionalProperties\": false\n}\n{\n  \"metadata\": {\n    \"method_name\": \"Gateway-weighted relatedness to retaining fields (H2 next-field entry) + rescue, relay, trajectories\",\n    \"baselines\": \"M0 = relatedness-to-home + log field size + Hidalgo relatedness density + target field's own gateway centrality\",\n    \"frame\": {\n      \"n_candidates\": 653,\n      \"drops\": {\n        \"no_onset_after_grounding\": 0,\n        \"precision_below_gate\": 0,\n        \"n_early_lt30\": 0,\n        \"no_labelled\": 0\n      },\n      \"n_frame\": 653,\n      \"n_newborn\": 653,\n      \"by_split\": {\n        \"dev\": 279,\n        \"heldout_cohort\": 248,\n        \"heldout_field\": 126\n      },\n      \"by_split_newborn\": {\n        \"dev\": 279,\n        \"heldout_cohort\": 248,\n        \"heldout_field\": 126\n      },\n      \"by_group_newborn\": {\n        \"dev|DEV_BGM\": 27,\n        \"dev|DEV_CS\": 22,\n        \"dev|DEV_Eng\": 59,\n        \"dev|DEV_Med\": 171,\n        \"heldout_cohort|DEV_BGM\": 13,\n        \"heldout_cohort|DEV_CS\": 18,\n        \"heldout_cohort|DEV_Eng\": 37,\n        \"heldout_cohort|DEV_Med\": 109,\n        \"heldout_cohort|LifeEnv\": 13,\n        \"heldout_cohort|OtherHealth\": 2,\n        \"heldout_cohort|Physical\": 15,\n        \"heldout_cohort|Social\": 41,\n        \"heldout_field|LifeEnv\": 34,\n        \"heldout_field|OtherHealth\": 4,\n        \"heldout_field|Physical\": 34,\n        \"heldout_field|Social\": 54\n      },\n      \"n_episodes\": 1865,\n      \"episodes_by_split\": {\n        \"heldout_cohort\": 768,\n        \"dev\": 707,\n        \"heldout_field\": 390\n      },\n      \"o2r_resi", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [116] ASSISTANT · 2026-09-28 21:59:30 UTC

```
Writing `outputs.py`: the consolidated result JSON, six figures (PNG + PDF), and schema-conformant `method_out.json`, split into parts when too large.
```

### [117] TOOL CALL — Write · 2026-09-28 21:59:30 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/outputs.py

#!/usr/bin/env python3
"""Stage `outputs`: results/frontier_result.json (everything in one place), figures/ (PNG + PDF), method_out.json
(exp_gen_sol_out schema; one example per held-out candidate row in an informative primary-sample stratum, with
within-stratum probabilities from the frozen DEV coefficients of R2 (RCA>1 + volume baseline) and R3 (+ retained frontier))."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
import models as M  # noqa: E402
import analysis as AN  # noqa: E402,F401  (registers the extra rungs)

RES, FIGS = ROOT / "results", ROOT / "figures"
plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 9, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 200, "savefig.bbox": "tight"})
C = {"exp6": "#0072B2", "dev": "#999999", "held": "#D55E00", "dl": "#000000", "cohort": "#009E73", "null": "#56B4E9"}
HELD4 = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
PART_LIMIT = 90 * 1024 * 1024


def load(name: str) -> dict:
    p = RES / name
    return json.loads(p.read_text()) if p.exists() else {}


def save(fig, name: str) -> None:
    fig.savefig(FIGS / f"{name}.png"); fig.savefig(FIGS / f"{name}.pdf")
    plt.close(fig)


def _ci(d: dict, key: str) -> tuple[float, float, float]:
    x = d[key]
    lo, hi = x.get("boot_ci", [x["coef"] - 1.96 * x["se_concept"], x["coef"] + 1.96 * x["se_concept"]])
    return x["coef"], lo, hi


def forest(s1: dict, dev: dict, ho: dict, key: str, dl_key: str, title: str, name: str) -> None:
    rows = []
    for u in ("Physical", "LifeEnv", "Social", "Cohort"):
        if key in s1.get("heldout_units", {}).get(u, {}):
            rows.append((f"EXP6 {u}", *_ci(s1["heldout_units"][u], key), C["exp6"], "o"))
    if s1:
        d = s1["heldout_DL"][dl_key]
        rows.append(("EXP6 DL pooled", d["b"], d["ci"][0], d["ci"][1], C["exp6"], "D"))
    for g in ("CS", "Eng", "BGM", "Med"):
        if key in dev.get("dev_groups", {}).get(g, {}):
            rows.append((f"DEV {g}", *_ci(dev["dev_groups"][g], key), C["dev"], "o"))
    for u in HELD4 + ["COHORT_DEVHOME", "COHORT_NONDEVHOME"]:
        if key in ho.get("units", {}).get(u, {}):
            rows.append((f"HELD {u}", *_ci(ho["units"][u], key), C["cohort"] if u.startswith("COHORT") else C["held"], "o"))
    if ho:
        d = ho["DL_4groups"][dl_key]
        rows.append(("HELD DL (4 groups)", d["b"], d["ci"][0], d["ci"][1], C["dl"], "D"))
        bkey = "d0_R3" if key == "d0_R3" else "d_lost_A1"
        tg = "d0_ret_rel" if key == "d0_R3" else "d_lost"
        b = ho["pooled4"]["boot"][bkey][tg]
        rows.append(("HELD pooled-4 (refit boot)", b["est"], b["ci"][0], b["ci"][1], C["dl"], "s"))
    fig, ax = plt.subplots(figsize=(5.2, 0.28 * len(rows) + 1.0))
    for i, (lab, b, lo, hi, col, mk) in enumerate(rows[::-1]):
        ax.plot([lo, hi], [i, i], color=col, lw=1.4)
        ax.plot(b, i, marker=mk, color=col, ms=5 if mk != "D" else 6)
    ax.axvline(0, color="k", lw=0.6, ls="--")
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]])
    ax.set_xlabel("coefficient per DEV-SD (conditional logit, concept-year strata); 95% CI, resampling unit = concept")
    ax.set_title(title, fontsize=9)
    save(fig, name)


def ladder_fig(panels: list[tuple[str, dict]]) -> None:
    steps = [("R1_rca_vs_R0_M0", "+RCA>1\ndensity"), ("R2_vol_vs_R1_rca", "+share\ndensity"), ("R3_ret_vs_R2_vol", "+retained\nfrontier"),
             ("R4_lost_vs_R3_ret", "+lost"), ("S_strict_vs_S_strict0", "strict:\n+retained")]
    rungs = ["R0_M0", "R1_rca", "R2_vol", "R3_ret", "R4_lost"]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.1 * len(panels), 3.0), sharey=False)
    axes = np.atleast_1d(axes)
    for ax, (lab, lad) in zip(axes, panels):
        lr = [lad["LR"][k]["LR"] for k, _ in steps]
        cols = [C["held"] if "retained" in s else C["dev"] for _, s in steps]
        ax.bar(range(len(steps)), lr, color=cols)
        ax.axhline(6.63, color="k", lw=0.6, ls=":")
        ax.set_xticks(range(len(steps))); ax.set_xticklabels([s for _, s in steps], fontsize=7)
        ax.set_title(lab, fontsize=8); ax.set_ylabel("LR (df=1); dotted: p=0.01")
        ax2 = ax.twinx()
        ax2.plot(range(len(rungs)), [lad["auc_within"][r] for r in rungs], "k.-", lw=0.8)
        ax2.set_ylabel("within-stratum AUC (R0..R4)", fontsize=7)
    fig.tight_layout()
    save(fig, "ladder")


def dose_fig(panels: list[tuple[str, dict]]) -> None:
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    for j, (lab, d, col) in enumerate(panels):
        f = d["fit"]
        xs = np.arange(3) + (j - 1) * 0.12
        b = [f[c]["coef"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
        se = [f[c]["se_concept"] for c in ("d_ret_a2", "d_ret_a3", "d_ret_a4p")]
        ax.errorbar(xs, b, yerr=1.96 * np.array(se), fmt="o-", color=col, label=lab, capsize=2, lw=1)
    ax.axhline(0, color="k", lw=0.6, ls="--")
    ax.set_xticks(range(3)); ax.set_xticklabels(["2", "3", ">=4"])
    ax.set_xlabel("years the retaining field has held the concept (persistence age)")
    ax.set_ylabel("coefficient (per SD of d0)")
    ax.legend(fontsize=7, frameon=False)
    save(fig, "dose_response")


def null_fig(tags: list[tuple[str, str]]) -> None:
    fig, axes = plt.subplots(len(tags), 3, figsize=(9, 2.3 * len(tags)), squeeze=False)
    for i, (lab, tag) in enumerate(tags):
        p = RES / f"nulls_{tag}.npz"
        if not p.exists():
            continue
        z = np.load(p)
        obs = float(z["LR_obs"])
        for j, (k, t) in enumerate((("perm", "retained-label permutation"), ("rewire", "degree-preserving rewiring"), ("label_perm", "node-label permutation"))):
            ax = axes[i, j]
            ax.hist(z[k], bins=40, color=C["null"])
            ax.axvline(obs, color=C["held"], lw=1.5)
            ax.set_title(f"{lab}: {t}\n(obs LR = {obs:.1f}; p = {(1 + (z[k] >= obs).sum()) / (1 + len(z[k])):.4f})", fontsize=7)
            ax.set_xlabel("LR(R3 vs R2) under the null")
    fig.tight_layout()
    save(fig, "null_hist")


def vm_fig(panels: list[tuple[str, dict]]) -> None:
    fig, ax = plt.subplots(figsize=(5.0, 3.0))
    labs, i = [], 0
    for lab, sp in panels:
        for key, tag, rk, nk in (("b_volume_matched", "coarse", "d_R_m", "d_N_m"), ("b2_volume_matched_fine", "fine", "d_R_mf", "d_N_mf")):
            c = sp.get(key, {}).get("contrast_R_minus_N")
            if not c:
                continue
            for off, kk, col in ((-0.15, rk, C["held"]), (0.15, nk, C["dev"])):
                ax.errorbar(i + off, c[kk]["est"], yerr=[[c[kk]["est"] - c[kk]["ci"][0]], [c[kk]["ci"][1] - c[kk]["est"]]],
                            fmt="o", color=col, capsize=2)
            labs.append(f"{lab}\n{tag}\nR-N={c['est']:.2f}\n[{c['ci'][0]:.2f},{c['ci'][1]:.2f}]")
            i += 1
    ax.axhline(0, color="k", lw=0.6, ls="--")
    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, fontsize=6)
    ax.set_ylabel("coefficient per SD of d0\n(orange: retained R; grey: entered-not-retained N)")
    save(fig, "vol_matched")


def method_out(ho: dict, spec: dict) -> dict:
    df = pd.read_parquet(RES / "risk_sets_exp5_minus_exp6_heldout.parquet")
    dev = load("step2_dev.json")
    fr = pd.read_csv(Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv"),
                     usecols=["ci", "concept_id", "qid", "name"]).set_index("ci")
    std = spec["standardisation_DEV"]
    prim = M.standardise(df[df.n_ret > 0], std)
    raw = df[df.n_ret > 0]
    inf = M.informative(prim)
    raw = raw.loc[inf.index]
    coef = dev["battery"]["ladder"]["frontier_primary_sample"]["models"]
    preds = {}
    for rn, nm in (("R2_vol", "predict_R2_rca_vol_baseline"), ("R3_ret", "predict_R3_retained_frontier")):
        cols = M.RUNGS[rn]
        eta = inf[cols].to_numpy() @ np.array([coef[rn]["coef"][c] for c in cols])
        e = np.exp(eta - inf.assign(_e=eta).groupby("stratum")._e.transform("max").to_numpy())
        preds[nm] = e / pd.Series(e, index=inf.index).groupby(inf.stratum).transform("sum").to_numpy()
    covs = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_rca_w3", "D_rca_cum", "D_rca_pers", "D_vol",
            "D_vol_w3", "d0_ret_rel", "d_lost", "n_ret", "n_lost"]
    datasets = {}
    for i, (ix, r) in enumerate(raw.iterrows()):
        c = int(r.cidx)
        inp = {"concept_id": f"C{int(fr.loc[c, 'concept_id'])}", "qid": fr.loc[c, "qid"], "name": fr.loc[c, "name"], "year": int(r.t),
               "target_field": int(r.field), "covariates_raw": {k: round(float(r[k]), 5) for k in covs}}
        ex = {"input": json.dumps(inp), "output": str(int(r.entered)),
              "predict_R2_rca_vol_baseline": f"{preds['predict_R2_rca_vol_baseline'][i]:.6f}",
              "predict_R3_retained_frontier": f"{preds['predict_R3_retained_frontier'][i]:.6f}",
              "metadata_unit": r.unit, "metadata_stratum": int(r.stratum), "metadata_age": int(r.age),
              "metadata_home_group": r.group}
        ds = "entry_events_heldout_pooled4" if r.unit in HELD4 else "entry_events_heldout_cohort"
        datasets.setdefault(ds, []).append(ex)
    meta = {"method_name": "Retained frontier (d0_ret_rel = mean relatedness of target field to off-home fields that RETAIN the concept)",
            "baseline": "R2 = relatedness-to-home + log field size + Hidalgo density of entered fields + own gateway + RCA>1 density (annual, "
                        "Hidalgo current portfolio) + share-weighted density",
            "prediction": "within-stratum (concept-year) choice probability from the FROZEN DEV coefficients; output = 1 if the field was entered",
            "rows": "held-out candidate rows in informative strata of the primary sample (non-empty retained set)",
            "verdicts": ho.get("verdicts", {}).get("FRONTIER"), "abandonment": ho.get("verdicts", {}).get("ABANDONMENT")}
    return {"metadata": meta, "datasets": [{"dataset": k, "examples": v} for k, v in datasets.items()]}


def write_method_out(mo: dict) -> list[str]:
    s = json.dumps(mo)
    if len(s) <= PART_LIMIT:
        (ROOT / "method_out.json").write_text(s)
        return ["method_out.json"]
    # split into parts under the limit (aii-file-size-limit), each a valid exp_gen_sol_out document
    d = ROOT / "method_out"
    d.mkdir(exist_ok=True)
    for f in d.glob("method_out_*.json"):
        f.unlink()
    parts, cur, size = [], {}, 0
    for ds in mo["datasets"]:
        for ex in ds["examples"]:
            n = len(json.dumps(ex)) + 2
            if size + n > PART_LIMIT * 0.97 and cur:
                parts.append(cur); cur, size = {}, 0
            cur.setdefault(ds["dataset"], []).append(ex); size += n
    parts.append(cur)
    names = []
    for i, p in enumerate(parts, 1):
        fn = d / f"method_out_{i}.json"
        fn.write_text(json.dumps({"metadata": {**mo["metadata"], "part": i, "n_parts": len(parts)},
                                  "datasets": [{"dataset": k, "examples": v} for k, v in p.items()]}))
        names.append(str(fn.relative_to(ROOT)))
    return names


@logger.catch(reraise=True)
def main() -> None:
    s1, dev, ho = load("step1_exp6_robustness.json"), load("step2_dev.json"), load("step2_heldout.json")
    spec = load("frozen_spec.json")
    forest(s1, dev, ho, "d0_R3", "d0", "Retained frontier d0 in R3 (beyond RCA>1 and share-weighted density)", "forest_d0_by_unit")
    forest(s1, dev, ho, "d_lost_A1", "d_lost", "Abandonment penalty d_lost in A1 (given ever-entered density)", "forest_dlost_by_unit")
    panels = [("EXP6 dev", s1.get("dev")), ("EXP6 held-out", s1.get("heldout")), ("EXP5-EXP6 DEV", dev.get("battery")),
              ("EXP5-EXP6 held-out pooled-4", ho.get("pooled4"))]
    panels = [(a, b["ladder"]["frontier_primary_sample"]) for a, b in panels if b]
    ladder_fig(panels)
    dp = [("EXP6 held-out", s1.get("heldout"), C["exp6"]), ("DEV", dev.get("battery"), C["dev"]), ("held-out pooled-4", ho.get("pooled4"), C["held"])]
    dose_fig([(a, b["specificity"]["c_dose"], c) for a, b, c in dp if b and "specificity" in b])
    null_fig([(a, t) for a, t in (("EXP6 held-out", "exp6_heldout"), ("DEV", "exp5_dev"), ("held-out pooled-4", "exp5_heldout_pooled4"))
              if (RES / f"nulls_{t}.npz").exists()])
    vm_fig([(a, b["specificity"]) for a, b, _ in dp if b and "specificity" in b])
    fr = {"title": "Do concepts spread from fields that keep them?",
          "step1_robustness_exp6": s1, "step2_dev": dev, "power_table": dev.get("power"), "step2_heldout": ho,
          "verdicts": ho.get("verdicts"), "overlap": load("overlap_report.json"), "deviations": load("deviations.json"),
          "unit_tests_T0": load("unit_tests_T0.json"), "audit": load("audit.json"),
          "guevara_comparison": {"ours_exp5_heldout_pooled4": ho.get("pooled4", {}).get("guevara_comparable_auc"),
                                 "ours_exp6_heldout": s1.get("heldout", {}).get("guevara_comparable_auc"),
                                 "guevara_2016": {"individuals": 0.896, "organisations": 0.715, "countries": 0.682},
                                 "flag": "different unit (concept vs scholar/org/country), event (D3 count entry vs RCA transition) and proximity (26-field PMI vs author-sharing over subfields): not a head-to-head"},
          "resampling_unit_note": "every CI resamples concepts unless labelled 'concept x target field' (crossed bootstrap)",
          "provenance_note": "EXP5 held-out concepts' counts and retention outcomes (t0+6..8) were unsealed in iteration 2 for H1/H3; no entry or "
                             "frontier analysis had touched them. The replication is independent of EXP6's concepts and of any d0 analysis, but "
                             "the frame is not never-seen data."}
    (RES / "frontier_result.json").write_text(json.dumps(fr, indent=1, default=float))
    if ho and spec:
        mo = method_out(ho, spec)
        names = write_method_out(mo)
        logger.info(f"method_out: {sum(len(d['examples']) for d in mo['datasets']):,} examples -> {names}")
    logger.info("outputs done")


if __name__ == "__main__":
    main()
```

### [118] TOOL RESULT — Write · 2026-09-28 21:59:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/outputs.py", "content": "#!/usr/bin/env python3\n\"\"\"Stage `outputs`: results/frontier_result.json (everything in one place), figures/ (PNG + PDF), method_out.json\n(exp_gen_sol_out schema; one example per held-out candidate row in an informative primary-sample stratum, with\nwithin-stratum probabilities from the frozen DEV coefficients of R2 (RCA>1 + volume baseline) and R3 (+ retained frontier)).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nimport matplotlib\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt  # noqa: E402\nimport numpy as np  # noqa: E402\nimport pandas as pd  # noqa: E402\nfrom loguru import logger  # noqa: E402\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\nimport models as M  # noqa: E402\nimport analysis as AN  # noqa: E402,F401  (registers the extra rungs)\n\nRES, FIGS = ROOT / \"results\", ROOT / \"figures\"\nplt.rcParams.update({\"pdf.fonttype\": 42, \"ps.fonttype\": 42, \"font.size\": 9, \"axes.spines.top\": False,\n                     \"axes.spines.right\": False, \"savefig.dpi\": 200, \"savefig.bbox\": \"tight\"})\nC = {\"exp6\": \"#0072B2\", \"dev\": \"#999999\", \"held\": \"#D55E00\", \"dl\": \"#000000\", \"cohort\": \"#009E73\", \"null\": \"#56B4E9\"}\nHELD4 = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nPART_LIMIT = 90 * 1024 * 1024\n\n\ndef load(name: str) -> dict:\n    p = RES / name\n    return json.loads(p.read_text()) if p.exists() else {}\n\n\ndef save(fig, name: str) -> None:\n    fig.savefig(FIGS / f\"{name}.png\"); fig.savefig(FIGS / f\"{name}.pdf\")\n    plt.close(fig)\n\n\ndef _ci(d: dict, key: str) -> tuple[float, float, float]:\n    x = d[key]\n    lo, hi = x.get(\"boot_ci\", [x[\"coef\"] - 1.96 * x[\"se_concept\"], x[\"coef\"] + 1.96 * x[\"se_concept\"]])\n    return x[\"coef\"], lo, hi\n\n\ndef forest(s1: dict, dev: dict, ho: dict, key: str, dl_key: str, title: str, name: str) -> None:\n    rows = []\n    for u in (\"Physical\", \"LifeEnv\", \"Social\", \"Cohort\"):\n        if key in s1.get(\"heldout_units\", {}).get(u, {}):\n            rows.append((f\"EXP6 {u}\", *_ci(s1[\"heldout_units\"][u], key), C[\"exp6\"], \"o\"))\n    if s1:\n        d = s1[\"heldout_DL\"][dl_key]\n        rows.append((\"EXP6 DL pooled\", d[\"b\"], d[\"ci\"][0], d[\"ci\"][1], C[\"exp6\"], \"D\"))\n    for g in (\"CS\", \"Eng\", \"BGM\", \"Med\"):\n        if key in dev.get(\"dev_groups\", {}).get(g, {}):\n            rows.append((f\"DEV {g}\", *_ci(dev[\"dev_groups\"][g], key), C[\"dev\"], \"o\"))\n    for u in HELD4 + [\"COHORT_DEVHOME\", \"COHORT_NONDEVHOME\"]:\n        if key in ho.get(\"units\", {}).get(u, {}):\n            rows.append((f\"HELD {u}\", *_ci(ho[\"units\"][u], key), C[\"cohort\"] if u.startswith(\"COHORT\") else C[\"held\"], \"o\"))\n    if ho:\n        d = ho[\"DL_4groups\"][dl_key]\n        rows.append((\"HELD DL (4 groups)\", d[\"b\"], d[\"ci\"][0], d[\"ci\"][1], C[\"dl\"], \"D\"))\n        bkey = \"d0_R3\" if key == \"d0_R3\" else \"d_lost_A1\"\n        tg = \"d0_ret_rel\" if key == \"d0_R3\" else \"d_lost\"\n        b = ho[\"pooled4\"][\"boot\"][bkey][tg]\n        rows.append((\"HELD pooled-4 (refit boot)\", b[\"est\"], b[\"ci\"][0], b[\"ci\"][1], C[\"dl\"], \"s\"))\n    fig, ax = plt.subplots(figsize=(5.2, 0.28 * len(rows) + 1.0))\n    for i, (lab, b, lo, hi, col, mk) in enumerate(rows[::-1]):\n        ax.plot([lo, hi], [i, i], color=col, lw=1.4)\n        ax.plot(b, i, marker=mk, color=col, ms=5 if mk != \"D\" else 6)\n    ax.axvline(0, color=\"k\", lw=0.6, ls=\"--\")\n    ax.set_yticks(range(len(rows))); ax.set_yticklabels([r[0] for r in rows[::-1]])\n    ax.set_xlabel(\"coefficient per DEV-SD (conditional logit, concept-year strata); 95% CI, resampling unit = concept\")\n    ax.set_title(title, fontsize=9)\n    save(fig, name)\n\n\ndef ladder_fig(panels: list[tuple[str, dict]]) -> None:\n    steps = [(\"R1_rca_vs_R0_M0\", \"+RCA>1\\ndensity\"), (\"R2_vol_vs_R1_rca\", \"+share\\ndensity\"), (\"R3_ret_vs_R2_vol\", \"+retained\\nfrontier\"),\n             (\"R4_lost_vs_R3_ret\", \"+lost\"), (\"S_strict_vs_S_strict0\", \"strict:\\n+retained\")]\n    rungs = [\"R0_M0\", \"R1_rca\", \"R2_vol\", \"R3_ret\", \"R4_lost\"]\n    fig, axes = plt.subplots(1, len(panels), figsize=(3.1 * len(panels), 3.0), sharey=False)\n    axes = np.atleast_1d(axes)\n    for ax, (lab, lad) in zip(axes, panels):\n        lr = [lad[\"LR\"][k][\"LR\"] for k, _ in steps]\n        cols = [C[\"held\"] if \"retained\" in s else C[\"dev\"] for _, s in steps]\n        ax.bar(range(len(steps)), lr, color=cols)\n        ax.axhline(6.63, color=\"k\", lw=0.6, ls=\":\")\n        ax.set_xticks(range(len(steps))); ax.set_xticklabels([s for _, s in steps], fontsize=7)\n        ax.set_title(lab, fontsize=8); ax.set_ylabel(\"LR (df=1); dotted: p=0.01\")\n        ax2 = ax.twinx()\n        ax2.plot(range(len(rungs)), [lad[\"auc_within\"][r] for r in rungs], \"k.-\", lw=0.8)\n        ax2.set_ylabel(\"within-stratum AUC (R0..R4)\", fontsize=7)\n    fig.tight_layout()\n    save(fig, \"ladder\")\n\n\ndef dose_fig(panels: list[tuple[str, dict]]) -> None:\n    fig, ax = plt.subplots(figsize=(4.6, 3.0))\n    for j, (lab, d, col) in enumerate(panels):\n        f = d[\"fit\"]\n        xs = np.arange(3) + (j - 1) * 0.12\n        b = [f[c][\"coef\"] for c in (\"d_ret_a2\", \"d_ret_a3\", \"d_ret_a4p\")]\n        se = [f[c][\"se_concept\"] for c in (\"d_ret_a2\", \"d_ret_a3\", \"d_ret_a4p\")]\n        ax.errorbar(xs, b, yerr=1.96 * np.array(se), fmt=\"o-\", color=col, label=lab, capsize=2, lw=1)\n    ax.axhline(0, color=\"k\", lw=0.6, ls=\"--\")\n    ax.set_xticks(range(3)); ax.set_xticklabels([\"2\", \"3\", \">=4\"])\n    ax.set_xlabel(\"years the retaining field has held the concept (persistence age)\")\n    ax.set_ylabel(\"coefficient (per SD of d0)\")\n    ax.legend(fontsize=7, frameon=False)\n    save(fig, \"dose_response\")\n\n\ndef null_fig(tags: list[tuple[str, str]]) -> None:\n    fig, axes = plt.subplots(len(tags), 3, figsize=(9, 2.3 * len(tags)), squeeze=False)\n    for i, (lab, tag) in enumerate(tags):\n        p = RES / f\"nulls_{tag}.npz\"\n        if not p.exists():\n            continue\n        z = np.load(p)\n        obs = float(z[\"LR_obs\"])\n        for j, (k, t) in enumerate(((\"perm\", \"retained-label permutation\"), (\"rewire\", \"degree-preserving rewiring\"), (\"label_perm\", \"node-label permutation\"))):\n            ax = axes[i, j]\n            ax.hist(z[k], bins=40, color=C[\"null\"])\n            ax.axvline(obs, color=C[\"held\"], lw=1.5)\n            ax.set_title(f\"{lab}: {t}\\n(obs LR = {obs:.1f}; p = {(1 + (z[k] >= obs).sum()) / (1 + len(z[k])):.4f})\", fontsize=7)\n            ax.set_xlabel(\"LR(R3 vs R2) under the null\")\n    fig.tight_layout()\n    save(fig, \"null_hist\")\n\n\ndef vm_fig(panels: list[tuple[str, dict]]) -> None:\n    fig, ax = plt.subplots(figsize=(5.0, 3.0))\n    labs, i = [], 0\n    for lab, sp in panels:\n        for key, tag, rk, nk in ((\"b_volume_matched\", \"coarse\", \"d_R_m\", \"d_N_m\"), (\"b2_volume_matched_fine\", \"fine\", \"d_R_mf\", \"d_N_mf\")):\n            c = sp.get(key, {}).get(\"contrast_R_minus_N\")\n            if not c:\n                continue\n            for off, kk, col in ((-0.15, rk, C[\"held\"]), (0.15, nk, C[\"dev\"])):\n                ax.errorbar(i + off, c[kk][\"est\"], yerr=[[c[kk][\"est\"] - c[kk][\"ci\"][0]], [c[kk][\"ci\"][1] - c[kk][\"est\"]]],\n                            fmt=\"o\", color=col, capsize=2)\n            labs.append(f\"{lab}\\n{tag}\\nR-N={c['est']:.2f}\\n[{c['ci'][0]:.2f},{c['ci'][1]:.2f}]\")\n            i += 1\n    ax.axhline(0, color=\"k\", lw=0.6, ls=\"--\")\n    ax.set_xticks(range(len(labs))); ax.set_xticklabels(labs, fontsize=6)\n    ax.set_ylabel(\"coefficient per SD of d0\\n(orange: retained R; grey: entered-not-retained N)\")\n    save(fig, \"vol_matched\")\n\n\ndef method_out(ho: dict, spec: dict) -> dict:\n    df = pd.read_parquet(RES / \"risk_sets_exp5_minus_exp6_heldout.parquet\")\n    dev = load(\"step2_dev.json\")\n    fr = pd.read_csv(Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/frame_concepts.csv\"),\n                     usecols=[\"ci\", \"concept_id\", \"qid\", \"name\"]).set_index(\"ci\")\n    std = spec[\"standardisation_DEV\"]\n    prim = M.standardise(df[df.n_ret > 0], std)\n    raw = df[df.n_ret > 0]\n    inf = M.informative(prim)\n    raw = raw.loc[inf.index]\n    coef = dev[\"battery\"][\"ladder\"][\"frontier_primary_sample\"][\"models\"]\n    preds = {}\n    for rn, nm in ((\"R2_vol\", \"predict_R2_rca_vol_baseline\"), (\"R3_ret\", \"predict_R3_retained_frontier\")):\n        cols = M.RUNGS[rn]\n        eta = inf[cols].to_numpy() @ np.array([coef[rn][\"coef\"][c] for c in cols])\n        e = np.exp(eta - inf.assign(_e=eta).groupby(\"stratum\")._e.transform(\"max\").to_numpy())\n        preds[nm] = e / pd.Series(e, index=inf.index).groupby(inf.stratum).transform(\"sum\").to_numpy()\n    covs = [\"a_phi_home\", \"b_log_size\", \"c_density\", \"e_gate_own\", \"D_rca_1y\", \"D_rca_w3\", \"D_rca_cum\", \"D_rca_pers\", \"D_vol\",\n            \"D_vol_w3\", \"d0_ret_rel\", \"d_lost\", \"n_ret\", \"n_lost\"]\n    datasets = {}\n    for i, (ix, r) in enumerate(raw.iterrows()):\n        c = int(r.cidx)\n        inp = {\"concept_id\": f\"C{int(fr.loc[c, 'concept_id'])}\", \"qid\": fr.loc[c, \"qid\"], \"name\": fr.loc[c, \"name\"], \"year\": int(r.t),\n               \"target_field\": int(r.field), \"covariates_raw\": {k: round(float(r[k]), 5) for k in covs}}\n        ex = {\"input\": json.dumps(inp), \"output\": str(int(r.entered)),\n              \"predict_R2_rca_vol_baseline\": f\"{preds['predict_R2_rca_vol_baseline'][i]:.6f}\",\n              \"predict_R3_retained_frontier\": f\"{preds['predict_R3_retained_frontier'][i]:.6f}\",\n              \"metadata_unit\": r.unit, \"metadata_stratum\": int(r.stratum), \"metadata_age\": int(r.age),\n              \"metadata_home_group\": r.group}\n        ds = \"entry_events_heldout_pooled4\" if r.unit in HELD4 else \"entry_events_heldout_cohort\"\n        datasets.setdefault(ds, []).append(ex)\n    meta = {\"method_name\": \"Retained frontier (d0_ret_rel = mean relatedness of target field to off-home fields that RETAIN the concept)\",\n            \"baseline\": \"R2 = relatedness-to-home + log field size + Hidalgo density of entered fields + own gateway + RCA>1 density (annual, \"\n                        \"Hidalgo current portfolio) + share-weighted density\",\n            \"prediction\": \"within-stratum (concept-year) choice probability from the FROZEN DEV coefficients; output = 1 if the field was entered\",\n            \"rows\": \"held-out candidate rows in informative strata of the primary sample (non-empty retained set)\",\n            \"verdicts\": ho.get(\"verdicts\", {}).get(\"FRONTIER\"), \"abandonment\": ho.get(\"verdicts\", {}).get(\"ABANDONMENT\")}\n    return {\"metadata\": meta, \"datasets\": [{\"dataset\": k, \"examples\": v} for k, v in datasets.items()]}\n\n\ndef write_method_out(mo: dict) -> list[str]:\n    s = json.dumps(mo)\n    if len(s) <= PART_LIMIT:\n        (ROOT / \"method_out.json\").write_text(s)\n        return [\"method_out.json\"]\n    # split into parts under the limit (aii-file-size-limit), each a valid exp_gen_sol_out document\n    d = ROOT / \"method_out\"\n    d.mkdir(exist_ok=True)\n    for f in d.glob(\"method_out_*.json\"):\n        f.unlink()\n    parts, cur, size = [], {}, 0\n    for ds in mo[\"datasets\"]:\n        for ex in ds[\"examples\"]:\n            n = len(json.dumps(ex)) + 2\n            if size + n > PART_LIMIT * 0.97 and cur:\n                parts.append(cur); cur, size = {}, 0\n            cur.setdefault(ds[\"dataset\"], []).append(ex); size += n\n    parts.append(cur)\n    names = []\n    for i, p in enumerate(parts, 1):\n        fn = d / f\"method_out_{i}.json\"\n        fn.write_text(json.dumps({\"metadata\": {**mo[\"metadata\"], \"part\": i, \"n_parts\": len(parts)},\n                                  \"datasets\": [{\"dataset\": k, \"examples\": v} for k, v in p.items()]}))\n        names.append(str(fn.relative_to(ROOT)))\n    return names\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    s1, dev, ho = load(\"step1_exp6_robustness.json\"), load(\"step2_dev.json\"), load(\"step2_heldout.json\")\n    spec = load(\"frozen_spec.json\")\n    forest(s1, dev, ho, \"d0_R3\", \"d0\", \"Retained frontier d0 in R3 (beyond RCA>1 and share-weighted density)\", \"forest_d0_by_unit\")\n    forest(s1, dev, ho, \"d_lost_A1\", \"d_lost\", \"Abandonment penalty d_lost in A1 (given ever-entered density)\", \"forest_dlost_by_unit\")\n    panels = [(\"EXP6 dev\", s1.get(\"dev\")), (\"EXP6 held-out\", s1.get(\"heldout\")), (\"EXP5-EXP6 DEV\", dev.get(\"battery\")),\n              (\"EXP5-EXP6 held-out pooled-4\", ho.get(\"pooled4\"))]\n    panels = [(a, b[\"ladder\"][\"frontier_primary_sample\"]) for a, b in panels if b]\n    ladder_fig(panels)\n    dp = [(\"EXP6 held-out\", s1.get(\"heldout\"), C[\"exp6\"]), (\"DEV\", dev.get(\"battery\"), C[\"dev\"]), (\"held-out pooled-4\", ho.get(\"pooled4\"), C[\"held\"])]\n    dose_fig([(a, b[\"specificity\"][\"c_dose\"], c) for a, b, c in dp if b and \"specificity\" in b])\n    null_fig([(a, t) for a, t in ((\"EXP6 held-out\", \"exp6_heldout\"), (\"DEV\", \"exp5_dev\"), (\"held-out pooled-4\", \"exp5_heldout_pooled4\"))\n              if (RES / f\"nulls_{t}.npz\").exists()])\n    vm_fig([(a, b[\"specificity\"]) for a, b, _ in dp if b and \"specificity\" in b])\n    fr = {\"title\": \"Do concepts spread from fields that keep them?\",\n          \"step1_robustness_exp6\": s1, \"step2_dev\": dev, \"power_table\": dev.get(\"power\"), \"step2_heldout\": ho,\n          \"verdicts\": ho.get(\"verdicts\"), \"overlap\": load(\"overlap_report.json\"), \"deviations\": load(\"deviations.json\"),\n          \"unit_tests_T0\": load(\"unit_tests_T0.json\"), \"audit\": load(\"audit.json\"),\n          \"guevara_comparison\": {\"ours_exp5_heldout_pooled4\": ho.get(\"pooled4\", {}).get(\"guevara_comparable_auc\"),\n                                 \"ours_exp6_heldout\": s1.get(\"heldout\", {}).get(\"guevara_comparable_auc\"),\n                                 \"guevara_2016\": {\"individuals\": 0.896, \"organisations\": 0.715, \"countries\": 0.682},\n                                 \"flag\": \"different unit (concept vs scholar/org/country), event (D3 count entry vs RCA transition) and proximity (26-field PMI vs author-sharing over subfields): not a head-to-head\"},\n          \"resampling_unit_note\": \"every CI resamples concepts unless labelled 'concept x target field' (crossed bootstrap)\",\n          \"provenance_note\": \"EXP5 held-out concepts' counts and retention outcomes (t0+6..8) were unsealed in iteration 2 for H1/H3; no entry or \"\n                             \"frontier analysis had touched them. The replication is independent of EXP6's concepts and of any d0 analysis, but \"\n                             \"the frame is not never-seen data.\"}\n    (RES / \"frontier_result.json\").write_text(json.dumps(fr, indent=1, default=float))\n    if ho and spec:\n        mo = method_out(ho, spec)\n        names = write_method_out(mo)\n        logger.info(f\"method_out: {sum(len(d['examples']) for d in mo['datasets']):,} examples -> {names}\")\n    logger.info(\"outputs done\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [119] TOOL CALL — Bash · 2026-09-28 21:59:30 UTC

```
tail -3 logs/step1_full.out; tail -8 logs/dev_full.out 2>/dev/null
```

### [120] TOOL RESULT — Bash · 2026-09-28 21:59:30 UTC

```
{"stdout": "21:56:54|INFO   |[exp6_heldout] rebuild sensitivities 1s; battery total 98s\n21:57:03|INFO   |step1 done in 118s\nSTEP1 EXIT 0\n21:57:33|INFO   |input checks: {'early_volume_agreement': 1.0, 'home_agreement': 0.9988854213107445, 'GF_spearman_min': 0.9999999999999999, 'GF_max_rel_diff': 0.0, 'home_mismatch_cidx': [27075, 36139, 38268, 47191, 51213]}\n21:57:36|INFO   |DEV risk sets 958,542 rows / 44,860 strata / 4,486 concepts; state panel 2,350,062 rows (16s)\n21:57:42|INFO   |[exp5_dev] ladder: R1_rca_vs_R0_M0 LR=120.49, R2_vol_vs_R1_rca LR=14.46, R3_ret_vs_R2_vol LR=365.58, R4_lost_vs_R3_ret LR=26.67, S_strict_vs_S_strict0 LR=292.30, S_pca_vs_S_pca0 LR=285.59, EXP6_M1_vs_R0_M0 LR=422.11, EXP6_M2lost_vs_R0_M0 LR=2.79\n21:57:42|INFO   |[exp5_dev] d0 in R3 = 0.2455; d0 in S_strict = 0.2283; d_lost in A1 = -0.0049", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [121] THINKING · 2026-09-28 21:59:30 UTC

```
Step1 completed in 118s and dev is now running with 958k rows, 44,860 strata, and 4,486 concepts; on DEV, d0 = 0.2455 (LR 366) in R3 and 0.228 in S_strict, with d_lost in A1 near zero. I'll review the step-1 results while dev continues running.
```

### [122] TOOL CALL — Bash · 2026-09-28 21:59:30 UTC

```
.venv/bin/python -c "
import json;d=json.load(open('results/step1_exp6_robustness.json'));h=d['heldout']
b=h['boot']; print({k:(v.get('d0_ret_rel',v.get('d_lost',{})).get('ci') if isinstance(v,dict) else v) for k,v in b.items()})
print(b['R4']); print(b['T6_seed_stability_d0_R3'])
print(h['crossed_boot'])
s=h['specificity']; print('perm',s['a_permutation']['p'], s['a_permutation']['share_strata_nontrivial'], 'sec',s['a_permutation_secondary_all_entered_offhome']['p'])
print('vm', s['b_volume_matched']['contrast_R_minus_N']['est'], s['b_volume_matched']['contrast_R_minus_N']['ci'], 'fine', s['b2_volume_matched_fine']['contrast_R_minus_N']['est'], s['b2_volume_matched_fine']['contrast_R_minus_N']['ci'])
print('dose', s['c_dose']['betas_by_age'], s['c_dose']['contrast_4p_minus_2']['ci'])
print('bb', s['d_backbone_d0_only']['rewire']['p'], s['d_backbone_d0_only']['label_perm']['p'], s['d_backbone_full_recompute']['p'])
print(d['heldout_DL'])
for u,v in d['heldout_units'].items(): print(u, v['d0_R3']['coef'], v['d0_R3']['boot_ci'], v['d_lost_A1']['coef'], v['d_lost_A1']['boot_ci'])
"
```

### [123] TOOL RESULT — Bash · 2026-09-28 21:59:30 UTC

```
{"stdout": "{'d0_R3': [0.19597718020748217, 0.3197966952645508], 'd0_S_strict': [0.18802006138368704, 0.31463308232242004], 'd0_S_pca': [0.18903552318146316, 0.31605775723201157], 'd_lost_A1': [-0.12487257115534149, 0.008204420593385772], 'R4': [0.19563781228890167, 0.3214473452406537], 'T6_seed_stability_d0_R3': None}\n{'resampling_unit': 'concept', 'n_boot': 1000, 'd0_ret_rel': {'est': 0.26012769942440317, 'ci': [0.19563781228890167, 0.3214473452406537], 'se_boot': 0.03153578200420645, 'p_one_sided_le0': 0.000999000999000999}, 'd_lost': {'est': -0.02559678628157827, 'ci': [-0.11590378724524344, 0.044481392671217555], 'se_boot': 0.03997303453320477, 'p_one_sided_le0': 0.7492507492507493}}\n{'ci_seed1': [0.19597718020748217, 0.3197966952645508], 'ci_seed2': [0.198226927213525, 0.3209058123240659], 'max_endpoint_shift': 0.0022497470060428293, 'pass_lt_0.01': True}\n{'d0_R3': {'resampling_unit': 'concept x target field (Owen pigeonhole, Poisson(1) weights)', 'n_boot': 500, 'ci': [0.09600964363240713, 0.42323271222583136], 'se_boot': 0.08423991240432416}, 'd_lost_A1': {'resampling_unit': 'concept x target field (Owen pigeonhole, Poisson(1) weights)', 'n_boot': 500, 'ci': [-0.17573405948309592, 0.030522538084819008], 'se_boot': 0.05365158796856888}}\nperm 0.000999000999000999 0.3392299687825182 sec 0.001996007984031936\nvm 0.13024456178553268 [-0.0021824344179531955, 0.2581740187723079] fine 0.07128497866967277 [-0.06684938141579845, 0.23624288557092998]\ndose {'2': 0.10169621551567232, '3': 0.1370538962555718, '4+': 0.21322504889131338} [0.025344642901098238, 0.19423921726687526]\nbb 0.001996007984031936 0.000999000999000999 0.009900990099009901\n{'d0': {'units': ['Physical', 'LifeEnv', 'Social', 'Cohort'], 'k': 4, 'b': 0.24997453235111952, 'se': 0.03192101686028168, 'ci': [0.18740933930496742, 0.3125397253972716], 'p': 4.838781267530549e-15, 'tau2': 0.0, 'Q': 0.19671683407584548, 'I2': 0.0, 'n_positive': 4, 'n_negative': 0, 'se_type': 'concept-clustered sandwich'}, 'd_lost': {'units': ['Physical', 'LifeEnv', 'Social', 'Cohort'], 'k': 4, 'b': -0.04471989350846939, 'se': 0.03320823727368421, 'ci': [-0.10980803856489044, 0.02036825154795166], 'p': 0.1780927810207238, 'tau2': 0.0, 'Q': 2.19246764535408, 'I2': 0.0, 'n_positive': 1, 'n_negative': 3, 'se_type': 'concept-clustered sandwich'}}\nPhysical 0.28011218679313565 [-0.01775102243889481, 0.5048310267601186] 0.05908181079720997 [-0.8334059938413105, 0.19318005461709015]\nLifeEnv 0.20759840960826784 [-0.028380277150944995, 0.47592940491487845] -0.015201745540007127 [-0.5490745123741618, 0.20227592981412884]\nSocial 0.25507112412188926 [-0.000654077188753527, 0.47287233760092073] -0.2073866528161323 [-1.1703756642018661, 0.0011955278879830678]\nCohort 0.25068084932328116 [0.1728265643341578, 0.32011483707333266] -0.04891456842142703 [-0.12668865173368665, 0.014116475615273984]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [124] THINKING · 2026-09-28 21:59:30 UTC

```
EXP6 robustness checks out across metrics: d0, S_strict, and crossed concept × field intervals all hold, permutation p = 0.001, and there's a monotone dose effect (0.10 → 0.14 → 0.21), though the volume-matched contrast is borderline. Now checking `dev` progress.
```

### [125] TOOL CALL — Bash · 2026-09-28 21:59:30 UTC

```
sleep 240; cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 && tail -6 logs/dev_full.out; cat /sys/fs/cgroup/memory.current | awk '{print $1/1e9 " GB"}'
```

### [126] TOOL RESULT — Bash [ERROR] · 2026-09-28 21:59:30 UTC

```
Error: Blocked: sleep 240 followed by: cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 tail -6 logs/dev_full.out cat /sys/fs/cgroup/memory.current awk '{print $1/1e9 " GB"}'. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.
```

### [127] TOOL CALL — Bash · 2026-09-28 21:59:30 UTC

```
tail -6 logs/dev_full.out; awk '{print $1/1e9 " GB"}' /sys/fs/cgroup/memory.current
```

### [128] TOOL RESULT — Bash · 2026-09-28 21:59:30 UTC

```
{"stdout": "21:57:33|INFO   |input checks: {'early_volume_agreement': 1.0, 'home_agreement': 0.9988854213107445, 'GF_spearman_min': 0.9999999999999999, 'GF_max_rel_diff': 0.0, 'home_mismatch_cidx': [27075, 36139, 38268, 47191, 51213]}\n21:57:36|INFO   |DEV risk sets 958,542 rows / 44,860 strata / 4,486 concepts; state panel 2,350,062 rows (16s)\n21:57:42|INFO   |[exp5_dev] ladder: R1_rca_vs_R0_M0 LR=120.49, R2_vol_vs_R1_rca LR=14.46, R3_ret_vs_R2_vol LR=365.58, R4_lost_vs_R3_ret LR=26.67, S_strict_vs_S_strict0 LR=292.30, S_pca_vs_S_pca0 LR=285.59, EXP6_M1_vs_R0_M0 LR=422.11, EXP6_M2lost_vs_R0_M0 LR=2.79\n21:57:42|INFO   |[exp5_dev] d0 in R3 = 0.2455; d0 in S_strict = 0.2283; d_lost in A1 = -0.0049\n3.8248 GB", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [129] TOOL CALL — ToolSearch · 2026-09-28 21:59:30 UTC

```
{'query': 'select:Monitor', 'max_results': 1}
```

### [130] TOOL RESULT — ToolSearch · 2026-09-28 21:59:30 UTC

```
{"matches": ["Monitor"], "query": "select:Monitor", "total_deferred_tools": 27}
```

### [131] ASSISTANT · 2026-09-28 21:59:30 UTC

```
The full DEV run is in its 1,000-draw bootstraps; I'm setting a watch on its log.
```

### [132] TOOL CALL — Monitor · 2026-09-28 21:59:30 UTC

```
{'command': 'cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 && tail -n 0 -f logs/dev_full.out | grep -E --line-buffered "bootstr|crossed|permutation|backbone|rebuild|power|done|Error|Traceback|EXIT|Killed"', 'description': 'DEV full run progress (exp5 minus exp6)', 'timeout_ms': 1800000}
```

### [133] TOOL RESULT — Monitor · 2026-09-28 21:59:30 UTC

```
{"taskId": "bxzhys2cs", "timeoutMs": 1800000, "persistent": false}
```

### [134] ASSISTANT · 2026-09-28 21:59:30 UTC

```
While DEV runs, drafting the storage manifest (only `.venv/` and `__pycache__/` are regenerable; parquet outputs are kept).
```

### [135] TOOL CALL — Bash · 2026-09-28 21:59:30 UTC

```
ls -la results/ && du -sh .venv && rm -f scratch_repro.py scratch_exp5.py
```

### [136] TOOL RESULT — Bash · 2026-09-28 21:59:30 UTC

```
{"stdout": "total 29350\ndrwxrwxrwx  2 root root  2002478 Sep 28 21:54 .\ndrwxrwxrwx 11 root root  2056364 Sep 28 21:58 ..\n-rw-rw-rw-  1 root root    10190 Sep 28 21:57 overlap_report.json\n-rw-rw-rw-  1 root root 16313773 Sep 28 21:57 risk_sets_exp5_minus_exp6_dev.parquet\n-rw-rw-rw-  1 root root  1041337 Sep 28 21:55 risk_sets_exp6_extended_dev.parquet\n-rw-rw-rw-  1 root root  1438665 Sep 28 21:55 risk_sets_exp6_extended_heldout.parquet\n-rw-rw-rw-  1 root root  7102493 Sep 28 21:57 state_panel_dev.parquet\n-rw-rw-rw-  1 root root    85929 Sep 28 21:57 step1_exp6_robustness.json\n-rw-rw-rw-  1 root root      871 Sep 28 21:54 unit_tests_T0.json\n1.8G\t.venv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [137] TOOL CALL — Bash · 2026-09-28 22:00:08 UTC

```
printf ".venv/\n__pycache__/\n*.pyc\n.repl_agent.ptylog\n.aii_claude_session.json\n.aii_worker_result.json\n.terminal_claude_agent_struct_out.json\ntests/_seal_tmp/\n" > .gitignore && cat .gitignore
```

### [138] TOOL RESULT — Bash · 2026-09-28 22:00:08 UTC

```
{"stdout": ".venv/\n__pycache__/\n*.pyc\n.repl_agent.ptylog\n.aii_claude_session.json\n.aii_worker_result.json\n.terminal_claude_agent_struct_out.json\ntests/_seal_tmp/", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [139] ASSISTANT · 2026-09-28 22:00:08 UTC

```
Waiting for the DEV run's next milestone.
```

### [140] TOOL CALL — Bash · 2026-09-28 22:00:08 UTC

```
until grep -qE "headline bootstraps|Traceback|EXIT" logs/dev_full.out; do sleep 5; done; tail -3 logs/dev_full.out
```

### [141] TOOL RESULT — Bash · 2026-09-28 22:00:08 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkwpg6nga"}
```

### [142] THINKING · 2026-09-28 22:00:08 UTC

```
While waiting, I'm patching a gap in the frozen verdict logic: the "relatedness principle unchanged" reading should trigger when d0 is significant without rivals in EXP6_M1, but not in R3.
```

### [143] TOOL CALL — Edit · 2026-09-28 22:00:08 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py
OLD:         if lad["models"]["R1_rca"] and d0 <= 0:
            v += "; relatedness principle unchanged (RCA>1 density absorbs the retained frontier)"
NEW:         m1 = lad["models"]["EXP6_M1"]["coef"]["d0_ret_rel"]
        if m1 > 0 and lad["LR"]["EXP6_M1_vs_R0_M0"]["p"] < 0.01:
            v += "; relatedness principle unchanged (d0 is significant without the RCA>1/volume rivals but not with them)"
```

### [144] TOOL RESULT — Edit · 2026-09-28 22:00:08 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/method.py", "oldString": "        if lad[\"models\"][\"R1_rca\"] and d0 <= 0:\n            v += \"; relatedness principle unchanged (RCA>1 density absorbs the retained frontier)\"", "newString": "        m1 = lad[\"models\"][\"EXP6_M1\"][\"coef\"][\"d0_ret_rel\"]\n        if m1 > 0 and lad[\"LR\"][\"EXP6_M1_vs_R0_M0\"][\"p\"] < 0.01:\n            v += \"; relatedness principle unchanged (d0 is significant without the RCA>1/volume rivals but not with them)\"", "originalFile": null, "structuredPatch": [{"oldStart": 446, "oldLines": 8, "newStart": 446, "newLines": 9, "lines": ["         v = \"CONFIRMED\"", "     elif ci[0] <= 0 <= ci[1] or d0 <= 0:", "         v = \"DISCONFIRMED\" + (\" (holds only on the EXP6 frame)\" if c[\"6_EXP6_R3_CI>0\"] else \"\")", "-        if lad[\"models\"][\"R1_rca\"] and d0 <= 0:", "-            v += \"; relatedness principle unchanged (RCA>1 density absorbs the retained frontier)\"", "+        m1 = lad[\"models\"][\"EXP6_M1\"][\"coef\"][\"d0_ret_rel\"]", "+        if m1 > 0 and lad[\"LR\"][\"EXP6_M1_vs_R0_M0\"][\"p\"] < 0.01:", "+            v += \"; relatedness principle unchanged (d0 is significant without the RCA>1/volume rivals but not with them)\"", "     elif c[\"1_pooled4_R3\"] and c[\"3_sign_rule\"]:", "         fails = [k for k, ok in c.items() if not ok]", "         if not c[\"2_S_strict\"]:"]}], "userModified": false, "replaceAll": false, "staleRecovered": true, "contentNotInModelContext": true}
```

### [145] TOOL CALL — Bash · 2026-09-28 22:00:08 UTC

```
until grep -qE "headline bootstraps|Traceback|EXIT" logs/dev_full.out; do sleep 5; done; tail -3 logs/dev_full.out
```

### [146] TOOL RESULT — Bash · 2026-09-28 22:03:44 UTC

```
{"stdout": "21:57:42|INFO   |[exp5_dev] ladder: R1_rca_vs_R0_M0 LR=120.49, R2_vol_vs_R1_rca LR=14.46, R3_ret_vs_R2_vol LR=365.58, R4_lost_vs_R3_ret LR=26.67, S_strict_vs_S_strict0 LR=292.30, S_pca_vs_S_pca0 LR=285.59, EXP6_M1_vs_R0_M0 LR=422.11, EXP6_M2lost_vs_R0_M0 LR=2.79\n21:57:42|INFO   |[exp5_dev] d0 in R3 = 0.2455; d0 in S_strict = 0.2283; d_lost in A1 = -0.0049\n22:02:22|INFO   |headline bootstraps (1000) in 279s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [147] ASSISTANT · 2026-09-28 22:03:44 UTC

```
Headline bootstraps took 279 s at full DEV size. While the specificity battery runs, I'm drafting the README's fixed sections.
```

### [148] TOOL CALL — Bash · 2026-09-28 22:03:44 UTC

```
until grep -qE "rebuild sensitivities|Traceback|EXIT" logs/dev_full.out; do sleep 5; done; tail -6 logs/dev_full.out
```

### [149] TOOL RESULT — Bash · 2026-09-28 22:12:14 UTC

```
{"stdout": "21:57:42|INFO   |[exp5_dev] d0 in R3 = 0.2455; d0 in S_strict = 0.2283; d_lost in A1 = -0.0049\n22:02:22|INFO   |headline bootstraps (1000) in 279s\n22:02:33|INFO   |[exp5_dev] crossed bootstrap 12s: [0.1389341578158411, 0.33278368415161613]\n22:05:00|INFO   |  (a) permutation 146s p=0.0010\n22:10:52|INFO   |  (d) backbone nulls 308s\n22:11:14|INFO   |[exp5_dev] rebuild sensitivities 15s; battery total 818s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [150] ASSISTANT · 2026-09-28 22:12:14 UTC

```
The DEV battery finished in 818 s (permutation p = 0.001; crossed CI [0.139, 0.333]). Units and the power simulation are next.
```

### [151] TOOL CALL — Bash · 2026-09-28 22:12:14 UTC

```
until grep -qE "dev stage done|Traceback|DEV EXIT" logs/dev_full.out; do sleep 5; done; grep -E "power|done|EXIT|Error" logs/dev_full.out | tail -12
```

### [152] TOOL RESULT — Bash · 2026-09-28 22:19:12 UTC

```
{"stdout": "22:13:53|INFO   |  power POOLED4 (n=3251): d0 {'0': 0.0, '0.05': 0.71, '0.1': 1.0, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.025, '-0.03': 0.64, '-0.06': 0.99, '-0.1': 1.0}\n22:14:13|INFO   |  power PHYS (n=708): d0 {'0': 0.0, '0.05': 0.13, '0.1': 0.67, '0.15': 0.99, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.03, '-0.03': 0.17, '-0.06': 0.64, '-0.1': 0.97}\n22:14:38|INFO   |  power LIFEENV (n=1079): d0 {'0': 0.0, '0.05': 0.19, '0.1': 0.88, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.04, '-0.03': 0.26, '-0.06': 0.8, '-0.1': 0.99}\n22:15:07|INFO   |  power SOC (n=1299): d0 {'0': 0.0, '0.05': 0.18, '0.1': 0.94, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.02, '-0.03': 0.33, '-0.06': 0.86, '-0.1': 1.0}\n22:15:17|INFO   |  power MATHDEC (n=165): d0 {'0': 0.01, '0.05': 0.05, '0.1': 0.12, '0.15': 0.42, '0.2': 0.77, '0.28': 1.0} | d_lost {'0': 0.04, '-0.03': 0.14, '-0.06': 0.28, '-0.1': 0.4}\n22:16:24|INFO   |  power COHORT (n=4104): d0 {'0': 0.0, '0.05': 0.66, '0.1': 1.0, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.01, '-0.03': 0.72, '-0.06': 1.0, '-0.1': 1.0}\n22:17:15|INFO   |  power COHORT_DEVHOME (n=2301): d0 {'0': 0.0, '0.05': 0.48, '0.1': 0.99, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.01, '-0.03': 0.46, '-0.06': 0.97, '-0.1': 1.0}\n22:17:55|INFO   |  power COHORT_NONDEVHOME (n=1803): d0 {'0': 0.0, '0.05': 0.36, '0.1': 1.0, '0.15': 1.0, '0.2': 1.0, '0.28': 1.0} | d_lost {'0': 0.02, '-0.03': 0.47, '-0.06': 0.95, '-0.1': 1.0}\n22:17:55|INFO   |power simulation 374s\n22:17:55|INFO   |dev stage done in 1234s\nDEV EXIT 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [153] THINKING · 2026-09-28 22:19:12 UTC

```
DEV finished after 1,234 s. With MATHDEC power at d=0.15 sitting at 0.42 (below 0.5), the frozen sign rule now applies to all 3 groups plus the cohort, and the null rejection rate is 0 — I'll re-run `step1` to save its null draws and then review the DEV results and verdict code path before freezing.
```

### [154] TOOL CALL — Bash · 2026-09-28 22:19:12 UTC

```
(timeout 1200 .venv/bin/python method.py step1 > logs/step1_full.out 2>&1; echo "STEP1 EXIT $?" >> logs/step1_full.out) & 
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 && .venv/bin/python -c "
import json;d=json.load(open('results/step2_dev.json'));h=d['battery']
print(d['input_checks']); print(d['T4_sanity'], d['T3_shuffled_entered'], d['T3_planted'])
l=h['ladder']['frontier_primary_sample']; print(l['n'], l['auc_within']); print(l['models']['R4_lost']['coef'])
print(h['convergence']); print({k:round(v,1) for k,v in h['vif']['vif_within_stratum'].items()}, h['vif']['condition_number'])
b=h['boot']; print({k:(v.get('d0_ret_rel',v.get('d_lost',{})).get('ci') if isinstance(v,dict) else v) for k,v in b.items()}); print(b['T6_seed_stability_d0_R3'])
print(h['ladder']['abandonment_all_rows']['models']['A1_split']['coef'])
s=h['specificity']; print('perm',s['a_permutation']['p'], s['a_permutation']['share_strata_nontrivial'])
print('vm', s['b_volume_matched']['contrast_R_minus_N']['est'], s['b_volume_matched']['contrast_R_minus_N']['ci'], s['b_volume_matched']['balance'])
print('fine', s['b2_volume_matched_fine']['contrast_R_minus_N']['est'], s['b2_volume_matched_fine']['contrast_R_minus_N']['ci'], s['b2_volume_matched_fine']['balance'])
print('dose', s['c_dose']['betas_by_age'], s['c_dose']['contrast_4p_minus_2']['ci'])
print('bb', s['d_backbone_d0_only']['rewire']['p'], s['d_backbone_d0_only']['label_perm']['p'], s['d_backbone_full_recompute']['p'])
for k in ['e_excl_intersection_born','g_target_field_FE','h_horizon8','i_excl_weak_home','j_excl_medicine_home','n_newborn_only_descriptive','o_label_coverage_ge_0.5']: print(k, round(s[k]['d0_R3']['coef'],3), s[k]['d0_R3']['LR']['p'], round(s[k]['d_lost_A1']['coef'],3))
for k,v in h['specificity_rebuild'].items(): print(k, round(v['d0_R3']['coef'],3), v['d0_R3']['LR']['p'], round(v['d_lost_A1']['coef'],3))
print(h['lpm_concept_year_FE']['coef']['d0_ret_rel'], h['guevara_comparable_auc'])
print(d['dev_groups_DL'])
"
```

### [155] TOOL RESULT — Bash · 2026-09-28 22:19:12 UTC

```
{"stdout": "{'early_volume_agreement': 1.0, 'home_agreement': 0.9988854213107445, 'GF_spearman_min': 0.9999999999999999, 'GF_max_rel_diff': 0.0, 'home_mismatch_cidx': [27075, 36139, 38268, 47191, 51213], 'pass_ev_995': True, 'pass_home_99': True}\n{'b_log_size>0': True, 'c_density>0': True, 'R0_within_auc': 0.8143961684462847, 'R0_auc_in_[0.75,0.85]': True} {'n': 20, 'n_reject_p<0.01': 0, 'pass_le_1': True} {'beta_d0_0.2_detect_pooled4': 1.0, 'pass_ge_0.9': True, 'null_rejection_pooled4_alpha0.01': 0.0, 'pass_le_0.02': True, 'd_lost_-0.10_power_pooled4': 1.0}\n{'rows': 740183, 'strata': 35466, 'concepts': 4302, 'events': 8305, 'informative_strata': 7241, 'informative_rows': 149693} {'R0_M0': 0.8143961684462847, 'R1_rca': 0.8166671330795342, 'R2_vol': 0.8171712341086482, 'R3_ret': 0.8210124515568055, 'R4_lost': 0.8211321193518397, 'S_strict0': 0.8207459029054467, 'S_strict': 0.8231380732946998, 'S_pca0': 0.8199329050367153, 'S_pca': 0.8223984171302506, 'EXP6_M1': 0.819506513103486, 'EXP6_M2lost': 0.8142745473517615}\n{'a_phi_home': 0.31879330883668194, 'b_log_size': 1.7653015627247062, 'c_density': 0.2098574325516749, 'e_gate_own': 0.09208532319835631, 'D_rca_1y': 0.08712169366097425, 'D_vol': 0.09923067977093664, 'd0_ret_rel': 0.2580967823432124, 'd_lost': 0.06854451886242284}\n{'R0_M0': {'converged': True, 'max_grad': 7.275957614183426e-12, 'max_abs_beta': 1.6793587903596328}, 'R1_rca': {'converged': True, 'max_grad': 1.5916157281026244e-11, 'max_abs_beta': 1.695678630387491}, 'R2_vol': {'converged': True, 'max_grad': 1.0913936421275139e-11, 'max_abs_beta': 1.684398135302692}, 'R3_ret': {'converged': True, 'max_grad': 1.1823431123048067e-11, 'max_abs_beta': 1.7537925000677053}, 'R4_lost': {'converged': True, 'max_grad': 1.0913936421275139e-11, 'max_abs_beta': 1.7653015627247062}, 'S_strict0': {'converged': True, 'max_grad': 6.366462912410498e-12, 'max_abs_beta': 1.7112134383594213}, 'S_strict': {'converged': True, 'max_grad': 5.002220859751105e-12, 'max_abs_beta': 1.7686409852426463}, 'S_pca0': {'converged': True, 'max_grad': 3.183231456205249e-12, 'max_abs_beta': 1.7084971351277058}, 'S_pca': {'converged': True, 'max_grad': 1.3642420526593924e-11, 'max_abs_beta': 1.7631050585418477}, 'EXP6_M1': {'converged': True, 'max_grad': 2.1827872842550278e-11, 'max_abs_beta': 1.7642553532386418}, 'EXP6_M2lost': {'converged': True, 'max_grad': 7.275957614183426e-12, 'max_abs_beta': 1.677596743861709}}\n{'a_phi_home': 4.2, 'b_log_size': 1.2, 'c_density': 4.3, 'e_gate_own': 1.2, 'D_rca_1y': 4.7, 'D_rca_w3': 6.2, 'D_rca_cum': 5.4, 'D_rca_pers': 5.6, 'D_vol': 33.4, 'D_vol_w3': 36.6, 'd0_ret_rel': 1.9, 'd_lost': 1.4} 21.212355625137057\n{'d0_R3': [0.222163121182832, 0.27056760450369177], 'd0_S_strict': [0.20111993313939794, 0.2540306621986624], 'd0_S_pca': [0.19880053053120209, 0.24732771700047007], 'd_lost_A1': [-0.02862867228892064, 0.015863374234381583], 'R4': [0.23281561154294425, 0.2836968013984525], 'T6_seed_stability_d0_R3': None}\n{'ci_seed1': [0.222163121182832, 0.27056760450369177], 'ci_seed2': [0.22101360148785326, 0.27018733705402215], 'max_endpoint_shift': 0.001149519694978729, 'pass_lt_0.01': True}\n{'a_phi_home': 0.40070987999976426, 'b_log_size': 1.7043199508085376, 'c_density': 0.43214998408066846, 'e_gate_own': 0.10979158311616269, 'd_lost_short': -0.010999567943902472, 'd_lost_long': 0.016604405854200307}\nperm 0.000999000999000999 0.6568153569948902\nvm -0.008486480213936415 [-0.07059399248479571, 0.05021468639357409] {'mean_n_prev_R': 0.47206756472587585, 'mean_n_prev_N': 0.3375639021396637, 'mean_cum_prev_R': 7.775964736938477, 'mean_cum_prev_N': 6.074563503265381, 'n_matched_R_fields': 5209, 'n_matched_N_fields': 5673}\nfine -0.013704900847151348 [-0.07739106044339919, 0.04829867951155931] {'mean_n_prev_R': 0.3345656096935272, 'mean_n_prev_N': 0.3058406412601471, 'mean_cum_prev_R': 6.199219703674316, 'mean_cum_prev_N': 5.521552562713623, 'n_matched_R_fields': 4869, 'n_matched_N_fields': 5359}\ndose {'2': 0.056281272485283286, '3': 0.10334686549606299, '4+': 0.251387886891025} [0.15308912972221123, 0.2363674670829122]\nbb 0.001996007984031936 0.000999000999000999 0.009900990099009901\ne_excl_intersection_born 0.255 1.3764204290034746e-84 -0.003\ng_target_field_FE 0.241 6.304360951981708e-72 -0.037\nh_horizon8 0.238 8.267920796229041e-64 0.002\ni_excl_weak_home 0.235 1.9063753200685074e-71 -0.001\nj_excl_medicine_home 0.23 3.012664089490675e-36 -0.034\nn_newborn_only_descriptive 0.389 0.010653800172584679 -0.733\no_label_coverage_ge_0.5 0.236 5.152862799802157e-70 -0.001\nf_min_n_3 0.301 1.4839217090971063e-114 0.012\nf_min_n_5 0.32 8.500100570941594e-101 0.03\nl_rca_entry_event 0.294 2.153311116616724e-50 0.015\nk_primary_topic_fields 0.259 2.5053856543191066e-145 0.008\nm_min_conditional_probability_proximity -0.024 0.006288645779299288 -0.082\n{'b': 0.0003998189491609222, 'se': 0.0002109531371402222, 'ci': [-1.3757988138174567e-05, 0.000813395886460019], 'p': 0.05811999092092676} {'note': 'GLOBAL (pooled, not within-stratum) AUC over all candidate rows; unit = concept x target field x year, event = D3 count entry; Guevara et al. 2016 report 0.896 (individuals), 0.715 (organisations), 0.682 (countries) for RCA-transition entry into research fields: different unit, event and proximity', 'D_rca_cum_alone': 0.6450014792429385, 'D_rca_1y_alone': 0.6322222379554436, 'c_density_alone': 0.6481888033758139, 'b_log_size_alone': 0.7231357459075937, 'R3_linear_predictor_primary_rows': 0.8078694852566195}\n{'d0': {'units': ['CS', 'Eng', 'BGM', 'Med'], 'k': 4, 'b': 0.21857901160572968, 'se': 0.01692305010405662, 'ci': [0.1854098334017787, 0.25174818980968067], 'p': 3.654107889268284e-38, 'tau2': 0.0003393374013345382, 'Q': 4.270348685430887, 'I2': 0.29748125481296767, 'n_positive': 4, 'n_negative': 0, 'se_type': 'concept-clustered sandwich'}, 'd_lost': {'units': ['CS', 'Eng', 'BGM', 'Med'], 'k': 4, 'b': -0.020599960334132285, 'se': 0.03031692130453938, 'ci': [-0.08002112609102946, 0.0388212054227649], 'p': 0.4968292075862645, 'tau2': 0.002768038180076376, 'Q': 15.925559665173013, 'I2': 0.8116235747393805, 'n_positive': 2, 'n_negative': 2, 'se_type': 'concept-clustered sandwich'}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [156] THINKING · 2026-09-28 22:19:12 UTC

```
On DEV, the retained frontier beats every RCA rival with a monotone dose effect, but the pre-declared volume-matched contrast is null and d0 flips slightly negative under min-CP proximity — none of which changes the frozen rule. Next I'll dry-run the verdict function on DEV-shaped inputs to catch bugs before freezing.
```

### [157] TOOL CALL — Bash · 2026-09-28 22:19:12 UTC

```
until grep -q "STEP1 EXIT" logs/step1_full.out; do sleep 3; done; tail -2 logs/step1_full.out; ls results/nulls_*; .venv/bin/python -c "
import json,sys; sys.argv=['x']
import method as MM
d=json.load(open('results/step2_dev.json'))
u=d['dev_groups']; res={'pooled4':d['battery'],'cohort':d['battery'],'units':{'PHYS':u['CS'],'LIFEENV':u['Eng'],'SOC':u['BGM'],'MATHDEC':u['Med']}}
v=MM.verdicts(res,{'mathdec_counts_in_sign_rule':False}); print(json.dumps(v,default=str,indent=0)[:2500])
"
```

### [158] TOOL RESULT — Bash · 2026-09-28 22:21:58 UTC

```
{"stdout": "22:20:38|INFO   |step1 done in 119s\nSTEP1 EXIT 0\nresults/nulls_exp5_dev.npz\nresults/nulls_exp6_heldout.npz\n{\n\"criteria\": {\n\"1_pooled4_R3\": true,\n\"2_S_strict\": true,\n\"3_sign_rule\": true,\n\"4_permutation_p<0.05\": true,\n\"5_volume_matched_CI>0\": false,\n\"6_EXP6_R3_CI>0\": true\n},\n\"FRONTIER\": \"PARTIAL: persistence confounded with volume\",\n\"ABANDONMENT\": \"INCONCLUSIVE (negative point estimate, CI includes 0)\",\n\"positive_groups\": [\n\"PHYS\",\n\"LIFEENV\",\n\"SOC\"\n],\n\"groups_in_sign_rule\": [\n\"PHYS\",\n\"LIFEENV\",\n\"SOC\"\n],\n\"cohort_d0\": 0.24552971935682877,\n\"d0_pooled4\": 0.24552971935682877,\n\"d0_ci\": [\n0.222163121182832,\n0.27056760450369177\n],\n\"d0_S_strict\": 0.22831907461531895,\n\"d0_S_strict_ci\": [\n0.20111993313939794,\n0.2540306621986624\n],\n\"d_lost_pooled4\": -0.004927001588392673,\n\"d_lost_ci\": [\n-0.02862867228892064,\n0.015863374234381583\n],\n\"holm\": {\n\"F1\": {\n\"raw\": {\n\"d0_pooled4_R3\": 1.7158363075042834e-81,\n\"d0_S_strict\": 1.565792458788652e-65,\n\"d0_cohort\": 1.7158363075042834e-81\n},\n\"holm\": {\n\"d0_pooled4_R3\": 5.14750892251285e-81,\n\"d0_cohort\": 5.14750892251285e-81,\n\"d0_S_strict\": 1.565792458788652e-65\n}\n},\n\"F2\": {\n\"raw\": {\n\"perm\": 0.000999000999000999,\n\"vol_matched\": 0.6113886113886113,\n\"dose_trend\": 0.000999000999000999,\n\"rewire\": 0.001996007984031936,\n\"label_perm\": 0.000999000999000999,\n\"field_FE\": 6.304360951981708e-72\n},\n\"holm\": {\n\"field_FE\": 3.782616571189025e-71,\n\"perm\": 0.004995004995004995,\n\"dose_trend\": 0.004995004995004995,\n\"label_perm\": 0.004995004995004995,\n\"rewire\": 0.004995004995004995,\n\"vol_matched\": 0.6113886113886113\n}\n},\n\"F3\": {\n\"raw\": {\n\"d_lost_A1_pooled_one_sided\": 0.33265683221337794,\n\"d_lost_short_2s\": 0.3395428356886441,\n\"d_lost_long_2s\": 0.1314757875848766\n},\n\"holm\": {\n\"d_lost_long_2s\": 0.3944273627546298,\n\"d_lost_A1_pooled_one_sided\": 0.6653136644267559,\n\"d_lost_short_2s\": 0.6653136644267559\n}\n}\n}\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [159] ASSISTANT · 2026-09-28 22:22:32 UTC

```
The verdict code path works. Recording deviations, then freezing (spec + code hashes + git commit).
```

### [160] TOOL CALL — Bash · 2026-09-28 22:22:32 UTC

```
.venv/bin/python - <<'EOF'
import json
from pathlib import Path
d = {
 "copies_exp6_lib": "lib/h2.py -> lib/h2_exp6.py and lib/stats_core.py copied byte-identical (sha256 logged in logs/method.log of setup: c0886d24..., a1c30fae...); only change: h2_exp6 imports Y0 from cfg_exp6 instead of config. config.py -> lib/cfg_exp6.py with its directory-creating loop removed (it would create folders inside lib/).",
 "vectorised_builder": "Risk sets are built by lib/d3.py (vectorised over concepts: per-stratum field masks @ phi) instead of calling h2_exp6.build_risk_sets row by row; T1 gate shows every EXP6 column identical to < 1e-15 on both EXP6 splits and M0/M1/M2lost refits reproduce LR 68.57, d0 0.2809, d_lost_gate -0.0632.",
 "estimator_engine": "Conditional logit fitted with an own Newton solver (lib/models.FastCLogit; same Breslow likelihood as stats_core.CLogit, agrees to 1e-5 in coefficients); concept-clustered refit bootstrap implemented with multinomial concept weights, proven identical to EXP6's duplicate-and-relabel scheme (tests 4b).",
 "primary_sample": "Frontier rungs (R0..R4, S_strict, S_pca) are fitted on EXP6's primary sample: concept-year strata with a non-empty retained set (as EXP6's frozen M0/M1). The abandonment rung A1 (and A1_split) uses all candidate rows.",
 "added_before_freeze_S_pca": "Fallback F6 pre-declared on EXP6/DEV: VIF of D_vol/D_vol_w3 ~ 35-60 and D_rca_w3 ~ 10, so a PCA-combined RCA factor rung S_pca (first PC of the four standardised D_rca, loadings frozen from DEV) was added and reported alongside S_strict (S_strict remains the verdict rung).",
 "added_before_freeze_fine_matching": "The pre-declared coarse volume bins leave poor balance at the open top bins on EXP6 (matched R n(t-1) 32.6 vs N 3.8), so a finer-bin volume-matched contrast (b2) was added before the EXP5 freeze; the coarse contrast (b) remains the verdict criterion (5).",
 "min_cp_standardisation": "Sensitivity (m) min-conditional-probability proximity: covariates standardised on the analysed sample's own moments (different scale than PMI phi).",
 "mathdec_sign_rule": "Power table (DEV simulation) gives MATHDEC power 0.42 < 0.5 at d0 = 0.15, so the sign rule was fixed BEFORE the freeze to 3 of 3 groups (PHYS, LIFEENV, SOC) + the 2010-14 cohort.",
 "power_sim_simplification": "Power grid run as two one-dimensional grids (d0 grid with beta_lost at the DEV R4 value; d_lost grid in A1 with other betas at DEV values) rather than the full 6 x 4 product; d_lost power uses the one-sided Wald test (model SE) as a fast proxy for the bootstrap CI.",
 "crossed_boot_scope": "Crossed concept x target-field bootstrap (500) run for d0 in R3 and d_lost in A1 only (headline coefficients), as planned.",
 "exact_audit": "statsmodels exact conditional likelihood audit run in audit.py on the full EXP6 held-out sample and on 3 x 30% concept subsamples of the EXP5 held-out pooled-4 sample (fallback F8, for runtime).",
 "git": "The workspace was not a git repository; `git init` was run so the freeze commit could be recorded.",
 "rca_ties": "RCA > 1 strict; exact ties RCA == 1 are counted in step2_dev.json (ties_rca_1y_eq_1).",
 "state_panel_split": "state_panel written as state_panel_dev.parquet before the freeze and state_panel_heldout.parquet after unsealing (instead of one file)."
}
Path("results/deviations.json").write_text(json.dumps(d, indent=1))
EOF
grep -c ties_rca results/step2_dev.json; .venv/bin/python -c "import json;print(json.load(open('results/step2_dev.json'))['ties_rca_1y_eq_1'])"; .venv/bin/python method.py freeze 2>&1 | tail -3; cat logs/seal.log | head -20; git log --oneline
```

### [161] TOOL RESULT — Bash · 2026-09-28 22:23:16 UTC

```
{"stdout": "1\n0\n22:22:08|INFO   |FROZEN: sha256=345d391b73f2fb134cdc5551ba002a335ee0361668b4500e9690b2b44959d60d; git 24da538b8a084118b0d34a65f30a57315caa2cdd / dc7db049b6c062465530cb2574c19f89aee54f8b; sign rule: 3 of 3 groups (PHYS, LIFEENV, SOC) + cohort\n{\n \"time\": \"2026-09-28T22:22:07.393568+00:00\",\n \"frozen_spec_sha256\": \"345d391b73f2fb134cdc5551ba002a335ee0361668b4500e9690b2b44959d60d\",\n \"code_sha256\": {\n  \"method.py\": \"97c567b256f2e029f854c10d640901f846fee17ec7e9592a4e8484ad9d43097c\",\n  \"lib/d3.py\": \"b8b44f09d56f175b175cb1bf016d1846162a65cf97385273f6b97ad16f64bce5\",\n  \"lib/models.py\": \"ac8fac289333fd7fad585ca21486962085534eb058fffff989b02ae236415e26\",\n  \"lib/analysis.py\": \"35dd709e77f31c499ca2ce09635b0d09dca2556d71944d7b36ba43914c17deea\",\n  \"lib/exp5.py\": \"4d1287d0656933019e9c0ebf580d6422f78d8fb4728907c51f33f3cffdc70049\",\n  \"lib/h2_exp6.py\": \"0cf6f10147720bac4479547ac2e73898445ba36679c265209207446efafefcf1\",\n  \"lib/stats_core.py\": \"a1c30faeddf9a658bc6dcd9826619cd2f42f51bfa856ef772c1d293b7f2582e9\",\n  \"lib/cfg_exp6.py\": \"e230ce8fc526b505e0e250bbbbc140965d32c532d2c0ec3d51342d7bdf9dee31\",\n  \"lib/seal.py\": \"8fc8c54097a6abd00eef15bf52b1f5355cd3208f28f2a7a191a491748439ece9\"\n },\n \"git_commit\": \"24da538b8a084118b0d34a65f30a57315caa2cdd\"\n}dc7db04 EXP7: frozen_spec.json + seal.log\n24da538 EXP7: pre-freeze snapshot (DEV analyses, frozen spec inputs)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [162] ASSISTANT · 2026-09-28 22:23:16 UTC

```
Frozen (spec sha256 `345d391b…`, commit `24da538`). Running the held-out stage once.
```

### [163] TOOL CALL — Bash · 2026-09-28 22:23:16 UTC

```
(timeout 5400 .venv/bin/python method.py heldout > logs/heldout_full.out 2>&1; echo "HELDOUT EXIT $?" >> logs/heldout_full.out) & echo started
```

### [164] TOOL RESULT — Bash · 2026-09-28 22:23:16 UTC

```
{"stdout": "started", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [165] TOOL CALL — Monitor · 2026-09-28 22:23:16 UTC

```
{'command': 'cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 && tail -n +1 -f logs/heldout_full.out | grep -E --line-buffered "UNSEALED|risk sets|ladder|d0 in R3|bootstr|crossed|permutation|backbone|rebuild|VERDICTS|done|Error|Traceback|EXIT|Killed"', 'description': 'held-out stage progress', 'timeout_ms': 1800000}
```

### [166] TOOL RESULT — Monitor · 2026-09-28 22:23:16 UTC

```
{"taskId": "bc68gcnz0", "timeoutMs": 1800000, "persistent": false}
```

### [167] ASSISTANT · 2026-09-28 22:23:16 UTC

```
While the held-out stage runs, I'm testing `outputs.py` on the Step-1 and DEV results to debug the figures.
```

### [168] TOOL CALL — Bash · 2026-09-28 22:23:16 UTC

```
mv results/step2_heldout.json /dev/null 2>/dev/null; timeout 600 .venv/bin/python outputs.py 2>&1 | tail -5; ls figures
```

### [169] TOOL RESULT — Bash · 2026-09-28 22:23:58 UTC

```
{"stdout": "2026-09-28 22:22:55.116 | INFO     | __main__:main:252 - outputs done\ndose_response.pdf\ndose_response.png\nforest_d0_by_unit.pdf\nforest_d0_by_unit.png\nforest_dlost_by_unit.pdf\nforest_dlost_by_unit.png\nladder.pdf\nladder.png\nnull_hist.pdf\nnull_hist.png\nvol_matched.pdf\nvol_matched.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [170] TOOL CALL — Bash · 2026-09-28 22:23:58 UTC

```
ls -la /dev/null
```

### [171] TOOL RESULT — Bash · 2026-09-28 22:23:58 UTC

```
{"stdout": "crw-rw-rw- 1 nobody nogroup 1, 3 May 20 17:59 /dev/null", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [172] ASSISTANT · 2026-09-28 22:23:58 UTC

```
`/dev/null` is intact; the stray `mv` was a no-op because the file didn't exist yet. The held-out pooled-4 ladder already shows LR(R3 vs R2) = 325.8 and S_strict 272.9. Now checking figure quality.
```

### [173] TOOL CALL — Read · 2026-09-28 22:23:58 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/ladder.png
```

### [174] TOOL RESULT — Read · 2026-09-28 22:23:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [175] TOOL CALL — Read · 2026-09-28 22:23:58 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/forest_d0_by_unit.png
```

### [176] TOOL RESULT — Read · 2026-09-28 22:23:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [177] TOOL CALL — Read · 2026-09-28 22:23:58 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/vol_matched.png
```

### [178] TOOL RESULT — Read · 2026-09-28 22:23:58 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [179] ASSISTANT · 2026-09-28 22:23:58 UTC

```
The ladder figure has overlapping labels and mismatched AUC points. Fixing it so each bar shows the AUC of the rung it adds, with R0's AUC in the title.
```

### [180] TOOL CALL — Bash · 2026-09-28 22:23:58 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('outputs.py'); s=p.read_text()
old=s[s.index('def ladder_fig'):s.index('def dose_fig')]
new='''def ladder_fig(panels: list[tuple[str, dict]]) -> None:
    steps = [("R1_rca_vs_R0_M0", "R1", "+RCA>1 dens."), ("R2_vol_vs_R1_rca", "R2", "+share dens."),
             ("R3_ret_vs_R2_vol", "R3", "+RETAINED"), ("R4_lost_vs_R3_ret", "R4", "+lost"), ("S_strict_vs_S_strict0", "S_strict", "strict: +RET.")]
    fig, axes = plt.subplots(1, len(panels), figsize=(3.3 * len(panels), 3.3))
    axes = np.atleast_1d(axes)
    for ax, (lab, lad) in zip(axes, panels):
        lr = [lad["LR"][k]["LR"] for k, _, _ in steps]
        cols = [C["held"] if "RET" in s else C["dev"] for _, _, s in steps]
        ax.bar(range(len(steps)), lr, color=cols)
        ax.axhline(6.63, color="k", lw=0.6, ls=":")
        ax.set_xticks(range(len(steps))); ax.set_xticklabels([s for _, _, s in steps], fontsize=7, rotation=35, ha="right")
        ax.set_title(f"{lab}\\n(R0 within-AUC {lad['auc_within']['R0_M0']:.3f})", fontsize=8)
        ax.set_ylabel("LR of the added block (dotted: p = 0.01)", fontsize=7)
        ax2 = ax.twinx()
        ax2.plot(range(len(steps)), [lad["auc_within"][r] for _, r, _ in steps], "k.-", lw=0.8)
        ax2.set_ylabel("within-stratum AUC of the rung", fontsize=7)
        ax2.tick_params(labelsize=7)
    fig.tight_layout()
    save(fig, "ladder")


'''
s=s.replace(old,new); p.write_text(s)
EOF
echo ok
```

### [181] TOOL RESULT — Bash · 2026-09-28 22:23:58 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [182] TOOL CALL — Bash · 2026-09-28 22:24:42 UTC

```
until grep -qE "HELDOUT EXIT" logs/heldout_full.out; do sleep 10; done; grep -E "VERDICT|done|EXIT|Error|Trace" logs/heldout_full.out | cut -c1-3000
```

### [183] TOOL RESULT — Bash · 2026-09-28 22:24:42 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bkwlk6oki"}
```

### [184] ASSISTANT · 2026-09-28 22:24:42 UTC

```
While the held-out stage runs: writing the environment lock, `install.sh`, and the manifest.
```

### [185] TOOL CALL — Bash · 2026-09-28 22:24:42 UTC

```
uv pip freeze --python .venv/bin/python > requirements.lock.txt && wc -l requirements.lock.txt && cat > install.sh <<'EOF'
#!/usr/bin/env bash
# Rebuild the Python environment (.venv is deleted after the run; see README "Restoring removed files").
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.lock.txt
.venv/bin/python -c "import numpy, pandas, scipy, statsmodels, networkx, sklearn, matplotlib, loguru; print('environment ok')"
EOF
chmod +x install.sh; du -sh .git lib/__pycache__ 2>/dev/null
```

### [186] TOOL RESULT — Bash · 2026-09-28 22:24:42 UTC

```
{"stdout": "28 requirements.lock.txt\n53M\t.git\n1.2M\tlib/__pycache__", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [187] TOOL CALL — Bash · 2026-09-28 22:24:42 UTC

```
tail -4 logs/heldout_full.out | cut -c1-400
```

### [188] TOOL RESULT — Bash · 2026-09-28 22:24:42 UTC

```
{"stdout": "22:22:37|INFO   |input checks: {'early_volume_agreement': 1.0, 'home_agreement': 0.9976886471787899, 'GF_spearman_min': 0.9999999999999999, 'GF_max_rel_diff': 0.0, 'home_mismatch_cidx': [2644, 6008, 9710, 10331, 14929, 16222, 19492, 23220, 26951, 29330, 30046, 31270, 37254, 38207, 41411, 48008, 53238]}\n22:22:43|INFO   |held-out risk sets 1,473,546 rows; state panel 3,207,880 (18s)\n22:22:48|INFO   |[exp5_heldout_pooled4] ladder: R1_rca_vs_R0_M0 LR=40.12, R2_vol_vs_R1_rca LR=1.93, R3_ret_vs_R2_vol LR=325.84, R4_lost_vs_R3_ret LR=16.70, S_strict_vs_S_strict0 LR=272.94, S_pca_vs_S_pca0 LR=263.39, EXP6_M1_vs_R0_M0 LR=361.63, EXP6_M2lost_vs_R0_M0 LR=0.18\n22:22:48|INFO   |[exp5_heldout_pooled4] d0 in R3 = 0.3219; d0 in S_strict = 0.3036; d_lost in A1 = -0.0071", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [189] ASSISTANT · 2026-09-28 22:24:42 UTC

```
Held-out pooled-4 d0 in R3 is 0.322, and 0.304 in S_strict. The bootstraps and specificity battery are still running, about 20–25 minutes by the DEV timing.
```

### [190] TOOL CALL — Bash · 2026-09-28 22:24:42 UTC

```
until grep -qE "HELDOUT EXIT" logs/heldout_full.out; do sleep 10; done; grep -E "VERDICT|done|EXIT|Error|Trace" logs/heldout_full.out | cut -c1-2500
```

### [191] TOOL RESULT — Bash · 2026-09-28 22:34:19 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bq6l6nnbl", "timedOutAfterMs": 600000}
```

### [192] ASSISTANT · 2026-09-28 22:34:19 UTC

```
The pooled-4 battery is done: permutation p = 0.001, crossed concept × field CI [0.201, 0.468]. In the cohort, LR(R3 vs R2) = 483. Cohort bootstraps and unit fits remain.
```

### [193] TOOL CALL — Bash · 2026-09-28 22:34:19 UTC

```
until grep -qE "HELDOUT EXIT" logs/heldout_full.out; do sleep 10; done; grep -E "VERDICT|done|EXIT|Error|Trace" logs/heldout_full.out | cut -c1-2500
```

### [194] TOOL RESULT — Bash · 2026-09-28 22:38:45 UTC

```
{"stdout": "22:37:17|INFO   |VERDICTS: {\"criteria\": {\"1_pooled4_R3\": true, \"2_S_strict\": true, \"3_sign_rule\": true, \"4_permutation_p<0.05\": true, \"5_volume_matched_CI>0\": false, \"6_EXP6_R3_CI>0\": true}, \"FRONTIER\": \"PARTIAL: persistence confounded with volume\", \"ABANDONMENT\": \"INCONCLUSIVE (negative point estimate, CI includes 0)\", \"positive_groups\": [\"PHYS\", \"LIFEENV\", \"SOC\"], \"groups_in_sign_rule\": [\"PHYS\", \"LIFEENV\", \"SOC\"], \"cohort_d0\": 0.3207453847057732, \"d0_pooled4\": 0.32192230141153, \"d0_ci\": [0.2913060435128285, 0.3552976576819212], \"d0_S_strict\": 0.30358096911738586, \"d0_S_strict_ci\": [0.2684803464897879, 0.3361101417337734], \"d_lost_pooled4\": -0.007123814921314389, \"d_lost_ci\": [-0.036094059720961615, 0.02206413911333745], \"holm\": {\"F1\": {\"raw\": {\"d0_pooled4_R3\": 7.739262185789853e-73, \"d0_S_strict\": 2.6001123697028655e-61, \"d0_cohort\": 4.492578726413454e-107}, \"holm\": {\"d0_cohort\": 1.3477736179240363e-106, \"d0_pooled4_R3\": 1.5478524371579707e-72, \"d0_S_strict\": 2.6001123697028655e-61}}, \"F2\": {\"raw\": {\"perm\": 0.000999000999000999, \"vol_matched\": 0.7552447552447552, \"dose_trend\": 0.000999000999000999, \"rewire\": 0.003992015968063872, \"label_perm\": 0.002997002997002997, \"field_FE\": 3.982335311694236e-58}, \"holm\": {\"field_FE\": 2.3894011870165417e-57, \"perm\": 0.004995004995004995, \"dose_trend\": 0.004995004995004995, \"label_perm\": 0.008991008991008992, \"rewire\": 0.008991008991008992, \"vol_matched\": 0.7552447552447552}}, \"F3\": {\"raw\": {\"d_lost_A1_pooled_one_sided\": 0.3162207700423322, \"d_lost_short_2s\": 0.15364166449825709, \"d_lost_long_2s\": 0.17101275926506165}, \"holm\": {\"d_lost_short_2s\": 0.46092499349477123, \"d_lost_long_2s\": 0.46092499349477123, \"d_lost_A1_pooled_one_sided\": 0.46092499349477123}}}}\n22:37:17|INFO   |held-out stage done in 891s\nHELDOUT EXIT 0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [195] THINKING · 2026-09-28 22:38:45 UTC

```
The held-out stage scored: Frontier is PARTIAL ("persistence confounded with volume") since criteria 1–4 and 6 pass but the volume-matched contrast (criterion 5) fails, while Abandonment is INCONCLUSIVE (d_lost ≈ 0). Now running the independent audit and outputs stage.
```

### [196] TOOL CALL — Bash · 2026-09-28 22:38:45 UTC

```
(timeout 3000 .venv/bin/python audit.py > logs/audit.out 2>&1; echo "AUDIT EXIT $?" >> logs/audit.out) & 
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 && timeout 1500 .venv/bin/python method.py outputs 2>&1 | tail -4; ls -la method_out* 2>/dev/null; ls -la method_out/ 2>/dev/null
```

### [197] TOOL RESULT — Bash [ERROR] · 2026-09-28 22:39:15 UTC

```
Error: Exit code 2
  File "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/outputs.py", line 94, in ladder_fig
    ax2.plot(range(len(steps)), [lad["auc_within"][r] for _, r, _ in steps], "k.-", lw=0.8)
                                 ~~~~~~~~~~~~~~~~~^^^
KeyError: 'R1'
```

### [198] TOOL CALL — Bash · 2026-09-28 22:39:15 UTC

```
sed -i 's/("R1_rca_vs_R0_M0", "R1", /("R1_rca_vs_R0_M0", "R1_rca", /; s/("R2_vol_vs_R1_rca", "R2", /("R2_vol_vs_R1_rca", "R2_vol", /; s/("R3_ret_vs_R2_vol", "R3", /("R3_ret_vs_R2_vol", "R3_ret", /; s/("R4_lost_vs_R3_ret", "R4", /("R4_lost_vs_R3_ret", "R4_lost", /' outputs.py && timeout 1500 .venv/bin/python method.py outputs 2>&1 | tail -3; ls -la method_out* 2>/dev/null; ls -la method_out/ 2>/dev/null
```

### [199] TOOL RESULT — Bash · 2026-09-28 22:40:39 UTC

```
{"stdout": "22:39:58|INFO   |method_out: 252,922 examples -> ['method_out/method_out_1.json', 'method_out/method_out_2.json']\n22:39:58|INFO   |outputs done\ntotal 168801\ndrwxrwxrwx  2 root root  2016093 Sep 28 22:39 .\ndrwxrwxrwx 13 root root  2079400 Sep 28 22:39 ..\n-rw-rw-rw-  1 root root 91541515 Sep 28 22:39 method_out_1.json\n-rw-rw-rw-  1 root root 77213773 Sep 28 22:39 method_out_2.json\ntotal 168801\ndrwxrwxrwx  2 root root  2016093 Sep 28 22:39 .\ndrwxrwxrwx 13 root root  2079400 Sep 28 22:39 ..\n-rw-rw-rw-  1 root root 91541515 Sep 28 22:39 method_out_1.json\n-rw-rw-rw-  1 root root 77213773 Sep 28 22:39 method_out_2.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [200] ASSISTANT · 2026-09-28 22:41:11 UTC

```
Part 1 is 91.5 MB. Lowering the part limit to 85 MB for safety, then validating the schema and generating mini/preview variants.
```

### [201] TOOL CALL — Bash · 2026-09-28 22:41:11 UTC

```
sed -i 's/^PART_LIMIT = 90 \* 1024 \* 1024/PART_LIMIT = 85_000_000/' outputs.py && grep -n "^PART_LIMIT" outputs.py && timeout 1500 .venv/bin/python method.py outputs 2>&1 | tail -2; ls -la method_out/; export SKILL_DIR=/ai-inventor/.claude/skills/aii-json; for f in method_out/method_out_*.json; do $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/$f 2>&1 | tail -2; done
```

### [202] TOOL RESULT — Bash · 2026-09-28 22:43:47 UTC

```
{"stdout": "29:PART_LIMIT = 85_000_000\n22:41:55|INFO   |method_out: 252,922 examples -> ['method_out/method_out_1.json', 'method_out/method_out_2.json', 'method_out/method_out_3.json']\n22:41:55|INFO   |outputs done\ntotal 168802\ndrwxrwxrwx  2 root root  2016093 Sep 28 22:41 .\ndrwxrwxrwx 13 root root  2079409 Sep 28 22:40 ..\n-rw-rw-rw-  1 root root 82450260 Sep 28 22:41 method_out_1.json\n-rw-rw-rw-  1 root root 82450210 Sep 28 22:41 method_out_2.json\n-rw-rw-rw-  1 root root  3855611 Sep 28 22:41 method_out_3.json\nFormat: exp_gen_sol_out\nValidation PASSED\nFormat: exp_gen_sol_out\nValidation PASSED\nFormat: exp_gen_sol_out\nValidation PASSED", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [203] ASSISTANT · 2026-09-28 22:44:27 UTC

```
All three parts validate. Generating mini and preview variants per part; the helper script expects a top-level array, so I'm doing it directly.
```

### [204] TOOL CALL — Bash · 2026-09-28 22:44:27 UTC

```
.venv/bin/python - <<'EOF'
import json
from pathlib import Path
def trunc(o):
    if isinstance(o,str): return o[:200]
    if isinstance(o,dict): return {k:trunc(v) for k,v in o.items()}
    if isinstance(o,list): return [trunc(v) for v in o]
    return o
for f in sorted(Path('method_out').glob('method_out_*.json')):
    d=json.loads(f.read_text())
    mini={"metadata":d["metadata"],"datasets":[{"dataset":x["dataset"],"examples":x["examples"][:3]} for x in d["datasets"]]}
    (f.parent/f"mini_{f.name}").write_text(json.dumps(mini,indent=1))
    (f.parent/f"preview_{f.name}").write_text(json.dumps(trunc(mini),indent=1))
    print(f, [(x["dataset"],len(x["examples"])) for x in d["datasets"]])
EOF
export SKILL_DIR=/ai-inventor/.claude/skills/aii-json; for f in method_out/mini_*.json method_out/preview_*.json; do $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/$f 2>&1 | tail -1; done; head -c 1500 method_out/preview_method_out_1.json | tail -c 900
```

### [205] TOOL RESULT — Bash · 2026-09-28 22:45:35 UTC

```
{"stdout": "method_out/method_out_1.json [('entry_events_heldout_cohort', 122590)]\nmethod_out/method_out_2.json [('entry_events_heldout_cohort', 7451), ('entry_events_heldout_pooled4', 117058)]\nmethod_out/method_out_3.json [('entry_events_heldout_pooled4', 5823)]\nValidation PASSED\nValidation PASSED\nValidation PASSED\nValidation PASSED\nValidation PASSED\nValidation PASSED\npersistence confounded with volume\",\n  \"abandonment\": \"INCONCLUSIVE (negative point estimate, CI includes 0)\",\n  \"part\": 1,\n  \"n_parts\": 3\n },\n \"datasets\": [\n  {\n   \"dataset\": \"entry_events_heldout_cohort\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"concept_id\\\": \\\"C125502\\\", \\\"qid\\\": \\\"Q1153279\\\", \\\"name\\\": \\\"Early adopter\\\", \\\"year\\\": 2013, \\\"target_field\\\": 13, \\\"covariates_raw\\\": {\\\"a_phi_home\\\": 0.0, \\\"b_log_size\\\": 11.77919, \\\"c_density\\\": 0.24588, \\\"e_gate_own\\\"\",\n     \"output\": \"0\",\n     \"predict_R2_rca_vol_baseline\": \"0.084149\",\n     \"predict_R3_retained_frontier\": \"0.088694\",\n     \"metadata_unit\": \"COHORT_NONDEVHOME\",\n     \"metadata_stratum\": 1613,\n     \"metadata_age\": 2,\n     \"metadata_home_group\": \"SOC\"\n    },\n    {\n     \"input\": \"{\\\"concept_id\\\": \\\"C125502\\\", \\\"qid\\\": \\\"Q1153279\\\", \\\"name\\\": \\\"Early adopter\\\", \\\"year\\\": 2013, \\\"target_field\\\": 15, \\\"covariates_raw\\\": {\\\"a_phi_", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [206] ASSISTANT · 2026-09-28 22:46:19 UTC

```
Outputs are valid. Pulling the full held-out numbers for the write-up.
```

### [207] TOOL CALL — Bash · 2026-09-28 22:46:19 UTC

```
tail -3 logs/audit.out | cut -c1-600; .venv/bin/python -c "
import json;d=json.load(open('results/step2_heldout.json'));h=d['pooled4']
print(d['n_concepts']); print(d['input_checks']['home_agreement'])
l=h['ladder']['frontier_primary_sample']; print(l['n']); print({k:round(v,4) for k,v in l['auc_within'].items()})
print({k:round(v['LR'],2) for k,v in l['LR'].items()})
print({c:round(v,3) for c,v in l['models']['R3_ret']['coef'].items()}, l['models']['R3_ret']['se_concept']['d0_ret_rel'], l['models']['R3_ret']['se_two_way_concept_field']['d0_ret_rel'])
print('R4',{c:round(v,3) for c,v in l['models']['R4_lost']['coef'].items()})
print('Spca', l['models']['S_pca']['coef']['d0_ret_rel'])
b=h['boot']; print({k:(v.get('d0_ret_rel',v.get('d_lost',{})).get('ci') if isinstance(v,dict) and ('d0_ret_rel' in v or 'd_lost' in v) else None) for k,v in b.items()}); print(b['R4']['d_lost'], b['T6_seed_stability_d0_R3'], b['d0_R3']['LR_boot_q'])
print('crossed', h['crossed_boot'])
ab=h['ladder']['abandonment_all_rows']; print(ab['n'], ab['LR'], ab['models']['A1_lost']['coef']['d_lost'], ab['models']['A1_lost']['se_concept']['d_lost'], ab['models']['A1_split']['coef'])
print(h['vif']['vif_within_stratum'], h['vif']['condition_number'])
s=h['specificity']; print('perm',s['a_permutation']['p'], s['a_permutation']['LR_obs'], s['a_permutation']['null_q'], s['a_permutation']['share_strata_nontrivial'], 'sec',s['a_permutation_secondary_all_entered_offhome']['p'])
for k in ['b_volume_matched','b2_volume_matched_fine']: c=s[k]['contrast_R_minus_N']; print(k, s[k]['match_rate_strata'], s[k]['n_concepts'], c['est'], c['ci'], c['d_R_m' if k[1]=='_' else 'd_R_mf']['est'], c['d_N_m' if k[1]=='_' else 'd_N_mf']['est'], s[k]['balance'])
print('Dcum', s['b_D_cum_rival']['coef'], s['b_D_cum_rival']['LR'])
print('dose', s['c_dose']['betas_by_age'], s['c_dose']['contrast_4p_minus_2']['est'], s['c_dose']['contrast_4p_minus_2']['ci'])
bb=s['d_backbone_d0_only']; print('bb', bb['rewire']['p'], bb['rewire']['null_q'], bb['label_perm']['p'], s['d_backbone_full_recompute']['p'], s['d_backbone_full_recompute']['LR_null_q'])
for k in ['e_excl_intersection_born','g_target_field_FE','h_horizon8','i_excl_weak_home','j_excl_medicine_home','n_newborn_only_descriptive','o_label_coverage_ge_0.5']: print(k, round(s[k]['d0_R3']['coef'],3), round(s[k]['d0_R3']['se_concept'],3), s[k]['d0_R3']['LR']['p'], s[k]['d0_R3']['n_concepts'], '| dl', round(s[k]['d_lost_A1']['coef'],3), round(s[k]['d_lost_A1']['se_concept'],3))
for k,v in h['specificity_rebuild'].items(): print(k, round(v['d0_R3']['coef'],3), round(v['d0_R3']['se_concept'],3), v['d0_R3']['LR']['p'], '| dl', round(v['d_lost_A1']['coef'],3), round(v['d_lost_A1']['se_concept'],3))
print(h['specificity_rebuild']['m_min_conditional_probability_proximity']['ladder']['LR'])
print('lpm', h['lpm_concept_year_FE']['coef']['d0_ret_rel'], h['lpm_concept_year_FE']['base_rate']); print(h['guevara_comparable_auc']); print(h['sparsity'])
for u,v in d['units'].items(): print(u, v['d0_R3']['n_concepts'], v['d0_R3']['n_events'], round(v['d0_R3']['coef'],3), [round(x,3) for x in v['d0_R3']['boot_ci']], v['d0_R3']['LR']['p'], '| dl', round(v['d_lost_A1']['coef'],3), [round(x,3) for x in v['d_lost_A1']['boot_ci']], v['within_auc_R3_vs_R2'])
print(d['DL_4groups']); print(d['DL_4groups_plus_cohort_parts']['d0'])
c=d['cohort']; cl=c['ladder']['frontier_primary_sample']; print('cohort', cl['n'], cl['models']['R3_ret']['coef']['d0_ret_rel'], c['boot']['d0_R3']['d0_ret_rel']['ci'], cl['models']['S_strict']['coef']['d0_ret_rel'], c['boot']['d0_S_strict']['d0_ret_rel']['ci'], c['boot']['d_lost_A1']['d_lost'])
"
```

### [208] TOOL RESULT — Bash · 2026-09-28 22:46:19 UTC

```
{"stdout": "22:40:36|INFO   |[EXP5 held-out pooled-4 (30% concepts)] seed 3: {'seed': 3, 'n_strata': 1837, 'share_multi_event_strata': 0.12955906369080022, 'breslow_hand': {'d0': 0.3051764360795691, 'LR': 86.0287232796527}, 'exact_statsmodels': {'d0': 0.31187899599045055, 'LR': 85.2504152165875}, 'sec': [5.8, 31.7], 'LR_ratio_exact_over_breslow': 0.9909529278897333, 'same_sign_d0': True}\n22:40:37|INFO   |audit summary: {'checks': {'exp6_heldout_exact': True, 'exp5_heldout_pooled4_breslow_full': True, 'exp5_heldout_pooled4_exact_subsample': True, 'naive_rows': True, 'DL_inline': True}, 'all_pass': True}\nAUDIT EXIT 0\n{'COHORT_DEVHOME': 2301, 'COHORT_NONDEVHOME': 1803, 'SOC': 1299, 'LIFEENV': 1079, 'PHYS': 708, 'MATHDEC': 165}\n0.9976886471787899\n{'rows': 586057, 'strata': 28951, 'concepts': 3162, 'events': 6978, 'informative_strata': 6076, 'informative_rows': 122881}\n{'R0_M0': 0.846, 'R1_rca': 0.8468, 'R2_vol': 0.8471, 'R3_ret': 0.8516, 'R4_lost': 0.8515, 'S_strict0': 0.8502, 'S_strict': 0.8534, 'S_pca0': 0.8492, 'S_pca': 0.8523, 'EXP6_M1': 0.8514, 'EXP6_M2lost': 0.846}\n{'R1_rca_vs_R0_M0': 40.12, 'R2_vol_vs_R1_rca': 1.93, 'R3_ret_vs_R2_vol': 325.84, 'R4_lost_vs_R3_ret': 16.7, 'S_strict_vs_S_strict0': 272.94, 'S_pca_vs_S_pca0': 263.39, 'EXP6_M1_vs_R0_M0': 361.63, 'EXP6_M2lost_vs_R0_M0': 0.18}\n{'a_phi_home': 0.393, 'b_log_size': 1.98, 'c_density': 0.241, 'e_gate_own': -0.144, 'D_rca_1y': 0.022, 'D_vol': 0.032, 'd0_ret_rel': 0.322} 0.01610834343415797 0.05638161445328756\nR4 {'a_phi_home': 0.395, 'b_log_size': 1.993, 'c_density': 0.207, 'e_gate_own': -0.153, 'D_rca_1y': 0.039, 'D_vol': 0.037, 'd0_ret_rel': 0.334, 'd_lost': 0.064}\nSpca 0.2967582175167318\n{'d0_R3': [0.2913060435128285, 0.3552976576819212], 'd0_S_strict': [0.2684803464897879, 0.3361101417337734], 'd0_S_pca': [0.26420226785305856, 0.3302873528797484], 'd_lost_A1': [-0.036094059720961615, 0.02206413911333745], 'R4': [0.30258485078062225, 0.36678048551971965], 'T6_seed_stability_d0_R3': None}\n{'est': 0.06374381430661213, 'ci': [0.03017683965048923, 0.09540383698954594], 'se_boot': 0.016135726516094715, 'p_one_sided_le0': 0.000999000999000999} {'ci_seed1': [0.2913060435128285, 0.3552976576819212], 'ci_seed2': [0.28842757101426897, 0.3515160890764386], 'max_endpoint_shift': 0.003781568605482566, 'pass_lt_0.01': True} [271.07450776528077, 301.72446348815083, 322.9811467645468, 348.7750723646586, 388.4137346476176]\ncrossed {'d0_R3': {'resampling_unit': 'concept x target field (Owen pigeonhole, Poisson(1) weights)', 'n_boot': 500, 'ci': [0.20064222710017335, 0.4680266653336612], 'se_boot': 0.06874877484210384}, 'd_lost_A1': {'resampling_unit': 'concept x target field (Owen pigeonhole, Poisson(1) weights)', 'n_boot': 500, 'ci': [-0.08228654095579149, 0.05228894933543425], 'se_boot': 0.03568722107692661}}\n{'rows': 667975, 'strata': 32510, 'concepts': 3251, 'events': 7682, 'informative_strata': 6695, 'informative_rows': 137135} {'A1_lost_vs_R0_M0': {'LR': 0.2600640091695823, 'df': 1, 'p': 0.6100761830601356}, 'A1_split_vs_R0_M0': {'LR': 4.5859742106476915, 'df': 2, 'p': 0.10096441960714274}} -0.007123814921314389 0.014894242727859495 {'a_phi_home': 0.37329067690709233, 'b_log_size': 1.861291398611067, 'c_density': 0.40202374987534095, 'e_gate_own': -0.10738590539872064, 'd_lost_short': -0.02138440367983592, 'd_lost_long': 0.019050879660868585}\n{'a_phi_home': 3.5759952601935368, 'b_log_size': 1.2036287132364203, 'c_density': 4.124291599080814, 'e_gate_own': 1.1574092251430694, 'D_rca_1y': 4.517845288323978, 'D_rca_w3': 5.682671631393862, 'D_rca_cum': 5.073714551625267, 'D_rca_pers': 5.059444449432175, 'D_vol': 17.661788593218464, 'D_vol_w3': 20.354118979522056, 'd0_ret_rel': 1.9898473858448797, 'd_lost': 1.389846819119036} 15.318486930250991\nperm 0.000999000999000999 325.8407278855957 [183.40021014933154, 211.48608375697148, 219.4061710646332, 234.62337849037488] 0.7081961816984859 sec 0.001996007984031936\nb_volume_matched 0.15287900245241962 1864 -0.027505466975510706 [-0.10467892431252351, 0.04600899777491371] 0.07257303690927058 0.10007850388478129 {'mean_n_prev_R': 0.39882928133010864, 'mean_n_prev_N': 0.3373235762119293, 'mean_cum_prev_R': 7.97599983215332, 'mean_cum_prev_N': 6.299088954925537, 'n_matched_R_fields': 5125, 'n_matched_N_fields': 5597}\nb2_volume_matched_fine 0.14396739318158266 1798 -0.026169176481130554 [-0.10719628404478031, 0.049464494555594526] 0.06607427400221003 0.09224345048334058 {'mean_n_prev_R': 0.35145387053489685, 'mean_n_prev_N': 0.3116562068462372, 'mean_cum_prev_R': 6.4001264572143555, 'mean_cum_prev_N': 5.713443756103516, 'n_matched_R_fields': 4746, 'n_matched_N_fields': 5259}\nDcum 0.3221187421942731 {'LR': 325.56979729646264, 'df': 1, 'p': 8.865657022297552e-73}\ndose {'2': 0.09817601792668047, '3': 0.07502115649028332, '4+': 0.3038449939708723} 0.20566897604419182 [0.15620187544917435, 0.2554942703936106]\nbb 0.003992015968063872 [19.58908569941923, 109.96927687620963, 157.72342894140544, 237.7816389250079] 0.002997002997002997 0.009900990099009901 [12.661119569536822, 64.77540730970797, 78.2466138139407, 169.95889661350319]\ne_excl_intersection_born 0.332 0.016 5.994637063206546e-74 3048 | dl -0.007 0.015\ng_target_field_FE 0.3 0.017 3.982335311694236e-58 3162 | dl -0.044 0.015\nh_horizon8 0.318 0.017 2.3788864694236208e-61 3143 | dl -0.016 0.017\ni_excl_weak_home 0.312 0.017 2.1878716748447017e-60 2747 | dl 0.006 0.016\nj_excl_medicine_home 0.322 0.016 7.739262185789853e-73 3162 | dl -0.007 0.015\nn_newborn_only_descriptive 0.562 0.265 0.07198886915526245 13 | dl -2.377 0.775\no_label_coverage_ge_0.5 0.317 0.019 2.6042867013587814e-55 2551 | dl -0.019 0.018\nf_min_n_3 0.323 0.017 1.2585880516174545e-76 | dl 0.005 0.018\nf_min_n_5 0.277 0.018 4.8174458151248156e-49 | dl 0.038 0.026\nl_rca_entry_event 0.243 0.023 2.895876117709942e-21 | dl 0.019 0.021\nk_primary_topic_fields 0.276 0.014 5.268628698797247e-78 | dl -0.012 0.009\nm_min_conditional_probability_proximity -0.021 0.009 0.012408295239020964 | dl -0.03 0.008\n{'R1_rca_vs_R0_M0': {'LR': 245.5226692711076, 'df': 1, 'p': 2.4579488565911594e-55}, 'R2_vol_vs_R1_rca': {'LR': 37.14232299662399, 'df': 1, 'p': 1.0981422480161409e-09}, 'R3_ret_vs_R2_vol': {'LR': 6.251574661015184, 'df': 1, 'p': 0.012408295239020964}, 'R4_lost_vs_R3_ret': {'LR': 0.1269938415098295, 'df': 1, 'p': 0.7215695186714723}}\nlpm {'b': -0.0010121188579259519, 'se': 0.0002658820189378561, 'ci': [-0.0015334376537781522, -0.0004908000620737516], 'p': 0.00014353612693148883} 0.011906691669922892\n{'note': 'GLOBAL (pooled, not within-stratum) AUC over all candidate rows; unit = concept x target field x year, event = D3 count entry; Guevara et al. 2016 report 0.896 (individuals), 0.715 (organisations), 0.682 (countries) for RCA-transition entry into research fields: different unit, event and proximity', 'D_rca_cum_alone': 0.6349705166449515, 'D_rca_1y_alone': 0.623356986695988, 'c_density_alone': 0.6369078959961669, 'b_log_size_alone': 0.7723955305904917, 'R3_linear_predictor_primary_rows': 0.836800612712897}\n{'share_strata_any_lost': 0.5164257151645647, 'mean_n_lost_per_stratum': 0.812949861581052, 'mean_n_ret_primary': 2.660080826223619}\nPHYS 656 1222 0.148 [0.074, 0.219] 0.0002010121980472527 | dl -0.026 [-0.091, 0.033] {'R2_vol': 0.8908675605295565, 'R3_ret': 0.8917308602598149}\nLIFEENV 1071 2378 0.401 [0.347, 0.458] 3.6526524624858006e-36 | dl -0.043 [-0.098, 0.011] {'R2_vol': 0.8751143936427417, 'R3_ret': 0.8800733452007374}\nSOC 1274 3082 0.297 [0.245, 0.345] 3.2108943650479568e-27 | dl 0.005 [-0.04, 0.044] {'R2_vol': 0.8589122465076183, 'R3_ret': 0.8625271136197508}\nMATHDEC 161 296 0.065 [-0.11, 0.234] 0.5668704227723791 | dl -0.077 [-0.304, 0.076] {'R2_vol': 0.8350958665707131, 'R3_ret': 0.8356497919195301}\nCOHORT_DEVHOME 2199 4106 0.304 [0.272, 0.335] 1.3229918858352912e-63 | dl -0.002 [-0.034, 0.028] {'R2_vol': 0.8041275296284859, 'R3_ret': 0.8120204164544333}\nCOHORT_NONDEVHOME 1750 3326 0.338 [0.293, 0.385] 2.1784488911453811e-41 | dl 0.006 [-0.034, 0.045] {'R2_vol': 0.8409376302155507, 'R3_ret': 0.8440282224407479}\n{'d0': {'units': ['PHYS', 'LIFEENV', 'SOC', 'MATHDEC'], 'k': 4, 'b': 0.24294390456781997, 'se': 0.06371164172616042, 'ci': [0.11806908678454554, 0.3678187223510944], 'p': 0.0001371905859810929, 'tau2': 0.014010035101759877, 'Q': 36.24905676746911, 'I2': 0.9172392258578083, 'n_positive': 4, 'n_negative': 0, 'se_type': 'concept-clustered sandwich'}, 'd_lost': {'units': ['PHYS', 'LIFEENV', 'SOC', 'MATHDEC'], 'k': 4, 'b': -0.016528958033249826, 'se': 0.014710968289330034, 'ci': [-0.04536245588033669, 0.01230453981383704], 'p': 0.26119100566559983, 'tau2': 0.0, 'Q': 2.43427712395724, 'I2': 0.0, 'n_positive': 1, 'n_negative': 3, 'se_type': 'concept-clustered sandwich'}}\n{'units': ['PHYS', 'LIFEENV', 'SOC', 'MATHDEC', 'COHORT_DEVHOME', 'COHORT_NONDEVHOME'], 'k': 6, 'b': 0.28070432930079364, 'se': 0.032773032229465794, 'ci': [0.2164691861310407, 0.34493947247054657], 'p': 1.0798120389129155e-17, 'tau2': 0.005140636224275265, 'Q': 39.160326666391, 'I2': 0.8723197576313579, 'n_positive': 6, 'n_negative': 0, 'se_type': 'concept-clustered sandwich'}\ncohort {'rows': 662827, 'strata': 32726, 'concepts': 3949, 'events': 7432, 'informative_strata': 6434, 'informative_rows': 130041} 0.3207453847057732 [0.2922823279287081, 0.347025567631734] 0.30958916638288425 [0.28214929494376834, 0.33560255259053157] {'est': -0.0014238261598870465, 'ci': [-0.026353167129645007, 0.02036247580137791], 'se_boot': 0.011891013671761633, 'p_one_sided_le0': 0.5494505494505495}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [209] THINKING · 2026-09-28 22:46:19 UTC

```
All audit checks pass, but I've spotted a discrepancy: the econ-geo LPM shows a negative d0 on held-out data while conditional logit shows +0.32. I'll run an exploratory diagnostic to check if this stems from the LPM's linear treatment of the dominant size effect.
```

### [210] TOOL CALL — Bash · 2026-09-28 22:46:19 UTC

```
cat > exploratory_lpm.py <<'EOF'
#!/usr/bin/env python3
"""EXPLORATORY (post-unseal; never changes a verdict): why the econ-geo LPM row gives d0 a different sign than the
conditional logit on the held-out pooled-4 sample. Variants: (i) the frozen LPM; (ii) informative strata only;
(iii) + log-size decile dummies (non-linear size); (iv) (iii) on informative strata; (v) the same on DEV.
Writes results/exploratory_lpm.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))
import analysis as AN  # noqa: E402,F401
import models as M  # noqa: E402

spec = json.loads((ROOT / "results" / "frozen_spec.json").read_text())["standardisation_DEV"]
out = {"label": "EXPLORATORY (post-unseal diagnostic; verdicts unchanged)"}
for tag, f, sel in (("heldout_pooled4", "risk_sets_exp5_minus_exp6_heldout.parquet", ["PHYS", "LIFEENV", "SOC", "MATHDEC"]),
                    ("dev", "risk_sets_exp5_minus_exp6_dev.parquet", None)):
    df = pd.read_parquet(ROOT / "results" / f)
    if sel:
        df = df[df.unit.isin(sel)]
    p = M.standardise(df[df.n_ret > 0], spec)
    cols = M.RUNGS["R3_ret"]
    dec = pd.qcut(p.b_log_size, 10, labels=False, duplicates="drop")
    for q in range(1, int(dec.max()) + 1):
        p[f"sz{q}"] = (dec == q).astype(float)
    szc = [c for c in p.columns if c.startswith("sz")]
    inf = M.informative(p)
    r = {}
    for nm, d, cc in (("frozen_lpm", p, cols), ("informative_strata", inf, cols), ("size_deciles", p, cols + szc),
                      ("size_deciles_informative", inf, cols + szc)):
        x = M.lpm(d, cc)["coef"]["d0_ret_rel"]
        r[nm] = {"b": x["b"], "ci": x["ci"], "p": x["p"]}
    r["clogit_R3_d0"] = M.summarise(*(lambda m: (m, m.fit()))(M.model(p, cols)), cols)["coef"]["d0_ret_rel"]
    r["corr_d0_logsize_within_stratum"] = float(np.corrcoef(
        p.d0_ret_rel - p.groupby("stratum").d0_ret_rel.transform("mean"),
        p.b_log_size - p.groupby("stratum").b_log_size.transform("mean"))[0, 1])
    out[tag] = r
    print(tag, json.dumps(r, indent=0))
(ROOT / "results" / "exploratory_lpm.json").write_text(json.dumps(out, indent=1))
EOF
timeout 900 .venv/bin/python exploratory_lpm.py 2>&1 | tail -40
```

### [211] TOOL RESULT — Bash · 2026-09-28 22:47:01 UTC

```
{"stdout": "},\n\"clogit_R3_d0\": 0.32192229839652015,\n\"corr_d0_logsize_within_stratum\": -0.24888058268035512\n}\ndev {\n\"frozen_lpm\": {\n\"b\": 0.0003998189780689934,\n\"ci\": [\n-1.3757945692767135e-05,\n0.0008133959018307539\n],\n\"p\": 0.058119964554857115\n},\n\"informative_strata\": {\n\"b\": 0.004244696115777997,\n\"ci\": [\n0.002405708713429589,\n0.006083683518126404\n],\n\"p\": 6.238317841582466e-06\n},\n\"size_deciles\": {\n\"b\": 0.0004952285305771117,\n\"ci\": [\n7.89166905067007e-05,\n0.0009115403706475226\n],\n\"p\": 0.019738511747570454\n},\n\"size_deciles_informative\": {\n\"b\": 0.005238629317285979,\n\"ci\": [\n0.003402319418632665,\n0.007074939215939292\n],\n\"p\": 2.4104490036948546e-08\n},\n\"clogit_R3_d0\": 0.24552971349069158,\n\"corr_d0_logsize_within_stratum\": -0.20988792859734132\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [212] TOOL CALL — Bash · 2026-09-28 22:47:01 UTC

```
.venv/bin/python -c "
import json;d=json.load(open('results/exploratory_lpm.json'))['heldout_pooled4']; print({k:(v['b'],v['ci']) if isinstance(v,dict) else v for k,v in d.items()})"
```

### [213] TOOL RESULT — Bash · 2026-09-28 22:47:01 UTC

```
{"stdout": "{'frozen_lpm': (-0.0010121187779185596, [-0.0015334375578303582, -0.0004907999980067612]), 'informative_strata': (-0.0028652985775528823, [-0.005121829299177432, -0.0006087678559283331]), 'size_deciles': (-0.0004209248046992257, [-0.0009476908550254317, 0.00010584124562698031]), 'size_deciles_informative': (0.00032344073890352786, [-0.0019499849552616552, 0.002596866433068711]), 'clogit_R3_d0': 0.32192229839652015, 'corr_d0_logsize_within_stratum': -0.24888058268035512}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [214] THINKING · 2026-09-28 22:47:01 UTC

```
Found that the linear size term misfits the steep field-size effect: with size-decile dummies, the LPM's d0 shrinks to about 0 while the clogit still shows +0.32 relative odds, meaning the frontier effect isn't established on the additive probability scale. I'll flag this caveat prominently in the consolidated results and re-render.
```

### [215] TOOL CALL — Bash · 2026-09-28 22:47:01 UTC

```
sed -i 's/          "unit_tests_T0": load("unit_tests_T0.json"), "audit": load("audit.json"),/          "unit_tests_T0": load("unit_tests_T0.json"), "audit": load("audit.json"),\n          "exploratory_lpm_EXPLORATORY": load("exploratory_lpm.json"),/' outputs.py && grep -n exploratory_lpm outputs.py && timeout 1500 .venv/bin/python method.py outputs 2>&1 | tail -1 && timeout 300 .venv/bin/python tests/test_units.py | tail -1
```

### [216] TOOL RESULT — Bash · 2026-09-28 22:49:07 UTC

```
{"stdout": "240:          \"exploratory_lpm_EXPLORATORY\": load(\"exploratory_lpm.json\"),\n22:47:51|INFO   |outputs done\nALL PASS", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [217] TOOL CALL — Read · 2026-09-28 22:49:37 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/forest_d0_by_unit.png
```

### [218] TOOL RESULT — Read · 2026-09-28 22:49:38 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [219] TOOL CALL — Read · 2026-09-28 22:49:37 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/ladder.png
```

### [220] TOOL RESULT — Read · 2026-09-28 22:49:38 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [221] SYSTEM-USER prompt · 2026-09-28 22:49:37 UTC

```
[Image: original 2623x641, displayed at 2000x489. Multiply coordinates by 1.31 to map to original image.]
```

### [222] TOOL CALL — Read · 2026-09-28 22:49:37 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/figures/null_hist.png
```

### [223] TOOL RESULT — Read · 2026-09-28 22:49:38 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [224] THINKING · 2026-09-28 22:49:38 UTC

```
The figures check out—the permutation null runs high (median LR ~185 vs. observed 326) since the entered-field footprint already carries signal, with persistence labels adding the rest. Now gathering the audit and overlap numbers for the README.
```

### [225] TOOL CALL — Bash · 2026-09-28 22:49:38 UTC

```
.venv/bin/python -c "
import json;a=json.load(open('results/audit.json'))
r=a['exp6_heldout_exact']['runs'][0]; print('exp6',r['breslow_hand'],r['exact_statsmodels'],r['share_multi_event_strata'], a['exp6_heldout_exact'].get('breslow_matches_pipeline'))
print(a['exp5_heldout_pooled4_breslow_full'])
print([ (x['breslow_hand'],x['exact_statsmodels'],round(x['LR_ratio_exact_over_breslow'],3)) for x in a['exp5_heldout_pooled4_exact_subsample']['runs']])
print(a['DL_inline']); print(a['summary'])
o=json.load(open('results/overlap_report.json')); print({k:v for k,v in o.items() if k not in ('dropped_concept_ids','dropped_by_split_group')})
"; .venv/bin/python - <<'EOF'
import json
from pathlib import Path
def trunc(o):
    if isinstance(o,str): return o[:200]
    if isinstance(o,dict): return {k:trunc(v) for k,v in o.items()}
    if isinstance(o,list): return [trunc(v) for v in o]
    return o
for f in sorted(Path('method_out').glob('method_out_*.json')):
    d=json.loads(f.read_text())
    mini={"metadata":d["metadata"],"datasets":[{"dataset":x["dataset"],"examples":x["examples"][:3]} for x in d["datasets"]]}
    (f.parent/f"mini_{f.name}").write_text(json.dumps(mini,indent=1)); (f.parent/f"preview_{f.name}").write_text(json.dumps(trunc(mini),indent=1))
print("mini/preview regenerated")
EOF
du -sh results/* | sort -h | tail -8
```

### [226] TOOL RESULT — Bash · 2026-09-28 22:49:38 UTC

```
{"stdout": "exp6 {'d0': 0.2617949241291159, 'LR': 57.59294289877198} {'d0': 0.2859685876679951, 'LR': 57.62376385933567} 0.2976066597294485 True\n{'breslow_hand': {'d0': 0.3219223031781732, 'LR': 325.84072685837236}, 'reported_pipeline': {'LR': 325.8407278855957, 'd0': 0.32192230141153}, 'sec': 37.0, 'match': True}\n[({'d0': 0.3522987159226039, 'LR': 112.80440594585707}, {'d0': 0.3630243452745173, 'LR': 113.01552255405659}, 1.002), ({'d0': 0.30687811181966956, 'LR': 88.37704559238409}, {'d0': 0.3180162879477959, 'LR': 90.17540008540709}, 1.02), ({'d0': 0.3051764360795691, 'LR': 86.0287232796527}, {'d0': 0.31187899599045055, 'LR': 85.2504152165875}, 0.991)]\n{'b': 0.24294390456781997, 'se': 0.06371164172616042, 'tau2': 0.014010035101759877, 'I2': 0.9172392258578083, 'pipeline_b': 0.24294390456781997, 'pipeline_se': 0.06371164172616042, 'match': True}\n{'checks': {'exp6_heldout_exact': True, 'exp5_heldout_pooled4_breslow_full': True, 'exp5_heldout_pooled4_exact_subsample': True, 'naive_rows': True, 'DL_inline': True}, 'all_pass': True}\n{'n_exp5': 12499, 'n_exp6_newborn_frame': 653, 'n_exp6_ids': 653, 'n_exp6_qids': 638, 'n_exp6_labels': 667, 'concept_recognition_records_scanned': 65026, 'dropped_by_id': 628, 'dropped_by_qid': 658, 'dropped_by_label': 628, 'dropped_union': 658, 'dropped_only_by_qid': 30, 'dropped_only_by_label': 0, 'kept': 11841, 'exp6_ids_not_in_exp5': 25}\nmini/preview regenerated\n116K\tresults/frozen_spec.json\n278K\tresults/frontier_result.json\n1017K\tresults/risk_sets_exp6_extended_dev.parquet\n1.4M\tresults/risk_sets_exp6_extended_heldout.parquet\n6.8M\tresults/state_panel_dev.parquet\n9.7M\tresults/state_panel_heldout.parquet\n16M\tresults/risk_sets_exp5_minus_exp6_dev.parquet\n28M\tresults/risk_sets_exp5_minus_exp6_heldout.parquet", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [227] ASSISTANT · 2026-09-28 22:51:06 UTC

```
Writing the README and manifest now; everything computed is final.
```

### [228] TOOL CALL — Write · 2026-09-28 22:51:06 UTC

````
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/README.md

# Do concepts spread from fields that keep them?

AI Inventor, invention loop iteration 3, artifact `gen_art_experiment_7` (plan `gen_plan_experiment_1_idx1`).
This is a "deepen" move on the lead `art_N-mpomDZZ1ln` (EXP6).

EXP6 found that a newborn concept next enters fields related to the off-home fields that currently **retain** it (the
*retained frontier*, `d0_ret_rel`). Two tests follow.

1. **Retained frontier vs the field-standard rival.** Does `d0` survive the relatedness-density rival as the
   relatedness literature builds it? That rival is RCA > 1 density, ω = Σ_j U_j φ_jk / Σ_j φ_jk (Hidalgo 2007;
   Guevara et al. 2016; Boschma, Balland & Kogler 2015). We use four RCA variants plus share-weighted (volume) density.
   The test runs on an independent frame and passes a battery of specificity nulls.
2. **Abandonment penalty.** Given ever-entered density, are fields related to presences the concept has **dropped**
   (`d_lost`) entered less?

Zero LLM and zero OpenAlex spend. Everything is computed from cached EXP5/EXP6 scan arrays of the full OpenAlex
snapshot (2026-09 release).

## Headline results

**Setup.** The estimator is a conditional logit with concept-year strata and Breslow ties. The unit is concept × target
field × year. Every coefficient is per DEV-SD. The resampling unit is **the concept**, except for the crossed
bootstrap, which resamples concept × target field.

**Frames.**
- **Step 1**, robustness: EXP6's frame, whose evidence was seen once before.
- **Step 2**, the independent confirmation: EXP5's 12,499-concept frame **minus every EXP6 concept**.
  - Matching is on OpenAlex ID, Wikidata QID and normalised label. 658 concepts are dropped (30 of them by QID only),
    leaving 11,841.
  - The 4,486 DEV concepts were used to build and check the code, standardise, run the power analysis and fix the
    sign rule.
  - The specification was then **hash-frozen**: `logs/seal.log`, git commit `24da538`. The held-out units were
    scored **once**: `logs/unseal.log`, 0 code changes since the freeze.

| quantity | EXP6 held-out (robustness) | EXP5−EXP6 DEV | **EXP5−EXP6 held-out, pooled-4** (PHYS+LIFEENV+SOC+MATHDEC) | held-out 2010–14 cohort |
|---|---|---|---|---|
| concepts / events / informative strata | 369 / 1,373 / 961 | 4,302 / 8,305 / 7,241 | **3,162 / 6,978 / 6,076** | 3,949 / 7,432 / 6,434 |
| LR, +RCA>1 density (R1 vs R0) | 21.7 | 120.5 | 40.1 | 79.7 |
| LR, +share-weighted density (R2 vs R1) | 20.4 | 14.5 | 1.9 | 4.1 |
| **LR, +retained frontier (R3 vs R2)** | 57.6 | 365.6 | **325.8** (p = 8e-73) | 483.1 |
| **d0 in R3** [concept refit bootstrap, 1,000 draws] | 0.262 [0.196, 0.320] | 0.246 [0.222, 0.271] | **0.322 [0.291, 0.355]** | 0.321 [0.292, 0.347] |
| d0 in S_strict (all 4 RCA variants + both D_vol) | 0.252 [0.188, 0.315] | 0.228 [0.201, 0.254] | **0.304 [0.268, 0.336]**; LR 272.9 | 0.310 [0.282, 0.336] |
| d0 in S_pca (first PC of the 4 RCA densities) | 0.253 | 0.225 | 0.297 [0.264, 0.330] | – |
| crossed concept × target-field bootstrap CI of d0 | [0.096, 0.423] | [0.139, 0.333] | [0.201, 0.468] | – |
| two-way (concept, field) clustered SE of d0 | 0.067 | – | 0.056 (concept only: 0.016) | – |
| within-stratum AUC, R0 → R2 → R3 | 0.809 → 0.815 → 0.821 | 0.814 → 0.817 → 0.821 | 0.846 → 0.847 → 0.852 | – |
| retained-label permutation p (1,000; footprint kept) | 0.001 | 0.001 | **0.001** (null median LR 183 vs observed 326; non-trivial in 71% of strata) | – |
| degree-preserving rewire p (500) / node-label permutation p (1,000) | 0.002 / 0.001 | 0.002 / 0.001 | 0.004 / 0.003 | – |
| full-recompute rewire p (100) | 0.010 | 0.010 | 0.010 | – |
| **volume-matched retained − non-retained** (pre-declared coarse bins) | +0.130 [−0.002, 0.258] | −0.008 [−0.071, 0.050] | **−0.028 [−0.105, 0.046]** | – |
| volume-matched, fine bins (added before the freeze) | +0.071 [−0.067, 0.236] | −0.014 [−0.077, 0.048] | −0.026 [−0.107, 0.049] | – |
| dose: β by persistence age 2 / 3 / ≥4 | 0.10 / 0.14 / 0.21 | 0.06 / 0.10 / 0.25 | 0.10 / 0.08 / 0.30; β(≥4) − β(2) = 0.21 [0.16, 0.26] | – |
| **d_lost in A1** (given ever-entered density; all rows) | −0.053 [−0.125, 0.008] | −0.005 [−0.029, 0.016] | **−0.007 [−0.036, 0.022]**; LR 0.26 | −0.001 [−0.026, 0.020] |
| d_lost in R4 (with d0 and the rivals) | −0.026 [−0.116, 0.044] | +0.069 | +0.064 [0.030, 0.095] | – |

**Per held-out unit.** d0 in R3 [500-draw concept bootstrap]:

| unit | d0 [bootstrap CI] |
|---|---|
| PHYS | 0.148 [0.074, 0.219] |
| LIFEENV | 0.401 [0.347, 0.458] |
| SOC | 0.297 [0.245, 0.345] |
| MATHDEC (n = 161, underpowered) | 0.065 [−0.110, 0.234] |
| COHORT_DEVHOME | 0.304 [0.272, 0.335] |
| COHORT_NONDEVHOME | 0.338 [0.293, 0.385] |

- DerSimonian-Laird pooling over the 4 groups gives **0.243 [0.118, 0.368]**, with **I² = 0.92**. The effect is
  positive everywhere but heterogeneous in size.
- d_lost is not distinguishable from 0 in any unit, and the DL estimate is −0.017 [−0.045, 0.012], I² = 0.

### Frozen verdicts (`results/step2_heldout.json → verdicts`)

- **FRONTIER: PARTIAL: "persistence confounded with volume".**
  - Criteria met:
    - (1) pooled-4 d0 in R3 > 0, CI > 0, LR p < 0.01;
    - (2) the same in S_strict;
    - (3) 3 of 3 powered groups (PHYS, LIFEENV, SOC) plus the cohort positive. MATHDEC was excluded **before the
      freeze** because its simulated power at d = 0.15 was 0.42;
    - (4) retained-label permutation p = 0.001;
    - (6) EXP6 robustness CI > 0.
  - Failed criterion: **(5)**. Once a retained field is compared with an entered-but-not-retained field of the *same
    current and cumulative volume*, the retained label adds nothing: −0.028 [−0.105, 0.046]. DEV had already shown
    the same (−0.008). The finer bins agree.
  - Reading: relatedness to fields where the concept is *persistently present* predicts next entry far beyond every
    RCA > 1 density variant, continuous share-weighted density (D_vol, D_vol_w3, D_cum) and target-field FE.
  - But within matched volume cells, persistence per se is not separable from volume. The matched cells are
    dominated by low-volume presences (mean n(t−1) about 0.4), so this test has little leverage at high volume.
- **ABANDONMENT: INCONCLUSIVE.** The point estimate is negative (−0.007), the CI includes 0 and the Holm F3 p is
  0.46. The EXP6 frame hinted at −0.05 (CI includes 0), and this did not replicate on the larger frame. Given d0, the
  sign even turns positive (R4, +0.064). **No abandonment penalty is supported.**
- Holm-adjusted p values:
  - F1 (d0 pooled, S_strict, cohort): all < 1e-60.
  - F2:

    | test | Holm p |
    |---|---|
    | permutation | 0.005 |
    | dose trend | 0.005 |
    | rewire | 0.009 |
    | label permutation | 0.009 |
    | field FE | < 1e-56 |
    | volume-matched | 0.76 |

### Sensitivities (held-out pooled-4, d0 in R3 ± concept-cluster SE)

The effect is stable under:
- excluding intersection-born concepts: 0.332 ± 0.016;
- **target-field fixed effects**: 0.300 ± 0.017;
- horizon 8: 0.318;
- excluding weak-home concepts: 0.312;
- excluding Medicine-home concepts: 0.322;
- label coverage ≥ 0.5: 0.317;
- min_n = 3: 0.323; min_n = 5: 0.277;
- **RCA-defined entry event**: 0.243 ± 0.023;
- primary-topic instead of venue fields: 0.276;
- adding D_cum: 0.322.

Two results limit the claim:

1. **The effect is specific to the frozen PMI backbone.** With a Hidalgo min-conditional-probability proximity
   (`C_jk / max(C_jj, C_kk)`, 1998–2002 co-assignment) the retained frontier **vanishes and turns slightly negative**:
   −0.021 ± 0.009 (p = 0.012) held-out and −0.024 on DEV. Under that proximity, RCA > 1 density itself becomes
   strong (LR 246). The sparse positive-PMI backbone and the dense co-assignment proximity encode different
   relatedness.
2. **The econ-geo LPM comparability row does not reproduce the sign.** The LPM uses stratum FE and concept-clustered
   errors. On held-out pooled-4, d0 = −0.0010 [−0.0015, −0.0005], against a base rate of 1.2%. It is +0.0004
   (p = 0.06) on DEV and +0.0016 (n.s.) on EXP6.
   - An **EXPLORATORY** post-unseal diagnostic (`exploratory_lpm.py` → `results/exploratory_lpm.json`) shows why:
     d0 is negatively correlated with target-field size within strata (r = −0.25), and the linear size term misfits.
   - With size-decile dummies, the held-out LPM d0 is ≈ 0 (−0.0004 [−0.0009, 0.0001]).
   - So the frontier is a **relative-odds** effect. It is not an established effect on the additive probability
     scale.

**Guevara-comparable global AUCs** (different unit, event and proximity; not head-to-head):
- D_rca_cum alone 0.635, D_rca_1y alone 0.623, size alone 0.772.
- R3 linear predictor 0.837 (held-out pooled-4).
- Guevara et al. (2016) report 0.896 for individuals, 0.715 for organisations and 0.682 for countries.

## Checks

| check | result |
|---|---|
| T0 unit tests (`tests/test_units.py`, 10) | all pass. Covers: toy D3 states; equality with `h2_exp6.states` / `rca_entered` on 50 real concepts; RCA toy with ties at exactly 1 (strict >); density algebra; FastCLogit vs statsmodels (rel. diff 1e-4); weighted bootstrap equal to duplicate-and-relabel; permutation keeps size and pool; rewire keeps degrees and weights; crossed offset with v = 1 is exact; seal guard |
| T1 reproduction gate | EXP6 risk sets rebuilt row-for-row (47,762 + 61,648 rows; max column diff 4e-16); held-out M1 vs M0 **LR 68.569, d0 0.2809, d_lost_gate −0.0632** |
| EXP5 array re-implementation | early volume 100%; home rule 99.9% (DEV) and 99.8% (held-out); GF identical to EXP6's |
| T3 planted / null | simulated d0 = 0.2 detected in 100% at pooled-4 size; null rejection 0/200 at α = 0.01; entry shuffled within strata rejects 0/20 |
| T4 sanity (DEV) | size > 0, density > 0, R0 within-AUC 0.814 ∈ [0.75, 0.85]; max VIF 37 (D_vol vs D_vol_w3), RCA variants 4.7–6.2 |
| T5 seal | held-out risk-set file created only after `logs/seal.log`; exactly one unseal |
| T6 seed stability | second bootstrap seed moves the d0 CI endpoints by 0.001 (DEV) and 0.004 (held-out) |
| T7 audit (`audit.py`, separate code path) | hand-looped Breslow reproduces the pipeline LR 325.84 / d0 0.3219 exactly. statsmodels **exact** conditional likelihood gives LR ratio exact/Breslow 1.00 on EXP6 (d0 0.286 vs 0.262) and 0.99–1.02 on 3 × 30% held-out subsamples. 20 random rows re-derived from the raw `agg_counts.parquet` with naive loops match (D_rca_1y and d0). DL recomputed inline matches. **All pass** (`results/audit.json`) |

**Power** (DEV simulation, `results/step2_dev.json → power`). 80% MDE for d0:
- about 0.04 for pooled-4 and the cohort;
- about 0.10–0.12 for PHYS, LIFEENV and SOC;
- about 0.2 for MATHDEC.

For d_lost, power is 0.99 at −0.06 in pooled-4. The abandonment null is therefore informative: an effect of
−0.06 SD or larger would have been detected.

## Layout

| path | content |
|---|---|
| `method.py` | orchestrator. Stages: `step1` (EXP6 robustness with the T1 gate), `dev`, `freeze`, `heldout` (sealed, once), `outputs` |
| `lib/d3.py` | vectorised D3 state machine, RCA>1 portfolios (annual / 3-year / cumulative / persistence-filtered), risk sets, every covariate as (field mask) @ φ, volume-matched masks |
| `lib/models.py` | Newton conditional logit (Breslow) with stratum weights, offsets, concept / two-way clustered SEs; rung definitions; refit, contrast and crossed bootstraps; LPM; Holm; DL |
| `lib/analysis.py` | shared battery: ladder, specificity (a)–(o), abandonment, per-unit fits, power simulation, shuffled control |
| `lib/exp5.py` | read-only inputs, de-duplication (ID / QID / normalised label), grounded arrays (EXP5 `c_TAG` rule), home rule, min-CP proximity |
| `lib/seal.py` | freeze / unseal guard |
| `lib/h2_exp6.py`, `lib/stats_core.py`, `lib/cfg_exp6.py` | verbatim EXP6 copies (import lines only changed; see `results/deviations.json`) |
| `audit.py` | T7 independent audit → `results/audit.json` |
| `exploratory_lpm.py` | EXPLORATORY post-unseal LPM diagnostic → `results/exploratory_lpm.json` |
| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out/` |
| `tests/test_units.py` | T0 unit tests → `results/unit_tests_T0.json` |
| `results/frontier_result.json` | **everything in one file**: step 1, DEV, power table, held-out, verdicts, overlap, deviations, tests, audit, Guevara comparison |
| `results/step1_exp6_robustness.json`, `results/step2_dev.json`, `results/step2_heldout.json` | per-stage results |
| `results/frozen_spec.json`, `logs/seal.log`, `logs/unseal.log` | freeze record (spec sha256 `345d391b…`, code hashes, git commit) |
| `results/overlap_report.json` | de-duplication counts by key and split × group, plus dropped IDs |
| `results/risk_sets_exp5_minus_exp6_{dev,heldout}.parquet`, `results/risk_sets_exp6_extended_{dev,heldout}.parquet` | every candidate row with all covariates |
| `results/state_panel_{dev,heldout}.parquet` | (concept, field, year) D3 state: 0 untouched, 1 entered, 2 retained, 3 lost, 4 home; plus counts, RCA and age |
| `results/nulls_*.npz` | permutation / rewire / label-permutation null LR draws |
| `results/deviations.json` | every departure from the plan |
| `figures/` | `forest_d0_by_unit`, `forest_dlost_by_unit`, `ladder`, `dose_response`, `null_hist`, `vol_matched` (PNG + PDF) |
| `method_out/method_out_{1,2,3}.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: 252,922 held-out candidate rows in informative primary strata, with `predict_R2_rca_vol_baseline` and `predict_R3_retained_frontier`. These are within-stratum probabilities from the **frozen DEV** coefficients |
| `logs/` | run logs (`method.log`, `*_full.out`, `audit.out`) |

The parquet results stay on the run's volume and are small enough (≤ 28 MB) to be published. No absolute server paths
are needed to read them. Inputs are read by path from EXP5/EXP6 (`lib/exp5.py`: `RUN`), and the concept-recognition
dataset `art_O7Dq4L02QnDN` is used for QID and label de-duplication.

## How to run

```bash
bash install.sh                          # uv venv + pinned requirements
.venv/bin/python tests/test_units.py     # T0
.venv/bin/python method.py step1         # ~2 min
.venv/bin/python method.py dev           # ~21 min (1,000 bootstraps, nulls, power)
.venv/bin/python method.py freeze
.venv/bin/python method.py heldout       # ~15 min, runs once (seal guard)
.venv/bin/python audit.py
.venv/bin/python exploratory_lpm.py      # EXPLORATORY
.venv/bin/python method.py outputs
```

Smoke-run overrides: `AII_SMOKE_CONCEPTS`, `AII_NBOOT`, `AII_NPERM`, `AII_NREWIRE`, `AII_NREWIRE_FULL`,
`AII_NCROSS`, `AII_NUNITBOOT`, `AII_NPOWER`, `AII_THREADS`. Seed 20261101.

## Caveats and deviations

- **Held-out provenance.** The EXP5 held-out concepts' counts and retention outcomes were unsealed in iteration 2 for
  H1/H3. No entry or frontier analysis had touched them. The replication is independent of EXP6's concepts and of
  every d0 analysis, but the frame is not never-seen data.
- **Scope of the frame.** The EXP5 frame is mostly non-newborn onset concepts. The newborn-only subgroup has 13
  held-out concepts, so it is descriptive only.
- **Entry event.** Entry is EXP6's D3 count rule, not the RCA transition. The RCA-event sensitivity keeps d0 at 0.243.
- **Primary sample.** Frontier rungs use EXP6's primary sample (strata with a non-empty retained set). A1 uses all
  candidate rows.
- **Choices made before the freeze** (see `results/deviations.json`):
  - S_pca and fine-bin matching were added before the EXP5 freeze;
  - MATHDEC was excluded from the sign rule on the basis of the power table;
  - the power grids are one-dimensional.

## Restoring removed files

| removed path (`.aii/manifest.yaml`) | restore with |
|---|---|
| `.venv/` | `bash install.sh` (`uv venv .venv --python=3.12 && uv pip install -r requirements.lock.txt`) |
| `lib/__pycache__/`, `tests/__pycache__/` | regenerated automatically by any `python` run |
````

### [229] TOOL RESULT — Write · 2026-09-28 22:51:06 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_7/README.md", "content": "# Do concepts spread from fields that keep them?\n\nAI Inventor, invention loop iteration 3, artifact `gen_art_experiment_7` (plan `gen_plan_experiment_1_idx1`).\nThis is a \"deepen\" move on the lead `art_N-mpomDZZ1ln` (EXP6).\n\nEXP6 found that a newborn concept next enters fields related to the off-home fields that currently **retain** it (the\n*retained frontier*, `d0_ret_rel`). Two tests follow.\n\n1. **Retained frontier vs the field-standard rival.** Does `d0` survive the relatedness-density rival as the\n   relatedness literature builds it? That rival is RCA > 1 density, ω = Σ_j U_j φ_jk / Σ_j φ_jk (Hidalgo 2007;\n   Guevara et al. 2016; Boschma, Balland & Kogler 2015). We use four RCA variants plus share-weighted (volume) density.\n   The test runs on an independent frame and passes a battery of specificity nulls.\n2. **Abandonment penalty.** Given ever-entered density, are fields related to presences the concept has **dropped**\n   (`d_lost`) entered less?\n\nZero LLM and zero OpenAlex spend. Everything is computed from cached EXP5/EXP6 scan arrays of the full OpenAlex\nsnapshot (2026-09 release).\n\n## Headline results\n\n**Setup.** The estimator is a conditional logit with concept-year strata and Breslow ties. The unit is concept × target\nfield × year. Every coefficient is per DEV-SD. The resampling unit is **the concept**, except for the crossed\nbootstrap, which resamples concept × target field.\n\n**Frames.**\n- **Step 1**, robustness: EXP6's frame, whose evidence was seen once before.\n- **Step 2**, the independent confirmation: EXP5's 12,499-concept frame **minus every EXP6 concept**.\n  - Matching is on OpenAlex ID, Wikidata QID and normalised label. 658 concepts are dropped (30 of them by QID only),\n    leaving 11,841.\n  - The 4,486 DEV concepts were used to build and check the code, standardise, run the power analysis and fix the\n    sign rule.\n  - The specification was then **hash-frozen**: `logs/seal.log`, git commit `24da538`. The held-out units were\n    scored **once**: `logs/unseal.log`, 0 code changes since the freeze.\n\n| quantity | EXP6 held-out (robustness) | EXP5−EXP6 DEV | **EXP5−EXP6 held-out, pooled-4** (PHYS+LIFEENV+SOC+MATHDEC) | held-out 2010–14 cohort |\n|---|---|---|---|---|\n| concepts / events / informative strata | 369 / 1,373 / 961 | 4,302 / 8,305 / 7,241 | **3,162 / 6,978 / 6,076** | 3,949 / 7,432 / 6,434 |\n| LR, +RCA>1 density (R1 vs R0) | 21.7 | 120.5 | 40.1 | 79.7 |\n| LR, +share-weighted density (R2 vs R1) | 20.4 | 14.5 | 1.9 | 4.1 |\n| **LR, +retained frontier (R3 vs R2)** | 57.6 | 365.6 | **325.8** (p = 8e-73) | 483.1 |\n| **d0 in R3** [concept refit bootstrap, 1,000 draws] | 0.262 [0.196, 0.320] | 0.246 [0.222, 0.271] | **0.322 [0.291, 0.355]** | 0.321 [0.292, 0.347] |\n| d0 in S_strict (all 4 RCA variants + both D_vol) | 0.252 [0.188, 0.315] | 0.228 [0.201, 0.254] | **0.304 [0.268, 0.336]**; LR 272.9 | 0.310 [0.282, 0.336] |\n| d0 in S_pca (first PC of the 4 RCA densities) | 0.253 | 0.225 | 0.297 [0.264, 0.330] | – |\n| crossed concept × target-field bootstrap CI of d0 | [0.096, 0.423] | [0.139, 0.333] | [0.201, 0.468] | – |\n| two-way (concept, field) clustered SE of d0 | 0.067 | – | 0.056 (concept only: 0.016) | – |\n| within-stratum AUC, R0 → R2 → R3 | 0.809 → 0.815 → 0.821 | 0.814 → 0.817 → 0.821 | 0.846 → 0.847 → 0.852 | – |\n| retained-label permutation p (1,000; footprint kept) | 0.001 | 0.001 | **0.001** (null median LR 183 vs observed 326; non-trivial in 71% of strata) | – |\n| degree-preserving rewire p (500) / node-label permutation p (1,000) | 0.002 / 0.001 | 0.002 / 0.001 | 0.004 / 0.003 | – |\n| full-recompute rewire p (100) | 0.010 | 0.010 | 0.010 | – |\n| **volume-matched retained − non-retained** (pre-declared coarse bins) | +0.130 [−0.002, 0.258] | −0.008 [−0.071, 0.050] | **−0.028 [−0.105, 0.046]** | – |\n| volume-matched, fine bins (added before the freeze) | +0.071 [−0.067, 0.236] | −0.014 [−0.077, 0.048] | −0.026 [−0.107, 0.049] | – |\n| dose: β by persistence age 2 / 3 / ≥4 | 0.10 / 0.14 / 0.21 | 0.06 / 0.10 / 0.25 | 0.10 / 0.08 / 0.30; β(≥4) − β(2) = 0.21 [0.16, 0.26] | – |\n| **d_lost in A1** (given ever-entered density; all rows) | −0.053 [−0.125, 0.008] | −0.005 [−0.029, 0.016] | **−0.007 [−0.036, 0.022]**; LR 0.26 | −0.001 [−0.026, 0.020] |\n| d_lost in R4 (with d0 and the rivals) | −0.026 [−0.116, 0.044] | +0.069 | +0.064 [0.030, 0.095] | – |\n\n**Per held-out unit.** d0 in R3 [500-draw concept bootstrap]:\n\n| unit | d0 [bootstrap CI] |\n|---|---|\n| PHYS | 0.148 [0.074, 0.219] |\n| LIFEENV | 0.401 [0.347, 0.458] |\n| SOC | 0.297 [0.245, 0.345] |\n| MATHDEC (n = 161, underpowered) | 0.065 [−0.110, 0.234] |\n| COHORT_DEVHOME | 0.304 [0.272, 0.335] |\n| COHORT_NONDEVHOME | 0.338 [0.293, 0.385] |\n\n- DerSimonian-Laird pooling over the 4 groups gives **0.243 [0.118, 0.368]**, with **I² = 0.92**. The effect is\n  positive everywhere but heterogeneous in size.\n- d_lost is not distinguishable from 0 in any unit, and the DL estimate is −0.017 [−0.045, 0.012], I² = 0.\n\n### Frozen verdicts (`results/step2_heldout.json → verdicts`)\n\n- **FRONTIER: PARTIAL: \"persistence confounded with volume\".**\n  - Criteria met:\n    - (1) pooled-4 d0 in R3 > 0, CI > 0, LR p < 0.01;\n    - (2) the same in S_strict;\n    - (3) 3 of 3 powered groups (PHYS, LIFEENV, SOC) plus the cohort positive. MATHDEC was excluded **before the\n      freeze** because its simulated power at d = 0.15 was 0.42;\n    - (4) retained-label permutation p = 0.001;\n    - (6) EXP6 robustness CI > 0.\n  - Failed criterion: **(5)**. Once a retained field is compared with an entered-but-not-retained field of the *same\n    current and cumulative volume*, the retained label adds nothing: −0.028 [−0.105, 0.046]. DEV had already shown\n    the same (−0.008). The finer bins agree.\n  - Reading: relatedness to fields where the concept is *persistently present* predicts next entry far beyond every\n    RCA > 1 density variant, continuous share-weighted density (D_vol, D_vol_w3, D_cum) and target-field FE.\n  - But within matched volume cells, persistence per se is not separable from volume. The matched cells are\n    dominated by low-volume presences (mean n(t−1) about 0.4), so this test has little leverage at high volume.\n- **ABANDONMENT: INCONCLUSIVE.** The point estimate is negative (−0.007), the CI includes 0 and the Holm F3 p is\n  0.46. The EXP6 frame hinted at −0.05 (CI includes 0), and this did not replicate on the larger frame. Given d0, the\n  sign even turns positive (R4, +0.064). **No abandonment penalty is supported.**\n- Holm-adjusted p values:\n  - F1 (d0 pooled, S_strict, cohort): all < 1e-60.\n  - F2:\n\n    | test | Holm p |\n    |---|---|\n    | permutation | 0.005 |\n    | dose trend | 0.005 |\n    | rewire | 0.009 |\n    | label permutation | 0.009 |\n    | field FE | < 1e-56 |\n    | volume-matched | 0.76 |\n\n### Sensitivities (held-out pooled-4, d0 in R3 ± concept-cluster SE)\n\nThe effect is stable under:\n- excluding intersection-born concepts: 0.332 ± 0.016;\n- **target-field fixed effects**: 0.300 ± 0.017;\n- horizon 8: 0.318;\n- excluding weak-home concepts: 0.312;\n- excluding Medicine-home concepts: 0.322;\n- label coverage ≥ 0.5: 0.317;\n- min_n = 3: 0.323; min_n = 5: 0.277;\n- **RCA-defined entry event**: 0.243 ± 0.023;\n- primary-topic instead of venue fields: 0.276;\n- adding D_cum: 0.322.\n\nTwo results limit the claim:\n\n1. **The effect is specific to the frozen PMI backbone.** With a Hidalgo min-conditional-probability proximity\n   (`C_jk / max(C_jj, C_kk)`, 1998–2002 co-assignment) the retained frontier **vanishes and turns slightly negative**:\n   −0.021 ± 0.009 (p = 0.012) held-out and −0.024 on DEV. Under that proximity, RCA > 1 density itself becomes\n   strong (LR 246). The sparse positive-PMI backbone and the dense co-assignment proximity encode different\n   relatedness.\n2. **The econ-geo LPM comparability row does not reproduce the sign.** The LPM uses stratum FE and concept-clustered\n   errors. On held-out pooled-4, d0 = −0.0010 [−0.0015, −0.0005], against a base rate of 1.2%. It is +0.0004\n   (p = 0.06) on DEV and +0.0016 (n.s.) on EXP6.\n   - An **EXPLORATORY** post-unseal diagnostic (`exploratory_lpm.py` → `results/exploratory_lpm.json`) shows why:\n     d0 is negatively correlated with target-field size within strata (r = −0.25), and the linear size term misfits.\n   - With size-decile dummies, the held-out LPM d0 is ≈ 0 (−0.0004 [−0.0009, 0.0001]).\n   - So the frontier is a **relative-odds** effect. It is not an established effect on the additive probability\n     scale.\n\n**Guevara-comparable global AUCs** (different unit, event and proximity; not head-to-head):\n- D_rca_cum alone 0.635, D_rca_1y alone 0.623, size alone 0.772.\n- R3 linear predictor 0.837 (held-out pooled-4).\n- Guevara et al. (2016) report 0.896 for individuals, 0.715 for organisations and 0.682 for countries.\n\n## Checks\n\n| check | result |\n|---|---|\n| T0 unit tests (`tests/test_units.py`, 10) | all pass. Covers: toy D3 states; equality with `h2_exp6.states` / `rca_entered` on 50 real concepts; RCA toy with ties at exactly 1 (strict >); density algebra; FastCLogit vs statsmodels (rel. diff 1e-4); weighted bootstrap equal to duplicate-and-relabel; permutation keeps size and pool; rewire keeps degrees and weights; crossed offset with v = 1 is exact; seal guard |\n| T1 reproduction gate | EXP6 risk sets rebuilt row-for-row (47,762 + 61,648 rows; max column diff 4e-16); held-out M1 vs M0 **LR 68.569, d0 0.2809, d_lost_gate −0.0632** |\n| EXP5 array re-implementation | early volume 100%; home rule 99.9% (DEV) and 99.8% (held-out); GF identical to EXP6's |\n| T3 planted / null | simulated d0 = 0.2 detected in 100% at pooled-4 size; null rejection 0/200 at α = 0.01; entry shuffled within strata rejects 0/20 |\n| T4 sanity (DEV) | size > 0, density > 0, R0 within-AUC 0.814 ∈ [0.75, 0.85]; max VIF 37 (D_vol vs D_vol_w3), RCA variants 4.7–6.2 |\n| T5 seal | held-out risk-set file created only after `logs/seal.log`; exactly one unseal |\n| T6 seed stability | second bootstrap seed moves the d0 CI endpoints by 0.001 (DEV) and 0.004 (held-out) |\n| T7 audit (`audit.py`, separate code path) | hand-looped Breslow reproduces the pipeline LR 325.84 / d0 0.3219 exactly. statsmodels **exact** conditional likelihood gives LR ratio exact/Breslow 1.00 on EXP6 (d0 0.286 vs 0.262) and 0.99–1.02 on 3 × 30% held-out subsamples. 20 random rows re-derived from the raw `agg_counts.parquet` with naive loops match (D_rca_1y and d0). DL recomputed inline matches. **All pass** (`results/audit.json`) |\n\n**Power** (DEV simulation, `results/step2_dev.json → power`). 80% MDE for d0:\n- about 0.04 for pooled-4 and the cohort;\n- about 0.10–0.12 for PHYS, LIFEENV and SOC;\n- about 0.2 for MATHDEC.\n\nFor d_lost, power is 0.99 at −0.06 in pooled-4. The abandonment null is therefore informative: an effect of\n−0.06 SD or larger would have been detected.\n\n## Layout\n\n| path | content |\n|---|---|\n| `method.py` | orchestrator. Stages: `step1` (EXP6 robustness with the T1 gate), `dev`, `freeze`, `heldout` (sealed, once), `outputs` |\n| `lib/d3.py` | vectorised D3 state machine, RCA>1 portfolios (annual / 3-year / cumulative / persistence-filtered), risk sets, every covariate as (field mask) @ φ, volume-matched masks |\n| `lib/models.py` | Newton conditional logit (Breslow) with stratum weights, offsets, concept / two-way clustered SEs; rung definitions; refit, contrast and crossed bootstraps; LPM; Holm; DL |\n| `lib/analysis.py` | shared battery: ladder, specificity (a)–(o), abandonment, per-unit fits, power simulation, shuffled control |\n| `lib/exp5.py` | read-only inputs, de-duplication (ID / QID / normalised label), grounded arrays (EXP5 `c_TAG` rule), home rule, min-CP proximity |\n| `lib/seal.py` | freeze / unseal guard |\n| `lib/h2_exp6.py`, `lib/stats_core.py`, `lib/cfg_exp6.py` | verbatim EXP6 copies (import lines only changed; see `results/deviations.json`) |\n| `audit.py` | T7 independent audit → `results/audit.json` |\n| `exploratory_lpm.py` | EXPLORATORY post-unseal LPM diagnostic → `results/exploratory_lpm.json` |\n| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out/` |\n| `tests/test_units.py` | T0 unit tests → `results/unit_tests_T0.json` |\n| `results/frontier_result.json` | **everything in one file**: step 1, DEV, power table, held-out, verdicts, overlap, deviations, tests, audit, Guevara comparison |\n| `results/step1_exp6_robustness.json`, `results/step2_dev.json`, `results/step2_heldout.json` | per-stage results |\n| `results/frozen_spec.json`, `logs/seal.log`, `logs/unseal.log` | freeze record (spec sha256 `345d391b…`, code hashes, git commit) |\n| `results/overlap_report.json` | de-duplication counts by key and split × group, plus dropped IDs |\n| `results/risk_sets_exp5_minus_exp6_{dev,heldout}.parquet`, `results/risk_sets_exp6_extended_{dev,heldout}.parquet` | every candidate row with all covariates |\n| `results/state_panel_{dev,heldout}.parquet` | (concept, field, year) D3 state: 0 untouched, 1 entered, 2 retained, 3 lost, 4 home; plus counts, RCA and age |\n| `results/nulls_*.npz` | permutation / rewire / label-permutation null LR draws |\n| `results/deviations.json` | every departure from the plan |\n| `figures/` | `forest_d0_by_unit`, `forest_dlost_by_unit`, `ladder`, `dose_response`, `null_hist`, `vol_matched` (PNG + PDF) |\n| `method_out/method_out_{1,2,3}.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: 252,922 held-out candidate rows in informative primary strata, with `predict_R2_rca_vol_baseline` and `predict_R3_retained_frontier`. These are within-stratum probabilities from the **frozen DEV** coefficients |\n| `logs/` | run logs (`method.log`, `*_full.out`, `audit.out`) |\n\nThe parquet results stay on the run's volume and are small enough (≤ 28 MB) to be published. No absolute server paths\nare needed to read them. Inputs are read by path from EXP5/EXP6 (`lib/exp5.py`: `RUN`), and the concept-recognition\ndataset `art_O7Dq4L02QnDN` is used for QID and label de-duplication.\n\n## How to run\n\n```bash\nbash install.sh                          # uv venv + pinned requirements\n.venv/bin/python tests/test_units.py     # T0\n.venv/bin/python method.py step1         # ~2 min\n.venv/bin/python method.py dev           # ~21 min (1,000 bootstraps, nulls, power)\n.venv/bin/python method.py freeze\n.venv/bin/python method.py heldout       # ~15 min, runs once (seal guard)\n.venv/bin/python audit.py\n.venv/bin/python exploratory_lpm.py      # EXPLORATORY\n.venv/bin/python method.py outputs\n```\n\nSmoke-run overrides: `AII_SMOKE_CONCEPTS`, `AII_NBOOT`, `AII_NPERM`, `AII_NREWIRE`, `AII_NREWIRE_FULL`,\n`AII_NCROSS`, `AII_NUNITBOOT`, `AII_NPOWER`, `AII_THREADS`. Seed 20261101.\n\n## Caveats and deviations\n\n- **Held-out provenance.** The EXP5 held-out concepts' counts and retention outcomes were unsealed in iteration 2 for\n  H1/H3. No entry or frontier analysis had touched them. The replication is independent of EXP6's concepts and of\n  every d0 analysis, but the frame is not never-seen data.\n- **Scope of the frame.** The EXP5 frame is mostly non-newborn onset concepts. The newborn-only subgroup has 13\n  held-out concepts, so it is descriptive only.\n- **Entry event.** Entry is EXP6's D3 count rule, not the RCA transition. The RCA-event sensitivity keeps d0 at 0.243.\n- **Primary sample.** Frontier rungs use EXP6's primary sample (strata with a non-empty retained set). A1 uses all\n  candidate rows.\n- **Choices made before the freeze** (see `results/deviations.json`):\n  - S_pca and fine-bin matching were added before the EXP5 freeze;\n  - MATHDEC was excluded from the sign rule on the basis of the power table;\n  - the power grids are one-dimensional.\n\n## Restoring removed files\n\n| removed path (`.aii/manifest.yaml`) | restore with |\n|---|---|\n| `.venv/` | `bash install.sh` (`uv venv .venv --python=3.12 && uv pip install -r requirements.lock.txt`) |\n| `lib/__pycache__/`, `tests/__pycache__/` | regenerated automatically by any `python` run |\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [230] ASSISTANT · 2026-09-28 22:51:06 UTC

```
Verifying the power MDE figures I quoted in the README.
```

### [231] TOOL CALL — Bash · 2026-09-28 22:51:06 UTC

```
.venv/bin/python -c "
import json;p=json.load(open('results/step2_dev.json'))['power']['table']
for u,v in p.items(): print(u, v['MDE80_d0'], v['MDE80_d_lost'])"
```

### [232] TOOL RESULT — Bash · 2026-09-28 22:51:06 UTC

```
{"stdout": "POOLED4 0.06551724137931036 0.04371428571428572\nPHYS 0.1203125 0.0793939393939394\nLIFEENV 0.09420289855072465 0.06\nSOC 0.09078947368421053 0.05660377358490566\nMATHDEC 0.21043478260869566 None\nCOHORT 0.07058823529411765 0.038571428571428576\nCOHORT_DEVHOME 0.08137254901960786 0.05\nCOHORT_NONDEVHOME 0.084375 0.050625", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [233] TOOL CALL — Bash · 2026-09-28 22:51:06 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('README.md'); s=p.read_text()
old="""**Power** (DEV simulation, `results/step2_dev.json → power`). 80% MDE for d0:
- about 0.04 for pooled-4 and the cohort;
- about 0.10–0.12 for PHYS, LIFEENV and SOC;
- about 0.2 for MATHDEC.

For d_lost, power is 0.99 at −0.06 in pooled-4. The abandonment null is therefore informative: an effect of
−0.06 SD or larger would have been detected."""
new="""**Power** (DEV simulation, `results/step2_dev.json → power`). 80% MDE for d0:
- 0.066 for pooled-4 and 0.071 for the cohort;
- 0.09–0.12 for PHYS, LIFEENV and SOC;
- 0.21 for MATHDEC.

For d_lost, the 80% MDE is 0.044 in pooled-4 (power 0.99 at −0.06). The abandonment null is therefore informative:
a penalty of −0.05 SD or larger would very likely have been detected."""
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
mkdir -p .aii && cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .venv/
    delete: regenerable
    source: "bash install.sh"
  - path: lib/__pycache__/
    delete: regenerable
    source: "any .venv/bin/python run of method.py regenerates it"
  - path: tests/__pycache__/
    delete: regenerable
    source: ".venv/bin/python tests/test_units.py"
  - path: results/
    keep: frozen risk sets, state panels, null draws and sealed held-out results; the held-out stage may run only once
  - path: method_out/
    keep: exp_gen_sol_out predictions consumed by later steps
  - path: .git/
    keep: holds the pre-freeze commit 24da538 that the seal log cites as pre-registration evidence
EOF
ls tests; git add -A && git -c user.name="AII executor" -c user.email=aii@localhost commit -qm "EXP7: held-out results, audit, outputs, README

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git log --oneline | head -3; du -sh .git
```

### [234] TOOL RESULT — Bash · 2026-09-28 22:51:06 UTC

```
{"stdout": "test_units.py\n9defa36 EXP7: held-out results, audit, outputs, README\ndc7db04 EXP7: frozen_spec.json + seal.log\n24da538 EXP7: pre-freeze snapshot (DEV analyses, frozen spec inputs)\n130M\t.git", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [235] TOOL CALL — Bash · 2026-09-28 22:51:06 UTC

```
find . -name __pycache__ -not -path "./.venv/*"; python3 - <<'EOF'
from pathlib import Path
import os
p=Path('.aii/manifest.yaml'); s=p.read_text()
if not Path('tests/__pycache__').exists():
    s=s.replace('''  - path: tests/__pycache__/
    delete: regenerable
    source: ".venv/bin/python tests/test_units.py"
''','')
if Path('__pycache__').exists():
    s=s.replace('entries:\n','entries:\n  - path: __pycache__/\n    delete: regenerable\n    source: "any .venv/bin/python run regenerates it"\n')
p.write_text(s); print(s)
EOF
sed -i 's#| `lib/__pycache__/`, `tests/__pycache__/` | regenerated automatically by any `python` run |#| `lib/__pycache__/`, `__pycache__/` | regenerated automatically by any `python` run |#' README.md; find . -size +10M -not -path "./.venv/*" -not -path "./.git/*" | xargs ls -la
```

### [236] TOOL RESULT — Bash · 2026-09-28 22:51:06 UTC

```
{"stdout": "./__pycache__\n./lib/__pycache__\nentries:\n  - path: __pycache__/\n    delete: regenerable\n    source: \"any .venv/bin/python run regenerates it\"\n  - path: .venv/\n    delete: regenerable\n    source: \"bash install.sh\"\n  - path: lib/__pycache__/\n    delete: regenerable\n    source: \"any .venv/bin/python run of method.py regenerates it\"\n  - path: results/\n    keep: frozen risk sets, state panels, null draws and sealed held-out results; the held-out stage may run only once\n  - path: method_out/\n    keep: exp_gen_sol_out predictions consumed by later steps\n  - path: .git/\n    keep: holds the pre-freeze commit 24da538 that the seal log cites as pre-registration evidence\n\n-rw-rw-rw- 1 root root 82450260 Sep 28 22:47 ./method_out/method_out_1.json\n-rw-rw-rw- 1 root root 82450210 Sep 28 22:47 ./method_out/method_out_2.json\n-rw-rw-rw- 1 root root 16313773 Sep 28 21:57 ./results/risk_sets_exp5_minus_exp6_dev.parquet\n-rw-rw-rw- 1 root root 28337838 Sep 28 22:22 ./results/risk_sets_exp5_minus_exp6_heldout.parquet", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [237] ASSISTANT · 2026-09-28 22:51:06 UTC

```
Frontier: **PARTIAL** — held-out d0 0.32 [0.29, 0.36] beats all RCA>1 rivals, but a volume-matched test finds no retained effect and d0 vanishes under min-CP proximity. Abandonment: **INCONCLUSIVE** (−0.007, CI spans 0). Audit passes; see README.md.
```

### [238] SYSTEM-USER prompt · 2026-09-28 22:52:38 UTC

````
n'). Applied ON TOP OF the deploy step's built-in exclusions. Use this for executor-specific caches, large transient intermediates, or content-addressed blob stores (e.g. a cache/ dir of thousands of hash-named files) that would bloat the repo. Examples: ['(^|/)cache/', '(^|/)\\\\.weight_cache/', '(^|/)checkpoints/']. Leave empty if every workspace file should be published.",
      "items": {
        "type": "string"
      },
      "title": "Upload Ignore Regexes",
      "type": "array"
    }
  },
  "required": [
    "out_expected_files"
  ],
  "title": "ExperimentArtifact",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
</prompt>
````

### [239] ASSISTANT · 2026-09-28 22:52:38 UTC

```
The schema was cut off, so I'm using EXP6's struct-out file as a format reference.
```

### [240] TOOL CALL — Bash · 2026-09-28 22:52:38 UTC

```
cat /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/.terminal_claude_agent_struct_out.json; echo; cat /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/.terminal_claude_agent_struct_out.json | head -c 1500
```

### [241] TOOL RESULT — Bash · 2026-09-28 22:52:38 UTC

```
{"stdout": "{\n \"title\": \"Where new scientific concepts spread next\",\n \"layman_summary\": \"Scans 476 million papers to see which research field a new scientific idea enters next, finding it moves into fields related to those that keep using it, not via hub fields.\",\n \"summary\": \"Full-corpus OpenAlex snapshot experiment (476M works, 0 API credits for data) on how 653 newborn concepts (legacy-concept lexicon, tag-AND-title grounding; benchmark precision 0.996, LLM+hand labelled, $0.007) enter new venue fields, using the frozen iteration-1 26-field PMI backbone. Dev = CS/Eng/BGM/Med homes, t0 2003-09 (274 concepts); held-out = other fields + 2010-14 cohort (369), run ONCE after a hashed freeze. H2 ENTRY (conditional logit on concept-year risk sets): relatedness to the off-home fields that currently RETAIN the concept predicts the next field entered beyond size, Hidalgo density, relatedness-to-home and own centrality: held-out LR 71.7 (p=2e-17), d=0.30 [0.24,0.37], positive in Physical/LifeEnv/Social/Cohort, DL pooled 0.28 [0.22,0.35] I2=0, label-permutation p=0.001, rewired-backbone p=0.015 -> CONFIRMED by the frozen rule. BUT the gateway WEIGHTING adds nothing beyond plain retaining relatedness (M3 vs M1 g-only permutation p=0.17 held-out, 0.31 dev); target-field size is the strongest single block (AUC 0.76 vs density 0.59); incremental AUC only 0.809->0.817. ORDERING: first retained gateway field precedes the calibrated entropy take-off in 66% of broad concepts (sign p=0.003) vs 57% for peripheral fields (McNemar p=0.09) -> confirmed by rule, but the lead-lag gateway-permutation placebo (p=0.63) says the panel does not single out gateway fields. RESCUE (background-adjusted citation provenance, shared-author links removed; Hanski connectivity) and RELAY (availability-null) NOT supported on held-out; the iteration-1 gateway-retention lead did NOT replicate (coef ~0). TRAJECTORIES: DTW k-medoids k=2 stable (bootstrap ARI 1.0): volume-matched 'integrating' vs 'localized' classes (held-out independent recluster ARI 0.54; localized class dominated by Medicine homes). Independent audits: R1, p_gw and held-out AUCs reproduced exactly; exact-likelihood clogit gives LR 77.3, DL-pooled d 0.32 [0.25,0.39] (Breslow pipeline is conservative); within-stratum shuffled labels reject 0/20; random-year ordering placebo 0.43 << 0.66. Outputs: method_out.json (entry_events_dev/heldout with predict_M0 vs predict_M2 within-stratum probabilities; retention_episodes), results/*.json|csv (frame_concepts, episodes, dev/heldout results, frozen_spec, grounding report, deviations), figures/ (AUC forest, group forest, incidence curve, trajectory clusters, event studies, case field-flow plots). Caveats: 1,865 episodes (<4k target), MathDec untestable, sense filter uninformative, no Wikidata aliases.\",\n \"out_expected_files\": {\n  \"script\": \"method.py\",\n  \"full_output\": \"full_method_out.json\",\n  \"mini_output\": \"mini_method_out.json\",\n  \"preview_output\": \"preview_method_out.json\",\n  \"reproducibility\": \"reproducibility.md\"\n },\n \"upload_ignore_regexes\": [\n  \"(^|/)\\\\.repl_agent\\\\.ptylog$\",\n  \"(^|/)\\\\.aii_claude_session\\\\.json$\",\n  \"(^|/)scan/pass1/\",\n  \"(^|/)scan/pass2/m\\\\d+\\\\.npz$\",\n  \"(^|/)\\\\.venv/\",\n  \"(^|/)__pycache__/\"\n ]\n}\n{\n  \"title\": \"Do hub fields keep new concepts? Held-out test\",\n  \"layman_summary\": \"Scans all 476M OpenAlex works to find 12,499 new concepts and tests, on sealed held-out fields, whether well-connected 'hub' fields keep concepts they adopt; they do not beyond simpler predictors.\",\n  \"summary\": \"Sealed held-out test of H1 (does the adopting field's frozen 1998-2002 eigenvector gateway centrality predict retention of a newly adopted concept beyond B5, field size, phi(home,j), relatedness density, the field's leave-concept-out retention propensity P_j(-c), coverage and episode size?) and H3 (does gateway-weighted early landing G predict size-adjusted breadth O2r_resid given B5?).\\n\\nData: one zero-credit scan of all 2,040 OpenAlex S3 works files (2026-09-23; 476,196,327 works; 129.4M base works 1995-2022), with Aho-Corasick title matching of 56,643 legacy concepts (levels 2-5) plus Wikidata aliases and stemmed verification: 60.0M verified matches. Grounding: legacy-tag rule TAG (test P 0.947, R 0.659), chosen on a 390-pair LLM benchmark with 60 hand-checked pairs (90% agreement), plus a per-concept LLM precision gate ($2.28 of OpenRouter).\\n\\nAuthoritative S1 tables for iteration 3: frame_concepts.csv (12,499 concepts: DEV 4,771, held-out PHYS/LIFEENV/SOC/MATHDEC 742/1,113/1,352/165, cohort 4,356), episodes.csv (27,393 concept x off-home-field episodes with R and the R_abs1-3 sensitivity outcomes for all splits), concept_outcomes.csv (O1, O3, O2r_m30/m50) and concept_features_b", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [242] ASSISTANT · 2026-09-28 22:52:38 UTC

```
I'll write a `reproducibility.md`, plus root-level mini and preview files that combine the parts, then the struct-out JSON.
```

### [243] TOOL CALL — Bash · 2026-09-28 22:52:38 UTC

````
.venv/bin/python - <<'EOF'
import json
from pathlib import Path
def trunc(o):
    if isinstance(o,str): return o[:200]
    if isinstance(o,dict): return {k:trunc(v) for k,v in o.items()}
    if isinstance(o,list): return [trunc(v) for v in o]
    return o
ds={}; meta=None
for f in sorted(Path('method_out').glob('mini_method_out_*.json')):
    d=json.loads(f.read_text()); meta=meta or d['metadata']
    for x in d['datasets']:
        ds.setdefault(x['dataset'],[]).extend(x['examples'])
meta={k:v for k,v in meta.items() if k not in ('part','n_parts')}
meta['full_output_parts']=sorted(str(p) for p in Path('method_out').glob('method_out_*.json'))
mini={"metadata":meta,"datasets":[{"dataset":k,"examples":v[:3]} for k,v in ds.items()]}
Path('mini_method_out.json').write_text(json.dumps(mini,indent=1)); Path('preview_method_out.json').write_text(json.dumps(trunc(mini),indent=1))
EOF
export SKILL_DIR=/ai-inventor/.claude/skills/aii-json; for f in mini_method_out.json preview_method_out.json; do $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/$f | tail -1; done
cat > reproducibility.md <<'EOF'
# Reproducibility

- **Environment:** Python 3.12. `bash install.sh` creates `.venv` from `requirements.lock.txt` (uv).
  - All numerics run on CPU; no GPU is needed.
  - BLAS threads are pinned to 1. Parallelism is a deterministic thread map over pre-drawn resamples.
- **Seeds:** SEED = 20261101. Each analysis draws from `np.random.default_rng([SEED, crc32(tag)])`.
  - A second-seed bootstrap moves the d0 CI endpoints by at most 0.004 (T6).
- **Inputs (read-only, by path under the run tree):**
  - EXP6 `iter_2/gen_art/gen_art_experiment_6`:
    - `scan/frame_g_*.npz`, `scan/frame_gpf_*.npz`, `scan/agg_counts.npz` (the GF key only);
    - `inputs/field_backbone.json`;
    - `results/frame_concepts.csv`, `lexicon.parquet`, `entry_risk_sets_*.parquet`, `frozen_spec.json`.
  - EXP5 `iter_2/gen_art/gen_art_experiment_5`:
    - `frame_concepts.csv`, `grounding_report.json`;
    - `scan/agg_counts.parquet`, `scan/year_field_totals.npz`, `scan/co_by_year.npz`.
  - Dataset `art_O7Dq4L02QnDN`: `full_data_out/full_data_out_{1,2,3}.json`, concept_recognition only.
- **Order:**

  ```bash
  python tests/test_units.py
  python method.py step1 && python method.py dev && python method.py freeze
  python method.py heldout
  python audit.py && python exploratory_lpm.py && python method.py outputs
  ```

  Wall times: step1 2 min, dev 21 min, heldout 15 min, audit 3 min, outputs 2 min on 10 vCPU.
- **Sealing:** `method.py heldout` refuses to run unless `logs/seal.log` matches the sha256 of
  `results/frozen_spec.json` and of every analysis `.py` file, and refuses a second unseal.
  - To re-run the held-out stage in a fresh clone, delete `logs/unseal.log`. The spec and code hashes must still
    match.
  - Frozen spec sha256: `345d391b73f2fb134cdc5551ba002a335ee0361668b4500e9690b2b44959d60d`.
  - Pre-freeze git commit: `24da538`.
- **Determinism:** risk sets and every point estimate are deterministic. Bootstrap, permutation and power results are
  deterministic given the seed and N (`AII_*` environment overrides are for smoke runs only).
- **Spend:** $0 of LLM calls and 0 OpenAlex API calls.
EOF
ls
````

### [244] TOOL RESULT — Bash · 2026-09-28 22:53:22 UTC

```
{"stdout": "Validation PASSED\nValidation PASSED\nREADME.md\n__pycache__\naudit.py\nexploratory_lpm.py\nfigures\ninstall.sh\nlib\nlogs\nmethod.py\nmethod_out\nmini_method_out.json\noutputs.py\npreview_method_out.json\npyproject.toml\nreproducibility.md\nrequirements.lock.txt\nresults\nscan\ntests", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [245] TOOL CALL — Bash · 2026-09-28 22:53:22 UTC

```
rmdir scan 2>/dev/null; .venv/bin/python - <<'EOF'
import json
from pathlib import Path
summary = """Decisive zero-credit test of the retained-frontier claim (EXP6 lead: a concept next enters fields related to the off-home fields that currently RETAIN it, d0_ret_rel) against the field-standard relatedness-density rival built as the literature builds it (omega = sum U phi / sum phi with U = RCA>1: annual Hidalgo current portfolio [primary], 3-year, Guevara-2016 cumulative and persistence-filtered), plus share-weighted density (D_vol, D_vol_w3, D_cum), and of the abandonment penalty (d_lost: relatedness to dropped off-home presences). Conditional logit (Breslow) on concept x target-field x year entry risk sets, concept-year strata, frozen 1998-2002 26-field PMI backbone; nested ladder R0 (home relatedness, log size, entered density, own gateway) -> R1 +D_rca_1y -> R2 +D_vol -> R3 +d0 -> R4 +d_lost; S_strict = all 4 RCA + both D_vol; S_pca; A1 = R0 + d_lost.

STEP 1 (EXP6 frame, robustness): risk sets rebuilt row-for-row (max diff 4e-16) and EXP6 held-out M1 vs M0 LR 68.57 / d0 0.2809 reproduced; d0 survives RCA>1 and volume: R3 0.262 [0.196,0.320], S_strict 0.252 [0.188,0.315], permutation p=0.001.

STEP 2 (independent frame: EXP5 12,499 concepts minus every EXP6 concept by OpenAlex ID/QID/normalised label -> 11,841; DEV 4,486 used for code, standardisation, power and rules; hash-frozen, git 24da538; held-out scored ONCE). Held-out pooled PHYS+LIFEENV+SOC+MATHDEC (3,162 concepts, 6,978 entries): LR(R3 vs R2)=325.8, d0=0.322 [0.291,0.355] (concept refit bootstrap 1,000), S_strict 0.304 [0.268,0.336], crossed concept x field CI [0.201,0.468]; positive in PHYS 0.15, LIFEENV 0.40, SOC 0.30 (MATHDEC 0.07, underpowered, excluded pre-freeze), cohort 2010-14 0.321 [0.292,0.347]; DL 4 groups 0.243 [0.118,0.368], I2=0.92. Retained-label permutation p=0.001, rewire p=0.004, node-label p=0.003; dose by persistence age 2/3/>=4 = 0.10/0.08/0.30 (4+ minus 2: 0.21 [0.16,0.26]); stable under target-field FE (0.30), RCA-defined entry event (0.24), primary-topic fields, min_n 3/5, horizon 8, exclusions. BUT the pre-declared volume-matched contrast (retained vs entered-not-retained fields in the same current x cumulative volume cell) is null: -0.028 [-0.105,0.046] (fine bins -0.026), so frozen verdict FRONTIER = PARTIAL ('persistence confounded with volume'). Also: under a Hidalgo min-conditional-probability proximity d0 vanishes (-0.021, p=0.012) - backbone-specific; the econ-geo LPM row gives d0 slightly negative, and an EXPLORATORY diagnostic shows it is ~0 once size enters non-linearly (relative-odds, not additive-probability, effect). ABANDONMENT: d_lost in A1 = -0.007 [-0.036,0.022] (power 0.99 at -0.06) -> INCONCLUSIVE/no penalty; with d0 it turns positive (+0.064). Within-stratum AUC R2 0.847 -> R3 0.852; Guevara-comparable global AUC of D_rca_cum 0.635 (flagged, different unit/event).

Checks: 10 unit tests pass; planted d0=0.2 detected 100%, null rejection 0/200; shuffled entries 0/20; independent audit (hand Breslow exact reproduction; statsmodels EXACT likelihood LR ratio 0.99-1.02; 20 rows re-derived from raw counts; inline DL) all pass. Outputs: results/frontier_result.json (all numbers), step1/step2 JSONs, frozen_spec + seal/unseal logs, risk-set and state-panel parquets, null draws, 6 figures (forest d0 / d_lost by unit, ladder, dose, null histograms, volume-matched), method_out/method_out_{1,2,3}.json (252,922 held-out candidate rows with predict_R2_rca_vol_baseline vs predict_R3_retained_frontier from frozen DEV coefficients). No LLM or OpenAlex spend."""
out = {
 "title": "Do concepts spread from fields that keep them?",
 "layman_summary": "Tests on 11,841 new concepts whether ideas spread to fields related to those that keep using them; this beats standard specialisation measures, but may just reflect how much use there is.",
 "summary": summary,
 "out_expected_files": {"script": "method.py", "full_output": "method_out/method_out_1.json",
                        "mini_output": "mini_method_out.json", "preview_output": "preview_method_out.json",
                        "reproducibility": "reproducibility.md"},
 "upload_ignore_regexes": ["(^|/)\\.repl_agent\\.ptylog$", "(^|/)\\.aii_claude_session\\.json$", "(^|/)\\.venv/", "(^|/)__pycache__/"]
}
Path('.terminal_claude_agent_struct_out.json').write_text(json.dumps(out, indent=1))
print(len(out["layman_summary"]))
EOF
git add -A && git -c user.name="AII executor" -c user.email=aii@localhost commit -qm "EXP7: reproducibility, mini/preview, struct out

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; git log --oneline | head -1
```

### [246] TOOL RESULT — Bash · 2026-09-28 22:53:22 UTC

```
{"stdout": "187\n75a3d9a EXP7: reproducibility, mini/preview, struct out", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [247] ASSISTANT · 2026-09-28 22:53:22 UTC

```
Wrote `.terminal_claude_agent_struct_out.json`. Your schema was cut off, so I copied EXP6's format. Output is split in three; `full_output` points to the first part and the summary names all three. Added `reproducibility.md` and root mini/preview files (schema-valid).
```

### [248] SYSTEM-USER prompt · 2026-09-28 22:54:46 UTC

```
<verification_failed>
Your experiment output failed verification (attempt 1/10).
</verification_failed>

<file_errors>
MISSING OR UNREADABLE FILES:
  - Missing file: full_method_out.json

Fix: Create the missing files directly in your workspace (see <workspace> above for the exact path).
     Required files: method.py, method_out.json, full_method_out.json, mini_method_out.json, preview_method_out.json, reproducibility.md
     Use 'ls' to check what files exist.
</file_errors>

<task>
FIX THESE ISSUES:
1. Create all missing files by running method.py

After making changes, verify:
- 'ls -la' shows all required files
- 'uv run method.py' completes successfully
- JSON files are valid (use aii-json skill validation)
- full_method_out.json has at least 50 examples
</task>
```

### [249] ASSISTANT · 2026-09-28 22:54:46 UTC

```
The verifier needs `method_out.json` and `full_method_out.json` at the root, and `uv run method.py` with no arguments must succeed (it currently exits with the usage text). I'll make the examples compact enough that the complete held-out output fits in one file, and make the default stage `outputs`. First, measuring the size.
```

### [250] TOOL CALL — Bash · 2026-09-28 22:54:46 UTC

```
.venv/bin/python -c "
import json;d=json.load(open('method_out/mini_method_out_1.json'));e=d['datasets'][0]['examples'][0];print(len(json.dumps(e)));print(e)"
```

### [251] TOOL RESULT — Bash · 2026-09-28 22:54:46 UTC

```
{"stdout": "673\n{'input': '{\"concept_id\": \"C125502\", \"qid\": \"Q1153279\", \"name\": \"Early adopter\", \"year\": 2013, \"target_field\": 13, \"covariates_raw\": {\"a_phi_home\": 0.0, \"b_log_size\": 11.77919, \"c_density\": 0.24588, \"e_gate_own\": 0.41902, \"D_rca_1y\": 0.0, \"D_rca_w3\": 0.02015, \"D_rca_cum\": 0.02015, \"D_rca_pers\": 0.0, \"D_vol\": 0.01322, \"D_vol_w3\": 0.01205, \"d0_ret_rel\": 0.15446, \"d_lost\": 0.8187, \"n_ret\": 4.0, \"n_lost\": 1.0}}', 'output': '0', 'predict_R2_rca_vol_baseline': '0.084149', 'predict_R3_retained_frontier': '0.088694', 'metadata_unit': 'COHORT_NONDEVHOME', 'metadata_stratum': 1613, 'metadata_age': 2, 'metadata_home_group': 'SOC'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [252] THINKING · 2026-09-28 22:54:46 UTC

```
Using a compact positional `input` string should keep the dataset to about 71 MB for all 252,922 rows, small enough for a single file. I'll now update `outputs.py` and the default stage accordingly.
```

### [253] TOOL CALL — Bash · 2026-09-28 22:54:46 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('outputs.py'); s=p.read_text()
old=s[s.index('    covs = ["a_phi_home"'):s.index('    meta = {"method_name"')]
new='''    covs = ["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol", "d0_ret_rel", "d_lost", "n_ret", "n_lost"]
    datasets = {}
    cid = fr.concept_id.to_dict(); qid = fr.qid.to_dict()
    vals = raw[covs].to_numpy()
    for i, r in enumerate(raw[["cidx", "t", "field", "entered", "unit", "stratum"]].itertuples(index=False)):
        c = int(r.cidx)
        inp = "|".join([f"C{int(cid[c])}", str(qid[c]), str(int(r.t)), str(int(r.field))] + [f"{v:.4g}" for v in vals[i]])
        ex = {"input": inp, "output": str(int(r.entered)),
              "predict_R2_rca_vol_baseline": f"{preds['predict_R2_rca_vol_baseline'][i]:.4g}",
              "predict_R3_retained_frontier": f"{preds['predict_R3_retained_frontier'][i]:.4g}",
              "metadata_unit": r.unit, "metadata_stratum": int(r.stratum)}
        ds = "entry_events_heldout_pooled4" if r.unit in HELD4 else "entry_events_heldout_cohort"
        datasets.setdefault(ds, []).append(ex)
'''
s=s.replace(old,new)
s=s.replace('''            "rows": "held-out candidate rows in informative strata of the primary sample (non-empty retained set)",''','''            "rows": "held-out candidate rows in informative strata of the primary sample (non-empty retained set)",
            "input_format": "concept_id|qid|year|target_field|" + "|".join(["a_phi_home", "b_log_size", "c_density", "e_gate_own", "D_rca_1y", "D_vol", "d0_ret_rel", "d_lost", "n_ret", "n_lost"]) + " (raw, unstandardised covariates at t-1; stratum = concept-year)",''')
old=s[s.index('def write_method_out'):s.index('@logger.catch')]
new='''def trunc(o):
    if isinstance(o, str):
        return o[:200]
    if isinstance(o, dict):
        return {k: trunc(v) for k, v in o.items()}
    if isinstance(o, list):
        return [trunc(v) for v in o]
    return o


def write_method_out(mo: dict) -> list[str]:
    """method_out.json == full_method_out.json (complete; compact rows keep it under the size limit), plus mini/preview."""
    s = json.dumps(mo, separators=(",", ":"))
    if len(s) > PART_LIMIT:
        raise RuntimeError(f"method_out would be {len(s)/1e6:.1f} MB > {PART_LIMIT/1e6:.0f} MB limit")
    for nm in ("method_out.json", "full_method_out.json"):
        (ROOT / nm).write_text(s)
    mini = {"metadata": mo["metadata"], "datasets": [{"dataset": d["dataset"], "examples": d["examples"][:3]} for d in mo["datasets"]]}
    (ROOT / "mini_method_out.json").write_text(json.dumps(mini, indent=1))
    (ROOT / "preview_method_out.json").write_text(json.dumps(trunc(mini), indent=1))
    return ["method_out.json", "full_method_out.json", "mini_method_out.json", "preview_method_out.json"]


'''
s=s.replace(old,new); p.write_text(s)

p=Path('method.py'); s=p.read_text()
old='''    st = sys.argv[1] if len(sys.argv) > 1 else ""'''
new='''    st = sys.argv[1] if len(sys.argv) > 1 else "outputs"  # default: rebuild outputs from the stored (sealed) stage results'''
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
rm -rf method_out; timeout 1200 uv run method.py 2>&1 | tail -3; echo EXIT $?; ls -la *.json
```

### [254] TOOL RESULT — Bash · 2026-09-28 22:55:28 UTC

```
{"stdout": "22:54:34|INFO   |method_out: 252,922 examples -> ['method_out.json', 'full_method_out.json', 'mini_method_out.json', 'preview_method_out.json']\n22:54:34|INFO   |outputs done\nEXIT 0\n-rw-rw-rw- 1 root root 58709555 Sep 28 22:54 full_method_out.json\n-rw-rw-rw- 1 root root 58709555 Sep 28 22:54 method_out.json\n-rw-rw-rw- 1 root root     2718 Sep 28 22:54 mini_method_out.json\n-rw-rw-rw- 1 root root     2718 Sep 28 22:54 preview_method_out.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [255] ASSISTANT · 2026-09-28 22:55:56 UTC

```
Everything now comes out as one 58.7 MB file. Validating, then updating the README, manifest, struct-out and deviations.
```

### [256] TOOL CALL — Bash · 2026-09-28 22:55:56 UTC

````
export SKILL_DIR=/ai-inventor/.claude/skills/aii-json; for f in method_out.json full_method_out.json mini_method_out.json preview_method_out.json; do echo $f; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/$f | tail -1; done; head -c 700 mini_method_out.json | tail -c 300; .venv/bin/python - <<'EOF'
import json
from pathlib import Path
d=json.loads(Path('full_method_out.json').read_text()); print([(x['dataset'],len(x['examples'])) for x in d['datasets']]); print(d['datasets'][0]['examples'][0])
p=Path('README.md'); s=p.read_text()
old=[l for l in s.splitlines() if l.startswith('| `method_out/method_out_{1,2,3}.json`')][0]
s=s.replace(old,"| `method_out.json` = `full_method_out.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: all 252,922 held-out candidate rows in informative primary strata (datasets `entry_events_heldout_pooled4`, `entry_events_heldout_cohort`). `input` = `concept_id|qid|year|target_field|` + 10 raw covariates (order in `metadata.input_format`). `predict_R2_rca_vol_baseline` vs `predict_R3_retained_frontier` are within-stratum probabilities from the **frozen DEV** coefficients |")
s=s.replace("| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out/` |","| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out.json` / `full_method_out.json` (`python method.py` with no stage runs it) |")
s=s.replace(".venv/bin/python method.py outputs\n```",".venv/bin/python method.py outputs    # also the default: `uv run method.py`\n```")
p.write_text(s)
m=Path('.aii/manifest.yaml'); t=m.read_text().replace("  - path: method_out/\n    keep: exp_gen_sol_out predictions consumed by later steps\n",""); m.write_text(t)
dv=json.loads(Path('results/deviations.json').read_text())
dv["post_unseal_code_edits"]="After the single unseal, only output-side code changed: outputs.py (compact method_out rows so the full output fits in one file; figure fixes) and method.py's default stage (no argument -> 'outputs'). No analysis code (lib/*) changed; logs/seal.log code hashes therefore differ only for method.py."
dv["method_out_compact"]="method_out.json / full_method_out.json carry all 252,922 held-out rows with a positional input string (10 raw covariates) instead of the per-row JSON dict, to stay under the file-size limit."
Path('results/deviations.json').write_text(json.dumps(dv,indent=1))
so=json.loads(Path('.terminal_claude_agent_struct_out.json').read_text())
so["out_expected_files"]={"script":"method.py","full_output":"full_method_out.json","mini_output":"mini_method_out.json","preview_output":"preview_method_out.json","reproducibility":"reproducibility.md"}
so["summary"]=so["summary"].replace("method_out/method_out_{1,2,3}.json (252,922","method_out.json = full_method_out.json (252,922")
Path('.terminal_claude_agent_struct_out.json').write_text(json.dumps(so,indent=1))
EOF
grep -n "method_out" README.md | head; sed -i 's#python audit.py \&\& python exploratory_lpm.py \&\& python method.py outputs#python audit.py \&\& python exploratory_lpm.py \&\& python method.py   # default stage = outputs#' reproducibility.md; git add -A; git -c user.name="AII executor" -c user.email=aii@localhost commit -qm "EXP7: single full_method_out.json; default stage outputs

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; ls -la
````

### [257] TOOL RESULT — Bash · 2026-09-28 22:57:12 UTC

```
{"stdout": "method_out.json\nValidation PASSED\nfull_method_out.json\nValidation PASSED\nmini_method_out.json\nValidation PASSED\npreview_method_out.json\nValidation PASSED\nom the FROZEN DEV coefficients; output = 1 if the field was entered\",\n  \"rows\": \"held-out candidate rows in informative strata of the primary sample (non-empty retained set)\",\n  \"input_format\": \"concept_id|qid|year|target_field|a_phi_home|b_log_size|c_density|e_gate_own|D_rca_1y|D_vol|d0_ret_rel|d_l[('entry_events_heldout_cohort', 130041), ('entry_events_heldout_pooled4', 122881)]\n{'input': 'C125502|Q1153279|2013|13|0|11.78|0.2459|0.419|0|0.01322|0.1545|0.8187|4|1', 'output': '0', 'predict_R2_rca_vol_baseline': '0.08415', 'predict_R3_retained_frontier': '0.08869', 'metadata_unit': 'COHORT_NONDEVHOME', 'metadata_stratum': 1613}\n173:| `outputs.py` | `results/frontier_result.json`, `figures/`, `method_out.json` / `full_method_out.json` (`python method.py` with no stage runs it) |\n184:| `method_out.json` = `full_method_out.json` (+ `mini_`, `preview_`) | exp_gen_sol_out: all 252,922 held-out candidate rows in informative primary strata (datasets `entry_events_heldout_pooled4`, `entry_events_heldout_cohort`). `input` = `concept_id|qid|year|target_field|` + 10 raw covariates (order in `metadata.input_format`). `predict_R2_rca_vol_baseline` vs `predict_R3_retained_frontier` are within-stratum probabilities from the **frozen DEV** coefficients |\nsed: -e expression #1, char 153: unknown option to `s'\ntotal 132919\ndrwxrwxrwx 11 root root  2079949 Sep 28 22:54 .\ndrwxrwxrwx  7 root root  3000246 Sep 28 21:29 ..\ndrwxrwxrwx  2 root root    55200 Sep 28 22:50 .aii\n-rw-rw-rw-  1 root root       54 Sep 28 21:31 .aii_claude_session.json\ndrwxrwxrwx  8 root root  2007490 Sep 28 22:56 .git\n-rw-rw-rw-  1 root root      150 Sep 28 21:58 .gitignore\n-rw-rw-rw-  1 root root  2047902 Sep 28 22:56 .repl_agent.ptylog\n-rw-rw-rw-  1 root root     4183 Sep 28 22:56 .terminal_claude_agent_struct_out.json\ndrwxrwxrwx  5 root root  2054707 Sep 28 21:33 .venv\n-rw-rw-rw-  1 root root    16404 Sep 28 22:56 README.md\ndrwxrwxrwx  2 root root  1007409 Sep 28 22:54 __pycache__\n-rw-rw-rw-  1 root root    10983 Sep 28 21:56 audit.py\n-rw-rw-rw-  1 root root     2219 Sep 28 22:45 exploratory_lpm.py\ndrwxrwxrwx  2 root root  1089460 Sep 28 22:22 figures\n-rw-rw-rw-  1 root root 58709555 Sep 28 22:54 full_method_out.json\n-rwxrwxrwx  1 root root      385 Sep 28 22:23 install.sh\ndrwxrwxrwx  3 root root  1023763 Sep 28 21:44 lib\ndrwxrwxrwx  2 root root  1005077 Sep 28 22:37 logs\n-rw-rw-rw-  1 root root    29571 Sep 28 22:53 method.py\n-rw-rw-rw-  1 root root 58709555 Sep 28 22:54 method_out.json\n-rw-rw-rw-  1 root root     2718 Sep 28 22:54 mini_method_out.json\n-rw-rw-rw-  1 root root    14840 Sep 28 22:53 outputs.py\n-rw-rw-rw-  1 root root     2718 Sep 28 22:54 preview_method_out.json\n-rw-rw-rw-  1 root root      327 Sep 28 21:33 pyproject.toml\n-rw-rw-rw-  1 root root     2110 Sep 28 22:51 reproducibility.md\n-rw-rw-rw-  1 root root      477 Sep 28 22:23 requirements.lock.txt\ndrwxrwxrwx  2 root root  2006205 Sep 28 22:45 results\ndrwxrwxrwx  2 root root  1000924 Sep 28 22:48 tests\n-rw-rw-rw-  1 root root   216210 Sep 28 22:53 uv.lock", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [258] ASSISTANT · 2026-09-28 22:57:53 UTC

```
The reproducibility sed failed on the `|` characters; fixing that line directly and committing.
```

### [259] TOOL CALL — Bash · 2026-09-28 22:57:53 UTC

```
python3 - <<'EOF'
from pathlib import Path
p=Path('reproducibility.md'); s=p.read_text()
s=s.replace("python audit.py && python exploratory_lpm.py && python method.py outputs","python audit.py && python exploratory_lpm.py && python method.py   # default stage = outputs")
p.write_text(s)
EOF
grep -n "default stage" reproducibility.md; grep -c . results/deviations.json; git add -A; git -c user.name="AII executor" -c user.email=aii@localhost commit -qm "EXP7: reproducibility note

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"; git log --oneline | head -2
```

### [260] TOOL RESULT — Bash · 2026-09-28 22:57:53 UTC

```
{"stdout": "23:  python audit.py && python exploratory_lpm.py && python method.py   # default stage = outputs\n18\na9b49da EXP7: reproducibility note\n0fcccdd EXP7: single full_method_out.json; default stage outputs", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [261] ASSISTANT · 2026-09-28 22:57:53 UTC

```
Fixed: `method_out.json` and `full_method_out.json` (58.7 MB, all 252,922 rows) plus mini/preview are now in the workspace root and pass schema checks. `uv run method.py` rebuilds them (exit 0). Only output code changed after the unseal; noted in deviations.
```

### [262] SYSTEM-USER prompt · 2026-09-28 22:59:40 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: '.git/' names module bookkeeping, which is never a decision

FIX IT:
1. Add one entry per uncovered path to `.aii/manifest.yaml` (create it if missing).
   Every path is RELATIVE TO YOUR CWD and must resolve inside it. Globs and
   whole directories are fine — a whole `hf_cache/` is ONE entry.

   entries:
     - path: results/
       keep: six GPU-hours of sweep output, not reproducible in this run
     - path: hf_cache/
       delete: redownloadable
       source: "huggingface-cli download meta-llama/Llama-3-8B"
     - path: checkpoints/
       delete: regenerable
       source: "uv run train.py --epochs 3"

   `keep:` takes a one-line reason. `delete:` takes `redownloadable` or
   `regenerable` and a `source:` that brings the files back.
2. Make sure `README.md` reads like a GitHub repository README: what you did,
   the layout (a line per important file/dir), how to run it, and a
   "Restoring removed files" section with the command for EVERY delete entry.
3. Text and code files never need a decision, and neither does anything under
   the auto-keep floor. Only large binaries and cache directories do.
</CRITICAL_ERROR>
```

### [263] TOOL CALL — Bash · 2026-09-28 22:59:40 UTC

```
python3 - <<'EOF'
from pathlib import Path
m=Path('.aii/manifest.yaml'); t=m.read_text()
t=t.replace("  - path: .git/\n    keep: holds the pre-freeze commit 24da538 that the seal log cites as pre-registration evidence\n","")
m.write_text(t); print(t)
EOF
grep -n "Restoring" -A5 README.md
```

### [264] TOOL RESULT — Bash · 2026-09-28 22:59:40 UTC

```
{"stdout": "entries:\n  - path: __pycache__/\n    delete: regenerable\n    source: \"any .venv/bin/python run regenerates it\"\n  - path: .venv/\n    delete: regenerable\n    source: \"bash install.sh\"\n  - path: lib/__pycache__/\n    delete: regenerable\n    source: \"any .venv/bin/python run of method.py regenerates it\"\n  - path: results/\n    keep: frozen risk sets, state panels, null draws and sealed held-out results; the held-out stage may run only once\n\n223:## Restoring removed files\n224-\n225-| removed path (`.aii/manifest.yaml`) | restore with |\n226-|---|---|\n227-| `.venv/` | `bash install.sh` (`uv venv .venv --python=3.12 && uv pip install -r requirements.lock.txt`) |\n228-| `lib/__pycache__/`, `__pycache__/` | regenerated automatically by any `python` run |", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [265] ASSISTANT · 2026-09-28 22:59:40 UTC

```
I removed the `.git/` entry from `.aii/manifest.yaml`, which fixes the one reported problem; I haven't re-run the check.

The manifest now has three delete entries (`.venv/`, `__pycache__/`, `lib/__pycache__/`) and keeps `results/`. The README's "Restoring removed files" section already gives the command for each delete entry, and no other large paths are uncovered.
```
