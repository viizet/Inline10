# Telegram Media Search Bot

A powerful Telegram bot that automatically indexes media files from configured channels into MongoDB and provides instant inline search functionality. Users can search for videos, documents, audio files, photos, and GIFs by typing `@BotUsername query` anywhere in Telegram.

## Features

- 🔍 **Instant Inline Search** - Search media by typing `@BotUsername query` in any chat
- 📁 **Multi-format Support** - Videos, documents, audio files, photos, and animated GIFs
- 🔄 **Auto-indexing** - Automatically indexes new media as it's posted to configured channels
- 🗃️ **MongoDB Storage** - Efficient database storage with text search optimization
- 👨‍💼 **Admin Management** - Full admin control with statistics and management commands
- 🔒 **Authorization System** - User authorization and subscription verification
- ⚡ **Real-time Processing** - Instant indexing and search results
- 📊 **Statistics Tracking** - Comprehensive usage and performance statistics

## How It Works

1. **Channel Monitoring**: Bot monitors configured Telegram channels for new media
2. **Auto-indexing**: Automatically indexes file names, captions, and metadata
3. **Inline Search**: Users search by typing `@BotUsername search_term` anywhere
4. **Instant Results**: Returns actual media files that can be sent directly

## Admin Commands

- `/start` - Start the bot and show welcome message
- `/stats` - View detailed bot statistics
- `/total` - Show total indexed files count
- `/broadcast <message>` - Send message to all authorized users
- `/ban <user_id>` - Ban a user from using the bot
- `/unban <user_id>` - Unban a previously banned user
- `/logs` - View recent bot logs
- `/delete <query>` - Delete media matching query from database
- `/index` - Manually index messages from configured channels

## Installation & Setup

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd telegram-media-search-bot
```

### 2. Install Dependencies
```bash
pip install -r render_requirements.txt
```

### 3. Environment Variables

Set up the following environment variables:

#### Required Variables
- `API_ID` - Your Telegram API ID (get from https://my.telegram.org)
- `API_HASH` - Your Telegram API Hash (get from https://my.telegram.org)
- `BOT_TOKEN` - Your bot token from @BotFather
- `DATABASE_URI` - MongoDB connection string
- `ADMINS` - Comma-separated admin user IDs (e.g., "123456789,987654321")
- `CHANNELS` - Comma-separated channel IDs to monitor (e.g., "-1001234567890,-1009876543210")

#### Optional Variables
- `FORCE_SUB_CHANNEL` - Channel ID for subscription verification
- `COLLECTION_NAME` - MongoDB collection name (default: "media")
- `DATABASE_NAME` - MongoDB database name (default: "MediaSearchBot")

### 4. Getting Telegram API Credentials

1. Go to https://my.telegram.org
2. Log in with your phone number
3. Go to "API Development Tools"
4. Create a new application
5. Copy your `API_ID` and `API_HASH`
6. Create a bot with @BotFather on Telegram
7. Copy the bot token

### 5. Setting Up MongoDB

1. Create a free MongoDB Atlas account at https://mongodb.com
2. Create a new cluster
3. Get your connection string
4. Add it as `DATABASE_URI` environment variable

### 6. Channel Setup

1. Add your bot to the channels you want to monitor
2. Make the bot an admin with "Delete Messages" permission
3. Get channel IDs (they start with -100)
4. Add them to `CHANNELS` environment variable

## Deployment on Render

This bot is optimized for Render deployment:

### 1. Connect Repository
- Connect your GitHub repository to Render
- Choose "Web Service" when creating new service

### 2. Configuration
Render will automatically detect the `render.yaml` file with these settings:
- **Build Command**: `pip install -r render_requirements.txt`
- **Start Command**: `python main.py`
- **Environment**: Python

### 3. Set Environment Variables
Add all required environment variables in Render dashboard:
- API_ID
- API_HASH  
- BOT_TOKEN
- DATABASE_URI
- ADMINS
- CHANNELS

### 4. Deploy
- Click "Deploy" and wait for build completion
- Bot will start automatically and begin monitoring channels

## File Structure

```
telegram-media-search-bot/
├── main.py                 # Main application entry point
├── bot.py                  # Bot client setup and initialization
├── config.py              # Configuration management
├── database.py             # MongoDB connection and operations
├── utils.py                # Utility functions
├── keep_alive.py           # Keep-alive server for hosting platforms
├── plugins/                # Plugin-based architecture
│   ├── admin.py           # Admin commands and management
│   ├── index.py           # Media indexing functionality
│   ├── inline.py          # Inline search handling
│   └── start.py           # Start command and user onboarding
├── render.yaml            # Render deployment configuration
├── render_requirements.txt # Python dependencies for Render
└── README.md              # This documentation
```

## Usage Examples

### For Users
```
# Search for videos containing "marvel"
@BotUsername marvel

# Search for documents with "report"
@BotUsername report

# Search for audio files
@BotUsername song

# Show recent files (empty search)
@BotUsername
```

### For Admins
```
# View statistics
/stats

# Ban a user
/ban 123456789

# Broadcast message
/broadcast Hello everyone!

# Manual indexing
/index
```

## Technical Details

### Database Schema
```json
{
  "_id": "ObjectId",
  "file_id": "telegram_file_id",
  "file_unique_id": "unique_telegram_id",
  "file_name": "filename.mp4",
  "file_size": 12345678,
  "file_type": "video",
  "mime_type": "video/mp4",
  "caption": "optional_caption",
  "chat_id": -1001234567890,
  "message_id": 12345,
  "date": "2025-01-01T00:00:00Z",
  "width": 1920,
  "height": 1080,
  "duration": 7200
}
```

### Search Algorithm
- Text-based search across file names and captions
- Supports partial word matching
- Case-insensitive search
- MongoDB text indexes for performance
- Configurable result limits

### Performance Features
- Asynchronous processing with asyncio
- Connection pooling for MongoDB
- Efficient duplicate prevention
- Background indexing for minimal user impact
- Caching for frequently accessed data

## Troubleshooting

### Common Issues

1. **Bot not responding**: Check if bot token is correct and bot is started
2. **No search results**: Verify channels are properly configured and bot has admin access
3. **Database errors**: Check MongoDB connection string and network access
4. **Permission errors**: Ensure bot has necessary permissions in channels

### Logs
Bot logs are stored in `bot.log` file and can be viewed with `/logs` command.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use and modify for your needs.

## Support

For issues and questions:
- Check the troubleshooting section
- Review bot logs
- Create an issue in the repository

## Credits

Built with:
- [Pyrogram](https://pyrogram.org) - Modern Telegram Bot API framework
- [MongoDB](https://mongodb.com) - Document database for media storage
- [Motor](https://motor.readthedocs.io) - Async MongoDB driver for Python

---

**Note**: This bot is designed for educational and personal use. Ensure compliance with Telegram's Terms of Service and respect copyright laws when indexing media content.