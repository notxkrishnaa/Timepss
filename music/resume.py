import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from db import db

logger = logging.getLogger(__name__)

# Music player instance will be imported from bot.py
music_player = None

@Client.on_message(filters.command("resume"))
async def resume_command(client: Client, message: Message):
    """Handle /resume command"""
    try:
        chat_id = message.chat.id
        
        # Check if bot is in voice chat
        try:
            call = music_player.pytgcalls.get_active_call(chat_id)
            if not call:
                await message.reply_text("❌ I'm not playing anything right now!")
                return
        except:
            await message.reply_text("❌ I'm not in a voice chat!")
            return
            
        # Resume playback
        await music_player.pytgcalls.resume_stream(chat_id)
        await message.reply_text("▶️ Playback resumed!")
        
    except Exception as e:
        logger.error(f"Error resuming playback: {e}")
        await message.reply_text("❌ Failed to resume playback!")