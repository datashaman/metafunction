from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from api.models import Base
from api.models.types import EncryptedJSON


class CredentialModel(Base):
    __tablename__ = "credentials"
    id = Column(Integer, primary_key=True, index=True)
    type_id = Column(Integer, ForeignKey('credential_types.id'))
    type = relationship("CredentialTypeModel")
    data = Column(EncryptedJSON, nullable=False)
