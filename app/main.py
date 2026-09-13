import os
import string
import random
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import redis

app = FastAPI(
    title="Cloud-Native URL Shortener",
    description="A simple, fast, and scalable URL shortener API",
    version="1.0.0"
)

# Cloud-ready yaklaşım: Konfigürasyonları ortam değişkenlerinden okuyoruz
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis bağlantı havuzu
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

class URLCreateRequest(BaseModel):
    url: HttpUrl

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

@app.get("/health", tags=["Health"])
def health_check():
    """Cloud sağlık kontrolü (Liveness/Readiness Probe) için endpoint."""
    try:
        r.ping()
        return {"status": "healthy", "redis": "connected"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis connection failed: {str(e)}")

@app.post("/shorten", tags=["URL Operations"])
def shorten_url(payload: URLCreateRequest):
    code = generate_short_code()
    # Kod çakışması kontrolü
    while r.exists(f"url:{code}"):
        code = generate_short_code()
    
    r.set(f"url:{code}", str(payload.url))
    r.set(f"clicks:{code}", 0)
    return {"short_code": code, "original_url": str(payload.url)}

@app.get("/{code}", tags=["URL Operations"])
def redirect_to_url(code: str):
    original_url = r.get(f"url:{code}")
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    r.incr(f"clicks:{code}")
    return RedirectResponse(url=original_url, status_code=307)

@app.get("/stats/{code}", tags=["Analytics"])
def get_stats(code: str):
    original_url = r.get(f"url:{code}")
    if not original_url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
    clicks = r.get(f"clicks:{code}")
    return {
        "short_code": code,
        "original_url": original_url,
        "clicks": int(clicks or 0)
    }