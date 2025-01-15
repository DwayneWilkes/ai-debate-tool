import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from backend.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to the AI Debate Tool Backend!"}
