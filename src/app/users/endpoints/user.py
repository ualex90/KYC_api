from fastapi import APIRouter


user_router = APIRouter()


@user_router.get('/register')
async def register_user():
    return {"key": "Register Ok!"}
