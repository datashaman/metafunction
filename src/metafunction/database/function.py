from typing import Any, ClassVar, Dict, Optional

from sqlalchemy import Column
from sqlmodel import Field, SQLModel

from metafunction.database.types import EncryptedJSON


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
    model_config: ClassVar = {
        'from_attributes': True,
    }

    id: int
