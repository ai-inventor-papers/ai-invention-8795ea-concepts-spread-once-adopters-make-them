#!/usr/bin/env python3
"""End-to-end pipeline for the co-occurrence screen (candidates D and F vs the B5 baseline) on the P78 dev panel.

Steps (each idempotent / cached; re-running only redoes what is missing):
  1. s0_fetch        S0 yearly counts via the OpenAlex API (cached; 0 credits when cached)
  2. snapshot_meta   source->field venue labels and topic metadata from the free S3 snapshot
  3. scan_snapshot   zero-credit column-pruned scan of all 476M snapshot works (resumable)
  4. s0_outcomes     onset, dev restriction, outcomes O1/O2r/O3/R_j, B5 baseline
  5. backbone        full-corpus topic PMI backbone, Leiden communities, slice alignment
  6. features        ego networks, D and F (+nulls), secondaries, rivals, field-level features, split-half
  7. screen          LOGO ridge/logistic, concept bootstrap, selection rule, dissociation, portability
  8. extra_analyses  EXPLORATORY out-of-group partial association (not pre-registered, not used for selection)
  9. make_outputs    figures + method_out.json
Usage: .venv/bin/python method.py [--from STEP] [--n_boot 2000] [--workers 4]"""
from __future__ import annotations

import argparse
import json
import resource
import subprocess
import sys
import time

from loguru import logger

from config import DROPPED_ALIASES, LOGS, RES, ROOT

PY = sys.executable
STEPS = ["s0_fetch", "snapshot_meta", "scan_snapshot", "s0_outcomes", "backbone", "features", "screen",
         "extra_analyses", "make_outputs"]

DEVIATIONS = DROPPED_ALIASES + [
    {"id": "API_KEY_EXHAUSTED", "what": "The shared OpenAlex key had 0 credits left (x-ratelimit-remaining=0, reset "
     "~11.7 h) when this artifact started. API use was limited to the S0 yearly counts (78 concepts + global + OR test, "
     "156 credits in total) on the public per-IP anonymous pool (1,000/day; >= 800 left for siblings).",
     "consequence": "All other data (venue windows, ego networks, backbone, background prevalence) come from the free "
     "OpenAlex S3 works snapshot (2026-09-23; 476M works) at 0 credits."},
    {"id": "TITLE_GROUNDING_FOR_COMPOSITION", "what": "Venue-field compositions (home field, O2r, R_j, early "
     "off-home share/entropy/reach) and ego topic counts use TITLE-matched base works from the snapshot "
     "(OpenAlex-like analysis: lowercase, possessive strip, stop words with position gaps, Porter stemming, "
     "positional phrase match), not title+abstract matches, because abstracts are 43% of the snapshot bytes. "
     "t0, newborn, O1, O3, log volume and growth use the S0-exact API title+abstract counts.",
     "consequence": "Lower recall (see sanity.median_title_share_of_api_early), higher topical precision; field "
     "compositions are estimated from the papers that name the concept in the title."},
    {"id": "HOME_WINDOW_WIDENED", "what": "If fewer than 5 labelled title-matched papers exist in t0..t0+1, the home "
     "field is decided on t0..t0+2 (flag home_window in outcomes.csv)."},
    {"id": "FULL_CORPUS_BACKBONE", "what": "The backbone uses ALL base works of each slice (millions) instead of "
     "10k-work samples, and exact yearly background prevalence instead of slice-level log-linear interpolation "
     "(plan departures 2 and 3 are removed)."},
    {"id": "GAMMA_RULE", "what": "On the dense full-corpus backbone the plan's rule (gamma maximising median standard "
     "modularity) picks gamma=1, which leaves only ~8 communities of ~500 topics, outside the plan's expected 'tens to a "
     "few hundred' (T2). BEFORE any outcome was inspected, the primary gamma was redefined as the highest-median-Q gamma "
     "whose median number of non-trivial communities is >= 20; the plan-rule partition is reported as D_q."},
    {"id": "SELF_TOPIC_LEXICAL_RULE", "what": "A literal 'shares one content lemma' rule flagged generic topics as "
     "SELF (e.g. 'cell' -> 30 topics for iPSC, 'sensing' -> Remote Sensing for compressed sensing, 'comparative' -> "
     "legal studies). The lexical SELF rule was tightened (before outcomes were inspected) to: the topic name contains "
     "ALL content lemmas (lemma occurring in <= 100 topic names) of at least one of the concept's phrases; the >= 20% "
     "paper-share rule is unchanged. 16 of 47 dev concepts get a lexical self topic (e.g. compressed sensing -> "
     "'Sparse and Compressive Sensing Techniques')."},
    {"id": "D_PRIMARY_FALLBACK_T3", "what": "T3 STOP-AND-FIX fired: 70% of dev concepts have D_z < -5 and "
     "Spearman(D_z, M) = -0.69 (with log early volume -0.63): the frequency-matched null draws from all of science "
     "while real neighbours are topically concentrated, so z scales with M. Per the plan's pre-stated fallback, and "
     "decided on outcome-blind diagnostics only, the primary D is the one of D_ratio / D_rare with the smaller "
     "|Spearman| with M: D_ratio (obs distinct communities / null mean; 0.23 vs 0.29). D_z is still screened and "
     "reported as 'D_z_literal' (not ranked)."},
    {"id": "SPLIT_HALF_PAPER_LEVEL", "what": "Split-half reliability uses real paper-level random halves (paper topic "
     "lists are available from the snapshot) instead of binomial thinning of aggregate counts (plan departure 7)."},
    {"id": "EGO_WINDOWS_EXACT", "what": "Ego windows are exact paper sets per year, so first-appearance years of new "
     "neighbours are yearly (plan departure 4 no longer binds)."},
    {"id": "CENTRALITY_ON_KNN_BACKBONE", "what": "Betweenness/k-core/constraint of the inserted concept node are "
     "computed on a kNN-sparsified (top-10 PMI edges per topic), unweighted copy of the slice backbone, for runtime."},
    {"id": "COMPRESSED_SENSING_ALIAS", "what": "The OR-syntax test showed 'compressed sensing' and 'compressive "
     "sensing' return identical counts (same Porter stem), so the alias adds nothing; the pipe syntax was frozen."},
]


def run(step: str, extra: list[str]) -> None:
    t = time.time()
    cmd = [PY, str(ROOT / f"{step}.py")] + extra
    logger.info(f"=== {step}: {step}.py {' '.join(extra)}")
    r = subprocess.run(cmd, cwd=ROOT)
    if r.returncode != 0:
        raise RuntimeError(f"step {step} failed with exit code {r.returncode}")
    logger.info(f"=== {step} done in {(time.time() - t) / 60:.1f} min")


@logger.catch(reraise=True)
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start", default="s0_fetch", choices=STEPS)
    ap.add_argument("--to", dest="stop", default="make_outputs", choices=STEPS)
    ap.add_argument("--n_boot", type=int, default=2000)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / "method.log", rotation="30 MB", level="DEBUG")
    ram = 20 * 1024 ** 3  # container limit is 29 GB; the scan aggregates need < 6 GB
    resource.setrlimit(resource.RLIMIT_AS, (ram * 3, ram * 3))
    (RES / "deviations.json").write_text(json.dumps(DEVIATIONS, indent=1))
    todo = STEPS[STEPS.index(a.start): STEPS.index(a.stop) + 1]
    for s in todo:
        if s == "s0_fetch" and (RES / "yearly_counts_api.json").exists():
            logger.info("s0_fetch: cached results present, skipping (no credits)")
            continue
        if s == "snapshot_meta" and (RES / "source_field.parquet").exists():
            logger.info("snapshot_meta: present, skipping")
            continue
        extra = {"screen": ["--n_boot", str(a.n_boot), "--workers", str(a.workers)],
                 "features": ["--workers", str(a.workers)],
                 "scan_snapshot": ["--workers", "6"]}.get(s, [])
        run(s, extra)


if __name__ == "__main__":
    main()
