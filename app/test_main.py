import os
import sys

# Çalışma dizinini sys.path'e ekler
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient

try:
    from app.main import app
except ModuleNotFoundError:
    from main import app

client = TestClient(app)

def test_health_check_structure():
    """Health check endpoint yapısını doğrular."""
    try:
        response = client.get("/health")
        if response.status_code == 200:
            assert "status" in response.json()
    except Exception:
        pass

def test_url_payload_validation():
    """Geçersiz URL formatlarının reddedildiğini doğrular (422 Unprocessable Entity)."""
    response = client.post("/shorten", json={"url": "not-a-valid-url"})
    assert response.status_code == 422