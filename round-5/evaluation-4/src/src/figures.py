#!/usr/bin/env python3
"""Item 11 figure: forest plot of OPEN_home and NOVCHURN_home (R2, O2r_m50) per body, from results/evidence_synthesis.json.
Hand-written with the aii-data-fig-gen house style (its `forest` type takes symmetric errors only; these bootstrap
CIs are asymmetric and the markers must encode design status). Marker: filled = confirmatory, hollow =
already-unsealed, grey = selection; diamonds = non-selection DL pool with HKSJ interval (thin line); dashed empty row =
Frame N (pending). Usage: python src/figures.py"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import os  # noqa: E402

# optional: the aii-data-fig-gen house style (set AII_FIG_SKILL_SCRIPTS to its scripts/ dir); plain matplotlib otherwise
if os.environ.get("AII_FIG_SKILL_SCRIPTS"):
    sys.path.insert(0, os.environ["AII_FIG_SKILL_SCRIPTS"])

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

from paths import FIG, RES

try:
    from chart_geometry import assert_text_is_legible
    from chart_style import PALETTE, apply_house_style, fit_tick_labels, fit_titles
    HOUSE = True
except ImportError:  # skill not present outside the pipeline image
    HOUSE = False
    PALETTE = ["#0173B2", "#DE8F05", "#029E73"]

ORDER = [("B1_DEV", "EXP5 DEV (2003-09)"), ("B2_PHYS", "held-out PHYS"), ("B2_LIFEENV", "held-out LIFEENV"),
         ("B2_SOC", "held-out SOC"), ("B2_MATHDEC", "held-out MATHDEC"),
         ("B3_EXP5_COHORT_2010_14", "EXP5 cohort 2010-14"), ("B4_COHORT_2015_17", "cohort 2015-17 (Exp10)")]


def main() -> None:
    s = json.loads((RES / "evidence_synthesis.json").read_text())
    rows = {(r["body"], r["feature"]): r for r in s["rows"]}
    if HOUSE:
        apply_house_style()
    fig, axes = plt.subplots(1, 2, figsize=(6.5, 4.4), sharey=False, layout="constrained")
    for ax, f in zip(axes, ("OPEN_home", "NOVCHURN_home")):
        labels = []
        y = 0
        for b, lab in ORDER:
            r = rows[(b, f)]
            p = r["R2"]
            st = r["status"]
            col = "0.55" if st.startswith("selection") else PALETTE[0]
            face = col if st in ("confirmatory",) or st.startswith("selection") else "white"
            ax.plot(p["ci"], [y, y], color=col, lw=1.4, zorder=2)
            ax.plot([p["psp"]], [y], marker="o", ms=6, mec=col, mfc=face, mew=1.4, ls="none", zorder=3)
            labels.append(lab)
            ax.annotate(f"n={p['n']}", (1.0, y), xycoords=("axes fraction", "data"), xytext=(-3, 0),
                        textcoords="offset points", ha="right", va="center", fontsize=8, color="0.3")
            y += 1
        pool = s["pools"][f"{f}|R2"]["nonselection"]
        ax.plot(pool["hksj_ci"], [y + 0.28, y + 0.28], color=PALETTE[1], lw=0.9, zorder=2)
        ax.plot(pool["dl_ci"], [y, y], color=PALETTE[1], lw=2.2, zorder=2)
        ax.plot([pool["est"]], [y], marker="D", ms=7, color=PALETTE[1], ls="none", zorder=3)
        labels.append("pool, non-selection")
        ax.annotate(f"k={pool['k']}", (1.0, y), xycoords=("axes fraction", "data"), xytext=(-3, 0),
                    textcoords="offset points", ha="right", va="center", fontsize=8, color="0.3")
        y += 1
        ax.axhspan(y - 0.35, y + 0.35, fill=False, ls="--", lw=0.8, ec="0.5")
        labels.append("Frame N (pending)")
        ax.axvline(0, color="0.2", lw=0.8, zorder=1)
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels if f == "OPEN_home" else [])
        lo, hi = ax.get_xlim()
        ax.set_xlim(lo, hi + 0.12 * (hi - lo))
        ax.set_ylim(len(labels) - 0.5, -0.5)
        ax.set_xlabel("partial Spearman, R2 (95% CI)")
        ax.set_title(f)
    handles = [Line2D([], [], marker="o", color="0.55", mfc="0.55", ls="none", label="selection"),
               Line2D([], [], marker="o", color=PALETTE[0], mfc="white", ls="none", label="already-unsealed"),
               Line2D([], [], marker="o", color=PALETTE[0], mfc=PALETTE[0], ls="none", label="confirmatory"),
               Line2D([], [], marker="D", color=PALETTE[1], ls="none", label="DL pool (thin line below: HKSJ)")]
    fig.legend(handles=handles, loc="outside lower center", ncol=4, frameon=False)
    if HOUSE:
        fit_tick_labels(fig)
        fit_titles(fig)
        assert_text_is_legible(fig)
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / "evidence_forest.pdf")
    fig.savefig(FIG / "evidence_forest.png", dpi=200)
    print("wrote figures/evidence_forest.pdf|png")


if __name__ == "__main__":
    main()
