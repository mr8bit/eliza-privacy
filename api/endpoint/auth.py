from datetime import datetime, timedelta
from auth.service import get_current_active_user

from auth.service import authenticate
from auth.token import create_access_token
from fastapi import APIRouter, Depends, Header
from schemas.users import Token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from models.fake import fake_users_db
from fastapi import Depends, FastAPI, HTTPException, status
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas.users import UserRegister
from models.users import User
from auth.security import get_password_hash
from models.api_token import Token as TokenAPI
from starlette.status import HTTP_302_FOUND, HTTP_403_FORBIDDEN
from typing import Optional
from fastapi.security.utils import get_authorization_scheme_param
from auth.service import get_current_user

from auth.apikey import get_api_key

app = APIRouter()


@app.post('/verify')
async def verify(Authorization: Optional[str] = Header(None)):
    if Authorization:
        type, _, value = Authorization.split(' ')
        print(Authorization.split(' '))
        if type == 'Token':
            token = await get_api_key(value)
            user = await token.user
            if user:
                return {"email": user.email,
                        "first_name": user.first_name,
                        "is_active": user.is_active,
                        "last_name": user.last_name}
        if type == 'Bearer':
            user = await get_current_user(value)
            if user:
                return {"email": user.email,
                        "first_name": user.first_name,
                        "is_active": user.is_active,
                        "last_name": user.last_name}
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Not passed token in Header"
        )


@app.post('/create_token')
async def create_token(current_user: User = Depends(get_current_active_user)):
    """
        Создание токена для API
    :param current_user:
    :return:
    """
    token = await TokenAPI.get_or_none(user=current_user)
    if token:
        raise HTTPException(
            status_code=HTTP_302_FOUND, detail="Token already exist"
        )
    else:
        token = await TokenAPI.create(user=current_user)
        return {"token": token.key}


@app.post('/register')
async def register(user: UserRegister):
    """
        Регистрация пользователя

    Args:
        - user: UserRegister
    """
    user.password = get_password_hash(user.password)
    user_obj = await User.create(**user.dict(exclude_unset=True))
    print(user_obj)
    return {"complete": True}


@app.post("/jwt", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Получить токен доступа
    :param form_data:
    :return:
    """
    user = await authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "email": user.email,
            "fist_name": user.first_name,
            "last_name": user.last_name,
        }, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
