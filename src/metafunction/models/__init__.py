from sqlmodel import SQLModel, Session, create_engine, select

from metafunction.settings import SQLALCHEMY_DATABASE_URL

from metafunction.models.function import Function
from metafunction.models.user import User
from metafunction.models.credential_type import CredentialType
from metafunction.models.credential import Credential

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def get_session() -> Session:
    with Session(engine) as session:
        yield session


def create_tables() -> None:
    SQLModel.metadata.create_all(engine)
