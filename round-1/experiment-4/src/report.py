"""Figures for the G screen (matplotlib, PNG + PDF)."""
from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

plt.rcParams.update({"font.size": 9, "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False})
GROUPS = ["CS", "Eng", "BGM", "Med"]


def _save(fig, out: Path, name: str) -> None:
    fig.tight_layout()
    fig.savefig(out / f"{name}.png", dpi=200)
    fig.savefig(out / f"{name}.pdf")
    plt.close(fig)


def make_figures(b: dict, sr: dict, si: pd.DataFrame, nf: dict, out: Path) -> None:
    out.mkdir(exist_ok=True)
    f = np.array(b["fields"])
    g = np.array(b["gateway_eig"])
    o = np.argsort(g)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.barh(f[o], g[o], color="#4C72B0")
    ax.set_xlabel("eigenvector gateway centrality (max = 1), positive-PMI backbone 1998-2002")
    _save(fig, out, "gateway_centrality")

    P = np.array(b["pmi"], float)
    P[P < -50] = np.nan
    np.fill_diagonal(P, np.nan)
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(P, cmap="RdBu_r", vmin=-3, vmax=3)
    ax.set_xticks(range(26), [x[:22] for x in f], rotation=90, fontsize=6)
    ax.set_yticks(range(26), [x[:22] for x in f], fontsize=6)
    fig.colorbar(im, ax=ax, label="PMI of topic co-assignment (1998-2002)")
    _save(fig, out, "relatedness_heatmap")

    d = sr["delta_rho_O2r_m30"]
    rows = [(gname, d["per_group"][gname]["delta"], d["per_group"][gname]["n"]) for gname in GROUPS]
    fig, ax = plt.subplots(figsize=(5, 3))
    y = np.arange(len(rows) + 1)
    vals = [r[1] if r[1] is not None else np.nan for r in rows]
    ax.scatter(vals, y[:-1], color="#DD8452")
    ax.errorbar([d["delta"]], [y[-1]], xerr=[[d["delta"] - d["ci90"][0]], [d["ci90"][1] - d["delta"]]],
                fmt="D", color="black", capsize=3)
    ax.axvline(0, color="grey", lw=0.8)
    ax.axvline(0.10, color="grey", lw=0.8, ls="--")
    ax.set_yticks(y, [f"{r[0]} (n={r[2]})" for r in rows] + ["pooled (90% CI)"])
    ax.set_xlabel("Δρ (B5+G − B5), O2r m=30, LOGO")
    _save(fig, out, "delta_rho_forest")

    for yname, col in (("O2r_m30", "raw_"), ("O1", "oriented_"), ("O3", "oriented_")):
        s = si[si.outcome == yname]
        M = s[[f"{col}{gname}" for gname in GROUPS]].values.astype(float)
        pooled = s["pooled_spearman" if yname == "O2r_m30" else "pooled_raw_auc"].values.astype(float)[:, None]
        M = np.hstack([M, pooled])
        fig, ax = plt.subplots(figsize=(5, 8))
        center, span = (0, 1) if yname == "O2r_m30" else (0.5, 0.5)
        im = ax.imshow(M, cmap="RdBu_r", vmin=center - span, vmax=center + span, aspect="auto")
        ax.set_yticks(range(len(s)), s["indicator"], fontsize=7)
        ax.set_xticks(range(5), GROUPS + ["pooled"])
        for i in range(M.shape[0]):
            for j in range(M.shape[1]):
                if np.isfinite(M[i, j]):
                    ax.text(j, i, f"{M[i, j]:.2f}", ha="center", va="center", fontsize=6)
        fig.colorbar(im, ax=ax, label="Spearman" if yname == "O2r_m30" else "AUC (oriented on training groups)")
        ax.set_title(f"single indicators vs {yname}")
        _save(fig, out, f"single_indicator_heatmap_{yname}")

    pn = nf.get("all", {}).get("perm_null")
    if pn:
        fig, ax = plt.subplots(figsize=(5, 3))
        ax.hist(pn["values"], bins=30, color="#bbbbbb", label="permuted phi (1,000)")
        ax.axvline(nf["all"]["auc_density_mean"], color="#C44E52", label="observed density AUC")
        ax.axvline(nf["all"]["auc_size_mean"], color="#4C72B0", ls="--", label="field-size baseline AUC")
        ax.set_xlabel("mean within concept-step AUC of next-field entry")
        ax.legend(fontsize=7)
        _save(fig, out, "next_field_auc_null")
