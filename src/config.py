from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Telegram settings
    telegram_api_id: int
    telegram_api_hash: str
    telegram_bot_token: str

    # School settings
    school_website_url: str
    school_email_server: str
    school_email_user: str
    school_email_password: str

    # Database settings
    database_url: str

    # Redis settings
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
