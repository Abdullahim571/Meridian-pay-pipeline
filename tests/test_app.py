import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_index_returns_service_info(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"service": "meridian-pay", "status": "ok"}


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


def test_unknown_route_returns_404(client):
    assert client.get("/does-not-exist").status_code == 404
