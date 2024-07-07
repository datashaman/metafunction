from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from api.models.types import EncryptedJSON


class Function(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    specification: dict = Field(default={}, sa_column=Column(EncryptedJSON))
