import os
from typing import Optional

class Config:
    # Telegram API credentials
    API_ID: int = int(os.getenv("API_ID", 0))
    API_HASH: str = os.getenv("API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # MongoDB
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    
    # Pyrogram session name
    SESSION_NAME: str = os.getenv("SESSION_NAME", "music_bot")
    
    # Other settings
    MAX_DURATION: int = 3600  # Max song duration in seconds (1 hour)

config = Config()
