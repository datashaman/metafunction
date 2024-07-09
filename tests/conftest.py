import os
from typing import Generator, Dict, Any

import pytest  # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from metafunction import app
from metafunction.database import (
    SQLModel,
    User,
    engine,
)


@pytest.fixture(scope="session")
def tables() -> Generator[None, None, None]:
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def session(tables: None) -> Generator[Session, None, None]:
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def token(client: TestClient, test_user: User) -> str:
    response = client.post(
        "/auth/token",
        data={
            "username": test_user.email,
            "password": test_user.password,
        },
    )
    return response.json()["access_token"]


@pytest.fixture
def test_user(session: Session) -> User:
    user = User(
        name="Test User",
        email="test@example.com",
        password="testpassword",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
