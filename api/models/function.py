from sqlalchemy import Column, Integer, String, JSON

from . import Base


class FunctionModel(Base):
    __tablename__ = "functions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    specification = Column(JSON)
