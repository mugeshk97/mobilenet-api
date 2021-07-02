import base64
import requests

filename = "mountain_bike.jpeg"

with open(filename, "rb") as f:
    data = f.read()

b64_bytes = base64.b64encode(data)

b64_string = b64_bytes.decode('utf8').replace("'", '"')
payload = {'bytes': b64_string}

data = requests.post('http://172.17.0.2:5001/', json= payload)

print(data.json())
