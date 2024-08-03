import os
import unittest
from unittest.mock import AsyncMock, patch
from discord.ext import commands
from discord import ApplicationContext
from bot.general import GeneralCommands
from bot.youtube import YouTubeCommands

# Устанавливаем заглушку для GUILD_ID
os.environ['GUILD_ID'] = '123456789'

class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = commands.Bot()
        self.general_cog = GeneralCommands(self.bot)
        self.youtube_cog = YouTubeCommands(self.bot)

    def test_hello_command_exists(self):
        self.assertIsNotNone(self.general_cog.hello)

    @patch('discord.ApplicationContext')
    async def test_hello_command_response(self, mock_ctx):
        mock_ctx.author = AsyncMock()
        mock_ctx.author.name = "TestUser"
        await self.general_cog.hello(mock_ctx)
        mock_ctx.respond.assert_called_once_with("Привет, TestUser!")

    def test_play_command_exists(self):
        self.assertIsNotNone(self.youtube_cog.play)

    def test_stop_command_exists(self):
        self.assertIsNotNone(self.youtube_cog.stop)

    @patch('discord.ApplicationContext')
    @patch('bot.youtube.YoutubeDL')
    async def test_play_command_no_voice_channel(self, mock_ytdl, mock_ctx):
        mock_ctx.author.voice = None
        await self.youtube_cog.play(mock_ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        mock_ctx.respond.assert_called_once_with("Вы должны быть в голосовом канале, чтобы использовать эту команду.")

    @patch('discord.ApplicationContext')
    @patch('discord.VoiceClient')
    async def test_stop_command(self, mock_voice_client, mock_ctx):
        mock_ctx.voice_client = mock_voice_client
        mock_voice_client.is_playing.return_value = True
        await self.youtube_cog.stop(mock_ctx)
        mock_voice_client.stop.assert_called_once()
        mock_voice_client.disconnect.assert_called_once()
        mock_ctx.respond.assert_called_once_with("Остановлено и отключено от голосового канала.")

if __name__ == '__main__':
    unittest.main()