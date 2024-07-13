import os

from decouple import Config, RepositoryEnv

STAGE = os.getenv('STAGE', 'local')
config = Config(RepositoryEnv(f'.env.{STAGE}'))

ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', default=30, cast=int)
ACCESS_TOKEN_ALGORITHM: str = config('ACCESS_TOKEN_ALGORITHM', default='HS256')
SECRET_KEY: str = config('SECRET_KEY')
SQLALCHEMY_DATABASE_URL: str = config('SQLALCHEMY_DATABASE_URL', 'sqlite:///:memory:')
