from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse

from src.app.auth.permission import get_user
from src.app.users.models import User
from src.app.base.utils.file_manager import get_file_data

download_router = APIRouter()


@download_router.get('/{pk}')
async def download_file(
        current_user: Annotated[User, Depends(get_user)],
        pk: int,
):
    """
    Отправка файла пользователю

    Скачивать разрешено в следующих случаях:
    1. Пользователь является владельцем файла
    2. Пользователь является администратором
    3. Файл публичный и не привязан к пользователю

    :param current_user: текущий пользователь</br>
    :param pk: ID файла
    # :param filename: Имя файла для скачивания (имя физическое, в хранилище DOCUMENT_DIR)</br>
    # :param owner: Владелец файла в формате user@example.com (опционально, для получения приватного файла)</br>
    """
    # Ищем файл в базе данных проверяем права доступа и получаем о нем информацию
    file_data = await get_file_data(current_user=current_user, pk=pk)
    # Проверяем наличие файла по сформированному адресу и отправляем файл пользователю
    if file_data.get("path").exists():
        return FileResponse(**file_data)

    # Если файл не найден, возвращаем ошибку
    raise HTTPException(
        status_code=404, detail="File not found"
    )
