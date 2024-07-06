from typing import Optional, Dict, Any
from pydantic import BaseModel
from api.schemas.credential_type import CredentialType

class CredentialBase(BaseModel):
    type_id: int
    data: Dict[str, Any]

class CredentialCreate(CredentialBase):
    pass

class Credential(CredentialBase):
    id: int
    type: CredentialType

    class Config:
        orm_mode = True
