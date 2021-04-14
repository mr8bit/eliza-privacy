from auth.service import get_current_active_user
from fastapi import APIRouter
from fastapi import Depends
from schemas.users import User
from auth.apikey import get_api_key
from fastapi.security.api_key import APIKey

app = APIRouter()


@app.get("/secure_endpoint")
async def get_open_api_endpoint(api_key: APIKey = Depends(get_api_key)):
    response = "How cool is this?"
    return response


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
        Информация о пользователе
    :param current_user: Пользователь
    :return:
    """
    return {"email": current_user.email,
            "first_name": current_user.first_name,
            "is_active": current_user.is_active,
            "last_name": current_user.last_name}


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """
        Список где пользователь владелец
    :param current_user:
    :return:
    """
    return [{"item_id": "Foo", "owner": current_user.email}]
