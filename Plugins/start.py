"""
Start Command Handler
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils import is_subscribed, is_authorized_user
from config import Config

logger = logging.getLogger(__name__)

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
🎬 <b>Soo dhawoow!</b>

Salaan {user.first_name}! Waxaan ahay bot-ka raadinta filimka.

<b>🔍 Sidee loo isticmaalo:</b>
• Qor <code>@{bot_username} magaca filmka</code> chat walba
• Waxaan ku siin doonaa filimada aad raadineysid
• Riix filmka aad rabto si aad u hesho

<b>🎯 Tusaalayaal:</b>
• <code>@{bot_username} action filim</code>
• <code>@{bot_username} majaajilo filim</code>
• <code>@{bot_username} cabsi filim</code>

<b>🎬 Noocyada Filimka:</b>
🎭 Dagaal • 😂 Majaajilo • 😱 Cabsi • ❤️ Jacayl • 🚀 Khayaali

Bilow raadinta <code>@{bot_username}</code> chat walba!
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
ℹ️ <b>Caawimaad</b>

<b>🔍 Sidee loo raadiyaa:</b>
Qor <code>@botusername magaca filmka</code> chat walba.

<b>🎯 Sida fiican loo raadiyaa:</b>
• Isticmaal magaca saxda ah
• Qor nooca filmka: dagaal, majaajilo, cabsi
• Isticmaal qanjeyntaha: <code>"magaca dhabta ah"</code>

<b>🎬 Tusaalayaal sahlan:</b>
• <code>@botusername avengers</code>
• <code>@botusername titanic</code>
• <code>@botusername fast furious</code>

<b>📝 Noocyada Filimka:</b>
🎭 Dagaal - Filimo dagaal
😂 Majaajilo - Filimo qosol
😱 Cabsi - Filimo argagax
❤️ Jacayl - Filimo jacayl
🚀 Khayaali - Filimo khayaali

<b>❓ Caawimaad kelale?</b>
La xiriir maamulka bot-ka.
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