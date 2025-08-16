"""
Admin Commands Handler
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from utils import is_admin, format_file_size
from config import Config
import asyncio

logger = logging.getLogger(__name__)

# Admin filter
admin_filter = filters.user(Config.ADMINS)

@Client.on_message(filters.command("stats") & admin_filter)
async def stats_command(client: Client, message: Message):
    """Show bot statistics"""
    try:
        stats = await client.db.get_stats()
        total_size = await client.db.get_total_size()
        
        stats_text = f"""
📊 <b>Bot Statistics</b>

📁 <b>Total Files:</b> {stats['total_files']:,}
💾 <b>Total Size:</b> {format_file_size(total_size)}

<b>📂 Files by Type:</b>
"""
        
        for file_type, count in stats['by_type'].items():
            emoji_map = {
                "video": "🎬",
                "document": "📄",
                "audio": "🎵", 
                "photo": "🖼",
                "gif": "🎞"
            }
            emoji = emoji_map.get(file_type, "📎")
            stats_text += f"• {emoji} {file_type.title()}: {count:,}\n"
        
        stats_text += f"\n<b>⚙️ Configuration:</b>\n"
        stats_text += f"• Indexed Channels: {len(Config.CHANNELS)}\n"
        stats_text += f"• Cache Time: {Config.CACHE_TIME}s\n"
        stats_text += f"• Max Results: {Config.MAX_RESULTS}\n"
        stats_text += f"• Caption Filter: {'✅' if Config.USE_CAPTION_FILTER else '❌'}\n"
        
        await message.reply(stats_text)
        
    except Exception as e:
        logger.error(f"Error in stats command: {e}")
        await message.reply("❌ Error retrieving statistics.")

@Client.on_message(filters.command("total") & admin_filter)
async def total_command(client: Client, message: Message):
    """Show total files count"""
    try:
        stats = await client.db.get_stats()
        total_size = await client.db.get_total_size()
        
        await message.reply(
            f"📊 <b>Total Files:</b> {stats['total_files']:,}\n"
            f"💾 <b>Total Size:</b> {format_file_size(total_size)}"
        )
        
    except Exception as e:
        logger.error(f"Error in total command: {e}")
        await message.reply("❌ Error retrieving total count.")

@Client.on_message(filters.command("broadcast") & admin_filter)
async def broadcast_command(client: Client, message: Message):
    """Broadcast message to all users"""
    if not message.reply_to_message:
        await message.reply("❌ Reply to a message to broadcast it.")
        return
    
    # Get all unique user IDs from database (if you store user data)
    # For now, we'll use a simple approach with AUTH_USERS
    users = Config.AUTH_USERS + Config.ADMINS
    
    if not users:
        await message.reply("❌ No users found to broadcast to.")
        return
    
    broadcast_msg = message.reply_to_message
    success_count = 0
    failed_count = 0
    
    status_msg = await message.reply("📡 <b>Broadcasting...</b>\n\n⏳ Starting broadcast...")
    
    for user_id in users:
        try:
            await broadcast_msg.copy(user_id)
            success_count += 1
            
            # Update status every 10 users
            if (success_count + failed_count) % 10 == 0:
                await status_msg.edit_text(
                    f"📡 <b>Broadcasting...</b>\n\n"
                    f"✅ Sent: {success_count}\n"
                    f"❌ Failed: {failed_count}\n"
                    f"⏳ Progress: {success_count + failed_count}/{len(users)}"
                )
            
            # Sleep to avoid flood limits
            await asyncio.sleep(0.1)
            
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to send broadcast to {user_id}: {e}")
    
    # Final status
    await status_msg.edit_text(
        f"📡 <b>Broadcast Complete!</b>\n\n"
        f"✅ Successfully sent: {success_count}\n"
        f"❌ Failed: {failed_count}\n"
        f"📊 Total users: {len(users)}"
    )

@Client.on_message(filters.command("ban") & admin_filter)
async def ban_command(client: Client, message: Message):
    """Ban a user from using the bot"""
    args = message.text.split(None, 1)
    
    if len(args) < 2:
        await message.reply("❌ Usage: /ban <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        # Add to banned users
        await client.db.ban_user(user_id)
        await message.reply(f"✅ User {user_id} has been banned from using the bot.")
            
    except ValueError:
        await message.reply("❌ Invalid user ID. Please provide a valid number.")
    except Exception as e:
        logger.error(f"Error in ban command: {e}")
        await message.reply("❌ Error banning user.")

@Client.on_message(filters.command("unban") & admin_filter)
async def unban_command(client: Client, message: Message):
    """Unban a user"""
    args = message.text.split(None, 1)
    
    if len(args) < 2:
        await message.reply("❌ Usage: /unban <user_id>")
        return
    
    try:
        user_id = int(args[1])
        
        # Remove from banned users
        await client.db.unban_user(user_id)
        await message.reply(f"✅ User {user_id} has been unbanned and can now use the bot.")
            
    except ValueError:
        await message.reply("❌ Invalid user ID. Please provide a valid number.")
    except Exception as e:
        logger.error(f"Error in unban command: {e}")
        await message.reply("❌ Error unbanning user.")

@Client.on_message(filters.command("logger") & admin_filter)
async def logger_command(client: Client, message: Message):
    """Show recent log entries"""
    try:
        # Read last 20 lines from log file
        log_lines = []
        try:
            with open("bot.log", "r", encoding="utf-8") as f:
                log_lines = f.readlines()[-20:]
        except FileNotFoundError:
            await message.reply("❌ Log file not found.")
            return
        
        if not log_lines:
            await message.reply("📋 Log file is empty.")
            return
        
        log_text = "📋 <b>Recent Log Entries:</b>\n\n"
        log_text += "<code>" + "".join(log_lines[-10:]) + "</code>"
        
        if len(log_text) > 4000:
            log_text = log_text[:4000] + "\n... (truncated)"
        
        await message.reply(log_text)
        
    except Exception as e:
        logger.error(f"Error in logger command: {e}")
        await message.reply("❌ Error reading log file.")

@Client.on_message(filters.command("delete") & admin_filter)
async def delete_command(client: Client, message: Message):
    """Delete media from database"""
    if not message.reply_to_message:
        await message.reply("❌ Reply to a media message to delete it from database.")
        return
    
    replied_msg = message.reply_to_message
    
    if not (replied_msg.video or replied_msg.document or replied_msg.audio or 
            replied_msg.photo or replied_msg.animation):
        await message.reply("❌ Replied message doesn't contain any media.")
        return
    
    try:
        # Delete from database
        success = await client.db.delete_media(replied_msg.chat.id, replied_msg.id)
        
        if success:
            await message.reply("✅ Media deleted from database successfully.")
        else:
            await message.reply("❌ Media not found in database or already deleted.")
            
    except Exception as e:
        logger.error(f"Error deleting media: {e}")
        await message.reply("❌ Error deleting media from database.")
