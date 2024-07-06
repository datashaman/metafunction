from sqlalchemy import Column, Integer, String, JSON

from api.models import Base
from api.models.types import EncryptedJSON


class FunctionModel(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specification = Column(EncryptedJSON, nullable=False)
