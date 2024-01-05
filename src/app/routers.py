from fastapi import APIRouter
from src.app.documents.routers import documents_router
from src.app.users.routers import users_router


api_router = APIRouter()

api_router.include_router(documents_router, prefix='/documents', tags=['documents'])
api_router.include_router(users_router, prefix='/users', tags=['users'])
