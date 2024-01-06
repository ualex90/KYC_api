import json

from fastapi import APIRouter, HTTPException
from starlette import status

from src.app.auth.auth_handler import Auth
from src.app.auth.schemas import GetTokenSchema, TokenSchema
from src.app.users.models import User
from src.app.users.schemas import UserRegisterInSchema, UserPydantic, UserRegisterOutSchema

user_router = APIRouter()


@user_router.post('/register', response_model=UserRegisterOutSchema)
async def register_user(user_data: UserRegisterInSchema):
    """
    Регистрация нового пользователя и получения JWT access_token.

    :param user_data: Данные пользователя согласно схемы UserRegisterInSchema.
    """
    # Если пользователь с указанным email уже существует, вызываем исключение
    if await User.get_or_none(email=user_data.email) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    # После валидации, сохраняем пользователя в базу данных
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


@user_router.post("/token", response_model=TokenSchema)
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
            token_type="bearer",
            access_token=Auth.get_token(data=json.loads(user_json.json()))
        )

    # Если почта или пароль не верные, возвращаем ошибку
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Wrong login details",
        headers={"WWW-Authenticate": "Bearer"},
    )
