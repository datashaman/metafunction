from typing import Any, ClassVar, Dict, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from metafunction.types.encrypted_json import EncryptedJSON
from metafunction.users.models import User


class FunctionBase(SQLModel):
    name: str
    specification: Dict[str, Any]


class Function(FunctionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='functions')
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
