from functools import lru_cache
from typing import Tuple, Type

from pydantic_settings import (
    BaseSettings, 
    PydanticBaseSettingsSource,
    SettingsConfigDict
)


class Settings(BaseSettings):
    """
    Load and validate application settings from environment variables.
    """
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

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        validate_default=True,
        extra='forbid'
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
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
