from fastapi import FastAPI
from api.routers import api_router
from tortoise.contrib.fastapi import register_tortoise
from config import settings

app = FastAPI(title=settings.PROJECT_NAME, version="0.0.1")

app.include_router(api_router)


register_tortoise(
    app,
    db_url=settings.DATABASE_URI,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=False,
    add_exception_handlers=True,
)
