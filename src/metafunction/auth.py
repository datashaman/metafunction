from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from metafunction.crud import users
from metafunction.database import Session, User, get_session
from metafunction.settings import ACCESS_TOKEN_ALGORITHM, SECRET_KEY

get_token = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(token: str = Depends(get_token), session: Session = Depends(get_session)) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=401,
        detail='Unauthorized',
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        if (email := payload.get('sub')) is None:
            raise credentials_exception
    except jwt.PyJWTError as exc:
        raise credentials_exception from exc
    return users.get_by_email(session, email)


async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    if not (current_user and current_user.is_admin):
        raise HTTPException(status_code=403, detail='You are not an admin')
    return current_user
