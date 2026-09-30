#!/usr/bin/env python3
"""STEP 1: outcome-blind lexicon v0 from the legacy OpenAlex concept vocabulary (levels 2-5).

Surface forms per concept: normalised display name (parenthetical disambiguators stripped), a joined-hyphen
variant, and singular/plural variants of the last token. Forms shared by two concepts are dropped for both
(an ambiguous form goes to nobody). Output: lexicon_v0.parquet + frozen_lexicon.sha256 (appended)."""
from __future__ import annotations

import hashlib
import re
from collections import defaultdict

import pandas as pd
import pyarrow.parquet as pq

from common import ES_STOP, RES, ROOT, SNAP, phrase_spec, plural_variants, setup_logger, surf

logger = setup_logger("lexicon")
PAREN = re.compile(r"\s*\([^)]*\)\s*")


def load_concepts() -> pd.DataFrame:
    fs = sorted((SNAP / "concepts").glob("*.parquet"))
    return pd.concat([pq.read_table(f, columns=["id", "display_name", "level", "description", "wikidata",
                                                "works_count"]).to_pandas() for f in fs]).drop_duplicates("id",
                                                                                                          keep="last")


def forms_for(name: str) -> list[tuple[str, str]]:
    """[(surface form, mtype)] for a display name."""
    base = PAREN.sub(" ", name).strip()
    if not base:
        return []
    out: dict[str, str] = {}
    s = surf(base)
    if s.strip():
        out[s] = "name_exact"
    # hyphen variants: 'e-mail' -> 'email'
    if "-" in base:
        j = surf(base.replace("-", ""))
        if j.strip():
            out.setdefault(j, "name_variant")
    for f in list(out):
        for v in plural_variants(f.strip()):
            out.setdefault(" " + v + " ", "name_variant")
    return list(out.items())


def valid_form(f: str) -> bool:
    toks = f.split()
    if not toks:
        return False
    if len(toks) == 1 and (len(toks[0]) <= 3 or toks[0] in ES_STOP):
        return False
    if all(t in ES_STOP for t in toks):
        return False
    if all(t.isdigit() for t in toks):
        return False
    return bool(phrase_spec(f))


@logger.catch(reraise=True)
def main() -> None:
    df = load_concepts()
    logger.info(f"legacy concepts: {len(df)}")
    lvl01 = {surf(PAREN.sub(" ", n)) for n in df[df.level <= 1].display_name}
    df = df[df.level >= 2].copy()
    df["concept_id"] = df.id.str.rsplit("/", n=1).str[-1].str.lstrip("C").astype("int64")
    df["qid"] = df.wikidata.fillna("").str.rsplit("/", n=1).str[-1]
    owners: dict[str, set[int]] = defaultdict(set)
    per: dict[int, list[tuple[str, str]]] = {}
    n_bad = 0
    for cid, name in zip(df.concept_id, df.display_name):
        fs = [(f, m) for f, m in forms_for(name) if valid_form(f) and f not in lvl01]
        n_bad += len(forms_for(name)) - len(fs)
        per[cid] = fs
        for f, _ in fs:
            owners[f].add(cid)
    amb = {f for f, o in owners.items() if len(o) > 1}
    rows = []
    for cid, name, lvl, desc, qid, wc in zip(df.concept_id, df.display_name, df.level, df.description, df.qid,
                                             df.works_count):
        fs = [(f, m) for f, m in per[cid] if f not in amb]
        if not any(m == "name_exact" for _, m in fs):
            continue  # the concept's own name is ambiguous/invalid -> not usable
        rows.append({"concept_id": int(cid), "qid": qid, "name": name, "level": int(lvl),
                     "description": desc or "", "works_count_legacy": int(wc or 0),
                     "forms": [f for f, _ in fs], "mtypes": [m for _, m in fs]})
    lex = pd.DataFrame(rows).sort_values("concept_id").reset_index(drop=True)
    out = ROOT / "lexicon_v0.parquet"
    lex.to_parquet(out, index=False)
    h = hashlib.sha256(out.read_bytes()).hexdigest()
    (ROOT / "frozen_lexicon.sha256").write_text(f"lexicon_v0.parquet {h}\n")
    logger.info(f"lexicon_v0: {len(lex)} concepts, {sum(len(f) for f in lex.forms)} forms; "
                f"ambiguous forms dropped={len(amb)}, invalid/level01 forms dropped={n_bad}; sha256={h[:12]}")
    (RES / "lexicon_v0_summary.json").write_text(pd.Series({
        "n_concepts": len(lex), "n_forms": int(sum(len(f) for f in lex.forms)), "ambiguous_forms": len(amb),
        "invalid_or_level01_forms": n_bad, "levels": lex.level.value_counts().sort_index().to_dict(),
        "sha256": h}).to_json(indent=1))


if __name__ == "__main__":
    main()
