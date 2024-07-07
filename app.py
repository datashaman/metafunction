
from fastapi import FastAPI
from sqlmodel import SQLModel

from api.endpoints import user, auth
from api.models import engine

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    SQLModel.metadata.create_all(engine)


app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
