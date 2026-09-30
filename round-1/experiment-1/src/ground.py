"""Local exact/lemma phrase confirmation on title + abstract (guards against stemmed-search false positives)."""
from __future__ import annotations

import re

from panel import ACRONYMS

LEMMAS = {  # extra surface variants beyond the regular optional plural
    "optogenetics": ["optogenetic", "optogenetics"],
    "crowdsourcing": ["crowdsourcing", "crowdsourced", "crowd sourcing", "crowd sourced"],
    "compressed sensing": ["compressed sensing", "compressive sensing"],
    "Web 2.0": ["web 2.0"],
}


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[-_/]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def _pat(phrase: str) -> re.Pattern:
    toks = norm(phrase).split(" ")
    body = r"[\s\-]+".join(re.escape(t) for t in toks)
    return re.compile(r"(?<![a-z0-9])" + body + r"(?:s|es)?(?![a-z0-9])")


def _acr_pat(acr: str) -> re.Pattern:
    toks = acr.split(" ")
    body = r"[\s\-]+".join(re.escape(t) for t in toks)
    return re.compile(r"(?<![A-Za-z0-9])" + body + r"s?(?![A-Za-z0-9])")


class Matcher:
    def __init__(self, aliases: list[str]) -> None:
        self.pats: list[re.Pattern] = []
        self.acr: list[tuple[re.Pattern, re.Pattern | None]] = []
        for a in aliases:
            if a in ACRONYMS:
                ctx = re.compile(r"endoscop|transluminal", re.I) if a == "NOTES" else None
                self.acr.append((_acr_pat(a), ctx))
            else:
                for v in LEMMAS.get(a, [a]):
                    self.pats.append(_pat(v))

    def match(self, text: str) -> bool:
        if not text:
            return False
        n = norm(text)
        if any(p.search(n) for p in self.pats):
            return True
        for p, ctx in self.acr:
            if p.search(text) and (ctx is None or ctx.search(text)):
                return True
        return False


def status(m: Matcher, title: str | None, abstract: str | None) -> str:
    """'confirmed' (phrase found), 'rejected' (full abstract available, phrase absent) or 'unverifiable'
    (abstract elided by the publisher and phrase absent from title: kept on the strength of the S2 phrase index)."""
    if m.match(title or "") or m.match(abstract or ""):
        return "confirmed"
    return "rejected" if abstract else "unverifiable"
