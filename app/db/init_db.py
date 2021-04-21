from app.schemas.user import UserCreateBySuperuser
from app.core.config import settings
from app import crud
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=settings.SQLALCHEMY_DATABASE_URI, modules={"models": ["app.models"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
    user = await crud.user.get_by_email(email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_data = UserCreateBySuperuser(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        await crud.user.create_by_superuser(user_data)
