import unittest
from unittest.mock import AsyncMock
from discord.ext import commands
from discord import ApplicationContext
from bot.general import GeneralCommands
import asyncio

asyncio.set_event_loop(asyncio.new_event_loop())

class TestGeneralCommands(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = commands.Bot()
        self.general_cog = GeneralCommands(self.bot)
    
    async def test_hello_command_exists(self):
        mock_ctx = AsyncMock(spec=ApplicationContext)
        mock_ctx.respond = AsyncMock()
        mock_ctx.author.name = "TestUser"
        await self.general_cog.hello.callback(self.general_cog, mock_ctx)
        mock_ctx.respond.assert_called_once_with(f"Привет, {mock_ctx.author}!")

if __name__ == '__main__':
    unittest.main()
