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
        modules={"models": ["app.models.tortoise"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
