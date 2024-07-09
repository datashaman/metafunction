from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict

from metafunction.database import (
    get_session,
    Session,
    select,
    User,
    UserCreate,
    UserUpdate,
    UserPublic,
)
from metafunction.security.oauth2 import get_admin_user


router = APIRouter()


@router.get("/{user_id}", response_model=UserPublic)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    user = session.get(User, user_id)
    if user:
        return UserPublic.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=List[UserPublic])
async def get_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> List[UserPublic]:
    statement = select(User).offset(offset).limit(limit)
    return [UserPublic.model_validate(user) for user in session.exec(statement)]


@router.post("/", response_model=UserPublic)
async def create_user(
    user: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPublic.model_validate(user)


@router.put("/{user_id}", response_model=UserPublic)
async def update_user(
    user_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    user = session.get(User, user_id)
    if user:
        for key, value in data.dict().items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
        return UserPublic.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return UserPublic.model_validate(user)
    raise HTTPException(status_code=404, detail="User not found")
