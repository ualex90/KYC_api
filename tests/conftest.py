from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer

from main import create_app
from src.config import settings
from faker import Faker

from tests.utils.utils import get_token_headers, register_test_users

faker = Faker()


@pytest.fixture(scope="module")
def client() -> Generator:
    """
    Клиент и тестовая базы данных которая будет
    удалена по окончании тестирования
    """
    app = create_app()
    # Создание тестовой базы данных и миграций
    initializer(
        db_url=settings.TEST_DB_URL,
        modules=settings.APPS_MODELS,
    )
    # Подключение к тестовой базе
    register_tortoise(
        app,
        db_url=settings.TEST_DB_URL,
        modules={'models': settings.APPS_MODELS},
        add_exception_handlers=True,
    )
    with TestClient(app) as c:
        # Предварительно заполняем базу данных (для доступа из каждого модуля)
        register_test_users(c)
        yield c
    # Удаление тестовой базы
    finalizer()


@pytest.fixture(scope="module")
def admin_token_headers(client: TestClient) -> dict[str, str]:
    user_data = {
            'email': 'admin@sky.pro',
            'password': '123qwe',
        }
    return get_token_headers(client, user_data)


@pytest.fixture(scope="module")
def user1_token_headers(client: TestClient) -> dict[str, str]:
    user_data = {
            'email': 'ivanov@sky.pro',
            'password': '123qwe',
        }
    return get_token_headers(client, user_data)


@pytest.fixture(scope="module")
def user2_token_headers(client: TestClient) -> dict[str, str]:
    user_data = {
            'email': 'petrov@sky.pro',
            'password': '123qwe',
        }
    return get_token_headers(client, user_data)


@pytest.fixture()
def random_user_data() -> dict:
    """ Случайные пользовательские данные """
    return {
        "email": faker.email(),
        "password": faker.password(),
        "last_name": faker.last_name(),
        "first_name": faker.first_name(),
        "surname": faker.first_name() + 'ich',
    }
