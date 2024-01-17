import uvicorn
from celery import Celery
from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_pagination.utils import disable_installed_extensions_check
from tortoise.contrib.fastapi import register_tortoise

from src.config import settings
from src.app import routers
from src.app.auth.endpoints import token


def create_app() -> FastAPI:
    """
    Создание приложения

    Создание приложения выделено в отдельную функцию
    для возможности создания тестовой базы данных при тестировании
    """
    # Регистрация объекта FastAPI
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )

    # Роутеры со всех приложений
    application.include_router(routers.api_router, prefix='/api')
    # Отдельный роутер для авторизации в Swagger
    application.include_router(token.swagger_router, prefix='')

    # Подключаем пагинацию
    add_pagination(application)
    # Отключаем назойливое сообщение, что для tortoise лучше использовать"fastapi_pagination.ext.tortoise"
    # При этом разработчик не создал инструкцию к этому функционалу
    disable_installed_extensions_check()
    return application


# Создание приложения
app = create_app()

# Подключение базы данных tortoise
register_tortoise(
    app,
    config=settings.TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
