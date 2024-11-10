import asyncio
import logging
from contextlib import asynccontextmanager

from faststream import FastStream
from faststream.redis import RedisBroker
from telethon import TelegramClient

from src.config import settings
from src.database import init_db
from src.bot import setup_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Redis broker
broker = RedisBroker(settings.redis_url)
app = FastStream(broker)

# Initialize Telegram client
bot = TelegramClient(
    'school_bot',
    settings.telegram_api_id,
    settings.telegram_api_hash
)

@asynccontextmanager
async def lifespan():
    """Startup and shutdown events for the application."""
    # Initialize database
    await init_db()
    
    # Start Telegram client
    await bot.start(bot_token=settings.telegram_bot_token)
    
    # Setup bot handlers
    setup_handlers(bot)
    
    logger.info("Application startup complete")
    
    try:
        yield
    finally:
        # Cleanup
        await bot.disconnect()
        await broker.close()
        logger.info("Application shutdown complete")

app.lifespan(lifespan)

if __name__ == "__main__":
    asyncio.run(app.run())
