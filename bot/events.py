import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info(f'Бот {self.bot.user} готов.')

def setup(bot):
    bot.add_cog(BotEvents(bot))
