from typing import Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from metafunction.auth import get_current_user
from metafunction.database import Session, get_session
from metafunction.responses import FailResponse, SuccessResponse, fail_response, success_response
from metafunction.users import crud as users
from metafunction.users.models import User, UserPublic


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


router = APIRouter()


@router.get('/me', response_model=SuccessResponse[UserPublic])
async def me(current_user: User = Depends(get_current_user)) -> JSONResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    return success_response(user=UserPublic.model_validate(current_user))


@router.post('/token', response_model=Union[Token, FailResponse])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Union[Token, JSONResponse]:
    user = users.get_by_email(session, email=form_data.username)
    if not (user and user.password == form_data.password):
        return fail_response(username='Incorrect username or password')
    return Token(access_token=user.create_access_token())
