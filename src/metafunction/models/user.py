from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from metafunction.models.types import EncryptedType


class UserBase(SQLModel):
    name: str
    email: str
    is_admin: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    password: str = Field(sa_column=Column(EncryptedType))


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    password: Optional[str] = None


class UserPublic(UserBase):
    id: int

    class Config:
        from_attributes = True
