"""
Main Bot Class
--------------
This file contains the main MediaSearchBot class which handles:
- Pyrogram Client setup
- Database initialization
- Start & Stop lifecycle methods
"""

import logging
from pyrogram import Client
from pyrogram.enums import ParseMode
from config import Config
from database import Database

logger = logging.getLogger(__name__)

class MediaSearchBot(Client):
    def __init__(self):
        super().__init__(
            name="MediaSearchBot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="Plugins"),
            parse_mode=ParseMode.HTML,
            sleep_threshold=60
        )

        # Initialize database
        self.db = Database()

    async def start(self):
        """Start the bot and initialize database"""
        try:
            await super().start()
            logger.info("✅ Bot client started successfully!")

            # Connect to database
            try:
                await self.db.connect()
                logger.info("📦 Database connected successfully!")
            except Exception as e:
                logger.error(f"❌ Database connection failed: {e}")
                raise

            # Log bot info
            me = await self.get_me()
            logger.info(f"🤖 Logged in as {me.first_name} (@{me.username})")
            logger.info("🚀 Bot is now running!")
            
        except Exception as e:
            logger.error(f"❌ Failed to start bot: {e}")
            raise

    async def stop(self, *args):
        """Stop the bot cleanly"""
        await super().stop()
        self.db.close()
        logger.info("🛑 Bot stopped. Goodbye!")
