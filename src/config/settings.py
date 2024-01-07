from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

# Token 60 минут * 24 часа * 7 дней = 7 дней
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

BASE_DIR = Path(__file__).parent.parent.parent
DOCUMENTS_DIR = BASE_DIR / 'documents'

# Database config
DB_URL = (f"{os.environ.get('DB_TYPE')}://"
          f"{os.environ.get('DB_USER')}:"
          f"{os.environ.get('DB_PASS')}@"
          f"{os.environ.get('DB_HOST')}:"
          f"{os.environ.get('DB_PORT')}/"
          f"{os.environ.get('DB_NAME')}")

APPS_MODELS = [
    "src.app.users.models",
]
