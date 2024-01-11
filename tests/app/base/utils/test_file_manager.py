from pathlib import Path

from src.app.base.utils.file_manager import get_path_to_save
from src.app.users.models import User
from src.config import settings


def test_get_path_to_save_private():
    """ Тестирование формирования пути сохранения файла """
    filename = "test.fm"
    user = User()
    user.email = "test1@example.com"

    good_path = Path(settings.DOCUMENTS_DIR, user.email)
    if good_path.exists():
        good_path.rmdir()

    path = get_path_to_save(filename, user)
    assert path.parent == good_path
    assert good_path.exists()
    good_path.rmdir()


def test_get_path_to_save_public():
    """ Тестирование формирования пути сохранения файла """
    filename = "test.fm"
    user = None

    good_path = Path(settings.PUBLIC_FILES_DIR)

    path = get_path_to_save(filename, user)
    assert path.parent == good_path
    assert good_path.exists()
