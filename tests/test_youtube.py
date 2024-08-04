import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from discord import ApplicationContext
from bot.youtube import YouTubeCommands
import asyncio
import warnings

asyncio.set_event_loop(asyncio.new_event_loop())

class TestYouTubeCommands(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = commands.Bot()
        self.youtube_cog = YouTubeCommands(self.bot)
    
    async def test_play_command_no_voice_channel(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_ctx.defer = AsyncMock()
            mock_ctx.respond = AsyncMock()
            mock_ctx.author.voice = None
            await self.youtube_cog.play.callback(self.youtube_cog, mock_ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
            mock_ctx.respond.assert_called_once_with("Вы должны быть в голосовом канале, чтобы использовать эту команду.")

    async def test_stop_command(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_voice_client = AsyncMock()
            mock_voice_client.is_playing.return_value = True
            mock_voice_client.stop = MagicMock()
            mock_voice_client.disconnect = AsyncMock()
            mock_ctx.voice_client = mock_voice_client
            mock_ctx.respond = AsyncMock()
            await self.youtube_cog.stop.callback(self.youtube_cog, mock_ctx)
            mock_voice_client.stop.assert_called_once()
            mock_voice_client.disconnect.assert_awaited_once()
            mock_ctx.respond.assert_called_once_with("Остановлено и отключено от голосового канала.")

    @patch('bot.utils.YoutubeDL')
    @patch('discord.FFmpegPCMAudio', new_callable=AsyncMock)
    async def test_play_command_high_quality_thumbnail(self, mock_FFmpegPCMAudio, mock_YoutubeDL):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_ctx.defer = AsyncMock()
            mock_ctx.respond = AsyncMock()
            mock_ctx.author.voice = MagicMock()
            mock_ctx.author.voice.channel.connect = AsyncMock()

            mock_ydl_instance = MagicMock()
            mock_ydl_instance.extract_info.return_value = {
                'url': 'http://example.com/audio',
                'title': 'Test Title',
                'thumbnails': [
                    {'url': 'http://example.com/low_quality.jpg', 'preference': 1},
                    {'url': 'http://example.com/high_quality.jpg', 'preference': 2}
                ],
                'id': 'test_id'
            }
            mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

            await self.youtube_cog.play.callback(self.youtube_cog, mock_ctx, "http://example.com/video")

            mock_ctx.respond.assert_called_once()
            call_args = mock_ctx.respond.call_args
            if call_args:
                if call_args.args:
                    embed = call_args.args[0]
                else:
                    embed = call_args.kwargs.get('embed') 
            else:
                embed = None
            self.assertIsNotNone(embed, "Embed should not be None")
            self.assertEqual(embed.image.url, 'http://example.com/high_quality.jpg')

    @patch('bot.utils.YoutubeDL')
    @patch('discord.FFmpegPCMAudio', new_callable=AsyncMock)
    async def test_play_command_fallback_thumbnail(self, mock_FFmpegPCMAudio, mock_YoutubeDL):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_ctx.defer = AsyncMock()
            mock_ctx.respond = AsyncMock()
            mock_ctx.author.voice = MagicMock()
            mock_ctx.author.voice.channel.connect = AsyncMock()

            mock_ydl_instance = MagicMock()
            mock_ydl_instance.extract_info.return_value = {
                'url': 'http://example.com/audio',
                'title': 'Test Title',
                'thumbnails': [], 
                'id': 'test_id'
            }
            mock_YoutubeDL.return_value.__enter__.return_value = mock_ydl_instance

            await self.youtube_cog.play.callback(self.youtube_cog, mock_ctx, "http://example.com/video")
            
            mock_ctx.respond.assert_called_once()
            call_args = mock_ctx.respond.call_args
            embed = call_args.kwargs.get('embed') if call_args.kwargs else call_args.args[0]
            self.assertIsNotNone(embed, "Embed should not be None")
            self.assertEqual(embed.image.url, 'https://img.youtube.com/vi/test_id/maxresdefault.jpg')

    async def test_volume_up_command(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_ctx.voice_client = AsyncMock()
            mock_ctx.voice_client.source = MagicMock()
            mock_ctx.respond = AsyncMock()
            self.youtube_cog.volume = 0.5

            await self.youtube_cog.volume_up.callback(self.youtube_cog, mock_ctx)
            mock_ctx.respond.assert_called_once_with("Громкость установлена на 60%")
            self.assertEqual(mock_ctx.voice_client.source.volume, 0.6)

    async def test_volume_down_command(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_ctx = AsyncMock(spec=ApplicationContext)
            mock_ctx.voice_client = AsyncMock()
            mock_ctx.voice_client.source = MagicMock()
            mock_ctx.respond = AsyncMock()
            self.youtube_cog.volume = 0.5

            await self.youtube_cog.volume_down.callback(self.youtube_cog, mock_ctx)
            mock_ctx.respond.assert_called_once_with("Громкость установлена на 40%")
            self.assertEqual(mock_ctx.voice_client.source.volume, 0.4)

    async def test_disconnect_after_playback(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=RuntimeWarning)
            mock_voice_client = AsyncMock()
            await self.youtube_cog.disconnect_after_playback(mock_voice_client)
            mock_voice_client.disconnect.assert_awaited_once()

if __name__ == '__main__':
    unittest.main()
