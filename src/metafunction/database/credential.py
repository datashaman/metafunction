from typing import Optional, Dict, Any
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship

from metafunction.database import CredentialType
from metafunction.database.types import EncryptedJSON


class CredentialBase(SQLModel):
    credential_type_id: Optional[int]
    data: Dict[str, Any]


class Credential(CredentialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credential_type_id: Optional[int] = Field(
        default=None, foreign_key="credentialtype.id"
    )
    credential_type: CredentialType = Relationship(back_populates="credentials")
    data: Dict[str, Any] = Field(default={}, sa_column=Column(EncryptedJSON))


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(CredentialBase):
    pass


class CredentialPublic(CredentialBase):
    model_config = {
        "from_attributes": True,
    }

    id: int
