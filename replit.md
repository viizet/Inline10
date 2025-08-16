# Overview

This is a Telegram Media Search Bot built with Pyrogram that indexes media files from configured Telegram channels into MongoDB and provides inline search functionality. Users can search for videos, documents, audio files, photos, and GIFs by typing `@BotUsername query` anywhere in Telegram. The bot includes admin tools for management, user authorization systems, and subscription verification features.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Core Framework
- **Pyrogram Client**: Asynchronous Telegram bot framework handling all Telegram API interactions
- **Plugin-based Architecture**: Modular design with separate handlers for different functionalities (admin, indexing, inline search, start commands)
- **Async/Await Pattern**: Full asynchronous operation for better performance and scalability

## Database Layer
- **MongoDB with Motor**: Asynchronous MongoDB driver for Python
- **Document-based Storage**: Media metadata stored as documents with text indexes for search optimization
- **Automatic Indexing**: Creates database indexes on file_name, caption, file_unique_id, chat_id, and message_id for performance
- **Duplicate Prevention**: Unique constraints on file_unique_id to prevent duplicate entries

## Authentication & Authorization
- **Multi-level Access Control**: 
  - Admin users with full access to management commands
  - Authorized users list for general bot access
  - Channel subscription verification for access control
- **Subscription Verification**: Checks if users are subscribed to a required channel before allowing bot usage

## Media Processing
- **Multi-format Support**: Handles videos, documents, audio files, photos, and animated GIFs
- **Metadata Extraction**: Captures file information, captions, sizes, and message context
- **Real-time Indexing**: Automatically indexes new media as it's posted to configured channels
- **Manual Indexing**: Admin command to bulk index historical messages from channels

## Search System
- **Inline Query Processing**: Telegram inline mode for searching from any chat
- **Text-based Search**: MongoDB text search across file names and captions
- **Result Filtering**: Configurable result limits and caching for performance
- **Type-specific Results**: Returns appropriate Telegram inline result types based on media format

## Deployment Infrastructure
- **Keep-alive Server**: HTTP server for platforms like Replit to maintain bot uptime
- **Environment Configuration**: Comprehensive config management through environment variables
- **Logging System**: File and console logging for debugging and monitoring

# External Dependencies

## Telegram API
- **Pyrogram**: Modern Telegram Bot API framework
- **Bot Token**: Authentication with Telegram Bot API
- **API Credentials**: Telegram API ID and hash for client authentication

## Database Service
- **MongoDB Atlas**: Cloud MongoDB service for data persistence
- **Motor Driver**: Asynchronous MongoDB driver for Python
- **Connection String**: MongoDB URI for database connectivity

## Deployment Platforms
- **Replit Support**: Built-in keep-alive functionality for Replit hosting
- **Render Support**: Complete deployment configuration with render.yaml and requirements
- **Environment Variables**: Platform-agnostic configuration management

## Python Dependencies
- **asyncio**: Asynchronous programming support
- **logging**: Built-in Python logging framework
- **typing**: Type hints for better code documentation
- **threading**: Background server management for keep-alive functionality

# Deployment Ready

## Render Hosting Configuration
- **render.yaml**: Configured for automatic Render deployment
- **render_requirements.txt**: Python dependencies for production hosting
- **README.md**: Comprehensive documentation with setup instructions
- **DEPLOYMENT.md**: Step-by-step Render deployment guide
- **Environment Variables**: All secrets configured for Render hosting