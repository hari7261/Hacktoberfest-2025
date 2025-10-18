from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_health():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data.get("status") == "ok"


def test_classify():
    r = client.post("/classify", json={"text": "The media hides the truth; elections are always rigged."})
    assert r.status_code == 200
    data = r.json()
    assert "label" in data and "confidence" in data and "explanation" in data


def test_explain():
    r = client.post(
        "/explain",
        json={
            "text": "The media hides the truth; elections are always rigged.",
            "label": "propaganda",
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert "explanation" in data
