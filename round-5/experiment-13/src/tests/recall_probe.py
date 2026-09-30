import sys, math, numpy as np, pandas as pd
sys.path.insert(0,'lib'); sys.path.insert(0,'.')
import s3_candidates as s3
from common5 import surf
from nrules import key_hash, key_of_tokens
keys,S,_=s3.load_counts(); order=np.argsort(keys); ks=keys[order]
fr=pd.read_csv(s3.EXP5/'frame_concepts.csv', usecols=['ci','name','t0','newborn','early_volume'])
rows=[]
for r in fr.itertuples():
    toks=surf(r.name).split()
    if not (2<=len(toks)<=3) or not (2003<=r.t0<=2014): continue
    h=np.uint64(key_hash(key_of_tokens(toks))); p=np.searchsorted(ks,h)
    s=S[order[p]] if p<len(ks) and ks[p]==h else np.zeros(18,int)
    rows.append((r.ci,r.t0,r.newborn,r.early_volume,s))
for k in (3,4,5):
  for nb in (None,True):
    det=[]
    for ci,t0,newb,ev,s in rows:
        if nb is not None and newb!=nb: continue
        d=-1
        for t in range(2003,2018):
            i=t-2000
            if s[i]>=k and s[i-3:i].max()<=math.floor(0.25*s[i]): d=t;break
        det.append(d!=-1 and d<=t0+2)
    print('k',k,'newborn_only' if nb else 'all', len(det), round(np.mean(det),3))
s_t0p2=[s[t0+2-2000] for ci,t0,nb,ev,s in rows]; print('median sample count at t0+2', np.median(s_t0p2), np.percentile(s_t0p2,[25,75,90]))
C=s3.cand_matrix(S,{t:3 for t in range(2003,2018)}); print('k=3 per-year counts', C.sum(0))
C=s3.cand_matrix(S,{t:4 for t in range(2003,2018)}); print('k=4 per-year counts', C.sum(0))
