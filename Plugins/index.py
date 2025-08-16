"""
Media Indexing Handler
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import extract_media_info, is_admin
from config import Config
import asyncio

logger = logging.getLogger(__name__)

# Channel filter for configured channels
channel_filter = filters.chat(Config.CHANNELS)

@Client.on_message(channel_filter & (filters.video | filters.document | filters.audio | filters.photo | filters.animation))
async def index_media(client: Client, message: Message):
    """Index media files from configured channels"""
    try:
        # Extract media information
        media_info = extract_media_info(message)
        
        if not media_info:
            return
        
        # Save to database
        success = await client.db.save_media(media_info)
        
        if success:
            logger.info(f"Indexed {media_info['file_type']}: {media_info['file_name']} from {message.chat.title}")
        else:
            logger.debug(f"Media already exists: {media_info['file_name']}")
            
    except Exception as e:
        logger.error(f"Error indexing media: {e}")

@Client.on_message(filters.command("index") & filters.user(Config.ADMINS))
async def manual_index_command(client: Client, message: Message):
    """Manually index messages from a channel"""
    args = message.text.split()
    
    if len(args) < 2:
        await message.reply(
            "❌ Usage: /index <channel_id> [limit]\n\n"
            "Example: /index -1001234567890 100\n"
            "This will index last 100 messages from the channel."
        )
        return
    
    try:
        channel_id = int(args[1])
        limit = int(args[2]) if len(args) > 2 else 100
        
        if limit > 1000:
            await message.reply("❌ Limit cannot exceed 1000 messages.")
            return
        
        status_msg = await message.reply(
            f"🔄 <b>Starting manual indexing...</b>\n\n"
            f"📊 Channel ID: <code>{channel_id}</code>\n"
            f"📊 Limit: {limit} messages\n"
            f"⏳ Please wait..."
        )
        
        indexed_count = 0
        skipped_count = 0
        error_count = 0
        
        try:
            # Get chat info
            chat = await client.get_chat(channel_id)
            chat_title = chat.title or "Unknown Chat"
            
            await status_msg.edit_text(
                f"🔄 <b>Indexing: {chat_title}</b>\n\n"
                f"📊 Processing {limit} messages...\n"
                f"⏳ Starting..."
            )
            
        except Exception as e:
            await status_msg.edit_text(f"❌ Error accessing channel: {e}")
            return
        
        # Process messages
        async for msg in client.get_chat_history(channel_id, limit=limit):
            try:
                # Check if message has media
                if not (msg.video or msg.document or msg.audio or msg.photo or msg.animation):
                    skipped_count += 1
                    continue
                
                # Extract media info
                media_info = extract_media_info(msg)
                if not media_info:
                    skipped_count += 1
                    continue
                
                # Save to database
                success = await client.db.save_media(media_info)
                
                if success:
                    indexed_count += 1
                    logger.info(f"Manually indexed: {media_info['file_name']}")
                else:
                    skipped_count += 1
                
                # Update status every 10 files
                if (indexed_count + skipped_count + error_count) % 10 == 0:
                    await status_msg.edit_text(
                        f"🔄 <b>Indexing: {chat_title}</b>\n\n"
                        f"✅ Indexed: {indexed_count}\n"
                        f"⏭ Skipped: {skipped_count}\n"
                        f"❌ Errors: {error_count}\n"
                        f"📊 Progress: {indexed_count + skipped_count + error_count}/{limit}"
                    )
                
                # Small delay to prevent rate limits
                await asyncio.sleep(0.1)
                
            except Exception as e:
                error_count += 1
                logger.error(f"Error processing message {msg.id}: {e}")
        
        # Final status
        await status_msg.edit_text(
            f"✅ <b>Indexing Complete!</b>\n\n"
            f"📊 <b>Results for {chat_title}:</b>\n"
            f"✅ Successfully indexed: {indexed_count}\n"
            f"⏭ Skipped (no media/duplicate): {skipped_count}\n"
            f"❌ Errors: {error_count}\n"
            f"📊 Total processed: {indexed_count + skipped_count + error_count}/{limit}"
        )
        
    except ValueError:
        await message.reply("❌ Invalid channel ID. Please provide a valid number.")
    except Exception as e:
        logger.error(f"Error in manual index command: {e}")
        await message.reply(f"❌ Error during indexing: {e}")

@Client.on_edited_message(channel_filter & (filters.video | filters.document | filters.audio | filters.photo | filters.animation))
async def handle_edited_media(client: Client, message: Message):
    """Handle edited media messages"""
    try:
        # For edited messages, we can update the existing record
        # First delete the old record, then add the new one
        await client.db.delete_media(message.chat.id, message.id)
        
        # Index the updated message
        await index_media(client, message)
        
        logger.info(f"Updated indexed media: {message.id} from {message.chat.title}")
        
    except Exception as e:
        logger.error(f"Error handling edited media: {e}")
