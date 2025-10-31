import os
import logging
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream, InputStream

# Import handlers
from handlers.start import start_command
from music.play import play_command, MusicPlayer
from music.pause import pause_command
from music.resume import resume_command
from music.skip import skip_command
from music.stop import stop_command

# Import database
from db import db
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Pyrogram client
app = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)

# Initialize music player
music_player = MusicPlayer(pytgcalls)

# Set music_player instances in other modules
from music.play import music_player as play_music_player
from music.pause import music_player as pause_music_player
from music.resume import music_player as resume_music_player
from music.skip import music_player as skip_music_player
from music.stop import music_player as stop_music_player

play_music_player = music_player
pause_music_player = music_player
resume_music_player = music_player
skip_music_player = music_player
stop_music_player = music_player

@pytgcalls.on_stream_end()
async def on_stream_end(client: PyTgCalls, update: Update):
    """Handle stream end event"""
    try:
        chat_id = update.chat_id
        await music_player.handle_stream_end(chat_id)
    except Exception as e:
        logger.error(f"Error in stream end handler: {e}")

async def startup():
    """Initialize bot on startup"""
    logger.info("Starting Music Bot...")
    
    # Connect to MongoDB
    if not await db.connect():
        logger.error("Failed to connect to MongoDB. Exiting...")
        return False
        
    # Load existing queues from database
    try:
        chats = await db.db.chats.find({}).to_list(length=None)
        for chat in chats:
            chat_id = chat['chat_id']
            queue = chat.get('queue', [])
            music_player.queues[chat_id] = queue
    except Exception as e:
        logger.error(f"Error loading queues from database: {e}")
    
    logger.info("Music Bot started successfully!")
    return True

async def shutdown():
    """Cleanup on shutdown"""
    logger.info("Shutting down Music Bot...")
    await db.disconnect()

async def main():
    """Main function to run the bot"""
    await startup()
    
    try:
        # Start PyTgCalls
        await pytgcalls.start()
        
        # Run Pyrogram client
        await app.run()
        
    except Exception as e:
        logger.error(f"Error running bot: {e}")
    finally:
        await shutdown()

if __name__ == "__main__":
    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)
    
    # Run the bot
    import asyncio
    asyncio.run(main())