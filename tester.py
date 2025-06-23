import requests
import json
headers = {
    "model-prompt": "Name the 10 most popular programming languages.",
    "model-name": "llama3.2",
    "name": "Jake Rase",
    "key": "0000000001"
}
out = requests.get('https://ollama-proxy-server-five.vercel.app/api', headers=headers)
if out.status_code != 200:
    out = {"error": f"Status code {out.status_code}", "text": out.text}
else:
    try:
        out = out.json()
    except Exception as e:
        out = {"error": "Invalid JSON response", "text": out.text}
with open('test.json', 'w') as f:
    f.write(str(out))
try:
    print(out["response"])
except Exception as e:
    print(out)