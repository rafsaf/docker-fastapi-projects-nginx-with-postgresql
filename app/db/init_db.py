from app.core.config import settings
from app import crud, schemas
from sqlalchemy.orm import Session
from app.db.session import engine
from app.db.base_class import Base


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations

    Base.metadata.create_all(bind=engine)  # type: ignore

    user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER_EMAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER_EMAIL,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.user.create(db, obj_in=user_in)  # noqa: F841
