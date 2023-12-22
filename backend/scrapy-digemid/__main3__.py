from urllib import request
import json

url = "https://opm-digemid.minsa.gob.pe"


payload = json({
"filtro": {
    "codigoProducto": "10007",
    "codEstablecimiento": "01",
    "tokenGoogle": ""
}
})
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': url,
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': url,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers'
}


req = request.Request(url, data=payload)
req.add_header('User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/json',
    'Origin': url,
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': url,
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'TE': 'trailers')

#resp = request.urlopen(req)

data = json.dumps(payload)
data = data.encode()
r = request.urlopen(req, data=data)
content = r.read()
print(content)











































