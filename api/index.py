from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from supabase import create_client, Client

class Supabase:
    def __init__(self, table):
        url: str = os.environ.get("SUPABASE_URL", "None")
        key: str = os.environ.get("SUPABASE_KEY", "None")
        supabase: Client = create_client(url, key)
        self.table = table
        self.base = supabase
        
    
    def search(self, data: dict):
        response = self.base.from_(self.table).select().text_search('name', data["name"]).execute()
        return response.model_dump()


db = Supabase("users")
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def auth_check(request: Request, permission_level: int = 0):
    HEADERS = request.headers
    name = HEADERS.get("name", None)
    real_key = HEADERS.get("key", None)
    if not name or not real_key:
        return False
    response = db.base.from_("users").select("*").eq("name", name).execute()
    results = response.model_dump()
    print("AUTH RESULTS:", results)
    theo_key = results["data"][0]["key"] if results["data"] else None
    if not theo_key:
        return False
    if str(theo_key) != str(real_key):
        return False
    perm_level = results["data"][0]["level"] if results["data"] else 0
    if perm_level < permission_level:
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
        return {"error": "Authentication failed. Invalid name, key, or permissions."}
    remote_host = os.getenv("REMOTE_HOST", "70.22.254.47")
    remote_port = os.getenv("REMOTE_PORT", "8000")
    response = requests.get(f'http://{remote_host}:{remote_port}/api', headers=HEADERS)
    response.raise_for_status()  # Raises an HTTPError for bad responses
    try:
        out = response.json()
    except requests.exceptions.JSONDecodeError:
        return {"error": "Invalid JSON response from remote server", "text": response.text}
    return out