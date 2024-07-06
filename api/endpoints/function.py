
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.function import Function
from api.models import get_db, FunctionModel

router = APIRouter()

@router.post("/", response_model=Function)
def create_function(function: Function, db: Session = Depends(get_db)):
    db_function = FunctionModel(name=function.name, specification=function.specification)
    db.add(db_function)
    db.commit()
    db.refresh(db_function)
    return db_function

@router.get("/", response_model=List[Function])
def read_functions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    functions = db.query(FunctionModel).offset(skip).limit(limit).all()
    return functions

@router.get("/{function_id}", response_model=Function)
def read_function(function_id: int, db: Session = Depends(get_db)):
    function = db.query(FunctionModel).filter(FunctionModel.id == function_id).first()
    if function is None:
        raise HTTPException(status_code=404, detail="Function not found")
    return function
