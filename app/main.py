from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from app.api.api import api_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json"
    )
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(api_router, prefix=settings.API_STR)
    return app


app = create_app()

register_tortoise(
    app=app,
    db_url=settings.TORTOISE_ALCHEMY_DATABASE_URI,
    modules={"models": ["app.models"]},
    add_exception_handlers=True,
)