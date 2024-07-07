from fastapi import APIRouter, Depends, HTTPException
from typing import List, Sequence

from metafunction.models import get_session, Session, select, User
from metafunction.security.oauth2 import get_admin_user


router = APIRouter()


@router.get("/me", response_model=User, response_model_exclude={"password"})
async def me(current_user: User = Depends(get_admin_user)) -> User:
    return current_user


@router.get("/{user_id}", response_model=User, response_model_exclude={"password"})
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> User:
    user = session.get(User, user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/", response_model=List[User], response_model_exclude={"password"})
async def get_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> Sequence[User]:
    statement = select(User).offset(offset).limit(limit)
    return session.exec(statement).all()


@router.post("/", response_model=User, response_model_exclude={"password"})
async def create_user(
    user: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.put("/{user_id}", response_model=User, response_model_exclude={"password"})
async def update_user(
    user_id: int,
    updates: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> User:
    user = session.get(User, user_id)
    if user:
        user.update(updates)
        session.commit()
        session.refresh(user)
        return user
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> dict:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")
