from fastapi.security import OAuth2PasswordBearer
from auth.security import verify_password
from fastapi import Depends, HTTPException, status
import jwt
from jwt import PyJWTError
from config.settings import SECRET_KEY, ALGORITHM
from schemas.users import UserInDB, TokenData, User
from models.users import User as UserDB

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="jwt")


async def get_userbd(email: str):
    user = await UserDB.get(email=email)
    if user:
        return user


async def authenticate(email: str, password: str):
    user = await UserDB.get(email=email)
    print(user.password)
    if not password:
        return False
    if not verify_password(password, user.password):
        return False
    return user



async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except PyJWTError:
        raise credentials_exception
    user = await UserDB.get(email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    print("get_current_active_user", current_user)
    return current_user
