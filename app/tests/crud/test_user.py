from app.schemas.user import UserUpdateMe
from asyncio import AbstractEventLoop as EventLoop, events
from fastapi.testclient import TestClient
from app.models import User
from app import crud
from app.schemas import UserCreateMe, UserCreateBySuperuser, UserPydantic
from app.tests.utils.utils import random_email, random_lower_string
from app.core.security import verify_password


def test_user_create_me(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateMe(email=email, password=password)
    user = event_loop.run_until_complete(crud.user.create_me(user_in))

    assert user.email == email
    assert hasattr(user, "password_hash")
    assert user.is_superuser == False


def test_user_create_by_superuser(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    is_superuser = True
    is_active = False
    user_in = UserCreateBySuperuser(
        email=email,
        password=password,
        is_superuser=is_superuser,
        is_active=is_active,
    )

    user = event_loop.run_until_complete(crud.user.create_by_superuser(user_in))
    assert user.email == email
    assert hasattr(user, "password_hash")
    assert user.is_superuser == is_superuser
    assert user.is_active == is_active


def test_user_get_by_email(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateMe(email=email, password=password)
    user = event_loop.run_until_complete(crud.user.create_me(user_in))
    user_2 = event_loop.run_until_complete(crud.user.get_by_email(email))

    assert user_2
    assert UserPydantic.from_orm(user) == UserPydantic.from_orm(user_2)


def test_user_update_me(client: TestClient, event_loop: EventLoop):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreateMe(email=email, password=password)
    user = event_loop.run_until_complete(crud.user.create_me(user_in))

    name = random_lower_string()
    family_name = random_lower_string()
    new_password = random_lower_string()

    user_in = UserUpdateMe(name=name, family_name=family_name, password=new_password)
    updated_user = event_loop.run_until_complete(crud.user.update_me(user, user_in))
    assert updated_user.name == name
    assert updated_user.family_name == family_name
    assert verify_password(new_password, updated_user.password_hash)
