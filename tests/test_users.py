from starlette.testclient import TestClient

from delvify.models import User


def test_create_user_no_password(client: TestClient, test_user: User):
    request_body = {
        "email": test_user.email
    }
    response = client.post("/api/v1/users", json=request_body)
    assert response.status_code == 422
    assert len(response.json()["detail"]) > 0


def test_create_user_no_email(client: TestClient, test_user: User):
    request_body = {
        "password": test_user.password
    }
    response = client.post("/api/v1/users", json=request_body)
    assert response.status_code == 422
    assert len(response.json()["detail"]) > 0


def test_login_no_password(client: TestClient, test_user: User):
    request_body = {
        "email": test_user.email
    }
    response = client.post("/api/v1/users/login", json=request_body)
    assert response.status_code == 422
    assert len(response.json()["detail"]) > 0


def test_login_no_email(client: TestClient, test_user: User):
    request_body = {
        "password": test_user.password
    }
    response = client.post("/api/v1/users/login", json=request_body)
    assert response.status_code == 422
    assert len(response.json()["detail"]) > 0


def test_get_me_no_token(client: TestClient, test_user: User):
    response = client.get("/api/v1/users/me")
    assert response.status_code == 403
    assert len(response.json()["detail"]) > 0
