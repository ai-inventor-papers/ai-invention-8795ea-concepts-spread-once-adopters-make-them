"""Title phrase matcher: one Aho-Corasick automaton over space-padded normalised surface forms.

Normalisation (identical for titles and surface forms): lowercase, curly apostrophe -> ', possessive 's
stripped, every run of non-letter/non-digit characters -> one space, padded with spaces, so a hit is always a
whole-word phrase match ('in vitro' never matches 'invitrogen'). Variants = simple plural/singular forms of the
last token (s / es / y->ies, and a trailing s stripped)."""
from __future__ import annotations

import re

import ahocorasick
import pyarrow as pa
import pyarrow.compute as pc

_NONWORD = re.compile(r"[^\w]+|_+", re.UNICODE)


def norm_py(text: str) -> str:
    t = text.lower().replace("’", "'")
    t = re.sub(r"'s\b", "", t)
    t = _NONWORD.sub(" ", t).strip()
    return f" {t} "


def norm_arrow(arr: pa.Array) -> pa.Array:
    t = pc.utf8_lower(pc.fill_null(arr, ""))
    t = pc.replace_substring(t, "’", "'")
    t = pc.replace_substring_regex(t, r"'s\b", "")
    t = pc.replace_substring_regex(t, r"[^\p{L}\p{N}]+", " ")
    return pc.binary_join_element_wise("", pc.utf8_trim_whitespace(t), "", " ")  # " " + t + " "


def variants(form: str) -> list[str]:
    toks = form.strip().split(" ")
    last = toks[-1]
    out = []
    if len(last) >= 4 and not last[-1].isdigit():
        if last.endswith("y") and last[-2] not in "aeiou":
            out.append(last[:-1] + "ies")
        elif last.endswith(("s", "x", "z", "ch", "sh")):
            out.append(last + "es")
            if last.endswith("s") and not last.endswith("ss"):
                out.append(last[:-1])
        else:
            out.append(last + "s")
        if last.endswith("ies"):
            out.append(last[:-3] + "y")
    return [" " + " ".join(toks[:-1] + [v]) + " " if len(toks) > 1 else f" {v} " for v in out]


def build_automaton(forms: dict[int, list[str]]) -> ahocorasick.Automaton:
    """forms: concept_idx -> list of raw surface forms. Value stored per key = tuple of (cidx, is_variant)."""
    table: dict[str, set] = {}
    for ci, fl in forms.items():
        for f in fl:
            n = norm_py(f)
            if len(n.strip()) < 3:
                continue
            table.setdefault(n, set()).add((ci, 0))
            for v in variants(n):
                table.setdefault(v, set()).add((ci, 1))
    A = ahocorasick.Automaton()
    for k, v in table.items():
        # exact beats variant when a string is both
        best = {}
        for ci, var in v:
            best[ci] = min(best.get(ci, 1), var)
        A.add_word(k, tuple(sorted(best.items())))
    A.make_automaton()
    return A


def match(A: ahocorasick.Automaton, padded_title: str) -> dict[int, int]:
    """-> {cidx: is_variant(0/1)} for one normalised padded title."""
    out: dict[int, int] = {}
    for _, vals in A.iter(padded_title):
        for ci, var in vals:
            out[ci] = min(out.get(ci, 1), var)
    return out
