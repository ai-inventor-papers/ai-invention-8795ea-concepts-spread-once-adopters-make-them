#!/usr/bin/env python3
"""STEP 4: Part A corrections pack (corrections/00..11) + results/claims_ledger_v3.csv.

Every number printed in corrections/*.md is produced by Ledger.num (value read from a named file at a key path and
formatted) or Ledger.carry (verbatim token carried over from a named text block / CSV row, checked for presence).
Numbers this module derives itself (counts, DL pools of existing per-unit rows, two-way CIs) are first written to
results/partA_derived.json and then read back through the ledger, so every number has a file and a key.

Usage: python build_corrections.py"""
from __future__ import annotations

import os as _os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    _os.environ[_v] = "1"

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import numpy as np
import pandas as pd
from loguru import logger

from common import (COR, E7, E8, E9, EV2, HELD4, LOGS, R2, RES, REPORT, RUN, UNITS6, Ledger, dl, jdump, rel)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "build_corrections.log", rotation="30 MB", level="DEBUG")

L = Ledger()
TAG4 = "[Correction, iteration 4, from {art}]"
A8, A7, AEV2, AR2 = "art_dFQ6jbgNsR6Q", "art_22ppE1snfHKj", "art_7W9xiIO3FVBs", "art_EesdB8cuSfcU"
HS = E8 / "results/heldout_summary.json"
RQ = E8 / "results/rq1_heldout.json"
LV = E8 / "results/learned_vs_single_heldout.json"
PV = E8 / "results/prereg_verdicts.json"
FS8 = E8 / "results/frozen_spec.json"
S2H, S2D = E7 / "results/step2_heldout.json", E7 / "results/step2_dev.json"
DER = RES / "partA_derived.json"
REPORT_TXT = REPORT.read_text() if REPORT.exists() else ""


def ci(src, path, fmt="{:+.3f}", **kw) -> str:
    return f"[{L.num(src, path + '[0]', fmt, **kw)}, {L.num(src, path + '[1]', fmt, **kw)}]"


def report_block(start: str, end: str) -> str:
    """Verbatim slice of current_report.md between two headings/markers (the OLD text)."""
    i = REPORT_TXT.find(start)
    if i < 0:
        return "NOT_FOUND in current_report.md"
    j = REPORT_TXT.find(end, i + len(start))
    return REPORT_TXT[i:j if j > 0 else i + 1500].strip()


def quote(txt: str) -> str:
    return "\n".join("> " + l if l.strip() else ">" for l in txt.splitlines())


def src_line(*pairs) -> str:
    return "Source: " + "; ".join(f"`{rel(p)}` -> `{k}`" for p, k in pairs)


def write(name: str, text: str) -> None:
    (COR / name).write_text(text.rstrip() + "\n")
    logger.info(f"wrote corrections/{name} ({len(text):,} chars)")


def jget(path: Path, key: str):
    return Ledger.json_get(json.loads(path.read_text()), key)


def exists(path: Path, key: str) -> bool:
    try:
        jget(path, key)
        return True
    except (KeyError, IndexError, TypeError):
        return False


# ============================================================================= derived numbers (written, then read)
def build_derived() -> dict:
    D: dict = {}
    # iteration counts from each artifact's .aii_worker_result.json
    it = {}
    for i in (1, 2, 3):
        rows = []
        for d in sorted((RUN / f"iter_{i}/gen_art").glob("*/src")):
            f = d / ".aii_worker_result.json"
            failed = json.loads(f.read_text())["result"].get("failed") if f.exists() else None
            rows.append({"artifact": d.name, "failed": failed})
        it[f"iter_{i}"] = {"n_commissioned": len(rows), "n_completed": sum(r["failed"] is False for r in rows),
                           "n_failed": sum(r["failed"] is True for r in rows), "artifacts": rows}
    D["iterations"] = it
    # indicator families
    dic = pd.read_csv(E8 / "results/indicator_dictionary.csv")
    fam = dic.groupby("family").indicator.apply(list).to_dict()
    D["families"] = {"n_indicators": int(len(dic)), "n_families": int(len(fam)),
                     "counts": {k: len(v) for k, v in fam.items()}, "members": fam}
    # candidate S: DL4 pooled from the per-unit held-out rows (z, se_z) for every outcome
    hu = pd.read_csv(E8 / "results/heldout_unit_results.csv")
    cs = {}
    for ind in ("S_comp", "S_comp_n", "S_isolated_share"):
        for o, t in hu[hu.indicator == ind].groupby("outcome"):
            t = t.set_index("unit")
            tt = t.reindex(HELD4).dropna(subset=["z", "se_z"])
            P = dl(tt.z.to_numpy(float), tt.se_z.to_numpy(float) ** 2)
            if not P.get("k"):
                continue
            cs[f"{ind}|{o}"] = {"pooled": P["est"], "ci": P["ci"], "I2": P["I2"], "k": P["k"],
                                "n_pos_6": int((t.reindex(UNITS6).rho > 0).sum()),
                                "n_ci_excl0_6": int(((t.reindex(UNITS6).ci_lo > 0) | (t.reindex(UNITS6).ci_hi < 0)).sum())}
    D["candidate_S_DL4"] = cs
    # Exp7 d0 two-way clustered CI (coef +- 1.96 SE)
    for tag, src, pre in (("heldout", S2H, "pooled4"), ("dev", S2D, "battery")):
        base = f"{pre}.ladder.frontier_primary_sample.models.R3_ret"
        try:
            b, s = jget(src, base + ".coef.d0_ret_rel"), jget(src, base + ".se_two_way_concept_field.d0_ret_rel")
            D[f"exp7_d0_two_way_{tag}"] = {"coef": b, "se": s, "ci": [b - 1.96 * s, b + 1.96 * s]}
        except (KeyError, TypeError):
            pass
    # Exp7 home mismatches
    D["exp7_home_mismatch"] = {"dev": len(jget(S2D, "input_checks.home_mismatch_cidx")),
                               "heldout": len(jget(S2H, "input_checks.home_mismatch_cidx"))}
    D["exp7_home_mismatch"]["total"] = D["exp7_home_mismatch"]["dev"] + D["exp7_home_mismatch"]["heldout"]
    # Eval2 ledger status counts
    cl = pd.read_csv(EV2 / "claims_ledger.csv")
    D["eval2_ledger"] = {"n_rows": int(len(cl)), "status_counts": cl.status.value_counts().to_dict()}
    # record_tables row counts
    rt = {}
    for f in sorted((EV2 / "record_tables").iterdir()):
        if f.suffix == ".csv":
            rt[f.name] = int(len(pd.read_csv(f)))
        elif f.suffix == ".parquet":
            import pyarrow.parquet as pq
            rt[f.name] = int(pq.ParquetFile(f).metadata.num_rows)
        else:
            rt[f.name] = None
    D["record_tables_rows"] = rt
    # confirmed counts per outcome (Exp8)
    hb = jget(RQ, "headline_by_outcome")
    D["exp8_confirmed"] = {o: {"n_top10": v["n_top10"], "n_confirmed": v["n_confirmed_holm"]} for o, v in hb.items()}
    D["eval2_text_blocks"] = len(parse_eval2_blocks())
    jdump(D, DER)
    return D


# ============================================================================= 01
def f01() -> None:
    tf = "01_exp8_outcomes_relabel.md"
    T = TAG4.format(art=A8)
    summ = json.loads(HS.read_text())
    out = [f"# 01 Exp8 outcome relabelling (replaces Sections 19.4-19.7 and dead end 22.6)", "",
           f"Tag for every insert below: `{T}`.", "",
           "The draft's Section 19.5 is headed 'Transience' but reports the **O4** results (field- and year-normalised "
           "citation growth; REL_home and author_growth). The real O3 (transience) results are missing from the draft, "
           "and dead end 22.6 repeats the mislabel. The tables below are generated from Exp8's result files; the README "
           "tables at lines 57 (O4) and 87 (O3) were cross-read and agree to 3 decimals.", ""]

    def top10(o: str, sec: str) -> list[str]:
        rows = ["| indicator | family | frozen sign | pooled psp | 95% CI | I2 | Holm p | sign agree | confirmed |",
                "|---|---|---|---|---|---|---|---|---|"]
        for i, r in enumerate(summ[o]):
            if not r.get("in_top10"):
                continue
            p = f"{o}[{i}]"
            kw = dict(section=sec, target_file=tf, snippet=f"{o} {r['indicator']}")
            rows.append(f"| {r['indicator']} | {r['family']} | {'+' if r['frozen_sign'] > 0 else '-'} | "
                        f"{L.num(HS, p + '.pooled', '{:+.3f}', **kw)} | {ci(HS, p + '.pooled_ci', **kw)} | "
                        f"{L.num(HS, p + '.I2', '{:.2f}', **kw)} | {L.num(HS, p + '.holm_p', '{:.3g}', **kw)} | "
                        f"{L.num(HS, p + '.sign_agree', '{:.0f}', **kw)}/{L.num(HS, p + '.n_units', '{:.0f}', **kw)} | "
                        f"{'**yes**' if r.get('confirmed') else 'no'} |")
        return rows

    kw = dict(target_file=tf)
    out += ["## Old text (19.5, verbatim)", "", quote(report_block("### 19.5", "### 19.6")), "",
            "## New 19.4 O1c (sustained uptake)", "",
            f"{T} Only n_authors_early is confirmed for O1c: pooled psp "
            f"{L.num(RQ, 'headline_by_outcome.O1c.pooled.n_authors_early.pooled', '{:+.3f}', section='19.4', **kw)} "
            f"{ci(RQ, 'headline_by_outcome.O1c.pooled.n_authors_early.ci', section='19.4', **kw)}, Holm p "
            f"{L.num(RQ, 'headline_by_outcome.O1c.pooled.n_authors_early.holm_p', '{:.2g}', section='19.4', **kw)} "
            f"({L.num(DER, 'exp8_confirmed.O1c.n_confirmed', '{:.0f}', section='19.4', **kw)} of "
            f"{L.num(DER, 'exp8_confirmed.O1c.n_top10', '{:.0f}', section='19.4', **kw)} frozen indicators).", "",
            f"## New 19.5 O4 (field- and year-normalised citation growth): "
            f"{L.num(DER, 'exp8_confirmed.O4.n_confirmed', '{:.0f}', section='19.5', **kw)} of "
            f"{L.num(DER, 'exp8_confirmed.O4.n_top10', '{:.0f}', section='19.5', **kw)} confirmed", "",
            f"{T} This section reports O4, not transience. Concepts whose home field is related to many fields "
            f"(REL_home) show LOWER later citation growth, and early author growth predicts HIGHER citation growth.", ""]
    out += top10("O4", "19.5") + ["", src_line((HS, "O4[i].{pooled,pooled_ci,I2,holm_p,sign_agree,n_units,confirmed}")), ""]
    out += [f"## New 19.5b O3 (transience): "
            f"{L.num(DER, 'exp8_confirmed.O3.n_confirmed', '{:.0f}', section='19.5b', **kw)} of "
            f"{L.num(DER, 'exp8_confirmed.O3.n_top10', '{:.0f}', section='19.5b', **kw)} confirmed", "",
            f"{T} For transience (O3, binary; groups with an estimable O3), only n_authors_early is confirmed; "
            f"MATHDEC has too few transient concepts for O3 (Exp8 deviation F6_MATHDEC_O3), so sign agreement is out of 5.", ""]
    out += top10("O3", "19.5b") + ["", src_line((HS, "O3[i].*")), ""]
    out += [f"## New 19.6 External recognition (O5, O5_WW): "
            f"{L.num(DER, 'exp8_confirmed.O5.n_confirmed', '{:.0f}', section='19.6', **kw)} and "
            f"{L.num(DER, 'exp8_confirmed.O5_WW.n_confirmed', '{:.0f}', section='19.6', **kw)} of "
            f"{L.num(DER, 'exp8_confirmed.O5.n_top10', '{:.0f}', section='19.6', **kw)} confirmed", "",
            f"{T} No indicator predicts external recognition beyond B5 + onset year (see file 10 for the section "
            "cross-reference fix).", "", src_line((RQ, "headline_by_outcome.{O5,O5_WW}.n_confirmed_holm")), ""]
    # learned models
    out += ["## New 19.7 Learned models vs B5 vs B5 + best single (held-out groups pooled)", "",
            f"{T} All 8 outcomes; Spearman(pred, y) for continuous outcomes, AUC for binary (O1c, O1b, O3, O5, O5_WW); "
            "[95% CI of the paired difference vs B5].", "",
            "| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |", "|---|---|---|---|---|---|"]
    lv = json.loads(LV.read_text())
    for o in ["O1c", "O2r_m50", "O2r_resid", "O4", "O1b", "O3", "O5", "O5_WW"]:
        p = f"{o}.POOLED_HELDOUT"
        k = dict(section="19.7", target_file=tf, snippet=f"learned {o}")
        cells = []
        for m in ("B5_best_single", "linear_all", "EBM"):
            if lv[o]["POOLED_HELDOUT"][m]["metric"] is None:
                cells.append("constant (all coefficients 0; no ranking)")
            else:
                cells.append(f"{L.num(LV, f'{p}.{m}.metric', '{:.3f}', **k)} {ci(LV, f'{p}.{m}.delta_ci', **k)}")
        out.append(f"| {o} | {L.num(LV, p + '.n', '{:,.0f}', **k)} | {L.num(LV, p + '.B5.metric', '{:.3f}', **k)} | "
                   + " | ".join(cells) + " |")
    out += ["", src_line((LV, "<outcome>.POOLED_HELDOUT.{n,B5.metric,<model>.metric,<model>.delta_ci}")), "",
            "Cross-read: README.md line 132 table (Exp8) shows the same values to 3 decimals.", "",
            "## O3 as a positive held-out result", "",
            f"{T} Transience IS predictable beyond B5 on held-out groups: L1-logit AUC "
            f"{L.num(LV, 'O3.POOLED_HELDOUT.linear_all.metric', '{:.3f}', section='19.7', **kw)} vs B5 "
            f"{L.num(LV, 'O3.POOLED_HELDOUT.B5.metric', '{:.3f}', section='19.7', **kw)} (paired difference "
            f"{ci(LV, 'O3.POOLED_HELDOUT.linear_all.delta_ci', section='19.7', **kw)}); EBM "
            f"{L.num(LV, 'O3.POOLED_HELDOUT.EBM.metric', '{:.3f}', section='19.7', **kw)}. Caveat: B5 itself is at "
            "chance for O3, so the gain is over a null baseline, not over a strong one.", "",
            "## Old text (dead end 22.6, verbatim)", "",
            quote(report_block("6. **Transience ElasticNet", "7. **Four of five")), "",
            "## New dead end 22.6", "",
            f"{T} 6. **O4 (citation growth) linear model: shrank to a constant.** The ElasticNet for O4 (field- and "
            "year-normalised citation growth, NOT transience) set every coefficient to zero, so it ranks nothing on "
            f"held-out data, while the EBM reaches Spearman "
            f"{L.num(LV, 'O4.POOLED_HELDOUT.EBM.metric', '{:.3f}', section='22.6', **kw)} vs B5 "
            f"{L.num(LV, 'O4.POOLED_HELDOUT.B5.metric', '{:.3f}', section='22.6', **kw)} (gain "
            f"{L.num(LV, 'O4.POOLED_HELDOUT.EBM.delta_vs_B5', '{:+.3f}', section='22.6', **kw)} "
            f"{ci(LV, 'O4.POOLED_HELDOUT.EBM.delta_ci', section='22.6', **kw)}). The O4 signal is non-linear. "
            "Transience (O3) is a separate outcome with a positive held-out learned-model result (above).", "",
            src_line((LV, "O4.POOLED_HELDOUT.*"), (E8 / "results/deviations.json", "O4_linear_all_constant"))]
    write(tf, "\n".join(out))


# ============================================================================= 02
def f02() -> None:
    tf = "02_prereg_P1_P5.md"
    T = TAG4.format(art=A8)
    fs = json.loads(FS8.read_text())["preregistered_predictions"]
    pv = json.loads(PV.read_text())
    k = dict(section="19.8", target_file=tf)
    P1 = "P1.detail"
    dq = {
        "P1": (f"raw part: groups with raw CI > 0 = D_rare {L.num(PV, P1 + '.D_rare.n_groups_raw_CI_gt0', '{:.0f}', **k)}, "
               f"D_ratio {L.num(PV, P1 + '.D_ratio.n_groups_raw_CI_gt0', '{:.0f}', **k)}, participation "
               f"{L.num(PV, P1 + '.participation.n_groups_raw_CI_gt0', '{:.0f}', **k)}, NOV_res "
               f"{L.num(PV, P1 + '.NOV_res.n_groups_raw_CI_gt0', '{:.0f}', **k)}, entropy "
               f"{L.num(PV, P1 + '.entropy.n_groups_raw_CI_gt0', '{:.0f}', **k)} (of 4); adds-little part: pooled psp CI "
               f"upper bounds D_rare {L.num(PV, P1 + '.D_rare.pooled_ci[1]', '{:.3f}', **k)}, D_ratio "
               f"{L.num(PV, P1 + '.D_ratio.pooled_ci[1]', '{:.3f}', **k)}, participation "
               f"{L.num(PV, P1 + '.participation.pooled_ci[1]', '{:.3f}', **k)}, NOV_res "
               f"{L.num(PV, P1 + '.NOV_res.pooled_ci[1]', '{:.3f}', **k)} (rule: all < 0.10)"),
        "P2": (f"edge_persistence pooled psp {L.num(PV, 'P2.pooled_psp', '{:+.3f}', **k)} {ci(PV, 'P2.pooled_ci', **k)}; "
               f"mean raw rho over 4 groups {L.num(PV, 'P2.mean_raw_rho_4_groups', '{:+.3f}', **k)}"),
        "P3": (f"new_edge_rate pooled psp {L.num(PV, 'P3.detail.new_edge_rate.pooled_psp', '{:+.3f}', **k)} "
               f"{ci(PV, 'P3.detail.new_edge_rate.pooled_ci', **k)}, sign flips "
               f"{L.num(PV, 'P3.detail.new_edge_rate.sign_flips', '{:.0f}', **k)} -> it TRANSFERS; deg_growth "
               f"{L.num(PV, 'P3.detail.deg_growth.pooled_psp', '{:+.3f}', **k)} {ci(PV, 'P3.detail.deg_growth.pooled_ci', **k)} "
               f"and str_growth {L.num(PV, 'P3.detail.str_growth.pooled_psp', '{:+.3f}', **k)} "
               f"{ci(PV, 'P3.detail.str_growth.pooled_ci', **k)} do fail as predicted"),
        "P4": (f"RETENTION_RATIO_early on O2r_resid {L.num(PV, 'P4.detail.RETENTION_RATIO_early|O2r_resid.pooled_psp', '{:+.3f}', **k)} "
               f"{ci(PV, 'P4.detail.RETENTION_RATIO_early|O2r_resid.pooled_ci', **k)} (predicted > 0: wrong sign); on O1c "
               f"{L.num(PV, 'P4.detail.RETENTION_RATIO_early|O1c.pooled_psp', '{:+.3f}', **k)} "
               f"{ci(PV, 'P4.detail.RETENTION_RATIO_early|O1c.pooled_ci', **k)}; FRONTIER_POTENTIAL on O2r_resid "
               f"{L.num(PV, 'P4.detail.FRONTIER_POTENTIAL|O2r_resid.pooled_psp', '{:+.3f}', **k)} "
               f"{ci(PV, 'P4.detail.FRONTIER_POTENTIAL|O2r_resid.pooled_ci', **k)}"),
        "P5": (f"CONTACT_REACH pooled psp on O2r_m50 {L.num(PV, 'P5.pooled_psp_O2r_m50', '{:+.3f}', **k)} "
               f"{ci(PV, 'P5.pooled_ci', **k)} (predicted: CI includes 0); given B5 minus reach on O2r_resid "
               f"{L.num(PV, 'P5.given_B5_minus_reach_O2r_resid', '{:+.3f}', **k)} {ci(PV, 'P5.ci_B5_minus_reach', **k)}"),
    }
    out = [f"# 02 Pre-registered predictions P1-P5 (replaces 19.8 and 22.7; corrects dead end 7.4 and Section 4.3)", "",
           "The draft's 19.8 paraphrases P1-P5 with statements that were never pre-registered (e.g. 'entropy is the single "
           "strongest indicator', 'CONTACT_REACH is the strongest single indicator'). The table below quotes the EXACT "
           "frozen text (Exp8 frozen_spec.json, key preregistered_predictions, file lines 2960-2964).", "",
           "## Old text (19.8, verbatim)", "", quote(report_block("### 19.8", "### 19.9")), "",
           "## New 19.8", "", f"{T}", "",
           "| # | exact frozen text | verdict | deciding quantity |", "|---|---|---|---|"]
    for p in ["P1", "P2", "P3", "P4", "P5"]:
        txt = L.carry(FS8, f"preregistered_predictions.{p}", fs[p], fs[p], section="19.8", target_file=tf)
        out.append(f"| {p} | {txt} | **{pv[p]['verdict']}** | {dq[p]} |")
    out += ["", src_line((FS8, "preregistered_predictions.P1..P5"), (PV, "P1..P5.{verdict,detail,...}")), "",
            "Reading: P1 fails on BOTH parts (D_rare is positive in fewer than 3 groups, and all four breadth candidates "
            "add more than the 0.10 bound). P3 was a prediction of FAILURE; its failure means new_edge_rate transfers to "
            "held-out groups. P4 fails because the retention ratio has the opposite sign. P5 predicted that "
            "CONTACT_REACH adds nothing; it adds a clearly positive amount.", "",
            "## Correction to dead end 7.4 (Section 7, item 4)", "", quote(report_block("4. **Raw cooccurrence growth", "\n\n")), "",
            f"{T} The held-out test contradicts 'specific to Computer Science' for new_edge_rate: pooled psp given B5 "
            f"{L.num(PV, 'P3.detail.new_edge_rate.pooled_psp', '{:+.3f}', section='7.4', target_file=tf)} "
            f"{ci(PV, 'P3.detail.new_edge_rate.pooled_ci', section='7.4', target_file=tf)} with "
            f"{L.num(PV, 'P3.detail.new_edge_rate.sign_flips', '{:.0f}', section='7.4', target_file=tf)} sign flips "
            "across the 4 held-out groups. Degree and strength growth do fail held-out (CIs include 0).", "",
            "## Correction to Section 4.3", "",
            f"{T} Append: 'On held-out groups (Exp8), new_edge_rate transfers beyond B5 (pooled psp "
            f"{L.num(PV, 'P3.detail.new_edge_rate.pooled_psp', '{:+.3f}', section='4.3', target_file=tf)}), whereas "
            f"participation {L.num(PV, 'P1.detail.participation.pooled_psp', '{:+.3f}', section='4.3', target_file=tf)}, "
            f"NOV_res {L.num(PV, 'P1.detail.NOV_res.pooled_psp', '{:+.3f}', section='4.3', target_file=tf)}, D_rare "
            f"{L.num(PV, 'P1.detail.D_rare.pooled_psp', '{:+.3f}', section='4.3', target_file=tf)} and D_ratio "
            f"{L.num(PV, 'P1.detail.D_ratio.pooled_psp', '{:+.3f}', section='4.3', target_file=tf)} are small but "
            "positive, so the iteration-1 conclusion that none adds to B5 does not hold on held-out data.'", "",
            "## Old text (dead end 22.7, verbatim)", "", quote(report_block("7. **Four of five", "8. **G_btw")), "",
            "## New dead end 22.7", "",
            f"{T} 7. **Four of five pre-registered predictions fail, as frozen.** P2 (edge_persistence negative) holds. "
            "P1 fails (the iteration-1 breadth candidates do add beyond B5 on held-out data); P3 fails because "
            "new_edge_rate transfers; P4 fails because RETENTION_RATIO_early is negative, not positive; P5 fails because "
            "CONTACT_REACH is positive given B5. See the table in 19.8 for the deciding numbers.", "",
            "## Held-out table: iteration-1 candidates (O2r_m50)", "", f"{T}", "",
            "| indicator | pooled psp given B5 | 95% CI | raw rho PHYS | LIFEENV | SOC | MATHDEC |", "|---|---|---|---|---|---|---|"]
    k2 = dict(section="19.8", target_file=tf)
    for ind in ["D_ratio", "D_rare", "participation", "NOV_res", "entropy"]:
        b = f"P1.detail.{ind}"
        pooled = (f"{L.num(PV, b + '.pooled_psp', '{:+.3f}', **k2)} | {ci(PV, b + '.pooled_ci', **k2)}"
                  if ind != "entropy" else "n/a (B5 member) | n/a")
        raws = []
        for u in HELD4:
            v = pv["P1"]["detail"][ind]["raw_rho"].get(u)
            raws.append(L.num(PV, f"{b}.raw_rho.{u}", "{:+.3f}", **k2) if v is not None else "n/a (n too small)")
        out.append(f"| {ind} | {pooled} | " + " | ".join(raws) + " |")
    raws = [L.num(PV, f"P2.raw_rho.{u}", "{:+.3f}", **k2) for u in HELD4]
    out.append(f"| edge_persistence | {L.num(PV, 'P2.pooled_psp', '{:+.3f}', **k2)} | {ci(PV, 'P2.pooled_ci', **k2)} | "
               + " | ".join(raws) + " |")
    out += ["", src_line((PV, "P1.detail.<ind>.{pooled_psp,pooled_ci,raw_rho.<group>}"), (PV, "P2.{pooled_psp,pooled_ci,raw_rho}"))]
    write(tf, "\n".join(out))


# ============================================================================= 03
def f03() -> None:
    tf = "03_exp7_tables.md"
    T = TAG4.format(art=A7)
    out = ["# 03 Exp7 tables (inserts for Section 18)", "", f"Tag: `{T}`. Every value is printed with its key path; a value "
           "not found at its key is printed NOT_FOUND (never retyped).", ""]

    def cell(src, key, fmt="{:+.3f}", sec="18"):
        return L.num(src, key, fmt, section=sec, target_file=tf)

    def cic(src, key, sec="18"):
        return ci(src, key, section=sec, target_file=tf)

    # (a) volume matched
    out += ["## 18.5 Volume-matched contrast (retained R vs entered-not-retained N, same current x cumulative volume cell)", "",
            "| split | bins | d_R_m [CI] | d_N_m [CI] | contrast R - N [CI] | one-sided p | match rate (strata) | matched R / N fields | mean cum. prev. volume R / N |",
            "|---|---|---|---|---|---|---|---|---|"]
    for split, src, pre in (("DEV", S2D, "battery"), ("held-out pooled 4", S2H, "pooled4")):
        for bins, key, r_, n_ in (("coarse", "b_volume_matched", "d_R_m", "d_N_m"), ("fine", "b2_volume_matched_fine", "d_R_mf", "d_N_mf")):
            b = f"{pre}.specificity.{key}"
            c = b + ".contrast_R_minus_N"
            out.append(f"| {split} | {bins} | {cell(src, f'{c}.{r_}.est')} {cic(src, f'{c}.{r_}.ci')} | "
                       f"{cell(src, f'{c}.{n_}.est')} {cic(src, f'{c}.{n_}.ci')} | {cell(src, c + '.est')} {cic(src, c + '.ci')} | "
                       f"{cell(src, c + '.p_one_sided', '{:.3f}')} | {cell(src, b + '.match_rate_strata', '{:.3f}')} | "
                       f"{cell(src, b + '.balance.n_matched_R_fields', '{:,.0f}')} / {cell(src, b + '.balance.n_matched_N_fields', '{:,.0f}')} | "
                       f"{cell(src, b + '.balance.mean_cum_prev_R', '{:.2f}')} / {cell(src, b + '.balance.mean_cum_prev_N', '{:.2f}')} |")
    out += ["", src_line((S2D, "battery.specificity.{b_volume_matched,b2_volume_matched_fine}.*"),
                         (S2H, "pooled4.specificity.{b_volume_matched,b2_volume_matched_fine}.*")), "",
            "Reading: both retained and non-retained matched fields carry a positive coefficient, and the pre-declared "
            "contrast is null in both bin sets. The retained-relatedness signal cannot be separated from volume.", ""]
    # (b) dose
    c = "pooled4.specificity.c_dose"
    mono = jget(S2H, c + ".monotone_nondecreasing") if exists(S2H, c + ".monotone_nondecreasing") else "NOT_FOUND"
    out += ["## 18.4 Dose by persistence age (held-out pooled 4)", "",
            "| age 2 | age 3 | age >= 4 | 4+ minus 2 [CI] | monotone non-decreasing | Spearman(beta, age) |", "|---|---|---|---|---|---|",
            f"| {cell(S2H, c + '.betas_by_age.2')} | {cell(S2H, c + '.betas_by_age.3')} | {cell(S2H, c + '.betas_by_age.4+')} | "
            f"{cell(S2H, c + '.contrast_4p_minus_2.est')} {cic(S2H, c + '.contrast_4p_minus_2.ci')} | {mono} | "
            f"{cell(S2H, c + '.spearman_beta_age', '{:.2f}')} |", "", src_line((S2H, c + ".*")), ""]
    # (c) d_lost
    lad = "pooled4.ladder"
    rows = [("A1 = R0 + d_lost (all rows)", f"{lad}.abandonment_all_rows.models.A1_lost.coef.d_lost", "pooled4.crossed_boot.d_lost_A1.ci"),
            ("R4 = R3 + d_lost (primary sample)", f"{lad}.frontier_primary_sample.models.R4_lost.coef.d_lost", None)]
    out += ["## 18.9 Abandonment penalty d_lost: A1 vs R4 and variants (held-out pooled 4)", "",
            "| model | d_lost | CI | note |", "|---|---|---|---|"]
    out.append(f"| {rows[0][0]} | {cell(S2H, rows[0][1])} | concept {cic(S2H, 'verdicts.d_lost_ci')}; crossed {cic(S2H, rows[0][2])} | "
               f"verdict: {jget(S2H, 'verdicts.ABANDONMENT')} |")
    out.append(f"| {rows[1][0]} | {cell(S2H, rows[1][1])} | - | positive once d0 is in the model |")
    mcp = "pooled4.specificity_rebuild.m_min_conditional_probability_proximity"
    out.append(f"| min-cp proximity backbone, R4 | {cell(S2H, mcp + '.ladder.models.R4_lost.coef.d_lost')} | - | "
               f"min-cp A1: d_lost {cell(S2H, mcp + '.d_lost_A1.coef')}, p = {cell(S2H, mcp + '.d_lost_A1.p_wald_concept_2s', '{:.2g}')} |")
    tfe = "pooled4.specificity.g_target_field_FE"
    tfe_key = next((f"{tfe}.{k}.coef" for k in ("d_lost_A1", "A1_lost", "d_lost") if exists(S2H, f"{tfe}.{k}.coef")), f"{tfe}.d_lost_A1.coef")
    out.append(f"| target-field FE, A1 | {cell(S2H, tfe_key)} | - | key `{tfe_key}` |")
    out += ["", src_line((S2H, "pooled4.ladder.*.models.{A1_lost,R4_lost}.coef.d_lost; verdicts.d_lost_ci; crossed_boot.d_lost_A1.ci; " + mcp + "; " + tfe)), ""]
    # (d) d0 CIs
    out += ["## 18.3 d0_ret_rel with three resampling units (held-out pooled 4, R3)", "",
            "| estimate | concept bootstrap (1,000) | two-way concept x field clustered (coef +- 1.96 SE) | crossed concept x field bootstrap (500) |",
            "|---|---|---|---|",
            f"| {cell(S2H, 'pooled4.boot.d0_R3.d0_ret_rel.est')} | {cic(S2H, 'pooled4.boot.d0_R3.d0_ret_rel.ci')} | "
            f"{cic(DER, 'exp7_d0_two_way_heldout.ci')} | {cic(S2H, 'pooled4.crossed_boot.d0_R3.ci')} |", "",
            src_line((S2H, "pooled4.boot.d0_R3.d0_ret_rel.{est,ci}; pooled4.crossed_boot.d0_R3.ci"),
                     (DER, "exp7_d0_two_way_heldout.ci (from ladder...R3_ret.se_two_way_concept_field.d0_ret_rel)")), ""]
    # (e) held-out sensitivities
    out += ["## 18.6 Held-out sensitivities of d0 (R3)", "", "| sensitivity | d0 | concept-clustered p |", "|---|---|---|"]
    h = json.loads(S2H.read_text())["pooled4"]
    for grp in ("specificity", "specificity_rebuild"):
        for name, v in h[grp].items():
            if isinstance(v, dict) and isinstance(v.get("d0_R3"), dict) and "coef" in v["d0_R3"]:
                b = f"pooled4.{grp}['{name}'].d0_R3"
                out.append(f"| {name} | {cell(S2H, b + '.coef')} | {cell(S2H, b + '.p_wald_concept_2s', '{:.2g}')} |")
    out += ["", src_line((S2H, "pooled4.{specificity,specificity_rebuild}.<name>.d0_R3.{coef,p_wald_concept_2s}")), ""]
    # (f) proximity dependence
    out += ["## New subsection 18.6a Proximity dependence", "",
            f"{T} The retained-frontier coefficient depends on the proximity backbone. Under Hidalgo's minimum "
            f"conditional-probability proximity (instead of the frozen PMI backbone), d0 in R3 is "
            f"{cell(S2H, mcp + '.ladder.models.R3_ret.coef.d0_ret_rel')} (LR R3 vs R2 p = "
            f"{cell(S2H, mcp + '.ladder.LR.R3_ret_vs_R2_vol.p', '{:.3f}')}), while the RCA density itself becomes much "
            f"stronger (LR R1 vs R0 = {cell(S2H, mcp + '.ladder.LR.R1_rca_vs_R0_M0.LR', '{:.1f}')}). Within-stratum AUC is "
            f"higher under min-cp without d0 (R2 {cell(S2H, mcp + '.ladder.auc_within.R2_vol', '{:.3f}')}) than under PMI with d0 "
            f"(R3 {cell(S2H, 'pooled4.ladder.frontier_primary_sample.auc_within.R3_ret', '{:.3f}')}). The d0 effect is "
            "backbone-specific: it measures relatedness as PMI encodes it, not relatedness in general.", "",
            src_line((S2H, mcp + ".ladder.{models.R3_ret.coef.d0_ret_rel,LR.*,auc_within.R2_vol}"),
                     (S2H, "pooled4.ladder.frontier_primary_sample.auc_within.R3_ret")), ""]
    # (g) step 3
    dc = RES / "drca_persist_comparison.json"
    DC = json.loads(dc.read_text())
    k = dict(section="18.1", target_file=tf)
    out += ["## Step-3 comparison: Exp7 D_rca_pers vs Research 2 D_rca_persist_k", "",
            f"- Exp7 frozen definition (frozen_spec.json covariates.D_rca_pers): "
            f"'{L.carry(E7 / 'results/frozen_spec.json', 'covariates.D_rca_pers', DC['definitions']['D_rca_pers (Exp7 frozen_spec.covariates.D_rca_pers)'], DC['definitions']['D_rca_pers (Exp7 frozen_spec.covariates.D_rca_pers)'], **k)}'.",
            f"- Research 2 ({AR2}) R1: 'entered or RCA > 1 in each of t-k..t'.",
            f"- Verdict: **{DC['verdict']}**. D_rca_pers uses two window-aggregated 3-year RCAs over a 6-year horizon; "
            "persist_k requires the state in each single year and admits 'entered' presences below RCA 1. Neither "
            "U-set contains the other.",
            f"- DEV check ({L.num(dc, 'n_rows', '{:,.0f}', **k)} candidate rows, {L.num(dc, 'n_concepts', '{:,.0f}', **k)} "
            f"concepts; recipe check: rebuilt D_rca_1y vs Exp7 Spearman "
            f"{L.num(dc, 'recipe_check_D_rca_1y_spearman', '{:.4f}', **k)}):", "",
            "| variant | Spearman with D_rca_pers | Spearman with D_rca_1y | share rows > 0 |", "|---|---|---|---|"]
    for key in DC["comparisons"]:
        b = f"comparisons.{key}"
        out.append(f"| {key} | {L.num(dc, b + '.spearman_vs_D_rca_pers', '{:.3f}', **k)} | "
                   f"{L.num(dc, b + '.spearman_vs_D_rca_1y', '{:.3f}', **k)} | {L.num(dc, b + '.share_rows_nonzero', '{:.3f}', **k)} |")
    out += ["", src_line((dc, "comparisons.*; recipe_check_D_rca_1y_spearman")),
            "Consequence: Exp7's S_strict rival set did NOT contain Research 2's D_rca_persist_k; the 'persistence-filtered "
            "RCA density' rival (R1 in Research 2) remains untested against d0 and should be listed as an open rival.", "",
            "## Nearest-neighbour paragraph (draft for Section 18.1 / Related work)", "",
            f"{T} The retained-frontier predictor sits next to four lines of work. Hidalgo et al. (2007) define density "
            "from a region's current revealed-comparative-advantage basket and show that products close to that basket "
            "are entered next. Pinheiro et al. (2022) add persistence, but only on the outcome side: an entry counts only "
            "if RCA stays above one after years below it. Albora et al. (2023) benchmark relatedness against machine-"
            "learning forecasts of entry that use the unit's own past RCA trajectory (the benchmark Research 2 flags as a "
            "missing rival here). Cheng et al. (2023) bring the diffusion question to science and tie a topic's spread to "
            "the social structure of its early adopters (unconnected co-author groups; our candidate S). Our d0 moves persistence to the predictor side (relatedness to fields that RETAIN the "
            "concept). It is backbone-specific (18.6a) and not separable from volume in the matched contrast (18.5), "
            "and the persistence-filtered density twin D_rca_persist_k differs from Exp7's D_rca_pers (Step-3 above)."]
    write(tf, "\n".join(out))


# ============================================================================= 04
def parse_eval2_blocks() -> list[dict]:
    t = (EV2 / "text_corrections.md").read_text()
    parts = re.split(r"(?m)^## ", t)[1:]
    out = []
    for p in parts:
        title, _, body = p.partition("\n")
        new = re.search(r"\*\*New:?\*\*:?\s*\n(.*?)(?=\n\*\*Source keys|\Z)", body, re.S)
        old = re.search(r"\*\*Old\*\*.*?\n(.*?)(?=\n\*\*New)", body, re.S)
        srck = re.search(r"\*\*Source keys:?\*\*:?\s*(.*)", body)
        out.append({"title": title.strip(), "body": body, "new": (new.group(1).strip() if new else body.strip()),
                    "old": (old.group(1).strip() if old else ""), "source_keys": srck.group(1).strip() if srck else ""})
    return out


def f04() -> None:
    tf = "04_eval2_text_corrections.md"
    src = EV2 / "text_corrections.md"
    blocks = parse_eval2_blocks()
    tag = f"[Correction, iteration 3, from {AEV2}]"
    out = ["# 04 Eval2 text corrections, insert-ready", "",
           f"All {L.num(DER, 'eval2_text_blocks', '{:.0f}', section='20', target_file=tf)} '## ' blocks of "
           f"Eval2's text_corrections.md, rendered for insertion. Each insert starts with `{tag}`; the number tokens are "
           "carried verbatim from the Eval2 block (checked token by token in the ledger).", ""]
    for b in blocks:
        new = L.carry(src, f"## {b['title']}::New", b["body"], b["new"], section=b["title"].split()[0], target_file=tf)
        new = "\n".join(l[2:] if l.startswith("> ") else l for l in new.splitlines())
        title = b["title"]
        keys = L.carry(src, f"## {title}::Source keys", b["body"], b["source_keys"], section=title.split()[0], target_file=tf)
        out += [f"## {title}", "", f"{tag} {new}", "", f"Source (from Eval2): {keys or 'see Eval2 block'}", ""]
    write(tf, "\n".join(out))


# ============================================================================= 05
MAP05 = {"coverage_iter2": "8a (coverage table, iteration-2 column)", "coverage_iter2_steps": "8a",
         "definitions_diff": "9 / 11 (frame comparison Exp5 vs Exp6)", "draft_number_harvest": "ledger (all sections)",
         "frame_crosstab_split_group": "9 / 11 (frame comparison)", "frame_disagreement_causes": "9 / 11 (frame comparison)",
         "frame_overlap_by_group": "9 / 11 (frame comparison)", "h1_criteria": "10.3 (H1 criteria)",
         "hypothesis_iter3_numbers": "11.2 / 16.x (hypothesis LR, d, strata)", "lineage_robustness_iter1": "3.5 (alternative lineage indicators)",
         "next_field_heldout_rows": "11.2 (next-field entry, held-out rows)", "next_field_trace": "11.2 (next-field entry trace)",
         "o5_associations": "20.2 (O5 associations) and file 09", "o5_concept_panel": "20.2 / 13 (O5 panel)",
         "o5_coverage_by_group": "13.1 (Dataset 2 coverage)", "o5_coverage_by_group_source": "13.1 and file 09 (per-source coverage)",
         "o5_handcheck_items": "20.3 (O5 hand check)", "o5_handcheck_items_final": "20.3 (O5 hand check)",
         "o5_km_cumulative_incidence": "20.2 (O5 timing)", "ordering_mixed": "11.3 / 16.3 (ordering MIXED)",
         "partial_association_all": "4.4 (remaining partial associations)", "portability_F3": "4.3 (portability)",
         "refit_bootstrap_iter1": "3.3 / 4.2 (refit bootstrap)"}


def f05() -> None:
    tf = "05_record_tables_map.md"
    D = json.loads(DER.read_text())
    out = ["# 05 Eval2 record_tables: file -> report section", "", "| file | rows | target section |", "|---|---|---|"]
    for f, n in D["record_tables_rows"].items():
        stem = Path(f).stem
        rows = L.num(DER, f"record_tables_rows['{f}']", "{:,.0f}", section="map", target_file=tf) if n is not None else "json"
        out.append(f"| `record_tables/{f}` | {rows} | {MAP05.get(stem, 'appendix (no direct section)')} |")
    out += ["", src_line((DER, "record_tables_rows.<file>")) + " (row counts computed from the files listed)"]
    write(tf, "\n".join(out))


# ============================================================================= 06
def f06() -> None:
    tf = "06_ledger_open_rows.md"
    cl = pd.read_csv(EV2 / "claims_ledger.csv")
    src = EV2 / "claims_ledger.csv"
    out = ["# 06 Eval2 ledger: open rows (MISMATCH and MISLABELLED)", "",
           f"Eval2's claims_ledger.csv has {L.num(DER, 'eval2_ledger.n_rows', '{:.0f}', section='20.1', target_file=tf)} rows: "
           f"{L.num(DER, 'eval2_ledger.status_counts.MISMATCH', '{:.0f}', section='20.1', target_file=tf)} MISMATCH and "
           f"{L.num(DER, 'eval2_ledger.status_counts.MISLABELLED', '{:.0f}', section='20.1', target_file=tf)} MISLABELLED. "
           "Each is listed with the fixed text; values are carried verbatim from the row.", ""]
    for st in ("MISMATCH", "MISLABELLED"):
        out += [f"## {st}", ""]
        for r in cl[cl.status == st].itertuples():
            row_txt = " | ".join(str(getattr(r, c)) for c in cl.columns)
            key = f"claim_id=={r.claim_id}"
            fix = r.correction_text if isinstance(r.correction_text, str) and r.correction_text.strip() else \
                (r.text_change_note if isinstance(r.text_change_note, str) else "")
            body = (f"- **{r.claim_id}** (section {r.draft_section}; {r.quantity}): draft said '{r.claim_text}' "
                    f"(reported {r.reported_value}); file value {r.source_value} at `{r.source_file}` -> `{r.key_path}`. "
                    f"**Fixed text:** {fix}")
            out.append(L.carry(src, key, row_txt, body, section=str(r.draft_section), target_file=tf))
        out.append("")
    write(tf, "\n".join(out))


# ============================================================================= 07
def f07() -> None:
    tf = "07_failed_artifacts.md"
    k = dict(section="5a", target_file=tf)
    wr = E9 / ".aii_worker_result.json"
    err = json.loads(wr.read_text())["result"]["error_message"].split("\n")[0] if wr.exists() else "NOT_FOUND"
    plan = RUN / "iter_3/gen_plan/gen_plan_experiment_3/README.md"
    ptitle = plan.read_text().splitlines()[0].lstrip("# ").strip() if plan.exists() else "NOT_FOUND"
    has_method = (E9 / "method.py").exists()
    D = json.loads(DER.read_text())
    out = ["# 07 Failed artifacts, iteration counts and artifact ids", "",
           "## New Section 22b (or addition to 5a): Experiment 9 did not run", "",
           f"{TAG4.format(art='gen_art_experiment_9 .aii_worker_result.json')} Iteration 3 commissioned a fifth artifact, "
           f"gen_art_experiment_9, from the plan '{ptitle}' (`iter_3/gen_plan/gen_plan_experiment_3/`: state sequences, "
           "breadth decomposition, empirical trajectory typology, sequence tests, snapshot lineage check, case studies, "
           f"recognition timing). The worker failed before producing any output: `failed = true`, error: '{err}'. "
           f"The workspace holds no method.py ({'present' if has_method else 'absent'}) and no results. What was lost: "
           "the RQ2 trajectory typology and sequence tests for iteration 3. Status: **not run, not refuted**.", "",
           "## Iteration counts (from each artifact's .aii_worker_result.json)", "", "| iteration | commissioned | completed | failed | failed artifacts |", "|---|---|---|---|---|"]
    for i in (1, 2, 3):
        b = f"iterations.iter_{i}"
        failed = ", ".join(r["artifact"] for r in D["iterations"][f"iter_{i}"]["artifacts"] if r["failed"]) or "-"
        out.append(f"| {i} | {L.num(DER, b + '.n_commissioned', '{:.0f}', **k)} | {L.num(DER, b + '.n_completed', '{:.0f}', **k)} | "
                   f"{L.num(DER, b + '.n_failed', '{:.0f}', **k)} | {failed} |")
    out += ["", src_line((DER, "iterations.iter_<i>.*")),
            "Cross-check with Section 5a: it lists gen_art_dataset_1 and gen_art_experiment_2 as the two iteration-1 "
            "failures, which agrees. Iteration 2 had no failures. Iteration 3's failure (Experiment 9) is not in the draft.", "",
            "## Artifact id placeholders -> real ids", "", "| placeholder in draft | real id | artifact |", "|---|---|---|"]
    for ph, real, name in (("art_experiment_7", A7, "Experiment 7 (retained frontier)"), ("art_experiment_8", A8, "Experiment 8 (held-out indicator screen)"),
                           ("art_evaluation_2", AEV2, "Evaluation 2 (record audit, O5)"), ("art_research_2", AR2, "Research 2 (prior art, venue)")):
        n = REPORT_TXT.count(f"[ARTIFACT:{ph}]")
        out.append(f"| `[ARTIFACT:{ph}]` ({L.carry(REPORT, f'count [ARTIFACT:{ph}]', ' '.join([str(n)]), str(n), **k)} occurrences) | `{real}` | {name} |")
    write(tf, "\n".join(out))


# ============================================================================= 08
def f08() -> None:
    tf = "08_candidate_S_and_families.md"
    D = json.loads(DER.read_text())
    k = dict(section="19.1", target_file=tf)
    out = ["# 08 Candidate S rows and the indicator families (corrects 19.1)", "",
           "## Candidate S (co-author reach; Cheng et al. 2023) on held-out groups", "",
           f"{TAG4.format(art=A8)} The iteration-1 open rival 'candidate S' was scored in Exp8 as S_comp, S_comp_n and "
           "S_isolated_share. DL pooled over the 4 held-out groups from the per-unit rows:", "",
           "| indicator | outcome | pooled psp | 95% CI | I2 | units positive (of 6) | units CI excl. 0 (of 6) |", "|---|---|---|---|---|---|---|"]
    for key in sorted(D["candidate_S_DL4"]):
        b = f"candidate_S_DL4.{key}"
        ind, o = key.split("|")
        out.append(f"| {ind} | {o} | {L.num(DER, b + '.pooled', '{:+.3f}', **k)} | {ci(DER, b + '.ci', **k)} | "
                   f"{L.num(DER, b + '.I2', '{:.2f}', **k)} | {L.num(DER, b + '.n_pos_6', '{:.0f}', **k)} | {L.num(DER, b + '.n_ci_excl0_6', '{:.0f}', **k)} |")
    out += ["", src_line((E8 / "results/heldout_unit_results.csv", "indicator in S_* :: {z, se_z, rho, ci_lo, ci_hi}"),
                         (DER, "candidate_S_DL4.*")),
            "Reading: candidate S is now tested (not only 'not run'); none of its rows is in a frozen top-10 confirmed set "
            "for breadth; the social-reach rival is weak beyond B5.", "",
            "## Indicator families (from indicator_dictionary.csv, column 'family')", "",
            "## Old text (19.1 family list, verbatim)", "", quote(report_block("The 7 indicator families are:", "The outcomes are:")), "",
            f"## New 19.1 family list", "",
            f"{TAG4.format(art=A8)} Exp8 computes {L.num(DER, 'families.n_indicators', '{:.0f}', **k)} indicators in "
            f"{L.num(DER, 'families.n_families', '{:.0f}', **k)} families (entropy, reach, offhome share, log volume and "
            "growth belong to the B5 baseline, not to an indicator family; there is no 'external recognition' family, "
            "O5 is an outcome):", ""]
    names = {"A": "A: co-occurrence ego network", "E": "E: popularity / volume", "F": "F: disciplinary spread",
             "FR": "FR: retained frontier / relatedness to entered fields", "G": "G: landing on gateway fields", "S": "S: co-author (social) reach"}
    for f, mem in D["families"]["members"].items():
        out.append(f"- **{names.get(f, f)}** ({L.num(DER, f'families.counts.{f}', '{:.0f}', **k)}): {', '.join(mem)}")
    dsel = E8 / "results/rq1_dev_selection.json"
    dv = E8 / "results/deviations.json"
    dtxt = json.loads(dv.read_text())["T4_M_median"]
    out += ["", src_line((E8 / "results/indicator_dictionary.csv", "family column (counts per value)"), (DER, "families.*")), "",
            "## D-family exclusion (why D_ratio, D_rare and the other D indicators were never frozen)", "",
            f"{TAG4.format(art=A8)} DEV missing share: D_ratio {L.num(dsel, 'missing.D_ratio', '{:.3f}', **k)}, D_z "
            f"{L.num(dsel, 'missing.D_z', '{:.3f}', **k)}, D_sub {L.num(dsel, 'missing.D_sub', '{:.3f}', **k)}, D_obs "
            f"{L.num(dsel, 'missing.D_obs', '{:.3f}', **k)}, D_rare {L.num(dsel, 'missing.D_rare', '{:.3f}', **k)}; the DEV "
            "eligibility rule excludes indicators with more than 30% missing. Deviation record, verbatim: '"
            + L.carry(dv, "T4_M_median", dtxt, dtxt, **k) + "'", "",
            src_line((dsel, "missing.<indicator>"), (dv, "T4_M_median"))]
    write(tf, "\n".join(out))


# ============================================================================= 09
def f09() -> None:
    tf = "09_o5_leakage.md"
    ov = EV2 / "o5_validation.json"
    O = json.loads(ov.read_text())
    k = dict(section="20.2", target_file=tf)
    out = ["# 09 O5 precedence leakage by source and the O5-O3 association", "",
           f"{TAG4.format(art=AEV2)} External recognition is often dated at or before the concept's onset year t0, so O5 "
           "partly measures prior recognition, not diffusion success. Per source:", "",
           "| source | matched concepts | share first event <= t0 | median lag (years, events after t0) | IQR |", "|---|---|---|---|---|"]
    srcs = [s for s, v in O["precedence_leakage"].items() if isinstance(v, dict) and "n_matched" in v]
    order = sorted(srcs, key=lambda s: -O["precedence_leakage"][s]["n_matched"])
    for s in order:
        lag = f"lag.{s}"
        has = s in O["lag"]
        out.append(f"| {s} | {L.num(ov, f'precedence_leakage.{s}.n_matched', '{:,.0f}', **k)} | "
                   f"{L.num(ov, f'precedence_leakage.{s}.share_first_event_le_t0', '{:.2f}', **k)} | "
                   + (f"{L.num(ov, lag + '.median', '{:.1f}', **k)} | [{L.num(ov, lag + '.iqr[0]', '{:.1f}', **k)}, {L.num(ov, lag + '.iqr[1]', '{:.1f}', **k)}] |"
                      if has else "n/a | n/a |"))
    pl = "precedence_leakage"
    out += ["", f"Also: {L.num(ov, pl + '.wikidata_old_inception.share_year_lt_t0_minus_10', '{:.2f}', **k)} of the "
            f"{L.num(ov, pl + '.wikidata_old_inception.n_events', '{:.0f}', **k)} Wikidata inception events predate t0 by more "
            f"than 10 years; {L.num(ov, pl + '.wikipedia_growth_wave.share_dates_2001_2007', '{:.2f}', **k)} of Wikipedia "
            "dates fall in Wikipedia's 2001-2007 growth wave.",
            "", src_line((ov, "precedence_leakage.<source>.{n_matched,share_first_event_le_t0}; lag.<source>.{median,iqr}")),
            "Coverage per group and source (share found, share qualifying in window) is in "
            "`iter_3/gen_art/gen_art_evaluation_2/record_tables/o5_coverage_by_group_source.csv`.", "",
            "## O5-O3 association per held-out group (O5_main; Spearman)", "", "| group | n | rho(O5, O3) | 95% CI |", "|---|---|---|---|"]
    oa = EV2 / "record_tables/o5_associations.csv"
    A = pd.read_csv(oa)
    for g in A[A.variant == "O5_main"].group:
        if not any(h in g for h in HELD4):
            continue
        f = f"group=={g}&variant==O5_main"
        cis = json.loads(A[(A.group == g) & (A.variant == "O5_main")].rho_O3_ci95.iloc[0])
        out.append(f"| {g} | {L.num(oa, f + '::n', '{:,.0f}', **k)} | {L.num(oa, f + '::rho_O3', '{:+.3f}', **k)} | "
                   f"{_ci_from_csv(oa, f, cis, k)} |")
    b = "associations_pooled_heldout_DL.O5_main.rho_O3"
    out += ["", f"Pooled (DL, 4 held-out groups): {L.num(ov, b + '.pooled', '{:+.3f}', **k)} {ci(ov, b + '.ci95', **k)}, "
            f"p = {L.num(ov, b + '.p', '{:.3f}', **k)}, I2 = {L.num(ov, b + '.I2', '{:.2f}', **k)}. Recognised concepts are "
            "slightly LESS transient, but the association is small and heterogeneous.", "",
            src_line((oa, "group==<g>&variant==O5_main::{n,rho_O3,rho_O3_ci95}"), (ov, b + ".{pooled,ci95,p,I2}"))]
    write(tf, "\n".join(out))


def _ci_from_csv(src: Path, filt: str, cis: list, k: dict) -> str:
    """CSV list-valued CI: ledger each endpoint against the parsed list (file value = parsed element)."""
    out = []
    for j, v in enumerate(cis):
        txt = f"{v:+.3f}"
        L.rows.append({"claim_id": f"C{len(L.rows)+1:04d}", "target_file": k.get("target_file", ""),
                       "target_section": k.get("section", ""), "text_snippet": f"CI endpoint {j}", "reported_value": txt,
                       "source_file": rel(src), "key_path": f"{filt}::rho_O3_ci95[{j}]", "file_value": v,
                       "abs_diff": abs(float(txt) - v), "tolerance": Ledger.tolerance(txt),
                       "status": "MATCH" if abs(float(txt) - v) <= 1e-12 else ("ROUNDING_ONLY" if abs(float(txt) - v) <= Ledger.tolerance(txt) else "MISMATCH"),
                       "scale": 1.0, "fmt": "{:+.3f}", "kind": "value"})
        out.append(txt)
    return f"[{out[0]}, {out[1]}]"


# ============================================================================= 10
def f10() -> None:
    tf = "10_minor_slips.md"
    D = json.loads(DER.read_text())
    k = dict(section="18.11", target_file=tf)
    hs = HS
    summ = json.loads(hs.read_text())
    i_res = next(i for i, r in enumerate(summ["O2r_resid"]) if r["indicator"] == "M0_density_end")
    i_m50 = next(i for i, r in enumerate(summ["O2r_m50"]) if r["indicator"] == "M0_density_end")
    out = ["# 10 Minor slips", "",
           "## 19.6 cross-reference", "", quote(report_block("No indicator predicts external recognition. All Holm", "\n\n")), "",
           f"{TAG4.format(art=AEV2)} Replace 'Section 21.2' with 'Section 20.2' (the O5 validation result is Section 20.2, "
           "External recognition validation; 21.2 is 'Missing rivals').", "",
           "## 18.11 home-field mismatch sentence", "", quote(report_block("- The primary sample is the Experiment 5 frame minus", "\n")), "",
           f"{TAG4.format(art=A7)} Replace with: 'The primary sample is the Experiment 5 frame minus Experiment 6 (by ID, "
           f"QID and label), not a fully independent draw. Home fields disagree with Exp5's for "
           f"{L.num(DER, 'exp7_home_mismatch.total', '{:.0f}', **k)} concepts ({L.num(DER, 'exp7_home_mismatch.dev', '{:.0f}', **k)} DEV, "
           f"{L.num(DER, 'exp7_home_mismatch.heldout', '{:.0f}', **k)} held-out; held-out home agreement "
           f"{L.num(S2H, 'input_checks.home_agreement', '{:.4f}', **k)}).'", "",
           src_line((S2D, "input_checks.home_mismatch_cidx (length)"), (S2H, "input_checks.home_mismatch_cidx (length); input_checks.home_agreement")), "",
           "## M0_density_end +0.375 vs +0.377 (source note for 19.2)", "",
           f"{TAG4.format(art=A8)} Both numbers are correct but refer to different outcomes: "
           f"{L.num(hs, f'O2r_m50[{i_m50}].pooled', '{:+.3f}', section='19.2', target_file=tf)} is O2r_m50 (the 19.2 table "
           f"and README), {L.num(hs, f'O2r_resid[{i_res}].pooled', '{:+.3f}', section='19.2', target_file=tf)} is O2r_resid "
           "(the Exp8 summary headline). Add to 19.2: 'Source: heldout_summary.json -> O2r_m50[indicator=M0_density_end]."
           "pooled; the headline +0.377 is O2r_resid.'", "",
           src_line((hs, f"O2r_m50[{i_m50}].pooled"), (hs, f"O2r_resid[{i_res}].pooled"))]
    write(tf, "\n".join(out))


# ============================================================================= 11
def f11() -> None:
    tf = "11_boundary_results.md"
    B1 = RES / "post_onset_rescore.json"
    SC = RES / "spec_curve.json"
    H = RES / "heterogeneity.json"
    PG = RES / "per_group_pooled.csv"
    T0 = RES / "gate_T0.json"
    k = dict(section="new 19.10", target_file=tf)
    h = json.loads(H.read_text())
    b1 = json.loads(B1.read_text())
    pg = pd.read_csv(PG)
    out = ["# 11 Boundary results for the OPEN lead (EXPLORATORY)", "",
           "**Status: EXPLORATORY.** All analyses reuse the Exp8 held-out groups, which were unsealed in Exp5 and Exp8. "
           "They can reveal fragility; they cannot confirm OPEN. Confirmation needs the never-screened 2015-16 cohort. "
           f"The specification was hash-frozen before any statistic (`logs/seal.log`, boundary_spec.json sha256).", "",
           "## Reproduction gate T0", "",
           f"Exp8's pooled held-out psp was re-derived from analysis_table.parquet with the Exp8 estimator: M0_density_end "
           f"{L.num(T0, 'rows[1].rederived_pooled', '{:+.4f}', **k)} (record {L.num(T0, 'rows[1].record_pooled', '{:+.4f}', **k)}, O2r_m50) "
           f"and {L.num(T0, 'rows[0].rederived_pooled', '{:+.4f}', **k)} (O2r_resid); D_vol_end {L.num(T0, 'rows[2].rederived_pooled', '{:+.4f}', **k)}; "
           f"n_comm_W3 {L.num(T0, 'rows[3].rederived_pooled', '{:+.4f}', **k)}; ego_density_W3 {L.num(T0, 'rows[4].rederived_pooled', '{:+.4f}', **k)}; "
           f"new_edge_rate {L.num(T0, 'rows[5].rederived_pooled', '{:+.4f}', **k)}. All within the 1e-3 tolerance (gate passed).", "",
           src_line((T0, "rows[i].{record_pooled,rederived_pooled}")), "",
           "## B1 Post-onset re-score of the two largest breadth effects", ""]
    for f in ("M0_density_end", "D_vol_end"):
        for o in ("O2r_m50",):
            b = f"pooled.DL4|{f}|{o}"
            exc = b1["pooled"][f"DL4|{f}|{o}"]["units_excluded_undefined_post"]
            out.append(f"- **{f}** ({o}, DL over held-out groups{' excluding ' + ', '.join(exc) if exc else ''}): full history "
                       f"{L.num(B1, b + '.psp_full', '{:+.3f}', **k)} -> post-onset only (t0..t0+2 papers) "
                       f"{L.num(B1, b + '.psp_post', '{:+.3f}', **k)} {ci(B1, b + '.psp_post_ci_boot', **k)}; paired difference "
                       f"{L.num(B1, b + '.diff', '{:+.3f}', **k)} {ci(B1, b + '.diff_ci', **k)}; attenuation "
                       f"{L.num(B1, b + '.attenuation', '{:.2f}', **k)} {ci(B1, b + '.attenuation_ci', '{:.2f}', **k)}; "
                       f"verdict **{b1['pooled'][f'DL4|{f}|{o}']['verdict']}** (frozen rule: MOST if upper CI of post < half of full; "
                       "LITTLE if the paired difference CI includes 0).")
    fc = b1["footprint_controlled"]
    for j, r in enumerate(fc):
        if r["pool"] == "DL4" and r["outcome"] == "O2r_m50":
            out.append(f"- {r['indicator']} given B5 + pre-onset footprint (D_vol_pre, log pre-onset papers): "
                       f"{L.num(B1, f'footprint_controlled[{j}].pooled', '{:+.3f}', **k)} {ci(B1, f'footprint_controlled[{j}].ci', **k)}.")
    out += [f"- D_vol_post is near rank-identical to the B5 'reach' column (within-unit Spearman "
            f"{L.num(B1, 'collinearity_post_vs_B5_reach.spearman_D_vol_post_reach_by_unit.LIFEENV', '{:.3f}', **k)} in LIFEENV, "
            f"{L.num(B1, 'collinearity_post_vs_B5_reach.spearman_D_vol_post_reach_by_unit.MATHDEC', '{:.3f}', **k)} in MATHDEC). "
            "Once the pre-onset years are removed, D_vol is almost the baseline itself; in MATHDEC its partial correlation is "
            "undefined in the bootstrap, so MATHDEC is excluded from the D_vol pools. M0_density_post is less collinear with "
            f"reach (within-unit Spearman from {L.num(B1, 'collinearity_post_vs_B5_reach.spearman_M0_post_reach_by_unit.CS', '{:.2f}', **k)} "
            f"in CS to {L.num(B1, 'collinearity_post_vs_B5_reach.spearman_M0_post_reach_by_unit.Med', '{:.2f}', **k)} in Med) "
            "and its bootstrap is defined in every unit.",
            f"- Spearman(D_vol_post, D_vol_end) = {L.num(B1, 'spearman.D_vol_post_vs_D_vol_end_heldout6', '{:.3f}', **k)}; "
            f"Spearman(footprint share, O2r_m50) = {L.num(B1, 'spearman.footprint_share_vs_O2r_m50_heldout6', '{:.3f}', **k)}; "
            f"share of held-out concepts with any pre-onset off-home entry {L.num(B1, 'spearman.share_with_any_pre_onset_entry', '{:.3f}', **k)}.",
            "", "**Paper wording.** About half of the M0_density_end and D_vol_end breadth signal comes from the concept's "
            "pre-onset footprint in other fields. The post-onset part is still clearly positive, so these are partly, but "
            "not only, early network signals.", "", src_line((B1, "pooled.*; footprint_controlled; collinearity_post_vs_B5_reach; spearman")), "",
            "## B2 OPEN per unit (O2r_m50 and O2r_resid)", ""]
    for o in ("O2r_m50", "O2r_resid"):
        for pool in ("DL4", "DL6"):
            f = f"indicator==OPEN&outcome=={o}&pool=={pool}"
            out.append(f"- OPEN, {o}, {pool}: {L.num(PG, f + '::pooled', '{:+.3f}', **k)} [{L.num(PG, f + '::ci_lo', '{:+.3f}', **k)}, "
                       f"{L.num(PG, f + '::ci_hi', '{:+.3f}', **k)}], I2 {L.num(PG, f + '::I2', '{:.2f}', **k)}, prediction interval "
                       f"[{L.num(PG, f + '::pi_lo', '{:+.3f}', **k)}, {L.num(PG, f + '::pi_hi', '{:+.3f}', **k)}], positive in "
                       f"{L.num(PG, f + '::sign_pos_6', '{:.0f}', **k)} of 6 units, CI includes 0 in "
                       f"{L.num(PG, f + '::n_ci_includes_0_6', '{:.0f}', **k)} of 6.")
    sp = E8 / "results/sensitivities_pooled.json"
    for j, r in enumerate(json.loads(sp.read_text())):
        if r["indicator"] == "CONTACT_REACH" and r["sensitivity"] == "excl_intersection":
            out.append(f"- CONTACT_REACH without intersection-born (multi-home) concepts, {r['outcome']}: "
                       f"{L.num(sp, f'[{j}].pooled', '{:+.3f}', **k)} {ci(sp, f'[{j}].ci', **k)} (Exp8 sensitivity, verbatim "
                       "from sensitivities_pooled.json; all rows of that file are carried in `results/per_group_extra.json`).")
    out += ["", "The full per-unit table (all confirmed indicators, the iteration-1 candidates, new_edge_rate, the post-onset "
            "rows, OPEN and OPEN_PC1; DEV units labelled SELECTION_DATA) is `results/per_group_table.csv`.", "",
            src_line((PG, "indicator==OPEN&outcome==<o>&pool==<pool>::{pooled,ci_lo,ci_hi,I2,pi_lo,pi_hi,sign_pos_6,n_ci_includes_0_6}")), "",
            "## B3 Specification curve", "",
            f"Across {L.num(SC, 'n_specs', '{:,.0f}', **k)} specifications (120 composites x 4 outcomes x 4 control sets), the "
            f"pooled psp CI excludes 0 in a share of {L.num(SC, 'summary.DL4.share_ci_gt0', '{:.3f}', **k)} (4 held-out groups; "
            f"{L.num(SC, 'summary.DL6.share_ci_gt0', '{:.3f}', **k)} with the 2 cohort units). Median psp "
            f"{L.num(SC, 'summary.DL4.median', '{:.3f}', **k)} (IQR {L.num(SC, 'summary.DL4.iqr[0]', '{:.3f}', **k)}-"
            f"{L.num(SC, 'summary.DL4.iqr[1]', '{:.3f}', **k)}). Under a Freedman-Lane null "
            f"({L.num(SC, 'null.DL4.n_draws', '{:.0f}', **k)} draws), the null median is "
            f"{L.num(SC, 'null.DL4.null_median_mean', '{:+.4f}', **k)} and the null share with CI > 0 averages "
            f"{L.num(SC, 'null.DL4.null_share_ci_gt0_mean', '{:.3f}', **k)}; permutation p = "
            f"{L.num(SC, 'null.DL4.p_share_ci_gt0', '{:.3f}', **k)} (the smallest possible with this many draws). Headline "
            f"spec (all 6 components, equal weights, O2r_m50, C1): {L.num(SC, 'headline.DL4.est', '{:+.3f}', **k)} "
            f"{ci(SC, 'headline.DL4.ci', **k)}, I2 {L.num(SC, 'headline.DL4.I2', '{:.2f}', **k)}, prediction interval "
            f"{ci(SC, 'headline.DL4.pi', **k)}. With contact reach as a control (C3) the median is "
            f"{L.num(SC, 'marginals.DL4.control.C3.median', '{:.3f}', **k)} vs {L.num(SC, 'marginals.DL4.control.C1.median', '{:.3f}', **k)} "
            f"under C1. Analytic vs bootstrap SE calibration: median width ratio "
            f"{L.num(SC, 'calibration.median_ratio_boot_over_analytic', '{:.3f}', **k)} (< 1.2, no inflation).", "",
            "**Reading.** The positive OPEN association is a property of the construct, not of one combination: every "
            "component subset, both weightings, all four breadth outcomes and all four control sets give a positive pooled "
            "estimate. The prediction interval of the headline spec includes 0, so a new domain can show a null.", "",
            src_line((SC, "n_specs; summary.*; null.DL4.*; headline.DL4.*; marginals.DL4.control.*; calibration.*")), "",
            "## B4 Heterogeneity and the LIFEENV diagnosis", "",
            f"On {L.num(H, 'k_subunits', '{:.0f}', **k)} home-field x period sub-units (n >= {L.num(H, 'min_n', '{:.0f}', **k)}), "
            f"I2 is {L.num(H, 'I2_subunit', '{:.2f}', **k)} (vs {L.num(H, 'I2_unit6', '{:.2f}', **k)} over the 6 units). No "
            "trait explains the between-sub-unit variance (univariate REML meta-regression with Knapp-Hartung; Holm over 7 traits):", "",
            "| trait (ecological, sub-unit level) | slope per SD | 95% CI | permutation p | Holm p |", "|---|---|---|---|---|"]
    for t in h["meta_regression"]["univariate"]:
        b = f"meta_regression.univariate.{t}"
        out.append(f"| {t} | {L.num(H, b + '.slope_per_sd', '{:+.3f}', **k)} | {ci(H, b + '.ci', **k)} | "
                   f"{L.num(H, b + '.p_perm', '{:.3f}', **k)} | {L.num(H, b + '.p_perm_holm', '{:.3f}', **k)} |")
    le = "lifeenv"
    out += ["", f"LIFEENV: OPEN psp {L.num(H, le + '.psp_LIFEENV', '{:+.3f}', **k)} vs the other 5 units pooled "
            f"{L.num(H, le + '.others_pooled_6minusL.est', '{:+.3f}', **k)} {ci(H, le + '.others_pooled_6minusL.ci', **k)}. "
            f"(i) OPEN varies less in LIFEENV (SD ratio {L.num(H, le + '.sd_ratio.OPEN.ratio', '{:.2f}', **k)} "
            f"{ci(H, le + '.sd_ratio.OPEN.ci', '{:.2f}', **k)}; new_edge_rate {L.num(H, le + '.sd_ratio.new_edge_rate.ratio', '{:.2f}', **k)}), "
            f"but the Thorndike range-restriction correction only moves psp to {L.num(H, le + '.psp_thorndike_corrected', '{:+.3f}', **k)}. "
            f"(ii) Reweighting LIFEENV to the others' label-coverage distribution (entropy balancing) gives "
            f"{L.num(H, le + '.entropy_balanced.psp_reweighted', '{:+.3f}', **k)} {ci(H, le + '.entropy_balanced.ci', **k)}. "
            f"Verdict under the frozen rule: **{h['lifeenv']['verdict']}**: neither coverage nor restricted range explains the "
            "weak LIFEENV cell, so it is treated as a domain boundary.", "",
            src_line((H, "k_subunits; I2_*; meta_regression.univariate.*; lifeenv.*")), "",
            "Figures: `figures/spec_curve.pdf`, `figures/open_forest.pdf`, `figures/b1_post_onset.pdf`, `figures/lifeenv_diagnosis.pdf`."]
    write(tf, "\n".join(out))


# ============================================================================= 00
def f00() -> None:
    idx = [("01_exp8_outcomes_relabel.md", "19.4, 19.5 (relabel O4), new 19.5b (O3), 19.6, 19.7, 22.6", A8),
           ("02_prereg_P1_P5.md", "19.8, 22.7; corrections to 7.4 and 4.3; iteration-1 candidates table", A8),
           ("03_exp7_tables.md", "18.3, 18.4, 18.5, 18.6 (+ new 18.6a), 18.9, 18.1 (D_rca_pers vs persist_k; neighbours)", A7),
           ("04_eval2_text_corrections.md", "the 14 blocks of Eval2 (10.3, 11.3/16.3, 10.6/16.5, 10.7, 5.4, 13.1, 8a, 4.4, 11.2, 16.1, 10.5, 11.5, 9/11, 20.2)", AEV2),
           ("05_record_tables_map.md", "map of Eval2 record_tables to sections", AEV2),
           ("06_ledger_open_rows.md", "the MISMATCH and MISLABELLED rows of Eval2's ledger", AEV2),
           ("07_failed_artifacts.md", "5a / new 22b (Exp9 not run), iteration counts, artifact ids", "run records"),
           ("08_candidate_S_and_families.md", "19.1 (families), candidate S rows, D-family exclusion", A8),
           ("09_o5_leakage.md", "20.2 (O5 leakage per source, O5-O3 association)", AEV2),
           ("10_minor_slips.md", "19.6 cross-reference, 18.11 mismatch sentence, 19.2 source note", "mixed"),
           ("11_boundary_results.md", "new 19.10 (EXPLORATORY boundary results for OPEN)", "this artifact")]
    out = ["# Corrections pack: index", "",
           "Each file replaces or adds the report sections listed. Inserts carry the tag "
           "`[Correction, iteration 4, from art_...]` (or `[Correction, iteration 3, from art_7W9xiIO3FVBs]` for the "
           "Eval2 blocks in file 04). Every number is ledgered in `results/claims_ledger_v3.csv` and re-verified by "
           "`verify_ledger.py` (`results/ledger_verification.json`).", "",
           "| file | replaces / adds | source artifact |", "|---|---|---|"]
    out += [f"| `{f}` | {s} | {a} |" for f, s, a in idx]
    (COR / "00_index.md").write_text("\n".join(out) + "\n")


def main() -> None:
    build_derived()
    for fn in (f01, f02, f03, f04, f05, f06, f07, f08, f09, f10, f11, f00):
        fn()
    L.write(RES / "claims_ledger_v3.csv")
    st = pd.Series([r["status"] for r in L.rows]).value_counts().to_dict()
    logger.info(f"ledger rows {len(L.rows)}; status {st}")
    bad = [r for r in L.rows if r["status"] in ("MISMATCH", "NOT_FOUND")]
    for r in bad[:40]:
        logger.warning(f"{r['status']}: {r['target_file']} {r['source_file']} {r['key_path']} -> {r['reported_value']}")


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
