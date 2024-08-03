import os
import unittest
import tracemalloc
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from discord import ApplicationContext
from bot.general import GeneralCommands
from bot.youtube import YouTubeCommands
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())
tracemalloc.start()

os.environ['GUILD_ID'] = '123456789'

class TestBot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = commands.Bot()
        self.general_cog = GeneralCommands(self.bot)
        self.youtube_cog = YouTubeCommands(self.bot)
    
    async def test_hello_command_exists(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_ctx.respond = AsyncMock()
        mock_ctx.author.name = "TestUser"
        await self.general_cog.hello.callback(self.general_cog, mock_ctx)
        mock_ctx.respond.assert_called_once_with(f"Привет, {mock_ctx.author}!")

    async def test_play_command_no_voice_channel(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_ctx.defer = AsyncMock()
        mock_ctx.respond = AsyncMock()
        mock_ctx.author.voice = None
        await self.youtube_cog.play.callback(self.youtube_cog, mock_ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        mock_ctx.respond.assert_called_once_with("Вы должны быть в голосовом канале, чтобы использовать эту команду.")

    async def test_stop_command(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_voice_client = MagicMock()
        mock_voice_client.is_playing.return_value = True
        mock_voice_client.stop = AsyncMock()
        mock_voice_client.disconnect = AsyncMock()
        mock_ctx.voice_client = mock_voice_client
        mock_ctx.respond = AsyncMock()
        await self.youtube_cog.stop.callback(self.youtube_cog, mock_ctx)
        mock_voice_client.stop.assert_called_once()
        mock_voice_client.disconnect.assert_called_once()
        mock_ctx.respond.assert_called_once_with("Остановлено и отключено от голосового канала.")

    @patch('bot.youtube.YoutubeDL')
    async def test_play_command_string_thumbnail(self, mock_YoutubeDL):
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

        with patch('bot.youtube.discord.FFmpegOpusAudio.from_probe', new_callable=AsyncMock) as mock_from_probe:
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

        # Проверяем вызов к maxresdefault.jpg
        mock_ydl_instance.extracct_info.return_value['thumbnails'] = []
        await self.youtube_cog.play.callback(self.youtube_cog, mock_ctx, "http://example.com/video")
        call_args = mock_ctx.respond.call_args
        if call_args:
            if call_args.args:
                embed = call_args.args[0]
            else:
                embed = call_args.kwargs.get('embed')
        else:
            embed = None
        self.assertIsNotNone(embed, "Embed should not be None")
        self.assertEqual(embed.image.url, 'https://img.youtube.com/vi/test_id/maxresdefault.jpg')


if __name__ == '__main__':
    unittest.main()