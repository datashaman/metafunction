from typing import Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from metafunction.models import get_session, Session, select, User, UserPublic
from metafunction.security.oauth2 import create_access_token, get_current_user


router = APIRouter()


@router.get("/me", response_model=User, response_model_exclude={"password"})
async def me(current_user: User = Depends(get_current_user)) -> UserPublic:
    return UserPublic.from_orm(current_user)


@router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
) -> Dict[str, str]:
    statement = select(User).where(User.email == form_data.username)
    user = session.exec(statement).first()

    if not (user and user.password == form_data.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type": "bearer"}
