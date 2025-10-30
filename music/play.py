import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream, InputStream
from db import db
from music.youtube import youtube_dl

logger = logging.getLogger(__name__)

class MusicPlayer:
    def __init__(self, pytgcalls: PyTgCalls):
        self.pytgcalls = pytgcalls
        self.queues = {}  # {chat_id: [song1, song2, ...]}
        
    async def play_music(self, client: Client, message: Message, query: str):
        """Play music in voice chat"""
        try:
            chat_id = message.chat.id
            
            # Check if user is in a voice chat
            if message.from_user is None:
                await message.reply_text("❌ You need to be in a group to use this command!")
                return
                
            user_id = message.from_user.id
            
            # Get user's voice chat status
            try:
                member = await client.get_chat_member(chat_id, user_id)
                if not member:
                    await message.reply_text("❌ Cannot get your voice chat status!")
                    return
            except Exception as e:
                await message.reply_text("❌ You need to be in a voice chat to play music!")
                return
            
            # Download and get audio info
            loading_msg = await message.reply_text("🔍 Searching and downloading...")
            
            result = await youtube_dl.download_audio(query)
            if not result:
                await loading_msg.edit_text("❌ Failed to download audio. Please try another song.")
                return
                
            file_path, audio_info = result
            
            # Initialize queue for chat if not exists
            if chat_id not in self.queues:
                self.queues[chat_id] = []
            
            # Add to queue
            queue_item = {
                'file_path': file_path,
                'info': audio_info,
                'requested_by': message.from_user.first_name
            }
            self.queues[chat_id].append(queue_item)
            
            await db.update_queue(chat_id, self.queues[chat_id])
            
            # If this is the first song, start playing
            if len(self.queues[chat_id]) == 1:
                await loading_msg.edit_text(f"🎵 Playing: **{audio_info['title']}**")
                await self._play_next(chat_id, client)
            else:
                await loading_msg.edit_text(
                    f"🎵 Added to queue: **{audio_info['title']}**\n"
                    f"Position: #{len(self.queues[chat_id])}"
                )
                
        except Exception as e:
            logger.error(f"Error in play_music: {e}")
            await message.reply_text("❌ An error occurred while playing music.")
    
    async def _play_next(self, chat_id: int, client: Client):
        """Play next song in queue"""
        try:
            if not self.queues.get(chat_id):
                return
                
            current_song = self.queues[chat_id][0]
            file_path = current_song['file_path']
            
            if not os.path.exists(file_path):
                logger.error(f"File not found: {file_path}")
                return
                
            # Join voice chat and play
            await self.pytgcalls.join_group_call(
                chat_id,
                InputStream(
                    InputAudioStream(
                        file_path,
                    ),
                ),
            )
            
        except Exception as e:
            logger.error(f"Error playing next song: {e}")
    
    async def handle_stream_end(self, chat_id: int):
        """Handle stream end and play next song"""
        try:
            if self.queues.get(chat_id):
                # Remove current song
                current_song = self.queues[chat_id].pop(0)
                
                # Clean up file
                try:
                    if os.path.exists(current_song['file_path']):
                        os.remove(current_song['file_path'])
                except:
                    pass
                
                await db.update_queue(chat_id, self.queues[chat_id])
                
                # Play next song if available
                if self.queues[chat_id]:
                    await self._play_next(chat_id, self.pytgcalls._client._app)
                else:
                    # No more songs, leave voice chat
                    try:
                        await self.pytgcalls.leave_group_call(chat_id)
                    except:
                        pass
        except Exception as e:
            logger.error(f"Error handling stream end: {e}")

# Music player instance will be initialized in bot.py
music_player = None

@Client.on_message(filters.command("play"))
async def play_command(client: Client, message: Message):
    """Handle /play command"""
    if len(message.command) < 2:
        await message.reply_text("❌ Please provide a song name or YouTube link!\nUsage: `/play song name`")
        return
        
    query = " ".join(message.command[1:])
    await music_player.play_music(client, message, query)