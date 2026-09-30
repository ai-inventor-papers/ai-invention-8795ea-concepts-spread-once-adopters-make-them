#!/usr/bin/env python3
"""Render the README results tables from results/rq1_heldout.json (between <!-- TABLES --> markers) and, with
--check, assert that every number printed in those README tables equals the JSON (T8 cross-check)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RES = ROOT / "results"


def f(v, d=3):
    return "NA" if v is None else f"{v:+.{d}f}"


def render() -> str:
    r = json.loads((RES / "rq1_heldout.json").read_text())
    out = []
    out.append("### Frozen top 10, scored once on the held-out groups (DL-pooled PHYS/LIFEENV/SOC/MATHDEC)\n")
    out.append("psp = partial Spearman given B5 (+ onset-year dummies); binary outcomes: dAUC over B5 with frozen DEV "
               "coefficients. `sign` = frozen DEV sign; `agree` = units (4 groups + 2 cohort parts) with that sign; "
               "**bold** = confirmed (Holm p < 0.05 within the outcome family and pooled sign = frozen sign).\n")
    for o, rows in r["heldout_summary"].items():
        out.append(f"\n**{o}**\n")
        out.append("| indicator | family | sign | pooled | 95% CI | I2 | Holm p | agree | cohort DEV-home / other |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for x in rows:
            if not x["in_top10"]:
                continue
            nm = f"**{x['indicator']}**" if x.get("confirmed") else x["indicator"]
            ps = " (prev. scored)" if x.get("previously_scored") else ""
            ci = x["pooled_ci"]
            out.append(f"| {nm}{ps} | {x['family']} | {'+' if x['frozen_sign'] > 0 else '-'} | {f(x['pooled'])} | "
                       f"[{f(ci[0])}, {f(ci[1])}] | {x['I2']:.2f} | {x.get('holm_p', float('nan')):.3g} | "
                       f"{x['sign_agree']}/{x['n_units']} | {f(x['per_unit'].get('COH_DEVHOME'))} / "
                       f"{f(x['per_unit'].get('COH_OTHER'))} |")
    out.append("\n### Learned models vs B5 vs B5 + best single (held-out groups pooled)\n")
    out.append("Spearman(pred, y) for continuous outcomes, AUC for binary; [95% CI of the paired difference vs B5].\n")
    out.append("| outcome | n | B5 | B5 + best single | ElasticNet / L1-logit (all) | EBM |")
    out.append("|---|---|---|---|---|---|")
    for o, d in r["learned_vs_single"].items():
        p = d.get("POOLED_HELDOUT", {})
        if "B5" not in p:
            continue

        def cell(k):
            if k not in p:
                return "NA"
            m = p[k].get("metric")
            if m is None:
                return "constant (all coef. 0)"
            if k == "B5":
                return f"{m:.3f}"
            ci = p[k].get("delta_ci") or [None, None]
            return f"{m:.3f} [{f(ci[0])}, {f(ci[1])}]"
        out.append(f"| {o} | {p['n']} | {cell('B5')} | {cell('B5_best_single')} | {cell('linear_all')} | {cell('EBM')} |")
    out.append("\n### Pre-registered predictions (frozen before the unseal)\n")
    out.append("| id | prediction | verdict |")
    out.append("|---|---|---|")
    from_spec = json.loads((RES / "frozen_spec.json").read_text())["preregistered_predictions"]
    for k, v in r["prereg_verdicts"].items():
        out.append(f"| {k} | {from_spec[k]} | **{v['verdict']}** |")
    return "\n".join(out) + "\n"


def main() -> None:
    readme = ROOT / "README.md"
    txt = readme.read_text()
    block = render()
    if "--check" in sys.argv:
        m = re.search(r"<!-- TABLES -->\n(.*?)<!-- /TABLES -->", txt, re.S)
        assert m, "tables block missing"
        assert m.group(1) == block, "README tables differ from results/rq1_heldout.json"
        print("T8 README cross-check: README tables == rq1_heldout.json")
        return
    if "<!-- TABLES -->" in txt:
        txt = re.sub(r"<!-- TABLES -->\n.*?<!-- /TABLES -->", lambda _: f"<!-- TABLES -->\n{block}<!-- /TABLES -->", txt,
                     flags=re.S)
    else:
        txt = txt.replace("<!-- RESULTS -->", f"<!-- RESULTS -->\n<!-- TABLES -->\n{block}<!-- /TABLES -->")
    readme.write_text(txt)
    print("README tables rendered")


if __name__ == "__main__":
    main()
