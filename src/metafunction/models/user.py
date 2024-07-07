from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from metafunction.models.types import EncryptedType


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str = Field(sa_column=Column(EncryptedType))
    is_admin: bool
