
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My OpenAPI Management System"
    admin_email: str
    items_per_user: int = 50
    secret_key: str = "your_secret_key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
