from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_api_key(monkeypatch):
    monkeypatch.setattr(settings, "ALLOWED_API_KEYS", ["test-key"])


def test_validate_endpoint_success():
    payload = {
        "payload": {
            "amount": 5000,
            "email": "user@company.com",
            "user_id": "550e8400-e29b-41d4-a716-446655440000",
        }
    }

    response = client.post("/validate", json=payload, headers={"x-api-key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "success"


def test_validate_endpoint_failure():
    payload = {"payload": {"password": "123", "amount": 20000}}
    response = client.post("/validate", json=payload, headers={"x-api-key": "test-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["overall_status"] == "failure"


def test_invalid_json():
    response = client.post(
        "/validate", data="not json", headers={"x-api-key": "test-key"}
    )
    assert response.status_code == 400
