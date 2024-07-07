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
    "User",
    "UserCreate",
    "UserPublic",
    "UserUpdate",
    "create_tables",
    "get_session",
    "select",
]

from typing import Generator

from sqlmodel import SQLModel, Session, create_engine, select

from metafunction.settings import SQLALCHEMY_DATABASE_URL

from metafunction.models.credential_type import CredentialType
from metafunction.models.credential import (
    Credential,
    CredentialCreate,
    CredentialUpdate,
    CredentialPublic,
)
from metafunction.models.function import (
    Function,
    FunctionCreate,
    FunctionUpdate,
    FunctionPublic,
)
from metafunction.models.user import (
    User,
    UserCreate,
    UserUpdate,
    UserPublic,
)


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)
