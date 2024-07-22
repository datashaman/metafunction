from typing import Any, ClassVar, Dict, List, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from metafunction.database.types import EncryptedJSON


class CredentialTypeBase(SQLModel):
    name: str


class CredentialType(CredentialTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credentials: List['Credential'] = Relationship(back_populates='credential_type')


class CredentialTypeCreate(CredentialTypeBase):
    pass


class CredentialTypeUpdate(CredentialTypeBase):
    pass


class CredentialTypePublic(CredentialTypeBase):
    model_config: ClassVar = {
        'from_attributes': True,
    }

    id: int


class CredentialBase(SQLModel):
    name: str
    credential_type_id: Optional[int]
    data: Dict[str, Any]


class Credential(CredentialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credential_type_id: Optional[int] = Field(default=None, foreign_key='credentialtype.id')
    credential_type: CredentialType = Relationship(back_populates='credentials')
    data: Dict[str, Any] = Field(default={}, sa_column=Column(EncryptedJSON))


class CredentialCreate(CredentialBase):
    pass


class CredentialUpdate(CredentialBase):
    pass


class CredentialPublic(CredentialBase):
    model_config: ClassVar = {
        'from_attributes': True,
    }

    id: int
