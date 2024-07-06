from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from api.settings import SQLALCHEMY_DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from api.models.function import FunctionModel
from api.models.user import UserModel

Base.metadata.create_all(bind=engine)

def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
