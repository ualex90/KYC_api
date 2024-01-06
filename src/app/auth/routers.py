from fastapi import APIRouter
from src.app.auth.endpoints import token


auth_router = APIRouter()

auth_router.include_router(token.token_router, prefix='/token', tags=['auth'])
