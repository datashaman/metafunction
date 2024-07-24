from typing import List

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from metafunction.auth import get_current_user
from metafunction.database import Session, get_session
from metafunction.functions.models import Function, FunctionCreate, FunctionPublic, FunctionUpdate
from metafunction.repositories import functions
from metafunction.responses import SuccessResponse, fail_response, success_response
from metafunction.users.models import User

router = APIRouter()


@router.post(
    '/',
    response_model=SuccessResponse[FunctionPublic],
)
async def create_function(
    data: FunctionCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    function = functions.create(session, current_user, data)
    return success_response(status_code=201, function=FunctionPublic.model_validate(function))


@router.get(
    '/',
    response_model=SuccessResponse[List[FunctionPublic]],
)
async def read_functions(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    return success_response(
        functions=[
            FunctionPublic.model_validate(function)
            for function in functions.get_all(session, current_user, offset=offset, limit=limit)
        ]
    )


@router.get(
    '/{function_id}',
    response_model=SuccessResponse[FunctionPublic],
)
async def read_function(
    function_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    if function := functions.get(session, current_user, function_id):
        return success_response(function=FunctionPublic.model_validate(function))
    return fail_response(status_code=404, function_id='Function not found')


@router.put(
    '/{function_id}',
    response_model=SuccessResponse[FunctionPublic],
)
async def update_function(
    function_id: int,
    data: FunctionUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    if function := functions.update_by_id(session, current_user, function_id, data):
        return success_response(function=FunctionPublic.model_validate(function))
    return fail_response(status_code=404, function_id='Function not found')


@router.delete(
    '/{function_id}',
    response_model=SuccessResponse[FunctionPublic],
)
async def delete_function(
    function_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> JSONResponse:
    if function := functions.delete_by_id(session, current_user, function_id):
        return success_response(function=FunctionPublic.model_validate(function))
    return fail_response(status_code=404, function_id='Function not found')
