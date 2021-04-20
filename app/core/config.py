import secrets
from typing import Dict, List, Optional, Union
from pydantic import AnyHttpUrl, BaseSettings, AnyUrl, validator, EmailStr


class Settings(BaseSettings):
    # SECURITY
    SECRET_KEY: str = secrets.token_urlsafe()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # PROJECT NAME, API PREFIX, CORS ORIGINS
    PROJECT_NAME: str = "Just a project name, appears in OpenAPI docs"
    API_STR: str = ""
    BACKEND_CORS_ORIGINS: Union[str, List[AnyHttpUrl]] = \
        "http://localhost:3000,http://localhost:8000"

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "super_secret_db_password"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "db"
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    # Above (see validators) -> postgresql://user:secret@localhost:5432/db

    # FIRST SUPERUSER
    FIRST_SUPERUSER_EMAIL: EmailStr = "example@example.com"  # type: ignore
    FIRST_SUPERUSER_PASSWORD: str = "my_secret_password"

    # TESTING
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    # VALIDATORS
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def _assemble_cors_origins(cls, cors_origins):
        if isinstance(cors_origins, str):
            return [item.strip() for item in cors_origins.split(",")]
        return cors_origins

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def _assemble_db_connection(cls, v: Optional[str], values: Dict[str, str]) -> str:
        if isinstance(v, str):
            return v
        return AnyUrl.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER") or "localhost",
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB')}",
        )

    class Config:
        env_file = "/build/.env"
        case_sensitive = True


settings: Settings = Settings()
