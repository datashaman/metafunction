from sqlmodel import Session, create_engine, select

from api.settings import SQLALCHEMY_DATABASE_URL

from api.models.function import Function
from api.models.user import User
from api.models.credential_type import CredentialType
from api.models.credential import Credential

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, connect_args={"check_same_thread": False})


def get_session() -> Session:
    with Session(engine) as session:
        yield session
