from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from src.app.auth.permission import get_user
from src.app.base.utils.file_manager import get_file_list, get_file
from src.app.files.models import StatusFileEnum
from src.app.files.schemas import FileBaseSchema
from src.app.users.models import User

file_router = APIRouter()


@file_router.get('/list', response_model=Page[FileBaseSchema])
async def get_file_data_list(
        current_user: Annotated[User, Depends(get_user)],
        status: StatusFileEnum = None,
        owner_email: str = None,
):
    """
    Получение списка файлов

    Обычный пользователь имеет право получить список только своих файлов. Администратор - файлы всех пользователей
    """
    file_list = await get_file_list(current_user, status, owner_email)
    return paginate(file_list)


@file_router.get('/{pk}')
async def get_file_data(
        current_user: Annotated[User, Depends(get_user)],
        pk: int
):
    return await get_file(current_user, pk)
