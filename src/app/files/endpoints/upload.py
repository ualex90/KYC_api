import shutil
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, Depends

from src.app.auth.permission import get_user
from src.app.base.utils.file_manager import save_file
from src.app.users.models import User

upload_router = APIRouter()


@upload_router.post('')
async def upload_file(
        current_user: Annotated[User, Depends(get_user)],
        file: UploadFile = File(...)
):
    """
    Загрузка одного файла

    :param current_user: текущий пользователь
    :param file: загружаемый файл
    """
    # Получаем путь для сохранения и сохраняем
    await save_file(file=file, user=current_user)
    return {"file_name": file.filename}


@upload_router.post('/multiple')
async def upload_multiple_file(
        current_user: Annotated[User, Depends(get_user)],
        files: List[UploadFile] = File(...)
):
    """
    Загрузка нескольких файлов

    :param current_user: текущий пользователь
    :param files: загружаемые файлы
    """
    # Итерируем список файлов, получаем путь для сохранения и сохраняем
    for file in files:
        await save_file(file=file, user=current_user)

    return {"file_name": [i.filename for i in files], "total": len(files)}
