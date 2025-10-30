from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    """Handle /start command with welcome message"""
    welcome_text = """
🎵 **Music Bot Started!**

I can play music in voice chats. Here are my commands:

**/play** [song name or YouTube link] - Play a song
**/pause** - Pause current song
**/resume** - Resume paused song  
**/skip** - Skip to next song
**/stop** - Stop playback and leave VC

Just add me to your group voice chat and start playing music! 🎶
    """
    
    await message.reply_text(welcome_text)