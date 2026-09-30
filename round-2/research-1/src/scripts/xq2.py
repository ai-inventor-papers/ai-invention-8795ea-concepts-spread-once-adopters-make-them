import json,sys,urllib.request,urllib.parse,time
for q in [l.strip() for l in open(sys.argv[1]) if l.strip()]:
    u='https://api.crossref.org/works?rows=2&select=DOI,title,author,issued,container-title,volume,page&query.bibliographic='+urllib.parse.quote(q)+'&mailto=aii-research@example.org'
    for k in range(3):
        try: items=json.load(urllib.request.urlopen(u,timeout=40))['message']['items']; break
        except Exception as e: items=[]; time.sleep(4)
    print('\n>>',q)
    for it in items:
        au=it.get('author',[]); fa=au[0].get('family','') if au else ''
        print('   ',it['DOI'],'|',fa,(it.get('issued',{}).get('date-parts') or [[None]])[0][0],'|',(it.get('title') or [''])[0][:95],'|',(it.get('container-title') or [''])[0][:35],it.get('volume'),it.get('page'))
    time.sleep(1.5)
