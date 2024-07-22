from datetime import datetime, timedelta, timezone
from typing import ClassVar, Optional

import jwt
from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from metafunction.database.types import EncryptedType
from metafunction.settings import (
    ACCESS_TOKEN_ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    SECRET_KEY,
)


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


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserPublic(UserBase):
    model_config: ClassVar = {
        'from_attributes': True,
    }

    id: int
