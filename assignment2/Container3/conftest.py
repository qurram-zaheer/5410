import pytest
import json

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_missing_arg(client):
    rv = client.get("/sessions")

    assert rv.json['error'] == "Bad request"