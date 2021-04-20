import logging
try:
    from app.db.init_db import init_db
    from app.db.session import SessionLocal
    from app.core.config import settings
except ModuleNotFoundError:
    import sys
    import os
    import pathlib

    app = pathlib.Path(os.path.dirname(__file__)).parent
    sys.path.append(str(app))
    from app.db.init_db import init_db
    from app.db.session import SessionLocal
    from app.core.config import settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    db = SessionLocal()
    init_db(db)


def main() -> None:
    logger.info(f'{settings.SQLALCHEMY_DATABASE_URI}')
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
