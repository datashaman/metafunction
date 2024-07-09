from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List

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


router = APIRouter()


@router.post("/", response_model=SuccessResponse[FunctionPublic])
async def create_function(
    data: FunctionCreate, session: Session = Depends(get_session)
) -> JSONResponse:
    function = Function.model_validate(data.dict())
    session.add(function)
    session.commit()
    session.refresh(function)
    return success_response(data=FunctionPublic.model_validate(function))


@router.get("/", response_model=SuccessResponse[List[FunctionPublic]])
async def read_functions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> JSONResponse:
    statement = select(Function).offset(offset).limit(limit)
    return success_response(
        data=[
            FunctionPublic.model_validate(function)
            for function in session.exec(statement)
        ]
    )


@router.get("/{function_id}", response_model=SuccessResponse[FunctionPublic])
async def read_function(
    function_id: int, session: Session = Depends(get_session)
) -> JSONResponse:
    function = session.get(Function, function_id)
    if function is None:
        return fail_response(
            data={
                "function_id": "Function not found",
            },
            status_code=404,
        )
    return success_response(data=FunctionPublic.model_validate(function))
