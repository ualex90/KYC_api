from fastapi import APIRouter
from src.app.auth.routers import auth_router
from src.app.files.routers import documents_router
from src.app.users.routers import users_router


api_router = APIRouter()

api_router.include_router(documents_router, prefix='/files', tags=['files'])
api_router.include_router(users_router, prefix='/users', tags=['users'])
api_router.include_router(auth_router, prefix='/auth', tags=['auth'])
