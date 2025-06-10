from fastapi.testclient import TestClient
from dais_2025_apps_ci.app import app

client = TestClient(app)


def test_get_info():
    response = client.get("/api/info")
    assert response.status_code == 200
    response_json = response.json()
    assert "version" in response_json
    assert "server_time" in response_json
    assert isinstance(response_json["version"], str)
    assert isinstance(response_json["server_time"], str)


def test_index_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "<!DOCTYPE html>" in response.text
