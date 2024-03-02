# import requests
# import hashlib
# url = "http://host3.dreamhack.games:17122/flag"

# guest_key = hashlib.md5(b"guest").hexdigest()
# #data = {"cmd_input":"sleep 6", "key":""}
# data = {"cmd_input":"", "key":"409ac0d96943d3da52f176ae9ff2b974"}
# resp = requests.post(url, data=data)
# print(resp.text)

s = input()
x = len(s)

if x%2==0:
    print(s[x//2-1], s[x//2])
else:
    print(s[x//2])