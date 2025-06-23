from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import subprocess
import json

App = FastAPI()

App.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@App.get("/")
def read_root():
    """
    Returns a simple message indicating the root endpoint is reached.
    """
    return {"message": "Welcome to the FastAPI application!"}


@App.get("/api")
def get_api(request: Request):
    HEADERS = request.headers
    model_prompt = HEADERS["model-prompt"]
    model_name = HEADERS["model-name"]
    try:
        output = subprocess.run(
        ["curl", "http://localhost:11434/api/generate",  "-d",  f'{{ "model": "{model_name}", "prompt": "{model_prompt}", "stream": false }}'],
        capture_output=True, text=True
        )
        print("MODEL NAME:", model_name)
        print("MODEL PROMPT:", model_prompt)
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))
    return json.loads(output.stdout)

if __name__ == "__main__":
    uvicorn.run(App, host="192.168.1.153", port=8000)
