from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # NUEVO
    APP_NAME: str = "UniverseThings Backend"  # o el nombre que quieras

    # Opcional: si quieres seguir usando PROJECT_NAME también
    PROJECT_NAME: str = "AgroDroneAPI"

    API_V1_STR: str = "/api/v1"

    SQLALCHEMY_DATABASE_URL: str

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
