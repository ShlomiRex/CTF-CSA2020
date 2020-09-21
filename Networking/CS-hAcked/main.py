import requests

server = "3.126.154.76"
url = 'http://' + server
try:
    res = requests.get(url)
except:
    pass

data = "\x28\x30\xF4"
requests.post(url, data)