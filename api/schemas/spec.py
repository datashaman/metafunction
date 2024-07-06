
from pydantic import BaseModel
from typing import Any, Dict

class OpenAPISpec(BaseModel):
    id: int
    name: str
    specification: Dict[str, Any]

    class Config:
        orm_mode = True
