import time
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from passlib.hash import bcrypt
import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from src.app.users.models import User
from src.config import settings

# TODO: секретный ключ хранится в .env файле
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class Auth:
    """ Менеджер авторизации """

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        """
        Возвращает пароль, хешированный с помощью bcrypt.

        :param password: Строка, которая будет хеширована bcrypt.
        """
        return bcrypt.hash(password)

    @classmethod
    def verify_password(cls, password: str, hash_string: str) -> bool:
        """
        Проверяет нехешированный пароль путем сравнения с хешированным паролем.

       :param password: Строка нехешированного пароля.
       :param hash_string: Строка хешированного пароля.
       """
        return bcrypt.verify(password, hash_string)

    @staticmethod
    def get_token(data: dict):
        """
        Генерирует JWT токен на основе пользовательских данных.

       :param data: Запись пользовательских данных.
       """
        to_encode = data.copy()
        to_encode.update({
            "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        })
        return jwt.encode(
            to_encode,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def decode_token(token: str) -> dict:
        """
        Декодирует токен JWT и возвращает декодированные данные, если токен действителен.

        :param token: JWT access token.
        """
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            return {}

    @classmethod
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
        """
        Вспомогательная функция, которая позволяет получить текущего аутентифицированного
        пользователя внутри конечной точки API и сделать конечную точку JWT защищенной

        :param token: JWT access token.
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = cls.decode_token(token)
            username: str = payload.get("email")
            if username is None:
                raise credentials_exception
        except:
            raise credentials_exception
        user = await User.get_or_none(email=username)
        if user is None:
            raise credentials_exception
        return user
