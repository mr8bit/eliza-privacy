from fastapi import APIRouter
from api.endpoint.auth import app as auth_api
from api.endpoint.users import app as users_api
api_router = APIRouter()

api_router.include_router(auth_api,  tags=["login"])
api_router.include_router(users_api,  tags=["users"])
