import requests
import json

url_autocompletado = "https://ms-opm.minsa.gob.pe/msopmcovid/producto/autocompleteciudadano"

payload = json.dumps({
  "filtro": {
    "nombreProducto": "DAVINTEX 120",
    "pagina": 1,
    "tamanio": 10,
    "tokenGoogle": ""
  }
})
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/119.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/json',
  'Origin': 'https://opm-digemid.minsa.gob.pe',
  'DNT': '1',
  'Connection': 'keep-alive',
  'Referer': 'https://opm-digemid.minsa.gob.pe/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'TE': 'trailers'
}

response = requests.request("POST", url_autocompletado, headers=headers, data=payload)

print(response.text)

print("-" * 30)

url_detalles = "https://ms-opm.minsa.gob.pe/msopmcovid/precioproducto/obtener"

payload = json.dumps({
  "filtro": {
    "codigoProducto": 53725,
    "codEstablecimiento": "0053974",
    "tokenGoogle": "03AFcWeA4brpAjtcOv7mBJ7zrLyEc_wHKtkgCqPJZHvYvRHda00y_XCahZ5cScyR3IriKqzSY-XVRwQndyGvPlty2PIuV44a8-qRqyxKxB9fWoE9k8yCVF2FJlnvuQJSfUPDOyWa5CzQSGKhuEMfFxdwGF7f_nIskIsqeKhwkwbzJEjZMuysqH2jnTaKm2aMITuXKk2UOmvFHDHKzYzYw-kTpBSLqfuo6l1iXRO5FDVNRtjzH1AvP-u218JIJj7UkDgyEhTqoVj9i4126d1fH850lqpkq-GKSRaKWaDFZi3xmCZIL0poGxYWB19Nq17D618nDlmnM2aNPPK03ZSzitxk10FJEcxxg3kQdYgka-OQ2TqLuHSd-NV75Apq-Q0OnZDCQ7gL8vSnBz4QVAWUq7KSLmMO_0mbfCnCmnCkOs75XJVtWaGcjruxBf4r7ZW_WZqC6h2A9bJUT4x1qZKklFw-Jfq5d1rg2G4lssKqQVRAaCsQiyDP63OKUQ8Pu4fAFYcy2pSzEHQ73VOAZC9lPA8XD-wnwDLbaJ0ZfH4KEJNrFgCJPhwykNmX1zX-HnJhlg4Ug6nR0Wt1hZ"
  }
})

headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Content-Type': 'application/json',
  'Origin': 'https://opm-digemid.minsa.gob.pe',
  'Connection': 'keep-alive',
  'Referer': 'https://opm-digemid.minsa.gob.pe/',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-site',
  'TE': 'trailers'
}

response = requests.request("POST", url_detalles, headers=headers, data=payload)

print(response.text)










