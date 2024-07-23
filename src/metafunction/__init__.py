from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlmodel import SQLModel

from metafunction.database import engine
from metafunction.endpoints import auth, credentials, functions, users
from metafunction.responses import error_response


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix='/auth', tags=['auth'])
app.include_router(credentials.router, prefix='/credentials', tags=['credentials'])
app.include_router(functions.router, prefix='/functions', tags=['functions'])
app.include_router(users.router, prefix='/users', tags=['users'])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return error_response(exc)
