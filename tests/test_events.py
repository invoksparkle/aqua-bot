import unittest
from unittest.mock import AsyncMock
from discord.ext import commands
from bot.events import BotEvents
import asyncio
import warnings

asyncio.set_event_loop(asyncio.new_event_loop())

class TestBotEvents(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = commands.Bot()
        self.events_cog = BotEvents(self.bot)

    async def test_on_ready_event(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=ResourceWarning)
            self.events_cog.bot = AsyncMock()
            self.events_cog.bot.user = "TestBot"
            self.events_cog.bot.dispatch = AsyncMock()

            await self.events_cog.on_ready()

if __name__ == '__main__':
    unittest.main()
