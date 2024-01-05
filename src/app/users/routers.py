from fastapi import APIRouter
from src.app.users.endpoints import user


users_router = APIRouter()

users_router.include_router(user.user_router, prefix='', tags=['users'])
