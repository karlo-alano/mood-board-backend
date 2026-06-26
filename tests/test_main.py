from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_quote():
    response = client.get("/quote")

    assert response.status_code == 200

    data = response.json()

    assert "text" in data
    assert "author" in data
    assert data["text"] != ""


def test_submit_perfect():
    payload = {
        "original_text": "The quick brown fox jumps over the lazy dog.",
        "typed_text": "The quick brown fox jumps over the lazy dog.",
        "time_taken_seconds": 10.0,
    }

    response = client.post("/submit", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["accuracy"] == 100
    assert data["wpm"] > 0


def test_submit_with_typos():
    payload = {
        "original_text": "The quick brown fox jumps over the lazy dog.",
        "typed_text": "The quick brown box jumps ovre the lazy dog.",
        "time_taken_seconds": 10.0,
    }

    response = client.post("/submit", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["accuracy"] < 100
    assert data["wpm"] > 0
