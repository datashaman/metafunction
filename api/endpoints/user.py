
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from api.schemas.user import User
from api.security.oauth2 import get_current_user

router = APIRouter()

users = []

@router.post("/", response_model=User)
def create_user(user: User):
    users.append(user)
    return user

@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@router.get("/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
