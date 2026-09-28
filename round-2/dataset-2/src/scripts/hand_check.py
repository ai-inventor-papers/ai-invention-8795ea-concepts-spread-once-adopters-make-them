#!/usr/bin/env python3
"""Merge the executor's hand verdicts with the 60-item sample and summarise model accuracy against them."""
import json

import pandas as pd

from common import OUT, ROOT, WORK

ACC = {"same", "narrower_entry", "broader_entry"}
REL = {"narrower": "narrower_entry", "broader": "broader_entry", "same": "same"}
h = pd.read_csv(WORK / "hand_check_sample.csv")
v = json.loads((ROOT / "scripts" / "hand_check_verdicts.json").read_text())
h["hand"] = v["verdicts"]
h["model_a"] = h.model_a.map(lambda x: REL.get(x, x))
h["a_exact"] = h.model_a == h.hand
h["a_accept_agree"] = h.model_a.isin(ACC) == h.hand.isin(ACC)
h["b_exact"] = h.model_b == h.hand
h["b_accept_agree"] = h.model_b.isin(ACC) == h.hand.isin(ACC)
h.to_csv(OUT / "hand_check.csv", index=False)
s = {}
for kind, g in h.groupby("kind"):
    s[kind] = {"n": int(len(g)), "primary_relation_exact": float(g.a_exact.mean()),
               "primary_accept_decision_agrees": float(g.a_accept_agree.mean())}
    if kind == "disagreement":
        s[kind].update({"second_relation_exact": float(g.b_exact.mean()), "second_accept_decision_agrees": float(g.b_accept_agree.mean())})
    else:
        s[kind]["precision_of_accepted_links_vs_hand"] = float(g.hand.isin(ACC).mean())
agr = json.loads((OUT / "llm_agreement.json").read_text())
agr["hand_check_60"] = s
(OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
print(json.dumps(s, indent=1))

# second sample: 30 random accepted curated-list links after the v2 (gpt-4.1-mini) re-verification
h2 = pd.read_csv(WORK / "hand_check_lists_v2.csv")
h2["hand"] = json.loads((ROOT / "scripts" / "hand_check_lists_v2_verdicts.json").read_text())["verdicts"]
h2["model"] = h2.relation.map(lambda x: REL.get(x, x))
h2["kind"] = "lists_v2_random_accepted"
h2.to_csv(OUT / "hand_check_lists_v2.csv", index=False)
s2 = {"n": int(len(h2)), "precision_of_accepted_links_vs_hand": float(h2.hand.isin(ACC).mean()),
      "relation_exact": float((h2.model == h2.hand).mean()),
      "precision_of_same_links": float((h2[h2.model == "same"].hand == "same").mean()),
      "n_same_links": int((h2.model == "same").sum())}
agr = json.loads((OUT / "llm_agreement.json").read_text())
agr["hand_check_lists_v2_30"] = s2
(OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
print(json.dumps(s2, indent=1))

# direction-robust agreement: same | hierarchical (narrower or broader) | reject (related/different)
from s7_verify import kappa  # noqa: E402

v = pd.read_parquet(WORK / "verifications.parquet")
three = lambda x: "same" if x == "same" else ("hier" if x in ("narrower_entry", "broader_entry") else "reject")
p = v[v.task.isin(["verify", "audit"]) & ~v.status.str.contains("reused")].drop_duplicates(["entry_id", "openalex_id", "task"])
q = v[v.task.str.startswith("double_")].copy()
q["task"] = q.task.str.replace("double_", "")
j = p.merge(q[["entry_id", "openalex_id", "task", "relation"]], on=["entry_id", "openalex_id", "task"],
            suffixes=("", "_2")).dropna(subset=["relation", "relation_2"])
a, b = j.relation.map(three).tolist(), j.relation_2.map(three).tolist()
l1 = v[(v.task == "verify") & v.entry_id.str.contains("moty|boty|tr10|hype", regex=True)].drop_duplicates(["entry_id", "openalex_id"])
l2 = v[v.task == "verify_lists_v2"].drop_duplicates(["entry_id", "openalex_id"])
jl = l1.merge(l2, on=["entry_id", "openalex_id"], suffixes=("_1", "_2")).dropna(subset=["relation_1", "relation_2"])
agr = json.loads((OUT / "llm_agreement.json").read_text())
agr["three_class_agreement"] = {
    "primary_vs_second_double_200": {"n_pairs": len(j), "raw": float(sum(x == y for x, y in zip(a, b)) / max(1, len(j))),
                                     "kappa": kappa(a, b)},
    "lists_v1_vs_v2": {"n_pairs": len(jl), "raw": float((jl.relation_1.map(three) == jl.relation_2.map(three)).mean()),
                       "kappa": kappa(jl.relation_1.map(three).tolist(), jl.relation_2.map(three).tolist())},
    "note": "the second model (gpt-4.1-mini) was shown to flip the narrower/broader direction under the original label "
            "names, so the 5-class kappa understates agreement; 3-class merges narrower and broader"}
(OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
print(json.dumps(agr["three_class_agreement"], indent=1))

# third sample: 30 random accepted Research Fronts links
h3 = pd.read_csv(WORK / "hand_check_rf.csv")
h3["hand"] = json.loads((ROOT / "scripts" / "hand_check_rf_verdicts.json").read_text())["verdicts"]
h3["model"] = h3.relation.map(lambda x: REL.get(x, x))
h3.to_csv(OUT / "hand_check_research_fronts.csv", index=False)
s3 = {"n": int(len(h3)), "precision_of_accepted_links_vs_hand": float(h3.hand.isin(ACC).mean()),
      "relation_exact": float((h3.model == h3.hand).mean()),
      "precision_of_same_links": float((h3[h3.model == "same"].hand == "same").mean()),
      "n_same_links": int((h3.model == "same").sum())}
agr = json.loads((OUT / "llm_agreement.json").read_text())
agr["hand_check_research_fronts_30"] = s3
(OUT / "llm_agreement.json").write_text(json.dumps(agr, indent=1))
print(json.dumps(s3, indent=1))
