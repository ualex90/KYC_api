from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

# Token 60 минут * 24 часа * 7 дней = 7 дней
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

# Базовая директория проекта
BASE_DIR = Path(__file__).parent.parent.parent

# Файловое хранилище
FILES = BASE_DIR / 'files'

# Директория для сохранения документов пользователей
DOCUMENTS_DIR = FILES / 'documents'
if not DOCUMENTS_DIR.exists():
    DOCUMENTS_DIR.mkdir(parents=True)

# Директория для сохранения публичных файлов
PUBLIC_FILES_DIR = FILES / 'public'
if not PUBLIC_FILES_DIR.exists():
    PUBLIC_FILES_DIR.mkdir(parents=True)

# Конфигурация базы данных Tortoise ORM
DB_URL = (f"{os.environ.get('DB_TYPE')}://"
          f"{os.environ.get('DB_USER')}:"
          f"{os.environ.get('DB_PASS')}@"
          f"{os.environ.get('DB_HOST')}:"
          f"{os.environ.get('DB_PORT')}/"
          f"{os.environ.get('DB_NAME')}")
APPS_MODELS = [
    "src.app.users.models",
    "src.app.files.models",
    "aerich.models",
]
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}
