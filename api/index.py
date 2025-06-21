from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from supabase import create_client, Client


class Supabase:
    def __init__(self, table):
        url: str = "https://wvszrkaovwiaiboyohya.supabase.co"
        key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind2c3pya2FvdndpYWlib3lvaHlhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDUxMzMyMiwiZXhwIjoyMDY2MDg5MzIyfQ.p-dk-85jbg1kJv9r7iCHO3Ir_X5Jf7M3juR8tiUPxeY"
        supabase: Client = create_client(url, key)
        self.table = table
        self.base = supabase
        
    
    def search(self, data: dict):
        response = self.base.from_(self.table).select().text_search('name', data["name"]).execute()
        return response.model_dump()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def auth_check(request: Request):
    HEADERS = request.headers
    name = HEADERS.get("name", None)
    real_key = HEADERS.get("key", None)
    if not name or not real_key:
        return False
    response = Supabase("users").base.from_("users").select("key").eq("name", name).execute()
    results = response.model_dump()
    theo_key = results["data"][0]["key"] if results["data"] else None
    if not theo_key:
        return {"error": "No key found for the provided name."}
    if str(theo_key) != str(real_key):
        return False
    return True

@app.get("/")
def read_root():
    """
    Returns a simple message indicating the root endpoint is reached.
    """
    return {"message": "Welcome to the FastAPI application!"}

@app.get("/api")
def api(request: Request):
    print("API endpoint called")
    HEADERS = request.headers
    if not auth_check(request):
        return {"error": "Authentication failed. Invalid name or key."}
    remote_host = os.getenv("REMOTE_HOST", "0.0.0.0")
    remote_port = os.getenv("REMOTE_PORT", "3000")
    response = requests.get(f'http://{remote_host}:{remote_port}/api', headers=HEADERS)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    try:
        out = response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response from remote server", "text": response.text}
    return out