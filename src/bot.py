from faststream.redis import RedisBroker
from telethon import TelegramClient

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
import logging
from telethon import TelegramClient, events
from telethon.tl.types import Message

logger = logging.getLogger(__name__)

async def start_handler(event: Message):
    """Handle /start command."""
    await event.respond(
        "👋 Welcome to School Parent Assistant Bot!\n\n"
        "I'll help you stay updated with:\n"
        "📚 School schedules\n"
        "📧 Important notifications\n"
        "📊 Academic performance\n\n"
        "Use /help to see available commands."
    )

async def help_handler(event: Message):
    """Handle /help command."""
    await event.respond(
        "Available commands:\n\n"
        "/schedule - View today's schedule\n"
        "/homework - Check homework assignments\n"
        "/grades - View recent grades\n"
        "/notifications - Manage notification settings\n"
        "/help - Show this help message"
    )

def setup_handlers(bot: TelegramClient):
    """Register all message handlers."""
    # Command handlers
    bot.add_event_handler(
        start_handler,
        events.NewMessage(pattern='/start')
    )
    
    bot.add_event_handler(
        help_handler,
        events.NewMessage(pattern='/help')
    )
    
    logger.info("Bot handlers registered")
