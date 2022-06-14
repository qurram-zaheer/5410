import pytest
import json

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_missing_key(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "email": "test@test.com",
    }
    rv = client.post("/login", data=json.dumps(data), headers=headers)
    assert rv.json['error'] == "Bad request"