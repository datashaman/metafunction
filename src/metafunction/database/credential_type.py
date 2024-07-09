from typing import Optional, List, TYPE_CHECKING

from sqlmodel import SQLModel, Field, Relationship


if TYPE_CHECKING:
    from metafunction.database.credential import Credential


class CredentialTypeBase(SQLModel):
    name: str


class CredentialType(CredentialTypeBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    credentials: List["Credential"] = Relationship(back_populates="credential_type")


class CredentialTypeCreate(CredentialTypeBase):
    pass


class CredentialTypeUpdate(CredentialTypeBase):
    pass


class CredentialTypePublic(CredentialTypeBase):
    model_config = {
        "from_attributes": True,
    }

    id: int
