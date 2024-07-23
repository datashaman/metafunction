import pytest
from fastapi.testclient import TestClient

from metafunction import app
from metafunction.crud import credentials, functions, users
from metafunction.database import (
    Credential,
    CredentialCreate,
    CredentialType,
    CredentialTypeCreate,
    Function,
    FunctionCreate,
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


@pytest.fixture
def test_credential(session: Session) -> Credential:
    credential_type = CredentialType.model_validate(CredentialTypeCreate(id='password', name='Password'))
    session.add(credential_type)
    session.commit()
    session.refresh(credential_type)

    return credentials.create(
        session,
        CredentialCreate.model_validate(
            {
                'credential_type_id': credential_type.id,
                'data': {},
                'name': 'Test Credential',
                'user_id': 1,
            }
        ),
    )


@pytest.fixture
def test_function(session: Session) -> Function:
    return functions.create(
        session,
        FunctionCreate.model_validate(
            {
                'name': 'Test Function',
                'specification': {},
            }
        ),
    )
