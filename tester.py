import requests
import json
headers = {
    "model-prompt": "Name 5 popular programming languages.",
    "model-name": "llama3.2",
    "name": "Jake Rase",
    "key": "0000000001"
}
out = requests.get('http://127.0.0.1:8000/api', headers=headers).json() 
with open('test.json', 'w') as f:
    f.write(str(out))
print(out["response"])