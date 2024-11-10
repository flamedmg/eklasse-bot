from telethon import TelegramClient
from faststream.redis import RedisBroker

from .config import settings


async def init_bot() -> TelegramClient:
    """Initialize and start the Telegram bot client."""
    client = TelegramClient(
        "school_bot_session",
        settings.telegram_api_id,
        settings.telegram_api_hash,
    )
    await client.start(bot_token=settings.telegram_bot_token)
    return client


async def init_broker() -> RedisBroker:
    """Initialize the Redis message broker."""
    broker = RedisBroker(settings.redis_url)
    await broker.connect()
    return broker
