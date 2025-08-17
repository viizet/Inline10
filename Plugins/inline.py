"""
Inline Query Handler for Search Functionality
"""

import logging
from pyrogram import Client, filters
from pyrogram.types import (
    InlineQuery, InlineQueryResultDocument, InlineQueryResultVideo, InlineQueryResultArticle,
    InlineQueryResultAudio, InlineQueryResultPhoto, InlineQueryResultAnimation,
    InlineQueryResultCachedVideo, InlineQueryResultCachedDocument, 
    InlineQueryResultCachedAudio, InlineQueryResultCachedPhoto, InlineQueryResultCachedAnimation,
    InputTextMessageContent
)
from utils import is_subscribed, is_authorized_user, format_file_size, get_file_type_emoji, escape_html
from config import Config

logger = logging.getLogger(__name__)

@Client.on_inline_query()
async def inline_query_handler(client: Client, query: InlineQuery):
    """Handle inline queries for media search"""
    user_id = query.from_user.id
    search_query = query.query.strip()
    
    # Check subscription
    if not await is_subscribed(client, user_id):
        results = [
            InlineQueryResultDocument(
                id="auth_required",
                title="🔒 Authorization Required",
                description="Join our channel to use this bot",
                document_url="https://telegram.org/",
                mime_type="text/plain",
                input_message_content=InputTextMessageContent(
                    "🔒 You need to join our channel to use this bot.\n"
                    f"Start the bot @{(await client.get_me()).username} for more information."
                )
            )
        ]
        
        await query.answer(
            results=results,
            cache_time=0,
            is_personal=True
        )
        return
    
    # Check authorization
    if not await is_authorized_user(user_id, client):
        results = [
            InlineQueryResultArticle(
                id="unauthorized",
                title="❌ Unauthorized Access",
                description="Contact admin for access",
                input_message_content=InputTextMessageContent(
                    "❌ You are not authorized to use this bot.\n"
                    "Contact an administrator for access."
                )
            )
        ]
        
        await query.answer(
            results=results,
            cache_time=0,
            is_personal=True
        )
        return
    
    # Handle empty query - show recent media
    if not search_query:
        try:
            # Get recent media files optimized for large collections
            recent_media = await client.db.get_recent_media(limit=30)
            
            if not recent_media:
                results = [
                    InlineQueryResultArticle(
                        id="help",
                        title="🔍 No Media Found",
                        description="Add media to channels first, then search here",
                        input_message_content=InputTextMessageContent(
                            "🔍 <b>No media files found</b>\n\n"
                            "To use this bot:\n"
                            "• Add the bot to your media channels\n"
                            "• Upload some videos, documents, or other files\n"
                            "• Then search here using keywords\n\n"
                            "<b>Search Examples:</b>\n"
                            "• <code>video name</code>\n"
                            "• <code>keyword | video</code>\n"
                            "• <code>\"exact phrase\"</code>"
                        )
                    )
                ]
            else:
                results = []
                for idx, media in enumerate(recent_media):
                    try:
                        result = create_inline_result(media, idx)
                        if result:
                            results.append(result)
                    except Exception as e:
                        logger.error(f"Error creating inline result: {e}")
                        continue
                
                # Ensure we have at least some results
                if not results:
                    results = [
                        InlineQueryResultArticle(
                            id="fallback",
                            title="🔍 Recent Videos Available",
                            description="Type to search your media collection",
                            input_message_content=InputTextMessageContent(
                                "🔍 <b>Search your media collection</b>\n\n"
                                f"You have {len(recent_media)} recent files available.\n"
                                "Type your search query to find specific content."
                            )
                        )
                    ]
            
            await query.answer(
                results=results,
                cache_time=10,  # Reduced cache time for recent media
                is_personal=True
            )
            return
            
        except Exception as e:
            logger.error(f"Error getting recent media: {e}")
            # Fallback - still try to show something useful
            results = [
                InlineQueryResultArticle(
                    id="search_prompt",
                    title="🔍 Search Your 899 Videos",
                    description="Type to search your media collection",
                    input_message_content=InputTextMessageContent(
                        "🔍 <b>Search your media collection</b>\n\n"
                        "You have 899+ videos indexed!\n"
                        "Type your search query to find specific content.\n\n"
                        "<b>Examples:</b>\n"
                        "• <code>action</code> - for action movies\n"
                        "• <code>comedy</code> - for comedy films\n"
                        "• <code>2023</code> - for recent movies"
                    )
                )
            ]
            
            await query.answer(
                results=results,
                cache_time=5,
                is_personal=True
            )
            return
    
    # Parse query for file type filter
    file_type_filter = None
    if " | " in search_query:
        search_query, file_type_filter = search_query.split(" | ", 1)
        file_type_filter = file_type_filter.strip().lower()
        search_query = search_query.strip()
    
    try:
        # Search database
        logger.info(f"Searching for: '{search_query}' with filter: {file_type_filter}")
        media_results = await client.db.search_media(search_query, file_type_filter)
        logger.info(f"Found {len(media_results)} results")
        
        if not media_results:
            from pyrogram.types import InlineQueryResultArticle
            results = [
                InlineQueryResultArticle(
                    id="no_results",
                    title="🔍 Not Found",
                    description=f"No results for '{search_query}' - Try different keywords",
                    input_message_content=InputTextMessageContent(
                        f"🔍 <b>Not Found</b>\n\n"
                        f"No videos found for: <code>{search_query}</code>\n\n"
                        "💡 <b>Try:</b>\n"
                        "• Different keywords\n"
                        "• Shorter search terms\n"
                        "• Check spelling"
                    )
                )
            ]
        else:
            results = []
            
            for idx, media in enumerate(media_results):
                try:
                    result = create_inline_result(media, idx)
                    if result:
                        results.append(result)
                except Exception as e:
                    logger.error(f"Error creating inline result: {e}")
                    continue
        
        # Answer inline query
        await query.answer(
            results=results[:50],  # Telegram limit
            cache_time=Config.CACHE_TIME,
            is_personal=True,
            next_offset=str(len(results)) if len(media_results) >= Config.MAX_RESULTS else ""
        )
        
    except Exception as e:
        logger.error(f"Error handling inline query: {e}")
        
        # Error result
        from pyrogram.types import InlineQueryResultArticle
        results = [
            InlineQueryResultArticle(
                id="error",
                title="❌ Search Error",
                description="An error occurred while searching",
                input_message_content=InputTextMessageContent(
                    "❌ <b>Search Error</b>\n\n"
                    "An error occurred while searching. Please try again later.\n"
                    "If the problem persists, contact the bot administrators."
                )
            )
        ]
        
        await query.answer(
            results=results,
            cache_time=0,
            is_personal=True
        )

def create_inline_result(media: dict, index: int):
    """Create inline result based on media type"""
    file_type = media.get("file_type")
    file_name = media.get("file_name", "Unknown")
    file_size = media.get("file_size", 0)
    caption = media.get("caption", "")
    file_id = media.get("file_id")
    
    # Truncate long filenames for display
    display_name = file_name if len(file_name) <= 50 else file_name[:47] + "..."
    
    # Create description
    size_text = format_file_size(file_size) if file_size else "Unknown size"
    description = f"{size_text}"
    
    if caption:
        caption_preview = caption[:100] + "..." if len(caption) > 100 else caption
        description += f" • {caption_preview}"
    
    # Get emoji for file type
    emoji = get_file_type_emoji(file_type)
    title = f"{emoji} {display_name}"
    
    try:
        if file_type == "video":
            from pyrogram.types import InlineQueryResultCachedVideo, InlineKeyboardMarkup, InlineKeyboardButton
            
            # Create custom keyboard with Search and Join buttons
            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat=""),
                    InlineKeyboardButton("📢 Join", url="https://t.me/daawotv")
                ]
            ])
            
            return InlineQueryResultCachedVideo(
                id=f"video_{index}",
                video_file_id=file_id,
                title=title,
                description=description,
                caption=f"{file_name}\n\nKUSO BIIT @DAAWOTV",
                reply_markup=keyboard
            )
            
        elif file_type == "document":
            from pyrogram.types import InlineQueryResultCachedDocument
            return InlineQueryResultCachedDocument(
                id=f"doc_{index}",
                title=title,
                description=description,
                document_file_id=file_id
            )
            
        elif file_type == "audio":
            from pyrogram.types import InlineQueryResultCachedAudio
            return InlineQueryResultCachedAudio(
                id=f"audio_{index}",
                audio_file_id=file_id,
                title=title
            )
            
        elif file_type == "photo":
            from pyrogram.types import InlineQueryResultCachedPhoto
            return InlineQueryResultCachedPhoto(
                id=f"photo_{index}",
                photo_file_id=file_id,
                title=title,
                description=description
            )
            
        elif file_type == "gif":
            from pyrogram.types import InlineQueryResultCachedAnimation
            return InlineQueryResultCachedAnimation(
                id=f"gif_{index}",
                animation_file_id=file_id,
                title=title
            )
            
        else:
            # Fallback to document
            from pyrogram.types import InlineQueryResultCachedDocument
            return InlineQueryResultCachedDocument(
                id=f"file_{index}",
                title=title,
                description=description,
                document_file_id=file_id
            )
            
    except Exception as e:
        logger.error(f"Error creating inline result for {file_type}: {e}")
        return None
