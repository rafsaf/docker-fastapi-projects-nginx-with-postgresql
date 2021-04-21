from app.core.config import settings
from app import crud, schemas
from tortoise import Tortoise


async def init_db():
    await Tortoise.init(
        db_url=settings.SQLALCHEMY_DATABASE_URI, modules={"models": ["app.models.user"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()
