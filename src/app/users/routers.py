from fastapi import APIRouter
from src.app.users.endpoints import user, admin


users_router = APIRouter()

users_router.include_router(user.user_router, prefix='', tags=['users'])
users_router.include_router(admin.admin_router, prefix='', tags=['users'])
