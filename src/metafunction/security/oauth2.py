from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from metafunction.crud import users
from metafunction.database import get_session, Session, select, User
from metafunction.helpers import fail_response
from metafunction.settings import SECRET_KEY


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(email: str) -> str:
    data = {
        "sub": email,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)
) -> Optional[User]:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Unauthorized",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if (email := payload.get("sub")) is None:
            raise credentials_exception
    except jwt.PyJWTError as exc:
        raise credentials_exception
    return users.get_by_email(session, email)


async def get_admin_user(
    current_user: User = Depends(get_current_user),
) -> Optional[User]:
    if not (current_user and current_user.is_admin):
        raise HTTPException(status_code=403, detail="You are not an admin")
    return current_user
