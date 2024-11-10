from functools import lru_cache

from pydantic import Field, RedisDsn
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)


class Settings(BaseSettings):
    """
    Load and validate application settings from environment variables.
    """

    # Telegram settings
    telegram_api_id: int = Field(description="Telegram API ID from my.telegram.org")
    telegram_api_hash: str = Field(description="Telegram API hash from my.telegram.org")
    telegram_bot_token: str = Field(description="Telegram Bot token from @BotFather")

    # School settings
    school_website_url: str = Field(description="School website URL")

    # Database settings - using SQLite for now, but prepared for PostgreSQL if needed
    database_url: str = Field(
        default="sqlite:///data/school_bot.db", description="Database connection string"
    )

    # Redis settings with validation
    redis_url: RedisDsn = Field(
        default="redis://redis:6379/0", description="Redis connection URL"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
        extra="forbid",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """
        Customize the priority of settings sources.

        Priority (highest to lowest):
        1. Environment variables
        2. .env file
        3. Init values
        4. Defaults
        """
        return env_settings, dotenv_settings, init_settings


@lru_cache
def get_settings() -> Settings:
    """
    Return cached settings instance.

    :raises ValidationError: If required environment variables are missing or invalid
    :return: Settings instance
    """
    return Settings()
