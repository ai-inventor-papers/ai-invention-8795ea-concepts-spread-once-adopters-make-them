"""Frozen P78 screen panel (identical across screen artifacts), seeded order and exact query strings."""
from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# Exactly as in the strategy direction (aliases after '/'), grouped by intended dev field.
PANEL_RAW = {
    "CS/AI": ["extreme learning machine", "compressed sensing/compressive sensing", "crowdsourcing", "cloud computing",
              "deep belief network", "dictionary learning", "folksonomy", "social tagging", "Web 2.0", "mashup",
              "service-oriented architecture", "MapReduce", "NoSQL", "cognitive radio", "network coding",
              "vehicular ad hoc network/VANET", "wireless body area network", "internet of things",
              "cyber-physical system", "sentiment analysis", "latent Dirichlet allocation", "differential privacy",
              "learning to rank", "microblog"],
    "Engineering": ["smart grid", "microgrid", "vehicle-to-grid", "plug-in hybrid electric vehicle", "energy harvesting",
                    "microbial fuel cell", "carbon capture and storage", "WiMAX", "ZigBee", "LTE-Advanced",
                    "virtual power plant", "piezoelectric nanogenerator", "memristor", "ultra-wideband",
                    "demand response", "structural health monitoring"],
    "Biochem/Genetics": ["induced pluripotent stem cell", "optogenetics", "ChIP-seq", "RNA-seq",
                         "next-generation sequencing", "copy number variation", "genome-wide association study/GWAS",
                         "exome sequencing", "long noncoding RNA/lncRNA", "piRNA", "synthetic biology", "metagenomics",
                         "human microbiome", "cancer stem cell", "zinc finger nuclease", "lipidomics", "interactome",
                         "DNA barcoding", "sirtuin", "nanopore sequencing"],
    "Medicine": ["severe acute respiratory syndrome/SARS coronavirus", "H5N1", "pandemic H1N1/swine flu",
                 "transcatheter aortic valve implantation/TAVI",
                 "natural orifice transluminal endoscopic surgery/NOTES", "single-incision laparoscopic surgery",
                 "drug-eluting stent", "cardiac resynchronization therapy", "HPV vaccine", "biosimilar",
                 "pay for performance", "comparative effectiveness research", "patient-centered medical home",
                 "ribotype 027", "chronic traumatic encephalopathy", "mHealth", "capsule endoscopy",
                 "takotsubo cardiomyopathy"],
}
PANEL = [c for g in PANEL_RAW.values() for c in g]
assert len(PANEL) == 78, len(PANEL)
INTENDED_GROUP = {c: g for g, cs in PANEL_RAW.items() for c in cs}

# Alias hygiene (logged deviation, identical for every concept)
DROPPED_ALIASES = {"natural orifice transluminal endoscopic surgery/NOTES": ["NOTES"]}
ADDED_ALIASES = {"natural orifice transluminal endoscopic surgery/NOTES":
                 ["natural orifice translumenal endoscopic surgery"]}


def name(c: str) -> str:
    return c.split("/")[0]


def aliases(c: str) -> list[str]:
    a = [x.strip() for x in c.split("/")]
    a = [x for x in a if x not in DROPPED_ALIASES.get(c, [])]
    return a + ADDED_ALIASES.get(c, [])


BASE_FILTER = "type:article|review,is_paratext:false"
OR_SYNTAX_OK = True  # set False by smoke test if boolean OR inside search fails


def search_value(c: str) -> str:
    return " OR ".join(f'"{a}"' for a in aliases(c))


def query(c: str) -> str:
    return f"title_and_abstract.search:{search_value(c)},{BASE_FILTER}"


def order() -> list[str]:
    o = list(PANEL)
    random.Random(20260928).shuffle(o)
    fp = ROOT / "panel_order.json"
    if not fp.exists():
        fp.write_text(json.dumps(o, indent=1))
    return o
