#!/usr/bin/env python3
"""P4 checks -> results/ledger_rerun.json:
 (a) v3 re-verification (copied verify_ledger over an unmodified copy of Eval3 claims_ledger_v3.csv)
 (b) v4 verification (same verifier over results/claims_ledger_v4.csv and corrections_iter5/*.md, orphan check)
 (c) text presence of every v3 / v4 reported_value inside its target section of report_corrected.md
 (d) stale-string scan of report_corrected.md
 (e) verbatim checks (Section 23, PR1-PR3, H-M1..H-P1 clause lines, Exp10 'Leads replicated' block)
Usage: python src/checks.py"""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pandas as pd
from loguru import logger

from ledger import Ledger
from paths import COR, E10, E11, E12, EVAL3, LOGS, REPORT5, RES, WS, jdump

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "checks.log", rotation="30 MB", level="DEBUG")
PY = sys.executable


def supplementary_rows() -> None:
    """Ledger rows for numbers that apply_corrections.py writes into 05_eval3_application.md."""
    L = Ledger()
    L.target_file, L.section = "05_eval3_application.md", "27.6"
    L.num(EVAL3 / "results/drca_persist_comparison.json",
          "comparisons.D_rca_persist_2_rca.spearman_vs_D_rca_pers", "{:.3f}")
    v4 = pd.read_csv(RES / "claims_ledger_v4.csv", dtype={"reported_value": str})
    v4 = v4[v4.target_file != "05_eval3_application.md"]
    sup = pd.DataFrame(L.rows)
    sup["claim_id"] = [f"S{i + 1:04d}" for i in range(len(sup))]
    pd.concat([v4, sup], ignore_index=True).to_csv(RES / "claims_ledger_v4.csv", index=False)


def run_verifier(args: list[str]) -> dict:
    r = subprocess.run([PY, str(WS / "verify_ledger_v4.py")] + args, capture_output=True, text=True,
                       env={"PYTHONDONTWRITEBYTECODE": "1", "OPENBLAS_NUM_THREADS": "1", "PATH": "/usr/bin:/bin"})
    (LOGS / f"verifier_{args[-1]}.out").write_text(r.stdout + r.stderr)
    if r.returncode:
        raise RuntimeError(r.stderr[-800:])
    return json.loads((RES / f"{args[-1]}.json").read_text())


# ----------------------------------------------------------------------------- report sections
def heading_level(ln: str) -> int:
    m = re.match(r"^(#{1,6}) ", ln)
    return len(m.group(1)) if m else 0


def section_text(lines: list[str], label: str) -> tuple[str, str]:
    m = re.search(r"(\d+(?:\.\d+)?[a-z]?)", str(label))
    if not m:
        return "\n".join(lines), "whole document (label has no section number)"
    num = m.group(1)
    rx = re.compile(rf"^#{{1,6}} {re.escape(num)}[\. ]")
    for i, ln in enumerate(lines):
        if rx.match(ln):
            lv = heading_level(ln)
            j = i + 1
            while j < len(lines) and not (heading_level(lines[j]) and heading_level(lines[j]) <= lv):
                j += 1
            return "\n".join(lines[i:j]), f"section {num}"
    return "\n".join(lines), f"whole document (section {num} heading not found)"


def variants(v: str) -> list[str]:
    v = str(v)
    out = {v, v.replace("-", "−"), v.replace("−", "-")}
    if v.startswith("+"):
        out |= {v[1:]}
    if v.startswith("-"):
        out |= {"−" + v[1:]}
    return list(out)


def presence(ledger: pd.DataFrame, lines: list[str], tag: str) -> dict:
    rows, cache = [], {}
    whole = "\n".join(lines)
    for r in ledger.itertuples():
        if r.target_section not in cache:
            cache[r.target_section] = section_text(lines, r.target_section)
        txt, scope = cache[r.target_section]
        pat = [r"(?<![\w.])" + re.escape(x) + r"(?![\w])" for x in variants(r.reported_value)]
        ok = any(re.search(q, txt) for q in pat)
        st = "TEXT_PRESENT" if ok else ("TEXT_PRESENT_ELSEWHERE" if any(re.search(q, whole) for q in pat)
                                        else "TEXT_ABSENT")
        rows.append({"ledger": tag, "claim_id": r.claim_id, "target_file": r.target_file,
                     "target_section": r.target_section, "scope": scope, "reported_value": r.reported_value,
                     "status": st})
    df = pd.DataFrame(rows)
    return {"counts": df.status.value_counts().to_dict(), "absent": df[df.status != "TEXT_PRESENT"].to_dict("records"),
            "n_whole_document_scope": int(df.scope.str.startswith("whole").sum())}


@logger.catch(reraise=True)
def main() -> None:
    supplementary_rows()
    e3 = EVAL3
    a = run_verifier(["--ledger", str(RES / "claims_ledger_v3_copy.csv"), "--cor", str(e3 / "corrections"),
                      "--base", str(e3), "--out", "ledger_v3_reverify"])
    b = run_verifier(["--ledger", str(RES / "claims_ledger_v4.csv"), "--cor", str(COR), "--base", str(WS),
                      "--out", "ledger_v4_verification"])
    rc = (WS / "report_corrected.md").read_text()
    lines = rc.splitlines()
    v3 = pd.read_csv(RES / "claims_ledger_v3_copy.csv", dtype={"reported_value": str})
    v4 = pd.read_csv(RES / "claims_ledger_v4.csv", dtype={"reported_value": str})
    c3, c4 = presence(v3, lines, "v3"), presence(v4, lines, "v4")
    pd.DataFrame(c3["absent"] + c4["absent"]).to_csv(RES / "text_absent_rows.csv", index=False)
    # ---------------- (d) stale strings
    old = REPORT5.read_text().splitlines()
    i = next(k for k, s in enumerate(old) if s.startswith("### 26.4"))
    names = set()
    for s in old[i:i + 15]:
        if s.startswith("|") and not s.startswith("|---") and "high OPEN concept" not in s:
            c = [x.strip() for x in s.strip("|").split("|")]
            names |= {c[0], c[1]}
    cp = json.loads((E12 / "results/case_pairs.json").read_text())
    real = {p["high"] for p in cp["pairs"]} | {p["low"] for p in cp["pairs"]}
    atlas = {c["name"] for c in json.loads((E12 / "ai_atlas/atlas.json").read_text())["concepts"]}
    invented = sorted(names - real)
    stale = {"footprint control rung": r"footprint control rung",
             "GPU computing and deep learning are canonical cases": r"GPU computing and deep learning are canonical",
             "lone I2 = 0.43 without model label": r"I²? ?(?:drops to|=) ?0\.43(?![^\n]{0,30}sub-units)",
             "old O3 learned row": r"diff = -0\.021 \(not evaluable\)"}
    hits = {}
    for k, rx in stale.items():
        hits[k] = [{"line": n + 1, "text": s[:160]} for n, s in enumerate(lines) if re.search(rx, s)]
    inv_hits = {}
    for nm in invented:
        hh = []
        for n, s in enumerate(lines):
            if re.search(r"(?<![\w-])" + re.escape(nm) + r"(?![\w-])", s):
                is_atlas_row = s.startswith("|") and nm in atlas and s.startswith(f"| {nm} |")
                is_note = "[Correction, iteration" in s and ("no artifact produced" in s or "deleted" in s)
                hh.append({"line": n + 1, "text": s[:160], "legit_atlas_row": bool(is_atlas_row),
                           "correction_note_mention": bool(is_note)})
        inv_hits[nm] = hh
    n_stale = sum(len(v) for v in hits.values()) + sum(1 for v in inv_hits.values() for h in v
                                                        if not h["legit_atlas_row"] and not h["correction_note_mention"])
    n_note = sum(1 for v in inv_hits.values() for h in v if h["correction_note_mention"])
    # ---------------- (e) verbatim checks
    verb = {}
    s23 = (RES / "section23_source_slice.txt").read_text().replace(
        "## 23. What we have learned so far", "## 23. What we have learned so far (end of iteration 3)", 1)
    verb["section23_byte_identical"] = s23 in rc
    pr = json.loads((E12 / "results/preregistration_R2.json").read_text())
    for k in ("PR1", "PR1b", "PR2", "PR3"):
        verb[f"{k}_verbatim"] = pr[k] in rc
    pl = (E11 / "prereg.md").read_text().splitlines()[23:32]
    verb["Exp11_HM1_HP1_lines_24_32_verbatim"] = all(("> " + x) in rc for x in pl)
    ld = (E10 / "README.md").read_text().splitlines()[47:53]
    verb["Exp10_leads_block_lines_48_53_verbatim"] = all(("> " + x) in rc for x in ld)
    out = {"a_v3_reverify": {k: v for k, v in a.items() if k != "disagreements"},
           "b_v4": {k: v for k, v in b.items() if k != "disagreements"},
           "c_text_presence": {"v3": {k: v for k, v in c3.items() if k != "absent"},
                               "v4": {k: v for k, v in c4.items() if k != "absent"},
                               "absent_rows_file": "results/text_absent_rows.csv"},
           "d_stale": {"hits": hits, "invented_26_4_names": invented, "invented_name_hits": inv_hits,
                       "n_stale_hits": n_stale, "n_correction_note_mentions": n_note,
                       "rule": "invented-name hits that are rows of the 26.5 AI atlas table (real atlas concepts) "
                               "are legitimate and not counted; a mention inside the mandated correction note that "
                                       "announces the deletion ('...contained 5 rows that no artifact produced...') is "
                                       "counted separately as n_correction_note_mentions"},
           "e_verbatim": verb}
    jdump(RES / "ledger_rerun.json", out)
    logger.info(f"v3: {a['recomputed_status_counts']} orphans {a['n_orphan_numeric_tokens']}")
    logger.info(f"v4: {b['recomputed_status_counts']} orphans {b['n_orphan_numeric_tokens']} rows {b['n_rows']}")
    logger.info(f"text presence v3 {c3['counts']} v4 {c4['counts']}")
    logger.info(f"stale hits {n_stale}; verbatim {verb}")


if __name__ == "__main__":
    main()
