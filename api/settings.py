from decouple import config

SECRET_KEY = config('SECRET_KEY')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')
