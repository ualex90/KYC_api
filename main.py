from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from src.config import settings

app = FastAPI(
    title="KYC",
    description="Author - u_alex90",
    version="0.0.1",
)

register_tortoise(
    app,
    db_url=settings.DB_URL,
    modules={"models": settings.APPS_MODELS},
    generate_schemas=False,
    add_exception_handlers=True,
)
