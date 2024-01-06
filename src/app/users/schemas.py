from typing import Optional

from pydantic import Field, BaseModel, EmailStr, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.users.models import User


class UserBaseSchema(BaseModel):
    """ Базовая схема пользователя """
    email: EmailStr
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    surname: Optional[str] = Field(None, max_length=30)  # Опциональный тип, так как поле может быть None,

    class Config:
        json_schema_extra = {
            "example": {
                "id": "Идентификатор",
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)"
            }
        }


class UserRegisterInSchema(UserBaseSchema):
    """ Схема для получения через API при регистрации """
    password: SecretStr = Field(..., max_length=30)

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "********",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
            }
        }


class UserRegisterOutSchema(UserBaseSchema):
    """ Схема для ответа при регистрации """
    token_type: str = None
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "id": "Идентификатор",
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
                "token_type": "Тип токена",
                "access_token": "Токен доступа",
            }
        }


class UserListSchema(UserBaseSchema):
    """ Схема для получения списка пользователей """
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ID",
                "email": "user@example.com",
                "password": "********",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
            }
        }


UserPydantic = pydantic_model_creator(
    User,
    name='User',
)
