import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from db import db

logger = logging.getLogger(__name__)

# Music player instance will be imported from bot.py
music_player = None

@Client.on_message(filters.command("skip"))
async def skip_command(client: Client, message: Message):
    """Handle /skip command"""
    try:
        chat_id = message.chat.id
        
        # Check if there are songs in queue
        if not music_player.queues.get(chat_id):
            await message.reply_text("❌ No songs in queue to skip!")
            return
            
        # Skip to next song
        await message.reply_text("⏭️ Skipping to next song...")
        await music_player.pytgcalls.leave_group_call(chat_id)
        await music_player.handle_stream_end(chat_id)
        
    except Exception as e:
        logger.error(f"Error skipping song: {e}")
        await message.reply_text("❌ Failed to skip song!")