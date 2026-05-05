from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, PositiveFloat, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    telegram_bot_token: str = Field(default="", alias="TELEGRAM_BOT_TOKEN")
    api_base_url: str = Field(default="http://localhost:4000/api", alias="API_BASE_URL")
    api_timeout_seconds: PositiveFloat = Field(default=10, alias="API_TIMEOUT_SECONDS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    user_links_path: Path = Field(default=Path("data/user_links.json"), alias="USER_LINKS_PATH")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    @field_validator("telegram_bot_token")
    @classmethod
    def validate_bot_token(cls, value: str) -> str:
        if not value:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        return value

    @field_validator("api_base_url")
    @classmethod
    def validate_api_base_url(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("API_BASE_URL must be an HTTP URL")
        return value.rstrip("/")


@lru_cache
def get_settings() -> Settings:
    return Settings()
