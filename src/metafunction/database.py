__all__ = [
    'SQLModel',
    'Session',
    'engine',
    'get_session',
    'select',
    'update',
    'credentials',
    'functions',
    'users',
]

from typing import Generator

from sqlmodel import Session, SQLModel, create_engine, select, update

import metafunction.credentials.models as credentials
import metafunction.functions.models as functions
import metafunction.users.models as users
from metafunction.settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False, connect_args={'check_same_thread': False})
SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
