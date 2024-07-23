__all__ = [
    'Credential',
    'CredentialCreate',
    'CredentialPublic',
    'CredentialUpdate',
    'CredentialType',
    'CredentialTypeCreate',
    'CredentialTypeUpdate',
    'Function',
    'FunctionCreate',
    'FunctionPublic',
    'FunctionUpdate',
    'Session',
    'SQLModel',
    'User',
    'UserCreate',
    'UserPublic',
    'UserUpdate',
    'engine',
    'get_session',
    'select',
    'update',
]

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select, update

from metafunction.database.credential import (
    Credential,
    CredentialCreate,
    CredentialPublic,
    CredentialType,
    CredentialTypeCreate,
    CredentialTypeUpdate,
    CredentialUpdate,
)
from metafunction.database.function import (
    Function,
    FunctionCreate,
    FunctionPublic,
    FunctionUpdate,
)
from metafunction.database.user import (
    User,
    UserCreate,
    UserPublic,
    UserUpdate,
)
from metafunction.settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, connect_args={'check_same_thread': False})
SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
