#!/usr/bin/env python3
"""S4: the EXP5 per-concept LLM precision gate, applied to the cohort candidates (verbatim EXP5 grounding.cmd_precision
logic: google/gemini-2.5-flash-lite, temperature 0, EXP5 SYSTEM prompt and batch_prompt, one call per concept with 10
grounded titles, +10 more if 7-8 of 10 are positive, pass at precision >= 0.8).

Only difference (outcome-blind by construction): titles are drawn from the candidate's grounded papers in
t0-3..t0+2 (Pass C early rows), ordered by a hash of the work id, instead of the EXP5 2003-2022 reservoir.

  u8     test: rebuild the EXP5 first-batch messages for 20 EXP5 concepts and check they hit the EXP5 cache
         (byte-identical prompt, model and parameters)
  run    label the candidates -> data/precision_cohort.csv and data/cohort_frame.csv
Usage: python s4_gate.py u8|run"""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))

import aiohttp
import numpy as np
import pandas as pd

from common import DATA, EXP5, INPUTS, RES, jdump, read_parquet_parts, setup_logger
from llmc import EXP5_CACHE, LLM, BudgetStop, batch_prompt, parse_json

logger = setup_logger("s4_gate")
M1 = "google/gemini-2.5-flash-lite"


def load_lex() -> pd.DataFrame:
    """EXP5 grounding.load_lex description rule (wd_description first, else description)."""
    lex = pd.read_parquet(INPUTS / "lexicon_v1.parquet", columns=["concept_id", "name", "description", "wd_description"])
    lex["desc"] = [(w if isinstance(w, str) and w else (d if isinstance(d, str) else ""))
                   for w, d in zip(lex.wd_description, lex.description)]
    return lex


def cache_key(model: str, messages: list[dict], temperature: float = 0.0) -> str:
    return hashlib.sha1(json.dumps([model, messages, temperature]).encode()).hexdigest() + ".json"


def cmd_u8() -> None:
    lex = load_lex()
    prec = pd.read_csv(EXP5 / "grounding_precision.csv")
    prec = prec[prec.precision_source == "llm"].sample(20, random_state=3)
    rs = read_parquet_parts(EXP5 / "scan/reservoir")
    rs = rs[rs.ci.isin(set(prec.ci)) & (rs.era >= 1) & (rs.tagstate == 1)].sort_values(["ci", "h"])
    hits = 0
    for ci, g in rs.groupby("ci"):
        f = g.head(10)
        items = [{"id": int(i), "name": lex["name"].iat[c], "description": lex.desc.iat[c], "title": t}
                 for i, c, t in zip(f.index, f.ci, f.title)]
        hits += int((EXP5_CACHE / cache_key(M1, batch_prompt(items))).exists())
    res = {"n": 20, "exp5_cache_hits": hits, "pass": hits == 20}
    jdump(res, RES / "u8_prompt_identity.json")
    logger.info(f"U8: {res}")


def cmd_run() -> None:
    lex = load_lex()
    cc = pd.read_csv(DATA / "cohort_candidates.csv")
    em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "work_id", "tagstate", "title"])
    em = em[(em.tagstate == 1) & em.ci.isin(set(cc.ci))].copy()
    em["h"] = [int(hashlib.sha1(f"gate:{w}".encode()).hexdigest()[:12], 16) for w in em.work_id]
    em = em.sort_values(["ci", "h"]).reset_index(drop=True)
    first = em.groupby("ci").head(10)
    second = em.groupby("ci").nth(slice(10, 20))
    order = cc.sample(frac=1, random_state=20260929).ci.tolist()   # seeded order: a budget stop leaves a random prefix
    llm = LLM(concurrency=32)

    def items(df):
        return [{"id": int(i), "name": lex["name"].iat[c], "description": lex.desc.iat[c], "title": t}
                for i, c, t in zip(df.index, df.ci, df.title)]

    async def run(df, tag):
        out = {}
        pos = {c: i for i, c in enumerate(order)}
        groups = [items(g) for _, g in sorted(df.groupby("ci"), key=lambda kv: pos.get(kv[0], 0))]
        async with aiohttp.ClientSession() as sess:
            async def one(its):
                if llm.stopped:
                    return
                try:
                    txt = await llm.chat(sess, M1, batch_prompt(its), tag, max_tokens=60 * len(its) + 100)
                except BudgetStop as e:
                    logger.error(f"budget refusal: {e}")
                    return
                d = parse_json(txt)
                for x in (d or {}).get("labels", []) if isinstance(d, dict) else []:
                    try:
                        out[int(x["id"])] = bool(x["refers_to_concept"])
                    except (KeyError, TypeError, ValueError):
                        continue
            await asyncio.gather(*(one(g) for g in groups))
        return out
    lab = asyncio.run(run(first, "prec:first"))
    first = first.assign(lab=first.index.map(lambda i: lab.get(int(i))))
    s1 = first.dropna(subset=["lab"]).groupby("ci").lab.agg(["sum", "size"])
    gray = s1[(s1["sum"] >= 0.7 * s1["size"]) & (s1["sum"] <= 0.8 * s1["size"]) & (s1["size"] >= 8)].index
    sec = second[second.ci.isin(gray)]
    lab2 = asyncio.run(run(sec, "prec:second")) if len(sec) else {}
    sec = sec.assign(lab=sec.index.map(lambda i: lab2.get(int(i))))
    allb = pd.concat([first, sec]).dropna(subset=["lab"])
    agg = allb.groupby("ci").lab.agg(["sum", "size"]).rename(columns={"sum": "n_pos", "size": "n_labelled_prec"})
    out = cc[["ci"]].merge(agg, left_on="ci", right_index=True, how="left")
    out["precision_c"] = out.n_pos / out.n_labelled_prec
    out["precision_source"] = np.where(out.n_labelled_prec.notna(), "llm", "none")
    out.to_csv(DATA / "precision_cohort.csv", index=False)
    fr = cc.merge(out[["ci", "precision_c", "n_labelled_prec", "precision_source"]], on="ci")
    fr["pass_gate"] = fr.precision_c >= 0.8
    fr["intersection_born"] = fr.intersect40.astype(int)
    fr.rename(columns={"concept_id": "openalex_id", "name": "label"}).to_csv(DATA / "cohort_candidates_gated.csv",
                                                                           index=False)
    summ = {"n_candidates": int(len(cc)), "n_labelled": int(out.n_labelled_prec.notna().sum()),
            "n_second_round": int(len(gray)), "pass_rate": float(fr.pass_gate.mean()),
            "pass_by_t0": fr.groupby("t0").pass_gate.agg(["sum", "size"]).to_dict(orient="index"),
            "llm_spent_total_usd": llm.spent, "calls": llm.n_calls, "cache_hits": llm.cache_hits}
    jdump(summ, RES / "s4_gate_summary.json")
    logger.info(f"S4: {summ}")




def cmd_retry() -> None:
    """Concepts with no parsable gate label: one retry with the same first-10 titles split into two calls of 5
    (new messages, hence a fresh call); declared deviation (EXP5 used a MiniLM sense-filter fallback instead)."""
    lex = load_lex()
    pc_ = pd.read_csv(DATA / "precision_cohort.csv")
    miss = set(pc_.ci[pc_.precision_c.isna()])
    em = pd.read_parquet(DATA / "passC_early.parquet", columns=["ci", "year", "work_id", "tagstate", "title"])
    em = em[(em.tagstate == 1) & em.ci.isin(miss)].copy()
    em["h"] = [int(hashlib.sha1(f"gate:{w}".encode()).hexdigest()[:12], 16) for w in em.work_id]
    first = em.sort_values(["ci", "h"]).reset_index(drop=True).groupby("ci").head(10)
    llm = LLM(concurrency=16)
    lab = {}

    async def run():
        async with aiohttp.ClientSession() as sess:
            async def one(its):
                try:
                    txt = await llm.chat(sess, M1, batch_prompt(its), "prec:retry", max_tokens=60 * len(its) + 100)
                except BudgetStop as e:
                    logger.error(f"budget refusal: {e}")
                    return
                d = parse_json(txt)
                for x in (d or {}).get("labels", []) if isinstance(d, dict) else []:
                    try:
                        lab[int(x["id"])] = bool(x["refers_to_concept"])
                    except (KeyError, TypeError, ValueError):
                        continue
            groups = []
            for _, g in first.groupby("ci"):
                its = [{"id": int(i), "name": lex["name"].iat[c], "description": lex.desc.iat[c], "title": t}
                       for i, c, t in zip(g.index, g.ci, g.title)]
                groups += [its[:5], its[5:]]
            await asyncio.gather(*(one(g) for g in groups if g))
    asyncio.run(run())
    first = first.assign(lab=first.index.map(lambda i: lab.get(int(i)))).dropna(subset=["lab"])
    agg = first.groupby("ci").lab.agg(["sum", "size"])
    for ci, r in agg.iterrows():
        m = pc_.ci == ci
        pc_.loc[m, "n_pos"] = r["sum"]
        pc_.loc[m, "n_labelled_prec"] = r["size"]
        pc_.loc[m, "precision_c"] = r["sum"] / r["size"]
        pc_.loc[m, "precision_source"] = "llm_retry"
    pc_.to_csv(DATA / "precision_cohort.csv", index=False)
    g = pd.read_csv(DATA / "cohort_candidates_gated.csv").drop(columns=["precision_c", "n_labelled_prec",
                                                                         "precision_source", "pass_gate"])
    g = g.merge(pc_[["ci", "precision_c", "n_labelled_prec", "precision_source"]], on="ci")
    g["pass_gate"] = g.precision_c >= 0.8
    g.to_csv(DATA / "cohort_candidates_gated.csv", index=False)
    from common import add_deviation
    add_deviation("precision_gate_retry", f"{len(miss)} candidates had no parsable gate label; one retry (2 calls of 5 "
                                          f"titles) labelled {len(agg)}; remaining unlabelled are excluded "
                                          "(no MiniLM sense-filter fallback in this artifact)")
    logger.info(f"retry: {len(miss)} missing -> {len(agg)} labelled; pass rate now {g.pass_gate.mean():.3f}; "
                f"by t0 {g.groupby('t0').pass_gate.sum().to_dict()}")


if __name__ == "__main__":
    {"u8": cmd_u8, "run": cmd_run, "retry": cmd_retry}[sys.argv[1]]()
