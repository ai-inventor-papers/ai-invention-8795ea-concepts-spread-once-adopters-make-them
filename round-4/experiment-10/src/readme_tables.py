#!/usr/bin/env python3
"""Markdown tables for README.md, generated from results/*.json (no hand transcription)."""
import json
import math
from pathlib import Path

R = Path(__file__).resolve().parent / "results"
res = json.loads((R / "cohort_result.json").read_text())
sel = json.loads((R / "exp5_selection_result.json").read_text())


def f(x, d=3):
    return "NA" if x is None or (isinstance(x, float) and not math.isfinite(x)) else f"{x:+.{d}f}"


def ci(v):
    return f"[{f(v['ci'][0])}, {f(v['ci'][1])}]"


out = []
out.append("| build | outcome | " + " | ".join(f"R{i}" for i in range(6)) + " | n |")
out.append("|---|---|" + "---|" * 7)
for b in ("home", "all", "sizematch"):
    for y in ("O2r_m50", "O2r_resid"):
        cells = [f"{f(res['primary'][f'OPEN_{b}|{y}|R{i}']['rho'])} {ci(res['primary'][f'OPEN_{b}|{y}|R{i}'])}" for i in range(6)]
        out.append(f"| OPEN_{b} | {y} | " + " | ".join(cells) + f" | {res['primary'][f'OPEN_{b}|{y}|R0']['n']} |")
out.append("")
out.append("EXP5 selection data (2003-14 onsets; not confirmatory), O2r_m50:")
out.append("")
out.append("| build | " + " | ".join(f"R{i}" for i in range(6)) + " | n |")
out.append("|---|" + "---|" * 7)
for b in ("home", "all", "sizematch"):
    cells = [f"{f(sel['ladder'][f'OPEN_{b}|O2r_m50|R{i}']['rho'])} {ci(sel['ladder'][f'OPEN_{b}|O2r_m50|R{i}'])}" for i in range(6)]
    out.append(f"| OPEN_{b} | " + " | ".join(cells) + f" | {sel['ladder'][f'OPEN_{b}|O2r_m50|R0']['n']} |")
out.append("\n### Per group (R2, O2r_m50) and DerSimonian-Laird pooling\n")
out.append("| build | CS+Eng | BGM+Med | PHYS | LIFEENV | SOC | MATHDEC (report only) | DL pooled [95% CI] | I2 | positive / 5 |")
out.append("|---|---|---|---|---|---|---|---|---|---|")
for b in ("home", "all", "sizematch"):
    g = res["groups"][f"OPEN_{b}|O2r_m50|R2"]
    cells = [f"{f(g['groups'][k]['rho'])} (n={g['groups'][k]['n']})" for k in ("CS+Eng", "BGM+Med", "PHYS", "LIFEENV", "SOC", "MATHDEC")]
    out.append(f"| OPEN_{b} | " + " | ".join(cells) + f" | {f(g['DL']['b'])} {ci(g['DL'])} | {g['DL']['I2']:.2f} | {g['n_positive_of_5']} |")
out.append("\n### Within concept type (R3 without type dummies; method/object = M1 = M2 concepts only)\n")
out.append("| build | method | object | property | topic |")
out.append("|---|---|---|---|---|")
for b in ("home", "all", "sizematch"):
    cells = [f"{f(res['within_type'][f'OPEN_{b}|{t}|R3']['rho'])} {ci(res['within_type'][f'OPEN_{b}|{t}|R3'])} n={res['within_type'][f'OPEN_{b}|{t}|R3']['n']}" for t in ("method", "object", "property", "topic")]
    out.append(f"| OPEN_{b} | " + " | ".join(cells) + " |")
out.append("\n### The six components alone (O2r_m50, R2): cohort vs EXP5 selection\n")
out.append("| component (sign) | HOME cohort | HOME EXP5 | ALL cohort | ALL EXP5 |")
out.append("|---|---|---|---|---|")
sg = {"new_edge_rate": "+", "n_comm_W3": "+", "participation": "+", "NOV_res": "+", "ego_density_W3": "-", "edge_persistence": "-"}
for k in sg:
    c = [res["components"][f"{k}__home|O2r_m50|R2"], sel["components"][f"{k}__home|O2r_m50|R2"],
         res["components"][f"{k}__all|O2r_m50|R2"], sel["components"][f"{k}__all|O2r_m50|R2"]]
    out.append(f"| {k} ({sg[k]}) | " + " | ".join(f"{f(v['rho'])} {ci(v)}" for v in c) + " |")
out.append("\n### RETENTION_RATIO_early, Holm family, build contrasts\n")
out.append("| test | estimate [95% CI] | n |")
out.append("|---|---|---|")
for k, v in res["retention"].items():
    out.append(f"| {k} | {f(v['rho'])} {ci(v)} | {v['n']} |")
for k, v in res["contrasts"].items():
    out.append(f"| psp difference {k} (paired) | {f(v['diff'])} {ci(v)} | {v['n']} |")
out.append("")
out.append("| Holm family member (R2, one-sided bootstrap p) | p | Holm p |")
out.append("|---|---|---|")
for k, v in res["holm"].items():
    out.append(f"| {k} | {v['p_one']:.4f} | {v['p_holm']:.4f} |")
out.append("\n### Sensitivities (declared)\n")
out.append("| analysis | estimate [95% CI] | n |")
out.append("|---|---|---|")
for k, v in res["sensitivity"].items():
    if isinstance(v, dict) and "rho" in v:
        out.append(f"| {k} | {f(v['rho'])} {ci(v)} | {v['n']} |")
print("\n".join(out))
