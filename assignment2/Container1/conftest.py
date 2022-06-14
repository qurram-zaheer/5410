import pytest
import json

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def cleanup_successful_register(client):
    # Startup code
    ...
    yield
    
    client.post("/delete_test")
    print("Cleaned up successfully")

        
@pytest.mark.usefixtures('cleanup_successful_register')
def test_register(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "name": "test",
        "email": "test@test.com",
        "password": "test",
        "location": "test" 
    }
    rv = client.post("/register", data=json.dumps(data), headers=headers)

    rv = rv.json['user']
    
    assert rv['name'] == data['name']
    assert rv['email'] == data['email']
    assert rv['password'] == data['password']
    assert rv['location'] == data['location']



def test_missing_param(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "name": "test",
        "email": "test@test.com",
        "password": "test",
    }
    rv = client.post("/register", data=json.dumps(data), headers=headers)
    
    assert rv.json['error'] == "Bad request"

@pytest.mark.usefixtures('cleanup_successful_register')
def test_already_exists(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    data = {
        "name": "test",
        "email": "test@test.com",
        "password": "test",
        "location": "test" 
    }
    rv = client.post("/register", data=json.dumps(data), headers=headers)
    rv = client.post("/register", data=json.dumps(data), headers=headers)
    assert rv.json['error'] == "Email already exists, please login!"

