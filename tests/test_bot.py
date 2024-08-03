import os
import unittest
import tracemalloc
from unittest.mock import AsyncMock, patch
from discord.ext import commands
from discord import ApplicationContext
from bot.general import GeneralCommands
from bot.youtube import YouTubeCommands
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())
tracemalloc.start()

# Устанавливаем заглушку для GUILD_ID
os.environ['GUILD_ID'] = '123456789'

class TestBot(unittest.IsolatedAsyncioTestCase):
    async def SetUp(self):
        self.bot = commands.Bot()
        self.general_cog = GeneralCommands(self.bot)
        self.youtube_cog = YouTubeCommands(self.bot)
    
    async def test_hello_command_exists(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_ctx.author.name = "TestUser"
        await self.general_cog.hello(mock_ctx)
        mock_ctx.respond.assert_called_once_with("Привет, TestUser!")

    async def test_play_command_no_voice_channel(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_ctx.author.voice = None
        await self.youtube_cog.play(mock_ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        mock_ctx.respond.assert_called_once_with("Вы должны быть в голосовом канале, чтобы использовать эту команду.")

    async def test_stop_command(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_voice_client = AsyncMock()
        mock_ctx.voice_client = mock_voice_client
        mock_voice_client.is_playing.return_value = True
        await self.youtube_cog.stop(mock_ctx)
        mock_voice_client.stop.assert_called_once()
        mock_voice_client.disconnect.assert_called_once()
        mock_ctx.respond.assert_called_once_with("Остановлено и отключено от голосового канала.")

if __name__ == '__main__':
    unittest.main()