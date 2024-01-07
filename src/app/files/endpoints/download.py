from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.app.auth.permission import get_user
from src.app.users.models import User
from src.config import settings

download_router = APIRouter()


@download_router.get('')
async def download_file(
        current_user: Annotated[User, Depends(get_user)],
        file: str,
        user: str = None,
):
    """
    Отправка файла пользователю

    Скачивать разрешено в следующих случаях:
    1. Пользователь является владельцем файла
    2. Пользователь является администратором
    3. Файл публичный и не привязан к пользователю

    :param current_user: текущий пользователь
    :param file: Имя файла для скачивания (имя физическое, в папке DOCUMENT_DIR)
    :param user: Пользователь в формате user@example.com
    """
    # Формируем путь к файлу
    file = settings.DOCUMENTS_DIR / user / file
    # Проверяем наличие файла по сформированному адресу
    if file.exists():
        return FileResponse(
            path=file,
            filename=file.name,
        )
    # Если файл не найден, возвращаем ошибку
    raise HTTPException(
        status_code=404, detail="File not found"
    )
