from pydantic import Field, BaseModel, EmailStr


class GetTokenSchema(BaseModel):
    """ Схема авторизации для админ панели """
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "********"
            }
        }


class TokenSchema(BaseModel):
    """ Схема авторизации по токену """
    token_type: str
    access_token: str

    class Config:
        json_schema_extra = {
            "example": {
                "token_type": "Тип токена",
                "access_token": "Токен доступа"
            }
        }
