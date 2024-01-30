from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import paginate, Page

from src.app.auth.permission import get_superuser
from src.app.files.models import File
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


@admin_router.patch('/{pk}', response_model=UserDetailSchema)
async def update_user(
        pk: int,
        user_data: UserUpdateInSchema,
        current_user: Annotated[User, Depends(get_superuser)],
):
    """
    Редактирование пользователя. Доступно только администратору

    Можно изменить все доступные редактируемые поля. Можно изменить как одно, так и несколько полей
    """
    user = await User.get_or_none(id=pk)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    new_data = {k: v for k, v in user_data.model_dump().items() if v is not None}
    await user.update_from_dict(new_data)
    await user.save()
    return user


@admin_router.delete('/{pk}')
async def delete_user(
        pk: int,
        current_user: Annotated[User, Depends(get_superuser)],
):
    """ Удаление пользователя по ID. Доступно только администратору"""
    user = await User.get_or_none(id=pk)
    if not user:
        raise HTTPException(
            status_code=404, detail="User not found"
        )
    # Ввиду отсутствия прямой поддержки ForeingKey у Tortoise ORM
    # и невозможности применения related_name по причине циркулярного импорта,
    # самостоятельно устанавливаем в None поле owner во всх записях связанных файлов
    async for file in File.filter(owner=user.id):
        file.owner = None
        await file.save()
    await user.delete()
    return {'detail': 'deleted'}
