from fastapi import APIRouter
from src.app.documents.endpoints import upload


documents_router = APIRouter()

documents_router.include_router(upload.upload_router, prefix='/upload', tags=['documents'])
