import os

PROJECT_NAME = "Eliza Privacy Bus"
SERVER_HOST = os.environ.get("SERVER_HOST")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

APPS_MODELS = [
    "models.users",
    "models.api_token",
    "aerich.models",
]
# Secret key
SECRET_KEY = b"awubsyb872378t^*TG8y68&*&&*8y8yg9POB)*896ft7CR^56dfYUv"


DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("POSTGRES_HOST")}:5432/' \
               f'{os.environ.get("POSTGRES_DB")}'

