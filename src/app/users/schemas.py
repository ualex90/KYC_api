from datetime import datetime
from typing import Optional

from pydantic import Field, BaseModel, EmailStr, SecretStr
from tortoise.contrib.pydantic import pydantic_model_creator

from src.app.users.models import User


class UserBaseSchema(BaseModel):
    """ Базовая модель пользователя """
    id: int
    email: EmailStr
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ID",
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
            }
        }


class UserMySchema(UserBaseSchema):
    """ Схема для получения данных о себе """
    last_name: str
    first_name: str
    surname: Optional[str]
    join_date: datetime
    is_staff: bool
    is_superuser: bool

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ID",
                "email": "user@example.com",
                "is_active": "Признак активности",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
                "join_date": "2024-01-01T00:00:00.000000Z",
                "is_staff": "Признак персонала",
                "is_superuser": "Признак администратора",
            }
        }


class UserDetailSchema(UserMySchema):
    """ Схема с полной информацией о пользователе """
    comments: Optional[str]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "ID",
                "email": "user@example.com",
                "is_active": "Признак активности",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
                "join_date": "2024-01-01T00:00:00.000000Z",
                "is_staff": "Признак персонала",
                "is_superuser": "Признак администратора",
                "comment": None
            }
        }


class UserRegisterBaseSchema(BaseModel):
    """ Базовая схема регистрации пользователя """
    email: EmailStr
    last_name: str = Field(..., max_length=30)
    first_name: str = Field(..., max_length=30)
    surname: Optional[str] = Field(None, max_length=30)  # Опциональный тип, так как поле может быть None,

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)"
            }
        }


class UserRegisterInSchema(UserRegisterBaseSchema):
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


class UserRegisterOutSchema(UserRegisterBaseSchema):
    """ Схема для ответа при регистрации """
    token_type: str = None
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
                "token_type": "Тип токена",
                "access_token": "Токен доступа",
            }
        }


UserPydantic = pydantic_model_creator(
    User,
    name='User',
)
