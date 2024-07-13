from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

from metafunction.crud import functions
from metafunction.database import (
    get_session,
    Session,
    select,
    Function,
    FunctionCreate,
    FunctionPublic,
)
from metafunction.helpers import success_response, fail_response
from metafunction.responses import SuccessResponse
from metafunction.security.oauth2 import get_current_user


router = APIRouter()


@router.post(
    "/",
    response_model=SuccessResponse[FunctionPublic],
    dependencies=[Depends(get_current_user)],
)
async def create_function(
    data: FunctionCreate, session: Session = Depends(get_session)
) -> JSONResponse:
    function = functions.create(session, data)
    return success_response(function=FunctionPublic.model_validate(function))


@router.get(
    "/",
    response_model=SuccessResponse[List[FunctionPublic]],
    dependencies=[Depends(get_current_user)],
)
async def read_functions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> JSONResponse:
    return success_response(
        functions=[
            FunctionPublic.model_validate(function)
            for function in functions.list(session, offset=offset, limit=limit)
        ]
    )


@router.get(
    "/{function_id}",
    response_model=SuccessResponse[FunctionPublic],
    dependencies=[Depends(get_current_user)],
)
async def read_function(
    function_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    if function := functions.get(session, function_id):
        return success_response(function=FunctionPublic.model_validate(function))
    return fail_response(status_code=404, function_id="Function not found")
