
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My OpenAPI Management System"
    admin_email: str
    items_per_user: int = 50

    class Config:
        env_file = ".env"

settings = Settings()
