from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from src.app.auth.permission import get_superuser
from src.app.users.models import User
from src.app.users.schemas import UserListSchema

admin_router = APIRouter()


@admin_router.get('/user', response_model=Page[UserListSchema])
async def get_users(
        current_user: Annotated[User, Depends(get_superuser)],
):
    response = await User.all()
    # Возвращаем список с пагинацией
    return paginate(response)
