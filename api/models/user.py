from sqlalchemy import Boolean, Column, Integer, String, JSON

from api.models import Base
from api.models.types import EncryptedType


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    email = Column(String, index=True, nullable=False, unique=True)
    password = Column(EncryptedType, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)

    def verify_password(self, password: str) -> bool:
        return self.password == password
