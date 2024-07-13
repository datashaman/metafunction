from typing import Dict, Any

from fastapi.testclient import TestClient

from metafunction import app
from metafunction.database import Session, User


def test_login(client: TestClient, test_user: User, session: Session) -> None:
    print(session)
    response = client.post(
        "/auth/token",
        data={
            "username": test_user.email,
            "password": test_user.password,
        },
    )

    print(response.json(), test_user)

    assert response.status_code == 200

    data = response.json()
    assert data["access_token"] is not None


def test_login_invalid_username(client: TestClient, test_user: User) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": "invalid",
            "password": test_user.password,
        },
    )
    assert response.status_code == 400

    data = response.json()
    assert data["status"] == "fail"
    assert data["data"]["username"] == "Incorrect username or password"


def test_login_invalid_password(client: TestClient, test_user: User) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": test_user.email,
            "password": "invalid",
        },
    )
    assert response.status_code == 400

    data = response.json()
    assert data["status"] == "fail"
    assert data["data"]["username"] == "Incorrect username or password"


def test_unauthorized_me(client: TestClient) -> None:
    response = client.get("/auth/me")
    assert response.status_code == 401

    data = response.json()
    assert data["status"] == "error"
    assert data["message"] == "Not authenticated"


def test_authorized_me(client: TestClient, token: str, test_user: User) -> None:
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["user"]["email"] == test_user.email
    assert data["data"]["user"]["name"] == test_user.name
    assert not "password" in data["data"]["user"]
