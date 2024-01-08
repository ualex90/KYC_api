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

# Данные для подключения к базе данных из .env
DB_TYPE = os.environ.get('DB_TYPE')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')

# URL для подключения к безе данных Tortoise ORM
DB_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# URL для подключения к тестовой безе данных Tortoise ORM
TEST_DB_URL = f"{DB_TYPE}://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME_TEST}"

# Файлы моделей Tortoise ORM
APPS_MODELS = [
    "src.app.users.models",
    "src.app.files.models",
    "aerich.models",
]

# Конфигурация базы данных Tortoise ORM
TORTOISE_ORM = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": APPS_MODELS,
            "default_connection": "default",
        }
    },
}
