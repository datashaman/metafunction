from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict, Union

from metafunction.database import (
    get_session,
    Session,
    select,
    User,
    UserCreate,
    UserUpdate,
    UserPublic,
)
from metafunction.helpers import success_response, fail_response
from metafunction.responses import SuccessResponse, FailResponse
from metafunction.security.oauth2 import get_admin_user


router = APIRouter()


@router.get("/{user_id}", response_model=SuccessResponse[UserPublic])
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> JSONResponse:
    user = session.get(User, user_id)
    if user:
        return success_response(user=UserPublic.model_validate(user).dict())

    return fail_response(
        data={
            "user_id": "User not found",
        },
    )


@router.get("/", response_model=SuccessResponse[List[UserPublic]])
async def get_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> JSONResponse:
    statement = select(User).offset(offset).limit(limit)
    return success_response(
        users=[
            UserPublic.model_validate(user).dict() for user in session.exec(statement)
        ]
    )


@router.post("/", response_model=SuccessResponse[UserPublic])
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> JSONResponse:
    user = User.model_validate(data.dict())
    session.add(user)
    session.commit()
    session.refresh(user)
    return success_response(user=UserPublic.model_validate(user).dict())


@router.put(
    "/{user_id}", response_model=Union[SuccessResponse[UserPublic], FailResponse]
)
async def update_user(
    user_id: int,
    data: User,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> JSONResponse:
    user = session.get(User, user_id)
    if user:
        for key, value in data.dict().items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
        return success_response(user=UserPublic.model_validate(user).dict())
    return fail_response(
        data={
            "user_id": "User not found",
        },
    )


@router.delete(
    "/{user_id}", response_model=Union[SuccessResponse[UserPublic], FailResponse]
)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_admin_user),
) -> JSONResponse:
    user = session.get(User, user_id)
    if user:
        session.delete(user)
        session.commit()
        return success_response(user=UserPublic.model_validate(user).dict())
    return fail_response(
        data={
            "user_id": "User not found",
        },
    )
