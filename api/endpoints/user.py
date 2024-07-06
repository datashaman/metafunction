
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.models import get_db, Session, UserModel
from api.schemas.user import User
from api.security.oauth2 import get_admin_user

router = APIRouter()


@router.post("/", response_model=User, response_model_exclude={"password"})
async def create_user(user: User, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    db_user = UserModel(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return user


@router.get("/me", response_model=User, response_model_exclude={"password"})
async def me(current_user: User = Depends(get_admin_user)):
    return current_user


@router.get("/{user_id}", response_model=User, response_model_exclude={"password"})
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if db_user:
        return db_user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=List[User], response_model_exclude={"password"})
async def get_users(offset: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: User = Depends(get_admin_user)):
    return db.query(UserModel).offset(offset).limit(limit).all()
