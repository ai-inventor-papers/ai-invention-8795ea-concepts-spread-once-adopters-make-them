import sys, json, numpy as np, pandas as pd
from pathlib import Path
import os; E=Path(os.environ.get('AII_RUN_ROOT', str(Path(__file__).resolve().parents[5]))) / '3_invention_loop/iter_4/gen_art/gen_art_experiment_10'; T=Path('tests/t1_parts')
cc=pd.read_csv('inputs/cohort_candidates.csv'); cis=set(cc.ci)
out={}
for fi in (65,1125,1407):
    g1=np.load(T/f'tot_{fi:04d}.npz')['G']; g0=np.load(E/'passC/parts'/f'tot_{fi:04d}.npz')['G']
    mine=pd.concat([pd.read_parquet(T/f'pre_{fi:04d}.parquet'), pd.read_parquet(T/f'sealedA_{fi:04d}.parquet'),
                    pd.read_parquet(T/f'early_{fi:04d}.parquet').assign(n=1)[['ci','year','vfield','mt','n']]])
    ref=pd.concat([pd.read_parquet(E/'passC/parts'/f'pre_{fi:04d}.parquet'), pd.read_parquet(E/'data/sealed/parts'/f'sealed_{fi:04d}.parquet')])
    ref=ref[ref.ci.isin(cis)]
    a=mine.groupby(['ci','year','vfield']).n.sum(); b=ref.groupby(['ci','year','vfield']).n.sum()
    j=pd.concat([a.rename('mine'),b.rename('exp10')],axis=1).fillna(0)
    out[fi]={'G_equal':bool((g1==g0).all()),'n_cells':len(j),'counts_equal':bool((j.mine==j.exp10).all()),'n_hits_mine':int(a.sum()),'n_hits_exp10':int(b.sum()),'concepts':sorted(int(x) for x in j.index.get_level_values(0).unique())[:5]}
ok=all(v['G_equal'] and v['counts_equal'] for v in out.values())
print(json.dumps(out)); json.dump({'T1':out,'pass':ok}, open('results/t1.json','w'), indent=1)
