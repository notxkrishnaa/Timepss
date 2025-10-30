import os
import logging
import yt_dlp
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class YouTubeDownloader:
    def __init__(self):
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'restrictfilenames': True,
            'noplaylist': True,
            'nocheckcertificate': True,
            'ignoreerrors': False,
            'logtostderr': False,
            'quiet': True,
            'no_warnings': True,
            'default_search': 'ytsearch',
            'max_filesize': 100000000,  # 100MB
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }
        
        # Create downloads directory if it doesn't exist
        os.makedirs("downloads", exist_ok=True)
        
    async def get_audio_info(self, query: str) -> Optional[dict]:
        """Get audio information without downloading"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(query, download=False)
                
                if 'entries' in info:
                    # Take first result from search
                    info = info['entries'][0]
                    
                return {
                    'id': info['id'],
                    'title': info['title'],
                    'duration': info.get('duration', 0),
                    'url': info['url'],
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader', 'Unknown')
                }
        except Exception as e:
            logger.error(f"Error getting audio info: {e}")
            return None
            
    async def download_audio(self, query: str) -> Optional[Tuple[str, dict]]:
        """Download audio and return file path and info"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                
                if 'entries' in info:
                    info = info['entries'][0]
                
                filename = ydl.prepare_filename(info)
                # Change extension to mp3 due to FFmpeg postprocessing
                filename = os.path.splitext(filename)[0] + '.mp3'
                
                audio_info = {
                    'id': info['id'],
                    'title': info['title'],
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail'),
                    'uploader': info.get('uploader', 'Unknown')
                }
                
                return filename, audio_info
                
        except Exception as e:
            logger.error(f"Error downloading audio: {e}")
            return None

# Global downloader instance
youtube_dl = YouTubeDownloader()