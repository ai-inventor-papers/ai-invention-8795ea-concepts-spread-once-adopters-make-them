import sys, numpy as np, pandas as pd
sys.path.insert(0,'lib'); sys.path.insert(0,'.')
import s3_candidates as s3
keys,S,nlen=s3.load_counts()
C3=s3.cand_matrix(S,{t:3 for t in range(2003,2018)}); inU=C3.any(1)
Uk,US=keys[inU],S[inU]; UNS=s3.nsrc_matrix(Uk)
c=pd.read_csv('data/frame_n_candidates.csv',low_memory=False)
# exclusion flags: reuse lexical exclusion via names in superset is expensive; approximate with v2 lexical pass rate
for k in (3,4):
  for msrc in (0,3):
    kt={t:k for t in range(2003,2018)}
    NS=UNS if msrc else None
    Ck=s3.cand_matrix(US,kt,NS)
    if not msrc: pass
    has=Ck.any(1); td=np.where(has,2003+np.argmax(Ck,1),-1)
    sel=np.nonzero(has)[0]
    # projected full-corpus rows in t_det-5..t_det+4 (x4.4), years>2017 use s_2017
    tot=0
    for j in sel:
        t=td[j]; ys=range(t-5,t+5)
        tot+=sum(US[j,min(max(y,2000),2017)-2000] for y in ys)
    st=US[sel,td[sel]-2000]; st2=np.array([US[j,min(td[j]+2,2017)-2000] for j in sel])
    print(f'k={k} msrc={msrc}: candidates(before lexical) {len(sel)}, early rows proj {tot*4.4/1e6:.1f}M, frac s(t+2)*4.4>=20: {np.mean(st2*4.4>=20):.3f}, n with s(t+2)*4.4>=20 & t_det<=2014+2: {int(np.sum((st2*4.4>=20)&(td[sel]<=2016)))}')
