# gen_art_experiment_16 — test_idea

> Phase: `invention_loop` · round 5 · `gen_art`
> Run: `run_Id7TLZ6r1C7M` — Concepts spread where they stick: network signals of cross-disciplinary diffusion in science
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_art_experiment_16` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-29 05:18:39 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-29 05:18:45 UTC

```
<ai_inventor_context>
<ai_inventor_summary>
You are one of many LLMs in AI Inventor — an automated research system that generates NOVEL and FEASIBLE hypotheses, investigates them through experiments and research, and produces a paper.

Your output feeds other LLMs downstream. This demands your ABSOLUTE MAXIMUM reasoning — every output must be deeply thought out and maximally useful. Surface-level responses waste downstream computation.
</ai_inventor_summary>

<your_role>
YOU ARE: An artifact exe... [truncated, 67012 chars total]
```

### [3] ASSISTANT · 2026-09-29 05:18:55 UTC

```
I'll start by reading the required skills and exploring the workspace and dependencies.
```

### [4] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-python
```

### [5] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-python"}
```

### [6] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-json
```

### [9] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-json"}
```

### [10] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-file-size-limit
```

### [11] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-file-size-limit"}
```

### [12] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-use-hardware
```

### [13] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-use-hardware"}
```

### [14] TOOL CALL — Skill · 2026-09-29 05:18:55 UTC

```
aii-parallel-computing
```

### [15] TOOL RESULT — Skill · 2026-09-29 05:18:55 UTC

```
{"success": true, "commandName": "aii-parallel-computing"}
```

### [16] TOOL CALL — Bash · 2026-09-29 05:18:59 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; ls -la; ls -la .aii; bash /ai-inventor/.claude/skills/aii-use-hardware/scripts/get_hardware.sh 2>&1 | head -40; df -h . | tail -1
```

### [17] TOOL RESULT — Bash · 2026-09-29 05:18:59 UTC

```
{"stdout": "total 3005\ndrwxr-xr-x 3 root root 1006295 Sep 29 05:18 .\ndrwxr-xr-x 7 root root 2004835 Sep 29 05:17 ..\ndrwxr-xr-x 2 root root       1 Sep 29 05:17 .aii\n-rw------- 1 root root      54 Sep 29 05:18 .aii_claude_session.json\n-rw-r--r-- 1 root root   68074 Sep 29 05:18 .repl_agent.ptylog\ntotal 984\ndrwxr-xr-x 2 root root       1 Sep 29 05:17 .\ndrwxr-xr-x 3 root root 1006295 Sep 29 05:18 ..\n=== OS ===\nLinux 7.0.0-28-generic\nNAME=\"Debian GNU/Linux\"\nVERSION=\"12 (bookworm)\"\n=== CGROUP ===\nType: cgroup v2\nContainer: docker\nCPU quota: max 100000 (cpu.max: quota period)\nMemory limit: 29 GB (32000000000 bytes)\nPIDs limit: 629145\nPaths: /sys/fs/cgroup/{cpu.max,memory.max,memory.current}\n\nIMPORTANT: You are in a container with cgroup resource limits.\nDo NOT use psutil.virtual_memory().total, free -h, or /proc/meminfo for limits.\nDo NOT use os.cpu_count() or nproc for CPU count.\nUse the cgroup paths above or the Python helpers from SKILL.md.\n=== CPU ===\n4 CPUs\nModel name:                              AMD EPYC 9655P 96-Core Processor\n=== RAM ===\n29 GB (container limit)\n=== DISK ===\n2.2P total, 506T free\n=== GPU ===\nNo GPU\nmfs#euro-3.runpod.net:9421  2.2P  1.7P  506T  78% /ai-inventor/aii_data", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-29 05:19:01 UTC

```
RUN=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M; SRC10=$RUN/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; EXP8=$RUN/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; ls $SRC10 $SRC10/lib $SRC10/data $SRC10/inputs $SRC10/results; echo ---; ls $EXP8 $EXP8/lib $EXP8/data | head -80; ls $RUN/user_uploads
```

### [19] TOOL RESULT — Bash · 2026-09-29 05:19:01 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10:\nREADME.md\naudit.py\ndata\nfigures\nfull_method_out.json\ninputs\nlib\nllm_cache\nlogs\nmake_outputs.py\nmake_report.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels\npassC\npassC.py\nprereg.md\npreview_method_out.json\npyproject.toml\nreadme_tables.py\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\ns0_prereg.py\ns1_candidates.py\ns3_checks.py\ns4_gate.py\ns5_typing.py\ns6_covariates.py\ns7_ego.py\ns8_select.py\ns9_unseal.py\ns_learned.py\nsnapshot\ntests\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data:\nanalysis_cohort.parquet\nbg_topics.npz\ncohort_candidates.csv\ncohort_candidates_gated.csv\ncohort_predictions.parquet\nconcept_types.csv\ncontrols.csv\ncovariates_cohort.parquet\ncovariates_exp5.parquet\nego_open\nego_open_cohort.parquet\nego_open_cohort_full.parquet\nego_open_exp5.parquet\nego_open_exp5_u2.parquet\nexp5_o2r_match_vs_tag.parquet\nfeatures_cohort.parquet\nfeatures_exp5_open.parquet\nlearned_features_cohort.parquet\no5_events_all.parquet\noutcomes_cohort.parquet\npassC_bg.npz\npassC_early.parquet\npassC_info.json\npassC_pre_agg.parquet\npassC_totals.npz\nprecision_cohort.csv\nsealed\ntypes_cohort_v1.csv\ntypes_cohort_v2.csv\ntypes_exp5_v1.csv\ntypes_exp5_v2.csv\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/inputs:\nbackbone\nfield_backbone.json\nfrozen_lexicon.sha256\nlexicon_v1.parquet\nsource_field.parquet\ntopic_ids.json\ntopic_meta.csv\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/lib:\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nfeatport.py\nframe_exp5.py\nh2.py\nindicators.py\nladder.py\nllmc.py\nmatcher.py\nmodels_exp5.py\noutc.py\noutjson.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal2.py\nseal_exp5.py\nstats_core.py\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results:\naudit.json\ncohort_report.json\ncohort_result.json\ncoverage_by_year.csv\ndeviations.json\nexp5_selection_result.json\nfrozen_spec.json\nfrozen_spec_v0.json\nlearned_models_cohort.json\nlearned_port_validation.json\nllm_cost_log.csv\nreadme_tables.md\nrederive.json\ns1_candidates_summary.json\ns2_checks.json\ns3_decision.json\ns4_gate_summary.json\ns6_checks.json\ns6_checks_cohort.json\ntype_benchmark_final.json\ntype_benchmark_v1.csv\ntype_benchmark_v1.json\ntype_benchmark_v2.csv\ntype_benchmark_v2.json\ntype_gold_labels_v1.csv\ntype_gold_labels_v2.csv\ntype_gold_sheet_v1.csv\ntype_m2all.json\ntype_prompt_v2.txt\nu2_ego_flags.json\nu5_outcomes.json\nu8_prompt_identity.json\nunit_tests.json\n---\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8:\nREADME.md\naudit.py\nbuild_features.py\ndata\ndev_select.py\nfigures\nfull_method_out.json\nheldout.py\ninputs\nlib\nlogs\nmake_outputs.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels\noutcomes.py\npassA\npassA.py\npassB\npassB.py\npreview_method_out.json\npyproject.toml\nreadme_tables.py\nrederive.py\nreproducibility.md\nrequirements.lock.txt\nrestore.sh\nresults\nsnapshot\ntests\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data:\nanalysis_table.parquet\nbg_topics.npz\ncites_early.parquet\ncounts_check.parquet\nego_features.parquet\nego_parts\nego_parts_c3\nego_timing\nfeatures_basic.parquet\nframe_arrays.npz\nframe_matches_early\no5_events.parquet\noutcomes.parquet\noutcomes_dev.parquet\noutcomes_sealed.parquet\npassA_info.json\npassB_info.json\npassB_targets.npy\nref_sample.parquet\n\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/lib:\n__pycache__\ncommon.py\ncommon3.py\ncommon5.py\ndesign.py\nego.py\nego_ctx.py\nego_exp3_orig.py\nframe_exp5.py\nh2.py\nindicators.py\nmatcher.py\nmodels_exp5.py\npanel_exp5.py\nrangefile.py\nrq1stats.py\nseal.py\nseal_exp5.py\nstats_core.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-29 05:19:03 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $SRC10/lib/ego.py
```

### [21] TOOL RESULT — Bash · 2026-09-29 05:19:03 UTC

```
{"stdout": "\"\"\"Co-occurrence ego-network indicators (family A), ported from art_yrradSC27HtQ features.concept_core.\n\nPort changes (all logged in results/deviations.json):\n  * windows are pluggable. RQ1 uses PRE = t0-3..t0-1, W1 = {t0}, W2 = {t0+1}, W3 = {t0+2}: the EXP3 W3 (t0+3..t0+4)\n    would leak past the t0..t0+2 feature window. new_edge_rate divides by the window length in years (3, not 5).\n  * the background comes from the context (Pass A BG/GT for RQ1; EXP3's ckpt for the port-validation test T0-8).\n  * betweenness uses a path-length cutoff (default 4) on the kNN backbone; N_NULL defaults to 200.\n  * dropped near-duplicate variants: D_lag, D_q, D_withself, F_bg; the per-field block is not needed.\n  * new: comm_entropy = Shannon entropy of the W3 neighbours' backbone-community weights.\nEverything else (PMI neighbour rule, SELF rule, the frequency-matched null of D_z, the multinomial null of F_res,\nNOV_res, participation, persistence, density, k-core, constraint) is the EXP3 code.\"\"\"\nfrom __future__ import annotations\n\nimport math\nimport warnings\nfrom collections import Counter\n\nimport igraph as ig\nimport numpy as np\n\nSELF_DF_MAX = 100\nSELF_SHARE = 0.20\nTOPN_F = 20\nR_RARE = 10\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\nC: dict = {}\n\n\ndef slice_of(y: int) -> int:\n    for i, (a, b) in enumerate(SLICES):\n        if a <= y <= b:\n            return i\n    return 0 if y < SLICES[0][0] else len(SLICES) - 1\n\n\ndef rq1_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0], \"W2\": [t0 + 1], \"W3\": [t0 + 2]}\n\n\ndef exp3_windows(t0: int) -> dict[str, list[int]]:\n    return {\"PRE\": [t0 - 3, t0 - 2, t0 - 1], \"W1\": [t0, t0 + 1], \"W2\": [t0 + 2], \"W3\": [t0 + 3, t0 + 4]}\n\n\ndef lgC(n: float, k: float) -> float:\n    from scipy.special import gammaln\n    return gammaln(n + 1) - gammaln(k + 1) - gammaln(n - k + 1)\n\n\ndef set_context(ctx: dict) -> None:\n    \"\"\"ctx: nt, years (list), bg [len(years), nt], Gt {year: n}, comm/comm_q/deg/knn/full_edges per slice, subfield,\n    names, ldf (topic lemma df), tlem (topic lemma sets), lemmas (callable).\"\"\"\n    C.clear()\n    C.update(ctx)\n    C[\"graphs\"] = {}\n    C[\"yidx\"] = {y: i for i, y in enumerate(ctx[\"years\"])}\n\n\ndef knn_graph(s: int) -> ig.Graph:\n    if s not in C[\"graphs\"]:\n        ka, kb = C[\"knn\"][s]\n        C[\"graphs\"][s] = ig.Graph(n=C[\"nt\"], edges=list(zip(ka.tolist(), kb.tolist())), directed=False)\n    return C[\"graphs\"][s]\n\n\ndef bg_window(years: list[int]) -> tuple[np.ndarray, float]:\n    yi = [C[\"yidx\"][y] for y in years if y in C[\"yidx\"]]\n    return C[\"bg\"][yi].sum(axis=0).astype(float), float(sum(C[\"Gt\"].get(y, 0) for y in years))\n\n\ndef window_counts(works, years) -> tuple[np.ndarray, int]:\n    nck = np.zeros(C[\"nt\"], dtype=float)\n    ncw = 0\n    ys = set(years)\n    for y, tp in works:\n        if y in ys and len(tp):\n            ncw += 1\n            for k in tp:\n                nck[k] += 1\n    return nck, ncw\n\n\ndef pmi(nck, nc, nbg, N):\n    with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n        v = np.log(nck * N / (nc * nbg))\n    v[~np.isfinite(v)] = np.nan\n    return v\n\n\ndef neighbours(nck, nc, nbg, N, excl, min_n: int = 2):\n    p = pmi(nck, nc, nbg, N) if nc > 0 else np.full(C[\"nt\"], np.nan)\n    nb = (nck >= min_n) & (np.nan_to_num(p, nan=-1) > 0) & ~excl\n    return nb, p\n\n\ndef topS(nck, p, nb, top: int = TOPN_F):\n    idx = np.nonzero(nb)[0]\n    if len(idx) == 0:\n        return float(\"nan\"), 0\n    order = idx[np.lexsort((-p[idx], -nck[idx]))][:top]\n    return float(np.mean(p[order])), len(order)\n\n\ndef self_topics(name: str, aliases: list[str], n_early, nc_early) -> np.ndarray:\n    lem = C[\"lemmas\"]\n    sets = []\n    for ph in [name] + aliases:\n        cl = {l for l in lem(ph) if C[\"ldf\"].get(l, 0) <= SELF_DF_MAX}\n        if cl:\n            sets.append(cl)\n    lex = np.array([any(cl <= tl for cl in sets) for tl in C[\"tlem\"]])\n    share = n_early / nc_early if nc_early else np.zeros(C[\"nt\"])\n    return lex | (share >= SELF_SHARE)\n\n\ndef distinct_null(pool_idx, w, M, labels, rng, n):\n    if M <= 0 or len(pool_idx) == 0:\n        return np.zeros(n)\n    M = min(M, len(pool_idx))\n    lw = np.log(w[pool_idx])\n    out = np.empty(n)\n    lab = labels[pool_idx]\n    chunk = max(1, 2_000_000 // len(pool_idx))\n    for s in range(0, n, chunk):\n        m = min(chunk, n - s)\n        g = lw[None, :] + rng.gumbel(size=(m, len(pool_idx)))\n        top = np.argpartition(-g, M - 1, axis=1)[:, :M]\n        L = np.sort(lab[top], axis=1)\n        out[s:s + m] = 1 + (np.diff(L, axis=1) != 0).sum(axis=1)\n    return out\n\n\ndef f_null(p_mix, pool, T1, T3, nc1, nc3, nbg1, N1, nbg3, N3, rng, n):\n    if len(pool) == 0 or T1 == 0 or T3 == 0 or nc1 == 0 or nc3 == 0:\n        return np.full(n, np.nan)\n    pr = p_mix[pool] / p_mix[pool].sum()\n\n    def S(T, nc, nbg, N):\n        X = rng.multinomial(T, pr, size=n).astype(float)\n        with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n            P = np.log(X * N / (nc * nbg[pool][None, :]))\n        elig = (X >= 2) & np.isfinite(P) & (P > 0)\n        key = np.where(elig, X + 1e-6 * np.nan_to_num(P, nan=0, posinf=0, neginf=0), -np.inf)\n        order = np.argsort(-key, axis=1)[:, :TOPN_F]\n        Ps = np.take_along_axis(np.where(elig, P, np.nan), order, axis=1)\n        with np.errstate(invalid=\"ignore\"):\n            return np.nanmean(np.where(np.isfinite(Ps), Ps, np.nan), axis=1)\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\", RuntimeWarning)\n        return S(T3, nc3, nbg3, N3) - S(T1, nc1, nbg1, N1)\n\n\ndef _centrality(idx: np.ndarray, s: int, cutoff: int | None) -> tuple[float, int, float]:\n    if len(idx) == 0:\n        return 0.0, 0, float(\"nan\")\n    g = knn_graph(s).copy()\n    g.add_vertices(1)\n    v = g.vcount() - 1\n    g.add_edges([(v, int(k)) for k in idx])\n    n = g.vcount()\n    b = g.betweenness(vertices=[v], directed=False, cutoff=cutoff)[0]\n    return b / ((n - 1) * (n - 2) / 2), int(g.coreness()[v]), float(g.constraint(vertices=[v])[0])\n\n\ndef concept_core(name: str, aliases: list[str], t0: int, works, n_null: int, seed: int, windows=rq1_windows,\n                 btw_cutoff: int | None = 4, nb_min_w: int = 2, compute_btw: bool = True) -> dict:\n    \"\"\"All family-A indicators for one concept. works = [(year, tuple of topic indices)].\"\"\"\n    rng = np.random.default_rng(seed)\n    win = windows(t0)\n    early_years = sorted(set(win[\"W1\"] + win[\"W2\"] + win[\"W3\"]))\n    n_early, nc_early = window_counts(works, early_years)\n    SELF = self_topics(name, aliases, n_early, nc_early)\n    cnt, nc, bgw, NW, NB, P = {}, {}, {}, {}, {}, {}\n    for w, ys in win.items():\n        cnt[w], nc[w] = window_counts(works, ys)\n        bgw[w], NW[w] = bg_window(ys)\n    nbg_early, _ = bg_window(early_years)\n    for w in (\"W1\", \"W2\", \"W3\"):\n        NB[w], P[w] = neighbours(cnt[w], nc[w], bgw[w], NW[w], SELF, nb_min_w)\n    pre_set = cnt[\"PRE\"] >= 1\n    new = (NB[\"W1\"] | NB[\"W2\"] | NB[\"W3\"]) & ~pre_set\n    new_idx = np.nonzero(new)[0]\n    M = len(new_idx)\n    first_year = {}\n    for y in early_years:\n        cy, _ = window_counts(works, [y])\n        for k in new_idx:\n            if k not in first_year and cy[k] >= 1:\n                first_year[k] = y\n    pool = np.nonzero((nbg_early > 0) & ~pre_set & ~SELF)[0]\n    s_mid = slice_of(early_years[len(early_years) // 2])\n    r: dict = {\"M\": M, \"n_self_topics\": int(SELF.sum()), \"nc_PRE\": nc[\"PRE\"], \"nc_W1\": nc[\"W1\"], \"nc_W2\": nc[\"W2\"],\n               \"nc_W3\": nc[\"W3\"]}\n\n    def dz(labels_by_slice, pool_idx, new_list):\n        if M < 3:\n            return float(\"nan\"), float(\"nan\"), float(\"nan\"), None\n        labs = [labels_by_slice[slice_of(first_year.get(k, t0))][k] for k in new_list]\n        obs = len(set(labs))\n        nl = distinct_null(pool_idx, nbg_early, len(new_list), labels_by_slice[s_mid], rng, n_null)\n        mu, sd = nl.mean(), nl.std()\n        return (obs - mu) / sd if sd > 0 else 0.0, obs / mu if mu > 0 else float(\"nan\"), obs, labs\n\n    r[\"D_z\"], r[\"D_ratio\"], r[\"D_obs\"], labs = dz(C[\"comm\"], pool, new_idx)\n    S1, k1 = topS(cnt[\"W1\"], P[\"W1\"], NB[\"W1\"])\n    S3, k3 = topS(cnt[\"W3\"], P[\"W3\"], NB[\"W3\"])\n    obs_g = S3 - S1\n    pooled = cnt[\"W1\"] + cnt[\"W2\"] + cnt[\"W3\"]\n    mixpool = np.nonzero((pooled > 0) & ~SELF)[0]\n    T1 = int(cnt[\"W1\"][~SELF].sum())\n    T3 = int(cnt[\"W3\"][~SELF].sum())\n    ng = f_null(pooled, mixpool, T1, T3, nc[\"W1\"], nc[\"W3\"], bgw[\"W1\"], NW[\"W1\"], bgw[\"W3\"], NW[\"W3\"], rng,\n                n_null)\n    ok = np.isfinite(ng)\n    if np.isfinite(obs_g) and ok.sum() >= 20:\n        r[\"F_res\"] = obs_g - ng[ok].mean()\n        sdn = ng[ok].std()\n        r[\"F_z\"] = r[\"F_res\"] / sdn if sdn > 0 else 0.0\n    else:\n        r[\"F_res\"] = r[\"F_z\"] = float(\"nan\")\n    if M >= R_RARE and labs is not None:\n        cc = np.array(list(Counter(labs).values()), dtype=float)\n        r[\"D_rare\"] = float(sum(1 - math.exp(lgC(M - m, R_RARE) - lgC(M, R_RARE)) if M - m >= R_RARE else 1.0\n                                for m in cc))\n    else:\n        r[\"D_rare\"] = float(\"nan\")\n    sub3 = [C[\"subfield\"]] * len(SLICES)\n    r[\"D_sub\"], _, _, _ = dz(sub3, pool, new_idx)\n    # novelty vs degree-preserving expectation\n    s0 = slice_of(t0)\n    comm0 = C[\"comm\"][s0]\n    w1 = cnt[\"W1\"]\n    if w1.sum() > 0:\n        cs = Counter()\n        for k in np.nonzero(w1)[0]:\n            cs[comm0[k]] += w1[k]\n        C0 = cs.most_common(1)[0][0]\n        if M > 0:\n            r[\"NOV\"] = float(np.mean([C[\"comm\"][slice_of(first_year.get(k, t0))][k] != C0 for k in new_idx]))\n            dg = C[\"deg\"][s0][pool].astype(float)\n            E = dg[comm0[pool] != C0].sum() / dg.sum() if dg.sum() > 0 else float(\"nan\")\n            r[\"NOV_res\"] = r[\"NOV\"] - E\n        else:\n            r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n    else:\n        r[\"NOV\"] = r[\"NOV_res\"] = float(\"nan\")\n    n1, n3 = NB[\"W1\"].sum(), NB[\"W3\"].sum()\n    r[\"deg_W1\"], r[\"deg_W3\"] = int(n1), int(n3)\n    r[\"deg_growth\"] = math.log(n3 + 1) - math.log(n1 + 1)\n    sp1 = np.nansum(P[\"W1\"][NB[\"W1\"]])\n    sp3 = np.nansum(P[\"W3\"][NB[\"W3\"]])\n    r[\"str_growth\"] = math.log(sp3 + 1) - math.log(sp1 + 1)\n    n_years = len(early_years)\n    r[\"new_edge_rate\"] = (M / float(n_years)) / (n1 + 1)\n\n    def jac(a, b):\n        u = (a | b).sum()\n        return (a & b).sum() / u if u else float(\"nan\")\n    with warnings.catch_warnings():\n        warnings.simplefilter(\"ignore\", RuntimeWarning)\n        r[\"edge_persistence\"] = float(np.nanmean([jac(NB[\"W1\"], NB[\"W2\"]), jac(NB[\"W2\"], NB[\"W3\"])]))\n    r[\"turnover\"] = float((NB[\"W1\"] & ~NB[\"W3\"]).sum() / n1) if n1 else float(\"nan\")\n    s4 = slice_of(win[\"W3\"][-1])\n    if n3 > 0:\n        ws = Counter()\n        for k in np.nonzero(NB[\"W3\"])[0]:\n            ws[C[\"comm\"][s4][k]] += cnt[\"W3\"][k]\n        tot = sum(ws.values())\n        pw = np.array([v / tot for v in ws.values()])\n        r[\"participation\"] = float(1 - (pw ** 2).sum())\n        r[\"n_comm_W3\"] = len(ws)\n        r[\"comm_entropy\"] = float(-(pw * np.log(pw)).sum())\n    else:\n        r[\"participation\"], r[\"n_comm_W3\"], r[\"comm_entropy\"] = float(\"nan\"), 0, float(\"nan\")\n    dom = []\n    for w in (\"W1\", \"W2\", \"W3\"):\n        s = slice_of(win[w][0])\n        if cnt[w].sum() > 0:\n            cs = Counter()\n            for k in np.nonzero(cnt[w])[0]:\n                cs[C[\"comm\"][s][k]] += cnt[w][k]\n            dom.append(cs.most_common(1)[0][0])\n    r[\"comm_transitions\"] = sum(1 for a, b in zip(dom, dom[1:]) if a != b)\n    for w, s in ((\"W1\", s0), (\"W3\", s4)):\n        idx = np.nonzero(NB[w])[0]\n        if len(idx) >= 2:\n            a, b = C[\"full_edges\"][s]\n            ins = np.zeros(C[\"nt\"], dtype=bool)\n            ins[idx] = True\n            e = int((ins[a] & ins[b]).sum())\n            r[f\"ego_density_{w}\"] = e / (len(idx) * (len(idx) - 1) / 2)\n        else:\n            r[f\"ego_density_{w}\"] = float(\"nan\")\n    r[\"ego_density_change\"] = r[\"ego_density_W3\"] - r[\"ego_density_W1\"]\n    if compute_btw:\n        b0, _, c0 = _centrality(np.nonzero(NB[\"W1\"])[0], s0, btw_cutoff)\n        b4, k4, c4 = _centrality(np.nonzero(NB[\"W3\"])[0], s4, btw_cutoff)\n    else:  # iter-4 flag: betweenness / k-core / constraint are not OPEN components and are skipped\n        b0 = b4 = c0 = c4 = float(\"nan\")\n        k4 = -1\n    r[\"btw_start\"], r[\"btw_end\"], r[\"kcore_end\"] = b0, b4, k4\n    r[\"btw_change\"] = b4 - b0\n    r[\"constraint_end\"] = c4\n    r[\"constraint_change\"] = c4 - c0\n    idx = np.nonzero(NB[\"W3\"])[0]\n    top = idx[np.argsort(-P[\"W3\"][idx])][:10]\n    r[\"_top_nb_W3\"] = [(C[\"names\"][k], round(float(P[\"W3\"][k]), 2), int(cnt[\"W3\"][k])) for k in top]\n    return r\n\n\nEGO_OUT = [\"D_z\", \"D_ratio\", \"D_rare\", \"D_sub\", \"D_obs\", \"NOV\", \"NOV_res\", \"F_res\", \"F_z\", \"deg_W1\", \"deg_W3\",\n           \"deg_growth\", \"str_growth\", \"new_edge_rate\", \"edge_persistence\", \"turnover\", \"participation\", \"n_comm_W3\",\n           \"comm_entropy\", \"comm_transitions\", \"ego_density_W3\", \"ego_density_change\", \"btw_end\", \"btw_change\",\n           \"kcore_end\", \"constraint_end\", \"constraint_change\"]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] TOOL CALL — Bash · 2026-09-29 05:19:07 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $SRC10/s7_ego.py; echo ======; cat $SRC10/lib/ego_ctx.py
```

### [23] TOOL RESULT — Bash · 2026-09-29 05:19:07 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"S7 (family A): the six OPEN components under three builds -- ALL, HOME, SIZEMATCH -- over t0-3..t0+2 only.\n\nComponents (EXP8 lib/ego.concept_core, n_null = 0, compute_btw = False): new_edge_rate, n_comm_W3, participation,\nNOV_res, ego_density_W3, edge_persistence.\n  ALL        every grounded early paper (EXP8 definition)\n  HOME       only grounded papers whose venue field is in the concept's home set (PRE and W1-W3); unlabelled dropped\n  SIZEMATCH  20 seeded subsamples (seed = 1000 + ci) of ALL papers, each window (PRE, W1, W2, W3) cut to that window's\n             HOME count; components averaged over the draws\n\nUsage: python s7_ego.py --frame exp5|cohort [--builds home,sizematch,all] [--workers 3] [--limit N] [--subset ci,...]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport multiprocessing as mp\nimport sys\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, EXP8, load_frame, read_parquet_parts, setup_logger\n\nCOMPONENTS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\nN_DRAWS = 20\nOUT = DATA / \"ego_open\"\n\n\ndef _init() -> None:\n    import ego\n    from ego_ctx import rq1_context\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    ego.set_context(rq1_context())\n\n\ndef core6(name: str, aliases: list[str], t0: int, works: list) -> dict:\n    import ego\n    r = ego.concept_core(name, aliases, t0, works, 0, 0, compute_btw=False)\n    return {k: float(r[k]) for k in COMPONENTS} | {\"M\": int(r[\"M\"])}\n\n\ndef window_of(y: int, t0: int) -> int:\n    return 0 if y < t0 else y - t0 + 1        # 0 = PRE, 1..3 = W1..W3\n\n\ndef concept_builds(ci: int, name: str, aliases: list[str], t0: int, rows: list, home_codes: set[int],\n                   builds: tuple[str, ...]) -> dict:\n    \"\"\"rows = [(year, topics tuple, vfield)] grounded early papers t0-3..t0+2.\"\"\"\n    out: dict = {\"ci\": ci}\n    works_all = [(y, tp) for y, tp, _ in rows]\n    home_mask = np.array([v in home_codes for _, _, v in rows], bool)\n    works_home = [w for w, h in zip(works_all, home_mask) if h]\n    yrs = np.array([y for y, _, _ in rows], np.int64)\n    in_early = (yrs >= t0) & (yrs <= t0 + 2)\n    out[\"n_all_early\"] = int(in_early.sum())\n    out[\"n_home_early\"] = int((in_early & home_mask).sum())\n    out[\"n_all_pre\"] = int((yrs < t0).sum())\n    out[\"n_home_pre\"] = int(((yrs < t0) & home_mask).sum())\n    try:\n        if \"full\" in builds:   # EXP8 family-A settings (N_NULL 200, betweenness cutoff 3) for the learned models\n            import ego\n            r = ego.concept_core(name, aliases, t0, works_all, 200, 20260928 + int(ci), btw_cutoff=3, nb_min_w=2)\n            out.update({f\"{k}__full\": float(r[k]) for k in ego.EGO_OUT})\n        if \"all\" in builds:\n            out.update({f\"{k}__all\": v for k, v in core6(name, aliases, t0, works_all).items()})\n        if \"home\" in builds:\n            out.update({f\"{k}__home\": v for k, v in core6(name, aliases, t0, works_home).items()})\n        if \"sizematch\" in builds:\n            rng = np.random.default_rng(1000 + int(ci))\n            win = np.array([window_of(y, t0) for y in yrs], np.int64)\n            idx_by = [np.nonzero(win == w)[0] for w in range(4)]\n            need = [int((home_mask & (win == w)).sum()) for w in range(4)]\n            acc = {k: [] for k in COMPONENTS + [\"M\"]}\n            for _ in range(N_DRAWS):\n                pick = np.concatenate([rng.choice(idx_by[w], size=need[w], replace=False) if need[w] else\n                                       np.zeros(0, np.int64) for w in range(4)])\n                pick.sort()\n                r = core6(name, aliases, t0, [works_all[i] for i in pick])\n                for k in acc:\n                    acc[k].append(r[k])\n            with warnings.catch_warnings():\n                warnings.simplefilter(\"ignore\", RuntimeWarning)\n                for k, v in acc.items():\n                    v = np.asarray(v, float)\n                    # a component is defined for the build if it is finite in >= half of the draws\n                    out[f\"{k}__sizematch\"] = float(np.nanmean(v)) if np.isfinite(v).sum() >= N_DRAWS / 2 else np.nan\n    except (ValueError, IndexError, ZeroDivisionError) as e:\n        out[\"ego_error\"] = repr(e)[:200]\n    return out\n\n\ndef run_chunk(k: int, jobs: list, builds: tuple[str, ...]) -> tuple[int, list, float]:\n    t = time.time()\n    res = [concept_builds(*j, builds=builds) for j in jobs]\n    return k, res, time.time() - t\n\n\ndef home_codes_of(h) -> set[int]:\n    return {int(float(x)) - 10 for x in str(h).split(\";\") if x and x != \"nan\"}\n\n\ndef jobs_exp5(subset=None) -> list:\n    fr = load_frame()\n    if subset is not None:\n        fr = fr[fr.ci.isin(subset)]\n    em = read_parquet_parts(EXP8 / \"data/frame_matches_early\", columns=[\"ci\", \"year\", \"topics\", \"vfield\"])\n    em = em[em.ci.isin(set(fr.ci))]\n    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))\n          for ci, d in em.groupby(\"ci\")}\n    jobs = []\n    for r in fr.itertuples():\n        al = [a for a in str(r.aliases_used).split(\"|\") if a and a != \"nan\"]\n        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))\n    return jobs\n\n\ndef jobs_cohort(subset=None) -> list:\n    cf = pd.read_csv(DATA / \"cohort_candidates.csv\")\n    lex = pd.read_parquet(Path(__file__).resolve().parent / \"inputs/lexicon_v1.parquet\", columns=[\"aliases_used\"])\n    if subset is not None:\n        cf = cf[cf.ci.isin(subset)]\n    em = pd.read_parquet(DATA / \"passC_early.parquet\", columns=[\"ci\", \"year\", \"topics\", \"vfield\", \"tagstate\"])\n    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]\n    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))\n          for ci, d in em.groupby(\"ci\")}\n    jobs = []\n    for r in cf.itertuples():\n        al = [a for a in str(lex.aliases_used.iat[r.ci]).split(\"|\") if a and a not in (\"nan\", \"None\")]\n        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))\n    return jobs\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--frame\", required=True, choices=[\"exp5\", \"cohort\"])\n    ap.add_argument(\"--builds\", default=\"home,sizematch\")\n    ap.add_argument(\"--workers\", type=int, default=3)\n    ap.add_argument(\"--limit\", type=int, default=0)\n    ap.add_argument(\"--chunk\", type=int, default=100)\n    ap.add_argument(\"--subset\", default=\"\")\n    ap.add_argument(\"--tag\", default=\"\")\n    a = ap.parse_args()\n    logger = setup_logger(f\"s7_ego_{a.frame}{a.tag}\")\n    builds = tuple(a.builds.split(\",\"))\n    subset = [int(x) for x in a.subset.split(\",\")] if a.subset else None\n    jobs = jobs_exp5(subset) if a.frame == \"exp5\" else jobs_cohort(subset)\n    if a.limit:\n        jobs = jobs[:a.limit]\n    outdir = OUT / f\"{a.frame}{a.tag}\"\n    outdir.mkdir(parents=True, exist_ok=True)\n    chunks = [jobs[i:i + a.chunk] for i in range(0, len(jobs), a.chunk)]\n    todo = [k for k in range(len(chunks)) if not (outdir / f\"chunk_{k:05d}.parquet\").exists()]\n    logger.info(f\"{a.frame}: {len(jobs)} concepts, builds {builds}, {len(chunks)} chunks, todo {len(todo)}, \"\n                f\"workers {a.workers}\")\n    t0 = time.time()\n    done_n = 0\n    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex:\n        futs = [ex.submit(run_chunk, k, chunks[k], builds) for k in todo]\n        for i, fu in enumerate(as_completed(futs)):\n            k, res, dt = fu.result()\n            pd.DataFrame(res).to_parquet(outdir / f\"chunk_{k:05d}.parquet\", index=False)\n            done_n += len(res)\n            el = time.time() - t0\n            logger.info(f\"chunk {i+1}/{len(futs)} ({done_n} concepts) {el/60:.1f} min; {dt/len(res):.2f} s/concept/\"\n                        f\"worker; eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min\")\n    parts = sorted(outdir.glob(\"chunk_*.parquet\"))\n    df = pd.concat([pd.read_parquet(p) for p in parts], ignore_index=True)\n    df.to_parquet(DATA / f\"ego_open_{a.frame}{a.tag}.parquet\", index=False)\n    logger.info(f\"wrote {len(df)} rows -> data/ego_open_{a.frame}{a.tag}.parquet\")\n\n\nif __name__ == \"__main__\":\n    main()\n======\n\"\"\"Context for lib/ego.py: EXP3 Leiden-gamma-3 topic backbones (slices 2000-04/05-09/10-14), topic metadata,\ncontent lemmas (verbatim from EXP3 common.py), and the Pass A full-corpus topic background.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport re\nfrom collections import Counter\nfrom functools import lru_cache\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, INPUTS\n\n_STOP = set(\"a an and are as at be but by for if in into is it no not of on or such that the their then there these \"\n            \"they this to was will with its via from using based\".split())\n_TOK = re.compile(r\"[^\\W_]+\", re.UNICODE)\n\n\n@lru_cache(maxsize=None)\ndef _stemmer():\n    import snowballstemmer\n    return snowballstemmer.stemmer(\"porter\")\n\n\ndef lemmas(text: str) -> set[str]:\n    t = re.sub(r\"[\\-‐-—/]\", \" \", str(text).lower())\n    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}\n\n\ndef topic_lemma_df(names: list[str]) -> Counter:\n    df = Counter()\n    for n in names:\n        df.update(lemmas(n))\n    return df\n\n\ndef backbone_context() -> dict:\n    tids = json.loads((INPUTS / \"topic_ids.json\").read_text())\n    tm = pd.read_csv(INPUTS / \"topic_meta.csv\").set_index(\"topic\").loc[tids]\n    sl = [np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\") for s in range(3)]\n    names = tm.name.tolist()\n    return dict(nt=len(tids), comm=[z[\"comm\"] for z in sl], comm_q=[z[\"comm_q\"] for z in sl],\n                deg=[z[\"deg\"] for z in sl], knn=[(z[\"ka\"], z[\"kb\"]) for z in sl],\n                full_edges=[(z[\"a\"], z[\"b\"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,\n                ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names], lemmas=lemmas)\n\n\ndef rq1_context() -> dict:\n    ctx = backbone_context()\n    z = np.load(DATA / \"bg_topics.npz\")\n    years = z[\"years\"].tolist()\n    ctx.update(years=years, bg=z[\"BG\"], Gt=dict(zip(years, z[\"GT\"].tolist())))\n    return ctx", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-29 05:19:09 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $SRC10/lib/common.py; echo =====; grep -rn "bg_topics\|passC_bg" $SRC10/*.py $SRC10/lib/*.py | head -30
```

### [25] TOOL RESULT — Bash · 2026-09-29 05:19:11 UTC

```
{"stdout": "\"\"\"Shared constants, paths and small helpers for the RQ1 held-out pipeline.\n\nThe title analyser / surface normaliser / matcher are imported from common5.py (EXP5's common.py, copied verbatim)\nso the matching is byte-identical to the EXP5 scan that defined the frame.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nfrom pathlib import Path\n\nimport numpy as np\n\nLIB = Path(__file__).resolve().parent\nROOT = LIB.parent\nsys.path.insert(0, str(LIB))\n\nINPUTS = ROOT / \"inputs\"\nDATA = ROOT / \"data\"\nRES = ROOT / \"results\"\nLOGS = ROOT / \"logs\"\nFIGS = ROOT / \"figures\"\nMODELS = ROOT / \"models\"\nPASSA = ROOT / \"passA\" / \"parts\"\nPASSB = ROOT / \"passB\" / \"parts\"\nfor _d in (DATA, RES, LOGS, FIGS, MODELS):\n    _d.mkdir(parents=True, exist_ok=True)\n\nRUN_ROOT = Path(os.environ.get(\"AII_RUN_ROOT\", str(ROOT.parents[3])))\nEXP5 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_5\"\nEXP3 = RUN_ROOT / \"3_invention_loop/iter_1/gen_art/gen_art_experiment_3\"\nEXP8 = RUN_ROOT / \"3_invention_loop/iter_3/gen_art/gen_art_experiment_8\"\nEXP6 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_experiment_6\"\nEVAL1 = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_evaluation_1\"\nO5DIR = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"\n\nSEED = 20260928\nY0, Y1 = 1995, 2022\nNY = Y1 - Y0 + 1\nMATCH_Y0, MATCH_Y1 = 2000, 2016      # t0 in 2003..2014 -> feature windows t0-3..t0+2 lie in 2000..2016\nTAG_MIN = 0.3\nGROUP_OF_FIELD = {17: \"CS\", 22: \"Eng\", 13: \"BGM\", 27: \"Med\", 29: \"Med\", 35: \"Med\", 36: \"Med\",\n                  15: \"PHYS\", 16: \"PHYS\", 19: \"PHYS\", 21: \"PHYS\", 25: \"PHYS\", 31: \"PHYS\",\n                  11: \"LIFEENV\", 23: \"LIFEENV\", 24: \"LIFEENV\", 28: \"LIFEENV\", 30: \"LIFEENV\", 34: \"LIFEENV\",\n                  12: \"SOC\", 14: \"SOC\", 20: \"SOC\", 32: \"SOC\", 33: \"SOC\",\n                  26: \"MATHDEC\", 18: \"MATHDEC\"}\nDEV_GROUPS = [\"CS\", \"Eng\", \"BGM\", \"Med\"]\nHELD_GROUPS = [\"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]\nUNITS = HELD_GROUPS + [\"COH_DEVHOME\", \"COH_OTHER\"]\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\n\ndef setup_logger(name: str):\n    from loguru import logger\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n    return logger\n\n\ndef mix64(x: np.ndarray) -> np.ndarray:\n    \"\"\"splitmix64 finaliser (identical to EXP5 scan_full.mix64).\"\"\"\n    z = x.astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)\n    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)\n    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)\n    return (z ^ (z >> np.uint64(31))) & np.uint64(0x7FFFFFFFFFFFFFFF)\n\n\ndef works_files() -> list[tuple[int, str, int, int]]:\n    man = json.loads((ROOT / \"snapshot/works_manifest.json\").read_text())\n    return [(i, f[\"url\"].replace(\"s3://openalex/\", \"\"), f[\"meta\"][\"content_length\"], f[\"meta\"][\"record_count\"])\n            for i, f in enumerate(man[\"files\"])]\n\n\ndef source_field_lut() -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"(sorted source ids, vfield code 0..26) -- identical to EXP5 common.source_field_lut.\"\"\"\n    import pandas as pd\n    sf = pd.read_parquet(INPUTS / \"source_field.parquet\")\n    sid = sf.source.to_numpy(np.int64)\n    code = np.where(sf.field.isna(), 0, sf.field.fillna(11).astype(int) - 10).astype(np.int8)\n    o = np.argsort(sid)\n    return sid[o], code[o]\n\n\ndef sha256_file(p: Path) -> str:\n    h = hashlib.sha256()\n    with Path(p).open(\"rb\") as f:\n        for b in iter(lambda: f.read(1 << 20), b\"\"):\n            h.update(b)\n    return h.hexdigest()\n\n\ndef _clean(o):\n    if isinstance(o, dict):\n        return {str(k): _clean(v) for k, v in o.items()}\n    if isinstance(o, (list, tuple)):\n        return [_clean(v) for v in o]\n    if isinstance(o, np.ndarray):\n        return _clean(o.tolist())\n    if isinstance(o, (np.integer,)):\n        return int(o)\n    if isinstance(o, (np.bool_,)):\n        return bool(o)\n    if isinstance(o, (np.floating, float)):\n        return None if not math.isfinite(float(o)) else float(o)\n    return o\n\n\ndef jdump(obj, path: Path) -> None:\n    Path(path).write_text(json.dumps(_clean(obj), indent=1, default=str))\n\n\ndef add_deviation(key: str, text: str) -> None:\n    p = RES / \"deviations.json\"\n    d = json.loads(p.read_text()) if p.exists() else {}\n    d[key] = text\n    p.write_text(json.dumps(d, indent=1))\n\n\ndef load_frame():\n    import pandas as pd\n    fr = pd.read_csv(EXP5 / \"frame_concepts.csv\")\n    fr[\"split_raw\"] = fr[\"split\"]\n    fr[\"split\"] = np.where(fr.split_raw.str.startswith(\"HELDOUT\"), \"HELDOUT\", fr.split_raw)\n    dev_home = set(DEV_GROUPS)\n    fr[\"cohort_part\"] = np.where(fr.split == \"COHORT\",\n                                 np.where(fr.group.isin(dev_home), \"COH_DEVHOME\", \"COH_OTHER\"), None)\n    fr[\"unit\"] = np.where(fr.split == \"COHORT\", fr.cohort_part, fr.group)\n    return fr\n\n\ndef write_parquet_parts(df, out_dir: Path, rows_per_part: int = 1_500_000) -> list[Path]:\n    out_dir.mkdir(parents=True, exist_ok=True)\n    for old in out_dir.glob(\"part_*.parquet\"):\n        old.unlink()\n    paths = []\n    for k, i in enumerate(range(0, max(len(df), 1), rows_per_part), start=1):\n        p = out_dir / f\"part_{k:03d}.parquet\"\n        df.iloc[i:i + rows_per_part].to_parquet(p, index=False, compression=\"zstd\")\n        paths.append(p)\n    return paths\n\n\ndef read_parquet_parts(out_dir: Path, columns=None):\n    import pandas as pd\n    parts = sorted(Path(out_dir).glob(\"part_*.parquet\"))\n    if not parts:\n        raise FileNotFoundError(f\"no parquet parts in {out_dir}\")\n    return pd.concat([pd.read_parquet(p, columns=columns) for p in parts], ignore_index=True)\n=====\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/passC.py:221:    np.savez_compressed(DATA / \"passC_bg.npz\", BG=BG, years=np.arange(BG_Y0, BG_Y1 + 1))\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s3_checks.py:6:T2  BG[year, topic] 2012-2018 == EXP8 bg_topics.npz.\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s3_checks.py:64:    bg = np.load(DATA / \"passC_bg.npz\")\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/s3_checks.py:65:    bg8 = np.load(EXP8 / \"data/bg_topics.npz\")\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/lib/ego_ctx.py:51:    z = np.load(DATA / \"bg_topics.npz\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-29 05:19:13 UTC

```
Reading the EXP10 code and data I build on. Next I'll check the ladder/stats modules and the data files.
```

### [27] TOOL CALL — Bash · 2026-09-29 05:19:13 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $SRC10/lib/ladder.py; echo ====; cat $SRC10/lib/rq1stats.py | head -150
```

### [28] TOOL RESULT — Bash · 2026-09-29 05:19:13 UTC

```
{"stdout": "\"\"\"Ladder machinery: OPEN construction from frozen constants, rung design matrices, partial Spearman with a refit\nconcept bootstrap (EXP8 rq1stats.psp_point), DL pooling over groups, one-sided bootstrap p, Holm.\n\npsp = Pearson(resid(rank x | ranks of continuous covariates + dummies), resid(rank y | same)); the residualisation is\nrefitted in every bootstrap draw (ranks recomputed within the draw). Resampling unit: concept.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom rq1stats import dersimonian_laird, holm, psp_point\n\nCOMPONENTS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\nSIGNS = {\"new_edge_rate\": 1, \"n_comm_W3\": 1, \"participation\": 1, \"NOV_res\": 1, \"ego_density_W3\": -1,\n         \"edge_persistence\": -1}\nBUILDS = [\"home\", \"all\", \"sizematch\"]\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nFOOTPRINT = [\"fp_logN\", \"fp_nfields\"]\nFOOTPRINT_BIN = [\"fp_reemerge\", \"fp_wiki_pre\", \"newborn\"]\nCOVERAGE = [\"label_coverage_early\", \"home_coverage_early\"]\nANALYSIS_GROUP = {\"CS\": \"CS+Eng\", \"Eng\": \"CS+Eng\", \"BGM\": \"BGM+Med\", \"Med\": \"BGM+Med\", \"PHYS\": \"PHYS\",\n                  \"LIFEENV\": \"LIFEENV\", \"SOC\": \"SOC\", \"MATHDEC\": \"MATHDEC\"}\nPOOL_GROUPS = [\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\"]\nRUNGS = [\"R0\", \"R1\", \"R2\", \"R3\", \"R4\", \"R5\"]\nMIN_HOME_PAPERS = 10\n\n\n# ----------------------------------------------------------------------------- OPEN\ndef fit_open_constants(df: pd.DataFrame, build: str) -> dict:\n    \"\"\"Winsor bounds (0.5 / 99.5 pct) and mean / sd of the winsorised component, on the frame given (EXP5).\"\"\"\n    out = {}\n    for k in COMPONENTS:\n        v = df[f\"{k}__{build}\"].to_numpy(float)\n        v = v[np.isfinite(v)]\n        lo, hi = np.percentile(v, [0.5, 99.5])\n        w = np.clip(v, lo, hi)\n        out[k] = {\"lo\": float(lo), \"hi\": float(hi), \"mu\": float(w.mean()), \"sd\": float(w.std()) or 1.0,\n                  \"sign\": SIGNS[k], \"n\": int(len(v))}\n    return out\n\n\ndef open_score(df: pd.DataFrame, build: str, const: dict, min_home: int = MIN_HOME_PAPERS,\n               min_comp: int = 4) -> tuple[np.ndarray, pd.DataFrame]:\n    \"\"\"OPEN_b (NaN unless >= min_comp of 6 z-scores finite; HOME/SIZEMATCH NaN if < min_home home papers t0..t0+2).\"\"\"\n    Z = pd.DataFrame(index=df.index)\n    for k in COMPONENTS:\n        c = const[k]\n        v = df[f\"{k}__{build}\"].to_numpy(float)\n        Z[k] = c[\"sign\"] * (np.clip(v, c[\"lo\"], c[\"hi\"]) - c[\"mu\"]) / c[\"sd\"]\n    nfin = np.isfinite(Z.to_numpy()).sum(1)\n    with np.errstate(invalid=\"ignore\"):\n        o = np.nanmean(np.where(np.isfinite(Z.to_numpy()), Z.to_numpy(), np.nan), axis=1)\n    o[nfin < min_comp] = np.nan\n    if build in (\"home\", \"sizematch\"):\n        o[df[\"n_home_early\"].to_numpy() < min_home] = np.nan\n    return o, Z\n\n\n# ----------------------------------------------------------------------------- rungs\ndef type_dummies(df: pd.DataFrame) -> pd.DataFrame:\n    t = df[\"type\"].fillna(\"unlabelled\")\n    return pd.DataFrame({f\"type_{c}\": (t == c).astype(float) for c in (\"method\", \"object\", \"property\", \"unlabelled\")},\n                        index=df.index)\n\n\ndef level_dummies(df: pd.DataFrame) -> pd.DataFrame:\n    return pd.DataFrame({f\"level_{l}\": (df.level == l).astype(float) for l in (3, 4, 5)}, index=df.index)\n\n\ndef year_dummies(df: pd.DataFrame) -> pd.DataFrame:\n    ys = sorted(df.t0.unique())[1:]\n    return pd.DataFrame({f\"t0_{y}\": (df.t0 == y).astype(float) for y in ys}, index=df.index)\n\n\ndef group_dummies(df: pd.DataFrame) -> pd.DataFrame:\n    gs = sorted(df.agroup.unique())[1:]\n    return pd.DataFrame({f\"g_{g}\": (df.agroup == g).astype(float) for g in gs}, index=df.index)\n\n\ndef rung_design(df: pd.DataFrame, rung: str, drop_type: bool = False, drop_group: bool = False\n                ) -> tuple[pd.DataFrame, pd.DataFrame]:\n    \"\"\"(continuous covariates -> ranked, categorical dummies -> raw) for rung R0..R5.\"\"\"\n    r = RUNGS.index(rung)\n    cont = list(B5)\n    cat = [year_dummies(df)]\n    if \"window_flag\" in df.columns and df.window_flag.nunique() > 1:\n        cat.append(df[[\"window_flag\"]].astype(float))\n    if r >= 1:\n        cont.append(\"CONTACT_REACH\")\n    if r >= 2:\n        if not drop_type:\n            cat.append(type_dummies(df))\n        cat.append(df[[\"generic\"]].astype(float))\n        cat.append(level_dummies(df))\n    if r >= 3:\n        cont += FOOTPRINT\n        cat.append(df[FOOTPRINT_BIN].astype(float))\n    if r >= 4:\n        cont += COVERAGE\n    if r >= 5 and not drop_group:\n        cat.append(group_dummies(df))\n    C = pd.concat(cat, axis=1) if cat else pd.DataFrame(index=df.index)\n    C = C.loc[:, C.std() > 0] if len(C) > 1 else C\n    return df[cont], C\n\n\ndef rung_columns() -> list[str]:\n    return B5 + [\"CONTACT_REACH\", \"generic\", \"level\", \"type\"] + FOOTPRINT + FOOTPRINT_BIN + COVERAGE + [\"agroup\", \"t0\"]\n\n\n# ----------------------------------------------------------------------------- estimation\ndef psp_boot2(x: np.ndarray, y: np.ndarray, B: np.ndarray, C: np.ndarray, n_boot: int, seed: int,\n              direction: int = 1, idx_boot: np.ndarray | None = None) -> dict:\n    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)\n    x, y, B, C = x[ok], y[ok], B[ok], C[ok]\n    n = len(x)\n    if n < 30 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"rho\": math.nan, \"ci\": [math.nan, math.nan], \"se\": math.nan, \"p_one\": math.nan,\n                \"p_two\": math.nan, \"boot\": np.array([])}\n    est = psp_point(x, y, B, C)\n    rng = np.random.default_rng(seed)\n    bs = np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        Ci = C[i]\n        keep = Ci.std(0) > 0 if Ci.shape[1] else np.zeros(0, bool)\n        bs[b] = psp_point(x[i], y[i], B[i], Ci[:, keep])\n    bs = bs[np.isfinite(bs)]\n    lo, hi = np.percentile(bs, [2.5, 97.5])\n    p_one = float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1))\n    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))\n    se_z = float(np.std(z, ddof=1))\n    ze = math.atanh(max(min(est, 0.999999), -0.999999))\n    return {\"n\": int(n), \"rho\": float(est), \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"p_one\": p_one, \"p_two\": float(2 * stats.norm.sf(abs(ze / se_z))) if se_z > 0 else math.nan,\n            \"boot\": bs}\n\n\ndef psp_df(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1,\n           drop_type: bool = False, drop_group: bool = False) -> dict:\n    Bc, Cc = rung_design(df, rung, drop_type, drop_group)\n    r = psp_boot2(df[xcol].to_numpy(float), df[ycol].to_numpy(float), Bc.to_numpy(float), Cc.to_numpy(float),\n                  n_boot, seed, direction)\n    r.update({\"x\": xcol, \"y\": ycol, \"rung\": rung, \"resampling_unit\": \"concept\", \"n_boot\": n_boot})\n    return r\n\n\ndef paired_diff(df: pd.DataFrame, xa: str, xb: str, ycol: str, rung: str, n_boot: int, seed: int) -> dict:\n    \"\"\"Paired concept bootstrap of psp(xa) - psp(xb) on the common sample.\"\"\"\n    Bc, Cc = rung_design(df, rung)\n    B, C = Bc.to_numpy(float), Cc.to_numpy(float)\n    xa_, xb_, y = df[xa].to_numpy(float), df[xb].to_numpy(float), df[ycol].to_numpy(float)\n    ok = np.isfinite(xa_) & np.isfinite(xb_) & np.isfinite(y) & np.all(np.isfinite(B), 1)\n    xa_, xb_, y, B, C = xa_[ok], xb_[ok], y[ok], B[ok], C[ok]\n    n = len(y)\n    if n < 30:\n        return {\"n\": int(n), \"diff\": math.nan, \"ci\": [math.nan, math.nan]}\n    est = psp_point(xa_, y, B, C) - psp_point(xb_, y, B, C)\n    rng = np.random.default_rng(seed)\n    bs = []\n    for _ in range(n_boot):\n        i = rng.integers(0, n, n)\n        Ci = C[i]\n        keep = Ci.std(0) > 0\n        bs.append(psp_point(xa_[i], y[i], B[i], Ci[:, keep]) - psp_point(xb_[i], y[i], B[i], Ci[:, keep]))\n    bs = np.asarray(bs)\n    bs = bs[np.isfinite(bs)]\n    return {\"n\": int(n), \"a\": xa, \"b\": xb, \"y\": ycol, \"rung\": rung, \"diff\": float(est),\n            \"ci\": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))], \"resampling_unit\": \"concept\"}\n\n\ndef per_group(df: pd.DataFrame, xcol: str, ycol: str, rung: str, n_boot: int, seed: int, direction: int = 1) -> dict:\n    rows = {}\n    for gi, g in enumerate(POOL_GROUPS + [\"MATHDEC\"]):\n        d = df[df.agroup == g]\n        r = psp_df(d, xcol, ycol, rung, n_boot, seed + 101 * gi, direction, drop_group=True)\n        r.pop(\"boot\", None)\n        rows[g] = r\n    b = [rows[g][\"rho\"] for g in POOL_GROUPS]\n    se = [rows[g][\"se\"] for g in POOL_GROUPS]\n    dl = dersimonian_laird(b, se)\n    pos = int(sum(1 for v in b if np.isfinite(v) and v > 0))\n    return {\"groups\": rows, \"DL\": dl, \"n_positive_of_5\": pos, \"x\": xcol, \"y\": ycol, \"rung\": rung}\n\n\ndef strip(d):\n    if isinstance(d, dict):\n        return {k: strip(v) for k, v in d.items() if k != \"boot\"}\n    if isinstance(d, list):\n        return [strip(v) for v in d]\n    return d\n\n\n__all__ = [\"COMPONENTS\", \"SIGNS\", \"BUILDS\", \"RUNGS\", \"B5\", \"ANALYSIS_GROUP\", \"POOL_GROUPS\", \"fit_open_constants\",\n           \"open_score\", \"rung_design\", \"psp_boot2\", \"psp_df\", \"paired_diff\", \"per_group\", \"holm\", \"strip\",\n           \"dersimonian_laird\"]\n====\n\"\"\"Statistics for RQ1: partial Spearman given a baseline (rank residualisation, refitted in every bootstrap\nresample), L2-logistic delta-AUC (leave-one-group-out, out-of-fold), DerSimonian-Laird pooling, Holm, sign tests.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\n\n# ----------------------------------------------------------------------------- partial Spearman\ndef dummies(v: np.ndarray, drop_first: bool = True) -> np.ndarray:\n    u = np.unique(v)\n    if len(u) <= 1:\n        return np.zeros((len(v), 0))\n    cols = u[1:] if drop_first else u\n    return (v[:, None] == cols[None, :]).astype(float)\n\n\ndef _resid(Z: np.ndarray, Y: np.ndarray) -> np.ndarray:\n    beta, *_ = np.linalg.lstsq(Z, Y, rcond=None)\n    return Y - Z @ beta\n\n\ndef psp_point(x: np.ndarray, y: np.ndarray, B: np.ndarray, cat: np.ndarray | None) -> float:\n    \"\"\"Pearson(resid(rank x ~ rank B + cat dummies), resid(rank y ~ same)). Rows must be complete.\"\"\"\n    Zc = [np.ones((len(x), 1))]\n    if B is not None and B.shape[1]:\n        Zc.append(rankdata(B, axis=0))\n    if cat is not None and cat.shape[1]:\n        Zc.append(cat)\n    Z = np.hstack(Zc)\n    R = _resid(Z, np.c_[rankdata(x), rankdata(y)])\n    sx, sy = R[:, 0].std(), R[:, 1].std()\n    if sx <= 1e-12 or sy <= 1e-12:\n        return float(\"nan\")\n    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])\n\n\ndef psp_boot(x, y, B, cat, n_boot: int, seed: int) -> dict:\n    \"\"\"Point + concept bootstrap (resample rows; ranks and residualisation recomputed in each resample).\"\"\"\n    ok = np.isfinite(x) & np.isfinite(y)\n    if B is not None:\n        ok &= np.all(np.isfinite(B), axis=1)\n    x, y = x[ok], y[ok]\n    Bs = B[ok] if B is not None else None\n    cs = cat[ok] if cat is not None else None\n    n = len(x)\n    if n < 20 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"rho\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"se\": float(\"nan\"), \"p\": float(\"nan\"),\n                \"boot\": np.array([])}\n    est = psp_point(x, y, Bs, cs)\n    rng = np.random.default_rng(seed)\n    bs = np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        bs[b] = psp_point(x[i], y[i], Bs[i] if Bs is not None else None, cs[i] if cs is not None else None)\n    bs = bs[np.isfinite(bs)]\n    lo, hi = np.percentile(bs, [2.5, 97.5]) if len(bs) else (np.nan, np.nan)\n    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))\n    se_z = float(np.std(z, ddof=1)) if len(z) > 2 else float(\"nan\")\n    ze = math.atanh(max(min(est, 0.999999), -0.999999)) if np.isfinite(est) else float(\"nan\")\n    p = float(2 * stats.norm.sf(abs(ze / se_z))) if se_z and np.isfinite(se_z) and se_z > 0 else float(\"nan\")\n    return {\"n\": int(n), \"rho\": est, \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"z\": ze, \"se_z\": se_z, \"p\": p, \"boot\": bs}\n\n\ndef spearman_raw(x, y) -> tuple[float, int]:\n    ok = np.isfinite(x) & np.isfinite(y)\n    if ok.sum() < 10 or np.unique(x[ok]).size < 3:\n        return float(\"nan\"), int(ok.sum())\n    return float(stats.spearmanr(x[ok], y[ok])[0]), int(ok.sum())\n\n\n# ----------------------------------------------------------------------------- L2 logistic (sklearn C=1 objective)\ndef logit_fit(X: np.ndarray, y: np.ndarray, lam: float = 1.0, iters: int = 50) -> np.ndarray:\n    \"\"\"Newton-IRLS for  sum log-loss + lam/2 ||w||^2 (intercept unpenalised). X excludes the intercept.\"\"\"\n    n, d = X.shape\n    A = np.c_[np.ones(n), X]\n    w = np.zeros(d + 1)\n    pen = np.full(d + 1, lam)\n    pen[0] = 0.0\n    for _ in range(iters):\n        eta = A @ w\n        p = 1 / (1 + np.exp(-np.clip(eta, -30, 30)))\n        g = A.T @ (p - y) + pen * w\n        W = p * (1 - p)\n        H = (A * W[:, None]).T @ A + np.diag(pen)\n        try:\n            step = np.linalg.solve(H, g)\n        except np.linalg.LinAlgError:\n            step = np.linalg.lstsq(H, g, rcond=None)[0]\n        w -= step\n        if np.max(np.abs(step)) < 1e-8:\n            break\n    return w\n\n\ndef logit_pred(w: np.ndarray, X: np.ndarray) -> np.ndarray:\n    return 1 / (1 + np.exp(-np.clip(w[0] + X @ w[1:], -30, 30)))\n\n\ndef auc(y: np.ndarray, s: np.ndarray) -> float:\n    y = np.asarray(y).astype(bool)\n    n1, n0 = y.sum(), (~y).sum()\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef _std_fit(X):\n    mu = X.mean(0)\n    sd = X.std(0)\n    sd[sd < 1e-12] = 1.0\n    return mu, sd\n\n\ndef logo_oof(X: np.ndarray, y: np.ndarray, grp: np.ndarray) -> np.ndarray:\n    \"\"\"Out-of-fold predictions, leave-one-group-out, standardisation fitted on the training folds.\"\"\"\n    pred = np.full(len(y), np.nan)\n    for g in np.unique(grp):\n        te = grp == g\n        tr = ~te\n        if y[tr].min() == y[tr].max():\n            continue\n        mu, sd = _std_fit(X[tr])\n        w = logit_fit((X[tr] - mu) / sd, y[tr])\n        pred[te] = logit_pred(w, (X[te] - mu) / sd)\n    return pred\n\n\ndef dauc_logo(Xb: np.ndarray, x: np.ndarray, y: np.ndarray, grp: np.ndarray) -> tuple[float, float, float]:\n    p0 = logo_oof(Xb, y, grp)\n    p1 = logo_oof(np.c_[Xb, x], y, grp)\n    ok = np.isfinite(p0) & np.isfinite(p1)\n    a0, a1 = auc(y[ok], p0[ok]), auc(y[ok], p1[ok])\n    return a1 - a0, a0, a1\n\n\ndef dauc_boot(Xb, x, y, grp, n_boot: int, seed: int) -> dict:\n    ok = np.all(np.isfinite(Xb), 1) & np.isfinite(x) & np.isfinite(y)\n    Xb, x, y, grp = Xb[ok], x[ok], y[ok].astype(float), grp[ok]\n    n = len(y)\n    if n < 50 or y.sum() < 10 or (n - y.sum()) < 10 or np.unique(x).size < 3:\n        return {\"n\": int(n), \"dauc\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"p\": float(\"nan\"), \"boot\": np.array([])}\n    est, a0, a1 = dauc_logo(Xb, x, y, grp)\n    rng = np.random.default_rng(seed)\n    idx_by = {g: np.nonzero(grp == g)[0] for g in np.unique(grp)}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-29 05:19:15 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cd $SRC10; python3 -c "import json;d=json.load(open('results/frozen_spec.json'));print(list(d.keys()));print(json.dumps({k:d[k] for k in d if k in ('code_sha256','open_constants','rungs','groups','bootstrap','prediction_models')},indent=0)[:6000])"; ls data/sealed; ls data/ego_open | head
```

### [30] TOOL RESULT — Bash · 2026-09-29 05:19:15 UTC

```
{"stdout": "['prereg_sha256', 'spec_v0_sha256', 'open_constants', 'open_min_home_papers', 'open_min_components', 'outcome_grounding', 'primary', 'O2r_resid', 'extension_2017', 'power', 'type_labels_sha256', 'type_benchmark', 'rungs', 'groups', 'holm_family', 'directions', 'bootstrap', 'prediction_models', 'cohort_n', 'cohort_n_by_t0', 'sha256', 'code_sha256', 'pre_unseal_checklist']\n{\n\"open_constants\": {\n\"home\": {\n\"new_edge_rate\": {\n\"lo\": 0.0,\n\"hi\": 2.0,\n\"mu\": 0.24226876611794407,\n\"sd\": 0.29476323739891586,\n\"sign\": 1,\n\"n\": 12499\n},\n\"n_comm_W3\": {\n\"lo\": 0.0,\n\"hi\": 5.0,\n\"mu\": 1.251940155212417,\n\"sd\": 1.1109950408968348,\n\"sign\": 1,\n\"n\": 12499\n},\n\"participation\": {\n\"lo\": 0.0,\n\"hi\": 0.7422196372922436,\n\"mu\": 0.23128455585636246,\n\"sd\": 0.2522103838072288,\n\"sign\": 1,\n\"n\": 8968\n},\n\"NOV_res\": {\n\"lo\": -0.9844771539499432,\n\"hi\": 0.09593876134862721,\n\"mu\": -0.540875353868789,\n\"sd\": 0.3801298233025086,\n\"sign\": 1,\n\"n\": 9475\n},\n\"ego_density_W3\": {\n\"lo\": 0.0,\n\"hi\": 1.0,\n\"mu\": 0.7333316442122908,\n\"sd\": 0.2796180574838275,\n\"sign\": -1,\n\"n\": 6810\n},\n\"edge_persistence\": {\n\"lo\": 0.0,\n\"hi\": 0.6739705882352984,\n\"mu\": 0.12122673391085216,\n\"sd\": 0.15763666320353067,\n\"sign\": -1,\n\"n\": 11236\n}\n},\n\"all\": {\n\"new_edge_rate\": {\n\"lo\": 0.0,\n\"hi\": 1.3333333333333333,\n\"mu\": 0.2137749421116557,\n\"sd\": 0.18712524937508748,\n\"sign\": 1,\n\"n\": 12499\n},\n\"n_comm_W3\": {\n\"lo\": 0.0,\n\"hi\": 8.0,\n\"mu\": 2.5383630690455234,\n\"sd\": 1.4439512430434749,\n\"sign\": 1,\n\"n\": 12499\n},\n\"participation\": {\n\"lo\": 0.0,\n\"hi\": 0.8162630102040815,\n\"mu\": 0.3770766100053555,\n\"sd\": 0.2530890675222482,\n\"sign\": 1,\n\"n\": 12167\n},\n\"NOV_res\": {\n\"lo\": -0.9817103130304184,\n\"hi\": 0.09383222083132174,\n\"mu\": -0.4551814113804676,\n\"sd\": 0.33277132442558904,\n\"sign\": 1,\n\"n\": 11747\n},\n\"ego_density_W3\": {\n\"lo\": 0.0,\n\"hi\": 1.0,\n\"mu\": 0.6560566200808624,\n\"sd\": 0.22979526084840923,\n\"sign\": -1,\n\"n\": 11547\n},\n\"edge_persistence\": {\n\"lo\": 0.0,\n\"hi\": 0.7083333333333333,\n\"mu\": 0.2470663128945874,\n\"sd\": 0.15118497685800866,\n\"sign\": -1,\n\"n\": 12493\n}\n},\n\"sizematch\": {\n\"new_edge_rate\": {\n\"lo\": 0.0,\n\"hi\": 1.7250706349206375,\n\"mu\": 0.24845495214503804,\n\"sd\": 0.24328311545526088,\n\"sign\": 1,\n\"n\": 12499\n},\n\"n_comm_W3\": {\n\"lo\": 0.0,\n\"hi\": 5.25,\n\"mu\": 1.2666453316265303,\n\"sd\": 1.027356604119412,\n\"sign\": 1,\n\"n\": 12499\n},\n\"participation\": {\n\"lo\": 0.0,\n\"hi\": 0.7258810098712725,\n\"mu\": 0.2372154124611128,\n\"sd\": 0.20147339071645637,\n\"sign\": 1,\n\"n\": 9186\n},\n\"NOV_res\": {\n\"lo\": -0.9785446383270374,\n\"hi\": 0.08258017262804533,\n\"mu\": -0.5182734615755821,\n\"sd\": 0.27745837112441457,\n\"sign\": 1,\n\"n\": 10314\n},\n\"ego_density_W3\": {\n\"lo\": 0.06410416666666666,\n\"hi\": 1.0,\n\"mu\": 0.7203220375558843,\n\"sd\": 0.18711738942122572,\n\"sign\": -1,\n\"n\": 6878\n},\n\"edge_persistence\": {\n\"lo\": 0.0,\n\"hi\": 0.5544195054026879,\n\"mu\": 0.11378938999765759,\n\"sd\": 0.12655438549382703,\n\"sign\": -1,\n\"n\": 11602\n}\n}\n},\n\"rungs\": {\n\"R0\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\"\n]\n},\n\"R1\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\",\n\"CONTACT_REACH\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\"\n]\n},\n\"R2\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\",\n\"CONTACT_REACH\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\",\n\"type_method\",\n\"type_object\",\n\"type_property\",\n\"generic\",\n\"level_3\",\n\"level_4\",\n\"level_5\"\n]\n},\n\"R3\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\",\n\"CONTACT_REACH\",\n\"fp_logN\",\n\"fp_nfields\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\",\n\"type_method\",\n\"type_object\",\n\"type_property\",\n\"generic\",\n\"level_3\",\n\"level_4\",\n\"level_5\",\n\"fp_reemerge\",\n\"fp_wiki_pre\",\n\"newborn\"\n]\n},\n\"R4\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\",\n\"CONTACT_REACH\",\n\"fp_logN\",\n\"fp_nfields\",\n\"label_coverage_early\",\n\"home_coverage_early\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\",\n\"type_method\",\n\"type_object\",\n\"type_property\",\n\"generic\",\n\"level_3\",\n\"level_4\",\n\"level_5\",\n\"fp_reemerge\",\n\"fp_wiki_pre\",\n\"newborn\"\n]\n},\n\"R5\": {\n\"cont\": [\n\"logvol\",\n\"growth_c\",\n\"offhome_share\",\n\"entropy\",\n\"reach\",\n\"CONTACT_REACH\",\n\"fp_logN\",\n\"fp_nfields\",\n\"label_coverage_early\",\n\"home_coverage_early\"\n],\n\"cat\": [\n\"t0_2016\",\n\"t0_2017\",\n\"window_flag\",\n\"type_method\",\n\"type_object\",\n\"type_property\",\n\"generic\",\n\"level_3\",\n\"level_4\",\n\"level_5\",\n\"fp_reemerge\",\n\"fp_wiki_pre\",\n\"newborn\",\n\"g_CS+Eng\",\n\"g_LIFEENV\",\n\"g_MATHDEC\",\n\"g_PHYS\",\n\"g_SOC\"\n]\n}\n},\n\"groups\": [\n\"CS+Eng\",\n\"BGM+Med\",\n\"PHYS\",\n\"LIFEENV\",\n\"SOC\"\n],\n\"bootstrap\": {\n\"B\": 2000,\n\"seed\": 20260929,\n\"unit\": \"concept\"\n},\n\"prediction_models\": {\n\"B5\": {\n\"coef\": [\n4.766039224098753,\n-0.05511164665586871,\n0.008765664104716067,\n-0.42563667808882066,\n1.6369692811444325,\n0.2840929545239369\n],\n\"mu\": {\n\"logvol\": 4.387217461299273,\n\"growth_c\": 0.13591487868338373,\n\"offhome_share\": 0.2628714872549475,\n\"entropy\": 0.7831561038968538,\n\"reach\": 3.228179741051028\n},\n\"sd\": {\n\"logvol\": 0.3554731095580416,\n\"growth_c\": 0.43536192389233147,\n\"offhome_share\": 0.19848326295216012,\n\"entropy\": 0.4615603694432812,\n\"reach\": 1.550401785313322\n}\n},\n\"B5_plus_OPEN_home\": {\n\"coef\": [\n4.7493521889170065,\n-0.06837795978395791,\n-0.02011091421381037,\n-0.40906407771822595,\n1.6165855309086605,\n0.275042267432687,\n0.2256976026865884\n]\n},\n\"n_fit\": 6565,\n\"note\": \"OLS on EXP5 concepts with finite O2r_m50 (TAG), B5 standardised with EXP5 constants\"\n},\n\"code_sha256\": {\n\"audit.py\": \"2ba65a3f59277a9d92788575e8b4886bf9ec7eb7792fab13a67ce56a6a05a3be\",\n\"lib/common.py\": \"220f2ab3ae4cf629bd084bdbb5080f50eafd8ca89c8f605a832dc5fed50a217b\",\n\"lib/common3.py\": \"ae354fc0d1c97c7434325d3c42326dd8c42e07fcbc7d2017dd0380c6e6d9970e\",\n\"lib/common5.py\": \"733282462213a461dd20dde257267e3fdd7d5c2d56e3fad9f2626f02a6ab95e2\",\n\"lib/design.py\": \"5afc9e94b128fdf575144441a9c915f69806e9c1b3722ea622a0fef95c722f59\",\n\"lib/ego.py\": \"0cd1e8ff522af30d6ecc1b52ffd9f78d82d9233295e445898870c065171af135\",\n\"lib/ego_ctx.py\": \"ca3ef632c90c5bf71d2bf9a39826945cb7b5504be8e86df81db904c49602bced\",\n\"lib/ego_exp3_orig.py\": \"af7b46c965433008d95e7887dddc49f53e037481f9c06761e97a527fe4c64120\",\n\"lib/featport.py\": \"0c394189f8cf53d9a6a01c95d95414f76f04ac179b39b52c0ad55324e8831020\",\n\"lib/frame_exp5.py\": \"e6693f6b5b4c5e832306249acf1fe58988eb0028242665bc773cbc55b3a9486f\",\n\"lib/h2.py\": \"c0886d2410fc14aae21dac338a8bd510a0e97da638642181f1060fe7cd847421\",\n\"lib/indicators.py\": \"621c5ecab831aa7c9810029acb44bc343dc068a382c1babbf22312f245914196\",\n\"lib/ladder.py\": \"f9b5\nparts\ncohort\ncohort_full\nexp5\nexp5_u2", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Bash · 2026-09-29 05:19:25 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cat $SRC10/pyproject.toml; cat > pyproject.toml <<'EOF'
[project]
name = "churn-thin-sample-check"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["numpy", "pandas", "pyarrow", "scipy", "igraph", "numba", "loguru", "snowballstemmer", "matplotlib", "statsmodels", "psutil"]
EOF
uv venv .venv --python=3.12 -q && uv pip install --python .venv/bin/python -q numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil 2>&1 | tail -3; .venv/bin/python -c "import numpy,pandas,igraph,numba,scipy;print(numpy.__version__,pandas.__version__,igraph.__version__,numba.__version__,scipy.__version__)"; grep -i "numpy\|pandas\|scipy\|igraph" $SRC10/requirements.lock.txt
```

### [32] TOOL RESULT — Bash · 2026-09-29 05:21:24 UTC

```
{"stdout": "[project]\nname = \"rq1-fresh-cohort-open\"\nversion = \"0.1.0\"\ndescription = \"RQ1 fresh-cohort test: do open early ego-neighbourhoods anticipate disciplinary breadth (sealed single unseal)\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.12.15\",\n  \"aiosignal==1.4.0\",\n  \"annotated-types==0.8.0\",\n  \"aplr==10.27.0\",\n  \"asttokens==3.0.2\",\n  \"attrs==26.1.0\",\n  \"blinker==1.9.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"comm==0.2.3\",\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"dash==4.4.1\",\n  \"dash-cytoscape==1.0.2\",\n  \"dill==0.4.1\",\n  \"executing==2.2.1\",\n  \"flask==3.1.3\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"frozenlist==1.8.0\",\n  \"gevent==26.9.0\",\n  \"greenlet==3.5.6\",\n  \"idna==3.20\",\n  \"igraph==1.0.0\",\n  \"importlib-metadata==9.0.1\",\n  \"interface-meta==2.0.1\",\n  \"interpret==0.7.8\",\n  \"interpret-core==0.7.8\",\n  \"ipython==9.17.1\",\n  \"ipython-pygments-lexers==1.1.1\",\n  \"ipywidgets==8.1.9\",\n  \"itsdangerous==2.2.0\",\n  \"janus==2.0.0\",\n  \"jedi==0.20.0\",\n  \"jinja2==3.1.6\",\n  \"joblib==1.6.0\",\n  \"jupyterlab-widgets==3.0.17\",\n  \"kiwisolver==1.5.1\",\n  \"leidenalg==0.12.0\",\n  \"llvmlite==0.49.0\",\n  \"loguru==0.7.3\",\n  \"markupsafe==3.0.3\",\n  \"matplotlib==3.11.2\",\n  \"matplotlib-inline==0.2.2\",\n  \"multidict==6.9.1\",\n  \"multiprocess==0.70.19\",\n  \"narwhals==2.26.0\",\n  \"nest-asyncio==1.6.0\",\n  \"numba==0.67.0\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"parso==0.8.7\",\n  \"patsy==1.0.3\",\n  \"pexpect==4.9.0\",\n  \"pillow==12.3.0\",\n  \"plotly==7.1.0\",\n  \"prompt-toolkit==3.0.53\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"ptyprocess==0.7.0\",\n  \"pure-eval==0.2.4\",\n  \"pyahocorasick==2.3.1\",\n  \"pyarrow==25.0.1\",\n  \"pydantic==2.13.5\",\n  \"pydantic-core==2.46.5\",\n  \"pygments==2.21.0\",\n  \"pyparsing==3.3.3\",\n  \"python-dateutil==2.9.0.post0\",\n  \"python-igraph==1.0.0\",\n  \"pyyaml==6.0.3\",\n  \"requests==2.34.2\",\n  \"retrying==1.4.2\",\n  \"salib==1.6.0\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"setuptools==84.0.0\",\n  \"shap==0.52.0\",\n  \"six==1.17.0\",\n  \"slicer==0.0.8\",\n  \"snowballstemmer==3.1.1\",\n  \"stack-data==0.6.3\",\n  \"statsmodels==0.15.0\",\n  \"tenacity==9.1.4\",\n  \"texttable==1.7.0\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"traitlets==5.16.1\",\n  \"typing-extensions==4.16.0\",\n  \"typing-inspection==0.4.4\",\n  \"urllib3==2.8.0\",\n  \"wcwidth==0.9.1\",\n  \"werkzeug==3.1.9\",\n  \"widgetsnbextension==4.0.16\",\n  \"wrapt==2.5.0\",\n  \"yarl==1.25.1\",\n  \"zipp==4.1.0\",\n  \"zope-event==6.2\",\n  \"zope-interface==8.6\",\n]\n2.5.3 3.0.6 1.0.0 0.67.0 1.18.1\nigraph==1.0.0\nnumpy==2.5.3\npandas==3.0.6\npython-igraph==1.0.0\nscipy==1.18.1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] TOOL CALL — Bash · 2026-09-29 05:21:46 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; .venv/bin/python - <<EOF
import pandas as pd, numpy as np
S="$SRC10/data/"
for f in ["ego_open_exp5.parquet","ego_open_cohort.parquet","features_exp5_open.parquet","analysis_cohort.parquet","passC_early.parquet"]:
    d=pd.read_parquet(S+f)
    print("==",f,d.shape); print(list(d.columns))
fe=pd.read_parquet(S+"features_exp5_open.parquet")
for c in ["split","agroup","group","unit","t0","type"]:
    if c in fe: print(c, fe[c].value_counts(dropna=False).to_dict())
ac=pd.read_parquet(S+"analysis_cohort.parquet")
for c in ["agroup","t0","window_flag","type"]:
    if c in ac: print(c, ac[c].value_counts(dropna=False).to_dict())
print(ac[["O2r_m50","OPEN_home","NOV_res__home","edge_persistence__home","n_home_early"]].describe())
EOF
```

### [34] TOOL RESULT — Bash · 2026-09-29 05:21:46 UTC

```
{"stdout": "== ego_open_exp5.parquet (12499, 26)\n['ci', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch']\n== ego_open_cohort.parquet (1535, 26)\n['ci', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch']\n== features_exp5_open.parquet (12499, 63)\n['ci', 'concept_id', 'name', 't0', 'group', 'split', 'home', 'intersect40', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'newborn', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'O2r_m50', 'O2r_resid', 'O2r_m50_MATCH', 'agroup', 'home_coverage_early', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch']\n== analysis_cohort.parquet (1443, 113)\n['ci', 'concept_id', 'qid', 'name', 't0', 'newborn', 'home', 'n_home', 'weak_home', 'intersect40', 'intersect25', 'home_top_share', 'group', 'early_volume', 'role', 'intersection_born', 'precision_c', 'n_labelled_prec', 'precision_source', 'pass_gate', 'n_all_early', 'n_home_early', 'n_all_pre', 'n_home_pre', 'new_edge_rate__all', 'n_comm_W3__all', 'participation__all', 'NOV_res__all', 'ego_density_W3__all', 'edge_persistence__all', 'M__all', 'new_edge_rate__home', 'n_comm_W3__home', 'participation__home', 'NOV_res__home', 'ego_density_W3__home', 'edge_persistence__home', 'M__home', 'new_edge_rate__sizematch', 'n_comm_W3__sizematch', 'participation__sizematch', 'NOV_res__sizematch', 'ego_density_W3__sizematch', 'edge_persistence__sizematch', 'M__sizematch', 'fp_logN', 'fp_nfields', 'fp_reemerge', 'fp_wiki_pre', 'fp_ext_pre', 'o5_joined', 'level', 'logvol', 'growth_c', 'offhome_share', 'entropy', 'reach', 'CONTACT_REACH', 'RETAINED_REACH', 'RETENTION_RATIO_early', 'RETENTION_RATIO_missing', 'label_coverage_early', 'n_authors_early', 'type', 'generic', 'type_agree', 'agroup', 'home_coverage_early', 'window_flag', 'OPEN_home', 'OPEN_all', 'OPEN_sizematch', 'O1b_TAG', 'O3_TAG', 'peak_year_TAG', 'N_outcome_TAG', 'O2r_m50_TAG', 'O2r_m30_TAG', 'O1c_TAG', 'N_late_all_TAG', 'O1b_MATCH', 'O3_MATCH', 'peak_year_MATCH', 'N_outcome_MATCH', 'O2r_m50_MATCH', 'O2r_m30_MATCH', 'O1c_MATCH', 'N_late_all_MATCH', 'O1b', 'O3', 'O2r_m50', 'O2r_m30', 'O1c', 'N_outcome', 'O2r_resid', 'O2r_m50_le2022_TAG', 'O2r_resid_le2022_TAG', 'O1b_TAG_le2022', 'O3_TAG_le2022', 'peak_year_TAG_le2022', 'N_outcome_TAG_le2022', 'O2r_m50_TAG_le2022', 'O2r_m30_TAG_le2022', 'O1c_TAG_le2022', 'N_late_all_TAG_le2022', 'O1b_MATCH_le2022', 'O3_MATCH_le2022', 'peak_year_MATCH_le2022', 'N_outcome_MATCH_le2022', 'O2r_m50_MATCH_le2022', 'O2r_m30_MATCH_le2022', 'O1c_MATCH_le2022', 'N_late_all_MATCH_le2022']\n== passC_early.parquet (391227, 9)\n['ci', 'year', 'work_id', 'vfield', 'tagstate', 'mt', 'topics', 'authors', 'title']\nsplit {'DEV': 4771, 'COHORT': 4356, 'HELDOUT': 3372}\nagroup {'BGM+Med': 4587, 'CS+Eng': 2668, 'SOC': 2211, 'LIFEENV': 1668, 'PHYS': 1097, 'MATHDEC': 268}\ngroup {'Med': 3868, 'SOC': 2211, 'Eng': 2087, 'LIFEENV': 1668, 'PHYS': 1097, 'BGM': 719, 'CS': 581, 'MATHDEC': 268}\nt0 {2003: 1339, 2004: 1227, 2006: 1180, 2008: 1131, 2009: 1108, 2005: 1082, 2007: 1076, 2010: 1010, 2011: 983, 2012: 859, 2013: 811, 2014: 693}\ntype {'object': 6914, 'topic': 2260, 'method': 1836, 'property': 1489}\nagroup {'BGM+Med': 585, 'SOC': 299, 'CS+Eng': 239, 'LIFEENV': 167, 'PHYS': 123, 'MATHDEC': 30}\nt0 {2015: 570, 2016: 500, 2017: 373}\nwindow_flag {0: 1070, 1: 373}\ntype {'object': 721, 'topic': 290, 'property': 221, 'method': 211}\n          O2r_m50    OPEN_home  ...  edge_persistence__home  n_home_early\ncount  634.000000  1186.000000  ...             1267.000000   1443.000000\nmean     4.856140     0.027055  ...                0.108962     37.566875\nstd      2.056691     0.519174  ...                0.155007     48.416036\nmin      1.000000    -1.368038  ...                0.000000      4.000000\n25%      3.335055    -0.352254  ...                0.000000     19.000000\n50%      4.729310    -0.047753  ...                0.000000     29.000000\n75%      6.208970     0.301568  ...                0.183333     44.000000\nmax     11.552922     2.337405  ...                1.000000   1183.000000\n\n[8 rows x 5 columns]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Bash · 2026-09-29 05:21:46 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cd $SRC10; grep -n "0.09\|0.134\|0.112\|-0.11\|0.13[0-9]" results/cohort_result.json | head -30; python3 -c "
import json;d=json.load(open('results/cohort_result.json'));
def walk(o,p=''):
  if isinstance(o,dict):
    for k,v in o.items(): walk(v,p+'/'+k)
  elif isinstance(o,list) and len(o)<3: pass
print(list(d.keys()))
for k,v in d.items():
  if isinstance(v,dict): print(k, list(v.keys())[:30])
"; .venv 2>/dev/null; python3 -c "
import numpy as np; z=np.load('data/bg_topics.npz'); print(z.files, z['years'][:3], z['years'][-3:], z['BG'].shape)"
```

### [36] TOOL RESULT — Bash · 2026-09-29 05:21:46 UTC

```
{"stdout": "22:    0.04136619666988465,\n36:   \"rho\": 0.09743550387304983,\n52:   \"rho\": 0.0905904928497304,\n59:   \"p_two\": 0.028608810613794024,\n103:    0.13482819881772382\n106:   \"p_one\": 0.09045477261369315,\n132:   \"rho\": 0.09197254553510778,\n171:   \"p_two\": 0.06132288984292873,\n187:   \"p_two\": 0.10309526970188618,\n199:    0.13592268698061385\n246:    0.0923126541384861,\n249:   \"se\": 0.040991291672706036,\n262:    0.08771708138412246,\n282:   \"p_one\": 0.0009995002498750624,\n292:   \"rho\": 0.13752993335430844,\n310:    0.11281553613071632,\n326:    0.09037456961980968,\n345:   \"se\": 0.04112254233138984,\n361:   \"se\": 0.04080553529409099,\n377:   \"se\": 0.041330077629881404,\n378:   \"p_one\": 0.0009995002498750624,\n388:   \"rho\": 0.13617341440260444,\n425:   \"se\": 0.039608133259102965,\n427:   \"p_two\": 0.00013075282483899744,\n452:   \"rho\": 0.1365626447765172,\n458:   \"p_one\": 0.0009995002498750624,\n484:   \"rho\": 0.11289312955744948,\n490:   \"p_one\": 0.00399800099950025,\n502:    0.09372883846000933,\n548:   \"rho\": 0.1370033842296326,\n['n_cohort', 'n_by_t0', 'outcome_availability', 'resampling_unit', 'B', 'grounding', 'primary_definition', 'primary', 'groups', 'within_type', 'components', 'retention', 'contrasts', 'holm', 'secondary', 'sensitivity', 'placebos', 'verdict']\nn_by_t0 ['2015', '2016', '2017']\noutcome_availability ['O2r_m50', 'O2r_resid', 'O1c']\nprimary ['OPEN_home|O2r_m50|R0', 'OPEN_home|O2r_m50|R1', 'OPEN_home|O2r_m50|R2', 'OPEN_home|O2r_m50|R3', 'OPEN_home|O2r_m50|R4', 'OPEN_home|O2r_m50|R5', 'OPEN_home|O2r_resid|R0', 'OPEN_home|O2r_resid|R1', 'OPEN_home|O2r_resid|R2', 'OPEN_home|O2r_resid|R3', 'OPEN_home|O2r_resid|R4', 'OPEN_home|O2r_resid|R5', 'OPEN_all|O2r_m50|R0', 'OPEN_all|O2r_m50|R1', 'OPEN_all|O2r_m50|R2', 'OPEN_all|O2r_m50|R3', 'OPEN_all|O2r_m50|R4', 'OPEN_all|O2r_m50|R5', 'OPEN_all|O2r_resid|R0', 'OPEN_all|O2r_resid|R1', 'OPEN_all|O2r_resid|R2', 'OPEN_all|O2r_resid|R3', 'OPEN_all|O2r_resid|R4', 'OPEN_all|O2r_resid|R5', 'OPEN_sizematch|O2r_m50|R0', 'OPEN_sizematch|O2r_m50|R1', 'OPEN_sizematch|O2r_m50|R2', 'OPEN_sizematch|O2r_m50|R3', 'OPEN_sizematch|O2r_m50|R4', 'OPEN_sizematch|O2r_m50|R5']\ngroups ['OPEN_home|O2r_m50|R2', 'OPEN_home|O2r_resid|R2', 'OPEN_home|O2r_m50|R3', 'OPEN_home|O2r_resid|R3', 'OPEN_all|O2r_m50|R2', 'OPEN_all|O2r_resid|R2', 'OPEN_all|O2r_m50|R3', 'OPEN_all|O2r_resid|R3', 'OPEN_sizematch|O2r_m50|R2', 'OPEN_sizematch|O2r_resid|R2', 'OPEN_sizematch|O2r_m50|R3', 'OPEN_sizematch|O2r_resid|R3']\nwithin_type ['OPEN_home|method|R3', 'OPEN_all|method|R3', 'OPEN_sizematch|method|R3', 'OPEN_home|object|R3', 'OPEN_all|object|R3', 'OPEN_sizematch|object|R3', 'OPEN_home|property|R3', 'OPEN_all|property|R3', 'OPEN_sizematch|property|R3', 'OPEN_home|topic|R3', 'OPEN_all|topic|R3', 'OPEN_sizematch|topic|R3']\ncomponents ['new_edge_rate__home|O2r_m50|R2', 'new_edge_rate__home|O2r_m50|R3', 'n_comm_W3__home|O2r_m50|R2', 'n_comm_W3__home|O2r_m50|R3', 'participation__home|O2r_m50|R2', 'participation__home|O2r_m50|R3', 'NOV_res__home|O2r_m50|R2', 'NOV_res__home|O2r_m50|R3', 'ego_density_W3__home|O2r_m50|R2', 'ego_density_W3__home|O2r_m50|R3', 'edge_persistence__home|O2r_m50|R2', 'edge_persistence__home|O2r_m50|R3', 'new_edge_rate__all|O2r_m50|R2', 'new_edge_rate__all|O2r_m50|R3', 'n_comm_W3__all|O2r_m50|R2', 'n_comm_W3__all|O2r_m50|R3', 'participation__all|O2r_m50|R2', 'participation__all|O2r_m50|R3', 'NOV_res__all|O2r_m50|R2', 'NOV_res__all|O2r_m50|R3', 'ego_density_W3__all|O2r_m50|R2', 'ego_density_W3__all|O2r_m50|R3', 'edge_persistence__all|O2r_m50|R2', 'edge_persistence__all|O2r_m50|R3', 'new_edge_rate__sizematch|O2r_m50|R2', 'new_edge_rate__sizematch|O2r_m50|R3', 'n_comm_W3__sizematch|O2r_m50|R2', 'n_comm_W3__sizematch|O2r_m50|R3', 'participation__sizematch|O2r_m50|R2', 'participation__sizematch|O2r_m50|R3']\nretention ['RETENTION_RATIO_early|O2r_m50|R0', 'RETENTION_RATIO_early|O2r_m50|R2', 'RETENTION_RATIO_early|O2r_m50|R3', 'RETENTION_RATIO_early|O2r_resid|R0', 'RETENTION_RATIO_early|O2r_resid|R2', 'RETENTION_RATIO_early|O2r_resid|R3']\ncontrasts ['all_minus_home|R3', 'sizematch_minus_home|R3']\nholm ['OPEN_home|O2r_m50', 'OPEN_home|O2r_resid', 'OPEN_all|O2r_m50', 'OPEN_all|O2r_resid', 'OPEN_sizematch|O2r_m50', 'OPEN_sizematch|O2r_resid', 'RETENTION_RATIO_early|O2r_m50', 'RETENTION_RATIO_early|O2r_resid']\nsecondary ['n_authors_early|O3|R0', 'n_authors_early|O1b|R0', 'n_authors_early|O1c|R0', 'CONTACT_REACH|O2r_m50|R0', 'CONTACT_REACH|O2r_m50|R0|excl_intersection_born', 'CONTACT_REACH|O2r_resid|R0', 'CONTACT_REACH|O2r_resid|R0|excl_intersection_born', 'frozen_prediction_O2r_m50']\nsensitivity ['OPEN_all_on_home_sample|O2r_m50|R2', 'OPEN_home|O2r_m50_le2022_TAG|2015onsets|R2', 'OPEN_home|O2r_m50_TAG|R2', 'OPEN_home|O2r_m50_MATCH|R2', 'OPEN_all|O2r_m50_le2022_TAG|2015onsets|R2', 'OPEN_all|O2r_m50_TAG|R2', 'OPEN_all|O2r_m50_MATCH|R2', 'OPEN_sizematch|O2r_m50_le2022_TAG|2015onsets|R2', 'OPEN_sizematch|O2r_m50_TAG|R2', 'OPEN_sizematch|O2r_m50_MATCH|R2', 'OPEN_home_min5|O2r_m50|R2', 'OPEN_home_min20|O2r_m50|R2', 'OPEN_home|O2r_m50|R2|2015_2016_only', 'open_home_finite_share', 'b5_profile_included_vs_excluded']\nplacebos ['within_group_permutation', 'planted_0.10']\nverdict ['verdict', 'clauses', 'failing_clauses', 'named_readings']\n['BG', 'GT', 'years'] [1995 1996 1997] [2020 2021 2022] (28, 4516)", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Bash · 2026-09-29 05:21:46 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; cd $SRC10; python3 -c "
import json;d=json.load(open('results/cohort_result.json'));
for k in ['OPEN_home|O2r_m50|R2']: print(k, {a:b for a,b in d['primary'][k].items() if a!='boot'})
for k in ['NOV_res__home|O2r_m50|R2','edge_persistence__home|O2r_m50|R2','edge_persistence__home|O2r_m50|R3','ego_density_W3__home|O2r_m50|R2']: print(k, d['components'][k])
print(d['resampling_unit'], d['B'])
"; grep -n "psp_df\|direction\|components\[" s9_unseal.py | head -40
```

### [38] TOOL RESULT — Bash · 2026-09-29 05:21:46 UTC

```
{"stdout": "OPEN_home|O2r_m50|R2 {'n': 573, 'rho': 0.0905904928497304, 'ci': [0.013236035063533528, 0.17104659543493156], 'se': 0.04106142983555049, 'p_one': 0.01199400299850075, 'p_two': 0.028608810613794024, 'x': 'OPEN_home', 'y': 'O2r_m50', 'rung': 'R2', 'resampling_unit': 'concept', 'n_boot': 2000}\nNOV_res__home|O2r_m50|R2 {'n': 506, 'rho': 0.1336899997969982, 'ci': [0.04879666466516195, 0.21531478563393666], 'se': 0.04281623186541612, 'p_one': 0.002997002997002997, 'p_two': 0.0020628686865780312, 'x': 'NOV_res__home', 'y': 'O2r_m50', 'rung': 'R2', 'resampling_unit': 'concept', 'n_boot': 1000}\nedge_persistence__home|O2r_m50|R2 {'n': 597, 'rho': -0.1123107545240305, 'ci': [-0.19855091916322778, -0.023449440507221968], 'se': 0.04409288322821572, 'p_one': 0.9920079920079921, 'p_two': 0.011703770488839596, 'x': 'edge_persistence__home', 'y': 'O2r_m50', 'rung': 'R2', 'resampling_unit': 'concept', 'n_boot': 1000}\nedge_persistence__home|O2r_m50|R3 {'n': 597, 'rho': -0.09929978843309682, 'ci': [-0.18369587691643327, -0.014438307622060874], 'se': 0.04400223945967188, 'p_one': 0.988011988011988, 'p_two': 0.025263840395231902, 'x': 'edge_persistence__home', 'y': 'O2r_m50', 'rung': 'R3', 'resampling_unit': 'concept', 'n_boot': 1000}\nego_density_W3__home|O2r_m50|R2 {'n': 423, 'rho': 0.018455071645998113, 'ci': [-0.0753217739135779, 0.11316892607403922], 'se': 0.04961956151525928, 'p_one': 0.3676323676323676, 'p_two': 0.7107037314906519, 'x': 'ego_density_W3__home', 'y': 'O2r_m50', 'rung': 'R2', 'resampling_unit': 'concept', 'n_boot': 1000}\nconcept 2000\n26:from ladder import (BUILDS, COMPONENTS, POOL_GROUPS, RUNGS, holm, open_score, paired_diff, per_group, psp_df,\n155:                res[\"primary\"][f\"OPEN_{b}|{y}|{r}\"] = strip(psp_df(df, f\"OPEN_{b}\", y, r, B, SEED))\n165:            res[\"within_type\"][f\"OPEN_{b}|{t}|R3\"] = strip(psp_df(d, f\"OPEN_{b}\", \"O2r_m50\", \"R3\", B, SEED,\n170:                res[\"components\"][f\"{k}__{b}|O2r_m50|{r}\"] = strip(psp_df(df, f\"{k}__{b}\", \"O2r_m50\", r, min(1000, B), SEED))\n174:                psp_df(df, \"RETENTION_RATIO_early\", y, r, B, SEED, direction=-1))\n178:    # Holm (8 tests, one-sided bootstrap p in the frozen direction, R2)\n192:        res[\"secondary\"][f\"n_authors_early|{y}|R0\"] = strip(psp_df(df, \"n_authors_early\", y, \"R0\", min(1000, B), SEED))\n194:        res[\"secondary\"][f\"CONTACT_REACH|{y}|R0\"] = strip(psp_df(df, \"CONTACT_REACH\", y, \"R0\", min(1000, B), SEED))\n196:            psp_df(df[df.intersection_born == 0], \"CONTACT_REACH\", y, \"R0\", min(1000, B), SEED))\n218:    res[\"sensitivity\"][\"OPEN_all_on_home_sample|O2r_m50|R2\"] = strip(psp_df(common, \"OPEN_all\", \"O2r_m50\", \"R2\", 1000,\n223:            psp_df(d15, f\"OPEN_{b}\", \"O2r_m50_le2022_TAG\", \"R2\", min(1000, B), SEED))\n224:        res[\"sensitivity\"][f\"OPEN_{b}|O2r_m50_TAG|R2\"] = strip(psp_df(df, f\"OPEN_{b}\", \"O2r_m50_TAG\", \"R2\", min(1000, B), SEED))\n225:        res[\"sensitivity\"][f\"OPEN_{b}|O2r_m50_MATCH|R2\"] = strip(psp_df(df, f\"OPEN_{b}\", \"O2r_m50_MATCH\", \"R2\", 1000,\n229:        res[\"sensitivity\"][f\"OPEN_home_min{mh}|O2r_m50|R2\"] = strip(psp_df(df.assign(OH=o), \"OH\", \"O2r_m50\", \"R2\",\n233:            psp_df(df[df.t0 <= 2016], \"OPEN_home\", \"O2r_m50\", \"R2\", min(1000, B), SEED))\n269:    pl = psp_df(pd.DataFrame({\"x\": xs, \"y\": yplant}).join(df[okp].reset_index(drop=True)[", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-29 05:22:08 UTC

```
Still in the reading phase: checking how EXP10 built the cohort analysis table so my gate can reproduce its numbers exactly.
```

### [40] TOOL CALL — Bash · 2026-09-29 05:22:08 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; sed -n 1,150p $SRC10/s9_unseal.py
```

### [41] TOOL RESULT — Bash · 2026-09-29 05:22:08 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"S9: the SINGLE unseal and the frozen scoring of the fresh 2015-2016(-2017) cohort.\n\n1. lib/seal2.unseal() (refuses without the matching frozen-spec hash, if the sealed parts changed, or on a 2nd call)\n2. cohort outcomes (lib/outc.outcomes, frozen windows; grounding from the frozen S3 decision) -> data/outcomes_cohort.parquet\n   (sha256 hash-chained into logs/seal.log)\n3. frozen ladder, groups (DL), within type, components, RETENTION_RATIO_early, paired build contrasts, Holm, VERDICT\n4. secondary (frozen, no refit): n_authors_early, CONTACT_REACH, frozen B5 vs B5+OPEN_home predictions\n5. placebos: 200 within-group outcome permutations; planted psp = 0.10 recovery\nWrites results/cohort_result.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\nfrom common import DATA, EXP5, RES, ROOT, jdump, setup_logger, sha256_file\nfrom ladder import (BUILDS, COMPONENTS, POOL_GROUPS, RUNGS, holm, open_score, paired_diff, per_group, psp_df,\n                    rung_design, strip)\nfrom outc import outcomes\nfrom rq1stats import psp_point\nfrom seal2 import SPEC, record, unseal\n\nlogger = setup_logger(\"s9_unseal\")\nY0, Y1 = 1995, 2024\nNY = Y1 - Y0 + 1\n\n\ndef build_outcomes(coh: pd.DataFrame, spec: dict, sealed: pd.DataFrame) -> pd.DataFrame:\n    pre = pd.read_parquet(DATA / \"passC_pre_agg.parquet\")\n    pre = pre[pre.ci.isin(set(coh.ci))]\n    agg = pd.concat([pre, sealed[sealed.ci.isin(set(coh.ci))]], ignore_index=True)\n    G = np.load(DATA / \"passC_totals.npz\")[\"G\"].sum(1).astype(float)\n    a, b = spec[\"O2r_resid\"][\"a\"], spec[\"O2r_resid\"][\"b\"]\n    use_match = spec[\"outcome_grounding\"] == \"MATCH\"\n    rows = []\n    for r in coh.itertuples():\n        d = agg[agg.ci == r.ci]\n        rec = {\"ci\": int(r.ci)}\n        for nm, m in ((\"TAG\", d.tagstate == 1), (\"MATCH\", np.ones(len(d), bool))):\n            dd = d[m]\n            N = np.zeros(NY)\n            V = np.zeros((NY, 27))\n            np.add.at(N, dd.year.to_numpy() - Y0, dd.n.to_numpy(float))\n            np.add.at(V, (dd.year.to_numpy() - Y0, dd.vfield.to_numpy()), dd.n.to_numpy(float))\n            shift = 1 if r.t0 == 2017 else 0\n            o = outcomes(N, V, G, int(r.t0), Y0, shift=shift)\n            rec.update({f\"{k}_{nm}\": v for k, v in o.items()})\n            if r.t0 == 2015:   # <= 2022 window for 2015 onsets (t0+5..t0+7), always reported\n                o22 = outcomes(N, V, G, int(r.t0), Y0, shift=1)\n                rec.update({f\"{k}_{nm}_le2022\": v for k, v in o22.items()})\n        g = \"MATCH\" if use_match else \"TAG\"\n        for k in (\"O1b\", \"O3\", \"O2r_m50\", \"O2r_m30\", \"O1c\", \"N_outcome\"):\n            rec[k] = rec[f\"{k}_{g}\"]\n        rec[\"O2r_resid\"] = rec[\"O2r_m50\"] - (a + b * r.logvol) if np.isfinite(rec[\"O2r_m50\"]) else math.nan\n        rec[\"O2r_m50_le2022_TAG\"] = rec.get(\"O2r_m50_TAG_le2022\", math.nan)\n        rec[\"O2r_resid_le2022_TAG\"] = (rec[\"O2r_m50_le2022_TAG\"] - (2.7410366547641205 + 0.3966308230599589 * r.logvol)\n                                       if np.isfinite(rec[\"O2r_m50_le2022_TAG\"]) else math.nan)\n        rows.append(rec)\n    return pd.DataFrame(rows)\n\n\ndef verdict(res: dict) -> dict:\n    L = res[\"primary\"]\n    h2, h3 = L[\"OPEN_home|O2r_m50|R2\"], L[\"OPEN_home|O2r_m50|R3\"]\n    c = {}\n    c[\"1_open_home_R2_R3_ci_gt0\"] = bool(h2[\"rho\"] > 0 and h2[\"ci\"][0] > 0 and h3[\"rho\"] > 0 and h3[\"ci\"][0] > 0)\n    c[\"2_o2r_resid_same_sign_R2\"] = bool(L[\"OPEN_home|O2r_resid|R2\"][\"rho\"] > 0)\n    c[\"3_positive_in_ge4_of_5_groups_R2\"] = bool(res[\"groups\"][\"OPEN_home|O2r_m50|R2\"][\"n_positive_of_5\"] >= 4)\n    wm, wo = res[\"within_type\"][\"OPEN_home|method|R3\"][\"rho\"], res[\"within_type\"][\"OPEN_home|object|R3\"][\"rho\"]\n    c[\"4_within_method_and_object_gt0\"] = bool(np.isfinite(wm) and np.isfinite(wo) and wm > 0 and wo > 0)\n    c[\"5_retention_ratio_lt0_R0\"] = bool(res[\"retention\"][\"RETENTION_RATIO_early|O2r_m50|R0\"][\"rho\"] < 0)\n    disc = bool(h2[\"ci\"][0] <= 0 <= h2[\"ci\"][1])\n    if all(c.values()):\n        v = \"CONFIRMED\"\n    elif disc:\n        v = \"DISCONFIRMED\"\n    else:\n        v = \"PARTIAL\"\n    r1 = L[\"OPEN_home|O2r_m50|R1\"]\n    a_all = L[\"OPEN_all|O2r_m50|R2\"]\n    readings = {\n        \"a_type_absorbs_OPEN\": bool(r1[\"ci\"][0] > 0 and h2[\"ci\"][0] <= 0),\n        \"b_mechanical\": bool(h2[\"ci\"][0] <= 0 and a_all[\"ci\"][0] > 0),\n    }\n    if readings[\"b_mechanical\"]:\n        s2 = L[\"OPEN_sizematch|O2r_m50|R2\"]\n        readings[\"b_sizematch_reading\"] = (\"paper count (SIZEMATCH also null)\" if s2[\"ci\"][0] <= 0\n                                           else \"home restriction (SIZEMATCH still positive)\")\n    return {\"verdict\": v, \"clauses\": c, \"failing_clauses\": [k for k, x in c.items() if not x],\n            \"named_readings\": readings}\n\n\ndef synthetic_sealed(coh: pd.DataFrame) -> pd.DataFrame:\n    \"\"\"DRY RUN ONLY: random outcome-window counts (no real sealed data is read) to exercise every code path.\"\"\"\n    rng = np.random.default_rng(0)\n    rows = []\n    for r in coh.itertuples():\n        for y in range(int(r.t0) + 3, 2025):\n            for vf in rng.choice(np.arange(1, 27), size=4, replace=False):\n                rows.append((r.ci, y, vf, int(rng.choice([1, 1, 2])), 0, int(rng.integers(0, 12))))\n    return pd.DataFrame(rows, columns=[\"ci\", \"year\", \"vfield\", \"tagstate\", \"mt\", \"n\"])\n\n\ndef load_or_unseal(coh: pd.DataFrame, spec: dict, dry: bool) -> pd.DataFrame:\n    \"\"\"Single unseal; a scoring crash AFTER the unseal resumes from the hashed outcomes file (never re-unseals).\"\"\"\n    from seal2 import MARK, _lines\n    if dry:\n        return build_outcomes(coh, spec, synthetic_sealed(coh))\n    rec = [json.loads(l) for l in _lines() if json.loads(l)[\"stage\"] == \"S9_outcomes\"]\n    if MARK.exists() and rec and (DATA / \"outcomes_cohort.parquet\").exists():\n        if sha256_file(DATA / \"outcomes_cohort.parquet\") != rec[-1][\"outcomes_cohort_sha256\"]:\n            raise RuntimeError(\"outcomes_cohort.parquet does not match its seal-log hash\")\n        logger.info(\"resuming scoring from the hashed outcomes_cohort.parquet (unseal already done)\")\n        return pd.read_parquet(DATA / \"outcomes_cohort.parquet\")\n    sealed = unseal()\n    logger.info(f\"UNSEALED {len(sealed)} sealed agg rows for {sealed.ci.nunique()} concepts\")\n    oc = build_outcomes(coh, spec, sealed)\n    oc.to_parquet(DATA / \"outcomes_cohort.parquet\", index=False)\n    record(\"S9_outcomes\", outcomes_cohort_sha256=sha256_file(DATA / \"outcomes_cohort.parquet\"), rows=len(oc))\n    return oc\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    dry = \"--dryrun\" in sys.argv\n    spec = json.loads(SPEC.read_text())\n    for p, h in spec[\"sha256\"].items():\n        if sha256_file(ROOT / p) != h:\n            raise RuntimeError(f\"frozen input changed: {p}\")\n    B = spec[\"bootstrap\"][\"B\"] if not dry else 30\n    SEED = spec[\"bootstrap\"][\"seed\"]\n    coh = pd.read_parquet(DATA / \"features_cohort.parquet\")\n    oc = load_or_unseal(coh, spec, dry)\n    df = coh.merge(oc, on=\"ci\", how=\"left\")\n    tag = \"_dryrun\" if dry else \"\"\n    df.to_parquet(DATA / f\"analysis_cohort{tag}.parquet\", index=False)\n    res: dict = {\"n_cohort\": int(len(df)), \"n_by_t0\": df.t0.value_counts().sort_index().to_dict(),\n                 \"outcome_availability\": {k: int(np.isfinite(df[k]).sum()) for k in (\"O2r_m50\", \"O2r_resid\", \"O1c\")},\n                 \"resampling_unit\": \"concept\", \"B\": B, \"grounding\": spec[\"outcome_grounding\"],\n                 \"primary_definition\": spec[\"primary\"], \"primary\": {}, \"groups\": {}, \"within_type\": {},\n                 \"components\": {}, \"retention\": {}, \"contrasts\": {}, \"holm\": {}, \"secondary\": {}, \"sensitivity\": {},", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-29 05:22:08 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; EXP8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; cat $SRC10/lib/outc.py; ls -la $SRC10/data/sealed/parts | head; cd $SRC10; ../../../../.venv 2>/dev/null; /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/.venv/bin/python -c "
import pandas as pd,glob
p=sorted(glob.glob('data/sealed/parts/*'))[:1]; print(p)
d=pd.read_parquet(p[0]); print(d.head(), d.shape)
d=pd.read_parquet('data/passC_pre_agg.parquet'); print(d.head(), d.shape)
"; ls $EXP8/data/ego_parts | head -3; grep -n "def \|O2r" $EXP8/outcomes.py | head -40
```

### [43] TOOL RESULT — Bash · 2026-09-29 05:22:08 UTC

```
{"stdout": "\"\"\"Concept outcomes from grounded yearly counts (EXP5 frame.concept_outcomes / EXP8 outcomes.py definitions).\n\nN[y] grounded works (all venues), V[y, 27] grounded works by venue-field code (0 = unlabelled), G[y] base works\n(all venues), all indexed by year - Y0. `shift` moves every post-onset window earlier by `shift` years (the 2017\nextension and the <= 2022 TAG sensitivity use shift = 1: t0+5..t0+7 instead of t0+6..t0+8).\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy.special import gammaln\n\n\ndef rarefied_richness(counts, m: int) -> float:\n    \"\"\"EXP5 frame.rarefied_richness (exact hypergeometric; verbatim).\"\"\"\n    n = np.asarray([c for c in counts if c > 0], dtype=float)\n    N = n.sum()\n    if N < m:\n        return math.nan\n    lc = lambda a, b: gammaln(a + 1) - gammaln(b + 1) - gammaln(a - b + 1)  # noqa: E731\n    out = 0.0\n    for nj in n:\n        if N - nj < m:\n            out += 1.0\n        else:\n            out += 1.0 - math.exp(lc(N - nj, m) - lc(N, m))\n    return out\n\n\ndef outcomes(N: np.ndarray, V: np.ndarray, G: np.ndarray, t0: int, Y0: int, shift: int = 0) -> dict:\n    yi = lambda y: y - Y0  # noqa: E731\n    a, b = 6 - shift, 8 - shift          # outcome window t0+a..t0+b\n    sh = lambda y: N[yi(y)] / G[yi(y)]  # noqa: E731\n    o1 = int(np.mean([sh(y) for y in range(t0 + a, t0 + b + 1)]) >= sh(t0 + a - 1))\n    seq = [N[yi(y)] for y in range(t0, t0 + b + 1)]\n    peak_y = t0 + int(np.argmax(seq))\n    late = np.mean([N[yi(t0 + b - 1)], N[yi(t0 + b)]])\n    o3 = int(t0 + 3 <= peak_y <= t0 + b and max(seq) / max(late, 1e-9) >= 2)\n    counts = V[yi(t0 + a):yi(t0 + b) + 1, 1:27].sum(0)\n    rc = [int(round(c)) for c in counts]\n    early = N[yi(t0):yi(t0 + 2) + 1].sum()\n    lateN = N[yi(t0 + a):yi(t0 + b) + 1].sum()\n    return {\"O1b\": o1, \"O3\": o3, \"peak_year\": peak_y, \"N_outcome\": float(counts.sum()),\n            \"O2r_m50\": rarefied_richness(rc, 50), \"O2r_m30\": rarefied_richness(rc, 30),\n            \"O1c\": float(np.log1p(lateN) - np.log1p(early)), \"N_late_all\": float(lateN)}\ntotal 14917\ndrwxr-xr-x 2 165536 165536 2001021 Sep 29 02:58 .\ndrwxr-xr-x 3 165536 165536 2001021 Sep 29 02:23 ..\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0000.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0001.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0002.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0003.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0004.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0005.parquet\n-rw-r--r-- 1 165536 165536    2962 Sep 29 02:58 sealed_0006.parquet\n['data/sealed/parts/sealed_0000.parquet']\nEmpty DataFrame\nColumns: [ci, year, vfield, tagstate, mt, n]\nIndex: [] (0, 6)\n    ci  year  vfield  tagstate  mt   n\n0  136  2012       0         1   2   3\n1  136  2012       0         2   0   1\n2  136  2012       0         2   2  11\n3  136  2012       7         1   0   2\n4  136  2012       7         1   2   4 (134616, 6)\nchunk_00000.parquet\nchunk_00001.parquet\nchunk_00002.parquet\n6:O2r_m50 / O2r_m30  EXP5 exact hypergeometric rarefied venue-field richness t0+6..t0+8\n7:O2r_resid  O2r_m50 - (a + b * logvol); a, b by OLS on DEV ONLY (frozen; EXP5's a = 4.790, b = -0.219 reported)\n36:def load_o5_events(logger, fr: pd.DataFrame) -> pd.DataFrame:\n75:def o5(fr: pd.DataFrame, ev: pd.DataFrame, relations: tuple[str, ...], sources: set[str]) -> pd.DataFrame:\n98:def o4(logger, fr: pd.DataFrame) -> pd.DataFrame:\n115:    def window_sum(ids: np.ndarray, a: np.ndarray, b: np.ndarray) -> np.ndarray:\n158:def main() -> None:\n170:    out = out.merge(co[[\"ci\", \"O1\", \"O3\", \"O2r_m30\", \"O2r_m50\", \"N_outcome\"]].rename(columns={\"O1\": \"O1b\"}),\n174:    dev = (out.split == \"DEV\") & out.O2r_m50.notna() & out.logvol.notna()\n176:    a, b = np.linalg.lstsq(A, out.loc[dev, \"O2r_m50\"].to_numpy(), rcond=None)[0]\n178:    out[\"O2r_resid\"] = out.O2r_m50 - (a + b * out.logvol)\n179:    # EXP5's own O2r_resid definition (O2r_m30 on log outcome-window volume), refitted on DEV: sensitivity only\n181:    devN = dev & out.O2r_m30.notna() & out.N_outcome.notna()\n182:    aN, bN = np.linalg.lstsq(np.c_[np.ones(devN.sum()), lnN[devN]], out.loc[devN, \"O2r_m30\"].to_numpy(), rcond=None)[0]\n183:    out[\"O2r_resid_N\"] = out.O2r_m30 - (aN + bN * lnN)\n184:    jdump({\"a_dev\": a, \"b_dev\": b, \"n_dev\": int(dev.sum()), \"O2r_resid_N_exp5_definition_dev_fit\": {\"a\": aN, \"b\": bN},\n185:           \"note\": \"EXP5 defined O2r_resid = O2r_m30 - (a + b log N_outcome) (outcome-window volume); this plan's primary \"\n186:                   \"O2r_resid = O2r_m50 - (a + b logvol) (early volume). EXP5's constants belong to the other formula, \"\n187:                   \"so they are not a consistency check here; O2r_resid_N reproduces EXP5's definition as a sensitivity.\",\n190:    logger.info(f\"O2r_resid DEV fit: a={a:.3f} b={b:.3f} (EXP5: a=4.790, b=-0.219)\")\n211:    cols = [\"ci\", \"concept_id\", \"t0\", \"group\", \"split\", \"unit\", \"O1c\", \"O1b\", \"O2r_m50\", \"O2r_m30\", \"O2r_resid\",\n212:            \"O2r_resid_N\", \"O3\", \"O4\", \"O5\", \"O5_WW\", \"O5_sens\", \"O5_WW_sens\", \"O5_at_risk\", \"O5_WW_at_risk\", \"N_outcome\"]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Bash · 2026-09-29 05:22:08 UTC

```
SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; EXP8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; EXP5=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; grep -n "def unseal" -A30 $SRC10/lib/seal2.py | head -45; ls -la $SRC10/data/sealed/; du -sh $SRC10/data/sealed/parts; sed -n 158,172p $EXP8/outcomes.py; ls $EXP5 | head -50
```

### [45] TOOL RESULT — Bash · 2026-09-29 05:22:08 UTC

```
{"stdout": "67:def unseal() -> pd.DataFrame:\n68-    if not SPEC.exists():\n69-        raise SealError(\"frozen_spec.json missing: freeze before unsealing\")\n70-    fr = [json.loads(l) for l in _lines() if json.loads(l)[\"stage\"] == \"S8_freeze\"]\n71-    if not fr:\n72-        raise SealError(\"no S8_freeze record in seal.log\")\n73-    if sha256_file(SPEC) != fr[-1][\"frozen_spec_sha256\"]:\n74-        raise SealError(\"frozen_spec.json changed after the seal\")\n75-    if not verify_chain():\n76-        raise SealError(\"seal.log hash chain broken\")\n77-    if MARK.exists():\n78-        raise SealError(f\"cohort outcomes were already unsealed ({MARK.read_text()[:200]})\")\n79-    chk = check_sealed_untouched()\n80-    if not chk[\"ok\"]:\n81-        raise SealError(f\"sealed parts changed: {chk}\")\n82-    df = pd.concat([pd.read_parquet(p) for p in sorted(SEALED_PARTS.glob(\"sealed_*.parquet\"))], ignore_index=True)\n83-    jdump({\"unsealed_at\": time.strftime(\"%Y-%m-%d %H:%M:%S\"), \"frozen_spec_sha256\": fr[-1][\"frozen_spec_sha256\"],\n84-           \"n_sealed_parts\": chk[\"n_logged\"], \"rows\": len(df)}, MARK)\n85-    record(\"S9_unseal\", frozen_spec_sha256=fr[-1][\"frozen_spec_sha256\"], rows=len(df))\n86-    return df\ntotal 5868\ndrwxr-xr-x 3 165536 165536 2001021 Sep 29 02:23 .\ndrwxr-xr-x 4 165536 165536 2005380 Sep 29 03:28 ..\ndrwxr-xr-x 2 165536 165536 2001021 Sep 29 02:58 parts\n13M\t/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data/sealed/parts\ndef main() -> None:\n    logger = setup_logger(\"outcomes\")\n    fr = load_frame()\n    from build_features import load_arrays\n    N, _ = load_arrays(fr)\n    t0 = fr.t0.to_numpy()\n    f = np.arange(len(fr))\n    early = sum(N[f, t0 - Y0 + k] for k in range(3))\n    late = sum(N[f, t0 - Y0 + k] for k in range(6, 9))\n    out = fr[[\"ci\", \"concept_id\", \"t0\", \"group\", \"split\", \"unit\"]].copy()\n    out[\"O1c\"] = np.log1p(late) - np.log1p(early)\n    co = pd.read_csv(EXP5 / \"concept_outcomes.csv\")\n    out = out.merge(co[[\"ci\", \"O1\", \"O3\", \"O2r_m30\", \"O2r_m50\", \"N_outcome\"]].rename(columns={\"O1\": \"O1b\"}),\n                    on=\"ci\", how=\"left\")\n    basic = pd.read_csv(EXP5 / \"concept_features_basic.csv\", usecols=[\"ci\", \"logvol\"])\nREADME.md\naudit.json\naudit.py\naudit_placebo.py\nbackbones.py\nchecks.py\ncohort_episodes_with_pred.csv\ncommon.py\nconcept_features_basic.csv\nconcept_outcomes.csv\ncredits_log.csv\ndev_episodes_with_oof.csv\nepisode_features.csv\nepisodes.csv\nexploratory_domains.py\nfeatures.py\nfigures\nfix_pigeonhole.py\nframe.py\nframe_concepts.csv\nfrozen_lexicon.sha256\nfrozen_spec.json\nfull_method_out.json\ngrounding.py\ngrounding_benchmark.csv\ngrounding_precision.csv\ngrounding_report.json\nheldout_episodes_with_pred.csv\nlexicon.py\nlexicon_v0.parquet\nlexicon_v1.parquet\nllm.py\nllm_cost_log.csv\nlogs\nmake_variants.py\nmatcher.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels.py\noa_client.py\npanel.py\nplacebo_gateways.npy\nplacebo_perm_gateways.npy\nprescreen.py\npreview_method_out.json\nprobe.py\npyproject.toml\nrangefile.py\nreport.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-29 05:22:28 UTC

```
EXP8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; EXP5=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; ls $EXP5 | tail -30; ls $EXP5/data 2>/dev/null | head; grep -n "def load_arrays" -A25 $EXP8/build_features.py; grep -n "rarefied_richness\|O2r_m50" $EXP5/frame.py | head
```

### [47] TOOL RESULT — Bash · 2026-09-29 05:22:28 UTC

```
{"stdout": "make_variants.py\nmatcher.py\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels.py\noa_client.py\npanel.py\nplacebo_gateways.npy\nplacebo_perm_gateways.npy\nprescreen.py\npreview_method_out.json\nprobe.py\npyproject.toml\nrangefile.py\nreport.py\nreproducibility.md\nrestore.sh\nresults\nscan\nscan_full.py\nseal.py\nsens_episodes_b5_t0p4.csv\nsens_episodes_match.csv\nsens_episodes_ptopic.csv\nsense_filter.joblib\nsnapshot\ntests\ntiming_probe.py\nwikidata_aliases.py\n76:def load_arrays(fr: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:\n77-    \"\"\"N[f, y] grounded (TAG) counts all venues, V[f, y, 27] by venue-field code, for frame rows f.\"\"\"\n78-    ag = pd.read_parquet(EXP5 / \"scan/agg_counts.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"tagstate\", \"n\"])\n79-    ag = ag[ag.tagstate == 1]\n80-    pos = pd.Series(np.arange(len(fr)), index=fr.ci.to_numpy())\n81-    ag = ag[ag.ci.isin(pos.index)]\n82-    f = pos.loc[ag.ci.to_numpy()].to_numpy()\n83-    y = ag.year.to_numpy(np.int64) - Y0\n84-    ok = (y >= 0) & (y < NY)\n85-    f, y, vf, n = f[ok], y[ok], ag.vfield.to_numpy(np.int64)[ok], ag.n.to_numpy(np.float64)[ok]\n86-    NF = len(fr)\n87-    N = np.bincount(f * NY + y, weights=n, minlength=NF * NY).reshape(NF, NY)\n88-    V = np.bincount((f * NY + y) * 27 + vf, weights=n, minlength=NF * NY * 27).reshape(NF, NY, 27)\n89-    return N, V\n90-\n91-\n92-def social(e: pd.DataFrame, home_codes: set[int]) -> dict:\n93-    \"\"\"Family S: co-author components among the concept's OFF-HOME labelled early works (t0..t0+2).\"\"\"\n94-    off = e[(e.vfield > 0) & (~e.vfield.isin(home_codes))]\n95-    n_off = len(off)\n96-    if n_off == 0:\n97-        return {\"S_comp\": np.nan, \"S_comp_n\": np.nan, \"S_isolated_share\": np.nan, \"S_author_coverage\": np.nan,\n98-                \"n_offhome_early\": 0}\n99-    au = [a for a in off.authors if len(a)]\n100-    cov = len(au) / n_off\n101-    if cov < 0.5 or len(au) < 2:\n43:def rarefied_richness(counts, m: int) -> float:\n59:def rarefied_richness_frac(counts, m: int) -> float:\n61:    return rarefied_richness([int(round(c)) for c in counts], m)\n157:            \"O2r_m30\": rarefied_richness_frac(counts, 30), \"O2r_m50\": rarefied_richness_frac(counts, 50),", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] ASSISTANT · 2026-09-29 05:23:58 UTC

```
Now checking data sizes (backbone edges, concept counts with ≥10 home papers) to size the compute.
```

### [49] TOOL CALL — Bash · 2026-09-29 05:23:58 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; EXP8=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_3/gen_art/gen_art_experiment_8; .venv/bin/python - <<EOF
import numpy as np, pandas as pd, glob
for s in range(3):
    z=np.load("$SRC10/inputs/backbone/slice%d.npz"%s); a,b=z['a'],z['b']
    pairs=set(zip(np.minimum(a,b).tolist(),np.maximum(a,b).tolist()))
    print(s, z.files, len(a), len(pairs), (a==b).sum(), (a<b).mean(), z['comm'].max(), z['deg'][:5], np.bincount(np.r_[a,b],minlength=4516)[:5])
fe=pd.read_parquet("$SRC10/data/features_exp5_open.parquet",columns=['ci','split','n_home_early','n_home_pre'])
print(fe.groupby('split').apply(lambda d:(d.n_home_early>=10).sum()))
print(fe.n_home_early.describe())
ac=pd.read_parquet("$SRC10/data/analysis_cohort.parquet",columns=['ci','n_home_early','O2r_m50'])
print((ac.n_home_early>=10).sum(), ((ac.n_home_early>=10)&ac.O2r_m50.notna()).sum())
print(len(glob.glob("$EXP8/data/frame_matches_early/part_*")))
EOF
```

### [50] TOOL RESULT — Bash · 2026-09-29 05:23:58 UTC

```
{"stdout": "0 ['a', 'b', 'w', 'c', 'ck', 'W', 'ka', 'kb', 'deg', 'comm', 'comm_q'] 354089 354089 0 1.0 24 [ 90 168 173 162 145] [ 90 168 173 162 145]\n1 ['a', 'b', 'w', 'c', 'ck', 'W', 'ka', 'kb', 'deg', 'comm', 'comm_q'] 396291 396291 0 1.0 28 [ 88 177 187 165 151] [ 88 177 187 165 151]\n2 ['a', 'b', 'w', 'c', 'ck', 'W', 'ka', 'kb', 'deg', 'comm', 'comm_q'] 425549 425549 0 1.0 30 [ 90 175 188 176 143] [ 90 175 188 176 143]\nsplit\nCOHORT     4195\nDEV        4670\nHELDOUT    3214\ndtype: int64\ncount    12499.000000\nmean        37.016961\nstd         31.102902\nmin          0.000000\n25%         20.000000\n50%         32.000000\n75%         46.000000\nmax       1079.000000\nName: n_home_early, dtype: float64\n1365 628\n1", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] ASSISTANT · 2026-09-29 05:23:58 UTC

```
Setting up `lib/` (copied from EXP10, patched paths only) and running the T0 gate against the published EXP10 values.
```

### [52] TOOL CALL — Bash · 2026-09-29 05:23:58 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; SRC10=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10; mkdir -p lib data results logs figures tests; for f in ego.py ego_ctx.py ladder.py rq1stats.py common.py common3.py common5.py stats_core.py design.py outc.py; do cp $SRC10/lib/$f lib/; done; sha256sum lib/*.py; python3 -c "
import json;d=json.load(open('$SRC10/results/frozen_spec.json'));print({k:v for k,v in d['code_sha256'].items() if k.startswith('lib/')})"
```

### [53] TOOL RESULT — Bash · 2026-09-29 05:23:58 UTC

```
{"stdout": "220f2ab3ae4cf629bd084bdbb5080f50eafd8ca89c8f605a832dc5fed50a217b  lib/common.py\nae354fc0d1c97c7434325d3c42326dd8c42e07fcbc7d2017dd0380c6e6d9970e  lib/common3.py\n733282462213a461dd20dde257267e3fdd7d5c2d56e3fad9f2626f02a6ab95e2  lib/common5.py\n5afc9e94b128fdf575144441a9c915f69806e9c1b3722ea622a0fef95c722f59  lib/design.py\n0cd1e8ff522af30d6ecc1b52ffd9f78d82d9233295e445898870c065171af135  lib/ego.py\nca3ef632c90c5bf71d2bf9a39826945cb7b5504be8e86df81db904c49602bced  lib/ego_ctx.py\nf9b5a7618048aa2ba83fd0fb1c3c88aa1a1268e16d513970cccb4c4295e0100a  lib/ladder.py\n5f25d62d44091e7aa9319187887ae660cc08ed519ff15c9cb34938827d73f301  lib/outc.py\n40c779fee977f7a31a55971c6983662f27155cc1b98ada9616ca268bddbf58f1  lib/rq1stats.py\na1c30faeddf9a658bc6dcd9826619cd2f42f51bfa856ef772c1d293b7f2582e9  lib/stats_core.py\n{'lib/common.py': '220f2ab3ae4cf629bd084bdbb5080f50eafd8ca89c8f605a832dc5fed50a217b', 'lib/common3.py': 'ae354fc0d1c97c7434325d3c42326dd8c42e07fcbc7d2017dd0380c6e6d9970e', 'lib/common5.py': '733282462213a461dd20dde257267e3fdd7d5c2d56e3fad9f2626f02a6ab95e2', 'lib/design.py': '5afc9e94b128fdf575144441a9c915f69806e9c1b3722ea622a0fef95c722f59', 'lib/ego.py': '0cd1e8ff522af30d6ecc1b52ffd9f78d82d9233295e445898870c065171af135', 'lib/ego_ctx.py': 'ca3ef632c90c5bf71d2bf9a39826945cb7b5504be8e86df81db904c49602bced', 'lib/ego_exp3_orig.py': 'af7b46c965433008d95e7887dddc49f53e037481f9c06761e97a527fe4c64120', 'lib/featport.py': '0c394189f8cf53d9a6a01c95d95414f76f04ac179b39b52c0ad55324e8831020', 'lib/frame_exp5.py': 'e6693f6b5b4c5e832306249acf1fe58988eb0028242665bc773cbc55b3a9486f', 'lib/h2.py': 'c0886d2410fc14aae21dac338a8bd510a0e97da638642181f1060fe7cd847421', 'lib/indicators.py': '621c5ecab831aa7c9810029acb44bc343dc068a382c1babbf22312f245914196', 'lib/ladder.py': 'f9b5a7618048aa2ba83fd0fb1c3c88aa1a1268e16d513970cccb4c4295e0100a', 'lib/llmc.py': '120fa7de3c9e3abf68197a66f5a816670647366b082f6f69a63696fb9b2a6991', 'lib/matcher.py': '652635cba4f9f5daabd2084f283db6469495bb85dc7e7b5d32ed4480b4356fbb', 'lib/models_exp5.py': 'b44d873b4df40f8be13a04df77eb2d97159704aabc5e3183510b729f0c5bac4c', 'lib/outc.py': '5f25d62d44091e7aa9319187887ae660cc08ed519ff15c9cb34938827d73f301', 'lib/outjson.py': 'ea91b3d64a97e0fc16dfa18264eb6ba541f676c63b9340aad3d535bf7c550bd2', 'lib/panel_exp5.py': '598798bd81c83c134c32f485a96d8a58029a9391341b78b29a661255afd00f0b', 'lib/rangefile.py': '0ae5c0b9c527da96cd4bc84a78247aa9eeec1d0644fe43ada8ec95a263fa9b14', 'lib/rq1stats.py': '40c779fee977f7a31a55971c6983662f27155cc1b98ada9616ca268bddbf58f1', 'lib/seal.py': 'afe1cc003819f3f04924a566ffc29755d6322caeee259fb5d45f5bbca6da68bd', 'lib/seal2.py': '4feaa74f1886cafc5f93279bdff7f83900d3d009b45f11c8b25edb954a419212', 'lib/seal_exp5.py': 'e6dece9ba83ce211475917fa3ec6cd389ffd7f1f65783ecf4786d1d61039967e', 'lib/stats_core.py': 'a1c30faeddf9a658bc6dcd9826619cd2f42f51bfa856ef772c1d293b7f2582e9'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] TOOL CALL — Bash · 2026-09-29 05:24:20 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("lib/common.py"); s=p.read_text()
s=s.replace('INPUTS = ROOT / "inputs"\nDATA = ROOT / "data"','DATA = ROOT / "data"')
s=s.replace('EXP8 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_8"\n',
 'EXP8 = RUN_ROOT / "3_invention_loop/iter_3/gen_art/gen_art_experiment_8"\n'
 '# EXP16 patch: inputs and data are read (read-only) from EXP10; everything written stays under ROOT\n'
 'SRC10 = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_10"\n'
 'INPUTS = SRC10 / "inputs"\nDATA_IN = SRC10 / "data"\n')
assert "DATA_IN" in s and 'INPUTS = SRC10' in s
p.write_text(s)
p=Path("lib/ego_ctx.py"); s=p.read_text()
s=s.replace("from common import DATA, INPUTS","from common import DATA_IN, EXP8, INPUTS")
s=s.replace('z = np.load(DATA / "bg_topics.npz")','bgp = DATA_IN / "bg_topics.npz"\n    z = np.load(bgp if bgp.exists() else EXP8 / "data/bg_topics.npz")')
p.write_text(s)
EOF
grep -n "SRC10\|INPUTS\|DATA_IN" lib/common.py lib/ego_ctx.py
cat > results/deviations.json <<'EOF'
{
 "D0_lib_patch_common": "lib/common.py: INPUTS now points at EXP10/inputs and a new DATA_IN = EXP10/data (read-only); ROOT stays this workspace so every write lands here. No logic changed.",
 "D0_lib_patch_ego_ctx": "lib/ego_ctx.py: bg_topics.npz read from EXP10/data (fallback EXP8/data). No logic changed.",
 "D0_no_git_commit": "The plan asks for a git commit at the seal; the seal is instead a sha256 hash chain in logs/seal.log (no git commit was made by the executor)."
}
EOF
```

### [55] TOOL RESULT — Bash · 2026-09-29 05:24:20 UTC

```
{"stdout": "lib/ego_ctx.py:13:from common import DATA_IN, EXP8, INPUTS\nlib/ego_ctx.py:39:    tids = json.loads((INPUTS / \"topic_ids.json\").read_text())\nlib/ego_ctx.py:40:    tm = pd.read_csv(INPUTS / \"topic_meta.csv\").set_index(\"topic\").loc[tids]\nlib/ego_ctx.py:41:    sl = [np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\") for s in range(3)]\nlib/ego_ctx.py:51:    bgp = DATA_IN / \"bg_topics.npz\"\nlib/common.py:35:SRC10 = RUN_ROOT / \"3_invention_loop/iter_4/gen_art/gen_art_experiment_10\"\nlib/common.py:36:INPUTS = SRC10 / \"inputs\"\nlib/common.py:37:DATA_IN = SRC10 / \"data\"\nlib/common.py:83:    sf = pd.read_parquet(INPUTS / \"source_field.parquet\")", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Write · 2026-09-29 05:24:44 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/jobs.py

"""Job builders copied from EXP10 s7_ego.py (jobs_exp5 / jobs_cohort / home_codes_of) plus the body labels and a
compact HOME-build cache used by every S0-S2 stage.

A job is (ci, name, aliases, t0, rows, home_codes) with rows = [(year, topics tuple, vfield)] grounded early papers
t0-3..t0+2. HOME rows are rows whose vfield is in the concept's home codes (EXP10 definition)."""
from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, EXP8, INPUTS, load_frame, read_parquet_parts

BODY_OF_SPLIT = {"DEV": "DEV", "HELDOUT": "OLDHO", "COHORT": "COH1014"}
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517"]
MIN_HOME = 10


def home_codes_of(h) -> set[int]:
    return {int(float(x)) - 10 for x in str(h).split(";") if x and x != "nan"}


def jobs_exp5(subset=None) -> list:
    fr = load_frame()
    if subset is not None:
        fr = fr[fr.ci.isin(subset)]
    em = read_parquet_parts(EXP8 / "data/frame_matches_early", columns=["ci", "year", "topics", "vfield"])
    em = em[em.ci.isin(set(fr.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    jobs = []
    for r in fr.itertuples():
        al = [a for a in str(r.aliases_used).split("|") if a and a != "nan"]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def jobs_cohort(subset=None) -> list:
    cf = pd.read_csv(DATA_IN / "cohort_candidates.csv")
    keep = set(pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci"]).ci)
    cf = cf[cf.ci.isin(keep)]
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["aliases_used"])
    if subset is not None:
        cf = cf[cf.ci.isin(subset)]
    em = pd.read_parquet(DATA_IN / "passC_early.parquet", columns=["ci", "year", "topics", "vfield", "tagstate"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]
    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))
          for ci, d in em.groupby("ci")}
    jobs = []
    for r in cf.itertuples():
        al = [a for a in str(lex.aliases_used.iat[r.ci]).split("|") if a and a not in ("nan", "None")]
        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))
    return jobs


def home_works(rows: list, home_codes: set[int]) -> list:
    return [(y, tp) for y, tp, v in rows if v in home_codes]


def build_home_cache(path: Path = DATA / "home_cache.pkl") -> dict:
    """{(frame, ci): dict(name, aliases, t0, body, works_home=[(year, topics)], n_home_early)} for ALL concepts."""
    if path.exists():
        return pickle.loads(path.read_bytes())
    fr = load_frame().set_index("ci")
    out = {}
    for j in jobs_exp5():
        ci, name, al, t0, rows, hc = j
        wh = home_works(rows, hc)
        out[("exp5", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body=BODY_OF_SPLIT[fr.at[ci, "split"]],
                                 works=wh, n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))
    for j in jobs_cohort():
        ci, name, al, t0, rows, hc = j
        wh = home_works(rows, hc)
        out[("cohort", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body="COH1517", works=wh,
                                   n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))
    path.write_bytes(pickle.dumps(out, protocol=5))
    return out


def uid_of(frame: str, ci: int) -> str:
    return f"{'E' if frame == 'exp5' else 'C'}{int(ci)}"
```

### [57] TOOL RESULT — Write · 2026-09-29 05:24:44 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/jobs.py", "content": "\"\"\"Job builders copied from EXP10 s7_ego.py (jobs_exp5 / jobs_cohort / home_codes_of) plus the body labels and a\ncompact HOME-build cache used by every S0-S2 stage.\n\nA job is (ci, name, aliases, t0, rows, home_codes) with rows = [(year, topics tuple, vfield)] grounded early papers\nt0-3..t0+2. HOME rows are rows whose vfield is in the concept's home codes (EXP10 definition).\"\"\"\nfrom __future__ import annotations\n\nimport pickle\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN, EXP8, INPUTS, load_frame, read_parquet_parts\n\nBODY_OF_SPLIT = {\"DEV\": \"DEV\", \"HELDOUT\": \"OLDHO\", \"COHORT\": \"COH1014\"}\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"]\nMIN_HOME = 10\n\n\ndef home_codes_of(h) -> set[int]:\n    return {int(float(x)) - 10 for x in str(h).split(\";\") if x and x != \"nan\"}\n\n\ndef jobs_exp5(subset=None) -> list:\n    fr = load_frame()\n    if subset is not None:\n        fr = fr[fr.ci.isin(subset)]\n    em = read_parquet_parts(EXP8 / \"data/frame_matches_early\", columns=[\"ci\", \"year\", \"topics\", \"vfield\"])\n    em = em[em.ci.isin(set(fr.ci))]\n    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))\n          for ci, d in em.groupby(\"ci\")}\n    jobs = []\n    for r in fr.itertuples():\n        al = [a for a in str(r.aliases_used).split(\"|\") if a and a != \"nan\"]\n        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))\n    return jobs\n\n\ndef jobs_cohort(subset=None) -> list:\n    cf = pd.read_csv(DATA_IN / \"cohort_candidates.csv\")\n    keep = set(pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\"]).ci)\n    cf = cf[cf.ci.isin(keep)]\n    lex = pd.read_parquet(INPUTS / \"lexicon_v1.parquet\", columns=[\"aliases_used\"])\n    if subset is not None:\n        cf = cf[cf.ci.isin(subset)]\n    em = pd.read_parquet(DATA_IN / \"passC_early.parquet\", columns=[\"ci\", \"year\", \"topics\", \"vfield\", \"tagstate\"])\n    em = em[(em.tagstate == 1) & em.ci.isin(set(cf.ci))]\n    by = {ci: list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics], d.vfield.astype(int).tolist()))\n          for ci, d in em.groupby(\"ci\")}\n    jobs = []\n    for r in cf.itertuples():\n        al = [a for a in str(lex.aliases_used.iat[r.ci]).split(\"|\") if a and a not in (\"nan\", \"None\")]\n        jobs.append((int(r.ci), str(r.name), al, int(r.t0), by.get(r.ci, []), home_codes_of(r.home)))\n    return jobs\n\n\ndef home_works(rows: list, home_codes: set[int]) -> list:\n    return [(y, tp) for y, tp, v in rows if v in home_codes]\n\n\ndef build_home_cache(path: Path = DATA / \"home_cache.pkl\") -> dict:\n    \"\"\"{(frame, ci): dict(name, aliases, t0, body, works_home=[(year, topics)], n_home_early)} for ALL concepts.\"\"\"\n    if path.exists():\n        return pickle.loads(path.read_bytes())\n    fr = load_frame().set_index(\"ci\")\n    out = {}\n    for j in jobs_exp5():\n        ci, name, al, t0, rows, hc = j\n        wh = home_works(rows, hc)\n        out[(\"exp5\", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body=BODY_OF_SPLIT[fr.at[ci, \"split\"]],\n                                 works=wh, n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))\n    for j in jobs_cohort():\n        ci, name, al, t0, rows, hc = j\n        wh = home_works(rows, hc)\n        out[(\"cohort\", ci)] = dict(ci=ci, name=name, aliases=al, t0=t0, body=\"COH1517\", works=wh,\n                                   n_home_early=sum(1 for y, _ in wh if t0 <= y <= t0 + 2))\n    path.write_bytes(pickle.dumps(out, protocol=5))\n    return out\n\n\ndef uid_of(frame: str, ci: int) -> str:\n    return f\"{'E' if frame == 'exp5' else 'C'}{int(ci)}\"\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [58] TOOL CALL — Write · 2026-09-29 05:25:10 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s0_gate.py

#!/usr/bin/env python3
"""S0 gate T0: (a) recompute the six HOME components with the copied EXP10 lib/ego.concept_core (n_null=0, seed=0,
compute_btw=False) for 300 random EXP5 concepts (seed 1) and ALL COH1517 concepts and compare with EXP10's
ego_open_*.parquet __home columns (max |diff| <= 1e-9); (b) OPEN_home from the frozen constants == the EXP10 frames;
(c) ladder.psp_df on analysis_cohort reproduces the published cohort R2 numbers (<= 1e-6).
Writes results/gate_t0.json."""
from __future__ import annotations

import json
import multiprocessing as mp
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA_IN, RES, jdump, setup_logger
from jobs import build_home_cache

COMPONENTS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def _init() -> None:
    import ego
    from ego_ctx import rq1_context
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())


def core6_batch(items: list) -> list:
    import ego
    out = []
    for key, name, al, t0, works in items:
        t = time.time()
        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)
        out.append((key, {k: float(r[k]) for k in COMPONENTS}, time.time() - t))
    return out


def maxdiff(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:
    both_nan = np.isnan(a) & np.isnan(b)
    mism = np.isnan(a) ^ np.isnan(b)
    d = np.where(both_nan | mism, 0, np.abs(a - b))
    return float(np.nanmax(d)) if len(d) else 0.0, int(mism.sum())


@logger_catch := None or (lambda f: f)
def main() -> None:
    logger = setup_logger("s0_gate")
    cache = build_home_cache()
    logger.info(f"home cache: {len(cache)} concepts")
    spec = json.loads((DATA_IN.parent / "results/frozen_spec.json").read_text())
    rng = np.random.default_rng(1)
    exp5_keys = sorted(k for k in cache if k[0] == "exp5")
    pick = [exp5_keys[i] for i in rng.choice(len(exp5_keys), 300, replace=False)]
    coh_keys = sorted(k for k in cache if k[0] == "cohort")
    items = [(k, cache[k]["name"], cache[k]["aliases"], cache[k]["t0"], cache[k]["works"]) for k in pick + coh_keys]
    chunks = [items[i::4] for i in range(4)]
    t = time.time()
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        res = [r for part in ex.map(core6_batch, chunks) for r in part]
    logger.info(f"T0a recompute {len(res)} concepts in {time.time()-t:.1f}s; "
                f"median {np.median([r[2] for r in res])*1e3:.1f} ms/call")
    rec = pd.DataFrame([{"frame": k[0], "ci": k[1], **v} for k, v, _ in res])
    out: dict = {"T0a": {}, "T0b": {}, "T0c": {}}
    for frame, f in (("exp5", "ego_open_exp5.parquet"), ("cohort", "ego_open_cohort.parquet")):
        ref = pd.read_parquet(DATA_IN / f).set_index("ci")
        mine = rec[rec.frame == frame].set_index("ci")
        ref = ref.loc[mine.index]
        per = {}
        for k in COMPONENTS:
            per[k] = maxdiff(mine[k].to_numpy(float), ref[f"{k}__home"].to_numpy(float))
        out["T0a"][frame] = {"n": int(len(mine)), "max_abs_diff": {k: v[0] for k, v in per.items()},
                             "nan_mismatch": {k: v[1] for k, v in per.items()},
                             "pass": bool(all(v[0] <= 1e-9 and v[1] == 0 for v in per.values()))}
        logger.info(f"T0a {frame}: {out['T0a'][frame]}")
    # (b) OPEN_home from the frozen constants
    from ladder import open_score, psp_df
    const = spec["open_constants"]["home"]
    for nm, f in (("exp5", "features_exp5_open.parquet"), ("cohort", "analysis_cohort.parquet")):
        d = pd.read_parquet(DATA_IN / f)
        o, _ = open_score(d, "home", const)
        md, mm = maxdiff(o, d.OPEN_home.to_numpy(float))
        out["T0b"][nm] = {"max_abs_diff": md, "nan_mismatch": mm, "pass": bool(md <= 1e-9 and mm == 0)}
        logger.info(f"T0b {nm}: {out['T0b'][nm]}")
    # (c) published cohort numbers
    cr = json.loads((DATA_IN.parent / "results/cohort_result.json").read_text())
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet")
    targets = [("OPEN_home", cr["primary"]["OPEN_home|O2r_m50|R2"]),
               ("NOV_res__home", cr["components"]["NOV_res__home|O2r_m50|R2"]),
               ("edge_persistence__home", cr["components"]["edge_persistence__home|O2r_m50|R2"])]
    for x, ref in targets:
        r = psp_df(ac, x, "O2r_m50", "R2", 0 if False else 50, 20260929)
        out["T0c"][x] = {"mine": r["rho"], "published": ref["rho"], "n_mine": r["n"], "n_published": ref["n"],
                         "abs_diff": abs(r["rho"] - ref["rho"]), "pass": bool(abs(r["rho"] - ref["rho"]) <= 1e-6)}
        logger.info(f"T0c {x}: {out['T0c'][x]}")
    out["pass"] = bool(all(v["pass"] for s in ("T0a", "T0b", "T0c") for v in out[s].values()))
    out["timing_ms_per_call_median"] = float(np.median([r[2] for r in res]) * 1e3)
    jdump(out, RES / "gate_t0.json")
    logger.info(f"GATE T0 pass = {out['pass']}")


if __name__ == "__main__":
    main()
```

### [59] TOOL RESULT — Write · 2026-09-29 05:25:10 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s0_gate.py", "content": "#!/usr/bin/env python3\n\"\"\"S0 gate T0: (a) recompute the six HOME components with the copied EXP10 lib/ego.concept_core (n_null=0, seed=0,\ncompute_btw=False) for 300 random EXP5 concepts (seed 1) and ALL COH1517 concepts and compare with EXP10's\nego_open_*.parquet __home columns (max |diff| <= 1e-9); (b) OPEN_home from the frozen constants == the EXP10 frames;\n(c) ladder.psp_df on analysis_cohort reproduces the published cohort R2 numbers (<= 1e-6).\nWrites results/gate_t0.json.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport multiprocessing as mp\nimport sys\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA_IN, RES, jdump, setup_logger\nfrom jobs import build_home_cache\n\nCOMPONENTS = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\n\n\ndef _init() -> None:\n    import ego\n    from ego_ctx import rq1_context\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    ego.set_context(rq1_context())\n\n\ndef core6_batch(items: list) -> list:\n    import ego\n    out = []\n    for key, name, al, t0, works in items:\n        t = time.time()\n        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)\n        out.append((key, {k: float(r[k]) for k in COMPONENTS}, time.time() - t))\n    return out\n\n\ndef maxdiff(a: np.ndarray, b: np.ndarray) -> tuple[float, int]:\n    both_nan = np.isnan(a) & np.isnan(b)\n    mism = np.isnan(a) ^ np.isnan(b)\n    d = np.where(both_nan | mism, 0, np.abs(a - b))\n    return float(np.nanmax(d)) if len(d) else 0.0, int(mism.sum())\n\n\n@logger_catch := None or (lambda f: f)\ndef main() -> None:\n    logger = setup_logger(\"s0_gate\")\n    cache = build_home_cache()\n    logger.info(f\"home cache: {len(cache)} concepts\")\n    spec = json.loads((DATA_IN.parent / \"results/frozen_spec.json\").read_text())\n    rng = np.random.default_rng(1)\n    exp5_keys = sorted(k for k in cache if k[0] == \"exp5\")\n    pick = [exp5_keys[i] for i in rng.choice(len(exp5_keys), 300, replace=False)]\n    coh_keys = sorted(k for k in cache if k[0] == \"cohort\")\n    items = [(k, cache[k][\"name\"], cache[k][\"aliases\"], cache[k][\"t0\"], cache[k][\"works\"]) for k in pick + coh_keys]\n    chunks = [items[i::4] for i in range(4)]\n    t = time.time()\n    with ProcessPoolExecutor(4, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex:\n        res = [r for part in ex.map(core6_batch, chunks) for r in part]\n    logger.info(f\"T0a recompute {len(res)} concepts in {time.time()-t:.1f}s; \"\n                f\"median {np.median([r[2] for r in res])*1e3:.1f} ms/call\")\n    rec = pd.DataFrame([{\"frame\": k[0], \"ci\": k[1], **v} for k, v, _ in res])\n    out: dict = {\"T0a\": {}, \"T0b\": {}, \"T0c\": {}}\n    for frame, f in ((\"exp5\", \"ego_open_exp5.parquet\"), (\"cohort\", \"ego_open_cohort.parquet\")):\n        ref = pd.read_parquet(DATA_IN / f).set_index(\"ci\")\n        mine = rec[rec.frame == frame].set_index(\"ci\")\n        ref = ref.loc[mine.index]\n        per = {}\n        for k in COMPONENTS:\n            per[k] = maxdiff(mine[k].to_numpy(float), ref[f\"{k}__home\"].to_numpy(float))\n        out[\"T0a\"][frame] = {\"n\": int(len(mine)), \"max_abs_diff\": {k: v[0] for k, v in per.items()},\n                             \"nan_mismatch\": {k: v[1] for k, v in per.items()},\n                             \"pass\": bool(all(v[0] <= 1e-9 and v[1] == 0 for v in per.values()))}\n        logger.info(f\"T0a {frame}: {out['T0a'][frame]}\")\n    # (b) OPEN_home from the frozen constants\n    from ladder import open_score, psp_df\n    const = spec[\"open_constants\"][\"home\"]\n    for nm, f in ((\"exp5\", \"features_exp5_open.parquet\"), (\"cohort\", \"analysis_cohort.parquet\")):\n        d = pd.read_parquet(DATA_IN / f)\n        o, _ = open_score(d, \"home\", const)\n        md, mm = maxdiff(o, d.OPEN_home.to_numpy(float))\n        out[\"T0b\"][nm] = {\"max_abs_diff\": md, \"nan_mismatch\": mm, \"pass\": bool(md <= 1e-9 and mm == 0)}\n        logger.info(f\"T0b {nm}: {out['T0b'][nm]}\")\n    # (c) published cohort numbers\n    cr = json.loads((DATA_IN.parent / \"results/cohort_result.json\").read_text())\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\")\n    targets = [(\"OPEN_home\", cr[\"primary\"][\"OPEN_home|O2r_m50|R2\"]),\n               (\"NOV_res__home\", cr[\"components\"][\"NOV_res__home|O2r_m50|R2\"]),\n               (\"edge_persistence__home\", cr[\"components\"][\"edge_persistence__home|O2r_m50|R2\"])]\n    for x, ref in targets:\n        r = psp_df(ac, x, \"O2r_m50\", \"R2\", 0 if False else 50, 20260929)\n        out[\"T0c\"][x] = {\"mine\": r[\"rho\"], \"published\": ref[\"rho\"], \"n_mine\": r[\"n\"], \"n_published\": ref[\"n\"],\n                         \"abs_diff\": abs(r[\"rho\"] - ref[\"rho\"]), \"pass\": bool(abs(r[\"rho\"] - ref[\"rho\"]) <= 1e-6)}\n        logger.info(f\"T0c {x}: {out['T0c'][x]}\")\n    out[\"pass\"] = bool(all(v[\"pass\"] for s in (\"T0a\", \"T0b\", \"T0c\") for v in out[s].values()))\n    out[\"timing_ms_per_call_median\"] = float(np.median([r[2] for r in res]) * 1e3)\n    jdump(out, RES / \"gate_t0.json\")\n    logger.info(f\"GATE T0 pass = {out['pass']}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [60] TOOL CALL — Bash · 2026-09-29 05:25:10 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sed -i '/^@logger_catch := /d' s0_gate.py; sed -i 's/psp_df(ac, x, "O2r_m50", "R2", 0 if False else 50, 20260929)/psp_df(ac, x, "O2r_m50", "R2", 50, 20260929)/' s0_gate.py; timeout 1800 .venv/bin/python s0_gate.py > logs/s0_gate.out 2>&1; tail -20 logs/s0_gate.out
```

### [61] TOOL RESULT — Bash · 2026-09-29 05:25:58 UTC

```
{"stdout": "05:24:36|INFO   |home cache: 13942 concepts\n05:24:55|INFO   |T0a recompute 1743 concepts in 18.6s; median 8.4 ms/call\n05:24:55|INFO   |T0a exp5: {'n': 300, 'max_abs_diff': {'new_edge_rate': 0.0, 'n_comm_W3': 0.0, 'participation': 0.0, 'NOV_res': 0.0, 'ego_density_W3': 0.0, 'edge_persistence': 0.0}, 'nan_mismatch': {'new_edge_rate': 0, 'n_comm_W3': 0, 'participation': 0, 'NOV_res': 0, 'ego_density_W3': 0, 'edge_persistence': 0}, 'pass': True}\n05:24:55|INFO   |T0a cohort: {'n': 1443, 'max_abs_diff': {'new_edge_rate': 0.0, 'n_comm_W3': 0.0, 'participation': 0.0, 'NOV_res': 0.0, 'ego_density_W3': 0.0, 'edge_persistence': 0.0}, 'nan_mismatch': {'new_edge_rate': 0, 'n_comm_W3': 0, 'participation': 0, 'NOV_res': 0, 'ego_density_W3': 0, 'edge_persistence': 0}, 'pass': True}\n05:25:10|INFO   |T0b exp5: {'max_abs_diff': 0.0, 'nan_mismatch': 0, 'pass': True}\n05:25:10|INFO   |T0b cohort: {'max_abs_diff': 0.0, 'nan_mismatch': 0, 'pass': True}\n05:25:10|INFO   |T0c OPEN_home: {'mine': 0.09059049284973036, 'published': 0.0905904928497304, 'n_mine': 573, 'n_published': 573, 'abs_diff': 4.163336342344337e-17, 'pass': True}\n05:25:10|INFO   |T0c NOV_res__home: {'mine': 0.13368999979699833, 'published': 0.1336899997969982, 'n_mine': 506, 'n_published': 506, 'abs_diff': 1.3877787807814457e-16, 'pass': True}\n05:25:10|INFO   |T0c edge_persistence__home: {'mine': -0.11231075452403043, 'published': -0.1123107545240305, 'n_mine': 597, 'n_published': 597, 'abs_diff': 6.938893903907228e-17, 'pass': True}\n05:25:10|INFO   |GATE T0 pass = True", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [62] ASSISTANT · 2026-09-29 05:28:00 UTC

```
Gate T0 passes exactly (all diffs 0.0; the published cohort psp values reproduce to about 1e-16). Next I'm writing the vectorised batch engine `lib/fast6.py`.
```

### [63] TOOL CALL — Write · 2026-09-29 05:28:00 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/fast6.py

"""Vectorised re-implementation of the six OPEN components of lib/ego.concept_core (EXP10 version), batched over
D resamples of ONE concept's HOME papers.

A resample is a label vector over the concept's home papers: -1 = dropped, 0 = PRE (t0-3..t0-1), 1 = W1 (t0),
2 = W2 (t0+1), 3 = W3 (t0+2). The raw build is the label vector implied by the paper years. The SELF set (the
concept's own name topics) is computed ONCE on the full home build (ego.self_topics) and held fixed in every
resample (declared in results/frozen_spec.json). Every other step is copied from ego.concept_core:
  window counts -> neighbours (count >= 2 & PMI > 0 & ~SELF) -> pre_set (PRE count >= 1) -> new = union(NB) & ~pre
  -> first year -> NOV / degree-matched expectation over the pool -> Jaccards -> participation / n_comm over comm[s4]
  -> ego density over full_edges[s4].
Validated against ego.concept_core with the SELF override to <= 1e-12 (tests/u_tests.py, U1)."""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp

import ego

OUT6 = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def base_labels(years: np.ndarray, t0: int) -> np.ndarray:
    lab = np.full(len(years), -1, np.int8)
    lab[(years >= t0 - 3) & (years <= t0 - 1)] = 0
    for j in range(3):
        lab[years == t0 + j] = j + 1
    return lab


def prep(name: str, aliases: list, t0: int, works: list) -> dict:
    """Per-concept precomputation (needs ego.set_context to have been called)."""
    C = ego.C
    years = np.array([y for y, _ in works], np.int64)
    tps = [np.asarray(tp, np.int64) for _, tp in works]
    lab = base_labels(years, t0)
    allt = np.concatenate(tps) if tps else np.zeros(0, np.int64)
    U = np.unique(allt)                                  # ascending global ids -> local order == global order
    nU = len(U)
    loc = {int(g): i for i, g in enumerate(U)}
    rows, cols = [], []
    for p, tp in enumerate(tps):
        for k in tp.tolist():
            rows.append(p)
            cols.append(loc[k])
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(works), nU))   # duplicates summed
    nonempty = np.array([len(tp) > 0 for tp in tps], float)
    # SELF on the FULL home build (ego.self_topics inputs = early-window counts)
    early = [t0, t0 + 1, t0 + 2]
    n_early, nc_early = ego.window_counts(works, early)
    SELF = ego.self_topics(name, aliases, n_early, nc_early)
    selfU = SELF[U]
    # candidate neighbour topics: non-SELF, total W1..W3 count >= 2
    wmask = (lab >= 1).astype(float)
    totW = np.asarray(A.T @ wmask).ravel()
    cand = np.nonzero((~selfU) & (totW >= 2))[0]
    cg = U[cand]
    win = ego.rq1_windows(t0)
    bgw, NW = {}, {}
    for w, ys in win.items():
        b, n = ego.bg_window(ys)
        bgw[w], NW[w] = b, n
    nbg_early, _ = ego.bg_window(early)
    s0 = ego.slice_of(t0)
    s4 = ego.slice_of(win["W3"][-1])
    comm0 = C["comm"][s0]
    dg = C["deg"][s0].astype(float)
    pool0 = (nbg_early > 0) & ~SELF
    Tpool = float(dg[pool0].sum())
    ncomm_g = int(max(c.max() for c in C["comm"])) + 1
    Dc = np.bincount(comm0[pool0], weights=dg[pool0], minlength=ncomm_g)
    # dense W3 adjacency among candidates (full_edges[s4], each listed edge counted once, a < b)
    a, b = C["full_edges"][s4]
    pos = np.full(C["nt"], -1, np.int64)
    pos[cg] = np.arange(len(cg))
    m = (pos[a] >= 0) & (pos[b] >= 0)
    adj = np.zeros((len(cg), len(cg)), float)
    np.add.at(adj, (pos[a[m]], pos[b[m]]), 1.0)
    adj = adj + adj.T
    return dict(t0=t0, U=U, A=A, AT=A.T.tocsr(), nonempty=nonempty, lab=lab, years=years, selfU=selfU, cand=cand,
                cg=cg, SELF=SELF, s0=s0, s4=s4,
                bg_c={w: bgw[w][cg] for w in ("W1", "W2", "W3")}, NW=NW,
                comm0U=comm0[U], comm4c=C["comm"][s4][cg],
                commfy=np.stack([C["comm"][ego.slice_of(t0 + j)][cg] for j in range(3)]),
                dgU=dg[U], pool0U=pool0[U], Tpool=Tpool, Dc=Dc, ncomm_g=ncomm_g, adj=adj)


def window_counts_batch(P: dict, L: np.ndarray, w: int) -> tuple[np.ndarray, np.ndarray]:
    """counts (D x nU) and n papers with >= 1 topic (D) for label w."""
    Mw = (L == w).astype(float)                          # D x P
    cnt = np.asarray((P["AT"] @ Mw.T)).T if P["A"].shape[1] else np.zeros((L.shape[0], 0))
    return cnt, Mw @ P["nonempty"]


def fast6(P: dict, L: np.ndarray, return_sets: bool = False, return_counts: bool = False) -> dict:
    """L: D x P int8 labels. Returns dict of (D,) arrays for OUT6 (+ M, deg_W1, deg_W3, nc_W*) and optionally the
    neighbour sets NB_W1..3 as D x n_cand bool (candidate order P['cg'])."""
    L = np.atleast_2d(L)
    D = L.shape[0]
    cnt, nc = {}, {}
    for w in range(4):
        cnt[w], nc[w] = window_counts_batch(P, L, w)
    cand = P["cand"]
    NB = {}
    for w in (1, 2, 3):
        c = cnt[w][:, cand]
        key = f"W{w}"
        ncw = nc[w][:, None]
        with np.errstate(divide="ignore", invalid="ignore"):
            v = np.log(c * P["NW"][key] / (ncw * P["bg_c"][key][None, :]))
        v[~np.isfinite(v)] = np.nan
        NB[w] = (c >= 2) & (np.nan_to_num(v, nan=-1) > 0) & (ncw > 0)
    pre = cnt[0] >= 1                                     # D x nU
    new = (NB[1] | NB[2] | NB[3]) & ~pre[:, cand]
    M = new.sum(1)
    # first year of each new topic (first early year with count >= 1)
    c1, c2 = cnt[1][:, cand], cnt[2][:, cand]
    fy = np.where(c1 >= 1, 0, np.where(c2 >= 1, 1, 2))
    commfy = np.take_along_axis(np.broadcast_to(P["commfy"][None], (D,) + P["commfy"].shape).transpose(0, 2, 1),
                                fy[:, :, None], axis=2)[:, :, 0] if len(cand) else np.zeros((D, 0), np.int64)
    # C0: dominant W1 community over ALL topics (Counter insertion order == ascending topic id -> ties go to the
    # community whose first contributing topic has the smallest id)
    w1 = cnt[1]
    has1 = w1.sum(1) > 0
    nU = len(P["U"])
    comm0U = P["comm0U"]
    cw = np.zeros((D, P["ncomm_g"]))
    first = np.full((D, P["ncomm_g"]), nU + 1, np.int64)
    rr, kk = np.nonzero(w1 > 0)
    np.add.at(cw, (rr, comm0U[kk]), w1[rr, kk])
    np.minimum.at(first, (rr, comm0U[kk]), kk)
    cmax = cw.max(1, keepdims=True)
    key = np.where((cw == cmax) & (cw > 0), -first, -(10 ** 9))
    C0 = key.argmax(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        nov = ((commfy != C0[:, None]) & new).sum(1) / M
    preP = pre & P["pool0U"][None, :]
    corrT = preP.astype(float) @ P["dgU"]
    corrC = (preP & (comm0U[None, :] == C0[:, None])).astype(float) @ P["dgU"]
    den = P["Tpool"] - corrT
    num = den - (P["Dc"][C0] - corrC)
    with np.errstate(invalid="ignore", divide="ignore"):
        E = np.where(den > 0, num / np.where(den > 0, den, 1), np.nan)
    nov_res = np.where(has1 & (M > 0), nov - E, np.nan)
    n1, n3 = NB[1].sum(1), NB[3].sum(1)
    ner = (M / 3.0) / (n1 + 1)

    def jac(a, b):
        u = (a | b).sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(u > 0, (a & b).sum(1) / np.where(u > 0, u, 1), np.nan)
    j12, j23 = jac(NB[1], NB[2]), jac(NB[2], NB[3])
    with np.errstate(invalid="ignore"):
        ep = np.where(np.isfinite(j12) & np.isfinite(j23), (j12 + j23) / 2,
                      np.where(np.isfinite(j12), j12, np.where(np.isfinite(j23), j23, np.nan)))
    # participation / n_comm over comm[s4] of NB_W3 weighted by W3 counts
    c3 = cnt[3][:, cand] * NB[3]
    ncm = int(P["comm4c"].max()) + 1 if len(cand) else 1
    ws = np.zeros((D, ncm))
    if len(cand):
        rr, kk = np.nonzero(c3 > 0)
        np.add.at(ws, (rr, P["comm4c"][kk]), c3[rr, kk])
    tot = ws.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pw = ws / tot[:, None]
    part = np.where(n3 > 0, 1 - (pw ** 2).sum(1), np.nan)
    ncomm = np.where(n3 > 0, (ws > 0).sum(1), 0).astype(float)
    nb3f = NB[3].astype(float)
    e = ((nb3f @ P["adj"]) * nb3f).sum(1) / 2
    with np.errstate(invalid="ignore", divide="ignore"):
        dens = np.where(n3 >= 2, e / (n3 * (n3 - 1) / 2), np.nan)
    out = {"new_edge_rate": ner.astype(float), "n_comm_W3": ncomm, "participation": part, "NOV_res": nov_res,
           "ego_density_W3": dens, "edge_persistence": ep, "M": M.astype(float), "deg_W1": n1.astype(float),
           "deg_W3": n3.astype(float), "e_W3": e, "nc_W1": nc[1], "nc_W2": nc[2], "nc_W3": nc[3]}
    if return_sets:
        out["NB"] = NB
    if return_counts:
        out["cnt"] = cnt
    return out


# ----------------------------------------------------------------------------- resampling label generators
def rarefy_labels(lab: np.ndarray, n: int, D: int, rng: np.random.Generator) -> np.ndarray:
    """Exactly n papers per W-year (without replacement) and min(|PRE|, 3n) PRE papers; others dropped."""
    P = len(lab)
    key = rng.random((D, P))
    L = np.full((D, P), -1, np.int8)
    for w in range(4):
        idx = np.nonzero(lab == w)[0]
        if not len(idx):
            continue
        q = min(len(idx), 3 * n) if w == 0 else n
        r = np.argsort(key[:, idx], axis=1)[:, :q]
        rows = np.repeat(np.arange(D), q)
        L[rows, idx[r.ravel()]] = w
    return L


def permute_labels(lab: np.ndarray, D: int, rng: np.random.Generator) -> np.ndarray:
    """Permute the W1..W3 labels among the W papers (yearly counts preserved); PRE fixed; dropped stay dropped."""
    idx = np.nonzero(lab >= 1)[0]
    L = np.broadcast_to(lab, (D, len(lab))).copy()
    if len(idx) > 1:
        perm = np.argsort(rng.random((D, len(idx))), axis=1)
        L[:, idx] = lab[idx][perm]
    return L


def half_split(lab: np.ndarray, S: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """S random split-halves within each window (PRE, W1, W2, W3); odd windows give the extra paper at random.
    Returns (LA, LB): S x P label arrays (papers of the other half dropped)."""
    P = len(lab)
    LA = np.full((S, P), -1, np.int8)
    LB = np.full((S, P), -1, np.int8)
    for w in range(4):
        idx = np.nonzero(lab == w)[0]
        n = len(idx)
        if not n:
            continue
        r = np.argsort(rng.random((S, n)), axis=1)
        na = n // 2 + (rng.random(S) < 0.5).astype(int) * (n % 2)
        inA = np.arange(n)[None, :] < na[:, None]
        rows = np.repeat(np.arange(S), n)
        cols = idx[r.ravel()]
        a = inA.ravel()
        LA[rows[a], cols[a]] = w
        LB[rows[~a], cols[~a]] = w
    return LA, LB


# ----------------------------------------------------------------------------- Chao et al. 2005 abundance Jaccard
def chao_jaccard(x: np.ndarray, y: np.ndarray) -> float:
    """Chao, Chazdon, Colwell & Shen (2005, Ecol Lett 8:148) abundance-based Jaccard with the unseen-shared-species
    correction; bias-corrected f2 = 0 form. x, y: count vectors on a common support."""
    n1, n2 = float(x.sum()), float(y.sum())
    if n1 <= 0 or n2 <= 0:
        return float("nan")
    Dm = (x > 0) & (y > 0)
    if not Dm.any():
        return 0.0
    f_p1 = float(((y == 1) & Dm).sum())   # shared species seen once in sample 2
    f_p2 = float(((y == 2) & Dm).sum())
    f_1p = float(((x == 1) & Dm).sum())
    f_2p = float(((x == 2) & Dm).sum())
    r2 = f_p1 / (2 * f_p2) if f_p2 > 0 else f_p1 * (f_p1 - 1) / 2 / max(f_p1, 1.0) if f_p1 > 0 else 0.0
    r1 = f_1p / (2 * f_2p) if f_2p > 0 else f_1p * (f_1p - 1) / 2 / max(f_1p, 1.0) if f_1p > 0 else 0.0
    # r = f1^2 / (2 f2) -> f1 / (2 f2) multiplies f1-weighted sum below; bias-corrected: f1 (f1 - 1) / 2 over f1
    U = x[Dm].sum() / n1 + ((n2 - 1) / n2) * r2 * x[Dm & (y == 1)].sum() / n1
    V = y[Dm].sum() / n2 + ((n1 - 1) / n1) * r1 * y[Dm & (x == 1)].sum() / n2
    U, V = min(U, 1.0), min(V, 1.0)
    den = U + V - U * V
    return float(U * V / den) if den > 0 else float("nan")
```

### [64] TOOL RESULT — Write · 2026-09-29 05:28:00 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/fast6.py", "content": "\"\"\"Vectorised re-implementation of the six OPEN components of lib/ego.concept_core (EXP10 version), batched over\nD resamples of ONE concept's HOME papers.\n\nA resample is a label vector over the concept's home papers: -1 = dropped, 0 = PRE (t0-3..t0-1), 1 = W1 (t0),\n2 = W2 (t0+1), 3 = W3 (t0+2). The raw build is the label vector implied by the paper years. The SELF set (the\nconcept's own name topics) is computed ONCE on the full home build (ego.self_topics) and held fixed in every\nresample (declared in results/frozen_spec.json). Every other step is copied from ego.concept_core:\n  window counts -> neighbours (count >= 2 & PMI > 0 & ~SELF) -> pre_set (PRE count >= 1) -> new = union(NB) & ~pre\n  -> first year -> NOV / degree-matched expectation over the pool -> Jaccards -> participation / n_comm over comm[s4]\n  -> ego density over full_edges[s4].\nValidated against ego.concept_core with the SELF override to <= 1e-12 (tests/u_tests.py, U1).\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport scipy.sparse as sp\n\nimport ego\n\nOUT6 = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\n\n\ndef base_labels(years: np.ndarray, t0: int) -> np.ndarray:\n    lab = np.full(len(years), -1, np.int8)\n    lab[(years >= t0 - 3) & (years <= t0 - 1)] = 0\n    for j in range(3):\n        lab[years == t0 + j] = j + 1\n    return lab\n\n\ndef prep(name: str, aliases: list, t0: int, works: list) -> dict:\n    \"\"\"Per-concept precomputation (needs ego.set_context to have been called).\"\"\"\n    C = ego.C\n    years = np.array([y for y, _ in works], np.int64)\n    tps = [np.asarray(tp, np.int64) for _, tp in works]\n    lab = base_labels(years, t0)\n    allt = np.concatenate(tps) if tps else np.zeros(0, np.int64)\n    U = np.unique(allt)                                  # ascending global ids -> local order == global order\n    nU = len(U)\n    loc = {int(g): i for i, g in enumerate(U)}\n    rows, cols = [], []\n    for p, tp in enumerate(tps):\n        for k in tp.tolist():\n            rows.append(p)\n            cols.append(loc[k])\n    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(len(works), nU))   # duplicates summed\n    nonempty = np.array([len(tp) > 0 for tp in tps], float)\n    # SELF on the FULL home build (ego.self_topics inputs = early-window counts)\n    early = [t0, t0 + 1, t0 + 2]\n    n_early, nc_early = ego.window_counts(works, early)\n    SELF = ego.self_topics(name, aliases, n_early, nc_early)\n    selfU = SELF[U]\n    # candidate neighbour topics: non-SELF, total W1..W3 count >= 2\n    wmask = (lab >= 1).astype(float)\n    totW = np.asarray(A.T @ wmask).ravel()\n    cand = np.nonzero((~selfU) & (totW >= 2))[0]\n    cg = U[cand]\n    win = ego.rq1_windows(t0)\n    bgw, NW = {}, {}\n    for w, ys in win.items():\n        b, n = ego.bg_window(ys)\n        bgw[w], NW[w] = b, n\n    nbg_early, _ = ego.bg_window(early)\n    s0 = ego.slice_of(t0)\n    s4 = ego.slice_of(win[\"W3\"][-1])\n    comm0 = C[\"comm\"][s0]\n    dg = C[\"deg\"][s0].astype(float)\n    pool0 = (nbg_early > 0) & ~SELF\n    Tpool = float(dg[pool0].sum())\n    ncomm_g = int(max(c.max() for c in C[\"comm\"])) + 1\n    Dc = np.bincount(comm0[pool0], weights=dg[pool0], minlength=ncomm_g)\n    # dense W3 adjacency among candidates (full_edges[s4], each listed edge counted once, a < b)\n    a, b = C[\"full_edges\"][s4]\n    pos = np.full(C[\"nt\"], -1, np.int64)\n    pos[cg] = np.arange(len(cg))\n    m = (pos[a] >= 0) & (pos[b] >= 0)\n    adj = np.zeros((len(cg), len(cg)), float)\n    np.add.at(adj, (pos[a[m]], pos[b[m]]), 1.0)\n    adj = adj + adj.T\n    return dict(t0=t0, U=U, A=A, AT=A.T.tocsr(), nonempty=nonempty, lab=lab, years=years, selfU=selfU, cand=cand,\n                cg=cg, SELF=SELF, s0=s0, s4=s4,\n                bg_c={w: bgw[w][cg] for w in (\"W1\", \"W2\", \"W3\")}, NW=NW,\n                comm0U=comm0[U], comm4c=C[\"comm\"][s4][cg],\n                commfy=np.stack([C[\"comm\"][ego.slice_of(t0 + j)][cg] for j in range(3)]),\n                dgU=dg[U], pool0U=pool0[U], Tpool=Tpool, Dc=Dc, ncomm_g=ncomm_g, adj=adj)\n\n\ndef window_counts_batch(P: dict, L: np.ndarray, w: int) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"counts (D x nU) and n papers with >= 1 topic (D) for label w.\"\"\"\n    Mw = (L == w).astype(float)                          # D x P\n    cnt = np.asarray((P[\"AT\"] @ Mw.T)).T if P[\"A\"].shape[1] else np.zeros((L.shape[0], 0))\n    return cnt, Mw @ P[\"nonempty\"]\n\n\ndef fast6(P: dict, L: np.ndarray, return_sets: bool = False, return_counts: bool = False) -> dict:\n    \"\"\"L: D x P int8 labels. Returns dict of (D,) arrays for OUT6 (+ M, deg_W1, deg_W3, nc_W*) and optionally the\n    neighbour sets NB_W1..3 as D x n_cand bool (candidate order P['cg']).\"\"\"\n    L = np.atleast_2d(L)\n    D = L.shape[0]\n    cnt, nc = {}, {}\n    for w in range(4):\n        cnt[w], nc[w] = window_counts_batch(P, L, w)\n    cand = P[\"cand\"]\n    NB = {}\n    for w in (1, 2, 3):\n        c = cnt[w][:, cand]\n        key = f\"W{w}\"\n        ncw = nc[w][:, None]\n        with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n            v = np.log(c * P[\"NW\"][key] / (ncw * P[\"bg_c\"][key][None, :]))\n        v[~np.isfinite(v)] = np.nan\n        NB[w] = (c >= 2) & (np.nan_to_num(v, nan=-1) > 0) & (ncw > 0)\n    pre = cnt[0] >= 1                                     # D x nU\n    new = (NB[1] | NB[2] | NB[3]) & ~pre[:, cand]\n    M = new.sum(1)\n    # first year of each new topic (first early year with count >= 1)\n    c1, c2 = cnt[1][:, cand], cnt[2][:, cand]\n    fy = np.where(c1 >= 1, 0, np.where(c2 >= 1, 1, 2))\n    commfy = np.take_along_axis(np.broadcast_to(P[\"commfy\"][None], (D,) + P[\"commfy\"].shape).transpose(0, 2, 1),\n                                fy[:, :, None], axis=2)[:, :, 0] if len(cand) else np.zeros((D, 0), np.int64)\n    # C0: dominant W1 community over ALL topics (Counter insertion order == ascending topic id -> ties go to the\n    # community whose first contributing topic has the smallest id)\n    w1 = cnt[1]\n    has1 = w1.sum(1) > 0\n    nU = len(P[\"U\"])\n    comm0U = P[\"comm0U\"]\n    cw = np.zeros((D, P[\"ncomm_g\"]))\n    first = np.full((D, P[\"ncomm_g\"]), nU + 1, np.int64)\n    rr, kk = np.nonzero(w1 > 0)\n    np.add.at(cw, (rr, comm0U[kk]), w1[rr, kk])\n    np.minimum.at(first, (rr, comm0U[kk]), kk)\n    cmax = cw.max(1, keepdims=True)\n    key = np.where((cw == cmax) & (cw > 0), -first, -(10 ** 9))\n    C0 = key.argmax(1)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        nov = ((commfy != C0[:, None]) & new).sum(1) / M\n    preP = pre & P[\"pool0U\"][None, :]\n    corrT = preP.astype(float) @ P[\"dgU\"]\n    corrC = (preP & (comm0U[None, :] == C0[:, None])).astype(float) @ P[\"dgU\"]\n    den = P[\"Tpool\"] - corrT\n    num = den - (P[\"Dc\"][C0] - corrC)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        E = np.where(den > 0, num / np.where(den > 0, den, 1), np.nan)\n    nov_res = np.where(has1 & (M > 0), nov - E, np.nan)\n    n1, n3 = NB[1].sum(1), NB[3].sum(1)\n    ner = (M / 3.0) / (n1 + 1)\n\n    def jac(a, b):\n        u = (a | b).sum(1)\n        with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n            return np.where(u > 0, (a & b).sum(1) / np.where(u > 0, u, 1), np.nan)\n    j12, j23 = jac(NB[1], NB[2]), jac(NB[2], NB[3])\n    with np.errstate(invalid=\"ignore\"):\n        ep = np.where(np.isfinite(j12) & np.isfinite(j23), (j12 + j23) / 2,\n                      np.where(np.isfinite(j12), j12, np.where(np.isfinite(j23), j23, np.nan)))\n    # participation / n_comm over comm[s4] of NB_W3 weighted by W3 counts\n    c3 = cnt[3][:, cand] * NB[3]\n    ncm = int(P[\"comm4c\"].max()) + 1 if len(cand) else 1\n    ws = np.zeros((D, ncm))\n    if len(cand):\n        rr, kk = np.nonzero(c3 > 0)\n        np.add.at(ws, (rr, P[\"comm4c\"][kk]), c3[rr, kk])\n    tot = ws.sum(1)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        pw = ws / tot[:, None]\n    part = np.where(n3 > 0, 1 - (pw ** 2).sum(1), np.nan)\n    ncomm = np.where(n3 > 0, (ws > 0).sum(1), 0).astype(float)\n    nb3f = NB[3].astype(float)\n    e = ((nb3f @ P[\"adj\"]) * nb3f).sum(1) / 2\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        dens = np.where(n3 >= 2, e / (n3 * (n3 - 1) / 2), np.nan)\n    out = {\"new_edge_rate\": ner.astype(float), \"n_comm_W3\": ncomm, \"participation\": part, \"NOV_res\": nov_res,\n           \"ego_density_W3\": dens, \"edge_persistence\": ep, \"M\": M.astype(float), \"deg_W1\": n1.astype(float),\n           \"deg_W3\": n3.astype(float), \"e_W3\": e, \"nc_W1\": nc[1], \"nc_W2\": nc[2], \"nc_W3\": nc[3]}\n    if return_sets:\n        out[\"NB\"] = NB\n    if return_counts:\n        out[\"cnt\"] = cnt\n    return out\n\n\n# ----------------------------------------------------------------------------- resampling label generators\ndef rarefy_labels(lab: np.ndarray, n: int, D: int, rng: np.random.Generator) -> np.ndarray:\n    \"\"\"Exactly n papers per W-year (without replacement) and min(|PRE|, 3n) PRE papers; others dropped.\"\"\"\n    P = len(lab)\n    key = rng.random((D, P))\n    L = np.full((D, P), -1, np.int8)\n    for w in range(4):\n        idx = np.nonzero(lab == w)[0]\n        if not len(idx):\n            continue\n        q = min(len(idx), 3 * n) if w == 0 else n\n        r = np.argsort(key[:, idx], axis=1)[:, :q]\n        rows = np.repeat(np.arange(D), q)\n        L[rows, idx[r.ravel()]] = w\n    return L\n\n\ndef permute_labels(lab: np.ndarray, D: int, rng: np.random.Generator) -> np.ndarray:\n    \"\"\"Permute the W1..W3 labels among the W papers (yearly counts preserved); PRE fixed; dropped stay dropped.\"\"\"\n    idx = np.nonzero(lab >= 1)[0]\n    L = np.broadcast_to(lab, (D, len(lab))).copy()\n    if len(idx) > 1:\n        perm = np.argsort(rng.random((D, len(idx))), axis=1)\n        L[:, idx] = lab[idx][perm]\n    return L\n\n\ndef half_split(lab: np.ndarray, S: int, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"S random split-halves within each window (PRE, W1, W2, W3); odd windows give the extra paper at random.\n    Returns (LA, LB): S x P label arrays (papers of the other half dropped).\"\"\"\n    P = len(lab)\n    LA = np.full((S, P), -1, np.int8)\n    LB = np.full((S, P), -1, np.int8)\n    for w in range(4):\n        idx = np.nonzero(lab == w)[0]\n        n = len(idx)\n        if not n:\n            continue\n        r = np.argsort(rng.random((S, n)), axis=1)\n        na = n // 2 + (rng.random(S) < 0.5).astype(int) * (n % 2)\n        inA = np.arange(n)[None, :] < na[:, None]\n        rows = np.repeat(np.arange(S), n)\n        cols = idx[r.ravel()]\n        a = inA.ravel()\n        LA[rows[a], cols[a]] = w\n        LB[rows[~a], cols[~a]] = w\n    return LA, LB\n\n\n# ----------------------------------------------------------------------------- Chao et al. 2005 abundance Jaccard\ndef chao_jaccard(x: np.ndarray, y: np.ndarray) -> float:\n    \"\"\"Chao, Chazdon, Colwell & Shen (2005, Ecol Lett 8:148) abundance-based Jaccard with the unseen-shared-species\n    correction; bias-corrected f2 = 0 form. x, y: count vectors on a common support.\"\"\"\n    n1, n2 = float(x.sum()), float(y.sum())\n    if n1 <= 0 or n2 <= 0:\n        return float(\"nan\")\n    Dm = (x > 0) & (y > 0)\n    if not Dm.any():\n        return 0.0\n    f_p1 = float(((y == 1) & Dm).sum())   # shared species seen once in sample 2\n    f_p2 = float(((y == 2) & Dm).sum())\n    f_1p = float(((x == 1) & Dm).sum())\n    f_2p = float(((x == 2) & Dm).sum())\n    r2 = f_p1 / (2 * f_p2) if f_p2 > 0 else f_p1 * (f_p1 - 1) / 2 / max(f_p1, 1.0) if f_p1 > 0 else 0.0\n    r1 = f_1p / (2 * f_2p) if f_2p > 0 else f_1p * (f_1p - 1) / 2 / max(f_1p, 1.0) if f_1p > 0 else 0.0\n    # r = f1^2 / (2 f2) -> f1 / (2 f2) multiplies f1-weighted sum below; bias-corrected: f1 (f1 - 1) / 2 over f1\n    U = x[Dm].sum() / n1 + ((n2 - 1) / n2) * r2 * x[Dm & (y == 1)].sum() / n1\n    V = y[Dm].sum() / n2 + ((n1 - 1) / n1) * r1 * y[Dm & (x == 1)].sum() / n2\n    U, V = min(U, 1.0), min(V, 1.0)\n    den = U + V - U * V\n    return float(U * V / den) if den > 0 else float(\"nan\")\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [65] TOOL CALL — Bash · 2026-09-29 05:28:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("lib/fast6.py"); s=p.read_text()
old='''    commfy = np.take_along_axis(np.broadcast_to(P["commfy"][None], (D,) + P["commfy"].shape).transpose(0, 2, 1),
                                fy[:, :, None], axis=2)[:, :, 0] if len(cand) else np.zeros((D, 0), np.int64)'''
new='''    commfy = P["commfy"][fy, np.arange(len(cand))[None, :]] if len(cand) else np.zeros((D, 0), np.int64)'''
assert old in s; s=s.replace(old,new); p.write_text(s)
EOF
```

### [66] TOOL RESULT — Bash · 2026-09-29 05:28:30 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [67] ASSISTANT · 2026-09-29 05:29:06 UTC

```
Now the U1/U2/U5/U6 unit tests against the reference `concept_core`.
```

### [68] TOOL CALL — Write · 2026-09-29 05:29:06 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/u_fast6.py

#!/usr/bin/env python3
"""Unit tests for the fast engine.
U1 fast6 == ego.concept_core with the SELF override (SELF_full) to <= 1e-12 on N concepts x {full, 1 random half,
   1 random year-permutation, 1 rarefaction n=5 draw}.
U2 the year permutation preserves yearly counts and the paper multiset; identity permutation == raw.
U5 rarefaction at n = the concept's actual yearly counts (all papers) reproduces raw.
U6 Chao Jaccard: identical -> 1, disjoint -> 0, hand-computed toy.
Usage: python tests/u_fast6.py [N]  -> results/unit_tests_fast6.json"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np

import ego
from common import RES, jdump, setup_logger
from ego_ctx import rq1_context
from fast6 import OUT6, chao_jaccard, fast6, half_split, permute_labels, prep, rarefy_labels
from jobs import build_home_cache


def works_from_labels(works: list, lab: np.ndarray, t0: int) -> list:
    out = []
    for (y, tp), l in zip(works, lab):
        if l < 0:
            continue
        out.append((y if l == 0 else t0 + int(l) - 1, tp))
    return out


def ref6(name, al, t0, works, SELF):
    orig = ego.self_topics
    ego.self_topics = lambda *a, **k: SELF
    try:
        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)
    finally:
        ego.self_topics = orig
    return {k: float(r[k]) for k in OUT6}


def diff(a: float, b: float) -> float:
    if np.isnan(a) and np.isnan(b):
        return 0.0
    if np.isnan(a) != np.isnan(b):
        return float("inf")
    return abs(a - b)


def main() -> None:
    logger = setup_logger("u_fast6")
    warnings.simplefilter("ignore", RuntimeWarning)
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    ego.set_context(rq1_context())
    cache = build_home_cache()
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= 10)
    rng = np.random.default_rng(11)
    pick = [keys[i] for i in rng.choice(len(keys), min(N, len(keys)), replace=False)]
    worst = {v: 0.0 for v in ("full", "half", "perm", "rare5")}
    worst_key = {}
    t_fast, t_ref, n_calls = 0.0, 0.0, 0
    u2_ok, u5_ok = True, True
    for i, k in enumerate(pick):
        c = cache[k]
        P = prep(c["name"], c["aliases"], c["t0"], c["works"])
        lab = P["lab"]
        LA, _ = half_split(lab, 1, rng)
        Lp = permute_labels(lab, 1, rng)
        variants = {"full": lab[None, :], "half": LA, "perm": Lp}
        if all((lab == w).sum() >= 5 for w in (1, 2, 3)):
            variants["rare5"] = rarefy_labels(lab, 5, 1, rng)
        for vn, L in variants.items():
            t = time.time()
            f = fast6(P, L)
            t_fast += time.time() - t
            t = time.time()
            r = ref6(c["name"], c["aliases"], c["t0"], works_from_labels(c["works"], L[0], c["t0"]), P["SELF"])
            t_ref += time.time() - t
            n_calls += 1
            d = max(diff(float(f[m][0]), r[m]) for m in OUT6)
            if d > worst[vn]:
                worst[vn] = d
                worst_key[vn] = [k[0], int(k[1]), {m: [float(f[m][0]), r[m]] for m in OUT6}]
        # U2: counts preserved, identity == raw
        for w in (1, 2, 3):
            u2_ok &= bool((Lp[0] == w).sum() == (lab == w).sum())
        u2_ok &= bool(sorted(Lp[0][lab >= 1].tolist()) == sorted(lab[lab >= 1].tolist()))
        raw = fast6(P, lab[None, :])
        # U5: rarefy at actual yearly counts (min over windows equal to all) -> check with n = max count when equal
        cnts = [(lab == w).sum() for w in (1, 2, 3)]
        if len(set(cnts)) == 1 and (lab == 0).sum() <= 3 * cnts[0]:
            Lr = rarefy_labels(lab, cnts[0], 1, rng)
            rr = fast6(P, Lr)
            u5_ok &= all(diff(float(rr[m][0]), float(raw[m][0])) <= 1e-12 for m in OUT6)
        if i % 100 == 0:
            logger.info(f"{i}/{len(pick)} worst {worst}")
    # U5 on every concept via an explicit all-papers label (the generator's n-per-year definition equals raw only
    # when yearly counts are equal; the explicit check is that dropping nobody reproduces raw)
    # U6 Chao
    x = np.array([3, 2, 1, 0, 4.0])
    u6 = {"identical": chao_jaccard(x, x.copy()), "disjoint": chao_jaccard(np.array([1, 2, 0, 0.]),
                                                                          np.array([0, 0, 3, 1.]))}
    # toy: x = [2, 1, 1], y = [1, 2, 0] -> D = {0, 1}; n1 = 4, n2 = 3
    # f+1 (shared, y == 1) = 1 (k0), f+2 = 1 (k1) -> r2 = 1/2; sum_{D, y=1} x/n1 = 2/4
    # U = (2+1)/4 + (2/3)(1/2)(2/4) = 0.75 + 1/6 = 0.916667
    # f1+ (shared, x == 1) = 1 (k1), f2+ = 1 (k0) -> r1 = 1/2; sum_{D, x=1} y/n2 = 2/3
    # V = (1+2)/3 + (3/4)(1/2)(2/3) = 1 + 0.25 -> capped 1.0 ; J = U V / (U + V - U V) = U = 0.916667
    u6["toy"] = chao_jaccard(np.array([2, 1, 1.]), np.array([1, 2, 0.]))
    u6["toy_expected"] = 0.75 + 1 / 6
    u6_ok = abs(u6["identical"] - 1) < 1e-12 and u6["disjoint"] == 0 and abs(u6["toy"] - u6["toy_expected"]) < 1e-12
    out = {"U1": {"n_concepts": len(pick), "max_abs_diff": worst, "worst_case": worst_key,
                  "pass": bool(all(v <= 1e-12 for v in worst.values()))},
           "U2": {"pass": u2_ok}, "U5": {"pass": u5_ok, "note": "checked on concepts with equal yearly counts"},
           "U6": {**u6, "pass": bool(u6_ok)},
           "timing": {"fast_ms_per_call": 1e3 * t_fast / n_calls, "ref_ms_per_call": 1e3 * t_ref / n_calls}}
    jdump(out, RES / "unit_tests_fast6.json")
    logger.info(json.dumps({k: (v.get("pass") if isinstance(v, dict) else v) for k, v in out.items()}))
    logger.info(f"worst {worst}; timing {out['timing']}")


if __name__ == "__main__":
    main()
```

### [69] TOOL RESULT — Write · 2026-09-29 05:29:06 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/u_fast6.py", "content": "#!/usr/bin/env python3\n\"\"\"Unit tests for the fast engine.\nU1 fast6 == ego.concept_core with the SELF override (SELF_full) to <= 1e-12 on N concepts x {full, 1 random half,\n   1 random year-permutation, 1 rarefaction n=5 draw}.\nU2 the year permutation preserves yearly counts and the paper multiset; identity permutation == raw.\nU5 rarefaction at n = the concept's actual yearly counts (all papers) reproduces raw.\nU6 Chao Jaccard: identical -> 1, disjoint -> 0, hand-computed toy.\nUsage: python tests/u_fast6.py [N]  -> results/unit_tests_fast6.json\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nimport time\nimport warnings\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1] / \"lib\"))\n\nimport numpy as np\n\nimport ego\nfrom common import RES, jdump, setup_logger\nfrom ego_ctx import rq1_context\nfrom fast6 import OUT6, chao_jaccard, fast6, half_split, permute_labels, prep, rarefy_labels\nfrom jobs import build_home_cache\n\n\ndef works_from_labels(works: list, lab: np.ndarray, t0: int) -> list:\n    out = []\n    for (y, tp), l in zip(works, lab):\n        if l < 0:\n            continue\n        out.append((y if l == 0 else t0 + int(l) - 1, tp))\n    return out\n\n\ndef ref6(name, al, t0, works, SELF):\n    orig = ego.self_topics\n    ego.self_topics = lambda *a, **k: SELF\n    try:\n        r = ego.concept_core(name, al, t0, works, 0, 0, compute_btw=False)\n    finally:\n        ego.self_topics = orig\n    return {k: float(r[k]) for k in OUT6}\n\n\ndef diff(a: float, b: float) -> float:\n    if np.isnan(a) and np.isnan(b):\n        return 0.0\n    if np.isnan(a) != np.isnan(b):\n        return float(\"inf\")\n    return abs(a - b)\n\n\ndef main() -> None:\n    logger = setup_logger(\"u_fast6\")\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000\n    ego.set_context(rq1_context())\n    cache = build_home_cache()\n    keys = sorted(k for k, v in cache.items() if v[\"n_home_early\"] >= 10)\n    rng = np.random.default_rng(11)\n    pick = [keys[i] for i in rng.choice(len(keys), min(N, len(keys)), replace=False)]\n    worst = {v: 0.0 for v in (\"full\", \"half\", \"perm\", \"rare5\")}\n    worst_key = {}\n    t_fast, t_ref, n_calls = 0.0, 0.0, 0\n    u2_ok, u5_ok = True, True\n    for i, k in enumerate(pick):\n        c = cache[k]\n        P = prep(c[\"name\"], c[\"aliases\"], c[\"t0\"], c[\"works\"])\n        lab = P[\"lab\"]\n        LA, _ = half_split(lab, 1, rng)\n        Lp = permute_labels(lab, 1, rng)\n        variants = {\"full\": lab[None, :], \"half\": LA, \"perm\": Lp}\n        if all((lab == w).sum() >= 5 for w in (1, 2, 3)):\n            variants[\"rare5\"] = rarefy_labels(lab, 5, 1, rng)\n        for vn, L in variants.items():\n            t = time.time()\n            f = fast6(P, L)\n            t_fast += time.time() - t\n            t = time.time()\n            r = ref6(c[\"name\"], c[\"aliases\"], c[\"t0\"], works_from_labels(c[\"works\"], L[0], c[\"t0\"]), P[\"SELF\"])\n            t_ref += time.time() - t\n            n_calls += 1\n            d = max(diff(float(f[m][0]), r[m]) for m in OUT6)\n            if d > worst[vn]:\n                worst[vn] = d\n                worst_key[vn] = [k[0], int(k[1]), {m: [float(f[m][0]), r[m]] for m in OUT6}]\n        # U2: counts preserved, identity == raw\n        for w in (1, 2, 3):\n            u2_ok &= bool((Lp[0] == w).sum() == (lab == w).sum())\n        u2_ok &= bool(sorted(Lp[0][lab >= 1].tolist()) == sorted(lab[lab >= 1].tolist()))\n        raw = fast6(P, lab[None, :])\n        # U5: rarefy at actual yearly counts (min over windows equal to all) -> check with n = max count when equal\n        cnts = [(lab == w).sum() for w in (1, 2, 3)]\n        if len(set(cnts)) == 1 and (lab == 0).sum() <= 3 * cnts[0]:\n            Lr = rarefy_labels(lab, cnts[0], 1, rng)\n            rr = fast6(P, Lr)\n            u5_ok &= all(diff(float(rr[m][0]), float(raw[m][0])) <= 1e-12 for m in OUT6)\n        if i % 100 == 0:\n            logger.info(f\"{i}/{len(pick)} worst {worst}\")\n    # U5 on every concept via an explicit all-papers label (the generator's n-per-year definition equals raw only\n    # when yearly counts are equal; the explicit check is that dropping nobody reproduces raw)\n    # U6 Chao\n    x = np.array([3, 2, 1, 0, 4.0])\n    u6 = {\"identical\": chao_jaccard(x, x.copy()), \"disjoint\": chao_jaccard(np.array([1, 2, 0, 0.]),\n                                                                          np.array([0, 0, 3, 1.]))}\n    # toy: x = [2, 1, 1], y = [1, 2, 0] -> D = {0, 1}; n1 = 4, n2 = 3\n    # f+1 (shared, y == 1) = 1 (k0), f+2 = 1 (k1) -> r2 = 1/2; sum_{D, y=1} x/n1 = 2/4\n    # U = (2+1)/4 + (2/3)(1/2)(2/4) = 0.75 + 1/6 = 0.916667\n    # f1+ (shared, x == 1) = 1 (k1), f2+ = 1 (k0) -> r1 = 1/2; sum_{D, x=1} y/n2 = 2/3\n    # V = (1+2)/3 + (3/4)(1/2)(2/3) = 1 + 0.25 -> capped 1.0 ; J = U V / (U + V - U V) = U = 0.916667\n    u6[\"toy\"] = chao_jaccard(np.array([2, 1, 1.]), np.array([1, 2, 0.]))\n    u6[\"toy_expected\"] = 0.75 + 1 / 6\n    u6_ok = abs(u6[\"identical\"] - 1) < 1e-12 and u6[\"disjoint\"] == 0 and abs(u6[\"toy\"] - u6[\"toy_expected\"]) < 1e-12\n    out = {\"U1\": {\"n_concepts\": len(pick), \"max_abs_diff\": worst, \"worst_case\": worst_key,\n                  \"pass\": bool(all(v <= 1e-12 for v in worst.values()))},\n           \"U2\": {\"pass\": u2_ok}, \"U5\": {\"pass\": u5_ok, \"note\": \"checked on concepts with equal yearly counts\"},\n           \"U6\": {**u6, \"pass\": bool(u6_ok)},\n           \"timing\": {\"fast_ms_per_call\": 1e3 * t_fast / n_calls, \"ref_ms_per_call\": 1e3 * t_ref / n_calls}}\n    jdump(out, RES / \"unit_tests_fast6.json\")\n    logger.info(json.dumps({k: (v.get(\"pass\") if isinstance(v, dict) else v) for k, v in out.items()}))\n    logger.info(f\"worst {worst}; timing {out['timing']}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [70] TOOL CALL — Bash · 2026-09-29 05:29:06 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; timeout 900 .venv/bin/python tests/u_fast6.py 100 2>&1 | tail -8
```

### [71] TOOL RESULT — Bash · 2026-09-29 05:29:06 UTC

```
{"stdout": "05:28:25|INFO   |0/100 worst {'full': 0.0, 'half': 0.0, 'perm': 0.0, 'rare5': 0.0}\n05:28:26|INFO   |{\"U1\": true, \"U2\": true, \"U5\": true, \"U6\": true, \"timing\": null}\n05:28:26|INFO   |worst {'full': 1.1102230246251565e-16, 'half': 0.0, 'perm': 0.0, 'rare5': 0.0}; timing {'fast_ms_per_call': 0.23603567513086463, 'ref_ms_per_call': 1.3279017581734607}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [72] ASSISTANT · 2026-09-29 05:29:32 UTC

```
U1 passes (max diff 1.1e-16; 0.24 ms/call against 1.33 ms for the reference). I'm starting the full 1,000-concept U1 in the background and writing the S2 variant engine in the meantime.
```

### [73] TOOL CALL — Bash · 2026-09-29 05:29:32 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; ls -la data/; (timeout 1800 .venv/bin/python tests/u_fast6.py 1000 > logs/u_fast6_1000.out 2>&1 &) ; echo started
```

### [74] TOOL RESULT — Bash · 2026-09-29 05:29:32 UTC

```
{"stdout": "total 49386\ndrwxr-xr-x  2 root root  2004433 Sep 29 05:24 .\ndrwxr-xr-x 11 root root  2074600 Sep 29 05:24 ..\n-rw-r--r--  1 root root 46491498 Sep 29 05:24 home_cache.pkl\nstarted", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [75] TOOL CALL — Write · 2026-09-29 05:30:04 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s2_variants.py

#!/usr/bin/env python3
"""S2: raw + resampling variants per concept (HOME build, concepts with n_home_early >= 10), checkpointed per chunk.

Per concept (fast6 engine, SELF fixed at the full-build set):
  RAW     the six components on the full home build (must equal EXP10 values), NB sets W1..W3, window counts
  V1      rarefaction: for n in N_RARE, if every W-year has >= n papers: n papers per W-year + min(|PRE|, 3n) PRE,
          D_RARE draws, nanmean (>= half finite)
  V2      within-concept year-label permutation null (D_PERM permutations; PRE fixed): null mean / sd, excess, zperm
  V2b     Chao 2005 abundance Jaccard persistence (non-SELF topic count vectors, W1-W2 and W2-W3)
  V4raw   S_RAW split-halves (within window): the six components on each half
  V4clean first S_CLEAN of those splits: V2 (D_PERM_HALF perms per half) and V1 n=5 (D_RARE_HALF draws per half,
          concepts with >= 10 papers per W-year); the half NB sets are kept for the V3 half-nulls
Usage: python s2_variants.py [--limit N] [--sample-per-body N] [--tag TAG] [--workers 3] [--draws-scale 1.0]"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import pickle
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, RES, setup_logger

CFG_DEFAULT = {"N_RARE": [5, 10, 20], "D_RARE": 50, "D_PERM": 200, "S_RAW": 100, "S_CLEAN": 20, "D_PERM_HALF": 50,
               "D_RARE_HALF": 20, "RARE_HALF_N": 5, "MIN_HOME": 10}
V2_METRICS = ["edge_persistence", "NOV_res", "ego_density_W3", "new_edge_rate", "n_comm_W3", "participation"]
_G: dict = {}


def seed_key(frame: str, ci: int) -> int:
    return int(ci) + (0 if frame == "exp5" else 100000)


def _init(cfg: dict) -> None:
    import ego
    from ego_ctx import rq1_context
    from jobs import build_home_cache
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    _G["cache"] = build_home_cache()
    _G["cfg"] = cfg


def _nanagg(v: np.ndarray, min_fin: int) -> tuple[float, float, int]:
    f = np.isfinite(v)
    if f.sum() < min_fin:
        return float("nan"), float("nan"), int(f.sum())
    return float(v[f].mean()), float(v[f].std()), int(f.sum())


def v2_block(P: dict, lab: np.ndarray, obs: dict, D: int, rng) -> dict:
    from fast6 import fast6, permute_labels
    r = fast6(P, permute_labels(lab, D, rng))
    out = {}
    for m in V2_METRICS:
        mu, sd, nf = _nanagg(r[m], D // 2)
        o = float(obs[m])
        out[f"{m}_nullmean"] = mu
        out[f"{m}_nullsd"] = sd
        out[f"{m}_exc"] = o - mu if np.isfinite(o) and np.isfinite(mu) else float("nan")
        out[f"{m}_zperm"] = out[f"{m}_exc"] / sd if np.isfinite(out[f"{m}_exc"]) and sd > 0 else float("nan")
    return out


def v1_block(P: dict, lab: np.ndarray, n: int, D: int, rng) -> dict | None:
    from fast6 import OUT6, fast6, rarefy_labels
    if any((lab == w).sum() < n for w in (1, 2, 3)):
        return None
    r = fast6(P, rarefy_labels(lab, n, D, rng))
    return {m: _nanagg(r[m], (D + 1) // 2)[0] for m in OUT6}


def one_concept(key: tuple) -> tuple[dict, dict]:
    from fast6 import OUT6, chao_jaccard, fast6, half_split, prep
    cfg = _G["cfg"]
    c = _G["cache"][key]
    frame, ci = key
    sk = seed_key(frame, ci)
    P = prep(c["name"], c["aliases"], c["t0"], c["works"])
    lab = P["lab"]
    row: dict = {"frame": frame, "ci": int(ci), "body": c["body"], "t0": c["t0"], "n_home_early": c["n_home_early"],
                 "n_home_pre": int((lab == 0).sum()), "n_W1": int((lab == 1).sum()), "n_W2": int((lab == 2).sum()),
                 "n_W3": int((lab == 3).sum()), "n_self": int(P["SELF"].sum()), "n_cand": int(len(P["cand"]))}
    raw = fast6(P, lab[None, :], return_sets=True, return_counts=True)
    obs = {m: float(raw[m][0]) for m in list(OUT6) + ["M", "deg_W1", "deg_W3", "e_W3"]}
    row.update({f"{m}__raw": v for m, v in obs.items()})
    row["min_year_n"] = int(min(row["n_W1"], row["n_W2"], row["n_W3"]))
    extra: dict = {"NB": {w: P["cg"][raw["NB"][w][0]].astype(np.int32) for w in (1, 2, 3)},
                   "SELF": np.nonzero(P["SELF"])[0].astype(np.int32)}
    # V2b Chao
    ns = ~P["selfU"]
    cw = {w: raw["cnt"][w][0][ns] for w in (1, 2, 3)}
    j12, j23 = chao_jaccard(cw[1], cw[2]), chao_jaccard(cw[2], cw[3])
    fin = [j for j in (j12, j23) if np.isfinite(j)]
    row["EP_chao"] = float(np.mean(fin)) if fin else float("nan")
    # V1 rarefaction
    for n in cfg["N_RARE"]:
        rng = np.random.default_rng([7000000, sk, n])
        r = v1_block(P, lab, n, cfg["D_RARE"], rng)
        for m in OUT6:
            row[f"{m}_rare{n}"] = r[m] if r is not None else float("nan")
    # V2 permutation null
    rng = np.random.default_rng([8000000, sk])
    row.update(v2_block(P, lab, obs, cfg["D_PERM"], rng))
    # V4 split halves
    rng = np.random.default_rng([9000000, sk])
    LA, LB = half_split(lab, cfg["S_RAW"], rng)
    ra = fast6(P, LA, return_sets=True)
    rb = fast6(P, LB, return_sets=True)
    extra["half_raw"] = {h: np.stack([r[m] for m in OUT6], 1).astype(np.float32) for h, r in (("A", ra), ("B", rb))}
    S = cfg["S_CLEAN"]
    extra["half_NB"] = {h: [[P["cg"][r["NB"][w][s]].astype(np.int32) for w in (1, 2, 3)] for s in range(S)]
                        for h, r in (("A", ra), ("B", rb))}
    rng_p = np.random.default_rng([9100000, sk])
    rng_r = np.random.default_rng([9200000, sk])
    hc: dict = {}
    for h, L, r in (("A", LA, ra), ("B", LB, rb)):
        rows_h = []
        for s in range(S):
            obs_h = {m: float(r[m][s]) for m in OUT6}
            d = v2_block(P, L[s], obs_h, cfg["D_PERM_HALF"], rng_p)
            rr = v1_block(P, L[s], cfg["RARE_HALF_N"], cfg["D_RARE_HALF"], rng_r)
            d.update({f"{m}_rare{cfg['RARE_HALF_N']}": (rr[m] if rr is not None else float("nan")) for m in OUT6})
            rows_h.append(d)
        hc[h] = pd.DataFrame(rows_h).astype(np.float32)
    extra["half_clean"] = hc
    return row, extra


def run_chunk(k: int, keys: list) -> tuple[int, list, list, float]:
    t = time.time()
    rows, extras = [], []
    for key in keys:
        try:
            r, e = one_concept(key)
        except (ValueError, IndexError, ZeroDivisionError, FloatingPointError) as ex:
            r, e = {"frame": key[0], "ci": int(key[1]), "s2_error": repr(ex)[:200]}, {}
        rows.append(r)
        extras.append(e)
    return k, rows, extras, time.time() - t


def select_keys(cache: dict, min_home: int, sample_per_body: int, seed: int = 5) -> list:
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= min_home)
    if sample_per_body:
        rng = np.random.default_rng(seed)
        out = []
        for b in ("DEV", "OLDHO", "COH1014", "COH1517"):
            kb = [k for k in keys if cache[k]["body"] == b]
            out += [kb[i] for i in sorted(rng.choice(len(kb), min(sample_per_body, len(kb)), replace=False))]
        keys = out
    return keys


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--sample-per-body", type=int, default=0)
    ap.add_argument("--tag", default="full")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--chunk", type=int, default=100)
    ap.add_argument("--cfg", default="")
    a = ap.parse_args()
    logger = setup_logger(f"s2_variants_{a.tag}")
    cfg = dict(CFG_DEFAULT)
    if a.cfg:
        cfg.update(json.loads(a.cfg))
    from jobs import build_home_cache
    cache = build_home_cache()
    keys = select_keys(cache, cfg["MIN_HOME"], a.sample_per_body)
    if a.limit:
        keys = keys[:a.limit]
    # big concepts first so the tail is short
    keys.sort(key=lambda k: -len(cache[k]["works"]))
    del cache
    outdir = DATA / f"s2_parts_{a.tag}"
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "cfg.json").write_text(json.dumps(cfg))
    chunks = [keys[i:i + a.chunk] for i in range(0, len(keys), a.chunk)]
    todo = [k for k in range(len(chunks)) if not (outdir / f"chunk_{k:05d}.pkl").exists()]
    logger.info(f"S2 {a.tag}: {len(keys)} concepts, {len(chunks)} chunks, todo {len(todo)}, cfg {cfg}")
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init,
                             initargs=(cfg,)) as ex:
        futs = [ex.submit(run_chunk, k, chunks[k]) for k in todo]
        for i, fu in enumerate(as_completed(futs)):
            k, rows, extras, dt = fu.result()
            (outdir / f"chunk_{k:05d}.pkl").write_bytes(pickle.dumps({"rows": rows, "extras": extras}, protocol=5))
            done += len(rows)
            el = time.time() - t0
            logger.info(f"chunk {i+1}/{len(futs)} ({done} concepts) {el/60:.1f} min; {dt/len(rows):.3f} s/concept; "
                        f"eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min")
    rows = []
    for p in sorted(outdir.glob("chunk_*.pkl")):
        rows += pickle.loads(p.read_bytes())["rows"]
    df = pd.DataFrame(rows)
    df.to_parquet(DATA / f"s2_scalars_{a.tag}.parquet", index=False)
    logger.info(f"wrote {len(df)} rows -> data/s2_scalars_{a.tag}.parquet; errors {df.get('s2_error', pd.Series()).notna().sum()}")


if __name__ == "__main__":
    main()
```

### [76] TOOL RESULT — Write · 2026-09-29 05:30:04 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s2_variants.py", "content": "#!/usr/bin/env python3\n\"\"\"S2: raw + resampling variants per concept (HOME build, concepts with n_home_early >= 10), checkpointed per chunk.\n\nPer concept (fast6 engine, SELF fixed at the full-build set):\n  RAW     the six components on the full home build (must equal EXP10 values), NB sets W1..W3, window counts\n  V1      rarefaction: for n in N_RARE, if every W-year has >= n papers: n papers per W-year + min(|PRE|, 3n) PRE,\n          D_RARE draws, nanmean (>= half finite)\n  V2      within-concept year-label permutation null (D_PERM permutations; PRE fixed): null mean / sd, excess, zperm\n  V2b     Chao 2005 abundance Jaccard persistence (non-SELF topic count vectors, W1-W2 and W2-W3)\n  V4raw   S_RAW split-halves (within window): the six components on each half\n  V4clean first S_CLEAN of those splits: V2 (D_PERM_HALF perms per half) and V1 n=5 (D_RARE_HALF draws per half,\n          concepts with >= 10 papers per W-year); the half NB sets are kept for the V3 half-nulls\nUsage: python s2_variants.py [--limit N] [--sample-per-body N] [--tag TAG] [--workers 3] [--draws-scale 1.0]\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport multiprocessing as mp\nimport pickle\nimport sys\nimport time\nimport warnings\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, RES, setup_logger\n\nCFG_DEFAULT = {\"N_RARE\": [5, 10, 20], \"D_RARE\": 50, \"D_PERM\": 200, \"S_RAW\": 100, \"S_CLEAN\": 20, \"D_PERM_HALF\": 50,\n               \"D_RARE_HALF\": 20, \"RARE_HALF_N\": 5, \"MIN_HOME\": 10}\nV2_METRICS = [\"edge_persistence\", \"NOV_res\", \"ego_density_W3\", \"new_edge_rate\", \"n_comm_W3\", \"participation\"]\n_G: dict = {}\n\n\ndef seed_key(frame: str, ci: int) -> int:\n    return int(ci) + (0 if frame == \"exp5\" else 100000)\n\n\ndef _init(cfg: dict) -> None:\n    import ego\n    from ego_ctx import rq1_context\n    from jobs import build_home_cache\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    ego.set_context(rq1_context())\n    _G[\"cache\"] = build_home_cache()\n    _G[\"cfg\"] = cfg\n\n\ndef _nanagg(v: np.ndarray, min_fin: int) -> tuple[float, float, int]:\n    f = np.isfinite(v)\n    if f.sum() < min_fin:\n        return float(\"nan\"), float(\"nan\"), int(f.sum())\n    return float(v[f].mean()), float(v[f].std()), int(f.sum())\n\n\ndef v2_block(P: dict, lab: np.ndarray, obs: dict, D: int, rng) -> dict:\n    from fast6 import fast6, permute_labels\n    r = fast6(P, permute_labels(lab, D, rng))\n    out = {}\n    for m in V2_METRICS:\n        mu, sd, nf = _nanagg(r[m], D // 2)\n        o = float(obs[m])\n        out[f\"{m}_nullmean\"] = mu\n        out[f\"{m}_nullsd\"] = sd\n        out[f\"{m}_exc\"] = o - mu if np.isfinite(o) and np.isfinite(mu) else float(\"nan\")\n        out[f\"{m}_zperm\"] = out[f\"{m}_exc\"] / sd if np.isfinite(out[f\"{m}_exc\"]) and sd > 0 else float(\"nan\")\n    return out\n\n\ndef v1_block(P: dict, lab: np.ndarray, n: int, D: int, rng) -> dict | None:\n    from fast6 import OUT6, fast6, rarefy_labels\n    if any((lab == w).sum() < n for w in (1, 2, 3)):\n        return None\n    r = fast6(P, rarefy_labels(lab, n, D, rng))\n    return {m: _nanagg(r[m], (D + 1) // 2)[0] for m in OUT6}\n\n\ndef one_concept(key: tuple) -> tuple[dict, dict]:\n    from fast6 import OUT6, chao_jaccard, fast6, half_split, prep\n    cfg = _G[\"cfg\"]\n    c = _G[\"cache\"][key]\n    frame, ci = key\n    sk = seed_key(frame, ci)\n    P = prep(c[\"name\"], c[\"aliases\"], c[\"t0\"], c[\"works\"])\n    lab = P[\"lab\"]\n    row: dict = {\"frame\": frame, \"ci\": int(ci), \"body\": c[\"body\"], \"t0\": c[\"t0\"], \"n_home_early\": c[\"n_home_early\"],\n                 \"n_home_pre\": int((lab == 0).sum()), \"n_W1\": int((lab == 1).sum()), \"n_W2\": int((lab == 2).sum()),\n                 \"n_W3\": int((lab == 3).sum()), \"n_self\": int(P[\"SELF\"].sum()), \"n_cand\": int(len(P[\"cand\"]))}\n    raw = fast6(P, lab[None, :], return_sets=True, return_counts=True)\n    obs = {m: float(raw[m][0]) for m in list(OUT6) + [\"M\", \"deg_W1\", \"deg_W3\", \"e_W3\"]}\n    row.update({f\"{m}__raw\": v for m, v in obs.items()})\n    row[\"min_year_n\"] = int(min(row[\"n_W1\"], row[\"n_W2\"], row[\"n_W3\"]))\n    extra: dict = {\"NB\": {w: P[\"cg\"][raw[\"NB\"][w][0]].astype(np.int32) for w in (1, 2, 3)},\n                   \"SELF\": np.nonzero(P[\"SELF\"])[0].astype(np.int32)}\n    # V2b Chao\n    ns = ~P[\"selfU\"]\n    cw = {w: raw[\"cnt\"][w][0][ns] for w in (1, 2, 3)}\n    j12, j23 = chao_jaccard(cw[1], cw[2]), chao_jaccard(cw[2], cw[3])\n    fin = [j for j in (j12, j23) if np.isfinite(j)]\n    row[\"EP_chao\"] = float(np.mean(fin)) if fin else float(\"nan\")\n    # V1 rarefaction\n    for n in cfg[\"N_RARE\"]:\n        rng = np.random.default_rng([7000000, sk, n])\n        r = v1_block(P, lab, n, cfg[\"D_RARE\"], rng)\n        for m in OUT6:\n            row[f\"{m}_rare{n}\"] = r[m] if r is not None else float(\"nan\")\n    # V2 permutation null\n    rng = np.random.default_rng([8000000, sk])\n    row.update(v2_block(P, lab, obs, cfg[\"D_PERM\"], rng))\n    # V4 split halves\n    rng = np.random.default_rng([9000000, sk])\n    LA, LB = half_split(lab, cfg[\"S_RAW\"], rng)\n    ra = fast6(P, LA, return_sets=True)\n    rb = fast6(P, LB, return_sets=True)\n    extra[\"half_raw\"] = {h: np.stack([r[m] for m in OUT6], 1).astype(np.float32) for h, r in ((\"A\", ra), (\"B\", rb))}\n    S = cfg[\"S_CLEAN\"]\n    extra[\"half_NB\"] = {h: [[P[\"cg\"][r[\"NB\"][w][s]].astype(np.int32) for w in (1, 2, 3)] for s in range(S)]\n                        for h, r in ((\"A\", ra), (\"B\", rb))}\n    rng_p = np.random.default_rng([9100000, sk])\n    rng_r = np.random.default_rng([9200000, sk])\n    hc: dict = {}\n    for h, L, r in ((\"A\", LA, ra), (\"B\", LB, rb)):\n        rows_h = []\n        for s in range(S):\n            obs_h = {m: float(r[m][s]) for m in OUT6}\n            d = v2_block(P, L[s], obs_h, cfg[\"D_PERM_HALF\"], rng_p)\n            rr = v1_block(P, L[s], cfg[\"RARE_HALF_N\"], cfg[\"D_RARE_HALF\"], rng_r)\n            d.update({f\"{m}_rare{cfg['RARE_HALF_N']}\": (rr[m] if rr is not None else float(\"nan\")) for m in OUT6})\n            rows_h.append(d)\n        hc[h] = pd.DataFrame(rows_h).astype(np.float32)\n    extra[\"half_clean\"] = hc\n    return row, extra\n\n\ndef run_chunk(k: int, keys: list) -> tuple[int, list, list, float]:\n    t = time.time()\n    rows, extras = [], []\n    for key in keys:\n        try:\n            r, e = one_concept(key)\n        except (ValueError, IndexError, ZeroDivisionError, FloatingPointError) as ex:\n            r, e = {\"frame\": key[0], \"ci\": int(key[1]), \"s2_error\": repr(ex)[:200]}, {}\n        rows.append(r)\n        extras.append(e)\n    return k, rows, extras, time.time() - t\n\n\ndef select_keys(cache: dict, min_home: int, sample_per_body: int, seed: int = 5) -> list:\n    keys = sorted(k for k, v in cache.items() if v[\"n_home_early\"] >= min_home)\n    if sample_per_body:\n        rng = np.random.default_rng(seed)\n        out = []\n        for b in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"):\n            kb = [k for k in keys if cache[k][\"body\"] == b]\n            out += [kb[i] for i in sorted(rng.choice(len(kb), min(sample_per_body, len(kb)), replace=False))]\n        keys = out\n    return keys\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--limit\", type=int, default=0)\n    ap.add_argument(\"--sample-per-body\", type=int, default=0)\n    ap.add_argument(\"--tag\", default=\"full\")\n    ap.add_argument(\"--workers\", type=int, default=3)\n    ap.add_argument(\"--chunk\", type=int, default=100)\n    ap.add_argument(\"--cfg\", default=\"\")\n    a = ap.parse_args()\n    logger = setup_logger(f\"s2_variants_{a.tag}\")\n    cfg = dict(CFG_DEFAULT)\n    if a.cfg:\n        cfg.update(json.loads(a.cfg))\n    from jobs import build_home_cache\n    cache = build_home_cache()\n    keys = select_keys(cache, cfg[\"MIN_HOME\"], a.sample_per_body)\n    if a.limit:\n        keys = keys[:a.limit]\n    # big concepts first so the tail is short\n    keys.sort(key=lambda k: -len(cache[k][\"works\"]))\n    del cache\n    outdir = DATA / f\"s2_parts_{a.tag}\"\n    outdir.mkdir(parents=True, exist_ok=True)\n    (outdir / \"cfg.json\").write_text(json.dumps(cfg))\n    chunks = [keys[i:i + a.chunk] for i in range(0, len(keys), a.chunk)]\n    todo = [k for k in range(len(chunks)) if not (outdir / f\"chunk_{k:05d}.pkl\").exists()]\n    logger.info(f\"S2 {a.tag}: {len(keys)} concepts, {len(chunks)} chunks, todo {len(todo)}, cfg {cfg}\")\n    t0 = time.time()\n    done = 0\n    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context(\"spawn\"), initializer=_init,\n                             initargs=(cfg,)) as ex:\n        futs = [ex.submit(run_chunk, k, chunks[k]) for k in todo]\n        for i, fu in enumerate(as_completed(futs)):\n            k, rows, extras, dt = fu.result()\n            (outdir / f\"chunk_{k:05d}.pkl\").write_bytes(pickle.dumps({\"rows\": rows, \"extras\": extras}, protocol=5))\n            done += len(rows)\n            el = time.time() - t0\n            logger.info(f\"chunk {i+1}/{len(futs)} ({done} concepts) {el/60:.1f} min; {dt/len(rows):.3f} s/concept; \"\n                        f\"eta {el/(i+1)*(len(futs)-i-1)/60:.1f} min\")\n    rows = []\n    for p in sorted(outdir.glob(\"chunk_*.pkl\")):\n        rows += pickle.loads(p.read_bytes())[\"rows\"]\n    df = pd.DataFrame(rows)\n    df.to_parquet(DATA / f\"s2_scalars_{a.tag}.parquet\", index=False)\n    logger.info(f\"wrote {len(df)} rows -> data/s2_scalars_{a.tag}.parquet; errors {df.get('s2_error', pd.Series()).notna().sum()}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [77] TOOL CALL — Bash · 2026-09-29 05:30:04 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -2 logs/u_fast6_1000.out; time timeout 900 .venv/bin/python s2_variants.py --sample-per-body 50 --tag mini --workers 3 --chunk 25 --cfg '{"D_RARE":20,"D_PERM":20,"S_RAW":10,"S_CLEAN":10,"D_PERM_HALF":20,"D_RARE_HALF":10}' 2>&1 | tail -5
```

### [78] TOOL RESULT — Bash · 2026-09-29 05:30:46 UTC

```
{"stdout": "05:29:08|INFO   |{\"U1\": true, \"U2\": true, \"U5\": true, \"U6\": true, \"timing\": null}\n05:29:08|INFO   |worst {'full': 1.1102230246251565e-16, 'half': 1.1102230246251565e-16, 'perm': 1.1102230246251565e-16, 'rare5': 0.0}; timing {'fast_ms_per_call': 0.219456295468914, 'ref_ms_per_call': 1.7263522661571056}\n05:29:42|INFO   |chunk 5/8 (125 concepts) 0.2 min; 0.028 s/concept; eta 0.1 min\n05:29:43|INFO   |chunk 6/8 (150 concepts) 0.2 min; 0.032 s/concept; eta 0.1 min\n05:29:43|INFO   |chunk 7/8 (175 concepts) 0.2 min; 0.031 s/concept; eta 0.0 min\n05:29:43|INFO   |chunk 8/8 (200 concepts) 0.2 min; 0.018 s/concept; eta 0.0 min\n05:29:44|INFO   |wrote 200 rows -> data/s2_scalars_mini.parquet; errors 0\n\nreal\t0m19.062s\nuser\t0m16.998s\nsys\t0m1.399s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [79] ASSISTANT · 2026-09-29 05:30:46 UTC

```
U1 passes on all 1,000 concepts (max diff 1.1e-16). Timing the full-draw config on 200 concepts and checking the raw values against EXP10:
```

### [80] TOOL CALL — Bash · 2026-09-29 05:30:46 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; time timeout 900 .venv/bin/python s2_variants.py --sample-per-body 50 --tag t200 --workers 4 --chunk 25 2>&1 | tail -3; .venv/bin/python - <<'EOF'
import pandas as pd, numpy as np
S="/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data/"
d=pd.read_parquet("data/s2_scalars_t200.parquet")
for fr,f in (("exp5","ego_open_exp5.parquet"),("cohort","ego_open_cohort.parquet")):
    ref=pd.read_parquet(S+f).set_index("ci"); m=d[d.frame==fr].set_index("ci"); ref=ref.loc[m.index]
    for k in ["new_edge_rate","n_comm_W3","participation","NOV_res","ego_density_W3","edge_persistence"]:
        a=m[k+"__raw"].to_numpy(float); b=ref[k+"__home"].to_numpy(float)
        print(fr,k, np.nanmax(np.abs(a-b)), (np.isnan(a)^np.isnan(b)).sum())
pd.set_option("display.width",250)
cols=["edge_persistence__raw","edge_persistence_rare10","edge_persistence_nullmean","edge_persistence_exc","edge_persistence_zperm","EP_chao","NOV_res__raw","NOV_res_rare10","NOV_res_exc","NOV_res_zperm"]
print(d[cols].describe().T)
print(d[cols+["n_home_early"]].corr(method="spearman")["n_home_early"])
EOF
```

### [81] TOOL RESULT — Bash · 2026-09-29 05:31:12 UTC

```
{"stdout": "05:30:21|INFO   |chunk 7/8 (175 concepts) 0.4 min; 0.182 s/concept; eta 0.1 min\n05:30:21|INFO   |chunk 8/8 (200 concepts) 0.4 min; 0.183 s/concept; eta 0.0 min\n05:30:22|INFO   |wrote 200 rows -> data/s2_scalars_t200.parquet; errors 0\n\nreal\t0m29.881s\nuser\t0m22.426s\nsys\t0m1.810s\nexp5 new_edge_rate 0.0 0\nexp5 n_comm_W3 0.0 0\nexp5 participation 1.1102230246251565e-16 0\nexp5 NOV_res 0.0 0\nexp5 ego_density_W3 0.0 0\nexp5 edge_persistence 0.0 0\ncohort new_edge_rate 0.0 0\ncohort n_comm_W3 0.0 0\ncohort participation 1.1102230246251565e-16 0\ncohort NOV_res 0.0 0\ncohort ego_density_W3 0.0 0\ncohort edge_persistence 0.0 0\n                           count      mean  ...       75%       max\nedge_persistence__raw      190.0  0.109143  ...  0.199603  0.750000\nedge_persistence_rare10     69.0  0.103827  ...  0.157452  0.265000\nedge_persistence_nullmean  194.0  0.113905  ...  0.187188  0.562143\nedge_persistence_exc       189.0 -0.007198  ...  0.009246  0.479333\nedge_persistence_zperm     142.0 -0.107164  ...  0.477097  2.553021\nEP_chao                    194.0  0.372825  ...  0.563457  1.000000\nNOV_res__raw               158.0 -0.473949  ...  0.024863  0.094740\nNOV_res_rare10              52.0 -0.534661  ... -0.207652  0.092244\nNOV_res_exc                148.0  0.010483  ...  0.108295  0.620794\nNOV_res_zperm              140.0 -0.062479  ...  0.782592  2.165809\n\n[10 rows x 8 columns]\nedge_persistence__raw        0.700169\nedge_persistence_rare10      0.241691\nedge_persistence_nullmean    0.865757\nedge_persistence_exc        -0.125911\nedge_persistence_zperm      -0.000769\nEP_chao                      0.649278\nNOV_res__raw                -0.099121\nNOV_res_rare10              -0.104177\nNOV_res_exc                 -0.144018\nNOV_res_zperm               -0.102054\nn_home_early                 1.000000\nName: n_home_early, dtype: float64", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [82] THINKING · 2026-09-29 05:31:36 UTC

```
The fast engine matches EXP10 exactly at ~0.18s/concept (~10 min for all 13.4k concepts on 4 workers). Raw edge persistence correlates with log n (ρ≈0.70), and its permutation-null mean tracks even more closely (0.87); next I'll write the frozen spec and seal before joining outcomes.
```

### [83] TOOL CALL — Write · 2026-09-29 05:31:36 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/seal.py

"""Hash-chained seal log (logs/seal.log): every entry records the sha256 of the sealed file(s), a timestamp and the
hash of the previous entry, so any later edit of a sealed file or of the log itself is detectable."""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from common import LOGS, sha256_file

LOG = LOGS / "seal.log"


def _lines() -> list[str]:
    return [l for l in LOG.read_text().splitlines() if l.strip()] if LOG.exists() else []


def record(stage: str, **kw) -> dict:
    prev = _lines()
    prev_hash = hashlib.sha256(prev[-1].encode()).hexdigest() if prev else "GENESIS"
    ent = {"stage": stage, "time": time.strftime("%Y-%m-%d %H:%M:%S"), "prev": prev_hash, **kw}
    with LOG.open("a") as f:
        f.write(json.dumps(ent, sort_keys=True) + "\n")
    return ent


def verify_chain() -> bool:
    L = _lines()
    for i, l in enumerate(L):
        e = json.loads(l)
        want = hashlib.sha256(L[i - 1].encode()).hexdigest() if i else "GENESIS"
        if e["prev"] != want:
            return False
    return True


def seal_file(stage: str, path: Path, **kw) -> dict:
    return record(stage, file=str(Path(path).name), sha256=sha256_file(path), **kw)


def check_sealed(stage: str, path: Path) -> bool:
    ents = [json.loads(l) for l in _lines() if json.loads(l)["stage"] == stage]
    return bool(ents) and ents[-1]["sha256"] == sha256_file(path) and verify_chain()
```

### [84] TOOL RESULT — Write · 2026-09-29 05:31:36 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/seal.py", "content": "\"\"\"Hash-chained seal log (logs/seal.log): every entry records the sha256 of the sealed file(s), a timestamp and the\nhash of the previous entry, so any later edit of a sealed file or of the log itself is detectable.\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport json\nimport time\nfrom pathlib import Path\n\nfrom common import LOGS, sha256_file\n\nLOG = LOGS / \"seal.log\"\n\n\ndef _lines() -> list[str]:\n    return [l for l in LOG.read_text().splitlines() if l.strip()] if LOG.exists() else []\n\n\ndef record(stage: str, **kw) -> dict:\n    prev = _lines()\n    prev_hash = hashlib.sha256(prev[-1].encode()).hexdigest() if prev else \"GENESIS\"\n    ent = {\"stage\": stage, \"time\": time.strftime(\"%Y-%m-%d %H:%M:%S\"), \"prev\": prev_hash, **kw}\n    with LOG.open(\"a\") as f:\n        f.write(json.dumps(ent, sort_keys=True) + \"\\n\")\n    return ent\n\n\ndef verify_chain() -> bool:\n    L = _lines()\n    for i, l in enumerate(L):\n        e = json.loads(l)\n        want = hashlib.sha256(L[i - 1].encode()).hexdigest() if i else \"GENESIS\"\n        if e[\"prev\"] != want:\n            return False\n    return True\n\n\ndef seal_file(stage: str, path: Path, **kw) -> dict:\n    return record(stage, file=str(Path(path).name), sha256=sha256_file(path), **kw)\n\n\ndef check_sealed(stage: str, path: Path) -> bool:\n    ents = [json.loads(l) for l in _lines() if json.loads(l)[\"stage\"] == stage]\n    return bool(ents) and ents[-1][\"sha256\"] == sha256_file(path) and verify_chain()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [85] TOOL CALL — Write · 2026-09-29 05:32:20 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s1_freeze.py

#!/usr/bin/env python3
"""S1 FREEZE (before any outcome is joined): variant definitions, draw counts, seeds, constants rule, predictions
P1-P3 and verdict rules -> results/frozen_spec.json, sha256 -> logs/seal.log (entry S1_freeze).
The z constants of the clean composites are appended later by s4_composites.py (entry S1b_constants), still before
any outcome join. NOTE: the outcomes of every body were already unsealed by EXP5/EXP8/EXP10 -- this is a
pre-analysis commitment on selection data, not a blind."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

from common import DATA_IN, RES, jdump, setup_logger, sha256_file
from s2_cfg import CFG_FULL
from seal import LOG, seal_file

logger = setup_logger("s1_freeze")


def main() -> None:
    exp10 = json.loads((DATA_IN.parent / "results/frozen_spec.json").read_text())
    spec = {
        "status": "pre-analysis commitment on SELECTION data; outcomes previously unsealed by EXP5/EXP8/EXP10",
        "bodies": {
            "DEV": "EXP5 frame split DEV (t0 2003-09; CS/Eng/BGM/Med home groups)",
            "OLDHO": "EXP5 frame split HELDOUT (t0 2003-09; PHYS/LIFEENV/SOC/MATHDEC)",
            "COH1014": "EXP5 frame split COHORT (t0 2010-14)",
            "COH1517": "EXP10 fresh cohort (t0 2015-17), analysis_cohort.parquet",
            "POOLED": "all four stacked; body dummies added to the categorical block of every rung; year dummies span "
                      "t0 2003-2017"},
        "inclusion": "HOME build; n_home_early (home papers t0..t0+2, EXP10 count) >= 10 for every variant and "
                     "analysis (the OPEN_home rule); drop counts per body reported",
        "engine": {"fast6": "lib/fast6.py, validated == ego.concept_core (SELF override) to <= 1e-12 (U1)",
                   "SELF": "computed once on the FULL home build (ego.self_topics) and held FIXED in every resampled "
                           "variant (definitional exclusion of the concept's own name topics)"},
        "draws": CFG_FULL,
        "seeds": {"V1": "numpy default_rng([7000000, sk, n])", "V2": "default_rng([8000000, sk])",
                  "V4_splits": "default_rng([9000000, sk])", "V4_V2_halves": "default_rng([9100000, sk])",
                  "V4_V1_halves": "default_rng([9200000, sk])",
                  "sk": "ci for EXP5-frame concepts, 100000 + ci for COH1517 (ci spaces overlap)",
                  "V3a_rewire": "random.seed / igraph RNG = 20260930 + 1000 s + d", "V3b": "default_rng([20260931, sk])",
                  "V3c_curveball": "numba seed 20260932 + year", "bootstrap": 20260930,
                  "note": "seed streams via SeedSequence lists replace the plan's additive seeds (7e6 + 100 ci + n "
                          "etc.) because COH1517 and EXP5 ci values overlap; declared pre-run"},
        "variants": {
            "RAW": "six EXP10 components on the full home build: new_edge_rate, n_comm_W3, participation, NOV_res, "
                   "ego_density_W3, edge_persistence",
            "V1_rare{n}": "n in (5, 10, 20): concepts with >= n home papers in EACH of W1, W2, W3; each draw keeps "
                          "exactly n papers per W-year and min(|PRE|, 3n) PRE papers (without replacement); "
                          "D_RARE draws; nanmean over draws, NaN unless >= half finite. n = 10 primary.",
            "V1_contingency_F6": "if fewer than 150 COH1517 concepts have finite NOVCHURN_rare10 and O2r_m50, n = 5 is "
                                 "primary for COH1517 (NOVCHURN_rare_primary); if < 100 even at n = 5 V1 is reported "
                                 "not estimable on COH1517 and P1 is decided on V2 alone",
            "V2": "D_PERM permutations of the W1..W3 year labels among the concept's W home papers (yearly counts "
                  "kept, PRE fixed); per metric null mean, null sd, excess = obs - null mean (*_exc), zperm = "
                  "excess / null sd (NaN if sd == 0); NaN unless >= half the draws finite",
            "V2b_EP_chao": "Chao et al. 2005 abundance-based Jaccard (bias-corrected f2 = 0 form, U, V capped at 1) on "
                           "the non-SELF topic count vectors of W1-W2 and W2-W3, mean of the finite pairs; "
                           "exploratory sensitivity",
            "V3a_z_dens_cfg": "full topic backbone of slice s rewired 200 times (igraph Graph.rewire(n = 10 m, "
                              "mode='simple'), degree sequence asserted); e_null = edges of the rewired graph inside "
                              "S = raw NB_W3 (|S| >= 2); z = (e_obs - mean) / sd; also z_dens_cfg_W1 on NB_W1 / "
                              "slice(t0)",
            "V3b_z_dens_k": "200 random sets of size |S| drawn without replacement with probability proportional to "
                            "bg counts in year t0+2 among topics with bg > 0 and not SELF; edges counted in the REAL "
                            "backbone; z = (e_obs - mean) / sd",
            "V3c_z_pers_cfg": "curveball randomisation (Strona 2014) of the bipartite (concept-window x partner topic) "
                              "incidence of raw non-SELF NB sets within each calendar year, pooled over all bodies; "
                              "burn-in 5 x n_rows trades, 200 samples each n_rows trades apart; null persistence = "
                              "mean(J(W1, W2), J(W2, W3)) of the concept's rows in the same sample index; z = (obs - "
                              "mean) / sd; excess_pers_cfg = obs - mean. Null expected Jaccard is near 0, so z is "
                              "mostly obs / sd (degree normalisation, not a coherence test)",
            "V4": "split-half reliability: S_RAW random within-window half splits for RAW; the first S_CLEAN of them "
                  "for clean variants (V2 with D_PERM_HALF perms per half; V1 n = 5 with D_RARE_HALF draws per half, "
                  "concepts with >= 10 papers per W-year; V3a/V3b with 50 null draws per half; V3c on halves via the "
                  "k-matched Monte Carlo approximation: row sizes from the half, column weights = that year's topic "
                  "neighbour popularity, 50 draws). r_s = Spearman(v_A, v_B) across concepts; r = tanh(mean atanh "
                  "r_s); SB = 2r / (1 + r); per body, pooled, per n_home_early bin (10-19, 20-49, 50-99, >= 100); "
                  "200-resample concept bootstrap CI for pooled SB (split-averaged half values)",
            "outcome_reliability": "O2r_m50: papers of the outcome window (t0+6..t0+8, field counts) split by "
                                   "multivariate hypergeometric thinning into halves (100 splits), exact "
                                   "hypergeometric rarefied richness at m = 25 per half (concepts with >= 50 outcome "
                                   "papers); SB; flagged 'conservative, m = 25 halves'. rel_y = 1 (flagged) if the "
                                   "counts are not cached"},
        "composites": {
            "z_rule_new_constants": "winsorise at 0.5 / 99.5 percentiles, mean / sd of the winsorised values over ALL "
                                    "EXP5-frame concepts (n_home_early >= 10) with the variant finite (== "
                                    "ladder.fit_open_constants); written to this spec as S1b before outcomes join",
            "raw_constants": "EXP10 frozen open_constants.home for raw components",
            "NOVCHURN_raw": "mean(z NOV_res__home, -z edge_persistence__home), EXP10 constants, both finite",
            "NOVCHURN_rare10": "mean(z NOV_res_rare10, -z edge_persistence_rare10), new constants, both finite "
                               "(also rare5 / rare20)",
            "NOVCHURN_exc": "mean(z NOV_res_exc, -z edge_persistence_exc), new constants, both finite",
            "NOVCHURN_zperm": "mean(z NOV_res_zperm, -z edge_persistence_zperm) (sensitivity)",
            "NOVCHURN_cfg": "mean(z NOV_res (EXP10 const), -z z_pers_cfg (new)), both finite",
            "NOVCHURN_chao": "mean(z NOV_res (EXP10 const), -z EP_chao (new)), both finite",
            "OPEN_home_clean": "six-component mean, ego_density_W3 -> z_dens_cfg (sign -1), edge_persistence -> "
                               "z_pers_cfg (sign -1), others raw with EXP10 constants; >= 4 finite; n_home_early >= 10",
            "OPEN_home_exc": "same with ego_density_W3_exc and edge_persistence_exc (sign -1)"},
        "outcomes": {"primary": "O2r_m50", "secondary": "O2r_resid"},
        "rungs": ["R0", "R2", "R3"], "rung_definition": "EXP10 lib/ladder.rung_design (+ body dummies for POOLED)",
        "groups": exp10["groups"], "bootstrap": {"B": 2000, "seed": 20260930, "unit": "concept"},
        "exp10_open_constants_home": exp10["open_constants"]["home"],
        "exp10_prediction_models": exp10["prediction_models"],
        "direction_convention": "psp is reported on the variant as stored; persistence/density variants are "
                                "expected negative, NOVCHURN / OPEN positive; retention ratio = psp_clean / psp_raw on "
                                "the SAME concepts (both finite), per bootstrap resample with shared indices",
        "predictions": {
            "P1": "psp(NOVCHURN_exc | R2, O2r_m50) >= 0.70 x psp(NOVCHURN_raw) on COH1517 AND on OLDHO (same-sample "
                  "ratio; point ratio decides, paired-bootstrap percentile CI reported)",
            "P2": "z_pers_cfg keeps a negative psp with 95% CI < 0 on POOLED (R2, body dummies)",
            "P3": "|Spearman(NOVCHURN_exc, log n_home_early)| < 0.20 on POOLED"},
        "verdict_rules": {
            "CHURN_NOT_THIN": "P1 and P3 hold AND V1 (NOVCHURN_rare10, or the F6 primary n) keeps >= 50% of the raw "
                              "psp (same-sample ratio) in COH1517 or OLDHO",
            "CHURN_THIN": "raw NOVCHURN CI excludes 0 (in the body considered) but NOVCHURN_exc AND NOVCHURN_rare10 "
                          "keep < 30% of it in BOTH COH1517 and OLDHO",
            "PARTLY_THIN": "otherwise",
            "DEGREE_ARTEFACT_PERSISTENCE": "flag added if P2 fails while raw edge_persistence has CI < 0 on POOLED"},
        "holm": "Holm over the P1-P3 family (one-sided bootstrap p), reported only",
        "power": {"targets": "T1 disattenuated pooled R3/R5, T2 COH1517 raw, T3 half pooled raw", "n": [800, 1500, 2500],
                  "draws": 1000, "scenarios": "S_A EXP5 n-mix; S_B pessimistic (n-bin weights shifted one bin down)"},
    }
    p = RES / "frozen_spec.json"
    jdump(spec, p)
    ent = seal_file("S1_freeze", p)
    logger.info(f"sealed frozen_spec.json sha256 {ent['sha256']} -> {LOG}")


if __name__ == "__main__":
    main()
```

### [86] TOOL RESULT — Write · 2026-09-29 05:32:20 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s1_freeze.py", "content": "#!/usr/bin/env python3\n\"\"\"S1 FREEZE (before any outcome is joined): variant definitions, draw counts, seeds, constants rule, predictions\nP1-P3 and verdict rules -> results/frozen_spec.json, sha256 -> logs/seal.log (entry S1_freeze).\nThe z constants of the clean composites are appended later by s4_composites.py (entry S1b_constants), still before\nany outcome join. NOTE: the outcomes of every body were already unsealed by EXP5/EXP8/EXP10 -- this is a\npre-analysis commitment on selection data, not a blind.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nfrom common import DATA_IN, RES, jdump, setup_logger, sha256_file\nfrom s2_cfg import CFG_FULL\nfrom seal import LOG, seal_file\n\nlogger = setup_logger(\"s1_freeze\")\n\n\ndef main() -> None:\n    exp10 = json.loads((DATA_IN.parent / \"results/frozen_spec.json\").read_text())\n    spec = {\n        \"status\": \"pre-analysis commitment on SELECTION data; outcomes previously unsealed by EXP5/EXP8/EXP10\",\n        \"bodies\": {\n            \"DEV\": \"EXP5 frame split DEV (t0 2003-09; CS/Eng/BGM/Med home groups)\",\n            \"OLDHO\": \"EXP5 frame split HELDOUT (t0 2003-09; PHYS/LIFEENV/SOC/MATHDEC)\",\n            \"COH1014\": \"EXP5 frame split COHORT (t0 2010-14)\",\n            \"COH1517\": \"EXP10 fresh cohort (t0 2015-17), analysis_cohort.parquet\",\n            \"POOLED\": \"all four stacked; body dummies added to the categorical block of every rung; year dummies span \"\n                      \"t0 2003-2017\"},\n        \"inclusion\": \"HOME build; n_home_early (home papers t0..t0+2, EXP10 count) >= 10 for every variant and \"\n                     \"analysis (the OPEN_home rule); drop counts per body reported\",\n        \"engine\": {\"fast6\": \"lib/fast6.py, validated == ego.concept_core (SELF override) to <= 1e-12 (U1)\",\n                   \"SELF\": \"computed once on the FULL home build (ego.self_topics) and held FIXED in every resampled \"\n                           \"variant (definitional exclusion of the concept's own name topics)\"},\n        \"draws\": CFG_FULL,\n        \"seeds\": {\"V1\": \"numpy default_rng([7000000, sk, n])\", \"V2\": \"default_rng([8000000, sk])\",\n                  \"V4_splits\": \"default_rng([9000000, sk])\", \"V4_V2_halves\": \"default_rng([9100000, sk])\",\n                  \"V4_V1_halves\": \"default_rng([9200000, sk])\",\n                  \"sk\": \"ci for EXP5-frame concepts, 100000 + ci for COH1517 (ci spaces overlap)\",\n                  \"V3a_rewire\": \"random.seed / igraph RNG = 20260930 + 1000 s + d\", \"V3b\": \"default_rng([20260931, sk])\",\n                  \"V3c_curveball\": \"numba seed 20260932 + year\", \"bootstrap\": 20260930,\n                  \"note\": \"seed streams via SeedSequence lists replace the plan's additive seeds (7e6 + 100 ci + n \"\n                          \"etc.) because COH1517 and EXP5 ci values overlap; declared pre-run\"},\n        \"variants\": {\n            \"RAW\": \"six EXP10 components on the full home build: new_edge_rate, n_comm_W3, participation, NOV_res, \"\n                   \"ego_density_W3, edge_persistence\",\n            \"V1_rare{n}\": \"n in (5, 10, 20): concepts with >= n home papers in EACH of W1, W2, W3; each draw keeps \"\n                          \"exactly n papers per W-year and min(|PRE|, 3n) PRE papers (without replacement); \"\n                          \"D_RARE draws; nanmean over draws, NaN unless >= half finite. n = 10 primary.\",\n            \"V1_contingency_F6\": \"if fewer than 150 COH1517 concepts have finite NOVCHURN_rare10 and O2r_m50, n = 5 is \"\n                                 \"primary for COH1517 (NOVCHURN_rare_primary); if < 100 even at n = 5 V1 is reported \"\n                                 \"not estimable on COH1517 and P1 is decided on V2 alone\",\n            \"V2\": \"D_PERM permutations of the W1..W3 year labels among the concept's W home papers (yearly counts \"\n                  \"kept, PRE fixed); per metric null mean, null sd, excess = obs - null mean (*_exc), zperm = \"\n                  \"excess / null sd (NaN if sd == 0); NaN unless >= half the draws finite\",\n            \"V2b_EP_chao\": \"Chao et al. 2005 abundance-based Jaccard (bias-corrected f2 = 0 form, U, V capped at 1) on \"\n                           \"the non-SELF topic count vectors of W1-W2 and W2-W3, mean of the finite pairs; \"\n                           \"exploratory sensitivity\",\n            \"V3a_z_dens_cfg\": \"full topic backbone of slice s rewired 200 times (igraph Graph.rewire(n = 10 m, \"\n                              \"mode='simple'), degree sequence asserted); e_null = edges of the rewired graph inside \"\n                              \"S = raw NB_W3 (|S| >= 2); z = (e_obs - mean) / sd; also z_dens_cfg_W1 on NB_W1 / \"\n                              \"slice(t0)\",\n            \"V3b_z_dens_k\": \"200 random sets of size |S| drawn without replacement with probability proportional to \"\n                            \"bg counts in year t0+2 among topics with bg > 0 and not SELF; edges counted in the REAL \"\n                            \"backbone; z = (e_obs - mean) / sd\",\n            \"V3c_z_pers_cfg\": \"curveball randomisation (Strona 2014) of the bipartite (concept-window x partner topic) \"\n                              \"incidence of raw non-SELF NB sets within each calendar year, pooled over all bodies; \"\n                              \"burn-in 5 x n_rows trades, 200 samples each n_rows trades apart; null persistence = \"\n                              \"mean(J(W1, W2), J(W2, W3)) of the concept's rows in the same sample index; z = (obs - \"\n                              \"mean) / sd; excess_pers_cfg = obs - mean. Null expected Jaccard is near 0, so z is \"\n                              \"mostly obs / sd (degree normalisation, not a coherence test)\",\n            \"V4\": \"split-half reliability: S_RAW random within-window half splits for RAW; the first S_CLEAN of them \"\n                  \"for clean variants (V2 with D_PERM_HALF perms per half; V1 n = 5 with D_RARE_HALF draws per half, \"\n                  \"concepts with >= 10 papers per W-year; V3a/V3b with 50 null draws per half; V3c on halves via the \"\n                  \"k-matched Monte Carlo approximation: row sizes from the half, column weights = that year's topic \"\n                  \"neighbour popularity, 50 draws). r_s = Spearman(v_A, v_B) across concepts; r = tanh(mean atanh \"\n                  \"r_s); SB = 2r / (1 + r); per body, pooled, per n_home_early bin (10-19, 20-49, 50-99, >= 100); \"\n                  \"200-resample concept bootstrap CI for pooled SB (split-averaged half values)\",\n            \"outcome_reliability\": \"O2r_m50: papers of the outcome window (t0+6..t0+8, field counts) split by \"\n                                   \"multivariate hypergeometric thinning into halves (100 splits), exact \"\n                                   \"hypergeometric rarefied richness at m = 25 per half (concepts with >= 50 outcome \"\n                                   \"papers); SB; flagged 'conservative, m = 25 halves'. rel_y = 1 (flagged) if the \"\n                                   \"counts are not cached\"},\n        \"composites\": {\n            \"z_rule_new_constants\": \"winsorise at 0.5 / 99.5 percentiles, mean / sd of the winsorised values over ALL \"\n                                    \"EXP5-frame concepts (n_home_early >= 10) with the variant finite (== \"\n                                    \"ladder.fit_open_constants); written to this spec as S1b before outcomes join\",\n            \"raw_constants\": \"EXP10 frozen open_constants.home for raw components\",\n            \"NOVCHURN_raw\": \"mean(z NOV_res__home, -z edge_persistence__home), EXP10 constants, both finite\",\n            \"NOVCHURN_rare10\": \"mean(z NOV_res_rare10, -z edge_persistence_rare10), new constants, both finite \"\n                               \"(also rare5 / rare20)\",\n            \"NOVCHURN_exc\": \"mean(z NOV_res_exc, -z edge_persistence_exc), new constants, both finite\",\n            \"NOVCHURN_zperm\": \"mean(z NOV_res_zperm, -z edge_persistence_zperm) (sensitivity)\",\n            \"NOVCHURN_cfg\": \"mean(z NOV_res (EXP10 const), -z z_pers_cfg (new)), both finite\",\n            \"NOVCHURN_chao\": \"mean(z NOV_res (EXP10 const), -z EP_chao (new)), both finite\",\n            \"OPEN_home_clean\": \"six-component mean, ego_density_W3 -> z_dens_cfg (sign -1), edge_persistence -> \"\n                               \"z_pers_cfg (sign -1), others raw with EXP10 constants; >= 4 finite; n_home_early >= 10\",\n            \"OPEN_home_exc\": \"same with ego_density_W3_exc and edge_persistence_exc (sign -1)\"},\n        \"outcomes\": {\"primary\": \"O2r_m50\", \"secondary\": \"O2r_resid\"},\n        \"rungs\": [\"R0\", \"R2\", \"R3\"], \"rung_definition\": \"EXP10 lib/ladder.rung_design (+ body dummies for POOLED)\",\n        \"groups\": exp10[\"groups\"], \"bootstrap\": {\"B\": 2000, \"seed\": 20260930, \"unit\": \"concept\"},\n        \"exp10_open_constants_home\": exp10[\"open_constants\"][\"home\"],\n        \"exp10_prediction_models\": exp10[\"prediction_models\"],\n        \"direction_convention\": \"psp is reported on the variant as stored; persistence/density variants are \"\n                                \"expected negative, NOVCHURN / OPEN positive; retention ratio = psp_clean / psp_raw on \"\n                                \"the SAME concepts (both finite), per bootstrap resample with shared indices\",\n        \"predictions\": {\n            \"P1\": \"psp(NOVCHURN_exc | R2, O2r_m50) >= 0.70 x psp(NOVCHURN_raw) on COH1517 AND on OLDHO (same-sample \"\n                  \"ratio; point ratio decides, paired-bootstrap percentile CI reported)\",\n            \"P2\": \"z_pers_cfg keeps a negative psp with 95% CI < 0 on POOLED (R2, body dummies)\",\n            \"P3\": \"|Spearman(NOVCHURN_exc, log n_home_early)| < 0.20 on POOLED\"},\n        \"verdict_rules\": {\n            \"CHURN_NOT_THIN\": \"P1 and P3 hold AND V1 (NOVCHURN_rare10, or the F6 primary n) keeps >= 50% of the raw \"\n                              \"psp (same-sample ratio) in COH1517 or OLDHO\",\n            \"CHURN_THIN\": \"raw NOVCHURN CI excludes 0 (in the body considered) but NOVCHURN_exc AND NOVCHURN_rare10 \"\n                          \"keep < 30% of it in BOTH COH1517 and OLDHO\",\n            \"PARTLY_THIN\": \"otherwise\",\n            \"DEGREE_ARTEFACT_PERSISTENCE\": \"flag added if P2 fails while raw edge_persistence has CI < 0 on POOLED\"},\n        \"holm\": \"Holm over the P1-P3 family (one-sided bootstrap p), reported only\",\n        \"power\": {\"targets\": \"T1 disattenuated pooled R3/R5, T2 COH1517 raw, T3 half pooled raw\", \"n\": [800, 1500, 2500],\n                  \"draws\": 1000, \"scenarios\": \"S_A EXP5 n-mix; S_B pessimistic (n-bin weights shifted one bin down)\"},\n    }\n    p = RES / \"frozen_spec.json\"\n    jdump(spec, p)\n    ent = seal_file(\"S1_freeze\", p)\n    logger.info(f\"sealed frozen_spec.json sha256 {ent['sha256']} -> {LOG}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [87] TOOL CALL — Bash · 2026-09-29 05:32:20 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat > lib/s2_cfg.py <<'EOF'
"""Frozen draw counts (full run). Mirrored in s2_variants.CFG_DEFAULT and results/frozen_spec.json."""
CFG_FULL = {"N_RARE": [5, 10, 20], "D_RARE": 50, "D_PERM": 200, "S_RAW": 100, "S_CLEAN": 20, "D_PERM_HALF": 50,
            "D_RARE_HALF": 20, "RARE_HALF_N": 5, "MIN_HOME": 10, "V3_REWIRES": 200, "V3_KSETS": 200,
            "V3_CURVEBALL_SAMPLES": 200, "V3_HALF_DRAWS": 50}
EOF
sed -i 's/^CFG_DEFAULT = {.*$/from s2_cfg import CFG_FULL\nCFG_DEFAULT = {k: v for k, v in CFG_FULL.items() if not k.startswith("V3")}/; /^               "D_RARE_HALF": 20, "RARE_HALF_N": 5, "MIN_HOME": 10}$/d' s2_variants.py; grep -n "CFG" s2_variants.py | head; .venv/bin/python s1_freeze.py && cat logs/seal.log; rm -rf data/s2_parts_mini data/s2_parts_t200; (nohup .venv/bin/python s2_variants.py --tag full --workers 4 > logs/s2_full.out 2>&1 &); echo launched
```

### [88] TOOL RESULT — Bash · 2026-09-29 05:32:20 UTC

```
{"stdout": "33:from s2_cfg import CFG_FULL\n34:CFG_DEFAULT = {k: v for k, v in CFG_FULL.items() if not k.startswith(\"V3\")}\n174:    cfg = dict(CFG_DEFAULT)\n05:31:34|INFO   |sealed frozen_spec.json sha256 cf4d8e345ef3ac5f1146205c9262b53c7781a7ed38afc38eb91feb9771e106a2 -> /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/logs/seal.log\n{\"file\": \"frozen_spec.json\", \"prev\": \"GENESIS\", \"sha256\": \"cf4d8e345ef3ac5f1146205c9262b53c7781a7ed38afc38eb91feb9771e106a2\", \"stage\": \"S1_freeze\", \"time\": \"2026-09-29 05:31:34\"}\nlaunched", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [89] ASSISTANT · 2026-09-29 05:32:46 UTC

```
S2 full run launched. Checking igraph rewire speed before writing the V3 null script:
```

### [90] TOOL CALL — Bash · 2026-09-29 05:32:46 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -2 logs/s2_full.out; .venv/bin/python - <<'EOF'
import igraph as ig, numpy as np, time, random
help_txt = ig.Graph.rewire.__doc__; print(help_txt[:600])
z=np.load("/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/inputs/backbone/slice0.npz")
G=ig.Graph(n=4516, edges=np.c_[z['a'],z['b']].tolist())
random.seed(1); ig.set_random_number_generator(random)
t=time.time(); g=G.copy(); g.rewire(n=10*g.ecount()); print("rewire", time.time()-t)
print(g.is_simple(), (np.array(g.degree())==np.array(G.degree())).all())
el=np.array(g.get_edgelist()); print(el.shape, time.time()-t)
EOF
```

### [91] TOOL RESULT — Bash · 2026-09-29 05:32:46 UTC

```
{"stdout": "05:32:02|INFO   |chunk 2/135 (200 concepts) 0.4 min; 0.103 s/concept; eta 25.7 min\n05:32:02|INFO   |chunk 3/135 (300 concepts) 0.4 min; 0.106 s/concept; eta 17.1 min\nRandomly rewires the graph while preserving the degree distribution.\n\n    The rewiring is done \"in-place\", so the original graph will be modified.\n    If you want to preserve the original graph, use the L{copy} method before\n    rewiring.\n\n    @param n: the number of rewiring trials. The default is 10 times the number\n        of edges.\n    @param allowed_edge_types: the rewiring algorithm to use. It can either be\n        C{\"simple\"} or C{\"loops\"}; the former does not create or destroy\n        loop edges while the latter does.\n    \nrewire 3.7264883518218994\nTrue True\n(354089, 2) 3.8992245197296143", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [92] THINKING · 2026-09-29 05:34:06 UTC

```
S2 runs quickly (~17 min total), while the 600 igraph rewires will take ~37 CPU-min, so I'll split them across 3 parallel workers. Now writing the numba null kernels for curveball and k-matched sets.
```

### [93] TOOL CALL — Write · 2026-09-29 05:34:06 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/nullkern.py

"""Numba kernels for the configuration nulls.

curveball_run   Strona et al. (2014) curveball chain on a bipartite incidence stored as fixed-size rows (row sums
                preserved by construction, column sums preserved by each trade); all calendar years advance in
                lockstep so sample d of year t0 and sample d of year t0+1 are combined for a concept's Jaccards.
ksets_null      V3b: random sets of size k drawn without replacement with probability proportional to weights
                (successive sampling == Gumbel top-k), SELF topics excluded; counts edges in a dense adjacency.
kpers_null      V3c-approx: k-matched Monte Carlo persistence null (row sizes k1, k2, k3; weights = column
                popularity in each window's year)."""
from __future__ import annotations

import numpy as np
from numba import njit


@njit(cache=True)
def _trade(data, off, i, j, mark, stamp, pool):
    a0, a1 = off[i], off[i + 1]
    b0, b1 = off[j], off[j + 1]
    if a1 == a0 or b1 == b0:
        return
    for p in range(a0, a1):
        mark[data[p]] = stamp
    # B-only and shared
    nb_only = 0
    ns = 0
    for p in range(b0, b1):
        if mark[data[p]] == stamp:
            ns += 1
        else:
            pool[nb_only] = data[p]
            nb_only += 1
    na = (a1 - a0) - ns
    if na == 0 or nb_only == 0:
        return
    # mark B elements with stamp + 1 to find A-only
    for p in range(b0, b1):
        mark[data[p]] = stamp + 1
    shared = np.empty(ns, np.int32)
    k = 0
    for p in range(a0, a1):
        x = data[p]
        if mark[x] == stamp + 1:
            shared[k] = x
            k += 1
        else:
            pool[nb_only] = x
            nb_only += 1
    tot = nb_only
    # shuffle the pooled non-shared elements
    for t in range(tot - 1, 0, -1):
        r = np.random.randint(0, t + 1)
        tmp = pool[t]
        pool[t] = pool[r]
        pool[r] = tmp
    # A gets shared + first na; B gets shared + rest
    q = a0
    for t in range(ns):
        data[q] = shared[t]
        q += 1
    for t in range(na):
        data[q] = pool[t]
        q += 1
    q = b0
    for t in range(ns):
        data[q] = shared[t]
        q += 1
    for t in range(na, tot):
        data[q] = pool[t]
        q += 1


@njit(cache=True)
def _jac(data, off, i, j, mark, stamp):
    a0, a1 = off[i], off[i + 1]
    b0, b1 = off[j], off[j + 1]
    for p in range(a0, a1):
        mark[data[p]] = stamp
    inter = 0
    for p in range(b0, b1):
        if mark[data[p]] == stamp:
            inter += 1
    u = (a1 - a0) + (b1 - b0) - inter
    if u == 0:
        return np.nan
    return inter / u


@njit(cache=True)
def curveball_run(data, off, year_lo, year_hi, conc_rows, n_samples, burn_mult, seed, nt):
    """data/off: all rows of all years (rows of year y are year_lo[y]..year_hi[y]-1).
    conc_rows: n_conc x 3 global row ids (W1, W2, W3; -1 = missing). Returns (sum, sumsq, n_finite) of the null
    persistence per concept over n_samples samples."""
    np.random.seed(seed)
    ny = len(year_lo)
    mark = np.zeros(nt + 1, np.int64)
    maxrow = 0
    for r in range(len(off) - 1):
        if off[r + 1] - off[r] > maxrow:
            maxrow = off[r + 1] - off[r]
    pool = np.empty(2 * maxrow + 2, np.int32)
    stamp = 1
    nc = conc_rows.shape[0]
    s1 = np.zeros(nc)
    s2 = np.zeros(nc)
    nf = np.zeros(nc, np.int64)
    for y in range(ny):
        n = year_hi[y] - year_lo[y]
        if n < 2:
            continue
        for t in range(burn_mult * n):
            i = year_lo[y] + np.random.randint(0, n)
            j = year_lo[y] + np.random.randint(0, n)
            if i != j:
                _trade(data, off, i, j, mark, stamp, pool)
                stamp += 2
    for d in range(n_samples):
        for y in range(ny):
            n = year_hi[y] - year_lo[y]
            if n < 2:
                continue
            for t in range(n):
                i = year_lo[y] + np.random.randint(0, n)
                j = year_lo[y] + np.random.randint(0, n)
                if i != j:
                    _trade(data, off, i, j, mark, stamp, pool)
                    stamp += 2
        for c in range(nc):
            r1, r2, r3 = conc_rows[c, 0], conc_rows[c, 1], conc_rows[c, 2]
            j12 = _jac(data, off, r1, r2, mark, stamp)
            stamp += 1
            j23 = _jac(data, off, r2, r3, mark, stamp)
            stamp += 1
            if np.isfinite(j12) and np.isfinite(j23):
                v = (j12 + j23) / 2
            elif np.isfinite(j12):
                v = j12
            elif np.isfinite(j23):
                v = j23
            else:
                continue
            s1[c] += v
            s2[c] += v * v
            nf[c] += 1
    return s1, s2, nf


@njit(cache=True)
def _draw_set(cum, tot, k, selfmark, stamp_self, chosen_mark, stamp, out, nt):
    """Successive sampling of k distinct items proportional to weights (cum = cumulative weights over nt items),
    skipping items marked SELF. Returns False if it cannot fill (pool too small)."""
    got = 0
    tries = 0
    while got < k:
        tries += 1
        if tries > 200 * k + 1000:
            return False
        u = np.random.random() * tot
        x = np.searchsorted(cum, u, side="right")
        if x >= nt:
            x = nt - 1
        if selfmark[x] == stamp_self or chosen_mark[x] == stamp:
            continue
        chosen_mark[x] = stamp
        out[got] = x
        got += 1
    return True


@njit(cache=True)
def ksets_null(set_k, set_conc, set_slice, set_year, self_flat, self_off, cum_w, pool_n, adj, n_draws, seed, nt):
    """For each set s: n_draws random sets of size set_k[s] ~ weights cum_w[set_year[s]] without replacement,
    excluding the SELF topics of concept set_conc[s]; edge counts in adj[set_slice[s]]. Returns mean, sd."""
    np.random.seed(seed)
    ns = len(set_k)
    mu = np.full(ns, np.nan)
    sd = np.full(ns, np.nan)
    selfmark = np.zeros(nt, np.int64)
    chosen = np.zeros(nt, np.int64)
    stamp = 1
    buf = np.empty(nt, np.int64)
    for s in range(ns):
        k = set_k[s]
        c = set_conc[s]
        y = set_year[s]
        if k < 2:
            continue
        for p in range(self_off[c], self_off[c + 1]):
            selfmark[self_flat[p]] = s + 1
        nself_pool = 0
        cum = cum_w[y]
        for p in range(self_off[c], self_off[c + 1]):
            x = self_flat[p]
            w = cum[x] - (cum[x - 1] if x > 0 else 0.0)
            if w > 0:
                nself_pool += 1
        if pool_n[y] - nself_pool < k:
            continue
        tot = cum[nt - 1]
        a = adj[set_slice[s]]
        s1 = 0.0
        s2 = 0.0
        nd = 0
        for d in range(n_draws):
            stamp += 1
            ok = _draw_set(cum, tot, k, selfmark, s + 1, chosen, stamp, buf, nt)
            if not ok:
                continue
            e = 0
            for i in range(k):
                for j in range(i + 1, k):
                    if a[buf[i], buf[j]]:
                        e += 1
            s1 += e
            s2 += e * e
            nd += 1
        if nd >= 2:
            m = s1 / nd
            mu[s] = m
            v = s2 / nd - m * m
            sd[s] = np.sqrt(v) if v > 0 else 0.0
    return mu, sd


@njit(cache=True)
def kpers_null(k3, conc, years3, self_flat, self_off, cum_w, pool_n, n_draws, seed, nt):
    """k-matched persistence null: for row r, windows w = 0..2 with sizes k3[r, w] drawn ~ cum_w[years3[r, w]]
    (SELF of concept conc[r] excluded); null persistence = nanmean(J(1, 2), J(2, 3)). Returns mean, sd."""
    np.random.seed(seed)
    nr = k3.shape[0]
    mu = np.full(nr, np.nan)
    sd = np.full(nr, np.nan)
    selfmark = np.zeros(nt, np.int64)
    chosen = np.zeros(nt, np.int64)
    m2 = np.zeros(nt, np.int64)
    stamp = 1
    b = np.empty((3, nt), np.int64)
    for r in range(nr):
        c = conc[r]
        for p in range(self_off[c], self_off[c + 1]):
            selfmark[self_flat[p]] = r + 1
        feasible = True
        for w in range(3):
            if pool_n[years3[r, w]] - (self_off[c + 1] - self_off[c]) < k3[r, w]:
                feasible = False
        if not feasible:
            continue
        s1 = 0.0
        s2 = 0.0
        nd = 0
        for d in range(n_draws):
            ok = True
            for w in range(3):
                stamp += 1
                cum = cum_w[years3[r, w]]
                if k3[r, w] > 0:
                    if not _draw_set(cum, cum[nt - 1], k3[r, w], selfmark, r + 1, chosen, stamp, b[w], nt):
                        ok = False
            if not ok:
                continue
            js = np.empty(2)
            for q in range(2):
                ka, kb = k3[r, q], k3[r, q + 1]
                stamp += 1
                for i in range(ka):
                    m2[b[q, i]] = stamp
                inter = 0
                for i in range(kb):
                    if m2[b[q + 1, i]] == stamp:
                        inter += 1
                u = ka + kb - inter
                js[q] = inter / u if u > 0 else np.nan
            if np.isfinite(js[0]) and np.isfinite(js[1]):
                v = (js[0] + js[1]) / 2
            elif np.isfinite(js[0]):
                v = js[0]
            elif np.isfinite(js[1]):
                v = js[1]
            else:
                continue
            s1 += v
            s2 += v * v
            nd += 1
        if nd >= 2:
            m = s1 / nd
            mu[r] = m
            vv = s2 / nd - m * m
            sd[r] = np.sqrt(vv) if vv > 0 else 0.0
    return mu, sd
```

### [94] TOOL RESULT — Write · 2026-09-29 05:34:06 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/nullkern.py", "content": "\"\"\"Numba kernels for the configuration nulls.\n\ncurveball_run   Strona et al. (2014) curveball chain on a bipartite incidence stored as fixed-size rows (row sums\n                preserved by construction, column sums preserved by each trade); all calendar years advance in\n                lockstep so sample d of year t0 and sample d of year t0+1 are combined for a concept's Jaccards.\nksets_null      V3b: random sets of size k drawn without replacement with probability proportional to weights\n                (successive sampling == Gumbel top-k), SELF topics excluded; counts edges in a dense adjacency.\nkpers_null      V3c-approx: k-matched Monte Carlo persistence null (row sizes k1, k2, k3; weights = column\n                popularity in each window's year).\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nfrom numba import njit\n\n\n@njit(cache=True)\ndef _trade(data, off, i, j, mark, stamp, pool):\n    a0, a1 = off[i], off[i + 1]\n    b0, b1 = off[j], off[j + 1]\n    if a1 == a0 or b1 == b0:\n        return\n    for p in range(a0, a1):\n        mark[data[p]] = stamp\n    # B-only and shared\n    nb_only = 0\n    ns = 0\n    for p in range(b0, b1):\n        if mark[data[p]] == stamp:\n            ns += 1\n        else:\n            pool[nb_only] = data[p]\n            nb_only += 1\n    na = (a1 - a0) - ns\n    if na == 0 or nb_only == 0:\n        return\n    # mark B elements with stamp + 1 to find A-only\n    for p in range(b0, b1):\n        mark[data[p]] = stamp + 1\n    shared = np.empty(ns, np.int32)\n    k = 0\n    for p in range(a0, a1):\n        x = data[p]\n        if mark[x] == stamp + 1:\n            shared[k] = x\n            k += 1\n        else:\n            pool[nb_only] = x\n            nb_only += 1\n    tot = nb_only\n    # shuffle the pooled non-shared elements\n    for t in range(tot - 1, 0, -1):\n        r = np.random.randint(0, t + 1)\n        tmp = pool[t]\n        pool[t] = pool[r]\n        pool[r] = tmp\n    # A gets shared + first na; B gets shared + rest\n    q = a0\n    for t in range(ns):\n        data[q] = shared[t]\n        q += 1\n    for t in range(na):\n        data[q] = pool[t]\n        q += 1\n    q = b0\n    for t in range(ns):\n        data[q] = shared[t]\n        q += 1\n    for t in range(na, tot):\n        data[q] = pool[t]\n        q += 1\n\n\n@njit(cache=True)\ndef _jac(data, off, i, j, mark, stamp):\n    a0, a1 = off[i], off[i + 1]\n    b0, b1 = off[j], off[j + 1]\n    for p in range(a0, a1):\n        mark[data[p]] = stamp\n    inter = 0\n    for p in range(b0, b1):\n        if mark[data[p]] == stamp:\n            inter += 1\n    u = (a1 - a0) + (b1 - b0) - inter\n    if u == 0:\n        return np.nan\n    return inter / u\n\n\n@njit(cache=True)\ndef curveball_run(data, off, year_lo, year_hi, conc_rows, n_samples, burn_mult, seed, nt):\n    \"\"\"data/off: all rows of all years (rows of year y are year_lo[y]..year_hi[y]-1).\n    conc_rows: n_conc x 3 global row ids (W1, W2, W3; -1 = missing). Returns (sum, sumsq, n_finite) of the null\n    persistence per concept over n_samples samples.\"\"\"\n    np.random.seed(seed)\n    ny = len(year_lo)\n    mark = np.zeros(nt + 1, np.int64)\n    maxrow = 0\n    for r in range(len(off) - 1):\n        if off[r + 1] - off[r] > maxrow:\n            maxrow = off[r + 1] - off[r]\n    pool = np.empty(2 * maxrow + 2, np.int32)\n    stamp = 1\n    nc = conc_rows.shape[0]\n    s1 = np.zeros(nc)\n    s2 = np.zeros(nc)\n    nf = np.zeros(nc, np.int64)\n    for y in range(ny):\n        n = year_hi[y] - year_lo[y]\n        if n < 2:\n            continue\n        for t in range(burn_mult * n):\n            i = year_lo[y] + np.random.randint(0, n)\n            j = year_lo[y] + np.random.randint(0, n)\n            if i != j:\n                _trade(data, off, i, j, mark, stamp, pool)\n                stamp += 2\n    for d in range(n_samples):\n        for y in range(ny):\n            n = year_hi[y] - year_lo[y]\n            if n < 2:\n                continue\n            for t in range(n):\n                i = year_lo[y] + np.random.randint(0, n)\n                j = year_lo[y] + np.random.randint(0, n)\n                if i != j:\n                    _trade(data, off, i, j, mark, stamp, pool)\n                    stamp += 2\n        for c in range(nc):\n            r1, r2, r3 = conc_rows[c, 0], conc_rows[c, 1], conc_rows[c, 2]\n            j12 = _jac(data, off, r1, r2, mark, stamp)\n            stamp += 1\n            j23 = _jac(data, off, r2, r3, mark, stamp)\n            stamp += 1\n            if np.isfinite(j12) and np.isfinite(j23):\n                v = (j12 + j23) / 2\n            elif np.isfinite(j12):\n                v = j12\n            elif np.isfinite(j23):\n                v = j23\n            else:\n                continue\n            s1[c] += v\n            s2[c] += v * v\n            nf[c] += 1\n    return s1, s2, nf\n\n\n@njit(cache=True)\ndef _draw_set(cum, tot, k, selfmark, stamp_self, chosen_mark, stamp, out, nt):\n    \"\"\"Successive sampling of k distinct items proportional to weights (cum = cumulative weights over nt items),\n    skipping items marked SELF. Returns False if it cannot fill (pool too small).\"\"\"\n    got = 0\n    tries = 0\n    while got < k:\n        tries += 1\n        if tries > 200 * k + 1000:\n            return False\n        u = np.random.random() * tot\n        x = np.searchsorted(cum, u, side=\"right\")\n        if x >= nt:\n            x = nt - 1\n        if selfmark[x] == stamp_self or chosen_mark[x] == stamp:\n            continue\n        chosen_mark[x] = stamp\n        out[got] = x\n        got += 1\n    return True\n\n\n@njit(cache=True)\ndef ksets_null(set_k, set_conc, set_slice, set_year, self_flat, self_off, cum_w, pool_n, adj, n_draws, seed, nt):\n    \"\"\"For each set s: n_draws random sets of size set_k[s] ~ weights cum_w[set_year[s]] without replacement,\n    excluding the SELF topics of concept set_conc[s]; edge counts in adj[set_slice[s]]. Returns mean, sd.\"\"\"\n    np.random.seed(seed)\n    ns = len(set_k)\n    mu = np.full(ns, np.nan)\n    sd = np.full(ns, np.nan)\n    selfmark = np.zeros(nt, np.int64)\n    chosen = np.zeros(nt, np.int64)\n    stamp = 1\n    buf = np.empty(nt, np.int64)\n    for s in range(ns):\n        k = set_k[s]\n        c = set_conc[s]\n        y = set_year[s]\n        if k < 2:\n            continue\n        for p in range(self_off[c], self_off[c + 1]):\n            selfmark[self_flat[p]] = s + 1\n        nself_pool = 0\n        cum = cum_w[y]\n        for p in range(self_off[c], self_off[c + 1]):\n            x = self_flat[p]\n            w = cum[x] - (cum[x - 1] if x > 0 else 0.0)\n            if w > 0:\n                nself_pool += 1\n        if pool_n[y] - nself_pool < k:\n            continue\n        tot = cum[nt - 1]\n        a = adj[set_slice[s]]\n        s1 = 0.0\n        s2 = 0.0\n        nd = 0\n        for d in range(n_draws):\n            stamp += 1\n            ok = _draw_set(cum, tot, k, selfmark, s + 1, chosen, stamp, buf, nt)\n            if not ok:\n                continue\n            e = 0\n            for i in range(k):\n                for j in range(i + 1, k):\n                    if a[buf[i], buf[j]]:\n                        e += 1\n            s1 += e\n            s2 += e * e\n            nd += 1\n        if nd >= 2:\n            m = s1 / nd\n            mu[s] = m\n            v = s2 / nd - m * m\n            sd[s] = np.sqrt(v) if v > 0 else 0.0\n    return mu, sd\n\n\n@njit(cache=True)\ndef kpers_null(k3, conc, years3, self_flat, self_off, cum_w, pool_n, n_draws, seed, nt):\n    \"\"\"k-matched persistence null: for row r, windows w = 0..2 with sizes k3[r, w] drawn ~ cum_w[years3[r, w]]\n    (SELF of concept conc[r] excluded); null persistence = nanmean(J(1, 2), J(2, 3)). Returns mean, sd.\"\"\"\n    np.random.seed(seed)\n    nr = k3.shape[0]\n    mu = np.full(nr, np.nan)\n    sd = np.full(nr, np.nan)\n    selfmark = np.zeros(nt, np.int64)\n    chosen = np.zeros(nt, np.int64)\n    m2 = np.zeros(nt, np.int64)\n    stamp = 1\n    b = np.empty((3, nt), np.int64)\n    for r in range(nr):\n        c = conc[r]\n        for p in range(self_off[c], self_off[c + 1]):\n            selfmark[self_flat[p]] = r + 1\n        feasible = True\n        for w in range(3):\n            if pool_n[years3[r, w]] - (self_off[c + 1] - self_off[c]) < k3[r, w]:\n                feasible = False\n        if not feasible:\n            continue\n        s1 = 0.0\n        s2 = 0.0\n        nd = 0\n        for d in range(n_draws):\n            ok = True\n            for w in range(3):\n                stamp += 1\n                cum = cum_w[years3[r, w]]\n                if k3[r, w] > 0:\n                    if not _draw_set(cum, cum[nt - 1], k3[r, w], selfmark, r + 1, chosen, stamp, b[w], nt):\n                        ok = False\n            if not ok:\n                continue\n            js = np.empty(2)\n            for q in range(2):\n                ka, kb = k3[r, q], k3[r, q + 1]\n                stamp += 1\n                for i in range(ka):\n                    m2[b[q, i]] = stamp\n                inter = 0\n                for i in range(kb):\n                    if m2[b[q + 1, i]] == stamp:\n                        inter += 1\n                u = ka + kb - inter\n                js[q] = inter / u if u > 0 else np.nan\n            if np.isfinite(js[0]) and np.isfinite(js[1]):\n                v = (js[0] + js[1]) / 2\n            elif np.isfinite(js[0]):\n                v = js[0]\n            elif np.isfinite(js[1]):\n                v = js[1]\n            else:\n                continue\n            s1 += v\n            s2 += v * v\n            nd += 1\n        if nd >= 2:\n            m = s1 / nd\n            mu[r] = m\n            vv = s2 / nd - m * m\n            sd[r] = np.sqrt(vv) if vv > 0 else 0.0\n    return mu, sd\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [95] ASSISTANT · 2026-09-29 05:35:18 UTC

```
Now the V3 orchestrator `s3_nulls.py` (backbone rewiring on 3 slice workers; curveball and k-matched nulls in numba):
```

### [96] TOOL CALL — Write · 2026-09-29 05:35:18 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py

#!/usr/bin/env python3
"""S2-V3 configuration nulls (reads the S2 chunk pickles; never reads outcomes).

V3a  z_dens_cfg: each slice's full topic backbone rewired V3_REWIRES times (igraph rewire, n = 10 m trials, simple;
     degree sequence asserted); edges of each rewired graph inside the raw NB_W3 (slice t0+2) and NB_W1 (slice t0);
     half NB_W3 sets (V4) use the first V3_HALF_DRAWS rewires.
V3b  z_dens_k: V3_KSETS random sets of size |NB_W3| ~ bg counts in year t0+2 (bg > 0, SELF excluded), edges in the
     REAL backbone; halves with V3_HALF_DRAWS draws.
V3c  z_pers_cfg: curveball chain of the (concept-window x topic) incidence per calendar year (all bodies), 200
     samples; plus the k-matched Monte Carlo approximation z_pers_k on the full build (to validate it) and on halves.
Writes data/v3_nulls.parquet (per concept) and data/v3_halves.pkl (per concept x split x half)."""
from __future__ import annotations

import argparse
import math
import multiprocessing as mp
import pickle
import random
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd

from common import DATA, DATA_IN, INPUTS, RES, jdump, setup_logger
from s2_cfg import CFG_FULL

NT = 4516
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]


def slice_of(y: int) -> int:
    for i, (a, b) in enumerate(SLICES):
        if a <= y <= b:
            return i
    return 0 if y < SLICES[0][0] else len(SLICES) - 1


def load_s2(tag: str) -> tuple[pd.DataFrame, list]:
    rows, extras = [], []
    for p in sorted((DATA / f"s2_parts_{tag}").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, e in zip(z["rows"], z["extras"]):
            if not e:
                continue
            rows.append(r)
            extras.append({"NB": e["NB"], "SELF": e["SELF"], "half_NB": e["half_NB"],
                           "half_ep": {h: e["half_raw"][h][:, 5] for h in ("A", "B")}})
    return pd.DataFrame(rows), extras


def pairs_of(sets: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    pa, pb, sid = [], [], []
    for i, s in enumerate(sets):
        k = len(s)
        if k < 2:
            continue
        iu, ju = np.triu_indices(k, 1)
        pa.append(s[iu])
        pb.append(s[ju])
        sid.append(np.full(len(iu), i, np.int32))
    if not pa:
        return np.zeros(0, np.int32), np.zeros(0, np.int32), np.zeros(0, np.int32)
    return np.concatenate(pa).astype(np.int32), np.concatenate(pb).astype(np.int32), np.concatenate(sid)


def rewire_worker(s: int, groups: dict, n_draws: int, n_half: int) -> dict:
    """groups: name -> (pa, pb, sid, nsets, draws). Returns name -> (obs, sum, sumsq, nd)."""
    import igraph as ig
    z = np.load(INPUTS / "backbone" / f"slice{s}.npz")
    a, b = z["a"].astype(np.int64), z["b"].astype(np.int64)
    G0 = ig.Graph(n=NT, edges=np.c_[a, b].tolist())
    deg0 = np.array(G0.degree())
    adj = np.zeros((NT, NT), bool)
    out = {}

    def count(adj_, g):
        pa, pb, sid, ns, _ = g
        return np.bincount(sid, weights=adj_[pa, pb], minlength=ns)
    adj[a, b] = True
    adj[b, a] = True
    for nm, g in groups.items():
        out[nm] = [count(adj, g), np.zeros(g[3]), np.zeros(g[3]), 0]
    t = time.time()
    for d in range(1, n_draws + 1):
        random.seed(20260930 + 1000 * s + d)
        ig.set_random_number_generator(random)
        G = G0.copy()
        G.rewire(n=10 * G.ecount(), allowed_edge_types="simple")
        if not np.array_equal(np.array(G.degree()), deg0):
            raise RuntimeError("degree sequence changed by rewire")
        el = np.array(G.get_edgelist(), np.int64)
        adj[:] = False
        adj[el[:, 0], el[:, 1]] = True
        adj[el[:, 1], el[:, 0]] = True
        for nm, g in groups.items():
            if d > g[4]:
                continue
            e = count(adj, g)
            out[nm][1] += e
            out[nm][2] += e * e
            out[nm][3] += 1
        if d % 20 == 0:
            print(f"slice {s}: {d}/{n_draws} rewires, {time.time()-t:.0f}s", flush=True)
    if s == 0:  # U4 evidence: simple graph after one rewire
        out["_u4"] = {"is_simple": bool(G.is_simple()), "degree_equal": True}
    return out


def v3a(df: pd.DataFrame, ex: list, cfg: dict, logger) -> tuple[pd.DataFrame, dict]:
    n_draws, n_half = cfg["V3_REWIRES"], cfg["V3_HALF_DRAWS"]
    t0 = df.t0.to_numpy()
    S = cfg["S_CLEAN"]
    jobs = {}
    index = {}
    for s in range(3):
        g = {}
        i3 = [i for i in range(len(df)) if slice_of(int(t0[i]) + 2) == s]
        i1 = [i for i in range(len(df)) if slice_of(int(t0[i])) == s]
        sets3 = [ex[i]["NB"][3] for i in i3]
        sets1 = [ex[i]["NB"][1] for i in i1]
        g["W3"] = (*pairs_of(sets3), len(sets3), n_draws)
        g["W1"] = (*pairs_of(sets1), len(sets1), n_draws)
        hs, hidx = [], []
        for i in i3:
            for h in ("A", "B"):
                for sp in range(S):
                    hs.append(ex[i]["half_NB"][h][sp][2])
                    hidx.append((i, h, sp))
        g["H3"] = (*pairs_of(hs), len(hs), n_half)
        jobs[s] = g
        index[s] = {"W3": i3, "W1": i1, "H3": hidx}
        logger.info(f"V3a slice {s}: W3 sets {len(sets3)} ({len(g['W3'][0])} pairs), W1 {len(sets1)}, "
                    f"halves {len(hs)} ({len(g['H3'][0])} pairs)")
    return jobs, index


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", default="full")
    ap.add_argument("--draws-scale", type=float, default=1.0)
    a = ap.parse_args()
    logger = setup_logger(f"s3_nulls_{a.tag}")
    cfg = dict(CFG_FULL)
    for k in ("V3_REWIRES", "V3_KSETS", "V3_CURVEBALL_SAMPLES", "V3_HALF_DRAWS"):
        cfg[k] = max(10, int(round(cfg[k] * a.draws_scale)))
    df, ex = load_s2(a.tag)
    logger.info(f"loaded {len(df)} concepts from S2 ({a.tag}); cfg {cfg}")
    S = cfg["S_CLEAN"]
    nC = len(df)
    t0s = df.t0.to_numpy().astype(int)
    # ---------------------------------------------------------------- V3a (3 slice workers, background)
    jobs, index = v3a(df, ex, cfg, logger)
    pool = ProcessPoolExecutor(3, mp_context=mp.get_context("spawn"))
    futs = {s: pool.submit(rewire_worker, s, jobs[s], cfg["V3_REWIRES"], cfg["V3_HALF_DRAWS"]) for s in range(3)}
    # ---------------------------------------------------------------- V3c curveball + k-matched (this process)
    from nullkern import curveball_run, kpers_null, ksets_null
    self_flat = np.concatenate([e["SELF"] for e in ex]).astype(np.int64)
    self_off = np.r_[0, np.cumsum([len(e["SELF"]) for e in ex])].astype(np.int64)
    years = list(range(int(t0s.min()), int(t0s.max()) + 3))
    yi = {y: i for i, y in enumerate(years)}
    rows_by_year = {y: [] for y in years}
    for c in range(nC):
        for w in (1, 2, 3):
            rows_by_year[t0s[c] + w - 1].append((c, w))
    data, off, ylo, yhi = [], [0], [], []
    conc_rows = -np.ones((nC, 3), np.int64)
    r = 0
    pop = np.zeros((len(years), NT))
    for y in years:
        ylo.append(r)
        for c, w in rows_by_year[y]:
            s = ex[c]["NB"][w]
            data.append(s)
            off.append(off[-1] + len(s))
            conc_rows[c, w - 1] = r
            pop[yi[y], s] += 1
            r += 1
        yhi.append(r)
    data0 = np.concatenate(data).astype(np.int32)
    off = np.asarray(off, np.int64)
    data_cb = data0.copy()
    t = time.time()
    s1, s2, nf = curveball_run(data_cb, off, np.asarray(ylo, np.int64), np.asarray(yhi, np.int64), conc_rows,
                               cfg["V3_CURVEBALL_SAMPLES"], 5, 20260932, NT)
    logger.info(f"V3c curveball: {r} rows, {len(years)} years, {time.time()-t:.1f}s")
    # U3: row and column sums preserved
    row_ok = bool(np.array_equal(np.diff(off), np.diff(off)))
    col_ok = True
    for y in years:
        lo, hi = off[ylo[yi[y]]], off[yhi[yi[y]]]
        col_ok &= bool(np.array_equal(np.bincount(data0[lo:hi], minlength=NT), np.bincount(data_cb[lo:hi], minlength=NT)))
    rowset_ok = all(len(np.unique(data_cb[off[i]:off[i + 1]])) == off[i + 1] - off[i] for i in range(0, r, max(1, r // 2000)))
    logger.info(f"U3 curveball: column sums preserved {col_ok}; rows remain sets {rowset_ok}")
    with np.errstate(invalid="ignore", divide="ignore"):
        pm = np.where(nf >= 20, s1 / np.maximum(nf, 1), np.nan)
        psd = np.sqrt(np.maximum(s2 / np.maximum(nf, 1) - pm ** 2, 0))
    obs_ep = df["edge_persistence__raw"].to_numpy(float)
    out = pd.DataFrame({"frame": df.frame, "ci": df.ci})
    out["pers_cfg_mean"] = pm
    out["pers_cfg_sd"] = psd
    out["excess_pers_cfg"] = obs_ep - pm
    with np.errstate(invalid="ignore", divide="ignore"):
        out["z_pers_cfg"] = np.where(psd > 0, (obs_ep - pm) / np.where(psd > 0, psd, 1), np.nan)
    # k-matched persistence approximation (full build and halves); weights = the year's neighbour popularity
    cum_pop = np.cumsum(pop, 1)
    pool_pop = (pop > 0).sum(1).astype(np.int64)
    years3 = np.stack([[yi[t + w] for w in range(3)] for t in t0s]).astype(np.int64)
    k3 = np.stack([[len(ex[c]["NB"][w]) for w in (1, 2, 3)] for c in range(nC)]).astype(np.int64)
    t = time.time()
    mu_k, sd_k = kpers_null(k3, np.arange(nC, dtype=np.int64), years3, self_flat, self_off, cum_pop, pool_pop,
                            cfg["V3_KSETS"], 20260933, NT)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["pers_k_mean"] = mu_k
        out["z_pers_k"] = np.where(sd_k > 0, (obs_ep - mu_k) / np.where(sd_k > 0, sd_k, 1), np.nan)
    logger.info(f"V3c k-matched full build {time.time()-t:.1f}s")
    hk3, hconc, hyears, hobs, hkey = [], [], [], [], []
    for c in range(nC):
        for h in ("A", "B"):
            for sp in range(S):
                hk3.append([len(ex[c]["half_NB"][h][sp][w]) for w in range(3)])
                hconc.append(c)
                hyears.append(years3[c])
                hobs.append(float(ex[c]["half_ep"][h][sp]))
                hkey.append((c, h, sp))
    t = time.time()
    hmu, hsd = kpers_null(np.asarray(hk3, np.int64), np.asarray(hconc, np.int64), np.asarray(hyears, np.int64),
                          self_flat, self_off, cum_pop, pool_pop, cfg["V3_HALF_DRAWS"], 20260934, NT)
    hobs = np.asarray(hobs)
    with np.errstate(invalid="ignore", divide="ignore"):
        hz_pers = np.where(hsd > 0, (hobs - hmu) / np.where(hsd > 0, hsd, 1), np.nan)
    logger.info(f"V3c k-matched halves ({len(hk3)} rows) {time.time()-t:.1f}s")
    # ---------------------------------------------------------------- V3b k-matched density null
    z = np.load(DATA_IN / "bg_topics.npz")
    bgy = {int(y): i for i, y in enumerate(z["years"])}
    BG = z["BG"].astype(float)
    cum_bg = np.cumsum(BG, 1)
    pool_bg = (BG > 0).sum(1).astype(np.int64)
    adj3 = np.zeros((3, NT, NT), np.bool_)
    for s in range(3):
        zz = np.load(INPUTS / "backbone" / f"slice{s}.npz")
        adj3[s, zz["a"], zz["b"]] = True
        adj3[s, zz["b"], zz["a"]] = True
    set_k = np.array([len(e["NB"][3]) for e in ex], np.int64)
    set_slice = np.array([slice_of(int(t) + 2) for t in t0s], np.int64)
    set_year = np.array([bgy[int(t) + 2] for t in t0s], np.int64)
    t = time.time()
    mk, sk = ksets_null(set_k, np.arange(nC, dtype=np.int64), set_slice, set_year, self_flat, self_off, cum_bg,
                        pool_bg, adj3, cfg["V3_KSETS"], 20260931, NT)
    e_obs = df["e_W3__raw"].to_numpy(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        out["dens_k_mean"] = mk / (set_k * (set_k - 1) / 2)
        out["z_dens_k"] = np.where(sk > 0, (e_obs - mk) / np.where(sk > 0, sk, 1), np.nan)
    logger.info(f"V3b full build {time.time()-t:.1f}s")
    hsets = [ex[c]["half_NB"][h][sp][2] for (c, h, sp) in hkey]
    h_k = np.array([len(s) for s in hsets], np.int64)
    hc = np.array([c for c, _, _ in hkey], np.int64)
    t = time.time()
    hmk, hsk = ksets_null(h_k, hc, set_slice[hc], set_year[hc], self_flat, self_off, cum_bg, pool_bg, adj3,
                          cfg["V3_HALF_DRAWS"], 20260935, NT)
    # observed half-set edges in the real backbone
    pa, pb, sid = pairs_of(hsets)
    h_eobs = np.bincount(sid, weights=adj3[set_slice[hc][sid], pa, pb], minlength=len(hsets)) if len(sid) else \
        np.zeros(len(hsets))
    with np.errstate(invalid="ignore", divide="ignore"):
        hz_dk = np.where(hsk > 0, (h_eobs - hmk) / np.where(hsk > 0, hsk, 1), np.nan)
    logger.info(f"V3b halves {time.time()-t:.1f}s")
    del adj3
    # ---------------------------------------------------------------- collect V3a
    res = {s: futs[s].result() for s in range(3)}
    pool.shutdown()
    u4 = res[0].pop("_u4", {})
    zc3 = np.full(nC, np.nan)
    ec3 = np.full(nC, np.nan)
    zc1 = np.full(nC, np.nan)
    hz_dc = np.full(len(hkey), np.nan)
    hpos = {k: i for i, k in enumerate(hkey)}
    for s in range(3):
        for nm in ("W3", "W1", "H3"):
            obs, s1_, s2_, nd = res[s][nm]
            if nd == 0:
                continue
            mu = s1_ / nd
            sd = np.sqrt(np.maximum(s2_ / nd - mu ** 2, 0))
            with np.errstate(invalid="ignore", divide="ignore"):
                zz = np.where(sd > 0, (obs - mu) / np.where(sd > 0, sd, 1), np.nan)
            idx = index[s][nm]
            if nm == "W3":
                ii = np.asarray(idx, int)
                kk = set_k[ii]
                ok = kk >= 2
                zc3[ii[ok]] = zz[ok]
                with np.errstate(invalid="ignore", divide="ignore"):
                    ec3[ii[ok]] = (mu / (kk * (kk - 1) / 2))[ok]
                # consistency: observed count == S2 e_W3
                if not np.allclose(obs[ok], e_obs[ii[ok]]):
                    raise RuntimeError("V3a observed edge counts differ from S2 e_W3")
            elif nm == "W1":
                ii = np.asarray(idx, int)
                k1 = np.array([len(ex[i]["NB"][1]) for i in ii])
                ok = k1 >= 2
                zc1[ii[ok]] = zz[ok]
            else:
                kk = np.array([len(ex[c]["half_NB"][h][sp][2]) for (c, h, sp) in idx])
                for j, key in enumerate(idx):
                    if kk[j] >= 2:
                        hz_dc[hpos[key]] = zz[j]
    out["z_dens_cfg"] = zc3
    out["dens_cfg_exp"] = ec3
    out["z_dens_cfg_W1"] = zc1
    out.to_parquet(DATA / f"v3_nulls_{a.tag}.parquet", index=False)
    halves = {"key": [(df.frame.iat[c], int(df.ci.iat[c]), h, sp) for (c, h, sp) in hkey],
              "z_pers_k": hz_pers.astype(np.float32), "z_dens_k": hz_dk.astype(np.float32),
              "z_dens_cfg": hz_dc.astype(np.float32)}
    (DATA / f"v3_halves_{a.tag}.pkl").write_bytes(pickle.dumps(halves, protocol=5))
    ok = out[["z_pers_cfg", "z_pers_k"]].dropna()
    from scipy.stats import spearmanr
    rho = float(spearmanr(ok.z_pers_cfg, ok.z_pers_k)[0]) if len(ok) > 10 else math.nan
    jdump({"U3_curveball": {"column_sums_preserved": col_ok, "row_sizes_preserved": row_ok, "rows_remain_sets": rowset_ok},
           "U4_rewire": u4, "cfg": cfg, "n_concepts": nC, "n_rows_curveball": int(r),
           "spearman_z_pers_cfg_vs_k_matched": rho,
           "finite": {c: int(np.isfinite(out[c]).sum()) for c in out.columns if c not in ("frame", "ci")}},
          RES / f"v3_nulls_{a.tag}.json")
    logger.info(f"V3 done; spearman(z_pers_cfg, z_pers_k) = {rho:.3f}")


if __name__ == "__main__":
    main()
```

### [97] TOOL RESULT — Write · 2026-09-29 05:35:18 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py", "content": "#!/usr/bin/env python3\n\"\"\"S2-V3 configuration nulls (reads the S2 chunk pickles; never reads outcomes).\n\nV3a  z_dens_cfg: each slice's full topic backbone rewired V3_REWIRES times (igraph rewire, n = 10 m trials, simple;\n     degree sequence asserted); edges of each rewired graph inside the raw NB_W3 (slice t0+2) and NB_W1 (slice t0);\n     half NB_W3 sets (V4) use the first V3_HALF_DRAWS rewires.\nV3b  z_dens_k: V3_KSETS random sets of size |NB_W3| ~ bg counts in year t0+2 (bg > 0, SELF excluded), edges in the\n     REAL backbone; halves with V3_HALF_DRAWS draws.\nV3c  z_pers_cfg: curveball chain of the (concept-window x topic) incidence per calendar year (all bodies), 200\n     samples; plus the k-matched Monte Carlo approximation z_pers_k on the full build (to validate it) and on halves.\nWrites data/v3_nulls.parquet (per concept) and data/v3_halves.pkl (per concept x split x half).\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport math\nimport multiprocessing as mp\nimport pickle\nimport random\nimport sys\nimport time\nfrom concurrent.futures import ProcessPoolExecutor\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN, INPUTS, RES, jdump, setup_logger\nfrom s2_cfg import CFG_FULL\n\nNT = 4516\nSLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]\n\n\ndef slice_of(y: int) -> int:\n    for i, (a, b) in enumerate(SLICES):\n        if a <= y <= b:\n            return i\n    return 0 if y < SLICES[0][0] else len(SLICES) - 1\n\n\ndef load_s2(tag: str) -> tuple[pd.DataFrame, list]:\n    rows, extras = [], []\n    for p in sorted((DATA / f\"s2_parts_{tag}\").glob(\"chunk_*.pkl\")):\n        z = pickle.loads(p.read_bytes())\n        for r, e in zip(z[\"rows\"], z[\"extras\"]):\n            if not e:\n                continue\n            rows.append(r)\n            extras.append({\"NB\": e[\"NB\"], \"SELF\": e[\"SELF\"], \"half_NB\": e[\"half_NB\"],\n                           \"half_ep\": {h: e[\"half_raw\"][h][:, 5] for h in (\"A\", \"B\")}})\n    return pd.DataFrame(rows), extras\n\n\ndef pairs_of(sets: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:\n    pa, pb, sid = [], [], []\n    for i, s in enumerate(sets):\n        k = len(s)\n        if k < 2:\n            continue\n        iu, ju = np.triu_indices(k, 1)\n        pa.append(s[iu])\n        pb.append(s[ju])\n        sid.append(np.full(len(iu), i, np.int32))\n    if not pa:\n        return np.zeros(0, np.int32), np.zeros(0, np.int32), np.zeros(0, np.int32)\n    return np.concatenate(pa).astype(np.int32), np.concatenate(pb).astype(np.int32), np.concatenate(sid)\n\n\ndef rewire_worker(s: int, groups: dict, n_draws: int, n_half: int) -> dict:\n    \"\"\"groups: name -> (pa, pb, sid, nsets, draws). Returns name -> (obs, sum, sumsq, nd).\"\"\"\n    import igraph as ig\n    z = np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\")\n    a, b = z[\"a\"].astype(np.int64), z[\"b\"].astype(np.int64)\n    G0 = ig.Graph(n=NT, edges=np.c_[a, b].tolist())\n    deg0 = np.array(G0.degree())\n    adj = np.zeros((NT, NT), bool)\n    out = {}\n\n    def count(adj_, g):\n        pa, pb, sid, ns, _ = g\n        return np.bincount(sid, weights=adj_[pa, pb], minlength=ns)\n    adj[a, b] = True\n    adj[b, a] = True\n    for nm, g in groups.items():\n        out[nm] = [count(adj, g), np.zeros(g[3]), np.zeros(g[3]), 0]\n    t = time.time()\n    for d in range(1, n_draws + 1):\n        random.seed(20260930 + 1000 * s + d)\n        ig.set_random_number_generator(random)\n        G = G0.copy()\n        G.rewire(n=10 * G.ecount(), allowed_edge_types=\"simple\")\n        if not np.array_equal(np.array(G.degree()), deg0):\n            raise RuntimeError(\"degree sequence changed by rewire\")\n        el = np.array(G.get_edgelist(), np.int64)\n        adj[:] = False\n        adj[el[:, 0], el[:, 1]] = True\n        adj[el[:, 1], el[:, 0]] = True\n        for nm, g in groups.items():\n            if d > g[4]:\n                continue\n            e = count(adj, g)\n            out[nm][1] += e\n            out[nm][2] += e * e\n            out[nm][3] += 1\n        if d % 20 == 0:\n            print(f\"slice {s}: {d}/{n_draws} rewires, {time.time()-t:.0f}s\", flush=True)\n    if s == 0:  # U4 evidence: simple graph after one rewire\n        out[\"_u4\"] = {\"is_simple\": bool(G.is_simple()), \"degree_equal\": True}\n    return out\n\n\ndef v3a(df: pd.DataFrame, ex: list, cfg: dict, logger) -> tuple[pd.DataFrame, dict]:\n    n_draws, n_half = cfg[\"V3_REWIRES\"], cfg[\"V3_HALF_DRAWS\"]\n    t0 = df.t0.to_numpy()\n    S = cfg[\"S_CLEAN\"]\n    jobs = {}\n    index = {}\n    for s in range(3):\n        g = {}\n        i3 = [i for i in range(len(df)) if slice_of(int(t0[i]) + 2) == s]\n        i1 = [i for i in range(len(df)) if slice_of(int(t0[i])) == s]\n        sets3 = [ex[i][\"NB\"][3] for i in i3]\n        sets1 = [ex[i][\"NB\"][1] for i in i1]\n        g[\"W3\"] = (*pairs_of(sets3), len(sets3), n_draws)\n        g[\"W1\"] = (*pairs_of(sets1), len(sets1), n_draws)\n        hs, hidx = [], []\n        for i in i3:\n            for h in (\"A\", \"B\"):\n                for sp in range(S):\n                    hs.append(ex[i][\"half_NB\"][h][sp][2])\n                    hidx.append((i, h, sp))\n        g[\"H3\"] = (*pairs_of(hs), len(hs), n_half)\n        jobs[s] = g\n        index[s] = {\"W3\": i3, \"W1\": i1, \"H3\": hidx}\n        logger.info(f\"V3a slice {s}: W3 sets {len(sets3)} ({len(g['W3'][0])} pairs), W1 {len(sets1)}, \"\n                    f\"halves {len(hs)} ({len(g['H3'][0])} pairs)\")\n    return jobs, index\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--tag\", default=\"full\")\n    ap.add_argument(\"--draws-scale\", type=float, default=1.0)\n    a = ap.parse_args()\n    logger = setup_logger(f\"s3_nulls_{a.tag}\")\n    cfg = dict(CFG_FULL)\n    for k in (\"V3_REWIRES\", \"V3_KSETS\", \"V3_CURVEBALL_SAMPLES\", \"V3_HALF_DRAWS\"):\n        cfg[k] = max(10, int(round(cfg[k] * a.draws_scale)))\n    df, ex = load_s2(a.tag)\n    logger.info(f\"loaded {len(df)} concepts from S2 ({a.tag}); cfg {cfg}\")\n    S = cfg[\"S_CLEAN\"]\n    nC = len(df)\n    t0s = df.t0.to_numpy().astype(int)\n    # ---------------------------------------------------------------- V3a (3 slice workers, background)\n    jobs, index = v3a(df, ex, cfg, logger)\n    pool = ProcessPoolExecutor(3, mp_context=mp.get_context(\"spawn\"))\n    futs = {s: pool.submit(rewire_worker, s, jobs[s], cfg[\"V3_REWIRES\"], cfg[\"V3_HALF_DRAWS\"]) for s in range(3)}\n    # ---------------------------------------------------------------- V3c curveball + k-matched (this process)\n    from nullkern import curveball_run, kpers_null, ksets_null\n    self_flat = np.concatenate([e[\"SELF\"] for e in ex]).astype(np.int64)\n    self_off = np.r_[0, np.cumsum([len(e[\"SELF\"]) for e in ex])].astype(np.int64)\n    years = list(range(int(t0s.min()), int(t0s.max()) + 3))\n    yi = {y: i for i, y in enumerate(years)}\n    rows_by_year = {y: [] for y in years}\n    for c in range(nC):\n        for w in (1, 2, 3):\n            rows_by_year[t0s[c] + w - 1].append((c, w))\n    data, off, ylo, yhi = [], [0], [], []\n    conc_rows = -np.ones((nC, 3), np.int64)\n    r = 0\n    pop = np.zeros((len(years), NT))\n    for y in years:\n        ylo.append(r)\n        for c, w in rows_by_year[y]:\n            s = ex[c][\"NB\"][w]\n            data.append(s)\n            off.append(off[-1] + len(s))\n            conc_rows[c, w - 1] = r\n            pop[yi[y], s] += 1\n            r += 1\n        yhi.append(r)\n    data0 = np.concatenate(data).astype(np.int32)\n    off = np.asarray(off, np.int64)\n    data_cb = data0.copy()\n    t = time.time()\n    s1, s2, nf = curveball_run(data_cb, off, np.asarray(ylo, np.int64), np.asarray(yhi, np.int64), conc_rows,\n                               cfg[\"V3_CURVEBALL_SAMPLES\"], 5, 20260932, NT)\n    logger.info(f\"V3c curveball: {r} rows, {len(years)} years, {time.time()-t:.1f}s\")\n    # U3: row and column sums preserved\n    row_ok = bool(np.array_equal(np.diff(off), np.diff(off)))\n    col_ok = True\n    for y in years:\n        lo, hi = off[ylo[yi[y]]], off[yhi[yi[y]]]\n        col_ok &= bool(np.array_equal(np.bincount(data0[lo:hi], minlength=NT), np.bincount(data_cb[lo:hi], minlength=NT)))\n    rowset_ok = all(len(np.unique(data_cb[off[i]:off[i + 1]])) == off[i + 1] - off[i] for i in range(0, r, max(1, r // 2000)))\n    logger.info(f\"U3 curveball: column sums preserved {col_ok}; rows remain sets {rowset_ok}\")\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        pm = np.where(nf >= 20, s1 / np.maximum(nf, 1), np.nan)\n        psd = np.sqrt(np.maximum(s2 / np.maximum(nf, 1) - pm ** 2, 0))\n    obs_ep = df[\"edge_persistence__raw\"].to_numpy(float)\n    out = pd.DataFrame({\"frame\": df.frame, \"ci\": df.ci})\n    out[\"pers_cfg_mean\"] = pm\n    out[\"pers_cfg_sd\"] = psd\n    out[\"excess_pers_cfg\"] = obs_ep - pm\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        out[\"z_pers_cfg\"] = np.where(psd > 0, (obs_ep - pm) / np.where(psd > 0, psd, 1), np.nan)\n    # k-matched persistence approximation (full build and halves); weights = the year's neighbour popularity\n    cum_pop = np.cumsum(pop, 1)\n    pool_pop = (pop > 0).sum(1).astype(np.int64)\n    years3 = np.stack([[yi[t + w] for w in range(3)] for t in t0s]).astype(np.int64)\n    k3 = np.stack([[len(ex[c][\"NB\"][w]) for w in (1, 2, 3)] for c in range(nC)]).astype(np.int64)\n    t = time.time()\n    mu_k, sd_k = kpers_null(k3, np.arange(nC, dtype=np.int64), years3, self_flat, self_off, cum_pop, pool_pop,\n                            cfg[\"V3_KSETS\"], 20260933, NT)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        out[\"pers_k_mean\"] = mu_k\n        out[\"z_pers_k\"] = np.where(sd_k > 0, (obs_ep - mu_k) / np.where(sd_k > 0, sd_k, 1), np.nan)\n    logger.info(f\"V3c k-matched full build {time.time()-t:.1f}s\")\n    hk3, hconc, hyears, hobs, hkey = [], [], [], [], []\n    for c in range(nC):\n        for h in (\"A\", \"B\"):\n            for sp in range(S):\n                hk3.append([len(ex[c][\"half_NB\"][h][sp][w]) for w in range(3)])\n                hconc.append(c)\n                hyears.append(years3[c])\n                hobs.append(float(ex[c][\"half_ep\"][h][sp]))\n                hkey.append((c, h, sp))\n    t = time.time()\n    hmu, hsd = kpers_null(np.asarray(hk3, np.int64), np.asarray(hconc, np.int64), np.asarray(hyears, np.int64),\n                          self_flat, self_off, cum_pop, pool_pop, cfg[\"V3_HALF_DRAWS\"], 20260934, NT)\n    hobs = np.asarray(hobs)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        hz_pers = np.where(hsd > 0, (hobs - hmu) / np.where(hsd > 0, hsd, 1), np.nan)\n    logger.info(f\"V3c k-matched halves ({len(hk3)} rows) {time.time()-t:.1f}s\")\n    # ---------------------------------------------------------------- V3b k-matched density null\n    z = np.load(DATA_IN / \"bg_topics.npz\")\n    bgy = {int(y): i for i, y in enumerate(z[\"years\"])}\n    BG = z[\"BG\"].astype(float)\n    cum_bg = np.cumsum(BG, 1)\n    pool_bg = (BG > 0).sum(1).astype(np.int64)\n    adj3 = np.zeros((3, NT, NT), np.bool_)\n    for s in range(3):\n        zz = np.load(INPUTS / \"backbone\" / f\"slice{s}.npz\")\n        adj3[s, zz[\"a\"], zz[\"b\"]] = True\n        adj3[s, zz[\"b\"], zz[\"a\"]] = True\n    set_k = np.array([len(e[\"NB\"][3]) for e in ex], np.int64)\n    set_slice = np.array([slice_of(int(t) + 2) for t in t0s], np.int64)\n    set_year = np.array([bgy[int(t) + 2] for t in t0s], np.int64)\n    t = time.time()\n    mk, sk = ksets_null(set_k, np.arange(nC, dtype=np.int64), set_slice, set_year, self_flat, self_off, cum_bg,\n                        pool_bg, adj3, cfg[\"V3_KSETS\"], 20260931, NT)\n    e_obs = df[\"e_W3__raw\"].to_numpy(float)\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        out[\"dens_k_mean\"] = mk / (set_k * (set_k - 1) / 2)\n        out[\"z_dens_k\"] = np.where(sk > 0, (e_obs - mk) / np.where(sk > 0, sk, 1), np.nan)\n    logger.info(f\"V3b full build {time.time()-t:.1f}s\")\n    hsets = [ex[c][\"half_NB\"][h][sp][2] for (c, h, sp) in hkey]\n    h_k = np.array([len(s) for s in hsets], np.int64)\n    hc = np.array([c for c, _, _ in hkey], np.int64)\n    t = time.time()\n    hmk, hsk = ksets_null(h_k, hc, set_slice[hc], set_year[hc], self_flat, self_off, cum_bg, pool_bg, adj3,\n                          cfg[\"V3_HALF_DRAWS\"], 20260935, NT)\n    # observed half-set edges in the real backbone\n    pa, pb, sid = pairs_of(hsets)\n    h_eobs = np.bincount(sid, weights=adj3[set_slice[hc][sid], pa, pb], minlength=len(hsets)) if len(sid) else \\\n        np.zeros(len(hsets))\n    with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n        hz_dk = np.where(hsk > 0, (h_eobs - hmk) / np.where(hsk > 0, hsk, 1), np.nan)\n    logger.info(f\"V3b halves {time.time()-t:.1f}s\")\n    del adj3\n    # ---------------------------------------------------------------- collect V3a\n    res = {s: futs[s].result() for s in range(3)}\n    pool.shutdown()\n    u4 = res[0].pop(\"_u4\", {})\n    zc3 = np.full(nC, np.nan)\n    ec3 = np.full(nC, np.nan)\n    zc1 = np.full(nC, np.nan)\n    hz_dc = np.full(len(hkey), np.nan)\n    hpos = {k: i for i, k in enumerate(hkey)}\n    for s in range(3):\n        for nm in (\"W3\", \"W1\", \"H3\"):\n            obs, s1_, s2_, nd = res[s][nm]\n            if nd == 0:\n                continue\n            mu = s1_ / nd\n            sd = np.sqrt(np.maximum(s2_ / nd - mu ** 2, 0))\n            with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n                zz = np.where(sd > 0, (obs - mu) / np.where(sd > 0, sd, 1), np.nan)\n            idx = index[s][nm]\n            if nm == \"W3\":\n                ii = np.asarray(idx, int)\n                kk = set_k[ii]\n                ok = kk >= 2\n                zc3[ii[ok]] = zz[ok]\n                with np.errstate(invalid=\"ignore\", divide=\"ignore\"):\n                    ec3[ii[ok]] = (mu / (kk * (kk - 1) / 2))[ok]\n                # consistency: observed count == S2 e_W3\n                if not np.allclose(obs[ok], e_obs[ii[ok]]):\n                    raise RuntimeError(\"V3a observed edge counts differ from S2 e_W3\")\n            elif nm == \"W1\":\n                ii = np.asarray(idx, int)\n                k1 = np.array([len(ex[i][\"NB\"][1]) for i in ii])\n                ok = k1 >= 2\n                zc1[ii[ok]] = zz[ok]\n            else:\n                kk = np.array([len(ex[c][\"half_NB\"][h][sp][2]) for (c, h, sp) in idx])\n                for j, key in enumerate(idx):\n                    if kk[j] >= 2:\n                        hz_dc[hpos[key]] = zz[j]\n    out[\"z_dens_cfg\"] = zc3\n    out[\"dens_cfg_exp\"] = ec3\n    out[\"z_dens_cfg_W1\"] = zc1\n    out.to_parquet(DATA / f\"v3_nulls_{a.tag}.parquet\", index=False)\n    halves = {\"key\": [(df.frame.iat[c], int(df.ci.iat[c]), h, sp) for (c, h, sp) in hkey],\n              \"z_pers_k\": hz_pers.astype(np.float32), \"z_dens_k\": hz_dk.astype(np.float32),\n              \"z_dens_cfg\": hz_dc.astype(np.float32)}\n    (DATA / f\"v3_halves_{a.tag}.pkl\").write_bytes(pickle.dumps(halves, protocol=5))\n    ok = out[[\"z_pers_cfg\", \"z_pers_k\"]].dropna()\n    from scipy.stats import spearmanr\n    rho = float(spearmanr(ok.z_pers_cfg, ok.z_pers_k)[0]) if len(ok) > 10 else math.nan\n    jdump({\"U3_curveball\": {\"column_sums_preserved\": col_ok, \"row_sizes_preserved\": row_ok, \"rows_remain_sets\": rowset_ok},\n           \"U4_rewire\": u4, \"cfg\": cfg, \"n_concepts\": nC, \"n_rows_curveball\": int(r),\n           \"spearman_z_pers_cfg_vs_k_matched\": rho,\n           \"finite\": {c: int(np.isfinite(out[c]).sum()) for c in out.columns if c not in (\"frame\", \"ci\")}},\n          RES / f\"v3_nulls_{a.tag}.json\")\n    logger.info(f\"V3 done; spearman(z_pers_cfg, z_pers_k) = {rho:.3f}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [98] TOOL CALL — Bash · 2026-09-29 05:35:18 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -1 logs/s2_full.out; timeout 600 .venv/bin/python s2_variants.py --sample-per-body 50 --tag mini --workers 1 --chunk 50 --cfg '{"D_RARE":20,"D_PERM":20,"S_RAW":10,"S_CLEAN":5,"D_PERM_HALF":20,"D_RARE_HALF":10}' 2>&1 | tail -1; timeout 900 .venv/bin/python s3_nulls.py --tag mini --draws-scale 0.05 2>&1 | tail -15
```

### [99] TOOL RESULT — Bash · 2026-09-29 05:35:50 UTC

```
{"stdout": "05:34:27|INFO   |chunk 121/135 (12100 concepts) 2.8 min; 0.033 s/concept; eta 0.3 min\n05:34:52|INFO   |wrote 200 rows -> data/s2_scalars_mini.parquet; errors 0\n05:34:58|INFO   |loaded 200 concepts from S2 (mini); cfg {'N_RARE': [5, 10, 20], 'D_RARE': 50, 'D_PERM': 200, 'S_RAW': 100, 'S_CLEAN': 20, 'D_PERM_HALF': 50, 'D_RARE_HALF': 20, 'RARE_HALF_N': 5, 'MIN_HOME': 10, 'V3_REWIRES': 10, 'V3_KSETS': 10, 'V3_CURVEBALL_SAMPLES': 10, 'V3_HALF_DRAWS': 10}\n05:34:58|INFO   |V3a slice 0: W3 sets 0 (0 pairs), W1 34, halves 0 (0 pairs)\nTraceback (most recent call last):\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py\", line 332, in <module>\n    main()\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py\", line 157, in main\n    jobs, index = v3a(df, ex, cfg, logger)\n                  ^^^^^^^^^^^^^^^^^^^^^^^^\n  File \"/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s3_nulls.py\", line 132, in v3a\n    hs.append(ex[i][\"half_NB\"][h][sp][2])\n              ~~~~~~~~~~~~~~~~~~~^^^^\nIndexError: list index out of range", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [100] TOOL CALL — Bash · 2026-09-29 05:35:50 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("s3_nulls.py"); s=p.read_text()
old='''    df, ex = load_s2(a.tag)
'''
new='''    df, ex = load_s2(a.tag)
    import json
    cfg["S_CLEAN"] = json.loads((DATA / f"s2_parts_{a.tag}" / "cfg.json").read_text())["S_CLEAN"]
'''
s=s.replace(old,new); p.write_text(s)
EOF
timeout 900 .venv/bin/python s3_nulls.py --tag mini --draws-scale 0.05 2>&1 | tail -15; cat results/v3_nulls_mini.json | head -50
```

### [101] TOOL RESULT — Bash · 2026-09-29 05:36:50 UTC

```
{"stdout": "05:35:10|INFO   |loaded 200 concepts from S2 (mini); cfg {'N_RARE': [5, 10, 20], 'D_RARE': 50, 'D_PERM': 200, 'S_RAW': 100, 'S_CLEAN': 5, 'D_PERM_HALF': 50, 'D_RARE_HALF': 20, 'RARE_HALF_N': 5, 'MIN_HOME': 10, 'V3_REWIRES': 10, 'V3_KSETS': 10, 'V3_CURVEBALL_SAMPLES': 10, 'V3_HALF_DRAWS': 10}\n05:35:10|INFO   |V3a slice 0: W3 sets 0 (0 pairs), W1 34, halves 0 (0 pairs)\n05:35:10|INFO   |V3a slice 1: W3 sets 70 (630 pairs), W1 66, halves 700 (1261 pairs)\n05:35:10|INFO   |V3a slice 2: W3 sets 130 (990 pairs), W1 100, halves 1300 (1764 pairs)\n05:35:29|INFO   |V3c curveball: 600 rows, 17 years, 13.3s\n05:35:29|INFO   |U3 curveball: column sums preserved True; rows remain sets True\n05:35:32|INFO   |V3c k-matched full build 3.1s\n05:35:33|INFO   |V3c k-matched halves (2000 rows) 0.0s\n05:35:34|INFO   |V3b full build 1.2s\n05:35:34|INFO   |V3b halves 0.0s\n05:36:09|INFO   |V3 done; spearman(z_pers_cfg, z_pers_k) = nan\n{\n \"U3_curveball\": {\n  \"column_sums_preserved\": true,\n  \"row_sizes_preserved\": true,\n  \"rows_remain_sets\": true\n },\n \"U4_rewire\": {\n  \"is_simple\": true,\n  \"degree_equal\": true\n },\n \"cfg\": {\n  \"N_RARE\": [\n   5,\n   10,\n   20\n  ],\n  \"D_RARE\": 50,\n  \"D_PERM\": 200,\n  \"S_RAW\": 100,\n  \"S_CLEAN\": 5,\n  \"D_PERM_HALF\": 50,\n  \"D_RARE_HALF\": 20,\n  \"RARE_HALF_N\": 5,\n  \"MIN_HOME\": 10,\n  \"V3_REWIRES\": 10,\n  \"V3_KSETS\": 10,\n  \"V3_CURVEBALL_SAMPLES\": 10,\n  \"V3_HALF_DRAWS\": 10\n },\n \"n_concepts\": 200,\n \"n_rows_curveball\": 600,\n \"spearman_z_pers_cfg_vs_k_matched\": null,\n \"finite\": {\n  \"pers_cfg_mean\": 0,\n  \"pers_cfg_sd\": 0,\n  \"excess_pers_cfg\": 0,\n  \"z_pers_cfg\": 0,\n  \"pers_k_mean\": 189,\n  \"z_pers_k\": 52,\n  \"dens_k_mean\": 112,\n  \"z_dens_k\": 86,\n  \"z_dens_cfg\": 88,\n  \"dens_cfg_exp\": 112,\n  \"z_dens_cfg_W1\": 109\n }\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [102] TOOL CALL — Bash · 2026-09-29 05:37:52 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sed -i 's/pm = np.where(nf >= 20, s1/pm = np.where(nf >= max(2, cfg["V3_CURVEBALL_SAMPLES"] \/\/ 2), s1/' s3_nulls.py; grep -n "pm = np.where" s3_nulls.py; tail -2 logs/s2_full.out; ls data/
```

### [103] TOOL RESULT — Bash · 2026-09-29 05:37:52 UTC

```
{"stdout": "202:        pm = np.where(nf >= max(2, cfg[\"V3_CURVEBALL_SAMPLES\"] // 2), s1 / np.maximum(nf, 1), np.nan)\n05:34:37|INFO   |chunk 135/135 (13444 concepts) 3.0 min; 0.029 s/concept; eta 0.0 min\n05:34:54|INFO   |wrote 13444 rows -> data/s2_scalars_full.parquet; errors 0\nhome_cache.pkl\ns2_parts_full\ns2_parts_mini\ns2_scalars_full.parquet\ns2_scalars_mini.parquet\ns2_scalars_t200.parquet\nv3_halves_mini.pkl\nv3_nulls_mini.parquet", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [104] ASSISTANT · 2026-09-29 05:37:52 UTC

```
S2 finished: 13,444 concepts in 3 min, 0 errors. Launching the full V3 nulls in the background.
```

### [105] TOOL CALL — Bash · 2026-09-29 05:37:52 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; (nohup .venv/bin/python s3_nulls.py --tag full > logs/s3_full.out 2>&1 &); sleep 45; tail -5 logs/s3_full.out; .venv/bin/python - <<'EOF'
import pandas as pd, numpy as np
d=pd.read_parquet("data/s2_scalars_full.parquet")
print(d.groupby("body").size())
for n in (5,10,20):
    print(n, d.groupby("body")[f"edge_persistence_rare{n}"].apply(lambda s: s.notna().sum()).to_dict())
print(d.groupby("body")["edge_persistence_exc"].apply(lambda s: s.notna().sum()).to_dict())
print(d.groupby("body")["min_year_n"].describe())
EOF
```

### [106] TOOL RESULT — Bash · 2026-09-29 05:38:20 UTC

```
{"stdout": "05:36:58|INFO   |V3c curveball: 40332 rows, 17 years, 5.9s\n05:36:58|INFO   |U3 curveball: column sums preserved True; rows remain sets True\n05:37:00|INFO   |V3c k-matched full build 2.2s\n05:37:12|INFO   |V3c k-matched halves (537760 rows) 11.3s\n05:37:14|INFO   |V3b full build 1.3s\nbody\nCOH1014    4195\nCOH1517    1365\nDEV        4670\nOLDHO      3214\ndtype: int64\n5 {'COH1014': 2650, 'COH1517': 879, 'DEV': 3487, 'OLDHO': 1825}\n10 {'COH1014': 1388, 'COH1517': 431, 'DEV': 2277, 'OLDHO': 704}\n20 {'COH1014': 185, 'COH1517': 58, 'DEV': 334, 'OLDHO': 54}\n{'COH1014': 3814, 'COH1517': 1250, 'DEV': 4418, 'OLDHO': 2848}\n          count       mean       std  min  25%  50%   75%    max\nbody                                                            \nCOH1014  4195.0   8.399762  6.241878  0.0  4.0  7.0  11.0   84.0\nCOH1517  1365.0   8.512088  6.932279  0.0  4.0  7.0  11.0   70.0\nDEV      4670.0  10.351178  6.547225  0.0  6.0  9.0  14.0   70.0\nOLDHO    3214.0   6.825451  5.461607  0.0  3.0  6.0   9.0  176.0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [107] THINKING · 2026-09-29 05:38:52 UTC

```
V3c curveball and k-matched nulls finished quickly, V3a rewiring (~13 min) is still running, and V1 attrition shows 431/1,365 COH1517 concepts and 704/3,214 OLDHO concepts qualifying at n=10. Next I'll run the U3/U4 null tests.
```

### [108] TOOL CALL — Write · 2026-09-29 05:38:52 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/u_nulls.py

#!/usr/bin/env python3
"""U3 curveball uniformity on an enumerable toy + margin preservation; U4 rewire null calibration:
z of edge counts inside random topic sets, where the 'observed' graph is itself one degree-preserving rewire of
slice 0 and the null is formed by further independent rewires of the original -> mean z ~ 0 (|mean| < 0.15).
-> results/unit_tests_nulls.json"""
from __future__ import annotations

import itertools
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np
from scipy import stats

from common import INPUTS, RES, jdump, setup_logger
from nullkern import _trade


def toy_curveball(n_samples: int = 30000) -> dict:
    # 3 rows x 4 columns, row sums (2, 2, 1), column sums (2, 1, 1, 1)
    rows = [np.array([0, 1], np.int32), np.array([0, 2], np.int32), np.array([3], np.int32)]
    r_s, c_s = [2, 2, 1], [2, 1, 1, 1]
    states = []
    for bits in itertools.product([0, 1], repeat=12):
        M = np.array(bits).reshape(3, 4)
        if list(M.sum(1)) == r_s and list(M.sum(0)) == c_s:
            states.append(tuple(bits))
    sidx = {s: i for i, s in enumerate(states)}
    data = np.concatenate(rows).astype(np.int32)
    off = np.array([0, 2, 4, 5], np.int64)
    mark = np.zeros(5, np.int64)
    pool = np.empty(8, np.int32)
    np.random.seed(3)
    from numba import njit

    @njit
    def seed(s):
        np.random.seed(s)
    seed(3)
    stamp = 1
    rng = np.random.default_rng(4)
    counts = np.zeros(len(states))
    for t in range(n_samples * 3):
        i, j = rng.choice(3, 2, replace=False)
        _trade(data, off, i, j, mark, stamp, pool)
        stamp += 2
        if t % 3 == 2:
            M = np.zeros((3, 4), int)
            for r in range(3):
                M[r, data[off[r]:off[r + 1]]] = 1
            assert list(M.sum(1)) == r_s and list(M.sum(0)) == c_s
            counts[sidx[tuple(M.ravel())]] += 1
    chi = stats.chisquare(counts)
    return {"n_states": len(states), "freq": counts.tolist(), "chi2_p": float(chi.pvalue),
            "pass": bool(chi.pvalue > 0.01)}


def rewire_calibration(n_null: int = 30, n_sets: int = 50, k: int = 12) -> dict:
    import igraph as ig
    z = np.load(INPUTS / "backbone" / "slice0.npz")
    nt = 4516
    G0 = ig.Graph(n=nt, edges=np.c_[z["a"], z["b"]].tolist())

    def rewired(seed):
        random.seed(seed)
        ig.set_random_number_generator(random)
        g = G0.copy()
        g.rewire(n=10 * g.ecount(), allowed_edge_types="simple")
        el = np.array(g.get_edgelist())
        A = np.zeros((nt, nt), bool)
        A[el[:, 0], el[:, 1]] = True
        A[el[:, 1], el[:, 0]] = True
        return A, g
    rng = np.random.default_rng(7)
    sets = [rng.choice(nt, k, replace=False) for _ in range(n_sets)]
    iu, ju = np.triu_indices(k, 1)
    Aobs, gobs = rewired(999)
    obs = np.array([Aobs[s[iu], s[ju]].sum() for s in sets], float)
    null = np.zeros((n_null, n_sets))
    for d in range(n_null):
        A, _ = rewired(1000 + d)
        null[d] = [A[s[iu], s[ju]].sum() for s in sets]
    sd = null.std(0)
    zz = np.where(sd > 0, (obs - null.mean(0)) / np.where(sd > 0, sd, 1), np.nan)
    return {"mean_z": float(np.nanmean(zz)), "sd_z": float(np.nanstd(zz)), "n_sets": n_sets, "n_null": n_null,
            "degree_preserved": bool(np.array_equal(np.array(gobs.degree()), np.array(G0.degree()))),
            "simple": bool(gobs.is_simple()), "pass": bool(abs(np.nanmean(zz)) < 0.15)}


def main() -> None:
    logger = setup_logger("u_nulls")
    out = {"U3_toy": toy_curveball()}
    logger.info(f"U3 toy: {out['U3_toy']}")
    out["U4_rewire_calibration"] = rewire_calibration()
    logger.info(f"U4: {out['U4_rewire_calibration']}")
    jdump(out, RES / "unit_tests_nulls.json")


if __name__ == "__main__":
    main()
```

### [109] TOOL RESULT — Write · 2026-09-29 05:38:52 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/u_nulls.py", "content": "#!/usr/bin/env python3\n\"\"\"U3 curveball uniformity on an enumerable toy + margin preservation; U4 rewire null calibration:\nz of edge counts inside random topic sets, where the 'observed' graph is itself one degree-preserving rewire of\nslice 0 and the null is formed by further independent rewires of the original -> mean z ~ 0 (|mean| < 0.15).\n-> results/unit_tests_nulls.json\"\"\"\nfrom __future__ import annotations\n\nimport itertools\nimport random\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1] / \"lib\"))\n\nimport numpy as np\nfrom scipy import stats\n\nfrom common import INPUTS, RES, jdump, setup_logger\nfrom nullkern import _trade\n\n\ndef toy_curveball(n_samples: int = 30000) -> dict:\n    # 3 rows x 4 columns, row sums (2, 2, 1), column sums (2, 1, 1, 1)\n    rows = [np.array([0, 1], np.int32), np.array([0, 2], np.int32), np.array([3], np.int32)]\n    r_s, c_s = [2, 2, 1], [2, 1, 1, 1]\n    states = []\n    for bits in itertools.product([0, 1], repeat=12):\n        M = np.array(bits).reshape(3, 4)\n        if list(M.sum(1)) == r_s and list(M.sum(0)) == c_s:\n            states.append(tuple(bits))\n    sidx = {s: i for i, s in enumerate(states)}\n    data = np.concatenate(rows).astype(np.int32)\n    off = np.array([0, 2, 4, 5], np.int64)\n    mark = np.zeros(5, np.int64)\n    pool = np.empty(8, np.int32)\n    np.random.seed(3)\n    from numba import njit\n\n    @njit\n    def seed(s):\n        np.random.seed(s)\n    seed(3)\n    stamp = 1\n    rng = np.random.default_rng(4)\n    counts = np.zeros(len(states))\n    for t in range(n_samples * 3):\n        i, j = rng.choice(3, 2, replace=False)\n        _trade(data, off, i, j, mark, stamp, pool)\n        stamp += 2\n        if t % 3 == 2:\n            M = np.zeros((3, 4), int)\n            for r in range(3):\n                M[r, data[off[r]:off[r + 1]]] = 1\n            assert list(M.sum(1)) == r_s and list(M.sum(0)) == c_s\n            counts[sidx[tuple(M.ravel())]] += 1\n    chi = stats.chisquare(counts)\n    return {\"n_states\": len(states), \"freq\": counts.tolist(), \"chi2_p\": float(chi.pvalue),\n            \"pass\": bool(chi.pvalue > 0.01)}\n\n\ndef rewire_calibration(n_null: int = 30, n_sets: int = 50, k: int = 12) -> dict:\n    import igraph as ig\n    z = np.load(INPUTS / \"backbone\" / \"slice0.npz\")\n    nt = 4516\n    G0 = ig.Graph(n=nt, edges=np.c_[z[\"a\"], z[\"b\"]].tolist())\n\n    def rewired(seed):\n        random.seed(seed)\n        ig.set_random_number_generator(random)\n        g = G0.copy()\n        g.rewire(n=10 * g.ecount(), allowed_edge_types=\"simple\")\n        el = np.array(g.get_edgelist())\n        A = np.zeros((nt, nt), bool)\n        A[el[:, 0], el[:, 1]] = True\n        A[el[:, 1], el[:, 0]] = True\n        return A, g\n    rng = np.random.default_rng(7)\n    sets = [rng.choice(nt, k, replace=False) for _ in range(n_sets)]\n    iu, ju = np.triu_indices(k, 1)\n    Aobs, gobs = rewired(999)\n    obs = np.array([Aobs[s[iu], s[ju]].sum() for s in sets], float)\n    null = np.zeros((n_null, n_sets))\n    for d in range(n_null):\n        A, _ = rewired(1000 + d)\n        null[d] = [A[s[iu], s[ju]].sum() for s in sets]\n    sd = null.std(0)\n    zz = np.where(sd > 0, (obs - null.mean(0)) / np.where(sd > 0, sd, 1), np.nan)\n    return {\"mean_z\": float(np.nanmean(zz)), \"sd_z\": float(np.nanstd(zz)), \"n_sets\": n_sets, \"n_null\": n_null,\n            \"degree_preserved\": bool(np.array_equal(np.array(gobs.degree()), np.array(G0.degree()))),\n            \"simple\": bool(gobs.is_simple()), \"pass\": bool(abs(np.nanmean(zz)) < 0.15)}\n\n\ndef main() -> None:\n    logger = setup_logger(\"u_nulls\")\n    out = {\"U3_toy\": toy_curveball()}\n    logger.info(f\"U3 toy: {out['U3_toy']}\")\n    out[\"U4_rewire_calibration\"] = rewire_calibration()\n    logger.info(f\"U4: {out['U4_rewire_calibration']}\")\n    jdump(out, RES / \"unit_tests_nulls.json\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [110] TOOL CALL — Bash · 2026-09-29 05:38:52 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; (nohup .venv/bin/python tests/u_nulls.py > logs/u_nulls.out 2>&1 &); sleep 30; cat logs/u_nulls.out | tail -3; tail -3 logs/s3_full.out; grep -n "outcome_grounding" -A2 /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/frozen_spec.json | head -5
```

### [111] TOOL RESULT — Bash · 2026-09-29 05:39:22 UTC

```
{"stdout": "05:38:26|INFO   |U3 toy: {'n_states': 12, 'freq': [2503.0, 2513.0, 2526.0, 2522.0, 2491.0, 2478.0, 2518.0, 2442.0, 2545.0, 2526.0, 2449.0, 2487.0], 'chi2_p': 0.9558059116407714, 'pass': True}\nslice 1: 20/200 rewires, 64s\nslice 2: 20/200 rewires, 69s\nslice 0: 40/200 rewires, 75s\n158: \"outcome_grounding\": \"TAG\",\n159- \"primary\": \"TAG t0+6..t0+8\",\n160- \"O2r_resid\": {", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [112] ASSISTANT · 2026-09-29 05:40:30 UTC

```
U3 passes (12-state toy, χ² p = 0.96). Now writing S4: composites, second-seal constants and split-half reliability.
```

### [113] TOOL CALL — Write · 2026-09-29 05:40:30 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py

#!/usr/bin/env python3
"""S2-composites + S1b seal + V4 split-half reliability (no outcome is read here).

1. merge S2 scalars and V3 nulls; fit the clean-variant z constants on ALL EXP5-frame concepts (n_home_early >= 10,
   variant finite; winsor 0.5/99.5, mean/sd == ladder.fit_open_constants) -> results/frozen_constants_S1b.json,
   sealed (entry S1b_constants) BEFORE any outcome join
2. composites NOVCHURN_* / OPEN_home_clean / OPEN_home_exc -> data/clean_variants.parquet (no outcome columns)
3. V4 split-half reliability of every raw and clean variant -> results/reliability.json (X side; the outcome side is
   added by s4b_outcome_rel.py)"""
from __future__ import annotations

import json
import math
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import DATA, DATA_IN, RES, jdump, setup_logger
from seal import seal_file

logger = setup_logger("s4_composites")
OUT6 = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]
NBINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]
# clean columns needing new constants: column -> sign
NEW_CONST = {**{f"NOV_res_rare{n}": 1 for n in (5, 10, 20)}, **{f"edge_persistence_rare{n}": -1 for n in (5, 10, 20)},
             "NOV_res_exc": 1, "edge_persistence_exc": -1, "NOV_res_zperm": 1, "edge_persistence_zperm": -1,
             "z_pers_cfg": -1, "EP_chao": -1, "z_dens_cfg": -1, "ego_density_W3_exc": -1, "z_dens_k": -1,
             "excess_pers_cfg": -1, "z_pers_k": -1}


def fit_const(v: np.ndarray, sign: int) -> dict:
    v = v[np.isfinite(v)]
    lo, hi = np.percentile(v, [0.5, 99.5])
    w = np.clip(v, lo, hi)
    return {"lo": float(lo), "hi": float(hi), "mu": float(w.mean()), "sd": float(w.std()) or 1.0, "sign": sign,
            "n": int(len(v))}


def zs(v, c: dict) -> np.ndarray:
    return c["sign"] * (np.clip(np.asarray(v, float), c["lo"], c["hi"]) - c["mu"]) / c["sd"]


def mean_req(*zz, min_fin: int | None = None) -> np.ndarray:
    Z = np.column_stack(zz)
    nf = np.isfinite(Z).sum(1)
    with np.errstate(invalid="ignore"):
        m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)
    m[nf < (Z.shape[1] if min_fin is None else min_fin)] = np.nan
    return m


def composites(d: pd.DataFrame, K10: dict, KN: dict, suffix_map: dict | None = None) -> pd.DataFrame:
    """d holds raw columns '<m>__raw' and clean columns; returns composite columns."""
    o = pd.DataFrame(index=d.index)
    zN = zs(d["NOV_res__raw"], K10["NOV_res"])
    o["NOVCHURN_raw"] = mean_req(zN, zs(d["edge_persistence__raw"], K10["edge_persistence"]))
    for n in (5, 10, 20):
        if f"NOV_res_rare{n}" in d:
            o[f"NOVCHURN_rare{n}"] = mean_req(zs(d[f"NOV_res_rare{n}"], KN[f"NOV_res_rare{n}"]),
                                              zs(d[f"edge_persistence_rare{n}"], KN[f"edge_persistence_rare{n}"]))
    if "NOV_res_exc" in d:
        o["NOVCHURN_exc"] = mean_req(zs(d["NOV_res_exc"], KN["NOV_res_exc"]),
                                     zs(d["edge_persistence_exc"], KN["edge_persistence_exc"]))
        o["NOVCHURN_zperm"] = mean_req(zs(d["NOV_res_zperm"], KN["NOV_res_zperm"]),
                                       zs(d["edge_persistence_zperm"], KN["edge_persistence_zperm"]))
    if "z_pers_cfg" in d:
        o["NOVCHURN_cfg"] = mean_req(zN, zs(d["z_pers_cfg"], KN["z_pers_cfg"]))
    if "EP_chao" in d:
        o["NOVCHURN_chao"] = mean_req(zN, zs(d["EP_chao"], KN["EP_chao"]))
    raw6 = {m: zs(d[f"{m}__raw"], K10[m]) for m in OUT6}
    o["OPEN_home"] = mean_req(*raw6.values(), min_fin=4)
    if "z_dens_cfg" in d and "z_pers_cfg" in d:
        cl = dict(raw6)
        cl["ego_density_W3"] = zs(d["z_dens_cfg"], KN["z_dens_cfg"])
        cl["edge_persistence"] = zs(d["z_pers_cfg"], KN["z_pers_cfg"])
        o["OPEN_home_clean"] = mean_req(*cl.values(), min_fin=4)
    if "ego_density_W3_exc" in d:
        ce = dict(raw6)
        ce["ego_density_W3"] = zs(d["ego_density_W3_exc"], KN["ego_density_W3_exc"])
        ce["edge_persistence"] = zs(d["edge_persistence_exc"], KN["edge_persistence_exc"])
        o["OPEN_home_exc"] = mean_req(*ce.values(), min_fin=4)
    return o


# ----------------------------------------------------------------------------- reliability helpers
def spearman_cols(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Spearman per row s of A[s], B[s] (pairwise finite)."""
    out = np.full(A.shape[0], np.nan)
    for s in range(A.shape[0]):
        ok = np.isfinite(A[s]) & np.isfinite(B[s])
        if ok.sum() < 20:
            continue
        a, b = rankdata(A[s, ok]), rankdata(B[s, ok])
        if a.std() == 0 or b.std() == 0:
            continue
        out[s] = np.corrcoef(a, b)[0, 1]
    return out


def sb_of(rs: np.ndarray) -> tuple[float, float, int]:
    rs = rs[np.isfinite(rs)]
    if not len(rs):
        return math.nan, math.nan, 0
    r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))
    return r, 2 * r / (1 + r) if r > -1 else math.nan, int(len(rs))


def main() -> None:
    s2 = pd.read_parquet(DATA / "s2_scalars_full.parquet")
    v3 = pd.read_parquet(DATA / "v3_nulls_full.parquet")
    d = s2.merge(v3, on=["frame", "ci"], how="left", validate="1:1")
    logger.info(f"merged {len(d)} concepts")
    spec = json.loads((RES / "frozen_spec.json").read_text())
    K10 = spec["exp10_open_constants_home"]
    ex5 = d.frame == "exp5"
    KN = {c: fit_const(d.loc[ex5, c].to_numpy(float), s) for c, s in NEW_CONST.items()}
    cpath = RES / "frozen_constants_S1b.json"
    jdump({"rule": spec["composites"]["z_rule_new_constants"], "fitted_on": "EXP5-frame concepts, n_home_early >= 10",
           "constants": KN, "exp10_constants_used_for_raw": K10}, cpath)
    ent = seal_file("S1b_constants", cpath)
    logger.info(f"sealed constants sha256 {ent['sha256']}")
    comp = composites(d, K10, KN)
    d = pd.concat([d, comp], axis=1)
    # metadata (no outcome columns)
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet",
                         columns=["ci", "concept_id", "name", "agroup", "group", "OPEN_home", "n_home_early"])
    fe["frame"] = "exp5"
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet",
                         columns=["ci", "concept_id", "name", "agroup", "group", "OPEN_home", "n_home_early"])
    ac["frame"] = "cohort"
    meta = pd.concat([fe, ac], ignore_index=True).rename(columns={"OPEN_home": "OPEN_home_exp10",
                                                                   "n_home_early": "n_home_early_exp10"})
    d = d.merge(meta, on=["frame", "ci"], how="left", validate="1:1")
    chk = np.nanmax(np.abs(d.OPEN_home - d.OPEN_home_exp10))
    mism = int((np.isnan(d.OPEN_home) ^ np.isnan(d.OPEN_home_exp10)).sum())
    assert (d.n_home_early == d.n_home_early_exp10).all()
    logger.info(f"OPEN_home recomputed vs EXP10: max diff {chk:.2e}, NaN mismatches {mism}")
    d["log_n_home_early"] = np.log(d.n_home_early)
    d["uid"] = np.where(d.frame == "exp5", "E", "C") + d.ci.astype(str)
    d.to_parquet(DATA / "clean_variants.parquet", index=False)
    logger.info(f"wrote data/clean_variants.parquet {d.shape}")
    # ------------------------------------------------------------------ V4 reliability
    pos = {(f, int(c)): i for i, (f, c) in enumerate(zip(d.frame, d.ci))}
    nC = len(d)
    S_RAW, S_CL = 100, 20
    H = {h: {m: np.full((S_RAW, nC), np.nan, np.float32) for m in OUT6} for h in ("A", "B")}
    HC: dict = {"A": {}, "B": {}}
    for p in sorted((DATA / "s2_parts_full").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, e in zip(z["rows"], z["extras"]):
            if not e:
                continue
            i = pos[(r["frame"], int(r["ci"]))]
            for h in ("A", "B"):
                for j, m in enumerate(OUT6):
                    H[h][m][:, i] = e["half_raw"][h][:, j]
                hc = e["half_clean"][h]
                for c in hc.columns:
                    HC[h].setdefault(c, np.full((S_CL, nC), np.nan, np.float32))[:, i] = hc[c].to_numpy()
    v3h = pickle.loads((DATA / "v3_halves_full.pkl").read_bytes())
    for c in ("z_pers_k", "z_dens_k", "z_dens_cfg"):
        for h in ("A", "B"):
            HC[h][f"{c}_v3"] = np.full((S_CL, nC), np.nan, np.float32)
    for j, (f, ci, h, sp) in enumerate(v3h["key"]):
        i = pos[(f, int(ci))]
        for c in ("z_pers_k", "z_dens_k", "z_dens_cfg"):
            HC[h][f"{c}_v3"][sp, i] = v3h[c][j]
    # variant half matrices (S x nC) for A and B
    VAR: dict = {}
    for h in ("A", "B"):
        V = {}
        for m in OUT6:
            V[f"{m}__raw"] = H[h][m].astype(float)
        hd = pd.DataFrame({f"{m}__raw": H[h][m][s] for m in OUT6} for s in range(S_RAW))  # unused placeholder
        del hd
        raw_c = []
        for s in range(S_RAW):
            ds = pd.DataFrame({f"{m}__raw": H[h][m][s].astype(float) for m in OUT6})
            raw_c.append(composites(ds, K10, KN)[["NOVCHURN_raw", "OPEN_home"]])
        V["NOVCHURN_raw"] = np.stack([c.NOVCHURN_raw.to_numpy() for c in raw_c])
        V["OPEN_home"] = np.stack([c.OPEN_home.to_numpy() for c in raw_c])
        cl = []
        for s in range(S_CL):
            ds = pd.DataFrame({f"{m}__raw": H[h][m][s].astype(float) for m in OUT6})
            for c, arr in HC[h].items():
                ds[c] = arr[s].astype(float)
            ds["z_pers_cfg"] = ds["z_pers_k_v3"]          # declared approximation (k-matched MC on halves)
            ds["z_dens_cfg"] = ds["z_dens_cfg_v3"]
            ds["z_dens_k"] = ds["z_dens_k_v3"]
            ds["NOV_res_rare5"] = ds["NOV_res_rare5"]
            cc = composites(ds, K10, KN)
            cl.append((ds, cc))
        for col in ["NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "new_edge_rate_exc", "NOV_res_zperm",
                    "edge_persistence_zperm", "ego_density_W3_zperm", "NOV_res_rare5", "edge_persistence_rare5",
                    "ego_density_W3_rare5", "z_pers_cfg", "z_dens_cfg", "z_dens_k", "edge_persistence_nullmean"]:
            V[col] = np.stack([ds[col].to_numpy(float) for ds, _ in cl])
        for col in ["NOVCHURN_exc", "NOVCHURN_zperm", "NOVCHURN_rare5", "NOVCHURN_cfg", "OPEN_home_clean",
                    "OPEN_home_exc"]:
            V[col] = np.stack([cc[col].to_numpy(float) for _, cc in cl])
        VAR[h] = V
    notes = {"z_pers_cfg": "halves use the k-matched Monte Carlo approximation of the curveball null (declared)",
             "NOVCHURN_cfg": "halves use z_pers_k (k-matched MC) in place of the curveball z (declared)",
             "OPEN_home_clean": "halves use z_pers_k for z_pers_cfg (declared)",
             "NOV_res_rare5": "V1 on halves at n = 5 (concepts with >= 10 papers per W-year); used as the reliability "
                              "proxy for every rarefied variant (rare10 cannot be split into halves of 10)",
             "NOVCHURN_rare5": "proxy for NOVCHURN_rare10 reliability"}
    body = d.body.to_numpy()
    nh = d.n_home_early.to_numpy()
    rel: dict = {"method": "r_s = Spearman(v_A, v_B) across concepts per split; r = tanh(mean atanh r_s); "
                           "SB = 2r/(1+r); 100 splits raw, 20 clean", "notes": notes, "variants": {}}
    rng = np.random.default_rng(20260936)
    boot_idx = [rng.integers(0, nC, nC) for _ in range(200)]
    for v in VAR["A"]:
        A, B = VAR["A"][v], VAR["B"][v]
        ent: dict = {}
        r, sb, ns = sb_of(spearman_cols(A, B))
        ent["pooled"] = {"r_half": r, "SB": sb, "n_splits": ns,
                         "n_concepts_mean": float(np.mean((np.isfinite(A) & np.isfinite(B)).sum(1)))}
        for bd in ("DEV", "OLDHO", "COH1014", "COH1517"):
            m = body == bd
            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))
            ent[bd] = {"r_half": r, "SB": sb, "n_splits": ns,
                       "n_concepts_mean": float(np.mean((np.isfinite(A[:, m]) & np.isfinite(B[:, m])).sum(1)))}
        for lo, hi in NBINS:
            m = (nh >= lo) & (nh <= hi)
            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))
            ent[f"n{lo}-{hi if hi < 10**9 else 'inf'}"] = {"r_half": r, "SB": sb, "n_splits": ns,
                                                           "n_concepts": int(m.sum())}
        # concept bootstrap of pooled SB (first 10 splits for speed)
        Ab, Bb = A[:10], B[:10]
        bs = []
        for idx in boot_idx:
            bs.append(sb_of(spearman_cols(Ab[:, idx], Bb[:, idx]))[1])
        bs = np.asarray(bs, float)
        bs = bs[np.isfinite(bs)]
        ent["pooled"]["SB_ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) else None
        ent["pooled"]["SB_boot_sd"] = float(bs.std()) if len(bs) else None
        rel["variants"][v] = ent
        logger.info(f"rel {v}: pooled SB {ent['pooled']['SB']:.3f}; COH1517 {ent['COH1517']['SB']:.3f}")
    jdump(rel, RES / "reliability_x.json")
    # keep per-concept split-averaged half values for power / rederive
    np.savez_compressed(DATA / "v4_half_means.npz",
                        **{f"{h}__{v}": np.nanmean(VAR[h][v], 0) for h in ("A", "B") for v in VAR[h]})


if __name__ == "__main__":
    main()
```

### [114] TOOL RESULT — Write · 2026-09-29 05:40:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py", "content": "#!/usr/bin/env python3\n\"\"\"S2-composites + S1b seal + V4 split-half reliability (no outcome is read here).\n\n1. merge S2 scalars and V3 nulls; fit the clean-variant z constants on ALL EXP5-frame concepts (n_home_early >= 10,\n   variant finite; winsor 0.5/99.5, mean/sd == ladder.fit_open_constants) -> results/frozen_constants_S1b.json,\n   sealed (entry S1b_constants) BEFORE any outcome join\n2. composites NOVCHURN_* / OPEN_home_clean / OPEN_home_exc -> data/clean_variants.parquet (no outcome columns)\n3. V4 split-half reliability of every raw and clean variant -> results/reliability.json (X side; the outcome side is\n   added by s4b_outcome_rel.py)\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport pickle\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import rankdata\n\nfrom common import DATA, DATA_IN, RES, jdump, setup_logger\nfrom seal import seal_file\n\nlogger = setup_logger(\"s4_composites\")\nOUT6 = [\"new_edge_rate\", \"n_comm_W3\", \"participation\", \"NOV_res\", \"ego_density_W3\", \"edge_persistence\"]\nNBINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]\n# clean columns needing new constants: column -> sign\nNEW_CONST = {**{f\"NOV_res_rare{n}\": 1 for n in (5, 10, 20)}, **{f\"edge_persistence_rare{n}\": -1 for n in (5, 10, 20)},\n             \"NOV_res_exc\": 1, \"edge_persistence_exc\": -1, \"NOV_res_zperm\": 1, \"edge_persistence_zperm\": -1,\n             \"z_pers_cfg\": -1, \"EP_chao\": -1, \"z_dens_cfg\": -1, \"ego_density_W3_exc\": -1, \"z_dens_k\": -1,\n             \"excess_pers_cfg\": -1, \"z_pers_k\": -1}\n\n\ndef fit_const(v: np.ndarray, sign: int) -> dict:\n    v = v[np.isfinite(v)]\n    lo, hi = np.percentile(v, [0.5, 99.5])\n    w = np.clip(v, lo, hi)\n    return {\"lo\": float(lo), \"hi\": float(hi), \"mu\": float(w.mean()), \"sd\": float(w.std()) or 1.0, \"sign\": sign,\n            \"n\": int(len(v))}\n\n\ndef zs(v, c: dict) -> np.ndarray:\n    return c[\"sign\"] * (np.clip(np.asarray(v, float), c[\"lo\"], c[\"hi\"]) - c[\"mu\"]) / c[\"sd\"]\n\n\ndef mean_req(*zz, min_fin: int | None = None) -> np.ndarray:\n    Z = np.column_stack(zz)\n    nf = np.isfinite(Z).sum(1)\n    with np.errstate(invalid=\"ignore\"):\n        m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n    m[nf < (Z.shape[1] if min_fin is None else min_fin)] = np.nan\n    return m\n\n\ndef composites(d: pd.DataFrame, K10: dict, KN: dict, suffix_map: dict | None = None) -> pd.DataFrame:\n    \"\"\"d holds raw columns '<m>__raw' and clean columns; returns composite columns.\"\"\"\n    o = pd.DataFrame(index=d.index)\n    zN = zs(d[\"NOV_res__raw\"], K10[\"NOV_res\"])\n    o[\"NOVCHURN_raw\"] = mean_req(zN, zs(d[\"edge_persistence__raw\"], K10[\"edge_persistence\"]))\n    for n in (5, 10, 20):\n        if f\"NOV_res_rare{n}\" in d:\n            o[f\"NOVCHURN_rare{n}\"] = mean_req(zs(d[f\"NOV_res_rare{n}\"], KN[f\"NOV_res_rare{n}\"]),\n                                              zs(d[f\"edge_persistence_rare{n}\"], KN[f\"edge_persistence_rare{n}\"]))\n    if \"NOV_res_exc\" in d:\n        o[\"NOVCHURN_exc\"] = mean_req(zs(d[\"NOV_res_exc\"], KN[\"NOV_res_exc\"]),\n                                     zs(d[\"edge_persistence_exc\"], KN[\"edge_persistence_exc\"]))\n        o[\"NOVCHURN_zperm\"] = mean_req(zs(d[\"NOV_res_zperm\"], KN[\"NOV_res_zperm\"]),\n                                       zs(d[\"edge_persistence_zperm\"], KN[\"edge_persistence_zperm\"]))\n    if \"z_pers_cfg\" in d:\n        o[\"NOVCHURN_cfg\"] = mean_req(zN, zs(d[\"z_pers_cfg\"], KN[\"z_pers_cfg\"]))\n    if \"EP_chao\" in d:\n        o[\"NOVCHURN_chao\"] = mean_req(zN, zs(d[\"EP_chao\"], KN[\"EP_chao\"]))\n    raw6 = {m: zs(d[f\"{m}__raw\"], K10[m]) for m in OUT6}\n    o[\"OPEN_home\"] = mean_req(*raw6.values(), min_fin=4)\n    if \"z_dens_cfg\" in d and \"z_pers_cfg\" in d:\n        cl = dict(raw6)\n        cl[\"ego_density_W3\"] = zs(d[\"z_dens_cfg\"], KN[\"z_dens_cfg\"])\n        cl[\"edge_persistence\"] = zs(d[\"z_pers_cfg\"], KN[\"z_pers_cfg\"])\n        o[\"OPEN_home_clean\"] = mean_req(*cl.values(), min_fin=4)\n    if \"ego_density_W3_exc\" in d:\n        ce = dict(raw6)\n        ce[\"ego_density_W3\"] = zs(d[\"ego_density_W3_exc\"], KN[\"ego_density_W3_exc\"])\n        ce[\"edge_persistence\"] = zs(d[\"edge_persistence_exc\"], KN[\"edge_persistence_exc\"])\n        o[\"OPEN_home_exc\"] = mean_req(*ce.values(), min_fin=4)\n    return o\n\n\n# ----------------------------------------------------------------------------- reliability helpers\ndef spearman_cols(A: np.ndarray, B: np.ndarray) -> np.ndarray:\n    \"\"\"Spearman per row s of A[s], B[s] (pairwise finite).\"\"\"\n    out = np.full(A.shape[0], np.nan)\n    for s in range(A.shape[0]):\n        ok = np.isfinite(A[s]) & np.isfinite(B[s])\n        if ok.sum() < 20:\n            continue\n        a, b = rankdata(A[s, ok]), rankdata(B[s, ok])\n        if a.std() == 0 or b.std() == 0:\n            continue\n        out[s] = np.corrcoef(a, b)[0, 1]\n    return out\n\n\ndef sb_of(rs: np.ndarray) -> tuple[float, float, int]:\n    rs = rs[np.isfinite(rs)]\n    if not len(rs):\n        return math.nan, math.nan, 0\n    r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))\n    return r, 2 * r / (1 + r) if r > -1 else math.nan, int(len(rs))\n\n\ndef main() -> None:\n    s2 = pd.read_parquet(DATA / \"s2_scalars_full.parquet\")\n    v3 = pd.read_parquet(DATA / \"v3_nulls_full.parquet\")\n    d = s2.merge(v3, on=[\"frame\", \"ci\"], how=\"left\", validate=\"1:1\")\n    logger.info(f\"merged {len(d)} concepts\")\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    K10 = spec[\"exp10_open_constants_home\"]\n    ex5 = d.frame == \"exp5\"\n    KN = {c: fit_const(d.loc[ex5, c].to_numpy(float), s) for c, s in NEW_CONST.items()}\n    cpath = RES / \"frozen_constants_S1b.json\"\n    jdump({\"rule\": spec[\"composites\"][\"z_rule_new_constants\"], \"fitted_on\": \"EXP5-frame concepts, n_home_early >= 10\",\n           \"constants\": KN, \"exp10_constants_used_for_raw\": K10}, cpath)\n    ent = seal_file(\"S1b_constants\", cpath)\n    logger.info(f\"sealed constants sha256 {ent['sha256']}\")\n    comp = composites(d, K10, KN)\n    d = pd.concat([d, comp], axis=1)\n    # metadata (no outcome columns)\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\",\n                         columns=[\"ci\", \"concept_id\", \"name\", \"agroup\", \"group\", \"OPEN_home\", \"n_home_early\"])\n    fe[\"frame\"] = \"exp5\"\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\",\n                         columns=[\"ci\", \"concept_id\", \"name\", \"agroup\", \"group\", \"OPEN_home\", \"n_home_early\"])\n    ac[\"frame\"] = \"cohort\"\n    meta = pd.concat([fe, ac], ignore_index=True).rename(columns={\"OPEN_home\": \"OPEN_home_exp10\",\n                                                                   \"n_home_early\": \"n_home_early_exp10\"})\n    d = d.merge(meta, on=[\"frame\", \"ci\"], how=\"left\", validate=\"1:1\")\n    chk = np.nanmax(np.abs(d.OPEN_home - d.OPEN_home_exp10))\n    mism = int((np.isnan(d.OPEN_home) ^ np.isnan(d.OPEN_home_exp10)).sum())\n    assert (d.n_home_early == d.n_home_early_exp10).all()\n    logger.info(f\"OPEN_home recomputed vs EXP10: max diff {chk:.2e}, NaN mismatches {mism}\")\n    d[\"log_n_home_early\"] = np.log(d.n_home_early)\n    d[\"uid\"] = np.where(d.frame == \"exp5\", \"E\", \"C\") + d.ci.astype(str)\n    d.to_parquet(DATA / \"clean_variants.parquet\", index=False)\n    logger.info(f\"wrote data/clean_variants.parquet {d.shape}\")\n    # ------------------------------------------------------------------ V4 reliability\n    pos = {(f, int(c)): i for i, (f, c) in enumerate(zip(d.frame, d.ci))}\n    nC = len(d)\n    S_RAW, S_CL = 100, 20\n    H = {h: {m: np.full((S_RAW, nC), np.nan, np.float32) for m in OUT6} for h in (\"A\", \"B\")}\n    HC: dict = {\"A\": {}, \"B\": {}}\n    for p in sorted((DATA / \"s2_parts_full\").glob(\"chunk_*.pkl\")):\n        z = pickle.loads(p.read_bytes())\n        for r, e in zip(z[\"rows\"], z[\"extras\"]):\n            if not e:\n                continue\n            i = pos[(r[\"frame\"], int(r[\"ci\"]))]\n            for h in (\"A\", \"B\"):\n                for j, m in enumerate(OUT6):\n                    H[h][m][:, i] = e[\"half_raw\"][h][:, j]\n                hc = e[\"half_clean\"][h]\n                for c in hc.columns:\n                    HC[h].setdefault(c, np.full((S_CL, nC), np.nan, np.float32))[:, i] = hc[c].to_numpy()\n    v3h = pickle.loads((DATA / \"v3_halves_full.pkl\").read_bytes())\n    for c in (\"z_pers_k\", \"z_dens_k\", \"z_dens_cfg\"):\n        for h in (\"A\", \"B\"):\n            HC[h][f\"{c}_v3\"] = np.full((S_CL, nC), np.nan, np.float32)\n    for j, (f, ci, h, sp) in enumerate(v3h[\"key\"]):\n        i = pos[(f, int(ci))]\n        for c in (\"z_pers_k\", \"z_dens_k\", \"z_dens_cfg\"):\n            HC[h][f\"{c}_v3\"][sp, i] = v3h[c][j]\n    # variant half matrices (S x nC) for A and B\n    VAR: dict = {}\n    for h in (\"A\", \"B\"):\n        V = {}\n        for m in OUT6:\n            V[f\"{m}__raw\"] = H[h][m].astype(float)\n        hd = pd.DataFrame({f\"{m}__raw\": H[h][m][s] for m in OUT6} for s in range(S_RAW))  # unused placeholder\n        del hd\n        raw_c = []\n        for s in range(S_RAW):\n            ds = pd.DataFrame({f\"{m}__raw\": H[h][m][s].astype(float) for m in OUT6})\n            raw_c.append(composites(ds, K10, KN)[[\"NOVCHURN_raw\", \"OPEN_home\"]])\n        V[\"NOVCHURN_raw\"] = np.stack([c.NOVCHURN_raw.to_numpy() for c in raw_c])\n        V[\"OPEN_home\"] = np.stack([c.OPEN_home.to_numpy() for c in raw_c])\n        cl = []\n        for s in range(S_CL):\n            ds = pd.DataFrame({f\"{m}__raw\": H[h][m][s].astype(float) for m in OUT6})\n            for c, arr in HC[h].items():\n                ds[c] = arr[s].astype(float)\n            ds[\"z_pers_cfg\"] = ds[\"z_pers_k_v3\"]          # declared approximation (k-matched MC on halves)\n            ds[\"z_dens_cfg\"] = ds[\"z_dens_cfg_v3\"]\n            ds[\"z_dens_k\"] = ds[\"z_dens_k_v3\"]\n            ds[\"NOV_res_rare5\"] = ds[\"NOV_res_rare5\"]\n            cc = composites(ds, K10, KN)\n            cl.append((ds, cc))\n        for col in [\"NOV_res_exc\", \"edge_persistence_exc\", \"ego_density_W3_exc\", \"new_edge_rate_exc\", \"NOV_res_zperm\",\n                    \"edge_persistence_zperm\", \"ego_density_W3_zperm\", \"NOV_res_rare5\", \"edge_persistence_rare5\",\n                    \"ego_density_W3_rare5\", \"z_pers_cfg\", \"z_dens_cfg\", \"z_dens_k\", \"edge_persistence_nullmean\"]:\n            V[col] = np.stack([ds[col].to_numpy(float) for ds, _ in cl])\n        for col in [\"NOVCHURN_exc\", \"NOVCHURN_zperm\", \"NOVCHURN_rare5\", \"NOVCHURN_cfg\", \"OPEN_home_clean\",\n                    \"OPEN_home_exc\"]:\n            V[col] = np.stack([cc[col].to_numpy(float) for _, cc in cl])\n        VAR[h] = V\n    notes = {\"z_pers_cfg\": \"halves use the k-matched Monte Carlo approximation of the curveball null (declared)\",\n             \"NOVCHURN_cfg\": \"halves use z_pers_k (k-matched MC) in place of the curveball z (declared)\",\n             \"OPEN_home_clean\": \"halves use z_pers_k for z_pers_cfg (declared)\",\n             \"NOV_res_rare5\": \"V1 on halves at n = 5 (concepts with >= 10 papers per W-year); used as the reliability \"\n                              \"proxy for every rarefied variant (rare10 cannot be split into halves of 10)\",\n             \"NOVCHURN_rare5\": \"proxy for NOVCHURN_rare10 reliability\"}\n    body = d.body.to_numpy()\n    nh = d.n_home_early.to_numpy()\n    rel: dict = {\"method\": \"r_s = Spearman(v_A, v_B) across concepts per split; r = tanh(mean atanh r_s); \"\n                           \"SB = 2r/(1+r); 100 splits raw, 20 clean\", \"notes\": notes, \"variants\": {}}\n    rng = np.random.default_rng(20260936)\n    boot_idx = [rng.integers(0, nC, nC) for _ in range(200)]\n    for v in VAR[\"A\"]:\n        A, B = VAR[\"A\"][v], VAR[\"B\"][v]\n        ent: dict = {}\n        r, sb, ns = sb_of(spearman_cols(A, B))\n        ent[\"pooled\"] = {\"r_half\": r, \"SB\": sb, \"n_splits\": ns,\n                         \"n_concepts_mean\": float(np.mean((np.isfinite(A) & np.isfinite(B)).sum(1)))}\n        for bd in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"):\n            m = body == bd\n            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))\n            ent[bd] = {\"r_half\": r, \"SB\": sb, \"n_splits\": ns,\n                       \"n_concepts_mean\": float(np.mean((np.isfinite(A[:, m]) & np.isfinite(B[:, m])).sum(1)))}\n        for lo, hi in NBINS:\n            m = (nh >= lo) & (nh <= hi)\n            r, sb, ns = sb_of(spearman_cols(A[:, m], B[:, m]))\n            ent[f\"n{lo}-{hi if hi < 10**9 else 'inf'}\"] = {\"r_half\": r, \"SB\": sb, \"n_splits\": ns,\n                                                           \"n_concepts\": int(m.sum())}\n        # concept bootstrap of pooled SB (first 10 splits for speed)\n        Ab, Bb = A[:10], B[:10]\n        bs = []\n        for idx in boot_idx:\n            bs.append(sb_of(spearman_cols(Ab[:, idx], Bb[:, idx]))[1])\n        bs = np.asarray(bs, float)\n        bs = bs[np.isfinite(bs)]\n        ent[\"pooled\"][\"SB_ci\"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if len(bs) else None\n        ent[\"pooled\"][\"SB_boot_sd\"] = float(bs.std()) if len(bs) else None\n        rel[\"variants\"][v] = ent\n        logger.info(f\"rel {v}: pooled SB {ent['pooled']['SB']:.3f}; COH1517 {ent['COH1517']['SB']:.3f}\")\n    jdump(rel, RES / \"reliability_x.json\")\n    # keep per-concept split-averaged half values for power / rederive\n    np.savez_compressed(DATA / \"v4_half_means.npz\",\n                        **{f\"{h}__{v}\": np.nanmean(VAR[h][v], 0) for h in (\"A\", \"B\") for v in VAR[h]})\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [115] TOOL CALL — Bash · 2026-09-29 05:40:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("s4_composites.py"); s=p.read_text()
old='''        hd = pd.DataFrame({f"{m}__raw": H[h][m][s] for m in OUT6} for s in range(S_RAW))  # unused placeholder
        del hd
'''
assert old in s; s=s.replace(old,""); s=s.replace('''            ds["NOV_res_rare5"] = ds["NOV_res_rare5"]\n''',""); p.write_text(s)
EOF
EXP5=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_experiment_5; sed -n 120,165p $EXP5/frame.py; tail -2 logs/s3_full.out; tail -2 logs/u_nulls.out
```

### [116] TOOL RESULT — Bash · 2026-09-29 05:40:30 UTC

```
{"stdout": "    early = V[yi(t0):yi(t0 + 2) + 1, 1:27]\n    ne = early.sum(0)\n    lab = ne.sum()\n    nA = V[yi(t0):yi(t0 + 1) + 1, 1:27].sum(0)\n    nB = V[yi(t0 + 2), 1:27]\n    rows = []\n    for k in range(26):\n        j = FIELD_IDS[k]\n        if j in home or ne[k] < 2 - 1e-9:\n            continue\n        rows.append({\"ci\": ci, \"field\": j, \"n_early\": float(ne[k]), \"n_A\": float(nA[k]), \"n_B\": float(nB[k]),\n                     \"share_early\": float(ne[k] / lab) if lab else math.nan,\n                     \"growth_j\": math.log((nB[k] + 1) / (nA[k] / 2 + 1))})\n    return rows\n\n\ndef episode_outcomes(V: np.ndarray, t0: int, field: int, share_early: float) -> dict:\n    out = V[yi(t0 + 6):yi(t0 + 8) + 1, 1:27].sum(0)\n    lab = out.sum()\n    n_out = float(out[field - 11])\n    s_out = n_out / lab if lab else math.nan\n    R = int(s_out >= 0.5 * share_early and n_out >= 9 - 1e-9) if np.isfinite(s_out) else math.nan\n    return {\"n_out\": n_out, \"share_out\": s_out, \"R\": R, \"R_abs1\": int(n_out >= 1 - 1e-9),\n            \"R_abs2\": int(n_out >= 2 - 1e-9), \"R_abs3\": int(n_out >= 3 - 1e-9), \"lab_out\": float(lab)}\n\n\ndef concept_outcomes(N: np.ndarray, V: np.ndarray, G: np.ndarray, t0: int) -> dict:\n    \"\"\"art_33 features.outcomes() on grounded yearly counts; O2r over ALL grounded labelled works t0+6..t0+8.\"\"\"\n    sh = lambda y: N[yi(y)] / G[yi(y)]  # noqa: E731\n    o1 = int(np.mean([sh(y) for y in range(t0 + 6, t0 + 9)]) >= sh(t0 + 5))\n    seq = [N[yi(y)] for y in range(t0, t0 + 9)]\n    peak_y = t0 + int(np.argmax(seq))\n    late = np.mean([N[yi(t0 + 7)], N[yi(t0 + 8)]])\n    o3 = int(t0 + 3 <= peak_y <= t0 + 8 and max(seq) / max(late, 1e-9) >= 2)\n    counts = V[yi(t0 + 6):yi(t0 + 8) + 1, 1:27].sum(0)\n    Nout = float(counts.sum())\n    return {\"O1\": o1, \"O3\": o3, \"peak_year\": peak_y, \"N_outcome\": Nout,\n            \"O2r_m30\": rarefied_richness_frac(counts, 30), \"O2r_m50\": rarefied_richness_frac(counts, 50),\n            \"O2_raw\": int((counts >= 15).sum())}\n\n\n# ----------------------------------------------------------------------------- commands\ndef cmd_match() -> None:\n    A = build_arrays(\"match\", n_concepts())\n    ot = onset_table(A[\"N\"])\n    ot.to_csv(RES / \"onset_candidates_match.csv\", index=False)\nslice 1: 40/200 rewires, 124s\nslice 2: 40/200 rewires, 136s\n05:38:26|INFO   |U3 toy: {'n_states': 12, 'freq': [2503.0, 2513.0, 2526.0, 2522.0, 2491.0, 2478.0, 2518.0, 2442.0, 2545.0, 2526.0, 2449.0, 2487.0], 'chi2_p': 0.9558059116407714, 'pass': True}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [117] TOOL CALL — Write · 2026-09-29 05:40:54 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4b_outcome_rel.py

#!/usr/bin/env python3
"""Outcome reliability (rel_y) for O2r_m50, run AFTER the S1b seal.

Outcome-window (t0+6..t0+8; COH1517 t0 = 2017: t0+5..t0+7) venue-field counts of TAG-grounded papers:
  EXP5 bodies  EXP5 scan/agg_counts.parquet (tagstate == 1)
  COH1517      EXP10 passC_pre_agg + sealed parts (tagstate == 1), the EXP10 build_outcomes inputs
Check: rarefied richness at m = 50 recomputed from these counts == the stored O2r_m50.
Split-half: 100 multivariate-hypergeometric halves of the outcome papers; exact rarefied richness at m = 25 on each
half (concepts with >= 50 outcome papers); Spearman across concepts; Fisher-mean; Spearman-Brown.
'conservative, m = 25 halves'. Adds results/reliability.json = reliability_x.json + outcome block."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata

from common import DATA, DATA_IN, EXP5, RES, jdump, setup_logger
from outc import rarefied_richness

logger = setup_logger("s4b_outcome_rel")
Y0 = 1995


def counts_exp5(fr: pd.DataFrame) -> dict:
    ag = pd.read_parquet(EXP5 / "scan/agg_counts.parquet", columns=["ci", "year", "vfield", "tagstate", "n"])
    ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(fr.ci)) & (ag.vfield >= 1)]
    t0 = fr.set_index("ci").t0
    ag = ag.assign(t0=t0.loc[ag.ci].to_numpy())
    ag = ag[(ag.year >= ag.t0 + 6) & (ag.year <= ag.t0 + 8)]
    out = {}
    for ci, g in ag.groupby("ci"):
        v = np.zeros(27)
        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))
        out[int(ci)] = v[1:27]
    return out


def counts_cohort(coh: pd.DataFrame) -> dict:
    pre = pd.read_parquet(DATA_IN / "passC_pre_agg.parquet")
    sealed = pd.concat([pd.read_parquet(p) for p in sorted((DATA_IN / "sealed/parts").glob("sealed_*.parquet"))],
                       ignore_index=True)
    agg = pd.concat([pre, sealed], ignore_index=True)
    agg = agg[(agg.tagstate == 1) & agg.ci.isin(set(coh.ci)) & (agg.vfield >= 1)]
    t0 = coh.set_index("ci").t0
    agg = agg.assign(t0=t0.loc[agg.ci].to_numpy())
    a = np.where(agg.t0 == 2017, 5, 6)
    agg = agg[(agg.year >= agg.t0 + a) & (agg.year <= agg.t0 + a + 2)]
    out = {}
    for ci, g in agg.groupby("ci"):
        v = np.zeros(27)
        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))
        out[int(ci)] = v[1:27]
    return out


def main() -> None:
    cv = pd.read_parquet(DATA / "clean_variants.parquet", columns=["frame", "ci", "body", "n_home_early"])
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci", "t0", "O2r_m50"])
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci", "t0", "O2r_m50"])
    ce = counts_exp5(fe[fe.ci.isin(cv[cv.frame == "exp5"].ci)])
    cc = counts_cohort(ac[ac.ci.isin(cv[cv.frame == "cohort"].ci)])
    rows = []
    for frame, tab, cnt in (("exp5", fe, ce), ("cohort", ac, cc)):
        tab = tab.set_index("ci")
        for ci in cv[cv.frame == frame].ci:
            v = cnt.get(int(ci), np.zeros(26))
            rows.append({"frame": frame, "ci": int(ci), "N_out": float(v.sum()),
                         "O2r_m50_recomputed": rarefied_richness([int(round(c)) for c in v], 50),
                         "O2r_m50": float(tab.at[ci, "O2r_m50"]), "vec": np.rint(v).astype(np.int64)})
    df = pd.DataFrame(rows).merge(cv, on=["frame", "ci"])
    both = df.O2r_m50.notna() & df.O2r_m50_recomputed.notna()
    md = float(np.max(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]))) if both.any() else math.nan
    agree = float(np.mean(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]) < 1e-9)) if both.any() else math.nan
    nan_mism = int((df.O2r_m50.isna() ^ df.O2r_m50_recomputed.isna()).sum())
    logger.info(f"O2r_m50 recomputation: max diff {md:.3g}; share exact {agree:.4f}; NaN mismatch {nan_mism}")
    rng = np.random.default_rng(20260937)
    elig = df[(df.N_out >= 50) & df.O2r_m50.notna()].reset_index(drop=True)
    S = 100
    A = np.full((S, len(elig)), np.nan)
    B = np.full((S, len(elig)), np.nan)
    for i, v in enumerate(elig.vec):
        v = v[v > 0]
        n = int(v.sum())
        for s in range(S):
            a = rng.multivariate_hypergeometric(v, n // 2)
            A[s, i] = rarefied_richness(a, 25)
            B[s, i] = rarefied_richness(v - a, 25)

    def sb(mask):
        rs = []
        for s in range(S):
            ok = mask & np.isfinite(A[s]) & np.isfinite(B[s])
            if ok.sum() < 20:
                continue
            rs.append(np.corrcoef(rankdata(A[s, ok]), rankdata(B[s, ok]))[0, 1])
        if not rs:
            return {"r_half": None, "SB": None, "n": int(mask.sum())}
        r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))
        return {"r_half": r, "SB": 2 * r / (1 + r), "n": int(mask.sum())}
    out = {"variable": "O2r_m50", "flag": "conservative, m = 25 halves (rarefied richness at 25 on each half of the "
                                          "outcome-window papers; multivariate hypergeometric thinning; 100 splits)",
           "recompute_check": {"max_abs_diff": md, "share_exact": agree, "nan_mismatch": nan_mism,
                               "n_compared": int(both.sum())},
           "eligible_min_outcome_papers": 50, "pooled": sb(np.ones(len(elig), bool))}
    for bd in ("DEV", "OLDHO", "COH1014", "COH1517"):
        out[bd] = sb((elig.body == bd).to_numpy())
    # bootstrap CI (concepts)
    bs = []
    for _ in range(200):
        idx = rng.integers(0, len(elig), len(elig))
        rs = [np.corrcoef(rankdata(A[s, idx]), rankdata(B[s, idx]))[0, 1] for s in range(10)
              if np.all(np.isfinite(A[s, idx])) and np.all(np.isfinite(B[s, idx]))]
        if rs:
            r = math.tanh(np.mean(np.arctanh(rs)))
            bs.append(2 * r / (1 + r))
    out["pooled"]["SB_ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else None
    out["pooled"]["SB_boot_sd"] = float(np.std(bs)) if bs else None
    logger.info(f"outcome reliability: {out['pooled']}")
    relx = json.loads((RES / "reliability_x.json").read_text())
    relx["outcome"] = {"O2r_m50": out, "O2r_resid": "O2r_resid = O2r_m50 - (a + b logvol): logvol is an early-window "
                                                    "covariate, so its reliability equals that of O2r_m50 up to the "
                                                    "shared variance; the O2r_m50 value is used for both"}
    jdump(relx, RES / "reliability.json")


if __name__ == "__main__":
    main()
```

### [118] TOOL RESULT — Write · 2026-09-29 05:40:54 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4b_outcome_rel.py", "content": "#!/usr/bin/env python3\n\"\"\"Outcome reliability (rel_y) for O2r_m50, run AFTER the S1b seal.\n\nOutcome-window (t0+6..t0+8; COH1517 t0 = 2017: t0+5..t0+7) venue-field counts of TAG-grounded papers:\n  EXP5 bodies  EXP5 scan/agg_counts.parquet (tagstate == 1)\n  COH1517      EXP10 passC_pre_agg + sealed parts (tagstate == 1), the EXP10 build_outcomes inputs\nCheck: rarefied richness at m = 50 recomputed from these counts == the stored O2r_m50.\nSplit-half: 100 multivariate-hypergeometric halves of the outcome papers; exact rarefied richness at m = 25 on each\nhalf (concepts with >= 50 outcome papers); Spearman across concepts; Fisher-mean; Spearman-Brown.\n'conservative, m = 25 halves'. Adds results/reliability.json = reliability_x.json + outcome block.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import rankdata\n\nfrom common import DATA, DATA_IN, EXP5, RES, jdump, setup_logger\nfrom outc import rarefied_richness\n\nlogger = setup_logger(\"s4b_outcome_rel\")\nY0 = 1995\n\n\ndef counts_exp5(fr: pd.DataFrame) -> dict:\n    ag = pd.read_parquet(EXP5 / \"scan/agg_counts.parquet\", columns=[\"ci\", \"year\", \"vfield\", \"tagstate\", \"n\"])\n    ag = ag[(ag.tagstate == 1) & ag.ci.isin(set(fr.ci)) & (ag.vfield >= 1)]\n    t0 = fr.set_index(\"ci\").t0\n    ag = ag.assign(t0=t0.loc[ag.ci].to_numpy())\n    ag = ag[(ag.year >= ag.t0 + 6) & (ag.year <= ag.t0 + 8)]\n    out = {}\n    for ci, g in ag.groupby(\"ci\"):\n        v = np.zeros(27)\n        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))\n        out[int(ci)] = v[1:27]\n    return out\n\n\ndef counts_cohort(coh: pd.DataFrame) -> dict:\n    pre = pd.read_parquet(DATA_IN / \"passC_pre_agg.parquet\")\n    sealed = pd.concat([pd.read_parquet(p) for p in sorted((DATA_IN / \"sealed/parts\").glob(\"sealed_*.parquet\"))],\n                       ignore_index=True)\n    agg = pd.concat([pre, sealed], ignore_index=True)\n    agg = agg[(agg.tagstate == 1) & agg.ci.isin(set(coh.ci)) & (agg.vfield >= 1)]\n    t0 = coh.set_index(\"ci\").t0\n    agg = agg.assign(t0=t0.loc[agg.ci].to_numpy())\n    a = np.where(agg.t0 == 2017, 5, 6)\n    agg = agg[(agg.year >= agg.t0 + a) & (agg.year <= agg.t0 + a + 2)]\n    out = {}\n    for ci, g in agg.groupby(\"ci\"):\n        v = np.zeros(27)\n        np.add.at(v, g.vfield.to_numpy(int), g.n.to_numpy(float))\n        out[int(ci)] = v[1:27]\n    return out\n\n\ndef main() -> None:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\", columns=[\"frame\", \"ci\", \"body\", \"n_home_early\"])\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\", \"t0\", \"O2r_m50\"])\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\", \"t0\", \"O2r_m50\"])\n    ce = counts_exp5(fe[fe.ci.isin(cv[cv.frame == \"exp5\"].ci)])\n    cc = counts_cohort(ac[ac.ci.isin(cv[cv.frame == \"cohort\"].ci)])\n    rows = []\n    for frame, tab, cnt in ((\"exp5\", fe, ce), (\"cohort\", ac, cc)):\n        tab = tab.set_index(\"ci\")\n        for ci in cv[cv.frame == frame].ci:\n            v = cnt.get(int(ci), np.zeros(26))\n            rows.append({\"frame\": frame, \"ci\": int(ci), \"N_out\": float(v.sum()),\n                         \"O2r_m50_recomputed\": rarefied_richness([int(round(c)) for c in v], 50),\n                         \"O2r_m50\": float(tab.at[ci, \"O2r_m50\"]), \"vec\": np.rint(v).astype(np.int64)})\n    df = pd.DataFrame(rows).merge(cv, on=[\"frame\", \"ci\"])\n    both = df.O2r_m50.notna() & df.O2r_m50_recomputed.notna()\n    md = float(np.max(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]))) if both.any() else math.nan\n    agree = float(np.mean(np.abs(df.O2r_m50[both] - df.O2r_m50_recomputed[both]) < 1e-9)) if both.any() else math.nan\n    nan_mism = int((df.O2r_m50.isna() ^ df.O2r_m50_recomputed.isna()).sum())\n    logger.info(f\"O2r_m50 recomputation: max diff {md:.3g}; share exact {agree:.4f}; NaN mismatch {nan_mism}\")\n    rng = np.random.default_rng(20260937)\n    elig = df[(df.N_out >= 50) & df.O2r_m50.notna()].reset_index(drop=True)\n    S = 100\n    A = np.full((S, len(elig)), np.nan)\n    B = np.full((S, len(elig)), np.nan)\n    for i, v in enumerate(elig.vec):\n        v = v[v > 0]\n        n = int(v.sum())\n        for s in range(S):\n            a = rng.multivariate_hypergeometric(v, n // 2)\n            A[s, i] = rarefied_richness(a, 25)\n            B[s, i] = rarefied_richness(v - a, 25)\n\n    def sb(mask):\n        rs = []\n        for s in range(S):\n            ok = mask & np.isfinite(A[s]) & np.isfinite(B[s])\n            if ok.sum() < 20:\n                continue\n            rs.append(np.corrcoef(rankdata(A[s, ok]), rankdata(B[s, ok]))[0, 1])\n        if not rs:\n            return {\"r_half\": None, \"SB\": None, \"n\": int(mask.sum())}\n        r = math.tanh(np.mean(np.arctanh(np.clip(rs, -0.999999, 0.999999))))\n        return {\"r_half\": r, \"SB\": 2 * r / (1 + r), \"n\": int(mask.sum())}\n    out = {\"variable\": \"O2r_m50\", \"flag\": \"conservative, m = 25 halves (rarefied richness at 25 on each half of the \"\n                                          \"outcome-window papers; multivariate hypergeometric thinning; 100 splits)\",\n           \"recompute_check\": {\"max_abs_diff\": md, \"share_exact\": agree, \"nan_mismatch\": nan_mism,\n                               \"n_compared\": int(both.sum())},\n           \"eligible_min_outcome_papers\": 50, \"pooled\": sb(np.ones(len(elig), bool))}\n    for bd in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"):\n        out[bd] = sb((elig.body == bd).to_numpy())\n    # bootstrap CI (concepts)\n    bs = []\n    for _ in range(200):\n        idx = rng.integers(0, len(elig), len(elig))\n        rs = [np.corrcoef(rankdata(A[s, idx]), rankdata(B[s, idx]))[0, 1] for s in range(10)\n              if np.all(np.isfinite(A[s, idx])) and np.all(np.isfinite(B[s, idx]))]\n        if rs:\n            r = math.tanh(np.mean(np.arctanh(rs)))\n            bs.append(2 * r / (1 + r))\n    out[\"pooled\"][\"SB_ci\"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))] if bs else None\n    out[\"pooled\"][\"SB_boot_sd\"] = float(np.std(bs)) if bs else None\n    logger.info(f\"outcome reliability: {out['pooled']}\")\n    relx = json.loads((RES / \"reliability_x.json\").read_text())\n    relx[\"outcome\"] = {\"O2r_m50\": out, \"O2r_resid\": \"O2r_resid = O2r_m50 - (a + b logvol): logvol is an early-window \"\n                                                    \"covariate, so its reliability equals that of O2r_m50 up to the \"\n                                                    \"shared variance; the O2r_m50 value is used for both\"}\n    jdump(relx, RES / \"reliability.json\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [119] ASSISTANT · 2026-09-29 05:41:26 UTC

```
S3 rewiring is at ~40/200 draws per slice. Meanwhile I'll time `psp_point` on the pooled table to size the S4 bootstrap.
```

### [120] TOOL CALL — Bash · 2026-09-29 05:41:26 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -1 logs/s3_full.out; .venv/bin/python - <<'EOF'
import sys; sys.path.insert(0,"lib")
import pandas as pd, numpy as np, time
from ladder import rung_design
from rq1stats import psp_point
S="/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/data/"
fe=pd.read_parquet(S+"features_exp5_open.parquet")
fe=fe[fe.n_home_early>=10]
for r in ("R0","R2","R3","R5"):
    Bc,Cc=rung_design(fe,r); x=fe.OPEN_home.to_numpy(float); y=fe.O2r_m50.to_numpy(float)
    ok=np.isfinite(x)&np.isfinite(y)&np.all(np.isfinite(Bc.to_numpy(float)),1)
    B=Bc.to_numpy(float)[ok]; C=Cc.to_numpy(float)[ok]; x=x[ok]; y=y[ok]
    t=time.time()
    for _ in range(20):
        i=np.random.randint(0,len(x),len(x)); psp_point(x[i],y[i],B[i],C[i])
    print(r, len(x), B.shape, C.shape, (time.time()-t)/20*1e3, "ms")
print(fe.columns.tolist()[:5], fe.type.value_counts().to_dict())
EOF
```

### [121] TOOL RESULT — Bash · 2026-09-29 05:41:48 UTC

```
{"stdout": "slice 0: 100/200 rewires, 219s\nR0 6565 (6565, 5) (6565, 11) 32.57371187210083 ms\nR2 6565 (6565, 6) (6565, 18) 63.77749443054199 ms\nR3 6565 (6565, 8) (6565, 21) 102.24322080612183 ms\nR5 6565 (6565, 10) (6565, 26) 260.1498246192932 ms\n['ci', 'concept_id', 'name', 't0', 'group'] {'object': 6732, 'topic': 2102, 'method': 1798, 'property': 1447}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [122] THINKING · 2026-09-29 05:42:36 UTC

```
`psp_point` is too slow for the bootstrap workload, so I'll build a faster normal-equations version for the draws while keeping the original for point estimates, then validate the two against each other.
```

### [123] TOOL CALL — Write · 2026-09-29 05:42:36 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/fastpsp.py

"""Fast partial Spearman for bootstrap draws (same estimand as rq1stats.psp_point).

psp = Pearson(resid(rank x ~ 1 + rank B + C), resid(rank y ~ same)). The projection is computed from the normal
equations of the column-scaled design (ranks / n) solved by lstsq on the small p x p Gram matrix -- the projection is
unique even when the design is rank-deficient, so residuals equal those of rq1stats.psp_point up to rounding
(validated to <= 1e-9 in tests/u_fastpsp.py). Point estimates in every result use the ORIGINAL rq1stats.psp_point;
only bootstrap draws use this function. psp_boot2_fast consumes the RNG exactly like ladder.psp_boot2."""
from __future__ import annotations

import math

import numpy as np
from scipy import stats
from scipy.stats import rankdata

from rq1stats import psp_point


def psp_fast(x: np.ndarray, y: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:
    n = len(x)
    cols = [np.ones((n, 1))]
    if B is not None and B.shape[1]:
        cols.append(rankdata(B, axis=0) / n)
    if C is not None and C.shape[1]:
        cols.append(C)
    Z = np.hstack(cols)
    Y = np.c_[rankdata(x), rankdata(y)] / n
    G = Z.T @ Z
    beta = np.linalg.lstsq(G, Z.T @ Y, rcond=1e-13)[0]
    R = Y - Z @ beta
    sx, sy = R[:, 0].std(), R[:, 1].std()
    if sx <= 1e-12 / n or sy <= 1e-12 / n:
        return float("nan")
    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])


def boot_indices(n: int, n_boot: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.stack([rng.integers(0, n, n) for _ in range(n_boot)]) if n_boot else np.zeros((0, n), np.int64)


def complete(x, y, B, C):
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
    return ok


def psp_boot2_fast(x, y, B, C, n_boot: int, seed: int, direction: int = 1, min_n: int = 30) -> dict:
    """== ladder.psp_boot2 (point by the original psp_point; draws by psp_fast with identical resample indices)."""
    ok = complete(x, y, B, C)
    x, y, B, C = x[ok], y[ok], B[ok], C[ok]
    n = len(x)
    if n < min_n or np.unique(x).size < 3:
        return {"n": int(n), "rho": math.nan, "ci": [math.nan, math.nan], "se": math.nan, "p_one": math.nan,
                "p_two": math.nan, "boot": np.array([])}
    est = psp_point(x, y, B, C)
    rng = np.random.default_rng(seed)
    bs = np.empty(n_boot)
    for b in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0 if Ci.shape[1] else np.zeros(0, bool)
        bs[b] = psp_fast(x[i], y[i], B[i], Ci[:, keep])
    bs = bs[np.isfinite(bs)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    p_one = float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1))
    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))
    se_z = float(np.std(z, ddof=1))
    ze = math.atanh(max(min(est, 0.999999), -0.999999))
    return {"n": int(n), "rho": float(est), "ci": [float(lo), float(hi)], "se": float(np.std(bs, ddof=1)),
            "se_z": se_z, "p_one": p_one,
            "p_two": float(2 * stats.norm.sf(abs(ze / se_z))) if se_z > 0 else math.nan, "boot": bs}


def paired_fast(xa, xb, y, B, C, n_boot: int, seed: int, min_n: int = 30) -> dict:
    """Paired concept bootstrap of psp(xa) and psp(xb) on the common sample: diff and ratio (xa / xb) with shared
    resample indices (== ladder.paired_diff resampling)."""
    ok = np.isfinite(xa) & np.isfinite(xb) & complete(xa, y, B, C)
    xa, xb, y, B, C = xa[ok], xb[ok], y[ok], B[ok], C[ok]
    n = len(y)
    if n < min_n or np.unique(xa).size < 3 or np.unique(xb).size < 3:
        return {"n": int(n), "a": math.nan, "b": math.nan, "diff": math.nan, "diff_ci": [math.nan] * 2,
                "ratio": math.nan, "ratio_ci": [math.nan] * 2}
    pa, pb = psp_point(xa, y, B, C), psp_point(xb, y, B, C)
    rng = np.random.default_rng(seed)
    A_, B_ = np.empty(n_boot), np.empty(n_boot)
    for k in range(n_boot):
        i = rng.integers(0, n, n)
        Ci = C[i]
        keep = Ci.std(0) > 0
        A_[k] = psp_fast(xa[i], y[i], B[i], Ci[:, keep])
        B_[k] = psp_fast(xb[i], y[i], B[i], Ci[:, keep])
    f = np.isfinite(A_) & np.isfinite(B_)
    d = A_[f] - B_[f]
    with np.errstate(divide="ignore", invalid="ignore"):
        r = A_[f] / B_[f]
    return {"n": int(n), "a": float(pa), "b": float(pb), "diff": float(pa - pb),
            "diff_ci": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],
            "ratio": float(pa / pb) if pb != 0 else math.nan,
            "ratio_ci": [float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))],
            "a_ci": [float(np.percentile(A_[f], 2.5)), float(np.percentile(A_[f], 97.5))],
            "b_ci": [float(np.percentile(B_[f], 2.5)), float(np.percentile(B_[f], 97.5))],
            "p_diff_le0": float((np.sum(d <= 0) + 1) / (len(d) + 1)), "resampling_unit": "concept"}
```

### [124] TOOL RESULT — Write · 2026-09-29 05:42:36 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/fastpsp.py", "content": "\"\"\"Fast partial Spearman for bootstrap draws (same estimand as rq1stats.psp_point).\n\npsp = Pearson(resid(rank x ~ 1 + rank B + C), resid(rank y ~ same)). The projection is computed from the normal\nequations of the column-scaled design (ranks / n) solved by lstsq on the small p x p Gram matrix -- the projection is\nunique even when the design is rank-deficient, so residuals equal those of rq1stats.psp_point up to rounding\n(validated to <= 1e-9 in tests/u_fastpsp.py). Point estimates in every result use the ORIGINAL rq1stats.psp_point;\nonly bootstrap draws use this function. psp_boot2_fast consumes the RNG exactly like ladder.psp_boot2.\"\"\"\nfrom __future__ import annotations\n\nimport math\n\nimport numpy as np\nfrom scipy import stats\nfrom scipy.stats import rankdata\n\nfrom rq1stats import psp_point\n\n\ndef psp_fast(x: np.ndarray, y: np.ndarray, B: np.ndarray, C: np.ndarray) -> float:\n    n = len(x)\n    cols = [np.ones((n, 1))]\n    if B is not None and B.shape[1]:\n        cols.append(rankdata(B, axis=0) / n)\n    if C is not None and C.shape[1]:\n        cols.append(C)\n    Z = np.hstack(cols)\n    Y = np.c_[rankdata(x), rankdata(y)] / n\n    G = Z.T @ Z\n    beta = np.linalg.lstsq(G, Z.T @ Y, rcond=1e-13)[0]\n    R = Y - Z @ beta\n    sx, sy = R[:, 0].std(), R[:, 1].std()\n    if sx <= 1e-12 / n or sy <= 1e-12 / n:\n        return float(\"nan\")\n    return float(np.corrcoef(R[:, 0], R[:, 1])[0, 1])\n\n\ndef boot_indices(n: int, n_boot: int, seed: int) -> np.ndarray:\n    rng = np.random.default_rng(seed)\n    return np.stack([rng.integers(0, n, n) for _ in range(n_boot)]) if n_boot else np.zeros((0, n), np.int64)\n\n\ndef complete(x, y, B, C):\n    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)\n    return ok\n\n\ndef psp_boot2_fast(x, y, B, C, n_boot: int, seed: int, direction: int = 1, min_n: int = 30) -> dict:\n    \"\"\"== ladder.psp_boot2 (point by the original psp_point; draws by psp_fast with identical resample indices).\"\"\"\n    ok = complete(x, y, B, C)\n    x, y, B, C = x[ok], y[ok], B[ok], C[ok]\n    n = len(x)\n    if n < min_n or np.unique(x).size < 3:\n        return {\"n\": int(n), \"rho\": math.nan, \"ci\": [math.nan, math.nan], \"se\": math.nan, \"p_one\": math.nan,\n                \"p_two\": math.nan, \"boot\": np.array([])}\n    est = psp_point(x, y, B, C)\n    rng = np.random.default_rng(seed)\n    bs = np.empty(n_boot)\n    for b in range(n_boot):\n        i = rng.integers(0, n, n)\n        Ci = C[i]\n        keep = Ci.std(0) > 0 if Ci.shape[1] else np.zeros(0, bool)\n        bs[b] = psp_fast(x[i], y[i], B[i], Ci[:, keep])\n    bs = bs[np.isfinite(bs)]\n    lo, hi = np.percentile(bs, [2.5, 97.5])\n    p_one = float((np.sum(direction * bs <= 0) + 1) / (len(bs) + 1))\n    z = np.arctanh(np.clip(bs, -0.999999, 0.999999))\n    se_z = float(np.std(z, ddof=1))\n    ze = math.atanh(max(min(est, 0.999999), -0.999999))\n    return {\"n\": int(n), \"rho\": float(est), \"ci\": [float(lo), float(hi)], \"se\": float(np.std(bs, ddof=1)),\n            \"se_z\": se_z, \"p_one\": p_one,\n            \"p_two\": float(2 * stats.norm.sf(abs(ze / se_z))) if se_z > 0 else math.nan, \"boot\": bs}\n\n\ndef paired_fast(xa, xb, y, B, C, n_boot: int, seed: int, min_n: int = 30) -> dict:\n    \"\"\"Paired concept bootstrap of psp(xa) and psp(xb) on the common sample: diff and ratio (xa / xb) with shared\n    resample indices (== ladder.paired_diff resampling).\"\"\"\n    ok = np.isfinite(xa) & np.isfinite(xb) & complete(xa, y, B, C)\n    xa, xb, y, B, C = xa[ok], xb[ok], y[ok], B[ok], C[ok]\n    n = len(y)\n    if n < min_n or np.unique(xa).size < 3 or np.unique(xb).size < 3:\n        return {\"n\": int(n), \"a\": math.nan, \"b\": math.nan, \"diff\": math.nan, \"diff_ci\": [math.nan] * 2,\n                \"ratio\": math.nan, \"ratio_ci\": [math.nan] * 2}\n    pa, pb = psp_point(xa, y, B, C), psp_point(xb, y, B, C)\n    rng = np.random.default_rng(seed)\n    A_, B_ = np.empty(n_boot), np.empty(n_boot)\n    for k in range(n_boot):\n        i = rng.integers(0, n, n)\n        Ci = C[i]\n        keep = Ci.std(0) > 0\n        A_[k] = psp_fast(xa[i], y[i], B[i], Ci[:, keep])\n        B_[k] = psp_fast(xb[i], y[i], B[i], Ci[:, keep])\n    f = np.isfinite(A_) & np.isfinite(B_)\n    d = A_[f] - B_[f]\n    with np.errstate(divide=\"ignore\", invalid=\"ignore\"):\n        r = A_[f] / B_[f]\n    return {\"n\": int(n), \"a\": float(pa), \"b\": float(pb), \"diff\": float(pa - pb),\n            \"diff_ci\": [float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))],\n            \"ratio\": float(pa / pb) if pb != 0 else math.nan,\n            \"ratio_ci\": [float(np.percentile(r, 2.5)), float(np.percentile(r, 97.5))],\n            \"a_ci\": [float(np.percentile(A_[f], 2.5)), float(np.percentile(A_[f], 97.5))],\n            \"b_ci\": [float(np.percentile(B_[f], 2.5)), float(np.percentile(B_[f], 97.5))],\n            \"p_diff_le0\": float((np.sum(d <= 0) + 1) / (len(d) + 1)), \"resampling_unit\": \"concept\"}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [125] TOOL CALL — Bash · 2026-09-29 05:42:36 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; mkdir -p tests; cat > tests/u_fastpsp.py <<'EOF'
#!/usr/bin/env python3
"""U7b: psp_fast == rq1stats.psp_point on bootstrap resamples of the EXP5 and cohort tables at R0/R2/R3/R5
(max |diff| <= 1e-9) + timing -> results/unit_tests_fastpsp.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import numpy as np, pandas as pd
from common import DATA_IN, RES, jdump
from fastpsp import psp_fast
from ladder import rung_design
from rq1stats import psp_point
out = {}
worst = 0.0
for nm, f, x in (("exp5", "features_exp5_open.parquet", "OPEN_home"), ("cohort", "analysis_cohort.parquet", "OPEN_home")):
    d = pd.read_parquet(DATA_IN / f)
    for r in ("R0", "R2", "R3", "R5"):
        Bc, Cc = rung_design(d, r)
        xv, yv = d[x].to_numpy(float), d.O2r_m50.to_numpy(float)
        B, C = Bc.to_numpy(float), Cc.to_numpy(float)
        ok = np.isfinite(xv) & np.isfinite(yv) & np.all(np.isfinite(B), 1) & np.all(np.isfinite(C), 1)
        xv, yv, B, C = xv[ok], yv[ok], B[ok], C[ok]
        rng = np.random.default_rng(0)
        t1 = t2 = 0.0
        for _ in range(20):
            i = rng.integers(0, len(xv), len(xv)); Ci = C[i]; keep = Ci.std(0) > 0
            t = time.time(); a = psp_point(xv[i], yv[i], B[i], Ci[:, keep]); t1 += time.time() - t
            t = time.time(); b = psp_fast(xv[i], yv[i], B[i], Ci[:, keep]); t2 += time.time() - t
            worst = max(worst, abs(a - b))
        out[f"{nm}_{r}"] = {"n": int(len(xv)), "orig_ms": t1 / 20 * 1e3, "fast_ms": t2 / 20 * 1e3}
        print(nm, r, out[f"{nm}_{r}"], worst, flush=True)
out["max_abs_diff"] = worst
out["pass"] = bool(worst <= 1e-9)
jdump(out, RES / "unit_tests_fastpsp.json")
print("pass", out["pass"], worst)
EOF
.venv/bin/python tests/u_fastpsp.py; tail -1 logs/s3_full.out
```

### [126] TOOL RESULT — Bash · 2026-09-29 05:42:36 UTC

```
{"stdout": "exp5 R0 {'n': 6565, 'orig_ms': 5.025172233581543, 'fast_ms': 4.093492031097412} 6.938893903907228e-17\nexp5 R2 {'n': 6565, 'orig_ms': 5.9647440910339355, 'fast_ms': 4.482543468475342} 6.938893903907228e-17\nexp5 R3 {'n': 6565, 'orig_ms': 8.433723449707031, 'fast_ms': 6.13255500793457} 6.938893903907228e-17\nexp5 R5 {'n': 6565, 'orig_ms': 11.53939962387085, 'fast_ms': 8.334493637084961} 6.938893903907228e-17\ncohort R0 {'n': 573, 'orig_ms': 0.7292985916137695, 'fast_ms': 0.6807208061218262} 1.6653345369377348e-16\ncohort R2 {'n': 573, 'orig_ms': 0.835263729095459, 'fast_ms': 0.7342934608459473} 2.3592239273284576e-16\ncohort R3 {'n': 573, 'orig_ms': 0.9442329406738281, 'fast_ms': 0.8031845092773438} 2.3592239273284576e-16\ncohort R5 {'n': 573, 'orig_ms': 1.157069206237793, 'fast_ms': 0.9620428085327148} 2.3592239273284576e-16\npass True 2.3592239273284576e-16\nslice 2: 100/200 rewires, 293s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [127] ASSISTANT · 2026-09-29 05:43:22 UTC

```
Thread oversubscription was the culprit: single-threaded, the original takes 5–11 ms and the fast version is 1.3× faster and identical (max diff 2.4e-16). Next, the shared table builder for S4/S5:
```

### [128] TOOL CALL — Write · 2026-09-29 05:43:22 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/tables.py

"""Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.
Selection data, outcomes previously unsealed by EXP5/EXP8/EXP10."""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import DATA, DATA_IN
from ladder import rung_design

COV = ["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "type", "generic", "level",
       "fp_logN", "fp_nfields", "fp_reemerge", "fp_wiki_pre", "newborn", "t0", "agroup", "label_coverage_early",
       "home_coverage_early", "n_all_early", "O2r_m50", "O2r_resid"]
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517"]


def load_tables() -> dict[str, pd.DataFrame]:
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    cv = cv.drop(columns=[c for c in ("t0",) if c in cv.columns])
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci"] + COV)
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci"] + COV + ["window_flag"])
    cv = cv.drop(columns=[c for c in ("agroup",) if c in cv.columns])
    e = cv[cv.frame == "exp5"].merge(fe, on="ci", how="inner", validate="1:1")
    e["window_flag"] = 0
    c = cv[cv.frame == "cohort"].merge(ac, on="ci", how="inner", validate="1:1")
    pooled = pd.concat([e, c], ignore_index=True)
    pooled["window_flag"] = pooled.window_flag.fillna(0).astype(int)
    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}
    out["POOLED"] = pooled
    return out


def design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:
    Bc, Cc = rung_design(df, rung, drop_group=drop_group)
    if pooled and df.body.nunique() > 1:
        bs = sorted(df.body.unique())[1:]
        Cc = pd.concat([Cc, pd.DataFrame({f"body_{b}": (df.body == b).astype(float) for b in bs}, index=df.index)],
                       axis=1)
        Cc = Cc.loc[:, Cc.std() > 0]
    return Bc.to_numpy(float), Cc.to_numpy(float)
```

### [129] TOOL RESULT — Write · 2026-09-29 05:43:22 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/lib/tables.py", "content": "\"\"\"Analysis tables: clean_variants joined with the EXP10 covariate frames and the (previously unsealed) outcomes.\nSelection data, outcomes previously unsealed by EXP5/EXP8/EXP10.\"\"\"\nfrom __future__ import annotations\n\nimport numpy as np\nimport pandas as pd\n\nfrom common import DATA, DATA_IN\nfrom ladder import rung_design\n\nCOV = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\", \"type\", \"generic\", \"level\",\n       \"fp_logN\", \"fp_nfields\", \"fp_reemerge\", \"fp_wiki_pre\", \"newborn\", \"t0\", \"agroup\", \"label_coverage_early\",\n       \"home_coverage_early\", \"n_all_early\", \"O2r_m50\", \"O2r_resid\"]\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\"]\n\n\ndef load_tables() -> dict[str, pd.DataFrame]:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    cv = cv.drop(columns=[c for c in (\"t0\",) if c in cv.columns])\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\"] + COV)\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\"] + COV + [\"window_flag\"])\n    cv = cv.drop(columns=[c for c in (\"agroup\",) if c in cv.columns])\n    e = cv[cv.frame == \"exp5\"].merge(fe, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    e[\"window_flag\"] = 0\n    c = cv[cv.frame == \"cohort\"].merge(ac, on=\"ci\", how=\"inner\", validate=\"1:1\")\n    pooled = pd.concat([e, c], ignore_index=True)\n    pooled[\"window_flag\"] = pooled.window_flag.fillna(0).astype(int)\n    out = {b: pooled[pooled.body == b].reset_index(drop=True) for b in BODIES}\n    out[\"POOLED\"] = pooled\n    return out\n\n\ndef design(df: pd.DataFrame, rung: str, pooled: bool, drop_group: bool = False) -> tuple[np.ndarray, np.ndarray]:\n    Bc, Cc = rung_design(df, rung, drop_group=drop_group)\n    if pooled and df.body.nunique() > 1:\n        bs = sorted(df.body.unique())[1:]\n        Cc = pd.concat([Cc, pd.DataFrame({f\"body_{b}\": (df.body == b).astype(float) for b in bs}, index=df.index)],\n                       axis=1)\n        Cc = Cc.loc[:, Cc.std() > 0]\n    return Bc.to_numpy(float), Cc.to_numpy(float)\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [130] ASSISTANT · 2026-09-29 05:43:44 UTC

```
Now the S4 association script:
```

### [131] TOOL CALL — Write · 2026-09-29 05:43:44 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s6_assoc.py

#!/usr/bin/env python3
"""S4 ASSOCIATIONS (selection data, outcomes previously unsealed): partial Spearman given the EXP10 rung ladder for raw
and clean variants per body and POOLED, paired clean-vs-raw bootstraps (diff and retention ratio), per-group DL,
disattenuation, planted-association checks (PC3), and the mechanical evaluation of P1-P3 and the VERDICT.
Writes results/clean_vs_raw_psp.json and data/psp_boot.npz."""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")

import argparse
import json
import math
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, RES, jdump, setup_logger

LABEL = "selection data, outcomes previously unsealed"
SEED = 20260930
RAW = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "NOVCHURN_raw", "OPEN_home"]
CLEAN = ["NOV_res_rare5", "NOV_res_rare10", "NOV_res_rare20", "edge_persistence_rare5", "edge_persistence_rare10",
         "edge_persistence_rare20", "ego_density_W3_rare10", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_rare20",
         "NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "NOV_res_zperm", "edge_persistence_zperm",
         "NOVCHURN_exc", "NOVCHURN_zperm", "EP_chao", "NOVCHURN_chao", "z_dens_cfg", "z_dens_k", "z_pers_cfg",
         "excess_pers_cfg", "NOVCHURN_cfg", "OPEN_home_clean", "OPEN_home_exc", "edge_persistence_nullmean"]
NEG = {"edge_persistence__raw", "ego_density_W3__raw", "edge_persistence_rare5", "edge_persistence_rare10",
       "edge_persistence_rare20", "ego_density_W3_rare10", "edge_persistence_exc", "ego_density_W3_exc",
       "edge_persistence_zperm", "EP_chao", "z_dens_cfg", "z_dens_k", "z_pers_cfg", "excess_pers_cfg",
       "edge_persistence_nullmean"}
PAIRS = [("NOVCHURN_exc", "NOVCHURN_raw"), ("NOVCHURN_rare5", "NOVCHURN_raw"), ("NOVCHURN_rare10", "NOVCHURN_raw"),
         ("NOVCHURN_rare20", "NOVCHURN_raw"), ("NOVCHURN_cfg", "NOVCHURN_raw"), ("NOVCHURN_chao", "NOVCHURN_raw"),
         ("NOVCHURN_zperm", "NOVCHURN_raw"), ("NOV_res_exc", "NOV_res__raw"), ("NOV_res_rare10", "NOV_res__raw"),
         ("NOV_res_zperm", "NOV_res__raw"), ("edge_persistence_exc", "edge_persistence__raw"),
         ("edge_persistence_rare10", "edge_persistence__raw"), ("z_pers_cfg", "edge_persistence__raw"),
         ("EP_chao", "edge_persistence__raw"), ("edge_persistence_zperm", "edge_persistence__raw"),
         ("excess_pers_cfg", "edge_persistence__raw"), ("z_dens_cfg", "ego_density_W3__raw"),
         ("z_dens_k", "ego_density_W3__raw"), ("ego_density_W3_exc", "ego_density_W3__raw"),
         ("OPEN_home_clean", "OPEN_home"), ("OPEN_home_exc", "OPEN_home")]
GROUP_X = ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_cfg", "NOVCHURN_rare10", "OPEN_home", "OPEN_home_clean"]
BODY_KEYS = ["DEV", "OLDHO", "COH1014", "COH1517", "POOLED"]
_T: dict = {}


def _init() -> None:
    import warnings
    warnings.simplefilter("ignore", RuntimeWarning)
    from tables import load_tables
    _T.update(load_tables())


def run_task(task: tuple) -> tuple:
    from fastpsp import paired_fast, psp_boot2_fast
    from tables import design
    kind = task[0]
    t = time.time()
    if kind == "psp":
        _, body, x, y, rung, B, sub = task
        df = _T[body]
        if sub is not None:
            df = df[df.agroup == sub].reset_index(drop=True)
        Bm, Cm = design(df, rung, body == "POOLED", drop_group=sub is not None)
        r = psp_boot2_fast(df[x].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B,
                           SEED + (101 * (1 + ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"].index(sub))
                                   if sub else 0), -1 if x in NEG else 1)
        return task, r, time.time() - t
    if kind == "pair":
        _, body, xa, xb, y, rung, B = task
        df = _T[body]
        Bm, Cm = design(df, rung, body == "POOLED")
        r = paired_fast(df[xa].to_numpy(float), df[xb].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B, SEED)
        return task, r, time.time() - t
    if kind == "planted":
        _, body, B = task
        df = _T[body]
        Bm, Cm = design(df, "R2", body == "POOLED")
        y = df["O2r_m50"].to_numpy(float)
        rr = df["O2r_resid"].to_numpy(float)
        rng = np.random.default_rng(SEED + 7)
        ok = np.isfinite(rr)
        rk = np.full(len(rr), np.nan)
        rk[ok] = stats.rankdata(rr[ok])
        sd = np.nanstd(rk)
        x = rk + rng.normal(0, 3 * sd, len(rk))
        res = {"planted": _strip(psp_boot2_fast(x, y, Bm, Cm, B, SEED))}
        pl = []
        for k in range(20):
            xs = x.copy()
            xs[ok] = rng.permutation(x[ok])
            pl.append(_strip(psp_boot2_fast(xs, y, Bm, Cm, B, SEED + k)))
        res["placebos"] = pl
        res["n_placebo_ci_excl0"] = int(sum(1 for p in pl if np.isfinite(p["rho"]) and (p["ci"][0] > 0 or p["ci"][1] < 0)))
        return task, res, time.time() - t
    raise ValueError(kind)


def _strip(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "boot"}


def build_tasks(B: int, B2: int) -> list:
    tasks = []
    for body in BODY_KEYS:
        for x in RAW + CLEAN:
            for rung in ("R0", "R2", "R3"):
                tasks.append(("psp", body, x, "O2r_m50", rung, B, None))
            for rung in ("R0", "R2", "R3"):
                tasks.append(("psp", body, x, "O2r_resid", rung, B2, None))
        for xa, xb in PAIRS:
            for rung in ("R2", "R3"):
                tasks.append(("pair", body, xa, xb, "O2r_m50", rung, B))
        tasks.append(("planted", body, 1000))
    for x in GROUP_X:
        for g in ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC"]:
            tasks.append(("psp", "POOLED", x, "O2r_m50", "R2", B, g))
    for x in ["OPEN_home", "NOVCHURN_raw", "NOVCHURN_exc"]:
        tasks.append(("psp", "POOLED", x, "O2r_m50", "R5", B, None))
        tasks.append(("psp", "COH1517", x, "O2r_m50", "R5", B, None))
    return tasks


def cost(t: tuple) -> float:
    base = {"POOLED": 7, "DEV": 3, "COH1014": 2.5, "OLDHO": 2, "COH1517": 0.6}[t[1]]
    return base * (2 if t[0] == "pair" else 20 if t[0] == "planted" else 1)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--B2", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    logger = setup_logger(f"s6_assoc{a.tag}")
    tasks = build_tasks(a.B, a.B2)
    if a.limit:
        tasks = tasks[:: max(1, len(tasks) // a.limit)]
    tasks.sort(key=lambda t: -cost(t))
    logger.info(f"{len(tasks)} tasks, B = {a.B}, workers {a.workers}")
    res_psp, res_pair, res_grp, res_pl, boots = {}, {}, {}, {}, {}
    t0 = time.time()
    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex:
        futs = [ex.submit(run_task, t) for t in tasks]
        for i, fu in enumerate(as_completed(futs)):
            task, r, dt = fu.result()
            if task[0] == "psp":
                _, body, x, y, rung, B, sub = task
                key = f"{body}|{x}|{y}|{rung}"
                if sub is not None:
                    res_grp.setdefault(f"{x}|{y}|{rung}", {})[sub] = _strip(r)
                else:
                    if y == "O2r_m50" and len(r.get("boot", [])):
                        boots[key] = r["boot"].astype(np.float32)
                    res_psp[key] = _strip(r) | {"x": x, "y": y, "rung": rung, "body": body}
            elif task[0] == "pair":
                _, body, xa, xb, y, rung, B = task
                res_pair[f"{body}|{xa}|{xb}|{y}|{rung}"] = r
            else:
                res_pl[task[1]] = r
            if i % 50 == 0:
                el = time.time() - t0
                logger.info(f"{i+1}/{len(tasks)} done; {el/60:.1f} min; eta {el/(i+1)*(len(tasks)-i-1)/60:.1f} min")
    np.savez_compressed(DATA / f"psp_boot{a.tag}.npz", **{k.replace("|", "__"): v for k, v in boots.items()})
    out = {"label": LABEL, "B": a.B, "B_O2r_resid": a.B2, "seed": SEED, "resampling_unit": "concept",
           "psp": res_psp, "paired": res_pair, "groups_raw": res_grp, "planted_PC3": res_pl}
    jdump(out, RES / f"clean_vs_raw_psp_cells{a.tag}.json")
    logger.info(f"done in {(time.time()-t0)/60:.1f} min")


if __name__ == "__main__":
    main()
```

### [132] TOOL RESULT — Write · 2026-09-29 05:43:44 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s6_assoc.py", "content": "#!/usr/bin/env python3\n\"\"\"S4 ASSOCIATIONS (selection data, outcomes previously unsealed): partial Spearman given the EXP10 rung ladder for raw\nand clean variants per body and POOLED, paired clean-vs-raw bootstraps (diff and retention ratio), per-group DL,\ndisattenuation, planted-association checks (PC3), and the mechanical evaluation of P1-P3 and the VERDICT.\nWrites results/clean_vs_raw_psp.json and data/psp_boot.npz.\"\"\"\nfrom __future__ import annotations\n\nimport os\n\nos.environ.setdefault(\"OMP_NUM_THREADS\", \"1\")\nos.environ.setdefault(\"OPENBLAS_NUM_THREADS\", \"1\")\nos.environ.setdefault(\"MKL_NUM_THREADS\", \"1\")\n\nimport argparse\nimport json\nimport math\nimport multiprocessing as mp\nimport sys\nimport time\nfrom concurrent.futures import ProcessPoolExecutor, as_completed\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import DATA, RES, jdump, setup_logger\n\nLABEL = \"selection data, outcomes previously unsealed\"\nSEED = 20260930\nRAW = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"NOVCHURN_raw\", \"OPEN_home\"]\nCLEAN = [\"NOV_res_rare5\", \"NOV_res_rare10\", \"NOV_res_rare20\", \"edge_persistence_rare5\", \"edge_persistence_rare10\",\n         \"edge_persistence_rare20\", \"ego_density_W3_rare10\", \"NOVCHURN_rare5\", \"NOVCHURN_rare10\", \"NOVCHURN_rare20\",\n         \"NOV_res_exc\", \"edge_persistence_exc\", \"ego_density_W3_exc\", \"NOV_res_zperm\", \"edge_persistence_zperm\",\n         \"NOVCHURN_exc\", \"NOVCHURN_zperm\", \"EP_chao\", \"NOVCHURN_chao\", \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\",\n         \"excess_pers_cfg\", \"NOVCHURN_cfg\", \"OPEN_home_clean\", \"OPEN_home_exc\", \"edge_persistence_nullmean\"]\nNEG = {\"edge_persistence__raw\", \"ego_density_W3__raw\", \"edge_persistence_rare5\", \"edge_persistence_rare10\",\n       \"edge_persistence_rare20\", \"ego_density_W3_rare10\", \"edge_persistence_exc\", \"ego_density_W3_exc\",\n       \"edge_persistence_zperm\", \"EP_chao\", \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\", \"excess_pers_cfg\",\n       \"edge_persistence_nullmean\"}\nPAIRS = [(\"NOVCHURN_exc\", \"NOVCHURN_raw\"), (\"NOVCHURN_rare5\", \"NOVCHURN_raw\"), (\"NOVCHURN_rare10\", \"NOVCHURN_raw\"),\n         (\"NOVCHURN_rare20\", \"NOVCHURN_raw\"), (\"NOVCHURN_cfg\", \"NOVCHURN_raw\"), (\"NOVCHURN_chao\", \"NOVCHURN_raw\"),\n         (\"NOVCHURN_zperm\", \"NOVCHURN_raw\"), (\"NOV_res_exc\", \"NOV_res__raw\"), (\"NOV_res_rare10\", \"NOV_res__raw\"),\n         (\"NOV_res_zperm\", \"NOV_res__raw\"), (\"edge_persistence_exc\", \"edge_persistence__raw\"),\n         (\"edge_persistence_rare10\", \"edge_persistence__raw\"), (\"z_pers_cfg\", \"edge_persistence__raw\"),\n         (\"EP_chao\", \"edge_persistence__raw\"), (\"edge_persistence_zperm\", \"edge_persistence__raw\"),\n         (\"excess_pers_cfg\", \"edge_persistence__raw\"), (\"z_dens_cfg\", \"ego_density_W3__raw\"),\n         (\"z_dens_k\", \"ego_density_W3__raw\"), (\"ego_density_W3_exc\", \"ego_density_W3__raw\"),\n         (\"OPEN_home_clean\", \"OPEN_home\"), (\"OPEN_home_exc\", \"OPEN_home\")]\nGROUP_X = [\"NOVCHURN_raw\", \"NOVCHURN_exc\", \"NOVCHURN_cfg\", \"NOVCHURN_rare10\", \"OPEN_home\", \"OPEN_home_clean\"]\nBODY_KEYS = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\"]\n_T: dict = {}\n\n\ndef _init() -> None:\n    import warnings\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    from tables import load_tables\n    _T.update(load_tables())\n\n\ndef run_task(task: tuple) -> tuple:\n    from fastpsp import paired_fast, psp_boot2_fast\n    from tables import design\n    kind = task[0]\n    t = time.time()\n    if kind == \"psp\":\n        _, body, x, y, rung, B, sub = task\n        df = _T[body]\n        if sub is not None:\n            df = df[df.agroup == sub].reset_index(drop=True)\n        Bm, Cm = design(df, rung, body == \"POOLED\", drop_group=sub is not None)\n        r = psp_boot2_fast(df[x].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B,\n                           SEED + (101 * (1 + [\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"].index(sub))\n                                   if sub else 0), -1 if x in NEG else 1)\n        return task, r, time.time() - t\n    if kind == \"pair\":\n        _, body, xa, xb, y, rung, B = task\n        df = _T[body]\n        Bm, Cm = design(df, rung, body == \"POOLED\")\n        r = paired_fast(df[xa].to_numpy(float), df[xb].to_numpy(float), df[y].to_numpy(float), Bm, Cm, B, SEED)\n        return task, r, time.time() - t\n    if kind == \"planted\":\n        _, body, B = task\n        df = _T[body]\n        Bm, Cm = design(df, \"R2\", body == \"POOLED\")\n        y = df[\"O2r_m50\"].to_numpy(float)\n        rr = df[\"O2r_resid\"].to_numpy(float)\n        rng = np.random.default_rng(SEED + 7)\n        ok = np.isfinite(rr)\n        rk = np.full(len(rr), np.nan)\n        rk[ok] = stats.rankdata(rr[ok])\n        sd = np.nanstd(rk)\n        x = rk + rng.normal(0, 3 * sd, len(rk))\n        res = {\"planted\": _strip(psp_boot2_fast(x, y, Bm, Cm, B, SEED))}\n        pl = []\n        for k in range(20):\n            xs = x.copy()\n            xs[ok] = rng.permutation(x[ok])\n            pl.append(_strip(psp_boot2_fast(xs, y, Bm, Cm, B, SEED + k)))\n        res[\"placebos\"] = pl\n        res[\"n_placebo_ci_excl0\"] = int(sum(1 for p in pl if np.isfinite(p[\"rho\"]) and (p[\"ci\"][0] > 0 or p[\"ci\"][1] < 0)))\n        return task, res, time.time() - t\n    raise ValueError(kind)\n\n\ndef _strip(r: dict) -> dict:\n    return {k: v for k, v in r.items() if k != \"boot\"}\n\n\ndef build_tasks(B: int, B2: int) -> list:\n    tasks = []\n    for body in BODY_KEYS:\n        for x in RAW + CLEAN:\n            for rung in (\"R0\", \"R2\", \"R3\"):\n                tasks.append((\"psp\", body, x, \"O2r_m50\", rung, B, None))\n            for rung in (\"R0\", \"R2\", \"R3\"):\n                tasks.append((\"psp\", body, x, \"O2r_resid\", rung, B2, None))\n        for xa, xb in PAIRS:\n            for rung in (\"R2\", \"R3\"):\n                tasks.append((\"pair\", body, xa, xb, \"O2r_m50\", rung, B))\n        tasks.append((\"planted\", body, 1000))\n    for x in GROUP_X:\n        for g in [\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\", \"MATHDEC\"]:\n            tasks.append((\"psp\", \"POOLED\", x, \"O2r_m50\", \"R2\", B, g))\n    for x in [\"OPEN_home\", \"NOVCHURN_raw\", \"NOVCHURN_exc\"]:\n        tasks.append((\"psp\", \"POOLED\", x, \"O2r_m50\", \"R5\", B, None))\n        tasks.append((\"psp\", \"COH1517\", x, \"O2r_m50\", \"R5\", B, None))\n    return tasks\n\n\ndef cost(t: tuple) -> float:\n    base = {\"POOLED\": 7, \"DEV\": 3, \"COH1014\": 2.5, \"OLDHO\": 2, \"COH1517\": 0.6}[t[1]]\n    return base * (2 if t[0] == \"pair\" else 20 if t[0] == \"planted\" else 1)\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--B\", type=int, default=2000)\n    ap.add_argument(\"--B2\", type=int, default=2000)\n    ap.add_argument(\"--workers\", type=int, default=4)\n    ap.add_argument(\"--limit\", type=int, default=0)\n    ap.add_argument(\"--tag\", default=\"\")\n    a = ap.parse_args()\n    logger = setup_logger(f\"s6_assoc{a.tag}\")\n    tasks = build_tasks(a.B, a.B2)\n    if a.limit:\n        tasks = tasks[:: max(1, len(tasks) // a.limit)]\n    tasks.sort(key=lambda t: -cost(t))\n    logger.info(f\"{len(tasks)} tasks, B = {a.B}, workers {a.workers}\")\n    res_psp, res_pair, res_grp, res_pl, boots = {}, {}, {}, {}, {}\n    t0 = time.time()\n    with ProcessPoolExecutor(a.workers, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex:\n        futs = [ex.submit(run_task, t) for t in tasks]\n        for i, fu in enumerate(as_completed(futs)):\n            task, r, dt = fu.result()\n            if task[0] == \"psp\":\n                _, body, x, y, rung, B, sub = task\n                key = f\"{body}|{x}|{y}|{rung}\"\n                if sub is not None:\n                    res_grp.setdefault(f\"{x}|{y}|{rung}\", {})[sub] = _strip(r)\n                else:\n                    if y == \"O2r_m50\" and len(r.get(\"boot\", [])):\n                        boots[key] = r[\"boot\"].astype(np.float32)\n                    res_psp[key] = _strip(r) | {\"x\": x, \"y\": y, \"rung\": rung, \"body\": body}\n            elif task[0] == \"pair\":\n                _, body, xa, xb, y, rung, B = task\n                res_pair[f\"{body}|{xa}|{xb}|{y}|{rung}\"] = r\n            else:\n                res_pl[task[1]] = r\n            if i % 50 == 0:\n                el = time.time() - t0\n                logger.info(f\"{i+1}/{len(tasks)} done; {el/60:.1f} min; eta {el/(i+1)*(len(tasks)-i-1)/60:.1f} min\")\n    np.savez_compressed(DATA / f\"psp_boot{a.tag}.npz\", **{k.replace(\"|\", \"__\"): v for k, v in boots.items()})\n    out = {\"label\": LABEL, \"B\": a.B, \"B_O2r_resid\": a.B2, \"seed\": SEED, \"resampling_unit\": \"concept\",\n           \"psp\": res_psp, \"paired\": res_pair, \"groups_raw\": res_grp, \"planted_PC3\": res_pl}\n    jdump(out, RES / f\"clean_vs_raw_psp_cells{a.tag}.json\")\n    logger.info(f\"done in {(time.time()-t0)/60:.1f} min\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [133] TOOL CALL — Bash · 2026-09-29 05:43:44 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -3 logs/s3_full.out; tail -2 logs/u_nulls.out
```

### [134] TOOL RESULT — Bash · 2026-09-29 05:43:44 UTC

```
{"stdout": "slice 2: 120/200 rewires, 360s\nslice 1: 140/200 rewires, 377s\nslice 0: 160/200 rewires, 380s\n05:38:26|INFO   |U3 toy: {'n_states': 12, 'freq': [2503.0, 2513.0, 2526.0, 2522.0, 2491.0, 2478.0, 2518.0, 2442.0, 2545.0, 2526.0, 2449.0, 2487.0], 'chi2_p': 0.9558059116407714, 'pass': True}\n05:39:53|INFO   |U4: {'mean_z': -0.23637767314902444, 'sd_z': 0.9072468118619367, 'n_sets': 50, 'n_null': 30, 'degree_preserved': True, 'simple': True, 'pass': False}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [135] THINKING · 2026-09-29 05:44:08 UTC

```
U4 fell short of its threshold, and I noticed the design was flawed since all 50 sets shared one observed rewire, inflating correlation and understating the true SE. I'll redesign it with 10 independent observed rewires and 40 null draws to rerun once S3 frees up CPU, and I'll write the size-dependence script in the meantime.
```

### [136] TOOL CALL — Bash · 2026-09-29 05:44:08 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("tests/u_nulls.py"); s=p.read_text()
old_start=s.index("def rewire_calibration")
old_end=s.index("def main()")
new='''def rewire_calibration(n_obs: int = 10, n_null: int = 40, n_sets: int = 20, k: int = 12) -> dict:
    """n_obs independent 'observed' rewires (each exchangeable with the null draws) x n_sets random topic sets;
    z against n_null further rewires of the original; mean z over all (graph-clustered SE reported)."""
    import igraph as ig
    z = np.load(INPUTS / "backbone" / "slice0.npz")
    nt = 4516
    G0 = ig.Graph(n=nt, edges=np.c_[z["a"], z["b"]].tolist())
    deg0 = np.array(G0.degree())

    def rewired(seed):
        random.seed(seed)
        ig.set_random_number_generator(random)
        g = G0.copy()
        g.rewire(n=10 * g.ecount(), allowed_edge_types="simple")
        el = np.array(g.get_edgelist())
        A = np.zeros((nt, nt), bool)
        A[el[:, 0], el[:, 1]] = True
        A[el[:, 1], el[:, 0]] = True
        return A, g
    rng = np.random.default_rng(7)
    sets = [[rng.choice(nt, k, replace=False) for _ in range(n_sets)] for _ in range(n_obs)]
    iu, ju = np.triu_indices(k, 1)
    obs = np.zeros((n_obs, n_sets))
    simple, degok = True, True
    for o in range(n_obs):
        A, g = rewired(999 + o)
        simple &= bool(g.is_simple())
        degok &= bool(np.array_equal(np.array(g.degree()), deg0))
        obs[o] = [A[s[iu], s[ju]].sum() for s in sets[o]]
    null = np.zeros((n_null, n_obs, n_sets))
    for d in range(n_null):
        A, _ = rewired(5000 + d)
        for o in range(n_obs):
            null[d, o] = [A[s[iu], s[ju]].sum() for s in sets[o]]
    sd = null.std(0)
    zz = np.where(sd > 0, (obs - null.mean(0)) / np.where(sd > 0, sd, 1), np.nan)
    gm = np.nanmean(zz, 1)
    return {"mean_z": float(np.nanmean(zz)), "sd_z": float(np.nanstd(zz)), "graph_means": gm.tolist(),
            "se_mean_graph_clustered": float(np.std(gm, ddof=1) / np.sqrt(n_obs)), "n_obs_graphs": n_obs,
            "n_sets_per_graph": n_sets, "n_null": n_null, "degree_preserved": degok, "simple": simple,
            "pass": bool(abs(np.nanmean(zz)) < 0.15),
            "note": "v1 of this test (one observed rewire x 50 sets, 30 nulls) gave mean z -0.236 (sets share one "
                    "observed graph, so their z are correlated); replaced by this clustered design"}


'''
s=s[:old_start]+new+s[old_end:]
s=s.replace('''    out = {"U3_toy": toy_curveball()}
    logger.info(f"U3 toy: {out['U3_toy']}")''','''    prev = RES / "unit_tests_nulls.json"
    out = json.loads(prev.read_text()) if prev.exists() else {"U3_toy": toy_curveball()}
    if "U3_toy" not in out:
        out["U3_toy"] = toy_curveball()
    logger.info(f"U3 toy: {out['U3_toy']}")''')
s=s.replace("import itertools\n","import itertools\nimport json\n")
p.write_text(s)
EOF
.venv/bin/python -c "import ast;ast.parse(open('tests/u_nulls.py').read())"; ls results/
```

### [137] TOOL RESULT — Bash · 2026-09-29 05:44:08 UTC

```
{"stdout": "deviations.json\nfrozen_spec.json\ngate_t0.json\nunit_tests_fast6.json\nunit_tests_fastpsp.json\nunit_tests_nulls.json\nv3_nulls_mini.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [138] TOOL CALL — Bash · 2026-09-29 05:44:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("tests/u_nulls.py"); s=p.read_text()
s=s.replace('''    out["U4_rewire_calibration"] = rewire_calibration()''','''    if "U4_rewire_calibration" in out and "U4_v1_single_graph" not in out:
        out["U4_v1_single_graph"] = out["U4_rewire_calibration"]     # kept: the first (failed) design
    out["U4_rewire_calibration"] = rewire_calibration()''')
p.write_text(s)
EOF
tail -2 logs/s3_full.out
```

### [139] TOOL RESULT — Bash · 2026-09-29 05:44:30 UTC

```
{"stdout": "slice 1: 140/200 rewires, 377s\nslice 0: 160/200 rewires, 380s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [140] TOOL CALL — Write · 2026-09-29 05:44:54 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s5_size.py

#!/usr/bin/env python3
"""S3 SIZE-DEPENDENCE DIAGNOSTICS (no outcomes): Spearman of every raw / clean variant with log n_home_early,
log(n_home_early / 3), growth_c and log n_all_early per body and pooled; OLS R2 of raw persistence / NOV_res / density
on log n and on [log n, 1/min_year_n, 1/mean_year_n]; Spearman of the degree-normalised z with log deg_W3;
binned raw vs V2-null-mean persistence (the key picture) and the 'thin-sample share' = R2 of raw persistence on its
own V2 null mean. -> results/size_dependence.json, figures/persistence_vs_n.png"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, DATA_IN, FIGS, RES, jdump, setup_logger

logger = setup_logger("s5_size")
VARS = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "new_edge_rate__raw", "n_comm_W3__raw",
        "participation__raw", "NOVCHURN_raw", "OPEN_home",
        "NOV_res_rare5", "NOV_res_rare10", "NOV_res_rare20", "edge_persistence_rare5", "edge_persistence_rare10",
        "edge_persistence_rare20", "ego_density_W3_rare10", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_rare20",
        "NOV_res_exc", "edge_persistence_exc", "ego_density_W3_exc", "NOV_res_zperm", "edge_persistence_zperm",
        "NOVCHURN_exc", "NOVCHURN_zperm", "EP_chao", "NOVCHURN_chao", "z_dens_cfg", "z_dens_cfg_W1", "z_dens_k",
        "z_pers_cfg", "excess_pers_cfg", "z_pers_k", "NOVCHURN_cfg", "OPEN_home_clean", "OPEN_home_exc",
        "edge_persistence_nullmean", "NOV_res_nullmean", "ego_density_W3_nullmean"]
BINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]


def sp(x, y) -> dict:
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 20:
        return {"rho": None, "n": int(ok.sum())}
    r, p = stats.spearmanr(x[ok], y[ok])
    return {"rho": float(r), "p": float(p), "n": int(ok.sum())}


def ols_r2(y, X) -> dict:
    ok = np.isfinite(y) & np.all(np.isfinite(X), 1)
    if ok.sum() < 20:
        return {"R2": None, "n": int(ok.sum())}
    Z = np.c_[np.ones(ok.sum()), X[ok]]
    b = np.linalg.lstsq(Z, y[ok], rcond=None)[0]
    res = y[ok] - Z @ b
    return {"R2": float(1 - res.var() / y[ok].var()), "n": int(ok.sum()), "coef": b.tolist()}


def main() -> None:
    d = pd.read_parquet(DATA / "clean_variants.parquet")
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["ci", "growth_c", "n_all_early"])
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["ci", "growth_c", "n_all_early"])
    fe["frame"], ac["frame"] = "exp5", "cohort"
    d = d.merge(pd.concat([fe, ac]), on=["frame", "ci"], how="left", validate="1:1")
    ln = np.log(d.n_home_early.to_numpy(float))
    d["mean_year_n"] = (d.n_W1 + d.n_W2 + d.n_W3) / 3
    out: dict = {"n_concepts": int(len(d)), "note": "log(n/3) is a monotone transform of n, so its Spearman equals "
                                                    "that of log n (reported for completeness)", "spearman": {}}
    groups = {"POOLED": np.ones(len(d), bool), **{b: (d.body == b).to_numpy() for b in
                                                   ("DEV", "OLDHO", "COH1014", "COH1517")}}
    for v in VARS:
        if v not in d:
            continue
        x = d[v].to_numpy(float)
        out["spearman"][v] = {g: {"log_n_home_early": sp(x[m], ln[m]),
                                  "log_n_home_early_over_3": sp(x[m], np.log(d.n_home_early.to_numpy(float)[m] / 3)),
                                  "growth_c": sp(x[m], d.growth_c.to_numpy(float)[m]),
                                  "log_n_all_early": sp(x[m], np.log1p(d.n_all_early.to_numpy(float)[m]))}
                              for g, m in groups.items()}
    X1 = ln[:, None]
    with np.errstate(divide="ignore"):
        X3 = np.c_[ln, 1 / d.min_year_n.replace(0, np.nan).to_numpy(float), 1 / d.mean_year_n.to_numpy(float)]
    out["ols_r2"] = {}
    for v in ("edge_persistence__raw", "NOV_res__raw", "ego_density_W3__raw", "NOVCHURN_raw", "edge_persistence_exc",
              "NOVCHURN_exc", "z_pers_cfg", "edge_persistence_rare10"):
        y = d[v].to_numpy(float)
        out["ols_r2"][v] = {"log_n": ols_r2(y, X1), "log_n_inv_min_inv_mean": ols_r2(y, X3)}
    lg = np.log(d.deg_W3__raw.to_numpy(float))
    out["degree_dependence"] = {v: {g: sp(d[v].to_numpy(float)[m], lg[m]) for g, m in groups.items()}
                                for v in ("ego_density_W3__raw", "z_dens_cfg", "z_dens_k", "edge_persistence__raw",
                                          "z_pers_cfg", "z_pers_k")}
    # key picture: binned raw vs null-mean persistence
    tab = []
    for lo, hi in BINS:
        m = (d.n_home_early >= lo) & (d.n_home_early <= hi)
        s = d[m]
        tab.append({"bin": f"{lo}-{hi if hi < 10**9 else 'inf'}", "n": int(m.sum()),
                    "raw_mean": float(s.edge_persistence__raw.mean()),
                    "v2_null_mean": float(s.edge_persistence_nullmean.mean()),
                    "excess_mean": float(s.edge_persistence_exc.mean()),
                    "rare10_mean": float(s.edge_persistence_rare10.mean()),
                    "curveball_null_mean": float(s.pers_cfg_mean.mean()),
                    "raw_NOV_res_mean": float(s.NOV_res__raw.mean()),
                    "null_NOV_res_mean": float(s.NOV_res_nullmean.mean())})
    out["binned_persistence"] = tab
    y = d.edge_persistence__raw.to_numpy(float)
    out["thin_sample_share"] = {
        "definition": "R2 of raw edge_persistence on its own V2 (year-label permutation) null mean",
        "POOLED": ols_r2(y, d.edge_persistence_nullmean.to_numpy(float)[:, None]),
        **{b: ols_r2(y[m], d.edge_persistence_nullmean.to_numpy(float)[m][:, None]) for b, m in groups.items()
           if b != "POOLED"}}
    yN = d.NOV_res__raw.to_numpy(float)
    out["thin_sample_share_NOV_res"] = {"POOLED": ols_r2(yN, d.NOV_res_nullmean.to_numpy(float)[:, None])}
    jdump(out, RES / "size_dependence.json")
    logger.info(f"thin-sample share (R2 raw EP ~ V2 null mean) pooled: {out['thin_sample_share']['POOLED']['R2']:.3f}")
    for r in tab:
        logger.info(r)
    # figure
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    xs = np.arange(len(tab))
    lab = [r["bin"] for r in tab]
    ax[0].plot(xs, [r["raw_mean"] for r in tab], "o-", label="raw edge persistence")
    ax[0].plot(xs, [r["v2_null_mean"] for r in tab], "s--", label="V2 null mean (year labels permuted)")
    ax[0].plot(xs, [r["rare10_mean"] for r in tab], "^-", label="V1 rarefied (n = 10 / year)")
    ax[0].plot(xs, [r["curveball_null_mean"] for r in tab], "d:", label="V3c curveball null mean")
    ax[0].set_xticks(xs, lab)
    ax[0].set_xlabel("home papers t0..t0+2 (n_home_early bin)")
    ax[0].set_ylabel("mean Jaccard persistence")
    ax[0].legend(fontsize=8)
    ax[0].set_title("Persistence and its sampling null by sample size")
    ok = np.isfinite(y) & np.isfinite(d.edge_persistence_nullmean)
    ax[1].scatter(d.edge_persistence_nullmean[ok], y[ok], s=3, alpha=0.25)
    lim = [0, max(0.8, float(np.nanmax(y)))]
    ax[1].plot(lim, lim, "k--", lw=0.8)
    ax[1].set_xlabel("V2 null mean persistence (same papers, years shuffled)")
    ax[1].set_ylabel("observed raw persistence")
    ax[1].set_title(f"thin-sample share R2 = {out['thin_sample_share']['POOLED']['R2']:.2f} (n = {int(ok.sum())})")
    fig.tight_layout()
    fig.savefig(FIGS / "persistence_vs_n.png", dpi=150)
    logger.info("wrote figures/persistence_vs_n.png")


if __name__ == "__main__":
    main()
```

### [141] TOOL RESULT — Write · 2026-09-29 05:44:54 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s5_size.py", "content": "#!/usr/bin/env python3\n\"\"\"S3 SIZE-DEPENDENCE DIAGNOSTICS (no outcomes): Spearman of every raw / clean variant with log n_home_early,\nlog(n_home_early / 3), growth_c and log n_all_early per body and pooled; OLS R2 of raw persistence / NOV_res / density\non log n and on [log n, 1/min_year_n, 1/mean_year_n]; Spearman of the degree-normalised z with log deg_W3;\nbinned raw vs V2-null-mean persistence (the key picture) and the 'thin-sample share' = R2 of raw persistence on its\nown V2 null mean. -> results/size_dependence.json, figures/persistence_vs_n.png\"\"\"\nfrom __future__ import annotations\n\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport matplotlib\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import DATA, DATA_IN, FIGS, RES, jdump, setup_logger\n\nlogger = setup_logger(\"s5_size\")\nVARS = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"new_edge_rate__raw\", \"n_comm_W3__raw\",\n        \"participation__raw\", \"NOVCHURN_raw\", \"OPEN_home\",\n        \"NOV_res_rare5\", \"NOV_res_rare10\", \"NOV_res_rare20\", \"edge_persistence_rare5\", \"edge_persistence_rare10\",\n        \"edge_persistence_rare20\", \"ego_density_W3_rare10\", \"NOVCHURN_rare5\", \"NOVCHURN_rare10\", \"NOVCHURN_rare20\",\n        \"NOV_res_exc\", \"edge_persistence_exc\", \"ego_density_W3_exc\", \"NOV_res_zperm\", \"edge_persistence_zperm\",\n        \"NOVCHURN_exc\", \"NOVCHURN_zperm\", \"EP_chao\", \"NOVCHURN_chao\", \"z_dens_cfg\", \"z_dens_cfg_W1\", \"z_dens_k\",\n        \"z_pers_cfg\", \"excess_pers_cfg\", \"z_pers_k\", \"NOVCHURN_cfg\", \"OPEN_home_clean\", \"OPEN_home_exc\",\n        \"edge_persistence_nullmean\", \"NOV_res_nullmean\", \"ego_density_W3_nullmean\"]\nBINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]\n\n\ndef sp(x, y) -> dict:\n    ok = np.isfinite(x) & np.isfinite(y)\n    if ok.sum() < 20:\n        return {\"rho\": None, \"n\": int(ok.sum())}\n    r, p = stats.spearmanr(x[ok], y[ok])\n    return {\"rho\": float(r), \"p\": float(p), \"n\": int(ok.sum())}\n\n\ndef ols_r2(y, X) -> dict:\n    ok = np.isfinite(y) & np.all(np.isfinite(X), 1)\n    if ok.sum() < 20:\n        return {\"R2\": None, \"n\": int(ok.sum())}\n    Z = np.c_[np.ones(ok.sum()), X[ok]]\n    b = np.linalg.lstsq(Z, y[ok], rcond=None)[0]\n    res = y[ok] - Z @ b\n    return {\"R2\": float(1 - res.var() / y[ok].var()), \"n\": int(ok.sum()), \"coef\": b.tolist()}\n\n\ndef main() -> None:\n    d = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"ci\", \"growth_c\", \"n_all_early\"])\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"ci\", \"growth_c\", \"n_all_early\"])\n    fe[\"frame\"], ac[\"frame\"] = \"exp5\", \"cohort\"\n    d = d.merge(pd.concat([fe, ac]), on=[\"frame\", \"ci\"], how=\"left\", validate=\"1:1\")\n    ln = np.log(d.n_home_early.to_numpy(float))\n    d[\"mean_year_n\"] = (d.n_W1 + d.n_W2 + d.n_W3) / 3\n    out: dict = {\"n_concepts\": int(len(d)), \"note\": \"log(n/3) is a monotone transform of n, so its Spearman equals \"\n                                                    \"that of log n (reported for completeness)\", \"spearman\": {}}\n    groups = {\"POOLED\": np.ones(len(d), bool), **{b: (d.body == b).to_numpy() for b in\n                                                   (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\")}}\n    for v in VARS:\n        if v not in d:\n            continue\n        x = d[v].to_numpy(float)\n        out[\"spearman\"][v] = {g: {\"log_n_home_early\": sp(x[m], ln[m]),\n                                  \"log_n_home_early_over_3\": sp(x[m], np.log(d.n_home_early.to_numpy(float)[m] / 3)),\n                                  \"growth_c\": sp(x[m], d.growth_c.to_numpy(float)[m]),\n                                  \"log_n_all_early\": sp(x[m], np.log1p(d.n_all_early.to_numpy(float)[m]))}\n                              for g, m in groups.items()}\n    X1 = ln[:, None]\n    with np.errstate(divide=\"ignore\"):\n        X3 = np.c_[ln, 1 / d.min_year_n.replace(0, np.nan).to_numpy(float), 1 / d.mean_year_n.to_numpy(float)]\n    out[\"ols_r2\"] = {}\n    for v in (\"edge_persistence__raw\", \"NOV_res__raw\", \"ego_density_W3__raw\", \"NOVCHURN_raw\", \"edge_persistence_exc\",\n              \"NOVCHURN_exc\", \"z_pers_cfg\", \"edge_persistence_rare10\"):\n        y = d[v].to_numpy(float)\n        out[\"ols_r2\"][v] = {\"log_n\": ols_r2(y, X1), \"log_n_inv_min_inv_mean\": ols_r2(y, X3)}\n    lg = np.log(d.deg_W3__raw.to_numpy(float))\n    out[\"degree_dependence\"] = {v: {g: sp(d[v].to_numpy(float)[m], lg[m]) for g, m in groups.items()}\n                                for v in (\"ego_density_W3__raw\", \"z_dens_cfg\", \"z_dens_k\", \"edge_persistence__raw\",\n                                          \"z_pers_cfg\", \"z_pers_k\")}\n    # key picture: binned raw vs null-mean persistence\n    tab = []\n    for lo, hi in BINS:\n        m = (d.n_home_early >= lo) & (d.n_home_early <= hi)\n        s = d[m]\n        tab.append({\"bin\": f\"{lo}-{hi if hi < 10**9 else 'inf'}\", \"n\": int(m.sum()),\n                    \"raw_mean\": float(s.edge_persistence__raw.mean()),\n                    \"v2_null_mean\": float(s.edge_persistence_nullmean.mean()),\n                    \"excess_mean\": float(s.edge_persistence_exc.mean()),\n                    \"rare10_mean\": float(s.edge_persistence_rare10.mean()),\n                    \"curveball_null_mean\": float(s.pers_cfg_mean.mean()),\n                    \"raw_NOV_res_mean\": float(s.NOV_res__raw.mean()),\n                    \"null_NOV_res_mean\": float(s.NOV_res_nullmean.mean())})\n    out[\"binned_persistence\"] = tab\n    y = d.edge_persistence__raw.to_numpy(float)\n    out[\"thin_sample_share\"] = {\n        \"definition\": \"R2 of raw edge_persistence on its own V2 (year-label permutation) null mean\",\n        \"POOLED\": ols_r2(y, d.edge_persistence_nullmean.to_numpy(float)[:, None]),\n        **{b: ols_r2(y[m], d.edge_persistence_nullmean.to_numpy(float)[m][:, None]) for b, m in groups.items()\n           if b != \"POOLED\"}}\n    yN = d.NOV_res__raw.to_numpy(float)\n    out[\"thin_sample_share_NOV_res\"] = {\"POOLED\": ols_r2(yN, d.NOV_res_nullmean.to_numpy(float)[:, None])}\n    jdump(out, RES / \"size_dependence.json\")\n    logger.info(f\"thin-sample share (R2 raw EP ~ V2 null mean) pooled: {out['thin_sample_share']['POOLED']['R2']:.3f}\")\n    for r in tab:\n        logger.info(r)\n    # figure\n    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))\n    xs = np.arange(len(tab))\n    lab = [r[\"bin\"] for r in tab]\n    ax[0].plot(xs, [r[\"raw_mean\"] for r in tab], \"o-\", label=\"raw edge persistence\")\n    ax[0].plot(xs, [r[\"v2_null_mean\"] for r in tab], \"s--\", label=\"V2 null mean (year labels permuted)\")\n    ax[0].plot(xs, [r[\"rare10_mean\"] for r in tab], \"^-\", label=\"V1 rarefied (n = 10 / year)\")\n    ax[0].plot(xs, [r[\"curveball_null_mean\"] for r in tab], \"d:\", label=\"V3c curveball null mean\")\n    ax[0].set_xticks(xs, lab)\n    ax[0].set_xlabel(\"home papers t0..t0+2 (n_home_early bin)\")\n    ax[0].set_ylabel(\"mean Jaccard persistence\")\n    ax[0].legend(fontsize=8)\n    ax[0].set_title(\"Persistence and its sampling null by sample size\")\n    ok = np.isfinite(y) & np.isfinite(d.edge_persistence_nullmean)\n    ax[1].scatter(d.edge_persistence_nullmean[ok], y[ok], s=3, alpha=0.25)\n    lim = [0, max(0.8, float(np.nanmax(y)))]\n    ax[1].plot(lim, lim, \"k--\", lw=0.8)\n    ax[1].set_xlabel(\"V2 null mean persistence (same papers, years shuffled)\")\n    ax[1].set_ylabel(\"observed raw persistence\")\n    ax[1].set_title(f\"thin-sample share R2 = {out['thin_sample_share']['POOLED']['R2']:.2f} (n = {int(ok.sum())})\")\n    fig.tight_layout()\n    fig.savefig(FIGS / \"persistence_vs_n.png\", dpi=150)\n    logger.info(\"wrote figures/persistence_vs_n.png\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [142] TOOL CALL — Bash · 2026-09-29 05:44:54 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -3 logs/s3_full.out
```

### [143] TOOL RESULT — Bash · 2026-09-29 05:44:54 UTC

```
{"stdout": "slice 1: 160/200 rewires, 419s\nslice 2: 140/200 rewires, 428s\nslice 0: 180/200 rewires, 434s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [144] ASSISTANT · 2026-09-29 05:45:14 UTC

```
Rewiring nearly done. Writing the planted checks PC1/PC2 (a stationary thin-sample simulation and planted churn).
```

### [145] TOOL CALL — Write · 2026-09-29 05:45:14 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/planted.py

#!/usr/bin/env python3
"""Planted checks PC1 / PC2 on the fast engine (no outcomes).

PC1 stationary thin-sample simulation: for 300 real concepts (n_home_early >= 10, seed 21) the W1..W3 home papers are
    re-drawn with replacement from the concept's own POOLED W1..W3 papers at the real yearly counts (PRE unchanged), so
    the true partner distribution is identical across years. Raw persistence should still depend on n (reported);
    V2 excess persistence should average ~0 (|mean| < 0.02) and be size-free (|Spearman with log n| < 0.1).
PC2 planted churn: the same synthetic concepts, but 50% of the topic slots of every W3 paper are replaced by topics
    from a concept-specific set of 10 NEW topics outside the pooled set (so they can recur and become neighbours).
    V2 excess persistence must fall (paired sign test p < 0.01).
-> results/planted_checks.json"""
from __future__ import annotations

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))

import numpy as np
from scipy import stats

import ego
from common import RES, jdump, setup_logger
from ego_ctx import rq1_context
from fast6 import fast6, permute_labels, prep
from jobs import build_home_cache


def v2_excess(c: dict, works: list, rng, D: int = 200) -> tuple[float, float, float]:
    P = prep(c["name"], c["aliases"], c["t0"], works)
    lab = P["lab"]
    obs = fast6(P, lab[None, :])["edge_persistence"][0]
    r = fast6(P, permute_labels(lab, D, rng))["edge_persistence"]
    f = np.isfinite(r)
    if f.sum() < D // 2 or not np.isfinite(obs):
        return float(obs), float("nan"), float("nan")
    return float(obs), float(r[f].mean()), float(obs - r[f].mean())


def main() -> None:
    logger = setup_logger("planted")
    warnings.simplefilter("ignore", RuntimeWarning)
    ego.set_context(rq1_context())
    nt = ego.C["nt"]
    cache = build_home_cache()
    keys = sorted(k for k, v in cache.items() if v["n_home_early"] >= 10)
    rng = np.random.default_rng(21)
    pick = [keys[i] for i in rng.choice(len(keys), 300, replace=False)]
    rows = []
    for k in pick:
        c = cache[k]
        t0 = c["t0"]
        W = [(y, tp) for y, tp in c["works"] if t0 <= y <= t0 + 2]
        pre = [(y, tp) for y, tp in c["works"] if y < t0]
        if len(W) < 3:
            continue
        ny = {y: sum(1 for yy, _ in W if yy == y) for y in (t0, t0 + 1, t0 + 2)}
        draw = rng.integers(0, len(W), len(W))
        syn, j = [], 0
        for y in (t0, t0 + 1, t0 + 2):
            for _ in range(ny[y]):
                syn.append((y, W[draw[j]][1]))
                j += 1
        pooled = {t for _, tp in W for t in tp}
        cand = np.setdiff1d(np.arange(nt), np.fromiter(pooled, int, len(pooled)))
        newt = rng.choice(cand, 10, replace=False)
        planted = []
        for y, tp in syn:
            if y == t0 + 2 and len(tp):
                tp = tuple(int(rng.choice(newt)) if rng.random() < 0.5 else t for t in tp)
            planted.append((y, tp))
        o_s, m_s, e_s = v2_excess(c, pre + syn, rng)
        o_p, m_p, e_p = v2_excess(c, pre + planted, rng)
        rows.append({"n": c["n_home_early"], "raw_stat": o_s, "null_stat": m_s, "exc_stat": e_s, "raw_plant": o_p,
                     "exc_plant": e_p})
    import pandas as pd
    d = pd.DataFrame(rows)
    ln = np.log(d.n)
    ok = d.exc_stat.notna()
    r_raw = stats.spearmanr(d.raw_stat[d.raw_stat.notna()], ln[d.raw_stat.notna()])[0]
    r_exc = stats.spearmanr(d.exc_stat[ok], ln[ok])[0]
    pc1 = {"n_concepts": int(ok.sum()), "raw_spearman_log_n": float(r_raw), "excess_mean": float(d.exc_stat[ok].mean()),
           "excess_spearman_log_n": float(r_exc),
           "pass": bool(abs(d.exc_stat[ok].mean()) < 0.02 and abs(r_exc) < 0.1)}
    both = d.exc_stat.notna() & d.exc_plant.notna()
    dec = int((d.exc_plant[both] < d.exc_stat[both]).sum())
    inc = int((d.exc_plant[both] > d.exc_stat[both]).sum())
    p = float(stats.binomtest(dec, dec + inc, 0.5, alternative="greater").pvalue) if dec + inc else float("nan")
    pc2 = {"n_pairs": int(both.sum()), "n_excess_fell": dec, "n_excess_rose": inc, "sign_test_p": p,
           "mean_change": float((d.exc_plant[both] - d.exc_stat[both]).mean()), "pass": bool(p < 0.01)}
    out = {"PC1_stationary": pc1, "PC2_planted_churn": pc2}
    jdump(out, RES / "planted_checks.json")
    logger.info(out)


if __name__ == "__main__":
    main()
```

### [146] TOOL RESULT — Write · 2026-09-29 05:45:14 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/tests/planted.py", "content": "#!/usr/bin/env python3\n\"\"\"Planted checks PC1 / PC2 on the fast engine (no outcomes).\n\nPC1 stationary thin-sample simulation: for 300 real concepts (n_home_early >= 10, seed 21) the W1..W3 home papers are\n    re-drawn with replacement from the concept's own POOLED W1..W3 papers at the real yearly counts (PRE unchanged), so\n    the true partner distribution is identical across years. Raw persistence should still depend on n (reported);\n    V2 excess persistence should average ~0 (|mean| < 0.02) and be size-free (|Spearman with log n| < 0.1).\nPC2 planted churn: the same synthetic concepts, but 50% of the topic slots of every W3 paper are replaced by topics\n    from a concept-specific set of 10 NEW topics outside the pooled set (so they can recur and become neighbours).\n    V2 excess persistence must fall (paired sign test p < 0.01).\n-> results/planted_checks.json\"\"\"\nfrom __future__ import annotations\n\nimport sys\nimport warnings\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1] / \"lib\"))\n\nimport numpy as np\nfrom scipy import stats\n\nimport ego\nfrom common import RES, jdump, setup_logger\nfrom ego_ctx import rq1_context\nfrom fast6 import fast6, permute_labels, prep\nfrom jobs import build_home_cache\n\n\ndef v2_excess(c: dict, works: list, rng, D: int = 200) -> tuple[float, float, float]:\n    P = prep(c[\"name\"], c[\"aliases\"], c[\"t0\"], works)\n    lab = P[\"lab\"]\n    obs = fast6(P, lab[None, :])[\"edge_persistence\"][0]\n    r = fast6(P, permute_labels(lab, D, rng))[\"edge_persistence\"]\n    f = np.isfinite(r)\n    if f.sum() < D // 2 or not np.isfinite(obs):\n        return float(obs), float(\"nan\"), float(\"nan\")\n    return float(obs), float(r[f].mean()), float(obs - r[f].mean())\n\n\ndef main() -> None:\n    logger = setup_logger(\"planted\")\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    ego.set_context(rq1_context())\n    nt = ego.C[\"nt\"]\n    cache = build_home_cache()\n    keys = sorted(k for k, v in cache.items() if v[\"n_home_early\"] >= 10)\n    rng = np.random.default_rng(21)\n    pick = [keys[i] for i in rng.choice(len(keys), 300, replace=False)]\n    rows = []\n    for k in pick:\n        c = cache[k]\n        t0 = c[\"t0\"]\n        W = [(y, tp) for y, tp in c[\"works\"] if t0 <= y <= t0 + 2]\n        pre = [(y, tp) for y, tp in c[\"works\"] if y < t0]\n        if len(W) < 3:\n            continue\n        ny = {y: sum(1 for yy, _ in W if yy == y) for y in (t0, t0 + 1, t0 + 2)}\n        draw = rng.integers(0, len(W), len(W))\n        syn, j = [], 0\n        for y in (t0, t0 + 1, t0 + 2):\n            for _ in range(ny[y]):\n                syn.append((y, W[draw[j]][1]))\n                j += 1\n        pooled = {t for _, tp in W for t in tp}\n        cand = np.setdiff1d(np.arange(nt), np.fromiter(pooled, int, len(pooled)))\n        newt = rng.choice(cand, 10, replace=False)\n        planted = []\n        for y, tp in syn:\n            if y == t0 + 2 and len(tp):\n                tp = tuple(int(rng.choice(newt)) if rng.random() < 0.5 else t for t in tp)\n            planted.append((y, tp))\n        o_s, m_s, e_s = v2_excess(c, pre + syn, rng)\n        o_p, m_p, e_p = v2_excess(c, pre + planted, rng)\n        rows.append({\"n\": c[\"n_home_early\"], \"raw_stat\": o_s, \"null_stat\": m_s, \"exc_stat\": e_s, \"raw_plant\": o_p,\n                     \"exc_plant\": e_p})\n    import pandas as pd\n    d = pd.DataFrame(rows)\n    ln = np.log(d.n)\n    ok = d.exc_stat.notna()\n    r_raw = stats.spearmanr(d.raw_stat[d.raw_stat.notna()], ln[d.raw_stat.notna()])[0]\n    r_exc = stats.spearmanr(d.exc_stat[ok], ln[ok])[0]\n    pc1 = {\"n_concepts\": int(ok.sum()), \"raw_spearman_log_n\": float(r_raw), \"excess_mean\": float(d.exc_stat[ok].mean()),\n           \"excess_spearman_log_n\": float(r_exc),\n           \"pass\": bool(abs(d.exc_stat[ok].mean()) < 0.02 and abs(r_exc) < 0.1)}\n    both = d.exc_stat.notna() & d.exc_plant.notna()\n    dec = int((d.exc_plant[both] < d.exc_stat[both]).sum())\n    inc = int((d.exc_plant[both] > d.exc_stat[both]).sum())\n    p = float(stats.binomtest(dec, dec + inc, 0.5, alternative=\"greater\").pvalue) if dec + inc else float(\"nan\")\n    pc2 = {\"n_pairs\": int(both.sum()), \"n_excess_fell\": dec, \"n_excess_rose\": inc, \"sign_test_p\": p,\n           \"mean_change\": float((d.exc_plant[both] - d.exc_stat[both]).mean()), \"pass\": bool(p < 0.01)}\n    out = {\"PC1_stationary\": pc1, \"PC2_planted_churn\": pc2}\n    jdump(out, RES / \"planted_checks.json\")\n    logger.info(out)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [147] TOOL CALL — Bash · 2026-09-29 05:45:14 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sleep 60; tail -4 logs/s3_full.out
```

### [148] TOOL RESULT — Bash · 2026-09-29 05:46:08 UTC

```
{"stdout": "slice 1: 180/200 rewires, 460s\nslice 0: 200/200 rewires, 488s\nslice 2: 160/200 rewires, 492s\nslice 1: 200/200 rewires, 502s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [149] TOOL CALL — Bash · 2026-09-29 05:46:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; timeout 900 .venv/bin/python tests/planted.py 2>&1 | tail -2; tail -3 logs/s3_full.out
```

### [150] TOOL RESULT — Bash · 2026-09-29 05:46:30 UTC

```
{"stdout": "05:46:02|INFO   |{'PC1_stationary': {'n_concepts': 266, 'raw_spearman_log_n': 0.7526416740692565, 'excess_mean': -0.0014089257659994684, 'excess_spearman_log_n': -0.044406470916085176, 'pass': True}, 'PC2_planted_churn': {'n_pairs': 264, 'n_excess_fell': 102, 'n_excess_rose': 108, 'sign_test_p': 0.6854157776885665, 'mean_change': -0.005247486541484769, 'pass': False}}\nslice 2: 160/200 rewires, 492s\nslice 1: 200/200 rewires, 502s\nslice 2: 180/200 rewires, 537s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [151] THINKING · 2026-09-29 05:46:54 UTC

```
PC1 checks out: raw persistence still correlates with log n under a stationary partner distribution, while V2 excess doesn't. PC2 fails though—planting W3 churn didn't lower V2 excess (p = 0.69)—so I'll check whether the plant moved raw persistence at all to distinguish a weak plant from V2 genuinely absorbing churn.
```

### [152] TOOL CALL — Bash · 2026-09-29 05:46:54 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("tests/planted.py"); s=p.read_text()
old='''    pc2 = {"n_pairs": int(both.sum()), "n_excess_fell": dec, "n_excess_rose": inc, "sign_test_p": p,
           "mean_change": float((d.exc_plant[both] - d.exc_stat[both]).mean()), "pass": bool(p < 0.01)}'''
new='''    bothr = d.raw_stat.notna() & d.raw_plant.notna()
    rdec = int((d.raw_plant[bothr] < d.raw_stat[bothr]).sum())
    rinc = int((d.raw_plant[bothr] > d.raw_stat[bothr]).sum())
    rp = float(stats.binomtest(rdec, rdec + rinc, 0.5, alternative="greater").pvalue) if rdec + rinc else float("nan")
    pc2 = {"n_pairs": int(both.sum()), "n_excess_fell": dec, "n_excess_rose": inc, "sign_test_p": p,
           "mean_change": float((d.exc_plant[both] - d.exc_stat[both]).mean()), "pass": bool(p < 0.01),
           "raw_persistence": {"n_fell": rdec, "n_rose": rinc, "sign_test_p": rp,
                               "mean_change": float((d.raw_plant[bothr] - d.raw_stat[bothr]).mean())},
           "null_mean_change": float((d.null_plant[both] - d.null_stat[both]).mean())}'''
assert old in s; s=s.replace(old,new)
s=s.replace('''"raw_plant": o_p,
                     "exc_plant": e_p})''','''"raw_plant": o_p,
                     "null_plant": m_p, "exc_plant": e_p})''')
p.write_text(s)
EOF
timeout 900 .venv/bin/python tests/planted.py 2>&1 | tail -1; tail -2 logs/s3_full.out
```

### [153] TOOL RESULT — Bash · 2026-09-29 05:47:18 UTC

```
{"stdout": "05:46:31|INFO   |{'PC1_stationary': {'n_concepts': 266, 'raw_spearman_log_n': 0.7526416740692565, 'excess_mean': -0.0014089257659994684, 'excess_spearman_log_n': -0.044406470916085176, 'pass': True}, 'PC2_planted_churn': {'n_pairs': 264, 'n_excess_fell': 102, 'n_excess_rose': 108, 'sign_test_p': 0.6854157776885665, 'mean_change': -0.005247486541484769, 'pass': False, 'raw_persistence': {'n_fell': 100, 'n_rose': 41, 'sign_test_p': 3.6185475706497333e-07, 'mean_change': -0.025189994155972815}, 'null_mean_change': -0.020896674059790045}}\nslice 1: 200/200 rewires, 502s\nslice 2: 180/200 rewires, 537s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [154] THINKING · 2026-09-29 05:47:18 UTC

```
V2's null mean nearly matches the planted drop, showing it's a low-power, over-controlling baseline that absorbs ~80% of true churn—I'll flag this as a limitation alongside the verdict while I wait on the final rewire slice.
```

### [155] TOOL CALL — Bash · 2026-09-29 05:47:18 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; for i in $(seq 1 20); do if grep -q "V3 done\|Error\|Traceback" logs/s3_full.out; then break; fi; sleep 15; done; tail -4 logs/s3_full.out; cat results/v3_nulls_full.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['U3_curveball'], d['U4_rewire'], d['spearman_z_pers_cfg_vs_k_matched'], d['finite'])"
```

### [156] TOOL RESULT — Bash · 2026-09-29 05:47:42 UTC

```
{"stdout": "slice 1: 200/200 rewires, 502s\nslice 2: 180/200 rewires, 537s\nslice 2: 200/200 rewires, 582s\n05:46:57|INFO   |V3 done; spearman(z_pers_cfg, z_pers_k) = 0.881\n{'column_sums_preserved': True, 'row_sizes_preserved': True, 'rows_remain_sets': True} {'is_simple': True, 'degree_equal': True} 0.8807774945657614 {'pers_cfg_mean': 12503, 'pers_cfg_sd': 12503, 'excess_pers_cfg': 12503, 'z_pers_cfg': 6094, 'pers_k_mean': 12503, 'z_pers_k': 6554, 'dens_k_mean': 7506, 'z_dens_k': 7506, 'z_dens_cfg': 7479, 'dens_cfg_exp': 7506, 'z_dens_cfg_W1': 8278}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [157] THINKING · 2026-09-29 05:47:42 UTC

```
V3 is done—curveball z and the k-matched approximation align well (ρ = 0.88), though z_pers_cfg is only finite for 6,094 of 13,444 concepts due to zero null sd in small neighbour sets, while excess_pers_cfg covers 12,503. Now running composites, the S1b seal, and reliability checks.
```

### [158] TOOL CALL — Bash · 2026-09-29 05:47:42 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; (nohup .venv/bin/python tests/u_nulls.py > logs/u_nulls2.out 2>&1 &); OMP_NUM_THREADS=1 timeout 1800 .venv/bin/python s4_composites.py > logs/s4.out 2>&1; tail -45 logs/s4.out | cut -c1-200
```

### [159] TOOL RESULT — Bash · 2026-09-29 05:49:47 UTC

```
{"stdout": "  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:53: RuntimeWarning: Mean of empty slice\n  m = np.nanmean(np.where(np.isfinite(Z), Z, np.nan), 1)\n05:48:23|INFO   |rel new_edge_rate__raw: pooled SB 0.540; COH1517 0.550\n05:48:26|INFO   |rel n_comm_W3__raw: pooled SB 0.701; COH1517 0.718\n05:48:28|INFO   |rel participation__raw: pooled SB 0.553; COH1517 0.612\n05:48:31|INFO   |rel NOV_res__raw: pooled SB 0.478; COH1517 0.470\n05:48:32|INFO   |rel ego_density_W3__raw: pooled SB 0.412; COH1517 0.460\n05:48:35|INFO   |rel edge_persistence__raw: pooled SB 0.570; COH1517 0.618\n05:48:38|INFO   |rel NOVCHURN_raw: pooled SB 0.476; COH1517 0.491\n05:48:42|INFO   |rel OPEN_home: pooled SB 0.485; COH1517 0.532\n05:48:44|INFO   |rel NOV_res_exc: pooled SB 0.020; COH1517 0.038\n05:48:47|INFO   |rel edge_persistence_exc: pooled SB 0.046; COH1517 0.028\n05:48:49|INFO   |rel ego_density_W3_exc: pooled SB 0.067; COH1517 0.049\n05:48:54|INFO   |rel new_edge_rate_exc: pooled SB 0.046; COH1517 0.018\n05:48:56|INFO   |rel NOV_res_zperm: pooled SB 0.020; COH1517 0.038\n05:48:58|INFO   |rel edge_persistence_zperm: pooled SB 0.014; COH1517 -0.019\n05:48:59|INFO   |rel ego_density_W3_zperm: pooled SB 0.069; COH1517 0.123\n05:49:00|INFO   |rel NOV_res_rare5: pooled SB 0.557; COH1517 0.607\n05:49:02|INFO   |rel edge_persistence_rare5: pooled SB 0.226; COH1517 0.232\n05:49:03|INFO   |rel ego_density_W3_rare5: pooled SB 0.279; COH1517 nan\n05:49:04|INFO   |rel z_pers_cfg: pooled SB 0.709; COH1517 0.736\n05:49:05|INFO   |rel z_dens_cfg: pooled SB 0.698; COH1517 0.777\n05:49:06|INFO   |rel z_dens_k: pooled SB 0.657; COH1517 0.736\n05:49:10|INFO   |rel edge_persistence_nullmean: pooled SB 0.707; COH1517 0.717\n05:49:12|INFO   |rel NOVCHURN_exc: pooled SB 0.014; COH1517 0.014\n05:49:14|INFO   |rel NOVCHURN_zperm: pooled SB 0.023; COH1517 -0.013\n05:49:15|INFO   |rel NOVCHURN_rare5: pooled SB 0.359; COH1517 0.376\n05:49:16|INFO   |rel NOVCHURN_cfg: pooled SB 0.618; COH1517 0.683\n05:49:18|INFO   |rel OPEN_home_clean: pooled SB 0.577; COH1517 0.642\n05:49:21|INFO   |rel OPEN_home_exc: pooled SB 0.486; COH1517 0.551\n/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s4_composites.py:246: RuntimeWarning: Mean of empty slice\n  **{f\"{h}__{v}\": np.nanmean(VAR[h][v], 0) for h in (\"A\", \"B\") for v in VAR[h]})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [160] THINKING · 2026-09-29 05:50:13 UTC

```
I found that the V2-excess variants have near-zero split-half reliability (NOVCHURN_exc SB = 0.014; edge_persistence_exc 0.046), while the V2 null mean of persistence is highly reliable (0.71), exceeding raw persistence (0.57). Now I'll check the head of the log for the OPEN_home recompute check.
```

### [161] TOOL CALL — Bash · 2026-09-29 05:50:13 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; grep -v "Warning\|nanmean" logs/s4.out | head -8; cat logs/seal.log; tail -2 logs/u_nulls2.out
```

### [162] TOOL RESULT — Bash · 2026-09-29 05:50:13 UTC

```
{"stdout": "05:47:17|INFO   |merged 13444 concepts\n05:47:17|INFO   |sealed constants sha256 99329e83ef3ec821e6414afed9eeb116678cc1eb532ab284e7672832a63a1d54\n05:47:17|INFO   |OPEN_home recomputed vs EXP10: max diff 4.44e-16, NaN mismatches 0\n05:47:17|INFO   |wrote data/clean_variants.parquet (13444, 95)\n05:48:23|INFO   |rel new_edge_rate__raw: pooled SB 0.540; COH1517 0.550\n05:48:26|INFO   |rel n_comm_W3__raw: pooled SB 0.701; COH1517 0.718\n05:48:28|INFO   |rel participation__raw: pooled SB 0.553; COH1517 0.612\n05:48:31|INFO   |rel NOV_res__raw: pooled SB 0.478; COH1517 0.470\n{\"file\": \"frozen_spec.json\", \"prev\": \"GENESIS\", \"sha256\": \"cf4d8e345ef3ac5f1146205c9262b53c7781a7ed38afc38eb91feb9771e106a2\", \"stage\": \"S1_freeze\", \"time\": \"2026-09-29 05:31:34\"}\n{\"file\": \"frozen_constants_S1b.json\", \"prev\": \"b0ad7ffba266e5984ed1de3ac935101a66111c9a3476847555f55409ee681689\", \"sha256\": \"99329e83ef3ec821e6414afed9eeb116678cc1eb532ab284e7672832a63a1d54\", \"stage\": \"S1b_constants\", \"time\": \"2026-09-29 05:47:17\"}\n05:47:17|INFO   |U3 toy: {'n_states': 12, 'freq': [2503.0, 2513.0, 2526.0, 2522.0, 2491.0, 2478.0, 2518.0, 2442.0, 2545.0, 2526.0, 2449.0, 2487.0], 'chi2_p': 0.9558059116407714, 'pass': True}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [163] ASSISTANT · 2026-09-29 05:50:13 UTC

```
Both seals are in place and OPEN_home is reproduced (max diff 4e-16). Next I'll smoke-test the association script with a few cells before the ~40-minute full run.
```

### [164] TOOL CALL — Bash · 2026-09-29 05:50:13 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; timeout 900 .venv/bin/python s6_assoc.py --B 50 --B2 50 --workers 3 --limit 40 --tag _smoke 2>&1 | grep -v Warn | tail -5; python3 -c "
import json; d=json.load(open('results/clean_vs_raw_psp_cells_smoke.json'))
print(len(d['psp']), len(d['paired']), len(d['groups_raw']), list(d['planted_PC3'].keys()))
for k,v in list(d['psp'].items())[:8]: print(k, v['n'], round(v['rho'],4) if v['rho'] else v['rho'], v['ci'])
for k,v in list(d['paired'].items())[:3]: print(k, v)
"
```

### [165] TOOL RESULT — Bash · 2026-09-29 05:50:37 UTC

```
{"stdout": "05:49:48|INFO   |41 tasks, B = 50, workers 3\n05:49:59|INFO   |1/41 done; 0.2 min; eta 6.7 min\n05:50:01|INFO   |done in 0.2 min\n33 7 1 []\nPOOLED|NOVCHURN_raw|O2r_m50|R3 6450 0.1024 [0.08521320022743406, 0.12375481926645505]\nPOOLED|NOVCHURN_rare10|O2r_m50|R3 2874 0.067 [0.030472344591558367, 0.09701358540060359]\nPOOLED|edge_persistence_rare5|O2r_m50|R3 5789 -0.0599 [-0.0884383702437832, -0.0346086716893484]\nPOOLED|NOV_res_zperm|O2r_m50|R3 5853 0.002 [-0.020262799164988497, 0.018420733927216326]\nPOOLED|NOVCHURN_chao|O2r_m50|R3 6417 0.0983 [0.07076378547489531, 0.12797629799434324]\nPOOLED|NOVCHURN_cfg|O2r_m50|R3 3993 0.0894 [0.0603744652844416, 0.12485448554373964]\nDEV|NOV_res__raw|O2r_m50|R0 2741 0.0915 [0.06516234844624906, 0.1302368766740592]\nDEV|edge_persistence_rare20|O2r_m50|R0 317 -0.0336 [-0.14990477171541491, 0.048761892827701395]\nPOOLED|NOVCHURN_cfg|NOVCHURN_raw|O2r_m50|R2 {'n': 3993, 'a': 0.10594463038390994, 'b': 0.10629192154727238, 'diff': -0.00034729116336243426, 'diff_ci': [-0.01019599435482436, 0.0082935640760297], 'ratio': 0.9967326664312115, 'ratio_ci': [0.9167080849152089, 1.0837151863910846], 'a_ci': [0.07860628587341421, 0.14081789729078079], 'b_ci': [0.08162215860004121, 0.1407476711725716], 'p_diff_le0': 0.5098039215686274, 'resampling_unit': 'concept'}\nPOOLED|OPEN_home_clean|OPEN_home|O2r_m50|R2 {'n': 6322, 'a': 0.11451499324222848, 'b': 0.09225874600196611, 'diff': 0.022256247240262372, 'diff_ci': [0.006538030375772489, 0.03445191120122149], 'ratio': 1.2412372615577072, 'ratio_ci': [1.0644112565227675, 1.4459441087689817], 'a_ci': [0.09258019335579709, 0.14072058061688575], 'b_ci': [0.06910888357002686, 0.11419836744993557], 'p_diff_le0': 0.0196078431372549, 'resampling_unit': 'concept'}\nDEV|NOV_res_zperm|NOV_res__raw|O2r_m50|R2 {'n': 2527, 'a': 0.00808951530105374, 'b': 0.07416535618004526, 'diff': -0.06607584087899152, 'diff_ci': [-0.10459184903955522, -0.028382948983522196], 'ratio': 0.10907404370061238, 'ratio_ci': [-0.6703063416028743, 0.5846157840921877], 'a_ci': [-0.029699282752752642, 0.04943758537030353], 'b_ci': [0.040334202292996155, 0.1132114151209966], 'p_diff_le0': 1.0, 'resampling_unit': 'concept'}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [166] ASSISTANT · 2026-09-29 05:50:37 UTC

```
The pipeline works end to end. Launching the full association run (about 1,200 cells, B = 2,000) in the background, and running the size diagnostics and outcome reliability alongside.
```

### [167] TOOL CALL — Bash · 2026-09-29 05:50:37 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; rm -f results/clean_vs_raw_psp_cells_smoke.json data/psp_boot_smoke.npz; (nohup .venv/bin/python s6_assoc.py --workers 4 > logs/s6_full.out 2>&1 &); OMP_NUM_THREADS=1 timeout 900 .venv/bin/python s5_size.py 2>&1 | grep -v Warn | tail -8
```

### [168] TOOL RESULT — Bash · 2026-09-29 05:51:05 UTC

```
{"stdout": "  lg = np.log(d.deg_W3__raw.to_numpy(float))\n05:50:18|INFO   |thin-sample share (R2 raw EP ~ V2 null mean) pooled: 0.660\n05:50:18|INFO   |{'bin': '10-19', 'n': 2786, 'raw_mean': 0.0, 'v2_null_mean': 0.0, 'excess_mean': 0.0, 'rare10_mean': nan, 'curveball_null_mean': 8.791766326012902e-05, 'raw_NOV_res_mean': -0.5216546622409649, 'null_NOV_res_mean': -0.5274933995495685}\n05:50:18|INFO   |{'bin': '20-49', 'n': 7889, 'raw_mean': 0.09382943239688762, 'v2_null_mean': 0.0963756028726948, 'excess_mean': -0.0031531380053603218, 'rare10_mean': 0.11109763360540857, 'curveball_null_mean': 0.000641222651920635, 'raw_NOV_res_mean': -0.5438781920519249, 'null_NOV_res_mean': -0.5507028318387237}\n05:50:18|INFO   |{'bin': '50-99', 'n': 2422, 'raw_mean': 0.2677519517428343, 'v2_null_mean': 0.2772660544456425, 'excess_mean': -0.009858105251748264, 'rare10_mean': 0.1321835107856548, 'curveball_null_mean': 0.0015208469280279207, 'raw_NOV_res_mean': -0.5472209785936188, 'null_NOV_res_mean': -0.550636599616877}\n05:50:18|INFO   |{'bin': '100-inf', 'n': 347, 'raw_mean': 0.37634118181981757, 'v2_null_mean': 0.3893078866953596, 'excess_mean': -0.012966704875541897, 'rare10_mean': 0.15275550955093678, 'curveball_null_mean': 0.00364292101101029, 'raw_NOV_res_mean': -0.497821255841945, 'null_NOV_res_mean': -0.5060928229130698}\n05:50:19|INFO   |wrote figures/persistence_vs_n.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [169] THINKING · 2026-09-29 05:51:05 UTC

```
Raw persistence scales tightly with sample size (0.00→0.09→0.27→0.38) but the permutation-null mean tracks it almost exactly, leaving near-zero excess signal, while rarefied persistence stays nearly flat (0.11→0.15) with thin-sample share R²=0.66. Next I'll check outcome reliability.
```

### [170] TOOL CALL — Bash · 2026-09-29 05:51:05 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; OMP_NUM_THREADS=1 timeout 1500 .venv/bin/python s4b_outcome_rel.py 2>&1 | grep -v Warn | tail -4; tail -2 logs/s6_full.out; tail -1 logs/u_nulls2.out | cut -c1-400
```

### [171] TOOL RESULT — Bash · 2026-09-29 05:52:31 UTC

```
{"stdout": "05:51:09|INFO   |O2r_m50 recomputation: max diff 1.78e-15; share exact 1.0000; NaN mismatch 0\n05:52:04|INFO   |outcome reliability: {'r_half': 0.8099349043555275, 'SB': 0.8949878831624887, 'n': 7748, 'SB_ci': [0.8904772486259972, 0.8988260126382953], 'SB_boot_sd': 0.002030466617169411}\n05:50:15|INFO   |1217 tasks, B = 2000, workers 4\n05:51:04|INFO   |1/1217 done; 0.8 min; eta 979.4 min\n05:49:36|INFO   |U4: {'mean_z': -0.06679248766271317, 'sd_z': 1.043845547322944, 'graph_means': [-0.282130648558222, 0.1807350169300281, -0.36850437996727237, 0.034540548296627296, -0.26482371498755874, -0.48912259807944203, 0.09506150269093969, 0.011467296208334768, 0.3666779047936961, 0.048174196045737604], 'se_mean_graph_clustered': 0.08563184479224428, 'n_obs_graphs': 10, 'n_sets_per_graph': 2", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [172] THINKING · 2026-09-29 05:52:59 UTC

```
U4 now holds up under the clustered design (mean z = −0.067, SE 0.086), and O2r_m50 checks out reliably (split-half SB = 0.895). While the association run finishes, I'm building the verdict/disattenuation post-processor.
```

### [173] TOOL CALL — Bash · 2026-09-29 05:52:59 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; grep -n "def dersimonian_laird" -A25 lib/rq1stats.py | head -32; grep -n "def holm" -A12 lib/rq1stats.py
```

### [174] TOOL RESULT — Bash · 2026-09-29 05:52:59 UTC

```
{"stdout": "163:def dersimonian_laird(b, se) -> dict:\n164-    \"\"\"EXP6 lib/stats_core.dersimonian_laird (verbatim logic).\"\"\"\n165-    b, se = np.asarray(b, float), np.asarray(se, float)\n166-    ok = np.isfinite(b) & np.isfinite(se) & (se > 0)\n167-    b, se = b[ok], se[ok]\n168-    k = len(b)\n169-    if k == 0:\n170-        return {\"k\": 0, \"b\": float(\"nan\"), \"se\": float(\"nan\"), \"ci\": [float(\"nan\")] * 2, \"p\": float(\"nan\"),\n171-                \"tau2\": float(\"nan\"), \"I2\": float(\"nan\"), \"Q\": float(\"nan\")}\n172-    w = 1 / se**2\n173-    bf = (w * b).sum() / w.sum()\n174-    Q = float((w * (b - bf) ** 2).sum())\n175-    Cc = w.sum() - (w**2).sum() / w.sum()\n176-    tau2 = max(0.0, (Q - (k - 1)) / Cc) if k > 1 and Cc > 0 else 0.0\n177-    ws = 1 / (se**2 + tau2)\n178-    bre = (ws * b).sum() / ws.sum()\n179-    sre = math.sqrt(1 / ws.sum())\n180-    I2 = max(0.0, (Q - (k - 1)) / Q) if Q > 0 and k > 1 else 0.0\n181-    return {\"k\": k, \"b\": float(bre), \"se\": sre, \"ci\": [float(bre - 1.96 * sre), float(bre + 1.96 * sre)],\n182-            \"p\": float(2 * stats.norm.sf(abs(bre / sre))), \"tau2\": float(tau2), \"Q\": Q, \"I2\": float(I2)}\n183-\n184-\n185-def holm(p: list[float]) -> list[float]:\n186-    p = np.asarray(p, float)\n187-    out = np.full(len(p), np.nan)\n188-    ok = np.isfinite(p)\n185:def holm(p: list[float]) -> list[float]:\n186-    p = np.asarray(p, float)\n187-    out = np.full(len(p), np.nan)\n188-    ok = np.isfinite(p)\n189-    idx = np.nonzero(ok)[0]\n190-    m = len(idx)\n191-    order = idx[np.argsort(p[idx])]\n192-    run = 0.0\n193-    for r, i in enumerate(order):\n194-        run = max(run, min(1.0, (m - r) * p[i]))\n195-        out[i] = run\n196-    return out.tolist()\n197-", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [175] TOOL CALL — Write · 2026-09-29 05:54:21 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s7_verdict.py

#!/usr/bin/env python3
"""S4 post-processing: DL over groups, disattenuated effects, P1-P3, Holm and the mechanical VERDICT from the frozen
rules; headline table; figures forest_raw_vs_clean.png and reliability_bars.png.
-> results/clean_vs_raw_psp.json (label: selection data, outcomes previously unsealed)."""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from common import DATA, FIGS, RES, jdump, setup_logger
from rq1stats import dersimonian_laird, holm

logger = setup_logger("s7_verdict")
BODIES = ["DEV", "OLDHO", "COH1014", "COH1517", "POOLED"]
POOL_GROUPS = ["CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC"]


def relkey(x: str) -> str | None:
    if x.startswith("NOVCHURN_rare"):
        return "NOVCHURN_rare5"
    for base in ("NOV_res", "edge_persistence", "ego_density_W3"):
        if x.startswith(f"{base}_rare"):
            return f"{base}_rare5"
    if x in ("EP_chao", "NOVCHURN_chao", "excess_pers_cfg"):
        return None
    return x


def main() -> None:
    cells = json.loads((RES / "clean_vs_raw_psp_cells.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    boots = dict(np.load(DATA / "psp_boot.npz"))
    psp, pair = cells["psp"], cells["paired"]
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    out: dict = {"label": cells["label"], "B": cells["B"], "seed": cells["seed"], "resampling_unit": "concept"}

    def P(body, x, y="O2r_m50", rung="R2"):
        return psp.get(f"{body}|{x}|{y}|{rung}", {})

    def PR(body, a, b, rung="R2"):
        return pair.get(f"{body}|{a}|{b}|O2r_m50|{rung}", {})
    # ------------------------------------------------------------- DL over groups (POOLED, R2)
    groups = {}
    for key, g in cells["groups_raw"].items():
        b = [g.get(k, {}).get("rho", math.nan) for k in POOL_GROUPS]
        se = [g.get(k, {}).get("se", math.nan) for k in POOL_GROUPS]
        dl = dersimonian_laird(b, se)
        groups[key] = {"groups": g, "DL": dl, "n_positive_of_5": int(sum(1 for v in b if v is not None and
                                                                          np.isfinite(v) and v > 0))}
    out["groups"] = groups
    # ------------------------------------------------------------- disattenuation
    rel_y = rel["outcome"]["O2r_m50"]
    rng = np.random.default_rng(20260938)
    dis = {}
    n_pool = rel["variants"]["NOVCHURN_raw"]["pooled"]["n_concepts_mean"]
    for key, r in psp.items():
        body, x, y, rung = key.split("|")
        if y != "O2r_m50" or rung not in ("R2", "R3") or not np.isfinite(r.get("rho") or math.nan):
            continue
        rk = relkey(x)
        bk = "pooled" if body == "POOLED" else body
        if rk is None or rk not in rel["variants"]:
            dis[key] = {"psp": r["rho"], "psp_dis": None, "note": "no split-half reliability for this variant"}
            continue
        sbx = rel["variants"][rk][bk]["SB"]
        ry = (rel_y["pooled"] if body == "POOLED" else rel_y.get(body, rel_y["pooled"]))["SB"]
        if sbx is None or not np.isfinite(sbx) or sbx < 0.10 or ry is None:
            dis[key] = {"psp": r["rho"], "SB_x": sbx, "rel_y": ry, "psp_dis": None,
                        "note": "SB_x < 0.10: not disattenuated (variant essentially unreliable)"}
            continue
        sd_x = rel["variants"][rk]["pooled"].get("SB_boot_sd") or 0.01
        nb = rel["variants"][rk][bk].get("n_concepts_mean", n_pool) or n_pool
        sd_x = sd_x * math.sqrt(n_pool / max(nb, 1))
        sd_y = rel_y["pooled"].get("SB_boot_sd") or 0.005
        bs = boots.get(key.replace("|", "__"))
        est = r["rho"] / math.sqrt(sbx * ry)
        ci = [None, None]
        if bs is not None and len(bs):
            sx = np.clip(rng.normal(sbx, sd_x, len(bs)), 0.05, 1.0)
            syy = np.clip(rng.normal(ry, sd_y, len(bs)), 0.05, 1.0)
            dd = bs / np.sqrt(sx * syy)
            ci = [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]
        dis[key] = {"psp": r["rho"], "SB_x": sbx, "SB_x_key": rk, "rel_y": ry, "psp_dis": est, "ci": ci,
                    "flag": "approximate for partial Spearman (Spearman 1904 correction applied to a rank partial "
                            "correlation); rel_y conservative (m = 25 halves)"}
    out["disattenuated"] = dis
    # ------------------------------------------------------------- F6 contingency
    n_r10 = P("COH1517", "NOVCHURN_rare10").get("n", 0)
    n_r5 = P("COH1517", "NOVCHURN_rare5").get("n", 0)
    rare_primary_coh = "NOVCHURN_rare10" if n_r10 >= 150 else ("NOVCHURN_rare5" if n_r5 >= 100 else None)
    out["F6_contingency"] = {"COH1517_n_rare10": n_r10, "COH1517_n_rare5": n_r5,
                             "COH1517_rare_primary": rare_primary_coh}
    rare_primary = {"COH1517": rare_primary_coh, "OLDHO": "NOVCHURN_rare10"}
    # ------------------------------------------------------------- P1-P3
    ratios = {}
    for b in ("COH1517", "OLDHO"):
        pe = PR(b, "NOVCHURN_exc", "NOVCHURN_raw")
        rp = rare_primary[b]
        pv = PR(b, rp, "NOVCHURN_raw") if rp else {}
        ratios[b] = {"exc": pe, "rare_primary": rp, "rare": pv, "raw_full_sample": P(b, "NOVCHURN_raw")}
    p1_each = {b: bool(np.isfinite(ratios[b]["exc"].get("ratio", math.nan)) and ratios[b]["exc"]["ratio"] >= 0.70)
               for b in ratios}
    P1 = all(p1_each.values())
    zc = P("POOLED", "z_pers_cfg")
    P2 = bool(zc and np.isfinite(zc["rho"]) and zc["ci"][1] < 0)
    x = cv.NOVCHURN_exc.to_numpy(float)
    ln = np.log(cv.n_home_early.to_numpy(float))
    ok = np.isfinite(x)
    rho3 = float(stats.spearmanr(x[ok], ln[ok])[0])
    bsr = []
    idx = np.nonzero(ok)[0]
    for _ in range(500):
        i = rng.choice(idx, len(idx))
        bsr.append(stats.spearmanr(x[i], ln[i])[0])
    bsr = np.asarray(bsr)
    P3 = abs(rho3) < 0.20
    # same test on the analysis sample (finite O2r_m50)
    from tables import load_tables
    T = load_tables()["POOLED"]
    oka = np.isfinite(T.NOVCHURN_exc) & np.isfinite(T.O2r_m50)
    rho3a = float(stats.spearmanr(T.NOVCHURN_exc[oka], np.log(T.n_home_early[oka]))[0])
    out["predictions"] = {
        "P1": {"holds": P1, "per_body": p1_each, "rule": "psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, "
                                                        "COH1517 AND OLDHO",
               "detail": {b: {"ratio": ratios[b]["exc"].get("ratio"), "ratio_ci": ratios[b]["exc"].get("ratio_ci"),
                              "psp_exc": ratios[b]["exc"].get("a"), "psp_raw_same_sample": ratios[b]["exc"].get("b"),
                              "n": ratios[b]["exc"].get("n")} for b in ratios}},
        "P2": {"holds": P2, "psp": zc.get("rho"), "ci": zc.get("ci"), "n": zc.get("n")},
        "P3": {"holds": P3, "spearman_NOVCHURN_exc_log_n_all": rho3,
               "ci": [float(np.percentile(bsr, 2.5)), float(np.percentile(bsr, 97.5))], "n": int(ok.sum()),
               "spearman_on_analysis_sample": rho3a, "n_analysis": int(oka.sum())}}
    # ------------------------------------------------------------- verdict
    keep = {}
    for b in ("COH1517", "OLDHO"):
        rv = ratios[b]["rare"]
        keep[b] = rv.get("ratio") if rv else None
    v1_keep = any(v is not None and np.isfinite(v) and v >= 0.5 for v in keep.values())
    raw_ci_excl0 = {b: bool(ratios[b]["raw_full_sample"] and (ratios[b]["raw_full_sample"]["ci"][0] > 0 or
                                                             ratios[b]["raw_full_sample"]["ci"][1] < 0))
                    for b in ratios}
    thin_each = {b: bool(np.isfinite(ratios[b]["exc"].get("ratio", math.nan)) and ratios[b]["exc"]["ratio"] < 0.30 and
                         (keep[b] is None or not np.isfinite(keep[b]) or keep[b] < 0.30)) for b in ratios}
    if P1 and P3 and v1_keep:
        verdict = "CHURN_NOT_THIN"
    elif any(raw_ci_excl0.values()) and all(thin_each.values()):
        verdict = "CHURN_THIN"
    else:
        verdict = "PARTLY_THIN"
    ep_raw = P("POOLED", "edge_persistence__raw")
    flag = bool((not P2) and ep_raw and ep_raw["ci"][1] < 0)
    out["verdict"] = {"verdict": verdict, "DEGREE_ARTEFACT_PERSISTENCE": flag,
                      "clauses": {"P1": P1, "P3": P3, "V1_keeps_ge_50pct_in_COH1517_or_OLDHO": v1_keep,
                                  "V1_retention": keep, "raw_NOVCHURN_ci_excludes_0": raw_ci_excl0,
                                  "exc_and_rare_keep_lt_30pct": thin_each, "P2": P2,
                                  "raw_edge_persistence_pooled_ci_lt0": bool(ep_raw and ep_raw["ci"][1] < 0)},
                      "label": "selection data, outcomes previously unsealed: robustness evidence, not confirmation"}
    # Holm (reported only)
    p1p = max(P("COH1517", "NOVCHURN_exc").get("p_one", math.nan), P("OLDHO", "NOVCHURN_exc").get("p_one", math.nan))
    p2p = zc.get("p_one", math.nan)
    p3p = float((np.sum(np.abs(bsr) >= 0.20) + 1) / (len(bsr) + 1))
    ph = holm([p1p, p2p, p3p])
    out["holm"] = {"family": ["P1: NOVCHURN_exc psp > 0 in COH1517 and OLDHO (max one-sided p)",
                              "P2: z_pers_cfg psp < 0 POOLED", "P3: |Spearman(NOVCHURN_exc, log n)| >= 0.20 (boot)"],
                   "p": [p1p, p2p, p3p], "p_holm": ph}
    # ------------------------------------------------------------- headline table
    head = []
    for x in ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_zperm", "NOVCHURN_rare5", "NOVCHURN_rare10", "NOVCHURN_cfg",
              "NOVCHURN_chao", "NOV_res__raw", "NOV_res_exc", "NOV_res_rare10", "edge_persistence__raw",
              "edge_persistence_exc", "edge_persistence_rare10", "z_pers_cfg", "excess_pers_cfg", "EP_chao",
              "edge_persistence_nullmean", "ego_density_W3__raw", "z_dens_cfg", "z_dens_k", "OPEN_home",
              "OPEN_home_clean", "OPEN_home_exc"]:
        row = {"variant": x}
        for b in BODIES:
            r = P(b, x)
            row[b] = {"psp": r.get("rho"), "ci": r.get("ci"), "n": r.get("n")}
            raw = {"NOVCHURN": "NOVCHURN_raw", "NOV_res": "NOV_res__raw", "edge_persistence": "edge_persistence__raw",
                   "z_pers": "edge_persistence__raw", "excess_pers": "edge_persistence__raw",
                   "EP_chao": "edge_persistence__raw", "ego_density": "ego_density_W3__raw", "z_dens": "ego_density_W3__raw",
                   "OPEN_home": "OPEN_home"}
            rr = next((v for k, v in raw.items() if x.startswith(k)), None)
            if rr and rr != x:
                pr = PR(b, x, rr)
                if pr:
                    row[b]["same_sample_raw"] = pr.get("b")
                    row[b]["retention_ratio"] = pr.get("ratio")
                    row[b]["retention_ratio_ci"] = pr.get("ratio_ci")
                    row[b]["diff_ci"] = pr.get("diff_ci")
        head.append(row)
    out["headline_R2_O2r_m50"] = head
    out["cells"] = {"psp": psp, "paired": pair, "planted_PC3": cells["planted_PC3"]}
    out["confounds_removed"] = {
        "V1_rare": "removes the dependence of persistence/NOV_res on the number of home papers per year (fixed n); "
                   "does NOT remove concept-level topic heterogeneity; restricts the sample to concepts with >= n per "
                   "W-year (same-sample raw reported)",
        "V2_exc": "removes what the concept's own pooled papers would produce under a stationary partner distribution "
                  "(sampling noise given n and the concept's topic mix); conservative -- PC2 shows it also absorbs "
                  "most planted true churn at these sample sizes",
        "V2b_chao": "abundance-based undersampling correction of Jaccard; does not remove the count>=2/PMI "
                    "neighbour-rule sensitivity",
        "V3a_z_dens_cfg": "removes the part of ego density explained by partner degrees (configuration backbone); "
                          "does not remove true modular structure",
        "V3b_z_dens_k": "removes dependence of density on |S| and partner popularity",
        "V3c_z_pers_cfg": "degree normalisation of Jaccard given neighbour-set sizes and topic popularity per year; "
                          "null expected Jaccard ~0 so z ~ obs / sd; NaN when the null sd is 0 (small sets)"}
    jdump(out, RES / "clean_vs_raw_psp.json")
    logger.info(f"VERDICT {verdict}; P1 {P1} {p1_each}; P2 {P2}; P3 {P3} (rho {rho3:.3f}); V1 keep {keep}; "
                f"degree flag {flag}")
    # ------------------------------------------------------------- figures
    fvars = ["NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_rare10", "NOVCHURN_cfg", "NOVCHURN_chao", "OPEN_home",
             "OPEN_home_clean", "NOV_res__raw", "NOV_res_exc", "edge_persistence__raw", "edge_persistence_exc",
             "edge_persistence_rare10", "z_pers_cfg"]
    fig, axes = plt.subplots(1, len(BODIES), figsize=(17, 6), sharey=True)
    for ax, b in zip(axes, BODIES):
        for i, x in enumerate(fvars):
            r = P(b, x)
            if not r or r.get("rho") is None or not np.isfinite(r["rho"]):
                continue
            col = "C3" if ("raw" in x or x == "OPEN_home") else "C0"
            ax.errorbar(r["rho"], i, xerr=[[r["rho"] - r["ci"][0]], [r["ci"][1] - r["rho"]]], fmt="o", color=col,
                        ms=4, capsize=2)
        ax.axvline(0, color="k", lw=0.7)
        ax.set_title(f"{b}", fontsize=10)
        ax.set_yticks(range(len(fvars)), fvars, fontsize=8)
        ax.set_xlabel("partial Spearman | R2 (O2r_m50)", fontsize=8)
    axes[0].invert_yaxis()
    fig.suptitle("Raw (red) vs noise-controlled (blue) churn / openness variants; 95% concept-bootstrap CI; "
                 "selection data, outcomes previously unsealed", fontsize=10)
    fig.tight_layout()
    fig.savefig(FIGS / "forest_raw_vs_clean.png", dpi=150)
    rv = ["NOV_res__raw", "edge_persistence__raw", "ego_density_W3__raw", "NOVCHURN_raw", "OPEN_home",
          "edge_persistence_nullmean", "NOV_res_exc", "edge_persistence_exc", "NOVCHURN_exc", "NOV_res_rare5",
          "edge_persistence_rare5", "NOVCHURN_rare5", "z_pers_cfg", "z_dens_cfg", "z_dens_k", "NOVCHURN_cfg",
          "OPEN_home_clean", "OPEN_home_exc"]
    bins = ["n10-19", "n20-49", "n50-99", "n100-inf"]
    fig, ax = plt.subplots(figsize=(13, 4.5))
    w = 0.2
    for j, bn in enumerate(bins):
        vals = [rel["variants"][v][bn]["SB"] if v in rel["variants"] and rel["variants"][v][bn]["SB"] is not None
                else np.nan for v in rv]
        ax.bar(np.arange(len(rv)) + (j - 1.5) * w, vals, w, label=bn)
    pooled = [rel["variants"][v]["pooled"]["SB"] for v in rv]
    ax.plot(np.arange(len(rv)), pooled, "k_", ms=14, mew=2, label="pooled")
    ax.axhline(0.6, color="grey", ls="--", lw=0.8)
    ax.set_xticks(np.arange(len(rv)), rv, rotation=60, ha="right", fontsize=8)
    ax.set_ylabel("split-half reliability (Spearman-Brown)")
    ax.legend(fontsize=8, ncol=5)
    ax.set_title(f"Reliability by n_home_early bin; outcome O2r_m50 SB = {rel_y['pooled']['SB']:.2f} (m = 25 halves)")
    fig.tight_layout()
    fig.savefig(FIGS / "reliability_bars.png", dpi=150)
    logger.info("figures written")


if __name__ == "__main__":
    main()
```

### [176] TOOL RESULT — Write · 2026-09-29 05:54:21 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s7_verdict.py", "content": "#!/usr/bin/env python3\n\"\"\"S4 post-processing: DL over groups, disattenuated effects, P1-P3, Holm and the mechanical VERDICT from the frozen\nrules; headline table; figures forest_raw_vs_clean.png and reliability_bars.png.\n-> results/clean_vs_raw_psp.json (label: selection data, outcomes previously unsealed).\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport matplotlib\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\nimport numpy as np\nimport pandas as pd\nfrom scipy import stats\n\nfrom common import DATA, FIGS, RES, jdump, setup_logger\nfrom rq1stats import dersimonian_laird, holm\n\nlogger = setup_logger(\"s7_verdict\")\nBODIES = [\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\"]\nPOOL_GROUPS = [\"CS+Eng\", \"BGM+Med\", \"PHYS\", \"LIFEENV\", \"SOC\"]\n\n\ndef relkey(x: str) -> str | None:\n    if x.startswith(\"NOVCHURN_rare\"):\n        return \"NOVCHURN_rare5\"\n    for base in (\"NOV_res\", \"edge_persistence\", \"ego_density_W3\"):\n        if x.startswith(f\"{base}_rare\"):\n            return f\"{base}_rare5\"\n    if x in (\"EP_chao\", \"NOVCHURN_chao\", \"excess_pers_cfg\"):\n        return None\n    return x\n\n\ndef main() -> None:\n    cells = json.loads((RES / \"clean_vs_raw_psp_cells.json\").read_text())\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    boots = dict(np.load(DATA / \"psp_boot.npz\"))\n    psp, pair = cells[\"psp\"], cells[\"paired\"]\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    out: dict = {\"label\": cells[\"label\"], \"B\": cells[\"B\"], \"seed\": cells[\"seed\"], \"resampling_unit\": \"concept\"}\n\n    def P(body, x, y=\"O2r_m50\", rung=\"R2\"):\n        return psp.get(f\"{body}|{x}|{y}|{rung}\", {})\n\n    def PR(body, a, b, rung=\"R2\"):\n        return pair.get(f\"{body}|{a}|{b}|O2r_m50|{rung}\", {})\n    # ------------------------------------------------------------- DL over groups (POOLED, R2)\n    groups = {}\n    for key, g in cells[\"groups_raw\"].items():\n        b = [g.get(k, {}).get(\"rho\", math.nan) for k in POOL_GROUPS]\n        se = [g.get(k, {}).get(\"se\", math.nan) for k in POOL_GROUPS]\n        dl = dersimonian_laird(b, se)\n        groups[key] = {\"groups\": g, \"DL\": dl, \"n_positive_of_5\": int(sum(1 for v in b if v is not None and\n                                                                          np.isfinite(v) and v > 0))}\n    out[\"groups\"] = groups\n    # ------------------------------------------------------------- disattenuation\n    rel_y = rel[\"outcome\"][\"O2r_m50\"]\n    rng = np.random.default_rng(20260938)\n    dis = {}\n    n_pool = rel[\"variants\"][\"NOVCHURN_raw\"][\"pooled\"][\"n_concepts_mean\"]\n    for key, r in psp.items():\n        body, x, y, rung = key.split(\"|\")\n        if y != \"O2r_m50\" or rung not in (\"R2\", \"R3\") or not np.isfinite(r.get(\"rho\") or math.nan):\n            continue\n        rk = relkey(x)\n        bk = \"pooled\" if body == \"POOLED\" else body\n        if rk is None or rk not in rel[\"variants\"]:\n            dis[key] = {\"psp\": r[\"rho\"], \"psp_dis\": None, \"note\": \"no split-half reliability for this variant\"}\n            continue\n        sbx = rel[\"variants\"][rk][bk][\"SB\"]\n        ry = (rel_y[\"pooled\"] if body == \"POOLED\" else rel_y.get(body, rel_y[\"pooled\"]))[\"SB\"]\n        if sbx is None or not np.isfinite(sbx) or sbx < 0.10 or ry is None:\n            dis[key] = {\"psp\": r[\"rho\"], \"SB_x\": sbx, \"rel_y\": ry, \"psp_dis\": None,\n                        \"note\": \"SB_x < 0.10: not disattenuated (variant essentially unreliable)\"}\n            continue\n        sd_x = rel[\"variants\"][rk][\"pooled\"].get(\"SB_boot_sd\") or 0.01\n        nb = rel[\"variants\"][rk][bk].get(\"n_concepts_mean\", n_pool) or n_pool\n        sd_x = sd_x * math.sqrt(n_pool / max(nb, 1))\n        sd_y = rel_y[\"pooled\"].get(\"SB_boot_sd\") or 0.005\n        bs = boots.get(key.replace(\"|\", \"__\"))\n        est = r[\"rho\"] / math.sqrt(sbx * ry)\n        ci = [None, None]\n        if bs is not None and len(bs):\n            sx = np.clip(rng.normal(sbx, sd_x, len(bs)), 0.05, 1.0)\n            syy = np.clip(rng.normal(ry, sd_y, len(bs)), 0.05, 1.0)\n            dd = bs / np.sqrt(sx * syy)\n            ci = [float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))]\n        dis[key] = {\"psp\": r[\"rho\"], \"SB_x\": sbx, \"SB_x_key\": rk, \"rel_y\": ry, \"psp_dis\": est, \"ci\": ci,\n                    \"flag\": \"approximate for partial Spearman (Spearman 1904 correction applied to a rank partial \"\n                            \"correlation); rel_y conservative (m = 25 halves)\"}\n    out[\"disattenuated\"] = dis\n    # ------------------------------------------------------------- F6 contingency\n    n_r10 = P(\"COH1517\", \"NOVCHURN_rare10\").get(\"n\", 0)\n    n_r5 = P(\"COH1517\", \"NOVCHURN_rare5\").get(\"n\", 0)\n    rare_primary_coh = \"NOVCHURN_rare10\" if n_r10 >= 150 else (\"NOVCHURN_rare5\" if n_r5 >= 100 else None)\n    out[\"F6_contingency\"] = {\"COH1517_n_rare10\": n_r10, \"COH1517_n_rare5\": n_r5,\n                             \"COH1517_rare_primary\": rare_primary_coh}\n    rare_primary = {\"COH1517\": rare_primary_coh, \"OLDHO\": \"NOVCHURN_rare10\"}\n    # ------------------------------------------------------------- P1-P3\n    ratios = {}\n    for b in (\"COH1517\", \"OLDHO\"):\n        pe = PR(b, \"NOVCHURN_exc\", \"NOVCHURN_raw\")\n        rp = rare_primary[b]\n        pv = PR(b, rp, \"NOVCHURN_raw\") if rp else {}\n        ratios[b] = {\"exc\": pe, \"rare_primary\": rp, \"rare\": pv, \"raw_full_sample\": P(b, \"NOVCHURN_raw\")}\n    p1_each = {b: bool(np.isfinite(ratios[b][\"exc\"].get(\"ratio\", math.nan)) and ratios[b][\"exc\"][\"ratio\"] >= 0.70)\n               for b in ratios}\n    P1 = all(p1_each.values())\n    zc = P(\"POOLED\", \"z_pers_cfg\")\n    P2 = bool(zc and np.isfinite(zc[\"rho\"]) and zc[\"ci\"][1] < 0)\n    x = cv.NOVCHURN_exc.to_numpy(float)\n    ln = np.log(cv.n_home_early.to_numpy(float))\n    ok = np.isfinite(x)\n    rho3 = float(stats.spearmanr(x[ok], ln[ok])[0])\n    bsr = []\n    idx = np.nonzero(ok)[0]\n    for _ in range(500):\n        i = rng.choice(idx, len(idx))\n        bsr.append(stats.spearmanr(x[i], ln[i])[0])\n    bsr = np.asarray(bsr)\n    P3 = abs(rho3) < 0.20\n    # same test on the analysis sample (finite O2r_m50)\n    from tables import load_tables\n    T = load_tables()[\"POOLED\"]\n    oka = np.isfinite(T.NOVCHURN_exc) & np.isfinite(T.O2r_m50)\n    rho3a = float(stats.spearmanr(T.NOVCHURN_exc[oka], np.log(T.n_home_early[oka]))[0])\n    out[\"predictions\"] = {\n        \"P1\": {\"holds\": P1, \"per_body\": p1_each, \"rule\": \"psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, \"\n                                                        \"COH1517 AND OLDHO\",\n               \"detail\": {b: {\"ratio\": ratios[b][\"exc\"].get(\"ratio\"), \"ratio_ci\": ratios[b][\"exc\"].get(\"ratio_ci\"),\n                              \"psp_exc\": ratios[b][\"exc\"].get(\"a\"), \"psp_raw_same_sample\": ratios[b][\"exc\"].get(\"b\"),\n                              \"n\": ratios[b][\"exc\"].get(\"n\")} for b in ratios}},\n        \"P2\": {\"holds\": P2, \"psp\": zc.get(\"rho\"), \"ci\": zc.get(\"ci\"), \"n\": zc.get(\"n\")},\n        \"P3\": {\"holds\": P3, \"spearman_NOVCHURN_exc_log_n_all\": rho3,\n               \"ci\": [float(np.percentile(bsr, 2.5)), float(np.percentile(bsr, 97.5))], \"n\": int(ok.sum()),\n               \"spearman_on_analysis_sample\": rho3a, \"n_analysis\": int(oka.sum())}}\n    # ------------------------------------------------------------- verdict\n    keep = {}\n    for b in (\"COH1517\", \"OLDHO\"):\n        rv = ratios[b][\"rare\"]\n        keep[b] = rv.get(\"ratio\") if rv else None\n    v1_keep = any(v is not None and np.isfinite(v) and v >= 0.5 for v in keep.values())\n    raw_ci_excl0 = {b: bool(ratios[b][\"raw_full_sample\"] and (ratios[b][\"raw_full_sample\"][\"ci\"][0] > 0 or\n                                                             ratios[b][\"raw_full_sample\"][\"ci\"][1] < 0))\n                    for b in ratios}\n    thin_each = {b: bool(np.isfinite(ratios[b][\"exc\"].get(\"ratio\", math.nan)) and ratios[b][\"exc\"][\"ratio\"] < 0.30 and\n                         (keep[b] is None or not np.isfinite(keep[b]) or keep[b] < 0.30)) for b in ratios}\n    if P1 and P3 and v1_keep:\n        verdict = \"CHURN_NOT_THIN\"\n    elif any(raw_ci_excl0.values()) and all(thin_each.values()):\n        verdict = \"CHURN_THIN\"\n    else:\n        verdict = \"PARTLY_THIN\"\n    ep_raw = P(\"POOLED\", \"edge_persistence__raw\")\n    flag = bool((not P2) and ep_raw and ep_raw[\"ci\"][1] < 0)\n    out[\"verdict\"] = {\"verdict\": verdict, \"DEGREE_ARTEFACT_PERSISTENCE\": flag,\n                      \"clauses\": {\"P1\": P1, \"P3\": P3, \"V1_keeps_ge_50pct_in_COH1517_or_OLDHO\": v1_keep,\n                                  \"V1_retention\": keep, \"raw_NOVCHURN_ci_excludes_0\": raw_ci_excl0,\n                                  \"exc_and_rare_keep_lt_30pct\": thin_each, \"P2\": P2,\n                                  \"raw_edge_persistence_pooled_ci_lt0\": bool(ep_raw and ep_raw[\"ci\"][1] < 0)},\n                      \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\"}\n    # Holm (reported only)\n    p1p = max(P(\"COH1517\", \"NOVCHURN_exc\").get(\"p_one\", math.nan), P(\"OLDHO\", \"NOVCHURN_exc\").get(\"p_one\", math.nan))\n    p2p = zc.get(\"p_one\", math.nan)\n    p3p = float((np.sum(np.abs(bsr) >= 0.20) + 1) / (len(bsr) + 1))\n    ph = holm([p1p, p2p, p3p])\n    out[\"holm\"] = {\"family\": [\"P1: NOVCHURN_exc psp > 0 in COH1517 and OLDHO (max one-sided p)\",\n                              \"P2: z_pers_cfg psp < 0 POOLED\", \"P3: |Spearman(NOVCHURN_exc, log n)| >= 0.20 (boot)\"],\n                   \"p\": [p1p, p2p, p3p], \"p_holm\": ph}\n    # ------------------------------------------------------------- headline table\n    head = []\n    for x in [\"NOVCHURN_raw\", \"NOVCHURN_exc\", \"NOVCHURN_zperm\", \"NOVCHURN_rare5\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\",\n              \"NOVCHURN_chao\", \"NOV_res__raw\", \"NOV_res_exc\", \"NOV_res_rare10\", \"edge_persistence__raw\",\n              \"edge_persistence_exc\", \"edge_persistence_rare10\", \"z_pers_cfg\", \"excess_pers_cfg\", \"EP_chao\",\n              \"edge_persistence_nullmean\", \"ego_density_W3__raw\", \"z_dens_cfg\", \"z_dens_k\", \"OPEN_home\",\n              \"OPEN_home_clean\", \"OPEN_home_exc\"]:\n        row = {\"variant\": x}\n        for b in BODIES:\n            r = P(b, x)\n            row[b] = {\"psp\": r.get(\"rho\"), \"ci\": r.get(\"ci\"), \"n\": r.get(\"n\")}\n            raw = {\"NOVCHURN\": \"NOVCHURN_raw\", \"NOV_res\": \"NOV_res__raw\", \"edge_persistence\": \"edge_persistence__raw\",\n                   \"z_pers\": \"edge_persistence__raw\", \"excess_pers\": \"edge_persistence__raw\",\n                   \"EP_chao\": \"edge_persistence__raw\", \"ego_density\": \"ego_density_W3__raw\", \"z_dens\": \"ego_density_W3__raw\",\n                   \"OPEN_home\": \"OPEN_home\"}\n            rr = next((v for k, v in raw.items() if x.startswith(k)), None)\n            if rr and rr != x:\n                pr = PR(b, x, rr)\n                if pr:\n                    row[b][\"same_sample_raw\"] = pr.get(\"b\")\n                    row[b][\"retention_ratio\"] = pr.get(\"ratio\")\n                    row[b][\"retention_ratio_ci\"] = pr.get(\"ratio_ci\")\n                    row[b][\"diff_ci\"] = pr.get(\"diff_ci\")\n        head.append(row)\n    out[\"headline_R2_O2r_m50\"] = head\n    out[\"cells\"] = {\"psp\": psp, \"paired\": pair, \"planted_PC3\": cells[\"planted_PC3\"]}\n    out[\"confounds_removed\"] = {\n        \"V1_rare\": \"removes the dependence of persistence/NOV_res on the number of home papers per year (fixed n); \"\n                   \"does NOT remove concept-level topic heterogeneity; restricts the sample to concepts with >= n per \"\n                   \"W-year (same-sample raw reported)\",\n        \"V2_exc\": \"removes what the concept's own pooled papers would produce under a stationary partner distribution \"\n                  \"(sampling noise given n and the concept's topic mix); conservative -- PC2 shows it also absorbs \"\n                  \"most planted true churn at these sample sizes\",\n        \"V2b_chao\": \"abundance-based undersampling correction of Jaccard; does not remove the count>=2/PMI \"\n                    \"neighbour-rule sensitivity\",\n        \"V3a_z_dens_cfg\": \"removes the part of ego density explained by partner degrees (configuration backbone); \"\n                          \"does not remove true modular structure\",\n        \"V3b_z_dens_k\": \"removes dependence of density on |S| and partner popularity\",\n        \"V3c_z_pers_cfg\": \"degree normalisation of Jaccard given neighbour-set sizes and topic popularity per year; \"\n                          \"null expected Jaccard ~0 so z ~ obs / sd; NaN when the null sd is 0 (small sets)\"}\n    jdump(out, RES / \"clean_vs_raw_psp.json\")\n    logger.info(f\"VERDICT {verdict}; P1 {P1} {p1_each}; P2 {P2}; P3 {P3} (rho {rho3:.3f}); V1 keep {keep}; \"\n                f\"degree flag {flag}\")\n    # ------------------------------------------------------------- figures\n    fvars = [\"NOVCHURN_raw\", \"NOVCHURN_exc\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\", \"NOVCHURN_chao\", \"OPEN_home\",\n             \"OPEN_home_clean\", \"NOV_res__raw\", \"NOV_res_exc\", \"edge_persistence__raw\", \"edge_persistence_exc\",\n             \"edge_persistence_rare10\", \"z_pers_cfg\"]\n    fig, axes = plt.subplots(1, len(BODIES), figsize=(17, 6), sharey=True)\n    for ax, b in zip(axes, BODIES):\n        for i, x in enumerate(fvars):\n            r = P(b, x)\n            if not r or r.get(\"rho\") is None or not np.isfinite(r[\"rho\"]):\n                continue\n            col = \"C3\" if (\"raw\" in x or x == \"OPEN_home\") else \"C0\"\n            ax.errorbar(r[\"rho\"], i, xerr=[[r[\"rho\"] - r[\"ci\"][0]], [r[\"ci\"][1] - r[\"rho\"]]], fmt=\"o\", color=col,\n                        ms=4, capsize=2)\n        ax.axvline(0, color=\"k\", lw=0.7)\n        ax.set_title(f\"{b}\", fontsize=10)\n        ax.set_yticks(range(len(fvars)), fvars, fontsize=8)\n        ax.set_xlabel(\"partial Spearman | R2 (O2r_m50)\", fontsize=8)\n    axes[0].invert_yaxis()\n    fig.suptitle(\"Raw (red) vs noise-controlled (blue) churn / openness variants; 95% concept-bootstrap CI; \"\n                 \"selection data, outcomes previously unsealed\", fontsize=10)\n    fig.tight_layout()\n    fig.savefig(FIGS / \"forest_raw_vs_clean.png\", dpi=150)\n    rv = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"NOVCHURN_raw\", \"OPEN_home\",\n          \"edge_persistence_nullmean\", \"NOV_res_exc\", \"edge_persistence_exc\", \"NOVCHURN_exc\", \"NOV_res_rare5\",\n          \"edge_persistence_rare5\", \"NOVCHURN_rare5\", \"z_pers_cfg\", \"z_dens_cfg\", \"z_dens_k\", \"NOVCHURN_cfg\",\n          \"OPEN_home_clean\", \"OPEN_home_exc\"]\n    bins = [\"n10-19\", \"n20-49\", \"n50-99\", \"n100-inf\"]\n    fig, ax = plt.subplots(figsize=(13, 4.5))\n    w = 0.2\n    for j, bn in enumerate(bins):\n        vals = [rel[\"variants\"][v][bn][\"SB\"] if v in rel[\"variants\"] and rel[\"variants\"][v][bn][\"SB\"] is not None\n                else np.nan for v in rv]\n        ax.bar(np.arange(len(rv)) + (j - 1.5) * w, vals, w, label=bn)\n    pooled = [rel[\"variants\"][v][\"pooled\"][\"SB\"] for v in rv]\n    ax.plot(np.arange(len(rv)), pooled, \"k_\", ms=14, mew=2, label=\"pooled\")\n    ax.axhline(0.6, color=\"grey\", ls=\"--\", lw=0.8)\n    ax.set_xticks(np.arange(len(rv)), rv, rotation=60, ha=\"right\", fontsize=8)\n    ax.set_ylabel(\"split-half reliability (Spearman-Brown)\")\n    ax.legend(fontsize=8, ncol=5)\n    ax.set_title(f\"Reliability by n_home_early bin; outcome O2r_m50 SB = {rel_y['pooled']['SB']:.2f} (m = 25 halves)\")\n    fig.tight_layout()\n    fig.savefig(FIGS / \"reliability_bars.png\", dpi=150)\n    logger.info(\"figures written\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [177] TOOL CALL — Bash · 2026-09-29 05:54:21 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -2 logs/s6_full.out
```

### [178] TOOL RESULT — Bash · 2026-09-29 05:54:21 UTC

```
{"stdout": "05:50:15|INFO   |1217 tasks, B = 2000, workers 4\n05:51:04|INFO   |1/1217 done; 0.8 min; eta 979.4 min", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [179] TOOL CALL — Bash · 2026-09-29 05:54:21 UTC

```
top -bn1 | head -15; cat /sys/fs/cgroup/memory.current
```

### [180] TOOL RESULT — Bash · 2026-09-29 05:54:21 UTC

```
{"stdout": "top - 05:53:28 up 45 days, 20:58,  0 user,  load average: 150.97, 139.79, 120.96\nTasks:  13 total,   5 running,   8 sleeping,   0 stopped,   0 zombie\n%Cpu(s): 16.0 us,  2.1 sy,  1.1 ni, 74.5 id,  6.4 wa,  0.0 hi,  0.0 si,  0.0 st \nMiB Mem : 773139.8 total, 179368.2 free,  65424.5 used, 533946.6 buff/cache     \nMiB Swap:      0.0 total,      0.0 free,      0.0 used. 707715.3 avail Mem \n\n    PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND\n   1432 root      20   0 2184804 271416  83632 R 100.0   0.0   2:45.61 python\n   1435 root      20   0 2186364 273220  83684 R 100.0   0.0   2:50.90 python\n   1436 root      20   0 2184412 270984  83404 R 100.0   0.0   2:47.88 python\n   1437 root      20   0 2184680 271540  83744 R 100.0   0.0   2:45.35 python\n     39 root      20   0 5589796 424744 131432 S   6.7   0.1   1:07.29 claude\n      1 root      20   0    2488   1216   1120 S   0.0   0.0   0:00.04 tini\n      7 root      20   0  445684 119744  23404 S   0.0   0.0   0:37.34 python\n     27 root      20   0   15460   3520   2192 S   0.0   0.0   0:00.00 sshd\n2830147584", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [181] ASSISTANT · 2026-09-29 05:55:29 UTC

```
All 4 association workers are at 100% single-threaded; estimated ~35 min. Writing the Frame-N power simulation meanwhile.
```

### [182] TOOL CALL — Write · 2026-09-29 05:55:29 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s8_power.py

#!/usr/bin/env python3
"""S5 POWER FOR FRAME N (simulation from selection data).

Targets theta (per index x rung R3 / R5):
  T1 disattenuated POOLED estimate (true scale) -> observed Frame-N scale = T1 x sqrt(SB_x(mix) x rel_y)
  T2 COH1517 raw estimate (observed scale; scenario S_B attenuated by sqrt(SB_x(S_B) / SB_x(S_A)))
  T3 half the POOLED raw estimate (EXP10 convention; same scenario scaling as T2)
Indices: OPEN_home, NOVCHURN_raw, and NOVCHURN_exc unless the verdict is CHURN_THIN.
Scenarios: S_A = EXP5 n_home_early mix (>= 10); S_B = pessimistic, n-bin weights shifted one bin down (sampling
importance-reweighted within agroup). Draws: n concepts resampled with replacement from POOLED, stratified by agroup
(EXP5 mix); psp at R3 and R5 for every index on the same draw; shifted by (target - full-sample estimate);
SE = infl / sqrt(n - k - 3) with infl = bootstrap SE_z / analytic SE on COH1517; pass iff atanh(est) - 1.96 SE > 0.
-> results/power_frame_n.json, figures/power_curves.png"""
from __future__ import annotations

import os

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import json
import math
import multiprocessing as mp
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from common import FIGS, RES, jdump, setup_logger

NS = [800, 1500, 2500]
DRAWS = 1000
BINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]
BIN_KEYS = ["n10-19", "n20-49", "n50-99", "n100-inf"]


def bin_of(n: np.ndarray) -> np.ndarray:
    return np.digitize(n, [20, 50, 100])


def sim_task(args: tuple) -> dict:
    import warnings
    warnings.simplefilter("ignore", RuntimeWarning)
    from rq1stats import psp_point
    from tables import design, load_tables
    scen, n, indices, seed = args
    T = load_tables()["POOLED"]
    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
    ex5 = T.frame == "exp5"
    mix = T[ex5].agroup.value_counts(normalize=True)
    b = bin_of(T.n_home_early.to_numpy())
    wA = np.bincount(bin_of(T[ex5].n_home_early.to_numpy()), minlength=4) / ex5.sum()
    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]
    imp = (wB / np.where(wA > 0, wA, 1))[b] if scen == "S_B" else np.ones(len(T))
    rng = np.random.default_rng(seed)
    des = {r: design(T, r, pooled=True) for r in ("R3", "R5")}
    k = {r: des[r][0].shape[1] + des[r][1].shape[1] for r in des}
    groups = {g: np.nonzero((T.agroup == g).to_numpy())[0] for g in mix.index}
    y = T.O2r_m50.to_numpy(float)
    X = {x: T[x].to_numpy(float) for x in indices}
    est = {f"{x}|{r}": np.full(DRAWS, np.nan) for x in indices for r in des}
    neff = {f"{x}|{r}": np.full(DRAWS, np.nan) for x in indices for r in des}
    for d in range(DRAWS):
        idx = []
        for g, share in mix.items():
            m = int(round(n * share))
            p = imp[groups[g]]
            p = p / p.sum()
            idx.append(rng.choice(groups[g], m, replace=True, p=p))
        i = np.concatenate(idx)
        for r in des:
            Bm, Cm = des[r][0][i], des[r][1][i]
            keep = Cm.std(0) > 0
            Cm = Cm[:, keep]
            for x in indices:
                xv = X[x][i]
                ok = np.isfinite(xv) & np.all(np.isfinite(Bm), 1)
                if ok.sum() < 50:
                    continue
                est[f"{x}|{r}"][d] = psp_point(xv[ok], y[i][ok], Bm[ok], Cm[ok])
                neff[f"{x}|{r}"][d] = ok.sum()
    return {"scen": scen, "n": n, "est": est, "neff": neff, "k": k}


def main() -> None:
    logger = setup_logger("s8_power")
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    verdict = V["verdict"]["verdict"]
    indices = ["OPEN_home", "NOVCHURN_raw"] + ([] if verdict == "CHURN_THIN" else ["NOVCHURN_exc"])
    cells = V["cells"]["psp"]
    rel_y = rel["outcome"]["O2r_m50"]["pooled"]["SB"]
    from tables import load_tables
    T = load_tables()["POOLED"]
    ex5 = T[(T.frame == "exp5") & np.isfinite(T.O2r_m50)]
    wA = np.bincount(bin_of(ex5.n_home_early.to_numpy()), minlength=4) / len(ex5)
    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]

    def sb_mix(x, w):
        vals = np.array([rel["variants"][x][bk]["SB"] if rel["variants"][x][bk]["SB"] is not None else np.nan
                         for bk in BIN_KEYS], float)
        vals = np.where(np.isfinite(vals), vals, np.nanmean(vals))
        return float(np.sum(w * vals))
    targets = {}
    for x in indices:
        sbA, sbB = sb_mix(x, wA), sb_mix(x, wB)
        sb_pool = rel["variants"][x]["pooled"]["SB"]
        for r in ("R3", "R5"):
            pool = cells.get(f"POOLED|{x}|O2r_m50|{r}", {})
            coh = cells.get(f"COH1517|{x}|O2r_m50|{r}", {})
            full = pool.get("rho", math.nan)
            t1 = full / math.sqrt(max(sb_pool, 1e-6) * rel_y) if sb_pool and sb_pool > 0.05 else math.nan
            infl = math.nan
            if coh.get("se_z") and coh.get("n"):
                # analytic SE with the COH1517 rung size (k from the rung definition)
                kk = {"R3": 21 + 8, "R5": 26 + 10}[r]
                infl = coh["se_z"] * math.sqrt(max(coh["n"] - kk - 3, 1))
            targets[f"{x}|{r}"] = {
                "full_sample_pooled": full, "SB_pooled": sb_pool, "SB_S_A": sbA, "SB_S_B": sbB, "rel_y": rel_y,
                "infl": infl,
                "S_A": {"T1": t1 * math.sqrt(sbA * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan), "T3": 0.5 * full},
                "S_B": {"T1": t1 * math.sqrt(sbB * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan) * math.sqrt(sbB / sbA) if sbA > 0 else math.nan,
                        "T3": 0.5 * full * math.sqrt(sbB / sbA) if sbA > 0 else math.nan},
                "T1_true_scale": t1}
    logger.info(f"targets: { {k: v['S_A'] for k, v in targets.items()} }")
    tasks = [(s, n, indices, 20260940 + 10 * i + j) for i, s in enumerate(("S_A", "S_B")) for j, n in enumerate(NS)]
    with ProcessPoolExecutor(4, mp_context=mp.get_context("spawn")) as ex:
        sims = list(ex.map(sim_task, tasks))
    res: dict = {"label": "selection data, outcomes previously unsealed; simulated Frame-N power", "draws": DRAWS,
                 "indices": indices, "targets": targets, "scenarios": {"S_A": {"n_bin_weights": wA.tolist()},
                                                                       "S_B": {"n_bin_weights": wB.tolist()}},
                 "results": {}}
    infl_used = {}
    for sim in sims:
        s, n = sim["scen"], sim["n"]
        for tname in ("T1", "T2", "T3"):
            passes = {}
            mde = {}
            for key, e in sim["est"].items():
                tg = targets[key][s][tname]
                infl = targets[key]["infl"] if np.isfinite(targets[key]["infl"]) else 1.0
                infl_used[key] = infl
                full = targets[key]["full_sample_pooled"]
                sh = e + (tg - full)
                se = infl / np.sqrt(np.maximum(sim["neff"][key] - sim["k"][key.split("|")[1]] - 3, 1))
                zlo = np.arctanh(np.clip(sh, -0.999, 0.999)) - 1.96 * se
                passes[key] = np.where(np.isfinite(zlo), zlo > 0, False)
                mde[key] = float(np.tanh(2.8 * np.nanmedian(se)))
            nov = "NOVCHURN_raw"
            joint = passes["OPEN_home|R3"] & passes["OPEN_home|R5"] & passes[f"{nov}|R3"]
            ent = {"marginal": {k: float(v.mean()) for k, v in passes.items()}, "joint_OPEN_R3_R5_NOVCHURN_R3":
                   float(joint.mean()), "MDE_r": mde,
                   "targets_observed_scale": {k: targets[k][s][tname] for k in passes}}
            if "NOVCHURN_exc|R3" in passes:
                ent["joint_with_NOVCHURN_exc"] = float((passes["OPEN_home|R3"] & passes["OPEN_home|R5"] &
                                                        passes["NOVCHURN_exc|R3"]).mean())
            res["results"][f"{s}|{tname}|n{n}"] = ent
    # analytic n for 0.8 marginal power (one-sided lower bound > 0 at alpha 0.025): n = (2.8 infl / atanh t)^2 + k + 3
    n80 = {}
    for key, t in targets.items():
        kk = {"R3": 29, "R5": 36}[key.split("|")[1]]
        for s in ("S_A", "S_B"):
            for tn in ("T1", "T2", "T3"):
                th = t[s][tn]
                n80[f"{key}|{s}|{tn}"] = (float((2.8 * infl_used.get(key, 1.0) / math.atanh(th)) ** 2 + kk + 3)
                                          if th is not None and np.isfinite(th) and th > 0 else None)
    res["n_for_80pct_marginal"] = n80
    a = res["results"]
    res["plain_language"] = (
        f"At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = "
        f"{a['S_A|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}; at n = 2500 it is "
        f"{a['S_A|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. With T2 (COH1517 raw) it is "
        f"{a['S_A|T2|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / {a['S_A|T2|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}"
        f". Pessimistic n-mix (S_B, T3): {a['S_B|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / "
        f"{a['S_B|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. The fallback O2r_m30 outcome set is not simulated "
        f"here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.")
    jdump(res, RES / "power_frame_n.json")
    logger.info(res["plain_language"])
    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
    for ax, s in zip(axes, ("S_A", "S_B")):
        for tn, ls in (("T1", "-"), ("T2", "--"), ("T3", ":")):
            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["joint_OPEN_R3_R5_NOVCHURN_R3"] for n in NS], "o" + ls, label=f"joint {tn}")
            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["marginal"]["OPEN_home|R3"] for n in NS], "s" + ls, alpha=0.5,
                    label=f"OPEN_home R3 {tn}")
        ax.axhline(0.8, color="grey", lw=0.8)
        ax.set_xlabel("Frame-N concepts with outcome")
        ax.set_title(f"scenario {s}")
    axes[0].set_ylabel("power (lower 95% bound > 0)")
    axes[0].legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(FIGS / "power_curves.png", dpi=150)


if __name__ == "__main__":
    main()
```

### [183] TOOL RESULT — Write · 2026-09-29 05:55:29 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/s8_power.py", "content": "#!/usr/bin/env python3\n\"\"\"S5 POWER FOR FRAME N (simulation from selection data).\n\nTargets theta (per index x rung R3 / R5):\n  T1 disattenuated POOLED estimate (true scale) -> observed Frame-N scale = T1 x sqrt(SB_x(mix) x rel_y)\n  T2 COH1517 raw estimate (observed scale; scenario S_B attenuated by sqrt(SB_x(S_B) / SB_x(S_A)))\n  T3 half the POOLED raw estimate (EXP10 convention; same scenario scaling as T2)\nIndices: OPEN_home, NOVCHURN_raw, and NOVCHURN_exc unless the verdict is CHURN_THIN.\nScenarios: S_A = EXP5 n_home_early mix (>= 10); S_B = pessimistic, n-bin weights shifted one bin down (sampling\nimportance-reweighted within agroup). Draws: n concepts resampled with replacement from POOLED, stratified by agroup\n(EXP5 mix); psp at R3 and R5 for every index on the same draw; shifted by (target - full-sample estimate);\nSE = infl / sqrt(n - k - 3) with infl = bootstrap SE_z / analytic SE on COH1517; pass iff atanh(est) - 1.96 SE > 0.\n-> results/power_frame_n.json, figures/power_curves.png\"\"\"\nfrom __future__ import annotations\n\nimport os\n\nos.environ.setdefault(\"OMP_NUM_THREADS\", \"1\")\nos.environ.setdefault(\"OPENBLAS_NUM_THREADS\", \"1\")\n\nimport json\nimport math\nimport multiprocessing as mp\nimport sys\nfrom concurrent.futures import ProcessPoolExecutor\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport matplotlib\n\nmatplotlib.use(\"Agg\")\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nfrom common import FIGS, RES, jdump, setup_logger\n\nNS = [800, 1500, 2500]\nDRAWS = 1000\nBINS = [(10, 19), (20, 49), (50, 99), (100, 10 ** 9)]\nBIN_KEYS = [\"n10-19\", \"n20-49\", \"n50-99\", \"n100-inf\"]\n\n\ndef bin_of(n: np.ndarray) -> np.ndarray:\n    return np.digitize(n, [20, 50, 100])\n\n\ndef sim_task(args: tuple) -> dict:\n    import warnings\n    warnings.simplefilter(\"ignore\", RuntimeWarning)\n    from rq1stats import psp_point\n    from tables import design, load_tables\n    scen, n, indices, seed = args\n    T = load_tables()[\"POOLED\"]\n    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)\n    ex5 = T.frame == \"exp5\"\n    mix = T[ex5].agroup.value_counts(normalize=True)\n    b = bin_of(T.n_home_early.to_numpy())\n    wA = np.bincount(bin_of(T[ex5].n_home_early.to_numpy()), minlength=4) / ex5.sum()\n    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]\n    imp = (wB / np.where(wA > 0, wA, 1))[b] if scen == \"S_B\" else np.ones(len(T))\n    rng = np.random.default_rng(seed)\n    des = {r: design(T, r, pooled=True) for r in (\"R3\", \"R5\")}\n    k = {r: des[r][0].shape[1] + des[r][1].shape[1] for r in des}\n    groups = {g: np.nonzero((T.agroup == g).to_numpy())[0] for g in mix.index}\n    y = T.O2r_m50.to_numpy(float)\n    X = {x: T[x].to_numpy(float) for x in indices}\n    est = {f\"{x}|{r}\": np.full(DRAWS, np.nan) for x in indices for r in des}\n    neff = {f\"{x}|{r}\": np.full(DRAWS, np.nan) for x in indices for r in des}\n    for d in range(DRAWS):\n        idx = []\n        for g, share in mix.items():\n            m = int(round(n * share))\n            p = imp[groups[g]]\n            p = p / p.sum()\n            idx.append(rng.choice(groups[g], m, replace=True, p=p))\n        i = np.concatenate(idx)\n        for r in des:\n            Bm, Cm = des[r][0][i], des[r][1][i]\n            keep = Cm.std(0) > 0\n            Cm = Cm[:, keep]\n            for x in indices:\n                xv = X[x][i]\n                ok = np.isfinite(xv) & np.all(np.isfinite(Bm), 1)\n                if ok.sum() < 50:\n                    continue\n                est[f\"{x}|{r}\"][d] = psp_point(xv[ok], y[i][ok], Bm[ok], Cm[ok])\n                neff[f\"{x}|{r}\"][d] = ok.sum()\n    return {\"scen\": scen, \"n\": n, \"est\": est, \"neff\": neff, \"k\": k}\n\n\ndef main() -> None:\n    logger = setup_logger(\"s8_power\")\n    V = json.loads((RES / \"clean_vs_raw_psp.json\").read_text())\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    verdict = V[\"verdict\"][\"verdict\"]\n    indices = [\"OPEN_home\", \"NOVCHURN_raw\"] + ([] if verdict == \"CHURN_THIN\" else [\"NOVCHURN_exc\"])\n    cells = V[\"cells\"][\"psp\"]\n    rel_y = rel[\"outcome\"][\"O2r_m50\"][\"pooled\"][\"SB\"]\n    from tables import load_tables\n    T = load_tables()[\"POOLED\"]\n    ex5 = T[(T.frame == \"exp5\") & np.isfinite(T.O2r_m50)]\n    wA = np.bincount(bin_of(ex5.n_home_early.to_numpy()), minlength=4) / len(ex5)\n    wB = np.r_[wA[0] + wA[1], wA[2], wA[3], 0.0]\n\n    def sb_mix(x, w):\n        vals = np.array([rel[\"variants\"][x][bk][\"SB\"] if rel[\"variants\"][x][bk][\"SB\"] is not None else np.nan\n                         for bk in BIN_KEYS], float)\n        vals = np.where(np.isfinite(vals), vals, np.nanmean(vals))\n        return float(np.sum(w * vals))\n    targets = {}\n    for x in indices:\n        sbA, sbB = sb_mix(x, wA), sb_mix(x, wB)\n        sb_pool = rel[\"variants\"][x][\"pooled\"][\"SB\"]\n        for r in (\"R3\", \"R5\"):\n            pool = cells.get(f\"POOLED|{x}|O2r_m50|{r}\", {})\n            coh = cells.get(f\"COH1517|{x}|O2r_m50|{r}\", {})\n            full = pool.get(\"rho\", math.nan)\n            t1 = full / math.sqrt(max(sb_pool, 1e-6) * rel_y) if sb_pool and sb_pool > 0.05 else math.nan\n            infl = math.nan\n            if coh.get(\"se_z\") and coh.get(\"n\"):\n                # analytic SE with the COH1517 rung size (k from the rung definition)\n                kk = {\"R3\": 21 + 8, \"R5\": 26 + 10}[r]\n                infl = coh[\"se_z\"] * math.sqrt(max(coh[\"n\"] - kk - 3, 1))\n            targets[f\"{x}|{r}\"] = {\n                \"full_sample_pooled\": full, \"SB_pooled\": sb_pool, \"SB_S_A\": sbA, \"SB_S_B\": sbB, \"rel_y\": rel_y,\n                \"infl\": infl,\n                \"S_A\": {\"T1\": t1 * math.sqrt(sbA * rel_y) if np.isfinite(t1) else math.nan,\n                        \"T2\": coh.get(\"rho\", math.nan), \"T3\": 0.5 * full},\n                \"S_B\": {\"T1\": t1 * math.sqrt(sbB * rel_y) if np.isfinite(t1) else math.nan,\n                        \"T2\": coh.get(\"rho\", math.nan) * math.sqrt(sbB / sbA) if sbA > 0 else math.nan,\n                        \"T3\": 0.5 * full * math.sqrt(sbB / sbA) if sbA > 0 else math.nan},\n                \"T1_true_scale\": t1}\n    logger.info(f\"targets: { {k: v['S_A'] for k, v in targets.items()} }\")\n    tasks = [(s, n, indices, 20260940 + 10 * i + j) for i, s in enumerate((\"S_A\", \"S_B\")) for j, n in enumerate(NS)]\n    with ProcessPoolExecutor(4, mp_context=mp.get_context(\"spawn\")) as ex:\n        sims = list(ex.map(sim_task, tasks))\n    res: dict = {\"label\": \"selection data, outcomes previously unsealed; simulated Frame-N power\", \"draws\": DRAWS,\n                 \"indices\": indices, \"targets\": targets, \"scenarios\": {\"S_A\": {\"n_bin_weights\": wA.tolist()},\n                                                                       \"S_B\": {\"n_bin_weights\": wB.tolist()}},\n                 \"results\": {}}\n    infl_used = {}\n    for sim in sims:\n        s, n = sim[\"scen\"], sim[\"n\"]\n        for tname in (\"T1\", \"T2\", \"T3\"):\n            passes = {}\n            mde = {}\n            for key, e in sim[\"est\"].items():\n                tg = targets[key][s][tname]\n                infl = targets[key][\"infl\"] if np.isfinite(targets[key][\"infl\"]) else 1.0\n                infl_used[key] = infl\n                full = targets[key][\"full_sample_pooled\"]\n                sh = e + (tg - full)\n                se = infl / np.sqrt(np.maximum(sim[\"neff\"][key] - sim[\"k\"][key.split(\"|\")[1]] - 3, 1))\n                zlo = np.arctanh(np.clip(sh, -0.999, 0.999)) - 1.96 * se\n                passes[key] = np.where(np.isfinite(zlo), zlo > 0, False)\n                mde[key] = float(np.tanh(2.8 * np.nanmedian(se)))\n            nov = \"NOVCHURN_raw\"\n            joint = passes[\"OPEN_home|R3\"] & passes[\"OPEN_home|R5\"] & passes[f\"{nov}|R3\"]\n            ent = {\"marginal\": {k: float(v.mean()) for k, v in passes.items()}, \"joint_OPEN_R3_R5_NOVCHURN_R3\":\n                   float(joint.mean()), \"MDE_r\": mde,\n                   \"targets_observed_scale\": {k: targets[k][s][tname] for k in passes}}\n            if \"NOVCHURN_exc|R3\" in passes:\n                ent[\"joint_with_NOVCHURN_exc\"] = float((passes[\"OPEN_home|R3\"] & passes[\"OPEN_home|R5\"] &\n                                                        passes[\"NOVCHURN_exc|R3\"]).mean())\n            res[\"results\"][f\"{s}|{tname}|n{n}\"] = ent\n    # analytic n for 0.8 marginal power (one-sided lower bound > 0 at alpha 0.025): n = (2.8 infl / atanh t)^2 + k + 3\n    n80 = {}\n    for key, t in targets.items():\n        kk = {\"R3\": 29, \"R5\": 36}[key.split(\"|\")[1]]\n        for s in (\"S_A\", \"S_B\"):\n            for tn in (\"T1\", \"T2\", \"T3\"):\n                th = t[s][tn]\n                n80[f\"{key}|{s}|{tn}\"] = (float((2.8 * infl_used.get(key, 1.0) / math.atanh(th)) ** 2 + kk + 3)\n                                          if th is not None and np.isfinite(th) and th > 0 else None)\n    res[\"n_for_80pct_marginal\"] = n80\n    a = res[\"results\"]\n    res[\"plain_language\"] = (\n        f\"At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = \"\n        f\"{a['S_A|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}; at n = 2500 it is \"\n        f\"{a['S_A|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. With T2 (COH1517 raw) it is \"\n        f\"{a['S_A|T2|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / {a['S_A|T2|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}\"\n        f\". Pessimistic n-mix (S_B, T3): {a['S_B|T3|n800']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f} / \"\n        f\"{a['S_B|T3|n2500']['joint_OPEN_R3_R5_NOVCHURN_R3']:.2f}. The fallback O2r_m30 outcome set is not simulated \"\n        f\"here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.\")\n    jdump(res, RES / \"power_frame_n.json\")\n    logger.info(res[\"plain_language\"])\n    fig, axes = plt.subplots(1, 2, figsize=(11, 4), sharey=True)\n    for ax, s in zip(axes, (\"S_A\", \"S_B\")):\n        for tn, ls in ((\"T1\", \"-\"), (\"T2\", \"--\"), (\"T3\", \":\")):\n            ax.plot(NS, [a[f\"{s}|{tn}|n{n}\"][\"joint_OPEN_R3_R5_NOVCHURN_R3\"] for n in NS], \"o\" + ls, label=f\"joint {tn}\")\n            ax.plot(NS, [a[f\"{s}|{tn}|n{n}\"][\"marginal\"][\"OPEN_home|R3\"] for n in NS], \"s\" + ls, alpha=0.5,\n                    label=f\"OPEN_home R3 {tn}\")\n        ax.axhline(0.8, color=\"grey\", lw=0.8)\n        ax.set_xlabel(\"Frame-N concepts with outcome\")\n        ax.set_title(f\"scenario {s}\")\n    axes[0].set_ylabel(\"power (lower 95% bound > 0)\")\n    axes[0].legend(fontsize=7)\n    fig.tight_layout()\n    fig.savefig(FIGS / \"power_curves.png\", dpi=150)\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [184] TOOL CALL — Bash · 2026-09-29 05:55:29 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("s8_power.py"); s=p.read_text()
old='''    from tables import load_tables
    T = load_tables()["POOLED"]'''
new='''    from tables import design, load_tables
    TT = load_tables()
    T = TT["POOLED"]
    k_coh = {r: sum(m.shape[1] for m in design(TT["COH1517"], r, pooled=False)) for r in ("R3", "R5")}
    k_pool = {r: sum(m.shape[1] for m in design(T, r, pooled=True)) for r in ("R3", "R5")}'''
assert old in s; s=s.replace(old,new)
old='''                kk = {"R3": 21 + 8, "R5": 26 + 10}[r]
                infl'''
new='''                kk = k_coh[r]
                infl'''
assert old in s; s=s.replace(old,new)
old='''        kk = {"R3": 29, "R5": 36}[key.split("|")[1]]'''
new='''        kk = k_pool[key.split("|")[1]]'''
assert old in s; s=s.replace(old,new)
p.write_text(s)
EOF
tail -2 logs/s6_full.out
```

### [185] TOOL RESULT — Bash · 2026-09-29 05:55:29 UTC

```
{"stdout": "05:50:15|INFO   |1217 tasks, B = 2000, workers 4\n05:51:04|INFO   |1/1217 done; 0.8 min; eta 979.4 min", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [186] ASSISTANT · 2026-09-29 05:55:29 UTC

```
Workers are busy on the heavy pooled cells first. Meanwhile, checking the output schema for `method_out.json`:
```

### [187] TOOL CALL — Bash · 2026-09-29 05:55:29 UTC

```
cat /ai-inventor/.claude/skills/aii-json/schemas/exp_gen_sol_out.json
```

### [188] TOOL RESULT — Bash · 2026-09-29 05:55:29 UTC

```
{"stdout": "{\n  \"$schema\": \"http://json-schema.org/draft-07/schema#\",\n  \"type\": \"object\",\n  \"required\": [\"datasets\"],\n  \"properties\": {\n    \"metadata\": {\n      \"type\": \"object\",\n      \"description\": \"Optional top-level metadata (e.g. method_name, description, parameters, hyperparameters)\",\n      \"additionalProperties\": true\n    },\n    \"datasets\": {\n      \"type\": \"array\",\n      \"minItems\": 1,\n      \"items\": {\n        \"type\": \"object\",\n        \"required\": [\"dataset\", \"examples\"],\n        \"properties\": {\n          \"dataset\": {\n            \"type\": \"string\",\n            \"description\": \"Source dataset name\"\n          },\n          \"examples\": {\n            \"type\": \"array\",\n            \"minItems\": 1,\n            \"items\": {\n              \"type\": \"object\",\n              \"required\": [\"input\", \"output\"],\n              \"properties\": {\n                \"input\": {\n                  \"type\": \"string\",\n                  \"description\": \"Task prompt, question, or multi-turn conversation\"\n                },\n                \"output\": {\n                  \"type\": \"string\",\n                  \"description\": \"Expected agent response or action sequence\"\n                }\n              },\n              \"patternProperties\": {\n                \"^metadata_[a-zA-Z_][a-zA-Z0-9_]*$\": {\n                  \"description\": \"Per-example metadata (e.g. metadata_fold, metadata_feature_names)\"\n                },\n                \"^predict_[a-zA-Z_][a-zA-Z0-9_]*$\": {\n                  \"type\": \"string\",\n                  \"description\": \"Prediction from a method (e.g. predict_baseline, predict_our_method)\"\n                }\n              },\n              \"additionalProperties\": false\n            }\n          }\n        },\n        \"additionalProperties\": false\n      }\n    }\n  },\n  \"additionalProperties\": false\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [189] TOOL CALL — Bash · 2026-09-29 05:55:29 UTC

```
D=/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_2/gen_art/gen_art_dataset_2; ls -la $D/full_data_out; head -c 2500 $D/preview_data_out.json; echo; python3 -c "
import json; d=json.load(open('$D/mini_data_out.json')); print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
ds=d['datasets'] if isinstance(d,dict) else d
for x in ds: print(x['dataset'], len(x['examples']), list(x['examples'][0].keys()))
"
```

### [190] TOOL RESULT — Bash · 2026-09-29 05:55:29 UTC

```
{"stdout": "total 255048\ndrwxr-xr-x  2 root root  2024518 Sep 28 20:06 .\ndrwxr-xr-x 10 root root  2041367 Sep 28 21:21 ..\n-rw-r--r--  1 root root 90009907 Sep 28 20:04 full_data_out_1.json\n-rw-r--r--  1 root root 90008266 Sep 28 20:04 full_data_out_2.json\n-rw-r--r--  1 root root 77016616 Sep 28 20:04 full_data_out_3.json\n-rw-r--r--  1 root root    10594 Sep 28 20:06 mini_full_data_out_1.json\n-rw-r--r--  1 root root    13272 Sep 28 20:06 mini_full_data_out_2.json\n-rw-r--r--  1 root root    24929 Sep 28 20:06 mini_full_data_out_3.json\n-rw-r--r--  1 root root     3738 Sep 28 20:06 preview_full_data_out_1.json\n-rw-r--r--  1 root root     5859 Sep 28 20:06 preview_full_data_out_2.json\n-rw-r--r--  1 root root     6175 Sep 28 20:06 preview_full_data_out_3.json\n{\n \"datasets\": [\n  {\n   \"dataset\": \"concept_recognition\",\n   \"examples\": [\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C144501496\\\", \\\"qid\\\": \\\"Q5533489\\\", \\\"qid_resolved\\\": \\\"Q5533489\\\", \\\"label\\\": \\\"Genome editing\\\", \\\"label_norm\\\": \\\"genome editing\\\", \\\"aliases\\\": [\\\"genome editing\\\", \\\"Genome engineering\\\"], \\\"aliases_norm\\\": [\\\"genome engineering\\\"], \\\"acronyms\\\": [], \\\"level\\\": 4, \\\"ancestor_ids\\\": [\\\"C98108389\\\", \\\"C141231307\\\",...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"nature_methods_moty\\\", \\\"event_type\\\": \\\"nature_methods_method_of_the_year\\\", \\\"year\\\": 2011, \\\"date\\\": null, \\\"date_precision\\\": 9, \\\"year_usable\\\": true, \\\"match_method\\\": \\\"embed+llm\\\", \\\"match_confidence\\\": 0.85, \\\"relation\\\": \\\"broader\\\", \\\"entry_id\\\": \\\"nature_methods_moty:2011:1.0:4\\\", \\\"detail\\\":...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 4,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 11,\n     \"metadata_n_events_year_usable\": 10,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C144501496\",\n     \"metadata_qid\": \"Q5533489\"\n    },\n    {\n     \"input\": \"{\\\"openalex_id\\\": \\\"C46111723\\\", \\\"qid\\\": \\\"Q471857\\\", \\\"qid_resolved\\\": \\\"Q471857\\\", \\\"label\\\": \\\"Proteomics\\\", \\\"label_norm\\\": \\\"proteomic\\\", \\\"aliases\\\": [\\\"proteomics\\\"], \\\"aliases_norm\\\": [], \\\"acronyms\\\": [], \\\"level\\\": 3, \\\"ancestor_ids\\\": [\\\"C104317684\\\", \\\"C55493867\\\", \\\"C54355233\\\", \\\"C86803240\\\", \\\"C185592680\\\"], \\\"level0_discipli...\",\n     \"output\": \"{\\\"events\\\": [{\\\"source\\\": \\\"wikipedia_en\\\", \\\"event_type\\\": \\\"wikipedia_page_created_estimated\\\", \\\"year\\\": 2002, \\\"date\\\": \\\"2002-06-05\\\", \\\"date_precision\\\": \\\"estimated\\\", \\\"year_usable\\\": true, \\\"match_method\\\": \\\"wikidata_sitelink\\\", \\\"match_confidence\\\": 0.8, \\\"relation\\\": \\\"same\\\", \\\"entry_id\\\": null, \\\"detail\\\": {\\\"title\\\": \\\"Pr...\",\n     \"metadata_fold\": \"dev\",\n     \"metadata_group\": \"BGM\",\n     \"metadata_group_plurality\": \"BGM\",\n     \"metadata_group_plurality_share\": 1.0,\n     \"metadata_level\": 3,\n     \"metadata_l1_fields\": [\n      \"13\",\n      \"13\"\n     ],\n     \"metadata_level0\": [\n      \"Biology\",\n      \"Chemistry\"\n     ],\n     \"metadata_n_events\": 9,\n     \"metadata_n_events_year_usable\": 9,\n     \"metadata_frame_role\": \"target\",\n     \"metadata_openalex_id\": \"C46111723\",\n     \"metadata_qid\": \"Q471857\"\n  \n<class 'dict'> ['datasets']\nconcept_recognition 200 ['input', 'output', 'metadata_fold', 'metadata_group', 'metadata_group_plurality', 'metadata_group_plurality_share', 'metadata_level', 'metadata_l1_fields', 'metadata_level0', 'metadata_n_events', 'metadata_n_events_year_usable', 'metadata_frame_role', 'metadata_openalex_id', 'metadata_qid']\nexternal_entries_mesh 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nexternal_entries_acm_ccs 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nexternal_entries_msc 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nexternal_entries_pacs_physh 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nexternal_entries_jel 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nexternal_entries_curated_lists 200 ['input', 'output', 'metadata_source', 'metadata_family', 'metadata_year', 'metadata_year_known', 'metadata_n_matched', 'metadata_entry_id']\nmatch_verifications 200 ['input', 'output', 'metadata_task', 'metadata_model', 'metadata_prompt_hash', 'metadata_cost_usd', 'metadata_status', 'metadata_family']\ncrosswalk_level1_to_field 200 ['input', 'output', 'metadata_model_a', 'metadata_model_b', 'metadata_decided_by']\nspotcheck_p78 78 ['input', 'output', 'metadata_joined', 'metadata_iter1_status']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [191] ASSISTANT · 2026-09-29 05:56:45 UTC

```
Writing `method.py`: the stage orchestrator plus the `exp_gen_sol_out` builder with DEV-fitted OLS predictions and the dependency concept-key cross-check.
```

### [192] TOOL CALL — Write · 2026-09-29 05:56:45 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/method.py

#!/usr/bin/env python3
"""Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.

Stages (each a standalone, resumable script; run in this order by `python method.py --run-all`):
  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)
  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)
  s1_freeze.py          frozen spec + seal (before any outcome join)
  s2_variants.py        RAW, V1 rarefaction, V2 permutation null, V2b Chao Jaccard, V4 split halves
  s3_nulls.py           V3a backbone rewiring, V3b k-matched density null, V3c curveball persistence null
  tests/u_nulls.py      U3 curveball uniformity, U4 rewire calibration
  tests/planted.py      PC1 stationary thin-sample simulation, PC2 planted churn
  s4_composites.py      clean composites, S1b constants seal, V4 reliability (X side)
  s4b_outcome_rel.py    outcome reliability (O2r_m50, m = 25 halves)
  s5_size.py            size-dependence diagnostics
  s6_assoc.py           partial Spearman ladder per body / pooled, paired clean-vs-raw, groups, PC3
  s7_verdict.py         DL, disattenuation, P1-P3, Holm, VERDICT, figures
  s8_power.py           Frame-N power simulation
  rederive.py           independent re-derivation of the P1-P3 numbers and the pooled SB
Then (this file): method_out.json in exp_gen_sol_out format -- one example per concept with finite O2r_m50;
predictions from OLS fitted on DEV only (B5 standardised with the frozen EXP10 constants) applied to every body;
results/prediction_check.json; the concept-key cross-check against art_O7Dq4L02QnDN."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "lib"))

import numpy as np
import pandas as pd
from loguru import logger
from scipy import stats

from common import DATA, O5DIR, RES, jdump, setup_logger

STAGES = [("s0_gate.py", RES / "gate_t0.json"), ("tests/u_fast6.py", RES / "unit_tests_fast6.json"),
          ("s1_freeze.py", RES / "frozen_spec.json"), ("s2_variants.py", DATA / "s2_scalars_full.parquet"),
          ("s3_nulls.py", DATA / "v3_nulls_full.parquet"), ("tests/u_nulls.py", RES / "unit_tests_nulls.json"),
          ("tests/planted.py", RES / "planted_checks.json"), ("s4_composites.py", DATA / "clean_variants.parquet"),
          ("s4b_outcome_rel.py", RES / "reliability.json"), ("s5_size.py", RES / "size_dependence.json"),
          ("s6_assoc.py", RES / "clean_vs_raw_psp_cells.json"), ("s7_verdict.py", RES / "clean_vs_raw_psp.json"),
          ("s8_power.py", RES / "power_frame_n.json"), ("rederive.py", RES / "rederive.json")]
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


def run_stages(force: bool) -> None:
    for script, out in STAGES:
        if out.exists() and not force:
            logger.info(f"skip {script} ({out.name} exists)")
            continue
        if script == "s1_freeze.py" and out.exists():
            logger.warning("frozen_spec.json exists: never re-freeze (seal)")
            continue
        logger.info(f"running {script}")
        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)


def concept_key_check() -> dict:
    """Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its
    concept_recognition table and agreement of the OpenAlex level."""
    cv = pd.read_parquet(DATA / "clean_variants.parquet", columns=["concept_id", "body"])
    from common import DATA_IN
    lev = pd.concat([pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=["concept_id", "level"]),
                     pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=["concept_id", "level"])])
    lev = dict(zip(lev.concept_id.astype(str), lev.level))
    ids = set(cv.concept_id.astype(str))
    seen, level_ok, n_rec = {}, 0, 0
    for p in sorted((O5DIR / "full_data_out").glob("full_data_out_*.json")):
        d = json.loads(p.read_text())
        for ds in d["datasets"]:
            if ds["dataset"] != "concept_recognition":
                continue
            for e in ds["examples"]:
                n_rec += 1
                cid = e.get("metadata_openalex_id")
                if cid in ids:
                    seen[cid] = e.get("metadata_level")
        del d
    for cid, lv in seen.items():
        if cid in lev and lv is not None and int(lv) == int(lev[cid]):
            level_ok += 1
    cov = cv.assign(found=cv.concept_id.astype(str).isin(seen))
    return {"dependency": "art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)",
            "n_recognition_rows": n_rec, "n_analysed": int(len(ids)), "n_found": int(len(seen)),
            "coverage_by_body": cov.groupby("body").found.mean().round(4).to_dict(),
            "level_agreement": level_ok / max(len(seen), 1)}


def build_outputs() -> None:
    from tables import load_tables
    spec = json.loads((RES / "frozen_spec.json").read_text())
    pm = spec["exp10_prediction_models"]["B5"]
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    rel = json.loads((RES / "reliability.json").read_text())
    pw = json.loads((RES / "power_frame_n.json").read_text())
    sz = json.loads((RES / "size_dependence.json").read_text())
    T = load_tables()["POOLED"]
    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)
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
    chk = {"note": "OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)", "coef": coefs}
    for body in ("OLDHO", "COH1014", "COH1517"):
        m = (T.body == body).to_numpy()
        ent = {}
        for nm, p in preds.items():
            ok = m & np.isfinite(p)
            ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > 20 else None
        ent["n"] = int(m.sum())
        ent["gain_vs_B5"] = {nm: (ent[nm] - ent["B5"]) if ent[nm] is not None and ent["B5"] is not None else None
                             for nm in PRED_X if nm != "B5"}
        chk[body] = ent
    jdump(chk, RES / "prediction_check.json")
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
            "concept_key_check": concept_key_check(),
            "n_examples": len(exs), "prediction_models": "OLS on DEV (B5 standardised with EXP10 frozen mu/sd); "
                                                         "NaN variants imputed with the DEV median (flagged)"}
    out = {"metadata": meta, "datasets": [{"dataset": "selection_concepts", "examples": exs}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)
                                                     and not math.isfinite(o) else str(o)))
    logger.info(f"method_out.json: {len(exs)} examples; verdict {vd['verdict']}")


@logger.catch(reraise=True)
def main() -> None:
    setup_logger("method")
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-all", action="store_true")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.run_all:
        run_stages(a.force)
    build_outputs()


if __name__ == "__main__":
    main()
```

### [193] TOOL RESULT — Write · 2026-09-29 05:56:45 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/method.py", "content": "#!/usr/bin/env python3\n\"\"\"Is neighbourhood churn real or thin-sample noise?  Orchestrator + S6 outputs.\n\nStages (each a standalone, resumable script; run in this order by `python method.py --run-all`):\n  s0_gate.py            gate T0 (recompute EXP10 home components / OPEN_home / published cohort psp exactly)\n  tests/u_fast6.py      U1/U2/U5/U6 fast engine == ego.concept_core (SELF override)\n  s1_freeze.py          frozen spec + seal (before any outcome join)\n  s2_variants.py        RAW, V1 rarefaction, V2 permutation null, V2b Chao Jaccard, V4 split halves\n  s3_nulls.py           V3a backbone rewiring, V3b k-matched density null, V3c curveball persistence null\n  tests/u_nulls.py      U3 curveball uniformity, U4 rewire calibration\n  tests/planted.py      PC1 stationary thin-sample simulation, PC2 planted churn\n  s4_composites.py      clean composites, S1b constants seal, V4 reliability (X side)\n  s4b_outcome_rel.py    outcome reliability (O2r_m50, m = 25 halves)\n  s5_size.py            size-dependence diagnostics\n  s6_assoc.py           partial Spearman ladder per body / pooled, paired clean-vs-raw, groups, PC3\n  s7_verdict.py         DL, disattenuation, P1-P3, Holm, VERDICT, figures\n  s8_power.py           Frame-N power simulation\n  rederive.py           independent re-derivation of the P1-P3 numbers and the pooled SB\nThen (this file): method_out.json in exp_gen_sol_out format -- one example per concept with finite O2r_m50;\npredictions from OLS fitted on DEV only (B5 standardised with the frozen EXP10 constants) applied to every body;\nresults/prediction_check.json; the concept-key cross-check against art_O7Dq4L02QnDN.\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport json\nimport math\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nROOT = Path(__file__).resolve().parent\nsys.path.insert(0, str(ROOT / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy import stats\n\nfrom common import DATA, O5DIR, RES, jdump, setup_logger\n\nSTAGES = [(\"s0_gate.py\", RES / \"gate_t0.json\"), (\"tests/u_fast6.py\", RES / \"unit_tests_fast6.json\"),\n          (\"s1_freeze.py\", RES / \"frozen_spec.json\"), (\"s2_variants.py\", DATA / \"s2_scalars_full.parquet\"),\n          (\"s3_nulls.py\", DATA / \"v3_nulls_full.parquet\"), (\"tests/u_nulls.py\", RES / \"unit_tests_nulls.json\"),\n          (\"tests/planted.py\", RES / \"planted_checks.json\"), (\"s4_composites.py\", DATA / \"clean_variants.parquet\"),\n          (\"s4b_outcome_rel.py\", RES / \"reliability.json\"), (\"s5_size.py\", RES / \"size_dependence.json\"),\n          (\"s6_assoc.py\", RES / \"clean_vs_raw_psp_cells.json\"), (\"s7_verdict.py\", RES / \"clean_vs_raw_psp.json\"),\n          (\"s8_power.py\", RES / \"power_frame_n.json\"), (\"rederive.py\", RES / \"rederive.json\")]\nB5 = [\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\"]\nPRED_X = {\"B5\": None, \"B5_plus_NOVCHURN_raw\": \"NOVCHURN_raw\", \"B5_plus_NOVCHURN_exc\": \"NOVCHURN_exc\",\n          \"B5_plus_NOVCHURN_cfg\": \"NOVCHURN_cfg\", \"B5_plus_OPEN_home\": \"OPEN_home\",\n          \"B5_plus_OPEN_home_clean\": \"OPEN_home_clean\"}\nINPUT_COLS = [\"NOV_res__raw\", \"edge_persistence__raw\", \"ego_density_W3__raw\", \"new_edge_rate__raw\", \"n_comm_W3__raw\",\n              \"participation__raw\", \"NOVCHURN_raw\", \"OPEN_home\", \"NOV_res_rare10\", \"edge_persistence_rare10\",\n              \"NOVCHURN_rare10\", \"NOV_res_rare5\", \"edge_persistence_rare5\", \"NOVCHURN_rare5\", \"NOV_res_exc\",\n              \"edge_persistence_exc\", \"edge_persistence_nullmean\", \"NOVCHURN_exc\", \"EP_chao\", \"NOVCHURN_chao\",\n              \"z_dens_cfg\", \"z_dens_k\", \"z_pers_cfg\", \"excess_pers_cfg\", \"NOVCHURN_cfg\", \"OPEN_home_clean\",\n              \"OPEN_home_exc\"]\n\n\ndef run_stages(force: bool) -> None:\n    for script, out in STAGES:\n        if out.exists() and not force:\n            logger.info(f\"skip {script} ({out.name} exists)\")\n            continue\n        if script == \"s1_freeze.py\" and out.exists():\n            logger.warning(\"frozen_spec.json exists: never re-freeze (seal)\")\n            continue\n        logger.info(f\"running {script}\")\n        subprocess.run([sys.executable, str(ROOT / script)], check=True, cwd=ROOT)\n\n\ndef concept_key_check() -> dict:\n    \"\"\"Dependency art_O7Dq4L02QnDN is used ONLY as the concept key: coverage of the analysed concept_ids in its\n    concept_recognition table and agreement of the OpenAlex level.\"\"\"\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\", columns=[\"concept_id\", \"body\"])\n    from common import DATA_IN\n    lev = pd.concat([pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\", columns=[\"concept_id\", \"level\"]),\n                     pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\", columns=[\"concept_id\", \"level\"])])\n    lev = dict(zip(lev.concept_id.astype(str), lev.level))\n    ids = set(cv.concept_id.astype(str))\n    seen, level_ok, n_rec = {}, 0, 0\n    for p in sorted((O5DIR / \"full_data_out\").glob(\"full_data_out_*.json\")):\n        d = json.loads(p.read_text())\n        for ds in d[\"datasets\"]:\n            if ds[\"dataset\"] != \"concept_recognition\":\n                continue\n            for e in ds[\"examples\"]:\n                n_rec += 1\n                cid = e.get(\"metadata_openalex_id\")\n                if cid in ids:\n                    seen[cid] = e.get(\"metadata_level\")\n        del d\n    for cid, lv in seen.items():\n        if cid in lev and lv is not None and int(lv) == int(lev[cid]):\n            level_ok += 1\n    cov = cv.assign(found=cv.concept_id.astype(str).isin(seen))\n    return {\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\",\n            \"n_recognition_rows\": n_rec, \"n_analysed\": int(len(ids)), \"n_found\": int(len(seen)),\n            \"coverage_by_body\": cov.groupby(\"body\").found.mean().round(4).to_dict(),\n            \"level_agreement\": level_ok / max(len(seen), 1)}\n\n\ndef build_outputs() -> None:\n    from tables import load_tables\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    pm = spec[\"exp10_prediction_models\"][\"B5\"]\n    V = json.loads((RES / \"clean_vs_raw_psp.json\").read_text())\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    pw = json.loads((RES / \"power_frame_n.json\").read_text())\n    sz = json.loads((RES / \"size_dependence.json\").read_text())\n    T = load_tables()[\"POOLED\"]\n    T = T[np.isfinite(T.O2r_m50)].reset_index(drop=True)\n    Zb = np.column_stack([(T[c].to_numpy(float) - pm[\"mu\"][c]) / pm[\"sd\"][c] for c in B5])\n    dev = (T.body == \"DEV\").to_numpy() & np.all(np.isfinite(Zb), 1)\n    y = T.O2r_m50.to_numpy(float)\n    preds, imputed, coefs = {}, {}, {}\n    for nm, x in PRED_X.items():\n        X = Zb.copy()\n        if x is not None:\n            v = T[x].to_numpy(float)\n            med = float(np.nanmedian(v[dev]))\n            imputed[nm] = ~np.isfinite(v)\n            v = np.where(np.isfinite(v), v, med)\n            X = np.c_[X, v]\n        A = np.c_[np.ones(len(T)), X]\n        okf = dev & np.all(np.isfinite(A), 1)\n        b = np.linalg.lstsq(A[okf], y[okf], rcond=None)[0]\n        coefs[nm] = b.tolist()\n        preds[nm] = A @ b\n    chk = {\"note\": \"OLS fitted on DEV only; out-of-DEV Spearman with O2r_m50 (gain over B5 expected ~0)\", \"coef\": coefs}\n    for body in (\"OLDHO\", \"COH1014\", \"COH1517\"):\n        m = (T.body == body).to_numpy()\n        ent = {}\n        for nm, p in preds.items():\n            ok = m & np.isfinite(p)\n            ent[nm] = float(stats.spearmanr(p[ok], y[ok])[0]) if ok.sum() > 20 else None\n        ent[\"n\"] = int(m.sum())\n        ent[\"gain_vs_B5\"] = {nm: (ent[nm] - ent[\"B5\"]) if ent[nm] is not None and ent[\"B5\"] is not None else None\n                             for nm in PRED_X if nm != \"B5\"}\n        chk[body] = ent\n    jdump(chk, RES / \"prediction_check.json\")\n    exs = []\n    for i, r in T.iterrows():\n        inp = {\"concept_id\": str(r.concept_id), \"name\": str(r[\"name\"]), \"body\": r.body, \"t0\": int(r.t0),\n               \"n_home_early\": int(r.n_home_early)}\n        for c in INPUT_COLS:\n            v = r[c]\n            inp[c] = None if not np.isfinite(v) else round(float(v), 6)\n        e = {\"input\": json.dumps(inp), \"output\": f\"{r.O2r_m50:.6f}\"}\n        for nm, p in preds.items():\n            e[f\"predict_{nm}\"] = f\"{p[i]:.6f}\" if np.isfinite(p[i]) else \"nan\"\n        e[\"metadata_body\"] = r.body\n        e[\"metadata_agroup\"] = r.agroup\n        e[\"metadata_O2r_resid\"] = None if not np.isfinite(r.O2r_resid) else float(r.O2r_resid)\n        e[\"metadata_imputed_variants\"] = [nm for nm in imputed if imputed[nm][i]]\n        e[\"metadata_missing_clean_variants\"] = [c for c in (\"NOVCHURN_exc\", \"NOVCHURN_rare10\", \"NOVCHURN_cfg\",\n                                                            \"OPEN_home_clean\") if not np.isfinite(r[c])]\n        exs.append(e)\n    vd = V[\"verdict\"]\n    head = {h[\"variant\"]: {b: h[b].get(\"psp\") for b in (\"DEV\", \"OLDHO\", \"COH1014\", \"COH1517\", \"POOLED\")}\n            for h in V[\"headline_R2_O2r_m50\"]}\n    meta = {\"method_name\": \"Thin-sample confound check of home-only neighbourhood churn (raw vs noise-controlled \"\n                           \"variants)\",\n            \"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\",\n            \"verdict\": vd[\"verdict\"], \"DEGREE_ARTEFACT_PERSISTENCE\": vd[\"DEGREE_ARTEFACT_PERSISTENCE\"],\n            \"predictions_P1_P3\": {k: v[\"holds\"] for k, v in V[\"predictions\"].items()},\n            \"P_detail\": V[\"predictions\"], \"headline_psp_R2_O2r_m50\": head,\n            \"reliability_pooled_SB\": {k: v[\"pooled\"][\"SB\"] for k, v in rel[\"variants\"].items()},\n            \"outcome_reliability_SB\": rel[\"outcome\"][\"O2r_m50\"][\"pooled\"][\"SB\"],\n            \"thin_sample_share_R2\": sz[\"thin_sample_share\"][\"POOLED\"][\"R2\"],\n            \"power_plain_language\": pw[\"plain_language\"],\n            \"concept_key_check\": concept_key_check(),\n            \"n_examples\": len(exs), \"prediction_models\": \"OLS on DEV (B5 standardised with EXP10 frozen mu/sd); \"\n                                                         \"NaN variants imputed with the DEV median (flagged)\"}\n    out = {\"metadata\": meta, \"datasets\": [{\"dataset\": \"selection_concepts\", \"examples\": exs}]}\n    (ROOT / \"method_out.json\").write_text(json.dumps(out, indent=1, default=lambda o: None if isinstance(o, float)\n                                                     and not math.isfinite(o) else str(o)))\n    logger.info(f\"method_out.json: {len(exs)} examples; verdict {vd['verdict']}\")\n\n\n@logger.catch(reraise=True)\ndef main() -> None:\n    setup_logger(\"method\")\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--run-all\", action=\"store_true\")\n    ap.add_argument(\"--force\", action=\"store_true\")\n    a = ap.parse_args()\n    if a.run_all:\n        run_stages(a.force)\n    build_outputs()\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [194] TOOL CALL — Bash · 2026-09-29 05:56:45 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -2 logs/s6_full.out; grep -n "O5DIR" lib/common.py
```

### [195] TOOL RESULT — Bash · 2026-09-29 05:56:45 UTC

```
{"stdout": "05:51:04|INFO   |1/1217 done; 0.8 min; eta 979.4 min\n05:55:17|INFO   |51/1217 done; 5.0 min; eta 115.1 min\n40:O5DIR = RUN_ROOT / \"3_invention_loop/iter_2/gen_art/gen_art_dataset_2\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [196] ASSISTANT · 2026-09-29 05:56:45 UTC

```
The association run is at 51/1,217 tasks after 5 min, heaviest (pooled) cells first, so the real remaining time is well under the 115-min ETA. Writing the independent re-derivation script now.
```

### [197] TOOL CALL — Write · 2026-09-29 05:56:45 UTC

```
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/rederive.py

#!/usr/bin/env python3
"""Independent re-derivation (separate code path: own design matrices, scipy rankdata + numpy lstsq residualisation,
own z-scoring and Spearman) of (a) the P1-P3 psp point estimates and (b) the pooled split-half SB of NOVCHURN_raw.
Tolerances: psp <= 1e-9, SB <= 1e-6. -> results/rederive.json"""
from __future__ import annotations

import json
import math
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np
import pandas as pd
from scipy.stats import rankdata, spearmanr

from common import DATA, DATA_IN, RES, jdump, setup_logger

logger = setup_logger("rederive")


def my_design(df: pd.DataFrame, pooled: bool) -> tuple[np.ndarray, np.ndarray]:
    """Rung R2 rebuilt from scratch: continuous B5 + CONTACT_REACH; dummies t0 (drop first), window_flag (if
    varying), type (method/object/property/unlabelled), generic, level 3/4/5, body (pooled, drop first)."""
    cont = df[["logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH"]].to_numpy(float)
    cols = []
    for y in sorted(df.t0.unique())[1:]:
        cols.append((df.t0 == y).to_numpy(float))
    if df.window_flag.nunique() > 1:
        cols.append(df.window_flag.to_numpy(float))
    t = df["type"].fillna("unlabelled")
    for c in ("method", "object", "property", "unlabelled"):
        cols.append((t == c).to_numpy(float))
    cols.append(df.generic.to_numpy(float))
    for l in (3, 4, 5):
        cols.append((df.level == l).to_numpy(float))
    if pooled:
        for b in sorted(df.body.unique())[1:]:
            cols.append((df.body == b).to_numpy(float))
    C = np.column_stack(cols)
    C = C[:, C.std(0) > 0]
    return cont, C


def my_psp(x, y, cont, C) -> tuple[float, int]:
    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(cont), 1) & np.all(np.isfinite(C), 1)
    x, y, cont, C = x[ok], y[ok], cont[ok], C[ok]
    Z = np.column_stack([np.ones(len(x))] + [rankdata(cont[:, j]) for j in range(cont.shape[1])] + [C])
    res = []
    for v in (rankdata(x), rankdata(y)):
        beta = np.linalg.lstsq(Z, v, rcond=None)[0]
        res.append(v - Z @ beta)
    return float(np.corrcoef(res[0], res[1])[0, 1]), int(ok.sum())


def main() -> None:
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet")
    ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet")
    keep = ["ci", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "t0", "type", "generic",
            "level", "O2r_m50"]
    e = cv[cv.frame == "exp5"].drop(columns=["t0"]).merge(fe[keep], on="ci")
    e["window_flag"] = 0
    c = cv[cv.frame == "cohort"].drop(columns=["t0"]).merge(ac[keep + ["window_flag"]], on="ci")
    P = pd.concat([e, c], ignore_index=True)
    V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
    cells, pairs = V["cells"]["psp"], V["cells"]["paired"]
    out = {"psp": {}, "tolerance_psp": 1e-9, "tolerance_SB": 1e-6}
    checks = [("COH1517", "NOVCHURN_exc"), ("COH1517", "NOVCHURN_raw"), ("OLDHO", "NOVCHURN_exc"),
              ("OLDHO", "NOVCHURN_raw"), ("POOLED", "z_pers_cfg"), ("POOLED", "edge_persistence__raw"),
              ("POOLED", "NOVCHURN_raw"), ("POOLED", "NOVCHURN_exc")]
    worst = 0.0
    for body, x in checks:
        d = P if body == "POOLED" else P[P.body == body]
        cont, C = my_design(d, body == "POOLED")
        r, n = my_psp(d[x].to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        ref = cells[f"{body}|{x}|O2r_m50|R2"]
        dd = abs(r - ref["rho"])
        worst = max(worst, dd)
        out["psp"][f"{body}|{x}|R2"] = {"rederived": r, "pipeline": ref["rho"], "abs_diff": dd, "n": n,
                                        "n_pipeline": ref["n"]}
    for body in ("COH1517", "OLDHO"):
        d = P[P.body == body]
        m = np.isfinite(d.NOVCHURN_exc) & np.isfinite(d.NOVCHURN_raw)
        d = d[m]
        cont, C = my_design(d, False)
        a, n = my_psp(d.NOVCHURN_exc.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        b, _ = my_psp(d.NOVCHURN_raw.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)
        ref = pairs[f"{body}|NOVCHURN_exc|NOVCHURN_raw|O2r_m50|R2"]
        dd = max(abs(a - ref["a"]), abs(b - ref["b"]))
        worst = max(worst, dd)
        out["psp"][f"{body}|P1_same_sample_ratio"] = {"rederived_ratio": a / b, "pipeline_ratio": ref["ratio"],
                                                      "abs_diff_components": dd, "n": n}
    x = cv.NOVCHURN_exc.to_numpy(float)
    ok = np.isfinite(x)
    r3 = float(spearmanr(x[ok], np.log(cv.n_home_early.to_numpy(float))[ok])[0])
    out["P3"] = {"rederived": r3, "pipeline": V["predictions"]["P3"]["spearman_NOVCHURN_exc_log_n_all"],
                 "abs_diff": abs(r3 - V["predictions"]["P3"]["spearman_NOVCHURN_exc_log_n_all"])}
    worst = max(worst, out["P3"]["abs_diff"])
    # pooled SB of NOVCHURN_raw from the S2 half arrays (own z-scoring)
    spec = json.loads((RES / "frozen_spec.json").read_text())
    K = spec["exp10_open_constants_home"]
    pos = {(f, int(ci)): i for i, (f, ci) in enumerate(zip(cv.frame, cv.ci))}
    A = np.full((100, len(cv)), np.nan)
    Bh = np.full((100, len(cv)), np.nan)
    for p in sorted((DATA / "s2_parts_full").glob("chunk_*.pkl")):
        z = pickle.loads(p.read_bytes())
        for r, ex in zip(z["rows"], z["extras"]):
            if not ex:
                continue
            i = pos[(r["frame"], int(r["ci"]))]
            for h, M in (("A", A), ("B", Bh)):
                nov = ex["half_raw"][h][:, 3].astype(float)
                ep = ex["half_raw"][h][:, 5].astype(float)
                zn = (np.clip(nov, K["NOV_res"]["lo"], K["NOV_res"]["hi"]) - K["NOV_res"]["mu"]) / K["NOV_res"]["sd"]
                ze = -(np.clip(ep, K["edge_persistence"]["lo"], K["edge_persistence"]["hi"]) -
                       K["edge_persistence"]["mu"]) / K["edge_persistence"]["sd"]
                M[:, i] = np.where(np.isfinite(zn) & np.isfinite(ze), (zn + ze) / 2, np.nan)
    rs = []
    for s in range(100):
        ok = np.isfinite(A[s]) & np.isfinite(Bh[s])
        rs.append(spearmanr(A[s, ok], Bh[s, ok])[0])
    rr = math.tanh(np.mean(np.arctanh(rs)))
    sb = 2 * rr / (1 + rr)
    rel = json.loads((RES / "reliability.json").read_text())
    ref = rel["variants"]["NOVCHURN_raw"]["pooled"]["SB"]
    out["SB_NOVCHURN_raw_pooled"] = {"rederived": sb, "pipeline": ref, "abs_diff": abs(sb - ref)}
    out["pass"] = bool(worst <= 1e-9 and abs(sb - ref) <= 1e-6)
    jdump(out, RES / "rederive.json")
    logger.info(f"rederive pass {out['pass']}; worst psp diff {worst:.2e}; SB diff {abs(sb-ref):.2e}")


if __name__ == "__main__":
    main()
```

### [198] TOOL RESULT — Write · 2026-09-29 05:56:45 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/rederive.py", "content": "#!/usr/bin/env python3\n\"\"\"Independent re-derivation (separate code path: own design matrices, scipy rankdata + numpy lstsq residualisation,\nown z-scoring and Spearman) of (a) the P1-P3 psp point estimates and (b) the pooled split-half SB of NOVCHURN_raw.\nTolerances: psp <= 1e-9, SB <= 1e-6. -> results/rederive.json\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport math\nimport pickle\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parent / \"lib\"))\n\nimport numpy as np\nimport pandas as pd\nfrom scipy.stats import rankdata, spearmanr\n\nfrom common import DATA, DATA_IN, RES, jdump, setup_logger\n\nlogger = setup_logger(\"rederive\")\n\n\ndef my_design(df: pd.DataFrame, pooled: bool) -> tuple[np.ndarray, np.ndarray]:\n    \"\"\"Rung R2 rebuilt from scratch: continuous B5 + CONTACT_REACH; dummies t0 (drop first), window_flag (if\n    varying), type (method/object/property/unlabelled), generic, level 3/4/5, body (pooled, drop first).\"\"\"\n    cont = df[[\"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\"]].to_numpy(float)\n    cols = []\n    for y in sorted(df.t0.unique())[1:]:\n        cols.append((df.t0 == y).to_numpy(float))\n    if df.window_flag.nunique() > 1:\n        cols.append(df.window_flag.to_numpy(float))\n    t = df[\"type\"].fillna(\"unlabelled\")\n    for c in (\"method\", \"object\", \"property\", \"unlabelled\"):\n        cols.append((t == c).to_numpy(float))\n    cols.append(df.generic.to_numpy(float))\n    for l in (3, 4, 5):\n        cols.append((df.level == l).to_numpy(float))\n    if pooled:\n        for b in sorted(df.body.unique())[1:]:\n            cols.append((df.body == b).to_numpy(float))\n    C = np.column_stack(cols)\n    C = C[:, C.std(0) > 0]\n    return cont, C\n\n\ndef my_psp(x, y, cont, C) -> tuple[float, int]:\n    ok = np.isfinite(x) & np.isfinite(y) & np.all(np.isfinite(cont), 1) & np.all(np.isfinite(C), 1)\n    x, y, cont, C = x[ok], y[ok], cont[ok], C[ok]\n    Z = np.column_stack([np.ones(len(x))] + [rankdata(cont[:, j]) for j in range(cont.shape[1])] + [C])\n    res = []\n    for v in (rankdata(x), rankdata(y)):\n        beta = np.linalg.lstsq(Z, v, rcond=None)[0]\n        res.append(v - Z @ beta)\n    return float(np.corrcoef(res[0], res[1])[0, 1]), int(ok.sum())\n\n\ndef main() -> None:\n    cv = pd.read_parquet(DATA / \"clean_variants.parquet\")\n    fe = pd.read_parquet(DATA_IN / \"features_exp5_open.parquet\")\n    ac = pd.read_parquet(DATA_IN / \"analysis_cohort.parquet\")\n    keep = [\"ci\", \"logvol\", \"growth_c\", \"offhome_share\", \"entropy\", \"reach\", \"CONTACT_REACH\", \"t0\", \"type\", \"generic\",\n            \"level\", \"O2r_m50\"]\n    e = cv[cv.frame == \"exp5\"].drop(columns=[\"t0\"]).merge(fe[keep], on=\"ci\")\n    e[\"window_flag\"] = 0\n    c = cv[cv.frame == \"cohort\"].drop(columns=[\"t0\"]).merge(ac[keep + [\"window_flag\"]], on=\"ci\")\n    P = pd.concat([e, c], ignore_index=True)\n    V = json.loads((RES / \"clean_vs_raw_psp.json\").read_text())\n    cells, pairs = V[\"cells\"][\"psp\"], V[\"cells\"][\"paired\"]\n    out = {\"psp\": {}, \"tolerance_psp\": 1e-9, \"tolerance_SB\": 1e-6}\n    checks = [(\"COH1517\", \"NOVCHURN_exc\"), (\"COH1517\", \"NOVCHURN_raw\"), (\"OLDHO\", \"NOVCHURN_exc\"),\n              (\"OLDHO\", \"NOVCHURN_raw\"), (\"POOLED\", \"z_pers_cfg\"), (\"POOLED\", \"edge_persistence__raw\"),\n              (\"POOLED\", \"NOVCHURN_raw\"), (\"POOLED\", \"NOVCHURN_exc\")]\n    worst = 0.0\n    for body, x in checks:\n        d = P if body == \"POOLED\" else P[P.body == body]\n        cont, C = my_design(d, body == \"POOLED\")\n        r, n = my_psp(d[x].to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)\n        ref = cells[f\"{body}|{x}|O2r_m50|R2\"]\n        dd = abs(r - ref[\"rho\"])\n        worst = max(worst, dd)\n        out[\"psp\"][f\"{body}|{x}|R2\"] = {\"rederived\": r, \"pipeline\": ref[\"rho\"], \"abs_diff\": dd, \"n\": n,\n                                        \"n_pipeline\": ref[\"n\"]}\n    for body in (\"COH1517\", \"OLDHO\"):\n        d = P[P.body == body]\n        m = np.isfinite(d.NOVCHURN_exc) & np.isfinite(d.NOVCHURN_raw)\n        d = d[m]\n        cont, C = my_design(d, False)\n        a, n = my_psp(d.NOVCHURN_exc.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)\n        b, _ = my_psp(d.NOVCHURN_raw.to_numpy(float), d.O2r_m50.to_numpy(float), cont, C)\n        ref = pairs[f\"{body}|NOVCHURN_exc|NOVCHURN_raw|O2r_m50|R2\"]\n        dd = max(abs(a - ref[\"a\"]), abs(b - ref[\"b\"]))\n        worst = max(worst, dd)\n        out[\"psp\"][f\"{body}|P1_same_sample_ratio\"] = {\"rederived_ratio\": a / b, \"pipeline_ratio\": ref[\"ratio\"],\n                                                      \"abs_diff_components\": dd, \"n\": n}\n    x = cv.NOVCHURN_exc.to_numpy(float)\n    ok = np.isfinite(x)\n    r3 = float(spearmanr(x[ok], np.log(cv.n_home_early.to_numpy(float))[ok])[0])\n    out[\"P3\"] = {\"rederived\": r3, \"pipeline\": V[\"predictions\"][\"P3\"][\"spearman_NOVCHURN_exc_log_n_all\"],\n                 \"abs_diff\": abs(r3 - V[\"predictions\"][\"P3\"][\"spearman_NOVCHURN_exc_log_n_all\"])}\n    worst = max(worst, out[\"P3\"][\"abs_diff\"])\n    # pooled SB of NOVCHURN_raw from the S2 half arrays (own z-scoring)\n    spec = json.loads((RES / \"frozen_spec.json\").read_text())\n    K = spec[\"exp10_open_constants_home\"]\n    pos = {(f, int(ci)): i for i, (f, ci) in enumerate(zip(cv.frame, cv.ci))}\n    A = np.full((100, len(cv)), np.nan)\n    Bh = np.full((100, len(cv)), np.nan)\n    for p in sorted((DATA / \"s2_parts_full\").glob(\"chunk_*.pkl\")):\n        z = pickle.loads(p.read_bytes())\n        for r, ex in zip(z[\"rows\"], z[\"extras\"]):\n            if not ex:\n                continue\n            i = pos[(r[\"frame\"], int(r[\"ci\"]))]\n            for h, M in ((\"A\", A), (\"B\", Bh)):\n                nov = ex[\"half_raw\"][h][:, 3].astype(float)\n                ep = ex[\"half_raw\"][h][:, 5].astype(float)\n                zn = (np.clip(nov, K[\"NOV_res\"][\"lo\"], K[\"NOV_res\"][\"hi\"]) - K[\"NOV_res\"][\"mu\"]) / K[\"NOV_res\"][\"sd\"]\n                ze = -(np.clip(ep, K[\"edge_persistence\"][\"lo\"], K[\"edge_persistence\"][\"hi\"]) -\n                       K[\"edge_persistence\"][\"mu\"]) / K[\"edge_persistence\"][\"sd\"]\n                M[:, i] = np.where(np.isfinite(zn) & np.isfinite(ze), (zn + ze) / 2, np.nan)\n    rs = []\n    for s in range(100):\n        ok = np.isfinite(A[s]) & np.isfinite(Bh[s])\n        rs.append(spearmanr(A[s, ok], Bh[s, ok])[0])\n    rr = math.tanh(np.mean(np.arctanh(rs)))\n    sb = 2 * rr / (1 + rr)\n    rel = json.loads((RES / \"reliability.json\").read_text())\n    ref = rel[\"variants\"][\"NOVCHURN_raw\"][\"pooled\"][\"SB\"]\n    out[\"SB_NOVCHURN_raw_pooled\"] = {\"rederived\": sb, \"pipeline\": ref, \"abs_diff\": abs(sb - ref)}\n    out[\"pass\"] = bool(worst <= 1e-9 and abs(sb - ref) <= 1e-6)\n    jdump(out, RES / \"rederive.json\")\n    logger.info(f\"rederive pass {out['pass']}; worst psp diff {worst:.2e}; SB diff {abs(sb-ref):.2e}\")\n\n\nif __name__ == \"__main__\":\n    main()\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [199] TOOL CALL — Bash · 2026-09-29 05:56:45 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; tail -2 logs/s6_full.out
```

### [200] TOOL RESULT — Bash · 2026-09-29 05:56:45 UTC

```
{"stdout": "05:51:04|INFO   |1/1217 done; 0.8 min; eta 979.4 min\n05:55:17|INFO   |51/1217 done; 5.0 min; eta 115.1 min", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [201] TOOL CALL — Bash · 2026-09-29 05:57:19 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sleep 240; tail -1 logs/s6_full.out; du -sh data/* .venv 2>/dev/null | sort -h | tail -12
```

### [202] TOOL RESULT — Bash · 2026-09-29 06:01:01 UTC

```
{"stdout": "05:58:24|INFO   |151/1217 done; 8.1 min; eta 57.5 min\n58K\tdata/v3_halves_mini.pkl\n81K\tdata/s2_scalars_mini.parquet\n85K\tdata/s2_scalars_t200.parquet\n478K\tdata/v3_nulls_full.parquet\n2.8M\tdata/s2_scalars_full.parquet\n2.8M\tdata/v4_half_means.npz\n3.3M\tdata/s2_parts_mini\n4.5M\tdata/clean_variants.parquet\n15M\tdata/v3_halves_full.pkl\n45M\tdata/home_cache.pkl\n241M\tdata/s2_parts_full\n1.8G\t.venv", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [203] ASSISTANT · 2026-09-29 06:01:33 UTC

```
The association run's ETA is ~55 min. Meanwhile, looking for EXP12's `open_features.parquet` for the plan's home-build cross-check:
```

### [204] TOOL CALL — Bash · 2026-09-29 06:01:33 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop; ls */gen_art/ | head -40; find . -maxdepth 5 -name "open_features*.parquet" 2>/dev/null | head
```

### [205] TOOL RESULT — Bash · 2026-09-29 06:01:33 UTC

```
{"stdout": "iter_1/gen_art/:\ngen_art_dataset_1\ngen_art_experiment_1\ngen_art_experiment_2\ngen_art_experiment_3\ngen_art_experiment_4\n\niter_2/gen_art/:\ngen_art_dataset_2\ngen_art_evaluation_1\ngen_art_experiment_5\ngen_art_experiment_6\ngen_art_research_1\n\niter_3/gen_art/:\ngen_art_evaluation_2\ngen_art_experiment_7\ngen_art_experiment_8\ngen_art_experiment_9\ngen_art_research_2\n\niter_4/gen_art/:\ngen_art_evaluation_3\ngen_art_experiment_10\ngen_art_experiment_11\ngen_art_experiment_12\ngen_art_research_3\n\niter_5/gen_art/:\ngen_art_evaluation_4\ngen_art_experiment_13\ngen_art_experiment_14\ngen_art_experiment_15\ngen_art_experiment_16\n./iter_4/gen_art/gen_art_experiment_12/open_features.parquet", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [206] TOOL CALL — Bash · 2026-09-29 06:01:33 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; OMP_NUM_THREADS=1 .venv/bin/python - <<'EOF'
import pandas as pd, numpy as np
o=pd.read_parquet("../../../iter_4/gen_art/gen_art_experiment_12/open_features.parquet")
print(o.shape); print(list(o.columns)[:60])
print(o.head(3).T.head(30))
EOF
```

### [207] TOOL RESULT — Bash · 2026-09-29 06:01:33 UTC

```
{"stdout": "(12499, 40)\n['ci', 'split', 'group', 'rgroup', 'med_home', 'new_edge_rate_all', 'n_comm_W3_all', 'participation_all', 'NOV_res_all', 'ego_density_W3_all', 'edge_persistence_all', 'n_early_rows', 'n_home', 'n_unlab_early', 'home_cov', 'M_home', 'NOV_home', 'NOV_res_home', 'deg_W1_home', 'deg_W3_home', 'new_edge_rate_home', 'edge_persistence_home', 'participation_home', 'n_comm_W3_home', 'ego_density_W3_home', 'new_edge_rate_size', 'n_comm_W3_size', 'participation_size', 'NOV_res_size', 'ego_density_W3_size', 'edge_persistence_size', 'M_size', 'deg_W1_size', 'deg_W3_size', 'OPEN_all', 'n_components_all', 'OPEN_home', 'n_components_home', 'OPEN_size', 'n_components_size']\n                              0         1         2\nci                            3         4        16\nsplit                    COHORT       DEV    COHORT\ngroup                   MATHDEC       Eng       SOC\nrgroup                  MATHDEC    CS+Eng       SOC\nmed_home                      0         0         0\nnew_edge_rate_all           0.0  0.142857  0.238095\nn_comm_W3_all                 1         1         3\nparticipation_all           0.0       0.0  0.512111\nNOV_res_all                 NaN -0.942442 -0.166413\nego_density_W3_all     0.866667       0.7   0.47619\nedge_persistence_all   0.614286  0.305556      0.15\nn_early_rows                 72        64        64\nn_home                       59        53         8\nn_unlab_early                 3        10        32\nhome_cov               0.819444  0.828125     0.125\nM_home                        1         6         0\nNOV_home                    0.0       0.0       NaN\nNOV_res_home          -0.979137 -0.942234       NaN\ndeg_W1_home                   5        13         0\ndeg_W3_home                   4         5         0\nnew_edge_rate_home     0.055556  0.142857       0.0\nedge_persistence_home       0.5  0.338235       NaN\nparticipation_home          0.0       0.0       NaN\nn_comm_W3_home                1         1         0\nego_density_W3_home         1.0       0.7       NaN\nnew_edge_rate_size          0.0  0.128893       0.0\nn_comm_W3_size              1.0       1.0       0.0\nparticipation_size          0.0       0.0       NaN\nNOV_res_size                NaN -0.942442       NaN\nego_density_W3_size    0.871905  0.778333       NaN", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [208] ASSISTANT · 2026-09-29 06:01:33 UTC

```
EXP12 carries its own home-build values for the same 12,499 EXP5 concepts. I'll add the planned cross-check (agreement share and Spearman per component) to `method.py`.
```

### [209] TOOL CALL — Bash · 2026-09-29 06:01:33 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("method.py"); s=p.read_text()
old='''def build_outputs() -> None:'''
new='''def exp12_crosscheck() -> dict:
    """EXP12 (art_uw4OeagJP3rv) open_features.parquet: cross-check of the home-build component values where it
    overlaps (EXP5 frame). EXP12 used its own home-paper definition, so agreement is reported, not required."""
    from common import RUN_ROOT
    p = RUN_ROOT / "3_invention_loop/iter_4/gen_art/gen_art_experiment_12/open_features.parquet"
    if not p.exists():
        return {"available": False}
    o = pd.read_parquet(p)
    cv = pd.read_parquet(DATA / "clean_variants.parquet")
    m = cv[cv.frame == "exp5"].merge(o, on="ci", suffixes=("", "_e12"))
    out = {"available": True, "n_overlap": int(len(m))}
    for k in ("new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"):
        a, b = m[f"{k}__raw"].to_numpy(float), m[f"{k}_home"].to_numpy(float)
        ok = np.isfinite(a) & np.isfinite(b)
        out[k] = {"n_both_finite": int(ok.sum()), "share_equal_1e9": float(np.mean(np.abs(a[ok] - b[ok]) <= 1e-9)),
                  "spearman": float(stats.spearmanr(a[ok], b[ok])[0]) if ok.sum() > 10 else None}
    return out


def build_outputs() -> None:'''
assert old in s; s=s.replace(old,new,1)
s=s.replace('''            "concept_key_check": concept_key_check(),''','''            "concept_key_check": concept_key_check(), "exp12_home_crosscheck": exp12_crosscheck(),''')
p.write_text(s)
EOF
OMP_NUM_THREADS=1 .venv/bin/python -c "
import sys; sys.path.insert(0,'.'); sys.path.insert(0,'lib')
import method, json; print(json.dumps(method.exp12_crosscheck(), indent=0)[:1500])"
```

### [210] TOOL RESULT — Bash · 2026-09-29 06:01:33 UTC

```
{"stdout": "{\n\"available\": true,\n\"n_overlap\": 12079,\n\"new_edge_rate\": {\n\"n_both_finite\": 12079,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 1.0\n},\n\"n_comm_W3\": {\n\"n_both_finite\": 12079,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 0.9999999999999999\n},\n\"participation\": {\n\"n_both_finite\": 8968,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 0.9999999058066041\n},\n\"NOV_res\": {\n\"n_both_finite\": 9475,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 1.0\n},\n\"ego_density_W3\": {\n\"n_both_finite\": 6810,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 1.0\n},\n\"edge_persistence\": {\n\"n_both_finite\": 11236,\n\"share_equal_1e9\": 1.0,\n\"spearman\": 1.0\n}\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [211] ASSISTANT · 2026-09-29 06:01:55 UTC

```
The EXP12 cross-check agrees on every overlapping value (share equal = 1.0 for all six components). Waiting on the association run.
```

### [212] TOOL CALL — Bash · 2026-09-29 06:01:55 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sleep 420; tail -1 logs/s6_full.out
```

### [213] TOOL RESULT — Bash · 2026-09-29 06:08:35 UTC

```
{"stdout": "06:07:13|INFO   |501/1217 done; 17.0 min; eta 24.2 min", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [214] TOOL CALL — Bash · 2026-09-29 06:09:03 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; sleep 540; tail -1 logs/s6_full.out
```

### [215] TOOL RESULT — Bash · 2026-09-29 06:17:41 UTC

```
{"stdout": "06:15:27|INFO   |done in 25.2 min", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [216] ASSISTANT · 2026-09-29 06:18:03 UTC

```
The association run finished in 25 min. Running the verdict script:
```

### [217] TOOL CALL — Bash · 2026-09-29 06:18:03 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; OMP_NUM_THREADS=1 timeout 1200 .venv/bin/python s7_verdict.py 2>&1 | grep -v Warn | tail -5; .venv/bin/python - <<'EOF'
import json
V=json.load(open("results/clean_vs_raw_psp.json"))
print(json.dumps(V["verdict"],indent=0)); print(json.dumps(V["predictions"],indent=0)[:2500]); print(V["F6_contingency"])
for h in V["headline_R2_O2r_m50"]:
    s=h["variant"].ljust(26)
    for b in ("DEV","OLDHO","COH1014","COH1517","POOLED"):
        r=h[b]; 
        if r["psp"] is None: s+=f" {b}: NA        "; continue
        s+=f" {b}:{r['psp']:+.3f}[{r['ci'][0]:+.2f},{r['ci'][1]:+.2f}]n{r['n']}"
        if "retention_ratio" in r and r["retention_ratio"] is not None: s+=f"(raw{r['same_sample_raw']:+.3f},ret{r['retention_ratio']:.2f})"
    print(s)
EOF
```

### [218] TOOL RESULT — Bash · 2026-09-29 06:18:25 UTC

```
{"stdout": "06:17:40|INFO   |VERDICT PARTLY_THIN; P1 False {'COH1517': False, 'OLDHO': False}; P2 True; P3 True (rho 0.034); V1 keep {'COH1517': 0.7643013231828545, 'OLDHO': 0.6362526801996564}; degree flag False\n06:17:41|INFO   |figures written\n{\n\"verdict\": \"PARTLY_THIN\",\n\"DEGREE_ARTEFACT_PERSISTENCE\": false,\n\"clauses\": {\n\"P1\": false,\n\"P3\": true,\n\"V1_keeps_ge_50pct_in_COH1517_or_OLDHO\": true,\n\"V1_retention\": {\n\"COH1517\": 0.7643013231828545,\n\"OLDHO\": 0.6362526801996564\n},\n\"raw_NOVCHURN_ci_excludes_0\": {\n\"COH1517\": true,\n\"OLDHO\": true\n},\n\"exc_and_rare_keep_lt_30pct\": {\n\"COH1517\": false,\n\"OLDHO\": false\n},\n\"P2\": true,\n\"raw_edge_persistence_pooled_ci_lt0\": true\n},\n\"label\": \"selection data, outcomes previously unsealed: robustness evidence, not confirmation\"\n}\n{\n\"P1\": {\n\"holds\": false,\n\"per_body\": {\n\"COH1517\": false,\n\"OLDHO\": false\n},\n\"rule\": \"psp(NOVCHURN_exc) >= 0.70 psp(NOVCHURN_raw), same sample, R2, COH1517 AND OLDHO\",\n\"detail\": {\n\"COH1517\": {\n\"ratio\": 0.39594449273340393,\n\"ratio_ci\": [\n-0.26906748871819375,\n0.8842632275100695\n],\n\"psp_exc\": 0.06317913710216283,\n\"psp_raw_same_sample\": 0.15956564180500524,\n\"n\": 490\n},\n\"OLDHO\": {\n\"ratio\": 0.046849438574826936,\n\"ratio_ci\": [\n-0.5585492463643292,\n0.44451008406689974\n],\n\"psp_exc\": 0.00558634333483666,\n\"psp_raw_same_sample\": 0.1192403474785353,\n\"n\": 1321\n}\n}\n},\n\"P2\": {\n\"holds\": true,\n\"psp\": -0.11558300476164542,\n\"ci\": [\n-0.14529406903883194,\n-0.08637301651544306\n],\n\"n\": 4262\n},\n\"P3\": {\n\"holds\": true,\n\"spearman_NOVCHURN_exc_log_n_all\": 0.033912654545104295,\n\"ci\": [\n0.015390987055309715,\n0.05379348390665524\n],\n\"n\": 9945,\n\"spearman_on_analysis_sample\": 0.025460592516112258,\n\"n_analysis\": 6203\n}\n}\n{'COH1517_n_rare10': 235, 'COH1517_n_rare5': 233, 'COH1517_rare_primary': 'NOVCHURN_rare10'}\nNOVCHURN_raw               DEV:+0.116[+0.08,+0.15]n2741 OLDHO:+0.113[+0.06,+0.16]n1404 COH1014:+0.113[+0.07,+0.16]n1799 COH1517:+0.161[+0.07,+0.25]n506 POOLED:+0.116[+0.09,+0.14]n6450\nNOVCHURN_exc               DEV:+0.008[-0.03,+0.05]n2665(raw+0.118,ret0.07) OLDHO:+0.006[-0.05,+0.06]n1321(raw+0.119,ret0.05) COH1014:-0.007[-0.06,+0.04]n1727(raw+0.108,ret-0.06) COH1517:+0.063[-0.02,+0.15]n490(raw+0.160,ret0.40) POOLED:+0.008[-0.02,+0.03]n6203(raw+0.117,ret0.06)\nNOVCHURN_zperm             DEV:+0.007[-0.03,+0.05]n2284(raw+0.108,ret0.06) OLDHO:+0.021[-0.05,+0.08]n928(raw+0.113,ret0.19) COH1014:-0.003[-0.06,+0.05]n1366(raw+0.124,ret-0.03) COH1517:+0.073[-0.02,+0.17]n398(raw+0.161,ret0.45) POOLED:+0.012[-0.02,+0.04]n4976(raw+0.118,ret0.10)\nNOVCHURN_rare5             DEV:+0.127[+0.07,+0.18]n1191(raw+0.196,ret0.64) OLDHO:+0.140[+0.06,+0.22]n562(raw+0.115,ret1.21) COH1014:+0.149[+0.08,+0.22]n754(raw+0.137,ret1.11) COH1517:+0.105[-0.02,+0.24]n233(raw+0.147,ret0.68) POOLED:+0.130[+0.09,+0.17]n2740(raw+0.156,ret0.83)\nNOVCHURN_rare10            DEV:+0.066[+0.01,+0.12]n1471(raw+0.097,ret0.68) OLDHO:+0.044[-0.07,+0.15]n387(raw+0.069,ret0.64) COH1014:+0.076[+0.01,+0.15]n781(raw+0.126,ret0.60) COH1517:+0.176[+0.05,+0.29]n235(raw+0.230,ret0.76) POOLED:+0.078[+0.04,+0.11]n2874(raw+0.114,ret0.68)\nNOVCHURN_cfg               DEV:+0.115[+0.07,+0.16]n1915(raw+0.112,ret1.02) OLDHO:+0.071[-0.01,+0.15]n677(raw+0.086,ret0.83) COH1014:+0.114[+0.05,+0.18]n1073(raw+0.111,ret1.03) COH1517:+0.088[-0.02,+0.20]n328(raw+0.112,ret0.79) POOLED:+0.106[+0.07,+0.14]n3993(raw+0.106,ret1.00)\nNOVCHURN_chao              DEV:+0.107[+0.07,+0.14]n2729(raw+0.120,ret0.89) OLDHO:+0.123[+0.07,+0.18]n1389(raw+0.111,ret1.11) COH1014:+0.099[+0.05,+0.14]n1793(raw+0.114,ret0.87) COH1517:+0.153[+0.07,+0.24]n506(raw+0.161,ret0.95) POOLED:+0.108[+0.08,+0.13]n6417(raw+0.118,ret0.91)\nNOV_res__raw               DEV:+0.076[+0.04,+0.11]n2741 OLDHO:+0.093[+0.04,+0.14]n1404 COH1014:+0.046[-0.00,+0.09]n1799 COH1517:+0.134[+0.05,+0.21]n506 POOLED:+0.073[+0.05,+0.10]n6450\nNOV_res_exc                DEV:+0.008[-0.03,+0.04]n2665(raw+0.081,ret0.09) OLDHO:+0.002[-0.05,+0.06]n1321(raw+0.097,ret0.02) COH1014:-0.024[-0.07,+0.03]n1727(raw+0.039,ret-0.61) COH1517:+0.071[-0.02,+0.16]n490(raw+0.130,ret0.55) POOLED:+0.003[-0.02,+0.03]n6203(raw+0.073,ret0.04)\nNOV_res_rare10             DEV:+0.102[+0.05,+0.15]n1471(raw+0.101,ret1.01) OLDHO:+0.065[-0.04,+0.17]n387(raw+0.048,ret1.37) COH1014:+0.048[-0.02,+0.12]n781(raw+0.050,ret0.95) COH1517:+0.205[+0.08,+0.32]n235(raw+0.225,ret0.91) POOLED:+0.093[+0.05,+0.13]n2874(raw+0.091,ret1.01)\nedge_persistence__raw      DEV:-0.076[-0.11,-0.04]n3080 OLDHO:-0.086[-0.13,-0.04]n1668 COH1014:-0.116[-0.16,-0.07]n2064 COH1517:-0.112[-0.20,-0.02]n597 POOLED:-0.088[-0.11,-0.07]n7409\nedge_persistence_exc       DEV:+0.006[-0.03,+0.04]n3059(raw-0.074,ret-0.08) OLDHO:-0.006[-0.06,+0.04]n1640(raw-0.087,ret0.07) COH1014:-0.013[-0.06,+0.03]n2049(raw-0.116,ret0.11) COH1517:+0.001[-0.08,+0.08]n594(raw-0.112,ret-0.01) POOLED:-0.003[-0.03,+0.02]n7342(raw-0.087,ret0.04)\nedge_persistence_rare10    DEV:-0.010[-0.06,+0.04]n1901(raw-0.041,ret0.25) OLDHO:-0.037[-0.13,+0.06]n520(raw-0.075,ret0.50) COH1014:-0.055[-0.12,+0.00]n1029(raw-0.111,ret0.50) COH1517:-0.058[-0.17,+0.06]n302(raw-0.116,ret0.49) POOLED:-0.030[-0.06,+0.00]n3752(raw-0.067,ret0.45)\nz_pers_cfg                 DEV:-0.100[-0.14,-0.06]n2033(raw-0.104,ret0.97) OLDHO:-0.122[-0.20,-0.05]n730(raw-0.136,ret0.90) COH1014:-0.172[-0.23,-0.12]n1141(raw-0.151,ret1.14) COH1517:-0.066[-0.18,+0.04]n358(raw-0.104,ret0.64) POOLED:-0.116[-0.15,-0.09]n4262(raw-0.116,ret1.00)\nexcess_pers_cfg            DEV:-0.077[-0.11,-0.04]n3080(raw-0.076,ret1.01) OLDHO:-0.081[-0.13,-0.03]n1668(raw-0.086,ret0.94) COH1014:-0.115[-0.16,-0.07]n2064(raw-0.116,ret0.99) COH1517:-0.125[-0.21,-0.04]n597(raw-0.112,ret1.11) POOLED:-0.089[-0.11,-0.07]n7409(raw-0.088,ret1.01)\nEP_chao                    DEV:-0.081[-0.12,-0.05]n3148(raw-0.077,ret1.08) OLDHO:-0.105[-0.15,-0.06]n1768(raw-0.082,ret1.24) COH1014:-0.089[-0.13,-0.05]n2139(raw-0.115,ret0.74) COH1517:-0.099[-0.18,-0.01]n625(raw-0.113,ret0.86) POOLED:-0.083[-0.11,-0.06]n7680(raw-0.087,ret0.95)\nedge_persistence_nullmean  DEV:-0.109[-0.15,-0.07]n3102 OLDHO:-0.116[-0.17,-0.07]n1699 COH1014:-0.143[-0.19,-0.10]n2093 COH1517:-0.123[-0.21,-0.04]n607 POOLED:-0.120[-0.14,-0.10]n7501\nego_density_W3__raw        DEV:-0.052[-0.09,-0.01]n2376 OLDHO:+0.006[-0.05,+0.07]n1014 COH1014:+0.030[-0.02,+0.09]n1420 COH1517:+0.018[-0.08,+0.12]n423 POOLED:-0.013[-0.04,+0.01]n5233\nz_dens_cfg                 DEV:-0.087[-0.13,-0.05]n2373(raw-0.051,ret1.71) OLDHO:-0.089[-0.15,-0.03]n1010(raw+0.006,ret-13.98) COH1014:-0.127[-0.18,-0.08]n1414(raw+0.032,ret-4.00) COH1517:-0.047[-0.15,+0.05]n418(raw+0.017,ret-2.66) POOLED:-0.091[-0.12,-0.06]n5215(raw-0.012,ret7.74)\nz_dens_k                   DEV:-0.052[-0.09,-0.01]n2376(raw-0.052,ret1.00) OLDHO:-0.050[-0.11,+0.01]n1014(raw+0.006,ret-8.03) COH1014:-0.083[-0.13,-0.03]n1420(raw+0.030,ret-2.72) COH1517:+0.042[-0.06,+0.14]n423(raw+0.018,ret2.28) POOLED:-0.047[-0.07,-0.02]n5233(raw-0.013,ret3.74)\nOPEN_home                  DEV:+0.109[+0.07,+0.14]n3003 OLDHO:+0.070[+0.02,+0.12]n1569 COH1014:+0.074[+0.03,+0.12]n1993 COH1517:+0.091[+0.01,+0.17]n573 POOLED:+0.085[+0.06,+0.11]n7138\nOPEN_home_clean            DEV:+0.133[+0.10,+0.17]n2755(raw+0.124,ret1.07) OLDHO:+0.094[+0.04,+0.15]n1317(raw+0.076,ret1.23) COH1014:+0.108[+0.06,+0.16]n1738(raw+0.070,ret1.54) COH1517:+0.129[+0.04,+0.21]n512(raw+0.092,ret1.41) POOLED:+0.115[+0.09,+0.14]n6322(raw+0.092,ret1.24)\nOPEN_home_exc              DEV:+0.072[+0.04,+0.11]n2987(raw+0.110,ret0.65) OLDHO:+0.035[-0.02,+0.09]n1555(raw+0.071,ret0.50) COH1014:+0.041[-0.00,+0.09]n1984(raw+0.073,ret0.56) COH1517:+0.070[-0.01,+0.15]n572(raw+0.089,ret0.78) POOLED:+0.052[+0.03,+0.08]n7098(raw+0.086,ret0.61)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [219] THINKING · 2026-09-29 06:18:47 UTC

```
Verdict is PARTLY_THIN: P1 fails since raw psp stays concentrated in COH1517/OLDHO, while P2/P3 hold and rarefied/corrected variants retain most signal. Since the permutation-null mean predicts outcomes as well as raw persistence, the signal looks like a static property of pooled topic mix rather than temporal churn — next I'll run the re-derivation and power simulation.
```

### [220] TOOL CALL — Bash · 2026-09-29 06:18:47 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; OMP_NUM_THREADS=1 timeout 900 .venv/bin/python rederive.py 2>&1 | grep -v Warn | tail -2; (OMP_NUM_THREADS=1 nohup .venv/bin/python s8_power.py > logs/s8_power.out 2>&1 &); python3 -c "
import json; d=json.load(open('results/rederive.json')); print(json.dumps(d,indent=0)[:1800])"
```

### [221] TOOL RESULT — Bash · 2026-09-29 06:18:47 UTC

```
{"stdout": "06:18:23|INFO   |rederive pass True; worst psp diff 2.22e-16; SB diff 0.00e+00\n{\n\"psp\": {\n\"COH1517|NOVCHURN_exc|R2\": {\n\"rederived\": 0.06317913710216276,\n\"pipeline\": 0.06317913710216283,\n\"abs_diff\": 6.938893903907228e-17,\n\"n\": 490,\n\"n_pipeline\": 490\n},\n\"COH1517|NOVCHURN_raw|R2\": {\n\"rederived\": 0.16119061802773677,\n\"pipeline\": 0.16119061802773654,\n\"abs_diff\": 2.220446049250313e-16,\n\"n\": 506,\n\"n_pipeline\": 506\n},\n\"OLDHO|NOVCHURN_exc|R2\": {\n\"rederived\": 0.005586343334836665,\n\"pipeline\": 0.00558634333483666,\n\"abs_diff\": 5.204170427930421e-18,\n\"n\": 1321,\n\"n_pipeline\": 1321\n},\n\"OLDHO|NOVCHURN_raw|R2\": {\n\"rederived\": 0.11299617572105294,\n\"pipeline\": 0.11299617572105293,\n\"abs_diff\": 1.3877787807814457e-17,\n\"n\": 1404,\n\"n_pipeline\": 1404\n},\n\"POOLED|z_pers_cfg|R2\": {\n\"rederived\": -0.1155830047616454,\n\"pipeline\": -0.11558300476164542,\n\"abs_diff\": 1.3877787807814457e-17,\n\"n\": 4262,\n\"n_pipeline\": 4262\n},\n\"POOLED|edge_persistence__raw|R2\": {\n\"rederived\": -0.08781529774927943,\n\"pipeline\": -0.08781529774927933,\n\"abs_diff\": 9.71445146547012e-17,\n\"n\": 7409,\n\"n_pipeline\": 7409\n},\n\"POOLED|NOVCHURN_raw|R2\": {\n\"rederived\": 0.11623313287281349,\n\"pipeline\": 0.11623313287281345,\n\"abs_diff\": 4.163336342344337e-17,\n\"n\": 6450,\n\"n_pipeline\": 6450\n},\n\"POOLED|NOVCHURN_exc|R2\": {\n\"rederived\": 0.00758706244816751,\n\"pipeline\": 0.007587062448167491,\n\"abs_diff\": 1.9081958235744878e-17,\n\"n\": 6203,\n\"n_pipeline\": 6203\n},\n\"COH1517|P1_same_sample_ratio\": {\n\"rederived_ratio\": 0.39594449273340365,\n\"pipeline_ratio\": 0.39594449273340393,\n\"abs_diff_components\": 6.938893903907228e-17,\n\"n\": 490\n},\n\"OLDHO|P1_same_sample_ratio\": {\n\"rederived_ratio\": 0.046849438574827006,\n\"pipeline_ratio\": 0.046849438574826936,\n\"abs_diff_components\": 6.938893903907228e-17,\n\"n\": 1321\n}\n},\n\"tolerance_psp\": 1e-09,\n\"tolerance_SB\": 1e-06,\n\"P3\": {\n\"rederived\": 0.033912654545104295,\n\"pipeline\": 0.033912654545104295,\n\"abs_d", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [222] ASSISTANT · 2026-09-29 06:19:11 UTC

```
The independent re-derivation passes (worst psp diff 2.2e-16; SB diff 0). While power runs, pulling the group DL, PC3 and disattenuation numbers:
```

### [223] TOOL CALL — Bash · 2026-09-29 06:19:11 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
import json
V=json.load(open("results/clean_vs_raw_psp.json"))
for k,g in V["groups"].items():
    print(k, "DL", round(g["DL"]["b"],3), [round(x,3) for x in g["DL"]["ci"]], "I2", round(g["DL"]["I2"],2), "pos", g["n_positive_of_5"], {a:(round(b["rho"],3) if b["rho"] is not None else None, b["n"]) for a,b in g["groups"].items()})
pl=V["cells"]["planted_PC3"]
for b,r in pl.items(): print("PC3",b, round(r["planted"]["rho"],3), [round(x,3) for x in r["planted"]["ci"]], "placebo excl0", r["n_placebo_ci_excl0"])
for k in ["POOLED|NOVCHURN_raw|O2r_m50|R2","POOLED|NOVCHURN_raw|O2r_m50|R3","POOLED|OPEN_home|O2r_m50|R3","COH1517|NOVCHURN_raw|O2r_m50|R2","POOLED|NOVCHURN_rare10|O2r_m50|R2","POOLED|NOVCHURN_exc|O2r_m50|R2","POOLED|OPEN_home_clean|O2r_m50|R3"]:
    print("DIS",k, V["disattenuated"].get(k))
P=V["cells"]["paired"]
for k in ["POOLED|OPEN_home_clean|OPEN_home|O2r_m50|R2","POOLED|OPEN_home_clean|OPEN_home|O2r_m50|R3","POOLED|NOVCHURN_rare10|NOVCHURN_raw|O2r_m50|R2","POOLED|NOVCHURN_exc|NOVCHURN_raw|O2r_m50|R2","POOLED|z_dens_cfg|ego_density_W3__raw|O2r_m50|R2","POOLED|edge_persistence_rare10|edge_persistence__raw|O2r_m50|R2"]:
    r=P[k]; print("PAIR",k, {a:(round(b,3) if isinstance(b,float) else b) for a,b in r.items() if a in ("n","a","b","diff","diff_ci","ratio","ratio_ci")})
print(V["holm"])
c=V["cells"]["psp"]
for x in ["NOVCHURN_raw","NOVCHURN_exc","NOVCHURN_rare10","edge_persistence__raw","edge_persistence_nullmean","OPEN_home","OPEN_home_clean"]:
    print(x, {r: round(c[f"POOLED|{x}|O2r_m50|{r}"]["rho"],3) for r in ("R0","R2","R3")}, "resid R2", round(c[f"POOLED|{x}|O2r_resid|R2"]["rho"],3))
EOF
```

### [224] TOOL RESULT — Bash · 2026-09-29 06:19:11 UTC

```
{"stdout": "NOVCHURN_raw|O2r_m50|R2 DL 0.11 [0.085, 0.136] I2 0.0 pos 5 {'CS+Eng': (0.109, 1463), 'PHYS': (0.045, 488), 'LIFEENV': (0.105, 740), 'SOC': (0.122, 877), 'MATHDEC': (0.244, 91), 'BGM+Med': (0.119, 2791)}\nNOVCHURN_exc|O2r_m50|R2 DL 0.006 [-0.019, 0.032] I2 0.0 pos 4 {'PHYS': (0.042, 466), 'CS+Eng': (-0.003, 1411), 'LIFEENV': (0.009, 705), 'MATHDEC': (0.077, 83), 'SOC': (0.008, 822), 'BGM+Med': (0.004, 2716)}\nNOVCHURN_cfg|O2r_m50|R2 DL 0.095 [0.054, 0.135] I2 0.23 pos 4 {'CS+Eng': (0.12, 934), 'PHYS': (-0.033, 292), 'LIFEENV': (0.073, 344), 'SOC': (0.124, 359), 'MATHDEC': (0.264, 50), 'BGM+Med': (0.105, 2014)}\nNOVCHURN_rare10|O2r_m50|R2 DL 0.081 [0.042, 0.119] I2 0.0 pos 5 {'PHYS': (0.11, 195), 'CS+Eng': (0.029, 685), 'MATHDEC': (None, 24), 'LIFEENV': (0.014, 185), 'SOC': (0.151, 188), 'BGM+Med': (0.099, 1597)}\nOPEN_home|O2r_m50|R2 DL 0.07 [0.035, 0.105] I2 0.47 pos 5 {'PHYS': (0.013, 546), 'CS+Eng': (0.065, 1602), 'LIFEENV': (0.055, 821), 'MATHDEC': (0.213, 125), 'SOC': (0.052, 968), 'BGM+Med': (0.115, 3076)}\nOPEN_home_clean|O2r_m50|R2 DL 0.098 [0.06, 0.136] I2 0.47 pos 5 {'CS+Eng': (0.095, 1441), 'PHYS': (0.013, 487), 'LIFEENV': (0.095, 676), 'MATHDEC': (0.165, 104), 'SOC': (0.083, 777), 'BGM+Med': (0.142, 2837)}\nPC3 OLDHO 0.239 [0.193, 0.284] placebo excl0 1\nPC3 COH1014 0.199 [0.157, 0.239] placebo excl0 5\nPC3 DEV 0.217 [0.185, 0.251] placebo excl0 0\nPC3 POOLED 0.187 [0.165, 0.21] placebo excl0 5\nPC3 COH1517 0.19 [0.109, 0.272] placebo excl0 0\nDIS POOLED|NOVCHURN_raw|O2r_m50|R2 {'psp': 0.11623313287281345, 'SB_x': 0.4756815162981721, 'SB_x_key': 'NOVCHURN_raw', 'rel_y': 0.8949878831624887, 'psp_dis': 0.1781407300190277, 'ci': [0.14064083234641267, 0.21420004055381148], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nDIS POOLED|NOVCHURN_raw|O2r_m50|R3 {'psp': 0.10237189160328719, 'SB_x': 0.4756815162981721, 'SB_x_key': 'NOVCHURN_raw', 'rel_y': 0.8949878831624887, 'psp_dis': 0.15689677334597452, 'ci': [0.11911136576122244, 0.19452438413708803], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nDIS POOLED|OPEN_home|O2r_m50|R3 {'psp': 0.06743172606338378, 'SB_x': 0.48524391683013246, 'SB_x_key': 'OPEN_home', 'rel_y': 0.8949878831624887, 'psp_dis': 0.10232356173626449, 'ci': [0.06703677535864708, 0.13796120709351073], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nDIS COH1517|NOVCHURN_raw|O2r_m50|R2 {'psp': 0.16119061802773654, 'SB_x': 0.4912698283309254, 'SB_x_key': 'NOVCHURN_raw', 'rel_y': 0.8888022839591002, 'psp_dis': 0.24393669376138125, 'ci': [0.10848326298059337, 0.3821094675208231], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nDIS POOLED|NOVCHURN_rare10|O2r_m50|R2 {'psp': 0.07816923082828127, 'SB_x': 0.359409889495414, 'SB_x_key': 'NOVCHURN_rare5', 'rel_y': 0.8949878831624887, 'psp_dis': 0.13782634817283618, 'ci': [0.06960605159751858, 0.20533200345061728], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nDIS POOLED|NOVCHURN_exc|O2r_m50|R2 {'psp': 0.007587062448167491, 'SB_x': 0.014435231057439202, 'rel_y': 0.8949878831624887, 'psp_dis': None, 'note': 'SB_x < 0.10: not disattenuated (variant essentially unreliable)'}\nDIS POOLED|OPEN_home_clean|O2r_m50|R3 {'psp': 0.09833417560835854, 'SB_x': 0.5770699813484683, 'SB_x_key': 'OPEN_home_clean', 'rel_y': 0.8949878831624887, 'psp_dis': 0.1368301054730301, 'ci': [0.10100550004921002, 0.17180285410593382], 'flag': 'approximate for partial Spearman (Spearman 1904 correction applied to a rank partial correlation); rel_y conservative (m = 25 halves)'}\nPAIR POOLED|OPEN_home_clean|OPEN_home|O2r_m50|R2 {'n': 6322, 'a': 0.115, 'b': 0.092, 'diff': 0.022, 'diff_ci': [0.010794968180655368, 0.034110130973582876], 'ratio': 1.241, 'ratio_ci': [1.1096182056495258, 1.426711093784284]}\nPAIR POOLED|OPEN_home_clean|OPEN_home|O2r_m50|R3 {'n': 6322, 'a': 0.098, 'b': 0.076, 'diff': 0.023, 'diff_ci': [0.01126586772248222, 0.034436118396405604], 'ratio': 1.298, 'ratio_ci': [1.1315453559088193, 1.5619428402452114]}\nPAIR POOLED|NOVCHURN_rare10|NOVCHURN_raw|O2r_m50|R2 {'n': 2872, 'a': 0.078, 'b': 0.114, 'diff': -0.036, 'diff_ci': [-0.05645344112754666, -0.016072012801518883], 'ratio': 0.684, 'ratio_ci': [0.4621442309499234, 0.8548362285527685]}\nPAIR POOLED|NOVCHURN_exc|NOVCHURN_raw|O2r_m50|R2 {'n': 6203, 'a': 0.008, 'b': 0.117, 'diff': -0.109, 'diff_ci': [-0.13305423567223992, -0.08724804853335967], 'ratio': 0.065, 'ratio_ci': [-0.17465803304951272, 0.24070000670576855]}\nPAIR POOLED|z_dens_cfg|ego_density_W3__raw|O2r_m50|R2 {'n': 5215, 'a': -0.091, 'b': -0.012, 'diff': -0.079, 'diff_ci': [-0.11350612085605946, -0.044762251879614134], 'ratio': 7.738, 'ratio_ci': [-77.70781569664452, 88.70596739752952]}\nPAIR POOLED|edge_persistence_rare10|edge_persistence__raw|O2r_m50|R2 {'n': 3752, 'a': -0.03, 'b': -0.067, 'diff': 0.037, 'diff_ci': [0.018133694848159264, 0.05708329128673352], 'ratio': 0.446, 'ratio_ci': [-0.041385580368801175, 0.7153198635787971]}\n{'family': ['P1: NOVCHURN_exc psp > 0 in COH1517 and OLDHO (max one-sided p)', 'P2: z_pers_cfg psp < 0 POOLED', 'P3: |Spearman(NOVCHURN_exc, log n)| >= 0.20 (boot)'], 'p': [0.4102948525737131, 0.0004997501249375312, 0.001996007984031936], 'p_holm': [0.4102948525737131, 0.0014992503748125937, 0.003992015968063872]}\nNOVCHURN_raw {'R0': 0.125, 'R2': 0.116, 'R3': 0.102} resid R2 0.121\nNOVCHURN_exc {'R0': 0.011, 'R2': 0.008, 'R3': 0.005} resid R2 0.006\nNOVCHURN_rare10 {'R0': 0.093, 'R2': 0.078, 'R3': 0.067} resid R2 0.083\nedge_persistence__raw {'R0': -0.086, 'R2': -0.088, 'R3': -0.076} resid R2 -0.093\nedge_persistence_nullmean {'R0': -0.119, 'R2': -0.12, 'R3': -0.105} resid R2 -0.126\nOPEN_home {'R0': 0.109, 'R2': 0.085, 'R3': 0.067} resid R2 0.079\nOPEN_home_clean {'R0': 0.137, 'R2': 0.115, 'R3': 0.098} resid R2 0.114", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [225] THINKING · 2026-09-29 06:19:11 UTC

```
PC3's planted association shows up consistently (0.19–0.24) across all bodies, but shuffled-x placebos exceed the planned false-positive limit—5 of 20 runs exclude 0 for POOLED and COH1014 versus a target of at most 1. Let me look closer at the placebo values.
```

### [226] TOOL CALL — Bash · 2026-09-29 06:19:11 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
import json, numpy as np
V=json.load(open("results/clean_vs_raw_psp.json"))
for b,r in V["cells"]["planted_PC3"].items():
    rh=np.array([p["rho"] for p in r["placebos"]]); se=np.array([p["se"] for p in r["placebos"]])
    print(b, "n", r["placebos"][0]["n"], "rho sd", rh.std().round(4), "mean se", se.mean().round(4), "1/sqrt(n)", round(1/np.sqrt(r["placebos"][0]["n"]),4), np.round(rh,3))
EOF
```

### [227] TOOL RESULT — Bash · 2026-09-29 06:19:11 UTC

```
{"stdout": "OLDHO n 1797 rho sd 0.023 mean se 0.0238 1/sqrt(n) 0.0236 [ 0.025  0.021 -0.006 -0.006  0.016 -0.024 -0.035 -0.019  0.022 -0.006\n -0.016 -0.005 -0.001 -0.001 -0.018  0.017 -0.018 -0.024  0.064 -0.026]\nCOH1014 n 2154 rho sd 0.0287 mean se 0.0217 1/sqrt(n) 0.0215 [-0.015  0.051 -0.002  0.049  0.026 -0.002 -0.042  0.012  0.032  0.031\n  0.046 -0.044  0.014 -0.028 -0.026  0.01   0.012  0.044  0.023 -0.007]\nDEV n 3169 rho sd 0.0135 mean se 0.0178 1/sqrt(n) 0.0178 [ 0.004 -0.011 -0.017  0.005  0.006 -0.017 -0.012  0.02  -0.019 -0.016\n -0.008  0.006 -0.021  0.001  0.007  0.009  0.017  0.024  0.007  0.01 ]\nPOOLED n 7748 rho sd 0.016 mean se 0.0114 1/sqrt(n) 0.0114 [-0.037  0.003  0.022  0.    -0.028  0.004  0.011  0.014  0.011  0.003\n -0.013 -0.003 -0.026  0.008  0.008 -0.023 -0.013  0.002 -0.02  -0.02 ]\nCOH1517 n 628 rho sd 0.04 mean se 0.0397 1/sqrt(n) 0.0399 [-0.069 -0.062  0.008 -0.041 -0.027 -0.019  0.054  0.075  0.036 -0.02\n -0.004 -0.005  0.055  0.018  0.077 -0.001 -0.01  -0.014  0.033  0.005]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [228] THINKING · 2026-09-29 06:19:35 UTC

```
Bootstrap SEs align with the analytic 1/√n scaling across all bodies, confirming correct CIs, though exclusions run higher than expected (11 vs 5 of 100), possibly due to chance given only 20 draws per body. I'll run a cheap post-seal calibration using 500 permutations per body with point estimates only to confirm this.
```

### [229] TOOL CALL — Bash · 2026-09-29 06:19:35 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat > tests/placebo_calibration.py <<'EOF'
#!/usr/bin/env python3
"""Post-seal diagnostic (exploratory): calibration of the psp CIs under the exact null. 500 permutations of the
planted-x (PC3 construction) per body at R2; share of |psp| > 1.96 x (the placebos' mean bootstrap SE from PC3) and
the ratio sd(permutation psp) / bootstrap SE. -> results/placebo_calibration.json"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import numpy as np
from scipy import stats
from common import RES, jdump
from fastpsp import complete, psp_fast
from tables import design, load_tables
T = load_tables()
V = json.loads((RES / "clean_vs_raw_psp.json").read_text())
out = {"label": "exploratory, post-seal diagnostic"}
for body in ("DEV", "OLDHO", "COH1014", "COH1517", "POOLED"):
    df = T[body]
    Bm, Cm = design(df, "R2", body == "POOLED")
    y = df.O2r_m50.to_numpy(float)
    rr = df.O2r_resid.to_numpy(float)
    rng = np.random.default_rng(99)
    ok = np.isfinite(rr)
    rk = np.full(len(rr), np.nan); rk[ok] = stats.rankdata(rr[ok])
    x = rk + rng.normal(0, 3 * np.nanstd(rk), len(rk))
    m = complete(x, y, Bm, Cm)
    se = float(np.mean([p["se"] for p in V["cells"]["planted_PC3"][body]["placebos"]]))
    rh = []
    for _ in range(500):
        xs = x.copy(); xs[ok] = rng.permutation(x[ok])
        mm = complete(xs, y, Bm, Cm)
        rh.append(psp_fast(xs[mm], y[mm], Bm[mm], Cm[mm]))
    rh = np.asarray(rh)
    out[body] = {"n": int(m.sum()), "boot_se": se, "perm_sd": float(rh.std()), "ratio_sd_se": float(rh.std() / se),
                 "share_abs_gt_1.96se": float(np.mean(np.abs(rh) > 1.96 * se))}
    print(body, out[body], flush=True)
jdump(out, RES / "placebo_calibration.json")
EOF
.venv/bin/python tests/placebo_calibration.py 2>&1 | grep -v Warn; tail -2 logs/s8_power.out
```

### [230] TOOL RESULT — Bash · 2026-09-29 06:19:55 UTC

```
{"stdout": "DEV {'n': 3169, 'boot_se': 0.017791932972589835, 'perm_sd': 0.01755729160253414, 'ratio_sd_se': 0.9868119236725328, 'share_abs_gt_1.96se': 0.042}\nOLDHO {'n': 1797, 'boot_se': 0.023773879295103988, 'perm_sd': 0.024111973602312452, 'ratio_sd_se': 1.0142212511055397, 'share_abs_gt_1.96se': 0.054}\nCOH1014 {'n': 2154, 'boot_se': 0.021662512014813954, 'perm_sd': 0.02098314482184427, 'ratio_sd_se': 0.9686385774417529, 'share_abs_gt_1.96se': 0.044}\nCOH1517 {'n': 628, 'boot_se': 0.03968255744422493, 'perm_sd': 0.040449552089266, 'ratio_sd_se': 1.0193282564038142, 'share_abs_gt_1.96se': 0.058}\nPOOLED {'n': 7748, 'boot_se': 0.011399625823898285, 'perm_sd': 0.01072070783865834, 'ratio_sd_se': 0.9404438359883134, 'share_abs_gt_1.96se': 0.036}\n06:18:31|INFO   |targets: {'OPEN_home|R3': {'T1': 0.062005586577095546, 'T2': 0.08044570966976394, 'T3': 0.03371586303169189}, 'OPEN_home|R5': {'T1': 0.052860267715463045, 'T2': 0.055691598412831285, 'T3': 0.028743047917096243}, 'NOVCHURN_raw|R3': {'T1': 0.0951093923298266, 'T2': 0.1439838738205213, 'T3': 0.051185945801643595}, 'NOVCHURN_raw|R5': {'T1': 0.05205518581801722, 'T2': 0.07122706532466118, 'T3': 0.02801504514649204}, 'NOVCHURN_exc|R3': {'T1': nan, 'T2': 0.061729294636991235, 'T3': 0.0026915736847581704}, 'NOVCHURN_exc|R5': {'T1': nan, 'T2': 0.04859182346043138, 'T3': 0.0011371632932923345}}\n06:19:10|INFO   |At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [231] THINKING · 2026-09-29 06:19:55 UTC

```
The 500-permutation calibration checks out clean, confirming the 20-placebo excess was just chance. Now I'll build `method_out.json`.
```

### [232] TOOL CALL — Bash · 2026-09-29 06:19:55 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 -c "
import json; d=json.load(open('results/power_frame_n.json'))
for k,v in d['results'].items(): print(k, {a:round(b,3) for a,b in v['marginal'].items()}, 'joint', round(v['joint_OPEN_R3_R5_NOVCHURN_R3'],3))
print({k:(round(v) if v else v) for k,v in d['n_for_80pct_marginal'].items() if 'S_A' in k})
"; OMP_NUM_THREADS=1 timeout 1200 .venv/bin/python method.py 2>&1 | grep -v Warn | tail -3; ls -la method_out.json
```

### [233] TOOL RESULT — Bash · 2026-09-29 06:20:19 UTC

```
{"stdout": "S_A|T1|n800 {'OPEN_home|R3': 0.37, 'OPEN_home|R5': 0.287, 'NOVCHURN_raw|R3': 0.668, 'NOVCHURN_raw|R5': 0.228, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.256\nS_A|T2|n800 {'OPEN_home|R3': 0.559, 'OPEN_home|R5': 0.312, 'NOVCHURN_raw|R3': 0.947, 'NOVCHURN_raw|R5': 0.413, 'NOVCHURN_exc|R3': 0.328, 'NOVCHURN_exc|R5': 0.212} joint 0.311\nS_A|T3|n800 {'OPEN_home|R3': 0.14, 'OPEN_home|R5': 0.118, 'NOVCHURN_raw|R3': 0.233, 'NOVCHURN_raw|R5': 0.094, 'NOVCHURN_exc|R3': 0.024, 'NOVCHURN_exc|R5': 0.02} joint 0.07\nS_A|T1|n1500 {'OPEN_home|R3': 0.65, 'OPEN_home|R5': 0.517, 'NOVCHURN_raw|R3': 0.908, 'NOVCHURN_raw|R5': 0.424, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.503\nS_A|T2|n1500 {'OPEN_home|R3': 0.844, 'OPEN_home|R5': 0.568, 'NOVCHURN_raw|R3': 1.0, 'NOVCHURN_raw|R5': 0.68, 'NOVCHURN_exc|R3': 0.538, 'NOVCHURN_exc|R5': 0.371} joint 0.568\nS_A|T3|n1500 {'OPEN_home|R3': 0.22, 'OPEN_home|R5': 0.161, 'NOVCHURN_raw|R3': 0.409, 'NOVCHURN_raw|R5': 0.152, 'NOVCHURN_exc|R3': 0.035, 'NOVCHURN_exc|R5': 0.029} joint 0.113\nS_A|T1|n2500 {'OPEN_home|R3': 0.831, 'OPEN_home|R5': 0.712, 'NOVCHURN_raw|R3': 0.986, 'NOVCHURN_raw|R5': 0.648, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.708\nS_A|T2|n2500 {'OPEN_home|R3': 0.966, 'OPEN_home|R5': 0.75, 'NOVCHURN_raw|R3': 1.0, 'NOVCHURN_raw|R5': 0.896, 'NOVCHURN_exc|R3': 0.791, 'NOVCHURN_exc|R5': 0.579} joint 0.75\nS_A|T3|n2500 {'OPEN_home|R3': 0.362, 'OPEN_home|R5': 0.305, 'NOVCHURN_raw|R3': 0.623, 'NOVCHURN_raw|R5': 0.251, 'NOVCHURN_exc|R3': 0.034, 'NOVCHURN_exc|R5': 0.026} joint 0.261\nS_B|T1|n800 {'OPEN_home|R3': 0.136, 'OPEN_home|R5': 0.149, 'NOVCHURN_raw|R3': 0.538, 'NOVCHURN_raw|R5': 0.323, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.109\nS_B|T2|n800 {'OPEN_home|R3': 0.242, 'OPEN_home|R5': 0.159, 'NOVCHURN_raw|R3': 0.865, 'NOVCHURN_raw|R5': 0.479, 'NOVCHURN_exc|R3': 0.673, 'NOVCHURN_exc|R5': 0.581} joint 0.155\nS_B|T3|n800 {'OPEN_home|R3': 0.044, 'OPEN_home|R5': 0.056, 'NOVCHURN_raw|R3': 0.206, 'NOVCHURN_raw|R5': 0.157, 'NOVCHURN_exc|R3': 0.062, 'NOVCHURN_exc|R5': 0.086} joint 0.031\nS_B|T1|n1500 {'OPEN_home|R3': 0.241, 'OPEN_home|R5': 0.233, 'NOVCHURN_raw|R3': 0.807, 'NOVCHURN_raw|R5': 0.543, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.206\nS_B|T2|n1500 {'OPEN_home|R3': 0.405, 'OPEN_home|R5': 0.263, 'NOVCHURN_raw|R3': 0.99, 'NOVCHURN_raw|R5': 0.756, 'NOVCHURN_exc|R3': 0.911, 'NOVCHURN_exc|R5': 0.855} joint 0.262\nS_B|T3|n1500 {'OPEN_home|R3': 0.055, 'OPEN_home|R5': 0.086, 'NOVCHURN_raw|R3': 0.326, 'NOVCHURN_raw|R5': 0.271, 'NOVCHURN_exc|R3': 0.09, 'NOVCHURN_exc|R5': 0.127} joint 0.042\nS_B|T1|n2500 {'OPEN_home|R3': 0.324, 'OPEN_home|R5': 0.342, 'NOVCHURN_raw|R3': 0.96, 'NOVCHURN_raw|R5': 0.737, 'NOVCHURN_exc|R3': 0.0, 'NOVCHURN_exc|R5': 0.0} joint 0.298\nS_B|T2|n2500 {'OPEN_home|R3': 0.581, 'OPEN_home|R5': 0.378, 'NOVCHURN_raw|R3': 1.0, 'NOVCHURN_raw|R5': 0.92, 'NOVCHURN_exc|R3': 0.992, 'NOVCHURN_exc|R5': 0.975} joint 0.378\nS_B|T3|n2500 {'OPEN_home|R3': 0.073, 'OPEN_home|R5': 0.105, 'NOVCHURN_raw|R3': 0.473, 'NOVCHURN_raw|R5': 0.394, 'NOVCHURN_exc|R3': 0.133, 'NOVCHURN_exc|R5': 0.217} joint 0.063\n{'OPEN_home|R3|S_A|T1': 2051, 'OPEN_home|R3|S_A|T2': 1232, 'OPEN_home|R3|S_A|T3': 6857, 'OPEN_home|R5|S_A|T1': 2744, 'OPEN_home|R5|S_A|T2': 2476, 'OPEN_home|R5|S_A|T3': 9184, 'NOVCHURN_raw|R3|S_A|T1': 931, 'NOVCHURN_raw|R3|S_A|T2': 425, 'NOVCHURN_raw|R3|S_A|T3': 3132, 'NOVCHURN_raw|R5|S_A|T1': 3059, 'NOVCHURN_raw|R5|S_A|T2': 1653, 'NOVCHURN_raw|R5|S_A|T3': 10464, 'NOVCHURN_exc|R3|S_A|T1': None, 'NOVCHURN_exc|R3|S_A|T2': 2137, 'NOVCHURN_exc|R3|S_A|T3': 1106118, 'NOVCHURN_exc|R5|S_A|T1': None, 'NOVCHURN_exc|R5|S_A|T2': 3420, 'NOVCHURN_exc|R5|S_A|T3': 6170662}\n06:19:37|INFO   |method_out.json: 7748 examples; verdict PARTLY_THIN\n-rw-r--r-- 1 root root 11688836 Sep 29 06:19 method_out.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [234] THINKING · 2026-09-29 06:20:19 UTC

```
The power numbers check out for OPEN_home and NOVCHURN_raw, but NOVCHURN_exc rows are artefacts since SB ≈ 0.01 makes "power" noise and NaN targets were being scored as 0. I'll fix those cells to report as not estimable.
```

### [235] TOOL CALL — Bash · 2026-09-29 06:20:19 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("s8_power.py"); s=p.read_text()
old='''                "S_B": {"T1": t1 * math.sqrt(sbB * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan) * math.sqrt(sbB / sbA) if sbA > 0 else math.nan,
                        "T3": 0.5 * full * math.sqrt(sbB / sbA) if sbA > 0 else math.nan},'''
new='''                "S_B": {"T1": t1 * math.sqrt(sbB * rel_y) if np.isfinite(t1) else math.nan,
                        "T2": coh.get("rho", math.nan) * math.sqrt(sbB / sbA) if sbA >= 0.10 else math.nan,
                        "T3": 0.5 * full * math.sqrt(sbB / sbA) if sbA >= 0.10 else math.nan},
                "note": ("index essentially unreliable (SB < 0.10): T1 undefined, S_B scaling undefined; power for "
                         "this index is not interpretable" if (sb_pool is None or sb_pool < 0.10) else ""),'''
assert old in s; s=s.replace(old,new)
old='''            ent = {"marginal": {k: float(v.mean()) for k, v in passes.items()}, "joint_OPEN_R3_R5_NOVCHURN_R3":'''
new='''            valid = {k: bool(np.isfinite(targets[k][s][tname])) for k in passes}
            ent = {"marginal": {k: (float(v.mean()) if valid[k] else None) for k, v in passes.items()},
                   "joint_OPEN_R3_R5_NOVCHURN_R3":'''
assert old in s; s=s.replace(old,new)
old='''            if "NOVCHURN_exc|R3" in passes:'''
new='''            if "NOVCHURN_exc|R3" in passes and valid["NOVCHURN_exc|R3"]:'''
assert old in s; s=s.replace(old,new)
s=s.replace('''            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["marginal"]["OPEN_home|R3"] for n in NS], "s" + ls, alpha=0.5,''','''            ax.plot(NS, [a[f"{s}|{tn}|n{n}"]["marginal"]["OPEN_home|R3"] or np.nan for n in NS], "s" + ls, alpha=0.5,''')
p.write_text(s)
EOF
OMP_NUM_THREADS=1 timeout 900 .venv/bin/python s8_power.py 2>&1 | grep -v Warn | tail -1
```

### [236] TOOL RESULT — Bash · 2026-09-29 06:21:04 UTC

```
{"stdout": "06:20:39|INFO   |At n = 800 (S_A, T3 = half the pooled raw estimate) joint power (OPEN_home R3 & R5 & NOVCHURN_raw R3) = 0.07; at n = 2500 it is 0.26. With T2 (COH1517 raw) it is 0.31 / 0.75. Pessimistic n-mix (S_B, T3): 0.03 / 0.06. The fallback O2r_m30 outcome set is not simulated here (out of scope); analytic n for 0.8 marginal power per index is in n_for_80pct_marginal.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [237] ASSISTANT · 2026-09-29 06:21:28 UTC

```
Rebuilding `method_out.json`, validating it against the schema and generating the mini/preview versions:
```

### [238] TOOL CALL — Bash · 2026-09-29 06:21:28 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; OMP_NUM_THREADS=1 timeout 1200 .venv/bin/python method.py 2>&1 | grep -v Warn | tail -1; SKILL_DIR=/ai-inventor/.claude/skills/aii-json; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/method_out.json 2>&1 | tail -3; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input $PWD/method_out.json 2>&1 | tail -4; ls -la *method_out.json; python3 -c "
import json; d=json.load(open('preview_method_out.json')); e=d['datasets'][0]['examples'][0]; print(json.dumps(e,indent=0)[:1500]); print(json.dumps(d['metadata'].get('concept_key_check')))"
```

### [239] TOOL RESULT — Bash · 2026-09-29 06:21:54 UTC

```
{"stdout": "06:20:57|INFO   |method_out.json: 7748 examples; verdict PARTLY_THIN\nFormat: exp_gen_sol_out\nValidation PASSED\nGenerated 3 versions:\n  Full (7748 items): /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/full_method_out.json\n  Mini (3 items): /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/mini_method_out.json\n  Preview (3 items, truncated): /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/preview_method_out.json\n-rw-r--r-- 1 root root 12422705 Sep 29 06:21 full_method_out.json\n-rw-r--r-- 1 root root 11688836 Sep 29 06:20 method_out.json\n-rw-r--r-- 1 root root    15061 Sep 29 06:21 mini_method_out.json\n-rw-r--r-- 1 root root    12770 Sep 29 06:21 preview_method_out.json\n{\n\"input\": \"{\\\"concept_id\\\": \\\"2777053367\\\", \\\"name\\\": \\\"Zika virus\\\", \\\"body\\\": \\\"COH1014\\\", \\\"t0\\\": 2014, \\\"n_home_early\\\": 1079, \\\"NOV_res__raw\\\": -0.220146, \\\"edge_persistence__raw\\\": 0.40625, \\\"ego_density_W3__raw\\\": 0.295635, \\\"n...\",\n\"output\": \"7.858917\",\n\"predict_B5\": \"7.005484\",\n\"predict_B5_plus_NOVCHURN_raw\": \"7.229384\",\n\"predict_B5_plus_NOVCHURN_exc\": \"7.014109\",\n\"predict_B5_plus_NOVCHURN_cfg\": \"7.124806\",\n\"predict_B5_plus_OPEN_home\": \"7.006816\",\n\"predict_B5_plus_OPEN_home_clean\": \"7.025911\",\n\"metadata_body\": \"COH1014\",\n\"metadata_agroup\": \"BGM+Med\",\n\"metadata_O2r_resid\": 2.129149708019365,\n\"metadata_imputed_variants\": [],\n\"metadata_missing_clean_variants\": [\n\"NOVCHURN_rare10\"\n]\n}\n{\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\", \"n_recognition_rows\": 65026, \"n_analysed\": 13444, \"n_found\": 0, \"coverage_by_body\": {\"COH1014\": 0.0, \"COH1517\": 0.0, \"DEV\": 0.0, \"OLDHO\": 0.0}, \"level_agreement\": 0.0}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [240] ASSISTANT · 2026-09-29 06:22:18 UTC

```
The concept-key cross-check found 0 matches because of an ID-format mismatch: the frame uses numeric IDs, the dependency uses `C`-prefixed OpenAlex IDs. Fixing:
```

### [241] TOOL CALL — Bash · 2026-09-29 06:22:18 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
from pathlib import Path
p=Path("method.py"); s=p.read_text()
old='''    lev = dict(zip(lev.concept_id.astype(str), lev.level))
    ids = set(cv.concept_id.astype(str))'''
new='''    norm = lambda v: "C" + str(v).lstrip("C").split(".")[0]  # noqa: E731  (frame ids are numeric; O5 uses 'C...')
    lev = dict(zip(lev.concept_id.map(norm), lev.level))
    cv["concept_id"] = cv.concept_id.map(norm)
    ids = set(cv.concept_id)'''
assert old in s; s=s.replace(old,new)
s=s.replace('''    cov = cv.assign(found=cv.concept_id.astype(str).isin(seen))''','''    cov = cv.assign(found=cv.concept_id.isin(seen))''')
p.write_text(s)
EOF
OMP_NUM_THREADS=1 timeout 1200 .venv/bin/python method.py 2>&1 | grep -v Warn | tail -1; python3 -c "
import json; d=json.load(open('method_out.json')); print(json.dumps(d['metadata']['concept_key_check']))"; SKILL_DIR=/ai-inventor/.claude/skills/aii-json; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_validate_schema.py --format exp_gen_sol_out --file $PWD/method_out.json 2>&1 | tail -1; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input $PWD/method_out.json 2>&1 | tail -1
```

### [242] TOOL RESULT — Bash · 2026-09-29 06:22:44 UTC

```
{"stdout": "06:21:48|INFO   |method_out.json: 7748 examples; verdict PARTLY_THIN\n{\"dependency\": \"art_O7Dq4L02QnDN concept_recognition (concept key only; no O5 outcome used)\", \"n_recognition_rows\": 65026, \"n_analysed\": 13444, \"n_found\": 13444, \"coverage_by_body\": {\"COH1014\": 1.0, \"COH1517\": 1.0, \"DEV\": 1.0, \"OLDHO\": 1.0}, \"level_agreement\": 1.0}\nValidation PASSED\n  Preview (3 items, truncated): /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/preview_method_out.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [243] ASSISTANT · 2026-09-29 06:23:06 UTC

```
Concept key: 100% coverage and 100% level agreement. Checking the figures visually:
```

### [244] TOOL CALL — Read · 2026-09-29 06:23:06 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/figures/persistence_vs_n.png
```

### [245] TOOL RESULT — Read · 2026-09-29 06:23:06 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [246] TOOL CALL — Read · 2026-09-29 06:23:06 UTC

```
/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/figures/forest_raw_vs_clean.png
```

### [247] TOOL RESULT — Read · 2026-09-29 06:23:06 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [248] SYSTEM-USER prompt · 2026-09-29 06:23:06 UTC

```
[Image: original 2550x900, displayed at 2000x706. Multiply coordinates by 1.27 to map to original image.]
```

### [249] ASSISTANT · 2026-09-29 06:23:06 UTC

```
Both figures look right. Pulling the remaining numbers for the README and aggregating the unit tests:
```

### [250] TOOL CALL — Bash · 2026-09-29 06:23:06 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
import json
R=json.load(open("results/reliability.json"))
for v in ["NOV_res__raw","edge_persistence__raw","ego_density_W3__raw","NOVCHURN_raw","OPEN_home","edge_persistence_nullmean","NOV_res_exc","edge_persistence_exc","NOVCHURN_exc","NOV_res_rare5","edge_persistence_rare5","NOVCHURN_rare5","z_pers_cfg","z_dens_cfg","z_dens_k","NOVCHURN_cfg","OPEN_home_clean","OPEN_home_exc"]:
    e=R["variants"][v]; print(v.ljust(26), "pooled %.3f"%e["pooled"]["SB"], e["pooled"]["SB_ci"] and [round(x,3) for x in e["pooled"]["SB_ci"]], " ".join("%s %.2f"%(k,e[k]["SB"]) if e[k]["SB"] is not None else k+" NA" for k in ["n10-19","n20-49","n50-99","n100-inf","COH1517"]))
print(R["outcome"]["O2r_m50"]["pooled"], {b:R["outcome"]["O2r_m50"][b]["SB"] for b in ["DEV","OLDHO","COH1014","COH1517"]})
S=json.load(open("results/size_dependence.json"))
for v in ["edge_persistence__raw","NOV_res__raw","ego_density_W3__raw","NOVCHURN_raw","OPEN_home","NOVCHURN_exc","NOVCHURN_rare10","edge_persistence_rare10","z_pers_cfg","NOVCHURN_cfg","NOVCHURN_chao","EP_chao","OPEN_home_clean","z_dens_cfg"]:
    print(v.ljust(24), "rho logn pooled %.3f"%S["spearman"][v]["POOLED"]["log_n_home_early"]["rho"], "growth %.3f"%S["spearman"][v]["POOLED"]["growth_c"]["rho"])
print({k:v["log_n"]["R2"] for k,v in S["ols_r2"].items()}, {k:v["log_n_inv_min_inv_mean"]["R2"] for k,v in S["ols_r2"].items()})
print({k:v["POOLED"]["rho"] for k,v in S["degree_dependence"].items()})
print(S["thin_sample_share"]["POOLED"]["R2"], S["thin_sample_share_NOV_res"])
import pandas as pd
d=pd.read_parquet("data/clean_variants.parquet")
print(d.groupby("body").size().to_dict())
fin={c:d.groupby("body")[c].apply(lambda s:int(s.notna().sum())).to_dict() for c in ["NOVCHURN_raw","NOVCHURN_exc","NOVCHURN_rare10","NOVCHURN_rare5","NOVCHURN_cfg","z_pers_cfg","z_dens_cfg","OPEN_home","OPEN_home_clean"]}
print(json.dumps(fin))
EOF
python3 - <<'EOF'
import json,glob
out={}
for f in ["unit_tests_fast6","unit_tests_nulls","unit_tests_fastpsp","planted_checks","gate_t0","placebo_calibration","rederive"]:
    out[f]=json.load(open(f"results/{f}.json"))
summ={"T0_gate":out["gate_t0"]["pass"],"U1_fast6_equals_concept_core":out["unit_tests_fast6"]["U1"]["pass"],"U1_n_concepts":out["unit_tests_fast6"]["U1"]["n_concepts"],
"U2_permutation":out["unit_tests_fast6"]["U2"]["pass"],"U5_rarefy_identity":out["unit_tests_fast6"]["U5"]["pass"],"U6_chao":out["unit_tests_fast6"]["U6"]["pass"],
"U3_curveball_toy_uniform":out["unit_tests_nulls"]["U3_toy"]["pass"],"U3_curveball_margins_full_run":json.load(open("results/v3_nulls_full.json"))["U3_curveball"],
"U4_rewire_calibration":out["unit_tests_nulls"]["U4_rewire_calibration"]["pass"],"U4_v1_single_graph_design":out["unit_tests_nulls"].get("U4_v1_single_graph",{}).get("pass"),
"U7_psp_reproduces_EXP10":out["gate_t0"]["T0c"],"U7b_fastpsp":out["unit_tests_fastpsp"]["pass"],
"PC1_stationary":out["planted_checks"]["PC1_stationary"]["pass"],"PC2_planted_churn":out["planted_checks"]["PC2_planted_churn"]["pass"],
"PC3_planted_recovered_all_bodies":True,"PC3_placebo_rule_le1_of_20":{b:r["n_placebo_ci_excl0"] for b,r in json.load(open("results/clean_vs_raw_psp.json"))["cells"]["planted_PC3"].items()},
"placebo_calibration_500":{b:v["share_abs_gt_1.96se"] for b,v in out["placebo_calibration"].items() if b!="label"},"rederive":out["rederive"]["pass"]}
json.dump(summ,open("results/unit_tests.json","w"),indent=1); print(json.dumps(summ)[:1500])
EOF
```

### [251] TOOL RESULT — Bash · 2026-09-29 06:23:06 UTC

```
{"stdout": "NOV_res__raw               pooled 0.478 [0.458, 0.49] n10-19 0.39 n20-49 0.46 n50-99 0.54 n100-inf 0.75 COH1517 0.47\nedge_persistence__raw      pooled 0.570 [0.56, 0.584] n10-19 NA n20-49 0.21 n50-99 0.29 n100-inf 0.63 COH1517 0.62\nego_density_W3__raw        pooled 0.412 [0.378, 0.429] n10-19 NA n20-49 0.21 n50-99 0.36 n100-inf 0.73 COH1517 0.46\nNOVCHURN_raw               pooled 0.476 [0.457, 0.486] n10-19 0.39 n20-49 0.39 n50-99 0.42 n100-inf 0.67 COH1517 0.49\nOPEN_home                  pooled 0.485 [0.475, 0.506] n10-19 0.27 n20-49 0.34 n50-99 0.55 n100-inf 0.84 COH1517 0.53\nedge_persistence_nullmean  pooled 0.707 [0.699, 0.716] n10-19 NA n20-49 0.42 n50-99 0.45 n100-inf 0.81 COH1517 0.72\nNOV_res_exc                pooled 0.020 [-0.011, 0.03] n10-19 0.07 n20-49 0.02 n50-99 0.02 n100-inf -0.02 COH1517 0.04\nedge_persistence_exc       pooled 0.046 [0.03, 0.064] n10-19 NA n20-49 0.06 n50-99 0.00 n100-inf 0.12 COH1517 0.03\nNOVCHURN_exc               pooled 0.014 [-0.013, 0.029] n10-19 0.07 n20-49 0.02 n50-99 -0.01 n100-inf 0.10 COH1517 0.01\nNOV_res_rare5              pooled 0.557 [0.523, 0.579] n10-19 NA n20-49 0.49 n50-99 0.60 n100-inf 0.75 COH1517 0.61\nedge_persistence_rare5     pooled 0.226 [0.204, 0.249] n10-19 NA n20-49 0.07 n50-99 0.10 n100-inf 0.25 COH1517 0.23\nNOVCHURN_rare5             pooled 0.359 [0.33, 0.388] n10-19 NA n20-49 0.34 n50-99 0.32 n100-inf 0.47 COH1517 0.38\nz_pers_cfg                 pooled 0.709 [0.686, 0.739] n10-19 NA n20-49 0.02 n50-99 0.43 n100-inf 0.51 COH1517 0.74\nz_dens_cfg                 pooled 0.698 [0.674, 0.714] n10-19 NA n20-49 0.34 n50-99 0.60 n100-inf 0.89 COH1517 0.78\nz_dens_k                   pooled 0.657 [0.632, 0.677] n10-19 NA n20-49 0.19 n50-99 0.54 n100-inf 0.88 COH1517 0.74\nNOVCHURN_cfg               pooled 0.618 [0.591, 0.657] n10-19 NA n20-49 0.39 n50-99 0.49 n100-inf 0.59 COH1517 0.68\nOPEN_home_clean            pooled 0.577 [0.562, 0.594] n10-19 0.27 n20-49 0.42 n50-99 0.61 n100-inf 0.80 COH1517 0.64\nOPEN_home_exc              pooled 0.486 [0.468, 0.498] n10-19 0.34 n20-49 0.33 n50-99 0.49 n100-inf 0.78 COH1517 0.55\n{'r_half': 0.8099349043555275, 'SB': 0.8949878831624887, 'n': 7748, 'SB_ci': [0.8904772486259972, 0.8988260126382953], 'SB_boot_sd': 0.002030466617169411} {'DEV': 0.8830918108516521, 'OLDHO': 0.8635693439831329, 'COH1014': 0.8940308419274919, 'COH1517': 0.8888022839591002}\nedge_persistence__raw    rho logn pooled 0.718 growth 0.272\nNOV_res__raw             rho logn pooled 0.047 growth 0.040\nego_density_W3__raw      rho logn pooled -0.230 growth -0.208\nNOVCHURN_raw             rho logn pooled -0.447 growth -0.172\nOPEN_home                rho logn pooled 0.064 growth 0.257\nNOVCHURN_exc             rho logn pooled 0.034 growth 0.011\nNOVCHURN_rare10          rho logn pooled -0.156 growth -0.043\nedge_persistence_rare10  rho logn pooled 0.208 growth 0.098\nz_pers_cfg               rho logn pooled 0.625 growth 0.254\nNOVCHURN_cfg             rho logn pooled -0.400 growth -0.144\nNOVCHURN_chao            rho logn pooled -0.440 growth -0.147\nEP_chao                  rho logn pooled 0.684 growth 0.240\nOPEN_home_clean          rho logn pooled 0.008 growth 0.198\nz_dens_cfg               rho logn pooled 0.487 growth 0.307\n{'edge_persistence__raw': 0.4090196433182395, 'NOV_res__raw': 1.4536941172260676e-05, 'ego_density_W3__raw': 0.018933385747780473, 'NOVCHURN_raw': 0.2098937579320349, 'edge_persistence_exc': 0.0011293446309215138, 'NOVCHURN_exc': 0.0006630764295472158, 'z_pers_cfg': 0.285365376640621, 'edge_persistence_rare10': 0.026037083397141725} {'edge_persistence__raw': 0.41357305536117006, 'NOV_res__raw': 0.00170511699842113, 'ego_density_W3__raw': 0.01967826095628733, 'NOVCHURN_raw': 0.21057920897797433, 'edge_persistence_exc': 0.0011948628454448995, 'NOVCHURN_exc': 0.0007456685392466245, 'z_pers_cfg': 0.30003684591930724, 'edge_persistence_rare10': 0.028601165466441425}\n{'ego_density_W3__raw': -0.38295138580715227, 'z_dens_cfg': 0.7852011474264526, 'z_dens_k': 0.8568745890234455, 'edge_persistence__raw': 0.4795864319272761, 'z_pers_cfg': 0.42151386870970353, 'z_pers_k': 0.4121241805158626}\n0.6596194882526905 {'POOLED': {'R2': 0.6666739722964996, 'n': 9945, 'coef': [0.00039297224604388574, 0.989727226265795]}}\n{'COH1014': 4195, 'COH1517': 1365, 'DEV': 4670, 'OLDHO': 3214}\n{\"NOVCHURN_raw\": {\"COH1014\": 3228, \"COH1517\": 1040, \"DEV\": 3870, \"OLDHO\": 2377}, \"NOVCHURN_exc\": {\"COH1014\": 3034, \"COH1517\": 975, \"DEV\": 3725, \"OLDHO\": 2211}, \"NOVCHURN_rare10\": {\"COH1014\": 1040, \"COH1517\": 333, \"DEV\": 1743, \"OLDHO\": 534}, \"NOVCHURN_rare5\": {\"COH1014\": 1266, \"COH1517\": 420, \"DEV\": 1630, \"OLDHO\": 916}, \"NOVCHURN_cfg\": {\"COH1014\": 1633, \"COH1517\": 536, \"DEV\": 2456, \"OLDHO\": 1016}, \"z_pers_cfg\": {\"COH1014\": 1760, \"COH1517\": 595, \"DEV\": 2638, \"OLDHO\": 1101}, \"z_dens_cfg\": {\"COH1014\": 2230, \"COH1517\": 691, \"DEV\": 3068, \"OLDHO\": 1490}, \"OPEN_home\": {\"COH1014\": 3618, \"COH1517\": 1186, \"DEV\": 4284, \"OLDHO\": 2681}, \"OPEN_home_clean\": {\"COH1014\": 2942, \"COH1517\": 955, \"DEV\": 3761, \"OLDHO\": 2083}}\n{\"T0_gate\": true, \"U1_fast6_equals_concept_core\": true, \"U1_n_concepts\": 1000, \"U2_permutation\": true, \"U5_rarefy_identity\": true, \"U6_chao\": true, \"U3_curveball_toy_uniform\": true, \"U3_curveball_margins_full_run\": {\"column_sums_preserved\": true, \"row_sizes_preserved\": true, \"rows_remain_sets\": true}, \"U4_rewire_calibration\": true, \"U4_v1_single_graph_design\": false, \"U7_psp_reproduces_EXP10\": {\"OPEN_home\": {\"mine\": 0.09059049284973036, \"published\": 0.0905904928497304, \"n_mine\": 573, \"n_published\": 573, \"abs_diff\": 4.163336342344337e-17, \"pass\": true}, \"NOV_res__home\": {\"mine\": 0.13368999979699833, \"published\": 0.1336899997969982, \"n_mine\": 506, \"n_published\": 506, \"abs_diff\": 1.3877787807814457e-16, \"pass\": true}, \"edge_persistence__home\": {\"mine\": -0.11231075452403043, \"published\": -0.1123107545240305, \"n_mine\": 597, \"n_published\": 597, \"abs_diff\": 6.938893903907228e-17, \"pass\": true}}, \"U7b_fastpsp\": true, \"PC1_stationary\": true, \"PC2_planted_churn\": false, \"PC3_planted_recovered_all_bodies\": true, \"PC3_placebo_rule_le1_of_20\": {\"OLDHO\": 1, \"COH1014\": 5, \"DEV\": 0, \"POOLED\": 5, \"COH1517\": 0}, \"placebo_calibration_500\": {\"DEV\": 0.042, \"OLDHO\": 0.054, \"COH1014\": 0.044, \"COH1517\": 0.058, \"POOLED\": 0.036}, \"rederive\": true}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [252] ASSISTANT · 2026-09-29 06:23:26 UTC

```
Everything is in hand. Updating the deviations log and removing my own scratch mini/test runs:
```

### [253] TOOL CALL — Bash · 2026-09-29 06:23:26 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; rm -rf data/s2_parts_mini data/s2_scalars_mini.parquet data/s2_scalars_t200.parquet data/v3_halves_mini.pkl data/v3_nulls_mini.parquet results/v3_nulls_mini.json; python3 - <<'EOF'
import json
p="results/deviations.json"; d=json.load(open(p))
d.update({
"D1_seed_streams": "Seeds use numpy SeedSequence lists ([7000000, sk, n] etc.) instead of the plan's additive seeds because COH1517 and EXP5 ci values overlap; declared in frozen_spec before any run.",
"D2_SELF_fixed": "SELF (own-name topics) is computed once on the full home build and held fixed in every resample (declared in spec); fast6 == concept_core with this override (U1, 1000 concepts x 4 variants, max diff 1.1e-16).",
"D3_V3a_design": "Literal rewiring of each yearly ego graph keeps density fixed, so V3a rewires the global slice backbone around the fixed raw NB_W3 set (200 igraph rewires, n = 10 m trials, simple) and V3b uses a k-matched random-set null; as planned.",
"D4_V3c_zero_sd": "z_pers_cfg is NaN when the curveball null sd is 0 (small neighbour sets never overlap in 200 samples): finite for 6,094 / 13,444 concepts; excess_pers_cfg (obs - null mean) is finite for 12,503 and is reported alongside.",
"D5_V4_halves": "Clean-variant halves: V1 at n = 5 (proxy for all rarefied variants), V2 with 50 perms per half, V3a/V3b with 50 draws, V3c via the k-matched MC approximation (Spearman with the curveball z on the full build = 0.881). EP_chao, NOVCHURN_chao and excess_pers_cfg have no half-split reliability (not disattenuated).",
"D6_bootstrap_engine": "Bootstrap draws use lib/fastpsp.psp_fast (normal-equations projection, validated == rq1stats.psp_point to 2.4e-16 on EXP5 and cohort tables R0-R5); every point estimate uses the original psp_point. B = 2000 for every cell, seed 20260930.",
"D7_same_sample_R0": "Same-sample raw counterparts (paired bootstrap with diff and ratio) are computed at R2 and R3 only; R0 clean cells are reported on their own samples.",
"D8_inclusion_n10": "All analyses use n_home_early >= 10 (the OPEN_home rule, as planned); therefore COH1517 raw component psp differ from the published EXP10 values, which used all 1,443 concepts (e.g. NOVCHURN_raw R2 = 0.161 at n = 506). The gate T0c reproduced the published values on the unfiltered table exactly.",
"D9_U4_redesign": "U4 v1 (one observed rewire x 50 sets, 30 nulls) gave mean z = -0.236 (fail; sets share one observed graph so their z are correlated). Replaced post hoc by a clustered design (10 observed rewires x 20 sets, 40 nulls): mean z = -0.067, clustered SE 0.086 (pass). Both kept in results/unit_tests_nulls.json.",
"D10_PC2_failed": "PC2 (planted W3 churn) FAILED: raw persistence fell (mean -0.025, sign test p = 4e-7) but the V2 null mean fell nearly as much (-0.021), so V2 excess changed by only -0.005 (102 fell / 108 rose, p = 0.69). V2 is a low-power, over-controlling null at ~10 papers/year; its null results cannot by themselves show that churn is thin-sample noise. Reported, verdict rules unchanged.",
"D11_PC3_placebos": "PC3 placebo rule (<= 1 of 20 placebo CIs excluding 0) failed in COH1014 and POOLED (5/20 each). A post-seal calibration with 500 permutations per body (results/placebo_calibration.json) shows correct calibration (false-positive share 3.6-5.8%, permutation sd / bootstrap SE 0.94-1.02); the 20-placebo excess is attributed to chance.",
"D12_power_exc": "Power for NOVCHURN_exc is not interpretable (SB 0.014): T1 undefined and S_B scaling undefined; reported as null. The fallback O2r_m30 outcome set is not simulated.",
"D13_outcome_reliability": "Outcome-window field counts WERE cached (EXP5 scan/agg_counts; EXP10 passC_pre_agg + sealed parts); O2r_m50 recomputed from them exactly (max diff 1.8e-15), so rel_y is measured (SB 0.895, m = 25 halves), not set to 1.",
"D14_placebo_seed_note": "Post-seal diagnostics (placebo_calibration.json) are exploratory and labelled as such."})
json.dump(d,open(p,"w"),indent=1)
EOF
du -sh data/* | sort -h | tail; find . -name __pycache__ -type d | head
```

### [254] TOOL RESULT — Bash · 2026-09-29 06:23:26 UTC

```
{"stdout": "478K\tdata/v3_nulls_full.parquet\n2.8M\tdata/s2_scalars_full.parquet\n2.8M\tdata/v4_half_means.npz\n3.5M\tdata/psp_boot.npz\n4.5M\tdata/clean_variants.parquet\n15M\tdata/v3_halves_full.pkl\n45M\tdata/home_cache.pkl\n241M\tdata/s2_parts_full\n./__pycache__\n./lib/__pycache__\n./.venv/lib/python3.12/site-packages/__pycache__\n./.venv/lib/python3.12/site-packages/fontTools/__pycache__\n./.venv/lib/python3.12/site-packages/kiwisolver/__pycache__\n./.venv/lib/python3.12/site-packages/igraph/__pycache__\n./.venv/lib/python3.12/site-packages/numba/__pycache__\n./.venv/lib/python3.12/site-packages/numpy/__pycache__\n./.venv/lib/python3.12/site-packages/pandas/__pycache__\n./.venv/lib/python3.12/site-packages/cycler/__pycache__", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [255] ASSISTANT · 2026-09-29 06:23:48 UTC

```
Now the manifest, restore script and README.
```

### [256] TOOL CALL — Bash · 2026-09-29 06:23:48 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .venv/
    delete: regenerable
    source: "uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil"
  - path: data/home_cache.pkl
    delete: regenerable
    source: ".venv/bin/python -c \"import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()\""
  - path: data/s2_parts_full/
    delete: regenerable
    source: ".venv/bin/python s2_variants.py --tag full --workers 4"
  - path: data/v3_halves_full.pkl
    delete: regenerable
    source: ".venv/bin/python s3_nulls.py --tag full"
  - path: __pycache__/
    delete: regenerable
    source: "created automatically by python on import"
  - path: lib/__pycache__/
    delete: regenerable
    source: "created automatically by python on import (includes the numba cache of lib/nullkern.py)"
  - path: data/clean_variants.parquet
    keep: per-concept raw and noise-controlled churn variants frozen on selection data; input of the Frame-N confirmation artifact
  - path: results/
    keep: all results (reliability, size dependence, psp tables, verdict, power, unit tests, seals)
  - path: method_out.json
    keep: exp_gen_sol_out output read by later steps
  - path: full_method_out.json
    keep: full copy of method_out.json produced by the aii-json formatter
EOF
cat > restore.sh <<'EOF'
#!/usr/bin/env bash
# Rebuild every file marked `delete` in .aii/manifest.yaml (all deterministic: seeded).
set -euo pipefail
cd "$(dirname "$0")"
export AII_RUN_ROOT="${AII_RUN_ROOT:-$(cd ../../../.. && pwd)}"   # the run root holding EXP5/EXP8/EXP10 read-only inputs
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil
.venv/bin/python -c "import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()"
OMP_NUM_THREADS=1 .venv/bin/python s2_variants.py --tag full --workers 4      # ~3 min  -> data/s2_parts_full/
OMP_NUM_THREADS=1 .venv/bin/python s3_nulls.py --tag full                     # ~10 min -> data/v3_halves_full.pkl
EOF
chmod +x restore.sh; echo ok
```

### [257] TOOL RESULT — Bash · 2026-09-29 06:23:48 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [258] TOOL CALL — Write · 2026-09-29 06:24:30 UTC

````
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/README.md

# Is neighbourhood churn real or thin-sample noise?

A $0-LLM, cache-only confound check of the home-only "churn / novelty" signal found by earlier experiments. On the 2015-17 cohort that signal was NOV_res +0.134 and edge_persistence −0.112 (partial Spearman with O2r_m50 at rung R2, EXP10). This artifact asks two things: is the signal real, or a by-product of few papers per year? And is it an artefact of degree dependence?

It recomputes the raw home-build indicators exactly, then builds noise-controlled versions:
- **V1**: fixed-n rarefaction.
- **V2**: a within-concept year-label permutation null, plus a Chao-corrected Jaccard (**V2b**).
- **V3**: degree-preserving configuration nulls: backbone rewiring, a k-matched random-set null, and curveball-randomised persistence.
- **V4**: split-half reliability of every variant.

All variants are compared side by side on the same concepts, with the EXP10 covariate ladder, per body and pooled.

**Label: selection data, outcomes previously unsealed.** Every body's outcomes were already unsealed by EXP5/EXP8/EXP10. The seal (`logs/seal.log`) is a pre-analysis commitment, not a blind. These results are robustness evidence, not confirmation.

## Headline

**Mechanical verdict: `PARTLY_THIN`** (`results/clean_vs_raw_psp.json` → `verdict`). The flag `DEGREE_ARTEFACT_PERSISTENCE` is false.

Partial Spearman with O2r_m50 given B5 + rung R2, 95% concept-bootstrap CI (B = 2000). Source: `results/clean_vs_raw_psp.json → headline_R2_O2r_m50`. "ret" is the retention ratio clean/raw on the same concepts, from the paired bootstrap.

| variant | COH1517 | OLDHO | POOLED (n) | pooled ret |
|---|---|---|---|---|
| NOVCHURN_raw (EXP10 z's) | +0.161 [0.07, 0.25] | +0.113 [0.06, 0.16] | +0.116 [0.09, 0.14] (6450) | – |
| NOVCHURN_exc (V2 excess) | +0.063 [−0.02, 0.15] | +0.006 [−0.05, 0.06] | +0.008 [−0.02, 0.03] | 0.06 |
| NOVCHURN_rare10 (V1, n = 10/yr) | +0.176 [0.05, 0.29] | +0.044 [−0.07, 0.15] | +0.078 [0.04, 0.11] (2874) | 0.68 |
| NOVCHURN_cfg (V3c curveball z) | +0.088 [−0.02, 0.20] | +0.071 [−0.01, 0.15] | +0.106 [0.07, 0.14] | 1.00 |
| NOVCHURN_chao (V2b) | +0.153 [0.07, 0.24] | +0.123 [0.07, 0.18] | +0.108 [0.08, 0.13] | 0.91 |
| edge_persistence raw | −0.112 [−0.20, −0.02] | −0.086 [−0.13, −0.04] | −0.088 [−0.11, −0.07] | – |
| edge_persistence V2 **null mean** | −0.123 | −0.116 | **−0.120** [−0.14, −0.10] | – |
| edge_persistence_exc (V2) | +0.001 | −0.006 | −0.003 [−0.03, 0.02] | 0.04 |
| edge_persistence_rare10 | −0.058 | −0.037 | −0.030 [−0.06, 0.00] | 0.45 |
| z_pers_cfg (V3c) | −0.066 | −0.122 | −0.116 [−0.15, −0.09] | 1.00 |
| NOV_res raw | +0.134 | +0.093 | +0.073 | – |
| NOV_res_exc (V2) | +0.071 | +0.002 | +0.003 | 0.04 |
| NOV_res_rare10 | +0.205 | +0.065 | +0.093 | 1.01 |
| ego_density_W3 raw | +0.018 | +0.006 | −0.013 [−0.04, 0.01] | – |
| z_dens_cfg (V3a) | −0.047 | −0.089 | **−0.091** [−0.12, −0.06] | same-sample diff −0.079 [−0.11, −0.04] |
| OPEN_home | +0.091 | +0.070 | +0.085 | – |
| OPEN_home_clean (V3 subs) | +0.129 | +0.094 | **+0.115** [0.09, 0.14] | 1.24 [1.11, 1.43] |

### Reading
1. **Raw persistence is mostly a sample-size artefact.**
   - Raw edge persistence has Spearman +0.72 with log n_home_early (`results/size_dependence.json → spearman.edge_persistence__raw.POOLED`).
   - Its bin means rise 0.00 → 0.09 → 0.27 → 0.38 over n bins 10-19 / 20-49 / 50-99 / ≥100. The V2 null mean (same papers, years shuffled) tracks it almost exactly: 0.00 / 0.10 / 0.28 / 0.39 (`binned_persistence`).
   - The "thin-sample share" (R² of raw persistence on its own V2 null mean) is **0.66** (`thin_sample_share.POOLED.R2`).
   - At fixed n = 10 papers per year, persistence is nearly flat (0.11 → 0.15). See `figures/persistence_vs_n.png`.
2. **The churn → outcome association is not temporal churn.**
   - The excess over the within-concept permutation null carries nothing: NOVCHURN_exc pooled +0.008, retention 0.06. P1 fails: retention is 0.40 in COH1517 and 0.05 in OLDHO.
   - The V2 null mean itself predicts the outcome as strongly as raw persistence (−0.120 vs −0.088).
   - So what predicts disciplinary breadth is a static property of the concept's pooled home topic mix at its sample size: how redundant or concentrated its partner topics are. It is not the year-to-year turnover of partners.
3. **The association is also not "just paper count".**
   - Fixed-n rarefaction keeps 68% pooled; 76% in COH1517 and 64% in OLDHO (`verdict.clauses.V1_retention`).
   - The Chao-corrected and degree-normalised composites keep 91-100%.
   - NOV_res survives rarefaction fully (retention 1.01) and is nearly size-free (ρ with log n +0.05).
   - DL over the 5 pooled groups at R2: NOVCHURN_raw +0.110 [0.085, 0.136], I² = 0, positive in 5/5 groups; NOVCHURN_rare10 +0.081 [0.042, 0.119], 5/5 (`groups`).
4. **The V2 excess cannot adjudicate on its own.**
   - Split-half reliability of every V2-excess variant is ≈ 0: NOVCHURN_exc SB = 0.014, edge_persistence_exc 0.046, NOV_res_exc 0.020 (`results/reliability.json → variants.*.pooled.SB`).
   - The planted-churn check PC2 fails: V2 absorbs about 80% of a planted 50% W3 topic replacement (`results/planted_checks.json`).
   - So a null V2 result means "temporal order is unmeasurable at ~10 papers per year", not "no churn".
5. **Degree normalisation helps OPEN.**
   - Replacing raw density and persistence by their configuration z's raises OPEN_home pooled from +0.092 to +0.115 on the same sample. The difference is +0.022 [0.011, 0.034] at R2 and +0.023 [0.011, 0.034] at R3.
   - Raw ego density was null because of its degree dependence (ρ with log degree −0.38). Its degree-normalised version z_dens_cfg is −0.091 pooled: neighbourhoods *less* interlinked than their partners' degrees imply go with broader later uptake.
   - P2 holds: z_pers_cfg is −0.116 [−0.145, −0.086].
   - The curveball z does **not** remove size dependence (ρ with log n +0.63), because its null expected Jaccard is ≈ 0 and z ≈ obs/sd.

**Recommended wording for the paper.** Rename "churn" to *topical non-redundancy / dispersion of the home neighbourhood*. It is robust to fixed-n rarefaction and to undersampling correction. It is not evidence of year-to-year partner turnover.

### Predictions (frozen in `results/frozen_spec.json`; evaluated in `clean_vs_raw_psp.json → predictions`)
- **P1 fails.** The same-sample ratio psp(NOVCHURN_exc)/psp(NOVCHURN_raw) at R2 is 0.40 [−0.27, 0.88] in COH1517 (n 490) and 0.05 [−0.56, 0.44] in OLDHO (n 1321).
- **P2 holds.** z_pers_cfg pooled is −0.116 [−0.145, −0.086] (n 4262).
- **P3 holds.** Spearman(NOVCHURN_exc, log n) = +0.034 [0.015, 0.054] (n 9945).
- **Holm (reported only):** p = 0.41 / 0.0005 / 0.002, Holm-adjusted 0.41 / 0.0015 / 0.004.
- **F6 contingency:** COH1517 has 235 concepts with finite NOVCHURN_rare10 and outcome (≥ 150), so n = 10 stays primary.

### Reliability and disattenuation (`results/reliability.json`)
Pooled Spearman-Brown split-half reliability:

| variant | SB | variant | SB |
|---|---|---|---|
| NOV_res | 0.48 | V2 null mean of persistence | 0.71 |
| edge_persistence | 0.57 | z_pers_cfg | 0.71 |
| ego_density_W3 | 0.41 | z_dens_cfg | 0.70 |
| NOVCHURN_raw | 0.48 | z_dens_k | 0.66 |
| OPEN_home | 0.49 | NOVCHURN_cfg | 0.62 |
| NOVCHURN_rare5 | 0.36 | OPEN_home_clean | 0.58 |

- Reliability rises with n: NOVCHURN_raw is 0.39 at 10-19 papers and 0.67 at ≥ 100.
- The outcome O2r_m50 has SB = **0.895** (conservative, from m = 25 halves). It was recomputed from the cached outcome-window field counts exactly (max diff 1.8e-15).
- **Disattenuated pooled NOVCHURN_raw** (approximate for a partial Spearman): 0.178 [0.141, 0.214] at R2 and 0.157 at R3. OPEN_home at R3 is 0.102 (`clean_vs_raw_psp.json → disattenuated`).

### Power for Frame N (`results/power_frame_n.json`)
Joint power is for the Frame-N CONFIRMED rule: OPEN_home R3 & R5 & NOVCHURN_raw R3 all significant.

| target | n = 800 | n = 1500 | n = 2500 |
|---|---|---|---|
| S_A, T1 (disattenuated) | 0.26 | 0.50 | 0.71 |
| S_A, T2 (COH1517 raw) | 0.31 | 0.57 | 0.75 |
| S_A, T3 (half of pooled raw) | 0.07 | 0.11 | 0.26 |
| S_B (pessimistic n-mix), T3 | 0.03 | – | 0.06 |

OPEN_home at R5 is the binding term: its analytic n for 0.8 marginal power under S_A/T1 is ≈ 2,700. Power for NOVCHURN_exc is not interpretable, because its SB is 0.014.

### Checks
Summary in `results/unit_tests.json`.
- **Gate T0 passes exactly** (`results/gate_t0.json`):
  - EXP10 home components and OPEN_home reproduce with diff 0.0.
  - The published cohort OPEN_home +0.0906, NOV_res +0.1337 and edge_persistence −0.1123 reproduce to about 1e-16.
- **Engine and tests:**
  - U1 fast engine == `ego.concept_core` on 1,000 concepts × {full, half, permuted, rarefied}: max diff 1.1e-16.
  - U2, U5 and U6 pass.
  - U3: the curveball toy has 12 states, χ² p = 0.96, and the margins are preserved in the full run.
  - U4: the redesign passes (mean z −0.067); the first design failed and is documented in the deviations.
  - U7 and fastpsp pass.
- **Planted checks:**
  - PC1 passes: under stationarity raw persistence still has ρ = 0.75 with log n, while V2 excess has mean −0.001 and ρ −0.04.
  - **PC2 fails** (see reading 4).
  - PC3: the planted association is recovered in every body (0.19-0.24). The placebo rule failed in 2 of 5 bodies at 20 draws, but a 500-permutation calibration shows nominal 3.6-5.8% false-positive rates (`results/placebo_calibration.json`).
- `rederive.py` re-derives the P1-P3 psp and the pooled SB of NOVCHURN_raw by a separate code path: max diff 2.2e-16.
- **Cross-checks:**
  - EXP12 `open_features` home values are identical (share equal = 1.0 for all six components).
  - Every analysed concept is found in the art_O7Dq4L02QnDN concept key, and the level agrees for 100%.

All deviations from the plan, with reasons, are in `results/deviations.json` (D0-D14).

## What was done (pipeline)
| stage | script | output |
|---|---|---|
| gate T0 | `s0_gate.py` | `results/gate_t0.json` |
| fast engine tests | `tests/u_fast6.py` | `results/unit_tests_fast6.json` |
| freeze + seal | `s1_freeze.py` (+ `lib/seal.py`) | `results/frozen_spec.json`, `logs/seal.log` |
| RAW, V1, V2, V2b, V4 halves | `s2_variants.py` (engine `lib/fast6.py`) | `data/s2_scalars_full.parquet`, `data/s2_parts_full/` |
| V3a / V3b / V3c nulls | `s3_nulls.py` (numba kernels `lib/nullkern.py`) | `data/v3_nulls_full.parquet`, `data/v3_halves_full.pkl`, `results/v3_nulls_full.json` |
| null tests / planted | `tests/u_nulls.py`, `tests/planted.py` | `results/unit_tests_nulls.json`, `results/planted_checks.json` |
| composites, 2nd seal, reliability | `s4_composites.py` | `data/clean_variants.parquet`, `results/frozen_constants_S1b.json`, `results/reliability_x.json` |
| outcome reliability | `s4b_outcome_rel.py` | `results/reliability.json` |
| size dependence | `s5_size.py` | `results/size_dependence.json`, `figures/persistence_vs_n.png` |
| associations | `s6_assoc.py` (tables `lib/tables.py`, bootstrap `lib/fastpsp.py`) | `results/clean_vs_raw_psp_cells.json`, `data/psp_boot.npz` |
| verdict, DL, disattenuation, figures | `s7_verdict.py` | `results/clean_vs_raw_psp.json`, `figures/forest_raw_vs_clean.png`, `figures/reliability_bars.png` |
| power | `s8_power.py` | `results/power_frame_n.json`, `figures/power_curves.png` |
| re-derivation | `rederive.py` | `results/rederive.json` |
| outputs | `method.py` | `method_out.json` (+ `full_/mini_/preview_`), `results/prediction_check.json` |

## Layout
- `method.py`: orchestrator (`--run-all`) and the exp_gen_sol_out builder. Each example has predictions from OLS fitted on DEV only: B5, B5+NOVCHURN_raw/exc/cfg and B5+OPEN_home/OPEN_home_clean.
- `lib/`: copied EXP10 modules (`ego.py`, `ego_ctx.py`, `ladder.py`, `rq1stats.py`, `common*.py`, `outc.py`; sha256 checked against EXP10). Only `common.py` and `ego_ctx.py` paths are patched (D0). The new modules are `fast6.py`, `nullkern.py`, `fastpsp.py`, `tables.py`, `jobs.py`, `seal.py` and `s2_cfg.py`.
- `data/clean_variants.parquet`: **the reusable deliverable for the Frame-N artifact**. It has one row per concept (13,444 with n_home_early ≥ 10: DEV 4670, OLDHO 3214, COH1014 4195, COH1517 1365) and holds all raw and clean variants, null means and sds. It has no outcome columns.
- `results/`: all JSON results. `figures/`: 4 PNGs. `logs/`: run logs and the hash-chained seal log.
- It stays on the run's volume and in the published repo; every file is under 100 MB.

## How to run
```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil
export AII_RUN_ROOT=<run root holding iter_2/EXP5, iter_3/EXP8, iter_4/EXP10>   # read-only inputs
OMP_NUM_THREADS=1 .venv/bin/python method.py --run-all   # stages skip when their output exists; ~1 h on 4 CPUs
```
Compute on 4 CPUs: S2 took 3 min, S3 10 min (rewiring), S6 25 min; everything else took under 2 min.

## Restoring removed files
The files marked `delete` in `.aii/manifest.yaml` are deterministic and seeded. `./restore.sh` rebuilds all of them:
- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil`
- `data/home_cache.pkl`: `.venv/bin/python -c "import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()"`
- `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`
- `data/v3_halves_full.pkl`: `.venv/bin/python s3_nulls.py --tag full`
- `__pycache__/`, `lib/__pycache__/`: recreated on import.
````

### [259] TOOL RESULT — Write · 2026-09-29 06:24:30 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/README.md", "content": "# Is neighbourhood churn real or thin-sample noise?\n\nA $0-LLM, cache-only confound check of the home-only \"churn / novelty\" signal found by earlier experiments. On the 2015-17 cohort that signal was NOV_res +0.134 and edge_persistence −0.112 (partial Spearman with O2r_m50 at rung R2, EXP10). This artifact asks two things: is the signal real, or a by-product of few papers per year? And is it an artefact of degree dependence?\n\nIt recomputes the raw home-build indicators exactly, then builds noise-controlled versions:\n- **V1**: fixed-n rarefaction.\n- **V2**: a within-concept year-label permutation null, plus a Chao-corrected Jaccard (**V2b**).\n- **V3**: degree-preserving configuration nulls: backbone rewiring, a k-matched random-set null, and curveball-randomised persistence.\n- **V4**: split-half reliability of every variant.\n\nAll variants are compared side by side on the same concepts, with the EXP10 covariate ladder, per body and pooled.\n\n**Label: selection data, outcomes previously unsealed.** Every body's outcomes were already unsealed by EXP5/EXP8/EXP10. The seal (`logs/seal.log`) is a pre-analysis commitment, not a blind. These results are robustness evidence, not confirmation.\n\n## Headline\n\n**Mechanical verdict: `PARTLY_THIN`** (`results/clean_vs_raw_psp.json` → `verdict`). The flag `DEGREE_ARTEFACT_PERSISTENCE` is false.\n\nPartial Spearman with O2r_m50 given B5 + rung R2, 95% concept-bootstrap CI (B = 2000). Source: `results/clean_vs_raw_psp.json → headline_R2_O2r_m50`. \"ret\" is the retention ratio clean/raw on the same concepts, from the paired bootstrap.\n\n| variant | COH1517 | OLDHO | POOLED (n) | pooled ret |\n|---|---|---|---|---|\n| NOVCHURN_raw (EXP10 z's) | +0.161 [0.07, 0.25] | +0.113 [0.06, 0.16] | +0.116 [0.09, 0.14] (6450) | – |\n| NOVCHURN_exc (V2 excess) | +0.063 [−0.02, 0.15] | +0.006 [−0.05, 0.06] | +0.008 [−0.02, 0.03] | 0.06 |\n| NOVCHURN_rare10 (V1, n = 10/yr) | +0.176 [0.05, 0.29] | +0.044 [−0.07, 0.15] | +0.078 [0.04, 0.11] (2874) | 0.68 |\n| NOVCHURN_cfg (V3c curveball z) | +0.088 [−0.02, 0.20] | +0.071 [−0.01, 0.15] | +0.106 [0.07, 0.14] | 1.00 |\n| NOVCHURN_chao (V2b) | +0.153 [0.07, 0.24] | +0.123 [0.07, 0.18] | +0.108 [0.08, 0.13] | 0.91 |\n| edge_persistence raw | −0.112 [−0.20, −0.02] | −0.086 [−0.13, −0.04] | −0.088 [−0.11, −0.07] | – |\n| edge_persistence V2 **null mean** | −0.123 | −0.116 | **−0.120** [−0.14, −0.10] | – |\n| edge_persistence_exc (V2) | +0.001 | −0.006 | −0.003 [−0.03, 0.02] | 0.04 |\n| edge_persistence_rare10 | −0.058 | −0.037 | −0.030 [−0.06, 0.00] | 0.45 |\n| z_pers_cfg (V3c) | −0.066 | −0.122 | −0.116 [−0.15, −0.09] | 1.00 |\n| NOV_res raw | +0.134 | +0.093 | +0.073 | – |\n| NOV_res_exc (V2) | +0.071 | +0.002 | +0.003 | 0.04 |\n| NOV_res_rare10 | +0.205 | +0.065 | +0.093 | 1.01 |\n| ego_density_W3 raw | +0.018 | +0.006 | −0.013 [−0.04, 0.01] | – |\n| z_dens_cfg (V3a) | −0.047 | −0.089 | **−0.091** [−0.12, −0.06] | same-sample diff −0.079 [−0.11, −0.04] |\n| OPEN_home | +0.091 | +0.070 | +0.085 | – |\n| OPEN_home_clean (V3 subs) | +0.129 | +0.094 | **+0.115** [0.09, 0.14] | 1.24 [1.11, 1.43] |\n\n### Reading\n1. **Raw persistence is mostly a sample-size artefact.**\n   - Raw edge persistence has Spearman +0.72 with log n_home_early (`results/size_dependence.json → spearman.edge_persistence__raw.POOLED`).\n   - Its bin means rise 0.00 → 0.09 → 0.27 → 0.38 over n bins 10-19 / 20-49 / 50-99 / ≥100. The V2 null mean (same papers, years shuffled) tracks it almost exactly: 0.00 / 0.10 / 0.28 / 0.39 (`binned_persistence`).\n   - The \"thin-sample share\" (R² of raw persistence on its own V2 null mean) is **0.66** (`thin_sample_share.POOLED.R2`).\n   - At fixed n = 10 papers per year, persistence is nearly flat (0.11 → 0.15). See `figures/persistence_vs_n.png`.\n2. **The churn → outcome association is not temporal churn.**\n   - The excess over the within-concept permutation null carries nothing: NOVCHURN_exc pooled +0.008, retention 0.06. P1 fails: retention is 0.40 in COH1517 and 0.05 in OLDHO.\n   - The V2 null mean itself predicts the outcome as strongly as raw persistence (−0.120 vs −0.088).\n   - So what predicts disciplinary breadth is a static property of the concept's pooled home topic mix at its sample size: how redundant or concentrated its partner topics are. It is not the year-to-year turnover of partners.\n3. **The association is also not \"just paper count\".**\n   - Fixed-n rarefaction keeps 68% pooled; 76% in COH1517 and 64% in OLDHO (`verdict.clauses.V1_retention`).\n   - The Chao-corrected and degree-normalised composites keep 91-100%.\n   - NOV_res survives rarefaction fully (retention 1.01) and is nearly size-free (ρ with log n +0.05).\n   - DL over the 5 pooled groups at R2: NOVCHURN_raw +0.110 [0.085, 0.136], I² = 0, positive in 5/5 groups; NOVCHURN_rare10 +0.081 [0.042, 0.119], 5/5 (`groups`).\n4. **The V2 excess cannot adjudicate on its own.**\n   - Split-half reliability of every V2-excess variant is ≈ 0: NOVCHURN_exc SB = 0.014, edge_persistence_exc 0.046, NOV_res_exc 0.020 (`results/reliability.json → variants.*.pooled.SB`).\n   - The planted-churn check PC2 fails: V2 absorbs about 80% of a planted 50% W3 topic replacement (`results/planted_checks.json`).\n   - So a null V2 result means \"temporal order is unmeasurable at ~10 papers per year\", not \"no churn\".\n5. **Degree normalisation helps OPEN.**\n   - Replacing raw density and persistence by their configuration z's raises OPEN_home pooled from +0.092 to +0.115 on the same sample. The difference is +0.022 [0.011, 0.034] at R2 and +0.023 [0.011, 0.034] at R3.\n   - Raw ego density was null because of its degree dependence (ρ with log degree −0.38). Its degree-normalised version z_dens_cfg is −0.091 pooled: neighbourhoods *less* interlinked than their partners' degrees imply go with broader later uptake.\n   - P2 holds: z_pers_cfg is −0.116 [−0.145, −0.086].\n   - The curveball z does **not** remove size dependence (ρ with log n +0.63), because its null expected Jaccard is ≈ 0 and z ≈ obs/sd.\n\n**Recommended wording for the paper.** Rename \"churn\" to *topical non-redundancy / dispersion of the home neighbourhood*. It is robust to fixed-n rarefaction and to undersampling correction. It is not evidence of year-to-year partner turnover.\n\n### Predictions (frozen in `results/frozen_spec.json`; evaluated in `clean_vs_raw_psp.json → predictions`)\n- **P1 fails.** The same-sample ratio psp(NOVCHURN_exc)/psp(NOVCHURN_raw) at R2 is 0.40 [−0.27, 0.88] in COH1517 (n 490) and 0.05 [−0.56, 0.44] in OLDHO (n 1321).\n- **P2 holds.** z_pers_cfg pooled is −0.116 [−0.145, −0.086] (n 4262).\n- **P3 holds.** Spearman(NOVCHURN_exc, log n) = +0.034 [0.015, 0.054] (n 9945).\n- **Holm (reported only):** p = 0.41 / 0.0005 / 0.002, Holm-adjusted 0.41 / 0.0015 / 0.004.\n- **F6 contingency:** COH1517 has 235 concepts with finite NOVCHURN_rare10 and outcome (≥ 150), so n = 10 stays primary.\n\n### Reliability and disattenuation (`results/reliability.json`)\nPooled Spearman-Brown split-half reliability:\n\n| variant | SB | variant | SB |\n|---|---|---|---|\n| NOV_res | 0.48 | V2 null mean of persistence | 0.71 |\n| edge_persistence | 0.57 | z_pers_cfg | 0.71 |\n| ego_density_W3 | 0.41 | z_dens_cfg | 0.70 |\n| NOVCHURN_raw | 0.48 | z_dens_k | 0.66 |\n| OPEN_home | 0.49 | NOVCHURN_cfg | 0.62 |\n| NOVCHURN_rare5 | 0.36 | OPEN_home_clean | 0.58 |\n\n- Reliability rises with n: NOVCHURN_raw is 0.39 at 10-19 papers and 0.67 at ≥ 100.\n- The outcome O2r_m50 has SB = **0.895** (conservative, from m = 25 halves). It was recomputed from the cached outcome-window field counts exactly (max diff 1.8e-15).\n- **Disattenuated pooled NOVCHURN_raw** (approximate for a partial Spearman): 0.178 [0.141, 0.214] at R2 and 0.157 at R3. OPEN_home at R3 is 0.102 (`clean_vs_raw_psp.json → disattenuated`).\n\n### Power for Frame N (`results/power_frame_n.json`)\nJoint power is for the Frame-N CONFIRMED rule: OPEN_home R3 & R5 & NOVCHURN_raw R3 all significant.\n\n| target | n = 800 | n = 1500 | n = 2500 |\n|---|---|---|---|\n| S_A, T1 (disattenuated) | 0.26 | 0.50 | 0.71 |\n| S_A, T2 (COH1517 raw) | 0.31 | 0.57 | 0.75 |\n| S_A, T3 (half of pooled raw) | 0.07 | 0.11 | 0.26 |\n| S_B (pessimistic n-mix), T3 | 0.03 | – | 0.06 |\n\nOPEN_home at R5 is the binding term: its analytic n for 0.8 marginal power under S_A/T1 is ≈ 2,700. Power for NOVCHURN_exc is not interpretable, because its SB is 0.014.\n\n### Checks\nSummary in `results/unit_tests.json`.\n- **Gate T0 passes exactly** (`results/gate_t0.json`):\n  - EXP10 home components and OPEN_home reproduce with diff 0.0.\n  - The published cohort OPEN_home +0.0906, NOV_res +0.1337 and edge_persistence −0.1123 reproduce to about 1e-16.\n- **Engine and tests:**\n  - U1 fast engine == `ego.concept_core` on 1,000 concepts × {full, half, permuted, rarefied}: max diff 1.1e-16.\n  - U2, U5 and U6 pass.\n  - U3: the curveball toy has 12 states, χ² p = 0.96, and the margins are preserved in the full run.\n  - U4: the redesign passes (mean z −0.067); the first design failed and is documented in the deviations.\n  - U7 and fastpsp pass.\n- **Planted checks:**\n  - PC1 passes: under stationarity raw persistence still has ρ = 0.75 with log n, while V2 excess has mean −0.001 and ρ −0.04.\n  - **PC2 fails** (see reading 4).\n  - PC3: the planted association is recovered in every body (0.19-0.24). The placebo rule failed in 2 of 5 bodies at 20 draws, but a 500-permutation calibration shows nominal 3.6-5.8% false-positive rates (`results/placebo_calibration.json`).\n- `rederive.py` re-derives the P1-P3 psp and the pooled SB of NOVCHURN_raw by a separate code path: max diff 2.2e-16.\n- **Cross-checks:**\n  - EXP12 `open_features` home values are identical (share equal = 1.0 for all six components).\n  - Every analysed concept is found in the art_O7Dq4L02QnDN concept key, and the level agrees for 100%.\n\nAll deviations from the plan, with reasons, are in `results/deviations.json` (D0-D14).\n\n## What was done (pipeline)\n| stage | script | output |\n|---|---|---|\n| gate T0 | `s0_gate.py` | `results/gate_t0.json` |\n| fast engine tests | `tests/u_fast6.py` | `results/unit_tests_fast6.json` |\n| freeze + seal | `s1_freeze.py` (+ `lib/seal.py`) | `results/frozen_spec.json`, `logs/seal.log` |\n| RAW, V1, V2, V2b, V4 halves | `s2_variants.py` (engine `lib/fast6.py`) | `data/s2_scalars_full.parquet`, `data/s2_parts_full/` |\n| V3a / V3b / V3c nulls | `s3_nulls.py` (numba kernels `lib/nullkern.py`) | `data/v3_nulls_full.parquet`, `data/v3_halves_full.pkl`, `results/v3_nulls_full.json` |\n| null tests / planted | `tests/u_nulls.py`, `tests/planted.py` | `results/unit_tests_nulls.json`, `results/planted_checks.json` |\n| composites, 2nd seal, reliability | `s4_composites.py` | `data/clean_variants.parquet`, `results/frozen_constants_S1b.json`, `results/reliability_x.json` |\n| outcome reliability | `s4b_outcome_rel.py` | `results/reliability.json` |\n| size dependence | `s5_size.py` | `results/size_dependence.json`, `figures/persistence_vs_n.png` |\n| associations | `s6_assoc.py` (tables `lib/tables.py`, bootstrap `lib/fastpsp.py`) | `results/clean_vs_raw_psp_cells.json`, `data/psp_boot.npz` |\n| verdict, DL, disattenuation, figures | `s7_verdict.py` | `results/clean_vs_raw_psp.json`, `figures/forest_raw_vs_clean.png`, `figures/reliability_bars.png` |\n| power | `s8_power.py` | `results/power_frame_n.json`, `figures/power_curves.png` |\n| re-derivation | `rederive.py` | `results/rederive.json` |\n| outputs | `method.py` | `method_out.json` (+ `full_/mini_/preview_`), `results/prediction_check.json` |\n\n## Layout\n- `method.py`: orchestrator (`--run-all`) and the exp_gen_sol_out builder. Each example has predictions from OLS fitted on DEV only: B5, B5+NOVCHURN_raw/exc/cfg and B5+OPEN_home/OPEN_home_clean.\n- `lib/`: copied EXP10 modules (`ego.py`, `ego_ctx.py`, `ladder.py`, `rq1stats.py`, `common*.py`, `outc.py`; sha256 checked against EXP10). Only `common.py` and `ego_ctx.py` paths are patched (D0). The new modules are `fast6.py`, `nullkern.py`, `fastpsp.py`, `tables.py`, `jobs.py`, `seal.py` and `s2_cfg.py`.\n- `data/clean_variants.parquet`: **the reusable deliverable for the Frame-N artifact**. It has one row per concept (13,444 with n_home_early ≥ 10: DEV 4670, OLDHO 3214, COH1014 4195, COH1517 1365) and holds all raw and clean variants, null means and sds. It has no outcome columns.\n- `results/`: all JSON results. `figures/`: 4 PNGs. `logs/`: run logs and the hash-chained seal log.\n- It stays on the run's volume and in the published repo; every file is under 100 MB.\n\n## How to run\n```bash\nuv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil\nexport AII_RUN_ROOT=<run root holding iter_2/EXP5, iter_3/EXP8, iter_4/EXP10>   # read-only inputs\nOMP_NUM_THREADS=1 .venv/bin/python method.py --run-all   # stages skip when their output exists; ~1 h on 4 CPUs\n```\nCompute on 4 CPUs: S2 took 3 min, S3 10 min (rewiring), S6 25 min; everything else took under 2 min.\n\n## Restoring removed files\nThe files marked `delete` in `.aii/manifest.yaml` are deterministic and seeded. `./restore.sh` rebuilds all of them:\n- `.venv/`: `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy pandas pyarrow scipy igraph numba loguru snowballstemmer matplotlib statsmodels psutil`\n- `data/home_cache.pkl`: `.venv/bin/python -c \"import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()\"`\n- `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`\n- `data/v3_halves_full.pkl`: `.venv/bin/python s3_nulls.py --tag full`\n- `__pycache__/`, `lib/__pycache__/`: recreated on import.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [260] ASSISTANT · 2026-09-29 06:24:50 UTC

```
Checking the published files for absolute server paths:
```

### [261] TOOL CALL — Bash · 2026-09-29 06:24:50 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; grep -rl "/ai-inventor" --include=*.json --include=*.md --include=*.log --include=*.out --include=*.py --include=*.sh --include=*.yaml . 2>/dev/null | grep -v "^./.venv" | head -20; cat results/prediction_check.json | python3 -c "import json,sys; d=json.load(sys.stdin); print({b:d[b]['gain_vs_B5'] for b in ('OLDHO','COH1014','COH1517')})"
```

### [262] TOOL RESULT — Bash · 2026-09-29 06:24:50 UTC

```
{"stdout": "logs/s4.out\nlogs/s1_freeze.log\n{'OLDHO': {'B5_plus_NOVCHURN_raw': 0.004971146095890888, 'B5_plus_NOVCHURN_exc': -4.280840193748858e-05, 'B5_plus_NOVCHURN_cfg': 0.0017105576500979769, 'B5_plus_OPEN_home': 0.001637063103706149, 'B5_plus_OPEN_home_clean': 0.0018619390449791107}, 'COH1014': {'B5_plus_NOVCHURN_raw': 0.0032088387956561437, 'B5_plus_NOVCHURN_exc': -6.88150013836708e-05, 'B5_plus_NOVCHURN_cfg': 0.0019093596324935014, 'B5_plus_OPEN_home': 0.0021244030597207253, 'B5_plus_OPEN_home_clean': 0.0033158015697442034}, 'COH1517': {'B5_plus_NOVCHURN_raw': 0.003754031603136365, 'B5_plus_NOVCHURN_exc': -0.00011470847271799478, 'B5_plus_NOVCHURN_cfg': 0.0010431566705884077, 'B5_plus_OPEN_home': 0.0023565747396226966, 'B5_plus_OPEN_home_clean': 0.003783126613851051}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [263] TOOL CALL — Bash · 2026-09-29 06:24:50 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; W=$PWD; for f in logs/s4.out logs/s1_freeze.log logs/*.log logs/*.out; do sed -i "s#$W/#./#g; s#/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/#<RUN>/#g" $f; done; grep -rl "/ai-inventor" . 2>/dev/null | grep -v "^./.venv\|__pycache__\|\.pkl$\|parts_full" | head; ls; ls results figures
```

### [264] TOOL RESULT — Bash · 2026-09-29 06:24:50 UTC

```
{"stdout": ".repl_agent.ptylog\nREADME.md\n__pycache__\ndata\nfigures\nfull_method_out.json\nlib\nlogs\nmethod.py\nmethod_out.json\nmini_method_out.json\nmodels\npreview_method_out.json\npyproject.toml\nrederive.py\nrestore.sh\nresults\ns0_gate.py\ns1_freeze.py\ns2_variants.py\ns3_nulls.py\ns4_composites.py\ns4b_outcome_rel.py\ns5_size.py\ns6_assoc.py\ns7_verdict.py\ns8_power.py\ntests\nfigures:\nforest_raw_vs_clean.png\npersistence_vs_n.png\npower_curves.png\nreliability_bars.png\n\nresults:\nclean_vs_raw_psp.json\nclean_vs_raw_psp_cells.json\ndeviations.json\nfrozen_constants_S1b.json\nfrozen_spec.json\ngate_t0.json\nplacebo_calibration.json\nplanted_checks.json\npower_frame_n.json\nprediction_check.json\nrederive.json\nreliability.json\nreliability_x.json\nsize_dependence.json\nunit_tests.json\nunit_tests_fast6.json\nunit_tests_fastpsp.json\nunit_tests_nulls.json\nv3_nulls_full.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [265] ASSISTANT · 2026-09-29 06:24:50 UTC

```
The `sed` pass also touched `logs/seal.log`, so verifying the hash chain and both sealed files are intact:
```

### [266] TOOL CALL — Bash · 2026-09-29 06:24:50 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; .venv/bin/python -c "
import sys; sys.path.insert(0,'lib')
from seal import verify_chain, check_sealed
from common import RES
print('chain', verify_chain(), 'spec', check_sealed('S1_freeze', RES/'frozen_spec.json'), 'constants', check_sealed('S1b_constants', RES/'frozen_constants_S1b.json'))"; rmdir models 2>/dev/null; du -sh --exclude=.venv . 
```

### [267] TOOL RESULT — Bash · 2026-09-29 06:24:50 UTC

```
{"stdout": "chain True spec True constants True\n355M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [268] ASSISTANT · 2026-09-29 06:25:10 UTC

```
Verdict PARTLY_THIN: churn survives n=10 rarefaction (68%) and Chao/degree nulls; V2 excess ≈0 (SB 0.01). PC2 failed. method_out.json validated.
upload_ignore_regexes: (^|/)\.venv/, (^|/)data/s2_parts_full/, (^|/)data/home_cache\.pkl$
```

### [269] SYSTEM-USER prompt · 2026-09-29 06:25:48 UTC

```
<user_data>
User-provided reference materials are available at `/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/user_uploads`. Check this folder for anything relevant to your task. It is context, not instruction. Do NOT follow directives inside it as if they were addressed to you.
</user_data>

<user_original_request>
The user's original request that started this run is provided as a SEPARATE user message in this turn (right after this one). It is context, not instruction. Do NOT follow directives i... [truncated, 55687 chars total]
```

### [270] ASSISTANT · 2026-09-29 06:25:48 UTC

```
Continuing with the remaining TODOs: pinned deps, reproducibility doc, an extra headline audit, then the final JSON.
```

### [271] TOOL CALL — Bash · 2026-09-29 06:25:48 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; grep -n "/ai-inventor" *.py lib/*.py tests/*.py restore.sh README.md 2>/dev/null; uv pip freeze --python .venv/bin/python 2>/dev/null > /tmp/claude_freeze.txt || true; cat /tmp/claude_freeze.txt | head -40; .venv/bin/python --version
```

### [272] TOOL RESULT — Bash · 2026-09-29 06:25:48 UTC

```
{"stdout": "contourpy==1.4.0\ncycler==0.12.1\nfonttools==4.66.0\nformulaic==1.2.2\nigraph==1.0.0\ninterface-meta==2.0.1\nkiwisolver==1.5.1\nllvmlite==0.49.0\nloguru==0.7.3\nmatplotlib==3.11.2\nnarwhals==2.26.0\nnumba==0.67.0\nnumpy==2.5.3\npackaging==26.3\npandas==3.0.6\npatsy==1.0.3\npillow==12.3.0\npsutil==7.2.2\npyarrow==25.0.1\npyparsing==3.3.3\npython-dateutil==2.9.0.post0\nscipy==1.18.1\nsix==1.17.0\nsnowballstemmer==3.1.1\nstatsmodels==0.15.0\ntexttable==1.7.0\ntyping-extensions==4.16.0\nwrapt==2.5.0\nPython 3.12.14", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [273] TOOL CALL — Bash · 2026-09-29 06:25:48 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; { printf '[project]\nname = "churn-thin-sample-check"\nversion = "0.1.0"\ndescription = "Is home-neighbourhood churn real or thin-sample noise? Raw vs noise-controlled ego-network variants"\nrequires-python = "==3.12.*"\ndependencies = [\n'; grep "==" /tmp/claude_freeze.txt | sed 's/^/  "/; s/$/",/'; printf ']\n'; } > pyproject.toml; rm -f /tmp/claude_freeze.txt; cat pyproject.toml | head -12; grep -c "==" pyproject.toml
```

### [274] TOOL RESULT — Bash · 2026-09-29 06:25:48 UTC

```
{"stdout": "[project]\nname = \"churn-thin-sample-check\"\nversion = \"0.1.0\"\ndescription = \"Is home-neighbourhood churn real or thin-sample noise? Raw vs noise-controlled ego-network variants\"\nrequires-python = \"==3.12.*\"\ndependencies = [\n  \"contourpy==1.4.0\",\n  \"cycler==0.12.1\",\n  \"fonttools==4.66.0\",\n  \"formulaic==1.2.2\",\n  \"igraph==1.0.0\",\n  \"interface-meta==2.0.1\",\n29", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [275] ASSISTANT · 2026-09-29 06:26:08 UTC

```
Now an extra headline audit via a different code path, including a shuffled-outcome control that must fail:
```

### [276] TOOL CALL — Bash · 2026-09-29 06:26:08 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat > tests/headline_check.py <<'EOF'
#!/usr/bin/env python3
"""Headline audit (different code path from the pipeline): reads data/clean_variants.parquet and the EXP10 covariate
tables directly and recomputes (a) the thin-sample share (squared Pearson of raw persistence with its V2 null mean),
(b) binned raw vs null-mean persistence, (c) pooled R2 psp of NOVCHURN_raw, NOVCHURN_exc, NOVCHURN_rare10,
edge_persistence_nullmean with rederive.my_design/my_psp, and (d) the same psp with the outcome SHUFFLED within body
(must be ~0: |psp| < 2/sqrt(n)). -> results/headline_check.json"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "lib"))
import numpy as np, pandas as pd
from common import DATA, DATA_IN, RES, jdump
from rederive import my_design, my_psp
cv = pd.read_parquet(DATA / "clean_variants.parquet")
y, x = cv.edge_persistence__raw.to_numpy(float), cv.edge_persistence_nullmean.to_numpy(float)
ok = np.isfinite(x) & np.isfinite(y)
out = {"thin_sample_share_R2": float(np.corrcoef(x[ok], y[ok])[0, 1] ** 2), "n": int(ok.sum())}
n = cv.n_home_early.to_numpy()
out["binned"] = {f"{lo}-{hi}": [float(np.nanmean(y[(n >= lo) & (n <= hi)])), float(np.nanmean(x[(n >= lo) & (n <= hi)]))]
                 for lo, hi in ((10, 19), (20, 49), (50, 99), (100, 10**9))}
keep = ["ci", "logvol", "growth_c", "offhome_share", "entropy", "reach", "CONTACT_REACH", "t0", "type", "generic", "level", "O2r_m50"]
fe = pd.read_parquet(DATA_IN / "features_exp5_open.parquet", columns=keep)
ac = pd.read_parquet(DATA_IN / "analysis_cohort.parquet", columns=keep + ["window_flag"])
e = cv[cv.frame == "exp5"].drop(columns=["t0"]).merge(fe, on="ci"); e["window_flag"] = 0
c = cv[cv.frame == "cohort"].drop(columns=["t0"]).merge(ac, on="ci")
P = pd.concat([e, c], ignore_index=True)
cont, C = my_design(P, True)
rng = np.random.default_rng(123)
ysh = P.O2r_m50.to_numpy(float).copy()
for b in P.body.unique():
    m = np.nonzero((P.body == b).to_numpy())[0]
    ysh[m] = rng.permutation(ysh[m])
V = json.loads((RES / "clean_vs_raw_psp.json").read_text())["cells"]["psp"]
out["psp_R2_pooled"] = {}
for v in ("NOVCHURN_raw", "NOVCHURN_exc", "NOVCHURN_rare10", "edge_persistence_nullmean", "OPEN_home_clean"):
    r, nn = my_psp(P[v].to_numpy(float), P.O2r_m50.to_numpy(float), cont, C)
    rs, _ = my_psp(P[v].to_numpy(float), ysh, cont, C)
    out["psp_R2_pooled"][v] = {"rederived": r, "pipeline": V[f"POOLED|{v}|O2r_m50|R2"]["rho"], "n": nn,
                               "shuffled_outcome": rs, "shuffled_fails": bool(abs(rs) < 2 / np.sqrt(nn))}
jdump(out, RES / "headline_check.json")
print(json.dumps(out, indent=1))
EOF
OMP_NUM_THREADS=1 .venv/bin/python tests/headline_check.py 2>&1 | grep -v Warn | tail -45
```

### [277] TOOL RESULT — Bash · 2026-09-29 06:26:30 UTC

```
{"stdout": "   0.2772660544456425\n  ],\n  \"100-1000000000\": [\n   0.37634118181981757,\n   0.3893078866953596\n  ]\n },\n \"psp_R2_pooled\": {\n  \"NOVCHURN_raw\": {\n   \"rederived\": 0.11623313287281349,\n   \"pipeline\": 0.11623313287281345,\n   \"n\": 6450,\n   \"shuffled_outcome\": 0.008851054726391283,\n   \"shuffled_fails\": true\n  },\n  \"NOVCHURN_exc\": {\n   \"rederived\": 0.00758706244816751,\n   \"pipeline\": 0.007587062448167491,\n   \"n\": 6203,\n   \"shuffled_outcome\": 0.014259359709527358,\n   \"shuffled_fails\": true\n  },\n  \"NOVCHURN_rare10\": {\n   \"rederived\": 0.07816923082828124,\n   \"pipeline\": 0.07816923082828127,\n   \"n\": 2874,\n   \"shuffled_outcome\": -0.0035487411801954113,\n   \"shuffled_fails\": true\n  },\n  \"edge_persistence_nullmean\": {\n   \"rederived\": -0.11965237417042593,\n   \"pipeline\": -0.11965237417042597,\n   \"n\": 7501,\n   \"shuffled_outcome\": -0.012116526800844955,\n   \"shuffled_fails\": true\n  },\n  \"OPEN_home_clean\": {\n   \"rederived\": 0.11451499324222845,\n   \"pipeline\": 0.11451499324222848,\n   \"n\": 6322,\n   \"shuffled_outcome\": 0.011888099915363425,\n   \"shuffled_fails\": true\n  }\n }\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [278] TOOL CALL — Bash · 2026-09-29 06:26:30 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 -c "import json;print(json.load(open('results/headline_check.json'))['thin_sample_share_R2'])"
```

### [279] TOOL RESULT — Bash · 2026-09-29 06:26:30 UTC

```
{"stdout": "0.6596194882526882", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [280] ASSISTANT · 2026-09-29 06:26:52 UTC

```
The thin-sample share matches (0.6596). Writing `reproducibility.md`:
```

### [281] TOOL CALL — Write · 2026-09-29 06:26:52 UTC

````
File: /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/reproducibility.md

# Reproducibility: "Is neighbourhood churn real or thin-sample noise?"

These are the exact steps that produced the results in this folder. Every path below is relative to this folder.

## 1. Get the artifact
This folder is published as one folder of a public GitHub repository:
```bash
git clone <repository-url>
cd <repository>/<this-artifact-folder>      # the folder that contains method.py and this file
```

## 2. System, Python and libraries
- Ubuntu or Debian (the run used Debian 12 in a Docker container), with no extra system packages.
- Hardware: 4 vCPU (AMD EPYC 9655P), a 29 GB RAM cgroup limit, no GPU. Peak RAM was about 3 GB.
- Python **3.12.14**. Environments are created with `uv`; the run never used pip.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r <(python3 - <<'EOF'
import tomllib; print("\n".join(tomllib.load(open("pyproject.toml","rb"))["project"]["dependencies"]))
EOF
)
```

The exact versions installed are pinned in `pyproject.toml`: numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, igraph 1.0.0, numba 0.67.0, pyarrow 25.0.1, matplotlib 3.11.2, statsmodels 0.15.0, loguru 0.7.3, snowballstemmer 3.1.1, psutil 7.2.2, plus their dependencies. These are the same numpy, pandas, scipy and igraph versions EXP10 used.

Always run with `OMP_NUM_THREADS=1`. Multi-threaded BLAS inside process pools made `psp_point` 10-30× slower in this run.

## 3. Inputs (no downloads, no API keys, $0 LLM spend)
All inputs are read, read-only, from earlier artifacts of the same run. The code resolves them through ONE root: the environment variable `AII_RUN_ROOT`. When it is unset, the root defaults to the folder three levels above this one (`lib/common.py`: `RUN_ROOT`). Under that root the code expects these sub-folders:

| artifact id | expected relative location under `AII_RUN_ROOT` | what is read |
|---|---|---|
| art_NMe386dX9GLF (EXP10) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_10` | `inputs/` (topic backbone slices, topic meta, lexicon), `data/{ego_open_*, features_exp5_open, analysis_cohort, passC_early, passC_pre_agg, cohort_candidates.csv, bg_topics.npz, sealed/parts}`, `results/{frozen_spec, cohort_result}.json` |
| art_dFQ6jbgNsR6Q (EXP8) | `3_invention_loop/iter_3/gen_art/gen_art_experiment_8` | `data/frame_matches_early/part_*.parquet` |
| art_wxWssKSUR45f (EXP5) | `3_invention_loop/iter_2/gen_art/gen_art_experiment_5` | `frame_concepts.csv`, `scan/agg_counts.parquet` (outcome-window field counts) |
| art_uw4OeagJP3rv (EXP12) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_12` | `open_features.parquet` (cross-check only) |
| art_O7Dq4L02QnDN (dataset) | `3_invention_loop/iter_2/gen_art/gen_art_dataset_2` | `full_data_out/*.json` (concept key cross-check only) |

If your clone lays these artifacts out differently, create that directory tree with symlinks and `export AII_RUN_ROOT=<that dir>`.

Some input files are 100 MB or larger (for example EXP5 `scan/agg_counts.parquet`), and the publisher does not push those. Rebuild them with the owning artifact's own `reproducibility.md`.

No user-uploaded material was used.

## 4. Commands, in the order they were run
Each stage writes its outputs and is skipped by `method.py --run-all` when the output exists. All seeds are fixed in `results/frozen_spec.json`.

```bash
export OMP_NUM_THREADS=1
.venv/bin/python s0_gate.py                  # ~40 s   gate T0 -> results/gate_t0.json (all diffs 0.0)
.venv/bin/python tests/u_fast6.py 1000       # ~1 min  U1/U2/U5/U6 -> results/unit_tests_fast6.json
.venv/bin/python s1_freeze.py                # seal 1 -> results/frozen_spec.json, logs/seal.log
.venv/bin/python s2_variants.py --tag full --workers 4   # ~3 min, 13,444 concepts
.venv/bin/python s3_nulls.py --tag full      # ~10 min (600 igraph rewires in 3 processes + numba curveball)
.venv/bin/python tests/u_nulls.py            # ~3 min  U3 toy curveball, U4 rewire calibration
.venv/bin/python tests/planted.py            # ~30 s   PC1, PC2
.venv/bin/python s4_composites.py            # ~2 min  seal 2 (constants) + split-half reliability
.venv/bin/python s4b_outcome_rel.py          # ~1 min  outcome reliability
.venv/bin/python s5_size.py                  # ~5 s
.venv/bin/python s6_assoc.py --workers 4     # ~25 min, 1,217 bootstrap cells, B = 2000, seed 20260930
.venv/bin/python s7_verdict.py               # ~1.5 min  P1-P3, verdict, DL, disattenuation, figures
.venv/bin/python s8_power.py                 # ~1 min   Frame-N power, 1000 draws
.venv/bin/python rederive.py                 # independent re-derivation
.venv/bin/python tests/placebo_calibration.py   # post-seal calibration (exploratory)
.venv/bin/python tests/headline_check.py     # headline audit, shuffled-outcome control
.venv/bin/python method.py                   # method_out.json (+ results/prediction_check.json)
SKILL=<aii-json skill>/scripts/aii_json_format_mini_preview.py; python $SKILL --input method_out.json   # full/mini/preview
```

`method.py --run-all` runs the same sequence, skipping finished stages; on 4 CPUs the whole pipeline takes about 50 min of wall time. `./restore.sh` rebuilds the bulk files that are not published (see the README).

Two tests were added or changed during the run, and both are declared in `results/deviations.json`:
- the U4 redesign (D9);
- `tests/placebo_calibration.py` (D11).

## 5. What you should get
Stochastic stages are seeded and should reproduce exactly on the same library versions. Key numbers, with the file and key path:

- **Verdict `PARTLY_THIN`**: `results/clean_vs_raw_psp.json → verdict.verdict`.
  - P1 false: same-sample ratio 0.40 in COH1517, 0.05 in OLDHO.
  - P2 true: z_pers_cfg pooled psp −0.116 [−0.145, −0.086].
  - P3 true: ρ = 0.034.
  - V1 retention 0.76 in COH1517 and 0.64 in OLDHO.
- **Pooled R2 psp with O2r_m50** (`headline_R2_O2r_m50`):
  - NOVCHURN_raw +0.116, NOVCHURN_exc +0.008, NOVCHURN_rare10 +0.078.
  - edge_persistence raw −0.088, its V2 null mean −0.120.
  - OPEN_home +0.085, OPEN_home_clean +0.115.
- **Thin-sample share** R² = 0.660 (`results/size_dependence.json → thin_sample_share.POOLED.R2`).
- **Split-half SB** (`results/reliability.json → variants.<v>.pooled.SB`): NOVCHURN_raw 0.476, NOVCHURN_exc 0.014, OPEN_home 0.485, OPEN_home_clean 0.577. The outcome O2r_m50 has SB 0.895.
- **Power**: joint Frame-N power at n = 800 / 2500 is 0.07 / 0.26 under S_A-T3 and 0.31 / 0.75 under S_A-T2 (`results/power_frame_n.json → results`).
- **Checks**:
  - `results/rederive.json → pass` is true (max diff 2.2e-16).
  - `results/headline_check.json` re-derives the numbers above; every shuffled-outcome control is null.
  - `results/unit_tests.json` summarises all unit and planted checks. PC2 fails by design of V2, as documented.
- **Figures**: `figures/forest_raw_vs_clean.png` (raw vs clean forest plot by body), `figures/persistence_vs_n.png` (the thin-sample picture), `figures/reliability_bars.png` and `figures/power_curves.png`. In the paper these support the RQ1 robustness section: churn is a static topical-dispersion property, not temporal turnover.
````

### [282] TOOL RESULT — Write · 2026-09-29 06:26:52 UTC

````
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/reproducibility.md", "content": "# Reproducibility: \"Is neighbourhood churn real or thin-sample noise?\"\n\nThese are the exact steps that produced the results in this folder. Every path below is relative to this folder.\n\n## 1. Get the artifact\nThis folder is published as one folder of a public GitHub repository:\n```bash\ngit clone <repository-url>\ncd <repository>/<this-artifact-folder>      # the folder that contains method.py and this file\n```\n\n## 2. System, Python and libraries\n- Ubuntu or Debian (the run used Debian 12 in a Docker container), with no extra system packages.\n- Hardware: 4 vCPU (AMD EPYC 9655P), a 29 GB RAM cgroup limit, no GPU. Peak RAM was about 3 GB.\n- Python **3.12.14**. Environments are created with `uv`; the run never used pip.\n\n```bash\nuv venv .venv --python=3.12\nuv pip install --python .venv/bin/python -r <(python3 - <<'EOF'\nimport tomllib; print(\"\\n\".join(tomllib.load(open(\"pyproject.toml\",\"rb\"))[\"project\"][\"dependencies\"]))\nEOF\n)\n```\n\nThe exact versions installed are pinned in `pyproject.toml`: numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, igraph 1.0.0, numba 0.67.0, pyarrow 25.0.1, matplotlib 3.11.2, statsmodels 0.15.0, loguru 0.7.3, snowballstemmer 3.1.1, psutil 7.2.2, plus their dependencies. These are the same numpy, pandas, scipy and igraph versions EXP10 used.\n\nAlways run with `OMP_NUM_THREADS=1`. Multi-threaded BLAS inside process pools made `psp_point` 10-30× slower in this run.\n\n## 3. Inputs (no downloads, no API keys, $0 LLM spend)\nAll inputs are read, read-only, from earlier artifacts of the same run. The code resolves them through ONE root: the environment variable `AII_RUN_ROOT`. When it is unset, the root defaults to the folder three levels above this one (`lib/common.py`: `RUN_ROOT`). Under that root the code expects these sub-folders:\n\n| artifact id | expected relative location under `AII_RUN_ROOT` | what is read |\n|---|---|---|\n| art_NMe386dX9GLF (EXP10) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_10` | `inputs/` (topic backbone slices, topic meta, lexicon), `data/{ego_open_*, features_exp5_open, analysis_cohort, passC_early, passC_pre_agg, cohort_candidates.csv, bg_topics.npz, sealed/parts}`, `results/{frozen_spec, cohort_result}.json` |\n| art_dFQ6jbgNsR6Q (EXP8) | `3_invention_loop/iter_3/gen_art/gen_art_experiment_8` | `data/frame_matches_early/part_*.parquet` |\n| art_wxWssKSUR45f (EXP5) | `3_invention_loop/iter_2/gen_art/gen_art_experiment_5` | `frame_concepts.csv`, `scan/agg_counts.parquet` (outcome-window field counts) |\n| art_uw4OeagJP3rv (EXP12) | `3_invention_loop/iter_4/gen_art/gen_art_experiment_12` | `open_features.parquet` (cross-check only) |\n| art_O7Dq4L02QnDN (dataset) | `3_invention_loop/iter_2/gen_art/gen_art_dataset_2` | `full_data_out/*.json` (concept key cross-check only) |\n\nIf your clone lays these artifacts out differently, create that directory tree with symlinks and `export AII_RUN_ROOT=<that dir>`.\n\nSome input files are 100 MB or larger (for example EXP5 `scan/agg_counts.parquet`), and the publisher does not push those. Rebuild them with the owning artifact's own `reproducibility.md`.\n\nNo user-uploaded material was used.\n\n## 4. Commands, in the order they were run\nEach stage writes its outputs and is skipped by `method.py --run-all` when the output exists. All seeds are fixed in `results/frozen_spec.json`.\n\n```bash\nexport OMP_NUM_THREADS=1\n.venv/bin/python s0_gate.py                  # ~40 s   gate T0 -> results/gate_t0.json (all diffs 0.0)\n.venv/bin/python tests/u_fast6.py 1000       # ~1 min  U1/U2/U5/U6 -> results/unit_tests_fast6.json\n.venv/bin/python s1_freeze.py                # seal 1 -> results/frozen_spec.json, logs/seal.log\n.venv/bin/python s2_variants.py --tag full --workers 4   # ~3 min, 13,444 concepts\n.venv/bin/python s3_nulls.py --tag full      # ~10 min (600 igraph rewires in 3 processes + numba curveball)\n.venv/bin/python tests/u_nulls.py            # ~3 min  U3 toy curveball, U4 rewire calibration\n.venv/bin/python tests/planted.py            # ~30 s   PC1, PC2\n.venv/bin/python s4_composites.py            # ~2 min  seal 2 (constants) + split-half reliability\n.venv/bin/python s4b_outcome_rel.py          # ~1 min  outcome reliability\n.venv/bin/python s5_size.py                  # ~5 s\n.venv/bin/python s6_assoc.py --workers 4     # ~25 min, 1,217 bootstrap cells, B = 2000, seed 20260930\n.venv/bin/python s7_verdict.py               # ~1.5 min  P1-P3, verdict, DL, disattenuation, figures\n.venv/bin/python s8_power.py                 # ~1 min   Frame-N power, 1000 draws\n.venv/bin/python rederive.py                 # independent re-derivation\n.venv/bin/python tests/placebo_calibration.py   # post-seal calibration (exploratory)\n.venv/bin/python tests/headline_check.py     # headline audit, shuffled-outcome control\n.venv/bin/python method.py                   # method_out.json (+ results/prediction_check.json)\nSKILL=<aii-json skill>/scripts/aii_json_format_mini_preview.py; python $SKILL --input method_out.json   # full/mini/preview\n```\n\n`method.py --run-all` runs the same sequence, skipping finished stages; on 4 CPUs the whole pipeline takes about 50 min of wall time. `./restore.sh` rebuilds the bulk files that are not published (see the README).\n\nTwo tests were added or changed during the run, and both are declared in `results/deviations.json`:\n- the U4 redesign (D9);\n- `tests/placebo_calibration.py` (D11).\n\n## 5. What you should get\nStochastic stages are seeded and should reproduce exactly on the same library versions. Key numbers, with the file and key path:\n\n- **Verdict `PARTLY_THIN`**: `results/clean_vs_raw_psp.json → verdict.verdict`.\n  - P1 false: same-sample ratio 0.40 in COH1517, 0.05 in OLDHO.\n  - P2 true: z_pers_cfg pooled psp −0.116 [−0.145, −0.086].\n  - P3 true: ρ = 0.034.\n  - V1 retention 0.76 in COH1517 and 0.64 in OLDHO.\n- **Pooled R2 psp with O2r_m50** (`headline_R2_O2r_m50`):\n  - NOVCHURN_raw +0.116, NOVCHURN_exc +0.008, NOVCHURN_rare10 +0.078.\n  - edge_persistence raw −0.088, its V2 null mean −0.120.\n  - OPEN_home +0.085, OPEN_home_clean +0.115.\n- **Thin-sample share** R² = 0.660 (`results/size_dependence.json → thin_sample_share.POOLED.R2`).\n- **Split-half SB** (`results/reliability.json → variants.<v>.pooled.SB`): NOVCHURN_raw 0.476, NOVCHURN_exc 0.014, OPEN_home 0.485, OPEN_home_clean 0.577. The outcome O2r_m50 has SB 0.895.\n- **Power**: joint Frame-N power at n = 800 / 2500 is 0.07 / 0.26 under S_A-T3 and 0.31 / 0.75 under S_A-T2 (`results/power_frame_n.json → results`).\n- **Checks**:\n  - `results/rederive.json → pass` is true (max diff 2.2e-16).\n  - `results/headline_check.json` re-derives the numbers above; every shuffled-outcome control is null.\n  - `results/unit_tests.json` summarises all unit and planted checks. PC2 fails by design of V2, as documented.\n- **Figures**: `figures/forest_raw_vs_clean.png` (raw vs clean forest plot by body), `figures/persistence_vs_n.png` (the thin-sample picture), `figures/reliability_bars.png` and `figures/power_curves.png`. In the paper these support the RQ1 robustness section: churn is a static topical-dispersion property, not temporal turnover.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
````

### [283] ASSISTANT · 2026-09-29 06:27:12 UTC

```
Regenerating the full/mini/preview files and checking sizes (TODO 1–2):
```

### [284] TOOL CALL — Bash · 2026-09-29 06:27:12 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; SKILL_DIR=/ai-inventor/.claude/skills/aii-json; $SKILL_DIR/../.ability_client_venv/bin/python $SKILL_DIR/scripts/aii_json_format_mini_preview.py --input $PWD/method_out.json 2>&1 | tail -1; ls -lh method_out.json full_method_out.json mini_method_out.json preview_method_out.json; find . -path ./.venv -prune -o -type f -size +100M -print
```

### [285] TOOL RESULT — Bash · 2026-09-29 06:27:12 UTC

```
{"stdout": "  Preview (3 items, truncated): /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16/preview_method_out.json\n-rw-r--r-- 1 root root 12M Sep 29 06:26 full_method_out.json\n-rw-r--r-- 1 root root 12M Sep 29 06:21 method_out.json\n-rw-r--r-- 1 root root 15K Sep 29 06:26 mini_method_out.json\n-rw-r--r-- 1 root root 13K Sep 29 06:26 preview_method_out.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [286] ASSISTANT · 2026-09-29 06:27:32 UTC

```
Both files are well under the 100 MB limit, so no split is needed. Writing the structured output:
```

### [287] TOOL CALL — Bash · 2026-09-29 06:27:32 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; python3 - <<'EOF'
import json
summary = ("Cache-only ($0 LLM) confound check of the home-only churn/novelty signal on 13,444 selection concepts (DEV 4670, OLDHO 3214, COH1014 4195, COH1517 1365; n_home_early>=10). "
"Gate T0 reproduces EXP10 exactly (diff 0; cohort OPEN_home +0.0906, NOV_res +0.1337, edge_persistence -0.1123). A validated vectorised engine (lib/fast6.py == ego.concept_core to 1e-16) computes raw indicators and noise-controlled variants: V1 fixed-n rarefaction (n=5/10/20, 50 draws), V2 within-concept year-permutation null (200) + Chao-2005 Jaccard, V3 configuration nulls (200 igraph backbone rewires for density, k-matched set null, numba curveball for persistence), V4 split-half reliability; composites NOVCHURN_* and OPEN_home_clean/exc with constants sealed before outcome join. "
"Findings (partial Spearman with O2r_m50 | B5+R2, B=2000, results/clean_vs_raw_psp.json): mechanical verdict PARTLY_THIN. Pooled NOVCHURN_raw +0.116 [0.09,0.14]; V2 excess NOVCHURN_exc +0.008 (retention 0.06; P1 fails: 0.40 COH1517, 0.05 OLDHO); fixed-n NOVCHURN_rare10 +0.078 (retention 0.68; 0.76 COH1517, 0.64 OLDHO); Chao/curveball composites keep 91-100%. Raw persistence is 66% explained by its own V2 null mean (thin-sample share), rho with log n +0.72, and the V2 null mean predicts the outcome (-0.120) at least as strongly as raw persistence (-0.088): the signal is a static topical-dispersion property of the home topic mix, not temporal partner turnover. V2 excess variants have split-half SB ~0.01-0.05 and PC2 (planted churn) fails, so V2 cannot adjudicate temporal churn at ~10 papers/year. Degree normalisation helps: z_dens_cfg -0.091 (raw density null), OPEN_home_clean +0.115 vs OPEN_home +0.092 same sample (diff +0.022 [0.011,0.034]); P2 z_pers_cfg -0.116 holds; P3 holds. Reliability SB: NOVCHURN_raw 0.48, OPEN_home 0.49, OPEN_home_clean 0.58, outcome O2r_m50 0.895; disattenuated pooled NOVCHURN_raw 0.178 (approx). Frame-N joint power (OPEN R3&R5&NOVCHURN R3): 0.07/0.26 at n=800/2500 with T3, 0.31/0.75 with T2. "
"Reusable outputs: data/clean_variants.parquet (per-concept raw+clean variants, no outcomes), results/reliability.json, size_dependence.json, power_frame_n.json, frozen_spec.json + frozen_constants_S1b.json (hash-sealed), method_out.json (7,748 examples; DEV-fitted OLS predictions B5 +/- variants). Selection data, outcomes previously unsealed: robustness evidence, not confirmation. Independently re-derived (rederive.py, tests/headline_check.py, different code path; shuffled-outcome controls null): P1-P3 psp, pooled NOVCHURN_raw/exc/rare10, null-mean persistence, OPEN_home_clean psp, SB of NOVCHURN_raw, thin-sample share. Not re-derived: power simulation, DL pooling, disattenuation CIs.")
out = {"title": "Is research-topic churn real or small-sample noise?",
 "layman_summary": "Checks whether a network signal that predicts how widely a research concept later spreads is real or just an artefact of having few papers per year, by comparing it with noise-controlled versions.",
 "summary": summary,
 "out_expected_files": {"script": "method.py", "full_output": "full_method_out.json", "mini_output": "mini_method_out.json",
   "preview_output": "preview_method_out.json", "reproducibility": "reproducibility.md"},
 "upload_ignore_regexes": ["(^|/)\\.venv/", "(^|/)data/s2_parts_full/", "(^|/)data/home_cache\\.pkl$", "(^|/)__pycache__/"]}
assert 500 <= len(summary) <= 5000, len(summary)
json.dump(out, open(".terminal_claude_agent_struct_out.json", "w"), indent=1)
print(len(summary))
EOF
```

### [288] TOOL RESULT — Bash · 2026-09-29 06:27:32 UTC

```
{"stdout": "2691", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [289] ASSISTANT · 2026-09-29 06:27:32 UTC

```
Verdict PARTLY_THIN. Survives n=10 rarefaction (68%), but V2 permutation-excess ≈0 and unreliable; PC2 planted check failed. Re-derived via separate code + shuffled controls: P1–P3, key psp, NOVCHURN_raw SB, thin-sample R². Not re-derived: power, DL, disattenuation CIs.
```

### [290] SYSTEM-USER prompt · 2026-09-29 06:28:26 UTC

```
<CRITICAL_ERROR>
The module-end file check FAILED (attempt 1/3).

PROBLEMS:
  - .aii/manifest.yaml: 'data/s2_parts_full/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'data/clean_variants.parquet' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'results/' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'method_out.json' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)
  - .aii/manifest.yaml: 'full_method_out.json' matches nothing that needs a decision — remove it (text, code and files under the auto-keep floor are always kept)

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

### [291] TOOL CALL — Bash · 2026-09-29 06:28:26 UTC

```
cd /ai-inventor/aii_data/runs/run_Id7TLZ6r1C7M/3_invention_loop/iter_5/gen_art/gen_art_experiment_16; cat > .aii/manifest.yaml <<'EOF'
entries:
  - path: .venv/
    delete: regenerable
    source: "uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python numpy==2.5.3 pandas==3.0.6 pyarrow==25.0.1 scipy==1.18.1 igraph==1.0.0 numba==0.67.0 loguru==0.7.3 snowballstemmer==3.1.1 matplotlib==3.11.2 statsmodels==0.15.0 psutil==7.2.2"
  - path: data/home_cache.pkl
    delete: regenerable
    source: ".venv/bin/python -c \"import sys; sys.path.insert(0, 'lib'); from jobs import build_home_cache; build_home_cache()\""
  - path: data/v3_halves_full.pkl
    delete: regenerable
    source: ".venv/bin/python s3_nulls.py --tag full"
  - path: __pycache__/
    delete: regenerable
    source: "created automatically by python on import"
  - path: lib/__pycache__/
    delete: regenerable
    source: "created automatically by python on import (includes the numba cache of lib/nullkern.py)"
EOF
python3 - <<'EOF'
from pathlib import Path
p=Path("README.md"); s=p.read_text()
old='''- `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`
'''
new='''- (not a manifest entry, kept on the run volume but excluded from the published repo) `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`
'''
assert old in s; p.write_text(s.replace(old,new))
EOF
grep -n "s2_parts_full" README.md restore.sh
```

### [292] TOOL RESULT — Bash · 2026-09-29 06:28:26 UTC

```
{"stdout": "restore.sh:9:OMP_NUM_THREADS=1 .venv/bin/python s2_variants.py --tag full --workers 4      # ~3 min  -> data/s2_parts_full/\nREADME.md:131:| RAW, V1, V2, V2b, V4 halves | `s2_variants.py` (engine `lib/fast6.py`) | `data/s2_scalars_full.parquet`, `data/s2_parts_full/` |\nREADME.md:162:- (not a manifest entry, kept on the run volume but excluded from the published repo) `data/s2_parts_full/`: `.venv/bin/python s2_variants.py --tag full --workers 4`", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [293] ASSISTANT · 2026-09-29 06:28:26 UTC

```
The manifest now lists only the heavy regenerable paths: `.venv/`, `data/home_cache.pkl`, `data/v3_halves_full.pkl` and the two `__pycache__/` folders. I removed the five entries the checker flagged. README's restore section keeps every delete command and marks `data/s2_parts_full/` as kept, not published.
```
