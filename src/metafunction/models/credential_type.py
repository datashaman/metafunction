from typing import Optional

from sqlmodel import SQLModel, Field, Relationship


class CredentialType(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    credentials: list["Credential"] = Relationship(back_populates="credential_type")
