__all__ = [
    "Credential",
    "CredentialCreate",
    "CredentialPublic",
    "CredentialUpdate",
    "CredentialType",
    "Function",
    "FunctionCreate",
    "FunctionPublic",
    "FunctionUpdate",
    "Session",
    "SQLModel",
    "User",
    "UserCreate",
    "UserPublic",
    "UserUpdate",
    "create_tables",
    "engine",
    "get_session",
    "select",
]

from typing import Generator

from sqlmodel import SQLModel, Session, create_engine, select

from metafunction.settings import SQLALCHEMY_DATABASE_URL

from metafunction.database.credential_type import CredentialType
from metafunction.database.credential import (
    Credential,
    CredentialCreate,
    CredentialUpdate,
    CredentialPublic,
)
from metafunction.database.function import (
    Function,
    FunctionCreate,
    FunctionUpdate,
    FunctionPublic,
)
from metafunction.database.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPublic,
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def get_session(rollback: bool = False) -> Generator[Session, None, None]:
    session = Session(engine)
    yield session
    if rollback:
        session.rollback()
    session.close()


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)


def drop_tables() -> None:
    SQLModel.metadata.drop_all(engine)
