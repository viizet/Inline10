# 🎬 Telegram Media Search Bot

A powerful Telegram bot that indexes media files from channels and provides instant inline search functionality. Users can search for videos, documents, audio files, photos, and GIFs using `@BotUsername query` in any chat.

## ✨ Current Features

### 🔍 Smart Media Search System
- **Inline Search** - Search from any chat using `@BotUsername query`
- **Multi-format Support** - Videos, documents, audio, photos, GIFs
- **Text-based Search** - Search by filename and caption content
- **Recent Videos Display** - Shows recent uploads when no search query
- **Smart Results** - Cached results with proper file type handling

### 🤖 Automated Media Indexing
- **Real-time Indexing** - Automatically indexes new media from configured channels
- **Manual Indexing** - Admin command `/index` to process historical messages
- **Duplicate Prevention** - Prevents duplicate entries using unique file IDs
- **Metadata Extraction** - Captures file size, duration, dimensions, captions

### 👨‍💼 Admin Management Tools
- **Statistics Dashboard** - `/stats` command shows detailed analytics
- **User Management** - Ban/unban users with `/ban` and `/unban` commands
- **Broadcast System** - `/broadcast` to send messages to all users
- **Content Deletion** - `/delete` to remove media from database
- **Log Monitoring** - `/logger` to view recent bot logs
- **Top Analytics** - `/top10` shows most searched content and active users
- **Total Count** - `/total` displays total files and storage size

### 🔒 Security & Authorization
- **Admin Access Control** - Admin-only commands and management features
- **User Authorization** - Configurable authorized users list
- **Channel Subscription** - Require users to join specific channels
- **Ban System** - Prevent banned users from accessing bot features
- **Input Validation** - Secure handling of user inputs

### ⚡ Performance Features
- **MongoDB Integration** - Fast text-indexed database search
- **Async Operations** - Non-blocking database and API operations
- **Connection Pooling** - Efficient database connection management
- **Error Handling** - Comprehensive error recovery and logging
- **Result Caching** - Smart caching for better response times

### 🎯 User Experience
- **Somali Language Support** - Native Somali interface and help text
- **Rich Inline Results** - Proper thumbnails and metadata display
- **Custom Keyboards** - Search and channel join buttons on results
- **Subscription Checks** - Automatic verification of channel membership
- **Help System** - Comprehensive help command with examples

## 🚀 Quick Setup

### Environment Variables
```bash
# Telegram API (Required)
API_ID=your_api_id
API_HASH=your_api_hash
BOT_TOKEN=your_bot_token

# Database (Required)
DATABASE_URI=your_mongodb_uri
DATABASE_NAME=your_database_name
COLLECTION_NAME=media

# Configuration (Required)
ADMINS=user_id1,user_id2
CHANNELS=channel_id1,channel_id2

# Optional Settings
AUTH_CHANNEL=channel_id_for_subscription
AUTH_USERS=authorized_user_ids
CACHE_TIME=300
MAX_RESULTS=50
USE_CAPTION_FILTER=True
```

### Channel Setup
1. Add your bot to channels as admin
2. Grant "Delete Messages" permission
3. Get channel IDs and add to `CHANNELS`
4. Use `/index` command to process existing media

## 💻 Commands

### User Commands
- `/start` - Start the bot and get help
- `/help` - Show usage instructions

### Admin Commands
- `/stats` - View comprehensive bot statistics
- `/total` - Show total files count and storage
- `/top10` - Most searched content and active users
- `/index` - Manually index channel messages
- `/delete` - Remove media from database
- `/broadcast` - Send message to all users
- `/ban` - Ban a user from using bot
- `/unban` - Remove user ban
- `/logger` - View recent log entries

## 🔍 Search Examples

```
# Search for action movies
@BotUsername action movies

# Find specific content
@BotUsername "movie name"

# Search documents
@BotUsername tutorial pdf

# Browse recent videos (empty query)
@BotUsername
```

## 📊 Database Schema

Your bot stores media with this structure:
```json
{
  "file_id": "telegram_file_id",
  "file_unique_id": "unique_identifier", 
  "file_name": "movie_title.mp4",
  "file_size": 1073741824,
  "file_type": "video",
  "caption": "Movie description",
  "chat_id": -1001234567890,
  "chat_title": "Movies Channel",
  "message_id": 12345,
  "date": "2025-01-01T00:00:00Z"
}
```

## 🌐 Deployment on Replit

1. **Import to Replit**
   - Create new Repl from GitHub repository
   - All dependencies will auto-install

2. **Configure Secrets**
   - Open Secrets tab in Replit
   - Add all environment variables listed above
   - Make sure BOT_TOKEN, API_ID, API_HASH are correct

3. **Run the Bot**
   - Click Run button
   - Bot will start automatically
   - Check console for connection status

## 🔧 Technical Details

- **Framework**: Pyrogram (Async Telegram Bot API)
- **Database**: MongoDB with text indexing
- **Architecture**: Plugin-based modular design
- **Language**: Python 3.11+ with async/await
- **Hosting**: Replit with keep-alive functionality

## 📝 File Structure

```
├── main.py              # Bot entry point
├── bot.py               # Pyrogram client setup
├── config.py            # Configuration management
├── database.py          # MongoDB operations
├── utils.py             # Helper functions
├── keep_alive.py        # Replit uptime server
└── Plugins/
    ├── admin.py         # Admin commands
    ├── index.py         # Media indexing
    ├── inline.py        # Inline search handler
    ├── start.py         # User onboarding
    └── delete_handler.py # Content deletion
```

## 🛠️ Current Status

Your bot includes:
- ✅ Complete inline search system
- ✅ Admin management dashboard
- ✅ User authorization and bans
- ✅ Channel subscription verification
- ✅ Automated media indexing
- ✅ Comprehensive logging
- ✅ Somali language interface
- ✅ MongoDB integration
- ✅ Replit deployment ready

## 🔧 Troubleshooting

1. **Bot not responding**: Check BOT_TOKEN in secrets
2. **Database errors**: Verify DATABASE_URI connection
3. **No search results**: Run `/index` to process channels
4. **Permission issues**: Ensure bot is admin in channels

This is your complete, feature-rich Telegram media search bot ready for deployment!
