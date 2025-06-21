from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
import uvicorn

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/api")
def api(request: Request):
    HEADERS = request.headers
    remote_host = os.getenv("REMOTE_HOST", "127.0.0.1")
    remote_port = os.getenv("REMOTE_PORT", "8000")
    response = requests.get(f'http://{remote_host}:{remote_port}/api', headers=HEADERS)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    try:
        out = response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response from remote server", "text": response.text}
    return out

uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")