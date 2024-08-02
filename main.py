import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

# Получение ID гильдии из переменной окружения
GUILD_ID = os.getenv('GUILD_ID')
if GUILD_ID is None:
    raise ValueError("GUILD_ID environment variable is not set")
GUILD_ID = int(GUILD_ID)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} is ready.')

# Гильдейская команда
@bot.slash_command(guild_ids=[GUILD_ID])
async def hello(ctx: discord.ApplicationContext):
    """Say hello to the bot"""
    await ctx.respond(f"Hello {ctx.author}!")

bot.run(os.getenv('DISCORD_TOKEN'))
