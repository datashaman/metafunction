from fastapi import APIRouter, Depends, HTTPException
from typing import List, Sequence

from metafunction.database import (
    get_session,
    Session,
    select,
    Function,
    FunctionCreate,
    FunctionPublic,
)


router = APIRouter()


@router.post("/", response_model=FunctionPublic)
async def create_function(
    data: FunctionCreate, session: Session = Depends(get_session)
) -> FunctionPublic:
    function = Function(**data.dict())
    session.add(function)
    session.commit()
    session.refresh(function)
    return FunctionPublic.model_validate(function)


@router.get("/", response_model=List[FunctionPublic])
async def read_functions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> List[FunctionPublic]:
    statement = select(Function).offset(offset).limit(limit)
    return [
        FunctionPublic.model_validate(function) for function in session.exec(statement)
    ]


@router.get("/{function_id}", response_model=FunctionPublic)
async def read_function(
    function_id: int, session: Session = Depends(get_session)
) -> FunctionPublic:
    function = session.get(Function, function_id)
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    return FunctionPublic.model_validate(function)
