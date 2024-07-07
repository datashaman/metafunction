from decouple import config  # type: ignore

SECRET_KEY = config("SECRET_KEY")
SQLALCHEMY_DATABASE_URL = config("SQLALCHEMY_DATABASE_URL")
