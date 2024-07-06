
from fastapi import APIRouter, HTTPException
from typing import List
from api.schemas.user import User

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
