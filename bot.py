"""
Main Bot Class - Handles Pyrogram Client Setup
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
            plugins=dict(root="plugins"),
            parse_mode=ParseMode.HTML,
            sleep_threshold=60
        )
        
        # Initialize database
        self.db = Database()
        
    async def start(self):
        """Start the bot and initialize database"""
        await super().start()
        
        # Connect to database
        await self.db.connect()
        
        # Get bot info
        me = await self.get_me()
        logger.info(f"Bot started as @{me.username}")
        
        # Set bot info for global access
        self.me = me
        
    async def stop(self):
        """Stop the bot and close database connection"""
        await self.db.disconnect()
        await super().stop()
