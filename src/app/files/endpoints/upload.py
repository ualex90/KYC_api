from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, Depends

from src.app.auth.permission import get_user, get_superuser
from src.app.base.utils.file_manager import save_file
from src.app.files.services import send_message_files_add
from src.app.users.models import User

upload_router = APIRouter()


@upload_router.post('')
async def upload_file(
        current_user: Annotated[User, Depends(get_user)],
        file: UploadFile = File(...)
):
    """
    Загрузка одного файла
    """
    # Получаем путь для сохранения и сохраняем
    await save_file(upload_file=file, user=current_user)
    # Отправляем сообщения администраторам
    await send_message_files_add(current_user, file)
    return {"file": file.filename}


@upload_router.post('/multiple')
async def upload_multiple_file(
        current_user: Annotated[User, Depends(get_user)],
        files: List[UploadFile] = File(...)
):
    """
    Загрузка нескольких файлов
    """
    # Итерируем список файлов, получаем путь для сохранения и сохраняем
    for file in files:
        await save_file(upload_file=file, user=current_user)
    # Отправляем сообщения администраторам
    await send_message_files_add(current_user, files)
    return {"files": [i.filename for i in files], "total": len(files)}


@upload_router.post('/public')
async def upload_public_file(
        current_user: Annotated[User, Depends(get_superuser)],
        file: UploadFile = File(...)
):
    """
    Загрузка одного публичного файла

    Доступно только для администратора
    """
    # Получаем путь для сохранения и сохраняем
    await save_file(upload_file=file, user=current_user, is_public=True)
    return {"file": file.filename}


@upload_router.post('/public/multiple')
async def upload_multiple_public_file(
        current_user: Annotated[User, Depends(get_superuser)],
        files: List[UploadFile] = File(...)
):
    """
    Загрузка нескольких публичных файлов

    Доступно только для администратора
    """
    # Итерируем список файлов, получаем путь для сохранения и сохраняем
    for file in files:
        await save_file(upload_file=file, user=current_user, is_public=True)

    return {"files": [i.filename for i in files], "total": len(files)}
