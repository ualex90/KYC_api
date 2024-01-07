import shutil
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile, HTTPException
from tortoise.exceptions import ValidationError

from src.app.files.models import File, StatusFileEnum
from src.app.users.models import User
from src.config import settings


def get_path_to_save(file_name: str, user: User = None) -> Path:
    """
    Формирование пути к файлу и создание необходимых директорий

    :param user: Объект текущего пользователя
    :param file_name: Имя исходного файла
    :return: Объект Path содержащий путь к файлу
    """
    # Собираем путь к директории где будет храниться файл.
    if user:
        path = settings.DOCUMENTS_DIR / user.email  # Добавляем пользователя если файл приватный
    else:
        path = settings.PUBLIC_FILES_DIR  # Если пользователь не передан, файл делаем публичным

    # Если директория не существует, то создадим ее
    if not path.exists():
        path.mkdir(parents=True)

    # Формируем новое имя для файла состоящее из текущего времени по UTC с сохранением исходного расширения
    date = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    new_name = Path(file_name).with_stem(date)

    return path / new_name


async def save_file(upload_file: UploadFile, user: User = None):
    """ Сохранение загруженных файлов """
    # Формируем путь к файлу
    path = get_path_to_save(upload_file.filename, user)

    # Сохранение файла на диске
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Сохранение информации о файле в базе данных
    try:
        file = await File(
            file_name=upload_file.filename,
            size=upload_file.size,
            path=path.name,
            status=StatusFileEnum.UNDER_REVIEW if user else StatusFileEnum.ACCEPTED,
            owner=user
        )
        await file.save()
    # В случае ошибки, удалить загруженный файл и ответить что пошло не так
    except ValidationError as text:
        path.unlink()
        raise HTTPException(
            status_code=422, detail=text.args
        )
