from fastapi import FastAPI, Query, HTTPException, Header, Depends
from pymongo import MongoClient
import time

from fastapi.middleware.cors import CORSMiddleware

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response, Request
import time

app = FastAPI(title="Distributed Scraper API", version="1.0")


REQUESTS = Counter("api_requests_total", "API Requests", ["path", "method", "status"])
LATENCY = Histogram("api_request_duration_seconds", "Latency", ["path", "method"])

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    LATENCY.labels(request.url.path, request.method).observe(time.perf_counter() - start)
    REQUESTS.labels(request.url.path, request.method, str(response.status_code)).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)





app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



client = MongoClient("mongodb://localhost:27017/")
db = client["scraper_db"]
raw_col = db["raw_data"]
clean_col = db["cleaned_data"]

API_KEY = "12345"
RATE_LIMIT = {}
MAX_REQUESTS = 10

def rate_limit(client_id):
    now = time.time()
    window = 60
    if client_id not in RATE_LIMIT:
        RATE_LIMIT[client_id] = []
    RATE_LIMIT[client_id] = [t for t in RATE_LIMIT[client_id] if now - t < window]
    if len(RATE_LIMIT[client_id]) >= MAX_REQUESTS:
        raise HTTPException(status_code=429, detail="Rate limit exceeded.")
    RATE_LIMIT[client_id].append(now)

def check_auth(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    rate_limit(x_api_key)
    return True

@app.get("/")
def root():
    return {"message": "Welcome to the Distributed Scraper API"}

@app.get("/get_raw_data")
def get_raw_data(limit: int = 10, auth: bool = Depends(check_auth)):
    data = list(raw_col.find().limit(limit))
    for d in data:
        d["_id"] = str(d["_id"])
    return {"count": len(data), "results": data}

@app.get("/get_cleaned_data")
def get_cleaned_data(limit: int = 10, auth: bool = Depends(check_auth)):
    data = list(clean_col.find().limit(limit))
    for d in data:
        d["_id"] = str(d["_id"])
    return {"count": len(data), "results": data}

@app.get("/search")
def search_data(keyword: str = Query(..., min_length=2), limit: int = 10, auth: bool = Depends(check_auth)):
    query = {"clean_text": {"$regex": keyword, "$options": "i"}}
    results = list(clean_col.find(query).limit(limit))
    for r in results:
        r["_id"] = str(r["_id"])
    return {"matches": len(results), "results": results}
