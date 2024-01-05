from fastapi import APIRouter


upload_router = APIRouter()


@upload_router.get('/')
async def upload_document():
    return {"key": "upload complete!"}
