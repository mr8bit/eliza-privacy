from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
        Верефикация пароля
    :param plain_password: Введеный пароль
    :param hashed_password: Хэш пааоля (береться из бд)
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
        Получить Хэш Пароля
    :param password:
    :return:
    """
    return pwd_context.hash(password)
