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
                "is_active": "Признак активности"
            }
        }


class UserMySchema(UserBaseSchema):
    """ Схема для получения данных о себе """
    last_name: str
    first_name: str
    surname: Optional[str]
    date_joined: datetime
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
                "date_joined": "Дата и время регистрации",
                "is_staff": "Признак персонала",
                "is_superuser": "Признак администратора",
            }
        }


class UserDetailSchema(UserMySchema):
    """ Схема с полной информацией о пользователе """
    last_login: Optional[datetime]
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
                "date_joined": "Дата и время регистрации",
                "is_staff": "Признак персонала",
                "is_superuser": "Признак администратора",
                "last_login": "Дата и время последнего входа",
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


class UserUpdateBaseInSchema(BaseModel):
    """ Схема для изменения профиля пользователя """
    last_name: Optional[str] = Field(None, max_length=30)
    first_name: Optional[str] = Field(None, max_length=30)
    surname: Optional[str] = Field(None, max_length=30)

    class Config:
        json_schema_extra = {
            "example": {
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
            }
        }


class UserUpdateInSchema(UserUpdateBaseInSchema):
    """ Схема для изменения данных пользователя """
    is_active: Optional[bool] = Field(None)
    is_staff: Optional[bool] = Field(None)
    is_superuser: Optional[bool] = Field(None)
    comments: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)",
                "is_active": "Признак активности",
                "is_staff": "Признак персонала",
                "is_superuser": "Признак администратора",
                "comments": "Комментарии",
            }
        }


UserPydantic = pydantic_model_creator(
    User,
    name='User',
)


class UserActiveSchema(BaseModel):
    """ Схема для активации пользователя """
    is_active: bool

    class Config:
        json_schema_extra = {
            "example": {
                "is_active": "Статус активности",
            }
        }
