import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = discord.Bot(intents=intents)

# Получение ID гильдии из переменной окружения
GUILD_ID = os.getenv('GUILD_ID')
if GUILD_ID is None:
    raise ValueError("Переменная окружения GUILD_ID не установлена")
GUILD_ID = int(GUILD_ID)

@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов.')

# Гильдейская команда
@bot.slash_command(guild_ids=[GUILD_ID])
async def hello(ctx: discord.ApplicationContext):
    """Поздороваться с ботом"""
    await ctx.respond(f"Привет, {ctx.author}!")

bot.run(os.getenv('DISCORD_TOKEN'))
