"""Context for lib/ego.py: EXP3 Leiden-gamma-3 topic backbones (slices 2000-04/05-09/10-14), topic metadata,
content lemmas (verbatim from EXP3 common.py), and the Pass A full-corpus topic background."""
from __future__ import annotations

import json
import re
from collections import Counter
from functools import lru_cache

import numpy as np
import pandas as pd

from common import E8_DATA as DATA, E8_INPUTS as INPUTS  # PATCH (plan fallback 4): resolve against EXP8 inputs

_STOP = set("a an and are as at be but by for if in into is it no not of on or such that the their then there these "
            "they this to was will with its via from using based".split())
_TOK = re.compile(r"[^\W_]+", re.UNICODE)


@lru_cache(maxsize=None)
def _stemmer():
    import snowballstemmer
    return snowballstemmer.stemmer("porter")


def lemmas(text: str) -> set[str]:
    t = re.sub(r"[\-‐-—/]", " ", str(text).lower())
    return {_stemmer().stemWord(w) for w in _TOK.findall(t) if w not in _STOP and len(w) > 1}


def topic_lemma_df(names: list[str]) -> Counter:
    df = Counter()
    for n in names:
        df.update(lemmas(n))
    return df


def backbone_context() -> dict:
    tids = json.loads((INPUTS / "topic_ids.json").read_text())
    tm = pd.read_csv(INPUTS / "topic_meta.csv").set_index("topic").loc[tids]
    sl = [np.load(INPUTS / "backbone" / f"slice{s}.npz") for s in range(3)]
    names = tm.name.tolist()
    return dict(nt=len(tids), comm=[z["comm"] for z in sl], comm_q=[z["comm_q"] for z in sl],
                deg=[z["deg"] for z in sl], knn=[(z["ka"], z["kb"]) for z in sl],
                full_edges=[(z["a"], z["b"]) for z in sl], subfield=tm.subfield.to_numpy(), names=names,
                ldf=topic_lemma_df(names), tlem=[lemmas(n) for n in names], lemmas=lemmas)


def rq1_context() -> dict:
    ctx = backbone_context()
    z = np.load(DATA / "bg_topics.npz")
    years = z["years"].tolist()
    ctx.update(years=years, bg=z["BG"], Gt=dict(zip(years, z["GT"].tolist())))
    return ctx
