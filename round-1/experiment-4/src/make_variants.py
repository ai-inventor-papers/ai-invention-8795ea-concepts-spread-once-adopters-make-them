"""Write full/mini/preview variants of method_out.json (datasets-grouped exp_gen_sol_out format)."""
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def trunc(o, n=200):
    if isinstance(o, str):
        return o if len(o) <= n else o[:n] + "..."
    if isinstance(o, list):
        return [trunc(v, n) for v in o]
    if isinstance(o, dict):
        return {k: trunc(v, n) for k, v in o.items()}
    return o


def main() -> None:
    full = json.loads((ROOT / "method_out.json").read_text())
    (ROOT / "full_method_out.json").write_text(json.dumps(full, indent=1))
    mini = copy.deepcopy(full)
    for d in mini["datasets"]:
        d["examples"] = d["examples"][:3]
    (ROOT / "mini_method_out.json").write_text(json.dumps(mini, indent=1))
    prev = copy.deepcopy(mini)
    prev["metadata"] = {k: (v if k in ("method_name", "description", "deviations") else "see full_method_out.json")
                        for k, v in prev["metadata"].items()}
    (ROOT / "preview_method_out.json").write_text(json.dumps(trunc(prev), indent=1))
    print({d["dataset"]: len(d["examples"]) for d in full["datasets"]})


if __name__ == "__main__":
    main()
