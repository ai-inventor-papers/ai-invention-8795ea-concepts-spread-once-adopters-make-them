"""Shared constants, paths, the OpenAlex-like title analyser (copied verbatim from art_yrradSC27HtQ
scan_snapshot.py) and small helpers used by every step of the pipeline."""
from __future__ import annotations

import json
import math
import re
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent


def _dep_dir(env: str, artifact_id: str, run_tree_rel: str) -> Path:
    """Input artifact directory: env var override, else the run tree (pipeline layout), else the sibling folder
    of the published repository named by the artifact id."""
    import os
    if os.environ.get(env):
        return Path(os.environ[env])
    run_tree = ROOT.parents[3] / run_tree_rel
    return run_tree if run_tree.exists() else ROOT.parent / artifact_id


# iteration-1 inputs (read-only): art_yrradSC27HtQ (scan/analyser/source-field map), art_33_KKk_G8Gw5 (frozen backbone)
ART3 = _dep_dir("AII_ART_YRRAD_DIR", "art_yrradSC27HtQ", "3_invention_loop/iter_1/gen_art/gen_art_experiment_3")
ART33 = _dep_dir("AII_ART_33_DIR", "art_33_KKk_G8Gw5", "3_invention_loop/iter_1/gen_art/gen_art_experiment_4")
SNAP = ROOT / "snapshot"
SCAN = ROOT / "scan"
RES = ROOT / "results"
LOGS = ROOT / "logs"
FIGS = ROOT / "figures"
# (mkdir side effect removed in this copy: only the analyser / surface helpers are used)

SEED = 20260928
Y0, Y1 = 1995, 2022
NY = Y1 - Y0 + 1
FIELD_IDS = list(range(11, 37))            # the 26 OpenAlex fields; index k = fid - 11; vfield code = k + 1 (0 = unlabelled)
FIELD_NAMES = {11: "Agricultural and Biological Sciences", 12: "Arts and Humanities",
               13: "Biochemistry, Genetics and Molecular Biology", 14: "Business, Management and Accounting",
               15: "Chemical Engineering", 16: "Chemistry", 17: "Computer Science", 18: "Decision Sciences",
               19: "Earth and Planetary Sciences", 20: "Economics, Econometrics and Finance", 21: "Energy",
               22: "Engineering", 23: "Environmental Science", 24: "Immunology and Microbiology",
               25: "Materials Science", 26: "Mathematics", 27: "Medicine", 28: "Neuroscience", 29: "Nursing",
               30: "Pharmacology, Toxicology and Pharmaceutics", 31: "Physics and Astronomy", 32: "Psychology",
               33: "Social Sciences", 34: "Veterinary", 35: "Dentistry", 36: "Health Professions"}
# fixed before any data were seen (plan step 5)
GROUP_OF_FIELD = {17: "CS", 22: "Eng", 13: "BGM", 27: "Med", 29: "Med", 35: "Med", 36: "Med",
                  15: "PHYS", 16: "PHYS", 19: "PHYS", 21: "PHYS", 25: "PHYS", 31: "PHYS",
                  11: "LIFEENV", 23: "LIFEENV", 24: "LIFEENV", 28: "LIFEENV", 30: "LIFEENV", 34: "LIFEENV",
                  12: "SOC", 14: "SOC", 20: "SOC", 32: "SOC", 33: "SOC",
                  26: "MATHDEC", 18: "MATHDEC"}
DEV_GROUPS = ["CS", "Eng", "BGM", "Med"]
HELD_GROUPS = ["PHYS", "LIFEENV", "SOC", "MATHDEC"]
DOMAIN_OF = {11: "Life", 13: "Life", 24: "Life", 28: "Life", 30: "Life",
             12: "Social", 14: "Social", 18: "Social", 20: "Social", 32: "Social", 33: "Social",
             15: "Physical", 16: "Physical", 17: "Physical", 19: "Physical", 21: "Physical", 22: "Physical",
             23: "Physical", 25: "Physical", 26: "Physical", 31: "Physical",
             27: "Health", 29: "Health", 34: "Health", 35: "Health", 36: "Health"}
MTYPES = ["name_exact", "name_variant", "alias"]

# ----------------------------------------------------------------------------- analyser (verbatim from art_yrradSC27HtQ)
ES_STOP = set("a an and are as at be but by for if in into is it no not of on or such that the their then there "
              "these they this to was will with".split())
TOKEN_RE = re.compile(r"[^\W_]+(?:\.[^\W_]+)*", re.UNICODE)
_STEMMER = None


def _stem(w: str) -> str:
    global _STEMMER
    if _STEMMER is None:
        import snowballstemmer
        _STEMMER = snowballstemmer.stemmer("porter")
    return _cached_stem(w)


@lru_cache(maxsize=500_000)
def _cached_stem(w: str) -> str:
    return _STEMMER.stemWord(w)


def normalise(text: str) -> str:
    t = text.lower().replace("’", "'")
    t = re.sub(r"'s\b", "", t)
    return re.sub(r"[\-‐‑‒–—/]", " ", t)


def analyse(text: str) -> list[tuple[int, str]]:
    """(position, stem) for non-stop tokens; stop words keep their position slot (ES semantics)."""
    out = []
    for p, tok in enumerate(TOKEN_RE.findall(normalise(text))):
        if tok in ES_STOP:
            continue
        out.append((p, _stem(tok)))
    return out


def phrase_spec(phrase: str) -> tuple[tuple[int, str], ...]:
    a = analyse(phrase)
    if not a:
        return ()
    p0 = a[0][0]
    return tuple((p - p0, s) for p, s in a)


def spec_in(pos: dict[str, list[int]], spec) -> bool:
    """match_title logic for one spec against a title's {stem: [positions]} index."""
    if not spec:
        return False
    first = spec[0][1]
    for p0 in pos.get(first, ()):
        if all(p0 + off in pos.get(s, ()) for off, s in spec[1:]):
            return True
    return False


def title_pos(title: str) -> dict[str, list[int]]:
    pos: dict[str, list[int]] = {}
    for p, s in analyse(title):
        pos.setdefault(s, []).append(p)
    return pos


# ----------------------------------------------------------------------------- surface normalisation for Aho-Corasick
_WS = re.compile(r"\s+")
_NONWORD = re.compile(r"[^\w\s]")


def surf(text: str) -> str:
    """Surface normalisation used for AC keys AND titles: lowercase, possessive strip, hyphen/slash -> space,
    other punctuation -> space, collapse whitespace, pad with single spaces."""
    t = normalise(text)
    t = _NONWORD.sub(" ", t).replace("_", " ")
    return " " + _WS.sub(" ", t).strip() + " "


def surf_arrow(arr):
    """Vectorised (pyarrow) version of surf() for a string array."""
    import pyarrow.compute as pc
    t = pc.utf8_lower(pc.fill_null(arr, ""))
    t = pc.replace_substring(t, "’", "'")
    t = pc.replace_substring_regex(t, r"'s\b", "")
    t = pc.replace_substring_regex(t, r"[\-‐‑‒–—/]", " ")
    t = pc.replace_substring_regex(t, r"[^\w\s]|_", " ")
    t = pc.replace_substring_regex(t, r"\s+", " ")
    t = pc.utf8_trim_whitespace(t)
    return pc.binary_join_element_wise(pc.cast(" ", "string"), t, pc.cast(" ", "string"), "")


def plural_variants(form: str) -> set[str]:
    """Singular/plural variants of the LAST token (s | es | ies)."""
    toks = form.split(" ")
    last = toks[-1]
    out = {last}
    if len(last) >= 4:
        if last.endswith("ies"):
            out.add(last[:-3] + "y")
        elif last.endswith("es") and last[:-2].endswith(("s", "x", "z", "ch", "sh")):
            out.add(last[:-2])
        elif last.endswith("s") and not last.endswith("ss") and not last.endswith("us") and not last.endswith("is"):
            out.add(last[:-1])
        else:
            if last.endswith("y") and last[-2:-1] not in "aeiou":
                out.add(last[:-1] + "ies")
            elif last.endswith(("s", "x", "z", "ch", "sh")):
                out.add(last + "es")
            else:
                out.add(last + "s")
    return {" ".join(toks[:-1] + [v]) for v in out}


# ----------------------------------------------------------------------------- misc
def jdump(obj, path: Path) -> None:
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        if isinstance(o, float) and not math.isfinite(o):
            return None
        return str(o)

    def clean(o):
        if isinstance(o, dict):
            return {str(k): clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [clean(v) for v in o]
        if isinstance(o, float) and not math.isfinite(o):
            return None
        if isinstance(o, (np.floating,)):
            return None if not np.isfinite(o) else float(o)
        return o
    path.write_text(json.dumps(clean(obj), indent=1, default=conv))


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger


def add_deviation(key: str, text: str) -> None:
    p = RES / "deviations.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    d[key] = text
    p.write_text(json.dumps(d, indent=1))


def source_field_lut() -> tuple[np.ndarray, np.ndarray]:
    """(sorted source ids, vfield code 0..26) from art_yrradSC27HtQ results/source_field.parquet."""
    import pandas as pd
    p = RES / "source_field.parquet"
    if not p.exists():
        import shutil
        shutil.copy(ART3 / "results/source_field.parquet", p)
    sf = pd.read_parquet(p)
    sid = sf.source.to_numpy(np.int64)
    code = np.where(sf.field.isna(), 0, sf.field.fillna(11).astype(int) - 10).astype(np.int8)
    o = np.argsort(sid)
    return sid[o], code[o]


def works_files() -> list[tuple[int, str, int, int]]:
    man = json.loads((SNAP / "works_manifest.json").read_text())
    return [(i, f["url"].replace("s3://openalex/", ""), f["meta"]["content_length"], f["meta"]["record_count"])
            for i, f in enumerate(man["files"])]


# ----------------------------------------------------------------------------- split parquet storage (< 100 MB per file)
def write_parquet_parts(df, out_dir: Path, rows_per_part: int = 400_000) -> list[Path]:
    """Write a DataFrame as out_dir/part_001.parquet, part_002.parquet, ... (zstd). Existing parts are replaced."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for old in out_dir.glob("part_*.parquet"):
        old.unlink()
    paths = []
    for k, i in enumerate(range(0, max(len(df), 1), rows_per_part), start=1):
        p = out_dir / f"part_{k:03d}.parquet"
        df.iloc[i:i + rows_per_part].to_parquet(p, index=False, compression="zstd")
        paths.append(p)
    return paths


def read_parquet_parts(out_dir: Path, columns: list[str] | None = None):
    """Read the parts written by write_parquet_parts in sorted order and concatenate them."""
    import pandas as pd
    parts = sorted(out_dir.glob("part_*.parquet"))
    if not parts:
        raise FileNotFoundError(f"no parquet parts in {out_dir}")
    return pd.concat([pd.read_parquet(p, columns=columns) for p in parts], ignore_index=True)


RESERVOIR_DIR = SCAN / "reservoir"          # was scan/reservoir.parquet (136 MB)
SAMPLE_TITLES_DIR = SCAN / "sample_titles"  # was scan/sample_titles.parquet (152 MB)
