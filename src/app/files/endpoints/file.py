from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi_pagination import paginate, Page

from src.app.auth.permission import get_user
from src.app.base.utils.file_manager import get_file_list
from src.app.files.models import StatusFileEnum
from src.app.files.schemas import FileBaseSchema
from src.app.users.models import User

file_router = APIRouter()


@file_router.get('/list', response_model=Page[FileBaseSchema])
async def get_files(
        current_user: Annotated[User, Depends(get_user)],
        status: StatusFileEnum = None,
        owner: str = None,
):
    """
    Получение списка файлов

    Обычный пользователь имеет право получить список только своих файлов. Администратор - файлы всех пользователей
    """
    file_list = await get_file_list(current_user, status, owner)
    return paginate(file_list)

