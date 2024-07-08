from typing import Optional, Dict, Any

from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from metafunction.models.types import EncryptedJSON


class FunctionBase(SQLModel):
    name: str
    specification: Dict[str, Any]


class Function(FunctionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    specification: Dict[str, Any] = Field(default={}, sa_column=Column(EncryptedJSON))


class FunctionCreate(FunctionBase):
    pass


class FunctionUpdate(FunctionBase):
    pass


class FunctionPublic(FunctionBase):
    model_config = {
        "from_attributes": True,
    }

    id: int
