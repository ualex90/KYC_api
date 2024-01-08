import shutil
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile, HTTPException
from tortoise.exceptions import ValidationError

from src.app.auth.permission import is_owner_or_superuser
from src.app.files.models import File, StatusFileEnum
from src.app.users.models import User
from src.config import settings


def get_path_to_save(filename: str, user: User = None) -> Path:
    """
    Формирование пути к файлу и создание необходимых директорий

    :param user: Объект текущего пользователя
    :param filename: Имя исходного файла
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
    new_name = Path(filename).with_stem(date)

    return path / new_name


async def save_file(upload_file: UploadFile, user: User = None) -> None:
    """
    Сохранение загруженных файлов

    :param upload_file: Файл, объект UploadFile
    :param user: Текущий пользователь для сохранения приватного файла, или None для публичного
    """
    # Формируем путь к файлу
    path = get_path_to_save(upload_file.filename, user)

    # Сохранение файла на диске
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Сохранение информации о файле в базе данных
    try:
        file = await File(
            name=upload_file.filename,
            size=upload_file.size,
            content_type=upload_file.content_type,
            filename=Path(path.name).stem,
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


async def get_file(filename: str, owner: User = None, current_user: User = None) -> dict:
    """
    Получение файла для FileResponse

    :param filename: имя файла находящегося в хранилище DOCUMENTS_DIR без расширения
    :param owner: Владелец для получения приватного файла, или None для публичного
    :param current_user: Текущий пользователь
    :return: Словарь пригодный для распаковки в аргументы FileResponse
    """
    # Определим переменные file и path чтоб не прописывать для каждого if else
    file = None
    path_no_suffix = None

    if owner:
        # Проверяем, является ли пользователь владельцем или администратором
        if is_owner_or_superuser(current_user=current_user, owner=owner):
            # Проверяем, существует ли пользователь и берем его ID
            if owner_id := await User.get_or_none(email=owner):
                file = await File.get_or_none(filename=filename, owner=owner_id)
                path_no_suffix = settings.DOCUMENTS_DIR / owner / filename
    else:
        file = await File.get_or_none(filename=filename)
        path_no_suffix = settings.PUBLIC_FILES_DIR / filename

    # Возвращаем словарь пригодный для распаковки в аргументы FileResponse
    if file:
        return {
            'path': path_no_suffix.with_suffix(Path(file.name).suffix),  # Приклеиваем расширение как у file.name
            'filename': file.name,
            'media_type': file.content_type
        }

    # Если файл в базе не найден, вызываем ошибку 404
    raise HTTPException(
        status_code=404, detail="File not found"
    )