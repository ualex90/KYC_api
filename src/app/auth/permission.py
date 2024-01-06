from fastapi import Security, HTTPException

from src.app.auth.auth_handler import Auth
from src.app.users.models import User


def get_user(current_user: User = Security(Auth.get_current_user)):
    """ Проверка активный юзер или нет """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_superuser(current_user: User = Security(Auth.get_current_user)):
    """ Проверка суперюзер или нет """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
