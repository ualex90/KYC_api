import shutil
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile, HTTPException
from tortoise.exceptions import ValidationError

from src.app.auth.permission import is_owner_or_superuser
from src.app.files.models import File, StatusFileEnum

from src.app.users.models import User
from src.config import settings


def get_path_to_save(filename: str, user: User, is_public: bool) -> Path:
    """
    Формирование пути к файлу и создание необходимых директорий

    :param user: Объект текущего пользователя
    :param filename: Имя исходного файла
    :param is_public: Признак публичности
    :return: Объект Path содержащий путь к файлу
    """
    # Собираем путь к директории где будет храниться файл.
    if is_public:
        path = settings.PUBLIC_FILES_DIR  # Если имеется признак публичности, сохраняем файл в директорию public
    else:
        path = settings.DOCUMENTS_DIR / user.email  # Если не публичный, то в папку пользователя

    # Если директория не существует, то создадим ее
    if not path.exists():
        path.mkdir(parents=True)

    # Формируем новое имя для файла состоящее из текущего времени по UTC с сохранением исходного расширения
    date = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    new_name = Path(filename).with_stem(date)

    return path / new_name


async def save_file(upload_file: UploadFile, user: User = None, is_public: bool = False) -> None:
    """
    Сохранение загруженных файлов

    :param upload_file: Файл, объект UploadFile
    :param user: Текущий пользователь для сохранения приватного файла, или None для публичного
    :param is_public: Признак публичности
    """
    # Формируем путь к файлу
    path = get_path_to_save(upload_file.filename, user, is_public)

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
            is_public=is_public,
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


async def get_file_data(current_user: User, pk: int) -> dict:
    """
    Получение данных файла для FileResponse

    :param pk: ID файла
    :param current_user: Текущий пользователь
    :return: Словарь пригодный для распаковки в аргументы FileResponse
    """

    file = await File.get_or_none(id=pk)
    if not file:
        # Если файл в базе не найден, вызываем ошибку 404
        raise HTTPException(
            status_code=404, detail="File not found"
        )
    file_owner = await file.owner
    path_no_suffix = None

    if file.is_public:
        path_no_suffix = settings.PUBLIC_FILES_DIR / file.filename
    else:
        # Проверяем, является ли пользователь владельцем или администратором
        if is_owner_or_superuser(current_user=current_user, owner=file_owner):
            # Проверяем, существует ли пользователь и берем его ID
            path_no_suffix = settings.DOCUMENTS_DIR / file_owner.email / file.filename

    # Возвращаем словарь пригодный для распаковки в аргументы FileResponse
    if file:
        return {
            'path': path_no_suffix.with_suffix(Path(file.name).suffix),  # Приклеиваем расширение как у file.name
            'filename': file.name,
            'media_type': file.content_type
        }


async def get_file_list(
        current_user: User,
        status: StatusFileEnum = None,
        owner_email: str = None
) -> list[dict]:
    """
    Получение списка файлов по заданным фильтрам

    :param current_user: Текущий пользователь
    :param status: Статус файла
    :param owner_email: Email владельца
    """
    file_list = []
    owner_obj = None

    # Если текущий пользователь администратор
    if current_user.is_superuser:
        if owner_email:
            owner_obj = await User.get_or_none(email=owner_email)
            if not owner_obj:
                raise HTTPException(
                    status_code=404, detail="User not found"
                )
    else:
        if owner_email:
            if owner_email != current_user.email:
                raise HTTPException(
                    status_code=403, detail="You are not the owner or superuser"
                )
        # Если владелец не указан, присвоим переменной текущего пользователя
        owner_obj = current_user

    if status and owner_obj:
        query = await File.all().filter(status=status).filter(owner=owner_obj.id)
    elif status:
        query = await File.all().filter(status=status)
    elif owner_obj:
        query = await File.all().filter(owner=owner_obj.id)
    else:
        query = await File.all()

    for file in query:
        file_owner = await file.owner
        file_list.append({
            "id": file.id,
            "name": file.name,
            "status": file.status,
            "owner": file_owner.email if file_owner else None,
            "is_public": file.is_public,
        })
    return file_list


async def get_file(current_user: User, pk: int) -> dict:
    """
    Получение информации о файле
    :param current_user: Текущий пользователь
    :param pk: ID файла
    :return: Подробные данные о файле
    """
    file = await File.get_or_none(id=pk)
    if file:
        file_owner = await file.owner
        if is_owner_or_superuser(current_user, file_owner) or file.is_public:
            data = {
                "id": file.id,
                "name": file.name,
                "status": file.status,
                "owner": file_owner.email,
                "is_public": file.is_public,
                "filename": file.filename,
                "size": file.size,
                "content_type": file.content_type,
                "upload_at": file.upload_at,
                "change_at": file.change_at
            }
            return data
        else:
            raise HTTPException(
                status_code=403, detail="You are not the owner or superuser"
            )
    raise HTTPException(
        status_code=404, detail="File not found"
    )


async def change_status(pk: int, status: StatusFileEnum) -> File:
    """
    Изменение статуса файла

    :param pk: ID файла
    :param status: Новый статус
    :return: Файл с измененным статусом
    """
    file = await File.get_or_none(id=pk)
    if file:
        file.status = status
        await file.save()
        return file
    raise HTTPException(
        status_code=404, detail="File not found"
    )


async def remove_file(current_user: User, pk: int) -> dict:
    """
    Удаление файла

    :param current_user: Текущий пользователь
    :param pk: ID файла
    :return: Результат
    """
    file = await File.get_or_none(id=pk)
    if not file:
        raise HTTPException(
            status_code=404, detail="File not found"
        )
    file_owner = await file.owner
    if is_owner_or_superuser(current_user, file_owner):
        file_data = await get_file_data(current_user, pk)
        file_data['path'].unlink(missing_ok=True)
        await file.delete()
        return {'detail': f'{file_data["filename"]} deleted'}
    raise HTTPException(
        status_code=403, detail="You are not the owner or superuser"
    )
