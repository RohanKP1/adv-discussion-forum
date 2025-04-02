import pytest
import requests
from unittest.mock import patch

BASE_URL = "http://localhost:8000/api"

@pytest.fixture
def auth_client():
    from api_service import AuthClient
    return AuthClient(base_url=BASE_URL)

@pytest.fixture
def mock_requests_post():
    with patch("requests.post") as mock_post:
        yield mock_post

@pytest.fixture
def mock_requests_get():
    with patch("requests.get") as mock_get:
        yield mock_get

@pytest.fixture
def mock_requests_put():
    with patch("requests.put") as mock_put:
        yield mock_put

@pytest.fixture
def mock_requests_delete():
    with patch("requests.delete") as mock_delete:
        yield mock_delete

def test_register_user(auth_client, mock_requests_post):
    mock_requests_post.return_value.status_code = 201
    mock_requests_post.return_value.json.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }

    response = auth_client.register("testuser", "test@example.com", "password123")
    assert response is not None
    assert response["username"] == "testuser"
    assert response["email"] == "test@example.com"

def test_login_user(auth_client, mock_requests_post):
    mock_requests_post.return_value.status_code = 200
    mock_requests_post.return_value.json.return_value = {
        "access_token": "mocked_token",
        "token_type": "bearer"
    }

    token = auth_client.login("testuser", "password123")
    assert token == "mocked_token"

def test_get_current_user(auth_client, mock_requests_get):
    auth_client.access_token = "mocked_token"
    mock_requests_get.return_value.status_code = 200
    mock_requests_get.return_value.json.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }

    user_info = auth_client.get_current_user()
    assert user_info is not None
    assert user_info["username"] == "testuser"
    assert user_info["email"] == "test@example.com"

def test_update_user(auth_client, mock_requests_put):
    auth_client.access_token = "mocked_token"
    mock_requests_put.return_value.status_code = 200
    mock_requests_put.return_value.json.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "newemail@example.com"
    }

    updated_user = auth_client.update_user(email="newemail@example.com")
    assert updated_user is not None
    assert updated_user["email"] == "newemail@example.com"

def test_delete_user(auth_client, mock_requests_delete):
    auth_client.access_token = "mocked_token"
    mock_requests_delete.return_value.status_code = 200
    mock_requests_delete.return_value.json.return_value = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com"
    }

    deleted_user = auth_client.delete_user()
    assert deleted_user is not None
    assert deleted_user["username"] == "testuser"
    assert deleted_user["email"] == "test@example.com"
