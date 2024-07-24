from typing import Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from metafunction.database import Session, get_session
from metafunction.repositories import users
from metafunction.settings import ACCESS_TOKEN_ALGORITHM, SECRET_KEY
from metafunction.users.models import User

get_token = OAuth2PasswordBearer(tokenUrl='token')


def get_current_user(token: str = Depends(get_token), session: Session = Depends(get_session)) -> Optional[User]:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
    return session.exec(users.base_query(session).where(User.email == payload['sub'])).first()


def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    if not (current_user and current_user.is_admin):
        raise HTTPException(status_code=403, detail='You are not an admin')
    return current_user
