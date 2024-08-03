import unittest
from discord.ext import commands
from bot.general import GeneralCommands

class TestBot(unittest.TestCase):
    def setUp(self):
        self.bot = commands.Bot()
        self.cog = GeneralCommands(self.bot)

    def test_hello_command(self):
        self.assertIsNotNone(self.cog.hello)

if __name__ == '__main__':
    unittest.main()