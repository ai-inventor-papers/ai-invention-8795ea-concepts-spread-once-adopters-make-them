#!/usr/bin/env python3
"""S8 MATCHED CASE PAIRS (most-similar design; rule frozen in results/frozen_spec.json before any outcome was read).
Pairs are matched on B5 volume and growth within a reporting group and onset window and are OPPOSITE on OPEN_all;
O2r is shown only after selection. ILLUSTRATION, NOT INFERENCE (n <= 8)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import cases_spec as CS  # noqa: E402
import viz  # noqa: E402
from common import (CASES, DATA, DISCLOSURE, DS2, E6, E8, E8_DATA, FIGS, RES, ROOT, REPORT_GROUPS, add_deviation,  # noqa: E402
                    jdump, load_outcomes, network_guard, setup_logger, update_status)

network_guard()
logger = setup_logger("s8_cases")
KEYS = ["new_edge_rate", "n_comm_W3", "participation", "NOV_res", "ego_density_W3", "edge_persistence"]


def base_table() -> pd.DataFrame:
    J = pd.read_parquet(DATA / "joined.parquet")
    O = pd.read_parquet(ROOT / "open_features.parquet").drop(columns=["split", "group", "rgroup", "med_home"])
    O = O.drop(columns=[c for c in O.columns if c in J.columns and c != "ci"])   # *_all duplicates (EXP8 values)
    pre = pd.read_parquet(DATA / "pre_onset.parquet")
    T = J.merge(O, on="ci").merge(pre, on="ci")
    T["generic"], T["generic_why"] = CS.generic_flags(T.name, T.pre_onset_papers, T.early_volume)
    for c in ("logvol", "growth_c"):
        T[f"z_{c}"] = (T[c] - T[c].mean()) / T[c].std(ddof=0)
    return T


def exemplar_ci() -> set[int]:
    d = json.loads((E8 / "results/case_exemplars.json").read_text())
    blocks = d if isinstance(d, list) else [d]
    return {int(r["ci"]) for b in blocks for side in ("high", "low") for r in b.get(side, [])}


def select_pairs(T: pd.DataFrame) -> tuple[list[dict], dict]:
    anchors = exemplar_ci()
    E = T[~T.generic & T.OPEN_home.notna() & T.OPEN_all.notna()].copy()
    E["q"] = E.groupby("rgroup").OPEN_all.transform(lambda s: pd.qcut(s.rank(method="first"), 5, labels=False))
    Cm = np.cov(T[["logvol", "growth_c", "offhome_share"]].to_numpy(float).T)
    Ci = np.linalg.inv(Cm)
    log = {"generic_excluded": int(T.generic.sum()), "generic_hits": T[T.generic][["ci", "name", "generic_why"]]
           .head(400).to_dict("records"), "anchors_available": sorted(anchors), "widened": [], "per_group": {}}
    used: set[int] = set()
    cand_by_group = {}
    for g in REPORT_GROUPS:
        Gd = E[E.rgroup == g]
        hi, lo = Gd[Gd.q == 4], Gd[Gd.q == 0]
        found = []
        for tol in (CS.CASE_RULE["tol"], CS.CASE_RULE["tol_wide"]):
            for h in hi.itertuples():
                ok = lo[(np.abs(lo.z_logvol - h.z_logvol) <= tol) & (np.abs(lo.z_growth_c - h.z_growth_c) <= tol)
                        & (np.abs(lo.t0 - h.t0) <= 2)]
                for l in ok.itertuples():
                    dv = np.array([h.logvol - l.logvol, h.growth_c - l.growth_c, h.offhome_share - l.offhome_share])
                    found.append({"hi": int(h.ci), "lo": int(l.ci), "gap": float(h.OPEN_all - l.OPEN_all),
                                  "maha": float(np.sqrt(dv @ Ci @ dv)), "tol": tol,
                                  "anchor": int(h.ci in anchors or l.ci in anchors)})
            if found:
                if tol > CS.CASE_RULE["tol"]:
                    log["widened"].append(g)
                break
        found.sort(key=lambda r: (-r["anchor"], -r["gap"], r["maha"]))
        cand_by_group[g] = found
        log["per_group"][g] = {"n_hi_pool": int(len(hi)), "n_lo_pool": int(len(lo)), "n_candidate_pairs": len(found)}
    pairs: list[dict] = []

    def take(g):
        for r in cand_by_group[g]:
            if r["hi"] not in used and r["lo"] not in used:
                used.update((r["hi"], r["lo"]))
                pairs.append({**r, "rgroup": g})
                return True
        return False
    for g in REPORT_GROUPS:                    # round 1: one pair per group
        take(g)
    for g in REPORT_GROUPS:                    # round 2: second pairs until max_pairs (CS+Eng at most 2)
        if len(pairs) >= CS.CASE_RULE["max_pairs"]:
            break
        take(g)
    log["n_pairs"] = len(pairs)
    log["groups_covered"] = sorted({p["rgroup"] for p in pairs})
    if log["widened"]:
        add_deviation("case_pairs_widened", f"no 0.25-SD match in {log['widened']}", "those pairs use a 0.35-SD match")
    if len(pairs) < CS.CASE_RULE["min_pairs"]:
        add_deviation("case_pairs_few", f"only {len(pairs)} valid pairs", "fewer illustrations")
    return pairs, log


def recognition(cids: list[int]) -> dict:
    o5 = pd.read_parquet(E8_DATA / "o5_events.parquet")
    o5 = o5[o5.concept_id.isin(cids) & (o5.relation == "same")]
    out = {int(c): d[["source", "event_type", "year", "year_usable"]].to_dict("records") for c, d in o5.groupby("concept_id")}
    # declared dependency cross-check (dataset 'concept_recognition'): count of events per concept
    dep = {}
    want = {f"C{c}" for c in cids}
    for p in sorted((DS2 / "full_data_out").glob("full_data_out_*.json")):
        try:
            d = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError) as e:
            logger.warning(f"dependency {p.name} unreadable: {e!r}")
            continue
        for ds in d.get("datasets", []):
            for ex in ds.get("examples", []):
                oid = str(ex.get("metadata_openalex_id", ""))
                if oid in want:
                    try:
                        ev = json.loads(ex["output"]).get("events", [])
                    except (json.JSONDecodeError, AttributeError, TypeError):
                        ev = []
                    dep[int(oid[1:])] = len(ev)
        del d
    return {"o5_events": out, "dependency_event_counts": dep}


def ego_ctx():
    import ego_open
    from ego_ctx import rq1_context
    ctx = rq1_context()
    ego_open.set_context(ctx)
    return ctx


def works_for(ci: int, em: pd.DataFrame, home: list[int], home_only: bool):
    d = em[em.ci == ci]
    if home_only:
        d = d[d.vfield.isin([h - 10 for h in home])]
    return list(zip(d.year.astype(int).tolist(), [tuple(t) for t in d.topics]))


@logger.catch(reraise=True)
def main() -> None:
    import ego_open
    O = load_outcomes().all()
    T = base_table()
    pairs, log = select_pairs(T)          # selection uses NO outcome column
    logger.info(f"selected {len(pairs)} pairs over {log['groups_covered']}")
    T = T.merge(O.drop(columns=["split"]), on="ci", how="left")
    Dd = pd.read_parquet(DATA / "decomp_inputs.parquet")
    ta = pd.concat([pd.read_parquet(RES / "typology_dev_assign.parquet"),
                    pd.read_parquet(RES / "typology_heldout_assign.parquet")])
    T = T.merge(Dd[["ci", "E2", "EH", "Bn"]], on="ci").merge(ta[["ci", "PC1"] + (["PC2"] if "PC2" in ta else [])], on="ci", how="left")
    codes = np.load(DATA / "state_codes.npy")
    ci_pos = {c: i for i, c in enumerate(pd.read_parquet(DATA / "joined.parquet").ci)}
    bb = json.loads((E6 / "inputs/field_backbone.json").read_text())
    comm = np.asarray(json.loads((RES / "field_communities.json").read_text())["labels"])
    order = np.lexsort((np.arange(26), comm))
    em = pd.read_parquet(E8_DATA / "frame_matches_early/part_001.parquet", columns=["ci", "year", "vfield", "topics"])
    em = em[em.ci.isin({p["hi"] for p in pairs} | {p["lo"] for p in pairs})]
    ctx = ego_ctx()
    rec = recognition([int(T.set_index("ci").concept_id[c]) for p in pairs for c in (p["hi"], p["lo"])])
    summary = []
    for k, p in enumerate(pairs, start=1):
        pid = f"pair{k:02d}_{p['rgroup'].replace('+', '')}"
        out = CASES / pid
        out.mkdir(parents=True, exist_ok=True)
        R = T.set_index("ci").loc[[p["hi"], p["lo"]]]
        fig, axes = __import__("matplotlib.pyplot").pyplot.subplots(2, 2, figsize=(9, 6.5),
                                                                     gridspec_kw={"height_ratios": [1, 1.6]})
        members = {}
        for j, (role, ci) in enumerate((("HIGH_OPEN", p["hi"]), ("LOW_OPEN", p["lo"]))):
            r = R.loc[ci]
            cc = codes[ci_pos[ci]]
            viz.state_flow(axes[0, j], np.where(cc == 4, -2, cc)[:, :].clip(-1, 3) if False else
                           np.where(cc == 4, 0, cc), f"{role}: {r['name']} (t0 {int(r.t0)})")
            viz.state_raster(axes[1, j], cc, order, bb["fields"], comm)
            if j == 1:
                axes[1, j].set_yticklabels([])
            snaps = {}
            home = [int(h) for h in str(r.home_list).split(";")]
            for build in ("all", "home"):
                w = works_for(ci, em, home, build == "home")
                snaps[build] = ego_open.concept_open(str(r["name"]), [], int(r.t0), w, keep_nb=True)
            members[role] = (ci, r, snaps)
            cid = int(r.concept_id)
            members[role] = members[role] + ({"events_same": rec["o5_events"].get(cid, []),
                                              "dependency_event_count": rec["dependency_event_counts"].get(cid)},)
        axes[0, 0].legend(loc="upper left", frameon=False, fontsize=7)
        fig.suptitle(f"Case pair {k} ({p['rgroup']}): matched on volume/growth, opposite OPEN_all "
                     f"(illustration, not inference)", fontsize=9)
        viz.save(fig, out / "flow_raster")
        # ego snapshots W1..W3 (all papers) + W3 home-only, both members
        plt = __import__("matplotlib.pyplot").pyplot
        fig, axes = plt.subplots(2, 4, figsize=(13, 6.2))
        snap_stats = {}
        for j, role in enumerate(("HIGH_OPEN", "LOW_OPEN")):
            ci, r, snaps, _ = members[role]
            t0 = int(r.t0)
            for w_i, w in enumerate(("W1", "W2", "W3")):
                s = snaps["all"]
                sl = __import__("ego").slice_of(t0 + w_i)
                snap_stats[f"{role}_{w}_all"] = viz.ego_snapshot(
                    axes[j, w_i], s["_nb"][w], s["_cnt"][w], s["_pmi"][w], ctx["full_edges"][sl], ctx["comm"][sl],
                    ctx["names"], (f"{role}: {r['name'][:30]}\n" if w_i == 0 else "\n") + f"{w} ({t0 + w_i}), all papers")
            s = snaps["home"]
            sl = __import__("ego").slice_of(t0 + 2)
            snap_stats[f"{role}_W3_home"] = viz.ego_snapshot(
                axes[j, 3], s["_nb"]["W3"], s["_cnt"]["W3"], s["_pmi"]["W3"], ctx["full_edges"][sl], ctx["comm"][sl],
                ctx["names"], f"\nW3 ({t0 + 2}), home-venue papers only")
        fig.suptitle(f"Case pair {k}: topic co-occurrence ego networks (nodes = PMI>0 neighbour topics, colour = EXP3 "
                     "Leiden community, size = count)", fontsize=9)
        viz.save(fig, out / "ego_snapshots")
        pj = {"pair": pid, "rgroup": p["rgroup"], "selection": {k2: p[k2] for k2 in ("gap", "maha", "tol", "anchor")},
              "illustration_only": True, "disclosure": DISCLOSURE, "members": {}}
        for role in ("HIGH_OPEN", "LOW_OPEN"):
            ci, r, snaps, recog = members[role]
            t0 = int(r.t0)
            ev = [dict(e, lag_to_t0=int(e["year"]) - t0, pre_t0=bool(int(e["year"]) < t0)) for e in recog["events_same"]]
            pj["members"][role] = {
                "ci": int(ci), "concept_id": int(r.concept_id), "name": r["name"], "group": r.group, "t0": t0,
                "home": r.home_list, "B5": {c: float(r[c]) for c in ("logvol", "growth_c", "offhome_share", "entropy", "reach")},
                "OPEN": {b: float(r[f"OPEN_{b}"]) if pd.notna(r[f"OPEN_{b}"]) else None for b in ("all", "home", "size")},
                "components": {b: {kk: (float(r[f"{kk}_{b}"]) if pd.notna(r[f"{kk}_{b}"]) else None) for kk in KEYS}
                               for b in ("all", "home", "size")},
                "decomposition": {"E2": float(r.E2), "EH": float(r.EH), "Bn": float(r.Bn),
                                  "M": float(r.EH / r.E2) if r.E2 > 0 else None,
                                  "rho": float(r.Bn / r.EH) if r.EH > 0 else None},
                "axis": {"PC1": float(r.PC1) if pd.notna(r.PC1) else None},
                "outcomes_shown_after_selection": {o: (float(r[o]) if pd.notna(r[o]) else None)
                                                   for o in ("O2r_m50", "O2r_resid", "O1c", "O1b", "O3", "O4")},
                "recognition_events_same": ev, "dependency_event_count": recog["dependency_event_count"],
                "top_W3_neighbours": [(ctx["names"][v], round(float(snaps["all"]["_pmi"]["W3"][v]), 2),
                                       int(snaps["all"]["_cnt"]["W3"][v]))
                                      for v in sorted(snaps["all"]["_nb"]["W3"],
                                                      key=lambda v: -np.nan_to_num(snaps["all"]["_pmi"]["W3"][v]))[:10]],
                "ego_snapshot_stats": {kk: v for kk, v in snap_stats.items() if kk.startswith(role)}}
        hi, lo = pj["members"]["HIGH_OPEN"], pj["members"]["LOW_OPEN"]
        oh = (hi["OPEN"]["home"], lo["OPEN"]["home"])
        pj["flag_open_home_order_disagrees"] = bool(oh[0] is not None and oh[1] is not None and oh[0] <= oh[1])
        a, b = hi["outcomes_shown_after_selection"]["O2r_resid"], lo["outcomes_shown_after_selection"]["O2r_resid"]
        pj["high_open_has_higher_O2r_resid"] = None if a is None or b is None else bool(a > b)
        jdump(pj, out / "pair.json")
        summary.append({"pair": pid, "rgroup": p["rgroup"], "high": hi["name"], "low": lo["name"],
                        "OPEN_all": [hi["OPEN"]["all"], lo["OPEN"]["all"]], "OPEN_home": list(oh),
                        "logvol": [hi["B5"]["logvol"], lo["B5"]["logvol"]], "O2r_resid": [a, b],
                        "Bn": [hi["decomposition"]["Bn"], lo["decomposition"]["Bn"]],
                        "E2": [hi["decomposition"]["E2"], lo["decomposition"]["E2"]],
                        "rho": [hi["decomposition"]["rho"], lo["decomposition"]["rho"]],
                        "high_open_higher_O2r_resid": pj["high_open_has_higher_O2r_resid"],
                        "open_home_order_disagrees": pj["flag_open_home_order_disagrees"]})
        logger.info(f"{pid}: {hi['name']} vs {lo['name']}; O2r_resid {a} vs {b}")
    ev = [s["high_open_higher_O2r_resid"] for s in summary if s["high_open_higher_O2r_resid"] is not None]
    res = {"rule": CS.CASE_RULE, "selection_log": log, "pairs": summary,
           "descriptive_summary": f"in {sum(ev)} of {len(ev)} pairs the high-OPEN member has the higher O2r_resid "
                                  "(no p-value; n <= 8; illustration only)",
           "disclosure": DISCLOSURE, "Source": "s8_cases.py; rule frozen in results/frozen_spec.json (case_pairs)"}
    jdump(res, RES / "case_pairs.json")
    # overview figure
    plt = __import__("matplotlib.pyplot").pyplot
    fig, ax = plt.subplots(figsize=(7, 0.5 + 0.45 * len(summary)))
    for i, s in enumerate(summary):
        y = len(summary) - 1 - i
        for j, (col, lab) in enumerate(((viz.OI["blue"], "high OPEN"), (viz.OI["orange"], "low OPEN"))):
            v = s["O2r_resid"][j]
            if v is not None:
                ax.scatter(v, y, color=col, s=30, zorder=3, label=lab if i == 0 else None)
        if None not in s["O2r_resid"]:
            ax.plot(s["O2r_resid"], [y, y], color="grey", lw=0.8)
        ax.text(ax.get_xlim()[0] if False else -0.02, y, f"{s['high'][:24]} / {s['low'][:24]} ({s['rgroup']})",
                transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=6)
    ax.axvline(0, color="black", lw=0.5)
    ax.set_yticks([])
    ax.set_xlabel("O2r_resid (breadth at t0+6..t0+8, volume-residualised) - shown AFTER selection")
    ax.legend(frameon=False, loc="lower right")
    ax.set_title("Matched case pairs: most-similar on B5 volume/growth, opposite on OPEN_all (illustration)", loc="left",
                 fontsize=8)
    viz.save(fig, FIGS / "fig_case_pairs")
    update_status("S8_case_pairs", {"case_pairs_summary": res["descriptive_summary"]})


if __name__ == "__main__":
    main()
