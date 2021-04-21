from typing import Generator
from app.core.config import settings
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from app.api.api import api_router
from tortoise.contrib.test import finalizer, initializer

app = FastAPI()

app.include_router(api_router, prefix=settings.API_STR)


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["app.models"], db_url="sqlite://test-{}")
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
