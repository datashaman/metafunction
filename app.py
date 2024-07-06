
from fastapi import FastAPI
from api.endpoints import user

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
