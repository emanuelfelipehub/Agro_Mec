import json, time, urllib.request
leituras=[{'patrimonio':'PAT-004','horimetro':3362},{'patrimonio':'PAT-001','horimetro':1500}]
for dados in leituras:
 req=urllib.request.Request('http://127.0.0.1:5000/api/horimetro',data=json.dumps(dados).encode(),headers={'Content-Type':'application/json'},method='POST')
 try:
  print(urllib.request.urlopen(req).read().decode())
 except Exception as e: print('Erro:',e)
 time.sleep(2)
