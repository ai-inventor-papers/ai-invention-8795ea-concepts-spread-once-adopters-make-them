#!/usr/bin/env python3
"""Item 5 + assembly: apply Eval3's corrections pack (00-11) and then the iteration-5 blocks to a COPY of
iter_5/gen_strat/current_report.md -> report_corrected.md. Writes results/corrections_applied.csv and
corrections_iter5/05_eval3_application.md, and replaces Section 27.6 by the per-file applied list.

Actions: replace-section, append-to-section, insert-new-section-after (all keyed by a heading regex),
text-replace / text-replace-all / text-prefix / text-append-line (keyed by an exact string).
Before inserting a block, its tag-free first sentence is searched in the current report text; if found, the block is
ALREADY_PRESENT and is not duplicated. Usage: python src/apply_corrections.py"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from loguru import logger

from paths import COR, EVAL3, LOGS, REPORT5, RES, WS

NUM_RE = r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:e[-+]?\d+)?(?![\w])"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "apply_corrections.log", rotation="30 MB", level="DEBUG")

E3C = EVAL3 / "corrections"
# (file, block-title prefix, target heading regex, action, new heading for replace/insert or None)
# Derived from Eval3 corrections/00_index.md ('replaces / adds' column).
EVAL3_MAP = [
    ("01_exp8_outcomes_relabel.md", "New 19.4", r"^### 19\.4 ", "replace-section", "### 19.4 O1c (sustained uptake)"),
    ("01_exp8_outcomes_relabel.md", "New 19.5 ", r"^### 19\.5 ", "replace-section",
     "### 19.5 O4 (field- and year-normalised citation growth): 2 of 10 confirmed"),
    ("01_exp8_outcomes_relabel.md", "New 19.5b", r"^### 19\.5b ", "replace-section", "### 19.5b O3 (transience): 1 of 10 confirmed"),
    ("01_exp8_outcomes_relabel.md", "New 19.6", r"^### 19\.6 ", "replace-section",
     "### 19.6 External recognition (O5, O5_WW): 0 and 0 of 10 confirmed"),
    ("01_exp8_outcomes_relabel.md", "New 19.7", r"^### 19\.7 ", "replace-section",
     "### 19.7 Learned models vs B5 vs B5 + best single (heldout groups pooled)"),
    ("01_exp8_outcomes_relabel.md", "O3 as a positive", r"^### 19\.5b ", "append-to-section", None),
    ("01_exp8_outcomes_relabel.md", "New dead end 22.6", r"^## 22\. ", "append-to-section", None),
    ("02_prereg_P1_P5.md", "New 19.8", r"^### 19\.8 ", "replace-section", "### 19.8 Preregistered verdicts"),
    ("02_prereg_P1_P5.md", "Correction to dead end 7.4", r"^## 7\. ", "append-to-section", None),
    ("02_prereg_P1_P5.md", "Correction to Section 4.3", r"^### 4\.3 ", "append-to-section", None),
    ("02_prereg_P1_P5.md", "New dead end 22.7", r"^## 22\. ", "append-to-section", None),
    ("02_prereg_P1_P5.md", "Held-out table: iteration-1", r"^### 19\.8 ", "append-to-section", None),
    ("03_exp7_tables.md", "18.5 ", r"^### 18\.5 ", "append-to-section", None),
    ("03_exp7_tables.md", "18.4 ", r"^### 18\.4 ", "append-to-section", None),
    ("03_exp7_tables.md", "18.9 ", r"^### 18\.9 ", "append-to-section", None),
    ("03_exp7_tables.md", "18.3 ", r"^### 18\.3 ", "append-to-section", None),
    ("03_exp7_tables.md", "18.6 ", r"^### 18\.6 ", "append-to-section", None),
    ("03_exp7_tables.md", "New subsection 18.6a", r"^### 18\.6 ", "insert-new-section-after", "### 18.6a Proximity dependence"),
    ("03_exp7_tables.md", "Step-3 comparison", r"^### 18\.1 ", "append-to-section", None),
    ("03_exp7_tables.md", "Nearest-neighbour paragraph", r"^### 18\.1 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "10.3 ", r"^### 10\.3 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "11.3 / 16.3", r"^### 11\.3 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "10.6 / 16.5", r"^### 10\.6 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "10.7 ", r"^### 10\.7 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "5.4 ", r"^### 5\.4 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "13.1 ", r"^### 13\.1 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "8a ", r"^## 8a\. ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "4.4 ", r"^### 4\.4 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "11.2 ", r"^### 11\.2 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "16.1 ", r"^## 16\. ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "10.5 ", r"^### 10\.5 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "11.5 ", r"^### 11\.5 ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "New: frame comparison", r"^## 9\. ", "append-to-section", None),
    ("04_eval2_text_corrections.md", "New: O5 external", r"^### 13\.2 ", "append-to-section", None),
    ("05_record_tables_map.md", "", r"^### 20\.1 ", "append-to-section", None),
    ("06_ledger_open_rows.md", "", r"^### 20\.1 ", "append-to-section", None),
    ("07_failed_artifacts.md", "New Section 22b", r"^## 22a\. ", "insert-new-section-after",
     "## 22b. Failed artifact of iteration 3: Experiment 9 did not run"),
    ("07_failed_artifacts.md", "Iteration counts", r"^## 24\. ", "append-to-section", None),
    ("07_failed_artifacts.md", "Artifact id placeholders", r"^## 24\. ", "append-to-section", None),
    ("08_candidate_S_and_families.md", "Candidate S", r"^### 19\.1 ", "append-to-section", None),
    ("08_candidate_S_and_families.md", "New 19.1 family list", r"^### 19\.1 ", "append-to-section", None),
    ("08_candidate_S_and_families.md", "D-family exclusion", r"^### 19\.1 ", "append-to-section", None),
    ("09_o5_leakage.md", "", r"^### 20\.2 ", "append-to-section", None),
    ("10_minor_slips.md", "19.6 cross-reference", r"^### 19\.6 ", "append-to-section", None),
    ("10_minor_slips.md", "18.11 ", r"^### 18\.11 ", "append-to-section", None),
    ("10_minor_slips.md", "M0_density_end +0.375", r"^### 19\.2 ", "append-to-section", None),
    ("11_boundary_results.md", "", r"^### 19\.9 ", "insert-new-section-after",
     "### 19.10 Boundary results for the OPEN lead (EXPLORATORY; Evaluation 3)"),
]


# ----------------------------------------------------------------------------- parsing
def md_blocks(text: str) -> list[tuple[str, str]]:
    """[(title, body)] for '## ' blocks; a file with no '## ' blocks (or its preamble) gives ('', ...)."""
    out, title, buf = [], "", []
    for ln in text.splitlines():
        if ln.startswith("## "):
            out.append((title, "\n".join(buf).strip()))
            title, buf = ln[3:].strip(), []
        elif ln.startswith("# ") and not out and not buf:
            continue
        else:
            buf.append(ln)
    out.append((title, "\n".join(buf).strip()))
    return [(t, b) for t, b in out if b]


def heading_level(ln: str) -> int:
    m = re.match(r"^(#{1,6}) ", ln)
    return len(m.group(1)) if m else 0


def find_section(lines: list[str], rx: str) -> tuple[int, int] | None:
    r = re.compile(rx)
    for i, ln in enumerate(lines):
        if r.search(ln) and heading_level(ln):
            lv = heading_level(ln)
            j = i + 1
            while j < len(lines) and not (heading_level(lines[j]) and heading_level(lines[j]) <= lv):
                j += 1
            return i, j
    return None


def first_sentence(body: str) -> str:
    for ln in body.splitlines():
        s = re.sub(r"\[Correction, iteration [^\]]*\]", "", ln).strip().lstrip(">*- ").strip()
        if len(s) >= 40 and not s.startswith("|") and not s.startswith("Source:"):
            return s[:90]
    return ""


class Report:
    def __init__(self, text: str):
        self.lines = text.splitlines()

    @property
    def text(self) -> str:
        return "\n".join(self.lines) + "\n"

    def apply(self, target: str, action: str, block: str, new_heading: str | None) -> tuple[str, str, int]:
        """-> (status, reason, 1-based line of the inserted text or -1)."""
        blines = block.rstrip("\n").splitlines()
        if action.startswith("text-"):
            t = self.text
            n = t.count(target)
            if n == 0:
                return "NOT_APPLIED_TARGET_MISSING", f"string not found: {target[:60]}", -1
            if action == "text-replace":
                t = t.replace(target, block, 1)
            elif action == "text-replace-all":
                t = t.replace(target, block)
            elif action == "text-prefix":
                t = t.replace(target, block + re.sub(r"^\d+\.\s+", "", target), 1)   # keep one list number
            elif action == "text-append-line":
                i = t.index(target)
                e = t.find("\n", i)
                t = t[:e] + block + t[e:]
            self.lines = t.rstrip("\n").splitlines()
            ln = next((k + 1 for k, s in enumerate(self.lines) if block.strip()[:40] in s), -1)
            return "APPLIED", f"{action} ({n} occurrence(s))", ln
        sec = find_section(self.lines, target)
        if sec is None:
            return "NOT_APPLIED_TARGET_MISSING", f"heading not found: {target}", -1
        i, j = sec
        if action == "replace-section":
            if new_heading and not blines[0].startswith("#"):
                blines = [new_heading, ""] + blines
            self.lines[i:j] = blines + [""]
            return "APPLIED", "section replaced", i + 1
        if action == "append-to-section":
            while j > i + 1 and not self.lines[j - 1].strip():
                j -= 1
            self.lines[j:j] = [""] + blines + [""]
            return "APPLIED", "appended at end of section", j + 2
        if action == "insert-new-section-after":
            if new_heading and not blines[0].startswith("#"):
                blines = [new_heading, ""] + blines
            self.lines[j:j] = blines + ["", ""]
            return "APPLIED", "new section inserted after target section", j + 1
        raise ValueError(action)


@logger.catch(reraise=True)
def main() -> None:
    rep = Report(REPORT5.read_text())
    original = REPORT5.read_text()
    rows: list[dict] = []
    # ---------------- Eval3 blocks
    used = set()
    for fn, pref, rx, act, nh in EVAL3_MAP:
        blocks = md_blocks((E3C / fn).read_text())
        cand = [(t, b) for t, b in blocks if (t.startswith(pref) if pref else True) and not t.startswith("Old text")]
        if not pref:
            body = "\n\n".join((f"**{t}**\n\n{b}" if t else b) for t, b in blocks if not t.startswith("Old text"))
            title = f"(whole file) {fn}"
            header = (E3C / fn).read_text().splitlines()[0].lstrip("# ").strip()
            body = f"**{header}**\n\n{body}"
            if nh is None:
                pass
        else:
            if not cand:
                rows.append({"source_file": fn, "block_id": pref, "target_section": rx, "action": act,
                             "status": "NOT_APPLIED_TARGET_MISSING", "reason": "block title not found in file",
                             "line_in_corrected": -1})
                continue
            title, body = cand[0]
        used.add((fn, title))
        fs = first_sentence(body)
        toks = re.findall(NUM_RE, re.sub(r"`[^`]*`", " ", body))
        share = (sum(bool(re.search(r"(?<![\w.])" + re.escape(t) + r"(?![\w])", original)) for t in toks) / len(toks)
                 if toks else 1.0)
        if fs and fs in original and share < 0.9:
            act, rx = "append-to-section", rx
            body = ("[Correction, iteration 5, from this evaluation] The Evaluation 3 block below was only partly applied "
                    f"in the iteration-5 report ({share:.0%} of its numbers present); it is appended in full.\n\n" + body)
        elif fs and fs in original:
            rows.append({"source_file": fn, "block_id": title, "target_section": rx, "action": act,
                         "status": "ALREADY_PRESENT", "reason": f"first sentence already in iter-5 report: '{fs[:50]}'",
                         "line_in_corrected": -1})
            continue
        if act == "replace-section" and nh:
            body = f"{nh}\n\n{body}"
        if act == "append-to-section" and nh and body.startswith("[Correction, iteration 5"):
            nh = None
        st, why, ln = rep.apply(rx, act, body, nh)
        rows.append({"source_file": fn, "block_id": title, "target_section": rx, "action": act, "status": st,
                     "reason": why, "line_in_corrected": ln})
    # Old-text quotes (reference only)
    for f in sorted(E3C.glob("[01]*.md")):
        if f.name == "00_index.md":
            continue
        for t, _ in md_blocks(f.read_text()):
            if t.startswith("Old text"):
                rows.append({"source_file": f.name, "block_id": t, "target_section": "-", "action": "none",
                             "status": "NOT_APPLIED_SUPERSEDED", "reason": "verbatim quote of the old draft text, "
                             "kept in Eval3 file as evidence; the matching 'New' block is applied instead",
                             "line_in_corrected": -1})
    # ---------------- iteration-5 blocks
    plan = json.loads((RES / "apply_plan_iter5.json").read_text())
    for p in plan:
        body = p["text"]
        if p["action"] in ("append-to-section", "insert-new-section-after"):   # replacements are intended
            fs = first_sentence(body)
            if fs and fs in rep.text and "[Correction, iteration 5" not in fs:
                rows.append({"source_file": p["source_file"], "block_id": p["block_id"], "target_section": p["target"],
                             "action": p["action"], "status": "ALREADY_PRESENT", "reason": "first sentence present",
                             "line_in_corrected": -1})
                continue
        st, why, ln = rep.apply(p["target"], p["action"], body, p.get("new_heading"))
        rows.append({"source_file": p["source_file"], "block_id": p["block_id"], "target_section": p["target"][:80],
                     "action": p["action"], "status": st, "reason": why + (f"; {p['note']}" if p.get("note") else ""),
                     "line_in_corrected": ln})
    # ---------------- 27.6 = the applied list, rendered per file
    per = {}
    for r in rows:
        per.setdefault(r["source_file"], []).append(r)
    lines = ["### 27.6 Corrections applied", "",
             "[Correction, iteration 5, from this evaluation] The previous text claimed that all Evaluation 3 "
             "corrections had been applied in place; most had not. This list is generated by "
             "`src/apply_corrections.py` from `results/corrections_applied.csv` and records, per correction file, what "
             "happened to each block in this corrected report.", "",
             "| correction file | blocks | APPLIED | ALREADY_PRESENT | NOT_APPLIED (target missing) | "
             "NOT_APPLIED (superseded old-text quote) |", "|---|---|---|---|---|---|"]
    for fn in sorted(per):
        rs = per[fn]
        c = lambda s: sum(r["status"] == s for r in rs)  # noqa: E731
        lines.append(f"| `{fn}` | {len(rs)} | {c('APPLIED')} | {c('ALREADY_PRESENT')} | "
                     f"{c('NOT_APPLIED_TARGET_MISSING')} | {c('NOT_APPLIED_SUPERSEDED')} |")
    lines.append("")
    lines.append("Evaluation 3 Step 3 is recorded: D_rca_persist_k rival untested; Exp7 D_rca_pers is a different "
                 "construct (max rho 0.877, drca_persist_comparison.json).")
    st, why, ln = rep.apply(r"^### 27\.6 ", "replace-section", "\n".join(lines), None)
    rows.append({"source_file": "05_eval3_application.md", "block_id": "27.6_list", "target_section": r"^### 27\.6 ",
                 "action": "replace-section", "status": st, "reason": why, "line_in_corrected": ln})
    # line numbers of APPLIED blocks in the final text (positions shift after later inserts)
    final = rep.lines
    for r in rows:
        if r["status"] == "APPLIED" and r["block_id"]:
            key = r["block_id"]
            m = re.match(r"(New subsection |New Section |New dead end |New )?(\d+\.\d+[a-z]?|\d+[a-z]?)", key)
            r["line_in_corrected_final"] = next((k + 1 for k, s in enumerate(final)
                                                 if heading_level(s) and m and f" {m.group(2)}" in s), r["line_in_corrected"])
        else:
            r["line_in_corrected_final"] = r["line_in_corrected"]
    (WS / "report_corrected.md").write_text(rep.text)
    with open(RES / "corrections_applied.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["source_file", "block_id", "target_section", "action", "status", "reason",
                                          "line_in_corrected", "line_in_corrected_final"])
        w.writeheader()
        w.writerows(rows)
    md = ["# 05 Evaluation 3 corrections pack: application record", "",
          "Mapping (file, block, target heading, action) is the explicit list `EVAL3_MAP` in `src/apply_corrections.py`,"
          " derived from Eval3 `corrections/00_index.md`. Status per block:", "",
          "| source file | block | target | action | status | reason |", "|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| `{r['source_file']}` | `{r['block_id']}` | `{r['target_section']}` | {r['action']} | {r['status']} | "
                  f"`{r['reason'][:120].replace('|', '/').replace('`', '')}` |")
    md += ["", "The Section 27.6 replacement is the per-file summary of this table.", "",
           "Evaluation 3 Step 3 is recorded: D_rca_persist_k rival untested; Exp7 D_rca_pers is a different "
           "construct (max rho 0.877, drca_persist_comparison.json)."]
    (COR / "05_eval3_application.md").write_text("\n".join(md) + "\n")
    cnt = {}
    for r in rows:
        cnt[r["status"]] = cnt.get(r["status"], 0) + 1
    json.dumps(cnt)
    (RES / "corrections_applied_counts.json").write_text(json.dumps(cnt, indent=1))
    logger.info(f"applied: {cnt}; report_corrected.md {len(rep.lines)} lines (original {len(original.splitlines())})")
    for r in rows:
        if r["status"].startswith("NOT_APPLIED_TARGET"):
            logger.warning(f"{r['source_file']} | {r['block_id']} | {r['reason']}")


if __name__ == "__main__":
    main()
