from fastapi import APIRouter
from src.app.files.endpoints import file, upload, download

documents_router = APIRouter()

documents_router.include_router(file.file_router, prefix='', tags=['files'])
documents_router.include_router(upload.upload_router, prefix='/upload', tags=['files'])
documents_router.include_router(download.download_router, prefix='/download', tags=['files'])
