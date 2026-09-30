"""Plot helpers shared by the case pairs (S8), the atlas (S9) and the summary figures (S10): house style, state
flows (stacked ribbons), field x age state rasters and topic ego-network snapshots."""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

plt.rcParams.update({"pdf.fonttype": 42, "ps.fonttype": 42, "font.size": 9, "axes.titlesize": 10,
                     "axes.labelsize": 9, "legend.fontsize": 8, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.dpi": 150, "savefig.bbox": "tight"})
# Okabe-Ito colourblind-safe palette
OI = {"blue": "#0072B2", "orange": "#E69F00", "green": "#009E73", "vermillion": "#D55E00", "sky": "#56B4E9",
      "purple": "#CC79A7", "yellow": "#F0E442", "grey": "#999999", "black": "#000000"}
STATE_COL = {0: "#EEEEEE", 1: OI["sky"], 2: OI["blue"], 3: OI["vermillion"], 4: OI["grey"], -1: "#FFFFFF"}
STATE_LAB = {0: "untouched", 1: "entered", 2: "retained", 3: "lost", 4: "home"}


def save(fig, path_no_ext) -> list[str]:
    out = []
    for ext in ("png", "pdf"):
        p = f"{path_no_ext}.{ext}"
        fig.savefig(p, dpi=200 if ext == "png" else None)
        out.append(p)
    plt.close(fig)
    return out


def state_flow(ax, codes: np.ndarray, title: str) -> None:
    """codes [ages, 26] state codes for one concept -> stacked ribbons of off-home field counts per state."""
    ages = np.arange(codes.shape[0])
    valid = (codes >= 0).all(1)
    base = np.zeros(len(ages))
    for s in (2, 1, 3, 0):
        c = np.where(valid, (codes == s).sum(1), np.nan)
        ax.fill_between(ages, base, base + c, color=STATE_COL[s], label=STATE_LAB[s], step=None, lw=0.3,
                        edgecolor="white")
        base = base + np.nan_to_num(c)
    ax.set_xlim(0, ages[-1])
    ax.set_xlabel("age (years since onset t0)")
    ax.set_ylabel("off-home fields")
    ax.set_title(title, loc="left")


def state_raster(ax, codes: np.ndarray, order: np.ndarray, field_names: list[str], comm: np.ndarray) -> None:
    from matplotlib.colors import ListedColormap
    cm = ListedColormap([STATE_COL[s] for s in (-1, 0, 1, 2, 3, 4)])
    M = codes[:, order].T + 1
    ax.imshow(M, aspect="auto", cmap=cm, vmin=0, vmax=5, interpolation="nearest")
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([field_names[i][:22] for i in order], fontsize=5)
    ax.set_xticks(range(codes.shape[0]))
    ax.set_xlabel("age")
    for j in range(1, len(order)):
        if comm[order[j]] != comm[order[j - 1]]:
            ax.axhline(j - 0.5, color="black", lw=0.4)


def ego_snapshot(ax, nb: list[int], cnt: np.ndarray, pmi: np.ndarray, edges: tuple[np.ndarray, np.ndarray],
                 comm: np.ndarray, names: list[str], title: str, seed: int = 0) -> dict:
    import networkx as nx
    ax.set_axis_off()
    ax.set_title(title, loc="left", fontsize=7)
    if len(nb) == 0:
        ax.text(0.5, 0.5, "no neighbours", ha="center", va="center", transform=ax.transAxes, fontsize=7)
        return {"n_nodes": 0, "n_edges": 0}
    ins = np.zeros(len(cnt), bool)
    ins[nb] = True
    a, b = edges
    m = ins[a] & ins[b]
    G = nx.Graph()
    G.add_nodes_from(nb)
    G.add_edges_from(zip(a[m].tolist(), b[m].tolist()))
    pos = nx.spring_layout(G, seed=seed, k=1.2 / max(1, np.sqrt(len(nb))))
    cmap = plt.get_cmap("tab20")
    cols = [cmap(int(comm[v]) % 20) for v in G.nodes]
    sizes = [12 + 10 * float(cnt[v]) for v in G.nodes]
    nx.draw_networkx_edges(G, pos, ax=ax, width=0.3, alpha=0.4)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=cols, node_size=sizes, linewidths=0)
    top = sorted(nb, key=lambda v: -np.nan_to_num(pmi[v]))[:10]
    for v in top:
        ax.text(pos[v][0], pos[v][1], names[v][:26], fontsize=4.2, ha="center", va="bottom")
    return {"n_nodes": G.number_of_nodes(), "n_edges": G.number_of_edges(),
            "n_communities": int(len({int(comm[v]) for v in nb})),
            "density": float(nx.density(G)) if G.number_of_nodes() > 1 else None}
