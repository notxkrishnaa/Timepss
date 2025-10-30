import logging
from typing import Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorClient
from config import config

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.db = None
        
    async def connect(self):
        """Connect to MongoDB database"""
        try:
            self.client = AsyncIOMotorClient(config.MONGO_URI)
            self.db = self.client.music_bot
            logger.info("Connected to MongoDB successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            return False
            
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            
    async def insert_chat(self, chat_id: int, data: Dict[str, Any]):
        """Insert or update chat data"""
        try:
            await self.db.chats.update_one(
                {"chat_id": chat_id},
                {"$set": data},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error inserting chat data: {e}")
            
    async def get_chat(self, chat_id: int) -> Optional[Dict[str, Any]]:
        """Get chat data by chat_id"""
        try:
            return await self.db.chats.find_one({"chat_id": chat_id})
        except Exception as e:
            logger.error(f"Error getting chat data: {e}")
            return None
            
    async def delete_chat(self, chat_id: int):
        """Delete chat data"""
        try:
            await self.db.chats.delete_one({"chat_id": chat_id})
        except Exception as e:
            logger.error(f"Error deleting chat data: {e}")
            
    async def update_queue(self, chat_id: int, queue: list):
        """Update queue for a chat"""
        try:
            await self.db.chats.update_one(
                {"chat_id": chat_id},
                {"$set": {"queue": queue}},
                upsert=True
            )
        except Exception as e:
            logger.error(f"Error updating queue: {e}")

# Global database instance
db = MongoDB()