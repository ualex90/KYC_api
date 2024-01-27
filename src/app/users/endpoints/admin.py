from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate, Page

from src.app.auth.permission import get_superuser
from src.app.users.models import User
from src.app.users.schemas import UserBaseSchema, UserDetailSchema, UserUpdateInSchema

admin_router = APIRouter()


@admin_router.get('/list', response_model=Page[UserBaseSchema])
async def get_list_users(
        current_user: Annotated[User, Depends(get_superuser)],
):
    """ Получение списка пользователей. Доступно только администратору """
    response = await User.all()
    # Возвращаем список с пагинацией
    return paginate(response)


@admin_router.get('/{pk}', response_model=UserDetailSchema)
async def get_detail_user(
        pk: int, current_user: Annotated[User, Depends(get_superuser)],
):
    """ Получение списка пользователей. Доступно только администратору """
    user = await User.get_or_none(id=pk)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    return user
