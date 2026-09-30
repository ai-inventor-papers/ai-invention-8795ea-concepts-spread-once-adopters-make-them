"""Aho-Corasick surface matching + stemmed positional verification.

Keys and titles are both passed through common.surf (space padded), so a key ' graphene ' can only hit on
word boundaries (never inside ' polygraphene '). Each AC hit is then verified with the OpenAlex-like stemmed
positional phrase matcher (common.analyse / spec_in) on the matched form."""
from __future__ import annotations

import ahocorasick

from common5 import MTYPES, phrase_spec, spec_in, title_pos


def build_automaton(entries: list[tuple[str, int, str]]) -> tuple[ahocorasick.Automaton, list]:
    """entries: (space-padded surface form, concept index, mtype). Returns automaton and spec list."""
    A = ahocorasick.Automaton()
    specs = []
    for form, ci, mt in entries:
        if form in A:
            continue
        specs.append(phrase_spec(form))
        A.add_word(form, (ci, MTYPES.index(mt), len(specs) - 1))
    A.make_automaton()
    return A, specs


def match(stitle: str, raw_title: str, A, specs) -> dict[int, int]:
    """{concept index: best mtype code} for verified hits in one title (stitle = surf(title))."""
    hits: dict[int, list[tuple[int, int]]] = {}
    for _, (ci, mt, si) in A.iter(stitle):
        hits.setdefault(ci, []).append((mt, si))
    if not hits:
        return {}
    pos = title_pos(raw_title)
    out = {}
    for ci, lst in hits.items():
        for mt, si in sorted(lst):
            if spec_in(pos, specs[si]):
                out[ci] = mt
                break
    return out
