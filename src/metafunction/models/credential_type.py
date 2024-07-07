from typing import Optional, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from metafunction.models.credential import Credential


class CredentialTypeBase(SQLModel):
    name: str


class CredentialType(CredentialTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credentials: list["Credential"] = Relationship(back_populates="credential_type")


class CredentialTypeCreate(CredentialTypeBase):
    pass


class CredentialTypeUpdate(CredentialTypeBase):
    pass


class CredentialTypePublic(CredentialTypeBase):
    id: int

    class Config:
        from_attributes = True
