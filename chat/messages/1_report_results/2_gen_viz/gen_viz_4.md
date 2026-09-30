# gen_viz_4 — report_results

> Phase: `gen_paper_repo` · `gen_viz`
> Run: `gen_paper_repo_64e492a00621` — Early co-occurrence network openness predicts cross-disciplinary concept breadth: evidence from 12,499 scientific concepts
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_viz_4` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 20:03:09 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 20:03:17 UTC

```
<research_methodology>
Create figures that belong in a top-venue paper.

- Every figure needs a clear takeaway visible at a glance.
- Choose chart types that match the data relationship (comparisons, trends, correlations, distributions).
- Include uncertainty (error bars, confidence intervals) when showing experimental results.
- Keep it clean — no clutter, clear labels with units, readable at print size.
</research_methodology>

<safeguard_research_reporting>
When the research concerns bypassin... [truncated, 80950 chars total]
```

### [3] ASSISTANT · 2026-09-29 20:03:25 UTC

```
I'll treat the pasted spec as the task. First, the skill, the workspace and the source data for the case pairs.
```

### [4] TOOL CALL — Bash · 2026-09-29 20:03:25 UTC

```
Inspect workspace and locate the figure skill:
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4; ls -la; ls .claude/skills 2>/dev/null; find / -path /proc -prune -o -type d -name aii-data-fig-gen -print 2>/dev/null | head; free -g; nproc
```

### [5] TOOL CALL — Bash · 2026-09-29 20:03:25 UTC

```
List Experiment 12 artifact contents:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; ls $W; ls $W/case_studies $W/results $W/figures 2>/dev/null | head -80
```

### [6] TOOL RESULT — Bash · 2026-09-29 20:05:23 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "brm0vpsua", "timedOutAfterMs": 120000, "backgroundCwdHint": "Session cwd remains /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4; directory changes made by the backgrounded command do not apply to subsequent commands."}
```

### [7] TOOL RESULT — Bash · 2026-09-29 20:05:23 UTC

```
{"stdout": "README.md\nai_atlas\naudit_headlines.py\ncase_studies\ndata\ndtw_cache\nfigures\nfull_method_out.json\nlib\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\nopen_features.parquet\npanel.parquet\npreview_method_out.json\npyproject.toml\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\ns0_skeleton.py\ns10_outputs.py\ns2_open.py\ns3_states.py\ns4_decomp.py\ns5_typology.py\ns6_sequence.py\ns7_seal.py\ns8_cases.py\ns9_atlas.py\nstate_sequences.parquet\ntests\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies:\npair01_CSEng\npair02_BGMMed\npair03_PHYS\npair04_SOC\npair05_CSEng\npair06_BGMMed\npair07_SOC\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/figures:\nfig_case_pairs.pdf\nfig_case_pairs.png\nfig_decomposition_waterfall.pdf\nfig_decomposition_waterfall.png\nfig_dtw_hmm_agreement.pdf\nfig_dtw_hmm_agreement.png\nfig_forest_explore_vs_retention.pdf\nfig_forest_explore_vs_retention.png\nfig_km_takeoff.pdf\nfig_km_takeoff.png\nfig_open_vs_pc1_hexbin.pdf\nfig_open_vs_pc1_hexbin.png\nfig_pca_loadings.pdf\nfig_pca_loadings.png\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/results:\nT7_rederivation.json\naudit_headlines.json\ncase_pairs.json\ndecomposition_dev.json\ndecomposition_heldout.json\ndeviations.json\nfield_communities.json\nfrozen_spec.json\nopen_diagnostics.json\npipeline_counts.json\npreregistration_R2.json\nsequence_light_dev.json\nsequence_light_heldout.json\nstates_verification.json\nt2_ego_open_reproduction.json\nt2_o2r_crosscheck.json\nt4_open_timing.json\ntrajectories_dev.json\ntrajectories_heldout.json\ntransitions_dev.json\ntransitions_heldout.json\ntypology_dev_assign.parquet\ntypology_heldout_assign.parquet\nunit_tests_T0.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] TOOL CALL — Bash · 2026-09-29 20:05:27 UTC

```
Read case pairs JSON and case study folders:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; head -c 6000 $W/results/case_pairs.json; echo; ls -la $W/case_studies/pair01_CSEng; ls $W/case_studies/*
```

### [9] TOOL RESULT — Bash · 2026-09-29 20:05:27 UTC

```
{"stdout": "{\n \"rule\": {\n  \"pools\": \"per reporting group: top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with OPEN_home defined (quintiles within reporting group)\",\n  \"match\": \"|z logvol diff| <= 0.25 and |z growth_c diff| <= 0.25 (z over all 12,499), same reporting group, |t0 diff| <= 2; widen to 0.35 for a group with no valid match (logged)\",\n  \"seeding\": \"first try concepts named in EXP8 case_exemplars.json (high/low lists) as anchors; then the pair with the largest OPEN_all gap among remaining matches; ties by the smallest Mahalanobis distance on (logvol, growth_c, offhome_share)\",\n  \"limits\": \"6-8 pairs; at most 2 from CS+Eng; at least 4 groups covered; one concept in at most one pair\",\n  \"outcome_use\": \"O2r is NOT used in selection; displayed after selection only\",\n  \"tol\": 0.25,\n  \"tol_wide\": 0.35,\n  \"max_pairs\": 8,\n  \"min_pairs\": 6,\n  \"max_cs_eng\": 2\n },\n \"selection_log\": {\n  \"generic_excluded\": 11157,\n  \"generic_hits\": [\n   {\n    \"ci\": 3,\n    \"name\": \"Complete intersection\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 4,\n    \"name\": \"Torque converter\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 16,\n    \"name\": \"Early adopter\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 37,\n    \"name\": \"Prospect theory\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 48,\n    \"name\": \"Dwarf spheroidal galaxy\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 52,\n    \"name\": \"Magnetoelectric effect\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 53,\n    \"name\": \"Neural development\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 54,\n    \"name\": \"Science communication\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 55,\n    \"name\": \"Acronym\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 61,\n    \"name\": \"Angle of attack\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 69,\n    \"name\": \"Turing test\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 70,\n    \"name\": \"Base course\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 74,\n    \"name\": \"Endogeneity\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 75,\n    \"name\": \"Impedance matching\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 91,\n    \"name\": \"Scientific management\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 92,\n    \"name\": \"World literature\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 98,\n    \"name\": \"Ferrimagnetism\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 105,\n    \"name\": \"Space launch\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 112,\n    \"name\": \"Trophic cascade\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 113,\n    \"name\": \"Ferroalloy\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 115,\n    \"name\": \"Team learning\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 116,\n    \"name\": \"Distributed feedback laser\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 133,\n    \"name\": \"Anabolism\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 136,\n    \"name\": \"Software bug\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 144,\n    \"name\": \"Expansive clay\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 150,\n    \"name\": \"HRAS\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 153,\n    \"name\": \"Economic order quantity\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 162,\n    \"name\": \"Autoregressive fractionally integrated moving average\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 168,\n    \"name\": \"Herbig Ae/Be star\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 186,\n    \"name\": \"Linear actuator\",\n    \"generic_why\": \"pre_onset_footprint|generic_regex\"\n   },\n   {\n    \"ci\": 192,\n    \"name\": \"Immunogenetics\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 193,\n    \"name\": \"Normalized Difference Vegetation Index\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 196,\n    \"name\": \"Matrix pencil\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 197,\n    \"name\": \"Measurement invariance\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 198,\n    \"name\": \"Health belief model\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 208,\n    \"name\": \"Life course approach\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 212,\n    \"name\": \"Recuperator\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 218,\n    \"name\": \"Optical rectification\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 219,\n    \"name\": \"Liquefied petroleum gas\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 224,\n    \"name\": \"Neutron reflectometry\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 230,\n    \"name\": \"Asian option\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 234,\n    \"name\": \"Mahalanobis distance\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 250,\n    \"name\": \"Extracellular fluid\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 263,\n    \"name\": \"Siegel modular form\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 269,\n    \"name\": \"Health equity\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 277,\n    \"name\": \"Glocalization\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 280,\n    \"name\": \"Cow dung\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 282,\n    \"name\": \"Uncanny valley\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 284,\n    \"name\": \"Linear code\",\n    \"generic_why\": \"pre_onset_footprint|generic_regex\"\n   },\n   {\n    \"ci\": 286,\n    \"name\": \"Medical prescription\",\n    \"generic_why\": \"pre_onset_footprint\"\n   },\n   {\n    \"ci\": 293,\n    \"name\": \ntotal 3828\ndrwxrwxrwx 2 aii-agent aii-agent 1081600 Sep 29 03:34 .\ndrwxrwxrwx 9 aii-agent aii-agent 2000502 Sep 29 03:35 ..\n-rw-rw-rw- 1 aii-agent aii-agent   47536 Sep 29 03:40 ego_snapshots.pdf\n-rw-rw-rw- 1 aii-agent aii-agent  587956 Sep 29 03:40 ego_snapshots.png\n-rw-rw-rw- 1 aii-agent aii-agent   25690 Sep 29 03:40 flow_raster.pdf\n-rw-rw-rw- 1 aii-agent aii-agent  167504 Sep 29 03:40 flow_raster.png\n-rw-rw-rw- 1 aii-agent aii-agent    6902 Sep 29 03:40 pair.json\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair01_CSEng:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair02_BGMMed:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair03_PHYS:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair04_SOC:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair05_CSEng:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair06_BGMMed:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair07_SOC:\nego_snapshots.pdf\nego_snapshots.png\nflow_raster.pdf\nflow_raster.png\npair.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-29 20:05:27 UTC

```
Check workspace skill directory:
ls /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/.claude/skills/ 2>&1; ls -la /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4
```

### [11] TOOL RESULT — Bash · 2026-09-29 20:05:27 UTC

```
{"stdout": "ls: cannot access '/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/.claude/skills/': No such file or directory\ntotal 3046\ndrwxrwxrwx 3 aii-agent aii-agent 1010364 Sep 29 20:03 .\ndrwxrwxrwx 7 aii-agent aii-agent 2000383 Sep 29 20:00 ..\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 20:00 .aii\n-rw-rw-rw- 1 aii-agent aii-agent      54 Sep 29 20:03 .aii_claude_session.json\n-rw-rw-rw- 1 aii-agent aii-agent  106083 Sep 29 20:05 .repl_agent.ptylog", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Skill · 2026-09-29 20:05:31 UTC

```
aii-data-fig-gen
```

### [13] TOOL RESULT — Skill · 2026-09-29 20:05:31 UTC

```
{"success": true, "commandName": "aii-data-fig-gen"}
```

### [14] TOOL CALL — Bash · 2026-09-29 20:05:31 UTC

```
Read pair 1 details and case_pairs structure:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; cat $W/case_studies/pair01_CSEng/pair.json; echo; python3 -c "
import json;d=json.load(open('$W/results/case_pairs.json'));print(list(d.keys()))
for k in d:
  if k!='selection_log': print(k, json.dumps(d[k])[:3000])
"
```

### [15] TOOL RESULT — Bash · 2026-09-29 20:05:31 UTC

```
{"stdout": "{\n \"pair\": \"pair01_CSEng\",\n \"rgroup\": \"CS+Eng\",\n \"selection\": {\n  \"gap\": 2.7915748198295907,\n  \"maha\": null,\n  \"tol\": 0.25,\n  \"anchor\": 0\n },\n \"illustration_only\": true,\n \"disclosure\": \"held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's analysis choices (fixed on DEV before held-out states/outcomes were read by this artifact)\",\n \"members\": {\n  \"HIGH_OPEN\": {\n   \"ci\": 42309,\n   \"concept_id\": 2779851693,\n   \"name\": \"Graphics processing unit\",\n   \"group\": \"Eng\",\n   \"t0\": 2008,\n   \"home\": \"22\",\n   \"B5\": {\n    \"logvol\": 4.890349128221754,\n    \"growth_c\": 0.7096764668771506,\n    \"offhome_share\": 0.5833333134651184,\n    \"entropy\": 1.761137844001943,\n    \"reach\": 8.0\n   },\n   \"OPEN\": {\n    \"all\": 2.1224511003497835,\n    \"home\": 0.4987059599128893,\n    \"size\": 1.7057721031414068\n   },\n   \"components\": {\n    \"all\": {\n     \"new_edge_rate\": 1.1794871794871795,\n     \"n_comm_W3\": 8.0,\n     \"participation\": 0.7587429111531191,\n     \"NOV_res\": -0.16491208007678892,\n     \"ego_density_W3\": 0.29590017825311943,\n     \"edge_persistence\": 0.11981566820276497\n    },\n    \"home\": {\n     \"new_edge_rate\": 0.8333333333333334,\n     \"n_comm_W3\": 2.0,\n     \"participation\": 0.2975206611570247,\n     \"NOV_res\": -0.14674982010074356,\n     \"ego_density_W3\": 0.8095238095238095,\n     \"edge_persistence\": 0.16666666666666666\n    },\n    \"size\": {\n     \"new_edge_rate\": 0.8174999999999999,\n     \"n_comm_W3\": 3.4,\n     \"participation\": 0.6112551208323845,\n     \"NOV_res\": -0.12873665207789226,\n     \"ego_density_W3\": 0.4280952380952381,\n     \"edge_persistence\": 0.03831043956043956\n    }\n   },\n   \"decomposition\": {\n    \"E2\": 7.0,\n    \"EH\": 11.0,\n    \"Bn\": 8.0,\n    \"M\": 1.5714285714285714,\n    \"rho\": 0.7272727272727273\n   },\n   \"axis\": {\n    \"PC1\": 10.554667195070259\n   },\n   \"outcomes_shown_after_selection\": {\n    \"O2r_m50\": 7.940617046233275,\n    \"O2r_resid\": 3.2599171916920078,\n    \"O1c\": 0.4662371464502586,\n    \"O1b\": 0.0,\n    \"O3\": 0.0,\n    \"O4\": -0.06187304938435001\n   },\n   \"recognition_events_same\": [\n    {\n     \"source\": \"wikipedia_en\",\n     \"event_type\": \"wikipedia_page_created_estimated\",\n     \"year\": 2003,\n     \"year_usable\": true,\n     \"lag_to_t0\": -5,\n     \"pre_t0\": true\n    }\n   ],\n   \"dependency_event_count\": 1,\n   \"top_W3_neighbours\": [\n    [\n     \"Digital Holography and Microscopy\",\n     5.85,\n     3\n    ],\n    [\n     \"Optical Coherence Tomography Applications\",\n     5.55,\n     5\n    ],\n    [\n     \"Image and Object Detection Techniques\",\n     5.33,\n     4\n    ],\n    [\n     \"Autonomous Vehicle Technology and Safety\",\n     5.31,\n     2\n    ],\n    [\n     \"Advanced Fluorescence Microscopy Techniques\",\n     4.94,\n     4\n    ],\n    [\n     \"Parallel Computing and Optimization Techniques\",\n     4.87,\n     6\n    ],\n    [\n     \"Photoacoustic and Ultrasonic Imaging\",\n     4.84,\n     4\n    ],\n    [\n     \"Computer Graphics and Visualization Techniques\",\n     4.83,\n     4\n    ],\n    [\n     \"Scientific Research and Discoveries\",\n     4.75,\n     3\n    ],\n    [\n     \"Advanced Optical Imaging Technologies\",\n     4.74,\n     2\n    ]\n   ],\n   \"ego_snapshot_stats\": {\n    \"HIGH_OPEN_W1_all\": {\n     \"n_nodes\": 12,\n     \"n_edges\": 35,\n     \"n_communities\": 6,\n     \"density\": 0.5303030303030303\n    },\n    \"HIGH_OPEN_W2_all\": {\n     \"n_nodes\": 22,\n     \"n_edges\": 48,\n     \"n_communities\": 8,\n     \"density\": 0.2077922077922078\n    },\n    \"HIGH_OPEN_W3_all\": {\n     \"n_nodes\": 34,\n     \"n_edges\": 166,\n     \"n_communities\": 8,\n     \"density\": 0.29590017825311943\n    },\n    \"HIGH_OPEN_W3_home\": {\n     \"n_nodes\": 7,\n     \"n_edges\": 17,\n     \"n_communities\": 2,\n     \"density\": 0.8095238095238095\n    }\n   }\n  },\n  \"LOW_OPEN\": {\n   \"ci\": 33270,\n   \"concept_id\": 2777596722,\n   \"name\": \"Vertical axis wind turbine\",\n   \"group\": \"Eng\",\n   \"t0\": 2009,\n   \"home\": \"22\",\n   \"B5\": {\n    \"logvol\": 4.897839799950911,\n    \"growth_c\": 0.6931471805599453,\n    \"offhome_share\": 0.1078431382775306,\n    \"entropy\": 0.4893724062136025,\n    \"reach\": 3.0\n   },\n   \"OPEN\": {\n    \"all\": -0.6691237194798072,\n    \"home\": -0.4069733522454708,\n    \"size\": -0.5376855099279206\n   },\n   \"components\": {\n    \"all\": {\n     \"new_edge_rate\": 0.18181818181818182,\n     \"n_comm_W3\": 1.0,\n     \"participation\": 0.0,\n     \"NOV_res\": -0.609326004399896,\n     \"ego_density_W3\": 0.696969696969697,\n     \"edge_persistence\": 0.35416666666666663\n    },\n    \"home\": {\n     \"new_edge_rate\": 0.26666666666666666,\n     \"n_comm_W3\": 1.0,\n     \"participation\": 0.0,\n     \"NOV_res\": -0.6924204447969953,\n     \"ego_density_W3\": 0.6444444444444445,\n     \"edge_persistence\": 0.3246753246753247\n    },\n    \"size\": {\n     \"new_edge_rate\": 0.16127645502645502,\n     \"n_comm_W3\": 1.0,\n     \"participation\": 0.0,\n     \"NOV_res\": -0.6684926710665626,\n     \"ego_density_W3\": 0.7285606060606059,\n     \"edge_persistence\": 0.3149963924963925\n    }\n   },\n   \"decomposition\": {\n    \"E2\": 2.0,\n    \"EH\": 6.0,\n    \"Bn\": 4.0,\n    \"M\": 3.0,\n    \"rho\": 0.6666666666666666\n   },\n   \"axis\": {\n    \"PC1\": 0.8168201244858367\n   },\n   \"outcomes_shown_after_selection\": {\n    \"O2r_m50\": 3.765660415396956,\n    \"O2r_resid\": -0.9180104704375194,\n    \"O1c\": 0.895173808433233,\n    \"O1b\": 1.0,\n    \"O3\": 0.0,\n    \"O4\": 0.8695705766597654\n   },\n   \"recognition_events_same\": [\n    {\n     \"source\": \"wikipedia_en\",\n     \"event_type\": \"wikipedia_page_created_estimated\",\n     \"year\": 2020,\n     \"year_usable\": false,\n     \"lag_to_t0\": 11,\n     \"pre_t0\": false\n    }\n   ],\n   \"dependency_event_count\": 1,\n   \"top_W3_neighbours\": [\n    [\n     \"Icing and De-icing Technologies\",\n     6.91,\n     13\n    ],\n    [\n     \"Wind Turbine Control Systems\",\n     6.34,\n     6\n    ],\n    [\n     \"Aerospace Engineering and Energy Systems\",\n     6.3,\n     6\n    ],\n    [\n     \"Aerodynamics and Fluid Dynamics Research\",\n     5.93,\n     12\n    ],\n    [\n     \"Fluid Dynamics and Vibration Analysis\",\n     5.79,\n     11\n    ],\n    [\n     \"Soil, Finite Element Methods\",\n     4.82,\n     5\n    ],\n    [\n     \"Vibration and Dynamic Analysis\",\n     4.43,\n     6\n    ],\n    [\n     \"Electric Motor Design and Analysis\",\n     4.41,\n     3\n    ],\n    [\n     \"Magnetic Bearings and Levitation Dynamics\",\n     4.08,\n     2\n    ],\n    [\n     \"Fluid Dynamics and Turbulent Flows\",\n     3.58,\n     3\n    ]\n   ],\n   \"ego_snapshot_stats\": {\n    \"LOW_OPEN_W1_all\": {\n     \"n_nodes\": 10,\n     \"n_edges\": 32,\n     \"n_communities\": 2,\n     \"density\": 0.7111111111111111\n    },\n    \"LOW_OPEN_W2_all\": {\n     \"n_nodes\": 10,\n     \"n_edges\": 32,\n     \"n_communities\": 2,\n     \"density\": 0.7111111111111111\n    },\n    \"LOW_OPEN_W3_all\": {\n     \"n_nodes\": 12,\n     \"n_edges\": 46,\n     \"n_communities\": 1,\n     \"density\": 0.696969696969697\n    },\n    \"LOW_OPEN_W3_home\": {\n     \"n_nodes\": 10,\n     \"n_edges\": 29,\n     \"n_communities\": 1,\n     \"density\": 0.6444444444444445\n    }\n   }\n  }\n },\n \"flag_open_home_order_disagrees\": false,\n \"high_open_has_higher_O2r_resid\": true\n}\n['rule', 'selection_log', 'pairs', 'descriptive_summary', 'disclosure', 'Source']\nrule {\"pools\": \"per reporting group: top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with OPEN_home defined (quintiles within reporting group)\", \"match\": \"|z logvol diff| <= 0.25 and |z growth_c diff| <= 0.25 (z over all 12,499), same reporting group, |t0 diff| <= 2; widen to 0.35 for a group with no valid match (logged)\", \"seeding\": \"first try concepts named in EXP8 case_exemplars.json (high/low lists) as anchors; then the pair with the largest OPEN_all gap among remaining matches; ties by the smallest Mahalanobis distance on (logvol, growth_c, offhome_share)\", \"limits\": \"6-8 pairs; at most 2 from CS+Eng; at least 4 groups covered; one concept in at most one pair\", \"outcome_use\": \"O2r is NOT used in selection; displayed after selection only\", \"tol\": 0.25, \"tol_wide\": 0.35, \"max_pairs\": 8, \"min_pairs\": 6, \"max_cs_eng\": 2}\npairs [{\"pair\": \"pair01_CSEng\", \"rgroup\": \"CS+Eng\", \"high\": \"Graphics processing unit\", \"low\": \"Vertical axis wind turbine\", \"OPEN_all\": [2.1224511003497835, -0.6691237194798072], \"OPEN_home\": [0.4987059599128893, -0.4069733522454708], \"logvol\": [4.890349128221754, 4.897839799950911], \"O2r_resid\": [3.2599171916920078, -0.9180104704375194], \"Bn\": [8.0, 4.0], \"E2\": [7.0, 2.0], \"rho\": [0.7272727272727273, 0.6666666666666666], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair02_BGMMed\", \"rgroup\": \"BGM+Med\", \"high\": \"Shotgun proteomics\", \"low\": \"Image-guided radiation therapy\", \"OPEN_all\": [1.5506709977859554, -1.2190170907446358], \"OPEN_home\": [1.4542920248036852, -0.7631447507436927], \"logvol\": [4.418840607796598, 4.477336814478207], \"O2r_resid\": [1.3359666347862138, -3.5168864406072657], \"Bn\": [3.0, 0.0], \"E2\": [3.0, 1.0], \"rho\": [0.6, 0.0], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair03_PHYS\", \"rgroup\": \"PHYS\", \"high\": \"Nanocarriers\", \"low\": \"Nanosheet\", \"OPEN_all\": [0.6659290147271483, -0.6149791238010124], \"OPEN_home\": [0.3895793814732094, -0.23251228926495204], \"logvol\": [4.709530201312334, 4.795790545596741], \"O2r_resid\": [2.787922462888554, 0.7304328490468972], \"Bn\": [6.0, 7.0], \"E2\": [6.0, 4.0], \"rho\": [0.6, 0.875], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair04_SOC\", \"rgroup\": \"SOC\", \"high\": \"Soft power\", \"low\": \"Autonomous learning\", \"OPEN_all\": [1.9551989199475421, -0.38976664105244546], \"OPEN_home\": [1.6015831865502823, 0.3134843986564578], \"logvol\": [4.941642422609304, 4.941642422609304], \"O2r_resid\": [1.3480751627507148, 0.26018283759672567], \"Bn\": [6.0, 4.0], \"E2\": [4.0, 3.0], \"rho\": [0.75, 1.0], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair05_CSEng\", \"rgroup\": \"CS+Eng\", \"high\": \"Scopus\", \"low\": \"Oxygen reduction reaction\", \"OPEN_all\": [1.843065009540754, -0.8267895779585691], \"OPEN_home\": [0.20170638376003294, -0.4097957144497746], \"logvol\": [4.553876891600541, 4.51085950651685], \"O2r_resid\": [5.685703432708352, 0.7422291339682907], \"Bn\": [9.0, 5.0], \"E2\": [6.0, 4.0], \"rho\": [0.6428571428571429, 0.8333333333333334], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair06_BGMMed\", \"rgroup\": \"BGM+Med\", \"high\": \"Sclerostin\", \"low\": \"IgG4-related disease\", \"OPEN_all\": [1.5477404399585464, -0.8642079724220579], \"OPEN_home\": [2.8382178903528357, -0.8004409804793847], \"logvol\": [5.081404364984463, 5.111987788356544], \"O2r_resid\": [-0.9212264694059553, -1.578998499974558], \"Bn\": [4.0, 3.0], \"E2\": [3.0, 2.0], \"rho\": [1.0, 0.75], \"high_open_higher_O2r_resid\": true, \"open_home_order_disagrees\": false}, {\"pair\": \"pair07_SOC\", \"rgroup\": \"SOC\", \"high\": \"User-generated content\", \"low\": \"Mindfulness-based cognitive therapy\", \"OPEN_all\": [1.1430986105439127, -0.4039826307924678], \"OPEN_home\": [1.4395310622494302, -0.46320683684895664], \"logvol\": [4.52178857704\ndescriptive_summary \"in 7 of 7 pairs the high-OPEN member has the higher O2r_resid (no p-value; n <= 8; illustration only)\"\ndisclosure \"held-out outcomes were previously unsealed by EXP5/EXP7/EXP8; this seal fixes only this artifact's analysis choices (fixed on DEV before held-out states/outcomes were read by this artifact)\"\nSource \"s8_cases.py; rule frozen in results/frozen_spec.json (case_pairs)\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] THINKING · 2026-09-29 20:05:41 UTC

```
Pair 1's real numbers don't match the spec — GPU shows 7/11/8 and wind turbine shows 2/6/4 for off-home fields, and the ego network has only 1 community, not the claimed 2 clusters. I'll now dig into the yearly timeline and ego-network data underlying these figures.
```

### [17] TOOL CALL — Bash · 2026-09-29 20:05:41 UTC

```
Inspect case-study script structure:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; wc -l $W/s8_cases.py; grep -n "def \|parquet\|W3\|flow_raster\|ego_snap\|community\|leiden" $W/s8_cases.py | head -80
```

### [18] TOOL RESULT — Bash · 2026-09-29 20:05:41 UTC

```
{"stdout": "280 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/s8_cases.py\n23:KEYS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\n26:def base_table() -> pd.DataFrame:\n27:    J = pd.read_parquet(DATA / \"joined.parquet\")\n28:    O = pd.read_parquet(ROOT / \"open_features.parquet\").drop(columns=[\"split\", \"group\", \"rgroup\", \"med_home\"])\n30:    pre = pd.read_parquet(DATA / \"pre_onset.parquet\")\n38:def exemplar_ci() -> set[int]:\n44:def select_pairs(T: pd.DataFrame) -> tuple[list[dict], dict]:\n76:    def take(g):\n98:def recognition(cids: list[int]) -> dict:\n99:    o5 = pd.read_parquet(E8_DATA / \"o5_events.parquet\")\n124:def ego_ctx():\n132:def works_for(ci: int, em: pd.DataFrame, home: list[int], home_only: bool):\n140:def main() -> None:\n147:    Dd = pd.read_parquet(DATA / \"decomp_inputs.parquet\")\n148:    ta = pd.concat([pd.read_parquet(RES / \"typology_dev_assign.parquet\"),\n149:                    pd.read_parquet(RES / \"typology_heldout_assign.parquet\")])\n152:    ci_pos = {c: i for i, c in enumerate(pd.read_parquet(DATA / \"joined.parquet\").ci)}\n156:    em = pd.read_parquet(E8_DATA / \"frame_matches_early/part_001.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"topics\"])\n189:        viz.save(fig, out / \"flow_raster\")\n190:        # ego snapshots W1..W3 (all papers) + W3 home-only, both members\n197:            for w_i, w in enumerate((\"W1\", \"W2\", \"W3\")):\n200:                snap_stats[f\"{role}_{w}_all\"] = viz.ego_snapshot(\n205:            snap_stats[f\"{role}_W3_home\"] = viz.ego_snapshot(\n206:                axes[j, 3], s[\"_nb\"][\"W3\"], s[\"_cnt\"][\"W3\"], s[\"_pmi\"][\"W3\"], ctx[\"full_edges\"][sl], ctx[\"comm\"][sl],\n207:                ctx[\"names\"], f\"\\nW3 ({t0 + 2}), home-venue papers only\")\n209:                     \"Leiden community, size = count)\", fontsize=9)\n210:        viz.save(fig, out / \"ego_snapshots\")\n230:                \"top_W3_neighbours\": [(ctx[\"names\"][v], round(float(snaps[\"all\"][\"_pmi\"][\"W3\"][v]), 2),\n231:                                       int(snaps[\"all\"][\"_cnt\"][\"W3\"][v]))\n232:                                      for v in sorted(snaps[\"all\"][\"_nb\"][\"W3\"],\n233:                                                      key=lambda v: -np.nan_to_num(snaps[\"all\"][\"_pmi\"][\"W3\"][v]))[:10]],\n234:                \"ego_snapshot_stats\": {kk: v for kk, v in snap_stats.items() if kk.startswith(role)}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Read · 2026-09-29 20:05:41 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair01_CSEng/flow_raster.png
```

### [20] TOOL RESULT — Read · 2026-09-29 20:05:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [21] TOOL CALL — Read · 2026-09-29 20:05:41 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/case_studies/pair01_CSEng/ego_snapshots.png
```

### [22] TOOL RESULT — Read · 2026-09-29 20:05:41 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [23] SYSTEM-USER prompt · 2026-09-29 20:05:41 UTC

```
[Image: original 2145x1118, displayed at 2000x1042. Multiply coordinates by 1.07 to map to original image.]
```

### [24] ASSISTANT · 2026-09-29 20:05:49 UTC

```
Real per-year state data and ego-network data exist. I'll re-derive both from Exp12's own code path instead of using the spec's invented clusters. First, how s8_cases builds them:
```

### [25] TOOL CALL — Bash · 2026-09-29 20:05:49 UTC

```
Read case-study builder and plotting helpers:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; sed -n 1,25p $W/s8_cases.py; sed -n 120,215p $W/s8_cases.py; ls $W/lib; grep -n "def ego_snapshot\|def flow_raster\|def state_area" -A45 $W/lib/viz.py | head -150
```

### [26] TOOL RESULT — Bash · 2026-09-29 20:05:49 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"S8 MATCHED CASE PAIRS (most-similar design; rule frozen in results/frozen_spec.json before any outcome was read).\nPairs are matched on B5 volume and growth within a reporting group and onset window and are OPPOSITE on OPEN_all;\nO2r is shown only after selection. ILLUSTRATION, NOT INFERENCE (n <= 8).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np  # noqa: E402\nimport pandas as pd  # noqa: E402\n\nimport cases_spec as CS  # noqa: E402\nimport viz  # noqa: E402\nfrom common import (CASES, DATA, DISCLOSURE, DS2, E6, E8, E8_DATA, FIGS, RES, ROOT, REPORT_GROUPS, add_deviation,  # noqa: E402\n                    jdump, load_outcomes, network_guard, setup_logger, update_status)\n\nnetwork_guard()\nlogger = setup_logger(\"s8_cases\")\nKEYS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\n\n\n        del d\n    return {\"o5_events\": out, \"dependency_event_counts\": dep}\n\n\ndef ego_ctx():\n    import ego_open\n    from ego_ctx import rq1_context\n    ctx = rq1_context()\n    ego_open.set_context(ctx)\n    return ctx\n\n\ndef works_for(ci: int, em: pd.DataFrame, home: list[int], home_only: bool):\n    d = em[em.ci == ci]\n    if home_only:\n        d = d[d.vfield.isin([h - 10 for h in home])]\n    return list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    import ego_open\n    O = load_outcomes().all()\n    T = base_table()\n    pairs, log = select_pairs(T)          # selection uses NO outcome column\n    logger.info(f\"selected {len(pairs)} pairs over {log['groups_covered']}\")\n    T = T.merge(O.drop(columns=[\"split\"]), on=\"ci\", how=\"left\")\n    Dd = pd.read_parquet(DATA / \"decomp_inputs.parquet\")\n    ta = pd.concat([pd.read_parquet(RES / \"typology_dev_assign.parquet\"),\n                    pd.read_parquet(RES / \"typology_heldout_assign.parquet\")])\n    T = T.merge(Dd[[\"ci\", \"E2\", \"EH\", \"Bn\"]], on=\"ci\").merge(ta[[\"ci\", \"PC1\"] + ([\"PC2\"] if \"PC2\" in ta else [])], on=\"ci\", how=\"left\")\n    codes = np.load(DATA / \"state_codes.npy\")\n    ci_pos = {c: i for i, c in enumerate(pd.read_parquet(DATA / \"joined.parquet\").ci)}\n    bb = json.loads((E6 / \"inputs/field_backbone.json\").read_text())\n    comm = np.asarray(json.loads((RES / \"field_communities.json\").read_text())[\"labels\"])\n    order = np.lexsort((np.arange(26), comm))\n    em = pd.read_parquet(E8_DATA / \"frame_matches_early/part_001.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"topics\"])\n    em = em[em.ci.isin({p[\"hi\"] for p in pairs} | {p[\"lo\"] for p in pairs})]\n    ctx = ego_ctx()\n    rec = recognition([int(T.set_index(\"ci\").concept_id[c]) for p in pairs for c in (p[\"hi\"], p[\"lo\"])])\n    summary = []\n    for k, p in enumerate(pairs, start=1):\n        pid = f\"pair{k:02d}_{p['rgroup'].replace('+', '')}\"\n        out = CASES / pid\n        out.mkdir(parents=True, exist_ok=True)\n        R = T.set_index(\"ci\").loc[[p[\"hi\"], p[\"lo\"]]]\n        fig, axes = __import__(\"matplotlib.pyplot\").pyplot.subplots(2, 2, figsize=(9, 6.5),\n                                                                     gridspec_kw={\"height_ratios\": [1, 1.6]})\n        members = {}\n        for j, (role, ci) in enumerate(((\"HIGH_OPEN\", p[\"hi\"]), (\"LOW_OPEN\", p[\"lo\"]))):\n            r = R.loc[ci]\n            cc = codes[ci_pos[ci]]\n            viz.state_flow(axes[0, j], np.where(cc == 4, -2, cc)[:, :].clip(-1, 3) if False else\n                           np.where(cc == 4, 0, cc), f\"{role}: {r['name']} (t0 {int(r.t0)})\")\n            viz.state_raster(axes[1, j], cc, order, bb[\"fields\"], comm)\n            if j == 1:\n                axes[1, j].set_yticklabels([])\n            snaps = {}\n            home = [int(h) for h in str(r.home_list).split(\";\")]\n            for build in (\"all\", \"home\"):\n                w = works_for(ci, em, home, build == \"home\")\n                snaps[build] = ego_open.concept_open(str(r[\"name\"]), [], int(r.t0), w, keep_nb=True)\n            members[role] = (ci, r, snaps)\n            cid = int(r.concept_id)\n            members[role] = members[role] + ({\"events_same\": rec[\"o5_events\"].get(cid, []),\n                                              \"dependency_event_count\": rec[\"dependency_event_counts\"].get(cid)},)\n        axes[0, 0].legend(loc=\"upper left\", frameon=False, fontsize=7)\n        fig.suptitle(f\"Case pair {k} ({p['rgroup']}): matched on volume/growth, opposite OPEN_all \"\n                     f\"(illustration, not inference)\", fontsize=9)\n        viz.save(fig, out / \"flow_raster\")\n        # ego snapshots W1..W3 (all papers) + W3 home-only, both members\n        plt = __import__(\"matplotlib.pyplot\").pyplot\n        fig, axes = plt.subplots(2, 4, figsize=(13, 6.2))\n        snap_stats = {}\n        for j, role in enumerate((\"HIGH_OPEN\", \"LOW_OPEN\")):\n            ci, r, snaps, _ = members[role]\n            t0 = int(r.t0)\n            for w_i, w in enumerate((\"W1\", \"W2\", \"W3\")):\n                s = snaps[\"all\"]\n                sl = __import__(\"ego\").slice_of(t0 + w_i)\n                snap_stats[f\"{role}_{w}_all\"] = viz.ego_snapshot(\n                    axes[j, w_i], s[\"_nb\"][w], s[\"_cnt\"][w], s[\"_pmi\"][w], ctx[\"full_edges\"][sl], ctx[\"comm\"][sl],\n                    ctx[\"names\"], (f\"{role}: {r['name'][:30]}\\n\" if w_i == 0 else \"\\n\") + f\"{w} ({t0 + w_i}), all papers\")\n            s = snaps[\"home\"]\n            sl = __import__(\"ego\").slice_of(t0 + 2)\n            snap_stats[f\"{role}_W3_home\"] = viz.ego_snapshot(\n                axes[j, 3], s[\"_nb\"][\"W3\"], s[\"_cnt\"][\"W3\"], s[\"_pmi\"][\"W3\"], ctx[\"full_edges\"][sl], ctx[\"comm\"][sl],\n                ctx[\"names\"], f\"\\nW3 ({t0 + 2}), home-venue papers only\")\n        fig.suptitle(f\"Case pair {k}: topic co-occurrence ego networks (nodes = PMI>0 neighbour topics, colour = EXP3 \"\n                     \"Leiden community, size = count)\", fontsize=9)\n        viz.save(fig, out / \"ego_snapshots\")\n        pj = {\"pair\": pid, \"rgroup\": p[\"rgroup\"], \"selection\": {k2: p[k2] for k2 in (\"gap\", \"maha\", \"tol\", \"anchor\")},\n              \"illustration_only\": True, \"disclosure\": DISCLOSURE, \"members\": {}}\n        for role in (\"HIGH_OPEN\", \"LOW_OPEN\"):\n            ci, r, snaps, recog = members[role]\n            t0 = int(r.t0)\nbuild_features_exp8.py\ncases_spec.py\ncommon.py\ncommon_exp8.py\nd3.py\ndecomp.py\nego.py\nego_ctx.py\nego_open.py\nlib_outcomes.py\nrq1stats.py\nseal_exp8.py\ntraj_exp6.py\ntypology.py\nviz.py\n61:def ego_snapshot(ax, nb: list[int], cnt: np.ndarray, pmi: np.ndarray, edges: tuple[np.ndarray, np.ndarray],\n62-                 comm: np.ndarray, names: list[str], title: str, seed: int = 0) -> dict:\n63-    import networkx as nx\n64-    ax.set_axis_off()\n65-    ax.set_title(title, loc=\"left\", fontsize=7)\n66-    if len(nb) == 0:\n67-        ax.text(0.5, 0.5, \"no neighbours\", ha=\"center\", va=\"center\", transform=ax.transAxes, fontsize=7)\n68-        return {\"n_nodes\": 0, \"n_edges\": 0}\n69-    ins = np.zeros(len(cnt), bool)\n70-    ins[nb] = True\n71-    a, b = edges\n72-    m = ins[a] & ins[b]\n73-    G = nx.Graph()\n74-    G.add_nodes_from(nb)\n75-    G.add_edges_from(zip(a[m].tolist(), b[m].tolist()))\n76-    pos = nx.spring_layout(G, seed=seed, k=1.2 / max(1, np.sqrt(len(nb))))\n77-    cmap = plt.get_cmap(\"tab20\")\n78-    cols = [cmap(int(comm[v]) % 20) for v in G.nodes]\n79-    sizes = [12 + 10 * float(cnt[v]) for v in G.nodes]\n80-    nx.draw_networkx_edges(G, pos, ax=ax, width=0.3, alpha=0.4)\n81-    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=cols, node_size=sizes, linewidths=0)\n82-    top = sorted(nb, key=lambda v: -np.nan_to_num(pmi[v]))[:10]\n83-    for v in top:\n84-        ax.text(pos[v][0], pos[v][1], names[v][:26], fontsize=4.2, ha=\"center\", va=\"bottom\")\n85-    return {\"n_nodes\": G.number_of_nodes(), \"n_edges\": G.number_of_edges(),\n86-            \"n_communities\": int(len({int(comm[v]) for v in nb})),\n87-            \"density\": float(nx.density(G)) if G.number_of_nodes() > 1 else None}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-09-29 20:05:53 UTC

```
Read state-flow plotting code and data listing:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; sed -n 1,60p $W/lib/viz.py; ls -la $W/data | head -40; cat $W/lib/ego_ctx.py | head -80
```

### [28] TOOL RESULT — Bash · 2026-09-29 20:05:53 UTC

```
{"stdout": "\"\"\"Plot helpers shared by the case pairs (S8), the atlas (S9) and the summary figures (S10): house style, state\nflows (stacked ribbons), field x age state rasters and topic ego-network snapshots.\"\"\"\nfrom __future__ import annotations\n\nimport matplotlib\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt  # noqa: E402\nimport numpy as np  # noqa: E402\n\nplt.rcParams.update({\"pdf.fonttype\": 42, \"ps.fonttype\": 42, \"font.size\": 9, \"axes.titlesize\": 10,\n                     \"axes.labelsize\": 9, \"legend.fontsize\": 8, \"axes.spines.top\": False,\n                     \"axes.spines.right\": False, \"figure.dpi\": 150, \"savefig.bbox\": \"tight\"})\n# Okabe-Ito colourblind-safe palette\nOI = {\"blue\": \"#0072B2\", \"orange\": \"#E69F00\", \"green\": \"#009E73\", \"vermillion\": \"#D55E00\", \"sky\": \"#56B4E9\",\n      \"purple\": \"#CC79A7\", \"yellow\": \"#F0E442\", \"grey\": \"#999999\", \"black\": \"#000000\"}\nSTATE_COL = {0: \"#EEEEEE\", 1: OI[\"sky\"], 2: OI[\"blue\"], 3: OI[\"vermillion\"], 4: OI[\"grey\"], -1: \"#FFFFFF\"}\nSTATE_LAB = {0: \"untouched\", 1: \"entered\", 2: \"retained\", 3: \"lost\", 4: \"home\"}\n\n\ndef save(fig, path_no_ext) -> list[str]:\n    out = []\n    for ext in (\"png\", \"pdf\"):\n        p = f\"{path_no_ext}.{ext}\"\n        fig.savefig(p, dpi=200 if ext == \"png\" else None)\n        out.append(p)\n    plt.close(fig)\n    return out\n\n\ndef state_flow(ax, codes: np.ndarray, title: str) -> None:\n    \"\"\"codes [ages, 26] state codes for one concept -> stacked ribbons of off-home field counts per state.\"\"\"\n    ages = np.arange(codes.shape[0])\n    valid = (codes >= 0).all(1)\n    base = np.zeros(len(ages))\n    for s in (2, 1, 3, 0):\n        c = np.where(valid, (codes == s).sum(1), np.nan)\n        ax.fill_between(ages, base, base + c, color=STATE_COL[s], label=STATE_LAB[s], step=None, lw=0.3,\n                        edgecolor=\"white\")\n        base = base + np.nan_to_num(c)\n    ax.set_xlim(0, ages[-1])\n    ax.set_xlabel(\"age (years since onset t0)\")\n    ax.set_ylabel(\"off-home fields\")\n    ax.set_title(title, loc=\"left\")\n\n\ndef state_raster(ax, codes: np.ndarray, order: np.ndarray, field_names: list[str], comm: np.ndarray) -> None:\n    from matplotlib.colors import ListedColormap\n    cm = ListedColormap([STATE_COL[s] for s in (-1, 0, 1, 2, 3, 4)])\n    M = codes[:, order].T + 1\n    ax.imshow(M, aspect=\"auto\", cmap=cm, vmin=0, vmax=5, interpolation=\"nearest\")\n    ax.set_yticks(range(len(order)))\n    ax.set_yticklabels([field_names[i][:22] for i in order], fontsize=5)\n    ax.set_xticks(range(codes.shape[0]))\n    ax.set_xlabel(\"age\")\n    for j in range(1, len(order)):\n        if comm[order[j]] != comm[order[j - 1]]:\n            ax.axhline(j - 0.5, color=\"black\", lw=0.4)\n\n\ntotal 14210\ndrwxrwxrwx  6 aii-agent aii-agent 2002478 Sep 29 03:25 .\ndrwxrwxrwx 12 aii-agent aii-agent 2007205 Sep 29 05:04 ..\n-rw-rw-rw-  1 aii-agent aii-agent  178879 Sep 29 02:28 decomp_inputs.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 1534465 Sep 29 02:23 joined.parquet\ndrwxrwxrwx  4 aii-agent aii-agent 2001853 Sep 29 02:26 open_parts\ndrwxrwxrwx  2 aii-agent aii-agent 1026876 Sep 29 02:24 open_test\ndrwxrwxrwx  2 aii-agent aii-agent 1034196 Sep 29 02:25 open_timing_home\ndrwxrwxrwx  2 aii-agent aii-agent 1049867 Sep 29 02:25 open_timing_size\n-rw-rw-rw-  1 aii-agent aii-agent    1980 Sep 29 02:29 open_zconst.json\n-rw-rw-rw-  1 aii-agent aii-agent   89140 Sep 29 02:28 pre_onset.parquet\n-rw-rw-rw-  1 aii-agent aii-agent 3574842 Sep 29 02:27 state_codes.npy\n-rw-rw-rw-  1 aii-agent aii-agent   45806 Sep 29 03:25 typology_frozen.pkl\n\"\"\"Context for lib/ego.py: EXP3 Leiden-gamma-3 topic backbones (slices 2000-04/05-09/10-14), topic metadata,\ncontent lemmas (verbatim from EXP3 common.py), and the Pass A full-corpus topic background.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport re\nfrom collections import Counter\nfrom functools import lru_cache\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import E8_DATA as DATA, E8_INPUTS as INPUTS  # PATCH (plan fallback 4): resolve against EXP8 inputs\n\n_STOP = set(\"a an and are as at be but by for if in into is it no not of on or such that the their then there these \"\n            \"they this to was will with its via from using based\".split())\n_TOK = re.compile(r\"[^\\W_]+\", re.UNICODE)\n\n\n@lru_cache(maxsize=None)\ndef _stemmer():\n    import snowballstemmer\n    return snowballstemmer.stemmer(\"porter\")\n\n\ndef lemmas(text: str) -> set[str]:\n    t = re.sub(r\"[\\-‐-—/]\", \" \", str(text).lower())\n    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}\n\n\ndef topic_lemma_df(names: list[str]) -> Counter:\n    df = Counter()\n    for n in names:\n        df.update(lemmas(n))\n    return df\n\n\ndef backbone_context() -> dict:\n    tids = json.loads((INPUTS / \"topic_ids.json\").read_text())\n    tm = pd.read_csv(INPUTS / \"topic_meta.csv\").set_index(\"topic\").loc[tids]\n    sl = [np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\") for s in range(3)]\n    names = tm.name.tolist()\n    return dict(nt=len(tids), comm=[z[\"comm\"] for z in sl], comm_q=[z[\"comm_q\"] for z in sl],\n                deg=[z[\"deg\"] for z in sl], knn=[(z[\"ka\"], z[\"kb\"]) for z in sl],\n                full_edges=[(z[\"a\"], z[\"b\"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,\n                ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names], lemmas=lemmas)\n\n\ndef rq1_context() -> dict:\n    ctx = backbone_context()\n    z = np.load(DATA / \"bg_topics.npz\")\n    years = z[\"years\"].tolist()\n    ctx.update(years=years, bg=z[\"BG\"], Gt=dict(zip(years, z[\"GT\"].tolist())))\n    return ctx", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-29 20:06:07 UTC

```
I'll pull the exact per-year state codes for both concepts from `state_codes.npy`, and check which Python has the libraries Exp12 needs.
```

### [30] TOOL CALL — Bash · 2026-09-29 20:06:07 UTC

```
Extract yearly off-home field states for both concepts:
W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; ls -a $W | grep -i venv; which python python3; python -c "import matplotlib, pandas, networkx, numpy, snowballstemmer; print('ok', matplotlib.__version__)"; cd $W && python -c "
import numpy as np, pandas as pd, json
codes=np.load('data/state_codes.npy', mmap_mode='r'); print(codes.shape, codes.dtype)
J=pd.read_parquet('data/joined.parquet', columns=['ci','name','t0'])
bb=json.load(open('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_6/inputs/field_backbone.json'))
pos={c:i for i,c in enumerate(J.ci)}
for ci in (42309,33270):
  cc=np.asarray(codes[pos[ci]]); print(J.iloc[pos[ci]].to_dict())
  for a in range(cc.shape[0]):
    print(a, 'ent',(cc[a]==1).sum(),'ret',(cc[a]==2).sum(),'lost',(cc[a]==3).sum(),'ever',np.isin(cc[a],[1,2,3]).sum(), 'home',(cc[a]==4).sum())
" 2>&1 | tail -40; grep -n "^E6\|^E8\|E6 =\|E8 =" $W/lib/common.py
```

### [31] TOOL RESULT — Bash · 2026-09-29 20:06:11 UTC

```
{"stdout": "/usr/local/bin/python\n/usr/local/bin/python3\nTraceback (most recent call last):\n  File \"<string>\", line 1, in <module>\nModuleNotFoundError: No module named 'networkx'\n(12499, 11, 26) int8\n{'ci': 42309, 'name': 'Graphics processing unit', 't0': 2008}\n0 ent 3 ret 0 lost 0 ever 3 home 1\n1 ent 4 ret 1 lost 0 ever 5 home 1\n2 ent 4 ret 3 lost 0 ever 7 home 1\n3 ent 3 ret 5 lost 0 ever 8 home 1\n4 ent 3 ret 6 lost 0 ever 9 home 1\n5 ent 3 ret 6 lost 1 ever 10 home 1\n6 ent 2 ret 7 lost 1 ever 10 home 1\n7 ent 1 ret 9 lost 1 ever 11 home 1\n8 ent 2 ret 8 lost 1 ever 11 home 1\n9 ent 3 ret 7 lost 1 ever 11 home 1\n10 ent 2 ret 7 lost 2 ever 11 home 1\n{'ci': 33270, 'name': 'Vertical axis wind turbine', 't0': 2009}\n0 ent 1 ret 1 lost 0 ever 2 home 1\n1 ent 0 ret 2 lost 0 ever 2 home 1\n2 ent 0 ret 2 lost 0 ever 2 home 1\n3 ent 2 ret 2 lost 0 ever 4 home 1\n4 ent 2 ret 2 lost 0 ever 4 home 1\n5 ent 4 ret 2 lost 0 ever 6 home 1\n6 ent 2 ret 3 lost 1 ever 6 home 1\n7 ent 1 ret 4 lost 1 ever 6 home 1\n8 ent 0 ret 4 lost 2 ever 6 home 1\n9 ent 1 ret 4 lost 2 ever 7 home 1\n10 ent 3 ret 4 lost 1 ever 8 home 1\n36:E6 = Path(os.environ.get(\"AII_EXP6_DIR\", RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"))  # art_N-mpomDZZ1ln\n38:E8 = Path(os.environ.get(\"AII_EXP8_DIR\", RUN_ROOT / \"3_invention_loop/iter_3/gen_art/gen_art_experiment_8\"))  # art_dFQ6jbgNsR6Q\n40:E8_DATA = E8 / \"data\"\n41:E8_INPUTS = E8 / \"inputs\"", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] ASSISTANT · 2026-09-29 20:06:19 UTC

```
The yearly states match `pair.json` exactly: GPU E2=7, EH=11, Bn=8 and wind turbine E2=2, EH=6, Bn=4. Now the generator's `network` type, and whether I can recompute the W3 ego network.
```

### [33] TOOL CALL — Bash · 2026-09-29 20:06:19 UTC

```
Show network/step examples and ego code imports:
G=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_gen.py; python $G --example network; python $G --example step | head -40; W=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12; grep -n "import\|def concept_open" $W/lib/ego_open.py $W/lib/ego.py | head -30; which uv
```

### [34] TOOL RESULT — Bash · 2026-09-29 20:06:21 UTC

```
{"stdout": "{\n  \"type\": \"network\",\n  \"title\": \"Which agents exchanged messages, and how often\",\n  \"nodes\": [\n    {\n      \"label\": \"Planner\",\n      \"value\": 9,\n      \"group\": \"Control\"\n    },\n    {\n      \"label\": \"Router\",\n      \"value\": 7,\n      \"group\": \"Control\"\n    },\n    {\n      \"label\": \"Retriever\",\n      \"value\": 6,\n      \"group\": \"Tools\"\n    },\n    {\n      \"label\": \"Coder\",\n      \"value\": 8,\n      \"group\": \"Tools\"\n    },\n    {\n      \"label\": \"Executor\",\n      \"value\": 5,\n      \"group\": \"Tools\"\n    },\n    {\n      \"label\": \"Critic\",\n      \"value\": 6,\n      \"group\": \"Review\"\n    },\n    {\n      \"label\": \"Verifier\",\n      \"value\": 4,\n      \"group\": \"Review\"\n    },\n    {\n      \"label\": \"Writer\",\n      \"value\": 5,\n      \"group\": \"Review\"\n    }\n  ],\n  \"edges\": [\n    {\n      \"source\": \"Planner\",\n      \"target\": \"Router\",\n      \"weight\": 42\n    },\n    {\n      \"source\": \"Router\",\n      \"target\": \"Retriever\",\n      \"weight\": 31\n    },\n    {\n      \"source\": \"Router\",\n      \"target\": \"Coder\",\n      \"weight\": 28\n    },\n    {\n      \"source\": \"Coder\",\n      \"target\": \"Executor\",\n      \"weight\": 36\n    },\n    {\n      \"source\": \"Executor\",\n      \"target\": \"Critic\",\n      \"weight\": 22\n    },\n    {\n      \"source\": \"Retriever\",\n      \"target\": \"Critic\",\n      \"weight\": 14\n    },\n    {\n      \"source\": \"Critic\",\n      \"target\": \"Verifier\",\n      \"weight\": 19\n    },\n    {\n      \"source\": \"Verifier\",\n      \"target\": \"Writer\",\n      \"weight\": 11\n    },\n    {\n      \"source\": \"Critic\",\n      \"target\": \"Planner\",\n      \"weight\": 9\n    },\n    {\n      \"source\": \"Writer\",\n      \"target\": \"Planner\",\n      \"weight\": 6\n    }\n  ],\n  \"directed\": true\n}\n{\n  \"type\": \"step\",\n  \"title\": \"Learning-rate schedule\",\n  \"xlabel\": \"Training step\",\n  \"ylabel\": \"Learning rate\",\n  \"logy\": true,\n  \"aspect\": \"16:9\",\n  \"where\": \"post\",\n  \"series\": [\n    {\n      \"label\": \"warmup then step decay\",\n      \"x\": [\n        0,\n        500,\n        1000,\n        5000,\n        10000,\n        20000,\n        40000\n      ],\n      \"values\": [\n        1e-05,\n        0.0003,\n        0.0003,\n        0.00024,\n        0.00015,\n        6e-05,\n        1e-05\n      ]\n    }\n  ]\n}\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:6:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:8:import warnings\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:9:from collections import Counter\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:11:import numpy as np\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:13:import ego\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:14:from ego import C, bg_window, neighbours, rq1_windows, self_topics, slice_of, window_counts\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py:19:def concept_open(name: str, aliases: list[str], t0: int, works, windows=rq1_windows, nb_min_w: int = 2,\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:12:from __future__ import annotations\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:14:import math\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:15:import warnings\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:16:from collections import Counter\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:18:import igraph as ig\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:19:import numpy as np\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego.py:46:    from scipy.special import gammaln\n/usr/bin/uv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] ASSISTANT · 2026-09-29 20:06:29 UTC

```
Recomputing the ego network needs `igraph` and `snowballstemmer`. I'll create a small venv in the workspace and check the size of the background-topic inputs.
```

### [36] TOOL CALL — Bash · 2026-09-29 20:06:29 UTC

```
Create venv and inspect ego-network input sizes:
uv venv -q .venv --python 3.12 && uv pip install -q --python .venv/bin/python numpy pandas pyarrow scipy python-igraph snowballstemmer networkx matplotlib 2>&1 | tail -3; E8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls -la $E8/data/bg_topics.npz $E8/inputs/backbone/ $E8/data/frame_matches_early/ ; du -sh .venv
```

### [37] TOOL RESULT — Bash · 2026-09-29 20:11:31 UTC

```
{"stdout": "-rw-rw-rw- 1 aii-agent aii-agent  298030 Sep 28 23:17 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/bg_topics.npz\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/frame_matches_early/:\ntotal 30774\ndrwxrwxrwx 2 aii-agent aii-agent  2002622 Sep 28 23:17 .\ndrwxrwxrwx 6 aii-agent aii-agent  2007277 Sep 29 00:35 ..\n-rw-rw-rw- 1 aii-agent aii-agent 27501352 Sep 28 23:17 part_001.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/inputs/backbone/:\ntotal 11688\ndrwxrwxrwx 2 aii-agent aii-agent 2000759 Sep 28 22:05 .\ndrwxrwxrwx 3 aii-agent aii-agent 2002001 Sep 28 22:05 ..\n-rw-rw-rw- 1 aii-agent aii-agent 2386351 Sep 28 22:05 slice0.npz\n-rw-rw-rw- 1 aii-agent aii-agent 2682026 Sep 28 22:05 slice1.npz\n-rw-rw-rw- 1 aii-agent aii-agent 2896133 Sep 28 22:05 slice2.npz\n1.1G\t.venv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] ASSISTANT · 2026-09-29 20:12:41 UTC

```
Now an extraction script that calls Exp12's own ego code (read-only import) and writes the plotted numbers to JSON.
```

### [39] TOOL CALL — Write · 2026-09-29 20:12:41 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/extract_case_pair.py

#!/usr/bin/env python3
"""Extract the numbers behind fig_case_study (Experiment 12, case pair 1) from the artifact's own outputs.

Timeline: per-age off-home field states from EXP12 data/state_codes.npy (codes 0 untouched, 1 entered,
2 retained, 3 lost, 4 home), exactly the array s8_cases.py plotted in case_studies/pair01_CSEng/flow_raster.
Ego network: the W3 (t0..t0+2) all-papers topic co-occurrence ego network, recomputed with EXP12's own
lib/ego_open.concept_open (read-only import) on the EXP8 early matches; node colour = EXP3 Leiden community of
the backbone slice for t0+2, as in case_studies/pair01_CSEng/ego_snapshots. Node/edge/community counts are
checked against pair.json's ego_snapshot_stats before anything is written.
Writes case_pair_data.json (plain numbers only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop")
E12 = RUN / "iter_4/gen_art/gen_art_experiment_12"
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"
E6 = RUN / "iter_2/gen_art/gen_art_experiment_6"
OUT = Path(__file__).resolve().parent / "case_pair_data.json"
sys.path.insert(0, str(E12 / "lib"))

HORIZON = 8  # the draft specifies t0 .. t0+8 (the decomposition's Bn horizon)


def main() -> None:
    import ego
    import ego_open
    from ego_ctx import rq1_context

    pair = json.loads((E12 / "case_studies/pair01_CSEng/pair.json").read_text())
    J = pd.read_parquet(E12 / "data/joined.parquet")
    pos = {c: i for i, c in enumerate(J.ci)}
    codes = np.load(E12 / "data/state_codes.npy", mmap_mode="r")
    fields = json.loads((E6 / "inputs/field_backbone.json").read_text())["fields"]
    ctx = rq1_context()
    ego_open.set_context(ctx)
    em = pd.read_parquet(E8 / "data/frame_matches_early/part_001.parquet", columns=["ci", "year", "vfield", "topics"])

    out = {"source": {"pair": str(E12.name) + "/case_studies/pair01_CSEng/pair.json",
                      "states": "data/state_codes.npy", "ego": "lib/ego_open.concept_open W3, all papers"},
           "members": {}}
    for role in ("HIGH_OPEN", "LOW_OPEN"):
        m = pair["members"][role]
        ci, t0 = int(m["ci"]), int(m["t0"])
        row = J.iloc[pos[ci]]
        assert row["name"] == m["name"], (row["name"], m["name"])
        cc = np.asarray(codes[pos[ci]])[: HORIZON + 1]
        ever = np.isin(cc, [1, 2, 3])
        first = {}
        for f in range(cc.shape[1]):
            hit = np.flatnonzero(ever[:, f])
            if hit.size:
                first[fields[f]] = int(hit[0])
        timeline = {"age": list(range(HORIZON + 1)),
                    "ever_entered": [int(ever[a].sum()) for a in range(HORIZON + 1)],
                    "retained": [int((cc[a] == 2).sum()) for a in range(HORIZON + 1)],
                    "lost": [int((cc[a] == 3).sum()) for a in range(HORIZON + 1)],
                    "home": [fields[f] for f in range(cc.shape[1]) if (cc[:, f] == 4).any()],
                    "first_entry_age": dict(sorted(first.items(), key=lambda kv: (kv[1], kv[0])))}
        dec = m["decomposition"]
        assert timeline["ever_entered"][2] == dec["E2"], "E2 mismatch"
        assert timeline["ever_entered"][HORIZON] == dec["EH"], "EH mismatch"
        assert timeline["retained"][HORIZON] == dec["Bn"], "Bn mismatch"

        home = [int(h) for h in str(row.home_list).split(";")]
        d = em[em.ci == ci]
        works = list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))
        s = ego_open.concept_open(str(row["name"]), [], t0, works, keep_nb=True)
        nb = [int(v) for v in s["_nb"]["W3"]]
        sl = ego.slice_of(t0 + 2)
        a, b = ctx["full_edges"][sl]
        comm = ctx["comm"][sl]
        ins = np.zeros(ctx["nt"], bool)
        ins[nb] = True
        msk = ins[a] & ins[b]
        edges = sorted({(int(min(x, y)), int(max(x, y))) for x, y in zip(a[msk], b[msk]) if x != y})
        stats = m["ego_snapshot_stats"][f"{role}_W3_all"]
        ncomm = len({int(comm[v]) for v in nb})
        assert (len(nb), len(edges), ncomm) == (stats["n_nodes"], stats["n_edges"], stats["n_communities"]), \
            (role, len(nb), len(edges), ncomm, stats)
        cnt = s["_cnt"]["W3"]
        out["members"][role] = {
            "name": m["name"], "t0": t0, "home_field_ids": home, "timeline": timeline,
            "decomposition": dec, "OPEN_all": m["OPEN"]["all"], "O2r_resid": m["outcomes_shown_after_selection"]["O2r_resid"],
            "ego_W3": {"window": f"{t0}-{t0 + 2}", "n_nodes": len(nb), "n_edges": len(edges),
                       "n_communities": ncomm, "density": stats["density"],
                       "nodes": [{"id": v, "topic": ctx["names"][v], "community": int(comm[v]),
                                  "count": float(cnt[v])} for v in nb],
                       "edges": edges}}
        print(role, m["name"], timeline["ever_entered"], timeline["retained"], len(nb), len(edges), ncomm)
    OUT.write_text(json.dumps(out, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
```

### [40] TOOL RESULT — Write · 2026-09-29 20:12:41 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/extract_case_pair.py", "content": "#!/usr/bin/env python3\n\"\"\"Extract the numbers behind fig_case_study (Experiment 12, case pair 1) from the artifact's own outputs.\n\nTimeline: per-age off-home field states from EXP12 data/state_codes.npy (codes 0 untouched, 1 entered,\n2 retained, 3 lost, 4 home), exactly the array s8_cases.py plotted in case_studies/pair01_CSEng/flow_raster.\nEgo network: the W3 (t0..t0+2) all-papers topic co-occurrence ego network, recomputed with EXP12's own\nlib/ego_open.concept_open (read-only import) on the EXP8 early matches; node colour = EXP3 Leiden community of\nthe backbone slice for t0+2, as in case_studies/pair01_CSEng/ego_snapshots. Node/edge/community counts are\nchecked against pair.json's ego_snapshot_stats before anything is written.\nWrites case_pair_data.json (plain numbers only).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop\")\nE12 = RUN / \"iter_4/gen_art/gen_art_experiment_12\"\nE8 = RUN / \"iter_3/gen_art/gen_art_experiment_8\"\nE6 = RUN / \"iter_2/gen_art/gen_art_experiment_6\"\nOUT = Path(__file__).resolve().parent / \"case_pair_data.json\"\nsys.path.insert(0, str(E12 / \"lib\"))\n\nHORIZON = 8  # the draft specifies t0 .. t0+8 (the decomposition's Bn horizon)\n\n\ndef main() -> None:\n    import ego\n    import ego_open\n    from ego_ctx import rq1_context\n\n    pair = json.loads((E12 / \"case_studies/pair01_CSEng/pair.json\").read_text())\n    J = pd.read_parquet(E12 / \"data/joined.parquet\")\n    pos = {c: i for i, c in enumerate(J.ci)}\n    codes = np.load(E12 / \"data/state_codes.npy\", mmap_mode=\"r\")\n    fields = json.loads((E6 / \"inputs/field_backbone.json\").read_text())[\"fields\"]\n    ctx = rq1_context()\n    ego_open.set_context(ctx)\n    em = pd.read_parquet(E8 / \"data/frame_matches_early/part_001.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"topics\"])\n\n    out = {\"source\": {\"pair\": str(E12.name) + \"/case_studies/pair01_CSEng/pair.json\",\n                      \"states\": \"data/state_codes.npy\", \"ego\": \"lib/ego_open.concept_open W3, all papers\"},\n           \"members\": {}}\n    for role in (\"HIGH_OPEN\", \"LOW_OPEN\"):\n        m = pair[\"members\"][role]\n        ci, t0 = int(m[\"ci\"]), int(m[\"t0\"])\n        row = J.iloc[pos[ci]]\n        assert row[\"name\"] == m[\"name\"], (row[\"name\"], m[\"name\"])\n        cc = np.asarray(codes[pos[ci]])[: HORIZON + 1]\n        ever = np.isin(cc, [1, 2, 3])\n        first = {}\n        for f in range(cc.shape[1]):\n            hit = np.flatnonzero(ever[:, f])\n            if hit.size:\n                first[fields[f]] = int(hit[0])\n        timeline = {\"age\": list(range(HORIZON + 1)),\n                    \"ever_entered\": [int(ever[a].sum()) for a in range(HORIZON + 1)],\n                    \"retained\": [int((cc[a] == 2).sum()) for a in range(HORIZON + 1)],\n                    \"lost\": [int((cc[a] == 3).sum()) for a in range(HORIZON + 1)],\n                    \"home\": [fields[f] for f in range(cc.shape[1]) if (cc[:, f] == 4).any()],\n                    \"first_entry_age\": dict(sorted(first.items(), key=lambda kv: (kv[1], kv[0])))}\n        dec = m[\"decomposition\"]\n        assert timeline[\"ever_entered\"][2] == dec[\"E2\"], \"E2 mismatch\"\n        assert timeline[\"ever_entered\"][HORIZON] == dec[\"EH\"], \"EH mismatch\"\n        assert timeline[\"retained\"][HORIZON] == dec[\"Bn\"], \"Bn mismatch\"\n\n        home = [int(h) for h in str(row.home_list).split(\";\")]\n        d = em[em.ci == ci]\n        works = list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))\n        s = ego_open.concept_open(str(row[\"name\"]), [], t0, works, keep_nb=True)\n        nb = [int(v) for v in s[\"_nb\"][\"W3\"]]\n        sl = ego.slice_of(t0 + 2)\n        a, b = ctx[\"full_edges\"][sl]\n        comm = ctx[\"comm\"][sl]\n        ins = np.zeros(ctx[\"nt\"], bool)\n        ins[nb] = True\n        msk = ins[a] & ins[b]\n        edges = sorted({(int(min(x, y)), int(max(x, y))) for x, y in zip(a[msk], b[msk]) if x != y})\n        stats = m[\"ego_snapshot_stats\"][f\"{role}_W3_all\"]\n        ncomm = len({int(comm[v]) for v in nb})\n        assert (len(nb), len(edges), ncomm) == (stats[\"n_nodes\"], stats[\"n_edges\"], stats[\"n_communities\"]), \\\n            (role, len(nb), len(edges), ncomm, stats)\n        cnt = s[\"_cnt\"][\"W3\"]\n        out[\"members\"][role] = {\n            \"name\": m[\"name\"], \"t0\": t0, \"home_field_ids\": home, \"timeline\": timeline,\n            \"decomposition\": dec, \"OPEN_all\": m[\"OPEN\"][\"all\"], \"O2r_resid\": m[\"outcomes_shown_after_selection\"][\"O2r_resid\"],\n            \"ego_W3\": {\"window\": f\"{t0}-{t0 + 2}\", \"n_nodes\": len(nb), \"n_edges\": len(edges),\n                       \"n_communities\": ncomm, \"density\": stats[\"density\"],\n                       \"nodes\": [{\"id\": v, \"topic\": ctx[\"names\"][v], \"community\": int(comm[v]),\n                                  \"count\": float(cnt[v])} for v in nb],\n                       \"edges\": edges}}\n        print(role, m[\"name\"], timeline[\"ever_entered\"], timeline[\"retained\"], len(nb), len(edges), ncomm)\n    OUT.write_text(json.dumps(out, indent=1))\n    print(\"wrote\", OUT)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [41] TOOL CALL — Bash · 2026-09-29 20:12:41 UTC

```
Check concept_open signature and home_list source:
grep -n "def concept_open" -A12 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/ego_open.py; grep -n "home_list" /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/s8_cases.py | head -3
```

### [42] TOOL RESULT — Bash · 2026-09-29 20:12:41 UTC

```
{"stdout": "19:def concept_open(name: str, aliases: list[str], t0: int, works, windows=rq1_windows, nb_min_w: int = 2,\n20-                 keep_nb: bool = False) -> dict:\n21-    win = windows(t0)\n22-    early_years = sorted(set(win[\"W1\"] + win[\"W2\"] + win[\"W3\"]))\n23-    n_early, nc_early = window_counts(works, early_years)\n24-    SELF = self_topics(name, aliases, n_early, nc_early)\n25-    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}\n26-    for w, ys in win.items():\n27-        cnt[w], nc[w] = window_counts(works, ys)\n28-        bgw[w], NW[w] = bg_window(ys)\n29-    nbg_early, _ = bg_window(early_years)\n30-    for w in (\"W1\", \"W2\", \"W3\"):\n31-        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, nb_min_w)\n178:            home = [int(h) for h in str(r.home_list).split(\";\")]\n219:                \"home\": r.home_list, \"B5\": {c: float(r[c]) for c in (\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\")},", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Bash · 2026-09-29 20:13:13 UTC

```
Run extraction of case-pair numbers:
python -c "import pandas as pd;print('home_list' in pd.read_parquet('/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/data/joined.parquet').columns)"; mkdir -p logs; timeout 900 .venv/bin/python extract_case_pair.py 2>&1 | grep -v Warning | tail -15 | tee logs/extract.log
```

### [44] TOOL RESULT — Bash · 2026-09-29 20:14:05 UTC

```
{"stdout": "True\nHIGH_OPEN Graphics processing unit [3, 5, 7, 8, 9, 10, 10, 11, 11] [0, 1, 3, 5, 6, 6, 7, 9, 8] 34 166 8\nLOW_OPEN Vertical axis wind turbine [2, 2, 2, 4, 4, 6, 6, 6, 6] [1, 2, 2, 2, 2, 2, 3, 4, 4] 12 46 1\nwrote /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/case_pair_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] THINKING · 2026-09-29 20:14:39 UTC

```
All checks pass — recomputed W3 networks match pair.json (GPU: 34 nodes/166 edges/8 communities; wind turbine: 12/46/1). Next I'll check entry order and community sizes.
```

### [46] TOOL CALL — Bash · 2026-09-29 20:14:39 UTC

```
Inspect entry order and community counts:
python -c "
import json,collections
d=json.load(open('case_pair_data.json'))
for r,m in d['members'].items():
  t=m['timeline']; print(r, t['home'], t['first_entry_age'], t['lost'])
  e=m['ego_W3']; print(collections.Counter(n['community'] for n in e['nodes']))
  for n in sorted(e['nodes'],key=lambda n:-n['count'])[:8]: print('  ',n)
"
```

### [47] TOOL RESULT — Bash · 2026-09-29 20:14:39 UTC

```
{"stdout": "HIGH_OPEN ['Engineering'] {'Computer Science': 0, 'Physics and Astronomy': 0, 'Social Sciences': 0, 'Earth and Planetary Sciences': 1, 'Medicine': 1, 'Biochemistry, Genetics and Molecular Biology': 2, 'Mathematics': 2, 'Environmental Science': 3, 'Chemistry': 4, 'Neuroscience': 5, 'Materials Science': 7} [0, 0, 0, 0, 0, 1, 1, 1, 1]\nCounter({20: 11, 4: 10, 0: 5, 5: 3, 11: 2, 13: 1, 3: 1, 2: 1})\n   {'id': 53, 'topic': 'Parallel Computing and Optimization Techniques', 'community': 4, 'count': 6.0}\n   {'id': 521, 'topic': 'Medical Imaging Techniques and Applications', 'community': 0, 'count': 6.0}\n   {'id': 1568, 'topic': 'Optical Coherence Tomography Applications', 'community': 20, 'count': 5.0}\n   {'id': 43, 'topic': 'Protein Structure and Dynamics', 'community': 5, 'count': 4.0}\n   {'id': 480, 'topic': 'Computer Graphics and Visualization Techniques', 'community': 4, 'count': 4.0}\n   {'id': 539, 'topic': 'Advanced Fluorescence Microscopy Techniques', 'community': 20, 'count': 4.0}\n   {'id': 2014, 'topic': 'Photoacoustic and Ultrasonic Imaging', 'community': 20, 'count': 4.0}\n   {'id': 2548, 'topic': 'Image and Object Detection Techniques', 'community': 4, 'count': 4.0}\nLOW_OPEN ['Engineering'] {'Environmental Science': 0, 'Social Sciences': 0, 'Agricultural and Biological Sciences': 3, 'Physics and Astronomy': 3, 'Computer Science': 5, 'Materials Science': 5} [0, 0, 0, 0, 0, 0, 1, 1, 2]\nCounter({2: 12})\n   {'id': 2695, 'topic': 'Icing and De-icing Technologies', 'community': 2, 'count': 13.0}\n   {'id': 2080, 'topic': 'Aerodynamics and Fluid Dynamics Research', 'community': 2, 'count': 12.0}\n   {'id': 1253, 'topic': 'Fluid Dynamics and Vibration Analysis', 'community': 2, 'count': 11.0}\n   {'id': 739, 'topic': 'Wind Turbine Control Systems', 'community': 2, 'count': 6.0}\n   {'id': 2205, 'topic': 'Vibration and Dynamic Analysis', 'community': 2, 'count': 6.0}\n   {'id': 2717, 'topic': 'Aerospace Engineering and Energy Systems', 'community': 2, 'count': 6.0}\n   {'id': 3857, 'topic': 'Soil, Finite Element Methods', 'community': 2, 'count': 5.0}\n   {'id': 4151, 'topic': 'Engineering Applied Research', 'community': 2, 'count': 5.0}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] THINKING · 2026-09-29 20:15:17 UTC

```
I see 8 distinct Leiden community IDs across both panels (one shared), comparable since both concepts fall in the same 2010–14 backbone slice. Let me check if `topic_meta` provides descriptive field labels for these communities.
```

### [49] TOOL CALL — Bash · 2026-09-29 20:15:17 UTC

```
Characterise Leiden communities by topic field:
E8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; head -3 $E8/inputs/topic_meta.csv; cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4 && .venv/bin/python -c "
import json,numpy as np,pandas as pd,collections
E8='$E8'
tids=json.load(open(E8+'/inputs/topic_ids.json')); tm=pd.read_csv(E8+'/inputs/topic_meta.csv').set_index('topic').loc[tids]
z=np.load(E8+'/inputs/backbone/slice2.npz'); comm=z['comm']
print(tm.columns.tolist())
col='field' if 'field' in tm.columns else tm.columns[1]
for c in [20,4,0,5,11,13,3,2]:
  s=tm[col].to_numpy()[comm==c]; vc=collections.Counter(s).most_common(3); print(c,len(s),vc)
"
```

### [50] TOOL RESULT — Bash · 2026-09-29 20:15:53 UTC

```
{"stdout": "topic,name,subfield,subfield_name,field,field_name,keywords\n10001,Geological and Geochemical Analysis,1908,Geophysics,19,Earth and Planetary Sciences,Zircon; Geochronology; Tectonics; Granitic Rocks; Isotopic Composition; Subduction Zones; Mantle Evolution; Plate Tectonics; Thermodynamic Modeling; Continental Growth\n10002,Advanced Chemical Physics Studies,3107,\"Atomic and Molecular Physics, and Optics\",31,Physics and Astronomy,Density Functional Theory; Dispersion Correction; Ab Initio Parametrization; Wavefunction Analyzer; Semiempirical Methods; Van der Waals Interactions; Continuum Solvation Models; Hybrid Density Functionals; Molecular Simulations; Electronic Structure Calculations\n['name', 'subfield', 'subfield_name', 'field', 'field_name', 'keywords']\n20 261 [(np.int64(22), 106), (np.int64(31), 77), (np.int64(25), 57)]\n4 293 [(np.int64(17), 172), (np.int64(22), 86), (np.int64(33), 9)]\n0 435 [(np.int64(27), 375), (np.int64(13), 14), (np.int64(35), 13)]\n5 304 [(np.int64(13), 130), (np.int64(27), 123), (np.int64(28), 21)]\n11 106 [(np.int64(19), 41), (np.int64(23), 39), (np.int64(22), 8)]\n13 134 [(np.int64(26), 67), (np.int64(17), 23), (np.int64(31), 17)]\n3 270 [(np.int64(16), 88), (np.int64(25), 51), (np.int64(22), 49)]\n2 299 [(np.int64(22), 242), (np.int64(25), 12), (np.int64(21), 10)]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] THINKING · 2026-09-29 20:17:03 UTC

```
I'll label each community by its plurality OpenAlex field in the 2010–14 backbone slice, including a second field if it's at least 0.6× the top count, and add this logic to the extraction script for reproducibility.
```

### [52] TOOL CALL — Edit · 2026-09-29 20:17:03 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/extract_case_pair.py
OLD:         print(role, m["name"], timeline["ever_entered"], timeline["retained"], len(nb), len(edges), ncomm)
    OUT.write_text(json.dumps(out, indent=1))
NEW:         print(role, m["name"], timeline["ever_entered"], timeline["retained"], len(nb), len(edges), ncomm)
        out.setdefault("_slices", set()).add(sl)
    # Describe each Leiden community drawn by the OpenAlex field(s) of ALL its topics in that backbone slice:
    # the plurality field, plus the runner-up when it has >= 0.6x the plurality count.
    (sl,) = out.pop("_slices")
    tm = pd.read_csv(E8 / "inputs/topic_meta.csv").set_index("topic").loc[json.loads((E8 / "inputs/topic_ids.json").read_text())]
    fname = tm.field_name.to_numpy()
    comm = ctx["comm"][sl]
    used = sorted({n["community"] for m in out["members"].values() for n in m["ego_W3"]["nodes"]})
    labels = {}
    for c in used:
        vc = pd.Series(fname[comm == c]).value_counts()
        top = [vc.index[0]] + ([vc.index[1]] if len(vc) > 1 and vc.iloc[1] >= 0.6 * vc.iloc[0] else [])
        labels[str(c)] = {"fields": top, "n_topics": int(vc.sum()),
                          "field_counts": {k: int(v) for k, v in vc.head(3).items()}}
    out["community_labels"] = {"backbone_slice": int(sl), "rule": "plurality OpenAlex field of the community's topics "
                               "(+ runner-up if >= 0.6x plurality)", "communities": labels}
    OUT.write_text(json.dumps(out, indent=1))
```

### [53] TOOL RESULT — Edit · 2026-09-29 20:17:03 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/extract_case_pair.py", "oldString": "        print(role, m[\"name\"], timeline[\"ever_entered\"], timeline[\"retained\"], len(nb), len(edges), ncomm)\n    OUT.write_text(json.dumps(out, indent=1))", "newString": "        print(role, m[\"name\"], timeline[\"ever_entered\"], timeline[\"retained\"], len(nb), len(edges), ncomm)\n        out.setdefault(\"_slices\", set()).add(sl)\n    # Describe each Leiden community drawn by the OpenAlex field(s) of ALL its topics in that backbone slice:\n    # the plurality field, plus the runner-up when it has >= 0.6x the plurality count.\n    (sl,) = out.pop(\"_slices\")\n    tm = pd.read_csv(E8 / \"inputs/topic_meta.csv\").set_index(\"topic\").loc[json.loads((E8 / \"inputs/topic_ids.json\").read_text())]\n    fname = tm.field_name.to_numpy()\n    comm = ctx[\"comm\"][sl]\n    used = sorted({n[\"community\"] for m in out[\"members\"].values() for n in m[\"ego_W3\"][\"nodes\"]})\n    labels = {}\n    for c in used:\n        vc = pd.Series(fname[comm == c]).value_counts()\n        top = [vc.index[0]] + ([vc.index[1]] if len(vc) > 1 and vc.iloc[1] >= 0.6 * vc.iloc[0] else [])\n        labels[str(c)] = {\"fields\": top, \"n_topics\": int(vc.sum()),\n                          \"field_counts\": {k: int(v) for k, v in vc.head(3).items()}}\n    out[\"community_labels\"] = {\"backbone_slice\": int(sl), \"rule\": \"plurality OpenAlex field of the community's topics \"\n                               \"(+ runner-up if >= 0.6x plurality)\", \"communities\": labels}\n    OUT.write_text(json.dumps(out, indent=1))", "originalFile": "#!/usr/bin/env python3\n\"\"\"Extract the numbers behind fig_case_study (Experiment 12, case pair 1) from the artifact's own outputs.\n\nTimeline: per-age off-home field states from EXP12 data/state_codes.npy (codes 0 untouched, 1 entered,\n2 retained, 3 lost, 4 home), exactly the array s8_cases.py plotted in case_studies/pair01_CSEng/flow_raster.\nEgo network: the W3 (t0..t0+2) all-papers topic co-occurrence ego network, recomputed with EXP12's own\nlib/ego_open.concept_open (read-only import) on the EXP8 early matches; node colour = EXP3 Leiden community of\nthe backbone slice for t0+2, as in case_studies/pair01_CSEng/ego_snapshots. Node/edge/community counts are\nchecked against pair.json's ego_snapshot_stats before anything is written.\nWrites case_pair_data.json (plain numbers only).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\n\nRUN = Path(\"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop\")\nE12 = RUN / \"iter_4/gen_art/gen_art_experiment_12\"\nE8 = RUN / \"iter_3/gen_art/gen_art_experiment_8\"\nE6 = RUN / \"iter_2/gen_art/gen_art_experiment_6\"\nOUT = Path(__file__).resolve().parent / \"case_pair_data.json\"\nsys.path.insert(0, str(E12 / \"lib\"))\n\nHORIZON = 8  # the draft specifies t0 .. t0+8 (the decomposition's Bn horizon)\n\n\ndef main() -> None:\n    import ego\n    import ego_open\n    from ego_ctx import rq1_context\n\n    pair = json.loads((E12 / \"case_studies/pair01_CSEng/pair.json\").read_text())\n    J = pd.read_parquet(E12 / \"data/joined.parquet\")\n    pos = {c: i for i, c in enumerate(J.ci)}\n    codes = np.load(E12 / \"data/state_codes.npy\", mmap_mode=\"r\")\n    fields = json.loads((E6 / \"inputs/field_backbone.json\").read_text())[\"fields\"]\n    ctx = rq1_context()\n    ego_open.set_context(ctx)\n    em = pd.read_parquet(E8 / \"data/frame_matches_early/part_001.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"topics\"])\n\n    out = {\"source\": {\"pair\": str(E12.name) + \"/case_studies/pair01_CSEng/pair.json\",\n                      \"states\": \"data/state_codes.npy\", \"ego\": \"lib/ego_open.concept_open W3, all papers\"},\n           \"members\": {}}\n    for role in (\"HIGH_OPEN\", \"LOW_OPEN\"):\n        m = pair[\"members\"][role]\n        ci, t0 = int(m[\"ci\"]), int(m[\"t0\"])\n        row = J.iloc[pos[ci]]\n        assert row[\"name\"] == m[\"name\"], (row[\"name\"], m[\"name\"])\n        cc = np.asarray(codes[pos[ci]])[: HORIZON + 1]\n        ever = np.isin(cc, [1, 2, 3])\n        first = {}\n        for f in range(cc.shape[1]):\n            hit = np.flatnonzero(ever[:, f])\n            if hit.size:\n                first[fields[f]] = int(hit[0])\n        timeline = {\"age\": list(range(HORIZON + 1)),\n                    \"ever_entered\": [int(ever[a].sum()) for a in range(HORIZON + 1)],\n                    \"retained\": [int((cc[a] == 2).sum()) for a in range(HORIZON + 1)],\n                    \"lost\": [int((cc[a] == 3).sum()) for a in range(HORIZON + 1)],\n                    \"home\": [fields[f] for f in range(cc.shape[1]) if (cc[:, f] == 4).any()],\n                    \"first_entry_age\": dict(sorted(first.items(), key=lambda kv: (kv[1], kv[0])))}\n        dec = m[\"decomposition\"]\n        assert timeline[\"ever_entered\"][2] == dec[\"E2\"], \"E2 mismatch\"\n        assert timeline[\"ever_entered\"][HORIZON] == dec[\"EH\"], \"EH mismatch\"\n        assert timeline[\"retained\"][HORIZON] == dec[\"Bn\"], \"Bn mismatch\"\n\n        home = [int(h) for h in str(row.home_list).split(\";\")]\n        d = em[em.ci == ci]\n        works = list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))\n        s = ego_open.concept_open(str(row[\"name\"]), [], t0, works, keep_nb=True)\n        nb = [int(v) for v in s[\"_nb\"][\"W3\"]]\n        sl = ego.slice_of(t0 + 2)\n        a, b = ctx[\"full_edges\"][sl]\n        comm = ctx[\"comm\"][sl]\n        ins = np.zeros(ctx[\"nt\"], bool)\n        ins[nb] = True\n        msk = ins[a] & ins[b]\n        edges = sorted({(int(min(x, y)), int(max(x, y))) for x, y in zip(a[msk], b[msk]) if x != y})\n        stats = m[\"ego_snapshot_stats\"][f\"{role}_W3_all\"]\n        ncomm = len({int(comm[v]) for v in nb})\n        assert (len(nb), len(edges), ncomm) == (stats[\"n_nodes\"], stats[\"n_edges\"], stats[\"n_communities\"]), \\\n            (role, len(nb), len(edges), ncomm, stats)\n        cnt = s[\"_cnt\"][\"W3\"]\n        out[\"members\"][role] = {\n            \"name\": m[\"name\"], \"t0\": t0, \"home_field_ids\": home, \"timeline\": timeline,\n            \"decomposition\": dec, \"OPEN_all\": m[\"OPEN\"][\"all\"], \"O2r_resid\": m[\"outcomes_shown_after_selection\"][\"O2r_resid\"],\n            \"ego_W3\": {\"window\": f\"{t0}-{t0 + 2}\", \"n_nodes\": len(nb), \"n_edges\": len(edges),\n                       \"n_communities\": ncomm, \"density\": stats[\"density\"],\n                       \"nodes\": [{\"id\": v, \"topic\": ctx[\"names\"][v], \"community\": int(comm[v]),\n                                  \"count\": float(cnt[v])} for v in nb],\n                       \"edges\": edges}}\n        print(role, m[\"name\"], timeline[\"ever_entered\"], timeline[\"retained\"], len(nb), len(edges), ncomm)\n    OUT.write_text(json.dumps(out, indent=1))\n    print(\"wrote\", OUT)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [{"oldStart": 93, "oldLines": 6, "newStart": 93, "newLines": 22, "lines": ["                                   \"count\": float(cnt[v])} for v in nb],", "                        \"edges\": edges}}", "         print(role, m[\"name\"], timeline[\"ever_entered\"], timeline[\"retained\"], len(nb), len(edges), ncomm)", "+        out.setdefault(\"_slices\", set()).add(sl)", "+    # Describe each Leiden community drawn by the OpenAlex field(s) of ALL its topics in that backbone slice:", "+    # the plurality field, plus the runner-up when it has >= 0.6x the plurality count.", "+    (sl,) = out.pop(\"_slices\")", "+    tm = pd.read_csv(E8 / \"inputs/topic_meta.csv\").set_index(\"topic\").loc[json.loads((E8 / \"inputs/topic_ids.json\").read_text())]", "+    fname = tm.field_name.to_numpy()", "+    comm = ctx[\"comm\"][sl]", "+    used = sorted({n[\"community\"] for m in out[\"members\"].values() for n in m[\"ego_W3\"][\"nodes\"]})", "+    labels = {}", "+    for c in used:", "+        vc = pd.Series(fname[comm == c]).value_counts()", "+        top = [vc.index[0]] + ([vc.index[1]] if len(vc) > 1 and vc.iloc[1] >= 0.6 * vc.iloc[0] else [])", "+        labels[str(c)] = {\"fields\": top, \"n_topics\": int(vc.sum()),", "+                          \"field_counts\": {k: int(v) for k, v in vc.head(3).items()}}", "+    out[\"community_labels\"] = {\"backbone_slice\": int(sl), \"rule\": \"plurality OpenAlex field of the community's topics \"", "+                               \"(+ runner-up if >= 0.6x plurality)\", \"communities\": labels}", "     OUT.write_text(json.dumps(out, indent=1))", "     print(\"wrote\", OUT)", " "]}], "userModified": false, "replaceAll": false}
```

### [54] TOOL CALL — Bash · 2026-09-29 20:17:03 UTC

```
Re-run extraction with community labels:
cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4; timeout 900 .venv/bin/python extract_case_pair.py 2>&1 | grep -v Warning | tail -5 > logs/extract.log; cat logs/extract.log; python -c "
import json;print(json.dumps(json.load(open('case_pair_data.json'))['community_labels'],indent=0))"
```

### [55] TOOL RESULT — Bash · 2026-09-29 20:17:35 UTC

```
{"stdout": "HIGH_OPEN Graphics processing unit [3, 5, 7, 8, 9, 10, 10, 11, 11] [0, 1, 3, 5, 6, 6, 7, 9, 8] 34 166 8\nLOW_OPEN Vertical axis wind turbine [2, 2, 2, 4, 4, 6, 6, 6, 6] [1, 2, 2, 2, 2, 2, 3, 4, 4] 12 46 1\nwrote /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/case_pair_data.json\n{\n\"backbone_slice\": 2,\n\"rule\": \"plurality OpenAlex field of the community's topics (+ runner-up if >= 0.6x plurality)\",\n\"communities\": {\n\"0\": {\n\"fields\": [\n\"Medicine\"\n],\n\"n_topics\": 435,\n\"field_counts\": {\n\"Medicine\": 375,\n\"Biochemistry, Genetics and Molecular Biology\": 14,\n\"Dentistry\": 13\n}\n},\n\"2\": {\n\"fields\": [\n\"Engineering\"\n],\n\"n_topics\": 299,\n\"field_counts\": {\n\"Engineering\": 242,\n\"Materials Science\": 12,\n\"Energy\": 10\n}\n},\n\"3\": {\n\"fields\": [\n\"Chemistry\"\n],\n\"n_topics\": 270,\n\"field_counts\": {\n\"Chemistry\": 88,\n\"Materials Science\": 51,\n\"Engineering\": 49\n}\n},\n\"4\": {\n\"fields\": [\n\"Computer Science\"\n],\n\"n_topics\": 293,\n\"field_counts\": {\n\"Computer Science\": 172,\n\"Engineering\": 86,\n\"Social Sciences\": 9\n}\n},\n\"5\": {\n\"fields\": [\n\"Biochemistry, Genetics and Molecular Biology\",\n\"Medicine\"\n],\n\"n_topics\": 304,\n\"field_counts\": {\n\"Biochemistry, Genetics and Molecular Biology\": 130,\n\"Medicine\": 123,\n\"Neuroscience\": 21\n}\n},\n\"11\": {\n\"fields\": [\n\"Earth and Planetary Sciences\",\n\"Environmental Science\"\n],\n\"n_topics\": 106,\n\"field_counts\": {\n\"Earth and Planetary Sciences\": 41,\n\"Environmental Science\": 39,\n\"Engineering\": 8\n}\n},\n\"13\": {\n\"fields\": [\n\"Mathematics\"\n],\n\"n_topics\": 134,\n\"field_counts\": {\n\"Mathematics\": 67,\n\"Computer Science\": 23,\n\"Physics and Astronomy\": 17\n}\n},\n\"20\": {\n\"fields\": [\n\"Engineering\",\n\"Physics and Astronomy\"\n],\n\"n_topics\": 261,\n\"field_counts\": {\n\"Engineering\": 106,\n\"Physics and Astronomy\": 77,\n\"Materials Science\": 57\n}\n}\n}\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] THINKING · 2026-09-29 20:18:07 UTC

```
Since no existing generator can produce a cumulative timeline alongside two ego networks with 34 unnamed-topic nodes (the `network` type always labels nodes), I'll hand-write the figure using house-style passes, starting with the helper signatures.
```

### [57] TOOL CALL — Bash · 2026-09-29 20:18:07 UTC

```
Read house-style helper signatures:
S=/ai-inventor/.claude/skills/aii-data-fig-gen/scripts; grep -n "^def \(apply_house_style\|place_legend\|place_point_label\|fit_legends\|clear_legends_of_data\|fit_tick_labels\|fit_titles\|assert_legends_clear_of_data\|assert_series_are_distinguishable\|assert_axis_names_are_unique\|literal\|rasterize_dense_clouds\)" -A14 $S/chart_style.py | grep -v '^\s*$' | head -150; grep -n "^PALETTE" -A10 $S/chart_style.py
```

### [58] TOOL RESULT — Bash · 2026-09-29 20:18:41 UTC

```
{"stdout": "146:def apply_house_style(base_font_pt: int = BASE_FONT_PT, family: str | None = None) -> None:\n147-    \"\"\"Install the house style into matplotlib's global rcParams.\n148-\n149-    ``family`` puts one font ahead of the default stack — the escape hatch\n150-    for a script the default fonts do not cover (CJK, Devanagari, Thai).\n151-    Without it those figures cannot be produced at all, because the glyph\n152-    gate refuses to write a figure full of hollow boxes.\n153-\n154-    Call once before building a figure. Idempotent.\n155-    \"\"\"\n156-    plt.rcParams.update(\n157-        {\n158-            # -- typography ---------------------------------------------------\n159-            # The caption's typeface; see ``PAPER_FONT_FAMILY``. A script it\n160-            # lacks needs ``font_family`` on the spec to put a covering font\n--\n277:def literal(text) -> str:\n278-    \"\"\"User text, with ``$`` neutralised so matplotlib prints it verbatim.\n279-\n280-    A MATCHED PAIR of dollar signs is mathtext to matplotlib, so a title like\n281-    \"Cost $5 to $9 per run\" silently renders as \"Cost 5to9 per run\" with the\n282-    currency gone and the middle word italicised. A cost figure losing its\n283-    currency symbols is precisely the kind of quiet corruption this renderer\n284-    is built to refuse, and unlike a bad number it survives review because\n285-    the sentence still reads.\n286-\n287-    Escaping rather than rejecting: a literal dollar is what a spec author\n288-    means essentially every time. The cost is that mathtext is unavailable —\n289-    use Unicode for superscripts (``R²``, ``10⁻³``), which the rest of this\n290-    module already does.\n291-\n--\n391:def rasterize_dense_clouds(fig) -> None:\n392-    \"\"\"Draw very dense point clouds as a bitmap, keeping everything else vector.\n393-\n394-    A scatter of 360,000 points writes every marker as its own path: 5.7 MB\n395-    for one figure, and a six-figure paper then does not fit inside a venue's\n396-    upload limit. Rasterizing the cloud alone is the standard answer — the\n397-    axes, ticks, labels and legend stay vector, so the text is still selectable\n398-    and sharp at any zoom, which is the whole reason the deliverable is a PDF.\n399-\n400-    Only ``Collection``s are touched. A dense LINE is already handled by\n401-    matplotlib's path simplification (120,000 points is 0.09 MB), so\n402-    rasterizing one would trade crispness for nothing.\n403-    \"\"\"\n404-    for ax in fig.axes:\n405-        for collection in ax.collections:\n--\n422:def fit_titles(fig) -> None:\n423-    \"\"\"Wrap any title wider than the axes it sits on, after layout.\n424-\n425-    Constrained layout reflows axes to fit their labels but cannot wrap a\n426-    single line, so a long title runs off the edge and loses its last words.\n427-\n428-    This has to run POST-LAYOUT and measure against the AXES, not the\n429-    figure. Two earlier attempts got that wrong and silently under-wrapped:\n430-    a characters-per-inch estimate (titles render a point larger than the\n431-    base size, and the average glyph is wider than half an em), then a\n432-    measurement against the figure width — but ``ax.set_title`` centres on\n433-    the axes, which is narrower than the figure by the y-label and tick\n434-    margins. A 6.0in title fits a 7in figure and still overflows a 5.6in\n435-    axes.\n436-    \"\"\"\n--\n691:def place_point_label(ax, text: str, xy, *, offset: tuple[float, float] = (5, 4), **kwargs):\n692-    \"\"\"Name a single plotted point, beside it, and record it for nudging.\n693-\n694-    Every renderer that writes a name next to a marker goes through here. The\n695-    offset it is given is a FIRST GUESS: whether the name lands on a\n696-    neighbouring point is a question about the drawn figure, and\n697-    ``fit_point_labels`` answers it after layout by trying the other corners.\n698-\n699-    ``volcano`` is why. It chooses which points to label by spacing the\n700-    LABELLED ones apart, which says nothing about the sixty it did not label —\n701-    so \"few-shot 3\" was printed with a data marker through the middle of the\n702-    word, at exit 0, and the text gate never saw it because a marker is not\n703-    text.\n704-    \"\"\"\n705-    figure = ax.figure\n--\n727:def place_legend(parent, *args, **kwargs):\n728-    \"\"\"Draw a legend and record the call, so ``fit_legends`` can reflow it.\n729-\n730-    Every legend in the catalogue goes through here, whether its parent is an\n731-    axes or the figure. The recording is what makes a reflow possible at all:\n732-    ``Legend.set_ncols`` stores the new column count and does NOT re-pack the\n733-    legend box, so calling it changes nothing a reader would ever see — a\n734-    four-entry legend measured 700 px before and 700 px after. Narrowing means\n735-    building the legend again, and that needs the arguments it was built with.\n736-    \"\"\"\n737-    legend = parent.legend(*args, **kwargs)\n738-    figure = parent if isinstance(parent, plt.Figure) else parent.figure\n739-    figure.aii_legends = [*getattr(figure, \"aii_legends\", []), (parent, args, kwargs, legend)]\n740-    return legend\n741-\n--\n764:def fit_legends(fig) -> None:\n765-    \"\"\"Reflow any legend that is wider than the space it has to sit in.\n766-\n767-    The column count is chosen before layout runs and whether it fits is only\n768-    knowable after. Three entries in one row measured 695 px on a 700 px\n769-    canvas, and constrained layout answers a legend wider than its axes by\n770-    shrinking the axes — on EVERY draw, without converging, so the figure\n771-    collapsed to nothing and was refused outright. Dropping a column at a time\n772-    until it fits leaves the axes stable instead.\n773-\n774-    A legend that has been re-parented with ``add_artist`` is left alone:\n775-    replaying ``ax.legend`` would overwrite whichever legend is currently the\n776-    axes' own, and ``bubble`` deliberately carries two — a colour key and a\n777-    size key. It keeps its columns; if it genuinely does not fit, the layout\n778-    gate refuses the figure with a message rather than shipping it.\n--\n858:def clear_legends_of_data(fig) -> None:\n859-    \"\"\"Move an inside legend that landed on the data out of the axes.\n860-\n861-    ``loc=\"best\"`` avoids the data only where free space exists. A horizontal\n862-    chart has none to buy: the y-headroom trick that clears a bar chart's\n863-    legend does nothing for a Gantt, whose rows are fixed and whose bars start\n864-    wherever the schedule says. ``timeline``'s legend covered 1,674 px of the\n865-    \"Paper writing\" bar — its LEFT END, so a reader could not see when the\n866-    task began — in the shipped catalogue example.\n867-\n868-    ``draw_legend`` already moves a legend out past six entries, or when the\n869-    plot area is full by construction. That is a guess made before layout; this\n870-    is the measurement after it, and it catches the cases the guess does not.\n871-    \"\"\"\n872-    fig.canvas.draw()\n--\n897:def assert_legends_clear_of_data(fig) -> None:\n898-    \"\"\"Refuse a figure whose legend is hiding the data it explains.\n899-\n900-    ``clear_legends_of_data`` moves a lone chart's legend below the axes, so\n901-    by the time this runs the only cases left are the ones nothing can move: a\n902-    PANEL cell has no strip of its own to move into, and its neighbours' cells\n903-    are not free space either.\n904-\n905-    That case was silent and it is not small. A ``timeline`` in a two-column\n906-    grid drew its five-entry legend over EIGHT OF ITS NINE BARS and exited 0,\n907-    and the ``bar`` cell beside it had its bar TOPS masked — GSM8K reading as\n908-    ~40 where the spec said 55.8.\n909-\n910-    The bar for refusing is deliberately higher than the bar for moving: a\n911-    legend clipping the corner of one bar costs a reader nothing, and refusing\n--\n977:def fit_tick_labels(fig) -> None:\n978-    \"\"\"Wrap, then tilt, then stand up any x tick labels that would collide.\n979-\n980-    This has to run POST-LAYOUT and measure the AXES. The rule it replaces\n981-    estimated a characters-per-slot budget from the FIGURE width, which is\n982-    right for a lone chart and wrong by the column count for every panel: in\n78:PALETTE: tuple[str, ...] = (\n79-    \"#0173B2\",  # blue\n80-    \"#DE8F05\",  # amber\n81-    \"#029E73\",  # green\n82-    \"#CC78BC\",  # violet\n83-    \"#CA9161\",  # tan\n84-    \"#949494\",  # grey\n85-    \"#ECE133\",  # yellow\n86-    \"#56B4E9\",  # sky\n87-)\n88-", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] ASSISTANT · 2026-09-29 20:19:15 UTC

```
Both concepts' numbers are extracted and verified. Next I'm writing the figure spec and a house-style renderer.
```

### [60] TOOL CALL — Bash · 2026-09-29 20:19:15 UTC

```
Build the figure spec JSON from extracted data:
cat > make_spec.py <<'EOF'
#!/usr/bin/env python3
"""Build fig_case_study_spec.json (every plotted number) from case_pair_data.json (extract_case_pair.py)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
d = json.loads((HERE / "case_pair_data.json").read_text())
SHORT = {"Biochemistry, Genetics and Molecular Biology": "Biochemistry", "Earth and Planetary Sciences": "Earth Sci.",
         "Environmental Science": "Environ. Sci.", "Physics and Astronomy": "Physics", "Computer Science": "Computer Sci."}
# Fixed colour per Leiden community (same ID -> same colour in both panels; both use backbone slice 2010-14).
COLOURS = {"2": "#0173B2", "20": "#DE8F05", "4": "#029E73", "0": "#CC78BC", "5": "#CA9161", "11": "#56B4E9",
           "13": "#ECE133", "3": "#949494"}
comms = d["community_labels"]["communities"]
spec = {
    "figure_id": "fig_case_study", "aspect": "21:9", "width_in": 6.5, "layout_seed": 0,
    "source": "EXP12 case pair 1 (results/case_pairs.json, case_studies/pair01_CSEng); extract_case_pair.py",
    "timeline": {"xlabel": "Years since onset t0", "ylabel": "Off-home venue fields (count)",
                 "series": []},
    "networks": [],
    "communities": [{"id": int(c), "label": " & ".join(SHORT.get(f, f) for f in comms[c]["fields"]),
                     "colour": COLOURS[c], "n_topics_in_backbone": comms[c]["n_topics"]}
                    for c in ["2", "20", "4", "0", "5", "11", "13", "3"]],
}
short_name = {"HIGH_OPEN": "GPU", "LOW_OPEN": "VAWT"}
style = {"HIGH_OPEN": ("#1a1a1a", "o"), "LOW_OPEN": ("#8a8a8a", "s")}
for role, m in d["members"].items():
    t = m["timeline"]
    col, mk = style[role]
    for key, ls, lab in (("ever_entered", "-", "ever entered"), ("retained", "--", "retained")):
        spec["timeline"]["series"].append({"label": f"{short_name[role]}, {lab}", "x": t["age"], "values": t[key],
                                           "colour": col, "marker": mk, "linestyle": ls})
    e = m["ego_W3"]
    spec["networks"].append({"role": role, "name": m["name"], "short": short_name[role], "t0": m["t0"],
                             "window": e["window"], "n_nodes": e["n_nodes"], "n_edges": e["n_edges"],
                             "n_communities": e["n_communities"], "density": round(e["density"], 2),
                             "OPEN_all": round(m["OPEN_all"], 2),
                             "nodes": [{"id": n["id"], "community": n["community"], "count": n["count"]} for n in e["nodes"]],
                             "edges": e["edges"]})
assert {n["community"] for net in spec["networks"] for n in net["nodes"]} == {c["id"] for c in spec["communities"]}
(HERE / "fig_case_study_spec.json").write_text(json.dumps(spec, indent=1))
print("ok")
EOF
python make_spec.py
```

### [61] TOOL RESULT — Bash · 2026-09-29 20:19:55 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [62] TOOL CALL — Write · 2026-09-29 20:20:33 UTC

```
File: /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/render_fig_case_study.py

#!/usr/bin/env python3
"""Render fig_case_study from fig_case_study_spec.json with the aii-data-fig-gen house style and layout passes.

(a) off-home venue fields ever entered / retained per year since onset, both concepts on one axis;
(b), (c) W3 (t0..t0+2) topic co-occurrence ego networks, node colour = Leiden community, area = W3 paper count.
Usage: .venv/bin/python render_fig_case_study.py --spec fig_case_study_spec.json --out fig_case_study_v0"""
from __future__ import annotations

import argparse
import json
import sys
import warnings
from pathlib import Path

SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts")
sys.path.insert(0, str(SKILL))

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

from chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402
from chart_style import (apply_house_style, assert_axis_names_are_unique, assert_legends_clear_of_data,  # noqa: E402
                         assert_series_are_distinguishable, clear_legends_of_data, fit_legends, fit_tick_labels,
                         fit_titles, literal, place_legend, rasterize_dense_clouds)


def timeline(ax, spec: dict) -> None:
    tl = spec["timeline"]
    for s in tl["series"]:
        ax.step(s["x"], s["values"], where="post", color=s["colour"], ls=s["linestyle"], lw=1.4,
                marker=s["marker"], ms=3.6, mfc=s["colour"] if s["linestyle"] == "-" else "white",
                mec=s["colour"], mew=1.0, label=literal(s["label"]))
    xs = tl["series"][0]["x"]
    ax.set_xlim(min(xs) - 0.3, max(xs) + 0.3)
    ax.set_xticks(xs)
    top = max(max(s["values"]) for s in tl["series"])
    ax.set_ylim(0, top + 5)
    ax.set_yticks(range(0, top + 5, 2))
    ax.set_xlabel(literal(tl["xlabel"]))
    ax.set_ylabel(literal(tl["ylabel"]))
    ax.set_title("Field entry over time", loc="left")
    place_legend(ax, loc="upper left", ncols=2, handlelength=2.2, columnspacing=0.8, frameon=False)


def ego(ax, net: dict, colour: dict, seed: int) -> None:
    ids = [n["id"] for n in net["nodes"]]
    G = nx.Graph()
    G.add_nodes_from(ids)
    G.add_edges_from(tuple(e) for e in net["edges"])
    assert G.number_of_nodes() == net["n_nodes"] and G.number_of_edges() == net["n_edges"]
    pos = nx.spring_layout(G, seed=seed, k=1.6 / np.sqrt(len(ids)), iterations=300)
    P = np.array([pos[v] for v in ids])
    P = (P - P.mean(0)) / np.abs(P - P.mean(0)).max()
    pos = {v: P[i] for i, v in enumerate(ids)}
    for a, b in G.edges:
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color="#9a9a9a", lw=0.35, alpha=0.55, zorder=1)
    cnt = np.array([n["count"] for n in net["nodes"]])
    ax.scatter(P[:, 0], P[:, 1], s=10 + 7 * cnt, c=[colour[n["community"]] for n in net["nodes"]],
               edgecolors="#333333", linewidths=0.4, zorder=2)
    ax.set_xlim(-1.18, 1.18)
    ax.set_ylim(-1.18, 1.18)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.grid(False)
    ax.set_title(literal(f"{net['name']}, t0 = {net['t0']}"), loc="left")
    ax.set_xlabel(literal(f"{net['n_nodes']} topics, {net['n_communities']} "
                          f"communit{'y' if net['n_communities'] == 1 else 'ies'}, density {net['density']:.2f}"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", default="fig_case_study_spec.json")
    ap.add_argument("--out", default="fig_case_study_v0")
    a = ap.parse_args()
    spec = json.loads(Path(a.spec).read_text())
    w = spec["width_in"]
    rw, rh = (float(x) for x in spec["aspect"].split(":"))
    apply_house_style()
    with warnings.catch_warnings(record=True):
        fig = plt.figure(figsize=(w, w * rh / rw), layout="constrained")
        gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1, 1])
        ax_t = fig.add_subplot(gs[0, 0])
        timeline(ax_t, spec)
        colour = {c["id"]: c["colour"] for c in spec["communities"]}
        net_axes = []
        for j, net in enumerate(spec["networks"]):
            ax = fig.add_subplot(gs[0, 1 + j])
            ego(ax, net, colour, spec["layout_seed"])
            net_axes.append(ax)
        for ax, letter in zip([ax_t, *net_axes], "abc"):
            ax.set_title(f"({letter}) " + ax.get_title(loc="left"), loc="left")
        handles = [Line2D([], [], ls="", marker="o", ms=5, mfc=c["colour"], mec="#333333", mew=0.4,
                          label=literal(c["label"])) for c in spec["communities"]]
        place_legend(fig, handles=handles, loc="outside lower right", ncols=4, frameon=False,
                     title="Leiden topic community (plurality OpenAlex field)", handletextpad=0.3,
                     columnspacing=1.0)
        fit_legends(fig)
        clear_legends_of_data(fig)
        fit_tick_labels(fig)
        fit_titles(fig)
        clear_legends_of_data(fig)
        fit_point_labels(fig)
        rasterize_dense_clouds(fig)
        assert_text_is_legible(fig)
        assert_legends_clear_of_data(fig)
        assert_series_are_distinguishable(fig)
        assert_axis_names_are_unique(fig)
        for ext in ("pdf", "png"):
            fig.savefig(f"{a.out}.{ext}", dpi=300 if ext == "png" else None)
    print("wrote", a.out)


if __name__ == "__main__":
    main()
```

### [63] TOOL CALL — Bash · 2026-09-29 20:20:33 UTC

```
Render figure (render 1):
.venv/bin/python render_fig_case_study.py 2>&1 | tail -15
```

### [64] TOOL RESULT — Write · 2026-09-29 20:20:33 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/render_fig_case_study.py", "content": "#!/usr/bin/env python3\n\"\"\"Render fig_case_study from fig_case_study_spec.json with the aii-data-fig-gen house style and layout passes.\n\n(a) off-home venue fields ever entered / retained per year since onset, both concepts on one axis;\n(b), (c) W3 (t0..t0+2) topic co-occurrence ego networks, node colour = Leiden community, area = W3 paper count.\nUsage: .venv/bin/python render_fig_case_study.py --spec fig_case_study_spec.json --out fig_case_study_v0\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport sys\nimport warnings\nfrom pathlib import Path\n\nSKILL = Path(\"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts\")\nsys.path.insert(0, str(SKILL))\n\nimport matplotlib  # noqa: E402\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt  # noqa: E402\nimport networkx as nx  # noqa: E402\nimport numpy as np  # noqa: E402\nfrom matplotlib.lines import Line2D  # noqa: E402\n\nfrom chart_geometry import assert_text_is_legible, fit_point_labels  # noqa: E402\nfrom chart_style import (apply_house_style, assert_axis_names_are_unique, assert_legends_clear_of_data,  # noqa: E402\n                         assert_series_are_distinguishable, clear_legends_of_data, fit_legends, fit_tick_labels,\n                         fit_titles, literal, place_legend, rasterize_dense_clouds)\n\n\ndef timeline(ax, spec: dict) -> None:\n    tl = spec[\"timeline\"]\n    for s in tl[\"series\"]:\n        ax.step(s[\"x\"], s[\"values\"], where=\"post\", color=s[\"colour\"], ls=s[\"linestyle\"], lw=1.4,\n                marker=s[\"marker\"], ms=3.6, mfc=s[\"colour\"] if s[\"linestyle\"] == \"-\" else \"white\",\n                mec=s[\"colour\"], mew=1.0, label=literal(s[\"label\"]))\n    xs = tl[\"series\"][0][\"x\"]\n    ax.set_xlim(min(xs) - 0.3, max(xs) + 0.3)\n    ax.set_xticks(xs)\n    top = max(max(s[\"values\"]) for s in tl[\"series\"])\n    ax.set_ylim(0, top + 5)\n    ax.set_yticks(range(0, top + 5, 2))\n    ax.set_xlabel(literal(tl[\"xlabel\"]))\n    ax.set_ylabel(literal(tl[\"ylabel\"]))\n    ax.set_title(\"Field entry over time\", loc=\"left\")\n    place_legend(ax, loc=\"upper left\", ncols=2, handlelength=2.2, columnspacing=0.8, frameon=False)\n\n\ndef ego(ax, net: dict, colour: dict, seed: int) -> None:\n    ids = [n[\"id\"] for n in net[\"nodes\"]]\n    G = nx.Graph()\n    G.add_nodes_from(ids)\n    G.add_edges_from(tuple(e) for e in net[\"edges\"])\n    assert G.number_of_nodes() == net[\"n_nodes\"] and G.number_of_edges() == net[\"n_edges\"]\n    pos = nx.spring_layout(G, seed=seed, k=1.6 / np.sqrt(len(ids)), iterations=300)\n    P = np.array([pos[v] for v in ids])\n    P = (P - P.mean(0)) / np.abs(P - P.mean(0)).max()\n    pos = {v: P[i] for i, v in enumerate(ids)}\n    for a, b in G.edges:\n        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=\"#9a9a9a\", lw=0.35, alpha=0.55, zorder=1)\n    cnt = np.array([n[\"count\"] for n in net[\"nodes\"]])\n    ax.scatter(P[:, 0], P[:, 1], s=10 + 7 * cnt, c=[colour[n[\"community\"]] for n in net[\"nodes\"]],\n               edgecolors=\"#333333\", linewidths=0.4, zorder=2)\n    ax.set_xlim(-1.18, 1.18)\n    ax.set_ylim(-1.18, 1.18)\n    ax.set_aspect(\"equal\")\n    ax.set_xticks([])\n    ax.set_yticks([])\n    for sp in ax.spines.values():\n        sp.set_visible(False)\n    ax.grid(False)\n    ax.set_title(literal(f\"{net['name']}, t0 = {net['t0']}\"), loc=\"left\")\n    ax.set_xlabel(literal(f\"{net['n_nodes']} topics, {net['n_communities']} \"\n                          f\"communit{'y' if net['n_communities'] == 1 else 'ies'}, density {net['density']:.2f}\"))\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--spec\", default=\"fig_case_study_spec.json\")\n    ap.add_argument(\"--out\", default=\"fig_case_study_v0\")\n    a = ap.parse_args()\n    spec = json.loads(Path(a.spec).read_text())\n    w = spec[\"width_in\"]\n    rw, rh = (float(x) for x in spec[\"aspect\"].split(\":\"))\n    apply_house_style()\n    with warnings.catch_warnings(record=True):\n        fig = plt.figure(figsize=(w, w * rh / rw), layout=\"constrained\")\n        gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 1, 1])\n        ax_t = fig.add_subplot(gs[0, 0])\n        timeline(ax_t, spec)\n        colour = {c[\"id\"]: c[\"colour\"] for c in spec[\"communities\"]}\n        net_axes = []\n        for j, net in enumerate(spec[\"networks\"]):\n            ax = fig.add_subplot(gs[0, 1 + j])\n            ego(ax, net, colour, spec[\"layout_seed\"])\n            net_axes.append(ax)\n        for ax, letter in zip([ax_t, *net_axes], \"abc\"):\n            ax.set_title(f\"({letter}) \" + ax.get_title(loc=\"left\"), loc=\"left\")\n        handles = [Line2D([], [], ls=\"\", marker=\"o\", ms=5, mfc=c[\"colour\"], mec=\"#333333\", mew=0.4,\n                          label=literal(c[\"label\"])) for c in spec[\"communities\"]]\n        place_legend(fig, handles=handles, loc=\"outside lower right\", ncols=4, frameon=False,\n                     title=\"Leiden topic community (plurality OpenAlex field)\", handletextpad=0.3,\n                     columnspacing=1.0)\n        fit_legends(fig)\n        clear_legends_of_data(fig)\n        fit_tick_labels(fig)\n        fit_titles(fig)\n        clear_legends_of_data(fig)\n        fit_point_labels(fig)\n        rasterize_dense_clouds(fig)\n        assert_text_is_legible(fig)\n        assert_legends_clear_of_data(fig)\n        assert_series_are_distinguishable(fig)\n        assert_axis_names_are_unique(fig)\n        for ext in (\"pdf\", \"png\"):\n            fig.savefig(f\"{a.out}.{ext}\", dpi=300 if ext == \"png\" else None)\n    print(\"wrote\", a.out)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [65] TOOL RESULT — Bash · 2026-09-29 20:21:11 UTC

```
{"stdout": "findfont: Failed to find font weight normal for CMU Serif, now using 500.\nfindfont: Failed to find font weight normal for CMU Serif, now using 500.\nfindfont: Failed to find font weight normal for CMU Serif, now using 500.\nfindfont: Failed to find font weight normal for CMU Serif, now using 500.\nTraceback (most recent call last):\n  File \"/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/render_fig_case_study.py\", line 122, in <module>\n    main()\n  File \"/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/render_fig_case_study.py\", line 112, in main\n    assert_text_is_legible(fig)\n  File \"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_geometry.py\", line 557, in assert_text_is_legible\n    raise RuntimeError(\nRuntimeError: 3 label(s) run off the edge of the figure — '(c) Vertical axis wind turbine, t0 = 2009' is only 52% visible, so the rest of it is cut off with no indication. Shorten the text, raise 'width_in', or choose an 'aspect' that gives that side more room.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [66] ASSISTANT · 2026-09-29 20:22:29 UTC

```
The layout gate refused render 1 because the panel titles are too long for the narrow network columns. I'll use short names with the OPEN label and a two-line stats line.
```

### [67] TOOL CALL — Bash · 2026-09-29 20:22:29 UTC

```
Shorten titles and re-render (render 2):
python - <<'EOF'
p='render_fig_case_study.py'; s=open(p).read()
s=s.replace('''ax.set_title(literal(f"{net['name']}, t0 = {net['t0']}"), loc="left")''','''ax.set_title(literal(f"{net['short']} ({net['open_label']})"), loc="left")''')
s=s.replace('''f"communit{'y' if net['n_communities'] == 1 else 'ies'}, density {net['density']:.2f}"))''','''f"communit{'y' if net['n_communities'] == 1 else 'ies'}\\ndensity {net['density']:.2f}"))''')
open(p,'w').write(s)
p='make_spec.py'; s=open(p).read()
s=s.replace('''"window": e["window"],''','''"window": e["window"], "open_label": "high OPEN" if role == "HIGH_OPEN" else "low OPEN",''')
open(p,'w').write(s)
EOF
python make_spec.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v findfont | tail -5
```

### [68] TOOL RESULT — Bash · 2026-09-29 20:23:09 UTC

```
{"stdout": "ok\n  File \"/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/render_fig_case_study.py\", line 112, in main\n    assert_text_is_legible(fig)\n  File \"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_geometry.py\", line 557, in assert_text_is_legible\n    raise RuntimeError(\nRuntimeError: 2 label(s) run off the edge of the figure — '(c) VAWT (low OPEN)' is only 91% visible, so the rest of it is cut off with no indication. Shorten the text, raise 'width_in', or choose an 'aspect' that gives that side more room.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [69] TOOL CALL — Bash · 2026-09-29 20:23:49 UTC

```
Let network axes fill cell width (render 3):
sed -i 's/    ax.set_aspect("equal")/    ax.set_aspect("equal", adjustable="datalim")/' render_fig_case_study.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v findfont | tail -4
```

### [70] TOOL RESULT — Bash · 2026-09-29 20:24:31 UTC

```
{"stdout": "    assert_text_is_legible(fig)\n  File \"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_geometry.py\", line 557, in assert_text_is_legible\n    raise RuntimeError(\nRuntimeError: 1 label(s) run off the edge of the figure — 'Off-home venue fields (count)' is only 97% visible, so the rest of it is cut off with no indication. Shorten the text, raise 'width_in', or choose an 'aspect' that gives that side more room.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [71] TOOL CALL — Bash · 2026-09-29 20:25:11 UTC

```
Shorten y-label and re-render (render 4):
sed -i 's/"Off-home venue fields (count)"/"Off-home fields (count)"/' make_spec.py && python make_spec.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v findfont | tail -3
```

### [72] TOOL RESULT — Bash · 2026-09-29 20:25:51 UTC

```
{"stdout": "ok\n  File \"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_style.py\", line 937, in assert_legends_clear_of_data\n    raise RuntimeError(\nRuntimeError: a legend is drawn over the data it explains: (a) Field entry over time has 3 of its shapes 67% behind its legend. The legend is opaque by design — it has to mask the gridline it lands on — so whatever is under it is gone, not merely faint. A lone chart's legend is moved below the axes automatically; a panel cell has nowhere to move it, so give that chart its own figure, use fewer columns so each cell has room, or drop the series that need naming.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [73] ASSISTANT · 2026-09-29 20:26:33 UTC

```
The two-column legend in panel (a) covers the early data. I'll label the concepts directly at the line ends and keep only a two-entry line-style key.
```

### [74] TOOL CALL — Bash · 2026-09-29 20:26:33 UTC

```
Direct-label concepts in timeline (render 5):
python - <<'EOF'
p='render_fig_case_study.py'; s=open(p).read()
old_start=s.index('def timeline(ax, spec: dict) -> None:'); old_end=s.index('def ego(')
new='''def timeline(ax, spec: dict) -> None:
    tl = spec["timeline"]
    for s in tl["series"]:
        ax.step(s["x"], s["values"], where="post", color=s["colour"], ls=s["linestyle"], lw=1.4,
                marker=s["marker"], ms=3.6, mfc=s["colour"] if s["linestyle"] == "-" else "white",
                mec=s["colour"], mew=1.0)
    xs = tl["series"][0]["x"]
    ax.set_xlim(min(xs) - 0.3, max(xs) + 1.9)
    ax.set_xticks(xs)
    top = max(max(s["values"]) for s in tl["series"])
    ax.set_ylim(0, top + 4)
    ax.set_yticks(range(0, top + 4, 2))
    ax.set_xlabel(literal(tl["xlabel"]))
    ax.set_ylabel(literal(tl["ylabel"]))
    ax.set_title("Field entry over time", loc="left")
    # concept named directly at the end of its ever-entered line; line style keyed in a two-entry legend
    for s in tl["series"]:
        if s["linestyle"] == "-":
            place_point_label(ax, literal(s["concept"]), (s["x"][-1], s["values"][-1]), offset=(6, -3),
                              color=s["colour"], fontsize=8.5)
    keys = [Line2D([], [], color="#555555", ls="-", marker="o", ms=3.6, mfc="#555555", label="ever entered"),
            Line2D([], [], color="#555555", ls="--", marker="o", ms=3.6, mfc="white", label="retained")]
    place_legend(ax, handles=keys, loc="upper left", frameon=False, handlelength=2.4)


'''
s=s[:old_start]+new+s[old_end:]
s=s.replace("from chart_style import (apply_house_style,","from chart_style import (apply_house_style, place_point_label,")
open(p,'w').write(s)
p='make_spec.py'; s=open(p).read()
s=s.replace('''"colour": col, "marker": mk, "linestyle": ls})''','''"colour": col, "marker": mk, "linestyle": ls, "concept": short_name[role]})''')
open(p,'w').write(s)
EOF
python make_spec.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v findfont | tail -3
```

### [75] TOOL RESULT — Bash · 2026-09-29 20:27:15 UTC

```
{"stdout": "ok\n  File \"/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_style.py\", line 1218, in assert_series_are_distinguishable\n    raise RuntimeError(\nRuntimeError: the legend gives 'Engineering' and 'Engineering & Physics' the same colour, dash pattern and marker, so a reader cannot tell them apart. The palette holds 8 colours and the dash patterns multiply that to 32 for line charts; past that, and past 8 for anything drawn as a solid shape, the styles repeat. Show fewer series — aggregate them, split them across panels, or draw the spread with 'box'/'violin'/'ridgeline' instead of one line each.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [76] TOOL CALL — Bash · 2026-09-29 20:28:01 UTC

```
Give community legend proxies real colours (render 6):
sed -i 's/handles = \[Line2D(\[\], \[\], ls="", marker="o", ms=5, mfc=c\["colour"\]/handles = [Line2D([], [], ls="", color=c["colour"], marker="o", ms=5, mfc=c["colour"]/' render_fig_case_study.py && grep -n 'handles = \[Line2D' render_fig_case_study.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v findfont | tail -3
```

### [77] TOOL RESULT — Bash · 2026-09-29 20:28:54 UTC

```
{"stdout": "107:        handles = [Line2D([], [], ls=\"\", color=c[\"colour\"], marker=\"o\", ms=5, mfc=c[\"colour\"], mec=\"#333333\", mew=0.4,\nIgnoring fixed y limits to fulfill fixed data aspect with adjustable data limits.\nIgnoring fixed y limits to fulfill fixed data aspect with adjustable data limits.\nwrote fig_case_study_v0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [78] TOOL CALL — Read · 2026-09-29 20:29:48 UTC

```
/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/fig_case_study_v0.png
```

### [79] TOOL RESULT — Read · 2026-09-29 20:29:48 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [80] THINKING · 2026-09-29 20:30:46 UTC

```
Render 6 passes all checks and matches the extracted data, but the VAWT end label is misaligned near GPU's line instead of its own. I'll fix this by vertically centering both labels just right of their respective line ends.
```

### [81] TOOL CALL — Bash · 2026-09-29 20:30:46 UTC

```
Re-anchor concept end labels (render 7):
sed -i 's/offset=(6, -3),/offset=(7, 0), va="center", ha="left",/' render_fig_case_study.py && .venv/bin/python render_fig_case_study.py 2>&1 | grep -v "findfont\|Ignoring" | tail -3
```

### [82] TOOL RESULT — Bash · 2026-09-29 20:31:42 UTC

```
{"stdout": "wrote fig_case_study_v0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [83] TOOL CALL — Read · 2026-09-29 20:32:38 UTC

```
/ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4/fig_case_study_v0.png
```

### [84] TOOL RESULT — Read · 2026-09-29 20:32:38 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [85] THINKING · 2026-09-29 20:33:26 UTC

```
Render 7 looks good, with node counts per color matching the data correctly, so I'll stop refining labels here. Next I'll check the PDF fonts and verify my imports didn't write `__pycache__` into the read-only Exp12 tree.
```

### [86] TOOL CALL — Bash · 2026-09-29 20:33:26 UTC

```
Check PDF fonts, sizes and stray caches:
ls -la fig_case_study_v0.* ; (pdffonts fig_case_study_v0.pdf 2>/dev/null || strings fig_case_study_v0.pdf | grep -i "FontFile\|Type3" | sort | uniq -c); ls -la --time-style=full-iso /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/__pycache__ 2>/dev/null | head; du -sh .venv; find . -name __pycache__ -not -path "./.venv/*"
```

### [87] TOOL RESULT — Bash · 2026-09-29 20:34:10 UTC

```
{"stdout": "-rw-rw-rw- 1 aii-agent aii-agent  33390 Sep 29 20:30 fig_case_study_v0.pdf\n-rw-rw-rw- 1 aii-agent aii-agent 320861 Sep 29 20:30 fig_case_study_v0.png\nname                                 type              encoding         emb sub uni object ID\n------------------------------------ ----------------- ---------------- --- --- --- ---------\nFQCBUM+CMUSerif-Roman                CID TrueType      Identity-H       yes yes yes     19  0\nBJONCV+CMUSerif-Roman                CID TrueType      Identity-H       yes yes yes     26  0\ntotal 2029\ndrwxrwxrwx 2 aii-agent aii-agent 1005342 2026-09-29 20:13:21.000000000 +0000 .\ndrwxrwxrwx 3 aii-agent aii-agent 1016302 2026-09-29 20:13:06.000000000 +0000 ..\n-rw-rw-rw- 1 aii-agent aii-agent   17767 2026-09-29 20:13:21.000000000 +0000 common.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent   25101 2026-09-29 20:13:06.000000000 +0000 ego.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent    4405 2026-09-29 20:13:21.000000000 +0000 ego_ctx.cpython-312.pyc\n-rw-rw-rw- 1 aii-agent aii-agent    7432 2026-09-29 20:13:21.000000000 +0000 ego_open.cpython-312.pyc\n1.3G\t.venv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [88] THINKING · 2026-09-29 20:34:56 UTC

```
My extraction run accidentally wrote a `lib/__pycache__` directory into the read-only Exp12 tree. I'll remove those four files and configure the script to skip bytecode writing.
```

### [89] TOOL CALL — Bash · 2026-09-29 20:34:56 UTC

```
Remove stray bytecode cache and prevent recurrence:
D=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_12/lib/__pycache__; rm -f $D/common.cpython-312.pyc $D/ego.cpython-312.pyc $D/ego_ctx.cpython-312.pyc $D/ego_open.cpython-312.pyc && rmdir $D && echo removed; cd /ai-inventor/aii_data/runs/run_DVtwwCx0JbFq/4_gen_paper_repo/_3_gen_viz/gen_viz_4 && sed -i 's/^sys.path.insert(0, str(E12 \/ "lib"))/sys.dont_write_bytecode = True  # never write __pycache__ into the read-only EXP12 tree\nsys.path.insert(0, str(E12 \/ "lib"))/' extract_case_pair.py && grep -n dont_write extract_case_pair.py; ls -la .aii
```

### [90] TOOL RESULT — Bash · 2026-09-29 20:35:42 UTC

```
{"stdout": "removed\n25:sys.dont_write_bytecode = True  # never write __pycache__ into the read-only EXP12 tree\ntotal 2000\ndrwxrwxrwx 2 aii-agent aii-agent       1 Sep 29 20:00 .\ndrwxrwxrwx 5 aii-agent aii-agent 2047025 Sep 29 20:34 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [91] ASSISTANT · 2026-09-29 20:36:26 UTC

```
Now the manifest, README and structured output.
```

### [92] TOOL CALL — Bash · 2026-09-29 20:36:26 UTC

````
Write manifest, restore script and README:
cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .venv/
    delete: regenerable
    source: "uv venv .venv --python 3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy python-igraph snowballstemmer networkx matplotlib"
EOF
cat > restore.sh <<'EOF'
#!/usr/bin/env bash
# Recreate the Python environment used by extract_case_pair.py and render_fig_case_study.py.
set -euo pipefail
cd "$(dirname "$0")"
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python numpy pandas pyarrow scipy python-igraph snowballstemmer networkx matplotlib
EOF
chmod +x restore.sh
cat > README.md <<'EOF'
# fig_case_study — matched case-study pair (Experiment 12, pair 1)

A data figure for the paper. It shows the matched case pair 1 from Experiment 12: *Graphics processing unit* (GPU), a
high-OPEN concept, against *Vertical axis wind turbine* (VAWT), a low-OPEN concept. Both come from the CS+Eng
reporting group, share the Engineering home field and are matched on early volume and growth. The pair is an
**illustration only (n = 1 pair)**, not evidence.

Produced on reduced hardware: a 2 vCPU / 8 GB RAM CPU pod with no GPU. That makes no difference to the output,
since the extraction reads cached outputs and draws a small figure.

## What the figure shows, and where each number comes from

- **(a)** Off-home venue fields each concept had *ever entered* (solid) and *retained* (dashed), by year since
  onset, from t0 to t0+8. The values come from Exp12 `data/state_codes.npy`, the array its `s8_cases.py` plotted in
  `case_studies/pair01_CSEng/flow_raster`. Three values are asserted against `pair.json`: ever entered at t0+2 equals
  E2 (7 vs 2), ever entered at t0+8 equals EH (11 vs 6), and retained at t0+8 equals Bn (8 vs 4).
- **(b, c)** The W3 topic co-occurrence ego network (papers from t0 to t0+2, all venues). It is recomputed with
  Exp12's own `lib/ego_open.concept_open` on the Exp8 early matches. Node colour is the Leiden community in the
  2010–14 backbone slice, and node area is the W3 paper count. The node, edge and community counts are asserted
  equal to `pair.json` `ego_snapshot_stats`: GPU has 34 nodes, 166 edges and 8 communities; VAWT has 12, 46 and 1.
  Each community is named by the plurality OpenAlex field of all its topics in that slice, plus the runner-up field
  when its count is at least 0.6× the plurality (`case_pair_data.json` → `community_labels`).

Corrections to the draft specification: the draft's "1→~12 vs 1→~3 fields", its "~15 partners in 4 clusters
(CS/Engineering/Medicine/Materials)" and its "~10 partners in 2 clusters (Engineering/Energy)" appear in no
results file. The figure plots the artifact's own numbers instead.

## Layout

| path | what |
|---|---|
| `fig_case_study_v0.pdf` | deliverable (vector, Type-42 fonts) |
| `fig_case_study_v0.png` | raster preview |
| `fig_case_study_spec.json` | the figure's source: every plotted number, label and colour |
| `case_pair_data.json` | extracted numbers with provenance (timelines, first-entry ages, ego nodes/edges, community labels) |
| `extract_case_pair.py` | reads the Exp12/Exp8/Exp6 run outputs (read-only) → `case_pair_data.json` |
| `make_spec.py` | `case_pair_data.json` → `fig_case_study_spec.json` |
| `render_fig_case_study.py` | spec → PDF/PNG with the aii-data-fig-gen house style and layout gates |
| `logs/extract.log` | extraction log |
| `restore.sh` | recreates `.venv/` |

## Run

```bash
./restore.sh
.venv/bin/python extract_case_pair.py      # needs the run_Id7TLZ6r1C7M invention-loop artifacts on disk
python make_spec.py
.venv/bin/python render_fig_case_study.py --spec fig_case_study_spec.json --out fig_case_study_v0
```

## Restoring removed files

`.venv/` (~1.3 GB, the Python environment) is marked `delete: regenerable`. To recreate it, run `./restore.sh`, or:

```bash
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python numpy pandas pyarrow scipy python-igraph snowballstemmer networkx matplotlib
```
EOF
ls
````

### [93] TOOL RESULT — Bash · 2026-09-29 20:37:16 UTC

```
{"stdout": "README.md\ncase_pair_data.json\nextract_case_pair.py\nfig_case_study_spec.json\nfig_case_study_v0.pdf\nfig_case_study_v0.png\nlogs\nmake_spec.py\nrender_fig_case_study.py\nrestore.sh", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [94] TOOL CALL — Bash · 2026-09-29 20:38:02 UTC

```
Write structured output JSON:
python - <<'EOF'
import json
caption = (r"Illustrative matched case-study pair from Experiment 12 (case pair 1 of 7): graphics processing unit (GPU; onset $t_0=2008$, high early-neighbourhood openness OPEN) "
 r"versus vertical-axis wind turbine (VAWT; $t_0=2009$, low OPEN). Both have an Engineering home field and are matched on early volume and growth. "
 r"(a) Number of off-home venue fields each concept has ever entered (solid line, filled markers) and currently retains (dashed line, open markers) in each year from $t_0$ to $t_0+8$; "
 r"GPU is shown in black and VAWT in grey on a shared axis. By $t_0+2$ GPU had entered 7 off-home fields and VAWT 2; by $t_0+8$ they had entered 11 and 6 and retained 8 and 4. "
 r"(b, c) Topic co-occurrence ego networks over the first three years ($t_0$ to $t_0+2$, all papers). The nodes are the concept's positive-PMI neighbour topics (the concept itself is not drawn), "
 r"the edges are links between those topics in the 2010--14 topic backbone, node area scales with the number of the concept's papers carrying the topic, "
 r"and colour gives the topic's Leiden community, named by the plurality OpenAlex field of its topics (plus the runner-up field when it has at least 0.6 times as many). "
 r"GPU's neighbourhood has 34 topics in 8 communities (density 0.30), led by Engineering \& Physics, Computer Science and Medicine communities. "
 r"VAWT's has 12 topics in a single Engineering community (density 0.70). "
 r"The pair illustrates the openness--breadth association and is not evidence for it (case\_pairs.json, pair 1).")
out = {
 "title": "Two matched concepts: open vs closed early network",
 "summary": (
  "Hand-written matplotlib figure using the aii-data-fig-gen house style and all of its layout and legibility gates, in a 21:9, 6.5-inch layout with three panels. "
  "No catalogue generator combines a timeline with community-coloured ego networks: the network type labels every node, which would clutter 34 unnamed topics. "
  "Every number comes from Experiment 12's own outputs for case pair 1 (Graphics processing unit vs Vertical axis wind turbine). "
  "(a) Off-home fields ever entered and retained per year from t0 to t0+8, taken from data/state_codes.npy. The values are GPU ever 3,5,7,8,9,10,10,11,11 and retained 0,1,3,5,6,6,7,9,8; "
  "VAWT ever 2,2,2,4,4,6,6,6,6 and retained 1,2,2,2,2,2,3,4,4. They are asserted equal to pair.json E2/EH/Bn (7/11/8 and 2/6/4). "
  "(b, c) W3 ego networks recomputed with Exp12's lib/ego_open.concept_open, asserted equal to pair.json: GPU 34 nodes, 166 edges, 8 communities, density 0.30; "
  "VAWT 12 nodes, 46 edges, 1 community, density 0.70. Each Leiden community is named from the OpenAlex fields of its topics. "
  "The draft specification's numbers ('1 to ~12' vs '1 to ~3' fields, '~15 partners in 4 clusters CS/Eng/Med/Materials', '~10 partners in 2 clusters Eng/Energy') "
  "appear in no results file, so they were NOT plotted. The figure shows the artifact's real values, and the caption was rewritten from the rendered image. "
  "Seven renders; the gates refused and fixed long titles running off the canvas, a clipped y-label, a legend covering data in (a) (replaced by direct end labels plus a line-style key), "
  "and identical community legend keys. Remaining minor flaw: the 'VAWT' end label sits slightly above its line end; its grey colour matches its own line. "
  "Produced on reduced hardware (2 vCPU, 8 GB RAM, no GPU), which does not affect the output. "
  "Files: fig_case_study_v0.pdf (deliverable), fig_case_study_v0.png, fig_case_study_spec.json (the figure's source), case_pair_data.json, extract_case_pair.py, make_spec.py, render_fig_case_study.py."),
 "caption": caption,
 "out_expected_files": {"image_path": "fig_case_study_v0.pdf"},
}
assert 500 <= len(out["summary"]) <= 5000 and len(out["caption"]) <= 2000, (len(out["summary"]), len(out["caption"]))
json.dump(out, open(".terminal_claude_agent_struct_out.json", "w"), indent=1)
print(len(out["summary"]), len(caption))
EOF
```

### [95] TOOL RESULT — Bash · 2026-09-29 20:38:48 UTC

```
{"stdout": "1966 1492", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [96] ASSISTANT · 2026-09-29 20:39:32 UTC

```
I rendered `fig_case_study_v0.pdf` from Experiment 12's own outputs. The figure does not show the draft's numbers, because most of them appear in no results file.

**What the data actually says, compared with the draft:**

| | Draft said | Experiment 12 files say |
|---|---|---|
| GPU fields entered | 1 → ~12 | ever entered 3 → 11, retained 8 by t0+8 |
| Wind turbine fields entered | 1 → ~3 | ever entered 2 → 6, retained 4 by t0+8 |
| GPU early network | ~15 partners in 4 clusters (CS, Engineering, Medicine, Materials) | 34 topics in 8 communities, density 0.30 |
| Wind turbine early network | ~10 partners in 2 clusters (Engineering, Energy) | 12 topics in 1 Engineering community, density 0.70 |

The draft's point still holds: GPU spreads into more fields and has a much more varied early neighbourhood.

**The figure** (21:9, three panels):
- **(a)** Off-home fields ever entered (solid) and retained (dashed) each year from t0 to t0+8. GPU is black, the wind turbine grey, on one shared axis.
- **(b, c)** Each concept's early topic network (first three years). Colour is the topic community, named by the most common OpenAlex field among its topics. Node size is how many of the concept's papers carry that topic.

**How the numbers were checked:** the yearly counts are read directly from Experiment 12's saved state array. I recomputed the networks with Experiment 12's own code. The script stops unless the fields entered by t0+2 and t0+8, the fields retained at t0+8, and the node, edge and community counts all match `pair.json`, and they all do. The caption was rewritten from the final image and calls the pair an illustration, not evidence.

**Things to know:**
- No catalogue chart type could combine a timeline with two community-coloured networks, so I wrote the plot by hand using the skill's house style and all its layout checks. It took 7 renders, and the final one passes every check.
- One small flaw remains: the "VAWT" label sits slightly above the end of its line. It is grey like its own line, so it still reads correctly.
- My first extraction run accidentally wrote a Python cache folder into Experiment 12's read-only directory. I deleted exactly the four files it created, and the script now can't do that again.
- The work ran on the smaller 2 vCPU / 8 GB machine; this doesn't affect the figure.
- The 1.3 GB `.venv/` is marked for deletion in `.aii/manifest.yaml`. `restore.sh` and the README explain how to rebuild it.

Files are in `gen_viz_4/`:
- `fig_case_study_v0.pdf` (the deliverable)
- `fig_case_study_v0.png`
- `fig_case_study_spec.json` (every plotted number)
- `case_pair_data.json`
- `extract_case_pair.py`
- `make_spec.py`
- `render_fig_case_study.py`
- `README.md`
- `.terminal_claude_agent_struct_out.json`
```
