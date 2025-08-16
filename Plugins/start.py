"""
Start Command Handler
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import is_subscribed, is_authorized_user
from config import Config

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user = message.from_user
    
    # Track user in database
    try:
        await client.db.add_user(user.id, user.username, user.first_name)
    except Exception as e:
        logger.error(f"Error tracking user {user.id}: {e}")
    
    # Check if user is subscribed to auth channel
    if not await is_subscribed(client, user.id):
        auth_channel_link = f"https://t.me/{Config.AUTH_CHANNEL}"
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Join Channel", url=auth_channel_link)],
            [InlineKeyboardButton("Check Subscription", callback_data="check_sub")]
        ])
        
        await message.reply(
            "🔒 <b>Access Restricted</b>\n\n"
            "You need to join our channel to use this bot.\n"
            "Click the button below to join and then check your subscription.",
            reply_markup=keyboard
        )
        return
    
    # Check if user is authorized
    if not await is_authorized_user(user.id, client):
        await message.reply(
            "❌ <b>Unauthorized Access</b>\n\n"
            "You are not authorized to use this bot.\n"
            "Contact an administrator for access."
        )
        return
    
    # Welcome message
    bot_username = (await client.get_me()).username
    
    welcome_text = f"""
🎉 <b>Welcome to Media Search Bot!</b>

Hello {user.first_name}! I'm your personal media search assistant.

<b>🔍 How to use:</b>
• Type <code>@{bot_username} your search query</code> in any chat
• I'll show you relevant media files instantly
• Tap on any result to share it

<b>🎯 Search Examples:</b>
• <code>@{bot_username} python tutorial</code>
• <code>@{bot_username} movie | video</code>
• <code>@{bot_username} ebook | document</code>
• <code>@{bot_username} music | audio</code>
• <code>@{bot_username} "exact phrase"</code>

<b>📁 Supported Types:</b>
🎬 Videos • 📄 Documents • 🎵 Audio • 🖼 Photos • 🎞 GIFs

<b>✨ Features:</b>
• Lightning fast search
• Multiple file format support
• Caption-based filtering
• Real-time results

Start typing <code>@{bot_username}</code> in any chat to begin searching!
"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Search Movies", switch_inline_query_current_chat="")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ])
    
    await message.reply(welcome_text, reply_markup=keyboard)

@Client.on_callback_query(filters.regex("check_sub"))
async def check_subscription(client: Client, callback_query):
    """Check user subscription status"""
    user_id = callback_query.from_user.id
    
    if await is_subscribed(client, user_id):
        await callback_query.answer("✅ Subscription verified! You can now use the bot.", show_alert=True)
        # Send start message
        await start_command(client, callback_query.message)
    else:
        await callback_query.answer("❌ Please join the channel first!", show_alert=True)

@Client.on_callback_query(filters.regex("help"))
async def handle_callbacks(client: Client, callback_query):
    """Handle callback queries"""
    data = callback_query.data
    
    if data == "help":
        help_text = """
ℹ️ <b>How to Use Media Search Bot</b>

<b>🔍 Inline Search:</b>
Type <code>@botusername query</code> in any chat to search for media files.

<b>🎯 Search Tips:</b>
• Use specific keywords for better results
• Add file type filters: <code>query | video</code>
• Use quotes for exact phrases: <code>"exact phrase"</code>
• Combine multiple terms for refined search

<b>📝 Supported Filters:</b>
• <code>| video</code> - Videos only
• <code>| document</code> - Documents only  
• <code>| audio</code> - Audio files only
• <code>| photo</code> - Photos only
• <code>| gif</code> - GIFs only

<b>💡 Examples:</b>
• <code>@botusername python programming | video</code>
• <code>@botusername "machine learning" | document</code>
• <code>@botusername relaxing music | audio</code>

<b>❓ Need Help?</b>
Contact bot administrators for assistance.
"""
        await callback_query.edit_message_text(help_text)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def get_file_type_emoji(file_type: str) -> str:
    """Get emoji for file type"""
    emojis = {
        "video": "🎬",
        "document": "📄", 
        "audio": "🎵",
        "photo": "🖼",
        "gif": "🎞"
    }
    return emojis.get(file_type, "📎")
