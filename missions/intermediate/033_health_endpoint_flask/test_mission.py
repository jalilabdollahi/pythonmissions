import pytest
import sys
sys.path.insert(0, ".")
from broken import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

def test_health_status_code(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_health_json(client):
    r = client.get("/health")
    data = r.get_json()
    assert data["status"] == "ok"
