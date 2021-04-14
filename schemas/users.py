from typing import Optional
from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str
    first_name: str
    last_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class User(BaseModel):
    email: str
    first_name: str
    last_name: str
    is_active: Optional[bool] = False


class UserInDB(User):
    hashed_password: str
