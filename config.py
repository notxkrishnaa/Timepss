import os
from typing import Optional

class Config:
    # Telegram API credentials - Yahan apne actual values fill karein
    API_ID: int = int(os.getenv("API_ID", "1234567"))  # Apna API ID yahan daalein
    API_HASH: str = os.getenv("API_HASH", "your_api_hash_here")  # Apna API Hash yahan daalein
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")  # Apna Bot Token yahan daalein
    
    # MongoDB - Apna MongoDB connection string yahan daalein
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority")
    
    # Pyrogram session name
    SESSION_NAME: str = os.getenv("SESSION_NAME", "music_bot")
    
    # Other settings
    MAX_DURATION: int = 3600  # Max song duration in seconds (1 hour)

config = Config()