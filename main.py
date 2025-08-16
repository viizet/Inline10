#!/usr/bin/env python3
"""
Telegram Media Search Bot - Main Entry Point
"""

import asyncio
import logging
import pyrogram
from bot import MediaSearchBot
from keep_alive import keep_alive   # ✅ Import keep_alive

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Main function to start the bot"""
    try:
        # ✅ Start keep-alive webserver for Render
        keep_alive()

        # Initialize and start the bot
        bot = MediaSearchBot()
        await bot.start()
        logger.info("Bot started successfully!")

        # Keep the bot running
        await pyrogram.idle()

    except Exception as e:
        logger.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    asyncio.run(main())
