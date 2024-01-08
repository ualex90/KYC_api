from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.test import finalizer, initializer

from main import create_app
from src.config import settings


# Адрес для тестовой базы данных
TEST_DB_URL = settings.DB_URL + '_test'


@pytest.fixture(scope="module", autouse=True)
def client() -> Generator:
    app = create_app()
    # Создание тестовой базы данных и миграций
    initializer(
        db_url=TEST_DB_URL,
        modules=settings.APPS_MODELS,
    )
    # Подключение к тестовой базе
    register_tortoise(
        app,
        db_url=TEST_DB_URL,
        modules={'models': settings.APPS_MODELS},
        add_exception_handlers=True,
    )
    with TestClient(app) as c:
        yield c
    # Удаление тестовой базы
    finalizer()


@pytest.fixture
def user1_data() -> dict:
    data = {
        "email": "user1@test.com",
        "password": "123qwe",
        "last_name": "Test 1 Last Name",
        "first_name": "Test 1 First Name",
        "surname": "Test 1 Surname"
    }
    return data


@pytest.fixture
def user2_data() -> dict:
    data = {
        "email": "user2@test.com",
        "password": "123qwe",
        "last_name": "Test 2 Last Name",
        "first_name": "Test 2 First Name",
        "surname": "Test 2 Surname"
    }
    return data


@pytest.fixture
def admin_data() -> dict:
    data = {
        "email": "admin@test.com",
        "password": "123qwe",
        "last_name": "Admin Last Name",
        "first_name": "Admin First Name",
        "surname": "Admin Surname"
    }
    return data
