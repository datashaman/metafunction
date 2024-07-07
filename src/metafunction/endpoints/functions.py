from fastapi import APIRouter, Depends, HTTPException
from typing import List, Sequence

from metafunction.models import (
    get_session,
    Session,
    select,
    Function,
    FunctionCreate,
    FunctionPublic,
)


router = APIRouter()


@router.post("/", response_model=Function)
async def create_function(
    data: FunctionCreate, session: Session = Depends(get_session)
) -> FunctionPublic:
    function = Function(**data.dict())
    session.add(function)
    session.commit()
    session.refresh(function)
    return FunctionPublic.from_orm(function)


@router.get("/", response_model=List[Function])
async def read_functions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
) -> List[FunctionPublic]:
    statement = select(Function).offset(offset).limit(limit)
    return [FunctionPublic.from_orm(function) for function in session.exec(statement)]


@router.get("/{function_id}", response_model=FunctionPublic)
async def read_function(
    function_id: int, session: Session = Depends(get_session)
) -> FunctionPublic:
    function = session.get(Function, function_id)
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    return FunctionPublic.from_orm(function)
