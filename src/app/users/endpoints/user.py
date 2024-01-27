import json
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from src.app.auth.auth_handler import Auth
from src.app.auth.permission import get_user, get_this_user_or_superuser
from src.app.users.models import User
from src.app.users.schemas import UserMySchema, UserRegisterInSchema, UserPydantic, UserRegisterOutSchema, \
    UserUpdateInSchema

user_router = APIRouter()


@user_router.post('/register', response_model=UserRegisterOutSchema)
async def register_user(user_data: UserRegisterInSchema):
    """
    Регистрация нового пользователя и получения JWT access_token.

    Первый пользователь в базе данных, будет суперпользователем
    :param user_data: Данные пользователя согласно схемы UserRegisterInSchema.
    """
    # Если в базе данных отсутствуют пользователи, то первым создаем суперпользователя
    if not await User.first():
        user = await User.create(
            email=user_data.email,
            last_name=user_data.last_name,
            first_name=user_data.first_name,
            surname=user_data.surname,
            password=Auth.get_password_hash(
                user_data.password.get_secret_value()
            ),
            is_staff=True,
            is_superuser=True
        )
        await user.save()

    # Если пользователь с указанным email уже существует, вызываем исключение
    elif await User.get_or_none(email=user_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    # После валидации, сохраняем пользователя в базу данных
    else:
        user = await User.create(
            email=user_data.email,
            last_name=user_data.last_name,
            first_name=user_data.first_name,
            surname=user_data.surname,
            password=Auth.get_password_hash(
                user_data.password.get_secret_value()
            )
        )
        await user.save()

    # Получаем сериализуемый экземпляр модели pydantic, созданный на основе модели User
    user_json = await UserPydantic.from_tortoise_orm(user)
    # На основе полученных данных, получаем access_token
    token = Auth.get_token(data=json.loads(user_json.json()))

    # Добавляем сгенерированный токен и тип токена в схему UserRegisterOutSchema
    response = UserRegisterOutSchema(
        **user_data.model_dump(),
        token_type="bearer",
        access_token=token
    )
    return response


@user_router.get("/me", response_model=UserMySchema)
async def read_users_me(current_user: Annotated[User, Depends(get_user)]):
    """ Получение данных о текущем пользователе"""
    return current_user


@user_router.patch('/{pk}', response_model=UserMySchema)
async def update_user(
        pk: int,
        user_data: UserUpdateInSchema,
        current_user: Annotated[User, Depends(get_this_user_or_superuser)],
):
    """ Редактирование профиля пользователя """
    user = await User.get_or_none(id=pk)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    new_data = {k: v for k, v in user_data.model_dump().items() if v}
    await user.update_from_dict(new_data)
    await user.save()
    return user
