from typing import Generator

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.fastapi import register_tortoise

from main import create_app
from src.config import settings


@pytest.fixture(scope="module")
def client() -> Generator:
    # set up
    app = create_app()
    register_tortoise(
        app,
        db_url=settings.TEST_DB_URL,
        modules={"models": settings.APPS_MODELS},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def admin_data() -> dict:
    data = {
        "email": "admin@test.com",
        "password": "123qwe",
        "last_name": "Admin Last Name",
        "first_name": "Admin First Name",
        "surname": "Admin Surname",
    }
    return data


@pytest.fixture
def user1_data() -> dict:
    data = {
        "email": "user1@test.com",
        "password": "123qwe",
        "last_name": "Test 1 Last Name",
        "first_name": "Test 1 First Name",
        "surname": "Test 1 Surname",
    }
    return data


@pytest.fixture
def user2_data() -> dict:
    data = {
        "email": "user2@test.com",
        "password": "123qwe",
        "last_name": "Test 2 Last Name",
        "first_name": "Test 2 First Name",
        "surname": "Test 2 Surname",
    }
    return data
