from typing import Any, ClassVar, Dict, List, Optional

from sqlalchemy import Column
from sqlmodel import Field, Relationship, SQLModel

from metafunction.types.encrypted_json import EncryptedJSON
from metafunction.users.models import User


class CredentialTypeBase(SQLModel):
    id: str
    name: str


class CredentialType(CredentialTypeBase, table=True):
    id: str = Field(primary_key=True)
    credentials: List['Credential'] = Relationship(back_populates='credential_type')


class CredentialTypeCreate(CredentialTypeBase):
    pass


class CredentialTypeUpdate(CredentialTypeBase):
    pass


class CredentialTypePublic(CredentialTypeBase):
    model_config: ClassVar = {
        'from_attributes': True,
    }


class CredentialBase(SQLModel):
    name: str
    credential_type_id: str
    data: Dict[str, Any]


class Credential(CredentialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credential_type_id: str = Field(foreign_key='credentialtype.id')
    credential_type: CredentialType = Relationship(back_populates='credentials')
    user_id: int = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='credentials')
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
