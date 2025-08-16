"""
Database Operations with MongoDB
"""

import logging
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError
from config import Config
from typing import List, Dict, Any, Optional
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        
    async def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = AsyncIOMotorClient(Config.DATABASE_URI)
            self.db = self.client[Config.DATABASE_NAME]
            self.collection = self.db[Config.COLLECTION_NAME]
            
            # Create indexes for better search performance
            await self.collection.create_index([("file_name", "text"), ("caption", "text")])
            await self.collection.create_index("file_unique_id", unique=True)
            await self.collection.create_index("chat_id")
            await self.collection.create_index("message_id")
            
            logger.info("Connected to MongoDB successfully")
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def close(self):
        """Close database connection (sync version for bot.stop)"""
        if self.client:
            self.client.close()
            logger.info("Database connection closed")
    
    async def save_media(self, media_data: Dict[str, Any]) -> bool:
        """Save media information to database"""
        try:
            await self.collection.insert_one(media_data)
            return True
        except DuplicateKeyError:
            # File already exists, skip
            return False
        except Exception as e:
            logger.error(f"Error saving media: {e}")
            return False
    
    async def search_media(self, query: str, file_type: str = None) -> List[Dict[str, Any]]:
        """Search media by query"""
        try:
            # Create search filter
            search_filter = {}
            
            # Add file type filter if specified
            if file_type:
                search_filter["file_type"] = file_type
            
            # Text search in file name and caption
            if query.strip():
                # Split query into words for better matching
                query_words = query.strip().split()
                or_conditions = []
                
                # Search for each word individually and the full query
                for word in query_words:
                    or_conditions.extend([
                        {"file_name": {"$regex": re.escape(word), "$options": "i"}},
                        {"caption": {"$regex": re.escape(word), "$options": "i"}}
                    ])
                
                # Also search for the complete query
                or_conditions.extend([
                    {"file_name": {"$regex": re.escape(query), "$options": "i"}},
                    {"caption": {"$regex": re.escape(query), "$options": "i"}}
                ])
                
                search_filter["$or"] = or_conditions
            
            # Execute search with limit, sorted by date (newest first)
            cursor = self.collection.find(search_filter).sort("date", -1).limit(Config.MAX_RESULTS)
            results = await cursor.to_list(length=Config.MAX_RESULTS)
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching media: {e}")
            return []
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        try:
            total_files = await self.collection.count_documents({})
            
            # Count by file type
            pipeline = [
                {"$group": {"_id": "$file_type", "count": {"$sum": 1}}}
            ]
            
            type_counts = {}
            async for doc in self.collection.aggregate(pipeline):
                type_counts[doc["_id"]] = doc["count"]
            
            return {
                "total_files": total_files,
                "by_type": type_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {"total_files": 0, "by_type": {}}
    
    async def delete_media(self, chat_id: int, message_id: int) -> bool:
        """Delete media from database"""
        try:
            result = await self.collection.delete_one({
                "chat_id": chat_id,
                "message_id": message_id
            })
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting media: {e}")
            return False
    
    async def get_total_size(self) -> int:
        """Get total size of all files in bytes"""
        try:
            pipeline = [
                {"$group": {"_id": None, "total_size": {"$sum": "$file_size"}}}
            ]
            
            result = await self.collection.aggregate(pipeline).to_list(1)
            return result[0]["total_size"] if result else 0
            
        except Exception as e:
            logger.error(f"Error getting total size: {e}")
            return 0
    
    async def get_recent_media(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent media files"""
        try:
            cursor = self.collection.find({}).sort("date", -1).limit(limit)
            results = await cursor.to_list(length=limit)
            return results
            
        except Exception as e:
            logger.error(f"Error getting recent media: {e}")
            return []
    
    async def ban_user(self, user_id: int) -> bool:
        """Ban a user from using the bot"""
        try:
            banned_collection = self.db["banned_users"]
            await banned_collection.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "banned_at": datetime.now()}},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error banning user {user_id}: {e}")
            return False
    
    async def unban_user(self, user_id: int) -> bool:
        """Unban a user"""
        try:
            banned_collection = self.db["banned_users"]
            await banned_collection.delete_one({"user_id": user_id})
            return True
        except Exception as e:
            logger.error(f"Error unbanning user {user_id}: {e}")
            return False
    
    async def is_banned(self, user_id: int) -> bool:
        """Check if a user is banned"""
        try:
            banned_collection = self.db["banned_users"]
            result = await banned_collection.find_one({"user_id": user_id})
            return result is not None
        except Exception as e:
            logger.error(f"Error checking if user {user_id} is banned: {e}")
            return False
    
    async def get_user_count(self) -> int:
        """Get total number of users who have used the bot"""
        try:
            users_collection = self.db["users"]
            return await users_collection.count_documents({})
        except Exception as e:
            logger.error(f"Error getting user count: {e}")
            return 0
    
    async def add_user(self, user_id: int, username: str = None, first_name: str = None) -> bool:
        """Add user to database"""
        try:
            users_collection = self.db["users"]
            await users_collection.update_one(
                {"user_id": user_id},
                {
                    "$set": {
                        "user_id": user_id,
                        "username": username,
                        "first_name": first_name,
                        "last_seen": datetime.now()
                    }
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
            return False
