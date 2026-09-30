#!/usr/bin/env python3
"""S5b: PRECISION GATE + TYPE (one call does both), second-model agreement, blind-check sheet.

M1 = google/gemini-2.5-flash-lite, temperature 0, 8 phrases per call, 20 titles per phrase (<= 200 chars) sampled with
seed 7919 + ci from the phrase's grounded papers in t0..t0+2 (open/early_frame.parquet). KEEP iff specific AND
sense_share >= 0.8 AND NOT generic. Budget: the gate may spend at most GATE_CAP of the artifact's $1.35 cap; phrases are
gated in a seeded random priority order (phrases with >= 10 home papers in t0..t0+2 first; outcome-blind), so if the
budget binds the gated frame is a random sample of the candidates (plan F5).
  estimate   run 40 phrases, extrapolate the cost -> results/gate_cost_estimate.json
  run        gate in priority order -> data/gate_m1.csv
  m2         M2 = openai/gpt-4.1-mini on 100 random gated phrases (stratified by group) [+ all M1 method/object
             phrases if --m2all and the budget allows] -> data/gate_m2.csv, results/gate_benchmark.json
  sheet      blind-check sheet (30 kept + 30 rejected, titles only) -> results/blind_check_sheet.json
  score      read results/blind_check_labels.json (executor labels) -> gate_benchmark.json; frame_n_concepts.csv
Usage: python s5_gate.py estimate|run|m2|sheet|score"""
from __future__ import annotations

import asyncio
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import aiohttp
import numpy as np
import pandas as pd

from common import DATA, RES, ROOT, jdump, setup_logger, sha256_file

logger = setup_logger("s5_gate")
M1 = "google/gemini-2.5-flash-lite"
M2 = "openai/gpt-4.1-mini"
BS = 8
N_TITLES = 20
TOTAL_CAP = 1.35
GATE_CAP = 1.00          # M1 gate share of the cap; the rest is for M2 + contingency
TYPES = ["method", "object", "property", "topic"]
SYSTEM = (
    "You are an expert scientific indexer. Each item is a candidate PHRASE mined automatically from publication "
    "titles, its ONSET year, and up to 20 titles (from its first years of use) that contain it. For each item decide:\n"
    "- specific: true only if the phrase itself names ONE specific scientific concept in English: a method, "
    "technique, tool, algorithm, instrument, material, compound, organism, disease, gene, device, phenomenon, "
    "measure, theory, or a well-defined research topic. false if it is a generic word combination (e.g. 'large "
    "sample', 'potential predictor'), a truncated fragment of a longer term, a person / place / organisation / "
    "event / project / journal-section name, a non-English phrase, a boilerplate title element, or an accidental word "
    "sequence.\n"
    "- sense_share: the fraction (0..1) of the given titles in which the phrase is used in that single concept sense.\n"
    "- type: one of method (a technique, tool, algorithm, instrument, assay, software, procedure or model class used "
    "to DO research), object (a thing that is studied: material, organism, disease, device studied as an object, "
    "molecule, gene, compound, phenomenon-entity, population), property (a measure, statistic, index, quantity, "
    "theory, law, principle or property), topic (a field, research area, application domain or problem area).\n"
    "- generic: 1 if the concept was in common scientific use well BEFORE the onset year (an established general "
    "term), else 0.\n"
    "- gloss: a definition in at most 12 words.\n"
    "Answer strictly as JSON: {\"labels\": [{\"id\": <id>, \"specific\": true|false, \"sense_share\": <0..1>, "
    "\"type\": \"method|object|property|topic\", \"generic\": 0|1, \"gloss\": \"...\"}, ...]} with one entry per item.")


def items_all() -> list[dict]:
    on = pd.read_csv(DATA / "frame_n_onset.csv")
    e = pd.read_parquet(ROOT / "open/early_frame.parquet", columns=["ci", "year", "work_id", "vfield", "title"])
    e = e.merge(on[["ci", "t0", "home"]], on="ci")
    e = e[(e.year >= e.t0) & (e.year <= e.t0 + 2)]
    homes = {r.ci: {int(float(x)) - 10 for x in str(r.home).split(";") if x} for r in on.itertuples()}
    e["is_home"] = [v in homes[c] for c, v in zip(e.ci, e.vfield)]
    nh = e.groupby("ci").is_home.sum()
    out = []
    for ci, g in e.groupby("ci"):
        rng = np.random.default_rng(7919 + int(ci))
        k = min(N_TITLES, len(g))
        pick = np.sort(rng.choice(len(g), size=k, replace=False))
        titles = [str(t)[:200] for t in g.title.to_numpy()[pick]]
        out.append({"ci": int(ci), "titles": titles, "n_home_early": int(nh.get(ci, 0))})
    meta = on.set_index("ci")
    for it in out:
        it["name"] = str(meta.at[it["ci"], "name"])
        it["t0"] = int(meta.at[it["ci"], "t0"])
        it["group"] = str(meta.at[it["ci"], "agroup"])
        it["extension"] = int(meta.at[it["ci"], "extension"])
    # seeded random priority order (outcome-blind): main-frame onsets (t0 <= 2014) before the t0 = 2015 extension,
    # and within each, phrases with >= 10 home papers in t0..t0+2 first, then the rest
    rng = np.random.default_rng(20260929)
    r = rng.permutation(len(out))
    order = sorted(range(len(out)), key=lambda i: (out[i]["extension"], out[i]["n_home_early"] < 10, r[i]))
    return [out[i] for i in order]


def messages(batch: list[dict]) -> list[dict]:
    lines = [json.dumps({"id": k, "phrase": it["name"], "onset_year": it["t0"], "titles": it["titles"]},
                        ensure_ascii=False) for k, it in enumerate(batch)]
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "Items (one JSON object per line):\n" + "\n".join(lines)}]


def run_model(items: list[dict], model: str, tag: str, cap: float, stop_at: float | None = None) -> pd.DataFrame:
    """Label items; phrases left unlabelled (truncated / unparseable responses) are retried up to 2 more rounds in
    batches of 4 with a round marker in the prompt (distinct cache key)."""
    out = []
    todo = list(items)
    for rnd in range(3):
        if not todo:
            break
        d = _run_round(todo, model, tag if rnd == 0 else f"{tag}_retry{rnd}", cap, stop_at, rnd)
        out.append(d)
        got = set(d.ci) if len(d) else set()
        todo = [it for it in todo if it["ci"] not in got]
        logger.info(f"round {rnd}: labelled {len(got)}; still unlabelled {len(todo)}")
    df = pd.concat([d for d in out if len(d)], ignore_index=True) if any(len(d) for d in out) else pd.DataFrame()
    return df.drop_duplicates("ci") if len(df) else df


def _run_round(items: list[dict], model: str, tag: str, cap: float, stop_at: float | None, rnd: int) -> pd.DataFrame:
    from llmc import LLM, BudgetStop, parse_json
    llm = LLM(concurrency=24, cap=cap)
    bs = BS if rnd == 0 else 4
    batches = [items[i:i + bs] for i in range(0, len(items), bs)]
    out = []
    spent0 = llm.spent
    logger.info(f"{model} {tag}: {len(items)} phrases in {len(batches)} calls; ledger so far ${spent0:.4f}; cap ${cap}")

    async def go():
        async with aiohttp.ClientSession() as sess:
            async def one(b):
                if llm.stopped or (stop_at is not None and llm.spent - spent0 >= stop_at):
                    return
                try:
                    msg = messages(b)
                    if rnd:
                        msg[1]["content"] += f"\n(round {rnd})"
                    txt = await llm.chat(sess, model, msg, tag, max_tokens=120 * len(b) + 200)
                except BudgetStop as e:
                    logger.error(f"budget refusal -> batch stopped: {e}")
                    return
                d = parse_json(txt)
                labs = d.get("labels", []) if isinstance(d, dict) else []
                for x in labs:
                    try:
                        k = int(x["id"])
                        if not 0 <= k < len(b):
                            continue
                        t = str(x.get("type", "")).strip().lower()
                        out.append({"ci": b[k]["ci"], "specific": bool(x.get("specific")),
                                    "sense_share": float(x.get("sense_share", math.nan)),
                                    "type": t if t in TYPES else None, "generic": int(x.get("generic", 0)),
                                    "gloss": str(x.get("gloss", ""))[:120], "model": model})
                    except (KeyError, TypeError, ValueError):
                        continue
            # chunks of 200 calls so a budget stop / stop_at is checked between chunks
            for s in range(0, len(batches), 200):
                if llm.stopped or (stop_at is not None and llm.spent - spent0 >= stop_at):
                    break
                await asyncio.gather(*(one(b) for b in batches[s:s + 200]))
                logger.info(f"  {tag}: {min(s + 200, len(batches))}/{len(batches)} calls, spent ${llm.spent:.4f}")
    asyncio.run(go())
    df = pd.DataFrame(out).drop_duplicates("ci") if out else pd.DataFrame(columns=["ci"])
    logger.info(f"{model} {tag}: labelled {len(df)} phrases; ledger total ${llm.spent:.4f} (this run "
                f"${llm.spent - spent0:.4f}); cache hits {llm.cache_hits}")
    return df


def keep_rule(df: pd.DataFrame, thr: float = 0.8) -> np.ndarray:
    return (df.specific.astype(bool) & (df.sense_share >= thr) & (df.generic == 0)).to_numpy()


def kappa(a, b) -> float:
    a, b = np.asarray(a), np.asarray(b)
    cats = sorted(set(a) | set(b))
    po = float(np.mean(a == b))
    pe = sum(float(np.mean(a == c)) * float(np.mean(b == c)) for c in cats)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def main() -> None:
    cmd = sys.argv[1]
    if cmd == "estimate":
        items = items_all()
        est = items[:40]
        from llmc import LLM
        before = LLM._ledger_total()
        df = run_model(est, M1, "gate_estimate", TOTAL_CAP)
        spent = LLM._ledger_total() - before
        per = spent / max(len(df), 1)
        res = {"n_items_total": len(items), "n_home_ge10": int(sum(i["n_home_early"] >= 10 for i in items)),
               "estimate_n": len(df), "estimate_cost": spent, "cost_per_phrase": per,
               "projected_all": per * len(items), "gate_cap": GATE_CAP,
               "n_affordable": int(GATE_CAP / per) if per > 0 else len(items)}
        jdump(res, RES / "gate_cost_estimate.json")
        logger.info(f"estimate: {res}")
    elif cmd == "run":
        items = items_all()
        est = json.loads((RES / "gate_cost_estimate.json").read_text())
        n = min(len(items), est["n_affordable"])
        df = run_model(items[:n], M1, "gate_m1", TOTAL_CAP, stop_at=GATE_CAP)
        meta = pd.DataFrame([{k: it[k] for k in ("ci", "name", "t0", "group", "n_home_early")} for it in items])
        meta["priority_rank"] = np.arange(len(meta))
        df = meta.merge(df, on="ci", how="left")
        df["gated"] = df.model.notna()
        df.loc[df.gated, "keep"] = keep_rule(df[df.gated])
        df.to_csv(DATA / "gate_m1.csv", index=False)
        logger.info(f"M1: gated {int(df.gated.sum())}/{len(df)}; keep {int(df.keep.fillna(False).sum())}; "
                    f"keep rate {df[df.gated].keep.mean():.3f}")
    elif cmd == "m2":
        g = pd.read_csv(DATA / "gate_m1.csv")
        g = g[g.gated]
        items = {it["ci"]: it for it in items_all()}
        rng = np.random.default_rng(101)
        per = max(1, 100 // g.group.nunique())
        samp = []
        for grp, d in g.groupby("group"):
            samp += list(rng.choice(d.ci.to_numpy(), size=min(per, len(d)), replace=False))
        rest = [c for c in rng.permutation(g.ci.to_numpy()) if c not in set(samp)]
        samp = (samp + rest)[:100]
        todo = [items[int(c)] for c in samp]
        extra = []
        if "--m2all" in sys.argv:
            mo = g[g.keep.astype(bool) & g.type.isin(["method", "object"])]
            extra = [items[int(c)] for c in mo.ci if int(c) not in set(samp)]
        d2 = run_model(todo + extra, M2, "gate_m2", TOTAL_CAP)
        d2["in_kappa_sample"] = d2.ci.isin(set(int(c) for c in samp))
        d2.to_csv(DATA / "gate_m2.csv", index=False)
        m = g.merge(d2, on="ci", suffixes=("_m1", "_m2"))
        ks = m[m.in_kappa_sample]
        k1 = keep_rule(ks.rename(columns={c + "_m1": c for c in ("specific", "sense_share", "generic")}))
        k2 = keep_rule(ks.rename(columns={c + "_m2": c for c in ("specific", "sense_share", "generic")}))
        both = ks[k1 & k2]
        res = {"n_kappa_sample": int(len(ks)), "kappa_keep": kappa(k1, k2), "agree_keep": float(np.mean(k1 == k2)),
               "n_type_both_kept": int(len(both)),
               "kappa_type": kappa(both.type_m1.fillna("na"), both.type_m2.fillna("na")),
               "agree_type": float(np.mean(both.type_m1 == both.type_m2)),
               "m2_all_method_object": bool(extra), "n_m2_total": int(len(d2))}
        p = RES / "gate_benchmark.json"
        b = json.loads(p.read_text()) if p.exists() else {}
        b["m1_m2"] = res
        jdump(b, p)
        logger.info(f"M1-M2: {res}")
    elif cmd == "m2rest":
        # D_consensus_gate: M2 on every M1-kept phrase not yet labelled by M2
        g = pd.read_csv(DATA / "gate_m1.csv")
        g = g[g.gated & g.keep.astype(bool)]
        d2 = pd.read_csv(DATA / "gate_m2.csv")
        items = {it["ci"]: it for it in items_all()}
        todo = [items[int(c)] for c in g.ci if int(c) not in set(d2.ci)]
        d3 = run_model(todo, M2, "gate_m2_rest", TOTAL_CAP)
        d3["in_kappa_sample"] = False
        pd.concat([d2, d3], ignore_index=True).drop_duplicates("ci").to_csv(DATA / "gate_m2.csv", index=False)
        logger.info(f"M2 rest: labelled {len(d3)} of {len(todo)}")
    elif cmd == "sheet2":
        # fresh blind sample for the consensus gate (30 consensus-kept + 10 M1-kept/M2-rejected), excluding sheet 1
        g = pd.read_csv(DATA / "gate_m1.csv")
        d2 = pd.read_csv(DATA / "gate_m2.csv")
        d2["keep2"] = keep_rule(d2)
        g = g[g.gated & g.keep.astype(bool)].merge(d2[["ci", "keep2"]], on="ci")
        seen = {x["ci"] for x in json.loads((RES / "blind_check_sheet.json").read_text())}
        g = g[~g.ci.isin(seen)]
        items = {it["ci"]: it for it in items_all()}
        rng = np.random.default_rng(707)
        a = rng.choice(g[g.keep2].ci.to_numpy(), 30, replace=False)
        b = rng.choice(g[~g.keep2].ci.to_numpy(), 10, replace=False)
        order = rng.permutation(np.concatenate([a, b]))
        sheet = [{"ci": int(c), "phrase": items[int(c)]["name"], "titles": items[int(c)]["titles"][:6]} for c in order]
        jdump(sheet, RES / "blind_check_sheet2.json")
    elif cmd == "sheet":
        g = pd.read_csv(DATA / "gate_m1.csv")
        g = g[g.gated]
        items = {it["ci"]: it for it in items_all()}
        rng = np.random.default_rng(606)
        kept = rng.choice(g[g.keep.astype(bool)].ci.to_numpy(), 30, replace=False)
        rej = rng.choice(g[~g.keep.astype(bool)].ci.to_numpy(), 30, replace=False)
        order = rng.permutation(np.concatenate([kept, rej]))
        sheet = [{"ci": int(c), "phrase": items[int(c)]["name"], "titles": items[int(c)]["titles"][:6]} for c in order]
        jdump(sheet, RES / "blind_check_sheet.json")
        logger.info(f"blind sheet written: {len(sheet)} phrases")
    elif cmd == "score":
        g = pd.read_csv(DATA / "gate_m1.csv")
        lab = json.loads((RES / "blind_check_labels.json").read_text())
        lab = pd.DataFrame(lab)
        m = lab.merge(g[["ci", "keep"]], on="ci")
        m["keep"] = m.keep.astype(bool)
        res = {"n": int(len(m)), "agreement": float(np.mean(m.keep == m.executor_keep)),
               "kappa": kappa(m.keep, m.executor_keep),
               "keep_precision_vs_executor": float(m[m.keep].executor_keep.mean()),
               "reject_npv_vs_executor": float((~m[~m.keep].executor_keep).mean()),
               "reader": "executor agent (an LLM), blind to the model label; NOT a human annotator"}
        thr = 0.8
        if res["keep_precision_vs_executor"] < 0.8:
            thr = 0.9
            res["rule_tightened"] = "keep-precision < 0.8 -> sense_share >= 0.9 (declared, before the freeze)"
        p = RES / "gate_benchmark.json"
        b = json.loads(p.read_text()) if p.exists() else {}
        b["blind_check"] = res
        b["sense_share_threshold"] = thr
        jdump(b, p)
        logger.info(f"blind check: {res}")
        # frame_n_concepts.csv
        on = pd.read_csv(DATA / "frame_n_onset.csv")
        g = g[g.gated].copy()
        g["keep"] = keep_rule(g, thr)
        m2p = DATA / "gate_m2.csv"
        fr = on.merge(g[["ci", "keep", "specific", "sense_share", "type", "generic", "gloss", "n_home_early",
                         "priority_rank"]], on="ci")
        if m2p.exists():
            d2 = pd.read_csv(m2p)[["ci", "type"]].rename(columns={"type": "type_m2"})
            fr = fr.merge(d2, on="ci", how="left")
        else:
            fr["type_m2"] = None
        fr["type_agree"] = fr.type == fr.type_m2
        fr["gate_model"] = M1 + " AND " + M2 + " (consensus, D_consensus_gate)"
        d2 = pd.read_csv(DATA / "gate_m2.csv")
        d2["keep_m2"] = keep_rule(d2, thr)
        fr = fr.merge(d2[["ci", "keep_m2"]], on="ci", how="left")
        fr["keep_m2"] = fr.keep_m2.fillna(False).astype(bool)
        n_m1 = int(fr.keep.sum())
        fr = fr[fr.keep & fr.keep_m2].drop(columns=["keep"])
        b = json.loads((RES / "gate_benchmark.json").read_text())
        b["consensus_gate"] = {"n_m1_kept": n_m1, "n_consensus_kept": int(len(fr)),
                               "rule": "keep iff M1 keep AND M2 keep (same rule, thr " + str(thr) + ")"}
        jdump(b, RES / "gate_benchmark.json")
        fr.to_csv(DATA / "frame_n_concepts.csv", index=False)
        logger.info(f"frame_n_concepts: {len(fr)} (main {int((fr.extension == 0).sum())}, "
                    f"extension {int((fr.extension == 1).sum())})")


if __name__ == "__main__":
    main()
