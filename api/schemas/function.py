
from pydantic import BaseModel
from typing import Any, Dict

class Function(BaseModel):
    id: int
    name: str
    specification: Dict[str, Any]

    class Config:
        orm_mode = True
