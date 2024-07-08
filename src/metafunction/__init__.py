from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from metafunction.endpoints import auth, credentials, functions, users
from metafunction.models import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(credentials.router, prefix="/credentials", tags=["credentials"])
app.include_router(functions.router, prefix="/functions", tags=["functions"])
app.include_router(users.router, prefix="/users", tags=["users"])
