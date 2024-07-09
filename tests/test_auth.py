from typing import Dict, Any

from fastapi.testclient import TestClient

from metafunction import app
from metafunction.database import Session, User


def test_login(client: TestClient, test_user: User) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": test_user.email,
            "password": test_user.password,
        },
    )
    print(response.json())

    assert response.status_code == 200
    assert response.json()["access_token"] is not None


def test_login_invalid_username(client: TestClient, test_user: User) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": "invalid",
            "password": test_user.password,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_invalid_password(client: TestClient, test_user: User) -> None:
    response = client.post(
        "/auth/token",
        data={
            "username": test_user.email,
            "password": "invalid",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_unauthorized_me(client: TestClient) -> None:
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"


def test_authorized_me(client: TestClient, token: str, test_user: User) -> None:
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert data["email"] == test_user.email
    assert data["name"] == test_user.name
    assert not "password" in data
