import pytest
from fastapi.testclient import TestClient

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

SQLModel.metadata.create_all(bind=engine)


@pytest.fixture
def session():
    connection = engine.connect()
    connection.begin()
    session = Session(bind=connection)

    yield session

    session.rollback()
    connection.close()


@pytest.fixture
def client(session: Session) -> TestClient:
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


@pytest.fixture
def admin_user(session: Session) -> User:
    return users.create(
        session,
        UserCreate.model_validate(
            {
                'name': 'Admin User',
                'email': 'admin@example.com',
                'password': 'adminpassword',
                'is_admin': True,
            }
        ),
    )


@pytest.fixture
def test_user(session: Session) -> User:
    return users.create(
        session,
        UserCreate.model_validate(
            {
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpassword',
            }
        ),
    )
