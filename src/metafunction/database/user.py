from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from metafunction.database.types import EncryptedType


class UserBase(SQLModel):
    name: str
    email: str
    is_admin: bool = False


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
    model_config = {
        "from_attributes": True,
    }

    id: int
