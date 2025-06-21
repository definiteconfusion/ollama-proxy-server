import requests
import json
headers = {
    "model-prompt": "What is the capital of France?",
    "model-name": "qwen3:0.6b"
}
out = requests.get('http://0.0.0.0:8000/api', headers=headers).json()
with open('test.json', 'w') as f:
    f.write(str(out))
print(out["response"])