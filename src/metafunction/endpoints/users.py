from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from typing import List, Dict, Union

from metafunction.crud import users
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


@router.get(
    "/{user_id}",
    response_model=SuccessResponse[UserPublic],
    dependencies=[Depends(get_admin_user)],
)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
) -> JSONResponse:
    if user := users.get(session, user_id):
        return success_response(user=UserPublic.model_validate(user).model_dump())
    return fail_response(status_code=404, user_id="User not found")


@router.get(
    "/",
    response_model=SuccessResponse[List[UserPublic]],
    dependencies=[Depends(get_admin_user)],
)
async def get_users(
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
) -> JSONResponse:
    return success_response(
        users=[
            UserPublic.model_validate(user).model_dump()
            for user in users.list(
                session,
                offset=offset,
                limit=limit,
            )
        ]
    )


@router.post(
    "/",
    response_model=SuccessResponse[UserPublic],
    dependencies=[Depends(get_admin_user)],
)
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session),
) -> JSONResponse:
    try:
        user = users.create(session, data)
        return success_response(user=UserPublic.model_validate(user).model_dump())
    except IntegrityError as e:
        if "UNIQUE constraint failed: user.name" in str(e):
            return fail_response(name="User name exists")
        if "UNIQUE constraint failed: user.email" in str(e):
            return fail_response(email="User email exists")
        raise e


@router.put(
    "/{user_id}",
    response_model=Union[SuccessResponse[UserPublic], FailResponse],
    dependencies=[Depends(get_admin_user)],
)
async def update_user(
    user_id: int,
    data: UserUpdate,
    session: Session = Depends(get_session),
) -> JSONResponse:
    try:
        if user := users.update_by_id(session, user_id, data):
            return success_response(user=UserPublic.model_validate(user).model_dump())
    except IntegrityError as e:
        if "UNIQUE constraint failed: user.name" in str(e):
            return fail_response(name="User name exists")
        if "UNIQUE constraint failed: user.email" in str(e):
            return fail_response(email="User email exists")
        raise e
    return fail_response(status_code=404, user_id="User not found")


@router.delete(
    "/{user_id}",
    response_model=Union[SuccessResponse[UserPublic], FailResponse],
    dependencies=[Depends(get_admin_user)],
)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
) -> JSONResponse:
    if user := users.delete_by_id(session, user_id):
        return success_response(user=UserPublic.model_validate(user).model_dump())
    return fail_response(status_code=404, user_id="User not found")
