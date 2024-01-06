from pydantic import Field, BaseModel, EmailStr, SecretStr


class UserBaseSchema(BaseModel):
    """ Базовая схема пользователя """
    email: EmailStr
    last_name: str
    first_name: str
    surname: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "last_name": "Фамилия",
                "first_name": "Имя",
                "surname": "Отчество (при наличии)"
            }
        }


class UserRegisterInSchema(BaseModel):
    """ Свойства для получения через API при регистрации """
    email: EmailStr
    password: SecretStr
    last_name: str
    first_name: str
    surname: str = None

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
