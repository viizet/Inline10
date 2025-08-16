# Deployment Guide - Render Hosting

This guide shows you how to deploy the Telegram Media Search Bot to Render, just like the working example at https://github.com/kevyabdi/Videotolink.

## Prerequisites

Before deploying, make sure you have:

1. ✅ **GitHub Repository** - Your bot code in a GitHub repository
2. ✅ **Telegram Bot Token** - From @BotFather
3. ✅ **Telegram API Credentials** - API_ID and API_HASH from https://my.telegram.org
4. ✅ **MongoDB Database** - Free MongoDB Atlas cluster
5. ✅ **Render Account** - Free account at https://render.com

## Step 1: Prepare Your Repository

Ensure your repository has these files:
- `render.yaml` ✅ (Created automatically)
- `render_requirements.txt` ✅ (Created automatically)
- `main.py` ✅ (Your bot's main file)
- All plugin files in `plugins/` folder ✅

## Step 2: Set Up MongoDB Atlas (Free)

1. Go to https://mongodb.com and create a free account
2. Create a new cluster (choose the free tier)
3. Create a database user with read/write permissions
4. Get your connection string:
   ```
   mongodb+srv://username:password@cluster.mongodb.net/database_name
   ```
5. Replace `username`, `password`, and `database_name` with your actual values

## Step 3: Get Your Channel IDs

1. Add your bot to the channels you want to monitor
2. Make the bot an admin with these permissions:
   - ✅ Delete Messages
   - ✅ Read Messages
3. Get channel IDs (they look like `-1001234567890`)
4. Format them as comma-separated list: `-1001234567890,-1009876543210`

## Step 4: Deploy to Render

### Create New Web Service

1. Go to https://render.com and log in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Render will automatically detect the `render.yaml` configuration

### Configure Environment Variables

Add these environment variables in Render dashboard:

| Variable | Value | Example |
|----------|-------|---------|
| `API_ID` | Your Telegram API ID | `12345678` |
| `API_HASH` | Your Telegram API Hash | `abcdef123456...` |
| `BOT_TOKEN` | Your bot token from @BotFather | `1234567890:ABCdef...` |
| `DATABASE_URI` | Your MongoDB connection string | `mongodb+srv://user:pass@cluster.mongodb.net/db` |
| `ADMINS` | Your Telegram user ID | `123456789` |
| `CHANNELS` | Channel IDs to monitor | `-1001234567890,-1009876543210` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FORCE_SUB_CHANNEL` | Channel for subscription verification | None |
| `COLLECTION_NAME` | MongoDB collection name | `media` |
| `DATABASE_NAME` | MongoDB database name | `MediaSearchBot` |

## Step 5: Deploy and Test

1. Click "Deploy" in Render dashboard
2. Wait for build to complete (usually 2-3 minutes)
3. Check deployment logs for any errors
4. Test your bot:
   - Send `/start` to your bot
   - Try inline search: `@YourBotUsername test`

## Step 6: Configure Channels

After successful deployment:

1. Add your bot to channels as admin
2. Post some media to test auto-indexing
3. Use `/index` command to manually index existing messages
4. Test search functionality

## Automatic Features

Once deployed, your bot will automatically:

- ✅ **Monitor Channels** - Index new media as it's posted
- ✅ **Handle Searches** - Respond to inline queries instantly
- ✅ **Stay Online** - Keep-alive server prevents sleeping
- ✅ **Log Activity** - Track usage and errors
- ✅ **Manage Users** - Handle authorization and subscriptions

## Troubleshooting

### Common Issues

**Bot not starting:**
- Check environment variables are correctly set
- Verify bot token is valid
- Check MongoDB connection string

**No search results:**
- Ensure bot is admin in channels
- Check channel IDs are correct (negative numbers)
- Try `/index` command to manually index

**Database errors:**
- Verify MongoDB connection string
- Check database user permissions
- Ensure network access is allowed

### Checking Logs

1. Go to Render dashboard
2. Click on your service
3. Check "Logs" tab for detailed output
4. Look for connection errors or exceptions

## Service Management

### Updating Your Bot

1. Push changes to your GitHub repository
2. Render will automatically detect and redeploy
3. Or manually trigger deployment from Render dashboard

### Monitoring

- Check Render dashboard for service health
- Monitor MongoDB usage in Atlas dashboard
- Use bot's `/stats` command for usage statistics

## Cost Information

- **Render**: Free tier includes 750 hours/month
- **MongoDB Atlas**: Free tier includes 512MB storage
- **Telegram**: Completely free

Your bot should run entirely on free tiers!

## Security Best Practices

1. ✅ **Never commit secrets** - Use environment variables only
2. ✅ **Secure MongoDB** - Use strong passwords and network restrictions
3. ✅ **Monitor access** - Check bot usage regularly
4. ✅ **Update dependencies** - Keep packages up to date

## Support

If you encounter issues:

1. Check this deployment guide
2. Review Render logs
3. Test locally first
4. Check MongoDB connection
5. Verify environment variables

Your bot should now be running 24/7 on Render, automatically indexing media and responding to searches!