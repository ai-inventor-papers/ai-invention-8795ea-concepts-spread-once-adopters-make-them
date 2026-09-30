#!/usr/bin/env python3
"""STEP 5: independent re-verification of results/claims_ledger_v3.csv.

Does NOT import the Ledger class: it has its own key-path parser (JSON dotted / [i] / ['key'] paths; CSV
'col==v&col2==v::column[i]'), re-reads every source file, re-computes each status, and checks that every numeric
token in corrections/*.md has a ledger row in that file (orphan check). Exclusions from the orphan check: headings,
verbatim quotes of the OLD draft text ('>' lines), text in backticks, years, section numbers, list indices, and design
constants that appear in the sealed results/boundary_spec.json. Usage: python verify_ledger.py"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import pandas as pd
from loguru import logger

WS = Path(__file__).resolve().parent
RUNP = WS.parents[3]                        # directory that contains 3_invention_loop
LOGS, RES, COR = WS / "logs", WS / "results", WS / "corrections"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "verify_ledger.log", rotation="30 MB", level="DEBUG")

TOK = re.compile(r"\['([^']+)'\]|\[(\d+)\]|([^.\[\]]+)")
NUM = re.compile(r"(?<![\w.])[-+−]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:e[-+]?\d+)?(?![\w])")
_cache: dict = {}


def resolve(p: str) -> Path:
    q = RUNP / p
    return q if q.exists() else WS / p


def load(p: Path):
    if p not in _cache:
        _cache[p] = (json.loads(p.read_text()) if p.suffix == ".json" else
                     pd.read_csv(p) if p.suffix == ".csv" else p.read_text())
    return _cache[p]


def walk_json(obj, path: str):
    for m in TOK.finditer(path):
        key, idx, name = m.groups()
        obj = obj[key] if key is not None else (obj[int(idx)] if idx is not None else obj[name])
    return obj


def walk_csv(df: pd.DataFrame, path: str):
    filt, col = path.rsplit("::", 1)
    idx = None
    mm = re.match(r"(.+)\[(\d+)\]$", col)
    if mm:
        col, idx = mm.group(1), int(mm.group(2))
    mask = pd.Series(True, index=df.index)
    for cond in [c for c in filt.split("&") if c]:
        c, v = cond.split("==", 1)
        mask &= df[c].astype(str) == v
    sub = df.loc[mask, col]
    assert len(sub) == 1, f"{path}: {len(sub)} rows"
    v = sub.iloc[0]
    return json.loads(v)[idx] if idx is not None else v


def tol_of(txt: str) -> float:
    t = txt.replace(",", "").replace("+", "").replace("−", "-").lower()
    mant, _, ex = t.partition("e")
    dec = len(mant.split(".")[1]) if "." in mant else 0
    return 0.5 * 10 ** (-dec + (int(ex) if ex else 0)) * 1.0000001


def carry_source(src: Path, key: str) -> str:
    """Independent reconstruction of the text a verbatim token was carried from."""
    if key.startswith("## "):                               # Eval2 text_corrections.md block
        title = key[3:].rsplit("::", 1)[0]
        t = load(src)
        i = t.find("## " + title + "\n")
        j = t.find("\n## ", i + 3)
        return t[i:j if j > 0 else len(t)]
    if key.startswith("claim_id=="):
        df = load(src)
        r = df[df.claim_id.astype(str) == key.split("==", 1)[1]]
        return " | ".join(str(x) for x in r.iloc[0].tolist())
    if key.startswith("count [ARTIFACT:"):
        return str(load(src).count(key[len("count "):]))
    return str(walk_json(load(src), key))


def verify_rows(L: pd.DataFrame) -> pd.DataFrame:
    out = []
    for r in L.itertuples():
        src = resolve(r.source_file)
        try:
            if r.kind == "carry":
                txt = carry_source(src, r.key_path)
                ok = r.reported_value in set(NUM.findall(txt)) or re.search(r"(?<![\w.])" + re.escape(str(r.reported_value)) + r"(?![\w])", txt)
                st, fv = ("MATCH" if ok else "MISMATCH"), r.reported_value
            else:
                obj = load(src)
                v = walk_csv(obj, r.key_path) if src.suffix == ".csv" else walk_json(obj, r.key_path)
                fv = float(v) * float(r.scale)
                rv = float(str(r.reported_value).replace(",", "").replace("+", ""))
                d = abs(rv - fv)
                st = "MATCH" if d <= 1e-12 else ("ROUNDING_ONLY" if d <= tol_of(str(r.reported_value)) else "MISMATCH")
        except (FileNotFoundError, KeyError, IndexError, TypeError, ValueError, AssertionError) as e:
            st, fv = "NOT_FOUND", f"{type(e).__name__}: {e}"[:120]
        out.append({"claim_id": r.claim_id, "recomputed_status": st, "recomputed_file_value": fv,
                    "ledger_status": r.status, "agree": st == r.status})
    return pd.DataFrame(out)


def orphans(L: pd.DataFrame) -> list[dict]:
    spec_txt = (RES / "boundary_spec.json").read_text()
    constants = set(NUM.findall(spec_txt)) | {"0.10", "1e-3", "0.5", "1.2", "30%", "30", "2", "3", "4", "5", "6", "7", "10"}
    out = []
    for f in sorted(COR.glob("*.md")):
        vals = set(L[L.target_file == f.name].reported_value.astype(str))
        for ln, line in enumerate(f.read_text().splitlines(), 1):
            if line.startswith("#") or line.startswith(">"):
                continue
            clean = re.sub(r"`[^`]*`", " ", line)
            clean = re.sub(r"(?i)\blines?\s+\d+(\s*-\s*\d+)?", " ", clean)          # file line references
            clean = re.sub(r"95% CI|\(\d{1,3}(,\d{3})*\)(?=\s*\|)", " ", clean)             # CI label; B in table header
            clean = re.sub(r"(?i)(sections?|iteration|experiment|exp|evaluation|research|dataset|p)\s*\d+(\.\d+)*[a-z]?", " ", clean)
            clean = re.sub(r"\b\d{1,2}\.\d{1,2}[a-z]?\b(?=[ ,;:)/]|$)(?![\d])", lambda m: m.group(0) if m.group(0) in vals else " ", clean)
            clean = re.sub(r"^\s*(\d+\.|-)\s", " ", clean)
            clean = re.sub(r"\b(19|20)\d{2}(-\d{2})?\b", " ", clean)
            for tok in NUM.findall(clean):
                t = tok.replace("−", "-")
                if t in vals or t.lstrip("+-") in {v.lstrip("+-") for v in vals} or t.lstrip("+-") in constants:
                    continue
                out.append({"file": f.name, "line": ln, "token": t, "context": line.strip()[:140]})
    return out


def main() -> None:
    L = pd.read_csv(RES / "claims_ledger_v3.csv", dtype={"reported_value": str})
    V = verify_rows(L)
    O = orphans(L)
    summary = {"n_rows": int(len(L)), "ledger_status_counts": L.status.value_counts().to_dict(),
               "recomputed_status_counts": V.recomputed_status.value_counts().to_dict(),
               "n_disagreements": int((~V.agree).sum()), "n_mismatch_recomputed": int((V.recomputed_status == "MISMATCH").sum()),
               "n_not_found_recomputed": int((V.recomputed_status == "NOT_FOUND").sum()),
               "n_carry_rows": int((L.kind == "carry").sum()), "n_value_rows": int((L.kind == "value").sum()),
               "n_orphan_numeric_tokens": len(O), "orphans": O,
               "disagreements": V[~V.agree].to_dict("records")[:50]}
    V.to_csv(RES / "ledger_verification_rows.csv", index=False)
    (RES / "ledger_verification.json").write_text(json.dumps(summary, indent=1, default=str))
    logger.info(f"verify: {summary['recomputed_status_counts']}; disagreements {summary['n_disagreements']}; "
                f"orphans {len(O)}")
    for o in O[:30]:
        logger.warning(f"orphan {o['file']}:{o['line']} '{o['token']}' | {o['context'][:100]}")


if __name__ == "__main__":
    logger.catch(reraise=True)(main)()
