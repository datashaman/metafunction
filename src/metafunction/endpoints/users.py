from fastapi import APIRouter, Depends, HTTPException
from typing import List, Sequence, Dict

from metafunction.models import (
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


@router.get(
    "/{user_id}", response_model=UserPublic, response_model_exclude={"password"}
)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    user = session.get(User, user_id)
    if user:
        return UserPublic.from_orm(user)
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=List[UserPublic], response_model_exclude={"password"})
async def get_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> Sequence[UserPublic]:
    statement = select(User).offset(offset).limit(limit)
    return [UserPublic.from_orm(user) for user in session.exec(statement)]


@router.post("/", response_model=UserPublic)
async def create_user(
    user: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> UserPublic:
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserPublic.from_orm(user)


@router.put(
    "/{user_id}", response_model=UserPublic, response_model_exclude={"password"}
)
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
        return UserPublic.from_orm(user)
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
        return UserPublic.from_orm(user)
    raise HTTPException(status_code=404, detail="User not found")
