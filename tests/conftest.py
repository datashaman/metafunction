from typing import Generator, Dict, Any

import pytest  # type: ignore
from fastapi.testclient import TestClient

from metafunction import app
from metafunction.models import Session, get_session, create_tables, User


@pytest.fixture(scope="module")
def session(test_user: Dict[str, Any]) -> Generator[Session, None, None]:
    create_tables()
    session = next(get_session())

    user = User(**test_user)
    session.add(user)

    yield session

    session.rollback()
    session.close()


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(scope="module")
def token(client: TestClient, test_user: Dict[str, Any]) -> str:
    response = client.post(
        "/auth/token",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    return response.json()["access_token"]


@pytest.fixture(scope="module")
def test_user() -> Dict[str, Any]:
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword",
    }
