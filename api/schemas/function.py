from pydantic import BaseModel
from typing import Any, Dict


class FunctionBase(BaseModel):
    name: str
    specification: Dict[str, Any]


class FunctionCreate(FunctionBase):
    pass


class Function(BaseModel):
    id: int
    name: str
    specification: Dict[str, Any]

    class Config:
        orm_mode = True
