from typing import Dict, Union

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from metafunction.crud import users
from metafunction.database import get_session, Session, select, User, UserPublic
from metafunction.helpers import success_response, fail_response
from metafunction.responses import SuccessResponse, FailResponse
from metafunction.models.token import Token
from metafunction.security.oauth2 import create_access_token, get_current_user


router = APIRouter()


@router.get("/me", response_model=SuccessResponse[UserPublic])
async def me(current_user: User = Depends(get_current_user)) -> JSONResponse:
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return success_response(user=UserPublic.model_validate(current_user))


@router.post("/token", response_model=Union[Token, FailResponse])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Union[Token, JSONResponse]:
    user = users.get_by_email(session, email=form_data.username)
    if not (user and user.password == form_data.password):
        return fail_response(username="Incorrect username or password")
    return Token(access_token=create_access_token(user))
