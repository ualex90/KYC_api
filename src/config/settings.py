from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# Данные о проекте
PROJECT_NAME = "KYC Service"
PROJECT_DESCRIPTION = "Author - u_alex90"
PROJECT_VERSION = "0.0.1"

# Секретный ключ для генерации токенов доступа
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

# Директория шаблонов html
TEMPLATES_DIR = BASE_DIR / 'src/templates'

# Данные для подключения к базе данных из .env
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

# URL для подключения к безе данных Tortoise ORM
DB_URL = f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
TEST_DB_URL = DB_URL + '_test'

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

# Конфигурация исходящей почты
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_USE_TLS = True if os.environ.get('EMAIL_USE_TLS') == "True" else False
# Проверка заполнения переменных окружения
EMAILS_ENABLED = EMAIL_HOST and EMAIL_PORT and EMAIL_USER and EMAIL_PASSWORD and EMAIL_USE_TLS

# Конфигурация Redis
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER_URL')

# Параметры CORSMiddleware
BACKEND_CORS_ORIGINS = [
    "http://localhost",
    "http://localhost:8080",
]
