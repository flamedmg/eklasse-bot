from pydantic import Field, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    # Telegram settings
    telegram_api_id: int = Field(description="Telegram API ID from my.telegram.org")
    telegram_api_hash: str = Field(description="Telegram API hash from my.telegram.org")
    telegram_bot_token: str = Field(description="Telegram Bot token from @BotFather")

    # School settings
    school_website_url: str = Field(description="School website URL")
    school_email_server: str = Field(description="Email server hostname")
    school_email_user: str = Field(description="Email username")
    school_email_password: str = Field(description="Email password")

    # Database settings
    database_url: str = Field(
        default="sqlite:///data/school_bot.db",
        description="Database connection string"
    )

    # Redis settings
    redis_url: RedisDsn = Field(
        default="redis://redis:6379/0",
        description="Redis connection URL"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        validate_default=True,
        extra="forbid",
    )


settings = Settings()
