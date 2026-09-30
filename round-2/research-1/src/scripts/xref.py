import json,sys,urllib.request,urllib.parse,concurrent.futures as cf,time
dois=[l.split('#')[0].strip() for l in open(sys.argv[1]) if l.strip() and not l.startswith('#')]
def get(d):
    u='https://api.crossref.org/works/'+urllib.parse.quote(d)+'?mailto=aii-research@example.org'
    for k in range(3):
        try:
            r=json.load(urllib.request.urlopen(u,timeout=30))['message']
            au=r.get('author',[]); fa=(au[0].get('family','')+', '+au[0].get('given','')) if au else ''
            y=(r.get('issued',{}).get('date-parts') or [[None]])[0][0]
            return dict(doi=d,status='ok',first_author=fa,n_auth=len(au),authors=[(a.get('given','')+' '+a.get('family','')).strip() for a in au],year=y,title=(r.get('title') or [''])[0],venue=(r.get('container-title') or [''])[0],vol=r.get('volume'),issue=r.get('issue'),page=r.get('page') or r.get('article-number'),type=r.get('type'))
        except urllib.error.HTTPError as e:
            if e.code==404: return dict(doi=d,status='404')
            time.sleep(2)
        except Exception as e: time.sleep(2)
    return dict(doi=d,status='error')
with cf.ThreadPoolExecutor(6) as ex: res=list(ex.map(get,dois))
json.dump(res,open(sys.argv[2],'w'),indent=1)
for r in res:
    if r['status']!='ok': print('!!',r['doi'],r['status']); continue
    print(f"{r['doi']} | {r['first_author']} (+{r['n_auth']-1}) {r['year']} | {r['title'][:90]} | {r['venue']} {r['vol']}({r['issue']}):{r['page']}")
