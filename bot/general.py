import discord
from discord.ext import commands
from config.settings import GUILD_ID

class GeneralCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(guild_ids=[GUILD_ID])
    async def hello(self, ctx: discord.ApplicationContext):
        """Поздороваться с ботом"""
        await ctx.respond(f"Привет, {ctx.author}!")

def setup(bot):
    bot.add_cog(GeneralCommands(bot))
