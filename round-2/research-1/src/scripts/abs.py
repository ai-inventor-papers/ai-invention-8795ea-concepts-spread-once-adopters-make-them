import json,sys,urllib.request,urllib.parse
dois=sys.argv[1]
u='https://api.openalex.org/works?'+urllib.parse.urlencode({'filter':'doi:'+dois,'select':'doi,title,publication_year,authorships,abstract_inverted_index,primary_location,biblio,cited_by_count','per_page':50})
d=json.load(urllib.request.urlopen(u,timeout=60))
for w in d['results']:
    ai=w.get('abstract_inverted_index') or {}
    ab=' '.join(k for p,k in sorted((p,k) for k,v in ai.items() for p in v))
    src=((w.get('primary_location') or {}).get('source') or {}).get('display_name')
    print('\n##',w['publication_year'],w['doi'],'|',w['title'],'|',', '.join(a['author']['display_name'] for a in w['authorships'][:6]),'|',src,w['biblio'],'cites',w['cited_by_count'])
    print(ab[:1800])
