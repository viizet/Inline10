"""
Delete Handler - Sync database when videos are deleted from channels
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import Config

logger = logging.getLogger(__name__)

# Channel filter for configured channels
channel_filter = filters.chat(Config.CHANNELS)

@Client.on_deleted_messages(channel_filter)
async def handle_deleted_messages(client: Client, messages):
    """Handle deleted messages from configured channels"""
    try:
        deleted_count = 0
        
        for message in messages:
            # Delete from database using chat_id and message_id
            success = await client.db.delete_media(message.chat.id, message.id)
            
            if success:
                deleted_count += 1
                logger.info(f"Deleted media from database: chat_id={message.chat.id}, message_id={message.id}")
        
        if deleted_count > 0:
            logger.info(f"Successfully deleted {deleted_count} media files from database due to channel deletions")
            
    except Exception as e:
        logger.error(f"Error handling deleted messages: {e}")
