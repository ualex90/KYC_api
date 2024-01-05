from fastapi import APIRouter
from src.app.documents.routers import documents_router


api_router = APIRouter()

api_router.include_router(documents_router, prefix='/documents', tags=['documents'])
