from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from fastapi import Security, HTTPException
from starlette.status import HTTP_403_FORBIDDEN
import binascii
from fastapi import HTTPException, status

from models.api_token import Token

API_KEY_NAME = "Token"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: str = Security(api_key_header)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Token"},
    )
    try:
        token = await Token.get_or_none(key=api_key)
        if token:
            return token
    except:
        raise credentials_exception
