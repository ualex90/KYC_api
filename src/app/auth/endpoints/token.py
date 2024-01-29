import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.app.auth.auth_handler import Auth
from src.app.auth.schemas import GetTokenSchema, TokenSchema
from src.app.users.models import User
from src.app.users.schemas import UserPydantic

token_router = APIRouter()
swagger_router = APIRouter()


@token_router.post('', response_model=TokenSchema)
async def get_token(user_data: GetTokenSchema):
    """
    Получение нового JWT access_token.

    :param user_data: Данные согласно схеме GetTokenSchema.
    """
    # Ищем пользователя и проверяем пароль
    user = await User.get_or_none(email=user_data.email)
    if user and Auth.verify_password(user_data.password, user.password):
        user_json = await UserPydantic.from_tortoise_orm(user)
        return TokenSchema(
            token_type="Bearer",
            access_token=Auth.get_token(data=json.loads(user_json.json()))
        )

    # Если почта или пароль не верные, возвращаем ошибку
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong login details",
        headers={"WWW-Authenticate": "Bearer"},
    )


@swagger_router.post("/token", response_model=TokenSchema)
async def swagger_login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Авторизация для использования в Swagger (OAuth2PasswordRequestForm).

    :param form_data: Данные из формы авторизации
    """
    user = await User.get_or_none(email=form_data.username)
    if user and Auth.verify_password(form_data.password, user.password):
        user_json = await UserPydantic.from_tortoise_orm(user)
        return TokenSchema(
            token_type="Bearer",
            access_token=Auth.get_token(data=json.loads(user_json.json()))
        )

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong login details",
        headers={"WWW-Authenticate": "Bearer"},
    )
