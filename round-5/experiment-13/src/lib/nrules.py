"""Frame-N mining rules (frozen in prereg.md before any Frame-N count exists).

* token stream  = common5.surf(title).split()  (the same surface normaliser as the EXP5/EXP10 matcher)
* a token is VALID iff it is ASCII [a-z0-9]+, has >= 2 characters and at least one letter (not purely numeric)
* candidate n-grams: n in {2, 3}, all tokens valid, first and last token not in STOP (= NLTK stopwords of
  en/es/pt/fr/de/it + FILLER); the middle token of a trigram may be a stopword ('theory of mind')
* KEY = tuple of Porter stems (snowballstemmer 'porter', the matcher's stemmer) of the n-gram's tokens; the n-gram
  hash is a 63-bit mix of the stem hashes, so singular/plural/inflected surface forms share one key
  (stem-key grouping is applied at counting time)
* every key is counted at most once per title"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

LIB = Path(__file__).resolve().parent
ROOT = LIB.parent
STOPFILE = ROOT / "inputs" / "stoplists.json"

FILLER = ["study", "studies", "effect", "effects", "role", "impact", "case", "review", "new", "novel", "recent",
          "based", "using", "towards", "toward", "via", "approach", "results", "evaluation", "investigation",
          "assessment", "comparison", "analysis", "application", "applications", "development", "use", "influence",
          "characterization", "synthesis", "performance", "properties", "preparation", "design", "first", "two",
          "three", "high", "low", "different", "various"]
# frozen generic phrases (stem keys are compared, so plural forms are covered)
GENERIC = ["case study", "case report", "case series", "systematic review", "literature review", "recent advances",
           "recent progress", "recent developments", "novel approach", "new approach", "preliminary results",
           "preliminary study", "clinical trial", "randomized controlled trial", "controlled trial", "pilot study",
           "cross sectional", "cross sectional study", "united states", "united kingdom", "south africa",
           "new zealand", "hong kong", "saudi arabia", "south korea", "north america", "latin america",
           "european union", "middle east", "sub saharan africa", "developing countries", "developing country",
           "risk factors", "risk factor", "associated factors", "health care", "higher education",
           "retrospective study", "prospective study", "cohort study", "comparative study", "experimental study",
           "numerical simulation", "numerical study", "numerical analysis", "theoretical study",
           "theoretical analysis", "empirical study", "empirical analysis", "empirical evidence", "field study",
           "future directions", "future perspectives", "current status", "state of the art", "overview of",
           "short communication", "brief report", "editorial comment", "research progress", "research advances",
           "research status", "annual meeting", "annual report", "special issue", "conference proceedings",
           "book review", "letter to the editor", "invited review", "mini review", "open access",
           "meta analysis", "systematic review and meta analysis", "quality of life", "years of age",
           "significant difference", "long term", "short term", "large scale", "small scale", "real time",
           "high performance", "low cost", "key role", "important role", "critical role", "potential role",
           "part ii", "part i", "part iii", "et al", "vice versa"]
# added at S3 after the 60-candidate eye inspection, BEFORE the S3 hash (plan testing step 3): paratext / generic tokens
GENERIC_TOKENS = {"report", "reports", "appendix", "editorial", "editorials", "annual", "convention", "correspondence",
                  "briefing", "chart", "charts", "article", "articles", "paper", "papers", "part", "parts", "jr",
                  "photograph", "photographs", "meeting", "meetings", "conference", "proceedings", "symposium",
                  "workshop", "congress", "abstract", "abstracts", "letter", "letters", "issue", "issues", "volume",
                  "chapter", "book", "books", "erratum", "corrigendum", "preface", "introduction", "commentary",
                  "comment", "comments", "reply", "news", "newsletter", "bulletin", "minutes", "guest", "guests",
                  "challenges", "perspectives", "perspective", "prospects", "overview", "update", "updates",
                  "trends", "advances", "progress", "insights", "lessons", "learned", "toward", "beyond", "session",
                  "sessions", "keynote", "poster", "posters", "award", "awards", "obituary", "memoriam", "tribute",
                  "announcement", "call", "page", "pages", "supplement", "index", "contents", "table"}
TOK_OK = re.compile(r"^(?=.*[a-z])[a-z0-9]{2,}$")
M64 = np.uint64(0x7FFFFFFFFFFFFFFF)


def stoplists() -> dict:
    return json.loads(STOPFILE.read_text())


@lru_cache(maxsize=1)
def STOP() -> frozenset:
    s = stoplists()
    return frozenset(s["stop"]) | frozenset(FILLER)


_ST = None


@lru_cache(maxsize=2_000_000)
def stem(w: str) -> str:
    global _ST
    if _ST is None:
        import snowballstemmer
        _ST = snowballstemmer.stemmer("porter")
    return _ST.stemWord(w)


def mix64(x: np.ndarray) -> np.ndarray:
    z = np.asarray(x).astype(np.uint64) + np.uint64(0x9E3779B97F4A7C15)
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return (z ^ (z >> np.uint64(31))) & M64


def str_hash(arr) -> np.ndarray:
    """Deterministic 64-bit hash of strings (pandas SipHash with its fixed default key)."""
    return pd.util.hash_array(np.asarray(arr, dtype=object), categorize=False).astype(np.uint64)


def combine(hs: list[np.ndarray]) -> np.ndarray:
    with np.errstate(over="ignore"):
        h = mix64(hs[0] * np.uint64(0x9E3779B97F4A7C15) + np.uint64(len(hs)))
        for x in hs[1:]:
            h = mix64((h * np.uint64(0xD6E8FEB86659FD93)) ^ x)
    return h


def key_of_tokens(tokens: list[str]) -> tuple[str, ...]:
    return tuple(stem(t) for t in tokens)


def key_hash(key: tuple[str, ...]) -> int:
    hs = [str_hash([s]) for s in key]
    return int(combine(hs)[0])


def surf_tokens(text: str) -> list[str]:
    from common5 import surf
    return surf(text).split()


def ngram_table(stitles_trimmed, want_forms: bool = False) -> dict:
    """Vectorised n-gram extraction. stitles_trimmed: pyarrow string array of surf()-normalised, trimmed titles.
    Returns row (title index), h (63-bit key hash), n (2|3) and, if want_forms, the surface form of each n-gram."""
    import pyarrow.compute as pc
    toks = pc.split_pattern(stitles_trimmed, " ")
    ln = pc.fill_null(pc.list_value_length(toks), 0).to_numpy(zero_copy_only=False).astype(np.int64)
    flat = pc.list_flatten(toks).to_numpy(zero_copy_only=False)
    row = np.repeat(np.arange(len(ln)), ln)
    if len(flat) < 2:
        return {"row": np.zeros(0, np.int64), "h": np.zeros(0, np.uint64), "n": np.zeros(0, np.int8),
                "form": np.zeros(0, object)}
    codes, uniq = pd.factorize(flat)
    stop = STOP()
    u_valid = np.fromiter((bool(TOK_OK.match(u)) for u in uniq), bool, len(uniq))
    u_stop = np.fromiter((u in stop for u in uniq), bool, len(uniq))
    u_h = str_hash([stem(u) if v else "" for u, v in zip(uniq, u_valid)])
    valid, isstop, th = u_valid[codes], u_stop[codes], u_h[codes]
    L = len(flat)
    i2 = np.nonzero((row[:-1] == row[1:]) & valid[:-1] & valid[1:] & ~isstop[:-1] & ~isstop[1:])[0]
    i3 = np.nonzero((row[:-2] == row[2:]) & valid[:-2] & valid[1:-1] & valid[2:] & ~isstop[:-2] & ~isstop[2:])[0] \
        if L >= 3 else np.zeros(0, np.int64)
    h2 = combine([th[i2], th[i2 + 1]])
    h3 = combine([th[i3], th[i3 + 1], th[i3 + 2]])
    out = {"row": np.concatenate([row[i2], row[i3]]), "h": np.concatenate([h2, h3]),
           "n": np.concatenate([np.full(len(i2), 2, np.int8), np.full(len(i3), 3, np.int8)])}
    if want_forms:
        f2 = uniq[codes[i2]].astype(object) + " " + uniq[codes[i2 + 1]].astype(object)
        f3 = (uniq[codes[i3]].astype(object) + " " + uniq[codes[i3 + 1]].astype(object) + " "
              + uniq[codes[i3 + 2]].astype(object))
        out["form"] = np.concatenate([np.asarray(f2, object), np.asarray(f3, object)])
    return out
