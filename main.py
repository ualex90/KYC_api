from fastapi import FastAPI
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import register_tortoise

from src.config import settings
from src.app import routers
from src.app.auth.endpoints import token

# Регистрация объекта FastAPI
app = FastAPI(
    title="KYC",
    description="Author - u_alex90",
    version="0.0.1",
)

# Роутеры со всех приложений
app.include_router(routers.api_router, prefix='/api')
# Отдельный роутер для авторизации в Swagger
app.include_router(token.swagger_router, prefix='')

# Подключение базы данных tortoise
register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Подключаем пагинацию
add_pagination(app)
