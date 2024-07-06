from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    is_admin: Optional[bool] = False

class UserCreate(UserBase):
    name: str
    email: str
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
