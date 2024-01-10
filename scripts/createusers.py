import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tortoise import Tortoise, run_async

from src.app.auth.auth_handler import Auth
from src.config import settings
from src.app.users.models import User

users = [
    {
        'email': 'admin@sky.pro',
        'last_name': 'SkyPro',
        'first_name': 'Admin',
        'surname': None,
        'password': '123qwe',
        'is_active': True,
        'is_staff': True,
        'is_superuser': True,
    },
    {
        'email': 'ivanov@sky.pro',
        'last_name': 'Иванов',
        'first_name': 'Иван',
        'surname': 'Иванович',
        'password': '123qwe',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    },
    {
        'email': 'petrov@sky.pro',
        'last_name': 'Петров',
        'first_name': 'Петр',
        'surname': 'Петрович',
        'password': '123qwe',
        'is_active': True,
        'is_staff': False,
        'is_superuser': False,
    },
]


async def main():
    """ Создание тестовых пользователей """
    await Tortoise.init(
        config=settings.TORTOISE_ORM
    )
    for item in users:
        if not await User.first():
            print("ЕСТЬ!!!")
        this_user = await User.get_or_none(email=item['email'])
        if not this_user:
            user = await User(
                email=item['email'],
                last_name=item['last_name'],
                first_name=item['first_name'],
                surname=item['surname'],
                password=Auth.get_password_hash(item['password']),
                is_active=item['is_active'],
                is_staff=item['is_staff'],
                is_superuser=item['is_superuser']
            )
            await user.save()
            print(f'{user.email}, password: {item["password"]}{", superuser" if item["is_superuser"] else ""}')
        else:
            print(f'Ошибка! Пользователь "{item["email"]}" уже существует')


if __name__ == '__main__':
    run_async(main())
