from fastapi import APIRouter
from src.app.files.endpoints import upload, download


documents_router = APIRouter()

documents_router.include_router(upload.upload_router, prefix='/upload', tags=['files'])
documents_router.include_router(download.download_router, prefix='/download', tags=['files'])
