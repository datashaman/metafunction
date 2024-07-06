from typing import Optional, Dict, Any
from pydantic import BaseModel


class CredentialTypeBase(BaseModel):
    name: str

class CredentialTypeCreate(CredentialTypeBase):
    pass

class CredentialType(CredentialTypeBase):
    id: int

    class Config:
        orm_mode = True
