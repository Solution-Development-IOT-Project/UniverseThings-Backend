from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroDroneAPI"
    API_V1_STR: str = "/api/v1"

    # URL completa de la BD (tomada de .env)
    SQLALCHEMY_DATABASE_URL: str

    # Seguridad
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Configuración de Pydantic Settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # ignora variables extra en .env
    )


settings = Settings()
