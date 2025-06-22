import requests
import json
headers = {
    "model-prompt": "Name the 10 most popular programming languages.",
    "model-name": "llama3.2",
    "name": "Jake Rase",
    "key": "0000000001"
}
out = requests.get('https://ollama-proxy-server-five.vercel.app/api', headers=headers).json() 
with open('test.json', 'w') as f:
    f.write(str(out))
print(out["response"])