from typing import Optional
from sqlalchemy import Column
from sqlmodel import SQLModel, Field, Relationship

from api.models import CredentialType
from api.models.types import EncryptedJSON


class Credential(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credential_type_id: int | None = Field(
        default=None, foreign_key="credentialtype.id"
    )
    credential_type: CredentialType = Relationship(back_populates="credentials")
    data: dict = Field(default={}, sa_column=Column(EncryptedJSON))
