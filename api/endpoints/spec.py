
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from api.schemas.spec import OpenAPISpec
from api.database import get_db, OpenAPISpecModel

router = APIRouter()

@router.post("/", response_model=OpenAPISpec)
def create_spec(spec: OpenAPISpec, db: Session = Depends(get_db)):
    db_spec = OpenAPISpecModel(name=spec.name, specification=spec.specification)
    db.add(db_spec)
    db.commit()
    db.refresh(db_spec)
    return db_spec

@router.get("/", response_model=List[OpenAPISpec])
def read_specs(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    specs = db.query(OpenAPISpecModel).offset(skip).limit(limit).all()
    return specs

@router.get("/{spec_id}", response_model=OpenAPISpec)
def read_spec(spec_id: int, db: Session = Depends(get_db)):
    spec = db.query(OpenAPISpecModel).filter(OpenAPISpecModel.id == spec_id).first()
    if spec is None:
        raise HTTPException(status_code=404, detail="Spec not found")
    return spec
