from app.core.config import settings
import random
import string
from asyncio import AbstractEventLoop as EventLoop
from typing import Dict
from tortoise.models import Model
from fastapi.testclient import TestClient


def random_lower_string(length=20) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email(length=10) -> str:
    return f"{random_lower_string(length)}@{random_lower_string(length)}.com"


def clean_table(model: Model, event_loop: EventLoop):
    event_loop.run_until_complete(model.all().delete())


def user_authentication_headers(
    client: TestClient, email: str, password: str
) -> Dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(f"{settings.API_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers