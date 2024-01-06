from fastapi import APIRouter

from src.app.users.schemas import UserBaseSchema, UserRegisterInSchema

user_router = APIRouter()


@user_router.post('/register', response_model=UserBaseSchema)
async def register_user(user: UserRegisterInSchema):
    print(user.password)
    return user
