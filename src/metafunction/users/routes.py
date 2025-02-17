from typing import List, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from metafunction.auth import get_admin_user
from metafunction.database import Session, get_session
from metafunction.responses import FailResponse, SuccessResponse, fail_response, success_response
from metafunction.users import crud as users
from metafunction.users.models import UserCreate, UserPublic, UserUpdate

router = APIRouter()


@router.get(
    '/{user_id}',
    response_model=SuccessResponse[UserPublic],
    dependencies=[Depends(get_admin_user)],
)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
) -> JSONResponse:
    if user := users.get(session, user_id):
        return success_response(user=UserPublic.model_validate(user).model_dump())
    return fail_response(status_code=404, user_id='User not found')


@router.get(
    '/',
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
            for user in users.get_all(
                session,
                offset=offset,
                limit=limit,
            )
        ],
    )


@router.post(
    '/',
    response_model=SuccessResponse[UserPublic],
    dependencies=[Depends(get_admin_user)],
)
async def create_user(
    data: UserCreate,
    session: Session = Depends(get_session),
) -> JSONResponse:
    try:
        user = users.create(session, data)
        return success_response(status_code=201, user=UserPublic.model_validate(user).model_dump())
    except IntegrityError as exc:
        if 'UNIQUE constraint failed: user.name' in str(exc):
            return fail_response(name='User name exists')
        if 'UNIQUE constraint failed: user.email' in str(exc):
            return fail_response(email='User email exists')
        raise exc


@router.put(
    '/{user_id}',
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
    except IntegrityError as exc:
        if 'UNIQUE constraint failed: user.name' in str(exc):
            return fail_response(name='User name exists')
        if 'UNIQUE constraint failed: user.email' in str(exc):
            return fail_response(email='User email exists')
        raise exc
    return fail_response(status_code=404, user_id='User not found')


@router.delete(
    '/{user_id}',
    response_model=Union[SuccessResponse[UserPublic], FailResponse],
    dependencies=[Depends(get_admin_user)],
)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),  # pylint: disable=B008
) -> JSONResponse:
    if user := users.delete_by_id(session, user_id):
        return success_response(user=UserPublic.model_validate(user).model_dump())
    return fail_response(status_code=404, user_id='User not found')
