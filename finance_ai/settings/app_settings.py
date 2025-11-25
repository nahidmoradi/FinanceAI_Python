"""Application settings using Pydantic Settings."""

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Main application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    postgres_host: str = Field(
        default="localhost",
        description="PostgreSQL host",
    )
    postgres_port: int = Field(
        default=5432,
        description="PostgreSQL port",
    )
    postgres_db: str = Field(
        default="finance_ai",
        description="PostgreSQL database name",
    )
    postgres_user: str = Field(
        default="financeai_user",
        description="PostgreSQL user",
    )
    postgres_password: str = Field(
        default="",
        description="PostgreSQL password",
    )

    mongodb_uri: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URI",
    )
    mongodb_db: str = Field(
        default="finance_ai",
        description="MongoDB database name",
    )

    redis_host: str = Field(
        default="localhost",
        description="Redis host",
    )
    redis_port: int = Field(
        default=6379,
        description="Redis port",
    )
    redis_db: int = Field(
        default=0,
        description="Redis database number",
    )
    redis_password: str = Field(
        default="",
        description="Redis password",
    )

    faiss_index_path: str = Field(
        default="./data/faiss_index.bin",
        description="FAISS index file path",
    )
    faiss_dimension: int = Field(
        default=3072,
        description="FAISS vector dimension (OpenAI embeddings)",
    )
    faiss_index_type: str = Field(
        default="IndexFlatL2",
        description="FAISS index type (IndexFlatL2, IndexFlatIP, IndexIVFFlat)",
    )

    openai_api_key: str = Field(
        default="",
        description="OpenAI API key",
    )
    gemini_api_key: str = Field(
        default="",
        description="Google Gemini API key",
    )

    jwt_secret_key: str = Field(
        default="change_me_in_production",
        description="JWT secret key",
    )
    jwt_algorithm: str = Field(
        default="HS256",
        description="JWT algorithm",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time",
    )

    api_host: str = Field(
        default="0.0.0.0",
        description="API server host",
    )
    api_port: int = Field(
        default=8000,
        description="API server port",
    )
    api_reload: bool = Field(
        default=True,
        description="Enable auto-reload",
    )
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    environment: str = Field(
        default="development",
        description="Environment name",
    )

    @property
    def postgres_url(self) -> str:
        """Get PostgreSQL connection URL.

        Returns:
            PostgreSQL connection string.
        """
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def async_postgres_url(self) -> str:
        """Get async PostgreSQL connection URL.

        Returns:
            Async PostgreSQL connection string.
        """
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache
def get_settings() -> AppSettings:
    """Get cached settings instance.

    Returns:
        Application settings.
    """
    return AppSettings()
