import json,sys,urllib.request,urllib.parse,concurrent.futures as cf
qs=[l.strip() for l in open(sys.argv[1]) if l.strip()]
def f(q):
    u='https://api.crossref.org/works?rows=3&select=DOI,title,author,issued,container-title,volume,page&query.bibliographic='+urllib.parse.quote(q)+'&mailto=aii-research@example.org'
    try: items=json.load(urllib.request.urlopen(u,timeout=40))['message']['items']
    except Exception as e: return q,[('ERR',str(e))]
    out=[]
    for it in items:
        au=it.get('author',[]); fa=au[0].get('family','') if au else ''
        out.append((it['DOI'],fa,(it.get('issued',{}).get('date-parts') or [[None]])[0][0],(it.get('title') or [''])[0][:90],(it.get('container-title') or [''])[0][:40],it.get('volume'),it.get('page')))
    return q,out
with cf.ThreadPoolExecutor(5) as ex:
    for q,o in ex.map(f,qs):
        print('\n>>',q)
        for x in o: print('   ',x)
