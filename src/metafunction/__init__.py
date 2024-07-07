from fastapi import FastAPI

from metafunction.endpoints import user, auth
from metafunction.models import create_tables

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


@app.on_event("startup")
async def on_startup() -> None:
    create_tables()
