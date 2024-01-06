from fastapi import APIRouter


admin_router = APIRouter()


@admin_router.get('/user')
async def get_users():
    return {
        "User1": {
            'email@mail.com': 1
        },
        "User2": {
            'email@mail.com': 1
        },
    }
