"""Frozen screen panel P78 (identical in every screen artifact) and the seeded processing order."""
from __future__ import annotations

import random

GROUPS = {
    "CS/AI": "extreme learning machine; compressed sensing/compressive sensing; crowdsourcing; cloud computing; deep belief network; dictionary learning; folksonomy; social tagging; Web 2.0; mashup; service-oriented architecture; MapReduce; NoSQL; cognitive radio; network coding; vehicular ad hoc network/VANET; wireless body area network; internet of things; cyber-physical system; sentiment analysis; latent Dirichlet allocation; differential privacy; learning to rank; microblog",
    "Engineering": "smart grid; microgrid; vehicle-to-grid; plug-in hybrid electric vehicle; energy harvesting; microbial fuel cell; carbon capture and storage; WiMAX; ZigBee; LTE-Advanced; virtual power plant; piezoelectric nanogenerator; memristor; ultra-wideband; demand response; structural health monitoring",
    "Biochem/Genetics": "induced pluripotent stem cell; optogenetics; ChIP-seq; RNA-seq; next-generation sequencing; copy number variation; genome-wide association study/GWAS; exome sequencing; long noncoding RNA/lncRNA; piRNA; synthetic biology; metagenomics; human microbiome; cancer stem cell; zinc finger nuclease; lipidomics; interactome; DNA barcoding; sirtuin; nanopore sequencing",
    "Medicine": "severe acute respiratory syndrome/SARS coronavirus; H5N1; pandemic H1N1/swine flu; transcatheter aortic valve implantation/TAVI; natural orifice transluminal endoscopic surgery/NOTES; single-incision laparoscopic surgery; drug-eluting stent; cardiac resynchronization therapy; HPV vaccine; biosimilar; pay for performance; comparative effectiveness research; patient-centered medical home; ribotype 027; chronic traumatic encephalopathy; mHealth; capsule endoscopy; takotsubo cardiomyopathy",
}

# aliases that are common English words when lower-cased: never sent to the (case-insensitive) search filter
NOT_SEARCHED = {"NOTES"}
ACRONYMS = {"GWAS", "VANET", "lncRNA", "TAVI", "SARS coronavirus", "NOTES"}
SEED = 20260928
DEV_FIELDS = ["Computer Science", "Engineering", "Biochemistry, Genetics and Molecular Biology", "Medicine"]


def panel() -> list[dict]:
    out = []
    for g, s in GROUPS.items():
        for item in s.split(";"):
            names = [x.strip() for x in item.split("/")]
            out.append({"canonical": names[0], "aliases": names, "panel_group": g})
    assert len(out) == 78, len(out)
    return out


def seeded_order() -> list[dict]:
    order = panel()[:]
    random.Random(SEED).shuffle(order)
    return order


def slug(name: str) -> str:
    return "".join(ch if ch.isalnum() else "_" for ch in name.lower()).strip("_")


def search_filter(c: dict) -> str:
    phrases = [a for a in c["aliases"] if a not in NOT_SEARCHED]
    return "title_and_abstract.search:" + "|".join(f'"{p}"' for p in phrases)


BASE_FILTER = "type:article|review,is_paratext:false"
