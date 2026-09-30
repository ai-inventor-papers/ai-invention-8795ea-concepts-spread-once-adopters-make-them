#!/usr/bin/env python3
"""full_ / mini_ / preview_ variants of method_out.json (mini: first 3 examples per dataset; preview: mini with
every string truncated to 200 characters)."""
import copy
import json

from common import ROOT


def trunc(o, n=200):
    if isinstance(o, str):
        return o if len(o) <= n else o[:n] + "..."
    if isinstance(o, list):
        return [trunc(x, n) for x in o]
    if isinstance(o, dict):
        return {k: trunc(v, n) for k, v in o.items()}
    return o


d = json.loads((ROOT / "method_out.json").read_text())
(ROOT / "full_method_out.json").write_text(json.dumps(d))
mini = copy.deepcopy(d)
for ds in mini["datasets"]:
    ds["examples"] = ds["examples"][:3]
(ROOT / "mini_method_out.json").write_text(json.dumps(mini, indent=1))
(ROOT / "preview_method_out.json").write_text(json.dumps(trunc(mini), indent=1))
print("variants written")
