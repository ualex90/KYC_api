from pathlib import Path
import os

from dotenv import load_dotenv


load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')

BASE_DIR = Path('__file__').resolve().parent.parent.parent

# Database config
DB_URL = (f"{os.environ.get('DB_TYPE')}://"
          f"{os.environ.get('DB_USER')}:"
          f"{os.environ.get('DB_PASS')}@"
          f"{os.environ.get('DB_HOST')}:"
          f"{os.environ.get('DB_PORT')}/"
          f"{os.environ.get('DB_NAME')}")

APPS_MODELS = [

]
