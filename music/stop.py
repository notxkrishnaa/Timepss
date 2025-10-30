import logging
import os
from pyrogram import Client, filters
from pyrogram.types import Message
from db import db

logger = logging.getLogger(__name__)

# Music player instance will be imported from bot.py
music_player = None

@Client.on_message(filters.command("stop"))
async def stop_command(client: Client, message: Message):
    """Handle /stop command"""
    try:
        chat_id = message.chat.id
        
        # Clear queue and stop playback
        if chat_id in music_player.queues:
            # Clean up downloaded files
            for song in music_player.queues[chat_id]:
                try:
                    if os.path.exists(song['file_path']):
                        os.remove(song['file_path'])
                except:
                    pass
                    
            music_player.queues[chat_id] = []
            await db.update_queue(chat_id, [])
        
        # Leave voice chat
        try:
            await music_player.pytgcalls.leave_group_call(chat_id)
        except:
            pass
            
        await message.reply_text("🛑 Playback stopped and queue cleared!")
        
    except Exception as e:
        logger.error(f"Error stopping playback: {e}")
        await message.reply_text("❌ Failed to stop playback!")