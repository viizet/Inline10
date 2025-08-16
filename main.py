#!/usr/bin/env python3
"""
Telegram Media Search Bot - Main Entry Point
"""

import asyncio
import logging
import os
import pyrogram
from bot import MediaSearchBot

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
        # Initialize and start the bot
        bot = MediaSearchBot()
        await bot.start()
        logger.info("Bot started successfully!")
        
        # Keep the bot running
        await pyrogram.idle()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise
    finally:
        logger.info("Bot stopped.")

if __name__ == "__main__":
    # Start keep_alive server in background if running on Replit
    if os.getenv("REPL_ID"):
        from keep_alive import keep_alive
        keep_alive()
    
    # Run the bot
    asyncio.run(main())
