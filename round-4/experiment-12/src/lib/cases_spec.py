"""Frozen (pre-seal) rules for the matched case pairs (S8) and the retrospective AI/CS atlas (S9).
Case selection follows a most-similar design (Seawright & Gerring 2008): matched on B5 volume and growth, opposite
on OPEN_all, outcome shown only AFTER selection. The atlas is outcome-selected BY DESIGN (descriptive stage-1
inspection) and is labelled so everywhere."""
from __future__ import annotations

import re

import numpy as np

GENERIC_REGEX = (r"(?i)^(coefficient|exponential|linear|rate|ratio|index|analysis|method|model|approach|system|"
                 r"process|cross[- ]?disciplinary|interdisciplinary)\b")
GENERIC_ZIPF = 4.0                  # single-token names with wordfreq zipf_frequency >= 4.0 are generic
PRE_ONSET_FOOTPRINT = 0.5           # grounded papers in 1995..t0-1 >= 0.5 x early volume -> generic / re-emerging

CASE_RULE = {
    "pools": "per reporting group: top-quintile OPEN_all vs bottom-quintile OPEN_all among non-generic concepts with "
             "OPEN_home defined (quintiles within reporting group)",
    "match": "|z logvol diff| <= 0.25 and |z growth_c diff| <= 0.25 (z over all 12,499), same reporting group, "
             "|t0 diff| <= 2; widen to 0.35 for a group with no valid match (logged)",
    "seeding": "first try concepts named in EXP8 case_exemplars.json (high/low lists) as anchors; then the pair with "
               "the largest OPEN_all gap among remaining matches; ties by the smallest Mahalanobis distance on "
               "(logvol, growth_c, offhome_share)",
    "limits": "6-8 pairs; at most 2 from CS+Eng; at least 4 groups covered; one concept in at most one pair",
    "outcome_use": "O2r is NOT used in selection; displayed after selection only",
    "tol": 0.25, "tol_wide": 0.35, "max_pairs": 8, "min_pairs": 6, "max_cs_eng": 2,
}

AI_SUBFIELDS = {1702, 1707}
AI_TOPIC_REGEX = r"(?i)neural|learning|language processing|reinforcement|recommender|speech recognition"
ATLAS_RULE = {
    "eligible": "home contains field 17 (Computer Science) AND AI share >= 0.3 (share of t0..t0+2 topic assignments "
                "whose topic subfield is 1702 AI or 1707 Computer Vision, or whose topic name matches "
                f"'{AI_TOPIC_REGEX}'); generic filter applied; relax to 0.2 then 0.1 if a type has < 8 (logged tier)",
    "types": {"RAPID": "top-decile early growth (growth_c, among eligible)",
              "GRADUAL": "bottom-half early growth & O1b = 1 (sustained uptake)",
              "LOCAL": "O1b = 1 & bottom O2r_resid tercile",
              "DIFFUSING": "top O2r_resid tercile",
              "TRANSIENT": "O3 = 1"},
    "per_type": 8, "order": "largest early volume first; a concept is used in at most one type (type order as listed)",
    "looked_meaningful": "measure separates DIFFUSING from LOCAL by >= 0.5 pooled SD at age 2 AND has the same sign "
                         "as the frame-wide DEV Spearman with O2r_resid",
    "label": "RETROSPECTIVE, DESCRIPTIVE, OUTCOME-SELECTED BY DESIGN",
}


def generic_flags(names, pre_onset, early_volume) -> tuple[np.ndarray, list[str]]:
    from wordfreq import zipf_frequency
    rx = re.compile(GENERIC_REGEX)
    out, why = [], []
    for n, p, e in zip(names, pre_onset, early_volume):
        n = str(n)
        r = []
        if p >= PRE_ONSET_FOOTPRINT * e:
            r.append("pre_onset_footprint")
        toks = n.split()
        if len(toks) == 1 and zipf_frequency(n.lower(), "en") >= GENERIC_ZIPF:
            r.append("common_single_token")
        if rx.search(n):
            r.append("generic_regex")
        out.append(bool(r))
        why.append("|".join(r))
    return np.array(out), why
