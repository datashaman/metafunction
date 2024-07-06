from sqlalchemy import Column, Integer, String

from api.models import Base


class CredentialTypeModel(Base):
    __tablename__ = "credential_types"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
