from typing import Annotated, List

from fastapi import APIRouter, Depends

from src.app.auth.permission import get_superuser
from src.app.users.models import User
from src.app.users.schemas import UserListSchema

admin_router = APIRouter()


@admin_router.get('/user', response_model=List[UserListSchema])
async def get_users(
        current_user: Annotated[User, Depends(get_superuser)],
        limit: int = 10,
        offset: int = 0
):
    response = await User.all()
    return response[offset:][:limit]
