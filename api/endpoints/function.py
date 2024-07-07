from fastapi import APIRouter, Depends, HTTPException
from typing import List

from api.models import get_session, Session, select, Function


router = APIRouter()


@router.post("/", response_model=Function)
async def create_function(function: Function, session: Session = Depends(get_session)):
    session.add(function)
    session.commit()
    session.refresh(function)
    return function


@router.get("/", response_model=List[Function])
async def read_functions(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    statement = select(Function).offset(offset).limit(limit)
    return session.exec(statement).all()


@router.get("/{function_id}", response_model=Function)
async def read_function(function_id: int, session: Session = Depends(get_session)):
    function = session.get(Function, function_id)
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    return function
