"""Frozen configuration shared by every module: the P78 dev panel, the S0 protocol constants,
the credit caps and all paths (derived from this file's location, never absolute)."""
from __future__ import annotations

import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "cache"
SNAP = ROOT / "snapshot"
RES = ROOT / "results"
LOGS = ROOT / "logs"
FIGS = ROOT / "figures"
for _d in (CACHE, SNAP, RES, LOGS, FIGS):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- P78 panel (verbatim from gen_strat_1)
# (name, [aliases], panel_group) -- panel_group is the strategy's a-priori label, NOT the measured home field.
_CS = ["extreme learning machine", ("compressed sensing", ["compressive sensing"]), "crowdsourcing", "cloud computing",
       "deep belief network", "dictionary learning", "folksonomy", "social tagging", "Web 2.0", "mashup",
       "service-oriented architecture", "MapReduce", "NoSQL", "cognitive radio", "network coding",
       ("vehicular ad hoc network", ["VANET"]), "wireless body area network", "internet of things",
       "cyber-physical system", "sentiment analysis", "latent Dirichlet allocation", "differential privacy",
       "learning to rank", "microblog"]
_ENG = ["smart grid", "microgrid", "vehicle-to-grid", "plug-in hybrid electric vehicle", "energy harvesting",
        "microbial fuel cell", "carbon capture and storage", "WiMAX", "ZigBee", "LTE-Advanced", "virtual power plant",
        "piezoelectric nanogenerator", "memristor", "ultra-wideband", "demand response", "structural health monitoring"]
_BIO = ["induced pluripotent stem cell", "optogenetics", "ChIP-seq", "RNA-seq", "next-generation sequencing",
        "copy number variation", ("genome-wide association study", ["GWAS"]), "exome sequencing",
        ("long noncoding RNA", ["lncRNA"]), "piRNA", "synthetic biology", "metagenomics", "human microbiome",
        "cancer stem cell", "zinc finger nuclease", "lipidomics", "interactome", "DNA barcoding", "sirtuin",
        "nanopore sequencing"]
_MED = [("severe acute respiratory syndrome", ["SARS coronavirus"]), "H5N1", ("pandemic H1N1", ["swine flu"]),
        ("transcatheter aortic valve implantation", ["TAVI"]),
        # alias 'NOTES' DROPPED (common English word under stemmed case-insensitive search) -> results/deviations.json
        ("natural orifice transluminal endoscopic surgery", []),
        "single-incision laparoscopic surgery", "drug-eluting stent", "cardiac resynchronization therapy",
        "HPV vaccine", "biosimilar", "pay for performance", "comparative effectiveness research",
        "patient-centered medical home", "ribotype 027", "chronic traumatic encephalopathy", "mHealth",
        "capsule endoscopy", "takotsubo cardiomyopathy"]


def _norm(e, grp):
    return (e[0], list(e[1]), grp) if isinstance(e, tuple) else (e, [], grp)


PANEL: list[tuple[str, list[str], str]] = ([_norm(e, "CS/AI") for e in _CS] + [_norm(e, "Engineering") for e in _ENG]
                                           + [_norm(e, "Biochem/Genetics") for e in _BIO]
                                           + [_norm(e, "Medicine") for e in _MED])
assert len(PANEL) == 78, len(PANEL)
_ORDER = list(range(78))
random.Random(20260928).shuffle(_ORDER)
ORDER: list[int] = _ORDER  # seeded processing order -> a credit-capped partial run is an unbiased prefix
DROPPED_ALIASES = [{"concept": "natural orifice transluminal endoscopic surgery", "alias": "NOTES",
                    "reason": "common English word; case-insensitive stemmed phrase search would match 'notes'"}]

# ---------------------------------------------------------------- S0 protocol constants
DEV_FIELDS = {17: "Computer Science", 22: "Engineering", 13: "Biochemistry, Genetics and Molecular Biology",
              27: "Medicine"}
GROUP_SHORT = {17: "CS", 22: "ENG", 13: "BIO", 27: "MED"}
BASEF = "type:article|review,is_paratext:false"
T0_MIN_COUNT = 20
DEV_T0 = (2003, 2009)
SRC_FIELD_SHARE = 0.40
HOME_SHARE = 0.40
RAREFY_M = 30
RAREFY_M_SENS = 50
SLICES = [(2000, 2004), (2005, 2009), (2010, 2014)]
SLICE_MID = [2002, 2007, 2012]
SAMPLE_N = 10_000
SEED = 20260928

# ---------------------------------------------------------------- economy
CREDIT_CAP = 1200
STOP_NEW_AT = 1150          # stop starting new concepts when used + 15 > this
RESERVE_STOP_REMAINING = 500   # anonymous per-IP pool is 1,000/day: never take it below half (siblings share the IP)
# The shared key's daily allowance was exhausted (x-ratelimit-remaining=0, reset ~11.7 h) when this artifact started,
# so API use is restricted to the S0 yearly counts on the public anonymous pool; everything else comes from the
# free S3 works snapshot (0 credits). See results/deviations.json.
API_SESSION_CAP = 175
N_THREADS = 6
N_NULL = 1000
N_BOOT = 2000
