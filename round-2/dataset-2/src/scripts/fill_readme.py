#!/usr/bin/env python3
"""Fill the numeric placeholders of scripts/README.template.md from the final outputs -> README.md."""
import json

import pandas as pd

from common import OUT, ROOT, WORK

cov = json.loads((OUT / "coverage_report.json").read_text())["by_source"]
cal = json.loads((WORK / "wp_calibration.json").read_text())
cost = json.loads((OUT / "llm_cost.json").read_text())["total_usd"]
R = pd.read_pickle(WORK / "concept_rows.pkl")
t = R[R.level >= 2]
nonwiki = sum(1 for o in t.output if any(e["year_usable"] and e["source"] != "wikipedia_en" for e in o["events"]))
n_exact = sum(1 for line in (ROOT / "cache" / "wikipedia" / "first_rev.jsonl").open()
              if (r := json.loads(line)).get("first_rev_ts") and not r.get("error"))
lst = pd.read_parquet(WORK / "list_entries.parquet")
v = pd.read_parquet(WORK / "verifications.parquet")
yrs = cal.get("usable_estimated_years", [])
sub = {
    "LLM_SPEND": f"{cost:.2f}",
    "N_PW": f"{cov['physics_world_boty']['n_with_event']:,}",
    "N_RF": f"{cov['research_fronts']['n_with_event']:,}",
    "N_LISTS": f"{len(lst):,}",
    "N_VERIF": f"{len(v):,}",
    "N_NONWIKI": f"{nonwiki:,}",
    "N_WP": f"{cov['wikipedia_en']['n_with_event']:,}",
    "WP_EXACT": f"{n_exact:,}",
    "WP_SAME": f"{100 * cal['cv_share_same_calendar_year']:.1f}%",
    "WP_MED": f"{cal['cv_median_abs_err_years']:.3f}",
    "WP_P90": f"{cal['cv_p90_abs_err_years']:.2f}",
    "C_MESH": f"{cov['mesh']['n_with_event']:,}", "C_PACS": f"{cov['pacs_physh']['n_with_event']:,}",
    "C_ACM": f"{cov['acm_ccs']['n_with_event']:,}", "C_MSC": f"{cov['msc']['n_with_event']:,}",
    "C_WD": f"{cov['wikidata']['n_with_event']:,}", "C_GARTNER": f"{cov['gartner_hype_cycle']['n_with_event']:,}",
    "C_TR10": f"{cov['mit_tr10']['n_with_event']:,}", "C_SBOTY": f"{cov['science_boty']['n_with_event']:,}",
    "C_NM": f"{cov['nature_methods_moty']['n_with_event']:,}",
    "WP_MIN": json.loads((OUT / "qc_checks.json").read_text())["wikipedia_min_date"],
    "WP_YEARS": ", ".join(str(y) for y in yrs) if yrs else "none",
}
s = (ROOT / "scripts" / "README.template.md").read_text()
for k in sorted(sub, key=len, reverse=True):
    s = s.replace(k, sub[k])
(ROOT / "README.md").write_text(s)
print(json.dumps(sub, indent=1))
