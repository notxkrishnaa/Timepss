import os
from typing import Optional

class Config:
    # Telegram API credentials - Yahan apne actual values fill karein
    API_ID: int = int(os.getenv("API_ID", "23640310"))  # Apna API ID yahan daalein
    API_HASH: str = os.getenv("API_HASH", "079f8339732e35e032a64ee020e0b90b")  # Apna API Hash yahan daalein
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "8458860951:AAGnhMc3ATeiHRo43Q4ZDpz5tjPV1rygnsM")  # Apna Bot Token yahan daalein
    
    # MongoDB - Apna MongoDB connection string yahan daalein
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb+srv://rj5706603:O95nvJYxapyDHfkw@cluster0.fzmckei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
    
    # Pyrogram session name
    SESSION_NAME: str = os.getenv("SESSION_NAME", "1BVtsOJ0Bu6yUAF7S2Gg843d8LG_piuRM_VP-zI2Fa6ZBz7ZgRj1hqW1qU0GYYn0r0aA13qvCMS9N7OoiyOQCGy2mdmJh_AWghEQZJabmh-1Kq5p_z2mvTztXIOXBSySjnGTVhc-yQUYO3XIf-ce2__sbH2kqWJVe-8SP5ze3U6MPowZcYXKRaDETfgmjq7qZ5KWtpiY5UMVQ63FwHgXZ4UfGWdig6Ry0IuKiZDul6HWu0xDoHctRsndY29SlXm-Cez391wcIeh4aQp6Le6ii4HMwpq5L8_gVVyAqkwaN-uYohCb-dkzk104yzORpESa_ho5CSZSQoRTAZPgII_f9X-Crac9np-k=")
    
    # Other settings
    MAX_DURATION: int = 3600  # Max song duration in seconds (1 hour)

config = Config()