import traceback
from typing import Any

from fastapi import HTTPException
from fastapi.responses import JSONResponse

from metafunction.responses import ErrorResponse, FailResponse, SuccessResponse


def error_response(exc: HTTPException) -> JSONResponse:
    stack = traceback.format_exception(type(exc), exc, exc.__traceback__)
    error_response = ErrorResponse(
        message=exc.detail,
        code=exc.status_code,
        data={'stack': stack},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(),
    )


def fail_response(status_code: int = 400, **data: Any) -> JSONResponse:
    response = FailResponse(data=data)
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(),
    )


def success_response(status_code: int = 200, **data: Any) -> JSONResponse:
    response = SuccessResponse(data=data)
    return JSONResponse(
        status_code=status_code,
        content=response.model_dump(),
    )
