import os
from typing import Generator, Dict, Any

import pytest  # type: ignore
from fastapi.testclient import TestClient
from sqlalchemy.engine import Engine

from metafunction import app
from metafunction.crud import users
from metafunction.database import (
    Session,
    SQLModel,
    User,
    UserCreate,
    engine,
    get_session,
)
from metafunction.security.oauth2 import create_access_token


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def session(tables: None) -> Generator[Session, None, None]:
    session = next(get_session(rollback=True))
    yield session


@pytest.fixture
def token(client: TestClient, test_user: User) -> str:
    return create_access_token(test_user.email)


@pytest.fixture
def test_user(session: Session) -> User:
    return users.create(
        session,
        UserCreate.model_validate(
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "testpassword",
            }
        ),
    )


@pytest.fixture
def tables() -> Generator[None, None, None]:
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)
