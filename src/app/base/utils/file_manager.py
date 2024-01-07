import shutil
from datetime import datetime
from pathlib import Path

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
    if User:
        path = settings.DOCUMENTS_DIR / user.email
    else:
        path = settings.PUBLIC_FILES_DIR

    # Если директория не существует, то создадим ее
    if not path.exists():
        path.mkdir(parents=True)

    # Формируем новое имя для файла состоящее из текущего времени по UTC с сохранением исходного расширения
    date = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    new_name = Path(file_name).with_stem(date)

    return path / new_name


async def save_file(file, user=None):
    """ Сохранение загруженных файлов """
    # Формируем путь к файлу
    path = get_path_to_save(file.filename, user)
    with open(path, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
