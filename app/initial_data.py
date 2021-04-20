import logging
import asyncio

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


async def main() -> None:
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
