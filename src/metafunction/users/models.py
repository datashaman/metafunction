from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, ClassVar, List, Optional

import jwt
from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from metafunction.settings import (
    ACCESS_TOKEN_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)
from metafunction.types.encrypted_type import EncryptedType

if TYPE_CHECKING:
    from metafunction.credentials.models import Credential
    from metafunction.functions.models import Function


class UserBase(SQLModel):
    name: str
    email: str
    is_admin: bool = False

    def create_access_token(self) -> str:
        data = {
            'sub': self.email,
            'exp': datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        return jwt.encode(data, SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True)
    email: str = Field(unique=True)
    password: str = Field(sa_column=Column(EncryptedType))
    credentials: List['Credential'] = Relationship(back_populates='user')
    functions: List['Function'] = Relationship(back_populates='user')


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserPublic(UserBase):
    model_config: ClassVar = {
        'from_attributes': True,
    }

    id: int
