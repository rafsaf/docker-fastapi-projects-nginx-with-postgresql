import pytest
from typing import Generator
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer
from app.main import create_app

app = create_app()


@pytest.fixture(scope="module")
def client() -> Generator:
    initializer(["app.models"])
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture(scope="module")
def event_loop(client: TestClient) -> Generator:
    yield client.task.get_loop()
