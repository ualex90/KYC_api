from fastapi import Security, HTTPException

from src.app.auth.auth_handler import Auth
from src.app.users.models import User


def get_user(current_user: User = Security(Auth.get_current_user)):
    """ Проверка активный юзер или нет """
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_superuser(current_user: User = Security(Auth.get_current_user)):
    """ Проверка суперюзер или нет """

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )

    # Проверка на признак активности
    elif not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def get_this_user_or_superuser(pk: int, current_user: User = Security(Auth.get_current_user)):
    """ Проверка этот пользователь или суперюзер """

    if not current_user.is_superuser:
        if current_user.id != pk:
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )

    # Проверка на признак активности
    elif not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return current_user


def is_owner_or_superuser(current_user: User, owner: User) -> bool:
    """ Проверка является юзер владельцем или администратором """
    return current_user.is_superuser or current_user == owner
