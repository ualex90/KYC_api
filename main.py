from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.config import settings
from src.app import routers

# Регистрация объекта FastAPI
app = FastAPI(
    title="KYC",
    description="Author - u_alex90",
    version="0.0.1",
)

app.include_router(routers.api_router, prefix='/api')

# Подключение базы данных tortoise
register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=False,
    add_exception_handlers=True,
)
