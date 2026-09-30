"""T1: Pass A per-file grounded frame counts must EXACTLY equal the counts implied by EXP5 scan/parts/agg_{fi}.npz."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
import numpy as np, pandas as pd
from common import EXP5, PASSA, Y0, load_frame, jdump, RES, MATCH_Y0, MATCH_Y1

fr = load_frame(); fset = set(fr.ci.tolist())
out = {}
for fi in [int(x) for x in sys.argv[1].split(",")]:
    z = np.load(EXP5 / f"scan/parts/agg_{fi:04d}.npz"); u, c = z["uC"], z["cC"]
    mt = u % 4; r = u // 4; ts = r % 4; r //= 4; pt = r % 32; r //= 32; vf = r % 32; r //= 32; yy = r % 32; ci = r // 32
    d5 = pd.DataFrame({"ci": ci, "year": yy + Y0, "vfield": vf, "ts": ts, "n": c})
    d5 = d5[(d5.ts == 1) & d5.ci.isin(fset) & (d5.year >= MATCH_Y0) & (d5.year <= MATCH_Y1)]
    d5 = d5.groupby(["ci", "year", "vfield"]).n.sum()
    za = np.load(PASSA / f"agg_{fi:04d}.npz"); uk, ck = za["uK"], za["cK"]
    vf = uk % 32; r = uk // 32; yy = r % 32; ci = r // 32
    dA = pd.DataFrame({"ci": ci, "year": yy + Y0, "vfield": vf, "n": ck}).groupby(["ci", "year", "vfield"]).n.sum()
    j = pd.concat([d5.rename("exp5"), dA.rename("passA")], axis=1).fillna(0)
    out[fi] = {"exp5_total": int(j.exp5.sum()), "passA_total": int(j.passA.sum()), "n_keys": len(j),
               "n_keys_mismatch": int((j.exp5 != j.passA).sum()), "exact": bool((j.exp5 == j.passA).all())}
print(json.dumps(out, indent=1))
jdump(out, RES / f"t1_passA_exact_{sys.argv[1].replace(',', '_')}.json")
