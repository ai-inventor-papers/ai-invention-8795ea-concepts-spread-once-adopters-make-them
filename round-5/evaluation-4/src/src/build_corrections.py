#!/usr/bin/env python3
"""Items 1-4 and 6-11: insert-ready correction blocks (corrections_iter5/NN_*.md), each number read from a named file
through the Ledger (results/claims_ledger_v4.csv). Also writes results/apply_plan_iter5.json: for every block, the
target heading / action that apply_corrections.py executes on the report copy, and results/derived.json (values this
artifact computes, e.g. counts, which the ledger then keys).

Nothing outside this workspace is written. Usage: python src/build_corrections.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import numpy as np
import pandas as pd
from loguru import logger

from ledger import Ledger
from paths import (COR, DS2, E8, E10, E11, E12, EVAL3, EXP7, LOGS, REPORT4, REPORT5, RES, RUN, L as LOOP, jdump, rel)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "build_corrections.log", rotation="30 MB", level="DEBUG")

L = Ledger()
APPLY: list[dict] = []
DERIVED: dict = {}
DER = RES / "derived.json"
NOT_FOUND_NOTES: list[str] = []

A_E10, A_E11, A_E12, A_E8, A_E7, A_EVAL3 = ("art_NMe386dX9GLF", "gen_art_experiment_11", "art_uw4OeagJP3rv",
                                            "art_dFQ6jbgNsR6Q", "art_22ppE1snfHKj", "art_oKOd21ZMnu9S")
TAG = "[Correction, iteration 5, from {}]"

CR = E10 / "results/cohort_result.json"
CREP = E10 / "results/cohort_report.json"
SEL = E10 / "results/exp5_selection_result.json"
FS10 = E10 / "results/frozen_spec.json"
LMC = E10 / "results/learned_models_cohort.json"
CP = E12 / "results/case_pairs.json"
PR = E12 / "results/preregistration_R2.json"
DD, DH = E12 / "results/decomposition_dev.json", E12 / "results/decomposition_heldout.json"
SQD, SQH = E12 / "results/sequence_light_dev.json", E12 / "results/sequence_light_heldout.json"
TD, TH = E12 / "results/trajectories_dev.json", E12 / "results/trajectories_heldout.json"
ATL = E12 / "ai_atlas/atlas.json"
FE = E11 / "results/fe_results.json"
HUR = E8 / "results/heldout_unit_results.csv"
HS8 = E8 / "results/heldout_summary.json"
S2H = EXP7 / "results/step2_heldout.json"
S2D = EXP7 / "results/step2_dev.json"
HET, SPC = EVAL3 / "results/heterogeneity.json", EVAL3 / "results/spec_curve.json"
DRCA = EVAL3 / "results/drca_persist_comparison.json"
SYN = RES / "evidence_synthesis.json"


def begin(fname: str, section: str) -> None:
    L.target_file, L.section = fname, section


def apply(fname, block_id, target, action, text, new_heading=None, note=""):
    APPLY.append({"source_file": fname, "block_id": block_id, "target": target, "action": action, "text": text,
                  "new_heading": new_heading, "note": note})


def flush() -> None:
    DER.write_text(json.dumps(DERIVED, indent=1, default=str))
    L._cache.pop(DER, None)


def derive(key: str, value) -> str:
    DERIVED[key] = value
    flush()
    return key


def jl(p: Path):
    return json.loads(Path(p).read_text())


def f3(x):  # ledger helper: signed 3 dp
    return x


# ============================================================================ item 1: 26.4 rebuilt + atlas
def item1() -> str:
    fn = "01_case_studies_26_4.md"
    begin(fn, "26.4")
    cp = jl(CP)
    pairs = cp["pairs"]
    rows = []
    for i, p in enumerate(pairs):
        k = f"pairs[{i}]"
        cells = [p["pair"], p["rgroup"], p["high"], p["low"]]
        for v in ("OPEN_all", "OPEN_home", "logvol", "O2r_resid", "rho"):
            cells.append(f"{L.num(CP, f'{k}.{v}[0]', '{:+.3f}')} / {L.num(CP, f'{k}.{v}[1]', '{:+.3f}')}")
        for v in ("Bn", "E2"):
            cells.append(f"{L.num(CP, f'{k}.{v}[0]', '{:.0f}')} / {L.num(CP, f'{k}.{v}[1]', '{:.0f}')}")
        cells += ["yes" if p["high_open_higher_O2r_resid"] else "no", "yes" if p["open_home_order_disagrees"] else "no"]
        rows.append("| " + " | ".join(cells) + " |")
    n_pairs = len(pairs)
    k_resid = sum(bool(p["high_open_higher_O2r_resid"]) for p in pairs)
    k_bn = sum(p["Bn"][0] > p["Bn"][1] for p in pairs)
    k_dis = sum(bool(p["open_home_order_disagrees"]) for p in pairs)
    derive("item1.n_pairs", n_pairs)
    derive("item1.k_high_open_all_higher_O2r_resid", k_resid)
    derive("item1.k_high_open_all_larger_Bn", k_bn)
    derive("item1.k_open_home_order_disagrees", k_dis)
    flush()
    s_n = L.num(DER, "['item1.n_pairs']", "{:.0f}")
    s_k = L.num(DER, "['item1.k_high_open_all_higher_O2r_resid']", "{:.0f}")
    s_b = L.num(DER, "['item1.k_high_open_all_larger_Bn']", "{:.0f}")
    s_d = L.num(DER, "['item1.k_open_home_order_disagrees']", "{:.0f}")
    t = TAG.format(A_E12)
    block = (
        f"### 26.4 Case studies ({s_n} matched pairs)\n\n"
        f"{t} The previous 26.4 table contained 5 rows that no artifact produced, and a sentence on GPU computing and "
        f"deep learning that is not in the pair set. Both are deleted. [Correction, iteration 4/5] The table below is "
        f"read row by row from `case_pairs.json -> pairs`.\n\n"
        "Pairs were selected on OPEN_all (top vs bottom quintile within reporting group), matched on logvol, growth and "
        "onset within group; the outcome was not used in selection (`case_pairs.json -> rule.outcome_use`: "
        f"\"{cp['rule']['outcome_use']}\"). **Illustration, not inference.**\n\n"
        "| pair | group | high-OPEN_all concept | low-OPEN_all concept | OPEN_all (high / low) | OPEN_home | logvol | "
        "O2r_resid | rho (retention) | Bn | E2 | high has higher O2r_resid | OPEN_home order disagrees |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n"
        f"The high-OPEN_all member is broader (higher O2r_resid) in {s_k}/{s_n} pairs and has more retained off-home "
        f"fields (Bn) in {s_b}/{s_n}. In {s_d}/{s_n} pairs the OPEN_home ordering disagrees with the OPEN_all "
        "ordering, so these pairs illustrate the all-papers build, which Section 25.4 shows is mechanically coupled to "
        "spread.\n\nSource: `3_invention_loop/iter_4/gen_art/gen_art_experiment_12/results/case_pairs.json` -> "
        "`pairs[i].{OPEN_all,OPEN_home,logvol,O2r_resid,rho,Bn,E2}`; counts in `results/derived.json`.\n")
    apply(fn, "26.4_rebuilt", r"^### 26\.4 ", "replace-section", block)
    # ---- atlas
    begin(fn, "26.5")
    at = jl(ATL)
    cols = ["name", "type", "t0", "ai_share", "early_volume", "growth_c", "O1b", "O3", "O2r_resid", "OPEN_all",
            "OPEN_home"]
    fmts = {"t0": "{:.0f}", "ai_share": "{:.3f}", "early_volume": "{:.0f}", "growth_c": "{:+.3f}", "O1b": "{:.0f}",
            "O3": "{:.0f}", "O2r_resid": "{:+.3f}", "OPEN_all": "{:+.3f}", "OPEN_home": "{:+.3f}"}
    arows = []
    for i, c in enumerate(at["concepts"]):
        cells = []
        for col in cols:
            if col in ("name", "type"):
                cells.append(str(c.get(col)))
            elif c.get(col) is None or (isinstance(c.get(col), float) and not np.isfinite(c.get(col))):
                cells.append("NA")
            else:
                cells.append(L.num(ATL, f"concepts[{i}].{col}", fmts[col]))
        arows.append("| " + " | ".join(cells) + " |")
    derive("item1.n_atlas_rows", len(at["concepts"]))
    flush()
    s_na = L.num(DER, "['item1.n_atlas_rows']", "{:.0f}")
    ablock = (
        f"### 26.5 Exploratory AI atlas: retrospective, outcome-selected ({s_na} concepts)\n\n"
        f"{TAG.format(A_E12)} This is the exploratory stage the request asks for (Artificial Intelligence first). It "
        f"is labelled by its own file as \"{at['label']}\". Concepts were chosen per trajectory type AFTER outcomes were "
        "known, so the table describes; it does not test.\n\n"
        "| " + " | ".join(cols) + " |\n|" + "---|" * len(cols) + "\n" + "\n".join(arows) + "\n\n"
        "Measures that looked meaningful across types (`atlas.json -> looked_meaningful`): "
        + ", ".join(f"`{m}`" for m in at["looked_meaningful"]) + ". Data limit: " + at["data_limit"] + ".\n\n"
        "Source: `3_invention_loop/iter_4/gen_art/gen_art_experiment_12/ai_atlas/atlas.json` -> `concepts[i]` (the "
        "37-concept list; `ai_atlas/table.csv` is the per-measure median table by type, not the concept list).\n")
    apply(fn, "26.5_atlas", r"^### 26\.4 ", "insert-new-section-after", ablock)
    return f"# 01 Section 26.4 rebuilt from case_pairs.json, plus the AI atlas\n\n{block}\n{ablock}"


# ============================================================================ item 2: Exp11 section 25a + counts
def artifact_counts() -> dict:
    rows = []
    for d in sorted(LOOP.glob("iter_[1-4]/gen_art/gen_art_*")):
        w = d / ".aii_worker_result.json"
        status, why = "failed/incomplete", "no .aii_worker_result.json"
        if w.exists():
            r = json.loads(w.read_text()).get("result") or {}
            if r.get("failed"):
                status, why = "failed/incomplete", f"result.failed = true ({str(r.get('error_message'))[:60]})"
            elif r.get("structured_output") or (d / ".terminal_claude_agent_struct_out.json").exists():
                status, why = "completed", "structured output present"
            else:
                status, why = "failed/incomplete", "no structured output"
        rows.append({"dir": str(d.relative_to(LOOP)), "status": status, "evidence": why})
    n = len(rows)
    nc = sum(r["status"] == "completed" for r in rows)
    return {"rows": rows, "commissioned": n, "completed": nc, "failed": n - nc,
            "failed_dirs": [r["dir"] for r in rows if r["status"] != "completed"]}


def item2() -> str:
    fn = "02_exp11_25a.md"
    begin(fn, "25a")
    t = TAG.format(A_E11)
    prereg = E11 / "prereg.md"
    verb = L.carry(prereg, "lines:24-32")
    fe = jl(FE)

    def row(label, key, extra_i2=False):
        node = Ledger.json_get(fe["DEV"], key)
        b = L.num(FE, f"DEV.{key}.b", "{:+.4f}")
        ci = L.ci(FE, f"DEV.{key}.ci", "{:+.4f}")
        p = L.num(FE, f"DEV.{key}.p", "{:.3f}")
        n = L.num(FE, f"DEV.{key}.n", "{:,.0f}") if "n" in node else "NA"
        nc = L.num(FE, f"DEV.{key}.n_concepts", "{:,.0f}") if "n_concepts" in node else "NA"
        i2 = L.num(FE, f"DEV.{key}.I2", "{:.2f}") if "I2" in node else "-"
        return f"| {label} | {b} | {ci} | {p} | {n} | {nc} | {i2} |"

    rows = [row("H-M1 density (PPML)", "H_M1_density"), row("H-M2 OPEN_home (PPML)", "H_M2_open"),
            row("joint: density", "joint.density"), row("joint: OPEN_home", "joint.OPEN_home"),
            row("LPM density", "lpm_density"), row("LPM OPEN_home", "lpm_open")]
    for g in fe["DEV"]["by_group"]:
        for v in ("density", "OPEN_home"):
            rows.append(row(f"group {g}: {v}", f"by_group.{g}.{v}"))
    rows += [row("DL over DEV groups: density", "DL_density"), row("DL over DEV groups: OPEN_home", "DL_OPEN_home")]
    hm3 = (f"H-M3 point estimates: std beta_fwd {L.num(FE, 'DEV.H_M3_point.std_fwd', '{:+.4f}')}, std beta_rev "
           f"{L.num(FE, 'DEV.H_M3_point.std_rev', '{:+.4f}')}, difference {L.num(FE, 'DEV.H_M3_point.diff', '{:+.4f}')} "
           f"(bootstrap CI {L.ci(FE, 'DEV.bootstrap.diff.ci', '{:+.4f}')}).")
    nrows = L.num(FE, "DEV.n_rows", "{:,.0f}")
    ncon = L.num(FE, "DEV.n_concepts", "{:,.0f}")
    # what ran: from logs
    fe_log = (E11 / "logs/analysis_fe.log").read_text().strip().splitlines()
    es_out = (E11 / "logs/event_study.out").read_text()
    es_log_size = (E11 / "logs/event_study.log").stat().st_size
    part_log = (E11 / "logs/partners.log").read_text().strip().splitlines()
    dev = jl(E11 / "results/deviations.json")
    cnt = artifact_counts()
    jdump(RES / "artifact_counts.json", cnt)
    begin(fn, "24")
    s_c = L.num(RES / "artifact_counts.json", "commissioned", "{:.0f}")
    s_ok = L.num(RES / "artifact_counts.json", "completed", "{:.0f}")
    s_f = L.num(RES / "artifact_counts.json", "failed", "{:.0f}")
    cnt_tab = "| artifact directory | status | evidence |\n|---|---|---|\n" + "\n".join(
        f"| `{r['dir']}` | {r['status']} | `{r['evidence']}` |" for r in cnt["rows"])
    begin(fn, "25a")
    block = (
        "## 25a. Experiment 11 (incomplete): does within-concept closure precede an entry slowdown? "
        f"[ARTIFACT:gen_art_experiment_11]\n\n{t} This experiment was commissioned in iteration 4 and was missing from "
        "the report. Plan title: *Within-concept closure, OPEN and the next field entry (FE Poisson / event study)*.\n\n"
        "Pre-registered predictions and verdict rules, verbatim (`prereg.md`, lines 24-32):\n\n"
        + "\n".join("> " + x for x in verb.splitlines()) + "\n\n"
        f"**DEV results** (concept-year panel, {nrows} rows, {ncon} concepts; concept-clustered CIs):\n\n"
        "| model / term | b | 95% CI | p | n rows | n concepts (clustered) | I2 |\n|---|---|---|---|---|---|---|\n"
        + "\n".join(rows) + f"\n\n{hm3}\n\n"
        "**Verdict: NOT SUPPORTED.** The rule is 'NOT SUPPORTED = both H-M1 and H-M2 CIs include 0 on DEV', and both "
        "do (table rows 1-2).\n\n"
        "**What was not run.** Read from the logs, not from the plan:\n"
        f"- `logs/analysis_fe.log` last line: `{fe_log[-1][:160]}`. Only the DEV body was estimated; OLD_HELDOUT and "
        "COHORT body models (H-M5) have no results in `fe_results.json` (only their `sample_counts`).\n"
        f"- H-M4 (Sun-Abraham event study): `logs/event_study.log` is empty ({es_log_size} bytes) and "
        "`logs/event_study.out` ends in an OpenBLAS `pthread_create failed` error followed by `KeyboardInterrupt` "
        "during `import scipy`. No event-study estimate exists.\n"
        f"- H-S1 and H-P1: `logs/partners.log` last line: `{part_log[-1][:120]}`; partner indicators were built, but no "
        "H-S1/H-P1 test output was written. (H-S1's question is answered descriptively by Exp12's sequence analysis, "
        "Section 26.3.)\n"
        f"- `deviations.json` records `placebo_ii_not_run`: \"{dev.get('placebo_ii_not_run', 'NOT_FOUND')}\"\n"
        "- No partial outputs from `event_study.out` or `partners.out` are reported as results.\n\n"
        "Source: `3_invention_loop/iter_4/gen_art/gen_art_experiment_11/results/fe_results.json` -> `DEV.*`; "
        "`prereg.md` lines 24-32; `logs/*.log|out`; `results/deviations.json`.\n")
    apply(fn, "25a_exp11", r"^### 25\.7 ", "insert-new-section-after", block,
          note="new ## 25a placed after 25.7 (before Section 26)")
    begin(fn, "29")
    de = (f"\n10. **Within-concept closure does not precede an entry slowdown (Experiment 11, DEV only).** {t} H-M1 "
          f"density b = {L.num(FE, 'DEV.H_M1_density.b', '{:+.4f}')} {L.ci(FE, 'DEV.H_M1_density.ci', '{:+.4f}')}; "
          f"H-M2 OPEN_home b = {L.num(FE, 'DEV.H_M2_open.b', '{:+.4f}')} {L.ci(FE, 'DEV.H_M2_open.ci', '{:+.4f}')}. "
          "NOT SUPPORTED. The event study, the held-out bodies and H-S1/H-P1 did not run (Section 25a).\n")
    apply(fn, "29_deadend_exp11", r"^## 29\. ", "append-to-section", de)
    begin(fn, "28.1")
    c4 = (f"\n{t} C4 (within-concept closure -> entry slowdown) was tested: DEV null (H-M1 CI "
          f"{L.ci(FE, 'DEV.H_M1_density.ci', '{:+.4f}')}), [ARTIFACT:gen_art_experiment_11]. The 'NEW as lead-lag "
          "test' verdict therefore describes a test that was run and failed on DEV, not an open result.\n")
    apply(fn, "28.1_c4", r"^### 28\.1 ", "append-to-section", c4)
    begin(fn, "24")
    cb = (f"\n{t} Artifact counts derived from disk (`results/artifact_counts.json`), iterations 1-4: {s_c} "
          f"commissioned, {s_ok} completed, {s_f} failed or incomplete.\n\n{cnt_tab}\n")
    apply(fn, "24_counts", r"^## 24\. ", "append-to-section", cb)
    begin(fn, "31")
    old31 = ("Four iterations and sixteen artifacts (fifteen commissioned, twelve completed; three failed: "
             "gen_art_dataset_1, gen_art_experiment_2, gen_art_experiment_9)")
    s_c = L.num(RES / "artifact_counts.json", "commissioned", "{:.0f}")
    s_ok = L.num(RES / "artifact_counts.json", "completed", "{:.0f}")
    s_f = L.num(RES / "artifact_counts.json", "failed", "{:.0f}")
    new31 = (f"Four iterations and {s_c} commissioned artifacts ({s_ok} completed; {s_f} failed or incomplete: "
             + ", ".join(Path(d).name for d in cnt["failed_dirs"]) + f") {TAG.format('run records')}")
    apply(fn, "31_counts", old31, "text-replace", new31)
    return (f"# 02 Section 25a: Experiment 11 (incomplete), dead end, C4 note and artifact counts\n\n{block}\n"
            f"## Dead end for Section 29\n{de}\n## Note for Section 28.1\n{c4}\n## Counts for Sections 24 and 31\n{cb}\n"
            f"Section 31 opening sentence becomes: {new31}\n")


# ============================================================================ item 3: Exp10 rewrite
def lad(build, y, r, src=CR, grp="primary"):
    k = f"{grp}.['{build}|{y}|{r}']"
    return f"{L.num(src, k + '.rho')} {L.ci(src, k + '.ci')}"


def item3() -> str:
    fn = "03_exp10_rewrite.md"
    t = TAG.format(A_E10)
    begin(fn, "25.1")
    nb = {y: L.num(CR, f"n_by_t0.['{y}']", "{:,.0f}") for y in ("2015", "2016", "2017")}
    ncoh = L.num(CR, "n_cohort", "{:,.0f}")
    nav = L.num(CR, "outcome_availability.O2r_m50", "{:,.0f}")
    b251 = (
        "### 25.1 Design\n\n"
        f"{t} The OPEN index is the mean of six signed z-scored ego-network components from the early window (t0 to "
        "t0+2): new_edge_rate (+), n_comm_W3 (+), participation (+), NOV_res (+), ego_density_W3 (−), "
        f"edge_persistence (−), with winsor bounds and z constants frozen on the {L.num(SEL, 'n_exp5', '{:,.0f}')} EXP5 "
        "concepts. Three builds: "
        "OPEN_home (home-field papers only), OPEN_all (all papers; **mechanically coupled** to spread, because its "
        "off-home papers are part of what later counts as breadth) and OPEN_sizematch (a size-matched subsample of all "
        f"papers). The confirmatory cohort has onsets in **2015-2017**: {nb['2015']} (2015), {nb['2016']} (2016) and "
        f"{nb['2017']} (2017, the declared power extension), {ncoh} concepts in total, of which {nav} have a defined "
        "O2r_m50. None of them was used in any earlier screen.\n\n"
        f"Pre-seal power for OPEN_home at R2 was {L.num(FS10, 'power.with_2017.power_ci_gt0', '{:.2f}')} (true effect "
        f"= half the EXP5 estimate), and the minimum detectable effect (2.8 SE) was "
        f"{L.num(FS10, "power.with_2017.['MDE_2.8SE_analytic']", '{:.3f}')}.\n\n"
        "Source: `iter_4/gen_art/gen_art_experiment_10/results/cohort_result.json` -> `n_by_t0`, `n_cohort`, "
        "`outcome_availability`; `results/frozen_spec.json` -> `power.with_2017`.\n")
    apply(fn, "25.1", r"^### 25\.1 ", "replace-section", b251)
    begin(fn, "25.2")
    rows = []
    for b in ("OPEN_home", "OPEN_all", "OPEN_sizematch"):
        for y in ("O2r_m50", "O2r_resid"):
            n = L.num(CR, f"primary.['{b}|{y}|R2'].n", "{:.0f}")
            rows.append(f"| {b} | {y} | " + " | ".join(lad(b, y, r) for r in ("R0", "R1", "R2", "R3", "R4", "R5"))
                        + f" | {n} |")
    dl = f"{L.num(CR, 'groups.OPEN_home|O2r_m50|R2.DL.b')} {L.ci(CR, 'groups.OPEN_home|O2r_m50|R2.DL.ci')}"
    b252 = (
        "### 25.2 Control ladder\n\n"
        f"{t} Partial Spearman (psp) of each build with rarefied breadth (O2r_m50) and residualised breadth "
        f"(O2r_resid), concept bootstrap B = {L.num(CR, 'B', '{:,.0f}')}. R0 = B5 + onset year; R1 = + CONTACT_REACH; "
        "R2 = + concept type, "
        "generic flag and legacy level; R3 = + footprint; R4 = + label and home-paper coverage; R5 = + home-group FE.\n\n"
        "| build | outcome | R0 | R1 | R2 | R3 | R4 | R5 | n |\n|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(rows) + "\n\n"
        f"OPEN_home at R2 (the registered primary) is {lad('OPEN_home', 'O2r_m50', 'R2')}, Holm p = "
        f"{L.num(CR, 'holm.OPEN_home|O2r_m50.p_holm', '{:.3f}')}. **Its R4 and R5 intervals include 0**, and so does "
        f"its DerSimonian-Laird pool over groups at R2, {dl} (Section 25.3). OPEN_all and OPEN_sizematch stay above "
        "0 on every rung, but OPEN_all is mechanically coupled (Section 25.4).\n\n"
        "Source: `cohort_result.json` -> `primary['<build>|<outcome>|R0..R5'].{rho,ci,n}`, "
        "`groups['OPEN_home|O2r_m50|R2'].DL`, `holm`.\n")
    apply(fn, "25.2", r"^### 25\.2 ", "replace-section", b252)
    begin(fn, "25.4")
    b254 = (
        "### 25.4 Mechanical coupling: ALL minus HOME\n\n"
        f"{t} OPEN_all is **mechanically coupled** to the outcome: its ego network includes the off-home papers that "
        "later make up breadth. The paired concept-bootstrap differences at R3 are: ALL − HOME "
        f"{L.num(CR, 'contrasts.all_minus_home|R3.diff')} {L.ci(CR, 'contrasts.all_minus_home|R3.ci')} "
        f"(n = {L.num(CR, 'contrasts.all_minus_home|R3.n', '{:.0f}')}); SIZEMATCH − HOME "
        f"{L.num(CR, 'contrasts.sizematch_minus_home|R3.diff')} {L.ci(CR, 'contrasts.sizematch_minus_home|R3.ci')} "
        f"(n = {L.num(CR, 'contrasts.sizematch_minus_home|R3.n', '{:.0f}')}). The first says the all-papers build "
        "carries more signal than the home build; the second (CI includes 0) says a size-matched all-papers build does "
        "not beat the home build by a detectable margin. The home-only signal is carried by NOV_res "
        f"{lad('NOV_res__home', 'O2r_m50', 'R2', grp='components')} and low edge persistence "
        f"{lad('edge_persistence__home', 'O2r_m50', 'R2', grp='components')} (Section 25.8).\n\n"
        "Source: `cohort_result.json` -> `contrasts`, `components`.\n")
    apply(fn, "25.4", r"^### 25\.4 ", "replace-section", b254)
    begin(fn, "25.7")
    fp = "secondary.frozen_prediction_O2r_m50"
    b257 = (
        "### 25.7 Verdict\n\n"
        f"{t} The pre-registered verdict rule returns **{jl(CR)['verdict']['verdict']}** (all five clauses pass, "
        "`cohort_result.json -> verdict`). Read with its limits, the evidence is weaker than that word:\n"
        f"- OPEN_home is {lad('OPEN_home', 'O2r_m50', 'R2')} at R2 but its R4 "
        f"{lad('OPEN_home', 'O2r_m50', 'R4')} and R5 {lad('OPEN_home', 'O2r_m50', 'R5')} intervals include 0, as does "
        f"the group-level DL pool {L.num(CR, 'groups.OPEN_home|O2r_m50|R2.DL.b')} "
        f"{L.ci(CR, 'groups.OPEN_home|O2r_m50|R2.DL.ci')}.\n"
        f"- **No forecasting gain**: the frozen B5 model gives Spearman {L.num(CR, fp + '.spearman_B5')} and B5 + "
        f"OPEN_home {L.num(CR, fp + '.spearman_B5_plus_OPEN_home')}, a difference of {L.num(CR, fp + '.diff')} "
        f"{L.ci(CR, fp + '.diff_ci')} (n = {L.num(CR, fp + '.n', '{:.0f}')}).\n"
        f"- The planted control (true psp 0.10) was **not recovered** by the pipeline draw: "
        f"{L.num(CR, "placebos.['planted_0.10'].rho")} {L.ci(CR, "placebos.['planted_0.10'].ci")}; the independent audit draw "
        f"gave {L.num(CREP, 'audits.post_unseal_audit.A5_planted.estimate')} "
        f"{L.ci(CREP, 'audits.post_unseal_audit.A5_planted.ci')}. With power "
        f"{L.num(FS10, 'power.with_2017.power_ci_gt0', '{:.2f}')} and MDE "
        f"{L.num(FS10, "power.with_2017.['MDE_2.8SE_analytic']", '{:.3f}')}, a single cohort of this size cannot confirm "
        "or refute an effect near 0.09 reliably.\n"
        "- OPEN_all and OPEN_sizematch are larger but are labelled **mechanically coupled** / partly coupled "
        "(Section 25.4). Evaluation 3's specification curve (Section 27.2) used the all-papers build and is relabelled "
        "**exploratory, all-papers build**.\n\n"
        "**Reading:** a small home-only partial association, positive on the confirmatory cohort at the registered "
        "rung, fragile under coverage and group controls, and with no out-of-sample forecasting gain.\n\n"
        "Source: `cohort_result.json` -> `verdict`, `primary`, `groups`, `secondary.frozen_prediction_O2r_m50`, "
        "`placebos`; `cohort_report.json` -> `audits.post_unseal_audit.A5_planted`; `frozen_spec.json` -> `power`.\n")
    apply(fn, "25.7", r"^### 25\.7 ", "replace-section", b257)
    # ---- 25.8 components / within type / sensitivities / placebos
    begin(fn, "25.8")
    comp = []
    for k in ("new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"):
        comp.append(f"| {k} | {lad(f'{k}__home', 'O2r_m50', 'R2', grp='components')} | "
                    f"{lad(f'{k}__home', 'O2r_m50', 'R2', SEL, 'components')} | "
                    f"{lad(f'{k}__all', 'O2r_m50', 'R2', grp='components')} | "
                    f"{lad(f'{k}__all', 'O2r_m50', 'R2', SEL, 'components')} |")
    wt = []
    for b in ("OPEN_home", "OPEN_all", "OPEN_sizematch"):
        cells = []
        for ty in ("method", "object", "property", "topic"):
            k = f"within_type.['{b}|{ty}|R3']"
            cells.append(f"{L.num(CR, k + '.rho')} {L.ci(CR, k + '.ci')} n={L.num(CR, k + '.n', '{:.0f}')}")
        wt.append(f"| {b} | " + " | ".join(cells) + " |")
    sens = []
    for k, v in jl(CR)["sensitivity"].items():
        if isinstance(v, dict) and "rho" in v:
            kk = f"sensitivity.['{k}']"
            sens.append(f"| {k} | {L.num(CR, kk + '.rho')} {L.ci(CR, kk + '.ci')} | {L.num(CR, kk + '.n', '{:.0f}')} |")
    pl = "placebos.within_group_permutation"
    b258 = (
        "### 25.8 Components, within type, sensitivities and placebos (cohort)\n\n"
        f"{t} Re-keyed to `cohort_result.json` (cohort) and `exp5_selection_result.json` (EXP5 selection data), "
        "replacing the copies in the Exp10 README.\n\n"
        "| component (sign) | HOME cohort | HOME EXP5 | ALL cohort | ALL EXP5 |\n|---|---|---|---|---|\n"
        + "\n".join(comp) + "\n\nWithin concept type (R3 without type dummies):\n\n"
        "| build | method | object | property | topic |\n|---|---|---|---|---|\n" + "\n".join(wt) + "\n\n"
        "Declared sensitivities (R2):\n\n| analysis | estimate [95% CI] | n |\n|---|---|---|\n" + "\n".join(sens)
        + "\n\n"
        f"Placebos: within-group outcome permutations ({L.num(CR, pl + '.n_perm', '{:.0f}')} draws): 95th percentile "
        f"of |psp| = {L.num(CR, pl + '.q95_abs')}, against the observed {L.num(CR, pl + '.observed_R2')}. Planted "
        f"psp = 0.10: {L.num(CR, "placebos.['planted_0.10'].rho")} {L.ci(CR, "placebos.['planted_0.10'].ci")}, not "
        f"recovered; independent audit draw {L.num(CREP, 'audits.post_unseal_audit.A5_planted.estimate')}, "
        "recovered.\n\nSource: `cohort_result.json` -> `components`, `within_type`, `sensitivity`, `placebos`; "
        "`exp5_selection_result.json` -> `components`.\n")
    apply(fn, "25.8", r"^### 25\.7 ", "insert-new-section-after", b258)
    # ---- 31.1
    begin(fn, "31")
    old = "1. **Early cooccurrence openness (OPEN) predicts later cross field breadth on a confirmatory cohort.**"
    new31 = (
        f"1. **A small home-only openness association on a confirmatory cohort (fragile).** {t} On 2015-2017 onset "
        f"concepts never screened before, OPEN_home has psp {lad('OPEN_home', 'O2r_m50', 'R2')} at R2 "
        f"(Holm p = {L.num(CR, 'holm.OPEN_home|O2r_m50.p_holm', '{:.3f}')}), but R4, R5 and the group DL pool "
        f"{L.num(CR, 'groups.OPEN_home|O2r_m50|R2.DL.b')} {L.ci(CR, 'groups.OPEN_home|O2r_m50|R2.DL.ci')} include 0, "
        f"and adding it to B5 changes forecast Spearman by {L.num(CR, fp + '.diff')} {L.ci(CR, fp + '.diff_ci')}. "
        "OPEN_all is larger but mechanically coupled to the outcome. The previous wording of this finding follows, "
        "superseded: ")
    apply(fn, "31.1", old, "text-prefix", new31)
    return (f"# 03 Experiment 10 rewrite (25.1, 25.2, 25.4, 25.7, new 25.8, 31.1)\n\n{b251}\n{b252}\n{b254}\n{b257}\n"
            f"{b258}\n## 31.1 prefix\n\n{new31}\n")


# ============================================================================ item 4: Exp12 rewrite
def item4() -> str:
    fn = "04_exp12_rewrite.md"
    t = TAG.format(A_E12)
    begin(fn, "26.1")
    pr = jl(PR)
    dd, dh = jl(DD), jl(DH)
    vd = {"PR1": dd["verdicts"]["PR1"], "PR1b": dd["verdicts"]["PR1b"], "PR2": dd["verdicts"]["PR2"]}
    prl = []
    for k in ("PR1", "PR1b", "PR2", "PR3"):
        txt = L.carry(PR, k)
        prl.append(f"> **{k}** {txt}")
    dec = []
    for bl, src, base in (("DEV", DD, "variants"), ("held-out (4 groups pooled)", DH, "pooled_heldout4.variants"),
                          ("2010-14 cohort (pooled)", DH, "pooled_cohort.variants")):
        cells = []
        for v in ("i_pooled", "ii_vol_PRIMARY", "iii_vol_med_adjusted", "iv_vol_noMed_PR1"):
            k = f"{base}.{v}"
            cells.append(f"{L.num(src, k + '.point.diff_explore_ret')} {L.ci(src, k + '.ci.diff_explore_ret')} "
                         f"(n={L.num(src, k + '.n', '{:,.0f}')})")
        dec.append(f"| {bl} | " + " | ".join(cells) + " |")
    dlh = "DL_heldout_groups.diff_explore_ret"
    verd = []
    for bl, src, base in (("DEV", DD, "verdicts"), ("held-out", DH, "pooled_heldout4.verdicts"),
                          ("2010-14 cohort", DH, "pooled_cohort.verdicts")):
        v = Ledger.json_get(jl(src), base)
        verd.append(
            f"| {bl} | {v['PR1']['verdict']}: {L.num(src, base + '.PR1.s_explore_minus_s_ret')} "
            f"{L.ci(src, base + '.PR1.ci')} | {v['PR1b']['verdict']}: {L.num(src, base + '.PR1b.s_contact_minus_s_ret')} "
            f"{L.ci(src, base + '.PR1b.ci')} | {v['PR2']['verdict']}: diff {L.num(src, base + '.PR2.diff')} "
            f"{L.ci(src, base + '.PR2.diff_ci')}; psp {L.num(src, base + '.PR2.psp')} {L.ci(src, base + '.PR2.psp_ci')} "
            f"| D_rho {L.num(src, base + '.PR3_descriptive.D_rho')} {L.ci(src, base + '.PR3_descriptive.ci')} |")
    caveat = "Bn and O2r share papers; the decomposition is an identity, not a causal split."
    b261 = (
        "### 26.1 Log-additive breadth decomposition\n\n"
        f"{t} Rarefied breadth is decomposed as log Bn = log E2 (early contact) + log M (frontier advance) + log ρ "
        "(retention); shares of the top-vs-bottom O2r_resid tercile gap. **" + caveat + "**\n\n"
        "Pre-registered predictions, verbatim (`preregistration_R2.json`):\n\n" + "\n".join(prl) + "\n\n"
        "s_explore − s_ret by variant and body [95% concept-bootstrap CI] (PR1 is variant iv; the primary display "
        "variant is ii):\n\n"
        "| body | i pooled | ii volume-stratified (primary) | iii volume + Medicine adjusted | iv volume-stratified, "
        "no Medicine (PR1) |\n|---|---|---|---|---|\n" + "\n".join(dec) + "\n\n"
        f"DerSimonian-Laird over the held-out groups ({', '.join(dh['DL_heldout_groups']['diff_explore_ret']['units'])}"
        f", variant iv): {L.num(DH, dlh + '.b')} {L.ci(DH, dlh + '.ci')}, I2 = {L.num(DH, dlh + '.I2', '{:.2f}')}.\n\n"
        "Verdicts per clause (the rule: SUPPORTED / NOT SUPPORTED / REVERSED by CI side, per body):\n\n"
        "| body | PR1 (s_explore − s_ret, variant iv) | PR1b (s_contact − s_ret) | PR2 (bottom − top retention "
        "ratio; psp given B5) | PR3 (descriptive) |\n|---|---|---|---|---|\n" + "\n".join(verd) + "\n\n"
        "PR2 is REVERSED on its first clause wherever the difference is negative: localised concepts do **not** keep "
        "more early; the psp clause replicates EXP8 on the same frame and is not new evidence.\n\n"
        "Source: `iter_4/gen_art/gen_art_experiment_12/results/decomposition_dev.json`, `decomposition_heldout.json` "
        "-> `variants.*`, `verdicts.*`, `DL_heldout_groups`; `preregistration_R2.json`.\n")
    apply(fn, "26.1", r"^### 26\.1 ", "replace-section", b261)
    begin(fn, "31")
    apply(fn, "31.3_caveat", "3. **Breadth is driven by exploration, not retention.**", "text-prefix",
          f"3. {t} **Caveat: {caveat}** ")
    # ---- 26.3 sequence
    begin(fn, "26.3")
    sq = []
    for bl, src, key in (("DEV", SQD, "DEV"), ("held-out", SQH, "HELDOUT"), ("2010-14 cohort", SQH, "COHORT")):
        v = jl(src)[key]
        sq.append(f"| {bl} | {L.num(src, key + '.order.n', '{:,.0f}')} | {L.num(src, key + '.order.A_lt_T', '{:.3f}')} | "
                  f"{L.num(src, key + '.mechanical_lag_null.null_A_lt_T', '{:.3f}')} | "
                  f"{L.num(src, key + '.mechanical_lag_null.excess_A_lt_T', '{:+.3f}')} "
                  f"{L.ci(src, key + '.mechanical_lag_null.excess_ci')} | "
                  f"{L.num(src, key + '.cloglog_hazard.HR', '{:.2f}')} {L.ci(src, key + '.cloglog_hazard.HR_ci', '{:.2f}')} | "
                  f"{v['verdict']} |")
    b263 = (
        "### 26.3 Sequence: home prominence first, or born at the intersection?\n\n"
        f"{t} A = first age with home-field prominence ≥ half its 0-8 maximum; T = first cross-field take-off age. "
        "The share of concepts with A < T is compared with a mechanical-lag null (1,000 within-concept permutations "
        "of the prominence series). The hazard ratio compares take-off of intersection-born concepts with single-home "
        "concepts (cloglog, controlling log volume).\n\n"
        "| body | n | share A < T | null share | excess [95% CI] | intersection-born take-off HR [95% CI] | "
        "verdict |\n|---|---|---|---|---|---|---|\n" + "\n".join(sq) + "\n\n"
        "The excess over the mechanical lag is at most a few percentage points and changes sign between bodies "
        "(HOME-FIRST only on the held-out groups). Intersection-born concepts take off **later**, not earlier "
        "(HR < 1 in every body). There is no general home-first sequence and no intersection route.\n\n"
        "Source: `sequence_light_dev.json`, `sequence_light_heldout.json` -> `<body>.order`, "
        "`mechanical_lag_null`, `cloglog_hazard`, `verdict`.\n")
    apply(fn, "26.3", r"^### 26\.3 ", "replace-section", b263)
    # ---- OPEN on PC axes
    begin(fn, "26.2")
    pc = []
    for bn, bk in (("OPEN_all", "all"), ("OPEN_home", "home"), ("OPEN_sizematch", "size")):
        pc.append(
            f"| {bn} | {L.num(TD, f'open_on_axis.pooled.PC1.{bk}.partial_given_B5_labelcov.rho')} "
            f"{L.ci(TD, f'open_on_axis.pooled.PC1.{bk}.partial_given_B5_labelcov.ci')} | "
            f"{L.num(TD, f'open_on_axis.pooled.PC2.{bk}.partial_given_B5_labelcov.rho')} "
            f"{L.ci(TD, f'open_on_axis.pooled.PC2.{bk}.partial_given_B5_labelcov.ci')} | "
            f"{L.num(TH, f'DL_heldout_groups_PC1.{bk}.partial_given_B5_labelcov.b')} "
            f"{L.ci(TH, f'DL_heldout_groups_PC1.{bk}.partial_given_B5_labelcov.ci')} | "
            f"{L.num(TH, f'open_on_axis_cohort_PC1.{bk}.partial_given_B5_labelcov.rho')} "
            f"{L.ci(TH, f'open_on_axis_cohort_PC1.{bk}.partial_given_B5_labelcov.ci')} |")
    b262 = (
        f"\n{t} Where OPEN sits in the trajectory space (partial Spearman given B5 and label coverage):\n\n"
        "| build | DEV PC1 | DEV PC2 | held-out DL PC1 | 2010-14 cohort PC1 |\n|---|---|---|---|---|\n"
        + "\n".join(pc) + "\n\n"
        f"The typology is a continuum (DTW-HMM ARI {L.num(TD, 'hmm.ari_dtw_hmm', '{:.3f}')}); OPEN loads on the "
        "breadth axis (PC1) and weakly negatively on PC2 (retention-heavy profiles) for the all-papers build.\n\n"
        "Source: `trajectories_dev.json` -> `open_on_axis.pooled`, `hmm.ari_dtw_hmm`; `trajectories_heldout.json` -> "
        "`DL_heldout_groups_PC1`, `open_on_axis_cohort_PC1`. (`open_diagnostics.json` holds build correlations and "
        "coverage, not the PC table.)\n")
    apply(fn, "26.2_pc", r"^### 26\.2 ", "append-to-section", b262)
    return f"# 04 Experiment 12 rewrite (26.1, 26.2 addition, 26.3, 31.3 caveat)\n\n{b261}\n{b263}\n## Addition to 26.2\n{b262}"


# ============================================================================ item 6: section 23 restore
def item6() -> str:
    fn = "06_section23_restore.md"
    begin(fn, "23")
    lines = REPORT4.read_text().splitlines()
    i = next(k for k, s in enumerate(lines) if s.startswith("## 23. What we have learned so far"))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("## References"))
    while j > i and not lines[j - 1].strip():
        j -= 1
    src_slice = "\n".join(lines[i:j])
    DERIVED["item6.slice_lines_1based"] = [i + 1, j]
    flush()
    L.carry(REPORT4, f"lines:{i + 1}-{j}")
    restored = src_slice.replace("## 23. What we have learned so far",
                                 "## 23. What we have learned so far (end of iteration 3)", 1)
    t7, t12, t3 = TAG.format(A_E7), TAG.format(A_E12), TAG.format(A_EVAL3)
    notes = (
        "\n\n**Corrections to the restored Section 23 (iteration 5):**\n\n"
        f"- {t7} The dose response is **not monotone** on held-out data: betas by persistence age 2 / 3 / ≥4 are "
        f"{L.num(S2H, 'pooled4.specificity.c_dose.betas_by_age.2', '{:.2f}')} / "
        f"{L.num(S2H, 'pooled4.specificity.c_dose.betas_by_age.3', '{:.2f}')} / "
        f"{L.num(S2H, "pooled4.specificity.c_dose.betas_by_age['4+']", '{:.2f}')}.\n"
        f"- {t12} The trajectory typology is a **continuum**, not two classes: DTW-HMM ARI "
        f"{L.num(TD, 'hmm.ari_dtw_hmm', '{:.3f}')}.\n"
        f"- {t3} The volume-matched contrast (retained vs entered-not-retained fields) is null on DEV too: "
        f"{L.num(S2D, 'battery.specificity.b_volume_matched.contrast_R_minus_N.est')} "
        f"{L.ci(S2D, 'battery.specificity.b_volume_matched.contrast_R_minus_N.ci')}.\n")
    block = (f"{restored}\n\n{TAG.format('iter_4 report')} Section 23 was a stub in the iteration-5 report. The text "
             f"above is restored byte-for-byte from `iter_4/gen_strat/current_report.md` lines {i + 1}-{j} (heading "
             f"suffix '(end of iteration 3)' added).{notes}")
    apply(fn, "23_restore", r"^## 23\. ", "replace-section", block)
    begin(fn, "16")
    tag16 = (f" {t12} Superseded: at higher resolution the typology is a continuum (DTW-HMM ARI "
             f"{L.num(TD, 'hmm.ari_dtw_hmm', '{:.3f}')}; Section 26.2).")
    apply(fn, "16.2_tag", "2. **Two stable trajectory classes", "text-append-line", tag16)
    (RES / "section23_source_slice.txt").write_text(src_slice)
    return (f"# 06 Section 23 restored verbatim from the iteration-4 report\n\n{block}\n\n## Tag under 16.2\n\n{tag16}\n")


# ============================================================================ item 7: section 28 evidence
def item7() -> str:
    fn = "07_section28_evidence.md"
    begin(fn, "28.1")
    t = TAG.format("this run's artifacts")
    rq = E8 / "results/rq1_heldout.json"
    hs = jl(HS8)
    ed = next(i for i, e in enumerate(hs["O2r_m50"]) if e["indicator"] == "ego_density_W3")
    NOT_FOUND_NOTES.append("C2 'Exp8 raw sign flip +0.143 / -0.126': no key in any Exp8/Exp10/Eval3/Research-3 file "
                           "holds these two values as a sign flip; only -0.126 occurs, as prereg_verdicts.P2.pooled_ci[0]")
    rows = [
        f"| C1 openness → breadth | Exp10 OPEN_home R2 {lad('OPEN_home', 'O2r_m50', 'R2')} on the confirmatory cohort | "
        f"R4 {lad('OPEN_home', 'O2r_m50', 'R4')} and R5 include 0; the all-papers build (Eval3 spec-curve headline "
        f"{L.num(SPC, 'headline.DL4.est')}) is mechanically coupled |",
        f"| C2 consolidation → less breadth | Exp8 P2 (edge persistence) pooled psp "
        f"{L.num(rq, 'prereg_verdicts.P2.pooled_psp')} {L.ci(rq, 'prereg_verdicts.P2.pooled_ci')}; ego_density_W3 "
        f"{L.num(HS8, f'O2r_m50[{ed}].pooled')} | the review's 'raw sign flip' pair `+0.143 / -0.126` could not be "
        "located in any file (NOT_FOUND) and is not used |",
        f"| C3 low retention ratio → breadth | Exp8 held-out {L.num(HS8, 'O2r_m50[' + str(next(i for i, e in enumerate(hs['O2r_m50']) if e['indicator'] == 'RETENTION_RATIO_early')) + '].pooled')} "
        f"given B5 | cohort R2 {lad('RETENTION_RATIO_early', 'O2r_m50', 'R2', grp='retention')}, R3 "
        f"{L.num(CR, "retention.['RETENTION_RATIO_early|O2r_m50|R3'].rho")}; PR2 raw difference (bottom − top) DEV "
        f"{L.num(DD, 'early_ratio_PR2.diff_bottom_minus_top')}, held-out "
        f"{L.num(DH, 'pooled_heldout4.early_ratio_PR2.diff_bottom_minus_top')}, 2010-14 cohort "
        f"{L.num(DH, 'pooled_cohort.early_ratio_PR2.diff_bottom_minus_top')} |",
        f"| C4 closure → entry slowdown | none | Exp11 DEV null: H-M1 {L.num(FE, 'DEV.H_M1_density.b', '{:+.4f}')} "
        f"{L.ci(FE, 'DEV.H_M1_density.ci', '{:+.4f}')} |"]
    b = (f"\n{t} Evidence from this run FOR and AGAINST each verdict:\n\n| claim | for | against |\n|---|---|---|\n"
         + "\n".join(rows) + "\n\n**RETENTION_RATIO_early does not survive type controls** (cohort R2 CI includes 0); "
         "it is moved from 'NEW' to 'does not survive type controls'.\n")
    apply(fn, "28.1_evidence", r"^### 28\.1 ", "append-to-section", b)
    begin(fn, "28.2")
    s = (f"\n**What survives beyond Cheng 2023 and Maillart 2026.** {t} A home-only partial association of novel, "
         f"non-persistent early neighbours with later breadth: on the "
         f"{L.num(CR, "primary.['OPEN_home|O2r_m50|R2'].n", '{:.0f}')}-concept cohort, NOV_res "
         f"{lad('NOV_res__home', 'O2r_m50', 'R2', grp='components')} and edge persistence "
         f"{lad('edge_persistence__home', 'O2r_m50', 'R2', grp='components')}, with the composite OPEN_home "
         f"{lad('OPEN_home', 'O2r_m50', 'R2')}. It is fragile at R4/R5, adds nothing to forecasting "
         f"({L.num(CR, 'secondary.frozen_prediction_O2r_m50.diff')}), and awaits the Frame-N confirmation "
         "(Section 32).\n")
    apply(fn, "28.2_survives", r"^### 28\.2 ", "append-to-section", s)
    begin(fn, "31")
    old = "RETENTION_RATIO_early (−0.114), "
    new = (f"RETENTION_RATIO_early (−0.114; {TAG.format(A_E10)} does not survive type controls: cohort R2 "
           f"{lad('RETENTION_RATIO_early', 'O2r_m50', 'R2', grp='retention')}), ")
    apply(fn, "31.2_retention", old, "text-replace", new)
    return f"# 07 Section 28: evidence for and against, and what survives\n\n## 28.1\n{b}\n## 28.2\n{s}\n## 31.2\n\n{new}\n"


# ============================================================================ item 8: secondary
def item8() -> str:
    fn = "08_exp8_exp10_secondary.md"
    t = TAG.format(A_E10)
    begin(fn, "25.5")
    rd = (E10 / "README.md").read_text().splitlines()
    assert rd[47].startswith("* **Leads replicated"), rd[47]
    leads = L.carry(E10 / "README.md", "lines:48-53")
    b1 = (f"\n{t} Secondary leads, verbatim from the Exp10 README (lines 48-53):\n\n"
          + "\n".join("> " + x for x in leads.splitlines()) + "\n\n"
          f"Keyed values: CONTACT_REACH on O2r_m50 given R0 {lad('CONTACT_REACH', 'O2r_m50', 'R0', grp='secondary')}, "
          f"without intersection-born concepts "
          f"{L.num(CR, "secondary.['CONTACT_REACH|O2r_m50|R0|excl_intersection_born'].rho")} "
          f"(n = {L.num(CR, "secondary.['CONTACT_REACH|O2r_m50|R0|excl_intersection_born'].n", '{:.0f}')}).\n")
    apply(fn, "25.5_leads", r"^### 25\.5 ", "append-to-section", b1)
    begin(fn, "25.6")
    lm = jl(LMC)
    b2 = (
        "### 25.6 Learned models (cohort)\n\n"
        f"{t}\n\n| outcome | metric | B5 | linear_all | diff [95% CI] | n | evaluable |\n|---|---|---|---|---|---|---|\n"
        + "\n".join(
            f"| {o} | {lm[o]['metric']} | {L.num(LMC, o + '.B5')} | {L.num(LMC, o + '.linear_all')} | "
            f"{L.num(LMC, o + '.diff')} {L.ci(LMC, o + '.diff_ci')} | {L.num(LMC, o + '.n', '{:.0f}')} | "
            f"{'yes' if lm[o]['evaluable'] else 'no'} |" for o in ("O2r_m50", "O2r_resid", "O3"))
        + f"\n| O4 | - | - | - | - | - | no: {lm['O4_EBM']} |\n\n"
        f"The transience (O3) row is **evaluable and null**: AUC {L.num(LMC, 'O3.linear_all')} vs "
        f"{L.num(LMC, 'O3.B5')}, difference {L.num(LMC, 'O3.diff')} {L.ci(LMC, 'O3.diff_ci')}. The earlier row, which "
        "labelled this transience difference as not evaluable, was wrong. The frozen B5 + OPEN_home forecast adds "
        f"{L.num(CR, 'secondary.frozen_prediction_O2r_m50.diff')} "
        f"{L.ci(CR, 'secondary.frozen_prediction_O2r_m50.diff_ci')} (Section 25.7).\n\n"
        "Source: `iter_4/gen_art/gen_art_experiment_10/results/learned_models_cohort.json`; "
        "`cohort_result.json` -> `secondary.frozen_prediction_O2r_m50`.\n")
    apply(fn, "25.6", r"^### 25\.6 ", "replace-section", b2)
    begin(fn, "19.5b")
    tag195 = (f"\n{t} On the 2015-2017 cohort the learned model does not predict transience either: O3 AUC "
              f"{L.num(LMC, 'O3.linear_all')} vs B5 {L.num(LMC, 'O3.B5')}, {L.num(LMC, 'O3.diff')} "
              f"{L.ci(LMC, 'O3.diff_ci')} (Section 25.6).\n")
    apply(fn, "19.5b_tag", r"^### 19\.5b ", "append-to-section", tag195)
    begin(fn, "19.7")
    tag197 = (f"\n{t} Cohort check: linear_all over B5 on O2r_m50 {L.num(LMC, 'O2r_m50.diff')} "
              f"{L.ci(LMC, 'O2r_m50.diff_ci')}; the frozen B5 + OPEN_home forecast gains "
              f"{L.num(CR, 'secondary.frozen_prediction_O2r_m50.diff')} (Section 25.6).\n")
    apply(fn, "19.7_tag", r"^### 19\.7 ", "append-to-section", tag197)
    # ---- per-group table
    begin(fn, "19.2")
    hs = jl(HS8)
    conf = [e["indicator"] for e in hs["O2r_m50"] if e.get("confirmed")]
    h = pd.read_csv(HUR)
    units = [u for u in ("PHYS", "LIFEENV", "SOC", "MATHDEC", "COH_DEVHOME", "COH_OTHER") if u in set(h.unit)]
    out_rows, md = [], []
    for ind in conf:
        cells, dag = [], 0
        for u in units:
            sub = h[(h.indicator == ind) & (h.outcome == "O2r_m50") & (h.unit == u)]
            if len(sub) != 1:
                cells.append("NOT_FOUND")
                continue
            r = sub.iloc[0]
            kp = f"indicator=={ind}&outcome==O2r_m50&unit=={u}"
            d = "†" if (r.ci_lo <= 0 <= r.ci_hi) else ""
            dag += bool(d)
            cells.append(f"{L.num(HUR, kp + '::rho')} [{L.num(HUR, kp + '::ci_lo')}, {L.num(HUR, kp + '::ci_hi')}] "
                         f"({L.num(HUR, kp + '::n', '{:.0f}')}){d}")
            out_rows.append({"indicator": ind, "unit": u, "psp": r.rho, "ci_lo": r.ci_lo, "ci_hi": r.ci_hi, "n": int(r.n),
                             "ci_includes_0": bool(d)})
        derive(f"item8.dagger.{ind}", dag)
        md.append((ind, cells))
    flush()
    pd.DataFrame(out_rows).to_csv(RES / "per_group_table.csv", index=False)
    tab = "\n".join(f"| {ind} | " + " | ".join(c) + f" | {L.num(DER, f"['item8.dagger.{ind}']", '{:.0f}')} |"
                    for ind, c in md)
    b3 = (f"\n{TAG.format(A_E8)} Per-group held-out results for the confirmed O2r_m50 indicators "
          "(psp [95% CI] (n); † = CI includes 0). Domain failures are shown, not averaged away:\n\n"
          "| indicator | " + " | ".join(units) + " | † cells |\n|---|" + "---|" * (len(units) + 1) + "\n" + tab + "\n\n"
          "Source: `iter_3/gen_art/gen_art_experiment_8/results/heldout_unit_results.csv` (outcome == O2r_m50); "
          "confirmed list from `heldout_summary.json -> O2r_m50[*].confirmed`.\n")
    apply(fn, "19.2_pergroup", r"^### 19\.2 ", "append-to-section", b3)
    DERIVED["item8.confirmed_list"] = conf
    return (f"# 08 Secondary: Exp10 leads, 25.6 learned models, tags under 19.5b / 19.7, per-group table\n\n## 25.5\n{b1}\n"
            f"{b2}\n## 19.5b\n{tag195}\n## 19.7\n{tag197}\n## 19.2 per-group table\n{b3}")


# ============================================================================ item 9: coverage table 30
def item9() -> str:
    fn = "09_coverage_table_30.md"
    begin(fn, "30")
    t = TAG.format("this evaluation")
    cnt = jl(RES / "artifact_counts.json")
    changes = [
        ("RQ1: holdout evaluation", "Iteration 4", "OPEN cohort confirmed",
         f"OPEN_home small, fragile ({lad('OPEN_home', 'O2r_m50', 'R2')} at R2; R4/R5 include 0)", A_E10),
        ("RQ1: top-10 on holdout", "Iteration 4", "Extended (OPEN composite)",
         "Extended (OPEN composite; OPEN_all mechanically coupled)", A_E10),
        ("RQ1: learned model", "Iteration 4", "Cohort +0.030",
         f"Cohort linear_all {L.num(LMC, 'O2r_m50.diff')}; B5 + OPEN_home {L.num(CR, 'secondary.frozen_prediction_O2r_m50.diff')} (no gain)", A_E10),
        ("RQ2: diffusion trajectories", "Iteration 4", "Done: CONTINUUM (Exp12)", "Done: CONTINUUM (Exp12)", A_E12),
        ("RQ2: breadth decomposition", "Iteration 4", "Done: explore 73%, retain 27%",
         f"Done (identity, not causal): s_explore − s_ret {L.num(DD, 'variants.ii_vol_PRIMARY.point.diff_explore_ret')} (DEV, variant ii)", A_E12),
        ("Strongest indicator analysis", "Iteration 4", "Decomposition + case studies",
         "Components (Exp10: NOV_res, low edge persistence); Exp11 H-P1 not run", f"{A_E10}, gen_art_experiment_11"),
        ("Case studies", "Iteration 4", "Done (7 matched pairs)", "Done (7 matched pairs, rebuilt from case_pairs.json)", A_E12),
        ("Record audit", "Iteration 4", "Done (1,290 claims, 0 mismatch)",
         "Done (1,290 claims, 0 mismatch; corrections now applied, Section 27.6)", A_EVAL3),
        ("Spec curve / robustness", "Iteration 4", "Done (1,920 specs, 99.7% CI>0)",
         "Done (1,920 specs, 99.7% CI>0): exploratory, all-papers build", A_EVAL3)]
    log = "\n".join(f"| {r} | {c} | {o} | {n} | {a} |" for r, c, o, n, a in changes)
    new_rows = [
        ("Exploratory AI stage", "Not started", "Not started", "Not started",
         f"Done: {L.num(DER, "['item1.n_atlas_rows']", '{:.0f}')}-concept atlas (retrospective, outcome-selected)",
         "pending iteration-5 artifact"),
        ("Home-first vs intersection", "Not started", "MIXED (Exp6)", "Exp9 failed", "Done: MIXED / HOME-FIRST held-out only; intersection-born HR < 1", "pending iteration-5 artifact"),
        ("Why it works", "Not started", "Not started", "Not started", "Exp10 components; Exp11 H-P1 not run", "pending iteration-5 artifact")]
    rep = REPORT5.read_text().splitlines()
    i = next(k for k, s in enumerate(rep) if s.startswith("## 30."))
    tab = []
    for s in rep[i + 1:]:
        if s.startswith("## "):
            break
        if s.startswith("|"):
            tab.append(s)
    t0 = next(k for k in range(i, len(rep)) if rep[k].startswith("|"))
    t1 = t0 + len(tab)
    L.carry(REPORT5, f"lines:{t0 + 1}-{t1}", "\n".join(tab) + "\n" + "\n".join(f"{r} {c} {o}" for r, c, o, n, a in changes))
    hdr = tab[0].rstrip() + " Iteration 5 |"
    sep = tab[1].rstrip() + "---|"
    body = []
    fix = {r: n for r, c, o, n, a in changes}
    for s in tab[2:]:
        cells = [c.strip() for c in s.strip().strip("|").split("|")]
        if cells[0] in fix:
            cells[4] = fix[cells[0]]
        body.append("| " + " | ".join(cells + ["pending iteration-5 artifact"]) + " |")
    for r in new_rows:
        body.append("| " + " | ".join(r) + " |")
    block = ("## 30. Coverage of the original request (final)\n\n"
             f"{t} Corrected cell by cell; the change log below lists each old cell, the new cell and the artifact "
             "behind it. Cells for this iteration's work read 'pending iteration-5 artifact'.\n\n"
             + "\n".join([hdr, sep] + body) + "\n\nChange log:\n\n| row | column | old cell | new cell | artifact |\n"
             "|---|---|---|---|---|\n" + log + "\n")
    apply(fn, "30_table", r"^## 30\. ", "replace-section", block)
    return f"# 09 Section 30 coverage table, corrected cell by cell\n\n{block}"


# ============================================================================ item 10: minor fixes (refs in refs.py)
def item10() -> str:
    fn = "10_minor_and_refs.md"
    begin(fn, "27.4")
    t = TAG.format(A_E7)
    key = "pooled4.specificity_rebuild.m_min_conditional_probability_proximity.ladder.models.R3_ret.coef.d0_ret_rel"
    try:
        d0 = L.num(S2H, key + ".coef")
    except Exception:  # noqa: BLE001
        d0 = "NOT_FOUND"
    if d0 == "NOT_FOUND":
        L.rows.pop()
        d0 = L.num(S2H, key, "{:+.3f}")
    rep = REPORT5.read_text()
    n_fcr = rep.count("footprint control rung")
    derive("item10.n_footprint_control_rung_in_report", n_fcr)
    flush()
    apply(fn, "fcr", "footprint control rung", "text-replace-all", "R3 rung")
    b1 = (f"The earlier name of the R3 rung (it was called the footprint-control rung) is replaced by 'R3 rung' "
          f"everywhere "
          f"({L.num(DER, "['item10.n_footprint_control_rung_in_report']", '{:.0f}')} occurrence(s)). {t} The Exp7 "
          f"d0 value under min-cp proximity at R3 is {d0} (`step2_heldout.json -> {key}`).\n")
    apply(fn, "27.4_fcr_note", r"^### 27\.4 ", "append-to-section", "\n" + TAG.format(A_E7) + " " + b1)
    begin(fn, "27.3")
    old = "Higgins I² drops to 0.43 (vs 0.66 over the 6 units)"
    new = (f"I2 = {L.num(HET, 'I2_subunit', '{:.2f}')} (21 home-field × period sub-units) vs I2 = "
           f"{L.num(HET, 'I2_unit6', '{:.2f}')} (6 units); the spec-curve headline pool has I2 = "
           f"{L.num(SPC, 'headline.DL4.I2', '{:.2f}')} (DL over 4 held-out groups) "
           f"{TAG.format(A_EVAL3)}")
    apply(fn, "27.3_I2", old, "text-replace", new)
    begin(fn, "27.2")
    b27 = (f"\n{TAG.format(A_EVAL3)} Label: **exploratory, all-papers build.** The curve varies composites of the "
           "all-papers components on already-unsealed held-out groups; it does not test the home-only build and is "
           f"not confirmatory. Headline pooled psp {L.num(SPC, 'headline.DL4.est')} "
           f"{L.ci(SPC, 'headline.DL4.ci')}, I2 = {L.num(SPC, 'headline.DL4.I2', '{:.2f}')}.\n")
    apply(fn, "27.2_label", r"^### 27\.2 ", "append-to-section", b27)
    return (f"# 10 Minor fixes (references: see references_master.md)\n\n## R3 rung\n\n{b1}\n## 27.3 I2 labels\n\n"
            f"Old: `{old}`\n\nNew: {new}\n\n## 27.2 label\n{b27}")


# ============================================================================ item 11: evidence synthesis
def item11() -> str:
    fn = "11_evidence_synthesis.md"
    begin(fn, "32")
    s = jl(SYN)
    idx = {(r["body"], r["feature"]): i for i, r in enumerate(s["rows"])}
    order = ["B1_DEV", "B2_PHYS", "B2_LIFEENV", "B2_SOC", "B2_MATHDEC", "B2_HELDOUT_pooled", "B3_EXP5_COHORT_2010_14",
             "B4_COHORT_2015_17"]
    tabs = []
    for f in ("OPEN_home", "NOVCHURN_home"):
        rows = []
        for b in order:
            i = idx[(b, f)]
            k = f"rows[{i}]"
            cells = [f"{L.num(SYN, f'{k}.{r}.psp')} {L.ci(SYN, f'{k}.{r}.ci')}" for r in ("R0", "R2", "R3")]
            rows.append(f"| {b} | {s['rows'][i]['onsets']} | {s['rows'][i]['status']} | " + " | ".join(cells)
                        + f" | {L.num(SYN, f'{k}.R2.n', '{:,.0f}')} | {L.num(SYN, f'{k}.placebo.p95_abs_psp')} |")
        rows.append("| B5 Frame N | new frame (iteration-5 artifact) | pending iteration-5 artifact | - | - | - | - | - |")
        tabs.append(f"**{f}** (O2r_m50):\n\n| body | onsets | status | R0 | R2 (primary) | R3 | n (R2) | placebo 95th "
                    "pct abs psp |\n|---|---|---|---|---|---|---|---|\n" + "\n".join(rows))
    pl = []
    for f in ("OPEN_home", "NOVCHURN_home"):
        p = f"pools.['{f}|R2']"
        pl.append(
            f"| {f} | {', '.join(s['pools'][f + '|R2']['nonselection_bodies'])} | "
            f"{L.num(SYN, p + '.nonselection.est')} | {L.ci(SYN, p + '.nonselection.dl_ci')} | "
            f"{L.ci(SYN, p + '.nonselection.hksj_ci')} | {L.num(SYN, p + '.nonselection.I2', '{:.2f}')} | "
            f"{L.num(SYN, p + '.nonselection.tau2_z', '{:.4f}')} | {s['pools'][f + '|R2']['sign_agreement_nonselection']} | "
            f"{L.num(SYN, p + '.all_bodies_includes_selection_data.est')} | "
            f"{L.num(SYN, p + '.selection_body_estimate')} | "
            f"{L.num(SYN, p + '.shrinkage_ratio_selection_over_nonselection', '{:.2f}')} |")
    lobo = []
    for f in ("OPEN_home", "NOVCHURN_home"):
        p = f"pools.['{f}|R2'].leave_one_body_out"
        lobo.append(f"{f}: " + "; ".join(f"without {b} {L.num(SYN, p + '.' + b)}"
                                          for b in s["pools"][f + "|R2"]["leave_one_body_out"]))
    g = s["gates"]
    block = (
        "## 32. Evidence synthesis across bodies (iteration 5, descriptive)\n\n"
        f"{TAG.format('this evaluation')} How the home-only openness association behaves on every body scored so far. "
        "Same estimator, rungs and frozen EXP5 constants as Exp10; gate G1 reproduces Exp10's EXP5 selection psp "
        f"({L.num(SYN, "gates.G1.['OPEN_home|O2r_m50|R0'].recomputed")} at R0, "
        f"{L.num(SYN, "gates.G1.['OPEN_home|O2r_m50|R2'].recomputed")} at R2) and gate G2 its cohort value "
        f"({L.num(SYN, 'gates.G2.R2.rho')} {L.ci(SYN, 'gates.G2.R2.ci')}). Each body is labelled by design status: "
        "**selection** = the data on which the index or its constants were chosen; **already-unsealed** = held-out "
        "data whose outcomes earlier artifacts had already read; **confirmatory** = never used before the test. "
        "NOVCHURN_home = mean(z NOV_res, −z edge_persistence), the two home components that carried the cohort "
        "signal; it was chosen on the 2015-17 cohort, so that body is 'selection' for it.\n\n"
        + "\n\n".join(tabs) + "\n\n"
        "Random-effects pools at R2 (Fisher z, bootstrap SE; headline over non-selection bodies only, B2 groups "
        "entered separately):\n\n"
        "| index | non-selection bodies | pooled psp | DL 95% CI | HKSJ 95% CI | I2 | tau2 (z) | sign agreement | "
        "all bodies (includes selection data) | selection body (DEV) | shrinkage DEV / pooled |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n" + "\n".join(pl) + "\n\n"
        "Leave one body out (pooled psp, R2): " + " | ".join(lobo) + ".\n\n"
        "[FIGURE:fig_evidence_forest]\n\n"
        "**Reading.** The home-only association is small and has the same sign in every body. It is consistently "
        "larger on the selection body (DEV) than on the non-selection pool (shrinkage ratio above), which is the "
        "winner's-curse pattern this run measured before. I2 is imprecise at this k. Because the non-selection bodies "
        "other than the 2015-17 cohort were already unsealed and reused, the pooled interval is **descriptive**: it "
        "is not a confirmation, and it is not a forecast gain (Section 25.7). NOVCHURN_home is shown for the Frame-N "
        "test; its cohort row is a selection estimate. The Frame-N row is empty and will be compared with this "
        "pool, not pooled into it.\n\n"
        "Source: `results/evidence_synthesis.json` (this artifact; `src/synthesis.py`); figure "
        "`figures/evidence_forest.png|pdf`.\n")
    apply(fn, "32_synthesis", r"^## 31\. ", "insert-new-section-after", block)
    return f"# 11 Evidence synthesis (new Section 32)\n\n{block}"


@logger.catch(reraise=True)
def main() -> None:
    DER.write_text("{}")
    files = {}
    for fn, f in (("01_case_studies_26_4.md", item1), ("02_exp11_25a.md", item2), ("03_exp10_rewrite.md", item3),
                  ("04_exp12_rewrite.md", item4), ("06_section23_restore.md", item6),
                  ("07_section28_evidence.md", item7), ("08_exp8_exp10_secondary.md", item8),
                  ("09_coverage_table_30.md", item9), ("10_minor_and_refs.md", item10),
                  ("11_evidence_synthesis.md", item11)):
        txt = f()
        (COR / fn).write_text(txt)
        files[fn] = len(txt)
        logger.info(f"{fn}: {len(txt):,} chars; ledger rows so far {len(L.rows)}")
    flush()
    idx = ["# Corrections pack, iteration 5: index", "",
           "Each file is insert-ready; every insert carries `[Correction, iteration 5, from art_...]`. Every number is "
           "ledgered in `results/claims_ledger_v4.csv` and re-verified by `verify_ledger_v4.py`. "
           "`src/apply_corrections.py` applies the Eval3 pack and then these blocks to a copy of the report "
           "(`report_corrected.md`); the per-block record is `results/corrections_applied.csv`.", "",
           "| file | blocks -> target (action) |", "|---|---|"]
    for fn in sorted({x["source_file"] for x in APPLY} | {"05_eval3_application.md"}):
        bl = [f"`{x['block_id']}` -> `{x['target'][:50]}` ({x['action']})" for x in APPLY if x["source_file"] == fn]
        if fn == "05_eval3_application.md":
            bl = ["Eval3 pack `00`-`11` applied; `27.6` replaced by the per-file list"]
        idx.append(f"| `{fn}` | " + "; ".join(bl) + " |")
    (COR / "00_index.md").write_text("\n".join(idx) + "\n")
    L.write(RES / "claims_ledger_v4.csv")
    jdump(RES / "apply_plan_iter5.json", APPLY)
    jdump(RES / "not_found_notes.json", NOT_FOUND_NOTES)
    st = pd.Series([r["status"] for r in L.rows]).value_counts().to_dict()
    logger.info(f"ledger v4: {len(L.rows)} rows; {st}")
    bad = [r for r in L.rows if r["status"] in ("MISMATCH", "NOT_FOUND")]
    for r in bad[:40]:
        logger.warning(f"{r['status']} {r['target_file']} {r['key_path']} {r['source_file']}")


if __name__ == "__main__":
    main()
